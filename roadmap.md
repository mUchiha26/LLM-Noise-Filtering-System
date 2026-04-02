# Roadmap

## Phase 1: MVP Build (Day 1-2)

### Step-by-step

### ✅ Step 1 - Basic Input System (2-3h)

Accept:

- `.txt`
- raw string

```python
text = open("input.txt").read()
chunks = split_into_paragraphs(text)
```

### ✅ Step 2 - Regex Noise Filter (3-5h)

Remove:

- URLs
- ads
- repeated lines
- boilerplate phrases

```python
def regex_filter(text):
    # Remove URLs, ads, repeated lines, and boilerplate.
    return cleaned_text
```

### ✅ Step 3 - LLM Classification (CORE)

Use:

- API or local model (your whisper/LLM setup helps here)

Prompt example:

```text
Classify the following text:

Criteria:
- Is it a clear, actionable security requirement?
- Can it be reused across systems?

Answer ONLY:
Relevant / Noise

Text:
{chunk}
```

### ✅ Step 4 - Output

`[Relevant chunks only]`

### ✅ Step 5 - CLI Demo

```bash
python run.py input.txt
```

### MVP Deliverables

- `run.py`
- `filter.py`
- `llm_classifier.py`
- `README.md` (with demo)

## Phase 2: Public Visibility (Day 3-5)

### 🎯 Goal

Get noticed by OWASP.

### 🔥 Step 1 - Clean GitHub Repo

Your `README.md` should include:

- Problem (1 paragraph)
- Your approach (simple diagram)
- Demo example (before/after)

### 🔥 Step 2 - Post to OWASP

Where to post:

- GitHub Discussions
- Issues

Suggested post:

```text
Hi,

I've started building a prototype for the Noise/Relevance Filter module.

Current approach:
- Regex pre-filtering
- LLM-based classification for CRE-relevant content

Goal:
Filter raw security text into CRE-compatible information.

I'd really appreciate feedback on:
- Whether this aligns with OpenCRE expectations
- Possible improvements

Repo: [link]
```

### 🧠 Why this matters

You're signaling:

- initiative
- execution
- alignment

## Phase 3: Quick Iteration (Week 1-2)

After feedback:

### 🔧 Improve MVP

Add:

- confidence score
- better prompts
- few-shot examples

### ⚙️ Optional Upgrade

Replace LLM with:

- lightweight classifier (for credibility)

### 📊 Add Evaluation

Even small:

- 10 samples -> manually check accuracy

## Phase 4: Micro Contributions (Parallel)

### 🎯 Goal

Appear active in project.

Do:

- fix typos in docs
- improve explanations
- suggest ideas

## Final Strategy

You are optimizing for:

| Goal           | Strategy       |
| -------------- | -------------- |
| Get selected   | Show execution |
| Impress mentor | Show thinking  |
| Stand out      | Ship fast      |
