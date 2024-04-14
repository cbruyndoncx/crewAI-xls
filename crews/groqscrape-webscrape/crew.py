#import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
#from decouple import config

from langchain_groq import ChatGroq
#from langchain.chains import LLMChain
#from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
#from langchain.prompts import PromptTemplate

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
            Tasks (list): A list of tasks assigned to the crew.
            Agents (list): A list of agents that are part of the crew.
            Process (str, optional): The process flow (e.g., sequential, hierarchical) 
                                    the crew follows. Default is None.
            Verbose (int, optional): The verbosity level for logging during execution.
                                    Default is 0 (no verbose output).
            Manager_LLM (LanguageModel, optional): The language model used by the manager 
                                                agent in a hierarchical process.
                                                Required when using a hierarchical process.
            Function_Calling_LLM (LanguageModel, optional): If passed, the crew will use this LLM 
                                                            to do function calling for tools for all 
                                                            agents in the crew. Each agent can have its 
                                                            own LLM, which overrides the crew's LLM for 
                                                            function calling.
            Config (dict or JSON, optional): Optional configuration settings for the crew,
                                            in `Json` or `Dict[str, Any]` format.
            Max_RPM (int, optional): Maximum requests per minute the crew adheres to during execution.
                                    Default is None.
            Language (str, optional): Language used for the crew; defaults to English if not specified.
            Full_Output (bool, optional): Whether the crew should return the full output with all tasks' 
                                        outputs or just the final output. Default is False.
            Step_Callback (callable, optional): A function that is called after each step of every agent. 
                                                This can be used to log the agent's actions or to perform 
                                                other operations; it won't override the agent-specific
                                                `step_callback`.
            Share_Crew (bool, optional): Whether you want to share the complete crew information and
                                        execution with the CrewAI team to make the library better,
                                        and allow us to train models. Default is False.
     """
    def __init__(self, additional_details, language='en'):
        self.job_to_do = additional_details
        # Got error 
        #    agent.i18n = I18N(language=self.language)
        # File "/home/cb/miniconda/envs/mypi310/lib/python3.10/site-packages/pydantic/main.py", line 171, in __init__
        # self.__pydantic_validator__.validate_python(data, self_instance=self)
        # File "/home/cb/miniconda/envs/mypi310/lib/python3.10/site-packages/crewai/utilities/i18n.py", line 27, in load_translation
        #  raise ValidationError(
        # TypeError: No constructor defined
        self.language = language
        self.agents = CustomAgents()
        self.tasks = CustomTasks()
        self.GPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.GPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        self.GroqMixtral = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
        self.GroqGemma = ChatGroq(temperature=0, groq_api_key="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", model_name="gemma-7b-it")

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        # agents = CustomAgents()
        # tasks = CustomTasks()
        agents = self.agents
        tasks = self.tasks

        
        # Define your custom agents and tasks here
        webscraper = agents.webscraper()

        
        # Custom tasks include agent name and variables as input
        scrape_webpage = tasks.scrape_webpage(
            webscraper,
            var1=self.job_to_do,
            var2=f"focus on content in {self.language}",
        )

        # Define your custom crew here
        groqscrape = Crew(
            agents=[webscraper],
            tasks=[scrape_webpage],
            language="en",
            process=Process.sequential,
            verbose=True,
            manager_llm=self.GroqGemma,
            full_output=True,
        )

        result = groqscrape.kickoff()

        metrics=groqscrape.usage_metrics

        return (result, metrics)
    
    
        