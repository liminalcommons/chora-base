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

### 3.5 Discoverability Assessment Protocol

**Purpose**: Evaluate SAP discoverability across root awareness files and CLI touchpoints (2-5 minutes).

**Rationale**: Implementation quality is irrelevant if agents cannot discover the capability exists. This protocol measures how easily agents can find and understand SAP capabilities from root files (README.md, AGENTS.md, CLAUDE.md, justfile).

**Key Principle**: "The better the pattern, the worse the impact if undiscoverable" - advanced patterns (like SAP-009 nested hierarchies) require proportionally higher discoverability.

#### 3.5.1 Discoverability Scoring Framework

**Total Score**: 100 points across 6 touchpoints

| Touchpoint | Points | Description |
|-----------|--------|-------------|
| **README.md** | 30 | Dedicated section with use cases, examples, ROI |
| **AGENTS.md** | 20 | Dedicated section with workflows, integrations |
| **CLAUDE.md** | 15 | Claude-specific guidance or domain links |
| **justfile** | 15 | ≥3 recipes with comments and examples |
| **Documentation** | 10 | How-to guides, explanations, references |
| **Examples** | 10 | Working implementations or code samples |

**Score Interpretation**:
- **80-100**: HIGH - Excellent discoverability, agents find SAP easily (<5 min)
- **50-79**: MEDIUM - Adequate, but gaps exist (5-15 min discovery time)
- **0-49**: LOW - Critical gap, blocks adoption (>15 min or never discovered)

**L1 Requirement**: Score ≥80/100 (required before marking Level 1 complete)

#### 3.5.2 Touchpoint Scoring Criteria

**README.md (30 points)**:
- **30 points**: Dedicated section (≥30 lines) with:
  - "When to use SAP-XXX" (5 use cases)
  - "What you get" (detailed features)
  - Quick-start code example (5-10 commands)
  - Links to nested files (if SAP-009)
  - ROI statement (quantified value)
  - Documentation links
- **15 points**: Mentioned (10-29 lines) with some examples
- **5 points**: Brief mention only (<10 lines)
- **0 points**: Not mentioned

**Validation**:
```bash
grep -A 40 "### SAP-XXX\|### [SAP Name]" README.md | wc -l
# Target: ≥30 lines for full credit
```

**AGENTS.md (20 points)**:
- **20 points**: Dedicated section (≥60 lines) with:
  - "When to use SAP-XXX" (5+ scenarios)
  - Quick-start approach with commands
  - "What you get" (detailed capabilities)
  - Example workflow (complete scenario)
  - Integration patterns with other SAPs
  - Links to nested AGENTS.md (if applicable)
  - ROI statement
- **10 points**: Section exists (30-59 lines) with some guidance
- **5 points**: Listed in SAP catalog only (1-2 lines)
- **0 points**: Not mentioned

**Validation**:
```bash
grep -A 70 "### SAP-XXX\|### [SAP Name]" AGENTS.md | wc -l
# Target: ≥60 lines for full credit
```

**CLAUDE.md (15 points)**:
- **15 points**: Dedicated workflow/pattern section OR domain section with direct links
- **7 points**: Mentioned in context (integration pattern, example)
- **0 points**: Not mentioned

**Validation**:
```bash
grep -i "SAP-XXX\|[sap-name]" CLAUDE.md && echo "✅ Mentioned" || echo "❌ Not found"
```

**justfile (15 points)**:
- **15 points**: ≥3 recipes with:
  - Section header (# === SAP-XXX: Name ===)
  - Section comment (SAP purpose)
  - Inline comment for each recipe (# Description)
  - Usage example for complex recipes (# Example: just ...)
  - Default values for arguments
- **10 points**: 1-2 recipes with comments
- **5 points**: 1 recipe without comments
- **0 points**: No recipes

**Validation**:
```bash
grep -A 20 "SAP-XXX" justfile | grep "^[a-z]" | wc -l
# Target: ≥3 recipes
```

**Documentation (10 points)**:
- **10 points**: ≥3 docs (how-to, explanation, reference) in SAP-007 structure
- **5 points**: 1-2 docs
- **0 points**: No documentation

**Validation**:
```bash
ls docs/how-to/*[sap-name]* docs/explanation/*[sap-name]* docs/reference/*[sap-name]* 2>/dev/null | wc -l
# Target: ≥3 files
```

**Examples (10 points)**:
- **10 points**: ≥5 working implementations or code samples
- **5 points**: 1-4 examples
- **0 points**: No examples

**Validation**:
```bash
grep -r "SAP-XXX\|[sap-name]" examples/ tests/ 2>/dev/null | wc -l
# Target: ≥5 occurrences
```

#### 3.5.3 Automated Discoverability Audit

**Data Model**:
```python
@dataclass
class DiscoverabilityResult:
    """Result of SAP discoverability assessment"""

    # Identity
    sap_id: str
    sap_name: str
    timestamp: datetime

    # Scores (out of max points)
    readme_score: int           # 0-30
    agents_score: int           # 0-20
    claude_score: int           # 0-15
    justfile_score: int         # 0-15
    docs_score: int             # 0-10
    examples_score: int         # 0-10

    total_score: int            # 0-100
    level: str                  # "HIGH" | "MEDIUM" | "LOW"

    # Detailed findings
    readme_lines: int
    agents_lines: int
    claude_mentioned: bool
    recipe_count: int
    doc_count: int
    example_count: int

    # Gaps
    missing_touchpoints: list[str]
    below_threshold_touchpoints: list[str]

    # Recommendations
    priority_improvements: list[Action]
    estimated_effort_hours: float  # To reach ≥80
```

**CLI Interface**:
```bash
# Audit single SAP
python scripts/sap-evaluator.py --disc SAP-010

# Audit all SAPs
python scripts/sap-evaluator.py --disc --all

# Generate discoverability report
python scripts/sap-evaluator.py --disc SAP-010 --format md > disc-report.md
```

**Example Output**:
```
SAP-010 (Memory System) - Discoverability Audit
================================================
Generated: 2025-11-09 15:30:00

## Scores by Touchpoint

✅ README.md:      30/30 (Dedicated section, 45 lines)
✅ AGENTS.md:      20/20 (Dedicated section, 75 lines)
✅ CLAUDE.md:      15/15 (Domain section with links)
✅ justfile:       15/15 (8 recipes with comments)
❌ Documentation:   0/10 (No how-to guides found)
✅ Examples:       10/10 (12 examples found)

## Overall Score: 90/100 (HIGH)

✅ Meets L1 requirement (≥80/100)
✅ Agent discovery time: <5 minutes (estimated)
⚠️  Missing documentation touchpoint

## Priority Improvements (to reach 100/100)

1. Create how-to guide (P1, 1-2 hours)
   File: docs/how-to/using-memory-system.md
   Content: Quick start, common tasks, troubleshooting

Estimated effort to 100/100: 1-2 hours

Run deep dive for full analysis:
  python scripts/sap-evaluator.py --deep SAP-010
```

#### 3.5.4 Integration with Deep Dive Protocol

**Add to Deep Dive Evaluation**:

When running deep dive assessment, include discoverability check:

```python
def deep_dive_evaluation(sap_id: str) -> EvaluationResult:
    # Existing deep dive steps...

    # NEW: Add discoverability assessment
    disc_result = assess_discoverability(sap_id)

    # Fail L1 validation if discoverability <80
    if disc_result.total_score < 80:
        result.blockers.append(
            f"Discoverability score too low ({disc_result.total_score}/100, "
            f"target: ≥80/100). Cannot mark L1 complete until improved."
        )
        result.gaps.append(Gap(
            gap_id="disc-001",
            gap_type="installation",
            title="Discoverability below L1 requirement",
            description=f"SAP is {disc_result.total_score}/100 discoverable. "
                        f"Missing touchpoints: {disc_result.missing_touchpoints}",
            impact="high",
            effort="low" if disc_result.total_score >= 60 else "medium",
            priority="P0",  # Blocks L1
            actions=disc_result.priority_improvements,
            estimated_hours=disc_result.estimated_effort_hours
        ))

    return result
```

#### 3.5.5 Discovery-to-Value Ratio

**Metric**: Value gained per session / Discovery cost (one-time)

**Target**: Ratio ≥ 2.0 (value exceeds discovery cost from first session)

**Calculation**:
```python
def calculate_discovery_to_value_ratio(sap_id: str) -> float:
    """Calculate ROI ratio for discoverability investment"""

    # Estimate discovery cost based on discoverability score
    disc_score = get_discoverability_score(sap_id)
    if disc_score >= 80:
        discovery_time_min = 2  # Easy to find (<2 min)
    elif disc_score >= 50:
        discovery_time_min = 10  # Medium effort (5-15 min)
    else:
        discovery_time_min = 20  # Hard to find or never discovered

    # Estimate value gained per session (from SAP metadata or ledger)
    value_per_session_min = get_sap_value_per_session(sap_id)  # e.g., 10 min saved

    # Ratio
    ratio = value_per_session_min / discovery_time_min

    return ratio

# Example:
# SAP-010 (Memory System)
# - Discoverability: 90/100 → Discovery time: 2 min
# - Value per session: 12 min (context restoration)
# - Ratio: 12 / 2 = 6.0 (excellent - value >> cost)

# SAP-010 (before improvements)
# - Discoverability: 40/100 → Discovery time: 20 min
# - Value per session: 12 min
# - Ratio: 12 / 20 = 0.6 (poor - cost > value in first session)
```

#### 3.5.6 Meta-Discoverability Principle

**For SAPs using advanced patterns** (SAP-009 nested hierarchies, SAP-012 planning, etc.):

**Higher discoverability threshold**:
- Standard SAPs: ≥80/100
- Advanced pattern SAPs: ≥85/100

**Required elements** (in addition to standard touchpoints):
1. Explicit statement of pattern benefits (e.g., "60-70% token reduction")
2. Read time estimates (e.g., "8-min, 5k tokens")
3. Direct links from root to nested files (not optional)
4. "Navigation tip" sections

**Rationale**: Without strong discoverability, navigation tax exceeds pattern benefits, making advanced patterns net negative.

**Example** (SAP-010 with nested .chora/CLAUDE.md):

```markdown
### Domain 4: Memory System (.chora/)

**Path**: [.chora/AGENTS.md](.chora/AGENTS.md) + [.chora/CLAUDE.md](.chora/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.chora/CLAUDE.md](.chora/CLAUDE.md) - Claude workflows (8-min, 5k tokens)
- [.chora/AGENTS.md](.chora/AGENTS.md) - Memory patterns (13-min, 10k tokens)

**Use when**:
- Creating knowledge notes
- Querying event logs
- Restoring context across sessions
```

#### 3.5.7 Validation Script

**Core function**:

```python
def audit_discoverability(sap_id: str) -> DiscoverabilityResult:
    """Audit SAP discoverability across 6 touchpoints."""

    sap_name = get_sap_name(sap_id)
    score = 0
    missing = []
    below_threshold = []

    # README.md (30 points)
    readme_lines = count_sap_section_lines("README.md", sap_id, sap_name)
    if readme_lines >= 30:
        readme_score = 30
    elif readme_lines >= 10:
        readme_score = 15
        below_threshold.append("README.md (15/30)")
    elif readme_lines >= 1:
        readme_score = 5
        below_threshold.append("README.md (5/30)")
    else:
        readme_score = 0
        missing.append("README.md")

    # AGENTS.md (20 points)
    agents_lines = count_sap_section_lines("AGENTS.md", sap_id, sap_name)
    if agents_lines >= 60:
        agents_score = 20
    elif agents_lines >= 30:
        agents_score = 10
        below_threshold.append("AGENTS.md (10/20)")
    elif has_catalog_entry("AGENTS.md", sap_id):
        agents_score = 5
        below_threshold.append("AGENTS.md (5/20)")
    else:
        agents_score = 0
        missing.append("AGENTS.md")

    # CLAUDE.md (15 points)
    claude_mentioned = is_mentioned("CLAUDE.md", sap_id, sap_name)
    if has_dedicated_section("CLAUDE.md", sap_id, sap_name):
        claude_score = 15
    elif claude_mentioned:
        claude_score = 7
        below_threshold.append("CLAUDE.md (7/15)")
    else:
        claude_score = 0
        missing.append("CLAUDE.md")

    # justfile (15 points)
    recipe_count = count_recipes("justfile", sap_id, sap_name)
    if recipe_count >= 3:
        justfile_score = 15
    elif recipe_count >= 1:
        has_comments = check_recipe_comments("justfile", sap_id)
        justfile_score = 10 if has_comments else 5
        below_threshold.append(f"justfile ({justfile_score}/15)")
    else:
        justfile_score = 0
        missing.append("justfile")

    # Documentation (10 points)
    doc_count = count_docs(sap_name)
    if doc_count >= 3:
        docs_score = 10
    elif doc_count >= 1:
        docs_score = 5
        below_threshold.append("Documentation (5/10)")
    else:
        docs_score = 0
        missing.append("Documentation")

    # Examples (10 points)
    example_count = count_examples(sap_id, sap_name)
    if example_count >= 5:
        examples_score = 10
    elif example_count >= 1:
        examples_score = 5
        below_threshold.append("Examples (5/10)")
    else:
        examples_score = 0
        missing.append("Examples")

    total_score = (readme_score + agents_score + claude_score +
                   justfile_score + docs_score + examples_score)

    level = "HIGH" if total_score >= 80 else "MEDIUM" if total_score >= 50 else "LOW"

    # Generate priority improvements
    priority_improvements = generate_improvement_actions(
        sap_id, sap_name, missing, below_threshold
    )

    # Estimate effort to reach ≥80
    effort_hours = estimate_discoverability_improvement_effort(
        total_score, missing, below_threshold
    )

    return DiscoverabilityResult(
        sap_id=sap_id,
        sap_name=sap_name,
        timestamp=datetime.now(),
        readme_score=readme_score,
        agents_score=agents_score,
        claude_score=claude_score,
        justfile_score=justfile_score,
        docs_score=docs_score,
        examples_score=examples_score,
        total_score=total_score,
        level=level,
        readme_lines=readme_lines,
        agents_lines=agents_lines,
        claude_mentioned=claude_mentioned,
        recipe_count=recipe_count,
        doc_count=doc_count,
        example_count=example_count,
        missing_touchpoints=missing,
        below_threshold_touchpoints=below_threshold,
        priority_improvements=priority_improvements,
        estimated_effort_hours=effort_hours
    )
```

**Helper functions**:

```python
def count_sap_section_lines(file: str, sap_id: str, sap_name: str) -> int:
    """Count lines in SAP's dedicated section"""
    # Search for "### SAP-XXX" or "### [SAP Name]"
    # Count lines until next "###" or "##"
    pass

def count_recipes(file: str, sap_id: str, sap_name: str) -> int:
    """Count justfile recipes related to SAP"""
    # Search for section header or individual recipes
    # Match recipe names containing sap_name
    pass

def count_docs(sap_name: str) -> int:
    """Count documentation files"""
    # Check docs/how-to/, docs/explanation/, docs/reference/
    # Match files containing sap_name
    pass

def count_examples(sap_id: str, sap_name: str) -> int:
    """Count code examples"""
    # Search examples/ and tests/ directories
    # Match SAP-XXX or sap_name references
    pass

def generate_improvement_actions(sap_id: str, sap_name: str,
                                  missing: list[str],
                                  below_threshold: list[str]) -> list[Action]:
    """Generate prioritized actions to improve discoverability"""
    # Prioritize: missing touchpoints first, then below-threshold
    # Use templates from discoverability checklist
    pass

def estimate_discoverability_improvement_effort(total_score: int,
                                                 missing: list[str],
                                                 below_threshold: list[str]) -> float:
    """Estimate hours to reach ≥80/100"""
    # Missing README section: 1-2 hours
    # Missing AGENTS section: 2-3 hours
    # Missing justfile recipes: 2-3 hours
    # Below threshold adjustments: 0.5-1 hour each
    pass
```

#### 3.5.8 Usage in L1 Validation

**Update Level 1 completion criteria**:

```python
def validate_level_1_complete(sap_id: str) -> EvaluationResult:
    """Validate SAP meets Level 1 requirements"""

    result = EvaluationResult(sap_id=sap_id, current_level=1)

    # Existing L1 checks (installation, basic functionality)
    # ...

    # NEW: Discoverability check (required for L1)
    disc_result = audit_discoverability(sap_id)

    if disc_result.total_score < 80:
        result.validation_results["discoverability"] = False
        result.blockers.append(
            f"Discoverability score {disc_result.total_score}/100 "
            f"(target: ≥80/100). Add README.md, AGENTS.md sections, "
            f"justfile recipes before marking L1 complete."
        )
        result.current_level = 0  # Not complete until discoverable
    else:
        result.validation_results["discoverability"] = True

    return result
```

**Recommended workflow**:

```bash
# 1. Install SAP (implementation)
python scripts/install-sap.py SAP-010

# 2. Validate installation
python scripts/sap-evaluator.py --quick SAP-010
# Status: "Installed, but discoverability <80 (blocksL1)"

# 3. Improve discoverability
python scripts/sap-evaluator.py --disc SAP-010
# Shows: Missing README.md section (0/30), AGENTS.md section (5/20)

# 4. Add sections (use templates from adoption blueprint)
# ... (edit README.md, AGENTS.md, justfile)

# 5. Re-validate
python scripts/sap-evaluator.py --disc SAP-010
# Score: 90/100 (HIGH) ✅

# 6. Mark L1 complete
python scripts/sap-evaluator.py --validate-level SAP-010 1
# ✅ Level 1 complete (includes discoverability ≥80/100)
```

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
