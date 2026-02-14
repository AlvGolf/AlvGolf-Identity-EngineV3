"""
Test script for Analytics Pro Agent endpoint.
"""

import requests
import json

API_BASE = "http://localhost:8000"
USER_ID = "alvaro"

print("="*60)
print("Testing AlvGolf Analytics Pro Agent")
print("="*60)

payload = {
    "user_id": USER_ID
}

print(f"\n[USER ID] {USER_ID}\n")
print("[INFO] Requesting full analysis from Analytics Pro Agent...")
print("[INFO] This may take 30-60 seconds...\n")

try:
    response = requests.post(
        f"{API_BASE}/analyze",
        json=payload,
        timeout=90
    )
    response.raise_for_status()

    result = response.json()

    print("\n" + "="*60)
    print("ANALYTICS PRO AGENT - FULL ANALYSIS")
    print("="*60 + "\n")

    print(result["analysis"])

    print("\n" + "="*60)
    print(f"Generated at: {result['generated_at']}")
    print("="*60)
    print("\n[OK] Analysis complete!")

except Exception as e:
    print(f"[ERROR] {e}")

print("="*60)
