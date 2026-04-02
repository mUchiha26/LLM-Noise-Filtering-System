import pytest
from core.chunker import split_into_chunks
from core.regex_filter import apply_regex_filter
from core.llm_classifier import LLMClassifier

def test_chunker_filters_and_truncates(base_config):
    cfg = {"pipeline": {"chunking": {"separator": "\n\n", "min_length": 5, "max_length": 20}}}
    chunks = split_into_chunks("Hi\n\nCVE-2024 test\n\n" + "x"*50, cfg)
    assert len(chunks) == 2
    assert chunks[1].endswith("...[truncated]")

def test_regex_blacklist(base_config):
    assert apply_regex_filter("Click here for deals", base_config) == ""

def test_regex_whitelist_wins(base_config):
    result = apply_regex_filter("Buy now! CVE-2024-123 is critical", base_config)
    assert "CVE-2024-123" in result

def test_llm_mock_classification(base_config):
    clf = LLMClassifier(base_config)
    res, conf = clf.classify("SQL injection prevention")
    assert res is True and conf == "high"