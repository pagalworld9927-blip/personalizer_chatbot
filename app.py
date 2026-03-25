from flask import Flask, render_template, request, jsonify, Response
from src.graph.graph import Chatbot
from langchain_core.messages import HumanMessage

app = Flask(__name__)

config = {"configurable" : {"thread_id" : "user-1"}}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message")

    def generator():
        for chunk, metadata in Chatbot.stream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
            stream_mode="messages"
        ):
            if chunk.content:
                yield chunk.content

    return Response(generator(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
