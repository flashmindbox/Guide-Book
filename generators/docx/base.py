"""
Base document generator for Guide Book Generator.
Orchestrates the generation of complete DOCX documents.
"""

from io import BytesIO
from typing import Optional

from docx import Document

from core.models.base import ChapterData
from core.models.parts import PartManager

from .styles import DocxStyles, create_styled_document


class DocumentGenerator:
    """
    Main document generator class.
    Coordinates the generation of all parts of a chapter guide.
    """

    def __init__(self, chapter_data: ChapterData, part_manager: PartManager):
        self.data = chapter_data
        self.part_manager = part_manager
        self.document: Optional[Document] = None
        self.styles: Optional[DocxStyles] = None

    def generate(self) -> Document:
        """
        Generate the complete document.
        Returns the Document object.
        """
        # Create document with styles
        self.document, self.styles = create_styled_document(self.data.page_size)

        # Set up header
        header_text = f"Chapter {self.data.chapter_number}: {self.data.chapter_title}"
        self.styles.add_header(header_text)

        # Set up footer with page numbers
        if self.data.add_page_numbers:
            self.styles.add_footer_with_page_numbers(self.data.page_number_position)

        # Generate cover page
        self._generate_cover_page()

        # Generate each enabled part
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            self._generate_part(part.id)

        return self.document

    def generate_to_bytes(self) -> bytes:
        """
        Generate document and return as bytes.
        Useful for Streamlit download.
        """
        doc = self.generate()
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_to_file(self, filepath: str) -> str:
        """
        Generate document and save to file.
        Returns the filepath.
        """
        doc = self.generate()
        doc.save(filepath)
        return filepath

    def generate_cover_only(self) -> Document:
        """Generate only the cover page."""
        self.document, self.styles = create_styled_document(self.data.page_size)
        self._generate_cover_page()
        return self.document

    def generate_cover_only_to_bytes(self) -> bytes:
        """Generate cover page only and return as bytes."""
        doc = self.generate_cover_only()
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_part_only(self, part_id: str) -> Document:
        """Generate only a specific part (A, B, C, etc.)."""
        self.document, self.styles = create_styled_document(self.data.page_size)
        self._generate_part(part_id)
        return self.document

    def generate_part_only_to_bytes(self, part_id: str) -> bytes:
        """Generate specific part only and return as bytes."""
        doc = self.generate_part_only(part_id)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    def _generate_cover_page(self):
        """Generate the cover page."""
        from .parts.cover_page import CoverPageGenerator
        generator = CoverPageGenerator(self.document, self.data, self.part_manager)
        generator.generate()

    def _generate_part(self, part_id: str):
        """Generate a specific part."""
        generators = {
            'A': self._generate_part_a,
            'B': self._generate_part_b,
            'C': self._generate_part_c,
            'D': self._generate_part_d,
            'E': self._generate_part_e,
            'F': self._generate_part_f,
            'G': self._generate_part_g,
        }

        generator_func = generators.get(part_id.upper())
        if generator_func:
            generator_func()
        else:
            # Handle custom parts (H, I, J, etc.)
            self._generate_custom_part(part_id)

    def _generate_part_a(self):
        """Generate Part A: PYQ Analysis."""
        from .parts.part_a_pyq import PartAGenerator
        generator = PartAGenerator(self.document, self.data)
        generator.generate()

    def _generate_part_b(self):
        """Generate Part B: Key Concepts."""
        from .parts.part_b_concepts import PartBGenerator
        generator = PartBGenerator(self.document, self.data)
        generator.generate()

    def _generate_part_c(self):
        """Generate Part C: Model Answers."""
        from .parts.part_c_answers import PartCGenerator
        generator = PartCGenerator(self.document, self.data)
        generator.generate()

    def _generate_part_d(self):
        """Generate Part D: Practice Questions."""
        from .parts.part_d_practice import PartDGenerator
        generator = PartDGenerator(self.document, self.data)
        generator.generate()

    def _generate_part_e(self):
        """Generate Part E: Subject-specific content.

        Routes to appropriate generator based on subject:
        - History, Geography → Map Work
        - Political Science → Constitutional Articles
        - Economics → Graphs & Data Analysis
        - Mathematics, Physics → Formula Sheet
        - English → Grammar Focus
        - Science, Chemistry, Biology → Lab Manual
        """
        subject = self.data.subject.lower() if self.data.subject else ''

        # Route to appropriate Part E generator based on subject
        if subject in ('political_science', 'civics'):
            from .parts.part_e_constitutional import PartEConstitutionalGenerator
            generator = PartEConstitutionalGenerator(self.document, self.data)
        elif subject == 'economics':
            from .parts.part_e_graphs import PartEGraphsGenerator
            generator = PartEGraphsGenerator(self.document, self.data)
        elif subject in ('mathematics', 'physics', 'maths'):
            from .parts.part_e_formulas import PartEFormulasGenerator
            generator = PartEFormulasGenerator(self.document, self.data)
        elif subject in ('english', 'english_literature', 'english_grammar'):
            from .parts.part_e_grammar import PartEGrammarGenerator
            generator = PartEGrammarGenerator(self.document, self.data)
        elif subject in ('science', 'chemistry', 'biology'):
            from .parts.part_e_lab import PartELabGenerator
            generator = PartELabGenerator(self.document, self.data)
        else:
            # Default: Map Work (for history, geography, and others)
            from .parts.part_e_map import PartEGenerator
            generator = PartEGenerator(self.document, self.data)

        generator.generate()

    def _generate_part_f(self):
        """Generate Part F: Quick Revision."""
        from .parts.part_f_revision import PartFGenerator
        generator = PartFGenerator(self.document, self.data)
        generator.generate()

    def _generate_part_g(self):
        """Generate Part G: Exam Strategy."""
        from .parts.part_g_strategy import PartGGenerator
        generator = PartGGenerator(self.document, self.data)
        generator.generate()

    def _generate_custom_part(self, part_id: str):
        """Generate a custom part (H, I, J, etc.)."""
        from .parts.part_custom import CustomPartGenerator

        # Get the part info from the part manager
        part = self.part_manager.get_part_by_id(part_id)
        if part:
            part_name = part.name
        else:
            part_name = "Custom Section"

        generator = CustomPartGenerator(self.document, self.data, part_id, part_name)
        generator.generate()


def generate_chapter_document(chapter_data: ChapterData,
                              part_manager: PartManager) -> bytes:
    """
    Convenience function to generate a chapter document.
    Returns document as bytes.
    """
    generator = DocumentGenerator(chapter_data, part_manager)
    return generator.generate_to_bytes()
