import streamlit as st
import tempfile
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def RAG(col2):
    with col2:
        st.title("File Data Analysis")        
        
        if 'qa_chain' not in st.session_state:
            st.session_state.qa_chain = None

        file = st.file_uploader(label="Load A File To Analyze", type=["pdf", "docx", "txt"])
        execute = st.button("Load")

        if execute and file is not None:
            mime_type = file.type
            with st.spinner('Processing your request...'):
                with tempfile.NamedTemporaryFile(delete=False) as temporary_file:
                    temporary_file.write(file.read())
                if mime_type == "application/pdf":
                    pdf_loader = PyPDFLoader(temporary_file.name)
                    pages = pdf_loader.load()
                elif mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    docx_loader = Docx2txtLoader(temporary_file.name)
                    pages = docx_loader.load()
                elif mime_type == "text/plain":
                    txt_loader = TextLoader(temporary_file.name, encoding="utf-8")
                    pages = txt_loader.load()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=100
                )
                chunks = text_splitter.split_documents(pages)

                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

                vectorstore = Chroma.from_documents(
                    chunks,
                    embeddings,
                    persist_directory="chroma_db"
                )
                st.session_state.qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=vectorstore.as_retriever()
                )
                st.success("Document Loaded Successfully!")
        
        if st.session_state.qa_chain is not None:
            query = st.text_area("What do you want to know? ")
            ask = st.button("Submit Question")
            if ask and query:
                with st.spinner('Getting answer...'):
                    response = st.session_state.qa_chain.invoke(query)["result"]
                    st.write(response)  

                    if st.button("Clear Results"):
                        st.session_state.qa_chain = None
                        st.rerun()