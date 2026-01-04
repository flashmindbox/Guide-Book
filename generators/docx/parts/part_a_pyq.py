"""
Part A: PYQ Analysis generator for Guide Book Generator.
Generates the Previous Year Questions analysis section.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class PartAGenerator:
    """Generates Part A: PYQ Analysis."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

    def generate(self):
        """Generate Part A: PYQ Analysis."""
        # Page break
        DocxHelpers.add_page_break(self.document)

        # Part header
        self._add_part_header()

        # PYQ Table
        if self.data.pyq_items:
            self._add_pyq_table()

        # Prediction box
        if self.data.pyq_prediction:
            self._add_prediction_box()

        # Frequency legend
        self._add_frequency_legend()

        # Syllabus note
        if self.data.pyq_syllabus_note:
            self._add_syllabus_note()

    def _add_part_header(self):
        """Add the part header in a styled box - unified blue color."""
        # Create header box with neutral background
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Full title in PRIMARY_BLUE (no split coloring)
        run = para.add_run(f"Part A: PYQ Analysis ({self.data.pyq_year_range})")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        self.document.add_paragraph()  # Spacing

    def _add_pyq_table(self):
        """Add the PYQ analysis table."""
        # Convert PYQItem list to dict format for helper
        questions = []
        for item in self.data.pyq_items:
            if not item.is_empty():
                questions.append({
                    'question': item.question,
                    'marks': item.marks,
                    'years': item.years,
                })

        if questions:
            DocxHelpers.create_pyq_table(self.document, questions, self.data.pyq_year_range)
            self.document.add_paragraph(style='BodyText')  # Spacing

    def _add_prediction_box(self):
        """Add prediction box with INFO styling (blue left border)."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_INFO)
        DocxHelpers.set_cell_padding(cell, 120)

        para = cell.paragraphs[0]

        # Icon and label
        run = para.add_run(f"{Icons.TARGET} Prediction {self._get_next_year()}: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Prediction text
        run = para.add_run(self.data.pyq_prediction)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_frequency_legend(self):
        """Add frequency color legend."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(6)

        run = para.add_run("Frequency: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        # Red = 6+ times
        run = para.add_run("Red")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        run = para.add_run(" = 6+ times   ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL

        # Blue = 5 times
        run = para.add_run("Blue")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        run = para.add_run(" = 5 times   ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL

        # Green = 3-4 times
        run = para.add_run("Green")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        run = para.add_run(" = 3-4 times")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY_SMALL

        # Decorative line
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run('─' * 50)
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BORDER_NEUTRAL)

    def _add_syllabus_note(self):
        """Add syllabus note with TIP styling (green left border)."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_TIP)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_TIP)
        DocxHelpers.set_cell_padding(cell, 120)

        para = cell.paragraphs[0]

        # Star icon and label
        run = para.add_run("★ Syllabus Note: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Note text with markdown formatting
        DocxHelpers.add_formatted_text(para, self.data.pyq_syllabus_note)

    def _get_next_year(self) -> str:
        """Get the next year for prediction based on year range."""
        try:
            end_year = int(self.data.pyq_year_range.split('-')[1])
            return str(end_year + 2)  # Predict 2 years ahead
        except:
            return "2026"
