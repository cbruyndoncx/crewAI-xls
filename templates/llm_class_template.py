from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
#from langchain.llms import Ollama
#from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama

class LLMProviders:
    def __init__(self):
        self.models = {
            {{llm_list}}
        }