import os
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.nodes import call_llm_node, tool_node

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

# [核心修改] 将 checkpointer 传入函数，由 service.py 统一管理生命周期
def build_async_graph(checkpointer):
    workflow = StateGraph(AgentState)

    workflow.add_node("call_llm", call_llm_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("call_llm")

    workflow.add_conditional_edges(
        "call_llm",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )

    workflow.add_edge("tools", "call_llm")

    # 此时 checkpointer 已经是一个被 async with 激活的对象了
    return workflow.compile(checkpointer=checkpointer)