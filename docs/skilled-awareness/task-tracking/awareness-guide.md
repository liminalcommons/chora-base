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

## 4. Common Mistakes & Corrections

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

## 5. Troubleshooting

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

## 6. Best Practices

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

## 7. Quick Reference Card

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

## 8. Integration Checklist

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

## 9. Training Exercises

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
