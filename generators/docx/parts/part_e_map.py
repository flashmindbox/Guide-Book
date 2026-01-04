"""
Part E: Map Work generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartEGenerator:
    """Generates Part E: Map Work with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

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
        """Add part header with blue background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.HEADING_BLUE)
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Map Work")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb('#FFFFFF')

        self.document.add_paragraph()

    def _add_na_notice(self):
        """Add N/A notice for chapters without map work."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(24)
        para.paragraph_format.space_after = Pt(12)

        run = para.add_run("🗺 No Map Work from this Chapter")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

        # Subject-specific note
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if self.data.subject == 'history':
            note = "All History map work (2 marks) comes from Chapter 2: Nationalism in India"
        else:
            note = "N/A for this chapter"

        run = para.add_run(note)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True

    def _add_map_items(self):
        """Add map work items list."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("🗺 CBSE Prescribed Map Locations")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for idx, item in enumerate(self.data.map_items, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

            run = para.add_run(item)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_map_image(self):
        """Add map image placeholder."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(18)

        # Note: Actual image embedding would use:
        # self.document.add_picture(self.data.map_image_path, width=Inches(5))

        run = para.add_run("[Map Image Placeholder]")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    def _add_map_tips(self):
        """Add map marking tips."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("💡 Map Marking Tips")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        for tip in self.data.map_tips.split('\n'):
            tip = tip.strip()
            if tip:
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.25)
                para.paragraph_format.space_after = Pt(3)

                run = para.add_run("• ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(11)

                DocxHelpers.add_formatted_text(para, tip)
