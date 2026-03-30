from langchain_mistralai.chat_models import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
import logging
from src.exceptions import CustomException
import sys

logger = logging.getLogger(__name__)


load_dotenv()

def GetMistralAI(model_name = "mistral-large-2512"):

    try:
        logger.info(f"GetMistralAI model is called with model name:  {model_name}")
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            logger.warning(f"API key for {model_name} is not found!")
            raise ValueError("MISTRAL_API_KEY not found in environment variables")

        llm = ChatMistralAI(model = model_name, api_key=api_key, max_tokens =500)
        logger.info("GetMistralAI sucesfully created...")
        return llm
    except Exception as e:
        raise CustomException(e, sys)

def GetGroqAI(model_name = "llama-3.3-70b-versatile"):

    try:
        logger.info(f"GetGroqAI model is called with model name:  {model_name}")
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            logger.warning(f"API key for {model_name} is not found!")
            raise ValueError("Groq model api key not found")

        llm =  ChatGroq(model=model_name, api_key=api_key, max_tokens=300)
        logger.info("GetGroqAI sucesfully created...")
        return llm
    except Exception as e:
        raise CustomException(e, sys)


def GetHuggingFaceAI():

    try:
        logger.info("GetHuggingFaceAPi is called..")
        api_key = os.getenv("HUGGINGFACEHUB_API_KEY")

        if not api_key:
            logger.warning(f"API key for HuggingFaceModel is not found!")
            raise ValueError("API Key not found")

        llm = HuggingFaceEndpoint(
            model = "mistralai/Mixtral-8x7B-Instruct-v0.1",
            task = "conversational",
            max_new_tokens = 300,
            huggingfacehub_api_token = api_key   
        )
        logger.info("GetHuggingFaceAI successfully created...")

        return ChatHuggingFace(llm=llm, verbose=True)
    except Exception as e:
        raise CustomException(e, sys)