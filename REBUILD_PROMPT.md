# AI Prompt to Rebuild: CBSE Guide Book Generator

## Project Overview

Build a **Streamlit web application** called "Guide Book Generator" that creates professionally formatted CBSE Class 10 Social Science study guide chapters. The application should generate publication-ready Word documents (DOCX) and PDFs with consistent formatting, QR codes, auto-save, and real-time previews.

---

## Core Requirements

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Document Generation**: python-docx library
- **PDF Generation**: xhtml2pdf (optional, graceful fallback if unavailable)
- **QR Codes**: qrcode library with PIL
- **Storage**: Local file system (JSON for data, autosave directory)

### Supported Subjects
- History
- Geography
- Political Science
- Economics

### Page Sizes
- A4 (210mm × 297mm) - default
- A5 (148mm × 210mm)
- Letter (8.5" × 11")
- Legal (8.5" × 14")

---

## Application Structure

### Navigation Sections (Sidebar Radio Buttons)
1. **Import/Export** - Load/save chapters
2. **Cover Page** - Chapter metadata and header
3. **Part A: PYQ** - Previous Year Questions analysis
4. **Part B: Concepts** - Key concepts (dynamic add/delete)
5. **Part C: Answers** - Model Q&A pairs
6. **Part D: Practice** - MCQs, Short, Long questions
7. **Part E: Map** - Map work items and images
8. **Part F: Revision** - Quick revision content
9. **Part G: Strategy** - Exam strategy tips
10. **Generate** - Final document generation

### Sidebar Features
- Progress bar (0-100% overall completion)
- Section-wise progress indicators (✅ complete, 🔶 partial, ⬜ empty)
- Quick actions (Save Now, Reset)
- Auto-save status display

---

## Data Model (Session State Structure)

```python
data = {
    # Cover Page
    'subject': 'History',  # History/Geography/Political Science/Economics
    'chapter_number': 1,   # 1-20
    'chapter_title': '',
    'subtitle': '',        # Optional section info

    # Metadata
    'weightage': '4-5 Marks',      # 1-2/3-5/4-5/5-8 Marks
    'map_work': 'No',              # Yes/No
    'importance': 'High',          # High/Medium/Low
    'pyq_frequency': 'Every Year', # Every Year/High/Moderate/Low/Rare

    # Syllabus Alert
    'syllabus_alert_enabled': False,
    'syllabus_alert_text': '',

    # Learning Objectives (multiline, 5 main points)
    'learning_objectives': '',

    # Part Descriptions (for cover page Chapter Contents box)
    'part_a_desc': '10-year data with predictions, Marks distribution',
    'part_b_desc': '8 main topics, NCERT lines, Memory tricks',
    'part_c_desc': "8 most repeated questions, Examiner's marking scheme",
    'part_d_desc': '18 MCQs, 8 Assertion-Reason, 10 VSA, 10 SA, 6 LA, 4 HOTS, 2 CBQs',
    'part_e_desc': '6 CBSE prescribed locations, Marking tips',
    'part_f_desc': 'Key points summary, Timeline, Glossary',
    'part_g_desc': 'Time allocation, Topper tips, Common mistakes',

    # Part A: PYQ Analysis
    'pyq_year_range': '2015-2024',
    'pyq_data': '',        # Format: "Question | Marks | Years" per line
    'pyq_prediction': '',  # Single prediction sentence

    # Part B: Key Concepts (dynamic list)
    'concepts': [
        {'number': 1, 'title': '', 'content': ''},
        # ... more concepts
    ],

    # Part C: Model Answers
    'model_answers': '',   # Format: "Q: Question [Marks]\nA: Answer" blocks

    # Part D: Practice Questions
    'practice_mcqs': '',   # Format: "Question | a) | b) | c) | d)" per line
    'practice_short': '',  # One question per line (3 marks)
    'practice_long': '',   # One question per line (5 marks)

    # Part E: Map Work
    'map_work_na': False,  # N/A flag
    'map_items': '',       # One location per line
    'map_image': None,     # File path to uploaded image

    # Part F: Quick Revision
    'revision_content': '',

    # Part G: Exam Strategy
    'exam_strategy': '',

    # Page Settings
    'page_size': 'A4',
    'add_page_numbers': True,
    'page_number_position': 'Bottom Center',

    # QR Codes (optional)
    'qr_practice_url': '',
    'qr_practice_answers_url': '',
}
```

---

## Styling Constants

### Colors (RGB Hex)
```python
COLORS = {
    'PRIMARY_BLUE': '#2563EB',    # Headers, titles
    'DANGER_RED': '#DC2626',      # High importance, weightage
    'SUCCESS_GREEN': '#059669',   # Low importance, memory tricks
    'WARNING_ORANGE': '#F59E0B',  # Medium importance
    'DARK_GRAY': '#374151',       # Regular text
    'BLACK': '#000000',

    # Backgrounds
    'BG_LIGHT_GRAY': '#F9FAFB',   # Info boxes
    'BG_LIGHT_BLUE': '#EFF6FF',   # Learning Objectives
    'BG_LIGHT_RED': '#FEF2F2',    # Syllabus Alert
    'BG_LIGHT_GREEN': '#ECFDF5',  # Memory tricks

    # Borders
    'BORDER_GRAY': '#E5E7EB',
}
```

### Fonts
- **Primary Font**: Calibri
- **Decorative**: MS Gothic (for ━ line characters)
- **Emoji Font**: Segoe UI Symbol

### Font Sizes (Points)
- 24pt: Chapter number and title
- 14pt: Header text
- 12pt: Subtitles, section headers
- 11pt: Body text, table headers
- 10pt: Regular paragraphs
- 8pt: Metadata/footer

### Dynamic Color Coding
```python
# Importance Level
'High' → RED
'Medium' → ORANGE
'Low-Medium' → GREEN
'Low' → GREEN

# PYQ Frequency
'Every Year' → RED
'High' → RED
'Moderate' → BLUE
'Low' → GREEN
'Rare' → GRAY
```

---

## Document Generation: Cover Page Structure

Generate cover page with this exact order:

1. **Header**: "CBSE Class 10 | Social Science | {Subject}" (centered, 14pt)
2. **Decorative Line**: ━━━━━━━━━━━━━━━━━━━━ (34 characters)
3. **Chapter Number**: "CHAPTER {N}" (bold, 24pt, centered)
4. **Chapter Title**: "{Title}" (bold, 24pt, centered)
5. **Subtitle** (if present): italic, 12pt, centered
6. **Decorative Line**
7. **Metadata Table** (4 columns, gray background):
   | Weightage: {value} | Map Work: {value} | Importance: {value} | PYQ Frequency: {value} |
   - Red text for Weightage and Map Work
   - Dynamic colors for Importance and PYQ Frequency
8. **Syllabus Alert Box** (if enabled):
   - Light red background (#FEF2F2)
   - "⚠️ SYLLABUS ALERT:" in red
   - Alert text in bold
9. **Learning Objectives Box**:
   - Light blue background (#EFF6FF)
   - "🎯 Learning Objectives" title in blue
   - "After studying this chapter, you will be able to:" (italic)
   - Bullet points (• prefix, bold text)
10. **Chapter Contents Box**:
    - Light gray background (#F9FAFB)
    - "📑 Chapter Contents" title
    - Seven lines: "Part A: PYQ Analysis — {description}"
    - Part labels in red, part names in bold
11. **QR Codes** (if URLs provided):
    - 2-column layout
    - 1.2" × 1.2" QR images
    - Labels below each

---

## Document Generation: Parts A-G

### Part A: PYQ Analysis
- Page break before
- Header: "Part A: PYQ Analysis" (16pt, bold)
- 3-column table: Question | Marks | Years Asked
- Prediction box at end (blue background with 🎯 icon)

### Part B: Key Concepts
- Page break before
- Header: "Part B: Key Concepts"
- For each concept:
  - Numbered title in blue (12pt, bold)
  - Formatted content with markdown support:
    - `**bold**` → bold
    - `*italic*` → italic
    - `***bold-italic***` → green bold italic
    - `-` prefix → bullet points
  - Memory tricks in right-aligned green boxes with 💡 icon

### Part C: Model Answers
- Page break before
- Header: "Part C: Model Answers"
- For each Q&A:
  - Question (bold, 11pt) with marks in red brackets
  - "Ans." prefix (bold) + answer text
  - Same formatting support as Part B

### Part D: Practice Questions
- Page break before
- Header: "Part D: Practice Questions"
- Subsections:
  - "Multiple Choice Questions (MCQs)" with a) b) c) d) options
  - "Short Answer Questions (3 Marks)"
  - "Long Answer Questions (5 Marks)"

### Part E: Map Work
- Page break before
- Header: "Part E: Map Work"
- If N/A: "N/A for this chapter" (italic)
- If items: numbered list of locations
- If image: embedded centered image (5" wide)

### Part F: Quick Revision
- Page break before
- Header: "Part F: Quick Revision"
- Formatted content with markdown support

### Part G: Exam Strategy
- Page break before
- Header: "Part G: Exam Strategy"
- Formatted content with markdown support

---

## Features to Implement

### 1. Auto-Save System
- Save to `autosave/{subject}_Ch{number}_autosave.json`
- **Throttle**: Only save every 5 seconds (prevents lag)
- Auto-load most recent autosave on startup
- Show "Restored from autosave" notification

### 2. Import/Export

**Import from DOCX:**
- Parse existing Word documents
- Extract chapter metadata, learning objectives
- Parse PYQ tables
- Extract concepts with numbered headings
- Parse Q&A patterns
- Detect section headers

**Import from JSON:**
- Direct data restoration
- Backwards compatible with autosave format

**Export Formats:**
- DOCX: Complete formatted document
- PDF: Via WeasyPrint (HTML → PDF)
- JSON: Full data backup

### 3. QR Code Generation
- Use `qrcode` library with PIL
- Cache generated codes with `@st.cache_data`
- Embed as base64 in HTML previews
- Embed as images in DOCX

### 4. Real-Time Preview
- HTML preview matching PDF/DOCX output exactly
- Show in expandable section
- Estimate page count and warn if >1 page
- Display word counts

### 5. Progress Tracking
- Calculate completion for each section
- Show overall percentage in sidebar
- Per-section indicators (✅/🔶/⬜)

### 6. Subject Templates
Pre-populated content for each subject:
- History: timeline-focused objectives
- Geography: location-focused with map tips
- Political Science: constitutional articles
- Economics: formulas and calculations

### 7. Performance Optimization
- Cache QR codes: `@st.cache_data(ttl=3600)`
- Throttle auto-save (5-second interval)
- Avoid expensive operations in main loop

---

## UI Components by Section

### Cover Page Section
```
Row 1: [Chapter Number (1-20)] [Subject dropdown]
Row 2: [Chapter Title input]
Row 3: [Subtitle input (optional)]
Row 4: [Weightage dropdown] [Map Work dropdown]
Row 5: [Importance dropdown] [PYQ Frequency dropdown]
Row 6: [Syllabus Alert toggle] [Alert text area if enabled]
Row 7: [Learning Objectives text area] [Word count display]
Expander: Part Descriptions (7 text inputs)
Row 8: [QR Practice URL] [QR Answers URL]
Expander: Preview Cover Page (HTML render)
Buttons: [Download Cover PDF] [Download Cover DOCX]
```

### Part B: Key Concepts (Dynamic)
```
For each concept:
  Row: [Delete X] [Number] [Title input]
  Row: [Content text area] [Word count]
  Row: [Duplicate button]
[+ Add New Concept button]
Preview expander showing formatted content
```

### Part D: Practice Questions (Tabbed)
```
Tab 1: MCQs
  - Text area (pipe-delimited format)
  - Question count display
Tab 2: Short Answer
  - Text area (one per line)
Tab 3: Long Answer
  - Text area (one per line)
```

### Generate Section
```
Validation warnings (missing content)
Page Settings:
  [Page Size dropdown] [Page Numbers toggle] [Position dropdown]
Generation buttons:
  [Generate Full DOCX] [Generate Full PDF]
  [Preview Full Document]
Danger Zone:
  [Reset All Data button]
```

---

## Error Handling

1. **xhtml2pdf not available**: Catch ImportError, disable PDF features gracefully and show user-friendly warning
2. **File operations**: Wrap in try-except, show user-friendly errors
3. **DOCX parsing**: Graceful fallback if structure doesn't match
4. **Image uploads**: Validate file types (PNG, JPG only)
5. **Empty fields**: Show warnings but don't block generation

---

## File Structure

```
guide-book/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies (testing, linting)
├── pyproject.toml              # Project configuration and tool settings
├── run.bat                     # Windows launcher
├── config/
│   └── chapters/               # Subject/class chapter configurations (JSON)
├── core/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py             # Pydantic data models (ChapterData, etc.)
│   └── parsers.py              # DOCX/JSON/PDF import parsers
├── generators/
│   ├── __init__.py
│   ├── docx/
│   │   ├── __init__.py
│   │   ├── base.py             # Main DOCX generator orchestrator
│   │   ├── styles.py           # Color, font, spacing constants
│   │   └── parts/              # Part generators (A-G, custom, subject-specific)
│   │       ├── __init__.py
│   │       ├── part_a.py       # PYQ Analysis
│   │       ├── part_b.py       # Key Concepts
│   │       ├── part_c.py       # Model Answers
│   │       ├── part_d.py       # Practice Questions
│   │       ├── part_e.py       # Map Work (default)
│   │       ├── part_e_*.py     # Subject-specific Part E variants
│   │       ├── part_f.py       # Quick Revision
│   │       ├── part_g.py       # Exam Strategy
│   │       └── part_custom.py  # Dynamic custom parts (H, I, J, etc.)
│   └── pdf/
│       ├── __init__.py
│       └── converter.py        # HTML to PDF conversion (xhtml2pdf)
├── ui/
│   ├── __init__.py
│   └── components/
│       ├── __init__.py
│       └── preview.py          # HTML preview and quick export
├── utils/
│   ├── __init__.py
│   ├── autosave.py             # Throttled auto-save manager
│   └── logger.py               # Logging configuration
├── data/
│   ├── autosave/               # Auto-saved JSON files
│   ├── logs/                   # Application logs
│   └── images/                 # Uploaded map images
└── tests/                      # Test files
```

---

## Dependencies (requirements.txt)

```
streamlit>=1.28.0
python-docx>=0.8.11
qrcode[pil]>=7.3
Pillow>=9.0.0
xhtml2pdf>=0.2.17  # Optional: for PDF generation
htmldocx>=0.0.6    # Optional: for HTML to DOCX conversion during import
```

### Optional Dependencies Note

The application supports graceful degradation for optional dependencies:

- **xhtml2pdf**: Required for PDF export. If not installed, PDF generation is disabled with a user-friendly warning.
- **htmldocx**: Required for importing HTML content to DOCX. If not installed, HTML import features show a warning.
- **PyMuPDF (fitz)**: Required for PDF import. If not installed, PDF import is disabled with an informative message.

Users can install optional dependencies individually as needed, or install all development dependencies with:
```bash
pip install -r requirements-dev.txt
```

---

## Key Implementation Notes

1. **Consistent Styling**: All colors, fonts, and spacing must be hardcoded constants - no variation allowed
2. **Markdown Parsing**: Support `**bold**`, `*italic*`, `***bold-italic***`, and `- bullets` in all text areas
3. **Memory Tricks**: Detect "Memory Trick:" or similar patterns and render in special green right-aligned boxes
4. **Table Formatting**: Use consistent column widths in twips (1 inch = 1440 twips)
5. **Page Breaks**: Add before each Part (A-G)
6. **Unicode Support**: Use UTF-8 encoding throughout, support emojis
7. **XSS Protection**: Escape all user input when rendering HTML previews

---

## Sample Icons/Emojis Used

- 🎯 Learning Objectives, Predictions
- 📑 Chapter Contents
- ⚠️ Syllabus Alert
- 📊 PYQ Analysis
- 📖 Key Concepts
- ✅ Complete/Correct
- ❌ Delete/Wrong
- 💡 Tips/Memory tricks
- ⭐ Important
- ⏱️ Time management
- 📝 Practice
- 🗺️ Map work
- 🧠 Memory

---

## Testing Checklist

- [ ] Cover page generates with all 11 sections
- [ ] All 7 parts (A-G) generate correctly
- [ ] DOCX downloads without errors
- [ ] PDF generates (when WeasyPrint available)
- [ ] Auto-save works every 5 seconds
- [ ] Import from JSON restores all data
- [ ] Progress tracking updates correctly
- [ ] Preview matches final document
- [ ] QR codes generate and embed correctly
- [ ] Page numbers appear in correct position
- [ ] All 4 page sizes work
- [ ] Subject templates apply correctly
- [ ] Dynamic concept add/delete works
- [ ] Markdown formatting renders correctly

---

This prompt provides complete specifications to rebuild the Guide Book Generator application with full feature parity.
