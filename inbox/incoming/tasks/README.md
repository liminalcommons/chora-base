# Implementation Tasks

**Intake Type:** Type 3 - Implementation Task
**Review Frequency:** Continuous (as approved)
**Decision Makers:** Individual engineers
**Phase:** Phase 3 (Requirements & Design - DDD)

---

## Purpose

This directory contains **approved implementation tasks** ready to enter the development lifecycle (Phase 3: DDD → Phase 4: BDD/TDD).

## When to Use

Create an implementation task here when:
- ✅ Task is **already approved** for current sprint
- ✅ Task is **single-repo** (no cross-repo coordination needed)
- ✅ Task is **well-defined** with acceptance criteria
- ✅ Task is **ready to implement** (deps met, design approved)

**Common sources:**
- Sprint backlog items
- Bug fixes
- Small improvements
- Maintenance tasks
- Approved feature work

**Do NOT use for:**
- ❌ Strategic proposals (use `inbox/ecosystem/proposals/`)
- ❌ Cross-repo coordination (use `inbox/incoming/coordination/`)
- ❌ Unplanned work (discuss in sprint planning first)

---

## Task Format

Implementation tasks are JSON files following this schema:

```json
{
  "type": "task",
  "task_id": "task-001",
  "title": "Add health endpoint to chora-base MCP template",
  "created": "2025-10-27",
  "sprint": "Week 9-10",
  "priority": "P0 | P1 | P2",
  "category": "feature | bug | refactor | docs | test | chore",
  "repo": "chora-base",
  "assigned_to": "AI Agent | Developer Name",
  "estimated_effort": "4-8 hours",
  "context": {
    "background": "Why this task exists",
    "related_work": ["Links to RFCs, issues, etc."]
  },
  "deliverables": [
    "templates/mcp-server/src/health.py with health endpoint",
    "Updated documentation in templates/mcp-server/README.md"
  ],
  "acceptance_criteria": [
    "Health endpoint returns JSON with status, version, uptime",
    "Health endpoint supports optional dependencies field",
    "Tests cover happy path and error cases",
    "Documentation includes usage examples"
  ],
  "dependencies": [],
  "trace_id": "chora-base-health-template"
}
```

---

## Schema Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | ✅ | Always "task" |
| `task_id` | ✅ | Unique ID (task-NNN) |
| `title` | ✅ | Brief description |
| `created` | ✅ | Creation date (YYYY-MM-DD) |
| `sprint` | ✅ | Which sprint (Week N-M, Sprint N) |
| `priority` | ✅ | P0 (critical), P1 (high), P2 (medium) |
| `category` | ✅ | feature, bug, refactor, docs, test, chore |
| `repo` | ✅ | Target repository |
| `assigned_to` | ❌ | Who's working on it |
| `estimated_effort` | ✅ | Rough estimate |
| `context` | ❌ | Background info (object) |
| `deliverables` | ✅ | What will be created (list) |
| `acceptance_criteria` | ✅ | How to verify done (list) |
| `dependencies` | ❌ | Prerequisites (list) |
| `trace_id` | ❌ | For event correlation |

---

## Workflow (Your Existing DDD → BDD → TDD Process!)

### Step 1: Triage (Quick Check)
```bash
✅ Is this in current sprint? (Check sprint intent doc)
✅ Are dependencies met?
✅ Is assignee available?

If yes to all → Move to inbox/active/
If no → Keep in inbox/incoming/tasks/ until ready
```

### Step 2: Move to Active
```bash
mv inbox/incoming/tasks/task-001.json inbox/active/task-001/task.json
```

### Step 3: Phase 3 - Requirements & Design (DDD)
Create Diátaxis change request: `inbox/active/task-001/change-request.md`

**Your existing process:**
1. **Explanation** - Context, problem, business value
2. **How-to** - User/agent workflow steps
3. **Reference** - API design, parameters, types
4. **Extract acceptance criteria** - From task JSON

**See:** [dev-docs/workflows/DDD_WORKFLOW.md](../../../static-template/dev-docs/workflows/DDD_WORKFLOW.md)

### Step 4: Phase 4 - Development (BDD + TDD)
**Your existing process:**
1. **BDD**: Write Gherkin scenarios (from acceptance criteria)
2. **TDD**: RED-GREEN-REFACTOR cycles
3. **Implementation**: Code + tests
4. **Emit events**: Write to `inbox/coordination/events.jsonl`

**See:**
- [dev-docs/workflows/BDD_WORKFLOW.md](../../../static-template/dev-docs/workflows/BDD_WORKFLOW.md)
- [dev-docs/workflows/TDD_WORKFLOW.md](../../../static-template/dev-docs/workflows/TDD_WORKFLOW.md)

### Step 5: Completion
```bash
# Move to completed/
mv inbox/active/task-001/ inbox/completed/task-001/

# Add metadata
# - events.jsonl (filtered by trace_id)
# - test-report.json
# - coverage-report.json
# - completion-metadata.json
```

---

## Example Task

```json
{
  "type": "task",
  "task_id": "task-001",
  "title": "Add health endpoint standard to chora-base template",
  "created": "2025-10-27",
  "sprint": "Week 9-10",
  "priority": "P0",
  "category": "feature",
  "repo": "chora-base",
  "assigned_to": "Claude Code",
  "estimated_effort": "4-6 hours",
  "context": {
    "background": "Chora-base MCP server template needs a standardized health endpoint to support ecosystem-wide health monitoring (Waypoint W3)",
    "related_work": [
      "inbox/ecosystem/rfcs/0001-health-monitoring.md",
      "inbox/incoming/coordination/coord-001.json"
    ]
  },
  "deliverables": [
    "templates/mcp-server/src/health.py - Health endpoint module",
    "templates/mcp-server/README.md - Updated with health endpoint docs",
    "tests/test_health.py - Comprehensive test coverage"
  ],
  "acceptance_criteria": [
    "Health endpoint returns JSON with required fields: status, version, uptime_seconds",
    "Health endpoint supports optional fields: dependencies, metrics",
    "Status enum supports: healthy, degraded, unhealthy",
    "Endpoint returns 200 for healthy, 503 for unhealthy",
    "Tests achieve ≥90% coverage",
    "Documentation includes 2+ example responses"
  ],
  "dependencies": [
    "RFC 0001 health monitoring must be accepted"
  ],
  "trace_id": "chora-base-health-001"
}
```

---

## Creating a Task

### From Sprint Planning
After sprint planning, create tasks for sprint backlog items:

```bash
# 1. Create task JSON
cat > inbox/incoming/tasks/task-NNN.json <<EOF
{
  "type": "task",
  "task_id": "task-NNN",
  ...
}
EOF

# 2. Commit to repo
git add inbox/incoming/tasks/task-NNN.json
git commit -m "feat(inbox): Add task-NNN for Sprint N"
```

### From Coordination Request
When coordination request is accepted:

```bash
# Extract implementation task from coordination request
# Create task JSON with reference to coordination request
```

### From Bug Report
When bug is triaged and prioritized:

```bash
# Create task with category: "bug"
# Link to GitHub issue
# Add acceptance criteria for fix verification
```

---

## Status Tracking

```
inbox/incoming/tasks/  (approved, not started)
          ↓ triage: ready to start
inbox/active/          (in progress - Phase 3-4)
          ↓ implementation complete
inbox/completed/       (done)
```

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - Complete intake process
- [dev-docs/workflows/DEVELOPMENT_PROCESS.md](../../../static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - Your existing DDD → BDD → TDD process
- [schemas/implementation-task.schema.json](../../schemas/implementation-task.schema.json) - JSON schema
