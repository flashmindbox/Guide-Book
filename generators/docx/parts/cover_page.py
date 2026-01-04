"""
Cover page generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from core.models.parts import PartManager
from styles.theme import Colors, Fonts
from ..helpers import DocxHelpers


class CoverPageGenerator:
    """Generates a clean, simplified cover page."""

    def __init__(self, document: Document, data: ChapterData, part_manager: PartManager):
        self.document = document
        self.data = data
        self.part_manager = part_manager

    def generate(self):
        """Generate the complete cover page."""
        self._add_header()
        self._add_separator()
        self._add_chapter_title()
        self._add_separator()
        self._add_metadata()

        if self.data.syllabus_alert_enabled and self.data.syllabus_alert_text:
            self._add_syllabus_alert()

        if self.data.learning_objectives:
            self._add_learning_objectives()

        self._add_chapter_contents()

    def _add_header(self):
        """Add simple centered header."""
        subject_display = self.data.subject.replace('_', ' ').title()
        header_text = f"CBSE Class {self.data.class_num} | Social Science | {subject_display}"

        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run(header_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    def _add_separator(self):
        """Add a clean horizontal line."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(3)
        para.paragraph_format.space_after = Pt(3)
        run = para.add_run('━' * 40)
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

    def _add_chapter_title(self):
        """Add chapter number and title."""
        # Chapter number
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run(f"CHAPTER {self.data.chapter_number}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Chapter title
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(12)
        run = para.add_run(self.data.chapter_title)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Subtitle if present
        if self.data.subtitle:
            para = self.document.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(self.data.subtitle)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(12)
            run.font.italic = True

    def _add_metadata(self):
        """Add metadata as simple inline text."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(12)

        # Weightage
        run = para.add_run("Weightage: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True

        run = para.add_run(f"{self.data.weightage}  |  ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Map Work
        run = para.add_run("Map Work: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True

        run = para.add_run(f"{self.data.map_work}  |  ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

        # Importance
        run = para.add_run("Importance: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True

        importance_color = Colors.ACCENT_RED if self.data.importance == 'High' else Colors.BODY_TEXT
        run = para.add_run(f"{self.data.importance}  |  ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(importance_color)

        # PYQ Frequency
        run = para.add_run("PYQ: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True

        freq_color = Colors.ACCENT_RED if self.data.pyq_frequency == 'Every Year' else Colors.BODY_TEXT
        run = para.add_run(self.data.pyq_frequency)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(freq_color)

    def _add_syllabus_alert(self):
        """Add syllabus alert as simple highlighted text."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run("⚠ SYLLABUS NOTE: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        run = para.add_run(self.data.syllabus_alert_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

    def _add_learning_objectives(self):
        """Add learning objectives as a simple bulleted list."""
        objectives = [obj.strip() for obj in self.data.learning_objectives.strip().split('\n') if obj.strip()]

        # Clean up bullets/dashes
        clean_objectives = []
        for obj in objectives:
            if obj.startswith(('-', '•', '*')):
                obj = obj[1:].strip()
            clean_objectives.append(obj)

        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run("🎯 Learning Objectives")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Subtitle
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run("After studying this chapter, you will be able to:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True

        # Bullet points
        for obj in clean_objectives:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)
            run = para.add_run(f"• {obj}")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_chapter_contents(self):
        """Add chapter contents as a simple list."""
        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run("📑 Chapter Contents")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

        # List enabled parts
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            description = self.data.part_descriptions.get(part.id, part.description)

            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"Part {part.id}: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            run = para.add_run(description)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
