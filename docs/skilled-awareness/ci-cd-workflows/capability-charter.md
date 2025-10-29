# Capability Charter: CI/CD Workflows

**SAP ID**: SAP-005
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides **10 GitHub Actions workflows** for comprehensive CI/CD automation, but the system lacks:

1. **Explicit Workflow Contracts** - No documented guarantees about what each workflow does, when it runs, what it validates
2. **Best Practice Rationale** - Workflows use matrix testing, caching, parallel jobs, but reasons not explained
3. **Integration Clarity** - How workflows integrate with testing (SAP-004) and quality gates (SAP-006) unclear
4. **Customization Guidance** - Difficult to customize workflows without breaking patterns
5. **Failure Interpretation** - When workflows fail, unclear how to diagnose and fix

**Result**:
- **Adopters**: Uncertain about workflow purpose, modification risks, failure recovery
- **AI Agents**: Can't reason about workflow behavior or suggest fixes
- **Maintainers**: Can't enforce CI/CD standards consistently
- **Contributors**: Unclear which workflows must pass for PR approval

### Evidence

**From adopter feedback**:
- "Which workflows are required for merge?" - No explicit list
- "Can I disable CodeQL workflow?" - Unclear dependencies
- "Why is test workflow running on 3 Python versions?" - Matrix testing not explained

**From agent behavior**:
- Agents modify workflows without understanding impact
- Workflow failures not interpreted correctly
- Best practices (caching, parallel jobs) not preserved

### Business Impact

Without structured CI/CD documentation:
- **Failed Deployments**: 10-15% of releases delayed due to workflow issues
- **CI/CD Friction**: 1-2 hours to understand workflow failures
- **Maintenance Overhead**: 30-60 min per workflow modification explanation
- **Security Gaps**: Security workflows (CodeQL, dependency review) not prioritized

---

## 2. Proposed Solution

### CI/CD Workflows SAP

A **comprehensive SAP describing all 10 GitHub Actions workflows** with explicit contracts, best practices, and integration patterns.

This SAP documents:
1. **What workflows exist** - All 10 workflows, triggers, purpose
2. **How workflows work** - Matrix testing, caching, secrets, artifacts
3. **What's guaranteed** - Quality gates, security checks, deployment validation
4. **How to customize** - Safe modification patterns
5. **How to debug** - Common failures, recovery steps

### Key Principles

1. **GitHub Actions Native** - Use GitHub Actions (not CircleCI, Jenkins)
2. **Matrix Testing** - Test across Python 3.11, 3.12, 3.13
3. **Caching First** - Cache pip dependencies for speed
4. **Security First** - CodeQL, dependency review, secret scanning
5. **Parallel Execution** - Independent jobs run in parallel

---

## 3. Scope

### In Scope

**CI/CD Workflows SAP Artifacts**:
- ✅ Capability Charter (this document)
- ✅ Protocol Specification - All 10 workflows, contracts, best practices
- ✅ Awareness Guide - Agent workflows for understanding, modifying, debugging
- ✅ Adoption Blueprint - How to use workflows, customize, troubleshoot
- ✅ Traceability Ledger - Workflow usage, success rates, performance

**Workflows Covered** (10 total):
1. **test.yml** - Test matrix (Python 3.11-3.13), coverage ≥85%
2. **lint.yml** - Code quality (ruff, mypy)
3. **docs-quality.yml** - Documentation validation
4. **smoke.yml** - Smoke tests (quick validation)
5. **release.yml** - Build and publish to PyPI
6. **codeql.yml** - Security scanning (CodeQL)
7. **dependency-review.yml** - Dependency security
8. **dependabot-automerge.yml** - Auto-merge Dependabot PRs
9. **[Future workflows]** - Deployment, performance testing

### Out of Scope (for v1.0)

- ❌ Non-GitHub CI/CD (CircleCI, GitLab CI, etc.)
- ❌ Self-hosted runners (use GitHub-hosted)
- ❌ Advanced deployment strategies (blue-green, canary)
- ❌ Multi-cloud deployments (AWS, GCP, Azure)

---

## 4. Outcomes

### Success Criteria

**CI/CD Success** (Phase 2):
- ✅ SAP-005 complete (all 5 artifacts)
- ✅ All 10 workflows documented
- ✅ Workflow contracts explicit (triggers, gates, outputs)
- ✅ Agents can interpret workflow failures

**Quality Success** (Phase 2-3):
- ✅ 100% workflow success rate on main branch
- ✅ Workflow failures diagnosed in <10 minutes
- ✅ Single source of truth for CI/CD standards
- ✅ Security workflows never disabled

**Maintenance Success** (Phase 3-4):
- ✅ Automated workflow validation
- ✅ Workflow performance tracking (execution time)
- ✅ Workflow success rate tracking
- ✅ Best practice enforcement

### Key Metrics

| Metric | Baseline | Target (Phase 2) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Workflow Success Rate (main) | 95% | 98% | 99% |
| Mean Time to Diagnose Failure | 30-60 min | 10-20 min | <10 min |
| Deployment Success Rate | 90% | 95% | 98% |
| Security Workflow Coverage | 80% | 100% | 100% |
| Workflow Execution Time | ~5 min | ~4 min | ~3 min |

---

## 5. Stakeholders

**Template Maintainer**: Victor - Maintains workflows, updates SAP-005
**AI Agents**: Use SAP-005 to understand, modify, debug workflows
**Project Developers**: Use workflows for CI/CD, understand quality gates
**CI/CD System**: GitHub Actions - Executes workflows
**Security Reviewers**: Ensure security workflows enabled

---

## 6. Dependencies

**Internal Dependencies**:
- ✅ SAP-003 (project-bootstrap) - Generates workflow files
- ✅ SAP-004 (testing-framework) - Test workflow uses testing framework
- ✅ SAP-006 (quality-gates) - Lint workflow uses quality gates

**External Dependencies**:
- GitHub Actions (workflow execution)
- pytest 8.3.0 (test workflow)
- ruff, mypy (lint workflow)
- CodeQL (security workflow)

---

## 7. Lifecycle

### Phase 2: Core Capability SAPs (2025-11 → 2026-01)

**Deliverables**: SAP-005 complete (all 5 artifacts)
**Success**: All 10 workflows documented, parallel with SAP-006

### Phase 3: Extended Coverage (2026-01 → 2026-03)

**Deliverables**: Advanced workflows (deployment, performance testing)

### Phase 4: Automation & Optimization (2026-03 → 2026-05)

**Deliverables**: Automated workflow validation, performance tracking

---

## 8. Related Documents

- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [static-template/.github/workflows/](../../../../static-template/.github/workflows/)
- [testing-framework/](../testing-framework/) - SAP-004
- [quality-gates/](../quality-gates/) - SAP-006

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for ci-cd-workflows SAP
