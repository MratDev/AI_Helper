from tavily import TavilyClient
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain.tools import tool
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

client = TavilyClient()

# AGENTS & TOOLS

# SEARCH

@tool
def date():
    '''Return current date and time in the system's local timezone, required for current data search'''
    current_date = datetime.now()
    return current_date.strftime("%Y-%m-%d %H:%M:%S")

@tool
def search(query: str, max_results: int) -> str:
    '''Searches the web for results. Requires query and number of maximum results that should be set by relevance'''
    try:
        results = client.search(query=query,max_results=max_results)
        
        formatted_results = []
        for r in results["results"]:
            formatted_results.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r.get('content', r.get('snippet', ''))}\n---")
        
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Web search failed: {str(e)}. Please try a different query."
    
search_agent = create_react_agent(
    model=llm,
    tools=[date, search],
)

@tool
def search_agent_chain(query: str) -> str:
    """Uses the Search Agent to gather information"""
    response = search_agent.invoke({"messages": [
        ("system", "You are a search agent. Your task is to gather information from the web."),
        ("human", query)
        ]})
    return response["messages"][-1].content

# SYNTHESIZER
    
synthesizer_agent = create_react_agent(
    model=llm,
    tools=[]
)

@tool
def synthesizer_agent_chain(search_results: str, user_query: str) -> str:
    '''    
    Uses the Synthesizer Agent to create a final response:
    Synthesizes research results into a comprehensive response
    Process and combine information from multiple sources
    Create coherent narrative addressing the user's query
    Organize information logically with clear structure
    '''
    response = synthesizer_agent.invoke({"messages": [
        ("system", "You are a synthesizer agent. Your task is to create a coherent narrative from the search results."),
        ("human", f"Search Results: {search_results}\nUser Query: {user_query}")
    ]})
    return response["messages"][-1].content

# CITATIONS

citation_agent = create_react_agent(
    model=llm,
    tools=[search]
)

@tool
def citation_agent_chain(sources: str, style: str = "APA") -> str:
    '''
    Uses the Citation Agent to format sources: 
    Format sources into proper citations
    Parse source information (URL, title, date, author if available)
    Format according to citation style (APA, MLA, Chicago)
    Return formatted bibliography

    and validate sources:
    Validate source credibility and accessibility
    Check if URLs are accessible
    Assess domain authority/credibility
    Check publication dates
    '''
    response = citation_agent.invoke({"messages": [
        ("system", "You are a citation assistant. Your task is to format sources into proper citations."),
        ("human", f"Sources: {sources}\nStyle: {style}")
    ]})
    return response["messages"][-1].content

# FACTS CHECK

fact_checker_agent = create_react_agent(
    model=llm,
    tools=[search]
)

@tool
def fact_checker_agent_chain(claims: str, sources: str) -> str:
    '''
    Uses the Fact Checker Agent to verify claims:
    Cross-reference key claims against multiple sources
    Extract key factual claims from the content
    Search for additional sources to verify each claim
    Return confidence scores and conflicting information
    '''
    response = fact_checker_agent.invoke({"messages": [
        ("system", "You are a fact-checking assistant. Your task is to verify claims against credible sources."),
        ("human", f"Claims: {claims}\nSources: {sources}")
    ]})
    return response["messages"][-1].content

# BIAS

bias_detection_agent = create_react_agent(
    model=llm,
    tools=[search]
)

@tool
def bias_detection_agent_chain(content: str) -> str:
    '''    
    Use the Bias Detection Agent to analyze content
    Analyzes content for potential bias indicators
    Look for loaded language, one-sided perspectives
    Identify missing counterarguments
    Flag potential conflicts of interest in sources
    '''
    response = bias_detection_agent.invoke({"messages": [
        ("system", "You are a bias detection assistant. Your task is to analyze content for potential bias indicators."),
        ("human", f"Content: {content}")
    ]})
    return response["messages"][-1].content

# SUPERVISOR

supervisor_agent = create_react_agent(
    model=llm,
    tools=[search_agent_chain, synthesizer_agent_chain, citation_agent_chain, fact_checker_agent_chain, bias_detection_agent_chain]
)

# UI + Functionality

import streamlit as st

def send_by_email(text:str, email:str):
    sender_email = "aih235795@gmail.com"
    receiver_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("GOOGLE_APP_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Research"

    body = text
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    # st.write("Email sent!")  # Removed to avoid duplicate feedback


def run(col2):
    with col2:
        st.title("Web Research")
        if 'research_result' not in st.session_state:
            st.session_state.research_result = None
        if 'research_topic' not in st.session_state:
            st.session_state.research_topic = ""
            
        topic = st.text_input("What Would You Like To Research")
        search = st.button("Search")
        
        if search and topic:
            with st.spinner("Researching..."):
                try:
                    result = supervisor_agent.invoke(
                        {"messages": [
                            ("system", 
                             "You are a world-class web research assistant. Your task is to perform thorough, unbiased, and up-to-date research on any topic provided by the user."
                             "Your workflow consists of **five steps**, and you must execute each one **in order**, using the corresponding tool:"

                             "1) **Search**: Use `search_tool` to find relevant and credible sources. Return only factual search results."
                             "2) **Synthesize**: Use `synthesizer_tool` to generate a clear, structured, and comprehensive summary of the search results."
                             "3) **Citations**: Use `citation_tool` to format and validate references for the summarized content."
                             "4) **Fact-Check**: Use `fact_checker_tool` to verify key claims and indicate confidence levels."
                             "5) **Bias Analysis**: Use `bias_analyzer_tool` to highlight potential bias or conflicting information."

                             "**Rules:**"
                             "- Do **not skip any step**."
                             "- Use the tool explicitly assigned for each step; do not invent steps or tools."
                             "- Cite all sources and indicate confidence levels."
                             "- Clearly state limitations if information is unavailable or uncertain."
                             "- Use concise, professional language and organize output for easy understanding."

                             "When a step is completed, return only the information required for the next tool or the final output. Do not generate unrelated content."
                            ),
                            ("human", topic)
                        ]})
                    
                    st.session_state.research_result = result["messages"][-1].content
                    st.session_state.research_topic = topic
                    
                    st.success("Research completed!")
                    
                except Exception as e:
                    st.error(f"Research failed: {str(e)}")
        
        if st.session_state.research_result is not None:
            st.subheader(f"Research Results for: {st.session_state.research_topic}")
            st.write(st.session_state.research_result)
            
            send_email = st.checkbox("Send Output By Email")
            if send_email:
                email = st.text_input("Enter Your Email")
                send = st.button("Send")
                if send and email:
                    try:
                        send_by_email(st.session_state.research_result, email)
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Failed to send email: {str(e)}")

            if st.button("Clear Results"):
                st.session_state.research_result = None
                st.session_state.research_topic = ""
                st.rerun()