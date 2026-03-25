from flask import Flask, render_template, request, jsonify, Response
from src.graph.graph import Chatbot
from langchain_core.messages import HumanMessage
from src.memory.memory import checkpointer # Added this to read old database history

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    
    # Get the THREAD ID dynamically from javascript instead of hardcoding "user-1"!
    thread_id = data.get("thread_id", "default-thread")
    config = {"configurable": {"thread_id": thread_id}}

    def generator():
        for chunk, metadata in Chatbot.stream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
            stream_mode="messages"
        ):
            if chunk.content:
                yield chunk.content

    return Response(generator(), mimetype="text/plain")

@app.route("/history", methods=["POST"])
def get_history():
    """This route loads previously saved messages from the SQLite database."""
    data = request.get_json()
    thread_id = data.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    
    # Query LangGraph's checkpointer to get the exact state
    state = checkpointer.get(config)
    
    # If the thread is new/doesn't exist, return empty
    if not state or "channel_values" not in state or "messages" not in state["channel_values"]:
        return jsonify({"messages": []})
        
    messages = state["channel_values"]["messages"]
    history_array = []
    
    for msg in messages:
        # We don't want to print our hidden SYSTEM_PROMPT to the browser!
        if msg.type == "system":
            continue
            
        sender = "user" if msg.type == "human" else "ai"
        history_array.append({"sender": sender, "content": msg.content})
        
    return jsonify({"messages": history_array})

if __name__ == "__main__":
    app.run(debug=True)
