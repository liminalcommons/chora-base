---
sap_id: SAP-012
version: 1.0.0
status: Draft
last_updated: 2025-10-28
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

### 3.5 Release Version

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

## 8. Related Documents

**Workflow Docs**:
- [DEVELOPMENT_PROCESS.md](../../../../static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md)
- [DEVELOPMENT_LIFECYCLE.md](../../../../static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md)
- [DDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/DDD_WORKFLOW.md)
- [BDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/BDD_WORKFLOW.md)
- [TDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/TDD_WORKFLOW.md)

**Templates**:
- [sprint-template.md](../../../../static-template/project-docs/sprints/sprint-template.md)
- [release-template.md](../../../../static-template/project-docs/releases/release-template.md)

**Protocol**:
- [protocol-spec.md](protocol-spec.md) - Full lifecycle contracts

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for development-lifecycle SAP
