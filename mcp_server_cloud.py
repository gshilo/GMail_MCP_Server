"""
MCP Server for Gmail operations - Cloud Run version
"""
import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from config import GmailConfig
from gmail_client import GmailClient

# Configure logging
logging.basicConfig(
    level=getattr(logging, GmailConfig.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GmailMCPCloudServer:
    """MCP Server for Gmail operations - Cloud Run optimized"""
    
    def __init__(self):
        self.config = GmailConfig()
        self.gmail_client = None
        self.server = Server(GmailConfig.MCP_SERVER_NAME)
        self.port = int(os.environ.get('PORT', 8080))
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available Gmail tools"""
            tools = [
                Tool(
                    name="gmail_list_messages",
                    description="List Gmail messages with optional filtering",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Gmail search query (e.g., 'in:inbox', 'from:example@gmail.com', 'subject:meeting')",
                                "default": "in:inbox"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of messages to return",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 500
                            },
                            "label_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of label IDs to search in"
                            }
                        }
                    }
                ),
                Tool(
                    name="gmail_get_message",
                    description="Get detailed information about a specific Gmail message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_search_messages",
                    description="Search Gmail messages and return detailed results",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Gmail search query"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of messages to return",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 500
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="gmail_send_message",
                    description="Send an email message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient email address"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject"
                            },
                            "body": {
                                "type": "string",
                                "description": "Email body (plain text)"
                            },
                            "cc": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "CC recipients"
                            },
                            "bcc": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "BCC recipients"
                            },
                            "attachments": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of file paths to attach"
                            },
                            "html_body": {
                                "type": "string",
                                "description": "HTML version of the email body"
                            }
                        },
                        "required": ["to", "subject", "body"]
                    }
                ),
                Tool(
                    name="gmail_modify_message",
                    description="Modify message labels (mark as read, star, etc.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            },
                            "add_label_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Labels to add to the message"
                            },
                            "remove_label_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Labels to remove from the message"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_delete_message",
                    description="Delete a Gmail message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_get_labels",
                    description="Get all Gmail labels",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="gmail_mark_as_read",
                    description="Mark a message as read",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_mark_as_unread",
                    description="Mark a message as unread",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_star_message",
                    description="Star a message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
                Tool(
                    name="gmail_unstar_message",
                    description="Remove star from a message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["message_id"]
                    }
                )
            ]
            
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            try:
                # Initialize Gmail client if not already done
                if self.gmail_client is None:
                    self.gmail_client = GmailClient(self.config)
                
                # Route to appropriate handler
                if name == "gmail_list_messages":
                    return await self._handle_list_messages(arguments)
                elif name == "gmail_get_message":
                    return await self._handle_get_message(arguments)
                elif name == "gmail_search_messages":
                    return await self._handle_search_messages(arguments)
                elif name == "gmail_send_message":
                    return await self._handle_send_message(arguments)
                elif name == "gmail_modify_message":
                    return await self._handle_modify_message(arguments)
                elif name == "gmail_delete_message":
                    return await self._handle_delete_message(arguments)
                elif name == "gmail_get_labels":
                    return await self._handle_get_labels(arguments)
                elif name == "gmail_mark_as_read":
                    return await self._handle_mark_as_read(arguments)
                elif name == "gmail_mark_as_unread":
                    return await self._handle_mark_as_unread(arguments)
                elif name == "gmail_star_message":
                    return await self._handle_star_message(arguments)
                elif name == "gmail_unstar_message":
                    return await self._handle_unstar_message(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                        isError=True
                    )
                    
            except Exception as e:
                logger.error(f"Error handling tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
    
    async def _handle_list_messages(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle list messages tool"""
        try:
            query = arguments.get("query", "in:inbox")
            max_results = arguments.get("max_results", 50)
            label_ids = arguments.get("label_ids")
            
            messages = self.gmail_client.list_messages(
                query=query,
                max_results=max_results,
                label_ids=label_ids
            )
            
            result_text = f"Found {len(messages)} messages\n\n"
            for i, message in enumerate(messages[:10], 1):  # Show first 10
                result_text += f"{i}. Message ID: {message['id']}\n"
                result_text += f"   Thread ID: {message.get('threadId', 'N/A')}\n\n"
            
            if len(messages) > 10:
                result_text += f"... and {len(messages) - 10} more messages\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=False
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error listing messages: {str(e)}")],
                isError=True
            )
    
    async def _handle_get_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get message tool"""
        try:
            message_id = arguments["message_id"]
            message_details = self.gmail_client.get_message_details(message_id)
            
            result_text = f"Message Details:\n"
            result_text += f"ID: {message_details['id']}\n"
            result_text += f"Subject: {message_details['subject']}\n"
            result_text += f"From: {message_details['from']}\n"
            result_text += f"To: {message_details['to']}\n"
            result_text += f"Date: {message_details['date']}\n"
            result_text += f"Read: {message_details['is_read']}\n"
            result_text += f"Starred: {message_details['is_starred']}\n"
            result_text += f"Important: {message_details['is_important']}\n"
            result_text += f"Snippet: {message_details['snippet']}\n"
            result_text += f"\nBody:\n{message_details['body']}\n"
            
            if message_details['attachments']:
                result_text += f"\nAttachments:\n"
                for att in message_details['attachments']:
                    result_text += f"- {att['filename']} ({att['mime_type']})\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=False
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting message: {str(e)}")],
                isError=True
            )
    
    async def _handle_search_messages(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle search messages tool"""
        try:
            query = arguments["query"]
            max_results = arguments.get("max_results", 50)
            
            messages = self.gmail_client.search_messages(query, max_results)
            
            result_text = f"Search Results for '{query}':\n"
            result_text += f"Found {len(messages)} messages\n\n"
            
            for i, message in enumerate(messages[:10], 1):  # Show first 10
                result_text += f"{i}. {message['subject']}\n"
                result_text += f"   From: {message['from']}\n"
                result_text += f"   Date: {message['date']}\n"
                result_text += f"   ID: {message['id']}\n"
                result_text += f"   Snippet: {message['snippet'][:100]}...\n\n"
            
            if len(messages) > 10:
                result_text += f"... and {len(messages) - 10} more messages\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=False
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error searching messages: {str(e)}")],
                isError=True
            )
    
    async def _handle_send_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle send message tool"""
        try:
            to = arguments["to"]
            subject = arguments["subject"]
            body = arguments["body"]
            cc = arguments.get("cc", [])
            bcc = arguments.get("bcc", [])
            attachments = arguments.get("attachments", [])
            html_body = arguments.get("html_body")
            
            result = self.gmail_client.send_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                html_body=html_body
            )
            
            if result['success']:
                result_text = f"Message sent successfully!\n"
                result_text += f"Message ID: {result['message_id']}\n"
                result_text += f"Thread ID: {result['thread_id']}\n"
                result_text += f"To: {result['to']}\n"
                result_text += f"Subject: {result['subject']}\n"
            else:
                result_text = f"Failed to send message: {result['error']}\n"
                result_text += f"To: {result['to']}\n"
                result_text += f"Subject: {result['subject']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=not result['success']
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error sending message: {str(e)}")],
                isError=True
            )
    
    async def _handle_modify_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle modify message tool"""
        try:
            message_id = arguments["message_id"]
            add_label_ids = arguments.get("add_label_ids", [])
            remove_label_ids = arguments.get("remove_label_ids", [])
            
            result = self.gmail_client.modify_message(
                message_id=message_id,
                add_label_ids=add_label_ids,
                remove_label_ids=remove_label_ids
            )
            
            if result['success']:
                result_text = f"Message {message_id} modified successfully\n"
                if add_label_ids:
                    result_text += f"Added labels: {', '.join(add_label_ids)}\n"
                if remove_label_ids:
                    result_text += f"Removed labels: {', '.join(remove_label_ids)}\n"
            else:
                result_text = f"Failed to modify message: {result['error']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=not result['success']
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error modifying message: {str(e)}")],
                isError=True
            )
    
    async def _handle_delete_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle delete message tool"""
        try:
            message_id = arguments["message_id"]
            result = self.gmail_client.delete_message(message_id)
            
            if result['success']:
                result_text = f"Message {message_id} deleted successfully\n"
            else:
                result_text = f"Failed to delete message: {result['error']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=not result['success']
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error deleting message: {str(e)}")],
                isError=True
            )
    
    async def _handle_get_labels(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get labels tool"""
        try:
            labels = self.gmail_client.get_labels()
            
            result_text = f"Gmail Labels ({len(labels)} total):\n\n"
            for label in labels:
                result_text += f"- {label['name']} (ID: {label['id']})\n"
                result_text += f"  Type: {label['type']}\n"
                if 'messagesTotal' in label:
                    result_text += f"  Messages: {label['messagesTotal']}\n"
                if 'messagesUnread' in label:
                    result_text += f"  Unread: {label['messagesUnread']}\n"
                result_text += "\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)],
                isError=False
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting labels: {str(e)}")],
                isError=True
            )
    
    async def _handle_mark_as_read(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle mark as read tool"""
        return await self._handle_modify_message({
            "message_id": arguments["message_id"],
            "remove_label_ids": ["UNREAD"]
        })
    
    async def _handle_mark_as_unread(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle mark as unread tool"""
        return await self._handle_modify_message({
            "message_id": arguments["message_id"],
            "add_label_ids": ["UNREAD"]
        })
    
    async def _handle_star_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle star message tool"""
        return await self._handle_modify_message({
            "message_id": arguments["message_id"],
            "add_label_ids": ["STARRED"]
        })
    
    async def _handle_unstar_message(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle unstar message tool"""
        return await self._handle_modify_message({
            "message_id": arguments["message_id"],
            "remove_label_ids": ["STARRED"]
        })
    
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
