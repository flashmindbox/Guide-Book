"""
Part C: Model Answers generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartCGenerator:
    """Generates Part C: Model Answers with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part C: Model Answers."""
        DocxHelpers.add_page_break(self.document)

        self._add_part_header()

        # Each model answer
        for idx, answer in enumerate(self.data.model_answers, 1):
            if not answer.is_empty():
                self._add_model_answer(idx, answer)

        # Examiner's tips
        if self.data.examiner_tips:
            self._add_examiner_tips()

    def _add_part_header(self):
        """Add simple part header."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(12)

        run = para.add_run("Part C: Model Answers")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Subtitle
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(12)
        run = para.add_run("Model Answers with Examiner's Marking Scheme")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.italic = True

    def _add_model_answer(self, num: int, answer):
        """Add a single model answer with clean formatting."""
        # Question header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run(f"Q{num}. ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        DocxHelpers.add_formatted_text(para, answer.question)

        # Marks badge
        run = para.add_run(f" [{answer.marks}M]")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Answer label
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(3)
        run = para.add_run("📝 Model Answer:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Answer content with marking points
        if answer.marking_points:
            for point in answer.marking_points:
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.25)
                para.paragraph_format.space_after = Pt(2)

                # Green checkmark
                run = para.add_run("✓ ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(11)
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

                DocxHelpers.add_formatted_text(para, point)

                # Mark indication
                run = para.add_run(" (1 mark)")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(9)
                run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)
        else:
            # Plain answer
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            DocxHelpers.add_formatted_text(para, answer.answer)

    def _add_examiner_tips(self):
        """Add examiner's marking scheme tips."""
        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("🎯 Examiner's Marking Scheme")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for tip in self.data.examiner_tips.split('\n'):
            tip = tip.strip()
            if tip:
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.25)
                para.paragraph_format.space_after = Pt(3)

                run = para.add_run("• ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(11)

                DocxHelpers.add_formatted_text(para, tip)
