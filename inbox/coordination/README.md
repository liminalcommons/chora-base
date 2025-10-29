# Cross-Repo Coordination

**Purpose:** Shared coordination infrastructure for multi-repo ecosystem
**Contents:** Event logs, capability registry, ecosystem dashboard

---

## Purpose

This directory contains **shared coordination infrastructure** that enables multiple repositories to work together cohesively while maintaining their independence.

## Contents

### 1. Event Log (`events.jsonl`)

**Centralized JSONL event log** for cross-repo traceability.

**Format:** One JSON object per line, append-only

**Required Fields:**
- `event_type` - Type of event (task_started, phase_completed, etc.)
- `trace_id` - Correlation ID (e.g., `CHORA_TRACE_ID`)
- `timestamp` - ISO 8601 format
- `repo` - Which repository emitted this event

**Optional Fields:**
- `task_id` - Task or coordination request ID
- `phase` - Development phase (ddd, bdd, tdd)
- `duration_hours` - How long something took
- Custom fields per event type

**Example:**
```jsonl
{"event_type": "coordination_request_created", "request_id": "coord-001", "from_repo": "mcp-orchestration", "to_repo": "ecosystem-manifest", "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T09:00:00Z", "repo": "chora-base"}
{"event_type": "task_started", "task_id": "task-001", "title": "Add health spec v1.1", "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T09:15:00Z", "repo": "ecosystem-manifest"}
{"event_type": "phase_completed", "phase": "ddd", "task_id": "task-001", "duration_hours": 2.0, "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T11:15:00Z", "repo": "ecosystem-manifest"}
{"event_type": "task_completed", "task_id": "task-001", "duration_hours": 6.5, "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T15:30:00Z", "repo": "ecosystem-manifest"}
{"event_type": "coordination_request_fulfilled", "request_id": "coord-001", "to_repo": "mcp-orchestration", "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T15:35:00Z", "repo": "ecosystem-manifest"}
```

**Usage:**
```bash
# Watch events in real-time
tail -f inbox/coordination/events.jsonl

# Filter by trace ID
grep '"trace_id": "ecosystem-w3-001"' inbox/coordination/events.jsonl

# Filter by repo
grep '"repo": "ecosystem-manifest"' inbox/coordination/events.jsonl

# Extract for completed task
grep '"trace_id": "task-001-trace"' inbox/coordination/events.jsonl \
  > inbox/completed/task-001/events.jsonl
```

---

### 2. Capability Registry (`CAPABILITIES/`)

**Per-repo capability declarations** - what each repo can do and provides.

**Format:** YAML files, one per repository

**File:** `CAPABILITIES/repo-name.yaml`

**Structure:**
```yaml
repo: ecosystem-manifest
version: 1.0.0
updated: 2025-10-27

provides:
  - server_registry
  - health_specifications
  - quality_standards
  - manifest_schema

consumes:
  - chora-base:mcp_template
  - chora-base:drso_validation

capabilities:
  can_receive:
    - type: coordination
      for: [add_server, update_health_spec, modify_quality_gate]
    - type: task
      for: [update_manifest, add_spec, update_standards]

  dependencies:
    - repo: chora-base
      version: ">=3.5.0"
      reason: "Requires health endpoint template"

  inbox_protocol_version: "1.0"

maintainers:
  - name: Victor
    github: victorpiper

contact:
  - type: github_issue
    url: https://github.com/liminalcommons/ecosystem-manifest/issues
  - type: slack
    channel: "#ecosystem-dev"
```

**Usage:**
```bash
# Check if repo can handle a task type
yq '.capabilities.can_receive[].for[]' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

# Check dependencies
yq '.capabilities.dependencies' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml
```

---

### 3. Ecosystem Dashboard (`ECOSYSTEM_STATUS.yaml`)

**Live dashboard** showing current state of all repos in ecosystem.

**Format:** YAML, updated automatically or manually

**Structure:**
```yaml
ecosystem: liminal-commons
updated: 2025-10-27T16:00:00Z

repositories:
  - name: chora-base
    status: active
    version: v3.3.0
    next_release: v3.5.0
    active_work:
      - task-001: Health endpoint template
    pending_coordination: []
    health: healthy

  - name: ecosystem-manifest
    status: active
    version: v1.0.0
    next_release: v1.1.0
    active_work:
      - task-002: Add health spec v1.1
    pending_coordination:
      - coord-001: Deliver health spec for mcp-orchestration
    health: healthy

  - name: mcp-orchestration
    status: in_development
    version: v0.2.0
    next_release: v0.6.0
    active_work: []
    pending_coordination:
      - coord-001: Waiting for health spec from ecosystem-manifest
    blocked_by:
      - ecosystem-manifest:health-spec-v1.1
    health: healthy

  - name: mcp-gateway
    status: active
    version: v1.2.0
    next_release: v1.3.0
    active_work: []
    pending_coordination: []
    health: healthy

waypoints:
  W1:
    status: completed
    completed_date: 2025-10-18
    description: Basic Discovery & Deployment

  W2:
    status: in_progress
    target_date: 2026-01
    description: Automatic Updates
    progress: 40%

  W3:
    status: planned
    target_date: 2026-02
    description: Health Monitoring & Auto-Recovery
    progress: 15%
    blocked_by:
      - ecosystem-manifest:health-spec-v1.1

metrics:
  total_repos: 4
  active_repos: 3
  in_development_repos: 1
  total_coordination_requests: 1
  pending_requests: 1
  completed_waypoints: 1
  in_progress_waypoints: 1
```

**Usage:**
```bash
# Check ecosystem status
yq . inbox/coordination/ECOSYSTEM_STATUS.yaml

# Find blocked work
yq '.repositories[] | select(.blocked_by) | .name' \
  inbox/coordination/ECOSYSTEM_STATUS.yaml

# Check waypoint progress
yq '.waypoints' inbox/coordination/ECOSYSTEM_STATUS.yaml
```

---

## Workflow Integration

### When Creating Coordination Request

```bash
# 1. Create coordination request JSON
cat > inbox/incoming/coordination/coord-NNN.json <<EOF
{
  "type": "coordination",
  "request_id": "coord-NNN",
  ...
  "trace_id": "ecosystem-wN-NNN"
}
EOF

# 2. Emit event
echo '{"event_type": "coordination_request_created", "request_id": "coord-NNN", "from_repo": "mcp-orchestration", "to_repo": "ecosystem-manifest", "trace_id": "ecosystem-wN-NNN", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
  >> inbox/coordination/events.jsonl

# 3. Update dashboard
# (Update ECOSYSTEM_STATUS.yaml with pending request)
```

### When Starting Task

```bash
# Emit event
echo '{"event_type": "task_started", "task_id": "task-NNN", "trace_id": "....", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
  >> inbox/coordination/events.jsonl
```

### When Completing Task

```bash
# 1. Emit completion event
echo '{"event_type": "task_completed", "task_id": "task-NNN", "duration_hours": 6.5, "trace_id": "...", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
  >> inbox/coordination/events.jsonl

# 2. If coordination request, emit fulfillment
if [[ -f coordination.json ]]; then
  echo '{"event_type": "coordination_request_fulfilled", "request_id": "coord-NNN", "to_repo": "mcp-orchestration", "trace_id": "...", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
    >> inbox/coordination/events.jsonl
fi

# 3. Update dashboard
# (Update ECOSYSTEM_STATUS.yaml to remove from pending)
```

---

## Trace Context Propagation

Following chora-compose pattern, use `CHORA_TRACE_ID` environment variable:

```bash
# Set trace ID for entire workflow
export CHORA_TRACE_ID="ecosystem-w3-health-monitoring"

# All tools emit events with this trace_id
# Makes it easy to filter later
```

---

## Event Types Reference

| Event Type | When | Required Fields |
|------------|------|-----------------|
| `coordination_request_created` | New coordination request | `request_id`, `from_repo`, `to_repo` |
| `coordination_request_accepted` | Request accepted in sprint planning | `request_id` |
| `coordination_request_fulfilled` | Deliverables completed | `request_id`, `to_repo` |
| `task_started` | Implementation begins | `task_id` |
| `task_completed` | Implementation done | `task_id`, `duration_hours` |
| `phase_started` | Development phase begins | `phase` |
| `phase_completed` | Development phase done | `phase`, `duration_hours` |
| `waypoint_started` | Waypoint work begins | `waypoint` |
| `waypoint_completed` | Waypoint achieved | `waypoint` |
| `release_published` | Version released | `version`, `repo` |

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../INBOX_PROTOCOL.md) - Complete intake process
- [ADR 0001](../ecosystem/adrs/) - Event log format standard (if exists)
