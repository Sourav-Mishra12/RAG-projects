import time 
from ingestion.embedder import embed_query
from vector_store.client import client 
from observability.logger import logger
from observability.metrics import QueryMetrics 

COLLECTION_NAME = "baseline_chunks"

def retrieve(query: str, metrics: QueryMetrics, top_k: int = 5) -> list[dict]:
    """
    Baseline retriever:
    - embeds the query
    - performs vector search
    - fills retrieval-related metrics
    """

    # Embedding timing 
    embed_start = time.time()
    query_vector = embed_query(query)
    metrics.embedding_latency_ms = (time.time() - embed_start) * 1000

    #  Retrieval timing 
    retrieval_start = time.time()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    metrics.retrieval_latency_ms = (time.time() - retrieval_start) * 1000

    #  Retrieval stats 
    metrics.chunks_retrieved = len(results)

    logger.info(
        f"Retrieval | query='{query}' | top_k={top_k} | "
        f"embed={metrics.embedding_latency_ms:.2f}ms | "
        f"retrieval={metrics.retrieval_latency_ms:.2f}ms"
    )

    return [hit.payload for hit in results]
