---
title: Author inbox SAP weekly broadcast template
type: change-request
task_id: task-301
phase: 3-ddd
created: 2025-10-27
trace_id: sap-inbox-dryrun-20251027
---

# Change Request: Author inbox SAP weekly broadcast template

## Explanation
### Context
The inbox Skilled Awareness Package needs a reusable broadcast template to accompany the weekly ledger summaries ahead of broader ecosystem rollout.

### Problem Statement
Without a consistent format, ecosystem maintainers lack clarity on adoption status, blockers, and next actions reported from the ledger.

### Business Value
Improves cross-repo coordination by providing predictable messaging, reducing time to understand inbox status updates.

### Stakeholders
- Victor Piper (Ecosystem Coordinator)
- chora-compose maintainers (next pilot)
- Claude/Codex agents interpreting broadcasts

### Dependencies
- Coordination request `coord-101`

## How-to Guide
### User Workflow
1. Review latest ledger entries for updates.
2. Populate broadcast template with headline, adoption status, blockers, and upcoming actions.
3. Commit updated `ECOSYSTEM_STATUS.yaml` and broadcast markdown.

### Expected Journey
Claude/Codex agent follows adoption blueprint to gather data, fills in template, and prepares coordination broadcast PR or commit.

### Common Use Cases
- Weekly status update before Monday standup.
- Mid-week hotspot broadcast if blockers emerge.

## Reference Implementation Notes
- Template stored at `inbox/coordination/broadcasts/broadcast-template.md`.
- Broadcast content references ledger rows by repository name.
- Events appended to `inbox/coordination/events.jsonl` with `broadcast_prepared` and `broadcast_shared` event types.

## Open Questions
- Should broadcasts include metrics (tasks completed, hours logged)?
- Do we automate template population from ledger in future iteration?
