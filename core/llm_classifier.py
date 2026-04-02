"""
🎓 llm_classifier.py - LLM-based classification
🎓 Why: Handle nuanced security content that regex misses
🎓 MVP Focus: Simplicity, safety, testability
"""
import requests
import logging
from typing import Tuple
from tenacity import retry, stop_after_attempt, wait_exponential

from utils.config_loader import get_api_key

logger = logging.getLogger(__name__)

class LLMClassifier:
    def __init__(self, config: dict):
        self.config = config["llm"]
        self.api_key = get_api_key() if self.config["mode"] == "api" else None
        self.model = self.config["model"]
        self.prompt_template = self.config["prompt_template"]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _call_api(self, prompt: str) -> str:
        """🎓 Safe API call with retries"""
        if self.config["mode"] == "mock":
            # 🎓 Mock mode for testing without API calls
            logger.debug("Mock mode: returning 'YES'")
            return "YES"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 10,  # 🎓 Limit output to YES/NO
            "temperature": 0   # 🎓 Deterministic responses
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.config["timeout"]
        )
        response.raise_for_status()  # 🎓 Raise on HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    
    def _parse_response(self, raw: str) -> Tuple[bool, str]:
        """🎓 Strict parsing with confidence levels"""
        cleaned = raw.strip().lower()
        
        if cleaned == "yes":
            return True, "high"
        elif cleaned == "no":
            return False, "high"
        elif any(word in cleaned for word in ["maybe", "uncertain", "not sure"]):
            logger.warning(f"Ambiguous LLM response: '{raw}'")
            return False, "low"  # Safe default
        else:
            logger.error(f"Unparseable response: '{raw}'")
            return False, "unknown"
    
    def classify(self, text: str) -> Tuple[bool, str]:
        """
        Main entry point: classify text.
        🎓 Returns (is_relevant, confidence) for pipeline decisions.
        """
        # 🎓 Input validation
        if not text or len(text.strip()) < 5:
            return False, "invalid"
        
        # 🎓 Build prompt with delimiters (prompt injection defense)
        prompt = self.prompt_template.format(text=text)
        
        try:
            raw_response = self._call_api(prompt)
            return self._parse_response(raw_response)
        except Exception as e:
            logger.error(f"Classification failed: {e}", exc_info=True)
            return False, "error"  # Safe fallback

# 🎓 Simple test
if __name__ == "__main__":
    import yaml
    from utils.config_loader import load_config
    
    config = load_config()
    classifier = LLMClassifier(config)
    
    test_cases = [
        "CVE-2024-1234: SQL injection in login form",
        "Buy now! 50% off security software",
        "This is just random text"
    ]
    
    for text in test_cases:
        result, confidence = classifier.classify(text)
        print(f"'{text}' → {result} ({confidence})")