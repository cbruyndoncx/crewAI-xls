import json
import os

from langchain.tools import tool
from langchain.agents import Tool

from langchain_community.tools import DuckDuckGoSearchRun

from langchain_community.tools.tavily_search import TavilySearchResults


class SearchTools():

    @tool("Search the internet")
    def search_internet_using_ddgs(query):
        """
            Useful to search the internet about a given
            topic and return relevant results
        """
        search = DuckDuckGoSearchRun()
    
        results = search.run(query)
        return results
    

    @tool("Factual efficient internet search optimized for LLMs")
    def search_internet(query):
        """
            Factual and efficient to search the internet about a given
            topic and return relevant results to LLMs for further processing.
        """
        search = TavilySearchAPIWrapper()
        results = TavilySearchResults(api_wrapper=search)    
        return results

