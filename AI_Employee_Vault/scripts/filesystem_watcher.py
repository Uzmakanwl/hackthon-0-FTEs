"""
File System Watcher Module

Monitors a drop folder for new files and creates action files in the Needs_Action folder.
This is the simplest watcher to set up and test for the Bronze tier.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import shutil
from pathlib import Path
import datetime
from datetime import datetime
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handle file system events in the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        self.watcher = watcher
        self.logger = watcher.logger
    
    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return
        
        source_path = Path(event.src_path)
        self.logger.info(f'New file detected: {source_path.name}')
        
        # Create action file for this new file
        self.watcher.process_new_file(source_path)


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a file is added to the drop folder, creates a corresponding
    action file in the Needs_Action folder with metadata.
    """
    
    def __init__(self, vault_path: str, drop_folder: str, check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            drop_folder: Path to the folder to monitor for new files
            check_interval: Seconds between checks (default: 5 for file watcher)
        """
        super().__init__(vault_path, check_interval)
        
        self.drop_folder = Path(drop_folder)
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by their path and size
        self.processed_files: set = set()
        
        self.logger.info(f'Drop folder: {self.drop_folder}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        This method is not used for the file system watcher.
        The watcher uses watchdog event-driven notifications instead.
        
        Returns:
            Empty list (processing happens in event handler)
        """
        return []
    
    def process_new_file(self, source_path: Path) -> Optional[Path]:
        """
        Process a newly detected file.
        
        Args:
            source_path: Path to the new file
            
        Returns:
            Path to the created action file, or None if failed
        """
        # Create unique identifier for this file
        file_id = f'{source_path.name}_{source_path.stat().st_size}'
        
        # Skip if already processed
        if file_id in self.processed_files:
            self.logger.debug(f'File already processed: {source_path.name}')
            return None
        
        # Copy file to vault
        dest_path = self.needs_action / f'FILE_{source_path.name}'
        
        try:
            shutil.copy2(source_path, dest_path)
            self.logger.info(f'Copied file to: {dest_path}')
        except Exception as e:
            self.logger.error(f'Failed to copy file: {e}')
            return None
        
        # Create metadata action file
        action_file = self.create_action_file({
            'source_path': source_path,
            'dest_path': dest_path,
            'file_id': file_id
        })
        
        # Mark as processed
        self.processed_files.add(file_id)
        
        return action_file
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a .md action file for the dropped file.
        
        Args:
            item: Dictionary containing file information
            
        Returns:
            Path to the created action file, or None if failed
        """
        source_path = item['source_path']
        dest_path = item['dest_path']
        file_id = item['file_id']
        
        # Get file metadata
        try:
            file_size = source_path.stat().st_size
            file_mtime = source_path.stat().st_mtime
        except Exception as e:
            self.logger.error(f'Failed to get file metadata: {e}')
            return None
        
        # Generate content
        frontmatter = self.generate_frontmatter(
            item_type='file_drop',
            original_name=f'"{source_path.name}"',
            size=file_size
        )
        
        content = f'''{frontmatter}

## File Drop for Processing

**Original File:** `{source_path.name}`
**Size:** {self._format_size(file_size)}
**Copied To:** `{dest_path}`

## Content

_A file was dropped for processing. Review and take appropriate action._

## Suggested Actions

- [ ] Review file contents
- [ ] Categorize and file appropriately
- [ ] Take any required action
- [ ] Move to /Done when complete

---
*Created by FileSystemWatcher at {datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d %H:%M:%S")}*
'''
        
        # Write action file
        action_path = self.needs_action / f'FILE_DROP_{source_path.stem}_{file_id.split("_")[-1]}.md'
        
        try:
            action_path.write_text(content, encoding='utf-8')
            self.logger.info(f'Created action file: {action_path.name}')
            return action_path
        except Exception as e:
            self.logger.error(f'Failed to write action file: {e}')
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    
    def run(self) -> None:
        """
        Run the file system watcher with watchdog observer.
        
        Uses event-driven notifications instead of polling.
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Drop folder: {self.drop_folder}')
        
        # Set up watchdog observer
        event_handler = DropFolderHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        self.logger.info(f'Watching for new files in: {self.drop_folder}')
        
        try:
            while True:
                # Keep the main thread alive
                # File events are handled by the observer thread
                import time
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
            observer.stop()
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            observer.stop()
        
        observer.join()


def main():
    """Main entry point for the filesystem watcher."""
    if len(sys.argv) < 3:
        print('Usage: python filesystem_watcher.py <vault_path> <drop_folder>')
        print('')
        print('Arguments:')
        print('  vault_path    - Path to your Obsidian vault')
        print('  drop_folder   - Path to folder to monitor for new files')
        print('')
        print('Example:')
        print('  python filesystem_watcher.py "C:/Vaults/AI_Employee" "C:/Users/Me/Drop"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2]
    
    # Validate paths
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create watcher and run
    watcher = FileSystemWatcher(vault_path, drop_folder)
    watcher.run()


if __name__ == '__main__':
    main()
