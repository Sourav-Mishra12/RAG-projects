import tiktoken
from observability.logger import logger

# performing tokenized chuning for better baseline , not doing normal chunking

tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


def chunk_text(
    pages: list[str],
    chunk_size: int = 500,
    overlap: int = 60
) -> list[dict]:

    chunks = []
    current_chunk = ""
    current_tokens = 0
    chunk_id = 0

    for page_num, page in enumerate(pages):
        paragraphs = page.split(". ")

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            para_tokens = count_tokens(para)

            if current_tokens + para_tokens > chunk_size:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": current_chunk.strip(),
                    "tokens": current_tokens,
                    "page": page_num
                })
                chunk_id += 1

                # overlap handling
                overlap_tokens = tokenizer.encode(current_chunk)[-overlap:]
                current_chunk = tokenizer.decode(overlap_tokens)
                current_tokens = len(overlap_tokens)

            current_chunk += " " + para
            current_tokens += para_tokens

    if current_chunk.strip():
        chunks.append({
            "chunk_id": f"chunk_{chunk_id}",
            "text": current_chunk.strip(),
            "tokens": current_tokens,
            "page": page_num
        })

    logger.info(
        f"Chunking complete | Total chunks: {len(chunks)} | Avg tokens/chunk: "
        f"{sum(c['tokens'] for c in chunks) // len(chunks)}"
    )

    return chunks
