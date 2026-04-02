import os
import logging
from utils.config_loader import load_config
from core.chunker import split_into_chunks
from core.regex_filter import apply_regex_filter
from core.llm_classifier import LLMClassifier

def setup_logging(config: dict):
    os.makedirs("logs", exist_ok=True)
    lvl = getattr(logging, config["logging"]["level"].upper(), logging.INFO)
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(level=lvl, format=fmt, handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config["logging"]["file"], mode="a")
    ])

def run_pipeline(raw_text: str, config: dict = None) -> list[str]:
    if not config: config = load_config()
    setup_logging(config)
    logger = logging.getLogger(__name__)
    logger.info("Pipeline started")
    
    classifier = LLMClassifier(config)
    results = []
    chunks = split_into_chunks(raw_text, config)
    logger.info(f"Split into {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks, 1):
        cleaned = apply_regex_filter(chunk, config)
        if not cleaned: continue
        
        is_rel, conf = classifier.classify(cleaned)
        if is_rel and conf == "high":
            results.append(cleaned)
            logger.info(f"Chunk {i} accepted")
        else:
            logger.debug(f"Chunk {i} skipped ({conf})")
            
    logger.info(f"Pipeline complete: {len(results)}/{len(chunks)} kept")
    return results