---
title: "Daily Log - {DATE}"
created: {DATE}
tags:
  - daily-log
  - production-data
  - sap-015
  - sap-010
---

# Daily Log - {DATE}

## Morning Checklist

- [ ] Run `bd ready` to see unblocked work
- [ ] Pick task and mark `in_progress`
- [ ] Log session start (if context loading session)

## Work Summary

### Tasks Worked On
- **Task ID**: {TASK_ID}
- **Title**: {TASK_TITLE}
- **Status**: {open|in_progress|closed}
- **Time Spent**: {HOURS} hours
- **Notes**: {NOTES}

### Beads Usage
- [ ] Created new tasks for multi-step work?
- [ ] Updated task dependencies?
- [ ] Closed completed tasks?
- [ ] Used `bd ready` to find next work?

### Knowledge Graph Usage
- [ ] Queried existing notes when stuck?
- [ ] Created new knowledge notes for learnings?
- [ ] Referenced previous solutions?
- **Query Count**: {COUNT}
- **Notes Referenced**: {NOTE_IDS}

### Context Restoration
**If this session started with context loading:**
- Session type: [ ] baseline (no memory) [ ] with_beads [ ] with_a-mem
- Time to restore context: {MINUTES} min
- Tools used: [ ] beads [ ] a-mem events [ ] knowledge notes

## End of Day Checklist

- [ ] Close completed tasks
- [ ] Update task progress (`bd comment`)
- [ ] Log context restoration time (if applicable)
- [ ] Create knowledge note (if significant learning)

## Metrics Snapshot

Run periodically:
```bash
# SAP-015
python scripts/sap015-metrics.py --l3-check

# SAP-010
python scripts/a-mem-metrics.py --l3-check
```

## Notes / Learnings

{FREE_FORM_NOTES}

## Blockers / Issues

{BLOCKERS}

---

**Template Usage**:
1. Copy this template to `.chora/memory/knowledge/daily-log-YYYY-MM-DD.md`
2. Replace {PLACEHOLDERS} with actual values
3. Check off completed items
4. File in knowledge graph with [[wikilinks]] to related notes
