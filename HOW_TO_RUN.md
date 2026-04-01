# 🚀 How to Run Your AI Employee - Silver Tier

## Quick Start (3 Commands)

### 1️⃣ First Time Setup (5 minutes)

```bash
# Run the setup script
setup_silver_tier.bat
```

This will:
- ✅ Install Python dependencies
- ✅ Install Playwright browsers (including Chromium)
- ✅ Create directory structure
- ✅ Set up .env file

### 2️⃣ Configure Credentials (2 minutes)

Edit `.env` file with your information:

```env
# Required for WhatsApp
WHATSAPP_PRIORITY_SENDERS=Boss Name,Important Client
WHATSAPP_HEADLESS=false

# Required for Social Media (optional)
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
```

### 3️⃣ Start the System (1 command)

```bash
# Start all Silver Tier watchers
start_silver_tier.bat
```

This opens 4 windows:
1. **Filesystem Watcher** - Monitors vault folders
2. **Gmail Watcher** - Monitors email inbox
3. **WhatsApp Watcher** - Monitors WhatsApp messages (opens Chromium)
4. **Approval System** - Routes high-risk actions

---

## Detailed Instructions

### Step-by-Step First Run

#### Step 1: Verify Prerequisites

```bash
# Check Python is installed
python --version

# Should show: Python 3.8 or higher
```

If not installed: [Download Python](https://www.python.org/downloads/)

#### Step 2: Run Setup

```bash
# Double-click this file or run in terminal
setup_silver_tier.bat
```

**What it does:**
- Installs required packages from `requirements.txt`
- Downloads Chromium browser for Playwright
- Creates AI_Employee_Vault folders
- Copies .env.example to .env

**Expected output:**
```
Installing Python packages...
✓ watchdog installed
✓ playwright installed
✓ google-api-python-client installed

Installing Playwright browsers...
✓ Chromium downloaded

Creating directories...
✓ All folders created

Setup complete!
```

#### Step 3: Configure .env

Open `.env` in a text editor and update:

**Minimum configuration:**
```env
# Show browser windows (set false for first time)
WHATSAPP_HEADLESS=false
SOCIAL_HEADLESS=false

# Priority contacts for WhatsApp
WHATSAPP_PRIORITY_SENDERS=Boss Name,Client Name

# Gmail already configured (uses credentials.json)
```

**Optional - Social Media:**
```env
# Only if you want social media posting
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
```

#### Step 4: Start the System

```bash
# Run the start script
start_silver_tier.bat
```

**What happens:**

**Window 1: Filesystem Watcher**
```
Starting Filesystem Watcher...
Watching: AI_Employee_Vault
Monitoring for new files...
```

**Window 2: Gmail Watcher**
```
Starting Gmail Watcher...
Authenticating with Google...
✓ Connected to Gmail
Checking for new emails...
```

**Window 3: WhatsApp Watcher** ⭐ This opens Chromium
```
Starting WhatsApp Watcher...
Starting browser...
Opening WhatsApp Web...

👉 SCAN QR CODE WITH YOUR PHONE
```

**Window 4: Approval System**
```
Starting Approval System...
Monitoring: Needs_Action/
Ready to assess risk...
```

#### Step 5: WhatsApp QR Code (First Time Only)

When Chromium opens with WhatsApp Web:

1. **Get your phone ready**
2. **Open WhatsApp** on your phone
3. **Tap menu (⋮)** > "Linked Devices"
4. **Tap "Link a Device"**
5. **Scan the QR code** shown in the browser
6. **Wait for connection** - Browser shows "WhatsApp Web is active"
7. **Session saved** - You won't need to scan again!

---

## Different Ways to Run

### Option 1: Full Silver Tier (Recommended)

```bash
start_silver_tier.bat
```

**Starts:**
- Filesystem Watcher ✓
- Gmail Watcher ✓
- WhatsApp Watcher ✓ (opens Chromium)
- Approval System ✓

### Option 2: Bronze Tier Only (No WhatsApp)

```bash
start_watcher.bat
```

**Starts:**
- Filesystem Watcher only
- No browser needed

### Option 3: Individual Components

**Just WhatsApp:**
```bash
python whatsapp_watcher.py
```

**Just Gmail:**
```bash
python gmail_watcher.py
```

**Just Approval System:**
```bash
python approval_system.py
```

**Just Social Poster:**
```bash
python social_poster.py
```

### Option 4: Background Mode (Invisible)

1. Edit `.env`:
```env
WHATSAPP_HEADLESS=true
SOCIAL_HEADLESS=true
```

2. Run:
```bash
start_silver_tier.bat
```

Browser runs invisibly in background!

---

## Running Individual Features

### WhatsApp Monitoring

```bash
# Terminal/Command Prompt
python whatsapp_watcher.py
```

**First run:**
- Browser opens (Chromium)
- Shows QR code
- Scan with phone
- Session saved

**Subsequent runs:**
- Loads saved session
- No QR code needed
- Starts monitoring immediately

**What it monitors:**
- Messages from priority senders
- Messages with keywords (urgent, payment, etc.)
- Creates action files for important messages

### Social Media Posting

```bash
# Create a post file first
echo --- > AI_Employee_Vault\Social_Queue\test.md
echo platforms: twitter >> AI_Employee_Vault\Social_Queue\test.md
echo --- >> AI_Employee_Vault\Social_Queue\test.md
echo. >> AI_Employee_Vault\Social_Queue\test.md
echo Hello from my AI Employee! >> AI_Employee_Vault\Social_Queue\test.md

# Then run the poster
python social_poster.py
```

**First run:**
- Browser opens
- Logs into LinkedIn (if configured)
- Logs into Twitter (if configured)
- Posts your content
- Sessions saved

### Approval Workflow

```bash
python approval_system.py
```

**What it does:**
- Monitors `Needs_Action/` folder
- Assesses risk of each action
- Routes to `Pending_Approval/` if risky
- Auto-approves low-risk items (if enabled)

---

## Checking Status

### See What's Running

```bash
# Check status
check_silver_status.bat
```

**Shows:**
- ✓ Python version
- ✓ Installed packages
- ✓ Directory structure
- ✓ Running processes
- ✓ Recent logs

### Check Processes Manually

```bash
# Windows
tasklist | findstr python

# Shows all Python processes
```

### View Logs

```bash
# Open log folder
cd AI_Employee_Vault\Logs

# View recent logs
type whatsapp_watcher_*.log
type gmail_watcher_*.log
type approval_system_*.log
```

---

## Stopping the System

### Stop All Watchers

**Method 1: Close Windows**
- Close each command window
- Browsers close automatically

**Method 2: Ctrl+C**
- Press `Ctrl+C` in each terminal window
- Graceful shutdown

**Method 3: Kill Processes**
```bash
# List Python processes
tasklist | findstr python

# Kill specific process
taskkill /PID <process_id> /F
```

### Stop Individual Components

Just close the specific terminal window or press `Ctrl+C`

---

## Testing the System

### Test 1: Verify Setup

```bash
check_silver_status.bat
```

**Expected:**
```
✓ Python 3.x installed
✓ playwright installed
✓ watchdog installed
✓ google-api-python-client installed
✓ All directories exist
✓ credentials.json valid
```

### Test 2: Test File Drop

```bash
# Drop a test file
drop_test_file.bat
```

**Expected:**
- File appears in `test_drops/`
- Filesystem watcher detects it
- Logs show detection

### Test 3: Test WhatsApp (Manual)

1. Run `python whatsapp_watcher.py`
2. Scan QR code
3. Send yourself a message with "urgent"
4. Check `Needs_Action/` for action file

### Test 4: Test Approval System

1. Create test file:
```bash
echo --- > AI_Employee_Vault\Needs_Action\test.md
echo action: payment >> AI_Employee_Vault\Needs_Action\test.md
echo --- >> AI_Employee_Vault\Needs_Action\test.md
echo Process payment of $1000 >> AI_Employee_Vault\Needs_Action\test.md
```

2. Run `python approval_system.py`

**Expected:**
- File detected
- Risk assessed (HIGH - contains "payment")
- Moved to `Pending_Approval/`

---

## Troubleshooting

### Browser Won't Open

**Problem:** Chromium doesn't start

**Solution:**
```bash
# Install Playwright browsers
playwright install chromium

# Or full installation
python -m playwright install chromium
```

### QR Code Expired

**Problem:** WhatsApp QR code expires before scanning

**Solution:**
1. Set `WHATSAPP_HEADLESS=false` in .env
2. Have phone ready before starting
3. Scan quickly (within 60 seconds)

### Session Lost

**Problem:** WhatsApp asks for QR code again

**Solution:**
- Normal - sessions expire after ~2 weeks
- Just scan QR code again
- Keep watcher running for longer sessions

### Gmail Authentication

**Problem:** Browser opens for Gmail authentication

**Solution:**
1. First time only
2. Click "Allow" to grant Gmail access
3. `token.json` created
4. No re-authentication needed

### Permission Denied

**Problem:** Can't write files

**Solution:**
```bash
# Recreate vault structure
create_vault.bat

# Check folder exists
dir AI_Employee_Vault
```

---

## Running on Startup (Optional)

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "AI Employee Silver Tier"
4. Trigger: "When I log on"
5. Action: "Start a program"
6. Program: `D:\PIAIC AI\-PERSONAL-AI-Employee\start_silver_tier.bat`
7. Save

### Startup Folder

1. Press `Win+R`
2. Type: `shell:startup`
3. Create shortcut to `start_silver_tier.bat`
4. Paste shortcut

---

## Environment Variables Reference

### Essential Settings

```env
# Vault location
VAULT_PATH=D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault

# Browser visibility
WHATSAPP_HEADLESS=false    # Show browser
SOCIAL_HEADLESS=false      # Show browser

# Check intervals (seconds)
WHATSAPP_CHECK_INTERVAL=30
GMAIL_CHECK_INTERVAL=120
APPROVAL_CHECK_INTERVAL=10
```

### WhatsApp Settings

```env
WHATSAPP_PRIORITY_SENDERS=Boss Name,Client Name,Manager
WHATSAPP_HEADLESS=false
WHATSAPP_CHECK_INTERVAL=30
```

### Social Media Settings

```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_DAILY_LIMIT=5

TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_DAILY_LIMIT=10

SOCIAL_HEADLESS=false
POST_DELAY=60
```

### Approval Settings

```env
AUTO_APPROVE_LOW_RISK=true
HIGH_RISK_THRESHOLD=50
MEDIUM_RISK_THRESHOLD=20
```

---

## What Runs When You Start

### 1. Filesystem Watcher
- **Purpose:** Monitors vault folders
- **Watches:** AI_Employee_Vault/Inbox, test_drops
- **Action:** Moves files, creates actions
- **Browser:** ❌ No

### 2. Gmail Watcher
- **Purpose:** Monitors email inbox
- **Checks:** Unread important emails
- **Action:** Creates action files
- **Browser:** ✅ Yes (first time for OAuth)

### 3. WhatsApp Watcher
- **Purpose:** Monitors WhatsApp Web
- **Checks:** Priority contacts, urgent keywords
- **Action:** Creates action files for important messages
- **Browser:** ✅ Yes (Chromium - always)

### 4. Approval System
- **Purpose:** Routes actions by risk level
- **Monitors:** Needs_Action/ folder
- **Action:** Routes to Pending_Approval/ or auto-approves
- **Browser:** ❌ No

### 5. Social Poster (Optional - run separately)
- **Purpose:** Posts to social media
- **Monitors:** Social_Queue/ folder
- **Action:** Posts to LinkedIn/Twitter
- **Browser:** ✅ Yes (Chromium - for posting)

---

## Quick Reference Commands

```bash
# Setup (first time)
setup_silver_tier.bat

# Start system
start_silver_tier.bat

# Check status
check_silver_status.bat

# Individual components
python whatsapp_watcher.py
python gmail_watcher.py
python approval_system.py
python social_poster.py

# Test file drop
drop_test_file.bat

# Verify credentials
verify_credentials.bat
```

---

## Next Steps After Running

1. **Monitor logs** in `AI_Employee_Vault/Logs/`
2. **Check action files** in `Needs_Action/`
3. **Review approvals** in `Pending_Approval/`
4. **Test posting** via `Social_Queue/`
5. **Tune settings** in `.env`

---

**Need Help?**
- Check logs: `AI_Employee_Vault\Logs\`
- Run status check: `check_silver_tier_status.bat`
- Read guides: `SILVER_TIER_GUIDE.md`

**System Ready?**
```bash
start_silver_tier.bat
```

Let your AI Employee work for you! 🤖
