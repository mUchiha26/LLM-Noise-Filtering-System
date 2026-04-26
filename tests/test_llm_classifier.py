from core.llm_classifier import _extract_json_payload, classify_text


def test_extract_json_payload_from_fenced_block():
    raw = """Here is the result:\n```json\n{\"relevance\": 0.88, \"category\": \"vuln\", \"reason\": \"contains CVE\"}\n```"""
    out = _extract_json_payload(raw)
    assert out["relevance"] == 0.88
    assert out["category"] == "vuln"


def test_classify_text_uses_heuristic_without_httpx(monkeypatch):
    monkeypatch.setattr("core.llm_classifier.httpx", None)
    out = classify_text("CVE-2024-1234 remote code execution vulnerability", {"provider": "openai"})
    assert out["relevance"] >= 0.78
    assert out["category"] in {"vuln", "other"}
