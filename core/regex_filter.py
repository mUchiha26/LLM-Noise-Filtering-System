import re

def regex_filter(text: str):
    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove repeated whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove boilerplate (basic start)
    blacklist = ["click here", "subscribe", "buy now"]
    if any(word in text.lower() for word in blacklist):
        return ""

    return text.strip()
