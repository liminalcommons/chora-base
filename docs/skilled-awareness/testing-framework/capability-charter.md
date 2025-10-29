# Capability Charter: Testing Framework

**SAP ID**: SAP-004
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides a comprehensive testing framework using **pytest + pytest-asyncio + pytest-cov**, but the framework lacks:

1. **Explicit Testing Contracts** - No documented guarantees about test structure, coverage, patterns
2. **Test Pattern Library** - Common testing patterns (fixtures, mocks, async tests) not catalogued
3. **Coverage Standards** - 85% threshold exists but rationale and measurement not documented
4. **Test Organization** - Test directory structure follows conventions but not explicitly specified
5. **Testing Workflow Integration** - How testing integrates with DDD → BDD → TDD not clear

**Result**:
- **Adopters**: Uncertain about testing standards, coverage expectations, best practices
- **AI Agents**: Can't reason about test quality or generate appropriate tests
- **Maintainers**: Can't enforce testing standards consistently
- **CI/CD**: Testing requirements not explicit, failures hard to interpret

### Evidence

**From adopter feedback**:
- "What test coverage should I aim for?" - No clear target beyond 85%
- "How do I test async MCP operations?" - Patterns not documented
- "Should I use mocks or real implementations?" - No guidance

**From agent behavior**:
- Agents generate tests but don't follow chora-base patterns
- Coverage checks fail but reasons unclear
- Async test patterns inconsistent
- Test organization varies by project

**From maintenance burden**:
- Test standard enforcement is manual
- Coverage regressions not caught early
- Test patterns reinvented per project
- BDD → TDD integration unclear

### Business Impact

Without structured testing framework:
- **Quality Risk**: Inconsistent test coverage (varies 60-95%)
- **Development Friction**: 2-4 hours to understand testing approach
- **Maintenance Overhead**: 30-60 min per test pattern explanation
- **CI/CD Issues**: 20% of CI failures due to test configuration issues

---

## 2. Proposed Solution

### Testing Framework SAP

A **comprehensive SAP describing chora-base's testing framework** with explicit contracts, patterns, and integration with development workflow.

This SAP documents:
1. **What gets tested** - Test structure, coverage requirements, test types
2. **How to write tests** - pytest patterns, fixtures, async tests, mocks
3. **What's guaranteed** - Test quality contracts (coverage ≥85%, all critical paths tested)
4. **How to run tests** - Local development, CI/CD, debugging
5. **How testing integrates** - DDD → BDD → TDD workflow

### Key Principles

1. **pytest-Based** - Modern Python testing with pytest plugins
2. **85% Coverage Minimum** - Based on industry best practices (80-85% optimal)
3. **Async-First** - MCP servers are async, tests must handle this
4. **Pattern-Driven** - Reusable fixtures, clear test organization
5. **CI-Integrated** - Tests run automatically, coverage reported

---

## 3. Scope

### In Scope

**Testing Framework SAP Artifacts**:
- ✅ Capability Charter (this document) - Problem, scope, outcomes
- ✅ Protocol Specification - Test structure, patterns, coverage contracts
- ✅ Awareness Guide - Agent workflows for writing tests, achieving coverage
- ✅ Adoption Blueprint - How to use testing framework, run tests, debug
- ✅ Traceability Ledger - Projects using testing framework, coverage tracking

**Components Covered**:
1. **pytest Configuration** (pyproject.toml [tool.pytest.ini_options])
2. **Test Structure** (tests/ directory, test_*.py files)
3. **Coverage Configuration** (pytest-cov, 85% threshold)
4. **Async Testing** (pytest-asyncio, async fixtures)
5. **Test Patterns** (parametrized tests, fixtures, mocks)
6. **CI Integration** (.github/workflows/test.yml)

### Out of Scope (for v1.0)

- ❌ End-to-end testing framework (covered by future SAP)
- ❌ Performance testing (covered by future SAP)
- ❌ Property-based testing (not used in chora-base yet)
- ❌ Mutation testing (advanced, future consideration)

---

## 4. Outcomes

### Success Criteria

**Testing Success** (Phase 2):
- ✅ SAP-004 complete (all 5 artifacts)
- ✅ All test patterns documented (fixtures, async, parametrized)
- ✅ Coverage standard explained (why 85%, how to measure)
- ✅ Agents can generate appropriate tests

**Quality Success** (Phase 2-3):
- ✅ 100% of generated projects have ≥85% coverage
- ✅ Test patterns consistent across projects
- ✅ Single source of truth for testing standards
- ✅ CI/CD test failures easily interpretable

**Maintenance Success** (Phase 3-4):
- ✅ Automated test pattern validation
- ✅ Coverage tracking across projects
- ✅ Test quality metrics (flakiness, speed)
- ✅ Continuous improvement of patterns

### Key Metrics

| Metric | Baseline | Target (Phase 2) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Test Coverage | 60-95% (varies) | ≥85% (all projects) | ≥85% (enforced) |
| Coverage Compliance | ~70% | 100% | 100% |
| Test Pattern Reuse | ~40% | 80% | 90% |
| CI Test Failures (config) | ~20% | <10% | <5% |
| Test Writing Time | 30-60 min/feature | 20-40 min/feature | 15-30 min/feature |

**Measurement**:
- **Coverage**: pytest --cov report
- **Compliance**: % of projects at ≥85%
- **Pattern Reuse**: % of tests using documented patterns
- **CI Failures**: % due to test config vs real issues
- **Writing Time**: Survey adopters

---

## 5. Stakeholders

### Primary Stakeholders

**Template Maintainer**:
- Victor (chora-base owner)
- Maintains testing framework standards
- Updates SAP-004 when testing changes

**AI Agents** (Write Tests):
- Claude Code (primary agent)
- Cursor Composer
- Other LLM-based agents
- Use SAP-004 to generate appropriate tests

**Project Developers** (Write Tests):
- chora-compose maintainer
- mcp-n8n maintainer
- Example project maintainers
- External adopters
- Use SAP-004 for testing guidance

### Secondary Stakeholders

**CI/CD System**:
- Runs tests automatically
- Enforces coverage thresholds
- Reports test results

**Quality Gatekeepers**:
- Code reviewers
- Pre-commit hooks
- Use SAP-004 standards for review

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure
- ✅ SAP-002 (chora-base-meta) - References SAP-004 as capability
- ✅ SAP-003 (project-bootstrap) - Generates test structure

**Capability Dependencies**:
- SAP-005 (ci-cd-workflows) - Test workflow uses testing framework
- SAP-006 (quality-gates) - Coverage gates use testing framework

**Documentation Dependencies**:
- pyproject.toml - pytest configuration
- .github/workflows/test.yml - Test workflow

### External Dependencies

**Testing Tools**:
- pytest 8.3.0 (test runner)
- pytest-asyncio 0.24.0 (async test support)
- pytest-cov 6.0.0 (coverage measurement)
- Python 3.11+ (async features)

**Standards**:
- pytest conventions (test_*.py, Test* classes)
- Coverage best practices (80-85% optimal)
- BDD principles (given-when-then)

---

## 7. Constraints & Assumptions

### Constraints

1. **pytest Required**: Must use pytest (not unittest, nose)
2. **Async Support Required**: MCP servers are async, tests must be too
3. **85% Coverage Minimum**: Industry standard for production code
4. **Fast Tests**: Tests must complete in <60 seconds for dev workflow

### Assumptions

1. **Async Pattern Stable**: pytest-asyncio patterns won't change significantly
2. **Coverage Meaningful**: 85% line coverage approximates branch coverage
3. **Agent Capability**: Agents can write tests following documented patterns
4. **CI/CD Available**: Projects use GitHub Actions or equivalent

---

## 8. Risks & Mitigation

### Risk 1: Coverage Gaming

**Risk**: Developers achieve 85% coverage with meaningless tests

**Likelihood**: Medium
**Impact**: High (false confidence in quality)

**Mitigation**:
- Document meaningful testing patterns (not just coverage)
- Review tests for assertions, not just execution
- Track test quality metrics (assertions per test)
- Agent validation of test meaningfulness

### Risk 2: Slow Test Suite

**Risk**: Test suite grows too large, slows development

**Likelihood**: Medium
**Impact**: Medium (frustrates developers)

**Mitigation**:
- Document fast test patterns (mocks vs real implementations)
- Measure test suite speed (target <60s)
- Separate unit vs integration tests
- Parallelize tests in CI

### Risk 3: Flaky Async Tests

**Risk**: Async tests intermittently fail due to timing issues

**Likelihood**: Medium
**Impact**: Medium (erodes trust in tests)

**Mitigation**:
- Document robust async patterns (proper fixtures, timeouts)
- Avoid sleep(), use proper async primitives
- Track flakiness metrics
- Agent awareness of flaky patterns

### Risk 4: Pattern Drift

**Risk**: Test patterns diverge from SAP-004 documentation

**Likelihood**: Low
**Impact**: Medium (inconsistency)

**Mitigation**:
- Automated pattern validation (future)
- Regular SAP-004 updates
- Code review against patterns
- Agent pattern enforcement

---

## 9. Lifecycle

### Phase 2: Core Capability SAPs (2025-11 → 2026-01)

**Goal**: Create SAP-004 (testing-framework) second in dependency chain

**Deliverables**:
- ✅ Capability Charter (this document)
- 🔄 Protocol Specification (test structure, patterns, contracts)
- 🔄 Awareness Guide (agent workflows for writing tests)
- 🔄 Adoption Blueprint (how to use testing framework)
- 🔄 Traceability Ledger (coverage tracking)

**Success**: SAP-004 complete, foundational for SAP-005/006

### Phase 3: Extended Coverage (2026-01 → 2026-03)

**Goal**: Enhance SAP-004 with advanced patterns

**Deliverables**:
- Advanced test patterns (property-based, mutation)
- Performance testing integration
- Test quality metrics
- Coverage improvement workflows

**Success**: SAP-004 covers advanced testing scenarios

### Phase 4: Automation & Optimization (2026-03 → 2026-05)

**Goal**: Automate test quality validation

**Deliverables**:
- Automated pattern validation
- Test quality dashboard
- Coverage tracking across projects
- Test performance optimization

**Success**: SAP-004 validation automated, metrics tracked

---

## 10. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000 (framework SAP)
- [INDEX.md](../INDEX.md) - SAP registry
- [document-templates.md](../document-templates.md) - SAP templates

**chora-base Core**:
- [README.md](../../../../README.md) - Project overview
- [AGENTS.md](../../../../AGENTS.md) - Agent guidance
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP (Section 3.2.2)

**Testing Components**:
- [pyproject.toml](../../../../blueprints/pyproject.toml.blueprint) - pytest configuration (lines 45-50)
- [static-template/tests/](../../../../static-template/tests/) - Test examples
- [.github/workflows/test.yml](../../../../static-template/.github/workflows/test.yml) - Test workflow

**Related SAPs**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (runs tests in CI)
- [quality-gates/](../quality-gates/) - SAP-006 (enforces coverage)

**Development Process**:
- [static-template/dev-docs/workflows/TDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/TDD_WORKFLOW.md) - TDD workflow
- [static-template/dev-docs/workflows/BDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/BDD_WORKFLOW.md) - BDD workflow

---

## 11. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-28
**Review Cycle**: Quarterly (align with template releases)

**Next Review**: 2026-01-31 (end of Phase 2)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for testing-framework SAP
