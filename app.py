from flask import Flask, request, jsonify, render_template, redirect, send_file, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
import os
from ocr_llm import run_ocr, generate_prompt, run_llm
from db import save_document, collection
from bson import ObjectId
import io
import json



app = Flask(__name__)
app.secret_key = "tms"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)




@app.route("/", methods=["GET", "POST"])
def index():
    result_dict = None
    image_url = None

    if request.method == "POST":
        file = request.files["file"]
        doc_type = request.form["doc_type"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # OCR + LLM
        ocr_text = run_ocr(filepath)
        prompt = generate_prompt(ocr_text, doc_type)
        result = run_llm(prompt)

        try:
            result_dict = json.loads(result)
        except Exception:
            result_dict = {"error": "Failed to parse result"}

        image_url = url_for("uploaded_file", filename=filename)

    return render_template("index.html", result_dict=result_dict, image_url=image_url)






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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



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


"""
@app.route("/save", methods=["POST"])
def save_from_ui():
    try:
        data = dict(request.form)
        data.pop("image_path", None)
        doc_id = save_document(data)
        return redirect("/admin")
    except Exception as e:
        return f"Save failed: {str(e)}", 500

"""
    

    
@app.route("/save", methods=["POST"])
def save_from_ui():
    try:
        data = dict(request.form)
        data.pop("image_path", None)
        save_document(data)
        flash("Document saved successfully!", "success")
    except Exception as e:
        flash(f"Save failed: {e}", "danger")
    return redirect("/")




@app.route("/history", methods=["GET"])
def get_history():
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for JSON
    return jsonify(docs)


@app.route("/admin")
def admin_view():
    all_docs = list(collection.find().sort("_id", -1).limit(20))
    for doc in all_docs:
        doc["_id"] = str(doc["_id"])

    rate_docs = [doc for doc in all_docs if "Load Number" in doc]
    cdl_docs = [doc for doc in all_docs if "License Number" in doc]

    return render_template("admin.html", rate_docs=rate_docs, cdl_docs=cdl_docs)


@app.route("/delete/<doc_id>")
def delete_doc(doc_id):
    collection.delete_one({"_id": ObjectId(doc_id)})
    flash("Document deleted.", "warning")
    return redirect("/admin")

@app.route("/download/<doc_id>")
def download_doc(doc_id):
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return "Not Found", 404
    doc["_id"] = str(doc["_id"])
    return send_file(
        io.BytesIO(json.dumps(doc, indent=2).encode("utf-8")),
        as_attachment=True,
        download_name=f"{doc.get('Load Number', doc.get('Full Name', 'document'))}.json",
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)
