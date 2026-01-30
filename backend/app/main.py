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

# [关键新增] 异步初始化生命周期钩子
@app.on_event("startup")
async def startup_event():
    await assistant.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await assistant.close()
    
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/history/{thread_id}")
async def get_chat_history(thread_id: str):
    try:
        # 这里的 get_history 逻辑可以根据需要后续完善
        return {"code": 200, "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(
    user_input: str = Body(..., embed=True), 
    thread_id: str = Body("default", embed=True)
):
    async def event_generator():
        input_message = HumanMessage(content=user_input)
        config = {"configurable": {"thread_id": thread_id}}
        
        processed_ids = set()

        # astream 现在会自动调用异步持久化层
        async for event in assistant.graph.astream(
            {"messages": [input_message]},
            config=config,
            stream_mode="values" 
        ):
            if "messages" not in event:
                continue
            
            messages = event["messages"]
            if not messages:
                continue
                
            last_msg = messages[-1]
            
            if hasattr(last_msg, "id") and last_msg.id and last_msg.id in processed_ids:
                continue
            
            if hasattr(last_msg, "id") and last_msg.id:
                processed_ids.add(last_msg.id)

            if isinstance(last_msg, AIMessage) and hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                for tool_call in last_msg.tool_calls:
                    event_data = {
                        "type": "tool_start",
                        "tool": tool_call["name"],
                        "args": tool_call["args"]
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                    await asyncio.sleep(0.1) 

            elif isinstance(last_msg, ToolMessage):
                event_data = {
                    "type": "tool_result",
                    "tool": last_msg.name,
                    "output": last_msg.content
                }
                yield f"data: {json.dumps(event_data)}\n\n"

            elif isinstance(last_msg, AIMessage) and last_msg.content:
                content = last_msg.content
                chunk_size = 5 
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i+chunk_size]
                    yield f"data: {json.dumps({'type': 'answer', 'content': chunk})}\n\n"
                    await asyncio.sleep(0.02)

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")