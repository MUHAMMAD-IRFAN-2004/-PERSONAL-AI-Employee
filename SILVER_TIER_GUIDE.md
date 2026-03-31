# Silver Tier Complete Guide
## Personal AI Employee - Advanced Automation

---

## 🎉 Congratulations on Reaching Silver Tier!

You've successfully set up advanced AI employee capabilities including:
- ✅ **WhatsApp Web Integration** - Monitor important WhatsApp messages
- ✅ **Human-in-the-Loop Approval** - Risk assessment and approval workflows
- ✅ **Social Media Automation** - LinkedIn and Twitter posting automation

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [System Components](#system-components)
6. [Workflow Examples](#workflow-examples)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Architecture](#architecture)

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Playwright** - Browser automation framework
- **Google API credentials** - For Gmail integration
- **Active WhatsApp account** - For WhatsApp monitoring
- **LinkedIn/Twitter accounts** - For social media posting

### Required Python Packages
```bash
pip install -r requirements.txt
```

Key packages:
- `playwright>=1.41.0` - Browser automation
- `watchdog>=4.0.0` - Filesystem monitoring
- `google-api-python-client>=2.116.0` - Gmail API
- `python-dotenv>=1.0.0` - Environment variables

### Playwright Browser Installation
After installing playwright, install browser:
```bash
playwright install chromium
```

---

## Installation

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Edit `.env` and add your credentials:
```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# Twitter Credentials
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password

# Optional: WhatsApp Settings
WHATSAPP_HEADLESS=false
WHATSAPP_CHECK_INTERVAL=30
WHATSAPP_PRIORITY_SENDERS=Boss Name,Client Name

# Optional: Social Media Settings
LINKEDIN_DAILY_LIMIT=5
TWITTER_DAILY_LIMIT=10
POST_DELAY=60
SOCIAL_CHECK_INTERVAL=300

# Optional: Approval System Settings
APPROVAL_CHECK_INTERVAL=10
AUTO_APPROVE_LOW_RISK=true

# Optional: Logging
LOG_LEVEL=INFO
```

### Step 3: Verify Directory Structure

Run the status check:
```bash
check_silver_status.bat
```

This will verify:
- All required directories exist
- All Python scripts are present
- Required packages are installed
- Environment is properly configured

---

## Configuration

### WhatsApp Watcher Configuration

**Priority Senders**: Messages from these contacts will have higher importance scores
```env
WHATSAPP_PRIORITY_SENDERS=Boss Name,Important Client,Manager Name
```

**Important Keywords**: Automatically detected (configured in `whatsapp_watcher.py`):
- urgent, asap, emergency, critical
- payment, invoice, deadline
- meeting, call, help
- approval, confirm, verify

**Check Interval**: How often to check for new messages (seconds)
```env
WHATSAPP_CHECK_INTERVAL=30
```

### Approval System Configuration

**Risk Thresholds**:
- High Risk: Score ≥ 50 (requires approval)
- Medium Risk: Score ≥ 20 (requires approval)
- Low Risk: Score < 20 (auto-approved if enabled)

**Auto-approve Low Risk**:
```env
AUTO_APPROVE_LOW_RISK=true
```

**High-Risk Keywords** (automatically detected):
- Financial: payment, invoice, transaction, transfer
- Destructive: delete, remove, cancel, terminate
- Communications: send email, post, publish, share
- System: deploy, production, execute
- Legal: contract, agreement, sign

### Social Media Configuration

**Rate Limits** (per day):
```env
LINKEDIN_DAILY_LIMIT=5
TWITTER_DAILY_LIMIT=10
```

**Post Delay**: Wait time between posts to different platforms (seconds)
```env
POST_DELAY=60
```

**Queue Check Interval**: How often to check for new posts (seconds)
```env
SOCIAL_CHECK_INTERVAL=300
```

---

## Running the System

### Option 1: Start All Silver Tier Systems

```bash
start_silver_tier.bat
```

This starts:
1. Filesystem Watcher (Bronze)
2. Gmail Watcher (Bronze)
3. WhatsApp Watcher (Silver)
4. Approval System (Silver)

### Option 2: Start Individual Components

**WhatsApp Watcher**:
```bash
python whatsapp_watcher.py
```

**Approval System**:
```bash
python approval_system.py
```

**Social Media Poster**:
```bash
python social_poster.py
```

### Option 3: Start Specific Watchers

```bash
# Bronze tier only
start_watcher.bat

# All watchers (Bronze + WhatsApp)
start_all_watchers.bat
```

---

## System Components

### 1. WhatsApp Watcher (`whatsapp_watcher.py`)

**Purpose**: Monitor WhatsApp Web for important messages

**Features**:
- Persistent browser sessions (no repeated QR scanning)
- QR code authentication on first run
- Keyword-based importance detection
- Priority sender recognition
- Automatic action file creation

**How it works**:
1. Opens WhatsApp Web in browser
2. Waits for QR code authentication (first time only)
3. Monitors for unread messages every N seconds
4. Analyzes message importance based on keywords
5. Creates action files for important messages

**Action File Location**: `AI_Employee_Vault/Needs_Action/`

**First Time Setup**:
1. Run `python whatsapp_watcher.py`
2. Browser window opens showing WhatsApp Web QR code
3. Scan QR code with your phone
4. Session is saved for future runs

### 2. Approval System (`approval_system.py`)

**Purpose**: Route high-risk actions through human approval workflow

**Features**:
- Automatic risk assessment
- File routing based on risk level
- Approval/rejection handling
- Action execution tracking
- Low-risk auto-approval (configurable)

**How it works**:
1. Monitors `Needs_Action/` folder
2. Analyzes each action file for risk factors
3. Routes based on risk level:
   - **High/Medium Risk** → `Pending_Approval/`
   - **Low Risk** → `Approved/` (if auto-approve enabled)
4. User reviews files in `Pending_Approval/`
5. User moves to `Approved/` or `Rejected/`
6. System executes approved actions and archives

**Workflow**:
```
Needs_Action → [Risk Analysis] → High/Medium Risk → Pending_Approval
                                                    ↓
                                            [Human Decision]
                                                    ↓
                                         Approved / Rejected
                                              ↓           ↓
                                           Done       Archived
```

### 3. Social Media Poster (`social_poster.py`)

**Purpose**: Automate posting to LinkedIn and Twitter

**Features**:
- Queue-based posting system
- LinkedIn and Twitter support
- Rate limiting (configurable per platform)
- Session persistence (no repeated logins)
- Post scheduling support
- Automatic success/failure tracking

**How it works**:
1. Monitors `AI_Employee_Vault/Social_Queue/` folder
2. Reads post files with content and metadata
3. Logs into LinkedIn/Twitter (first time only)
4. Posts content to specified platforms
5. Tracks daily post limits
6. Moves completed posts to `Posted/` or `Failed/`

**Post File Format**:
```markdown
---
platforms: linkedin, twitter
scheduled: 2024-01-15T10:00:00
---

Your post content goes here!

This supports multiple lines.
#hashtags #work
```

**Rate Limits**:
- LinkedIn: 5 posts per day (default)
- Twitter: 10 posts per day (default)
- Resets daily at midnight

---

## Workflow Examples

### Example 1: WhatsApp Message → Action → Approval → Execution

1. **WhatsApp message received**:
   ```
   From: Important Client
   Message: "URGENT: We need the payment processed ASAP for invoice #1234"
   ```

2. **WhatsApp Watcher creates action file**:
   - File: `AI_Employee_Vault/Needs_Action/whatsapp_20240115_143022_Important_Client.md`
   - Importance score: 65 (urgent + payment keywords + priority sender)

3. **Approval System analyzes risk**:
   - Risk Level: HIGH
   - Matched keywords: urgent, payment, asap
   - Routes to: `Pending_Approval/`

4. **You review and approve**:
   - Read the action file
   - Verify it's legitimate
   - Move to: `Approved/`

5. **System executes**:
   - Processes the approved action
   - Moves to: `Done/`

### Example 2: Scheduled Social Media Post

1. **Create post file**: `AI_Employee_Vault/Social_Queue/launch_announcement.md`
```markdown
---
platforms: linkedin, twitter
scheduled: 2024-01-20T09:00:00
---

🚀 Excited to announce our new feature launch!

We've been working hard to bring you something amazing.
Check it out: https://example.com/new-feature

#ProductLaunch #Innovation #Tech
```

2. **Social Poster automatically**:
   - Detects post at scheduled time
   - Posts to LinkedIn (count: 1/5)
   - Waits 60 seconds
   - Posts to Twitter (count: 1/10)
   - Moves to `Posted/` with metadata

3. **Results tracked**:
   - `Posted/launch_announcement.md` - original post
   - `Posted/launch_announcement.md.meta.json` - results metadata

### Example 3: Low-Risk Auto-Approval

1. **Gmail Watcher creates action file**:
   - Newsletter subscription confirmation
   - No high-risk keywords detected
   - Risk score: 5 (LOW)

2. **Approval System**:
   - Detects low risk
   - Auto-approves (if enabled)
   - Routes directly to `Approved/`

---

## Troubleshooting

### WhatsApp Watcher Issues

**Problem**: QR code not appearing
- **Solution**: Make sure `WHATSAPP_HEADLESS=false` in `.env`
- Try deleting `.whatsapp_browser_data/` folder and restart

**Problem**: Authentication keeps timing out
- **Solution**: Increase timeout in code or scan QR code faster
- Check phone has internet connection

**Problem**: Not detecting new messages
- **Solution**: 
  - Check if WhatsApp Web is still logged in
  - Verify `WHATSAPP_CHECK_INTERVAL` is appropriate
  - Check logs in `AI_Employee_Vault/Logs/`

**Problem**: Browser crashes
- **Solution**:
  - Update Playwright: `pip install --upgrade playwright`
  - Reinstall browser: `playwright install chromium`

### Approval System Issues

**Problem**: Files not being routed
- **Solution**:
  - Check if `approval_system.py` is running
  - Verify directory permissions
  - Check logs for errors

**Problem**: Risk scores seem wrong
- **Solution**:
  - Review risk keywords in `approval_system.py`
  - Adjust `HIGH_RISK_THRESHOLD` and `MEDIUM_RISK_THRESHOLD`

### Social Media Poster Issues

**Problem**: Login fails
- **Solution**:
  - Verify credentials in `.env`
  - Check for 2FA/security challenges (may need manual login first)
  - Try with `SOCIAL_HEADLESS=false` to see browser

**Problem**: Rate limit reached too quickly
- **Solution**:
  - Adjust limits in `.env`
  - Check `.social_rate_limits.json` file
  - Delete file to reset (will reset all counters)

**Problem**: Posts not being detected
- **Solution**:
  - Verify files are in `Social_Queue/` root (not subfolders)
  - Check file format (must be `.md`)
  - Check if scheduled time has passed

### General Issues

**Problem**: Import errors
- **Solution**: `pip install -r requirements.txt`

**Problem**: Permission errors
- **Solution**: Run Command Prompt as Administrator

**Problem**: Multiple instances running
- **Solution**: Check Task Manager, close duplicate Python processes

---

## Best Practices

### Security

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use strong passwords** - For social media accounts
3. **Review high-risk actions carefully** - Don't blindly approve
4. **Keep logs secure** - May contain sensitive information
5. **Regular backups** - Of action files and configurations

### Operational

1. **Start with auto-approve OFF** - Learn the system first
2. **Review logs daily** - Check for errors or issues
3. **Test with low-risk actions first** - Before processing important items
4. **Keep browser sessions alive** - Don't close browser windows manually
5. **Monitor rate limits** - Don't exceed platform limits

### Performance

1. **Adjust check intervals** - Balance responsiveness vs. resource usage
2. **Clean up old logs** - Periodically archive or delete
3. **Monitor disk space** - Action files accumulate over time
4. **Close unused windows** - Each watcher uses resources

### Content Guidelines

1. **WhatsApp**:
   - Add important contacts to priority senders
   - Customize keywords for your use case
   - Review importance scores and adjust thresholds

2. **Social Media**:
   - Schedule posts in advance
   - Stay within rate limits
   - Review posts before queuing
   - Use appropriate hashtags
   - Check post success in `Posted/` folder

3. **Approval System**:
   - Review pending approvals regularly
   - Don't let pending queue grow too large
   - Adjust risk thresholds based on experience

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SILVER TIER ARCHITECTURE                 │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  DATA SOURCES    │
└──────────────────┘
        │
        ├─── WhatsApp Web ────────┐
        ├─── Gmail API ───────────┤
        └─── Filesystem ──────────┤
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │    WATCHERS LAYER       │
                    │  ┌──────────────────┐   │
                    │  │ WhatsApp Watcher │   │
                    │  │ Gmail Watcher    │   │
                    │  │ Filesystem Watch │   │
                    │  └──────────────────┘   │
                    └─────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   AI_Employee_Vault     │
                    │   /Needs_Action/        │
                    └─────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   APPROVAL SYSTEM       │
                    │   ┌───────────────┐     │
                    │   │ Risk Analysis │     │
                    │   │ File Routing  │     │
                    │   └───────────────┘     │
                    └─────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌──────────┐  ┌─────────┐  ┌──────────┐
              │ LOW RISK │  │ MEDIUM  │  │ HIGH RISK│
              │   AUTO   │  │ PENDING │  │ PENDING  │
              └──────────┘  └─────────┘  └──────────┘
                    │             │             │
                    │      ┌──────┴──────┐      │
                    │      ▼             ▼      │
                    │  ┌─────────┐  ┌─────────┐│
                    │  │APPROVED │  │REJECTED ││
                    │  └─────────┘  └─────────┘│
                    │      │             │      │
                    └──────┴─────────────┴──────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   EXECUTION LAYER       │
                    │   ┌───────────────┐     │
                    │   │ Action Exec   │     │
                    │   │ Social Poster │     │
                    │   └───────────────┘     │
                    └─────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   OUTPUT LAYER          │
                    │   ┌───────────────┐     │
                    │   │ LinkedIn      │     │
                    │   │ Twitter       │     │
                    │   │ Done/         │     │
                    │   └───────────────┘     │
                    └─────────────────────────┘
```

### Data Flow

1. **Input**: WhatsApp/Gmail/Files → Watchers
2. **Processing**: Watchers → Action Files → Needs_Action
3. **Analysis**: Approval System → Risk Assessment
4. **Routing**: Risk-based → Pending_Approval or Auto-Approved
5. **Human Decision**: Review → Approved or Rejected
6. **Execution**: Approved actions → Execution Layer
7. **Output**: Social posts or Done folder

### File Lifecycle

```
WhatsApp Message
    ↓
whatsapp_20240115_143022.md [Needs_Action]
    ↓
[Risk Analysis: Score 65]
    ↓
whatsapp_20240115_143022.md [Pending_Approval]
    ↓
[Human Review]
    ↓
whatsapp_20240115_143022.md [Approved]
    ↓
[Execute Actions]
    ↓
whatsapp_20240115_143022.md [Done]
```

---

## Next Steps: Gold Tier

Ready for the next level? Gold Tier includes:

- **Odoo ERP Integration** - Automate business processes
- **Advanced AI Analysis** - GPT/Claude integration for decision making
- **Multi-channel Orchestration** - Coordinate across all systems
- **Custom Workflows** - Build your own automation recipes
- **Analytics Dashboard** - Track performance and insights

See `GOLD_TIER_GUIDE.md` for details.

---

## Support & Resources

### Documentation
- `00_START_HERE.md` - Getting started guide
- `BRONZE_TIER_COMPLETE.md` - Bronze tier features
- `SILVER_TIER_COMPLETE.md` - Achievement checklist
- `FOLDER_STRUCTURE_EXPLAINED.md` - Directory layout

### Logs
- Check `AI_Employee_Vault/Logs/` for detailed logs
- Each component has its own log file with date stamp

### Status Check
```bash
check_silver_status.bat
```

### Community
- Share your success stories
- Contribute improvements
- Help others troubleshoot

---

## Changelog

### Version 1.0.0 (Initial Silver Tier Release)
- WhatsApp Web monitoring with Playwright
- Human-in-the-loop approval system
- LinkedIn and Twitter automation
- Rate limiting and session management
- Comprehensive logging and error handling

---

**🎉 Congratulations! You're now running a Silver Tier AI Employee!**

Keep building, keep automating, and enjoy your newfound productivity! 🚀
