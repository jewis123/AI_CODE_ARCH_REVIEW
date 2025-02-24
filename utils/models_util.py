import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

def get_dpr1_LLM():
    return ChatOpenAI(
        model=os.environ.get("ARK_R1_MODEL"),
        api_key=os.environ.get("ARK_API_KEY"),
        base_url=os.environ.get("ARK_API_URL"),
    )
    
def get_dqr1_7b_LLM():
    return ChatOpenAI(
        model=os.environ.get("ARK_R17b_MODEL"),
        api_key=os.environ.get("ARK_API_KEY"),
        base_url=os.environ.get("ARK_API_URL"),
    )
    
def get_dpv3_LLM():
    return ChatOpenAI(
        model=os.environ.get("ARK_V3_MODEL"),
        api_key=os.environ.get("ARK_API_KEY"),
        base_url=os.environ.get("ARK_API_URL"),
    )
    
def get_gemini_LLM():
    return ChatGoogleGenerativeAI(
        model = os.environ.get("GEMINI_MODEL"),
        api_key = os.environ.get("GEMINI_API_KEY")
    )
    
def get_local_dp_LLM():
    return ChatOllama(ChatOllama(model="deepseek-r1:14b"))