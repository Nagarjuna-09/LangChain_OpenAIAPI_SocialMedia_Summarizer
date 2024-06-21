from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name:str):
    """Searches for Linkedin or Twitter Profile Page."""

    # langchain_community contains third-party integrations with llms. This TavilySearchResults is inbuilt by someone in that library
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"] # Usually it returns 5 search results. This [0] returns only first search result
