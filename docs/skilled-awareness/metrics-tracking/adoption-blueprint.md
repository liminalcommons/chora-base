---
sap_id: SAP-013
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: adoption-blueprint
---

# Adoption Blueprint: Metrics Tracking

**SAP ID**: SAP-013
**Capability Name**: metrics-tracking
**Version**: 1.0.0

---

## Installing the SAP

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-013 --source /path/to/chora-base
```

**What This Installs**:
- metrics-tracking capability documentation (5 artifacts)
- ClaudeROICalculator utility (utils/claude_metrics.py)
- PROCESS_METRICS.md template

### Part of Sets

This SAP is included in:
- full

To install a complete set:
```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/metrics-tracking/*.md
ls utils/claude_metrics.py
```

---

## Quick Start (30 Minutes)

### Step 1: Copy Files

```bash
# ClaudeROICalculator (if not already in project)
cp <chora-base>/static-template/src/__package_name__/utils/claude_metrics.py \
   src/<your-package>/utils/

# Process metrics template
cp <chora-base>/static-template/project-docs/metrics/PROCESS_METRICS.md \
   project-docs/metrics/
```

### Step 2: Track First Claude Session

```python
from mypackage.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator

calculator = ClaudeROICalculator(developer_hourly_rate=100)
metric = ClaudeMetric(
    session_id="session-001",
    timestamp=datetime.now(),
    task_type="feature_implementation",
    lines_generated=250,
    time_saved_minutes=120,
    iterations_required=2,
    bugs_introduced=0,
    bugs_fixed=3,
    documentation_quality_score=8.5,
    test_coverage=0.92
)
calculator.add_metric(metric)
print(calculator.generate_report())
```

### Step 3: Set Baselines

Update `PROCESS_METRICS.md` with current project baselines:
- Test coverage: ____%
- Defect rate: ___ per release
- Sprint velocity: ____%

---

## Adoption Levels

### Level 1: Claude ROI (Week 1) - 1 hour

**Goal**: Track Claude effectiveness

**Steps**:
1. ✅ Copy claude_metrics.py
2. ✅ Track 3 sessions
3. ✅ Generate first report

**Validation**: ROI report shows time/cost savings

---

### Level 2: Process Metrics (Week 2) - 2 hours

**Goal**: Track quality and velocity

**Steps**:
1. ✅ Copy PROCESS_METRICS.md
2. ✅ Set targets (defect rate, coverage, velocity)
3. ✅ Track 1 sprint of metrics

**Validation**: Sprint dashboard updated with 3+ metrics

---

### Level 3: Continuous Tracking (Month 1) - 4 hours

**Goal**: Automated and regular metrics collection

**Steps**:
1. ✅ Automate coverage tracking (CI/CD)
2. ✅ Weekly sprint updates
3. ✅ Release metrics (1 week post-release)
4. ✅ Quarterly trends analysis

**Validation**: 3 months of data, trends visible

---

## Validation Checklist

- [ ] ClaudeROICalculator tracking ≥5 sessions
- [ ] Sprint metrics updated weekly
- [ ] Release metrics tracked (1 week post-release)
- [ ] Targets defined (defect rate, coverage, velocity)
- [ ] ROI demonstrable (hours saved, cost savings)

---

## Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Metrics Tracking capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover ClaudeROICalculator and process metrics
- Quick reference for metrics tracking
- Links to metrics documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Metrics Tracking

Claude ROI calculator and process metrics for quality and velocity tracking.

**Documentation**: [docs/skilled-awareness/metrics-tracking/](docs/skilled-awareness/metrics-tracking/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/metrics-tracking/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/metrics-tracking/awareness-guide.md)

**Key Metrics**:
- Claude ROI: Time saved, cost savings, quality improvement
- Process metrics: Test coverage, defect rate, sprint velocity
- Quality gates: Coverage ≥85%, defects <3 per release
```

**Validation**:
```bash
grep "Metrics Tracking" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## Related Documents

- [capability-charter.md](capability-charter.md)
- [protocol-spec.md](protocol-spec.md)
- [awareness-guide.md](awareness-guide.md)
- [PROCESS_METRICS.md](../../../static-template/project-docs/metrics/PROCESS_METRICS.md)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for metrics-tracking SAP
