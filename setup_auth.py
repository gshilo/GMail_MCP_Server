#!/usr/bin/env python3
"""
Setup script for Gmail MCP Server authentication
"""
import os
import json
import webbrowser
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import GmailConfig

def setup_authentication():
    """Setup Gmail API authentication"""
    print("Gmail MCP Server Authentication Setup")
    print("=" * 40)
    
    config = GmailConfig()
    
    # Check if credentials file exists
    credentials_path = config.get_credentials_path()
    if not credentials_path.exists():
        print("❌ Gmail credentials file not found!")
        print(f"Expected location: {credentials_path}")
        print("\nTo get credentials:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a new project or select existing one")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop application)")
        print("5. Download the credentials JSON file")
        print(f"6. Save it as: {credentials_path}")
        return False
    
    print(f"✅ Found credentials file: {credentials_path}")
    
    # Check if token file exists
    token_path = config.get_token_path()
    
    try:
        # Try to load existing credentials
        if token_path.exists():
            print(f"✅ Found existing token file: {token_path}")
            credentials = Credentials.from_authorized_user_file(
                str(token_path), 
                config.GMAIL_SCOPES
            )
            
            if credentials and credentials.valid:
                print("✅ Existing credentials are valid")
                return True
            elif credentials and credentials.expired and credentials.refresh_token:
                print("🔄 Refreshing expired credentials...")
                credentials.refresh(Request())
                
                # Save refreshed credentials
                with open(token_path, 'w') as token:
                    token.write(credentials.to_json())
                print("✅ Credentials refreshed successfully")
                return True
        
        # Get new credentials
        print("🔄 Getting new credentials...")
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path),
            config.GMAIL_SCOPES
        )
        
        # Run the OAuth flow
        credentials = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_path, 'w') as token:
            token.write(credentials.to_json())
        
        print("✅ Authentication successful!")
        print(f"✅ Token saved to: {token_path}")
        
        # Test the connection
        print("\n🧪 Testing Gmail API connection...")
        service = build('gmail', 'v1', credentials=credentials)
        
        # Get user profile
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Connected to Gmail account: {profile.get('emailAddress')}")
        print(f"✅ Total messages: {profile.get('messagesTotal', 0)}")
        print(f"✅ Total threads: {profile.get('threadsTotal', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def create_sample_credentials():
    """Create a sample credentials file template"""
    sample_credentials = {
        "installed": {
            "client_id": "your-client-id.apps.googleusercontent.com",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your-client-secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    credentials_path = GmailConfig.get_credentials_path()
    
    try:
        with open(credentials_path, 'w') as f:
            json.dump(sample_credentials, f, indent=2)
        
        print(f"✅ Created sample credentials file: {credentials_path}")
        print("📝 Please replace the sample values with your actual OAuth2 credentials")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample credentials file: {e}")
        return False

def main():
    """Main setup function"""
    print("Gmail MCP Server Setup")
    print("=" * 30)
    
    # Check if credentials file exists
    config = GmailConfig()
    credentials_path = config.get_credentials_path()
    
    if not credentials_path.exists():
        print("No credentials file found. Creating sample...")
        if create_sample_credentials():
            print("\nPlease follow these steps:")
            print("1. Go to Google Cloud Console")
            print("2. Create OAuth2 credentials")
            print("3. Replace the sample values in credentials.json")
            print("4. Run this script again")
        return False
    
    # Setup authentication
    if setup_authentication():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python mcp_server.py' to start the MCP server")
        print("2. Use the MCP client to connect to the server")
        print("3. Start using Gmail tools!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()
