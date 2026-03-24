from src.graph.graph import Chatbot
from langchain_core.messages import HumanMessage
from src.state import ChatState


config = {"configurable": {"thread_id" : "user-1"}}

while True:

    messages = input("Ask Here: ").lower().strip()

    if messages in ["quit", "exit", "bye"]:
       break

    print("AI: ", end="", flush=True)
    
    for chunk, metadata in Chatbot.stream(
        {"messages" : [HumanMessage(content=messages)]},
        config=config,
        stream_mode = "messages"
    ):
       if chunk.content:
        print(chunk.content, end="", flush=True)
    
    print()
        
