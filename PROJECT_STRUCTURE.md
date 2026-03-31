# 📁 Personal AI Employee - Project Structure

> **Quick Navigation Guide** - Find any file easily!

---

## 🎯 **QUICK START FILES** (Start Here!)

| File | Description | When to Use |
|------|-------------|-------------|
| **`README.md`** | 📖 Main project documentation | First time setup |
| **`create_vault.bat`** | 🏗️ Creates Obsidian vault structure | Before starting |
| **`.env.example`** | ⚙️ Environment variables template | Copy to `.env` and configure |

---

## 🤖 **PYTHON SCRIPTS** (Watchers & Core Logic)

### Main Watchers
```
📂 Python Scripts/
├── 📄 base_watcher.py          → Template for creating custom watchers
├── 📄 filesystem_watcher.py    → Monitors folders for new files ⭐ EASIEST TO TEST
└── 📄 gmail_watcher.py         → Monitors Gmail for important emails
```

| File | Purpose | Requirements |
|------|---------|--------------|
| **`base_watcher.py`** | Base template for all watchers | None |
| **`filesystem_watcher.py`** | Watches `test_drops/` folder for files | `watchdog` package |
| **`gmail_watcher.py`** | Monitors Gmail unread important emails | Gmail API credentials |

---

## 🪟 **BATCH FILES** (Windows Scripts - Double Click to Run)

### Testing & Setup
```
📂 Batch Scripts/
├── 🔧 create_vault.bat         → Creates AI_Employee_Vault structure
├── ▶️  start_watcher.bat        → Starts filesystem watcher
├── 🧪 test_watcher.bat         → Tests watcher functionality
├── 📊 check_status.bat         → Checks system status
├── 📋 drop_test_file.bat       → Drops a test file
└── ⚡ quick_test.bat           → Quick end-to-end test
```

| File | What It Does | Usage |
|------|--------------|-------|
| **`create_vault.bat`** | Sets up Obsidian vault folders | Run once at start |
| **`start_watcher.bat`** | Launches filesystem watcher | Daily use |
| **`test_watcher.bat`** | Tests if watcher works | Testing |
| **`check_status.bat`** | Shows current status | Diagnostics |
| **`drop_test_file.bat`** | Creates test file in drop folder | Testing |
| **`quick_test.bat`** | Runs complete test cycle | Validation |

---

## 📚 **DOCUMENTATION** (Learning & Reference)

### Core Documentation
```
📂 Documentation/
├── 📖 README.md                                    → Main project guide ⭐
├── 📖 README_VAULT.md                              → Vault setup guide
├── 📖 CLAUDE_CODE_GUIDE.md                         → How to use Claude Code
├── 📖 Personal AI Employee Hackathon 0_...md      → Complete hackathon guide
└── 📖 SAMPLE_ACTION_FILE.md                        → Example action file format
```

### Configuration Documentation
```
📂 Configuration Docs/
├── 📋 Company_Handbook.md          → Rules for AI employee
├── 🎯 Business_Goals.md            → Your business objectives
├── 📊 Dashboard.md                 → Status overview
├── ✅ SETUP_COMPLETE.md            → Setup completion marker
└── 🥉 BRONZE_TIER_COMPLETE.md      → Bronze tier marker
```

---

## ⚙️ **CONFIGURATION FILES**

```
📂 Configuration/
├── 🔧 .env                     → Your credentials (NEVER COMMIT!)
├── 📝 .env.example             → Template for environment variables
├── 📦 requirements.txt         → Python dependencies
├── 🔒 skills-lock.json         → Agent skills configuration
├── 📋 .gitignore              → Git ignore rules
└── 📋 .gitattributes          → Git attributes
```

---

## 📁 **FOLDERS**

### Main Vault (Your AI's Brain)
```
📂 AI_Employee_Vault/           → Main Obsidian vault ⭐
   ├── 📥 Inbox/                → New items appear here
   ├── ⚡ Needs_Action/         → Tasks waiting for processing
   ├── ⏳ In_Progress/          → Currently working on
   ├── ⏸️ Pending_Approval/     → Needs human approval
   ├── ✅ Done/                 → Completed tasks
   └── 📊 Dashboard.md          → Main overview
```

### Testing & Development
```
📂 test_drops/                  → Drop test files here
📂 test_dropss/                 → Additional test folder
📂 .agents/                     → Agent skills (Playwright, etc.)
   └── skills/
       ├── browsing-with-playwright/
       └── find-skills/
```

---

## 📊 **LOG FILES**

```
📝 filesystem_watcher.log       → Filesystem watcher logs
📝 gmail_watcher.log            → Gmail watcher logs (when running)
```

---

## 🗑️ **TEMPORARY/UNUSED FILES** (Can Be Deleted)

```
❌ Untitled.md                  → Empty untitled file
❌ Untitled 1.md                → Empty untitled file
❌ AI_empolyee_Vault/           → Typo folder (use AI_Employee_Vault instead)
```

---

## 🚀 **QUICK WORKFLOWS**

### First Time Setup
```bash
1. Read: README.md
2. Copy: .env.example → .env
3. Edit: .env (add your credentials)
4. Run: create_vault.bat
5. Install: pip install -r requirements.txt
6. Test: start_watcher.bat
```

### Daily Use
```bash
1. Run: start_watcher.bat (starts monitoring)
2. Open: AI_Employee_Vault in Obsidian
3. Check: Needs_Action folder for new tasks
4. Process tasks → move to Done/
```

### Testing
```bash
1. Run: test_watcher.bat
2. Or: drop_test_file.bat
3. Check: AI_Employee_Vault/Needs_Action/
```

---

## 🎯 **HACKATHON TIERS**

| Tier | Files Needed | Status |
|------|--------------|--------|
| 🥉 **Bronze** | filesystem_watcher.py + vault | ✅ COMPLETE |
| 🥈 **Silver** | gmail_watcher.py + MCP | In Progress |
| 🥇 **Gold** | All watchers + automation | Not Started |
| 💎 **Platinum** | Cloud deployment | Not Started |

---

## 📞 **NEED HELP?**

- **Setup Issues**: Check `README.md`
- **Watcher Problems**: Check `filesystem_watcher.log`
- **Vault Structure**: Check `README_VAULT.md`
- **Claude Code**: Check `CLAUDE_CODE_GUIDE.md`

---

## 🔍 **FILE FINDER**

**Can't find a file? Search by purpose:**

- **Want to start the project?** → `README.md`
- **Need to configure credentials?** → `.env.example` → `.env`
- **Want to test quickly?** → `quick_test.bat`
- **Need to create vault?** → `create_vault.bat`
- **Want to monitor files?** → `filesystem_watcher.py`
- **Want to monitor Gmail?** → `gmail_watcher.py`
- **Need to check logs?** → `filesystem_watcher.log`
- **Want to see status?** → `Dashboard.md`

---

**Last Updated**: 2026-03-29  
**Total Files**: 25+ files organized for easy access  
**Status**: Bronze Tier Complete ✅
