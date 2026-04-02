"""
🎓 evaluate.py - Real-world pipeline test with cost/latency tracking
🎓 Purpose: Observe behavior on noisy data, measure performance, guide prompt tuning
"""
import time
import json
import logging
from pathlib import Path
from utils.config_loader import load_config
from pipeline import run_pipeline

def evaluate_pipeline(input_file: str = "data/sample_input.txt", 
                      output_file: str = "evaluation_report.json"):
    config = load_config()
    path = Path(input_file)
    if not path.exists():
        raise FileNotFoundError(f"Test data not found: {path}")
    
    raw_text = path.read_text(encoding="utf-8")
    print(f"📊 Input: {len(raw_text)} chars | {raw_text.count(chr(10))} lines")
    
    # Setup logging to capture rejection reasons
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("🔍 Starting real-world evaluation...")
    
    start = time.time()
    results = run_pipeline(raw_text, config)
    elapsed = time.time() - start
    
    # Rough cost estimate (OpenRouter varies by model; this is conservative)
    input_tokens = len(raw_text) / 4.0
    output_tokens = len(results) * 8.0  # ~2 words per chunk
    cost_estimate = (input_tokens / 1_000_000 * 0.15) + (output_tokens / 1_000_000 * 0.60)
    
    report = {
        "metadata": {
            "input_file": str(path),
            "input_chars": len(raw_text),
            "processing_time_sec": round(elapsed, 2),
            "estimated_cost_usd": round(max(cost_estimate, 0.005), 4),
            "model": config["llm"]["model"],
            "mode": config["llm"]["mode"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "results": {
            "chunks_kept": len(results),
            "kept_content": results
        },
        "analysis_guide": {
            "check_false_positives": "Review kept_content for non-security text",
            "check_false_negatives": "See logs/pipeline.log for rejected chunks",
            "prompt_tuning": "Adjust criteria in config.yaml prompt_template if needed",
            "cost_optimization": "Increase chunk_length or enable regex pre-filter to reduce LLM calls"
        }
    }
    
    Path(output_file).write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    print(f"\n✅ Evaluation complete!")
    print(f"⏱️  Time: {elapsed:.2f}s | 💰 Est. Cost: ${cost_estimate:.4f}")
    print(f"📦 Kept: {len(results)}/{len(raw_text.split(config['pipeline']['chunking']['separator']))} chunks")
    print(f"📄 Report: {output_file}")
    print(f"📋 Logs: logs/pipeline.log (search for 'rejected' or 'skipped')")
    
    return report

if __name__ == "__main__":
    evaluate_pipeline()