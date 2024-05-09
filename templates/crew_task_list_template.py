
        # Custom tasks include agent name and variables as input
        {{task_name}} = tasks.{{task_name}}(
            {{assigned_agent_name}},
            var1=self.job_to_do,
            var2=f"focus on content in {self.language}",
        )
