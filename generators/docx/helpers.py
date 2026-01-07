"""
DOCX helper functions for Guide Book Generator.
Provides utilities for creating tables, boxes, and formatted text.
"""

import re
from typing import Dict, List, Optional, Tuple

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table, _Cell

from styles.theme import BoxStyles, Colors, Fonts, Icons, Spacing


class DocxHelpers:
    """
    Helper class for creating formatted DOCX elements.
    """

    @staticmethod
    def set_cell_background(cell: _Cell, hex_color: str):
        """Set background color of a table cell."""
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), hex_color.lstrip('#'))
        cell._tc.get_or_add_tcPr().append(shading)

    @staticmethod
    def set_cell_borders(cell: _Cell, border_color: str = '#E5E7EB',
                         top: bool = True, bottom: bool = True,
                         left: bool = True, right: bool = True):
        """Set borders on a table cell."""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        tcBorders = OxmlElement('w:tcBorders')

        border_settings = [
            ('w:top', top),
            ('w:bottom', bottom),
            ('w:left', left),
            ('w:right', right),
        ]

        for border_name, enabled in border_settings:
            border = OxmlElement(border_name)
            if enabled:
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4')
                border.set(qn('w:color'), border_color.lstrip('#'))
            else:
                border.set(qn('w:val'), 'nil')
            tcBorders.append(border)

        tcPr.append(tcBorders)

    @staticmethod
    def set_cell_padding(cell: _Cell, padding: int = 100):
        """Set padding inside a table cell (in twips)."""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        tcMar = OxmlElement('w:tcMar')
        for margin_name in ['w:top', 'w:bottom', 'w:left', 'w:right']:
            margin = OxmlElement(margin_name)
            margin.set(qn('w:w'), str(padding))
            margin.set(qn('w:type'), 'dxa')
            tcMar.append(margin)

        tcPr.append(tcMar)

    @staticmethod
    def set_cell_left_border_only(cell: _Cell, border_color: str, border_width: str = '24'):
        """Set only left border on a cell (for professional info boxes)."""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        tcBorders = OxmlElement('w:tcBorders')

        # Left border - thick colored
        left = OxmlElement('w:left')
        left.set(qn('w:val'), 'single')
        left.set(qn('w:sz'), border_width)  # 24 = 3pt thick
        left.set(qn('w:color'), border_color.lstrip('#'))
        tcBorders.append(left)

        # Other borders - none
        for border_name in ['w:top', 'w:bottom', 'w:right']:
            border = OxmlElement(border_name)
            border.set(qn('w:val'), 'nil')
            tcBorders.append(border)

        tcPr.append(tcBorders)

    @staticmethod
    def set_table_borders(table: Table, border_color: str = '#E5E7EB'):
        """Set borders on entire table."""
        tbl = table._tbl
        tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

        tblBorders = OxmlElement('w:tblBorders')
        for border_name in ['w:top', 'w:left', 'w:bottom', 'w:right', 'w:insideH', 'w:insideV']:
            border = OxmlElement(border_name)
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '4')
            border.set(qn('w:color'), border_color.lstrip('#'))
            tblBorders.append(border)

        tblPr.append(tblBorders)

    @staticmethod
    def remove_table_borders(table: Table):
        """Remove all borders from a table."""
        tbl = table._tbl
        tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

        tblBorders = OxmlElement('w:tblBorders')
        for border_name in ['w:top', 'w:left', 'w:bottom', 'w:right', 'w:insideH', 'w:insideV']:
            border = OxmlElement(border_name)
            border.set(qn('w:val'), 'nil')
            tblBorders.append(border)

        tblPr.append(tblBorders)

    @staticmethod
    def create_colored_box(document: Document, content: str, bg_color: str,
                          title: Optional[str] = None, title_color: str = None,
                          icon: str = "", border_color: str = None) -> Table:
        """
        Create a colored box with optional title.
        Uses a single-cell table for the box effect.
        """
        # Create single-cell table
        table = document.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Set table width to full page width minus margins
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)

        # Set background color
        DocxHelpers.set_cell_background(cell, bg_color)

        # Set border if specified
        if border_color:
            DocxHelpers.set_cell_borders(cell, border_color)
        else:
            DocxHelpers.set_cell_borders(cell, bg_color)  # Match background for subtle border

        # Set padding
        DocxHelpers.set_cell_padding(cell, 150)

        # Add title if provided
        if title:
            title_para = cell.paragraphs[0]
            if icon:
                run = title_para.add_run(f"{icon} ")
                run.font.size = Fonts.SIZE_CONCEPT_TITLE
            run = title_para.add_run(title)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_CONCEPT_TITLE
            run.font.bold = True
            if title_color:
                run.font.color.rgb = Colors.hex_to_rgb(title_color)

            # Add content in new paragraph
            content_para = cell.add_paragraph()
        else:
            content_para = cell.paragraphs[0]

        # Add content with markdown parsing
        DocxHelpers.add_formatted_text(content_para, content)

        return table

    @staticmethod
    def create_styled_box(document: Document, box_type: str, title: str,
                          content: str = None, content_items: list = None) -> Table:
        """
        Create a professionally styled box with left border.
        box_type: 'info', 'tip', 'warning', 'neutral'
        content_items: list of strings for bullet points (optional)
        """
        # Get style config
        styles = {
            'info': BoxStyles.INFO,
            'tip': BoxStyles.TIP,
            'warning': BoxStyles.WARNING,
            'neutral': BoxStyles.NEUTRAL,
        }
        style = styles.get(box_type, BoxStyles.NEUTRAL)

        # Create single-cell table
        table = document.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)

        # Set background
        DocxHelpers.set_cell_background(cell, style['bg'])

        # Set left border only (professional look)
        if style['border'] != '#E5E7EB':  # Not neutral
            DocxHelpers.set_cell_left_border_only(cell, style['border'])
        else:
            DocxHelpers.set_cell_borders(cell, style['border'])

        # Set padding
        DocxHelpers.set_cell_padding(cell, 150)

        # Title with icon
        para = cell.paragraphs[0]

        if style['icon']:
            run = para.add_run(f"{style['icon']} ")
            run.font.size = Fonts.SIZE_BODY

        run = para.add_run(title)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(style['title_color'])

        # Add content if provided
        if content:
            para = cell.add_paragraph()
            DocxHelpers.add_formatted_text(para, content)

        # Add bullet items if provided
        if content_items:
            for item in content_items:
                para = cell.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.15)
                run = para.add_run("• ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY
                DocxHelpers.add_formatted_text(para, item)

        return table

    @staticmethod
    def create_info_box(document: Document, content: str, box_type: str = 'info') -> Table:
        """
        Create a pre-styled info box using unified system.
        box_type: 'info', 'warning', 'success', 'tip', 'ncert', 'memory', 'didyouknow', 'contents'
        """
        # Map legacy types to new system
        type_mapping = {
            'info': ('info', 'Learning Objectives'),
            'warning': ('warning', 'Syllabus Alert'),
            'success': ('tip', 'Memory Trick'),
            'tip': ('tip', 'Did You Know?'),
            'ncert': ('info', 'NCERT Exact Line'),
            'memory': ('tip', 'Memory Trick'),
            'didyouknow': ('tip', 'Did You Know?'),
            'contents': ('neutral', 'Chapter Contents'),
        }

        mapped = type_mapping.get(box_type, ('neutral', 'Note'))
        return DocxHelpers.create_styled_box(document, mapped[0], mapped[1], content)

    @staticmethod
    def add_formatted_text(paragraph, text: str, default_color: str = None, highlight_years: bool = False):
        """
        Add text with markdown formatting to a paragraph using robust HTML parsing.
        """
        if not text:
            return

        # DEBUG: Log input
        # print(f"Processing formatted text: '{text[:30]}...'")

        try:
            import markdown
            from bs4 import BeautifulSoup, NavigableString
        except ImportError as e:
            print(f"ERROR: Missing dependencies for markdown formatting: {e}")
            run = paragraph.add_run(text)
            if default_color:
                run.font.color.rgb = Colors.hex_to_rgb(default_color)
            return

        # Convert markdown to HTML (fragments only)
        try:
            # nl2br helps preserve single newlines
            html = markdown.markdown(text, extensions=['nl2br', 'tables'])
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            print(f"ERROR: Markdown conversion failed: {e}")
            run = paragraph.add_run(text)
            return

        # Recursive function to traverse HTML and add runs
        def process_node(node, style_context=None):
            if style_context is None:
                style_context = {'bold': False, 'italic': False}

            if isinstance(node, NavigableString):
                text_content = str(node)
                if not text_content:
                    return

                # Handle Year Highlighting (if enabled)
                if highlight_years:
                    import re
                    parts = re.split(r'\b(1[789]\d{2}|20\d{2})\b', text_content)
                    for i, part in enumerate(parts):
                        if not part: continue
                        
                        run = paragraph.add_run(part)
                        run.font.name = Fonts.PRIMARY
                        run.font.size = Fonts.SIZE_BODY
                        run.font.bold = style_context['bold']
                        run.font.italic = style_context['italic']
                        
                        if i % 2 == 1: # Year match
                            run.font.bold = True
                            run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)
                        elif default_color:
                            run.font.color.rgb = Colors.hex_to_rgb(default_color)
                else:
                    run = paragraph.add_run(text_content)
                    run.font.name = Fonts.PRIMARY
                    run.font.size = Fonts.SIZE_BODY
                    run.font.bold = style_context['bold']
                    run.font.italic = style_context['italic']
                    if default_color:
                        run.font.color.rgb = Colors.hex_to_rgb(default_color)

            elif node.name in ['strong', 'b']:
                new_context = style_context.copy()
                new_context['bold'] = True
                for child in node.children:
                    process_node(child, new_context)
            
            elif node.name in ['em', 'i']:
                new_context = style_context.copy()
                new_context['italic'] = True
                for child in node.children:
                    process_node(child, new_context)
            
            elif node.name == 'br':
                paragraph.add_run('\n')
                
            elif node.name in ['p', 'div', 'span']:
                # If this isn't the first child, add a newline
                # (but since we're usually in a single-purpose call, 
                # we just process children)
                for child in node.children:
                    process_node(child, style_context)
                    
            elif node.name == 'li':
                paragraph.add_run('\n• ')
                for child in node.children:
                    process_node(child, style_context)
            
            elif node.name in ['ul', 'ol']:
                for child in node.children:
                    process_node(child, style_context)

        # Process the soup
        # If there are multiple paragraphs, we flattened them above.
        # Note: This method is designed to add content to an EXISTING paragraph.
        for child in soup.children:
            process_node(child)

    @staticmethod
    def create_metadata_table(document: Document, data: Dict[str, Tuple[str, str]], styles=None) -> Table:
        """
        Create metadata table like: | Weightage: X | Map Work: Y | Importance: Z | Frequency: W |
        data format: {'label': ('value', 'color')}
        styles: optional document.styles for applying named styles
        """
        cols = len(data)
        table = document.add_table(rows=1, cols=cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Set column widths
        for col in table.columns:
            col.width = Inches(6.5 / cols)

        # Check if MetadataValue style is available
        has_metadata_style = styles and 'MetadataValue' in [s.name for s in styles]

        # Fill cells
        for idx, (label, (value, color)) in enumerate(data.items()):
            cell = table.cell(0, idx)
            DocxHelpers.set_cell_background(cell, Colors.BG_LIGHT_GRAY)
            DocxHelpers.set_cell_borders(cell, Colors.BORDER_GRAY)
            DocxHelpers.set_cell_padding(cell, 80)

            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            if has_metadata_style:
                # Use named style
                para.style = styles['MetadataValue']
                para.add_run(f"{label} ")
                run = para.add_run(value)
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(color)
            else:
                # Fallback: inline formatting for backward compatibility
                run = para.add_run(f"{label} ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY_SMALL
                run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)

                run = para.add_run(value)
                run.font.name = Fonts.PRIMARY
                run.font.size = Fonts.SIZE_BODY_SMALL
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(color)

        return table

    @staticmethod
    def create_pyq_table(document: Document, questions: List[Dict],
                        year_range: str = "2015-2024") -> Table:
        """
        Create PYQ analysis table with Question, Marks, Years Asked columns.
        """
        if not questions:
            return None

        # Create table with header
        table = document.add_table(rows=1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        DocxHelpers.set_table_borders(table, Colors.BORDER_GRAY)

        # Set column widths
        table.columns[0].width = Inches(4.0)  # Question
        table.columns[1].width = Inches(0.75)  # Marks
        table.columns[2].width = Inches(1.75)  # Years

        # Header row
        headers = ['Question', 'Marks', 'Years Asked']
        header_row = table.rows[0]
        for idx, header in enumerate(headers):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)  # Light blue
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_TABLE_HEADER
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)  # Dark gray text

        # Data rows
        for q in questions:
            row = table.add_row()

            # Calculate frequency for row coloring
            years = q.get('years', '')
            year_count = len([y.strip() for y in years.split(',') if y.strip()])

            # Determine row background based on frequency
            row_bg = None
            if year_count >= 6:
                row_bg = '#FEF2F2'  # Light red for 6+ times (high frequency)
            elif year_count == 5:
                row_bg = '#EFF6FF'  # Light blue for 5 times
            elif year_count >= 3:
                row_bg = '#F0FDF4'  # Light green for 3-4 times

            # Question cell
            cell = row.cells[0]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            DocxHelpers.add_formatted_text(para, q.get('question', ''))

            # Marks cell
            cell = row.cells[1]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(q.get('marks', '3M'))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

            # Years cell
            cell = row.cells[2]
            if row_bg:
                DocxHelpers.set_cell_background(cell, row_bg)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Text color based on frequency
            color = Colors.get_pyq_frequency_color(year_count)

            run = para.add_run(years)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY_SMALL
            run.font.color.rgb = Colors.hex_to_rgb(color)

        return table

    @staticmethod
    def create_comparison_table(document: Document, title: str,
                               headers: List[str], rows: List[List[str]]) -> Table:
        """Create a comparison table with colored header."""
        if not rows:
            return None

        cols = len(headers)
        table = document.add_table(rows=1, cols=cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        DocxHelpers.set_table_borders(table, Colors.BORDER_GRAY)

        # Header row - all same blue background
        header_row = table.rows[0]
        for idx, header in enumerate(headers):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)  # Consistent light blue
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_TABLE_HEADER
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)  # Blue text on light blue bg

        # Data rows
        for row_data in rows:
            row = table.add_row()
            for idx, cell_text in enumerate(row_data):
                cell = row.cells[idx]
                DocxHelpers.set_cell_padding(cell, 80)
                para = cell.paragraphs[0]
                DocxHelpers.add_formatted_text(para, cell_text)

        return table

    @staticmethod
    def add_decorative_line(document: Document, line_char: str = '━', count: int = 34):
        """Add a decorative horizontal line."""
        para = document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(line_char * count)
        run.font.name = Fonts.DECORATIVE
        run.font.size = Pt(12)
        run.font.color.rgb = Colors.hex_to_rgb(Colors.DARK_GRAY)
        return para

    @staticmethod
    def add_page_break(document: Document):
        """Add a page break only if document has existing content."""
        # Check if document has any content (more than just the default empty paragraph)
        has_content = False
        for para in document.paragraphs:
            if para.text.strip():
                has_content = True
                break
        # Also check if there are any tables
        if not has_content and len(document.tables) > 0:
            has_content = True

        # Only add page break if there's existing content
        if has_content:
            document.add_page_break()

    @staticmethod
    def add_numbered_list(document: Document, items: List[str],
                         start_num: int = 1, bold_numbers: bool = True):
        """Add a numbered list."""
        for idx, item in enumerate(items, start=start_num):
            para = document.add_paragraph()

            # Number
            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            if bold_numbers:
                run.font.bold = True

            # Content
            DocxHelpers.add_formatted_text(para, item)

    @staticmethod
    def add_bullet_list(document: Document, items: List[str], bullet: str = '•'):
        """Add a bullet list."""
        for item in items:
            para = document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)

            # Bullet
            run = para.add_run(f"{bullet} ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY

            # Content
            DocxHelpers.add_formatted_text(para, item)

    @staticmethod
    def add_mcq_answers_grid(document: Document, answers: List[str], per_row: int = 10):
        """Add MCQ answers in a grid format."""
        if not answers:
            return

        rows_needed = (len(answers) + per_row - 1) // per_row
        table = document.add_table(rows=rows_needed, cols=per_row)
        table.alignment = WD_TABLE_ALIGNMENT.LEFT

        for idx, answer in enumerate(answers):
            row_idx = idx // per_row
            col_idx = idx % per_row
            cell = table.cell(row_idx, col_idx)
            para = cell.paragraphs[0]
            run = para.add_run(f"{idx + 1}({answer})")
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY_SMALL

        DocxHelpers.remove_table_borders(table)

    # =========================================================================
    # BOOK STANDARD FORMATTING HELPERS
    # =========================================================================

    @staticmethod
    def add_section_header(document: Document, text: str, level: int = 2):
        """
        Add a section header following BOOK STANDARD formatting.

        Args:
            document: The document to add to
            text: Header text (e.g., "1. The French Revolution")
            level: 2 for Heading 2 (16pt), 3 for Heading 3 (14pt)

        BOOK STANDARD:
        - Level 2: 16pt, blue (#2563EB), used for main section headers
        - Level 3: 14pt, blue (#2563EB), used for subsection headers
        """
        para = document.add_paragraph()

        run = para.add_run(text)
        run.font.name = Fonts.PRIMARY

        if level == 2:
            run.font.size = Pt(16)
        else:
            run.font.size = Pt(14)

        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        para.paragraph_format.space_before = Spacing.PARA_BEFORE_LARGE
        para.paragraph_format.space_after = Spacing.PARA_AFTER_SMALL

        return para

    @staticmethod
    def add_memory_trick(document: Document, acronym: str, explanation: str):
        """
        Add a memory trick following BOOK STANDARD formatting.

        BOOK STANDARD:
        - Right-aligned
        - Green color (#059669)
        - "Memory Trick: " in italic
        - Acronym in bold italic
        - Explanation in italic

        Example: Memory Trick: FLAT-CUN — Flag, Language, Assembly, Taxes...
        """
        para = document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # "Memory Trick: "
        run = para.add_run("Memory Trick: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Acronym (bold italic)
        run = para.add_run(acronym)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # " — " separator
        run = para.add_run(" — ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Explanation (italic)
        run = para.add_run(explanation)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        return para

    @staticmethod
    def add_ncert_box(document: Document, content: str) -> Table:
        """
        Add an NCERT Exact Line box following BOOK STANDARD.

        BOOK STANDARD:
        - Light blue background (#EFF6FF)
        - Blue left border (#1E40AF)
        - Icon: 📌
        - Title: "NCERT Exact Line"
        """
        table = document.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)

        # Set background
        DocxHelpers.set_cell_background(cell, Colors.BG_INFO)

        # Set left border only
        DocxHelpers.set_cell_left_border_only(cell, Colors.BORDER_INFO)

        # Set padding
        DocxHelpers.set_cell_padding(cell, 150)

        # Title
        para = cell.paragraphs[0]
        run = para.add_run("📌 ")
        run.font.size = Fonts.SIZE_BODY

        run = para.add_run("NCERT Exact Line: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.PRIMARY_BLUE)

        # Content (quoted)
        run = para.add_run(f'"{content}"')
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.italic = True

        return table

    @staticmethod
    def add_did_you_know_box(document: Document, content: str) -> Table:
        """
        Add a Did You Know box following BOOK STANDARD.

        BOOK STANDARD:
        - Light orange background (#FFF7ED)
        - Orange left border (#D97706)
        - Icon: ★ (Icons.TIP)
        - Title: "Did You Know?"
        """
        table = document.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)

        # Set background
        DocxHelpers.set_cell_background(cell, '#FFF7ED')

        # Set left border only
        DocxHelpers.set_cell_left_border_only(cell, Colors.WARNING_ORANGE)

        # Set padding
        DocxHelpers.set_cell_padding(cell, 150)

        # Title
        para = cell.paragraphs[0]
        run = para.add_run(f"{Icons.TIP} ")
        run.font.size = Fonts.SIZE_BODY

        run = para.add_run("Did You Know? ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.WARNING_ORANGE)

        # Content
        run = para.add_run(content)
        run.font.name = Fonts.PRIMARY
        run.font.size = Fonts.SIZE_BODY

        return table

    @staticmethod
    def create_timeline_table(document: Document, events: List[Dict[str, str]]) -> Table:
        """
        Create a timeline table following BOOK STANDARD.

        Args:
            events: List of {'year': '1789', 'event': 'French Revolution begins'}

        BOOK STANDARD:
        - 2 columns: Year | Event
        - Header row with blue background
        - Years in bold
        """
        if not events:
            return None

        table = document.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        DocxHelpers.set_table_borders(table, Colors.BORDER_GRAY)

        # Set column widths
        table.columns[0].width = Inches(1.0)
        table.columns[1].width = Inches(5.5)

        # Header row
        header_row = table.rows[0]
        for idx, header in enumerate(['Year', 'Event']):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_TABLE_HEADER
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Data rows
        for event in events:
            row = table.add_row()

            # Year cell
            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(event.get('year', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True

            # Event cell
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            DocxHelpers.add_formatted_text(para, event.get('event', ''))

        return table

    @staticmethod
    def create_key_terms_table(document: Document, terms: List[Dict[str, str]]) -> Table:
        """
        Create a key terms table following BOOK STANDARD.

        Args:
            terms: List of {'term': 'Nationalism', 'definition': 'A sense of...'}

        BOOK STANDARD:
        - 2 columns: Term | Definition
        - Header row with blue background
        - Terms in bold
        """
        if not terms:
            return None

        table = document.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        DocxHelpers.set_table_borders(table, Colors.BORDER_GRAY)

        # Set column widths
        table.columns[0].width = Inches(2.0)
        table.columns[1].width = Inches(4.5)

        # Header row
        header_row = table.rows[0]
        for idx, header in enumerate(['Term', 'Definition']):
            cell = header_row.cells[idx]
            DocxHelpers.set_cell_background(cell, Colors.TABLE_HEADER_BG)
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            run = para.add_run(header)
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_TABLE_HEADER
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Data rows
        for term_data in terms:
            row = table.add_row()

            # Term cell
            cell = row.cells[0]
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            run = para.add_run(term_data.get('term', ''))
            run.font.name = Fonts.PRIMARY
            run.font.size = Fonts.SIZE_BODY
            run.font.bold = True

            # Definition cell
            cell = row.cells[1]
            DocxHelpers.set_cell_padding(cell, 80)
            para = cell.paragraphs[0]
            DocxHelpers.add_formatted_text(para, term_data.get('definition', ''))

        return table
