# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import fastapi_cdn_host
from langchain_core.messages import HumanMessage

from app.service import AIAssistant

app = FastAPI(
    title="AI Agent API",
    version="1.0",
    description="基于 LangGraph 的 AI Agent 对话服务"
)

fastapi_cdn_host.patch_docs(app)

assistant = AIAssistant()

class ChatRequest(BaseModel):
    user_input: str
    thread_id: Optional[str] = "default"

class HistoryRequest(BaseModel):
    thread_id: Optional[str] = "default"

@app.post("/agent/chat")
async def agent_chat(request: ChatRequest):
    try:
        response = assistant.chat(request.user_input, request.thread_id)
        return {"code": 200, "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/get_history")
async def get_history(request: HistoryRequest):
    history = assistant.get_history(request.thread_id)
    return {
        "code": 200,
        "data": [
            {
                "role": "user" if isinstance(m, HumanMessage) else "ai",
                "content": m.content
            }
            for m in history
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
