# AGENTS.md - Metrics Framework (SAP-013)

**Domain**: Metrics & Measurement
**SAP**: SAP-013 (metrics-framework)
**Version**: 1.1.0
**Last Updated**: 2025-10-31

---

## Overview

This is the domain-specific AGENTS.md file for the metrics framework (SAP-013). It provides context for agents working with metrics collection, ROI calculation, velocity tracking, and quality measurement.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides metrics-specific context

---

## User Signal Patterns

### ROI & Value Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "calculate ROI" | run_claude_roi_calculator() | python scripts/claude-roi-calculator.py | Interactive calculator |
| "is this worth it" | run_claude_roi_calculator() | Same command | Natural variation |
| "show value" | display_roi_results() | Read previous calculation | Display saved results |
| "time savings" | calculate_time_savings() | ROI calculator → time saved | Specific metric |
| "cost benefit" | calculate_cost_benefit() | ROI calculator → full analysis | Comprehensive view |

### Velocity & Progress Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "check velocity" | calculate_sprint_velocity() | Read sprint plans, count tasks | Completion rate |
| "show progress" | display_progress_metrics() | Count completed vs total tasks | Overall progress |
| "sprint stats" | display_sprint_statistics() | Aggregate sprint data | Historical view |
| "completion rate" | calculate_completion_rate() | Completed / Total tasks | Percentage |

### Quality Metrics Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "quality metrics" | display_quality_metrics() | Coverage + lint + type check | All quality data |
| "defect rate" | calculate_defect_rate() | Count failing tests / total | Bug density |
| "coverage trend" | display_coverage_trend() | Historical coverage data | Track improvements |
| "quality score" | calculate_quality_score() | Aggregate quality metrics | Single score |

### Documentation Metrics Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "doc coverage" | calculate_doc_coverage() | Count documented vs total | Documentation completeness |
| "broken links" | validate_links() | bash scripts/validate-links.sh | Link validation |
| "how many broken links" | count_broken_links() | Parse validate-links.sh output | Count only |
| "fix broken links" | fix_broken_links() | Update links based on validation | Repair workflow |

### Traceability Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "show trace" | display_trace_events() | Read inbox/coordination/events.jsonl | Event log |
| "trace coord-NNN" | filter_trace_by_id(id) | grep CHORA_TRACE_ID=coord-NNN | Specific coordination |
| "recent events" | display_recent_events(N) | tail -N events.jsonl | Last N events |
| "event timeline" | display_event_timeline() | Parse events.jsonl by timestamp | Chronological view |

### Common Variations

**ROI Queries**:
- "calculate ROI" / "is this worth it" / "show value" → run_claude_roi_calculator()
- "time saved" / "efficiency gain" / "productivity boost" → calculate_time_savings()

**Quality Queries**:
- "quality metrics" / "how's quality" / "quality score" → display_quality_metrics()
- "coverage?" / "test coverage" / "how's our coverage" → validate_coverage() (see SAP-004)

**Progress Queries**:
- "velocity" / "progress" / "completion rate" → calculate_sprint_velocity()
- "sprint stats" / "sprint progress" / "how far along" → display_sprint_statistics()

**Documentation Queries**:
- "doc coverage" / "documentation completeness" → calculate_doc_coverage()
- "broken links" / "validate links" / "check links" → validate_links()

---

## Metrics Framework Quick Reference

### ROI Calculator (Claude Code)

**Tool**: `scripts/claude-roi-calculator.py`

**Purpose**: Calculate return on investment for Claude Code adoption

**Usage**:
```bash
python scripts/claude-roi-calculator.py
```

**Interactive Prompts**:
1. Work type (coding, debugging, documentation, testing, refactoring, learning)
2. Experience level (beginner, intermediate, advanced, expert)
3. Task complexity (simple, moderate, complex, very_complex)
4. Weekly hours with Claude Code
5. Time savings estimate (% of weekly hours)

**Output**:
```
=== ROI CALCULATION RESULTS ===

Time Savings:
- Weekly hours saved: 5.0 hours
- Monthly hours saved: 20.0 hours
- Yearly hours saved: 240.0 hours

Value:
- Hourly rate: $100/hour
- Weekly value: $500
- Monthly value: $2,000
- Yearly value: $24,000

ROI:
- Claude Code cost: $20/month ($240/year)
- Net yearly value: $23,760
- ROI: 9,900%

Break-even: Achieved in < 1 month
```

**Saved Results**: Results saved to `.chora/metrics/roi-calculation-YYYY-MM-DD.json`

### Velocity Tracking

**Metric**: Sprint velocity = Completed tasks / Total tasks

**Calculation**:
```bash
# Count completed tasks in sprint
grep -c "- \[x\]" docs/project-docs/sprints/sprint-05.md

# Count total tasks in sprint
grep -c "^- \[" docs/project-docs/sprints/sprint-05.md

# Calculate velocity
echo "scale=2; $(grep -c "- \[x\]" sprint-05.md) / $(grep -c "^- \[" sprint-05.md) * 100" | bc
```

**Expected Output**: Percentage (e.g., 87% completion rate)

**Historical Tracking**:
```bash
# Aggregate across all sprints
for sprint in docs/project-docs/sprints/sprint-*.md; do
  echo "$(basename $sprint): $(grep -c "- \[x\]" $sprint) / $(grep -c "^- \[" $sprint)"
done
```

### Quality Metrics

**Coverage Metric**: Test coverage percentage (target ≥85%)

```bash
# Run coverage and extract percentage
pytest --cov=scripts --cov=src --cov-report=term | grep "TOTAL" | awk '{print $NF}'
```

**Lint Metric**: Lint error count (target 0)

```bash
# Count lint errors
ruff check . 2>&1 | grep -c "error:"
```

**Type Check Metric**: Type error count (target 0)

```bash
# Count type errors
mypy --strict . 2>&1 | grep -c "error:"
```

**Quality Score**: Aggregate metric (0-100)

```
quality_score = (
  (coverage_pct * 0.4) +           # 40% weight
  ((100 - lint_errors) * 0.3) +    # 30% weight
  ((100 - type_errors) * 0.3)      # 30% weight
)
```

### Documentation Coverage

**Metric**: Documentation coverage = Documented artifacts / Total artifacts

**Calculation**:
```bash
# Count SAPs with all 5 artifacts
ls docs/skilled-awareness/*/charter.md | wc -l       # Has charter
ls docs/skilled-awareness/*/protocol-spec.md | wc -l # Has protocol
ls docs/skilled-awareness/*/awareness-guide.md | wc -l # Has awareness
ls docs/skilled-awareness/*/blueprint.md | wc -l     # Has blueprint
ls docs/skilled-awareness/*/ledger.md | wc -l        # Has ledger

# Total SAPs
ls -d docs/skilled-awareness/*/ | wc -l
```

**Link Validation**:
```bash
# Validate all documentation links
bash scripts/validate-links.sh

# Count broken links
bash scripts/validate-links.sh 2>&1 | grep -c "BROKEN"
```

### Traceability Metrics

**Event Count**: Total events in event log

```bash
wc -l < inbox/coordination/events.jsonl
```

**Events by Trace ID**:

```bash
# Count events for specific coordination
grep 'coord-2025-004-bidirectional' inbox/coordination/events.jsonl | wc -l
```

**Events by Type**:

```bash
# Count by event type
jq -r '.event' inbox/coordination/events.jsonl | sort | uniq -c
```

**Recent Events**:

```bash
# Last 10 events with timestamps
tail -10 inbox/coordination/events.jsonl | jq -r '"\(.timestamp) | \(.event) | \(.phase // .coordination_id)"'
```

### Metrics Dashboard

**Command**: Display all key metrics in one view

```bash
#!/bin/bash
# metrics-dashboard.sh

echo "=== METRICS DASHBOARD ==="
echo ""

echo "## Quality"
echo "Coverage: $(pytest --cov --cov-report=term | grep TOTAL | awk '{print $NF}')"
echo "Lint errors: $(ruff check . 2>&1 | grep -c error || echo 0)"
echo "Type errors: $(mypy --strict . 2>&1 | grep -c error || echo 0)"
echo ""

echo "## Progress"
echo "Active work: $(grep -c "status: pending\|status: accepted" inbox/coordination/ECOSYSTEM_STATUS.yaml)"
echo "Recent completions: $(grep -c "recent_completions:" inbox/coordination/ECOSYSTEM_STATUS.yaml)"
echo ""

echo "## Documentation"
echo "Total SAPs: $(ls -d docs/skilled-awareness/*/ | wc -l)"
echo "Broken links: $(bash scripts/validate-links.sh 2>&1 | grep -c BROKEN || echo 0)"
echo ""

echo "## Traceability"
echo "Total events: $(wc -l < inbox/coordination/events.jsonl)"
echo "Recent events (last 7 days): $(jq -r 'select(.timestamp >= now - 604800) | .event' inbox/coordination/events.jsonl | wc -l)"
```

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "calculate ROI" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "calculate ROI" → `run_claude_roi_calculator` with high confidence
5. Agent executes `python scripts/claude-roi-calculator.py` interactively
6. Agent parses results and displays formatted output

**Context-Aware Suggestions**:
- If coverage <85%, suggest running coverage improvement workflow
- If broken links detected, suggest running fix workflow
- If velocity declining, suggest reviewing sprint complexity
- If defect rate increasing, suggest reviewing testing practices
- Prioritizes quality metrics over vanity metrics

**Progressive Formalization**:
- Week 1: "is this worth it?" → Agent explains ROI concept and runs calculator
- Week 2-4: "calculate ROI" → Agent runs calculator directly
- Month 2+: "python scripts/claude-roi-calculator.py" → Agent executes command
- Month 3+: User runs calculator independently

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Common Tasks

### Calculate ROI for Claude Code

**Goal**: Determine return on investment for Claude Code adoption

**Steps**:
1. Run calculator: `python scripts/claude-roi-calculator.py`
2. Answer prompts:
   - Work type: coding
   - Experience: intermediate
   - Complexity: moderate
   - Weekly hours: 40
   - Time savings: 25%
3. Review results (time saved, value, ROI %, break-even)
4. Results saved to `.chora/metrics/roi-calculation-YYYY-MM-DD.json`

**Expected Output**: ROI calculation with time savings, value, ROI percentage, break-even period

### Track Sprint Velocity

**Goal**: Measure sprint completion rate over time

**Steps**:
1. List all sprint plans: `ls docs/project-docs/sprints/sprint-*.md`
2. For each sprint, calculate velocity:
   ```bash
   completed=$(grep -c "- \[x\]" sprint-NN.md)
   total=$(grep -c "^- \[" sprint-NN.md)
   velocity=$(echo "scale=2; $completed / $total * 100" | bc)
   echo "Sprint NN: $velocity%"
   ```
3. Aggregate results: Average velocity across sprints
4. Track trend: Improving, stable, or declining?

**Expected Output**: Velocity percentage per sprint, average velocity, trend

### Validate Documentation Quality

**Goal**: Check documentation completeness and link validity

**Steps**:
1. Check SAP completeness:
   ```bash
   for sap in docs/skilled-awareness/*/; do
     echo "$(basename $sap):"
     ls $sap/*.md | wc -l  # Should be ≥5 (charter, protocol, awareness, blueprint, ledger)
   done
   ```
2. Validate links: `bash scripts/validate-links.sh`
3. Count broken links: `bash scripts/validate-links.sh 2>&1 | grep -c BROKEN`
4. If broken links found, fix them using Edit tool

**Expected Output**: SAP artifact counts, broken link count (target 0)

### Display Quality Metrics Dashboard

**Goal**: Show all quality metrics in one view

**Steps**:
1. Run coverage: `pytest --cov --cov-report=term | grep TOTAL | awk '{print $NF}'`
2. Check lint: `ruff check . 2>&1 | grep -c error || echo 0`
3. Check types: `mypy --strict . 2>&1 | grep -c error || echo 0`
4. Check scenarios: `behave features/ --format progress 2>&1 | grep "scenarios passed"`
5. Format output:
   ```
   === QUALITY DASHBOARD ===
   Coverage: 87%
   Lint errors: 0
   Type errors: 0
   BDD scenarios: 61/61 passing
   ```

**Expected Output**: Quality metrics dashboard with all gates

### Trace Coordination Request

**Goal**: View all events for a specific coordination request

**Steps**:
1. Identify trace ID: Read coordination request JSON (e.g., "coord-2025-004-bidirectional")
2. Filter events: `grep 'coord-2025-004-bidirectional' inbox/coordination/events.jsonl`
3. Parse events: `grep 'coord-2025-004' events.jsonl | jq -r '"\(.timestamp) | \(.event) | \(.phase // .status)"'`
4. Visualize timeline:
   ```
   2025-10-31T10:00:00Z | coordination_request_created | intake
   2025-10-31T11:30:00Z | phase_completed | Governance_Updates
   2025-10-31T12:00:00Z | phase_started | DDD
   2025-10-31T14:00:00Z | change_request_approved | approved
   ...
   ```

**Expected Output**: Chronological event timeline for coordination request

### Generate Metrics Report

**Goal**: Create comprehensive metrics report for stakeholders

**Steps**:
1. Collect ROI data: Read `.chora/metrics/roi-calculation-*.json`
2. Collect velocity data: Aggregate sprint velocities
3. Collect quality data: Coverage, lint, types, scenarios
4. Collect documentation data: SAP completeness, link validity
5. Collect traceability data: Event counts, active work
6. Format report (Markdown or JSON):
   ```markdown
   # Metrics Report - 2025-10-31

   ## ROI
   - Yearly time savings: 240 hours
   - Yearly value: $24,000
   - ROI: 9,900%

   ## Velocity
   - Average sprint velocity: 93%
   - Sprint 5 velocity: 50% (in progress)

   ## Quality
   - Coverage: 87%
   - Lint errors: 0
   - Type errors: 0
   - BDD scenarios: 61/61 passing

   ## Documentation
   - Total SAPs: 18
   - SAP completeness: 100% (18/18 with all artifacts)
   - Broken links: 0

   ## Traceability
   - Total events: 35
   - Active coordination requests: 4
   - Recent completions: 3
   ```

**Expected Output**: Comprehensive metrics report (Markdown or JSON)

---

## Related SAPs

- **SAP-001** (inbox-protocol): Coordination request tracking, event logging
- **SAP-004** (testing-framework): Coverage metrics, test execution tracking
- **SAP-006** (quality-gates): Quality threshold enforcement
- **SAP-009** (agent-awareness): Metrics discovery via bidirectional translation
- **SAP-012** (development-lifecycle): Sprint velocity, phase completion tracking
- **SAP-013** (metrics-framework): THIS SAP - ROI, velocity, quality, documentation metrics
- **SAP-019** (sap-self-evaluation): SAP quality scoring and validation

---

**Version History**:
- **1.1.0** (2025-10-31): Added bidirectional translation layer integration, user signal patterns
- **1.0.0** (2025-10-29): Initial domain AGENTS.md for metrics framework

