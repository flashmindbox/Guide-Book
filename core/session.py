"""
Session state management for Guide Book Generator.
Handles Streamlit session state for chapter data and app state.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

import streamlit as st

from .models.base import ChapterData
from .models.parts import PartManager


class SessionManager:
    """
    Manages Streamlit session state for the application.
    Handles initialization, access, and persistence of chapter data.
    """

    # Session state keys
    KEY_CHAPTER_DATA = 'chapter_data'
    KEY_PART_MANAGER = 'part_manager'
    KEY_CURRENT_CLASS = 'current_class'
    KEY_CURRENT_SUBJECT = 'current_subject'
    KEY_CURRENT_CHAPTER = 'current_chapter'
    KEY_CURRENT_PAGE = 'current_page'
    KEY_LAST_SAVE_TIME = 'last_save_time'
    KEY_IS_DIRTY = 'is_dirty'
    KEY_AUTOSAVE_ENABLED = 'autosave_enabled'
    KEY_SHOW_PREVIEW = 'show_preview'

    @classmethod
    def initialize(cls) -> None:
        """Initialize session state with defaults if not already set."""
        defaults = {
            cls.KEY_CHAPTER_DATA: None,
            cls.KEY_PART_MANAGER: None,
            cls.KEY_CURRENT_CLASS: 10,
            cls.KEY_CURRENT_SUBJECT: 'history',
            cls.KEY_CURRENT_CHAPTER: 1,
            cls.KEY_CURRENT_PAGE: 'home',
            cls.KEY_LAST_SAVE_TIME: None,
            cls.KEY_IS_DIRTY: False,
            cls.KEY_AUTOSAVE_ENABLED: True,
            cls.KEY_SHOW_PREVIEW: False,
        }

        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @classmethod
    def get_chapter_data(cls) -> Optional[ChapterData]:
        """Get the current chapter data."""
        cls.initialize()
        return st.session_state.get(cls.KEY_CHAPTER_DATA)

    @classmethod
    def set_chapter_data(cls, data: ChapterData) -> None:
        """Set the chapter data and mark as dirty."""
        cls.initialize()
        st.session_state[cls.KEY_CHAPTER_DATA] = data
        st.session_state[cls.KEY_IS_DIRTY] = True

    @classmethod
    def get_part_manager(cls) -> PartManager:
        """Get the part manager, creating default if needed."""
        cls.initialize()
        if st.session_state[cls.KEY_PART_MANAGER] is None:
            st.session_state[cls.KEY_PART_MANAGER] = PartManager()
        return st.session_state[cls.KEY_PART_MANAGER]

    @classmethod
    def set_part_manager(cls, manager: PartManager) -> None:
        """Set the part manager."""
        cls.initialize()
        st.session_state[cls.KEY_PART_MANAGER] = manager

    @classmethod
    def create_new_chapter(
        cls,
        class_num: int,
        subject: str,
        chapter_number: int,
        chapter_title: str = ""
    ) -> ChapterData:
        """Create a new chapter and set it as current."""
        data = ChapterData(
            class_num=class_num,
            subject=subject,
            chapter_number=chapter_number,
            chapter_title=chapter_title,
        )
        cls.set_chapter_data(data)
        cls.set_part_manager(PartManager())

        # Update current selections
        st.session_state[cls.KEY_CURRENT_CLASS] = class_num
        st.session_state[cls.KEY_CURRENT_SUBJECT] = subject
        st.session_state[cls.KEY_CURRENT_CHAPTER] = chapter_number

        return data

    @classmethod
    def update_chapter_field(cls, field_name: str, value: Any) -> None:
        """Update a specific field in the chapter data."""
        data = cls.get_chapter_data()
        if data and hasattr(data, field_name):
            setattr(data, field_name, value)
            data.update_timestamp()
            st.session_state[cls.KEY_IS_DIRTY] = True

    @classmethod
    def get_current_selection(cls) -> Dict[str, Any]:
        """Get current class/subject/chapter selection."""
        cls.initialize()
        return {
            'class_num': st.session_state[cls.KEY_CURRENT_CLASS],
            'subject': st.session_state[cls.KEY_CURRENT_SUBJECT],
            'chapter': st.session_state[cls.KEY_CURRENT_CHAPTER],
        }

    @classmethod
    def set_current_selection(cls, class_num: int, subject: str, chapter: int) -> None:
        """Set current class/subject/chapter selection."""
        cls.initialize()
        st.session_state[cls.KEY_CURRENT_CLASS] = class_num
        st.session_state[cls.KEY_CURRENT_SUBJECT] = subject
        st.session_state[cls.KEY_CURRENT_CHAPTER] = chapter

    @classmethod
    def get_current_page(cls) -> str:
        """Get the current page/section."""
        cls.initialize()
        return st.session_state.get(cls.KEY_CURRENT_PAGE, 'home')

    @classmethod
    def set_current_page(cls, page: str) -> None:
        """Set the current page/section."""
        cls.initialize()
        st.session_state[cls.KEY_CURRENT_PAGE] = page

    @classmethod
    def is_dirty(cls) -> bool:
        """Check if there are unsaved changes."""
        cls.initialize()
        return st.session_state.get(cls.KEY_IS_DIRTY, False)

    @classmethod
    def mark_clean(cls) -> None:
        """Mark the session as clean (saved)."""
        cls.initialize()
        st.session_state[cls.KEY_IS_DIRTY] = False
        st.session_state[cls.KEY_LAST_SAVE_TIME] = datetime.now()

    @classmethod
    def get_last_save_time(cls) -> Optional[datetime]:
        """Get the last save time."""
        cls.initialize()
        return st.session_state.get(cls.KEY_LAST_SAVE_TIME)

    @classmethod
    def is_autosave_enabled(cls) -> bool:
        """Check if autosave is enabled."""
        cls.initialize()
        return st.session_state.get(cls.KEY_AUTOSAVE_ENABLED, True)

    @classmethod
    def set_autosave_enabled(cls, enabled: bool) -> None:
        """Enable or disable autosave."""
        cls.initialize()
        st.session_state[cls.KEY_AUTOSAVE_ENABLED] = enabled

    @classmethod
    def reset(cls) -> None:
        """Reset all session state."""
        keys_to_reset = [
            cls.KEY_CHAPTER_DATA,
            cls.KEY_PART_MANAGER,
            cls.KEY_IS_DIRTY,
            cls.KEY_LAST_SAVE_TIME,
        ]
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        cls.initialize()

    @classmethod
    def export_to_json(cls) -> Optional[str]:
        """Export current chapter data to JSON string."""
        data = cls.get_chapter_data()
        if data:
            export_data = {
                'chapter_data': data.to_autosave_dict(),
                'part_manager': cls.get_part_manager().to_dict(),
                'exported_at': datetime.now().isoformat(),
            }
            return json.dumps(export_data, indent=2, ensure_ascii=False)
        return None

    @classmethod
    def import_from_json(cls, json_string: str, show_preview: bool = False) -> Dict[str, Any]:
        """
        Import chapter data from JSON string with validation.

        Args:
            json_string: JSON string containing chapter data
            show_preview: If True, validates but doesn't import (for preview)

        Returns:
            Dict with 'success', 'errors', 'warnings', 'summary' keys
        """
        from .parsers import JsonValidator

        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'summary': {},
            'data': None
        }

        # Validate JSON structure
        is_valid, parsed_data, errors = JsonValidator.validate_json_string(json_string)

        if not is_valid:
            result['errors'] = errors
            return result

        # If just previewing, return validation success and data summary
        if show_preview:
            result['success'] = True
            result['data'] = parsed_data
            if 'chapter_data' in parsed_data:
                ch = parsed_data['chapter_data']
                result['summary'] = {
                    'chapter_title': ch.get('chapter_title', 'Untitled'),
                    'chapter_number': ch.get('chapter_number', 0),
                    'subject': ch.get('subject', 'unknown'),
                    'class_num': ch.get('class_num', 10),
                    'concepts_count': len(ch.get('concepts', [])),
                    'pyq_count': len(ch.get('pyq_items', [])),
                    'mcq_count': len(ch.get('mcqs', [])),
                    'model_answers_count': len(ch.get('model_answers', []))
                }
            return result

        # Actually import the data
        try:
            if 'chapter_data' in parsed_data:
                chapter_data = ChapterData.from_autosave_dict(parsed_data['chapter_data'])
                cls.set_chapter_data(chapter_data)
            else:
                result['errors'].append("No chapter data found in file")
                return result

            if 'part_manager' in parsed_data:
                part_manager = PartManager.from_dict(parsed_data['part_manager'])
                cls.set_part_manager(part_manager)
            else:
                # Use default part manager if not provided
                cls.set_part_manager(PartManager())
                result['warnings'].append("No part configuration found, using defaults")

            # Update current selection based on imported data
            data = cls.get_chapter_data()
            if data:
                cls.set_current_selection(data.class_num, data.subject, data.chapter_number)
                result['summary'] = {
                    'chapter_title': data.chapter_title,
                    'chapter_number': data.chapter_number,
                    'subject': data.subject,
                    'class_num': data.class_num
                }

            result['success'] = True
            return result

        except ValueError as e:
            result['errors'].append(f"Data validation error: {str(e)}")
        except TypeError as e:
            result['errors'].append(f"Data type error: {str(e)}")
        except KeyError as e:
            result['errors'].append(f"Missing required field: {str(e)}")
        except Exception as e:
            result['errors'].append(f"Import failed: {str(e)}")

        return result

    @classmethod
    def get_session_info(cls) -> Dict[str, Any]:
        """Get information about the current session."""
        cls.initialize()
        data = cls.get_chapter_data()

        return {
            'has_chapter': data is not None,
            'chapter_title': data.chapter_title if data else None,
            'class_num': st.session_state[cls.KEY_CURRENT_CLASS],
            'subject': st.session_state[cls.KEY_CURRENT_SUBJECT],
            'chapter_number': st.session_state[cls.KEY_CURRENT_CHAPTER],
            'current_page': st.session_state[cls.KEY_CURRENT_PAGE],
            'is_dirty': cls.is_dirty(),
            'last_save': cls.get_last_save_time(),
            'autosave_enabled': cls.is_autosave_enabled(),
        }
