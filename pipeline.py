"""
🎓 pipeline.py - Connect all components
🎓 Why: Single entry point for processing; easy to test and extend
"""
import logging
from typing import List, Optional, Tuple

from utils.config_loader import load_config
from core.chunker import split_into_chunks
from core.regex_filter import regex_filter
from core.llm_classifier import LLMClassifier

logger = logging.getLogger(__name__)

def setup_logging(config: dict):
    """🎓 Configure logging based on config"""
    level = getattr(logging, config["logging"]["level"].upper())
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

def run_pipeline(raw_text: str, config: Optional[dict] = None) -> List[str]:
    """
    Main pipeline: chunk → filter → classify → collect.
    🎓 Returns list of relevant, cleaned chunks.
    """
    # 🎓 Load config if not provided
    if config is None:
        config = load_config()
    
    setup_logging(config)
    logger.info("Starting pipeline")
    
    # 🎓 Initialize components
    classifier = LLMClassifier(config)
    results = []
    
    # 🎓 Process chunks
    chunks = split_into_chunks(raw_text, config)
    logger.info(f"Split into {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks, 1):
        # Step 1: Regex pre-filter
        cleaned = regex_filter(chunk, config)
        if not cleaned:
            logger.debug(f"Chunk {i} filtered by regex")
            continue
        
        # Step 2: LLM classification
        is_relevant, confidence = classifier.classify(cleaned)
        
        if is_relevant and confidence == "high":
            results.append(cleaned)
            logger.info(f"Chunk {i} accepted (high confidence)")
        elif confidence in ["low", "unknown"]:
            logger.warning(f"Chunk {i} ambiguous: '{cleaned[:50]}...'")
            # 🎓 MVP: Skip ambiguous; later: send to review queue
        else:
            logger.debug(f"Chunk {i} rejected")
    
    logger.info(f"Pipeline complete: {len(results)}/{len(chunks)} chunks kept")
    return results

# 🎓 CLI test runner
if __name__ == "__main__":
    sample_text = """
    This is spam: Buy now!
    
    CVE-2024-1234 describes a critical SQL injection vulnerability in Apache.
    
    Random tech news: New phone released today.
    
    XSS attack vectors in React applications include...
    """
    
    results = run_pipeline(sample_text)
    print("\n=== RELEVANT CHUNKS ===")
    for r in results:
        print(f"• {r[:100]}...")