"""
Utility components for UI enhancement.
"""
import streamlit as st

def insert_at_cursor(key: str, text_to_insert: str, is_block: bool = False):
    """
    Helper to append text to a session state variable.
    """
    if key in st.session_state:
        current_text = st.session_state[key] or ""
        
        # Ensure block elements (lists, tables) start on a new line
        if is_block and current_text and not current_text.endswith('\n'):
            current_text += '\n'
        
        # Add a space for inline elements if not at start/newline
        if not is_block and current_text and not current_text.endswith(('\n', ' ')):
            current_text += ' '
            
        st.session_state[key] = current_text + text_to_insert

def render_markdown_toolbar(target_key: str):
    """
    Render a functional markdown toolbar for a specific text area.
    """
    # Use extra small columns for a very tight toolbar
    cols = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 6])
    
    # Define tool buttons
    tools = [
        {"label": "𝐁", "help": "Bold", "insert": "**BOLD**", "block": False},
        {"label": "𝐼", "help": "Italic", "insert": "*italic*", "block": False},
        {"label": "•", "help": "Bullet List", "insert": "- Item", "block": True},
        {"label": "1.", "help": "Numbered List", "insert": "1. Item", "block": True},
        {"label": "▦", "help": "Table", "insert": "| Header 1 | Header 2 |\n|---|---|\n| Cell 1 | Cell 2 |", "block": True},
    ]
    
    for i, tool in enumerate(tools):
        with cols[i]:
            if st.button(tool["label"], 
                        key=f"btn_{target_key}_{i}", 
                        help=tool["help"],
                        use_container_width=True):
                insert_at_cursor(target_key, tool["insert"], tool["block"])
                st.rerun()
    
    # Add a Clear button as the 6th element
    with cols[5]:
        if st.button("⌫", key=f"btn_{target_key}_clear", help="Clear Field"):
            st.session_state[target_key] = ""
            st.rerun()

def get_markdown_help_caption():
    return "Supported formatting: **bold**, *italic*, - bullet point, 1. numbered list"
