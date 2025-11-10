# SAP-019: SAP Self-Evaluation Framework

**Pattern ID**: SAP-019
**Pattern Name**: sap-self-evaluation
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-30

---

## 🚀 Quick Start (30 seconds)

```bash
# Quick check: Is SAP-004 installed and functional?
python scripts/sap-evaluator.py --quick SAP-004

# Deep dive: Detailed gap analysis with action plan
python scripts/sap-evaluator.py --deep SAP-004

# Strategic analysis: Roadmap for all SAPs
python scripts/sap-evaluator.py --strategic

# Export JSON for CI/CD integration
python scripts/sap-evaluator.py --quick SAP-004 --json > sap-004-eval.json
```

**Expected output** (quick check):
```
SAP-004 (Testing Framework) - Quick Check
==========================================
✅ Installed (5/5 artifacts present)
✅ Tests pass (pytest: 12/12 passed)
❌ Coverage below target (65% < 85%)
✅ CI integration present

Current Level: 1
Next Milestone: Level 2 (85% coverage)
Estimated Effort: 3 hours
```

---

## What Is It?

SAP-019 provides a **progressive evaluation protocol** for assessing SAP adoption depth, identifying gaps, and generating actionable improvement roadmaps.

### Purpose

- **Rapid Assessment**: Quick check in 30 seconds to verify installation and basic functionality
- **Deep Analysis**: LLM-driven content analysis in 5 minutes with concrete next steps
- **Strategic Planning**: 30-minute roadmap generation across all SAPs with sprint breakdown
- **Automated Validation**: Exit codes and file checks for CI/CD integration
- **Actionable Output**: Concrete actions with tool, file path, and exact content (not just scores)

### How It Works

1. **Quick Check**: Automated validation (files exist, commands pass, exit codes)
2. **Deep Dive**: LLM reads files, compares to adoption criteria, identifies gaps
3. **Strategic Analysis**: Timeline trends, gap prioritization, roadmap generation
4. **Action Planning**: Agent-executable steps with estimated effort and validation

---

## When to Use

### ✅ Use SAP Self-Evaluation When

- **Session Startup**: Quick check to see if SAPs are functional before starting work
- **Sprint Planning**: Strategic analysis to identify highest-priority improvements
- **After Adoption**: Deep dive to verify SAP is integrated correctly
- **CI/CD Integration**: Automated validation in GitHub Actions (JSON export)
- **Troubleshooting**: Quick check fails → run deep dive to identify root cause
- **Quarterly Reviews**: Strategic analysis to track adoption trends over time
- **Gap Prioritization**: Multiple SAPs installed → which to improve next?

### ❌ Don't Use When

- **Initial SAP Installation**: Use adoption-blueprint.md first, then evaluate
- **Real-time Development**: Evaluation is diagnostic, not a development workflow
- **Non-SAP Projects**: Framework designed specifically for SAP ecosystem

---

## Key Features

### 3 Evaluation Depths

1. **Quick Check** (30 seconds)
   - Automated validation (file existence, exit codes)
   - Level assessment (0/1/2/3)
   - Next milestone identification
   - No LLM required

2. **Deep Dive** (5 minutes)
   - LLM content analysis (AGENTS.md, test files, CI workflows)
   - Gap identification (Installation, Integration, Quality, Optimization)
   - Action planning (concrete steps with tool, file, content)
   - Effort estimation (hours to next level)

3. **Strategic Analysis** (30 minutes)
   - Timeline trends across all SAPs
   - Gap prioritization (impact × effort scoring)
   - Roadmap generation (quarterly goals, sprint breakdown)
   - ROI tracking (hours invested vs. time saved)

### 4 Adoption Levels (Per SAP)

- **Level 0**: Not installed (missing artifacts)
- **Level 1**: Installed, basic capability functional
- **Level 2**: Integrated into workflows, standard usage patterns
- **Level 3**: Fully automated, optimized, comprehensive usage

### 4 Gap Types

- **Installation Gap**: Required artifacts missing (blocks Level 1)
- **Integration Gap**: Installed but not used in practice (blocks Level 2)
- **Quality Gap**: Used but incorrectly/incompletely (blocks Level 2)
- **Optimization Gap**: Used correctly but not optimized (blocks Level 3)

---

## Quick Reference

### Evaluation Commands

```bash
# Quick check (30s)
python scripts/sap-evaluator.py --quick SAP-004

# Deep dive (5min)
python scripts/sap-evaluator.py --deep SAP-004

# Strategic analysis (30min)
python scripts/sap-evaluator.py --strategic

# JSON export
python scripts/sap-evaluator.py --quick SAP-004 --json
```

### Data Models

**EvaluationResult**: Single SAP assessment
- `sap_id`, `current_level`, `completion_percent`
- `validation_results` (dict of automated checks)
- `gaps` (list of Gap objects)
- `recommended_actions` (list of Action objects)
- `estimated_effort_hours`

**Gap**: Identified improvement opportunity
- `gap_type` (installation | integration | quality | optimization)
- `impact` (high | medium | low)
- `effort` (high | medium | low)
- `priority` (P0 | P1 | P2)
- `actions` (list of Action objects)

**Action**: Concrete step to improve adoption
- `tool` (Read | Edit | Bash)
- `file_path`, `location`, `content`, `command`
- `rationale`, `expected_outcome`, `validation_command`
- `estimated_minutes`, `sequence`, `depends_on`

**AdoptionRoadmap**: Strategic plan over time
- `total_saps_installed`, `adoption_distribution`
- `quarterly_goals`, `target_saps_to_install`
- `priority_gaps` (ranked list with sprint assignment)
- `this_sprint`, `next_sprint`, `future_sprints`

### Level Criteria (Example: SAP-004 Testing)

**Level 1**: Basic testing infrastructure
- ✅ pytest configured in pyproject.toml
- ✅ tests/ directory with sample tests
- ✅ Tests pass (`pytest` exit code 0)

**Level 2**: Integrated testing workflow
- ✅ Coverage ≥85% (`pytest --cov=src`)
- ✅ CI/CD integration (.github/workflows/test.yml)
- ✅ Pre-commit hooks run tests

**Level 3**: Comprehensive testing strategy
- ✅ BDD scenarios (Gherkin features)
- ✅ TDD workflow documented (AGENTS.md)
- ✅ Coverage gaps tracked and prioritized

### Priority Scoring

```python
# Gap priority calculation
impact_score = {
    "high": 1.0,
    "medium": 0.5,
    "low": 0.25
}[gap.impact]

effort_score = {
    "low": 1.0,
    "medium": 0.5,
    "high": 0.25
}[gap.effort]

priority_score = impact_score / effort_score  # Higher = more important

# Example:
# Gap A: high impact, low effort → 1.0 / 1.0 = 1.0 (P0)
# Gap B: high impact, high effort → 1.0 / 0.25 = 4.0 (P0)
# Gap C: medium impact, medium effort → 0.5 / 0.5 = 1.0 (P1)
# Gap D: low impact, high effort → 0.25 / 0.25 = 1.0 (P2)
```

---

## Integration with Other SAPs

### SAP-013 (Metrics Tracking)
- **Link**: Evaluation results feed into metrics dashboard
- **How**: Export JSON → parse into ClaudeROICalculator
- **Benefit**: Track adoption progress over time

### SAP-015 (Task Tracking)
- **Link**: Recommended actions → bead creation
- **How**: `bd create "Fix SAP-004 coverage gap" --priority high`
- **Benefit**: Persistent task memory for multi-session work

### SAP-012 (Development Lifecycle)
- **Link**: Strategic analysis → sprint planning
- **How**: Priority gaps → sprint plan tasks
- **Benefit**: Data-driven sprint prioritization

### SAP-027 (Dogfooding Patterns)
- **Link**: Deep dive validates pilot criteria
- **How**: Level 2 adoption = pilot success threshold
- **Benefit**: GO/NO-GO decision criteria

### SAP-000 (SAP Framework)
- **Link**: Evaluates all SAPs using framework artifacts
- **How**: Checks for 5 required artifacts (capability-charter, protocol-spec, etc.)
- **Benefit**: Ensures SAP compliance

---

## Success Metrics

### Quick Check (30s)
- ✅ **Installation Status**: 5/5 artifacts present
- ✅ **Validation Results**: Automated checks pass/fail
- ✅ **Level Assessment**: 0/1/2/3 with completion %
- ✅ **Next Milestone**: Concrete goal with effort estimate

### Deep Dive (5min)
- ✅ **Gap Identification**: 4-8 gaps per SAP with priority (P0/P1/P2)
- ✅ **Action Planning**: 3-5 actions per gap with tool, file, content
- ✅ **Effort Estimation**: Hours to next level (±20% accuracy)
- ✅ **Confidence Assessment**: High/medium/low based on data quality

### Strategic Analysis (30min)
- ✅ **Adoption Distribution**: Level 0/1/2/3 counts across all SAPs
- ✅ **Gap Prioritization**: Top 10 gaps ranked by impact/effort
- ✅ **Sprint Breakdown**: This/next/future sprints with deliverables
- ✅ **ROI Tracking**: Hours invested vs. time saved (target: 3x)

### CI/CD Integration
- ✅ **JSON Export**: Machine-readable results for automation
- ✅ **Exit Codes**: 0 = success, 1 = failure (for CI/CD gating)
- ✅ **Threshold Validation**: Fail if adoption level < target

---

## Troubleshooting

### Problem: Quick check passes but deep dive finds gaps

**Symptom**: Quick check shows "✅ Level 2" but deep dive identifies integration gaps

**Cause**: Automated validation only checks exit codes, not content quality

**Fix**: Deep dive uses LLM to analyze content (e.g., test coverage metrics vs. actual test quality)

**Prevention**: Run deep dive after initial adoption to verify integration

---

### Problem: Action steps too generic ("improve coverage")

**Symptom**: Recommended actions lack concrete file paths or content

**Cause**: LLM prompt doesn't include enough context from repo files

**Fix**: Re-run deep dive with `--verbose` to include more file content in LLM prompt

**Example**:
```bash
# Generic action
Action: "Improve test coverage"

# Concrete action (verbose mode)
Action: "Add unit tests for src/utils/parser.py lines 45-78 (uncovered)"
Tool: Edit
File: tests/test_utils.py
Content: |
  def test_parse_edge_case():
      result = parse("edge case input")
      assert result.status == "success"
```

---

### Problem: Strategic analysis shows low ROI (<3x)

**Symptom**: Roadmap suggests many SAP adoptions but estimated effort > time saved

**Cause**: Installing SAPs that don't match project needs

**Fix**: Review SAP catalog, prioritize SAPs with high impact for your domain

**Example**:
```
Low ROI: Installing SAP-011 (Docker) for a non-containerized project
High ROI: Installing SAP-015 (Task Tracking) for multi-session work
```

**Prevention**: Use SAP-027 (Dogfooding) to pilot SAPs before full adoption

---

### Problem: Evaluation fails with "SAP not found"

**Symptom**: `python scripts/sap-evaluator.py --quick SAP-004` → "SAP-004 not found"

**Cause**: SAP directory name doesn't match catalog entry

**Fix**: Check sap-catalog.json for correct SAP name

**Example**:
```bash
# Check catalog
grep -A 5 '"id": "SAP-004"' sap-catalog.json

# Output:
# "id": "SAP-004",
# "name": "testing-framework",  ← Use this name

# Correct path
docs/skilled-awareness/testing-framework/
```

---

### Problem: Deep dive takes >5 minutes

**Symptom**: LLM analysis hangs or times out

**Cause**: Reading too many files (large repo, many SAPs)

**Fix**: Specify SAP explicitly, avoid strategic analysis on large repos

**Workaround**:
```bash
# Fast: Single SAP deep dive
python scripts/sap-evaluator.py --deep SAP-004

# Slow: Strategic analysis (all SAPs)
python scripts/sap-evaluator.py --strategic  # 30min for 30+ SAPs
```

---

## Learn More

### Documentation

- **[Capability Charter](capability-charter.md)**: Problem statement, solution design, success criteria
- **[Protocol Spec](protocol-spec.md)**: Complete technical specification (data models, evaluation protocols)
- **[Awareness Guide](awareness-guide.md)**: Detailed workflows, LLM prompt templates, examples
- **[Adoption Blueprint](adoption-blueprint.md)**: Step-by-step installation and setup
- **[Ledger](ledger.md)**: Adoption tracking, version history, active deployments

### Related SAPs

- **[SAP-000 (sap-framework)](../sap-framework/)**: Foundation for all SAPs (5 artifacts)
- **[SAP-013 (metrics-tracking)](../metrics-tracking/)**: ROI calculation and metrics dashboard
- **[SAP-015 (task-tracking)](../task-tracking/)**: Persistent memory for recommended actions
- **[SAP-027 (dogfooding-patterns)](../dogfooding-patterns/)**: Pilot validation and GO/NO-GO criteria
- **[SAP-012 (development-lifecycle)](../development-lifecycle/)**: Sprint planning integration

### Examples

**Quick Check Output**:
```bash
SAP-015 (Task Tracking) - Quick Check
======================================
✅ Installed (5/5 artifacts present)
✅ beads CLI functional (v1.2.0)
✅ .beads/issues.jsonl present
❌ No tasks created yet

Current Level: 1
Next Milestone: Level 2 (5+ tasks created)
Estimated Effort: 1 hour
```

**Deep Dive Output** (excerpt):
```markdown
# SAP-015 Deep Dive Analysis

## Current State
- Level: 1 (Installed, basic functionality)
- Completion: 40% toward Level 2

## Gaps Identified

### Gap 1: Integration Gap (P0)
**Title**: beads CLI not integrated into daily workflow
**Impact**: High (no context restoration between sessions)
**Effort**: Low (add to session startup)

**Actions**:
1. Add `bd ready --json` to session startup routine
   - Tool: Edit
   - File: .chora/CLAUDE.md
   - Location: Session Startup section
   - Content: "1. Check ready tasks: `bd ready --json`"
   - Estimated: 5 minutes

2. Create sample task to test workflow
   - Tool: Bash
   - Command: `bd create "Test task tracking" --priority medium`
   - Validation: `bd list --status open --json`
   - Estimated: 2 minutes
```

**Strategic Analysis Output** (excerpt):
```markdown
# Q1-2026 SAP Adoption Roadmap

## Current State (2025-11-09)
- Total SAPs installed: 12
- Adoption distribution:
  - Level 3: 2 SAPs (SAP-004, SAP-005)
  - Level 2: 3 SAPs (SAP-001, SAP-012, SAP-013)
  - Level 1: 7 SAPs (SAP-010, SAP-015, SAP-027, ...)
- Average level: 1.6
- Total hours invested: 45 hours

## Quarterly Goals
- Target SAPs to install: 5 (SAP-020, SAP-033, SAP-034, SAP-041, SAP-042)
- Target Level 2 count: 8 SAPs
- Target ROI: 3.5x

## Priority Gaps (Top 5)

### 1. SAP-015: Integration Gap (P0)
- Rank: 1
- Impact: High (context restoration)
- Effort: Low (1 hour)
- Sprint: This sprint
- Deliverables: Session startup routine, 5+ tasks created
- Blocks: Efficient multi-session work

### 2. SAP-004: Coverage Gap (P0)
- Rank: 2
- Impact: High (prevent bugs)
- Effort: Medium (3 hours)
- Sprint: This sprint
- Deliverables: 85%+ coverage, gap tracking
```

---

## Version History

- **1.0.0** (2025-10-30): Initial SAP-019 release
  - Quick check protocol (30s automated validation)
  - Deep dive protocol (5min LLM analysis)
  - Strategic analysis protocol (30min roadmap generation)
  - 4 adoption levels (0/1/2/3)
  - 4 gap types (installation, integration, quality, optimization)
  - Agent-executable action planning
  - JSON export for CI/CD integration
  - Integration with SAP-013, SAP-015, SAP-012, SAP-027

---

**Next Steps**:
1. Read [adoption-blueprint.md](adoption-blueprint.md) for installation instructions
2. Run quick check on installed SAPs: `python scripts/sap-evaluator.py --quick SAP-004`
3. Identify gaps with deep dive: `python scripts/sap-evaluator.py --deep SAP-004`
4. Review strategic roadmap: `python scripts/sap-evaluator.py --strategic`
