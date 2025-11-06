# Agent Task Tracking Awareness Guide

**Audience:** Claude Code, Cursor, and AI agents responsible for task tracking and execution
**Version:** 1.0.0
**Last Updated:** 2025-11-04
**Prerequisites:**
- Load [protocol-spec.md](protocol-spec.md) (understand beads CLI commands and workflows)
- Beads CLI installed (`bd version` should work)
- Repository initialized with beads (`.beads/` directory exists)

---

## 1. Quick Orientation

### When to Use SAP-015 (Beads Task Tracking)

**Use beads when**:
- Starting a new session and need to find unfinished work
- Tracking complex features spanning multiple sessions (5+ steps)
- Managing dependencies between tasks (what blocks what)
- Coordinating with other agents on shared repository
- Breaking down large features into trackable subtasks

**Don't use beads for**:
- Cross-repository coordination (use SAP-001 inbox instead)
- Event history/"what was done" tracking (use SAP-010 A-MEM instead)
- Simple single-step tasks that finish in one session
- Documentation-only changes with no task decomposition

### Capability Summary

Beads provides persistent task memory via git-backed JSONL storage:
- **Key Commands:**
  - `bd ready` — Show unblocked work ready to claim
  - `bd create "title"` — Create new task
  - `bd update {id} --status {status}` — Update task status
  - `bd close {id}` — Mark task complete
  - `bd dep add {blocked} {blocker}` — Add dependency

- **Key Paths:**
  - `.beads/beads.db` — SQLite cache (gitignored, fast queries)
  - `.beads/issues.jsonl` — Source of truth (committed to git)
  - `.beads/config.yaml` — Project configuration

---

## 2. Operating Patterns

### Pattern A: Session Start — Find Work

**Recognize:** User starts new session, asks "What should I work on?" or similar

**Act:**
```bash
# 1. Check for ready work (open tasks with no blockers)
bd ready --json

# 2. Review output and select task based on:
#    - Priority (0 = highest)
#    - Labels (e.g., "p0", "bug", "feature")
#    - Assignee (unclaimed or assigned to you)

# 3. Claim selected task
bd update chora-base-a3f8 --status in_progress --assignee claude-code

# 4. Show full task context
bd show chora-base-a3f8 --json

# 5. Summarize task for user
```

**Confirm:** Present task summary to user: "Working on `{title}` (Priority {priority}): {description}"

**Example:**
```
User: "What should I work on?"

Agent:
1. Runs `bd ready --json`
2. Finds 3 ready tasks, selects P0 task: "chora-base-a3f8: Implement OAuth flow"
3. Claims: `bd update chora-base-a3f8 --status in_progress --assignee claude-code`
4. Shows details: `bd show chora-base-a3f8 --json`
5. Says: "Working on P0 task: Implement OAuth2 flow for GitHub authentication. Description: Add OAuth2 provider with callback handler. No blockers."
```

---

### Pattern B: Task Completion

**Recognize:** Work finished, tests passing, ready to close task

**Act:**
```bash
# 1. Close completed task with reason
bd close chora-base-a3f8 --reason "Implemented OAuth2 flow with tests"

# 2. Check for newly-ready work (tasks unblocked by this completion)
bd ready --json

# 3. Optional: Export task summary for documentation
bd show chora-base-a3f8 --json > .chora/memory/tasks/chora-base-a3f8-summary.json
```

**Confirm:** "Task completed: `{title}`. {N} tasks now unblocked and ready."

**Example:**
```
User: "Looks good, wrap it up"

Agent:
1. Closes: `bd close chora-base-a3f8 --reason "OAuth2 flow implemented with unit tests"`
2. Checks: `bd ready --json`
3. Finds 2 newly-unblocked tasks
4. Says: "Task completed: Implement OAuth2 flow. 2 tasks now unblocked: Write integration tests (chora-base-b2c4), Update auth documentation (chora-base-c5d6)."
```

---

### Pattern C: Discovering Subtasks

**Recognize:** While working on task, discover subtasks needed

**Act:**
```bash
# 1. Create subtask(s)
bd create "Write OAuth2 tests" --priority 0 --assignee claude-code

# 2. Link as blocker (subtask blocks parent)
bd dep add chora-base-a3f8 chora-base-d7e9

# 3. Update parent status (now blocked)
bd update chora-base-a3f8 --status open  # Back to open

# 4. Update subtask status (start working)
bd update chora-base-d7e9 --status in_progress

# 5. Show dependency tree
bd dep tree chora-base-a3f8
```

**Confirm:** "Discovered subtask: `{subtask_title}`. Updated dependencies. Now working on subtask."

**Example:**
```
Agent (while working): "I need to write tests for OAuth2 before marking this complete."

Agent:
1. Creates: `bd create "Write OAuth2 unit tests" --priority 0`
2. Links: `bd dep add chora-base-a3f8 chora-base-d7e9`
3. Updates parent: `bd update chora-base-a3f8 --status open`
4. Starts subtask: `bd update chora-base-d7e9 --status in_progress`
5. Says: "Discovered subtask: Write OAuth2 unit tests. Updated dependencies. Now working on subtask first."
```

---

### Pattern D: Breaking Down Large Features

**Recognize:** User requests complex feature requiring multiple steps

**Act:**
```bash
# 1. Create epic task
bd create "Implement user authentication system" \
  --priority 0 \
  --type epic \
  --description "Complete auth system with OAuth, JWT, session management"

# 2. Create subtasks
bd create "Implement OAuth2 provider" --priority 0
bd create "Add JWT token generation" --priority 1
bd create "Create session middleware" --priority 1
bd create "Write authentication tests" --priority 1

# 3. Link subtasks to epic (parent-child)
bd dep add chora-base-epic1 chora-base-task1 --type parent
bd dep add chora-base-epic1 chora-base-task2 --type parent
bd dep add chora-base-epic1 chora-base-task3 --type parent
bd dep add chora-base-epic1 chora-base-task4 --type parent

# 4. Link blocking dependencies between subtasks (if any)
bd dep add chora-base-task2 chora-base-task1  # JWT needs OAuth first

# 5. Show dependency tree
bd dep tree chora-base-epic1

# 6. Start first task
bd update chora-base-task1 --status in_progress --assignee claude-code
```

**Confirm:** "Created epic `{epic_title}` with {N} subtasks. Starting with: `{first_task_title}`"

**Example:**
```
User: "Build a complete authentication system with OAuth and JWT"

Agent:
1. Creates epic: `bd create "User authentication system" --priority 0 --type epic`
2. Creates 4 subtasks (OAuth, JWT, sessions, tests)
3. Links to epic with parent-child relationships
4. Adds blocking: JWT depends on OAuth completing
5. Shows tree: `bd dep tree chora-base-epic1`
6. Says: "Created epic 'User authentication system' with 4 subtasks. Starting with: Implement OAuth2 provider (no blockers, P0)."
```

---

### Pattern E: Multi-Agent Coordination

**Recognize:** Multiple agents working on repository, need to coordinate

**Act:**
```bash
# Agent 1: Check what others are working on
bd list --status in_progress --json

# Agent 1: Find available work (not assigned)
bd ready --json | jq '.[] | select(.assignee == null or .assignee == "")'

# Agent 1: Claim available task
bd update chora-base-b2c4 --status in_progress --assignee claude-code

# Agent 1: Commit and push
git add .beads/issues.jsonl
git commit -m "task: Claim task chora-base-b2c4"
git push

# Agent 2: Pull updates
git pull  # Auto-imports new task states

# Agent 2: Check updated ready work
bd ready --json
```

**Confirm:** "Checked coordination state. {N} tasks in progress by other agents. Claimed: `{task_title}`"

**Example:**
```
Agent (Claude Code):
1. Lists: `bd list --status in_progress --json`
2. Sees: Agent "cursor-agent" working on chora-base-a3f8
3. Finds: `bd ready --json` shows chora-base-b2c4 available
4. Claims: `bd update chora-base-b2c4 --status in_progress --assignee claude-code`
5. Commits: `git add .beads/issues.jsonl && git commit -m "task: Claim b2c4" && git push`
6. Says: "Checked coordination state. 1 task in progress by cursor-agent. Claimed: Write integration tests (chora-base-b2c4)."
```

---

### Pattern F: Checking Task Status

**Recognize:** User asks "What's the status?" or "What are we working on?"

**Act:**
```bash
# 1. Show in-progress tasks
bd list --status in_progress --json

# 2. Show ready work (backlog)
bd ready --json

# 3. Show recently closed tasks (last 5-10)
bd list --status closed --json | jq '.[:10]'

# 4. Show blocked tasks
bd list --status open --json | jq '.[] | select(.dependencies | length > 0)'

# 5. Show dependency tree for specific task (if user asks)
bd dep tree chora-base-epic1
```

**Confirm:** Present summary: "{N} in progress, {M} ready, {K} blocked"

**Example:**
```
User: "Give me a status update"

Agent:
1. Checks: `bd list --status in_progress --json` (2 tasks)
2. Checks: `bd ready --json` (5 tasks)
3. Checks blocked: `bd list --status open --json | jq '...'` (3 tasks)
4. Says: "Status: 2 tasks in progress (OAuth flow, integration tests), 5 tasks ready to start, 3 tasks blocked waiting on dependencies. Epic 'User auth system' is 50% complete (2/4 subtasks done)."
```

---

### Pattern G: Resolving Circular Dependencies

**Recognize:** `bd dep add` fails with "circular dependency detected"

**Act:**
```bash
# 1. Detect cycle
bd dep cycles

# 2. Visualize dependency tree
bd dep tree chora-base-a3f8

# 3. Remove problematic dependency
bd dep remove chora-base-a3f8 chora-base-b2c4

# 4. Add correct dependency direction (if needed)
bd dep add chora-base-b2c4 chora-base-a3f8

# 5. Verify cycle resolved
bd dep cycles  # Should return empty
```

**Confirm:** "Resolved circular dependency: {task_a} ↔ {task_b}. Corrected to: {task_b} → {task_a}"

---

### Pattern H: Integration with Inbox (SAP-001)

**Recognize:** Coordination request from inbox needs task decomposition

**Act:**
```bash
# 1. Read coordination request
cat inbox/incoming/coordination/coord-003.json

# 2. Create epic for coordination
bd create "COORD-2025-003: Implement SAP-020 React foundation" \
  --priority 0 \
  --type epic \
  --description "From inbox coordination request coord-003"

# 3. Create subtasks based on coordination requirements
bd create "Write SAP-020 capability charter" --priority 0
bd create "Write SAP-020 protocol spec" --priority 1
# ... more subtasks

# 4. Link to epic
bd dep add chora-base-epic1 chora-base-task1 --type parent
# ... more links

# 5. Log coordination event in A-MEM
echo '{"event": "coordination_decomposed", "coord_id": "coord-003", "beads_epic": "chora-base-epic1", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> .chora/memory/events/inbox.jsonl

# 6. Move coordination request to active
mkdir -p inbox/active/coord-003
mv inbox/incoming/coordination/coord-003.json inbox/active/coord-003/
```

**Confirm:** "Decomposed coordination COORD-2025-003 into {N} tasks under epic `{epic_id}`"

---

### Pattern I: Integration with A-MEM (SAP-010)

**Recognize:** Correlate beads tasks with A-MEM event traces

**Act:**
```bash
# 1. Create task with trace ID in description
bd create "Implement OAuth flow" \
  --priority 0 \
  --description "OAuth2 implementation\n\nTrace: oauth-impl-2025-11"

# 2. Log task start event in A-MEM
echo '{"event": "task_started", "beads_id": "chora-base-a3f8", "trace_id": "oauth-impl-2025-11", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> .chora/memory/events/development.jsonl

# 3. Work on task (code, test, etc.)
# ... development work ...

# 4. Log task completion in A-MEM
echo '{"event": "task_completed", "beads_id": "chora-base-a3f8", "trace_id": "oauth-impl-2025-11", "outcome": "success", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> .chora/memory/events/development.jsonl

# 5. Close beads task
bd close chora-base-a3f8 --reason "OAuth2 flow complete, trace: oauth-impl-2025-11"
```

**Confirm:** "Task tracked in A-MEM with trace ID: {trace_id}"

---

## 3. Decision Trees

### Should I use beads for this task?

```
Is this a complex feature (5+ steps)?
├─ YES → Use beads for task decomposition
└─ NO → Is it multi-session work?
    ├─ YES → Use beads for persistence
    └─ NO → Does it have dependencies?
        ├─ YES → Use beads for dependency tracking
        └─ NO → Skip beads, track manually
```

### Should I create subtasks or complete the task?

```
While working, did I discover new requirements?
├─ YES → Estimate effort
│   ├─ >30 min → Create subtask, mark parent blocked
│   └─ <30 min → Complete inline, no subtask
└─ NO → Complete current task
```

### Which status should I set?

```
Task state?
├─ Not started → status: open
├─ Working now → status: in_progress
├─ Blocked by other task → status: open (add dependency)
└─ Finished → Close with reason
```

---

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

## 5. Common Mistakes & Corrections

### Mistake 1: Not checking ready work at session start

**Wrong:**
```
User: "What should I work on?"
Agent: "Let me look at the code..."
```

**Correct:**
```
User: "What should I work on?"
Agent: (runs `bd ready --json`)
Agent: "You have 3 ready tasks: [lists tasks]. Highest priority is P0: Implement OAuth flow. Should I start there?"
```

---

### Mistake 2: Forgetting to update status when starting work

**Wrong:**
```
bd ready  # Find task
# Start coding immediately
```

**Correct:**
```
bd ready  # Find task chora-base-a3f8
bd update chora-base-a3f8 --status in_progress --assignee claude-code
# Now start coding
```

---

### Mistake 3: Not closing tasks when complete

**Wrong:**
```
# Finish work, commit code
git commit -m "feat: Add OAuth"
# Move on to next task
```

**Correct:**
```
# Finish work
bd close chora-base-a3f8 --reason "OAuth2 flow implemented"
git add .beads/issues.jsonl
git commit -m "feat: Add OAuth (closes chora-base-a3f8)"
bd ready  # Check for newly-unblocked work
```

---

### Mistake 4: Creating too many granular tasks

**Wrong:**
```
bd create "Import auth module"
bd create "Define OAuth class"
bd create "Write __init__ method"
bd create "Write authenticate method"
# Too granular!
```

**Correct:**
```
bd create "Implement OAuth2 provider class" --priority 0
# One task for cohesive unit of work
```

---

### Mistake 5: Not using dependencies for blocked work

**Wrong:**
```
bd create "Write integration tests"  # Depends on OAuth being done
# No dependency link, appears as "ready" even though blocked
```

**Correct:**
```
bd create "Write integration tests" --priority 1
bd dep add chora-base-b2c4 chora-base-a3f8  # Tests block on OAuth
# Now correctly appears as blocked until OAuth done
```

---

## 6. Troubleshooting

### Issue: `bd` command not found

**Solution:**
```bash
# Check installation
npm list -g @beads/bd

# If not installed
npm install -g @beads/bd

# Verify
bd version
```

---

### Issue: "Database not found" error

**Solution:**
```bash
# Check if initialized
ls .beads/

# If not initialized
bd init

# Verify
bd status
```

---

### Issue: Git merge conflict in `.beads/issues.jsonl`

**Solution:**
```bash
# JSONL is line-based, conflicts are rare
# If they occur, resolve manually:

# 1. Open .beads/issues.jsonl
# 2. Resolve conflict markers (<<<<, ====, >>>>)
# 3. Ensure each line is valid JSON
# 4. Save file

# 5. Re-import
bd import

# 6. Verify
bd validate
```

---

### Issue: Task appears as "ready" but should be blocked

**Solution:**
```bash
# Check dependencies
bd show chora-base-a3f8 --json | jq '.dependencies'

# If missing blocker
bd dep add chora-base-a3f8 chora-base-blocker-id

# Verify
bd ready  # Task should no longer appear
```

---

## 7. Best Practices

### ✅ DO

1. **Check ready work at session start** — `bd ready --json` first thing
2. **Update status when starting** — `bd update {id} --status in_progress --assignee {agent}`
3. **Close tasks with reasons** — `bd close {id} --reason "Completed X"`
4. **Use dependencies for blockers** — `bd dep add {blocked} {blocker}`
5. **Commit `.beads/issues.jsonl` with code** — Keep tasks synced with git
6. **Use priorities** — P0 (highest) for urgent, P1-2 for normal, P3-4 for backlog
7. **Add descriptions** — Provide context for future sessions
8. **Use epics for large features** — Break down into subtasks

### ❌ DON'T

1. **Don't skip status updates** — Always update when starting/completing work
2. **Don't create too-granular tasks** — Tasks should be 30min-4hr units of work
3. **Don't forget to close tasks** — Closed tasks unlock dependent work
4. **Don't ignore circular dependencies** — Run `bd dep cycles` if suspicious
5. **Don't edit `.beads/issues.jsonl` manually** — Use `bd` commands instead
6. **Don't commit `.beads/beads.db`** — SQLite cache is gitignored (intentional)

---

## 8. Quick Reference Card

```bash
# === SESSION START ===
bd ready --json                    # Find unblocked work
bd update {id} --status in_progress --assignee {agent}
bd show {id} --json                # Get task context

# === DURING WORK ===
bd create "Task title" --priority 0        # New subtask discovered
bd dep add {blocked} {blocker}             # Link dependency
bd update {parent} --status open           # Parent now blocked

# === SESSION END ===
bd close {id} --reason "Completed X"       # Mark done
bd ready --json                            # Check newly-unblocked work

# === STATUS CHECK ===
bd list --status in_progress --json        # What's active
bd ready --json                            # What's available
bd dep tree {id}                           # Visualize dependencies

# === COORDINATION ===
bd list --status in_progress --json        # Who's working on what
git pull                                   # Sync task updates
git add .beads/issues.jsonl && git commit  # Share task updates

# === TROUBLESHOOTING ===
bd doctor                          # Health check
bd validate                        # Integrity check
bd dep cycles                      # Detect circular deps
```

---

## 9. Integration Checklist

When using beads in a chora-base project:

- [ ] Beads initialized (`bd init` completed)
- [ ] Git hooks installed (pre-commit, post-merge)
- [ ] AGENTS.md updated with beads patterns (SAP-009)
- [ ] First task created and tracked
- [ ] `.beads/issues.jsonl` committed to git
- [ ] Team members aware of beads workflow
- [ ] Integration with inbox (SAP-001) documented (if applicable)
- [ ] Integration with A-MEM (SAP-010) documented (if applicable)

---

## 10. Training Exercises

### Exercise 1: Basic Workflow

1. Check ready work: `bd ready --json`
2. Create task: `bd create "Exercise task" --priority 0`
3. Start task: `bd update {id} --status in_progress --assignee claude-code`
4. Complete task: `bd close {id} --reason "Exercise complete"`
5. Verify: `bd list --status closed --json`

### Exercise 2: Dependencies

1. Create two tasks: A and B
2. Make B block A: `bd dep add {A} {B}`
3. Check ready: `bd ready` (only B appears)
4. Complete B: `bd close {B}`
5. Check ready: `bd ready` (A now appears)

### Exercise 3: Feature Decomposition

1. Create epic: `bd create "Build API" --type epic`
2. Create 3 subtasks
3. Link to epic: `bd dep add {epic} {subtask} --type parent` (3x)
4. Visualize: `bd dep tree {epic}`
5. Work through subtasks sequentially

---

**Related Documents:**
- [protocol-spec.md](protocol-spec.md) - Complete CLI reference
- [capability-charter.md](capability-charter.md) - SAP-015 charter
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide

---

**Version History:**
- **1.0.0** (2025-11-04): Initial awareness guide for beads integration
