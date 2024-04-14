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

    def search_youtube_profile(self, agent=None, var1='', var2=''):
        """
                            Req     Supported In XLS
            Output JSON		no			Outputs a JSON object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
            Output Pydantic	no			Outputs a pydantic object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
        """
        if agent is None:     
            tempTask = Task(
                description=dedent(
                    f"""
                Search youtube for the profile of
                @carinebruyndoncx5331  
                {var1} 
                {var2}
            """
                ),
                expected_output=dedent(
                    f"""
                Only the url of the youtube profile
            """),
                tools=[],
                async_execution=False,
                context=[],
                output_file="",
                callback="",
            )
        else:
            tempTask = Task(
                description=dedent(
                    f"""
                Search youtube for the profile of
                @carinebruyndoncx5331  
                {var1} 
                {var2}
            """
                ),
                expected_output=dedent(
                    f"""
                Only the url of the youtube profile
            """),
                agent=agent,
                tools=[],
                async_execution=False,
                context=[],
                output_file="",
                callback="",
            )

        # Function to write the extracted print statements into a markdown file.
        markdown_file="./crews/groqscrape-ytp/task_search_youtube_profile.md"
        with open(markdown_file, 'w') as f:
            f.write("## search_youtube_profile"+ '\n')
            f.write(f"Description: {tempTask.description}"+ '\n')
            f.write(f"Expected output: {tempTask.expected_output}"+ '\n')
            f.write(f"Agent: {tempTask.agent}"+ '\n')
            f.write(f"Tools: {tempTask.tools}"+ '\n')
            f.write(f"Async execution: {tempTask.async_execution}"+ '\n')
            f.write(f"Context: {tempTask.context}"+ '\n')
            f.write(f"Output File: {tempTask.output_file}"+ '\n')
            f.write(f"Callback: {tempTask.callback}"+ '\n')
        
        return tempTask

    def list_subscriptions(self, agent=None, var1='', var2=''):
        """
                            Req     Supported In XLS
            Output JSON		no			Outputs a JSON object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
            Output Pydantic	no			Outputs a pydantic object based on a pydantic model; requires Agent LLM's use of an OpenAI client like Ollama with an OpenAI wrapper.
        """
        if agent is None:     
            tempTask = Task(
                description=dedent(
                    f"""
                List the subscriptions with just the author and channel name
                https://youtube.com/@carinebruyndoncx5331  
                {var1} 
                {var2}
            """
                ),
                expected_output=dedent(
                    f"""
                Users profile name: 
 * subscription 1
* subscription 2
* ...
* last subscription N
            """),
                tools=[],
                async_execution=False,
                context=[],
                output_file="",
                callback="",
            )
        else:
            tempTask = Task(
                description=dedent(
                    f"""
                List the subscriptions with just the author and channel name
                https://youtube.com/@carinebruyndoncx5331  
                {var1} 
                {var2}
            """
                ),
                expected_output=dedent(
                    f"""
                Users profile name: 
 * subscription 1
* subscription 2
* ...
* last subscription N
            """),
                agent=agent,
                tools=[],
                async_execution=False,
                context=[],
                output_file="",
                callback="",
            )

        # Function to write the extracted print statements into a markdown file.
        markdown_file="./crews/groqscrape-ytp/task_list_subscriptions.md"
        with open(markdown_file, 'w') as f:
            f.write("## list_subscriptions"+ '\n')
            f.write(f"Description: {tempTask.description}"+ '\n')
            f.write(f"Expected output: {tempTask.expected_output}"+ '\n')
            f.write(f"Agent: {tempTask.agent}"+ '\n')
            f.write(f"Tools: {tempTask.tools}"+ '\n')
            f.write(f"Async execution: {tempTask.async_execution}"+ '\n')
            f.write(f"Context: {tempTask.context}"+ '\n')
            f.write(f"Output File: {tempTask.output_file}"+ '\n')
            f.write(f"Callback: {tempTask.callback}"+ '\n')
        
        return tempTask

