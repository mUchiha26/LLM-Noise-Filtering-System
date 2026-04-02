"""
🎓 regex_filter.py - Fast, cheap rule-based filtering
🎓 Why: Catch obvious noise before spending LLM tokens
"""
import re
from typing import List

def load_patterns(config: dict) -> tuple[List[str], List[str]]:
    """🎓 Load regex patterns from config"""
    rf_config = config["pipeline"]["regex_filter"]
    return (
        rf_config.get("blacklist_patterns", []),
        rf_config.get("whitelist_patterns", [])
    )

def regex_filter(text: str, config: dict) -> str:
    """
    Filter text using regex rules.
    🎓 Returns cleaned text, or empty string if blacklisted.
    """
    if not config["pipeline"]["regex_filter"]["enabled"]:
        return text
    
    blacklist, whitelist = load_patterns(config)
    
    # 🎓 Check whitelist first: if matches, keep regardless
    for pattern in whitelist:
        if re.search(pattern, text, re.IGNORECASE):
            return text  # Keep security-relevant content
    
    # 🎓 Check blacklist: if matches, remove
    for pattern in blacklist:
        if re.search(pattern, text, re.IGNORECASE):
            return ""  # Filter out spam/marketing
    
    # 🎓 Basic cleanup: remove extra whitespace
    return re.sub(r'\s+', ' ', text).strip()

# 🎓 Test inline
#if __name__ == "__main__":
    test_config = {
        "pipeline": {
            "regex_filter": {
                "enabled": True,
                "blacklist_patterns": ["buy now", "click here"],
                "whitelist_patterns": [r"CVE-\d{4}"]
            }
        }
    }
    print(regex_filter("Buy now! CVE-2024-1234", test_config))  # Should keep (whitelist wins)
    print(regex_filter("Click here for deals", test_config))    # Should filter (blacklist)