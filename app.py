"""
Guide Book Generator - Main Application
CBSE Class 9 & 10 Study Guide Generator

A Streamlit application for creating professionally formatted
study guide chapters with DOCX and PDF export.
"""

import streamlit as st
from pathlib import Path
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Guide Book Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from config.constants import APP_NAME, APP_VERSION, AUTOSAVE_DIR
from config.subjects import load_chapters, get_subject_config, SUBJECT_CONFIGS
from core.models.base import ChapterData, ConceptItem, PYQItem, ModelAnswer, QuestionItem
from core.models.parts import PartManager
from core.session import SessionManager
from core.progress import ProgressTracker
from styles.theme import Colors, Weightage, Importance, PYQFrequency
from ui.components.preview import PreviewRenderer, show_preview_panel, show_generate_docx_button
from ui.components.navigation import (
    inject_custom_css, render_breadcrumb, render_next_prev_buttons,
    PAGE_INFO, WORKFLOW_ORDER
)

# File upload security constants
ALLOWED_EXTENSIONS = {'json', 'docx', 'pdf'}
MAX_FILE_SIZE_MB = 10


def validate_uploaded_file(uploaded_file):
    """
    Validate uploaded file for security.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if uploaded_file is None:
        return False, "No file uploaded"

    # Check file extension
    filename = uploaded_file.name
    if '.' not in filename:
        return False, "File must have an extension"

    extension = filename.rsplit('.', 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type '.{extension}'. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"

    # Check file size
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if uploaded_file.size > max_size_bytes:
        return False, f"File size ({uploaded_file.size / (1024*1024):.1f}MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)"

    return True, None


def init_session():
    """Initialize session state."""
    SessionManager.initialize()

    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = 'home'


def render_sidebar():
    """Render the sidebar with navigation and progress."""
    with st.sidebar:
        # Title with unsaved indicator
        is_dirty = SessionManager.is_dirty()
        if is_dirty:
            st.markdown(
                f'<h1 style="font-size: 1.5rem;">📚 Guide Book Generator '
                f'<span style="display: inline-block; width: 10px; height: 10px; '
                f'background-color: #EF4444; border-radius: 50%; margin-left: 8px;" '
                f'title="Unsaved changes"></span></h1>',
                unsafe_allow_html=True
            )
        else:
            st.title("📚 Guide Book Generator")
        st.caption(f"v{APP_VERSION}")

        st.divider()

        # Current chapter info
        data = SessionManager.get_chapter_data()
        if data:
            st.subheader("📖 Current Chapter")
            st.write(f"**Class {data.class_num}** | {data.subject.replace('_', ' ').title()}")
            st.write(f"**Ch {data.chapter_number}:** {data.chapter_title[:30]}...")

            # Progress
            part_manager = SessionManager.get_part_manager()
            tracker = ProgressTracker(data, part_manager)
            progress = tracker.get_overall_progress()

            st.progress(progress / 100)
            st.caption(f"Overall: {progress:.0f}% complete")

            st.divider()

            # Section progress
            st.subheader("📊 Section Progress")
            for name, status, pct in tracker.get_sidebar_display():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{status} {name}")
                with col2:
                    st.caption(f"{pct:.0f}%")

            st.divider()

        # Navigation with progress indicators
        st.subheader("🧭 Navigation")

        # Get progress data for badges
        progress_map = {}
        if data:
            progress_map = {
                'cover': tracker.calculate_cover_progress(),
                'part_a': tracker.calculate_part_a_progress(),
                'part_b': tracker.calculate_part_b_progress(),
                'part_c': tracker.calculate_part_c_progress(),
                'part_d': tracker.calculate_part_d_progress(),
                'part_e': tracker.calculate_part_e_progress(),
                'part_f': tracker.calculate_part_f_progress(),
                'part_g': tracker.calculate_part_g_progress(),
            }

        pages = [
            ("🏠 Home", "home"),
            ("📥 Import/Export", "import_export"),
            ("📄 Cover Page", "cover"),
            ("📊 Part A: PYQ", "part_a"),
            ("📖 Part B: Concepts", "part_b"),
            ("✅ Part C: Answers", "part_c"),
            ("📝 Part D: Practice", "part_d"),
            ("🗺️ Part E: Map Work", "part_e"),
            ("🔄 Part F: Revision", "part_f"),
            ("🎯 Part G: Strategy", "part_g"),
            ("⚙️ Generate", "generate"),
        ]

        current_page = st.session_state.get('current_page', 'home')

        for label, page_id in pages:
            # Add progress badge for applicable pages
            progress = progress_map.get(page_id, None)
            if progress is not None:
                if progress >= 80:
                    badge = "✅"
                elif progress >= 1:
                    badge = "🔶"
                else:
                    badge = "⬜"
                display_label = f"{badge} {label.split(' ', 1)[1] if ' ' in label else label}"
            else:
                display_label = label

            # Highlight current page
            button_type = "primary" if page_id == current_page else "secondary"
            if st.button(display_label, key=f"nav_{page_id}", use_container_width=True,
                        type=button_type):
                st.session_state.current_page = page_id
                st.rerun()

        st.divider()

        # Quick actions
        if data:
            st.subheader("⚡ Quick Actions")

            # Show save status
            last_save = SessionManager.get_last_save_time()
            if is_dirty:
                st.markdown(
                    '<p style="color: #EF4444; font-size: 12px; margin-bottom: 8px;">'
                    '● Unsaved changes</p>',
                    unsafe_allow_html=True
                )
            elif last_save:
                st.markdown(
                    f'<p style="color: #10B981; font-size: 12px; margin-bottom: 8px;">'
                    f'✓ Saved {last_save.strftime("%H:%M")}</p>',
                    unsafe_allow_html=True
                )

            save_label = "💾 Save Now" if not is_dirty else "💾 Save Now*"
            if st.button(save_label, use_container_width=True, type="primary" if is_dirty else "secondary"):
                save_chapter()
                st.success("Saved!")
                st.rerun()

            if st.button("🔄 Reset Chapter", use_container_width=True):
                if st.session_state.get('confirm_reset'):
                    SessionManager.reset()
                    st.session_state.confirm_reset = False
                    st.rerun()
                else:
                    st.session_state.confirm_reset = True
                    st.warning("Click again to confirm reset")

        st.divider()

        # Page Setup
        st.subheader("📄 Page Setup")

        page_size = st.selectbox(
            "Page Size",
            ["A4", "A5", "Letter", "Legal", "A3"],
            index=["A4", "A5", "Letter", "Legal", "A3"].index(
                st.session_state.get('preview_page_size', 'A4')
            ),
            key="sidebar_page_size"
        )
        st.session_state['preview_page_size'] = page_size

        orientation = st.selectbox(
            "Orientation",
            ["Portrait", "Landscape"],
            index=["Portrait", "Landscape"].index(
                st.session_state.get('preview_orientation', 'Portrait')
            ),
            key="sidebar_orientation"
        )
        st.session_state['preview_orientation'] = orientation

        add_page_numbers = st.checkbox(
            "Add Page Numbers",
            value=st.session_state.get('preview_add_page_numbers', True),
            key="sidebar_add_page_numbers"
        )
        st.session_state['preview_add_page_numbers'] = add_page_numbers

        if add_page_numbers:
            page_number_position = st.selectbox(
                "Page Number Position",
                ["Bottom Center", "Bottom Left", "Bottom Right"],
                index=["Bottom Center", "Bottom Left", "Bottom Right"].index(
                    st.session_state.get('preview_page_number_position', 'Bottom Center')
                ),
                key="sidebar_page_number_position"
            )
            st.session_state['preview_page_number_position'] = page_number_position
        else:
            page_number_position = st.session_state.get('preview_page_number_position', 'Bottom Center')

        # Sync page settings to ChapterData if data exists
        if data:
            data.page_size = page_size
            data.add_page_numbers = add_page_numbers
            data.page_number_position = page_number_position


def render_home_page():
    """Render the home page with chapter selection."""
    st.title("📚 Guide Book Generator")
    st.write("Create professional CBSE Class 9 & 10 study guides")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Create New Chapter")

        # Class selection
        class_num = st.selectbox("Select Class", [10, 9], key="new_class")

        # Subject selection
        subjects = ['history', 'geography', 'political_science', 'economics']
        subject_names = [s.replace('_', ' ').title() for s in subjects]
        subject_idx = st.selectbox("Select Subject", range(len(subjects)),
                                   format_func=lambda x: subject_names[x], key="new_subject")
        subject = subjects[subject_idx]

        # Chapter selection
        chapters = load_chapters(class_num, subject)

        if chapters:
            chapter_options = [f"Ch {c['number']}: {c['title']}" for c in chapters]
            chapter_options.append("✨ Custom Chapter")
            chapter_idx = st.selectbox("Select Chapter", range(len(chapter_options)),
                                       format_func=lambda x: chapter_options[x], key="new_chapter")

            if chapter_idx < len(chapters):
                selected_chapter = chapters[chapter_idx]
                chapter_num = selected_chapter['number']
                chapter_title = selected_chapter['title']
            else:
                # Custom chapter
                chapter_num = st.number_input("Chapter Number", min_value=1, max_value=50, value=1)
                chapter_title = st.text_input("Chapter Title", placeholder="Enter chapter title")
        else:
            chapter_num = st.number_input("Chapter Number", min_value=1, max_value=50, value=1)
            chapter_title = st.text_input("Chapter Title", placeholder="Enter chapter title")

        if st.button("🚀 Create Chapter", type="primary", use_container_width=True):
            if chapter_title:
                # Create new chapter
                data = SessionManager.create_new_chapter(
                    class_num=class_num,
                    subject=subject,
                    chapter_number=chapter_num,
                    chapter_title=chapter_title
                )

                # Set default values from chapter config
                if chapters and chapter_idx < len(chapters):
                    ch = chapters[chapter_idx]
                    data.weightage = ch.get('weightage', '4-5 Marks')
                    data.importance = ch.get('importance', 'High')
                    data.pyq_frequency = ch.get('pyq_frequency', 'Every Year')
                    data.map_work = 'Yes' if ch.get('has_map_work', False) else 'No'

                SessionManager.set_chapter_data(data)
                st.session_state.current_page = 'cover'
                st.success(f"Created: {chapter_title}")
                st.rerun()
            else:
                st.error("Please enter a chapter title")

    with col2:
        st.subheader("📂 Recent Chapters")

        # List autosaved files
        autosave_files = list(AUTOSAVE_DIR.glob("*.json"))
        autosave_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        if autosave_files:
            for f in autosave_files[:5]:
                with st.container():
                    try:
                        with open(f, 'r', encoding='utf-8') as file:
                            saved_data = json.load(file)
                            ch_data = saved_data.get('chapter_data', {})
                            title = ch_data.get('chapter_title', 'Untitled')[:30]
                            subject = ch_data.get('subject', 'unknown').replace('_', ' ').title()
                            class_n = ch_data.get('class_num', 10)

                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.write(f"**{title}**")
                                st.caption(f"Class {class_n} | {subject}")
                            with col_b:
                                if st.button("Load", key=f"load_{f.name}"):
                                    with open(f, 'r', encoding='utf-8') as file:
                                        SessionManager.import_from_json(file.read())
                                    st.session_state.current_page = 'cover'
                                    st.rerun()
                    except (json.JSONDecodeError, KeyError, OSError):
                        # Skip corrupted or invalid autosave files
                        continue
                st.divider()
        else:
            st.info("No recent chapters found. Create a new one to get started!")


def render_cover_page():
    """Render the cover page editor."""
    st.title("📄 Cover Page")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Chapter Title Section
    st.subheader("📝 Chapter Information")

    col1, col2 = st.columns(2)

    with col1:
        new_title = st.text_input("Chapter Title", value=data.chapter_title, key="ch_title")
        if new_title != data.chapter_title:
            data.chapter_title = new_title

        new_subtitle = st.text_input("Subtitle (optional)", value=data.subtitle or "", key="ch_subtitle")
        data.subtitle = new_subtitle if new_subtitle else None

    with col2:
        new_num = st.number_input("Chapter Number", min_value=1, max_value=50,
                                  value=data.chapter_number, key="ch_num")
        data.chapter_number = new_num

    st.divider()

    # Metadata Section
    st.subheader("📊 Chapter Metadata")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        weightage_options = Weightage.OPTIONS + ["Custom"]
        # Check if current value is custom
        is_custom = data.weightage not in Weightage.OPTIONS
        if is_custom:
            weightage_idx = len(weightage_options) - 1  # Select "Custom"
        else:
            weightage_idx = Weightage.OPTIONS.index(data.weightage)

        selected_weightage = st.selectbox("Weightage", weightage_options, index=weightage_idx, key="ch_weightage")

        if selected_weightage == "Custom":
            custom_weightage = st.text_input(
                "Enter marks",
                value=data.weightage if is_custom else "",
                placeholder="e.g., 8-10 Marks",
                key="ch_weightage_custom"
            )
            data.weightage = custom_weightage if custom_weightage else "4-5 Marks"
        else:
            data.weightage = selected_weightage

    with col2:
        map_work_options = ["Yes", "No"]
        map_idx = 0 if data.map_work == "Yes" else 1
        new_map = st.selectbox("Map Work", map_work_options, index=map_idx, key="ch_map")
        data.map_work = new_map

    with col3:
        importance_options = Importance.OPTIONS
        imp_idx = importance_options.index(data.importance) if data.importance in importance_options else 0
        new_importance = st.selectbox("Importance", importance_options, index=imp_idx, key="ch_importance")
        data.importance = new_importance

    with col4:
        freq_options = PYQFrequency.OPTIONS
        freq_idx = freq_options.index(data.pyq_frequency) if data.pyq_frequency in freq_options else 0
        new_freq = st.selectbox("PYQ Frequency", freq_options, index=freq_idx, key="ch_freq")
        data.pyq_frequency = new_freq

    st.divider()

    # Syllabus Alert
    st.subheader("⚠️ Syllabus Alert")

    alert_enabled = st.checkbox("Enable Syllabus Alert", value=data.syllabus_alert_enabled, key="alert_enabled")
    data.syllabus_alert_enabled = alert_enabled

    if alert_enabled:
        alert_text = st.text_area("Alert Text", value=data.syllabus_alert_text,
                                  placeholder="Enter syllabus alert message...", key="alert_text")
        data.syllabus_alert_text = alert_text

    st.divider()

    # Learning Objectives
    st.subheader("🎯 Learning Objectives")
    st.caption("Enter each objective on a new line. They will be displayed as bullet points.")

    objectives = st.text_area("Learning Objectives", value=data.learning_objectives,
                             height=200, placeholder="After studying this chapter, you will be able to:\n- Understand...\n- Analyse...\n- Explain...",
                             key="objectives")
    data.learning_objectives = objectives

    word_count = len(objectives.split()) if objectives else 0
    st.caption(f"Word count: {word_count}")

    st.divider()

    # Part Descriptions
    with st.expander("📑 Part Descriptions (for Chapter Contents box)"):
        for part_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            desc = st.text_input(f"Part {part_id} Description",
                                value=data.part_descriptions.get(part_id, ''),
                                key=f"part_desc_{part_id}")
            data.part_descriptions[part_id] = desc

    st.divider()

    # QR Codes Section
    st.subheader("📱 QR Codes for Downloadable Resources")
    st.caption("Enter URLs for PDF files. QR codes will be generated and shown below the Chapter Contents box.")

    col1, col2 = st.columns(2)

    with col1:
        qr_url_1 = st.text_input(
            "Practice Questions PDF URL",
            value=data.qr_practice_questions_url or "",
            placeholder="https://drive.google.com/...",
            key="qr_practice_url"
        )
        data.qr_practice_questions_url = qr_url_1 if qr_url_1 else None

    with col2:
        qr_url_2 = st.text_input(
            "Practice Questions with Answers PDF URL",
            value=data.qr_practice_with_answers_url or "",
            placeholder="https://drive.google.com/...",
            key="qr_answers_url"
        )
        data.qr_practice_with_answers_url = qr_url_2 if qr_url_2 else None

    # Show QR code preview if URLs are provided
    if data.qr_practice_questions_url or data.qr_practice_with_answers_url:
        st.caption("QR Code Preview:")
        qr_col1, qr_col2 = st.columns(2)

        with qr_col1:
            if data.qr_practice_questions_url:
                try:
                    import qrcode
                    from io import BytesIO
                    qr = qrcode.QRCode(version=1, box_size=5, border=2)
                    qr.add_data(data.qr_practice_questions_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buf = BytesIO()
                    img.save(buf, format='PNG')
                    st.image(buf.getvalue(), caption="Practice Questions", width=150)
                except Exception as e:
                    st.error(f"QR Error: {e}")

        with qr_col2:
            if data.qr_practice_with_answers_url:
                try:
                    import qrcode
                    from io import BytesIO
                    qr = qrcode.QRCode(version=1, box_size=5, border=2)
                    qr.add_data(data.qr_practice_with_answers_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buf = BytesIO()
                    img.save(buf, format='PNG')
                    st.image(buf.getvalue(), caption="With Answers", width=150)
                except Exception as e:
                    st.error(f"QR Error: {e}")

    # Save data
    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data)

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='cover')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('cover')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_a():
    """Render Part A: PYQ Analysis editor."""
    st.title("📊 Part A: PYQ Analysis")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Year Range
    col1, col2 = st.columns(2)
    with col1:
        year_range = st.text_input("Year Range", value=data.pyq_year_range, key="pyq_year_range")
        data.pyq_year_range = year_range

    st.divider()

    # PYQ Items
    st.subheader("📋 Previous Year Questions")
    st.caption("Format: Question | Marks (e.g., 3M or 5M) | Years (comma-separated)")

    # Add new PYQ
    with st.expander("➕ Add New PYQ"):
        new_q = st.text_area("Question", key="new_pyq_q")
        col1, col2 = st.columns(2)
        with col1:
            new_marks = st.selectbox("Marks", ["1M", "2M", "3M", "4M", "5M"], index=2, key="new_pyq_marks")
        with col2:
            new_years = st.text_input("Years Asked (comma-separated)", key="new_pyq_years",
                                      placeholder="2020, 2021, 2023")

        if st.button("Add PYQ", key="add_pyq"):
            if new_q:
                data.pyq_items.append(PYQItem(
                    question=new_q,
                    marks=new_marks,
                    years=new_years
                ))
                st.success("Added!")
                st.rerun()

    # Display existing PYQs
    for idx, item in enumerate(data.pyq_items):
        with st.container():
            col1, col2, col3, col4 = st.columns([4, 1, 2, 1])

            with col1:
                q = st.text_area(f"Question {idx+1}", value=item.question,
                                key=f"pyq_q_{idx}", height=80)
                item.question = q

            with col2:
                m = st.selectbox("Marks", ["1M", "2M", "3M", "4M", "5M"],
                                index=["1M", "2M", "3M", "4M", "5M"].index(item.marks) if item.marks in ["1M", "2M", "3M", "4M", "5M"] else 2,
                                key=f"pyq_m_{idx}")
                item.marks = m

            with col3:
                y = st.text_input("Years", value=item.years, key=f"pyq_y_{idx}")
                item.years = y

            with col4:
                if st.button("🗑️", key=f"del_pyq_{idx}"):
                    data.pyq_items.pop(idx)
                    st.rerun()

            st.divider()

    # Prediction
    st.subheader("🎯 Prediction")
    prediction = st.text_area("Prediction for next exam", value=data.pyq_prediction,
                             placeholder="German Unification (5M) + French Revolution (3M) + ...",
                             key="pyq_prediction")
    data.pyq_prediction = prediction

    # Syllabus Note
    st.subheader("📌 Syllabus Note")
    syllabus_note = st.text_area("Syllabus Note (optional)", value=data.pyq_syllabus_note or "",
                                placeholder="This chapter has remained unchanged since...",
                                key="pyq_syllabus_note")
    data.pyq_syllabus_note = syllabus_note if syllabus_note else None

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='A')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='A')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_a')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_b():
    """Render Part B: Key Concepts editor."""
    st.title("📖 Part B: Key Concepts")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Add new concept
    if st.button("➕ Add New Concept", type="primary"):
        new_num = len(data.concepts) + 1
        data.concepts.append(ConceptItem(number=new_num))
        st.rerun()

    st.divider()

    # Display concepts
    for idx, concept in enumerate(data.concepts):
        with st.expander(f"📌 Concept {concept.number}: {concept.title or 'Untitled'}", expanded=idx == 0):
            col1, col2 = st.columns([4, 1])

            with col1:
                title = st.text_input("Title", value=concept.title, key=f"concept_title_{idx}",
                                     placeholder="e.g., The French Revolution")
                concept.title = title

            with col2:
                if st.button("🗑️ Delete", key=f"del_concept_{idx}"):
                    data.concepts.pop(idx)
                    # Renumber
                    for i, c in enumerate(data.concepts):
                        c.number = i + 1
                    st.rerun()

            # NCERT Line
            ncert = st.text_input("NCERT Exact Line (optional)", value=concept.ncert_line or "",
                                 key=f"concept_ncert_{idx}",
                                 placeholder="The first clear expression of nationalism came with...")
            concept.ncert_line = ncert if ncert else None

            # Content
            content = st.text_area("Content", value=concept.content, height=200,
                                  key=f"concept_content_{idx}",
                                  placeholder="Main content with **bold**, *italic*, and bullet points (-)")
            concept.content = content

            col1, col2 = st.columns(2)

            with col1:
                # Memory Trick
                trick = st.text_input("Memory Trick (optional)", value=concept.memory_trick or "",
                                     key=f"concept_trick_{idx}",
                                     placeholder="FLAT-CUN — Flag, Language, Assembly...")
                concept.memory_trick = trick if trick else None

            with col2:
                # Did You Know
                dyk = st.text_area("Did You Know? (optional)", value=concept.did_you_know or "",
                                  height=100, key=f"concept_dyk_{idx}",
                                  placeholder="Interesting fact...")
                concept.did_you_know = dyk if dyk else None

            st.caption(f"Word count: {concept.word_count()}")

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='B')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='B')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_b')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_c():
    """Render Part C: Model Answers editor."""
    st.title("✅ Part C: Model Answers")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Add new answer
    if st.button("➕ Add New Model Answer", type="primary"):
        data.model_answers.append(ModelAnswer())
        st.rerun()

    st.divider()

    for idx, answer in enumerate(data.model_answers):
        with st.expander(f"Q{idx+1}: {answer.question[:50] or 'New Question'}...", expanded=idx == 0):
            col1, col2 = st.columns([5, 1])

            with col1:
                q = st.text_area("Question", value=answer.question, key=f"ans_q_{idx}")
                answer.question = q

            with col2:
                m = st.number_input("Marks", min_value=1, max_value=10,
                                   value=answer.marks, key=f"ans_m_{idx}")
                answer.marks = m

                if st.button("🗑️", key=f"del_ans_{idx}"):
                    data.model_answers.pop(idx)
                    st.rerun()

            # Answer
            ans = st.text_area("Answer (use **bold** for keywords)", value=answer.answer,
                              height=200, key=f"ans_a_{idx}")
            answer.answer = ans

            # Marking points
            st.caption("Marking Points (one per line, each worth 1 mark)")
            points_text = "\n".join(answer.marking_points) if answer.marking_points else ""
            points = st.text_area("Marking Points", value=points_text, height=150,
                                 key=f"ans_points_{idx}")
            answer.marking_points = [p.strip() for p in points.split("\n") if p.strip()]

    # Examiner Tips
    st.divider()
    st.subheader("📋 Examiner's Marking Scheme Tips")
    tips = st.text_area("Examiner Tips", value=data.examiner_tips or "",
                       placeholder="- 3-mark questions: 3 distinct points...",
                       key="examiner_tips")
    data.examiner_tips = tips if tips else None

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='C')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='C')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_c')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_d():
    """Render Part D: Practice Questions editor."""
    st.title("📝 Part D: Practice Questions")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    tabs = st.tabs(["MCQs", "Assertion-Reason", "Short Answer", "Long Answer", "HOTS"])

    with tabs[0]:
        render_mcq_editor(data)

    with tabs[1]:
        render_ar_editor(data)

    with tabs[2]:
        render_question_list_editor(data.short_answer, "Short Answer (3M)", "sa")

    with tabs[3]:
        render_question_list_editor(data.long_answer, "Long Answer (5M)", "la")

    with tabs[4]:
        render_question_list_editor(data.hots, "HOTS", "hots")

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='D')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='D')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_d')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_mcq_editor(data):
    """Render MCQ editor."""
    st.subheader("Multiple Choice Questions")

    if st.button("➕ Add MCQ", key="add_mcq"):
        data.mcqs.append(QuestionItem(
            marks=1,
            difficulty='M',
            options=['', '', '', ''],
            answer='a'
        ))
        st.rerun()

    for idx, mcq in enumerate(data.mcqs):
        with st.expander(f"MCQ {idx+1}: {mcq.question[:40] or 'New'}...", expanded=idx == 0):
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                q = st.text_input("Question", value=mcq.question, key=f"mcq_q_{idx}")
                mcq.question = q

            with col2:
                d = st.selectbox("Difficulty", ["E", "M", "H"],
                                index=["E", "M", "H"].index(mcq.difficulty) if mcq.difficulty in ["E", "M", "H"] else 1,
                                key=f"mcq_d_{idx}")
                mcq.difficulty = d

            with col3:
                if st.button("🗑️", key=f"del_mcq_{idx}"):
                    data.mcqs.pop(idx)
                    st.rerun()

            # Options
            cols = st.columns(2)
            options = mcq.options or ['', '', '', '']
            for i in range(4):
                with cols[i % 2]:
                    opt = st.text_input(f"({chr(97+i)})", value=options[i] if i < len(options) else "",
                                       key=f"mcq_opt_{idx}_{i}")
                    if len(options) > i:
                        options[i] = opt
            mcq.options = options

            # Answer
            ans = st.selectbox("Correct Answer", ['a', 'b', 'c', 'd'],
                              index=['a', 'b', 'c', 'd'].index(mcq.answer) if mcq.answer in ['a', 'b', 'c', 'd'] else 0,
                              key=f"mcq_ans_{idx}")
            mcq.answer = ans


def render_ar_editor(data):
    """Render Assertion-Reason editor."""
    st.subheader("Assertion-Reason Questions")

    if st.button("➕ Add A-R", key="add_ar"):
        data.assertion_reason.append(QuestionItem(
            marks=1,
            difficulty='M',
            answer='a'
        ))
        st.rerun()

    for idx, ar in enumerate(data.assertion_reason):
        with st.expander(f"A-R {idx+1}", expanded=idx == 0):
            col1, col2 = st.columns([5, 1])

            with col1:
                q = st.text_area("Assertion and Reason",
                                value=ar.question,
                                placeholder="Assertion: ...\nReason: ...",
                                key=f"ar_q_{idx}", height=100)
                ar.question = q

            with col2:
                if st.button("🗑️", key=f"del_ar_{idx}"):
                    data.assertion_reason.pop(idx)
                    st.rerun()

            ans = st.selectbox("Answer", ['a', 'b', 'c', 'd'],
                              index=['a', 'b', 'c', 'd'].index(ar.answer) if ar.answer in ['a', 'b', 'c', 'd'] else 0,
                              key=f"ar_ans_{idx}")
            ar.answer = ans


def render_question_list_editor(questions, title, prefix):
    """Render a generic question list editor."""
    st.subheader(title)

    if st.button(f"➕ Add {title.split()[0]}", key=f"add_{prefix}"):
        questions.append(QuestionItem(marks=3 if 'Short' in title else 5))
        st.rerun()

    for idx, q in enumerate(questions):
        with st.expander(f"{idx+1}. {q.question[:40] or 'New'}...", expanded=idx == 0):
            col1, col2 = st.columns([5, 1])

            with col1:
                question = st.text_area("Question", value=q.question, key=f"{prefix}_q_{idx}")
                q.question = question

            with col2:
                if st.button("🗑️", key=f"del_{prefix}_{idx}"):
                    questions.pop(idx)
                    st.rerun()

            hint = st.text_input("Hint (optional)", value=q.hint or "", key=f"{prefix}_h_{idx}")
            q.hint = hint if hint else None


def render_part_e():
    """Render Part E: Map Work editor."""
    st.title("🗺️ Part E: Map Work")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # N/A toggle
    na = st.checkbox("N/A for this chapter", value=data.map_work_na, key="map_na")
    data.map_work_na = na

    if not na:
        st.divider()

        # Map items
        st.subheader("📍 Map Locations")
        st.caption("Enter each location on a new line")

        items_text = "\n".join(data.map_items) if data.map_items else ""
        items = st.text_area("Map Items", value=items_text, height=200,
                            placeholder="Location 1\nLocation 2\n...")
        data.map_items = [i.strip() for i in items.split("\n") if i.strip()]

        # Map tips
        st.subheader("💡 Map Marking Tips")
        tips = st.text_area("Tips", value=data.map_tips or "", height=100,
                           placeholder="Mark locations with ✓ and write names...")
        data.map_tips = tips if tips else None

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='E')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='E')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_e')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_f():
    """Render Part F: Quick Revision editor."""
    st.title("🔄 Part F: Quick Revision")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Key Points
    st.subheader("📝 Key Points Summary")
    st.caption("One point per line. Use **bold** for keywords.")

    points_text = "\n".join(data.revision_key_points) if data.revision_key_points else ""
    points = st.text_area("Key Points", value=points_text, height=200)
    data.revision_key_points = [p.strip() for p in points.split("\n") if p.strip()]

    st.divider()

    # Key Terms
    st.subheader("📖 Key Terms")

    if st.button("➕ Add Term", key="add_term"):
        data.revision_key_terms.append({'term': '', 'definition': ''})
        st.rerun()

    for idx, item in enumerate(data.revision_key_terms):
        col1, col2, col3 = st.columns([2, 4, 1])

        with col1:
            term = st.text_input("Term", value=item.get('term', ''), key=f"term_{idx}")
            item['term'] = term

        with col2:
            definition = st.text_input("Definition", value=item.get('definition', ''), key=f"def_{idx}")
            item['definition'] = definition

        with col3:
            if st.button("🗑️", key=f"del_term_{idx}"):
                data.revision_key_terms.pop(idx)
                st.rerun()

    st.divider()

    # Memory Tricks
    st.subheader("🧠 Memory Tricks Compilation")
    tricks_text = "\n".join(data.revision_memory_tricks) if data.revision_memory_tricks else ""
    tricks = st.text_area("Memory Tricks", value=tricks_text, height=150)
    data.revision_memory_tricks = [t.strip() for t in tricks.split("\n") if t.strip()]

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='F')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='F')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_f')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_part_g():
    """Render Part G: Exam Strategy editor."""
    st.title("🎯 Part G: Exam Strategy")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    # Time Allocation
    st.subheader("⏱️ Time Allocation")

    if st.button("➕ Add Row", key="add_time"):
        data.time_allocation.append({'type': '', 'marks': '', 'time': ''})
        st.rerun()

    for idx, item in enumerate(data.time_allocation):
        col1, col2, col3, col4 = st.columns([3, 1, 2, 1])

        with col1:
            t = st.text_input("Question Type", value=item.get('type', ''), key=f"time_type_{idx}")
            item['type'] = t

        with col2:
            m = st.text_input("Marks", value=item.get('marks', ''), key=f"time_marks_{idx}")
            item['marks'] = m

        with col3:
            time = st.text_input("Time", value=item.get('time', ''), key=f"time_time_{idx}")
            item['time'] = time

        with col4:
            if st.button("🗑️", key=f"del_time_{idx}"):
                data.time_allocation.pop(idx)
                st.rerun()

    st.divider()

    # Common Mistakes
    st.subheader("❌ What Loses Marks")

    if st.button("➕ Add Mistake", key="add_mistake"):
        data.common_mistakes_exam.append({'mistake': '', 'correction': ''})
        st.rerun()

    for idx, item in enumerate(data.common_mistakes_exam):
        col1, col2, col3 = st.columns([3, 3, 1])

        with col1:
            m = st.text_input("Mistake", value=item.get('mistake', ''), key=f"mistake_{idx}")
            item['mistake'] = m

        with col2:
            c = st.text_input("What to do instead", value=item.get('correction', ''), key=f"correction_{idx}")
            item['correction'] = c

        with col3:
            if st.button("🗑️", key=f"del_mistake_{idx}"):
                data.common_mistakes_exam.pop(idx)
                st.rerun()

    st.divider()

    # Pro Tips
    st.subheader("✅ Examiner's Pro Tips")
    tips_text = "\n".join(data.examiner_pro_tips) if data.examiner_pro_tips else ""
    tips = st.text_area("Pro Tips (one per line)", value=tips_text, height=150)
    data.examiner_pro_tips = [t.strip() for t in tips.split("\n") if t.strip()]

    st.divider()

    # Self-Assessment
    st.subheader("☑️ Self-Assessment Checklist")
    checklist_text = "\n".join(data.self_assessment_checklist) if data.self_assessment_checklist else ""
    checklist = st.text_area("Checklist Items (one per line)", value=checklist_text, height=150)
    data.self_assessment_checklist = [c.strip() for c in checklist.split("\n") if c.strip()]

    SessionManager.set_chapter_data(data)

    # Preview panel
    st.divider()
    show_preview_panel(data, part_id='G')

    # Generate DOCX button
    st.divider()
    show_generate_docx_button(data, SessionManager.get_part_manager(), part_id='G')

    # Next/Previous navigation
    st.divider()
    new_page = render_next_prev_buttons('part_g')
    if new_page:
        st.session_state.current_page = new_page
        st.rerun()


def render_generate_page():
    """Render the document generation page."""
    st.title("⚙️ Generate Document")

    data = SessionManager.get_chapter_data()
    if not data:
        st.warning("Please create or load a chapter first.")
        return

    part_manager = SessionManager.get_part_manager()

    # Validation
    st.subheader("✅ Validation")

    warnings = []
    if not data.chapter_title:
        warnings.append("Chapter title is missing")
    if not data.learning_objectives:
        warnings.append("Learning objectives are empty")
    if not data.concepts or all(c.is_empty() for c in data.concepts):
        warnings.append("No concepts added")

    if warnings:
        for w in warnings:
            st.warning(f"⚠️ {w}")
    else:
        st.success("✅ All required fields are filled!")

    st.divider()

    # Page Settings
    st.subheader("📄 Page Settings")

    col1, col2, col3 = st.columns(3)

    with col1:
        page_size = st.selectbox("Page Size", ["A4", "A5", "Letter", "Legal"],
                                index=["A4", "A5", "Letter", "Legal"].index(data.page_size),
                                key="page_size")
        data.page_size = page_size

    with col2:
        add_numbers = st.checkbox("Add Page Numbers", value=data.add_page_numbers, key="page_numbers")
        data.add_page_numbers = add_numbers

    with col3:
        position = st.selectbox("Page Number Position",
                               ["Bottom Center", "Bottom Right", "Bottom Left"],
                               key="page_position")
        data.page_number_position = position

    st.divider()

    # Parts Manager
    st.subheader("📑 Parts to Include")

    parts = part_manager.get_all_parts()

    # Display parts in a table-like format
    for part in parts:
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 0.5])

        with col1:
            enabled = st.checkbox(
                "",
                value=part.enabled,
                key=f"part_enable_{part.id}",
                label_visibility="collapsed"
            )
            if enabled != part.enabled:
                if enabled:
                    part_manager.enable_part(part.id)
                else:
                    part_manager.disable_part(part.id)

        with col2:
            st.write(f"**Part {part.id}:** {part.name}")

        with col3:
            if not part.removable:
                st.caption("Required")
            else:
                st.caption("Optional")

        with col4:
            if part.removable and part.id not in ['A', 'B']:
                if st.button("🗑️", key=f"remove_part_{part.id}", help=f"Remove Part {part.id}"):
                    part_manager.remove_part(part.id)
                    # Also remove from part_descriptions
                    if part.id in data.part_descriptions:
                        del data.part_descriptions[part.id]
                    st.rerun()

    # Add new part section
    st.divider()
    with st.expander("➕ Add Custom Part"):
        col1, col2 = st.columns([1, 2])

        with col1:
            # Get next available ID
            existing_ids = [p.id for p in parts]
            next_id = 'H'
            for letter in 'HIJKLMNOP':
                if letter not in existing_ids:
                    next_id = letter
                    break

            new_part_id = st.text_input("Part ID", value=next_id, max_chars=1, key="new_part_id")

        with col2:
            new_part_name = st.text_input("Part Name", placeholder="e.g., Case Studies", key="new_part_name")

        if st.button("Add Part", type="primary", key="add_new_part"):
            if new_part_name and new_part_id:
                if new_part_id.upper() in existing_ids:
                    st.error(f"Part {new_part_id.upper()} already exists!")
                else:
                    part_manager.add_custom_part(new_part_id.upper(), new_part_name)
                    data.part_descriptions[new_part_id.upper()] = new_part_name
                    st.success(f"Added Part {new_part_id.upper()}: {new_part_name}")
                    st.rerun()
            else:
                st.error("Please enter both Part ID and Name")

    st.divider()

    # Save button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("💾 Save Project", use_container_width=True):
            save_chapter()
            st.success("Project saved!")

    SessionManager.set_chapter_data(data)
    SessionManager.set_part_manager(part_manager)

    # PDF Preview & Download Section
    st.divider()
    from ui.components.preview import show_pdf_preview
    show_pdf_preview(data, part_manager)


def render_import_export():
    """Render import/export page."""
    st.title("📥 Import / Export")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Export")

        data = SessionManager.get_chapter_data()
        if data:
            # Export as JSON
            json_str = SessionManager.export_to_json()
            if json_str:
                filename = f"Ch{data.chapter_number}_{data.subject}_data.json"
                st.download_button(
                    label="⬇️ Export as JSON",
                    data=json_str,
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("No chapter loaded to export")

    with col2:
        st.subheader("📥 Import")

        # Accept JSON, DOCX, and PDF files
        uploaded = st.file_uploader(
            "Upload file",
            type=['json', 'docx', 'pdf'],
            help="Import from JSON (full data), DOCX, or PDF (extracts basic info)"
        )

        if uploaded:
            # Validate file before processing
            is_valid, error_msg = validate_uploaded_file(uploaded)
            if not is_valid:
                st.error(error_msg)
            else:
                file_type = uploaded.name.split('.')[-1].lower()

                if st.button("Import", type="primary"):
                    try:
                        if file_type == 'json':
                            # Existing JSON import
                            content = uploaded.read().decode('utf-8')
                            if SessionManager.import_from_json(content):
                                st.success("✅ Imported successfully from JSON!")
                                st.session_state.current_page = 'cover'
                                st.rerun()
                        else:
                            # DOCX or PDF import
                            from core.parsers import parse_document

                            file_bytes = uploaded.read()
                            chapter_data = parse_document(file_bytes, file_type)

                            if chapter_data:
                                SessionManager.set_chapter_data(chapter_data)
                                st.success(f"✅ Imported from {file_type.upper()}!")
                                st.info("Note: Only basic metadata extracted. Fill in remaining sections manually.")
                                st.session_state.current_page = 'cover'
                                st.rerun()
                            else:
                                st.error(f"Failed to parse {file_type.upper()} file")

                    except Exception as e:
                        st.error(f"Import error: {str(e)}")

        # Help text
        st.caption("""
        **Import formats:**
        - **JSON**: Full chapter data (recommended for backup/restore)
        - **DOCX/PDF**: Extracts chapter title, number, subject, metadata
        """)


def save_chapter():
    """Save current chapter to autosave directory."""
    data = SessionManager.get_chapter_data()
    if not data:
        return

    json_str = SessionManager.export_to_json()
    if json_str:
        filename = f"class_{data.class_num}_{data.subject}_ch{data.chapter_number:02d}.json"
        filepath = AUTOSAVE_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)

        SessionManager.mark_clean()


def main():
    """Main application entry point."""
    init_session()

    # Inject custom CSS for improved styling
    inject_custom_css()

    render_sidebar()

    # Route to correct page
    page = st.session_state.get('current_page', 'home')

    # Render breadcrumb navigation for non-home pages
    data = SessionManager.get_chapter_data()
    if page != 'home':
        render_breadcrumb(page, data.chapter_title if data else None)

    pages = {
        'home': render_home_page,
        'import_export': render_import_export,
        'cover': render_cover_page,
        'part_a': render_part_a,
        'part_b': render_part_b,
        'part_c': render_part_c,
        'part_d': render_part_d,
        'part_e': render_part_e,
        'part_f': render_part_f,
        'part_g': render_part_g,
        'generate': render_generate_page,
    }

    render_func = pages.get(page, render_home_page)
    render_func()


if __name__ == "__main__":
    main()
