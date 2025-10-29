# Weekly Inbox SAP Broadcast

> Replace the `{{ … }}` placeholders with concrete information collected from the ledger, adoption blueprint, and current coordination work. Remove any sections that have no updates for the week.

**Week:** {{ week }}
**Prepared by:** {{ preparer }}
**Trace ID:** {{ trace_id }}
**Date Broadcast:** {{ broadcast_date }}

## Headline
- {{ single_line_summary }}

## Snapshot
- **New Adoptions:** {{ new_adoptions_count }} ({{ new_adoptions_notes }})
- **In Progress:** {{ in_progress_count }} (key repos: {{ in_progress_repos }})
- **Completed Actions:** {{ completed_actions }}

## Adoption Status
| Repository | Protocol Version | Awareness Installed | Blueprint Status | Notes |
|------------|------------------|---------------------|------------------|-------|
{{ adoption_rows }}

## Blockers & Risks
- {{ blocker_1 }}
- {{ blocker_2 }}
- {{ blocker_optional }}

## Upcoming Actions
1. {{ action_1 }} (Owner: {{ owner_1 }}, Due: {{ due_1 }})
2. {{ action_2 }} (Owner: {{ owner_2 }}, Due: {{ due_2 }})
3. {{ action_optional }}

## Feedback Highlights
- {{ feedback_1 }}
- {{ feedback_2 }}

## Calls to Action
- {{ cta_1 }}
- {{ cta_2 }}

## Links & References
- Ledger: docs/reference/skilled-awareness/inbox/ledger.md
- Broadcast workflow: docs/reference/skilled-awareness/inbox/broadcast-workflow.md
- Coordination request: inbox/active/coord-101-broadcast-launch/coordination.json
- Task: inbox/active/task-301-broadcast-template/task.json
- Events log: inbox/coordination/events.jsonl (append `broadcast_prepared` / `broadcast_shared`)
