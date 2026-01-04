"""
Cover page generator for Guide Book Generator.
Generates the cover page using named styles from template for consistency.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.base import ChapterData
from core.models.parts import PartManager
from styles.theme import Colors, Fonts, Decorative, Icons, BoxStyles
from ..helpers import DocxHelpers


class CoverPageGenerator:
    """Generates the cover page of the document using template styles."""

    def __init__(self, document: Document, data: ChapterData, part_manager: PartManager):
        self.document = document
        self.data = data
        self.part_manager = part_manager
        self.styles = document.styles  # Access template styles

    def generate(self):
        """Generate the complete cover page."""
        self._add_header()
        self._add_decorative_line()
        self._add_chapter_title()
        self._add_decorative_line()
        self._add_metadata_table()

        if self.data.syllabus_alert_enabled and self.data.syllabus_alert_text:
            self._add_syllabus_alert()

        if self.data.learning_objectives:
            self._add_learning_objectives()

        self._add_chapter_contents()

        # QR codes (if URLs provided)
        if self.data.qr_practice_questions_url or self.data.qr_practice_with_answers_url:
            self._add_qr_codes()

    def _add_header(self):
        """Add the header: CBSE Class X | Subject Category | Subject."""
        subject_display = self.data.subject.replace('_', ' ').title()
        header_text = f"CBSE Class {self.data.class_num} | Social Science | {subject_display}"

        # Simple centered text (no box)
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(header_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_decorative_line(self):
        """Add a solid decorative horizontal line."""
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run('─' * 50)  # Solid horizontal line character (U+2500)
        run.font.size = Pt(11)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

    def _add_chapter_title(self):
        """Add chapter number and title."""
        # Chapter number - BLUE (not red)
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(12)
        run = para.add_run(f"CHAPTER {self.data.chapter_number}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_PART_HEADER  # 16pt
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Chapter title - Large, bold, blue
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(self.data.chapter_title)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_CHAPTER_TITLE  # 24pt
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Thin underline below title
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(3)
        run = para.add_run('─' * 40)  # Thin line
        run.font.size = Pt(10)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        # Subtitle (if present)
        if self.data.subtitle:
            para = self.document.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(self.data.subtitle)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_metadata_table(self):
        """Add the metadata table with Weightage, Map Work, Importance, PYQ Frequency."""
        # Determine colors based on values - use ACCENT_RED for emphasis
        importance_color = Colors.ACCENT_RED if self.data.importance == 'High' else Colors.BODY_TEXT
        frequency_color = Colors.ACCENT_RED if self.data.pyq_frequency == 'Every Year' else Colors.BODY_TEXT

        metadata = {
            'Weightage': (self.data.weightage, Colors.PRIMARY_BLUE),
            'Map Work': (self.data.map_work, Colors.BODY_TEXT),
            'Importance': (self.data.importance, importance_color),
            'PYQ Frequency': (self.data.pyq_frequency, frequency_color),
        }

        self.document.add_paragraph()  # Spacing
        DocxHelpers.create_metadata_table(self.document, metadata, self.styles)
        self.document.add_paragraph()  # Spacing

    def _add_syllabus_alert(self):
        """Add syllabus alert box with warning styling."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_WARNING)
        DocxHelpers.set_cell_padding(cell, 150)

        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.WARNING} SYLLABUS ALERT: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

        run = para.add_run(self.data.syllabus_alert_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        self.document.add_paragraph()  # Spacing

    def _add_learning_objectives(self):
        """Add learning objectives box with left border styling."""
        objectives = self.data.learning_objectives.strip().split('\n')
        clean_objectives = []
        for obj in objectives:
            obj = obj.strip()
            if obj:
                # Remove leading bullet/dash if present
                if obj.startswith(('-', '•', '*')):
                    obj = obj[1:].strip()
                clean_objectives.append(obj)

        # Create INFO box (blue left border)
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_INFO)
        DocxHelpers.set_cell_padding(cell, 150)

        # Title with icon
        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.TARGET} Learning Objectives")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Subtitle
        para = cell.add_paragraph()
        run = para.add_run("After studying this chapter, you will be able to:")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        # Bullet points
        for obj in clean_objectives:
            para = cell.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.15)
            run = para.add_run("• ")
            run.font.name = Fonts.PRIMARY
            DocxHelpers.add_formatted_text(para, obj)

        self.document.add_paragraph()  # Spacing

    def _add_chapter_contents(self):
        """Add chapter contents box with neutral styling."""
        # Create NEUTRAL box (gray background)
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_NEUTRAL)
        DocxHelpers.set_cell_borders(cell, Colors.BORDER_NEUTRAL)
        DocxHelpers.set_cell_padding(cell, 150)

        # Title with icon
        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.BOOK} Chapter Contents")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        # List each enabled part
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            description = self.data.part_descriptions.get(part.id, part.description)

            para = cell.add_paragraph()

            # "Part A:" in PRIMARY_BLUE (consistent with headings)
            run = para.add_run(f"Part {part.id}: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

            # Description in body text
            run = para.add_run(description)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

    def _add_qr_codes(self):
        """Add QR codes for practice materials."""
        self.document.add_paragraph()

        # Create a table for QR codes box
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1  # CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_LIGHT_BLUE)
        DocxHelpers.set_cell_borders(cell, Colors.PRIMARY_BLUE)
        DocxHelpers.set_cell_padding(cell, 150)

        # Title
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run("📱 Scan QR Codes to Download Practice Materials")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Create inner table for QR codes side by side with spacer column
        qr_table = cell.add_table(rows=2, cols=3)
        qr_table.alignment = 1

        # Set column widths - QR columns and spacer in middle
        qr_table.columns[0].width = Inches(2.0)
        qr_table.columns[1].width = Inches(2.5)  # Spacer column for distance
        qr_table.columns[2].width = Inches(2.0)

        try:
            import qrcode
            from io import BytesIO

            # Generate QR code 1: Practice Questions
            if self.data.qr_practice_questions_url:
                qr1 = qrcode.QRCode(version=1, box_size=6, border=2)
                qr1.add_data(self.data.qr_practice_questions_url)
                qr1.make(fit=True)
                img1 = qr1.make_image(fill_color="black", back_color="white")

                buf1 = BytesIO()
                img1.save(buf1, format='PNG')
                buf1.seek(0)

                # Add to cell (first column)
                qr_cell = qr_table.cell(0, 0)
                qr_para = qr_cell.paragraphs[0]
                qr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = qr_para.add_run()
                run.add_picture(buf1, width=Inches(1.3))

                # Label
                label_cell = qr_table.cell(1, 0)
                label_para = label_cell.paragraphs[0]
                label_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = label_para.add_run("Practice Questions")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY_SMALL
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

            # Generate QR code 2: With Answers
            if self.data.qr_practice_with_answers_url:
                qr2 = qrcode.QRCode(version=1, box_size=6, border=2)
                qr2.add_data(self.data.qr_practice_with_answers_url)
                qr2.make(fit=True)
                img2 = qr2.make_image(fill_color="black", back_color="white")

                buf2 = BytesIO()
                img2.save(buf2, format='PNG')
                buf2.seek(0)

                # Add to cell (third column, leaving middle as spacer)
                qr_cell = qr_table.cell(0, 2)
                qr_para = qr_cell.paragraphs[0]
                qr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = qr_para.add_run()
                run.add_picture(buf2, width=Inches(1.3))

                # Label
                label_cell = qr_table.cell(1, 2)
                label_para = label_cell.paragraphs[0]
                label_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = label_para.add_run("With Answers")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY_SMALL
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

        except ImportError:
            # Fallback if qrcode not installed
            para = cell.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run("[QR codes require 'qrcode' library]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_CAPTION
            run.font.italic = True
