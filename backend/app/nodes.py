import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults # [新增] 搜索工具

from app.state import AgentState
from app.config import DEEPSEEK_API_KEY, logger 

# --- 1. 初始化资源 ---

# RAG: 向量数据库
DB_PATH = "./chroma_db"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists(DB_PATH):
    vector_store = Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embedding_model
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
else:
    logger.warning("⚠️ 未找到 chroma_db 文件夹，请先运行 ingest.py")
    retriever = None

# Search: 联网搜索工具
# max_results=3 表示每次搜索只看前3条结果，节省 Token
search_tool = TavilySearchResults(max_results=3)

# --- 2. 定义工具函数 ---

@tool
def get_current_time():
    """
    当用户询问“现在几点”、“今天几号”、“星期几”或“当前时间”时调用。
    返回精确的系统时间。
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")

@tool
def search_knowledge_base(query: str):
    """
    当用户询问关于“公司规章”、“业务文档”、“产品手册”或任何关于【内部/私有】的具体事实时调用。
    Args:
        query: 用户的搜索关键词
    """
    if not retriever:
        return "错误：知识库未初始化"
    
    try:
        logger.info(f"🔍 [RAG] 正在检索知识库: {query}")
        docs = retriever.invoke(query)
        if not docs:
            return "知识库中未找到相关信息。"
        return "\n\n".join([f"---内部文档片段 {i+1}---\n{doc.page_content}" for i, doc in enumerate(docs)])
    except Exception as e:
        return f"检索失败: {str(e)}"

@tool
def perform_internet_search(query: str):
    """
    当用户询问【实时新闻】、【天气】、【股票】、【外部世界】的通用信息，或者知识库里没有的信息时调用。
    例如：“DeepSeek 最新消息”、“今天的新闻”、“谁是现在的美国总统”。
    Args:
        query: 搜索关键词
    """
    try:
        logger.info(f"🌐 [Web] 正在联网搜索: {query}")
        # Tavily 可能会抛出异常，需要捕获
        results = search_tool.invoke({"query": query})
        
        # 格式化搜索结果
        output = ""
        for res in results:
            output += f"\n标题: {res.get('content', '')[:100]}...\n来源: {res.get('url')}\n"
        return output
    except Exception as e:
        return f"搜索失败: {str(e)}"

# --- 3. LLM 核心节点 ---

def call_llm_node(state: AgentState):
    if not DEEPSEEK_API_KEY:
        return {"messages": [AIMessage(content="错误：未配置 DeepSeek API Key")]}

    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base="https://api.deepseek.com",
        streaming=True
    )
    
    #  绑定三大工具：时间 + 知识库 + 联网搜索
    tools = [get_current_time, search_knowledge_base, perform_internet_search]
    llm_with_tools = llm.bind_tools(tools)

    #  路由提示词 (Router Prompt)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            "你是一个全能型的企业智能助手，拥有以下能力：\n"
            "1. `get_current_time`: 获取当前时间。\n"
            "2. `search_knowledge_base`: 查询【企业内部】私有文档。\n"
            "3. `perform_internet_search`: 通过搜索引擎查询【外部互联网】的实时信息。\n\n"
            "决策逻辑：\n"
            "- 问时间 -> 查时间。\n"
            "- 问公司内部事务（如上班时间、报销流程） -> 查知识库。\n"
            "- 问外部新闻、天气、股票、或通用知识 -> 联网搜索。\n"
            "- 闲聊 -> 直接回复。"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = prompt | llm_with_tools

    try:
        result = chain.invoke({"messages": state["messages"]})
        return {"messages": [result]}

    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        return {"messages": [AIMessage(content=f"系统错误: {str(e)}")]}

# --- 4. 工具执行节点 ---

def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_outputs = []
    
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            logger.info(f"⚙️ 执行工具: {tool_name}")
            
            # 工具路由分发
            if tool_name == "get_current_time":
                output = get_current_time.invoke(tool_args)
            elif tool_name == "search_knowledge_base":
                output = search_knowledge_base.invoke(tool_args)
            elif tool_name == "perform_internet_search":
                output = perform_internet_search.invoke(tool_args)
            else:
                output = "未知工具"

            tool_outputs.append(ToolMessage(
                content=str(output),
                tool_call_id=tool_call["id"],
                name=tool_name
            ))
    
    return {"messages": tool_outputs}