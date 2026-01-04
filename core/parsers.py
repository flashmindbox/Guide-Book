"""
Document parsers for importing chapter data from DOCX and PDF files.
"""

import re
from typing import Optional, Dict, Any
from io import BytesIO

from .models.base import ChapterData


class DocxParser:
    """Parse DOCX files to extract chapter data."""

    @staticmethod
    def parse(file_bytes: bytes) -> Optional[ChapterData]:
        """
        Parse a DOCX file and extract chapter data.

        Args:
            file_bytes: The DOCX file content as bytes

        Returns:
            ChapterData object if successful, None otherwise
        """
        try:
            from docx import Document

            doc = Document(BytesIO(file_bytes))

            # Extract text from all paragraphs
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)

            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        full_text.append(cell.text)

            text_content = '\n'.join(full_text)

            # Parse the content
            return DocxParser._extract_chapter_data(text_content)

        except Exception:
            return None

    @staticmethod
    def _extract_chapter_data(text: str) -> ChapterData:
        """Extract chapter data from text content."""
        data = ChapterData()

        # Extract class number (e.g., "CBSE Class 10")
        class_match = re.search(r'CBSE Class (\d+)', text)
        if class_match:
            data.class_num = int(class_match.group(1))

        # Extract subject
        subject_match = re.search(r'Social Science \| (\w+)', text)
        if subject_match:
            data.subject = subject_match.group(1).lower()

        # Extract chapter number (e.g., "CHAPTER 1" or "CHAPTER 2")
        chapter_match = re.search(r'CHAPTER (\d+)', text, re.IGNORECASE)
        if chapter_match:
            data.chapter_number = int(chapter_match.group(1))

        # Extract chapter title (text after CHAPTER X, before next section)
        title_match = re.search(r'CHAPTER \d+\s*\n?\s*([^\n]+)', text, re.IGNORECASE)
        if title_match:
            data.chapter_title = title_match.group(1).strip()

        # Extract weightage
        weightage_match = re.search(r'Weightage[:\s]*([^\n]+)', text)
        if weightage_match:
            data.weightage = weightage_match.group(1).strip()

        # Extract importance
        importance_match = re.search(r'Importance[:\s]*(\w+)', text)
        if importance_match:
            data.importance = importance_match.group(1).strip()

        # Extract map work
        map_match = re.search(r'Map Work[:\s]*(\w+)', text)
        if map_match:
            data.map_work = map_match.group(1).strip()

        # Extract PYQ frequency
        freq_match = re.search(r'PYQ Frequency[:\s]*([^\n]+)', text)
        if freq_match:
            data.pyq_frequency = freq_match.group(1).strip()

        # Extract learning objectives
        obj_match = re.search(r'Learning Objectives[:\s]*\n(.*?)(?=\*|Part [A-G]|$)', text, re.DOTALL | re.IGNORECASE)
        if obj_match:
            data.learning_objectives = obj_match.group(1).strip()

        # Extract syllabus alert
        alert_match = re.search(r'SYLLABUS ALERT[:\s]*([^\n]+)', text)
        if alert_match:
            data.syllabus_alert_text = alert_match.group(1).strip()
            data.syllabus_alert_enabled = True

        return data

    @staticmethod
    def parse_section(file_bytes: bytes, section: str) -> Dict[str, Any]:
        """
        Parse a specific section from a DOCX file.

        Args:
            file_bytes: The DOCX file content as bytes
            section: Section to parse ('cover', 'part_a', 'part_b', etc.)

        Returns:
            Dict with section-specific data
        """
        try:
            from docx import Document

            doc = Document(BytesIO(file_bytes))

            # Extract all text
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        full_text.append(cell.text)

            text_content = '\n'.join(full_text)

            # Route to section-specific parser
            parsers = {
                'cover': DocxParser._parse_cover_section,
                'part_a': DocxParser._parse_part_a_section,
                'part_b': DocxParser._parse_part_b_section,
                'part_c': DocxParser._parse_part_c_section,
                'part_d': DocxParser._parse_part_d_section,
                'part_e': DocxParser._parse_part_e_section,
                'part_f': DocxParser._parse_part_f_section,
                'part_g': DocxParser._parse_part_g_section,
            }

            parser_func = parsers.get(section)
            if parser_func:
                return parser_func(text_content)
            return {}

        except Exception:
            return {}

    @staticmethod
    def _parse_cover_section(text: str) -> Dict[str, Any]:
        """Parse cover page data."""
        data = {}

        # Chapter title
        title_match = re.search(r'CHAPTER \d+\s*\n?\s*([^\n]+)', text, re.IGNORECASE)
        if title_match:
            data['chapter_title'] = title_match.group(1).strip()

        # Subtitle
        subtitle_match = re.search(r'CHAPTER \d+\s*\n[^\n]+\n([^\n]+)', text)
        if subtitle_match and not subtitle_match.group(1).startswith(('-', 'Weightage', 'CBSE')):
            data['subtitle'] = subtitle_match.group(1).strip()

        # Weightage, Importance, etc.
        for field, pattern in [
            ('weightage', r'Weightage[:\s]*([^\n]+)'),
            ('importance', r'Importance[:\s]*(\w+)'),
            ('map_work', r'Map Work[:\s]*(\w+)'),
            ('pyq_frequency', r'PYQ Frequency[:\s]*([^\n]+)'),
        ]:
            match = re.search(pattern, text)
            if match:
                data[field] = match.group(1).strip()

        # Learning objectives
        obj_match = re.search(r'Learning Objectives[:\s]*\n(.*?)(?=\*|Chapter Contents|$)', text, re.DOTALL | re.IGNORECASE)
        if obj_match:
            data['learning_objectives'] = obj_match.group(1).strip()

        # Syllabus alert
        alert_match = re.search(r'SYLLABUS ALERT[:\s]*([^\n]+)', text)
        if alert_match:
            data['syllabus_alert_text'] = alert_match.group(1).strip()
            data['syllabus_alert_enabled'] = True

        return data

    @staticmethod
    def _parse_part_a_section(text: str) -> Dict[str, Any]:
        """Parse Part A: PYQ Analysis data."""
        data = {'pyq_items': []}

        # Year range
        range_match = re.search(r'PYQ.*?(\d{4}-\d{4})', text)
        if range_match:
            data['pyq_year_range'] = range_match.group(1)

        # Prediction
        pred_match = re.search(r'Prediction[:\s]*([^\n]+)', text)
        if pred_match:
            data['pyq_prediction'] = pred_match.group(1).strip()

        # Syllabus note
        note_match = re.search(r'Syllabus Note[:\s]*([^\n]+)', text)
        if note_match:
            data['pyq_syllabus_note'] = note_match.group(1).strip()

        return data

    @staticmethod
    def _parse_part_b_section(text: str) -> Dict[str, Any]:
        """Parse Part B: Key Concepts data."""
        data = {'concepts': []}

        # Try multiple patterns to find Part B section
        part_b_patterns = [
            r'Part B[:\s]*Key Concepts(.*?)(?=Part [C-G]|End of Chapter|$)',
            r'Key Concepts(.*?)(?=Part [C-G]|Model Answers|$)',
            r'Part B(.*?)(?=Part C|$)',
        ]

        part_b_text = None
        for pattern in part_b_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                part_b_text = match.group(1)
                break

        if not part_b_text:
            return data

        # Find numbered concepts - try multiple patterns
        concept_patterns = [
            r'(\d+)\.\s*([^\n]+)',  # "1. Title"
            r'Concept\s*(\d+)[:\s]*([^\n]+)',  # "Concept 1: Title"
            r'(\d+)\)\s*([^\n]+)',  # "1) Title"
        ]

        concepts = []
        for pattern in concept_patterns:
            matches = list(re.finditer(pattern, part_b_text))
            if matches:
                for match in matches:
                    num = match.group(1)
                    title = match.group(2).strip()
                    if title and len(title) > 3 and not title.startswith(('(', '-', '•', 'mark')):
                        concepts.append({
                            'number': int(num),
                            'title': title,
                            'content': '',
                            'ncert_line': '',
                            'memory_trick': '',
                            'did_you_know': ''
                        })
                break

        if concepts:
            data['concepts'] = concepts

        return data

    @staticmethod
    def _parse_part_c_section(text: str) -> Dict[str, Any]:
        """Parse Part C: Model Answers data."""
        return {}

    @staticmethod
    def _parse_part_d_section(text: str) -> Dict[str, Any]:
        """Parse Part D: Practice Questions data."""
        return {}

    @staticmethod
    def _parse_part_e_section(text: str) -> Dict[str, Any]:
        """Parse Part E: Map Work data."""
        data = {}

        # Map items
        items = re.findall(r'\d+\.\s*([^\n]+?)(?=\d+\.|$)', text)
        if items:
            data['map_items'] = [item.strip() for item in items if item.strip()]

        # Map tips
        tips_match = re.search(r'Map.*Tips[:\s]*\n(.*?)(?=Part|$)', text, re.DOTALL | re.IGNORECASE)
        if tips_match:
            data['map_tips'] = tips_match.group(1).strip()

        return data

    @staticmethod
    def _parse_part_f_section(text: str) -> Dict[str, Any]:
        """Parse Part F: Quick Revision data."""
        return {}

    @staticmethod
    def _parse_part_g_section(text: str) -> Dict[str, Any]:
        """Parse Part G: Exam Strategy data."""
        return {}


class PdfParser:
    """Parse PDF files to extract chapter data."""

    @staticmethod
    def parse(file_bytes: bytes) -> Optional[ChapterData]:
        """
        Parse a PDF file and extract chapter data.

        Args:
            file_bytes: The PDF file content as bytes

        Returns:
            ChapterData object if successful, None otherwise
        """
        try:
            # Try PyMuPDF first
            try:
                import fitz  # PyMuPDF

                doc = fitz.open(stream=file_bytes, filetype="pdf")
                text_content = ""
                for page in doc:
                    text_content += page.get_text()
                doc.close()

            except ImportError:
                # Fallback to pdfplumber
                try:
                    import pdfplumber

                    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                        text_content = ""
                        for page in pdf.pages:
                            text_content += page.extract_text() or ""

                except ImportError:
                    return None

            # Use the same extraction logic as DOCX
            return DocxParser._extract_chapter_data(text_content)

        except Exception:
            return None


def parse_document(file_bytes: bytes, file_type: str) -> Optional[ChapterData]:
    """
    Parse a document file and extract chapter data.

    Args:
        file_bytes: The file content as bytes
        file_type: File extension ('json', 'docx', 'pdf')

    Returns:
        ChapterData object if successful, None otherwise
    """
    if file_type == 'docx':
        return DocxParser.parse(file_bytes)
    elif file_type == 'pdf':
        return PdfParser.parse(file_bytes)
    else:
        return None


def parse_section(file_bytes: bytes, file_type: str, section: str) -> Dict[str, Any]:
    """
    Parse a specific section from a document.

    Args:
        file_bytes: The file content as bytes
        file_type: File extension ('docx', 'pdf')
        section: Section to parse ('cover', 'part_a', 'part_b', etc.)

    Returns:
        Dict with section-specific data
    """
    if file_type == 'docx':
        return DocxParser.parse_section(file_bytes, section)
    elif file_type == 'pdf':
        # For PDF, extract text first then use same logic
        try:
            import fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            # Route to appropriate parser
            parsers = {
                'cover': DocxParser._parse_cover_section,
                'part_a': DocxParser._parse_part_a_section,
                'part_b': DocxParser._parse_part_b_section,
                'part_c': DocxParser._parse_part_c_section,
                'part_d': DocxParser._parse_part_d_section,
                'part_e': DocxParser._parse_part_e_section,
                'part_f': DocxParser._parse_part_f_section,
                'part_g': DocxParser._parse_part_g_section,
            }
            parser_func = parsers.get(section)
            return parser_func(text) if parser_func else {}
        except Exception:
            return {}
    return {}
