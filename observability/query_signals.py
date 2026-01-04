# Query length ; word count ; question type(simple heuristic) ; estimated intent

from dataclasses import dataclass
from typing import Optional

@dataclass
class QuerySignals:
    query : str

    char_length : int
    word_count : int
    is_question : bool
    intent : str

def extract_query_signals(query : str) -> QuerySignals:

    char_length = len(query)
    words = query.strip().split()
    word_count = len(words)

    is_question = query.strip().endswith("?")

    


