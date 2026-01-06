import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def get_sop_context(query):
    # 1. Load your specific 38-page file
    loader = Docx2txtLoader("IT-Incident-Response-SOP.docx")
    documents = loader.load()
    
    loader = TextLoader("IT-Incident-Response-SOP.docx")
    docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(loader.load())
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    return "\n".join([d.page_content for d in vectorstore.similarity_search(query, k=2)])
