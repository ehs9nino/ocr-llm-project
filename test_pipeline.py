from ocr_llm import run_ocr, generate_prompt
from llama_cpp import Llama
import time
import re  # <-- Required for regex
import os


# Define your models
model_paths = {
    "mistral": "models/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-IQ3_M.gguf",
    "llama": "models/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q8_0.gguf",
    "Phi":"models/Phi-3.1-mini-4k-instruct-GGUF/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf"
}

# Run the local model
def run_local_llm(prompt, model_path):
    print(f"\n🔍 Running local model: {model_path.split('/')[-1]} ...")
    try:
        import os
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,          # use GPU layers if available
            n_ctx=2048,               # bigger context (fixes 512 warning)
            n_threads=os.cpu_count() or 4,
            n_batch=256,              # reduce to 128/64 if you hit OOM
            verbose=False
        )
        output = llm(
            prompt,
            max_tokens=512,
            temperature=0.0,          # more deterministic, fewer glitches
            top_p=1.0,
            stop=["</s>"]
        )
        raw_text = output["choices"][0]["text"].strip()

        # Extract JSON if available
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        return match.group(0) if match else raw_text
    except Exception as e:
        return f"[ERROR] Failed to run model: {e}"


# Run everything
if __name__ == "__main__":
    image_path = "test_data/driver4.jpg"

    # Step 1: OCR
    ocr_text = run_ocr(image_path)
    print("\n=== OCR Output ===\n")
    print(ocr_text)

    # Step 2: Prompt
    prompt = generate_prompt(ocr_text, doc_type="cdl")
    print("\n=== Full Prompt Sent to LLM ===\n")
    print(prompt)

    # Step 3: Run models
    for name, path in model_paths.items():
        print(f"\n🔍 Running model: {name.upper()}")
        start = time.time()
        result = run_local_llm(prompt, path)
        end = time.time()

        print(f"\n=== Output from {name.upper()} ===\n{result}")
        print(f"🕒 {name} Inference Time: {round(end - start, 2)} seconds\n")


"""""
# Step 3: Run LLM
start = time.time()
response = run_llm(prompt)
end = time.time()

print("\n=== LLM Structured Output ===\n")
print(response)

print(f"\n🕒 LLM Inference Time: {round(end - start, 2)} seconds")

"""