import os
import time
from models_util import get_dpv3_LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def framework_analyzer():
    """
    根据给定的架构mermaid文件，调用LLM进行多角度分析，给出评审建议
    """
    
    with open(os.getenv("MERMAID_SAVE_PATH"), "r", encoding="utf-8") as f:
        mermaid_code = f.read()
        
    llm = get_dpv3_LLM()  
        
    prompt=f"""你是一个代码架构评审专家。请根据以下 Mermaid UML，分析架构设计是否合理，多角度给出评审意见。UML:\"{mermaid_code}\"。"""
    
    chain = PromptTemplate.from_template(prompt) | llm | StrOutputParser()
    startTime = time.time()
    rst = chain.invoke({})
    endTime = time.time()
    print(f"mermaid分析耗时：{endTime - startTime} s")
    return rst  