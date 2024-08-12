    def {{task_name}}(self, agent=None, var1='', var2=''):
        """
            Tasks defined for every or specific agent
            Outputs markdown description of task input details for logging
        """
        tempTask = Task(
            description=dedent(
                f"""
            {{description}}
            {{extra1}} {{extra2}} {{extra3}}
            {var1} 
            {var2}
        """
            ),
            expected_output=dedent(
                f"""
            {{expected_output}}
        """),
            agent=agent,
            tools=[{{task_tools}}],
            async_execution={{async_execution}},
            context=[{{context}}],
            output_file="{{output_file}}",
            callback="{{callback}}",
            human_input={{human_input}},
        )

        # Function to write the extracted print statements into a markdown file.
        markdown_file="{{crews_dir}}task_{{task_name}}.md"
        with open(markdown_file, 'w') as f:
            f.write("## {{task_name}}"+ '\n')
            f.write(f"Description: {tempTask.description}"+ '\n')
            f.write(f"Expected output: {tempTask.expected_output}"+ '\n')
            f.write(f"Agent: {tempTask.agent}"+ '\n')
            f.write(f"Tools: {tempTask.tools}"+ '\n')
            f.write(f"Async execution: {tempTask.async_execution}"+ '\n')
            f.write(f"Context: {tempTask.context}"+ '\n')
            f.write(f"Output File: {tempTask.output_file}"+ '\n')
            f.write(f"Callback: {tempTask.callback}"+ '\n')
            f.write(f"Human input: {tempTask.human_input}"+ '\n')
        
        return tempTask


