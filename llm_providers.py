from langchain.chat_models import ChatOpenAI

class LLMProviders:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        self.GroqMixtral = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
        self.GroqGemma = ChatGroq(temperature=0, model_name="gemma-7b-it")
        self.OllamaLlama2 = Ollama(model="llama2")
        self.OllamaLlama31 = Ollama(model="llama3.1")
        self.OllamaGemma2 = Ollama(model="gemma2")
        self.OllamaMistralNemo = Ollama(model="mistral-nemo")
        self.OllamaPhi3 = Ollama(model="phi3")
