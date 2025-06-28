# 📄 Cloud PDF Summarizer using Google Cloud Platform 🚀

This project is a cloud-based application that summarizes uploaded PDF documents using HuggingFace Transformers and stores the summaries in Firestore. It uses an event-driven architecture leveraging several GCP services.

## ✅ Objective

Automatically summarize PDF files uploaded to a Cloud Storage bucket, using an AI model, and save the summary to Firestore for quick access.

---

## 🏗️ Architecture Overview

**Cloud Services Used:**
- **Cloud Storage** – Stores uploaded PDF files.
- **Cloud Functions** – Triggered when a new PDF is uploaded to the bucket; it publishes a message to a Pub/Sub topic.
- **Cloud Pub/Sub** – Carries filename messages from the function to the summarizer service.
- **Cloud Run** – Runs a Python Flask app that:
  - Downloads the PDF from Cloud Storage.
  - Extracts the text using `PyMuPDF`.
  - Summarizes it using a HuggingFace transformer.
  - Stores the output summary in **Firestore**.

---

## 🔁 Workflow

[User Uploads PDF]
↓
[Cloud Function Trigger (GCS)]
↓
[Publishes filename to Pub/Sub]
↓
[Cloud Run Service picks message]
↓
[Downloads PDF, extracts text, summarizes]
↓
[Saves to Firestore]

---

## 📁 Project Structure

cloud-pdf-summarizer/
├── cloud_function_trigger/
│ ├── main.py # Publishes filename to Pub/Sub
│ ├── requirements.txt
│
├── cloud_run_service/
│ ├── main.py # Summarizes PDF and stores summary
│ ├── requirements.txt
│ ├── Dockerfile
│
├── README.md
├── .gitignore

---

## 🚀 Deployment Steps

### 1. Deploy the Cloud Function (GCS → Pub/Sub)

gcloud functions deploy notify-pdf-upload \
  --runtime python310 \
  --trigger-resource cps-bucket \
  --trigger-event google.storage.object.finalize \
  --set-env-vars PROJECT_ID=solar-bolt-464117-t2,TOPIC_ID=cps-topic \
  --region asia-south1 \
  --entry-point notify_pdf_upload \
  --project solar-bolt-464117-t2

### 2. Deploy Cloud Run (Summarizer Service)

cd cloud_run_service
gcloud run deploy summarize-service \
  --source . \
  --region asia-south1 \
  --project solar-bolt-464117-t2 \
  --memory 1Gi \
  --timeout 540s \
  --set-env-vars PROJECT_ID=solar-bolt-464117-t2,BUCKET_NAME=cps-bucket

### 🧪 Example Firestore Output
Collection: summaries
{
  "filename": "example.pdf",
  "summary": "This document discusses the key concepts of..."
}

### 📦 Tech Stack

Python 3.10
Flask
HuggingFace Transformers (DistilBART)
PyMuPDF (fitz)
Google Cloud Storage
Pub/Sub
Firestore
Cloud Functions
Cloud Run

### 🧑‍🎓 Author
Meet Jaywant Nachanekar
SY EXCS Engineering Student
CDAC Cloud Computing Project (June 2025)
