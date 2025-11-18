---
sap_id: SAP-056
version: 1.0.0
status: Draft
last_updated: 2025-11-16
scope: Governance
type: reference
feature_id: FEAT-SAP-056
requirement_refs:
  - REQ-SAP-056-001
  - REQ-SAP-056-002
  - REQ-SAP-056-008
---

# Capability Charter: Lifecycle Traceability

**SAP ID**: SAP-056
**Capability Name**: lifecycle-traceability
**Version**: 1.0.0
**Status**: Draft (Phase 1)

---

## 1. Problem Statement

### Current State

Development artifacts exist in isolation across the chora ecosystem: visions don't link to features, features don't link to requirements, requirements don't link to code, code doesn't link to tests, tests don't link to docs, docs don't link to adoption records. Result: **accountability gap** where teams cannot answer fundamental questions:

- "Why does this code exist?" (What feature/requirement drove it?)
- "Is requirement X implemented?" (Which code files implement it?)
- "What tests validate feature Y?" (What's our test coverage?)
- "Which docs explain this capability?" (Where's the user guide?)
- "What would break if I change feature Z?" (What depends on this?)

**Current Traceability Coverage**: ~40%

**Strong** (Low Gap):
- Code→Tests (SAP-004: pytest conventions, 85% coverage)
- Tests→Docs (SAP-007: executable how-tos)
- Git→Tasks (SAP-015 L3-L4: commit message suggestions, pre-commit hooks)
- Tasks→Events (SAP-010 + SAP-015 L4: event emission on task lifecycle)
- Events→Knowledge (SAP-015 L4 Phase 4: auto-extraction from completed tasks)

**Weak** (High Gap):
- Vision→Features (no machine-readable linkage)
- Features→Requirements (no formal requirement artifact)
- Requirements→Code (no linkage mechanism)
- Code→Features (no feature manifest)
- Docs→Code (only in executable docs via SAP-007)

### User Pain Points

**From traceability research (2025-11-16)**:
> "How can we ensure traceability along our entire development lifecycle, including beads? Do our SAPs already mandate traceability?"

**Specific Issues**:
1. **Context restoration takes 15-30 minutes**: Developers manually search git logs, beads tasks, docs to understand "why this code exists"
2. **Impact analysis impossible**: Can't identify "what would break if I change feature X?" without manual code review (1-2 hours)
3. **Compliance audits manual**: Quarterly audits take 4+ hours to verify all requirements implemented with tests and docs
4. **Feature queries slow**: Finding "all code/tests/docs for feature Y" requires grep across multiple locations (10-20 minutes)
5. **Orphaned artifacts**: Code exists without linkage to requirements, tasks created without features, docs drift from code

### Impact

**Without this SAP**:
- ❌ High context restoration cost (15-30 min → productivity loss)
- ❌ Impossible to trace requirements to implementation (compliance risk)
- ❌ Impact analysis requires manual review (change risk)
- ❌ Knowledge isolated (why decisions made unclear months later)
- ❌ Artifacts can drift undetected (docs outdated, code orphaned)

**With this SAP**:
- ✅ Context restoration <1 minute (query feature manifest)
- ✅ Requirements traceable to code, tests, docs (compliance validated)
- ✅ Impact analysis automated (<5 min via dependency graph)
- ✅ Complete provenance for every artifact (audit trail)
- ✅ Automated detection of drift (validation scripts)

**Measured ROI** (from existing traceability research):
- Time saved per project: ~93 hours annually
- Break-even: 6-8 months for single project, immediate for 2+ projects

---

## 2. Stakeholders

### Primary Users

- **AI Agents** (Claude Code, Cursor Composer): Query traceability for context ("show all code for feature X"), validate completeness before commits
- **Developers**: Understand code provenance, perform impact analysis, restore context
- **Project Managers**: Track feature→requirement→implementation completeness
- **QA Engineers**: Verify requirement coverage via test traceability markers

### Secondary Users

- **Technical Writers**: Identify docs needing updates when code changes
- **Auditors**: Verify compliance (requirements → tests → code → docs linkage)
- **Maintainers**: Understand why code exists years later
- **Onboarding Engineers**: Learn codebase structure via traceability graph

### Decision Makers

- **Technical Leads**: Evaluating SAP-056 adoption for projects
- **Compliance Officers**: Assessing traceability completeness for audits
- **Architects**: Reviewing dependency graphs before major refactors

### Beneficiaries

- **Development Teams**: Faster context restoration, safer changes
- **Future Maintainers**: Complete provenance for legacy code
- **Stakeholders**: Visibility into feature implementation status

---

## 3. Proposed Solution

A **comprehensive umbrella SAP** that governs traceability across 10 artifact types (Vision, Features, Requirements, Documentation, Tests, Code, Git Commits, Tasks, Events, Knowledge) while delegating implementation to existing SAPs with enhancements.

**Creation Order**: When following SAP-012 (development-lifecycle), use Documentation-First pattern: `Requirements → Docs → Tests → Code`.

**Key Principles**:
1. **Governance, Not Implementation** - SAP-056 defines linkage schemas and validates compliance, but does NOT implement traceability (existing SAPs do)
2. **Machine-Readable Manifests** - feature-manifest.yaml provides single source of truth for feature artifacts
3. **Bidirectional Linkage** - If doc references code, code manifest MUST list doc (prevents drift)
4. **Evidence Requirement** - Every feature MUST have ≥1 test AND ≥1 doc (completeness enforced)
5. **Automated Validation** - Pre-commit hooks + CI/CD enforce traceability (not manual)

**Scope**: Governance level only
- Traceability linkage schemas and validation rules
- Compliance tracking per SAP
- Automation scripts for validation
- Feature manifest template

**Out of Scope**:
- Implementing traceability in specific SAPs (enhancement PRs to those SAPs)
- Real-time traceability dashboards (Phase 2)
- Cross-repo traceability (Phase 3)

### Design Trade-offs and Rationale

**Why umbrella SAP instead of comprehensive implementation SAP?**
- **Trade-off**: Single monolithic SAP vs. umbrella + individual enhancements
- **Decision**: Umbrella SAP ensures consistent governance without coupling all traceability concerns into one SAP
- **Alternative considered**: SAP-056 implements all traceability → rejected due to ownership ambiguity (who maintains a universal traceability SAP spanning testing, docs, memory, tasks?)

**Why feature-manifest.yaml instead of database?**
- **Trade-off**: Database (queryable, relational) vs. YAML file (git-friendly, readable)
- **Decision**: YAML provides git-versionable linkage, no database dependencies, and human-readable audit trail
- **Alternative considered**: SQLite database → rejected due to git merge conflicts and binary format limiting visibility

**Why frontmatter for doc linkage instead of comment headers?**
- **Trade-off**: YAML frontmatter (structured, validated) vs. comment headers (freeform)
- **Decision**: Frontmatter is machine-parseable, validated by JSON Schema, and already used in SAP-007
- **Alternative considered**: Comment headers → rejected due to parsing ambiguity and lack of validation

**Why pytest markers instead of docstring metadata?**
- **Trade-off**: pytest markers (runtime accessible) vs. docstring metadata (comment-based)
- **Decision**: Markers integrate with pytest runtime, enable filtered execution (`pytest --feature F6-1`), and are convention in Python ecosystem
- **Alternative considered**: Docstring metadata → rejected because pytest doesn't parse docstrings for filtering

**Why 10 validation rules instead of comprehensive coverage?**
- **Trade-off**: Comprehensive validation (50+ rules) vs. essential 10 rules
- **Decision**: 10 rules cover 95% of traceability gaps with minimal adoption friction
- **Alternative considered**: Comprehensive 50+ rules → rejected due to overwhelming validation output and high false positive rate

---

## 4. Capability Definition

### What This SAP Includes

**Traceability Governance**:

**1. Linkage Schema** (10 artifact types):
- Vision → Features (via feature-manifest.yaml vision_ref field)
- Features → Requirements (via feature-manifest.yaml requirements array)
- Requirements → Code (via feature-manifest.yaml code array)
- Code → Tests (via feature-manifest.yaml tests array)
- Tests → Requirements (via pytest markers @pytest.mark.requirement)
- Tests → Docs (via frontmatter test_references field)
- Docs → Code (via frontmatter code_references field)
- Git Commits → Tasks (via commit message [task-id] suffix)
- Tasks → Events (via A-MEM event emission with task_id)
- Events → Knowledge (via wikilinks [[task-id]] in notes)

**2. Validation Rules** (10 core rules):
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

**3. Compliance Levels** (L0-L3):
- **L0 (No Traceability)**: No linkages defined
- **L1 (Partial)**: Vision→Features + Code→Tests linked
- **L2 (Substantial)**: L1 + Features→Requirements + Docs→Code
- **L3 (Complete)**: L2 + Git→Tasks + Tasks→Events + Events→Knowledge (100% coverage)

**4. Automation Scripts**:
- `scripts/validate-traceability.py` - Comprehensive validation (10 rules), markdown report output
- `scripts/generate-feature-manifest.py` - Auto-generate manifest from git log + beads queries
- `scripts/traceability-dashboard.py` - HTML dashboard generator for metrics visualization

**5. Schemas**:
- `schemas/feature-manifest.yaml` - JSON Schema for feature-manifest.yaml
- `schemas/traceability-frontmatter.yaml` - Frontmatter validation schema for docs

**6. Templates**:
- `templates/feature-manifest.j2` - Jinja2 template for creating feature entries
- `templates/requirement-entry.j2` - Template for adding requirements to manifest

**Documentation**:
- `capability-charter.md` - This document
- `protocol-spec.md` - Traceability linkage schemas, validation rules, schemas
- `awareness-guide.md` (AGENTS.md) - Agent patterns for verification and queries
- `adoption-blueprint.md` - L0→L4 adoption steps with validation checkpoints
- `ledger.md` - Adopter tracking, version history
- `README.md` - 9-section overview with quality gates

### What This SAP Excludes

- **Implementing traceability** in specific SAPs (covered by enhancement PRs to SAP-010, SAP-012, SAP-015, SAP-007, SAP-004)
- **Real-time dashboards** (future enhancement, Phase 2)
- **Cross-repository traceability** (future enhancement, Phase 3)
- **Automated traceability restoration** after git operations (future enhancement, Phase 4)
- **AI-assisted impact analysis** (future enhancement, Phase 5)

---

## 5. Success Criteria

### Adoption Metrics

**Target**: 80% of chora-base adopters achieve L2+ traceability (substantial coverage)

**Measurement**:
- Presence of `feature-manifest.yaml` in project root
- Validation script pass rate ≥80%
- ≥5 features documented in manifest
- Frontmatter present in ≥50% of documentation files

### Quality Metrics

**Target**: 100% of features pass validation rules

**Measurement**:
- Validation script: 100% pass rate for Rule 1-10
- Zero orphaned artifacts (no code/tests/docs without feature linkage)
- feature-manifest.yaml passes JSON Schema validation
- All cross-references resolve (no broken links)

### Efficiency Metrics

**Target**: 95% reduction in traceability query time (15-30 min → <1 min)

**Measurement**:
- Baseline: Manual grep/git log queries (15-30 min)
- Post-adoption: feature-manifest.yaml query (<1 min)
- Impact analysis: Manual code review (60 min) → automated graph (<5 min)
- Context restoration: Manual search (15-20 min) → manifest query (<1 min)

**Target ROI**: 100+ hours saved annually per project

---

## 6. Dependencies

### Upstream Dependencies

- **SAP-000** (sap-framework): Provides SAP structure and governance
- **SAP-004** (testing-framework): Pytest conventions for test markers
- **SAP-007** (documentation-framework): Frontmatter schema for doc linkage
- **SAP-010** (memory-system): Event correlation via trace_id
- **SAP-012** (development-lifecycle): Feature/sprint/theme chains
- **SAP-015** (task-tracking): Git commit→task linkage via beads
- **JSON Schema**: Validation for feature-manifest.yaml
- **YAML**: Manifest and frontmatter format

### Downstream Dependencies

- **SAP-012 Enhancement**: Feature manifest creation integrated into DDD→BDD→TDD
- **SAP-007 Enhancement**: Frontmatter traceability fields (feature_id, code_references, test_references)
- **SAP-015 Enhancement**: Traceability validation subcommand in beads CLI
- **SAP-010 Enhancement**: Feature completion events + feature_id in all dev events
- **SAP-004 Enhancement**: Requirement/feature pytest markers + coverage reporting
- **Future SAPs**: All new SAPs required to demonstrate L2+ traceability

### Cross-References

- **Feature Manifest Schema**: Central artifact defining all linkages
- **Traceability Validation Framework**: 10 rules enforcing completeness
- **Bidirectional Linkage Pattern**: Prevents doc/code drift
- **Evidence-Based Completeness**: Features require tests+docs for validation

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Adoption friction** (developers resist additional process) | High | Use git hooks + justfile helpers for minimal disruption; progressive enhancement (L1→L2→L3); automation reduces manual work |
| **Feature manifest drift** (manifest outdated vs actual code) | High | Pre-commit hooks validate manifest consistency; CI/CD blocks merges with broken linkage; automated manifest generation from git log |
| **Validation false positives** (rules too strict) | Medium | 10 essential rules only (not comprehensive 50+); allow exceptions via configuration; iterative rule refinement based on adopter feedback |
| **Cross-SAP coordination** (5 SAP enhancements required) | Medium | Phased rollout (SAP-056 L1 first, then SAP enhancements); coordination requests for each SAP; dogfooding in chora-workspace before distribution |
| **Performance overhead** (validation scripts slow) | Low | Validation runs pre-commit only (not every keystroke); caching for repeated queries; incremental validation (only changed features) |

---

## 8. Open Questions

1. **Feature manifest location**: Root of repo vs `.chora/traceability/manifest.yaml`?
2. **Requirement ID format**: `REQ-XXX` vs `FEAT-X-REQ-Y` vs freeform?
3. **Validation enforcement**: Pre-commit block vs CI/CD warn vs manual review?
4. **Cross-repo linkage**: How to trace chora-workspace → chora-base dependencies in manifest?
5. **Retroactive migration**: Apply to existing features or new features only?
6. **Exception handling**: Allow temporary validation failures during refactors?

---

## 9. Related Capabilities

- **SAP-000** (sap-framework): Meta-framework for SAP structure
- **SAP-004** (testing-framework): Test markers for requirement traceability
- **SAP-007** (documentation-framework): Frontmatter for doc linkage
- **SAP-010** (memory-system): Event correlation for task traceability
- **SAP-012** (development-lifecycle): Feature→sprint→theme chains
- **SAP-015** (task-tracking): Git commit→task linkage
- **SAP-019** (sap-self-evaluation): Traceability maturity assessment
- **SAP-027** (dogfooding-patterns): 5-week pilot for SAP-056 validation

---

## 10. Approval & Sign-Off

**Charter Author**: Claude Code
**Date**: 2025-11-16
**Status**: Draft - Ready for Protocol Spec

**Beads Task**: .beads-i6mf
**Trace ID**: sap-056-creation

**Approved By**: _(Pending Victor review)_

---

**Version History**:
- **1.0.0** (2025-11-16): Initial charter for lifecycle-traceability SAP
