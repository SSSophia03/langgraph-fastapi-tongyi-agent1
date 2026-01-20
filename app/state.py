from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    LangGraph Agent 状态定义
    """
    messages: Annotated[Sequence[BaseMessage], "对话历史"]
    user_input: str
    final_output: str
