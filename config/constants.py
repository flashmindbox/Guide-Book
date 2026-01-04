"""
Application-wide constants for Guide Book Generator.
"""

import logging
from pathlib import Path

# =============================================================================
# APPLICATION INFO
# =============================================================================

APP_NAME = "Guide Book Generator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "CBSE Class 9 & 10 Study Guide Generator"

# =============================================================================
# DIRECTORY PATHS
# =============================================================================

# Base directory (where app.py is located)
BASE_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
AUTOSAVE_DIR = DATA_DIR / "autosave"
CHAPTERS_DIR = BASE_DIR / "config" / "chapters"
IMAGES_DIR = DATA_DIR / "images"
OUTPUT_DIR = DATA_DIR / "output"

# Ensure directories exist
for dir_path in [DATA_DIR, AUTOSAVE_DIR, IMAGES_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# =============================================================================
# AUTO-SAVE SETTINGS
# =============================================================================

AUTOSAVE_INTERVAL_SECONDS = 5
AUTOSAVE_ENABLED = True
MAX_AUTOSAVE_FILES = 10  # Keep last N autosaves per chapter

# =============================================================================
# CLASS DEFINITIONS
# =============================================================================

SUPPORTED_CLASSES = [
    {'id': 9, 'name': 'Class 9', 'enabled': True},
    {'id': 10, 'name': 'Class 10', 'enabled': True},
]

DEFAULT_CLASS = 10

# =============================================================================
# SUBJECT CATEGORIES
# =============================================================================

SUBJECT_CATEGORIES = {
    'social_science': {
        'name': 'Social Science',
        'subjects': ['history', 'geography', 'political_science', 'economics'],
        'has_sub_subjects': True,
    },
    'mathematics': {
        'name': 'Mathematics',
        'subjects': ['mathematics'],
        'has_sub_subjects': False,
    },
    'science': {
        'name': 'Science',
        'subjects': ['science'],
        'has_sub_subjects': False,
    },
    'english': {
        'name': 'English',
        'subjects': ['english'],
        'has_sub_subjects': False,
    },
    'hindi': {
        'name': 'Hindi',
        'subjects': ['hindi'],
        'has_sub_subjects': False,
    },
}

# =============================================================================
# QUESTION TYPES
# =============================================================================

QUESTION_TYPES = {
    'mcq': {
        'name': 'Multiple Choice Questions',
        'short_name': 'MCQs',
        'marks': 1,
    },
    'ar': {
        'name': 'Assertion-Reason Questions',
        'short_name': 'AR',
        'marks': 1,
    },
    'vsa': {
        'name': 'Very Short Answer Questions',
        'short_name': 'VSA',
        'marks': 1,
    },
    'sa': {
        'name': 'Short Answer Questions',
        'short_name': 'SA',
        'marks': 3,
    },
    'la': {
        'name': 'Long Answer Questions',
        'short_name': 'LA',
        'marks': 5,
    },
    'hots': {
        'name': 'Higher Order Thinking Skills',
        'short_name': 'HOTS',
        'marks': 5,
    },
    'cbq': {
        'name': 'Case/Source Based Questions',
        'short_name': 'CBQs',
        'marks': 4,
    },
    'map': {
        'name': 'Map-Based Questions',
        'short_name': 'Map',
        'marks': 2,
    },
}

# =============================================================================
# FILE NAMING CONVENTIONS
# =============================================================================

def get_autosave_filename(class_num: int, subject: str, chapter_num: int) -> str:
    """Generate autosave filename."""
    return f"class_{class_num}_{subject}_ch{chapter_num:02d}_autosave.json"

def get_output_filename(class_num: int, subject: str, chapter_num: int, chapter_title: str) -> str:
    """Generate output document filename."""
    safe_title = "".join(c for c in chapter_title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')[:50]
    return f"Ch{chapter_num}_{safe_title}_Class{class_num}.docx"

# =============================================================================
# VALIDATION LIMITS
# =============================================================================

MAX_CHAPTER_TITLE_LENGTH = 200
MAX_CONCEPT_CONTENT_LENGTH = 10000
MAX_ANSWER_LENGTH = 5000
MAX_CONCEPTS_COUNT = 50
MAX_QUESTIONS_PER_TYPE = 100

# =============================================================================
# UI SETTINGS
# =============================================================================

PREVIEW_MAX_HEIGHT = 600  # pixels
SIDEBAR_WIDTH = 300  # pixels

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

def setup_logging() -> None:
    """Configure application-wide logging."""
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Only add handler if none exist to avoid duplicate logs
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


# Initialize logging at module load
setup_logging()
