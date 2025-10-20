# 🧠 OCR–LLM Document Processing System (PeerJ 2025 Code Release)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17392715.svg)](https://doi.org/10.5281/zenodo.17392715)

This repository contains the **implementation and evaluation pipeline** used in  
**“Traffic Document Processing with Large Language Models: A Benchmark for Information Extraction from Noisy OCR”**  
(Qader *et al.*, 2025, *PeerJ Computer Science*).

---

## 🔗 Related Dataset

The benchmark dataset accompanying this study is published separately:

**📦 Repository:** [Traffic OCR–LLM Benchmark Dataset](https://github.com/ehs9nino/traffic-ocr-llm-benchmark)  
**🆔 DOI:** [10.5281/zenodo.17392715](https://doi.org/10.5281/zenodo.17392715)



---

## ⚙️ System Overview

This project implements a complete **OCR → LLM → JSON extraction** workflow with a Flask web interface, MongoDB integration, and local or cloud-based inference options.

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
| LLM (API) | `mistralai/Mistral-Small-3.1-24B-Instruct-2503` via [Hugging Face Inference API](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) |
| LLM (Local) | [llama.cpp](https://github.com/ggerganov/llama.cpp) integration via `llama-cpp-python` |
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

### 3. Configure .env

Create a .env file in the root directory.

**⚙️ Option A – Using APIs (Recommended)**
```bash
HF_TOKEN=your_huggingface_token
MONGO_URI=your_mongodb_atlas_connection_uri
```

**⚙️ Option B – Fully Local Mode**
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

1. Upload a **Rate Confirmation** or **CDL** document.  
2. Extracted fields appear in editable form.  
3. Click **Save to Database** → stored in **MongoDB**.  
4. Use the **Admin View** (top-right) to browse, download, or delete records.

---

### 🧪 Evaluation

The evaluation scripts reproduce the paper’s results:

| Directory | Purpose |
|------------|----------|
| `OCR_Evaluation/` | Tesseract vs PaddleOCR speed & accuracy comparisons |
| `LLM_Evaluations/` | Structured extraction performance across Mistral, Phi and LLaMA models |

---
### 📊 Example Output

Example structured JSON output:

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

### 📦 Citation

If you use this code or dataset, please cite:

> Qader, E., Efremenko, D., & Derkach, D. (2025).  
> **Traffic Document Processing with Large Language Models: A Benchmark for Information Extraction from Noisy OCR.**  
> *PeerJ Computer Science.*  
> DOI: [10.5281/zenodo.17392715](https://doi.org/10.5281/zenodo.17392715)

---

### 📜 License

This repository is released under the **MIT License**.  
The accompanying dataset is licensed separately under **CC-BY-4.0**.

---

### 💡 Notes for Reviewers

- The code automatically detects when the Hugging Face provider is unavailable and falls back to **local inference** (`llama.cpp`).  
- The `.env` file must include **valid API tokens** or a running **local MongoDB** instance.  
- All external dependencies are lightweight and specified in `requirements.txt`.  
- Example screenshots, OCR outputs, and evaluation notebooks are included for reproducibility.

---

**Maintained by:** [Ehsan Qader](https://github.com/ehs9nino)  
📧 **Contact:** [eqader@hse.ru](mailto:eqader@hse.ru)
