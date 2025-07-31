import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
from typing import Dict, Optional
from config.settings import Config

class AuthManager:
    def __init__(self):
        self.cookie_name = Config.AUTH_COOKIE_NAME
        self.cookie_key = Config.AUTH_COOKIE_KEY
        self.cookie_expiry_days = Config.AUTH_COOKIE_EXPIRY_DAYS
        
        # Simple user database (in production, use proper database)
        self.users = {
            'demo_user': {
                'name': 'Demo User',
                'password': self._hash_password('demo123'),
                'email': 'demo@consciousday.app'
            },
            # ADD NEW USER HERE
            'your_username': {
                'name': 'Your Name',
                'password': self._hash_password('your_password'),
                'email': 'your@email.com'
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def login_form(self) -> Optional[str]:
        """Display login form and handle authentication."""
        with st.form("login_form"):
            st.subheader("🔐 Login to Your Journal")
            st.write("Demo credentials: username: `demo_user`, password: `demo123`")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if username in self.users:
                    if self._verify_password(password, self.users[username]['password']):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = self.users[username]['name']
                        st.success("Login successful!")
                        st.rerun()
                        return username
                    else:
                        st.error("Invalid password")
                else:
                    st.error("Username not found")
            
            return None
    
    def logout(self):
        """Handle user logout."""
        for key in ['authenticated', 'username', 'name']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return st.session_state.get('authenticated', False)
    
    def get_user_info(self) -> Dict[str, str]:
        """Get current user information."""
        return {
            'username': st.session_state.get('username', ''),
            'name': st.session_state.get('name', '')
        }