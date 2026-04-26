"""
Threshold-based scoring with confidence calibration.
"""
from typing import Dict


def apply_scoring(llm_result: Dict, config: Dict) -> Dict:
    """
    Apply threshold + fallback logic; enrich with confidence levels.
    Returns: {"keep": bool, "score": float, "decision": str, "confidence": str}
    """
    threshold = config.get("threshold", 0.75)
    fallback = config.get("fallback_strategy", "discard")
    
    score = llm_result.get("relevance", 0.0)
    
    # Handle error/missing responses
    if llm_result.get("category") == "error":
        return {
            "keep": fallback == "retain",
            "score": 0.0,
            "decision": "fallback",
            "confidence": "low",
            "reason": llm_result.get("reason", "llm_error")
        }
    
    # Confidence calibration (simple heuristic for MVP)
    if score >= 0.9:
        confidence = "high"
    elif score >= threshold:
        confidence = "medium"
    elif score >= threshold - 0.15:
        confidence = "uncertain"  # Could trigger human review later
    else:
        confidence = "low"
    
    return {
        "keep": score >= threshold,
        "score": round(score, 3),
        "decision": "retain" if score >= threshold else "discard",
        "confidence": confidence,
        "reason": llm_result.get("reason", "no_reason_provided")
    }