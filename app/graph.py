from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import AgentState
from app.nodes import call_llm_node

def build_graph():
    checkpointer = MemorySaver()
    workflow = StateGraph(AgentState)

    workflow.add_node("process_input", lambda state: state)
    workflow.add_node("call_llm", call_llm_node)

    workflow.set_entry_point("process_input")
    workflow.add_edge("process_input", "call_llm")
    workflow.add_edge("call_llm", END)

    return workflow.compile(checkpointer=checkpointer)
