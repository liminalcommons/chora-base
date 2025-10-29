# Coordination Requests

**Intake Type:** Type 2 - Coordination Request
**Review Frequency:** Every 2 weeks (Sprint Planning)
**Decision Makers:** Product + Engineering Leads
**Phase:** Phase 2 (Planning & Prioritization)

---

## Purpose

This directory contains **cross-repo coordination requests** - work that needs to be scheduled and prioritized in sprint planning because it affects multiple repositories or has dependencies.

## When to Use

Create a coordination request here when:
- 🔗 Work spans multiple repos (e.g., "ecosystem-manifest needs to deliver spec for mcp-orchestration")
- 📦 Work has dependencies on other repos
- 🚧 Work blocks other teams' progress
- ⏱️ Work has specific timing requirements
- 🎯 Work is part of coordinated release (e.g., Waypoint W3)

**Do NOT use for:**
- ❌ Strategic proposals (use `inbox/ecosystem/proposals/`)
- ❌ Single-repo tasks already in sprint (use `inbox/incoming/tasks/`)
- ❌ Completed work (use `inbox/completed/`)

---

## Request Format

Coordination requests are JSON files following this schema:

```json
{
  "type": "coordination",
  "request_id": "coord-001",
  "title": "Deliver health spec v1.1 for mcp-orchestration",
  "created": "2025-10-27",
  "from_repo": "mcp-orchestration",
  "to_repo": "ecosystem-manifest",
  "priority": "P0 | P1 | P2",
  "urgency": "blocks_sprint | next_sprint | backlog",
  "blocks": [
    "mcp-orchestration Sprint 3",
    "Waypoint W3 validation"
  ],
  "requested_by": "Victor",
  "requested_delivery": "Week 11",
  "context": {
    "waypoint": "W3",
    "related_rfc": "0001-health-monitoring.md",
    "background": "mcp-orchestration needs health check spec to implement HealthMonitor class"
  },
  "deliverables": [
    "ecosystem-manifest.yaml v1.1 with health_check schema",
    "QUALITY_STANDARDS.md updated with health endpoint requirements"
  ],
  "acceptance_criteria": [
    "Health check spec defines required fields (status, version, uptime)",
    "Health check spec includes optional fields (dependencies, metrics)",
    "Spec validated against OpenAPI format",
    "Documentation includes examples"
  ],
  "dependencies": [
    "RFC 0001 must be accepted",
    "chora-base MCP template must support health endpoints"
  ],
  "estimated_effort": "4-8 hours",
  "trace_id": "ecosystem-w3-health-spec"
}
```

---

## Schema Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | ✅ | Always "coordination" |
| `request_id` | ✅ | Unique ID (coord-NNN) |
| `title` | ✅ | Brief description |
| `created` | ✅ | Creation date (YYYY-MM-DD) |
| `from_repo` | ✅ | Requesting repository |
| `to_repo` | ✅ | Target repository |
| `priority` | ✅ | P0 (critical), P1 (high), P2 (medium) |
| `urgency` | ✅ | blocks_sprint, next_sprint, backlog |
| `blocks` | ❌ | What this blocks (list) |
| `requested_by` | ✅ | Person/team making request |
| `requested_delivery` | ❌ | When needed (Week N, Sprint N, etc.) |
| `context` | ❌ | Background information (object) |
| `deliverables` | ✅ | What needs to be delivered (list) |
| `acceptance_criteria` | ✅ | How to verify completion (list) |
| `dependencies` | ❌ | Prerequisites (list) |
| `estimated_effort` | ❌ | Rough estimate |
| `trace_id` | ❌ | For cross-repo event correlation |

---

## Review Process (Sprint Planning)

### Every 2 Weeks

1. **Review all coordination requests**
   - Check priority and urgency
   - Verify dependencies are met
   - Assess capacity for this sprint

2. **Triage Decision:**
   - **✅ This Sprint** → Add to sprint backlog, generate task
   - **⏭️ Next Sprint** → Keep in queue, add to backlog with priority
   - **❌ Reject** → Explain why, suggest alternatives

3. **If This Sprint:**
   - Move to [`inbox/active/`](../../active/)
   - Create Diátaxis change request (Phase 3: DDD)
   - Update sprint intent document
   - Notify requesting repo

4. **If Next Sprint:**
   - Keep in `inbox/incoming/coordination/`
   - Add to project backlog
   - Set review date

5. **If Rejected:**
   - Move to rejected/ subfolder
   - Document rationale
   - Notify requesting repo

---

## Example Coordination Request

```json
{
  "type": "coordination",
  "request_id": "coord-001",
  "title": "Deliver health spec v1.1 for mcp-orchestration",
  "created": "2025-10-27",
  "from_repo": "mcp-orchestration",
  "to_repo": "ecosystem-manifest",
  "priority": "P0",
  "urgency": "blocks_sprint",
  "blocks": [
    "mcp-orchestration Sprint 3 (Week 11-12)",
    "Waypoint W3 validation"
  ],
  "requested_by": "Ecosystem Coordination Team",
  "requested_delivery": "Week 11 (by Nov 1)",
  "context": {
    "waypoint": "W3",
    "related_rfc": "rfcs/0001-health-monitoring.md",
    "background": "mcp-orchestration needs health check specification to implement HealthMonitor class. Without this spec, Week 11-12 sprint cannot proceed."
  },
  "deliverables": [
    "ecosystem-manifest.yaml v1.1 with health_check schema added",
    "QUALITY_STANDARDS.md updated with health endpoint requirements",
    "Example health check responses in documentation"
  ],
  "acceptance_criteria": [
    "Health check spec defines required fields: status (enum), version (semver), uptime_seconds (number)",
    "Health check spec defines optional fields: dependencies (object), metrics (object)",
    "Spec validated against JSON Schema format",
    "Documentation includes at least 2 example responses (healthy, unhealthy)",
    "chora-base template updated to match spec"
  ],
  "dependencies": [
    "RFC 0001 (health monitoring) must be accepted and finalized",
    "chora-base v3.5.0 health endpoint template must exist"
  ],
  "estimated_effort": "4-8 hours",
  "trace_id": "ecosystem-w3-001"
}
```

---

## Creating a Coordination Request

### From Another Repo

If you're in `mcp-orchestration` and need something from `ecosystem-manifest`:

1. Create JSON file in your local repo's coordination tracking
2. Submit as PR or GitHub Issue to chora-base
3. File placed in `inbox/incoming/coordination/`
4. Reviewed in next sprint planning (every 2 weeks)

### From Strategic Planning

When strategic work (Phase 1) generates coordination needs:

1. Break down RFC into repo-specific work
2. Create coordination request for each cross-repo dependency
3. Link to original RFC
4. Schedule for sprint planning

---

## Status Tracking

Coordination requests move through these states:

```
inbox/incoming/coordination/  (pending review)
          ↓ sprint planning
          ↓ ACCEPTED FOR THIS SPRINT
inbox/active/                 (being worked)
          ↓ implementation complete
inbox/completed/              (delivered)
```

Track status by **file location**, not a status field.

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - Complete intake process
- [INTAKE_TRIAGE_GUIDE.md](../../INTAKE_TRIAGE_GUIDE.md) - Decision criteria
- [schemas/coordination-request.schema.json](../../schemas/coordination-request.schema.json) - JSON schema
