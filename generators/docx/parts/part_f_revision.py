"""
Part F: Quick Revision generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartFGenerator:
    """Generates Part F: Quick Revision with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part F: Quick Revision."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Key Points Summary
        if self.data.revision_key_points:
            self._add_key_points()

        # Key Terms Defined
        if self.data.revision_key_terms:
            self._add_key_terms()

        # Timeline
        if self.data.revision_timeline:
            self._add_timeline()

        # Memory Tricks Compilation
        if self.data.revision_memory_tricks:
            self._add_memory_tricks()

        # Encouragement message
        self._add_encouragement()

    def _add_part_header(self):
        """Add part header with light red background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)  # Light red background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part F: Quick Revision")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)  # Red text

        self.document.add_paragraph()

    def _add_key_points(self):
        """Add key points summary."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📝 Key Points Summary")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for idx, point in enumerate(self.data.revision_key_points, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            # Number in blue
            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            # Content with formatting
            DocxHelpers.add_formatted_text(para, point)

    def _add_key_terms(self):
        """Add key terms glossary table."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📚 Key Terms Defined")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create simple table
        table = self.document.add_table(rows=1, cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(2.0)
        table.columns[1].width = Inches(4.5)

        # Header row
        header_row = table.rows[0]

        cell = header_row.cells[0]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        run = para.add_run("Term")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        cell = header_row.cells[1]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        run = para.add_run("Definition")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Data rows
        for term_item in self.data.revision_key_terms:
            row = table.add_row()

            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(term_item.get('term', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(term_item.get('definition', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_timeline(self):
        """Add important dates timeline."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📅 Important Dates Timeline")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create simple timeline table
        table = self.document.add_table(rows=len(self.data.revision_timeline), cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(1.0)
        table.columns[1].width = Inches(5.5)

        for idx, item in enumerate(self.data.revision_timeline):
            row = table.rows[idx]

            # Year cell
            cell = row.cells[0]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(item.get('year', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            # Event cell
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            DocxHelpers.add_formatted_text(para, item.get('event', ''))

    def _add_memory_tricks(self):
        """Add memory tricks compilation - right-aligned, green, italic."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("💡 Memory Tricks Compilation")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        for trick in self.data.revision_memory_tricks:
            para = self.document.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            para.paragraph_format.space_after = Pt(6)

            run = para.add_run("💡 ")
            run.font.name = Fonts.PRIMARY

            run = para.add_run(trick)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

    def _add_encouragement(self):
        """Add encouragement message."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(24)

        run = para.add_run("⭐ You've got this! Trust your preparation. Good luck! ⭐")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)
