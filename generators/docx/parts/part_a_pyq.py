"""
Part A: PYQ Analysis generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartAGenerator:
    """Generates Part A: PYQ Analysis with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part A: PYQ Analysis."""
        DocxHelpers.add_page_break(self.document)

        self._add_part_header()

        if self.data.pyq_items:
            self._add_pyq_table()

        if self.data.pyq_prediction:
            self._add_prediction()

        self._add_frequency_legend()

        if self.data.pyq_syllabus_note:
            self._add_syllabus_note()

    def _add_part_header(self):
        """Add part header with light red background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)  # Light red background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run(f"Part A: PYQ Analysis ({self.data.pyq_year_range})")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)  # Red text

        self.document.add_paragraph()

    def _add_pyq_table(self):
        """Add the PYQ analysis table."""
        # Filter non-empty items
        questions = []
        for item in self.data.pyq_items:
            if not item.is_empty():
                questions.append({
                    'question': item.question,
                    'marks': item.marks,
                    'years': item.years,
                })

        if not questions:
            return

        # Create table
        table = self.document.add_table(rows=len(questions) + 1, cols=3)
        table.alignment = 1  # CENTER
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        # Set column widths
        table.columns[0].width = Inches(4.0)
        table.columns[1].width = Inches(0.75)
        table.columns[2].width = Inches(1.75)

        # Header row
        header_cells = table.rows[0].cells
        headers = ['Question', 'Marks', 'Years Asked']
        for i, header in enumerate(headers):
            cell = header_cells[i]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

        # Data rows
        for idx, q in enumerate(questions):
            row = table.rows[idx + 1]
            years = q.get('years', '')
            year_count = len([y.strip() for y in years.split(',') if y.strip()])

            # Apply row background based on frequency
            row_bg = None
            if year_count >= 6:
                row_bg = Colors.BG_WARNING  # Light red
            elif year_count == 5:
                row_bg = Colors.BG_INFO  # Light blue
            elif year_count >= 3:
                row_bg = Colors.BG_TIP  # Light green

            # Question cell
            cell = row.cells[0]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(q.get('question', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

            # Marks cell
            cell = row.cells[1]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(str(q.get('marks', '')))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

            # Years cell
            cell = row.cells[2]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(years)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

        self.document.add_paragraph()  # Spacing

    def _add_prediction(self):
        """Add prediction as simple text."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run(f"🎯 Prediction {self._get_next_year()}: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        run = para.add_run(self.data.pyq_prediction)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

    def _add_frequency_legend(self):
        """Add frequency color legend."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run("Frequency: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True

        run = para.add_run("Red")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        run = para.add_run(" = 6+ times   ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

        run = para.add_run("Blue")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        run = para.add_run(" = 5 times   ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

        run = para.add_run("Green")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        run = para.add_run(" = 3-4 times")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

    def _add_syllabus_note(self):
        """Add syllabus note as simple text."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run("★ Syllabus Note: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        run = para.add_run(self.data.pyq_syllabus_note)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

    def _get_next_year(self) -> str:
        """Get the next year for prediction."""
        try:
            end_year = int(self.data.pyq_year_range.split('-')[1])
            return str(end_year + 1)
        except (ValueError, IndexError, AttributeError):
            return "2025"
