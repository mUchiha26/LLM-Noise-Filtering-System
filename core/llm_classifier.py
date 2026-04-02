import os
import requests
import logging
from typing import Tuple
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class LLMClassifier:
    def __init__(self, config: dict):
        self.config = config["llm"]
        self.api_key = os.getenv("OPENROUTER_API_KEY") if self.config["mode"] == "api" else None
        self.model = self.config["model"]
        self.prompt_tpl = self.config["prompt_template"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _call_api(self, prompt: str) -> str:
        if self.config["mode"] == "mock":
            return "YES"
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 5,
            "temperature": 0.0
        }
        
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=self.config["timeout"])
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _parse_response(self, raw: str) -> Tuple[bool, str]:
        cleaned = raw.strip().lower()
        if cleaned == "yes": return True, "high"
        if cleaned == "no": return False, "high"
        logger.warning(f"Ambiguous LLM response: '{raw}'")
        return False, "low"

    def classify(self, text: str) -> Tuple[bool, str]:
        if not text or len(text.strip()) < 5:
            return False, "invalid"
        try:
            raw = self._call_api(self.prompt_tpl.format(text=text))
            return self._parse_response(raw)
        except Exception as e:
            logger.error(f"LLM call failed: {e}", exc_info=True)
            return False, "error"