from crewai import Agent
from textwrap import dedent
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

### Install duckduckgo-search for this example:
### !pip install -U duckduckgo-search

from crewai_tools import FileReadTool, ScrapeWebsiteTool, SerperDevTool, WebsiteSearchTool, YoutubeChannelSearchTool, YoutubeVideoSearchTool
    
web_search_tool = WebsiteSearchTool()
serper_dev_tool = SerperDevTool()
# file_read_tool = FileReadTool(
#         file_path='job_description_example.md',
#         description='A tool to read the job description example file.'
# )

youtube_channel_rag_tool = YoutubeChannelSearchTool()
youtube_video_rag_tool = YoutubeVideoSearchTool()
web_scrape_tool = ScrapeWebsiteTool()


class BaseAgents():

    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        #self.Ollama = Ollama(model="openhermes")
        self.tools = []
        self.max_iter=15
        self.max_rpm=20
        self.llm=self.OpenAIGPT4
        self.allow_delegation=True

        self.searchtools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ]
        self.calculatortools=[
                CalculatorTools.calculate
            ]

    
    def main_job(self, based_upon_agent):
        def handle_websearch():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                     SearchTools.search_internet
                ]
            
        def handle_webscrape():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                     web_scrape_tool
                ]
            
        def handle_webRAG():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                    web_search_tool
                ]
        
        def handle_ytchannelRAG():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                    youtube_channel_rag_tool
                ]
            
        def handle_ytvideoRAG():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                    youtube_video_rag_tool
                ]
            
        def handle_browse():
            serper_dev_tool = SerperDevTool()
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[
                     serper_dev_tool,
                ]

        def handle_summarize():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[]
            #self.llm=self.OpenAIGPT35

        def handle_translate():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[]
    
        def handle_default():
            self.role=""
            self.backstory=""
            self.goal=""
            self.tools=[]

        case_functions = {
            'webscrape': handle_webscrape,
            'websearch': handle_websearch,
            'webRAG': handle_webRAG,
            'ytchannel': handle_ytchannelRAG,
            'ytvideo': handle_ytvideoRAG,
            'browse': handle_browse,
            'summarize': handle_summarize,
            'translate': handle_translate
        }
        # The get method of dictionaries accepts a default value if key doesn't exist.
        return case_functions.get(based_upon_agent, handle_default)()

    # def research_agent(self, role, goal,backstory,allow_delegation,verbose,llm,max_iter,max_rpm,step_callback, memory):
    #     """
    #     function_calling_llm
    #     """
    #     return Agent(
    #         role=role,
    #         backstory=backstory,
    #         goal=goal,
    #         allow_delegation=allow_delegation,
    #         verbose=verbose,
    #         llm=llm,
    #         max_iter=max_iter,
    #         max_rpm=max_rpm,
    #         step_callback=step_callback,
    #         memory=memory,
    #     )
    

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents(BaseAgents):

    """
    Available CrewAI Tool as part of BaseAgents
    -------------------------------------------
    1. CodeDocsSearchTool: For developers and technical writers to search through extensive code documentation.
    2. CSVSearchTool: Allows efficient searching of structured data in CSV format for data analysts.
    3. DirectorySearchTool: Simplifies searching within directories, ideal for system administrators.
    4. DOCXSearchTool: Enables quick searching within Microsoft Word DOCX files.
    5. DirectoryReadTool: Assists in reading and processing directory structures and contents.
    6. FileReadTool: Supports reading from various file formats for data extraction.
    7. GithubSearchTool: Makes it easy to search through codebases on GitHub.
    8. SeperDevTool (In Progress): A specialized development tool with unique functionalities for niche needs.
    9. TXTSearchTool: Text files are ubiquitous and often contain unstructured data; this tool is tailored for searching within such .txt files efficiently.
    10. JSONSearchTool: As JSON becomes increasingly popular for storing structured data, this tool meets the need for a dedicated search utility that can handle JSON file formats effectively.
    11. MDXSearchTool: Markdown (MDX) files are commonly used in documentation; this utility ensures that users can easily search through such content without hassle.
    12. PDFSearchTool: Scanned documents and reports are often saved as PDFs; this tool is designed to make searching within PDFs feasible—an essential feature for many professionals including researchers and legal experts.
    13. PGSearchTool: Database administrators will find this PostgreSQL database search tool highly beneficial as it streamlines the process of executing database queries.
    14. agTool: A jack-of-all-trades in the toolkit; it's capable of handling multiple data sources and types—a versatile solution when you're unsure about the nature of your data source.
    15. ScrapeElementFromWebsiteTool: When you need targeted extraction from websites—like specific tags or classes—this scraping utility comes into play offering precision in web data collection tasks.
    16. ScrapeWebsiteTool: For broader web scraping needs where entire websites need to be crawled and analyzed, this comprehensive scraping solution does the job effectively.
    17. WebsiteSearchTool: Optimized specifically for web content extraction; if you need to search through website text or metadata quickly, look no further than this handy utility.
    18. XMLSearchTool: XML files hold structured information used across various industries; with this tool at hand, navigating through XML-based datasets becomes a breeze.
    19. YoutubeChannelSearchTool:
    20. YoutubeVideoSearchTool: These two tools cater specifically to YouTube content analysis—whether you're researching channels or needing detailed insights from video content itself—they provide tailored solutions for video-related searches.
    
    
                       Required Default Supported
    Role		            yes		    yes	Defines the agent's function within the crew. It determines the kind of tasks the agent is best suited for.
    Goal	         	    yes		    yes	The individual objective that the agent aims to achieve. It guides the agent's decision-making process.
    Backstory	        	yes		    yes	Provides context to the agent's role and goal, enriching the interaction and collaboration dynamics.
    LLM		                no		    	The language model used by the agent to process and generate text. It dynamically fetches the model name from the OPENAI_MODEL_NAME environment variable, defaulting to "gpt-4" if not specified.
    Tools	    	        no		    	Set of capabilities or functions that the agent can use to perform tasks. Tools can be shared or exclusive to specific agents. It's an attribute that can be set during the initialization of an agent, with a default value of an empty list.
    Function Calling LLM	no		    	If passed, this agent will use this LLM to execute function calling for tools instead of relying on the main LLM output.
    Max Iter	            no	15		    The maximum number of iterations the agent can perform before being forced to give its best answer.
    Max RPM		            no	None	    The maximum number of requests per minute the agent can perform to avoid rate limits.
    Verbose		            no	False	    Enables detailed logging of the agent's execution for debugging or monitoring purposes.
    Allow Delegation	    no	True	    Agents can delegate tasks or questions to one another, ensuring that each task is handled by the most suitable agent.
    Step Callback		    no			    A function that is called after each step of the agent. This can be used to log the agent's actions or to perform other operations. It will overwrite the crew step_callback.
    Memory		            no	False	    Indicates whether the agent should have memory or not. This impacts the agent's ability to remember past interactions.
    """
    def __init__(self):
        super().__init__()  # Call initializer of the ParentClass

