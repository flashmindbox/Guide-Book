"""
Part B: Key Concepts generator for Guide Book Generator.
Generates the Key Concepts section with formatted content.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class PartBGenerator:
    """Generates Part B: Key Concepts."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

    def generate(self):
        """Generate Part B: Key Concepts."""
        # Page break
        DocxHelpers.add_page_break(self.document)

        # Part header
        self._add_part_header()

        # Each concept
        for concept in self.data.concepts:
            if not concept.is_empty():
                self._add_concept(concept)

        # Comparison tables
        if self.data.comparison_tables:
            self._add_comparison_tables()

        # Common mistakes
        if self.data.common_mistakes:
            self._add_common_mistakes()

        # Important dates timeline
        if self.data.important_dates:
            self._add_important_dates()

    def _add_part_header(self):
        """Add the part header in a styled box - unified blue color."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]

        # Full title in PRIMARY_BLUE
        run = para.add_run("Part B: Key Concepts")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        self.document.add_paragraph()  # Spacing

    def _add_concept(self, concept):
        """Add a single concept with all its elements."""
        # Concept title (numbered, blue)
        para = self.document.add_paragraph(style='SectionTitle')
        run = para.add_run(f"{concept.number}. {concept.title}")
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # NCERT exact line box (if present)
        if concept.ncert_line:
            self._add_ncert_line_box(concept.ncert_line)

        # Main content
        if concept.content:
            self._add_concept_content(concept.content)

        # Memory trick (if present)
        if concept.memory_trick:
            self._add_memory_trick(concept.memory_trick)

        # Did You Know box (if present)
        if concept.did_you_know:
            self._add_did_you_know_box(concept.did_you_know)

        self.document.add_paragraph(style='BodyText')  # Spacing between concepts

    def _add_ncert_line_box(self, text: str):
        """Add NCERT exact line in INFO styled box (blue left border)."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_INFO)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]

        run = para.add_run(f"{Icons.IMPORTANT} NCERT Exact Line: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        run = para.add_run(f'"{text}"')
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_concept_content(self, content: str):
        """Add the main concept content with formatting."""
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if it's a bullet point
            if line.startswith(('-', '•', '*')):
                para = self.document.add_paragraph(style='BulletPoint')
                para.paragraph_format.left_indent = Inches(0.25)
                line = line[1:].strip()
                para.add_run("• ")

            # Check if it's a numbered point
            elif line[0].isdigit() and '.' in line[:3]:
                para = self.document.add_paragraph(style='BodyText')
                para.paragraph_format.left_indent = Inches(0.25)

            else:
                para = self.document.add_paragraph(style='BodyText')

            # Add formatted text
            DocxHelpers.add_formatted_text(para, line)

    def _add_memory_trick(self, text: str):
        """Add memory trick in TIP styled box (green left border)."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_TIP)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_TIP)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT  # Left align (not right)

        run = para.add_run(f"{Icons.TIP} Memory Trick: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        run = para.add_run(text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_did_you_know_box(self, text: str):
        """Add Did You Know box with distinct ORANGE styling."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, '#FFF7ED')  # Light orange
        DocxHelpers.set_cell_left_border_only(cell, '#D97706')  # Orange border
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]

        run = para.add_run("? Did You Know? ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb('#D97706')  # Orange title

        # Content - use bold styling
        run = para.add_run(text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_comparison_tables(self):
        """Add comparison tables section with unified styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.CHART} Comparison Tables")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        for table_data in self.data.comparison_tables:
            title = table_data.get('title', 'Comparison')
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])

            if headers and rows:
                # Add table title
                para = self.document.add_paragraph()
                run = para.add_run(title)
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY
                run.font.bold = True
                run.font.italic = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

                DocxHelpers.create_comparison_table(self.document, title, headers, rows)
                self.document.add_paragraph()

    def _add_common_mistakes(self):
        """Add common mistakes section with WARNING styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.WRONG} Common Mistakes to Avoid")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Create WARNING styled box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_WARNING)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("These mistakes cost students marks every year!")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        for mistake in self.data.common_mistakes:
            para = cell.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.1)

            run = para.add_run(f"{Icons.WRONG} ")
            run.font.name = Fonts.PRIMARY

            DocxHelpers.add_formatted_text(para, mistake)

    def _add_important_dates(self):
        """Add important dates timeline with improved styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"{Icons.CALENDAR} Important Dates Timeline")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Create timeline table
        table = self.document.add_table(rows=len(self.data.important_dates), cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(1.0)
        table.columns[1].width = Inches(5.5)

        for idx, date_item in enumerate(self.data.important_dates):
            year = date_item.get('year', '')
            event = date_item.get('event', '')

            # Year cell - blue background
            cell = table.cell(idx, 0)
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(year)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

            # Event cell - alternating background
            cell = table.cell(idx, 1)
            if idx % 2 == 1:
                DocxHelpers.set_cell_background(cell, Colors.TABLE_ALT_ROW)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]

            DocxHelpers.add_formatted_text(para, event)
