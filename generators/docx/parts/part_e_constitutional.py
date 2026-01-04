"""
Part E: Constitutional Articles generator for Guide Book Generator.
For Political Science subjects - covers key constitutional articles and amendments.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Icons

from ..helpers import DocxHelpers


class PartEConstitutionalGenerator:
    """Generates Part E: Constitutional Articles with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part E: Constitutional Articles."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if constitutional articles exist
        constitutional_articles = getattr(self.data, 'constitutional_articles', None)

        if not constitutional_articles:
            self._add_placeholder_notice()
            return

        # Render each constitutional article
        for idx, article in enumerate(constitutional_articles, 1):
            self._add_article(article, idx)

        # Related amendments section (if any)
        related_amendments = getattr(self.data, 'constitutional_amendments', None)
        if related_amendments:
            self._add_amendments_section(related_amendments)

    def _add_part_header(self):
        """Add part header with light purple background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)  # Light blue background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Constitutional Articles")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        self.document.add_paragraph()

    def _add_placeholder_notice(self):
        """Add placeholder notice when no constitutional articles exist."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run("📜 ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        run = para.add_run("Add constitutional articles in the Part E section.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()

    def _add_article(self, article: dict, index: int):
        """Add a single constitutional article with formatting."""
        # Article header box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]

        # Article number and title
        article_number = article.get('article_number', '')
        article_title = article.get('title', '')

        if article_number:
            run = para.add_run(f"Article {article_number}")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            if article_title:
                run = para.add_run(f": {article_title}")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(14)
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)
        elif article_title:
            run = para.add_run(article_title)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Description/Explanation
        description = article.get('description', '')
        if description:
            para = self.document.add_paragraph()
            para.paragraph_format.space_before = Pt(8)
            para.paragraph_format.space_after = Pt(6)
            para.paragraph_format.left_indent = Inches(0.25)

            run = para.add_run(description)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

        # Key points
        key_points = article.get('key_points', [])
        if key_points:
            para = self.document.add_paragraph()
            para.paragraph_format.space_before = Pt(8)
            para.paragraph_format.space_after = Pt(4)

            run = para.add_run("Key Points:")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

            for point in key_points:
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.5)
                para.paragraph_format.space_after = Pt(2)

                run = para.add_run("• ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

                run = para.add_run(point)
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)

        # Related case studies
        case_studies = article.get('case_studies', [])
        if case_studies:
            para = self.document.add_paragraph()
            para.paragraph_format.space_before = Pt(8)
            para.paragraph_format.space_after = Pt(4)

            run = para.add_run("Related Case Studies:")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_PURPLE)

            for case in case_studies:
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.5)
                para.paragraph_format.space_after = Pt(2)

                run = para.add_run("📋 ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)

                run = para.add_run(case)
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.italic = True

        # Add spacing between articles
        self.document.add_paragraph()

    def _add_amendments_section(self, amendments: list):
        """Add related constitutional amendments section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(8)

        run = para.add_run(f"{Icons.PENCIL} Related Constitutional Amendments")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create table for amendments
        table = self.document.add_table(rows=1, cols=3)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(1.5)
        table.columns[1].width = Inches(3.5)
        table.columns[2].width = Inches(1.5)

        # Header row
        header_row = table.rows[0]
        headers = ['Amendment', 'Description', 'Year']

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
        for amendment in amendments:
            row = table.add_row()

            # Amendment number
            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(amendment.get('number', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True

            # Description
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            run = para.add_run(amendment.get('description', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

            # Year
            cell = row.cells[2]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(amendment.get('year', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
