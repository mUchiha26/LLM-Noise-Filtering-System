"""
Configurable regex filter engine.
"""
import re
from typing import Dict, List, Optional


def apply_rules(text: str, config: Dict) -> Dict:
    """
    Apply regex patterns in order; first match wins.
    Returns: {"action": "discard"|"pass", "matched_rule": str|null, "reason": str}
    """
    if not config.get("enabled", True):
        return {"action": "pass", "matched_rule": None, "reason": "rules_disabled"}
    
    patterns: List[Dict] = config.get("patterns", [])
    
    for rule in patterns:
        pattern = rule.get("pattern")
        if not pattern:
            continue
        try:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return {
                    "action": rule.get("action", "discard"),
                    "matched_rule": rule.get("name", "unnamed"),
                    "reason": f"Matched regex: {pattern[:50]}..."
                }
        except re.error as e:
            # Log but don't crash (robustness for MVP)
            return {"action": "pass", "matched_rule": None, "reason": f"regex_error: {e}"}
    
    return {"action": "pass", "matched_rule": None, "reason": "no_rule_match"}