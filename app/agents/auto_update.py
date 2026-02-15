"""
Auto-Update Agent - TIER 3

Agente autónomo que:
1. Detecta qué datos cambiaron
2. Procesa datos (generate_dashboard_data.py)
3. Auto-ingesta a Pinecone (POST /ingest)
4. Notifica usuario
"""

import subprocess
import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime
from loguru import logger

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class AutoUpdateAgent:
    """
    Agente autónomo para actualización de dashboard.
    """

    def __init__(self, api_base="http://localhost:8000", user_id="alvaro"):
        """
        Args:
            api_base: URL base del backend API
            user_id: ID del usuario
        """
        self.api_base = api_base
        self.user_id = user_id
        self.project_root = Path(__file__).parent.parent.parent

        logger.info("[AutoUpdate] Agent initialized")
        logger.info(f"[AutoUpdate] API: {api_base}")
        logger.info(f"[AutoUpdate] User: {user_id}")

    def analyze_change(self, event_type, file_path):
        """
        Analiza qué tipo de cambio ocurrió.

        Args:
            event_type: 'created' o 'modified'
            file_path: Path del archivo que cambió

        Returns:
            dict con análisis del cambio
        """
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix

        analysis = {
            "event_type": event_type,
            "file_path": file_path,
            "file_name": file_name,
            "file_ext": file_ext,
            "timestamp": datetime.now().isoformat(),
            "data_type": self._identify_data_type(file_path),
            "action_required": "full_update"
        }

        logger.info(f"[AutoUpdate] Change analyzed: {analysis['data_type']}")
        return analysis

    def _identify_data_type(self, file_path):
        """Identifica tipo de datos basado en nombre de archivo"""
        file_name = Path(file_path).name.lower()

        if 'flightscope' in file_name or file_name.endswith('.csv'):
            return 'flightscope'
        elif 'tarjeta' in file_name or 'scorecard' in file_name:
            return 'scorecard'
        elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            return 'excel_data'
        else:
            return 'unknown'

    def run_data_generator(self):
        """
        Ejecuta generate_dashboard_data.py

        Returns:
            bool: True si exitoso
        """
        logger.info("[AutoUpdate] Running data generator...")

        try:
            script_path = self.project_root / "generate_dashboard_data.py"

            if not script_path.exists():
                logger.error(f"[AutoUpdate] Script not found: {script_path}")
                return False

            # Run script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.success("[AutoUpdate] Data generator completed successfully")
                return True
            else:
                logger.error(f"[AutoUpdate] Data generator failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("[AutoUpdate] Data generator timeout (>30s)")
            return False
        except Exception as e:
            logger.error(f"[AutoUpdate] Error running generator: {e}")
            return False

    def verify_json_output(self):
        """
        Verifica que dashboard_data.json se generó correctamente.

        Returns:
            dict: Data loaded o None si falla
        """
        logger.info("[AutoUpdate] Verifying JSON output...")

        json_path = self.project_root / "output" / "dashboard_data.json"

        if not json_path.exists():
            logger.error(f"[AutoUpdate] JSON not found: {json_path}")
            return None

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.success(f"[AutoUpdate] JSON verified ({len(json.dumps(data))} bytes)")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"[AutoUpdate] JSON parse error: {e}")
            return None
        except Exception as e:
            logger.error(f"[AutoUpdate] Error reading JSON: {e}")
            return None

    def auto_ingest_to_pinecone(self, data):
        """
        Auto-ingesta a Pinecone via POST /ingest.

        Args:
            data: dashboard_data.json content

        Returns:
            bool: True si exitoso
        """
        logger.info("[AutoUpdate] Auto-ingesting to Pinecone...")

        # Convert club_statistics to shots format
        shots = []
        for club in data.get("club_statistics", []):
            shot = {
                "date": "2025-12-31",  # Placeholder for aggregated data
                "source": "auto_update",
                "club": club.get("name", "Unknown"),
                "hole": 0,
                "ball_speed": float(club.get("speed_raw", 0)),
                "carry": float(club.get("distance_raw", 0)),
                "launch_angle": float(club.get("launch_angle_mean", 0)),
                "face_to_path": 0,
                "score": 0,
                "notes": f"Auto-updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
            shots.append(shot)

        if not shots:
            logger.warning("[AutoUpdate] No shots to ingest")
            return False

        # POST to /ingest
        try:
            url = f"{self.api_base}/ingest"
            payload = {
                "user_id": self.user_id,
                "shots": shots
            }

            logger.info(f"[AutoUpdate] Posting {len(shots)} shots to {url}...")

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            logger.success(f"[AutoUpdate] Ingestion successful: {result.get('chunks_ingested')} chunks")
            return True

        except requests.exceptions.ConnectionError:
            logger.error("[AutoUpdate] Cannot connect to API. Is backend running?")
            return False
        except requests.exceptions.Timeout:
            logger.error("[AutoUpdate] Ingestion timeout")
            return False
        except Exception as e:
            logger.error(f"[AutoUpdate] Ingestion error: {e}")
            return False

    def notify_user(self, success, details):
        """
        Notifica usuario del resultado.

        Args:
            success: bool
            details: dict con detalles
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if success:
            logger.success("=" * 70)
            logger.success("✅ DASHBOARD AUTO-UPDATE SUCCESSFUL")
            logger.success("=" * 70)
            logger.info(f"Timestamp: {timestamp}")
            logger.info(f"Data type: {details.get('data_type', 'unknown')}")
            logger.info(f"File: {details.get('file_name', 'unknown')}")
            logger.info("Actions completed:")
            logger.info("  1. ✅ Data generator executed")
            logger.info("  2. ✅ JSON verified")
            logger.info("  3. ✅ Pinecone updated")
            logger.success("Dashboard is now up-to-date!")
            logger.success("=" * 70)
        else:
            logger.error("=" * 70)
            logger.error("❌ DASHBOARD AUTO-UPDATE FAILED")
            logger.error("=" * 70)
            logger.error(f"Timestamp: {timestamp}")
            logger.error(f"File: {details.get('file_name', 'unknown')}")
            logger.error("Please check logs above for details")
            logger.error("=" * 70)

    def execute_update_pipeline(self, event_type, file_path):
        """
        Ejecuta el pipeline completo de actualización.

        Args:
            event_type: 'created' o 'modified'
            file_path: Path del archivo que cambió

        Returns:
            bool: True si todo exitoso
        """
        logger.info("=" * 70)
        logger.info("🚀 AUTO-UPDATE PIPELINE STARTED")
        logger.info("=" * 70)

        # Step 1: Analyze change
        analysis = self.analyze_change(event_type, file_path)

        # Step 2: Run data generator
        if not self.run_data_generator():
            self.notify_user(False, analysis)
            return False

        # Step 3: Verify JSON
        data = self.verify_json_output()
        if not data:
            self.notify_user(False, analysis)
            return False

        # Step 4: Auto-ingest to Pinecone
        if not self.auto_ingest_to_pinecone(data):
            self.notify_user(False, analysis)
            return False

        # Step 5: Notify success
        self.notify_user(True, analysis)
        return True


# Export
__all__ = ["AutoUpdateAgent"]
