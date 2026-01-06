import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS

def get_sop_context(query):
    # 1. Load your 38-page Markdown file
    loader = TextLoader("SOP.md")
    docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(loader.load())
    
    # 2. Use Cohere for high-volume embedding (2,000 requests/min)
    embeddings = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )
    
    # 3. Create searchable index
    vectorstore = FAISS.from_documents(docs, embeddings)
    relevant_docs = vectorstore.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in relevant_docs])
