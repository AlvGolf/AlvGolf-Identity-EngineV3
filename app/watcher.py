"""
File Watcher - TIER 3

Monitorea data/raw/ por cambios en archivos CSV y Excel.
Cuando detecta cambios, activa el Auto-Update Agent.
"""

import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DataFileHandler(FileSystemEventHandler):
    """
    Handler para eventos de cambios en archivos de datos.

    Monitorea:
    - .csv (FlightScope)
    - .xlsx/.xls (Tarjetas)
    """

    def __init__(self, callback):
        """
        Args:
            callback: Función a llamar cuando se detecta cambio
        """
        self.callback = callback
        self.last_trigger = {}
        self.debounce_seconds = 5  # Evitar triggers múltiples

        logger.info("[Watcher] Handler initialized")

    def should_trigger(self, file_path):
        """
        Debouncing: Solo trigger si han pasado N segundos desde último.
        """
        now = time.time()
        last = self.last_trigger.get(file_path, 0)

        if now - last < self.debounce_seconds:
            return False

        self.last_trigger[file_path] = now
        return True

    def on_modified(self, event):
        """Evento: Archivo modificado"""
        if event.is_directory:
            return

        file_path = event.src_path

        # Solo archivos de datos
        if not (file_path.endswith('.csv') or
                file_path.endswith('.xlsx') or
                file_path.endswith('.xls')):
            return

        # Debouncing
        if not self.should_trigger(file_path):
            logger.debug(f"[Watcher] Debounced: {file_path}")
            return

        logger.info(f"[Watcher] MODIFIED detected: {file_path}")
        self.callback(event_type='modified', file_path=file_path)

    def on_created(self, event):
        """Evento: Archivo creado"""
        if event.is_directory:
            return

        file_path = event.src_path

        # Solo archivos de datos
        if not (file_path.endswith('.csv') or
                file_path.endswith('.xlsx') or
                file_path.endswith('.xls')):
            return

        # Debouncing
        if not self.should_trigger(file_path):
            logger.debug(f"[Watcher] Debounced: {file_path}")
            return

        logger.info(f"[Watcher] CREATED detected: {file_path}")
        self.callback(event_type='created', file_path=file_path)


class DataWatcher:
    """
    Watcher principal que monitorea data/raw/ directory.
    """

    def __init__(self, watch_path, callback):
        """
        Args:
            watch_path: Path del directorio a monitorear
            callback: Función a llamar cuando hay cambios
        """
        self.watch_path = Path(watch_path)
        self.callback = callback
        self.observer = None

        # Verify path exists
        if not self.watch_path.exists():
            logger.warning(f"[Watcher] Creating watch directory: {self.watch_path}")
            self.watch_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"[Watcher] Initialized for: {self.watch_path}")

    def start(self):
        """Inicia el watcher en background"""
        event_handler = DataFileHandler(self.callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_path), recursive=True)
        self.observer.start()

        logger.success(f"[Watcher] Started monitoring: {self.watch_path}")
        logger.info("[Watcher] Watching for .csv, .xlsx, .xls files")

    def stop(self):
        """Detiene el watcher"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("[Watcher] Stopped")

    def run_forever(self):
        """
        Mantiene el watcher corriendo indefinidamente.
        Press Ctrl+C to stop.
        """
        try:
            logger.info("[Watcher] Running forever (Ctrl+C to stop)...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("[Watcher] Keyboard interrupt received")
            self.stop()


# Standalone execution
if __name__ == "__main__":
    def test_callback(event_type, file_path):
        """Test callback"""
        print(f"[TEST] Event: {event_type} | File: {file_path}")

    # Setup logging
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    # Watch data/raw directory
    project_root = Path(__file__).parent.parent
    watch_dir = project_root / "data" / "raw"

    watcher = DataWatcher(watch_dir, test_callback)
    watcher.start()
    watcher.run_forever()
