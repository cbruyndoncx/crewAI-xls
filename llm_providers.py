from langchain.chat_models import ChatOpenAI

class LLMProviders:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        self.llm = self.OpenAIGPT4
