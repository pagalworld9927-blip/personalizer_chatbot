from langgraph.graph import StateGraph, START, END
from src.state import ChatState
from src.nodes import Chat_nodes
from src.memory import checkpointer

def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("Chat_nodes", Chat_nodes)

    graph.add_edge(START, "Chat_nodes")
    graph.add_edge("Chat_nodes", END)

    return graph.compile(checkpointer=checkpointer)

Chatbot = build_graph()