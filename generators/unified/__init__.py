"""
Unified rendering system for Guide Book Generator.
Provides consistent output for both HTML preview and DOCX generation.
"""

from .content_builder import ContentBuilder, Element, ElementType, BoxType
from .html_renderer import HtmlRenderer
from .docx_renderer import DocxRenderer

__all__ = [
    'ContentBuilder',
    'Element',
    'ElementType',
    'BoxType',
    'HtmlRenderer',
    'DocxRenderer',
]
