import streamlit as st
from datetime import datetime, date
import logging
from typing import Any, Dict

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('consciousday.log'),
            logging.StreamHandler()
        ]
    )

def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if 'show_existing' not in st.session_state:
        st.session_state['show_existing'] = False
    
    if 'confirm_overwrite' not in st.session_state:
        st.session_state['confirm_overwrite'] = False

def format_date(date_str: str, format_type: str = "display") -> str:
    """Format date string for display."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if format_type == "display":
            return date_obj.strftime("%B %d, %Y")
        elif format_type == "short":
            return date_obj.strftime("%m/%d/%Y")
        else:
            return date_str
    except ValueError:
        return date_str

def validate_api_configuration() -> bool:
    """Validate API configuration."""
    from config.settings import Config
    return bool(Config.OPENROUTER_API_KEY)

def safe_get_session_state(key: str, default: Any = None) -> Any:
    """Safely get session state value."""
    return st.session_state.get(key, default)

def clear_form_data():
    """Clear form data from session state."""
    form_keys = ['journal', 'intention', 'dream', 'priorities', 'selected_date']
    for key in form_keys:
        if key in st.session_state:
            del st.session_state[key]

def get_user_timezone():
    """Get user timezone (placeholder for future enhancement)."""
    return "UTC"

def sanitize_input(text: str) -> str:
    """Basic input sanitization."""
    if not text:
        return ""
    # Remove potential harmful characters while preserving meaningful content
    return text.strip()[:10000]  # Limit length to prevent abuse