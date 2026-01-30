import asyncio
import aiosqlite 
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.graph import build_async_graph

class AIAssistant:
    def __init__(self):
        self._graph = None
        self.conn = None 

    async def initialize(self):
        """显式创建连接并初始化数据库"""
        if self._graph is None:
            print("🔄 正在初始化数据库连接...")
            
            # 1. 手动建立连接
            # check_same_thread=False 在异步模式下通常不需要，但为了兼容性加上无妨
            self.conn = await aiosqlite.connect("checkpoints.sqlite")
            
            # 2. 实例化 Saver (把连接传进去)
            checkpointer = AsyncSqliteSaver(self.conn)
            
            # 3. [关键步骤] 显式创建表结构
            # 之前的 from_conn_string 会自动做这个，手动模式下必须自己调 setup
            await checkpointer.setup()
            
            # 4. 编译 Graph
            self._graph = build_async_graph(checkpointer)
            
            print("✅ 数据库连接成功，Graph 初始化完成！")
        return self._graph

    async def close(self):
        """优雅关闭连接"""
        if self.conn:
            print("🛑 正在关闭数据库连接...")
            await self.conn.close()
            print("✅ 数据库连接已关闭")

    @property
    def graph(self):
        if self._graph is None:
            raise RuntimeError("Assistant graph has not been initialized.")
        return self._graph

    def get_history(self, thread_id: str):
        return []