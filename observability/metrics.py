from dataclasses import dataclass , asdict
from typing import Optional
import time


@dataclass
class QueryMetrics:
    query: str 

    # timing metrics (ms)
    embedding_latency_ms : Optional[float] = None # how much time it took to convert the question into vector
    retrieval_latency_ms : Optional[float] = None # how muxh time it took for the VECTOR DB to retrieve those chunks
    total_latency_ms : Optional[float] = None # total requests timing

    # retrieval stats
    chunks_retrieved : Optional[int] = None # how many chunk pieces are being retrieved from the DB
    estimated_tokens : Optional[int] = None # roughly how much text is being given to LLM

    # metadata
    timestamp : float = time.time() # when did this query happen

    def to_dict(self) -> dict : # converting it to dict because it gets ease while printing the logs , making them in JSON and storing into DB 
        # this converts metrics to a dictionary 
        return asdict(self)