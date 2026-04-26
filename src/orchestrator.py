"""
Simple synchronous pipeline router.
"""
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from core.chunker import chunk_text
from core.regex_filter import apply_rules
from core.llm_classifier import classify_with_llm
from core.scorer import apply_scoring


def run_pipeline(
    input_path: str,
    config: dict,
    scan_id: str
) -> Tuple[List[dict], List[dict]]:
    """
    Execute: Load → Chunk → Filter → Classify → Score → Output.
    Returns: (retained_records, discarded_records)
    """
    raw_data = _load_input_records(input_path)
    
    retained, discarded = [], []
    noise_cache = _load_noise_cache(config)  # O(1) lookup for reuse
    
    for idx, record in enumerate(raw_data):
        text = record.get("text") or record.get("data") or str(record)
        record_id = f"{scan_id}_{idx}"
        
        # Chunk if text exceeds max_length
        chunks = chunk_text(text, config["chunking"])
        
        for chunk in chunks:
            # Check cache first (cost reduction technique)
            cache_key = _hash_chunk(chunk)
            if cache_key in noise_cache:
                decision = noise_cache[cache_key]
                (discarded if decision["keep"] is False else retained).append(
                    _enrich_record(record, record_id, chunk, decision, "cache")
                )
                continue
            
            # Rule-based filter (fast path)
            rule_result = apply_rules(chunk, config["rules"])
            if rule_result["action"] == "discard":
                discarded.append(_enrich_record(record, record_id, chunk, rule_result, "rule"))
                continue
            
            # LLM classification (ambiguous cases only)
            llm_result = classify_with_llm(chunk, config["llm"])
            score_result = apply_scoring(llm_result, config["scoring"])
            
            # Cache only stable model decisions, not fallback/error outcomes.
            if score_result.get("decision") != "fallback":
                noise_cache[cache_key] = score_result
            
            target = retained if score_result["keep"] else discarded
            target.append(_enrich_record(record, record_id, chunk, score_result, "llm"))
    
    return retained, discarded


def _load_noise_cache(config: dict) -> dict:
    """Load existing noise_log.jsonl into dict for O(1) cache lookup."""
    cache = {}
    noise_path = Path(config["io"]["logs_dir"]) / config["io"]["noise_log"]
    if noise_path.exists():
        with open(noise_path) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    cache_key = entry.get("hash")
                    if not cache_key and entry.get("chunk"):
                        cache_key = _hash_chunk(entry["chunk"])

                    if not cache_key:
                        continue

                    # Normalize historical record formats into scoring-like decisions.
                    if "keep" in entry:
                        nested = entry.get("decision") if isinstance(entry.get("decision"), dict) else {}
                        decision = {
                            "keep": bool(entry.get("keep", nested.get("keep", False))),
                            "score": float(entry.get("score", nested.get("score", 0.0))),
                            "decision": entry.get("decision") if isinstance(entry.get("decision"), str) else nested.get("decision", "retain" if entry.get("keep") else "discard"),
                            "confidence": entry.get("confidence", nested.get("confidence", "unknown")),
                            "reason": entry.get("reason", nested.get("reason", "cache_entry"))
                        }
                    elif isinstance(entry.get("decision"), dict):
                        decision = entry["decision"]
                    elif entry.get("action") == "discard":
                        decision = {
                            "keep": False,
                            "score": 0.0,
                            "decision": "discard",
                            "confidence": "high",
                            "reason": entry.get("reason", "rule_discard")
                        }
                    else:
                        continue

                    decision = _flatten_decision(decision)

                    # Ignore uncertain/fallback cache lines to avoid persistent false discards.
                    if decision.get("decision") == "fallback":
                        continue
                    if decision.get("confidence") in {"low", "uncertain"}:
                        continue

                    cache[cache_key] = decision
                except (json.JSONDecodeError, TypeError, ValueError):
                    continue  # Skip malformed lines (robustness)
    return cache


def _hash_chunk(text: str) -> str:
    """SHA256 hash (first 12 chars) for cache key deduplication."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _enrich_record(original: dict, record_id: str, chunk: str, decision: dict, source: str) -> dict:
    """Add metadata for auditability and downstream integration."""
    keep = bool(decision.get("keep", decision.get("action") != "discard"))
    return {
        "id": record_id,
        "hash": _hash_chunk(chunk),
        "original": original,
        "chunk": chunk,
        "keep": keep,
        "decision": decision,
        "source": source,  # "cache" | "rule" | "llm"
        "timestamp": datetime.now().isoformat()
    }


def _load_input_records(input_path: str) -> List[dict]:
    """Load JSON, CSV, or line-delimited text input into standardized records."""
    if input_path.endswith(".json"):
        with open(input_path) as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]

    if input_path.endswith(".csv"):
        with open(input_path, newline="") as f:
            rows = list(csv.DictReader(f))
        records = []
        for row in rows:
            text = row.get("text") or row.get("chunk") or row.get("input") or ""
            text = text.strip()
            if not text:
                continue
            records.append({"text": text, **{k: v for k, v in row.items() if k not in {"text", "chunk", "input"}}})
        return records

    with open(input_path) as f:
        return [{"text": line.strip()} for line in f if line.strip()]


def _flatten_decision(decision: dict) -> dict:
    """Unwrap recursively nested 'decision' objects from historical log formats."""
    current = decision if isinstance(decision, dict) else {}
    safety = 0
    while isinstance(current.get("decision"), dict) and safety < 10:
        current = current["decision"]
        safety += 1
    return current