import os
import time
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
    batch_size=10
    vectorstore = None
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            vectorstore.add_documents(batch)
        
        # Wait 5 seconds between batches to avoid the 429 error
        time.sleep(5) 
    
    return "\n".join([d.page_content for d in vectorstore.similarity_search(query, k=2)])
