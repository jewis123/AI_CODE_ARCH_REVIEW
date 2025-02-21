import ast
import re  
from langchain_community.document_loaders import TextLoader,DirectoryLoader

def remove_fullwidth_chars(text):
    """移除全角字符."""
    # 使用正则表达式匹配全角字符并移除
    return re.sub(r'[\uFF01-\uFF5E\u3000]', '', text)



def extract_code_structure(dir_path):  
    """提取 Python 代码文件的类和方法信息."""  
    loader = DirectoryLoader(dir_path, glob="**/*.cs", recursive=False,show_progress=True, loader_cls=TextLoader, loader_kwargs={"autodetect_encoding":True})
    docs = loader.load()
    
    classes = []  
    
    for doc in docs:
        cleaned_content = remove_fullwidth_chars(doc.page_content)
        tree = ast.parse(cleaned_content)
        for node in ast.walk(tree):  
            if isinstance(node, ast.ClassDef):  
                class_name = node.name  
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]  
                bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
                classes.append({  
                "name": class_name,  
                "methods": methods,  
                "bases": bases  
            })  
            
    return classes  

# 示例  
dir_path = "G:\\AI\\GameFramework-master\\GameFramework\\FileSystem\\"  # 替换成你的代码文件路径  
code_structure = extract_code_structure(dir_path)  
print(code_structure) # 打印提取的类和方法信息