"""
Auto-save functionality for Guide Book Generator.
Implements throttled auto-save to prevent excessive disk writes.
"""

import json
import time
from pathlib import Path
from threading import Timer
from typing import Optional


class AutoSaveManager:
    """Manages throttled auto-save functionality."""

    THROTTLE_SECONDS = 5  # Minimum time between saves

    def __init__(self, autosave_dir: Path):
        self.autosave_dir = autosave_dir
        self.autosave_dir.mkdir(parents=True, exist_ok=True)
        self.last_save_time = 0
        self._pending_timer: Optional[Timer] = None
        self._pending_data = None
        self._pending_filename = None

    def save(self, data: dict, filename: str) -> bool:
        """
        Save data with throttling.
        Returns True if save was immediate, False if queued.
        """
        current_time = time.time()
        time_since_last = current_time - self.last_save_time

        if time_since_last >= self.THROTTLE_SECONDS:
            # Save immediately
            self._do_save(data, filename)
            return True
        else:
            # Queue save for later
            self._queue_save(data, filename)
            return False

    def _do_save(self, data: dict, filename: str):
        """Perform the actual save operation."""
        filepath = self.autosave_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.last_save_time = time.time()
        except Exception as e:
            print(f"Auto-save error: {e}")

    def _queue_save(self, data: dict, filename: str):
        """Queue a save for later execution."""
        self._pending_data = data
        self._pending_filename = filename

        # Cancel existing timer if any
        if self._pending_timer:
            self._pending_timer.cancel()

        # Calculate delay
        delay = self.THROTTLE_SECONDS - (time.time() - self.last_save_time)
        delay = max(0.1, delay)  # Minimum 100ms

        # Set new timer
        self._pending_timer = Timer(delay, self._execute_pending_save)
        self._pending_timer.daemon = True
        self._pending_timer.start()

    def _execute_pending_save(self):
        """Execute the pending save."""
        if self._pending_data and self._pending_filename:
            self._do_save(self._pending_data, self._pending_filename)
            self._pending_data = None
            self._pending_filename = None
            self._pending_timer = None

    def force_save(self, data: dict, filename: str):
        """Force an immediate save, bypassing throttle."""
        # Cancel any pending save
        if self._pending_timer:
            self._pending_timer.cancel()
            self._pending_timer = None
            self._pending_data = None
            self._pending_filename = None

        self._do_save(data, filename)

    def get_saved_files(self) -> list:
        """Get list of saved files, sorted by modification time."""
        files = list(self.autosave_dir.glob("*.json"))
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return files

    def load(self, filename: str) -> Optional[dict]:
        """Load data from autosave file."""
        filepath = self.autosave_dir / filename

        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Load error: {e}")
            return None

    def delete(self, filename: str) -> bool:
        """Delete an autosave file."""
        filepath = self.autosave_dir / filename

        try:
            if filepath.exists():
                filepath.unlink()
                return True
        except Exception as e:
            print(f"Delete error: {e}")

        return False
