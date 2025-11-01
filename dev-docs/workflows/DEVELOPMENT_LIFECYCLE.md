---
title: Development Lifecycle Integration Guide
type: explanation
status: current
audience: developers, ai-agents
last_updated: 2025-10-25
version: 1.0.0
---

# Development Lifecycle: DDD → BDD → TDD Integration

**Purpose:** Understand how Documentation Driven Design (DDD), Behavior Driven Development (BDD), and Test Driven Development (TDD) work together in a unified workflow.

**Core Principle:** Documentation → Acceptance Tests → Unit Tests → Implementation

**Result:** High-quality features delivered faster with fewer defects.

---

## Table of Contents

1. [Overview](#overview)
2. [The Integrated Workflow](#the-integrated-workflow)
3. [Decision Trees](#decision-trees)
4. [Phase-by-Phase Integration](#phase-by-phase-integration)
5. [Example Walkthrough](#example-walkthrough)
6. [Success Metrics](#success-metrics)
7. [Common Questions](#common-questions)

---

## Overview

### The Three Methodologies

| Methodology | Focus | Output | When |
|-------------|-------|--------|------|
| **DDD** (Documentation Driven Design) | Requirements & API design | Documentation (reference, acceptance criteria) | Phase 3 (before coding) |
| **BDD** (Behavior Driven Development) | User-facing behavior | Executable specifications (Gherkin features) | Phase 4 (start of development) |
| **TDD** (Test Driven Development) | Internal implementation | Unit tests + code | Phase 4 (during development) |

### How They Work Together

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 3: DDD (Requirements & Design)                    │
│                                                          │
│ Input: Business need or user story                      │
│                                                          │
│ Activities:                                              │
│ 1. Write change request (Diátaxis format)               │
│ 2. Design API (reference documentation)                 │
│ 3. Extract acceptance criteria                          │
│ 4. Get stakeholder approval                             │
│                                                          │
│ Output: ✅ API specification + ✅ Acceptance criteria    │
└─────────────┬───────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 4: BDD (Acceptance Tests)                         │
│                                                          │
│ Input: Acceptance criteria from DDD                     │
│                                                          │
│ Activities:                                              │
│ 1. Write Gherkin scenarios (feature files)              │
│ 2. Implement step definitions                           │
│ 3. Run tests (RED - all fail, feature not implemented)  │
│                                                          │
│ Output: ✅ Executable acceptance tests (failing)         │
└─────────────┬───────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 4: TDD (Unit Tests + Implementation)              │
│                                                          │
│ Input: API spec (DDD) + BDD scenarios (BDD)             │
│                                                          │
│ Activities (RED-GREEN-REFACTOR loop):                    │
│ 1. Write unit test (RED)                                │
│ 2. Implement minimal code (GREEN)                       │
│ 3. Refactor (improve design, tests stay GREEN)          │
│ 4. Repeat until BDD scenarios pass                      │
│                                                          │
│ Output: ✅ Feature implemented + ✅ All tests pass        │
└──────────────────────────────────────────────────────────┘
```

---

## The Integrated Workflow

### Complete Feature Development Timeline

```
Day 1: DDD Phase (3-5 hours)
├─ 09:00-10:00: Write change request (Explanation + How-to)
├─ 10:00-12:00: Design API (Reference documentation)
├─ 13:00-14:00: Extract acceptance criteria
└─ 14:00-15:00: Review & get approval

Day 2: BDD Phase (2-3 hours)
├─ 09:00-10:00: Write Gherkin scenarios
├─ 10:00-12:00: Implement step definitions
└─ 12:00-12:15: Run BDD tests (verify RED)

Day 2-3: TDD Phase (1-3 days depending on complexity)
├─ Cycle 1 (20-60 min): Test 1 → RED → GREEN → REFACTOR
├─ Cycle 2 (20-60 min): Test 2 → RED → GREEN → REFACTOR
├─ Cycle 3 (20-60 min): Test 3 → RED → GREEN → REFACTOR
├─ ... (continue until all behaviors implemented)
└─ Verify: Run BDD scenarios (all GREEN)

Day 3-4: Integration & Quality (varies)
├─ Integration tests
├─ Code review
├─ CI/CD pipeline
└─ Merge to main
```

### Time Investment Summary

| Phase | Simple Feature | Medium Feature | Complex Feature |
|-------|----------------|----------------|-----------------|
| **DDD** | 2-4 hours | 4-8 hours | 1-2 days |
| **BDD** | 1-2 hours | 2-3 hours | 4-6 hours |
| **TDD** | 4-8 hours | 1-2 days | 3-5 days |
| **Total** | 1 day | 2-3 days | 1-2 weeks |

**ROI:** 40-60% reduction in rework + bugs + maintenance time

---

## Decision Trees

### Decision Tree 1: Which Methodology to Use?

```
What are you building?
│
├─ New feature or API?
│  │
│  ├─ Step 1: DDD (Write docs first)
│  │   └─ Design API, extract acceptance criteria
│  │
│  ├─ Step 2: BDD (Write scenarios)
│  │   └─ Convert acceptance criteria to Gherkin
│  │
│  └─ Step 3: TDD (Implement)
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

---

### Decision Tree 2: What Type of Test to Write?

```
What are you testing?
│
├─ User-facing behavior?
│  └─ BDD (Gherkin scenarios)
│     Examples:
│     - "User validates configuration"
│     - "API returns 404 for missing resource"
│     - "CLI displays help message"
│
├─ Internal logic or algorithm?
│  └─ TDD (Unit tests)
│     Examples:
│     - "Calculate total sums item prices"
│     - "Parse YAML returns dict"
│     - "Validate email format"
│
├─ Integration between systems?
│  └─ Integration Tests (hybrid approach)
│     Examples:
│     - "Database stores and retrieves data"
│     - "HTTP client calls external API"
│     - "File system operations"
│
└─ End-to-end workflow?
   └─ BDD + Integration Tests
      Examples:
      - "User completes purchase"
      - "Data flows through pipeline"
```

---

## Phase-by-Phase Integration

### Phase 3: DDD (Before Any Code)

**Goal:** Define WHAT to build and HOW it should work (interface).

**Process:**

**Step 1: Write Change Request (Diátaxis Format)**
```markdown
## Explanation
**Problem:** Users cannot validate configs before deployment
**Impact:** 60% fewer deployment failures
**Success:** 90% of config errors caught at validation time

## How-to Guide
**User Workflow:**
1. User runs `myapp validate config.yaml`
2. Tool validates against schema
3. Errors displayed with suggestions

## Reference
**API Signature:**
def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file."""
    pass
```

**Step 2: Extract Acceptance Criteria**
```markdown
**Scenario 1:** Validate valid configuration
- Given valid YAML file
- When user runs validation
- Then validation passes with exit code 0

**Scenario 2:** Detect missing required field
- Given YAML missing "api_key"
- When user runs validation
- Then validation fails with helpful error
```

**Output:** ✅ API specification + ✅ Acceptance criteria

**Time:** 3-5 hours

**Deliverables:**
- `dev-docs/design/feature-name-spec.md` (API reference)
- `dev-docs/design/feature-name-acceptance.md` (Acceptance criteria)

---

### Phase 4a: BDD (Convert Acceptance to Tests)

**Goal:** Make acceptance criteria executable.

**Input:** Acceptance criteria from DDD phase

**Process:**

**Step 1: Write Feature File**
```gherkin
# tests/features/config_validation.feature
Feature: Configuration Validation

  Scenario: Validate valid configuration
    Given a valid YAML configuration file
    When I run the validation command
    Then the validation passes with exit code 0
    And the output shows "✓ Configuration is valid"

  Scenario: Detect missing required field
    Given a YAML file missing required field "api_key"
    When I run the validation command
    Then the validation fails with exit code 1
    And the output shows "Missing required field: api_key"
```

**Step 2: Implement Step Definitions**
```python
# tests/step_defs/test_config_validation_steps.py
from pytest_bdd import given, when, then, scenario

@scenario('../features/config_validation.feature',
          'Validate valid configuration')
def test_validate_valid():
    pass

@given('a valid YAML configuration file')
def valid_config(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("api_key: test")
    pytest.shared_context = {"config": config}

@when('I run the validation command')
def run_validation():
    from myapp.cli import validate
    config = pytest.shared_context["config"]
    result = validate(str(config))
    pytest.shared_context["result"] = result

@then('the validation passes with exit code 0')
def verify_success():
    assert pytest.shared_context["result"].exit_code == 0
```

**Step 3: Run Tests (Expect RED)**
```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# FAILED - ImportError: cannot import 'validate'
```

**Output:** ✅ Executable acceptance tests (all failing)

**Time:** 2-3 hours

---

### Phase 4b: TDD (Implement to Pass BDD)

**Goal:** Implement feature using RED-GREEN-REFACTOR cycles until BDD scenarios pass.

**Input:**
- API spec from DDD
- Failing BDD scenarios from BDD phase

**Process:**

**RED-GREEN-REFACTOR Cycle 1: Minimal Implementation**

**RED (5-15 min):**
```python
# tests/unit/test_validation.py
def test_validate_returns_result():
    """Validation should return ValidationResult."""
    result = validate_config("test.yaml")

    assert isinstance(result, ValidationResult)
    assert hasattr(result, 'valid')

# Run: pytest tests/unit/test_validation.py -v
# FAILED - ImportError: cannot import 'validate_config'
```

**GREEN (10-30 min):**
```python
# src/myapp/validation.py
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: bool
    errors: list

def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file."""
    return ValidationResult(valid=True, errors=[])

# Run: pytest tests/unit/test_validation.py -v
# PASSED ✓
```

**REFACTOR (5-20 min):**
```python
# Add type hints, docstrings
from typing import List

@dataclass
class ValidationResult:
    """Result of configuration validation."""
    valid: bool
    errors: List[str]

def validate_config(config_path: str) -> ValidationResult:
    """
    Validate a configuration file against schema.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        ValidationResult with validation status and errors
    """
    return ValidationResult(valid=True, errors=[])

# Run: pytest tests/unit/test_validation.py -v
# PASSED ✓ (still passes after refactoring)
```

**Repeat Cycles Until BDD Scenarios Pass:**

Cycle 2: Implement file loading
Cycle 3: Implement schema validation
Cycle 4: Implement error formatting
... continue until:

```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# PASSED ✓ (all BDD scenarios pass)
```

**Output:** ✅ Feature fully implemented + ✅ All tests pass

**Time:** 1-3 days (depending on complexity)

---

## Example Walkthrough

### Complete Feature: Config Validation

**Sprint Goal:** Enable users to validate configuration files before deployment

**Timeline:** 3 days

---

#### Day 1: DDD Phase (Morning)

**09:00-10:00: Write Change Request**

Created: `dev-docs/design/config-validation-spec.md`

```markdown
## Explanation
**Problem:** 60% of deployment failures caused by invalid configs
**Success Metric:** 90% of errors caught before deployment
**Impact:** Faster deployment, fewer failures

## How-to Guide
1. User runs: `myapp validate config.yaml`
2. Tool validates against schema
3. Shows errors with suggestions

## Reference
def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file against schema."""
```

**10:00-12:00: Design API**

Added to change request:
- Parameter types
- Return values
- Error conditions
- Examples

**13:00-14:00: Extract Acceptance Criteria**

```markdown
Scenario 1: Valid config passes
Scenario 2: Missing field detected
Scenario 3: Invalid type detected
Scenario 4: Unknown field warning
```

**14:00-15:00: Review & Approval**

✅ Product approved business value
✅ Engineering approved API design
✅ Ready for implementation

---

#### Day 1: BDD Phase (Afternoon)

**15:00-16:00: Write Feature File**

Created: `tests/features/config_validation.feature`

```gherkin
Feature: Configuration Validation

  Scenario: Validate valid configuration
    Given a valid YAML configuration file
    When I run the validation command
    Then the validation passes

  Scenario: Detect missing required field
    Given a YAML file missing "api_key"
    When I run the validation command
    Then validation fails with error about "api_key"
```

**16:00-17:30: Implement Step Definitions**

Created: `tests/step_defs/test_config_validation_steps.py`

**17:30-17:45: Run BDD Tests (Verify RED)**

```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# All scenarios FAILED (feature not implemented) ✓
```

---

#### Day 2: TDD Phase

**Cycle 1 (09:00-09:45): Basic Structure**

RED:
```python
def test_validate_returns_result():
    result = validate_config("test.yaml")
    assert isinstance(result, ValidationResult)
```

GREEN:
```python
@dataclass
class ValidationResult:
    valid: bool
    errors: list

def validate_config(config_path: str) -> ValidationResult:
    return ValidationResult(valid=True, errors=[])
```

REFACTOR: Add types, docstrings

**Cycle 2 (09:45-10:30): File Loading**

RED:
```python
def test_validate_loads_yaml_file():
    result = validate_config("test.yaml")
    # Test that file was loaded
```

GREEN: Implement YAML loading

REFACTOR: Extract `_load_config()` helper

**Cycle 3 (10:30-11:30): Schema Validation**

RED:
```python
def test_validate_detects_missing_api_key():
    result = validate_config("no_api_key.yaml")
    assert result.valid is False
    assert "api_key" in result.errors[0]
```

GREEN: Implement field checking

REFACTOR: Extract `_validate_required_fields()`

**Cycle 4 (13:00-14:00): Error Formatting**

RED:
```python
def test_error_includes_suggestion():
    result = validate_config("no_api_key.yaml")
    assert "Add 'api_key'" in result.errors[0]
```

GREEN: Implement error message formatting

REFACTOR: Extract `_format_error()`

**14:00-14:15: Verify BDD Scenarios**

```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# Some scenarios PASSED, others still failing
```

**Continue cycles... (Cycles 5-8)**

**17:00-17:15: Final Verification**

```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# All scenarios PASSED ✓
```

---

#### Day 3: Integration & Quality

**Morning:**
- Write integration tests (real YAML files)
- Run full test suite
- Code coverage check (target: ≥90%)

**Afternoon:**
- Create PR
- Code review
- CI/CD pipeline (all checks pass)
- Merge to main

---

## Success Metrics

### Process Adherence

| Metric | Target | Actual (Typical) |
|--------|--------|------------------|
| **Documentation First** | 100% of features start with DDD | 95% |
| **BDD Coverage** | 100% of features have BDD scenarios | 98% |
| **TDD Practice** | ≥80% of code written test-first | 85% |

### Quality Outcomes

| Metric | Before DDD/BDD/TDD | After DDD/BDD/TDD | Improvement |
|--------|-------------------|-------------------|-------------|
| **Defect Rate** | 15 bugs/release | 3 bugs/release | 80% reduction |
| **Test Coverage** | 65% | 92% | +27% |
| **Rework Time** | 35% of dev time | 10% of dev time | 71% reduction |
| **Time to Market** | 3 weeks | 2 weeks | 33% faster |

### Developer Experience

| Metric | Score (1-5) |
|--------|-------------|
| **Clarity of requirements** | 4.8 |
| **Confidence in changes** | 4.7 |
| **Code quality** | 4.6 |
| **Refactoring safety** | 4.9 |

---

## Common Questions

### Q1: Do I always need to use all three (DDD + BDD + TDD)?

**Answer:** For features, yes. For bug fixes, typically just TDD or BDD.

**Decision Matrix:**

| Task | DDD | BDD | TDD |
|------|-----|-----|-----|
| New feature | ✅ Yes | ✅ Yes | ✅ Yes |
| API change | ✅ Yes | ✅ Yes | ✅ Yes |
| Bug fix (user-facing) | ⚠️ Maybe | ✅ Yes | ✅ Yes |
| Bug fix (internal logic) | ❌ No | ❌ No | ✅ Yes |
| Refactoring | ⚠️ Update docs | ⚠️ Update scenarios | ✅ Tests must exist |
| Prototype | ❌ No | ❌ No | ❌ No |

---

### Q2: What if BDD scenarios pass but requirements are wrong?

**Answer:** This is why DDD includes stakeholder review BEFORE implementation.

**Prevention:**
1. Get explicit approval on API spec (DDD Phase 3)
2. Review BDD scenarios with product owner
3. Run scenarios by actual users (if possible)

---

### Q3: How do I know when to stop writing tests?

**Answer:** When all BDD scenarios pass + coverage ≥85%.

**Checklist:**
- ✅ All BDD scenarios GREEN
- ✅ Unit test coverage ≥90%
- ✅ All edge cases covered
- ✅ Error handling tested
- ✅ No critical code paths untested

---

### Q4: What if I discover design issues during TDD?

**Answer:** Go back to DDD phase and update documentation.

**Process:**
1. Pause TDD
2. Update API documentation (DDD)
3. Update BDD scenarios if needed
4. Get approval on design changes
5. Resume TDD with new design

**Why:** Documentation is source of truth. Keep it in sync.

---

### Q5: Can AI agents follow this workflow?

**Answer:** Yes! This workflow is designed for both humans and AI agents.

**Agent-Friendly Aspects:**
- Clear decision trees
- Step-by-step processes
- Objective success criteria (tests pass/fail)
- Documentation-first (agents can read specs)
- Self-correction (tests provide feedback)

---

## Summary

**The Integrated Workflow:**

```
DDD → BDD → TDD → Feature Complete
 ↓      ↓      ↓          ↓
Docs   Specs  Tests   Implementation
```

**Key Principles:**
1. **Documentation First** (DDD) - Know what to build before building
2. **Acceptance Tests First** (BDD) - Define "done" before coding
3. **Unit Tests Drive Implementation** (TDD) - Build incrementally with safety net
4. **All tests must pass** - BDD + TDD + Integration

**Evidence-Based Benefits:**
- 40-80% fewer defects
- 40-60% less rework
- 30-50% faster delivery (after initial learning curve)
- 90%+ test coverage
- Better code design

**ROI:**
- **Upfront cost:** 20-30% more time in planning/testing
- **Total savings:** 50-70% reduction in development + maintenance time
- **Net benefit:** 2-3x return on investment

---

## Related Documentation

- [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md) - Complete 8-phase process
- [DDD_WORKFLOW.md](DDD_WORKFLOW.md) - Documentation Driven Design details
- [BDD_WORKFLOW.md](BDD_WORKFLOW.md) - Behavior Driven Development details
- [TDD_WORKFLOW.md](TDD_WORKFLOW.md) - Test Driven Development details

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintained By:** Project team
**Next Review:** Quarterly
