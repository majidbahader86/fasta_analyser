# app.py
import os
import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from src.parser import parse_fasta
from datetime import datetime

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
ALLOWED_EXT = {"fasta", "fa", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        if "fasta_file" not in request.files:
            error = "No file part"
            return render_template("index.html", error=error)
        f = request.files["fasta_file"]
        if f.filename == "":
            error = "No file selected"
            return render_template("index.html", error=error)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            saved = os.path.join(app.config["UPLOAD_FOLDER"], f"{ts}_{filename}")
            f.save(saved)

            # parse and optionally do NCBI lookup if env var set
            do_ncbi = os.environ.get("ENTREZ_EMAIL", "") != ""
            df = parse_fasta(saved, do_ncbi_lookup=do_ncbi)

            # save result CSV
            result_name = f"result_{ts}.csv"
            result_path = os.path.join(app.config["RESULT_FOLDER"], result_name)
            df.to_csv(result_path, index=False)

            table_html = df.to_html(classes="table table-striped table-sm", index=False, escape=False)
            return render_template("result.html", table=table_html, download_url=url_for("download_result", filename=result_name))
        else:
            error = "Unsupported file type. Use .fasta or .fa"
    return render_template("index.html", error=error)

@app.route("/download/<path:filename>")
def download_result(filename):
    return send_from_directory(app.config["RESULT_FOLDER"], filename, as_attachment=True)

# Programmatic API: POST file and get JSON metadata back
@app.route("/api/parse", methods=["POST"])
def api_parse():
    if "fasta_file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400
    f = request.files["fasta_file"]
    if f.filename == "" or not allowed_file(f.filename):
        return jsonify({"error": "invalid file"}), 400
    filename = secure_filename(f.filename)
    saved = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(saved)
    do_ncbi = os.environ.get("ENTREZ_EMAIL", "") != ""
    df = parse_fasta(saved, do_ncbi_lookup=do_ncbi)
    return jsonify({"rows": df.to_dict(orient="records")})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
