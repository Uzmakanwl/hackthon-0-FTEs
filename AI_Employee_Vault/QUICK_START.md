# AI Employee - Quick Start Guide

## ⚡ Step-by-Step Setup

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault\scripts
pip install -r requirements.txt
```

### Step 2: Verify Qwen Code Installation

```bash
qwen --version
```

If not installed, follow the installation guide at [Qwen Code GitHub](https://github.com/QwenLM/Qwen)

### Step 3: Open Vault in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select `AI_Employee_Vault` folder

### Step 4: Start the AI Employee

**Windows:**
```bash
cd AI_Employee_Vault\scripts
run.bat
```

**Mac/Linux:**
```bash
cd AI_Employee_Vault/scripts
chmod +x run.sh
./run.sh
```

### Step 5: Test the System

1. **Create a test file** in the `DropFolder/`:
   ```bash
   echo "Please analyze this text and summarize it" > DropFolder/test.txt
   ```

2. **Watch the magic happen:**
   - File Watcher detects the new file
   - Creates action file in `Needs_Action/`
   - Orchestrator triggers Claude Code
   - Claude processes the request
   - Result moves to `Done/`

3. **Check the results:**
   - Open `Dashboard.md` in Obsidian
   - Check `Logs/` for detailed activity

---

## 🔑 API Keys (Optional)

**Bronze Tier:** No API keys required!

**Silver Tier and above:** See [API_KEYS_SETUP.md](API_KEYS_SETUP.md)

---

## 🛠️ Troubleshooting

### Qwen Code Not Found

**Error:** `qwen is not recognized`

**Solution:** Install Qwen Code following the [installation guide](https://github.com/QwenLM/Qwen)

### Python Not Found

**Error:** `python is not recognized`

**Solution:** Install Python 3.13+ from [python.org](https://www.python.org/downloads/)

### Watchdog Not Installed

**Error:** `ModuleNotFoundError: No module named 'watchdog'`

**Solution:**
```bash
pip install watchdog
```

---

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md          # Main status view
├── Company_Handbook.md   # Rules and guidelines
├── Business_Goals.md     # Your objectives
├── DropFolder/           # ← Drop files here
├── Needs_Action/         # Pending items
├── Done/                 # Completed items
└── scripts/              # Python scripts
```

---

## 🎯 What's Next?

After mastering Bronze Tier:

1. **Silver Tier:** Add Gmail and WhatsApp watchers
2. **Gold Tier:** Integrate Odoo ERP and social media
3. **Platinum Tier:** Deploy to cloud for 24/7 operation

See [COMPLETE_FILE_LIST.md](COMPLETE_FILE_LIST.md) for the full roadmap.

---

## 📞 Support

- **Documentation:** [README.md](README.md)
- **API Setup:** [API_KEYS_SETUP.md](API_KEYS_SETUP.md)
- **File List:** [COMPLETE_FILE_LIST.md](COMPLETE_FILE_LIST.md)

---

**Ready to go!** Drop a file in `DropFolder/` and watch your AI Employee get to work! 🚀
