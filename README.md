# 📄 Cloud PDF Summarizer using GCP and Flask

A serverless cloud-based application that **automatically summarizes PDF files** using Google Cloud services and displays the summary on a Flask web interface.

---

## 🚀 Project Overview

This project allows users to upload PDF files via a simple **Flask web app**. Once uploaded, the file is stored in **Google Cloud Storage**, and a message is published to **Google Cloud Pub/Sub**.  
A background listener running on a **Compute Engine VM** listens to these messages, extracts the text from the PDF using `PyMuPDF`, and summarizes it using **HuggingFace Transformers**. The final summary is sent back to the Flask app UI for display.

---

## 🧩 Tech Stack and Cloud Services Used

| Technology                | Purpose                                                         |
|---------------------------|-----------------------------------------------------------------|
| **Flask**                 | Frontend interface to upload PDF and view summary               |
| **Google Cloud Storage**  | Store uploaded PDF files securely in the cloud                  |
| **Google Pub/Sub**        | Trigger summarization pipeline when PDF is uploaded             |
| **Google Compute Engine** | VM runs  script for extraction & summarization                  |
| **Google Cloud Run**      |  To run summarization microservice (serverless)                 |
| **VS Code**               | Used for project development                                    |

---

## 🧠 Summary Generation Flow Diagram

graph TD
A[User uploads PDF via Flask UI] --> B[File uploaded to Cloud Storage (GCS)]
B --> C[Pub/Sub topic triggered]
C --> D[Compute Engine VM listener receives message]
D --> E[Extracts text using PyMuPDF]
E --> F[Summarizes text using Pegasus model (HuggingFace)]
F --> G[Prints summary to VM terminal (SSH)]

---

## 🖥️ Screenshots

✅ Flask UI
![Flask UI](<Screenshot 2025-06-28 213544.png>)

✅ Visual Studio Code Project Setup
![Visual Studio Code Project Setup](<Screenshot 2025-06-28 213607.png>)

✅ Cloud Storage Bucket
![Cloud Storage Bucket](<Screenshot 2025-06-28 213632.png>)

✅ Pub/Sub Topic and Subscription
![Pub/Sub Topic and Subscription](<Screenshot 2025-06-28 213811.png>)

✅ Compute Engine VM Running 
![Compute Engine VM Running](<Screenshot 2025-06-28 214239.png>)

✅ Cloud Run Deployment
![Cloud Run Deployment](<Screenshot 2025-06-28 214001.png>)

---

## 🧪 Sample Summary Output
Example of a summarized PDF:
Input PDF: Detailed_Cloud_Handout.pdf
Generated Summary:
- IaaS (Infrastructure as a Service): Offers virtualized computing resources.
- Benefits: Scalability, global reach.
- Hands-on: GCP Compute Engine to spin up virtual machines.

---

## ⚙️ Setup Instructions

✅ Prerequisites
Python 3.9+
pip and virtualenv
GCP project with the following enabled:
  1. Cloud Storage
  2. Pub/Sub
  3. Compute Engine
  4. Cloud Run

✅ Setup
### Clone repo and set up virtualenv
git clone https://github.com/Meet3724/cloud-pdf-summarizer.git 
cd cloud-pdf-summarizer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

### Install dependencies

pip install -r requirements.txt
✅ Flask Web App
cd flask_ui
python app.py
The app will be live at http://localhost:5000

✅ VM Listener Script
Deploy summarize_pdf.py on a Compute Engine VM.
Make sure it has access to GCS and Pub/Sub.
Install required packages (transformers, PyMuPDF, torch, etc.)
Run the listener with:
python summarize_pdf.py

--- 

### 🧠 Model Used
Model: google/pegasus-xsum (via HuggingFace Transformers)
Library: transformers + torch
Text Extraction: PyMuPDF

--- 

### 🧾 Credits
Meet Jaywant Nachanekar
SY EXCS Engineering Student
Developed as part of the Cloud Computing course project using real-world cloud tools and architecture!
