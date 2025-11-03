# Ecosystem Announcements

**Directory Type:** Outbound Communication
**Purpose:** Broadcast important updates to all ecosystem repositories
**Review Frequency:** As needed (ad-hoc)
**Action Required:** Distribution and tracking

---

## Purpose

This directory contains **ecosystem-wide announcements** intended for broadcast to all repositories in the Liminal Commons ecosystem. These are **outbound communications** that require distribution, not processing.

---

## What Goes Here

Announcements appropriate for this directory:

- 🎯 **Coordination hub launches** (new services available to ecosystem)
- 📢 **Major capability releases** (new patterns, protocols, or tools)
- 🔄 **Breaking changes** affecting multiple repositories
- 📊 **Ecosystem status updates** (quarterly health reports, metrics)
- 🎓 **New patterns or practices** available for adoption
- 🚀 **Waypoint initiations** (multi-repo initiatives starting)

**Do NOT use for:**
- ❌ Individual repository updates (those go in repo-specific releases)
- ❌ Coordination requests to specific repos (use `inbox/coordination/`)
- ❌ Implementation details (use coordination requests)

---

## Announcement Lifecycle

### 1. Creation (Draft)

When creating an announcement:

```markdown
---
title: Announcement Title
type: ecosystem-announcement
created: YYYY-MM-DD
author: Your Name
status: draft | ready | distributed | archived
distribution_date: YYYY-MM-DD (when to send)
trace_id: ecosystem-[topic]-YYYY-MM-DD
target_audience: all_repos | [specific-repo-list]
---

# Announcement: [Title]

## TL;DR
1-2 sentences: What's the news?

## What's Changing
Detailed explanation of the announcement.

## Why This Matters
Impact and value for ecosystem repositories.

## Next Steps
What should repositories do in response?
- Action 1 (timeline)
- Action 2 (timeline)

## Questions?
How to get more information or ask questions.
```

### 2. Distribution (Ready → Distributed)

**Who distributes:** Repository maintainer or coordination hub lead

**Distribution channels:**
1. **Create weekly broadcast** referencing announcement
   - Location: `inbox/coordination/broadcasts/YYYY-MM-DD-[topic].md`
   - Link to full announcement
   - Highlight key action items

2. **Notify target repositories**
   - GitHub notifications (watch/releases)
   - Email to registered maintainers
   - Coordination meeting agenda items

3. **Log distribution event**
   ```bash
   # Log to events.jsonl
   {
     "timestamp": "2025-10-31T10:00:00Z",
     "event_type": "announcement_distributed",
     "trace_id": "ecosystem-coordination-launch-2025-10-31",
     "details": {
       "announcement": "ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md",
       "target_audience": "all_repos",
       "distribution_channels": ["github", "email", "broadcast"]
     }
   }
   ```

### 3. Tracking Responses

**Create response tracking document:**

```markdown
# Response Tracking: [Announcement Title]

**Announcement**: [filename]
**Distributed**: YYYY-MM-DD
**Response Deadline**: YYYY-MM-DD (if applicable)

## Target Repositories

| Repository | Notified | Acknowledged | Action Taken | Notes |
|------------|----------|--------------|--------------|-------|
| chora-base | 2025-10-31 | 2025-10-31 | Adopted inbox protocol | - |
| ecosystem-manifest | 2025-10-31 | pending | - | Response requested by 2025-11-14 |
| mcp-orchestration | 2025-10-31 | pending | - | - |

## Summary
- Total notified: 3
- Acknowledged: 1 (33%)
- Actions taken: 1 (33%)
- Pending: 2 (67%)
```

**Location:** `inbox/ecosystem/announcements/responses/[announcement-name]-tracking.md`

### 4. Archival (Distributed → Archived)

**When to archive:**
- All target repositories have acknowledged (or deadline passed)
- Actions completed or transferred to coordination requests
- 30 days post-distribution with no outstanding responses

**How to archive:**
```bash
# Move to archive subdirectory
mkdir -p inbox/ecosystem/announcements/archive/
mv ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md \
   inbox/ecosystem/announcements/archive/

# Keep response tracking active until all responses received
```

---

## Current Announcements

### Active (Pending Distribution)

**ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md**
- **Status**: Ready for distribution
- **Created**: 2025-10-31
- **Target**: All ecosystem repositories
- **Action Required**:
  1. Create weekly broadcast (2025-11-03-ecosystem-launch.md)
  2. Notify target repositories (3+ repos)
  3. Create response tracking document
  4. Log distribution event

**Next Steps:**
- [ ] Draft weekly broadcast referencing announcement
- [ ] Identify target repository maintainers and contact info
- [ ] Send notifications via GitHub/email
- [ ] Create response tracking document
- [ ] Log `announcement_distributed` event with trace_id

---

## Response Guidelines (For Recipients)

If you receive an ecosystem announcement:

### 1. Acknowledge Receipt (Within 2 business days)

**Via coordination request:**
```json
{
  "trace_id": "[announcement-trace-id]",
  "type": "acknowledgment",
  "source_repo": "your-repo",
  "target_repo": "chora-base",
  "subject": "Acknowledgment: [Announcement Title]",
  "description": "Acknowledged receipt of [announcement]. [Brief response: interested / will review / not applicable / need clarification]"
}
```

**Via email/GitHub comment:**
Simple acknowledgment with initial response.

### 2. Take Action (Per Announcement Timeline)

Follow the "Next Steps" outlined in the announcement:
- Register capabilities
- Adopt new patterns
- Submit coordination requests
- Provide feedback

### 3. Ask Questions

**For clarifications:**
- File coordination request with questions
- Email announcement author
- Open GitHub issue

---

## Templates

### Announcement Template

```markdown
---
title: [Announcement Title]
type: ecosystem-announcement
created: YYYY-MM-DD
author: [Your Name]
status: draft
distribution_date: null
trace_id: ecosystem-[topic]-YYYY-MM-DD
target_audience: all_repos
---

# Ecosystem Announcement: [Title]

**Date**: YYYY-MM-DD
**From**: [Source Repository/Team]
**To**: [Target Audience]

---

## TL;DR

[1-2 sentences summarizing the announcement]

---

## What's Changing

[Detailed explanation of what's new/changing]

---

## Why This Matters

### For All Repositories
- [Benefit/impact 1]
- [Benefit/impact 2]

### For Specific Repository Types
- **[Type 1]**: [Specific value]
- **[Type 2]**: [Specific value]

---

## Next Steps

### Immediate (Within 1 week)
1. [Action 1]
2. [Action 2]

### Short-term (Within 1 month)
1. [Action 3]
2. [Action 4]

### Optional
- [Optional action 1]

---

## Questions & Support

- **Documentation**: [Link to relevant docs]
- **Examples**: [Link to examples]
- **Contact**: [How to ask questions]

---

**Trace ID**: `ecosystem-[topic]-YYYY-MM-DD`
**Response requested by**: YYYY-MM-DD (if applicable)
```

---

## Questions?

- **About this directory**: See [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md)
- **About creating announcements**: Contact repository maintainer
- **About responding to announcements**: Follow "Response Guidelines" above
