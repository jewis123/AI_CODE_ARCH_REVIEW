import os
from code_analyzer import CodeAnalyzer
from graphbuilder import GraphBuilder
from vector_store import VectorStore

from typing import List, Tuple,Annotated, TypedDict
import operator

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_text_splitters import Language as SpliterLanguage



class CodeAnalysisState(TypedDict):
    file_map : Annotated[List[Tuple], "文件路径到代码映射", operator.add]
    entities : Annotated[List[Tuple], "类实体", operator.add]
    language : str
    repo_path : str
    rst : bool=False
    ast_vector_gen:bool=False
    mermaid_gen:bool=False
    framework_anlayzed:bool=False
    security_anlayzed:bool=False
    performance_anlayzed:bool=False
    scalability_anlayzed:bool=False
    smell_anlayzed:bool=False

def globSuffix(language: str) -> str:
    return  {
        SpliterLanguage.LUA:"**/*.lua",
        SpliterLanguage.PYTHON:"**/*.py",
        SpliterLanguage.JAVA:"**/*.java",
        SpliterLanguage.CSHARP:"**/*.cs"
    }.get(language, "**/*.*")

def scan_directory(state: CodeAnalysisState) -> CodeAnalysisState:
    """扫描工程目录"""
    print("🚀 扫描工程目录...")
    
    from langchain_community.document_loaders import TextLoader,DirectoryLoader
    
    repo_path = state.get("repo_path")
    language = state.get("language")
    
    loader = DirectoryLoader(repo_path, glob=globSuffix(language), recursive=True,show_progress=True, loader_cls=TextLoader, loader_kwargs={"autodetect_encoding":True})
    docs = loader.load()
     # 过滤掉空文件
    non_empty_docs = [doc for doc in docs if doc.page_content.strip()]

    
    return {"file_map": [(doc.metadata['source'], doc.page_content) for doc in non_empty_docs]}

def parallel_parse(state: CodeAnalysisState) -> CodeAnalysisState:
    """并行解析所有文件"""
    print("👥 并行解析所有文件...")
    repo_path = state.get("repo_path", "")
    filemap  = state.get("file_map", [])
    language = state.get("language")
    analyzer = CodeAnalyzer(repo_path)
    
    results = []

    for path, content in filemap:
        result:List[Tuple] = analyzer.parse_file(path, content, language)
        if len(result[0][1]) == 0:
            continue
        results.append(result)

    return {"entities": [item for sublist in results for item in sublist]}


def build_relations(state: CodeAnalysisState) -> CodeAnalysisState:
    """构建调用关系图谱"""
    from tqdm import tqdm
    import pprint
    
    print("🔨 构建调用关系图谱...")
    gb_inherit = GraphBuilder()
    gb_call = GraphBuilder()
    gb_depend = GraphBuilder()
    
    entities = state.get("entities", [])
    for filePath, clsInfos in entities:
        for clsInfo in clsInfos:
            clsName = clsInfo['class_name']
            
            # 处理继承关系
            for parent in clsInfo['class_parent']:
                gb_inherit.add_relation(clsName, parent, 'inherit', filePath)
            
            # 处理方法调用
            for calling in clsInfo['class_method_calls']:
                gb_call.add_relation(clsName, calling[0], 'call', filePath)
                
            # 处理依赖关系
            for depend in clsInfo['class_dependencies']:
                gb_depend.add_relation(clsName, depend, 'depend', filePath)
                

    
    pretty_data = pprint.pformat(entities)
    relationFile = os.getenv("AST_RELATION_PATH")
    with open(relationFile, 'w') as f:
        f.write(pretty_data)
    
    # 生成交互式可视化
    gb_inherit.visualize_pyvis(os.getenv("INHERIT_GRAPH"))
    # 生成交互式可视化
    gb_call.visualize_pyvis(os.getenv("CALL_GRAPH"))
    # 生成交互式可视化
    gb_depend.visualize_pyvis(os.getenv("DEPEND_GRAPH"))

    print("🔨 构建代码AST向量库...")
    vector_store = VectorStore()
    vector_store.get_collection(os.getenv("AST_VECTORAB"), True)
    
    for path, class_infos in tqdm(entities, desc="记录AST关系图谱"): # 使用 tqdm 显示进度
        for class_info in class_infos:
            pretty_data = pprint.pformat(class_info)
            embedding = vector_store.model.encode(pretty_data).tolist()
            # 构建唯一的 ID，防止重复添加  
            doc_id = str(hash(path+class_info['class_name'])) 
            vector_store.add_to_chromadb(embedding, doc_id, metadata={
                "filePath" : path,
                "className" : class_info['class_name'],
                "classFields" : pprint.pformat(class_info['class_fields']) if len(class_info['class_fields']) > 0 else "None",
                "classMethods" : pprint.pformat(class_info['class_methods']) if len(class_info['class_methods']) > 0 else "None",
                "classProperties" : pprint.pformat(class_info['class_properties']) if len(class_info['class_properties']) > 0 else "None",
                "classParent" : pprint.pformat(class_info['class_parent']) if len(class_info['class_parent']) > 0 else "None",
                "classMethodCalls" : pprint.pformat(class_info['class_method_calls']) if len(class_info['class_method_calls']) > 0 else "None",
                "classDependencies" : pprint.pformat(class_info['class_dependencies']) if len(class_info['class_dependencies']) > 0 else "None"
            })
    
    return {"ast_vector_gen": True}


def generate_mermaid(state: CodeAnalysisState) -> CodeAnalysisState:
    """生成文档和可视化"""
    print("📝 生成代码架构分析文档...")
    from agents.mermaid_generator import mermaid_generator,save_mermaid_file
    
    query = "搜索所有class_parent及class_dependencies不为None的类信息"  # 查询语句  

    vector_store = VectorStore()
    vector_store.get_collection(os.getenv("AST_VECTORAB"), True)
    mermaid_code = mermaid_generator(query, vector_store.collection, vector_store.model)  # 生成 Mermaid 代码  
    save_mermaid_file(mermaid_code)  # 保存 Mermaid 代码到文件
    
    return {"mermaid_gen": True}

def analyze_framework(state: CodeAnalysisState) -> CodeAnalysisState:
    print("🔍 分析框架结构...")
    from agents.framework_analyzer import framework_analyzer
    rst = framework_analyzer()
    
    with open(os.getenv("FRAMEWORK_ANALYSIS_PATH"), "w", encoding="utf-8") as f:
        f.write(rst)
        
    return {"framework_anlayzed":True}

def analyze_security(state: CodeAnalysisState) -> CodeAnalysisState:
    print("🔍 分析代码安全漏洞...")
    return {"security_anlayzed":True}

def analyze_performance(state: CodeAnalysisState) -> CodeAnalysisState:
    print("🔍 分析代码性能...")
    return {"performance_anlayzed":True}

def analyze_scalability(state: CodeAnalysisState) -> CodeAnalysisState:
    print("🔍 分析代码可扩展性...")
    return {"scalability_anlayzed":True}

def analyze_smell(state: CodeAnalysisState) -> CodeAnalysisState:
    print("🔍 分析代码异味...")
    
    return {"smell_anlayzed":True}

def generate_report(state: CodeAnalysisState) -> CodeAnalysisState:
    print("📄 生成代码分析报告...")
    return {"rst":True}

def endScan(state: CodeAnalysisState) -> CodeAnalysisState:
    if len(state["file_map"]) == 0:
        print("❌ 构建代码映射失败！")
        return END
    return "parse"
def endParse(state: CodeAnalysisState) -> CodeAnalysisState:
    if len(state["entities"]) == 0:
        print("❌ 构建图谱实体失败！")
        return END
    return "build_graph"
def endBuildGraph(state: CodeAnalysisState) -> CodeAnalysisState:
    if state.get("ast_vector_gen", False):
        print("❌ 构建图谱关系失败！")
        return END
    return "generate_mermaid"
def endGenerateMermaid(state: CodeAnalysisState) -> CodeAnalysisState:
    if state.get("mermaid_gen", False):
        print("❌ 生成 Mermaid 文件失败！")
        return END
    return "analyze_framework"



def create_workflow() -> CompiledStateGraph:
    
    workflow = StateGraph(CodeAnalysisState)

    workflow.add_node("scan", scan_directory)
    workflow.add_node("parse", parallel_parse)
    workflow.add_node("build_graph", build_relations)
    workflow.add_node("generate_mermaid", generate_mermaid)
    workflow.add_node("analyze_framework", analyze_framework)
    workflow.add_node("analyze_security", analyze_security)
    workflow.add_node("analyze_performance", analyze_performance)
    workflow.add_node("analyze_scalability", analyze_scalability)
    workflow.add_node("analyze_smell", analyze_smell)
    workflow.add_node("generate_report", generate_report)

    workflow.set_entry_point("scan")
    workflow.add_conditional_edges("scan", endScan)
    workflow.add_conditional_edges("parse", endParse)
    workflow.add_conditional_edges("build_graph", endBuildGraph)
    workflow.add_conditional_edges("generate_mermaid", endGenerateMermaid)
    workflow.add_edge("generate_mermaid", END)

    app = workflow.compile()
    return app