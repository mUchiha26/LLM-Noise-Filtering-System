import os
import pytest
from pipeline import run_pipeline
from utils.config_loader import load_config

@pytest.mark.skipif(not os.getenv("OPENROUTER_API_KEY", "").startswith("sk-or-"), reason="Real API key required")
def test_real_api_accepts_security_content():
    config = load_config()
    config["llm"]["mode"] = "api"
    results = run_pipeline("CVE-2024-10001 describes a remote code execution flaw in nginx.", config)
    assert len(results) >= 1
    assert "CVE" in results[0]

@pytest.mark.skipif(not os.getenv("OPENROUTER_API_KEY", "").startswith("sk-or-"), reason="Real API key required")
def test_real_api_rejects_noise():
    config = load_config()
    config["llm"]["mode"] = "api"
    results = run_pipeline("This is a cooking recipe for pasta carbonara.", config)
    assert len(results) == 0