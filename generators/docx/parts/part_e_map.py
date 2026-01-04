"""
Part E: Map Work generator for Guide Book Generator.
"""

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Decorative
from ..helpers import DocxHelpers


class PartEGenerator:
    """Generates Part E: Map Work."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data
        self.styles = document.styles

    def generate(self):
        """Generate Part E: Map Work."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if N/A
        if self.data.map_work_na or self.data.map_work == "No":
            self._add_na_notice()
            return

        # Map items
        if self.data.map_items:
            self._add_map_items()

        # Map image
        if self.data.map_image_path:
            self._add_map_image()

        # Map tips
        if self.data.map_tips:
            self._add_map_tips()

    def _add_part_header(self):
        """Add the part header."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.WHITE)
        DocxHelpers.set_cell_borders(cell, Colors.DARK_GRAY)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]

        run = para.add_run("Part E: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DANGER_RED)

        run = para.add_run("Map Work")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        self.document.add_paragraph(style='BodyText')  # Spacing

    def _add_na_notice(self):
        """Add N/A notice for chapters without map work."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_LIGHT_GRAY)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_GRAY)
        DocxHelpers.set_cell_padding(cell, 150)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run(f"{Decorative.ICON_MAP} No Map Work from this Chapter")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_SECTION_TITLE
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

        para = cell.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Subject-specific note
        if self.data.subject == 'history':
            note = "All History map work (2 marks) comes from Chapter 2: Nationalism in India"
        else:
            note = "N/A for this chapter"

        run = para.add_run(note)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)

    def _add_map_items(self):
        """Add map work items list."""
        para = self.document.add_paragraph(style='SectionTitle')
        run = para.add_run(f"{Decorative.ICON_MAP} CBSE Prescribed Map Locations")
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # BOOK STANDARD

        for idx, item in enumerate(self.data.map_items, 1):
            para = self.document.add_paragraph(style='BodyText')
            para.paragraph_format.left_indent = Inches(0.25)

            run = para.add_run(f"{idx}. ")
            run.font.bold = True

            para.add_run(item)

        self.document.add_paragraph(style='BodyText')  # Spacing

    def _add_map_image(self):
        """Add map image placeholder."""
        para = self.document.add_paragraph(style='BodyText')
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Note: Actual image embedding would use:
        # self.document.add_picture(self.data.map_image_path, width=Inches(5))

        run = para.add_run("[Map Image Placeholder]")
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)

        self.document.add_paragraph(style='BodyText')  # Spacing

    def _add_map_tips(self):
        """Add map marking tips."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_LIGHT_GREEN)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_GREEN)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run(f"{Decorative.ICON_BULB} Map Marking Tips")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        for tip in self.data.map_tips.split('\n'):
            tip = tip.strip()
            if tip:
                para = cell.add_paragraph()
                run = para.add_run("• ")
                DocxHelpers.add_formatted_text(para, tip)
