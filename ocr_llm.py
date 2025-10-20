# ocr_llm.py
from __future__ import annotations

import os
import re
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from paddleocr import PaddleOCR
from huggingface_hub import InferenceClient
from llama_cpp import Llama

# ----------------------------
# Env & config
# ----------------------------
load_dotenv()

# BACKEND: "hf" or "local"
BACKEND = os.getenv("BACKEND", "hf").lower()
# HF settings
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-Small-3.1-24B-Instruct-2503")
HF_PROVIDER = os.getenv("HF_PROVIDER", "nebius")  # e.g., "nebius", "aws", "hf"
# Local model settings
MODEL_PATHS = {
    "mistral": "models/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-IQ3_M.gguf",
    "llama":   "models/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q8_0.gguf",
    "phi":     "models/Phi-3.1-mini-4k-instruct-GGUF/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf",
}
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "mistral").lower()

# ----------------------------
# Initialize engines once
# ----------------------------
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# HF client (only if token present)
_hf_client = None
if HF_TOKEN:
    _hf_client = InferenceClient(provider=HF_PROVIDER, api_key=HF_TOKEN)

_llm_cache: dict[str, Llama] = {}


def _get_local_llm(name: str) -> Llama:
    """Lazy-load and cache a local llama.cpp model."""
    name = name.lower()
    if name not in MODEL_PATHS:
        raise ValueError(f"Unknown local model '{name}'. Choose from {list(MODEL_PATHS)}.")
    if name not in _llm_cache:
        _llm_cache[name] = Llama(
            model_path=MODEL_PATHS[name],
            n_gpu_layers=-1,
            n_ctx=2048,
            n_threads=os.cpu_count() or 4,
            n_batch=128,      # drop to 64 if VRAM is tight
            verbose=False,
        )
    return _llm_cache[name]


def _json_from_text(text: str) -> str:
    """Extract a JSON object from text; always return a pretty JSON string."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return '{"error": "No JSON block found in model response."}'
    s = m.group(0)
    try:
        return json.dumps(json.loads(s), ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return '{"error": "Failed to parse JSON from model output."}'


# ----------------------------
# Public API
# ----------------------------
def run_ocr(image_path: str) -> str:
    """Perform OCR using PaddleOCR and return plain text."""
    t0 = time.time()
    result = ocr.ocr(image_path, cls=True)
    print(f"\n🕒 OCR Time: {time.time() - t0:.2f} seconds")
    lines = [line[1][0] for line in (result[0] or [])]
    return "\n".join(lines).strip()


def load_prompt_template(doc_type: str) -> str:
    """Load a predefined prompt template for a given document type."""
    prompt_dir = Path("prompts")
    filename = "rate_prompt.txt" if doc_type == "rate" else "cdl_prompt.txt"
    path = prompt_dir / filename
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_prompt(ocr_text: str, doc_type: str = "cdl") -> str:
    """Combine OCR text with the predefined prompt."""
    return load_prompt_template(doc_type).replace("{TEXT}", ocr_text).strip()


def run_llm(full_prompt: str) -> str:
    """
    Unified LLM call. Picks backend via .env:
      BACKEND=hf     → Hugging Face Inference API
      BACKEND=local  → local llama.cpp (GGUF)
    Falls back to the other backend if the primary fails.
    Returns a pretty JSON string (or an error JSON).
    """
    def _call_hf() -> str:
        if not _hf_client:
            raise RuntimeError("HF_TOKEN not set")
        t0 = time.time()
        completion = _hf_client.chat.completions.create(
            model=HF_MODEL,
            messages=[{"role": "user", "content": full_prompt}],
        )
        print(f"\n🕒 LLM Inference Time (HF): {time.time() - t0:.2f} seconds")
        raw = completion.choices[0].message.content.strip()
        return _json_from_text(raw)

    def _call_local() -> str:
        llm = _get_local_llm(LOCAL_MODEL)
        t0 = time.time()
        out = llm(
            full_prompt,
            max_tokens=512,
            temperature=0.0,
            top_p=1.0,
            stop=["</s>"],
        )
        print(f"\n🕒 LLM Inference Time (local:{LOCAL_MODEL}): {time.time() - t0:.2f} seconds")
        raw = out["choices"][0]["text"].strip()
        return _json_from_text(raw)

    try:
        if BACKEND == "local":
            try:
                return _call_local()
            except Exception as e_local:
                print(f"[WARN] Local LLM failed: {e_local}. Falling back to HF…")
                return _call_hf()
        else:  # default 'hf'
            try:
                return _call_hf()
            except Exception as e_hf:
                print(f"[WARN] HF API failed: {e_hf}. Falling back to local…")
                return _call_local()
    except Exception as e:
        print(f"[ERROR] {e}")
        return '{"error": "Both backends failed."}'
