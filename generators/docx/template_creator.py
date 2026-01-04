"""
Template Creator for Guide Book Generator.
Creates a .dotx template with all custom styles defined.
Uses values from styles/theme.py for consistency.
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path

from styles.theme import Colors, Fonts, Spacing, PageLayout


def create_guide_book_template():
    """Create the master template with all custom styles."""
    doc = Document()

    # === PAGE SETUP (from PageLayout) ===
    section = doc.sections[0]
    page_width, page_height = PageLayout.SIZES['A4']
    section.page_width = page_width
    section.page_height = page_height
    section.left_margin = PageLayout.MARGIN_LEFT
    section.right_margin = PageLayout.MARGIN_RIGHT
    section.top_margin = PageLayout.MARGIN_TOP
    section.bottom_margin = PageLayout.MARGIN_BOTTOM

    # === DEFINE CUSTOM STYLES ===
    styles = doc.styles

    # 1. Chapter Number Style (14pt to match HTML preview)
    style = styles.add_style('ChapterNumber', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_PART_HEADER  # 14pt for chapter number
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DANGER_RED)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

    # 2. Chapter Title Style
    style = styles.add_style('ChapterTitle', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_CHAPTER_TITLE
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style.paragraph_format.space_after = Spacing.PARA_AFTER_LARGE

    # 3. Part Header Style (Part A, Part B, etc.)
    style = styles.add_style('PartHeader', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_PART_HEADER
    style.font.bold = True
    style.paragraph_format.space_before = Spacing.PARA_BEFORE_SECTION
    style.paragraph_format.space_after = Spacing.PARA_AFTER_LARGE

    # 4. Section Title Style (Concept titles)
    style = styles.add_style('SectionTitle', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_SECTION_TITLE
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
    style.paragraph_format.space_before = Spacing.PARA_BEFORE_LARGE
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

    # 5. Body Text Style
    style = styles.add_style('BodyText', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL
    style.paragraph_format.line_spacing = Fonts.LINE_SPACING_NORMAL

    # 6. Bullet Point Style
    style = styles.add_style('BulletPoint', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.paragraph_format.left_indent = Inches(0.25)
    style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

    # 7. Box Title Style (for Learning Objectives, Chapter Contents, etc.)
    style = styles.add_style('BoxTitle', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_CONCEPT_TITLE
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

    # 8. Alert Text Style (for Syllabus Alert, warnings)
    style = styles.add_style('AlertText', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DANGER_RED)

    # 9. Memory Trick Style
    style = styles.add_style('MemoryTrick', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.italic = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

    # 10. NCERT Quote Style
    style = styles.add_style('NCERTQuote', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.italic = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
    style.paragraph_format.left_indent = Inches(0.25)

    # 11. Table Header Style
    style = styles.add_style('TableHeader', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

    # 12. Table Cell Style
    style = styles.add_style('TableCell', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

    # 13. Decorative Line Style
    style = styles.add_style('DecorativeLine', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style.paragraph_format.space_before = Spacing.PARA_BEFORE_NORMAL
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

    # 14. Metadata Value Style (for Weightage, Importance, etc.)
    style = styles.add_style('MetadataValue', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_TABLE_HEADER
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DANGER_RED)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 15. Part Label Style (Part A:, Part B:, etc.)
    style = styles.add_style('PartLabel', WD_STYLE_TYPE.CHARACTER)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_TABLE_HEADER
    style.font.bold = True
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DANGER_RED)

    # 16. Question Style
    style = styles.add_style('Question', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.paragraph_format.space_before = Spacing.PARA_BEFORE_NORMAL
    style.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

    # 17. Answer Style
    style = styles.add_style('Answer', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_BODY_SMALL
    style.paragraph_format.left_indent = Inches(0.25)
    style.paragraph_format.space_after = Spacing.PARA_AFTER_NORMAL

    # 18. Header Text Style (for page headers)
    style = styles.add_style('HeaderText', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = Fonts.PRIMARY
    style.font.size = Fonts.SIZE_SECTION_TITLE
    style.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Save template
    template_dir = Path('templates')
    template_dir.mkdir(exist_ok=True)
    template_path = template_dir / 'guide-book-template.docx'
    doc.save(template_path)

    print(f'Template created: {template_path}')
    print(f'Styles defined: {len([s for s in doc.styles if s.type == WD_STYLE_TYPE.PARAGRAPH])} paragraph styles')

    return template_path


if __name__ == '__main__':
    create_guide_book_template()
