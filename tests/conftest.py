import pytest
from utils.config_loader import load_config

@pytest.fixture
def base_config():
    """🎓 Loads real config, forces mock mode for safe/fast testing"""
    config = load_config()
    config["llm"]["mode"] = "mock"
    return config