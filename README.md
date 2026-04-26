# 🧠 LLM-Based Noise Filtering System

## 📖 Description

An intelligent filtering system that removes noisy and irrelevant data from logs using a hybrid approach combining rule-based filtering and Large Language Models (LLMs).

The project simulates a real-world AI pipeline used in cybersecurity and data processing systems, focusing on extracting meaningful information from large volumes of unstructured data.

---

## 🎯 Goals

- Reduce noise in logs and text data
- Identify relevant security-related information
- Build a real-world AI pipeline
- Evaluate system performance using manual labeling

---

## ⚙️ Tech Stack

- Python
- Regular Expressions (Regex)
- LLM APIs (OpenAI or open-source models)
- JSON / Text Processing

---

## 🧠 Key Concepts

- Data preprocessing
- Hybrid systems (rules + AI)
- Prompt engineering
- Pipeline architecture
- AI evaluation (accuracy, testing)

---

## 🏗️ Workflow

```mermaid
flowchart TD
  A["Raw Input"] --> B["main.py"]
  B --> C["config_loader.py"]
  C --> D["orchestrator.py"]
  D --> E["chunker.py"]
  E --> F["regex_filter.py"]
  F -->|Noise| G["logs/noise_log.jsonl"]
  F -->|Pass| H["llm_classifier.py"]
  H --> I["scorer.py"]
  I -->|Drop| G
  I -->|Keep| J["results/scan_id.json"]
```

---

## 🚀 Features

- Rule-based noise filtering
- LLM-powered relevance classification
- Scoring system for decision making
- Modular pipeline design
- Easy to extend and integrate

---

## 📂 Project Structure

```text
LLM Noise Filtering System/
|-- ENGINEERING_LOG.md
|-- README.md
|-- setup.py
|-- requirements.txt
|-- src/
|   |-- main.py
|   |-- config_loader.py
|   |-- orchestrator.py
|   `-- core/
|       |-- chunker.py
|       |-- regex_filter.py
|       |-- llm_classifier.py
|       `-- scorer.py
|-- config/
|   `-- config.yaml
|-- data/
|-- docs/
|-- logs/
|-- results/
`-- tests/
```

---

## 🧪 Usage

### Prerequisites

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your LLM_API_KEY
```

### Run the System

```bash
# Basic usage
python src/main.py --input data/raw_spiderfoot_sample.json

# With custom config and output directory
python src/main.py \
  --input data/target_recon.json \
  --config config/custom_rules.yaml \
  --output-dir results/custom_scan

# Dry-run mode (rules only, no LLM calls)
SCORING_THRESHOLD=1.0 python src/main.py --input data/sample.json
```

## 📊 Evaluation

The system is evaluated using a manually labeled dataset:

- Each log is labeled as **Relevant** or **Noise**
- Model predictions are compared against ground truth

### Accuracy Formula

```text
accuracy = correct_predictions / total_samples
```

This ensures reliable performance and helps improve prompt design.

---

## 🔮 Future Improvements

- Add API with FastAPI
- Improve scoring logic
- Support real-time log streams
- Optimize LLM usage (cost + speed)
- Integrate with security tools

---

## 📚 Learning Purpose

This project is designed to understand how modern AI systems work by combining:

- rule-based logic
- machine intelligence
- structured pipelines

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome!  
Feel free to open issues or submit pull requests.

---

## 📌 Author

**Maintainer**: Yasseene  
**GitHub**: [@mUchiha26](https://github.com/mUchiha26)
