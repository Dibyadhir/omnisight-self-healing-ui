"""
OmniSight - Week 1, Part B: Webhook Test Script
--------------------------------------------------
Simulates a CI/CD system (like GitHub Actions) sending a build-completed
event to your FastAPI webhook receiver.

Make sure main.py is already running:
    python -m uvicorn main:app --reload
before you run this script.

Run with:
    python send_test_webhook.py
"""

import requests

WEBHOOK_URL = "http://127.0.0.1:8000/webhook/ci"

# This mimics the JSON payload a real CI/CD system would POST to your
# server after a build finishes.
fake_payload = {
    "branch": "feature/checkout-fix",
    "commit": "a1b2c3d4",
    "status": "success",
    "repository": "omnisight-self-healing-ui",
    "staging_url": "https://staging.example.com",
}

response = requests.post(WEBHOOK_URL, json=fake_payload)

print("Status code:", response.status_code)
print("Response body:", response.json())