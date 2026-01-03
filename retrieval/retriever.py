import time 
from ingestion.embedder import embed_query
from vector_store.client import client 
from observability.logger import logger 

COLLECTION_NAME = "baseline_chunks"

def retrieve(query : str , top_k : int = 5 ) -> list[dict]:
   ''' 
    baseline retriever :
    - embeds the query 
    - performs vectro search
    - logs retreieval latency 
   '''

   start = time.time()

   query_vector = embed_query(query)

   results = client.search(
      collection_name = COLLECTION_NAME,
      query_vector=query_vector,
      limit=top_k
   )

   retrieval_time = (time.time() - start) * 1000

   logger.info(
      f"Retrieval | query = '{query}' | top_k={top_k} | time={retrieval_time:.2f}ms"
   )

   return [hit.payload for hit in results ]