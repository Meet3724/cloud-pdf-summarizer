import requests

# ✅ Replace with your actual Cloud Run URL
CLOUD_RUN_URL = "https://summarize-service-711853958035.asia-south1.run.app"

def trigger_summary(filename):
    try:
        payload = {"filename": filename}
        print(f"📤 Sending payload to Cloud Run: {payload}")
        response = requests.post(CLOUD_RUN_URL, json=payload)
        print(f"✅ Cloud Run responded with status: {response.status_code}")
        print("📄 Response body:", response.text)
    except Exception as e:
        print(f"❌ Error triggering Cloud Run: {e}")

if __name__ == "__main__":
    filename = input("📂 Enter the PDF filename in bucket (e.g., sample.pdf): ")
    trigger_summary(filename)
