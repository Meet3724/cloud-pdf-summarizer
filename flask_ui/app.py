from flask import Flask, render_template, request
from google.cloud import storage, pubsub_v1
import os
import json

app = Flask(__name__)

# Configuration
BUCKET_NAME = 'cps-bucket'
PROJECT_ID = 'solar-bolt-464117-t2'
TOPIC_ID = 'cps-topic'
TOPIC_PATH = f'projects/{PROJECT_ID}/topics/{TOPIC_ID}'

# Optional: Only set this if running locally and you have the file
if os.path.exists('gcs-key.json'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcs-key.json'

# Initialize GCP clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

def get_unique_filename(bucket, original_name):
    """Ensure filename is unique in GCS by appending (1), (2), ... if needed."""
    base, ext = os.path.splitext(original_name)
    candidate = original_name
    counter = 1

    while bucket.blob(candidate).exists():
        candidate = f"{base}({counter}){ext}"
        counter += 1

    return candidate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return render_template('index.html', message="❌ No file part in form.")

    file = request.files['pdf_file']
    if file.filename == '':
        return render_template('index.html', message="❌ No file selected.")

    if file and file.filename.endswith('.pdf'):
        bucket = storage_client.bucket(BUCKET_NAME)
        unique_filename = get_unique_filename(bucket, file.filename)
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file)

        # Publish message to Pub/Sub
        message_data = json.dumps({'filename': unique_filename}).encode("utf-8")
        publisher.publish(TOPIC_PATH, data=message_data)
        print(f"📨 Published to Pub/Sub: {unique_filename}")

        return render_template('index.html', message=f"✅ Uploaded and triggered summary for: {unique_filename}")
    else:
        return render_template('index.html', message="❌ Only PDF files are allowed.")

@app.route('/summarize', methods=['POST'])
def summarize():
    return render_template('index.html', message="🧠 Summary triggered manually (demo)")

if __name__ == '__main__':
    app.run(debug=True)
