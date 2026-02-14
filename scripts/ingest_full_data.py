"""
AlvGolf - Script de Ingesta Completa

Convierte TODOS los datos relevantes de dashboard_data.json a vectores Pinecone.
Incluye: clubs, rounds, HCP, courses, strokes gained, momentum, etc.
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime


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


def convert_club_statistics(data):
    """Convert club statistics to shots"""
    shots = []
    club_stats = data.get("club_statistics", [])

    print(f"[INFO] Converting {len(club_stats)} clubs...")

    for club in club_stats:
        shot = {
            "date": "2025-12-31",
            "source": "club_statistics",
            "club": club.get("name", "Unknown"),
            "hole": 0,
            "ball_speed": float(club.get("speed_raw", 0)) if club.get("speed_raw") else 0,
            "carry": float(club.get("distance_raw", 0)) if club.get("distance_raw") else 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": 0,
            "notes": f"Club stats: {club.get('distance', 'N/A')}, Rating {club.get('rating', 0)}/5, Smash {club.get('smash_factor_est', 0)}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} club shot records")
    return shots


def convert_best_worst_rounds(data):
    """Convert best/worst rounds to detailed shots"""
    shots = []
    bwr = data.get("best_worst_rounds", {})

    # Best rounds
    best_rounds = bwr.get("best_rounds", [])
    print(f"[INFO] Converting {len(best_rounds)} best rounds...")

    for round_data in best_rounds:
        shot = {
            "date": round_data.get("date", "2025-01-01"),
            "source": "best_round",
            "club": "Course",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": round_data.get("score", 0),
            "notes": f"Best round at {round_data.get('course', 'Unknown')}: Score {round_data.get('score')}, Differential {round_data.get('differential')}, Par {round_data.get('par')}, Front 9: {round_data.get('total_ida')}, Back 9: {round_data.get('total_vuelta')}"
        }
        shots.append(shot)

    # Worst rounds
    worst_rounds = bwr.get("worst_rounds", [])
    print(f"[INFO] Converting {len(worst_rounds)} worst rounds...")

    for round_data in worst_rounds:
        shot = {
            "date": round_data.get("date", "2025-01-01"),
            "source": "worst_round",
            "club": "Course",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": round_data.get("score", 0),
            "notes": f"Worst round at {round_data.get('course', 'Unknown')}: Score {round_data.get('score')}, Differential {round_data.get('differential')}, Par {round_data.get('par')}, Front 9: {round_data.get('total_ida')}, Back 9: {round_data.get('total_vuelta')}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} round records")
    return shots


def convert_hcp_evolution(data):
    """Convert HCP evolution to shots"""
    shots = []
    hcp_data = data.get("hcp_evolution_rfeg", {})

    labels = hcp_data.get("labels", [])
    values = hcp_data.get("values", [])
    source = hcp_data.get("source", "unknown")

    print(f"[INFO] Converting {len(labels)} HCP data points ({source})...")

    for i, (date, hcp) in enumerate(zip(labels, values)):
        # Calculate improvement from start
        improvement = values[0] - hcp if i > 0 else 0

        shot = {
            "date": date,
            "source": f"hcp_evolution_{source}",
            "club": "HCP",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": 0,
            "notes": f"Official RFEG Handicap: {hcp:.1f}, Improvement from start: {improvement:.1f}, Source: {source}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} HCP records")
    return shots


def convert_campo_performance(data):
    """Convert course performance to shots"""
    shots = []
    campo_data = data.get("campo_performance", {})

    print(f"[INFO] Converting {len(campo_data)} courses...")

    for course_name, stats in campo_data.items():
        shot = {
            "date": "2025-12-31",
            "source": "course_performance",
            "club": "Course",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": stats.get("average", 0),
            "notes": f"Course: {course_name}, Best: {stats.get('best')}, Average: {stats.get('average'):.1f}, Worst: {stats.get('worst')}, Rounds: {stats.get('rounds')}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} course records")
    return shots


def convert_momentum_indicators(data):
    """Convert momentum indicators (52 rounds)"""
    shots = []
    momentum_data = data.get("momentum_indicators", [])

    print(f"[INFO] Converting {len(momentum_data)} momentum records...")

    for record in momentum_data:
        shot = {
            "date": record.get("date", "2025-01-01"),
            "source": "momentum",
            "club": "Performance",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": record.get("score", 0),
            "notes": f"Score: {record.get('score')}, SMA-5: {record.get('sma_5', 0):.1f}, Momentum: {record.get('momentum', 0):.2f}, Direction: {record.get('direction', 'stable')}, Acceleration: {record.get('acceleration', 0):.2f}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} momentum records")
    return shots


def convert_quarterly_scoring(data):
    """Convert quarterly scoring data"""
    shots = []
    quarterly_data = data.get("quarterly_scoring", {})

    print(f"[INFO] Converting {len(quarterly_data)} quarters...")

    for quarter, stats in quarterly_data.items():
        shot = {
            "date": f"2025-{quarter}",
            "source": "quarterly_scoring",
            "club": "Quarter",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": stats.get("avg_score", 0),
            "notes": f"Quarter {quarter}: Avg {stats.get('avg_score', 0):.1f}, Rounds {stats.get('rounds')}, Best {stats.get('best')}, Worst {stats.get('worst')}, Trend: {stats.get('trend', 'N/A')}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} quarterly records")
    return shots


def convert_strokes_gained(data):
    """Convert strokes gained analysis"""
    shots = []
    sg_data = data.get("strokes_gained", {})

    categories = sg_data.get("categories", [])
    total_sg = sg_data.get("total_sg", 0)

    print(f"[INFO] Converting {len(categories)} strokes gained categories...")

    for cat in categories:
        shot = {
            "date": "2025-12-31",
            "source": "strokes_gained",
            "club": "Analysis",
            "hole": 0,
            "ball_speed": 0,
            "carry": 0,
            "launch_angle": 0,
            "face_to_path": 0,
            "score": 0,
            "notes": f"Strokes Gained - {cat.get('category')}: {cat.get('strokes_gained'):.1f}, Player avg {cat.get('player_avg'):.1f} vs HCP15 {cat.get('hcp15_benchmark'):.1f}, Percentile {cat.get('percentile')}%, Rating: {cat.get('rating')}"
        }
        shots.append(shot)

    print(f"[OK] Created {len(shots)} strokes gained records")
    return shots


def ingest_to_api(shots):
    """Send all shots to /ingest endpoint"""
    url = f"{API_BASE}/ingest"
    payload = {
        "user_id": USER_ID,
        "shots": shots
    }

    print(f"\n[INFO] Sending {len(shots)} total shots to API...")
    print(f"[INFO] URL: {url}")

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        print(f"\n[OK] Ingestion successful!")
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
    print("="*70)
    print("AlvGolf - FULL Data Ingestion (Expanded Dataset)")
    print("="*70)

    # Step 1: Load data
    data = load_dashboard_data()

    # Step 2: Convert all data sources
    all_shots = []

    print("\n" + "="*70)
    print("CONVERTING DATA SOURCES")
    print("="*70)

    all_shots.extend(convert_club_statistics(data))
    all_shots.extend(convert_best_worst_rounds(data))
    all_shots.extend(convert_hcp_evolution(data))
    all_shots.extend(convert_campo_performance(data))
    all_shots.extend(convert_momentum_indicators(data))
    all_shots.extend(convert_quarterly_scoring(data))
    all_shots.extend(convert_strokes_gained(data))

    print("\n" + "="*70)
    print(f"TOTAL SHOTS CONVERTED: {len(all_shots)}")
    print("="*70)

    # Breakdown by source
    sources = {}
    for shot in all_shots:
        src = shot["source"]
        sources[src] = sources.get(src, 0) + 1

    print("\nBreakdown by source:")
    for src, count in sorted(sources.items()):
        print(f"  - {src}: {count} records")

    # Step 3: Ingest to API
    result = ingest_to_api(all_shots)

    print("\n" + "="*70)
    print("[SUCCESS] Full data ingestion complete!")
    print("="*70)
    print("\nDataset Summary:")
    print(f"  - Total vectors: {len(all_shots)}")
    print(f"  - Data sources: {len(sources)}")
    print(f"  - User ID: {USER_ID}")
    print(f"  - Pinecone namespace: {USER_ID}")
    print("\nNext steps:")
    print(f"  1. Test Analytics Pro Agent: python scripts/test_analytics_agent.py")
    print(f"  2. Query specific data: python scripts/test_query.py")
    print(f"  3. Verify in dashboard at: http://localhost:8000/docs")
    print("="*70)


if __name__ == "__main__":
    main()
