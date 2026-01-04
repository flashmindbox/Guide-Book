"""
Base data models for Guide Book Generator.
Defines the structure of chapter data using Pydantic.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ConceptItem(BaseModel):
    """A single concept/topic in Part B."""
    number: int = Field(default=1, ge=1)
    title: str = Field(default="")
    content: str = Field(default="")
    ncert_line: Optional[str] = Field(default=None, description="NCERT exact line quote")
    memory_trick: Optional[str] = Field(default=None)
    did_you_know: Optional[str] = Field(default=None)

    def is_empty(self) -> bool:
        return not self.title and not self.content

    def word_count(self) -> int:
        return len(self.content.split()) if self.content else 0


class PYQItem(BaseModel):
    """A Previous Year Question item for Part A."""
    question: str = Field(default="")
    marks: str = Field(default="3M")
    years: str = Field(default="")  # Comma-separated years like "2020, 2021, 2023"

    def get_year_count(self) -> int:
        if not self.years:
            return 0
        return len([y.strip() for y in self.years.split(',') if y.strip()])

    def is_empty(self) -> bool:
        return not self.question


class QuestionItem(BaseModel):
    """A question item for Part D."""
    question: str = Field(default="")
    marks: int = Field(default=1, ge=1)
    difficulty: str = Field(default="M")  # E, M, H
    options: Optional[List[str]] = Field(default=None)  # For MCQs: [a, b, c, d]
    answer: Optional[str] = Field(default=None)
    hint: Optional[str] = Field(default=None)

    def is_empty(self) -> bool:
        return not self.question


class ModelAnswer(BaseModel):
    """A model answer item for Part C."""
    question: str = Field(default="")
    marks: int = Field(default=3)
    answer: str = Field(default="")
    marking_points: Optional[List[str]] = Field(default=None)

    def is_empty(self) -> bool:
        return not self.question and not self.answer


class PartData(BaseModel):
    """Data for a single part (A-G or custom)."""
    id: str
    name: str
    enabled: bool = True
    content: Dict[str, Any] = Field(default_factory=dict)


class ChapterData(BaseModel):
    """Complete data model for a chapter."""

    # =========================================================================
    # METADATA
    # =========================================================================
    class_num: int = Field(default=10, ge=9, le=12)
    subject: str = Field(default="history")
    chapter_number: int = Field(default=1, ge=1)
    chapter_title: str = Field(default="")
    subtitle: Optional[str] = Field(default=None)

    # Chapter metadata
    weightage: str = Field(default="4-5 Marks")
    map_work: str = Field(default="No")  # Yes/No
    importance: str = Field(default="High")
    pyq_frequency: str = Field(default="Every Year")

    # Syllabus Alert
    syllabus_alert_enabled: bool = Field(default=False)
    syllabus_alert_text: str = Field(default="")

    # Learning Objectives
    learning_objectives: str = Field(default="")

    # QR Codes for downloadable resources
    qr_practice_questions_url: Optional[str] = Field(default=None, description="URL for Practice Questions PDF")
    qr_practice_with_answers_url: Optional[str] = Field(default=None, description="URL for Practice Questions with Answers PDF")

    # =========================================================================
    # PART DESCRIPTIONS (for cover page)
    # =========================================================================
    part_descriptions: Dict[str, str] = Field(default_factory=lambda: {
        'A': '10-year data with predictions and syllabus note',
        'B': 'Core topics with memory tricks and exam-focused explanations',
        'C': 'Examiner-approved answers with marking scheme',
        'D': 'MCQs, AR, SA, LA, HOTS, CBQs with answer hints',
        'E': 'CBSE prescribed locations and marking tips',
        'F': 'One-page summary, memory tricks compilation, key dates',
        'G': 'Time management, marking scheme insights, last-minute tips',
    })

    # =========================================================================
    # PART A: PYQ ANALYSIS
    # =========================================================================
    pyq_year_range: str = Field(default="2015-2024")
    pyq_items: List[PYQItem] = Field(default_factory=list)
    pyq_prediction: str = Field(default="")
    pyq_syllabus_note: Optional[str] = Field(default=None)

    # =========================================================================
    # PART B: KEY CONCEPTS
    # =========================================================================
    concepts: List[ConceptItem] = Field(default_factory=lambda: [ConceptItem(number=1)])
    comparison_tables: List[Dict[str, Any]] = Field(default_factory=list)
    common_mistakes: List[str] = Field(default_factory=list)
    important_dates: List[Dict[str, str]] = Field(default_factory=list)  # [{year, event}]

    # =========================================================================
    # PART C: MODEL ANSWERS
    # =========================================================================
    model_answers: List[ModelAnswer] = Field(default_factory=list)
    examiner_tips: Optional[str] = Field(default=None)

    # =========================================================================
    # PART D: PRACTICE QUESTIONS
    # =========================================================================
    mcqs: List[QuestionItem] = Field(default_factory=list)
    assertion_reason: List[QuestionItem] = Field(default_factory=list)
    source_based: List[Dict[str, Any]] = Field(default_factory=list)
    case_study: List[Dict[str, Any]] = Field(default_factory=list)
    picture_based: List[Dict[str, Any]] = Field(default_factory=list)
    short_answer: List[QuestionItem] = Field(default_factory=list)
    long_answer: List[QuestionItem] = Field(default_factory=list)
    hots: List[QuestionItem] = Field(default_factory=list)
    value_based: List[QuestionItem] = Field(default_factory=list)
    competency_based: List[QuestionItem] = Field(default_factory=list)

    # =========================================================================
    # PART E: MAP WORK
    # =========================================================================
    map_work_na: bool = Field(default=False)
    map_items: List[str] = Field(default_factory=list)
    map_image_path: Optional[str] = Field(default=None)
    map_tips: Optional[str] = Field(default=None)

    # =========================================================================
    # PART F: QUICK REVISION
    # =========================================================================
    revision_key_points: List[str] = Field(default_factory=list)
    revision_key_terms: List[Dict[str, str]] = Field(default_factory=list)  # [{term, definition}]
    revision_timeline: List[Dict[str, str]] = Field(default_factory=list)  # [{year, event}]
    revision_memory_tricks: List[str] = Field(default_factory=list)

    # =========================================================================
    # PART G: EXAM STRATEGY
    # =========================================================================
    time_allocation: List[Dict[str, str]] = Field(default_factory=list)  # [{type, marks, time}]
    common_mistakes_exam: List[Dict[str, str]] = Field(default_factory=list)  # [{mistake, correction}]
    examiner_pro_tips: List[str] = Field(default_factory=list)
    self_assessment_checklist: List[str] = Field(default_factory=list)

    # =========================================================================
    # ENABLED PARTS (for dynamic part management)
    # =========================================================================
    enabled_parts: List[str] = Field(default_factory=lambda: ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    custom_parts: List[PartData] = Field(default_factory=list)

    # =========================================================================
    # QR CODES
    # =========================================================================
    qr_practice_url: Optional[str] = Field(default=None)
    qr_answers_url: Optional[str] = Field(default=None)

    # =========================================================================
    # PAGE SETTINGS
    # =========================================================================
    page_size: str = Field(default="A4")
    add_page_numbers: bool = Field(default=True)
    page_number_position: str = Field(default="Bottom Center")

    # =========================================================================
    # TIMESTAMPS
    # =========================================================================
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # =========================================================================
    # METHODS
    # =========================================================================

    def get_header_text(self) -> str:
        """Get the header text for the document."""
        subject_display = self.subject.replace('_', ' ').title()
        return f"CBSE Class {self.class_num} | Social Science | {subject_display}"

    def get_full_title(self) -> str:
        """Get the full chapter title."""
        return f"Chapter {self.chapter_number}: {self.chapter_title}"

    def is_map_work_applicable(self) -> bool:
        """Check if map work is applicable for this chapter."""
        return self.map_work == "Yes" and not self.map_work_na

    def get_enabled_part_ids(self) -> List[str]:
        """Get list of enabled part IDs in order."""
        # Standard parts that are enabled
        standard = [p for p in ['A', 'B', 'C', 'D', 'E', 'F', 'G'] if p in self.enabled_parts]
        # Custom parts
        custom = [p.id for p in self.custom_parts if p.enabled]
        return standard + custom

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def to_autosave_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for autosave."""
        return self.model_dump(mode='json')

    @classmethod
    def from_autosave_dict(cls, data: Dict[str, Any]) -> 'ChapterData':
        """Create instance from autosave dictionary."""
        return cls.model_validate(data)

    def calculate_completion(self) -> Dict[str, float]:
        """
        Calculate completion percentage for each section.
        Returns dict with section names as keys and 0-100 percentages as values.
        """
        completion = {}

        # Cover page completion
        cover_fields = [self.chapter_title, self.learning_objectives]
        cover_filled = sum(1 for f in cover_fields if f)
        completion['cover'] = (cover_filled / len(cover_fields)) * 100

        # Part A: PYQ
        if self.pyq_items:
            completion['part_a'] = 100
        else:
            completion['part_a'] = 0

        # Part B: Concepts
        non_empty_concepts = [c for c in self.concepts if not c.is_empty()]
        completion['part_b'] = min(100, len(non_empty_concepts) * 20)  # 5 concepts = 100%

        # Part C: Model Answers
        non_empty_answers = [a for a in self.model_answers if not a.is_empty()]
        completion['part_c'] = min(100, len(non_empty_answers) * 20)

        # Part D: Practice Questions
        total_questions = (
            len(self.mcqs) + len(self.short_answer) + len(self.long_answer) +
            len(self.assertion_reason) + len(self.hots)
        )
        completion['part_d'] = min(100, total_questions * 5)

        # Part E: Map Work
        if self.map_work_na or self.map_items or self.map_image_path:
            completion['part_e'] = 100
        else:
            completion['part_e'] = 0

        # Part F: Quick Revision
        revision_items = len(self.revision_key_points) + len(self.revision_key_terms)
        completion['part_f'] = min(100, revision_items * 10)

        # Part G: Exam Strategy
        strategy_items = len(self.examiner_pro_tips) + len(self.self_assessment_checklist)
        completion['part_g'] = min(100, strategy_items * 20)

        # Overall completion
        enabled_parts = self.get_enabled_part_ids()
        part_completions = [completion.get(f'part_{p.lower()}', 0) for p in enabled_parts]
        part_completions.append(completion['cover'])
        completion['overall'] = sum(part_completions) / len(part_completions) if part_completions else 0

        return completion
