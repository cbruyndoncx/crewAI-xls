import json
import os

from langchain.tools import tool

from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun


class SearchTools():

    @tool("Search the internet")
    def search_internet(query):
        """
            Useful to search the internet about a given
            topic and return relevant results
        """
        search = DuckDuckGoSearchRun()
    
        results = search.run(query)
        return results