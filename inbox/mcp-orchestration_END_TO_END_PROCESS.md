---
title: End-to-End Development Process
category: process
version: 1.0.0
created: 2025-10-25
audience: developers, product-owners, contributors
---

# End-to-End Development Process: Vision to Release

**Complete journey:** From strategic vision through planning, design, development, testing, deployment, and release publishing.

**Purpose:** This document provides a comprehensive overview of how ideas transform into production releases in the mcp-n8n project, connecting strategic planning with tactical execution.

---

## Table of Contents

1. [Process Overview](#process-overview)
2. [Phase 1: Vision & Strategy](#phase-1-vision--strategy)
3. [Phase 2: Planning & Prioritization](#phase-2-planning--prioritization)
4. [Phase 3: Requirements & Design](#phase-3-requirements--design)
5. [Phase 4: Development](#phase-4-development)
6. [Phase 5: Testing & Quality](#phase-5-testing--quality)
7. [Phase 6: Review & Integration](#phase-6-review--integration)
8. [Phase 7: Release & Deployment](#phase-7-release--deployment)
9. [Phase 8: Monitoring & Feedback](#phase-8-monitoring--feedback)
10. [Complete Example Walkthrough](#complete-example-walkthrough)
11. [Process Metrics & KPIs](#process-metrics--kpis)
12. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Process Overview

### The Complete Journey

```
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: VISION & STRATEGY (Months)                             │
│ Strategic roadmap, market analysis, ecosystem alignment          │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: PLANNING & PRIORITIZATION (Weeks)                      │
│ Sprint planning, backlog grooming, stakeholder alignment         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 3: REQUIREMENTS & DESIGN (Days)                           │
│ DDD: Diátaxis change request → API reference → Acceptance       │
│ criteria                                                         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 4: DEVELOPMENT (Days-Weeks)                               │
│ BDD: Gherkin scenarios (RED)                                    │
│ TDD: Red-Green-Refactor cycles                                  │
│ Implementation: Code + Tests                                    │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 5: TESTING & QUALITY (Hours-Days)                        │
│ Unit → Smoke → Integration → E2E                                │
│ Coverage, linting, type checking, security                      │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 6: REVIEW & INTEGRATION (Hours-Days)                     │
│ Code review, docs review, CI/CD pipeline, merge                │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 7: RELEASE & DEPLOYMENT (Hours)                          │
│ Version bump, changelog, build, publish PyPI, deploy prod      │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 8: MONITORING & FEEDBACK (Continuous)                    │
│ Metrics, user feedback, bug reports, iteration planning        │
└──────────────────────────────────────────────────────────────────┘
                     │
                     └──→ Back to PHASE 1 or PHASE 2 (continuous improvement)
```

### Time Scales by Phase

| Phase | Time Scale | Frequency | Participants |
|-------|-----------|-----------|--------------|
| **Vision & Strategy** | Months | Quarterly | Leadership, product, engineering |
| **Planning & Prioritization** | Weeks | Sprint cycle (2 weeks) | Product, engineering leads |
| **Requirements & Design** | Days | Per feature | Engineers, product, designers |
| **Development** | Days-Weeks | Per feature | Engineers, AI assistants |
| **Testing & Quality** | Hours-Days | Per PR | Engineers, QA, CI/CD |
| **Review & Integration** | Hours-Days | Per PR | Reviewers, maintainers |
| **Release & Deployment** | Hours | Per version | Release manager, DevOps |
| **Monitoring & Feedback** | Continuous | Always on | All stakeholders |

---

## Phase 1: Vision & Strategy

### Purpose
Define the strategic direction, market positioning, and long-term goals for the project.

### Key Activities

#### 1. Strategic Roadmap Definition
**Document:** [STRATEGIC_ROADMAP.md](../../project-docs/STRATEGIC_ROADMAP.md)

**Activities:**
- Define product vision and mission
- Identify target users and use cases
- Analyze ecosystem and competition
- Establish multi-year goals
- Define success metrics

**Example Vision Statement:**
```markdown
**Vision:** Transform mcp-n8n from prototype to production-grade
universal MCP gateway with comprehensive documentation pipeline,
multi-backend aggregation, and ecosystem integration.

**Current Status:** v1.0.0 released (Oct 2025)
**Next Milestone:** v2.0.0 (MCP Gateway) - Q1 2026
```

#### 2. Ecosystem Alignment
**Documents:**
- Integration pattern analysis
- Feasibility studies
- Cross-project coordination

**Activities:**
- Survey MCP ecosystem landscape
- Identify integration patterns (P5, N2, N3, N3b, N4, N5)
- Evaluate feasibility of approaches
- Coordinate with related projects (mcp-orchestration, chora-compose)
- Document architectural decisions

**Example Output:**
```markdown
| Pattern | Status | Feasibility | Priority |
|---------|--------|-------------|----------|
| P5 | ✅ Implemented | 85% | High |
| N2 | ✅ Production | 95% | Complete |
| N3b | 🔬 Design | 75% | Medium |
| N4 | ❌ Rejected | 45% | None |
```

#### 3. Release Planning
**Document:** Version strategy and timeline

**Activities:**
- Define version numbering scheme (semantic versioning)
- Plan major/minor/patch releases
- Identify breaking changes
- Establish deprecation timelines
- Set release cadence

**Example Timeline:**
```
v1.0.0 (Oct 2025) → v1.1.0 (Nov 2025) → v1.5.0 (Jan 2026) → v2.0.0 (Feb 2026)
  Foundation          Gateway Fixes       Advanced           Migration
                                         Workflows
```

### Deliverables
- ✅ Strategic roadmap document
- ✅ Vision statement
- ✅ Success metrics defined
- ✅ Ecosystem integration plan
- ✅ Release timeline

### Time Investment
- **Initial:** 1-2 weeks (strategic planning session)
- **Ongoing:** Quarterly reviews (4-8 hours)

---

## Phase 2: Planning & Prioritization

### Purpose
Transform strategic goals into actionable sprints and prioritized backlog items.

### Key Activities

#### 1. Sprint Planning
**Document:** Sprint intent documents (e.g., `sprint-15-v1.0.1-patch-intent.md`)

**Activities:**
- Review strategic roadmap
- Identify sprint goals (what we'll deliver)
- Break down into user stories/tasks
- Estimate effort (story points/hours)
- Assign to sprint backlog
- Define sprint success criteria

**Example Sprint Goal:**
```markdown
**Sprint 15: v1.0.1 Quality Fixes**
**Duration:** 1-2 days
**Goal:** Fix pre-commit hooks, mypy errors, ruff violations

**Success Criteria:**
- ✅ All pre-commit hooks pass
- ✅ 0 mypy errors
- ✅ All tests pass
- ✅ Release ready for v1.1.0 development
```

#### 2. Backlog Grooming
**Document:** GitHub Issues/Projects

**Activities:**
- Review and refine backlog items
- Add acceptance criteria
- Tag with labels (feature, bug, tech-debt)
- Prioritize by business value
- Estimate complexity
- Identify dependencies

**Example Backlog Item:**
```markdown
**Issue #42:** Pattern P5 - Tool Loading Failures

**Type:** Bug (Critical)
**Priority:** P0 (Blocks v1.1.0)
**Estimated Effort:** 2-3 weeks
**Dependencies:** None

**Acceptance Criteria:**
- [ ] 0% tool loading failures
- [ ] Gateway aggregates 10+ backends
- [ ] All tool names normalized
- [ ] Multi-backend tests passing

**Related Documents:**
- Research: MCP-n8n to MCP-Gateway Evolution.md
- Intent: sprint-16-v1.1.0-pattern-p5-fixes-intent.md
```

#### 3. Stakeholder Alignment
**Meeting:** Sprint planning meeting

**Activities:**
- Present sprint goals to stakeholders
- Gather feedback and concerns
- Adjust priorities if needed
- Confirm resource availability
- Get approval to proceed

### Deliverables
- ✅ Sprint goals defined
- ✅ Backlog prioritized
- ✅ Effort estimates complete
- ✅ Sprint intent document
- ✅ Stakeholder approval

### Time Investment
- **Sprint Planning:** 2-4 hours every 2 weeks
- **Backlog Grooming:** 1-2 hours weekly

---

## Phase 3: Requirements & Design

### Purpose
Define the "what" and "how" before writing code through documentation-first design.

### Key Activities

#### 1. Change Request Intake (Diátaxis)
**Document:** Diátaxis-formatted change request

**Required Sections:**

**Explanation:**
- Context and problem statement
- Business value
- Success metrics
- Affected stakeholders
- Dependencies

**How-to Guide:**
- User or agent workflow steps
- Expected user journey
- Common use cases
- Error scenarios

**Reference:**
- Proposed API/tool contract
- Parameters and return types
- Example inputs/outputs
- Performance requirements

**Tutorial (optional):**
- End-to-end walkthrough
- Integration examples
- Best practices

**Example:**
```markdown
## Explanation
**Problem:** Backend tools fail to expose through gateway (Pattern P5)
**Impact:** Cannot aggregate multiple MCP servers
**Success Metric:** 0% tool loading failures, 10+ backends supported

## How-to Guide
**User Workflow:**
1. User configures multiple backends in config.yaml
2. Gateway starts and discovers backend tools
3. User calls tools via unified namespace (e.g., chora:*, coda:*)
4. Gateway routes to correct backend
5. Response returned to user

## Reference
**Configuration Schema:**
```yaml
backends:
  - name: chora-composer
    namespace: chora
    type: stdio_subprocess
    command: python
    args: ["-m", "chora_composer.mcp_server"]
```

**API Contract:**
- Gateway must expose all backend tools with namespace prefix
- Tool names: `{namespace}:{tool_name}`
- Failures must log errors with backend context
```

#### 2. Documentation Driven Design (DDD)
**Process:** [DDD_WORKFLOW.md](DDD_WORKFLOW.md)

**Steps:**

**Step 1: Understand the Need (30-60 min)**
- Review change request Explanation section
- Identify stakeholders
- Define "why" and "who"

**Step 2: Define Acceptance Criteria (30-60 min)**
- Extract from How-to Guide
- Write Given-When-Then scenarios
- Cover happy path + error cases
- Make testable

**Step 3: Design the API (1-2 hours)**
- Write API reference documentation
- Define function signatures
- Specify parameters and types
- Document return shapes
- Include JSON examples

**Step 4: Document Examples & Edge Cases (30-60 min)**
- Happy path examples
- Error handling examples
- Edge cases (empty, invalid, max values)
- Performance considerations

**Step 5: Review & Validate (30-60 min)**
- Product owner validates business value
- Engineers validate technical feasibility
- Technical writer validates clarity
- Get explicit sign-off

**Example API Documentation:**
```markdown
## route_tool_call

**Canonical Name:** `route_tool_call`
**Category:** Gateway Routing
**Status:** ✅ Implemented

Route a namespaced tool call to the appropriate backend.

### Signature
```python
async def route_tool_call(
    tool_name: str
) -> Optional[Tuple[Backend, str]]:
```

### Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tool_name` | string | Yes | Namespaced tool name (e.g., "chora:assemble_artifact") |

### Returns
**Success:**
```python
(backend: Backend, stripped_name: str)
# Example: (<ChoraBackend>, "assemble_artifact")
```

**Not Found:**
```python
None
```

### Examples
```python
# Route to chora backend
result = registry.route_tool_call("chora:assemble_artifact")
assert result[0].namespace == "chora"
assert result[1] == "assemble_artifact"

# Unknown namespace
result = registry.route_tool_call("unknown:tool")
assert result is None
```

### Error Scenarios
| Error | Cause | Resolution |
|-------|-------|------------|
| None returned | Unknown namespace | Check backend is registered |
| None returned | Missing prefix | Tool name must include namespace |
```

### Deliverables
- ✅ Diátaxis change request complete
- ✅ Acceptance criteria defined
- ✅ API reference documented
- ✅ Examples provided
- ✅ Design review approved

### Time Investment
- **Simple feature:** 2-4 hours
- **Complex feature:** 1-2 days
- **Breaking change:** 2-3 days (includes migration guide)

---

## Phase 4: Development

### Purpose
Implement the feature using test-driven development with BDD/TDD methodologies.

### Key Activities

#### 1. Behavior Driven Development (BDD)
**Process:** [BDD_WORKFLOW.md](BDD_WORKFLOW.md)

**Step 1: Write Feature File (30-60 min)**
```gherkin
# tests/features/gateway_routing.feature
Feature: Gateway Tool Routing

  As a gateway user
  I want tools to route to the correct backend
  So that I can use multiple MCP servers seamlessly

  Background:
    Given the gateway is running with 2 backends
    And backend "chora" handles "chora:*" tools
    And backend "coda" handles "coda:*" tools

  Scenario: Route namespaced tool to correct backend
    When I call tool "chora:assemble_artifact"
    Then the request is routed to "chora" backend
    And the backend receives tool name "assemble_artifact"

  Scenario: Handle unknown namespace
    When I call tool "unknown:tool"
    Then the request returns None
    And an error is logged with context "unknown namespace"

  Scenario Outline: Multiple backends route correctly
    When I call tool "<tool_name>"
    Then the request is routed to "<backend>" backend

    Examples:
      | tool_name              | backend |
      | chora:list_templates   | chora   |
      | coda:list_docs         | coda    |
      | chora:assemble_artifact| chora   |
```

**Step 2: Implement Step Definitions (1-2 hours)**
```python
# tests/step_defs/gateway_routing_steps.py
from pytest_bdd import given, when, then, parsers

@given('the gateway is running with 2 backends')
def gateway_with_backends(gateway_registry):
    """Fixture provides pre-configured gateway."""
    return gateway_registry

@when(parsers.parse('I call tool "{tool_name}"'))
async def call_tool(tool_name, gateway_registry):
    """Route tool call through gateway."""
    result = gateway_registry.route_tool_call(tool_name)
    pytest.last_result = result

@then(parsers.parse('the request is routed to "{backend}" backend'))
def verify_backend_routing(backend):
    """Assert correct backend received request."""
    result = pytest.last_result
    assert result is not None
    assert result[0].namespace == backend
```

**Step 3: Run BDD Tests - RED (5 min)**
```bash
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# Expected: FAILED - Feature not implemented yet
```

#### 2. Test Driven Development (TDD)
**Process:** [TDD_WORKFLOW.md](TDD_WORKFLOW.md)

**RED Phase: Write Failing Tests (1-2 hours)**
```python
# tests/unit/test_backend_registry.py
import pytest
from mcp_n8n.backends.registry import BackendRegistry

async def test_route_tool_call_with_namespace():
    """Route namespaced tool to correct backend."""
    registry = BackendRegistry()
    registry.register(chora_config)  # Registers "chora" namespace

    result = registry.route_tool_call("chora:assemble_artifact")

    assert result is not None
    backend, stripped_name = result
    assert backend.namespace == "chora"
    assert stripped_name == "assemble_artifact"

async def test_route_tool_call_unknown_namespace():
    """Return None for unknown namespace."""
    registry = BackendRegistry()

    result = registry.route_tool_call("unknown:tool")

    assert result is None

# Run: pytest tests/unit/test_backend_registry.py -v
# Expected: FAILED - Methods not implemented
```

**GREEN Phase: Minimal Implementation (2-4 hours)**
```python
# src/mcp_n8n/backends/registry.py
from typing import Optional, Tuple

class BackendRegistry:
    """Registry for managing backend lifecycle and routing."""

    def __init__(self):
        self._backends: Dict[str, Backend] = {}

    def register(self, config: BackendConfig) -> None:
        """Register a backend with its namespace."""
        backend = self._create_backend(config)
        self._backends[config.namespace] = backend

    def route_tool_call(self, tool_name: str) -> Optional[Tuple[Backend, str]]:
        """
        Route a namespaced tool call to appropriate backend.

        Args:
            tool_name: Namespaced tool name (e.g., "chora:assemble")

        Returns:
            (Backend, stripped_tool_name) if found, None otherwise
        """
        # Split on namespace separator
        parts = tool_name.split(":", 1)
        if len(parts) != 2:
            self.logger.warning(f"Tool name missing namespace: {tool_name}")
            return None

        namespace, stripped_name = parts

        # Find backend by namespace
        backend = self._backends.get(namespace)
        if backend is None:
            self.logger.error(f"Unknown namespace: {namespace}")
            return None

        return (backend, stripped_name)

# Run: pytest tests/unit/test_backend_registry.py -v
# Expected: PASSED ✅
```

**REFACTOR Phase: Improve Design (1-2 hours)**
```python
# Extract validation to separate method
class BackendRegistry:

    def route_tool_call(self, tool_name: str) -> Optional[Tuple[Backend, str]]:
        """Route namespaced tool to backend."""
        namespace, stripped_name = self._parse_tool_name(tool_name)
        if namespace is None:
            return None

        backend = self._find_backend(namespace)
        if backend is None:
            return None

        return (backend, stripped_name)

    def _parse_tool_name(self, tool_name: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract namespace and tool name from namespaced string."""
        parts = tool_name.split(":", 1)
        if len(parts) != 2:
            self.logger.warning(f"Tool name missing namespace: {tool_name}")
            return (None, None)
        return tuple(parts)

    def _find_backend(self, namespace: str) -> Optional[Backend]:
        """Find backend by namespace."""
        backend = self._backends.get(namespace)
        if backend is None:
            self.logger.error(f"Unknown namespace: {namespace}")
        return backend

# Run: pytest tests/unit/test_backend_registry.py -v
# Expected: PASSED ✅ (still green after refactor)
```

**Repeat RED-GREEN-REFACTOR for each behavior**

#### 3. Integration Testing
```python
# tests/integration/test_gateway_e2e.py
@pytest.mark.integration
async def test_gateway_routes_to_real_backend():
    """Integration test with actual backend subprocess."""
    # Start real gateway with real backends
    gateway = await start_gateway_with_backends()

    # Call tool through gateway
    result = await gateway.call_tool("chora:list_templates")

    # Verify backend processed request
    assert result["success"] is True
    assert "templates" in result

    await gateway.shutdown()
```

### Deliverables
- ✅ BDD feature files (Gherkin scenarios)
- ✅ BDD step definitions
- ✅ Unit tests (≥90% coverage)
- ✅ Integration tests
- ✅ Implementation code
- ✅ All tests passing (GREEN)

### Time Investment
- **Small feature:** 1-2 days
- **Medium feature:** 3-5 days
- **Large feature:** 1-2 weeks

---

## Phase 5: Testing & Quality

### Purpose
Ensure code quality, test coverage, and security before integration.

### Key Activities

#### 1. Test Pyramid Execution
**Process:** [TESTING.md](TESTING.md)

**Layer 1: Unit Tests (seconds)**
```bash
# Fast, isolated tests
pytest tests/unit/ tests/test_*.py -v

# Expected: 60% of total tests, <1s execution
```

**Layer 2: Smoke Tests (seconds)**
```bash
# Critical paths with mocks
just smoke
# or: pytest tests/smoke/ -v

# Expected: 25% of total tests, <30s execution
```

**Layer 3: Integration Tests (seconds-minutes)**
```bash
# Real backends, real I/O
pytest tests/integration/ -m integration -v

# Expected: 10% of total tests, <2min execution
```

**Layer 4: BDD/E2E Tests (seconds-minutes)**
```bash
# Full workflows, acceptance criteria
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# Expected: 5% of total tests, <1min execution
```

#### 2. Coverage Analysis
```bash
# Generate coverage report
just test-coverage

# View in browser
open htmlcov/index.html

# Coverage targets:
# - Overall: ≥85%
# - Unit tests: ≥90%
# - Integration tests: ≥80%
# - Critical modules (gateway, registry): ≥95%
```

**Coverage Report Example:**
```
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/mcp_n8n/gateway.py           234     12    95%
src/mcp_n8n/backends/registry.py 156      5    97%
src/mcp_n8n/config.py            89       2    98%
--------------------------------------------------
TOTAL                           1234     94    92%
```

#### 3. Code Quality Checks
```bash
# Linting (ruff)
just lint
# or: ruff check src/ tests/

# Type checking (mypy)
just typecheck
# or: mypy src/

# Security scanning
bandit -r src/
pip-audit

# Pre-commit hooks (runs all checks)
pre-commit run --all-files
```

**Quality Gates (must pass):**
- ✅ 0 ruff errors
- ✅ 0 mypy errors
- ✅ 0 critical security issues
- ✅ All pre-commit hooks pass
- ✅ Test coverage ≥85%

#### 4. Performance Testing (optional for major releases)
```bash
# Load testing with Locust
locust -f tests/performance/locustfile.py

# Targets:
# - p50 latency: <100ms
# - p95 latency: <500ms
# - p99 latency: <1s
# - Throughput: 100 req/s
```

### Deliverables
- ✅ All tests passing
- ✅ Coverage ≥85%
- ✅ 0 linting errors
- ✅ 0 type errors
- ✅ 0 critical security issues
- ✅ Performance benchmarks met (if applicable)

### Time Investment
- **Per PR:** 30 min - 2 hours (automated via CI)
- **Major releases:** +1-2 days (performance testing)

---

## Phase 6: Review & Integration

### Purpose
Validate changes through peer review and automated CI/CD before merging.

### Key Activities

#### 1. Pull Request Creation
**PR Template:**
```markdown
## Summary
Brief description of changes

## Related Issues
Closes #42

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Documentation
- [ ] API reference updated
- [ ] CHANGELOG.md entry added
- [ ] Migration guide (if breaking)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] BDD scenarios added/updated
- [ ] All tests passing locally

## Quality Checklist
- [ ] Code follows style guidelines (ruff)
- [ ] Type hints complete (mypy)
- [ ] Coverage ≥90% for new code
- [ ] Pre-commit hooks pass
- [ ] No security issues (bandit)
```

#### 2. Code Review Process
**Reviewer Checklist:**

**Functionality:**
- [ ] Code matches acceptance criteria
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Logging sufficient

**Design:**
- [ ] Design is clear and maintainable
- [ ] No unnecessary complexity
- [ ] Follows project patterns
- [ ] Performance acceptable

**Tests:**
- [ ] Test coverage adequate
- [ ] Tests are meaningful (not just for coverage)
- [ ] BDD scenarios readable
- [ ] Integration tests appropriate

**Documentation:**
- [ ] API docs complete
- [ ] Code comments clear
- [ ] Examples provided
- [ ] CHANGELOG updated

**Review Outcomes:**
- ✅ **Approve:** Merge ready
- 🔄 **Request Changes:** Must address comments
- 💬 **Comment:** Suggestions, non-blocking

#### 3. CI/CD Pipeline
**GitHub Actions Workflow:**

```yaml
# .github/workflows/ci.yml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run linting
        run: ruff check src/ tests/

      - name: Run type checking
        run: mypy src/

      - name: Run unit tests
        run: pytest tests/unit/ --cov=mcp_n8n --cov-report=xml

      - name: Run smoke tests
        run: pytest tests/smoke/ -v

      - name: Run integration tests
        run: pytest tests/integration/ -m integration

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Pipeline Stages (all must pass):**
1. **Lint** (30 sec) - ruff check
2. **Type Check** (30 sec) - mypy
3. **Unit Tests** (1-2 min) - pytest with coverage
4. **Smoke Tests** (30 sec) - fast critical path tests
5. **Integration Tests** (2-3 min) - real backends
6. **Security Scan** (1 min) - bandit + pip-audit
7. **Coverage Report** (30 sec) - upload to Codecov

**Total Pipeline Time:** 5-8 minutes

#### 4. Merge Requirements
**All must be satisfied:**
- ✅ CI/CD pipeline GREEN
- ✅ 1+ code review approval
- ✅ All review comments addressed
- ✅ Branch up to date with main
- ✅ No merge conflicts
- ✅ Coverage not decreased

**Merge Strategy:**
- **Feature branches:** Squash and merge (clean history)
- **Hotfixes:** Rebase and merge (preserve commits)
- **Breaking changes:** Merge commit (preserve full history)

### Deliverables
- ✅ PR created and reviewed
- ✅ CI/CD pipeline passing
- ✅ Approval received
- ✅ Changes merged to main/develop

### Time Investment
- **PR Creation:** 15-30 min
- **Code Review:** 1-2 hours (per reviewer)
- **CI/CD:** 5-10 min (automated)
- **Addressing Feedback:** 1-4 hours

---

## Phase 7: Release & Deployment

### Purpose
Package, version, publish, and deploy the software to production.

### Key Activities

#### 1. Pre-Release Preparation
**Process:** [RELEASE.md](RELEASE.md)

**Step 1: Verify Readiness**
```bash
# Ensure clean state
git status  # No uncommitted changes
git branch --show-current  # On main branch
git pull origin main  # Up to date

# Run pre-merge checks
just pre-merge

# Expected: All checks pass
```

**Step 2: Update Documentation**
- [ ] CHANGELOG.md has entries in `[Unreleased]` section
- [ ] README.md reflects current features
- [ ] Configuration examples accurate
- [ ] Migration guide (if breaking change)

**Step 3: Decide Version**
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR (X.0.0):** Breaking changes
- **MINOR (0.X.0):** New features (backward-compatible)
- **PATCH (0.0.X):** Bug fixes (backward-compatible)

**Example:**
```
v1.0.0 → v1.0.1 (patch: bug fixes)
v1.0.0 → v1.1.0 (minor: new feature)
v1.0.0 → v2.0.0 (major: breaking change)
```

#### 2. Automated Release (Recommended)
```bash
# One-command release
just release patch   # For v1.0.0 → v1.0.1
just release minor   # For v1.0.0 → v1.1.0
just release major   # For v1.0.0 → v2.0.0
```

**What this does:**
1. Bumps version in `pyproject.toml`
2. Updates `CHANGELOG.md` (moves `[Unreleased]` → `[version]`)
3. Runs pre-merge checks
4. Creates release commit
5. Creates git tag `vX.Y.Z`
6. Pushes commit and tag to GitHub
7. Triggers GitHub Actions CI/CD

**Time:** ~5 minutes (1 command + CI wait)

#### 3. GitHub Actions Release Workflow
**Triggered by:** Git tag push (`v*`)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Build package
        run: python -m build

      - name: Test package
        run: |
          pip install dist/*.whl
          mcp-n8n --help

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGELOG.md
          files: dist/*
```

**Pipeline Steps:**
1. **Build** (~1 min) - Create wheel + tarball
2. **Test** (~1 min) - Install and verify
3. **Publish PyPI** (~30 sec) - Upload to pypi.org
4. **GitHub Release** (~30 sec) - Create release with notes

**Total Time:** ~3-5 minutes

#### 4. Verify Release
```bash
# Create clean environment
python -m venv verify-release
source verify-release/bin/activate

# Install from PyPI
pip install mcp-n8n==X.Y.Z

# Verify installation
mcp-n8n --help
pip show mcp-n8n

# Cleanup
deactivate
rm -rf verify-release
```

**Verify online:**
- 📦 PyPI: https://pypi.org/project/mcp-n8n/X.Y.Z/
- 🐙 GitHub Release: https://github.com/liminalcommons/mcp-n8n/releases/tag/vX.Y.Z

#### 5. Production Deployment
**For cloud deployments:**

```bash
# Kubernetes deployment
kubectl set image deployment/mcp-gateway \
  mcp-gateway=liminalcommons/mcp-n8n:vX.Y.Z

# Verify rollout
kubectl rollout status deployment/mcp-gateway

# Monitor metrics
kubectl logs -f deployment/mcp-gateway
```

**For Docker deployments:**
```bash
# Pull new image
docker pull liminalcommons/mcp-n8n:vX.Y.Z

# Stop old container
docker stop mcp-gateway

# Start new container
docker run -d --name mcp-gateway \
  -p 8000:8000 \
  liminalcommons/mcp-n8n:vX.Y.Z

# Verify health
curl http://localhost:8000/health
```

### Deliverables
- ✅ Git tag `vX.Y.Z` created
- ✅ Package published to PyPI
- ✅ GitHub Release created
- ✅ Production deployment successful
- ✅ Release announcement published

### Time Investment
- **Automated Release:** 5-10 minutes
- **Manual Review Release:** 10-20 minutes
- **Deployment:** 10-30 minutes (depending on infrastructure)

---

## Phase 8: Monitoring & Feedback

### Purpose
Monitor production health, gather user feedback, and plan next iteration.

### Key Activities

#### 1. Production Monitoring
**Metrics to Track:**

**Application Metrics (Prometheus):**
```python
# Request metrics
http_requests_total{method, status}
http_request_duration_seconds{method, quantile}

# Business metrics
backend_tool_calls_total{backend, tool, status}
backend_errors_total{backend, error_type}
gateway_backends_registered{namespace}

# Performance metrics
tool_execution_duration_seconds{tool, quantile}
event_processing_lag_seconds
```

**Dashboard (Grafana):**
- Request rate (req/s)
- Latency percentiles (p50, p95, p99)
- Error rate (%)
- Backend health status
- Tool call distribution

**Alerts:**
```yaml
# Prometheus alert rules
groups:
  - name: mcp-gateway
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        severity: critical

      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 5m
        severity: warning

      - alert: BackendDown
        expr: backend_status{status!="running"} == 1
        for: 2m
        severity: critical
```

#### 2. User Feedback Collection
**Channels:**
- GitHub Issues (bugs, feature requests)
- GitHub Discussions (questions, ideas)
- Email feedback
- Usage analytics (telemetry)
- Community Slack/Discord

**Tracking:**
```markdown
**Issue Template: Bug Report**

**Environment:**
- mcp-n8n version: X.Y.Z
- Python version:
- OS:

**Expected Behavior:**
What should happen?

**Actual Behavior:**
What actually happened?

**Steps to Reproduce:**
1. Step one
2. Step two

**Logs:**
```
[Include relevant logs]
```
```

#### 3. Performance Analysis
**Weekly Review:**
- Review Grafana dashboards
- Analyze error logs
- Identify performance bottlenecks
- Check resource utilization (CPU, memory, I/O)

**Monthly Report:**
```markdown
## Production Health Report - November 2025

### Key Metrics
- Uptime: 99.8% (target: 99.5%)
- p95 latency: 287ms (target: <500ms) ✅
- Error rate: 0.3% (target: <1%) ✅
- Total requests: 2.4M

### Top Issues
1. #127 - High memory usage with 10+ backends (P1)
2. #128 - Occasional timeout with n8n webhook (P2)

### Performance Improvements
- Implemented connection pooling → 30% latency reduction
- Added Redis caching → 50% cache hit rate

### Action Items
- [ ] Investigate memory leak in backend lifecycle
- [ ] Optimize n8n webhook retry logic
- [ ] Increase monitoring for cold starts
```

#### 4. Iteration Planning
**Feedback Loop:**

```
Production Metrics → User Feedback → Bug Reports → Feature Requests
                                          ↓
                                  Prioritization
                                          ↓
                             Next Sprint Planning
                                          ↓
                              Back to Phase 2
```

**Prioritization Framework:**

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| **P0 (Critical)** | Outage, data loss, security | Immediate (hours) |
| **P1 (High)** | Severe degradation, blocking users | 1-2 days |
| **P2 (Medium)** | Moderate impact, workaround exists | 1-2 weeks |
| **P3 (Low)** | Minor issue, cosmetic | Next sprint |

### Deliverables
- ✅ Monitoring dashboards configured
- ✅ Alerts firing appropriately
- ✅ Weekly health reports
- ✅ User feedback tracked
- ✅ Next iteration planned

### Time Investment
- **Monitoring Setup:** 1-2 days (one-time)
- **Daily Monitoring:** 15-30 minutes
- **Weekly Review:** 1-2 hours
- **Monthly Report:** 2-4 hours

---

## Complete Example Walkthrough

### Example: Implementing "Daily Report Workflow" Feature

Let's walk through the entire process for a real feature from the mcp-n8n project.

---

#### Phase 1: Vision & Strategy (Week 1)

**Strategic Context:**
- **Roadmap:** Sprint 5 - Production Workflows (v0.5.0)
- **Vision:** Enable automated reporting workflows driven by events
- **Success Metric:** Generate daily development reports with minimal manual effort

**Ecosystem Alignment:**
- Integrates with chora-compose for template rendering
- Uses git integration for commit data
- Prepares for n8n webhook integration

**Release Plan:**
- Target: v0.5.0 (Oct 2025)
- Type: Minor release (new feature)
- Dependencies: EventWorkflowRouter, chora-compose templates

---

#### Phase 2: Planning & Prioritization (Week 1-2)

**Sprint Planning:**
```markdown
**Sprint 5: Production Workflows (v0.5.0)**
**Duration:** 2 weeks
**Priority:** High (strategic capability)

**Sprint Goal:**
Enable event-driven workflow automation with daily report template

**User Stories:**
1. As a developer, I want automated daily reports of my commits
2. As a team lead, I want daily summaries of team progress
3. As a PM, I want event-triggered reports without manual work

**Success Criteria:**
- ✅ EventWorkflowRouter routes events to workflows
- ✅ DailyReportWorkflow generates report from git commits
- ✅ Report uses chora-compose template
- ✅ All workflows tested via BDD scenarios
```

**Backlog Item:**
```markdown
**Issue #67:** Daily Report Workflow

**Type:** Feature
**Priority:** P1 (Sprint 5 goal)
**Estimated Effort:** 1 week
**Dependencies:** EventWorkflowRouter, chora-compose integration

**Acceptance Criteria:**
- [ ] Workflow triggered by `daily_report_requested` event
- [ ] Retrieves git commits from last 24 hours
- [ ] Renders report using daily-report.md.j2 template
- [ ] Returns formatted markdown report
```

---

#### Phase 3: Requirements & Design (Week 2, Day 1)

**Diátaxis Change Request:**
```markdown
## Explanation
**Problem:** Manual effort to track daily development progress
**Solution:** Automated workflow that queries git, formats report
**Success Metric:** Daily reports generated in <5 seconds

## How-to Guide
**User Workflow:**
1. User emits `daily_report_requested` event (or scheduled cron)
2. DailyReportWorkflow queries git commits (last 24h)
3. Workflow aggregates statistics (files changed, lines added)
4. Workflow renders report via chora-compose template
5. Report returned as markdown (can be emailed, posted to Slack)

## Reference
**Event Schema:**
```json
{
  "event_type": "daily_report_requested",
  "timestamp": "2025-10-25T10:00:00Z",
  "parameters": {
    "hours": 24,
    "format": "markdown"
  }
}
```

**API Contract:**
```python
async def run(hours: int = 24) -> dict:
    """
    Generate daily report from git commits.

    Returns:
        {
          "report": "# Daily Report...",
          "commits": [...],
          "stats": {...}
        }
    """
```
```

**DDD Process:**

**Step 1: Acceptance Criteria**
```markdown
**Scenario 1:** Generate report with commits
- Given git repository has commits in last 24 hours
- When daily report workflow runs
- Then report includes commit summaries
- And report includes files changed
- And report includes statistics

**Scenario 2:** Handle no commits
- Given git repository has no commits in last 24 hours
- When daily report workflow runs
- Then report shows "No activity"
- And report includes timestamp

**Scenario 3:** Template rendering
- Given daily-report.md.j2 template exists
- When workflow renders report
- Then markdown is well-formatted
- And template variables populated correctly
```

**Step 2: API Design**
```python
# src/mcp_n8n/workflows/daily_report.py
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DailyReportWorkflow:
    """Generate daily development reports from git commits."""

    async def run(self, hours: int = 24) -> dict:
        """
        Generate daily report from git commits.

        Args:
            hours: Number of hours to look back

        Returns:
            {
              "report": str,      # Markdown report
              "commits": [...],   # Commit data
              "stats": {...}      # Aggregated statistics
            }
        """
        pass  # To be implemented
```

**Time Spent:** 3 hours (DDD process)

---

#### Phase 4: Development (Week 2, Days 2-4)

**BDD: Feature File**
```gherkin
# tests/features/daily_report.feature
Feature: Daily Report Workflow

  As a developer
  I want automated daily reports
  So that I can track my progress effortlessly

  Background:
    Given the EventWorkflowRouter is configured
    And the DailyReportWorkflow is registered

  Scenario: Generate report with recent commits
    Given the git repository has 5 commits in the last 24 hours
    When a daily_report_requested event is emitted
    Then the DailyReportWorkflow is triggered
    And the workflow queries git commits from the last 24 hours
    And a report is generated with commit summaries
    And the report includes statistics (files changed, lines added)

  Scenario: Handle repository with no commits
    Given the git repository has 0 commits in the last 24 hours
    When a daily_report_requested event is emitted
    Then the workflow generates a "No activity" report
    And the report includes the timestamp

  Scenario: Template rendering with chora-compose
    Given a daily-report.md.j2 template exists
    When the workflow renders the report
    Then the markdown is properly formatted
    And all template variables are populated
```

**BDD: Step Definitions**
```python
# tests/step_defs/test_daily_report_steps.py
from pytest_bdd import given, when, then, scenario

@scenario('features/daily_report.feature',
          'Generate report with recent commits')
def test_daily_report_with_commits():
    pass

@given('the git repository has 5 commits in the last 24 hours')
def mock_git_commits(mocker):
    """Mock git subprocess to return 5 commits."""
    mock_commits = [
        {"sha": "abc123", "message": "feat: Add feature", "author": "dev1"},
        {"sha": "def456", "message": "fix: Bug fix", "author": "dev1"},
        # ... 3 more
    ]
    mocker.patch('mcp_n8n.workflows.daily_report.get_recent_commits',
                 return_value=mock_commits)

@when('a daily_report_requested event is emitted')
async def emit_daily_report_event(event_router):
    """Emit event to trigger workflow."""
    event = {
        "event_type": "daily_report_requested",
        "timestamp": datetime.now().isoformat(),
    }
    await event_router.route_event(event)

@then('the workflow generates a report with commit summaries')
def verify_report_generated():
    """Assert report contains commits."""
    report = pytest.last_result["report"]
    assert "feat: Add feature" in report
    assert "fix: Bug fix" in report
```

**Run BDD Tests - RED:**
```bash
pytest tests/step_defs/test_daily_report_steps.py --gherkin-terminal-reporter -v

# Output: FAILED - DailyReportWorkflow not implemented
```

**TDD: Unit Tests (RED)**
```python
# tests/workflows/test_daily_report.py
import pytest
from mcp_n8n.workflows.daily_report import DailyReportWorkflow

@pytest.mark.asyncio
async def test_get_recent_commits_returns_list():
    """Unit: get_recent_commits returns commit list."""
    workflow = DailyReportWorkflow()

    commits = await workflow.get_recent_commits(hours=24)

    assert isinstance(commits, list)
    assert all("sha" in c for c in commits)

@pytest.mark.asyncio
async def test_render_report_with_template():
    """Unit: render_report uses chora-compose template."""
    workflow = DailyReportWorkflow()
    commits = [{"sha": "abc", "message": "test"}]

    report = await workflow.render_report(commits)

    assert "# Daily Report" in report
    assert "abc" in report

# Run: pytest tests/workflows/test_daily_report.py -v
# Output: FAILED - Methods not implemented
```

**TDD: Implementation (GREEN)**
```python
# src/mcp_n8n/workflows/daily_report.py
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class DailyReportWorkflow:
    """Generate daily development reports from git commits."""

    def __init__(self):
        self.logger = get_logger(__name__)

    async def run(self, hours: int = 24) -> dict:
        """Generate daily report from git commits."""
        self.logger.info(f"Generating daily report (last {hours} hours)")

        # Get commits
        commits = await self.get_recent_commits(hours)

        # Calculate statistics
        stats = self._calculate_stats(commits)

        # Render report
        report = await self.render_report(commits, stats)

        return {
            "report": report,
            "commits": commits,
            "stats": stats
        }

    async def get_recent_commits(self, hours: int) -> List[Dict[str, Any]]:
        """Query git for recent commits."""
        since_time = datetime.now() - timedelta(hours=hours)
        since_str = since_time.strftime("%Y-%m-%d %H:%M:%S")

        # Run git log
        result = subprocess.run(
            [
                "git", "log",
                f"--since={since_str}",
                "--pretty=format:%H|%an|%ae|%ad|%s",
                "--date=iso"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse output
        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            sha, author, email, date, message = line.split("|", 4)
            commits.append({
                "sha": sha,
                "author": author,
                "email": email,
                "date": date,
                "message": message
            })

        return commits

    def _calculate_stats(self, commits: List[Dict]) -> Dict[str, Any]:
        """Calculate statistics from commits."""
        return {
            "total_commits": len(commits),
            "authors": list(set(c["author"] for c in commits)),
            "commit_count_by_author": self._count_by_author(commits)
        }

    async def render_report(self, commits: List[Dict], stats: Dict) -> str:
        """Render report using chora-compose template."""
        # Load template
        template_path = "chora-configs/daily-report.md.j2"

        # Prepare context
        context = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "commits": commits,
            "stats": stats
        }

        # Render via chora-compose
        from chora_compose.template_engine import render_template
        report = render_template(template_path, context)

        return report

# Run tests: pytest tests/workflows/test_daily_report.py -v
# Output: PASSED ✅
```

**TDD: Refactor**
- Extract `_count_by_author()` helper
- Add error handling for git subprocess failures
- Add logging
- Validate template path

**Run all tests:**
```bash
pytest tests/workflows/test_daily_report.py -v
# Output: PASSED ✅

pytest tests/step_defs/test_daily_report_steps.py --gherkin-terminal-reporter -v
# Output: PASSED ✅ (BDD scenarios now pass)
```

**Time Spent:** 2.5 days (BDD + TDD + implementation)

---

#### Phase 5: Testing & Quality (Week 2, Day 5)

**Test Pyramid:**
```bash
# Unit tests
pytest tests/workflows/test_daily_report.py --cov=mcp_n8n.workflows.daily_report

# Coverage: 94%

# Integration test
pytest tests/integration/test_daily_report_integration.py -v
# Tests actual git repo, actual template rendering

# BDD scenarios
pytest tests/step_defs/test_daily_report_steps.py --gherkin-terminal-reporter
# All scenarios PASSED
```

**Code Quality:**
```bash
# Linting
ruff check src/mcp_n8n/workflows/daily_report.py
# ✅ No issues

# Type checking
mypy src/mcp_n8n/workflows/daily_report.py
# ✅ No errors

# Security
bandit -r src/mcp_n8n/workflows/
# ✅ No critical issues

# Pre-commit
pre-commit run --all-files
# ✅ All hooks passed
```

**Coverage Report:**
```
Name                                    Stmts   Miss  Cover
-------------------------------------------------------------
src/mcp_n8n/workflows/daily_report.py     87      5    94%
```

**Time Spent:** 4 hours (testing + quality)

---

#### Phase 6: Review & Integration (Week 3, Day 1)

**Pull Request:**
```markdown
## Summary
Implements Daily Report Workflow (Sprint 5) for automated git commit reporting.

## Related Issues
Closes #67

## Type of Change
- [x] New feature (non-breaking)

## Documentation
- [x] API reference added (workflows/daily_report.py docstrings)
- [x] CHANGELOG.md entry added
- [x] BDD scenarios document behavior
- [x] Template example included (chora-configs/daily-report.md.j2)

## Testing
- [x] Unit tests added (94% coverage)
- [x] Integration tests added (real git + templates)
- [x] BDD scenarios added and passing
- [x] All tests passing locally

## Quality Checklist
- [x] Code follows style guidelines (ruff)
- [x] Type hints complete (mypy)
- [x] Coverage 94% (exceeds 90% target)
- [x] Pre-commit hooks pass
- [x] No security issues (bandit)
```

**Code Review:**
- Reviewer 1: "Looks good, minor suggestion on error handling" (Comment)
- Reviewer 2: "Approve - excellent test coverage and docs" (Approve)

**Address Feedback:**
- Added try-catch for git subprocess failures
- Improved error messages
- Updated tests

**CI/CD Pipeline:**
```
✅ Lint (30s)
✅ Type Check (25s)
✅ Unit Tests (45s)
✅ Smoke Tests (20s)
✅ Integration Tests (1m 30s)
✅ Coverage (92%) (30s)
✅ Security Scan (45s)

Total: 4min 5s
```

**Merge:**
```bash
# Squash and merge
git merge --squash feature/daily-report-workflow
git commit -m "feat(workflows): Add daily report workflow

Implements automated daily development reports from git commits
with chora-compose template rendering.

Closes #67"
```

**Time Spent:** 6 hours (PR creation, review, feedback, merge)

---

#### Phase 7: Release & Deployment (Week 3, Day 2)

**Pre-Release:**
```bash
# Verify readiness
git status  # Clean
just pre-merge  # ✅ All checks pass

# CHANGELOG.md already updated in PR
```

**Release:**
```bash
# Automated release
just release minor  # v0.4.0 → v0.5.0

# What happens:
# 1. Version bumped to 0.5.0
# 2. CHANGELOG.md updated
# 3. Commit created
# 4. Tag v0.5.0 created
# 5. Pushed to GitHub
# 6. GitHub Actions triggered
```

**GitHub Actions:**
```
Release v0.5.0

✅ Build package (1m 12s)
✅ Test package (58s)
✅ Publish to PyPI (34s)
✅ Create GitHub Release (28s)

Total: 3min 12s
```

**Verify:**
```bash
# Install from PyPI
pip install mcp-n8n==0.5.0

# Test
python -c "from mcp_n8n.workflows.daily_report import DailyReportWorkflow; print('OK')"
# Output: OK
```

**Production Deployment:**
```bash
# Update production config
kubectl set image deployment/mcp-gateway mcp-gateway=liminalcommons/mcp-n8n:v0.5.0

# Verify rollout
kubectl rollout status deployment/mcp-gateway
# deployment "mcp-gateway" successfully rolled out

# Test in production
curl -X POST http://gateway.example.com/mcp \
  -d '{"event_type": "daily_report_requested"}'
# Returns: {"report": "# Daily Report...", "commits": [...]}
```

**Announcement:**
```markdown
# mcp-n8n v0.5.0 Released 🎉

**New Feature:** Daily Report Workflow

Automatically generate development reports from git commits!

**Usage:**
```python
from mcp_n8n.workflows import DailyReportWorkflow

workflow = DailyReportWorkflow()
report = await workflow.run(hours=24)
print(report["report"])
```

**What's New:**
- Event-driven workflow automation
- Git commit aggregation
- chora-compose template rendering
- Fully tested with BDD scenarios

Install: `pip install mcp-n8n==0.5.0`

📚 Docs: https://mcp-n8n.readthedocs.io/v0.5.0
📦 PyPI: https://pypi.org/project/mcp-n8n/0.5.0/
```

**Time Spent:** 2 hours (release + deployment + announcement)

---

#### Phase 8: Monitoring & Feedback (Ongoing)

**Day 1 Post-Release:**
```
Metrics:
- 24 installations (PyPI)
- 0 errors in production
- p95 latency: 1.2s (within target)
- 3 daily reports generated successfully
```

**Week 1 Post-Release:**
```
Metrics:
- 127 installations (PyPI)
- 2 bug reports (minor edge cases)
- 1 feature request (schedule recurring reports)
- Production uptime: 99.9%

Issues Filed:
- #71: Daily report fails when no git history
- #72: Template variables not documented
- #73: Feature request - scheduled daily reports
```

**Week 2 Post-Release:**
```
Actions Taken:
- Fixed #71 with patch v0.5.1
- Documented template variables in #72
- Planned #73 for Sprint 6

User Feedback:
- "Daily reports are game-changing!" (GitHub Discussions)
- "Would love Slack integration" (Feature request)
- "Works perfectly with chora-compose" (Twitter)
```

**Sprint 6 Planning:**
```markdown
Based on feedback from v0.5.0:

High Priority:
- #73: Scheduled daily reports (cron triggers)
- #74: Slack integration for reports
- #71: Edge case handling improvements

Backlog:
- Email report delivery
- Weekly/monthly report templates
- Multi-repo support
```

**Time Spent (Ongoing):**
- Daily monitoring: 15 min/day
- Weekly review: 2 hours/week
- Issue triage: 1-2 hours/week

---

### Total Time Investment for Daily Report Feature

| Phase | Time Spent | Cumulative |
|-------|-----------|------------|
| 1. Vision & Strategy | 2 hours (sprint planning) | 2 hours |
| 2. Planning & Prioritization | 3 hours (backlog, alignment) | 5 hours |
| 3. Requirements & Design | 3 hours (DDD process) | 8 hours |
| 4. Development | 2.5 days = 20 hours (BDD/TDD) | 28 hours |
| 5. Testing & Quality | 4 hours (coverage, quality) | 32 hours |
| 6. Review & Integration | 6 hours (PR, review, merge) | 38 hours |
| 7. Release & Deployment | 2 hours (release, deploy) | 40 hours |
| 8. Monitoring (Week 1) | 3 hours (monitoring, triage) | 43 hours |

**Total: ~43 hours (~5.4 days) from idea to production**

**Breakdown:**
- Planning & Design: 18% (8 hours)
- Development: 50% (20 hours)
- Testing & Quality: 10% (4 hours)
- Review & Integration: 15% (6 hours)
- Release & Deployment: 5% (2 hours)
- Monitoring: 2% (3 hours week 1)

---

## Process Metrics & KPIs

### Development Velocity

**Cycle Time Metrics:**
```markdown
**Cycle Time:** Idea → Production
- Target: <2 weeks for medium feature
- Actual (Daily Report): 1.5 weeks ✅

**Lead Time:** Commit → Production
- Target: <1 week
- Actual: 3 days ✅

**PR Throughput:** PRs merged per week
- Target: 3-5 PRs
- Actual: 4 PRs/week ✅
```

### Quality Metrics

**Test Coverage:**
```markdown
- Overall: 92% (target: ≥85%) ✅
- Unit: 94% (target: ≥90%) ✅
- Integration: 87% (target: ≥80%) ✅
- Critical modules: 97% (target: ≥95%) ✅
```

**Defect Metrics:**
```markdown
**Bug Escape Rate:** Bugs in production
- Target: <2 per release
- Actual: 1.2 per release ✅

**Mean Time to Recover (MTTR):** Critical bug fix
- Target: <4 hours
- Actual: 2.3 hours ✅

**Security Findings:** Critical vulnerabilities
- Target: 0
- Actual: 0 ✅
```

### Process Adoption

**DDD/BDD/TDD Adherence:**
```markdown
**Documentation First:** % PRs with docs before code
- Target: 100%
- Actual: 98% ✅

**BDD Coverage:** % features with BDD scenarios
- Target: 100%
- Actual: 95% ✅

**TDD Practice:** % commits with test + implementation
- Target: ≥80%
- Actual: 87% ✅

**CI Success Rate:** % CI runs passing
- Target: ≥95%
- Actual: 97% ✅
```

### Production Health

**Uptime & Performance:**
```markdown
**Uptime:** Production availability
- Target: ≥99.5%
- Actual: 99.8% ✅

**p95 Latency:** 95th percentile response time
- Target: <500ms
- Actual: 287ms ✅

**Error Rate:** HTTP 5xx errors
- Target: <1%
- Actual: 0.3% ✅

**Throughput:** Requests per second
- Target: 100 req/s
- Actual: 147 req/s ✅
```

---

## Anti-Patterns to Avoid

### ❌ Phase 1: Vision & Strategy

**Anti-Pattern:** No strategic direction
```markdown
❌ BAD: "Just build whatever seems useful"
✅ GOOD: Clear roadmap with version milestones and success metrics
```

**Anti-Pattern:** Ignoring ecosystem
```markdown
❌ BAD: Build in isolation, discover conflicts later
✅ GOOD: Research integration patterns, coordinate with related projects
```

### ❌ Phase 2: Planning & Prioritization

**Anti-Pattern:** No clear sprint goals
```markdown
❌ BAD: "Work on whatever tasks are in backlog"
✅ GOOD: "Sprint 5 goal: Production workflows with template rendering"
```

**Anti-Pattern:** Over-committing
```markdown
❌ BAD: Plan 40 hours of work for 1-week sprint
✅ GOOD: Plan 60-70% capacity (24-28 hours for 1-week sprint)
```

### ❌ Phase 3: Requirements & Design

**Anti-Pattern:** Skipping DDD (coding first)
```markdown
❌ BAD: Start coding → Documentation as afterthought
✅ GOOD: Write API docs → Get approval → Then code
```

**Anti-Pattern:** Vague requirements
```markdown
❌ BAD: "Build a reporting feature"
✅ GOOD: "Generate daily git commit reports with template rendering,
         triggered by events, <5s execution time"
```

### ❌ Phase 4: Development

**Anti-Pattern:** Writing tests after code
```markdown
❌ BAD: Write code → Write tests → Discover design issues
✅ GOOD: Write test (RED) → Write code (GREEN) → Refactor
```

**Anti-Pattern:** Large, untested commits
```markdown
❌ BAD: 1500-line PR with no tests
✅ GOOD: Small incremental commits, each with tests, <500 lines per PR
```

### ❌ Phase 5: Testing & Quality

**Anti-Pattern:** "Tests pass, ship it"
```markdown
❌ BAD: Only run unit tests
✅ GOOD: Test pyramid - unit, smoke, integration, E2E, coverage, linting
```

**Anti-Pattern:** Ignoring flaky tests
```markdown
❌ BAD: "Test is flaky, just skip it"
✅ GOOD: Fix root cause (usually timing, mocking, or async issues)
```

### ❌ Phase 6: Review & Integration

**Anti-Pattern:** Rubber-stamp reviews
```markdown
❌ BAD: "LGTM" without actually reading code
✅ GOOD: Check functionality, design, tests, docs, edge cases
```

**Anti-Pattern:** Skipping CI/CD
```markdown
❌ BAD: Merge without waiting for CI
✅ GOOD: All CI stages GREEN before merge
```

### ❌ Phase 7: Release & Deployment

**Anti-Pattern:** Manual, error-prone releases
```markdown
❌ BAD: 15 manual commands, easy to make mistakes
✅ GOOD: `just release minor` (automated, consistent)
```

**Anti-Pattern:** No rollback plan
```markdown
❌ BAD: Deploy and hope for the best
✅ GOOD: Test rollback procedure, monitor metrics, ready to revert
```

### ❌ Phase 8: Monitoring & Feedback

**Anti-Pattern:** "Deploy and forget"
```markdown
❌ BAD: No monitoring after release
✅ GOOD: Active monitoring, alert on errors, track metrics, gather feedback
```

**Anti-Pattern:** Ignoring user feedback
```markdown
❌ BAD: Bug reports pile up, no response
✅ GOOD: Triage within 24h, prioritize by impact, communicate status
```

---

## Related Documentation

### Process Workflows
- [DDD_WORKFLOW.md](DDD_WORKFLOW.md) - Documentation Driven Design process
- [BDD_WORKFLOW.md](BDD_WORKFLOW.md) - Behavior Driven Development with Gherkin
- [TDD_WORKFLOW.md](TDD_WORKFLOW.md) - Test Driven Development (Red-Green-Refactor)
- [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md) - Integrated DDD→BDD→TDD→CI/CD flow
- [TESTING.md](TESTING.md) - Testing strategy and best practices
- [RELEASE.md](RELEASE.md) - Release and deployment procedures

### Strategic Planning
- [STRATEGIC_ROADMAP.md](../../project-docs/STRATEGIC_ROADMAP.md) - Multi-year vision and roadmap
- Sprint intent documents - Detailed sprint planning (e.g., sprint-15-v1.0.1-patch-intent.md)

### Reference
- [Tool Standards](../../docs/reference/api.md) - API design conventions
- [Contributing Guide](../../CONTRIBUTING.md) - How to contribute to the project
- [Code of Conduct](../../CODE_OF_CONDUCT.md) - Community guidelines

---

## Conclusion

This end-to-end process ensures that every feature journey—from strategic vision to production release—follows a consistent, quality-driven path. By combining:

1. **Strategic planning** (roadmaps, ecosystem alignment)
2. **Documentation-first design** (DDD)
3. **Behavior specifications** (BDD)
4. **Test-driven implementation** (TDD)
5. **Comprehensive testing** (test pyramid)
6. **Automated CI/CD** (quality gates)
7. **Reliable releases** (semantic versioning, automation)
8. **Production monitoring** (metrics, feedback loops)

We create a sustainable development process that delivers high-quality software while maintaining velocity and enabling continuous improvement.

**Key Principles:**
- ✅ Write the docs before the code
- ✅ Write the tests before the implementation
- ✅ Automate everything repeatable
- ✅ Monitor everything in production
- ✅ Iterate based on feedback

**Result:** Predictable, high-quality releases that delight users and maintain team velocity.

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintainer:** mcp-n8n core team
**Next Review:** 2025-11-25 (monthly)
