from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage
import os
import uuid

app = Flask(__name__)
BUCKET_NAME = 'cps-bucket'
GCS_CREDENTIALS_JSON = 'gcs-key.json'  # Path to your service account key

# Set credentials (for local dev on VM)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCS_CREDENTIALS_JSON

storage_client = storage.Client()

def get_unique_filename(bucket, original_name):
    """Ensure unique filename in GCS by appending (1), (2), ..."""
    base, ext = os.path.splitext(original_name)
    counter = 1
    new_name = original_name

    blob = bucket.blob(new_name)
    while blob.exists():
        new_name = f"{base}({counter}){ext}"
        blob = bucket.blob(new_name)
        counter += 1

    return new_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return render_template('index.html', message="No file part")

    file = request.files['pdf_file']
    if file.filename == '':
        return render_template('index.html', message="No selected file")

    if file and file.filename.endswith('.pdf'):
        bucket = storage_client.bucket(BUCKET_NAME)
        unique_filename = get_unique_filename(bucket, file.filename)
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file)

        return render_template('index.html', message=f"✅ Uploaded as: {unique_filename}")
    else:
        return render_template('index.html', message="❌ Please upload a PDF file.")

@app.route('/summarize', methods=['POST'])
def summarize():
    return render_template('index.html', message="🧠 Summary triggered (for demo)")

if __name__ == '__main__':
    app.run(debug=True)
