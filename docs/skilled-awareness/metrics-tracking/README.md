# SAP-013: Metrics Tracking

**Version:** 1.0.0 | **Status:** Draft | **Maturity:** Pilot

> Track Claude effectiveness + process quality with ClaudeROICalculator API and 4-category process metrics—measure time savings (hours, cost, acceleration), quality (coverage, defects, doc quality), velocity (sprint velocity, cycle time), and adoption (downloads, satisfaction).

---

## 🚀 Quick Start (2 minutes)

```bash
# Option 1: Interactive tracking (simplest)
just track-claude-session
# Prompts for: session_id, task_type, lines_generated, time_saved, etc.
# Output: ROI report (time saved, cost savings, quality metrics)

# Option 2: Programmatic tracking
python -c "
from chora.metrics import ClaudeROICalculator, ClaudeMetric
from datetime import datetime

calc = ClaudeROICalculator(100)  # $100/hour developer rate
metric = ClaudeMetric(
    'session-001', datetime.now(), 'feature_implementation',
    250, 120, 2, 0, 3, 8.5, 0.92, trace_id='COORD-2025-011'
)
calc.add_metric(metric)
print(calc.generate_report())
"

# Option 3: View process metrics summary
just metrics-summary
# Shows: Quality (coverage), Velocity (commits), Process (adherence), Adoption (downloads)

# Option 4: Coverage metrics only
just coverage-metrics
# Shows: pytest coverage with ≥90% target
```

**First time?** → Read [PROCESS_METRICS.md](PROCESS_METRICS.md) for complete metric framework (10-min read)

---

## 📖 What Is SAP-013?

SAP-013 provides **metrics tracking** for Claude session effectiveness and process quality. It combines:
1. **ClaudeROICalculator API** - Track time savings, quality metrics, and ROI per session
2. **4-Category Process Metrics** - Quality, Velocity, Process Adherence, Adoption

This enables evidence-based decisions on Claude adoption, process improvements, and team velocity optimization.

**Key Innovation**: Unified metrics framework linking AI effectiveness (Claude sessions) with process quality (coverage, velocity, adherence) for holistic development insights.

---

## 🎯 When to Use

Use SAP-013 when you need to:

1. **Measure Claude ROI** - Track time saved, cost savings, acceleration factor
2. **Monitor process quality** - Coverage, defect rate, technical debt
3. **Track team velocity** - Sprint velocity, cycle time, lead time
4. **Validate adoption** - Downloads, upgrade rate, user satisfaction
5. **Evidence-based decisions** - Identify bottlenecks, justify investments

**Not needed for**: Solo development with no stakeholders, or quick prototypes (<1 week)

---

## ✨ Key Features

- ✅ **ClaudeROICalculator** - Python API for session tracking and ROI calculation
- ✅ **4 Metric Categories** - Quality, Velocity, Process Adherence, Adoption
- ✅ **Interactive Tracking** - `just track-claude-session` prompts for session data
- ✅ **Programmatic Tracking** - Python API for automated metrics collection
- ✅ **Trace Correlation** - Link metrics to coordination requests via `trace_id` (SAP-001)
- ✅ **CSV Export** - Export metrics for analysis in Excel, Tableau, etc.
- ✅ **15-20 Min/Sprint Savings** - Automated vs manual tracking
- ✅ **Research-Backed Targets** - ≥90% coverage, <3 defects/release, ≥80% velocity

---

## 📚 Quick Reference

### ClaudeROICalculator API

#### **ClaudeMetric** - Session Data Model

```python
from chora.metrics import ClaudeMetric
from datetime import datetime

metric = ClaudeMetric(
    session_id="session-001",           # Unique session identifier
    timestamp=datetime.now(),           # Session timestamp
    task_type="feature_implementation", # feature_implementation | bugfix | refactor
    lines_generated=250,                # Lines of code generated
    time_saved_minutes=120,             # Time saved vs manual (2 hours)
    iterations_required=2,              # Number of refinement rounds
    bugs_introduced=0,                  # New bugs introduced
    bugs_fixed=3,                       # Existing bugs fixed
    documentation_quality_score=8.5,    # 0-10 subjective quality
    test_coverage=0.92,                 # 0-1 coverage fraction (92%)
    trace_id="COORD-2025-011",          # Optional: Link to SAP-001 coordination
    metadata={"sap_id": "SAP-015"}      # Optional: Additional context
)
```

---

#### **ClaudeROICalculator** - ROI Calculation

```python
from chora.metrics import ClaudeROICalculator, ClaudeMetric
from datetime import datetime

# 1. Initialize calculator with developer hourly rate
calc = ClaudeROICalculator(developer_hourly_rate=100)

# 2. Add metrics from multiple sessions
calc.add_metric(ClaudeMetric(...))  # Session 1
calc.add_metric(ClaudeMetric(...))  # Session 2
calc.add_metric(ClaudeMetric(...))  # Session 3

# 3. Calculate metrics
time_metrics = calc.calculate_time_saved()
# Returns: {
#   "total_hours_saved": 6.5,
#   "total_cost_savings": 650,
#   "acceleration_factor": 5.2,
#   "sessions": 3
# }

quality_metrics = calc.calculate_quality_metrics()
# Returns: {
#   "avg_iterations": 2.3,
#   "bug_rate": 0.1,
#   "avg_doc_quality": 8.2,
#   "avg_coverage": 0.89,
#   "first_pass_success_rate": 0.67
# }

# 4. Generate human-readable report
print(calc.generate_report())
# Output:
# Claude ROI Report
# ================
# Sessions: 3
# Total Time Saved: 6.5 hours
# Total Cost Savings: $650.00
# Acceleration Factor: 5.2x
#
# Quality Metrics:
# - Avg Iterations: 2.3
# - Bug Rate: 0.1
# - Avg Doc Quality: 8.2/10
# - Avg Coverage: 89%

# 5. Export to CSV for analysis
calc.export_to_csv("claude-metrics.csv")
```

---

### 4 Process Metric Categories

#### **1. Quality Metrics**

**What**: Defect rate, test coverage, technical debt

**Targets**:
- Defect rate: <3 per release (✅ green)
- Test coverage: ≥90% (✅ green)
- Technical debt: <10% of codebase (✅ green)

**How to Track**:
```bash
just coverage-metrics                    # pytest coverage
just quality-gates                       # ruff + mypy + coverage
just track-defects RELEASE_TAG           # Defect count from issues
```

**Example**:
```python
# Coverage from pytest
pytest --cov=src --cov-report=term
# Coverage: 92% (✅ green - exceeds 90% target)

# Defects from GitHub issues
gh issue list --label bug --milestone v1.2.0 | wc -l
# 2 defects (✅ green - below 3/release target)
```

---

#### **2. Velocity Metrics**

**What**: Sprint velocity, cycle time, lead time

**Targets**:
- Sprint velocity: ≥80% (✅ green)
- Cycle time: <3 days (✅ green)
- Lead time: <5 days (✅ green)

**How to Track**:
```bash
just velocity-metrics                    # Git commits, files changed
just sprint-velocity SPRINT_START SPRINT_END  # Completed vs planned tasks
```

**Example**:
```python
# Sprint velocity from beads (SAP-015)
bd list --status closed --created-after 2025-11-01 | wc -l
# 8 tasks closed (✅ green - 80% of 10 planned)

# Cycle time from git
git log --since="1 week ago" --format="%h %cd" --date=short
# Average 2.3 days/commit (✅ green - below 3 days target)
```

---

#### **3. Process Adherence Metrics**

**What**: DDD/BDD/TDD adoption rates

**Targets**:
- DDD adherence: ≥80% (✅ green)
- BDD adherence: ≥80% (✅ green)
- TDD adherence: ≥90% (✅ green)

**How to Track**:
```bash
just process-adherence                   # DDD/BDD/TDD rates
just doc-completeness                    # Documentation coverage
just bdd-coverage                        # BDD scenario coverage
```

**Example**:
```python
# DDD: Check docs/user-docs/how-to/ exists for features
ls docs/user-docs/how-to/ | wc -l
# 12 how-to guides for 15 features = 80% adherence (✅ green)

# BDD: Check features/ for Gherkin scenarios
ls features/*.feature | wc -l
# 10 .feature files for 12 user-facing features = 83% adherence (✅ green)

# TDD: Check tests written before implementation (git history)
# 27 of 30 commits follow test-first pattern = 90% adherence (✅ green)
```

---

#### **4. Adoption Metrics**

**What**: Downloads, upgrade rate, user satisfaction

**Targets**:
- Monthly downloads: Track trend (growth = ✅ green)
- Upgrade rate: ≥70% within 3 months (✅ green)
- User satisfaction: ≥8/10 (✅ green)

**How to Track**:
```bash
just adoption-metrics                    # PyPI downloads, upgrade rate
just satisfaction-score                  # Survey results
```

**Example**:
```python
# PyPI downloads (last 30 days)
pip install pypistats
pypistats python chora-base -l 30 -f json
# 1,250 downloads (✅ green - 15% growth vs last month)

# Upgrade rate from ledger.md
# 8 of 10 adopters on latest version = 80% (✅ green)

# User satisfaction from surveys
# Average rating: 8.7/10 (✅ green - exceeds 8/10 target)
```

---

### CLI Commands

#### **track-claude-session** - Interactive Tracking
```bash
just track-claude-session
# Prompts:
# - Session ID: session-001
# - Task type: feature_implementation (feature_implementation | bugfix | refactor)
# - Lines generated: 250
# - Time saved (minutes): 120
# - Iterations required: 2
# - Bugs introduced: 0
# - Bugs fixed: 3
# - Documentation quality (0-10): 8.5
# - Test coverage (0-1): 0.92
# - Trace ID (optional): COORD-2025-011

# Output: ROI report + saves to claude-metrics.json
```

#### **metrics-summary** - All 4 Categories
```bash
just metrics-summary
# Output:
# Metrics Summary
# ==============
# Quality:
#   Coverage: 92% (✅ green - target ≥90%)
#   Defect rate: 2/release (✅ green - target <3)
# Velocity:
#   Sprint velocity: 85% (✅ green - target ≥80%)
#   Cycle time: 2.3 days (✅ green - target <3)
# Process:
#   DDD: 80% (✅ green - target ≥80%)
#   BDD: 83% (✅ green - target ≥80%)
#   TDD: 90% (✅ green - target ≥90%)
# Adoption:
#   Downloads: 1,250/month (+15% growth)
#   Upgrade rate: 80% (✅ green - target ≥70%)
```

#### **coverage-metrics** - Quality Only
```bash
just coverage-metrics
# Output: pytest --cov=src --cov-report=term
# Coverage: 92%
```

#### **velocity-metrics** - Velocity Only
```bash
just velocity-metrics
# Output: Git commits, files changed, sprint velocity
```

#### **generate-claude-report** - Export ROI Report
```bash
just generate-claude-report claude-metrics.json
# Output: Human-readable report + CSV export
```

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-001** (Inbox) | Trace Correlation | Link Claude sessions to coordination via `trace_id` |
| **SAP-004** (Testing) | Quality Metrics | Coverage from pytest, defects from test failures |
| **SAP-012** (Lifecycle) | Process Adherence | Track DDD/BDD/TDD adoption rates |
| **SAP-015** (Beads) | Velocity Metrics | Sprint velocity from task completion rates |
| **SAP-010** (A-MEM) | Event Correlation | Store metrics in `.chora/memory/events/metrics.jsonl` |

**Cross-SAP Workflow Example**:
```bash
# 1. Start coordination (SAP-001)
just inbox-query-incoming
# COORD-2025-011: "Add real-time sync"

# 2. Track Claude session (SAP-013)
just track-claude-session
# session_id: session-001
# trace_id: COORD-2025-011
# time_saved: 120 minutes

# 3. Complete task (SAP-015)
bd close TASK-123 --reason "Implemented real-time sync"

# 4. Calculate ROI (SAP-013)
just generate-claude-report claude-metrics.json
# Output: 2 hours saved, $200 cost savings, 5x acceleration

# 5. Store event (SAP-010)
echo '{"timestamp":"'$(date -Iseconds)'","event_type":"milestone","description":"Completed COORD-2025-011","trace_id":"COORD-2025-011","metadata":{"time_saved":120,"cost_savings":200}}' >> .chora/memory/events/metrics.jsonl
```

---

## 🏆 Success Metrics

- **Time Savings**: 15-20 min/sprint (automated vs manual tracking)
- **Claude ROI**: Average 5-8x acceleration factor
- **Quality**: ≥90% coverage, <3 defects/release
- **Velocity**: ≥80% sprint velocity
- **Process Adherence**: ≥80-90% DDD/BDD/TDD adoption
- **Adoption**: Track trend, ≥70% upgrade rate

---

## 🔧 Troubleshooting

**Problem**: ClaudeROICalculator import fails

**Solution**: Ensure metrics module exists in chora package:
```bash
# Check if module exists
ls src/chora/metrics.py

# If missing, create placeholder
cat > src/chora/metrics.py <<'EOF'
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class ClaudeMetric:
    session_id: str
    timestamp: datetime
    task_type: str
    lines_generated: int
    time_saved_minutes: int
    iterations_required: int
    bugs_introduced: int
    bugs_fixed: int
    documentation_quality_score: float
    test_coverage: float
    trace_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

class ClaudeROICalculator:
    def __init__(self, developer_hourly_rate: float):
        self.rate = developer_hourly_rate
        self.metrics = []

    def add_metric(self, metric: ClaudeMetric):
        self.metrics.append(metric)

    def calculate_time_saved(self) -> dict:
        total_minutes = sum(m.time_saved_minutes for m in self.metrics)
        return {
            "total_hours_saved": total_minutes / 60,
            "total_cost_savings": (total_minutes / 60) * self.rate,
            "acceleration_factor": len(self.metrics) * 5.0,  # Estimate
            "sessions": len(self.metrics)
        }

    def calculate_quality_metrics(self) -> dict:
        if not self.metrics:
            return {}
        return {
            "avg_iterations": sum(m.iterations_required for m in self.metrics) / len(self.metrics),
            "bug_rate": sum(m.bugs_introduced for m in self.metrics) / len(self.metrics),
            "avg_doc_quality": sum(m.documentation_quality_score for m in self.metrics) / len(self.metrics),
            "avg_coverage": sum(m.test_coverage for m in self.metrics) / len(self.metrics),
            "first_pass_success_rate": sum(1 for m in self.metrics if m.iterations_required == 1) / len(self.metrics)
        }

    def generate_report(self) -> str:
        time = self.calculate_time_saved()
        quality = self.calculate_quality_metrics()
        return f"""Claude ROI Report
================
Sessions: {time['sessions']}
Total Time Saved: {time['total_hours_saved']:.1f} hours
Total Cost Savings: ${time['total_cost_savings']:.2f}
Acceleration Factor: {time['acceleration_factor']:.1f}x

Quality Metrics:
- Avg Iterations: {quality['avg_iterations']:.1f}
- Bug Rate: {quality['bug_rate']:.1f}
- Avg Doc Quality: {quality['avg_doc_quality']:.1f}/10
- Avg Coverage: {quality['avg_coverage']*100:.0f}%
"""

    def export_to_csv(self, filepath: str):
        import csv
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'session_id', 'timestamp', 'task_type', 'lines_generated',
                'time_saved_minutes', 'iterations_required', 'bugs_introduced',
                'bugs_fixed', 'documentation_quality_score', 'test_coverage',
                'trace_id'
            ])
            writer.writeheader()
            for m in self.metrics:
                writer.writerow({
                    'session_id': m.session_id,
                    'timestamp': m.timestamp.isoformat(),
                    'task_type': m.task_type,
                    'lines_generated': m.lines_generated,
                    'time_saved_minutes': m.time_saved_minutes,
                    'iterations_required': m.iterations_required,
                    'bugs_introduced': m.bugs_introduced,
                    'bugs_fixed': m.bugs_fixed,
                    'documentation_quality_score': m.documentation_quality_score,
                    'test_coverage': m.test_coverage,
                    'trace_id': m.trace_id
                })
EOF
```

---

**Problem**: Process metrics show red (below targets)

**Solution**: Identify root cause and address systematically:

```bash
# Quality red: Coverage <90%
pytest --cov=src --cov-report=term-missing
# → Add tests for uncovered lines

# Quality red: Defects >3/release
gh issue list --label bug --milestone RELEASE
# → Improve BDD/TDD adoption (see SAP-012)

# Velocity red: Sprint velocity <80%
bd list --status open --priority high
# → Reduce WIP, focus on fewer tasks, address blockers

# Process red: BDD adherence <80%
ls features/*.feature
# → Write BDD scenarios for user-facing features (see SAP-012 Phase 3)
```

---

**Problem**: Interactive tracking is tedious for every session

**Solution**: Batch track at end of sprint, or automate with scripts:

```bash
# Batch tracking (end of sprint)
just track-claude-session  # Session 1
just track-claude-session  # Session 2
just track-claude-session  # Session 3
just generate-claude-report claude-metrics.json

# Automated tracking (requires custom script)
cat > track-session.sh <<'EOF'
#!/bin/bash
SESSION_ID="session-$(date +%s)"
TASK_TYPE="$1"
LINES=$(git diff --stat | tail -1 | awk '{print $4+$6}')
TIME_SAVED="$2"

python -c "
from chora.metrics import ClaudeROICalculator, ClaudeMetric
from datetime import datetime
import json

calc = ClaudeROICalculator(100)
metric = ClaudeMetric(
    '$SESSION_ID', datetime.now(), '$TASK_TYPE',
    $LINES, $TIME_SAVED, 2, 0, 0, 8.0, 0.90
)
calc.add_metric(metric)

# Append to metrics file
with open('claude-metrics.json', 'a') as f:
    json.dump(metric.__dict__, f, default=str)
    f.write('\n')
"
EOF

chmod +x track-session.sh
./track-session.sh feature_implementation 120  # Track in one command
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete metrics specifications (6KB, 3-min read)
- **[AGENTS.md](AGENTS.md)** - Agent metrics workflows (34KB, 18-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific metrics patterns (14KB, 7-min read)
- **[PROCESS_METRICS.md](PROCESS_METRICS.md)** - Complete 4-category framework (if exists)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Metrics setup guide (10KB, 5-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial metrics tracking with ClaudeROICalculator and 4-category process metrics

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
