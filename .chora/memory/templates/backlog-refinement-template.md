---
type: backlog-refinement
quarter: YYYY-Qn
date: YYYY-MM-DD
project: project-name
owner: Agent/Human Name
duration_hours: 2-4
linked_to:
  - vision-document-{date}.md
  - milestone-{version}.md
  - backlog-refinement-{previous-quarter}.md
---

# Backlog Refinement: {Project Name} - {Quarter}

**Refinement Date**: {YYYY-MM-DD}
**Duration**: {X} hours
**Facilitator**: {Agent/Human Name}
**Quarter**: {YYYY-Qn}

---

## 1. Executive Summary

**Goal**: Quarterly backlog grooming to maintain backlog health, align priorities with current vision, and archive stale work.

**Key Outcomes**:
- {X} stale tasks closed/archived
- {X} priorities adjusted to align with vision Wave {1/2/3}
- {X} epics completed/closed
- Priority distribution adjusted to target: P0 (<5%), P1 (<20%), P2 (<30%), P3 (<30%), P4 (<15%)

---

## 2. Pre-Refinement Metrics

**Backlog Snapshot** (before refinement):
- **Total open tasks**: {count}
- **Priority distribution**:
  - P0 (NOW): {count} ({percentage}%)
  - P1 (NEXT): {count} ({percentage}%)
  - P2 (LATER): {count} ({percentage}%)
  - P3 (SOMEDAY): {count} ({percentage}%)
  - P4 (BACKLOG): {count} ({percentage}%)
- **Stale tasks (>90 days)**: {count} ({percentage}% of backlog)
- **Open epics**: {count}
- **Average task age**: {days} days

**Query Used**:
```bash
# Total open tasks
bd list --status open --json | jq 'length'

# Priority distribution
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'

# Stale tasks
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json | jq 'length'

# Open epics
bd list --type epic --status open --json | jq 'length'

# Average task age
bd list --status open --json | jq '[.[] | (now - (.created_at | fromdateiso8601)) / 86400] | add / length'
```

---

## 3. Refinement Activities

### 3.1: Stale Task Review

**Threshold**: 90 days
**Stale tasks found**: {count}

**Actions Taken**:

| Task ID | Title | Age (days) | Action | Reason |
|---------|-------|------------|--------|--------|
| {task-id-1} | {title} | {days} | Closed | No longer relevant |
| {task-id-2} | {title} | {days} | P1 → P4 | Deprioritized to backlog |
| {task-id-3} | {title} | {days} | Kept P1 | Still roadmap-committed |
| ... | ... | ... | ... | ... |

**Summary**:
- **Closed**: {X} tasks (no longer relevant, duplicates, completed elsewhere)
- **Downgraded**: {X} tasks (P0/P1/P2 → P3/P4)
- **Kept priority**: {X} tasks (still relevant, updated notes)

**Query Used**:
```bash
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json > stale-tasks.json
```

---

### 3.2: Priority Adjustment

**Vision Alignment**: Aligned with vision document `{vision-doc-name}.md` Wave 1/2/3

**Actions Taken**:

| Task ID | Title | Old Priority | New Priority | Reason |
|---------|-------|--------------|--------------|--------|
| {task-id-1} | {title} | P1 (NEXT) | P3 (SOMEDAY) | Vision Wave 2 → exploratory |
| {task-id-2} | {title} | P2 (LATER) | P1 (NEXT) | Roadmap committed for {version} |
| {task-id-3} | {title} | P0 (NOW) | P1 (NEXT) | No longer blocks critical path |
| ... | ... | ... | ... | ... |

**Priority Adjustment Criteria**:
1. **Vision Wave Alignment**:
   - Vision Wave 1 (Committed - 3 months) → P1 (NEXT) or P2 (LATER)
   - Vision Wave 2 (Exploratory - 6 months) → P3 (SOMEDAY)
   - Vision Wave 3 (Aspirational - 12 months) → P4 (BACKLOG)

2. **Roadmap Commitments**:
   - Roadmap milestone {version} → P1 (NEXT) or P2 (LATER)
   - Exploratory features → P3 (SOMEDAY)

3. **Resource Availability**:
   - Team capacity for P0/P1 work: {X} tasks per sprint
   - Limit P0 to <5% of backlog (critical path only)

**Summary**:
- **Upgraded**: {X} tasks (P2/P3/P4 → P0/P1)
- **Downgraded**: {X} tasks (P0/P1/P2 → P3/P4)
- **No change**: {X} tasks (already aligned)

**Query Used**:
```bash
# Get priority distribution
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'

# Example: Downgrade exploratory tasks
bd list --priority 1 --json | jq '.[] | select(.metadata.vision_wave == 2) | .id' | xargs -I {} bd update {} --priority 3
```

---

### 3.3: Backlog Archival

**Archival Criteria**:
- P4 (BACKLOG) tasks open for >180 days
- Tasks no longer aligned with project vision
- Duplicate/superseded tasks

**Actions Taken**:

| Task ID | Title | Age (days) | Priority | Action | Reason |
|---------|-------|------------|----------|--------|--------|
| {task-id-1} | {title} | {days} | P4 | Closed | >180 days in P4, not relevant |
| {task-id-2} | {title} | {days} | P3 | Closed | Superseded by {new-task-id} |
| {task-id-3} | {title} | {days} | P4 | Closed | No longer aligned with vision |
| ... | ... | ... | ... | ... | ... |

**Summary**:
- **Archived**: {X} tasks (closed with reason "backlog cleanup")
- **Compacted**: {X} closed tasks older than 1 year (for performance)

**Query Used**:
```bash
# Close stale P4 tasks
bd list --priority 4 --status open --created-before $(date -v-180d +%Y-%m-%d) --json | \
  jq -r '.[] | .id' | \
  xargs -I {} bd close {} --reason "Backlog cleanup: archived after 180 days in P4"

# Archive closed tasks older than 1 year (optional)
bd compact --older-than 365d
```

---

### 3.4: Epic Progress Review

**Open Epics**: {count}

**Epic Completion Status**:

| Epic ID | Title | Total Subtasks | Completed | Progress | Action | Reason |
|---------|-------|----------------|-----------|----------|--------|--------|
| {epic-id-1} | {title} | {total} | {completed} | {%}% | Closed | 100% complete |
| {epic-id-2} | {title} | {total} | {completed} | {%}% | Kept open | In progress |
| {epic-id-3} | {title} | {total} | {completed} | {%}% | Deprioritized | Stalled >90 days |
| ... | ... | ... | ... | ... | ... | ... |

**Epic Review Criteria**:
1. **100% complete** → Close epic
2. **>75% complete, active** → Keep open, update notes
3. **<50% complete, stalled >90 days** → Re-evaluate or deprioritize
4. **No progress in 180 days** → Close or archive

**Summary**:
- **Epics closed**: {X} (100% complete)
- **Epics deprioritized**: {X} (stalled, low priority)
- **Epics updated**: {X} (progress notes added)

**Query Used**:
```bash
# List all epics with completion stats
bd list --type epic --status open --json | jq '.[] | {
  id: .id,
  title: .title,
  total_subtasks: (.dependencies | map(select(.type == "parent")) | length),
  completed_subtasks: (.dependencies | map(select(.type == "parent" and .target_status == "closed")) | length)
}'
```

---

### 3.5: Metadata Refresh

**Vision Alignment**: Updated metadata to reflect vision document `{vision-doc-name}.md`

**Actions Taken**:

| Epic ID | Title | Old Wave | New Wave | Target Quarter | Notes |
|---------|-------|----------|----------|----------------|-------|
| {epic-id-1} | {title} | Wave 1 | Wave 1 | {YYYY-Qn} | Still committed |
| {epic-id-2} | {title} | Wave 1 | Wave 2 | {YYYY-Qn} | Pushed to exploratory |
| {epic-id-3} | {title} | - | Wave 1 | {YYYY-Qn} | Newly committed |
| ... | ... | ... | ... | ... | ... |

**Metadata Fields Updated**:
- `vision_wave`: 1 (Committed), 2 (Exploratory), 3 (Aspirational)
- `target_quarter`: {YYYY-Qn}
- `roadmap_version`: {version}
- `vision_document`: {vision-doc-name}

**Summary**:
- **Epics updated with vision metadata**: {X}
- **Tasks updated with vision metadata**: {X}

**Query Used**:
```bash
# Update epic metadata with vision wave alignment
bd list --type epic --status open --json | jq -r '.[] | .id' | while read epic_id; do
  bd update $epic_id --metadata '{
    "vision_wave": 1,
    "target_quarter": "2026-Q2",
    "roadmap_version": "v1.5.0",
    "vision_document": "vision-chora-base-6-month"
  }'
done
```

---

## 4. Post-Refinement Metrics

**Backlog Snapshot** (after refinement):
- **Total open tasks**: {count} (Δ: {change})
- **Priority distribution**:
  - P0 (NOW): {count} ({percentage}%) - Target: <5%
  - P1 (NEXT): {count} ({percentage}%) - Target: <20%
  - P2 (LATER): {count} ({percentage}%) - Target: <30%
  - P3 (SOMEDAY): {count} ({percentage}%) - Target: <30%
  - P4 (BACKLOG): {count} ({percentage}%) - Target: <15%
- **Stale tasks (>90 days)**: {count} ({percentage}% of backlog) (Δ: {change})
- **Open epics**: {count} (Δ: {change})
- **Average task age**: {days} days (Δ: {change} days)

**Quality Gates Assessment**:
- ✅/❌ Stale tasks (>90 days) reduced by ≥50%: {before} → {after} ({%}% reduction)
- ✅/❌ Priority distribution within ±5% of target: P0 {%}%, P1 {%}%, P2 {%}%, P3 {%}%, P4 {%}%
- ✅/❌ All P0 tasks have assignees and are unblocked: {count}/{total} tasks
- ✅/❌ All epics have updated progress notes or are closed: {count}/{total} epics
- ✅/❌ Backlog health metrics logged to A-MEM: See Section 6

---

## 5. Insights & Lessons Learned

### 5.1: Backlog Health Trends

**Stale Task Accumulation**:
- {Observation: Are stale tasks increasing or decreasing over time?}
- {Root cause: Why are tasks going stale? Blocked dependencies? Unclear requirements?}
- {Action item: What can be done to prevent stale task accumulation?}

**Priority Drift**:
- {Observation: Is the team consistently over-allocating to P0/P1 (urgent work)?}
- {Root cause: Why is priority drift occurring? Vision changes? Reactive firefighting?}
- {Action item: How can priority discipline be improved?}

**Epic Completion Rate**:
- {Observation: How many epics were completed this quarter vs last quarter?}
- {Velocity trend: Is epic completion accelerating or decelerating?}
- {Action item: What can be done to improve epic completion rate?}

### 5.2: Strategic Alignment

**Vision Wave Alignment**:
- {Observation: Are tasks well-aligned with vision waves?}
- {Gaps: Are there vision themes with no corresponding tasks? Or vice versa?}
- {Action item: What adjustments are needed to align backlog with vision?}

**Roadmap Commitment**:
- {Observation: Are roadmap milestones on track?}
- {Blockers: What's preventing roadmap progress?}
- {Action item: What needs to be re-scoped or deprioritized?}

### 5.3: Recommendations for Next Quarter

1. **Priority Management**:
   - {Recommendation based on priority distribution trends}

2. **Epic Decomposition**:
   - {Recommendation based on epic completion trends}

3. **Backlog Archival**:
   - {Recommendation based on stale task trends}

4. **Vision Synthesis**:
   - {Recommendation based on vision alignment gaps}

---

## 6. A-MEM Event Log

**Backlog Health Event** (logged to `.chora/memory/events/backlog-health.jsonl`):

```json
{
  "event": "backlog_refinement_completed",
  "timestamp": "{YYYY-MM-DDTHH:MM:SSZ}",
  "quarter": "{YYYY-Qn}",
  "project": "{project-name}",
  "facilitator": "{agent/human}",
  "duration_hours": {X},
  "metrics": {
    "before": {
      "total_open_tasks": {count},
      "stale_tasks_count": {count},
      "stale_tasks_percentage": {percentage},
      "priority_distribution": {
        "P0": {count},
        "P1": {count},
        "P2": {count},
        "P3": {count},
        "P4": {count}
      },
      "open_epics": {count},
      "average_task_age_days": {days}
    },
    "after": {
      "total_open_tasks": {count},
      "stale_tasks_count": {count},
      "stale_tasks_percentage": {percentage},
      "priority_distribution": {
        "P0": {count},
        "P1": {count},
        "P2": {count},
        "P3": {count},
        "P4": {count}
      },
      "open_epics": {count},
      "average_task_age_days": {days}
    }
  },
  "actions_taken": {
    "tasks_closed": {count},
    "tasks_archived": {count},
    "priorities_adjusted": {count},
    "epics_closed": {count},
    "epics_deprioritized": {count},
    "metadata_updated": {count}
  },
  "quality_gates": {
    "stale_tasks_reduced_50pct": true/false,
    "priority_distribution_aligned": true/false,
    "p0_tasks_unblocked": true/false,
    "epics_updated": true/false,
    "metrics_logged": true/false
  },
  "linked_documents": {
    "vision_document": "{vision-doc-name}.md",
    "previous_refinement": "backlog-refinement-{previous-quarter}.md",
    "next_refinement_due": "{YYYY-Qn}"
  }
}
```

**Command to Log**:
```bash
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

---

## 7. Action Items

**Follow-Up Tasks**:

| Action | Owner | Due Date | Priority | Beads Task ID |
|--------|-------|----------|----------|---------------|
| {Action item from insights} | {owner} | {date} | P{0-4} | {task-id} |
| Update vision document based on refinement insights | {owner} | {date} | P{0-4} | {task-id} |
| Schedule next quarterly refinement ({next quarter}) | {owner} | {date} | P{0-4} | {task-id} |
| ... | ... | ... | ... | ... |

---

## 8. Sign-Off

**Facilitator**: {Agent/Human Name}
**Date**: {YYYY-MM-DD}
**Next Refinement Due**: {YYYY-Qn} ({date})

**Notes**:
- Backlog refinement completed successfully
- All quality gates met: ✅/❌
- Backlog health metrics logged to A-MEM: ✅
- Next refinement scheduled for {quarter}

---

## Appendix A: Reference Queries

### A.1: Priority Distribution
```bash
bd list --status open --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
```

### A.2: Stale Tasks (>90 days)
```bash
bd list --status open --created-before $(date -v-90d +%Y-%m-%d) --json
```

### A.3: Orphan Tasks (no epic)
```bash
bd list --status open --type task --json | jq '[.[] | select(.dependencies.blocked_by | length == 0)]'
```

### A.4: Epic Progress
```bash
bd list --type epic --status open --json | jq '.[] | {
  id: .id,
  title: .title,
  progress: ((.dependencies | map(select(.type == "parent" and .target_status == "closed")) | length) * 100 / (.dependencies | map(select(.type == "parent")) | length))
}'
```

### A.5: High-Priority Staleness
```bash
bd list --priority 0,1 --status open --created-before $(date -v-30d +%Y-%m-%d) --json
```

---

## Appendix B: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {YYYY-MM-DD} | {author} | Initial backlog refinement |
