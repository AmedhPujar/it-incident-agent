import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def get_sop_context(query):
    if not os.path.exists("SOP.md"):
        return "SOP.md not found. Please verify the file exists."

    loader = TextLoader("SOP.md")
    documents = loader.load()
    
    # 2. Split into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    
    # 3. Create searchable index
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # 4. Search and return top context
    relevant_docs = vectorstore.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in relevant_docs])
