from config_loader import load_config


def test_load_config_isolated_between_calls(tmp_path, monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("SCORING_THRESHOLD", raising=False)

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "pipeline:\n"
        "  scoring:\n"
        "    threshold: 0.9\n",
        encoding="utf-8",
    )

    first = load_config(str(config_path))
    second = load_config(str(config_path))

    assert first["scoring"]["threshold"] == 0.9
    assert second["scoring"]["threshold"] == 0.9


def test_load_config_uses_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("SCORING_THRESHOLD", "0.66")

    config_path = tmp_path / "config.yaml"
    config_path.write_text("pipeline: {}\n", encoding="utf-8")

    cfg = load_config(str(config_path))
    assert cfg["scoring"]["threshold"] == 0.66
