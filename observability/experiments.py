'''

we will keep record of these following things for every run :

- query
- intent
- word_count
- chosen top_k
- chunks_retrieved
- total_latency_ms
- timestamp

'''

from dataclasses import dataclass , asdict 
from typing import Dict
import json 
import os 
import time 

EXPERIMENT_LOG_PATH = "observability/experiment_log.jsonl"

@dataclass
class ExperimentRecord:
    query : str
    intent : str
    word_count : int
    top_k : int
    chunks_retrieved : int
    total_latency_ms : float
    timestamp : float 


def log_experiment (
        *,
        query:str,
        intent:str,
        word_count:int,
        top_k:int,
        chunks_retrieved:int,
        total_latency_ms:float
):
    
    # append one experiment record to a JSONL file , each line = one query run 

    record = ExperimentRecord(
        query=query,
        intent=intent,
        word_count=word_count,
        top_k=top_k,
        chunks_retrieved=chunks_retrieved,
        total_latency_ms=total_latency_ms,
        timestamp=time.time()
    )

    os.makedirs(os.path.dirname(EXPERIMENT_LOG_PATH) , exist_ok=True)

    with open(EXPERIMENT_LOG_PATH, "a" , encoding="utf-8")as f:
        f.write(json.dumps(asdict(record)) + "\n")