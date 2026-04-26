"""
Provider-agnostic LLM classifier with config-driven prompts and secure key handling.
Why: One unified HTTP caller avoids vendor lock-in. Prompts live in config.yaml.
     Secrets are injected at runtime via config_loader.py (never hardcoded).
"""
import json
import logging
import re
from typing import Dict

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class LLMResponse(BaseModel):
    """Strict schema for LLM output validation."""
    relevance: float = Field(..., ge=0.0, le=1.0)
    category: str = Field(...)
    reason: str = Field(..., max_length=200)

_DEFAULT_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "openai_compatible": "https://api.openai.com/v1/chat/completions",
    "ollama": "http://localhost:11434/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
}

def classify_text(text: str, config: Dict) -> Dict:
    """Public entry point. Handles errors and delegates to unified caller."""
    try:
        if httpx is None:
            raise ImportError("httpx required: pip install httpx")
        return _call_llm_provider(text, config)
    except Exception as e:
        logger.error(f"LLM classification failed: {e}")
        return _heuristic_fallback(text, f"llm_error: {e}")


def classify_with_llm(text: str, config: Dict) -> Dict:
    """Backward-compatible alias used by the pipeline orchestrator."""
    return classify_text(text, config)

def _call_llm_provider(text: str, config: Dict) -> Dict:
    """
    UNIFIED LLM CALLER: Single function for all providers.
    Flow: Extract config → Build prompt/payload → HTTP POST → Parse → Validate
    """
    provider = config.get("provider", "openai_compatible").lower()
    api_key = config.get("api_key")  # Injected securely by config_loader
    model = config.get("model", "gpt-4o-mini")

    # 1️⃣ Load prompts from config (zero hardcoding)
    prompt_cfg = config.get("prompt", {})
    system_prompt = prompt_cfg.get("system", "Return JSON only.")
    user_prompt = prompt_cfg.get("user", "Analyze: {text}").format(text=text)

    # Fallback to mock if no key (enables offline/CI testing)
    if not api_key:
        logger.warning("LLM_API_KEY missing; using mock response")
        return _heuristic_fallback(text, "missing_api_key")

    # 2️⃣ Resolve endpoint & build request
    api_url = _resolve_api_url(provider, config.get("api_url"))
    payload, headers = _build_request(provider, model, system_prompt, user_prompt, config)

    # Inject auth header securely
    if provider == "anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
    else:
        headers["Authorization"] = f"Bearer {api_key}"

    # 3️⃣ Execute HTTP call
    with httpx.Client(timeout=config.get("timeout", 15)) as client:
        resp = client.post(api_url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    # 4️⃣ Extract content based on provider format
    if provider == "anthropic":
        raw_content = data.get("content", [{}])[0].get("text", "")
    else:
        raw_content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

    return _validate_response(raw_content, text)

def _build_request(provider: str, model: str, system: str, user: str, config: dict) -> tuple:
    """Builds provider-specific JSON payload and base headers."""
    base_headers = {"Content-Type": "application/json"}

    if provider == "anthropic":
        return {
            "model": model,
            "max_tokens": config.get("max_tokens", 256),
            "system": system,
            "messages": [{"role": "user", "content": user}],
            "temperature": config.get("temperature", 0.1)
        }, base_headers

    # OpenAI-compatible format (covers Ollama, Groq, vLLM, LM Studio, etc.)
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": config.get("temperature", 0.1),
        "max_tokens": config.get("max_tokens", 256),
        "response_format": {"type": "json_object"}
    }, base_headers


def _resolve_api_url(provider: str, configured_url: str | None) -> str:
    """Accept provider base URLs and normalize to the correct chat endpoint."""
    if not configured_url:
        return _DEFAULT_ENDPOINTS.get(provider, _DEFAULT_ENDPOINTS["openai_compatible"])

    url = configured_url.strip().rstrip("/")

    # Anthropic endpoint is not OpenAI-compatible and should be used as-is.
    if provider == "anthropic":
        return url

    if url.endswith("/chat/completions") or url.endswith("/messages"):
        return url

    # Common pattern: users set base URL like https://openrouter.ai/api/v1.
    if url.endswith("/v1"):
        return f"{url}/chat/completions"

    return url

def _validate_response(raw_json: str, original_text: str) -> Dict:
    """Parses LLM output and enforces schema via Pydantic."""
    try:
        data = _extract_json_payload(raw_json)
        validated = LLMResponse(**data)
        return validated.model_dump()
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"LLM output validation failed: {e}")
        return _heuristic_fallback(original_text, f"validation_error: {e}")


def _extract_json_payload(raw_content: str) -> Dict:
    """Extract JSON object from plain JSON, fenced blocks, or mixed responses."""
    text = (raw_content or "").strip()
    if not text:
        raise json.JSONDecodeError("empty response", "", 0)

    # Fast path: strict JSON object.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Common model format: fenced JSON markdown.
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return json.loads(fenced.group(1))

    # Best-effort extraction of first JSON object from mixed text.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end + 1])

    raise json.JSONDecodeError("no JSON object found", text, 0)


def _heuristic_fallback(text: str, reason: str) -> Dict:
    """Conservative offline fallback tuned to avoid missing clearly security-relevant text."""
    lowered = (text or "").lower()
    keywords = (
        "cve-", "vulnerability", "exploit", "rce", "xss", "csrf", "sqli",
        "sql injection", "privilege escalation", "least privilege", "encrypt",
        "parameterized", "csp", "iam", "misconfiguration", "patch"
    )
    matches = sum(1 for kw in keywords if kw in lowered)

    if matches >= 2:
        relevance = 0.9
        category = "vuln"
    elif matches == 1:
        relevance = 0.78
        category = "other"
    else:
        relevance = 0.2
        category = "noise"

    return {
        "relevance": relevance,
        "category": category,
        "reason": f"heuristic_fallback ({reason})"
    }