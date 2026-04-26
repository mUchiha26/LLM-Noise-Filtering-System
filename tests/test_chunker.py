from core.chunker import chunk_text


def test_chunk_text_returns_single_chunk_when_short():
    text = "short security text"
    chunks = chunk_text(text, {"max_length": 100, "separator": "\n", "overlap": 0})
    assert chunks == [text]


def test_chunk_text_splits_long_text():
    text = "line1\nline2\nline3\nline4"
    chunks = chunk_text(text, {"max_length": 8, "separator": "\n", "overlap": 0})
    assert len(chunks) >= 2
    assert all(isinstance(c, str) and c for c in chunks)
