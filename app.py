import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools import server_health_check, restart_service
from knowledge_engine import get_sop_context

load_dotenv()

# 1. Setup the Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Define the Agent Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an SRE Agent. Use the following SOP context to fix the user issue: {context}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 3. Initialize Agent & Tools
tools = [server_health_check, restart_service]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Streamlit UI
st.title("🤖 LangChain SRE Agent")
log_input = st.text_area("Paste Server Log")

if st.button("Resolve Incident"):
    # RAG lookup from your 38-page SOP
    sop_section = get_sop_context(log_input)
    
    # Run the Agentic loop
    response = agent_executor.invoke({
        "input": log_input,
        "context": sop_section
    })
    st.success(response["output"])
