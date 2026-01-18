import numpy as np
from ingestion.embedder import embed_documents,embed_query

def rerank_chunks(query : str , chunks:list[dict] ,top_n:int) -> list[dict]:

    ''' rerank retrieved chunks based on similarity with query
        it is used only in DEEP strategy
    '''

    if not chunks:
        return chunks
    
    query_vec = embed_query(query)
    chunk_texts = [c["text"] for c in chunks]
    chunk_vecs = embed_documents(chunk_texts)

    # cosine similarity 

    scores = []
    for vec in chunk_vecs:

        score = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec))

        scores.append(score)

    # sort chunks by score

    ranked = sorted(
        zip(chunks , scores),
        key=lambda x:x[1],
        reverse=True
    )

    reranked_chunks = [c for c, _ in ranked[:top_n]]

    return reranked_chunks