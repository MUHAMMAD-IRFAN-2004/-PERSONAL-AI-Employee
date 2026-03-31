"""
Human-in-the-Loop Approval System - Silver Tier
================================================
Monitors action files and routes high-risk items through approval workflow.

Features:
- Automatic risk assessment
- File routing based on risk level
- Approval/rejection handling
- Action execution tracking
- Comprehensive logging

Author: AI Employee System
Version: 1.0.0
"""

import os
import sys
import time
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import json

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
    """Configuration for Approval System"""
    
    # Directories
    BASE_DIR = Path(__file__).parent
    VAULT_DIR = BASE_DIR / "AI_Employee_Vault"
    NEEDS_ACTION_DIR = VAULT_DIR / "Needs_Action"
    PENDING_APPROVAL_DIR = VAULT_DIR / "Pending_Approval"
    APPROVED_DIR = VAULT_DIR / "Approved"
    REJECTED_DIR = VAULT_DIR / "Rejected"
    LOGS_DIR = VAULT_DIR / "Logs"
    DONE_DIR = VAULT_DIR / "Done"
    
    # Monitoring settings
    CHECK_INTERVAL = int(os.getenv("APPROVAL_CHECK_INTERVAL", "10"))  # seconds
    
    # Risk assessment keywords
    HIGH_RISK_KEYWORDS = [
        # Financial
        "payment", "pay", "invoice", "transaction", "transfer", "money",
        "credit card", "bank", "wire", "refund", "charge",
        
        # Destructive actions
        "delete", "remove", "drop", "truncate", "destroy", "wipe",
        "cancel", "terminate", "end", "close account",
        
        # Communications
        "send email", "send message", "post", "publish", "tweet",
        "share", "broadcast", "announce",
        
        # System changes
        "deploy", "production", "live", "execute", "run",
        "modify", "update", "change", "alter",
        
        # Legal/Compliance
        "contract", "agreement", "legal", "sign", "approve deal",
        "commitment", "obligation", "terms"
    ]
    
    MEDIUM_RISK_KEYWORDS = [
        "schedule", "meeting", "appointment", "calendar",
        "response", "reply", "answer", "respond",
        "create", "add", "new", "setup",
        "urgent", "important", "priority", "asap"
    ]
    
    # Risk thresholds
    HIGH_RISK_THRESHOLD = 50
    MEDIUM_RISK_THRESHOLD = 20
    
    # Auto-approve low risk items
    AUTO_APPROVE_LOW_RISK = os.getenv("AUTO_APPROVE_LOW_RISK", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / f"approval_system_{datetime.now().strftime('%Y%m%d')}.log"


# ========================================
# Logging Setup
# ========================================

def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("ApprovalSystem")
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
# Action File Analysis
# ========================================

class ActionFile:
    """Represents an action file"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filename = filepath.name
        self.content = ""
        self.risk_score = 0
        self.risk_level = "LOW"
        self.matched_keywords = []
        self.source = "unknown"
        self.suggested_actions = []
        
        self._load_content()
        self._parse_metadata()
        self._assess_risk()
    
    def _load_content(self) -> None:
        """Load file content"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            logger.error(f"Error loading file {self.filename}: {e}")
            self.content = ""
    
    def _parse_metadata(self) -> None:
        """Parse metadata from file"""
        # Detect source
        if "gmail" in self.filename.lower():
            self.source = "Gmail"
        elif "whatsapp" in self.filename.lower():
            self.source = "WhatsApp"
        elif "filesystem" in self.filename.lower():
            self.source = "Filesystem"
        else:
            self.source = "Unknown"
        
        # Extract suggested actions (lines starting with - [ ])
        action_pattern = r'^- \[ \] (.+)$'
        self.suggested_actions = re.findall(action_pattern, self.content, re.MULTILINE)
    
    def _assess_risk(self) -> None:
        """Assess risk level based on content"""
        content_lower = self.content.lower()
        score = 0
        
        # Check for high-risk keywords
        for keyword in Config.HIGH_RISK_KEYWORDS:
            if keyword.lower() in content_lower:
                score += 30
                self.matched_keywords.append(("HIGH", keyword))
        
        # Check for medium-risk keywords
        for keyword in Config.MEDIUM_RISK_KEYWORDS:
            if keyword.lower() in content_lower:
                score += 10
                self.matched_keywords.append(("MEDIUM", keyword))
        
        # Additional risk factors
        
        # Large monetary amounts
        money_pattern = r'\$\s*\d{3,}|\d{3,}\s*(?:dollars|usd|eur|gbp)'
        if re.search(money_pattern, content_lower):
            score += 25
            self.matched_keywords.append(("HIGH", "large amount"))
        
        # URLs (potential phishing/external access)
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, content_lower)
        if len(urls) > 0:
            score += 10 * min(len(urls), 3)
            self.matched_keywords.append(("MEDIUM", f"{len(urls)} URLs"))
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.content)
        if len(emails) > 2:
            score += 10
            self.matched_keywords.append(("MEDIUM", "multiple emails"))
        
        # Urgent/ASAP indicators
        if any(word in content_lower for word in ["urgent", "asap", "immediately", "emergency"]):
            score += 15
            self.matched_keywords.append(("MEDIUM", "urgency"))
        
        # Multiple exclamation marks
        if self.content.count("!") >= 3:
            score += 5
            self.matched_keywords.append(("LOW", "emphasis"))
        
        self.risk_score = score
        
        # Determine risk level
        if score >= Config.HIGH_RISK_THRESHOLD:
            self.risk_level = "HIGH"
        elif score >= Config.MEDIUM_RISK_THRESHOLD:
            self.risk_level = "MEDIUM"
        else:
            self.risk_level = "LOW"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "filename": self.filename,
            "source": self.source,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "matched_keywords": self.matched_keywords,
            "suggested_actions": self.suggested_actions
        }


# ========================================
# Approval System
# ========================================

class ApprovalSystem:
    """Main approval system class"""
    
    def __init__(self):
        self.processed_files = set()
        
        # Ensure all directories exist
        Config.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        Config.PENDING_APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
        Config.APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        Config.REJECTED_DIR.mkdir(parents=True, exist_ok=True)
        Config.DONE_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("Approval System initialized")
    
    def scan_needs_action(self) -> List[ActionFile]:
        """Scan Needs_Action folder for new files"""
        action_files = []
        
        try:
            for filepath in Config.NEEDS_ACTION_DIR.glob("*.md"):
                if filepath.name not in self.processed_files:
                    action_file = ActionFile(filepath)
                    action_files.append(action_file)
                    self.processed_files.add(filepath.name)
            
            return action_files
            
        except Exception as e:
            logger.error(f"Error scanning Needs_Action folder: {e}")
            return []
    
    def route_file(self, action_file: ActionFile) -> bool:
        """Route file based on risk level"""
        try:
            source_path = action_file.filepath
            
            if action_file.risk_level == "HIGH":
                # High risk: Move to Pending_Approval
                dest_path = Config.PENDING_APPROVAL_DIR / action_file.filename
                shutil.move(str(source_path), str(dest_path))
                logger.warning(f"HIGH RISK: {action_file.filename} -> Pending_Approval (score: {action_file.risk_score})")
                self._add_approval_header(dest_path, action_file)
                return True
                
            elif action_file.risk_level == "MEDIUM":
                # Medium risk: Move to Pending_Approval
                dest_path = Config.PENDING_APPROVAL_DIR / action_file.filename
                shutil.move(str(source_path), str(dest_path))
                logger.info(f"MEDIUM RISK: {action_file.filename} -> Pending_Approval (score: {action_file.risk_score})")
                self._add_approval_header(dest_path, action_file)
                return True
                
            else:
                # Low risk: Auto-approve or keep in Needs_Action
                if Config.AUTO_APPROVE_LOW_RISK:
                    dest_path = Config.APPROVED_DIR / action_file.filename
                    shutil.move(str(source_path), str(dest_path))
                    logger.info(f"LOW RISK: {action_file.filename} -> Auto-approved (score: {action_file.risk_score})")
                    self._add_execution_header(dest_path, action_file, approved=True, auto=True)
                else:
                    logger.info(f"LOW RISK: {action_file.filename} kept in Needs_Action (score: {action_file.risk_score})")
                return True
            
        except Exception as e:
            logger.error(f"Error routing file {action_file.filename}: {e}")
            return False
    
    def _add_approval_header(self, filepath: Path, action_file: ActionFile) -> None:
        """Add approval information to file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            header = f"""---
**🚨 APPROVAL REQUIRED 🚨**

**Risk Level:** {action_file.risk_level}  
**Risk Score:** {action_file.risk_score}  
**Source:** {action_file.source}  
**Assessed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Risk Factors:**
"""
            for risk_level, keyword in action_file.matched_keywords:
                header += f"- [{risk_level}] {keyword}\n"
            
            header += f"""
**Instructions:**
1. Review the action file carefully
2. To APPROVE: Move this file to `Approved/` folder
3. To REJECT: Move this file to `Rejected/` folder
4. To MODIFY: Edit the file first, then move to `Approved/`

---

"""
            
            new_content = header + content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
        except Exception as e:
            logger.error(f"Error adding approval header to {filepath}: {e}")
    
    def _add_execution_header(self, filepath: Path, action_file: ActionFile, 
                             approved: bool, auto: bool = False) -> None:
        """Add execution status header to file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            status = "APPROVED" if approved else "REJECTED"
            emoji = "✅" if approved else "❌"
            auto_text = " (Auto)" if auto else ""
            
            header = f"""---
**{emoji} {status}{auto_text} {emoji}**

**Risk Level:** {action_file.risk_level}  
**Risk Score:** {action_file.risk_score}  
**Decision Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
            
            new_content = header + content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
        except Exception as e:
            logger.error(f"Error adding execution header to {filepath}: {e}")
    
    def check_approved_folder(self) -> List[Path]:
        """Check Approved folder for files to execute"""
        try:
            return list(Config.APPROVED_DIR.glob("*.md"))
        except Exception as e:
            logger.error(f"Error checking Approved folder: {e}")
            return []
    
    def check_rejected_folder(self) -> List[Path]:
        """Check Rejected folder for files to archive"""
        try:
            return list(Config.REJECTED_DIR.glob("*.md"))
        except Exception as e:
            logger.error(f"Error checking Rejected folder: {e}")
            return []
    
    def execute_approved_action(self, filepath: Path) -> bool:
        """Execute approved action"""
        try:
            logger.info(f"Executing approved action: {filepath.name}")
            
            # In a real implementation, you would:
            # 1. Parse the action file
            # 2. Execute the requested actions
            # 3. Log the results
            # 4. Move to Done folder
            
            # For now, just move to Done folder
            dest_path = Config.DONE_DIR / filepath.name
            shutil.move(str(filepath), str(dest_path))
            
            logger.info(f"Action executed and moved to Done: {filepath.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing action {filepath.name}: {e}")
            return False
    
    def archive_rejected_action(self, filepath: Path) -> bool:
        """Archive rejected action"""
        try:
            logger.info(f"Archiving rejected action: {filepath.name}")
            
            # Keep in Rejected folder (it's already there)
            # Optionally, could move to Done or a separate Archive folder
            
            logger.info(f"Action rejected and archived: {filepath.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error archiving rejected action {filepath.name}: {e}")
            return False
    
    def run_cycle(self) -> Dict:
        """Run one processing cycle"""
        stats = {
            "scanned": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "approved": 0,
            "rejected": 0
        }
        
        try:
            # 1. Scan Needs_Action folder
            action_files = self.scan_needs_action()
            stats["scanned"] = len(action_files)
            
            if action_files:
                logger.info(f"Found {len(action_files)} new action files")
            
            # 2. Route files based on risk
            for action_file in action_files:
                self.route_file(action_file)
                
                if action_file.risk_level == "HIGH":
                    stats["high_risk"] += 1
                elif action_file.risk_level == "MEDIUM":
                    stats["medium_risk"] += 1
                else:
                    stats["low_risk"] += 1
            
            # 3. Check for approved actions
            approved_files = self.check_approved_folder()
            for filepath in approved_files:
                if self.execute_approved_action(filepath):
                    stats["approved"] += 1
            
            # 4. Check for rejected actions
            rejected_files = self.check_rejected_folder()
            for filepath in rejected_files:
                if self.archive_rejected_action(filepath):
                    stats["rejected"] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error in processing cycle: {e}")
            return stats
    
    def run(self) -> None:
        """Main run loop"""
        logger.info("Starting Approval System")
        print("\n" + "="*60)
        print("APPROVAL SYSTEM - SILVER TIER")
        print("="*60)
        print(f"Monitoring interval: {Config.CHECK_INTERVAL}s")
        print(f"Auto-approve low risk: {Config.AUTO_APPROVE_LOW_RISK}")
        print(f"High risk threshold: {Config.HIGH_RISK_THRESHOLD}")
        print(f"Medium risk threshold: {Config.MEDIUM_RISK_THRESHOLD}")
        print("="*60)
        print("\nMonitoring folders:")
        print(f"  📥 Needs Action: {Config.NEEDS_ACTION_DIR}")
        print(f"  ⏳ Pending Approval: {Config.PENDING_APPROVAL_DIR}")
        print(f"  ✅ Approved: {Config.APPROVED_DIR}")
        print(f"  ❌ Rejected: {Config.REJECTED_DIR}")
        print("="*60 + "\n")
        
        try:
            cycle_count = 0
            
            while True:
                cycle_count += 1
                logger.debug(f"Starting cycle {cycle_count}")
                
                stats = self.run_cycle()
                
                if any(stats.values()):
                    logger.info(f"Cycle {cycle_count} stats: {stats}")
                
                time.sleep(Config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            print("\n\nShutting down Approval System...")
            
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            sys.exit(1)


# ========================================
# Main Entry Point
# ========================================

def main():
    """Main entry point"""
    try:
        system = ApprovalSystem()
        system.run()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
