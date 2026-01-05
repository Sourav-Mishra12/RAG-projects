from observability.query_signals import QuerySignals

def decide_top_k(signals : QuerySignals) -> int:

    # deciding number of chunks to be retrieved based on query signals

    if signals.intent == "definition":
        return 3
    
    if signals.intent == "comparison":
        return 6
    
    if signals.word_count > 12 :
        return 6 
    
    return 5

