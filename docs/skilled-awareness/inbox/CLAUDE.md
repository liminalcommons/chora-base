---
sap_id: SAP-001
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-150"   # Quick Start + Core Workflows
  phase_2: "lines 151-280" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9500
---

# Inbox Protocol (SAP-001) - Claude-Specific Awareness

**SAP ID**: SAP-001
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using the inbox coordination system.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic inbox patterns
2. Use this file for Claude Code tool integration (Read for status, Edit for updates, Bash for events)
3. Always check `inbox/coordination/ECOSYSTEM_STATUS.yaml` for current state

### Three-Tier Intake System

| Type | Directory | Review Frequency | File Pattern |
|------|-----------|------------------|--------------|
| **Type 1: Proposals** | `inbox/incoming/proposals/` | Strategic sessions | `proposal-NNN.md` |
| **Type 2: Coordination** | `inbox/incoming/coordination/` | Sprint planning (bi-weekly) | `COORD-YYYY-NNN.json` |
| **Type 3: Tasks** | `inbox/active/` | Daily | `task-NNN/` |

---

## Claude Code Inbox Workflows

### Workflow 1: Showing Inbox Status with Read

```markdown
User: "show inbox"

Claude (Phase 1: Read Status - 0-5k tokens):
1. Read ecosystem status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

2. Parse key sections:
   - coordination.active_requests: Pending coordination requests
   - active_work: Current sprint tasks
   - blockers: Cross-repo dependencies

Claude (response to user):
"✅ Inbox Status:

   **Active Coordination Requests**: 3
   - COORD-2025-001: SAP validation framework (priority: high)
   - COORD-2025-002: Gateway timeout fix (priority: medium)
   - COORD-2025-003: Documentation update (priority: low)

   **Active Work**: 5 tasks in progress
   - task-042: Implement metrics tracking
   - task-043: Update awareness files

   **Blockers**: 1
   - Gateway dependency blocking backend refactor

   **Recent Completions**: 2 (last 30 days)"

Result: Inbox status displayed from ECOSYSTEM_STATUS.yaml
```

---

### Workflow 2: Creating Coordination Request with Write and Bash

```markdown
User: "Create coordination request for backend timeout fix"

Claude (Phase 1: Create JSON - 0-10k tokens):
1. Generate coordination request ID:
   Bash: ls inbox/incoming/coordination/ | grep "COORD-2025" | tail -1
   # Last ID: COORD-2025-003 → Next: COORD-2025-004

2. Write coordination request JSON:
   Write inbox/incoming/coordination/COORD-2025-004.json
   {
     "type": "coordination",
     "request_id": "CORD-2025-004",
     "title": "Backend timeout fix",
     "created": "2025-11-04",
     "description": "Gateway returns 504 timeout after 30s, need to increase to 60s",
     "priority": "high",
     "requesting_repo": "chora-base",
     "target_repos": ["backend-gateway"],
     "relationships": {
       "blocks": [],
       "blocked_by": [],
       "related_to": ["COORD-2025-002"]
     },
     "affects_saps": ["SAP-015"],
     "affects_domains": ["gateway"]
   }

Claude (Phase 2: Update Ecosystem Status - 10-20k tokens):
3. Read current status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

4. Edit to add request:
   Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
   # Add COORD-2025-004 to coordination.active_requests

Claude (Phase 3: Log Event - 20-25k tokens):
5. Append event to log:
   Bash: echo '{"timestamp":"2025-11-04T10:30:00Z","event_type":"coordination_request_created","request_id":"COORD-2025-004","priority":"high"}' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Created coordination request:
   - ID: COORD-2025-004
   - Title: Backend timeout fix
   - Priority: high
   - Status: pending_triage (will be reviewed in next sprint planning)

   Files created:
   - inbox/incoming/coordination/COORD-2025-004.json
   - Updated: inbox/coordination/ECOSYSTEM_STATUS.yaml
   - Logged: inbox/coordination/events.jsonl"

Result: Coordination request created and tracked
```

---

### Workflow 3: Triaging Coordination Request with Edit

```markdown
User: "Accept COORD-2025-004"

Claude (Phase 1: Read Request - 0-5k tokens):
1. Read coordination request:
   Read inbox/incoming/coordination/COORD-2025-004.json

Claude (Phase 2: Add Decision - 5-15k tokens):
2. Edit JSON to add decision:
   Edit inbox/incoming/coordination/COORD-2025-004.json
   # Add decision field:
   "decision": {
     "status": "accepted",
     "decided_by": "claude-sonnet-4",
     "decided_at": "2025-11-04T10:35:00Z",
     "rationale": "High priority, affects gateway stability"
   }

Claude (Phase 3: Update Status - 15-25k tokens):
3. Read ecosystem status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

4. Edit to reflect decision:
   Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
   # Update COORD-2025-004 status in active_requests

Claude (Phase 4: Log Event - 25-30k tokens):
5. Log acceptance event:
   Bash: echo '{"timestamp":"2025-11-04T10:35:00Z","event_type":"coordination_request_accepted","request_id":"COORD-2025-004"}' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Accepted COORD-2025-004:
   - Decision: accepted
   - Rationale: High priority, affects gateway stability
   - Next: Will be assigned to sprint

   Updated:
   - inbox/incoming/coordination/COORD-2025-004.json
   - inbox/coordination/ECOSYSTEM_STATUS.yaml"

Result: Coordination request triaged and accepted
```

---

## Claude-Specific Tips

### Tip 1: Use Read for ECOSYSTEM_STATUS.yaml First

**Pattern**:
```markdown
# ALWAYS read status before operations
Read inbox/coordination/ECOSYSTEM_STATUS.yaml

# Then perform operation
# (Create, update, triage)
```

**Why**: ECOSYSTEM_STATUS.yaml is central dashboard, must understand current state

---

### Tip 2: Use Bash for Event Logging, Not Edit

**Pattern**:
```markdown
# ✅ GOOD: Append with Bash
Bash: echo '{"event_type":"..."}' >> inbox/coordination/events.jsonl

# ❌ BAD: Read entire log, Edit to append
Read inbox/coordination/events.jsonl  # Loads entire log
Edit inbox/coordination/events.jsonl  # Inefficient
```

**Why**: Event log grows large, Bash append is efficient

---

### Tip 3: Generate IDs from Directory Listing

**Pattern**:
```markdown
# Find last coordination request ID:
Bash: ls inbox/incoming/coordination/ | grep "COORD-2025" | sort | tail -1

# Extract number, increment:
# COORD-2025-003 → COORD-2025-004
```

**Why**: Ensures unique IDs, avoids conflicts

---

### Tip 4: Use Edit for Small JSON Updates

**Pattern**:
```markdown
# Read JSON first:
Read inbox/incoming/coordination/COORD-2025-004.json

# Edit specific field:
Edit inbox/incoming/coordination/COORD-2025-004.json
# old_string: "status": "pending_triage"
# new_string: "status": "accepted"
```

**Why**: Edit preserves JSON structure, safer than rewriting

---

### Tip 5: Validate JSON with jq After Edits

**Pattern**:
```markdown
# After editing JSON:
Bash: jq . inbox/incoming/coordination/COORD-2025-004.json > /dev/null

# Check exit code:
# 0 = valid JSON ✅
# Non-zero = invalid JSON ❌
```

**Why**: Catches JSON syntax errors immediately

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Reading ECOSYSTEM_STATUS.yaml Before Operations

**Problem**: Create coordination request without checking current status

**Fix**: ALWAYS read status first

```markdown
# ❌ BAD: Create request blindly
Write inbox/incoming/coordination/COORD-2025-004.json

# ✅ GOOD: Read status first
Read inbox/coordination/ECOSYSTEM_STATUS.yaml
# Check: What's the last ID? Any blockers?
# Then: Create request
```

**Why**: Avoids duplicate IDs, understands current priorities

---

### Pitfall 2: Using Edit for Event Log Appends

**Problem**: Read entire events.jsonl, Edit to append

**Fix**: Use Bash echo append

```markdown
# ❌ BAD: Edit event log
Read inbox/coordination/events.jsonl  # 1000+ events
Edit inbox/coordination/events.jsonl  # Inefficient

# ✅ GOOD: Bash append
Bash: echo '{"event_type":"..."}' >> inbox/coordination/events.jsonl
```

**Why**: Event logs grow large, Edit loads entire file

---

### Pitfall 3: Not Validating JSON After Edits

**Problem**: Edit JSON file, don't validate, breaks parsing

**Fix**: ALWAYS validate with jq

```markdown
# After editing:
Bash: jq . inbox/incoming/coordination/COORD-2025-004.json

# If error, fix syntax
```

**Why**: Invalid JSON breaks coordination system

---

### Pitfall 4: Forgetting to Update ECOSYSTEM_STATUS.yaml

**Problem**: Create coordination request but don't update status dashboard

**Fix**: ALWAYS update both

```markdown
# Create request:
Write inbox/incoming/coordination/COORD-2025-004.json

# Update status dashboard:
Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
# Add to coordination.active_requests
```

**Why**: ECOSYSTEM_STATUS.yaml is single source of truth for status

---

### Pitfall 5: Not Logging Events

**Problem**: Complete operation but don't log event

**Fix**: ALWAYS log events

```markdown
# After operation:
Bash: echo '{"timestamp":"...", "event_type":"coordination_request_created"}' >> inbox/coordination/events.jsonl
```

**Why**: Events enable traceability, required for audit trail

---

## Support & Resources

**SAP-001 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic inbox patterns
- [Capability Charter](capability-charter.md) - Three-tier intake system
- [Protocol Spec](protocol-spec.md) - Coordination request schema
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Inbox adoption tracking

**Schemas**:
- `inbox/schemas/coordination-request.schema.json` - Type 2 schema
- `inbox/schemas/strategic-proposal.schema.json` - Type 1 schema
- `inbox/schemas/implementation-task.schema.json` - Type 3 schema

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - SAP governance
- [SAP-009 (agent-awareness)](../agent-awareness/) - AGENTS.md pattern
- [SAP-010 (memory-system)](../memory-system/) - Event logging
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - DDD→BDD→TDD

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-001
  - 3 workflows: Show Status with Read, Create Request with Write/Bash, Triage with Edit
  - Tool patterns: Read for status, Write for requests, Edit for updates, Bash for events
  - 5 Claude-specific tips, 5 common pitfalls
  - JSON validation patterns

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic inbox patterns
2. Review [protocol-spec.md](protocol-spec.md) for schemas
3. Check [capability-charter.md](capability-charter.md) for three-tier intake system
4. Read status: `Read inbox/coordination/ECOSYSTEM_STATUS.yaml`
