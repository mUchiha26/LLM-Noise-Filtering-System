# Problem Definition — Noise/Relevance Filter

## 1. Problem Overview

OpenCRE relies on **high-quality, structured security content**.

However, real-world sources contain:

- Noise
- Redundant text
- Non-actionable information

This reduces:

- Mapping accuracy
- Knowledge quality
- Automation potential

---

## 2. Core Problem

> How can we automatically filter raw text to extract only **CRE-relevant content**?

---

## 3. System Role

The filter acts as a **pre-processing layer**:

```text
RAW DATA (Blogs, Docs, Reports)
                  |
                  v
Noise/Relevance Filter
                  |
                  v
Clean, Structured Security Text
                  |
                  v
OpenCRE System
```

---

## 4. Definitions

### Relevant Content

Text that:

- Defines a security requirement
- Is actionable and reusable
- Can be mapped to CRE / controls / vulnerabilities

Examples:

| Text                                    | Label    |
| --------------------------------------- | -------- |
| "Validate all inputs before processing" | Relevant |
| "Encrypt sensitive data at rest"        | Relevant |

---

### Noise

Text that:

- Is vague or generic
- Is not actionable
- Cannot be mapped to CRE

Examples:

| Text                        | Label |
| --------------------------- | ----- |
| "Security is important"     | Noise |
| "This article discusses..." | Noise |

---

## 5. Classification Objective

Binary classification:

`Input Text -> {Relevant (1), Noise (0)}`

---

## 6. Challenges

### Ambiguity

Some text is partially relevant

Example:

- "SQL injection is dangerous" → weak relevance

---

### Context Dependency

Meaning depends on surrounding text

---

### Imbalanced Data

More noise than useful content

---

## 7. Evaluation Considerations

### Metrics

| Metric    | Importance                      |
| --------- | ------------------------------- |
| Precision | Avoid false positives           |
| Recall    | Avoid missing important content |

Critical Insight:

> False negatives are more dangerous than false positives

---

## 8. System Design (High-Level)

```text
+-------------------+
|   Raw Documents   |
+-------------------+
          |
          v
+-------------------+
|   Text Chunking   |
+-------------------+
          |
          v
+-------------------+
|  Relevance Model  |
+-------------------+
          |
          v
+-------------------+
|  Filtered Output  |
+-------------------+
```

---

## 9. Solution Approaches

### Approach 1: Rule-Based

- Keywords
- Patterns

### Approach 2: ML-Based

- TF-IDF + Logistic Regression
- BERT-based models

### Approach 3: Hybrid (Recommended)

- Rules + ML + Semantic similarity

---

## 10. Success Criteria

The system should:

- Remove irrelevant content
- Preserve important security knowledge
- Improve mapping quality to CREs
- Be explainable and reproducible

---

## 11. Final Insight

> This is NOT just a classification problem.

It is a:

- Knowledge extraction problem
- Data quality problem
- Pre-processing problem for a security knowledge graph
