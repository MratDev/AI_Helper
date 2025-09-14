import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

st.title("AI Helper")

col1, col2 = st.columns([1,3])

with col1:
    option = st.selectbox(
        "Choose what to do:",
        ["Web Dom Scraper", "File Data Analysis", "Web research", "Essay Writing"]
    )

if option == "Web Dom Scraper":
    from web_scraper import scraper
    scraper(col2)
    
elif option == "File Data Analysis":
    from RAG import RAG
    RAG(col2)

elif option == "Web research":
    from research import run
    run(col2)

elif option == "Essay Writing":
    from essays import write_essay
    write_essay(col2)