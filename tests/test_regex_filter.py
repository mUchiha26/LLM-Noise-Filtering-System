from core.regex_filter import apply_rules


def test_apply_rules_discards_on_match():
    cfg = {
        "enabled": True,
        "patterns": [{"name": "banner", "pattern": r"^Apache/", "action": "discard"}],
    }
    out = apply_rules("Apache/2.4.52", cfg)
    assert out["action"] == "discard"
    assert out["matched_rule"] == "banner"


def test_apply_rules_passes_when_no_match():
    cfg = {
        "enabled": True,
        "patterns": [{"name": "banner", "pattern": r"^Apache/", "action": "discard"}],
    }
    out = apply_rules("Use parameterized SQL queries", cfg)
    assert out["action"] == "pass"
    assert out["matched_rule"] is None
