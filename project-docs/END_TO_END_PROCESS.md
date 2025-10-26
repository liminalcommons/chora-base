# End-to-End Process Overview: Vision Through Release Publishing

**Document Type:** Process Guide
**Audience:** Developers, AI Agents, Contributors, Project Managers
**Last Updated:** 2025-10-25
**Status:** Active

---

## Table of Contents

1. [Overview](#overview)
2. [The Complete Lifecycle](#the-complete-lifecycle)
3. [Phase 0: Strategic Vision & Wave Planning](#phase-0-strategic-vision--wave-planning)
4. [Phase 1: Capability Specification (DDD)](#phase-1-capability-specification-ddd)
5. [Phase 2: Behavior Specification (BDD)](#phase-2-behavior-specification-bdd)
6. [Phase 3: Value Scenarios (Living Documentation)](#phase-3-value-scenarios-living-documentation)
7. [Phase 4: Test-Driven Development (TDD)](#phase-4-test-driven-development-tdd)
8. [Phase 5: Implementation](#phase-5-implementation)
9. [Phase 6: Integration & Wiring](#phase-6-integration--wiring)
10. [Phase 7: Documentation & Quality Gates](#phase-7-documentation--quality-gates)
11. [Phase 8: Release Publishing](#phase-8-release-publishing)
12. [Phase 9: Feedback & Iteration](#phase-9-feedback--iteration)
13. [Process Integration Map](#process-integration-map)
14. [Appendices](#appendices)

---

## Overview

This document provides a **comprehensive end-to-end view** of how mcp-orchestration progresses from strategic vision through operational execution to production release. It integrates:

- **Vision-Driven Development** (strategic direction)
- **Domain-Driven Design** (DDD - capability modeling)
- **Behavior-Driven Development** (BDD - executable specifications)
- **Test-Driven Development** (TDD - RED-GREEN-REFACTOR)
- **Wave-Based Planning** (incremental delivery)
- **Release Management** (semantic versioning, changelog, PyPI publishing)

**Key Principles:**
- 📋 **Specification before implementation** - Write docs/specs first
- ✅ **Tests as documentation** - E2E tests validate how-to guides
- 🔄 **Continuous feedback** - Each phase validates the previous
- 📦 **Incremental delivery** - Ship value in waves, not waterfalls
- 🎯 **User-centric** - Everything driven by user value scenarios

---

## The Complete Lifecycle

### High-Level View

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE COMPLETE LIFECYCLE                           │
│                  (Vision → Release → Feedback)                       │
└─────────────────────────────────────────────────────────────────────┘

  Phase 0: STRATEGIC VISION
       ↓
  ┌────────────────────────────────────┐
  │   Wave Planning & Prioritization    │
  │   • User needs → Capabilities       │
  │   • Roadmap alignment               │
  │   • Success criteria                │
  └────────────────┬───────────────────┘
                   ↓
  Phase 1: CAPABILITY SPECIFICATION (DDD)
       ↓
  ┌────────────────────────────────────┐
  │   Domain Modeling                   │
  │   • Behaviors (@behavior tags)      │
  │   • Domain concepts (entities)      │
  │   • Value scenarios                 │
  └────────────────┬───────────────────┘
                   ↓
  Phase 2: BEHAVIOR SPECIFICATION (BDD)
       ↓
  ┌────────────────────────────────────┐
  │   Gherkin Scenarios                 │
  │   • Given/When/Then                 │
  │   • Happy paths & errors            │
  │   • Executable specs                │
  └────────────────┬───────────────────┘
                   ↓
  Phase 3: VALUE SCENARIOS (Living Docs)
       ↓
  ┌────────────────────────────────────┐
  │   How-To Guides + E2E Tests         │
  │   • User-facing guides              │
  │   • Tests validate guides           │
  │   • Documentation IS tests          │
  └────────────────┬───────────────────┘
                   ↓
  Phase 4: TEST-DRIVEN DEVELOPMENT (TDD)
       ↓
  ┌────────────────────────────────────┐
  │   RED → GREEN → REFACTOR            │
  │   • Write failing tests (RED)       │
  │   • Implement to pass (GREEN)       │
  │   • Clean up code (REFACTOR)        │
  └────────────────┬───────────────────┘
                   ↓
  Phase 5: IMPLEMENTATION
       ↓
  ┌────────────────────────────────────┐
  │   Domain Code                       │
  │   • Entities, Value Objects         │
  │   • Services, Repositories          │
  │   • Following domain model          │
  └────────────────┬───────────────────┘
                   ↓
  Phase 6: INTEGRATION & WIRING
       ↓
  ┌────────────────────────────────────┐
  │   System Integration                │
  │   • CLI commands                    │
  │   • MCP tools                       │
  │   • Module exports                  │
  └────────────────┬───────────────────┘
                   ↓
  Phase 7: DOCUMENTATION & QUALITY GATES
       ↓
  ┌────────────────────────────────────┐
  │   Quality Assurance                 │
  │   • API reference updates           │
  │   • Coverage ≥85%                   │
  │   • Linting, type checking          │
  │   • Pre-commit hooks pass           │
  └────────────────┬───────────────────┘
                   ↓
  Phase 8: RELEASE PUBLISHING
       ↓
  ┌────────────────────────────────────┐
  │   Release to Production             │
  │   • Version bump (semver)           │
  │   • CHANGELOG update                │
  │   • Git tag                         │
  │   • PyPI publish                    │
  └────────────────┬───────────────────┘
                   ↓
  Phase 9: FEEDBACK & ITERATION
       ↓
  ┌────────────────────────────────────┐
  │   Monitoring & Learning             │
  │   • User feedback                   │
  │   • Metrics & telemetry             │
  │   • Bug reports                     │
  │   • Feature requests                │
  └────────────────┬───────────────────┘
                   │
                   └─────► (Back to Phase 0 for next wave)
```

### Timeline View (Example: Wave 1.4 - Config Publishing)

```
Day 1-2    │ Phase 0-1 │ Vision & Capability Spec
Day 2-3    │ Phase 2   │ BDD Scenarios (Gherkin)
Day 3-4    │ Phase 3   │ How-To Guide + E2E Test
Day 4-6    │ Phase 4-5 │ TDD + Implementation
Day 6-7    │ Phase 6   │ Integration (CLI, MCP tools)
Day 7      │ Phase 7   │ Documentation + Quality Gates
Day 7      │ Phase 8   │ Release Publishing
Ongoing    │ Phase 9   │ Monitoring & Feedback

Total: ~7-8 days per capability (full lifecycle)
```

### Artifact Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      ARTIFACT FLOW                            │
│          (What gets created in each phase)                    │
└──────────────────────────────────────────────────────────────┘

Phase 0: Strategic Vision
    ↓
    📄 WAVE_1X_PLAN.md (updated)
    📄 ROADMAP.md (updated)
    ↓
Phase 1: Capability Specification
    ↓
    📄 project-docs/capabilities/{capability-name}.md
    ↓
Phase 2: Behavior Specification
    ↓
    📄 project-docs/capabilities/behaviors/{capability}.feature
    ↓
Phase 3: Value Scenarios
    ↓
    📄 user-docs/how-to/{guide-name}.md
    📄 tests/value-scenarios/test_{scenario}.py
    ↓
Phase 4-5: TDD + Implementation
    ↓
    📄 tests/test_{module}.py (unit tests)
    📄 src/mcp_orchestrator/{module}/
    ↓
Phase 6: Integration
    ↓
    📄 src/mcp_orchestrator/cli_{command}.py
    📄 src/mcp_orchestrator/mcp/server.py (updated)
    ↓
Phase 7: Documentation
    ↓
    📄 user-docs/reference/{api-docs}.md
    📄 CHANGELOG.md (updated)
    ↓
Phase 8: Release
    ↓
    🏷️ Git tag (v0.1.X)
    📦 PyPI package
    ↓
Phase 9: Feedback
    ↓
    📊 Metrics, user feedback, bug reports
    └──► (Feed into next wave planning)
```

---

## Phase 0: Strategic Vision & Wave Planning

### Purpose
Define **WHAT** we're building and **WHY** it matters to users before any implementation begins.

### Inputs
- User needs, feature requests
- Market/competitive analysis
- Technical constraints
- Long-term vision documents ([dev-docs/vision/](../dev-docs/vision/))

### Outputs
- **WAVE_1X_PLAN.md** - Wave scope, goals, timeline
- **ROADMAP.md** - Updated with committed features
- Stakeholder alignment

### Process

```
┌─────────────────────────────────────────────────────────────┐
│              PHASE 0: STRATEGIC VISION                       │
└─────────────────────────────────────────────────────────────┘

1. IDENTIFY USER NEEDS
   ↓
   Questions to answer:
   • What problem are users trying to solve?
   • What value does this provide?
   • How does this fit the product vision?
   ↓
2. PRIORITIZE CAPABILITIES
   ↓
   Criteria:
   • User impact (high/medium/low)
   • Implementation cost (person-days)
   • Dependencies (blockers?)
   • Strategic value (future enablement)
   ↓
3. DEFINE WAVE SCOPE
   ↓
   Wave structure:
   • Wave name & version (e.g., "Wave 1.4 - Config Publishing")
   • Goal statement (1-2 sentences)
   • Capabilities to deliver (3-5 max)
   • Success criteria (measurable)
   • Timeline (days/weeks)
   ↓
4. UPDATE PLANNING DOCS
   ↓
   • Update WAVE_1X_PLAN.md with new wave section
   • Update ROADMAP.md with committed features
   • Create capability placeholders
   ↓
5. GET STAKEHOLDER ALIGNMENT
   ↓
   • Review with team/stakeholders
   • Confirm priorities and timeline
   • Approve to proceed
```

### Example: Wave 1.4 Planning

**User Need:**
> "I want to validate my MCP configuration before publishing to catch errors early."

**Wave Definition:**
- **Name:** Wave 1.4 - Configuration Publishing Workflow
- **Goal:** Enable validated configuration publishing with cryptographic signing
- **Capabilities:**
  1. Config validation (validate_config tool)
  2. Publishing workflow (PublishingWorkflow service)
  3. CLI publishing (mcp-orchestration-publish-config)
- **Success Criteria:**
  - ✅ Users can validate configs before publishing
  - ✅ Invalid configs rejected with clear errors
  - ✅ Changelog included in published artifacts
- **Timeline:** 7-8 days

### Templates & Checklists

**Wave Planning Template:**
```markdown
## Wave X.Y (vX.Y.Z) — {Wave Name}

**Status**: Planning/In Progress/Complete
**Goal**: {One-sentence goal}
**Estimated Timeline**: {days/weeks}

### Scope

#### Capabilities
1. {Capability 1 name} - {Brief description}
2. {Capability 2 name} - {Brief description}

#### Success Criteria
- [ ] {Measurable outcome 1}
- [ ] {Measurable outcome 2}
- [ ] Test coverage ≥85%
- [ ] All BDD scenarios pass

#### Out of Scope
- {What we're NOT doing in this wave}

### Dependencies
- {External dependencies}
- {Prerequisites from previous waves}

### Risks
- {Risk 1} - {Mitigation}
```

**Wave Planning Checklist:**
- [ ] User need clearly identified
- [ ] Capability scoped to 3-5 deliverables
- [ ] Success criteria measurable
- [ ] Timeline estimated (7-10 days typical)
- [ ] Dependencies identified
- [ ] WAVE_1X_PLAN.md updated
- [ ] ROADMAP.md updated
- [ ] Stakeholders aligned

---

## Phase 1: Capability Specification (DDD)

### Purpose
Define the **domain model** and **behaviors** for the capability before writing any code.

### Inputs
- Wave plan with high-level features
- Domain knowledge (entities, value objects, aggregates)

### Outputs
- **Capability Specification Document** (`project-docs/capabilities/{name}.md`)
- Domain model (entities, services, repositories)
- Behavior tags (@behavior annotations)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│         PHASE 1: CAPABILITY SPECIFICATION (DDD)              │
└─────────────────────────────────────────────────────────────┘

1. IDENTIFY DOMAIN CONCEPTS
   ↓
   Domain-Driven Design elements:
   • Entities (objects with identity)
   • Value Objects (immutable values)
   • Aggregates (entity clusters)
   • Services (domain logic)
   • Repositories (storage abstractions)
   ↓
2. DEFINE BEHAVIORS
   ↓
   Each behavior answers:
   • WHAT does this capability do?
   • WHO are the actors?
   • WHEN does it happen?
   • Tag: @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
   ↓
3. MAP VALUE SCENARIOS
   ↓
   User workflows:
   • Scenario ID: {namespace}.{capability}.{scenario}
   • User journey: Step-by-step workflow
   • How-To guide: user-docs/how-to/{guide}.md
   • E2E test: tests/value-scenarios/test_{scenario}.py
   ↓
4. DOCUMENT INTEGRATIONS
   ↓
   • CLI commands
   • MCP tools
   • APIs/modules
   ↓
5. CREATE CAPABILITY SPEC
   ↓
   File: project-docs/capabilities/{capability-name}.md
```

### Example: Config Publishing Capability

**File:** `project-docs/capabilities/config-publishing.md`

**Domain Model:**
- **Entities:**
  - `ConfigArtifact` - Immutable signed configuration
- **Services:**
  - `PublishingWorkflow` - Orchestrates validation → signing → storage
- **Value Objects:**
  - `ValidationResult` - Validation outcome
  - `PublishResult` - Publishing outcome
- **Repositories:**
  - `ArtifactStore` - Content-addressable storage

**Behaviors:**
- `@behavior:MCP.CONFIG.PUBLISH` - Publish validated configuration
- `@behavior:MCP.CONFIG.VALIDATE` - Validate before publishing

**Value Scenarios:**
1. **Full Publishing Workflow**
   - ID: `mcp.config.publish.full-workflow`
   - Guide: [user-docs/how-to/publish-config.md](../user-docs/how-to/publish-config.md)
   - Test: [tests/value-scenarios/test_publish_config.py](../tests/value-scenarios/test_publish_config.py)

### Templates

**Capability Specification Template:**
```markdown
# Capability: {Capability Name}

{Brief description of what this capability provides}

## Behaviors
- @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
- @status:draft|ready|implemented

Behavior Specs:
- project-docs/capabilities/behaviors/{capability}.feature

## Value Scenarios

### Scenario 1: {Scenario Name}
- **ID:** {namespace}.{capability}.{scenario}
- **Status:** draft|ready|passing
- **Guide:** user-docs/how-to/{guide}.md
- **Tests:** tests/value-scenarios/test_{scenario}.py
- **Description:** {What this scenario demonstrates}

## Integrations

### MCP Tools
- `tool_name` - {Description}

### CLI Commands
- `command-name` - {Description}

### Domain Model

#### Entities
- **{EntityName}** - {Description}

#### Value Objects
- **{ValueObjectName}** - {Description}

#### Services
- **{ServiceName}** - {Description}

#### Repositories
- **{RepositoryName}** - {Description}

## Dependencies

### From Other Capabilities
- {Dependency 1}

### External Dependencies
- {Library/service}

## Success Criteria

### Functional
- [ ] {Functional requirement 1}

### Non-Functional
- [ ] Performance: {metric}
- [ ] Test coverage: ≥85%
- [ ] All BDD scenarios pass

## Wave Alignment
**Wave X.Y (vX.Y.Z)**
- Goal: {Wave goal}
- Deliverables: {What gets delivered}

## Spec Coverage
- ✅ **FR-X:** {Requirement description}

## Future Evolution
### Wave 2.x: {Future enhancement}

## References
- [Link to related docs]
```

**Capability Specification Checklist:**
- [ ] Domain model identified (entities, services, value objects)
- [ ] Behaviors defined with @behavior tags
- [ ] Value scenarios mapped to guides + tests
- [ ] Integrations documented (CLI, MCP, API)
- [ ] Success criteria measurable
- [ ] Wave alignment clear
- [ ] File created: `project-docs/capabilities/{name}.md`

---

## Phase 2: Behavior Specification (BDD)

### Purpose
Specify **executable behaviors** in Gherkin (Given/When/Then) format before implementation.

### Inputs
- Capability specification document
- Domain behaviors identified

### Outputs
- **Gherkin Feature File** (`project-docs/capabilities/behaviors/{capability}.feature`)
- Scenarios covering happy paths and error cases

### Process

```
┌─────────────────────────────────────────────────────────────┐
│         PHASE 2: BEHAVIOR SPECIFICATION (BDD)                │
└─────────────────────────────────────────────────────────────┘

1. EXTRACT SCENARIOS FROM CAPABILITY SPEC
   ↓
   Each behavior → Multiple scenarios:
   • Happy path (success case)
   • Error cases (validation failures, exceptions)
   • Edge cases (boundary conditions)
   ↓
2. WRITE GHERKIN SCENARIOS
   ↓
   Format: Given/When/Then
   • Given: Preconditions
   • When: Action taken
   • Then: Expected outcome
   • And: Additional assertions
   ↓
3. ADD METADATA TAGS
   ↓
   • @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
   • @status:draft|ready|implemented
   • @priority:high|medium|low (optional)
   ↓
4. VALIDATE COMPLETENESS
   ↓
   Coverage check:
   • All behaviors from capability spec covered?
   • All error paths specified?
   • All assertions testable?
   ↓
5. REVIEW & APPROVE
   ↓
   • Review with stakeholders
   • Update @status to "ready"
```

### Example: Config Publishing BDD Spec

**File:** `project-docs/capabilities/behaviors/mcp-config-publish.feature`

```gherkin
@behavior:MCP.CONFIG.PUBLISH
@status:implemented
Feature: MCP Configuration Publishing
  As an MCP user
  I want to publish validated configurations
  So that I can safely deploy MCP server configs

  Background:
    Given the orchestration system is initialized
    And signing keys are available

  Scenario: Successfully publish valid configuration
    Given I have a valid draft configuration with 2 servers
    And the configuration passes validation
    When I publish the configuration with changelog "Initial setup"
    Then a signed artifact is created
    And the artifact ID is computed from SHA-256(payload)
    And the artifact metadata includes changelog
    And the artifact metadata includes server_count=2
    And the profile index is updated

  Scenario: Reject publishing invalid configuration
    Given I have a draft configuration with missing required fields
    When I attempt to publish the configuration
    Then the publish operation fails
    And I receive a validation error with code "MISSING_REQUIRED_FIELD"
    And the error message identifies the missing field
    And no artifact is created

  Scenario: Reject empty configuration
    Given I have an empty draft configuration
    When I attempt to publish the configuration
    Then the publish operation fails
    And I receive a validation error with code "EMPTY_CONFIG"
    And no artifact is created
```

### Templates

**BDD Feature Template:**
```gherkin
@behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
@status:draft|ready|implemented
Feature: {Feature Name}
  As a {role/persona}
  I want {goal}
  So that {benefit}

  Background:
    Given {common setup for all scenarios}
    And {additional setup}

  Scenario: {Happy path scenario name}
    Given {precondition 1}
    And {precondition 2}
    When {action taken}
    Then {expected outcome}
    And {additional assertion}
    And {another assertion}

  Scenario: {Error case scenario name}
    Given {error condition}
    When {action taken}
    Then {error behavior}
    And {error details provided}
    And {system state unchanged}

  Scenario: {Edge case scenario name}
    Given {boundary condition}
    When {action taken}
    Then {expected edge behavior}
```

**BDD Specification Checklist:**
- [ ] All behaviors from capability spec covered
- [ ] Happy path scenarios written
- [ ] Error scenarios written
- [ ] Edge cases identified and specified
- [ ] @behavior and @status tags present
- [ ] Gherkin syntax valid (Given/When/Then)
- [ ] Scenarios are testable (concrete, measurable)
- [ ] File created: `project-docs/capabilities/behaviors/{capability}.feature`

---

## Phase 3: Value Scenarios (Living Documentation)

### Purpose
Create **user-facing documentation** that doubles as **E2E tests**, ensuring docs stay synchronized with code.

### Inputs
- BDD feature specification
- User workflows identified

### Outputs
- **How-To Guide** (`user-docs/how-to/{guide-name}.md`)
- **E2E Test** (`tests/value-scenarios/test_{scenario}.py`)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│       PHASE 3: VALUE SCENARIOS (Living Documentation)        │
└─────────────────────────────────────────────────────────────┘

1. WRITE HOW-TO GUIDE (User-Facing)
   ↓
   Structure (Diátaxis):
   • Goal: What this guide accomplishes
   • Audience: Who is this for
   • Prerequisites: Required setup
   • Step-by-step instructions
   • Code examples with expected output
   • Troubleshooting section
   ↓
2. WRITE E2E TEST (Validates Guide)
   ↓
   Test structure:
   • Docstring: Links to how-to guide
   • Test steps: Mirror guide steps EXACTLY
   • Assertions: Validate expected outcomes
   • Cleanup: Ensure test isolation
   ↓
3. ENSURE SYNCHRONIZATION
   ↓
   Key principle:
   • E2E test EXECUTES the how-to guide
   • If guide is wrong, test fails
   • If code breaks, test fails → guide needs update
   • Documentation IS the test specification
   ↓
4. ADD CROSS-REFERENCES
   ↓
   Link chain:
   • Capability spec → How-to guide
   • How-to guide → E2E test
   • E2E test → BDD scenarios
   • BDD scenarios → Capability spec
   (Full traceability)
```

### Example: Publish Config How-To + E2E Test

**How-To Guide:** `user-docs/how-to/publish-config.md`

```markdown
# How-To: Publish MCP Configuration

**Goal:** Publish a validated MCP configuration as a signed artifact
**Audience:** MCP users managing configurations
**Prerequisites:**
- mcp-orchestration installed
- Signing keys initialized

## Steps

### Step 1: Initialize Storage
```bash
mcp-orchestration-init
```

**Expected output:**
```
✅ Storage initialized at ~/.mcp-orchestration/
✅ Signing keys created
```

### Step 2: Add Servers to Draft
```bash
# Add filesystem server
mcp-orchestration-add-server \
  --client claude-desktop \
  --server-id filesystem \
  --env "ROOT_PATH=/Users/yourname/Documents"
```

### Step 3: Validate Configuration
Use the `validate_config` MCP tool to check for errors...

[... rest of guide ...]
```

**E2E Test:** `tests/value-scenarios/test_publish_config.py`

```python
def test_value_scenario_full_publish_workflow():
    """E2E test that executes the publish-config.md how-to guide.

    This test validates the complete user workflow documented in
    user-docs/how-to/publish-config.md

    References:
    - Capability: project-docs/capabilities/config-publishing.md
    - Behavior: @behavior:MCP.CONFIG.PUBLISH
    - How-To: user-docs/how-to/publish-config.md
    """
    # Step 1: Initialize storage (from guide)
    storage_path = tmp_path / "storage"
    init_storage(storage_path)
    assert (storage_path / "keys" / "signing.key").exists()

    # Step 2: Add servers to draft (from guide)
    builder = ConfigBuilder()
    builder.add_server(
        server_id="filesystem",
        env={"ROOT_PATH": "/Users/test/Documents"}
    )

    # Step 3: Validate configuration (from guide)
    result = validate_config(
        client_id="claude-desktop",
        profile_id="default",
        payload=builder.build()
    )
    assert result["is_valid"] is True

    # Step 4: Publish configuration (from guide)
    publish_result = publish_config(
        client_id="claude-desktop",
        profile_id="default",
        changelog="Initial setup"
    )
    assert publish_result["status"] == "success"
    assert "artifact_id" in publish_result

    # Verify artifact exists (from guide expectations)
    artifact = get_artifact(publish_result["artifact_id"])
    assert artifact.metadata["changelog"] == "Initial setup"
```

### Templates

**How-To Guide Template:**
```markdown
# How-To: {Task Name}

**Goal:** {Specific outcome user will achieve}
**Audience:** {Target user persona}
**Prerequisites:**
- {Requirement 1}
- {Requirement 2}

## Overview
{Brief 2-3 sentence summary of what this guide does}

## Steps

### Step 1: {Action Name}
{Instructions for this step}

```bash
# Example command
{command with real example values}
```

**Expected output:**
```
{Sample output user should see}
```

**Why this step:** {Brief explanation of purpose}

### Step 2: {Next Action}
{Continue for each step...}

## Verification
{How to verify the task completed successfully}

## Troubleshooting

**Problem:** {Common issue}
**Solution:** {How to fix}

**Problem:** {Another common issue}
**Solution:** {How to fix}

## Next Steps
- {Related guide or next action}

## Related Documentation
- [Link to reference docs]
- [Link to explanation]
```

**E2E Test Template:**
```python
def test_value_scenario_{scenario_name}():
    """E2E test that executes the {guide-name}.md how-to guide.

    This test validates the complete user workflow documented in
    user-docs/how-to/{guide-name}.md

    References:
    - Capability: project-docs/capabilities/{capability}.md
    - Behavior: @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION}
    - How-To: user-docs/how-to/{guide-name}.md
    """
    # Step 1: {Description from guide}
    # {Code that executes step 1}
    assert {expected outcome from guide}

    # Step 2: {Description from guide}
    # {Code that executes step 2}
    assert {expected outcome from guide}

    # Continue for all steps in guide...

    # Final verification
    assert {overall success condition}
```

**Value Scenario Checklist:**
- [ ] How-to guide written (Diátaxis format)
- [ ] Guide includes goal, audience, prerequisites
- [ ] Step-by-step instructions with examples
- [ ] Expected outputs documented
- [ ] Troubleshooting section included
- [ ] E2E test written
- [ ] E2E test mirrors guide steps EXACTLY
- [ ] E2E test references capability, behavior, guide
- [ ] Test passes (validates guide works)
- [ ] Cross-references added to capability spec

---

## Phase 4: Test-Driven Development (TDD)

### Purpose
Write **unit tests BEFORE implementation** to drive design and ensure correctness.

### Inputs
- BDD scenarios (from Phase 2)
- Value scenarios (from Phase 3)

### Outputs
- **Unit Tests** (`tests/test_{module}.py`) - Initially FAILING (RED)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│         PHASE 4: TEST-DRIVEN DEVELOPMENT (TDD)               │
│                  RED → GREEN → REFACTOR                      │
└─────────────────────────────────────────────────────────────┘

                   ┌──────────────┐
                   │     RED      │
                   │ Write Failing│
                   │    Tests     │
                   └──────┬───────┘
                          │
                          ↓
                   ┌──────────────┐
                   │    GREEN     │
                   │  Implement   │
                   │  to Pass     │
                   └──────┬───────┘
                          │
                          ↓
                   ┌──────────────┐
                   │  REFACTOR    │
                   │  Clean Code  │
                   │  & Tests     │
                   └──────┬───────┘
                          │
                          └──────► Next feature
                                   (repeat cycle)

DETAILED RED PHASE:
1. CREATE TEST FILE
   tests/test_{module}.py
   ↓
2. WRITE TEST CLASS
   class Test{Capability}{Scenario}:
   ↓
3. WRITE TEST METHODS (From BDD scenarios)
   • def test_{happy_path}()
   • def test_{error_case}()
   • def test_{edge_case}()
   ↓
4. RUN TESTS → SHOULD FAIL
   pytest tests/test_{module}.py
   ↓
   Expected: All tests FAIL (code doesn't exist yet)
   If tests pass → BUG in tests!
```

### Example: PublishingWorkflow TDD

**Test File:** `tests/test_publishing_workflow.py`

```python
"""Tests for PublishingWorkflow (Wave 1.4).

This module tests the configuration publishing workflow following
BDD scenarios from project-docs/capabilities/behaviors/mcp-config-publish.feature
"""

import pytest
from mcp_orchestrator.publishing.workflow import (
    PublishingWorkflow,
    ValidationError,
)

class TestPublishWorkflow:
    """Test publishing workflow integration."""

    def test_publish_valid_config_creates_signed_artifact(self):
        """Test @behavior:MCP.CONFIG.PUBLISH - happy path.

        Scenario: Successfully publish valid configuration
        Given I have a valid draft configuration
        When I publish with changelog
        Then a signed artifact is created
        """
        # Arrange
        workflow = PublishingWorkflow()
        payload = {"mcpServers": {"filesystem": {...}}}

        # Act
        result = workflow.publish(
            client_id="claude-desktop",
            profile_id="default",
            payload=payload,
            changelog="Initial setup"
        )

        # Assert
        assert result.status == "success"
        assert result.artifact_id.startswith("sha256:")
        assert result.metadata["changelog"] == "Initial setup"

    def test_publish_invalid_config_raises_validation_error(self):
        """Test @behavior:MCP.CONFIG.PUBLISH - error case.

        Scenario: Reject publishing invalid configuration
        Given I have invalid draft configuration
        When I attempt to publish
        Then ValidationError is raised
        """
        # Arrange
        workflow = PublishingWorkflow()
        payload = {"mcpServers": {}}  # Empty - invalid

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            workflow.publish(
                client_id="claude-desktop",
                profile_id="default",
                payload=payload,
                changelog="Should fail"
            )

        assert "EMPTY_CONFIG" in str(exc_info.value)
```

**Running Tests (RED Phase):**
```bash
$ pytest tests/test_publishing_workflow.py

tests/test_publishing_workflow.py::TestPublishWorkflow::test_publish_valid_config_creates_signed_artifact FAILED
tests/test_publishing_workflow.py::TestPublishWorkflow::test_publish_invalid_config_raises_validation_error FAILED

======================== 2 failed in 0.05s =========================
ERRORS:
ModuleNotFoundError: No module named 'mcp_orchestrator.publishing.workflow'

✅ EXPECTED! Tests fail because code doesn't exist yet.
```

### Templates

**Unit Test Template:**
```python
"""Tests for {module} (Wave X.Y).

This module tests {functionality} following BDD scenarios from
project-docs/capabilities/behaviors/{feature}.feature
"""

import pytest
from mcp_orchestrator.{module} import {ClassUnderTest}

class Test{Capability}{Scenario}:
    """Test {scenario description}."""

    def test_{happy_path_description}(self):
        """Test @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION} - happy path.

        Scenario: {BDD scenario name}
        Given {precondition}
        When {action}
        Then {expected outcome}
        """
        # Arrange
        {setup test data}

        # Act
        result = {call method under test}

        # Assert
        assert {expected condition 1}
        assert {expected condition 2}

    def test_{error_case_description}(self):
        """Test @behavior:{NAMESPACE}.{CAPABILITY}.{ACTION} - error case.

        Scenario: {BDD error scenario}
        Given {error condition}
        When {action}
        Then {error raised}
        """
        # Arrange
        {setup error condition}

        # Act & Assert
        with pytest.raises({ExpectedException}) as exc_info:
            {call method that should fail}

        assert "{expected error message}" in str(exc_info.value)

    @pytest.fixture
    def {fixture_name}(self):
        """Fixture for {reusable test data}."""
        {return test data}
```

**TDD Checklist (RED Phase):**
- [ ] Test file created: `tests/test_{module}.py`
- [ ] Test class created for each scenario
- [ ] Happy path test written
- [ ] Error case tests written
- [ ] Edge case tests written
- [ ] Tests reference BDD scenarios in docstrings
- [ ] Arrange-Act-Assert pattern used
- [ ] Tests run: `pytest tests/test_{module}.py`
- [ ] All tests FAIL (RED) ✅ Expected!
- [ ] Ready to implement (Phase 5 - GREEN)

---

## Phase 5: Implementation

### Purpose
Write **minimum code to make tests pass** (GREEN), following the domain model.

### Inputs
- Failing unit tests (RED)
- Capability specification (domain model)

### Outputs
- **Implementation Code** (`src/mcp_orchestrator/{module}/`)
- **Tests Passing** (GREEN)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│              PHASE 5: IMPLEMENTATION (GREEN)                 │
└─────────────────────────────────────────────────────────────┘

1. FOLLOW DOMAIN MODEL
   ↓
   From capability spec:
   • Entities (objects with identity)
   • Value Objects (immutable)
   • Services (domain logic)
   • Repositories (storage)
   ↓
2. IMPLEMENT MINIMUM CODE
   ↓
   Principle: YAGNI (You Aren't Gonna Need It)
   • Only code to pass current tests
   • No speculative features
   • Simplest solution first
   ↓
3. RUN TESTS FREQUENTLY
   ↓
   After each small change:
   pytest tests/test_{module}.py
   ↓
   Goal: See tests turn GREEN one by one
   ↓
4. ACHIEVE GREEN STATE
   ↓
   Success: All tests pass
   ✅ All tests GREEN
   ✅ Coverage ≥70% (for new code)
   ↓
5. REFACTOR (Next phase)
```

### Example: PublishingWorkflow Implementation

**File:** `src/mcp_orchestrator/publishing/workflow.py`

```python
"""Publishing workflow for MCP configurations.

This module implements the PublishingWorkflow service that orchestrates
validation → signing → storage operations.

Domain Model (DDD):
- Service: PublishingWorkflow
- Entities: ConfigArtifact
- Value Objects: ValidationResult, PublishResult
- Repositories: ArtifactStore
"""

from dataclasses import dataclass
from typing import Any

from mcp_orchestrator.crypto import sign_artifact
from mcp_orchestrator.storage import ArtifactStore
from mcp_orchestrator.validation import validate_config


class ValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


@dataclass
class PublishResult:
    """Result of publishing operation (Value Object)."""
    status: str
    artifact_id: str
    metadata: dict[str, Any]


class PublishingWorkflow:
    """Service: Orchestrates publishing workflow.

    Workflow: draft → validate → sign → store → update index
    """

    def __init__(self):
        self.store = ArtifactStore()

    def publish(
        self,
        client_id: str,
        profile_id: str,
        payload: dict[str, Any],
        changelog: str,
    ) -> PublishResult:
        """Publish configuration with validation.

        Args:
            client_id: Client identifier
            profile_id: Profile identifier
            payload: Configuration payload
            changelog: Change description

        Returns:
            PublishResult with artifact_id and metadata

        Raises:
            ValidationError: If validation fails
        """
        # Step 1: Validate
        validation = validate_config(client_id, profile_id, payload)
        if not validation["is_valid"]:
            raise ValidationError(
                f"EMPTY_CONFIG: {validation['errors']}"
            )

        # Step 2: Enrich metadata
        metadata = {
            "changelog": changelog,
            "generator": "mcp-orchestration",
            "server_count": len(payload.get("mcpServers", {})),
        }

        # Step 3: Sign
        artifact = sign_artifact(payload, metadata)

        # Step 4: Store
        self.store.save(artifact)

        # Step 5: Update index
        self.store.update_profile_index(
            client_id, profile_id, artifact.artifact_id
        )

        return PublishResult(
            status="success",
            artifact_id=artifact.artifact_id,
            metadata=metadata,
        )
```

**Running Tests (GREEN Phase):**
```bash
$ pytest tests/test_publishing_workflow.py

tests/test_publishing_workflow.py::TestPublishWorkflow::test_publish_valid_config_creates_signed_artifact PASSED
tests/test_publishing_workflow.py::TestPublishWorkflow::test_publish_invalid_config_raises_validation_error PASSED

======================== 2 passed in 0.12s =========================

✅ GREEN! All tests pass.
```

### Implementation Guidelines

**DDD Principles:**
- **Entities** - Objects with identity (e.g., `ConfigArtifact`)
  - Have unique ID
  - Mutable state (but prefer immutability)
  - Lifecycle management
- **Value Objects** - Immutable objects (e.g., `ValidationResult`)
  - No identity
  - Defined by values
  - Immutable (use `@dataclass(frozen=True)`)
- **Aggregates** - Clusters of entities (e.g., `Config + Servers`)
  - Consistency boundary
  - One entity is aggregate root
- **Services** - Domain logic (e.g., `PublishingWorkflow`)
  - Stateless operations
  - Coordinates entities/repositories
- **Repositories** - Storage abstractions (e.g., `ArtifactStore`)
  - Hide persistence details
  - Return domain objects

**Code Quality:**
- Use type hints on all functions
- Add docstrings (Google/NumPy style)
- Keep functions < 20 lines
- Single responsibility per class
- Avoid deep nesting (max 3-4 levels)

### Implementation Checklist:
- [ ] Module created: `src/mcp_orchestrator/{module}/`
- [ ] Domain model followed (entities, services, etc.)
- [ ] Type hints on all public APIs
- [ ] Docstrings on all public APIs
- [ ] Minimum code to pass tests (YAGNI)
- [ ] Tests run: `pytest tests/test_{module}.py`
- [ ] All tests PASS (GREEN) ✅
- [ ] Ready to refactor (Phase 6)

---

## Phase 6: Integration & Wiring

### Purpose
Connect implemented modules to the system (CLI, MCP server, module exports).

### Inputs
- Passing unit tests (GREEN)
- Domain modules implemented

### Outputs
- **CLI Commands** (`src/mcp_orchestrator/cli_{command}.py`)
- **MCP Tools** (updated `src/mcp_orchestrator/mcp/server.py`)
- **Module Exports** (`__init__.py` files)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│            PHASE 6: INTEGRATION & WIRING                     │
└─────────────────────────────────────────────────────────────┘

1. ADD CLI COMMANDS
   ↓
   Create: src/mcp_orchestrator/cli_{command}.py
   • Define argparse arguments
   • Call domain service
   • Format output (text/JSON)
   • Add to pyproject.toml [project.scripts]
   ↓
2. ADD MCP TOOLS
   ↓
   Update: src/mcp_orchestrator/mcp/server.py
   • @mcp.tool() decorator
   • Input schema (Pydantic)
   • Call domain service
   • Return MCP-compliant response
   ↓
3. UPDATE MODULE EXPORTS
   ↓
   Update: src/mcp_orchestrator/{module}/__init__.py
   • Export public classes
   • Export public functions
   • Hide private implementation
   ↓
4. RUN INTEGRATION TESTS
   ↓
   pytest tests/integration/
   ↓
5. RUN E2E VALUE SCENARIOS
   ↓
   pytest tests/value-scenarios/
```

### Example: Publishing Integration

**1. CLI Command:**

**File:** `src/mcp_orchestrator/cli_publishing.py`

```python
"""CLI command for publishing configurations."""

import argparse
import json
from pathlib import Path

from mcp_orchestrator.publishing.workflow import PublishingWorkflow


def publish_config():
    """CLI entry point for publishing configurations."""
    parser = argparse.ArgumentParser(
        description="Publish MCP configuration"
    )
    parser.add_argument("--client", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--changelog", required=True)
    parser.add_argument("--format", choices=["text", "json"], default="text")

    args = parser.parse_args()

    # Load payload from file
    with open(args.file) as f:
        payload = json.load(f)

    # Publish
    workflow = PublishingWorkflow()
    result = workflow.publish(
        client_id=args.client,
        profile_id=args.profile,
        payload=payload,
        changelog=args.changelog,
    )

    # Output
    if args.format == "json":
        print(json.dumps({
            "status": result.status,
            "artifact_id": result.artifact_id,
            "metadata": result.metadata,
        }))
    else:
        print(f"✅ Published successfully")
        print(f"Artifact ID: {result.artifact_id}")
        print(f"Changelog: {result.metadata['changelog']}")
```

**Update:** `pyproject.toml`

```toml
[project.scripts]
mcp-orchestration-publish-config = "mcp_orchestrator.cli_publishing:publish_config"
```

**2. MCP Tool:**

**File:** `src/mcp_orchestrator/mcp/server.py` (update)

```python
from mcp_orchestrator.publishing.workflow import PublishingWorkflow

@mcp.tool()
async def publish_config(
    client_id: str = "claude-desktop",
    profile_id: str = "default",
    changelog: str = "Configuration update",
) -> dict[str, Any]:
    """Publish draft configuration as signed artifact.

    Args:
        client_id: Client identifier (default: claude-desktop)
        profile_id: Profile identifier (default: default)
        changelog: Change description for artifact metadata

    Returns:
        - status: "success" or "error"
        - artifact_id: Published artifact identifier
        - metadata: Artifact metadata (changelog, generator, etc.)
    """
    workflow = PublishingWorkflow()
    builder = get_draft_builder(client_id, profile_id)

    result = workflow.publish(
        client_id=client_id,
        profile_id=profile_id,
        payload=builder.build(),
        changelog=changelog,
    )

    return {
        "status": result.status,
        "artifact_id": result.artifact_id,
        "metadata": result.metadata,
    }
```

**3. Module Exports:**

**File:** `src/mcp_orchestrator/publishing/__init__.py`

```python
"""Publishing module for MCP configurations."""

from .workflow import PublishingWorkflow, PublishResult, ValidationError

__all__ = ["PublishingWorkflow", "PublishResult", "ValidationError"]
```

### Integration Checklist:
- [ ] CLI command created (if applicable)
- [ ] CLI added to pyproject.toml [project.scripts]
- [ ] MCP tool added/updated (if applicable)
- [ ] Module exports updated (__init__.py)
- [ ] Integration tests pass
- [ ] E2E value scenarios pass
- [ ] CLI tested manually: `mcp-orchestration-{command} --help`
- [ ] MCP tool tested in Claude Desktop (if applicable)

---

## Phase 7: Documentation & Quality Gates

### Purpose
Ensure **documentation is complete** and **all quality gates pass** before release.

### Inputs
- Integrated system (from Phase 6)
- How-to guides (from Phase 3)

### Outputs
- **API Reference** (updated)
- **CHANGELOG.md** (updated)
- **Quality Report** (all gates GREEN)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│         PHASE 7: DOCUMENTATION & QUALITY GATES               │
└─────────────────────────────────────────────────────────────┘

1. UPDATE API REFERENCE
   ↓
   File: user-docs/reference/{api-docs}.md
   • Document new MCP tools
   • Document new CLI commands
   • Add usage examples
   • Cross-reference to how-to guides
   ↓
2. UPDATE CHANGELOG
   ↓
   File: CHANGELOG.md
   • Add entry under ## [Unreleased]
   • Section: ### Added / ### Changed / ### Fixed
   • Link to issues/PRs
   • Follow Keep a Changelog format
   ↓
3. RUN QUALITY GATES
   ↓
   Command: just pre-merge
   ↓
   Gates:
   ✅ Linting (ruff check)
   ✅ Formatting (ruff format --check)
   ✅ Type checking (mypy)
   ✅ Tests (pytest)
   ✅ Coverage (≥85%)
   ✅ Pre-commit hooks
   ↓
4. UPDATE WAVE PLAN
   ↓
   File: project-docs/WAVE_1X_PLAN.md
   • Mark deliverables complete
   • Update status to "Complete"
   • Add completion date
   ↓
5. FINAL REVIEW
   ↓
   Checklist:
   • All tests passing
   • Documentation complete
   • No uncommitted changes
   • Ready to release
```

### Example: Quality Gates Execution

```bash
$ just pre-merge

Running pre-merge checks...

1. Linting (ruff)...
✅ All checks passed!

2. Formatting (ruff format)...
✅ Code is formatted correctly

3. Type checking (mypy)...
✅ Type checking passed (0 errors)

4. Tests (pytest)...
======================== test session starts =========================
collected 167 items

tests/test_crypto.py ................                    [  9%]
tests/test_storage.py ...............                    [ 18%]
tests/test_publishing_workflow.py ..........             [ 24%]
tests/value-scenarios/test_publish_config.py ...         [ 26%]
...

======================== 167 passed in 4.23s =========================

5. Coverage...
---------- coverage: platform darwin, python 3.12.0 -----------
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
src/mcp_orchestrator/__init__.py            12      0   100%
src/mcp_orchestrator/publishing.py          45      3    93%
src/mcp_orchestrator/workflow.py            67      5    93%
...
------------------------------------------------------------
TOTAL                                      1245     78    94%

✅ Coverage: 94% (required: ≥85%)

6. Pre-commit hooks...
Trim Trailing Whitespace.................................Passed
Fix End of Files.........................................Passed
Check Yaml...............................................Passed
Check for added large files..............................Passed

✅ All quality gates PASSED!
```

### CHANGELOG.md Update

**File:** `CHANGELOG.md`

```markdown
## [Unreleased]

### Added
- **Configuration Publishing Workflow** (Wave 1.4):
  - `PublishingWorkflow` service for validated publishing
  - `validate_config` MCP tool for pre-publish validation
  - `publish_config` MCP tool with integrated validation
  - `mcp-orchestration-publish-config` CLI command
  - Metadata enrichment (generator, changelog, server_count)

### Changed
- Enhanced `publish_config` MCP tool to use `PublishingWorkflow`
- Updated workflow documentation: browse → add → view → validate → publish

### Fixed
- (Any bug fixes in this wave)
```

### Quality Gates Checklist:
- [ ] API reference updated (`user-docs/reference/`)
- [ ] CHANGELOG.md updated (under `## [Unreleased]`)
- [ ] Quality gates run: `just pre-merge`
- [ ] Linting passed (ruff check)
- [ ] Formatting passed (ruff format --check)
- [ ] Type checking passed (mypy)
- [ ] All tests passed (pytest)
- [ ] Coverage ≥85%
- [ ] Pre-commit hooks passed
- [ ] Wave plan updated (mark deliverables complete)
- [ ] No uncommitted changes
- [ ] Ready to release ✅

---

## Phase 8: Release Publishing

### Purpose
Publish the release to **production** (Git tag, PyPI package).

### Inputs
- All quality gates passed
- CHANGELOG.md updated
- Wave deliverables complete

### Outputs
- **Git Tag** (`v0.1.X`)
- **PyPI Package** (published)
- **GitHub Release** (notes)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│              PHASE 8: RELEASE PUBLISHING                     │
└─────────────────────────────────────────────────────────────┘

1. PREPARE RELEASE
   ↓
   Command: just prepare-release [patch|minor|major]
   ↓
   Actions:
   • Bump version in pyproject.toml
   • Update CHANGELOG.md (move Unreleased → vX.Y.Z)
   • Add release date
   • Create git commit
   ↓
2. CREATE GIT TAG
   ↓
   git tag -a v0.1.4 -m "Release v0.1.4: Config Publishing"
   git push origin v0.1.4
   ↓
3. BUILD DISTRIBUTION
   ↓
   Command: just build
   ↓
   Creates:
   • dist/mcp_orchestration-0.1.4-py3-none-any.whl
   • dist/mcp-orchestration-0.1.4.tar.gz
   ↓
4. PUBLISH TO PyPI
   ↓
   Test first:
   just publish-test  # TestPyPI
   ↓
   Then production:
   just publish-prod  # PyPI
   ↓
5. CREATE GITHUB RELEASE
   ↓
   • Go to GitHub Releases
   • Create release from tag v0.1.4
   • Copy CHANGELOG entry as description
   • Attach wheel/tarball files
   • Publish release
   ↓
6. VERIFY INSTALLATION
   ↓
   pip install mcp-orchestration==0.1.4
   mcp-orchestration --version
   ↓
   Expected: v0.1.4
```

### Example: Release Workflow

**Step 1: Prepare Release**

```bash
$ just prepare-release patch

Preparing patch release...

Current version: 0.1.3
New version: 0.1.4

Updating pyproject.toml...
Updating CHANGELOG.md...

## [0.1.4] - 2025-10-25

### Added
- Configuration Publishing Workflow (Wave 1.4)
  - PublishingWorkflow service
  - validate_config MCP tool
  - publish_config enhanced with validation
  - CLI: mcp-orchestration-publish-config
...

Created commit: "chore: release v0.1.4"
Created tag: v0.1.4

Next steps:
  git push origin main
  git push origin v0.1.4
  just publish-prod
```

**Step 2: Push to GitHub**

```bash
$ git push origin main
$ git push origin v0.1.4

To https://github.com/liminalcommons/mcp-orchestration.git
 * [new tag]         v0.1.4 -> v0.1.4
```

**Step 3: Build Distribution**

```bash
$ just build

Building distribution packages...

Building wheel...
Built mcp_orchestration-0.1.4-py3-none-any.whl

Building source distribution...
Built mcp-orchestration-0.1.4.tar.gz

Files created:
  dist/mcp_orchestration-0.1.4-py3-none-any.whl (45 KB)
  dist/mcp-orchestration-0.1.4.tar.gz (38 KB)

✅ Build complete!
```

**Step 4: Publish to PyPI**

```bash
# Test on TestPyPI first
$ just publish-test

Publishing to TestPyPI...
Uploading distributions to https://test.pypi.org/legacy/
Uploading mcp_orchestration-0.1.4-py3-none-any.whl
Uploading mcp-orchestration-0.1.4.tar.gz

View at: https://test.pypi.org/project/mcp-orchestration/0.1.4/

✅ Test publish successful!

# If test works, publish to production PyPI
$ just publish-prod

Publishing to PyPI...
Uploading distributions to https://upload.pypi.org/legacy/
Uploading mcp_orchestration-0.1.4-py3-none-any.whl
Uploading mcp-orchestration-0.1.4.tar.gz

✅ Published to PyPI!
View at: https://pypi.org/project/mcp-orchestration/0.1.4/
```

**Step 5: Create GitHub Release**

On GitHub:
1. Go to **Releases** → **Draft a new release**
2. Choose tag: `v0.1.4`
3. Release title: `v0.1.4 - Configuration Publishing Workflow`
4. Description: Copy from CHANGELOG.md
5. Attach files: `mcp_orchestration-0.1.4-py3-none-any.whl`, `mcp-orchestration-0.1.4.tar.gz`
6. Click **Publish release**

**Step 6: Verify Installation**

```bash
# Install from PyPI
$ pip install mcp-orchestration==0.1.4

Collecting mcp-orchestration==0.1.4
  Downloading mcp_orchestration-0.1.4-py3-none-any.whl (45 kB)
Installing collected packages: mcp-orchestration
Successfully installed mcp-orchestration-0.1.4

# Verify version
$ mcp-orchestration --version
mcp-orchestration v0.1.4

✅ Release verified!
```

### Release Checklist:
- [ ] All quality gates passed (from Phase 7)
- [ ] CHANGELOG.md finalized
- [ ] Version bumped: `just prepare-release [patch|minor|major]`
- [ ] Git commit created
- [ ] Git tag created: `v0.1.X`
- [ ] Pushed to GitHub: `git push origin main && git push origin v0.1.X`
- [ ] Distribution built: `just build`
- [ ] Published to TestPyPI: `just publish-test` (verify install)
- [ ] Published to PyPI: `just publish-prod`
- [ ] GitHub release created
- [ ] Installation verified: `pip install mcp-orchestration==0.1.X`
- [ ] Version command works: `mcp-orchestration --version`
- [ ] Announce release (blog, social media, email)

---

## Phase 9: Feedback & Iteration

### Purpose
**Monitor production usage**, gather feedback, and feed learnings back into the next wave.

### Inputs
- Released version (in production)
- User feedback
- Metrics & telemetry

### Outputs
- **Bug reports** (GitHub Issues)
- **Feature requests** (GitHub Issues)
- **Usage metrics** (analytics)
- **Knowledge notes** (learnings for next wave)

### Process

```
┌─────────────────────────────────────────────────────────────┐
│           PHASE 9: FEEDBACK & ITERATION                      │
└─────────────────────────────────────────────────────────────┘

1. MONITOR PRODUCTION
   ↓
   Metrics to track:
   • Installation count (PyPI downloads)
   • Error rates (if telemetry enabled)
   • User engagement (MCP tool usage)
   • Performance metrics
   ↓
2. GATHER FEEDBACK
   ↓
   Sources:
   • GitHub Issues (bugs, features)
   • GitHub Discussions (questions, ideas)
   • User interviews (direct feedback)
   • Support requests (email, chat)
   ↓
3. TRIAGE & PRIORITIZE
   ↓
   Categorize feedback:
   • 🔴 Critical bugs (hotfix needed)
   • 🟡 Non-critical bugs (patch release)
   • 🟢 Feature requests (next wave)
   • 💡 Ideas (backlog)
   ↓
4. HOTFIX IF NEEDED
   ↓
   Critical bugs:
   • Create hotfix branch
   • Fix + test
   • Release patch version (v0.1.4 → v0.1.5)
   ↓
5. CAPTURE LEARNINGS
   ↓
   Knowledge notes:
   • What worked well?
   • What didn't work?
   • What would we do differently?
   • User pain points
   ↓
6. PLAN NEXT WAVE
   ↓
   Feed learnings into Phase 0:
   • Update ROADMAP.md
   • Adjust priorities based on feedback
   • Plan next wave (Wave 1.5, 2.0, etc.)
   ↓
   └──► Back to Phase 0 (Vision & Planning)
```

### Example: Feedback Analysis

**Feedback Summary (Week 1 after v0.1.4 release):**

```markdown
## v0.1.4 Feedback Summary (Week 1)

### Metrics
- **PyPI Downloads:** 342 (up 15% from v0.1.3)
- **GitHub Stars:** +12
- **Issues Opened:** 8 (5 bugs, 3 feature requests)

### Bug Reports
1. **Critical:** publish_config fails with large configs (>100KB) [#45]
   - Impact: High (blocks publishing for 10% of users)
   - Fix: Increase payload size limit
   - Release: Hotfix v0.1.5

2. **Non-critical:** Validation error messages unclear [#46]
   - Impact: Medium (UX issue)
   - Fix: Improve error messages
   - Release: Patch v0.1.6

### Feature Requests
1. **High demand:** Support for rollback to previous config [#47]
   - User value: High
   - Complexity: Medium
   - Plan: Add to Wave 1.5

2. **Medium demand:** Export config to YAML format [#48]
   - User value: Medium
   - Complexity: Low
   - Plan: Add to Wave 1.5

### Learnings
✅ **What worked:**
- Validation before publish caught 90% of user errors
- How-to guide was comprehensive (0 documentation questions)
- E2E tests caught 3 bugs before release

❌ **What didn't work:**
- Didn't test with large payloads (edge case missed)
- Error messages too technical for non-developers
- CLI --help text unclear on changelog format

🔄 **For next wave:**
- Add payload size tests (edge cases)
- User-test error messages with non-technical users
- Improve CLI help text based on user questions
```

### Feedback Checklist:
- [ ] Monitoring dashboard set up (if applicable)
- [ ] PyPI download metrics tracked
- [ ] GitHub Issues triaged weekly
- [ ] User feedback collected (interviews, surveys)
- [ ] Critical bugs identified and hotfixed
- [ ] Non-critical bugs added to next patch backlog
- [ ] Feature requests prioritized and planned
- [ ] Knowledge notes created (learnings)
- [ ] Feedback fed into next wave planning
- [ ] ROADMAP.md updated based on learnings

---

## Process Integration Map

### How All Processes Connect

```
┌─────────────────────────────────────────────────────────────────┐
│                  PROCESS INTEGRATION MAP                         │
│         (How Vision, DDD, BDD, TDD, Waves all connect)          │
└─────────────────────────────────────────────────────────────────┘

STRATEGIC LEVEL (Quarters/Months)
    ↓
┌──────────────────────────────┐
│   Vision Documents           │ ← dev-docs/vision/
│   (Long-term direction)      │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   ROADMAP.md                 │ ← Committed features
│   (High-level plan)          │
└──────────────┬───────────────┘
               ↓
TACTICAL LEVEL (Weeks)
    ↓
┌──────────────────────────────┐
│   WAVE_1X_PLAN.md            │ ← Incremental delivery
│   (Wave-based planning)      │    (3-5 capabilities per wave)
└──────────────┬───────────────┘
               ↓
OPERATIONAL LEVEL (Days)
    ↓
┌──────────────────────────────┐
│   Capability Specs           │ ← project-docs/capabilities/
│   (DDD - Domain modeling)    │    (Domain model + behaviors)
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   BDD Scenarios              │ ← project-docs/capabilities/behaviors/
│   (Given/When/Then)          │    (Executable specs)
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Value Scenarios            │ ← user-docs/how-to/ + tests/value-scenarios/
│   (How-To + E2E tests)       │    (Living documentation)
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Unit Tests (TDD)           │ ← tests/test_*.py
│   (RED → GREEN → REFACTOR)   │    (Test-first development)
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Implementation             │ ← src/mcp_orchestrator/
│   (Domain code)              │    (Entities, Services, etc.)
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Integration                │ ← CLI, MCP tools, module exports
│   (System wiring)            │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Release                    │ ← Git tag, PyPI, GitHub Release
│   (Publish to production)    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Feedback                   │ ← GitHub Issues, metrics, users
│   (Monitor & learn)          │
└──────────────┬───────────────┘
               │
               └──────► (Back to Vision/Roadmap for next wave)


TRACEABILITY CHAIN (Full lifecycle)

Vision Doc
  ↓ (informs)
Roadmap
  ↓ (breaks down into)
Wave Plan
  ↓ (specifies)
Capability Spec
  ↓ (defines behaviors)
BDD Scenarios
  ↓ (validates via)
How-To Guide + E2E Test
  ↓ (drives)
Unit Tests (TDD)
  ↓ (implements)
Domain Code
  ↓ (integrates to)
CLI + MCP Tools
  ↓ (releases as)
Git Tag + PyPI Package
  ↓ (monitored via)
Feedback & Metrics
  ↓ (feeds back to)
Vision Doc (next iteration)
```

### Key Integration Points

| From | To | Integration Mechanism |
|------|----|-----------------------|
| **Vision** | **Roadmap** | Strategic themes → Committed features |
| **Roadmap** | **Wave Plan** | High-level features → 3-5 capabilities per wave |
| **Wave Plan** | **Capability Spec** | Wave scope → Domain model + behaviors |
| **Capability Spec** | **BDD Scenarios** | Behaviors → Given/When/Then specs |
| **BDD Scenarios** | **Value Scenarios** | Scenarios → How-to guides + E2E tests |
| **Value Scenarios** | **Unit Tests** | E2E workflows → Granular test cases |
| **Unit Tests** | **Implementation** | Tests → Domain code (TDD) |
| **Implementation** | **Integration** | Modules → CLI/MCP/exports |
| **Integration** | **Release** | System → Git tag + PyPI |
| **Release** | **Feedback** | Production → Metrics + user reports |
| **Feedback** | **Vision** | Learnings → Next wave planning |

---

## Appendices

### Appendix A: Complete Checklist

**Master Checklist (Full Lifecycle)**

```
Phase 0: Strategic Vision ✅
  [ ] User needs identified
  [ ] Capabilities prioritized
  [ ] Wave scope defined (3-5 capabilities)
  [ ] Success criteria measurable
  [ ] Timeline estimated
  [ ] WAVE_1X_PLAN.md updated
  [ ] ROADMAP.md updated
  [ ] Stakeholders aligned

Phase 1: Capability Specification (DDD) ✅
  [ ] Domain model identified (entities, services, value objects)
  [ ] Behaviors defined with @behavior tags
  [ ] Value scenarios mapped
  [ ] Integrations documented (CLI, MCP, API)
  [ ] Success criteria defined
  [ ] File created: project-docs/capabilities/{name}.md

Phase 2: Behavior Specification (BDD) ✅
  [ ] All behaviors from capability spec covered
  [ ] Happy path scenarios written
  [ ] Error scenarios written
  [ ] Edge cases specified
  [ ] @behavior and @status tags present
  [ ] Gherkin syntax valid
  [ ] File created: project-docs/capabilities/behaviors/{name}.feature

Phase 3: Value Scenarios ✅
  [ ] How-to guide written (Diátaxis format)
  [ ] Guide includes: goal, audience, prerequisites, steps
  [ ] Expected outputs documented
  [ ] Troubleshooting section included
  [ ] E2E test written
  [ ] E2E test mirrors guide steps EXACTLY
  [ ] Test references capability, behavior, guide
  [ ] Test passes (validates guide works)
  [ ] Files created:
      - user-docs/how-to/{guide}.md
      - tests/value-scenarios/test_{scenario}.py

Phase 4: Test-Driven Development (RED) ✅
  [ ] Test file created: tests/test_{module}.py
  [ ] Test classes created for each scenario
  [ ] Happy path tests written
  [ ] Error case tests written
  [ ] Edge case tests written
  [ ] Tests reference BDD scenarios
  [ ] Arrange-Act-Assert pattern used
  [ ] Tests run and FAIL (RED state) ✅ Expected!

Phase 5: Implementation (GREEN) ✅
  [ ] Module created: src/mcp_orchestrator/{module}/
  [ ] Domain model followed (DDD principles)
  [ ] Type hints on all public APIs
  [ ] Docstrings on all public APIs
  [ ] Minimum code to pass tests (YAGNI)
  [ ] Tests run and PASS (GREEN state) ✅
  [ ] Coverage ≥85% for new code

Phase 6: Integration ✅
  [ ] CLI command created (if applicable)
  [ ] CLI added to pyproject.toml [project.scripts]
  [ ] MCP tool added/updated (if applicable)
  [ ] Module exports updated (__init__.py)
  [ ] Integration tests pass
  [ ] E2E value scenarios pass

Phase 7: Documentation & Quality Gates ✅
  [ ] API reference updated (user-docs/reference/)
  [ ] CHANGELOG.md updated (## [Unreleased])
  [ ] Quality gates run: just pre-merge
  [ ] Linting passed (ruff check)
  [ ] Formatting passed (ruff format --check)
  [ ] Type checking passed (mypy)
  [ ] All tests passed (pytest)
  [ ] Coverage ≥85%
  [ ] Pre-commit hooks passed
  [ ] Wave plan updated (mark complete)
  [ ] No uncommitted changes

Phase 8: Release Publishing ✅
  [ ] Version bumped: just prepare-release [patch|minor|major]
  [ ] Git commit created
  [ ] Git tag created: v0.1.X
  [ ] Pushed to GitHub
  [ ] Distribution built: just build
  [ ] Published to TestPyPI (verified)
  [ ] Published to PyPI
  [ ] GitHub release created
  [ ] Installation verified
  [ ] Release announced

Phase 9: Feedback & Iteration ✅
  [ ] Monitoring set up (if applicable)
  [ ] Metrics tracked (PyPI downloads, etc.)
  [ ] GitHub Issues triaged
  [ ] User feedback collected
  [ ] Critical bugs hotfixed
  [ ] Non-critical bugs backlogged
  [ ] Feature requests prioritized
  [ ] Knowledge notes created (learnings)
  [ ] Feedback fed into next wave
```

### Appendix B: Templates Library

**All templates used in this document:**

1. **Wave Planning Template** (Phase 0)
2. **Capability Specification Template** (Phase 1)
3. **BDD Feature Template** (Phase 2)
4. **How-To Guide Template** (Phase 3)
5. **E2E Test Template** (Phase 3)
6. **Unit Test Template** (Phase 4)
7. **CLI Command Template** (Phase 6)
8. **MCP Tool Template** (Phase 6)

See each phase section above for full template content.

### Appendix C: Tools Reference

**Key Commands by Phase:**

| Phase | Command | Purpose |
|-------|---------|---------|
| **Phase 0** | `cat ROADMAP.md` | Review strategic plan |
| **Phase 1** | N/A (manual) | Write capability spec |
| **Phase 2** | N/A (manual) | Write BDD scenarios |
| **Phase 3** | N/A (manual) | Write how-to + E2E test |
| **Phase 4** | `pytest tests/test_{module}.py` | Run tests (expect RED) |
| **Phase 5** | `pytest tests/test_{module}.py` | Run tests (expect GREEN) |
| **Phase 6** | `pytest tests/integration/` | Integration tests |
| **Phase 6** | `pytest tests/value-scenarios/` | E2E value scenarios |
| **Phase 7** | `just pre-merge` | All quality gates |
| **Phase 7** | `just lint` | Linting only |
| **Phase 7** | `just typecheck` | Type checking only |
| **Phase 7** | `just test` | Tests + coverage |
| **Phase 8** | `just prepare-release patch` | Version bump + changelog |
| **Phase 8** | `just build` | Build distribution |
| **Phase 8** | `just publish-test` | Publish to TestPyPI |
| **Phase 8** | `just publish-prod` | Publish to PyPI |
| **Phase 9** | N/A (monitoring) | Track metrics, feedback |

**Quick Reference:**
```bash
# Discovery
just --list              # Show all available commands

# Common workflows
just test                # Run test suite
just pre-merge           # Pre-PR validation (required)
just build               # Build distribution packages

# Release workflow
just prepare-release patch    # Bump version
just publish-test            # Test on TestPyPI
just publish-prod            # Publish to PyPI
```

### Appendix D: Documentation Cross-References

**Related Documentation:**

- **[DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md)** - Detailed 8-phase development process (subset of this doc)
- **[WAVE_1X_PLAN.md](WAVE_1X_PLAN.md)** - Wave-by-wave planning and scope
- **[ROADMAP.md](../ROADMAP.md)** - Long-term product roadmap
- **[CONTRIBUTING.md](../dev-docs/CONTRIBUTING.md)** - Contributor guidelines, PR process
- **[dev-docs/vision/](../dev-docs/vision/)** - Strategic vision documents (exploratory)
- **[AGENTS.md](../AGENTS.md)** - Machine-readable instructions for AI agents
- **[CHANGELOG.md](../CHANGELOG.md)** - Release history and version changes

**How They Relate:**

```
END_TO_END_PROCESS.md (this doc)
    ├─ Incorporates: DEVELOPMENT_LIFECYCLE.md (Phases 1-8)
    ├─ References: WAVE_1X_PLAN.md (Phase 0 - Wave planning)
    ├─ Aligns with: ROADMAP.md (Strategic direction)
    ├─ Guides: CONTRIBUTING.md (Contributor workflow)
    ├─ Informed by: dev-docs/vision/ (Long-term vision)
    └─ Outputs to: CHANGELOG.md (Release history)
```

### Appendix E: Common Anti-Patterns

**What NOT to do (and why):**

❌ **Code-First Development**
- **Problem:** Write code, then write tests (testing becomes validation, not design)
- **Fix:** Write tests first (TDD - RED → GREEN → REFACTOR)

❌ **Documentation as Afterthought**
- **Problem:** Write docs after code is done (docs get stale, inconsistent)
- **Fix:** Write how-to guides as value scenarios (docs ARE tests)

❌ **Behavior Without Specification**
- **Problem:** Implement features without BDD specs (ambiguous requirements, missed cases)
- **Fix:** Write .feature files first (Given/When/Then)

❌ **Missing Domain Model**
- **Problem:** Jump straight to implementation (anemic models, tightly coupled code)
- **Fix:** Define capabilities and domain concepts first (DDD)

❌ **Skipping Refactoring**
- **Problem:** Get GREEN and move on (technical debt accumulates)
- **Fix:** Always REFACTOR after GREEN (clean code pays dividends)

❌ **Big Bang Releases**
- **Problem:** Ship everything at once (high risk, long feedback loops)
- **Fix:** Wave-based delivery (3-5 capabilities per wave, ship incrementally)

❌ **No Traceability**
- **Problem:** Can't link feature request → code → tests → docs
- **Fix:** Use @behavior tags, cross-references, ID chains

❌ **Premature Optimization**
- **Problem:** Build for future needs before current needs (scope creep, wasted effort)
- **Fix:** Build for today, design for tomorrow (YAGNI + strategic extension points)

---

## Summary

This document provides the **complete end-to-end process** for mcp-orchestration, from strategic vision through release publishing and feedback iteration. Key takeaways:

1. **Vision-Driven**: Everything starts with user needs and strategic direction
2. **Specification-First**: Write docs/specs/tests before code
3. **Incremental Delivery**: Ship value in waves (3-5 capabilities at a time)
4. **Living Documentation**: E2E tests ARE how-to guides (docs stay synchronized)
5. **Quality-Focused**: Multiple validation gates ensure production-readiness
6. **Feedback-Informed**: Learnings feed back into next wave planning

**For AI Agents:**
- Use this as your master reference for understanding the complete lifecycle
- Start at Phase 0 for new waves, Phase 4 for implementation-only tasks
- Follow checklists to ensure nothing is missed
- Reference templates for consistent outputs

**For Human Developers:**
- Read Overview and Process Integration Map first
- Dive into specific phases as needed
- Use checklists for quality assurance
- Consult Appendices for templates and references

**For Project Managers:**
- Use Phase 0-3 for planning and scoping
- Use Phase 7-9 for release management and feedback
- Track progress via wave plans and checklists

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-25
**Maintainer:** mcp-orchestration core team
**Next Review:** 2026-01-25

🤖 Generated with [Claude Code](https://claude.com/claude-code)
