from src.utils import GetMistralAI
from src.state import ChatState
from src.loggers import logging
from langchain_core.messages import SystemMessage

llm = GetMistralAI()

MAX_HISTORY = 10

SYSTEM_PROMPT = SystemMessage(content=(
    "You are a helpful assistant. Always give complete answers. "
    "Be concise and never cut off mid-sentence. "
    "Keep replies under 200 words."
))

def Chat_nodes(state: ChatState) -> dict:
    """ Takes messages from state, sends to LLM, returns response. """
    messages = state["messages"]

    # Only send the last MAX_HISTORY messages to the LLM
    trimmed = messages[-MAX_HISTORY:]

    # Prepend system prompt so llm knows to be concise and complete
    final_messages = [SYSTEM_PROMPT] + list(trimmed)

    # Call the LLM and get back a proper AIMessage object
    response = llm.invoke(final_messages)

    # Return the AIMessage — LangGraph's add_messages reducer stores it in state
    return {"messages": [response]}
