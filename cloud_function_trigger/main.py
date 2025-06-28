import base64
import json
from google.cloud import pubsub_v1
import os

PROJECT_ID = os.environ.get("PROJECT_ID", "solar-bolt-464117-t2")
TOPIC_ID = os.environ.get("TOPIC_ID", "cps-topic")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def notify_pdf_upload(event, context):
    file = event
    if not file['name'].endswith('.pdf'):
        print("Not a PDF file. Ignoring.")
        return

    message_json = json.dumps({"filename": file["name"]})
    message_bytes = message_json.encode("utf-8")
    
    publisher.publish(topic_path, data=message_bytes)
    print(f"✅ Published message for file: {file['name']}")
