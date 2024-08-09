import os
import json

from crewai import Agent, Task, Crew, Process
from llm_providers import LLMProviders
#from decouple import config

from langchain_groq import ChatGroq
#from langchain.chains import LLMChain
#from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
#from langchain.prompts import PromptTemplate

from langchain.llms import Ollama

from textwrap import dedent
from .agents import CustomAgents
from .tasks import CustomTasks
from importlib import import_module

#agent_module = import_module(".agents")
# Access Class from the imported module
#CustomAgents=getattr(agent_module, 'CustomAgents')
#task_module = import_module(".tasks")
#CustomTasks=getattr(task_module, 'CustomTasks')

# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py
class CustomCrew:
    """
        Help on the Crew class attributes v0.22.5:

        Attributes:
            Tasks (list): 
                A list of tasks assigned to the crew.
            
            Agents (list): 
                A list of agents that are part of the crew.
            
            Process (str, optional): 
                The process flow (e.g., sequential, hierarchical) the crew follows. 
                Default is None.

            Verbose (int, optional): 
                The verbosity level for logging during execution.
                Default is 0 (no verbose output).
            
            Manager_LLM (LanguageModel, optional): 
                The language model used by the manager agent in a hierarchical process.
                Required when using a hierarchical process.
            
            Function_Calling_LLM (LanguageModel, optional): 
                If passed, the crew will use this LLM  to do function calling for tools for all  agents
                in the crew. 
                Each agent can have its own LLM, which overrides the crew's LLM for function calling.

            Config (dict or JSON, optional): 
                Optional configuration settings for the crew, in `Json` or `Dict[str, Any]` format.

            Max_RPM (int, optional): 
                Maximum requests per minute the crew adheres to during execution.
                Default is None.

            Language (str, optional): 
                Language used for the crew.
                Defaults to English if not specified.
            
            Full_Output (bool, optional): 
                Whether the crew should return the full output with all tasks' outputs or just the final output. 
                Default is False.
            
            Step_Callback (callable, optional): 
                A function that is called after each step of every agent. 
                This can be used to log the agent's actions or to perform  other operations; 
                it won't override the agent-specific `step_callback`.

            Share_Crew (bool, optional): 
                Whether you want to share the complete crew information and execution with the CrewAI team 
                to make the library better, and allow us to train models. 
                Default is False.
     """
    from llm_providers import LLMProviders

    def __init__(self, additional_details, language='en'):
        self.llm_providers = LLMProviders()
        self.job_to_do = additional_details
        self.language = language
        self.agents = CustomAgents()
        self.tasks = CustomTasks()
        self.GPT35 = self.llm_providers.models["OpenAIGPT35"]
        self.GPT4 = self.llm_providers.models["OpenAIGPT4"]
        self.GroqMixtral = self.llm_providers.models["GroqMixtral"]
        self.GroqGemma = self.llm_providers.models["GroqGemma"]
        self.OllamaLlama2 = self.llm_providers.models["OllamaLlama2"]
        self.OllamaLlama31 = self.llm_providers.models["OllamaLlama31"]
        self.OllamaGemma2 = self.llm_providers.models["OllamaGemma2"]
        self.OllamaMistralNemo = self.llm_providers.models["OllamaMistralNemo"]
        self.OllamaPhi3 = self.llm_providers.models["OllamaPhi3"]
        
    
    def run(self):
        agents = self.agents
        tasks = self.tasks

        {{crew_agent_list_template}}

        {{crew_task_list_template}}

        # Define your custom crew here
        {{crew_name}} = Crew(
            agents=[{{crew_agent_list}}],
            tasks=[{{crew_task_list}}],
            language="{{language}}",
            process=Process.{{process}},
            verbose={{crew_verbose}},
            manager_llm=self.{{manager_llm}},
            full_output={{full_output}},
        )

        #result = {{crew_name}}.kickoff()
        crew_output = {{crew_name}}.kickoff()
        
        # Accessing the crew output
        print(f"Raw Output: {crew_output.raw}")
        if crew_output.json_dict:
            print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
        if crew_output.pydantic:
            print(f"Pydantic Output: {crew_output.pydantic}")
        print(f"Tasks Output: {crew_output.tasks_output}")
        metrics = f"Token Usage: {crew_output.token_usage}"

        #metrics={{crew_name}}.usage_metrics

        return (crew_output, metrics)
    
    
        
