"""
Gmail API client for MCP server
"""
import os
import base64
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GmailConfig

logger = logging.getLogger(__name__)

class GmailClient:
    """Gmail API client for email operations"""
    
    def __init__(self, config: GmailConfig):
        self.config = config
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        try:
            # Load existing credentials
            if os.path.exists(self.config.get_token_path()):
                self.credentials = Credentials.from_authorized_user_file(
                    str(self.config.get_token_path()), 
                    self.config.GMAIL_SCOPES
                )
            
            # If there are no valid credentials, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.config.get_credentials_path()),
                        self.config.GMAIL_SCOPES
                    )
                    self.credentials = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open(self.config.get_token_path(), 'w') as token:
                    token.write(self.credentials.to_json())
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            logger.info("Successfully authenticated with Gmail API")
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Gmail API: {e}")
            raise
    
    def list_messages(self, query: str = None, max_results: int = None, 
                     label_ids: List[str] = None) -> List[Dict[str, Any]]:
        """
        List messages from Gmail
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results
            label_ids: List of label IDs to search
        
        Returns:
            List of message metadata
        """
        try:
            query = query or self.config.DEFAULT_QUERY
            max_results = max_results or self.config.DEFAULT_MAX_RESULTS
            
            # Call the Gmail API
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results,
                labelIds=label_ids
            ).execute()
            
            messages = results.get('messages', [])
            logger.info(f"Retrieved {len(messages)} messages")
            
            return messages
            
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            raise
        except Exception as e:
            logger.error(f"Error listing messages: {e}")
            raise
    
    def get_message(self, message_id: str, format: str = 'full') -> Dict[str, Any]:
        """
        Get a specific message by ID
        
        Args:
            message_id: Gmail message ID
            format: Message format (full, minimal, raw, metadata)
        
        Returns:
            Message data
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format=format
            ).execute()
            
            logger.info(f"Retrieved message {message_id}")
            return message
            
        except HttpError as error:
            logger.error(f"Gmail API error getting message {message_id}: {error}")
            raise
        except Exception as e:
            logger.error(f"Error getting message {message_id}: {e}")
            raise
    
    def get_message_details(self, message_id: str) -> Dict[str, Any]:
        """
        Get detailed message information
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Parsed message details
        """
        try:
            message = self.get_message(message_id, 'full')
            
            # Extract headers
            headers = message.get('payload', {}).get('headers', [])
            header_dict = {h['name']: h['value'] for h in headers}
            
            # Extract body
            body = self._extract_message_body(message.get('payload', {}))
            
            # Extract attachments
            attachments = self._extract_attachments(message.get('payload', {}))
            
            # Parse message details
            details = {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'label_ids': message.get('labelIds', []),
                'snippet': message.get('snippet', ''),
                'size_estimate': message.get('sizeEstimate', 0),
                'history_id': message.get('historyId'),
                'internal_date': message.get('internalDate'),
                'subject': header_dict.get('Subject', 'No Subject'),
                'from': header_dict.get('From', 'Unknown Sender'),
                'to': header_dict.get('To', 'Unknown Recipient'),
                'cc': header_dict.get('Cc', ''),
                'bcc': header_dict.get('Bcc', ''),
                'date': header_dict.get('Date', ''),
                'message_id': header_dict.get('Message-ID', ''),
                'body': body,
                'attachments': attachments,
                'is_read': 'UNREAD' not in message.get('labelIds', []),
                'is_starred': 'STARRED' in message.get('labelIds', []),
                'is_important': 'IMPORTANT' in message.get('labelIds', [])
            }
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting message details for {message_id}: {e}")
            raise
    
    def send_message(self, to: str, subject: str, body: str, 
                    cc: List[str] = None, bcc: List[str] = None,
                    attachments: List[str] = None, 
                    html_body: str = None) -> Dict[str, Any]:
        """
        Send an email message
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of file paths to attach
            html_body: HTML version of the body
        
        Returns:
            Send result
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = ', '.join(cc)
            if bcc:
                message['bcc'] = ', '.join(bcc)
            
            # Add text part
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                message.attach(html_part)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        message.attach(part)
                    except Exception as e:
                        logger.warning(f"Failed to attach {file_path}: {e}")
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            logger.info(f"Message sent successfully: {result.get('id')}")
            return {
                'success': True,
                'message_id': result.get('id'),
                'thread_id': result.get('threadId'),
                'to': to,
                'subject': subject
            }
            
        except HttpError as error:
            logger.error(f"Gmail API error sending message: {error}")
            return {
                'success': False,
                'error': str(error),
                'to': to,
                'subject': subject
            }
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {
                'success': False,
                'error': str(e),
                'to': to,
                'subject': subject
            }
    
    def modify_message(self, message_id: str, add_label_ids: List[str] = None,
                      remove_label_ids: List[str] = None) -> Dict[str, Any]:
        """
        Modify message labels
        
        Args:
            message_id: Gmail message ID
            add_label_ids: Labels to add
            remove_label_ids: Labels to remove
        
        Returns:
            Modification result
        """
        try:
            body = {}
            if add_label_ids:
                body['addLabelIds'] = add_label_ids
            if remove_label_ids:
                body['removeLabelIds'] = remove_label_ids
            
            result = self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
            
            logger.info(f"Message {message_id} modified successfully")
            return {
                'success': True,
                'message_id': message_id,
                'result': result
            }
            
        except HttpError as error:
            logger.error(f"Gmail API error modifying message {message_id}: {error}")
            return {
                'success': False,
                'error': str(error),
                'message_id': message_id
            }
        except Exception as e:
            logger.error(f"Error modifying message {message_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message_id': message_id
            }
    
    def delete_message(self, message_id: str) -> Dict[str, Any]:
        """
        Delete a message
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Deletion result
        """
        try:
            self.service.users().messages().delete(
                userId='me',
                id=message_id
            ).execute()
            
            logger.info(f"Message {message_id} deleted successfully")
            return {
                'success': True,
                'message_id': message_id
            }
            
        except HttpError as error:
            logger.error(f"Gmail API error deleting message {message_id}: {error}")
            return {
                'success': False,
                'error': str(error),
                'message_id': message_id
            }
        except Exception as e:
            logger.error(f"Error deleting message {message_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message_id': message_id
            }
    
    def get_labels(self) -> List[Dict[str, Any]]:
        """
        Get all Gmail labels
        
        Returns:
            List of label information
        """
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            logger.info(f"Retrieved {len(labels)} labels")
            return labels
            
        except HttpError as error:
            logger.error(f"Gmail API error getting labels: {error}")
            raise
        except Exception as e:
            logger.error(f"Error getting labels: {e}")
            raise
    
    def search_messages(self, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        """
        Search messages with detailed results
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results
        
        Returns:
            List of detailed message information
        """
        try:
            # Get message IDs
            messages = self.list_messages(query, max_results)
            
            # Get detailed information for each message
            detailed_messages = []
            for message in messages:
                try:
                    details = self.get_message_details(message['id'])
                    detailed_messages.append(details)
                except Exception as e:
                    logger.warning(f"Failed to get details for message {message['id']}: {e}")
                    continue
            
            logger.info(f"Retrieved details for {len(detailed_messages)} messages")
            return detailed_messages
            
        except Exception as e:
            logger.error(f"Error searching messages: {e}")
            raise
    
    def _extract_message_body(self, payload: Dict[str, Any]) -> str:
        """Extract message body from payload"""
        body = ""
        
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            # Single part message
            if payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def _extract_attachments(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract attachment information from payload"""
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachment = {
                        'filename': part['filename'],
                        'mime_type': part['mimeType'],
                        'size': part['body'].get('size', 0),
                        'attachment_id': part['body'].get('attachmentId')
                    }
                    attachments.append(attachment)
        
        return attachments
