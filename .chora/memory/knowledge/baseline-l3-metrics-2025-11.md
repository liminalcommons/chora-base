---
title: "Baseline L3 Metrics - SAP-015 & SAP-010"
created: 2025-11-06
updated: 2025-11-06
tags:
  - baseline
  - l3-metrics
  - sap-015
  - sap-010
  - 90-day-roadmap
author: claude-code
status: baseline
links:
  - "[[sap-010-015-integration-2025-11]]"
---

# Baseline L3 Metrics (2025-11-06)

## Purpose

Baseline metrics captured at the start of the 90-day production data collection phase (Week 1 of L3 roadmap). These metrics establish the starting point for validating SAP-015 (task tracking) and SAP-010 (agent memory) for L3 Production status.

**Measurement Date**: 2025-11-06
**Phase**: Week 1 Foundation (Day 1)
**Next Review**: 2026-02-04 (90 days)

---

## SAP-015 (Task Tracking with Beads)

### L3 Criteria Status: 3/5 Met

**Criteria Met** ✅:
1. **Multi-adopter** (5/5 projects)
   - chora-base
   - chora-compose
   - beads-demo-basic
   - beads-demo-workflow
   - beads-demo-multiagent

2. **ROI Instrumentation** (sap015-metrics.py operational)
   - Dashboard functional
   - L3 checks automated
   - Metrics collection active

3. **Automation** (beads CLI + git hooks)
   - bd CLI operational
   - Git sync working
   - Task dependency tracking active

**Criteria Not Met** ❌:
4. **Setup Time** (0 avg vs ≤30 min target)
   - Status: No production setup data yet
   - Reason: Pilot phase, no external adoptions tracked
   - Target: Average setup time ≤30 minutes

5. **Context Savings** (0% vs ≥20% target)
   - Status: No production context tracking data yet
   - Reason: sap015-context.jsonl just created (1 session logged)
   - Baseline avg: 0.0 min (no baseline sessions recorded)
   - Beads avg: 0.0 min (1 session, no meaningful data)
   - Target: ≥20% time saved in context restoration

### Raw Metrics (2025-11-06)

```json
{
  "setup_time": {
    "total_setups": 0,
    "successful_setups": 0,
    "avg_setup_time_minutes": 0.0,
    "target": 30.0,
    "meets_target": false
  },
  "context": {
    "total_sessions": 1,
    "baseline_sessions": 0,
    "beads_sessions": 1,
    "baseline_avg_minutes": 0.0,
    "beads_avg_minutes": 0.0,
    "time_saved_minutes": 0.0,
    "percent_saved": 0.0,
    "target": 20.0,
    "meets_target": false
  },
  "task_velocity": {
    "total_tasks": 0,
    "avg_completion_time_hours": 0.0,
    "velocity_tasks_per_week": 0.0,
    "tasks_with_blockers": 0
  },
  "dependency": {
    "total_blocks": 0,
    "total_unblocks": 0,
    "avg_blocked_hours": 0.0,
    "currently_blocked": 0
  },
  "multi_adopter": {
    "count": 5,
    "target": 5,
    "meets_target": true
  }
}
```

---

## SAP-010 (Agent Memory Architecture)

### L3 Criteria Status: 2/5 Met

**Criteria Met** ✅:
1. **Multi-adopter** (2/2 projects)
   - chora-base
   - chora-compose

2. **Context Restoration** (97.2% vs ≥80% target)
   - With memory: 5 sec avg
   - Baseline: 180 sec avg
   - Time saved: 97.2% ✅

**Criteria Not Met** ❌:
3. **Knowledge Queries** (1.0 avg vs ≥3.0 target)
   - Status: Minimal query usage
   - Reason: Knowledge graph underutilized
   - Target: ≥3 queries per session

4. **Note Reuse** (0% vs ≥50% target)
   - Total notes: 4
   - Reused notes: 0
   - Target: ≥50% reuse rate

5. **Mistake Reduction** (0% vs ≥30% target)
   - Total mistakes tracked: 0
   - Reason: No mistake tracking infrastructure active
   - Target: ≥30% reduction in repeated mistakes

### Raw Metrics (2025-11-06)

```json
{
  "knowledge_queries": {
    "total_queries": 1,
    "total_sessions": 1,
    "avg_queries_per_session": 1.0,
    "target": 3.0,
    "meets_target": false
  },
  "note_reuse": {
    "total_notes": 4,
    "reused_notes": 0,
    "reuse_percentage": 0.0,
    "total_time_saved_minutes": 0,
    "target": 50.0,
    "meets_target": false
  },
  "mistake_reduction": {
    "total_mistakes": 0,
    "reduction_percentage": 0.0,
    "target": 30.0,
    "meets_target": false
  },
  "context_restoration": {
    "total_sessions": 1,
    "with_memory_sessions": 1,
    "avg_restoration_with_memory_seconds": 5.0,
    "avg_restoration_baseline_seconds": 180,
    "time_saved_percentage": 97.22,
    "target": 80.0,
    "meets_target": true
  },
  "multi_adopter": {
    "count": 2,
    "target": 2,
    "meets_target": true
  }
}
```

---

## Gap Analysis

### SAP-015 Gaps (2/5 criteria need work)

**Gap 1: Setup Time Data**
- **Issue**: No production setup tracking
- **Plan**: Log all new project adoptions (target: 3 more projects in 90 days)
- **Expected Data**: 3-5 setup sessions by Feb 2026
- **Success Metric**: Average ≤30 minutes

**Gap 2: Context Savings Data**
- **Issue**: Only 1 session logged, no baseline comparison
- **Plan**: Daily beads usage + context tracking (sap015-context.jsonl)
- **Expected Data**: 30-60 sessions by Feb 2026
- **Success Metric**: ≥20% time saved vs baseline

### SAP-010 Gaps (3/5 criteria need work)

**Gap 1: Knowledge Query Usage**
- **Issue**: Low query rate (1.0 avg vs 3.0 target)
- **Plan**: Proactive knowledge graph usage (weekly notes, regular queries)
- **Expected Data**: 90 sessions → target 270+ total queries
- **Success Metric**: ≥3 queries/session average

**Gap 2: Note Reuse**
- **Issue**: 0% reuse (4 notes, 0 reused)
- **Plan**: Reference existing notes when solving similar problems
- **Expected Data**: 20-40 notes, ≥10 reused
- **Success Metric**: ≥50% reuse rate

**Gap 3: Mistake Reduction**
- **Issue**: No mistake tracking
- **Plan**: Log mistakes in development.jsonl, track reduction
- **Expected Data**: 10-20 mistakes tracked, ≥30% reduction
- **Success Metric**: ≥30% fewer repeated mistakes

---

## 90-Day Action Plan

### Week 1-2: Foundation (Nov 6-19)
- ✅ YAML frontmatter (chora-base-066) - COMPLETE
- ✅ Test coverage (chora-base-nqj) - COMPLETE
- ⏳ Daily logging workflow (chora-base-3n2) - IN PROGRESS
- Start daily beads usage
- Log context restoration sessions

### Weeks 3-8: Active Data Collection (Nov 20 - Dec 31)
- Daily beads task management
- Weekly knowledge notes
- Monthly metrics reviews
- Target: 30-60 beads sessions
- Target: 10-20 knowledge notes

### Weeks 9-12: Analysis & Validation (Jan 1 - Feb 4)
- Run final L3 checks
- Analyze trends
- Document learnings
- GO/NO-GO decision

### Success Criteria (Feb 2026)

**SAP-015 L3 Target: 5/5 criteria**
- Multi-adopter: ✅ Already met (5/5)
- Setup time: 📊 Need 3-5 data points ≤30 min
- Context savings: 📊 Need ≥20% time saved (30-60 sessions)
- ROI instrumentation: ✅ Already met
- Automation: ✅ Already met

**SAP-010 L3 Target: 5/5 criteria**
- Multi-adopter: ✅ Already met (2/2)
- Context restoration: ✅ Already met (97.2%)
- Knowledge queries: 📊 Need ≥3/session avg (270+ queries over 90 sessions)
- Note reuse: 📊 Need ≥50% reuse (10+ of 20+ notes)
- Mistake reduction: 📊 Need ≥30% reduction (track 10-20 mistakes)

---

## Daily Logging Workflow

### Morning Routine (5 min)
1. Run `bd ready --json` to see unblocked work
2. Pick a task and mark in_progress
3. Log session start in sap015-context.jsonl (if applicable)

### During Work
- Create beads tasks for multi-step work
- Query knowledge graph when stuck (track in development.jsonl)
- Reference existing notes when solving similar problems

### End of Session (5 min)
1. Close completed tasks
2. Update task progress (bd comment)
3. Log context restoration time (if session start involved loading context)
4. Create knowledge notes for learnings (weekly minimum)

### Weekly Review (15 min)
1. Run `python scripts/sap015-metrics.py --l3-check`
2. Run `python scripts/a-mem-metrics.py --l3-check`
3. Review progress toward L3 criteria
4. Create knowledge note summarizing week's learnings

### Monthly Review (30 min)
1. Run full metrics dashboard
2. Update this baseline doc with progress
3. Identify blockers or adjustments needed
4. Document in project ledgers

---

## Automation Setup

### Metrics Commands
```bash
# SAP-015 L3 check
python scripts/sap015-metrics.py --l3-check --json

# SAP-010 L3 check
python scripts/a-mem-metrics.py --l3-check --json

# Combined dashboard
python scripts/sap015-metrics.py && python scripts/a-mem-metrics.py
```

### Beads Workflow
```bash
# Find work
bd ready

# Start task
bd update <task-id> --status in_progress

# Complete task
bd close <task-id> --reason "Task complete"

# Check blockers
bd list --status blocked
```

### Event Logging
```bash
# Log context session
cat >> .chora/memory/events/sap015-context.jsonl << 'EOF'
{
  "event_type": "beads_session",
  "session_type": "baseline|with_beads",
  "context_load_minutes": 5,
  "timestamp": "2025-11-06T02:00:00Z"
}
EOF
```

---

**Status**: 📊 Baseline captured, 90-day collection phase starting
**Review Date**: 2026-02-04
**Expected Outcome**: SAP-015 & SAP-010 promoted to L3 Production (5/5 criteria each)
