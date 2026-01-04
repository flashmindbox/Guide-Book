"""
Book Formatting Specification
==============================

This file defines the SINGLE SOURCE OF TRUTH for all book chapter formatting.
All chapters in the book MUST follow these specifications to ensure visual
consistency across the entire publication.

Based on analysis of: Ch-1_History_CBSE_Class_10_FINAL.docx
"""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

# =============================================================================
# PAGE LAYOUT SPECIFICATION
# =============================================================================

class BookPageLayout:
    """
    Exact page layout to be used for ALL chapters.
    Based on reference DOCX analysis.
    """
    # Page size (A4)
    PAGE_WIDTH = Inches(8.27)
    PAGE_HEIGHT = Inches(11.69)

    # Margins (exactly as in reference)
    MARGIN_LEFT = Inches(0.83)
    MARGIN_RIGHT = Inches(0.83)
    MARGIN_TOP = Inches(0.83)
    MARGIN_BOTTOM = Inches(0.69)


# =============================================================================
# COLOR PALETTE - BOOK STANDARD
# =============================================================================

class BookColors:
    """
    Official color palette for the entire book.
    These colors MUST be used consistently across all chapters.
    """

    # Primary heading color (section headers)
    HEADING_BLUE = '#2563EB'          # Tailwind blue-600

    # Important dates/years - RED BOLD
    YEAR_RED = '#DC2626'              # Tailwind red-600

    # Memory tricks - GREEN ITALIC RIGHT-ALIGNED
    MEMORY_GREEN = '#059669'          # Tailwind emerald-600

    # Body text
    BODY_TEXT = '#000000'             # Pure black for maximum readability

    # Secondary text
    SECONDARY_TEXT = '#374151'        # Tailwind gray-700

    # Table header background
    TABLE_HEADER_BG = '#DBEAFE'       # Tailwind blue-100

    # Info box backgrounds
    BG_INFO = '#EFF6FF'               # Light blue - Learning Objectives, NCERT
    BG_TIP = '#F0FDF4'                # Light green - Did You Know, Memory Tricks
    BG_WARNING = '#FEF2F2'            # Light red - Syllabus Alert, Common Mistakes
    BG_NEUTRAL = '#F9FAFB'            # Light gray - Chapter Contents
    BG_ORANGE = '#FFF7ED'             # Light orange - Did You Know alternative

    # Frequency-based row colors (for PYQ table)
    FREQ_HIGH_BG = '#FEF2F2'          # 6+ times - Light red
    FREQ_MEDIUM_BG = '#EFF6FF'        # 5 times - Light blue
    FREQ_LOW_BG = '#F0FDF4'           # 3-4 times - Light green

    # Border colors
    BORDER_GRAY = '#E5E7EB'           # Standard border
    BORDER_BLUE = '#1E40AF'           # Info box left border
    BORDER_GREEN = '#059669'          # Tip box left border
    BORDER_RED = '#B91C1C'            # Warning box left border

    @staticmethod
    def hex_to_rgb(hex_color: str) -> RGBColor:
        """Convert hex color to python-docx RGBColor."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGBColor(r, g, b)


# =============================================================================
# TYPOGRAPHY SPECIFICATION
# =============================================================================

class BookFonts:
    """
    Font specifications for the entire book.
    """
    # Primary font family
    PRIMARY = 'Arial'

    # Decorative font for horizontal lines
    DECORATIVE = 'MS Gothic'

    # Emoji support
    EMOJI = 'Segoe UI Symbol'

    # -------------------------------------------------------------------------
    # FONT SIZES
    # -------------------------------------------------------------------------

    # Cover page
    CHAPTER_NUMBER = Pt(24)           # "CHAPTER 1"
    CHAPTER_TITLE = Pt(24)            # Chapter title (bold)
    HEADER_TEXT = Pt(11)              # "CBSE Class 10 | Social Science | History"

    # Section headers (Part B content)
    SECTION_HEADER = Pt(16)           # Heading 2 - "1. The French Revolution..."
    SUBSECTION_HEADER = Pt(14)        # Heading 3 - "Model Answers with..."

    # Content
    BODY_TEXT = Pt(11)                # Regular paragraph text
    BODY_SMALL = Pt(10)               # Smaller body text (options, etc.)

    # Tables
    TABLE_HEADER = Pt(11)             # Table header text
    TABLE_CELL = Pt(11)               # Table cell text

    # Special elements
    METADATA = Pt(10)                 # Metadata table values
    FOOTER = Pt(8)                    # Page footer


# =============================================================================
# TEXT FORMATTING PATTERNS
# =============================================================================

class BookTextPatterns:
    """
    Standard text formatting patterns to be applied consistently.
    """

    # Key terms formatting
    KEY_TERM = {
        'bold': True,
        'italic': False,
        'color': None  # Uses BODY_TEXT color
    }

    # Important years (e.g., 1789, 1821, 1861)
    IMPORTANT_YEAR = {
        'bold': True,
        'italic': False,
        'color': '#DC2626'  # YEAR_RED
    }

    # Foreign terms (e.g., la patrie, le citoyen, das volk)
    FOREIGN_TERM = {
        'bold': True,
        'italic': True,
        'color': None  # Uses BODY_TEXT color
    }

    # Memory trick text
    MEMORY_TRICK = {
        'bold': False,
        'italic': True,
        'color': '#059669',  # MEMORY_GREEN
        'alignment': WD_ALIGN_PARAGRAPH.RIGHT
    }

    # Memory trick acronym (e.g., FLAT-CUN, PEACE, BRAN-PS)
    MEMORY_ACRONYM = {
        'bold': True,
        'italic': True,
        'color': '#059669'  # MEMORY_GREEN
    }

    # Section header (Heading 2)
    SECTION_HEADER = {
        'font_name': 'Arial',
        'font_size': Pt(16),
        'bold': False,  # Style handles this
        'color': '#2563EB'  # HEADING_BLUE
    }


# =============================================================================
# DOCUMENT STRUCTURE SPECIFICATION
# =============================================================================

class BookStructure:
    """
    Standard document structure for all chapters.
    Each chapter MUST follow this exact structure for consistency.
    """

    # Cover Page Elements (in order)
    COVER_PAGE = [
        'header_text',           # "CBSE Class 10 | Social Science | History"
        'decorative_line_heavy', # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        'chapter_number',        # "CHAPTER 1"
        'chapter_title',         # "The Rise of Nationalism in Europe"
        'decorative_line_heavy', # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        'metadata_table',        # Weightage | Map Work | Importance | PYQ Frequency
        'frequency_legend',      # "Frequency: Red = 6+ times  Blue = 5 times..."
        'decorative_line_light', # ──────────────────────────────────────────────────
        'syllabus_alert',        # (conditional) "★ Syllabus Note: ..."
        'learning_objectives',   # "🎯 Learning Objectives" box
        'chapter_contents',      # "📑 Chapter Contents" box
        'qr_codes',              # (optional) QR code images
    ]

    # Part A: PYQ Analysis
    PART_A = [
        'part_header',           # "Part A: PYQ Analysis (2015-2024)"
        'pyq_table',             # 3-column table: Question | Marks | Years Asked
        'prediction_box',        # "🎯 2025 Prediction" box
    ]

    # Part B: Key Concepts
    PART_B = [
        'part_header',           # "Part B: Key Concepts"
        'concepts',              # Numbered sections with content
        # Each concept contains:
        # - Section header (Heading 2)
        # - Body text with key terms bolded
        # - NCERT boxes (📌 NCERT Exact Line)
        # - Did You Know boxes (💡 Did You Know?)
        # - Memory tricks (right-aligned, green, italic)
        'comparison_tables',     # (if applicable)
        'common_mistakes',       # "Common Mistakes to Avoid" section
        'timeline',              # "Important Dates Timeline" section
    ]

    # Part C: Model Answers
    PART_C = [
        'part_header',           # "Part C: Model Answers"
        'section_header',        # "Model Answers with Examiner's Marking Scheme"
        'model_answers',         # Question-answer pairs in boxes
    ]

    # Part D: Practice Questions
    PART_D = [
        'part_header',           # "Part D: Practice Questions"
        'mcqs',                  # MCQs with [E]/[M]/[H] difficulty
        'mcq_answers',           # Answer grid
        'assertion_reason',      # A-R questions
        'ar_answers',            # A-R answer grid
        'short_answer',          # 3-mark questions
        'long_answer',           # 5-mark questions
        'source_based',          # Source/passage-based questions
        'case_study',            # Case study questions
        'picture_based',         # (if applicable)
    ]

    # Part E: Map Work
    PART_E = [
        'part_header',           # "Part E: Map Work"
        'map_items_table',       # 2-column table with locations
        'map_image',             # (if applicable) embedded map
    ]

    # Part F: Quick Revision
    PART_F = [
        'part_header',           # "Part F: Quick Revision"
        'key_points',            # "Key Points" section
        'key_terms_table',       # Term | Definition table
        'memory_tricks',         # Compiled memory tricks
    ]

    # Part G: Exam Strategy
    PART_G = [
        'part_header',           # "Part G: Exam Strategy"
        'time_allocation',       # Time management table
        'common_mistakes',       # Common mistakes table
        'examiner_tips',         # Pro tips section
        'self_assessment',       # Checklist items
    ]


# =============================================================================
# DECORATIVE ELEMENTS
# =============================================================================

class BookDecorativeElements:
    """
    Decorative elements for visual consistency.
    """
    # Horizontal lines
    HEAVY_LINE = '━' * 34           # Cover page separators
    LIGHT_LINE = '─' * 50           # Section separators

    # Icons (emoji for DOCX)
    ICON_TARGET = '🎯'               # Learning objectives, predictions
    ICON_CONTENTS = '📑'             # Chapter contents
    ICON_WARNING = '★'               # Syllabus alert (star for PDF compatibility)
    ICON_NCERT = '📌'                # NCERT exact lines
    ICON_TIP = '💡'                  # Did You Know
    ICON_CHECK = '✔'                 # Answers, completed
    ICON_CROSS = '❌'                # Mistakes


# =============================================================================
# BOX STYLES SPECIFICATION
# =============================================================================

class BookBoxStyles:
    """
    Standard box styles for information boxes.
    """

    # Learning Objectives box
    LEARNING_OBJECTIVES = {
        'icon': '🎯',
        'title': 'Learning Objectives',
        'bg_color': '#EFF6FF',
        'border_color': '#1E40AF',
        'title_color': '#1E40AF',
        'use_left_border': True,
    }

    # Chapter Contents box
    CHAPTER_CONTENTS = {
        'icon': '📑',
        'title': 'Chapter Contents',
        'bg_color': '#F9FAFB',
        'border_color': '#E5E7EB',
        'title_color': '#374151',
        'use_left_border': False,
    }

    # Syllabus Alert box
    SYLLABUS_ALERT = {
        'icon': '★',
        'title': 'Syllabus Note',
        'bg_color': '#FEF2F2',
        'border_color': '#B91C1C',
        'title_color': '#B91C1C',
        'use_left_border': True,
    }

    # NCERT Exact Line box
    NCERT_LINE = {
        'icon': '📌',
        'title': 'NCERT Exact Line',
        'bg_color': '#EFF6FF',
        'border_color': '#1E40AF',
        'title_color': '#1E40AF',
        'use_left_border': True,
    }

    # Did You Know box
    DID_YOU_KNOW = {
        'icon': '💡',
        'title': 'Did You Know?',
        'bg_color': '#FFF7ED',
        'border_color': '#D97706',
        'title_color': '#D97706',
        'use_left_border': True,
    }

    # Famous Quote box
    FAMOUS_QUOTE = {
        'icon': '📌',
        'title': 'Famous Quote (Often Asked)',
        'bg_color': '#EFF6FF',
        'border_color': '#1E40AF',
        'title_color': '#1E40AF',
        'use_left_border': True,
    }

    # Prediction box
    PREDICTION = {
        'icon': '🎯',
        'title': '2025 Prediction',
        'bg_color': '#EFF6FF',
        'border_color': '#1E40AF',
        'title_color': '#1E40AF',
        'use_left_border': True,
    }

    # Answer box
    ANSWER = {
        'icon': '✔',
        'title': 'Answers',
        'bg_color': '#F0FDF4',
        'border_color': '#059669',
        'title_color': '#059669',
        'use_left_border': True,
    }

    # Model Answer box
    MODEL_ANSWER = {
        'icon': '',
        'title': '',  # Q1, Q2, etc. set dynamically
        'bg_color': '#F9FAFB',
        'border_color': '#E5E7EB',
        'title_color': '#374151',
        'use_left_border': False,
    }

    # Common Mistakes box
    COMMON_MISTAKES = {
        'icon': '⚠',
        'title': 'Common Mistakes',
        'bg_color': '#FEF2F2',
        'border_color': '#B91C1C',
        'title_color': '#B91C1C',
        'use_left_border': True,
    }


# =============================================================================
# TABLE SPECIFICATIONS
# =============================================================================

class BookTableStyles:
    """
    Standard table formatting for consistency.
    """

    # Metadata table (cover page)
    METADATA_TABLE = {
        'columns': 4,
        'bg_color': '#F9FAFB',
        'border_color': '#E5E7EB',
        'text_centered': True,
    }

    # PYQ Analysis table
    PYQ_TABLE = {
        'columns': 3,
        'header_bg': '#DBEAFE',
        'header_text_color': '#374151',
        'border_color': '#E5E7EB',
        'col_widths': [Inches(4.0), Inches(0.75), Inches(1.75)],
    }

    # Comparison table
    COMPARISON_TABLE = {
        'header_bg': '#DBEAFE',
        'header_text_color': '#2563EB',
        'border_color': '#E5E7EB',
    }

    # Timeline table
    TIMELINE_TABLE = {
        'columns': 2,
        'header_bg': '#DBEAFE',
        'col_widths': [Inches(1.0), Inches(5.5)],  # Year | Event
    }

    # Key Terms table
    KEY_TERMS_TABLE = {
        'columns': 2,
        'header_bg': '#DBEAFE',
        'col_widths': [Inches(2.0), Inches(4.5)],  # Term | Definition
    }

    # Time Allocation table (Exam Strategy)
    TIME_ALLOCATION_TABLE = {
        'columns': 3,
        'header_bg': '#DBEAFE',
        'col_widths': [Inches(2.5), Inches(1.5), Inches(2.5)],  # Type | Marks | Time
    }

    # Common Mistakes table
    MISTAKES_TABLE = {
        'columns': 2,
        'col_widths': [Inches(3.25), Inches(3.25)],  # Mistake | Correction
    }


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_chapter_data(chapter_data: dict) -> list:
    """
    Validate that chapter data follows book formatting standards.
    Returns a list of validation warnings/errors.
    """
    warnings = []

    # Check required fields
    required_fields = ['chapter_number', 'chapter_title', 'subject']
    for field in required_fields:
        if not chapter_data.get(field):
            warnings.append(f"Missing required field: {field}")

    # Check learning objectives
    objectives = chapter_data.get('learning_objectives', [])
    if len(objectives) < 3:
        warnings.append("Consider adding at least 3 learning objectives")

    # Check concepts
    concepts = chapter_data.get('concepts', [])
    for i, concept in enumerate(concepts):
        if not concept.get('title'):
            warnings.append(f"Concept {i+1} missing title")
        if not concept.get('content'):
            warnings.append(f"Concept {i+1} missing content")

    return warnings


# =============================================================================
# USAGE EXAMPLE
# =============================================================================
"""
Usage in document generator:

from config.book_formatting import (
    BookPageLayout,
    BookColors,
    BookFonts,
    BookTextPatterns,
    BookBoxStyles,
    BookTableStyles,
)

# Apply page layout
section.page_width = BookPageLayout.PAGE_WIDTH
section.left_margin = BookPageLayout.MARGIN_LEFT

# Apply colors
run.font.color.rgb = BookColors.hex_to_rgb(BookColors.HEADING_BLUE)

# Apply fonts
run.font.size = BookFonts.SECTION_HEADER

# Create box
box_style = BookBoxStyles.LEARNING_OBJECTIVES
create_styled_box(document, box_style['bg_color'], box_style['title'], ...)
"""
