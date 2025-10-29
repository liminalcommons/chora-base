# Completed Work

**Status:** Done and archived
**Purpose:** Historical record and audit trail
**Contents:** Tasks, change requests, test reports, event logs

---

## Purpose

This directory contains **completed work items** with full historical record of what was done, when, and how.

## Why Archive Completed Work?

- 📊 **Metrics** - Analyze velocity, effort estimates, quality
- 🔍 **Audit Trail** - Who did what, when, and why
- 📚 **Knowledge** - Learn from past implementations
- 🔗 **Traceability** - Link released features back to original requests
- 🎓 **Onboarding** - Show new team members how work flows

---

## Structure

Each completed work item gets its own directory with full artifacts:

```
inbox/completed/
└── task-001-health-endpoint/
    ├── task.json                      # Original task definition
    ├── change-request.md              # Diátaxis change request (Phase 3)
    ├── events.jsonl                   # Event log (filtered by trace_id)
    ├── metadata.json                  # Completion metadata
    ├── test-report.json               # Test results
    ├── coverage-report.json           # Coverage stats
    ├── pr-link.txt                    # Link to merged PR
    └── release-notes-fragment.md      # For changelog
```

---

## Completion Metadata

Each completed item includes `metadata.json`:

```json
{
  "task_id": "task-001",
  "title": "Add health endpoint to chora-base template",
  "type": "task",
  "started": "2025-10-27T09:00:00Z",
  "completed": "2025-10-27T15:30:00Z",
  "duration_hours": 6.5,
  "sprint": "Week 9-10",
  "repo": "chora-base",
  "assigned_to": "Claude Code",
  "phase_durations": {
    "ddd": 2.0,
    "bdd": 1.0,
    "tdd": 3.0,
    "review": 0.5
  },
  "deliverables": [
    "static-template/templates/mcp-server/src/health.py",
    "static-template/templates/mcp-server/README.md updated",
    "tests/test_health.py"
  ],
  "test_results": {
    "total_tests": 12,
    "passed": 12,
    "failed": 0,
    "coverage_percent": 95.2
  },
  "quality_metrics": {
    "lines_of_code": 150,
    "test_lines": 180,
    "mypy_errors": 0,
    "ruff_violations": 0
  },
  "release_info": {
    "version": "v3.5.0",
    "pr_number": 42,
    "merged_at": "2025-10-27T16:00:00Z"
  },
  "cross_repo_notifications": [
    {
      "repo": "mcp-orchestration",
      "notification": "Health spec v1.1 delivered",
      "sent_at": "2025-10-27T15:35:00Z"
    }
  ],
  "trace_id": "chora-base-health-001"
}
```

---

## Event Log

Each completed item includes `events.jsonl` (filtered by `trace_id`):

```jsonl
{"event_type": "task_started", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T09:00:00Z"}
{"event_type": "phase_started", "phase": "ddd", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T09:00:00Z"}
{"event_type": "change_request_created", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T10:30:00Z"}
{"event_type": "phase_completed", "phase": "ddd", "duration_hours": 2.0, "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T11:00:00Z"}
{"event_type": "phase_started", "phase": "bdd", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T11:00:00Z"}
{"event_type": "bdd_scenario_written", "scenario": "Healthy service returns 200", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T11:30:00Z"}
{"event_type": "phase_completed", "phase": "bdd", "duration_hours": 1.0, "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T12:00:00Z"}
{"event_type": "phase_started", "phase": "tdd", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T12:00:00Z"}
{"event_type": "test_written", "test_name": "test_health_endpoint_healthy", "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T12:15:00Z"}
{"event_type": "tests_passing", "total": 12, "passed": 12, "coverage": 95.2, "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T15:00:00Z"}
{"event_type": "phase_completed", "phase": "tdd", "duration_hours": 3.0, "task_id": "task-001", "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T15:00:00Z"}
{"event_type": "task_completed", "task_id": "task-001", "duration_hours": 6.5, "trace_id": "chora-base-health-001", "timestamp": "2025-10-27T15:30:00Z"}
```

---

## Moving to Completed

### After Work is Done

```bash
# 1. Create completion directory
mkdir inbox/completed/task-001-health-endpoint/

# 2. Move task artifacts
mv inbox/active/task-001-health-endpoint/* \
   inbox/completed/task-001-health-endpoint/

# 3. Generate metadata.json
# (Extract from events.jsonl, test reports, coverage reports)

# 4. Filter events by trace_id
grep '"trace_id": "chora-base-health-001"' inbox/coordination/events.jsonl \
  > inbox/completed/task-001-health-endpoint/events.jsonl

# 5. Add test and coverage reports
cp test-output/report.json inbox/completed/task-001-health-endpoint/test-report.json
cp coverage/report.json inbox/completed/task-001-health-endpoint/coverage-report.json

# 6. Add PR link
echo "https://github.com/liminalcommons/chora-base/pull/42" \
  > inbox/completed/task-001-health-endpoint/pr-link.txt

# 7. Add release notes fragment
cat > inbox/completed/task-001-health-endpoint/release-notes-fragment.md <<EOF
### Added
- Health endpoint standard in chora-base MCP server template
- Health endpoint returns status, version, uptime_seconds
- Supports optional dependencies and metrics fields

### Documentation
- Updated templates/mcp-server/README.md with health endpoint usage
- Added example health responses

### Tests
- 12 new tests for health endpoint (95.2% coverage)
EOF

# 8. Commit
git add inbox/completed/task-001-health-endpoint/
git commit -m "chore(inbox): Archive completed task-001"
```

---

## Cross-Repo Notifications

When work completes that affects other repos, notify them:

```bash
# For coordination requests
if [[ -f coordination.json ]]; then
  from_repo=$(jq -r '.from_repo' coordination.json)

  # Send notification (create issue, post to Slack, etc.)
  gh issue create \
    --repo liminalcommons/$from_repo \
    --title "✅ Delivered: $(jq -r '.title' coordination.json)" \
    --body "Your coordination request has been completed.

    Deliverables: $(jq -r '.deliverables | join(", ")' coordination.json)

    See: https://github.com/liminalcommons/chora-base/tree/main/inbox/completed/coord-001"
fi
```

---

## Analyzing Completed Work

### Velocity Metrics

```bash
# Average time per task type
jq -s 'group_by(.type) | map({type: .[0].type, avg_hours: (map(.duration_hours) | add / length)})' \
  inbox/completed/*/metadata.json

# Phase breakdown
jq -s 'map(.phase_durations) | add | to_entries | map({phase: .key, total_hours: .value})' \
  inbox/completed/*/metadata.json
```

### Quality Metrics

```bash
# Average test coverage
jq -s 'map(.test_results.coverage_percent) | add / length' \
  inbox/completed/*/metadata.json

# Defect rate
jq -s 'map(select(.test_results.failed > 0)) | length' \
  inbox/completed/*/metadata.json
```

### Effort Estimation Accuracy

```bash
# Compare estimated vs actual
jq -s 'map({
  estimated: .task.estimated_effort,
  actual: .duration_hours,
  diff: (.duration_hours - (.task.estimated_effort | split("-") | map(tonumber) | add / 2))
})' inbox/completed/*/metadata.json
```

---

## Retention Policy

**Keep indefinitely** (or until project archived):
- All completed work artifacts
- Full event logs
- Test reports
- Metadata

**Rationale:**
- Git handles storage efficiently
- Historical data invaluable for metrics
- Audit trail required for compliance
- Knowledge base for onboarding

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../INBOX_PROTOCOL.md) - Complete intake process
- [inbox/coordination/README.md](../coordination/README.md) - Event correlation
