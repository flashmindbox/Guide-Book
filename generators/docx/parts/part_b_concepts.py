"""
Part B: Key Concepts generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts
from ..helpers import DocxHelpers


class PartBGenerator:
    """Generates Part B: Key Concepts with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part B: Key Concepts."""
        DocxHelpers.add_page_break(self.document)

        self._add_part_header()

        for concept in self.data.concepts:
            if not concept.is_empty():
                self._add_concept(concept)

        if self.data.comparison_tables:
            self._add_comparison_tables()

        if self.data.common_mistakes:
            self._add_common_mistakes()

        if self.data.important_dates:
            self._add_important_dates()

    def _add_part_header(self):
        """Add simple part header."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(12)

        run = para.add_run("Part B: Key Concepts")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

    def _add_concept(self, concept):
        """Add a single concept with all its elements."""
        # Concept title - 16pt blue
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run(f"{concept.number}. {concept.title}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # NCERT exact line (if present) - indented quote
        if concept.ncert_line:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.3)
            para.paragraph_format.space_after = Pt(6)

            run = para.add_run("📌 NCERT: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            run = para.add_run(f'"{concept.ncert_line}"')
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.italic = True

        # Main content
        if concept.content:
            self._add_concept_content(concept.content)

        # Memory trick - right-aligned, green, italic
        if concept.memory_trick:
            para = self.document.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            para.paragraph_format.space_before = Pt(6)

            run = para.add_run("💡 Memory: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

            run = para.add_run(concept.memory_trick)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Did You Know (if present)
        if concept.did_you_know:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.3)
            para.paragraph_format.space_before = Pt(6)

            run = para.add_run("💡 Did You Know? ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb('#D97706')  # Orange

            run = para.add_run(concept.did_you_know)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_concept_content(self, content: str):
        """Add the main concept content with formatting."""
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            para = self.document.add_paragraph()
            para.paragraph_format.space_after = Pt(3)

            # Check if it's a bullet point
            if line.startswith(('-', '•', '*')):
                para.paragraph_format.left_indent = Inches(0.25)
                line = line[1:].strip()
                DocxHelpers.add_formatted_text(para, f"• {line}")

            # Check if it's a numbered point
            elif line[0].isdigit() and '.' in line[:3]:
                para.paragraph_format.left_indent = Inches(0.25)
                DocxHelpers.add_formatted_text(para, line)

            else:
                DocxHelpers.add_formatted_text(para, line)

    def _add_comparison_tables(self):
        """Add comparison tables section."""
        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📊 Comparison Tables")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for table_data in self.data.comparison_tables:
            title = table_data.get('title', 'Comparison')
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])

            if headers and rows:
                # Table title
                para = self.document.add_paragraph()
                para.paragraph_format.space_before = Pt(12)
                run = para.add_run(title)
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(12)
                run.font.bold = True
                run.font.italic = True

                DocxHelpers.create_comparison_table(self.document, title, headers, rows)

    def _add_common_mistakes(self):
        """Add common mistakes section."""
        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("⚠ Common Mistakes to Avoid")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        for mistake in self.data.common_mistakes:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run("❌ ")
            run.font.name = Fonts.PRIMARY

            DocxHelpers.add_formatted_text(para, mistake)

    def _add_important_dates(self):
        """Add important dates timeline."""
        # Section header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📅 Important Dates Timeline")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create simple table
        table = self.document.add_table(rows=len(self.data.important_dates), cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(1.0)
        table.columns[1].width = Inches(5.5)

        for idx, date_item in enumerate(self.data.important_dates):
            year = date_item.get('year', '')
            event = date_item.get('event', '')

            # Year cell
            cell = table.cell(idx, 0)
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(year)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            # Event cell
            cell = table.cell(idx, 1)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            DocxHelpers.add_formatted_text(para, event)
