"""
Data models for Guide Book Generator.
Defines the structure of chapter data using Pydantic.
"""

from .base import ChapterData, ConceptItem, QuestionItem, PYQItem
from .parts import Part, PartManager
