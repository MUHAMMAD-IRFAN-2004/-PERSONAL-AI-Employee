#!/usr/bin/env python3
"""
Gmail Watcher - Bronze Tier Implementation

Monitors Gmail for unread important emails and creates action files.
This is a production-ready implementation for Bronze Tier completion.

Usage:
    python gmail_watcher.py

Requirements:
    pip install google-auth google-auth-oauthlib google-api-python-client

Setup:
    1. Enable Gmail API in Google Cloud Console
    2. Download credentials.json
    3. Run this script once to authenticate (creates token.json)
    4. Set VAULT_PATH in .env or pass as argument
"""

import os
import time
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Google API libraries not installed.")
    print("Run: pip install google-auth google-auth-oauthlib google-api-python-client")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gmail_watcher.log'),
        logging.StreamHandler()
    ]
)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Environment variables
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
VAULT_PATH = os.getenv('VAULT_PATH', 'AI_Employee_Vault')
CHECK_INTERVAL = int(os.getenv('GMAIL_CHECK_INTERVAL', '120'))  # seconds


class GmailWatcher:
    """
    Watches Gmail for unread important emails and creates action files.
    """
    
    def __init__(self, vault_path: str, credentials_path: str = 'credentials.json'):
        """
        Initialize Gmail Watcher.
        
        Args:
            vault_path: Path to Obsidian vault
            credentials_path: Path to Gmail API credentials
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.credentials_path = credentials_path
        self.token_path = 'token.json'
        self.processed_ids = set()
        self.service = None
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Load processed IDs from file if exists
        self.processed_file = Path('processed_emails.json')
        self._load_processed_ids()
        
        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Initialized GmailWatcher")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Check interval: {CHECK_INTERVAL}s")
        self.logger.info(f"DRY_RUN mode: {DRY_RUN}")
    
    def _load_processed_ids(self):
        """Load previously processed email IDs."""
        if self.processed_file.exists():
            try:
                with open(self.processed_file, 'r') as f:
                    data = json.load(f)
                    self.processed_ids = set(data.get('processed_ids', []))
                self.logger.info(f"Loaded {len(self.processed_ids)} processed email IDs")
            except Exception as e:
                self.logger.error(f"Error loading processed IDs: {e}")
    
    def _save_processed_ids(self):
        """Save processed email IDs to file."""
        try:
            with open(self.processed_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving processed IDs: {e}")
    
    def authenticate(self):
        """Authenticate with Gmail API."""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing Gmail API token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    self.logger.error(f"Credentials file not found: {self.credentials_path}")
                    self.logger.error("Download credentials.json from Google Cloud Console")
                    raise FileNotFoundError(f"Missing {self.credentials_path}")
                
                self.logger.info("Starting OAuth flow for Gmail API...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            self.logger.info("Gmail API token saved")
        
        # Build service
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail API authenticated successfully")
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check Gmail for new unread important emails.
        
        Returns:
            List of new messages to process
        """
        if not self.service:
            self.logger.error("Gmail service not authenticated")
            return []
        
        try:
            # Query for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            # Filter out already processed messages
            new_messages = [
                msg for msg in messages 
                if msg['id'] not in self.processed_ids
            ]
            
            if new_messages:
                self.logger.info(f"Found {len(new_messages)} new important email(s)")
            
            return new_messages
            
        except HttpError as error:
            self.logger.error(f"Gmail API error: {error}")
            return []
    
    def get_message_details(self, message_id: str) -> Dict[str, Any]:
        """
        Get full details of a message.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Message details
        """
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = {}
            for header in msg['payload'].get('headers', []):
                headers[header['name']] = header['value']
            
            # Get snippet
            snippet = msg.get('snippet', '')
            
            return {
                'id': message_id,
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', ''),
                'snippet': snippet,
                'thread_id': msg.get('threadId', ''),
                'labels': msg.get('labelIds', [])
            }
            
        except HttpError as error:
            self.logger.error(f"Error getting message {message_id}: {error}")
            return None
    
    def create_action_file(self, message: Dict[str, Any]) -> Path:
        """
        Create action file in Needs_Action folder.
        
        Args:
            message: Message details
            
        Returns:
            Path to created file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Clean subject for filename
        subject_clean = "".join(
            c if c.isalnum() or c in (' ', '_') else '_' 
            for c in message['subject']
        )[:50]
        
        filename = f"EMAIL_{timestamp}_{subject_clean}.md"
        filepath = self.needs_action / filename
        
        # Determine priority based on keywords
        priority = 'medium'
        urgent_keywords = ['urgent', 'asap', 'emergency', 'critical', 'immediate']
        if any(kw in message['subject'].lower() or kw in message['snippet'].lower() 
               for kw in urgent_keywords):
            priority = 'high'
        
        # Create markdown content
        content = f"""---
type: email
from: {message['from']}
to: {message['to']}
subject: {message['subject']}
date: {message['date']}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
message_id: {message['id']}
thread_id: {message['thread_id']}
---

## Email Details

**From**: {message['from']}  
**Subject**: {message['subject']}  
**Date**: {message['date']}  
**Priority**: {priority.upper()}

## Preview

{message['snippet']}

## Suggested Actions

- [ ] Read full email in Gmail
- [ ] Draft reply
- [ ] Forward to relevant party
- [ ] Add to calendar if meeting request
- [ ] Archive after processing

## Context

- **Labels**: {', '.join(message['labels'])}
- **Thread ID**: {message['thread_id']}
- **Message ID**: {message['id']}

## Notes

*Add your observations or decisions here*

---

**Detected by**: Gmail Watcher  
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if DRY_RUN:
            self.logger.info(f"[DRY RUN] Would create: {filename}")
            self.logger.info(f"[DRY RUN] Subject: {message['subject']}")
            self.logger.info(f"[DRY RUN] From: {message['from']}")
        else:
            filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"Created action file: {filename}")
        
        # Mark as processed
        self.processed_ids.add(message['id'])
        self._save_processed_ids()
        
        return filepath
    
    def run(self):
        """Main loop - continuously check for new emails."""
        self.logger.info("Starting Gmail Watcher main loop")
        self.logger.info(f"Checking every {CHECK_INTERVAL} seconds")
        
        # Authenticate
        try:
            self.authenticate()
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return
        
        # Main loop
        while True:
            try:
                # Check for new messages
                messages = self.check_for_updates()
                
                # Process each message
                for msg_summary in messages:
                    try:
                        # Get full message details
                        message = self.get_message_details(msg_summary['id'])
                        if message:
                            self.create_action_file(message)
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                
                if not messages:
                    self.logger.debug("No new important emails")
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)


def main():
    """Main entry point."""
    import sys
    
    # Get vault path from args or environment
    vault_path = VAULT_PATH
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    
    # Get credentials path
    credentials_path = 'credentials.json'
    if len(sys.argv) > 2:
        credentials_path = sys.argv[2]
    
    print(f"Gmail Watcher for AI Employee")
    print(f"=" * 50)
    print(f"Vault: {vault_path}")
    print(f"Credentials: {credentials_path}")
    print(f"DRY_RUN: {DRY_RUN}")
    print(f"Check Interval: {CHECK_INTERVAL}s")
    print(f"=" * 50)
    print()
    
    # Create watcher
    watcher = GmailWatcher(vault_path, credentials_path)
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n\nGmail Watcher stopped by user")
        watcher.logger.info("Watcher stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        watcher.logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
