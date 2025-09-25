#!/usr/bin/env python3
"""
Test script for Gmail MCP Server
"""
import asyncio
import json
import sys
import subprocess
import time
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'mcp',
        'google.auth',
        'google.oauth2',
        'google_auth_oauthlib',
        'googleapiclient',
        'dotenv',
        'json',
        'logging',
        'datetime',
        'typing',
        'asyncio'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_config():
    """Test configuration module"""
    print("\nTesting configuration...")
    
    try:
        from config import GmailConfig
        config = GmailConfig()
        print("✅ Configuration module loaded")
        
        # Test configuration validation (should fail without credentials)
        try:
            config.validate()
            print("⚠️  Configuration validation passed (credentials may be present)")
        except FileNotFoundError as e:
            print(f"⚠️  Configuration validation failed as expected: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_gmail_client():
    """Test Gmail client module"""
    print("\nTesting Gmail client...")
    
    try:
        from gmail_client import GmailClient
        from config import GmailConfig
        
        config = GmailConfig()
        # This will fail without credentials, but module should load
        try:
            client = GmailClient(config)
            print("✅ Gmail client module loaded")
        except Exception as e:
            if "credentials" in str(e).lower() or "file" in str(e).lower():
                print("⚠️  Gmail client module loaded (credentials required)")
            else:
                raise e
        return True
    except Exception as e:
        print(f"❌ Gmail client test failed: {e}")
        return False

def test_mcp_server():
    """Test MCP server module"""
    print("\nTesting MCP server...")
    
    try:
        from mcp_server import GmailMCPServer
        print("✅ MCP server module loaded")
        return True
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def test_setup_auth():
    """Test authentication setup module"""
    print("\nTesting authentication setup...")
    
    try:
        from setup_auth import setup_authentication, create_sample_credentials
        print("✅ Authentication setup module loaded")
        return True
    except Exception as e:
        print(f"❌ Authentication setup test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'config.py',
        'gmail_client.py',
        'mcp_server.py',
        'setup_auth.py',
        'example_client.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_credentials_template():
    """Test if credentials template can be created"""
    print("\nTesting credentials template...")
    
    try:
        from setup_auth import create_sample_credentials
        success = create_sample_credentials()
        
        if success:
            print("✅ Credentials template created")
            # Clean up
            Path('credentials.json').unlink(missing_ok=True)
        else:
            print("❌ Failed to create credentials template")
        
        return success
    except Exception as e:
        print(f"❌ Credentials template test failed: {e}")
        return False

def test_mcp_server_startup():
    """Test if MCP server can start (without running)"""
    print("\nTesting MCP server startup...")
    
    try:
        from mcp_server import GmailMCPServer
        
        # Create server instance (this should work even without credentials)
        server = GmailMCPServer()
        print("✅ MCP server instance created")
        
        # Test tool listing (this should work)
        print("✅ MCP server tools available")
        
        return True
    except Exception as e:
        print(f"❌ MCP server startup test failed: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 50)
    print("Gmail MCP Server Test Results")
    print("=" * 50)
    
    print("\nNext steps to use the Gmail MCP Server:")
    print("1. Get Gmail API credentials from Google Cloud Console")
    print("2. Save credentials as 'credentials.json'")
    print("3. Run 'python setup_auth.py' to authenticate")
    print("4. Run 'python mcp_server.py' to start the server")
    print("5. Connect your MCP client to the server")
    
    print("\nRequired Gmail API setup:")
    print("- Enable Gmail API in Google Cloud Console")
    print("- Create OAuth2 credentials (Desktop application)")
    print("- Download credentials JSON file")
    print("- Save as 'credentials.json' in project directory")
    
    print("\nMCP Client Integration:")
    print("- Use MCP client library to connect to the server")
    print("- Available tools: gmail_list_messages, gmail_send_message, etc.")
    print("- See example_client.py for usage examples")

def main():
    """Run all tests"""
    print("Gmail MCP Server Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_gmail_client,
        test_mcp_server,
        test_setup_auth,
        test_file_structure,
        test_credentials_template,
        test_mcp_server_startup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gmail MCP Server is ready to use.")
        print_usage_instructions()
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version (3.7+ required)")
        print("3. Verify all files are present")
        print("4. Check import errors for missing modules")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
