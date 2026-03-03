"""
Orchestrator Module

Main orchestration script that:
1. Monitors the Needs_Action folder for new items
2. Triggers Claude Code to process pending items
3. Updates the Dashboard.md with current status
4. Manages the overall AI Employee workflow

Usage:
    python orchestrator.py /path/to/vault
"""

import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
import time


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Coordinates between watchers, Claude Code, and the Obsidian vault.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 30):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 30)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        
        # Folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.done, self.plans, 
                       self.pending_approval, self.approved]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Track processed files
        self.processed_files: set = set()
        
    def _setup_logging(self) -> None:
        """Set up logging to file and console."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def get_pending_items(self) -> List[Path]:
        """
        Get list of pending action files in Needs_Action folder.
        
        Returns:
            List of paths to pending .md files
        """
        pending = []
        
        for file_path in self.needs_action.glob('*.md'):
            # Skip already processed files
            file_id = f'{file_path.name}_{file_path.stat().st_size}'
            if file_id in self.processed_files:
                continue
            
            pending.append(file_path)
        
        return pending
    
    def get_approved_items(self) -> List[Path]:
        """
        Get list of approved action files.
        
        Returns:
            List of paths to approved .md files
        """
        return list(self.approved.glob('*.md'))
    
    def trigger_qwen(self, prompt: str) -> bool:
        """
        Trigger Qwen Code to process items.
        
        Args:
            prompt: The prompt to send to Qwen Code
            
        Returns:
            True if Qwen was triggered successfully, False otherwise
        """
        self.logger.info('Triggering Qwen Code...')
        
        try:
            # Build the Qwen Code command
            # Using -p (print) mode for non-interactive execution
            # Try multiple possible paths for qwen executable
            import shutil
            
            # First try to find qwen in PATH
            qwen_path = shutil.which('qwen') or shutil.which('qwen.cmd')
            
            # If not found, try common Windows locations
            if not qwen_path:
                import os
                appdata_npm = os.path.join(os.environ.get('APPDATA', ''), 'npm', 'qwen.cmd')
                if os.path.exists(appdata_npm):
                    qwen_path = appdata_npm
            
            # Fallback to 'qwen' command
            if not qwen_path:
                qwen_path = 'qwen.cmd'  # Use .cmd extension for Windows
            
            self.logger.info(f'Using Qwen executable: {qwen_path}')
            
            # Build command with full path
            cmd = [
                qwen_path,
                '-p', prompt
            ]

            # Run Qwen Code in the vault directory
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=str(self.vault_path),  # Set working directory
                shell=True  # Use shell to resolve .cmd files on Windows
            )

            if result.returncode == 0:
                self.logger.info('Qwen Code completed successfully')
                self.logger.debug(f'Output: {result.stdout[:500]}')
                return True
            else:
                self.logger.error(f'Qwen Code failed: {result.stderr}')
                return False

        except subprocess.TimeoutExpired:
            self.logger.error('Qwen Code timed out after 5 minutes')
            return False
        except FileNotFoundError as e:
            self.logger.error(f'Qwen Code not found: {e}. Please ensure qwen is in PATH.')
            return False
        except Exception as e:
            self.logger.error(f'Error triggering Qwen Code: {e}')
            return False
    
    def update_dashboard(self) -> None:
        """
        Update the Dashboard.md with current status.
        """
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found, creating...')
            self.dashboard.write_text('''---
last_updated: {}
status: active
---

# AI Employee Dashboard

*Dashboard will be updated by the orchestrator*
'''.format(datetime.now().isoformat()))
            return
        
        # Count items in each folder
        pending_count = len(list(self.needs_action.glob('*.md')))
        done_count = len(list(self.done.glob('*.md')))
        approval_count = len(list(self.pending_approval.glob('*.md')))
        
        # Read current dashboard
        content = self.dashboard.read_text(encoding='utf-8')
        
        # Update timestamp
        content = content.replace(
            'last_updated: {}'.format(
                content.split('last_updated: ')[1].split('\n')[0] if 'last_updated:' in content else ''
            ),
            'last_updated: {}'.format(datetime.now().isoformat())
        )
        
        # Update stats if possible
        if '| Pending Tasks |' in content:
            content = content.replace(
                '| Pending Tasks | {} |'.format(
                    content.split('| Pending Tasks | ')[1].split(' |')[0]
                ),
                '| Pending Tasks | {} |'.format(pending_count)
            )
        
        if '| Awaiting Approval |' in content:
            content = content.replace(
                '| Awaiting Approval | {} |'.format(
                    content.split('| Awaiting Approval | ')[1].split(' |')[0]
                ),
                '| Awaiting Approval | {} |'.format(approval_count)
            )
        
        # Write updated dashboard
        self.dashboard.write_text(content, encoding='utf-8')
        self.logger.info(f'Dashboard updated: {pending_count} pending, {done_count} done')
    
    def process_approved_items(self) -> None:
        """
        Process items that have been approved by moving them to Done.
        
        This is a simple implementation - in higher tiers, this would
        trigger actual MCP actions.
        """
        approved = self.get_approved_items()
        
        for item in approved:
            self.logger.info(f'Processing approved item: {item.name}')
            
            # For Bronze tier, just move to Done
            dest = self.done / item.name
            item.rename(dest)
            
            self.logger.info(f'Moved to Done: {item.name}')
    
    def run(self) -> None:
        """
        Main orchestration loop.

        Continuously monitors folders and triggers Qwen Code when needed.
        """
        self.logger.info('=' * 60)
        self.logger.info('AI Employee Orchestrator Starting')
        self.logger.info('=' * 60)
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')

        try:
            while True:
                # Update dashboard
                self.update_dashboard()

                # Check for pending items
                pending = self.get_pending_items()

                if pending:
                    self.logger.info(f'Found {len(pending)} pending item(s)')

                    # Build prompt for Qwen
                    pending_files = ', '.join([p.name for p in pending])
                    prompt = f'''Check the Needs_Action folder in the vault. Process these pending items:
{pending_files}

For each item:
1. Read and understand what action is needed
2. Create a Plan.md if multi-step action is required
3. If approval is needed, create a file in Pending_Approval
4. If no approval needed, take the action and move to Done
5. Update the Dashboard.md with progress

Follow the Company_Handbook.md rules for all actions.'''

                    # Trigger Qwen Code
                    success = self.trigger_qwen(prompt)

                    if success:
                        # Mark as processed
                        for item in pending:
                            file_id = f'{item.name}_{item.stat().st_size}'
                            self.processed_files.add(file_id)

                # Check for approved items
                approved = self.get_approved_items()

                if approved:
                    self.logger.info(f'Found {len(approved)} approved item(s)')
                    self.process_approved_items()

                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


def main():
    """Main entry point for the orchestrator."""
    if len(sys.argv) < 2:
        print('Usage: python orchestrator.py <vault_path>')
        print('')
        print('Arguments:')
        print('  vault_path  - Path to your Obsidian vault')
        print('')
        print('Example:')
        print('  python orchestrator.py "C:/Vaults/AI_Employee"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    # Validate path
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create orchestrator and run
    orchestrator = Orchestrator(vault_path)
    orchestrator.run()


if __name__ == '__main__':
    main()
