---
sap_id: SAP-001
version: 1.1.0
status: active
last_updated: 2025-10-31
type: quick_reference
audience: all_agents
complexity: intermediate
estimated_reading_time: 13
progressive_loading:
  phase_1: "lines 1-100"
  phase_2: "lines 101-200"
  phase_3: "full"
phase_1_token_estimate: 3000
phase_2_token_estimate: 6000
phase_3_token_estimate: 6000
tags:
  - inbox
  - coordination
  - cross-repo
  - production
---

# AGENTS.md - Inbox Protocol (SAP-001)

**Domain**: Inbox Coordination
**SAP**: SAP-001 (inbox-protocol)
**Version**: 1.1.0
**Last Updated**: 2025-10-31

---

## Overview

This is the domain-specific AGENTS.md file for the inbox protocol (SAP-001). It provides context for agents working with the inbox coordination system, including Type 1/2/3 intake, coordination requests, and ecosystem status management.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides inbox-specific context

---

## User Signal Patterns

### Inbox Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "show inbox" | run_inbox_status | Read ECOSYSTEM_STATUS.yaml | Display dashboard |
| "what's pending" | list_pending_coordination_requests | Filter by status: pending_triage | Count by priority |
| "what's in the inbox" | run_inbox_status | Same as "show inbox" | Natural variation |
| "inbox status" | run_inbox_status | Dashboard view | Formal term |
| "check inbox" | run_inbox_status | Verification pattern | Common variation |
| "review coord-NNN" | open_coordination_request(id) | Read incoming/coordination/COORD-NNN.json | Load specific request |
| "open coord-005" | open_coordination_request("coord-005") | Navigate to specific file | With parameter |
| "create coordination request" | create_coordination_request() | Use coordination-request.schema.json | Type 2 intake |
| "new coordination request" | create_coordination_request() | Variation | |
| "triage inbox" | run_sprint_planning_triage | Process pending_triage items | Bi-weekly |
| "what's blocking" | list_blockers | Filter ECOSYSTEM_STATUS.yaml by blockers field | Cross-repo dependencies |
| "show blockers" | list_blockers | Same intent | |
| "archive coord-NNN" | archive_completed_request(id) | Move incoming/ → archived/ | After fulfillment complete |

### Coordination Request Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "accept coord-NNN" | accept_coordination_request(id) | Update decision field to "accepted" | Sprint planning decision |
| "reject coord-NNN" | reject_coordination_request(id) | Update decision field to "rejected" | With rationale |
| "defer coord-NNN" | defer_coordination_request(id) | Update decision field to "backlog" | Postpone |
| "complete coord-NNN" | complete_coordination_request(id) | Move to recent_completions | Mark fulfilled |

### Ecosystem Status Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "ecosystem status" | show_ecosystem_status | Read ECOSYSTEM_STATUS.yaml | Full dashboard |
| "what repos are active" | list_active_repos | From ecosystem.repositories | Filter by status: active |
| "show recent completions" | list_recent_completions | From coordination.recent_completions | Last 30 days |

### Common Variations

**Inbox Status Queries**:
- "show inbox" / "check inbox" / "what's in the queue" → run_inbox_status
- "pending items" / "what needs review" / "coordination queue" → list_pending_coordination_requests

**Blocker Queries**:
- "block" / "blocker" / "what's blocked" / "show blockers" → list_blockers

**Coordination Request Management**:
- "review coord-NNN" / "open coord-NNN" / "show coord-NNN" → open_coordination_request(id)
- "accept coord-NNN" / "approve coord-NNN" → accept_coordination_request(id)

---

## Inbox Protocol Quick Reference

### Three-Tier Intake System

**Type 1: Strategic Proposals** (`inbox/incoming/proposals/`)
- Major changes requiring ecosystem-wide coordination
- Reviewed in strategic planning sessions
- File pattern: `proposal-NNN.md`

**Type 2: Coordination Requests** (`inbox/incoming/coordination/`)
- Cross-repo dependencies or blocking work
- Reviewed in sprint planning (every 2 weeks)
- File pattern: `COORD-YYYY-NNN.json`

**Type 3: Implementation Tasks** (`inbox/active/`)
- Implementation work within single repo
- Directly assigned to sprints
- File pattern: `task-NNN/` directories

### Key Files

**Status Dashboard**: `inbox/coordination/ECOSYSTEM_STATUS.yaml`
- Active work tracking
- Blocker management
- Recent completions

**Event Log**: `inbox/coordination/events.jsonl`
- Event traceability
- CHORA_TRACE_ID correlation
- Append-only log

**Schemas**: `inbox/schemas/`
- `coordination-request.schema.json` (Type 2)
- `strategic-proposal.schema.json` (Type 1)
- `implementation-task.schema.json` (Type 3)

### Common Tasks

**Create Coordination Request**:
```bash
# 1. Create JSON file following schema
cat > inbox/incoming/coordination/COORD-2025-NNN.json << 'EOF'
{
  "type": "coordination",
  "request_id": "COORD-2025-NNN",
  "title": "Brief title",
  "created": "YYYY-MM-DD",
  "description": "Detailed description",
  "priority": "high",
  "requesting_repo": "chora-base",
  "target_repos": ["other-repo"],

  # NEW: Relationship metadata (optional, for graph-based curation)
  "relationships": {
    "blocks": ["COORD-2025-001"],           # This request blocks others
    "blocked_by": ["COORD-2025-002"],       # Blocked by other requests
    "related_to": ["COORD-2025-003"],       # Related work
    "spawns_tasks": ["task-123"]            # Spawned implementation tasks
  },

  # NEW: SAP correlation (optional, track which SAPs are affected)
  "affects_saps": ["SAP-001", "SAP-015"],

  # NEW: Domain impact (optional, track domain scope)
  "affects_domains": ["skilled-awareness", "dev-docs"]
}
EOF

# 2. Emit event
echo '{"event_type": "coordination_request_created", ...}' >> inbox/coordination/events.jsonl

# 3. Update ECOSYSTEM_STATUS.yaml
# Add to coordination.active_requests
```

**Note**: The `relationships`, `affects_saps`, and `affects_domains` fields are **optional** but enable graph-based curation and cross-SAP analysis. See [protocol-spec.md Section 7](protocol-spec.md#7-coordination-request-schema-enhancements) for details.

**Triage Coordination Request**:
```bash
# 1. Review request in sprint planning
# 2. Add decision field to JSON
# 3. Update ECOSYSTEM_STATUS.yaml
# 4. Emit coordination_request_accepted event
```

**Complete Coordination Request**:
```bash
# 1. Add fulfillment field to JSON
# 2. Move from active_work to recent_completions in ECOSYSTEM_STATUS.yaml
# 3. Emit coordination_request_completed event
# 4. Archive if needed: mv inbox/incoming/coordination/COORD-NNN.json inbox/archived/
```

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "show inbox" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "show inbox" → `run_inbox_status` with high confidence
5. Agent reads `inbox/coordination/ECOSYSTEM_STATUS.yaml`
6. Agent formats output according to user verbosity preference

**Progressive Formalization**:
- Week 1: "show me the inbox" → Agent translates
- Week 2-4: "what are coordination requests?" → Agent teaches term
- Month 2+: "run_inbox_status" → Agent executes directly
- Month 3+: User provides JSON → Agent validates schema

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Related SAPs

- **SAP-000** (sap-framework): Defines SAP structure and governance
- **SAP-001** (inbox-protocol): THIS SAP - Coordination system
- **SAP-009** (agent-awareness): AGENTS.md pattern and bidirectional translation
- **SAP-012** (development-lifecycle): DDD→BDD→TDD workflows referenced in coordination

---

**Version History**:
- **1.1.0** (2025-10-31): Added User Signal Patterns section for bidirectional translation layer integration
- **1.0.0** (2025-10-31): Initial domain AGENTS.md for inbox protocol
