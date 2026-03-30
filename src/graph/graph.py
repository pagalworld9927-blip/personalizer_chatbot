from langgraph.graph import StateGraph, START, END
from src.state import ChatState
from src.nodes import Chat_nodes
from src.memory import checkpointer
import logging
from src.exceptions import CustomException
import sys

logger = logging.getLogger(__name__)

def build_graph():
    try:
        graph = StateGraph(ChatState)
        logger.info("StateGraph is defined")

        graph.add_node("Chat_nodes", Chat_nodes)
        logger.info("Node is created")

        graph.add_edge(START, "Chat_nodes")
        graph.add_edge("Chat_nodes", END)
        logger.info("Edges are added")

        return graph.compile(checkpointer=checkpointer)
    
    except Exception as e:
        raise CustomException(e, sys)


Chatbot = build_graph()