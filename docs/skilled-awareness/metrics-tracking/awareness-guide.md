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
**Version**: 1.0.0
**Audience**: AI agents

---

## 1. Overview

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

## 4. Related Documents

- [protocol-spec.md](protocol-spec.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [PROCESS_METRICS.md](../../../static-template/project-docs/metrics/PROCESS_METRICS.md)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for metrics-tracking SAP
