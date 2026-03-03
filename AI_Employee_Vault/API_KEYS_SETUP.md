# API Keys Setup Guide

This guide explains where to get API keys and how to configure them for your AI Employee.

---

## Quick Start (Bronze Tier)

**Good news!** The Bronze tier doesn't require any API keys. You can start using the file system watcher and Claude Code CLI right away.m, 

---

## Silver Tier API Configuration

### 1. Gmail API Setup

For the Gmail Watcher to monitor your inbox:

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "AI Employee")
3. Enable the **Gmail API**

#### Step 2: Create OAuth Credentials
1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Desktop app** as the application type
4. Download the credentials JSON file

#### Step 3: Get Refresh Token
Run this Python script to get your refresh token:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    ['https://www.googleapis.com/auth/gmail.readonly']
)
creds = flow.run_local_server(port=0)
print(f"Refresh Token: {creds.refresh_token}")
```

#### Step 4: Update .env File
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your credentials
GMAIL_CLIENT_ID=your_client_id_here
GMAIL_CLIENT_SECRET=your_client_secret_here
GMAIL_REFRESH_TOKEN=your_refresh_token_here
```

---

### 2. Bank API Setup

For automatic transaction tracking:

#### Option A: Plaid (Recommended)
1. Sign up at [Plaid](https://plaid.com/)
2. Create an app in the Plaid Dashboard
3. Get your API keys from **Keys** section
4. Update `.env`:
   ```
   BANK_API_TOKEN=your_plaid_access_token
   BANK_API_KEY=your_plaid_public_key
   ```

#### Option B: Manual CSV Import (No API Required)
1. Download transaction CSV from your bank
2. Drop it in the `DropFolder/`
3. AI Employee will process and categorize automatically

---

### 3. WhatsApp Integration

For WhatsApp message monitoring:

**Note:** WhatsApp doesn't have an official public API for personal accounts. The current implementation uses WhatsApp Web automation.

1. Install Playwright:
   ```bash
   pip install playwright
   playwright install
   ```

2. The session will be stored locally in the path specified:
   ```
   WHATSAPP_SESSION_PATH=C:/Users/YOUR_USERNAME/whatsapp_session
   ```

---

### 4. Email MCP (For Sending Emails)

To enable automatic email sending:

#### Step 1: Enable App Password in Gmail
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an **App Password**
4. Update `.env`:
   ```
   EMAIL_MCP_ENABLED=true
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password_here
   ```

---

## Configuration File Locations

| File | Purpose | Location |
|------|---------|----------|
| `.env` | Your actual API keys (NEVER commit!) | `AI_Employee_Vault/.env` |
| `.env.example` | Template with placeholders | `AI_Employee_Vault/.env.example` |
| `config.py` | Configuration loader | `AI_Employee_Vault/scripts/config.py` |

---

## Security Best Practices

1. **Never commit `.env`** to version control
2. **Use environment variables** instead of hardcoding keys
3. **Rotate credentials** monthly
4. **Use app-specific passwords** instead of main passwords
5. **Enable DRY_RUN mode** when testing new integrations

---

## Verification

After configuring API keys, run:

```bash
cd AI_Employee_Vault/scripts
python -c "from config import config; print('Configured:', config.is_configured())"
```

---

## Tier Requirements Summary

| Tier | Required API Keys |
|------|------------------|
| **Bronze** | None - File system only |
| **Silver** | Gmail API (optional) |
| **Gold** | Gmail + Bank API + MCP servers |
| **Platinum** | All above + Cloud deployment |

---

## Troubleshooting

### "Invalid Client ID" Error
- Double-check credentials in `.env`
- Ensure OAuth consent screen is configured in Google Cloud

### "Token Expired" Error
- Refresh tokens expire after 1 year
- Re-run the OAuth flow to get a new token

### "API Not Enabled" Error
- Enable the required API in Google Cloud Console
- Wait 5 minutes for propagation

---

*For more help, refer to the main [README.md](README.md)*
