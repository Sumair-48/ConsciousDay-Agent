import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_PATH = "entries.db"
    
    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Model Configuration
    DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"
    
    # App Configuration
    APP_TITLE = "ConsciousDay Agent"
    APP_TAGLINE = "Reflect inward. Act with clarity."
    
    # Authentication
    AUTH_COOKIE_NAME = "consciousday_auth"
    AUTH_COOKIE_KEY = os.getenv("AUTH_COOKIE_KEY", "consciousday_secret_key")
    AUTH_COOKIE_EXPIRY_DAYS = 30