from observability.query_signals import QuerySignals
from observability.metrics import QueryMetrics

def decide_retrieval_strategy(
        signal : QuerySignals
) -> str:
    
    '''
    this is the step 1 where we will make decision only.
    We will decide retrieval strategy

    '''
    # very short, definition like queries
    if signal.intent == "definition" and signal.word_count <= 5:
        return "FAST"
    
    # if the query is comparisonal or instructional
    if signal.intent in ("comaprison" , "how_to") :
        return "BALANCED"
    
    # long and complex queries
    if signal.word_count > 10:
        return "DEEP"
    
    # well , default one's
    return "BALANCED"

