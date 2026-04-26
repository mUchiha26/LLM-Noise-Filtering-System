"""
Basic text chunker with overlap support.
"""
from typing import List, Dict


def chunk_text(text: str, config: Dict) -> List[str]:
    """
    Split text by separator, respecting max_length and overlap.
    MVP: Simple newline/fixed-size; semantic chunking added later.
    """
    max_len = config.get("max_length", 512)
    separator = config.get("separator", "\n")
    overlap = config.get("overlap", 0)
    
    # If text fits, return as-is (common for SpiderFoot records)
    if len(text) <= max_len:
        return [text]
    
    # Split by separator first (preserves logical units)
    parts = text.split(separator)
    chunks, current = [], []
    current_len = 0
    
    for part in parts:
        part_len = len(part) + len(separator)
        if current_len + part_len > max_len and current:
            chunks.append(separator.join(current))
            # Overlap: keep last N chars for context continuity
            if overlap > 0:
                last_chunk = chunks[-1]
                current = [last_chunk[-overlap:]] if len(last_chunk) > overlap else []
                current_len = len(current[0])
            else:
                current, current_len = [], 0
        current.append(part)
        current_len += part_len
    
    if current:
        chunks.append(separator.join(current))
    
    return chunks or [text]  # Fallback