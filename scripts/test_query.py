"""
Test script for RAG query endpoint.
"""

import requests
import json

API_BASE = "http://localhost:8000"
USER_ID = "alvaro"

print("="*60)
print("Testing AlvGolf RAG Query System")
print("="*60)

# Test query
query = "Cual es mi distancia promedio con el Driver?"

payload = {
    "user_id": USER_ID,
    "prompt": query
}

print(f"\n[QUERY] {query}\n")
print("[INFO] Sending query to API...")

try:
    response = requests.post(
        f"{API_BASE}/query",
        json=payload,
        timeout=30
    )
    response.raise_for_status()

    result = response.json()
    print("\n[ANSWER]")
    print("-" * 60)
    print(result["answer"])
    print("-" * 60)
    print("\n[OK] Query successful!")

except Exception as e:
    print(f"[ERROR] {e}")

print("="*60)
