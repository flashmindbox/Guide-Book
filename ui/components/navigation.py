"""
Navigation components for Guide Book Generator.
Provides breadcrumb navigation, progress badges, and unsaved indicators.
"""

from typing import Optional

import streamlit as st

# Page definitions with labels and icons
PAGE_INFO = {
    'home': {'label': 'Home', 'icon': '🏠', 'short': 'Home'},
    'import_export': {'label': 'Import/Export', 'icon': '📥', 'short': 'Import'},
    'cover': {'label': 'Cover Page', 'icon': '📄', 'short': 'Cover'},
    'part_a': {'label': 'Part A: PYQ Analysis', 'icon': '📊', 'short': 'Part A'},
    'part_b': {'label': 'Part B: Key Concepts', 'icon': '📖', 'short': 'Part B'},
    'part_c': {'label': 'Part C: Model Answers', 'icon': '✅', 'short': 'Part C'},
    'part_d': {'label': 'Part D: Practice Questions', 'icon': '📝', 'short': 'Part D'},
    'part_e': {'label': 'Part E: Map Work', 'icon': '🗺️', 'short': 'Part E'},
    'part_f': {'label': 'Part F: Quick Revision', 'icon': '🔄', 'short': 'Part F'},
    'part_g': {'label': 'Part G: Exam Strategy', 'icon': '🎯', 'short': 'Part G'},
    'generate': {'label': 'Generate', 'icon': '⚙️', 'short': 'Generate'},
}

# Workflow order for sequential navigation
WORKFLOW_ORDER = [
    'home', 'cover', 'part_a', 'part_b', 'part_c',
    'part_d', 'part_e', 'part_f', 'part_g', 'generate'
]


def inject_custom_css():
    """Inject custom CSS for improved UI styling."""
    st.markdown("""
    <style>
    /* Global Font & Reset */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Unsaved indicator pulsing animation */
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }

    .unsaved-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #EF4444;
        border-radius: 50%;
        margin-left: 8px;
        box-shadow: 0 0 4px rgba(239, 68, 68, 0.4);
        animation: pulse 2s infinite ease-in-out;
    }

    /* Progress badge styles */
    .progress-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 600;
        margin-left: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-complete {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }

    .badge-partial {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    .badge-empty {
        background-color: #F3F4F6;
        color: #6B7280;
        border: 1px solid #E5E7EB;
    }

    /* Breadcrumb navigation */
    .breadcrumb-nav {
        padding: 12px 16px;
        margin-bottom: 24px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    .breadcrumb-nav a {
        color: #6B7280;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        transition: color 0.2s;
    }

    .breadcrumb-nav a:hover {
        color: #2563EB;
    }

    .breadcrumb-separator {
        color: #D1D5DB;
        margin: 0 12px;
        font-size: 12px;
    }

    .breadcrumb-current {
        color: #111827;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Section header styling */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 24px;
        background: white;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        border-left: 5px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }

    .section-header h1 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #1F2937;
    }

    /* Workflow step indicator */
    .workflow-steps {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
        margin-bottom: 24px;
    }

    .workflow-step {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 600;
        z-index: 2;
        transition: all 0.3s ease;
    }

    .step-complete {
        background-color: #10B981;
        color: white;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
    }

    .step-current {
        background-color: #2563EB;
        color: white;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
    }

    .step-pending {
        background-color: white;
        border: 2px solid #E5E7EB;
        color: #9CA3AF;
    }

    .step-connector {
        width: 40px;
        height: 3px;
        background-color: #E5E7EB;
        margin: 0 -4px;
        z-index: 1;
    }

    .step-connector-complete {
        background-color: #10B981;
    }

    /* Card style for sections */
    .stExpander {
        border: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-radius: 8px !important;
        background-color: white !important;
        margin-bottom: 12px !important;
        overflow: hidden;
    }
    
    .streamlit-expanderHeader {
        background-color: #F9FAFB !important;
        border-bottom: 1px solid #F3F4F6;
        font-weight: 600;
        color: #374151;
    }

    /* Custom Form Styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        border-radius: 6px;
        border-color: #E5E7EB;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
    }

    /* Markdown Toolbar Buttons */
    .md-toolbar-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        color: #4B5563;
        font-size: 14px;
        cursor: default; /* Not clickable for now */
        margin-bottom: 4px;
        font-family: monospace;
    }
    
    .status-saved {
        color: #10B981;
        font-weight: 600;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 8px;
        background: #ECFDF5;
        border-radius: 4px;
    }

    .status-unsaved {
        color: #EF4444;
        font-weight: 600;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 8px;
        background: #FEF2F2;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_unsaved_indicator(is_dirty: bool) -> str:
    """Return HTML for unsaved indicator if dirty."""
    if is_dirty:
        return '<span class="unsaved-indicator" title="Unsaved changes"></span>'
    return ''


def render_progress_badge(percentage: float) -> str:
    """Return HTML for a progress badge."""
    if percentage >= 80:
        return f'<span class="progress-badge badge-complete">{percentage:.0f}%</span>'
    elif percentage >= 1:
        return f'<span class="progress-badge badge-partial">{percentage:.0f}%</span>'
    else:
        return '<span class="progress-badge badge-empty">0%</span>'


def render_breadcrumb(current_page: str, chapter_title: Optional[str] = None):
    """Render breadcrumb navigation at the top of the page."""
    if current_page == 'home':
        return  # No breadcrumb on home page

    page_info = PAGE_INFO.get(current_page, {'label': current_page.title(), 'icon': '📄'})

    # Build breadcrumb HTML
    breadcrumb_html = '<nav class="breadcrumb-nav">'
    breadcrumb_html += '<a href="#" onclick="return false;">🏠 Home</a>'

    if chapter_title:
        breadcrumb_html += '<span class="breadcrumb-separator">›</span>'
        breadcrumb_html += f'<span>{chapter_title[:30]}...</span>'

    breadcrumb_html += '<span class="breadcrumb-separator">›</span>'
    breadcrumb_html += f'<span class="breadcrumb-current">{page_info["icon"]} {page_info["label"]}</span>'
    breadcrumb_html += '</nav>'

    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def get_workflow_position(page_id: str) -> int:
    """Get the position of a page in the workflow."""
    if page_id in WORKFLOW_ORDER:
        return WORKFLOW_ORDER.index(page_id)
    return -1


def render_workflow_indicator(current_page: str, progress_data: dict):
    """Render a visual workflow progress indicator."""
    current_pos = get_workflow_position(current_page)

    steps_html = '<div class="workflow-steps">'

    for idx, page_id in enumerate(WORKFLOW_ORDER):
        if page_id == 'home':
            continue  # Skip home in workflow display

        # Determine step status
        page_progress = progress_data.get(page_id, 0)

        if idx < current_pos or page_progress >= 80:
            step_class = 'step-complete'
            connector_class = 'step-connector-complete'
            icon = '✓'
        elif idx == current_pos:
            step_class = 'step-current'
            connector_class = ''
            icon = str(idx)
        else:
            step_class = 'step-pending'
            connector_class = ''
            icon = str(idx)

        # Add connector (except for first item)
        if idx > 1:  # Skip connector before first visible step
            steps_html += f'<div class="step-connector {connector_class}"></div>'

        # Add step
        steps_html += f'<div class="workflow-step {step_class}" title="{PAGE_INFO.get(page_id, {}).get("label", page_id)}">{icon}</div>'

    steps_html += '</div>'

    st.markdown(steps_html, unsafe_allow_html=True)


def render_navigation_button(page_id: str, label: str, progress: float, is_current: bool) -> bool:
    """Render a navigation button with progress indicator."""
    # Build button label with status
    if progress >= 80:
        status = '✅'
    elif progress >= 1:
        status = '🔶'
    else:
        status = '⬜'

    full_label = f"{status} {label}"

    # Use Streamlit button
    button_type = "primary" if is_current else "secondary"
    return st.button(full_label, key=f"nav_{page_id}", use_container_width=True,
                     type=button_type if is_current else "secondary")


def render_next_prev_buttons(current_page: str) -> Optional[str]:
    """Render previous/next navigation buttons. Returns new page if navigation requested."""
    current_pos = get_workflow_position(current_page)

    if current_pos < 0:
        return None

    col1, col2, col3 = st.columns([1, 2, 1])
    new_page = None

    with col1:
        if current_pos > 0:
            prev_page = WORKFLOW_ORDER[current_pos - 1]
            prev_info = PAGE_INFO.get(prev_page, {'icon': '←', 'short': 'Previous'})
            if st.button(f"← {prev_info['short']}", use_container_width=True):
                new_page = prev_page

    with col3:
        if current_pos < len(WORKFLOW_ORDER) - 1:
            next_page = WORKFLOW_ORDER[current_pos + 1]
            next_info = PAGE_INFO.get(next_page, {'icon': '→', 'short': 'Next'})
            if st.button(f"{next_info['short']} →", type="primary", use_container_width=True):
                new_page = next_page

    return new_page


def render_section_header(title: str, icon: str, progress: Optional[float] = None):
    """Render a consistent section header with optional progress."""
    header_html = '<div class="section-header">'
    header_html += f'<h1>{icon} {title}</h1>'

    if progress is not None:
        header_html += render_progress_badge(progress)

    header_html += '</div>'

    st.markdown(header_html, unsafe_allow_html=True)
