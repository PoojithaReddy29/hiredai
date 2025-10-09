from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model


def load_llm():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable.")

    llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

    return llm

def load_llm_think():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable.")

    llm_think = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")

    return llm_think   
