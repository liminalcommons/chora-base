# Protocol Specification: Development Lifecycle

**SAP ID**: SAP-012
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Overview

This protocol defines the **8-phase development lifecycle** for chora-base projects, integrating **DDD → BDD → TDD** methodologies into a unified workflow.

**Core Guarantee**: Following this lifecycle reduces defects by 40-80% (research-backed) while maintaining development velocity.

**Lifecycle**: Vision (months) → Planning (weeks) → Requirements (days) → Development (days-weeks) → Testing (hours-days) → Review (hours-days) → Release (hours) → Monitoring (continuous)

---

## 2. Architecture

### 2.1 Lifecycle Overview

```
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: VISION & STRATEGY (Months)                             │
│ Strategic roadmap, market analysis, ecosystem alignment          │
│ Documents: ROADMAP.md, vision statements                         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: PLANNING & PRIORITIZATION (Weeks)                      │
│ Sprint planning, backlog grooming, stakeholder alignment         │
│ Documents: sprint-template.md, backlog                           │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 3: REQUIREMENTS & DESIGN (DDD) (Days)                     │
│ Documentation Driven Design: Change request → API reference →   │
│ Acceptance criteria                                              │
│ Documents: Diataxis docs, API specs, acceptance criteria        │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 4: DEVELOPMENT (BDD + TDD) (Days-Weeks)                   │
│ BDD: Gherkin scenarios (RED)                                    │
│ TDD: Red-Green-Refactor cycles                                  │
│ Documents: .feature files, tests/, src/                         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 5: TESTING & QUALITY (Hours-Days)                        │
│ Unit → Smoke → Integration → E2E                                │
│ Coverage ≥85%, linting, type checking, security                 │
│ Commands: pytest, ruff, mypy, pre-commit                        │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 6: REVIEW & INTEGRATION (Hours-Days)                     │
│ Code review, docs review, CI/CD pipeline, merge                │
│ Tools: GitHub PR, CI workflows                                  │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 7: RELEASE & DEPLOYMENT (Hours)                          │
│ Version bump, changelog, build, publish PyPI, deploy prod      │
│ Scripts: bump-version.sh, prepare-release.sh, publish-prod.sh  │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 8: MONITORING & FEEDBACK (Continuous)                    │
│ Metrics, user feedback, bug reports, iteration planning        │
│ Documents: PROCESS_METRICS.md, issue tracker                    │
└──────────────────────────────────────────────────────────────────┘
                     │
                     └──→ Back to PHASE 1 or PHASE 2 (continuous improvement)
```

### 2.2 DDD → BDD → TDD Integration

```
DDD (Documentation Driven Design)
  ↓
  Produces: API specification + Acceptance criteria
  ↓
BDD (Behavior Driven Development)
  ↓
  Produces: Executable Gherkin scenarios (.feature files)
  Status: RED (all scenarios fail, feature not implemented)
  ↓
TDD (Test Driven Development)
  ↓
  RED-GREEN-REFACTOR cycles:
    1. Write unit test (RED)
    2. Implement minimal code (GREEN)
    3. Refactor (improve design, tests stay GREEN)
    4. Repeat until all BDD scenarios pass
  ↓
  Produces: Fully tested feature (unit tests + BDD scenarios GREEN)
```

---

## 3. Phase Contracts

### 3.1 Phase 1: Vision & Strategy

**Time Scale**: Months (quarterly review)
**Frequency**: Quarterly
**Participants**: Leadership, product, engineering leads

#### Inputs
- Market trends
- User feedback
- Ecosystem evolution
- Competitive analysis

#### Activities
1. Define product vision and mission
2. Identify target users and use cases
3. Analyze ecosystem and competition
4. Establish multi-year goals
5. Define success metrics

#### Outputs
- **ROADMAP.md** - Strategic roadmap (quarters to years)
- **Vision statements** - Product vision, mission, goals
- **Release plan** - Major version timeline (v2.0, v3.0)

#### Quality Gates
- ✅ Vision statement reviewed by stakeholders
- ✅ Roadmap aligned with ecosystem trends
- ✅ Success metrics defined and measurable

#### Example Vision Statement
```markdown
**Vision:** Transform {project} from prototype to production-grade
{capability} with comprehensive documentation pipeline,
{feature 1}, and {feature 2}.

**Current Status:** v1.0.0 released (Oct 2025)
**Next Milestone:** v2.0.0 (Major Feature) - Q1 2026
```

---

### 3.2 Phase 2: Planning & Prioritization

**Time Scale**: Weeks (sprint cycle, typically 2 weeks)
**Frequency**: Every sprint (biweekly)
**Participants**: Product, engineering leads, team

#### Inputs
- ROADMAP.md (from Phase 1)
- Backlog items
- Previous sprint velocity
- Bug reports and user feedback

#### Activities
1. Sprint planning meeting (2 hours max with templates)
2. Backlog grooming and prioritization
3. Capacity planning (velocity-based)
4. Risk identification
5. Dependency mapping

#### Outputs
- **sprints/sprint-{NN}.md** - Sprint plan (from template)
- **Committed items** - Stories, bugs, tech debt
- **Sprint goals** - Clear, measurable objectives

#### Quality Gates
- ✅ Sprint capacity matches team velocity (±20%)
- ✅ Dependencies identified and resolved
- ✅ Sprint goals SMART (Specific, Measurable, Achievable, Relevant, Time-bound)

#### Template: Sprint Planning
**Location**: `project-docs/sprints/sprint-template.md`

**Key Sections**:
- Sprint metadata (number, dates, participants)
- Sprint goals (3-5 clear objectives)
- Committed items (user stories, bugs, tech debt)
- Stretch goals (optional, if capacity allows)
- Risks and dependencies
- Definition of Done

---

### 3.3 Phase 3: Requirements & Design (DDD)

**Time Scale**: Days (2-5 days for medium feature)
**Frequency**: Per feature
**Participants**: Engineers, product, designers

#### Inputs
- Sprint plan (from Phase 2)
- User story or feature request
- API constraints (existing architecture)

#### Activities (DDD Workflow)
1. **Write change request** (Explanation + How-To, Diataxis format)
2. **Design API** (Reference documentation, function signatures)
3. **Extract acceptance criteria** (Given-When-Then format)
4. **Get stakeholder approval** (review meeting)

#### Outputs
- **Explanation doc** - Why this feature? Problem statement, solution approach
- **Reference doc** - API specification (functions, parameters, return types)
- **Acceptance criteria** - Given-When-Then scenarios (input for BDD)

#### Quality Gates
- ✅ API design reviewed by technical lead
- ✅ Acceptance criteria complete (cover happy path + edge cases)
- ✅ Documentation passes frontmatter validation (SAP-007)
- ✅ Stakeholder approval obtained

#### DDD Workflow Example

**Step 1: Write Explanation Document** (Why?)
```markdown
---
title: Add Configuration Validation Feature
type: explanation
status: draft
audience: developers
last_updated: 2025-10-28
---

# Configuration Validation Feature

## Problem
Users frequently provide invalid configuration files, leading to
cryptic runtime errors.

## Solution
Add a `validate_config()` function that checks configuration schemas
before application startup, providing clear error messages.

## Acceptance Criteria
1. Given valid config, when validating, then return success
2. Given invalid config, when validating, then return detailed errors
3. Given missing required field, when validating, then specify field name
```

**Step 2: Write Reference Documentation** (What?)
```markdown
---
title: Configuration Validation API
type: reference
status: draft
audience: developers
last_updated: 2025-10-28
---

# Configuration Validation API

## `validate_config(config_path: str) -> ValidationResult`

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- `ValidationResult`: Object with `is_valid` (bool) and `errors` (list)

**Raises:**
- `FileNotFoundError`: If config_path doesn't exist

**Example:**
```python
result = validate_config("config.yaml")
if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
```
```

---

### 3.4 Phase 4: Development (BDD + TDD)

**Time Scale**: Days-Weeks (1-14 days depending on complexity)
**Frequency**: Per feature
**Participants**: Engineers, AI assistants

#### Part A: BDD (Behavior Driven Development)

**Time**: 1-3 hours
**Input**: Acceptance criteria (from DDD Phase 3)

**Activities**:
1. Write Gherkin scenarios (`.feature` files)
2. Implement step definitions (`steps/`)
3. Run BDD tests → Verify RED (all fail)

**Output**: Executable specifications (failing tests)

**BDD Example**:
```gherkin
# features/config_validation.feature
Feature: Configuration Validation
  As a user
  I want to validate my configuration file
  So that I catch errors before runtime

  Scenario: Valid configuration
    Given a valid configuration file "config.yaml"
    When I validate the configuration
    Then validation succeeds
    And no errors are reported

  Scenario: Missing required field
    Given a configuration file "config.yaml" missing "api_key"
    When I validate the configuration
    Then validation fails
    And error message includes "api_key is required"
```

#### Part B: TDD (Test Driven Development)

**Time**: 4 hours - 2 weeks (depending on complexity)
**Input**: API spec (DDD) + BDD scenarios

**Activities** (RED-GREEN-REFACTOR loop):
1. **RED**: Write unit test (fails)
2. **GREEN**: Implement minimal code (test passes)
3. **REFACTOR**: Improve design (tests stay green)
4. **Repeat** until all BDD scenarios pass

**Output**: Feature implemented with ≥85% coverage

**TDD Example (Cycle 1)**:

**RED** - Write failing test:
```python
# tests/test_config_validation.py
def test_validate_config_with_valid_file():
    """Test validation succeeds with valid config."""
    result = validate_config("tests/fixtures/valid_config.yaml")
    assert result.is_valid is True
    assert result.errors == []
```

**GREEN** - Implement minimal code:
```python
# src/config_validation.py
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]

def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file."""
    # Minimal implementation to pass test
    return ValidationResult(is_valid=True, errors=[])
```

**REFACTOR** - Improve design (add actual validation logic, tests stay green)

#### Quality Gates (Phase 4)
- ✅ All BDD scenarios pass (GREEN)
- ✅ All unit tests pass (GREEN)
- ✅ Coverage ≥85% (pytest --cov)
- ✅ No type errors (mypy)
- ✅ Linting passes (ruff)

---

### 3.5 Phase 5: Testing & Quality

**Time Scale**: Hours-Days (2 hours - 2 days)
**Frequency**: Per PR
**Participants**: Engineers, QA, CI/CD

#### Test Pyramid
```
        E2E (10%)
       /        \
    Integration (20%)
   /                \
  Smoke (10%)
 /                    \
Unit Tests (60%)
```

#### Activities
1. **Unit tests** - Already done in TDD (Phase 4)
2. **Smoke tests** - Quick validation (`./scripts/smoke-test.sh`, ~10 sec)
3. **Integration tests** - System interactions (`pytest tests/integration/`)
4. **E2E tests** - Full user workflows (if applicable)
5. **Coverage check** - `pytest --cov` (≥85% required)
6. **Linting** - `ruff check`
7. **Type checking** - `mypy src/ tests/`
8. **Security scan** - CodeQL (in CI)

#### Outputs
- Test results (pass/fail)
- Coverage report (HTML + terminal)
- Linting report
- Type checking report

#### Quality Gates
- ✅ All tests pass (unit, smoke, integration, E2E)
- ✅ Coverage ≥85%
- ✅ No linting errors
- ✅ No type errors
- ✅ No security vulnerabilities (CodeQL)

#### Commands
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run smoke tests (quick validation)
./scripts/smoke-test.sh

# Run integration tests only
pytest tests/integration/

# Pre-merge validation (runs all checks)
just pre-merge
```

---

### 3.6 Phase 6: Review & Integration

**Time Scale**: Hours-Days (4 hours - 3 days)
**Frequency**: Per PR
**Participants**: Reviewers, maintainers

#### Activities
1. **Code review** - Reviewer examines changes
2. **Documentation review** - Verify docs updated
3. **CI/CD pipeline** - All workflows pass (test.yml, lint.yml, security.yml)
4. **Address feedback** - Iterate on reviews
5. **Merge to main** - Squash and merge

#### Outputs
- Approved PR
- Merged code (main branch)
- Updated documentation

#### Quality Gates
- ✅ At least 1 approval from maintainer
- ✅ All CI workflows pass (test, lint, security)
- ✅ Documentation updated (if API changed)
- ✅ CHANGELOG.md updated (if user-facing change)
- ✅ No merge conflicts

#### Pull Request Checklist
```markdown
## PR Checklist
- [ ] Tests added/updated (coverage ≥85%)
- [ ] Documentation updated (API changes)
- [ ] CHANGELOG.md updated (user-facing changes)
- [ ] All CI workflows pass
- [ ] Code reviewed and approved
- [ ] No merge conflicts
```

---

### 3.7 Phase 7: Release & Deployment

**Time Scale**: Hours (1-4 hours)
**Frequency**: Per version (weekly to monthly)
**Participants**: Release manager, DevOps

#### Activities
1. **Version bump** - `./scripts/bump-version.sh <patch|minor|major>`
2. **Update CHANGELOG.md** - Add release notes
3. **Prepare release** - `./scripts/prepare-release.sh`
4. **Build distribution** - `./scripts/build-dist.sh`
5. **Publish to PyPI** - `./scripts/publish-prod.sh` (or publish-test.sh for testing)
6. **Create GitHub release** - Tag + release notes
7. **Deploy to production** - Infrastructure deployment (if applicable)

#### Outputs
- New version tag (e.g., v1.2.0)
- PyPI package published
- GitHub release created
- Production deployment (if applicable)

#### Quality Gates
- ✅ All tests pass on main branch
- ✅ Version number follows semver (MAJOR.MINOR.PATCH)
- ✅ CHANGELOG.md complete
- ✅ Release notes reviewed
- ✅ PyPI publish succeeds
- ✅ Smoke tests pass on published package

#### Semantic Versioning
- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features (backward compatible)
- **PATCH** (0.0.x): Bug fixes (backward compatible)

#### Commands
```bash
# Bump version (updates pyproject.toml, __init__.py)
./scripts/bump-version.sh patch  # 1.0.0 → 1.0.1
./scripts/bump-version.sh minor  # 1.0.1 → 1.1.0
./scripts/bump-version.sh major  # 1.1.0 → 2.0.0

# Prepare release (run tests, update CHANGELOG)
./scripts/prepare-release.sh patch

# Build distribution packages
./scripts/build-dist.sh

# Publish to test PyPI (verify before prod)
./scripts/publish-test.sh

# Publish to production PyPI
./scripts/publish-prod.sh
```

---

### 3.8 Phase 8: Monitoring & Feedback

**Time Scale**: Continuous
**Frequency**: Always on
**Participants**: All stakeholders

#### Activities
1. **Collect metrics** - Process metrics, quality metrics, velocity
2. **User feedback** - Issues, feature requests, surveys
3. **Bug triage** - Prioritize and schedule fixes
4. **Retrospectives** - Sprint retrospectives, release retrospectives
5. **Iterate** - Feed learnings back to Phase 1 or Phase 2

#### Outputs
- **PROCESS_METRICS.md** - Updated with actuals
- **Issue tracker** - Triaged bugs and feature requests
- **Retrospective notes** - Sprint retrospective, lessons learned

#### Metrics to Track

**Quality Metrics** (from PROCESS_METRICS.md):
- Defects per release: Target <3
- Test coverage: Target ≥85%
- Code review time: Target <24 hours
- CI/CD success rate: Target ≥95%

**Velocity Metrics**:
- Story points completed per sprint
- Sprint velocity trend (last 6 sprints)
- Planned vs delivered ratio: Target ≥70%

**Process Adherence Metrics**:
- DDD adoption: % features with docs-first approach
- BDD adoption: % features with Gherkin scenarios
- TDD adoption: % code written test-first

#### Feedback Loop
```
Phase 8 Monitoring
      ↓
Identify issue or opportunity
      ↓
   ┌─────────────────┐
   │ Minor fix/bug?  │ → Phase 2 (add to sprint backlog)
   │ Major feature?  │ → Phase 1 (update roadmap)
   └─────────────────┘
```

---

## 4. Decision Trees

### 4.1 Which Methodology to Use?

```
What are you building?
│
├─ New feature or API?
│  │
│  ├─ Step 1: DDD (Phase 3) - Write docs first
│  │   └─ Design API, extract acceptance criteria
│  │
│  ├─ Step 2: BDD (Phase 4) - Write scenarios
│  │   └─ Convert acceptance criteria to Gherkin
│  │
│  └─ Step 3: TDD (Phase 4) - Implement
│      └─ RED-GREEN-REFACTOR until BDD scenarios pass
│
├─ Bug fix?
│  │
│  ├─ Step 1: Write failing test that reproduces bug
│  │   └─ Use TDD (unit test) or BDD (if user-facing)
│  │
│  ├─ Step 2: Fix bug (make test pass)
│  │
│  └─ Step 3: Verify fix doesn't break anything
│      └─ Run full test suite
│
├─ Refactoring existing code?
│  │
│  ├─ Step 1: Ensure tests exist (write if missing)
│  │
│  ├─ Step 2: Refactor
│  │   └─ Tests must stay GREEN throughout
│  │
│  └─ Step 3: Verify behavior unchanged
│      └─ Run full test suite
│
└─ Experimental prototype?
   └─ Skip all three (prototype first, then wrap with tests)
```

### 4.2 Time Investment by Feature Complexity

| Phase | Simple Feature | Medium Feature | Complex Feature |
|-------|----------------|----------------|-----------------|
| **DDD (Phase 3)** | 2-4 hours | 4-8 hours | 1-2 days |
| **BDD (Phase 4)** | 1-2 hours | 2-3 hours | 4-6 hours |
| **TDD (Phase 4)** | 4-8 hours | 1-2 days | 3-5 days |
| **Testing (Phase 5)** | 1-2 hours | 2-4 hours | 4-8 hours |
| **Review (Phase 6)** | 2-4 hours | 4-8 hours | 1-2 days |
| **Total** | 1 day | 2-3 days | 1-2 weeks |

**ROI**: 40-60% reduction in rework + bugs + maintenance time

---

## 5. Templates

### 5.1 Sprint Template

**Location**: `project-docs/sprints/sprint-template.md`

**Usage**: Copy template at sprint start, fill in details

**Sections**:
1. Sprint metadata (number, dates, participants)
2. Sprint goals (3-5 SMART objectives)
3. Committed items (stories, bugs, tech debt with story points)
4. Stretch goals (optional items if capacity allows)
5. Risks and dependencies
6. Definition of Done
7. Daily standup notes
8. Sprint retrospective (completed at sprint end)

### 5.2 Release Template

**Location**: `project-docs/releases/release-template.md`

**Usage**: Copy template before release, fill in details

**Sections**:
1. Release metadata (version, date, release manager)
2. Release goals (what's included in this release)
3. Features (new functionality)
4. Bug fixes (resolved issues)
5. Breaking changes (if any, MAJOR version only)
6. Upgrade guide (if breaking changes)
7. Known issues (unresolved bugs)
8. Release checklist (pre-release validation)

### 5.3 Process Metrics Template

**Location**: `project-docs/metrics/PROCESS_METRICS.md`

**Usage**: Update monthly, track trends

**Metrics Categories**:
1. **Quality Metrics**: Defects per release, test coverage, code review time
2. **Velocity Metrics**: Story points per sprint, velocity trend, planned vs delivered
3. **Process Adherence**: DDD/BDD/TDD adoption rates
4. **CI/CD Metrics**: Pipeline success rate, build time, deployment frequency

---

## 6. Anti-Patterns

**Location**: `dev-docs/ANTI_PATTERNS.md` (1,309 lines)

**Key Anti-Patterns**:

### 6.1 Skipping DDD
**Anti-Pattern**: Writing code before documenting API
**Impact**: Unclear requirements, frequent rework, poor API design
**Fix**: Always write API reference docs (Phase 3) before coding

### 6.2 Writing Tests After Code
**Anti-Pattern**: Implement feature, then "add tests later"
**Impact**: Low coverage, tests confirm implementation (not requirements)
**Fix**: Follow TDD (RED-GREEN-REFACTOR), tests drive design

### 6.3 Ignoring BDD Scenarios
**Anti-Pattern**: Skip Gherkin scenarios, rely only on unit tests
**Impact**: Disconnect between user requirements and implementation
**Fix**: Write BDD scenarios for user-facing behavior (Phase 4)

### 6.4 Skipping Code Review
**Anti-Pattern**: Merge directly to main without review
**Impact**: Bugs slip through, knowledge not shared, inconsistent code quality
**Fix**: Always require PR + 1 approval (Phase 6)

### 6.5 No Sprint Retrospective
**Anti-Pattern**: Skip retrospectives to "save time"
**Impact**: Same mistakes repeated, no process improvement
**Fix**: 30-min retrospective at sprint end, document learnings

---

## 7. Integration with Other SAPs

### 7.1 SAP-004 (testing-framework)
- **TDD (Phase 4)** uses pytest infrastructure
- **Coverage enforcement** (≥85%) from SAP-004
- **Test patterns** (unit, parametrized, async, mock) from SAP-004

### 7.2 SAP-005 (ci-cd-workflows)
- **Phase 5 (Testing)** executes CI workflows (test.yml, lint.yml)
- **Phase 6 (Review)** requires CI pass (quality gate)
- **Phase 7 (Release)** uses release.yml workflow

### 7.3 SAP-006 (quality-gates)
- **Phase 4 (Development)** enforced by pre-commit hooks
- **Phase 5 (Testing)** includes lint + type check from SAP-006
- **Phase 6 (Review)** verifies all hooks passed

### 7.4 SAP-007 (documentation-framework)
- **DDD (Phase 3)** uses Diataxis structure (Explanation, Reference)
- **Frontmatter validation** ensures docs follow standard
- **Executable How-Tos** generate tests for Phase 4

### 7.5 SAP-008 (automation-scripts)
- **Phase 4 (Development)** uses `just test`, `just lint`
- **Phase 5 (Testing)** uses `./scripts/pre-merge.sh`
- **Phase 7 (Release)** uses `./scripts/bump-version.sh`, `./scripts/publish-prod.sh`

### 7.6 SAP-013 (metrics-tracking)
- **Phase 8 (Monitoring)** uses ClaudeROICalculator
- **Process metrics** tracked in PROCESS_METRICS.md
- **Sprint velocity** tracked per sprint

---

## 8. Research Evidence

### 8.1 DDD → BDD → TDD Effectiveness

**Source**: "Test Driven Development: By Example" (Kent Beck, 2002)
- **40-80% defect reduction** when following TDD
- **Improved design** due to testability-first approach
- **Living documentation** (tests as specs)

**Source**: "The Cucumber Book" (Matt Wynne, Aslak Hellesøy, 2017)
- **BDD scenarios reduce ambiguity** by 60%
- **Stakeholder alignment** improved (Given-When-Then)
- **Executable specifications** prevent regression

**Source**: "Docs as Code" (Anne Gentle, 2017)
- **Documentation Driven Design** reduces API churn by 50%
- **Docs-first** approach catches design issues early
- **Test extraction** from docs ensures synchronization

---

## 9. Quality Gates Summary

| Phase | Quality Gates | Tools |
|-------|---------------|-------|
| **Phase 1: Vision** | Vision reviewed, roadmap aligned, metrics defined | Manual review |
| **Phase 2: Planning** | Capacity matches velocity, dependencies resolved, SMART goals | sprint-template.md |
| **Phase 3: Requirements (DDD)** | API reviewed, acceptance criteria complete, docs validated | Diataxis, frontmatter validation |
| **Phase 4: Development (BDD+TDD)** | BDD scenarios pass, unit tests pass, coverage ≥85%, no type errors | pytest, mypy, ruff |
| **Phase 5: Testing** | All tests pass, coverage ≥85%, no linting/type errors, no vulnerabilities | pytest, ruff, mypy, CodeQL |
| **Phase 6: Review** | 1+ approval, CI pass, docs updated, CHANGELOG updated | GitHub PR, CI workflows |
| **Phase 7: Release** | Tests pass on main, semver followed, CHANGELOG complete, PyPI publish succeeds | bump-version.sh, publish-prod.sh |
| **Phase 8: Monitoring** | Metrics tracked, feedback collected, retrospectives documented | PROCESS_METRICS.md |

---

## 10. Related Documents

**Workflow Documentation**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - 8-phase lifecycle overview
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD→BDD→TDD integration
- [DDD_WORKFLOW.md](/static-template/dev-docs/workflows/DDD_WORKFLOW.md) - Documentation Driven Design
- [BDD_WORKFLOW.md](/static-template/dev-docs/workflows/BDD_WORKFLOW.md) - Behavior Driven Development
- [TDD_WORKFLOW.md](/static-template/dev-docs/workflows/TDD_WORKFLOW.md) - Test Driven Development
- [ANTI_PATTERNS.md](/static-template/dev-docs/ANTI_PATTERNS.md) - Common mistakes

**Templates**:
- [sprint-template.md](/static-template/project-docs/sprints/sprint-template.md) - Sprint planning template
- [release-template.md](/static-template/project-docs/releases/release-template.md) - Release planning template
- [PROCESS_METRICS.md](/static-template/project-docs/metrics/PROCESS_METRICS.md) - Process metrics dashboard

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - pytest, coverage, fixtures
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - GitHub Actions workflows
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit hooks
- [SAP-007: documentation-framework](../documentation-framework/) - Diataxis structure
- [SAP-008: automation-scripts](../automation-scripts/) - Scripts and justfile

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for development-lifecycle SAP
