# SAP-015 Backlog Organization Enhancement Plan

**Plan ID**: PLAN-2025-11-05-SAP-015-BACKLOG-ORG
**SAP**: SAP-015 (Task Tracking with Beads)
**Version**: 1.1.0 (from 1.0.0)
**Priority**: P3 (Operations)
**Estimated Effort**: 6-10 hours
**Dependencies**: Soft dependency on SAP-006 (vision cascade pattern)
**Created**: 2025-11-05
**Status**: Draft

---

## 1. Executive Summary

This plan enhances **SAP-015 (Task Tracking with Beads)** to add backlog organization patterns that enable teams to manage multi-tier work backlogs effectively across multiple timeframes (NOW → NEXT → LATER → SOMEDAY → BACKLOG).

**Core Problem**: Beads currently provides task tracking primitives (create, update, dependencies, status) but lacks guidance on backlog organization patterns: How should teams prioritize work? How should vision cascade into epics and tasks? How should backlogs be refined quarterly? How should backlog health be monitored?

**Solution**: Add 5 backlog organization patterns to SAP-015:
1. **Multi-Tier Priority Pattern (P0-P4)**: Five-tier priority system aligned with timeframes
2. **Vision Cascade Pattern**: Automated workflow for converting vision Wave 1 into beads epics/tasks
3. **Backlog Refinement Workflow**: Quarterly grooming process for backlog health
4. **Epic Decomposition Template**: Structured breakdown from roadmap milestones to executable tasks
5. **Backlog Health Queries**: CLI queries for detecting stale tasks, orphan tasks, epic progress

**Why This Matters**: This enhancement closes the gap between strategic vision (SAP-006) and operational execution (SAP-015), enabling teams to systematically cascade strategic plans into actionable backlogs while maintaining backlog health.

**Deliverables**:
1. Awareness Guide Backlog Organization Patterns (5 patterns)
2. Protocol Spec Section 3.4 (Backlog Refinement Workflow)
3. Backlog Refinement Template
4. Ledger Update (version 1.1.0)

**Integration**:
- **← SAP-006 (Development Lifecycle)**: Receives vision Wave 1 cascade (Phase 1.4)
- **← SAP-010 (Memory System)**: Links roadmap milestone notes to beads epics
- **→ SAP-027 (Dogfooding Patterns)**: GO pilot decisions create beads epics

**Success Criteria**:
- Teams can cascade vision Wave 1 into prioritized backlog in <30 minutes
- Backlog health queries detect issues (stale tasks, orphan tasks) in <5 seconds
- Quarterly refinement workflow reduces P3/P4 backlog by ≥20% per quarter

---

## 2. Current State

### 2.1 Artifact Completeness

All 5 SAP-015 artifacts exist and are complete:

| Artifact | Status | Location | Size |
|----------|--------|----------|------|
| Capability Charter | ✅ Complete | `docs/skilled-awareness/task-tracking/capability-charter.md` | 34 KB |
| Protocol Spec | ✅ Complete | `docs/skilled-awareness/task-tracking/protocol-spec.md` | 89 KB |
| Awareness Guide | ✅ Complete | `docs/skilled-awareness/task-tracking/awareness-guide.md` | 45 KB |
| Adoption Blueprint | ✅ Complete | `docs/skilled-awareness/task-tracking/adoption-blueprint.md` | 23 KB |
| Ledger | ✅ Complete | `docs/skilled-awareness/task-tracking/ledger.md` | 24 KB |

**Current Version**: 1.0.0

### 2.2 Current Capabilities

SAP-015 currently provides:

1. **Git-Backed Persistence**: `.beads/issues.jsonl` (source of truth), `.beads/beads.db` (SQLite cache)
2. **Task Lifecycle**: Create, update, assign, status transitions (open → in_progress → closed)
3. **Dependency Management**: `blocks`, `blocked_by`, `related_to` relationships
4. **Task Types**: `task`, `epic`, `bug`, `feature`, `chore`, `spike`
5. **CLI Operations**: `bd create`, `bd update`, `bd show`, `bd list`, `bd ready`, `bd dep add`
6. **Query Filters**: `--status`, `--priority`, `--assignee`, `--type`, `--tag`
7. **Git Integration**: Git hooks auto-sync `.beads/beads.db` on checkout/merge

### 2.3 Gaps in Backlog Organization

**Gap 1: No Backlog Priority Guidance**
- **Current**: Priority is optional integer (default 3)
- **Missing**: No semantic meaning for priority tiers (P0 vs P1 vs P2 vs P3 vs P4)
- **Impact**: Teams don't know how to prioritize work consistently

**Gap 2: No Vision → Backlog Cascade Workflow**
- **Current**: Protocol spec mentions vision → beads integration (Section 3.1) but no step-by-step workflow
- **Missing**: How to convert vision Wave 1 themes into beads epics and tasks
- **Impact**: Strategic vision doesn't cascade into operational backlog

**Gap 3: No Backlog Refinement Process**
- **Current**: No guidance on backlog grooming or refinement
- **Missing**: Quarterly refinement workflow for pruning stale tasks, promoting exploratory work, archiving low-priority items
- **Impact**: Backlog entropy (stale tasks accumulate, priorities drift, orphan tasks)

**Gap 4: No Epic Decomposition Template**
- **Current**: Epic type exists but no guidance on decomposition
- **Missing**: Template for breaking roadmap milestones into epics, breaking epics into tasks, estimating effort
- **Impact**: Teams struggle to decompose large initiatives into executable work

**Gap 5: No Backlog Health Monitoring**
- **Current**: Basic queries (`bd list --status open`)
- **Missing**: Health queries for stale tasks (>90 days), orphan tasks (no epic), epic progress (% tasks complete)
- **Impact**: Backlog health degrades invisibly

---

## 3. Enhancement Overview

### 3.1 Backlog Organization Patterns (5 Patterns)

We will add 5 patterns to the Awareness Guide:

**Pattern 1: Multi-Tier Priority (P0-P4)**
- **Purpose**: Align priority tiers with timeframes (NOW → NEXT → LATER → SOMEDAY → BACKLOG)
- **Semantic Meaning**:
  - **P0 (NOW)**: Current sprint, complete this week, blocks critical path
  - **P1 (NEXT)**: Next 1-2 sprints, decomposed and estimated, roadmap committed
  - **P2 (LATER)**: Roadmap committed (3-6 months), not yet scheduled
  - **P3 (SOMEDAY)**: Exploratory (6-12 months), vision Wave 2+, dogfooding candidates
  - **P4 (BACKLOG)**: Low priority, may never do, keep for historical context
- **Usage**: Set priority explicitly when creating tasks: `bd create --priority 1 "Task"`

**Pattern 2: Vision Cascade (Wave 1 → Beads)**
- **Purpose**: Convert vision Wave 1 themes into beads epics and tasks
- **Integration**: Triggered by SAP-006 Phase 1.4 (Backlog Cascade)
- **Workflow**:
  1. Read vision Wave 1 themes from vision document (SAP-010)
  2. Create beads epic per theme: `bd create --type epic --priority 1 "Wave 1: {Theme}"`
  3. Decompose epic into tasks (see Pattern 4)
  4. Add traceability metadata: `--metadata '{"from_vision_wave": 1, "roadmap_version": "v1.5.0"}'`
- **Output**: P1/P2 backlog populated with roadmap-committed work

**Pattern 3: Backlog Refinement (Quarterly)**
- **Purpose**: Maintain backlog health via quarterly grooming
- **Cadence**: Once per quarter (aligned with roadmap cycles)
- **Activities**:
  1. **Stale Task Review**: Find tasks >90 days old, archive or close
  2. **Priority Demotion**: Demote P1 → P2, P2 → P3 if not executed this quarter
  3. **Priority Promotion**: Promote P3 → P2 if dogfooding pilot succeeds (SAP-027 GO decision)
  4. **Backlog Archival**: Close P4 tasks with `--reason "deprioritized"`
  5. **Epic Progress Review**: Close epics with 100% tasks complete
- **Output**: Backlog health metrics (stale tasks reduced, priority distribution updated)

**Pattern 4: Epic Decomposition Template**
- **Purpose**: Standardized breakdown from roadmap milestone → epic → tasks
- **Template**:
  ```markdown
  ## Epic: {Theme} (v{Version})

  **From**: Roadmap Milestone {ID} (SAP-010 knowledge note)
  **Target Version**: v{Version}
  **Priority**: P1 (NEXT)
  **Effort**: {Total Hours}

  ### Tasks (Priority 2):
  - [ ] Task 1: {Description} ({Effort Hours})
  - [ ] Task 2: {Description} ({Effort Hours})
  - ...

  ### Dependencies:
  - Epic blocks Task 1: `bd dep add {epic-id} blocks {task-1-id}`
  - Task 1 blocks Task 2: `bd dep add {task-1-id} blocks {task-2-id}`

  ### Traceability:
  - Vision Document: `vision-{project}-{horizon}.md`
  - Vision Wave: 1
  - Roadmap Milestone: `roadmap-{project}-v{version}.md`
  ```
- **Usage**: Copy template, fill in blanks, create epic + tasks via CLI

**Pattern 5: Backlog Health Queries**
- **Purpose**: Detect backlog issues via CLI queries
- **Queries**:
  ```bash
  # Stale tasks (>90 days old, still open)
  bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json

  # Orphan tasks (no epic dependency)
  bd list --status open --type task --no-blockers --json

  # Epic progress (% tasks complete)
  bd show {epic-id} --json | jq '.dependencies.blocks | length' # total tasks
  bd list --status closed --blocked-by {epic-id} --json | jq 'length' # complete tasks

  # Priority distribution (count by P0-P4)
  bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'

  # High-priority staleness (P0/P1 tasks >30 days old)
  bd list --status open --priority 0,1 --created-before $(date -v-30d +%Y-%m-%d) --json
  ```
- **Usage**: Run queries during backlog refinement, create cleanup tasks for issues

### 3.2 Protocol Spec Section 3.4: Backlog Refinement Workflow

Add new Section 3.4 to `protocol-spec.md` documenting the quarterly backlog refinement workflow.

**Section Outline**:
```markdown
### 3.4: Backlog Refinement Workflow

**Cadence**: Once per quarter (aligned with roadmap cycles)
**Duration**: 2-4 hours
**Owner**: Product/Engineering lead

#### 3.4.1: Stale Task Review

**Query**:
```bash
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

**Actions**:
- Close tasks with `--reason "stale"` if no longer relevant
- Update tasks with context if still relevant
- Promote to P0/P1 if newly urgent

#### 3.4.2: Priority Adjustment

**Query**:
```bash
bd list --status open --priority 1 --json  # Review all P1 (NEXT)
bd list --status open --priority 2 --json  # Review all P2 (LATER)
```

**Actions**:
- **Demote P1 → P2**: If not executed this quarter, demote to LATER
- **Demote P2 → P3**: If not scheduled, demote to SOMEDAY
- **Promote P3 → P2**: If dogfooding pilot succeeds (SAP-027 GO), promote to LATER

#### 3.4.3: Backlog Archival

**Query**:
```bash
bd list --status open --priority 4 --json  # Review all P4 (BACKLOG)
```

**Actions**:
- Close P4 tasks with `--reason "deprioritized"` if >6 months old
- Keep P4 tasks if historical context valuable

#### 3.4.4: Epic Progress Review

**Query**:
```bash
bd list --type epic --status open --json
```

**Actions**:
- For each epic, calculate % tasks complete
- Close epic if 100% tasks complete
- Update epic description with progress metrics

#### 3.4.5: Backlog Health Metrics

**Output**: Log refinement results to A-MEM (SAP-010)

```bash
# Log to .chora/memory/events/backlog-refinement.jsonl
{
  "timestamp": "2025-11-05T00:00:00Z",
  "event": "backlog_refinement_complete",
  "quarter": "2025-Q4",
  "metrics": {
    "stale_tasks_closed": 12,
    "priority_demotions": 8,
    "priority_promotions": 3,
    "backlog_archived": 15,
    "epics_closed": 2
  },
  "backlog_snapshot": {
    "p0": 5,
    "p1": 18,
    "p2": 32,
    "p3": 47,
    "p4": 21
  }
}
```
```

### 3.3 Backlog Refinement Template

Create a template file for teams to copy during quarterly refinement:

**File**: `.chora/memory/templates/backlog-refinement-template.md`

**Content**:
```markdown
---
id: backlog-refinement-{quarter}
type: backlog-refinement
quarter: {YYYY-QQ}
status: draft | complete
date: {YYYY-MM-DD}
tags: [backlog, refinement, quarterly]
created: {ISO-8601}
updated: {ISO-8601}
---

# Backlog Refinement: {Quarter}

**Date**: {YYYY-MM-DD}
**Facilitator**: {Name}
**Participants**: {Names}
**Duration**: {Hours}

---

## 1. Stale Task Review (>90 days)

**Query**:
```bash
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

**Tasks Reviewed**: {Count}
**Tasks Closed**: {Count}
**Tasks Updated**: {Count}

### Closed Tasks
- {task-id}: {reason}
- ...

### Updated Tasks
- {task-id}: {update summary}
- ...

---

## 2. Priority Adjustment

### P1 (NEXT) Review
**Query**: `bd list --status open --priority 1 --json`
**Tasks Reviewed**: {Count}

**Demoted to P2 (LATER)**:
- {task-id}: {reason}
- ...

**Promoted to P0 (NOW)**:
- {task-id}: {reason}
- ...

### P2 (LATER) Review
**Query**: `bd list --status open --priority 2 --json`
**Tasks Reviewed**: {Count}

**Demoted to P3 (SOMEDAY)**:
- {task-id}: {reason}
- ...

**Promoted to P1 (NEXT)**:
- {task-id}: {reason}
- ...

### P3 (SOMEDAY) Review
**Query**: `bd list --status open --priority 3 --json`
**Tasks Reviewed**: {Count}

**Promoted to P2 (LATER)** (from dogfooding pilots):
- {task-id}: {pilot-id} GO decision
- ...

---

## 3. Backlog Archival (P4)

**Query**: `bd list --status open --priority 4 --json`
**Tasks Reviewed**: {Count}
**Tasks Closed**: {Count}

### Closed Tasks
- {task-id}: {reason}
- ...

---

## 4. Epic Progress Review

**Query**: `bd list --type epic --status open --json`
**Epics Reviewed**: {Count}

| Epic ID | Name | Tasks Total | Tasks Complete | Progress | Action |
|---------|------|-------------|----------------|----------|--------|
| {id}    | {name} | {total} | {complete} | {%} | Close / Continue |

**Epics Closed**:
- {epic-id}: 100% complete
- ...

---

## 5. Backlog Health Metrics

### Before Refinement
- P0 (NOW): {count}
- P1 (NEXT): {count}
- P2 (LATER): {count}
- P3 (SOMEDAY): {count}
- P4 (BACKLOG): {count}
- **Total Open**: {count}

### After Refinement
- P0 (NOW): {count} ({delta})
- P1 (NEXT): {count} ({delta})
- P2 (LATER): {count} ({delta})
- P3 (SOMEDAY): {count} ({delta})
- P4 (BACKLOG): {count} ({delta})
- **Total Open**: {count} ({delta})

### Actions Taken
- Stale tasks closed: {count}
- Priority demotions: {count}
- Priority promotions: {count}
- Backlog archived: {count}
- Epics closed: {count}

---

## 6. Next Steps

**Immediate Actions**:
- [ ] Log refinement to A-MEM: `.chora/memory/events/backlog-refinement.jsonl`
- [ ] Update ROADMAP.md with next quarter priorities
- [ ] Schedule next refinement: {next-quarter-date}

**Follow-up Tasks**:
- [ ] {task-id}: {description}
- ...

---

## 7. Notes

{Any observations, patterns, or lessons learned}
```

### 3.4 Ledger Update

Update `ledger.md` to version 1.1.0 with backlog organization enhancements.

**Version Entry**:
```markdown
## Version 1.1.0 (2025-11-05)

**Status**: Draft → Pilot
**Focus**: Backlog Organization Patterns

### Enhancements
1. **Multi-Tier Priority Pattern (P0-P4)**: Added semantic meaning for priority tiers aligned with timeframes (NOW → NEXT → LATER → SOMEDAY → BACKLOG)
2. **Vision Cascade Pattern**: Documented workflow for converting vision Wave 1 into beads epics/tasks (integration with SAP-006)
3. **Backlog Refinement Workflow**: Added quarterly grooming process (Section 3.4 in protocol-spec)
4. **Epic Decomposition Template**: Standardized breakdown from roadmap milestone → epic → tasks
5. **Backlog Health Queries**: Added 5 CLI queries for detecting stale tasks, orphan tasks, epic progress

### Artifacts Updated
- **Awareness Guide**: Added Backlog Organization Patterns section (5 patterns, ~12 pages)
- **Protocol Spec**: Added Section 3.4 (Backlog Refinement Workflow, ~8 pages)
- **Templates**: Added backlog-refinement-template.md

### Integration
- **SAP-006 (Development Lifecycle)**: Receives vision Wave 1 cascade (Phase 1.4)
- **SAP-010 (Memory System)**: Links roadmap milestone notes, logs refinement metrics to A-MEM
- **SAP-027 (Dogfooding Patterns)**: GO pilot decisions trigger priority promotion (P3 → P2)

### Dogfooding Plan
- **Project**: chora-base
- **Timeline**: 2025-Q4 (3 months)
- **Activities**:
  1. Cascade chora-base vision Wave 1 into beads backlog
  2. Run quarterly refinement (end of Q4)
  3. Track backlog health metrics (stale tasks, priority distribution)
  4. Validate epic decomposition template (3+ epics)
- **Success Criteria**:
  - Vision cascade completes in <30 minutes
  - Backlog health queries detect issues in <5 seconds
  - Quarterly refinement reduces P3/P4 backlog by ≥20%
```

---

## 4. Detailed Deliverables

### Deliverable 1: Awareness Guide Backlog Organization Patterns

**File**: `docs/skilled-awareness/task-tracking/awareness-guide.md`

**Section to Add**: "Backlog Organization Patterns" (after existing Section 3)

**Content** (5 patterns, ~12 pages):

```markdown
## 4. Backlog Organization Patterns

This section provides 5 backlog organization patterns for managing multi-tier work backlogs effectively.

### 4.1: Multi-Tier Priority Pattern (P0-P4)

**Problem**: Teams struggle to prioritize work consistently across timeframes (this week vs next quarter vs next year).

**Solution**: Use semantic priority tiers aligned with timeframes.

#### Priority Tier Definitions

| Tier | Name | Timeframe | Criteria | Example |
|------|------|-----------|----------|---------|
| **P0** | NOW | This week | Blocks critical path, current sprint, urgent bugs | "Fix production outage" |
| **P1** | NEXT | 1-2 sprints | Roadmap committed, decomposed, estimated | "Implement auth feature (v1.5)" |
| **P2** | LATER | 3-6 months | Roadmap committed, not yet scheduled | "Add GraphQL API (v2.0)" |
| **P3** | SOMEDAY | 6-12 months | Exploratory, vision Wave 2+, dogfooding candidates | "Evaluate Rust rewrite" |
| **P4** | BACKLOG | Indefinite | Low priority, may never do, historical context | "Support IE11" |

#### Usage

**Creating Tasks with Priority**:
```bash
# P0 (NOW): Urgent bug fix
bd create "Fix login timeout bug" --priority 0 --type bug

# P1 (NEXT): Roadmap committed feature
bd create "Implement OAuth2 flow" --priority 1 --type feature

# P2 (LATER): Scheduled for v2.0
bd create "Add GraphQL API" --priority 2 --type feature

# P3 (SOMEDAY): Exploratory, dogfooding candidate
bd create "Evaluate Rust for performance" --priority 3 --type spike

# P4 (BACKLOG): Low priority, may never do
bd create "Support IE11 browser" --priority 4 --type task
```

**Querying by Priority**:
```bash
# Show all P0 (NOW) tasks
bd list --status open --priority 0

# Show P1 (NEXT) and P2 (LATER) tasks (roadmap committed)
bd list --status open --priority 1,2

# Show P3 (SOMEDAY) + P4 (BACKLOG) (exploratory + low priority)
bd list --status open --priority 3,4
```

#### Best Practices

1. **Limit P0 (NOW) to <10 tasks**: If more than 10, promote from P1 or close stale P0
2. **Keep P1 (NEXT) decomposed**: All P1 tasks should have effort estimates and be ready to start
3. **Review P3 (SOMEDAY) quarterly**: Promote successful dogfooding pilots to P2, demote stale P3 to P4
4. **Archive P4 (BACKLOG) annually**: Close P4 tasks >1 year old with `--reason "deprioritized"`

#### Integration with Vision Waves (SAP-006)

Vision waves map to priority tiers:
- **Vision Wave 1 (Committed - 3 months)** → **P1 (NEXT)** or **P2 (LATER)**
- **Vision Wave 2 (Exploratory - 6 months)** → **P3 (SOMEDAY)**
- **Vision Wave 3 (Aspirational - 12 months)** → **P4 (BACKLOG)**

When cascading vision to backlog (SAP-006 Phase 1.4):
- Wave 1 themes become P1 epics
- Wave 1 features become P1/P2 tasks (P1 if this quarter, P2 if next quarter)

---

### 4.2: Vision Cascade Pattern (Wave 1 → Beads)

**Problem**: Strategic vision (SAP-006) doesn't cascade into operational backlog, creating gap between strategy and execution.

**Solution**: Automated workflow for converting vision Wave 1 themes into beads epics and tasks.

#### Workflow: Vision → Backlog

This pattern is triggered by **SAP-006 Phase 1.4 (Backlog Cascade)**.

**Step 1: Read Vision Wave 1**

```bash
# Query vision document (SAP-010 knowledge note)
vision_file=$(grep -l '"type": "strategic-vision"' .chora/memory/knowledge/notes/*.md | tail -1)
cat "$vision_file"
```

**Step 2: Extract Wave 1 Themes**

From vision document, extract all Wave 1 sections:
```markdown
## Wave 1: Strategic Planning Infrastructure (Committed - 3 months)
**Target Version**: v1.5.0
**Evidence**: A+B 75% (Level A: 35%, Level B: 40%)
**Themes**: 4 SAP enhancements (SAP-010, SAP-006, SAP-015, SAP-027)
...
```

**Step 3: Create Beads Epic per Theme**

```bash
# Create epic for Wave 1 theme
bd create "Wave 1: Strategic Planning Infrastructure (v1.5.0)" \
  --type epic \
  --priority 1 \
  --description "From vision-chora-base-6-month Wave 1. Enhance 4 SAPs to enable ecosystem-wide strategic planning." \
  --metadata '{
    "from_vision_wave": 1,
    "vision_document": "vision-chora-base-6-month",
    "roadmap_version": "v1.5.0",
    "target_quarter": "2025-Q4"
  }'

# Returns: chora-base-epic-abc123
```

**Step 4: Decompose Epic into Tasks**

Use Epic Decomposition Template (Pattern 4.4):

```bash
# SAP-010 tasks (P2 - LATER)
bd create "SAP-010: Create 4 strategic templates" \
  --type task \
  --priority 2 \
  --description "Vision, intention inventory, roadmap milestone, strategic theme matrix" \
  --metadata '{"effort_hours": 4, "sap": "SAP-010"}'

# SAP-006 tasks (P2 - LATER)
bd create "SAP-006: Expand Phase 1 with 4 sub-phases" \
  --type task \
  --priority 2 \
  --description "Discovery → Analysis → Vision Drafting → Backlog Cascade" \
  --metadata '{"effort_hours": 8, "sap": "SAP-006"}'

# SAP-015 tasks (P2 - LATER)
bd create "SAP-015: Add 5 backlog organization patterns" \
  --type task \
  --priority 2 \
  --description "Multi-tier priority, vision cascade, refinement, epic decomp, health queries" \
  --metadata '{"effort_hours": 6, "sap": "SAP-015"}'

# SAP-027 tasks (P2 - LATER)
bd create "SAP-027: Add Week -1 discovery phase" \
  --type task \
  --priority 2 \
  --description "Intention prioritization, pilot selection criteria, feedback loop" \
  --metadata '{"effort_hours": 4, "sap": "SAP-027"}'
```

**Step 5: Link Tasks to Epic**

```bash
# Epic blocks all tasks (tasks depend on epic)
bd dep add chora-base-epic-abc123 blocks {sap-010-task-id}
bd dep add chora-base-epic-abc123 blocks {sap-006-task-id}
bd dep add chora-base-epic-abc123 blocks {sap-015-task-id}
bd dep add chora-base-epic-abc123 blocks {sap-027-task-id}
```

**Step 6: Link Epic to Roadmap Milestone (SAP-010)**

```bash
# Create roadmap milestone note (SAP-010)
cat > .chora/memory/knowledge/notes/roadmap-chora-base-v1.5.0.md <<'EOF'
---
id: roadmap-chora-base-v1.5.0
type: roadmap-milestone
version: v1.5.0
status: in_progress
target_date: 2025-12-31
tags: [roadmap, milestone, strategic-planning]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Roadmap Milestone: chora-base v1.5.0

**Theme**: Strategic Planning Infrastructure
**From**: vision-chora-base-6-month Wave 1
**Beads Epic**: chora-base-epic-abc123
**Target Date**: 2025-12-31

## Features
1. SAP-010: Strategic knowledge templates (4 templates)
2. SAP-006: Vision synthesis workflow (4-phase)
3. SAP-015: Backlog organization patterns (5 patterns)
4. SAP-027: Pre-pilot discovery phase (Week -1)

## Success Criteria
- Vision cascade completes in <30 minutes
- Backlog health queries detect issues in <5 seconds
- Quarterly refinement reduces P3/P4 backlog by ≥20%
EOF

# Update epic with roadmap milestone link
bd update chora-base-epic-abc123 --metadata '{
  "roadmap_milestone_note": "roadmap-chora-base-v1.5.0"
}'
```

**Step 7: Verify Cascade**

```bash
# Show epic and all blocked tasks
bd show chora-base-epic-abc123 --json
bd list --blocked-by chora-base-epic-abc123 --json
```

#### Output

After cascade, backlog should have:
- 1 epic (P1 - NEXT) linked to roadmap milestone
- 4-10 tasks (P2 - LATER) blocked by epic
- Traceability metadata linking tasks → epic → roadmap → vision

---

### 4.3: Backlog Refinement Workflow (Quarterly)

**Problem**: Backlog entropy (stale tasks accumulate, priorities drift, orphan tasks).

**Solution**: Quarterly grooming process for backlog health.

#### When to Run

- **Cadence**: Once per quarter (aligned with roadmap cycles)
- **Duration**: 2-4 hours
- **Owner**: Product/Engineering lead
- **Participants**: Core team (3-5 people)

#### Workflow

Use backlog refinement template: `.chora/memory/templates/backlog-refinement-template.md`

**Step 1: Stale Task Review (>90 days)**

```bash
# Find tasks >90 days old, still open
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

**Actions**:
- **Close** tasks with `--reason "stale"` if no longer relevant
- **Update** tasks with context if still relevant
- **Promote** to P0/P1 if newly urgent

**Example**:
```bash
# Close stale task
bd close chora-base-abc --reason "Stale: No longer needed after v1.5 architecture change"

# Update stale task with context
bd update chora-base-def --description "Still relevant: Blocked on vendor API release (ETA 2026-Q1)"

# Promote stale task
bd update chora-base-ghi --priority 1  # Promote to P1 (NEXT)
```

**Step 2: Priority Adjustment**

**Review P1 (NEXT)**:
```bash
bd list --status open --priority 1 --json
```

**Actions**:
- **Demote P1 → P2**: If not executed this quarter, demote to LATER
- **Promote P2 → P1**: If newly urgent, promote to NEXT

**Example**:
```bash
# Demote P1 → P2 (not executed this quarter)
bd update chora-base-jkl --priority 2  # Demote to P2 (LATER)

# Promote P2 → P1 (newly urgent)
bd update chora-base-mno --priority 1  # Promote to P1 (NEXT)
```

**Review P2 (LATER)**:
```bash
bd list --status open --priority 2 --json
```

**Actions**:
- **Demote P2 → P3**: If not scheduled, demote to SOMEDAY
- **Promote P3 → P2**: If dogfooding pilot succeeds (SAP-027 GO), promote to LATER

**Example**:
```bash
# Demote P2 → P3 (not scheduled)
bd update chora-base-pqr --priority 3  # Demote to P3 (SOMEDAY)

# Promote P3 → P2 (dogfooding pilot GO decision)
bd update chora-base-stu --priority 2 --metadata '{
  "from_dogfooding_pilot": "pilot-sap-015-2025-q4",
  "decision": "GO"
}'
```

**Step 3: Backlog Archival (P4)**

```bash
bd list --status open --priority 4 --json
```

**Actions**:
- **Close** P4 tasks with `--reason "deprioritized"` if >6 months old
- **Keep** P4 tasks if historical context valuable

**Example**:
```bash
# Close old P4 task
bd close chora-base-vwx --reason "Deprioritized: Not executed in 6 months, no longer needed"
```

**Step 4: Epic Progress Review**

```bash
bd list --type epic --status open --json
```

**For each epic**:
1. Calculate % tasks complete
2. Close epic if 100% complete
3. Update epic description with progress

**Example**:
```bash
# Show epic and all tasks
bd show chora-base-epic-abc123 --json

# Count total tasks
total=$(bd list --blocked-by chora-base-epic-abc123 --json | jq 'length')

# Count complete tasks
complete=$(bd list --status closed --blocked-by chora-base-epic-abc123 --json | jq 'length')

# Calculate progress
progress=$((complete * 100 / total))

# Update epic description
bd update chora-base-epic-abc123 --description "Progress: $complete/$total ($progress%)"

# Close epic if 100% complete
if [ $progress -eq 100 ]; then
  bd close chora-base-epic-abc123 --reason "Epic complete: All tasks finished"
fi
```

**Step 5: Log Refinement to A-MEM (SAP-010)**

```bash
# Log to .chora/memory/events/backlog-refinement.jsonl
cat >> .chora/memory/events/backlog-refinement.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "backlog_refinement_complete",
  "quarter": "2025-Q4",
  "metrics": {
    "stale_tasks_closed": 12,
    "priority_demotions": 8,
    "priority_promotions": 3,
    "backlog_archived": 15,
    "epics_closed": 2
  },
  "backlog_snapshot": {
    "p0": 5,
    "p1": 18,
    "p2": 32,
    "p3": 47,
    "p4": 21
  }
}
EOF
```

#### Output

- Backlog health metrics logged to A-MEM
- Stale tasks closed or updated
- Priority distribution updated
- Epics closed if complete
- Backlog reduced by ≥20% (P3/P4 tasks)

---

### 4.4: Epic Decomposition Template

**Problem**: Teams struggle to decompose large initiatives (roadmap milestones) into executable work (epics, tasks).

**Solution**: Standardized template for breaking roadmap milestones into epics, breaking epics into tasks, estimating effort.

#### Template: Roadmap Milestone → Epic → Tasks

**Step 1: Read Roadmap Milestone (SAP-010)**

```bash
# Query roadmap milestone note
milestone_file=".chora/memory/knowledge/notes/roadmap-{project}-v{version}.md"
cat "$milestone_file"
```

**Step 2: Create Epic**

```bash
bd create "Epic: {Theme} (v{Version})" \
  --type epic \
  --priority 1 \
  --description "{Description from roadmap milestone}" \
  --metadata '{
    "roadmap_milestone_note": "roadmap-{project}-v{version}",
    "target_version": "v{Version}",
    "target_date": "{YYYY-MM-DD}"
  }'

# Returns: {epic-id}
```

**Step 3: Decompose Epic into Tasks**

For each feature in roadmap milestone:

```bash
bd create "{Feature Name}" \
  --type task \
  --priority 2 \
  --description "{Feature description}" \
  --metadata '{
    "effort_hours": {Hours},
    "feature": "{Feature Name}"
  }'

# Returns: {task-id}
```

**Step 4: Link Tasks to Epic**

```bash
# Epic blocks all tasks
bd dep add {epic-id} blocks {task-1-id}
bd dep add {epic-id} blocks {task-2-id}
# ...
```

**Step 5: Add Task Dependencies (if any)**

```bash
# Task 1 blocks Task 2 (Task 2 depends on Task 1)
bd dep add {task-1-id} blocks {task-2-id}
```

**Step 6: Estimate Total Epic Effort**

```bash
# Sum effort_hours from all tasks
total_effort=$(bd list --blocked-by {epic-id} --json | jq '[.[].metadata.effort_hours] | add')

# Update epic with total effort
bd update {epic-id} --metadata "{\"total_effort_hours\": $total_effort}"
```

#### Example: Epic Decomposition

**Roadmap Milestone**: chora-base v1.5.0 (Strategic Planning Infrastructure)

**Epic**:
```bash
bd create "Epic: Strategic Planning Infrastructure (v1.5.0)" \
  --type epic \
  --priority 1 \
  --description "Enable ecosystem-wide strategic planning via 4 SAP enhancements" \
  --metadata '{
    "roadmap_milestone_note": "roadmap-chora-base-v1.5.0",
    "target_version": "v1.5.0",
    "target_date": "2025-12-31"
  }'
# Returns: chora-base-epic-abc123
```

**Tasks** (4 SAP enhancements):
```bash
# SAP-010
bd create "SAP-010: Create 4 strategic templates" \
  --type task \
  --priority 2 \
  --description "Vision, intention inventory, roadmap milestone, strategic theme matrix" \
  --metadata '{"effort_hours": 4, "sap": "SAP-010"}'
# Returns: chora-base-task-def456

# SAP-006
bd create "SAP-006: Expand Phase 1 with 4 sub-phases" \
  --type task \
  --priority 2 \
  --description "Discovery → Analysis → Vision Drafting → Backlog Cascade" \
  --metadata '{"effort_hours": 8, "sap": "SAP-006"}'
# Returns: chora-base-task-ghi789

# SAP-015
bd create "SAP-015: Add 5 backlog organization patterns" \
  --type task \
  --priority 2 \
  --description "Multi-tier priority, vision cascade, refinement, epic decomp, health queries" \
  --metadata '{"effort_hours": 6, "sap": "SAP-015"}'
# Returns: chora-base-task-jkl012

# SAP-027
bd create "SAP-027: Add Week -1 discovery phase" \
  --type task \
  --priority 2 \
  --description "Intention prioritization, pilot selection criteria, feedback loop" \
  --metadata '{"effort_hours": 4, "sap": "SAP-027"}'
# Returns: chora-base-task-mno345
```

**Link Tasks to Epic**:
```bash
bd dep add chora-base-epic-abc123 blocks chora-base-task-def456
bd dep add chora-base-epic-abc123 blocks chora-base-task-ghi789
bd dep add chora-base-epic-abc123 blocks chora-base-task-jkl012
bd dep add chora-base-epic-abc123 blocks chora-base-task-mno345
```

**Estimate Total Effort**:
```bash
total_effort=$(bd list --blocked-by chora-base-epic-abc123 --json | jq '[.[].metadata.effort_hours] | add')
# Returns: 22 hours

bd update chora-base-epic-abc123 --metadata '{"total_effort_hours": 22}'
```

#### Output

- 1 epic (P1 - NEXT) linked to roadmap milestone
- 4 tasks (P2 - LATER) blocked by epic
- Total effort estimated (22 hours)
- Traceability metadata linking tasks → epic → roadmap

---

### 4.5: Backlog Health Queries

**Problem**: Backlog health degrades invisibly (stale tasks, orphan tasks, stuck epics).

**Solution**: CLI queries for detecting backlog issues.

#### Query 1: Stale Tasks (>90 days old)

```bash
# Find tasks >90 days old, still open
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

**Usage**: Run during backlog refinement (Pattern 4.3), close or update stale tasks.

---

#### Query 2: Orphan Tasks (no epic dependency)

```bash
# Find tasks with no epic (no blockers)
bd list --status open --type task --json | jq '[.[] | select(.dependencies.blocked_by | length == 0)]'
```

**Usage**: Find tasks that should be linked to epics but aren't. Add dependencies or close if no longer relevant.

---

#### Query 3: Epic Progress (% tasks complete)

```bash
# For a specific epic
epic_id="chora-base-epic-abc123"

# Total tasks
total=$(bd list --blocked-by $epic_id --json | jq 'length')

# Complete tasks
complete=$(bd list --status closed --blocked-by $epic_id --json | jq 'length')

# Progress
echo "Epic $epic_id: $complete/$total ($((complete * 100 / total))%)"
```

**Usage**: Run during backlog refinement, close epics at 100%, update epic descriptions with progress.

---

#### Query 4: Priority Distribution (count by P0-P4)

```bash
# Count open tasks by priority
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
```

**Output**:
```json
[
  {"priority": 0, "count": 5},
  {"priority": 1, "count": 18},
  {"priority": 2, "count": 32},
  {"priority": 3, "count": 47},
  {"priority": 4, "count": 21}
]
```

**Usage**: Understand backlog distribution, ensure P0 <10, P1 <30, P3+P4 <50% of total.

---

#### Query 5: High-Priority Staleness (P0/P1 >30 days old)

```bash
# Find P0/P1 tasks >30 days old
bd list --status open --priority 0,1 --created-before $(date -v-30d +%Y-%m-%d) --json
```

**Usage**: Detect stuck high-priority work. Demote to P2/P3 or unblock.

---

#### Backlog Health Dashboard

Combine all queries into a dashboard:

```bash
#!/bin/bash
# backlog-health.sh

echo "=== Backlog Health Dashboard ==="
echo ""

echo "## Priority Distribution"
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
echo ""

echo "## Stale Tasks (>90 days)"
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json | jq 'length'
echo ""

echo "## High-Priority Staleness (P0/P1 >30 days)"
bd list --status open --priority 0,1 --created-before $(date -v-30d +%Y-%m-%d) --json | jq 'length'
echo ""

echo "## Orphan Tasks (no epic)"
bd list --status open --type task --json | jq '[.[] | select(.dependencies.blocked_by | length == 0)] | length'
echo ""

echo "## Epic Progress"
bd list --type epic --status open --json | jq -r '.[] | "\(.id): \(.title)"' | while read epic; do
  epic_id=$(echo "$epic" | cut -d: -f1)
  total=$(bd list --blocked-by $epic_id --json | jq 'length')
  complete=$(bd list --status closed --blocked-by $epic_id --json | jq 'length')
  progress=$((complete * 100 / total))
  echo "$epic_id: $complete/$total ($progress%)"
done
```

**Usage**: Run monthly or during backlog refinement, create cleanup tasks for issues.

---
```

---

### Deliverable 2: Protocol Spec Section 3.4 (Backlog Refinement Workflow)

**File**: `docs/skilled-awareness/task-tracking/protocol-spec.md`

**Section to Add**: Section 3.4 after existing Section 3.3

**Content** (~8 pages):

```markdown
### 3.4: Backlog Refinement Workflow

**Cadence**: Once per quarter (aligned with roadmap cycles)
**Duration**: 2-4 hours
**Owner**: Product/Engineering lead
**Participants**: Core team (3-5 people)

#### 3.4.1: Stale Task Review

**Query**:
```bash
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

**Actions**:
- Close tasks with `--reason "stale"` if no longer relevant
- Update tasks with context if still relevant
- Promote to P0/P1 if newly urgent

**Example**:
```bash
# Close stale task
bd close chora-base-abc --reason "Stale: No longer needed after v1.5 architecture change"

# Update stale task with context
bd update chora-base-def --description "Still relevant: Blocked on vendor API release (ETA 2026-Q1)"

# Promote stale task
bd update chora-base-ghi --priority 1
```

---

#### 3.4.2: Priority Adjustment

**P1 (NEXT) Review**:
```bash
bd list --status open --priority 1 --json
```

**Actions**:
- **Demote P1 → P2**: If not executed this quarter, demote to LATER
- **Promote P2 → P1**: If newly urgent, promote to NEXT

**P2 (LATER) Review**:
```bash
bd list --status open --priority 2 --json
```

**Actions**:
- **Demote P2 → P3**: If not scheduled, demote to SOMEDAY
- **Promote P3 → P2**: If dogfooding pilot succeeds (SAP-027 GO), promote to LATER

**Example**:
```bash
# Promote P3 → P2 (dogfooding pilot GO decision)
bd update chora-base-stu --priority 2 --metadata '{
  "from_dogfooding_pilot": "pilot-sap-015-2025-q4",
  "decision": "GO"
}'
```

---

#### 3.4.3: Backlog Archival

**Query**:
```bash
bd list --status open --priority 4 --json
```

**Actions**:
- Close P4 tasks with `--reason "deprioritized"` if >6 months old
- Keep P4 tasks if historical context valuable

**Example**:
```bash
bd close chora-base-vwx --reason "Deprioritized: Not executed in 6 months, no longer needed"
```

---

#### 3.4.4: Epic Progress Review

**Query**:
```bash
bd list --type epic --status open --json
```

**For each epic**:
1. Calculate % tasks complete
2. Close epic if 100% complete
3. Update epic description with progress

**Example**:
```bash
# Show epic and all tasks
bd show chora-base-epic-abc123 --json

# Count total tasks
total=$(bd list --blocked-by chora-base-epic-abc123 --json | jq 'length')

# Count complete tasks
complete=$(bd list --status closed --blocked-by chora-base-epic-abc123 --json | jq 'length')

# Calculate progress
progress=$((complete * 100 / total))

# Update epic description
bd update chora-base-epic-abc123 --description "Progress: $complete/$total ($progress%)"

# Close epic if 100% complete
if [ $progress -eq 100 ]; then
  bd close chora-base-epic-abc123 --reason "Epic complete: All tasks finished"
fi
```

---

#### 3.4.5: Backlog Health Metrics

**Output**: Log refinement results to A-MEM (SAP-010)

```bash
# Log to .chora/memory/events/backlog-refinement.jsonl
cat >> .chora/memory/events/backlog-refinement.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "backlog_refinement_complete",
  "quarter": "2025-Q4",
  "metrics": {
    "stale_tasks_closed": 12,
    "priority_demotions": 8,
    "priority_promotions": 3,
    "backlog_archived": 15,
    "epics_closed": 2
  },
  "backlog_snapshot": {
    "p0": 5,
    "p1": 18,
    "p2": 32,
    "p3": 47,
    "p4": 21
  }
}
EOF
```

---

#### 3.4.6: Integration with Vision Waves (SAP-006)

After backlog refinement, review vision Wave 2 promotion criteria:

**Criteria for Promoting P3 (SOMEDAY) → P2 (LATER)**:
- Dogfooding pilot succeeds (SAP-027 GO decision)
- Evidence A+B ≥60% (updated after pilot)
- User demand ≥5 (validated via pilot feedback)

**Example**:
```bash
# Find P3 tasks linked to successful pilots
bd list --status open --priority 3 --json | jq '[.[] | select(.metadata.from_dogfooding_pilot != null and .metadata.decision == "GO")]'

# Promote to P2 (LATER)
bd update {task-id} --priority 2
```

---

#### 3.4.7: Backlog Refinement Template

Copy template from SAP-010:
```bash
cp .chora/memory/templates/backlog-refinement-template.md ./backlog-refinement-2025-q4.md
```

Fill in template during refinement, commit to project docs:
```bash
git add docs/project-docs/backlog-refinements/backlog-refinement-2025-q4.md
git commit -m "docs: Add backlog refinement Q4 2025"
```
```

---

### Deliverable 3: Backlog Refinement Template

**File**: `.chora/memory/templates/backlog-refinement-template.md` (create new)

**Content**: See Section 3.3 above (Backlog Refinement Template)

---

### Deliverable 4: Ledger Update (Version 1.1.0)

**File**: `docs/skilled-awareness/task-tracking/ledger.md`

**Section to Add**: Version 1.1.0 entry after existing version history

**Content**: See Section 3.4 above (Ledger Update)

---

## 5. Execution Tasks

### Task 1: Add Backlog Organization Patterns to Awareness Guide

**File**: `docs/skilled-awareness/task-tracking/awareness-guide.md`

**Steps**:
1. Read existing awareness-guide.md to understand structure
2. Add new Section 4: "Backlog Organization Patterns"
3. Write 5 patterns (see Deliverable 1 for full content):
   - 4.1: Multi-Tier Priority Pattern (P0-P4)
   - 4.2: Vision Cascade Pattern (Wave 1 → Beads)
   - 4.3: Backlog Refinement Workflow (Quarterly)
   - 4.4: Epic Decomposition Template
   - 4.5: Backlog Health Queries
4. Add code examples, usage patterns, integration notes
5. Save file

**Estimated Effort**: 4 hours

**Dependencies**: None

**Success Criteria**:
- Section 4 added with 5 patterns (~12 pages)
- Each pattern includes problem, solution, workflow, examples, best practices
- Integration with SAP-006 and SAP-010 documented
- Code examples tested (can be run in chora-base)

---

### Task 2: Add Section 3.4 to Protocol Spec (Backlog Refinement Workflow)

**File**: `docs/skilled-awareness/task-tracking/protocol-spec.md`

**Steps**:
1. Read existing protocol-spec.md to understand structure
2. Add new Section 3.4 after Section 3.3
3. Write 7 subsections (see Deliverable 2 for full content):
   - 3.4.1: Stale Task Review
   - 3.4.2: Priority Adjustment
   - 3.4.3: Backlog Archival
   - 3.4.4: Epic Progress Review
   - 3.4.5: Backlog Health Metrics
   - 3.4.6: Integration with Vision Waves (SAP-006)
   - 3.4.7: Backlog Refinement Template
4. Add bash examples, A-MEM logging format
5. Save file

**Estimated Effort**: 2 hours

**Dependencies**: None

**Success Criteria**:
- Section 3.4 added with 7 subsections (~8 pages)
- Complete workflow documented (stale task review → priority adjustment → archival → epic progress → metrics logging)
- Integration with SAP-006 (vision promotion) and SAP-010 (A-MEM logging) documented
- Bash examples tested

---

### Task 3: Create Backlog Refinement Template

**File**: `.chora/memory/templates/backlog-refinement-template.md` (create new)

**Steps**:
1. Create `.chora/memory/templates/` directory if not exists
2. Write template with 7 sections (see Section 3.3 for full content):
   - Metadata (YAML frontmatter)
   - Stale Task Review
   - Priority Adjustment
   - Backlog Archival
   - Epic Progress Review
   - Backlog Health Metrics (before/after)
   - Next Steps
3. Add placeholder values (e.g., `{Count}`, `{task-id}`, `{reason}`)
4. Save file

**Estimated Effort**: 45 minutes

**Dependencies**: None

**Success Criteria**:
- Template file created in `.chora/memory/templates/`
- 7 sections with placeholders
- Teams can copy template and fill in values during refinement

---

### Task 4: Update Ledger with Version 1.1.0

**File**: `docs/skilled-awareness/task-tracking/ledger.md`

**Steps**:
1. Read existing ledger.md to understand version history format
2. Add new version entry for 1.1.0 at top of version history
3. Write version summary (see Section 3.4 for full content):
   - Status: Draft → Pilot
   - Focus: Backlog Organization Patterns
   - Enhancements (5 items)
   - Artifacts Updated (3 items)
   - Integration (3 SAPs)
   - Dogfooding Plan (chora-base, 2025-Q4, 3 months, 4 activities, 3 success criteria)
4. Save file

**Estimated Effort**: 30 minutes

**Dependencies**: Tasks 1-3 (awareness guide, protocol spec, template) must be complete first

**Success Criteria**:
- Version 1.1.0 entry added to ledger
- Dogfooding plan documented (project, timeline, activities, success criteria)
- Integration with SAP-006, SAP-010, SAP-027 documented

---

## 6. Success Criteria

### Functional Success

1. **Vision Cascade Works**: Teams can convert vision Wave 1 into prioritized backlog in <30 minutes
   - **Validation**: Execute SAP-006 Phase 1.4 with chora-base vision, measure time to create epic + 4-10 tasks
   - **Target**: <30 minutes from vision document to beads backlog

2. **Backlog Health Queries Detect Issues**: CLI queries find stale tasks, orphan tasks, epic progress in <5 seconds
   - **Validation**: Run 5 health queries on chora-base beads backlog, measure execution time
   - **Target**: All queries complete in <5 seconds

3. **Quarterly Refinement Reduces Backlog**: Refinement workflow reduces P3/P4 backlog by ≥20% per quarter
   - **Validation**: Run quarterly refinement on chora-base (end of 2025-Q4), measure P3/P4 count before/after
   - **Target**: P3+P4 count reduced by ≥20%

### Documentation Success

4. **Awareness Guide Patterns Complete**: 5 patterns documented in awareness-guide.md (~12 pages)
   - **Validation**: Check awareness-guide.md has Section 4 with 5 subsections
   - **Target**: 5 patterns with problem, solution, workflow, examples, best practices

5. **Protocol Spec Workflow Complete**: Section 3.4 documented in protocol-spec.md (~8 pages)
   - **Validation**: Check protocol-spec.md has Section 3.4 with 7 subsections
   - **Target**: Complete workflow (stale review → priority adjustment → archival → epic progress → metrics logging)

6. **Backlog Refinement Template Exists**: Template file created in `.chora/memory/templates/`
   - **Validation**: Check `.chora/memory/templates/backlog-refinement-template.md` exists
   - **Target**: 7 sections with placeholders, teams can copy and fill in

### Integration Success

7. **SAP-006 Integration**: Vision cascade pattern (Pattern 4.2) works with SAP-006 Phase 1.4
   - **Validation**: Execute SAP-006 Phase 1.4, verify beads epic created with traceability metadata
   - **Target**: Epic has `from_vision_wave`, `vision_document`, `roadmap_version` metadata

8. **SAP-010 Integration**: Backlog refinement logs metrics to A-MEM
   - **Validation**: Run quarterly refinement, check `.chora/memory/events/backlog-refinement.jsonl` has new entry
   - **Target**: Refinement metrics logged (stale tasks, priority changes, backlog snapshot)

9. **SAP-027 Integration**: Pilot GO decisions promote P3 → P2
   - **Validation**: Simulate SAP-027 pilot GO decision, verify P3 task promoted to P2 with `from_dogfooding_pilot` metadata
   - **Target**: Task has `from_dogfooding_pilot`, `decision: "GO"` metadata

---

## 7. Testing & Validation

### Unit Testing (Manual)

**Test 1: Multi-Tier Priority Pattern**
```bash
# Create tasks with P0-P4
bd create "P0 task" --priority 0
bd create "P1 task" --priority 1
bd create "P2 task" --priority 2
bd create "P3 task" --priority 3
bd create "P4 task" --priority 4

# Query by priority
bd list --status open --priority 0  # Should show P0 task
bd list --status open --priority 3,4  # Should show P3 + P4 tasks
```

**Test 2: Vision Cascade Pattern**
```bash
# Simulate SAP-006 Phase 1.4
vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"
cat "$vision_file"  # Should show Wave 1 themes

# Create epic from Wave 1
bd create "Epic: Wave 1 Theme" --type epic --priority 1 --metadata '{"from_vision_wave": 1}'

# Verify epic created
bd list --type epic --status open  # Should show new epic
```

**Test 3: Backlog Refinement Workflow**
```bash
# Simulate quarterly refinement (use template)
cp .chora/memory/templates/backlog-refinement-template.md ./refinement-test.md

# Run stale task query
bd list --status open --created-before $(date -v-90d +%Y-%m-%d)  # Should list stale tasks

# Close stale task
bd close {task-id} --reason "Stale: Test closure"

# Verify closed
bd show {task-id}  # Should show status=closed
```

**Test 4: Epic Decomposition Template**
```bash
# Create epic
epic_id=$(bd create "Test Epic" --type epic --priority 1)

# Create tasks
task1=$(bd create "Test Task 1" --priority 2 --metadata '{"effort_hours": 2}')
task2=$(bd create "Test Task 2" --priority 2 --metadata '{"effort_hours": 3}')

# Link tasks to epic
bd dep add $epic_id blocks $task1
bd dep add $epic_id blocks $task2

# Verify dependencies
bd show $epic_id --json | jq '.dependencies.blocks'  # Should show 2 task IDs
```

**Test 5: Backlog Health Queries**
```bash
# Test priority distribution
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
# Should output JSON array with counts per priority

# Test orphan tasks
bd list --status open --type task --json | jq '[.[] | select(.dependencies.blocked_by | length == 0)]'
# Should show tasks with no epic

# Test epic progress
bd show $epic_id --json
total=$(bd list --blocked-by $epic_id --json | jq 'length')
complete=$(bd list --status closed --blocked-by $epic_id --json | jq 'length')
echo "Progress: $complete/$total"
```

### Integration Testing

**Test 6: SAP-006 Integration (Vision Cascade)**
```bash
# Prerequisite: SAP-006 Phase 1.4 workflow implemented

# Execute Phase 1.4 with test vision
# Expected: Beads epic created with from_vision_wave metadata

# Verify epic
bd list --type epic --json | jq '.[] | select(.metadata.from_vision_wave == 1)'
# Should show epic with vision metadata
```

**Test 7: SAP-010 Integration (A-MEM Logging)**
```bash
# Run quarterly refinement
# Log metrics to A-MEM

cat >> .chora/memory/events/backlog-refinement.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "backlog_refinement_complete",
  "quarter": "2025-Q4-TEST",
  "metrics": {"stale_tasks_closed": 5}
}
EOF

# Verify logged
tail -1 .chora/memory/events/backlog-refinement.jsonl | jq '.event'
# Should output: "backlog_refinement_complete"
```

**Test 8: SAP-027 Integration (Pilot → Priority Promotion)**
```bash
# Create P3 task (SOMEDAY)
task_id=$(bd create "Pilot Feature" --priority 3)

# Simulate SAP-027 GO decision
bd update $task_id --priority 2 --metadata '{
  "from_dogfooding_pilot": "pilot-test-2025-q4",
  "decision": "GO"
}'

# Verify promotion
bd show $task_id --json | jq '.priority, .metadata.decision'
# Should output: 2, "GO"
```

### Dogfooding Validation (3 months)

**Project**: chora-base
**Timeline**: 2025-Q4
**Activities**:
1. **Week 1-2**: Cascade chora-base vision Wave 1 into beads backlog (Pattern 4.2)
2. **Week 3-12**: Execute tasks, track backlog health weekly (Pattern 4.5)
3. **Week 13**: Run quarterly refinement (Pattern 4.3)
4. **Week 13**: Measure success criteria (cascade time, query performance, backlog reduction)

**Success Metrics**:
- Vision cascade time: <30 minutes ✅
- Backlog health queries: <5 seconds ✅
- Quarterly refinement: P3+P4 reduced by ≥20% ✅

---

## 8. Boundaries & Integration Points

### SAP-015 Owns (Boundaries)

1. **Backlog Priority Tiers (P0-P4)**: SAP-015 defines semantic meaning of priority tiers
2. **Backlog Refinement Workflow**: SAP-015 owns quarterly grooming process
3. **Epic Decomposition Template**: SAP-015 provides template for breaking roadmap milestones into tasks
4. **Backlog Health Queries**: SAP-015 defines CLI queries for detecting backlog issues
5. **Beads CLI**: SAP-015 owns beads CLI (bd commands), git-backed persistence, task lifecycle

### SAP-015 Does NOT Own

1. **Strategic Vision Synthesis**: SAP-006 owns vision creation (SAP-015 receives cascade)
2. **Strategic Knowledge Templates**: SAP-010 owns templates (vision, roadmap milestone, etc.)
3. **Dogfooding Methodology**: SAP-027 owns pilot process (SAP-015 receives GO/NO-GO decisions)
4. **Event Memory**: SAP-010 owns A-MEM (SAP-015 logs backlog refinement events)

### Integration Points

**← SAP-006 (Development Lifecycle)**: Receives vision Wave 1 cascade
- **Trigger**: SAP-006 Phase 1.4 (Backlog Cascade)
- **Input**: Vision Wave 1 themes from vision document (SAP-010 knowledge note)
- **Output**: Beads epic (P1) + tasks (P2) with traceability metadata (`from_vision_wave`, `vision_document`, `roadmap_version`)
- **Pattern**: Vision Cascade Pattern (awareness-guide.md Section 4.2)

**← SAP-010 (Memory System)**: Links roadmap milestones, logs refinement metrics
- **Trigger**: Epic decomposition (Pattern 4.4), quarterly refinement (Pattern 4.3)
- **Input**: Roadmap milestone note (SAP-010 knowledge note type `roadmap-milestone`)
- **Output**: Epic metadata linking to roadmap milestone, refinement metrics logged to `.chora/memory/events/backlog-refinement.jsonl`
- **Pattern**: Epic Decomposition Template (awareness-guide.md Section 4.4), Backlog Refinement Workflow (protocol-spec.md Section 3.4)

**→ SAP-027 (Dogfooding Patterns)**: GO pilot decisions create beads epics, promote P3 → P2
- **Trigger**: SAP-027 pilot GO decision
- **Input**: Pilot ID, decision (GO/NO-GO)
- **Output**: If GO, create beads epic (P1) or promote P3 task to P2 with metadata (`from_dogfooding_pilot`, `decision`)
- **Pattern**: Priority Adjustment (protocol-spec.md Section 3.4.2)

### Opt-In Integration

All integration is **opt-in** via metadata fields:
- Teams can use SAP-015 without SAP-006 (no vision cascade)
- Teams can use SAP-015 without SAP-010 (no roadmap milestone links, no A-MEM logging)
- Teams can use SAP-015 without SAP-027 (no pilot-driven priority promotion)

**Metadata Fields for Integration**:
```json
{
  "from_vision_wave": 1,                          // Vision cascade (SAP-006)
  "vision_document": "vision-{project}-{horizon}",  // Vision cascade (SAP-006)
  "roadmap_version": "v1.5.0",                    // Vision cascade (SAP-006)
  "roadmap_milestone_note": "roadmap-{project}-v{version}",  // Epic decomposition (SAP-010)
  "from_dogfooding_pilot": "pilot-{id}",          // Pilot promotion (SAP-027)
  "decision": "GO"                                // Pilot promotion (SAP-027)
}
```

---

## 9. Rollout Plan

### Phase 1: Documentation (Week 1)

**Tasks**:
1. Add Backlog Organization Patterns to awareness-guide.md (4 hours)
2. Add Section 3.4 to protocol-spec.md (2 hours)
3. Create backlog-refinement-template.md (45 min)
4. Update ledger.md to version 1.1.0 (30 min)

**Total Effort**: 7.25 hours
**Owner**: SAP maintainer
**Deliverables**: 4 artifact updates

### Phase 2: Dogfooding (Weeks 2-13, ~3 months)

**Project**: chora-base
**Activities**:
1. **Week 2**: Cascade chora-base vision Wave 1 into beads backlog (Pattern 4.2)
2. **Weeks 3-12**: Execute tasks, track backlog health weekly (Pattern 4.5)
3. **Week 13**: Run quarterly refinement (Pattern 4.3)
4. **Week 13**: Measure success criteria, log results to ledger

**Total Effort**: 2-3 hours per week (backlog management overhead)
**Owner**: Chora-base maintainers
**Deliverables**: Backlog refinement report, ledger update with metrics

### Phase 3: Ecosystem Adoption (Weeks 14+)

**Promotion**: After successful dogfooding (success criteria met)
**Status**: Pilot → Production
**Channels**:
- Update sap-catalog.json status to "production"
- Announce in chora ecosystem (docs, Discord, GitHub Discussions)
- Add to SAP-003 (project-bootstrap) default adoption

**Support**:
- Answer questions via GitHub Discussions
- Iterate on patterns based on early adopter feedback

---

## 10. Open Questions

**Q1: Should priority tiers (P0-P4) be configurable?**
- **Current**: Hardcoded semantic meaning (P0=NOW, P1=NEXT, etc.)
- **Alternative**: Allow teams to configure tier names/meanings in `.beads/config.yaml`
- **Decision**: Keep hardcoded for consistency. If demand arises, add configuration in v1.2.0.

**Q2: Should backlog health queries be automated (cron job)?**
- **Current**: Manual execution during refinement
- **Alternative**: Add cron job to run queries weekly, email results
- **Decision**: Start manual. If demand arises, add automation via SAP-005 (ci-cd-workflows) in v1.2.0.

**Q3: Should epic progress % be stored in epic metadata?**
- **Current**: Calculated on-demand via CLI queries
- **Alternative**: Store `progress_percent` in epic metadata, update on task status change
- **Decision**: Start with calculated (no state mutation). If performance issues, add caching in v1.2.0.

**Q4: Should backlog refinement template be stored in SAP-015 or SAP-010?**
- **Current**: SAP-010 owns all templates (`.chora/memory/templates/`)
- **Alternative**: SAP-015 owns backlog-specific template
- **Decision**: Keep in SAP-010 for consistency (all templates in one place). SAP-015 awareness-guide references it.

**Q5: How should vision Wave 2 → Wave 1 promotion work?**
- **Current**: Manual promotion during quarterly refinement (Section 3.4.2)
- **Alternative**: Automated promotion when pilot GO decision logged (SAP-027 integration)
- **Decision**: Start manual (human judgment required). If pilot integration matures, revisit in v1.2.0.

---

## 11. References

### Internal (Chora-Base)

- **SAP-015 (Task Tracking)**: [docs/skilled-awareness/task-tracking/](../skilled-awareness/task-tracking/)
  - Capability Charter: Problem statement, solution design
  - Protocol Spec: Complete CLI reference
  - Awareness Guide: Operating patterns (will be enhanced)
  - Adoption Blueprint: Installation guide
  - Ledger: Adoption tracking (will be updated to v1.1.0)

- **SAP-006 (Development Lifecycle)**: [docs/skilled-awareness/development-lifecycle/](../skilled-awareness/development-lifecycle/)
  - Phase 1.4 (Backlog Cascade): Vision → beads integration
  - Vision synthesis workflow: Discovery → Analysis → Vision Drafting → Cascade

- **SAP-010 (Memory System)**: [docs/skilled-awareness/memory-system/](../skilled-awareness/memory-system/)
  - Strategic knowledge templates: Vision, intention inventory, roadmap milestone
  - A-MEM event logging: `.chora/memory/events/*.jsonl`

- **SAP-027 (Dogfooding Patterns)**: [docs/skilled-awareness/dogfooding-patterns/](../skilled-awareness/dogfooding-patterns/)
  - Pilot GO/NO-GO decisions: Trigger priority promotion (P3 → P2)
  - Pilot feedback: Update vision Wave 2 decision criteria

### External

- **Beads Documentation**: (if public docs exist, link here)
- **Scrum Guide (Backlog Refinement)**: [https://scrumguides.org/](https://scrumguides.org/)
- **Shape Up (Hill Charts)**: [https://basecamp.com/shapeup](https://basecamp.com/shapeup)

---

**End of SAP-015 Backlog Organization Enhancement Plan**
