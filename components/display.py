import streamlit as st
from database.models import JournalEntry
from typing import Dict

class DisplayManager:
    def __init__(self):
        pass
    
    def display_reflection_results(self, results: Dict[str, str], entry_date: str):
        """Display the AI-generated reflection and strategy."""
        st.success("✨ Your reflection has been generated!")
        
        # Display results in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🪞 Inner Reflection", 
            "🌙 Dream Insights", 
            "🧠 Mindset Analysis", 
            "🎯 Day Strategy"
        ])
        
        with tab1:
            st.markdown("### Inner Reflection Summary")
            if results.get('reflection'):
                st.markdown(results['reflection'])
            else:
                st.info("Reflection analysis not available.")
        
        with tab2:
            st.markdown("### Dream Interpretation")
            if results.get('dream_interpretation'):
                st.markdown(results['dream_interpretation'])
            else:
                st.info("Dream interpretation not available.")
        
        with tab3:
            st.markdown("### Energy & Mindset Insight")
            if results.get('mindset_insight'):
                st.markdown(results['mindset_insight'])
            else:
                st.info("Mindset insight not available.")
        
        with tab4:
            st.markdown("### Suggested Day Strategy")
            if results.get('strategy'):
                st.markdown(results['strategy'])
            else:
                st.info("Day strategy not available.")
        
        # Show save confirmation
        st.info(f"💾 Entry saved for {entry_date}")
    
    def display_historical_entry(self, entry: JournalEntry):
        """Display a historical journal entry."""
        st.markdown(f"## 📖 Journal Entry - {entry.date}")
        
        # Input section
        st.markdown("### Your Inputs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Morning Journal:**")
            st.text_area("Journal", value=entry.journal, disabled=True, key=f"journal_{entry.id}")
            
            st.markdown("**Intention of the Day:**")
            st.text_input("Intention", value=entry.intention, disabled=True, key=f"intention_{entry.id}")
        
        with col2:
            st.markdown("**Dream:**")
            st.text_area("Dream", value=entry.dream or "No dream recorded", disabled=True, key=f"dream_{entry.id}")
            
            st.markdown("**Top 3 Priorities:**")
            st.text_area("Priorities", value=entry.priorities, disabled=True, key=f"priorities_{entry.id}")
        
        # AI Analysis section
        st.markdown("### AI Analysis & Strategy")
        
        # Parse the full response into sections
        full_response = entry.reflection if entry.reflection else entry.strategy
        
        if "## Inner Reflection Summary" in full_response:
            sections = self._parse_response_sections(full_response)
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "🪞 Inner Reflection", 
                "🌙 Dream Insights", 
                "🧠 Mindset Analysis", 
                "🎯 Day Strategy"
            ])
            
            with tab1:
                st.markdown(sections.get('reflection', 'Not available'))
            
            with tab2:
                st.markdown(sections.get('dream_interpretation', 'Not available'))
            
            with tab3:
                st.markdown(sections.get('mindset_insight', 'Not available'))
            
            with tab4:
                st.markdown(sections.get('strategy', 'Not available'))
        else:
            # Fallback display
            st.markdown("**Reflection:**")
            st.markdown(entry.reflection)
            
            st.markdown("**Strategy:**")
            st.markdown(entry.strategy)
    
    def _parse_response_sections(self, response: str) -> Dict[str, str]:
        """Parse AI response into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('## Inner Reflection Summary'):
                current_section = 'reflection'
                current_content = []
            elif line.startswith('## Dream Interpretation Summary'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'dream_interpretation'
                current_content = []
            elif line.startswith('## Energy/Mindset Insight'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'mindset_insight'
                current_content = []
            elif line.startswith('## Suggested Day Strategy'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'strategy'
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def display_error(self, error_message: str):
        """Display error message."""
        st.error(f"❌ {error_message}")
    
    def display_loading(self, message: str = "Processing your reflection..."):
        """Display loading message."""
        with st.spinner(message):
            return st.empty()