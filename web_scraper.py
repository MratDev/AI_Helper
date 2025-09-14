# PARSING

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


llm = ChatOpenAI(model="gpt-4o-mini")

def parse_with_ai(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)
        result = parsed_results[0].content

    return result

# SCRAPING

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Lauinching chrome browser...")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_lenght=6000):
    return[dom_content[i:i+max_lenght] for i in range (0, len(dom_content), max_lenght)]

# UI + FUNCTIONALITY

import streamlit as st

def scraper(col2):
    with col2:
        st.title("AI Web Scraper")
        url = st.text_input("Enter Website URL")

        if st.button("Scrape Website"):
            if url:
                st.write("Scraping the website...")

                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                st.session_state.dom_content = cleaned_content

                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)

        if "dom_content" in st.session_state:
            parse_description = st.text_area("Describe what you want to parse")

            if st.button("Parse Content"):
                if parse_description:
                    st.write("Parsing the content...")

                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ai(dom_chunks, parse_description)
                    st.write(parsed_result)