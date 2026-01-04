"""
Live Preview Component for Guide Book Generator.
Renders chapter data as styled HTML matching the DOCX output.
"""

import streamlit as st

from core.models.base import ChapterData
from core.models.parts import PartManager
from styles.theme import Colors, Icons


class PreviewRenderer:
    """Renders chapter data as HTML preview."""

    # CSS styles - xhtml2pdf compatible (no flex, no border-radius, simple styles)
    CSS = f"""
    <style>
        {Colors.to_css_variables()}

        @page {{
            size: A4;
            margin: 1.5cm;
        }}
        /* xhtml2pdf specific fixes */
        * {{
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        body {{
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: var(--body-text);
            -pdf-keep-with-next: false;
        }}
        /* Prevent content overflow */
        div, td, th {{
            max-width: 100%;
            word-wrap: break-word;
        }}
        /* Table fixes */
        table {{
            -pdf-keep-with-next: false;
            word-wrap: break-word;
        }}
        .preview-container {{
            font-family: Helvetica, Arial, sans-serif;
            max-width: 100%;
            padding: 10px;
            background: var(--white);
        }}
        .preview-header {{
            text-align: center;
            padding: 15px;
            background: var(--bg-neutral);
            border: 2px solid var(--primary-blue);
            margin-bottom: 20px;
        }}
        .preview-title {{
            font-size: 22pt;
            font-weight: bold;
            color: var(--primary-blue);
            margin: 10px 0;
        }}
        .preview-subtitle {{
            font-size: 11pt;
            color: var(--body-text);
        }}
        .preview-chapter-num {{
            font-size: 14pt;
            font-weight: bold;
            color: var(--primary-blue);
        }}
        .decorative-line {{
            text-align: center;
            color: var(--primary-blue);
            font-size: 10pt;
            margin: 8px 0;
        }}
        .preview-meta-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .preview-meta-table th {{
            background: var(--table-header-bg);
            padding: 8px;
            text-align: center;
            font-size: 10pt;
            border: 1px solid var(--border-neutral);
            white-space: nowrap;
        }}
        .preview-meta-table td {{
            padding: 8px;
            text-align: center;
            font-weight: bold;
            border: 1px solid var(--border-neutral);
        }}
        .preview-alert {{
            background: var(--bg-warning);
            border-left: 4px solid var(--accent-red);
            padding: 10px 15px;
            margin: 15px 0;
        }}
        .preview-alert-title {{
            color: var(--accent-red);
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .preview-objectives {{
            background: var(--bg-info);
            border-left: 4px solid var(--border-info);
            padding: 15px;
            margin: 15px 0;
        }}
        .preview-objectives-title {{
            color: var(--primary-blue);
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .preview-contents-box {{
            background: var(--bg-neutral);
            border: 1px solid var(--border-neutral);
            padding: 15px;
            margin: 15px 0;
        }}
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        .preview-part-header {{
            page-break-before: always;
            break-before: page;
            background: var(--bg-warning);
            border: 1px solid var(--border-neutral);
            padding: 10px 15px;
            margin: 20px 0 15px 0;
        }}
        .preview-part-label {{
            color: #DC2626;
            font-weight: bold;
            font-size: 14pt;
        }}
        .preview-part-name {{
            color: #DC2626;
            font-weight: bold;
            font-size: 14pt;
        }}
        .preview-section-title {{
            color: var(--primary-blue);
            font-weight: bold;
            font-size: 12pt;
            margin: 15px 0 10px 0;
        }}
        .preview-concept-box {{
            background: var(--bg-neutral);
            border: 1px solid var(--border-neutral);
            padding: 12px;
            margin: 10px 0;
        }}
        .preview-concept-title {{
            color: var(--primary-blue);
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 8px;
        }}
        .preview-ncert {{
            background: var(--bg-info);
            border-left: 3px solid var(--border-info);
            padding: 8px 12px;
            margin: 8px 0;
            font-style: italic;
            font-size: 10pt;
        }}
        .preview-memory-trick {{
            background: var(--bg-tip);
            border-left: 3px solid var(--border-tip);
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .preview-memory-label {{
            color: var(--success-green);
            font-weight: bold;
            font-size: 10pt;
        }}
        .preview-dyk {{
            background: #F3F4F6;
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .preview-dyk-label {{
            color: #DC2626;
            font-weight: bold;
        }}
        .preview-pyq-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .preview-pyq-table th {{
            background: var(--table-header-bg);
            color: var(--primary-blue);
            padding: 8px;
            text-align: left;
            border: 1px solid var(--border-neutral);
            font-size: 10pt;
            white-space: nowrap;
            min-width: 50px;
        }}
        .preview-pyq-table td {{
            padding: 8px;
            border: 1px solid var(--border-neutral);
            font-size: 10pt;
        }}
        .preview-marks {{
            color: var(--accent-red);
            font-weight: bold;
        }}
        .preview-prediction {{
            background: var(--bg-info);
            border-left: 4px solid var(--border-info);
            padding: 10px 15px;
            margin: 15px 0;
        }}
        /* Timeline Visual Treatment */
        .preview-timeline {{
            position: relative;
            padding-left: 25px;
            margin: 10px 0;
        }}
        .preview-timeline::before {{
            content: '';
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--primary-blue);
        }}
        .preview-timeline-item {{
            position: relative;
            padding: 8px 12px;
            margin-bottom: 8px;
            background: var(--bg-neutral);
            border-radius: 4px;
            border-left: 3px solid var(--primary-blue);
        }}
        .preview-timeline-item::before {{
            content: '';
            position: absolute;
            left: -22px;
            top: 12px;
            width: 10px;
            height: 10px;
            background: var(--primary-blue);
            border-radius: 50%;
        }}
        .preview-timeline-year {{
            display: inline-block;
            background: var(--primary-blue);
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
            font-size: 10pt;
            margin-right: 10px;
        }}
        .preview-timeline-event {{
            color: var(--body-text);
            font-size: 10pt;
        }}
        .preview-mcq {{
            background: var(--bg-neutral);
            padding: 10px 15px;
            margin: 8px 0;
            border-left: 3px solid var(--primary-blue);
        }}
        .preview-mcq-options {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        .preview-answer {{
            background: var(--bg-tip);
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .preview-marking-points {{
            margin: 10px 0 10px 10px;
        }}
        .preview-marking-point {{
            color: var(--body-text);
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
        }}
        .preview-marking-point::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success-green);
            font-weight: bold;
        }}
        .preview-marking-point-mark {{
            color: var(--accent-red);
            font-size: 9pt;
            margin-left: 5px;
        }}
        .preview-map-item {{
            padding: 5px 0;
            padding-left: 20px;
        }}
        .preview-checklist {{
            padding: 5px 0;
        }}
        .preview-mistake-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .preview-mistake-table th.mistake {{
            background: var(--bg-warning);
            color: var(--accent-red);
            padding: 8px;
            border: 1px solid var(--border-neutral);
        }}
        .preview-mistake-table th.correct {{
            background: var(--bg-tip);
            color: var(--success-green);
            padding: 8px;
            border: 1px solid var(--border-neutral);
        }}
        .preview-mistake-table td {{
            padding: 8px;
            border: 1px solid var(--border-neutral);
            font-size: 10pt;
        }}
        .preview-divider {{
            border-top: 1px solid var(--border-neutral);
            margin: 20px 0;
        }}
        .preview-end-marker {{
            text-align: center;
            color: var(--primary-blue);
            font-weight: bold;
            margin-top: 30px;
        }}
        .qr-table {{
            width: 100%;
            margin: 15px 0;
        }}
        .qr-cell {{
            text-align: center;
            padding: 10px;
            width: 50%;
        }}
        .importance-high {{ color: var(--accent-red); }}
        .importance-medium {{ color: var(--warning-orange); }}
        .importance-low {{ color: var(--success-green); }}
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
        """Render cover page section."""
        subject_display = data.subject.replace('_', ' ').title()

        # Use solid line character for decorative line (U+2500)
        decorative_line = '<div class="decorative-line">' + '─' * 50 + '</div>'

        html = f'''
        <div class="preview-header">
            <div class="preview-subtitle">CBSE Class {data.class_num} | Social Science | {subject_display}</div>
            {decorative_line}
            <div class="preview-chapter-num">CHAPTER {data.chapter_number}</div>
            <div class="preview-title">{data.chapter_title}</div>
            {f'<div class="preview-subtitle">{data.subtitle}</div>' if data.subtitle else ''}
            {decorative_line}
        </div>

        <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
            <tr>
                <td style="border: 1px solid #E5E7EB; padding: 10px 15px; text-align: center; white-space: nowrap;">
                    Weightage <span style="color: #B91C1C; font-weight: bold;">{data.weightage}</span>
                </td>
                <td style="border: 1px solid #E5E7EB; padding: 10px 15px; text-align: center; white-space: nowrap;">
                    Map Work <span style="color: #B91C1C; font-weight: bold;">{data.map_work}</span>
                </td>
                <td style="border: 1px solid #E5E7EB; padding: 10px 15px; text-align: center; white-space: nowrap;">
                    Importance <span style="color: #B91C1C; font-weight: bold;">{data.importance}</span>
                </td>
                <td style="border: 1px solid #E5E7EB; padding: 10px 15px; text-align: center; white-space: nowrap;">
                    PYQ Frequency <span style="color: #B91C1C; font-weight: bold;">{data.pyq_frequency}</span>
                </td>
            </tr>
        </table>
        '''

        # Syllabus Alert
        if data.syllabus_alert_enabled and data.syllabus_alert_text:
            html += f'''
            <div class="preview-alert">
                <div class="preview-alert-title">! SYLLABUS ALERT</div>
                <div>{data.syllabus_alert_text}</div>
            </div>
            '''

        # Learning Objectives
        if data.learning_objectives:
            objectives_html = data.learning_objectives.replace('\n', '<br/>')
            html += f'''
            <div class="preview-objectives">
                <div class="preview-objectives-title">* Learning Objectives</div>
                <div>{objectives_html}</div>
            </div>
            '''

        # Chapter Contents box (Part Descriptions)
        if data.part_descriptions:
            html += f'''
            <div class="preview-contents-box">
                <div style="color: var(--primary-blue); font-weight: bold; margin-bottom: 10px;">{Icons.BOOK} Chapter Contents</div>
            '''
            for part_id, desc in data.part_descriptions.items():
                if desc:
                    html += f'''
                    <div style="margin: 5px 0; padding-left: 10px;">
                        <span style="color: var(--primary-blue); font-weight: bold;">Part {part_id}:</span>
                        <span style="color: var(--body-text);"> {desc}</span>
                    </div>
                    '''
            html += '</div>'

        # QR Codes Section - using TABLE layout instead of flex (xhtml2pdf compatible)
        if data.qr_practice_questions_url or data.qr_practice_with_answers_url:
            html += '''
            <div style="background: var(--bg-info); border: 1px solid var(--primary-blue); padding: 15px; margin: 15px 0;">
                <div style="color: var(--primary-blue); font-weight: bold; margin-bottom: 10px; text-align: center;">
                    Scan QR Codes to Download Practice Materials
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
                            <span style="font-size: 10pt; color: var(--body-text); font-weight: bold;">Practice Questions</span>
                            <br/>
                            <span style="font-size: 9pt; color: var(--light-gray);">(PDF Download)</span>
                        </td>
                    '''

            if data.qr_practice_with_answers_url:
                qr_img_2 = cls._generate_qr_base64(data.qr_practice_with_answers_url)
                if qr_img_2:
                    html += f'''
                        <td class="qr-cell">
                            <img src="data:image/png;base64,{qr_img_2}" width="100" height="100"/>
                            <br/>
                            <span style="font-size: 10pt; color: var(--body-text); font-weight: bold;">With Answers</span>
                            <br/>
                            <span style="font-size: 9pt; color: var(--light-gray);">(PDF Download)</span>
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
        except Exception:
            return ""

    @classmethod
    def _render_part_a(cls, data: ChapterData) -> str:
        """Render Part A: PYQ Analysis."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part A: </span>
            <span class="preview-part-name">Previous Year Questions Analysis</span>
        </div>
        '''

        if data.pyq_year_range:
            html += f'<div class="preview-section-title">&gt; PYQ Pattern ({data.pyq_year_range})</div>'

        if data.pyq_items:
            html += '''
            <table class="preview-pyq-table">
                <tr>
                    <th style="width:60%">Question</th>
                    <th style="width:15%">Marks</th>
                    <th style="width:25%">Years Asked</th>
                </tr>
            '''
            for item in data.pyq_items:
                # Calculate frequency for row coloring
                years = item.years or ''
                year_count = len([y.strip() for y in years.split(',') if y.strip()])

                # Row background color based on frequency
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
                    <td class="preview-marks">{item.marks}</td>
                    <td>{item.years}</td>
                </tr>
                '''
            html += '</table>'

        if data.pyq_prediction:
            html += f'''
            <div class="preview-prediction">
                <strong>&gt; Prediction:</strong> {data.pyq_prediction}
            </div>
            '''

        if data.pyq_syllabus_note:
            html += f'''
            <div style="background: var(--bg-tip); border-left: 4px solid var(--border-tip); padding: 10px 15px; margin: 15px 0;">
                <strong style="color: var(--success-green);">{Icons.TIP} Syllabus Note:</strong> {data.pyq_syllabus_note}
            </div>
            '''

        return html

    @classmethod
    def _render_part_b(cls, data: ChapterData) -> str:
        """Render Part B: Key Concepts."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part B: </span>
            <span class="preview-part-name">Key Concepts Explained</span>
        </div>
        '''

        for concept in data.concepts:
            if concept.is_empty():
                continue

            html += f'''
            <div class="preview-concept-box">
                <div class="preview-concept-title">{concept.number}. {concept.title or 'Untitled'}</div>
            '''

            if concept.ncert_line:
                html += f'<div class="preview-ncert"><span style="color: var(--accent-red); font-weight: bold; font-style: normal;">NCERT Exact Line:</span> "{concept.ncert_line}"</div>'

            if concept.content:
                content_html = cls._format_text(concept.content)
                html += f'<div>{content_html}</div>'

            if concept.memory_trick:
                html += f'''
                <div class="preview-memory-trick">
                    <span class="preview-memory-label">&gt; Memory Trick:</span>
                    {concept.memory_trick}
                </div>
                '''

            if concept.did_you_know:
                html += f'''
                <div class="preview-dyk">
                    <span class="preview-dyk-label">Do You Know?</span> {concept.did_you_know}
                </div>
                '''

            html += '</div>'

        # Comparison Tables
        if data.comparison_tables:
            html += f'<div class="preview-section-title" style="color: var(--primary-blue);">{Icons.CHART} Comparison Tables</div>'
            for table in data.comparison_tables:
                table_title = table.get('title', 'Comparison')
                headers = table.get('headers', [])
                rows = table.get('rows', [])

                html += f'<div style="font-weight: bold; margin: 10px 0 5px 0;">{table_title}</div>'
                html += '<table class="preview-pyq-table"><tr>'
                for header in headers:
                    html += f'<th>{header}</th>'
                html += '</tr>'
                for row in rows:
                    html += '<tr>'
                    for cell in row:
                        html += f'<td>{cell}</td>'
                    html += '</tr>'
                html += '</table>'

        # Common Mistakes
        if data.common_mistakes:
            html += f'<div class="preview-section-title" style="color: var(--accent-red);">{Icons.WRONG} Common Mistakes to Avoid</div>'
            html += '''
            <div style="background: var(--bg-warning); border-left: 4px solid var(--border-warning); padding: 12px 15px; margin: 10px 0;">
                <div style="color: var(--accent-red); font-style: italic; margin-bottom: 8px;">These mistakes cost students marks every year!</div>
            '''
            for mistake in data.common_mistakes:
                html += f'<div style="margin: 5px 0;">{Icons.WRONG} {mistake}</div>'
            html += '</div>'

        # Important Dates Timeline
        if data.important_dates:
            html += f'<div class="preview-section-title" style="color: var(--primary-blue);">{Icons.CALENDAR} Important Dates Timeline</div>'
            html += '<div class="preview-timeline">'
            for date_item in data.important_dates:
                year = date_item.get('year', '')
                event = date_item.get('event', '')
                html += f'''
                <div class="preview-timeline-item">
                    <span class="preview-timeline-year">{year}</span>
                    <span class="preview-timeline-event">{cls._format_text(event)}</span>
                </div>
                '''
            html += '</div>'

        return html

    @classmethod
    def _render_part_c(cls, data: ChapterData) -> str:
        """Render Part C: Model Answers."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part C: </span>
            <span class="preview-part-name">Model Answers</span>
        </div>
        '''

        for idx, answer in enumerate(data.model_answers, 1):
            if not answer.question:
                continue

            html += f'''
            <div class="preview-concept-box">
                <div class="preview-concept-title">Q{idx}. {answer.question} <span class="preview-marks">[{answer.marks}M]</span></div>
                <div class="preview-answer">
                    <strong>Answer:</strong><br>
                    {cls._format_text(answer.answer)}
                </div>
            '''

            if answer.marking_points:
                html += '<div class="preview-marking-points"><strong>Marking Points:</strong>'
                for point in answer.marking_points:
                    html += f'<div class="preview-marking-point">{point}<span class="preview-marking-point-mark">(1 mark)</span></div>'
                html += '</div>'

            html += '</div>'

        return html

    @classmethod
    def _render_part_d(cls, data: ChapterData) -> str:
        """Render Part D: Practice Questions."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part D: </span>
            <span class="preview-part-name">Practice Questions</span>
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
        """Render Part E: Map Work."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part E: </span>
            <span class="preview-part-name">Map Work</span>
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
        """Render Part F: Quick Revision."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part F: </span>
            <span class="preview-part-name">Quick Revision</span>
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
        """Render Part G: Exam Strategy."""
        html = '''
        <div class="preview-part-header">
            <span class="preview-part-label">Part G: </span>
            <span class="preview-part-name">Exam Strategy</span>
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
        """Format text with markdown-like syntax."""
        if not text:
            return ''

        import re

        # Bold: **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        # Italic: *text*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

        # Line breaks (xhtml2pdf prefers self-closing tags)
        text = text.replace('\n', '<br/>')

        return text

    @staticmethod
    def _pdf_safe_text(text: str) -> str:
        """Replace multi-byte emojis with PDF-safe Unicode symbols."""
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

def show_pdf_preview(data: ChapterData, part_manager: PartManager):
    """
    Generate and display actual PDF preview.
    Uses HTML-to-PDF conversion for accurate preview matching.
    """
    import base64

    import streamlit.components.v1 as components

    from generators.docx.base import DocumentGenerator
    from generators.pdf.converter import PDFConverter

    st.subheader("📄 Document Preview & Download")

    # Check PDF conversion availability
    html_pdf_available = PDFConverter.is_html_pdf_available()
    docx_pdf_available, method = PDFConverter.is_available()

    if not html_pdf_available and not docx_pdf_available:
        st.warning("""
            ⚠️ **PDF generation not available**

            Install xhtml2pdf for PDF support: `pip install xhtml2pdf`
        """)

    # Generate Preview button
    col1, col2 = st.columns([1, 3])

    with col1:
        generate_clicked = st.button(
            "🔄 Generate Preview",
            type="primary",
            use_container_width=True,
            help="Generate the document to see preview and download"
        )

    if generate_clicked:
        with st.spinner("Generating document..."):
            try:
                # Generate DOCX
                generator = DocumentGenerator(data, part_manager)
                docx_bytes = generator.generate_to_bytes()

                # Store DOCX in session state
                st.session_state['preview_docx'] = docx_bytes
                st.session_state['preview_generated'] = True

                # Generate PDF from HTML (matches preview exactly)
                if html_pdf_available:
                    with st.spinner("Generating PDF preview..."):
                        # Generate HTML preview
                        html_content = PreviewRenderer.render_full_preview(data, part_manager)
                        pdf_bytes = PDFConverter.convert_html_to_pdf(html_content)

                        if pdf_bytes:
                            st.session_state['preview_pdf'] = pdf_bytes
                            st.session_state['preview_html'] = html_content
                        else:
                            st.session_state['preview_pdf'] = None
                            st.warning("PDF generation failed.")
                elif docx_pdf_available:
                    # Fallback to DOCX-to-PDF if Word/LibreOffice available
                    with st.spinner("Converting to PDF..."):
                        pdf_bytes = PDFConverter.convert_bytes(docx_bytes)
                        if pdf_bytes:
                            st.session_state['preview_pdf'] = pdf_bytes
                        else:
                            st.session_state['preview_pdf'] = None
                else:
                    st.session_state['preview_pdf'] = None

                st.success("✅ Preview generated successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error generating document: {str(e)}")
                return

    # Display preview if available
    if st.session_state.get('preview_pdf'):
        st.divider()
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
        st.divider()
        st.info("📝 PDF preview not available. Click 'Download DOCX' to view the document in Microsoft Word or LibreOffice.")

    elif st.session_state.get('preview_generated'):
        st.divider()
        st.info("📝 Preview generated. Download the file to view.")

    # Download buttons
    if st.session_state.get('preview_docx') or st.session_state.get('preview_pdf'):
        st.divider()
        col1, col2, col3 = st.columns(3)

        # Safe filename
        safe_title = "".join(c for c in data.chapter_title[:20] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_') if safe_title else 'Chapter'

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
    keys_to_clear = ['preview_docx', 'preview_pdf', 'preview_generated']
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
