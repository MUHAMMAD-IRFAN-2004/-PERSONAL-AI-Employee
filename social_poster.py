"""
Social Media Poster - Silver Tier
==================================
Automated posting to LinkedIn and Twitter using browser automation.

Features:
- Queue-based posting system
- LinkedIn and Twitter support
- Rate limiting (5 LinkedIn/day, 10 Twitter/day)
- Session management
- Post scheduling
- Comprehensive logging

Author: AI Employee System
Version: 1.0.0
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
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
    """Configuration for Social Poster"""
    
    # Directories
    BASE_DIR = Path(__file__).parent
    VAULT_DIR = BASE_DIR / "AI_Employee_Vault"
    SOCIAL_QUEUE_DIR = VAULT_DIR / "Social_Queue"
    POSTED_DIR = VAULT_DIR / "Social_Queue" / "Posted"
    FAILED_DIR = VAULT_DIR / "Social_Queue" / "Failed"
    LOGS_DIR = VAULT_DIR / "Logs"
    
    # Browser settings
    BROWSER_USER_DATA_DIR = BASE_DIR / ".social_browser_data"
    HEADLESS = os.getenv("SOCIAL_HEADLESS", "false").lower() == "true"
    
    # Rate limits (posts per day)
    LINKEDIN_DAILY_LIMIT = int(os.getenv("LINKEDIN_DAILY_LIMIT", "5"))
    TWITTER_DAILY_LIMIT = int(os.getenv("TWITTER_DAILY_LIMIT", "10"))
    
    # Delay between posts (seconds)
    POST_DELAY = int(os.getenv("POST_DELAY", "60"))
    
    # Check interval (seconds)
    CHECK_INTERVAL = int(os.getenv("SOCIAL_CHECK_INTERVAL", "300"))  # 5 minutes
    
    # Credentials (loaded from environment)
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
    TWITTER_USERNAME = os.getenv("TWITTER_USERNAME", "")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / f"social_poster_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Rate limit tracking file
    RATE_LIMIT_FILE = VAULT_DIR / ".social_rate_limits.json"


# ========================================
# Logging Setup
# ========================================

def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("SocialPoster")
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
# Rate Limit Tracker
# ========================================

class RateLimitTracker:
    """Track daily posting limits"""
    
    def __init__(self):
        self.filepath = Config.RATE_LIMIT_FILE
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load rate limit data"""
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading rate limits: {e}")
        
        return self._get_default()
    
    def _get_default(self) -> Dict:
        """Get default rate limit structure"""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "linkedin": {
                "date": today,
                "count": 0,
                "limit": Config.LINKEDIN_DAILY_LIMIT
            },
            "twitter": {
                "date": today,
                "count": 0,
                "limit": Config.TWITTER_DAILY_LIMIT
            }
        }
    
    def _save(self) -> None:
        """Save rate limit data"""
        try:
            Config.VAULT_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving rate limits: {e}")
    
    def _reset_if_needed(self, platform: str) -> None:
        """Reset counter if new day"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data[platform]["date"] != today:
            self.data[platform]["date"] = today
            self.data[platform]["count"] = 0
            self._save()
            logger.info(f"Reset {platform} counter for new day")
    
    def can_post(self, platform: str) -> bool:
        """Check if can post to platform"""
        self._reset_if_needed(platform)
        remaining = self.get_remaining(platform)
        return remaining > 0
    
    def get_remaining(self, platform: str) -> int:
        """Get remaining posts for platform"""
        self._reset_if_needed(platform)
        limit = self.data[platform]["limit"]
        count = self.data[platform]["count"]
        return max(0, limit - count)
    
    def increment(self, platform: str) -> None:
        """Increment post count for platform"""
        self._reset_if_needed(platform)
        self.data[platform]["count"] += 1
        self._save()
        logger.info(f"Incremented {platform} counter to {self.data[platform]['count']}")


# ========================================
# Social Post
# ========================================

class SocialPost:
    """Represents a social media post"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filename = filepath.name
        self.content = ""
        self.platforms = []
        self.scheduled_time = None
        self.metadata = {}
        
        self._load_and_parse()
    
    def _load_and_parse(self) -> None:
        """Load and parse post file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # Parse frontmatter if exists
            if raw_content.startswith("---"):
                parts = raw_content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    self.content = parts[2].strip()
                    self._parse_frontmatter(frontmatter)
                else:
                    self.content = raw_content
            else:
                self.content = raw_content
            
            # Auto-detect platforms if not specified
            if not self.platforms:
                if "linkedin" in self.filename.lower():
                    self.platforms = ["linkedin"]
                elif "twitter" in self.filename.lower():
                    self.platforms = ["twitter"]
                else:
                    self.platforms = ["linkedin", "twitter"]
            
        except Exception as e:
            logger.error(f"Error loading post {self.filename}: {e}")
    
    def _parse_frontmatter(self, frontmatter: str) -> None:
        """Parse YAML-like frontmatter"""
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == "platforms":
                    self.platforms = [p.strip().lower() for p in value.split(",")]
                elif key == "scheduled":
                    try:
                        self.scheduled_time = datetime.fromisoformat(value)
                    except:
                        pass
                else:
                    self.metadata[key] = value
    
    def is_ready(self) -> bool:
        """Check if post is ready to be published"""
        if self.scheduled_time:
            return datetime.now() >= self.scheduled_time
        return True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "filename": self.filename,
            "platforms": self.platforms,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "scheduled": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "metadata": self.metadata
        }


# ========================================
# Social Media Platforms
# ========================================

class LinkedInPoster:
    """LinkedIn posting automation"""
    
    def __init__(self, page: Page):
        self.page = page
        self.is_logged_in = False
    
    def login(self) -> bool:
        """Login to LinkedIn"""
        try:
            logger.info("Logging into LinkedIn...")
            
            # Navigate to LinkedIn
            self.page.goto("https://www.linkedin.com/login", timeout=30000)
            time.sleep(2)
            
            # Check if already logged in
            if "feed" in self.page.url:
                logger.info("Already logged in to LinkedIn")
                self.is_logged_in = True
                return True
            
            # Enter credentials
            if not Config.LINKEDIN_EMAIL or not Config.LINKEDIN_PASSWORD:
                logger.error("LinkedIn credentials not configured in .env")
                return False
            
            # Fill login form
            self.page.fill('input[id="username"]', Config.LINKEDIN_EMAIL)
            time.sleep(0.5)
            self.page.fill('input[id="password"]', Config.LINKEDIN_PASSWORD)
            time.sleep(0.5)
            
            # Click login button
            self.page.click('button[type="submit"]')
            time.sleep(5)
            
            # Check if login successful
            if "feed" in self.page.url or "checkpoint" in self.page.url:
                logger.info("LinkedIn login successful")
                self.is_logged_in = True
                return True
            
            logger.error("LinkedIn login failed")
            return False
            
        except Exception as e:
            logger.error(f"Error logging into LinkedIn: {e}")
            return False
    
    def post(self, content: str) -> bool:
        """Post content to LinkedIn"""
        try:
            if not self.is_logged_in:
                if not self.login():
                    return False
            
            logger.info("Posting to LinkedIn...")
            
            # Go to feed if not there
            if "feed" not in self.page.url:
                self.page.goto("https://www.linkedin.com/feed/", timeout=30000)
                time.sleep(3)
            
            # Click "Start a post" button
            start_post_selectors = [
                'button:has-text("Start a post")',
                '[aria-label="Start a post"]',
                '.share-box-feed-entry__trigger'
            ]
            
            clicked = False
            for selector in start_post_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                logger.error("Could not find 'Start a post' button")
                return False
            
            time.sleep(2)
            
            # Type content
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                '[role="textbox"][contenteditable="true"]',
                '.mentions-texteditor__content[contenteditable="true"]'
            ]
            
            typed = False
            for selector in editor_selectors:
                try:
                    self.page.fill(selector, content)
                    typed = True
                    break
                except:
                    continue
            
            if not typed:
                logger.error("Could not find post editor")
                return False
            
            time.sleep(1)
            
            # Click Post button
            post_button_selectors = [
                'button:has-text("Post")',
                '[aria-label="Post"]',
                '.share-actions__primary-action'
            ]
            
            posted = False
            for selector in post_button_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    posted = True
                    break
                except:
                    continue
            
            if not posted:
                logger.error("Could not find Post button")
                return False
            
            time.sleep(3)
            logger.info("Successfully posted to LinkedIn")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False


class TwitterPoster:
    """Twitter/X posting automation"""
    
    def __init__(self, page: Page):
        self.page = page
        self.is_logged_in = False
    
    def login(self) -> bool:
        """Login to Twitter"""
        try:
            logger.info("Logging into Twitter...")
            
            # Navigate to Twitter
            self.page.goto("https://twitter.com/login", timeout=30000)
            time.sleep(2)
            
            # Check if already logged in
            if "home" in self.page.url:
                logger.info("Already logged in to Twitter")
                self.is_logged_in = True
                return True
            
            # Enter credentials
            if not Config.TWITTER_USERNAME or not Config.TWITTER_PASSWORD:
                logger.error("Twitter credentials not configured in .env")
                return False
            
            # Fill username
            username_selectors = [
                'input[autocomplete="username"]',
                'input[name="text"]'
            ]
            
            filled = False
            for selector in username_selectors:
                try:
                    self.page.fill(selector, Config.TWITTER_USERNAME)
                    filled = True
                    break
                except:
                    continue
            
            if not filled:
                logger.error("Could not find username field")
                return False
            
            time.sleep(0.5)
            
            # Click Next
            self.page.keyboard.press("Enter")
            time.sleep(2)
            
            # Fill password
            password_selectors = [
                'input[autocomplete="current-password"]',
                'input[name="password"]',
                'input[type="password"]'
            ]
            
            filled = False
            for selector in password_selectors:
                try:
                    self.page.fill(selector, Config.TWITTER_PASSWORD)
                    filled = True
                    break
                except:
                    continue
            
            if not filled:
                logger.error("Could not find password field")
                return False
            
            time.sleep(0.5)
            
            # Click Login
            self.page.keyboard.press("Enter")
            time.sleep(5)
            
            # Check if login successful
            if "home" in self.page.url:
                logger.info("Twitter login successful")
                self.is_logged_in = True
                return True
            
            logger.error("Twitter login failed")
            return False
            
        except Exception as e:
            logger.error(f"Error logging into Twitter: {e}")
            return False
    
    def post(self, content: str) -> bool:
        """Post content to Twitter"""
        try:
            if not self.is_logged_in:
                if not self.login():
                    return False
            
            logger.info("Posting to Twitter...")
            
            # Go to home if not there
            if "home" not in self.page.url:
                self.page.goto("https://twitter.com/home", timeout=30000)
                time.sleep(3)
            
            # Find tweet compose box
            compose_selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[aria-label="Tweet text"]',
                '.public-DraftEditor-content[contenteditable="true"]'
            ]
            
            typed = False
            for selector in compose_selectors:
                try:
                    self.page.fill(selector, content)
                    typed = True
                    break
                except:
                    continue
            
            if not typed:
                logger.error("Could not find tweet compose box")
                return False
            
            time.sleep(1)
            
            # Click Post/Tweet button
            post_button_selectors = [
                '[data-testid="tweetButtonInline"]',
                '[data-testid="tweetButton"]',
                'button:has-text("Post")',
                'button:has-text("Tweet")'
            ]
            
            posted = False
            for selector in post_button_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    posted = True
                    break
                except:
                    continue
            
            if not posted:
                logger.error("Could not find Post button")
                return False
            
            time.sleep(3)
            logger.info("Successfully posted to Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return False


# ========================================
# Social Poster
# ========================================

class SocialPoster:
    """Main social poster class"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.rate_limiter = RateLimitTracker()
        
        # Ensure directories exist
        Config.SOCIAL_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        Config.POSTED_DIR.mkdir(parents=True, exist_ok=True)
        Config.FAILED_DIR.mkdir(parents=True, exist_ok=True)
        Config.BROWSER_USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("Social Poster initialized")
    
    def start_browser(self) -> bool:
        """Start browser with persistent session"""
        try:
            logger.info("Starting browser...")
            self.playwright = sync_playwright().start()
            
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(Config.BROWSER_USER_DATA_DIR),
                headless=Config.HEADLESS,
                args=['--no-sandbox', '--disable-setuid-sandbox'],
                viewport={'width': 1280, 'height': 720}
            )
            
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
            
            logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    def scan_queue(self) -> List[SocialPost]:
        """Scan queue for posts"""
        posts = []
        
        try:
            for filepath in Config.SOCIAL_QUEUE_DIR.glob("*.md"):
                if filepath.parent == Config.SOCIAL_QUEUE_DIR:  # Not in subdirs
                    post = SocialPost(filepath)
                    if post.is_ready():
                        posts.append(post)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error scanning queue: {e}")
            return []
    
    def post_to_platform(self, post: SocialPost, platform: str) -> bool:
        """Post to specific platform"""
        try:
            # Check rate limit
            if not self.rate_limiter.can_post(platform):
                logger.warning(f"Rate limit reached for {platform}")
                return False
            
            # Post based on platform
            if platform == "linkedin":
                poster = LinkedInPoster(self.page)
                success = poster.post(post.content)
            elif platform == "twitter":
                poster = TwitterPoster(self.page)
                success = poster.post(post.content)
            else:
                logger.error(f"Unknown platform: {platform}")
                return False
            
            # Increment counter if successful
            if success:
                self.rate_limiter.increment(platform)
            
            return success
            
        except Exception as e:
            logger.error(f"Error posting to {platform}: {e}")
            return False
    
    def process_post(self, post: SocialPost) -> Dict[str, bool]:
        """Process a post across all platforms"""
        results = {}
        
        for platform in post.platforms:
            logger.info(f"Posting to {platform}: {post.filename}")
            results[platform] = self.post_to_platform(post, platform)
            
            # Delay between platforms
            if len(post.platforms) > 1:
                time.sleep(Config.POST_DELAY)
        
        return results
    
    def move_post(self, post: SocialPost, results: Dict[str, bool]) -> None:
        """Move post based on results"""
        try:
            all_success = all(results.values())
            
            if all_success:
                dest_dir = Config.POSTED_DIR
                status = "SUCCESS"
            else:
                dest_dir = Config.FAILED_DIR
                status = "FAILED"
            
            # Create metadata file
            metadata = {
                "posted_at": datetime.now().isoformat(),
                "results": results,
                "status": status
            }
            
            # Move post file
            dest_path = dest_dir / post.filename
            post.filepath.rename(dest_path)
            
            # Create metadata file
            meta_path = dest_dir / f"{post.filename}.meta.json"
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Moved {post.filename} to {dest_dir.name}")
            
        except Exception as e:
            logger.error(f"Error moving post {post.filename}: {e}")
    
    def run_cycle(self) -> Dict:
        """Run one processing cycle"""
        stats = {
            "scanned": 0,
            "posted": 0,
            "failed": 0,
            "linkedin_remaining": self.rate_limiter.get_remaining("linkedin"),
            "twitter_remaining": self.rate_limiter.get_remaining("twitter")
        }
        
        try:
            posts = self.scan_queue()
            stats["scanned"] = len(posts)
            
            if not posts:
                logger.debug("No posts in queue")
                return stats
            
            logger.info(f"Found {len(posts)} posts to process")
            
            for post in posts:
                logger.info(f"Processing: {post.filename}")
                
                results = self.process_post(post)
                
                if any(results.values()):
                    stats["posted"] += 1
                else:
                    stats["failed"] += 1
                
                self.move_post(post, results)
                
                # Update remaining counts
                stats["linkedin_remaining"] = self.rate_limiter.get_remaining("linkedin")
                stats["twitter_remaining"] = self.rate_limiter.get_remaining("twitter")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error in processing cycle: {e}")
            return stats
    
    def run(self) -> None:
        """Main run loop"""
        logger.info("Starting Social Poster")
        print("\n" + "="*60)
        print("SOCIAL MEDIA POSTER - SILVER TIER")
        print("="*60)
        print(f"LinkedIn daily limit: {Config.LINKEDIN_DAILY_LIMIT}")
        print(f"Twitter daily limit: {Config.TWITTER_DAILY_LIMIT}")
        print(f"Check interval: {Config.CHECK_INTERVAL}s")
        print(f"Queue location: {Config.SOCIAL_QUEUE_DIR}")
        print("="*60 + "\n")
        
        try:
            # Start browser
            if not self.start_browser():
                logger.error("Failed to start browser")
                return
            
            print("✓ Browser started. Monitoring queue...\n")
            
            cycle_count = 0
            while True:
                cycle_count += 1
                logger.debug(f"Starting cycle {cycle_count}")
                
                stats = self.run_cycle()
                
                if stats["scanned"] > 0:
                    logger.info(f"Cycle {cycle_count} stats: {stats}")
                
                time.sleep(Config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            print("\n\nShutting down Social Poster...")
            
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
        poster = SocialPoster()
        poster.run()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
