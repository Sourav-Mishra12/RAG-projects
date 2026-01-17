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
from observability.decision_policy import decide_top_k
from observability.query_signals import extract_query_signals
from observability.experiments import log_experiment
from observability.retrieval_strategy import decide_retrieval_strategy



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


query = "define embeddings"

signals = extract_query_signals(query)

print("\n ----QUERY SIGNALS----")
print(signals)

metrics = QueryMetrics(query=query)
strategy = decide_retrieval_strategy(signals)
base_top_k = decide_top_k(signals)

if strategy == "FAST":
    top_k = max(3 ,base_top_k -1)

elif strategy == "BALANCED":
    top_k = base_top_k

else:
    top_k = base_top_k  



print("\n--- Decision ---")
print(f"Intent: {signals.intent}")
print(f"Word count: {signals.word_count}")
print(f"Chosen top_k: {top_k}")

start = time.time()
retrieved_chunks = retrieve(query, metrics, top_k=top_k)

if strategy == "DEEP" and metrics.chunks_retrieved < max(2 , base_top_k // 2):

    expanded_top_k = min(8,base_top_k + 2)

    print("\n ---- DEEP STRATEGY TRIGGERED ----")
    print(f"Retrying with expanded top_k={expanded_top_k}")

    more_chunks = retrieve(query,metrics,top_k=expanded_top_k)

    # simple merge by text (or id)

    seen = set()
    merged = []
    for c in retrieved_chunks + more_chunks:
        key = c["text"]
        if key not in seen:
            seen.add(key)
            merged.append(c)

    retrieved_chunks = merged



metrics.total_latency_ms = (time.time() - start) * 1000

log_experiment(
    query=query,
    intent=signals.intent,
    word_count=signals.word_count,
    top_k=top_k,
    chunks_retrieved=metrics.chunks_retrieved,
    total_latency_ms=metrics.total_latency_ms
)



print("\n---- Retrieved Context ----")
for i, chunk in enumerate(retrieved_chunks):
    print(f"[{i+1}] {chunk['text'][:200]}...\n")

print("\n--- Metrics ---")
print(metrics.to_dict())
