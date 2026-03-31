#!/usr/bin/env python3
"""
Filesystem Watcher - Bronze Tier Implementation (EASIEST TO TEST!)

Monitors a drop folder for new files and creates action files.
This is the simplest watcher to test - perfect for Bronze Tier.

Usage:
    python filesystem_watcher.py <vault_path> <watch_folder>
    
Example:
    python filesystem_watcher.py AI_Employee_Vault test_drops

Requirements:
    pip install watchdog

No API keys needed - just drop files and it works!
"""

import os
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Watchdog import for real-time file monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    print("WARNING: watchdog not installed. Using polling mode.")
    print("For better performance: pip install watchdog")
    WATCHDOG_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filesystem_watcher.log'),
        logging.StreamHandler()
    ]
)

# Environment variables
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
CHECK_INTERVAL = int(os.getenv('FILESYSTEM_CHECK_INTERVAL', '10'))  # seconds


class FilesystemWatcher:
    """
    Watches a folder for new files and creates action files in vault.
    """
    
    def __init__(self, vault_path: str, watch_folder: str):
        """
        Initialize Filesystem Watcher.
        
        Args:
            vault_path: Path to Obsidian vault
            watch_folder: Folder to monitor for new files
        """
        self.vault_path = Path(vault_path).resolve()
        self.watch_folder = Path(watch_folder).resolve()
        self.needs_action = self.vault_path / 'Needs_Action'
        self.processed_files = set()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create watch folder if it doesn't exist
        self.watch_folder.mkdir(parents=True, exist_ok=True)
        
        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Initialized FilesystemWatcher")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Watching: {self.watch_folder}")
        self.logger.info(f"Check interval: {CHECK_INTERVAL}s")
        self.logger.info(f"DRY_RUN mode: {DRY_RUN}")
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check watch folder for new files.
        
        Returns:
            List of new files to process
        """
        new_files = []
        
        try:
            for file_path in self.watch_folder.iterdir():
                # Skip directories and already processed files
                if not file_path.is_file():
                    continue
                if str(file_path) in self.processed_files:
                    continue
                
                # Get file info
                stat = file_path.stat()
                new_files.append({
                    'path': file_path,
                    'name': file_path.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'extension': file_path.suffix.lower()
                })
                
                # Mark as processed
                self.processed_files.add(str(file_path))
            
            if new_files:
                self.logger.info(f"Found {len(new_files)} new file(s)")
        
        except Exception as e:
            self.logger.error(f"Error checking for files: {e}")
        
        return new_files
    
    def determine_priority(self, file_info: Dict[str, Any]) -> str:
        """
        Determine priority based on file characteristics.
        
        Args:
            file_info: File information
            
        Returns:
            Priority level: high, medium, or low
        """
        name_lower = file_info['name'].lower()
        
        # High priority keywords
        if any(kw in name_lower for kw in ['urgent', 'asap', 'critical', 'important']):
            return 'high'
        
        # High priority file types
        if file_info['extension'] in ['.pdf', '.docx', '.xlsx']:
            return 'medium'
        
        # Large files
        if file_info['size'] > 10 * 1024 * 1024:  # > 10 MB
            return 'medium'
        
        return 'low'
    
    def get_file_type_description(self, extension: str) -> str:
        """Get human-readable file type."""
        types = {
            '.pdf': 'PDF Document',
            '.docx': 'Word Document',
            '.xlsx': 'Excel Spreadsheet',
            '.pptx': 'PowerPoint Presentation',
            '.txt': 'Text File',
            '.md': 'Markdown Document',
            '.jpg': 'Image (JPEG)',
            '.jpeg': 'Image (JPEG)',
            '.png': 'Image (PNG)',
            '.gif': 'Image (GIF)',
            '.zip': 'ZIP Archive',
            '.csv': 'CSV Data File',
            '.json': 'JSON Data File',
            '.py': 'Python Script',
            '.js': 'JavaScript File',
            '.html': 'HTML Document',
        }
        return types.get(extension.lower(), 'Unknown File Type')
    
    def create_action_file(self, file_info: Dict[str, Any]) -> Path:
        """
        Create action file in Needs_Action folder.
        
        Args:
            file_info: File information
            
        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Clean filename for action file
        clean_name = "".join(
            c if c.isalnum() or c in (' ', '_', '.') else '_' 
            for c in file_info['name']
        )[:50]
        
        action_filename = f"FILE_{timestamp}_{clean_name}.md"
        action_filepath = self.needs_action / action_filename
        
        # Determine priority
        priority = self.determine_priority(file_info)
        
        # Format file size
        size_kb = file_info['size'] / 1024
        if size_kb < 1024:
            size_str = f"{size_kb:.2f} KB"
        else:
            size_str = f"{size_kb / 1024:.2f} MB"
        
        # Get file type description
        file_type = self.get_file_type_description(file_info['extension'])
        
        # Create markdown content
        content = f"""---
type: file_drop
original_name: {file_info['name']}
file_type: {file_type}
size: {file_info['size']}
size_readable: {size_str}
extension: {file_info['extension']}
detected: {datetime.now().isoformat()}
modified: {file_info['modified'].isoformat()}
priority: {priority}
status: pending
source_path: {file_info['path']}
---

## New File Dropped

**Filename**: `{file_info['name']}`  
**Type**: {file_type}  
**Size**: {size_str}  
**Modified**: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}  
**Priority**: {priority.upper()}

## File Location

**Original Path**: `{file_info['path']}`  
**Drop Folder**: `{self.watch_folder}`

## Suggested Actions

- [ ] Review file contents
- [ ] Determine what needs to be done
- [ ] Extract key information
- [ ] Move to appropriate project folder
- [ ] Update relevant documentation
- [ ] Archive original if needed

## Processing Notes

### Document Files (.pdf, .docx, .xlsx)
- Review contents for important information
- Extract action items or data
- File appropriately in vault

### Image Files
- Review and categorize
- Add to relevant project or documentation
- Consider if needs processing/editing

### Data Files (.csv, .json, .xlsx)
- Import into accounting or project tracking
- Validate data integrity
- Process as needed

### Archive Files (.zip)
- Extract and review contents
- Process individual files
- Clean up after extraction

## Notes

*Add any observations or decisions here*

---

**Detected by**: Filesystem Watcher  
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**DRY_RUN**: {DRY_RUN}
"""
        
        if DRY_RUN:
            self.logger.info(f"[DRY RUN] Would create: {action_filename}")
            self.logger.info(f"[DRY RUN] File: {file_info['name']} ({size_str})")
            self.logger.info(f"[DRY RUN] Priority: {priority}")
        else:
            action_filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"✓ Created action file: {action_filename}")
            self.logger.info(f"  Original: {file_info['name']} ({size_str})")
        
        return action_filepath
    
    def run_polling(self):
        """Run in polling mode (checks periodically)."""
        self.logger.info("Running in POLLING mode")
        self.logger.info(f"Checking every {CHECK_INTERVAL} seconds")
        self.logger.info("Drop files into the watch folder to test!")
        self.logger.info(f"Watch folder: {self.watch_folder}")
        self.logger.info("")
        
        while True:
            try:
                files = self.check_for_updates()
                
                for file_info in files:
                    try:
                        self.create_action_file(file_info)
                    except Exception as e:
                        self.logger.error(f"Error processing file: {e}")
                
                if not files:
                    self.logger.debug("No new files")
            
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
            
            time.sleep(CHECK_INTERVAL)
    
    def run_realtime(self):
        """Run in real-time mode using watchdog."""
        self.logger.info("Running in REAL-TIME mode (watchdog)")
        self.logger.info("Monitoring for immediate file detection!")
        self.logger.info(f"Watch folder: {self.watch_folder}")
        self.logger.info("")
        
        class FileHandler(FileSystemEventHandler):
            def __init__(self, watcher):
                self.watcher = watcher
            
            def on_created(self, event):
                if event.is_directory:
                    return
                
                # Small delay to ensure file is fully written
                time.sleep(0.5)
                
                file_path = Path(event.src_path)
                if str(file_path) not in self.watcher.processed_files:
                    stat = file_path.stat()
                    file_info = {
                        'path': file_path,
                        'name': file_path.name,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'extension': file_path.suffix.lower()
                    }
                    self.watcher.processed_files.add(str(file_path))
                    try:
                        self.watcher.create_action_file(file_info)
                    except Exception as e:
                        self.watcher.logger.error(f"Error processing file: {e}")
        
        # Set up observer
        observer = Observer()
        event_handler = FileHandler(self)
        observer.schedule(event_handler, str(self.watch_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
    def run(self):
        """Main loop - use real-time if watchdog available, otherwise poll."""
        if WATCHDOG_AVAILABLE:
            self.run_realtime()
        else:
            self.run_polling()


def main():
    """Main entry point."""
    import sys
    
    print("=" * 70)
    print("Filesystem Watcher for AI Employee - Bronze Tier")
    print("=" * 70)
    print()
    
    # Check arguments
    if len(sys.argv) < 3:
        print("Usage: python filesystem_watcher.py <vault_path> <watch_folder>")
        print()
        print("Example:")
        print("  python filesystem_watcher.py AI_Employee_Vault test_drops")
        print()
        print("This will:")
        print("  1. Monitor 'test_drops' folder for new files")
        print("  2. Create action files in 'AI_Employee_Vault/Needs_Action'")
        print()
        print("Test it:")
        print("  1. Run this script")
        print("  2. Drop any file into 'test_drops' folder")
        print("  3. Check 'AI_Employee_Vault/Needs_Action' for the action file!")
        print()
        sys.exit(1)
    
    vault_path = sys.argv[1]
    watch_folder = sys.argv[2]
    
    print(f"Vault Path:    {vault_path}")
    print(f"Watch Folder:  {watch_folder}")
    print(f"DRY_RUN:       {DRY_RUN}")
    print(f"Mode:          {'Real-time' if WATCHDOG_AVAILABLE else 'Polling'}")
    if not WATCHDOG_AVAILABLE:
        print(f"Check Interval: {CHECK_INTERVAL}s")
    print()
    print("=" * 70)
    print()
    
    if DRY_RUN:
        print("⚠️  DRY_RUN MODE: Action files will be simulated (not created)")
        print("   Set DRY_RUN=false in .env to actually create files")
        print()
    
    print("Ready! Drop files into the watch folder to see them processed.")
    print("Press Ctrl+C to stop.")
    print()
    
    # Create watcher
    watcher = FilesystemWatcher(vault_path, watch_folder)
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Filesystem Watcher stopped by user")
        print("=" * 70)
        watcher.logger.info("Watcher stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        watcher.logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
