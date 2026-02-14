"""
AlvGolf - Script de Ingesta Inicial

Convierte dashboard_data.json a vectores Pinecone.
Usa la API /ingest del backend.
"""

import json
import requests
import sys
from pathlib import Path


# Config
API_BASE = "http://localhost:8000"
USER_ID = "alvaro"
JSON_PATH = Path(__file__).parent.parent / "output" / "dashboard_data.json"


def load_dashboard_data():
    """Load dashboard_data.json"""
    print(f"[INFO] Loading data from: {JSON_PATH}")
    
    if not JSON_PATH.exists():
        print(f"[ERROR] File not found: {JSON_PATH}")
        sys.exit(1)
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"[OK] Loaded dashboard data (version: {data.get('metadata', {}).get('version', 'unknown')})")
    return data


def convert_to_shots(data):
    """
    Convert dashboard_data.json to ShotData format.
    
    Since dashboard_data has aggregated club statistics,
    we'll create representative shots for each club.
    """
    shots = []
    
    # Extract club statistics
    club_stats = data.get("club_statistics", [])
    
    print(f"[INFO] Converting {len(club_stats)} clubs to shots...")
    
    for club in club_stats:
        # Create a representative shot for this club
        shot = {
            "date": "2025-12-31",  # Placeholder (aggregated data)
            "source": "dashboard_json",
            "club": club.get("name", "Unknown"),  # Fixed: use "name" not "palo"
            "hole": 0,  # Practice/aggregated
            "ball_speed": float(club.get("speed_raw", 0)) if club.get("speed_raw") else 0,
            "carry": float(club.get("distance_raw", 0)) if club.get("distance_raw") else 0,
            "launch_angle": float(club.get("launch_angle_mean", 0)) if club.get("launch_angle_mean") else 0,
            "face_to_path": 0,  # Not available in current JSON
            "score": 0,
            "notes": f"Aggregated data: Rating {club.get('rating', 0)}/5, Category: {club.get('category', 'N/A')}"
        }
        shots.append(shot)
    
    print(f"[OK] Created {len(shots)} shot records")
    return shots


def ingest_to_api(shots):
    """
    Send shots to /ingest endpoint.
    """
    url = f"{API_BASE}/ingest"
    payload = {
        "user_id": USER_ID,
        "shots": shots
    }
    
    print(f"[INFO] Sending {len(shots)} shots to API...")
    print(f"[INFO] URL: {url}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        print(f"[OK] Ingestion successful!")
        print(f"     Status: {result['status']}")
        print(f"     Chunks ingested: {result['chunks_ingested']}")
        print(f"     Message: {result.get('message', '')}")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to API. Is the server running?")
        print(f"       Try: python -m app.main")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout. API took too long to respond.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error: {e}")
        print(f"       Response: {response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main execution"""
    print("="*60)
    print("AlvGolf - Initial Data Ingestion")
    print("="*60)
    
    # Step 1: Load data
    data = load_dashboard_data()
    
    # Step 2: Convert to shots
    shots = convert_to_shots(data)
    
    # Step 3: Ingest to API
    result = ingest_to_api(shots)
    
    print("="*60)
    print("[SUCCESS] Initial data ingestion complete!")
    print("="*60)
    print("Next steps:")
    print(f"1. Test query endpoint: {API_BASE}/query")
    print(f"2. Test analyze endpoint: {API_BASE}/analyze")
    print(f"3. User ID: {USER_ID}")
    print("="*60)


if __name__ == "__main__":
    main()
