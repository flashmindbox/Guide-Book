"""
Logging configuration for Guide Book Generator.
Provides structured logging to console and file.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


# Default log directory
LOG_DIR = Path("data/logs")
LOG_FILE = "app.log"


def setup_logging(
    log_dir: Optional[Path] = None,
    log_file: Optional[str] = None,
    level: int = logging.INFO
) -> None:
    """
    Set up the root logger with console and file handlers.

    Args:
        log_dir: Directory for log files (default: data/logs)
        log_file: Log file name (default: app.log)
        level: Logging level (default: INFO)
    """
    log_dir = log_dir or LOG_DIR
    log_file = log_file or LOG_FILE

    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_file

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    try:
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # If we can't create the file handler, just log to console
        console_handler.setLevel(logging.DEBUG)
        root_logger.warning(f"Could not create log file at {log_path}: {e}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured Logger instance
    """
    return logging.getLogger(name)


# Initialize logging on module import (can be reconfigured later)
# Use a flag to avoid re-initialization
_initialized = False


def ensure_initialized():
    """Ensure logging is initialized (called lazily)."""
    global _initialized
    if not _initialized:
        setup_logging()
        _initialized = True
