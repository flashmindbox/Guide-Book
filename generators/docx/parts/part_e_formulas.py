"""
Part E: Formula Sheet generator for Guide Book Generator.
For Mathematics/Physics subjects - covers formulas, equations, and their applications.
"""

from collections import defaultdict

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Icons

from ..helpers import DocxHelpers


class PartEFormulasGenerator:
    """Generates Part E: Formula Sheet with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part E: Formula Sheet."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if formulas data exists
        formulas_data = getattr(self.data, 'formulas_data', None)

        if not formulas_data:
            self._add_placeholder_notice()
            return

        # Group formulas by category
        grouped = self._group_by_category(formulas_data)

        # Render each category
        for category, formulas in grouped.items():
            if category:
                self._add_category_header(category)
            for idx, formula in enumerate(formulas, 1):
                self._add_formula(formula, idx)

    def _add_part_header(self):
        """Add part header with light purple background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)  # Light blue background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Formula Sheet")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        self.document.add_paragraph()

    def _add_placeholder_notice(self):
        """Add placeholder notice when no formulas data exists."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run("📐 ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        run = para.add_run("Add formulas and equations in the Part E section.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()

    def _group_by_category(self, formulas_data: list) -> dict:
        """Group formulas by category, preserving order."""
        grouped = defaultdict(list)
        uncategorized = []

        for formula in formulas_data:
            category = formula.get('category', '')
            if category:
                grouped[category].append(formula)
            else:
                uncategorized.append(formula)

        # Build ordered result - categories first, then uncategorized
        result = dict(grouped)
        if uncategorized:
            result[''] = uncategorized

        return result

    def _add_category_header(self, category: str):
        """Add category section header."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(16)
        para.paragraph_format.space_after = Pt(8)

        run = para.add_run(f"▸ {category}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_PURPLE)

    def _add_formula(self, formula: dict, index: int):
        """Add a single formula with formatting."""
        name = formula.get('name', f'Formula {index}')
        formula_text = formula.get('formula', '')
        variables = formula.get('variables', {})
        example = formula.get('example', '')

        # Formula name
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run(f"📌 {name}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Formula box (highlighted)
        if formula_text:
            self._add_formula_box(formula_text)

        # Variables explanation
        if variables:
            self._add_variables(variables)

        # Example usage
        if example:
            self._add_example(example)

        # Small spacing between formulas
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(6)

    def _add_formula_box(self, formula_text: str):
        """Add formula in a highlighted box for visibility."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)  # Light yellow/orange for visibility
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run(formula_text)
        run.font.name = Fonts.MONO  # Monospace for formulas
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)

    def _add_variables(self, variables: dict):
        """Add variables explanation."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.left_indent = Inches(0.25)

        run = para.add_run("Where: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

        # Create inline variable list
        var_parts = []
        for var, desc in variables.items():
            var_parts.append(f"{var} = {desc}")

        para = self.document.add_paragraph()
        para.paragraph_format.left_indent = Inches(0.5)
        para.paragraph_format.space_after = Pt(2)

        for i, (var, desc) in enumerate(variables.items()):
            # Variable name (bold, monospace style)
            run = para.add_run(var)
            run.font.name = Fonts.MONO
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            # Equals and description
            run = para.add_run(f" = {desc}")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

            # Add separator if not last
            if i < len(variables) - 1:
                run = para.add_run("   |   ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    def _add_example(self, example: str):
        """Add example usage."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.left_indent = Inches(0.25)

        run = para.add_run(f"{Icons.TIP} Example: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        run = para.add_run(example)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.italic = True
