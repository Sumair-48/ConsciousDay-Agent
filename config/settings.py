import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database

    DATABASE_PATH = os.getenv("DATABASE_PATH")
    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Model Configuration
    DEFAULT_MODEL = "anthropic/claude-3-haiku"
    
    # App Configuration
    APP_TITLE = "ConsciousDay Agent"
    APP_TAGLINE = "Reflect inward. Act with clarity."
    
    # Authentication
    AUTH_COOKIE_NAME = "consciousday_auth"
    AUTH_COOKIE_KEY = os.getenv("AUTH_COOKIE_KEY", "consciousday_secret_key")
    AUTH_COOKIE_EXPIRY_DAYS = 30

    @classmethod
    def validate_config(cls):
        """Validate required configuration."""
        missing = []
        if not cls.OPENROUTER_API_KEY:
            missing.append("OPENROUTER_API_KEY")
        if not cls.DATABASE_PATH:
            missing.append("DATABASE_PATH")
        if not cls.AUTH_COOKIE_KEY:
            missing.append("AUTH_COOKIE_KEY")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return True