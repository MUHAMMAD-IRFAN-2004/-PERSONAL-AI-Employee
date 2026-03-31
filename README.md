# Personal AI Employee 🤖

> Build an autonomous "Digital FTE" that manages your personal and business affairs 24/7

[![Hackathon](https://img.shields.io/badge/Hackathon-2026-blue)](https://panaversity.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-yellow.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-24+-green.svg)](https://nodejs.org)

---

## 🚀 **NEW USER? START HERE!**

**Never seen this before? Read these files in order:**

1. **[00_START_HERE.md](00_START_HERE.md)** - ⭐ Quick start guide (5 min read)
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 📂 Find any file easily
3. **[FILE_INDEX.md](FILE_INDEX.md)** - 📇 Complete alphabetical file list

**Already familiar?** Continue below for complete documentation.

---

A hackathon project for building a **Digital Full-Time Equivalent (FTE)** - an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs with human-in-the-loop oversight.

## 🎯 What is This?

This project implements an **autonomous AI agent** that:

- 📧 Monitors Gmail, WhatsApp, and other communication channels
- 💰 Tracks finances and generates business insights
- 📊 Creates weekly CEO briefings automatically
- 🔄 Manages tasks through an Obsidian vault
- 🤝 Requires human approval for sensitive actions
- 🤖 Runs 24/7 with continuous learning

**Think of it as hiring a senior employee who figures out how to solve problems autonomously.**

## ✨ Key Features

- **Local-First**: All data stored locally in Obsidian
- **Autonomous**: Ralph Wiggum loop keeps working until tasks complete
- **Secure**: Human-in-the-loop for payments and sensitive actions
- **Extensible**: Agent Skills system for modular capabilities
- **Observable**: Complete audit logging of all actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Perception → Reasoning → Action        │
└─────────────────────────────────────────────────┘

📡 Watchers (Python)        🧠 Claude Code         🤲 MCP Servers
├── Gmail Monitor           ├── Read vault         ├── Email
├── WhatsApp Monitor        ├── Create plans       ├── Browser
├── Filesystem Monitor      ├── Make decisions     ├── Calendar
└── Banking Monitor         └── Write reports      └── Social Media
          ↓                         ↓                      ↓
    ┌─────────────────────────────────────────────────────┐
    │           📁 Obsidian Vault (State Management)       │
    │  /Inbox → /Needs_Action → /In_Progress → /Done      │
    └─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/-PERSONAL-AI-Employee.git
cd -PERSONAL-AI-Employee

# Create vault structure
create_vault.bat

# Copy environment template
copy .env.example .env
# Edit .env with your credentials
```

### 2. Install Dependencies

```bash
# Python (using uv - recommended)
uv init
uv add google-auth google-auth-oauthlib google-api-python-client
uv add playwright watchdog

# Or using pip
pip install -r requirements.txt

# Node.js (for MCP servers)
npm install -g @playwright/mcp
```

### 3. Open Vault in Obsidian

1. Open Obsidian
2. "Open folder as vault"
3. Select `AI_Employee_Vault`
4. Customize `Company_Handbook.md` and `Business_Goals.md`

### 4. Run Your First Watcher

```bash
# Test with filesystem watcher (easiest to start)
python base_watcher.py AI_Employee_Vault test_drops
```

Drop a file in `test_drops` folder and watch it appear in `AI_Employee_Vault/Needs_Action`!

## 📚 Documentation

- **[Quick Start Guide](README_VAULT.md)** - Step-by-step setup
- **[Copilot Instructions](.github/copilot-instructions.md)** - Architecture & patterns
- **[Main Guide](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)** - Complete hackathon guide

## 🎓 Hackathon Tiers

### 🥉 Bronze (8-12 hours)
- ✅ Obsidian vault with Dashboard
- ✅ One Watcher script working
- ✅ Basic folder structure
- ✅ Claude Code reading/writing vault

### 🥈 Silver (20-30 hours)
- ✅ Multiple Watchers (Gmail + WhatsApp)
- ✅ MCP server integration
- ✅ Human-in-the-loop approval
- ✅ Automated social posting

### 🥇 Gold (40+ hours)
- ✅ Full Personal + Business automation
- ✅ Odoo accounting integration
- ✅ Weekly CEO briefings
- ✅ Ralph Wiggum autonomous loop

### 💎 Platinum (60+ hours)
- ✅ 24/7 cloud deployment
- ✅ Multi-agent coordination
- ✅ Advanced error recovery
- ✅ Complete business autonomy

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **AI Brain** | Claude Code (or via Claude Code Router) |
| **Knowledge Base** | Obsidian (Markdown) |
| **Watchers** | Python 3.13+ |
| **MCP Servers** | Node.js 24+ |
| **Browser Automation** | Playwright |
| **Accounting** | Odoo Community (optional) |
| **Version Control** | Git |

## 📁 Project Structure

```
-PERSONAL-AI-Employee/
├── .agents/
│   └── skills/
│       ├── browsing-with-playwright/  # Playwright MCP skill
│       └── find-skills/               # Skill discovery
├── .github/
│   └── copilot-instructions.md        # Architecture guide
├── AI_Employee_Vault/                 # Your Obsidian vault
│   ├── Dashboard.md                   # Status overview
│   ├── Company_Handbook.md            # AI rules
│   ├── Business_Goals.md              # Objectives
│   ├── Inbox/                         # New items
│   ├── Needs_Action/                  # Pending tasks
│   ├── Pending_Approval/              # HITL approval
│   └── ...                            # Other folders
├── base_watcher.py                    # Watcher template
├── create_vault.bat                   # Vault setup script
├── .env.example                       # Environment template
└── README.md                          # This file
```

## 🔐 Security

⚠️ **Critical Security Rules**:

1. **Never commit `.env`** - Contains all credentials
2. **Start with `DRY_RUN=true`** - Test safely first
3. **Use test accounts** - Don't test with real banking/email initially
4. **Human approval required** - For payments >$500, important emails
5. **Audit everything** - Check `/Logs/` folder regularly

## 🎯 Use Cases

### Personal
- 📧 Email triage and response drafting
- 💳 Expense tracking and categorization
- 📅 Calendar management
- 📱 WhatsApp monitoring for urgent messages

### Business
- 💰 Invoice tracking and payment reminders
- 📊 Weekly revenue and bottleneck reports
- 🔍 Unused subscription detection
- 📱 Automated LinkedIn posting
- 💼 Client communication management

## 🤝 Contributing

This is a hackathon project for learning. Feel free to:

- Fork and experiment
- Share your implementations
- Join Wednesday research meetings (10 PM)
- Contribute improvements

## 📅 Research Meetings

**Every Wednesday at 10:00 PM**

- Zoom: [Meeting Link](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube: [@panaversity](https://www.youtube.com/@panaversity)

## 📖 Learning Resources

- [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Ecosystem](https://skills.sh/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Obsidian](https://obsidian.md/)

## 🐛 Troubleshooting

### Vault won't open in Obsidian
```bash
# Ensure vault directory exists
cd AI_Employee_Vault
# Create .obsidian folder
mkdir .obsidian
```

### MCP Server won't start
```bash
# Install Playwright browsers
npx playwright install
# Check port availability
netstat -an | findstr "8808"
```

### Watcher not detecting items
```bash
# Test with DRY_RUN=true
set DRY_RUN=true
python base_watcher.py AI_Employee_Vault test_drops
```

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PIAIC AI** for the hackathon framework
- **Anthropic** for Claude Code
- **Obsidian** for the knowledge base platform
- **Skills Ecosystem** for modular agent capabilities

## 🚨 Disclaimer

This is an educational project. When using with real accounts:

- Start with dry-run mode
- Use test/sandbox accounts first
- Review all automated actions
- Understand terms of service for APIs
- Keep credentials secure

## 💡 What's Next?

1. **Complete Bronze Tier** - Get basic vault + one Watcher running
2. **Add MCP Integration** - Enable browser automation
3. **Implement HITL** - Add approval workflow
4. **Scale Up** - Move to Silver/Gold tier features
5. **Deploy to Cloud** - Platinum tier 24/7 operation

---

**Ready to build your AI Employee?** Start with the [Quick Start Guide](README_VAULT.md)!

*Built with ❤️ by the PIAIC AI community*
