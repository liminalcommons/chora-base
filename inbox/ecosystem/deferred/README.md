# Deferred Proposals

**Status:** Not accepted for current roadmap
**Purpose:** Preserve ideas for future consideration
**Review:** Next quarterly planning session

---

## Purpose

This directory contains strategic proposals that were **deferred** or **rejected** during quarterly review, along with the rationale for why they weren't accepted.

## Why Defer/Reject?

Common reasons:
- ⏰ **Timing** - Good idea, wrong time (capacity, priorities)
- 🎯 **Alignment** - Doesn't align with current strategic direction
- 🔬 **Needs Research** - Requires more investigation before deciding
- 💰 **ROI** - Benefit doesn't justify effort at this time
- 🚫 **Out of Scope** - Better suited for different project/ecosystem

---

## Format

When moving a proposal to deferred/, add a frontmatter section with decision metadata:

```markdown
---
title: Original Proposal Title
type: strategic-proposal
created: YYYY-MM-DD
reviewed: YYYY-MM-DD
status: deferred | rejected
decision: |
  Brief explanation of why this was deferred or rejected.
  What would need to change for us to reconsider?
next_review: YYYY-MM-DD (for deferred items)
decision_makers: [List of people who made decision]
---

# [Original Proposal Content]

...
```

---

## Example

```markdown
---
title: Implement Real-Time Collaboration Features
type: strategic-proposal
created: 2025-10-15
reviewed: 2025-10-27
status: deferred
decision: |
  Deferred to Q2 2026. While real-time collaboration would be valuable,
  we need to complete W3 health monitoring first (current priority).
  Additionally, this would require websocket infrastructure we don't
  have yet. Revisit after W3 is stable.
next_review: 2026-04-01
decision_makers: [Victor, Team]
---

# Proposal: Implement Real-Time Collaboration Features

[Original proposal content...]
```

---

## Review Process

Deferred proposals are reviewed:
- **Quarterly** - During strategic planning sessions
- **On Request** - If circumstances change (e.g., new requirements, capacity opens up)

### Decision Matrix

| Status | Meaning | Next Review | Action |
|--------|---------|-------------|--------|
| **Deferred (Timing)** | Good idea, wrong time | Next quarter | Move back to proposals/ for re-review |
| **Deferred (Research)** | Needs investigation | After research complete | Create research task |
| **Rejected (Alignment)** | Doesn't fit direction | Not scheduled | Keep for historical reference |
| **Rejected (Out of Scope)** | Wrong project | Not scheduled | Suggest alternative home |

---

## Resurrection Process

To resurrect a deferred proposal:
1. Check if circumstances have changed
2. Update proposal with new context
3. Move back to [`inbox/ecosystem/proposals/`](../proposals/)
4. Mark as "revised" in frontmatter
5. Include in next quarterly review

---

## Questions?

See [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) for complete intake process.
