# Coordination Requests for chora-base

This directory contains coordination requests submitted to chora-base for cross-repository collaboration.

## Active Coordination Requests

### COORD-2025-003: v1.9.0 Capabilities Update
**Status:** Pending
**Priority:** Medium
**Created:** 2025-10-30
**Target Repo:** chora-base

**Summary:**
Update chora-base documentation to reference chora-compose v1.9.0 capabilities (stigmergic context links and freshness tracking) for efficient SAP regeneration and maintenance workflows.

**Files:**
- [COORD-2025-003-v190-capabilities-update.json](./COORD-2025-003-v190-capabilities-update.json) - Formal coordination request (JSON schema)
- [COORD-2025-003-communication-brief.md](./COORD-2025-003-communication-brief.md) - Comprehensive communication document (9,000+ words)

**What's Included:**
1. **Executive Summary** - TL;DR of v1.9.0 capabilities
2. **Feature Deep-Dives**:
   - Stigmergic context links (95% token reduction)
   - Freshness tracking (automated staleness detection)
   - Collections documentation (complete reference)
3. **Integration Guide for chora-base**:
   - Scenario 1: Regenerate SAP documentation
   - Scenario 2: Weekly SAP freshness checks
   - Scenario 3: Health monitoring dashboard
4. **Integration Checklist** (3 phases, 2-7 hours total)
5. **Technical Reference** (API specs, schemas, examples)

**Action Required:**
- Review coordination request and communication brief
- Approve/reject based on chora-base priorities
- If approved: Assign to sprint, follow integration checklist (Phase 1: 2-4 hours)

**Expected Impact:**
- 95% token reduction for SAP regeneration workflows (20k→1k tokens)
- Automated staleness detection for proactive SAP maintenance
- Foundation for ecosystem-wide cross-repo coordination

---

## How to Submit Coordination Requests

### 1. Create JSON Request

Use the schema: [../schemas/coordination-request.schema.json](../schemas/coordination-request.schema.json)

**Required Fields:**
```json
{
  "trace_id": "CHORA-COORD-YYYY-XXX",
  "type": "coordination",
  "priority": "low|medium|high|urgent",
  "source_repo": "chora-compose",
  "target_repo": "target-repo-name",
  "title": "Brief description (10-200 chars)",
  "description": "Detailed description",
  "requested_capabilities": ["capability1", "capability2"]
}
```

**Optional but Recommended:**
- `category`: mcp_integration, generator_collaboration, config_schema_sharing, documentation_sync
- `expected_outcome`: What success looks like
- `acceptance_criteria`: Specific validation criteria
- `estimated_effort`: Rough effort estimate (e.g., "2-4 hours")
- `context`: Background, related issues/PRs, related proposals

### 2. Create Communication Brief (Optional but Recommended)

For complex coordination requests, create a detailed communication document:
- Executive summary
- Feature explanations
- Integration guides
- Technical reference
- Resources and next steps

**Benefits:**
- Provides comprehensive context
- Reduces back-and-forth clarification
- Serves as implementation guide
- Can be referenced by other repos

### 3. Log Event

Append event to [../coordination/events.jsonl](../coordination/events.jsonl):
```json
{"timestamp":"<ISO 8601>","trace_id":"CHORA-COORD-YYYY-XXX","event_type":"coordination_submitted","source":"chora-compose","target":"target-repo","metadata":{}}
```

### 4. Notify Target Repo (Optional)

- GitHub Issue in target repo
- Tag in GitHub Discussions
- Slack message (if applicable)
- Email to maintainer

---

## Coordination Request Lifecycle

### 1. Submitted
- JSON file created in `inbox/incoming/coordination/`
- Event logged to `coordination/events.jsonl`
- Target repo notified (optional)

### 2. Under Review
- Target repo maintainer reviews request
- Questions/clarifications via GitHub or coordination protocol
- Status updated in JSON: `"status": "under_review"`

### 3. Decision
- **Accepted**: Assigned to sprint, work begins
- **Rejected**: Rationale provided in `response` field
- **Deferred**: Scheduled for future sprint
- **Needs Clarification**: Questions sent back to source repo

### 4. In Progress
- If accepted, work artifacts created in target repo
- Progress tracked via events.jsonl
- Checkpoints logged for complex work

### 5. Completed
- Acceptance criteria validated
- Completion event logged
- Request moved to `../completed/` (optional)
- Summary provided to source repo

---

## Review SLA

**chora-base Review SLA:**
- Coordination requests: Reviewed within 72 hours
- Decision: Accept/reject/defer within 1 week
- Implementation: According to sprint planning (typically 1-2 weeks)

**Priority Handling:**
- **Urgent**: Reviewed within 24 hours, prioritized for current sprint
- **High**: Reviewed within 48 hours, considered for current sprint
- **Medium**: Reviewed within 72 hours, scheduled for next sprint
- **Low**: Reviewed within 1 week, scheduled as capacity allows

---

## Resources

### chora-compose Capabilities
- [../coordination/CAPABILITIES/chora-compose.yaml](../coordination/CAPABILITIES/chora-compose.yaml) - What we provide/consume
- [../../docs/reference/mcp/tool-reference.md](../../docs/reference/mcp/tool-reference.md) - 18 MCP tools
- [../../AGENTS.md](../../AGENTS.md) - Project overview and capabilities

### Inbox Protocol
- [../INBOX_PROTOCOL.md](../INBOX_PROTOCOL.md) - Quick reference
- [../CLAUDE.md](../CLAUDE.md) - Operational guide for AI agents
- [../../docs/skilled-awareness/inbox/protocol-spec.md](../../docs/skilled-awareness/inbox/protocol-spec.md) - Full protocol spec

### Schemas
- [../schemas/coordination-request.schema.json](../schemas/coordination-request.schema.json) - Coordination request schema
- [../schemas/implementation-task.schema.json](../schemas/implementation-task.schema.json) - Task schema
- [../schemas/strategic-proposal.schema.json](../schemas/strategic-proposal.schema.json) - Proposal schema

---

## Contact

**Questions or Issues:**
- GitHub Issues: https://github.com/liminalcommons/chora-compose/issues
- GitHub Discussions: https://github.com/liminalcommons/chora-compose/discussions
- Maintainer: Victor (@victorpiper)

**For Urgent Matters:**
- Tag @victorpiper in GitHub issue
- Use priority: "urgent" in coordination request
- Follow up via direct communication channel
