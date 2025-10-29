# Cross-Repository Inbox Awareness Guide

**Audience:** Claude Code, Codex, and human operators responsible for inbox triage and execution  
**Last Updated:** 2025-10-27  
**Prerequisites:**  
- Load `docs/reference/skilled-awareness/inbox/protocol-spec.md` (understand lifecycle and artefacts).  
- Review `inbox/` directory structure in the target repository.  
- Ensure shell access with basic commands (`ls`, `cat`, `mv`, `mkdir`, `jq`, `yq` if available).

---

## 1. Quick Orientation
- **Capability Summary:** The inbox coordinates strategic proposals, cross-repo dependencies, and approved tasks by keeping state in Git. Operators move items through intake → review → activation → completion while logging events.
- **When to Use:** Whenever the user requests to check or act on `inbox/`, triage cross-repo requests, or start work on active tasks.  
- **Key Paths:**  
  - `inbox/ecosystem/` — Strategic proposals, RFCs, ADRs.  
  - `inbox/incoming/coordination/` — Pending coordination requests (JSON).  
  - `inbox/incoming/tasks/` — Approved implementation tasks waiting activation.  
  - `inbox/active/` — Work in progress directories (each with task metadata).  
  - `inbox/coordination/` — Event logs, capability descriptors, ecosystem status.  
  - `inbox/completed/` — Archived tasks with summaries.

---

## 2. Operating Patterns

### Pattern A: Process Coordination Requests
1. **Recognize:** User prompts like "Review coordination requests" or `coord-XXX` references.  
2. **Act:**  
   - List pending items: `ls inbox/incoming/coordination/*.json`.  
   - For each item, read and summarize with context from `CAPABILITIES/<repo>.yaml`.  
   - Determine triage recommendation (This Sprint / Next Sprint / Reject).  
   - If accepted, create directory under `inbox/active/` and move JSON file.  
   - Ensure `coordination/events.jsonl` exists (create empty file if missing) and emit event capturing acceptance.  
3. **Confirm:** Provide structured summary and ask user to confirm next phase (e.g., start DDD).

### Pattern B: Start an Implementation Task
1. **Recognize:** User asks to work on `task-XXX`.  
2. **Act:**  
   - Locate task in `incoming/tasks/` or `active/`.  
   - Move to `active/` if not already, ensuring directory naming `task-XXX-<slug>/`.  
   - Set or read `CHORA_TRACE_ID` from task JSON.  
   - Confirm `coordination/events.jsonl` exists, then emit `task_started` event.  
   - Begin DDD documentation (create `change-request.md` if missing) before coding.  
3. **Confirm:** Summarize context, plan, and next steps; check with user before executing changes.

### Pattern C: Complete a Task
1. **Recognize:** Work finished, results ready.  
2. **Act:**  
   - Run verification tests as per task acceptance criteria.  
   - Update `README.md` or relevant docs if required.  
   - Move task directory to `inbox/completed/`, ensuring summary included.  
   - Emit `task_completed` event with outcomes.  
3. **Confirm:** Deliver completion summary, attach diff highlights, and highlight any follow-up actions.

### Pattern D: Prepare Weekly Broadcast
1. **Recognize:** Scheduled Monday update or user request to publish inbox broadcast.  
2. **Act:**  
   - Review latest ledger entries and ecosystem status YAML.  
   - Open `inbox/coordination/broadcasts/broadcast-template.md` and replace placeholders with current data (adoption counts, blockers, actions, CTAs).  
   - Save filled template as `inbox/coordination/broadcasts/<week>-broadcast.md`.  
   - Append `broadcast_prepared` (and later `broadcast_shared`) events to `coordination/events.jsonl`.  
3. **Confirm:** Share summary with Victor for approval before posting to coordination channel; once shared, note link in ledger feedback.

---

## 3. Decision Support
- **Checklist Before Activating:**  
  - Does capability file confirm we can handle this type?  
  - Are prerequisites met (dependencies resolved, design approved)?  
  - Do we have capacity? If not, recommend deferral.
- **Escalation Rules:**  
  - Strategic proposals requiring governance input → escalate to maintainer.  
  - Unclear capability mapping → request update to `CAPABILITIES/<repo>.yaml`.  
  - Schema validation failure → notify user, do not progress until fixed.
- **Context Management:**  
  - Maintain working notes in `change-request.md` or equivalent.  
  - Use checkpoint summaries after major actions (`inbox/active/.../notes.md` or memory system).

---

## 4. Collaboration Protocols
- **Artifacts to Produce:**  
  - Triage summaries (markdown bullet lists).  
  - DDD/BDD/TDD documents as tasks advance.  
  - Event log entries for state changes.  
  - Completion summaries with verification notes.  
  - Weekly broadcast files referencing the template.
- **Event Logging:**  
  - Append JSON object with timestamp, event type, `trace_id`, `repo`.  
  - Common events: `coordination_request_accepted`, `task_started`, `checkpoint`, `task_completed`.
- **Handoff Notes:**  
  - Record outstanding questions, next steps, and owners in `notes.md` or task summary.  
  - Update Traceability Ledger (if applicable) or notify coordinator via inbox item.

---

## 5. Troubleshooting
- **Issue:** Schema validation failure.  
  - **Action:** Run `jq`/`yq` to inspect structure; compare against schema; flag missing fields.  
- **Issue:** Capability mismatch.  
  - **Action:** Suggest updating capability file or rerouting to correct repo via coordination request.  
- **Issue:** Event log conflicts.  
  - **Action:** Ensure append-only entries; if merge conflict, resolve by chronological order.  
- **Issue:** Task stalled.  
  - **Action:** Emit `checkpoint` with blockers; alert maintainer for escalation.

---

## 6. Continuous Learning Hooks
- **Feedback Capture:** Add notes to task completion summary or update Ledger feedback section.  
- **Staying Updated:** Watch `docs/reference/skilled-awareness/inbox/` for version bumps; maintainers should broadcast via inbox strategic updates or CHANGELOG entries.  
- **Agent Training:** When guide updates, rerun dry run to ensure patterns remain executable.
