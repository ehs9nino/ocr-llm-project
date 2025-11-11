# 🧠 OCR–LLM Document Processing System (PeerJ 2025 Code Release)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17392715.svg)](https://doi.org/10.5281/zenodo.17392715)

This repository contains the **implementation and evaluation pipeline** for  
**“Traffic Document Processing with Large Language Models: A Benchmark for Information Extraction from Noisy OCR”**  
(Qader *et al.*, 2025, *PeerJ Computer Science*).

---

## 🔗 Related Dataset

The benchmark dataset accompanying this study is published separately:

**📦 Repository:** [Traffic OCR–LLM Benchmark Dataset](https://github.com/ehs9nino/traffic-ocr-llm-benchmark)  
**🆔 DOI:** [10.5281/zenodo.17392715](https://doi.org/10.5281/zenodo.17392715)

**Dataset Overview**
- 15 rate confirmation documents scans (semi-structured business forms)  
- 40 commercial driver license (CDL) scan results (identity-type layouts) 
- For rate confirmation includes (`.jpg` or `.png`) which can be directly used for whole pipeline available with there corresponding ground truths. 
- For driver's license sample includes: 4 document image (`.jpg` or `.png`), OCR text output (`.txt`), and corresponding ground-truth annotations (`.json`) well suitable for LLM stage.  
- All personal data were anonymized; synthetic identifiers were used for names and IDs  

---

## ⚙️ System Overview

This project implements a full **OCR → LLM → JSON extraction** workflow with a Flask web interface, MongoDB integration, and both local and cloud-based inference modes.

### 🧩 Components

| File / Directory | Description |
|------------------|--------------|
| `app.py` | Flask web interface for document upload, OCR + LLM inference, and database management |
| `ocr_llm.py` | Core pipeline (PaddleOCR + Hugging Face or local LLaMA inference) |
| `db.py` | MongoDB connector (supports both local and Atlas cloud URIs) |
| `templates/` | Jinja2 HTML templates |
| `static/` | Bootstrap assets and background image |
| `prompts/` | Predefined text-extraction prompts for each document type |
| `test_pipeline.py` | Local testing and LLM comparison |
| `OCR_Evaluation/`, `LLM_Evaluations/` | Reproducible experiment notebooks and outputs |

---

## 🧠 Technologies Used

| Layer | Library / Tool |
|-------|----------------|
| OCR | [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (v3, English) |
| OCR (Baseline) | [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) |
| LLM (API) | `mistralai/Mistral-Small-3.1-24B-Instruct-2503` via [Hugging Face Inference API](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) |
| LLM (Local) | [llama.cpp](https://github.com/ggerganov/llama.cpp) via `llama-cpp-python` |
| Backend | Flask (Python 3.12) |
| Database | MongoDB (local or [Atlas](https://www.mongodb.com/atlas)) |
| Frontend | HTML + Bootstrap + Jinja2 templates |

---

## 🧩 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ehs9nino/ocr-llm-project.git
cd ocr-llm-project
```

### 2. Create and Activate Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the project root.

**Option A – Using APIs (Recommended)**
```bash
HF_TOKEN=your_huggingface_token
MONGO_URI=your_mongodb_atlas_connection_uri
```

**Option B – Fully Local Mode**
```bash
HF_TOKEN=none
MONGO_URI=mongodb://localhost:27017
```

---

## 🚀 Running the Application

```bash
python3 app.py
```
Then open in your browser:
```bash
http://127.0.0.1:5000
```

### 🧭 Workflow

1. Upload a **Rate Confirmation** or **CDL** document  
2. OCR → LLM extraction produces structured JSON  
3. Results appear in editable form on the web interface  
4. Click **Save to Database** to store results in MongoDB  
5. Use **Admin View** to browse or download entries  

---

## 🧪 Evaluation & Methodology

The evaluation scripts reproduce all results reported in the paper.

| Directory | Purpose |
|------------|----------|
| `OCR_Evaluation/` | Tesseract vs. PaddleOCR comparison (confidence, speed, completeness) |
| `LLM_Evaluations/` | Structured extraction tests using Mistral, Phi, and LLaMA models |

**Evaluation Procedure**
- Cross-document comparative approach  
- Each OCR output processed by all LLMs using identical JSON prompts  
- Predictions compared against manually verified ground-truth annotations  
- Metrics computed per document and aggregated by field  
- Ablation-style comparison performed for text-only vs. vision-assisted pipelines  

**Assessment Metrics**
- **Exact Match** – Proportion of predictions identical to ground truth  
- **Macro F1** – Mean F1-score across all fields  
- **Per-field F1** – Field-specific accuracy (e.g., Load ID, Time, Address)  
- **Normalized Levenshtein Distance** – Character-level edit similarity  

---

## 📊 Example Output

```json
{
  "Full Name": "AHMAD NUROV",
  "License Number": "N939501400",
  "Expiration Date": "09-13-2025",
  "State": "NEW JERSEY",
  "Address": "390 BATES STREET PHILLIPSBURG, NJ 08865-3240",
  "Date of Birth": "09-13-1987"
}
```

---

## 📋 Requirements

- Python ≥ 3.10  
- Required libraries: `paddleocr`, `pytesseract`, `llama-cpp-python`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `flask`, `python-dotenv`, `pymongo`

---

## 📜 License

- **Code:** MIT License  
- **Dataset:** CC-BY-4.0  
- **Citation:**  
  Qader, E., Efremenko, D., & Derkach, D. (2025).  
  *Traffic Document Processing with Large Language Models: A Benchmark for Information Extraction from Noisy OCR.*  
  *PeerJ Computer Science.*  
  DOI: [10.5281/zenodo.17392715](https://doi.org/10.5281/zenodo.17392715)

---

## 🧱 Contribution Guidelines

Contributions are welcome through pull requests.  
For significant changes, please open an issue first to discuss the proposed modification.  
Ensure code is PEP8-compliant and accompanied by a brief test script or notebook.

---

## 💡 Notes for Reviewers

- The system supports both **local** and **API-based** inference.  
- All examples in `LLM_Evaluations/` reproduce the quantitative results in the paper.  
- Example figures and tables correspond directly to the manuscript’s OCR and LLM evaluation sections.  
- A small subset of anonymized documents is included for demonstration and reproducibility.

---

**Maintained by:** [Ehsan Qader](https://github.com/ehs9nino)  
📧 **Contact:** [eqader@hse.ru](mailto:eqader@hse.ru)
