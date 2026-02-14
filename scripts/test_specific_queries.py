"""
Test script for specific RAG queries with expanded dataset.
"""

import requests
import json

API_BASE = "http://localhost:8000"
USER_ID = "alvaro"

queries = [
    "¿Cuál ha sido mi evolución de handicap en los últimos meses?",
    "¿En qué campo juego mejor y por qué?",
    "¿Cuáles son mis mejores y peores rondas?",
    "¿Qué dice el análisis de strokes gained sobre mi juego?",
    "¿Cuál es mi score promedio en el último trimestre?",
]

print("="*70)
print("Testing Specific Queries with Expanded Dataset")
print("="*70)

for i, query in enumerate(queries, 1):
    print(f"\n{'='*70}")
    print(f"QUERY {i}/{len(queries)}")
    print(f"{'='*70}")
    print(f"[Q] {query}\n")

    payload = {
        "user_id": USER_ID,
        "prompt": query
    }

    try:
        response = requests.post(
            f"{API_BASE}/query",
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        print(f"[ANSWER]")
        print("-" * 70)
        print(result["answer"])
        print("-" * 70)

    except Exception as e:
        print(f"[ERROR] {e}")

    print()

print("="*70)
print("[OK] All queries completed!")
print("="*70)
