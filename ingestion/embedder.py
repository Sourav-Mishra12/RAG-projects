from sentence_transformers import SentenceTransformer
from observability.logger import logger

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5",
    device = "cpu"
)


def embed_documents(text : list[str] ) -> list[list[float]]:

    logger.info(f"Generating BGE embeddings for {len(text)} document chunks")

    embeddings = model.encode(
        text,
        normalize_embeddings= True,
        show_progress_bar=True
    )

    return embeddings.tolist()


def embed_query(query : str) -> list[float]:
     # embedds a single query

     embedding = model.encode(
          query,
          normalize_embeddings=True
     )

     return embedding.tolist()

