# flask_ui/app.py
from flask import Flask, render_template, request, redirect, flash
from google.cloud import storage, pubsub_v1, firestore
import os
import json

app = Flask(__name__)
app.secret_key = 'secret123'

# Constants
BUCKET_NAME = "cps-bucket"
TOPIC_ID = "cps-topic"
PROJECT_ID = "solar-bolt-464117-t2"

# Clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
firestore_client = firestore.Client()

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['pdf']
        if file.filename == '' or not file.filename.endswith('.pdf'):
            flash('❌ Please upload a valid PDF file.')
            return redirect('/')

        # Upload to GCS
        try:
            blob = storage_client.bucket(BUCKET_NAME).blob(file.filename)
            blob.upload_from_file(file, content_type='application/pdf')
            print(f"📁 Uploaded {file.filename} to bucket.")
        except Exception as e:
            print(f"❌ Failed to upload PDF: {e}")
            flash("❌ Failed to upload PDF to Cloud Storage.")
            return redirect('/')

        # Publish to Pub/Sub
        try:
            message = json.dumps({"filename": file.filename}).encode("utf-8")
            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
            future = publisher.publish(topic_path, message)
            message_id = future.result()
            print(f"📡 Published message to Pub/Sub: {message_id}")
            flash('✅ PDF uploaded and Pub/Sub message sent.')
        except Exception as e:
            print(f"❌ Failed to publish Pub/Sub message: {e}")
            flash("❌ Failed to publish message to Pub/Sub.")
            return redirect('/')

        return redirect(f'/summary/{file.filename}')

    return render_template('index.html')

@app.route('/summary/<filename>')
def summary(filename):
    try:
        doc = firestore_client.collection("summaries").document(filename).get()
        if doc.exists:
            return render_template('index.html', summary=doc.to_dict().get('summary'))
        else:
            flash("⏳ Summary not ready. Please try again in a moment.")
            return redirect('/')
    except Exception as e:
        print(f"❌ Firestore error: {e}")
        flash("❌ Could not retrieve summary.")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
