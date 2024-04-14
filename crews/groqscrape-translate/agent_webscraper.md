## webscraper
Role: get website content from url
Goal: get current up to date information published on a website
Backstory: you are able to get content from a website url and extract the main body of the page
Tools: [ScrapeWebsiteTool(name='Read website content', description="Read website content(website_url: 'string') - A tool that can be used to read a website content.", args_schema=<class 'crewai_tools.tools.scrape_website_tool.scrape_website_tool.ScrapeWebsiteToolSchema'>, description_updated=False, website_url=None, cookies=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Referer': 'https://www.google.com/', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Accept-Encoding': 'gzip, deflate, br'})]
Allow Delegation: True
Max Iter: 15
Max RPM: 20
LLM: callbacks=[<crewai.utilities.token_counter_callback.TokenCalcHandler object at 0x7fa1744f1bd0>] client=<openai.resources.chat.completions.Completions object at 0x7fa1744e8250> async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7fa1744e9c30> model_name='gpt-4' temperature=0.1 openai_api_key='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' openai_proxy=''
