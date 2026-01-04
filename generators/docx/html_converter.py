"""
HTML to DOCX converter for Guide Book Generator.
Converts HTML preview to DOCX format for exact visual matching.
"""

from io import BytesIO

from docx import Document
from htmldocx import HtmlToDocx

from styles.theme import PageLayout


class HtmlToDocxConverter:
    """Converts HTML content to DOCX format."""

    @staticmethod
    def convert(html_content: str, page_size: str = 'A4') -> bytes:
        """
        Convert HTML content to DOCX bytes.

        Args:
            html_content: HTML string to convert
            page_size: Page size ('A4', 'Letter', etc.)

        Returns:
            DOCX file as bytes
        """
        # Create a new document
        document = Document()

        # Apply page setup
        section = document.sections[0]
        width, height = PageLayout.SIZES.get(page_size, PageLayout.SIZES['A4'])
        section.page_width = width
        section.page_height = height
        section.top_margin = PageLayout.MARGIN_TOP
        section.bottom_margin = PageLayout.MARGIN_BOTTOM
        section.left_margin = PageLayout.MARGIN_LEFT
        section.right_margin = PageLayout.MARGIN_RIGHT

        # Convert HTML to DOCX
        parser = HtmlToDocx()

        # Clean up HTML for better conversion
        html_content = HtmlToDocxConverter._prepare_html(html_content)

        # Parse HTML and add to document
        parser.add_html_to_document(html_content, document)

        # Save to bytes
        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _prepare_html(html: str) -> str:
        """
        Prepare HTML for better DOCX conversion.

        Args:
            html: Raw HTML string

        Returns:
            Cleaned HTML string
        """
        import re

        # Extract body content if present
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
        if body_match:
            html = body_match.group(1)

        # Remove style tags (htmldocx doesn't process CSS well)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove script tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove all inline style attributes (they cause parsing issues)
        html = re.sub(r'\s+style="[^"]*"', '', html, flags=re.IGNORECASE)
        html = re.sub(r"\s+style='[^']*'", '', html, flags=re.IGNORECASE)

        # Remove class attributes (not needed for DOCX)
        html = re.sub(r'\s+class="[^"]*"', '', html, flags=re.IGNORECASE)
        html = re.sub(r"\s+class='[^']*'", '', html, flags=re.IGNORECASE)

        # Replace page-break divs
        html = re.sub(r'<div[^>]*page-break[^>]*>.*?</div>', '<p><br/></p>', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove empty divs
        html = re.sub(r'<div>\s*</div>', '', html, flags=re.IGNORECASE)

        # Convert divs to paragraphs for better DOCX compatibility
        html = re.sub(r'<div>', '<p>', html, flags=re.IGNORECASE)
        html = re.sub(r'</div>', '</p>', html, flags=re.IGNORECASE)

        # Remove any remaining problematic attributes
        html = re.sub(r'\s+onclick="[^"]*"', '', html, flags=re.IGNORECASE)

        return html


def generate_docx_from_html(html_content: str, page_size: str = 'A4') -> bytes:
    """
    Convenience function to generate DOCX from HTML.

    Args:
        html_content: HTML string
        page_size: Page size

    Returns:
        DOCX file as bytes
    """
    return HtmlToDocxConverter.convert(html_content, page_size)
