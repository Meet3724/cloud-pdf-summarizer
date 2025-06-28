from flask import Flask, request, jsonify
from google.cloud import storage, firestore
from transformers import pipeline
import fitz  # PyMuPDF
import os

app = Flask(__name__)

# Clients
storage_client = storage.Client()
firestore_client = firestore.Client()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

BUCKET_NAME = "cps-bucket"

@app.route("/", methods=["POST"])
def summarize_pdf():
    try:
        data = request.get_json()
        filename = data["filename"]
        print(f"📥 Received filename: {filename}")

        # Read PDF from GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        pdf_bytes = blob.download_as_bytes()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()
        text = text[:3000]  # limit for summarization model

        print("🧠 Summarizing text...")
        result = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

        # Save to Firestore
        firestore_client.collection("summaries").document(filename).set({
            "summary": result
        })
        print("✅ Summary stored in Firestore")
        return jsonify({"status": "success", "summary": result})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

