import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import shutil

# 1. 配置路径
DATA_PATH = "./data"
DB_PATH = "./chroma_db"

def ingest_data():
    """
    读取 data 目录下的文件，转换为向量，并存储到 ChromaDB
    """
    print("🚀 开始数据入库流程...")
    
    documents = []
    
    # 2. 遍历目录加载文件 (支持 PDF 和 TXT)
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"⚠️ {DATA_PATH} 目录不存在，已自动创建。请放入 knowledge.pdf 或 .txt 后重试。")
        return

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        if file.endswith(".pdf"):
            print(f"📄 正在加载 PDF: {file}...")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".txt"):
            print(f"📄 正在加载 TXT: {file}...")
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())
            
    if not documents:
        print("❌ 未找到文档，请在 backend/data/ 目录下放入 .pdf 或 .txt 文件")
        return

    print(f"✅ 共加载 {len(documents)} 页文档")

    # 3. 文本切分 (Chunking)
    # 把大文档切成小块，每块 500 字，重叠 50 字（防止上下文丢失）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(documents)
    print(f"✂️ 文档已切分为 {len(splits)} 个片段")

    # 4. 初始化 Embedding 模型 (使用本地轻量级模型，免费且快速)
    print("🧠 正在初始化 Embedding 模型 (sentence-transformers)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. 创建/更新向量数据库
    # 为了演示方便，每次运行前清除旧数据库 (生产环境不要这么做!)
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
    
    print("💾 正在写入向量数据库 ChromaDB...")
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print("🎉 数据入库完成！数据库保存在 ./chroma_db")

if __name__ == "__main__":
    ingest_data()