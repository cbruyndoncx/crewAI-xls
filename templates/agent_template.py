
    def {{agent_name}}(self):
        """
        function_calling_llm
        """
        super().main_job(based_upon_agent="{{based_upon_agent}}")

        tempAgent = Agent(
            role=f"{self.role}{{role}}",
            backstory=dedent(f"""{self.backstory}{{backstory}}"""),
            goal=dedent(f"""{self.goal}{{goal}}"""),
            allow_delegation={{allow_delegation}},
            verbose={{verbose}},
            tools=self.tools,
            llm=self.models['{{llm}}'],
            max_iter=min(self.max_iter,{{max_iter}}),
            max_rpm=min(self.max_rpm,{{max_rpm}}),
            step_callback="{{step_callback}}",
            allow_code_execution={{allow_code_execution}},
            #system_template="{{system_template}}",
            #prompt_template="{{prompt_template}}",
    	    #response_template="{{response_template}}",

        )

        # Function to write the extracted print statements into a markdown file.
        markdown_file="{{crews_dir}}agent_{{agent_name}}.md"
        with open(markdown_file, 'w') as f:
            f.write("## {{agent_name}}"+ '\n')
            f.write(f"Role: {tempAgent.role}"+ '\n')
            f.write(f"Goal: {tempAgent.goal}"+ '\n')
            f.write(f"Backstory: {tempAgent.backstory}"+ '\n')
            f.write(f"Tools: {tempAgent.tools}"+ '\n')
            f.write(f"Allow Delegation: {tempAgent.allow_delegation}"+ '\n')
            f.write(f"Max Iter: {tempAgent.max_iter}"+ '\n')
            f.write(f"Max RPM: {tempAgent.max_rpm}"+ '\n')
            f.write(f"LLM: {tempAgent.llm}"+ '\n')        
            f.write(f"Step Callback: {tempAgent.step_callback}"+ '\n')
            f.write(f"Allow Code Execution: {tempAgent.allow_code_execution}"+ '\n')
            f.write(f"System Template: {tempAgent.system_template}"+ '\n')
            f.write(f"Prompt Template: {tempAgent.prompt_template}"+ '\n')
            f.write(f"Response Template: {tempAgent.response_template}"+ '\n')
        return tempAgent

