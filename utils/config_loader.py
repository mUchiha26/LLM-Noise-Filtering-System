import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

def load_config(config_path: str = "config.yaml") -> dict:
    path = Path(__file__).parent.parent / config_path if not Path(config_path).is_absolute() else Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found at {path}")
    
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    
    # Env overrides
    if os.getenv("LLM_MODEL"): config["llm"]["model"] = os.getenv("LLM_MODEL")
    if os.getenv("LOG_LEVEL"): config["logging"]["level"] = os.getenv("LOG_LEVEL")
    
    if config["llm"]["mode"] == "api" and not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY missing in .env for API mode")
    
    return config