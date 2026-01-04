"""
Part G: Exam Strategy generator for Guide Book Generator.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class PartGGenerator:
    """Generates Part G: Exam Strategy."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

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
        run = para.add_run("Part G: Exam Strategy")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        self.document.add_paragraph()  # Spacing

    def _add_time_allocation(self):
        """Add time allocation guide table."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.CLOCK} Time Allocation Guide")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

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
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_TABLE_HEADER
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Data rows with alternating background
        for idx, item in enumerate(self.data.time_allocation):
            row = table.add_row()

            cell = row.cells[0]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(item.get('type', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

            cell = row.cells[1]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(item.get('marks', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

            cell = row.cells[2]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(item.get('time', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_common_mistakes(self):
        """Add what loses marks table with WARNING styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.WRONG} What Loses Marks — Examiner's Warning")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Warning message box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_WARNING)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        run = para.add_run("These mistakes cost students marks every exam. Avoid them!")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        self.document.add_paragraph()  # Small spacing

        # Create two-column table
        table = self.document.add_table(rows=1, cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(3.25)
        table.columns[1].width = Inches(3.25)

        # Header row
        header_row = table.rows[0]

        cell = header_row.cells[0]
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_padding(cell, 80)
        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.WRONG} MISTAKE")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_TABLE_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        cell = header_row.cells[1]
        DocxHelpers.set_cell_background(cell, Colors.BG_TIP)
        DocxHelpers.set_cell_padding(cell, 80)
        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.CORRECT} WHAT TO DO INSTEAD")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_TABLE_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Data rows with alternating background
        for idx, item in enumerate(self.data.common_mistakes_exam):
            row = table.add_row()

            cell = row.cells[0]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]

            mistake = item.get('mistake', '')
            run = para.add_run(mistake)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY_SMALL
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            cell = row.cells[1]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]

            correction = item.get('correction', '')
            run = para.add_run(correction)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY_SMALL
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_pro_tips(self):
        """Add examiner's pro tips with TIP styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.TIP} Examiner's Pro Tips (What Gets EXTRA Marks)")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # TIP styled box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_TIP)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_TIP)
        DocxHelpers.set_cell_padding(cell, 100)

        for idx, tip in enumerate(self.data.examiner_pro_tips):
            para = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()

            run = para.add_run(f"{Icons.CORRECT} ")
            run.font.name = Fonts.PRIMARY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

            DocxHelpers.add_formatted_text(para, tip)

        self.document.add_paragraph()  # Spacing

    def _add_checklist(self):
        """Add self-assessment checklist with NEUTRAL styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.CHECKLIST} Self-Assessment Checklist")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # NEUTRAL styled box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        for idx, item in enumerate(self.data.self_assessment_checklist):
            para = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()

            run = para.add_run("☐ ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

            run = para.add_run(item)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_end_marker(self):
        """Add end of chapter marker."""
        # Decorative line
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run('─' * 40)
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BORDER_NEUTRAL)

        # End message
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(6)

        run = para.add_run(f"{Icons.STAR} End of Chapter {self.data.chapter_number} {Icons.STAR}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD
