from config import Config
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

def azure_query_disambiguation(user_query):
    """
    Use Azure Cognitive Search to glean possible query expansions/corrections.
    Return a refined or disambiguated query if possible.
    """
    endpoint = Config.AZURE_SEARCH_ENDPOINT
    key = Config.AZURE_SEARCH_KEY
    index = Config.AZURE_SEARCH_INDEX

    # This is a minimalistic approach. For advanced scenarios, you might use
    # semantic ranking or suggestions from Azure.
    search_client = SearchClient(endpoint=endpoint, index_name=index, credential=AzureKeyCredential(key))

    # Example: try a simple 'suggest'
    suggestions = search_client.suggest(search_text=user_query, suggester_name="sg")
    # If suggestions exist, pick one
    for s in suggestions:
        if s.text.lower() != user_query.lower():
            return s.text
    return user_query