# CLAUDE.md - Metrics Framework (SAP-013)

**Domain**: Metrics & Measurement
**SAP**: SAP-013 (metrics-framework)
**Version**: 1.1.0
**Last Updated**: 2025-11-05

---

## Overview

This is the Claude-specific CLAUDE.md file for the metrics framework (SAP-013). It provides Claude Code tool patterns for metrics collection, ROI calculation, velocity tracking, and quality measurement.

**Parent**: See [/CLAUDE.md](/CLAUDE.md) for project-level Claude guidance

**Pattern**: "Nearest File Wins" - This file provides metrics-specific Claude patterns

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "Claude (first-time orientation)"
  estimated_tokens: 5000
  estimated_time_minutes: 3
  sections:
    - "Tool Integration Patterns"
    - "User Signal Detection"

phase_2_implementation:
  target_audience: "Claude implementing metrics workflows"
  estimated_tokens: 15000
  estimated_time_minutes: 10
  sections:
    - "Key Workflows (Claude Code)"
    - "Common Patterns"

phase_3_deep_dive:
  target_audience: "Claude analyzing metrics or generating reports"
  estimated_tokens: 30000
  estimated_time_minutes: 20
  files_to_read:
    - "AGENTS.md (complete metrics reference)"
    - "scripts/claude-roi-calculator.py (ROI implementation)"
```

---

## Tool Integration Patterns

### Bash Tool (for metrics commands)

**ROI Calculation**:
```bash
# Run interactive ROI calculator
Bash: python scripts/claude-roi-calculator.py

# Non-interactive (with defaults)
Bash: python -c "
from scripts.claude_roi_calculator import calculate_roi
result = calculate_roi(
    work_type='coding',
    experience='intermediate',
    complexity='moderate',
    weekly_hours=40,
    time_savings_pct=25,
    hourly_rate=100
)
print(result)
"
```

**Velocity Tracking**:
```bash
# Calculate sprint velocity
Bash: python -c "
import subprocess
completed = int(subprocess.check_output(['grep', '-c', '- \\[x\\]', 'sprint-05.md']).strip())
total = int(subprocess.check_output(['grep', '-c', '^- \\[', 'sprint-05.md']).strip())
velocity = (completed / total) * 100
print(f'Sprint velocity: {velocity:.1f}%')
"
```

**Quality Metrics**:
```bash
# Run coverage report
Bash: pytest --cov=src --cov-report=term

# Run lint checks
Bash: ruff check src/

# Run type checks
Bash: mypy src/
```

**Link Validation**:
```bash
# Validate all links
Bash: bash scripts/validate-links.sh

# Count broken links
Bash: bash scripts/validate-links.sh | grep -c "BROKEN"
```

---

### Read Tool (for metrics data)

**Read ROI Results**:
```bash
# Read saved ROI calculation
Read .chora/metrics/roi-calculation-2025-11-05.json
```

**Read Sprint Plans**:
```bash
# Read sprint progress
Read docs/project-docs/sprints/sprint-05.md
# Count [x] vs [ ] for velocity
```

**Read Coverage Reports**:
```bash
# Read coverage output
Read coverage.xml
# Or HTML report
Read htmlcov/index.html
```

**Read Event Logs**:
```bash
# Read coordination events
Read inbox/coordination/events.jsonl
# Filter by CHORA_TRACE_ID
```

---

### Write Tool (for metrics reports)

**Write ROI Report**:
```bash
# Save ROI calculation results
Write .chora/metrics/roi-report-2025-11-05.md
# Content: Formatted ROI analysis
```

**Write Sprint Dashboard**:
```bash
# Create sprint dashboard
Write docs/project-docs/sprints/sprint-05-dashboard.md
# Content: Velocity, quality, completion metrics
```

**Write Quality Report**:
```bash
# Save quality metrics
Write .chora/metrics/quality-report-2025-11-05.md
# Content: Coverage, lint, type check results
```

---

### Edit Tool (for updating metrics)

**Update Sprint Plan**:
```bash
# Mark tasks complete
Edit docs/project-docs/sprints/sprint-05.md
# Change: - [ ] Task → - [x] Task
```

**Update Metrics Config**:
```bash
# Adjust ROI parameters
Edit scripts/claude-roi-calculator.py
# Update defaults: hourly_rate, time_savings_pct
```

---

## User Signal Detection

### ROI & Value Signals

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Calculate ROI" | Run ROI calculator | Bash (ROI script) |
| "Is Claude worth it?" | Generate ROI report | Bash + Write (report) |
| "Show time saved" | Extract time savings from ROI | Read (ROI results) |
| "Cost benefit analysis" | Full ROI calculation + report | Bash + Write |

**Example**:
```
User: "Calculate ROI for Claude Code"

Claude:
1. Bash: python scripts/claude-roi-calculator.py
   [User completes interactive prompts]
2. Read .chora/metrics/roi-calculation-[date].json
3. Write .chora/metrics/roi-report-[date].md
   [Formatted summary with recommendations]
4. Show user: "ROI calculation complete. Yearly value: $24,000 (9,900% ROI)"
```

---

### Velocity & Progress Signals

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Check velocity" | Calculate sprint completion rate | Bash (grep count) + Read (sprint) |
| "Show progress" | Display completed vs total tasks | Read (sprint plan) |
| "Sprint stats" | Aggregate sprint metrics | Bash (calculations) |
| "How far along?" | Calculate completion percentage | Bash + Read |

**Example**:
```
User: "Check sprint velocity"

Claude:
1. Read docs/project-docs/sprints/sprint-05.md
2. Bash: grep -c "- \\[x\\]" sprint-05.md  # Count completed
3. Bash: grep -c "^- \\[" sprint-05.md     # Count total
4. Calculate: completed / total * 100
5. Show user: "Sprint velocity: 87% (13/15 tasks completed)"
```

---

### Quality Metrics Signals

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Quality metrics" | Run all quality checks | Bash (pytest, ruff, mypy) |
| "Check coverage" | Run coverage report | Bash (pytest --cov) |
| "Defect rate" | Count failing tests | Bash (pytest --json) |
| "Quality score" | Aggregate quality metrics | Bash + Write (report) |

**Example**:
```
User: "Show quality metrics"

Claude:
1. Bash: pytest --cov=src --cov-report=term
2. Bash: ruff check src/
3. Bash: mypy src/
4. Aggregate results:
   - Coverage: 94%
   - Lint: 0 errors
   - Type check: 0 errors
5. Write .chora/metrics/quality-report-[date].md
6. Show user: "Quality: 94% coverage, 0 lint errors, 0 type errors"
```

---

### Documentation Metrics Signals

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Doc coverage" | Calculate documented vs total | Bash (grep count) |
| "Broken links" | Validate all links | Bash (validate-links.sh) |
| "How many broken links?" | Count broken links | Bash (validate + grep) |
| "Fix broken links" | Update links based on validation | Read + Edit |

**Example**:
```
User: "Check for broken links"

Claude:
1. Bash: bash scripts/validate-links.sh
2. Bash: bash scripts/validate-links.sh | grep -c "BROKEN"
3. Show user: "Found 3 broken links"
4. If user asks to fix:
   a. Read validation output
   b. Identify broken links
   c. Edit affected files
   d. Re-validate
```

---

### Traceability Signals

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Show trace" | Display event log | Read (events.jsonl) |
| "Trace coord-XXX" | Filter by CHORA_TRACE_ID | Bash (grep) + Read |
| "Recent events" | Display last N events | Bash (tail) + Read |
| "Event timeline" | Parse events chronologically | Bash + Read |

**Example**:
```
User: "Show trace for coord-005"

Claude:
1. Bash: grep "CHORA_TRACE_ID=coord-005" inbox/coordination/events.jsonl
2. Read matching events
3. Format timeline:
   - 2025-11-01 10:00: Coordination created
   - 2025-11-01 11:30: Task decomposed
   - 2025-11-02 14:00: Coordination completed
4. Show user: "Traced coord-005: 3 events over 1 day"
```

---

## Key Workflows (Claude Code)

### Workflow 1: Calculate and Report ROI

**Goal**: Calculate Claude Code ROI and generate report

**Tools**: Bash (ROI calculator), Read (results), Write (report)

**Steps**:

1. **Run ROI calculator**:
   ```bash
   Bash: python scripts/claude-roi-calculator.py
   ```

2. **User completes interactive prompts**:
   - Work type: coding
   - Experience: intermediate
   - Complexity: moderate
   - Weekly hours: 40
   - Time savings: 25%
   - Hourly rate: $100

3. **Read saved results**:
   ```bash
   Read .chora/metrics/roi-calculation-2025-11-05.json
   ```

4. **Generate formatted report**:
   ```bash
   Write .chora/metrics/roi-report-2025-11-05.md
   ```

   Content:
   ```markdown
   # ROI Report - 2025-11-05

   ## Summary
   - **Weekly hours saved**: 10 hours
   - **Yearly hours saved**: 480 hours
   - **Yearly value**: $48,000
   - **ROI**: 19,900%

   ## Breakdown
   - Weekly hours with Claude: 40 hours
   - Time savings: 25%
   - Hourly rate: $100/hour
   - Claude Code cost: $20/month ($240/year)
   - Net yearly value: $47,760

   ## Recommendation
   ✅ **Extremely high ROI** - Continue using Claude Code
   💡 Consider expanding to more team members
   ```

5. **Show user**:
   ```
   ROI calculation complete!
   - Yearly value: $48,000
   - ROI: 19,900%
   - Report saved to: .chora/metrics/roi-report-2025-11-05.md
   ```

**Expected Outcome**: ROI report demonstrating Claude Code value

**Time Estimate**: 5-10 minutes

---

### Workflow 2: Track Sprint Velocity

**Goal**: Calculate sprint completion rate and identify remaining tasks

**Tools**: Read (sprint plan), Bash (grep counts)

**Steps**:

1. **Read sprint plan**:
   ```bash
   Read docs/project-docs/sprints/sprint-05.md
   ```

2. **Count completed tasks**:
   ```bash
   Bash: grep -c "- \\[x\\]" docs/project-docs/sprints/sprint-05.md
   # Output: 13
   ```

3. **Count total tasks**:
   ```bash
   Bash: grep -c "^- \\[" docs/project-docs/sprints/sprint-05.md
   # Output: 15
   ```

4. **Calculate velocity**:
   ```python
   velocity = (13 / 15) * 100  # 86.7%
   ```

5. **Identify remaining tasks**:
   ```bash
   Bash: grep "- \\[ \\]" docs/project-docs/sprints/sprint-05.md
   # Output:
   # - [ ] Task 14: Implement feature X
   # - [ ] Task 15: Write documentation for Y
   ```

6. **Generate sprint dashboard**:
   ```bash
   Write docs/project-docs/sprints/sprint-05-dashboard.md
   ```

   Content:
   ```markdown
   # Sprint 05 Dashboard

   ## Velocity
   - **Completion rate**: 86.7% (13/15 tasks)
   - **Target**: 80% ✅ (on track)

   ## Remaining Tasks
   - Task 14: Implement feature X
   - Task 15: Write documentation for Y

   ## Recommendations
   - ✅ Sprint on track for completion
   - 💡 Focus on remaining 2 tasks this week
   ```

7. **Show user**:
   ```
   Sprint velocity: 86.7% (13/15 tasks completed)
   Remaining: 2 tasks
   Dashboard saved to: sprint-05-dashboard.md
   ```

**Expected Outcome**: Sprint velocity calculated, remaining work identified

**Time Estimate**: 5-10 minutes

---

### Workflow 3: Generate Quality Report

**Goal**: Run all quality checks and generate comprehensive report

**Tools**: Bash (pytest, ruff, mypy), Write (report)

**Steps**:

1. **Run coverage**:
   ```bash
   Bash: pytest --cov=src --cov-report=term
   # Output: 94% coverage
   ```

2. **Run lint checks**:
   ```bash
   Bash: ruff check src/
   # Output: All checks passed!
   ```

3. **Run type checks**:
   ```bash
   Bash: mypy src/
   # Output: Success: no issues found
   ```

4. **Aggregate results**:
   ```python
   quality_metrics = {
       "coverage": 94,
       "lint_errors": 0,
       "type_errors": 0,
       "quality_score": 98  # Calculated from metrics
   }
   ```

5. **Generate quality report**:
   ```bash
   Write .chora/metrics/quality-report-2025-11-05.md
   ```

   Content:
   ```markdown
   # Quality Report - 2025-11-05

   ## Metrics
   - **Test Coverage**: 94% (target: ≥90%, ✅ green)
   - **Lint Errors**: 0 (target: 0, ✅ green)
   - **Type Errors**: 0 (target: 0, ✅ green)
   - **Quality Score**: 98/100 (✅ excellent)

   ## Trends
   - Coverage: ⬆️ +2% since last week
   - Lint errors: ⬇️ -3 since last week
   - Type errors: → No change (maintained)

   ## Recommendations
   - ✅ All quality gates passed
   - 💡 Consider increasing coverage target to 95%
   - 💡 Continue current quality practices
   ```

6. **Show user**:
   ```
   Quality report complete!
   - Coverage: 94% ✅
   - Lint: 0 errors ✅
   - Type check: 0 errors ✅
   - Quality score: 98/100
   Report saved to: .chora/metrics/quality-report-2025-11-05.md
   ```

**Expected Outcome**: Comprehensive quality report with recommendations

**Time Estimate**: 10-15 minutes

---

## Common Patterns

### Pattern 1: Calculate-Report-Show

**Always follow this sequence for metrics**:

```markdown
Step 1: Calculate metric
Bash: [run calculation]

Step 2: Generate report
Write [report file]

Step 3: Show user summary
[Display key metrics]
```

**Why**: Provides both persistent record (report) and immediate feedback (summary)

---

### Pattern 2: Read-Count-Calculate

**For velocity and progress metrics**:

```markdown
Step 1: Read source data
Read [sprint plan or task list]

Step 2: Count items
Bash: grep -c [pattern] [file]

Step 3: Calculate percentage
[completed / total * 100]
```

**Why**: Accurate metrics from source of truth

---

### Pattern 3: Run-Aggregate-Report

**For quality metrics**:

```markdown
Step 1: Run all quality checks
Bash: pytest --cov
Bash: ruff check
Bash: mypy

Step 2: Aggregate results
[Collect coverage, errors, scores]

Step 3: Generate report
Write [quality report]
```

**Why**: Comprehensive quality view in single report

---

## Claude-Specific Tips

### Tip 1: Use Interactive ROI Calculator for First Time

**Pattern**:
```bash
Bash: python scripts/claude-roi-calculator.py
[User completes prompts interactively]
```

**Why**: Ensures user understands each parameter

**Later**: Use non-interactive with saved defaults

---

### Tip 2: Save All Metrics to .chora/metrics/

**Pattern**:
```bash
Write .chora/metrics/roi-report-[date].md
Write .chora/metrics/quality-report-[date].md
Write .chora/metrics/velocity-report-[date].md
```

**Why**: Centralized metrics storage, version controlled

---

### Tip 3: Use Grep with Precise Patterns

**Pattern**:
```bash
# Count completed tasks (CORRECT)
Bash: grep -c "- \\[x\\]" sprint-05.md

# Count completed tasks (WRONG - matches any checkbox)
Bash: grep -c "\\[x\\]" sprint-05.md
```

**Why**: Precise patterns avoid false positives

---

### Tip 4: Generate Dashboards Automatically

**Pattern**:
```markdown
After calculating metrics:
Write docs/project-docs/sprints/sprint-[N]-dashboard.md
# Auto-generate from metrics
```

**Why**: Regular visibility drives improvement

---

### Tip 5: Show Trends, Not Just Snapshots

**Pattern**:
```markdown
# In reports, always include trends
- Coverage: 94% (⬆️ +2% since last week)
- Defects: 2 (⬇️ -3 since last week)
```

**Why**: Trends show improvement or regression

---

## Common Pitfalls

### Pitfall 1: Wrong Grep Pattern

**Problem**: `grep -c "\\[x\\]"` matches any checkbox, not just task checkboxes

**Fix**: Use `grep -c "- \\[x\\]"` for tasks only

---

### Pitfall 2: Not Saving ROI Results

**Problem**: Running ROI calculator but not saving results

**Fix**: Always save to `.chora/metrics/roi-calculation-[date].json`

---

### Pitfall 3: Calculating Velocity from Wrong Source

**Problem**: Using git commits instead of sprint plan tasks

**Fix**: Calculate velocity from sprint plan markdown files (source of truth)

---

### Pitfall 4: Not Generating Reports

**Problem**: Calculating metrics but not creating persistent reports

**Fix**: Always write metrics to `.chora/metrics/` for historical tracking

---

### Pitfall 5: Ignoring Trends

**Problem**: Only showing current metrics, no historical context

**Fix**: Include trend arrows (⬆️ ⬇️ →) and percentage changes

---

## Quick Reference

### Common Bash Commands

```bash
# ROI calculation
python scripts/claude-roi-calculator.py

# Sprint velocity
grep -c "- \\[x\\]" sprint-N.md  # Completed
grep -c "^- \\[" sprint-N.md     # Total

# Quality metrics
pytest --cov=src --cov-report=term
ruff check src/
mypy src/

# Link validation
bash scripts/validate-links.sh
bash scripts/validate-links.sh | grep -c "BROKEN"

# Event tracing
grep "CHORA_TRACE_ID=coord-XXX" events.jsonl
```

---

### Metrics File Locations

```
.chora/metrics/
├── roi-calculation-YYYY-MM-DD.json
├── roi-report-YYYY-MM-DD.md
├── quality-report-YYYY-MM-DD.md
└── velocity-report-YYYY-MM-DD.md

docs/project-docs/sprints/
├── sprint-N.md
└── sprint-N-dashboard.md

inbox/coordination/
└── events.jsonl
```

---

## Version History

**1.1.0** (2025-11-05):
- Initial CLAUDE.md for metrics-framework (SAP-013)
- 3 workflows: ROI calculation, sprint velocity, quality report
- Claude-specific tool patterns (Bash, Read, Write, Edit)
- 5 Claude-specific tips, 5 common pitfalls
- Tool usage patterns for metrics operations

**1.0.0** (2025-10-31):
- Initial metrics framework with AGENTS.md

---

## Quick Links

- **AGENTS.md**: [AGENTS.md](AGENTS.md) - Generic agent patterns
- **ROI Calculator**: [../../scripts/claude-roi-calculator.py](../../scripts/claude-roi-calculator.py)
- **Validate Links**: [../../scripts/validate-links.sh](../../scripts/validate-links.sh)
- **SAP Catalog**: [../AGENTS.md](../AGENTS.md) - SAP navigation

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive metrics reference
2. Run ROI calculator to demonstrate value
3. Set up automated metrics collection in CI/CD
4. Generate regular sprint and quality reports
