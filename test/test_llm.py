import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from utils import get_dpv3_LLM, get_dpr1_LLM ,get_dqr1_7b_LLM,get_dpv3_LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

import time
import tiktoken
import re


encoding = tiktoken.get_encoding("cl100k_base")
local_llm = ChatOllama(model="deepseek-r1:7b")
prompt = "用python写一个斐波那契函数。要求：只需要一种写法,不要输出非代码内容。"
def remove_think_tags(text):
    # 使用正则表达式匹配 <think> 标签及其中的内容
    pattern = r'<think>.*?</think>'
    # 使用 re.sub 函数替换匹配的内容为空字符串
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return cleaned_text
print("------------------加载本地模型 OVer--------------------------------")

# llm = get_dpv3_LLM()
# chain = PromptTemplate.from_template(prompt) | llm | StrOutputParser()
# start_time = time.time()
# result = chain.invoke({})
# token_count = len(encoding.encode(result))
# end_time = time.time()
# print(result)
# usedTime1 = end_time - start_time
# speed = token_count / usedTime1
# print(f"api-v3 耗时：{usedTime1} s,有效tokens: {token_count}, 生成速度：{speed} tokens/s")

# print("--------------------------------------------------")


# llm = get_dqr1_7b_LLM()
# chain = PromptTemplate.from_template(prompt) | llm | StrOutputParser()
# start_time = time.time()
# result = chain.invoke({})
# end_time = time.time()
# token_count = len(encoding.encode(result))
# print(result)
# usedTime1 = end_time - start_time
# speed = token_count / usedTime1
# print(f"api-7b 耗时：{usedTime1} s,有效tokens: {token_count}, 生成速度：{speed} tokens/s")

# print("--------------------------------------------------")
# llm = get_dpr1_LLM()
# chain = PromptTemplate.from_template(prompt) | llm | StrOutputParser()
# start_time = time.time()
# result = chain.invoke({})
# end_time = time.time()
# token_count = len(encoding.encode(result))
# print(result)
# usedTime1 = end_time - start_time
# speed = token_count / usedTime1
# print(f"api-max 耗时：{usedTime1} s,有效tokens: {token_count}, 生成速度：{speed} tokens/s")

# print("--------------------------------------------------")

chain = PromptTemplate.from_template(prompt) | local_llm | StrOutputParser()
start_time = time.time()
rst = chain.invoke({})
end_time = time.time()
result = remove_think_tags(rst)
token_count = len(encoding.encode(result))
print(result)
usedTime1 = end_time - start_time
speed = token_count / usedTime1
print(f"local 耗时：{usedTime1} s, 有效tokens: {token_count}, 生成速度：{speed} tokens/s")