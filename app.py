import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools import server_health_check, restart_service
from knowledge_engine import get_sop_context

load_dotenv()

st.title("🤖 Hybrid SRE Agent (Gemini + Cohere)")

log_input = st.text_area("Paste Incident Log")

if st.button("🚀 Execute Fix"):
    # 1. RAG Search through 38 pages (via Cohere)
    sop_context = get_sop_context(log_input)
    
    # 2. Setup Agent Brain (via Gemini)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    tools = [server_health_check, restart_service]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SRE. Use this SOP to fix the issue: {context}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Modern create_agent for LangChain v1.0
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # 3. Run the agentic loop
    response = executor.invoke({"input": log_input, "context": sop_context})
    st.success(f"### Resolution:\n{response['output']}")




