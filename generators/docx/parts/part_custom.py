"""
Custom Part generator for Guide Book Generator.
Handles dynamically added parts (H, I, J, etc.) with placeholder content.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class CustomPartGenerator:
    """Generates custom parts (H, I, J, etc.) with placeholder content."""

    def __init__(self, document: Document, data: ChapterData, part_id: str, part_name: str):
        """
        Initialize the custom part generator.

        Args:
            document: The DOCX document to add content to
            data: Chapter data
            part_id: The part ID (H, I, J, etc.)
            part_name: The custom part name (e.g., "Case Studies")
        """
        self.document = document
        self.data = data
        self.part_id = part_id
        self.part_name = part_name

    def generate(self):
        """Generate the custom part with header and placeholder content."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()
        self._add_placeholder_content()

    def _add_part_header(self):
        """Add part header with light blue background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)  # Light blue background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run(f"Part {self.part_id}: {self.part_name}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        self.document.add_paragraph()

    def _add_placeholder_content(self):
        """Add placeholder message for custom part."""
        # Create a subtle info box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Icon
        run = para.add_run("📌 ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        # Message
        run = para.add_run("Content for this section can be added in future versions.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()
