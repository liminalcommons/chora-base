# Capability Charter: SAP Ecosystem Integration

**SAP ID**: SAP-061
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-11-20
**Author**: chora-base maintainers + Claude (AI peer)

---

## Document Purpose

This charter defines SAP-061 (SAP Ecosystem Integration) - a systematic approach to validating and maintaining SAP integration across the chora-base ecosystem. It establishes automated validation for 5 integration points (INDEX.md, sap-catalog.json, copier.yml, adoption paths, dependencies) to prevent gaps like the SAP-053 INDEX.md omission discovered during Phase 4 completion.

**Audience**: Developers, AI agents, SAP maintainers, ecosystem architects

**Related Documents**:
- [protocol-spec.md](protocol-spec.md) - Validation algorithms, integration point schemas, automation patterns
- [awareness-guide.md](awareness-guide.md) - Agent workflows for ecosystem integration, pre-commit hooks
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan (Design → Infrastructure → Pilot → Distribution)

---

## Problem Statement

### Current State: Manual Ecosystem Integration

**What's broken**:

1. **Integration gaps discovered too late** - SAP-053 was 100% complete (all 5 artifacts, L3 validated) but missing from INDEX.md until Phase 4 completion
2. **No systematic integration checklist** - Developers rely on memory to update INDEX.md, catalog, Copier, etc.
3. **No automated validation** - Integration gaps only discovered through manual review or user feedback
4. **No enforcement mechanism** - Nothing prevents committing incomplete integrations
5. **No visibility into integration status** - Cannot quickly answer "which SAPs are missing from INDEX.md?"

**Quantitative pain**:

| Metric | Current State | Pain Point |
|--------|---------------|------------|
| **Integration checklist** | Manual (5 steps) | Easy to forget steps, especially INDEX.md |
| **Discovery time for gaps** | Days to weeks (post-release) | Users discover gaps, maintainers scramble |
| **Integration validation** | 0% automated | All manual, error-prone |
| **Avg time to detect gap** | 3-7 days (retrospective review) | SAP-053 gap found during Phase 4 review |
| **Avg time to fix gap** | 15-30 min | But only after detection! |

**Cascading Impact**:

When a SAP is missing from integration points:
- **INDEX.md omission** → Users can't discover SAP, adoption blocked
- **sap-catalog.json omission** → Tooling can't find SAP metadata, automation fails
- **copier.yml omission** → SAP not distributable via Copier, ecosystem fragmentation
- **Adoption path omission** → New users miss recommended SAP, suboptimal onboarding
- **Broken dependencies** → Dependent SAPs reference non-existent SAPs, validation fails

**Real-World Example** (Trigger for SAP-061):

> During SAP-053 Phase 4 completion (2025-11-19), discovered SAP-053 was missing from INDEX.md despite being 100% complete. Root cause: Ecosystem integration treated as "post-completion quality gate" vs "pre-release deliverable". User question: **"How do we ensure that the full, end-to-end scope is always already known when we do SAP development?"**

**Annual cost** (estimated, 5 SAPs/year):
- Gap discovery time: 5 gaps × 5 days avg = 25 days wasted
- Emergency fixes: 5 fixes × 2 hours = 10 hours
- User confusion: 10-15 hours support time for "where is SAP-XXX?" questions
- **Total**: **~35-40 hours/year** wasted on preventable integration gaps

### Why Now?

**Immediate trigger**: SAP-053 Phase 4 INDEX.md gap discovery raised the question: "How do we prevent this systematically?"

**Strategic dependencies met**:
- ✅ INDEX.md centralized registry exists (updated 2025-11-11 with domain taxonomy)
- ✅ sap-catalog.json machine-readable catalog exists (updated 2025-10-28)
- ✅ Copier distribution system exists (OPP-2025-022, CORD-2025-022)
- ✅ Progressive Adoption Paths documented (SAP-DISCO-V5)
- ✅ Pre-commit hook infrastructure exists (.pre-commit-config.yaml)

**Ecosystem maturity**: With 48 SAPs (26 active, 13 pilot, 8 draft), the ecosystem is mature enough that integration gaps have **high visibility impact**. Automation is critical to maintain quality at scale.

**Multi-SAP suite context**: SAP-061 is part of the SAP Development Lifecycle Meta-SAP Suite (CORD-2025-023), which formalizes SAP development practices. Ecosystem integration is foundational to this suite.

---

## Solution Overview

### Core Capability: Automated Ecosystem Integration Validation

Define **SAP-061 (SAP Ecosystem Integration)** as a skilled awareness pattern providing:

1. **5 Integration Point Validation**
   - **INDEX.md**: SAP entry exists in appropriate domain section with description, features, dependencies
   - **sap-catalog.json**: SAP metadata in machine-readable format for tooling/automation
   - **copier.yml**: SAP available for Copier-based distribution (if status=active or pilot)
   - **Progressive Adoption Path**: SAP mentioned in relevant adoption path (if status=active)
   - **Dependencies**: All referenced SAPs exist and are valid (no broken references)

2. **Automated Validation Script** (`scripts/validate-ecosystem-integration.py`)
   - Validate single SAP or all SAPs (`--all`)
   - JSON output for CI/CD integration (`--json`)
   - Verbose mode for debugging (`-v/--verbose`)
   - Exit codes: 0=pass, 1=INDEX, 2=catalog, 3=copier, 4=deps, 5=multiple, 6=usage
   - Performance target: <2s for full ecosystem validation (all 48 SAPs)

3. **Pre-commit Hook** (blocks commits with integration gaps)
   - Triggers on: SAP artifact modifications (`docs/skilled-awareness/**/*.md`, `INDEX.md`, `sap-catalog.json`, `copier.yml`)
   - Runs: `python scripts/validate-ecosystem-integration.py --all`
   - Blocks commit if: Any SAP fails integration validation
   - Bypass: `git commit --no-verify` (discouraged, for emergency fixes only)

4. **Status-Based Requirements** (smart validation)
   - **Draft SAPs**: Only INDEX.md + dependencies required (minimal integration)
   - **Pilot SAPs**: INDEX.md + catalog + copier + dependencies required
   - **Active SAPs**: All 5 integration points required (full integration)
   - **Deprecated SAPs**: INDEX.md entry updated with deprecation notice, catalog marked deprecated

5. **Integration Gap Reporting**
   - Human-readable output: Clear pass/fail per integration point with remediation guidance
   - JSON output: Machine-readable for dashboards, CI/CD, metrics tracking
   - Exit codes: Specific codes for each integration point failure (enables targeted fixes)

### Value Proposition

**For SAP Developers**:
- ✅ **Automated checklist**: Never forget an integration step
- ✅ **Fast feedback**: Know about gaps in <2s (pre-commit hook)
- ✅ **Clear remediation**: Validation output explains exactly what's missing and where
- ✅ **No manual review burden**: Automation handles 100% of integration validation

**For SAP Maintainers**:
- ✅ **Comprehensive visibility**: `--all` mode shows all integration gaps at once
- ✅ **Quality gates**: Pre-commit hook prevents incomplete integrations from entering main branch
- ✅ **Ecosystem health**: JSON output enables dashboards tracking integration status
- ✅ **Reduced support burden**: Fewer "where is SAP-XXX?" questions from users

**For End Users**:
- ✅ **Complete discoverability**: All SAPs guaranteed to be in INDEX.md
- ✅ **Reliable tooling**: Catalog always up-to-date for automation
- ✅ **Smooth onboarding**: Adoption paths always include active SAPs
- ✅ **No broken dependencies**: All SAP references validated

---

## Success Criteria

### Phase 1: Design (L0 → L1)

**Goal**: Define SAP-061 scope, validation rules, automation requirements

**Deliverables**:
- ✅ Capability charter (this document) - Problem statement, solution, value prop
- ✅ Protocol specification - 5 integration point schemas, validation algorithms
- ✅ Awareness guide - Agent workflows for integration validation
- ✅ Adoption blueprint - 4-phase adoption plan with effort estimates

**Success Metric**: All 4 core artifacts complete, SAP-061 scope approved

---

### Phase 2: Infrastructure (L1 → L2)

**Goal**: Implement validation script and pre-commit hook

**Deliverables**:
- ✅ `scripts/validate-ecosystem-integration.py` (573 lines, 5 integration points)
- ✅ Pre-commit hook (`validate-sap-ecosystem-integration`)
- ✅ Test suite (15 tests covering all integration points)
- ✅ Documentation (README.md, usage examples)

**Success Metrics**:
- Validation script passes all tests (100% pass rate)
- Performance: <2s for full ecosystem validation (48 SAPs)
- Exit codes: Correct code for each failure scenario (1-6)
- Pre-commit hook: Blocks commits with integration gaps

**Note**: Phase 2 delivered early during CORD-2025-023 Phase 1 (2025-11-20). Script functional, tested with SAP-053.

---

### Phase 3: Pilot (L2 → L3)

**Goal**: Validate SAP-061 patterns in chora-workspace, measure ROI

**Deliverables**:
- Pilot period: 2-3 weeks (or 3-5 new SAPs created with SAP-061 validation)
- Metrics collection: Integration gaps caught, false positives, performance
- Knowledge notes: Patterns and edge cases discovered
- Pilot report: ROI analysis, GO/NO-GO recommendation

**Success Metrics**:
- **Integration gap detection**: ≥95% of gaps caught by validation (target: 100%)
- **False positives**: ≤5% (validation incorrectly flags valid integrations)
- **Performance**: <2s for full ecosystem validation (confirmed)
- **Developer satisfaction**: ≥80% positive feedback ("validation is helpful")
- **Adoption friction**: ≤10 min to understand and use validation script

**Validation Period**: Next 3-5 SAPs created (SAP-061, SAP-062, SAP-050 promoted, SAP-000 revised, future SAPs)

---

### Phase 4: Distribution (L3 → L4)

**Goal**: Integrate SAP-061 into chora-base template, enable ecosystem adoption

**Deliverables**:
- SAP-061 artifacts in chora-base (`docs/skilled-awareness/sap-ecosystem-integration/`)
- Validation script in chora-base (`scripts/validate-ecosystem-integration.py`)
- Pre-commit hook enabled in chora-base (`.pre-commit-config.yaml`)
- Documentation updates (INDEX.md, README.md, how-to guides)
- Copier template integration (if applicable)

**Success Metrics**:
- **Zero integration gaps**: All 48 SAPs pass validation (100% ecosystem health)
- **Pre-commit hook adoption**: Enabled in chora-base main branch
- **Distribution**: SAP-061 available via Copier for new projects
- **Documentation**: SAP-061 in INDEX.md, catalog, adoption paths
- **Ecosystem adoption**: ≥2 additional projects adopt SAP-061 (beyond chora-workspace)

---

## Scope & Boundaries

### In Scope (SAP-061)

✅ **5 Integration Point Validation**:
1. INDEX.md entry validation (SAP listed in appropriate domain)
2. sap-catalog.json metadata validation (machine-readable SAP entry)
3. copier.yml distribution validation (if status=active/pilot)
4. Progressive Adoption Path mention validation (if status=active)
5. Dependency validation (all referenced SAPs exist)

✅ **Automation**:
- Python validation script (`validate-ecosystem-integration.py`)
- Pre-commit hook (`validate-sap-ecosystem-integration`)
- JSON output for CI/CD integration
- Verbose mode for debugging

✅ **Status-Based Rules**:
- Draft: Minimal integration (INDEX + deps)
- Pilot: Standard integration (INDEX + catalog + copier + deps)
- Active: Full integration (all 5 points)
- Deprecated: INDEX updated with deprecation notice

### Out of Scope (Deferred or Other SAPs)

❌ **Content Quality Validation** (SAP-050: SAP Adoption Verification):
- Frontmatter schema validation (SAP ID, version, status)
- 5-artifact completeness (charter, protocol, awareness, blueprint, ledger)
- Link validation (broken cross-references)
- Section completeness (required sections in each artifact)

❌ **SAP Lifecycle Management** (SAP-062: SAP Distribution & Versioning):
- Versioning strategy (semver, L0-L4 status progression)
- Distribution via Copier (template creation, update strategy)
- Deprecation workflow (sunset timeline, migration guidance)

❌ **SAP Development Phases** (SAP-050: SAP Development Lifecycle, promoted):
- Phase gates (Design → Infrastructure → Pilot → Distribution)
- Maturity levels (L0 → L1 → L2 → L3 → L4 progression)
- Effort estimation (time to complete each phase)

❌ **Namespace Validation** (Existing: `scripts/validate-namespaces.py`):
- Capability namespace format validation (`chora.domain.capability`)
- Namespace uniqueness across ecosystem
- Domain validity (Infrastructure, Developer Experience, Foundation, etc.)

---

## Dependencies

**Upstream (Must Exist Before SAP-061)**:
- ✅ SAP-000 (SAP Framework v1.0.0) - Defines SAP structure, 5 core artifacts
- ✅ INDEX.md (Domain-Based Taxonomy v1.0.0) - Centralized SAP registry
- ✅ sap-catalog.json - Machine-readable SAP metadata
- ✅ copier.yml (Copier Template v1.0.0) - SAP distribution system
- ✅ Progressive Adoption Paths (SAP-DISCO-V5) - Adoption path documentation

**Downstream (Benefit from SAP-061)**:
- ➡️ SAP-062 (SAP Distribution & Versioning) - Uses SAP-061 validation in distribution workflow
- ➡️ SAP-050 (SAP Development Lifecycle, promoted) - Integrates SAP-061 as Phase 4 quality gate
- ➡️ SAP-000 (SAP Framework v1.1.0) - Elevates ecosystem integration to required deliverable
- ➡️ All future SAPs - Benefit from automated integration validation

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **False positives** (validation flags valid integrations) | Medium | Medium | Comprehensive test suite (15 tests), pilot validation, user feedback loop |
| **Performance degradation** (<2s target not met) | Low | Low | Optimized Python script, minimal I/O (read 3 files: INDEX, catalog, copier), parallel validation |
| **Pre-commit hook too strict** (blocks legitimate commits) | Medium | High | Bypass option (`--no-verify`), clear error messages, status-based rules reduce false positives |
| **Integration point schema changes** (INDEX format changes) | Low | Medium | Version all schemas, backward compatibility layer, migration guide |
| **Adoption friction** (developers find validation annoying) | Medium | Medium | Fast feedback (<2s), clear remediation guidance, opt-out for emergencies |
| **Maintenance burden** (validation script breaks often) | Low | Medium | Comprehensive test suite, CI/CD integration, quarterly review cycle |

**Overall Risk**: **Medium-Low** - Well-defined problem, proven solution (Phase 1 implementation successful), clear value prop

---

## Timeline & Effort

| Phase | Estimated Effort | Target Completion | Status |
|-------|-----------------|-------------------|--------|
| **Phase 1 (Design)** | 2-3 hours | 2025-11-20 | ✅ In Progress (CORD-2025-023 Phase 2) |
| **Phase 2 (Infrastructure)** | 3-4 hours | 2025-11-20 | ✅ Complete (delivered early in CORD-2025-023 Phase 1) |
| **Phase 3 (Pilot)** | 2-3 weeks | 2025-12-15 | ⏳ Planned (next 3-5 SAPs) |
| **Phase 4 (Distribution)** | 1-2 hours | 2025-12-22 | ⏳ Planned (integrate with template) |

**Total Effort**: ~8-10 hours (reduced from 10-12 hours due to early Phase 2 completion)

**Parallel Work**: Phase 3 pilot runs concurrently with other SAP development (SAP-062, SAP-050, SAP-000)

---

## Alternatives Considered

### Alternative 1: Manual Checklist (Status Quo)

**Approach**: Maintain manual checklist for SAP developers to follow

**Pros**:
- Zero implementation effort
- Flexible (easy to change checklist)

**Cons**:
- ❌ Error-prone (human memory unreliable)
- ❌ No enforcement (checklist can be ignored)
- ❌ Slow feedback (gaps discovered days/weeks later)
- ❌ Support burden (users ask "where is SAP-XXX?")

**Decision**: **Rejected** - Manual checklist failed for SAP-053, would fail again

---

### Alternative 2: CI/CD Only Validation (No Pre-commit Hook)

**Approach**: Run validation in CI/CD pipeline only, not on local commits

**Pros**:
- Less intrusive (no pre-commit delay)
- Centralized enforcement

**Cons**:
- ❌ Slow feedback (wait for CI/CD pipeline to run)
- ❌ Blocks PR merge, not local commit (rework required)
- ❌ Higher friction (must fix, force push, wait for CI/CD again)

**Decision**: **Rejected** - Pre-commit hook provides faster feedback (2s vs 2-5 min CI/CD)

---

### Alternative 3: Lint-Style Warnings (Non-Blocking)

**Approach**: Show validation warnings but don't block commits

**Pros**:
- Low friction (never blocks developers)
- Easy adoption

**Cons**:
- ❌ Warnings ignored (developers habituated to ignore warnings)
- ❌ No enforcement (gaps still slip through)
- ❌ Same problem as manual checklist

**Decision**: **Rejected** - Non-blocking validation doesn't prevent gaps

---

### Alternative 4: AI Agent Integration Validation (GPT-4, Claude)

**Approach**: Use LLM to validate integration during SAP generation

**Pros**:
- Intelligent validation (LLM can understand context)
- Flexible (adapts to schema changes)

**Cons**:
- ❌ High latency (2-5s LLM call per validation)
- ❌ Cost ($0.01-0.10 per validation)
- ❌ Reliability concerns (LLM hallucinations, rate limits)
- ❌ Complexity (API keys, error handling, retries)

**Decision**: **Rejected** - Deterministic Python script is faster, cheaper, more reliable

---

## Success Stories (Future)

**Upon L4 Distributed Status**:

> "Since adopting SAP-061, we've created 12 new SAPs without a single integration gap. The pre-commit hook catches mistakes immediately, and the validation script gives clear guidance on what's missing. Setup took 10 minutes, and it's saved us ~2-3 hours per SAP in manual checks and rework." - chora-base maintainer

> "As a new contributor, SAP-061 made it easy to create my first SAP. I didn't have to remember the integration checklist - the validation script told me exactly what to do. When I forgot to add my SAP to INDEX.md, the pre-commit hook caught it immediately." - First-time SAP contributor

---

## Related Documents

- **Protocol Specification**: [protocol-spec.md](protocol-spec.md) - Validation algorithms, schemas, exit codes
- **Awareness Guide**: [awareness-guide.md](awareness-guide.md) - Agent workflows, pre-commit patterns
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan
- **Ledger Template**: [ledger.md](ledger.md) - Adoption tracking for projects using SAP-061

**External References**:
- SAP-000 (SAP Framework v1.0.0): `docs/skilled-awareness/sap-framework/`
- SAP-050 (SAP Development Lifecycle): `docs/skilled-awareness/sap-adoption-verification/` (to be promoted)
- SAP-053 (Conflict Resolution): `docs/skilled-awareness/conflict-resolution/`
- CORD-2025-023 (SAP Development Lifecycle Meta-SAP Suite): `inbox/incoming/coordination/CORD-2025-023-sap-development-lifecycle-meta-saps.json`

---

**Document Status**: Draft (Phase 1 - Design in progress)
**Last Updated**: 2025-11-20
**Next Review**: Upon Phase 3 pilot completion (2025-12-15)
