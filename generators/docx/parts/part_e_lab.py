"""
Part E: Lab Manual & Activities generator for Guide Book Generator.
For Science subjects - covers experiments, practicals, and lab activities.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts, Icons

from ..helpers import DocxHelpers


class PartELabGenerator:
    """Generates Part E: Lab Manual & Activities with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part E: Lab Manual & Activities."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # Check if lab activities data exists
        lab_activities = getattr(self.data, 'lab_activities', None)

        if not lab_activities:
            self._add_placeholder_notice()
            return

        # Render each experiment/activity
        for idx, activity in enumerate(lab_activities, 1):
            self._add_experiment(activity, idx)

    def _add_part_header(self):
        """Add part header with light cyan background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)  # Light blue/cyan background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part E: Lab Manual & Activities")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        self.document.add_paragraph()

    def _add_placeholder_notice(self):
        """Add placeholder notice when no lab activities exist."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = para.add_run("🔬 ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)

        run = para.add_run("Add experiments and lab activities in the Part E section.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.TEXT_SECONDARY)

        self.document.add_paragraph()

    def _add_experiment(self, activity: dict, index: int):
        """Add a single experiment/activity with formatting."""
        name = activity.get('name', f'Experiment {index}')
        aim = activity.get('aim', '')
        materials = activity.get('materials', [])
        procedure = activity.get('procedure', [])
        observations = activity.get('observations', '')
        conclusion = activity.get('conclusion', '')
        precautions = activity.get('precautions', [])
        diagram = activity.get('diagram', '')

        # Experiment header box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 80)

        para = cell.paragraphs[0]
        run = para.add_run(f"🔬 Experiment {index}: {name}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Aim/Objective
        if aim:
            self._add_aim(aim)

        # Materials required
        if materials:
            self._add_materials(materials)

        # Diagram (if provided, show before procedure)
        if diagram:
            self._add_diagram(diagram)

        # Procedure steps
        if procedure:
            self._add_procedure(procedure)

        # Observations
        if observations:
            self._add_observations(observations)

        # Conclusion
        if conclusion:
            self._add_conclusion(conclusion)

        # Precautions
        if precautions:
            self._add_precautions(precautions)

        # Spacing between experiments
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(12)

    def _add_aim(self, aim: str):
        """Add aim/objective section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run(f"{Icons.TARGET} Aim: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        run = para.add_run(aim)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

    def _add_materials(self, materials: list):
        """Add materials required section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("📦 Materials Required:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_PURPLE)

        # Create a single line with materials separated by commas
        para = self.document.add_paragraph()
        para.paragraph_format.left_indent = Inches(0.25)
        para.paragraph_format.space_after = Pt(4)

        materials_text = ", ".join(materials)
        run = para.add_run(materials_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

    def _add_diagram(self, diagram_path: str):
        """Add diagram/image or placeholder."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("📐 Diagram:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(6)

        try:
            # Attempt to add actual image
            self.document.add_picture(diagram_path, width=Inches(4))
        except Exception:
            # Show placeholder if image cannot be loaded
            run = para.add_run("[Diagram: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

            run = para.add_run(diagram_path)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

            run = para.add_run("]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    def _add_procedure(self, procedure: list):
        """Add procedure steps with clear numbering."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("📋 Procedure:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Create numbered steps in a table for better formatting
        table = self.document.add_table(rows=len(procedure), cols=2)
        table.alignment = 1

        table.columns[0].width = Inches(0.5)
        table.columns[1].width = Inches(6.0)

        for idx, step in enumerate(procedure):
            row = table.rows[idx]

            # Step number
            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 40)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = para.add_run(f"{idx + 1}.")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

            # Step description
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 40)
            para = cell.paragraphs[0]

            run = para.add_run(step)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

    def _add_observations(self, observations: str):
        """Add observations section."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("👁 Observations:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_PURPLE)

        # Observation box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
        DocxHelpers.set_cell_padding(cell, 60)

        para = cell.paragraphs[0]
        run = para.add_run(observations)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

    def _add_conclusion(self, conclusion: str):
        """Add conclusion section with highlight."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("✅ Conclusion:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Conclusion box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_SUCCESS)
        DocxHelpers.set_cell_padding(cell, 60)

        para = cell.paragraphs[0]
        run = para.add_run(conclusion)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

    def _add_precautions(self, precautions: list):
        """Add precautions section with warning styling."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)

        run = para.add_run("⚠ Precautions:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        # Precautions box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.0)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_padding(cell, 60)

        for idx, precaution in enumerate(precautions):
            if idx > 0:
                para = cell.add_paragraph()
            else:
                para = cell.paragraphs[0]

            para.paragraph_format.space_after = Pt(2)

            run = para.add_run("• ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

            run = para.add_run(precaution)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
