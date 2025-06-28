import fitz  # PyMuPDF
from transformers import pipeline
from google.cloud import firestore, storage
import os

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
db = firestore.Client()
storage_client = storage.Client()

def summarize_pdf(data, context):
    bucket_name = data['bucket']
    file_name = data['name']

    if not file_name.endswith('.pdf'):
        print("❌ Not a PDF. Skipping.")
        return

    # Download PDF
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    temp_path = f"/tmp/{file_name}"
    blob.download_to_filename(temp_path)

    # Extract text
    text = ""
    with fitz.open(temp_path) as doc:
        for page in doc:
            text += page.get_text()

    if not text.strip():
        print("❌ No text extracted.")
        return

    # Summarize
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = " ".join(summarizer(chunk)[0]['summary_text'] for chunk in chunks)

    # Save to Firestore
    db.collection("summaries").document(file_name).set({"summary": summary})
    print(f"✅ Summary stored for {file_name}")
