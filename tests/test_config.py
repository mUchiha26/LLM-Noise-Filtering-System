import pytest
from utils.config_loader import load_config

def test_config_returns_valid_structure():
    config = load_config()
    assert "pipeline" in config
    assert "llm" in config
    assert config["pipeline"]["chunking"]["min_length"] >= 0
    assert len(config["llm"]["prompt_template"]) > 50

def test_config_env_override(monkeypatch):
    """🎓 Verifies .env vars override config.yaml defaults"""
    monkeypatch.setenv("LLM_MODEL", "anthropic/claude-3-haiku")
    config = load_config()
    assert config["llm"]["model"] == "anthropic/claude-3-haiku"