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

    if any(w in query.lower() for w in ["what" , "define" , "explain"]):
        intent = "definition"
    elif any(w in query.lower() for w in ["compare" , "difference" , "vs"]):
        intent = "comparison"
    elif any(w in query.lower() for w in ["how" , "steps" , "build"]):
        intent= "how_to"
    else:
        intent = "general"
    

    return QuerySignals(
        query=query,
        char_length=char_length,
        word_count=word_count,
        is_question=is_question,
        intent=intent
    )
