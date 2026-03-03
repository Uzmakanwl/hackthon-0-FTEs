# How AI Employee Works - Complete Guide

## 🎯 Overview

Your AI Employee is an autonomous agent that:
1. **Watches** for new tasks (files dropped in a folder)
2. **Thinks** about what needs to be done (using Qwen Code)
3. **Acts** by processing tasks and updating your vault

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOU (Human)                              │
│  - Drop files in DropFolder/                                │
│  - Review approvals in Pending_Approval/                    │
│  - Check Dashboard.md for status                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  PERCEPTION LAYER                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ File System Watcher (filesystem_watcher.py)         │   │
│  │ - Monitors DropFolder/ for new files                │   │
│  │ - Copies files to Needs_Action/                     │   │
│  │ - Creates .md action files with metadata            │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Orchestrator (orchestrator.py)                      │   │
│  │ - Checks Needs_Action/ every 30 seconds             │   │
│  │ - Builds prompt for Qwen Code                       │   │
│  │ - Triggers Qwen Code to process items               │   │
│  │ - Updates Dashboard.md                              │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  REASONING LAYER                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Qwen Code (qwen -p "prompt")                        │   │
│  │ - Reads pending items from Needs_Action/            │   │
│  │ - Reads Company_Handbook.md for rules               │   │
│  │ - Decides what action to take                       │   │
│  │ - Creates Plan.md for complex tasks                 │   │
│  │ - Moves completed items to Done/                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Commands You Need to Run

### Command 1: Start the File Watcher

**What it does:**
- Monitors `DropFolder/` for new files
- When a file is detected:
  - Copies it to `Needs_Action/`
  - Creates a `.md` action file with metadata
  - Logs the activity

**Run this command:**
```bash
cd AI_Employee_Vault\scripts
python filesystem_watcher.py "C:\Path\To\AI_Employee_Vault" "C:\Path\To\AI_Employee_Vault\DropFolder"
```

**Or use the startup script:**
```bash
cd AI_Employee_Vault\scripts
run.bat
```

---

### Command 2: Start the Orchestrator

**What it does:**
- Checks `Needs_Action/` every 30 seconds
- When items are found:
  - Builds a prompt for Qwen Code
  - Triggers Qwen Code with the prompt
  - Marks processed items
- Updates `Dashboard.md` with current stats

**Run this command:**
```bash
cd AI_Employee_Vault\scripts
python orchestrator.py "C:\Path\To\AI_Employee_Vault"
```

**Or use the startup script (runs both watcher + orchestrator):**
```bash
cd AI_Employee_Vault\scripts
run.bat
```

---

## 📝 Step-by-Step Example

### Scenario: Process a Client Inquiry

#### Step 1: Drop a File

Create a file in `DropFolder/`:

```bash
echo "Client John wants a website. Budget: $5000. Timeline: 2 weeks." > DropFolder/client_inquiry.txt
```

#### Step 2: File Watcher Detects

Within 5 seconds, the watcher:
- Detects `client_inquiry.txt`
- Copies it to `Needs_Action/FILE_client_inquiry.txt`
- Creates `Needs_Action/FILE_DROP_client_inquiry_123.md` with:
  ```markdown
  ---
  type: file_drop
  original_name: "client_inquiry.txt"
  size: 123
  received: 2026-03-02T21:00:00Z
  priority: medium
  status: pending
  ---
  
  ## File Drop for Processing
  
  **Original File:** `client_inquiry.txt`
  **Size:** 123 B
  
  ## Suggested Actions
  - [ ] Review file contents
  - [ ] Take any required action
  - [ ] Move to /Done when complete
  ```

#### Step 3: Orchestrator Triggers Qwen

Within 30 seconds, the orchestrator:
- Detects the `.md` file in `Needs_Action/`
- Builds prompt:
  ```
  Check the Needs_Action folder. Process these pending items:
  FILE_DROP_client_inquiry_123.md
  
  For each item:
  1. Read and understand what action is needed
  2. Create a Plan.md if multi-step action is required
  3. If approval is needed, create a file in Pending_Approval
  4. If no approval needed, take the action and move to Done
  5. Update the Dashboard.md with progress
  
  Follow the Company_Handbook.md rules for all actions.
  ```
- Runs: `qwen -p "<prompt>"`

#### Step 4: Qwen Code Processes

Qwen Code:
- Reads `FILE_DROP_client_inquiry_123.md`
- Reads `Company_Handbook.md` for rules
- Understands: "Client inquiry about website project"
- Creates `Plans/PLAN_website_proposal.md`:
  ```markdown
  ---
  created: 2026-03-02T21:01:00Z
  status: in_progress
  ---
  
  ## Objective
  Prepare website proposal for John
  
  ## Steps
  - [x] Identify client: John
  - [x] Budget: $5000
  - [x] Timeline: 2 weeks
  - [ ] Create proposal document
  - [ ] Send to client for approval
  ```
- Moves original file to `Done/`
- Updates `Dashboard.md`

#### Step 5: You Review

Open Obsidian and check:
- `Dashboard.md` - Shows 1 task completed
- `Plans/PLAN_website_proposal.md` - Next steps
- `Done/` - Completed items

---

## 🔄 Continuous Operation

Both scripts run continuously until you stop them:

**Stop with:** `Ctrl+C` in the terminal

**Or on Windows:**
```bash
taskkill /F /IM python.exe
```

---

## 📂 Folder Flow

```
DropFolder/          →  Needs_Action/      →  Done/
(New files here)        (Pending items)       (Completed items)
                              ↓
                         Plans/
                         (Multi-step plans)
                              ↓
                    Pending_Approval/
                    (Needs your approval)
                              ↓
                       Approved/
                       (You approved)
                              ↓
                         Done/
```

---

## 🎛️ Configuration

### Change Check Intervals

**File Watcher** (default: 5 seconds):
```python
# filesystem_watcher.py line ~50
check_interval: int = 5
```

**Orchestrator** (default: 30 seconds):
```python
# orchestrator.py line ~20
check_interval: int = 30
```

### Add Custom Rules

Edit `Company_Handbook.md`:
```markdown
## Payment Rules
- Auto-approve payments under $50
- Require approval for new payees
- Flag transactions over $500
```

---

## 🛠️ Troubleshooting

### "qwen: command not found"

```bash
# Install Qwen Code
# Follow: https://github.com/QwenLM/Qwen
```

### "ModuleNotFoundError: watchdog"

```bash
pip install watchdog
```

### Files not being detected

1. Check watcher is running (see logs)
2. Verify drop folder path is correct
3. Check file permissions

### Qwen not processing items

1. Check orchestrator logs
2. Test Qwen manually:
   ```bash
   qwen -p "Hello, are you there?"
   ```
3. Check Qwen is properly installed

---

## 📊 Monitoring

### Check Logs

```bash
# Windows
type Logs\orchestrator_20260302.log
type Logs\watcher_20260302.log

# Or open in Obsidian
```

### Check Dashboard

Open `Dashboard.md` in Obsidian to see:
- Pending tasks count
- Completed tasks count
- System status

---

## 🎯 Summary of Commands

| Purpose | Command |
|---------|---------|
| **Start everything** | `run.bat` |
| **Start watcher only** | `python filesystem_watcher.py "vault" "drop"` |
| **Start orchestrator only** | `python orchestrator.py "vault"` |
| **Test Qwen** | `qwen -p "Hello"` |
| **Stop all** | `Ctrl+C` or `taskkill /F /IM python.exe` |
| **View logs** | `type Logs\*.log` |

---

## ✅ Quick Test

Run this to test the entire system:

```bash
# 1. Start the system (in one terminal)
cd AI_Employee_Vault\scripts
run.bat

# 2. Drop a test file (in another terminal)
echo "Please summarize this text" > DropFolder\test.txt

# 3. Wait 30-60 seconds

# 4. Check results
dir Needs_Action
dir Done
type Logs\orchestrator_*.log
```

---

**That's it!** Your AI Employee is now working for you 24/7! 🎉
