"""
🎓 config_loader.py - Central config management
🎓 Why: Avoid scattering config logic; enable easy environment switching
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# 🎓 Load .env first so env vars override config if needed
load_dotenv()

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load YAML config and merge with environment variables.
    🎓 Env vars take precedence (e.g., for secrets).
    """
    # Default config path
    resolved_path = Path(config_path)
    if not resolved_path.is_absolute():
        resolved_path = Path(__file__).parent.parent / resolved_path
    
    # Load YAML
    with open(resolved_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # 🎓 Override with env vars for sensitive/variable settings
    if os.getenv("LLM_MODEL"):
        config["llm"]["model"] = os.getenv("LLM_MODEL")
    if os.getenv("LOG_LEVEL"):
        config["logging"]["level"] = os.getenv("LOG_LEVEL")
    
    # 🎓 Validate required fields
    if not os.getenv("OPENROUTER_API_KEY") and config["llm"]["mode"] == "api":
        raise ValueError("OPENROUTER_API_KEY env var required for API mode")
    
    return config

def get_api_key() -> str:
    """🎓 Safe API key retrieval - single source of truth"""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("API key not found. Set OPENROUTER_API_KEY in .env")
    return key