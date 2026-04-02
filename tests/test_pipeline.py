"""
🎓 test_pipeline.py - Learn testing by doing
🎓 Why: Catch regressions early; document expected behavior
"""
from pathlib import Path
import sys

import pytest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import run_pipeline
from utils.config_loader import load_config

@pytest.fixture
def test_config():
    """🎓 Override config for testing"""
    config = load_config()
    config["llm"]["mode"] = "mock"  # Avoid real API calls
    config["pipeline"]["regex_filter"]["enabled"] = True
    return config

def test_regex_filters_spam(test_config):
    """🎓 Verify blacklist works"""
    spam_text = "Click here for amazing deals!"
    results = run_pipeline(spam_text, config=test_config)
    assert len(results) == 0, "Spam should be filtered"

def test_whitelist_preserves_security_content(test_config):
    """🎓 Verify whitelist overrides blacklist"""
    # Contains both blacklist word AND CVE pattern
    text = "Buy now! CVE-2024-1234 is critical"
    results = run_pipeline(text, config=test_config)
    assert len(results) == 1, "Whitelisted content should pass"
    assert "CVE-2024-1234" in results[0]

@patch("core.llm_classifier.LLMClassifier.classify")
def test_llm_classification(mock_classify, test_config):
    """🎓 Test LLM decision logic with mock"""
    # Mock returns (is_relevant, confidence)
    mock_classify.return_value = (True, "high")
    
    text = "SQL injection prevention techniques"
    results = run_pipeline(text, config=test_config)
    
    assert len(results) == 1
    mock_classify.assert_called_once()

def test_empty_input_handling(test_config):
    """🎓 Edge case: empty or tiny input"""
    assert run_pipeline("", config=test_config) == []
    assert run_pipeline("Hi", config=test_config) == []  # Below min_length

# 🎓 Run tests: python -m pytest tests/ -v