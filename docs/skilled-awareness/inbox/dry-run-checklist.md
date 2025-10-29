# Inbox SAP Dry Run Checklist

Use this script to validate the awareness guide with Claude or Codex. Record actual outcomes in `ledger.md` under the feedback section.

---

## Preparation
- [ ] Load `docs/reference/skilled-awareness/inbox/awareness-guide.md`.
- [ ] Open a shell within the target repository (pilot repo).
- [ ] Ensure `inbox/` directory is present with required structure.
- [ ] Set `CHORA_TRACE_ID` environment variable (or plan to read from task file).
- [ ] Have sample payloads ready: `coordination-request.json`, `implementation-task.json`.

## Scripted Walkthrough
1. **Orientation:** Ask the agent to summarize the inbox capability and key directories.
2. **Coordination Triage Simulation:**
   - Provide sample coordination request.
   - Expect agent to list pending items, summarize, consult capabilities, provide recommendation, and log event.
3. **Task Activation Simulation:**
   - Provide sample implementation task while in `incoming/tasks/`.
   - Expect move to `active/`, trace ID handling, event emission, initiation of DDD checklist.
4. **Completion Simulation:**
   - Prompt agent to conclude the task, move artefacts to `completed/`, log event, and produce summary.
5. **Escalation Scenario:**
   - Introduce capability mismatch; expect agent to recommend rerouting or updating capability file.
6. **Feedback Capture:**
   - Ask agent to note friction points and propose improvements.

## Acceptance Criteria
- Agent follows patterns from awareness guide without additional prompting.
- Event log entries are syntactically valid JSON.
- Directory moves and summaries align with protocol spec.
- Any confusion or missing guidance captured for updates.

## Dry Run Result (2025-10-27)
- **Status:** Completed (Codex assistant acting as Claude surrogate).
- **Highlights:** Coordination request `coord-101` triaged, task `task-301` activated, change request drafted, broadcast template scaffolded, events logged.
- **Observations:** Needed to create `inbox/coordination/events.jsonl`; recommend adding explicit step in adoption blueprint. Escalation scenario confirmed capability file guidance was sufficient.
- **Follow-Up:** Share findings in ledger feedback; validate template with Victor before reuse.

Update this document with real findings after the first run.
