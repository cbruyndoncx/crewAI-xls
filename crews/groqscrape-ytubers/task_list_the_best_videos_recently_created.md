## list_the_best_videos_recently_created
Description: 
                List the 3 best video's recently created with the title author and channel name for each of the categories specified in the output format

                find the best webcontent about AI Agentic Frameworks
Include web articles as wel as recent videos 
                focus on content in en

Expected output: 
                Best Youtube channel for kids
 * video title 1 / url
* video title 2 / url
* video title 3 / url

Most fun Youtube channel
 * video title 1 / url
* video title 2 / url
* video title 3 / url

Most specialized Youtube channel
 * video title 1 / url
* video title 2 / url
* video title 3 / url


Agent: formatting_errors=0 id=UUID('c4628975-e8d4-463f-8aeb-150fc5cd6591') role='get video details ' goal='get details on video content on youtube' backstory="you are an expert in getting details on the video's published the user is interested in." config=None max_rpm=20 memory=False verbose=True allow_delegation=True tools=[YoutubeVideoSearchTool(name='Search a Youtube Video content', description="Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", args_schema=<class 'crewai_tools.tools.youtube_video_search_tool.youtube_video_search_tool.YoutubeVideoSearchToolSchema'>, description_updated=False, summarize=False, adapter=None, app=None, youtube_video_url=None)] max_iter=10 agent_executor=CrewAgentExecutor(verbose=True, agent=RunnableAgent(runnable={
  input: RunnableLambda(...),
  tools: RunnableLambda(...),
  tool_names: RunnableLambda(...),
  agent_scratchpad: RunnableLambda(...)
}
| PromptTemplate(input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'], partial_variables={'goal': 'get details on video content on youtube', 'role': 'get video details ', 'backstory': "you are an expert in getting details on the video's published the user is interested in."}, template='You are {role}. {backstory}\nYour personal goal is: {goal}\n\nYou ONLY have access to the following tools, and should NEVER make up tools that are not listed here:\n\n{tools}\n\nUse the following format:\n\nThought: you should always think about what to do\nAction: the action to take, only one name of [{tool_names}], just the name, exactly as it\'s written.\nAction Input: the input to the action, just a simple a python dictionary using " to wrap keys and values.\nObservation: the result of the action\n\nOnce all necessary information is gathered:\n\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\n\nCurrent Task: {input}\n\nBegin! This is VERY important to you, use the tools available and give your best Final Answer, your job depends on it!\n\nThought: \n{agent_scratchpad}')
| RunnableBinding(bound=ChatOpenAI(callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7f733b3c4d00>], client=<openai.resources.chat.completions.Completions object at 0x7f733b5dc2b0>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7f733b5dd9c0>, model_name='gpt-4', temperature=0.1, openai_api_key='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', openai_proxy=''), kwargs={'stop': ['\nObservation']})
| CrewAgentParser(agent=Agent(role=get video details , goal=get details on video content on youtube, backstory=you are an expert in getting details on the video's published the user is interested in.)), input_keys_arg=[], return_keys_arg=[]), tools=[StructuredTool(name='Search a Youtube Video content', description="Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", args_schema=<class 'crewai_tools.tools.youtube_video_search_tool.youtube_video_search_tool.YoutubeVideoSearchToolSchema'>, func=<bound method YoutubeVideoSearchTool._run of YoutubeVideoSearchTool(name='Search a Youtube Video content', description="Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", args_schema=<class 'crewai_tools.tools.youtube_video_search_tool.youtube_video_search_tool.YoutubeVideoSearchToolSchema'>, description_updated=False, summarize=False, adapter=None, app=None, youtube_video_url=None)>)], max_iterations=10, handle_parsing_errors=True, llm=ChatOpenAI(callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7f733b3c4d00>], client=<openai.resources.chat.completions.Completions object at 0x7f733b5dc2b0>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7f733b5dd9c0>, model_name='gpt-4', temperature=0.1, openai_api_key='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', openai_proxy=''), request_within_rpm_limit=<bound method RPMController.check_or_wait of RPMController(max_rpm=20, logger=<crewai.utilities.logger.Logger object at 0x7f733b3c4070>)>, tools_handler=<crewai.agents.tools_handler.ToolsHandler object at 0x7f733b583f40>, force_answer_max_iterations=8, step_callback='') tools_handler=<crewai.agents.tools_handler.ToolsHandler object at 0x7f733b583f40> cache_handler=<crewai.agents.cache.cache_handler.CacheHandler object at 0x7f735e9af3d0> step_callback='' i18n=I18N(language='en') llm=ChatOpenAI(callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7f733b3c4d00>], client=<openai.resources.chat.completions.Completions object at 0x7f733b5dc2b0>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7f733b5dd9c0>, model_name='gpt-4', temperature=0.1, openai_api_key='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', openai_proxy='') function_calling_llm=None callbacks=None
Tools: [YoutubeVideoSearchTool(name='Search a Youtube Video content', description="Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", args_schema=<class 'crewai_tools.tools.youtube_video_search_tool.youtube_video_search_tool.YoutubeVideoSearchToolSchema'>, description_updated=False, summarize=False, adapter=None, app=None, youtube_video_url=None)]
Async execution: False
Context: []
Output File: result.txt
Callback: 
