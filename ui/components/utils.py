"""
Utility components for UI enhancement.
"""
import streamlit as st

def insert_at_cursor(key: str, text_to_insert: str):
    """
    Helper to append text to a session state variable.
    Note: Streamlit doesn't support cursor-position insertion natively yet,
    so we append to the end.
    """
    if key in st.session_state:
        current_text = st.session_state[key]
        # Add a space if not empty and not ending with newline
        prefix = ""
        if current_text and not current_text.endswith(('\n', ' ')):
            prefix = " "
        
        st.session_state[key] = current_text + prefix + text_to_insert

def render_markdown_toolbar(target_key: str):
    """
    Render a functional markdown toolbar for a specific text area.
    Target key must match the key of the st.text_area.
    """
    # Use small columns for a compact toolbar
    cols = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 6])
    
    # Define tool buttons
    tools = [
        {"label": "𝐁", "help": "Bold", "insert": "**bold**"},
        {"label": "𝐼", "help": "Italic", "insert": "*italic*"},
        {"label": "•", "help": "Bullet List", "insert": "\n- "},
        {"label": "1.", "help": "Numbered List", "insert": "\n1. "},
        {"label": "▦", "help": "Table", "insert": "\n| Col 1 | Col 2 |\n|---|---|\n| Val 1 | Val 2 |"},
    ]
    
    # CSS to make buttons smaller/compact is handled in navigation.py (global styles)
    # We render standard buttons but they trigger the callback
    
    for i, tool in enumerate(tools):
        with cols[i]:
            if st.button(tool["label"], 
                        key=f"btn_{target_key}_{i}", 
                        help=tool["help"],
                        use_container_width=True):
                insert_at_cursor(target_key, tool["insert"])
                st.rerun()

def get_markdown_help_caption():
    return "Supported formatting: **bold**, *italic*, - bullet point, 1. numbered list"
