from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from ocr_llm import run_ocr, generate_prompt, run_llm
from db import save_document, collection


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload-rate", methods=["POST"])
def upload_rate():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    ocr_text = run_ocr(filepath)
    prompt = generate_prompt(ocr_text, doc_type="rate")
    structured = run_llm(prompt)

    return jsonify(structured)


@app.route("/upload-cdl", methods=["POST"])
def upload_cdl():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    ocr_text = run_ocr(filepath)
    prompt = generate_prompt(ocr_text, doc_type="cdl")
    structured = run_llm(prompt)

    return jsonify(structured)



@app.route("/save-result", methods=["POST"])
def save_result():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    doc_id = save_document(data)
    return jsonify({
        "status": "OK",
        "message": "Data saved to MongoDB",
        "id": doc_id
    })


@app.route("/history", methods=["GET"])
def get_history():
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for JSON
    return jsonify(docs)


if __name__ == "__main__":
    app.run(debug=True)
