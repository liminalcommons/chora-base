---
sap_id: SAP-012
version: 1.1.0
status: Active
last_updated: 2025-11-06
audience: ai-agents
---

# Awareness Guide: Development Lifecycle

**SAP ID**: SAP-012
**For**: AI Coding Agents
**Purpose**: Workflows for executing the 8-phase development lifecycle

---

## 1. Quick Reference

### When to Use This SAP

| User Request | Workflow to Use |
|--------------|-----------------|
| "Add feature X" | [3.1 Implement New Feature](#31-implement-new-feature-using-full-lifecycle) |
| "Fix bug Y" | [3.2 Fix Bug](#32-fix-bug) |
| "Refactor Z" | [3.3 Refactor Code](#33-refactor-code) |
| "Plan sprint" | [3.4 Sprint Planning](#34-sprint-planning) |
| "Release version" | [3.5 Release Version](#35-release-version) |

### Phase Quick Reference

| Phase | Agent Action | Tools |
|-------|--------------|-------|
| **Phase 1: Vision** | Read ROADMAP.md | Read |
| **Phase 2: Planning** | Use sprint-template.md | Write, Edit |
| **Phase 3: Requirements (DDD)** | Write Diataxis docs | Write (Explanation, Reference) |
| **Phase 4: Development (BDD+TDD)** | Write .feature files, tests, code | Write, Bash (pytest) |
| **Phase 5: Testing** | Run pytest, ruff, mypy | Bash |
| **Phase 6: Review** | Create PR | Bash (gh pr create) |
| **Phase 7: Release** | Run release scripts | Bash (bump-version.sh, publish-prod.sh) |
| **Phase 8: Monitoring** | Update PROCESS_METRICS.md | Edit |

### Light+ Planning Constructs (NEW in v1.1)

**What**: 4-level planning hierarchy (Strategy → Releases → Features → Tasks)
**Why**: Provides structure for **WHAT** to build (planning constructs) separate from **HOW** to build it (8 phases)

| Construct | Owner | Cadence | Artifact | Phase |
|-----------|-------|---------|----------|-------|
| **Strategy** | Product/Tech Lead | Quarterly | ROADMAP.md | Phase 1 |
| **Releases** | PM/Scrum Master | Per sprint (1-2 weeks) | Sprint docs | Phase 2 |
| **Features** | Feature Owner/Dev | Per feature | DDD docs, BDD scenarios | Phase 2-3 |
| **Tasks** | Individual Contributors | Daily | .beads/issues.jsonl | Phase 2-8 |

**Agent Usage**:
- Read [LIGHT_PLUS_REFERENCE.md](LIGHT_PLUS_REFERENCE.md) for planning workflows
- Read [protocol-spec.md - Section 2.3](protocol-spec.md#23-light-planning-construct-hierarchy) for technical details
- Use Light+ patterns when planning features, sprints, or strategy

**Key Benefits**:
- **Traceability**: Every task links to feature → release → strategy
- **Scalability**: Simple projects skip Strategy, complex projects use full hierarchy
- **Maturity Tracking**: L0-L5 maturity levels for each construct

---

## 2. Core Workflows

### 2.1 DDD → BDD → TDD Integration

**When**: Implementing new feature with full lifecycle

**Steps**:
1. **DDD (Phase 3)**: Write docs first (Explanation + Reference)
2. **BDD (Phase 4)**: Convert acceptance criteria to Gherkin scenarios
3. **TDD (Phase 4)**: RED-GREEN-REFACTOR until BDD scenarios pass

**Tool Sequence**:
```
Write (Explanation doc)
  ↓
Write (Reference doc with API spec)
  ↓
Write (.feature file with Gherkin scenarios)
  ↓
Write (step definitions in steps/)
  ↓
Bash (pytest features/ → verify RED)
  ↓
Write (test in tests/)
  ↓
Bash (pytest → verify RED)
  ↓
Write (minimal code in src/)
  ↓
Bash (pytest → verify GREEN)
  ↓
Edit (refactor code)
  ↓
Bash (pytest → verify still GREEN)
  ↓
Repeat until all BDD scenarios pass
```

---

## 3. Detailed Workflows

### 3.1 Implement New Feature (Using Full Lifecycle)

**Context**: User requests "Add feature X"

**Phases**: 3 (DDD) → 4 (BDD+TDD) → 5 (Testing) → 6 (Review)

#### Step 1: Phase 3 - DDD (Documentation Driven Design)

**Read relevant docs** to understand context:
```
Read AGENTS.md
Read src/<relevant_module>/__init__.py
Read tests/<relevant_module>/
```

**Write Explanation document** (Why?):
```markdown
File: user-docs/explanation/feature-x-overview.md

---
title: Feature X Overview
type: explanation
status: draft
audience: developers
last_updated: 2025-10-28
---

# Feature X Overview

## Problem
[Describe user problem this feature solves]

## Solution
[Describe high-level solution approach]

## Acceptance Criteria
1. Given [context], when [action], then [outcome]
2. Given [context], when [action], then [outcome]
3. Given [edge case], when [action], then [error handling]
```

**Write Reference document** (What?):
```markdown
File: user-docs/reference/feature-x-api.md

---
title: Feature X API Reference
type: reference
status: draft
audience: developers
last_updated: 2025-10-28
---

# Feature X API

## `feature_x(param1: str, param2: int = 10) -> Result`

**Parameters:**
- `param1` (str): Description
- `param2` (int, optional): Description, defaults to 10

**Returns:**
- `Result`: Object with `success` (bool) and `data` (Any)

**Raises:**
- `ValueError`: If param1 is empty

**Example:**
```python
result = feature_x("value", param2=20)
if result.success:
    print(result.data)
```
```

**Extract acceptance criteria** from Explanation doc → Use in BDD

#### Step 2: Phase 4 - BDD (Behavior Driven Development)

**Write Gherkin scenarios** (.feature file):
```gherkin
File: features/feature_x.feature

Feature: Feature X
  As a user
  I want to use feature X
  So that I can [benefit]

  Scenario: Valid input
    Given valid parameters "value" and 20
    When I call feature_x
    Then the result succeeds
    And the data contains expected values

  Scenario: Invalid input (empty param1)
    Given empty param1
    When I call feature_x
    Then a ValueError is raised
    And the error message includes "param1"
```

**Write step definitions**:
```python
File: features/steps/feature_x_steps.py

from pytest_bdd import scenarios, given, when, then, parsers
from src.module.feature_x import feature_x

scenarios('../feature_x.feature')

@given(parsers.parse('valid parameters "{param1}" and {param2:d}'))
def valid_params(param1, param2):
    # Setup context
    pass

@when('I call feature_x')
def call_feature_x():
    # Call feature
    pass

@then('the result succeeds')
def result_succeeds():
    # Assert success
    pass
```

**Run BDD tests** (verify RED):
```bash
Bash: pytest features/feature_x.feature
Expected: All scenarios fail (feature not implemented)
```

#### Step 3: Phase 4 - TDD (Test Driven Development)

**RED-GREEN-REFACTOR cycles**:

**Cycle 1: RED**
```python
File: tests/test_feature_x.py

def test_feature_x_with_valid_input():
    """Test feature_x succeeds with valid input."""
    result = feature_x("value", param2=20)
    assert result.success is True
    assert result.data is not None
```

```bash
Bash: pytest tests/test_feature_x.py
Expected: Test fails (feature_x not implemented)
```

**Cycle 1: GREEN**
```python
File: src/module/feature_x.py

from dataclasses import dataclass
from typing import Any

@dataclass
class Result:
    success: bool
    data: Any

def feature_x(param1: str, param2: int = 10) -> Result:
    """Feature X implementation."""
    if not param1:
        raise ValueError("param1 cannot be empty")

    # Minimal implementation
    return Result(success=True, data={"param1": param1, "param2": param2})
```

```bash
Bash: pytest tests/test_feature_x.py
Expected: Test passes (GREEN)
```

**Cycle 1: REFACTOR**
```python
Edit src/module/feature_x.py
# Improve design, add docstrings, improve error handling
# Tests must stay GREEN
```

**Repeat cycles** until all BDD scenarios pass:
```bash
Bash: pytest features/feature_x.feature
Expected: All scenarios pass (GREEN)
```

#### Step 4: Phase 5 - Testing & Quality

**Run full test suite**:
```bash
Bash: pytest --cov=src --cov-report=term
Expected: Coverage ≥85%
```

**Run linting**:
```bash
Bash: ruff check src/ tests/
Expected: No errors
```

**Run type checking**:
```bash
Bash: mypy src/ tests/
Expected: No errors
```

**Run pre-merge checks** (all quality gates):
```bash
Bash: just pre-merge
Expected: All checks pass
```

#### Step 5: Phase 6 - Review & Integration

**Create pull request**:
```bash
Bash: git checkout -b feature/feature-x
Bash: git add .
Bash: git commit -m "feat: Add feature X

Implements feature X with DDD→BDD→TDD approach.

- Add Explanation and Reference docs
- Add BDD scenarios (.feature file)
- Add unit tests (coverage: 95%)
- All quality gates pass

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

Bash: git push -u origin feature/feature-x
Bash: gh pr create --title "feat: Add feature X" --body "$(cat <<'EOF'
## Summary
- Implements feature X
- Full DDD→BDD→TDD approach
- Coverage: 95%

## Test plan
- [x] Unit tests pass
- [x] BDD scenarios pass
- [x] Coverage ≥85%
- [x] Linting passes
- [x] Type checking passes

🤖 Generated with Claude Code
EOF
)"
```

**Wait for review** → Address feedback → Merge

---

### 3.2 Fix Bug

**Context**: User reports "Bug: X doesn't work when Y"

**Phases**: 4 (TDD only) → 5 (Testing) → 6 (Review)

#### Step 1: Write Failing Test (Reproduces Bug)

**Read relevant code**:
```
Read src/<module_with_bug>.py
Read tests/test_<module_with_bug>.py
```

**Write test that reproduces bug**:
```python
File: tests/test_<module>_bug_fix.py

def test_bug_x_when_y():
    """Test that X works correctly when Y (regression test)."""
    # Setup Y condition
    result = function_x(condition_y=True)

    # Assert expected behavior (currently fails)
    assert result.success is True  # This will fail (bug exists)
```

**Run test** (verify RED):
```bash
Bash: pytest tests/test_<module>_bug_fix.py
Expected: Test fails (bug reproduced)
```

#### Step 2: Fix Bug (Make Test Pass)

**Edit code to fix bug**:
```python
Edit src/<module_with_bug>.py
# Fix the bug
```

**Run test** (verify GREEN):
```bash
Bash: pytest tests/test_<module>_bug_fix.py
Expected: Test passes (bug fixed)
```

#### Step 3: Verify No Regression

**Run full test suite**:
```bash
Bash: pytest
Expected: All tests pass
```

#### Step 4: Create PR

```bash
Bash: git checkout -b fix/bug-x-when-y
Bash: git add .
Bash: git commit -m "fix: X now works when Y

Fixes bug where X failed when Y condition was true.

- Add regression test
- Fix logic in src/<module>.py

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

Bash: git push -u origin fix/bug-x-when-y
Bash: gh pr create --title "fix: X now works when Y" --body "Fixes bug with regression test"
```

---

### 3.3 Refactor Code

**Context**: User requests "Refactor module X for better maintainability"

**Phases**: 4 (TDD with existing tests) → 5 (Testing) → 6 (Review)

#### Step 1: Ensure Tests Exist

**Read existing tests**:
```
Read tests/test_<module>.py
```

**If missing tests, write them first**:
```python
Write tests/test_<module>.py
# Add comprehensive tests for current behavior
```

**Run tests** (verify GREEN before refactoring):
```bash
Bash: pytest tests/test_<module>.py
Expected: All tests pass (baseline)
```

#### Step 2: Refactor (Tests Stay GREEN)

**Edit code** (improve design):
```python
Edit src/<module>.py
# Refactor: Extract functions, improve names, simplify logic
# DO NOT change behavior (tests must stay GREEN)
```

**Run tests after each change**:
```bash
Bash: pytest tests/test_<module>.py
Expected: All tests still pass (GREEN)
```

#### Step 3: Verify Full Suite

```bash
Bash: pytest
Expected: All tests pass (no regression)
```

#### Step 4: Create PR

```bash
Bash: git checkout -b refactor/module-x
Bash: git add .
Bash: git commit -m "refactor: Improve module X maintainability

- Extract helper functions
- Improve variable names
- Simplify complex logic
- No behavior changes (all tests pass)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

Bash: git push -u origin refactor/module-x
Bash: gh pr create --title "refactor: Improve module X" --body "Refactoring with no behavior changes"
```

---

### 3.4 Sprint Planning

**Context**: User requests "Plan next sprint"

**Phase**: 2 (Planning & Prioritization)

#### Step 1: Read Sprint Template

```
Read project-docs/sprints/sprint-template.md
```

#### Step 2: Read Current Sprint (If Exists)

```
Glob: project-docs/sprints/sprint-*.md
Read project-docs/sprints/sprint-<latest>.md
# Identify sprint number, review velocity
```

#### Step 3: Create New Sprint Plan

**Copy template** and fill in details:
```markdown
File: project-docs/sprints/sprint-<NN>.md

# Sprint <NN> Plan

**Sprint Number**: <NN>
**Duration**: 2025-MM-DD to 2025-MM-DD (2 weeks)
**Sprint Goals**:
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Committed Items

| Item | Type | Story Points | Owner | Status |
|------|------|--------------|-------|--------|
| Feature X | Feature | 5 | Victor | Not Started |
| Bug Y | Bug | 2 | Victor | Not Started |
| Tech Debt Z | Tech Debt | 3 | Victor | Not Started |

**Total Committed**: 10 story points

## Definition of Done
- [ ] All tests pass
- [ ] Coverage ≥85%
- [ ] Code reviewed
- [ ] Docs updated
- [ ] Deployed to staging

## Risks
- Dependency on external API (may cause delays)

## Retrospective
_(Fill at sprint end)_

### What Went Well
-

### What Could Improve
-

### Action Items
-
```

**Write sprint plan**:
```
Write project-docs/sprints/sprint-<NN>.md
# Use content above
```

---

### 3.5 Vision Synthesis Workflows

**When**: Quarterly strategic planning cycle (or monthly discovery for high-velocity projects)

**Purpose**: Transform scattered user intentions (inbox, GitHub, dogfooding, research, A-MEM) into structured strategic vision and operational backlog.

**Phases**: 4 sub-phases over 5-8 days (Discovery → Analysis → Vision Drafting → Backlog Cascade)

---

#### 3.5.1 Intention Discovery (Phase 1.1)

**Context**: Quarterly planning cycle begins, need to consolidate scattered intentions

**Duration**: 1-2 days

**Steps**:

**1. Check for Existing Intention Inventory**
```bash
# Query latest inventory
grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | sort | tail -1

# Read if exists
Read .chora/memory/knowledge/notes/intention-inventory-{latest-date}.md
```

**2. Copy Template**
```bash
# Use SAP-010 template
Bash: cp .chora/memory/templates/intention-inventory-template.md \
         .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md
```

**3. Scan 5 Intention Sources**

**Source 1: Inbox Coordination Requests (SAP-001)**
```bash
Bash: cat inbox/coordination/active.jsonl
# Extract: title, description, priority, requester
```

**Source 2: GitHub Issues**
```bash
Bash: gh issue list --label feature-request,high-demand --limit 50 --json number,title,labels,reactions
# Filter: upvotes ≥ 3, comments ≥ 5
```

**Source 3: Dogfooding Pilot Feedback (SAP-027)**
```bash
# Query pilot summaries
Bash: grep -l '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md

# Read final summaries for GO decisions
Read .chora/memory/knowledge/notes/{pilot-summary}.md
```

**Source 4: Research Reports**
```bash
Bash: ls docs/research/*-research.md

# Read recent reports (last 3 months)
Read docs/research/2025-11-*-research.md
```

**Source 5: A-MEM Knowledge Notes (SAP-010)**
```bash
# Query user requests
Bash: grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md

# Query unfulfilled needs
Bash: grep '"tags".*unmet-need' .chora/memory/knowledge/notes/*.md
```

**4. Consolidate into Intention Inventory**

For each intention, record:
```yaml
---
id: intention-{number}
title: {intention title}
source: {inbox|github|dogfooding|research|a-mem}
evidence_level: {A|B|C}
evidence_citations:
  - {citation 1}
  - {citation 2}
user_demand: {count of users requesting}
related_saps: [{SAP-XXX}]
priority: {LOW|MEDIUM|HIGH}
---

## Description
{detailed description}

## Evidence Assessment
- **Level A (Standards)**: {percentage}% - {list citations}
- **Level B (Case Studies)**: {percentage}% - {list citations}
- **Level C (Expert Opinion)**: {percentage}% - {list citations}
```

**5. Calculate Evidence Percentages**
```python
# For each intention, calculate:
evidence_a_pct = len(level_a_citations) / total_citations * 100
evidence_b_pct = len(level_b_citations) / total_citations * 100
evidence_c_pct = len(level_c_citations) / total_citations * 100

# Wave 1 target: A+B ≥ 70%
# Wave 2 target: A+B ≥ 60%
```

**Example Output** (chora-base Nov 2025):
- **89 intentions** discovered from 5 sources
- **42 HIGH-priority** (A+B ≥ 70%, user_demand ≥ 10)
- **Evidence breakdown**: 32% A (standards), 48% B (case studies), 20% C (opinion)
- **Top sources**: GitHub issues (34), inbox (12), dogfooding (15), research (18), A-MEM (10)

---

#### 3.5.2 Strategic Theme Analysis (Phase 1.2)

**Context**: Intention inventory complete, need to cluster into strategic themes

**Duration**: 1-2 days

**Steps**:

**1. Copy Strategic Theme Matrix Template**
```bash
Bash: cp .chora/memory/templates/strategic-theme-matrix-template.md \
         .chora/memory/knowledge/notes/strategic-themes-2025-11-05.md
```

**2. Cluster Intentions by Pattern**

Read intention inventory and identify patterns:
```python
# Group by similar user needs
themes = {}
for intention in intentions:
    # Pattern recognition: similar keywords, SAPs, user problem
    if matches_pattern(intention, "automation"):
        themes["automation"].append(intention)
    elif matches_pattern(intention, "documentation"):
        themes["documentation"].append(intention)
    # ... etc
```

**3. For Each Theme, Calculate Aggregate Metrics**
```yaml
theme:
  name: {theme name}
  intentions: [{list of intention IDs}]
  total_user_demand: {sum of user_demand across intentions}
  evidence_a_b_pct: {weighted average of A+B percentages}
  effort_estimate: {sum of effort estimates}
  strategic_alignment: {HIGH|MEDIUM|LOW}
  related_saps: [{unique SAPs across intentions}]
```

**4. Apply Wave Decision Criteria**

**Wave 1 (Committed - 3 months)**:
```python
wave_1_themes = []
for theme in themes:
    if (theme.evidence_a_b_pct >= 70 and
        theme.total_user_demand >= 10 and
        theme.effort_estimate < 50):  # hours
        wave_1_themes.append(theme)
```

**Wave 2 (Exploratory - 6 months)**:
```python
wave_2_themes = []
for theme in themes:
    if (theme.evidence_a_b_pct >= 60 and
        theme.total_user_demand >= 5 and
        theme.effort_estimate < 200):  # hours
        # Validate via dogfooding (SAP-027)
        wave_2_themes.append(theme)
```

**Wave 3 (Aspirational - 12 months)**:
```python
wave_3_themes = []
for theme in themes:
    if theme.evidence_a_b_pct < 60:
        # Defer to quarterly review
        wave_3_themes.append(theme)
```

**5. Write Strategic Theme Matrix**
```markdown
## Strategic Themes Matrix

| Theme | Intentions | User Demand | Evidence (A+B) | Effort | Wave | Decision |
|-------|------------|-------------|----------------|--------|------|----------|
| Strategic Planning Infrastructure | 12 | 45 | 78% | 40h | 1 | Commit |
| SAP Generation Automation | 8 | 22 | 85% | 30h | 1 | Commit |
| Multi-Repo Coordination | 6 | 15 | 65% | 80h | 2 | Pilot |
| Advanced Analytics | 4 | 8 | 55% | 120h | 3 | Defer |
```

**Example Output** (chora-base Nov 2025):
- **5 strategic themes** from 42 HIGH-priority intentions
- **2 themes → Wave 1** (Strategic Planning, SAP Generation)
- **2 themes → Wave 2** (Multi-Repo Coordination, Advanced Metrics)
- **1 theme → Wave 3** (Advanced Analytics)

---

#### 3.5.3 Vision Drafting (Phase 1.3)

**Context**: Strategic themes prioritized into waves, need to draft vision document

**Duration**: 2-3 days

**Steps**:

**1. Copy Vision Document Template**
```bash
Bash: cp .chora/memory/templates/vision-document-template.md \
         .chora/memory/knowledge/notes/vision-chora-base-6-month.md
```

**2. Define Multi-Timeframe Horizons**

**3-Month Horizon (Wave 1 - Committed)**
```markdown
## Wave 1: Strategic Planning Infrastructure (Committed - 3 months)

**Status**: Committed in ROADMAP.md
**Target Version**: v1.5.0
**Target Date**: 2026-02-01

### Features
1. **SAP-010 Strategic Templates** - Evidence: 85% A+B, Demand: 30 users
   - 4 templates: vision, intention inventory, theme matrix, roadmap milestone
   - Integration with A-MEM knowledge graph

2. **SAP-006 Vision Synthesis** - Evidence: 78% A+B, Demand: 25 users
   - 4-phase workflow: Discovery → Analysis → Vision → Backlog Cascade
   - Integration with SAP-001, SAP-015, SAP-027

3. **SAP-015 Backlog Organization** - Evidence: 80% A+B, Demand: 28 users
   - Multi-tier priority (P0-P4)
   - Vision cascade (Wave 1 → epic → tasks)
   - Health queries

### Success Criteria
- ✅ All 3 SAPs reach L3 (Production) maturity
- ✅ Time savings ≥ 10x for strategic planning cycles
- ✅ User satisfaction ≥ 85%
- ✅ Adoption ≥ 3 projects (chora-base, 2 ecosystem projects)

### Review Schedule
- Bi-weekly sprint planning (adjust feature scope)
- Bi-weekly sprint retrospective
- Monthly milestone review (v1.5.0 progress)
```

**6-Month Horizon (Wave 2 - Exploratory)**
```markdown
## Wave 2: Automation & Tooling (Exploratory - 6 months)

**Status**: Exploratory (validation via SAP-027 dogfooding)
**Decision Review**: 2026-Q1

### Candidate 1: SAP Generation Automation
- **Evidence**: 85% A+B (8 intentions, validated via SAP-029 pilot)
- **User Demand**: 22 users
- **Validation Status**: ✅ Pilot GO (119x time savings, 100% satisfaction, 0 bugs)
- **Decision**: Promote to Wave 1 in next vision (v1.6.0)

### Candidate 2: Multi-Repo Coordination
- **Evidence**: 65% A+B (6 intentions)
- **User Demand**: 15 users
- **Validation Plan**: Q1 2026 dogfooding pilot (6 weeks)
- **Decision Criteria**: Time savings ≥ 5x, satisfaction ≥ 85%, bugs = 0, adoption ≥ 2
- **Decision**: Defer to Q1 2026 review

### Review Schedule
- Quarterly vision review (update Wave 2 based on pilot results)
```

**12-Month Horizon (Wave 3 - Aspirational)**
```markdown
## Wave 3: Advanced Capabilities (Aspirational - 12 months)

**Status**: Aspirational (directional themes)
**Decision Review**: Quarterly (promote to Wave 2 if evidence/demand increases)

### Theme: Advanced Analytics
- **Evidence**: 55% A+B (4 intentions, mostly Level C)
- **User Demand**: 8 users
- **Strategic Alignment**: MEDIUM (nice-to-have, not critical)
- **Review**: Quarterly check for evidence upgrades (Level C → Level B)
- **Decision**: Deprecate if no traction by Q3 2026
```

**3. Add Traceability Metadata**
```yaml
---
id: vision-chora-base-6-month
type: strategic-vision
status: active
horizon: 6-months
created_at: 2025-11-05
review_schedule: quarterly
input_documents:
  - intention-inventory-2025-11-05
  - strategic-themes-2025-11-05
waves:
  - wave_1_committed: {list of themes}
  - wave_2_exploratory: {list of themes}
  - wave_3_aspirational: {list of themes}
---
```

**Example Output** (chora-base 6-month vision):
- **Wave 1 (Committed)**: 2 themes → 3 SAPs (SAP-010, SAP-006, SAP-015)
- **Wave 2 (Exploratory)**: 2 themes → 2 pilot candidates
- **Wave 3 (Aspirational)**: 1 theme → quarterly review

---

#### 3.5.4 Backlog Cascade (Phase 1.4)

**Context**: Vision Wave 1 defined, need to cascade to operational backlog

**Duration**: 1 day

**Steps**:

**1. Update ROADMAP.md**
```markdown
Read ROADMAP.md

Edit ROADMAP.md:
# Add v1.5.0 milestone

## Version 1.5.0 - Strategic Planning Infrastructure
**Target Date**: 2026-02-01 (3 months)
**Status**: Committed
**Vision**: vision-chora-base-6-month (Wave 1)

### Features
1. SAP-010 Strategic Templates (40h)
2. SAP-006 Vision Synthesis (35h)
3. SAP-015 Backlog Organization (30h)

**Total Effort**: 105 hours (~7 weeks at 15h/week)

### Success Criteria
- All 3 SAPs reach L3 maturity
- Time savings ≥ 10x
- User satisfaction ≥ 85%
- Adoption ≥ 3 projects
```

**2. Create Roadmap Milestone Note**
```bash
Bash: cp .chora/memory/templates/roadmap-milestone-template.md \
         .chora/memory/knowledge/notes/milestone-v1.5.0.md

Edit .chora/memory/knowledge/notes/milestone-v1.5.0.md:
---
id: milestone-v1.5.0
type: roadmap-milestone
version: v1.5.0
target_date: 2026-02-01
status: in_progress
linked_to:
  - vision-chora-base-6-month
  - beads-epic-{id}  # Add epic ID after Step 3
---
```

**3. Create Beads Epic (SAP-015 Integration)**
```bash
Bash: bd create "Wave 1: Strategic Planning Infrastructure (v1.5.0)" \
  --priority 1 \
  --type epic \
  --description "From vision-chora-base-6-month Wave 1. Features: SAP-010, SAP-006, SAP-015 enhancements."

# Output: chora-base-xyz (epic ID)
```

**4. Decompose Epic into Tasks**
```bash
# SAP-010 tasks (7 tasks)
Bash: bd create "SAP-010: Create vision-document-template.md" --priority 2
Bash: bd create "SAP-010: Create intention-inventory-template.md" --priority 2
Bash: bd create "SAP-010: Create strategic-theme-matrix-template.md" --priority 2
Bash: bd create "SAP-010: Create roadmap-milestone-template.md" --priority 2
Bash: bd create "SAP-010: Update protocol-spec Section 3.5" --priority 2
Bash: bd create "SAP-010: Update awareness-guide strategic section" --priority 2
Bash: bd create "SAP-010: Update ledger to v1.1.0" --priority 2

# SAP-006 tasks (7 tasks)
Bash: bd create "SAP-006: Expand protocol-spec Section 3.1 (4 sub-phases)" --priority 2
Bash: bd create "SAP-006: Enhance protocol-spec Section 4 (integration)" --priority 2
Bash: bd create "SAP-006: Add awareness-guide vision synthesis section" --priority 2
# ... etc (20 tasks total)
```

**5. Link Tasks to Epic**
```bash
Bash: bd dep add chora-base-xyz blocks {sap-010-task-1-id}
Bash: bd dep add chora-base-xyz blocks {sap-010-task-2-id}
# ... (repeat for all 20 tasks)
```

**6. Add Traceability Metadata**
```bash
Bash: bd update chora-base-xyz --metadata '{
  "from_vision_wave": 1,
  "roadmap_version": "v1.5.0",
  "vision_document": "vision-chora-base-6-month",
  "target_date": "2026-02-01"
}'

# Update roadmap milestone with epic ID
Edit .chora/memory/knowledge/notes/milestone-v1.5.0.md:
linked_to:
  - vision-chora-base-6-month
  - beads-epic-chora-base-xyz
```

**Example Output** (chora-base v1.5.0 backlog):
- **ROADMAP.md** updated with v1.5.0 milestone
- **Roadmap milestone note** created with vision linkage
- **Beads epic** created: `chora-base-xyz`
- **20 tasks** created (7 SAP-010, 7 SAP-006, 6 SAP-015)
- **Traceability chain**: Vision Wave 1 → Roadmap → Epic → Tasks

---

#### 3.5.5 Quarterly Vision Review

**Context**: End of quarter, review vision Wave 2 based on pilot feedback

**Duration**: 1-2 days (part of next quarterly cycle)

**Steps**:

**1. Query Dogfooding Pilot Results (SAP-027)**
```bash
# Find pilot summaries from last quarter
Bash: grep -l '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md | \
      xargs grep -l '"quarter": "2025-Q4"'

# Read GO/NO-GO decisions
Read .chora/memory/knowledge/notes/{pilot-summary}.md
```

**2. Review Wave 2 Decision Criteria**

For each Wave 2 candidate:
```python
# Check pilot results against criteria
if pilot.time_savings >= 5 and \
   pilot.satisfaction >= 85 and \
   pilot.bugs == 0 and \
   pilot.adoption >= 2:
    decision = "PROMOTE to Wave 1 in next vision"
elif pilot.time_savings < 5 or pilot.satisfaction < 85:
    decision = "DEFER to Wave 3 (needs more evidence)"
else:
    decision = "KEEP in Wave 2 (pilot inconclusive, retry Q+1)"
```

**3. Update Vision Document**
```bash
Read .chora/memory/knowledge/notes/vision-chora-base-6-month.md

Edit vision document:
## Wave 2: Automation & Tooling (Exploratory - 6 months)

**Candidate 1: SAP Generation Automation**
- **Status**: ✅ Validated (Pilot GO - Nov 2025)
- **Evidence**: Dogfooding pilot (SAP-029) achieved 119x time savings (target: ≥5x)
- **Satisfaction**: 100% (target: ≥85%)
- **Bugs**: 0 (target: 0)
- **Adoption**: 2 SAPs generated (target: ≥2)
- **Decision**: **COMMIT to Wave 1 in next vision (v1.6.0)**

**Candidate 2: Multi-Repo Coordination**
- **Status**: ⏳ Pilot in progress (Q1 2026)
- **Preliminary Results**: 3x time savings (below target)
- **Decision**: **DEFER to Wave 3** (needs more evidence, retry Q2 2026)
```

**4. Plan Next Vision Cycle**
```markdown
Next vision cycle (Q1 2026):
- Wave 1: Include SAP Generation (promoted from Wave 2)
- Wave 2: Add new exploratory candidates from Wave 3
- Wave 3: Deprecate Multi-Repo Coordination if no Q2 progress
```

**Example Output** (chora-base Q4 2025 vision review):
- **SAP-029 pilot GO** → Promote to Wave 1 in v1.6.0
- **Multi-Repo pilot inconclusive** → Defer to Wave 3
- **Wave 3 analytics theme** → No evidence upgrade → Deprecate

---

### 3.6 Release Version

**Context**: User requests "Release version 1.2.0"

**Phase**: 7 (Release & Deployment)

#### Step 1: Verify Main Branch Clean

```bash
Bash: git checkout main
Bash: git pull
Bash: git status
Expected: "nothing to commit, working tree clean"
```

#### Step 2: Run Full Test Suite

```bash
Bash: pytest
Expected: All tests pass
```

#### Step 3: Bump Version

```bash
# For patch release (1.1.0 → 1.1.1)
Bash: ./scripts/bump-version.sh patch

# For minor release (1.1.1 → 1.2.0)
Bash: ./scripts/bump-version.sh minor

# For major release (1.2.0 → 2.0.0)
Bash: ./scripts/bump-version.sh major
```

#### Step 4: Update CHANGELOG.md

```
Read CHANGELOG.md
Edit CHANGELOG.md
# Add release notes for this version:
# - Features added
# - Bugs fixed
# - Breaking changes (if MAJOR)
```

#### Step 5: Prepare Release

```bash
Bash: ./scripts/prepare-release.sh
Expected: All checks pass, release ready
```

#### Step 6: Build Distribution

```bash
Bash: ./scripts/build-dist.sh
Expected: dist/ contains .tar.gz and .whl files
```

#### Step 7: Publish to PyPI

**Test publish first** (optional):
```bash
Bash: ./scripts/publish-test.sh
# Verify package at test.pypi.org
```

**Publish to production**:
```bash
Bash: ./scripts/publish-prod.sh
Expected: Package uploaded to PyPI successfully
```

#### Step 8: Create Git Tag and GitHub Release

```bash
Bash: git tag -a v1.2.0 -m "Release v1.2.0"
Bash: git push origin v1.2.0

Bash: gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes "Release notes from CHANGELOG.md"
```

#### Step 9: Verify Deployment

```bash
# Install from PyPI (verify it works)
Bash: pip install <package>==1.2.0

# Run smoke tests on installed package
Bash: ./scripts/smoke-test.sh
Expected: All smoke tests pass
```

---

## 4. Decision Trees for Agents

### 4.1 Feature vs Bug vs Refactor?

```
User request classification:
│
├─ "Add feature X" / "Implement Y" / "Create Z"
│  └─ [3.1 Implement New Feature](#31-implement-new-feature-using-full-lifecycle)
│     Use: DDD → BDD → TDD (full lifecycle)
│
├─ "Fix bug X" / "X doesn't work" / "Error when Y"
│  └─ [3.2 Fix Bug](#32-fix-bug)
│     Use: TDD only (write failing test, fix, verify)
│
├─ "Refactor X" / "Improve Y" / "Simplify Z"
│  └─ [3.3 Refactor Code](#33-refactor-code)
│     Use: TDD with existing tests (ensure GREEN, refactor, verify GREEN)
│
├─ "Plan sprint" / "Plan next iteration"
│  └─ [3.4 Sprint Planning](#34-sprint-planning)
│     Use: sprint-template.md
│
└─ "Release version X.Y.Z" / "Publish to PyPI"
   └─ [3.5 Release Version](#35-release-version)
      Use: bump-version.sh, publish-prod.sh
```

### 4.2 Which Tests to Write?

```
What are you testing?
│
├─ User-facing behavior (API, CLI, UI)?
│  └─ BDD (Gherkin scenarios in .feature files)
│     Example: "User validates configuration"
│
├─ Internal logic or algorithm?
│  └─ TDD (Unit tests in tests/)
│     Example: "Calculate total sums item prices"
│
├─ Integration between systems?
│  └─ Integration tests (tests/integration/)
│     Example: "Database stores and retrieves data"
│
└─ Full user workflow?
   └─ E2E tests (tests/e2e/)
      Example: "User creates account, logs in, creates project"
```

---

## 5. Quality Gate Checklist for Agents

Before creating PR, verify:

```markdown
## Quality Gate Checklist
- [ ] Tests added/updated (new feature or bug fix)
- [ ] All tests pass (pytest)
- [ ] Coverage ≥85% (pytest --cov)
- [ ] Linting passes (ruff check)
- [ ] Type checking passes (mypy)
- [ ] Pre-commit hooks pass (pre-commit run --all-files)
- [ ] Documentation updated (if API changed)
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] BDD scenarios pass (if feature)
```

Run all checks:
```bash
Bash: just pre-merge
```

---

## 6. Common Agent Mistakes

### Mistake 1: Skipping DDD
**Wrong**: Write code first, then docs
**Correct**: Write docs (Explanation + Reference) first, then code

### Mistake 2: Writing Tests After Code
**Wrong**: Implement feature, then "add tests later"
**Correct**: Follow TDD (RED-GREEN-REFACTOR), tests drive design

### Mistake 3: Not Running Tests Between Refactoring
**Wrong**: Make multiple changes, then run tests
**Correct**: Run tests after each small change (keep tests GREEN)

### Mistake 4: Skipping BDD for User-Facing Features
**Wrong**: Only unit tests, no BDD scenarios
**Correct**: Write Gherkin scenarios for user-facing behavior

### Mistake 5: Creating PR Without Pre-Merge Checks
**Wrong**: `git push` without running quality gates
**Correct**: Run `just pre-merge` first, verify all pass

---

## 7. Integration with Other SAPs

### SAP-004 (testing-framework)
- Use pytest for TDD and BDD
- Use pytest-cov for coverage
- Use pytest-bdd for Gherkin scenarios

### SAP-005 (ci-cd-workflows)
- CI runs on PR (test.yml, lint.yml)
- Release workflow on tag (release.yml)

### SAP-006 (quality-gates)
- Pre-commit hooks enforce quality
- Run `pre-commit run --all-files` before PR

### SAP-007 (documentation-framework)
- Use Diataxis for DDD docs
- Use frontmatter schema (type, status, audience)
- Use test extraction for executable How-Tos

### SAP-008 (automation-scripts)
- Use `just test`, `just lint` during development
- Use `just pre-merge` before PR
- Use `./scripts/bump-version.sh` for releases

---

## 8. Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-012 --source /path/to/chora-base
```

This will automatically install:
- SAP-012 (Development Lifecycle)
- SAP-000 (SAP Framework)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `mcp-server` - 10 SAPs for building MCP servers
- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set mcp-server --source /path/to/chora-base
```

### Dependencies

This SAP depends on:
- SAP-000 (SAP Framework)

All dependencies are automatically installed.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/development-lifecycle/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

# Verify workflow documentation exists
ls docs/dev-docs/workflows/
# Should show: DEVELOPMENT_LIFECYCLE.md and related workflow files
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## 9. Related Documents

**Workflow Docs**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md)
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)
- [DDD_WORKFLOW.md](/static-template/dev-docs/workflows/DDD_WORKFLOW.md)
- [BDD_WORKFLOW.md](/static-template/dev-docs/workflows/BDD_WORKFLOW.md)
- [TDD_WORKFLOW.md](/static-template/dev-docs/workflows/TDD_WORKFLOW.md)

**Templates**:
- [sprint-template.md](/static-template/project-docs/sprints/sprint-template.md)
- [release-template.md](/static-template/project-docs/releases/release-template.md)

**Protocol**:
- [protocol-spec.md](protocol-spec.md) - Full lifecycle contracts

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for development-lifecycle SAP
