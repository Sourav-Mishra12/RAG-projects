from qdrant_client.models import VectorParams , Distance
from vector_store.client import client 

COLLECTION_NAME = "baseline_chunks"

def create_collection(vector_size : int):
    client.recreate_collection(
        collection_name = COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )