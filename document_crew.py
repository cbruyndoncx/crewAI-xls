import inspect

def describe_crew_instances(crew_instance):
    description = "Crew Instance Description:\n"

    # Describe Crew instance itself
    crew_attrs = inspect.getmembers(crew_instance, lambda a: not(inspect.isroutine(a)))
    for attr_name, attr_value in crew_attrs:
        if not(attr_name.startswith('__') and attr_name.endswith('__')):
            description += f"- {attr_name}: {attr_value}\n"

    # Describe Agents within the Crew
    if hasattr(crew_instance, 'agents'):
        description += "\nAgents Description:\n"
        for agent in crew_instance.agents:
            agent_attrs = inspect.getmembers(agent, lambda a: not(inspect.isroutine(a)))
            for attr_name, attr_value in agent_attrs:
                if not(attr_name.startswith('__') and attr_name.endswith('__')):
                    description += f"  - {attr_name}: {attr_value}\n"

    # Describe Tasks within the Crew
    if hasattr(crew_instance, 'tasks'):
        description += "\nTasks Description:\n"
        for task in crew_instance.tasks:
            task_attrs = inspect.getmembers(task, lambda a: not(inspect.isroutine(a)))
            for attr_name, attr_value in task_attrs:
                if not(attr_name.startswith('__') and attr_name.endswith('__')):
                    description += f"  - {attr_name}: {attr_value}\n"

    return description

def describe_crew_instances2(crew_instance):
    description = "Crew Instance Description:\n"

    # Describe Crew instance itself
    attrs = inspect.getmembers(crew_instance, lambda a: not(inspect.isroutine(a)))
    for attr_name, attr_value in attrs:
        if not(attr_name.startswith('__') and attr_name.endswith('__')):
            description += f"- {attr_name}: {attr_value}\n"



    # Describe Agents within the Crew
    if hasattr(crew_instance, 'agents'):
        description += "\nAgents Description:\n"

        # Get all functions from CustomAgents class which are assumed to return agent instances
        # agents_functions = inspect.getmembers(crew_instance.agents, inspect.ismethod)
        # for func_name, func in agents_functions:
        #     if not(func_name.startswith('_')):  # Assuming internal methods start with '_'
        #         agent = func()  # Call the function to get the agent instance
        #         description += f"  Agent - {func_name}:\n"
        #         agent_attrs = inspect.getmembers(agent, lambda a: not(inspect.isroutine(a)))
        #         for agent_attr_name, agent_attr_value in agent_attrs:
        #             if not(agent_attr_name.startswith('__') and agent_attr_name.endswith('__')):
        #                 description += f"    - {agent_attr_name}: {agent_attr_value}\n"


        #items = inspect.getmembers(crew_instance.agents, lambda a: not(inspect.isroutine(a)))
         # Get all functions from CustomAgents class which are assumed to return agent instances
        items = inspect.getmembers(crew_instance.agents, inspect.ismethod)
        for name, item in items:
            if not(name.startswith('__') and name.endswith('__')):
                description += f"  Agent - {name}:\n"
                attributes_dict = item.__dict__
                print(attributes_dict)
                attrs = inspect.getmembers(name, lambda a: (inspect.ismethod(a)))
                
                for attr_name, attr_value in attrs:
                    if not(attr_name.startswith('__') and attr_name.endswith('__')):
                        description += f"  - {attr_name}: {attr_value}\n"

    # Describe Tasks within the Crew
    if hasattr(crew_instance, 'tasks'):
        description += "\nTasks Description:\n"
        #items = inspect.getmembers(crew_instance.tasks, lambda a: not(inspect.isroutine(a)))
        items = inspect.getmembers(crew_instance.tasks, inspect.ismethod)
        for name, item in items:
            if not(name.startswith('__') and name.endswith('__')):
                description += f"  Task - {name}:\n"
                attrs = inspect.getmembers(item, lambda a: not(inspect.isroutine(a)))
                for attr_name, attr_value in attrs:
                    if not(attr_name.startswith('__') and attr_name.endswith('__')):
                        description += f"  - {attr_name}: {attr_value}\n"

    return description