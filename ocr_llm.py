# ocr_llm.py

from paddleocr import PaddleOCR
from llama_cpp import Llama
import os
import re
import json

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  

# Path to GGUF model file (downloaded via LM Studio)
LLM_MODEL_PATH = "models/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-IQ3_M.gguf"

# Initialize LLaMA model via llama.cpp
llm = Llama(
    model_path=LLM_MODEL_PATH,
    n_ctx=2048,
    n_threads=6,  
    verbose=False
)

def run_ocr(image_path):
    """
    Perform OCR using PaddleOCR and return plain text.
    """
    result = ocr.ocr(image_path, cls=True)
    lines = [line[1][0] for line in result[0]]
    text = "\n".join(lines)
    return text.strip()

def load_prompt_template(doc_type):
    """
    Load a predefined prompt template for a given document type.
    """
    prompt_dir = "prompts"
    filename = "rate_prompt.txt" if doc_type == "rate" else "cdl_prompt.txt"
    path = os.path.join(prompt_dir, filename)
    with open(path, "r") as f:
        return f.read()

def generate_prompt(ocr_text, doc_type="cdl"):
    """
    Combine OCR text with the predefined prompt.
    """
    prompt_template = load_prompt_template(doc_type)
    full_prompt = prompt_template.replace("{TEXT}", ocr_text)
    return full_prompt.strip()



def run_llm(full_prompt):
    response = llm.create_completion(
        prompt=full_prompt,
        max_tokens=512,
        stop=["</s>"]
    )
    raw_text = response["choices"][0]["text"].strip()

    # Attempt to extract JSON using regex
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        try:
            return json.dumps(json.loads(match.group(0)), indent=2)  # Return clean JSON string
        except json.JSONDecodeError:
            return '{"error": "Failed to parse JSON from model output."}'
    else:
        return '{"error": "No JSON block found in model response."}'



"""
def run_llm(full_prompt):
    
    response = llm.create_completion(
        prompt=full_prompt,
        max_tokens=512,
        stop=["</s>"]
    )
    return response["choices"][0]["text"].strip()
"""


