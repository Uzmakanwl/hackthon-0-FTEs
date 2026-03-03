# Personal AI Employee Hackathon 0 - QWEN.md

## Project Overview

This is a **hackathon project** for building a **Digital FTE (Full-Time Equivalent)** — an autonomous AI agent that manages personal and business affairs 24/7. The system uses **Claude Code** as the reasoning engine and **Obsidian** as the local-first dashboard/memory.

### Core Architecture

```
Perception (Watchers) → Reasoning (Claude Code) → Action (MCP Servers)
```

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Perception** | Python Watcher Scripts | Monitor Gmail, WhatsApp, filesystems for triggers |
| **Reasoning** | Claude Code | Brain/decision engine with Ralph Wiggum persistence loop |
| **Memory/GUI** | Obsidian Vault | Local Markdown dashboard (Dashboard.md, Company_Handbook.md) |
| **Action** | MCP Servers | Hands for external actions (email, browser, payments) |

### Tech Stack

- **AI Engine**: Claude Code (Pro or Free via Gemini API Router)
- **Dashboard**: Obsidian v1.10.6+
- **Automation**: Python 3.13+, Node.js v24+
- **Browser Automation**: Playwright MCP (installed skill)
- **Version Control**: GitHub Desktop

---

## Building and Running

### Prerequisites Setup

1. **Install Required Software**:
   ```bash
   # Verify installations
   claude --version
   python --version  # Should be 3.13+
   node --version    # Should be v24+ LTS
   ```

2. **Create Obsidian Vault**:
   - Name: `AI_Employee_Vault`
   - Folder structure: `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`, `/Pending_Approval`

3. **Set Up Python Project** (using UV):
   ```bash
   uv init ai_employee
   uv add google-api-python-client playwright watchdog
   ```

### Key Commands

#### Playwright MCP Server (Browser Automation)

```bash
# Start server (required for web automation tasks)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Stop server (after browser tasks complete)
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh

# Verify server is running
python3 .qwen/skills/browsing-with-playwright/scripts/verify.py
```

#### Watcher Scripts (Create these based on hackathon docs)

```bash
# Example: Start Gmail Watcher
python watchers/gmail_watcher.py

# Example: Start WhatsApp Watcher
python watchers/whatsapp_watcher.py

# Example: Start File System Watcher
python watchers/filesystem_watcher.py
```

#### Claude Code Commands

```bash
# Basic invocation pointed at vault
claude --prompt "Check /Needs_Action and process pending items"

# Ralph Wiggum Loop (for multi-step autonomous tasks)
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

#### Scheduled Operations (Windows Task Scheduler)

```bash
# Daily Briefing at 8:00 AM
schtasks /create /tn "AI_Daily_Briefing" /tr "claude --prompt 'Generate Monday Morning CEO Briefing'" /sc daily /st 08:00
```

---

## Development Conventions

### Folder Structure

```
AI_Employee_Vault/
├── Inbox/              # Raw incoming items
├── Needs_Action/       # Items requiring processing
├── In_Progress/        # Currently being handled (claim-by-move rule)
├── Done/               # Completed tasks
├── Plans/              # Generated plan files
├── Pending_Approval/   # HITL approval requests
├── Approved/           # User-approved actions
├── Rejected/           # User-rejected actions
├── Accounting/         # Bank transactions, invoices
├── Briefings/          # CEO Briefings (generated)
├── Dashboard.md        # Real-time summary
└── Company_Handbook.md # Rules of engagement
```

### File Naming Conventions

- **Action Files**: `TYPE_Description_YYYY-MM-DD.md` (e.g., `EMAIL_Client_Inquiry_2026-01-07.md`)
- **Approval Requests**: `APPROVAL_Action_Recipient_Date.md`
- **Plans**: `Plan_TaskName_Date.md`
- **Briefings**: `YYYY-MM-DD_Day_Briefing.md`

### Markdown Schema Standards

All files should use YAML frontmatter:

```yaml
---
type: email|whatsapp|payment|task|approval_request
from: Sender Name
subject: Subject Line
received: 2026-01-07T10:30:00Z
priority: high|medium|low
status: pending|in_progress|done|approved|rejected
---
```

### Human-in-the-Loop (HITL) Pattern

For sensitive actions (payments, sending messages):

1. Claude writes approval request to `/Pending_Approval/`
2. User reviews and moves file to `/Approved/` or `/Rejected/`
3. Orchestrator triggers MCP action only for approved items

### Claim-by-Move Rule (Multi-Agent)

- First agent to move item from `/Needs_Action/` to `/In_Progress/<agent>/` owns it
- Other agents must ignore items in `/In_Progress/` folders
- Prevents duplicate work

### Code Style

- **Python**: Use `pathlib` for paths, type hints, logging module
- **Node.js**: ES modules, async/await pattern
- **Markdown**: GitHub-flavored, consistent frontmatter

### Testing Practices

1. **Unit Test Watchers**: Mock API responses, verify file creation
2. **Integration Test**: Run full perception→reasoning→action loop
3. **HITL Test**: Verify approval workflow blocks unauthorized actions

---

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hrs | Obsidian vault, 1 watcher, Claude reading/writing |
| **Silver** | 20-30 hrs | 2+ watchers, Plan.md generation, 1 MCP server, HITL |
| **Gold** | 40+ hrs | Full integration, Odoo MCP, social media, CEO Briefing, Ralph loop |
| **Platinum** | 60+ hrs | Cloud deployment, Cloud/Local split, A2A upgrade, 24/7 operation |

---

## Available Skills

- **browsing-with-playwright**: Browser automation for web scraping, form submission, UI testing

---

## Resources

- **Main Documentation**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Playwright Tools Reference**: `.qwen/skills/browsing-with-playwright/references/playwright-tools.md`
- **Ralph Wiggum Pattern**: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
- **Agent Skills Docs**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

---

## Weekly Research Meeting

- **When**: Wednesdays at 10:00 PM (Zoom)
- **First Meeting**: January 7th, 2026
- **Meeting ID**: 871 8870 7642
- **Passcode**: 744832
- **Backup Stream**: https://www.youtube.com/@panaversity
