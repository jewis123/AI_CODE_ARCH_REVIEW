


import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from agents.code_analyzer import code_analyzer

smell_question = "分析所提供LUA代码的异味，并提供改进建议。（如果没有可改进的地方，输出“无需改进”），使用markdown格式输出。"

response = code_analyzer("G:\\WorkSpace\\evo_lua\\Framework\\core\\manager\\ActiveManager.lua", smell_question, True)

with open("docs/smell_analyze_local.md", "w", encoding="utf-8") as f:
    f.write(response)