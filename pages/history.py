import streamlit as st
from components.forms import DateSelector
from components.display import DisplayManager
from database.db_manager import DatabaseManager
from components.auth import AuthManager 

def render_history_page():
    """Render the history page for viewing previous entries."""

    # Initialize auth
    auth = AuthManager()
    
    # Check authentication
    if not auth.is_authenticated():
        auth.login_form()
        return

    st.title("📚 Journal History")
    st.markdown("*Review your journey of self-reflection and growth.*")
    
    # Initialize components
    db = DatabaseManager()
    date_selector = DateSelector(db)
    display = DisplayManager()
    
    # Render date selector
    selected_date = date_selector.render_date_selector()
    
    if selected_date:
        # Fetch and display the entry
        entry = db.get_entry_by_date(selected_date)
        
        if entry:
            display.display_historical_entry(entry)
        else:
            st.error("Entry not found for the selected date.")
    
    # Display statistics
    st.markdown("---")
    st.subheader("📊 Your Reflection Journey")
    
    all_dates = db.get_all_dates()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Entries", len(all_dates))
    
    with col2:
        if all_dates:
            from datetime import datetime
            first_entry = datetime.strptime(all_dates[-1], "%Y-%m-%d")
            days_since = (datetime.now() - first_entry).days
            st.metric("Days Since First Entry", days_since)
        else:
            st.metric("Days Since First Entry", 0)
    
    with col3:
        # Calculate consistency (entries in last 7 days)
        if all_dates:
            from datetime import datetime, timedelta
            recent_dates = [d for d in all_dates if datetime.strptime(d, "%Y-%m-%d") >= datetime.now() - timedelta(days=7)]
            consistency = len(recent_dates)
        else:
            consistency = 0
        st.metric("Entries (Last 7 Days)", consistency)