---
sap_id: SAP-056
version: 1.0.0
status: Draft
last_updated: 2025-11-16
scope: Governance
type: explanation
feature_id: FEAT-SAP-056
requirement_refs:
  - REQ-SAP-056-001
  - REQ-SAP-056-007
  - REQ-SAP-056-008
---

# SAP-056: Lifecycle Traceability

**Capability**: lifecycle-traceability
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Scope**: Governance

> **Mission**: Establish comprehensive traceability across the entire development lifecycle—from vision to deployment—enabling teams to answer "why does this code exist?", "is requirement X implemented?", and "what would break if I change feature Y?" in under 1 minute instead of 15-30 minutes.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Problem Statement](#2-problem-statement)
3. [Solution Overview](#3-solution-overview)
4. [Adoption Levels](#4-adoption-levels)
5. [Integration Points](#5-integration-points)
6. [Getting Started](#6-getting-started)
7. [Quality Gates](#7-quality-gates)
8. [Version History](#8-version-history)
9. [Related SAPs](#9-related-saps)

---

## 1. Overview

### What is SAP-056?

SAP-056 (Lifecycle Traceability) is an **umbrella governance SAP** that defines linkage schemas, validation rules, and compliance levels for tracing artifacts across 10 lifecycle stages:

**Vision → Features → Requirements → Code → Tests → Docs → Git Commits → Tasks → Events → Knowledge**

**Scope**: Governance only—SAP-056 does NOT implement traceability mechanisms. Instead, it delegates to existing SAPs with enhancement specifications:
- **SAP-004** (testing-framework): Pytest markers for requirement/feature traceability
- **SAP-007** (documentation-framework): Frontmatter fields for doc linkage
- **SAP-010** (memory-system): Event correlation with feature_id
- **SAP-012** (development-lifecycle): Feature manifest creation in DDD→BDD→TDD
- **SAP-015** (task-tracking): Git commit→task linkage validation

### Why SAP-056?

**Current State**: ~40% traceability coverage across chora ecosystem
- Strong: Code→Tests (85%), Tests→Docs, Git→Tasks (via SAP-015 L3-L4)
- Weak: Vision→Features (no linkage), Features→Requirements (no artifacts), Requirements→Code (no mechanism)

**Impact**:
- ❌ Context restoration takes 15-30 minutes (manual grep/git log)
- ❌ Impact analysis impossible without manual review (1-2 hours)
- ❌ Compliance audits manual (4+ hours quarterly)
- ❌ Orphaned artifacts (code without requirements, docs drift from code)

**With SAP-056**:
- ✅ Context restoration <1 minute (query feature manifest)
- ✅ Impact analysis automated (<5 min via dependency graph)
- ✅ Compliance validated (100% requirements → tests → code → docs)
- ✅ Zero orphaned artifacts (validation rules detect)

**ROI**: 93+ hours saved annually per project, break-even at 6-8 months

### Key Principles

1. **Governance, Not Implementation**: SAP-056 defines schemas and validates compliance, but existing SAPs implement traceability
2. **Machine-Readable Manifests**: feature-manifest.yaml provides single source of truth
3. **Bidirectional Linkage**: If doc references code, code manifest MUST list doc (prevents drift)
4. **Evidence Requirement**: Every feature MUST have ≥1 test AND ≥1 doc (completeness enforced)
5. **Automated Validation**: Pre-commit hooks + CI/CD enforce traceability (not manual)

---

## 2. Problem Statement

### Current Traceability Gaps

Development artifacts exist in isolation across the chora ecosystem:

**7 Critical Gaps** (from gap analysis):
1. **Vision → Features**: No machine-readable linkage between vision outcomes and feature implementations
2. **Features → Requirements**: No formal requirement artifact in current workflow
3. **Requirements → Code**: No linkage mechanism from requirements to implementing code files
4. **Code → Features**: No feature manifest to group related code/tests/docs
5. **Git Commits → Features**: Commits link to tasks but not features (no feature context)
6. **Tasks → Features**: Beads tasks don't reference feature IDs (isolation)
7. **Knowledge → Features**: Knowledge notes don't link to features they document

### User Pain Points

**From traceability research (2025-11-16)**:
> "How can we ensure traceability along our entire development lifecycle, including beads? Do our SAPs already mandate traceability?"

**Specific Issues**:
1. **Context restoration takes 15-30 minutes**: Developers manually search git logs, beads tasks, docs to understand "why this code exists"
2. **Impact analysis impossible**: Can't identify "what would break if I change feature X?" without manual code review (1-2 hours)
3. **Compliance audits manual**: Quarterly audits take 4+ hours to verify all requirements implemented with tests and docs
4. **Feature queries slow**: Finding "all code/tests/docs for feature Y" requires grep across multiple locations (10-20 minutes)
5. **Orphaned artifacts**: Code exists without linkage to requirements, tasks created without features, docs drift from code

### Measured Impact

**Baseline Metrics** (pre-SAP-056):
- Context restoration: 15-30 minutes (manual grep/git log)
- Impact analysis: 60+ minutes (manual code review)
- Compliance audit: 4+ hours quarterly (manual verification)
- Traceability coverage: ~40%

**Target Metrics** (post-SAP-056):
- Context restoration: <1 minute (feature manifest query)
- Impact analysis: <5 minutes (dependency graph)
- Compliance audit: <30 minutes quarterly (automated validation)
- Traceability coverage: 100%

**Projected ROI**: 93+ hours saved annually per project

---

## 3. Solution Overview

### Architecture

SAP-056 provides a **governance framework** with 4 core components:

#### 3.1 Linkage Schema (10 Artifact Types)

```
Vision Document (CHARTER-XXX)
    ↓ vision_ref
Feature (FEAT-XXX) ← feature-manifest.yaml (single source of truth)
    ↓ requirements[]
Requirements (REQ-XXX)
    ↓ code[]
Code Files (src/*.py)
    ↓ tests[]
Test Cases (tests/test_*.py::test_name)
    ↓ pytest markers
Requirements (validation loop)
    ↓ documentation[]
Documentation (docs/*.md)
    ↓ frontmatter
Feature (bidirectional loop)
    ↓ git commits
Git Commits (feat(scope): message [task-id])
    ↓ task_id
Tasks (.beads-XXXX)
    ↓ A-MEM events
Events (task.completed with feature_id)
    ↓ wikilinks
Knowledge Notes ([[feature-id]])
```

#### 3.2 Feature Manifest Schema

Central artifact: `feature-manifest.yaml` (git-committed, machine-readable)

```yaml
features:
  - id: FEAT-001
    name: "User Authentication"
    vision_ref: "CHARTER-001:Outcome-2"
    status: implemented
    requirements:
      - id: REQ-001
        description: "Support email/password login"
        status: implemented
    code:
      - path: src/auth/providers.py
        lines: "45-120"
    tests:
      - path: tests/test_auth.py::test_email_login
        type: unit
        requirement: REQ-001
      - path: tests/test_auth_integration.py::test_full_auth_flow
        type: integration
        requirement: REQ-001
    documentation:
      - path: docs/how-to/authentication.md
        type: how-to
```

#### 3.3 Validation Rules (10 Core Rules)

1. **Forward Linkage**: Every vision outcome → ≥1 feature
2. **Bidirectional Linkage**: If doc references code, code manifest lists doc
3. **Evidence Requirement**: Every feature → ≥1 test AND ≥1 doc
4. **Closed Loop**: Every git commit closing task → links to feature
5. **Orphan Detection**: No artifact without parent linkage
6. **Schema Compliance**: feature-manifest.yaml passes JSON Schema validation
7. **Reference Integrity**: All vision_ref/code/docs/tests paths exist
8. **Requirement Coverage**: Every requirement → ≥1 test with marker
9. **Documentation Coverage**: Every feature → ≥1 doc in frontmatter
10. **Event Correlation**: Every task completion → A-MEM event with feature_id

#### 3.4 Compliance Levels (L0-L3)

| Level | Name | Coverage | Validation Rules | Automation |
|-------|------|----------|------------------|------------|
| **L0** | No Traceability | 0% | None | None |
| **L1** | Partial | ~50% | Rules 1, 3, 6, 7 | Manual validation |
| **L2** | Substantial | ~80% | Rules 1-9 | Pre-commit hooks |
| **L3** | Complete | 100% | Rules 1-10 | CI/CD enforcement |

**Target**: 80% of adopters at L2+ within 6 months

### What SAP-056 Includes

**Governance Artifacts**:
- [capability-charter.md](capability-charter.md) - Problem statement, stakeholders, proposed solution
- [protocol-spec.md](protocol-spec.md) - Linkage schemas, validation rules, integration specs
- [awareness-guide.md](awareness-guide.md) - Agent execution patterns for traceability
- [adoption-blueprint.md](adoption-blueprint.md) - L0→L4 adoption steps with time estimates
- [ledger.md](ledger.md) - Adopter tracking, version history, enhancement requests
- This file (README.md) - 9-section overview

**Schemas**:
- schemas/feature-manifest.yaml - JSON Schema for feature-manifest.yaml validation
- schemas/traceability-frontmatter.yaml - Frontmatter validation for documentation

**Automation Scripts**:
- scripts/validate-traceability.py - Comprehensive validation (10 rules), markdown report
- scripts/generate-feature-manifest.py - Auto-generate manifest from git log + beads queries
- scripts/traceability-dashboard.py - HTML dashboard for metrics visualization

**Templates**:
- templates/feature-manifest.j2 - Jinja2 template for creating feature entries

### What SAP-056 Excludes

- **Implementing traceability** in specific SAPs (covered by enhancement PRs to SAP-004, SAP-007, SAP-010, SAP-012, SAP-015)
- **Real-time dashboards** (future enhancement, Phase 2)
- **Cross-repository traceability** (future enhancement, Phase 3)
- **Automated traceability restoration** after git operations (future enhancement, Phase 4)
- **AI-assisted impact analysis** (future enhancement, Phase 5)

---

## 4. Adoption Levels

SAP-056 defines 4 maturity levels (L0-L3) with clear progression paths.

### Level 0: Aware (No Traceability)

**Characteristics**:
- No feature-manifest.yaml
- No frontmatter in documentation
- No pytest markers for traceability
- Manual context restoration (15-30 min)

**Adoption Time**: N/A (starting point)

---

### Level 1: Pilot (Partial Traceability)

**Characteristics**:
- feature-manifest.yaml created for 1-3 features
- Vision→Features linkage established (vision_ref field)
- Code→Tests linkage via manifest (code[] and tests[] arrays)
- Manual validation (scripts/validate-traceability.py)

**Validation Rules**: 1, 3, 6, 7 (forward linkage, evidence, schema, integrity)

**Adoption Time**: 2-4 hours (first feature)

**Success Criteria**:
- ✅ feature-manifest.yaml exists and passes schema validation
- ✅ ≥1 feature with vision_ref, code, tests, docs
- ✅ Validation script runs (manual execution)

**Example Use Case**: Pilot feature "User Authentication" with complete manifest

---

### Level 2: Configured (Substantial Traceability)

**Characteristics**:
- feature-manifest.yaml covers 5+ features
- Features→Requirements linkage established (requirements[] array)
- Docs→Code bidirectional linkage (frontmatter feature_id + code_references)
- Git hooks for validation (pre-commit)

**Validation Rules**: 1-9 (all except event correlation)

**Adoption Time**: 8-12 hours (extending manifest, adding frontmatter, setting up hooks)

**Success Criteria**:
- ✅ ≥5 features documented in manifest
- ✅ Frontmatter present in ≥50% of documentation files
- ✅ Pre-commit hook validates manifest on every commit
- ✅ Validation script pass rate ≥80%

**Example Use Case**: Core authentication + authorization + session management features traced

---

### Level 3: Active (Complete Traceability)

**Characteristics**:
- feature-manifest.yaml covers 100% of features
- Git→Tasks→Events→Knowledge fully traced
- CI/CD enforces validation (blocks merge on failures)
- Automated manifest generation (scripts/generate-feature-manifest.py)

**Validation Rules**: 1-10 (all rules, including event correlation)

**Adoption Time**: 20-30 hours (extending to all features, CI/CD integration, automation)

**Success Criteria**:
- ✅ 100% feature coverage in manifest
- ✅ Validation script pass rate 100%
- ✅ CI/CD pipeline blocks merges with broken traceability
- ✅ Zero orphaned artifacts detected

**Example Use Case**: Entire project traceable from vision to knowledge notes

---

### Level 4: Community (Future)

**Characteristics** (Planned):
- Real-time traceability dashboard
- Cross-repository traceability (chora-workspace → chora-base)
- AI-assisted impact analysis
- Community contributions to validation rules

**Adoption Time**: 40-60 hours (dashboard, cross-repo linkage, advanced analytics)

**Status**: Not yet defined (future enhancement)

---

## 5. Integration Points

SAP-056 integrates with 5 existing SAPs via enhancement specifications.

### 5.1 SAP-004 (testing-framework)

**Enhancement**: Pytest markers for requirement/feature traceability

**Integration**:
- Add pytest markers: `@pytest.mark.feature("FEAT-XXX")`, `@pytest.mark.requirement("REQ-XXX")`
- Coverage reporting: `pytest --cov --feature FEAT-001` shows tests for feature
- Validation: `scripts/validate-traceability.py` checks marker presence

**Example**:
```python
import pytest

@pytest.mark.feature("FEAT-001")
@pytest.mark.requirement("REQ-001")
def test_email_login():
    """Test email/password login flow."""
    # ...
```

**Status**: Enhancement needed (PR to SAP-004)

---

### 5.2 SAP-007 (documentation-framework)

**Enhancement**: Frontmatter fields for traceability

**Integration**:
- Add frontmatter fields: `feature_id`, `code_references`, `test_references`
- Bidirectional validation: If doc lists code_references, code manifest MUST list doc
- Schema validation: `schemas/traceability-frontmatter.yaml`

**Example**:
```yaml
---
title: "How to Implement Authentication"
feature_id: FEAT-001
code_references:
  - src/auth/providers.py
  - src/auth/middleware.py
test_references:
  - tests/test_auth.py::test_email_login
last_updated: 2025-11-16
---
```

**Status**: Enhancement needed (PR to SAP-007)

---

### 5.3 SAP-010 (memory-system)

**Enhancement**: Event correlation with feature_id

**Integration**:
- Add `feature_id` field to all development events (task.completed, feature.implemented, etc.)
- Event query by feature: `grep "feature_id.*FEAT-001" .chora/memory/events/*.jsonl`
- Validation: Rule 10 checks task completion events include feature_id

**Example Event**:
```json
{
  "timestamp": "2025-11-16T14:30:00Z",
  "trace_id": "sap-056-creation",
  "event_type": "task.completed",
  "status": "success",
  "task_id": ".beads-i6mf",
  "feature_id": "FEAT-SAP-056",
  "metadata": {
    "description": "Created SAP-056 capability-charter.md"
  }
}
```

**Status**: Enhancement needed (PR to SAP-010)

---

### 5.4 SAP-012 (development-lifecycle)

**Enhancement**: Feature manifest creation integrated into DDD→BDD→TDD

**Integration**:
- During feature planning (DDD phase): Create feature entry in manifest with requirements
- During test writing (BDD→TDD phase): Add test cases to manifest tests[] array
- During implementation: Add code files to manifest code[] array
- Documentation phase: Add docs to manifest documentation[] array

**Workflow**:
```bash
# 1. Plan feature (DDD)
just feature-new "User Authentication"  # Creates manifest entry

# 2. Write tests (BDD→TDD)
pytest tests/test_auth.py  # Tests marked with @pytest.mark.feature

# 3. Implement (TDD)
# Code written, added to manifest code[] array

# 4. Document
# Docs created with frontmatter feature_id

# 5. Validate
just validate-traceability  # Ensure all linkages present
```

**Status**: Enhancement needed (PR to SAP-012)

---

### 5.5 SAP-015 (task-tracking)

**Enhancement**: Traceability validation subcommand in beads CLI

**Integration**:
- Add `bd validate-traceability` subcommand
- Check git commits for task IDs: `feat(scope): message [.beads-abc123]`
- Verify task→feature linkage via feature manifest
- Report orphaned tasks (no feature linkage)

**Example**:
```bash
bd validate-traceability
# Output:
# ✅ Rule 4 (Closed Loop): 45/45 commits link to tasks (100%)
# ✅ Task→Feature: 42/45 tasks link to features (93%)
# ⚠️ Orphaned tasks: 3 tasks without feature linkage
#   - .beads-xyz1 (Fix typo in README)
#   - .beads-xyz2 (Update dependencies)
#   - .beads-xyz3 (Refactor tests)
```

**Status**: Enhancement needed (PR to SAP-015)

---

## 6. Getting Started

### 6.1 Prerequisites

- **chora-base adoption**: Project must use chora-base as template
- **SAP-015 (task-tracking)**: Beads at L1+ for git→task linkage
- **SAP-010 (memory-system)**: A-MEM for event correlation (optional for L1-L2, required for L3)
- **Python 3.8+**: For validation scripts
- **Git hooks**: For pre-commit validation (L2+)

### 6.2 Quick Start (L0→L1 in 2-4 hours)

**Step 1: Create feature-manifest.yaml**

```bash
# Copy template to project root
cp chora-base/docs/skilled-awareness/lifecycle-traceability/templates/feature-manifest.j2 feature-manifest.yaml
```

**Step 2: Document first feature**

Edit `feature-manifest.yaml`:
```yaml
version: 1.0.0
project: my-project
features:
  - id: FEAT-001
    name: "My First Traced Feature"
    vision_ref: "CHARTER-001:Outcome-1"
    status: implemented
    requirements:
      - id: REQ-001
        description: "Feature requirement description"
        status: implemented
    code:
      - path: src/my_feature.py
    tests:
      - path: tests/test_my_feature.py::test_feature_works
        type: unit
        requirement: REQ-001
    documentation:
      - path: docs/how-to/my-feature.md
        type: how-to
```

**Step 3: Validate manifest**

```bash
# Run validation script
python chora-base/docs/skilled-awareness/lifecycle-traceability/scripts/validate-traceability.py

# Expected output:
# ✅ Rule 1 (Forward Linkage): 1/1 features have vision_ref (100%)
# ✅ Rule 3 (Evidence): 1/1 features have tests and docs (100%)
# ✅ Rule 6 (Schema): feature-manifest.yaml valid
# ✅ Rule 7 (Integrity): All paths exist
```

**Step 4: Verify L1 adoption**

```bash
# Check success criteria
- [ ] feature-manifest.yaml exists
- [ ] Passes schema validation
- [ ] ≥1 feature documented
- [ ] Validation script runs without errors
```

**Congratulations! You're at L1 (Pilot).**

### 6.3 Progression Paths

**L1→L2** (8-12 hours):
1. Extend manifest to 5+ features
2. Add frontmatter to documentation (feature_id, code_references)
3. Set up pre-commit hooks for validation
4. Achieve 80% validation pass rate

See [adoption-blueprint.md](adoption-blueprint.md) for detailed steps.

**L2→L3** (20-30 hours):
1. Extend manifest to 100% feature coverage
2. Integrate with CI/CD (block merges on validation failures)
3. Add event correlation (feature_id in A-MEM events)
4. Automate manifest generation

See [adoption-blueprint.md](adoption-blueprint.md) for detailed steps.

---

## 7. Quality Gates

SAP-056 defines quality gates for each adoption level to ensure consistent implementation.

### 7.1 Level 1 Quality Gates

**Required**:
- ✅ feature-manifest.yaml exists in project root
- ✅ Manifest passes JSON Schema validation
- ✅ ≥1 feature documented with vision_ref, code, tests, docs
- ✅ Validation script runs without errors
- ✅ Rule 1 (Forward Linkage): 100% pass
- ✅ Rule 3 (Evidence): 100% pass (all features have tests + docs)
- ✅ Rule 6 (Schema): Manifest validates against schemas/feature-manifest.yaml
- ✅ Rule 7 (Integrity): All file paths exist

**Optional**:
- 🔵 Frontmatter in documentation (for L2 preparation)
- 🔵 Git hooks for validation (for L2 preparation)

**Time to Achieve**: 2-4 hours (first feature)

---

### 7.2 Level 2 Quality Gates

**Required** (all L1 gates PLUS):
- ✅ ≥5 features documented in manifest
- ✅ Frontmatter present in ≥50% of documentation files
- ✅ Pre-commit hook validates manifest on every commit
- ✅ Validation script pass rate ≥80%
- ✅ Rule 2 (Bidirectional): 100% pass (docs ↔ code bidirectional linkage)
- ✅ Rule 4 (Closed Loop): ≥70% pass (commits → tasks → features)
- ✅ Rule 8 (Requirement Coverage): ≥80% pass (requirements → tests)
- ✅ Rule 9 (Documentation Coverage): 100% pass (features → docs)

**Optional**:
- 🔵 CI/CD integration (for L3 preparation)
- 🔵 Event correlation with feature_id (for L3 preparation)

**Time to Achieve**: 8-12 hours (extending from L1)

---

### 7.3 Level 3 Quality Gates

**Required** (all L2 gates PLUS):
- ✅ 100% feature coverage in manifest
- ✅ Validation script pass rate 100% (all 10 rules)
- ✅ CI/CD pipeline blocks merges with broken traceability
- ✅ Zero orphaned artifacts detected
- ✅ Rule 5 (Orphan Detection): 100% pass (no artifacts without parent)
- ✅ Rule 10 (Event Correlation): ≥90% pass (task completions → A-MEM events with feature_id)
- ✅ Automated manifest generation available (scripts/generate-feature-manifest.py)

**Optional**:
- 🔵 Real-time dashboard (for L4 preparation)
- 🔵 Cross-repository traceability (for L4 preparation)

**Time to Achieve**: 20-30 hours (extending from L2)

---

### 7.4 Validation Checklist (All Levels)

Use this checklist to verify compliance:

```bash
# Run comprehensive validation
python chora-base/docs/skilled-awareness/lifecycle-traceability/scripts/validate-traceability.py --output report.md

# Review report.md for pass/fail per rule
# Expected output:
# ✅ Rule 1 (Forward Linkage): 15/15 features (100%)
# ✅ Rule 2 (Bidirectional): 42/42 docs (100%)
# ✅ Rule 3 (Evidence): 15/15 features (100%)
# ...
# ⚠️ Rule 10 (Event Correlation): 12/15 tasks (80%)

# Fix failures, re-run validation
```

---

## 8. Version History

### Version 1.0.0 (Draft) - 2025-11-16

**Status**: Draft (not yet released)

**Created**: Initial SAP-056 creation

**Artifacts**:
- capability-charter.md (266 lines) - Problem statement, stakeholders, solution
- protocol-spec.md (1060 lines) - Linkage schemas, validation rules, integration specs
- awareness-guide.md (620 lines) - Agent execution patterns
- adoption-blueprint.md (870 lines) - L0→L4 adoption steps with time estimates
- ledger.md (395 lines) - Adopter tracking, version history
- README.md (this file) - 9-section overview
- schemas/feature-manifest.yaml - JSON Schema for validation
- schemas/traceability-frontmatter.yaml - Frontmatter validation
- scripts/validate-traceability.py - Comprehensive validation (10 rules)
- scripts/generate-feature-manifest.py - Auto-generate manifest from git/beads
- scripts/traceability-dashboard.py - HTML dashboard for metrics
- templates/feature-manifest.j2 - Jinja2 template

**Key Features**:
- Traceability governance framework (10 artifact types)
- Feature manifest schema (YAML-based)
- 10 validation rules for completeness
- 3 compliance levels (L0-L3)
- Integration specifications for 5 SAPs
- Automation scripts for validation, generation, dashboard

**Known Limitations**:
- No real-time dashboard (planned Phase 2)
- No cross-repository traceability (planned Phase 3)
- No automated traceability restoration (planned Phase 4)
- No AI-assisted impact analysis (planned Phase 5)

**Breaking Changes**: None (initial version)

**Deprecations**: None

---

## 9. Related SAPs

### 9.1 Upstream Dependencies

| SAP | Capability | Relationship |
|-----|------------|--------------|
| [SAP-000](../../sap-framework/README.md) | sap-framework | Provides SAP structure and governance |
| [SAP-004](../../testing-framework/README.md) | testing-framework | Pytest conventions for test markers |
| [SAP-007](../../documentation-framework/README.md) | documentation-framework | Frontmatter schema for doc linkage |
| [SAP-010](../../memory-system/README.md) | memory-system | Event correlation via trace_id |
| [SAP-012](../../development-lifecycle/README.md) | development-lifecycle | Feature/sprint/theme chains |
| [SAP-015](../../task-tracking/README.md) | task-tracking | Git commit→task linkage via beads |

### 9.2 Downstream Dependencies

| SAP | Enhancement Needed | Status |
|-----|-------------------|--------|
| SAP-004 | Pytest markers + coverage reporting | PR needed |
| SAP-007 | Frontmatter traceability fields | PR needed |
| SAP-010 | Feature completion events + feature_id | PR needed |
| SAP-012 | Feature manifest workflow integration | PR needed |
| SAP-015 | Traceability validation subcommand | PR needed |

### 9.3 Complementary SAPs

| SAP | Capability | How It Helps |
|-----|------------|--------------|
| [SAP-019](../../sap-self-evaluation/README.md) | sap-self-evaluation | Traceability maturity assessment |
| [SAP-027](../../dogfooding-patterns/README.md) | dogfooding-patterns | 5-week pilot methodology for SAP-056 validation |

---

## Further Reading

**Core Documentation**:
- [Capability Charter](capability-charter.md) - Detailed problem statement and solution design
- [Protocol Specification](protocol-spec.md) - Technical schemas, validation rules, integration specs
- [Awareness Guide](awareness-guide.md) - Agent execution patterns for using traceability
- [Adoption Blueprint](adoption-blueprint.md) - Step-by-step L0→L4 progression with time estimates
- [Ledger](ledger.md) - Adopter tracking, version history, enhancement requests

**Schemas & Validation**:
- schemas/feature-manifest.yaml - JSON Schema for feature-manifest.yaml
- schemas/traceability-frontmatter.yaml - Frontmatter validation schema
- scripts/validate-traceability.py - Comprehensive validation script (10 rules)

**Automation**:
- scripts/generate-feature-manifest.py - Auto-generate manifest from git log + beads
- scripts/traceability-dashboard.py - HTML dashboard generator
- templates/feature-manifest.j2 - Jinja2 template for new features

---

**Questions or Feedback?**

- **Beads Task**: .beads-i6mf (SAP-056 creation tracking)
- **Coordination Requests**: File in inbox/coordination/ with [SAP-056] prefix
- **Enhancement Requests**: Add to [ledger.md](ledger.md) Section 3

---

**Created**: 2025-11-16
**Last Updated**: 2025-11-16
**Version**: 1.0.0
**Status**: Draft
**Primary Maintainer**: (To be assigned)
