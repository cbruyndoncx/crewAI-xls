from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.llms import Ollama

class LLMProviders:
    def __init__(self):
        self.models = {
            "OpenAI_GPT35": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
            "OpenAI_GPT4": ChatOpenAI(model_name="gpt-4", temperature=0.1),
            "Groq_Mixtral": ChatGroq(temperature=0, model_name="mixtral-8x7b-32768"),
            "Groq_Gemma": ChatGroq(temperature=0, model_name="gemma-7b-it"),
            "Ollama_Llama2": Ollama(model="llama2"),
            "Ollama_Llama31": Ollama(model="llama3.1"),
            "Ollama_Gemma2": Ollama(model="gemma2"),
            "Ollama_MistralNemo": Ollama(model="mistral-nemo"),
            "Ollama_Phi3": Ollama(model="phi3")
        }
