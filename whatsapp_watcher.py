"""
WhatsApp Web Watcher - Silver Tier
===================================
Monitors WhatsApp Web for important messages and creates action files.

Features:
- Persistent browser sessions with authentication
- QR code authentication handling
- Keyword-based importance detection
- Automatic action file creation
- Error handling and recovery
- Comprehensive logging

Author: AI Employee System
Version: 1.0.0
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import re

try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("WARNING: python-dotenv not installed. Run: pip install python-dotenv")
    load_dotenv = lambda: None

# Load environment variables
load_dotenv()

# ========================================
# Configuration
# ========================================

class Config:
    """Configuration for WhatsApp Watcher"""
    
    # Directories
    BASE_DIR = Path(__file__).parent
    VAULT_DIR = BASE_DIR / "AI_Employee_Vault"
    NEEDS_ACTION_DIR = VAULT_DIR / "Needs_Action"
    LOGS_DIR = VAULT_DIR / "Logs"
    
    # Browser settings
    BROWSER_USER_DATA_DIR = BASE_DIR / ".whatsapp_browser_data"
    HEADLESS = os.getenv("WHATSAPP_HEADLESS", "false").lower() == "true"
    
    # WhatsApp Web URL
    WHATSAPP_URL = "https://web.whatsapp.com"
    
    # Monitoring settings
    CHECK_INTERVAL = int(os.getenv("WHATSAPP_CHECK_INTERVAL", "30"))  # seconds
    MAX_MESSAGES_PER_CHECK = int(os.getenv("WHATSAPP_MAX_MESSAGES", "50"))
    
    # Important keywords (case-insensitive)
    IMPORTANT_KEYWORDS = [
        "urgent", "asap", "emergency", "critical", "important",
        "payment", "invoice", "deadline", "meeting", "call",
        "help", "please respond", "need", "required",
        "approval", "confirm", "verify", "check",
        "problem", "issue", "error", "bug", "broken"
    ]
    
    # High priority senders (names or numbers)
    PRIORITY_SENDERS = os.getenv("WHATSAPP_PRIORITY_SENDERS", "").split(",")
    PRIORITY_SENDERS = [s.strip() for s in PRIORITY_SENDERS if s.strip()]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / f"whatsapp_watcher_{datetime.now().strftime('%Y%m%d')}.log"


# ========================================
# Logging Setup
# ========================================

def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("WhatsAppWatcher")
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # File handler
    fh = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


logger = setup_logging()


# ========================================
# Message Processing
# ========================================

class Message:
    """Represents a WhatsApp message"""
    
    def __init__(self, sender: str, text: str, timestamp: str, chat_name: str = ""):
        self.sender = sender
        self.text = text
        self.timestamp = timestamp
        self.chat_name = chat_name
        self.importance_score = 0
        self.matched_keywords = []
        
    def calculate_importance(self) -> int:
        """Calculate importance score based on keywords and sender"""
        score = 0
        text_lower = self.text.lower()
        
        # Check for important keywords
        for keyword in Config.IMPORTANT_KEYWORDS:
            if keyword.lower() in text_lower:
                score += 10
                self.matched_keywords.append(keyword)
        
        # Check for priority senders
        for priority_sender in Config.PRIORITY_SENDERS:
            if priority_sender.lower() in self.sender.lower():
                score += 20
                break
        
        # Check for question marks (questions need responses)
        if "?" in self.text:
            score += 5
        
        # Check for all caps (urgency indicator)
        if self.text.isupper() and len(self.text) > 10:
            score += 10
        
        # Check for multiple exclamation marks
        if self.text.count("!") >= 2:
            score += 5
        
        self.importance_score = score
        return score
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            "sender": self.sender,
            "text": self.text,
            "timestamp": self.timestamp,
            "chat_name": self.chat_name,
            "importance_score": self.importance_score,
            "matched_keywords": self.matched_keywords
        }


# ========================================
# WhatsApp Web Interface
# ========================================

class WhatsAppWatcher:
    """Main WhatsApp watcher class"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.seen_messages: Set[str] = set()
        self.is_authenticated = False
        
        # Ensure directories exist
        Config.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        Config.BROWSER_USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("WhatsApp Watcher initialized")
    
    def start_browser(self) -> bool:
        """Start browser with persistent session"""
        try:
            logger.info("Starting browser...")
            self.playwright = sync_playwright().start()
            
            # Launch browser with persistent context (saves session)
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(Config.BROWSER_USER_DATA_DIR),
                headless=Config.HEADLESS,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ],
                viewport={'width': 1280, 'height': 720}
            )
            
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
            
            logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    def navigate_to_whatsapp(self) -> bool:
        """Navigate to WhatsApp Web"""
        try:
            logger.info(f"Navigating to {Config.WHATSAPP_URL}")
            self.page.goto(Config.WHATSAPP_URL, timeout=60000)
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to WhatsApp: {e}")
            return False
    
    def check_authentication(self) -> bool:
        """Check if user is authenticated"""
        try:
            # Wait a bit for page to load
            time.sleep(2)
            
            # Check for QR code (means not authenticated)
            qr_code = self.page.query_selector('canvas[aria-label="Scan this QR code to link a device!"]')
            if qr_code:
                logger.warning("Not authenticated - QR code present")
                self.is_authenticated = False
                return False
            
            # Check for main chat area (means authenticated)
            chat_area = self.page.query_selector('[data-testid="conversation-panel-body"]')
            if chat_area:
                logger.info("Authenticated - chat area found")
                self.is_authenticated = True
                return True
            
            # Check for side pane (alternative check)
            side_pane = self.page.query_selector('#pane-side')
            if side_pane:
                logger.info("Authenticated - side pane found")
                self.is_authenticated = True
                return True
            
            logger.warning("Authentication status unclear")
            return False
            
        except Exception as e:
            logger.error(f"Error checking authentication: {e}")
            return False
    
    def wait_for_authentication(self, timeout: int = 120) -> bool:
        """Wait for user to scan QR code"""
        logger.info(f"Waiting for authentication (timeout: {timeout}s)")
        print("\n" + "="*60)
        print("WHATSAPP AUTHENTICATION REQUIRED")
        print("="*60)
        print("Please scan the QR code in the browser window with your phone")
        print("Waiting for authentication...")
        print("="*60 + "\n")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_authentication():
                logger.info("Authentication successful!")
                print("\n✓ Authentication successful!\n")
                return True
            time.sleep(2)
        
        logger.error("Authentication timeout")
        print("\n✗ Authentication timeout!\n")
        return False
    
    def get_unread_chats(self) -> List[Dict]:
        """Get list of chats with unread messages"""
        try:
            unread_chats = []
            
            # Find all chat elements with unread badge
            chat_elements = self.page.query_selector_all('[data-testid="cell-frame-container"]')
            
            for chat_elem in chat_elements[:Config.MAX_MESSAGES_PER_CHECK]:
                try:
                    # Check for unread badge
                    unread_badge = chat_elem.query_selector('[data-testid="icon-unread-count"]')
                    if not unread_badge:
                        continue
                    
                    # Get chat name
                    name_elem = chat_elem.query_selector('[data-testid="cell-frame-title"]')
                    chat_name = name_elem.inner_text() if name_elem else "Unknown"
                    
                    # Get last message preview
                    msg_elem = chat_elem.query_selector('[data-testid="last-msg-text"]')
                    last_msg = msg_elem.inner_text() if msg_elem else ""
                    
                    unread_chats.append({
                        "name": chat_name,
                        "last_message": last_msg,
                        "element": chat_elem
                    })
                    
                except Exception as e:
                    logger.debug(f"Error parsing chat element: {e}")
                    continue
            
            return unread_chats
            
        except Exception as e:
            logger.error(f"Error getting unread chats: {e}")
            return []
    
    def read_messages_from_chat(self, chat_name: str) -> List[Message]:
        """Read messages from currently open chat"""
        messages = []
        
        try:
            # Wait for messages to load
            time.sleep(1)
            
            # Get all message elements
            message_elements = self.page.query_selector_all('[data-testid="msg-container"]')
            
            # Get last N messages
            recent_messages = message_elements[-20:] if len(message_elements) > 20 else message_elements
            
            for msg_elem in recent_messages:
                try:
                    # Check if message is incoming (not from me)
                    is_incoming = msg_elem.query_selector('[data-testid="msg-container"] [data-testid="tail-in"]')
                    if not is_incoming:
                        continue
                    
                    # Get message text
                    text_elem = msg_elem.query_selector('[data-testid="conversation-text"]')
                    if not text_elem:
                        continue
                    
                    text = text_elem.inner_text()
                    
                    # Get timestamp
                    time_elem = msg_elem.query_selector('[data-testid="msg-meta"]')
                    timestamp = time_elem.inner_text() if time_elem else datetime.now().strftime("%H:%M")
                    
                    # Create unique message ID
                    msg_id = f"{chat_name}:{timestamp}:{text[:50]}"
                    
                    # Skip if already seen
                    if msg_id in self.seen_messages:
                        continue
                    
                    # Create message object
                    message = Message(
                        sender=chat_name,
                        text=text,
                        timestamp=timestamp,
                        chat_name=chat_name
                    )
                    
                    # Calculate importance
                    message.calculate_importance()
                    
                    messages.append(message)
                    self.seen_messages.add(msg_id)
                    
                except Exception as e:
                    logger.debug(f"Error parsing message: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            logger.error(f"Error reading messages from chat: {e}")
            return []
    
    def process_unread_messages(self) -> List[Message]:
        """Process all unread messages"""
        all_messages = []
        
        try:
            unread_chats = self.get_unread_chats()
            logger.info(f"Found {len(unread_chats)} chats with unread messages")
            
            for chat in unread_chats:
                try:
                    logger.info(f"Processing chat: {chat['name']}")
                    
                    # Click on chat to open it
                    chat['element'].click()
                    time.sleep(1)
                    
                    # Read messages
                    messages = self.read_messages_from_chat(chat['name'])
                    all_messages.extend(messages)
                    
                    logger.info(f"Found {len(messages)} new messages from {chat['name']}")
                    
                except Exception as e:
                    logger.error(f"Error processing chat {chat['name']}: {e}")
                    continue
            
            return all_messages
            
        except Exception as e:
            logger.error(f"Error processing unread messages: {e}")
            return []
    
    def create_action_file(self, message: Message) -> bool:
        """Create action file for important message"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_{timestamp}_{message.sender.replace(' ', '_')[:30]}.md"
            filepath = Config.NEEDS_ACTION_DIR / filename
            
            # Create action file content
            content = f"""# WhatsApp Message - Action Required

## Message Details
- **From:** {message.sender}
- **Chat:** {message.chat_name}
- **Time:** {message.timestamp}
- **Importance Score:** {message.importance_score}
- **Matched Keywords:** {', '.join(message.matched_keywords) if message.matched_keywords else 'None'}

## Message Content
```
{message.text}
```

## Suggested Actions
"""
            
            # Add suggested actions based on keywords
            if any(kw in message.text.lower() for kw in ["payment", "invoice"]):
                content += "- [ ] Check payment status\n- [ ] Verify invoice details\n- [ ] Process payment if required\n"
            
            if any(kw in message.text.lower() for kw in ["meeting", "call"]):
                content += "- [ ] Check calendar availability\n- [ ] Schedule meeting/call\n- [ ] Send confirmation\n"
            
            if any(kw in message.text.lower() for kw in ["urgent", "asap", "emergency"]):
                content += "- [ ] **RESPOND IMMEDIATELY**\n- [ ] Escalate if needed\n"
            
            if "?" in message.text:
                content += "- [ ] Answer the question\n- [ ] Provide requested information\n"
            
            content += "\n## Response\n[Draft your response here]\n\n"
            content += "---\n"
            content += f"*Created by WhatsApp Watcher on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Created action file: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return False
    
    def run_monitoring_cycle(self) -> None:
        """Run one monitoring cycle"""
        try:
            # Check authentication
            if not self.check_authentication():
                logger.warning("Not authenticated, waiting for authentication...")
                if not self.wait_for_authentication(timeout=300):
                    logger.error("Failed to authenticate")
                    return
            
            # Process unread messages
            messages = self.process_unread_messages()
            
            if messages:
                logger.info(f"Processed {len(messages)} new messages")
                
                # Create action files for important messages
                important_count = 0
                for message in messages:
                    if message.importance_score >= 10:
                        self.create_action_file(message)
                        important_count += 1
                
                logger.info(f"Created {important_count} action files")
            else:
                logger.debug("No new messages")
            
        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}")
    
    def run(self) -> None:
        """Main run loop"""
        logger.info("Starting WhatsApp Watcher")
        print("\n" + "="*60)
        print("WHATSAPP WATCHER - SILVER TIER")
        print("="*60)
        print(f"Monitoring interval: {Config.CHECK_INTERVAL}s")
        print(f"Action files location: {Config.NEEDS_ACTION_DIR}")
        print(f"Logs location: {Config.LOG_FILE}")
        print("="*60 + "\n")
        
        try:
            # Start browser
            if not self.start_browser():
                logger.error("Failed to start browser")
                return
            
            # Navigate to WhatsApp
            if not self.navigate_to_whatsapp():
                logger.error("Failed to navigate to WhatsApp")
                return
            
            # Check/wait for authentication
            if not self.check_authentication():
                if not self.wait_for_authentication():
                    logger.error("Failed to authenticate")
                    return
            
            print("✓ Ready! Monitoring WhatsApp messages...\n")
            
            # Main monitoring loop
            cycle_count = 0
            while True:
                cycle_count += 1
                logger.info(f"Starting monitoring cycle {cycle_count}")
                
                self.run_monitoring_cycle()
                
                logger.info(f"Cycle {cycle_count} complete. Sleeping for {Config.CHECK_INTERVAL}s")
                time.sleep(Config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            print("\n\nShutting down WhatsApp Watcher...")
            
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Cleanup complete")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# ========================================
# Main Entry Point
# ========================================

def main():
    """Main entry point"""
    try:
        watcher = WhatsAppWatcher()
        watcher.run()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
