# Gmail MCP Server

A comprehensive Model Context Protocol (MCP) server for Gmail operations, built with Python and ADK. This server provides a standardized interface for Gmail email operations that can be used by various AI agents and applications.

## Features

- **Complete Gmail Integration**: Full Gmail API integration with OAuth2 authentication
- **MCP Protocol**: Standardized Model Context Protocol for AI agent communication
- **Comprehensive Email Operations**: Read, send, search, delete, and manage emails
- **Advanced Search**: Support for Gmail's powerful search query syntax
- **Label Management**: Full support for Gmail labels and message organization
- **Attachment Support**: Send emails with file attachments
- **Error Handling**: Robust error handling and logging
- **Async Operations**: Fully asynchronous implementation for better performance

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail API credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project directory

4. **Run the authentication setup**:
   ```bash
   python setup_auth.py
   ```

## Quick Start

1. **Set up authentication**:
   ```bash
   python setup_auth.py
   ```

2. **Start the MCP server**:
   ```bash
   python mcp_server.py
   ```

3. **Connect your MCP client** to the server and start using Gmail tools!

## Available Tools

The Gmail MCP Server provides the following tools:

### Email Reading
- **`gmail_list_messages`**: List Gmail messages with optional filtering
- **`gmail_get_message`**: Get detailed information about a specific message
- **`gmail_search_messages`**: Search Gmail messages with detailed results

### Email Sending
- **`gmail_send_message`**: Send email messages with attachments support

### Email Management
- **`gmail_modify_message`**: Modify message labels (mark as read, star, etc.)
- **`gmail_delete_message`**: Delete Gmail messages
- **`gmail_mark_as_read`**: Mark messages as read
- **`gmail_mark_as_unread`**: Mark messages as unread
- **`gmail_star_message`**: Star messages
- **`gmail_unstar_message`**: Remove star from messages

### Labels and Organization
- **`gmail_get_labels`**: Get all Gmail labels

## Usage Examples

### List Recent Emails
```json
{
  "tool": "gmail_list_messages",
  "arguments": {
    "query": "in:inbox",
    "max_results": 10
  }
}
```

### Search for Specific Emails
```json
{
  "tool": "gmail_search_messages",
  "arguments": {
    "query": "from:boss@company.com subject:meeting",
    "max_results": 5
  }
}
```

### Send an Email
```json
{
  "tool": "gmail_send_message",
  "arguments": {
    "to": "recipient@example.com",
    "subject": "Important Meeting",
    "body": "Let's schedule a meeting for tomorrow.",
    "cc": ["colleague@example.com"],
    "attachments": ["/path/to/file.pdf"]
  }
}
```

### Mark Message as Read
```json
{
  "tool": "gmail_mark_as_read",
  "arguments": {
    "message_id": "message-id-here"
  }
}
```

## Gmail Search Query Examples

The server supports Gmail's powerful search query syntax:

- `in:inbox` - All messages in inbox
- `is:unread` - All unread messages
- `is:starred` - All starred messages
- `from:example@gmail.com` - Messages from specific sender
- `subject:meeting` - Messages with 'meeting' in subject
- `has:attachment` - Messages with attachments
- `label:important` - Messages with important label
- `after:2024/01/01` - Messages after specific date
- `newer_than:1d` - Messages newer than 1 day
- `is:unread AND from:boss@company.com` - Complex queries

## Configuration

The server can be configured using environment variables or a `.env` file:

```bash
# Gmail API Configuration
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json

# MCP Server Configuration
MCP_SERVER_NAME=gmail-mcp-server
MCP_SERVER_VERSION=1.0.0

# Email Configuration
DEFAULT_MAX_RESULTS=50
DEFAULT_QUERY=in:inbox

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=gmail_mcp_server.log
```

## Project Structure

```
gmail-mcp-server/
├── config.py              # Configuration management
├── gmail_client.py         # Gmail API client
├── mcp_server.py          # MCP server implementation
├── setup_auth.py          # Authentication setup
├── example_client.py      # Example MCP client usage
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables example
├── README.md             # This file
├── credentials.json      # Gmail OAuth2 credentials (you provide)
└── token.json           # OAuth2 token (auto-generated)
```

## Authentication

The server uses OAuth2 for Gmail API authentication:

1. **First-time setup**: Run `python setup_auth.py`
2. **Browser authentication**: The setup will open your browser for OAuth2 flow
3. **Token storage**: Authentication tokens are stored in `token.json`
4. **Automatic refresh**: Tokens are automatically refreshed when needed

## Error Handling

The server provides comprehensive error handling:

- **Authentication errors**: Clear messages for credential issues
- **API errors**: Detailed Gmail API error reporting
- **Validation errors**: Input parameter validation
- **Network errors**: Connection and timeout handling

## Logging

The server logs all operations to both console and file:

- **Console output**: Real-time operation status
- **Log file**: Detailed logs saved to `gmail_mcp_server.log`
- **Configurable levels**: DEBUG, INFO, WARNING, ERROR

## Security Considerations

- **OAuth2 authentication**: Secure Google OAuth2 flow
- **Token storage**: Local token storage with proper permissions
- **Scope limitation**: Minimal required Gmail API scopes
- **No credential exposure**: Credentials are never logged or exposed

## Troubleshooting

### Common Issues

1. **Authentication failed**:
   - Check if `credentials.json` exists and is valid
   - Ensure Gmail API is enabled in Google Cloud Console
   - Verify OAuth2 credentials are correct

2. **Permission denied**:
   - Check if the required Gmail API scopes are granted
   - Ensure the Gmail account has proper permissions

3. **Connection errors**:
   - Check internet connectivity
   - Verify Gmail API is accessible
   - Check firewall settings

### Debug Mode

Enable debug logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

## Development

### Running Tests
```bash
python example_client.py
```

### Adding New Tools

1. Add tool definition in `mcp_server.py`
2. Implement handler method
3. Add to tool routing logic
4. Update documentation

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the Gmail MCP Server.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Ensure all dependencies are installed
4. Verify Gmail API credentials are correct
