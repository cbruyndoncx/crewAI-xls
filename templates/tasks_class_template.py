from crewai import Task
from textwrap import dedent

# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class CustomTasks:
    """
                    Req     Supported In XLS
    Description				yes	A clear, concise statement of what the task entails.
    Agent		    no		yes	You can specify which agent is responsible for the task. If not, then who takes it on is determined by crew's process.
    Expected Output			yes	Clear and detailed definition of expected output for the task.
    Tools		    no			Functions or capabilities available to perform tasks ranging from simple actions like 'search' to complex interactions with APIs or other agents.
    Async Execution	no			Specifies if execution should occur asynchronously allowing other tasks to proceed without waiting.
    Context		    no			Specifies other tasks whose outputs are used as context; if those are asynchronous, their completion is awaited before context use.
    Output JSON		no			Outputs a JSON object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
    Output Pydantic	no			Outputs a pydantic object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
    Output File		no			Saves task output in specified file path location.
    Callback		no			Function executed post-completion of tasks.
    """

    def __tip_section(self):
        tip = "If you do your BEST WORK, I'll give you a $10,000 commission!"
        return tip


