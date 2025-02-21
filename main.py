from dotenv import load_dotenv
from langchain_text_splitters import Language as SpliterLanguage
from vector_store import VectorStore
from workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    # 初始化并运行工作流    
    vector_store = VectorStore(reset=True)
    app = create_workflow()
    state = app.invoke({
        "repo_path":"G:\\AI\\GameFramework-master",
        "language":SpliterLanguage.CSHARP}
    )
    
    # 打印统计信息
    print(f"分析文件数: {len(state.get('file_map', {}))}")
    print(f"发现实体数: {len(state.get('entities', []))}")
    print(f"建立关系数: {len(state.get('relations', []))}")
    
    if state.get("rst", False):
        print("输出文件已生成：")
        print("- call_graph.md      : Mermaid格式调用图")
        print("- graph.html       : 交互式可视化图表")
        print("- analysis_report.md : AI生成的架构分析报告")
