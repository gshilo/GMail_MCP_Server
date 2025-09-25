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

## Google Cloud Run Deployment

Deploy the Gmail MCP Server to Google Cloud Run for scalable, serverless operation.

### Prerequisites

1. **Google Cloud SDK**: Install and configure the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. **Docker**: Install [Docker](https://docs.docker.com/get-docker/) for containerization
3. **Google Cloud Project**: Create or select a Google Cloud project
4. **Gmail API**: Enable Gmail API in your Google Cloud project

### Step 1: Prepare for Cloud Run

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim

   # Set working directory
   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Create non-root user
   RUN useradd --create-home --shell /bin/bash app
   RUN chown -R app:app /app
   USER app

   # Expose port (Cloud Run uses PORT environment variable)
   EXPOSE 8080

   # Set environment variables
   ENV PORT=8080
   ENV PYTHONUNBUFFERED=1

   # Run the MCP server
   CMD ["python", "mcp_server.py"]
   ```

2. **Create a .dockerignore file**:
   ```
   __pycache__/
   *.pyc
   *.pyo
   *.pyd
   .git/
   .gitignore
   README.md
   .env
   env_example.txt
   test_server.py
   example_client.py
   setup_auth.py
   *.log
   ```

3. **Modify the MCP server for Cloud Run**:
   Create `mcp_server_cloud.py`:
   ```python
   # ... existing code ...
   
   # Add Cloud Run specific configuration
   import os
   from mcp.server.stdio import stdio_server
   
   class GmailMCPCloudServer(GmailMCPServer):
       def __init__(self):
           super().__init__()
           self.port = int(os.environ.get('PORT', 8080))
       
       async def run_cloud(self):
           """Run the MCP server for Cloud Run"""
           try:
               # Validate configuration
               self.config.validate()
               
               logger.info(f"Starting {GmailConfig.MCP_SERVER_NAME} v{GmailConfig.MCP_SERVER_VERSION} on port {self.port}")
               
               # For Cloud Run, we'll use stdio server
               async with stdio_server() as (read_stream, write_stream):
                   await self.server.run(
                       read_stream,
                       write_stream,
                       InitializationOptions(
                           server_name=GmailConfig.MCP_SERVER_NAME,
                           server_version=GmailConfig.MCP_SERVER_VERSION,
                           capabilities=self.server.get_capabilities(
                               notification_options=None,
                               experimental_capabilities={}
                           )
                       )
                   )
                   
           except Exception as e:
               logger.error(f"Error running MCP server: {e}")
               raise

   async def main():
       """Main function for Cloud Run"""
       server = GmailMCPCloudServer()
       await server.run_cloud()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

### Step 2: Set up Google Cloud Authentication

1. **Enable required APIs**:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable gmail.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Create a service account**:
   ```bash
   gcloud iam service-accounts create gmail-mcp-server \
       --display-name="Gmail MCP Server" \
       --description="Service account for Gmail MCP Server"
   ```

3. **Grant necessary permissions**:
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:gmail-mcp-server@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/gmail.readonly"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:gmail-mcp-server@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/gmail.send"
   ```

4. **Create and download service account key**:
   ```bash
   gcloud iam service-accounts keys create credentials.json \
       --iam-account=gmail-mcp-server@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

### Step 3: Configure for Cloud Run

1. **Update configuration for Cloud Run**:
   ```python
   # In config.py, add Cloud Run specific settings
   class GmailConfig:
       # ... existing code ...
       
       # Cloud Run specific configuration
       CLOUD_RUN_SERVICE_NAME = os.getenv('CLOUD_RUN_SERVICE_NAME', 'gmail-mcp-server')
       CLOUD_RUN_REGION = os.getenv('CLOUD_RUN_REGION', 'us-central1')
       CLOUD_RUN_MAX_INSTANCES = int(os.getenv('CLOUD_RUN_MAX_INSTANCES', '10'))
       CLOUD_RUN_MIN_INSTANCES = int(os.getenv('CLOUD_RUN_MIN_INSTANCES', '0'))
       CLOUD_RUN_CPU = os.getenv('CLOUD_RUN_CPU', '1')
       CLOUD_RUN_MEMORY = os.getenv('CLOUD_RUN_MEMORY', '512Mi')
   ```

2. **Create cloudbuild.yaml**:
   ```yaml
   steps:
     # Build the container image
     - name: 'gcr.io/cloud-builders/docker'
       args: ['build', '-t', 'gcr.io/$PROJECT_ID/gmail-mcp-server:$COMMIT_SHA', '.']
     
     # Push the container image to Container Registry
     - name: 'gcr.io/cloud-builders/docker'
       args: ['push', 'gcr.io/$PROJECT_ID/gmail-mcp-server:$COMMIT_SHA']
     
     # Deploy container image to Cloud Run
     - name: 'gcr.io/cloud-builders/gcloud'
       args:
       - 'run'
       - 'deploy'
       - 'gmail-mcp-server'
       - '--image'
       - 'gcr.io/$PROJECT_ID/gmail-mcp-server:$COMMIT_SHA'
       - '--region'
       - 'us-central1'
       - '--platform'
       - 'managed'
       - '--allow-unauthenticated'
       - '--memory'
       - '512Mi'
       - '--cpu'
       - '1'
       - '--max-instances'
       - '10'
       - '--min-instances'
       - '0'
       - '--set-env-vars'
       - 'GMAIL_CREDENTIALS_FILE=/app/credentials.json,LOG_LEVEL=INFO'
   ```

### Step 4: Deploy to Cloud Run

1. **Build and deploy using Cloud Build**:
   ```bash
   # Submit build to Cloud Build
   gcloud builds submit --config cloudbuild.yaml .
   ```

2. **Or deploy directly using gcloud**:
   ```bash
   # Build the container
   docker build -t gcr.io/YOUR_PROJECT_ID/gmail-mcp-server .
   
   # Push to Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/gmail-mcp-server
   
   # Deploy to Cloud Run
   gcloud run deploy gmail-mcp-server \
       --image gcr.io/YOUR_PROJECT_ID/gmail-mcp-server \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated \
       --memory 512Mi \
       --cpu 1 \
       --max-instances 10 \
       --min-instances 0 \
       --set-env-vars GMAIL_CREDENTIALS_FILE=/app/credentials.json,LOG_LEVEL=INFO
   ```

### Step 5: Configure Environment Variables

Set environment variables for your Cloud Run service:

```bash
gcloud run services update gmail-mcp-server \
    --region us-central1 \
    --set-env-vars \
    GMAIL_CREDENTIALS_FILE=/app/credentials.json,\
    GMAIL_TOKEN_FILE=/tmp/token.json,\
    MCP_SERVER_NAME=gmail-mcp-server,\
    MCP_SERVER_VERSION=1.0.0,\
    DEFAULT_MAX_RESULTS=50,\
    DEFAULT_QUERY=in:inbox,\
    LOG_LEVEL=INFO
```

### Step 6: Test the Deployment

1. **Get the service URL**:
   ```bash
   gcloud run services describe gmail-mcp-server \
       --region us-central1 \
       --format 'value(status.url)'
   ```

2. **Test the service**:
   ```bash
   curl -X POST https://YOUR_SERVICE_URL \
       -H "Content-Type: application/json" \
       -d '{"method": "tools/list", "params": {}}'
   ```

### Step 7: Monitor and Manage

1. **View logs**:
   ```bash
   gcloud logs read --service gmail-mcp-server --limit 50
   ```

2. **Update the service**:
   ```bash
   # After making changes, rebuild and redeploy
   gcloud builds submit --config cloudbuild.yaml .
   ```

3. **Scale the service**:
   ```bash
   gcloud run services update gmail-mcp-server \
       --region us-central1 \
       --max-instances 20 \
       --min-instances 1
   ```

### Cloud Run Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--memory` | Memory allocation | 512Mi |
| `--cpu` | CPU allocation | 1 |
| `--max-instances` | Maximum instances | 10 |
| `--min-instances` | Minimum instances | 0 |
| `--concurrency` | Requests per instance | 80 |
| `--timeout` | Request timeout | 300s |

### Security Considerations for Cloud Run

1. **Service Account**: Use a dedicated service account with minimal permissions
2. **Secrets Management**: Use Google Secret Manager for sensitive data
3. **VPC**: Configure VPC connector for private network access
4. **IAM**: Implement proper IAM policies
5. **HTTPS**: Cloud Run provides HTTPS by default

### Cost Optimization

1. **Set appropriate min/max instances**
2. **Use CPU allocation only when needed**
3. **Monitor usage with Cloud Monitoring**
4. **Set up billing alerts**

### Troubleshooting Cloud Run Deployment

1. **Check logs**: `gcloud logs read --service gmail-mcp-server`
2. **Verify environment variables**: Check Cloud Run service configuration
3. **Test locally**: Use `gcloud run deploy --source .` for local testing
4. **Check quotas**: Ensure you have sufficient Cloud Run quotas

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
