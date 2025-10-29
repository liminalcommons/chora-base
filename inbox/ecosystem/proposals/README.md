# Strategic Proposals

**Intake Type:** Type 1 - Strategic Communication
**Review Frequency:** Quarterly
**Decision Makers:** Leadership + Team
**Phase:** Phase 1 (Vision & Strategy)

---

## Purpose

This directory contains **strategic proposals** that could influence the ecosystem's vision, roadmap, or architectural direction across multiple repositories.

## When to Use

Create a proposal here when:
- 🌍 Proposing ecosystem-wide changes (affects 2+ repos)
- 📊 Suggesting new capability waves or waypoints
- 🏗️ Recommending architectural patterns
- 🔄 Proposing integration with external ecosystems
- 📈 Suggesting strategic direction changes

**Do NOT use for:**
- ❌ Sprint-level feature requests (use `inbox/incoming/coordination/`)
- ❌ Bug fixes or small improvements (use `inbox/incoming/tasks/`)
- ❌ Implementation details (handled in Phase 3: DDD)

---

## Proposal Format

Each proposal should be a markdown file with this structure:

```markdown
---
title: Proposal Title
type: strategic-proposal
created: YYYY-MM-DD
author: Your Name
status: proposed | under-review | accepted | deferred | rejected
impact: [list of affected repos]
---

# Proposal: [Title]

## Executive Summary
1-2 paragraphs explaining what you're proposing and why.

## Problem Statement
What problem does this solve? What pain point does it address?

## Proposed Solution
Detailed explanation of what you propose to implement.

## Ecosystem Impact
Which repos are affected? What changes are needed?

## Timeline Estimate
When could this realistically be delivered?

## Alternatives Considered
What other approaches did you consider? Why is this the best option?

## Success Metrics
How will we measure if this succeeded?

## Open Questions
What needs to be answered before proceeding?
```

---

## Review Process

1. **Quarterly Review Meeting**
   - All proposals reviewed by leadership + team
   - Discussion of strategic fit, capacity, ROI
   - Decision: Accept, Defer, Reject, or Request Research

2. **If Accepted:**
   - Move to [`inbox/ecosystem/rfcs/`](../rfcs/) for detailed design
   - Update [ROADMAP.md](../../../ROADMAP.md)
   - Create multi-repo coordination plan
   - Generate coordination requests → `inbox/incoming/coordination/`

3. **If Deferred:**
   - Move to [`inbox/ecosystem/deferred/`](../deferred/)
   - Document why (timing, capacity, priority)
   - Set review date for future quarter

4. **If Rejected:**
   - Move to [`inbox/ecosystem/deferred/`](../deferred/)
   - Document rationale
   - Preserve for historical reference

---

## Example Proposals

See existing proposals:
- [Multi-repo capability evolution to W3](../multi-repo-capability-evolution-to-w3.md) (accepted)
- [MCP ecosystem setup architecture](../ARCHITECTURE_CLARIFICATION.md) (accepted)

---

## Questions?

See [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) for complete intake process documentation.
