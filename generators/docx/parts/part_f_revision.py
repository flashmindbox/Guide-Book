"""
Part F: Quick Revision generator for Guide Book Generator.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class PartFGenerator:
    """Generates Part F: Quick Revision."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

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
        run = para.add_run("Part F: Quick Revision")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        self.document.add_paragraph()  # Spacing

    def _add_key_points(self):
        """Add key points summary in a NEUTRAL box."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run("1. Key Points Summary")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Box with numbered points
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        for idx, point in enumerate(self.data.revision_key_points, 1):
            para = cell.paragraphs[0] if idx == 1 else cell.add_paragraph()

            # Number in blue
            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

            # Content with formatting
            DocxHelpers.add_formatted_text(para, point)

        self.document.add_paragraph()  # Spacing

    def _add_key_terms(self):
        """Add key terms glossary table."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run("2. Key Terms Defined")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Create table
        table = self.document.add_table(rows=1, cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(2.0)
        table.columns[1].width = Inches(4.5)

        # Header row
        header_row = table.rows[0]

        cell = header_row.cells[0]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)
        para = cell.paragraphs[0]
        run = para.add_run("Term")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_TABLE_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        cell = header_row.cells[1]
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)
        para = cell.paragraphs[0]
        run = para.add_run("Definition")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_TABLE_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Data rows with alternating background
        for idx, term_item in enumerate(self.data.revision_key_terms):
            row = table.add_row()

            cell = row.cells[0]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            run = para.add_run(term_item.get('term', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

            cell = row.cells[1]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            run = para.add_run(term_item.get('definition', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_timeline(self):
        """Add important dates timeline."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.CALENDAR} Important Dates Timeline")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        # Create timeline table
        table = self.document.add_table(rows=len(self.data.revision_timeline), cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(1.2)
        table.columns[1].width = Inches(5.3)

        for idx, item in enumerate(self.data.revision_timeline):
            row = table.rows[idx]

            # Year cell - blue background
            cell = row.cells[0]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(item.get('year', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

            # Event cell - alternating background
            cell = row.cells[1]
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]

            DocxHelpers.add_formatted_text(para, item.get('event', ''))

        self.document.add_paragraph()  # Spacing

    def _add_memory_tricks(self):
        """Add memory tricks compilation with TIP styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.TIP} Memory Tricks Compilation")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Box with TIP styling
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_TIP)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_TIP)
        DocxHelpers.set_cell_padding(cell, 100)

        for idx, trick in enumerate(self.data.revision_memory_tricks):
            para = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()

            run = para.add_run(f"{Icons.TIP} ")
            run.font.name = Fonts.PRIMARY

            DocxHelpers.add_formatted_text(para, trick)

        self.document.add_paragraph()  # Spacing

    def _add_encouragement(self):
        """Add encouragement message."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run("You've got this! Trust your preparation. Good luck!")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)
