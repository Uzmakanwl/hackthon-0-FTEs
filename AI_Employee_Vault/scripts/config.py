"""
Configuration Module

Loads environment variables and provides configuration for the AI Employee system.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class Config:
    """Configuration class for AI Employee."""
    
    # Vault paths
    VAULT_PATH = os.getenv('VAULT_PATH', str(Path(__file__).parent.parent))
    DROP_FOLDER = os.getenv('DROP_FOLDER_PATH', str(Path(__file__).parent.parent / 'DropFolder'))
    
    # Gmail API (Silver Tier)
    GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID', '')
    GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET', '')
    GMAIL_REFRESH_TOKEN = os.getenv('GMAIL_REFRESH_TOKEN', '')
    GMAIL_API_KEY = os.getenv('GMAIL_API_KEY', '')
    
    # Bank API (Silver Tier)
    BANK_API_TOKEN = os.getenv('BANK_API_TOKEN', '')
    BANK_API_KEY = os.getenv('BANK_API_KEY', '')
    
    # WhatsApp
    WHATSAPP_SESSION_PATH = os.getenv('WHATSAPP_SESSION_PATH', '')
    
    # Email MCP
    EMAIL_MCP_ENABLED = os.getenv('EMAIL_MCP_ENABLED', 'false').lower() == 'true'
    EMAIL_SMTP_HOST = os.getenv('EMAIL_SMTP_HOST', 'smtp.gmail.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Development settings
    DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
    MAX_ACTIONS_PER_HOUR = int(os.getenv('MAX_ACTIONS_PER_HOUR', '10'))
    
    # Watcher settings
    WATCHER_CHECK_INTERVAL = int(os.getenv('WATCHER_CHECK_INTERVAL', '5'))
    ORCHESTRATOR_CHECK_INTERVAL = int(os.getenv('ORCHESTRATOR_CHECK_INTERVAL', '30'))
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if essential configuration is in place."""
        # For Bronze tier, no API keys are required
        return True
    
    @classmethod
    def get_missing_config(cls) -> list:
        """Return list of missing configuration for higher tiers."""
        missing = []
        
        # Gmail Watcher (Silver Tier)
        if not cls.GMAIL_CLIENT_ID:
            missing.append('GMAIL_CLIENT_ID')
        if not cls.GMAIL_CLIENT_SECRET:
            missing.append('GMAIL_CLIENT_SECRET')
        
        # Bank API (Silver Tier)
        if not cls.BANK_API_TOKEN:
            missing.append('BANK_API_TOKEN')
        
        return missing


# Export config instance
config = Config()
