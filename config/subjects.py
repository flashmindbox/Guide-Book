"""
Subject configurations for Guide Book Generator.
Defines which parts are available for each subject and their specific settings.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# =============================================================================
# SUBJECT CONFIGURATIONS
# =============================================================================

SUBJECT_CONFIGS: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # SOCIAL SCIENCE SUBJECTS
    # -------------------------------------------------------------------------
    'history': {
        'name': 'History',
        'category': 'Social Science',
        'icon': '📜',
        'accent_color': '#B45309',  # Amber
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Model Answers',
            'D': 'Practice Questions',
            'E': 'Map Work',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': True,  # Only Chapter 2 for Class 10
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'special_features': ['timeline', 'did_you_know', 'memory_tricks'],
    },

    'geography': {
        'name': 'Geography',
        'category': 'Social Science',
        'icon': '🌍',
        'accent_color': '#059669',  # Green
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Model Answers',
            'D': 'Practice Questions',
            'E': 'Map Work',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': True,  # Most chapters have map work
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'special_features': ['map_skills', 'did_you_know', 'memory_tricks'],
    },

    'political_science': {
        'name': 'Political Science',
        'category': 'Social Science',
        'icon': '⚖️',
        'accent_color': '#7C3AED',  # Purple
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Model Answers',
            'D': 'Practice Questions',
            'E': 'Map Work',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,  # No map work in Political Science
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'special_features': ['constitutional_articles', 'case_studies', 'memory_tricks'],
    },

    'economics': {
        'name': 'Economics',
        'category': 'Social Science',
        'icon': '💰',
        'accent_color': '#0891B2',  # Cyan
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Model Answers',
            'D': 'Practice Questions',
            'E': 'Map Work',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': True,  # HDI calculations, etc.
        'has_formulas': True,
        'special_features': ['formulas', 'graphs', 'memory_tricks'],
    },

    # -------------------------------------------------------------------------
    # MATHEMATICS (Future)
    # -------------------------------------------------------------------------
    'mathematics': {
        'name': 'Mathematics',
        'category': 'Mathematics',
        'icon': '📐',
        'accent_color': '#2563EB',  # Blue
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts & Formulas',
            'C': 'Solved Examples',
            'D': 'Practice Problems',
            'E': 'Formula Sheet',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': True,
        'has_formulas': True,
        'special_features': ['step_by_step', 'theorem_proofs', 'formula_derivations'],
    },

    # -------------------------------------------------------------------------
    # SCIENCE (Future)
    # -------------------------------------------------------------------------
    'science': {
        'name': 'Science',
        'category': 'Science',
        'icon': '🔬',
        'accent_color': '#059669',  # Green
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Diagrams & Experiments',
            'D': 'Numericals & Practice',
            'E': 'Lab Manual Summary',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': True,
        'has_numericals': True,
        'has_formulas': True,
        'special_features': ['diagrams', 'experiments', 'derivations', 'reactions'],
    },

    # -------------------------------------------------------------------------
    # ENGLISH (Future)
    # -------------------------------------------------------------------------
    'english': {
        'name': 'English',
        'category': 'English',
        'icon': '📚',
        'accent_color': '#DC2626',  # Red
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Summary & Themes',
            'C': 'Character Sketches',
            'D': 'Important Questions',
            'E': 'Grammar Focus',
            'F': 'Writing Formats',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'special_features': ['vocabulary', 'literary_devices', 'writing_templates'],
    },
}


def get_subject_config(subject_id: str) -> Dict[str, Any]:
    """Get configuration for a specific subject."""
    return SUBJECT_CONFIGS.get(subject_id, SUBJECT_CONFIGS['history'])


def get_part_name(subject_id: str, part_id: str) -> str:
    """Get the display name for a part in a specific subject."""
    config = get_subject_config(subject_id)
    return config['part_names'].get(part_id, f'Part {part_id}')


def get_available_parts(subject_id: str) -> List[str]:
    """Get list of available parts for a subject."""
    config = get_subject_config(subject_id)
    return config.get('parts', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])


def subject_has_map_work(subject_id: str) -> bool:
    """Check if subject has map work."""
    config = get_subject_config(subject_id)
    return config.get('has_map_work', False)


def get_subjects_by_category(category: str) -> List[str]:
    """Get list of subjects in a category."""
    return [
        subject_id for subject_id, config in SUBJECT_CONFIGS.items()
        if config['category'] == category
    ]


# =============================================================================
# CHAPTER LOADING
# =============================================================================

def load_chapters(class_num: int, subject_id: str) -> List[Dict[str, Any]]:
    """
    Load chapter list for a class and subject.
    Returns list of chapters with number and title.
    """
    chapters_dir = Path(__file__).parent / "chapters"

    # Try subject-specific file first
    file_path = chapters_dir / f"class_{class_num}_{subject_id}.json"
    if not file_path.exists():
        # Try combined social science file
        file_path = chapters_dir / f"class_{class_num}_social_science.json"

    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle nested structure (social science has sub-subjects)
            if subject_id in data:
                return data[subject_id]
            return data.get('chapters', [])

    # Return empty list if no chapters found
    return []


def get_chapter_by_number(class_num: int, subject_id: str, chapter_num: int) -> Dict[str, Any]:
    """Get a specific chapter by number."""
    chapters = load_chapters(class_num, subject_id)
    for chapter in chapters:
        if chapter.get('number') == chapter_num:
            return chapter
    return {'number': chapter_num, 'title': f'Chapter {chapter_num}'}
