## websearcher
Role: internet news analyst
Goal: find the latest news on specific topics
Backstory: you are aware of the latest news sites and look for interesting noteworthy content related to the provided topics.
Tools: [StructuredTool(name='Search the internet', description='Search the internet(query) - Useful to search the internet about a given\n            topic and return relevant results', args_schema=<class 'pydantic.v1.main.Search the internetSchema'>, func=<function SearchTools.search_internet at 0x7fe56db00670>)]
Allow Delegation: True
Max Iter: 15
Max RPM: 20
LLM: callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7fe5687ec340>] client=<openai.resources.chat.completions.Completions object at 0x7fe5689cfb20> async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7fe5689e5510> model_name='gpt-4' temperature=0.1 openai_api_key='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' openai_proxy=''
