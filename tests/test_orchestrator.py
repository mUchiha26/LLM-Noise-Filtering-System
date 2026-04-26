from pathlib import Path

from orchestrator import _flatten_decision, run_pipeline


def test_run_pipeline_txt_end_to_end(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "orchestrator.classify_with_llm",
        lambda text, cfg: {"relevance": 0.95, "category": "vuln", "reason": "security-relevant"},
    )

    input_file = tmp_path / "input.txt"
    input_file.write_text("Apache/2.4.52\nSQL injection prevention with parameterized queries\n", encoding="utf-8")

    config = {
        "chunking": {"max_length": 512, "separator": "\n", "overlap": 0},
        "rules": {
            "enabled": True,
            "patterns": [{"name": "banner", "pattern": r"^Apache/", "action": "discard"}],
        },
        "llm": {"api_key": "fake"},
        "scoring": {"threshold": 0.75, "fallback_strategy": "discard"},
        "io": {"logs_dir": str(tmp_path), "noise_log": "noise_log.jsonl"},
    }

    retained, discarded = run_pipeline(str(input_file), config, "scan_test")

    assert len(retained) == 1
    assert len(discarded) == 1
    assert retained[0]["source"] == "llm"
    assert discarded[0]["source"] == "rule"
    assert "hash" in retained[0]
    assert retained[0]["keep"] is True


def test_run_pipeline_supports_csv_input(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "orchestrator.classify_with_llm",
        lambda text, cfg: {"relevance": 0.2, "category": "noise", "reason": "not actionable"},
    )

    csv_path = tmp_path / "input.csv"
    csv_path.write_text("text,label\nSecurity is important,noise\n", encoding="utf-8")

    config = {
        "chunking": {"max_length": 512, "separator": "\n", "overlap": 0},
        "rules": {"enabled": False, "patterns": []},
        "llm": {"api_key": "fake"},
        "scoring": {"threshold": 0.75, "fallback_strategy": "discard"},
        "io": {"logs_dir": str(tmp_path), "noise_log": "noise_log.jsonl"},
    }

    retained, discarded = run_pipeline(str(csv_path), config, "scan_csv")

    assert retained == []
    assert len(discarded) == 1
    assert discarded[0]["original"]["label"] == "noise"


def test_flatten_decision_unwraps_nested_structure():
    nested = {
        "keep": False,
        "decision": {
            "keep": False,
            "decision": {
                "keep": False,
                "decision": "fallback",
                "confidence": "low",
                "reason": "parse_error",
            },
            "confidence": "unknown",
        },
        "confidence": "unknown",
    }

    flat = _flatten_decision(nested)
    assert flat["decision"] == "fallback"
    assert flat["confidence"] == "low"
