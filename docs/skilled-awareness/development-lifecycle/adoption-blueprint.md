---
sap_id: SAP-012
version: 1.5.0
status: Active
last_updated: 2025-11-06
type: how-to
audience: developers, ai-agents
---

# Adoption Blueprint: Development Lifecycle

**SAP ID**: SAP-012
**For**: Projects adopting the 8-phase lifecycle
**Purpose**: Step-by-step guide to implement DDD→BDD→TDD workflow with Light+ planning

---

## 1. Overview

This blueprint helps projects adopt the **8-phase development lifecycle** with integrated **DDD → BDD → TDD** workflow.

**Adoption Levels**:
- **Level 1** (Basic): Phases 4-6 only (Development → Testing → Review)
- **Level 2** (Standard): Phases 2-6 (Planning → Development → Testing → Review)
- **Level 3** (Full): All 8 phases (Vision → Monitoring)

**Recommended**: Start with Level 1, graduate to Level 2 after 2-3 sprints, then Level 3 after 1-2 releases.

---

## 2. Installing the SAP

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-012 --source /path/to/chora-base
```

**What This Installs**:
- development-lifecycle capability documentation (5 artifacts)
- Workflow documentation in docs/dev-docs/workflows/
- DDD → BDD → TDD templates and guides

### Part of Sets

This SAP is included in:
- full
- mcp-server

To install a complete set:
```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/development-lifecycle/*.md
ls docs/dev-docs/workflows/
```

---

## 3. Prerequisites

### Required Infrastructure

From **chora-base** generated projects:
- ✅ Testing framework (SAP-004): pytest, pytest-cov, pytest-bdd
- ✅ CI/CD workflows (SAP-005): test.yml, lint.yml, release.yml
- ✅ Quality gates (SAP-006): pre-commit hooks, ruff, mypy
- ✅ Automation scripts (SAP-008): justfile, release scripts

### Optional Infrastructure

- ✅ Documentation framework (SAP-007): Diataxis structure for DDD
- ✅ Metrics tracking (SAP-013): ClaudeROICalculator for ROI

### Team Requirements

- **Commitment**: 2-week sprint cycles (Level 2+)
- **Training**: 2-hour onboarding on DDD→BDD→TDD (all team members)
- **Process adherence**: ≥70% (measured in retrospectives)

---

## 3. Adoption Paths

### 3.1 Level 1: Basic (Development Focus)

**What You Get**: DDD→BDD→TDD workflow only
**Time to Adopt**: 1 sprint (2 weeks)
**Best For**: Small teams, single maintainer, early-stage projects

#### Phases Adopted
- ✅ Phase 4: Development (BDD + TDD)
- ✅ Phase 5: Testing & Quality
- ✅ Phase 6: Review & Integration

#### Setup Steps

**1. Install BDD tooling**:
```bash
# Add pytest-bdd to pyproject.toml
pip install pytest-bdd
```

**2. Create features/ directory**:
```bash
mkdir -p features/steps
```

**3. Read workflow docs**:
- Read `dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md` (753 lines)
- Read `dev-docs/workflows/BDD_WORKFLOW.md` (1,148 lines)
- Read `dev-docs/workflows/TDD_WORKFLOW.md` (1,187 lines)

**4. Try one feature with full DDD→BDD→TDD**:
- Write docs first (Explanation + Reference) - DDD
- Write Gherkin scenarios (.feature file) - BDD
- Write tests and code (RED-GREEN-REFACTOR) - TDD

**5. Measure impact** (after 2-3 features):
- Compare defect rate: Before vs After
- Compare rework time: Before vs After
- Target: 40-60% reduction in defects + rework

---

### 3.2 Level 2: Standard (+ Planning)

**What You Get**: Sprint planning + DDD→BDD→TDD workflow
**Time to Adopt**: 2 sprints (4 weeks)
**Best For**: Small-medium teams, regular release cadence

#### Additional Phases
- ✅ Phase 2: Planning & Prioritization

#### Setup Steps

**1. Complete Level 1** (Development focus)

**2. Create sprint structure**:
```bash
mkdir -p project-docs/sprints
cp docs/reference/skilled-awareness/development-lifecycle/templates/sprint-template.md \
   project-docs/sprints/sprint-template.md
```

**3. Plan first sprint**:
```bash
cp project-docs/sprints/sprint-template.md \
   project-docs/sprints/sprint-01.md
# Fill in sprint goals, committed items, capacity
```

**4. Run sprint** (2 weeks):
- Daily standup (15 min): What I did, what I'll do, blockers
- Mid-sprint check-in: Adjust if velocity off
- Sprint review: Demo completed work
- Sprint retrospective: What went well, what to improve

**5. Track velocity**:
- Committed story points vs delivered
- Target: ≥70% planned vs delivered ratio

**6. Iterate**: Plan sprint 02 using sprint-01 velocity

---

### 3.3 Level 3: Full (All 8 Phases)

**What You Get**: Vision → Monitoring (complete lifecycle)
**Time to Adopt**: 3-6 months
**Best For**: Medium-large teams, multi-year roadmaps, product focus

#### Additional Phases
- ✅ Phase 1: Vision & Strategy
- ✅ Phase 7: Release & Deployment
- ✅ Phase 8: Monitoring & Feedback

#### Setup Steps

**1. Complete Level 2** (Planning + Development)

**2. Create roadmap** (Phase 1):
```markdown
File: ROADMAP.md

# Project Roadmap

## Vision
[Product vision statement - where are we going?]

## Current Status
- Version: v1.2.0
- Status: Production
- Users: 100+ active

## Q1 2026 Goals
- [ ] Feature X (v1.3.0)
- [ ] Feature Y (v1.4.0)
- [ ] Ecosystem integration with Z

## Q2 2026 Goals
- [ ] Major refactor (v2.0.0)
- [ ] Performance improvements

## Success Metrics
- Defects per release: <3
- User satisfaction: ≥4.5/5
- Adoption rate: +20% per quarter
```

**3. Create release structure** (Phase 7):
```bash
mkdir -p project-docs/releases
cp docs/reference/skilled-awareness/development-lifecycle/templates/release-template.md \
   project-docs/releases/release-template.md
```

**4. Create metrics dashboard** (Phase 8):
```bash
mkdir -p project-docs/metrics
cp docs/reference/skilled-awareness/development-lifecycle/templates/PROCESS_METRICS.md \
   project-docs/metrics/PROCESS_METRICS.md
```

**5. Track process metrics**:
- Quality: Defects per release, test coverage, code review time
- Velocity: Story points per sprint, velocity trend
- Process adherence: DDD/BDD/TDD adoption rates

**6. Quarterly review**: Update ROADMAP.md, retrospective on process

---

## 4. Quick Start Guides

### 4.1 Quick Start: Your First DDD→BDD→TDD Feature

**Time**: 4-8 hours
**Goal**: Experience full lifecycle on simple feature

#### Step 1: Choose Simple Feature
- Example: "Add configuration validation"
- Complexity: 3-5 story points
- User-facing: Yes (good for BDD)

#### Step 2: DDD - Write Docs First (1-2 hours)

**Write Explanation** (Why?):
```markdown
File: user-docs/explanation/config-validation.md

---
title: Configuration Validation
type: explanation
status: draft
audience: developers
last_updated: 2025-10-28
---

# Configuration Validation

## Problem
Users provide invalid config files, leading to runtime errors.

## Solution
Validate config schema before startup, provide clear error messages.

## Acceptance Criteria
1. Given valid config, when validating, then return success
2. Given invalid config, when validating, then return errors
3. Given missing field, when validating, then specify field name
```

**Write Reference** (What?):
```markdown
File: user-docs/reference/config-validation-api.md

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
- `config_path` (str): Path to config file

**Returns:**
- `ValidationResult`: Object with `is_valid`, `errors`

**Example:**
```python
result = validate_config("config.yaml")
if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
```
```

#### Step 3: BDD - Write Scenarios (1 hour)

```gherkin
File: features/config_validation.feature

Feature: Configuration Validation
  Scenario: Valid configuration
    Given a valid configuration file
    When I validate the configuration
    Then validation succeeds

  Scenario: Invalid configuration
    Given an invalid configuration file
    When I validate the configuration
    Then validation fails
    And error messages are clear
```

Run BDD tests (verify RED):
```bash
pytest features/config_validation.feature
# Expected: All scenarios fail (not implemented)
```

#### Step 4: TDD - Implement (2-4 hours)

**RED-GREEN-REFACTOR cycles**:
```python
# Test 1 (RED)
def test_validate_config_with_valid_file():
    result = validate_config("tests/fixtures/valid.yaml")
    assert result.is_valid is True

# Implement minimal code (GREEN)
def validate_config(config_path):
    return ValidationResult(is_valid=True, errors=[])

# Refactor (improve design, tests stay GREEN)

# Test 2 (RED)
def test_validate_config_with_invalid_file():
    result = validate_config("tests/fixtures/invalid.yaml")
    assert result.is_valid is False
    assert len(result.errors) > 0

# Implement logic (GREEN)
# ... add validation logic

# Refactor
# ... improve error messages
```

Run BDD scenarios (verify all GREEN):
```bash
pytest features/config_validation.feature
# Expected: All scenarios pass
```

#### Step 5: Measure Impact

**Before DDD→BDD→TDD**:
- Time to implement: 6-8 hours
- Bugs found in code review: 2-3
- Rework time: 2-3 hours

**After DDD→BDD→TDD**:
- Time to implement: 4-6 hours (docs + scenarios = design clarity)
- Bugs found in code review: 0-1
- Rework time: 0-1 hours

**ROI**: 40-60% reduction in total time (implementation + rework)

---

### 4.2 Quick Start: Your First Sprint Plan

**Time**: 1-2 hours
**Goal**: Plan 2-week sprint with team

#### Step 1: Prepare

**1. Review backlog**:
- List all pending items (features, bugs, tech debt)
- Prioritize by value and dependencies

**2. Check previous sprint velocity** (if applicable):
- Story points committed vs delivered
- Use as baseline for capacity

**3. Identify blockers**:
- Dependencies on external teams
- Infrastructure requirements

#### Step 2: Sprint Planning Meeting

**Agenda** (2 hours max):
1. **Review sprint goals** (15 min)
   - What are top 3 priorities?
2. **Select items** (60 min)
   - Pull from backlog, estimate story points
   - Commit to items within capacity
3. **Identify risks** (15 min)
   - Dependencies, blockers, unknowns
4. **Define Definition of Done** (15 min)
   - What "done" means for this sprint
5. **Assign owners** (15 min)
   - Who owns each item?

#### Step 3: Fill Sprint Template

```markdown
File: project-docs/sprints/sprint-01.md

# Sprint 01 Plan

**Duration**: 2025-11-01 to 2025-11-14 (2 weeks)

## Sprint Goals
1. Launch configuration validation feature
2. Fix 3 high-priority bugs
3. Reduce test suite duration by 30%

## Committed Items

| Item | Type | Points | Owner | Status |
|------|------|--------|-------|--------|
| Config validation | Feature | 5 | Alice | Not Started |
| Bug: Timeout issue | Bug | 2 | Bob | Not Started |
| Bug: Parsing error | Bug | 2 | Alice | Not Started |
| Bug: Memory leak | Bug | 3 | Bob | Not Started |
| Optimize tests | Tech Debt | 3 | Alice | Not Started |

**Total Committed**: 15 story points

## Capacity
- Team size: 2 developers
- Availability: 100% (no PTO)
- Capacity: 15 story points (based on previous sprint)

## Risks
- Config validation blocked on schema library decision

## Definition of Done
- [ ] All tests pass (pytest)
- [ ] Coverage ≥85%
- [ ] Code reviewed and approved
- [ ] Docs updated
- [ ] Deployed to staging
```

#### Step 4: Run Sprint

**Daily Standup** (15 min):
- What did I complete yesterday?
- What will I work on today?
- Any blockers?

**Mid-Sprint Check** (Day 5):
- On track? Adjust if needed

**Sprint Review** (Day 14):
- Demo completed work to stakeholders

**Sprint Retrospective** (Day 14):
- What went well?
- What could improve?
- Action items for next sprint

---

## 5. Troubleshooting

### Problem 1: "DDD takes too long"

**Symptom**: Writing docs first feels slow

**Root Cause**: Unfamiliarity with Diataxis, perfectionism

**Fix**:
1. Use templates (Explanation template, Reference template)
2. Set time box: 2 hours max for simple feature
3. Focus on acceptance criteria (not perfect prose)
4. Remember: DDD saves time by catching design issues early

**ROI**: 2 hours DDD upfront saves 4-6 hours rework later

---

### Problem 2: "BDD scenarios too verbose"

**Symptom**: .feature files have 100+ lines

**Root Cause**: Over-specification, testing internal logic

**Fix**:
1. BDD is for **user-facing behavior** only
2. Use unit tests (TDD) for internal logic
3. Keep scenarios focused: 1 scenario = 1 behavior
4. Avoid implementation details in Given-When-Then

**Example**:
```gherkin
# ❌ Too verbose (implementation details)
Scenario: User validates config
  Given a config file with schema version 2.0
  And the validator is initialized with strict mode
  And the parser is set to YAML format
  When the user runs validate_config with path "config.yaml"
  Then the ValidationResult object has is_valid = True
  And the errors list has length 0

# ✅ Concise (user behavior)
Scenario: Valid configuration
  Given a valid configuration file
  When I validate the configuration
  Then validation succeeds
```

---

### Problem 3: "Team resists process change"

**Symptom**: Developers skip DDD, write code first

**Root Cause**: Perceived overhead, lack of ROI visibility

**Fix**:
1. **Start small**: 1 feature with DDD→BDD→TDD (demonstrate ROI)
2. **Measure impact**: Track defects before/after, show 40-80% reduction
3. **Pair programming**: Experienced developer pairs with skeptic
4. **Celebrate wins**: Recognize when DDD catches design issues early

**Talking Points**:
- "Research shows 40-80% defect reduction with TDD"
- "Docs-first prevents rework (we spent 6 hours rewriting X last sprint)"
- "BDD scenarios are living documentation (no more stale docs)"

---

### Problem 4: "Sprints feel like too much overhead"

**Symptom**: Planning meetings run long, bureaucracy

**Root Cause**: Over-planning, lack of templates

**Fix**:
1. Use **sprint-template.md** (reduces planning from 4 hours to 2 hours)
2. Time-box meetings: Planning (2h max), standup (15min max), retro (30min max)
3. Start with Level 1 (no sprints), add sprints when team grows
4. Focus on outcomes, not process compliance

**When to Skip Sprints**:
- Solo developer: Skip sprints, use ad-hoc planning
- 2-3 developers: Lightweight sprints (1-page plan)
- 4+ developers: Full sprint process (template-based)

---

## 6. Success Metrics

### Quality Metrics

| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| Defects per release | Varies | <3 | Count bugs in issue tracker |
| Test coverage | Varies | ≥85% | `pytest --cov` |
| Code review time | Varies | <24 hours | PR open → merge time |
| Rework rate | Varies | <20% | Rework time / total dev time |

### Velocity Metrics

| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| Sprint velocity | Establish in Sprint 1-2 | ±20% variance | Story points delivered |
| Planned vs delivered | Varies | ≥70% | Committed points / delivered points |
| Lead time | Varies | <5 days | Issue open → merged |

### Process Adherence Metrics

| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| DDD adoption | 0% | ≥80% | % features with docs-first |
| BDD adoption | 0% | ≥60% | % features with .feature files |
| TDD adoption | Varies | ≥70% | % code written test-first |
| Sprint adherence | N/A | ≥70% | % sprints completed on time |

---

## 7. Templates

### 7.1 Sprint Template

**Location**: `project-docs/sprints/sprint-template.md`

**Copy from**:
```bash
cp docs/reference/skilled-awareness/development-lifecycle/templates/sprint-template.md \
   project-docs/sprints/sprint-template.md
```

### 7.2 Release Template

**Location**: `project-docs/releases/release-template.md`

**Copy from**:
```bash
cp docs/reference/skilled-awareness/development-lifecycle/templates/release-template.md \
   project-docs/releases/release-template.md
```

### 7.3 Process Metrics Template

**Location**: `project-docs/metrics/PROCESS_METRICS.md`

**Copy from**:
```bash
cp docs/reference/skilled-awareness/development-lifecycle/templates/PROCESS_METRICS.md \
   project-docs/metrics/PROCESS_METRICS.md
```

---

## 8. FAQ

### Q1: Can I skip DDD for small bug fixes?

**Yes**. DDD is for **new features or API design**. For bug fixes:
1. Write failing test (TDD)
2. Fix bug (make test pass)
3. Verify no regression (run full suite)

### Q2: When should I use BDD vs just TDD?

**Use BDD** when:
- Feature is user-facing (API, CLI, UI)
- Requirements come from non-technical stakeholders
- Acceptance criteria are complex

**Use TDD only** when:
- Internal logic or algorithm
- Developer-only interface
- Quick bug fix

### Q3: How do I know if I'm doing TDD correctly?

**Checklist**:
- ✅ Test written **before** code (RED)
- ✅ Minimal code to pass test (GREEN)
- ✅ Refactor after test passes (REFACTOR)
- ✅ Tests run fast (<30 seconds for unit tests)
- ✅ Coverage ≥85%

### Q4: What if my team is too small for sprints?

**Solo developer**: Skip sprints, use ad-hoc planning
**2-3 developers**: Lightweight sprints (1-page plan, no ceremonies)
**4+ developers**: Full sprint process (template-based, ceremonies)

### Q5: How do I convince my team to adopt this?

**Steps**:
1. **Pilot**: 1 developer tries DDD→BDD→TDD on 1 feature
2. **Measure**: Track defects before/after, show 40-80% reduction
3. **Demo**: Show team the workflow, highlight benefits
4. **Expand**: 2-3 developers adopt, then full team
5. **Iterate**: Retrospective after 2-3 sprints, adjust process

**Key Message**: "This saves time by catching issues early"

---

## 9. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Development Lifecycle capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover 8-phase development lifecycle
- Quick reference for DDD→BDD→TDD workflow
- Links to lifecycle documentation

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
### Development Lifecycle

8-phase development lifecycle with integrated DDD→BDD→TDD workflow.

**Documentation**: [development-lifecycle/](./)

**Quick Start**:
- Read: [adoption-blueprint.md](adoption-blueprint.md)
- Guide: [awareness-guide.md](awareness-guide.md)

**Key Phases**:
- Documentation-Driven Design (DDD): Write docs first
- Behavior-Driven Development (BDD): Gherkin scenarios
- Test-Driven Development (TDD): RED-GREEN-REFACTOR
```

**Validation**:
```bash
grep "Development Lifecycle" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 10. Related Documents

**Workflow Docs**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - 8-phase lifecycle overview
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD→BDD→TDD integration
- [ANTI_PATTERNS.md](/static-template/dev-docs/ANTI_PATTERNS.md) - Common mistakes

**Templates** (in chora-base `static-template/`):
- `project-docs/sprints/sprint-template.md`
- `project-docs/releases/release-template.md`
- `project-docs/metrics/PROCESS_METRICS.md`

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - pytest infrastructure
- [SAP-007: documentation-framework](../documentation-framework/) - Diataxis for DDD
- [SAP-008: automation-scripts](../automation-scripts/) - Scripts for lifecycle

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for development-lifecycle SAP
