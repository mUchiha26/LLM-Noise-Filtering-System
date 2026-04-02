"""
🎓 chunker.py - Split text into processable pieces
🎓 Why: LLMs have context limits; smaller chunks = better focus + cost control
"""
from typing import List

def split_into_chunks(text: str, config: dict) -> List[str]:
    """
    Split text by separator, filter by length.
    🎓 Returns only chunks worth processing.
    """
    separator = config["pipeline"]["chunking"]["separator"]
    min_len = config["pipeline"]["chunking"]["min_length"]
    max_len = config["pipeline"]["chunking"]["max_length"]
    
    # Split and clean
    chunks = [chunk.strip() for chunk in text.split(separator) if chunk.strip()]
    
    # 🎓 Filter: too short = noise, too long = truncate
    filtered = []
    for chunk in chunks:
        if len(chunk) < min_len:
            continue  # Skip noise
        if len(chunk) > max_len:
            chunk = chunk[:max_len] + "..."  # Truncate with indicator
        filtered.append(chunk)
    
    return filtered

# 🎓 Quick test when run directly
#if __name__ == "__main__":
    test_config = {
        "pipeline": {
            "chunking": {
                "separator": "\n\n",
                "min_length": 10,
                "max_length": 100
            }
        }
    }
    sample = "Short.\n\nThis is a valid chunk with security info.\n\n" + "x" * 200
    print(split_into_chunks(sample, test_config))