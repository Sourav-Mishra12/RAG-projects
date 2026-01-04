import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from ingestion.pdf_loader import load_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_documents
from vector_store.collection_setup import create_collection
from vector_store.client import client 
from qdrant_client.models import PointStruct
from retrieval.retriever import retrieve
import time 
from observability.metrics import QueryMetrics
from observability.query_signals import extract_query_signals


PDF_PATH = "data/raw/sample_rag_test_document.pdf"

# loading & chunking 
pages = load_pdf(PDF_PATH)
chunks = chunk_text(pages)

# now we are preparing the texts 
texts = [c["text"] for c in chunks ]

# now we are generating embeddings 
embeddings = embed_documents(texts)

# creating collection for the embeddings
create_collection(vector_size=len(embeddings[0]))

# upserting into Qdrant 
points = [
    PointStruct(
        id=i,
        vector=embeddings[i],
        payload=chunks[i]
    )
    for i in range (len(chunks))
]

client.upsert(
    collection_name = "baseline_chunks",
    points=points
)

print("Baseline vector store with BGE is ready !!!!")


query = "What is vector quantization?"

metrics = QueryMetrics(query=query)

start = time.time()

retrieved_chunks = retrieve(query, metrics, top_k=5)

metrics.total_latency_ms = (time.time() - start) * 1000

print("\n---- Retrieved Context ----")
for i, chunk in enumerate(retrieved_chunks):
    print(f"[{i+1}] {chunk['text'][:200]}...\n")

print("\n--- Metrics ---")
print(metrics.to_dict())

signals = extract_query_signals(query)

print("\n ----QUERY SIGNALS----")
print(signals)