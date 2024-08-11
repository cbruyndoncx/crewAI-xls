from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.llms import Ollama

class CustomOllama(Ollama):
    def __init__(self, model, url=None):
        super().__init__(model=model)
        self.url = url

    def _call(self, prompt, stop=None):
        if self.url:
            self.client.base_url = self.url
        return super()._call(prompt, stop)

class LLMProviders:
    def __init__(self):
        self.models = {
            "OpenAI_GPT35": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
            "OpenAI_GPT4": ChatOpenAI(model_name="gpt-4", temperature=0.1),
            "Groq_Mixtral": ChatGroq(temperature=0, model_name="mixtral-8x7b-32768"),
            "Groq_Gemma": ChatGroq(temperature=0, model_name="gemma-7b-it"),
            "Ollama_Llama2": CustomOllama(model="llama2", url="http://specific-ip-address:port"),
            "Ollama_Llama31": CustomOllama(model="llama3.1", url="http://specific-ip-address:port"),
            "Ollama_Gemma2": CustomOllama(model="gemma2", url="http://specific-ip-address:port"),
            "Ollama_MistralNemo": CustomOllama(model="mistral-nemo", url="http://specific-ip-address:port"),
            "Ollama_Phi3": CustomOllama(model="phi3", url="http://specific-ip-address:port")
        }
