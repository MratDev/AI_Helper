from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# TOOLS

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def generate(topic: str) -> str:
    '''Generates text for project based on users input.'''
    messages = [
        ("system", "You are a student that writes an essay."),
        ("human", "Write an essay on the topic {topic}. The range is 200 - 220 words.")
    ]
    template = ChatPromptTemplate.from_messages(messages)
    prompt = template.invoke({"topic": topic})
    response = llm.invoke(prompt)
    return response.content

@tool
def review(text: str) -> str:
    '''Writes the review of the text and tells what to improve.'''
    messages = [
        ("system", "You are a teacher that reviews an essay."),
        ("human", "Write an review to the following essay: {text}")
    ]
    template = ChatPromptTemplate.from_messages(messages)
    prompt = template.invoke({"text": text})
    response = llm.invoke(prompt)
    return response.content

@tool
def improve_text(text:str, text_review:str) -> str:
    '''Edits the text of the project based on the review fo the text.'''
    messages = [
        ("system", "You are a student that writes an essay."),
        ("human", "Rewrite following essay: {text} Write it based on following review: {review}")
    ]
    template = ChatPromptTemplate.from_messages(messages)
    prompt = template.invoke({"text": text, "review": text_review})
    response = llm.invoke(prompt)
    return response

@tool
def get_keywords(text:str) -> str:
    '''Creates keywords or phrases for powerpoint presentation based on text.'''
    messages = [
        ("system", "You are a student that makes a powerpoint presentation."),
        ("human", "Write keywords or phrases for powerpoint presentation to the following essay: {text}")
    ]
    template = ChatPromptTemplate.from_messages(messages)
    prompt = template.invoke({"text": text})
    response = llm.invoke(prompt)
    return response

@tool
def combine_text(text:str, keywords:str):
    '''Combines text of the projext and keywords.'''
    combined_text = text + "\n\n" + keywords
    return combined_text

def send_by_email(receiver_email:str, text:str):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("GOOGLE_APP_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Essay"

    body = text
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent!")


tools = [generate, review, improve_text, get_keywords, combine_text]

import streamlit as st

def write_essay(col2):
    with col2:
        st.title("Essay writing")
        
        # Initialize session state
        if 'essay_result' not in st.session_state:
            st.session_state.essay_result = None
        if 'essay_topic' not in st.session_state:
            st.session_state.essay_topic = ""

        topic = st.text_input("The topic for the essay")
        generate = st.button("Generate")

        agent = create_react_agent(llm, tools)

        # Generation logic
        if topic and generate:
            with st.spinner("Generating essay..."):
                try:
                    result = agent.invoke({"messages": [
                        ("system", "You are a helpful assistant that helps users with their essays."
                        " You have to generate, review, and improve essays, create keywords for presentations, and combine text in following order."),
                        ("human", topic)
                    ]})

                    st.session_state.essay_result = result["messages"][-1].content
                    st.session_state.essay_topic = topic
                    st.success("Essay generated successfully!")

                except Exception as e:
                    st.error(f"Essay generation failed: {str(e)}")

        # Display results (MOVED OUTSIDE the generation block)
        if st.session_state.essay_result is not None:
            st.subheader(f"Essay Results for: {st.session_state.essay_topic}")
            st.write(st.session_state.essay_result)

            # Email functionality - now persistent
            send_email = st.checkbox("Send Output By Email", key="send_email_checkbox")
            if send_email:
                email = st.text_input("Enter Your Email", key="email_input")
                send = st.button("Send", key="send_button")
                if send and email:
                    try:
                        send_by_email(email, st.session_state.essay_result)
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Failed to send email: {str(e)}")

            # Clear functionality
            if st.button("Clear Results", key="clear_results_button"):
                st.session_state.essay_result = None
                st.session_state.essay_topic = ""
                st.rerun()