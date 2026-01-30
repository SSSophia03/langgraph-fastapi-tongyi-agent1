from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    LangGraph Agent 状态定义
    messages: 存储对话历史，使用 add 策略合并
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_input: str