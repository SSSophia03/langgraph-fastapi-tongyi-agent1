from app.graph import build_graph

class AIAssistant:

    def __init__(self):
        self.graph = build_graph()

    def chat(self, user_input: str, thread_id: str = "default") -> str:
        config = {"configurable": {"thread_id": thread_id}}
        initial_state = {
            "messages": [],
            "user_input": user_input,
            "final_output": ""
        }
        result = self.graph.invoke(initial_state, config=config)
        return result["final_output"]

    def get_history(self, thread_id: str = "default"):
        config = {"configurable": {"thread_id": thread_id}}
        state_tuple = self.graph.get_state(config)
        if state_tuple:
            return state_tuple[0].get("messages", [])
        return []
