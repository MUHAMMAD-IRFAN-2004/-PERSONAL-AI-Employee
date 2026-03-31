# Claude Code Integration Guide - Bronze Tier

## Overview

This guide helps Claude Code work effectively with your AI Employee vault. Claude can read tasks, create plans, and write reports directly in your Obsidian vault.

## Vault Structure

Your vault uses **folder-based state management**:

```
AI_Employee_Vault/
├── Needs_Action/    ← Claude reads tasks from here
├── In_Progress/     ← Claude moves files here when working
├── Done/            ← Claude moves completed tasks here
├── Plans/           ← Claude writes work plans here
└── Dashboard.md     ← Claude updates status here
```

**Key Concept**: File location = task status. Moving a file changes its state.

## How Claude Code Works with the Vault

### 1. Reading Tasks

Claude can list and read files in `Needs_Action/`:

```
Please check /Needs_Action for new tasks
```

Claude will:
- List all `.md` files in the folder
- Read frontmatter to understand priority and type
- Analyze content to determine required actions

### 2. Creating Plans

For complex tasks, Claude creates a plan in `/Plans/`:

```
Create a plan for processing the email from client@example.com
```

Claude will:
- Analyze the task requirements
- Break down into steps
- Write a Plan.md file
- Include success criteria

### 3. Updating Dashboard

Claude keeps Dashboard.md current:

```
Update the dashboard with current status
```

Claude will:
- Count pending items in each folder
- Update financial summary (if provided data)
- Reflect system health
- Add quick notes

### 4. Moving Tasks (State Management)

Claude moves files to change state:

```
Process the task in EMAIL_20260328_client.md and move to Done when complete
```

Claude will:
- Read the task file
- Perform required actions
- Update the file with notes
- Move to /Done when complete

## Bronze Tier Workflows

### Workflow 1: Simple Task Processing

```markdown
**User**: Check Needs_Action and process any pending tasks

**Claude**:
1. Lists files in Needs_Action/
2. Reads each file
3. Determines what action is needed
4. Creates a response or plan
5. Moves completed tasks to Done/
6. Updates Dashboard
```

### Workflow 2: Email Response Drafting

```markdown
**User**: Draft a reply to the email in Needs_Action about project update

**Claude**:
1. Finds email action file in Needs_Action/
2. Reads email content and context
3. Checks Company_Handbook.md for response guidelines
4. Drafts appropriate reply
5. Adds draft to the action file under "## Draft Reply"
6. Moves to Pending_Approval/ (requires human review)
```

### Workflow 3: Daily Briefing

```markdown
**User**: Generate today's briefing

**Claude**:
1. Reads Dashboard.md for current state
2. Counts items in each folder
3. Reviews completed tasks in Done/
4. Checks Business_Goals.md for targets
5. Creates briefing in /Briefings/
6. Updates Dashboard
```

## Example Prompts for Bronze Tier

### Task Management

```
"Check Needs_Action for new tasks"
"Process all pending email tasks"
"Move completed tasks to Done folder"
"Update the dashboard with current status"
```

### Analysis

```
"What are the high priority items in Needs_Action?"
"Summarize all tasks that arrived today"
"List any blocked tasks"
"Check if we're on track with Business_Goals"
```

### Planning

```
"Create a plan for processing today's tasks"
"Break down the project in Active_Project into steps"
"Plan my week based on current tasks and goals"
```

### Reporting

```
"Generate a daily briefing"
"Summarize what was completed this week"
"List all pending approvals"
"Check for overdue tasks"
```

## Claude's Capabilities in Bronze Tier

### ✅ Can Do

- **Read** all files in the vault
- **Write** new files (plans, reports, drafts)
- **Update** existing files (Dashboard, notes)
- **Move** files between folders (state management)
- **Create** structured markdown with frontmatter
- **Analyze** task priority and requirements
- **Draft** emails and responses
- **Generate** daily/weekly reports

### ⚠️ Cannot Do (Without MCP)

- **Send** actual emails (requires email MCP server)
- **Browse** websites (requires Playwright MCP server)
- **Execute** external programs
- **Make** API calls to external services
- **Access** files outside the vault

## File Naming Conventions

Claude should follow these patterns when creating files:

```
Plans:    PLAN_20260328_project_name.md
Reports:  REPORT_20260328_daily_briefing.md
Drafts:   DRAFT_20260328_email_reply.md
Notes:    NOTES_20260328_meeting.md
```

## Frontmatter Template

Claude should use this frontmatter structure:

```yaml
---
type: plan|report|draft|note
created: 2026-03-28T15:00:00Z
priority: high|medium|low
status: pending|in_progress|done
tags: [email, client-a, project-alpha]
---
```

## Best Practices

### 1. Always Read Before Acting

```
Before processing tasks:
1. Read Company_Handbook.md for rules
2. Check Business_Goals.md for priorities
3. Review Dashboard.md for context
```

### 2. Update Status Regularly

```
After completing work:
1. Move task files to appropriate folders
2. Update Dashboard.md
3. Log actions in the task file
4. Add completion notes
```

### 3. Use Human-in-the-Loop for Sensitive Actions

```
For sensitive tasks:
1. Draft the action in the file
2. Move to Pending_Approval/
3. Wait for human to move to Approved/
4. Then proceed with action
```

### 4. Maintain Audit Trail

```
All actions should:
1. Add notes to task files
2. Include timestamp
3. Document decision rationale
4. Reference source documents
```

## Testing Claude Integration

### Test 1: Read Vault

```bash
# Drop a test file
echo "Test task" > AI_Employee_Vault/Needs_Action/test_task.md

# Ask Claude
"Check Needs_Action for tasks"
```

Expected: Claude lists and reads test_task.md

### Test 2: Update Dashboard

```bash
# Ask Claude
"Update Dashboard with current status"
```

Expected: Dashboard.md reflects current folder counts

### Test 3: Create Plan

```bash
# Ask Claude
"Create a plan for organizing my tasks this week"
```

Expected: New file created in Plans/ folder

### Test 4: Move Files

```bash
# Ask Claude
"Process test_task.md and move to Done"
```

Expected: File moved from Needs_Action/ to Done/

## Troubleshooting

### Claude Can't Find Files

**Issue**: "I don't see any files in Needs_Action"

**Solution**:
- Verify folder exists: `AI_Employee_Vault/Needs_Action/`
- Check file permissions
- Confirm Claude has correct vault path

### Claude Won't Update Dashboard

**Issue**: Dashboard isn't being updated

**Solution**:
- Verify Dashboard.md exists in vault root
- Check file isn't read-only
- Ensure proper markdown format

### Files Not Moving

**Issue**: Tasks stay in Needs_Action

**Solution**:
- Explicitly tell Claude to move files
- Use: "Move [filename] to Done folder"
- Verify destination folder exists

## Bronze Tier Completion Checklist

- [ ] Vault folder structure created
- [ ] Dashboard.md, Company_Handbook.md, Business_Goals.md exist
- [ ] At least one Watcher creates files in Needs_Action/
- [ ] Claude can read files from vault
- [ ] Claude can write to vault (Plans, reports)
- [ ] Claude can move files between folders
- [ ] Claude updates Dashboard correctly
- [ ] Workflow tested end-to-end

## Next Steps to Silver Tier

After Bronze is working:

1. **Add Second Watcher** (Gmail or WhatsApp)
2. **Set up MCP Server** (Email or Playwright)
3. **Implement HITL Workflow** (Pending_Approval → Approved)
4. **Add Scheduling** (cron or Task Scheduler)
5. **Create Agent Skills** (modularize functionality)

---

## Quick Reference Commands

```bash
# Point Claude at your vault
claude code --vault "D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault"

# Or set environment variable
export VAULT_PATH="D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault"
claude code
```

---

*This guide covers Bronze Tier only. See main documentation for Silver/Gold tier features.*
