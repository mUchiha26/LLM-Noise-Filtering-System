import pytest
from unittest.mock import patch
from pipeline import run_pipeline

def test_pipeline_chaining_works(base_config):
    """🎓 Simulates full flow: chunk → filter → classify → collect"""
    with patch("core.llm_classifier.LLMClassifier.classify") as mock_clf:
        # Chunk 1: rejected by LLM | Chunk 2: accepted
        mock_clf.side_effect = [(False, "high"), (True, "high")]
        
        text = "Random tech blog\n\nCVE-2024-1234 SQL injection in Apache"
        results = run_pipeline(text, base_config)
        
        # Only the CVE chunk should survive
        assert len(results) == 1
        assert "CVE" in results[0]
        assert mock_clf.call_count == 2  # Called for both chunks that passed regex