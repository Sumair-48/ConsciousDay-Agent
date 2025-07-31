import streamlit as st
from datetime import datetime, date
from typing import Dict, Optional

class JournalForm:
    def __init__(self):
        pass
    
    def render_form(self, existing_entry=None) -> Optional[Dict[str, str]]:
        """Render the main journal form."""
        st.subheader("🌅 Morning Reflection")
        st.write("Take a moment to reflect on your inner state and set intentions for the day.")
        
        with st.form("journal_form", clear_on_submit=False):
            # Date selector
            selected_date = st.date_input(
                "Date",
                value=date.today() if not existing_entry else datetime.strptime(existing_entry.date, "%Y-%m-%d").date(),
                help="Select the date for this journal entry"
            )
            
            # Form fields
            journal = st.text_area(
                "Morning Journal",
                value=existing_entry.journal if existing_entry else "",
                placeholder="How are you feeling this morning? What's on your mind? Write freely about your current state...",
                height=150,
                help="Express your thoughts, feelings, and observations from this morning"
            )
            
            intention = st.text_input(
                "Intention of the Day",
                value=existing_entry.intention if existing_entry else "",
                placeholder="What do you want to embody or focus on today?",
                help="Your guiding principle or mindset for the day"
            )
            
            dream = st.text_area(
                "Dream (Optional)",
                value=existing_entry.dream if existing_entry else "",
                placeholder="Describe any dreams you remember from last night...",
                height=100,
                help="Dreams can offer insights into your subconscious mind"
            )
            
            priorities = st.text_area(
                "Top 3 Priorities",
                value=existing_entry.priorities if existing_entry else "",
                placeholder="1. Most important task\n2. Second priority\n3. Third priority",
                height=100,
                help="List your three most important tasks or goals for today"
            )
            
            submitted = st.form_submit_button("✨ Generate Reflection & Strategy", type="primary")
            
            if submitted:
                # Validation
                if not journal.strip():
                    st.error("Please write something in your morning journal.")
                    return None
                
                if not intention.strip():
                    st.error("Please set an intention for the day.")
                    return None
                
                if not priorities.strip():
                    st.error("Please list your top 3 priorities.")
                    return None
                
                return {
                    'date': selected_date.strftime("%Y-%m-%d"),
                    'journal': journal.strip(),
                    'intention': intention.strip(),
                    'dream': dream.strip(),
                    'priorities': priorities.strip()
                }
        
        return None

class DateSelector:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def render_date_selector(self) -> Optional[str]:
        """Render date selector for historical entries."""
        st.subheader("📅 View Previous Reflections")
        
        available_dates = self.db_manager.get_all_dates()
        
        if not available_dates:
            st.info("No previous entries found. Create your first journal entry!")
            return None
        
        selected_date = st.selectbox(
            "Select a date to view:",
            options=available_dates,
            format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%B %d, %Y"),
            help="Choose from your previous journal entries"
        )
        
        return selected_date