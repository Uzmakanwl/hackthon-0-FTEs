# AI Employee - Bronze Tier

A personal AI employee built with Qwen Code and Obsidian that autonomously processes tasks from your local vault.

## Overview

This Bronze Tier implementation provides the foundation for your AI Employee:

- **Obsidian Vault** as the dashboard and memory
- **File System Watcher** to detect new tasks
- **Orchestrator** to trigger Qwen Code for processing
- **Company Handbook** with rules of engagement

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Drop Folder    │────▶│  File Watcher    │────▶│  Needs_Action/  │
│  (Monitored)    │     │  (Python)        │     │  (Vault)        │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Dashboard.md   │◀────│  Orchestrator    │◀────│  Qwen Code      │
│  (Status)       │     │  (Python)        │     │  (Reasoning)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Qwen Code](https://github.com/QwenLM/Qwen) | Latest | AI reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Dashboard/GUI |
| [Node.js](https://nodejs.org/) | v24+ LTS | Qwen Code runtime |

## Installation

### Step 1: Clone or Copy the Vault

Copy the `AI_Employee_Vault` folder to your desired location:

```bash
# Example location
C:\Users\YourName\Obsidian\AI_Employee_Vault
```

### Step 2: Install Python Dependencies

```bash
cd AI_Employee_Vault/scripts
pip install -r requirements.txt
```

### Step 3: Configure API Keys (Optional)

**Bronze Tier:** No API keys required! Skip to Step 4.

**Silver Tier and above:** See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for detailed instructions.

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
```

### Step 4: Verify Qwen Code Installation

```bash
qwen --version
```

If not installed, follow the installation guide at [Qwen Code GitHub](https://github.com/QwenLM/Qwen)

### Step 5: Open Vault in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `AI_Employee_Vault` folder

## Usage

### Option A: Run Watchers Separately

**Terminal 1 - Start File System Watcher:**

```bash
cd AI_Employee_Vault/scripts

# Windows
python filesystem_watcher.py "C:\Path\To\AI_Employee_Vault" "C:\Path\To\DropFolder"

# Unix/Mac
python filesystem_watcher.py "/path/to/AI_Employee_Vault" "/path/to/DropFolder"
```

**Terminal 2 - Start Orchestrator:**

```bash
cd AI_Employee_Vault/scripts

# Windows
python orchestrator.py "C:\Path\To\AI_Employee_Vault"

# Unix/Mac
python orchestrator.py "/path/to/AI_Employee_Vault"
```

### Option B: Use Helper Scripts (Recommended)

**Windows:**

Create `start.bat`:
```batch
@echo off
start "File Watcher" cmd /k "cd scripts && python filesystem_watcher.py ".." "../DropFolder""
start "Orchestrator" cmd /k "cd scripts && python orchestrator.py "..""
```

**Mac/Linux:**

Create `start.sh`:
```bash
#!/bin/bash
python scripts/filesystem_watcher.py . ./DropFolder &
python scripts/orchestrator.py .
```

## How It Works

### 1. Drop a File

Place any file in the monitored drop folder:
- Text documents
- Images
- PDFs
- Any file type

### 2. Watcher Detects

The `filesystem_watcher.py` script:
- Detects the new file within 5 seconds
- Copies it to `Needs_Action/` folder
- Creates a metadata `.md` file with:
  - File name and size
  - Timestamp
  - Suggested actions

### 3. Orchestrator Triggers Claude

The `orchestrator.py` script:
- Checks `Needs_Action/` every 30 seconds
- When items found, triggers Claude Code with prompt
- Claude reads the item and Company_Handbook.md
- Creates Plan.md if multi-step action needed

### 4. Claude Processes

Claude Code:
- Reads the pending item
- Understands what action is needed
- Follows Company_Handbook.md rules
- Creates approval request if needed
- Moves completed items to `Done/`

### 5. Dashboard Updates

After each cycle:
- Dashboard.md shows current stats
- Pending tasks count updated
- Recent activity logged

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Real-time status
├── Company_Handbook.md    # Rules of engagement
├── Business_Goals.md      # Q1 2026 objectives
├── Inbox/                 # Raw incoming items
├── Needs_Action/          # Items pending processing
├── Plans/                 # Generated plans
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Human-approved items
├── Rejected/              # Human-rejected items
├── Done/                  # Completed tasks
├── Accounting/            # Financial records
├── Briefings/             # CEO briefings
├── Invoices/              # Generated invoices
├── Logs/                  # System logs
└── scripts/
    ├── base_watcher.py
    ├── filesystem_watcher.py
    ├── orchestrator.py
    └── requirements.txt
```

## Configuration

### Adjust Check Intervals

Edit the watcher scripts:

```python
# filesystem_watcher.py - Line ~50
check_interval: int = 5  # Seconds between file checks

# orchestrator.py - Line ~20
check_interval: int = 30  # Seconds between Claude triggers
```

### Add Custom Rules

Edit `Company_Handbook.md` to add your own rules:
- Payment thresholds
- Communication guidelines
- Auto-approve actions
- Require approval actions

## Testing

### Test the File Watcher

1. Start the filesystem watcher
2. Drop a test file in the monitored folder
3. Check `Needs_Action/` for new files:
   - Original file copied
   - `.md` metadata file created

### Test the Orchestrator

1. Start the orchestrator
2. Ensure there's a pending item in `Needs_Action/`
3. Watch logs for Qwen Code trigger
4. Check `Done/` after Qwen completes

### Test Qwen Code Integration

```bash
# Manual Qwen Code test
qwen -p "Read Dashboard.md and summarize the current status"
```

## Logs

Logs are stored in `Logs/` folder:

- `watcher_YYYYMMDD.log` - File watcher activity
- `orchestrator_YYYYMMDD.log` - Orchestrator activity

View logs:
```bash
# Windows
type Logs\watcher_20260107.log

# Unix/Mac
tail -f Logs/watcher_20260107.log
```

## Troubleshooting

### Qwen Code Not Found

```bash
# Verify installation
qwen --version

# Reinstall if needed - follow Qwen Code installation guide
```

### Watcher Not Detecting Files

1. Check drop folder path is correct
2. Verify folder permissions allow reading
3. Check watcher logs for errors

### Orchestrator Not Triggering Qwen

1. Verify Qwen Code is installed
2. Check orchestrator logs
3. Test Qwen manually (see above)

### Files Not Moving to Done

1. Check if approval is required
2. Review Company_Handbook.md rules
3. Check Qwen output in logs

## Next Steps (Silver Tier)

After mastering Bronze tier, add:

1. **Gmail Watcher** - Monitor email inbox
2. **WhatsApp Watcher** - Monitor messages
3. **MCP Servers** - Enable external actions
4. **Approval Workflow** - Human-in-the-loop
5. **Scheduled Tasks** - Cron/Task Scheduler

## Security Notes

- **Never** store credentials in the vault
- Use environment variables for API keys
- Review all auto-approved actions regularly
- Keep logs for audit purposes

## License

This project is part of the Personal AI Employee Hackathon 0.

## Resources

- [Hackathon Document](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code GitHub](https://github.com/QwenLM/Qwen)
- [Obsidian Help](https://help.obsidian.md)
- [Watchdog Docs](https://pypi.org/project/watchdog/)

---

*AI Employee v0.1 - Bronze Tier*
