# Cross-Repository Inbox Protocol

**Version:** 1.0.0
**Status:** Active
**Created:** 2025-10-27
**Maintainer:** Ecosystem Coordination Team

---

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Intake Types](#intake-types)
4. [Directory Structure](#directory-structure)
5. [Workflow by Type](#workflow-by-type)
6. [Triage Process](#triage-process)
7. [Event Correlation](#event-correlation)
8. [Capability-Based Routing](#capability-based-routing)
9. [Integration with Development Process](#integration-with-development-process)
10. [Tools & Automation](#tools--automation)
11. [Examples](#examples)

---

## Overview

### Purpose

The Inbox Protocol is a **cross-repository coordination system** that enables multiple repositories in the Liminal Commons ecosystem to work together cohesively while maintaining their autonomy.

### Key Features

- ✅ **Three-level intake** - Strategic, Coordination, Implementation
- ✅ **Respects development process** - Integrates with existing DDD → BDD → TDD workflow
- ✅ **Event-driven traceability** - JSONL event log with `CHORA_TRACE_ID`
- ✅ **Capability-based routing** - Tasks sent to repos that can handle them
- ✅ **Git-native** - No external infrastructure required
- ✅ **Claude Code optimized** - JSON configs + executable markdown

### Design Philosophy

**"Ecosystem communications influence team direction"** - Strategic proposals and coordination requests flow through proper planning phases (Vision & Strategy → Planning & Prioritization) before becoming implementation tasks.

This ensures:
- 🎯 Alignment with strategic goals
- 📊 Proper resource allocation
- 🔍 Informed decision-making
- 🤝 Stakeholder buy-in

---

## Design Principles

### 1. **Respect Strategic Process**
Don't bypass Vision & Strategy or Planning & Prioritization phases. Strategic proposals get quarterly review, coordination requests get sprint planning review.

### 2. **Three-Level Intake**
- **Type 1 (Strategic):** Influences vision/roadmap, reviewed quarterly
- **Type 2 (Coordination):** Cross-repo dependencies, reviewed in sprint planning
- **Type 3 (Implementation):** Approved tasks, continuous intake

### 3. **Appropriate Cadence**
- Strategic: Quarterly
- Coordination: Every 2 weeks (sprint planning)
- Implementation: Continuous

### 4. **Right Decision Makers**
- Strategic: Leadership + Team
- Coordination: Product + Engineering Leads
- Implementation: Individual Engineers

### 5. **Preserve Existing Workflows**
Phase 3-7 of development process (DDD → BDD → TDD) remain unchanged. Inbox adds coordination layer for Phases 1-2.

### 6. **Enable Cross-Repo Coordination**
While respecting each repo's autonomy and release cycle.

---

## Intake Types

### Type 1: Strategic Proposal

**Phase:** 1 (Vision & Strategy)
**Review:** Quarterly
**Format:** Markdown in `inbox/ecosystem/proposals/`
**Schema:** [strategic-proposal.schema.json](schemas/strategic-proposal.schema.json)

**When to use:**
- 🌍 Ecosystem-wide changes (affects 2+ repos)
- 📊 New capability waves or waypoints
- 🏗️ Architectural patterns
- 🔄 External ecosystem integration
- 📈 Strategic direction changes

**Lifecycle:**
```
proposals/ → quarterly review → accepted? → rfcs/ → adr/ → coordination/
                               ↓ deferred
                               deferred/
```

**See:** [inbox/ecosystem/proposals/README.md](ecosystem/proposals/README.md)

---

### Type 2: Coordination Request

**Phase:** 2 (Planning & Prioritization)
**Review:** Sprint Planning (every 2 weeks)
**Format:** JSON in `inbox/incoming/coordination/`
**Schema:** [coordination-request.schema.json](schemas/coordination-request.schema.json)

**When to use:**
- 🔗 Work spans multiple repos
- 📦 Work has dependencies on other repos
- 🚧 Work blocks other teams' progress
- ⏱️ Work has specific timing requirements
- 🎯 Work is part of coordinated release

**Lifecycle:**
```
incoming/coordination/ → sprint planning → accepted? → active/ → completed/
                                         ↓ defer
                                         (stays in incoming/)
```

**See:** [inbox/incoming/coordination/README.md](incoming/coordination/README.md)

---

### Type 3: Implementation Task

**Phase:** 3-7 (Design through Release)
**Review:** Continuous (as approved)
**Format:** JSON in `inbox/incoming/tasks/`
**Schema:** [implementation-task.schema.json](schemas/implementation-task.schema.json)

**When to use:**
- ✅ Task already approved for current sprint
- ✅ Single-repo task (no cross-repo coordination)
- ✅ Well-defined with acceptance criteria
- ✅ Ready to implement (deps met, design approved)

**Lifecycle:**
```
incoming/tasks/ → quick check → ready? → active/ → DDD → BDD → TDD → completed/
```

**See:** [inbox/incoming/tasks/README.md](incoming/tasks/README.md)

---

## Directory Structure

```
inbox/
├── ecosystem/                          # Type 1: Strategic
│   ├── proposals/                     # New strategic ideas
│   │   ├── README.md
│   │   └── prop-NNN-title.md
│   ├── rfcs/                          # Accepted proposals under discussion
│   │   ├── README.md
│   │   └── NNNN-title.md
│   ├── adrs/                          # Finalized decisions
│   │   ├── README.md
│   │   └── NNNN-title.md
│   ├── deferred/                      # Rejected/deferred proposals
│   │   └── prop-NNN-title.md
│   └── [existing strategic docs]     # multi-repo-capability-evolution-to-w3.md, etc.
│
├── incoming/                           # Type 2 & 3: Active intake
│   ├── coordination/                  # Type 2: Cross-repo requests
│   │   ├── README.md
│   │   └── coord-NNN.json
│   └── tasks/                         # Type 3: Implementation tasks
│       ├── README.md
│       └── task-NNN.json
│
├── active/                             # Currently being worked
│   ├── README.md
│   └── task-NNN-title/
│       ├── task.json                  # Original task
│       ├── change-request.md          # Diátaxis change request (DDD)
│       ├── features/                  # BDD scenarios
│       ├── tests/                     # TDD tests
│       ├── src/                       # Implementation
│       └── events.jsonl               # Work-specific events
│
├── completed/                          # Archived
│   ├── README.md
│   └── task-NNN-title/
│       ├── task.json
│       ├── change-request.md
│       ├── events.jsonl               # Filtered by trace_id
│       ├── metadata.json              # Completion metadata
│       ├── test-report.json
│       ├── coverage-report.json
│       ├── pr-link.txt
│       └── release-notes-fragment.md
│
├── coordination/                       # Cross-repo infrastructure
│   ├── README.md
│   ├── events.jsonl                   # Centralized event log
│   ├── ECOSYSTEM_STATUS.yaml          # Live dashboard
│   └── CAPABILITIES/                  # Capability registry
│       ├── README.md
│       ├── chora-base.yaml
│       └── ecosystem-manifest.yaml.template
│
├── schemas/                            # JSON schemas
│   ├── strategic-proposal.schema.json
│   ├── coordination-request.schema.json
│   └── implementation-task.schema.json
│
├── INBOX_PROTOCOL.md                  # This document
├── INTAKE_TRIAGE_GUIDE.md             # Decision criteria
└── CLAUDE.md                          # Claude Code patterns for inbox
```

---

## Workflow by Type

### Type 1: Strategic Proposal → Vision & Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CREATE PROPOSAL                                          │
│ Location: inbox/ecosystem/proposals/prop-NNN.md             │
│                                                              │
│ Format: Markdown with frontmatter                           │
│ Required: summary, problem, solution, impact, metrics       │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. QUARTERLY REVIEW (Phase 1: Vision & Strategy)           │
│ When: Quarterly planning sessions                           │
│ Who: Leadership + Team                                       │
│                                                              │
│ Questions:                                                   │
│ - Aligns with vision?                                        │
│ - Ecosystem implications?                                    │
│ - Have capacity?                                             │
│ - What's ROI?                                                │
│                                                              │
│ Decision: Accept | Defer | Reject | Research                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ↓            ↓            ↓
    ACCEPT      DEFER      REJECT
        │            │            │
        │            ↓            ↓
        │    deferred/    deferred/
        │                 (with rationale)
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. IF ACCEPTED: MOVE TO RFC                                 │
│ Location: inbox/ecosystem/rfcs/NNNN-title.md                │
│                                                              │
│ Activities:                                                  │
│ - Detailed design                                            │
│ - Collect feedback                                           │
│ - Iterate until consensus                                    │
│ - Final comment period                                       │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. RFC ACCEPTED: CREATE ADR                                 │
│ Location: inbox/ecosystem/adrs/NNNN-title.md                │
│                                                              │
│ Activities:                                                  │
│ - Document decision                                          │
│ - Record rationale                                           │
│ - List consequences                                          │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. GENERATE COORDINATION REQUESTS                           │
│ Location: inbox/incoming/coordination/coord-NNN.json        │
│                                                              │
│ Activities:                                                  │
│ - Break RFC into repo-specific work                         │
│ - Create coordination request per dependency                │
│ - Link to original RFC                                       │
│ - Schedule for sprint planning                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Type 2: Coordination Request → Planning & Prioritization

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CREATE COORDINATION REQUEST                              │
│ Location: inbox/incoming/coordination/coord-NNN.json        │
│                                                              │
│ Format: JSON following schema                               │
│ Required: from/to repos, deliverables, acceptance_criteria  │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. EMIT EVENT                                               │
│ Location: inbox/coordination/events.jsonl                   │
│                                                              │
│ Event: coordination_request_created                         │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. SPRINT PLANNING (Phase 2: Planning & Prioritization)    │
│ When: Every 2 weeks                                          │
│ Who: Product + Engineering Leads                             │
│                                                              │
│ Questions:                                                   │
│ - In current roadmap?                                        │
│ - Urgency? (blocks other work?)                             │
│ - Have capacity this sprint?                                │
│ - Dependencies met?                                          │
│                                                              │
│ Decision: This Sprint | Next Sprint | Backlog | Reject      │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ↓            ↓            ↓
   THIS SPRINT   NEXT SPRINT  REJECT
        │            │            │
        │            ↓            ↓
        │     (stays in       rejected/
        │      incoming/)
        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. IF THIS SPRINT: MOVE TO ACTIVE                          │
│ Location: inbox/active/coord-NNN-title/                     │
│                                                              │
│ Activities:                                                  │
│ - Create directory                                           │
│ - Move coordination.json                                     │
│ - Update sprint intent document                             │
│ - Notify requesting repo                                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. PHASE 3: DDD (Requirements & Design)                    │
│ Create: change-request.md (Diátaxis format)                 │
│                                                              │
│ YOUR EXISTING WORKFLOW →                                     │
└─────────────────────────────────────────────────────────────┘
```

---

### Type 3: Implementation Task → Design Through Release

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CREATE TASK                                              │
│ Location: inbox/incoming/tasks/task-NNN.json                │
│                                                              │
│ Format: JSON following schema                               │
│ Required: deliverables, acceptance_criteria, sprint         │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. QUICK TRIAGE                                             │
│ ✅ In current sprint?                                        │
│ ✅ Dependencies met?                                         │
│ ✅ Assignee available?                                       │
│                                                              │
│ If yes → Move to active/                                     │
│ If no → Wait until ready                                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓ IF READY
┌─────────────────────────────────────────────────────────────┐
│ 3. MOVE TO ACTIVE                                           │
│ Location: inbox/active/task-NNN-title/                      │
│                                                              │
│ mkdir inbox/active/task-NNN-title/                          │
│ mv task.json to active/task-NNN-title/                      │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. YOUR EXISTING DEVELOPMENT PROCESS                        │
│                                                              │
│ Phase 3: DDD (Requirements & Design)                        │
│ - Create change-request.md (Diátaxis format)                │
│ - Explanation, How-to, Reference                            │
│ - Extract acceptance criteria                               │
│                                                              │
│ Phase 4: BDD + TDD (Development)                            │
│ - Write Gherkin scenarios (BDD)                             │
│ - RED-GREEN-REFACTOR (TDD)                                  │
│ - Implementation                                             │
│                                                              │
│ Phase 5-7: Testing, Review, Release                         │
│ - Tests ≥85% coverage                                        │
│ - Code review                                                │
│ - CI/CD pipeline                                             │
│ - Merge & release                                            │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. MOVE TO COMPLETED                                        │
│ Location: inbox/completed/task-NNN-title/                   │
│                                                              │
│ Include:                                                     │
│ - task.json, change-request.md                              │
│ - events.jsonl (filtered by trace_id)                       │
│ - metadata.json (durations, metrics)                        │
│ - test-report.json, coverage-report.json                    │
│ - pr-link.txt, release-notes-fragment.md                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Triage Process

### Strategic Proposal Triage (Quarterly)

**Who:** Leadership + Team
**When:** Quarterly planning sessions
**Duration:** 2-4 hours

**Process:**
1. Review all proposals in `inbox/ecosystem/proposals/`
2. For each proposal, ask:
   - Does this align with our vision?
   - What are the ecosystem implications?
   - Do we have capacity?
   - What's the ROI?
   - What are the risks?

3. Decision:
   - **Accept** → Move to `inbox/ecosystem/rfcs/`, update ROADMAP.md
   - **Defer** → Move to `inbox/ecosystem/deferred/`, set next_review date
   - **Reject** → Move to `inbox/ecosystem/deferred/`, document rationale
   - **Research** → Create research task, defer decision

4. For accepted proposals:
   - Create RFC with detailed design
   - Assign discussion owner
   - Set FCP (final comment period) deadline

**Output:**
- Updated ROADMAP.md
- RFCs for accepted proposals
- Rationale for deferred/rejected

---

### Coordination Request Triage (Sprint Planning)

**Who:** Product + Engineering Leads
**When:** Every 2 weeks (sprint planning)
**Duration:** 1-2 hours

**Process:**
1. Review all requests in `inbox/incoming/coordination/`
2. For each request, ask:
   - Is this in current roadmap?
   - What's the urgency? (blocks other work?)
   - Do we have capacity this sprint?
   - Are dependencies met?

3. Check capabilities:
   ```bash
   # Can we handle this?
   yq '.capabilities.can_receive[] | select(.type == "coordination")' \
     inbox/coordination/CAPABILITIES/$(repo-name).yaml
   ```

4. Decision:
   - **This Sprint** → Move to `inbox/active/`, add to sprint backlog
   - **Next Sprint** → Keep in `inbox/incoming/coordination/`, add priority
   - **Backlog** → Keep in `inbox/incoming/coordination/`, lower priority
   - **Reject** → Move to rejected/, notify requesting repo

5. For accepted (this sprint):
   - Move coordination.json to `inbox/active/coord-NNN-title/`
   - Update sprint intent document
   - Create initial change-request.md (Phase 3: DDD)
   - Emit `coordination_request_accepted` event
   - Notify requesting repo

**Output:**
- Updated sprint backlog
- Active work in `inbox/active/`
- Notifications sent

---

### Implementation Task Triage (Continuous)

**Who:** Individual engineers
**When:** As tasks are approved
**Duration:** 5-10 minutes per task

**Process:**
1. Quick check:
   - ✅ In current sprint? (Check sprint intent doc)
   - ✅ Dependencies met?
   - ✅ Assignee available?

2. If ready:
   - Move to `inbox/active/task-NNN-title/`
   - Begin Phase 3: DDD

3. If not ready:
   - Keep in `inbox/incoming/tasks/`
   - Update status with blocker

**Output:**
- Task moved to active (if ready)
- Or task stays in incoming with updated status

---

## Event Correlation

### CHORA_TRACE_ID Pattern

Following chora-compose, use `CHORA_TRACE_ID` environment variable for cross-repo traceability:

```bash
# Set trace ID for entire workflow
export CHORA_TRACE_ID="ecosystem-w3-health-monitoring"

# All events emitted with this trace_id
# Makes filtering easy later
```

### Event Log Format

**File:** `inbox/coordination/events.jsonl`
**Format:** JSONL (JSON Lines) - one JSON object per line, append-only

**Required Fields:**
- `event_type` - Type of event
- `trace_id` - Correlation ID (CHORA_TRACE_ID)
- `timestamp` - ISO 8601 format
- `repo` - Which repository emitted event

**Common Event Types:**
- `coordination_request_created`
- `coordination_request_accepted`
- `coordination_request_fulfilled`
- `task_started`
- `task_completed`
- `phase_started`
- `phase_completed`
- `waypoint_started`
- `waypoint_completed`

**Example:**
```jsonl
{"event_type": "coordination_request_created", "request_id": "coord-001", "from_repo": "mcp-orchestration", "to_repo": "ecosystem-manifest", "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T09:00:00Z", "repo": "chora-base"}
{"event_type": "task_started", "task_id": "task-001", "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T09:15:00Z", "repo": "ecosystem-manifest"}
{"event_type": "task_completed", "task_id": "task-001", "duration_hours": 6.5, "trace_id": "ecosystem-w3-001", "timestamp": "2025-10-27T15:30:00Z", "repo": "ecosystem-manifest"}
```

### Event Emission

**During Task Lifecycle:**
```bash
# Task started
echo '{"event_type": "task_started", "task_id": "task-001", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
  >> inbox/coordination/events.jsonl

# Phase completed
echo '{"event_type": "phase_completed", "phase": "ddd", "duration_hours": 2.0, "task_id": "task-001", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
  >> inbox/coordination/events.jsonl

# Task completed
echo '{"event_type": "task_completed", "task_id": "task-001", "duration_hours": 6.5, "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "ecosystem-manifest"}' \
  >> inbox/coordination/events.jsonl
```

### Event Filtering

**Filter by trace ID:**
```bash
grep '"trace_id": "ecosystem-w3-001"' inbox/coordination/events.jsonl
```

**Filter by repo:**
```bash
grep '"repo": "ecosystem-manifest"' inbox/coordination/events.jsonl
```

**Extract for completed task:**
```bash
grep '"trace_id": "task-001-trace"' inbox/coordination/events.jsonl \
  > inbox/completed/task-001/events.jsonl
```

---

## Capability-Based Routing

### How It Works

1. **Repos declare capabilities** in `inbox/coordination/CAPABILITIES/{repo}.yaml`
2. **Tasks specify requirements** in JSON config
3. **Routing logic matches** task to capable repo

### Checking Capabilities

**Before creating coordination request:**
```bash
# Check if ecosystem-manifest can handle "update_health_spec"
yq '.capabilities.can_receive[] |
    select(.type == "coordination") |
    .category[] |
    select(. == "update_health_spec")' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

# If found → create coordination request
# If not found → wrong repo, or capability doesn't exist yet
```

**Verify dependencies:**
```bash
# Does ecosystem-manifest require chora-base?
yq '.consumes[] | select(.repo == "chora-base")' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

# Check version constraint
yq '.consumes[] | select(.repo == "chora-base") | .version' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml
```

### Example Routing Decision

**Scenario:** Need to add health endpoint template

**Question:** Which repo should handle this?

```bash
# Find who provides "mcp_server_template"
for file in inbox/coordination/CAPABILITIES/*.yaml; do
  repo=$(yq '.repo' "$file")
  provides=$(yq '.provides[] | select(.id == "mcp_server_template") | .repo' "$file")
  if [[ -n "$provides" ]]; then
    echo "Found: $repo provides mcp_server_template"
  fi
done

# Output: chora-base provides mcp_server_template

# Verify chora-base can handle task type
yq '.capabilities.can_receive[] | select(.type == "task")' \
  inbox/coordination/CAPABILITIES/chora-base.yaml

# Create task in chora-base
```

---

## Integration with Development Process

### Phase Mapping

| Inbox Phase | Development Phase | Activities |
|-------------|-------------------|------------|
| **Type 1 Intake** | Phase 1: Vision & Strategy | Quarterly review → RFC → ADR |
| **Type 2 Intake** | Phase 2: Planning & Prioritization | Sprint planning → Backlog |
| **Type 3 Intake** | Phase 3: Requirements & Design | DDD (Diátaxis change request) |
| **Active Work** | Phase 4: Development | BDD (scenarios) + TDD (tests) |
| **Active Work** | Phase 5-6: Testing & Review | Coverage, review, CI/CD |
| **Completed** | Phase 7: Release | Version, changelog, publish |
| **Completed** | Phase 8: Monitoring | Metrics, feedback |

### No Changes to Core Process

**Your existing development workflow (Phase 3-7) remains unchanged:**

1. **DDD** (Documentation Driven Design)
   - Create Diátaxis change request
   - Explanation, How-to, Reference
   - Extract acceptance criteria

2. **BDD** (Behavior Driven Development)
   - Write Gherkin scenarios
   - Implement step definitions
   - Run scenarios (RED)

3. **TDD** (Test Driven Development)
   - RED-GREEN-REFACTOR cycles
   - Implementation
   - Tests ≥85% coverage

4. **Review & Integration**
   - Code review
   - CI/CD pipeline
   - Merge to main

5. **Release**
   - Version bump
   - Changelog
   - Publish

**Inbox adds:**
- **Coordination layer** for Phases 1-2
- **Event logging** throughout
- **Cross-repo notifications**
- **Completion archiving**

---

## Tools & Automation

### Manual Tools (Current)

**Create coordination request:**
```bash
cat > inbox/incoming/coordination/coord-NNN.json <<EOF
{
  "type": "coordination",
  "request_id": "coord-NNN",
  "title": "...",
  ...
}
EOF

git add inbox/incoming/coordination/coord-NNN.json
git commit -m "feat(inbox): Add coordination request coord-NNN"
```

**Emit event:**
```bash
echo '{"event_type": "...", "trace_id": "...", "timestamp": "'$(date -Iseconds)'", "repo": "..."}' \
  >> inbox/coordination/events.jsonl
```

**Check capabilities:**
```bash
yq '.capabilities.can_receive[]' \
  inbox/coordination/CAPABILITIES/repo-name.yaml
```

### Future Automation

**Possible enhancements:**
1. **CLI tool** for creating tasks/coordination requests
2. **GitHub Actions** for event emission
3. **Dashboard web UI** for ECOSYSTEM_STATUS.yaml
4. **Validation hooks** for JSON schemas
5. **Auto-notification** when work completes

---

## Examples

### Example 1: Health Monitoring W3 (Multi-Repo Feature)

See: [inbox/examples/health-monitoring-w3/](examples/health-monitoring-w3/) (to be created)

**Scenario:** Implement Waypoint W3 (Health Monitoring & Auto-Recovery) across 4 repos.

**Steps:**
1. **Strategic Proposal** → `inbox/ecosystem/proposals/prop-001-health-monitoring.md`
2. **Quarterly Review** → Accepted
3. **RFC Created** → `inbox/ecosystem/rfcs/0001-health-monitoring.md`
4. **RFC Accepted** → Move to ADR
5. **ADR Documented** → `inbox/ecosystem/adrs/0001-health-check-format.md`
6. **Generate Coordination Requests:**
   - coord-001: ecosystem-manifest delivers health spec v1.1 → mcp-orchestration
   - coord-002: chora-base delivers health endpoint template → ecosystem-manifest
7. **Sprint Planning** → Coord requests accepted for Week 9-10, 11-12
8. **Implementation Tasks Created** → task-001, task-002, task-003, task-004
9. **Development** → DDD → BDD → TDD for each task
10. **Completion** → All tasks delivered, W3 validated

---

### Example 2: Simple Bug Fix (Single Repo)

**Scenario:** Fix mypy error in health endpoint

**Steps:**
1. **Create Task** → `inbox/incoming/tasks/task-042.json`
   ```json
   {
     "type": "task",
     "task_id": "task-042",
     "title": "Fix mypy error in health endpoint",
     "sprint": "Week 10",
     "priority": "P1",
     "category": "bug",
     "repo": "chora-base",
     "estimated_effort": "1-2 hours",
     "deliverables": ["Fixed mypy error in src/health.py"],
     "acceptance_criteria": ["mypy passes with 0 errors"]
   }
   ```

2. **Quick Triage** → Ready (in current sprint, deps met)
3. **Move to Active** → `inbox/active/task-042-mypy-fix/`
4. **Implementation** → Fix, test, commit
5. **Move to Completed** → `inbox/completed/task-042-mypy-fix/`

Total time: 1-2 hours

---

## Questions & Support

**Documentation:**
- [INTAKE_TRIAGE_GUIDE.md](INTAKE_TRIAGE_GUIDE.md) - Decision criteria
- [CLAUDE.md](CLAUDE.md) - Claude Code patterns for inbox management
- [Directory READMEs](.) - Detailed guidance for each directory

**Examples:**
- [Health Monitoring W3](examples/health-monitoring-w3/) (to be created)
- [Existing strategic docs](ecosystem/) - See multi-repo-capability-evolution-to-w3.md

**Contact:**
- GitHub Issues: https://github.com/liminalcommons/chora-base/issues
- Slack: #ecosystem-dev

---

**Version:** 1.0.0
**Last Updated:** 2025-10-27
**Maintainer:** Ecosystem Coordination Team
