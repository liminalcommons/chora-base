---
sap_id: SAP-013
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: awareness-guide
---

# Awareness Guide: Metrics Tracking

**SAP ID**: SAP-013
**Capability Name**: metrics-tracking
**Version**: 1.0.1
**Audience**: AI agents

---

## 1. Overview

### When to Use This SAP

**Use the Metrics Tracking SAP when**:
- Tracking Claude session effectiveness (time saved, lines generated, quality scores)
- Measuring sprint velocity and process quality (DDD/BDD/TDD adherence, defect rates)
- Calculating ROI for AI-assisted development (ClaudeROICalculator)
- Monitoring test coverage trends and defect rates over time
- Preparing release metrics (PyPI downloads, adoption rates, feedback)

**Don't use for**:
- Real-time dashboards - use dedicated monitoring tools (Grafana, Datadog)
- Financial accounting - ClaudeROI is directional for decision-making, not GAAP-compliant
- Individual performance tracking - metrics for process improvement, not employee evaluation
- Granular task timing - focus on session/sprint level, not individual function timing

Track Claude effectiveness, process quality, and team velocity using ClaudeROICalculator and process metrics.

---

## 2. Agent Workflows

### 2.1 Track Claude Session

```python
from mypackage.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator

# After completing task
calculator = ClaudeROICalculator(developer_hourly_rate=100)
metric = ClaudeMetric(
    session_id="unique-id",
    timestamp=datetime.now(),
    task_type="feature_implementation",  # or "bugfix", "refactor"
    lines_generated=250,
    time_saved_minutes=120,  # Estimate vs manual
    iterations_required=2,
    bugs_introduced=0,
    bugs_fixed=3,
    documentation_quality_score=8.5,
    test_coverage=0.92
)
calculator.add_metric(metric)
calculator.export_to_json("project-docs/metrics/claude_roi.json")
```

### 2.2 Update Sprint Metrics

**At end of sprint**:
1. Calculate velocity: `(completed_points / committed_points) * 100`
2. Count defects found during sprint
3. Calculate DDD/BDD/TDD adherence
4. Update `project-docs/sprints/sprint-N.md` metrics section

### 2.3 Update Release Metrics

**1 week post-release**:
1. Collect PyPI downloads, Docker pulls
2. Calculate upgrade rate: `(upgraded_users / total_users) * 100`
3. Review feedback (GitHub issues, support tickets)
4. Update `project-docs/releases/release-vX.Y.Z.md`

---

## 3. Quick Reference

**ClaudeROICalculator**:
```python
calculator = ClaudeROICalculator(hourly_rate=100)
calculator.add_metric(metric)
print(calculator.generate_report())
calculator.export_to_csv("metrics.csv")
```

**Process Metrics Targets**:
- Defect rate: <3 per release
- Test coverage: ≥90%
- Sprint velocity: ≥80%
- DDD/BDD/TDD adherence: ≥80-90%

---

## 4. Common Pitfalls

### Pitfall 1: Not Tracking Time Saved Accurately

**Scenario**: Agent records `time_saved_minutes` without comparing to actual manual effort, overestimates ROI.

**Example**:
```python
# Agent completes feature in 30 minutes with Claude
# Estimates time saved:
metric = ClaudeMetric(
    time_saved_minutes=180,  # "Would take 3 hours manually"
    # Based on gut feeling, not data
)

# Problem: Actual manual time might be 1 hour, not 3
# ROI calculation: 180 min saved → $300 value
# Reality: Only 30 min saved → $50 value
# 6x overestimated ROI!
```

**Fix**: Compare to historical data or similar tasks:
```python
# Look up similar tasks in past:
# - Feature X took 60 minutes manually (logged in sprint metrics)
# - Feature Y (similar complexity) took 75 minutes

# Calculate time saved based on data:
manual_estimate = 70  # Average of similar tasks
actual_with_claude = 30
time_saved = manual_estimate - actual_with_claude  # 40 minutes

metric = ClaudeMetric(
    time_saved_minutes=40,  # Data-driven estimate
    confidence="medium",  # Note estimation method
)
```

**Why it matters**: Overestimated time saved inflates ROI, leads to wrong decisions. Protocol Section 4.2 requires evidence-based estimates. Inflated metrics lose credibility (stakeholders distrust all metrics). Accurate tracking takes 2 extra minutes, fixing trust takes months.

### Pitfall 2: Ignoring Bugs Introduced in ROI Calculation

**Scenario**: Agent calculates ROI based only on time saved, doesn't subtract time spent fixing bugs introduced by Claude.

**Example**:
```python
# Session 1: Claude generates 250 lines in 30 minutes
metric1 = ClaudeMetric(
    lines_generated=250,
    time_saved_minutes=90,  # Would take 2 hours manually
    bugs_introduced=0,  # Agent doesn't track this
)

# Session 2 (next day): Fix 3 bugs from Claude code
# Takes 45 minutes to fix
# Agent doesn't record this as cost!

# ROI: +90 minutes saved
# Reality: +90 minutes - 45 minutes fixing = +45 minutes net
# 2x overestimated actual ROI
```

**Fix**: Track bugs introduced AND time to fix:
```python
# Session 1: Feature implementation
metric1 = ClaudeMetric(
    lines_generated=250,
    time_saved_minutes=90,
    bugs_introduced=3,  # Honest tracking
)

# Session 2: Bug fixing
metric2 = ClaudeMetric(
    task_type="bugfix",
    time_saved_minutes=-45,  # NEGATIVE (cost, not savings)
    bugs_fixed=3,
    bugs_introduced=0,
)

# Net ROI: 90 - 45 = 45 minutes saved (accurate)
```

**Why it matters**: Bugs are costs, not benefits. Protocol Section 3.3 mandates tracking `bugs_introduced` and `bugs_fixed`. Ignoring bug costs creates false ROI picture. One untracked bug session can negate 2-3 productive sessions.

### Pitfall 3: Comparing Metrics Across Different Task Types

**Scenario**: Agent compares metrics from "feature_implementation" vs "bugfix" tasks directly, draws wrong conclusions.

**Example**:
```python
# Feature task:
feature_metric = ClaudeMetric(
    task_type="feature_implementation",
    time_saved_minutes=120,
    lines_generated=300,
)

# Bug fix task:
bugfix_metric = ClaudeMetric(
    task_type="bugfix",
    time_saved_minutes=20,
    lines_generated=15,
)

# Agent compares: "Feature tasks save 6x more time than bugfixes!"
# Conclusion: "Focus on features, avoid bugfixes"

# Problem: Different task types have different baseline efforts
# Features naturally take longer, bugs are smaller scope
# Comparison is meaningless (apples to oranges)
```

**Fix**: Compare metrics WITHIN task types, not across:
```python
# Group by task type:
feature_metrics = [m for m in all_metrics if m.task_type == "feature_implementation"]
bugfix_metrics = [m for m in all_metrics if m.task_type == "bugfix"]

# Compare within groups:
avg_feature_time_saved = mean([m.time_saved_minutes for m in feature_metrics])
avg_bugfix_time_saved = mean([m.time_saved_minutes for m in bugfix_metrics])

# Valid insights:
# - "Features average 110 min saved (vs 120 min this sprint)" ✅
# - "Bugfixes average 22 min saved (vs 20 min this sprint)" ✅
# - "Features save more than bugfixes" ❌ (meaningless comparison)
```

**Why it matters**: Different task types have different characteristics. Protocol Section 4.1 defines task types (feature, bugfix, refactor, test, docs). Comparing across types leads to wrong optimization decisions. Segment by task type for valid insights.

### Pitfall 4: Not Updating Sprint Metrics at Sprint End

**Scenario**: Agent completes sprint but doesn't update `project-docs/sprints/sprint-N.md` metrics section, loses historical velocity data.

**Example**:
```markdown
# Sprint 5 ends (2025-10-28)

# Agent completes features, closes sprint
# But FORGETS to update sprint-5.md:

## Metrics (EMPTY - NOT UPDATED!)
- Velocity: ??? (should be 85%)
- Defect rate: ??? (should be 2 defects)
- Test coverage: ??? (should be 91%)

# Result: No historical data for sprint 5
# Can't compare sprint 6 to sprint 5
# Lose trend analysis capability
```

**Fix**: Update sprint metrics IMMEDIATELY at sprint end:
```markdown
# At sprint retrospective (last day of sprint):

## Metrics (Updated 2025-10-28)
- **Velocity**: 85% (17/20 points completed)
- **Defect Rate**: 2 defects found during sprint (target: <3) ✅
- **Test Coverage**: 91% (target: ≥90%) ✅
- **DDD Adherence**: 90% (9/10 features had design docs)
- **TDD Adherence**: 80% (8/10 features had tests first)

## Trends
- Velocity: Sprint 4 (82%) → Sprint 5 (85%) ↑ 3%
- Coverage: Sprint 4 (89%) → Sprint 5 (91%) ↑ 2%
```

**Why it matters**: Sprint metrics enable trend analysis. Protocol Section 5.2 mandates updating metrics at sprint end. Missing one sprint breaks trend continuity. Historical data powers retrospectives and forecasting. Updating takes 10 minutes at sprint end, recreating lost data later is impossible.

### Pitfall 5: Forgetting to Export Metrics Before Major Changes

**Scenario**: Agent makes major changes to project structure, loses historical metrics (no export/backup).

**Example**:
```bash
# Agent has 3 months of Claude ROI data:
project-docs/metrics/claude_roi.json  # 90 sessions tracked

# Agent refactors project structure:
git mv project-docs/ docs/project-lifecycle/  # Directory renamed

# claude_roi.json moved, metrics scripts break:
python scripts/generate_roi_report.py
# Error: FileNotFoundError: project-docs/metrics/claude_roi.json

# Result: Can't generate reports until path updated
# Worse: If file accidentally deleted, 3 months data LOST
```

**Fix**: Export metrics before major changes:
```bash
# Before refactoring:
# 1. Export to CSV (human-readable backup):
calculator = ClaudeROICalculator.from_json("project-docs/metrics/claude_roi.json")
calculator.export_to_csv("backups/claude_roi_backup_2025-10-28.csv")

# 2. Commit current state:
git add project-docs/metrics/claude_roi.json
git commit -m "backup: export metrics before refactor"

# 3. NOW safe to refactor:
git mv project-docs/ docs/project-lifecycle/

# 4. Update scripts to new path:
# Update path in scripts/generate_roi_report.py

# 5. Verify metrics still accessible:
python scripts/generate_roi_report.py  # Should work with new path
```

**Why it matters**: Metrics data is irreplaceable historical record. Protocol Section 6.2 recommends regular exports. One accidental deletion loses months of data. Exporting before changes takes 2 minutes, prevents catastrophic data loss.

---

## 5. Related Content

### Within This SAP (skilled-awareness/metrics-tracking/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-013
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (ClaudeROI calculator, process metrics, targets)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for implementing metrics tracking
- [ledger.md](ledger.md) - Metrics tracking adoption, version history
- **This document** (awareness-guide.md) - Agent workflows for tracking metrics

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/sprint-retrospective.md](/dev-docs/workflows/sprint-retrospective.md) - Sprint metrics review process
- [dev-docs/workflows/release-retrospective.md](/dev-docs/workflows/release-retrospective.md) - Post-release metrics analysis

**Tools**:
- [dev-docs/tools/claude-roi-calculator.md](/dev-docs/tools/claude-roi-calculator.md) - ClaudeROICalculator usage guide
- [dev-docs/tools/metrics-dashboard.md](/dev-docs/tools/metrics-dashboard.md) - Metrics visualization tools

**Development Guidelines**:
- [dev-docs/development/metrics-standards.md](/dev-docs/development/metrics-standards.md) - Standards for collecting metrics

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [static-template/project-docs/metrics/](/static-template/project-docs/metrics/) - Metrics directory structure
- [static-template/project-docs/metrics/PROCESS_METRICS.md](/static-template/project-docs/metrics/PROCESS_METRICS.md) - Process metrics template
- [static-template/src/utils/claude_metrics.py](/static-template/src/utils/claude_metrics.py) - ClaudeMetric and ClaudeROICalculator classes

**Guides**:
- [project-docs/guides/metrics-collection.md](/project-docs/guides/metrics-collection.md) - Guide for collecting metrics
- [project-docs/guides/roi-analysis.md](/project-docs/guides/roi-analysis.md) - Analyzing Claude ROI data

**Sprint & Release Tracking**:
- [project-docs/sprints/](/project-docs/sprints/) - Sprint metrics (velocity, defect rate, coverage)
- [project-docs/releases/](/project-docs/releases/) - Release metrics (downloads, adoption, feedback)

**Audits**:
- [project-docs/audits/](/project-docs/audits/) - SAP audits including SAP-013 validation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/understanding-metrics.md](/user-docs/guides/understanding-metrics.md) - Introduction to metrics tracking

**Tutorials**:
- [user-docs/tutorials/tracking-claude-sessions.md](/user-docs/tutorials/tracking-claude-sessions.md) - Track Claude effectiveness
- [user-docs/tutorials/calculating-roi.md](/user-docs/tutorials/calculating-roi.md) - Calculate AI development ROI

**Reference**:
- [user-docs/reference/metrics-reference.md](/user-docs/reference/metrics-reference.md) - Complete metrics reference
- [user-docs/reference/process-targets.md](/user-docs/reference/process-targets.md) - Process metric targets

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.11 (documents SAP-013)

**Dependent Capabilities**:
- [memory-system/](../memory-system/) - SAP-009 (event logs feed metrics)
- [automation-scripts/](../automation-scripts/) - SAP-008 (`just metrics` command)
- [testing-framework/](../testing-framework/) - SAP-004 (test coverage metrics)

**Supporting Capabilities**:
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (CI metrics)
- [quality-gates/](../quality-gates/) - SAP-006 (quality metrics)
- [development-lifecycle/](../development-lifecycle/) - SAP-012 (DDD/BDD/TDD adherence metrics)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-013 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings (5 scenarios: time saved accuracy, bugs introduced tracking, task type comparisons, sprint metrics updates, metric exports), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide for metrics-tracking SAP
