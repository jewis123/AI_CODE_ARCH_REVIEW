from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from vector_store import VectorStore


vector_store = VectorStore(reset=False)
print("🔨 构建代码AST向量库...")
vector_store.get_collection("rawcode_vector_db", True)

def add_code_to_vector_db(code_dir, language):
    loader = DirectoryLoader(code_dir, loader_cls=TextLoader, loader_kwargs={"autodetect_encoding": True}, use_multithreading=True, show_progress=True)
    docs = loader.load()
    for doc in docs:
        splitter = RecursiveCharacterTextSplitter.from_language(language=Language.CSHARP, chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)
        embedding = vector_store.model.encode(splits).tolist()
        code_file = doc.metadata['source']
        metadata = [{"text": split.page_content} for split in splits]
        doc_id = [hash(code_file)]
        vector_store.add_to_chromadb(embedding, doc_id, metadata)
        
    print(f"成功添加代码文件: {code_file} 到向量库")