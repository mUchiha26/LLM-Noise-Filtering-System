def split_into_chunks(text: str, config: dict) -> list[str]:
    sep = config["pipeline"]["chunking"]["separator"]
    min_len = config["pipeline"]["chunking"]["min_length"]
    max_len = config["pipeline"]["chunking"]["max_length"]
    
    chunks = [c.strip() for c in text.split(sep) if c.strip()]
    return [
        c if len(c) <= max_len else c[:max_len] + "...[truncated]"
        for c in chunks if len(c) >= min_len
    ]