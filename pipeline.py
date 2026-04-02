from core.chunker import split_into_paragraphs
from core.regex_filter import regex_filter
from core.llm_classifier import LLMClassifier


def run_pipeline(text: str):
    classifier = LLMClassifier()
    chunks = split_into_paragraphs(text)

    results = []

    for chunk in chunks:
        cleaned = regex_filter(chunk)
        if not cleaned:
            continue

        if classifier.classify(cleaned):
            results.append(cleaned)

    return results
