"""
Part C: Model Answers generator for Guide Book Generator.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class PartCGenerator:
    """Generates Part C: Model Answers."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

    def generate(self):
        """Generate Part C: Model Answers."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Subtitle
        para = self.document.add_paragraph()
        run = para.add_run("Model Answers with Examiner's Marking Scheme")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        self.document.add_paragraph()  # Spacing

        # Each model answer
        for idx, answer in enumerate(self.data.model_answers, 1):
            if not answer.is_empty():
                self._add_model_answer(idx, answer)

        # Examiner's tips
        if self.data.examiner_tips:
            self._add_examiner_tips()

    def _add_part_header(self):
        """Add the part header - unified blue color."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]

        # Full title in PRIMARY_BLUE
        run = para.add_run("Part C: Model Answers")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        self.document.add_paragraph()  # Spacing

    def _add_model_answer(self, num: int, answer):
        """Add a single model answer with NEUTRAL box styling."""
        # Question box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        # Question
        para = cell.paragraphs[0]
        run = para.add_run(f"Q{num}. ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        DocxHelpers.add_formatted_text(para, answer.question)

        # Marks in accent red brackets
        run = para.add_run(f" [{answer.marks}M]")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Answer label
        para = cell.add_paragraph()
        run = para.add_run("Model Answer:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Answer content with marking points
        if answer.marking_points:
            for point in answer.marking_points:
                para = cell.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.25)

                # Green checkmark
                run = para.add_run(f"{Icons.CORRECT} ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

                DocxHelpers.add_formatted_text(para, point)

                # Mark indication in accent red
                run = para.add_run(" (1 mark)")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY_SMALL
                run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)
        else:
            # Plain answer
            para = cell.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            DocxHelpers.add_formatted_text(para, answer.answer)

        self.document.add_paragraph()  # Spacing

    def _add_examiner_tips(self):
        """Add examiner's marking scheme tips with INFO styling."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_INFO)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.TARGET} Examiner's Marking Scheme")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        for tip in self.data.examiner_tips.split('\n'):
            tip = tip.strip()
            if tip:
                para = cell.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.15)
                run = para.add_run("• ")
                run.font.name = Fonts.PRIMARY
                DocxHelpers.add_formatted_text(para, tip)

    def _roman(self, num: int) -> str:
        """Convert number to roman numeral."""
        roman_map = [(1, 'i'), (4, 'iv'), (5, 'v'), (9, 'ix'), (10, 'x')]
        result = ''
        for value, numeral in reversed(roman_map):
            while num >= value:
                result += numeral
                num -= value
        return result
