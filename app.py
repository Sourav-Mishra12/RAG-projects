from ingestion.pdf_loader import load_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_documents
from vector_store.collection_setup import create_collection
from vector_store.client import client 
from qdrant_client.models import PointStruct
from retrieval.retriever import retrieve
import time 


PDF_PATH = "data/raw_pdfs/sample.pdf"

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


query = "What is vector quantization ? "

start = time.time()

retrieved_chunks = retrieve(query,top_k=5)

total_latency = (time.time() - start)* 1000

print("---- Retrieved Context ----")
for i , chunk in enumerate (retrieved_chunks):
    print(f"[{i+1}] {chunk['text'][:200]}....\n")

print(f"Total latency : {total_latency:.2f}ms")
print(f"Chunks Retrieved: {len(retrieved_chunks)}")