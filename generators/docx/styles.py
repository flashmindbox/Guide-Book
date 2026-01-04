"""
DOCX style definitions for Guide Book Generator.
Defines all document styles to match the demo PDF exactly.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from styles.theme import Colors, Fonts, PageLayout, Spacing


class DocxStyles:
    """
    Manages document styles for DOCX generation.
    Creates and applies consistent styles throughout the document.
    """

    def __init__(self, document: Document):
        self.document = document
        self._setup_styles()

    def _setup_styles(self):
        """Set up all custom styles for the document."""
        self._setup_heading_styles()
        self._setup_paragraph_styles()
        self._setup_table_styles()

    def _setup_heading_styles(self):
        """Set up heading styles - BOOK STANDARD."""
        styles = self.document.styles

        # Chapter Title style (24pt, bold, centered, blue)
        if 'ChapterTitle' not in [s.name for s in styles]:
            style = styles.add_style('ChapterTitle', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_CHAPTER_TITLE
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_NORMAL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

        # Part Header style (16pt, bold, blue) - For "Part A:", "Part B:" etc.
        if 'PartHeader' not in [s.name for s in styles]:
            style = styles.add_style('PartHeader', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_PART_HEADER
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_SECTION
            style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

        # Heading 2 style (16pt, blue) - BOOK STANDARD for section headers
        # Example: "1. The French Revolution and the Idea of the Nation"
        if 'Heading2Custom' not in [s.name for s in styles]:
            style = styles.add_style('Heading2Custom', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_PART_HEADER  # 16pt
            style.font.bold = False  # Reference shows normal weight
            style.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # #2563EB
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_LARGE
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Heading 3 style (14pt, blue) - BOOK STANDARD for subsection headers
        # Example: "Model Answers with Examiner's Marking Scheme"
        if 'Heading3Custom' not in [s.name for s in styles]:
            style = styles.add_style('Heading3Custom', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_SECTION_TITLE  # 14pt
            style.font.bold = False  # Reference shows normal weight
            style.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # #2563EB
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_NORMAL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Section Title style (14pt, bold) - Legacy, kept for compatibility
        if 'SectionTitle' not in [s.name for s in styles]:
            style = styles.add_style('SectionTitle', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_SECTION_TITLE
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # Updated to HEADING_BLUE
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_LARGE
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Concept Title style (12pt, bold, blue, numbered)
        if 'ConceptTitle' not in [s.name for s in styles]:
            style = styles.add_style('ConceptTitle', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_CONCEPT_TITLE
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)  # Updated to HEADING_BLUE
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_LARGE
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

    def _setup_paragraph_styles(self):
        """Set up paragraph styles - BOOK STANDARD."""
        styles = self.document.styles

        # Body Text style (black text for maximum readability)
        if 'BodyText' not in [s.name for s in styles]:
            style = styles.add_style('BodyText', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.color.rgb = Colors.hex_to_rgb(Colors.BLACK)  # Pure black for body
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_SMALL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL
            style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

        # Header Text style (centered, smaller)
        if 'HeaderText' not in [s.name for s in styles]:
            style = styles.add_style('HeaderText', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_SECTION_TITLE
            style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Decorative Line style
        if 'DecorativeLine' not in [s.name for s in styles]:
            style = styles.add_style('DecorativeLine', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.DECORATIVE
            style.font.size = Pt(12)
            style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_SMALL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Question style (bold)
        if 'Question' not in [s.name for s in styles]:
            style = styles.add_style('Question', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.BLACK)
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_NORMAL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        # Answer style
        if 'Answer' not in [s.name for s in styles]:
            style = styles.add_style('Answer', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_SMALL
            style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL
            style.paragraph_format.left_indent = Inches(0.25)

        # Memory Trick style (green, italic)
        if 'MemoryTrick' not in [s.name for s in styles]:
            style = styles.add_style('MemoryTrick', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY_SMALL
            style.font.italic = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            style.paragraph_format.space_before = Spacing.PARA_BEFORE_SMALL

        # Footer style
        if 'FooterText' not in [s.name for s in styles]:
            style = styles.add_style('FooterText', WD_STYLE_TYPE.PARAGRAPH)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_FOOTER
            style.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # BOOK STANDARD: Year style (red bold) for important dates
        if 'YearText' not in [s.name for s in styles]:
            style = styles.add_style('YearText', WD_STYLE_TYPE.CHARACTER)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)  # #DC2626

        # BOOK STANDARD: Key Term style (bold black)
        if 'KeyTerm' not in [s.name for s in styles]:
            style = styles.add_style('KeyTerm', WD_STYLE_TYPE.CHARACTER)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.bold = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.BLACK)

        # BOOK STANDARD: Foreign Term style (bold italic)
        if 'ForeignTerm' not in [s.name for s in styles]:
            style = styles.add_style('ForeignTerm', WD_STYLE_TYPE.CHARACTER)
            style.font.name = Fonts.PRIMARY
            style.font.size = Fonts.SIZE_BODY
            style.font.bold = True
            style.font.italic = True
            style.font.color.rgb = Colors.hex_to_rgb(Colors.BLACK)

    def _setup_table_styles(self):
        """Set up table styles."""
        # Table styles are applied directly when creating tables
        pass

    def apply_page_setup(self, page_size: str = 'A4'):
        """Apply page setup (size, margins, etc.)."""
        section = self.document.sections[0]

        # Page size
        width, height = PageLayout.SIZES.get(page_size, PageLayout.SIZES['A4'])
        section.page_width = width
        section.page_height = height

        # Margins
        section.top_margin = PageLayout.MARGIN_TOP
        section.bottom_margin = PageLayout.MARGIN_BOTTOM
        section.left_margin = PageLayout.MARGIN_LEFT
        section.right_margin = PageLayout.MARGIN_RIGHT

        # Header/Footer distance
        section.header_distance = PageLayout.HEADER_DISTANCE
        section.footer_distance = PageLayout.FOOTER_DISTANCE

    def add_header(self, text: str):
        """Add header to the document."""
        section = self.document.sections[0]
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        header_para.text = text
        header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        header_para.style = self.document.styles['Normal']

        # Style the header text
        for run in header_para.runs:
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_FOOTER
            run.font.italic = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

    def add_footer_with_page_numbers(self, position: str = 'Bottom Center'):
        """Add footer with page numbers."""
        section = self.document.sections[0]
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()

        # Set alignment based on position
        if 'Center' in position:
            footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif 'Right' in position:
            footer_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            footer_para.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Add decorative line and page number
        run = footer_para.add_run('───── ')
        run.font.name = Fonts.DECORATIVE
        run.font.size = Fonts.SIZE_FOOTER
        run.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)

        # Add page number field
        self._add_page_number_field(footer_para)

        run = footer_para.add_run(' ─────')
        run.font.name = Fonts.DECORATIVE
        run.font.size = Fonts.SIZE_FOOTER
        run.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)

    def _add_page_number_field(self, paragraph):
        """Add a page number field to a paragraph."""
        run = paragraph.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')

        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)

        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_FOOTER
        run.font.color.rgb = Colors.hex_to_rgb(Colors.LIGHT_GRAY)


def create_styled_document(page_size: str = 'A4') -> tuple:
    """
    Create a new document from template with all styles set up.
    Returns (document, styles_manager) tuple.
    """
    from pathlib import Path

    # Try to load template, fallback to blank document
    template_path = Path(__file__).parent.parent.parent / 'templates' / 'guide-book-template.docx'

    if template_path.exists():
        document = Document(str(template_path))
        print(f"Loaded template: {template_path}")
    else:
        # Fallback to blank document if template not found
        document = Document()
        print(f"Template not found, using blank document: {template_path}")

    styles_manager = DocxStyles(document)
    styles_manager.apply_page_setup(page_size)
    return document, styles_manager
