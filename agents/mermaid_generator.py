import os
import re
import time
from chromadb import Collection
from utils.models_util import get_dpv3_LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel


def remove_special_chars(text):
    # 定义一个正则表达式模式，匹配反斜杠和单引号
    pattern = r"[\\'\r\n]"
    # 使用 re.sub 函数替换匹配的字符为空字符串
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def mermaid_generator(query, collection:Collection, model:BaseChatModel):  
    """  
    根据查询语句，在 ChromaDB 数据库中搜索相关的代码结构信息，  
    然后使用 LLM 生成 Mermaid 代码。  
    """  
    
    llm = get_dpv3_LLM()
    
    query_embedding = model.encode(query).tolist()  
    results = collection.query(  
        query_embeddings=[query_embedding],  
        n_results=300  # 可以调整搜索结果数量  
    )  

    context = ""
    for metadata in results['metadatas'][0]:
        context += remove_special_chars(f"Class: {metadata['className']}, ClassParent:{metadata['classParent']}, ClassDenpend:{metadata['classDependencies']}") + "\n"

    cleaned_context = context
    prompt = f"""你是一个 Mermaid 代码生成器。 请根据以下代码结构信息，生成 Mermaid 代码，描述类之间的关系 (继承、实现、依赖等)。  信息：\"{cleaned_context}\" 。 要求：请只输出 Mermaid 代码，不要包含其他任何文字。 使用 standard UML class diagram 语法。  
    Mermaid 语法使用 `classDiagram` 开头.  请包含必要的连接符 (例如: `<|--`, `--`, `*--`, `o--`) 来表示关系。  
    """

    chain = PromptTemplate.from_template(prompt) | llm | StrOutputParser()
    startTime = time.time()
    mermaid_code = chain.invoke({})
    endTime = time.time()
    print(f"Mermaid 代码生成耗时: {endTime - startTime} s")
    return mermaid_code  

def save_mermaid_file(mermaid_code):  
    """将 Mermaid 代码保存到 .mmd 文件."""  
    if  mermaid_code == "":
        return
    
    output_file = os.getenv("MERMAID_SAVE_PATH")
    with open(output_file, "w", encoding="utf-8") as f:  
        f.write(mermaid_code)  
    print(f"Mermaid 文件已保存到: {output_file}")  
