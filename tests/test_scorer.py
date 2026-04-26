from core.scorer import apply_scoring


def test_apply_scoring_retain_when_above_threshold():
    out = apply_scoring(
        {"relevance": 0.91, "category": "vuln", "reason": "clear vulnerability"},
        {"threshold": 0.75, "fallback_strategy": "discard"},
    )
    assert out["keep"] is True
    assert out["decision"] == "retain"
    assert out["confidence"] == "high"


def test_apply_scoring_fallback_on_error():
    out = apply_scoring(
        {"relevance": 0.0, "category": "error", "reason": "timeout"},
        {"threshold": 0.75, "fallback_strategy": "discard"},
    )
    assert out["keep"] is False
    assert out["decision"] == "fallback"
