from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from models_util import get_dpv3_LLM
import time

def code_analyzer(file_path, question):
    
    loader = TextLoader(file_path, autodetect_encoding = True)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_language(language=Language.CSHARP, chunk_size=200, chunk_overlap=50)
    sliced = splitter.split_documents(docs)
    
    llm = get_dpv3_LLM()
    # 创建记忆存储
    memory = ConversationBufferMemory()
    
    # 定义提示模板
    template = """你是一个代码分析专家。请基于之前存储的所有代码片段，回答用户的问题。
    
    历史代码片段:
    {history}
    
    当前问题: {input}
    
    请给出分析回答:"""
    
    prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
    
    # 创建对话链
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )
    
    for slice in sliced:
        memory.chat_memory.add_user_message(slice.page_content)
    
    

    start_time = time.time()
    result = chain.invoke(question)
    end_time = time.time()
    
    print(f"文件：{file_path}，耗时：{end_time - start_time} s")    
    return result['response']
    
