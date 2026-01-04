"""
HTML Renderer for Guide Book Generator.
Renders document elements to HTML.
"""

from typing import List
from .content_builder import Element, ElementType, BoxType
from styles.theme import Colors


class HtmlRenderer:
    """Renders document elements to HTML."""

    CSS = f"""
    <style>
        :root {{
            --primary-blue: {Colors.PRIMARY_BLUE};
            --accent-red: {Colors.ACCENT_RED};
            --success-green: {Colors.SUCCESS_GREEN};
            --warning-orange: {Colors.WARNING_ORANGE};
            --body-text: {Colors.BODY_TEXT};
            --bg-neutral: {Colors.BG_NEUTRAL};
            --bg-info: {Colors.BG_INFO};
            --bg-tip: {Colors.BG_TIP};
            --bg-warning: {Colors.BG_WARNING};
            --border-neutral: {Colors.BORDER_NEUTRAL};
            --border-info: {Colors.BORDER_INFO};
            --border-tip: {Colors.BORDER_TIP};
            --border-warning: {Colors.BORDER_WARNING};
            --table-header-bg: {Colors.TABLE_HEADER_BG};
        }}
        body {{
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: var(--body-text);
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            color: var(--body-text);
            font-size: 11pt;
            margin-bottom: 10px;
        }}
        .decorative-line {{
            text-align: center;
            color: var(--primary-blue);
            font-size: 10pt;
            margin: 8px 0;
        }}
        .chapter-num {{
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            color: var(--primary-blue);
            margin-top: 15px;
        }}
        .chapter-title {{
            text-align: center;
            font-size: 24pt;
            font-weight: bold;
            color: var(--primary-blue);
            margin: 10px 0;
        }}
        .chapter-subtitle {{
            text-align: center;
            font-size: 11pt;
            font-style: italic;
            color: var(--body-text);
        }}
        .metadata-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .metadata-table th {{
            background: var(--table-header-bg);
            padding: 8px;
            text-align: center;
            font-size: 10pt;
            border: 1px solid var(--border-neutral);
        }}
        .metadata-table td {{
            padding: 8px;
            text-align: center;
            font-weight: bold;
            border: 1px solid var(--border-neutral);
        }}
        .highlight {{ color: var(--accent-red); }}
        .box {{
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid;
        }}
        .box-warning {{
            background: var(--bg-warning);
            border-color: var(--accent-red);
        }}
        .box-info {{
            background: var(--bg-info);
            border-color: var(--border-info);
        }}
        .box-tip {{
            background: var(--bg-tip);
            border-color: var(--border-tip);
        }}
        .box-neutral {{
            background: var(--bg-neutral);
            border: 1px solid var(--border-neutral);
            border-left: 4px solid var(--border-neutral);
        }}
        .box-title {{
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .box-title-warning {{ color: var(--accent-red); }}
        .box-title-info {{ color: var(--primary-blue); }}
        .box-title-tip {{ color: var(--success-green); }}
        .box-title-neutral {{ color: var(--body-text); }}
        .box-subtitle {{
            font-style: italic;
            margin-bottom: 10px;
            font-size: 10pt;
        }}
        .part-header {{
            background: var(--bg-neutral);
            border: 1px solid var(--border-neutral);
            padding: 10px 15px;
            margin: 20px 0 15px 0;
            page-break-before: always;
        }}
        .part-label {{
            color: var(--primary-blue);
            font-weight: bold;
            font-size: 14pt;
        }}
        .section-title {{
            color: var(--primary-blue);
            font-weight: bold;
            font-size: 12pt;
            margin: 15px 0 10px 0;
            border-bottom: 2px solid var(--primary-blue);
            padding-bottom: 5px;
        }}
        .concept-box {{
            background: var(--bg-neutral);
            border: 1px solid var(--border-neutral);
            padding: 12px;
            margin: 10px 0;
        }}
        .concept-title {{
            color: var(--primary-blue);
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 8px;
        }}
        .concept-content {{
            margin-bottom: 10px;
        }}
        .ncert-box {{
            background: var(--bg-info);
            border-left: 3px solid var(--border-info);
            padding: 8px 12px;
            margin: 8px 0;
            font-style: italic;
            font-size: 10pt;
        }}
        .memory-trick {{
            background: var(--bg-tip);
            border-left: 3px solid var(--border-tip);
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .memory-label {{
            color: var(--success-green);
            font-weight: bold;
            font-size: 10pt;
        }}
        .dyk-box {{
            background: #FFF7ED;
            border-left: 3px solid #D97706;
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .dyk-label {{
            color: #D97706;
            font-weight: bold;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .table th {{
            background: var(--table-header-bg);
            color: var(--primary-blue);
            padding: 8px;
            text-align: left;
            border: 1px solid var(--border-neutral);
            font-size: 10pt;
        }}
        .table td {{
            padding: 8px;
            border: 1px solid var(--border-neutral);
            font-size: 10pt;
        }}
        .marks {{ color: var(--accent-red); font-weight: bold; }}
        .question-block {{
            background: var(--bg-neutral);
            padding: 10px 15px;
            margin: 8px 0;
            border-left: 3px solid var(--primary-blue);
        }}
        .question-num {{
            color: var(--primary-blue);
            font-weight: bold;
        }}
        .mcq-options {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        .answer-block {{
            margin: 15px 0;
        }}
        .answer-content {{
            background: var(--bg-tip);
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .marking-points {{
            margin: 10px 0 10px 10px;
        }}
        .marking-point {{
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
        }}
        .marking-point::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success-green);
            font-weight: bold;
        }}
        .timeline-item {{
            padding: 8px 12px;
            margin-bottom: 8px;
            background: var(--bg-neutral);
            border-left: 3px solid var(--primary-blue);
        }}
        .timeline-year {{
            display: inline-block;
            background: var(--primary-blue);
            color: white;
            padding: 2px 8px;
            font-weight: bold;
            font-size: 10pt;
            margin-right: 10px;
        }}
        .divider {{
            border-top: 1px solid var(--border-neutral);
            margin: 20px 0;
        }}
        .end-marker {{
            text-align: center;
            color: var(--primary-blue);
            font-weight: bold;
            margin-top: 30px;
        }}
        .qr-section {{
            background: #EFF6FF;
            border: 1px solid var(--primary-blue);
            padding: 15px;
            margin: 15px 0;
            text-align: center;
        }}
        .qr-title {{
            color: var(--primary-blue);
            font-weight: bold;
            margin-bottom: 10px;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        @media print {{
            .part-header {{
                page-break-before: always;
            }}
        }}
    </style>
    """

    @classmethod
    def render(cls, elements: List[Element]) -> str:
        """Render elements to HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    {cls.CSS}
</head>
<body>
"""
        for element in elements:
            html += cls._render_element(element)

        html += "</body></html>"
        return html

    @classmethod
    def _render_element(cls, element: Element) -> str:
        """Render a single element to HTML."""
        renderers = {
            ElementType.HEADER: cls._render_header,
            ElementType.TITLE: cls._render_title,
            ElementType.DECORATIVE_LINE: cls._render_decorative_line,
            ElementType.METADATA_TABLE: cls._render_metadata_table,
            ElementType.ALERT_BOX: cls._render_alert_box,
            ElementType.INFO_BOX: cls._render_info_box,
            ElementType.TIP_BOX: cls._render_tip_box,
            ElementType.NEUTRAL_BOX: cls._render_neutral_box,
            ElementType.PARAGRAPH: cls._render_paragraph,
            ElementType.BULLET_LIST: cls._render_bullet_list,
            ElementType.NUMBERED_LIST: cls._render_numbered_list,
            ElementType.TABLE: cls._render_table,
            ElementType.PART_HEADER: cls._render_part_header,
            ElementType.SECTION_TITLE: cls._render_section_title,
            ElementType.CONCEPT_BOX: cls._render_concept_box,
            ElementType.QUESTION_BLOCK: cls._render_question_block,
            ElementType.MCQ_BLOCK: cls._render_mcq_block,
            ElementType.ANSWER_BLOCK: cls._render_answer_block,
            ElementType.TIMELINE: cls._render_timeline,
            ElementType.QR_CODES: cls._render_qr_codes,
            ElementType.PAGE_BREAK: cls._render_page_break,
            ElementType.DIVIDER: cls._render_divider,
            ElementType.END_MARKER: cls._render_end_marker,
        }

        renderer = renderers.get(element.type)
        if renderer:
            return renderer(element)
        return ""

    @classmethod
    def _render_header(cls, element: Element) -> str:
        return f'<div class="header">{cls._escape(element.content)}</div>'

    @classmethod
    def _render_title(cls, element: Element) -> str:
        content = element.content
        html = f'<div class="chapter-num">{cls._escape(content["chapter_num"])}</div>'
        html += f'<div class="chapter-title">{cls._escape(content["title"])}</div>'
        if content.get("subtitle"):
            html += f'<div class="chapter-subtitle">{cls._escape(content["subtitle"])}</div>'
        return html

    @classmethod
    def _render_decorative_line(cls, element: Element) -> str:
        return '<div class="decorative-line">─' * 50 + '</div>'

    @classmethod
    def _render_metadata_table(cls, element: Element) -> str:
        content = element.content
        html = '<table class="metadata-table"><tr>'
        for key in content:
            html += f'<th>{cls._escape(key)}</th>'
        html += '</tr><tr>'
        for key, data in content.items():
            value = data['value']
            highlight = data.get('highlight', False)
            css_class = ' class="highlight"' if highlight else ''
            html += f'<td{css_class}>{cls._escape(value)}</td>'
        html += '</tr></table>'
        return html

    @classmethod
    def _render_alert_box(cls, element: Element) -> str:
        content = element.content
        return f'''<div class="box box-warning">
            <div class="box-title box-title-warning">⚠️ {cls._escape(content["title"])}</div>
            <div>{cls._escape(content["text"])}</div>
        </div>'''

    @classmethod
    def _render_info_box(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="box box-info">
            <div class="box-title box-title-info">🎯 {cls._escape(content["title"])}</div>'''

        if content.get("subtitle"):
            html += f'<div class="box-subtitle">{cls._escape(content["subtitle"])}</div>'

        if content.get("text"):
            html += f'<div>{cls._escape(content["text"])}</div>'

        if content.get("items"):
            html += '<ul>'
            for item in content["items"]:
                html += f'<li>{cls._escape(item)}</li>'
            html += '</ul>'

        html += '</div>'
        return html

    @classmethod
    def _render_tip_box(cls, element: Element) -> str:
        content = element.content
        return f'''<div class="box box-tip">
            <div class="box-title box-title-tip">💡 {cls._escape(content["title"])}</div>
            <div>{cls._escape(content["text"])}</div>
        </div>'''

    @classmethod
    def _render_neutral_box(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="box box-neutral">
            <div class="box-title box-title-neutral">📚 {cls._escape(content["title"])}</div>'''

        if content.get("items"):
            for item in content["items"]:
                html += f'''<div style="margin: 5px 0;">
                    <span style="color: {Colors.PRIMARY_BLUE}; font-weight: bold;">{cls._escape(item["label"])}:</span>
                    {cls._escape(item["description"])}
                </div>'''

        html += '</div>'
        return html

    @classmethod
    def _render_paragraph(cls, element: Element) -> str:
        return f'<p>{cls._escape(element.content)}</p>'

    @classmethod
    def _render_bullet_list(cls, element: Element) -> str:
        html = '<ul>'
        for item in element.content:
            html += f'<li>{cls._escape(item)}</li>'
        html += '</ul>'
        return html

    @classmethod
    def _render_numbered_list(cls, element: Element) -> str:
        html = '<ol>'
        for item in element.content:
            html += f'<li>{cls._escape(item)}</li>'
        html += '</ol>'
        return html

    @classmethod
    def _render_table(cls, element: Element) -> str:
        content = element.content
        html = '<table class="table"><tr>'
        for header in content['headers']:
            html += f'<th>{cls._escape(header)}</th>'
        html += '</tr>'

        for row in content['rows']:
            html += '<tr>'
            if isinstance(row, dict):
                for key in content['headers']:
                    key_lower = key.lower().replace(' ', '_')
                    value = row.get(key_lower, row.get(key, ''))
                    if key_lower == 'marks' or key == 'Marks':
                        html += f'<td class="marks">{cls._escape(str(value))}</td>'
                    else:
                        html += f'<td>{cls._escape(str(value))}</td>'
            else:
                for cell in row:
                    html += f'<td>{cls._escape(str(cell))}</td>'
            html += '</tr>'

        html += '</table>'
        return html

    @classmethod
    def _render_part_header(cls, element: Element) -> str:
        content = element.content
        return f'''<div class="part-header">
            <span class="part-label">Part {cls._escape(content["id"])}: {cls._escape(content["name"])}</span>
        </div>'''

    @classmethod
    def _render_section_title(cls, element: Element) -> str:
        return f'<div class="section-title">{cls._escape(element.content)}</div>'

    @classmethod
    def _render_concept_box(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="concept-box">
            <div class="concept-title">{content["number"]}. {cls._escape(content["title"])}</div>
            <div class="concept-content">{cls._escape(content["content"])}</div>'''

        if content.get("ncert_line"):
            html += f'<div class="ncert-box">📖 NCERT: "{cls._escape(content["ncert_line"])}"</div>'

        if content.get("memory_trick"):
            html += f'''<div class="memory-trick">
                <span class="memory-label">💡 Memory Trick:</span> {cls._escape(content["memory_trick"])}
            </div>'''

        if content.get("did_you_know"):
            html += f'''<div class="dyk-box">
                <span class="dyk-label">🤔 Did You Know?</span> {cls._escape(content["did_you_know"])}
            </div>'''

        html += '</div>'
        return html

    @classmethod
    def _render_question_block(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="question-block">
            <span class="question-num">Q{content["number"]}.</span>
            {cls._escape(content["question"])}
            <span class="marks">[{content["marks"]}M]</span>'''

        if content.get("hint"):
            html += f'<div style="font-size: 10pt; color: #666; margin-top: 5px;">Hint: {cls._escape(content["hint"])}</div>'

        html += '</div>'
        return html

    @classmethod
    def _render_mcq_block(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="question-block">
            <span class="question-num">Q{content["number"]}.</span>
            {cls._escape(content["question"])}
            <span class="marks">[{content["marks"]}M]</span>'''

        if content.get("options"):
            html += '<div class="mcq-options">'
            for i, option in enumerate(content["options"]):
                letter = chr(97 + i)  # a, b, c, d
                html += f'<div>({letter}) {cls._escape(option)}</div>'
            html += '</div>'

        html += '</div>'
        return html

    @classmethod
    def _render_answer_block(cls, element: Element) -> str:
        content = element.content
        html = f'''<div class="answer-block">
            <div class="question-block">
                <span class="question-num">Q{content["number"]}.</span>
                {cls._escape(content["question"])}
                <span class="marks">[{content["marks"]}M]</span>
            </div>
            <div class="answer-content">
                <strong>Answer:</strong> {cls._escape(content["answer"])}
            </div>'''

        if content.get("marking_points"):
            html += '<div class="marking-points">'
            for point in content["marking_points"]:
                html += f'<div class="marking-point">{cls._escape(point)}</div>'
            html += '</div>'

        html += '</div>'
        return html

    @classmethod
    def _render_timeline(cls, element: Element) -> str:
        html = '<div class="timeline">'
        for item in element.content:
            year = item.get('year', '')
            event = item.get('event', '')
            html += f'''<div class="timeline-item">
                <span class="timeline-year">{cls._escape(year)}</span>
                <span>{cls._escape(event)}</span>
            </div>'''
        html += '</div>'
        return html

    @classmethod
    def _render_qr_codes(cls, element: Element) -> str:
        content = element.content
        html = '''<div class="qr-section">
            <div class="qr-title">📱 Scan QR Codes to Download Practice Materials</div>
            <div style="display: flex; justify-content: space-around;">'''

        if content.get("practice_url"):
            html += f'''<div style="text-align: center;">
                <div>[QR Code]</div>
                <div style="font-size: 10pt;">Practice Questions</div>
                <div style="font-size: 8pt; color: #666;">{cls._escape(content["practice_url"][:30])}...</div>
            </div>'''

        if content.get("answers_url"):
            html += f'''<div style="text-align: center;">
                <div>[QR Code]</div>
                <div style="font-size: 10pt;">With Answers</div>
                <div style="font-size: 8pt; color: #666;">{cls._escape(content["answers_url"][:30])}...</div>
            </div>'''

        html += '</div></div>'
        return html

    @classmethod
    def _render_page_break(cls, element: Element) -> str:
        return '<div style="page-break-before: always;"></div>'

    @classmethod
    def _render_divider(cls, element: Element) -> str:
        return '<div class="divider"></div>'

    @classmethod
    def _render_end_marker(cls, element: Element) -> str:
        return f'<div class="end-marker">{cls._escape(element.content)}</div>'

    @staticmethod
    def _escape(text: str) -> str:
        """Escape HTML special characters."""
        if not isinstance(text, str):
            text = str(text) if text else ""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))
