# SAP Self-Evaluation - Protocol Specification

**Pattern ID**: SAP-019
**Pattern Name**: sap-self-evaluation
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-30

## 1. Overview

This specification defines the evaluation protocol for assessing SAP (Skilled Awareness Pattern) adoption depth, identifying gaps, and generating actionable improvement roadmaps.

### Protocol Goals

1. **Progressive Assessment**: Quick check (30s) → Deep dive (5min) → Strategic analysis (30min)
2. **LLM-Executable**: Structured prompts enable AI agents to self-assess
3. **Actionable Output**: Concrete next steps, not just scores
4. **Tracking Over Time**: Version-controlled reports, event timeline
5. **Integration-Ready**: Feeds into SAP-013 metrics, sprint planning, roadmaps

### Key Concepts

**Evaluation Depth**:
- **Quick Check**: Automated validation (file existence, command execution, exit codes)
- **Deep Dive**: LLM-driven content analysis (quality, completeness, integration depth)
- **Strategic Analysis**: Timeline trends, gap prioritization, roadmap generation

**Adoption Levels** (per SAP):
- **Level 0**: Not installed
- **Level 1**: Installed, basic capability functional
- **Level 2**: Integrated into workflows, standard usage patterns
- **Level 3**: Fully automated, optimized, comprehensive usage

**Gap Types**:
- **Installation Gap**: Required artifacts missing
- **Integration Gap**: Installed but not used in practice
- **Quality Gap**: Used but incorrectly/incompletely
- **Optimization Gap**: Used correctly but not optimized

## 2. Data Models

### 2.1 EvaluationResult

```python
@dataclass
class EvaluationResult:
    """Result of a single SAP evaluation"""

    # Identity
    sap_id: str                    # e.g., "SAP-004"
    sap_name: str                  # e.g., "testing-framework"
    evaluation_type: str           # "quick" | "deep" | "strategic"
    timestamp: datetime

    # Current state
    is_installed: bool             # Artifacts present
    current_level: int             # 0, 1, 2, or 3
    completion_percent: float      # 0-100, progress toward next level

    # Validation results
    validation_results: dict[str, bool]  # Automated checks
    quality_scores: dict[str, float]     # LLM-assessed quality (0-1)

    # Gap analysis
    gaps: list[Gap]                # Identified improvement opportunities
    blockers: list[str]            # What prevents next level

    # Recommendations
    next_milestone: str            # e.g., "Level 2 adoption"
    recommended_actions: list[Action]  # Prioritized next steps
    estimated_effort_hours: float  # Total time to next level

    # Metadata
    duration_seconds: float        # Time to run evaluation
    confidence: str                # "high" | "medium" | "low"
    warnings: list[str]            # Non-blocking issues
```

### 2.2 Gap

```python
@dataclass
class Gap:
    """Identified improvement opportunity"""

    gap_id: str                    # Unique identifier
    gap_type: str                  # "installation" | "integration" | "quality" | "optimization"
    title: str                     # Short description
    description: str               # Detailed explanation

    # Impact assessment
    impact: str                    # "high" | "medium" | "low"
    effort: str                    # "high" | "medium" | "low"
    priority: str                  # "P0" | "P1" | "P2"
    urgency: str                   # "blocks_sprint" | "next_sprint" | "future"

    # Context
    current_state: str             # What exists now
    desired_state: str             # What should exist
    blocks: list[str]              # SAP IDs blocked by this gap
    blocked_by: list[str]          # Dependencies

    # Resolution
    actions: list[Action]          # How to fix
    estimated_hours: float         # Time estimate
    validation: str                # How to verify fixed
```

### 2.3 Action

```python
@dataclass
class Action:
    """Concrete step to improve adoption"""

    action_id: str                 # Unique identifier
    description: str               # What to do

    # Agent-executable details
    tool: str                      # "Read" | "Edit" | "Bash" | etc.
    file_path: Optional[str]       # Target file
    location: Optional[str]        # Line number, section, etc.
    content: Optional[str]         # Exact content to add/change
    command: Optional[str]         # Bash command to run

    # Context
    rationale: str                 # Why this helps
    expected_outcome: str          # What changes
    validation_command: Optional[str]  # How to verify

    # Planning
    estimated_minutes: int         # Time estimate
    sequence: int                  # Order to execute (1, 2, 3...)
    depends_on: list[str]          # Action IDs that must complete first
```

### 2.4 AdoptionRoadmap

```python
@dataclass
class AdoptionRoadmap:
    """Strategic adoption plan over time"""

    # Metadata
    generated_at: datetime
    target_quarter: str            # e.g., "Q1-2026"
    next_review_date: date

    # Current state
    total_saps_installed: int
    adoption_distribution: dict[str, int]  # {"level_1": 10, "level_2": 2, ...}
    average_adoption_level: float
    total_hours_invested: float

    # Goals
    quarterly_goals: dict[str, Any]  # Targets for next quarter
    target_saps_to_install: list[str]
    target_level_2_count: int
    target_roi: float              # e.g., 3.0 (3x return)

    # Prioritized gaps
    priority_gaps: list[PrioritizedGap]

    # Sprint breakdown
    this_sprint: SprintPlan
    next_sprint: SprintPlan
    future_sprints: list[SprintPlan]
```

### 2.5 PrioritizedGap

```python
@dataclass
class PrioritizedGap:
    """Gap with priority ranking and plan"""

    rank: int                      # 1 = highest priority
    sap_id: str
    gap: Gap

    # Justification
    reason: str                    # Why prioritized this way
    impact_score: float            # Calculated impact (0-1)
    effort_score: float            # Calculated effort (0-1)
    priority_score: float          # Impact / Effort

    # Planning
    sprint: str                    # "current" | "next" | "future"
    deliverables: list[str]        # Concrete outputs
    blocks: list[str]              # SAP IDs unblocked by fixing this
```

### 2.6 SprintPlan

```python
@dataclass
class SprintPlan:
    """SAP adoption tasks for a sprint"""

    sprint_name: str               # e.g., "Sprint 23"
    start_date: date
    end_date: date

    # Focus areas
    focus_saps: list[str]          # SAP IDs to work on
    target_levels: dict[str, int]  # {"SAP-004": 2, "SAP-013": 1}

    # Tasks
    tasks: list[Action]            # Actions to complete
    total_estimated_hours: float

    # Success criteria
    validation_commands: list[str]
    expected_outcomes: list[str]
```

## 3. Evaluation Protocols

### 3.1 Quick Check Protocol

**Purpose**: Rapid assessment of installation status and basic validation (30 seconds).

**Inputs**:
- `sap_id: str` - SAP to evaluate
- `repo_root: Path` - Repository root directory

**Process**:
1. **Check installation**: Does `docs/skilled-awareness/<sap-name>/` exist?
2. **Validate artifacts**: Are all 5 required files present?
   - capability-charter.md
   - protocol-spec.md
   - awareness-guide.md
   - adoption-blueprint.md
   - ledger.md
3. **Run validation commands**: Execute quick checks from protocol-spec.md
4. **Assess level**: Based on validation results, determine Level 0/1/2/3

**Outputs**:
- `EvaluationResult` with automated validation results
- Terminal output (color-coded status)
- JSON export (optional)

**Example**:
```bash
$ python scripts/sap-evaluator.py --quick SAP-004

SAP-004 (Testing Framework) - Quick Check
==========================================
✅ Installed (5/5 artifacts present)
✅ Tests pass (pytest: 12/12 passed)
❌ Coverage below target (65% < 85%)
✅ CI integration present

Current Level: 1
Next Milestone: Level 2 (85% coverage)
Estimated Effort: 3 hours

Run deep dive for detailed gap analysis:
  python scripts/sap-evaluator.py --deep SAP-004
```

**Validation Commands** (from protocol-spec.md):

Each SAP defines quick validation commands. Example for SAP-004:

```bash
# Check 1: Tests pass
pytest
exit_code=$?
if [ $exit_code -eq 0 ]; then echo "PASS"; else echo "FAIL"; fi

# Check 2: Coverage ≥85%
pytest --cov=src --cov-report=term | grep "TOTAL" | awk '{if ($NF+0 >= 85) print "PASS"; else print "FAIL"}'

# Check 3: CI configured
test -f .github/workflows/test.yml && echo "PASS" || echo "FAIL"
```

### 3.2 Deep Dive Protocol

**Purpose**: LLM-driven content analysis, gap identification, action planning (5 minutes).

**Inputs**:
- `sap_id: str` - SAP to evaluate
- `repo_root: Path` - Repository root
- `llm_model: str` - Model to use for analysis (default: claude-3-5-sonnet)

**Process**:
1. **Read protocol criteria**: Parse adoption-blueprint.md for Level 1/2/3 criteria
2. **Automated validation**: Run quick check first
3. **LLM content analysis**:
   - Read AGENTS.md (if SAP-009): Assess completeness, integration depth
   - Read test files (if SAP-004): Count tests, check patterns
   - Read CI workflows (if SAP-005): Validate configuration
   - Scan relevant files: Look for SAP artifact usage
4. **Compare to criteria**: For each Level 2/3 criterion, assess completion
5. **Identify gaps**: Where current state differs from desired state
6. **Prioritize gaps**: Impact × Effort scoring
7. **Generate actions**: Concrete steps to close highest-priority gaps
8. **Estimate effort**: Time required based on action complexity

**Outputs**:
- `EvaluationResult` with detailed gap analysis
- Markdown report (detailed assessment)
- JSON export (machine-readable)

**LLM Prompt Template**:

```markdown
You are assessing SAP-004 (Testing Framework) adoption depth for an AI agent.

**Context**:
- SAP installed: Yes
- Quick check results:
  - Tests pass: ✅
  - Coverage: 65% (target: 85%)
  - CI configured: ✅

**Adoption Criteria** (from adoption-blueprint.md):

Level 1: Basic Testing
- [ ] pytest installed and configured
- [ ] 10+ tests written
- [ ] Tests pass in CI

Level 2: Standard Testing
- [ ] Coverage ≥85%
- [ ] Async test patterns in use
- [ ] 6 test pattern templates applied
- [ ] Fixtures in conftest.py

Level 3: Comprehensive Testing
- [ ] Coverage ≥95%
- [ ] Property-based testing (Hypothesis)
- [ ] Performance benchmarks
- [ ] Test documentation complete

**Files Read**:
- tests/conftest.py (72 lines, 3 fixtures)
- tests/test_api.py (145 lines, 12 tests)
- .github/workflows/test.yml (54 lines)

**Your Task**:
1. Assess current level: Which criteria are met?
2. Identify gaps: What's missing for Level 2?
3. Prioritize gaps: Which gaps have highest impact?
4. Suggest actions: Concrete steps to close gaps

**Output Format** (JSON):
{
  "current_level": 1,
  "level_1_completion": 100,
  "level_2_completion": 45,
  "gaps": [
    {
      "title": "Coverage below 85%",
      "impact": "high",
      "effort": "medium",
      "actions": [...]
    }
  ]
}
```

**Example Output**:

```markdown
# SAP-004 (Testing Framework) - Deep Dive Assessment
**Generated**: 2025-10-30 15:30:00
**Evaluation Time**: 4.2 minutes

## Current State
- **Adoption Level**: Level 1 (Basic)
- **Level 1 Completion**: 100% ✅
- **Level 2 Completion**: 45% (5/11 criteria)
- **Next Milestone**: Level 2 adoption

## Validation Results
✅ **Artifacts Complete**: 5/5 files present
✅ **Tests Pass**: 12/12 tests passing
✅ **CI Configured**: GitHub Actions workflow active
❌ **Coverage Target**: 65% (target: 85%, gap: 20%)
✅ **Fixtures Present**: 3 fixtures in conftest.py
❌ **Async Patterns**: No async tests found
❌ **Pattern Templates**: 2/6 templates in use (33%)

## Gap Analysis (Prioritized)

### Gap 1: Coverage Below Target (P0)
**Impact**: High - Blocks CI/CD coverage gates (SAP-005)
**Effort**: Medium - 8 new tests needed (~3 hours)
**Priority Score**: 0.85

**Current**: 65% coverage (18 tests)
**Desired**: 85% coverage (26 tests, +8)
**Blocks**: SAP-005 (can't enable coverage checks)

**Actions**:
1. Identify uncovered modules (5 min)
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```
2. Write 8 tests for uncovered code (2.5 hours)
   - Use template: `tests/test_example.py`
   - Target: API handlers (40% uncovered)
3. Validate coverage ≥85% (2 min)
   ```bash
   pytest --cov=src --cov-report=term | grep TOTAL
   ```

**Estimated Effort**: 3 hours

### Gap 2: Missing Async Test Patterns (P1)
**Impact**: Medium - Async code untested
**Effort**: Low - Template available
**Priority Score**: 0.65

**Current**: 0 async tests, 4 async functions in src/
**Desired**: 4+ async tests using pytest-asyncio
**Blocks**: None

**Actions**:
1. Install pytest-asyncio (5 min)
   ```bash
   pip install pytest-asyncio
   echo "pytest-asyncio" >> requirements-dev.txt
   ```
2. Create async fixture in conftest.py (15 min)
   - Use template from SAP-004 awareness-guide.md
3. Write 4 async handler tests (1 hour)
4. Validate (2 min)
   ```bash
   pytest -k async -v
   ```

**Estimated Effort**: 1.5 hours

### Gap 3: Limited Pattern Template Usage (P2)
**Impact**: Low - Works, but not optimal
**Effort**: Medium - 4 patterns to add
**Priority Score**: 0.25

**Current**: 2/6 pattern templates in use
**Desired**: 6/6 patterns applied
**Blocks**: None

**Missing Patterns**:
- Exception testing
- Parametrized tests
- Mocking patterns
- Snapshot testing

**Actions**: [deferred to future sprint]

## Recommended Action Plan

### This Sprint (Next 2 Weeks)
**Focus**: Unblock SAP-005 by achieving 85% coverage

**Tasks**:
1. Generate coverage report, identify gaps (5 min)
2. Write 8 new tests for uncovered modules (3 hours)
3. Validate 85% coverage achieved (2 min)
4. Enable coverage gates in CI (SAP-005, 30 min)

**Total Effort**: 3.5 hours
**Success Criteria**:
- `pytest --cov=src` shows ≥85%
- CI coverage check passes

### Next Sprint
**Focus**: Add async test patterns (Level 2 complete)

**Tasks**:
1. Install pytest-asyncio (5 min)
2. Create async fixtures (15 min)
3. Write 4 async tests (1.5 hours)

**Total Effort**: 1.5 hours

### Level 2 Achievement
**After completing both sprints**:
- Adoption Level: 2
- Completion: 75% toward Level 3
- Value Delivered: CI/CD unblocked, async code tested
```

### 3.3 Strategic Analysis Protocol

**Purpose**: Comprehensive roadmap generation with timeline analysis, quarterly planning (30 minutes).

**Inputs**:
- `repo_root: Path` - Repository root
- `quarterly_goals: dict` - Target adoption levels, ROI goals
- `include_history: bool` - Analyze git history for trends (default: True)

**Process**:
1. **Evaluate all installed SAPs**: Run quick check for each
2. **Calculate aggregate metrics**:
   - Total SAPs installed / 18 total available
   - Distribution (Level 0/1/2/3 counts)
   - Average adoption level
3. **Analyze timeline** (if git history available):
   - SAP installation dates (from git log)
   - Ledger progression (Level 1 → 2 → 3 dates)
   - Adoption velocity (SAPs per month, levels per month)
4. **Identify cross-SAP dependencies**:
   - Which gaps block multiple SAPs
   - Dependency chains (SAP-A → SAP-B → SAP-C)
5. **Prioritize gaps globally**:
   - Impact score (how many SAPs unblocked)
   - Effort score (total hours)
   - ROI potential (value delivered / time invested)
6. **Generate sprint breakdown**:
   - This sprint (high-priority, unblocking gaps)
   - Next sprint (medium-priority)
   - Future (low-priority, optimization)
7. **Project ROI** (integrate with SAP-013):
   - Hours invested in SAP adoption
   - Hours saved from SAP capabilities
   - Current ROI, projected ROI after roadmap completion
8. **Output roadmap**: YAML format for version control

**Outputs**:
- `AdoptionRoadmap` object
- YAML file ([sap-roadmap.yaml](sap-roadmap.yaml))
- Markdown executive summary
- HTML dashboard (optional)

**Example Output (YAML)**:

```yaml
# SAP Adoption Roadmap
# Generated: 2025-10-30T16:45:00Z
# Next Review: 2025-12-15

metadata:
  generated_at: 2025-10-30T16:45:00Z
  target_quarter: Q1-2026
  next_review_date: 2025-12-15
  evaluation_duration_minutes: 28

current_state:
  total_saps_available: 18
  total_saps_installed: 12
  adoption_percentage: 67%

  distribution:
    level_0: 6   # Not installed
    level_1: 10  # Basic
    level_2: 2   # Standard
    level_3: 0   # Advanced

  average_adoption_level: 1.17
  total_hours_invested: 24
  estimated_value_delivered: 35  # hours saved
  current_roi: 1.46  # 35 / 24

velocity_analysis:
  saps_installed_per_month: 3.0
  time_to_level_1_avg_days: 2
  time_to_level_2_avg_days: 14
  adoption_trend: "accelerating"  # or "steady" or "slowing"

quarterly_goals:
  target_level_2_saps: 10  # 10/12 at Level 2+
  target_new_installations: 3  # Add SAP-016, SAP-017, SAP-018
  target_roi: 3.0  # 3x return
  target_hours_saved: 75

priority_gaps:
  - rank: 1
    sap_id: SAP-004
    gap_id: coverage-below-target
    gap_title: "Test coverage 65% < 85%"
    impact: high
    effort: medium
    priority_score: 0.85
    reason: "Blocks SAP-005 (CI/CD coverage gates)"
    sprint: current
    estimated_hours: 3
    blocks: [SAP-005]
    deliverables:
      - "85% test coverage achieved"
      - "8 new tests for API handlers"
      - "Coverage report in CI"

  - rank: 2
    sap_id: SAP-013
    gap_id: not-installed
    gap_title: "Metrics tracking not installed"
    impact: high
    effort: low
    priority_score: 0.90
    reason: "No ROI evidence for stakeholders"
    sprint: current
    estimated_hours: 1
    blocks: []
    deliverables:
      - "SAP-013 installed"
      - "ROI tracking for 5 sessions"
      - "First metrics report generated"

  - rank: 3
    sap_id: SAP-009
    gap_id: no-domain-agents-files
    gap_title: "No domain-specific AGENTS.md files"
    impact: medium
    effort: medium
    priority_score: 0.50
    reason: "Agent efficiency 20% below optimal"
    sprint: next
    estimated_hours: 2
    blocks: []
    deliverables:
      - "tests/AGENTS.md created"
      - "docker/AGENTS.md created"
      - "Agent task completion 20% faster"

sprints:
  current_sprint:
    name: "Sprint 23"
    start_date: 2025-11-01
    end_date: 2025-11-14
    focus: "Unblock CI/CD and establish metrics baseline"

    focus_saps:
      - SAP-004  # Testing → Level 2
      - SAP-013  # Metrics → Level 1

    target_levels:
      SAP-004: 2
      SAP-013: 1

    tasks:
      - description: "Achieve 85% test coverage (SAP-004)"
        estimated_hours: 3
        validation: "pytest --cov=src shows ≥85%"
      - description: "Install SAP-013 metrics tracking"
        estimated_hours: 1
        validation: "ClaudeROICalculator generates report"

    total_estimated_hours: 4
    expected_outcomes:
      - "SAP-005 unblocked (coverage gates enabled)"
      - "ROI evidence available for stakeholders"
      - "2 SAPs at Level 2+"

  next_sprint:
    name: "Sprint 24"
    start_date: 2025-11-15
    end_date: 2025-11-28
    focus: "Improve agent efficiency and expand testing"

    focus_saps:
      - SAP-009  # Awareness → Level 2
      - SAP-004  # Testing → Level 2 complete

    tasks:
      - description: "Create domain AGENTS.md files"
        estimated_hours: 2
      - description: "Add async test patterns"
        estimated_hours: 1.5

    total_estimated_hours: 3.5

  future_sprints:
    - name: "Q1-2026"
      focus: "Install link validation, chora-compose integration"
      saps: [SAP-016, SAP-017, SAP-018]
      estimated_hours: 12

projected_outcomes:
  end_of_quarter:
    level_2_saps: 10
    total_hours_invested: 43.5  # 24 + 4 + 3.5 + 12
    estimated_hours_saved: 130
    projected_roi: 3.0  # 130 / 43.5
    adoption_maturity: 83%  # 10/12 at Level 2+
```

### 3.4 Tracking Protocol

**Purpose**: Log adoption events for timeline analysis and progress tracking.

**Event Types**:
```python
# SAP lifecycle events
"sap_installed"           # SAP added to repo
"sap_level_completed"     # Reached Level 1/2/3
"sap_validation_passed"   # Validation check succeeded
"sap_validation_failed"   # Validation check failed
"sap_upgraded"            # SAP version updated

# Evaluation events
"evaluation_started"      # Begin evaluation
"evaluation_completed"    # Evaluation finished
"roadmap_generated"       # Strategic plan created
"roadmap_updated"         # Plan revised
"sprint_completed"        # Sprint goals achieved
```

**Event Schema** (JSONL format):
```json
{
  "event_type": "sap_level_completed",
  "sap_id": "SAP-004",
  "level": 2,
  "timestamp": "2025-10-30T17:00:00Z",
  "duration_hours": 3.5,
  "validation_results": {
    "coverage": "87%",
    "tests_passing": true,
    "ci_configured": true
  },
  "trace_id": "eval-20251030-170000"
}
```

**Storage**: Append to `adoption-history.jsonl` (git-tracked).

**Usage**:
- Trend analysis (adoption velocity over time)
- Time-to-level metrics (how long from install to Level 2?)
- Validation tracking (which checks fail most often?)
- Sprint retrospectives (actual vs. estimated effort)

## 4. Integration Points

### 4.1 SAP-013 Integration (Metrics Tracking)

**SAPAdoptionMetric** (extends SAP-013):

```python
@dataclass
class SAPAdoptionMetric:
    """Track SAP adoption as a metric"""

    sap_id: str
    adoption_level: int
    validation_results: dict[str, bool]
    integration_depth_score: float  # 0-1, LLM-assessed
    timestamp: datetime
    gaps_identified: list[str]
    hours_invested: float
    estimated_hours_saved: float

# Add to ClaudeROICalculator
def track_sap_adoption(self, metric: SAPAdoptionMetric):
    """Record SAP adoption progress"""
    self.sap_metrics.append(metric)

def generate_sap_adoption_report(self) -> str:
    """Include SAP adoption in ROI analysis"""
    # Show: Hours invested in SAP adoption vs. hours saved by capabilities
```

**Dashboard Integration**:
- SAP adoption trends alongside coding metrics
- ROI breakdown (SAP investment as line item)
- Capability maturity score

### 4.2 Per-SAP Protocol Extensions

**Add to each SAP's protocol-spec.md**:

```markdown
## 9. Self-Evaluation Criteria

### Quick Validation Commands

```bash
# Check 1: Installation complete
test -f docs/skilled-awareness/<sap-name>/protocol-spec.md && echo "PASS" || echo "FAIL"

# Check 2: [SAP-specific validation]
<command>

# Check 3: [SAP-specific validation]
<command>
```

### Level Assessment Criteria

**Level 1: Basic Adoption**
- [ ] Criterion 1 (boolean, agent-verifiable)
- [ ] Criterion 2
- [ ] Criterion 3

**Level 2: Standard Adoption**
- [ ] Criterion 4
- [ ] Criterion 5
- [ ] Criterion 6

**Level 3: Advanced Adoption**
- [ ] Criterion 7
- [ ] Criterion 8
- [ ] Criterion 9

### Integration Depth Indicators

**High Integration**:
- [Concrete example of excellent usage]

**Medium Integration**:
- [Concrete example of adequate usage]

**Low Integration**:
- [Concrete example of minimal usage]
```

### 4.3 Ledger Updates

**When evaluation completes**, update `ledger.md`:

```markdown
## 7. Changelog

### 2025-10-30 - Level 2 Adoption Achieved
**Evaluation**: Deep dive completed, 3 gaps identified
**Actions Taken**:
- Added 8 tests for API handlers (3 hours)
- Achieved 87% coverage (target: 85%)
- Enabled CI coverage gates

**Metrics**:
- Adoption Level: 1 → 2
- Coverage: 65% → 87%
- Tests: 18 → 26

**Next Steps**:
- Add async test patterns (Level 2 complete, 1.5 hours)
- Consider property-based testing (Level 3, future)
```

## 5. CLI Interface

### 5.1 Command Structure

```bash
# Quick check (30 seconds)
python scripts/sap-evaluator.py --quick [SAP-ID]
python scripts/sap-evaluator.py --quick         # All installed SAPs

# Deep dive (5 minutes)
python scripts/sap-evaluator.py --deep SAP-004
python scripts/sap-evaluator.py --deep SAP-004 --output report.md

# Strategic analysis (30 minutes)
python scripts/sap-evaluator.py --strategic
python scripts/sap-evaluator.py --strategic --output roadmap.yaml

# Track over time
python scripts/sap-evaluator.py --track --output adoption-history.jsonl

# Generate dashboard
python scripts/sap-evaluator.py --dashboard --output adoption-dashboard.html
```

### 5.2 Output Formats

**Terminal** (default):
- Color-coded status (green/yellow/red)
- Emoji indicators (✅❌🟡)
- Concise summaries

**JSON** (`--format json`):
- Machine-readable
- Full evaluation results
- For automation/dashboards

**Markdown** (`--format md`):
- Human-readable reports
- Git-committable
- Detailed gap analysis

**YAML** (`--format yaml`):
- Roadmap generation
- Sprint planning integration
- Version-controlled

**HTML** (`--format html`):
- Interactive dashboards
- Charts/graphs
- Stakeholder communication

### 5.3 Exit Codes

```python
0   # Success - all validations passed
1   # Partial - some validations failed
2   # Error - evaluation could not complete
3   # Not installed - SAP not found
```

## 6. Error Handling

### 6.1 Common Error Scenarios

**SAP Not Found**:
```
Error: SAP-999 not found
Available SAPs: SAP-000, SAP-001, ..., SAP-018
Did you mean: SAP-009?
```

**Missing Artifacts**:
```
Warning: SAP-004 partially installed
Missing: ledger.md
Action: Run install-sap.py SAP-004 to complete installation
```

**Validation Command Failed**:
```
Warning: Validation check failed
Command: pytest --cov=src
Exit code: 1
Output: [error message]
Action: Fix failing tests before re-evaluating
```

**LLM Inference Error**:
```
Error: LLM analysis failed (timeout)
Falling back to quick check only
Retry with: --deep SAP-004 --retry
```

### 6.2 Graceful Degradation

**If LLM unavailable**:
- Run quick check only (automated validation)
- Warn user deep dive not available
- Provide manual evaluation checklist

**If git history unavailable**:
- Skip timeline analysis
- Use current snapshot only
- Warn that velocity metrics unavailable

**If SAP artifacts incomplete**:
- Evaluate based on available files
- Flag missing artifacts as gaps
- Suggest running install-sap.py

## 7. Security & Privacy

### 7.1 Data Handling

**No external transmission**:
- All evaluation runs locally
- No data sent to external services (except LLM API if configured)
- Results stored in repo only

**LLM Privacy**:
- Only send SAP metadata and file summaries to LLM
- Never send sensitive code (credentials, secrets)
- Support local LLM models (Ollama, etc.)

### 7.2 Safe Command Execution

**Validation commands**:
- Whitelist allowed commands (pytest, git, grep, etc.)
- Sandbox execution (read-only where possible)
- Timeout limits (30s max per command)
- Abort on suspicious commands

## 8. Performance Considerations

### 8.1 Optimization Strategies

**Caching**:
- Cache SAP metadata (sap-catalog.json)
- Cache git history analysis (15-minute TTL)
- Cache LLM responses (same input → same output)

**Parallelization**:
- Run quick checks in parallel (all SAPs)
- Async validation command execution
- Batch LLM requests where possible

**Progressive Loading**:
- Quick check: Minimal file reads
- Deep dive: Load relevant files only
- Strategic: Full analysis only when needed

### 8.2 Performance Targets

| Operation | Target | Measured |
|-----------|--------|----------|
| Quick check (1 SAP) | <5s | TBD |
| Quick check (all SAPs) | <30s | TBD |
| Deep dive (1 SAP) | <5min | TBD |
| Strategic analysis | <30min | TBD |
| Dashboard generation | <2min | TBD |

## 9. Versioning & Compatibility

### 9.1 Protocol Versioning

**Version**: 1.0.0 (initial release)

**Breaking changes** (major version):
- Data model changes (EvaluationResult schema)
- CLI interface changes (command structure)
- Output format changes (incompatible with parsers)

**Non-breaking changes** (minor version):
- New evaluation criteria
- Additional output formats
- Performance improvements

**Patches** (patch version):
- Bug fixes
- Documentation updates
- Prompt refinements

### 9.2 Backward Compatibility

**Evaluation results**:
- Include schema version in output
- Support parsing old formats (1 major version back)
- Provide migration scripts if needed

**CLI**:
- Maintain old command structure (deprecation warnings)
- Support legacy output formats (--format legacy)

---

## 9.5. Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/sap-self-evaluation/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Quick Reference / Quick Start for Claude
- [ ] Common Workflows / Claude Code Workflows (5 workflows in AGENTS.md, 3 in CLAUDE.md)
- [ ] Best Practices / Claude-Specific Tips (5 tips each)
- [ ] Common Pitfalls (5 pitfalls each)
- [ ] Integration with Other SAPs / Support & Resources

**Source Artifact Coverage (Both Files)**:
- [ ] capability-charter.md problem statement → "When to Use" section
- [ ] protocol-spec.md data models/APIs → "Core Files" section (AGENTS) / "Tool Usage" (CLAUDE)
- [ ] awareness-guide.md workflows → "Common Workflows" section
- [ ] adoption-blueprint.md installation → "Quick Reference" section
- [ ] ledger.md metrics → referenced in "Best Practices" (track gaps in ledger)

**YAML Frontmatter Fields** (Required):
```yaml
sap_id: SAP-019
version: X.Y.Z
status: active | pilot | draft
last_updated: YYYY-MM-DD
type: reference
audience: agents | claude_code
complexity: beginner | intermediate | advanced
estimated_reading_time: N
progressive_loading:
  phase_1: "lines 1-X"
  phase_2: "lines X-Y"
  phase_3: "full"
phase_1_token_estimate: NNNN
phase_2_token_estimate: NNNN
phase_3_token_estimate: NNNN
```

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/sap-self-evaluation/AGENTS.md && \
test -f docs/skilled-awareness/sap-self-evaluation/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/sap-self-evaluation/AGENTS.md | grep "progressive_loading:"
grep -A 10 "^---$" docs/skilled-awareness/sap-self-evaluation/CLAUDE.md | grep "progressive_loading:"

# Check workflow count equivalence (should be within ±30%)
agents_workflows=$(grep "^### Workflow" docs/skilled-awareness/sap-self-evaluation/AGENTS.md | wc -l)
claude_workflows=$(grep "^### Workflow" docs/skilled-awareness/sap-self-evaluation/CLAUDE.md | wc -l)
echo "AGENTS workflows: $agents_workflows, CLAUDE workflows: $claude_workflows"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-019
```

**Expected Workflow Coverage**:
- AGENTS.md: 5 generic agent workflows (Quick Check, Deep Dive, Strategic Analysis, Batch Evaluation, Validate Installation)
- CLAUDE.md: 3 Claude Code workflows (Quick Check with Bash, Deep Dive with Read, Strategic Roadmap with Edit)
- Rationale: Different granularity acceptable - AGENTS.md covers all evaluation modes, CLAUDE.md focuses on high-level Claude Code tool patterns

---

## 10. Future Enhancements

### 10.1 Planned Features (v1.1.0)

- **Automated usage detection**: Scan codebase for SAP artifact usage
- **Comparative benchmarking**: Compare against recommended baseline
- **ROI prediction**: Estimate value of adopting SAP-X next
- **CI/CD integration**: Run quick checks in GitHub Actions

### 10.2 Considered Features (v2.0.0)

- **Interactive web dashboard**: Real-time metrics, drill-down views
- **Ecosystem analytics**: Cross-repo adoption trends
- **AI-driven recommendations**: LLM suggests which SAP to adopt based on project type
- **Automated remediation**: Generate PRs to fix gaps

## 11. Reference Implementation

See:
- [scripts/sap-evaluator.py](../../../scripts/sap-evaluator.py) - CLI tool
- [utils/sap_evaluation.py](../../../utils/sap_evaluation.py) - Core engine
- [docs/skilled-awareness/sap-self-evaluation/schemas/](schemas/) - JSON schemas
- [scripts/templates/](../../../scripts/templates/) - LLM prompt templates
