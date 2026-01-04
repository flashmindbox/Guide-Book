"""
PDF conversion for Guide Book Generator.
Converts DOCX files or HTML to PDF format.
"""

import os
import sys
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple


class PDFConverter:
    """
    Converts documents to PDF format.

    Supports multiple backends:
    1. xhtml2pdf - HTML to PDF (pure Python, no external dependencies)
    2. docx2pdf (Windows/Mac - requires MS Word or LibreOffice)
    3. LibreOffice command line (cross-platform)
    """

    @staticmethod
    def is_html_pdf_available() -> bool:
        """Check if HTML to PDF conversion is available (xhtml2pdf)."""
        try:
            from xhtml2pdf import pisa
            return True
        except ImportError:
            return False

    @staticmethod
    def is_available() -> Tuple[bool, str]:
        """
        Check if PDF conversion is available.
        Returns (available, method_name).
        """
        # Try docx2pdf
        try:
            import docx2pdf
            return True, "docx2pdf"
        except ImportError:
            pass

        # Try LibreOffice
        if PDFConverter._find_libreoffice():
            return True, "libreoffice"

        return False, "none"

    @staticmethod
    def _find_libreoffice() -> Optional[str]:
        """Find LibreOffice executable."""
        possible_paths = []

        if sys.platform == 'win32':
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
        elif sys.platform == 'darwin':
            possible_paths = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            ]
        else:  # Linux
            possible_paths = [
                "/usr/bin/libreoffice",
                "/usr/bin/soffice",
            ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    @classmethod
    def convert_bytes(cls, docx_bytes: bytes) -> Optional[bytes]:
        """
        Convert DOCX bytes to PDF bytes.
        Returns None if conversion fails.
        """
        available, method = cls.is_available()

        if not available:
            return None

        if method == "docx2pdf":
            return cls._convert_with_docx2pdf(docx_bytes)
        elif method == "libreoffice":
            return cls._convert_with_libreoffice(docx_bytes)

        return None

    @classmethod
    def convert_file(cls, docx_path: Path, pdf_path: Optional[Path] = None) -> Optional[Path]:
        """
        Convert DOCX file to PDF file.
        If pdf_path is None, uses same directory with .pdf extension.
        Returns path to PDF file or None if conversion fails.
        """
        if pdf_path is None:
            pdf_path = docx_path.with_suffix('.pdf')

        available, method = cls.is_available()

        if not available:
            return None

        try:
            if method == "docx2pdf":
                import docx2pdf
                docx2pdf.convert(str(docx_path), str(pdf_path))
                return pdf_path
            elif method == "libreoffice":
                return cls._convert_file_with_libreoffice(docx_path, pdf_path)
        except Exception as e:
            print(f"PDF conversion error: {e}")

        return None

    @classmethod
    def _convert_with_docx2pdf(cls, docx_bytes: bytes) -> Optional[bytes]:
        """Convert using docx2pdf library."""
        try:
            import docx2pdf

            # Create temp files
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as docx_tmp:
                docx_tmp.write(docx_bytes)
                docx_path = docx_tmp.name

            pdf_path = docx_path.replace('.docx', '.pdf')

            # Convert
            docx2pdf.convert(docx_path, pdf_path)

            # Read result
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()

            # Cleanup
            os.unlink(docx_path)
            os.unlink(pdf_path)

            return pdf_bytes

        except Exception as e:
            print(f"docx2pdf conversion error: {e}")
            return None

    @classmethod
    def _convert_with_libreoffice(cls, docx_bytes: bytes) -> Optional[bytes]:
        """Convert using LibreOffice command line."""
        import subprocess

        soffice = cls._find_libreoffice()
        if not soffice:
            return None

        try:
            # Create temp directory for conversion
            with tempfile.TemporaryDirectory() as tmpdir:
                docx_path = Path(tmpdir) / "document.docx"

                # Write DOCX
                with open(docx_path, 'wb') as f:
                    f.write(docx_bytes)

                # Convert with LibreOffice
                subprocess.run([
                    soffice,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', tmpdir,
                    str(docx_path)
                ], check=True, capture_output=True)

                # Read PDF result
                pdf_path = Path(tmpdir) / "document.pdf"
                if pdf_path.exists():
                    with open(pdf_path, 'rb') as f:
                        return f.read()

        except Exception as e:
            print(f"LibreOffice conversion error: {e}")

        return None

    @classmethod
    def _convert_file_with_libreoffice(cls, docx_path: Path, pdf_path: Path) -> Optional[Path]:
        """Convert file using LibreOffice command line."""
        import subprocess

        soffice = cls._find_libreoffice()
        if not soffice:
            return None

        try:
            # Convert
            subprocess.run([
                soffice,
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(pdf_path.parent),
                str(docx_path)
            ], check=True, capture_output=True)

            # LibreOffice uses input filename with .pdf extension
            result_path = pdf_path.parent / (docx_path.stem + '.pdf')

            # Rename if needed
            if result_path != pdf_path and result_path.exists():
                result_path.rename(pdf_path)

            if pdf_path.exists():
                return pdf_path

        except Exception as e:
            print(f"LibreOffice conversion error: {e}")

        return None

    @classmethod
    def convert_html_to_pdf(cls, html_content: str) -> Optional[bytes]:
        """
        Convert HTML content to PDF using xhtml2pdf.
        This method doesn't require Word or LibreOffice.

        Args:
            html_content: HTML string to convert

        Returns:
            PDF bytes or None if conversion fails
        """
        try:
            from xhtml2pdf import pisa

            # Create a BytesIO buffer for the PDF
            pdf_buffer = BytesIO()

            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=pdf_buffer,
                encoding='utf-8'
            )

            # Check if conversion was successful
            if pisa_status.err:
                print(f"xhtml2pdf conversion error: {pisa_status.err}")
                return None

            # Get the PDF bytes
            pdf_buffer.seek(0)
            return pdf_buffer.read()

        except ImportError:
            print("xhtml2pdf not installed. Run: pip install xhtml2pdf")
            return None
        except Exception as e:
            print(f"HTML to PDF conversion error: {e}")
            return None
