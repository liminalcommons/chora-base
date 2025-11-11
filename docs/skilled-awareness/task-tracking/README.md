# SAP-015: Task Tracking (Beads)

**Version:** 1.0.0 | **Status:** Pilot | **Maturity:** Phase 1

> Git-native task tracking for AI agents with `bd` CLI—persistent memory across sessions (hours, days, weeks), dependency-aware ready-work detection, and multi-agent coordination via `.beads/issues.jsonl`.

---

## Quick Start (5 minutes)

```bash
# Initialize beads in repository
bd init

# Create task
bd create "Implement user authentication" --priority high

# Find ready work (no blockers)
bd ready --json
# Output: [{"id": "PROJ-001", "title": "Implement user authentication", ...}]

# Claim task
bd update PROJ-001 --status in_progress --assignee me

# Add blocker (PROJ-001 blocks PROJ-002)
bd create "Add login UI" --blocked-by PROJ-001

# Complete task
bd close PROJ-001 --reason "Implemented authentication with NextAuth"

# Query backlog
bd list --status open --priority high --json
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for beads setup (5-min read)

---

## What Is It?

SAP-015 provides **git-native task tracking** using the `bd` CLI tool (beads). It stores tasks in `.beads/issues.jsonl` (committed to git) with SQLite cache (`.beads/beads.db`, gitignored) for fast queries. AI agents can find ready work, manage dependencies, and coordinate across sessions spanning hours, days, or weeks.

**Key Innovation**: **Git-native + dependency-aware** - Tasks survive context resets, session restarts, and git push/pull cycles. Agents automatically detect ready work (open issues with no blocking dependencies) for efficient session startup.

---

## When to Use

Use SAP-015 when you need to:

1. **Session persistence** - Restore task context after hours, days, or weeks
2. **Multi-session work** - Track progress across multiple agent sessions
3. **Dependency management** - Link tasks with blocks, parent-child, related relationships
4. **Multi-agent coordination** - Share tasks via git (agents on different machines)
5. **Backlog management** - Prioritize work, assign tasks, track status

**Not needed for**: Single-session work (<1 hour), or if project requires no task tracking

---

## Key Features

- ✅ **Git-Native Storage** - `.beads/issues.jsonl` (committed), `.beads/beads.db` (gitignored cache)
- ✅ **Dependency-Aware** - Automatic ready-work detection (no blockers)
- ✅ **Multi-Agent Coordination** - Share tasks via git push/pull
- ✅ **Hash-Based IDs** - `PROJ-xxx` format (v0.20.1+) prevents collisions
- ✅ **Session Persistence** - Tasks survive context resets and restarts
- ✅ **JSON Output** - `--json` flags for programmatic parsing
- ✅ **5-Second Sync** - Automatic JSONL ↔ SQLite sync (debounced)
- ✅ **Git Hooks** - Auto-commit tasks on branch operations
- ✅ **CLI-First Design** - `bd` command with 12+ operations

---

## Common Workflows

### Core Commands

#### **bd init** - Initialize Beads

```bash
bd init
# Creates:
# - .beads/issues.jsonl (task source of truth)
# - .beads/beads.db (SQLite cache, gitignored)
# - .beads/config.yaml (project configuration)
# - .beads/metadata.json (repository metadata)
# - .beads/.gitignore (ignore SQLite files)

# Prompts for:
# - Project prefix (e.g., "PROJ" → tasks named PROJ-001, PROJ-002, etc.)
# - Git hooks (optional, auto-commit tasks on branch switch)
```

---

#### **bd create** - Create Task

```bash
bd create TITLE [OPTIONS]

# Examples:
bd create "Add user authentication"
bd create "Fix login bug" --priority high
bd create "Add tests" --blocked-by PROJ-001
bd create "Refactor auth" --assignee alice --tags refactor,auth
bd create "Document API" --parent PROJ-001  # Child task

# Options:
# --priority: low|medium|high (default: medium)
# --assignee: username (default: unassigned)
# --tags: comma-separated tags
# --blocked-by: task ID that blocks this task
# --parent: parent task ID (for subtasks)
# --description: detailed description (optional)

# Output:
# Created: PROJ-003 "Add user authentication"
```

---

#### **bd ready** - Find Ready Work

```bash
bd ready [OPTIONS]

# Examples:
bd ready                                    # Show ready work (human-readable)
bd ready --json                             # JSON output for agents
bd ready --priority high                    # Filter by priority
bd ready --assignee me                      # Filter by assignee

# Output (JSON):
[
  {
    "id": "PROJ-001",
    "title": "Add user authentication",
    "status": "open",
    "priority": "high",
    "assignee": null,
    "created": "2025-11-09T12:00:00Z",
    "blocking_count": 2
  }
]

# Output (human-readable):
# Ready Work (2 tasks)
# ====================
# PROJ-001 [HIGH] Add user authentication (blocks 2 tasks)
# PROJ-004 [MEDIUM] Write API documentation
```

**Use Case**: Session startup - find unblocked work to resume immediately

---

#### **bd list** - Query Tasks

```bash
bd list [OPTIONS]

# Examples:
bd list                                     # All tasks
bd list --status open                       # Open tasks only
bd list --status closed                     # Completed tasks
bd list --priority high                     # High-priority tasks
bd list --assignee alice                    # Tasks assigned to alice
bd list --tags auth,security                # Tasks with specific tags
bd list --json                              # JSON output for agents

# Output (JSON):
[
  {
    "id": "PROJ-001",
    "title": "Add user authentication",
    "status": "open",
    "priority": "high",
    "assignee": "alice",
    "tags": ["auth", "security"],
    "created": "2025-11-09T12:00:00Z",
    "updated": "2025-11-09T14:30:00Z",
    "blocks": ["PROJ-002", "PROJ-003"],
    "blocked_by": [],
    "parent": null,
    "children": ["PROJ-005"]
  }
]
```

---

#### **bd show** - Show Task Details

```bash
bd show TASK_ID [OPTIONS]

# Examples:
bd show PROJ-001                            # Human-readable details
bd show PROJ-001 --json                     # JSON output for agents

# Output (JSON):
{
  "id": "PROJ-001",
  "title": "Add user authentication",
  "description": "Implement NextAuth v5 with Google OAuth provider",
  "status": "in_progress",
  "priority": "high",
  "assignee": "alice",
  "tags": ["auth", "security"],
  "created": "2025-11-09T12:00:00Z",
  "updated": "2025-11-09T14:30:00Z",
  "closed": null,
  "blocks": ["PROJ-002", "PROJ-003"],
  "blocked_by": [],
  "parent": null,
  "children": ["PROJ-005"],
  "history": [
    {"timestamp": "2025-11-09T12:00:00Z", "action": "created", "user": "alice"},
    {"timestamp": "2025-11-09T14:30:00Z", "action": "status_changed", "from": "open", "to": "in_progress"}
  ]
}
```

---

#### **bd update** - Update Task

```bash
bd update TASK_ID [OPTIONS]

# Examples:
bd update PROJ-001 --status in_progress     # Claim task
bd update PROJ-001 --assignee alice         # Assign to alice
bd update PROJ-001 --priority high          # Increase priority
bd update PROJ-001 --add-tag urgent         # Add tag
bd update PROJ-001 --remove-tag wontfix     # Remove tag

# Options:
# --status: open|in_progress|blocked|closed
# --assignee: username
# --priority: low|medium|high
# --add-tag: add tag
# --remove-tag: remove tag
# --description: update description
```

---

#### **bd close** - Complete Task

```bash
bd close TASK_ID [OPTIONS]

# Examples:
bd close PROJ-001                           # Close without reason
bd close PROJ-001 --reason "Implemented NextAuth authentication"
bd close PROJ-001 --resolution completed    # Explicit resolution

# Options:
# --reason: completion reason (recommended)
# --resolution: completed|wontfix|duplicate (default: completed)

# Side Effects:
# - Sets status to "closed"
# - Unblocks dependent tasks
# - Adds close event to history
```

---

#### **bd block** - Manage Dependencies

```bash
# Add blocker
bd block TASK_ID --blocked-by BLOCKER_ID

# Examples:
bd block PROJ-002 --blocked-by PROJ-001    # PROJ-001 blocks PROJ-002
bd block PROJ-003 --blocked-by PROJ-001    # PROJ-001 blocks PROJ-003

# Remove blocker
bd unblock TASK_ID --blocked-by BLOCKER_ID

# Examples:
bd unblock PROJ-002 --blocked-by PROJ-001  # Remove blocker

# Side Effects:
# - Updates task relationships
# - Affects ready-work detection (bd ready)
```

---

#### **bd delete** - Delete Task

```bash
bd delete TASK_ID

# Examples:
bd delete PROJ-001                          # Delete task

# Warning: Permanent operation, use sparingly
# Recommended: Use `bd close --resolution wontfix` instead
```

---

### Workflow Patterns

#### **Pattern 1: Session Startup (Context Restoration)**

**Goal**: Find unblocked work to resume immediately

```bash
# 1. Find ready work
bd ready --json | jq -r '.[0] | "\(.id): \(.title)"'
# Output: PROJ-001: Add user authentication

# 2. Show task details
bd show PROJ-001 --json | jq .

# 3. Claim task
bd update PROJ-001 --status in_progress --assignee me

# 4. Resume work with full context
```

**ROI**: 2-5 minutes saved per session vs manual task discovery

---

#### **Pattern 2: Multi-Session Work (Progress Tracking)**

**Goal**: Track progress across sessions spanning days/weeks

```bash
# Session 1 (Monday):
bd create "Implement authentication" --priority high
bd update PROJ-001 --status in_progress
# ... work for 2 hours ...
bd update PROJ-001 --description "Completed OAuth setup, pending UI"

# Session 2 (Wednesday):
bd ready --json | jq -r '.[0] | "\(.id): \(.title)"'
# Output: PROJ-001: Implement authentication
bd show PROJ-001 --json | jq .description
# Output: "Completed OAuth setup, pending UI"
# ... work for 3 hours ...
bd close PROJ-001 --reason "Implemented authentication with NextAuth"
```

---

#### **Pattern 3: Dependency Management (Blockers)**

**Goal**: Link tasks with dependency relationships

```bash
# Create parent task
bd create "User authentication feature" --priority high
# Output: PROJ-001

# Create dependent tasks (blocked by PROJ-001)
bd create "Add login UI" --blocked-by PROJ-001
bd create "Add profile page" --blocked-by PROJ-001

# Query ready work (PROJ-001 is ready, others blocked)
bd ready
# Output: PROJ-001 "User authentication feature" (blocks 2 tasks)

# Complete parent task (unblocks dependents)
bd close PROJ-001

# Query ready work again (dependents now ready)
bd ready
# Output:
# PROJ-002 "Add login UI"
# PROJ-003 "Add profile page"
```

---

#### **Pattern 4: Multi-Agent Coordination (Git-Based)**

**Goal**: Share tasks across agents via git

```bash
# Agent 1 (Machine 1):
bd create "Add authentication" --assignee agent2
git add .beads/issues.jsonl
git commit -m "chore: Add authentication task"
git push

# Agent 2 (Machine 2):
git pull
bd ready --assignee agent2 --json
# Output: [{"id": "PROJ-001", "title": "Add authentication", "assignee": "agent2"}]
bd update PROJ-001 --status in_progress
# ... work ...
bd close PROJ-001
git add .beads/issues.jsonl
git commit -m "chore: Complete authentication task"
git push

# Agent 1 (Machine 1):
git pull
bd show PROJ-001 --json | jq .status
# Output: "closed"
```

---

## Integration

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-001** (Inbox) | Coordination Decomposition | Decompose coordination requests into beads tasks |
| **SAP-010** (A-MEM) | Event Correlation | Link tasks to events via `trace_id` |
| **SAP-012** (Lifecycle) | Phase 2 Planning | Sprint plans → beads tasks |
| **SAP-013** (Metrics) | Velocity Tracking | Sprint velocity from task completion rates |
| **SAP-027** (Dogfooding) | Pilot Tracking | Track pilot candidates as beads tasks |

**Cross-SAP Workflow Example**:
```bash
# 1. Receive coordination request (SAP-001)
just inbox-query-incoming
# COORD-2025-011: "Add real-time sync to MCP server"

# 2. Decompose into tasks (SAP-015)
bd create "Research real-time sync options" --trace-id COORD-2025-011
bd create "Implement Socket.IO" --trace-id COORD-2025-011 --blocked-by PROJ-001
bd create "Add tests" --trace-id COORD-2025-011 --blocked-by PROJ-002
bd create "Update documentation" --trace-id COORD-2025-011 --blocked-by PROJ-003

# 3. Work on tasks (SAP-015)
bd ready --json | jq -r '.[0].id'
# PROJ-001 (no blockers)
bd update PROJ-001 --status in_progress
# ... research ...
bd close PROJ-001

# 4. Log events (SAP-010)
echo '{"timestamp":"'$(date -Iseconds)'","event_type":"milestone","description":"Completed research","trace_id":"COORD-2025-011"}' >> .chora/memory/events/development.jsonl

# 5. Track velocity (SAP-013)
bd list --status closed --created-after 2025-11-01 | wc -l
# 4 tasks completed this week (velocity metric)
```

---

## Success Metrics

- **Session Startup**: 2-5 minutes saved per session (ready-work vs manual discovery)
- **Context Restoration**: 80-90% faster than re-reading docs
- **Multi-Session Work**: 100% task persistence across restarts
- **Dependency Tracking**: Automatic ready-work detection (no manual blocking checks)
- **Multi-Agent Coordination**: Git-native sharing (no external DB required)

---

## Troubleshooting

### Problem 1: .beads/ Directory Doesn't Exist

**Solution**: Initialize beads in repository:
```bash
bd init
# Creates .beads/ with issues.jsonl, beads.db, config.yaml, metadata.json
```

---

### Problem 2: bd ready Shows No Tasks Despite Open Tasks

**Solution**: Check for blocking dependencies:
```bash
bd list --status open --json | jq '.[] | select(.blocked_by | length > 0) | {id, title, blocked_by}'
# Shows tasks blocked by other tasks

# Resolve by completing blocking tasks or removing dependency:
bd unblock PROJ-002 --blocked-by PROJ-001
```

---

### Problem 3: SQLite Cache Out of Sync with JSONL

**Solution**: Beads auto-syncs every 5 seconds, but manual sync available:
```bash
# Force JSONL → SQLite sync
bd sync

# Or delete cache (regenerates from JSONL)
rm .beads/beads.db
bd list  # Regenerates cache
```

---

### Problem 4: Multi-Agent Task ID Collisions

**Solution**: Upgrade to beads v0.20.1+ for hash-based IDs:
```bash
# Check beads version
bd --version

# Upgrade if <v0.20.1
pip install --upgrade beads

# Hash-based IDs prevent collisions:
# PROJ-abc (hash) vs PROJ-001 (sequential)
```

---

## Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete beads technical specification (26KB, 13-min read)
- **[AGENTS.md](AGENTS.md)** - Agent beads workflows (20KB, 10-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code beads patterns (16KB, 8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Beads setup guide (14KB, 7-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

---

**Version History**:
- **1.0.0** (2025-11-04) - Initial beads integration with git-native storage, dependency-aware ready-work, multi-agent coordination

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
