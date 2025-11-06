---
title: "SAP-015 Multi-Agent Coordination Validation Guide"
created: 2025-11-06
updated: 2025-11-06
tags:
  - sap-015
  - multi-agent
  - validation
  - git-sync
  - beads
  - coordination
author: claude-code
status: documented
links:
  - "[[sap-010-015-integration-2025-11]]"
---

# SAP-015 Multi-Agent Coordination Validation Guide

## Overview

This guide documents how to validate SAP-015 (beads task tracking) for multi-agent coordination, enabling multiple agents (Claude Code, Claude Desktop, or human developers) to collaborate on shared task management via git synchronization.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   Multi-Agent Coordination                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Agent 1 (Claude Code)          Git Repo          Agent 2 (Desktop) │
│  ┌─────────────────┐         ┌──────────┐        ┌─────────────┐ │
│  │ .beads/         │         │  Remote  │        │ .beads/     │ │
│  │  beads.db       │──push──►│  issues. │◄──pull─│  beads.db   │ │
│  │  issues.jsonl   │         │  jsonl   │        │  issues.jsonl│ │
│  └─────────────────┘         └──────────┘        └─────────────┘ │
│         │                                                │         │
│         └────────────── Sync via git ──────────────────┘         │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **.beads/issues.jsonl** is the **source of truth** (git-committed)
2. **.beads/beads.db** is a **local cache** (gitignored, auto-regenerated)
3. **Hash-based task IDs** prevent collisions between agents
4. **Git hooks** auto-sync beads.db ↔ issues.jsonl on commit/checkout
5. **Pull before create** workflow prevents most conflicts

## Hash-Based ID Generation

### How It Works

When a task is created, beads generates an ID like `chora-base-a3f`:

```
Repository prefix: "chora-base"
+
Content hash (first 3 chars): "a3f" (from SHA-256 of task content)
=
Task ID: "chora-base-a3f"
```

### Collision Prevention

- **Probability of collision**: ~1 in 4,096 for same repo (16^3)
- **Content-based hashing**: Same task content = same ID (deterministic)
- **Different content**: Different hash = different ID
- **Cross-agent safety**: Agents creating different tasks get different IDs

### Example

```bash
# Agent 1 creates task
bd create --title "Fix bug #123" --description "Details..."
# Generated ID: chora-base-7x2

# Agent 2 creates different task
bd create --title "Add feature X" --description "Details..."
# Generated ID: chora-base-9k5  (different hash)

# No collision! Both tasks coexist safely.
```

## Validation Workflows

### Workflow 1: Parallel Task Creation

**Goal**: Prove agents can create tasks concurrently without conflicts

**Steps:**

```bash
# Agent 1 (Claude Code)
git pull
bd create --title "Task from Agent 1" --actor "claude-code"
git add .beads/issues.jsonl
git commit -m "Agent 1: Created task"
git push

# Agent 2 (Claude Desktop or human)
git pull
bd create --title "Task from Agent 2" --actor "claude-desktop"
git add .beads/issues.jsonl
git commit -m "Agent 2: Created task"
git push

# Both agents pull
git pull

# Verify both tasks exist
bd list
```

**Expected Result**:
- Both tasks visible to both agents
- No merge conflicts
- Stable, unique IDs

### Workflow 2: Dependency Coordination

**Goal**: Prove agents can coordinate via dependencies

**Steps:**

```bash
# Agent 1: Create design task
git pull
bd create --title "Design API" --description "Trace: api-project-v1"
# Gets ID: chora-base-abc
git add .beads/issues.jsonl
git commit -m "Agent 1: Design task"
git push

# Agent 2: Pull and create dependent task
git pull
bd list  # See design task
bd create --title "Implement API" --description "Trace: api-project-v1"
# Gets ID: chora-base-xyz
bd dep add chora-base-xyz chora-base-abc --type blocks
git add .beads/issues.jsonl
git commit -m "Agent 2: Implementation task (depends on design)"
git push

# Agent 1: Pull and see dependency
git pull
bd show chora-base-abc
# Shows: "Depended on by: chora-base-xyz"

# Agent 1: Complete design
bd close chora-base-abc --reason "Design complete"
git add .beads/issues.jsonl
git commit -m "Agent 1: Design complete"
git push

# Agent 2: Pull and see unblocked task
git pull
bd ready
# Shows: chora-base-xyz (now unblocked)
```

**Expected Result**:
- Dependencies tracked correctly across agents
- Ready state updates after blocker completion
- Full audit trail in git history

### Workflow 3: Concurrent Updates (Potential Conflict)

**Goal**: Test conflict resolution when both agents modify same task

**Steps:**

```bash
# Setup: Both agents have same task chora-base-abc

# Agent 1: Update task
git pull
bd update chora-base-abc --status in_progress
git add .beads/issues.jsonl
git commit -m "Agent 1: Started work"
# DON'T push yet

# Agent 2: Update same task
git pull  # Doesn't see Agent 1's change yet
bd comment chora-base-abc "Making progress"
git add .beads/issues.jsonl
git commit -m "Agent 2: Added comment"
git push

# Agent 1: Now push (will conflict)
git push
# Git rejects: "Updates were rejected"

# Agent 1: Resolve conflict
git pull
# Merge conflict in .beads/issues.jsonl
# Manually resolve (merge both changes)
git add .beads/issues.jsonl
git commit -m "Agent 1: Merged changes from Agent 2"
git push
```

**Expected Result**:
- Git detects conflict
- JSONL structure allows manual merging
- Both changes preserved after resolution

### Workflow 4: Audit Trail

**Goal**: Prove agent actions are traceable

**Steps:**

```bash
# Create task with actor attribution
bd create --title "My task" --actor "claude-code"

# View audit trail
bd show <task-id> --json | jq '{created_by: .created_by, updated_by: .updated_by}'

# Check git history
git log --oneline .beads/issues.jsonl
```

**Expected Result**:
- Actor attribution in task metadata
- Git commits show which agent made changes
- Full history reconstructable

## Validation Checklist

### Phase 4 Requirements

- [ ] **Parallel Creation**: Two agents create tasks concurrently → no conflicts
- [ ] **Git Sync**: Changes by Agent 1 visible to Agent 2 after pull
- [ ] **Hash IDs**: Task IDs stable across agents, no collisions observed
- [ ] **Dependency Coordination**: Agent 2 creates task depending on Agent 1's task
- [ ] **Ready State**: Completing blocker in Agent 1 unblocks Agent 2's task
- [ ] **Audit Trail**: Actor attribution shows which agent did what
- [ ] **Conflict Resolution**: Concurrent updates handled gracefully via git

### Live Testing Required

**Why**: This guide documents the theory, but live testing requires:
- Two agent instances (Claude Code + Claude Desktop, or two machines)
- Real git push/pull cycles
- Actual conflict scenarios

**Recommended Setup**:
1. Clone repo on two machines OR use two agent contexts
2. Run workflows 1-4 above
3. Document any issues or edge cases discovered
4. Update this guide with findings

## Multi-Agent Workflows

### Workflow: Team Sprint Planning

```bash
# Product Owner (Agent 1): Create epic
bd create --title "User Auth Feature" --type epic --priority 1

# Tech Lead (Agent 2): Break down into tasks
git pull
bd create --title "Design auth schema" --description "Trace: auth-v1"
bd create --title "Implement login API" --description "Trace: auth-v1"
bd create --title "Build login UI" --description "Trace: auth-v1"

# Add dependencies
bd dep add <login-api-id> <design-id> --type blocks
bd dep add <login-ui-id> <login-api-id> --type blocks

git add .beads/issues.jsonl
git commit -m "Tech Lead: Sprint tasks"
git push

# Developer 1 (Agent 3): Pull and start design
git pull
bd ready  # See design task (unblocked)
bd update <design-id> --status in_progress --actor "dev1"
```

### Workflow: Handoff Between Agents

```bash
# Morning Agent (Claude Code): Start work
bd ready
bd update <task-id> --status in_progress
bd comment <task-id> "Started implementation, DB schema designed"

# [Work happens, agent session ends]

git add .beads/issues.jsonl
git commit -m "Morning: Progress on task <task-id>"
git push

# Evening Agent (Claude Desktop or human): Continue
git pull
bd show <task-id>  # See morning's comment
bd comment <task-id> "Continuing implementation, added API endpoints"
bd close <task-id> --reason "Implementation complete"

git add .beads/issues.jsonl
git commit -m "Evening: Completed task <task-id>"
git push
```

## Integration with A-MEM (SAP-010)

Multi-agent coordination + A-MEM enables full traceability:

```bash
# Agent 1: Complete task and log to A-MEM
bd close chora-base-abc --reason "Task complete"

cat >> .chora/memory/events/development.jsonl << 'EOF'
{
  "event_type": "task_completed",
  "beads_task_id": "chora-base-abc",
  "trace_id": "api-project-v1",
  "completed_by": "claude-code",
  "timestamp": "2025-11-06T03:00:00Z"
}
EOF

git add .beads/issues.jsonl .chora/memory/events/development.jsonl
git commit -m "Agent 1: Task complete + A-MEM event"
git push

# Agent 2: Pull and query history
git pull
python scripts/a-mem-beads-correlation.py events-for-task --task-id chora-base-abc
# Shows: Task completed by claude-code at 03:00Z
```

## Known Limitations

### What Works

- ✅ Parallel task creation (different tasks)
- ✅ Git-based synchronization
- ✅ Hash-based collision prevention
- ✅ Dependency tracking across agents
- ✅ Audit trails via actor attribution

### What Requires Care

- ⚠️ **Concurrent updates**: Same task modified by 2 agents → git conflict
- ⚠️ **Pull discipline**: Agents must `git pull` before creating tasks
- ⚠️ **Large teams**: >10 agents might need coordination workflow
- ⚠️ **Offline work**: Conflicts accumulate, require manual merge

### Mitigations

1. **Pull-before-create**: Always `git pull` before `bd create`
2. **Task ownership**: Assign tasks to reduce concurrent updates
3. **Comment-first**: Use `bd comment` instead of updating status
4. **Regular sync**: Automate `git pull` via cron or IDE hooks

## Success Criteria (L3)

For SAP-015 L3 Production status, multi-agent coordination must demonstrate:

- [x] **Architecture documented**: This guide ✅
- [ ] **Live validation**: 2+ agents tested in practice
- [ ] **Conflict resolution**: Documented conflict scenarios + resolutions
- [ ] **Performance**: <5s sync time for 100 tasks
- [ ] **Adoption**: Used by ≥2 agents in ≥2 projects

**Status**: Documented, awaiting live validation

## Next Steps

1. **Live test**: Run workflows 1-4 with 2 agent instances
2. **Document results**: Update this guide with findings
3. **Edge cases**: Test large task lists (>100 tasks)
4. **Performance**: Measure git sync + db rebuild times
5. **Iterate**: Improve workflow based on real-world usage

## References

- [Beads Demo: Multi-Agent](../../../examples/beads-demo-multiagent/README.md)
- [SAP-015 Protocol Spec](../../../docs/skilled-awareness/task-tracking/protocol-spec.md)
- [SAP-010 + SAP-015 Integration](sap-010-015-integration-2025-11.md)
- [Git Hooks Documentation](../../../.beads/git-hooks/)

---

**Status**: 📝 Documented, awaiting live validation
**Phase**: 4/5 (Multi-agent coordination)
**L3 Criterion**: Architecture complete, live testing pending
