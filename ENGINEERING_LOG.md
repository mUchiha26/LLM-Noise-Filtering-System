# Engineering Log (Personal Notes)

## Purpose

This file is for personal refresh notes: forgotten concepts, new ideas, and quick reminders.

## Quick Index

- Pipeline design notes
- Core software engineering concepts
- Python structure concepts
- Fast review checklist

## Pipeline Notes (This Project)

Why a pipeline helps in this repo:

- Each step has one clear responsibility.
- Debugging is easier because steps are isolated.
- A component can be replaced without rewriting the whole system.

Main principle: Separation of Concerns (SoC).

## Core Engineering Concepts

### Entry Point

Simple: where program execution starts.

Professional: the interface between the caller (user/system) and the app logic.

Common entry-point types:

| Type | Example                    |
| ---- | -------------------------- |
| CLI  | `python pipeline.py`       |
| API  | `POST /filter`             |
| GUI  | User action (button click) |

### Separation of Concerns (SoC)

Definition: separate the system by concern (different problem types).

Applied here:

- `pipeline.py`: workflow orchestration
- `core/`: processing logic modules
- `data/`: data and examples
- `docs/`: documentation

Reminder: do not mix unrelated concerns in one place.

### Single Responsibility Principle (SRP)

Definition: each unit should have one reason to change.

Applied here:

- `core/chunker.py`: text splitting/chunking
- `core/regex_filter.py`: pattern-based cleaning
- `core/llm_classifier.py`: LLM-based classification

Reminder: one component, one primary job.

Nuance: SRP is more granular and stricter than SoC.

### Modularity

Definition: design as independent, replaceable blocks.

Applied here:

- Classifier can be swapped.
- Regex strategy can evolve independently.
- Chunking can change without touching classifier internals.

Reminder: the system should behave like composable building blocks.

### SoC vs SRP vs Modularity

| Concept    | Focus                       | Level      | Guiding question               |
| ---------- | --------------------------- | ---------- | ------------------------------ |
| SoC        | Separation of problem types | High       | Are concerns separated?        |
| SRP        | One job per unit            | Low        | Does this module do one thing? |
| Modularity | Independence of components  | Structural | Can I replace this safely?     |

## Python Concepts Refresher

### 1) Module

A module is one Python file (`.py`) containing code (functions, classes, variables).

```python
# llm_classifier.py
def classify(text):
        return True
```

Key idea:

- Smallest unit of code organization
- Imported with `import`

### 2) Package

A package is a folder that groups related modules.

```text
core/
        chunker.py
        regex_filter.py
        llm_classifier.py
```

Key idea:

- Structures larger projects
- Keeps related modules together

### 3) Library

A library is reusable code, often external, that can include many modules and packages.

Examples:

- `requests`: HTTP communication
- `numpy`: numerical computing
- `pandas`: data analysis

Usage:

```bash
pip install requests
```

```python
import requests
```

### 4) Class

A class is a blueprint for objects (behavior + state/config).

```python
class LLMClassifier:
        def __init__(self, mode):
                self.mode = mode

        def classify(self, text):
                return True
```

```python
clf = LLMClassifier("local")
clf.classify("text")
```

## Comparison Table

| Concept | Type      | Level    | Purpose                    |
| ------- | --------- | -------- | -------------------------- |
| Module  | File      | Low      | Organize code              |
| Package | Folder    | Medium   | Group modules              |
| Library | External  | High     | Reusable tools             |
| Class   | Structure | Internal | Encapsulate behavior/state |

## Relationship Mental Model

```text
Library (requests)
  -> Package (core/)
    -> Module (llm_classifier.py)
      -> Class (LLMClassifier)
        -> Method (classify)
```

Quick memory aid:

- Module = file
- Package = folder
- Library = external toolkit
- Class = machine inside the file

## Security & Configuration Concepts

### 🔐 API Key Management

**Core Principle**: Secrets never in code, never in git history.

#### Methods Compared

| Method                   | How                                        | Best For           | Learning Stage        |
| ------------------------ | ------------------------------------------ | ------------------ | --------------------- |
| `.env` + `python-dotenv` | Store in `.env`, load with `load_dotenv()` | Local dev, MVP     | ⭐⭐⭐⭐⭐ Start here |
| OS Environment Variables | `export KEY=val` in shell, `os.getenv()`   | Production, Docker | ⭐⭐⭐⭐ Next step    |
| Secrets Managers         | AWS Secrets Manager, HashiCorp Vault       | Enterprise, teams  | ⭐⭐ Advanced         |
| GitHub Secrets           | Repo Settings → Secrets → Actions          | CI/CD pipelines    | ⭐⭐⭐ For automation |

#### Safe Loading Pattern

```python
# utils/config_loader.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env into os.environ

def get_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("Set OPENROUTER_API_KEY in .env")
    return key
```

## Python venv: Isolation & Naming

### Core Rule

Virtual environments are **filesystem-scoped**, not name-scoped.  
`projectA/.venv` and `projectB/.venv` are completely isolated.

### Activation Mechanics

```bash
source .venv/bin/activate
```

## Shell Ergonomics: Aliases vs Functions for venv

### The Trap

`alias actv='source .venv/bin/activate'` works, but is **path-blind**.  
Fails or activates wrong env if run outside project root.

### Safer Pattern: Context-Aware Function

```bash
actv() {
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo "✅ Activated: $(basename "$VIRTUAL_ENV")"
    else
        echo "❌ No .venv in $(pwd)"
    fi
}
alias dactv='deactivate'
```

## Python venv vs PYTHONPATH: The ROS 2 Leak

### The Problem

`venv` isolates `site-packages`, but **Python also scans `$PYTHONPATH`**.  
ROS 2 (`setup.bash`) modifies `PYTHONPATH` globally.  
Result: `pip list` shows system/ROS packages inside a venv.

### How to Verify

```bash
echo $PYTHONPATH          # Shows injected paths
which python              # Should point to .venv/bin/python
pip list                  # Shows all visible packages (venv + PYTHONPATH)
```

## config_loader.py vs config.yaml: Location & Logic

### The Rule

`config.yaml` → Project root (data)  
`config_loader.py` → `utils/` or `core/` (code that reads data)

### Why Root is Standard

- IDEs, linters, and CI tools expect configs at root
- Matches ecosystem conventions (`package.json`, `pyproject.toml`, `Dockerfile`)
- Easy to find, edit, and version control

### Path Resolution Logic

```python
from pathlib import Path
# __file__ = /project/utils/config_loader.py
project_root = Path(__file__).parent.parent  # Up 2 levels → /project/
config_path = project_root / "config.yaml"   # Joins safely
```

## Entry Point vs Orchestrator vs Packaging

### The Distinction

| File/Concept    | Role                          | Runs When?                         |
| --------------- | ----------------------------- | ---------------------------------- |
| `setup.py`      | Packaging & install metadata  | `pip install .`                    |
| `main.py`       | True entry point (CLI/I/O)    | `noise-filter` or `python main.py` |
| `pipeline.py`   | Orchestrator (workflow logic) | Imported by `main.py`              |
| `core/` modules | Single-responsibility logic   | Imported by orchestrator           |

### How `setup.py` Declares Entry Points

```python
entry_points={
    "console_scripts": [
        "noise-filter=main:main"  # CLI command → module:function
    ]
}
```

## Environment Mismatch: `ModuleNotFoundError` in IDE Runners

### Symptom

`ModuleNotFoundError` despite successful `pip install`.

### Root Cause

IDE runners (Code Runner, etc.) often bypass the activated terminal and use **system Python**.  
`venv` isolation only works when you explicitly run `./.venv/bin/python` or source the env first.

### Fix Pattern

```bash
actv                          # 1. Activate environment
pip install <package>         # 2. Install into .venv
python path/to/script.py      # 3. Run with venv Python explicitly
```

## Python Imports & `sys.path`: Why `ModuleNotFoundError` Happens

### The Trap

`python core/script.py` → Python only searches `core/` for imports.  
Sibling packages (`utils/`) become invisible.

### The Fix

```bash
python -m core.llm_classifier  # ✅ Adds project root to sys.path
```

## Common Pitfalls

## Practical Rules

## Review Checklist

## Closing Insight

Clean structure scales. Messy structure slows everything down.
