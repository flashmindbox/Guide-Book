"""
Part E: Grammar Focus generator for Guide Book Generator.
For English subjects - covers grammar rules, examples, and practice.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Icons

from ..helpers import DocxHelpers


class PartEGrammarGenerator:
    """Generates Part E: Grammar Focus with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part E: Grammar Focus."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if grammar data exists
        grammar_data = getattr(self.data, 'grammar_data', None)

        if not grammar_data:
            self._add_placeholder_notice()
            return

        # Render each grammar rule
        for idx, rule in enumerate(grammar_data, 1):
            self._add_grammar_rule(rule, idx)

    def _add_part_header(self):
        """Add part header with light orange background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)  # Light orange background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Grammar Focus")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)

        self.document.add_paragraph()

    def _add_placeholder_notice(self):
        """Add placeholder notice when no grammar data exists."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run(f"{Icons.PENCIL} ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        run = para.add_run("Add grammar rules and examples in the Part E section.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()

    def _add_grammar_rule(self, rule: dict, index: int):
        """Add a single grammar rule with formatting."""
        topic = rule.get('topic', f'Grammar Rule {index}')
        rule_text = rule.get('rule', '')
        examples = rule.get('examples', {})
        common_mistakes = rule.get('common_mistakes', [])
        practice = rule.get('practice', [])

        # Topic header box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.BOOK} {index}. {topic}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Rule explanation
        if rule_text:
            self._add_rule_explanation(rule_text)

        # Correct/Incorrect examples
        if examples:
            self._add_examples(examples)

        # Common mistakes
        if common_mistakes:
            self._add_common_mistakes(common_mistakes)

        # Practice sentences
        if practice:
            self._add_practice_sentences(practice)

        # Spacing between rules
        self.document.add_paragraph()

    def _add_rule_explanation(self, rule_text: str):
        """Add rule explanation text."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(6)
        para.paragraph_format.left_indent = Inches(0.25)

        run = para.add_run("Rule: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        run = para.add_run(rule_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

    def _add_examples(self, examples: dict):
        """Add correct and incorrect examples in a two-column table."""
        correct = examples.get('correct', [])
        incorrect = examples.get('incorrect', [])

        if not correct and not incorrect:
            return

        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("Examples:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True

        # Create two-column table for correct/incorrect
        table = self.document.add_table(rows=1, cols=2)
        table.alignment = 1
        DocxHelpers.set_table_borders(table, Colors.BORDER_NEUTRAL)

        table.columns[0].width = Inches(3.25)
        table.columns[1].width = Inches(3.25)

        # Header row
        header_row = table.rows[0]

        # Correct header
        cell = header_row.cells[0]
        DocxHelpers.set_cell_background(cell, Colors.BG_SUCCESS)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run("✓ CORRECT")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Incorrect header
        cell = header_row.cells[1]
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_padding(cell, 60)
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run("✗ INCORRECT")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Determine max rows needed
        max_rows = max(len(correct), len(incorrect))

        for i in range(max_rows):
            row = table.add_row()

            # Correct example
            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            if i < len(correct):
                run = para.add_run("✓ ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

                run = para.add_run(correct[i])
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)

            # Incorrect example
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 60)
            para = cell.paragraphs[0]
            if i < len(incorrect):
                run = para.add_run("✗ ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

                run = para.add_run(incorrect[i])
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.strike = True  # Strikethrough for incorrect

    def _add_common_mistakes(self, mistakes: list):
        """Add common mistakes section with warning styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("⚠ Common Mistakes to Avoid:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Create highlighted box for mistakes
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_padding(cell, 60)

        for idx, mistake in enumerate(mistakes):
            if idx > 0:
                # Add new paragraph for subsequent mistakes
                para = cell.add_paragraph()
            else:
                para = cell.paragraphs[0]

            para.paragraph_format.space_after = Pt(2)

            run = para.add_run("• ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            run = para.add_run(mistake)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

    def _add_practice_sentences(self, practice: list):
        """Add practice sentences section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("✏ Practice:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        for idx, sentence in enumerate(practice, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.5)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True

            run = para.add_run(sentence)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
