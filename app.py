import streamlit as st
import os
from utils.helpers import setup_logging, init_session_state, validate_api_configuration
from components.auth import AuthManager
from pages.home import render_home_page
from pages.history import render_history_page
from config.settings import Config

# Configure page
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logging
setup_logging()

# Initialize session state
init_session_state()

def main():
    """Main application function."""
    # Initialize auth manager
    try:
        # Try to access secrets, fallback to environment variables
        try:
            api_key = st.secrets["OPENROUTER_API_KEY"]
        except (KeyError, st.errors.StreamlitSecretNotFoundError):
            api_key = os.getenv("OPENROUTER_API_KEY")
            
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in secrets or environment")
            
        Config.validate_config()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please configure the required secrets in .streamlit/secrets.toml or Streamlit Cloud settings.")
        return
    
    auth = AuthManager()
    
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        color: #ecf0f1;
    }
    .sidebar-info {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 1.2rem;
        border-radius: 0.7rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .sidebar-info h3 {
        color: #ecf0f1;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .sidebar-info p {
        color: #e0e0e0;
        margin: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
        padding: 1.2rem;
        border-radius: 0.7rem;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stRadio > label {
        color: #34495e;
    }
    .stButton button {
        background: #3498db;
        color: white;
        border: none;
    }
    .stButton button:hover {
        background: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🌅 {Config.APP_TITLE}</h1>
        <p><em>{Config.APP_TAGLINE}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API configuration
    if not validate_api_configuration():
        st.error("⚠️ API configuration missing. Please set your OPENROUTER_API_KEY in environment variables.")
        st.info("The app will still work but will provide fallback responses instead of AI-generated insights.")
    
    # Authentication check
    if not auth.is_authenticated():
        st.info("🔐 Please log in to access your personal journal.")
        auth.login_form()
        return
    
    # Sidebar navigation
    with st.sidebar:
        user_info = auth.get_user_info()
        st.markdown(f"""
        <div class="sidebar-info">
            <h3>👋 Welcome, {user_info['name']}!</h3>
            <p>Ready for today's reflection?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Choose a page:",
            ["🌅 Daily Reflection", "📚 Journal History"],
            help="Navigate between creating new entries and viewing past reflections"
        )
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary"):
            auth.logout()
        
        # App info
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **ConsciousDay Agent** helps you:
        - Process morning thoughts & feelings
        - Understand your dreams
        - Set clear daily intentions
        - Create mindful action strategies
        """)
        
        # API status
        if validate_api_configuration():
            st.success("🤖 AI Agent: Connected")
        else:
            st.warning("🤖 AI Agent: Fallback Mode")


    # Main content area
    if page == "🌅 Daily Reflection":
        render_home_page()
    elif page == "📚 Journal History":
        render_history_page()

if __name__ == "__main__":
    main()