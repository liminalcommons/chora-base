# Agent Task Tracking Protocol Specification
## Beads Integration

**Version:** 1.0.0
**Status:** Pilot (Phase 1)
**Maintainer:** Capability Owner (Victor Piper)
**Last Updated:** 2025-11-04

---

## 1. Overview

- **Purpose:** Provide persistent task memory for AI agents across sessions using the beads CLI tool, enabling dependency-aware task tracking and multi-agent coordination.
- **Intended Consumers:**
  - AI agents (Claude Code, Cursor, etc.) executing task workflows
  - Repository maintainers implementing beads in projects
  - Developers coordinating multi-agent workflows
- **Modes of Operation:**
  - **Single-Agent Mode:** One agent tracking tasks across multiple sessions
  - **Multi-Agent Mode:** Multiple agents coordinating via shared git-backed task database

---

## 2. Design Principles

1. **Git-Native Storage** — Tasks stored in `.beads/issues.jsonl`, synced via git
2. **Agent Accessibility** — CLI-first design with `--json` flags for programmatic parsing
3. **Dependency Awareness** — Automatic ready-work detection based on blocking relationships
4. **Session Persistence** — Tasks survive context resets and agent restarts
5. **Multi-Agent Safety** — Hash-based IDs (v0.20.1+) prevent collision across agents

---

## 3. Functional Requirements

- **FR-1:** Initialize beads in repository with project-specific prefix and git hooks
- **FR-2:** Create, read, update, delete (CRUD) issues with metadata (title, description, priority, assignee, status)
- **FR-3:** Manage dependencies between issues (blocks, related, parent-child, discovered-from)
- **FR-4:** Query ready work (open issues with no blocking dependencies)
- **FR-5:** Automatic JSONL sync after CRUD operations (5s debounce)
- **FR-6:** Automatic JSONL import when newer than SQLite DB (after git pull)
- **FR-7:** Support for programmatic access via `--json` output flags
- **FR-8:** Integration with git workflows (hooks, branches, commits)

---

## 4. Architecture

### Storage Model

```
┌─────────────────────────────────────────────────┐
│ Repository Root                                 │
│                                                 │
│ ┌─────────────────┐      ┌──────────────────┐  │
│ │ .beads/         │      │ .beads/          │  │
│ │ beads.db        │ ←──→ │ issues.jsonl     │  │
│ │ (SQLite cache)  │      │ (source of truth)│  │
│ │ (gitignored)    │      │ (committed)      │  │
│ └─────────────────┘      └──────────────────┘  │
│         ↑                        ↓              │
│         │                        │              │
│    Query (fast)           Sync (auto)           │
│                                                 │
│ ┌───────────────────────────────────────────┐  │
│ │ .beads/config.yaml                        │  │
│ │ .beads/metadata.json                      │  │
│ │ (project config, committed)                │  │
│ └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                   │
                   ↓ (git push/pull)
          ┌────────────────┐
          │ Git Remote     │
          │ (GitHub/GitLab)│
          └────────────────┘
                   ↑
                   │
          ┌────────┴────────┐
          │                 │
    ┌─────▼─────┐    ┌─────▼─────┐
    │ Agent 2   │    │ Agent 3   │
    │ (Machine 2│    │ (Machine 3)│
    └───────────┘    └───────────┘
```

### Database Files

| File | Purpose | Git Tracked | Required |
|------|---------|-------------|----------|
| `.beads/beads.db` | SQLite cache for fast queries | ❌ No (gitignored) | ✅ Yes |
| `.beads/issues.jsonl` | Source of truth for issues | ✅ Yes (committed) | ✅ Yes |
| `.beads/config.yaml` | Project configuration | ✅ Yes (committed) | ✅ Yes |
| `.beads/metadata.json` | Repository metadata | ✅ Yes (committed) | ✅ Yes |
| `.beads/.gitignore` | Ignores SQLite files | ✅ Yes (committed) | ✅ Yes |

---

## 5. Issue Schema

### Core Fields

```json
{
  "id": "chora-base-a3f8",
  "title": "Implement beads integration for SAP-015",
  "description": "Add beads task tracking to chora-base as optional SAP",
  "status": "in_progress",
  "priority": 0,
  "assignee": "claude-code",
  "labels": ["sap-015", "task-tracking", "beads"],
  "created_at": "2025-11-04T17:32:00Z",
  "updated_at": "2025-11-04T18:15:00Z",
  "closed_at": null,
  "dependencies": [
    {
      "type": "blocks",
      "target_id": "chora-base-b2c4",
      "note": "Requires beads installation complete"
    }
  ],
  "metadata": {
    "trace_id": "sap-015-pilot",
    "epic": "SAP-015-implementation",
    "affects_saps": ["SAP-015", "SAP-009"],
    "affects_artifacts": [
      "/docs/skilled-awareness/task-tracking/CLAUDE.md",
      "/docs/skilled-awareness/task-tracking/protocol-spec.md"
    ],
    "sap_adoption_phase": "Phase 2"
  }
}
```

### Field Specifications

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | ✅ Yes (auto) | `{prefix}-{hash}` | Hash-based ID (v0.20.1+), e.g., `chora-base-a3f8` |
| `title` | string | ✅ Yes | - | Issue title (short description) |
| `description` | string | ❌ No | `""` | Long-form issue description |
| `status` | enum | ✅ Yes | `"open"` | Status: `open`, `in_progress`, `closed` |
| `priority` | int | ❌ No | `2` | Priority 0-4 (0=highest, 4=lowest) |
| `assignee` | string | ❌ No | `null` | Assigned user/agent |
| `labels` | array | ❌ No | `[]` | Tags for categorization |
| `created_at` | datetime | ✅ Yes (auto) | now | ISO 8601 timestamp |
| `updated_at` | datetime | ✅ Yes (auto) | now | ISO 8601 timestamp |
| `closed_at` | datetime | ❌ No | `null` | ISO 8601 timestamp when closed |
| `dependencies` | array | ❌ No | `[]` | Dependency relationships |
| `metadata` | object | ❌ No | `{}` | Flexible metadata for context (see Metadata Fields below) |

### Metadata Fields (SAP Correlation)

The `metadata` object supports flexible key-value pairs. The following fields are **recommended** for SAP-related tasks to enable curation and progress tracking:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `affects_saps` | array | ❌ No | SAP IDs affected by this task | `["SAP-015", "SAP-009"]` |
| `affects_artifacts` | array | ❌ No | File paths created/modified by this task | `["/docs/skilled-awareness/task-tracking/CLAUDE.md"]` |
| `sap_adoption_phase` | string | ❌ No | Adoption phase from SAP plan (e.g., "Phase 2") | `"Phase 2"` |
| `epic` | string | ❌ No | Parent epic ID or name | `"SAP-015-implementation"` |
| `trace_id` | string | ❌ No | A-MEM trace correlation ID | `"sap-015-pilot"` |

**Use Cases**:
- **SAP Progress Tracking**: Query tasks by `affects_saps` to see adoption progress
- **Impact Analysis**: Find all tasks touching specific artifacts
- **Epic Rollup**: Group tasks by `epic` for project planning
- **A-MEM Correlation**: Link tasks to event traces via `trace_id`

**Example Queries**:
```bash
# Find all tasks related to SAP-015
bd list --json | jq '.[] | select(.metadata.affects_saps[]? == "SAP-015")'

# Find tasks in Phase 2
bd list --json | jq '.[] | select(.metadata.sap_adoption_phase == "Phase 2")'

# Find tasks affecting specific file
bd list --json | jq '.[] | select(.metadata.affects_artifacts[]? | contains("CLAUDE.md"))'
```

### Dependency Types

| Type | Symbol | Meaning | Blocking | Use Case |
|------|--------|---------|----------|----------|
| `blocks` | → | Hard dependency | ✅ Yes | "Task B must finish before Task A starts" |
| `related` | ↔ | Soft connection | ❌ No | "Task A and B are contextually related" |
| `parent` | ↓ | Epic/subtask | ❌ No | "Task A is parent epic of Task B" |
| `child` | ↑ | Subtask/epic | ❌ No | "Task B is child of Task A" |
| `discovered-from` | ⤴ | AI discovery | ❌ No | "Agent found Task B while working on Task A" |

---

## 6. CLI Command Reference

### Initialization

```bash
# Initialize beads in repository (auto-detects prefix from directory name)
bd init

# Initialize with custom prefix
bd init --prefix myproject

# Initialize with separate branch for protected main (GitHub/GitLab)
bd init --branch beads-metadata
```

**Auto-Configured**:
- Creates `.beads/` directory
- Sets up git hooks (pre-commit, post-merge)
- Creates `.beads/.gitignore` (ignores SQLite files)
- Generates project metadata

### Issue Creation

```bash
# Create basic issue
bd create "Fix authentication bug"

# Create issue with full metadata
bd create "Add OAuth support" \
  --priority 0 \
  --type feature \
  --assignee claude-code \
  --description "Implement OAuth2 flow for GitHub"

# Create with JSON output (agent-friendly)
bd create "Write tests" --json
```

### Querying Issues

```bash
# List all issues
bd list

# List by status
bd list --status open
bd list --status in_progress
bd list --status closed

# List by priority
bd list --priority 0  # Highest priority
bd list --priority 4  # Lowest priority

# Show issue details
bd show chora-base-a3f8

# Show issue details (JSON format for agents)
bd show chora-base-a3f8 --json

# Show ready work (no blockers)
bd ready

# Show ready work (JSON for agents)
bd ready --json
```

### Updating Issues

```bash
# Update status
bd update chora-base-a3f8 --status in_progress
bd update chora-base-a3f8 --status closed

# Update priority
bd update chora-base-a3f8 --priority 0

# Update assignee
bd update chora-base-a3f8 --assignee cursor-agent

# Add labels
bd label add chora-base-a3f8 bug urgent p0
```

### Dependency Management

```bash
# Add blocking dependency (B blocks A)
bd dep add chora-base-a3f8 chora-base-b2c4
# Meaning: chora-base-b2c4 must complete before chora-base-a3f8 starts

# Add related (soft) dependency
bd dep add chora-base-a3f8 chora-base-c5d6 --type related

# Add parent-child relationship
bd dep add chora-base-epic1 chora-base-task1 --type parent

# View dependency tree
bd dep tree chora-base-a3f8

# Detect circular dependencies
bd dep cycles

# Remove dependency
bd dep remove chora-base-a3f8 chora-base-b2c4
```

### Closing Issues

```bash
# Close single issue
bd close chora-base-a3f8

# Close with reason
bd close chora-base-a3f8 --reason "Fixed in PR #42"

# Close multiple issues
bd close chora-base-a3f8 chora-base-b2c4 chora-base-c5d6

# Reopen closed issue
bd reopen chora-base-a3f8
```

### Status & Maintenance

```bash
# Show database status
bd status

# Show database info (paths, sizes)
bd info

# Run health checks
bd doctor

# Validate database integrity
bd validate

# Export to JSONL (usually automatic)
bd export

# Import from JSONL (usually automatic)
bd import

# Compact old closed issues
bd compact
```

---

## 7. Workflows

### Workflow 1: Agent Session Start

**Scenario**: Agent starts new session, needs to find work

```bash
# 1. Check for ready work (no blockers)
bd ready --json

# 2. If work found, claim task
bd update chora-base-a3f8 --status in_progress --assignee claude-code

# 3. Show task details for context
bd show chora-base-a3f8 --json
```

**Agent Pattern**:
```
1. Run `bd ready` to find unblocked tasks
2. Select task based on priority/labels
3. Update status to `in_progress` and assign to self
4. Begin work with full task context
```

### Workflow 2: Task Completion

**Scenario**: Agent finishes task, updates status, checks for newly-ready work

```bash
# 1. Close completed task
bd close chora-base-a3f8 --reason "Implemented OAuth2 flow"

# 2. Check for newly-ready work (tasks that were blocked by this one)
bd ready --json

# 3. Optional: Export summary
bd show chora-base-a3f8 --json > task-summary.json
```

### Workflow 3: Discovering Subtasks

**Scenario**: Agent working on task, discovers subtasks needed

```bash
# 1. Create subtask
bd create "Write OAuth2 tests" \
  --priority 0 \
  --assignee claude-code

# 2. Link as dependency (subtask blocks parent)
bd dep add chora-base-a3f8 chora-base-d7e9

# 3. Update parent status if blocked
bd update chora-base-a3f8 --status open  # Back to open, blocked by subtask

# 4. Work on subtask instead
bd update chora-base-d7e9 --status in_progress
```

### Workflow 4: Multi-Agent Coordination

**Scenario**: Multiple agents working on same repository

```bash
# Agent 1: Create task and push
bd create "Implement feature X" --priority 0
bd update chora-base-f1a2 --status in_progress --assignee agent-1
git add .beads/issues.jsonl
git commit -m "feat: Start feature X implementation"
git push

# Agent 2: Pull updates and find work
git pull  # Auto-imports new tasks from issues.jsonl
bd ready --json  # See what's available
bd update chora-base-g3h4 --status in_progress --assignee agent-2

# Agent 1: Push completion
bd close chora-base-f1a2
git add .beads/issues.jsonl
git commit -m "feat: Complete feature X"
git push

# Agent 2: Pull completion, dependencies update
git pull  # Auto-imports closed tasks
bd ready --json  # See if any newly-unblocked work
```

### Workflow 5: Backlog Refinement (Quarterly)

**Scenario**: Quarterly backlog grooming to maintain backlog health

**Duration**: 2-4 hours per quarter

**Frequency**: Quarterly (aligned with vision synthesis cycles)

**Inputs**:
1. Current backlog snapshot: `bd list --status open --json > backlog-snapshot-$(date +%Y-Q%q).json`
2. Stale task threshold: 90 days (configurable)
3. Priority distribution target: P0 (<5%), P1 (<20%), P2 (<30%), P3 (<30%), P4 (<15%)
4. Epic completion rates from last quarter

**Activities**:

**Step 1: Stale Task Review**
```bash
# Find tasks >90 days old
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json > stale-tasks.json

# Review each stale task:
# - Still relevant? Update priority or close
# - Blocked indefinitely? Convert to P4 (BACKLOG) or close
# - Wrong priority? Adjust based on current strategy
```

**Step 2: Priority Adjustment**
```bash
# Get priority distribution
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'

# Adjust priorities based on:
# - Vision wave alignment (Wave 1 → P1/P2, Wave 2 → P3, Wave 3 → P4)
# - Roadmap commitments (Committed → P1/P2, Exploratory → P3)
# - Resource availability (Team capacity for P0/P1 work)

# Example: Downgrade exploratory tasks
bd list --priority 1 --json | jq '.[] | select(.metadata.vision_wave == 2) | .id' | xargs -I {} bd update {} --priority 3
```

**Step 3: Backlog Archival**
```bash
# Close stale P4 tasks that won't be done
bd list --priority 4 --status open --created-before $(date -v-180d +%Y-%m-%d) --json | \
  jq -r '.[] | .id' | \
  xargs -I {} bd close {} --reason "Backlog cleanup: archived after 180 days in P4"

# Archive closed tasks older than 1 year (optional, for performance)
bd compact --older-than 365d
```

**Step 4: Epic Progress Review**
```bash
# List all epics with completion stats
bd list --type epic --status open --json | jq '.[] | {
  id: .id,
  title: .title,
  total_subtasks: (.dependencies | map(select(.type == "parent")) | length),
  completed_subtasks: (.dependencies | map(select(.type == "parent" and .target_status == "closed")) | length)
}'

# For epics with 100% completion: Close epic
# For epics stalled >90 days: Re-evaluate or deprioritize
```

**Step 5: Metadata Refresh**
```bash
# Update epic metadata with vision wave alignment
bd list --type epic --status open --json | jq -r '.[] | .id' | while read epic_id; do
  # Prompt: "Is this epic still aligned with current vision?"
  # Update metadata: bd update $epic_id --metadata '{"vision_wave": 2, "target_quarter": "2026-Q2"}'
done
```

**Outputs**:
1. Refined backlog with adjusted priorities
2. Closed stale/irrelevant tasks
3. Updated epic metadata
4. Backlog health metrics logged to A-MEM

**Quality Gates**:
- ✅ Stale tasks (>90 days) reduced by ≥50%
- ✅ Priority distribution within ±5% of target distribution
- ✅ All P0 tasks have assignees and are unblocked
- ✅ All epics have updated progress notes or are closed
- ✅ Backlog health metrics logged to `.chora/memory/events/backlog-health.jsonl`

**Integration with SAP-010 (A-MEM)**:

Log backlog health snapshot to A-MEM:
```bash
# Create backlog health event
cat <<EOF >> .chora/memory/events/backlog-health.jsonl
{
  "event": "backlog_refinement_completed",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "quarter": "$(date +%Y-Q%q)",
  "metrics": {
    "total_open_tasks": $(bd list --status open --json | jq 'length'),
    "stale_tasks_count": $(bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json | jq 'length'),
    "priority_distribution": $(bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'),
    "epic_completion_rate": $(bd list --type epic --status closed --created-after $(date -v-90d +%Y-%m-%d) --json | jq 'length')
  },
  "actions_taken": {
    "tasks_closed": $(bd list --status closed --closed-after $(date -v-7d +%Y-%m-%d) --json | jq 'length'),
    "priorities_adjusted": 42,
    "epics_closed": 3
  }
}
EOF
```

**Traceability**:
- Backlog refinement events stored in `.chora/memory/events/backlog-health.jsonl`
- Links to vision synthesis cycle (SAP-006) via `quarter` field
- Provides historical data for strategic planning (e.g., velocity trends, priority drift)

---

## 8. Integration with Chora-Base

### Integration with SAP-001 (Inbox)

**Use Case**: Coordination request becomes multiple beads tasks

```bash
# Coordination request: COORD-2025-003 (inbox/incoming/coordination/coord-003.json)
# Action: Break down into beads tasks

# 1. Create epic task for coordination
bd create "COORD-2025-003: Implement SAP-020 React foundation" \
  --priority 0 \
  --type epic \
  --description "From inbox coordination request coord-003"

# 2. Create subtasks
bd create "Write SAP-020 capability charter" --priority 0
bd create "Write SAP-020 protocol spec" --priority 1
bd create "Write SAP-020 awareness guide" --priority 1

# 3. Link dependencies
bd dep add chora-base-epic1 chora-base-task1 --type parent
bd dep add chora-base-epic1 chora-base-task2 --type parent
bd dep add chora-base-epic1 chora-base-task3 --type parent

# 4. Track in inbox event log
# .chora/memory/events/inbox.jsonl:
# {"event": "coordination_decomposed", "coord_id": "coord-003", "beads_epic": "chora-base-epic1", ...}
```

### Integration with SAP-010 (A-MEM)

**Use Case**: Correlate beads tasks with A-MEM event traces

```bash
# Beads task includes trace_id for A-MEM correlation
bd create "Implement OAuth flow" \
  --priority 0 \
  --description "OAuth2 implementation\nTrace: oauth-impl-2025-11"

# A-MEM event log correlation:
# .chora/memory/events/development.jsonl:
# {"event": "task_started", "beads_id": "chora-base-a3f8", "trace_id": "oauth-impl-2025-11", ...}
# {"event": "code_written", "file": "auth.py", "trace_id": "oauth-impl-2025-11", ...}
# {"event": "task_completed", "beads_id": "chora-base-a3f8", "trace_id": "oauth-impl-2025-11", ...}
```

### Integration with SAP-009 (Agent Awareness)

**AGENTS.md Pattern**:
```markdown
# Task Tracking (SAP-015)

## Quick Check
- Run `bd ready --json` at session start to find work
- Claim task: `bd update {id} --status in_progress --assignee claude-code`
- Complete task: `bd close {id} --reason "{completion note}"`

## Dependencies
- Add blocker: `bd dep add {blocked_task} {blocker_task}`
- Check tree: `bd dep tree {task_id}`

## Workflows
- See [SAP-015 Awareness Guide](docs/skilled-awareness/task-tracking/awareness-guide.md)
```

---

## 9. Git Sync Workflows

### Auto-Sync (Default)

Beads automatically syncs with git:

```bash
# CRUD operation (create/update/close)
bd create "Task title"
# → Auto-exports to .beads/issues.jsonl after 5s debounce

# Git pull
git pull
# → Auto-imports from .beads/issues.jsonl if newer than SQLite DB

# Commit workflow
git add .beads/issues.jsonl
git commit -m "feat: Add tasks for feature X"
git push
# Other machines: `git pull` → auto-imports
```

### Manual Sync (Disabled Auto-Sync)

```bash
# Disable auto-sync
bd create "Task title" --no-auto-flush

# Manual export
bd export  # Writes .beads/issues.jsonl

# Manual import
bd import  # Reads .beads/issues.jsonl

# Git workflow
git add .beads/issues.jsonl
git commit -m "feat: Add tasks"
git push
```

### Protected Branch Workflow

For repositories with protected `main` branch (GitHub/GitLab):

```bash
# Initialize with separate metadata branch
bd init --branch beads-metadata

# Beads syncs to separate branch
git checkout beads-metadata
bd create "Task title"
git add .beads/issues.jsonl
git commit -m "task: Add new task"
git push origin beads-metadata

# Merge to main via PR
# (Protected branch rules enforced)
```

---

## 10. Programmatic Access

### JSON Output for Agents

Most commands support `--json` flag for machine parsing:

```bash
# Get ready work as JSON
bd ready --json
# Output: [{"id": "chora-base-a3f8", "title": "...", "priority": 0, ...}, ...]

# Get issue details as JSON
bd show chora-base-a3f8 --json
# Output: {"id": "chora-base-a3f8", "title": "...", "dependencies": [...], ...}

# Create and capture JSON response
bd create "Task title" --json
# Output: {"id": "chora-base-b2c4", "title": "Task title", "created_at": "...", ...}
```

### SQLite Database Extension

Applications can extend beads' SQLite database:

```sql
-- Example: Add execution tracking table
CREATE TABLE IF NOT EXISTS myapp_executions (
  id INTEGER PRIMARY KEY,
  issue_id TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  outcome TEXT,
  FOREIGN KEY (issue_id) REFERENCES issues(id)
);

-- Query tasks with execution data
SELECT i.id, i.title, e.outcome
FROM issues i
LEFT JOIN myapp_executions e ON i.id = e.issue_id
WHERE i.status = 'closed';
```

---

## 11. Configuration

### `.beads/config.yaml`

```yaml
# Project configuration
prefix: chora-base
repository_id: 5fdc72de
clone_id: 570c048adee21e19

# Auto-sync settings
auto_flush: true
flush_debounce_seconds: 5
auto_import: true

# Git integration
git_hooks_enabled: true
sync_branch: main  # or 'beads-metadata' for protected branches

# Daemon settings (optional background sync)
daemon_enabled: false
daemon_sync_interval_seconds: 60
```

### Environment Variables

```bash
# Override database path
export BEADS_DB=/path/to/custom.db

# Disable auto-sync
export BD_NO_AUTO_FLUSH=1
export BD_NO_AUTO_IMPORT=1

# Actor name for audit trail
export BD_ACTOR=claude-code
```

---

## 12. Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Database not found` | No `.beads/` directory | Run `bd init` in repository root |
| `Issue not found: {id}` | Invalid issue ID | Run `bd list` to see valid IDs |
| `Circular dependency detected` | Dependency cycle | Run `bd dep cycles` and break cycle |
| `Git conflict in issues.jsonl` | Concurrent updates | Resolve merge conflict manually (JSONL is line-based) |
| `Beads not in PATH` | npm package not installed | Run `npm install -g @beads/bd` |

### Validation

```bash
# Run comprehensive health check
bd doctor

# Validate database integrity
bd validate

# Check for dependency cycles
bd dep cycles

# Check git sync status
bd info
```

---

## 13. Performance Considerations

- **SQLite Cache**: Fast local queries (<10ms for typical operations)
- **JSONL Sync**: Git-friendly line-based format, minimal merge conflicts
- **Debouncing**: 5s debounce on auto-export reduces git churn
- **Hash IDs**: Collision-resistant (v0.20.1+), safe for multi-agent scenarios
- **Scaling**: Tested with 10,000+ issues in single database

---

## 14. Security & Privacy

- **Local Storage**: All data stored locally in `.beads/` directory
- **Git-Based**: No SaaS/cloud dependencies, full control
- **Gitignore**: SQLite cache auto-gitignored (only JSONL committed)
- **Access Control**: Repository access = beads access (git permissions)
- **No PII**: Issue metadata controlled by users (avoid sensitive data in titles/descriptions)

---

## 15. Versioning & Compatibility

- **Beads Version**: SAP-015 requires beads v0.21.6+ (current)
- **Hash IDs**: v0.20.1+ required for multi-agent safety
- **Breaking Changes**: Follow beads project changelog
- **Backward Compatibility**: JSONL format stable, SQLite schema versioned

---

## 16. Reference Materials

**Beads Documentation**:
- [GitHub Repository](https://github.com/steveyegge/beads)
- [npm Package](https://www.npmjs.com/package/@beads/bd)
- [Database Extension Guide](https://github.com/steveyegge/beads/blob/main/EXTENDING.md)

**Related SAP Documents**:
- [capability-charter.md](capability-charter.md) - SAP-015 charter
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide

**Chora-Base Integration**:
- [SAP-001: Inbox Coordination](../inbox/protocol-spec.md)
- [SAP-009: Agent Awareness](../agent-awareness/protocol-spec.md)
- [SAP-010: Memory System](../memory-system/protocol-spec.md)

---

**Version History**:
- **1.0.0** (2025-11-04): Initial protocol specification for beads integration
