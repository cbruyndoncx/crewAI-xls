from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
#from langchain.llms import Ollama
from langchain_community.chat_models import ChatOllama

class LLMProviders:
    def __init__(self):
        self.models = {
            {{llm_list}}
        }
        provider1 = self.models["OpenAI_GPT4"]
        provider2 = self.models["Ollama_Llama31"]

        print(type(provider1))  # Output: <class '__main__.ChatOpenAI'>
        print(type(provider2))  # Output: <class '__main__.ChatOllama'>

