import re

def apply_regex_filter(text: str, config: dict) -> str:
    if not config["pipeline"]["regex_filter"]["enabled"]:
        return text
    
    cfg = config["pipeline"]["regex_filter"]
    # Whitelist wins
    for pat in cfg.get("whitelist_patterns", []):
        if re.search(pat, text, re.IGNORECASE):
            return text
    # Blacklist removes
    for pat in cfg.get("blacklist_patterns", []):
        if re.search(pat, text, re.IGNORECASE):
            return ""
    
    return re.sub(r"\s+", " ", text).strip()