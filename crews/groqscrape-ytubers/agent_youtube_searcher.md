## youtube_searcher
Role: find info in youtube
Goal: find informaation on youtube
Backstory: you understand the youtube website structure and can list all videos for  certain keywords
Tools: [SerperDevTool(name='Search the internet', description="Search the internet(search_query: 'string') - A tool that can be used to semantic search a query from a txt's content.", args_schema=<class 'crewai_tools.tools.serper_dev_tool.serper_dev_tool.SerperDevToolSchema'>, description_updated=False, search_url='https://google.serper.dev/search', n_results=None)]
Allow Delegation: True
Max Iter: 10
Max RPM: 20
LLM: callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7f733b583f10>] client=<openai.resources.chat.completions.Completions object at 0x7f733b5dc2b0> async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7f733b5dd9c0> model_name='gpt-4' temperature=0.1 openai_api_key='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' openai_proxy=''
