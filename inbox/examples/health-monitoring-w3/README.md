# Example: Health Monitoring & Auto-Recovery (W3)

**Purpose**: Complete end-to-end example showing how Waypoint W3 (Health Monitoring & Auto-Recovery) flows through the inbox system.

**Trace ID**: `ecosystem-w3-health-monitoring`

**Timeline**: 16 weeks across 4 repositories

---

## Overview

This example demonstrates:
1. **Strategic Proposal** (Type 1) → Quarterly review → RFC → ADR
2. **Coordination Requests** (Type 2) → Sprint planning → Task generation
3. **Implementation Tasks** (Type 3) → DDD → BDD → TDD → Completion
4. **Event correlation** using CHORA_TRACE_ID
5. **Cross-repo dependencies** and fulfillment tracking

---

## Timeline

```
Week 1-2:   Strategic proposal created and reviewed
Week 3-4:   RFC process, acceptance, ADR created
Week 5-6:   Coordination requests created for all 4 repos
Week 7-10:  Sprint planning, task generation, Week 1-2 implementation
Week 11-14: Week 3-4 implementation
Week 15-16: Integration testing, W3 validation
```

---

## Repositories Involved

1. **chora-base**: Health endpoint template, standards
2. **ecosystem-manifest**: Health check spec, quality standards
3. **mcp-orchestration**: Health monitoring service, auto-recovery
4. **mcp-gateway**: Health status aggregation, client notifications

---

## Files in This Example

### Strategic Phase
- `strategic/prop-001-health-monitoring.md` - Initial strategic proposal (Type 1)
- `strategic/0001-health-monitoring-rfc.md` - RFC after acceptance
- `strategic/0001-health-check-format-adr.md` - ADR for technical decision

### Coordination Phase
- `coordination/coord-001-chora-base.json` - Request to chora-base
- `coordination/coord-002-ecosystem-manifest.json` - Request to ecosystem-manifest
- `coordination/coord-003-mcp-orchestration.json` - Request to mcp-orchestration
- `coordination/coord-004-mcp-gateway.json` - Request to mcp-gateway

### Implementation Phase
- `tasks/task-001-health-template.json` - chora-base: Create health endpoint template
- `tasks/task-002-health-spec.json` - ecosystem-manifest: Write health check spec
- `tasks/task-003-monitoring-service.json` - mcp-orchestration: Build monitoring service
- `tasks/task-004-status-aggregation.json` - mcp-gateway: Aggregate health status

### Event Timeline
- `events/complete-timeline.jsonl` - All events with trace_id correlation
- `events/timeline-analysis.md` - Human-readable timeline with analysis

---

## How to Use This Example

### 1. View Strategic Flow
```bash
# Read the initial proposal
cat inbox/examples/health-monitoring-w3/strategic/prop-001-health-monitoring.md

# See RFC process
cat inbox/examples/health-monitoring-w3/strategic/0001-health-monitoring-rfc.md

# View technical decision
cat inbox/examples/health-monitoring-w3/strategic/0001-health-check-format-adr.md
```

### 2. View Coordination Flow
```bash
# See all coordination requests
jq . inbox/examples/health-monitoring-w3/coordination/*.json

# Filter by priority
jq 'select(.priority == "P0")' \
  inbox/examples/health-monitoring-w3/coordination/*.json

# Check fulfillment status
jq 'select(.fulfillment.completed_date != null)' \
  inbox/examples/health-monitoring-w3/coordination/*.json
```

### 3. View Implementation Flow
```bash
# See all tasks
jq . inbox/examples/health-monitoring-w3/tasks/*.json

# Check task status
jq '.workflow.status' inbox/examples/health-monitoring-w3/tasks/*.json

# View task dependencies
jq '.dependencies' inbox/examples/health-monitoring-w3/tasks/*.json
```

### 4. View Event Timeline
```bash
# All events for this trace
grep 'ecosystem-w3-health-monitoring' \
  inbox/examples/health-monitoring-w3/events/complete-timeline.jsonl

# Strategic events only
jq 'select(.event_type | startswith("proposal_"))' \
  inbox/examples/health-monitoring-w3/events/complete-timeline.jsonl

# Coordination events only
jq 'select(.event_type | startswith("coordination_"))' \
  inbox/examples/health-monitoring-w3/events/complete-timeline.jsonl

# Task events only
jq 'select(.event_type | startswith("task_"))' \
  inbox/examples/health-monitoring-w3/events/complete-timeline.jsonl
```

### 5. Generate Timeline Analysis
```bash
# Human-readable timeline with metrics
cat inbox/examples/health-monitoring-w3/events/timeline-analysis.md
```

---

## Key Lessons from This Example

### 1. Strategic Proposals Take Time
- **Week 1-2**: Proposal creation and review
- **Week 3-4**: RFC process with FCP (Final Comment Period)
- Don't rush strategic decisions

### 2. Coordination Happens in Parallel
- All 4 coordination requests created simultaneously
- Each repo triages independently during sprint planning
- Dependencies tracked explicitly

### 3. Implementation Can Be Parallelized
- task-001 (chora-base) and task-002 (ecosystem-manifest) run in parallel
- task-003 (mcp-orchestration) depends on task-002 completion
- task-004 (mcp-gateway) depends on task-003 completion

### 4. Event Correlation is Powerful
- Single `CHORA_TRACE_ID` links all work
- Can filter events to see complete story
- Enables cross-repo debugging and audit trails

### 5. Fulfillment Notifications Close the Loop
- Coordination requests include `fulfillment.notification_sent: true`
- Requesting repo knows when work is done
- Prevents duplicate requests or confusion

---

## Metrics from This Example

```yaml
strategic_phase:
  duration_weeks: 4
  proposals: 1
  rfcs: 1
  adrs: 1

coordination_phase:
  duration_weeks: 2
  requests: 4
  priority_p0: 2
  priority_p1: 2

implementation_phase:
  duration_weeks: 10
  tasks: 4
  repos_involved: 4
  parallel_tasks: 2
  sequential_tasks: 2

total_duration: 16 weeks
total_events: 47
cross_repo_dependencies: 3
```

---

## Next Steps

After reviewing this example:
1. Adapt the pattern for your own waypoints
2. Use the JSON structures as templates
3. Follow the event emission patterns
4. Leverage CHORA_TRACE_ID for correlation
5. Build your own end-to-end flows

---

## Related Documentation

- [../../INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - Complete protocol documentation
- [../../CLAUDE.md](../../CLAUDE.md) - Claude Code patterns
- [../../incoming/coordination/README.md](../../incoming/coordination/README.md) - Type 2 intake
- [../../ecosystem/proposals/README.md](../../ecosystem/proposals/README.md) - Type 1 intake
- [../../incoming/tasks/README.md](../../incoming/tasks/README.md) - Type 3 intake
