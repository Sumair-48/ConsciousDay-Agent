import streamlit as st
from components.forms import JournalForm
from components.display import DisplayManager
from agent.langchain_agent import ConsciousDayAgent
from database.db_manager import DatabaseManager
from database.models import JournalEntry

def render_home_page():
    """Render the main journaling page."""
    st.title("🌅 Daily Reflection")
    st.markdown("*Reflect inward. Act with clarity.*")
    
    # Initialize components
    form = JournalForm()
    display = DisplayManager()
    agent = ConsciousDayAgent()
    db = DatabaseManager()
    
    # Check if entry already exists for today
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    existing_entry = db.get_entry_by_date(today)
    
    if existing_entry:
        st.info(f"📝 You already have an entry for today ({today}). You can view it below or create a new one.")
        
        # Option to view existing entry
        if st.button("View Today's Entry"):
            st.session_state['show_existing'] = True
        
        if st.session_state.get('show_existing', False):
            display.display_historical_entry(existing_entry)
            if st.button("Create New Entry"):
                st.session_state['show_existing'] = False
                st.rerun()
            return
    
    # Render the form
    form_data = form.render_form()
    
    if form_data:
        # Check if entry already exists for selected date
        if db.entry_exists_for_date(form_data['date']) and form_data['date'] != today:
            if not st.session_state.get('confirm_overwrite', False):
                st.warning(f"An entry already exists for {form_data['date']}. Do you want to overwrite it?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, Overwrite"):
                        st.session_state['confirm_overwrite'] = True
                        st.rerun()
                with col2:
                    if st.button("Cancel"):
                        return
                return
        
        # Generate reflection
        with st.spinner("🤖 Generating your personalized reflection and strategy..."):
            try:
                results = agent.generate_reflection(
                    journal=form_data['journal'],
                    intention=form_data['intention'],
                    dream=form_data['dream'],
                    priorities=form_data['priorities']
                )
                
                # Create journal entry
                entry = JournalEntry(
                    date=form_data['date'],
                    journal=form_data['journal'],
                    intention=form_data['intention'],
                    dream=form_data['dream'],
                    priorities=form_data['priorities'],
                    reflection=results['full_response'],
                    strategy=results.get('strategy', '')
                )
                
                # Save to database
                if db.save_entry(entry):
                    display.display_reflection_results(results, form_data['date'])
                else:
                    st.error("Failed to save entry to database.")
                
                # Reset confirmation state
                if 'confirm_overwrite' in st.session_state:
                    del st.session_state['confirm_overwrite']
                    
            except Exception as e:
                st.error(f"An error occurred while generating your reflection: {str(e)}")
                st.info("Please check your API configuration and try again.")