# A-MEM Integration Guide (SAP-051 + SAP-010)

**Integration**: SAP-051 (Git Workflow Patterns) + SAP-010 (Memory System)
**Purpose**: Full event traceability from git commits to A-MEM logs
**Level**: Advanced (Level 3)

---

## Overview

Integrating SAP-051 with SAP-010 (A-MEM) provides:
- **Full Traceability**: Every significant commit logged as A-MEM event
- **Commit Correlation**: Link A-MEM events to git SHAs for context
- **Cross-Session Continuity**: Resume work from A-MEM query + git checkout
- **Metrics Tracking**: Analyze commit patterns via A-MEM queries

---

## Integration Patterns

### Pattern 1: Log Commits as A-MEM Events

**When to use**: Significant commits (SAP milestones, coordination deliverables, major features)

**Implementation**:
```bash
# After making a significant commit
COMMIT_SHA=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=format:%s)

cat >> .chora/memory/events/$(date +%Y-%m).jsonl << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "type": "sap_artifact_created",
  "sap_id": "SAP-051",
  "git_commit": "$COMMIT_SHA",
  "trace_id": "sap-051-implementation",
  "metadata": {
    "commit_message": "$COMMIT_MSG",
    "branch": "$(git branch --show-current)",
    "artifact": "git-hooks",
    "files_changed": $(git diff-tree --no-commit-id --name-only -r HEAD | wc -l)
  }
}
EOF
```

**Benefits**:
- `git show $COMMIT_SHA` provides full context for A-MEM events
- A-MEM queries can filter by `git_commit` field
- Full audit trail from event → commit → code changes

---

### Pattern 2: Extract Commit Metadata for A-MEM

**When to use**: Analyzing commit patterns, tracking SAP progress

**Implementation**:
```bash
# Query commits with SAP references
git log --grep="Refs: SAP-051" --format="%H|%s|%an|%ai" | while IFS='|' read sha msg author date; do
  cat >> .chora/memory/events/$(date +%Y-%m).jsonl << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "type": "commit_analysis",
  "sap_id": "SAP-051",
  "git_commit": "$sha",
  "metadata": {
    "message": "$msg",
    "author": "$author",
    "commit_date": "$date",
    "analysis_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
}
EOF
done
```

**Use Case**: Generate SAP adoption metrics from commit history

---

### Pattern 3: Link Coordination Requests to Commits

**When to use**: Working on COORD requests with git workflow

**Branch naming**:
```bash
git checkout -b feature/COORD-2025-013-sap-051-implementation
```

**Commit format**:
```bash
git commit -m "feat(sap-051): implement git workflow patterns

Implements git hooks and automation for multi-developer workflows.
Addresses requirements from COORD-2025-013.

Refs: SAP-051, COORD-2025-013"
```

**A-MEM event**:
```json
{
  "timestamp": "2025-11-16T12:00:00Z",
  "type": "coordination_deliverable_complete",
  "coord_id": "COORD-2025-013",
  "git_commit": "a1b2c3d4e5f6...",
  "trace_id": "coord-2025-013",
  "metadata": {
    "deliverable": "SAP-051 git hooks implementation",
    "branch": "feature/COORD-2025-013-sap-051-implementation",
    "commits_count": 6,
    "saps_involved": ["SAP-051", "SAP-010"]
  }
}
```

**Query pattern**:
```bash
# Find all commits for coordination request
git log --grep="COORD-2025-013" --oneline

# Find A-MEM events for same request
grep "COORD-2025-013" .chora/memory/events/*.jsonl
```

---

### Pattern 4: Beads Task Completion with Git Commits

**When to use**: Completing beads tasks with git work

**Workflow**:
```bash
# 1. Create branch with task ID
bd show .beads-9rtq
git checkout -b feature/.beads-9rtq-sap-051-charter

# 2. Do work and commit
git commit -m "feat(.beads-9rtq): create SAP-051 capability charter

Completes beads task for COORD-2025-013 charter deliverable.

Refs: .beads-9rtq, SAP-051, COORD-2025-013"

# 3. Log A-MEM event with task + commit
COMMIT_SHA=$(git rev-parse HEAD)
cat >> .chora/memory/events/$(date +%Y-%m).jsonl << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "type": "beads_task_complete",
  "beads_id": ".beads-9rtq",
  "git_commit": "$COMMIT_SHA",
  "trace_id": "coord-2025-013",
  "metadata": {
    "task_description": "Create SAP-051 capability charter",
    "completion_method": "git_commit",
    "sap_id": "SAP-051",
    "coord_id": "COORD-2025-013"
  }
}
EOF

# 4. Close beads task
bd close .beads-9rtq
```

**Full traceability**: beads task → git commit → A-MEM event → COORD request → SAP

---

## Automation Recipes

### Recipe 1: Auto-Log Significant Commits

Add to post-commit hook:
```bash
#!/usr/bin/env bash
# .githooks/post-commit

# Only log if commit message contains SAP/COORD references
COMMIT_MSG=$(git log -1 --pretty=format:%s)

if echo "$COMMIT_MSG" | grep -qE "(SAP-[0-9]+|COORD-[0-9]+-[0-9]+)"; then
  COMMIT_SHA=$(git rev-parse HEAD)
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  cat >> .chora/memory/events/$(date +%Y-%m).jsonl << EOF
{
  "timestamp": "$TIMESTAMP",
  "type": "significant_commit",
  "git_commit": "$COMMIT_SHA",
  "metadata": {
    "message": "$COMMIT_MSG",
    "branch": "$(git branch --show-current)",
    "author": "$(git log -1 --pretty=format:%an)"
  }
}
EOF
fi
```

### Recipe 2: Generate SAP Progress Report from Git + A-MEM

```bash
#!/usr/bin/env bash
# scripts/sap-progress-report.sh

SAP_ID="${1:-SAP-051}"

echo "=== SAP Progress Report: $SAP_ID ==="
echo ""

# Count commits
COMMIT_COUNT=$(git log --grep="$SAP_ID" --oneline | wc -l)
echo "Commits: $COMMIT_COUNT"

# Show A-MEM events
EVENT_COUNT=$(grep "\"sap_id\": \"$SAP_ID\"" .chora/memory/events/*.jsonl | wc -l)
echo "A-MEM Events: $EVENT_COUNT"

# Show commit timeline
echo ""
echo "Recent Commits:"
git log --grep="$SAP_ID" --format="%h %s (%ar)" -n 10

# Show A-MEM timeline
echo ""
echo "Recent Events:"
grep "\"sap_id\": \"$SAP_ID\"" .chora/memory/events/*.jsonl | tail -5 | jq '.type + " (" + .timestamp + ")"'
```

### Recipe 3: Correlate Session to Commits

```bash
#!/usr/bin/env bash
# scripts/session-commit-correlation.sh

TRACE_ID="${1}"

echo "=== Session-Commit Correlation: $TRACE_ID ==="
echo ""

# Find A-MEM events with trace_id
echo "A-MEM Events:"
grep "\"trace_id\": \"$TRACE_ID\"" .chora/memory/events/*.jsonl | jq -c '{time: .timestamp, type: .type, commit: .git_commit}'

echo ""
echo "Git Commits:"
# Extract commit SHAs from A-MEM events
grep "\"trace_id\": \"$TRACE_ID\"" .chora/memory/events/*.jsonl | jq -r '.git_commit' | while read sha; do
  if [ -n "$sha" ]; then
    git show --oneline -s $sha
  fi
done
```

---

## Query Patterns

### Query 1: Find All Commits for SAP

```bash
# Via git
git log --grep="SAP-051" --oneline

# Via A-MEM
grep '"sap_id": "SAP-051"' .chora/memory/events/*.jsonl | jq '.git_commit' | sort -u

# Combined view
git log --grep="SAP-051" --format="%H %s" | while read sha msg; do
  events=$(grep "\"git_commit\": \"$sha\"" .chora/memory/events/*.jsonl | wc -l)
  echo "$sha | $events events | $msg"
done
```

### Query 2: Session Resumption from A-MEM

```bash
# 1. Find session in A-MEM
grep "trace_id.*sap-051-pilot" .chora/memory/events/2025-11.jsonl | tail -1 | jq -r '.git_commit'
# Output: ea35313...

# 2. Checkout that commit
git checkout ea35313

# 3. See what was being worked on
git show --stat

# 4. Continue work on same branch
git checkout feature/SAP-051-git-workflow-implementation
```

### Query 3: Coordination Request Progress

```bash
# Show all work for COORD request
COORD_ID="COORD-2025-013"

echo "Git Commits:"
git log --grep="$COORD_ID" --oneline

echo ""
echo "A-MEM Events:"
grep "\"coord_id\": \"$COORD_ID\"" .chora/memory/events/*.jsonl | jq '{time: .timestamp, type: .type}'

echo ""
echo "Beads Tasks:"
grep "\"coord_id\": \"$COORD_ID\"" .chora/memory/events/*.jsonl | jq -r '.beads_id' | sort -u
```

---

## Best Practices

1. **Log Milestones, Not Every Commit**:
   - ✅ SAP artifact creation
   - ✅ Coordination deliverable completion
   - ✅ Phase completions
   - ❌ Typo fixes, formatting commits

2. **Include trace_id in Both Git and A-MEM**:
   ```bash
   # In git commit footer
   Refs: SAP-051
   Trace-ID: sap-051-pilot

   # In A-MEM event
   {"trace_id": "sap-051-pilot", ...}
   ```

3. **Use Consistent Identifiers**:
   - SAP IDs: `SAP-051`
   - COORD IDs: `COORD-2025-013`
   - Beads tasks: `.beads-9rtq`
   - Trace IDs: `sap-051-pilot`, `coord-2025-013`

4. **Correlation Fields**:
   Always include in A-MEM events:
   - `git_commit` (SHA)
   - `trace_id` (session identifier)
   - `sap_id`, `coord_id`, or `beads_id` (domain identifier)

5. **Query-Friendly Metadata**:
   Add structured metadata for easy querying:
   ```json
   "metadata": {
     "branch": "feature/SAP-051-...",
     "files_changed": 12,
     "lines_added": 450,
     "tests_added": 15
   }
   ```

---

## Metrics & Analytics

### Commit Velocity per SAP

```bash
# Commits per week for SAP-051
git log --grep="SAP-051" --since="1 week ago" --oneline | wc -l
```

### Event Density Analysis

```bash
# A-MEM events per commit
COMMITS=$(git log --grep="SAP-051" --oneline | wc -l)
EVENTS=$(grep '"sap_id": "SAP-051"' .chora/memory/events/*.jsonl | wc -l)
echo "Events per commit: $(($EVENTS / $COMMITS))"
```

### Session Productivity

```bash
# Find sessions with most commits
grep "trace_id" .chora/memory/events/2025-11.jsonl | jq -r '.trace_id' | sort | uniq -c | sort -rn
```

---

## Troubleshooting

**Problem**: A-MEM events missing git_commit field
**Solution**: Add git_commit to event schema in post-commit automation

**Problem**: Can't correlate old commits to A-MEM
**Solution**: Retroactively add events:
```bash
git log --since="2025-11-01" --grep="SAP-051" --format="%H|%s|%ai" | while IFS='|' read sha msg date; do
  # Create A-MEM event for historical commit
done
```

**Problem**: Too many A-MEM events (noise)
**Solution**: Only log commits with `Refs:` footer or SAP/COORD IDs

---

## See Also

- [SAP-010: Memory System](../../skilled-awareness/memory-system/)
- [SAP-001: Inbox Protocol](../../skilled-awareness/inbox/)
- [Git Workflow Protocol Spec](../skilled-awareness/git-workflow-patterns/protocol-spec.md)
- [Adoption Blueprint Level 3](../skilled-awareness/git-workflow-patterns/adoption-blueprint.md#level-3-mastery-production-ready)

---

**Version**: 1.0.0 (2025-11-16)
**Integration**: SAP-051 + SAP-010
**Status**: Production-Ready
