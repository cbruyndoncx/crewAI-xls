## youtube_browser
Role: get video details 
Goal: get details on video content on youtube
Backstory: you are an expert in getting details on the video's published the user is interested in.
Tools: [YoutubeVideoSearchTool(name='Search a Youtube Video content', description="Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", args_schema=<class 'crewai_tools.tools.youtube_video_search_tool.youtube_video_search_tool.YoutubeVideoSearchToolSchema'>, description_updated=False, summarize=False, adapter=None, app=None, youtube_video_url=None)]
Allow Delegation: True
Max Iter: 10
Max RPM: 20
LLM: callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7f733b3c43d0>] client=<openai.resources.chat.completions.Completions object at 0x7f733b5dc2b0> async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7f733b5dd9c0> model_name='gpt-4' temperature=0.1 openai_api_key='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' openai_proxy=''
