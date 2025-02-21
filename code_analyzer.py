import os
from pathlib import Path
from typing import List, Optional, Tuple
import diskcache as dc

global_cache = dc.Cache('.global_ast_cache')


class CodeAnalyzer:
    def __init__(self, repo_path: str):
        if not os.path.exists(repo_path) or repo_path == "":
            raise FileNotFoundError(f"目录不存在: {repo_path}")
        self.repo_path = Path(repo_path)
        
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """根据文件扩展名检测编程语言"""
        from tree_sitter import Language
        import tree_sitter_python as tspython
        import tree_sitter_c_sharp as tscsharp
        
        ext = Path(file_path).suffix.lower()
        return {
            '.py': Language(tspython.language()),
            '.cs': Language(tscsharp.language()),
        }.get(ext, None)
    
    @global_cache.memoize(expire=3600, tag='ast_parser')
    def parse_file(self, file_path: str, content:str, language:str) -> List[Tuple]:
        """解析单个文件并缓存结果"""
        from tree_sitter import Tree, Parser
        from extracts.extract_factory import extract_factory
        
        lang = self.detect_language(file_path)
        
        if lang is None:
            return []
        
        print(f"解析文件: {file_path}, 文本长度: {len(content)}")
        parser:Parser = Parser(lang)
        code_bytes = bytes(content, 'utf-8')
        
        try:
            tree:Tree = parser.parse(code_bytes)
        except Exception as e:
            print(f"解析错误: {str(e)}")
            return []
        
        return extract_factory(tree.root_node, file_path, language)