from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from app.state import AgentState
from app.config import DASHSCOPE_API_KEY, logger

def call_llm_node(state: AgentState) -> AgentState:
    llm = ChatTongyi(api_key=DASHSCOPE_API_KEY)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是世界级的技术专家"),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{user_input}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        result = chain.invoke({
            "messages": state["messages"],
            "user_input": state["user_input"]
        })

        logger.info(f"LLM 调用成功，输出预览: {result[:50]}...")

        return {
            "messages": state["messages"] + [AIMessage(content=result)],
            "user_input": state["user_input"],
            "final_output": result
        }

    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        return {
            "messages": state["messages"],
            "user_input": state["user_input"],
            "final_output": f"调用失败: {str(e)}"
        }
