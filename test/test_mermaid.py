



from agents.mermaid_generator import mermaid_generator, save_mermaid_file
from vector_store import VectorStore


vector_store = VectorStore(reset=False)  # 初始化代码向量库
query = "搜索所有class_parent及class_dependencies不为None的类信息"  # 查询语句  
mermaid_code = mermaid_generator(query, vector_store.collection, vector_store.model)  # 生成 Mermaid 代码  

save_mermaid_file(mermaid_code)  # 保存 Mermaid 代码到文件