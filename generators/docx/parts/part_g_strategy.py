"""
Part G: Exam Strategy generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartGGenerator:
    """Generates Part G: Exam Strategy with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part G: Exam Strategy."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Time Allocation Guide
        if self.data.time_allocation:
            self._add_time_allocation()

        # What Loses Marks (Common Mistakes)
        if self.data.common_mistakes_exam:
            self._add_common_mistakes()

        # Examiner's Pro Tips
        if self.data.examiner_pro_tips:
            self._add_pro_tips()

        # Self-Assessment Checklist
        if self.data.self_assessment_checklist:
            self._add_checklist()

        # End of chapter marker
        self._add_end_marker()

    def _add_part_header(self):
        """Add simple part header."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(12)

        run = para.add_run("Part G: Exam Strategy")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

    def _add_time_allocation(self):
        """Add time allocation guide table."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("⏱ Time Allocation Guide")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create table
        table = self.document.add_table(rows=1, cols=3)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(2.5)
        table.columns[1].width = Inches(1.5)
        table.columns[2].width = Inches(2.5)

        # Header row
        header_row = table.rows[0]
        headers = ['Question Type', 'Marks', 'Time']

        for idx, header in enumerate(headers):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Data rows
        for item in self.data.time_allocation:
            row = table.add_row()

            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(item.get('type', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(item.get('marks', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            cell = row.cells[2]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(item.get('time', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_common_mistakes(self):
        """Add what loses marks section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("⚠ What Loses Marks — Examiner's Warning")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Create two-column table
        table = self.document.add_table(rows=1, cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(3.25)
        table.columns[1].width = Inches(3.25)

        # Header row
        header_row = table.rows[0]

        cell = header_row.cells[0]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        run = para.add_run("❌ MISTAKE")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        cell = header_row.cells[1]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        run = para.add_run("✓ WHAT TO DO INSTEAD")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Data rows
        for item in self.data.common_mistakes_exam:
            row = table.add_row()

            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            mistake = item.get('mistake', '')
            run = para.add_run(mistake)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            correction = item.get('correction', '')
            run = para.add_run(correction)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

    def _add_pro_tips(self):
        """Add examiner's pro tips - right-aligned, green, italic."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("💡 Examiner's Pro Tips (What Gets EXTRA Marks)")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        for tip in self.data.examiner_pro_tips:
            para = self.document.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            para.paragraph_format.space_after = Pt(6)

            run = para.add_run("✓ ")
            run.font.name = Fonts.PRIMARY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

            run = para.add_run(tip)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

    def _add_checklist(self):
        """Add self-assessment checklist."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("☑ Self-Assessment Checklist")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for item in self.data.self_assessment_checklist:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run("☐ ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            run = para.add_run(item)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_end_marker(self):
        """Add end of chapter marker."""
        # Decorative line
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(24)
        run = para.add_run('━' * 40)
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # End message
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(6)

        run = para.add_run(f"⭐ End of Chapter {self.data.chapter_number} ⭐")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)
