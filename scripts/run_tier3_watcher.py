"""
TIER 3 Watcher Runner

Script principal que integra File Watcher + Auto-Update Agent.

Usage:
    python scripts/run_tier3_watcher.py

Press Ctrl+C to stop.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.watcher import DataWatcher
from app.agents.auto_update import AutoUpdateAgent
from loguru import logger


def on_data_change(event_type, file_path):
    """
    Callback ejecutado cuando el watcher detecta cambios.

    Args:
        event_type: 'created' o 'modified'
        file_path: Path del archivo que cambió
    """
    logger.info(f"[Main] Data change detected: {event_type} | {file_path}")

    # Create agent
    agent = AutoUpdateAgent(
        api_base="http://localhost:8000",
        user_id="alvaro"
    )

    # Execute update pipeline
    success = agent.execute_update_pipeline(event_type, file_path)

    if success:
        logger.success("[Main] Update pipeline completed successfully")
    else:
        logger.error("[Main] Update pipeline failed")


def main():
    """Main execution"""
    # Setup logging
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

    logger.info("=" * 70)
    logger.info("🤖 TIER 3 - Auto-Update Watcher")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Monitoring: data/raw/ for changes")
    logger.info("Watching: .csv, .xlsx, .xls files")
    logger.info("")
    logger.info("When changes detected:")
    logger.info("  1. Analyze change")
    logger.info("  2. Run data generator")
    logger.info("  3. Verify JSON output")
    logger.info("  4. Auto-ingest to Pinecone")
    logger.info("  5. Notify user")
    logger.info("")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 70)
    logger.info("")

    # Create watcher
    watch_dir = project_root / "data" / "raw"
    watcher = DataWatcher(watch_dir, on_data_change)

    # Start watching
    watcher.start()

    # Run forever
    try:
        watcher.run_forever()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 70)
        logger.info("🛑 TIER 3 Watcher stopped by user")
        logger.info("=" * 70)
        watcher.stop()


if __name__ == "__main__":
    main()
