from langchain.chat_models import ChatOpenAI

class LLMProviders:
    def __init__(self):
        self.models = {
            "OpenAIGPT35": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
            "OpenAIGPT4": ChatOpenAI(model_name="gpt-4", temperature=0.1),
            "GroqMixtral": ChatGroq(temperature=0, model_name="mixtral-8x7b-32768"),
            "GroqGemma": ChatGroq(temperature=0, model_name="gemma-7b-it"),
            "OllamaLlama2": Ollama(model="llama2"),
            "OllamaLlama31": Ollama(model="llama3.1"),
            "OllamaGemma2": Ollama(model="gemma2"),
            "OllamaMistralNemo": Ollama(model="mistral-nemo"),
            "OllamaPhi3": Ollama(model="phi3")
        }
