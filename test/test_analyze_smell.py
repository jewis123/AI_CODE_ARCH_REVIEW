
    
from agents.code_analyzer import code_analyzer

smell_question = "分析所提供LUA代码的异味，并提供改进建议。（如果没有可改进的地方，输出“无需改进”），使用markdown格式输出。"

response = code_analyzer("G:\\WorkSpace\\evo_lua\\Framework\\core\\manager\\ActiveManager.lua", smell_question)

with open("docs/smell_analyze.md", "w", encoding="utf-8") as f:
    f.write(response)