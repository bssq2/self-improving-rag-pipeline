from retrieval.pinecone_retriever import PineconeRetriever
from retrieval.weaviate_retriever import weaviate_bm25_retrieve

def hybrid_retrieve(query, top_k=5):
    pinecone_ret = PineconeRetriever()
    dense_results = pinecone_ret.retrieve(query, top_k=top_k)

    sparse_results = weaviate_bm25_retrieve(query, top_k=top_k)

    # Simple combination by just merging and truncating
    combined = dense_results + sparse_results
    # You might want to do more advanced ranking logic here
    combined = list(dict.fromkeys(combined))  # remove duplicates while preserving order

    return combined[:top_k]