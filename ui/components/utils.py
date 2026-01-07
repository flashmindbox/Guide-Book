"""
Utility components for UI enhancement.
"""
import streamlit as st

def render_markdown_toolbar(key_prefix: str):
    """
    Render a simulated toolbar for markdown formatting.
    Note: Real-time insertion isn't possible in Streamlit without custom components,
    but this provides a visual guide/helper.
    """
    cols = st.columns([1, 1, 1, 1, 1, 8])
    with cols[0]:
        st.markdown(f'<div class="md-toolbar-btn" title="Bold"><b>B</b></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="md-toolbar-btn" title="Italic"><i>I</i></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="md-toolbar-btn" title="Bullet List">•</div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="md-toolbar-btn" title="Numbered List">1.</div>', unsafe_allow_html=True)
    with cols[4]:
        st.markdown(f'<div class="md-toolbar-btn" title="Table">▦</div>', unsafe_allow_html=True)
    
    # In a real app with custom JS, these would be clickable. 
    # For now, we just show them as a visual hint or we could make them insert text if we used session state + callback,
    # but that resets the text area cursor position which is annoying.
    # So we'll add a caption instead explaining usage.
    
def get_markdown_help_caption():
    return "Supported formatting: **bold**, *italic*, - bullet point, 1. numbered list"
