from langchain_mistralai.chat_models import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
import logging
from src.loggers import loggging
from src.exceptions import CustomException

load_dotenv()

def GetMistralAI(model_name = "mistral-large-2512"):

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("API Key loaded sucessfully")

    llm = ChatMistralAI(model = model_name, api_key=api_key, max_tokens =300)
    return llm

def GetGroqAI(model_name = "llama-3.3-70b-versatile"):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq model api key not found")

    llm =  ChatGroq(model=model_name, api_key=api_key, max_tokens=300)
    return llm


def GetHuggingFaceAI():

    api_key = os.getenv("HUGGINGFACEHUB_API_KEY")

    if not api_key:
        raise ValueError("API Key not found")

    llm = HuggingFaceEndpoint(
        model = "mistralai/Mixtral-8x7B-Instruct-v0.1",
        task = "conversational",
        max_new_tokens = 300,
        huggingfacehub_api_token = api_key   
    )

    return ChatHuggingFace(llm=llm, verbose=True)