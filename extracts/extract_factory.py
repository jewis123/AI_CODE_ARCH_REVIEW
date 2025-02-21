from typing import List, Tuple
from tree_sitter import Node
from .extract_csharp import extract_csharp
from langchain_text_splitters import Language 

def extract_factory(node:Node, file_path: str, language:str) -> List[Tuple]:
    """根据节点类型调用对应的提取器"""
    if language == Language.CSHARP:
        return [(file_path, extract_csharp(node))]
    else:
        return []
    
