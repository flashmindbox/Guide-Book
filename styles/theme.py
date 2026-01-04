"""
Theme constants for Guide Book Generator.
All colors, fonts, and styling values used throughout the application.
Matches the demo PDF exactly.
"""

from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# =============================================================================
# COLOR DEFINITIONS (RGB Hex)
# =============================================================================

class Colors:
    """Color constants used throughout the application."""

    # Primary colors (3-color hierarchy)
    PRIMARY_BLUE = '#1E40AF'      # Deeper blue, more professional - headers, titles
    ACCENT_RED = '#B91C1C'        # Deep red for marks/warnings only
    BODY_TEXT = '#374151'         # Dark gray for all body text

    # Semantic colors (for backwards compatibility)
    DANGER_RED = '#B91C1C'        # Same as ACCENT_RED
    SUCCESS_GREEN = '#059669'     # Only for checkmarks/answers
    WARNING_ORANGE = '#D97706'    # Rarely used

    # Legacy aliases
    DARK_GRAY = '#374151'         # Body text (alias for BODY_TEXT)
    LIGHT_GRAY = '#6B7280'        # Secondary text
    BLACK = '#000000'
    WHITE = '#FFFFFF'

    # Background colors (simplified)
    BG_INFO = '#EFF6FF'           # Light blue - for NCERT, Learning Objectives
    BG_TIP = '#F0FDF4'            # Light green - for Did You Know, Memory Tricks
    BG_WARNING = '#FEF2F2'        # Light red - for Alerts, Mistakes
    BG_NEUTRAL = '#F9FAFB'        # Light gray - for Contents, Tables

    # Legacy background aliases
    BG_LIGHT_GRAY = '#F9FAFB'     # Alias for BG_NEUTRAL
    BG_LIGHT_BLUE = '#EFF6FF'     # Alias for BG_INFO
    BG_LIGHT_RED = '#FEF2F2'      # Alias for BG_WARNING
    BG_LIGHT_GREEN = '#F0FDF4'    # Alias for BG_TIP
    BG_LIGHT_YELLOW = '#FFFBEB'   # Tips, warnings (legacy)
    BG_LIGHT_ORANGE = '#FFF7ED'   # Medium importance highlights (legacy)

    # Border colors (for left-border boxes)
    BORDER_INFO = '#1E40AF'       # Blue
    BORDER_TIP = '#059669'        # Green
    BORDER_WARNING = '#B91C1C'    # Red
    BORDER_NEUTRAL = '#E5E7EB'    # Gray

    # Legacy border aliases
    BORDER_GRAY = '#E5E7EB'
    BORDER_BLUE = '#BFDBFE'
    BORDER_RED = '#FECACA'
    BORDER_GREEN = '#A7F3D0'

    # Table colors
    TABLE_HEADER_BG = '#DBEAFE'   # Light blue header
    TABLE_ALT_ROW = '#F9FAFB'     # Alternating rows

    # Legacy table aliases
    TABLE_HEADER_BLUE = '#DBEAFE'
    TABLE_HEADER_GRAY = '#F3F4F6'

    @staticmethod
    def hex_to_rgb(hex_color: str) -> RGBColor:
        """Convert hex color to python-docx RGBColor."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGBColor(r, g, b)

    @classmethod
    def get_importance_color(cls, importance: str) -> str:
        """Get color based on importance level."""
        mapping = {
            'High': cls.DANGER_RED,
            'Medium': cls.WARNING_ORANGE,
            'Low-Medium': cls.SUCCESS_GREEN,
            'Low': cls.SUCCESS_GREEN,
        }
        return mapping.get(importance, cls.DARK_GRAY)

    @classmethod
    def get_frequency_color(cls, frequency: str) -> str:
        """Get color based on PYQ frequency."""
        mapping = {
            'Every Year': cls.DANGER_RED,
            'High': cls.DANGER_RED,
            'Moderate': cls.PRIMARY_BLUE,
            'Low': cls.SUCCESS_GREEN,
            'Rare': cls.LIGHT_GRAY,
        }
        return mapping.get(frequency, cls.DARK_GRAY)

    @classmethod
    def get_pyq_frequency_color(cls, count: int) -> str:
        """Get color based on PYQ appearance count."""
        if count >= 6:
            return cls.DANGER_RED      # 6+ times = Red
        elif count == 5:
            return cls.PRIMARY_BLUE    # 5 times = Blue
        elif count >= 3:
            return cls.SUCCESS_GREEN   # 3-4 times = Green
        else:
            return cls.DARK_GRAY       # 1-2 times = Gray

    @classmethod
    def to_css_variables(cls) -> str:
        """Generate CSS :root block with all color variables."""
        return f"""
        :root {{
            --primary-blue: {cls.PRIMARY_BLUE};
            --accent-red: {cls.ACCENT_RED};
            --body-text: {cls.BODY_TEXT};
            --success-green: {cls.SUCCESS_GREEN};
            --warning-orange: {cls.WARNING_ORANGE};
            --light-gray: {cls.LIGHT_GRAY};
            --dark-gray: {cls.DARK_GRAY};
            --white: {cls.WHITE};
            --black: {cls.BLACK};

            --bg-info: {cls.BG_INFO};
            --bg-tip: {cls.BG_TIP};
            --bg-warning: {cls.BG_WARNING};
            --bg-neutral: {cls.BG_NEUTRAL};

            --border-info: {cls.BORDER_INFO};
            --border-tip: {cls.BORDER_TIP};
            --border-warning: {cls.BORDER_WARNING};
            --border-neutral: {cls.BORDER_NEUTRAL};

            --table-header-bg: {cls.TABLE_HEADER_BG};
            --table-alt-row: {cls.TABLE_ALT_ROW};
        }}
        """


# =============================================================================
# FONT DEFINITIONS
# =============================================================================

class Fonts:
    """Font constants used throughout the application."""

    # Font families
    PRIMARY = 'Arial'              # Changed from Calibri to match HTML
    DECORATIVE = 'MS Gothic'       # For decorative lines (━)
    EMOJI = 'Segoe UI Symbol'      # For emoji support
    MONOSPACE = 'Consolas'         # For code blocks

    # Font sizes (in points) - refined for professional look
    SIZE_CHAPTER_TITLE = Pt(24)    # Chapter number and title (increased from 22)
    SIZE_PART_HEADER = Pt(16)      # Part headers (Part A, Part B, etc.) (increased from 14)
    SIZE_SECTION_TITLE = Pt(14)    # Section titles within parts
    SIZE_CONCEPT_TITLE = Pt(12)    # Concept numbered titles
    SIZE_SUBTITLE = Pt(12)         # Subtitles
    SIZE_TABLE_HEADER = Pt(11)     # Table headers
    SIZE_BODY = Pt(11)             # Regular body text
    SIZE_BODY_SMALL = Pt(10)       # Smaller body text
    SIZE_CAPTION = Pt(9)           # Captions, notes
    SIZE_FOOTER = Pt(8)            # Footer, metadata

    # Line spacing
    LINE_SPACING_SINGLE = 1.0
    LINE_SPACING_NORMAL = 1.4      # For readability
    LINE_SPACING_RELAXED = 1.5


# =============================================================================
# PAGE LAYOUT DEFINITIONS
# =============================================================================

class PageLayout:
    """Page layout constants."""

    # Page sizes (width, height)
    SIZES = {
        'A4': (Inches(8.27), Inches(11.69)),
        'A5': (Inches(5.83), Inches(8.27)),
        'Letter': (Inches(8.5), Inches(11)),
        'Legal': (Inches(8.5), Inches(14)),
    }

    # Margins - reduced to 1.5cm (0.59 inches) to match HTML
    MARGIN_TOP = Inches(0.59)
    MARGIN_BOTTOM = Inches(0.59)
    MARGIN_LEFT = Inches(0.59)
    MARGIN_RIGHT = Inches(0.59)

    # Header/Footer
    HEADER_DISTANCE = Inches(0.5)
    FOOTER_DISTANCE = Inches(0.5)


# =============================================================================
# SPACING DEFINITIONS
# =============================================================================

class Spacing:
    """Spacing constants for paragraphs and elements."""

    # Paragraph spacing (in points) - reduced to match HTML
    PARA_BEFORE_NONE = Pt(0)
    PARA_BEFORE_SMALL = Pt(3)
    PARA_BEFORE_NORMAL = Pt(3)      # Reduced from 6
    PARA_BEFORE_LARGE = Pt(6)       # Reduced from 12
    PARA_BEFORE_SECTION = Pt(10)    # Reduced from 18

    PARA_AFTER_NONE = Pt(0)
    PARA_AFTER_SMALL = Pt(3)
    PARA_AFTER_NORMAL = Pt(3)       # Reduced from 6
    PARA_AFTER_LARGE = Pt(6)        # Reduced from 12

    # Table cell padding
    CELL_PADDING = Twips(100)

    # Box padding
    BOX_PADDING = Inches(0.15)


# =============================================================================
# DECORATIVE ELEMENTS
# =============================================================================

class Decorative:
    """Decorative elements and special characters."""

    # Line characters
    HEAVY_LINE = '━' * 34          # Heavy horizontal line
    LIGHT_LINE = '─' * 50          # Light horizontal line
    DOUBLE_LINE = '═' * 34         # Double horizontal line

    # Icons/Emojis
    ICON_TARGET = '🎯'             # Learning objectives, predictions
    ICON_BOOK = '📑'               # Chapter contents
    ICON_WARNING = '⚠️'            # Syllabus alert
    ICON_CHART = '📊'              # PYQ Analysis
    ICON_CONCEPTS = '📖'           # Key Concepts
    ICON_CHECK = '✅'              # Complete/correct
    ICON_CROSS = '❌'              # Delete/wrong
    ICON_BULB = '💡'               # Tips, memory tricks
    ICON_STAR = '⭐'               # Important
    ICON_TIME = '⏱️'               # Time management
    ICON_PENCIL = '📝'             # Practice
    ICON_MAP = '🗺️'               # Map work
    ICON_BRAIN = '🧠'              # Memory
    ICON_QUESTION = '❓'           # Questions
    ICON_ANSWER = '✔️'             # Answers

    # Progress indicators
    PROGRESS_COMPLETE = '✅'
    PROGRESS_PARTIAL = '🔶'
    PROGRESS_EMPTY = '⬜'


# =============================================================================
# TABLE STYLES
# =============================================================================

class TableStyles:
    """Table styling constants."""

    # Column widths for common tables (in inches)
    PYQ_TABLE_WIDTHS = [Inches(4.5), Inches(0.75), Inches(2.0)]  # Question, Marks, Years
    METADATA_TABLE_WIDTHS = [Inches(1.75)] * 4                    # 4 equal columns
    COMPARISON_TABLE_WIDTHS = [Inches(1.5), Inches(2.5), Inches(2.5)]  # Aspect, Col1, Col2

    # MCQ answer grid
    MCQ_ANSWERS_PER_ROW = 5


# =============================================================================
# PART CONFIGURATIONS
# =============================================================================

class PartConfig:
    """Default part configurations."""

    DEFAULT_PARTS = [
        {'id': 'A', 'name': 'PYQ Analysis', 'enabled': True, 'removable': False, 'order': 1},
        {'id': 'B', 'name': 'Key Concepts', 'enabled': True, 'removable': False, 'order': 2},
        {'id': 'C', 'name': 'Model Answers', 'enabled': True, 'removable': True, 'order': 3},
        {'id': 'D', 'name': 'Practice Questions', 'enabled': True, 'removable': True, 'order': 4},
        {'id': 'E', 'name': 'Map Work', 'enabled': True, 'removable': True, 'order': 5},
        {'id': 'F', 'name': 'Quick Revision', 'enabled': True, 'removable': True, 'order': 6},
        {'id': 'G', 'name': 'Exam Strategy', 'enabled': True, 'removable': True, 'order': 7},
    ]

    # Part descriptions for cover page
    DEFAULT_DESCRIPTIONS = {
        'A': '10-year data with predictions and syllabus note',
        'B': 'Core topics with memory tricks and exam-focused explanations',
        'C': 'Examiner-approved answers with marking scheme',
        'D': 'MCQs, AR, SA, LA, HOTS, CBQs with answer hints',
        'E': 'CBSE prescribed locations and marking tips',
        'F': 'One-page summary, memory tricks compilation, key dates',
        'G': 'Time management, marking scheme insights, last-minute tips',
    }


# =============================================================================
# DIFFICULTY LEVELS
# =============================================================================

class Difficulty:
    """Difficulty level indicators for questions."""

    EASY = '[E]'
    MEDIUM = '[M]'
    HARD = '[H]'

    COLORS = {
        'E': Colors.SUCCESS_GREEN,
        'M': Colors.WARNING_ORANGE,
        'H': Colors.DANGER_RED,
    }


# =============================================================================
# WEIGHTAGE OPTIONS
# =============================================================================

class Weightage:
    """Weightage options for chapters."""

    OPTIONS = [
        '1-2 Marks',
        '2-3 Marks',
        '3-4 Marks',
        '4-5 Marks',
        '5-6 Marks',
        '6-8 Marks',
    ]

    DEFAULT = '4-5 Marks'


# =============================================================================
# IMPORTANCE OPTIONS
# =============================================================================

class Importance:
    """Importance level options."""

    OPTIONS = ['High', 'Medium', 'Low-Medium', 'Low']
    DEFAULT = 'High'


# =============================================================================
# PYQ FREQUENCY OPTIONS
# =============================================================================

class PYQFrequency:
    """PYQ frequency options."""

    OPTIONS = ['Every Year', 'High', 'Moderate', 'Low', 'Rare']
    DEFAULT = 'Every Year'


# =============================================================================
# YEAR RANGE OPTIONS
# =============================================================================

class YearRange:
    """Year range options for PYQ analysis."""

    OPTIONS = [
        '2015-2024',
        '2016-2025',
        '2017-2026',
        '2018-2027',
        '2019-2028',
    ]
    DEFAULT = '2015-2024'


# =============================================================================
# UNIFIED ICON SYSTEM
# =============================================================================

class Icons:
    """PDF-safe icon system using Unicode symbols that render correctly in xhtml2pdf."""

    IMPORTANT = '▸'     # NCERT lines, key points (triangle pointer)
    TIP = '★'           # Did You Know, Memory Tricks, Tips (star)
    TARGET = '◎'        # Learning Objectives, Predictions (target circle)
    WARNING = '⚠'       # Syllabus Alert, Common Mistakes (warning sign - single char)
    CORRECT = '✓'       # Answers, Completed (checkmark)
    WRONG = '✗'         # Mistakes, Incorrect (x mark)
    BOOK = '■'          # Chapter Contents (square)
    CHART = '■'         # Tables, Analysis (square)
    CALENDAR = '■'      # Timeline, Dates (square)
    PENCIL = '■'        # Practice, Write (square)
    CLOCK = '○'         # Time Allocation (circle)
    CHECKLIST = '☐'     # Checklist, Self-Assessment (empty checkbox)
    STAR = '★'          # Important, End Markers (star)


# =============================================================================
# BOX STYLES CONFIGURATION
# =============================================================================

class BoxStyles:
    """Unified box styling configuration."""

    INFO = {
        'bg': '#EFF6FF',
        'border': '#1E40AF',
        'title_color': '#1E40AF',
        'icon': '▸'
    }
    TIP = {
        'bg': '#F0FDF4',
        'border': '#059669',
        'title_color': '#059669',
        'icon': '★'
    }
    DIDYOUKNOW = {
        'bg': '#FFF7ED',
        'border': '#D97706',
        'title_color': '#D97706',
        'icon': '?'
    }
    WARNING = {
        'bg': '#FEF2F2',
        'border': '#B91C1C',
        'title_color': '#B91C1C',
        'icon': '⚠'
    }
    NEUTRAL = {
        'bg': '#F9FAFB',
        'border': '#E5E7EB',
        'title_color': '#374151',
        'icon': ''
    }
