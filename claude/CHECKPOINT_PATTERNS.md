# Checkpoint Patterns for Claude

**Purpose:** State preservation and session continuity across Claude development sessions.

**Problem Solved:** Context loss between sessions, difficulty resuming work, lost decisions, wasted rework.

---

## Overview

Checkpoints are **structured snapshots of development state** that enable:

- **Session continuity** - Resume work seamlessly after breaks
- **Team handoffs** - Transfer context to other developers
- **Decision preservation** - Never lose architectural decisions
- **Progress tracking** - Historical record of development journey
- **Recovery** - Rollback to known-good states

**Without checkpoints:** Start from scratch, repeat analysis, lose context, waste time

**With checkpoints:** Load state, continue immediately, preserve decisions, save hours

---

## Checkpoint File Format

### Standard CLAUDE_CHECKPOINT.md Template

```markdown
# Claude Session Checkpoint

## Metadata
- **Date:** YYYY-MM-DD HH:MM
- **Session Duration:** X hours
- **Task:** [High-level task description]
- **Status:** 🔄 In Progress | ✅ Complete | ⚠️ Blocked
- **Completion:** XX%

---

## Completed Work

✅ **Task 1:** [Description]
   - Files: [list]
   - Outcome: [specific result]
   - Time: [duration]

✅ **Task 2:** [Description]
   - Files: [list]
   - Outcome: [specific result]
   - Time: [duration]

---

## In Progress

🔄 **Current Task:** [Description]
   - **Status:** XX% complete
   - **Files:** [list of active files]
   - **Progress:**
     - ✅ Completed: [subtask 1]
     - ✅ Completed: [subtask 2]
     - 🔄 In progress: [subtask 3] (details)
     - ⬜ Pending: [subtask 4]

---

## Key Decisions

### Decision 1: [Title]
- **What:** [Decision made]
- **Why:** [Rationale]
- **Alternatives considered:** [list]
- **Impact:** [consequences]
- **Documented in:** [path to ADR or design doc]

### Decision 2: [Title]
- **What:** [Decision made]
- **Why:** [Rationale]
- **Alternatives considered:** [list]
- **Impact:** [consequences]

---

## Code State

### File: src/module.py
```python
# Lines 1-100: ✅ Complete - Core implementation
# Lines 101-150: 🔄 In progress - Error handling
# Lines 151-200: ⬜ Not started - Edge cases
# TODO Line 125: Add timeout handling
# FIXME Line 143: Test failure - needs investigation
```

### File: tests/test_module.py
```python
# Lines 1-50: ✅ Complete - Happy path tests
# Lines 51-100: 🔄 In progress - Error case tests
# Coverage: 75% (target: 85%)
```

---

## Next Steps

**Immediate (next session):**
1. [ ] Complete error handling in src/module.py (lines 101-150)
2. [ ] Fix test failure at test_module.py:143
3. [ ] Add edge case handling (lines 151-200)

**Soon (this week):**
4. [ ] Integration tests
5. [ ] Documentation update
6. [ ] Code review

**Later (next sprint):**
7. [ ] Performance optimization
8. [ ] Additional error scenarios

---

## Context for Continuation

### Essential Context (load immediately)
- **Files:**
  - src/module.py (main work)
  - tests/test_module.py (test suite)
  - dev-docs/design/feature-design.md (reference)

- **Commands:**
  ```bash
  # Load current state
  pytest tests/test_module.py -v
  git diff src/module.py
  ```

### Extended Context (load if needed)
- **Related modules:**
  - src/related_module.py (integration point)
  - src/utils/helpers.py (shared utilities)

- **Documentation:**
  - dev-docs/workflows/TDD_WORKFLOW.md
  - AGENTS.md (architecture section)

---

## Known Issues

### Issue 1: Test Flakiness
- **Where:** tests/test_module.py:143
- **Symptom:** Intermittent failure on `test_async_operation`
- **Hypothesis:** Race condition in async test
- **Attempted:** Added asyncio.sleep(), didn't help
- **Next:** Try async context manager pattern

### Issue 2: Performance Concern
- **Where:** src/module.py:87 (database query)
- **Symptom:** Slow with large datasets (>10k records)
- **Impact:** Not blocking, but needs optimization
- **Deferred to:** Next sprint (logged in backlog)

---

## Blockers

⚠️ **Blocker 1:** Waiting for API documentation
- **Blocking:** Integration test implementation
- **Owner:** External team
- **ETA:** End of week
- **Workaround:** Mock API for now

---

## Learnings

### Technical Insights
1. **Pattern:** Using `async with` prevents race conditions in async tests
   - Applied in: tests/test_module.py:167
   - Reference: [link or knowledge graph ID]

2. **Library:** FastAPI's dependency injection simplifies testing
   - Will use for remaining endpoints
   - Example: src/api/endpoints.py:45

### Process Insights
1. **TDD saved time:** Writing tests first revealed design issue early
   - Prevented: 2-3 hours of refactoring
   - Validated: Continue TDD for remaining work

---

## Team Notes

### For Code Reviewer
- Focus review on error handling (lines 101-150)
- Security concern: Input validation at line 125 (addressed with validator)
- Performance note: Query optimization deferred to next sprint

### For Future Me
- Remember to update API docs after completing error handling
- Test coverage threshold is 85% - currently at 75%
- Performance optimization story created: PROJ-456

---

## Session Metrics

- **Lines written:** ~150
- **Tests added:** 12
- **Defects found:** 1 (test flakiness)
- **Decisions made:** 2
- **Time saved:** ~2 hours (vs manual approach)
- **Satisfaction:** 8/10 (blocked on API docs, otherwise smooth)

---

**Checkpoint Version:** 1.0
**Created by:** Claude + [Developer Name]
**Next Checkpoint:** When error handling complete or end of day
```

**Save to:** `.chora/memory/claude-checkpoints/YYYY-MM-DD-[feature].md`

---

## Checkpoint Patterns by Scenario

### Pattern 1: End-of-Day Checkpoint

**When:** End of coding session
**Purpose:** Enable smooth start tomorrow

```markdown
"Create end-of-day checkpoint:

Session summary:
- Worked on: [task]
- Completed: [list]
- In progress: [current subtask at XX%]
- Blocked by: [if any]

Key decisions:
- [Decision 1 with rationale]

Tomorrow's plan:
- Start with: [specific next step]
- Load files: [list]

Save to: .chora/memory/claude-checkpoints/$(date +%Y-%m-%d)-feature.md"
```

### Pattern 2: Mid-Task Checkpoint (Context Pruning)

**When:** Context getting full, need to prune
**Purpose:** Preserve state before losing context

```markdown
"Context is filling up. Create checkpoint before pruning:

Current state:
- Task: [description] (XX% complete)
- Files: [active files]
- Progress: [detailed status]
- Recent decisions: [list]

After checkpoint:
- Prune: Completed tasks, old discussions
- Keep: Current task, active files, decisions

Checkpoint: .chora/memory/claude-checkpoints/$(date +%H%M)-pruning.md"
```

### Pattern 3: Team Handoff Checkpoint

**When:** Transferring work to another developer
**Purpose:** Enable seamless continuation by someone else

```markdown
"Team handoff checkpoint:

## For [Next Developer Name]

### What I Completed
- [List with file paths and outcomes]

### What's In Progress
- [Current task with detailed state]
- [Specific files and line numbers]

### What You Need to Know
1. Architecture decision: [with rationale]
2. Known issue: [with workaround]
3. Don't forget: [important detail]

### How to Continue
1. Load files: [list]
2. Read: [relevant docs]
3. Start with: [specific next step]
4. If stuck: [resources or contacts]

### Questions to Consider
- [Open question 1]
- [Open question 2]

Checkpoint: .chora/memory/claude-checkpoints/handoff-to-[name].md"
```

### Pattern 4: Milestone Checkpoint

**When:** Completing major feature phase
**Purpose:** Document achievement, prepare for next phase

```markdown
"Milestone checkpoint: [Phase] Complete

## Achievement Summary
- ✅ All acceptance criteria met
- ✅ Tests passing (coverage: XX%)
- ✅ Code reviewed and approved
- ✅ Documentation updated

## Metrics
- Duration: [time]
- LOC: [count]
- Tests: [count]
- Defects: [count]

## Learnings
- [Key insights]
- [Process improvements]

## Next Phase
- Objective: [description]
- Approach: [strategy]
- Estimated: [time]

Checkpoint: .chora/memory/claude-checkpoints/milestone-[phase]-complete.md"
```

---

## Checkpoint Automation

### Automated Checkpoint Triggers

**Configure Claude to auto-checkpoint:**

```markdown
"Please create automatic checkpoints when:
1. Every 10 interactions
2. Before context pruning
3. At end of each 2-hour session
4. After completing each subtask
5. Before switching tasks

Format: Use standard CLAUDE_CHECKPOINT.md template
Location: .chora/memory/claude-checkpoints/auto-[timestamp].md"
```

### Git Integration

**Commit checkpoints with code:**

```bash
# After creating checkpoint
git add .chora/memory/claude-checkpoints/
git commit -m "checkpoint: [feature] - [status]

Session summary: [brief]
Completed: [list]
Next: [action]

Checkpoint: .chora/memory/claude-checkpoints/[file].md"
```

---

## Recovery Patterns

### Pattern: Resume After Interruption

```markdown
"Resuming work from checkpoint:

Checkpoint file: .chora/memory/claude-checkpoints/2025-10-26-feature.md

Summary from checkpoint:
- Task: [from checkpoint]
- Status: [XX% from checkpoint]
- Last completed: [from checkpoint]
- Next step: [from checkpoint]

Load essential context:
- [Files from checkpoint]
- [Decisions from checkpoint]

Continue from: [specific line/step from checkpoint]"
```

### Pattern: Rollback to Known-Good State

```markdown
"Issue with current approach. Rolling back to checkpoint:

Checkpoint: .chora/memory/claude-checkpoints/2025-10-25-before-refactor.md

Reason for rollback:
- Current approach: [problem]
- Better approach: [alternative]

Restore state:
- Revert files: [list]
- Reapply: [decisions to keep]
- Restart from: [checkpoint state]

New checkpoint: Will create after exploring alternative"
```

---

## Checkpoint Best Practices

### ✅ Do's

1. **Create frequently** - Every 10 interactions or 2 hours
2. **Be specific** - Include file paths, line numbers, exact states
3. **Record decisions** - Always capture "why" not just "what"
4. **Include metrics** - Time spent, progress %, satisfaction
5. **Plan next steps** - Concrete actions for continuation
6. **Save to git** - Track checkpoint evolution
7. **Use templates** - Consistent structure aids recovery

### ❌ Don'ts

1. **Skip checkpoints** - "I'll remember" → you won't
2. **Be vague** - "Working on feature" vs "Implementing error handling lines 101-150"
3. **Forget decisions** - Lost rationale leads to rework
4. **Ignore blockers** - Document what's blocking progress
5. **Skip learnings** - Insights are valuable for future work
6. **Inconsistent format** - Use template for easy parsing

---

## Checkpoint Metrics

**Track these to optimize:**

- **Checkpoint frequency** = Checkpoints / Session hours
  - Target: 0.5-1 per hour

- **Recovery success rate** = Successful resumes / Total resumes
  - Target: >90%

- **Time to resume** = Minutes from checkpoint load to productive work
  - Target: <5 minutes

- **Rework prevented** = Hours saved by decision preservation
  - Target: >2 hours per checkpoint

---

## Integration with Other Patterns

**With Context Management:**
- Create checkpoint before pruning context
- Include context loading strategy in checkpoint

**With Metrics Tracking:**
- Record session metrics in checkpoint
- Track checkpoint effectiveness as ROI metric

**With Knowledge Graph:**
- Reference knowledge graph IDs in decisions
- Create knowledge notes from checkpoint learnings

---

## Checkpoint Storage Strategy

### File Organization

```
.chora/memory/claude-checkpoints/
├── 2025-10-26-feature-auth.md          # Daily feature checkpoints
├── 2025-10-26-1430-pruning.md          # Mid-session pruning checkpoints
├── milestone-sprint-5-complete.md       # Milestone checkpoints
├── handoff-to-alice.md                  # Team handoff checkpoints
└── archive/
    └── 2025-10/                         # Archived by month
        ├── 2025-10-20-feature-x.md
        └── ...
```

### Retention Policy

- **Active checkpoints:** Last 30 days (quick access)
- **Archived checkpoints:** Monthly folders (historical reference)
- **Milestone checkpoints:** Never delete (permanent record)

---

## Troubleshooting

### Problem: Checkpoint Too Long to Load

**Solution:** Create summary checkpoint
```markdown
"Summarize checkpoint [file] to essentials:
- Task and status
- Key decisions only
- Next 3 steps
- Essential files only

Save as: [file]-summary.md"
```

### Problem: Can't Find Relevant Checkpoint

**Solution:** Index checkpoints
```bash
# Create index
ls .chora/memory/claude-checkpoints/ | \
  grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' | \
  xargs -I {} sh -c 'echo "- {}: $(head -n 5 .chora/memory/claude-checkpoints/{} | grep "Task:")"'
```

### Problem: Checkpoint Out of Sync with Code

**Solution:** Validate before loading
```bash
# Check if checkpoint matches current state
git diff --name-only $(git log --grep='checkpoint' -1 --format=%H)
```

---

**See Also:**
- [CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md) - Context loading strategies for checkpoints
- [FRAMEWORK_TEMPLATES.md](FRAMEWORK_TEMPLATES.md) - Task templates with checkpoint integration

---

**Version:** 3.3.0
**Pattern Maturity:** ⭐⭐⭐ Production-ready
**Last Updated:** 2025-10-26
