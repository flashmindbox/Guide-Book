"""
Live Preview Component for Guide Book Generator.
Renders chapter data as styled HTML matching the DOCX output.
"""

import streamlit as st

from core.models.base import ChapterData
from core.models.parts import PartManager
from styles.theme import Colors, Icons
from utils.logger import get_logger

logger = get_logger(__name__)


class PreviewRenderer:
    """Renders chapter data as HTML preview."""

    # CSS styles - SYNCHRONIZED WITH DOCX OUTPUT (styles/theme.py, generators/docx/styles.py)
    # xhtml2pdf compatible: no flex, no border-radius, no box-shadow, simple block layout
    CSS = f"""
    <style>
        {Colors.to_css_variables()}

        /* =================================================================
           PAGE SETUP - Matches PageLayout in theme.py
           A4: 210mm x 297mm, Margins: 0.83in (21mm) top/left/right, 0.69in (17.5mm) bottom
           ================================================================= */
        @page {{
            size: A4;
            margin: 21mm 21mm 18mm 21mm;
        }}

        /* =================================================================
           GLOBAL STYLES - Matches Fonts class in theme.py
           PRIMARY = Arial, SIZE_BODY = 11pt, LINE_SPACING_SINGLE = 1.0
           ================================================================= */
        * {{
            word-wrap: break-word;
            overflow-wrap: break-word;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, 'Segoe UI', Helvetica, sans-serif;
            font-size: 11pt;
            line-height: 1.15;
            color: #374151;
            margin: 0;
            padding: 0;
            -pdf-keep-with-next: false;
        }}

        /* =================================================================
           CONTAINER - Main document wrapper
           A4 content width = 6.5in (matches DOCX margins)
           ================================================================= */
        .preview-container {{
            font-family: Arial, 'Segoe UI', Helvetica, sans-serif;
            max-width: 6.5in;
            margin: 0 auto;
            padding: 0;
            background: #FFFFFF;
        }}

        /* =================================================================
           COVER PAGE STYLES - Matches DocxStyles.ChapterTitle (24pt bold blue centered)
           ================================================================= */
        .preview-header {{
            text-align: center;
            padding: 12pt;
            background: #F9FAFB;
            border: 2pt solid #1E40AF;
            margin-bottom: 15pt;
        }}
        .preview-title {{
            font-size: 24pt;
            font-weight: bold;
            color: #1E40AF;
            margin: 6pt 0;
            line-height: 1.2;
        }}
        .preview-subtitle {{
            font-size: 11pt;
            color: #374151;
            margin: 3pt 0;
        }}
        .preview-chapter-num {{
            font-size: 14pt;
            font-weight: bold;
            color: #1E40AF;
        }}
        .decorative-line {{
            width: 60%;
            margin: 6pt auto;
            border: none;
            border-top: 2pt solid #2563EB;
            height: 0;
        }}

        /* =================================================================
           METADATA TABLE - Matches TableStyles in theme.py
           Header: TABLE_HEADER_BG = #DBEAFE, Border: 1pt solid #E5E7EB
           Cell padding: 6pt
           ================================================================= */
        .preview-meta-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
        }}
        .preview-meta-table th {{
            background: #DBEAFE;
            padding: 6pt;
            text-align: center;
            font-size: 10pt;
            font-weight: bold;
            border: 1pt solid #E5E7EB;
            color: #1E40AF;
        }}
        .preview-meta-table td {{
            padding: 6pt;
            text-align: center;
            font-weight: bold;
            font-size: 11pt;
            border: 1pt solid #E5E7EB;
            color: #374151;
        }}

        /* =================================================================
           ALERT BOX - Matches BoxStyles.WARNING in theme.py
           BG: #FEF2F2, Border: 4pt solid #B91C1C, Full width
           ================================================================= */
        .preview-alert {{
            width: 100%;
            background: #FEF2F2;
            border-left: 4pt solid #B91C1C;
            padding: 10pt 12pt;
            margin: 12pt 0;
            box-sizing: border-box;
        }}
        .preview-alert-title {{
            color: #B91C1C;
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 6pt;
        }}

        /* =================================================================
           LEARNING OBJECTIVES - Matches BoxStyles.INFO in theme.py
           BG: #EFF6FF, Border: 4pt solid #1E40AF, Full width
           ================================================================= */
        .preview-objectives {{
            width: 100%;
            background: #EFF6FF;
            border-left: 4pt solid #1E40AF;
            padding: 10pt 12pt;
            margin: 12pt 0;
            box-sizing: border-box;
        }}
        .preview-objectives-title {{
            color: #1E40AF;
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 6pt;
        }}

        /* =================================================================
           CONTENTS BOX - Matches BoxStyles.NEUTRAL in theme.py
           BG: #F9FAFB, Border: 1pt solid #E5E7EB, Full width
           ================================================================= */
        .preview-contents-box {{
            width: 100%;
            background: #F9FAFB;
            border: 1pt solid #E5E7EB;
            padding: 10pt 12pt;
            margin: 12pt 0;
            box-sizing: border-box;
        }}

        /* =================================================================
           PAGE BREAKS - DOCX compatible
           ================================================================= */
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        /* =================================================================
           PART HEADER - Matches DOCX part_b_concepts.py _add_part_header
           Full width, BG_WARNING (#FEF2F2), 18pt bold, YEAR_RED text
           ================================================================= */
        .preview-part-header {{
            page-break-before: always;
            break-before: page;
            width: 100%;
            background: #FEF2F2;
            border: none;
            padding: 12pt 15pt;
            margin: 24pt 0 12pt 0;
            box-sizing: border-box;
        }}
        .preview-part-text {{
            color: #DC2626;
            font-weight: bold;
            font-size: 18pt;
        }}

        /* =================================================================
           SECTION TITLE - Matches DocxStyles.SectionTitle (14pt bold blue)
           HEADING_BLUE = #2563EB
           ================================================================= */
        .preview-section-title {{
            color: #2563EB;
            font-weight: bold;
            font-size: 14pt;
            margin: 12pt 0 6pt 0;
            line-height: 1.2;
        }}

        /* =================================================================
           CONCEPT - Matches DOCX part_b_concepts.py _add_concept
           Title: 16pt bold HEADING_BLUE, space-before 18pt, space-after 6pt
           No box wrapper - just title and content inline
           ================================================================= */
        .preview-concept-title {{
            color: #2563EB;
            font-weight: bold;
            font-size: 16pt;
            margin: 18pt 0 6pt 0;
            line-height: 1.2;
        }}
        .preview-concept-content {{
            margin: 3pt 0;
            font-size: 11pt;
        }}

        /* Legacy box style - for compatibility with Part D source boxes */
        .preview-concept-box {{
            background: #F9FAFB;
            border: 1pt solid #E5E7EB;
            padding: 10pt;
            margin: 10pt 0;
        }}

        /* =================================================================
           NCERT LINE - Matches DOCX part_b_concepts.py lines 76-90
           Indented (0.3in), "NCERT Exact Line: " bold red, content in italic quotes
           No box - just indented text
           ================================================================= */
        .preview-ncert {{
            margin: 6pt 0;
            padding-left: 0.3in;
            font-size: 11pt;
        }}
        .preview-ncert-label {{
            font-weight: bold;
            color: #B91C1C;
            font-style: normal;
        }}
        .preview-ncert-content {{
            font-style: italic;
        }}

        /* =================================================================
           MEMORY TRICK - Matches DOCX part_b_concepts.py lines 97-113
           Right-aligned, green (#059669), 10pt, italic
           No box - just right-aligned text
           ================================================================= */
        .preview-memory-trick {{
            text-align: right;
            margin: 6pt 0;
            font-size: 10pt;
            color: #059669;
            font-style: italic;
        }}
        .preview-memory-label {{
            font-weight: bold;
            font-style: italic;
        }}
        .preview-memory-acronym {{
            font-weight: bold;
            font-style: italic;
        }}

        /* =================================================================
           DID YOU KNOW - Matches DOCX part_b_concepts.py lines 116-137
           Grey box (#F3F4F6), "Do You Know? " bold red (#DC2626), max 6.0in centered
           ================================================================= */
        .preview-dyk {{
            width: 100%;
            max-width: 6.0in;
            background: #F3F4F6;
            border: 1pt solid #E5E7EB;
            padding: 10pt 12pt;
            margin: 12pt auto;
            box-sizing: border-box;
        }}
        .preview-dyk-label {{
            color: #DC2626;
            font-weight: bold;
            font-size: 9pt;
        }}
        .preview-dyk-content {{
            font-size: 9pt;
        }}
        .preview-custom-box {{
            width: 100%;
            max-width: 6.0in;
            border: 1pt solid #E5E7EB;
            padding: 10pt 12pt;
            margin: 12pt auto;
            box-sizing: border-box;
            font-size: 9pt;
        }}
        .preview-custom-box-title {{
            font-weight: bold;
            font-size: 9pt;
        }}
        .preview-concept-table {{
            width: 100%;
            max-width: 6.0in;
            margin: 12pt auto;
            border-collapse: collapse;
        }}
        .preview-concept-table th {{
            background: #F3F4F6;
            font-weight: bold;
            font-size: 9pt;
            padding: 6pt 8pt;
            border: 1pt solid #D1D5DB;
            text-align: left;
        }}
        .preview-concept-table td {{
            font-size: 9pt;
            padding: 6pt 8pt;
            border: 1pt solid #D1D5DB;
        }}
        .preview-table-title {{
            font-size: 10pt;
            font-weight: bold;
            font-style: italic;
            margin: 12pt 0 6pt 0;
        }}

        /* =================================================================
           PYQ TABLE - Matches DOCX part_a_pyq.py lines 74-144
           Full width, Header: #DBEAFE, Cell padding 60 twips (~4pt)
           ================================================================= */
        .preview-pyq-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
        }}
        .preview-pyq-table th {{
            background: #DBEAFE;
            color: #374151;
            padding: 4pt 6pt;
            text-align: center;
            border: 1pt solid #E5E7EB;
            font-size: 11pt;
            font-weight: bold;
        }}
        .preview-pyq-table td {{
            padding: 4pt 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 11pt;
            color: #374151;
            vertical-align: top;
        }}
        .preview-pyq-table td.marks-cell {{
            text-align: center;
        }}
        .preview-pyq-table td.years-cell {{
            text-align: center;
            font-size: 10pt;
        }}

        /* =================================================================
           MARKS STYLING - ACCENT_RED = #B91C1C
           ================================================================= */
        .preview-marks {{
            color: #B91C1C;
            font-weight: bold;
        }}

        /* =================================================================
           PREDICTION BOX - Matches BoxStyles.INFO, Full width
           ================================================================= */
        .preview-prediction {{
            width: 100%;
            background: #EFF6FF;
            border-left: 4pt solid #1E40AF;
            padding: 10pt 12pt;
            margin: 12pt 0;
            box-sizing: border-box;
        }}

        /* =================================================================
           TIMELINE TABLE - Matches DOCX part_b_concepts.py lines 218-261
           Full width, Year cell: blue bg (#DBEAFE), bold red text, centered
           ================================================================= */
        .preview-timeline {{
            margin: 10pt 0;
        }}
        .preview-timeline-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0;
        }}
        .preview-timeline-table th {{
            background: #DBEAFE;
            color: #2563EB;
            padding: 4pt 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 11pt;
            font-weight: bold;
        }}
        .preview-timeline-table td {{
            padding: 4pt 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 11pt;
            vertical-align: top;
        }}
        .preview-timeline-table td.year-cell {{
            width: 15%;
            background: #DBEAFE;
            font-weight: bold;
            color: #B91C1C;
            text-align: center;
        }}
        .preview-timeline-table td.event-cell {{
            width: 85%;
            color: #374151;
        }}

        /* =================================================================
           MCQ BOX - Matches concept box styling
           ================================================================= */
        .preview-mcq {{
            background: #F9FAFB;
            padding: 10pt;
            margin: 8pt 0;
            border-left: 4pt solid #1E40AF;
        }}
        .preview-mcq-options {{
            margin-left: 15pt;
            margin-top: 6pt;
        }}

        /* =================================================================
           ANSWER BOX - Matches BoxStyles.TIP
           ================================================================= */
        .preview-answer {{
            background: #F0FDF4;
            border-left: 4pt solid #059669;
            padding: 10pt;
            margin: 10pt 0;
        }}

        /* =================================================================
           MARKING POINTS - Table-based for DOCX compatibility
           ================================================================= */
        .preview-marking-points {{
            margin: 8pt 0 8pt 10pt;
        }}
        .preview-marking-point {{
            color: #374151;
            padding: 3pt 0 3pt 15pt;
            font-size: 10pt;
        }}
        .preview-marking-point-mark {{
            color: #B91C1C;
            font-size: 9pt;
            margin-left: 5pt;
        }}

        /* =================================================================
           MAP ITEMS
           ================================================================= */
        .preview-map-item {{
            padding: 3pt 0;
            padding-left: 15pt;
            font-size: 11pt;
        }}

        /* =================================================================
           CHECKLIST
           ================================================================= */
        .preview-checklist {{
            padding: 3pt 0;
            font-size: 11pt;
        }}

        /* =================================================================
           MISTAKE TABLE - Two-column comparison
           ================================================================= */
        .preview-mistake-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
        }}
        .preview-mistake-table th.mistake {{
            background: #FEF2F2;
            color: #B91C1C;
            padding: 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 10pt;
            font-weight: bold;
        }}
        .preview-mistake-table th.correct {{
            background: #F0FDF4;
            color: #059669;
            padding: 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 10pt;
            font-weight: bold;
        }}
        .preview-mistake-table td {{
            padding: 6pt;
            border: 1pt solid #E5E7EB;
            font-size: 10pt;
            color: #374151;
            vertical-align: top;
        }}

        /* =================================================================
           DIVIDERS AND END MARKERS
           ================================================================= */
        .preview-divider {{
            border-top: 1pt solid #E5E7EB;
            margin: 15pt 0;
        }}
        .preview-end-marker {{
            text-align: center;
            color: #1E40AF;
            font-weight: bold;
            font-size: 11pt;
            margin-top: 20pt;
        }}

        /* =================================================================
           QR CODE TABLE
           ================================================================= */
        .qr-table {{
            width: 100%;
            margin: 12pt 0;
        }}
        .qr-cell {{
            text-align: center;
            padding: 10pt;
            width: 50%;
            vertical-align: top;
        }}

        /* =================================================================
           IMPORTANCE COLORS - Matches Colors class
           ================================================================= */
        .importance-high {{ color: #B91C1C; font-weight: bold; }}
        .importance-medium {{ color: #D97706; font-weight: bold; }}
        .importance-low {{ color: #059669; font-weight: bold; }}

        /* =================================================================
           TEXT FORMATTING - Matches character styles
           ================================================================= */
        .year-text {{
            color: #DC2626;
            font-weight: bold;
        }}
        .key-term {{
            font-weight: bold;
            color: #000000;
        }}
        .foreign-term {{
            font-weight: bold;
            font-style: italic;
            color: #000000;
        }}

        /* =================================================================
           PREVENT OVERFLOW
           ================================================================= */
        div, td, th {{
            max-width: 100%;
            word-wrap: break-word;
        }}
        table {{
            -pdf-keep-with-next: false;
            word-wrap: break-word;
            table-layout: fixed;
        }}
    </style>
    """

    @classmethod
    def _get_page_number_css(cls, data: ChapterData) -> str:
        """Generate page number CSS based on data settings."""
        if not getattr(data, 'add_page_numbers', False):
            return ""

        position = getattr(data, 'page_number_position', 'Bottom Center').lower()
        if 'center' in position:
            align = 'center'
        elif 'right' in position:
            align = 'right'
        else:
            align = 'left'

        page_size = getattr(data, 'page_size', 'A4')

        return f'''
        <style>
        @media print {{
            @page {{
                size: {page_size};
                margin: 20mm 15mm 25mm 15mm;
                @bottom-{align} {{
                    content: "Page " counter(page);
                    font-size: 10pt;
                    color: #666;
                }}
            }}
        }}
        </style>
        '''

    @classmethod
    def render_full_preview(cls, data: ChapterData, part_manager: PartManager) -> str:
        """Render complete chapter preview."""

        # Dynamic page number CSS based on settings
        page_number_css = cls._get_page_number_css(data)

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    {cls.CSS}
    {page_number_css}
</head>
<body>
<div class="preview-container">
'''

        # Cover page
        html += cls._render_cover(data)

        # Enabled parts
        enabled_parts = part_manager.get_enabled_parts()

        for part in enabled_parts:
            if part.id == 'A':
                html += cls._render_part_a(data)
            elif part.id == 'B':
                html += cls._render_part_b(data)
            elif part.id == 'C':
                html += cls._render_part_c(data)
            elif part.id == 'D':
                html += cls._render_part_d(data)
            elif part.id == 'E':
                html += cls._render_part_e(data)
            elif part.id == 'F':
                html += cls._render_part_f(data)
            elif part.id == 'G':
                html += cls._render_part_g(data)

        # End marker
        html += f'''
        <div class="preview-divider"></div>
        <div class="preview-end-marker">End of Chapter {data.chapter_number}</div>
        '''

        html += '</div></body></html>'

        # Make PDF-safe by replacing emojis
        html = cls._pdf_safe_text(html)
        return html

    @classmethod
    def render_cover_preview(cls, data: ChapterData) -> str:
        """Render cover page preview only."""

        # Dynamic page number CSS based on settings
        page_number_css = cls._get_page_number_css(data)

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    {cls.CSS}
    {page_number_css}
</head>
<body>
<div class="preview-container">
'''
        html += cls._render_cover(data)
        html += '</div></body></html>'

        # Make PDF-safe by replacing emojis
        html = cls._pdf_safe_text(html)
        return html

    @classmethod
    def render_part_preview(cls, data: ChapterData, part_id: str) -> str:
        """Render a specific part preview."""

        # Dynamic page number CSS based on settings
        page_number_css = cls._get_page_number_css(data)

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    {cls.CSS}
    {page_number_css}
</head>
<body>
<div class="preview-container">
'''

        if part_id == 'A':
            html += cls._render_part_a(data)
        elif part_id == 'B':
            html += cls._render_part_b(data)
        elif part_id == 'C':
            html += cls._render_part_c(data)
        elif part_id == 'D':
            html += cls._render_part_d(data)
        elif part_id == 'E':
            html += cls._render_part_e(data)
        elif part_id == 'F':
            html += cls._render_part_f(data)
        elif part_id == 'G':
            html += cls._render_part_g(data)

        html += '</div></body></html>'

        # Make PDF-safe by replacing emojis
        html = cls._pdf_safe_text(html)
        return html

    @classmethod
    def _render_cover(cls, data: ChapterData) -> str:
        """Render cover page section - MATCHES DOCX STRUCTURE EXACTLY (cover_page.py)."""
        subject_display = data.subject.replace('_', ' ').title()

        # Decorative line: solid 2pt blue line, 60% width, centered
        separator_line = '<div class="decorative-line"></div>'

        # Header - matches DOCX _add_header (line 45-56): 11pt, centered, DARK_GRAY
        html = f'''
        <div style="text-align: center; margin-bottom: 6pt;">
            <div style="font-size: 11pt; color: #374151;">CBSE Class {data.class_num} | Social Science | {subject_display}</div>
        </div>

        {separator_line}

        <!-- Chapter Number - matches DOCX line 75-79: 18pt bold HEADING_BLUE -->
        <div style="text-align: center; margin: 12pt 0 6pt 0;">
            <span style="font-size: 18pt; font-weight: bold; color: #2563EB;">CHAPTER {data.chapter_number}</span>
        </div>

        <!-- Chapter Title - matches DOCX line 85-89: 24pt bold HEADING_BLUE -->
        <div style="text-align: center; margin-bottom: 12pt;">
            <span style="font-size: 24pt; font-weight: bold; color: #2563EB;">{data.chapter_title}</span>
        </div>
        '''

        # Subtitle if present - matches DOCX line 92-98: 12pt italic
        if data.subtitle:
            html += f'''
        <div style="text-align: center; margin-bottom: 6pt;">
            <span style="font-size: 12pt; font-style: italic;">{data.subtitle}</span>
        </div>
            '''

        html += separator_line

        # Metadata as inline text with | separators - matches DOCX _add_metadata (lines 100-150)
        importance_color = '#B91C1C' if data.importance == 'High' else '#374151'
        freq_color = '#B91C1C' if data.pyq_frequency == 'Every Year' else '#374151'

        html += f'''
        <div style="text-align: center; font-size: 10pt; margin: 12pt 0;">
            <span style="font-weight: bold;">Weightage:</span>
            <span style="color: #2563EB;">{data.weightage}</span>
            <span style="color: #374151;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
            <span style="font-weight: bold;">Map Work:</span>
            <span>{data.map_work}</span>
            <span style="color: #374151;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
            <span style="font-weight: bold;">Importance:</span>
            <span style="color: {importance_color};">{data.importance}</span>
            <span style="color: #374151;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
            <span style="font-weight: bold;">PYQ:</span>
            <span style="color: {freq_color};">{data.pyq_frequency}</span>
        </div>
        '''

        # Syllabus Alert - matches DOCX _add_syllabus_alert (lines 152-165): inline text, not a box
        if data.syllabus_alert_enabled and data.syllabus_alert_text:
            html += f'''
        <div style="margin: 12pt 0;">
            <span style="font-size: 11pt; font-weight: bold; color: #B91C1C;">! SYLLABUS NOTE:</span>
            <span style="font-size: 11pt;"> {data.syllabus_alert_text}</span>
        </div>
            '''

        # Learning Objectives - matches DOCX _add_learning_objectives (lines 167-203)
        if data.learning_objectives:
            # Parse objectives into list
            objectives = [obj.strip() for obj in data.learning_objectives.strip().split('\n') if obj.strip()]
            clean_objectives = []
            for obj in objectives:
                if obj.startswith(('-', '•', '*')):
                    obj = obj[1:].strip()
                clean_objectives.append(obj)

            html += f'''
        <!-- Learning Objectives Header - matches DOCX line 182-186: 14pt bold HEADING_BLUE -->
        <div style="margin: 18pt 0 6pt 0;">
            <span style="font-size: 14pt; font-weight: bold; color: #2563EB;">{Icons.TARGET} Learning Objectives</span>
        </div>
        <!-- Subtitle - matches DOCX line 191-194: 11pt italic -->
        <div style="margin-bottom: 6pt;">
            <span style="font-size: 11pt; font-style: italic;">After studying this chapter, you will be able to:</span>
        </div>
            '''
            # Bullet points - matches DOCX lines 197-203: 0.25in left indent, bullet
            for obj in clean_objectives:
                html += f'''
        <div style="margin: 3pt 0; padding-left: 18pt; font-size: 11pt;">• {obj}</div>
                '''

        # Chapter Contents - matches DOCX _add_chapter_contents (lines 205-234)
        if data.part_descriptions:
            html += f'''
        <!-- Chapter Contents Header - matches DOCX line 211-215: 14pt bold HEADING_BLUE -->
        <div style="margin: 18pt 0 6pt 0;">
            <span style="font-size: 14pt; font-weight: bold; color: #2563EB;">{Icons.BOOK} Chapter Contents</span>
        </div>
            '''
            # Part list - matches DOCX lines 222-234: 0.25in left indent
            for part_id, desc in data.part_descriptions.items():
                if desc:
                    html += f'''
        <div style="margin: 3pt 0; padding-left: 18pt; font-size: 11pt;">
            <span style="font-weight: bold; color: #2563EB;">Part {part_id}:</span>
            <span> {desc}</span>
        </div>
                    '''

        # QR Codes Section - using TABLE layout instead of flex (xhtml2pdf compatible)
        if data.qr_practice_questions_url or data.qr_practice_with_answers_url:
            html += '''
            <div style="background: var(--bg-info); border: 2px solid var(--primary-blue); padding: 15px; margin: 15px 0;">
                <div style="color: #1E40AF; font-weight: bold; font-size: 14pt; margin-bottom: 5px; text-align: center;">
                    Download Extra Practice Materials
                </div>
                <div style="color: #374151; font-size: 10pt; text-align: center; margin-bottom: 15px;">
                    Use your phone camera to scan these QR codes and download PDF worksheets
                </div>
                <table class="qr-table">
                    <tr>
            '''

            if data.qr_practice_questions_url:
                qr_img_1 = cls._generate_qr_base64(data.qr_practice_questions_url)
                if qr_img_1:
                    html += f'''
                        <td class="qr-cell">
                            <img src="data:image/png;base64,{qr_img_1}" width="100" height="100"/>
                            <br/>
                            <span style="font-size: 11pt; color: #1E40AF; font-weight: bold;">Practice Questions</span>
                            <br/>
                            <span style="font-size: 9pt; color: #374151;">(Questions Only - For Self Practice)</span>
                        </td>
                    '''

            if data.qr_practice_with_answers_url:
                qr_img_2 = cls._generate_qr_base64(data.qr_practice_with_answers_url)
                if qr_img_2:
                    html += f'''
                        <td class="qr-cell">
                            <img src="data:image/png;base64,{qr_img_2}" width="100" height="100"/>
                            <br/>
                            <span style="font-size: 11pt; color: #059669; font-weight: bold;">Questions + Answers</span>
                            <br/>
                            <span style="font-size: 9pt; color: #374151;">(Complete Solutions Included)</span>
                        </td>
                    '''

            html += '</tr></table></div>'

        return html

    @classmethod
    def _generate_qr_base64(cls, url: str) -> str:
        """Generate QR code as base64 string."""
        try:
            import base64
            from io import BytesIO

            import qrcode

            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)

            return base64.b64encode(buf.getvalue()).decode('utf-8')
        except Exception as e:
            logger.warning("Failed to generate QR code for URL '%s': %s", url, e)
            return ""

    @classmethod
    def _render_part_a(cls, data: ChapterData) -> str:
        """Render Part A: PYQ Analysis - matches DOCX part_a_pyq.py structure."""
        # Part header - matches DOCX _add_part_header
        html = f'''
        <div class="preview-part-header">
            <span class="preview-part-text">Part A: PYQ Analysis ({data.pyq_year_range})</span>
        </div>
        '''

        # PYQ Table - matches DOCX _add_pyq_table
        if data.pyq_items:
            html += '''
            <table class="preview-pyq-table">
                <tr>
                    <th style="width:62%; text-align:left;">Question</th>
                    <th style="width:12%;">Marks</th>
                    <th style="width:26%;">Years Asked</th>
                </tr>
            '''
            for item in data.pyq_items:
                if not item.question:
                    continue
                # Calculate frequency for row coloring
                years = item.years or ''
                year_count = len([y.strip() for y in years.split(',') if y.strip()])

                # Row background color based on frequency (matches DOCX logic)
                row_bg = ''
                if year_count >= 6:
                    row_bg = 'background: #FEF2F2;'  # Light red
                elif year_count == 5:
                    row_bg = 'background: #EFF6FF;'  # Light blue
                elif year_count >= 3:
                    row_bg = 'background: #F0FDF4;'  # Light green

                html += f'''
                <tr style="{row_bg}">
                    <td>{item.question}</td>
                    <td class="marks-cell">{item.marks}</td>
                    <td class="years-cell">{item.years}</td>
                </tr>
                '''
            html += '</table>'

        # Prediction - matches DOCX _add_prediction (simple inline text)
        if data.pyq_prediction:
            next_year = cls._get_next_year(data.pyq_year_range)
            html += f'''
            <div style="margin: 12pt 0 6pt 0;">
                <span style="font-size: 11pt; font-weight: bold; color: #2563EB;">{Icons.TARGET} Prediction {next_year}: </span>
                <span style="font-size: 11pt;">{data.pyq_prediction}</span>
            </div>
            '''

        # Frequency Legend - matches DOCX _add_frequency_legend
        html += '''
        <div style="margin: 12pt 0; font-size: 10pt;">
            <span style="font-weight: bold;">Frequency: </span>
            <span style="color: #B91C1C;">Red</span> = 6+ times &nbsp;&nbsp;
            <span style="color: #2563EB;">Blue</span> = 5 times &nbsp;&nbsp;
            <span style="color: #059669;">Green</span> = 3-4 times
        </div>
        '''

        # Syllabus Note - matches DOCX _add_syllabus_note (simple inline text)
        if data.pyq_syllabus_note:
            html += f'''
            <div style="margin: 12pt 0;">
                <span style="font-size: 11pt; font-weight: bold; color: #059669;">{Icons.TIP} Syllabus Note: </span>
                <span style="font-size: 11pt;">{data.pyq_syllabus_note}</span>
            </div>
            '''

        return html

    @staticmethod
    def _get_next_year(year_range: str) -> str:
        """Get the next year for prediction."""
        try:
            end_year = int(year_range.split('-')[1])
            return str(end_year + 1)
        except (ValueError, IndexError, AttributeError):
            return "2025"

    @classmethod
    def _render_part_b(cls, data: ChapterData) -> str:
        """Render Part B: Key Concepts - matches DOCX part_b_concepts.py structure."""
        # Part header - matches DOCX _add_part_header
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part B: Key Concepts</span>
        </div>
        '''

        # Concepts - matches DOCX _add_concept
        for concept in data.concepts:
            if concept.is_empty():
                continue

            # Concept title - 16pt blue, no box wrapper
            html += f'''
            <div class="preview-concept-title">{concept.number}. {concept.title or 'Untitled'}</div>
            '''

            # NCERT line - indented, bold red label, italic content in quotes
            if concept.ncert_line:
                html += f'''
            <div class="preview-ncert">
                <span class="preview-ncert-label">NCERT Exact Line: </span>
                <span class="preview-ncert-content">"{concept.ncert_line}"</span>
            </div>
                '''

            # Content - formatted text
            if concept.content:
                content_html = cls._format_concept_content(concept.content)
                html += f'<div class="preview-concept-content">{content_html}</div>'

            # Memory trick - right-aligned, green, italic
            if concept.memory_trick:
                html += f'''
            <div class="preview-memory-trick">
                <span class="preview-memory-label">Memory Trick: </span>
                <span>{concept.memory_trick}</span>
            </div>
                '''

            # Did You Know - grey box with red label
            if concept.did_you_know:
                html += f'''
            <div class="preview-dyk">
                <span class="preview-dyk-label">Do You Know? </span>
                <span class="preview-dyk-content">{concept.did_you_know}</span>
            </div>
                '''

            # Custom Boxes
            for box in concept.custom_boxes:
                if box.title or box.content:
                    title_html = f'<span class="preview-custom-box-title">{box.title}: </span>' if box.title else ''
                    html += f'''
            <div class="preview-custom-box" style="background: {box.background_color};">
                {title_html}<span>{box.content}</span>
            </div>
                    '''

            # Concept Tables
            for tbl in concept.tables:
                if tbl.headers and tbl.rows:
                    if tbl.title:
                        html += f'<div class="preview-table-title">{tbl.title}</div>'
                    html += '<table class="preview-concept-table"><thead><tr>'
                    for header in tbl.headers:
                        html += f'<th>{header}</th>'
                    html += '</tr></thead><tbody>'
                    for row in tbl.rows:
                        html += '<tr>'
                        for cell in row:
                            html += f'<td>{cell}</td>'
                        html += '</tr>'
                    html += '</tbody></table>'

        # Comparison Tables - matches DOCX _add_comparison_tables
        if data.comparison_tables:
            html += f'''
            <div class="preview-section-title" style="margin-top: 18pt;">{Icons.CHART} Comparison Tables</div>
            '''
            for table in data.comparison_tables:
                table_title = table.get('title', 'Comparison')
                headers = table.get('headers', [])
                rows = table.get('rows', [])

                html += f'''
            <div style="margin: 12pt 0 6pt 0; font-weight: bold; font-style: italic;">{table_title}</div>
            <table class="preview-pyq-table"><tr>
                '''
                for header in headers:
                    html += f'<th style="color: #1E40AF;">{header}</th>'
                html += '</tr>'
                for row in rows:
                    html += '<tr>'
                    for cell in row:
                        html += f'<td>{cls._format_text(cell)}</td>'
                    html += '</tr>'
                html += '</table>'

        # Common Mistakes - matches DOCX _add_common_mistakes
        if data.common_mistakes:
            html += f'''
            <div class="preview-section-title" style="color: #B91C1C; margin-top: 18pt;">{Icons.WARNING} Common Mistakes to Avoid</div>
            '''
            for mistake in data.common_mistakes:
                html += f'''
            <div style="margin: 3pt 0; padding-left: 18pt;">
                {Icons.WRONG} {cls._format_text(mistake)}
            </div>
                '''

        # Important Dates Timeline - matches DOCX _add_important_dates
        if data.important_dates:
            html += f'''
            <div class="preview-section-title" style="margin-top: 18pt;">{Icons.CALENDAR} Important Dates Timeline</div>
            <table class="preview-timeline-table">
            '''
            for date_item in data.important_dates:
                year = date_item.get('year', '')
                event = date_item.get('event', '')
                html += f'''
                <tr>
                    <td class="year-cell">{year}</td>
                    <td class="event-cell">{cls._format_text(event)}</td>
                </tr>
                '''
            html += '</table>'

        return html

    @classmethod
    def _format_concept_content(cls, content: str) -> str:
        """Format concept content with bullet points and numbering."""
        if not content:
            return ''

        lines = content.strip().split('\n')
        html = ''

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if it's a bullet point
            if line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                line = line[1:].strip()
                html += f'<div style="padding-left: 18pt; margin: 3pt 0;">• {cls._format_text(line)}</div>'

            # Check if it's a numbered point
            elif line[0].isdigit() and '.' in line[:3]:
                html += f'<div style="padding-left: 18pt; margin: 3pt 0;">{cls._format_text(line)}</div>'

            else:
                html += f'<div style="margin: 3pt 0;">{cls._format_text(line)}</div>'

        return html

    @classmethod
    def _render_part_c(cls, data: ChapterData) -> str:
        """Render Part C: Model Answers - matches DOCX structure."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part C: Model Answers</span>
        </div>
        '''

        for idx, answer in enumerate(data.model_answers, 1):
            if not answer.question:
                continue

            # Question title - matches concept title styling
            html += f'''
            <div class="preview-concept-title">Q{idx}. {answer.question} <span class="preview-marks" style="font-size: 11pt;">[{answer.marks}M]</span></div>
            '''

            # Answer - styled answer box
            if answer.answer:
                html += f'''
            <div class="preview-answer">
                <strong>Answer:</strong><br/>
                {cls._format_text(answer.answer)}
            </div>
                '''

            # Marking Points - indented list
            if answer.marking_points:
                html += '<div class="preview-marking-points"><strong>Marking Points:</strong>'
                for point in answer.marking_points:
                    html += f'<div class="preview-marking-point">{point}<span class="preview-marking-point-mark">(1 mark)</span></div>'
                html += '</div>'

        return html

    @classmethod
    def _render_part_d(cls, data: ChapterData) -> str:
        """Render Part D: Practice Questions - matches DOCX structure."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part D: Practice Questions</span>
        </div>
        '''

        # MCQs
        if data.mcqs:
            html += '<div class="preview-section-title">Multiple Choice Questions (1 Mark)</div>'
            # Difficulty legend
            html += '''
            <div style="font-size: 9pt; margin-bottom: 10px;">
                <span style="color: var(--success-green);">[E] Easy</span>&nbsp;&nbsp;
                <span style="color: var(--warning-orange);">[M] Medium</span>&nbsp;&nbsp;
                <span style="color: var(--accent-red);">[H] Hard</span>
            </div>
            '''
            for idx, mcq in enumerate(data.mcqs, 1):
                if not mcq.question:
                    continue
                # Difficulty tag color
                difficulty = getattr(mcq, 'difficulty', 'M') or 'M'
                diff_colors = {'E': 'var(--success-green)', 'M': 'var(--warning-orange)', 'H': 'var(--accent-red)'}
                diff_color = diff_colors.get(difficulty, 'var(--warning-orange)')
                html += f'''
                <div class="preview-mcq">
                    <span style="color: {diff_color}; font-weight: bold;">[{difficulty}]</span> <strong>Q{idx}.</strong> {mcq.question}
                    <div class="preview-mcq-options">
                '''
                for i, opt in enumerate(mcq.options or []):
                    if opt:
                        letter = chr(97 + i)
                        is_answer = letter == mcq.answer
                        style = 'color: var(--success-green); font-weight: bold;' if is_answer else ''
                        html += f'<div style="{style}">({letter}) {opt}</div>'
                html += '</div></div>'
            # MCQ Answer Key Box
            mcq_answers = [f"{idx}({mcq.answer})" for idx, mcq in enumerate(data.mcqs, 1) if mcq.answer]
            if mcq_answers:
                html += f'''
                <div style="background: var(--bg-tip); border-left: 4px solid var(--border-tip); padding: 10px 15px; margin: 15px 0;">
                    <strong style="color: var(--success-green);">{Icons.CORRECT} Answers (MCQs):</strong>
                    <div style="margin-top: 5px;">{" &nbsp; ".join(mcq_answers)}</div>
                </div>
                '''

        # Assertion-Reason
        if data.assertion_reason:
            html += '<div class="preview-section-title">Assertion-Reason Questions (1 Mark)</div>'
            # AR Instructions box
            html += '''
            <div style="background: #F9FAFB; padding: 10px 15px; margin: 10px 0; font-size: 10pt;">
                <div style="font-style: italic; margin-bottom: 8px;">
                    Directions: In the following questions, a statement of Assertion (A) is followed by a statement of Reason (R). Choose the correct option.
                </div>
                <div style="padding-left: 15px;">
                    (a) Both A and R are true and R is the correct explanation of A<br/>
                    (b) Both A and R are true but R is NOT the correct explanation of A<br/>
                    (c) A is true but R is false<br/>
                    (d) A is false but R is true
                </div>
            </div>
            '''
            for idx, ar in enumerate(data.assertion_reason, 1):
                if not ar.question:
                    continue
                html += f'''
                <div class="preview-mcq">
                    <strong>Q{idx}.</strong><br>{ar.question.replace(chr(10), '<br>')}
                    <div style="margin-top: 5px; color: var(--success-green);">
                        <strong>Answer: ({ar.answer})</strong>
                    </div>
                </div>
                '''
            # AR Answer Key Box
            ar_answers = [f"{idx}({ar.answer})" for idx, ar in enumerate(data.assertion_reason, 1) if ar.answer]
            if ar_answers:
                html += f'''
                <div style="background: var(--bg-tip); border-left: 4px solid var(--border-tip); padding: 10px 15px; margin: 15px 0;">
                    <strong style="color: var(--success-green);">{Icons.CORRECT} Answers (Assertion-Reason):</strong>
                    <div style="margin-top: 5px;">{" &nbsp; ".join(ar_answers)}</div>
                </div>
                '''

        # Short Answer
        if data.short_answer:
            html += '<div class="preview-section-title">Short Answer Questions (3 Marks)</div>'
            for idx, q in enumerate(data.short_answer, 1):
                if q.question:
                    html += f'<div class="preview-map-item"><strong>Q{idx}.</strong> {q.question}</div>'

        # Long Answer
        if data.long_answer:
            html += '<div class="preview-section-title">Long Answer Questions (5 Marks)</div>'
            for idx, q in enumerate(data.long_answer, 1):
                if q.question:
                    html += f'<div class="preview-map-item"><strong>Q{idx}.</strong> {q.question}</div>'

        # HOTS Questions
        if data.hots:
            html += '<div class="preview-section-title">Higher Order Thinking Skills (HOTS)</div>'
            for idx, question in enumerate(data.hots, 1):
                if question.question:
                    html += f'<div class="preview-map-item"><strong>Q{idx}.</strong> {question.question}'
                    if question.hint:
                        html += f'<div style="color: var(--success-green); font-style: italic; margin-top: 5px;">{Icons.TIP} Hint: {question.hint}</div>'
                    html += '</div>'

        # Source-Based Questions
        if data.source_based:
            html += '<div class="preview-section-title">Source-Based Questions</div>'
            for idx, item in enumerate(data.source_based, 1):
                source_text = item.get('source', '')
                questions = item.get('questions', [])
                # Source box
                html += f'''
                <div class="preview-concept-box">
                    <div style="font-weight: bold; font-style: italic;">Source {chr(64 + idx)}:</div>
                    <div style="font-style: italic;">"{source_text}"</div>
                </div>
                '''
                # Sub-questions
                for q_idx, q in enumerate(questions, 1):
                    q_text = q.get('question', '')
                    q_marks = q.get('marks', 1)
                    roman = cls._roman(q_idx)
                    html += f'<div class="preview-map-item">({roman}) {q_text} <span class="preview-marks">[{q_marks}]</span></div>'

        # Case Study Questions
        if data.case_study:
            html += '<div class="preview-section-title">Case Study Questions (NEW PATTERN)</div>'
            for idx, item in enumerate(data.case_study, 1):
                title = item.get('title', f'Case Study {idx}')
                passage = item.get('passage', '')
                questions = item.get('questions', [])
                # Title
                html += f'<div style="font-weight: bold; color: var(--primary-blue); margin: 10px 0 5px 0;">Case Study: {title}</div>'
                # Passage box
                html += f'''
                <div class="preview-concept-box">
                    {passage}
                </div>
                '''
                # Sub-questions
                for q_idx, q in enumerate(questions, 1):
                    q_text = q.get('question', '')
                    q_marks = q.get('marks', 1)
                    roman = cls._roman(q_idx)
                    html += f'<div class="preview-map-item">({roman}) {q_text} <span class="preview-marks">[{q_marks}]</span></div>'

        # Competency-Based Questions
        if data.competency_based:
            html += '<div class="preview-section-title">Competency-Based Questions (CBQs)</div>'
            for idx, question in enumerate(data.competency_based, 1):
                if question.question:
                    html += f'<div class="preview-map-item"><strong>Q{idx}.</strong> {question.question}'
                    if question.hint:
                        html += f'<div style="color: var(--success-green); font-style: italic; margin-top: 5px;">{Icons.TIP} Hint: {question.hint}</div>'
                    html += '</div>'

        # Value-Based Questions
        if data.value_based:
            html += '<div class="preview-section-title">Value-Based Questions</div>'
            for idx, question in enumerate(data.value_based, 1):
                if question.question:
                    html += f'<div class="preview-map-item"><strong>Q{idx}.</strong> {question.question}'
                    if question.hint:
                        html += f'<div style="color: var(--success-green); font-style: italic; margin-top: 5px;">{Icons.TIP} Hint: {question.hint}</div>'
                    html += '</div>'

        return html

    @classmethod
    def _render_part_e(cls, data: ChapterData) -> str:
        """Render Part E: Map Work - matches DOCX structure."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part E: Map Work</span>
        </div>
        '''

        if data.map_work_na or data.map_work == "No":
            html += '''
            <div style="text-align: center; padding: 30px; background: var(--bg-neutral);">
                <div style="font-size: 14pt; color: var(--body-text);">
                    &gt; No Map Work from this Chapter
                </div>
            </div>
            '''
        else:
            if data.map_items:
                html += '<div class="preview-section-title">&gt; CBSE Prescribed Map Locations</div>'
                for idx, item in enumerate(data.map_items, 1):
                    html += f'<div class="preview-map-item">{idx}. {item}</div>'

            if data.map_tips:
                html += f'''
                <div class="preview-memory-trick">
                    <span class="preview-memory-label">&gt; Map Marking Tips</span><br/>
                    {data.map_tips.replace(chr(10), '<br/>')}
                </div>
                '''

        return html

    @classmethod
    def _render_part_f(cls, data: ChapterData) -> str:
        """Render Part F: Quick Revision - matches DOCX structure."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part F: Quick Revision</span>
        </div>
        '''

        # Key Points
        if data.revision_key_points:
            html += '<div class="preview-section-title">1. Key Points Summary</div>'
            html += '<div class="preview-concept-box">'
            for idx, point in enumerate(data.revision_key_points, 1):
                html += f'<div><span style="color: var(--primary-blue); font-weight:bold;">{idx}.</span> {cls._format_text(point)}</div>'
            html += '</div>'

        # Key Terms
        if data.revision_key_terms:
            html += '<div class="preview-section-title">2. Key Terms Defined</div>'
            html += '''<table class="preview-pyq-table">
                <tr><th>Term</th><th>Definition</th></tr>
            '''
            for term in data.revision_key_terms:
                html += f'''<tr>
                    <td style="font-weight:bold; color: var(--primary-blue);">{term.get('term', '')}</td>
                    <td>{term.get('definition', '')}</td>
                </tr>'''
            html += '</table>'

        # Memory Tricks
        if data.revision_memory_tricks:
            html += '''
            <div class="preview-section-title">&gt; Memory Tricks Compilation</div>
            <div class="preview-memory-trick">
            '''
            for trick in data.revision_memory_tricks:
                html += f'<div>&gt; {cls._format_text(trick)}</div>'
            html += '</div>'

        return html

    @classmethod
    def _render_part_g(cls, data: ChapterData) -> str:
        """Render Part G: Exam Strategy - matches DOCX structure."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-text">Part G: Exam Strategy</span>
        </div>
        '''

        # Time Allocation
        if data.time_allocation:
            html += '<div class="preview-section-title">&gt; Time Allocation Guide</div>'
            html += '''<table class="preview-pyq-table">
                <tr><th>Question Type</th><th>Marks</th><th>Time</th></tr>
            '''
            for item in data.time_allocation:
                html += f'''<tr>
                    <td>{item.get('type', '')}</td>
                    <td style="font-weight:bold;">{item.get('marks', '')}</td>
                    <td>{item.get('time', '')}</td>
                </tr>'''
            html += '</table>'

        # Common Mistakes
        if data.common_mistakes_exam:
            html += f'<div class="preview-section-title" style="color: var(--accent-red);">{Icons.WRONG} WHAT LOSES MARKS</div>'
            html += '''<table class="preview-mistake-table">
                <tr><th class="mistake">MISTAKE</th><th class="correct">WHAT TO DO INSTEAD</th></tr>
            '''
            for item in data.common_mistakes_exam:
                html += f'''<tr>
                    <td style="color: var(--accent-red);">{item.get('mistake', '')}</td>
                    <td>{item.get('correction', '')}</td>
                </tr>'''
            html += '</table>'

        # Pro Tips
        if data.examiner_pro_tips:
            html += f'<div class="preview-section-title" style="color: var(--success-green);">{Icons.TIP} Examiner\'s Pro Tips</div>'
            for tip in data.examiner_pro_tips:
                html += f'<div class="preview-map-item">{Icons.CORRECT} {cls._format_text(tip)}</div>'

        # Checklist
        if data.self_assessment_checklist:
            html += '<div class="preview-section-title">3. Self-Assessment Checklist</div>'
            for item in data.self_assessment_checklist:
                html += f'<div class="preview-checklist">☐ {item}</div>'

        return html

    @staticmethod
    def _roman(n: int) -> str:
        """Convert number to roman numeral (lowercase)."""
        numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        return numerals[n - 1] if 1 <= n <= 10 else str(n)

    @classmethod
    def _format_text(cls, text: str) -> str:
        """Format text with robust markdown conversion."""
        if not text:
            return ''

        import markdown
        
        # Convert markdown to HTML
        # We use extensions for tables and lists
        html = markdown.markdown(text, extensions=['tables', 'nl2br'])
        
        # Post-process for xhtml2pdf compatibility (convert <p> to <div> or similar if needed)
        # but usually markdown is fine. We just need to make sure tags are closed.
        
        return html

    @staticmethod
    def _pdf_safe_text(text: str) -> str:
        """Replace multi-byte emojis and box-drawing characters with PDF-safe alternatives."""
        if not text:
            return ''

        # Emoji to PDF-safe Unicode replacements
        replacements = {
            '🎯': '◎',
            '📑': '■',
            '⚠️': '⚠',
            '📊': '■',
            '📖': '■',
            '✅': '✓',
            '❌': '✗',
            '💡': '★',
            '⭐': '★',
            '⏱️': '○',
            '📝': '■',
            '🗺️': '■',
            '🧠': '■',
            '📌': '▸',
            '📅': '■',
            '☑️': '☐',
            '📄': '■',
            '📕': '■',
            '📱': '■',
            # Box-drawing characters that may cause encoding issues
            '─': '-',  # Light horizontal (U+2500)
            '━': '=',  # Heavy horizontal (U+2501)
            '═': '=',  # Double horizontal (U+2550)
            '│': '|',  # Light vertical (U+2502)
            '┃': '|',  # Heavy vertical (U+2503)
            '║': '|',  # Double vertical (U+2551)
        }

        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)

        return text


def show_preview_panel(data: ChapterData, part_manager: PartManager = None,
                       part_id: str = None, show_full: bool = False):
    """
    Display a quick HTML preview panel in Streamlit with download options.

    Args:
        data: Chapter data to preview
        part_manager: Part manager (required for full preview)
        part_id: Specific part to preview (e.g., 'A', 'B', etc.)
        show_full: Whether to show full document preview
    """
    import base64

    import streamlit.components.v1 as components

    with st.expander("👁️ Quick Preview", expanded=False):
        # Generate content HTML based on what to preview
        if show_full and part_manager:
            html = PreviewRenderer.render_full_preview(data, part_manager)
        elif part_id:
            html = PreviewRenderer.render_part_preview(data, part_id)
        else:
            html = PreviewRenderer.render_cover_preview(data)

        # Display the HTML preview with increased height
        components.html(html, height=1200, scrolling=True)

        st.divider()

        # Print button - centered
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            # Print button (centered)
            b64_html = base64.b64encode(html.encode()).decode()
            print_script = f'''
            <a href="javascript:void(0);"
               onclick="var w=window.open('','_blank','width=900,height=700');
                        w.document.write(atob('{b64_html}'));
                        w.document.close();
                        setTimeout(function(){{w.print();}}, 500);"
               style="display:inline-block;
                      padding:0.5rem 1rem;
                      background:#ff4b4b;
                      color:white;
                      border-radius:0.5rem;
                      text-decoration:none;
                      font-size:14px;
                      font-weight:500;
                      text-align:center;
                      width:100%;
                      box-sizing:border-box;">
               Print
            </a>
            '''
            components.html(print_script, height=42)


# =============================================================================
# NEW PDF-BASED PREVIEW SYSTEM
# =============================================================================

def _compute_data_hash(data: ChapterData) -> str:
    """Compute a hash of the chapter data for change detection."""
    import hashlib
    import json
    # Use a subset of key fields for faster hashing
    key_data = {
        'title': data.chapter_title,
        'subject': data.subject,
        'chapter_number': data.chapter_number,
        'concepts_count': len(data.concepts),
        'mcqs_count': len(data.mcqs),
        'model_answers_count': len(data.model_answers),
        'learning_objectives': data.learning_objectives[:100] if data.learning_objectives else '',
    }
    data_str = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()[:12]


def show_pdf_preview(data: ChapterData, part_manager: PartManager):
    """
    Enhanced preview with Quick (HTML) and Accurate (PDF from DOCX) modes.

    - Quick Preview: Instant HTML preview while editing
    - Accurate Preview: Generate DOCX → Convert to PDF → Show exact output
    """
    import base64

    import streamlit.components.v1 as components

    from generators.docx.base import DocumentGenerator
    from generators.pdf.converter import PDFConverter

    st.subheader("📄 Document Preview & Download")

    # Compute current data hash for change detection
    current_hash = _compute_data_hash(data)

    # Check if data has changed since last preview
    preview_hash = st.session_state.get('preview_data_hash')
    data_changed = preview_hash is not None and preview_hash != current_hash

    if data_changed and st.session_state.get('preview_docx'):
        st.warning("⚠️ **Data has changed** since the last preview was generated. Click 'Generate Preview' to update.")

    # Create two tabs for different preview modes
    tab_quick, tab_accurate = st.tabs(["⚡ Quick Preview (HTML)", "🎯 Accurate Preview (PDF)"])

    # ==========================================================================
    # TAB 1: QUICK PREVIEW (HTML) - Instant, while editing
    # ==========================================================================
    with tab_quick:
        st.caption("Fast preview while editing. May differ slightly from final DOCX output.")

        # Render HTML preview instantly
        try:
            html_content = PreviewRenderer.render_full_preview(data, part_manager)

            # Add print button above preview
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                b64_html = base64.b64encode(html_content.encode()).decode()
                print_script = f'''
                <a href="javascript:void(0);"
                   onclick="var w=window.open('','_blank','width=900,height=700');
                            w.document.write(atob('{b64_html}'));
                            w.document.close();
                            setTimeout(function(){{w.print();}}, 500);"
                   style="display:inline-block;
                          padding:0.4rem 1rem;
                          background:#4CAF50;
                          color:white;
                          border-radius:0.5rem;
                          text-decoration:none;
                          font-size:13px;
                          font-weight:500;
                          text-align:center;">
                   🖨️ Print HTML
                </a>
                '''
                components.html(print_script, height=40)

            # Display HTML preview
            components.html(html_content, height=800, scrolling=True)

            st.info("💡 This is a quick HTML preview. For exact DOCX/PDF output with proper pagination, use the **Accurate Preview** tab.")

        except Exception as e:
            logger.error("Error rendering quick HTML preview: %s", e, exc_info=True)
            st.error(f"Error rendering preview: {str(e)}")

    # ==========================================================================
    # TAB 2: ACCURATE PREVIEW (PDF from DOCX) - Exact output
    # ==========================================================================
    with tab_accurate:
        st.caption("Exact preview of final document. Click Generate to create/update.")

        # Check PDF conversion availability
        html_pdf_available = PDFConverter.is_html_pdf_available()
        docx_pdf_available, method = PDFConverter.is_available()

        if not html_pdf_available and not docx_pdf_available:
            st.warning("""
                ⚠️ **PDF preview not available**

                Install xhtml2pdf for PDF support: `pip install xhtml2pdf`

                You can still generate and download the DOCX file.
            """)

        # Generate Preview button
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            generate_clicked = st.button(
                "🔄 Generate Preview",
                type="primary",
                use_container_width=True,
                help="Generate the document to see exact preview and download"
            )

        if generate_clicked:
            with st.spinner("Generating document (this may take a few seconds)..."):
                try:
                    # Step 1: Generate DOCX
                    generator = DocumentGenerator(data, part_manager)
                    docx_bytes = generator.generate_to_bytes()

                    # Store DOCX in session state
                    st.session_state['preview_docx'] = docx_bytes
                    st.session_state['preview_generated'] = True

                    # Step 2: Try to convert to PDF
                    pdf_bytes = None
                    preview_source = None

                    # Try DOCX-to-PDF first (most accurate)
                    if docx_pdf_available:
                        with st.spinner("Converting DOCX to PDF..."):
                            pdf_bytes = PDFConverter.convert_bytes(docx_bytes)
                            if pdf_bytes:
                                preview_source = 'docx'

                    # Fallback to HTML-to-PDF
                    if not pdf_bytes and html_pdf_available:
                        with st.spinner("Generating PDF from HTML..."):
                            html_content = PreviewRenderer.render_full_preview(data, part_manager)
                            pdf_bytes = PDFConverter.convert_html_to_pdf(html_content)
                            if pdf_bytes:
                                preview_source = 'html'
                                st.session_state['preview_html'] = html_content

                    # Store results
                    if pdf_bytes:
                        st.session_state['preview_pdf'] = pdf_bytes
                        st.session_state['preview_source'] = preview_source
                    else:
                        st.session_state['preview_pdf'] = None
                        st.session_state['preview_source'] = None

                    # Store data hash to track changes
                    st.session_state['preview_data_hash'] = current_hash

                    st.success("✅ Preview generated successfully!")
                    st.rerun()

                except Exception as e:
                    logger.error("Error generating document preview: %s", e, exc_info=True)
                    st.error(f"Error generating document: {str(e)}")

        # Display preview source indicator
        if st.session_state.get('preview_pdf') and st.session_state.get('preview_source'):
            source = st.session_state['preview_source']
            if source == 'docx':
                st.success("✅ This preview exactly matches the DOCX output (converted via Word/LibreOffice)")
            elif source == 'html':
                st.info("ℹ️ PDF generated from HTML. Download DOCX for exact formatting.")

        # Display PDF preview if available
        if st.session_state.get('preview_pdf'):
            pdf_bytes = st.session_state['preview_pdf']
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

            # PDF viewer iframe
            pdf_display = f'''
                <iframe
                    src="data:application/pdf;base64,{base64_pdf}"
                    width="100%"
                    height="800px"
                    style="border: 1px solid #ddd; border-radius: 8px;"
                    type="application/pdf">
                    <p>Your browser doesn't support PDF preview. Please download the file.</p>
                </iframe>
            '''
            components.html(pdf_display, height=820)

        elif st.session_state.get('preview_docx') and not st.session_state.get('preview_pdf'):
            st.info("📝 PDF preview not available. Download DOCX to view the document in Microsoft Word or LibreOffice.")

        elif not st.session_state.get('preview_generated'):
            st.info("👆 Click **'Generate Preview'** to see the exact document preview")

        # Download buttons
        if st.session_state.get('preview_docx') or st.session_state.get('preview_pdf'):
            st.divider()

            # Safe filename
            safe_title = "".join(c for c in data.chapter_title[:20] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_') if safe_title else 'Chapter'

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.session_state.get('preview_docx'):
                    filename = f"Ch{data.chapter_number}_{data.subject}_{safe_title}.docx"
                    st.download_button(
                        "⬇️ Download DOCX",
                        data=st.session_state['preview_docx'],
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

            with col2:
                if st.session_state.get('preview_pdf'):
                    filename = f"Ch{data.chapter_number}_{data.subject}_{safe_title}.pdf"
                    st.download_button(
                        "⬇️ Download PDF",
                        data=st.session_state['preview_pdf'],
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )

            with col3:
                if st.button("🗑️ Clear Preview", use_container_width=True):
                    clear_preview_cache()
                    st.rerun()


def show_section_preview(data: ChapterData, section: str = "cover"):
    """
    Quick HTML preview for individual sections during editing.
    This is a lightweight preview for immediate feedback while editing.

    Args:
        data: Chapter data to preview
        section: Section to preview - 'cover', 'A', 'B', 'C', 'D', 'E', 'F', 'G'
    """
    import streamlit.components.v1 as components

    with st.expander("👁️ Quick Preview", expanded=False):
        # Use existing HTML renderer for quick feedback
        if section == "cover":
            html = PreviewRenderer.render_cover_preview(data)
        else:
            html = PreviewRenderer.render_part_preview(data, section)

        components.html(html, height=500, scrolling=True)

        st.caption("💡 For accurate pagination with page breaks, use **'Generate Preview'** on the Generate page.")


def clear_preview_cache():
    """Clear all preview-related session state."""
    keys_to_clear = [
        'preview_docx',
        'preview_pdf',
        'preview_generated',
        'preview_html',
        'preview_source',
        'preview_data_hash'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def show_generate_docx_button(data: ChapterData, part_manager: PartManager = None, part_id: str = None):
    """
    Show a Generate DOCX button with download functionality.
    Can be placed on any page for quick document generation.

    Args:
        data: Chapter data to generate
        part_manager: Part manager (uses default if not provided)
        part_id: Specific part to generate ('cover', 'A', 'B', etc.) or None for full document
    """
    from core.models.parts import PartManager as PM
    from generators.docx.base import DocumentGenerator

    if part_manager is None:
        part_manager = PM()

    # Determine button label based on what we're generating
    if part_id == 'cover':
        button_label = "📥 Generate Cover Page DOCX"
        file_suffix = "Cover"
    elif part_id:
        button_label = f"📥 Generate Part {part_id} DOCX"
        file_suffix = f"Part_{part_id}"
    else:
        button_label = "📥 Generate Full DOCX"
        file_suffix = "Full"

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Use unique key based on part_id
        key_suffix = part_id if part_id else 'full'
        if st.button(button_label, type="primary", use_container_width=True,
                     key=f"gen_docx_{key_suffix}_{st.session_state.get('current_page', 'unknown')}"):
            with st.spinner("Generating DOCX..."):
                try:
                    generator = DocumentGenerator(data, part_manager)

                    # Generate based on part_id
                    if part_id == 'cover':
                        docx_bytes = generator.generate_cover_only_to_bytes()
                    elif part_id:
                        docx_bytes = generator.generate_part_only_to_bytes(part_id)
                    else:
                        docx_bytes = generator.generate_to_bytes()

                    # Store in session state for download with unique key
                    st.session_state[f'quick_docx_{key_suffix}'] = docx_bytes
                    st.session_state[f'quick_docx_ready_{key_suffix}'] = True
                    st.rerun()
                except Exception as e:
                    logger.error("Error generating quick DOCX export: %s", e, exc_info=True)
                    st.error(f"Error generating DOCX: {str(e)}")

        # Show download button if DOCX is ready
        if st.session_state.get(f'quick_docx_ready_{key_suffix}') and st.session_state.get(f'quick_docx_{key_suffix}'):
            safe_title = "".join(c for c in data.chapter_title[:20] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_') if safe_title else 'Chapter'
            filename = f"Ch{data.chapter_number}_{data.subject}_{safe_title}_{file_suffix}.docx"

            st.download_button(
                "⬇️ Download DOCX",
                data=st.session_state[f'quick_docx_{key_suffix}'],
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key=f"download_docx_{key_suffix}_{st.session_state.get('current_page', 'unknown')}"
            )
            st.success(f"✅ {file_suffix} DOCX generated! Click above to download.")
