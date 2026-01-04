"""
Part E: Graphs & Data Analysis generator for Guide Book Generator.
For Economics subjects - covers graphs, charts, and data interpretation.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Icons

from ..helpers import DocxHelpers


class PartEGraphsGenerator:
    """Generates Part E: Graphs & Data Analysis with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part E: Graphs & Data Analysis."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if graphs data exists
        graphs_data = getattr(self.data, 'graphs_data', None)

        if not graphs_data:
            self._add_placeholder_notice()
            return

        # Render each graph/data section
        for idx, graph in enumerate(graphs_data, 1):
            self._add_graph_section(graph, idx)

    def _add_part_header(self):
        """Add part header with light green background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_SUCCESS)  # Light green background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Graphs & Data Analysis")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        self.document.add_paragraph()

    def _add_placeholder_notice(self):
        """Add placeholder notice when no graphs data exists."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run(f"{Icons.CHART} ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        run = para.add_run("Add graphs and data analysis in the Part E section.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()

    def _add_graph_section(self, graph: dict, index: int):
        """Add a single graph/data section with formatting."""
        # Graph title header box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]

        # Graph number and title
        title = graph.get('title', f'Graph {index}')

        run = para.add_run(f"📈 {index}. {title}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Description
        description = graph.get('description', '')
        if description:
            para = self.document.add_paragraph()
            para.paragraph_format.space_before = Pt(8)
            para.paragraph_format.space_after = Pt(6)
            para.paragraph_format.left_indent = Inches(0.25)

            run = para.add_run(description)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

        # Graph image (if provided)
        image_path = graph.get('image_path', '')
        if image_path:
            self._add_graph_image(image_path)

        # Data points table (if provided)
        data_points = graph.get('data_points', [])
        if data_points:
            self._add_data_table(data_points)

        # Analysis/interpretation points
        analysis = graph.get('analysis', [])
        if analysis:
            self._add_analysis_points(analysis)

        # Add spacing between graphs
        self.document.add_paragraph()

    def _add_graph_image(self, image_path: str):
        """Add graph image or placeholder."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(12)

        try:
            # Attempt to add actual image
            self.document.add_picture(image_path, width=Inches(5))
        except Exception:
            # Show placeholder if image cannot be loaded
            run = para.add_run("[Graph Image: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

            run = para.add_run(image_path)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

            run = para.add_run("]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    def _add_data_table(self, data_points: list):
        """Add data points as a table."""
        if not data_points:
            return

        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("📋 Data Points:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Determine columns from first data point
        if not data_points:
            return

        first_point = data_points[0]
        columns = list(first_point.keys())
        num_cols = len(columns)

        if num_cols == 0:
            return

        # Create table
        table = self.document.add_table(rows=1, cols=num_cols)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        # Set column widths (distribute evenly)
        col_width = 6.5 / num_cols
        for i in range(num_cols):
            table.columns[i].width = Inches(col_width)

        # Header row
        header_row = table.rows[0]
        for idx, col_name in enumerate(columns):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Format column name (capitalize, replace underscores)
            display_name = col_name.replace('_', ' ').title()
            run = para.add_run(display_name)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Data rows
        for point in data_points:
            row = table.add_row()
            for idx, col_name in enumerate(columns):
                cell = row.cells[idx]
                DocxHelpers.set_cell_padding(cell, 60)
                para = cell.paragraphs[0]
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                value = str(point.get(col_name, ''))
                run = para.add_run(value)
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)

    def _add_analysis_points(self, analysis: list):
        """Add analysis/interpretation points."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("🔍 Analysis & Interpretation:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        for idx, point in enumerate(analysis, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.5)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

            run = para.add_run(point)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
