"""
Guide Book Generator - Main Application
CBSE Class 9 & 10 Study Guide Generator

A Streamlit application for creating professionally formatted
study guide chapters with DOCX and PDF export.
"""

import json

import streamlit as st

# Configure page
st.set_page_config(
    page_title="Guide Book Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from config.constants import APP_VERSION, AUTOSAVE_DIR
from config.subjects import load_chapters, get_categories_with_subjects, get_subject_config, get_subject_display_name, get_subject_icon
from core.models.base import ConceptItem, ModelAnswer, PYQItem, QuestionItem
from core.progress import ProgressTracker
from core.session import SessionManager
from styles.theme import Importance, PYQFrequency, Weightage
from ui.components.navigation import inject_custom_css, render_breadcrumb, render_next_prev_buttons
from ui.components.preview import show_generate_docx_button, show_preview_panel
from ui.components.utils import render_markdown_toolbar, get_markdown_help_caption

# File upload security constants
ALLOWED_EXTENSIONS = {'json', 'docx', 'pdf', 'md', 'markdown'}
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
        
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 2rem; margin-right: 10px;">📚</div>
                <div>
                    <h1 style="font-size: 1.2rem; margin: 0; padding: 0;">Guide Book</h1>
                    <div style="font-size: 0.8rem; color: #6B7280;">Generator v{APP_VERSION}</div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Quick Actions (Top for easy access)
        if SessionManager.get_chapter_data():
            col1, col2 = st.columns(2)
            with col1:
                # Save Button
                save_type = "primary" if is_dirty else "secondary"
                save_label = "💾 Save" if not is_dirty else "💾 Save*"
                if st.button(save_label, key="quick_save", type=save_type, use_container_width=True):
                    save_chapter()
                    st.toast("Project saved successfully!", icon="✅")
                    st.rerun()
            
            with col2:
                # Reset Button
                if st.button("🔄 Reset", key="quick_reset", use_container_width=True):
                    if st.session_state.get('confirm_reset'):
                        SessionManager.reset()
                        st.session_state.confirm_reset = False
                        st.rerun()
                    else:
                        st.session_state.confirm_reset = True
                        st.warning("Confirm?")

            # Status Text
            last_save = SessionManager.get_last_save_time()
            if is_dirty:
                st.markdown('<div class="status-unsaved">● Unsaved changes</div>', unsafe_allow_html=True)
            elif last_save:
                st.markdown(f'<div class="status-saved">✓ Saved {last_save.strftime("%H:%M")}</div>', unsafe_allow_html=True)
            
            st.divider()

        # Current chapter info
        data = SessionManager.get_chapter_data()
        if data:
            st.markdown(f"**Class {data.class_num}** | {get_subject_icon(data.subject)} {get_subject_display_name(data.subject)}")
            st.caption(f"Ch {data.chapter_number}: {data.chapter_title[:30] if data.chapter_title else 'Untitled'}")

            # Progress
            part_manager = SessionManager.get_part_manager()
            tracker = ProgressTracker(data, part_manager)
            progress = tracker.get_overall_progress()

            st.progress(progress / 100)
            
            # Compact section progress
            with st.expander("📊 Detailed Progress"):
                for name, status, pct in tracker.get_sidebar_display():
                    st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:0.85rem'><span>{status} {name}</span><span>{pct:.0f}%</span></div>", unsafe_allow_html=True)

            st.divider()

        # Navigation
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
            display_label = label
            
            # Highlight current page
            button_type = "primary" if page_id == current_page else "secondary"
            
            # Simple button for nav
            if st.button(display_label, key=f"nav_{page_id}", use_container_width=True, type=button_type):
                st.session_state.current_page = page_id
                st.rerun()

        st.divider()

        # Page Setup
        if data:
            with st.expander("📄 Page Setup"):
                page_size = st.selectbox(
                    "Size",
                    ["A4", "A5", "Letter", "Legal"],
                    index=["A4", "A5", "Letter", "Legal"].index(data.page_size),
                    key="sidebar_page_size"
                )
                data.page_size = page_size

                add_page_numbers = st.checkbox(
                    "Page Numbers",
                    value=data.add_page_numbers,
                    key="sidebar_add_page_numbers"
                )
                data.add_page_numbers = add_page_numbers


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

        # Subject Category selection
        categories = get_categories_with_subjects()
        category_names = list(categories.keys())
        category_display = [f"{categories[c]['icon']} {c}" for c in category_names]

        selected_cat_idx = st.selectbox(
            "Select Subject Category",
            range(len(category_names)),
            format_func=lambda x: category_display[x],
            key="new_category"
        )
        selected_category = category_names[selected_cat_idx]

        # Subject selection within category
        cat_subjects = categories[selected_category]['subjects']
        subject_display = [f"{s['icon']} {s['name']}" for s in cat_subjects]
        subject_idx = st.selectbox(
            "Select Subject",
            range(len(cat_subjects)),
            format_func=lambda x: subject_display[x],
            key="new_subject"
        )
        subject = cat_subjects[subject_idx]['id']

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
    with st.container(border=True):
        st.subheader("📝 Chapter Information")
        col1, col2 = st.columns([3, 1])

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

    # Metadata Section
    with st.container(border=True):
        st.subheader("📊 Chapter Metadata")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            weightage_options = Weightage.OPTIONS + ["Custom"]
            is_custom = data.weightage not in Weightage.OPTIONS
            weightage_idx = len(weightage_options) - 1 if is_custom else Weightage.OPTIONS.index(data.weightage)
            
            selected_weightage = st.selectbox("Weightage", weightage_options, index=weightage_idx, key="ch_weightage")

            if selected_weightage == "Custom":
                custom_weightage = st.text_input("Enter marks", value=data.weightage if is_custom else "", 
                                               placeholder="e.g., 8-10 Marks", key="ch_weightage_custom")
                data.weightage = custom_weightage if custom_weightage else "4-5 Marks"
            else:
                data.weightage = selected_weightage

        with col2:
            map_idx = 0 if data.map_work == "Yes" else 1
            new_map = st.selectbox("Map Work", ["Yes", "No"], index=map_idx, key="ch_map")
            data.map_work = new_map

        with col3:
            imp_idx = Importance.OPTIONS.index(data.importance) if data.importance in Importance.OPTIONS else 0
            new_importance = st.selectbox("Importance", Importance.OPTIONS, index=imp_idx, key="ch_importance")
            data.importance = new_importance

        with col4:
            freq_idx = PYQFrequency.OPTIONS.index(data.pyq_frequency) if data.pyq_frequency in PYQFrequency.OPTIONS else 0
            new_freq = st.selectbox("PYQ Frequency", PYQFrequency.OPTIONS, index=freq_idx, key="ch_freq")
            data.pyq_frequency = new_freq

    # Syllabus Alert
    with st.container(border=True):
        st.subheader("⚠️ Syllabus Alert")
        alert_enabled = st.checkbox("Enable Syllabus Alert", value=data.syllabus_alert_enabled, key="alert_enabled")
        data.syllabus_alert_enabled = alert_enabled

        if alert_enabled:
            alert_text = st.text_area("Alert Text", value=data.syllabus_alert_text,
                                      placeholder="Enter syllabus alert message...", key="alert_text")
            data.syllabus_alert_text = alert_text

    # Learning Objectives
    with st.container(border=True):
        st.subheader("🎯 Learning Objectives")
        st.caption("Enter each objective on a new line. They will be displayed as bullet points.")
        
        render_markdown_toolbar("objectives")
        objectives = st.text_area("Learning Objectives", value=data.learning_objectives,
                                 height=200, placeholder="After studying this chapter, you will be able to:\n- Understand...\n- Analyse...\n- Explain...",
                                 key="objectives", label_visibility="collapsed")
        data.learning_objectives = objectives
        st.caption(f"Word count: {len(objectives.split()) if objectives else 0}")

    # Part Descriptions
    with st.expander("📑 Part Descriptions (for Chapter Contents box)"):
        for part_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            desc = st.text_input(f"Part {part_id} Description",
                                value=data.part_descriptions.get(part_id, ''),
                                key=f"part_desc_{part_id}")
            data.part_descriptions[part_id] = desc

    # QR Codes Section
    with st.container(border=True):
        st.subheader("📱 QR Codes for Downloadable Resources")
        st.caption("Enter URLs for PDF files. QR codes will be generated and shown below the Chapter Contents box.")

        col1, col2 = st.columns(2)
        with col1:
            qr_url_1 = st.text_input("Practice Questions PDF URL", value=data.qr_practice_questions_url or "",
                                    placeholder="https://drive.google.com/...", key="qr_practice_url")
            data.qr_practice_questions_url = qr_url_1 if qr_url_1 else None

        with col2:
            qr_url_2 = st.text_input("Practice Questions with Answers PDF URL", value=data.qr_practice_with_answers_url or "",
                                    placeholder="https://drive.google.com/...", key="qr_answers_url")
            data.qr_practice_with_answers_url = qr_url_2 if qr_url_2 else None

        # QR Preview logic remains same...
        if data.qr_practice_questions_url or data.qr_practice_with_answers_url:
            st.divider()
            st.caption("QR Code Preview:")
            qr_col1, qr_col2 = st.columns(2)
            # ... (rendering code for QR remains)
            with qr_col1:
                if data.qr_practice_questions_url:
                    try:
                        from io import BytesIO
                        import qrcode
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
                        from io import BytesIO
                        import qrcode
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

    # Header with Add Button
    col_head, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ Add Concept", type="primary", use_container_width=True):
            new_num = len(data.concepts) + 1
            data.concepts.append(ConceptItem(number=new_num))
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Display concepts
    for idx, concept in enumerate(data.concepts):
        # Determine expander title
        expander_title = f"#{concept.number} {concept.title}" if concept.title else f"Concept #{concept.number}"
        
        with st.expander(expander_title, expanded=idx == 0):
            # Top row: Title and Delete
            col1, col2 = st.columns([5, 1])
            with col1:
                title = st.text_input("Concept Title", value=concept.title, key=f"concept_title_{idx}",
                                     placeholder="e.g., The French Revolution")
                concept.title = title
            with col2:
                if st.button("🗑️", key=f"del_concept_{idx}", help="Delete this concept"):
                    data.concepts.pop(idx)
                    # Renumber
                    for i, c in enumerate(data.concepts):
                        c.number = i + 1
                    st.rerun()

            # Tabs for different content types
            tab_main, tab_tables, tab_extras = st.tabs(["📝 Main Content", "📊 Tables", "✨ Extras"])

            # --- Main Content Tab ---
            with tab_main:
                # NCERT Line
                ncert = st.text_input("NCERT Exact Line (optional)", value=concept.ncert_line or "",
                                     key=f"concept_ncert_{idx}",
                                     placeholder="The first clear expression of nationalism came with...")
                concept.ncert_line = ncert if ncert else None

                # Content
                st.caption("Main explanation (supports markdown)")
                render_markdown_toolbar(f"concept_content_{idx}")
                content = st.text_area("Content", value=concept.content, height=200,
                                      key=f"concept_content_{idx}",
                                      label_visibility="collapsed",
                                      placeholder="Main content with **bold**, *italic*, and bullet points (-)")
                concept.content = content
                
                st.caption(f"Word count: {concept.word_count()}")

            # --- Tables Tab ---
            with tab_tables:
                st.info("Add comparison tables or data charts for this concept.")
                
                for tbl_idx, tbl in enumerate(concept.tables):
                    with st.container():
                        st.markdown(f"**Table {tbl_idx + 1}**")
                        tbl.title = st.text_input("Table Title", value=tbl.title,
                                                 key=f"tbl_title_{idx}_{tbl_idx}",
                                                 placeholder="e.g., Comparison of Events")

                        # Headers management
                        col_h_disp, col_h_act = st.columns([4, 1])
                        with col_h_disp:
                            st.caption(f"Columns: {len(tbl.headers)}")
                        with col_h_act:
                            col_btns = st.columns(2)
                            with col_btns[0]:
                                if st.button("➕", key=f"add_col_{idx}_{tbl_idx}", help="Add column"):
                                    tbl.headers.append(f"Col {len(tbl.headers)+1}")
                                    for row in tbl.rows:
                                        row.append("")
                                    st.rerun()
                            with col_btns[1]:
                                if len(tbl.headers) > 1 and st.button("➖", key=f"del_col_{idx}_{tbl_idx}", help="Remove last column"):
                                    tbl.headers.pop()
                                    for row in tbl.rows:
                                        if row: row.pop()
                                    st.rerun()
                        
                        # Headers Inputs
                        header_cols = st.columns(len(tbl.headers))
                        for h_idx, header in enumerate(tbl.headers):
                            with header_cols[h_idx]:
                                tbl.headers[h_idx] = st.text_input(f"H{h_idx+1}", value=header, 
                                                                 key=f"tbl_h_{idx}_{tbl_idx}_{h_idx}", 
                                                                 label_visibility="collapsed")

                        # Rows
                        st.markdown("Rows")
                        for r_idx, row in enumerate(tbl.rows):
                            row_cols = st.columns(len(tbl.headers) + 1)
                            for c_idx in range(len(tbl.headers)):
                                with row_cols[c_idx]:
                                    if c_idx < len(row):
                                        row[c_idx] = st.text_input(f"R{r_idx}C{c_idx}", value=row[c_idx],
                                                                  key=f"tbl_cell_{idx}_{tbl_idx}_{r_idx}_{c_idx}",
                                                                  label_visibility="collapsed")
                            with row_cols[-1]:
                                if st.button("🗑️", key=f"del_row_{idx}_{tbl_idx}_{r_idx}"):
                                    tbl.rows.pop(r_idx)
                                    st.rerun()

                        # Row Actions
                        btn_cols = st.columns([1, 4])
                        with btn_cols[0]:
                            if st.button("➕ Row", key=f"add_row_{idx}_{tbl_idx}"):
                                tbl.rows.append([""] * len(tbl.headers))
                                st.rerun()
                        with btn_cols[1]:
                            if st.button("Delete Table", key=f"del_tbl_{idx}_{tbl_idx}"):
                                concept.tables.pop(tbl_idx)
                                st.rerun()
                        
                        st.divider()

                if st.button("➕ Add Table", key=f"add_tbl_{idx}"):
                    from core.models.base import ConceptTable
                    concept.tables.append(ConceptTable())
                    st.rerun()

            # --- Extras Tab ---
            with tab_extras:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🧠 Memory Trick**")
                    trick = st.text_area("Mnemonic/Trick", value=concept.memory_trick or "",
                                         key=f"concept_trick_{idx}", height=100,
                                         placeholder="FLAT-CUN — Flag, Language, Assembly...")
                    concept.memory_trick = trick if trick else None

                with col2:
                    st.markdown("**💡 Did You Know?**")
                    dyk = st.text_area("Interesting Fact", value=concept.did_you_know or "",
                                      height=100, key=f"concept_dyk_{idx}",
                                      placeholder="Interesting fact...")
                    concept.did_you_know = dyk if dyk else None

                st.divider()
                st.markdown("**🎨 Custom Colored Boxes**")

                COLOR_OPTIONS = {
                    "Light Grey": "#F3F4F6", "Light Blue": "#DBEAFE", 
                    "Light Green": "#DCFCE7", "Light Yellow": "#FEF3C7",
                    "Light Purple": "#F3E8FF", "Light Pink": "#FEE2E2",
                }

                for box_idx, box in enumerate(concept.custom_boxes):
                    with st.container():
                        c1, c2, c3 = st.columns([3, 2, 1])
                        with c1:
                            box.title = st.text_input("Box Title", value=box.title,
                                                      key=f"box_title_{idx}_{box_idx}",
                                                      placeholder="e.g., Important Note")
                        with c2:
                            color_name = next((k for k, v in COLOR_OPTIONS.items() if v == box.background_color), "Light Grey")
                            selected = st.selectbox("Color", list(COLOR_OPTIONS.keys()),
                                                   index=list(COLOR_OPTIONS.keys()).index(color_name),
                                                   key=f"box_color_{idx}_{box_idx}")
                            box.background_color = COLOR_OPTIONS[selected]
                        with c3:
                            if st.button("🗑️", key=f"del_box_{idx}_{box_idx}"):
                                concept.custom_boxes.pop(box_idx)
                                st.rerun()

                        box.content = st.text_area("Box Content", value=box.content, height=80,
                                                  key=f"box_content_{idx}_{box_idx}")
                        st.divider()

                if st.button("➕ Add Colored Box", key=f"add_box_{idx}"):
                    from core.models.base import CustomBox
                    concept.custom_boxes.append(CustomBox())
                    st.rerun()

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
    col_head, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ Add Answer", type="primary", use_container_width=True):
            data.model_answers.append(ModelAnswer())
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    for idx, answer in enumerate(data.model_answers):
        with st.expander(f"Q{idx+1}: {answer.question[:50] or 'New Question'}...", expanded=idx == 0):
            # Top Row: Question and Meta
            col1, col2 = st.columns([5, 1])
            with col1:
                q = st.text_area("Question", value=answer.question, key=f"ans_q_{idx}", height=70,
                                placeholder="Enter the question here...")
                answer.question = q
            with col2:
                m = st.number_input("Marks", min_value=1, max_value=10,
                                   value=answer.marks, key=f"ans_m_{idx}")
                answer.marks = m
                
                if st.button("🗑️", key=f"del_ans_{idx}", use_container_width=True):
                    data.model_answers.pop(idx)
                    st.rerun()

            # Content Tabs
            tab_ans, tab_scheme = st.tabs(["📝 Model Answer", "📋 Marking Scheme"])
            
            with tab_ans:
                st.caption("Write the ideal answer using markdown.")
                # Toolbar targets the text area below
                render_markdown_toolbar(f"ans_a_{idx}")
                ans = st.text_area("Answer", value=answer.answer,
                                  height=200, key=f"ans_a_{idx}", label_visibility="collapsed",
                                  placeholder="Step-by-step answer...")
                answer.answer = ans
            
            with tab_scheme:
                st.info("Break down the answer into value points (1 mark each).")
                points_text = "\n".join(answer.marking_points) if answer.marking_points else ""
                points = st.text_area("Marking Points (one per line)", value=points_text, height=150,
                                     key=f"ans_points_{idx}")
                answer.marking_points = [p.strip() for p in points.split("\n") if p.strip()]

    # Examiner Tips
    st.divider()
    with st.container(border=True):
        st.subheader("📋 Examiner's Marking Scheme Tips")
        render_markdown_toolbar("examiner_tips")
        tips = st.text_area("Examiner Tips", value=data.examiner_tips or "",
                           placeholder="- 3-mark questions: 3 distinct points...",
                           key="examiner_tips", height=100)
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

    col_head, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ Add MCQ", key="add_mcq", type="primary", use_container_width=True):
            data.mcqs.append(QuestionItem(
                marks=1,
                difficulty='M',
                options=['', '', '', ''],
                answer='a'
            ))
            st.rerun()

    for idx, mcq in enumerate(data.mcqs):
        with st.expander(f"MCQ {idx+1}: {mcq.question[:40] or 'New'}...", expanded=idx == 0):
            # Question Row
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                q = st.text_input("Question", value=mcq.question, key=f"mcq_q_{idx}")
                mcq.question = q
            with col2:
                d = st.selectbox("Diff", ["E", "M", "H"],
                                index=["E", "M", "H"].index(mcq.difficulty) if mcq.difficulty in ["E", "M", "H"] else 1,
                                key=f"mcq_d_{idx}", label_visibility="collapsed")
                mcq.difficulty = d
            with col3:
                if st.button("🗑️", key=f"del_mcq_{idx}"):
                    data.mcqs.pop(idx)
                    st.rerun()

            # Options Grid
            st.caption("Options")
            options = mcq.options or ['', '', '', '']
            
            with st.container(border=True):
                opt_col1, opt_col2 = st.columns(2)
                for i in range(4):
                    col = opt_col1 if i < 2 else opt_col2
                    with col:
                        opt = st.text_input(f"Option ({chr(97+i)})", value=options[i] if i < len(options) else "",
                                           key=f"mcq_opt_{idx}_{i}")
                        if len(options) > i:
                            options[i] = opt
            mcq.options = options

            # Answer
            st.markdown(f"**Correct Answer:**")
            ans_cols = st.columns(4)
            current_ans = mcq.answer if mcq.answer in ['a', 'b', 'c', 'd'] else 'a'
            
            # Custom radio style using columns
            for i, opt_char in enumerate(['a', 'b', 'c', 'd']):
                with ans_cols[i]:
                    if st.checkbox(f"Option {opt_char}", value=(current_ans == opt_char), key=f"mcq_ans_chk_{idx}_{i}"):
                        mcq.answer = opt_char


def render_ar_editor(data):
    """Render Assertion-Reason editor."""
    st.subheader("Assertion-Reason Questions")

    col_head, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ Add A-R", key="add_ar", type="primary", use_container_width=True):
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
                render_markdown_toolbar(f"tb_ar_{idx}")
                q = st.text_area("Assertion and Reason",
                                value=ar.question,
                                placeholder="Assertion: ...\nReason: ...",
                                key=f"ar_q_{idx}", height=100)
                ar.question = q

            with col2:
                if st.button("🗑️", key=f"del_ar_{idx}"):
                    data.assertion_reason.pop(idx)
                    st.rerun()

            st.write("Correct Answer:")
            st.caption("a) Both A and R are true and R is correct explanation...")
            ans = st.selectbox("Select Option", ['a', 'b', 'c', 'd'],
                              index=['a', 'b', 'c', 'd'].index(ar.answer) if ar.answer in ['a', 'b', 'c', 'd'] else 0,
                              key=f"ar_ans_{idx}")
            ar.answer = ans


def render_question_list_editor(questions, title, prefix):
    """Render a generic question list editor."""
    col_h, col_b = st.columns([4, 1])
    with col_h:
        st.subheader(title)
    with col_b:
        if st.button(f"➕ Add", key=f"add_{prefix}", use_container_width=True):
            questions.append(QuestionItem(marks=3 if 'Short' in title else 5))
            st.rerun()

    for idx, q in enumerate(questions):
        with st.expander(f"{idx+1}. {q.question[:40] or 'New'}...", expanded=idx == 0):
            col1, col2 = st.columns([5, 1])

            with col1:
                render_markdown_toolbar(f"{prefix}_q_{idx}")
                question = st.text_area("Question", value=q.question, key=f"{prefix}_q_{idx}", height=100)
                q.question = question

            with col2:
                if st.button("🗑️", key=f"del_{prefix}_{idx}"):
                    questions.pop(idx)
                    st.rerun()

            hint = st.text_input("💡 Hint / Key Value Points (optional)", value=q.hint or "", key=f"{prefix}_h_{idx}")
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
    with st.container(border=True):
        st.subheader("📝 Key Points Summary")
        st.caption("One point per line. Use **bold** for keywords.")
        render_markdown_toolbar("key_points")
        
        points_text = "\n".join(data.revision_key_points) if data.revision_key_points else ""
        points = st.text_area("Key Points", value=points_text, height=200, key="key_points", label_visibility="collapsed")
        data.revision_key_points = [p.strip() for p in points.split("\n") if p.strip()]

    st.divider()

    # Key Terms
    st.subheader("📖 Key Terms")
    
    col_h, col_b = st.columns([4, 1])
    with col_b:
        if st.button("➕ Add Term", key="add_term", use_container_width=True):
            data.revision_key_terms.append({'term': '', 'definition': ''})
            st.rerun()

    for idx, item in enumerate(data.revision_key_terms):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                term = st.text_input("Term", value=item.get('term', ''), key=f"term_{idx}", placeholder="Term")
                item['term'] = term
            with col2:
                definition = st.text_input("Definition", value=item.get('definition', ''), key=f"def_{idx}", placeholder="Definition")
                item['definition'] = definition
            with col3:
                if st.button("🗑️", key=f"del_term_{idx}"):
                    data.revision_key_terms.pop(idx)
                    st.rerun()

    st.divider()

    # Memory Tricks
    with st.container(border=True):
        st.subheader("🧠 Memory Tricks Compilation")
        render_markdown_toolbar("mem_tricks")
        tricks_text = "\n".join(data.revision_memory_tricks) if data.revision_memory_tricks else ""
        tricks = st.text_area("Memory Tricks", value=tricks_text, height=150, key="mem_tricks", label_visibility="collapsed")
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

    col_h, col_b = st.columns([4, 1])
    with col_b:
        if st.button("➕ Add Row", key="add_time", use_container_width=True):
            data.time_allocation.append({'type': '', 'marks': '', 'time': ''})
            st.rerun()

    if data.time_allocation:
        with st.container(border=True):
            # Header Row
            h1, h2, h3, h4 = st.columns([3, 1, 2, 0.5])
            h1.markdown("**Question Type**")
            h2.markdown("**Marks**")
            h3.markdown("**Time (mins)**")
            
            for idx, item in enumerate(data.time_allocation):
                col1, col2, col3, col4 = st.columns([3, 1, 2, 0.5])

                with col1:
                    t = st.text_input("Type", value=item.get('type', ''), key=f"time_type_{idx}", label_visibility="collapsed")
                    item['type'] = t
                with col2:
                    m = st.text_input("Marks", value=item.get('marks', ''), key=f"time_marks_{idx}", label_visibility="collapsed")
                    item['marks'] = m
                with col3:
                    time = st.text_input("Time", value=item.get('time', ''), key=f"time_time_{idx}", label_visibility="collapsed")
                    item['time'] = time
                with col4:
                    if st.button("🗑️", key=f"del_time_{idx}"):
                        data.time_allocation.pop(idx)
                        st.rerun()

    st.divider()

    # Common Mistakes
    st.subheader("❌ What Loses Marks")
    
    col_h, col_b = st.columns([4, 1])
    with col_b:
        if st.button("➕ Add Mistake", key="add_mistake", use_container_width=True):
            data.common_mistakes_exam.append({'mistake': '', 'correction': ''})
            st.rerun()

    for idx, item in enumerate(data.common_mistakes_exam):
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 3, 0.5])
            with col1:
                m = st.text_input("Mistake", value=item.get('mistake', ''), key=f"mistake_{idx}", placeholder="Common Mistake")
                item['mistake'] = m
            with col2:
                c = st.text_input("Correction", value=item.get('correction', ''), key=f"correction_{idx}", placeholder="What to do instead")
                item['correction'] = c
            with col3:
                if st.button("🗑️", key=f"del_mistake_{idx}"):
                    data.common_mistakes_exam.pop(idx)
                    st.rerun()

    st.divider()

    # Pro Tips
    with st.container(border=True):
        st.subheader("✅ Examiner's Pro Tips")
        render_markdown_toolbar("pro_tips")
        tips_text = "\n".join(data.examiner_pro_tips) if data.examiner_pro_tips else ""
        tips = st.text_area("Pro Tips (one per line)", value=tips_text, height=150, key="pro_tips", label_visibility="collapsed")
        data.examiner_pro_tips = [t.strip() for t in tips.split("\n") if t.strip()]

    st.divider()

    # Self-Assessment
    with st.container(border=True):
        st.subheader("☑️ Self-Assessment Checklist")
        render_markdown_toolbar("checklist")
        checklist_text = "\n".join(data.self_assessment_checklist) if data.self_assessment_checklist else ""
        checklist = st.text_area("Checklist Items (one per line)", value=checklist_text, height=150, key="checklist", label_visibility="collapsed")
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

        # Accept JSON, DOCX, PDF, and Markdown files
        uploaded = st.file_uploader(
            "Upload file",
            type=['json', 'docx', 'pdf', 'md'],
            help="Import from JSON (full data), Markdown (structured), DOCX, or PDF"
        )

        if uploaded:
            # Validate file before processing
            is_valid, error_msg = validate_uploaded_file(uploaded)
            if not is_valid:
                st.error(error_msg)
            else:
                file_type = uploaded.name.split('.')[-1].lower()

                # Show preview first for JSON files
                if file_type == 'json':
                    content = uploaded.read().decode('utf-8')
                    uploaded.seek(0)  # Reset file pointer for later import

                    # Preview the data
                    preview_result = SessionManager.import_from_json(content, show_preview=True)

                    if preview_result['success']:
                        st.success("✅ File validated successfully!")

                        # Show preview summary
                        summary = preview_result.get('summary', {})
                        if summary:
                            st.markdown("**Preview:**")
                            preview_cols = st.columns(2)
                            with preview_cols[0]:
                                st.write(f"**Chapter:** {summary.get('chapter_number', '?')}")
                                st.write(f"**Title:** {summary.get('chapter_title', 'Untitled')}")
                            with preview_cols[1]:
                                st.write(f"**Subject:** {summary.get('subject', '?').title()}")
                                st.write(f"**Class:** {summary.get('class_num', '?')}")

                            # Show content counts
                            if any([summary.get('concepts_count'), summary.get('pyq_count'),
                                    summary.get('mcq_count'), summary.get('model_answers_count')]):
                                st.markdown("**Content:**")
                                content_info = []
                                if summary.get('concepts_count'):
                                    content_info.append(f"{summary['concepts_count']} concepts")
                                if summary.get('pyq_count'):
                                    content_info.append(f"{summary['pyq_count']} PYQs")
                                if summary.get('mcq_count'):
                                    content_info.append(f"{summary['mcq_count']} MCQs")
                                if summary.get('model_answers_count'):
                                    content_info.append(f"{summary['model_answers_count']} model answers")
                                st.write(", ".join(content_info))

                        # Confirm import button
                        if st.button("Confirm Import", type="primary", use_container_width=True):
                            content = uploaded.read().decode('utf-8')
                            result = SessionManager.import_from_json(content)

                            if result['success']:
                                st.success("✅ Imported successfully!")
                                if result.get('warnings'):
                                    for warning in result['warnings']:
                                        st.warning(warning)
                                st.session_state.current_page = 'cover'
                                st.rerun()
                            else:
                                for error in result.get('errors', ['Unknown error']):
                                    st.error(f"Import failed: {error}")
                    else:
                        # Show validation errors
                        st.error("File validation failed:")
                        for error in preview_result.get('errors', ['Unknown error']):
                            st.error(f"• {error}")

                elif file_type == 'md':
                    # Markdown import with preview
                    from core.parsers import MarkdownParser, parse_document

                    file_bytes = uploaded.read()
                    uploaded.seek(0)

                    chapter_data = parse_document(file_bytes, file_type)

                    if chapter_data:
                        # Show preview summary
                        summary = MarkdownParser.get_import_summary(chapter_data)
                        st.success("✅ Markdown parsed successfully!")

                        st.markdown("**Preview:**")
                        preview_cols = st.columns(2)
                        with preview_cols[0]:
                            st.write(f"**Chapter:** {summary.get('chapter_number', '?')}")
                            st.write(f"**Title:** {summary.get('chapter_title', 'Untitled')}")
                        with preview_cols[1]:
                            st.write(f"**Subject:** {summary.get('subject', '?').title() if summary.get('subject') else '?'}")
                            st.write(f"**Class:** {summary.get('class_num', '?')}")

                        # Show content counts
                        content_info = []
                        if summary.get('concepts_count'):
                            content_info.append(f"{summary['concepts_count']} concepts")
                        if summary.get('pyq_count'):
                            content_info.append(f"{summary['pyq_count']} PYQs")
                        if summary.get('mcq_count'):
                            content_info.append(f"{summary['mcq_count']} MCQs")
                        if summary.get('short_answer_count'):
                            content_info.append(f"{summary['short_answer_count']} short answers")
                        if summary.get('long_answer_count'):
                            content_info.append(f"{summary['long_answer_count']} long answers")
                        if summary.get('key_points_count'):
                            content_info.append(f"{summary['key_points_count']} key points")
                        if summary.get('key_terms_count'):
                            content_info.append(f"{summary['key_terms_count']} key terms")

                        if content_info:
                            st.markdown("**Content found:**")
                            st.write(", ".join(content_info))

                        if st.button("Confirm Import", type="primary", use_container_width=True, key="md_import"):
                            SessionManager.set_chapter_data(chapter_data)
                            st.success("✅ Imported from Markdown!")
                            st.session_state.current_page = 'cover'
                            st.rerun()
                    else:
                        st.error("Failed to parse Markdown file. Check the format and try again.")

                else:
                    # DOCX or PDF import
                    if st.button("Import", type="primary", use_container_width=True):
                        try:
                            from core.parsers import parse_document, PdfParser

                            file_bytes = uploaded.read()
                            chapter_data = parse_document(file_bytes, file_type)

                            if chapter_data:
                                SessionManager.set_chapter_data(chapter_data)

                                # Show what was extracted
                                st.success(f"✅ Imported from {file_type.upper()}!")

                                extracted = []
                                if chapter_data.chapter_title:
                                    extracted.append(f"Title: {chapter_data.chapter_title}")
                                if chapter_data.chapter_number:
                                    extracted.append(f"Chapter: {chapter_data.chapter_number}")
                                if chapter_data.subject:
                                    extracted.append(f"Subject: {chapter_data.subject.title()}")
                                if chapter_data.weightage:
                                    extracted.append(f"Weightage: {chapter_data.weightage}")
                                if chapter_data.importance:
                                    extracted.append(f"Importance: {chapter_data.importance}")

                                if extracted:
                                    st.info("**Extracted:** " + " | ".join(extracted))

                                st.warning("Note: Only basic metadata extracted from DOCX/PDF. Fill in remaining sections manually.")
                                st.session_state.current_page = 'cover'
                                st.rerun()
                            else:
                                # Check if failure was due to missing PDF dependencies
                                if file_type == 'pdf' and PdfParser.was_missing_deps():
                                    st.warning(PdfParser.get_missing_dependency_message())
                                st.error(f"Failed to parse {file_type.upper()} file. The document format may not be recognized.")

                        except Exception as e:
                            st.error(f"Import error: {str(e)}")

        # Help text
        st.caption("""
        **Import formats:**
        - **JSON**: Full chapter data with validation (recommended for backup/restore)
        - **Markdown**: Structured content with headers, tables, and lists
        - **DOCX/PDF**: Extracts chapter metadata and basic content
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
