# Development Lifecycle

This document defines the development process for mcp-orchestration, following **Vision-Driven Development** principles with BDD/TDD/DDD practices.

## Overview

We use a **capability-first, behavior-driven development lifecycle** that ensures:
- Features are driven by user value (capabilities)
- Behavior is explicitly specified before implementation (BDD)
- Tests are written before code (TDD)
- Domain models emerge from capabilities (DDD)
- Documentation and tests are unified (E2E tests as how-to guides)

## The Development Lifecycle

### Phase 0: Vision & Planning
**Input:** User need, feature request, or Wave plan
**Output:** Wave plan in WAVE_1X_PLAN.md
**Duration:** Variable

**Activities:**
- Define Wave goals and scope
- Identify capabilities to deliver
- Estimate timeline
- Get stakeholder alignment

**Artifacts:**
- `project-docs/WAVE_1X_PLAN.md` - Updated with wave scope
- `ROADMAP.md` - Updated with committed features

---

### Phase 1: Capability Specification (DDD)
**Input:** Wave plan with high-level features
**Output:** Capability specification document
**Duration:** 1 hour per capability

**Activities:**
1. Create capability spec in `project-docs/capabilities/{capability-name}.md`
2. Define:
   - Behaviors (@behavior tags)
   - Value scenarios (E2E tests)
   - Integrations (CLI, MCP tools, APIs)
3. Identify domain concepts and models

**Template:**
```markdown
# Capability: {Name}

Brief description of what this capability provides.

## Behaviors
- @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
- @status:draft|ready|implemented

Behavior Specs:
- project-docs/capabilities/behaviors/{capability-name}.feature

## Value Scenarios
- ID: {namespace}.{capability}.{scenario} — Status: draft|ready|passing
  - Guide: user-docs/how-to/{guide-name}.md
  - Tests: tests/value-scenarios/test_{scenario}.py

## Integrations
- CLI: command-name
- MCP tools: tool_name
- APIs: endpoint paths
```

**Artifacts:**
- `project-docs/capabilities/{capability-name}.md`

**Example:**
- `project-docs/capabilities/config-publishing.md`

---

### Phase 2: Behavior Specification (BDD)
**Input:** Capability spec
**Output:** Gherkin feature file
**Duration:** 1 hour per capability

**Activities:**
1. Create `.feature` file in `project-docs/capabilities/behaviors/`
2. Write scenarios in Gherkin (Given/When/Then)
3. Cover happy paths and error cases
4. Use @behavior and @status tags

**Template:**
```gherkin
@behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
@status:draft|ready|implemented
Feature: {Feature name}
  As a {role}
  I want {goal}
  So that {benefit}

  Background:
    Given {common setup}

  Scenario: {Happy path}
    Given {precondition}
    When {action}
    Then {expected outcome}
    And {additional assertion}

  Scenario: {Error case}
    Given {error condition}
    When {action}
    Then {error behavior}
```

**Artifacts:**
- `project-docs/capabilities/behaviors/{capability-name}.feature`

**Example:**
- `project-docs/capabilities/behaviors/mcp-config-publish.feature`

---

### Phase 3: Value Scenario - E2E Test as How-To (DDD + BDD)
**Input:** Behavior specification
**Output:** How-to guide + E2E test
**Duration:** 2 hours per scenario

**Activities:**
1. Create user-facing how-to guide in `user-docs/how-to/`
2. Write step-by-step instructions with examples
3. Create E2E test in `tests/value-scenarios/` that executes the guide
4. **Key principle:** The test validates the documentation

**How-To Guide Structure** (Diátaxis):
```markdown
# How-To: {Task Name}

**Goal:** Accomplish {specific task}
**Audience:** {User persona}
**Prerequisites:** {Required setup}

## Steps

### Step 1: {Action}
{Instructions}

```bash
# Example command
mcp-orchestration {command}
```

**Expected output:**
```
{Sample output}
```

### Step 2: {Next action}
{Continue...}

## Troubleshooting

**Problem:** {Common issue}
**Solution:** {Fix}
```

**E2E Test Structure:**
```python
def test_value_scenario_{scenario_name}():
    """E2E test that executes the {guide-name} how-to guide.

    This test validates the complete user workflow documented in
    user-docs/how-to/{guide-name}.md

    References:
    - Capability: project-docs/capabilities/{capability-name}.md
    - Behavior: @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
    """
    # Step 1: {From how-to guide}
    # Step 2: {From how-to guide}
    # Step 3: {From how-to guide}
    # ...

    # Assertions verify expected outcomes from guide
    assert {expected_state}
```

**Artifacts:**
- `user-docs/how-to/{guide-name}.md`
- `tests/value-scenarios/test_{scenario}.py`

**Examples:**
- `user-docs/how-to/publish-config.md` + `tests/value-scenarios/test_publish_config.py`

---

### Phase 4: Test-Driven Development (TDD)
**Input:** Behavior spec, value scenario
**Output:** Unit tests (RED state)
**Duration:** 1 hour per module

**Activities:**
1. Create test file in `tests/test_{module}.py`
2. Write unit tests for all scenarios from BDD feature
3. Run tests - they should FAIL (RED)
4. Use test doubles (mocks, stubs) as needed

**TDD Cycle:**
```
RED → GREEN → REFACTOR
 ↓      ↓        ↓
Write  Write    Clean
Fail   Pass     Code
Test   Code     & Test
```

**Test Structure:**
```python
"""Tests for {module} ({Wave X.Y}).

This module tests {functionality} following BDD scenarios from
project-docs/capabilities/behaviors/{feature}.feature
"""

class Test{Capability}{Scenario}:
    """Test {scenario name} from BDD spec."""

    def test_{happy_path}(self):
        """Test @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION} - happy path."""
        # Arrange
        # Act
        # Assert

    def test_{error_case}(self):
        """Test @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION} - error case."""
        # Arrange
        # Act with pytest.raises
        # Assert error details
```

**Artifacts:**
- `tests/test_{module}.py` (failing tests)

**Coverage Requirement:** ≥70%

---

### Phase 5: Implementation
**Input:** Failing unit tests
**Output:** Working code (GREEN state)
**Duration:** Variable (1-2 hours per module)

**Activities:**
1. Implement minimum code to make tests pass
2. Follow domain model from capability spec
3. Run tests after each change
4. Achieve GREEN state (all tests pass)

**Domain-Driven Design Principles:**
- **Entities:** Objects with identity (e.g., ConfigArtifact)
- **Value Objects:** Immutable objects (e.g., ArtifactID)
- **Aggregates:** Clusters of entities (e.g., Config + Servers)
- **Repositories:** Storage abstractions (e.g., ArtifactStore)
- **Services:** Domain logic (e.g., PublishingWorkflow)

**Implementation Guidelines:**
- Start with simplest solution
- Add complexity only when tests demand it
- Follow existing code patterns
- Use type hints
- Add docstrings

**Artifacts:**
- `src/mcp_orchestrator/{module}/` - Implementation code

---

### Phase 6: Refactoring
**Input:** Passing tests (GREEN)
**Output:** Clean code (REFACTOR)
**Duration:** 30-60 min

**Activities:**
1. Improve code quality without changing behavior
2. Extract common patterns
3. Improve naming
4. Add comments for complex logic
5. Run tests after each refactor (must stay GREEN)

**Refactoring Checklist:**
- [ ] No duplicate code
- [ ] Clear, descriptive names
- [ ] Functions < 20 lines
- [ ] Classes have single responsibility
- [ ] Type hints on all public APIs
- [ ] Docstrings on all public APIs

---

### Phase 7: Integration
**Input:** Unit-tested modules
**Output:** Integrated system
**Duration:** 1 hour

**Activities:**
1. Wire up modules (dependency injection)
2. Add CLI commands
3. Update MCP server tools
4. Run integration tests
5. Run E2E value scenario tests

**Integration Points:**
- CLI commands in `src/mcp_orchestrator/cli_*.py`
- MCP tools in `src/mcp_orchestrator/mcp/server.py`
- Module exports in `__init__.py`

---

### Phase 8: Documentation & Release
**Input:** Working, tested code
**Output:** Released version
**Duration:** 1 hour

**Activities:**
1. Update API reference (`user-docs/reference/`)
2. Update CHANGELOG.md
3. Update WAVE_1X_PLAN.md (mark deliverables complete)
4. Update ROADMAP.md
5. Run full test suite
6. Create git commit
7. Create git tag (e.g., `v0.1.4`)
8. (Optional) Publish to PyPI

**Release Checklist:**
- [ ] All tests passing (pytest)
- [ ] Coverage ≥70% (pytest --cov)
- [ ] All BDD scenarios pass
- [ ] All value scenarios pass
- [ ] E2E how-to guides tested manually
- [ ] CHANGELOG.md updated
- [ ] Git tag created
- [ ] No uncommitted changes

---

## Process Adherence

### For Each Wave, Ensure:

**Capability-Driven:**
- [ ] Capability spec created before coding
- [ ] Domain model identified

**Behavior-Driven:**
- [ ] BDD feature file with Gherkin scenarios
- [ ] Scenarios cover happy paths and errors
- [ ] @behavior and @status tags present

**Value-Driven:**
- [ ] How-to guide exists for user workflow
- [ ] E2E test validates the how-to guide
- [ ] Test references capability and behavior

**Test-Driven:**
- [ ] Unit tests written BEFORE implementation
- [ ] Tests initially fail (RED)
- [ ] Code makes tests pass (GREEN)
- [ ] Code refactored for quality (REFACTOR)
- [ ] Coverage ≥70%

**Documentation:**
- [ ] API reference updated
- [ ] CHANGELOG.md updated
- [ ] Wave plan updated

---

## Anti-Patterns to Avoid

### ❌ Code-First Development
**Problem:** Write code, then write tests (testing becomes validation, not design)
**Fix:** Write tests first (TDD)

### ❌ Documentation as Afterthought
**Problem:** Write docs after code is done (docs get stale)
**Fix:** Write how-to guides as value scenarios (docs ARE tests)

### ❌ Behavior Without Specification
**Problem:** Implement features without BDD specs (ambiguous requirements)
**Fix:** Write .feature files first

### ❌ Missing Domain Model
**Problem:** Jump straight to implementation (anemic models, coupled code)
**Fix:** Define capabilities and domain concepts first (DDD)

### ❌ Skipping Refactoring
**Problem:** Get GREEN and move on (technical debt accumulates)
**Fix:** Always REFACTOR after GREEN

---

## Examples in This Codebase

### Wave 1.0-1.3: Partial Process
**What we did:**
- ✅ Tests before some implementation (TDD)
- ✅ Documentation (how-to guides)
- ❌ No capability specs
- ❌ No BDD feature files
- ❌ No value scenario E2E tests

**Result:** Good code, but missing behavior specs and E2E validation

### Wave 1.4: Full Process (This Wave!)
**What we're doing:**
- ✅ Capability spec: `config-publishing.md`
- ✅ BDD feature: `mcp-config-publish.feature`
- ✅ How-to guide: `publish-config.md`
- ✅ Value scenario: `test_publish_config.py`
- ✅ TDD: Write tests before `PublishingWorkflow`
- ✅ Implementation: Make tests pass
- ✅ Documentation: Complete CHANGELOG and references

**Result:** Fully specified, tested, and documented capability

---

## Tools & Frameworks

### Testing
- **pytest:** Test runner
- **pytest-cov:** Coverage reporting
- **pytest-asyncio:** Async test support

### BDD (Future)
- **behave:** Gherkin test runner (currently manual validation)
- **cucumber:** Alternative Gherkin runner

### Development
- **pyproject.toml:** Build configuration
- **ruff:** Linting
- **mypy:** Type checking

---

## References

- **Vision-Driven Development:** See chora-base template `user-docs/explanation/vision-driven-development.md`
- **Diátaxis Framework:** https://diataxis.fr/
- **Domain-Driven Design:** Eric Evans, "Domain-Driven Design"
- **Test-Driven Development:** Kent Beck, "Test Driven Development: By Example"
- **Behavior-Driven Development:** Dan North, "Introducing BDD"

---

## Workflow Summary

```
Wave Plan → Capability → Behavior → Value Scenario → TDD → Implementation → Release
             (DDD)       (BDD)      (E2E)           (TDD)     (Code)       (Docs)

1. Define capability and domain model
2. Write BDD scenarios (.feature)
3. Create how-to guide + E2E test
4. Write unit tests (RED)
5. Implement code (GREEN)
6. Refactor (REFACTOR)
7. Integrate
8. Document and release
```

**Time per capability:** 6-8 hours (full lifecycle)

**Quality outcome:**
- ✅ Clear requirements (capability + BDD)
- ✅ Validated workflows (value scenarios)
- ✅ High test coverage (TDD + E2E)
- ✅ Living documentation (tests validate guides)
- ✅ Clean architecture (DDD + refactoring)

---

## Conclusion

This development lifecycle ensures that **every feature is driven by user value, explicitly specified, thoroughly tested, and comprehensively documented** before release. By following BDD/TDD/DDD principles with value scenarios as E2E tests, we create a maintainable, well-tested codebase with living documentation that stays synchronized with the code.

**Next Steps:** Apply this process to Wave 1.4 (Config Publishing) as the exemplar implementation.
