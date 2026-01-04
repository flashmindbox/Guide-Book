"""
Unified Content Builder for Guide Book Generator.
Creates an abstract document representation that can be rendered to HTML or DOCX.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from core.models.base import ChapterData
from core.models.parts import PartManager


class ElementType(Enum):
    """Types of document elements."""
    HEADER = "header"
    TITLE = "title"
    SUBTITLE = "subtitle"
    DECORATIVE_LINE = "decorative_line"
    METADATA_TABLE = "metadata_table"
    ALERT_BOX = "alert_box"
    INFO_BOX = "info_box"
    TIP_BOX = "tip_box"
    NEUTRAL_BOX = "neutral_box"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    TABLE = "table"
    PART_HEADER = "part_header"
    SECTION_TITLE = "section_title"
    CONCEPT_BOX = "concept_box"
    QUESTION_BLOCK = "question_block"
    MCQ_BLOCK = "mcq_block"
    ANSWER_BLOCK = "answer_block"
    TIMELINE = "timeline"
    QR_CODES = "qr_codes"
    PAGE_BREAK = "page_break"
    DIVIDER = "divider"
    END_MARKER = "end_marker"


class BoxType(Enum):
    """Types of styled boxes."""
    WARNING = "warning"
    INFO = "info"
    TIP = "tip"
    NEUTRAL = "neutral"


@dataclass
class Element:
    """A single document element."""
    type: ElementType
    content: Any = None
    style: Optional[Dict[str, Any]] = None
    children: List['Element'] = field(default_factory=list)

    def add_child(self, element: 'Element'):
        self.children.append(element)


@dataclass
class TextRun:
    """A run of text with optional formatting."""
    text: str
    bold: bool = False
    italic: bool = False
    color: Optional[str] = None
    size: Optional[int] = None


class ContentBuilder:
    """
    Builds an abstract document representation from ChapterData.
    This representation can then be rendered to HTML or DOCX.
    """

    def __init__(self, data: ChapterData, part_manager: PartManager):
        self.data = data
        self.part_manager = part_manager
        self.elements: List[Element] = []

    def build_full_document(self) -> List[Element]:
        """Build the complete document structure."""
        self.elements = []

        # Cover page
        self._build_cover_page()

        # Parts
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            self._build_part(part.id)

        # End marker
        self.elements.append(Element(ElementType.DIVIDER))
        self.elements.append(Element(
            ElementType.END_MARKER,
            content=f"End of Chapter {self.data.chapter_number}"
        ))

        return self.elements

    def build_cover_only(self) -> List[Element]:
        """Build only the cover page."""
        self.elements = []
        self._build_cover_page()
        return self.elements

    def build_part_only(self, part_id: str) -> List[Element]:
        """Build a specific part only."""
        self.elements = []
        self._build_part(part_id)
        return self.elements

    def _build_cover_page(self):
        """Build the cover page elements."""
        # Header
        subject_display = self.data.subject.replace('_', ' ').title()
        header_text = f"CBSE Class {self.data.class_num} | Social Science | {subject_display}"
        self.elements.append(Element(ElementType.HEADER, content=header_text))

        # Decorative line
        self.elements.append(Element(ElementType.DECORATIVE_LINE))

        # Chapter number and title
        self.elements.append(Element(
            ElementType.TITLE,
            content={
                'chapter_num': f"CHAPTER {self.data.chapter_number}",
                'title': self.data.chapter_title,
                'subtitle': self.data.subtitle
            }
        ))

        # Decorative line
        self.elements.append(Element(ElementType.DECORATIVE_LINE))

        # Metadata table
        self.elements.append(Element(
            ElementType.METADATA_TABLE,
            content={
                'Weightage': {'value': self.data.weightage, 'highlight': False},
                'Map Work': {'value': self.data.map_work, 'highlight': False},
                'Importance': {'value': self.data.importance, 'highlight': self.data.importance == 'High'},
                'PYQ Frequency': {'value': self.data.pyq_frequency, 'highlight': self.data.pyq_frequency == 'Every Year'},
            }
        ))

        # Syllabus alert
        if self.data.syllabus_alert_enabled and self.data.syllabus_alert_text:
            self.elements.append(Element(
                ElementType.ALERT_BOX,
                content={
                    'title': 'SYLLABUS ALERT',
                    'text': self.data.syllabus_alert_text,
                    'type': BoxType.WARNING
                }
            ))

        # Learning objectives
        if self.data.learning_objectives:
            objectives = [obj.strip().lstrip('-•* ') for obj in self.data.learning_objectives.strip().split('\n') if obj.strip()]
            self.elements.append(Element(
                ElementType.INFO_BOX,
                content={
                    'title': 'Learning Objectives',
                    'subtitle': 'After studying this chapter, you will be able to:',
                    'items': objectives,
                    'type': BoxType.INFO
                }
            ))

        # Chapter contents
        enabled_parts = self.part_manager.get_enabled_parts()
        contents = []
        for part in enabled_parts:
            description = self.data.part_descriptions.get(part.id, part.description)
            contents.append({
                'label': f"Part {part.id}",
                'description': description
            })

        self.elements.append(Element(
            ElementType.NEUTRAL_BOX,
            content={
                'title': 'Chapter Contents',
                'items': contents,
                'type': BoxType.NEUTRAL
            }
        ))

        # QR codes
        if self.data.qr_practice_questions_url or self.data.qr_practice_with_answers_url:
            self.elements.append(Element(
                ElementType.QR_CODES,
                content={
                    'practice_url': self.data.qr_practice_questions_url,
                    'answers_url': self.data.qr_practice_with_answers_url
                }
            ))

    def _build_part(self, part_id: str):
        """Build elements for a specific part."""
        builders = {
            'A': self._build_part_a,
            'B': self._build_part_b,
            'C': self._build_part_c,
            'D': self._build_part_d,
            'E': self._build_part_e,
            'F': self._build_part_f,
            'G': self._build_part_g,
        }

        builder = builders.get(part_id.upper())
        if builder:
            builder()

    def _build_part_a(self):
        """Build Part A: PYQ Analysis."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'A', 'name': 'PYQ Analysis'}
        ))

        # PYQ Table
        if self.data.pyq_items:
            rows = []
            for item in self.data.pyq_items:
                if not item.is_empty():
                    rows.append({
                        'question': item.question,
                        'marks': item.marks,
                        'years': item.years
                    })

            if rows:
                self.elements.append(Element(
                    ElementType.TABLE,
                    content={
                        'headers': ['Question', 'Marks', 'Years Asked'],
                        'rows': rows,
                        'type': 'pyq'
                    }
                ))

        # Prediction
        if self.data.pyq_prediction:
            self.elements.append(Element(
                ElementType.INFO_BOX,
                content={
                    'title': 'Prediction',
                    'text': self.data.pyq_prediction,
                    'type': BoxType.INFO
                }
            ))

        # Syllabus note
        if self.data.pyq_syllabus_note:
            self.elements.append(Element(
                ElementType.ALERT_BOX,
                content={
                    'title': 'Syllabus Note',
                    'text': self.data.pyq_syllabus_note,
                    'type': BoxType.WARNING
                }
            ))

    def _build_part_b(self):
        """Build Part B: Key Concepts."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'B', 'name': 'Key Concepts'}
        ))

        # Concepts
        for i, concept in enumerate(self.data.concepts):
            if not concept.is_empty():
                self.elements.append(Element(
                    ElementType.CONCEPT_BOX,
                    content={
                        'number': concept.number or (i + 1),
                        'title': concept.title,
                        'content': concept.content,
                        'ncert_line': concept.ncert_line,
                        'memory_trick': concept.memory_trick,
                        'did_you_know': concept.did_you_know
                    }
                ))

        # Important dates
        if self.data.important_dates:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Important Dates"
            ))
            self.elements.append(Element(
                ElementType.TIMELINE,
                content=self.data.important_dates
            ))

        # Common mistakes
        if self.data.common_mistakes:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Common Mistakes to Avoid"
            ))
            self.elements.append(Element(
                ElementType.BULLET_LIST,
                content=self.data.common_mistakes
            ))

    def _build_part_c(self):
        """Build Part C: Model Answers."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'C', 'name': 'Model Answers'}
        ))

        for i, answer in enumerate(self.data.model_answers):
            if not answer.is_empty():
                self.elements.append(Element(
                    ElementType.ANSWER_BLOCK,
                    content={
                        'number': i + 1,
                        'question': answer.question,
                        'marks': answer.marks,
                        'answer': answer.answer,
                        'marking_points': answer.marking_points
                    }
                ))

        # Examiner tips
        if self.data.examiner_tips:
            self.elements.append(Element(
                ElementType.TIP_BOX,
                content={
                    'title': 'Examiner Tips',
                    'text': self.data.examiner_tips,
                    'type': BoxType.TIP
                }
            ))

    def _build_part_d(self):
        """Build Part D: Practice Questions."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'D', 'name': 'Practice Questions'}
        ))

        # MCQs
        if self.data.mcqs:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Multiple Choice Questions (MCQs)"
            ))
            for i, mcq in enumerate(self.data.mcqs):
                if not mcq.is_empty():
                    self.elements.append(Element(
                        ElementType.MCQ_BLOCK,
                        content={
                            'number': i + 1,
                            'question': mcq.question,
                            'options': mcq.options or [],
                            'answer': mcq.answer,
                            'marks': mcq.marks
                        }
                    ))

        # Assertion-Reason
        if self.data.assertion_reason:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Assertion-Reason Questions"
            ))
            for i, ar in enumerate(self.data.assertion_reason):
                if not ar.is_empty():
                    self.elements.append(Element(
                        ElementType.QUESTION_BLOCK,
                        content={
                            'number': i + 1,
                            'question': ar.question,
                            'marks': ar.marks,
                            'type': 'assertion_reason'
                        }
                    ))

        # Short Answer
        if self.data.short_answer:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Short Answer Questions"
            ))
            for i, sa in enumerate(self.data.short_answer):
                if not sa.is_empty():
                    self.elements.append(Element(
                        ElementType.QUESTION_BLOCK,
                        content={
                            'number': i + 1,
                            'question': sa.question,
                            'marks': sa.marks,
                            'hint': sa.hint,
                            'type': 'short_answer'
                        }
                    ))

        # Long Answer
        if self.data.long_answer:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Long Answer Questions"
            ))
            for i, la in enumerate(self.data.long_answer):
                if not la.is_empty():
                    self.elements.append(Element(
                        ElementType.QUESTION_BLOCK,
                        content={
                            'number': i + 1,
                            'question': la.question,
                            'marks': la.marks,
                            'hint': la.hint,
                            'type': 'long_answer'
                        }
                    ))

        # HOTS
        if self.data.hots:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Higher Order Thinking Skills (HOTS)"
            ))
            for i, hots in enumerate(self.data.hots):
                if not hots.is_empty():
                    self.elements.append(Element(
                        ElementType.QUESTION_BLOCK,
                        content={
                            'number': i + 1,
                            'question': hots.question,
                            'marks': hots.marks,
                            'hint': hots.hint,
                            'type': 'hots'
                        }
                    ))

    def _build_part_e(self):
        """Build Part E: Map Work."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'E', 'name': 'Map Work'}
        ))

        if self.data.map_work_na:
            self.elements.append(Element(
                ElementType.PARAGRAPH,
                content="Map work is not applicable for this chapter."
            ))
        else:
            # Map items
            if self.data.map_items:
                self.elements.append(Element(
                    ElementType.SECTION_TITLE,
                    content="Locations to Mark"
                ))
                self.elements.append(Element(
                    ElementType.NUMBERED_LIST,
                    content=self.data.map_items
                ))

            # Map tips
            if self.data.map_tips:
                self.elements.append(Element(
                    ElementType.TIP_BOX,
                    content={
                        'title': 'Map Work Tips',
                        'text': self.data.map_tips,
                        'type': BoxType.TIP
                    }
                ))

    def _build_part_f(self):
        """Build Part F: Quick Revision."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'F', 'name': 'Quick Revision'}
        ))

        # Key points
        if self.data.revision_key_points:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Key Points"
            ))
            self.elements.append(Element(
                ElementType.BULLET_LIST,
                content=self.data.revision_key_points
            ))

        # Key terms
        if self.data.revision_key_terms:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Key Terms"
            ))
            self.elements.append(Element(
                ElementType.TABLE,
                content={
                    'headers': ['Term', 'Definition'],
                    'rows': self.data.revision_key_terms,
                    'type': 'terms'
                }
            ))

        # Timeline
        if self.data.revision_timeline:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Timeline"
            ))
            self.elements.append(Element(
                ElementType.TIMELINE,
                content=self.data.revision_timeline
            ))

        # Memory tricks
        if self.data.revision_memory_tricks:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Memory Tricks"
            ))
            for trick in self.data.revision_memory_tricks:
                self.elements.append(Element(
                    ElementType.TIP_BOX,
                    content={
                        'title': 'Memory Trick',
                        'text': trick,
                        'type': BoxType.TIP
                    }
                ))

    def _build_part_g(self):
        """Build Part G: Exam Strategy."""
        self.elements.append(Element(ElementType.PAGE_BREAK))
        self.elements.append(Element(
            ElementType.PART_HEADER,
            content={'id': 'G', 'name': 'Exam Strategy'}
        ))

        # Time allocation
        if self.data.time_allocation:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Time Allocation"
            ))
            self.elements.append(Element(
                ElementType.TABLE,
                content={
                    'headers': ['Question Type', 'Marks', 'Time'],
                    'rows': self.data.time_allocation,
                    'type': 'time_allocation'
                }
            ))

        # Common mistakes
        if self.data.common_mistakes_exam:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Common Mistakes to Avoid"
            ))
            self.elements.append(Element(
                ElementType.TABLE,
                content={
                    'headers': ['Mistake', 'Correction'],
                    'rows': self.data.common_mistakes_exam,
                    'type': 'mistakes'
                }
            ))

        # Pro tips
        if self.data.examiner_pro_tips:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Examiner Pro Tips"
            ))
            self.elements.append(Element(
                ElementType.BULLET_LIST,
                content=self.data.examiner_pro_tips
            ))

        # Self-assessment checklist
        if self.data.self_assessment_checklist:
            self.elements.append(Element(
                ElementType.SECTION_TITLE,
                content="Self-Assessment Checklist"
            ))
            self.elements.append(Element(
                ElementType.BULLET_LIST,
                content=[f"☐ {item}" for item in self.data.self_assessment_checklist]
            ))
