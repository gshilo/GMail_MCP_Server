#!/usr/bin/env python3
"""
Example MCP client for Gmail operations
"""
import asyncio
import json
from typing import Dict, Any

# This is a simplified example - in practice, you would use an MCP client library
class GmailMCPClient:
    """Example MCP client for Gmail operations"""
    
    def __init__(self, server_process):
        self.server_process = server_process
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a Gmail tool via MCP"""
        # This is a simplified example
        # In practice, you would use proper MCP client communication
        print(f"Calling tool: {tool_name}")
        print(f"Arguments: {json.dumps(arguments, indent=2)}")
        
        # Simulate tool call result
        return {
            "success": True,
            "result": f"Tool {tool_name} executed successfully"
        }

async def example_gmail_operations():
    """Example Gmail operations using MCP"""
    print("Gmail MCP Server Example")
    print("=" * 30)
    
    # Initialize client (simplified)
    client = GmailMCPClient(None)
    
    print("\n1. Listing recent emails...")
    result = await client.call_tool("gmail_list_messages", {
        "query": "in:inbox",
        "max_results": 10
    })
    print(f"Result: {result}")
    
    print("\n2. Searching for emails from specific sender...")
    result = await client.call_tool("gmail_search_messages", {
        "query": "from:example@gmail.com",
        "max_results": 5
    })
    print(f"Result: {result}")
    
    print("\n3. Getting detailed message information...")
    result = await client.call_tool("gmail_get_message", {
        "message_id": "sample-message-id"
    })
    print(f"Result: {result}")
    
    print("\n4. Sending an email...")
    result = await client.call_tool("gmail_send_message", {
        "to": "recipient@example.com",
        "subject": "Test Email from MCP",
        "body": "This is a test email sent via Gmail MCP Server",
        "cc": ["cc@example.com"]
    })
    print(f"Result: {result}")
    
    print("\n5. Marking message as read...")
    result = await client.call_tool("gmail_mark_as_read", {
        "message_id": "sample-message-id"
    })
    print(f"Result: {result}")
    
    print("\n6. Starring a message...")
    result = await client.call_tool("gmail_star_message", {
        "message_id": "sample-message-id"
    })
    print(f"Result: {result}")
    
    print("\n7. Getting Gmail labels...")
    result = await client.call_tool("gmail_get_labels", {})
    print(f"Result: {result}")
    
    print("\n8. Deleting a message...")
    result = await client.call_tool("gmail_delete_message", {
        "message_id": "sample-message-id"
    })
    print(f"Result: {result}")

def print_available_tools():
    """Print available Gmail MCP tools"""
    tools = [
        {
            "name": "gmail_list_messages",
            "description": "List Gmail messages with optional filtering",
            "parameters": ["query", "max_results", "label_ids"]
        },
        {
            "name": "gmail_get_message",
            "description": "Get detailed information about a specific Gmail message",
            "parameters": ["message_id"]
        },
        {
            "name": "gmail_search_messages",
            "description": "Search Gmail messages and return detailed results",
            "parameters": ["query", "max_results"]
        },
        {
            "name": "gmail_send_message",
            "description": "Send an email message",
            "parameters": ["to", "subject", "body", "cc", "bcc", "attachments", "html_body"]
        },
        {
            "name": "gmail_modify_message",
            "description": "Modify message labels (mark as read, star, etc.)",
            "parameters": ["message_id", "add_label_ids", "remove_label_ids"]
        },
        {
            "name": "gmail_delete_message",
            "description": "Delete a Gmail message",
            "parameters": ["message_id"]
        },
        {
            "name": "gmail_get_labels",
            "description": "Get all Gmail labels",
            "parameters": []
        },
        {
            "name": "gmail_mark_as_read",
            "description": "Mark a message as read",
            "parameters": ["message_id"]
        },
        {
            "name": "gmail_mark_as_unread",
            "description": "Mark a message as unread",
            "parameters": ["message_id"]
        },
        {
            "name": "gmail_star_message",
            "description": "Star a message",
            "parameters": ["message_id"]
        },
        {
            "name": "gmail_unstar_message",
            "description": "Remove star from a message",
            "parameters": ["message_id"]
        }
    ]
    
    print("Available Gmail MCP Tools:")
    print("=" * 40)
    
    for tool in tools:
        print(f"\n{tool['name']}")
        print(f"  Description: {tool['description']}")
        print(f"  Parameters: {', '.join(tool['parameters']) if tool['parameters'] else 'None'}")

def print_gmail_query_examples():
    """Print Gmail search query examples"""
    examples = [
        ("in:inbox", "All messages in inbox"),
        ("is:unread", "All unread messages"),
        ("is:starred", "All starred messages"),
        ("from:example@gmail.com", "Messages from specific sender"),
        ("to:me", "Messages sent to me"),
        ("subject:meeting", "Messages with 'meeting' in subject"),
        ("has:attachment", "Messages with attachments"),
        ("label:important", "Messages with important label"),
        ("after:2024/01/01", "Messages after specific date"),
        ("before:2024/12/31", "Messages before specific date"),
        ("newer_than:1d", "Messages newer than 1 day"),
        ("older_than:1w", "Messages older than 1 week"),
        ("is:read", "All read messages"),
        ("is:unread AND from:boss@company.com", "Unread messages from boss"),
        ("subject:urgent OR label:urgent", "Urgent messages"),
        ("has:attachment AND from:client@example.com", "Attachments from client")
    ]
    
    print("\nGmail Search Query Examples:")
    print("=" * 40)
    
    for query, description in examples:
        print(f"  {query:<40} - {description}")

async def main():
    """Main function"""
    print("Gmail MCP Server Examples")
    print("=" * 50)
    
    print_available_tools()
    print_gmail_query_examples()
    
    print("\n" + "=" * 50)
    print("Example Operations:")
    await example_gmail_operations()
    
    print("\n" + "=" * 50)
    print("To use the Gmail MCP Server:")
    print("1. Run 'python setup_auth.py' to set up authentication")
    print("2. Run 'python mcp_server.py' to start the MCP server")
    print("3. Connect your MCP client to the server")
    print("4. Use the available tools for Gmail operations")

if __name__ == "__main__":
    asyncio.run(main())
