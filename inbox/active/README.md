# Active Work

**Status:** Currently being worked (Phase 3-7)
**Contents:** Diátaxis change requests + implementation artifacts
**Process:** DDD → BDD → TDD (your existing development lifecycle)

---

## Purpose

This directory contains work that is **actively in progress** - from requirements definition (Phase 3: DDD) through implementation (Phase 4: BDD/TDD) to completion.

## Structure

Each active work item gets its own subdirectory:

```
inbox/active/
├── task-001-health-endpoint/
│   ├── task.json                    # Original task/coordination config
│   ├── change-request.md            # Diátaxis formatted (Phase 3: DDD)
│   ├── features/                    # BDD scenarios (Phase 4)
│   │   └── health-endpoint.feature
│   ├── tests/                       # TDD tests (Phase 4)
│   │   └── test_health_endpoint.py
│   ├── src/                         # Implementation (Phase 4)
│   │   └── health.py
│   └── events.jsonl                 # Event log for this work
│
└── coord-001-health-spec/
    ├── coordination.json
    ├── change-request.md
    └── ...
```

---

## Workflow Phases

### Phase 3: Requirements & Design (DDD)

**Create:** `change-request.md` (Diátaxis format)

```markdown
---
title: Change Request Title
type: change-request
task_id: task-001
phase: 3-ddd
created: YYYY-MM-DD
---

# Change Request: [Title]

## Explanation
Context, problem statement, business value, stakeholders, dependencies

## How-to Guide
User or agent workflow steps, expected journey, use cases, error scenarios

## Reference
Proposed API/tool contract, parameters, return types, examples, performance

## Acceptance Criteria
Given-When-Then scenarios extracted from above

## Tutorial (Optional)
End-to-end walkthrough, integration examples, best practices
```

**See:** [dev-docs/workflows/DDD_WORKFLOW.md](../../static-template/dev-docs/workflows/DDD_WORKFLOW.md)

**Time:** 2-4 hours (simple) to 1-2 days (complex)

---

### Phase 4: Development (BDD + TDD)

**Step 1: BDD - Write Gherkin Scenarios**

Create `features/*.feature` files:

```gherkin
Feature: Health Endpoint

  Scenario: Healthy service returns 200
    Given the service is running normally
    When I request GET /health
    Then the response status is 200
    And the response JSON contains "status": "healthy"
    And the response JSON contains "version"
    And the response JSON contains "uptime_seconds"
```

**Step 2: TDD - RED-GREEN-REFACTOR**

For each behavior:
1. Write test (RED - fails)
2. Implement minimal code (GREEN - passes)
3. Refactor (improve design, tests stay GREEN)

**Step 3: Implementation**

Write production code in `src/`

**Step 4: Event Emission**

Emit events to `events.jsonl`:
```jsonl
{"event_type": "task_started", "task_id": "task-001", "trace_id": "...", "timestamp": "..."}
{"event_type": "phase_completed", "phase": "ddd", "task_id": "task-001", "trace_id": "...", "timestamp": "..."}
{"event_type": "tests_passing", "coverage": 95, "task_id": "task-001", "trace_id": "...", "timestamp": "..."}
```

**See:**
- [dev-docs/workflows/BDD_WORKFLOW.md](../../static-template/dev-docs/workflows/BDD_WORKFLOW.md)
- [dev-docs/workflows/TDD_WORKFLOW.md](../../static-template/dev-docs/workflows/TDD_WORKFLOW.md)
- [dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](../../static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)

**Time:** 4-8 hours (simple) to 3-5 days (complex)

---

### Phase 5-7: Testing, Review, Release

**Phase 5:** Testing & Quality
- Unit tests ✅
- Integration tests
- Coverage ≥85%
- Linting, type checking

**Phase 6:** Review & Integration
- Code review
- Docs review
- CI/CD pipeline
- Merge to main

**Phase 7:** Release & Deployment
- Version bump
- Changelog
- Build
- Publish
- Deploy

**See:** [dev-docs/workflows/DEVELOPMENT_PROCESS.md](../../static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md)

---

## Moving to Active

### From incoming/coordination/
```bash
# 1. Create active directory
mkdir inbox/active/coord-NNN-title/

# 2. Move coordination request
mv inbox/incoming/coordination/coord-NNN.json \
   inbox/active/coord-NNN-title/coordination.json

# 3. Create change request (Phase 3: DDD)
# ... follow DDD workflow ...
```

### From incoming/tasks/
```bash
# 1. Create active directory
mkdir inbox/active/task-NNN-title/

# 2. Move task
mv inbox/incoming/tasks/task-NNN.json \
   inbox/active/task-NNN-title/task.json

# 3. Create change request (Phase 3: DDD)
# ... follow DDD workflow ...
```

---

## Completion Criteria

Work is complete when:
- ✅ All acceptance criteria met
- ✅ Tests passing (≥85% coverage)
- ✅ Code review approved
- ✅ Documentation updated
- ✅ CI/CD pipeline green
- ✅ Merged to main
- ✅ Released (if applicable)

Then move to `inbox/completed/`.

---

## Claude Code Workflow

When Claude is working on an active task:

```markdown
You: "Work on inbox/active/task-001-health-endpoint/"

Claude:
1. Reads task.json to understand requirements
2. Reads change-request.md for design (if exists)
3. OR creates change-request.md following DDD workflow
4. Writes BDD scenarios in features/
5. Implements using TDD (RED-GREEN-REFACTOR)
6. Emits events to events.jsonl
7. Runs tests, achieves ≥85% coverage
8. Asks: "Ready to move to completed?"
```

---

## Current Active Work

*Check subdirectories to see what's currently in progress*

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../INBOX_PROTOCOL.md) - Complete intake process
- [dev-docs/workflows/](../../static-template/dev-docs/workflows/) - Your development workflows (DDD, BDD, TDD)
