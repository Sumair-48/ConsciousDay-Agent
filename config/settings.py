import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_PATH = "entries.db"
    
    # API Configuration
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Model Configuration
    DEFAULT_MODEL = "anthropic/claude-3-haiku"
    
    # App Configuration
    APP_TITLE = "ConsciousDay Agent"
    APP_TAGLINE = "Reflect inward. Act with clarity."
    
    # Authentication
    AUTH_COOKIE_NAME = "consciousday_auth"
    AUTH_COOKIE_KEY = st.secrets["AUTH_COOKIE_KEY"]
    AUTH_COOKIE_EXPIRY_DAYS = 30