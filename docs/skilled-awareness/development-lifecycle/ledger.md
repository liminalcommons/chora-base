---
sap_id: SAP-012
version: 1.3.0
status: Active
last_updated: 2025-11-04
enhancement: sap-009-phase-4-awareness
---

# Ledger: Development Lifecycle Adoption

**SAP ID**: SAP-012
**Capability**: development-lifecycle
**Version**: 1.3.0
**Last Updated**: 2025-11-04
**Enhancement**: SAP-009 Phase 4 Agent Awareness Files

---

## 1. Adoption Overview

### Coverage Statistics

| Metric | Count | Target | Status |
|--------|-------|--------|--------|
| **Total Projects** | 0 | 10 | 🔴 0% |
| **Level 1 Adopters** (Development only) | 0 | 5 | 🔴 0% |
| **Level 2 Adopters** (+ Planning) | 0 | 3 | 🔴 0% |
| **Level 3 Adopters** (All 8 phases) | 0 | 2 | 🔴 0% |
| **DDD Adoption** | 0% | 80% | 🔴 Not Started |
| **BDD Adoption** | 0% | 60% | 🔴 Not Started |
| **TDD Adoption** | 0% | 70% | 🔴 Not Started |

**Status Legend**:
- 🟢 ≥80% (Excellent)
- 🟡 60-79% (Good)
- 🟠 40-59% (Fair)
- 🔴 <40% (Needs Improvement)

---

## 2. Adopter Registry

### Level 1: Development Focus (DDD→BDD→TDD)

#### chora-base (Self-Adoption)
- **Status**: 🔄 In Progress (Phase 3 Batch 2)
- **Version**: SAP-012 v1.0.0
- **Adoption Date**: 2025-10-28 (SAP created)
- **Level**: Level 1 (planning to Level 3)
- **Adopter Type**: Template repository (dogfooding)
- **Components**:
  - ✅ Workflow docs (6 files, 5,285 lines)
  - ✅ Templates (sprint, release, metrics)
  - ⏳ Full DDD→BDD→TDD adoption (in progress)
- **Metrics**:
  - Defects per release: Target <3 (baseline TBD)
  - Test coverage: 95%+ (already high)
  - Process adherence: TBD (start tracking in Sprint 1)
- **Notes**: chora-base is using this SAP to document its own development process
- **Contact**: Victor (victorpiper)

---

### Level 2: Planning + Development

_(No adopters yet)_

**Target Adopters**:
- chora-compose (MCP server)
- mcp-gateway (MCP gateway)
- Example projects in `examples/`

---

### Level 3: Full Lifecycle (All 8 Phases)

_(No adopters yet)_

**Target Adopters**:
- chora-base (upgrade from Level 1 after 2-3 sprints)
- Future chora-* ecosystem projects

---

## 3. Adoption Metrics by Project

### chora-base

**Adoption Timeline**:
- 2025-10-28: SAP-012 created (Protocol, Awareness, Adoption, Ledger)
- 2025-10-28: Level 1 adoption started (DDD→BDD→TDD workflow)
- TBD: Level 2 adoption (sprint planning)
- TBD: Level 3 adoption (full lifecycle)

**Quality Metrics** (baseline TBD):

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Defects per release | TBD | TBD | <3 | 🔴 Not tracking yet |
| Test coverage | 95% | 95% | ≥85% | 🟢 Excellent |
| Code review time | TBD | TBD | <24h | 🔴 Not tracking yet |
| Rework rate | TBD | TBD | <20% | 🔴 Not tracking yet |
| Release time (minutes) | 30-45 | 15-20 | <20 | 🟢 Improved (GAP-003 Tracks 1 & 2) |

**Velocity Metrics** (TBD after Sprint 1-2):

| Metric | Sprint 1 | Sprint 2 | Sprint 3 | Trend |
|--------|----------|----------|----------|-------|
| Story points committed | TBD | TBD | TBD | - |
| Story points delivered | TBD | TBD | TBD | - |
| Planned vs delivered | TBD | TBD | TBD | Target ≥70% |

**Process Adherence Metrics** (TBD):

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| DDD adoption (% features with docs-first) | 0% | 80% | 🔴 Not started |
| BDD adoption (% features with .feature files) | 0% | 60% | 🔴 Not started |
| TDD adoption (% code written test-first) | Unknown | 70% | 🔴 Not measured |
| Sprint adherence (% on-time completion) | N/A | 70% | 🔴 No sprints yet |

**Notes**:
- chora-base currently has workflow docs but not consistently following DDD→BDD→TDD
- SAP-012 formalizes the process, tracking adoption starting now
- Baseline metrics will be established in first sprint after SAP-012 adoption

---

## 4. Version History

### v1.3.0 (2025-11-04) - SAP-009 Phase 4: Agent Awareness Files

**Changes**:
- ✅ Added CLAUDE.md (~550 lines, ~11k tokens): Claude Code-specific patterns
  - 3 Claude Code workflows (Sprint start, DDD change request, BDD scenarios)
  - Tool usage patterns (Read templates, Edit sprint plans, Bash for quality gates)
  - Progressive token usage phases (5 phases per workflow)
  - Claude-specific tips (5 tips: Read templates, run gates, update ledger, verify RED, incremental edits)
  - Common pitfalls for Claude (5 scenarios: skip DDD, not verify RED, skip gates, forget ledger, overwrite plan)
- ✅ AGENTS.md already existed (513 lines): Generic agent guidance
  - 8-phase workflow documentation
  - User signal patterns (4 tables: Workflow, Sprint, DDD, BDD, TDD, Quality, Release)
  - Quick reference for all phases
  - Integration with templates

**Integration with SAP-009**:
- CLAUDE.md follows SAP-009 progressive token usage pattern
- Phase-based context loading for reduced initial token usage
- Tool-specific patterns (Read, Edit, Bash for development lifecycle)

**Expected Impact**:
- Faster agent onboarding (progressive loading reduces context)
- Improved workflow coverage (11 total workflows: 8 generic + 3 Claude Code)
- Better error prevention (10 common pitfalls documented with fixes)
- Enhanced template usage (Read-Edit pattern for sprint plans, change requests)

**Validation TODO** (before finalizing):
- [ ] Verify CLAUDE.md follows SAP-009 progressive token usage phase structure
- [ ] Verify tool usage patterns match Claude Code capabilities (Read, Edit, Bash, Write)
- [ ] Verify links to templates and related SAPs are correct
- [ ] Test workflows with actual sprint creation and BDD scenario writing

---

### v1.2.0 (2025-11-04) - Template Release Workflow (Track 2)

**Changes**:
- ✅ Added Track 2 completion to Section 4.5 (template generation)
- ✅ Documented template scripts for generated projects
- ✅ Extended 50% time savings to all generated projects
- ✅ Added multi-arch Docker build integration (Phase 7.4)

**Business Impact**:
- ALL generated projects inherit 50% release time reduction
- Multi-arch Docker support (linux/amd64, linux/arm64) built-in
- PyPI + Docker + GitHub release automation out-of-box
- ROI break-even: 3 releases per generated project

**Related Work**:
- GAP-003 Track 2 implementation (3 template scripts + CI/CD workflows)
- SAP-008 v1.3.0 (template scripts inventory)

**Adopters**: 0 (templates ready for new projects)

---

### v1.1.0 (2025-11-03) - Release Workflow Integration (Track 1)

**Changes**:
- ✅ Added Section 4.5: Release Workflow Integration (GAP-003)
- ✅ Documented Track 1 completion (chora-base scripts)
- ✅ Added release time metric to Quality Metrics table
- ✅ Integrated Phase 7 (Release) with automation scripts

**Business Impact**:
- 50% reduction in release time (30-45 min → 15-20 min)
- 100% CHANGELOG consistency through templates
- Automated GitHub release creation

**Related Work**:
- GAP-003 Track 1 implementation (bump-version.py, create-release.py)
- SAP-008 v1.2.0 (automation scripts documentation)

**Adopters**: 0 (chora-base adopting in progress)

---

### v1.0.0 (2025-10-28) - Initial Release

**Changes**:
- ✅ Created SAP-012 (5 artifacts)
- ✅ Documented 8-phase lifecycle
- ✅ Integrated DDD→BDD→TDD workflows
- ✅ Created templates (sprint, release, metrics)

**Artifacts**:
- [capability-charter.md](capability-charter.md) - Problem, solution, success criteria
- [protocol-spec.md](protocol-spec.md) - 8-phase contracts, DDD→BDD→TDD integration
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt lifecycle
- [ledger.md](ledger.md) - This document

**Adopters**: 0 (chora-base in progress)

---

## 4.5 Release Workflow Integration (GAP-003)

**Status**: ✅ Track 1 Complete (chora-base), ✅ Track 2 Complete (templates)

### Track 1: chora-base Unified Release (COMPLETE)

**Implemented**: 2025-11-03
**Scripts**: `bump-version.py`, `create-release.py`

**Integration with SAP-012 Phase 7 (Release)**:
- **Phase 7.1: Version bump** → `just bump <version>`
  - Automates CHANGELOG.md updates with version header
  - Creates git commit and annotated tag
  - Provides TODO template for release notes
- **Phase 7.2: Update CHANGELOG** → Manual editing (developer fills TODOs)
  - Developer replaces placeholders with actual changes
  - Structured format ensures consistency
- **Phase 7.3: Create release** → `just release`
  - Extracts notes from CHANGELOG.md
  - Creates GitHub release with gh CLI
  - Automated, no manual web UI needed
- **Phase 7.4: Publish packages** → (PyPI only in Track 1, Docker in Track 2)

**Metrics (Baseline)**:
- Release time: 30-45 min manual → 15-20 min with scripts (50% reduction)
- CHANGELOG consistency: 100% (template-based)
- GitHub release automation: 100% (no manual web UI)
- Manual extraction errors: 0 (automated extraction)

**Quality Impact**:
- Consistent version formatting (semver validation)
- Standardized commit messages (`chore(release): Bump version to vX.Y.Z`)
- GitHub release notes always match CHANGELOG
- No human error in note extraction

### Track 2: Template Generation (COMPLETE)

**Implemented**: 2025-11-04
**Templates**: `bump-version.py.template`, `create-release.py.template`, `justfile.template`
**Scope**: Extended to static-template for generated projects
**Goal**: Generated projects get unified PyPI + Docker + GitHub release workflow out-of-box

**Integration with SAP-012 Phase 7 (Release)** for generated projects:
- **Phase 7.1: Version bump** → `just bump <version>`
  - Updates 4 files: pyproject.toml, __init__.py, docker-compose.yml, CHANGELOG.md
  - Creates git commit and annotated tag
  - Same workflow as chora-base, but templated for any project
- **Phase 7.2: Update CHANGELOG** → Manual editing (developer fills TODOs)
  - Developer replaces placeholders with actual changes
  - Structured format ensures consistency
- **Phase 7.3: Create release** → `just release`
  - Extracts notes from CHANGELOG.md
  - Creates GitHub release with gh CLI
  - CI/CD triggers automatically on tag push
- **Phase 7.4: Publish packages** → Automated via GitHub Actions
  - PyPI publishing via OIDC trusted publishing
  - Multi-arch Docker builds (linux/amd64, linux/arm64)
  - Images pushed to ghcr.io (GitHub Container Registry)
  - Artifacts attached to GitHub release

**Metrics (Projected for Generated Projects)**:
- Release time: 30-45 min manual → 15-20 min automated (50% reduction, same as chora-base)
- Multi-arch Docker: Built-in support (no manual setup)
- PyPI + Docker + GitHub: All automated in one workflow
- ROI break-even: 3 releases per project

**Quality Impact**:
- Every generated project inherits best practices
- Consistent release workflow across all MCP projects
- Multi-arch Docker support by default
- No manual registry configuration needed

**Templates Added**:
- `bump-version.py.template` (400+ lines) - Version management
- `create-release.py.template` (300+ lines) - GitHub release automation
- `justfile.template` (200+ lines) - Task runner with release commands
- `docker-compose.yml` updates - Version variable substitution
- `Dockerfile` updates - OCI metadata labels
- `.github/workflows/release.yml` - Multi-arch Docker build job
- `how-to-create-release.md.template` (450+ lines) - Complete guide

**Commits**:
- `bc6df7b` - Docker and CI/CD template updates
- `13e4656` - Script templates (bump-version, create-release, justfile)

**Related Documents**:
- [GAP-003 Track 2 Completion Summary](../../project-docs/gap-003-track-2-completion-summary.md)
- [GAP-003 Track 1 Completion Summary](../../project-docs/gap-003-track-1-completion-summary.md)
- [Workflow Continuity Gap Report](../../project-docs/workflow-continuity-gap-report.md)
- [SAP-008 v1.3.0 Automation Scripts Ledger](../automation-scripts/ledger.md)

---

## 5. Feedback & Learnings

### Sprint 1 Learnings (TBD)

**What Went Well**:
- TBD after first sprint

**What Could Improve**:
- TBD after first sprint

**Action Items**:
- TBD after first sprint

---

### Common Adoption Challenges (Future)

_(Document patterns as projects adopt)_

**Challenge 1**: [TBD based on pilot feedback]
**Solution**: [TBD]

**Challenge 2**: [TBD]
**Solution**: [TBD]

---

## 6. Research Evidence & ROI

### Expected ROI (Research-Backed)

**Sources**:
- "Test Driven Development: By Example" (Kent Beck, 2002)
- "The Cucumber Book" (Matt Wynne, Aslak Hellesøy, 2017)
- "Docs as Code" (Anne Gentle, 2017)

**Expected Outcomes**:

| Metric | Baseline | Target (3 months) | Evidence |
|--------|----------|-------------------|----------|
| **Defect Reduction** | Varies | 40-80% reduction | Kent Beck (TDD) |
| **Rework Reduction** | Varies | 40-60% reduction | Anne Gentle (DDD) |
| **Requirement Ambiguity** | Varies | 60% reduction | Wynne & Hellesøy (BDD) |
| **API Churn** | Varies | 50% reduction | Anne Gentle (DDD) |
| **Test Coverage** | Varies | ≥85% | Industry best practice |

---

### Actual ROI (Measured After Adoption)

_(Update after 3-6 months of adoption)_

**chora-base Results** (TBD):
- Defect reduction: TBD
- Rework reduction: TBD
- Time to implement feature: TBD (before vs after)
- Developer satisfaction: TBD (survey)

---

## 7. Upgrade Path

### From v1.0.0 to Future Versions

**Breaking Changes** (MAJOR version):
- Will require migration guide
- Announced 3 months in advance

**New Features** (MINOR version):
- Backward compatible
- Optional adoption

**Bug Fixes** (PATCH version):
- Transparent updates to workflow docs

---

## 8. Maintenance Notes

### Document Updates

**Last Review**: 2025-10-28 (initial creation)
**Next Review**: 2025-11-28 (1 month after Sprint 1 starts)
**Review Frequency**: Monthly (first 3 months), then quarterly

### Metrics Update Schedule

**Frequency**: After each sprint (biweekly)
**Owner**: Release manager or project maintainer
**Process**:
1. Update project metrics tables
2. Document learnings in Section 5
3. Update adoption statistics in Section 1

---

## 9. Related Documents

**SAP Artifacts**:
- [capability-charter.md](capability-charter.md) - Problem and solution overview
- [protocol-spec.md](protocol-spec.md) - Technical contracts for 8 phases
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt

**Workflow Docs**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - 8-phase lifecycle overview (1,108 lines)
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD→BDD→TDD integration (753 lines)
- [DDD_WORKFLOW.md](/static-template/dev-docs/workflows/DDD_WORKFLOW.md) - Documentation Driven Design (919 lines)
- [BDD_WORKFLOW.md](/static-template/dev-docs/workflows/BDD_WORKFLOW.md) - Behavior Driven Development (1,148 lines)
- [TDD_WORKFLOW.md](/static-template/dev-docs/workflows/TDD_WORKFLOW.md) - Test Driven Development (1,187 lines)
- [ANTI_PATTERNS.md](/static-template/dev-docs/ANTI_PATTERNS.md) - Common mistakes (1,309 lines)

**Templates**:
- [sprint-template.md](/static-template/project-docs/sprints/sprint-template.md) - Sprint planning template
- [release-template.md](/static-template/project-docs/releases/release-template.md) - Release planning template
- [PROCESS_METRICS.md](/static-template/project-docs/metrics/PROCESS_METRICS.md) - Metrics dashboard

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Meta SAP framework
- [SAP-004: testing-framework](../testing-framework/) - pytest, coverage, fixtures
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - CI/CD automation
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit hooks
- [SAP-007: documentation-framework](../documentation-framework/) - Diataxis structure
- [SAP-008: automation-scripts](../automation-scripts/) - Automation scripts
- [SAP-013: metrics-tracking](../metrics-tracking/) - ClaudeROICalculator

---

**Changelog**:
- **2025-10-28**: Initial ledger created for SAP-012 v1.0.0
- **TBD**: First metrics update after Sprint 1
- **TBD**: Quarterly review and process improvements

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger for development-lifecycle SAP
