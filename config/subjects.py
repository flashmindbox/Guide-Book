"""
Subject configurations for Guide Book Generator.
Defines which parts are available for each subject and their specific settings.
Supports all CBSE Class 9 and 10 subjects.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# =============================================================================
# SUBJECT CONFIGURATIONS
# =============================================================================

SUBJECT_CONFIGS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # SOCIAL SCIENCE SUBJECTS
    # =========================================================================
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
        'has_map_work': True,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['timeline', 'did_you_know', 'memory_tricks'],
        'enabled': True,
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
        'has_map_work': True,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': True,
        'special_features': ['map_skills', 'did_you_know', 'memory_tricks'],
        'enabled': True,
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
            'E': 'Constitutional Articles',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['constitutional_articles', 'case_studies', 'memory_tricks'],
        'enabled': True,
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
            'E': 'Graphs & Data',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': True,
        'has_formulas': True,
        'has_diagrams': True,
        'special_features': ['formulas', 'graphs', 'memory_tricks', 'data_analysis'],
        'enabled': True,
    },

    # =========================================================================
    # MATHEMATICS
    # =========================================================================
    'mathematics': {
        'name': 'Mathematics',
        'category': 'Mathematics',
        'icon': '📐',
        'accent_color': '#2563EB',  # Blue
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts & Theorems',
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
        'has_diagrams': True,
        'special_features': ['step_by_step', 'theorem_proofs', 'formula_derivations', 'geometry_constructions'],
        'enabled': True,
    },

    # =========================================================================
    # SCIENCE
    # =========================================================================
    'science': {
        'name': 'Science',
        'category': 'Science',
        'icon': '🔬',
        'accent_color': '#059669',  # Green
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Diagrams & Reactions',
            'D': 'Numericals & Practice',
            'E': 'Lab Manual & Activities',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': True,
        'has_numericals': True,
        'has_formulas': True,
        'has_diagrams': True,
        'special_features': ['diagrams', 'experiments', 'derivations', 'reactions', 'practical_activities'],
        'enabled': True,
    },

    'physics': {
        'name': 'Physics',
        'category': 'Science',
        'icon': '⚛️',
        'accent_color': '#3B82F6',  # Blue
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts & Laws',
            'C': 'Derivations & Diagrams',
            'D': 'Numerical Problems',
            'E': 'Formula Sheet',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': True,
        'has_numericals': True,
        'has_formulas': True,
        'has_diagrams': True,
        'special_features': ['derivations', 'diagrams', 'numericals', 'practical_activities'],
        'enabled': True,
    },

    'chemistry': {
        'name': 'Chemistry',
        'category': 'Science',
        'icon': '🧪',
        'accent_color': '#8B5CF6',  # Violet
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Reactions & Equations',
            'D': 'Practice Questions',
            'E': 'Lab Activities',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': True,
        'has_numericals': True,
        'has_formulas': True,
        'has_diagrams': True,
        'special_features': ['reactions', 'equations', 'diagrams', 'practical_activities'],
        'enabled': True,
    },

    'biology': {
        'name': 'Biology',
        'category': 'Science',
        'icon': '🧬',
        'accent_color': '#10B981',  # Emerald
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Diagrams & Flowcharts',
            'D': 'Practice Questions',
            'E': 'Lab Activities',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': True,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': True,
        'special_features': ['diagrams', 'flowcharts', 'practical_activities', 'life_processes'],
        'enabled': True,
    },

    # =========================================================================
    # ENGLISH
    # =========================================================================
    'english': {
        'name': 'English',
        'category': 'English',
        'icon': '📚',
        'accent_color': '#DC2626',  # Red
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Summary & Themes',
            'C': 'Character Analysis',
            'D': 'Important Questions',
            'E': 'Grammar Focus',
            'F': 'Writing Skills',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['vocabulary', 'literary_devices', 'writing_templates', 'comprehension'],
        'enabled': True,
    },

    'english_literature': {
        'name': 'English Literature',
        'category': 'English',
        'icon': '📖',
        'accent_color': '#BE185D',  # Pink
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Summary & Themes',
            'C': 'Character Sketches',
            'D': 'Extract-Based Questions',
            'E': 'Long Answer Questions',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['themes', 'characters', 'literary_devices', 'extracts'],
        'enabled': True,
    },

    'english_grammar': {
        'name': 'English Grammar',
        'category': 'English',
        'icon': '✏️',
        'accent_color': '#F59E0B',  # Amber
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Grammar Rules',
            'C': 'Error Correction',
            'D': 'Practice Exercises',
            'E': 'Sentence Transformation',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['grammar_rules', 'error_correction', 'sentence_transformation'],
        'enabled': True,
    },

    # =========================================================================
    # HINDI
    # =========================================================================
    'hindi': {
        'name': 'Hindi',
        'category': 'Hindi',
        'icon': '🔤',
        'accent_color': '#EA580C',  # Orange
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'पाठ सारांश (Summary)',
            'C': 'प्रश्न-उत्तर (Q&A)',
            'D': 'अभ्यास प्रश्न (Practice)',
            'E': 'व्याकरण (Grammar)',
            'F': 'त्वरित पुनरावृत्ति (Quick Revision)',
            'G': 'परीक्षा रणनीति (Exam Strategy)',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['summary', 'character_sketch', 'grammar', 'letter_writing'],
        'enabled': True,
    },

    'hindi_a': {
        'name': 'Hindi Course A',
        'category': 'Hindi',
        'icon': '📝',
        'accent_color': '#EA580C',  # Orange
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'पाठ सारांश (Summary)',
            'C': 'कवि/लेखक परिचय',
            'D': 'प्रश्न-उत्तर (Q&A)',
            'E': 'व्याकरण (Grammar)',
            'F': 'लेखन कौशल (Writing)',
            'G': 'परीक्षा रणनीति',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['summary', 'author_intro', 'grammar', 'writing_skills'],
        'enabled': True,
    },

    'hindi_b': {
        'name': 'Hindi Course B',
        'category': 'Hindi',
        'icon': '📋',
        'accent_color': '#C2410C',  # Orange Dark
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'पाठ सारांश (Summary)',
            'C': 'प्रश्न-उत्तर (Q&A)',
            'D': 'अभ्यास प्रश्न (Practice)',
            'E': 'व्याकरण (Grammar)',
            'F': 'त्वरित पुनरावृत्ति',
            'G': 'परीक्षा रणनीति',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['summary', 'grammar', 'writing_skills'],
        'enabled': True,
    },

    # =========================================================================
    # SANSKRIT (Optional)
    # =========================================================================
    'sanskrit': {
        'name': 'Sanskrit',
        'category': 'Sanskrit',
        'icon': '🕉️',
        'accent_color': '#9333EA',  # Purple
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'पाठ सारांश (Summary)',
            'C': 'श्लोक अर्थ (Shloka Meaning)',
            'D': 'प्रश्न-उत्तर (Q&A)',
            'E': 'व्याकरण (Grammar)',
            'F': 'त्वरित पुनरावृत्ति',
            'G': 'परीक्षा रणनीति',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': False,
        'special_features': ['shloka_meaning', 'grammar', 'sandhi', 'samasa'],
        'enabled': True,
    },

    # =========================================================================
    # INFORMATION TECHNOLOGY / COMPUTER SCIENCE
    # =========================================================================
    'computer_science': {
        'name': 'Computer Science',
        'category': 'Computer',
        'icon': '💻',
        'accent_color': '#0EA5E9',  # Sky Blue
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Programs & Code',
            'D': 'Practice Questions',
            'E': 'Practical Work',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': True,
        'special_features': ['code_snippets', 'flowcharts', 'practical_programs'],
        'enabled': True,
    },

    'information_technology': {
        'name': 'Information Technology',
        'category': 'Computer',
        'icon': '🖥️',
        'accent_color': '#06B6D4',  # Cyan
        'parts': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'part_names': {
            'A': 'PYQ Analysis',
            'B': 'Key Concepts',
            'C': 'Practical Skills',
            'D': 'Practice Questions',
            'E': 'Lab Exercises',
            'F': 'Quick Revision',
            'G': 'Exam Strategy',
        },
        'has_map_work': False,
        'has_experiments': False,
        'has_numericals': False,
        'has_formulas': False,
        'has_diagrams': True,
        'special_features': ['practical_skills', 'software_usage', 'web_development'],
        'enabled': True,
    },
}


# =============================================================================
# SUBJECT CATEGORY MAPPING
# =============================================================================

SUBJECT_CATEGORIES = {
    'Social Science': {
        'icon': '🏛️',
        'subjects': ['history', 'geography', 'political_science', 'economics'],
        'description': 'History, Geography, Political Science & Economics',
    },
    'Science': {
        'icon': '🔬',
        'subjects': ['science', 'physics', 'chemistry', 'biology'],
        'description': 'Combined Science or Physics, Chemistry, Biology',
    },
    'Mathematics': {
        'icon': '📐',
        'subjects': ['mathematics'],
        'description': 'Mathematics',
    },
    'English': {
        'icon': '📚',
        'subjects': ['english', 'english_literature', 'english_grammar'],
        'description': 'English Language & Literature',
    },
    'Hindi': {
        'icon': '🔤',
        'subjects': ['hindi', 'hindi_a', 'hindi_b'],
        'description': 'Hindi Course A & B',
    },
    'Sanskrit': {
        'icon': '🕉️',
        'subjects': ['sanskrit'],
        'description': 'Sanskrit (Optional)',
    },
    'Computer': {
        'icon': '💻',
        'subjects': ['computer_science', 'information_technology'],
        'description': 'Computer Science / IT',
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
        if config['category'] == category and config.get('enabled', True)
    ]


def get_all_enabled_subjects() -> List[Dict[str, Any]]:
    """Get all enabled subjects with their configurations."""
    return [
        {'id': subject_id, **config}
        for subject_id, config in SUBJECT_CONFIGS.items()
        if config.get('enabled', True)
    ]


def get_subject_display_name(subject_id: str) -> str:
    """Get display name for a subject."""
    config = get_subject_config(subject_id)
    return config.get('name', subject_id.replace('_', ' ').title())


def get_subject_icon(subject_id: str) -> str:
    """Get icon for a subject."""
    config = get_subject_config(subject_id)
    return config.get('icon', '📖')


def get_categories_with_subjects() -> Dict[str, List[Dict[str, Any]]]:
    """Get all categories with their subjects for UI display."""
    result = {}
    for category, cat_info in SUBJECT_CATEGORIES.items():
        subjects = []
        for subject_id in cat_info['subjects']:
            if subject_id in SUBJECT_CONFIGS and SUBJECT_CONFIGS[subject_id].get('enabled', True):
                config = SUBJECT_CONFIGS[subject_id]
                subjects.append({
                    'id': subject_id,
                    'name': config['name'],
                    'icon': config['icon'],
                })
        if subjects:
            result[category] = {
                'icon': cat_info['icon'],
                'description': cat_info['description'],
                'subjects': subjects,
            }
    return result


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
