def split_into_paragraphs(text: str):
    return [p.strip() for p in text.split("\n\n") if p.strip()]
