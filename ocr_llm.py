# ocr_llm.py

from paddleocr import PaddleOCR
import os
import re
import json
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Initialize PaddleOCR  
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Hugging Face Inference API Setup
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    provider="nebius",  # You can also test with 'aws' or 'hf'
    api_key=HF_TOKEN,
)

def run_ocr(image_path):
    """
    Perform OCR using PaddleOCR and return plain text.
    """
    start_time = time.time()
    result = ocr.ocr(image_path, cls=True)
    elapsed = time.time() - start_time
    print(f"\n🕒 OCR Time: {elapsed:.2f} seconds")

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
    """
    Send the prompt to the Hugging Face-hosted Mistral model
    and extract structured fields as JSON.
    """
    try:
        start_time = time.time()

        completion = client.chat.completions.create(
            model="mistralai/Mistral-Small-3.1-24B-Instruct-2503",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )

        elapsed = time.time() - start_time
        print(f"\n🕒 LLM Inference Time: {elapsed:.2f} seconds")

        raw_text = completion.choices[0].message.content.strip()

        # Attempt to extract JSON
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            try:
                return json.dumps(json.loads(match.group(0)), indent=2)
            except json.JSONDecodeError:
                return '{"error": "Failed to parse JSON from model output."}'
        else:
            return '{"error": "No JSON block found in model response."}'

    except Exception as e:
        print(f"[ERROR] {e}")
        return '{"error": "Hugging Face API request failed."}'
