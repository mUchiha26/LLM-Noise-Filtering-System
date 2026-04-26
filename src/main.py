"""
Entry point: CLI parsing, scan_id generation, and pipeline orchestration.
"""
import argparse
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path

from config_loader import load_config
from orchestrator import run_pipeline

# Structured logging with scan_id correlation
logger = logging.getLogger(__name__)


def generate_scan_id(input_path: str) -> str:
    """
    Deterministic scan ID: timestamp + first 1KB hash of input.
    """
    file_hash = hashlib.sha256(Path(input_path).read_bytes()[:1024]).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"scan_{timestamp}_{file_hash}"


def setup_logging(logs_dir: str, scan_id: str, level: str = "INFO") -> None:
    """Configure JSON logging with file + console output."""
    Path(logs_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(logs_dir) / f"{scan_id}.log"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="LLM Noise Filtering MVP")
    parser.add_argument("--input", required=True, help="Path to input file (.json, .csv, or .txt)")
    parser.add_argument("--config", default="config/config.yaml", help="Config path")
    parser.add_argument("--output-dir", help="Override results output directory")
    args = parser.parse_args()
    
    # Load config and generate scan_id
    config = load_config(args.config)
    scan_id = generate_scan_id(args.input)
    setup_logging(config["io"]["logs_dir"], scan_id, config["io"].get("log_level", "INFO"))
    
    logger.info(f"Starting scan {scan_id} with input: {args.input}")
    
    # Run pipeline and write outputs
    results_dir = Path(args.output_dir or config["io"]["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    
    retained, discarded = run_pipeline(args.input, config, scan_id)
    
    # Write retained records (JSON for hierarchical metadata)
    output_path = results_dir / f"{scan_id}.json"
    with open(output_path, "w") as f:
        json.dump(retained, f, indent=2)
    
    # Append discarded to noise log (JSONL for cache lookup)
    noise_log = Path(config["io"]["logs_dir"]) / config["io"]["noise_log"]
    with open(noise_log, "a") as f:
        for item in discarded:
            f.write(json.dumps(item) + "\n")
    
    logger.info(f"Complete: {len(retained)} retained, {len(discarded)} discarded → {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())