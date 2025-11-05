# Adoption Blueprint: Agent Task Tracking with Beads

**SAP ID**: SAP-015
**Version**: 1.0.0
**Estimated Time**: 15-30 minutes
**Skill Level**: Beginner
**Last Updated**: 2025-11-04

---

## Overview

This blueprint guides you through adopting beads task tracking in your chora-base project or existing repository. By the end, you'll have:

- ✅ Beads CLI installed and verified
- ✅ Repository initialized with beads (`.beads/` directory)
- ✅ Git hooks configured for automatic sync
- ✅ First tasks created and tracked
- ✅ AGENTS.md updated with beads workflows
- ✅ Integration with existing SAPs (inbox, A-MEM) documented

---

## Prerequisites

Before starting, ensure you have:

- [x] Git repository initialized
- [x] Node.js 18+ installed (`node --version`)
- [x] npm available (`npm --version`)
- [x] Git configured (`git config user.name` and `git config user.email`)
- [x] Familiarity with command line

**Optional** (for integrations):
- [ ] SAP-001 (inbox) adopted (for coordination integration)
- [ ] SAP-010 (A-MEM) adopted (for event correlation)
- [ ] SAP-009 (agent-awareness) adopted (for AGENTS.md patterns)

---

## Installation Steps

### Step 1: Install Beads CLI

**Install via npm:**

```bash
npm install -g @beads/bd
```

**Verify installation:**

```bash
bd version
# Expected output: bd version 0.21.6 (or later)
```

**Troubleshooting:**

If `bd` command not found:
```bash
# Check npm global bin directory
npm config get prefix

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(npm config get prefix)/bin"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

**Alternative installation methods:**

<details>
<summary>Homebrew (macOS/Linux)</summary>

```bash
brew tap steveyegge/beads
brew install bd
```
</details>

<details>
<summary>Manual installation</summary>

```bash
# Download from releases
curl -L https://github.com/steveyegge/beads/releases/latest/download/bd-$(uname -s)-$(uname -m) -o bd

# Make executable
chmod +x bd

# Move to PATH
sudo mv bd /usr/local/bin/

# Verify
bd version
```
</details>

---

### Step 2: Initialize Beads in Repository

**Navigate to repository root:**

```bash
cd /path/to/your/project
```

**Initialize beads:**

```bash
bd init
```

**Expected output:**
```
Repository ID: 5fdc72de
  Clone ID: 570c048adee21e19

✓ bd initialized successfully!

  Database: .beads/beads.db
  Issue prefix: your-project
  Issues will be named: your-project-1, your-project-2, ...

Install git hooks now? [Y/n]
```

**Answer Yes** to install git hooks (recommended).

**Verify initialization:**

```bash
ls -la .beads/
# Expected files:
# beads.db (SQLite cache, gitignored)
# issues.jsonl (empty, committed)
# config.yaml (project config, committed)
# metadata.json (repo metadata, committed)
# .gitignore (ignores *.db files)
```

**Check git hooks:**

```bash
ls -la .git/hooks/
# Should see: pre-commit, post-merge
```

**Run health check:**

```bash
bd doctor
# Expected: All checks pass
```

**Custom prefix (optional):**

If auto-detected prefix is not ideal:
```bash
bd rename-prefix new-prefix
```

**Protected branch setup (GitHub/GitLab):**

If your `main` branch is protected:
```bash
# Re-initialize with separate metadata branch
bd init --branch beads-metadata

# Beads will sync to beads-metadata branch instead of main
```

---

### Step 3: Commit Initial Beads Setup

**Stage beads files:**

```bash
git add .beads/
```

**Commit:**

```bash
git commit -m "chore: Initialize beads task tracking (SAP-015)"
```

**Push:**

```bash
git push
```

**Verify in git:**

```bash
git log --oneline -1
# Should show commit with beads initialization

git ls-files .beads/
# Should show:
# .beads/.gitignore
# .beads/config.yaml
# .beads/issues.jsonl
# .beads/metadata.json
```

---

### Step 4: Create First Tasks

**Create initial task:**

```bash
bd create "Set up project task tracking" \
  --priority 0 \
  --description "Initialize beads and create first tasks for project management"
```

**Create a few more tasks:**

```bash
bd create "Document beads workflow in README" --priority 1
bd create "Update AGENTS.md with beads patterns" --priority 1
bd create "Train team on beads usage" --priority 2
```

**View created tasks:**

```bash
bd list
```

**Expected output:**
```
your-project-a3f8  open  P0  Set up project task tracking
your-project-b2c4  open  P1  Document beads workflow in README
your-project-c5d6  open  P1  Update AGENTS.md with beads patterns
your-project-d7e9  open  P2  Train team on beads usage
```

**Add dependencies (example):**

```bash
# "Train team" depends on "Document workflow" and "Update AGENTS.md"
bd dep add your-project-d7e9 your-project-b2c4
bd dep add your-project-d7e9 your-project-c5d6
```

**Check ready work:**

```bash
bd ready
# Should show tasks with no blockers
```

**Commit tasks:**

```bash
git add .beads/issues.jsonl
git commit -m "task: Add initial project tasks"
git push
```

---

### Step 5: Update AGENTS.md (SAP-009 Integration)

**Add beads section to AGENTS.md:**

```bash
cat >> AGENTS.md <<'EOF'

## Task Tracking (SAP-015)

### Quick Reference

**Session Start:**
- `bd ready --json` — Find unblocked work
- `bd update {id} --status in_progress --assignee {agent}` — Claim task
- `bd show {id} --json` — Get task context

**During Work:**
- `bd create "Task title" --priority 0` — Add discovered subtask
- `bd dep add {blocked} {blocker}` — Link dependency

**Session End:**
- `bd close {id} --reason "Completed X"` — Mark done
- `bd ready --json` — Check newly-unblocked work

**Status Check:**
- `bd list --status in_progress --json` — Active tasks
- `bd dep tree {id}` — Visualize dependencies

### When to Use Beads

✅ **Use for:**
- Complex features (5+ steps spanning multiple sessions)
- Tasks with dependencies (what blocks what)
- Multi-agent coordination
- Feature decomposition (epics → subtasks)

❌ **Don't use for:**
- Cross-repo coordination (use SAP-001 inbox)
- Event history (use SAP-010 A-MEM)
- Simple single-step tasks

### Full Documentation

See [SAP-015 Awareness Guide](docs/skilled-awareness/task-tracking/awareness-guide.md)

EOF
```

**Commit:**

```bash
git add AGENTS.md
git commit -m "docs: Add beads task tracking patterns to AGENTS.md"
git push
```

---

### Step 6: Optional Integrations

#### Integration with SAP-001 (Inbox Coordination)

If you have inbox adopted, document how to decompose coordination requests into beads tasks:

```bash
cat >> docs/skilled-awareness/task-tracking/INTEGRATION.md <<'EOF'
# Beads Integration with Inbox (SAP-001)

## Pattern: Decompose Coordination Request into Tasks

When receiving coordination request in inbox:

1. Create epic for coordination:
   ```bash
   bd create "COORD-{year}-{num}: {title}" --priority 0 --type epic
   ```

2. Create subtasks based on requirements

3. Link to epic with parent-child relationships

4. Log in A-MEM event log:
   ```bash
   echo '{"event": "coordination_decomposed", "coord_id": "coord-003", "beads_epic": "{epic_id}", "timestamp": "..."}' >> .chora/memory/events/inbox.jsonl
   ```

5. Move coordination to active in inbox

See [Awareness Guide Pattern H](awareness-guide.md#pattern-h-integration-with-inbox-sap-001)
EOF
```

#### Integration with SAP-010 (A-MEM)

Document event correlation:

```bash
cat >> docs/skilled-awareness/task-tracking/INTEGRATION.md <<'EOF'

# Beads Integration with A-MEM (SAP-010)

## Pattern: Correlate Tasks with Event Traces

1. Include trace ID in task description:
   ```bash
   bd create "Task title" --description "Task details\n\nTrace: {trace_id}"
   ```

2. Log task events in A-MEM:
   ```bash
   # Task start
   echo '{"event": "task_started", "beads_id": "{id}", "trace_id": "{trace}", ...}' >> .chora/memory/events/development.jsonl

   # Task complete
   echo '{"event": "task_completed", "beads_id": "{id}", "trace_id": "{trace}", ...}' >> .chora/memory/events/development.jsonl
   ```

3. Close task with trace reference:
   ```bash
   bd close {id} --reason "Completed, trace: {trace_id}"
   ```

See [Awareness Guide Pattern I](awareness-guide.md#pattern-i-integration-with-a-mem-sap-010)
EOF
```

**Commit integrations:**

```bash
git add docs/skilled-awareness/task-tracking/INTEGRATION.md
git commit -m "docs: Add beads integration patterns with inbox and A-MEM"
git push
```

---

### Step 7: Test Agent Workflows

**Test Pattern A: Session Start**

```bash
# Simulate agent starting session
bd ready --json
bd update {first_ready_id} --status in_progress --assignee test-agent
bd show {first_ready_id} --json
```

**Test Pattern B: Task Completion**

```bash
bd close {task_id} --reason "Test completion"
bd ready --json  # Check for newly-unblocked work
```

**Test Pattern C: Discovering Subtasks**

```bash
# Create subtask
bd create "Test subtask" --priority 0

# Link as blocker
bd dep add {parent_id} {subtask_id}

# Verify parent now blocked
bd ready  # Parent should not appear

# Complete subtask
bd close {subtask_id}

# Verify parent now ready
bd ready  # Parent should appear
```

**Verify all tests pass:**

```bash
bd validate
bd doctor
```

---

### Step 8: Update README (Optional)

Add beads section to project README:

```markdown
## Task Tracking

This project uses [beads](https://github.com/steveyegge/beads) for persistent task tracking across agent sessions (SAP-015).

### Quick Start

```bash
# Find work
bd ready

# Claim task
bd update {id} --status in_progress --assignee {your-name}

# Complete task
bd close {id} --reason "Completed X"
```

### Documentation

- [SAP-015 Adoption Blueprint](docs/skilled-awareness/task-tracking/adoption-blueprint.md)
- [SAP-015 Awareness Guide](docs/skilled-awareness/task-tracking/awareness-guide.md)
- [SAP-015 Protocol Spec](docs/skilled-awareness/task-tracking/protocol-spec.md)

```

---

### Step 9: Register Adoption in Ledger

Report your adoption in the SAP-015 ledger:

```bash
# See Step 10 for ledger update instructions
```

---

## Verification Checklist

Before completing adoption, verify:

- [ ] `bd version` works (v0.21.6+)
- [ ] `.beads/` directory exists with 4+ files
- [ ] `.beads/issues.jsonl` committed to git
- [ ] `.beads/beads.db` gitignored (NOT committed)
- [ ] Git hooks installed (`.git/hooks/pre-commit`, `post-merge`)
- [ ] `bd doctor` passes all checks
- [ ] `bd ready` shows ready tasks
- [ ] `bd list` shows all tasks
- [ ] AGENTS.md includes beads patterns (if SAP-009 adopted)
- [ ] Integration documented (if SAP-001 or SAP-010 adopted)
- [ ] At least 3 test tasks created
- [ ] Team members aware of beads workflow

---

## Quick Reference: Common Commands

```bash
# === DAILY WORKFLOWS ===
bd ready --json                                    # Find work
bd update {id} --status in_progress --assignee me  # Claim
bd close {id} --reason "Done"                      # Complete

# === TASK MANAGEMENT ===
bd create "Title" --priority 0                     # New task
bd list --status open                              # View backlog
bd show {id} --json                                # Task details
bd update {id} --priority 0                        # Update priority

# === DEPENDENCIES ===
bd dep add {blocked} {blocker}                     # Add dependency
bd dep tree {id}                                   # Visualize tree
bd dep cycles                                      # Detect cycles
bd dep remove {blocked} {blocker}                  # Remove dependency

# === STATUS & MAINTENANCE ===
bd status                                          # Database overview
bd info                                            # Paths and sizes
bd doctor                                          # Health check
bd validate                                        # Integrity check

# === GIT WORKFLOW ===
git add .beads/issues.jsonl                        # Stage tasks
git commit -m "task: {message}"                    # Commit
git push                                           # Share
git pull                                           # Sync (auto-imports)
```

---

## Troubleshooting

### Issue: `bd: command not found`

**Solution:**
```bash
npm install -g @beads/bd
export PATH="$PATH:$(npm config get prefix)/bin"
source ~/.bashrc
```

### Issue: `Database not found`

**Solution:**
```bash
cd /path/to/repo/root
bd init
```

### Issue: Git hooks not installed

**Solution:**
```bash
bd init  # Re-run, it will reinstall hooks
# Or manually:
# .beads should contain install script, run it
```

### Issue: Merge conflict in `.beads/issues.jsonl`

**Solution:**
```bash
# Resolve conflict markers in .beads/issues.jsonl
# Each line should be valid JSON
# Save file
bd import  # Re-import to SQLite
bd validate  # Verify integrity
```

### Issue: Tasks not syncing across machines

**Solution:**
```bash
# Ensure issues.jsonl committed
git add .beads/issues.jsonl
git commit -m "task: Sync tasks"
git push

# On other machine
git pull  # Auto-imports
bd list  # Verify tasks appear
```

---

## Next Steps

After adoption:

1. **Practice Workflows**: Use beads for next 2-3 features to build muscle memory
2. **Train Team**: Share awareness guide with team members
3. **Integrate with Existing SAPs**: Add inbox and A-MEM integration if applicable
4. **Provide Feedback**: Report issues or suggestions in SAP-015 ledger
5. **Monitor Adoption**: Track time savings and workflow improvements

---

## Support & Resources

**Documentation:**
- [SAP-015 Capability Charter](capability-charter.md)
- [SAP-015 Protocol Spec](protocol-spec.md)
- [SAP-015 Awareness Guide](awareness-guide.md)
- [SAP-015 Ledger](ledger.md)

**Beads Project:**
- [GitHub Repository](https://github.com/steveyegge/beads)
- [npm Package](https://www.npmjs.com/package/@beads/bd)
- [Issues & Feature Requests](https://github.com/steveyegge/beads/issues)

**Chora-Base:**
- [SAP Framework](../sap-framework/)
- [Inbox Coordination (SAP-001)](../inbox/)
- [Agent Awareness (SAP-009)](../agent-awareness/)
- [Memory System (SAP-010)](../memory-system/)

---

**Version History:**
- **1.0.0** (2025-11-04): Initial adoption blueprint for beads integration
