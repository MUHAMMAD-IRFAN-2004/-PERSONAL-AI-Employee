---
type: example_action
from: system
subject: Sample Action File Template
received: 2026-03-28T16:00:00Z
priority: medium
status: pending
---

# Sample Action File

This is a template for action files that Watchers create in the `/Needs_Action` folder.

## Overview

When a Watcher detects something that requires attention, it creates a markdown file like this one. The file contains:

1. **Frontmatter** (YAML between `---` lines) - Structured metadata
2. **Content** - Details about what was detected
3. **Suggested Actions** - Checklist of possible next steps
4. **Notes** - Space for AI or human observations

## Frontmatter Fields

The frontmatter should include:

```yaml
---
type: email|whatsapp|file_drop|transaction|alert
from: source_identifier
subject: brief_description
received: ISO_8601_timestamp
priority: high|medium|low
status: pending|in_progress|done|blocked
---
```

### Common Types

- **email**: From Gmail Watcher
- **whatsapp**: From WhatsApp Watcher
- **file_drop**: From Filesystem Watcher
- **transaction**: From Banking Watcher
- **alert**: From monitoring systems

### Priority Levels

- **high**: Requires action within 4 hours (client requests, payments, outages)
- **medium**: Requires action within 24 hours (routine inquiries, updates)
- **low**: Requires action within 48 hours (nice-to-haves, research)

### Status Values

- **pending**: Not yet started
- **in_progress**: Currently being worked on
- **done**: Completed
- **blocked**: Cannot proceed (waiting on something)

## Content Section

Provide context about what was detected:

**Example for Email**:
```markdown
## Email Content

From: client@example.com
Subject: Project Update Request
Date: 2026-03-28 10:30 AM

Hi [Your Name],

Could you send me an update on the current project status?
We have a stakeholder meeting tomorrow.

Thanks!
```

**Example for Transaction**:
```markdown
## Transaction Details

Amount: $49.99
Merchant: Adobe Creative Cloud
Category: Software Subscription
Date: 2026-03-28
Account: Business Checking (***1234)

Status: Posted
```

**Example for File Drop**:
```markdown
## File Details

Filename: client_invoice_draft.pdf
Size: 234 KB
Format: PDF
Dropped: 2026-03-28 14:30
Location: Desktop/drop_folder/

Preview: Invoice draft for Client A, amount $2,500
```

## Suggested Actions

Provide a checklist of possible next steps. AI Employee will consider these when planning.

### For Emails:
- [ ] Draft reply
- [ ] Forward to relevant team member
- [ ] Schedule meeting
- [ ] Add to calendar as reminder
- [ ] Mark as done after responding

### For Transactions:
- [ ] Verify against budget
- [ ] Categorize expense
- [ ] Check if approved vendor
- [ ] Update accounting records
- [ ] Flag if over threshold

### For Files:
- [ ] Review contents
- [ ] Move to project folder
- [ ] Share with relevant parties
- [ ] Convert format if needed
- [ ] Archive original

## Decision Context

Provide any additional context that helps with decision-making:

```markdown
## Context

- This client is Tier 1 (VIP) - response within 2 hours required
- Previous updates sent on: March 20, March 25
- Project deadline: April 15
- Next milestone: April 1
- Current project status: 65% complete
```

## Approval Required?

If human approval is needed, clearly state:

```markdown
## ⚠️ Human Approval Required

This action requires approval because:
- Payment amount: $2,500 (threshold: $500)
- New vendor: First time working with this client
- Sensitive information: Contains financial data

**To Approve**: Move this file to `/Approved/`
**To Reject**: Move this file to `/Rejected/`
**To Modify**: Edit suggested actions and save
```

## AI Notes

Section for AI observations and decisions:

```markdown
## AI Observations

- Analyzed email sentiment: Neutral/Professional
- Detected urgency indicators: "tomorrow", "stakeholder meeting"
- Cross-referenced with calendar: Meeting found for 2026-03-29 9:00 AM
- Previous response time: 3.2 hours average
- Recommended priority: HIGH due to VIP status + deadline

## Proposed Action

1. Draft comprehensive project update email
2. Include: Progress (65%), upcoming milestones, blockers (if any)
3. Attach visual progress chart from project dashboard
4. Request feedback on current direction
5. Offer to join stakeholder meeting if helpful

**Confidence**: 85%
**Estimated time**: 15 minutes to draft
**Waiting on**: Dashboard data refresh (ETA: 5 minutes)
```

## Human Notes

Section for human observations after review:

```markdown
## Human Review Notes

- Reviewed on: 2026-03-28 15:00
- Decision: Approved with modifications
- Changes: Add mention of budget under-run by 15%
- Additional context: Client mentioned concerns about timeline in last call
- Follow-up: Schedule check-in call for next week

Reviewed by: [Your Name]
```

## File Naming Convention

Action files should follow this pattern:

```
{TYPE}_{TIMESTAMP}_{IDENTIFIER}.md

Examples:
EMAIL_20260328_150030_client_update.md
TRANSACTION_20260328_143000_adobe.md
FILE_20260328_140000_invoice.md
WHATSAPP_20260328_120000_urgent.md
```

## Example Complete Action File

```markdown
---
type: email
from: important.client@example.com
subject: Project Update Request
received: 2026-03-28T10:30:00Z
priority: high
status: pending
---

## Email Content

From: important.client@example.com
Subject: Project Update Request
Received: 2026-03-28 10:30 AM

[Email content here]

## Suggested Actions

- [ ] Draft comprehensive reply
- [ ] Include progress metrics
- [ ] Mention upcoming milestones
- [ ] Offer to join stakeholder meeting
- [ ] Send within 2 hours (VIP SLA)

## Context

- Client Tier: 1 (VIP)
- SLA: < 2 hour response time
- Project: Client A Website Redesign
- Status: 65% complete
- Deadline: April 15, 2026

## AI Observations

- Urgency: High (stakeholder meeting tomorrow)
- Sentiment: Professional, neutral
- Recommended action: Draft detailed update
- Confidence: 90%

## Human Review

Status: ⏳ Awaiting review
Move to `/Approved/` to proceed or `/Rejected/` to cancel
```

---

**This is a template file.** Delete it after reviewing or keep it as reference in `/Plans/` folder.
