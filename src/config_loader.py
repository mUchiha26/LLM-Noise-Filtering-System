"""
Config loader with strict secret/config separation.
Loads .env first, then config.yaml, and securely merges them at runtime.
"""
import os
import copy
import warnings
import yaml
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DEFAULT_CONFIG = {
    "pipeline": {
        "chunking": {"max_length": 512, "separator": "\n", "overlap": 0},
        "rules": {"enabled": True, "patterns": []},
        "llm": {
            "provider": "openai_compatible",
            "api_url": None,
            "model": "gpt-4o-mini",
            "temperature": 0.1,
            "max_tokens": 256,
            "timeout": 15,
            "prompt": {"system": "Return JSON only.", "user": "Analyze: {text}"}
        },
        "scoring": {"threshold": 0.75, "fallback_strategy": "discard"},
        "io": {"input_format": "json", "results_dir": "results", "results_format": "json", "logs_dir": "logs", "noise_log": "noise_log.jsonl"},
    }
}


def load_config(path: str = "config/config.yaml") -> dict[str, Any]:
    """Merge config.yaml with .env secrets. Env vars take precedence for security."""
    # Deep copy prevents mutating DEFAULT_CONFIG across repeated calls/tests.
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    config_path = Path(path)

    # 1️⃣ Load YAML logic/prompts
    if config_path.exists():
        with open(config_path) as f:
            user_cfg = yaml.safe_load(f) or {}
            _deep_update(cfg["pipeline"], user_cfg.get("pipeline", {}))

    # 2️⃣ Securely inject secrets from environment
    cfg["pipeline"]["llm"]["api_key"] = os.getenv("LLM_API_KEY")
    if os.getenv("LLM_PROVIDER"):
        cfg["pipeline"]["llm"]["provider"] = os.getenv("LLM_PROVIDER")
    threshold_env = os.getenv("SCORING_THRESHOLD")
    if threshold_env:
        cfg["pipeline"]["scoring"]["threshold"] = float(threshold_env)

    # 3️⃣ Soft validation (allows offline/mock testing)
    if not cfg["pipeline"]["llm"]["api_key"]:
        warnings.warn("⚠️  LLM_API_KEY missing from .env. Pipeline will use mock/fallback responses.", UserWarning)

    return cfg["pipeline"]


def _deep_update(base: dict, update: dict) -> None:
    """Recursively merge YAML config into defaults without losing nested structure."""
    for key, value in update.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            _deep_update(base[key], value)
        else:
            base[key] = value