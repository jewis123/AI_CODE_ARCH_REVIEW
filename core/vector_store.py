from sentence_transformers import SentenceTransformer  
import chromadb

class VectorStore:
    def __init__(self, reset = False) -> None:
        st_model = "all-mpnet-base-v2"  # 推荐使用这个模型，效果较好且速度快  
        self.model = SentenceTransformer(st_model)
        
        self.client = chromadb.PersistentClient(settings=chromadb.Settings(allow_reset=True)) 

    def get_collection(self, collection_name:str, reset:bool=False):
        if reset:     
            try:
                self.collection = self.client.get_collection(collection_name)
                if self.collection is not None:
                    self.client.delete_collection(collection_name)  # 重置集合数据
            except:
                print(f"集合 {collection_name} 不存在")
        
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"成功连接到集合: {collection_name}")  

        

    # 定义函数，用于将代码文件向量化并添加到 ChromaDB  
    def add_to_chromadb(self, embedding, doc_id, metadata):  
        """  
        向量化后的数据添加到 ChromaDB 数据库。  
        """  
        self.collection.add(  
            embeddings=[embedding],  
            metadatas=[metadata],  
            ids=[doc_id]  
        )  
        

    #   测试搜索 (可选)  
    def search_code(self, query, collection, top_k=5):  
        """  
        根据查询语句，在 ChromaDB 数据库中搜索相关的代码片段。  
        """  
        query_embedding = self.model.encode(query).tolist()  
        results = collection.query(  
            query_embeddings=[query_embedding],  
            n_results=top_k  
        )  

        print(f"查询: {query}")  
        for i, (distance, file_path, content) in enumerate(zip(results['distances'][0], results['metadatas'][0], results['ids'])):  
            print(f"结果 {i+1}:")  
            print(f"  文件: {file_path['file_path']}")  
            print(f"  距离: {distance}")  
            #print(f"  代码片段: {content[:200]}...")  #  显示部分代码内容 (可选)  
            print("-" * 20)  


