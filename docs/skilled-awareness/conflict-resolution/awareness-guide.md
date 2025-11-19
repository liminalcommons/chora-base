# SAP-053: Conflict Resolution - Awareness Guide for AI Agents

**Document Type**: Awareness Guide
**SAP ID**: SAP-053
**SAP Name**: Conflict Resolution
**Version**: 1.0.0 (Phase 1 - Design)
**Status**: Draft
**Created**: 2025-11-18
**Last Updated**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper

---

## Document Purpose

This awareness guide provides **practical workflows** for AI agents to handle merge conflicts efficiently using SAP-053 tools and patterns.

**Audience**: AI agents (Claude, GitHub Copilot, etc.) working in chora ecosystem projects

**What you'll find here**:
1. **Quick reference workflows** - Step-by-step processes for common scenarios
2. **Decision trees** - Choose the right resolution strategy
3. **Tool reference** - Justfile recipes and script usage
4. **Best practices** - Patterns for efficient conflict resolution
5. **Integration patterns** - How SAP-053 works with SAP-051, SAP-052, SAP-010

---

## Quick Start: 5-Minute Conflict Resolution Workflow

**Scenario**: You're about to create a PR and want to check for conflicts first.

```bash
# Step 1: Check for conflicts (before creating PR)
just conflict-check

# Step 2: If conflicts detected, check if auto-resolvable
just conflict-check-json | jq '.auto_resolvable'

# Step 3: Auto-resolve safe conflicts
just conflict-auto-resolve

# Step 4: Manually resolve remaining conflicts
just conflict-resolve <file>

# Step 5: Verify resolution
git status
git diff --check

# Step 6: Commit and push
git push
```

**Time**: 2-5 minutes (auto-resolvable) or 10-20 minutes (manual review)

---

## 1. Agent Workflows

### Workflow 1: Pre-PR Conflict Check (Proactive)

**When**: Before creating a pull request
**Goal**: Detect conflicts early, before CI/CD or code review
**Time**: 2-5 minutes

**Steps**:

1. **Check for conflicts**:
   ```bash
   just conflict-check main
   ```

   **Output**:
   ```
   Conflict Check Results:

   ✅ No conflicts detected with main branch
   Safe to create PR.
   ```

   OR

   ```
   ⚠️  Conflicts detected in 3 files:
   - docs/vision/mcp.md (content conflict)
   - poetry.lock (lockfile conflict)
   - .DS_Store (metadata conflict)

   Auto-resolvable: 2 files (poetry.lock, .DS_Store)
   Manual review: 1 file (docs/vision/mcp.md)
   ```

2. **If no conflicts**: Proceed with PR creation

3. **If conflicts detected**: Assess auto-resolvability
   ```bash
   just conflict-check-json | jq '.auto_resolvable'
   # true = some/all conflicts are auto-resolvable
   # false = all conflicts require manual review
   ```

4. **Auto-resolve safe conflicts**:
   ```bash
   just conflict-auto-resolve
   ```

   **Output**:
   ```
   ✅ Resolved: poetry.lock (regenerated)
   ✅ Resolved: .DS_Store (deleted)
   ⏭️  Skipped: docs/vision/mcp.md (manual review needed)

   1 file remaining for manual resolution.
   ```

5. **Manually resolve remaining conflicts**:
   ```bash
   just conflict-resolve docs/vision/mcp.md
   ```

   **Interactive output**:
   ```
   Conflict in: docs/vision/mcp.md
   Strategy: MANUAL_REVIEW
   Owner: @victorpiper (from CODEOWNERS)

   Conflict markers found:
   <<<<<<< HEAD
   ## MCP Server Architecture (v2.0)
   =======
   ## MCP Server Design (v1.5)
   >>>>>>> feature/new-docs

   Options:
   1. Accept ours (HEAD)
   2. Accept theirs (feature/new-docs)
   3. Edit manually
   4. Contact owner (@victorpiper)
   5. Escalate to pair programming

   Your choice (1-5):
   ```

6. **Verify resolution**:
   ```bash
   git status
   git diff --check  # Check for remaining conflict markers
   ```

7. **Commit resolution** (if not auto-committed):
   ```bash
   git add docs/vision/mcp.md
   git commit -m "Resolve conflict in docs/vision/mcp.md

   Chose version from feature/new-docs (more complete architecture).

   Reviewed-by: @victorpiper (CODEOWNERS)
   "
   ```

8. **Log to A-MEM** (automatic if using `just conflict-resolve`):
   ```json
   {
     "type": "conflict_resolved",
     "resolved_files": ["docs/vision/mcp.md"],
     "resolution_time_minutes": 8.5,
     "strategy": "MANUAL_REVIEW",
     "owner_consulted": "@victorpiper"
   }
   ```

9. **Create PR** (now conflict-free):
   ```bash
   git push
   gh pr create --title "Add MCP server documentation" --body "..."
   ```

**Benefits**:
- Conflicts resolved before PR creation (faster review)
- CI/CD passes on first run (no rebase delays)
- Code reviewers see clean diff (better review quality)

---

### Workflow 2: CI/CD Conflict Detection (Reactive)

**When**: GitHub Actions detects conflicts in PR
**Goal**: Fix conflicts quickly to unblock merge
**Time**: 5-15 minutes

**Steps**:

1. **Pull latest changes**:
   ```bash
   git fetch origin
   git checkout feature/my-branch
   ```

2. **Check CI/CD output**:
   ```
   ❌ Conflicts detected in 2 files
   - project-docs/sprints/sprint-13.md
   - justfile

   Download conflict report: [conflict-report.json]
   ```

3. **Download conflict report** (if available):
   ```bash
   gh run download <run-id> -n conflict-report
   cat conflict-report.json | jq
   ```

4. **Run conflict check locally**:
   ```bash
   just conflict-check main
   ```

5. **Resolve conflicts** (follow Workflow 1, steps 4-8)

6. **Push fix**:
   ```bash
   git push --force-with-lease
   # Force push needed because you've rebased/merged main
   ```

7. **Verify CI/CD passes**:
   ```bash
   gh pr checks --watch
   ```

**Benefits**:
- Quick resolution (unblock reviewers)
- Automated conflict report (no manual investigation)
- CI/CD re-runs automatically

---

### Workflow 3: Recurring Conflict Pattern Detection (Preventive)

**When**: Weekly or monthly (preventive maintenance)
**Goal**: Identify high-conflict files and create prevention strategies
**Time**: 10-20 minutes

**Steps**:

1. **Query A-MEM for conflicts** (last 90 days):
   ```bash
   grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
     jq -r '.resolved_files[]' | \
     sort | uniq -c | sort -rn | head -10
   ```

   **Output**:
   ```
   5 project-docs/sprints/sprint-13.md
   3 docs/vision/mcp.md
   2 feature-manifest.yaml
   1 justfile
   ```

2. **Create knowledge notes for recurring patterns** (≥2 conflicts):
   ```bash
   just conflict-patterns
   ```

   **Output**:
   ```
   Detecting conflict patterns...

   ✅ Created knowledge note: .chora/memory/knowledge/notes/conflict-pattern-sprint-13.md
   ✅ Created knowledge note: .chora/memory/knowledge/notes/conflict-pattern-mcp-vision.md

   2 patterns documented.
   ```

3. **Review knowledge notes**:
   ```bash
   cat .chora/memory/knowledge/notes/conflict-pattern-sprint-13.md
   ```

   **Content**:
   ```markdown
   # Conflict Pattern: project-docs/sprints/sprint-13.md

   **Conflict Frequency**: 5 conflicts in last 90 days
   **Average Resolution Time**: 18.3 minutes

   ## Prevention Recommendations

   1. **Coordinate before editing** (SAP-052 multi-developer pattern)
      - File is 🔴 HIGH risk (active sprint plan)
      - Communicate before editing: "Working on sprint-13.md for 30 min"

   2. **Use feature branches for major updates**
      - Small updates: Edit on main (with communication)
      - Large refactors: Use feature branch, merge after sprint end

   3. **Split sprint plan into separate files** (future enhancement)
      - Current: Single sprint-13.md (5 conflicts)
      - Proposed: Split into sprint-13-tasks.md, sprint-13-retrospective.md
      - Reduces conflict surface area (each developer edits different file)
   ```

4. **Implement prevention strategies**:
   - Update CLAUDE.md with high-risk file warnings
   - Add communication triggers to team workflow
   - Refactor high-conflict files (if patterns suggest)

5. **Monitor metrics** (next quarter):
   ```bash
   just conflict-stats days=90
   ```

   **Expected improvement**: 30-50% reduction in recurring conflicts

**Benefits**:
- Proactive conflict prevention (reduces time wasted)
- Knowledge accumulation (patterns become institutional knowledge)
- Continuous improvement (quarterly metrics show progress)

---

### Workflow 4: Conflict Risk Prediction (Before Editing)

**When**: Before editing a file (especially high-traffic files)
**Goal**: Assess conflict risk and coordinate if needed
**Time**: 1-2 minutes

**Steps**:

1. **Stage files you plan to edit**:
   ```bash
   git add project-docs/sprints/sprint-13.md
   ```

2. **Predict conflict risk**:
   ```bash
   just conflict-predict
   ```

   **Output**:
   ```
   Conflict Risk Prediction:

   📄 project-docs/sprints/sprint-13.md
      Risk: 🔴 HIGH (85%)
      Reason: 12 commits in last 30 days, 5 conflicts in last 90 days, 2 active contributors
      Recommendation: Communicate with @victorpiper before editing

   Next Steps:
   1. Message colleague: "I'm working on sprint-13.md for 30 minutes"
   2. Wait for acknowledgment
   3. Edit file
   4. Commit and push promptly (don't leave uncommitted overnight)
   5. Message colleague: "Sprint-13.md updated, safe to edit now"
   ```

3. **Follow recommendation**:
   - 🔴 HIGH risk → Always communicate before editing
   - 🟡 MEDIUM risk → Communicate if colleague might be editing
   - 🟢 LOW risk → Proceed normally

4. **If HIGH risk, communicate**:
   ```
   [Slack/Discord message]
   "Working on sprint-13.md for next 30 minutes (updating task statuses)"
   ```

5. **Edit file after acknowledgment**

6. **Commit and push promptly**:
   ```bash
   git add project-docs/sprints/sprint-13.md
   git commit -m "Update sprint 13 task statuses"
   git push
   ```

7. **Signal completion**:
   ```
   [Slack/Discord message]
   "Sprint-13.md updated, safe to edit now"
   ```

**Benefits**:
- Prevents 80% of conflicts (proactive coordination)
- Fast coordination (1-2 min vs 10-20 min resolving conflict)
- Builds team awareness (everyone knows who's working where)

---

## 2. Decision Trees

### Decision Tree 1: Conflict Detection

**Question**: "How should I check for conflicts?"

```
Start
│
├─ Have you made commits on your branch?
│  ├─ NO → Skip conflict check (nothing to merge)
│  └─ YES → Continue
│
├─ Are you about to create a PR?
│  ├─ YES → Run `just conflict-check` (proactive)
│  └─ NO → Continue
│
├─ Did CI/CD report conflicts?
│  ├─ YES → Download conflict-report.json, run `just conflict-check` locally
│  └─ NO → Continue
│
├─ Are you editing a high-risk file? (See SAP-052 Conflict Risk Matrix)
│  ├─ YES → Run `just conflict-predict` first
│  └─ NO → Standard workflow (check before PR)
│
└─ Default: Run `just conflict-check` before creating PR
```

---

### Decision Tree 2: Resolution Strategy Selection

**Question**: "Which resolution strategy should I use?"

```
Conflict detected in file X
│
├─ What file type?
│  ├─ .md (Markdown) → MANUAL_REVIEW
│  ├─ .py, .ts, .js (Code) → Check conflict type
│  │  ├─ Whitespace/formatting? → AUTO_RESOLVE_FORMATTING
│  │  └─ Content? → MANUAL_REVIEW_WITH_OWNERSHIP
│  ├─ .yaml, .json (Config) → Check schema availability
│  │  ├─ Schema available? → SCHEMA_DRIVEN_MERGE
│  │  └─ No schema? → MANUAL_REVIEW
│  ├─ package-lock.json, poetry.lock (Lockfile) → REGENERATE_FROM_SOURCE
│  ├─ .DS_Store, __pycache__ (Metadata) → DELETE_AND_REGENERATE
│  └─ Unknown → MANUAL_REVIEW (conservative default)
│
├─ Auto-resolvable strategies:
│  ├─ AUTO_RESOLVE_FORMATTING → Run `just conflict-auto-resolve`
│  ├─ SCHEMA_DRIVEN_MERGE → Run `just conflict-auto-resolve`
│  ├─ REGENERATE_FROM_SOURCE → Run `just conflict-resolve-lockfile <file>`
│  └─ DELETE_AND_REGENERATE → Run `just conflict-auto-resolve`
│
└─ Manual strategies:
   ├─ MANUAL_REVIEW → Run `just conflict-resolve <file>`
   └─ MANUAL_REVIEW_WITH_OWNERSHIP → Check CODEOWNERS, contact owner
```

---

### Decision Tree 3: Escalation Path

**Question**: "I'm stuck resolving a conflict. What should I do?"

```
Conflict resolution in progress
│
├─ How long have you been stuck?
│  ├─ <10 minutes → Continue trying (normal resolution time)
│  ├─ 10-30 minutes → Review strategy (are you using the right approach?)
│  └─ >30 minutes → Escalate to Level 2
│
├─ Level 1: Developer Resolution (you)
│  ├─ Can you determine correct version?
│  │  ├─ YES → Resolve and commit
│  │  └─ NO → Escalate to Level 2
│  │
│  ├─ Is there a file owner (CODEOWNERS)?
│  │  ├─ YES → Contact owner (Level 2)
│  │  └─ NO → Escalate to peer developer (Level 2)
│
├─ Level 2: Pair Programming
│  ├─ Schedule 30-minute pairing session
│  ├─ Review conflict together
│  ├─ Resolved within 1 hour?
│  │  ├─ YES → Document decision, commit
│  │  └─ NO → Escalate to Level 3
│  │
│  ├─ Fundamental design disagreement?
│  │  └─ YES → Escalate to Level 3 immediately
│
└─ Level 3: Project Lead Arbitration
   ├─ Provide context: file, conflict, both versions, rationale
   ├─ Project lead reviews and makes final decision (24 hours)
   └─ Decision is binding → Implement and commit
```

---

### Decision Tree 4: When to Create Knowledge Note

**Question**: "Should I create a knowledge note for this conflict?"

```
Conflict resolved
│
├─ Is this a recurring conflict? (≥2 times in 90 days)
│  ├─ YES → Create knowledge note
│  └─ NO → Continue
│
├─ Did resolution take >20 minutes?
│  ├─ YES → Consider creating knowledge note (pattern may emerge)
│  └─ NO → Skip (quick resolution, unlikely to recur)
│
├─ Does the conflict reveal a structural issue?
│  │  (e.g., file organization, domain ownership, coordination gap)
│  ├─ YES → Create knowledge note + escalate to project improvement
│  └─ NO → Skip
│
├─ Is this a cross-domain conflict requiring consensus?
│  ├─ YES → Create knowledge note documenting consensus protocol
│  └─ NO → Skip
│
└─ Default: Run `just conflict-patterns` weekly to auto-detect recurring patterns
```

---

## 3. Tool Reference

### 3.1 Justfile Recipes (Quick Reference)

| Recipe | Purpose | Output | Exit Code |
|--------|---------|--------|-----------|
| `just conflict-check` | Detect conflicts with main | Text summary | 0=none, 1=conflicts |
| `just conflict-check-json` | Detect conflicts (JSON) | JSON report | 0=none, 1=conflicts |
| `just conflict-predict` | Predict risk for staged files | Risk levels (LOW/MED/HIGH) | 0=always |
| `just conflict-resolve <file>` | Interactive resolution | Guided prompts | 0=resolved, 1=failed |
| `just conflict-auto-resolve` | Auto-resolve safe conflicts | Resolution summary | 0=all resolved, 1=some failed |
| `just conflict-resolve-lockfile <file>` | Regenerate lockfile | Regeneration log | 0=success, 1=failed |
| `just conflict-patterns` | Detect recurring patterns | Knowledge notes created | 0=always |
| `just conflict-history <file>` | Query conflict history | A-MEM events | 0=always |
| `just conflict-stats` | Conflict metrics | Stats dashboard | 0=always |

**Common Workflows**:

```bash
# Before PR: Check and resolve
just conflict-check && just conflict-auto-resolve

# After CI/CD failure: Full resolution
just conflict-check && just conflict-auto-resolve && git push --force-with-lease

# Weekly maintenance: Pattern detection
just conflict-patterns && just conflict-stats

# Before editing high-risk file: Risk check
git add <file> && just conflict-predict
```

---

### 3.2 Python Scripts (Advanced Usage)

**All scripts follow this pattern**:
```bash
python3 scripts/<script>.py --format <text|json> [--verbose]
```

**Available scripts**:

| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `conflict-checker.py` | Detect conflicts | `--branch <branch>`, `--format <text\|json>` |
| `conflict-resolver.py` | Interactive resolution | `--file <file>`, `--interactive` |
| `conflict-auto-resolver.py` | Auto-resolve safe conflicts | `--format <text\|json>` |
| `conflict-predictor.py` | Predict conflict risk | `--files <files>`, `--format <text\|json>` |
| `conflict-pattern-detector.py` | Detect recurring patterns | `--days <days>` (default: 90) |
| `conflict-stats.py` | Generate metrics | `--days <days>`, `--format <text\|json>` |

**Example Usage**:

```bash
# Detect conflicts (JSON output for CI/CD)
python3 scripts/conflict-checker.py --branch main --format json > report.json

# Auto-resolve with verbose output
python3 scripts/conflict-auto-resolver.py --format text --verbose

# Predict risk for specific files
python3 scripts/conflict-predictor.py \
  --files project-docs/sprints/sprint-13.md docs/vision/mcp.md \
  --format json
```

---

### 3.3 A-MEM Query Patterns

**Query 1: Recent conflicts (last 30 days)**
```bash
grep '"type": "conflict_resolved"' .chora/memory/events/2025-11.jsonl | \
  jq 'select(.timestamp > (now - 30*86400 | todate))'
```

**Query 2: Conflicts for specific file**
```bash
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq 'select(.resolved_files[] | contains("sprint-13.md"))'
```

**Query 3: Average resolution time by strategy**
```bash
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq -r '[.resolution_strategies[], .resolution_time_minutes] | @tsv' | \
  awk '{sum[$1]+=$2; count[$1]++} END {for (s in sum) printf "%s: %.1f min\n", s, sum[s]/count[s]}'
```

**Query 4: Escalation rate (Level 2+ / Total)**
```bash
TOTAL=$(grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | wc -l)
ESCALATED=$(grep '"escalation_level": [23]' .chora/memory/events/*.jsonl | wc -l)
echo "Escalation rate: $(echo "scale=1; $ESCALATED / $TOTAL * 100" | bc)%"
```

---

## 4. Best Practices

### Best Practice 1: Always Check Before Creating PR

**Why**: Resolve conflicts before code review (faster merge, cleaner CI/CD)

**Implementation**:
```bash
# Add to your PR creation script
#!/bin/bash
# scripts/create-pr.sh

# Step 1: Check for conflicts
just conflict-check

if [ $? -eq 1 ]; then
    echo "❌ Conflicts detected. Resolve before creating PR."
    echo "Run 'just conflict-auto-resolve' for quick fixes."
    exit 1
fi

# Step 2: Create PR
gh pr create --title "$1" --body "$2"
```

**Time Saved**: 10-20 minutes per PR (avoid rebase delays)

---

### Best Practice 2: Auto-Resolve First, Manual Second

**Why**: Save 70-80% of conflict resolution time by handling easy conflicts automatically

**Workflow**:
```bash
# Step 1: Auto-resolve safe conflicts
just conflict-auto-resolve

# Output:
# ✅ Resolved: 3 files (poetry.lock, .DS_Store, scripts/format.py)
# ⏭️  Skipped: 1 file (docs/README.md)

# Step 2: Manually resolve remaining
just conflict-resolve docs/README.md
```

**Time Saved**: 5-10 minutes per conflict set

---

### Best Practice 3: Coordinate Before Editing High-Risk Files

**Why**: Prevent conflicts before they happen (80% prevention rate)

**High-Risk Files** (from SAP-052 Conflict Risk Matrix):
- 🔴 HIGH: `.chora/memory/events/*.jsonl`, `project-docs/sprints/*.md`, `inbox/incoming/coordination/*.json`
- 🟡 MEDIUM: `justfile`, `AGENTS.md`, `CLAUDE.md`

**Workflow**:
```bash
# Before editing high-risk file
git add project-docs/sprints/sprint-13.md
just conflict-predict

# Output shows 🔴 HIGH risk
# → Communicate before editing

# After editing
git commit && git push
# → Signal completion
```

**Time Saved**: 10-20 minutes per conflict avoided

---

### Best Practice 4: Log All Resolutions to A-MEM

**Why**: Build conflict pattern library for continuous improvement

**Implementation** (automatic if using `just conflict-resolve`):
```python
# scripts/conflict-resolver.py

def resolve_conflict(file, strategy):
    start_time = time.time()

    # ... resolution logic ...

    # Log to A-MEM
    log_event({
        "type": "conflict_resolved",
        "resolved_files": [file],
        "resolution_time_minutes": (time.time() - start_time) / 60,
        "strategy": strategy
    })
```

**Benefit**: Quarterly metrics show continuous improvement

---

### Best Practice 5: Create Knowledge Notes for Recurring Patterns

**Why**: Capture institutional knowledge, prevent future conflicts

**Automation**:
```bash
# Weekly cron job (or manual)
just conflict-patterns
```

**Manual Creation** (for unique patterns):
```bash
# After resolving complex conflict
cat > .chora/memory/knowledge/notes/conflict-pattern-custom.md <<EOF
---
title: "Conflict Pattern: Feature Manifest Schema Changes"
tags: [conflict-pattern, schema-evolution]
---

# Pattern

When updating feature-manifest schema, conflicts occur in 40% of cases
because multiple developers add features simultaneously.

## Prevention

1. **Announce schema changes** in team chat before committing
2. **Use feature flags** for schema migrations (gradual rollout)
3. **Coordinate schema updates** weekly (batch changes)

## Resolution

Schema validation ensures correctness. Use SCHEMA_DRIVEN_MERGE strategy.
EOF
```

**Benefit**: 30-50% reduction in recurring conflicts (from SAP-053 ROI estimate)

---

## 5. Integration Patterns

### 5.1 SAP-051 (Git Workflow) Integration

**Pre-Push Hook** (`.git/hooks/pre-push`):

```bash
#!/bin/bash
# SAP-053: Conflict detection before push

echo "Checking for conflicts..."
just conflict-check-json > /tmp/conflict-report.json

HAS_CONFLICTS=$(jq -r '.has_conflicts' /tmp/conflict-report.json)
AUTO_RESOLVABLE=$(jq -r '.auto_resolvable' /tmp/conflict-report.json)

if [ "$HAS_CONFLICTS" = "true" ]; then
    if [ "$AUTO_RESOLVABLE" = "true" ]; then
        echo "⚠️  Auto-resolvable conflicts detected."
        echo "Run 'just conflict-auto-resolve' before pushing."
        exit 0  # Allow push with warning
    else
        echo "❌ Conflicts detected. Resolve before pushing."
        exit 1  # Block push
    fi
fi

echo "✅ No conflicts detected."
exit 0
```

**Installation**:
```bash
# Automatic installation (SAP-051 adoption)
cp .git/hooks/pre-push.sample .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

---

### 5.2 SAP-052 (Ownership Zones) Integration

**Conflict Resolution with Owner Jurisdiction**:

```bash
# Step 1: Identify file owner
just ownership-suggest-reviewers-staged

# Output:
# Suggested reviewers: @victorpiper
# Domains: documentation, scripts
# Jurisdiction: Single domain (documentation owner has jurisdiction)

# Step 2: Contact owner for guidance
# (if conflict in their domain)

# Step 3: Resolve following owner's expertise
just conflict-resolve docs/vision/mcp.md

# Step 4: Commit with owner acknowledgment
git commit -m "Resolve conflict in mcp.md

Merged architecture updates from both branches.

Reviewed-by: @victorpiper (CODEOWNERS, documentation domain)
"
```

**Owner Jurisdiction Rules** (from SAP-052):
- **Single domain conflict**: Domain owner has jurisdiction
- **Cross-domain conflict**: All owners collaborate (consensus)
- **Deadlock**: Escalate to project lead (Level 3)

---

### 5.3 SAP-010 (A-MEM) Integration

**Automatic Event Logging**:

All conflict resolution tools (`just conflict-resolve`, `just conflict-auto-resolve`) automatically log events to `.chora/memory/events/`:

```json
{
  "timestamp": "2025-11-18T14:32:15Z",
  "type": "conflict_detected",
  "conflicting_files": ["docs/vision/mcp.md"],
  "auto_resolvable": false
}

{
  "timestamp": "2025-11-18T14:45:32Z",
  "type": "conflict_resolved",
  "resolved_files": ["docs/vision/mcp.md"],
  "resolution_time_minutes": 13.3,
  "strategy": "MANUAL_REVIEW",
  "owner_consulted": "@victorpiper"
}
```

**Query for Insights**:

```bash
# Average resolution time (last 90 days)
just conflict-stats days=90

# Recurring patterns
just conflict-patterns

# File-specific history
just conflict-history docs/vision/mcp.md
```

---

## 6. Common Scenarios and Solutions

### Scenario 1: Lockfile Conflict (Common)

**Problem**: `poetry.lock` has conflicts after both developers update dependencies

**Solution** (1-2 minutes):
```bash
# Step 1: Regenerate lockfile
just conflict-resolve-lockfile poetry.lock

# Step 2: Verify dependencies
poetry check

# Step 3: Done (auto-committed)
```

**Why This Works**: Lockfiles are deterministic (generated from `pyproject.toml`). Regenerating incorporates both sets of dependency updates.

---

### Scenario 2: Sprint Plan Conflict (Frequent)

**Problem**: Both developers updated `project-docs/sprints/sprint-13.md` (active sprint plan)

**Solution** (10-15 minutes):
```bash
# Step 1: Check who owns the file
just ownership-suggest-reviewers-staged

# Output: @victorpiper (project-docs domain)

# Step 2: Contact owner
# "I have a conflict in sprint-13.md. Can you review?"

# Step 3: Resolve together (pair programming)
just conflict-resolve project-docs/sprints/sprint-13.md

# Interactive editor opens:
# <<<<<<< HEAD
# - [ ] Task A (In Progress)
# =======
# - [x] Task A (Completed)
# >>>>>>> feature/branch

# Step 4: Choose correct version (discuss with owner)
# → Accept "Completed" (their version is more recent)

# Step 5: Commit
git commit -m "Resolve sprint-13 conflict: Accept completed task status

Reviewed with @victorpiper (project-docs owner).
"
```

**Prevention** (for next time):
- Add sprint-13.md to high-risk file list in CLAUDE.md
- Coordinate before editing: "Working on sprint-13 for 20 min"

---

### Scenario 3: Event Log Conflict (Rare but Critical)

**Problem**: `.chora/memory/events/2025-11.jsonl` has conflicts (both developers appended events simultaneously)

**Solution** (2-3 minutes):
```bash
# Step 1: Both versions are valid (append-only log)
git checkout --ours .chora/memory/events/2025-11.jsonl

# Step 2: Append their version
git show :3:.chora/memory/events/2025-11.jsonl >> .chora/memory/events/2025-11.jsonl

# Step 3: Validate JSONL format
python3 -c "import json; [json.loads(line) for line in open('.chora/memory/events/2025-11.jsonl')]"

# Output: (no error = valid)

# Step 4: Commit
git add .chora/memory/events/2025-11.jsonl
git commit -m "Merge event logs: append both versions"
```

**Prevention** (for multi-developer teams):
- Use developer-specific event logs: `dev-alice-2025-11.jsonl`, `dev-bob-2025-11.jsonl`
- Merge to shared log weekly (during sprint planning)
- See CLAUDE.md "Multi-Developer Coordination" section

---

### Scenario 4: Cross-Domain Conflict (Complex)

**Problem**: PR modifies files in 3 domains (docs/, scripts/, project-docs/), owned by 2 developers

**Solution** (20-30 minutes):
```bash
# Step 1: Identify domains and owners
just ownership-suggest-reviewers-staged

# Output:
# Reviewers: @alice, @bob
# Domains: docs (alice), scripts (bob), project-docs (bob)
# Jurisdiction: Multi-domain (consensus required)

# Step 2: Resolve each domain separately
just conflict-resolve docs/README.md          # Alice's jurisdiction
just conflict-resolve scripts/validate.py      # Bob's jurisdiction
just conflict-resolve project-docs/plan.md     # Bob's jurisdiction

# Step 3: Each owner reviews their domain
# Alice approves docs/ changes
# Bob approves scripts/ and project-docs/ changes

# Step 4: Commit with both owners tagged
git commit -m "Resolve cross-domain conflicts

Domains resolved:
- docs/ (reviewed by @alice)
- scripts/ + project-docs/ (reviewed by @bob)

Consensus achieved per SAP-052 Contract 4.
"
```

**Prevention**:
- Design PRs to minimize cross-domain changes (single domain = faster)
- If cross-domain needed, communicate upfront: "I'm making changes across docs/ and scripts/"

---

### Scenario 5: Metadata File Conflict (Trivial)

**Problem**: `.DS_Store` conflict

**Solution** (30 seconds):
```bash
# Auto-resolve (deletes and adds to .gitignore)
just conflict-auto-resolve

# Output:
# ✅ Resolved: .DS_Store (deleted and added to .gitignore)
```

**Prevention**:
- Ensure `.DS_Store` is in `.gitignore` from project start
- Run `git rm --cached .DS_Store` to remove from tracking

---

## 7. Metrics and Continuous Improvement

### 7.1 Conflict Metrics Dashboard

**Run weekly**:
```bash
just conflict-stats days=30
```

**Output**:
```
Conflict Statistics (Last 30 Days)

Total Conflicts: 12
Auto-Resolved: 5 (42%)
Manual Resolved: 7 (58%)

Average Resolution Time:
- Overall: 8.3 minutes
- Auto-Resolve: 1.5 minutes
- Manual Resolve: 13.2 minutes

Most Frequent Files:
1. project-docs/sprints/sprint-13.md (4 conflicts)
2. docs/vision/mcp.md (2 conflicts)
3. feature-manifest.yaml (2 conflicts)

Resolution Strategies:
- MANUAL_REVIEW: 5 (42%)
- REGENERATE_FROM_SOURCE: 3 (25%)
- AUTO_RESOLVE_FORMATTING: 2 (17%)
- DELETE_AND_REGENERATE: 2 (17%)

Escalation Rate:
- Level 1 (Developer): 10 (83%)
- Level 2 (Pair): 2 (17%)
- Level 3 (Lead): 0 (0%)

Time Saved (vs baseline 20 min/conflict):
- Actual: 100 minutes (12 conflicts × 8.3 min)
- Baseline: 240 minutes (12 conflicts × 20 min)
- **Saved: 140 minutes (58% reduction)**
```

---

### 7.2 Quarterly ROI Calculation

**Baseline** (from SAP-053 charter):
- Conflict frequency: 20-30% of PRs
- Resolution time: 15-30 min/conflict (baseline)
- Annual conflicts: ~150 (2 developers, 3-5 conflicts/week)
- Annual time wasted: **39-130 hours/year**

**After SAP-053 Adoption** (projected):
- Auto-resolution: 30-40% of conflicts (1-2 min/conflict)
- Manual resolution: 50-70% faster (5-10 min vs 15-30 min)
- Recurring conflicts: 80-90% reduction
- **Annual time saved: 51-137 hours/year**

**ROI**:
```
Year 1 ROI = (Benefits - Investment) / Investment
           = ($7,650-$20,550 - $12,900) / $12,900
           = -36% to +72%

Year 2+ ROI = Benefits / Maintenance
            = $7,650-$20,550 / $900
            = 750% to 2,189%
```

**Monitor** quarterly:
```bash
# Q1, Q2, Q3, Q4
just conflict-stats days=90
# Compare to baseline: 15-30 min/conflict
```

---

## 8. Anti-Patterns (Avoid These)

### Anti-Pattern 1: Skipping Pre-PR Conflict Check

**❌ BAD**:
```bash
# Create PR without checking for conflicts
git push
gh pr create
# → CI/CD fails with conflicts
# → 15-20 min delay resolving + rerunning CI/CD
```

**✅ GOOD**:
```bash
# Check first, resolve, then create PR
just conflict-check
just conflict-auto-resolve
git push
gh pr create
# → CI/CD passes on first run
```

**Impact**: 10-20 minutes saved per PR

---

### Anti-Pattern 2: Forcing Manual Resolution for Auto-Resolvable Conflicts

**❌ BAD**:
```bash
# Manually edit poetry.lock conflict markers
# (waste 10 minutes editing 500-line lockfile)
```

**✅ GOOD**:
```bash
# Regenerate from source (1 minute)
just conflict-resolve-lockfile poetry.lock
```

**Impact**: 5-10 minutes saved per lockfile conflict

---

### Anti-Pattern 3: Not Coordinating on High-Risk Files

**❌ BAD**:
```bash
# Both developers edit sprint-13.md simultaneously
# No communication
# → Merge conflict (15-20 min to resolve)
```

**✅ GOOD**:
```bash
# Developer A: "Working on sprint-13.md for 20 min"
# Developer B: "Thanks, I'll wait"
# Developer A: (edits, commits, pushes)
# Developer A: "Sprint-13 updated, safe to edit"
# Developer B: (now edits)
# → No conflict
```

**Impact**: 15-20 minutes saved per avoided conflict

---

### Anti-Pattern 4: Ignoring Recurring Conflict Patterns

**❌ BAD**:
```bash
# Resolve same file conflict 5 times in 90 days
# No knowledge note created
# → Keep wasting 15 min every 2 weeks
```

**✅ GOOD**:
```bash
# After 2nd conflict, create knowledge note
just conflict-patterns
# Document prevention strategy
# → Reduce recurrence by 80-90%
```

**Impact**: 60-80 minutes saved per quarter (per recurring file)

---

### Anti-Pattern 5: Using Force Push to "Resolve" Conflicts

**❌ BAD**:
```bash
# Overwrite remote branch to avoid resolving conflicts
git push --force
# → Colleague's work lost
# → 1-2 hours recovering changes
```

**✅ GOOD**:
```bash
# Resolve conflicts properly
just conflict-check
just conflict-auto-resolve
just conflict-resolve <file>
git push --force-with-lease  # Safe force push (only if no remote changes)
```

**Impact**: Prevents data loss, maintains team trust

---

## 9. Quick Reference: Cheat Sheet

### Common Commands

```bash
# Pre-PR workflow
just conflict-check                       # Check for conflicts
just conflict-auto-resolve                # Auto-resolve safe conflicts
just conflict-resolve <file>              # Manual resolution

# Risk assessment
just conflict-predict                     # Predict risk for staged files

# Pattern detection
just conflict-patterns                    # Detect recurring patterns
just conflict-stats                       # Weekly/monthly metrics

# History queries
just conflict-history <file>              # File-specific conflict history
```

### Decision Matrix

| Situation | Command | Time |
|-----------|---------|------|
| Before creating PR | `just conflict-check` | 30 sec |
| Lockfile conflict | `just conflict-resolve-lockfile poetry.lock` | 1-2 min |
| Metadata conflict | `just conflict-auto-resolve` | 30 sec |
| Code conflict | `just conflict-resolve <file>` | 5-15 min |
| Recurring pattern | `just conflict-patterns` | 2-5 min |
| Before editing high-risk file | `just conflict-predict` | 1 min |

### Resolution Time Targets

| Conflict Type | Target Time | Strategy |
|---------------|-------------|----------|
| Lockfile | 1-2 min | REGENERATE_FROM_SOURCE |
| Metadata | 30 sec | DELETE_AND_REGENERATE |
| Formatting | 1-2 min | AUTO_RESOLVE_FORMATTING |
| Documentation | 5-10 min | MANUAL_REVIEW |
| Code (with owner) | 10-15 min | MANUAL_REVIEW_WITH_OWNERSHIP |
| Cross-domain | 20-30 min | Consensus (SAP-052) |

---

## Document Metadata

**Version**: 1.0.0
**Status**: Draft (Phase 1 - Design)
**Last Updated**: 2025-11-18
**Next Review**: After Phase 3 (Pilot) completion

**Related Documents**:
- [capability-charter.md](capability-charter.md) - SAP-053 charter
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption plan (to be created)
- [ledger.md](ledger.md) - Adoption tracking (to be created)

**SAP Dependencies**:
- SAP-051 (Git Workflow) - ✅ Complete
- SAP-052 (Ownership Zones) - ✅ Complete
- SAP-010 (A-MEM) - ✅ Complete (L4)

---

**Created**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper
**Trace ID**: sap-053-phase1-design-2025-11-18
