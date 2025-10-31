# Cross-Repository Inbox Awareness Guide

**Audience:** Claude Code, Codex, and human operators responsible for inbox triage and execution
**Version:** 1.0.1
**Last Updated:** 2025-10-28
**Prerequisites:**
- Load [protocol-spec.md](protocol-spec.md) (understand lifecycle and artefacts).
- Review `inbox/` directory structure in the target repository.
- Ensure shell access with basic commands (`ls`, `cat`, `mv`, `mkdir`, `jq`, `yq` if available).

---

## 1. Quick Orientation

### When to Use This SAP

**Use the Inbox Coordination SAP when**:
- Coordinating work across multiple repositories in the ecosystem
- Processing strategic proposals, coordination requests, or implementation tasks
- Tracking cross-repo dependencies and state transitions
- Establishing Git-native coordination without external tools (no SaaS dependency)
- Triaging incoming work items with clear lifecycle management

**Don't use for**:
- Single-repository task management (use `project-docs/sprints/` instead)
- Real-time chat coordination (inbox is async, file-based)
- External SaaS integrations (inbox is Git-native only)
- Ad-hoc notes or scratch work (inbox requires structured intake schemas)

### Capability Summary
The inbox coordinates strategic proposals, cross-repo dependencies, and approved tasks by keeping state in Git. Operators move items through intake → review → activation → completion while logging events.
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

## 5. Common Pitfalls

### Pitfall 1: Moving Tasks Without Emitting Events
**Scenario**: Agent moves task from `incoming/` to `active/` but forgets to emit event to `coordination/events.jsonl`

**Example**:
```bash
# Wrong: Just moving file
mv inbox/incoming/tasks/task-123.json inbox/active/task-123-feature/

# Missing: Event emission
```

**Fix**: Always emit event after state transitions:
```bash
# Move task
mv inbox/incoming/tasks/task-123.json inbox/active/task-123-feature/

# Emit event
echo '{"timestamp":"2025-10-28T10:00:00Z","event":"task_started","trace_id":"task-123","repo":"chora-base"}' >> inbox/coordination/events.jsonl
```

**Why it matters**: Event log provides audit trail; missing events break traceability and status tracking

### Pitfall 2: Schema Validation Skipped
**Scenario**: Agent accepts coordination request without validating JSON schema

**Example**:
```json
{
  "type": "coordination_request",
  "from_repo": "chora-compose"
  // Missing required fields: priority, description, trace_id
}
```

**Fix**: Always validate schema before activation:
```bash
# Validate with jq
cat inbox/incoming/coordination/coord-456.json | jq empty
# If valid, proceed; if error, notify user

# Better: validate against schema
cat inbox/incoming/coordination/coord-456.json | jq -e 'has("trace_id") and has("priority") and has("description")'
```

**Why it matters**: Invalid requests cause downstream confusion; schema ensures complete information

### Pitfall 3: Capability Mismatch Not Checked
**Scenario**: Agent activates task that repo cannot handle (capability not listed in `CAPABILITIES/<repo>.yaml`)

**Example**:
```yaml
# In coordination/CAPABILITIES/chora-base.yaml
provides:
  - python-packaging
  - documentation

# Request asks for: rust-compilation (not provided!)
```

**Fix**: Always check capability match before activation:
```bash
# Check if repo provides capability
yq '.provides[] | select(. == "rust-compilation")' inbox/coordination/CAPABILITIES/chora-base.yaml
# If no match, recommend routing to different repo
```

**Why it matters**: Activating mismatched tasks leads to failed execution and wasted effort

### Pitfall 4: Mixing Strategic and Implementation Workflows
**Scenario**: Agent tries to execute strategic proposal as if it's an implementation task

**Example**:
```
Agent: "I'll start coding the architecture proposal from ecosystem/proposals/"
Problem: Strategic proposals need review/approval before becoming tasks
```

**Fix**: Follow correct workflow for each intake type:
```
Strategic proposal (ecosystem/proposals/) → Quarterly review → If approved, create coordination request
Coordination request (incoming/coordination/) → Sprint review → If approved, create implementation task
Implementation task (incoming/tasks/) → Activation → DDD → BDD → TDD → Completion
```

**Why it matters**: Skipping review stages leads to misaligned work; proposals need governance approval first

### Pitfall 5: Completing Task Without Summary
**Scenario**: Agent moves task to `completed/` but doesn't create completion summary

**Example**:
```bash
# Wrong: Just moving directory
mv inbox/active/task-123-feature/ inbox/completed/
# Missing: SUMMARY.md with outcomes, verification notes
```

**Fix**: Always create completion summary:
```bash
# Create summary first
cat > inbox/active/task-123-feature/SUMMARY.md <<EOF
# Task Completion Summary

**Task ID**: task-123
**Completed**: 2025-10-28
**Outcome**: Feature implemented and tested
**Verification**: All tests pass, coverage 87%
**Follow-up**: None
EOF

# Then move to completed
mv inbox/active/task-123-feature/ inbox/completed/
```

**Why it matters**: Summaries provide retrospective value; without them, completed work is undocumented

---

## 6. Troubleshooting
- **Issue:** Schema validation failure.
  - **Action:** Run `jq`/`yq` to inspect structure; compare against schema; flag missing fields.
- **Issue:** Capability mismatch.
  - **Action:** Suggest updating capability file or rerouting to correct repo via coordination request.
- **Issue:** Event log conflicts.
  - **Action:** Ensure append-only entries; if merge conflict, resolve by chronological order.
- **Issue:** Task stalled.
  - **Action:** Emit `checkpoint` with blockers; alert maintainer for escalation.

---

## 7. Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-001 --source /path/to/chora-base
```

This will automatically install:
- SAP-001 (Inbox Coordination Protocol)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `minimal-entry` - 5 essential SAPs for quick ecosystem onboarding
- `recommended` - 10 SAPs covering core development workflows
- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Dependencies

This SAP has no dependencies.

### Important Notice

**Pilot Status**: SAP-001 is currently in Pilot status and may undergo changes. Use with awareness that protocols and structures may evolve based on feedback from early adopters.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/inbox/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

# Verify inbox directory structure
ls inbox/
# Should show: coordination/, incoming/, outgoing/, schemas/
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## 8. Related Content

### Within This SAP (skilled-awareness/inbox/)
- [capability-charter.md](capability-charter.md) - Business case for cross-repo inbox coordination
- [protocol-spec.md](protocol-spec.md) - Complete technical specification for inbox lifecycle
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step installation guide for new repositories
- [ledger.md](ledger.md) - Adoption tracking and feedback log
- [dry-run-checklist.md](dry-run-checklist.md) - Validation checklist for pilot adoption
- [broadcast-workflow.md](broadcast-workflow.md) - Weekly ecosystem status broadcast process

### Developer Process (dev-docs/)
**Workflows**:
- [/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD → BDD → TDD lifecycle (referenced in task execution)

**Integration**:
- Inbox tasks follow DDD → BDD → TDD phases after activation
- `change-request.md` created during DDD phase for each active task

### Project Lifecycle (project-docs/)
**Planning**:
- `/docs/project-docs/sprints/` - Sprint planning (coordination requests reviewed at sprint cadence)
- `/docs/project-docs/releases/` - Release coordination (strategic proposals inform roadmap)

**Audits**:
- `/docs/project-docs/audits/wave-2-sap-001-audit.md` - This SAP's audit report (to be created)

**Coordination** (future):
- Ecosystem-wide status dashboards (planned integration with inbox broadcasts)

### User Guides (user-docs/)
**Existing**:
- [/docs/user-docs/explanation/architecture-clarification.md](/docs/user-docs/explanation/architecture-clarification.md) - Architecture overview
- [/docs/user-docs/explanation/benefits-of-chora-base.md](/docs/user-docs/explanation/benefits-of-chora-base.md) - Benefits including coordination patterns

**Planned** (to be created in Wave 2 Phase 5):
- How-To: Triage an inbox coordination request
- How-To: Write a strategic proposal for ecosystem review
- Tutorial: End-to-end cross-repo coordination workflow
- Reference: Inbox JSON schemas and event types

### Other SAPs (skilled-awareness/)
**Framework**:
- [/docs/skilled-awareness/sap-framework/](/docs/skilled-awareness/sap-framework/) - SAP-000, defines SAP structure (inbox follows SAP framework)
- [/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

**Related Capabilities**:
- [/docs/skilled-awareness/development-lifecycle/](/docs/skilled-awareness/development-lifecycle/) - SAP-012, DDD → BDD → TDD workflow (inbox tasks use this)
- [/docs/skilled-awareness/memory-system/](/docs/skilled-awareness/memory-system/) - SAP-010, event logging patterns (inbox event log compatible)
- [/docs/skilled-awareness/chora-base/](/docs/skilled-awareness/chora-base/) - SAP-002, meta-SAP references inbox as coordination capability

**Governance** (external repos):
- `chora-meta` repository - Ecosystem governance (strategic proposals escalate here)
- `chora-governance` repository - Coordination standards and patterns

---

## 8. Continuous Learning Hooks
- **Feedback Capture:** Add notes to task completion summary or update [ledger.md](ledger.md) feedback section
- **Staying Updated:** Watch [inbox/](.) for version bumps; maintainers broadcast via inbox strategic updates or CHANGELOG entries
- **Agent Training:** When guide updates, rerun [dry-run-checklist.md](dry-run-checklist.md) to ensure patterns remain executable

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with cross-repo coordination scenarios, enhanced "Related Content" with 4-domain coverage
- **1.0.0** (2025-10-27): Initial awareness guide for cross-repository inbox coordination
