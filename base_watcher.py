# Python Base Watcher Template
# Use this as a starting point for creating custom Watchers

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseWatcher(ABC):
    """
    Base class for all Watcher scripts.
    
    Watchers monitor external systems and create action files
    in the Needs_Action folder when new items are detected.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the Watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: How often to check for updates (seconds)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Initialized {self.__class__.__name__}")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Check interval: {check_interval}s")
    
    @abstractmethod
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check external system for new items.
        
        Returns:
            List of new items to process
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create a markdown file in Needs_Action folder.
        
        Args:
            item: Item data from check_for_updates
            
        Returns:
            Path to created file
        """
        pass
    
    def run(self):
        """
        Main loop - continuously check for updates.
        """
        self.logger.info(f"Starting {self.__class__.__name__} main loop")
        
        while True:
            try:
                # Check for new items
                items = self.check_for_updates()
                
                if items:
                    self.logger.info(f"Found {len(items)} new item(s)")
                    
                    # Process each item
                    for item in items:
                        try:
                            filepath = self.create_action_file(item)
                            self.logger.info(f"Created action file: {filepath.name}")
                        except Exception as e:
                            self.logger.error(f"Error creating action file: {e}")
                else:
                    self.logger.debug("No new items found")
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
            
            # Wait before next check
            time.sleep(self.check_interval)


# Example: Simple Filesystem Watcher
class FilesystemWatcher(BaseWatcher):
    """
    Watches a drop folder for new files.
    """
    
    def __init__(self, vault_path: str, watch_folder: str):
        super().__init__(vault_path, check_interval=10)
        self.watch_folder = Path(watch_folder)
        self.processed_files = set()
        
        # Ensure watch folder exists
        self.watch_folder.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Watching folder: {self.watch_folder}")
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """Check for new files in watch folder."""
        new_files = []
        
        for file_path in self.watch_folder.iterdir():
            if file_path.is_file() and str(file_path) not in self.processed_files:
                new_files.append({
                    'path': file_path,
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                })
                self.processed_files.add(str(file_path))
        
        return new_files
    
    def create_action_file(self, item: Dict[str, Any]) -> Path:
        """Create action file for new file drop."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_file = self.needs_action / f"FILE_{timestamp}_{item['name']}.md"
        
        content = f"""---
type: file_drop
original_name: {item['name']}
size: {item['size']} bytes
detected: {datetime.now().isoformat()}
priority: medium
status: pending
---

## New File Dropped

**File**: `{item['name']}`  
**Size**: {item['size']:,} bytes  
**Location**: `{item['path']}`  
**Modified**: {item['modified'].strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions

- [ ] Review file contents
- [ ] Determine processing required
- [ ] Move to appropriate project folder
- [ ] Update relevant documentation

## Notes

*Add any observations or decisions here*
"""
        
        action_file.write_text(content, encoding='utf-8')
        return action_file


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python base_watcher.py <vault_path> <watch_folder>")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    watch_folder = sys.argv[2]
    
    watcher = FilesystemWatcher(vault_path, watch_folder)
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nWatcher stopped by user")
        sys.exit(0)
