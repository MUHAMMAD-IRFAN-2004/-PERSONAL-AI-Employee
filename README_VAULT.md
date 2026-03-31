# AI Employee Vault - Quick Start Guide

Welcome to your AI Employee Vault! This guide will help you get started.

## 📁 Vault Structure

Your vault has been initialized with the following folders:

```
AI_Employee_Vault/
├── Inbox/              → New items from Watchers
├── Needs_Action/       → Tasks requiring processing
├── In_Progress/        → Currently active tasks
├── Done/               → Completed tasks
├── Pending_Approval/   → Awaiting your approval
├── Approved/           → Approved actions (triggers MCP)
├── Rejected/           → Rejected actions
├── Plans/              → AI-generated work plans
├── Briefings/          → Weekly CEO briefings
├── Logs/               → Audit logs (JSON format)
├── Accounting/         → Financial records
└── Active_Project/     → Current project files
```

## 🚀 Setup Steps

### 1. Run the Vault Creation Script

```cmd
cd "D:\PIAIC AI\-PERSONAL-AI-Employee"
create_vault.bat
```

This will create all the necessary folders.

### 2. Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Navigate to `D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault`
4. Click "Open"

### 3. Review Core Documents

Open and customize these files:
- **Dashboard.md** - Your daily status overview
- **Company_Handbook.md** - Rules of engagement for your AI
- **Business_Goals.md** - Your objectives and metrics

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env - NEVER commit this file
GMAIL_CLIENT_ID=your_client_id_here
GMAIL_CLIENT_SECRET=your_client_secret_here
WHATSAPP_SESSION_PATH=D:\path\to\whatsapp\session
DRY_RUN=true  # Set to false for production

# Optional
BANK_API_TOKEN=your_token_here
SLACK_WEBHOOK_URL=your_webhook_here
```

### 5. Install Dependencies

For Python Watchers:
```bash
# Using uv (recommended)
uv init
uv add google-auth google-auth-oauthlib google-api-python-client
uv add playwright watchdog

# Or using pip
pip install google-auth google-auth-oauthlib google-api-python-client
pip install playwright watchdog
playwright install
```

For MCP Servers:
```bash
npm install -g @playwright/mcp
```

## 🎯 Your First Task

### Bronze Tier Checklist

- [x] Create vault structure
- [x] Initialize core documents
- [ ] Run vault creation script
- [ ] Open vault in Obsidian
- [ ] Customize Company_Handbook.md with your rules
- [ ] Set your goals in Business_Goals.md
- [ ] Create `.env` file with credentials
- [ ] Install Python dependencies
- [ ] Create your first Watcher script
- [ ] Test Claude Code vault access

### Testing the Vault

1. **Manual Test**: Create a test file in `Needs_Action/`
   ```bash
   echo "Test task" > AI_Employee_Vault/Needs_Action/test.md
   ```

2. **Dashboard Test**: Open Dashboard.md and update the status

3. **Claude Code Test**: Point Claude Code at your vault
   ```bash
   claude code --vault-path "D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault"
   ```

## 📚 Next Steps

### Implement Your First Watcher

Choose one to start:

**Option A: Gmail Watcher**
- Monitors unread important emails
- Creates action files automatically
- Check interval: 2 minutes

**Option B: Filesystem Watcher**
- Monitors a drop folder
- Immediate detection
- Easier to test

**Option C: WhatsApp Watcher**
- Monitors WhatsApp Web
- Keyword-based triggers
- Check interval: 30 seconds

### Set Up MCP Server

1. Start Playwright MCP server:
   ```bash
   bash .agents/skills/browsing-with-playwright/scripts/start-server.sh
   ```

2. Verify it's running:
   ```bash
   python3 .agents/skills/browsing-with-playwright/scripts/verify.py
   ```

3. Test browser automation:
   ```bash
   python3 .agents/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://example.com"}'
   ```

## 🔧 Configuration

### Obsidian Settings

Recommended plugins:
- **Dataview** - Query your vault data
- **Templater** - Create templates for action files
- **Calendar** - Track daily logs
- **Kanban** - Visual task management

### Git Integration

Initialize git for your vault (optional but recommended):

```bash
cd AI_Employee_Vault
git init
git add .
git commit -m "Initial vault setup"
```

Add to `.gitignore`:
```
.env
Logs/*
*.log
.obsidian/workspace*
```

## 📖 Documentation

- **Main Guide**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Copilot Instructions**: `.github/copilot-instructions.md`
- **Playwright Skill**: `.agents/skills/browsing-with-playwright/SKILL.md`
- **Find Skills**: `.agents/skills/find-skills/SKILL.md`

## 🆘 Troubleshooting

### Vault Not Opening in Obsidian
- Make sure the `AI_Employee_Vault` folder exists
- Check folder permissions
- Try creating a `.obsidian` folder manually

### Claude Code Can't Access Vault
- Verify the vault path is correct
- Check file system permissions
- Ensure Dashboard.md exists in the vault root

### MCP Server Not Starting
- Check if port 8808 is available
- Install Playwright: `npx playwright install`
- Review logs for error messages

### Watcher Scripts Not Running
- Verify Python 3.13+ is installed
- Check credentials in `.env`
- Test with DRY_RUN=true first

## 💡 Tips

1. **Start Small**: Begin with Bronze tier, don't try everything at once
2. **Test in Dry-Run**: Always test with DRY_RUN=true
3. **Log Everything**: Check `/Logs/` folder regularly
4. **Human-in-the-Loop**: Approve sensitive actions manually first
5. **Iterate**: Your AI Employee gets better as you refine rules

## 📞 Getting Help

- **Weekly Research Meetings**: Wednesday 10:00 PM
- **YouTube**: https://www.youtube.com/@panaversity
- **Documentation**: Review the main hackathon guide
- **Copilot**: Ask GitHub Copilot CLI for help

## 🎓 Learning Path

1. **Week 1**: Set up vault, create first Watcher
2. **Week 2**: Add MCP server, test browser automation
3. **Week 3**: Implement HITL approval workflow
4. **Week 4**: Add second Watcher, create first briefing
5. **Week 5+**: Scale to Silver/Gold tier features

---

**Ready to build your AI Employee?** Run `create_vault.bat` and open the vault in Obsidian!

*Last Updated: 2026-03-28*
