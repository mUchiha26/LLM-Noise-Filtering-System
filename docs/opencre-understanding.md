# OpenCRE Understanding

## 1. What is OpenCRE?

**OpenCRE (Open Common Requirement Enumeration)** by OWASP is a system that organizes security knowledge into a **structured, connected graph** of requirements.

It unifies:

- Security standards (NIST, ISO, OWASP, etc.)
- Vulnerabilities (CWE, CAPEC)
- Best practices
- Code, tests, and tools

Key idea:

> OpenCRE is a **knowledge graph of security requirements**, not just a list.

---

## 2. Core Components

### Entity Types

| Entity                   | Role                                         |
| ------------------------ | -------------------------------------------- |
| CRE (Common Requirement) | Central security concept (hub node)          |
| Control                  | Specific requirement from a standard         |
| Artifact                 | Supporting resource (CWE, code, tools, etc.) |
| Mapping                  | Link between entities                        |

---

## 3. System Architecture (Graph View)

```text
     +------------------+
     |   CWE / CAPEC    |
     +------------------+
         ^
         |

+-------------+  +------------------+  +-------------+
| NIST        |->| CRE              |<-| ASVS        |
| Control     |  | (Core Concept)   |  | Control     |
+-------------+  +------------------+  +-------------+
             |
             v
         +------------------+
         |   Code / Tests   |
         +------------------+
```

Insight:

- CRE is the **hub**
- Everything connects through it

---

## 4. CRE Structure

Each CRE follows a structured schema:

### CRE Schema

| Field         | Description                       |
| ------------- | --------------------------------- |
| ID            | Unique identifier (e.g., CRE-123) |
| Name          | Short title                       |
| Description   | Clear security requirement        |
| Tags          | Category (auth, crypto, etc.)     |
| Relationships | Links to other CREs               |
| Mappings      | Links to controls & artifacts     |

---

## 5. Example CRE (Simplified)

**CRE-001: Input Validation**

Description:
All user inputs must be validated and sanitized before processing.

Mappings:

- NIST: SI-10
- ASVS: V5.1
- CWE-79 (XSS)

Artifacts:

- Test cases
- Secure coding examples

---

## 6. Mapping System (Core Value)

Mappings are stored as **edges in a graph**:

- CRE -> Control
- CRE -> CWE
- CRE -> Tool

Example:

- CRE-123 -> NIST AC-3
- CRE-123 -> CWE-79

Insight:

> OpenCRE enables **cross-standard visibility**

---

## 7. Mental Model (IMPORTANT)

Think of OpenCRE as:

```text
SECURITY KNOWLEDGE GRAPH
          |
--------------------------------
|              |               |
CREs        Controls       Artifacts
```

---

## 8. What Makes Text CRE-Relevant?

A text is relevant if it:

- Defines a **clear security requirement**
- Is **actionable**
- Can be **mapped to standards or vulnerabilities**
- Is **reusable across contexts**

Examples:

- "Validate all user inputs"
- "Encrypt sensitive data at rest"

---

## 9. What is NOT Useful?

- Generic statements
- Marketing or motivational text
- Long narratives without actionable info
- Context-specific internal wording

Examples:

- "Security is important"
- "Follow best practices"

---

## 10. Key Insight for This Project

Your system (Noise/Relevance Filter) acts as:

`Raw Text -> Filter -> CRE-Compatible Content -> OpenCRE Graph`
