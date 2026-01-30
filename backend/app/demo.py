import json
import asyncio
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from app.service import AIAssistant

app = FastAPI(title="LangGraph Agent API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = AIAssistant()

@app.get("/health")
async def health():
    return {"status": "ok"}

# [新增] 获取历史会话接口 (保持不变)
@app.get("/api/history/{thread_id}")
async def get_chat_history(thread_id: str):
    try:
        history = assistant.get_history(thread_id)
        formatted_history = []
        for msg in history:
            # 只返回用户和AI的消息，过滤掉工具调用的中间消息，保持界面整洁
            if isinstance(msg, HumanMessage):
                formatted_history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage) and msg.content:
                formatted_history.append({"role": "ai", "content": msg.content})
        return {"code": 200, "data": formatted_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# [核心修改 2] 升级后的流式对话接口，支持推送工具状态
@app.post("/api/chat/stream")
async def chat_stream(
    user_input: str = Body(..., embed=True), 
    thread_id: str = Body("default", embed=True)
):
    async def event_generator():
        input_message = HumanMessage(content=user_input)
        config = {"configurable": {"thread_id": thread_id}}
        
        # 记录已处理的消息 ID，防止 LangGraph 在迭代中重复推送相同的消息
        processed_ids = set()

        # 使用 values 模式，这样可以获取每一轮的状态更新
        async for event in assistant.graph.astream(
            {"messages": [input_message]},
            config=config,
            stream_mode="values" 
        ):
            # 保护性判断，防止 event 格式不符合预期
            if "messages" not in event:
                continue
            
            messages = event["messages"]
            if not messages:
                continue
                
            # 我们只关注状态机最新产生的消息
            last_msg = messages[-1]
            
            # 如果这条消息之前已经处理并推送过了，直接跳过
            if hasattr(last_msg, "id") and last_msg.id and last_msg.id in processed_ids:
                continue
            
            # 将消息 ID 加入已处理集合
            if hasattr(last_msg, "id") and last_msg.id:
                processed_ids.add(last_msg.id)

            # --- 情况 1: AI 决定调用工具 (AIMessage 且包含 tool_calls) ---
            if isinstance(last_msg, AIMessage) and hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                for tool_call in last_msg.tool_calls:
                    # 推送“正在调用工具”的事件
                    event_data = {
                        "type": "tool_start",
                        "tool": tool_call["name"],
                        "args": tool_call["args"]
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                    # 稍微停顿一下，让前端动画有机会展示
                    await asyncio.sleep(0.1) 

            # --- 情况 2: 工具执行完毕，返回结果 (ToolMessage) ---
            elif isinstance(last_msg, ToolMessage):
                # 推送“工具结果”的事件
                event_data = {
                    "type": "tool_result",
                    "tool": last_msg.name,
                    "output": last_msg.content
                }
                yield f"data: {json.dumps(event_data)}\n\n"

            # --- 情况 3: AI 生成最终回复 (AIMessage 且有 content) ---
            elif isinstance(last_msg, AIMessage) and last_msg.content:
                # 模拟打字机流式输出
                content = last_msg.content
                chunk_size = 5 # 每次发送几个字，视觉效果更像打字
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i+chunk_size]
                    # 注意：这里 type 是 answer，前端根据这个字段拼接文本
                    yield f"data: {json.dumps({'type': 'answer', 'content': chunk})}\n\n"
                    await asyncio.sleep(0.02)

        # 结束标志
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")