import base64
import json
import os
import fitz  # PyMuPDF
from flask import Flask, request
from google.cloud import storage, firestore
from transformers import pipeline

app = Flask(__name__)

# Initialize summarizer
print("🔄 Initializing summarization model...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
print("✅ Model loaded.")

# Cloud clients
storage_client = storage.Client()
firestore_client = firestore.Client()

# Environment variable
BUCKET_NAME = os.getenv("BUCKET_NAME", "cps-bucket")
print(f"📁 Using bucket: {BUCKET_NAME}")

@app.route("/", methods=["POST"])
def summarize():
    print("📩 Request received.")

    # Parse Pub/Sub envelope
    envelope = request.get_json()
    print("📦 Envelope:", envelope)

    if not envelope or "message" not in envelope:
        print("❌ Invalid Pub/Sub message format.")
        return "Invalid Pub/Sub message", 400

    message = envelope["message"]

    try:
        payload = base64.b64decode(message["data"]).decode("utf-8")
        data = json.loads(payload)
        print("🧾 Decoded Pub/Sub data:", data)
    except Exception as e:
        print("❌ Failed to decode message data:", str(e))
        return "Failed to decode message", 400

    filename = data.get("filename")
    if not filename:
        print("❌ No filename provided in the message.")
        return "Missing filename in message", 400

    try:
        print(f"⬇️ Downloading file from GCS: {filename}")
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        tmp_path = f"/tmp/{filename}"
        blob.download_to_filename(tmp_path)
        print(f"✅ File downloaded to: {tmp_path}")
    except Exception as e:
        print("❌ Error downloading file:", str(e))
        return "Failed to download PDF", 500

    try:
        print("📄 Extracting text from PDF...")
        doc = fitz.open(tmp_path)
        text = ""
        for page in doc:
            text += page.get_text()
        print("✅ Text extracted.")
    except Exception as e:
        print("❌ Error reading PDF:", str(e))
        return "Failed to extract text", 500

    if not text.strip():
        print("⚠️ No text found in the PDF.")
        return "No text found in PDF", 200

    try:
        print("🧠 Generating summary...")
        summary = summarizer(text[:1000], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        print("✅ Summary generated.")
    except Exception as e:
        print("❌ Error during summarization:", str(e))
        return "Summarization failed", 500

    try:
        print("📝 Storing summary to Firestore...")
        firestore_client.collection("summaries").document(filename).set({
            "filename": filename,
            "summary": summary
        })
        print("✅ Summary stored successfully.")
    except Exception as e:
        print("❌ Error storing to Firestore:", str(e))
        return "Failed to store summary", 500

    return "Success", 200


# ✅ For local testing or container startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)
