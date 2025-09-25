"""
Configuration module for Gmail MCP Server
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class GmailConfig:
    """Gmail MCP Server configuration"""
    
    # Gmail API Configuration
    GMAIL_CREDENTIALS_FILE = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
    GMAIL_TOKEN_FILE = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
    GMAIL_SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.compose'
    ]
    
    # MCP Server Configuration
    MCP_SERVER_NAME = os.getenv('MCP_SERVER_NAME', 'gmail-mcp-server')
    MCP_SERVER_VERSION = os.getenv('MCP_SERVER_VERSION', '1.0.0')
    MCP_SERVER_DESCRIPTION = os.getenv('MCP_SERVER_DESCRIPTION', 'Gmail MCP Server for email operations')
    
    # Email Configuration
    DEFAULT_MAX_RESULTS = int(os.getenv('DEFAULT_MAX_RESULTS', '50'))
    DEFAULT_QUERY = os.getenv('DEFAULT_QUERY', 'in:inbox')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'gmail_mcp_server.log')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        # Check if credentials file exists
        if not Path(cls.GMAIL_CREDENTIALS_FILE).exists():
            raise FileNotFoundError(
                f"Gmail credentials file not found: {cls.GMAIL_CREDENTIALS_FILE}\n"
                "Please download your OAuth2 credentials from Google Cloud Console"
            )
        
        return True
    
    @classmethod
    def get_credentials_path(cls) -> Path:
        """Get absolute path to credentials file"""
        return Path(cls.GMAIL_CREDENTIALS_FILE).resolve()
    
    @classmethod
    def get_token_path(cls) -> Path:
        """Get absolute path to token file"""
        return Path(cls.GMAIL_TOKEN_FILE).resolve()
