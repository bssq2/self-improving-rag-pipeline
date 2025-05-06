import weaviate
from config import Config

def weaviate_bm25_retrieve(query, top_k=5, metadata_filters=None):
    """
    Retrieve documents via BM25 in Weaviate.
    Optional metadata_filters can be used to narrow results.
    """
    client = weaviate.Client(
        url=Config.WEAVIATE_URL,
        additional_headers={"X-OpenAI-Api-Key": Config.WEAVIATE_API_KEY}
    )

    filter_string = ''
    if metadata_filters:
        # Build a Weaviate-style filter expression
        # Example: filter_string = 'content ~ "' + ' AND '.join(metadata_filters) + '"'
        # (adapt as needed for actual filters)
        pass

    # BM25 query: 'bm25("query")'
    query_str = f'{{Get {{ Document (bm25: {{query: "{query}", properties: ["content"]}}) {{ content _additional{{ distance }} }} }} }}'
    results = client.query.raw(query_str)

    documents = []
    data = results.get("data", {})
    get_data = data.get("Get", {})
    docs = get_data.get("Document", [])
    for doc in docs:
        documents.append(doc.get("content"))

    return documents[:top_k]