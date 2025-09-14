# 🤖 AI Helper - Intelligent Assistant for Everything

A comprehensive AI-powered application built with **Streamlit**, combining web scraping, document analysis, research, and essay generation into a single modern interface.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)  
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)  
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)  
![LangChain](https://img.shields.io/badge/LangChain-0.1+-purple.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [Modules](#-modules)
- [Requirements](#-requirements)
- [Project Structure](#-project-structure)

## ✨ Features

### 🕷️ **Web DOM Scraper**
- Automatic content extraction from websites  
- AI-powered parsing for specific data  
- Support for static and dynamic pages  
- Chrome WebDriver integration  

### 📊 **File Data Analysis (RAG)**
- Intelligent analysis of PDF, DOCX, and TXT files  
- Retrieval-Augmented Generation technology  
- Document Q&A system  
- Vector search with OpenAI embeddings  

### 🔍 **Web Research**
- Multi-agent research system  
- Automatic fact-checking  
- Bias detection and analysis  
- APA-style citations  
- 5-step research process  

### ✍️ **Essay Writing**
- AI-generated essays (200–220 words)  
- Automatic review and improvement  
- Keyword generation for presentations  
- Email export functionality  

## 🚀 Installation

### Prerequisites
- Python 3.9+  
- Installed Chrome browser  
- OpenAI API key  
- Tavily API key (for research)  

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-helper.git
cd ai-helper
```

### 2. Create a Virtual Environment
```bash
python -m venv ai_helper_env
source ai_helper_env/bin/activate  # Linux/Mac
# or
ai_helper_env\Scriptsctivate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create the .env File
```bash
cp .env.example .env
```

### 2. Set API Keys in .env
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Tavily API (for research)
TAVILY_API_KEY=your_tavily_api_key_here

# Email configuration
SENDER_EMAIL=your_email
GOOGLE_APP_PASSWORD=your_google_app_password_here
```

### 3. Get Your API Keys

#### OpenAI API:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and go to API Keys
3. Generate a new API key

#### Tavily API:
1. Visit [Tavily](https://tavily.com/)
2. Register and get your API key

#### Google App Password:
1. Enable 2FA on your Google account  
2. Generate an App Password in account settings  
3. Use this password instead of your regular password  

## 🏃 Running the App

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 🧩 Modules

### 📁 Project Structure
```
ai-helper/
│
├── main.py                 # Main application
├── essays.py               # Essay writing module
├── research.py             # Web research module  
├── RAG.py                  # Document analysis module
├── web_scraper.py          # Web scraping module
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .env.example            # Example environment file
├── chromedriver.exe        # Chrome WebDriver
└── README.md               # Documentation
```

### 🔧 Main Components

#### main.py
- Streamlit application  
- Module navigation  
- Responsive design  

#### essays.py
- LangGraph agents for essay workflow  
- OpenAI GPT-4 integration  
- Email export functionality  

#### research.py
- Multi-agent research system  
- Tavily search integration  
- Fact-checking and bias detection  
- Citation formatting  

#### RAG.py
- Document loading (PDF, DOCX, TXT)  
- Text chunking and embeddings  
- Chroma vector database  
- RetrievalQA chains  

#### web_scraper.py
- Selenium WebDriver automation  
- BeautifulSoup HTML parsing  
- AI-powered content extraction  
- Smart content filtering  

## 📦 Requirements

### Python Packages
```txt
streamlit
langchain
langchain-openai
langchain-community
langgraph
openai
tavily-python
selenium
beautifulsoup4
python-dotenv
chromadb
```

## 🚨 Troubleshooting

### Common Issues

#### ChromeDriver Errors
```bash
# Make sure ChromeDriver is in PATH or in the project root folder
# Verify compatibility with your installed Chrome version
```

#### OpenAI API Errors
```bash
# Check if your API key is valid
# Verify available credits on your OpenAI account
# Check for rate limits
```

#### Memory Issues with Large Files
```bash
# Reduce chunk_size in RAG.py
# Use smaller documents
# Increase system memory
```

## 🛡️ Security

### API Keys
- **Never** share API keys publicly  
- Use `.env` files for credentials  
- Rotate keys regularly  

### Data
- Local document processing  
- No persistent storage of sensitive data  
- GDPR-compliant processing  

## 📈 Future Improvements

- [ ] **HTML Frontend + Docker**  
- [ ] **API Endpoints**  

<p align="center">
  <strong>Made with ❤️ for the AI community</strong>
</p>

<p align="center">
  <a href="#top">⬆️ Back to Top</a>
</p>
