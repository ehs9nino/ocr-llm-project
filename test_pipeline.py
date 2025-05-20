from ocr_llm import run_ocr, generate_prompt, run_llm

# Path to a sample rate confirmation image
image_path = "test_data/driver4.jpg"  

# Step 1: Run OCR
ocr_text = run_ocr(image_path)
print("\n=== OCR Output ===\n")
print(ocr_text)

# Step 2: Generate prompt
prompt = generate_prompt(ocr_text, doc_type="cdl")
print("\n=== Full Prompt Sent to LLM ===\n")
print(prompt)





import time
...

# Step 3: Run LLM
start = time.time()
response = run_llm(prompt)
end = time.time()

print("\n=== LLM Structured Output ===\n")
print(response)

print(f"\n🕒 LLM Inference Time: {round(end - start, 2)} seconds")
