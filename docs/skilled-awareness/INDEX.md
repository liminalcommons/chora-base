# Skilled Awareness Package (SAP) Index

**Purpose**: Central registry of all capabilities packaged as SAPs in chora-base.

**Last Updated**: 2025-11-09
**Framework Version**: 1.0.0

---

## Overview

This index tracks all **40 capabilities** identified for SAP packaging across 4 roadmap phases + Wave 2 + Wave 3 + Wave 4 (React) + Week 5-6 Foundation + Week 7-8 User-Facing + Week 9-10 Advanced Patterns + Week 11-12 Advanced Patterns Part 2 + Immediate.

**Current Coverage**: 37/40 SAPs (92.5%) - Week 11-12 Advanced Patterns Part 2 in progress

**Target Coverage**:
- Phase 1: 3/14 (21%) ✅ Complete
- Phase 2: 7/14 (50%) ✅ Complete
- Phase 3: 13/14 (93%) ✅ Complete
- Phase 4: 14/14 (100%) ✅ Complete (SAP-013 metrics-tracking done!)
- Wave 2: 15/15 (100%) ✅ Complete (SAP-016 link-validation added!)

---

## Active SAPs

**Awareness Integration Status**: ✅ 33/33 PASS (100%) - Week 11-12 Advanced Patterns Part 2 SAPs Added (2025-11-09): SAP-039 (react-e2e-testing), SAP-040 (react-monorepo-architecture)

| SAP ID | Capability | Version | Status | Phase | Awareness | Location | Dependencies |
|--------| 2025-11-03 | SAP-027 (dogfooding-patterns) generated - Formalized 5-week dogfooding pilot methodology for validating patterns through internal use before ecosystem adoption | Claude Code |
| 2025-11-02 | SAP-029 (sap-generation) generated - Template-based SAP artifact generation to reduce creation time from 10 hours to 2 hours (80% savings) | Claude Code |
|------------|---------|--------|-------|-----------|----------|--------------|
| SAP-000 | sap-framework | 1.0.0 | Draft | Phase 1 | ✅ 4/4 | [sap-framework/](sap-framework/) | None (foundational) |
| SAP-001 | inbox-coordination | 1.0.0 | Pilot | Phase 1 | ⚠️  2/4 | [inbox/](inbox/) | None |
| SAP-002 | chora-base-meta | 1.0.0 | Draft | Phase 1 | ✅ 4/4 | [chora-base/](chora-base/) | SAP-000 |
| SAP-003 | project-bootstrap | 1.0.0 | Draft | Phase 2 | ✅ 4/4 | [project-bootstrap/](project-bootstrap/) | SAP-000 |
| SAP-004 | testing-framework | 1.0.0 | Draft | Phase 2 | ✅ 4/4 | [testing-framework/](testing-framework/) | SAP-000, SAP-003 |
| SAP-005 | ci-cd-workflows | 1.0.0 | Draft | Phase 2 | ✅ 4/4 | [ci-cd-workflows/](ci-cd-workflows/) | SAP-000, SAP-004 |
| SAP-006 | quality-gates | 1.0.0 | Draft | Phase 2 | ✅ 4/4 | [quality-gates/](quality-gates/) | SAP-000, SAP-004 |
| SAP-007 | documentation-framework | 1.0.0 | Draft | Phase 3 | ✅ 4/4 | [documentation-framework/](documentation-framework/) | SAP-000 |
| SAP-008 | automation-scripts | 1.0.0 | Draft | Phase 3 | ✅ 4/4 | [automation-scripts/](automation-scripts/) | SAP-000, SAP-012 |
| SAP-009 | agent-awareness | 2.1.0 | Active | Phase 3 | ✅ 5/5 | [agent-awareness/](agent-awareness/) | SAP-000, SAP-007 |
| SAP-010 | memory-system | 1.0.0 | Draft | Phase 3 | ✅ 4/4 | [memory-system/](memory-system/) | SAP-000 |
| SAP-011 | docker-operations | 1.0.0 | Draft | Phase 3 | ✅ 4/4 | [docker-operations/](docker-operations/) | SAP-000 |
| SAP-012 | development-lifecycle | 1.5.0 | Active | Phase 3 | ✅ 5/5 | [development-lifecycle/](development-lifecycle/) | SAP-000 |
| SAP-013 | metrics-tracking | 1.0.0 | Draft | Phase 4 | ✅ 4/4 | [metrics-tracking/](metrics-tracking/) | SAP-000 |
| SAP-014 | mcp-server-development | 1.0.0 | Active | Wave 3 | ✅ 4/4 | [mcp-server-development/](mcp-server-development/) | SAP-000, SAP-003, SAP-004, SAP-012 |
| SAP-015 | task-tracking | 1.0.0 | Pilot | Phase 1 | - | [task-tracking/](task-tracking/) | SAP-000 |
| SAP-016 | link-validation-reference-management | 1.0.0 | Active | Wave 2 | ✅ 4/4 | [link-validation-reference-management/](link-validation-reference-management/) | None (foundational) |
| SAP-017 | chora-compose-integration | 1.0.0 | Active | Wave 3 | ✅ 4/4 | [chora-compose-integration/](chora-compose-integration/) | SAP-003 |
| SAP-018 | chora-compose-meta | 1.0.0 | Active | Wave 3 | ✅ 4/4 | [chora-compose-meta/](chora-compose-meta/) | SAP-017 |
| SAP-019 | sap-self-evaluation | 1.0.0 | Active | Wave 3 | ✅ 4/4 | [sap-self-evaluation/](sap-self-evaluation/) | SAP-000 |
| SAP-020 | react-foundation | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-foundation/](react-foundation/) | SAP-000, SAP-003 |
| SAP-021 | react-testing | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-testing/](react-testing/) | SAP-000, SAP-004, SAP-020 |
| SAP-022 | react-linting | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-linting/](react-linting/) | SAP-000, SAP-006, SAP-020 |
| SAP-023 | react-state-management | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-state-management/](react-state-management/) | SAP-000, SAP-020 |
| SAP-024 | react-styling | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-styling/](react-styling/) | SAP-000, SAP-020 |
| SAP-025 | react-performance | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-performance/](react-performance/) | SAP-000, SAP-020 |
| SAP-026 | react-accessibility | 1.0.0 | Active | Wave 4 | ✅ 5/5 | [react-accessibility/](react-accessibility/) | SAP-000, SAP-020, SAP-021 |
| SAP-033 | react-authentication | 1.0.0 | Pilot | Week 5-6 Foundation | ✅ 5/5 | [react-authentication/](react-authentication/) | SAP-000, SAP-020, SAP-034 |
| SAP-034 | react-database-integration | 1.0.0 | Pilot | Week 5-6 Foundation | ✅ 5/5 | [react-database-integration/](react-database-integration/) | SAP-000, SAP-020 |
| SAP-041 | react-form-validation | 1.0.0 | Pilot | Week 5-6 Foundation | ✅ 5/5 | [react-form-validation/](react-form-validation/) | SAP-000, SAP-020, SAP-033 |
| SAP-035 | react-file-upload | 1.0.0 | Pilot | Week 7-8 User-Facing | ✅ 5/5 | [react-file-upload/](react-file-upload/) | SAP-000, SAP-020, SAP-033, SAP-034 |
| SAP-036 | react-error-handling | 1.0.0 | Pilot | Week 7-8 User-Facing | ✅ 5/5 | [react-error-handling/](react-error-handling/) | SAP-000, SAP-020 |
| SAP-037 | react-realtime-synchronization | 1.0.0 | Pilot | Week 9-10 Advanced Part 1 | ✅ 5/5 | [react-realtime-synchronization/](react-realtime-synchronization/) | SAP-000, SAP-020, SAP-023, SAP-034 |
| SAP-038 | react-internationalization | 1.0.0 | Pilot | Week 9-10 Advanced Part 1 | ✅ 5/5 | [react-internationalization/](react-internationalization/) | SAP-000, SAP-020, SAP-041 |
| SAP-039 | react-e2e-testing | 1.0.0 | Pilot | Week 11-12 Advanced Part 2 | ✅ 5/5 | [react-e2e-testing/](react-e2e-testing/) | SAP-000, SAP-020, SAP-021, SAP-033 |
| SAP-040 | react-monorepo-architecture | 1.0.0 | Pilot | Week 11-12 Advanced Part 2 | ✅ 5/5 | [react-monorepo-architecture/](react-monorepo-architecture/) | SAP-000, SAP-020, SAP-003 |
| SAP-028 | publishing-automation | 1.0.0 | Active | Immediate | ✅ 5/5 | [publishing-automation/](publishing-automation/) | SAP-003, SAP-005 |
| SAP-029 | sap-generation | 1.0.0 | Pilot | Pilot | - | [sap-generation/](sap-generation/) | SAP-000 |
| SAP-027 | dogfooding-patterns | 1.0.0 | Active | Formalization | - | [dogfooding-patterns/](dogfooding-patterns/) | SAP-000, SAP-029 |

**Awareness Score Legend**:
- ✅ 4/4: All checks pass (post-install section, AGENTS.md mention, validation cmd, agent instructions)
- ⚠️  2-3/4: Passing with warnings
- ❌ 0-1/4: Failing

**Audit Report**: [docs/project-docs/audits/wave-2-sap-awareness-integration-audit.md](../project-docs/audits/wave-2-sap-awareness-integration-audit.md)

---

## Planned SAPs

### Phase 1: Framework Hardening (2025-10 → 2025-11)

| SAP ID | Capability | Priority | Dependencies | Notes |
|--------|------------|----------|--------------|-------|
| SAP-000 | sap-framework | P0 | None | ✅ Complete (5 artifacts) |
| SAP-001 | inbox-coordination | P0 | None | ✅ Pilot complete |
| SAP-002 | chora-base-meta | P0 | SAP-000 | ✅ Complete (5 artifacts) |

**Phase 1 Target**: 3 SAPs (21% coverage) ✅ COMPLETE

### Phase 2: Core Capability Migration (2025-11 → 2026-01)

| SAP ID | Capability | Priority | Dependencies | Status |
|--------|------------|----------|--------------|--------|
| SAP-003 | project-bootstrap | P0 | SAP-000 | ✅ Complete (5 artifacts) |
| SAP-004 | testing-framework | P0 | SAP-000, SAP-003 | ✅ Complete (5 artifacts) |
| SAP-005 | ci-cd-workflows | P0 | SAP-000, SAP-004 | ✅ Complete (5 artifacts) |
| SAP-006 | quality-gates | P0 | SAP-000, SAP-004 | ✅ Complete (5 artifacts) |

**Phase 2 Target**: 7 SAPs total (50% coverage, +4 from Phase 1) ✅ COMPLETE

**Core Capabilities**: Every adopter needs these immediately (project bootstrap, testing, CI/CD, quality).

### Phase 3: Extended Capability Coverage (2026-01 → 2026-03)

| SAP ID | Capability | Priority | Dependencies | Estimated Effort |
|--------|------------|----------|--------------|------------------|
| SAP-007 | documentation-framework | P1 | SAP-000 | ✅ Complete (Batch 1) |
| SAP-008 | automation-scripts | P1 | SAP-000, SAP-012 | ✅ Complete (Batch 2) |
| SAP-009 | agent-awareness | P1 | SAP-000, SAP-007 | ✅ Complete (Batch 1) |
| SAP-010 | memory-system | P1 | SAP-000 | ✅ Complete (Batch 3) |
| SAP-011 | docker-operations | P1 | SAP-000 | ✅ Complete (Batch 3) |
| SAP-012 | development-lifecycle | P1 | SAP-000 | ✅ Complete (Batch 2) |

**Phase 3 Target**: 13 SAPs total (93% coverage, +6 from Phase 2)

**Extended Capabilities**: High value but not immediately required. Adopters can succeed without these initially.

### Phase 4: Optimization & Metrics (2026-03 → 2026-05)

| SAP ID | Capability | Priority | Dependencies | Estimated Effort |
|--------|------------|----------|--------------|------------------|
| SAP-013 | metrics-tracking | P2 | SAP-000 | ✅ Complete (Phase 4) |

**Phase 4 Target**: 14 SAPs total (100% coverage, +1 from Phase 3) ✅ COMPLETE!

**Optimization**: Measurement and improvement capabilities.

### Wave 2: Quality Assurance & SAP Audit (2025-10 → 2025-11)

| SAP ID | Capability | Priority | Dependencies | Status |
|--------|------------|----------|--------------|--------|
| SAP-016 | link-validation-reference-management | P0 | None (foundational) | ✅ Active (all 5 artifacts + script complete) |

**Wave 2 Target**: 15 SAPs total (100% enhanced coverage, +1 from Phase 4) ✅ COMPLETE!

**Quality Assurance**: Link validation for documentation integrity, enables SAP audit workflow.

### Wave 3: Technology-Specific Capabilities (2025-10)

| SAP ID | Capability | Priority | Dependencies | Status |
|--------|------------|----------|--------------|--------|
| SAP-014 | mcp-server-development | P1 | SAP-000, SAP-003, SAP-004, SAP-012 | ✅ Active (6 artifacts + 8 supporting docs + 11 templates) |

**Wave 3 Target**: First technology-specific SAP demonstrating extensibility pattern ✅ COMPLETE!

**Key Innovation**: Establishes pattern for technology-specific SAPs. MCP server development extracted from core into optional capability, making chora-base truly universal. Future tech SAPs: Django (SAP-017), FastAPI (SAP-018), React (SAP-019).

---

## SAP Dependency Graph

```
SAP-000 (sap-framework) [FOUNDATIONAL]
   ↓
   ├─→ SAP-001 (inbox-coordination)
   ├─→ SAP-002 (chora-base-meta)
   ├─→ SAP-003 (project-bootstrap)
   │      ↓
   │      └─→ SAP-004 (testing-framework)
   │             ↓
   │             ├─→ SAP-005 (ci-cd-workflows)
   │             └─→ SAP-006 (quality-gates)
   ├─→ SAP-007 (documentation-framework)
   ├─→ SAP-008 (automation-scripts)
   ├─→ SAP-009 (agent-awareness)
   ├─→ SAP-010 (memory-system / A-MEM)
   ├─→ SAP-011 (docker-operations)
   ├─→ SAP-012 (development-lifecycle)
   └─→ SAP-013 (metrics-tracking)

SAP-016 (link-validation) [FOUNDATIONAL - WAVE 2]
   ↓
   └─→ Enhances: SAP-000, SAP-007 (documentation quality)
```

**Key Dependencies**:
- **SAP-000** is foundational; all SAPs depend on it
- **SAP-003 → SAP-004**: Testing depends on project structure
- **SAP-004 → SAP-005, SAP-006**: CI/CD and quality depend on testing

---

## Capability Details

### Meta & Foundational (3 capabilities)

#### SAP-000: sap-framework
- **Purpose**: Meta-capability defining how SAPs work
- **Includes**: Protocol, governance, templates, SAP Index, blueprint-based installation
- **Status**: ✅ Draft (all 5 artifacts complete)
- **Scope**: Vision & Strategy, Planning, Implementation

#### SAP-001: inbox-coordination
- **Purpose**: Cross-repo coordination, capability registry, broadcast workflow
- **Includes**: inbox/ directory, schemas, coordination requests, ecosystem examples
- **Status**: ✅ Pilot (reference implementation)
- **Scope**: Planning, Implementation

#### SAP-002: chora-base-meta
- **Purpose**: chora-base describes itself using SAP framework (dogfooding)
- **Includes**: Charter, protocol, awareness for chora-base as a whole
- **Status**: 🔄 Draft (next Phase 1 task)
- **Scope**: All (Vision & Strategy, Planning, Implementation)

### Core Infrastructure (4 capabilities)

#### SAP-003: project-bootstrap
- **Purpose**: Blueprint generation, static-template scaffolding, setup.py workflow
- **Includes**: blueprints/ directory, static-template/ structure, generation logic
- **Status**: ✅ Draft (all 5 artifacts complete)
- **Scope**: Implementation
- **Key Features**: Zero-dependency generation, 12 blueprints, variable substitution, validation

#### SAP-004: testing-framework
- **Purpose**: pytest, coverage, fixtures, test patterns
- **Includes**: tests/ structure, conftest.py, coverage config, pytest-asyncio patterns
- **Status**: ✅ Draft (all 5 artifacts complete)
- **Scope**: Implementation
- **Key Features**: 85% coverage standard, async testing, 6 test patterns documented

#### SAP-005: ci-cd-workflows
- **Purpose**: GitHub Actions (test, lint, release, security, docs-quality)
- **Includes**: .github/workflows/ directory, all 10 workflow files
- **Status**: ✅ Draft (all 5 artifacts complete)
- **Scope**: Implementation
- **Key Features**: Matrix testing (Python 3.11-3.13), caching, security-first, parallel execution

#### SAP-006: quality-gates
- **Purpose**: pre-commit hooks, linting, type checking, coverage enforcement
- **Includes**: .pre-commit-config.yaml, ruff (linter+formatter), mypy (type checking)
- **Status**: ✅ Draft (all 5 artifacts complete)
- **Scope**: Implementation
- **Key Features**: Ruff-based (200x faster), 7 hooks, strict type checking, correct hook order

### Developer Experience (3 capabilities)

#### SAP-007: documentation-framework
- **Purpose**: Diataxis structure, frontmatter schema, executable How-Tos, test extraction
- **Includes**: DOCUMENTATION_STANDARD.md (~700 lines), Diataxis 4 types, frontmatter schema, scripts/extract_tests.py
- **Status**: ✅ Draft (all 5 artifacts complete, Phase 3 Batch 1)
- **Scope**: All (includes vision/strategy docs, planning templates, implementation guides)
- **Key Features**: Diataxis framework (Tutorial/How-To/Reference/Explanation), test extraction from How-Tos, frontmatter validation

#### SAP-008: automation-scripts
- **Purpose**: scripts/ directory (25 scripts), justfile tasks (30+ commands), release automation
- **Includes**: 25 scripts (shell + Python) in static-template/scripts/, justfile (~150 lines)
- **Status**: ✅ Draft (all 5 artifacts complete, Phase 3 Batch 2)
- **Scope**: Implementation
- **Key Features**: Idempotent scripts, justfile unified interface, safety contracts (error handling, rollback), 8 script categories

#### SAP-009: agent-awareness
- **Purpose**: AGENTS.md/CLAUDE.md patterns, nested awareness structure with file size thresholds, Critical Workflows pattern, automated validation tooling
- **Includes**: AGENTS.md.blueprint (~900 lines), CLAUDE.md.blueprint (~450 lines), 5 domain AGENTS.md files (~1,100 lines), 3 foundation tools (intent-router.py, chora-search.py, suggest-next.py with inbox integration), validation script (scripts/validate-nested-awareness.py, 549 lines), 4 justfile recipes
- **Status**: ✅ Active (v2.1.0 complete - Phase 3 + Phase 4, COORD-2025-012)
- **Scope**: Implementation + Tooling
- **Key Features**: Nested awareness hierarchy with domain-specific files, file size thresholds (1k warning, 2k critical), Critical Workflows pattern (lines 20-100), automated validation (127 files in seconds), 7-step splitting strategy, frontmatter schema (nested_structure, nested_files), 59% average file size reduction (proven in 3 Tier 1 SAPs), dual-file pattern (AGENTS + CLAUDE), "Nearest File Wins", progressive context loading (Phase 1/2/3), bidirectional translation (conversational ↔ formal), user preferences (100+ options)

### Advanced Features (3 capabilities)

#### SAP-010: memory-system (A-MEM)
- **Purpose**: Event log, knowledge graph, agent profiles, trace correlation
- **Includes**: .chora/memory/ structure, A-MEM architecture, Chora ecosystem event schema v1.0, query interfaces
- **Status**: ✅ Draft (all 5 artifacts complete, Phase 3 Batch 3)
- **Scope**: Implementation
- **Key Features**: 4 memory types, Zettelkasten knowledge graph, cross-session learning, 30% reduction in repeated mistakes
- **Note**: User explicitly mentioned A-MEM as needing SAP

#### SAP-011: docker-operations
- **Purpose**: Dockerfiles, docker-compose, container optimization, MCP deployment
- **Includes**: Dockerfile (multi-stage wheel build), Dockerfile.test (CI-optimized), docker-compose.yml, .dockerignore, DOCKER_BEST_PRACTICES.md
- **Status**: ✅ Draft (all 5 artifacts complete, Phase 3 Batch 3)
- **Scope**: Implementation
- **Key Features**: Multi-stage builds (150-250MB images), GitHub Actions cache (6x faster), non-root execution, 81% build context reduction
- **Current Adopter Pain**: "No documented lifecycle for enabling/disabling Docker options; inconsistent adoption"

#### SAP-012: development-lifecycle
- **Purpose**: DDD → BDD → TDD workflow, 8-phase lifecycle (Vision → Monitoring), Light+ Planning Model, sprint planning
- **Includes**: 6 workflow docs (5,285 lines), sprint/release templates, process metrics, ANTI_PATTERNS.md (1,309 lines), LIGHT_PLUS_REFERENCE.md (v1.5.0)
- **Status**: ✅ Active (v1.5.0, all 5 artifacts complete, Phase 3 Batch 2)
- **Scope**: All (includes vision/strategy, planning, implementation)
- **Key Features**: 8-phase lifecycle, Light+ Planning (4 constructs: Strategy → Releases → Features → Tasks), DDD→BDD→TDD integration, 40-80% defect reduction (research-backed), decision trees

### Cross-Repository (1 capability)

#### SAP-013: metrics-tracking
- **Purpose**: ClaudeROICalculator, process metrics, sprint velocity tracking
- **Includes**: utils/claude_metrics.py (~459 lines), PROCESS_METRICS.md (~855 lines), sprint/release dashboards
- **Status**: ✅ Draft (all 5 artifacts complete, Phase 4)
- **Scope**: Planning, Implementation
- **Key Features**: Claude ROI calculation, quality/velocity/adherence tracking, research-backed targets, $109k/year savings estimate

### Quality Assurance (1 capability - Wave 2)

#### SAP-016: link-validation-reference-management
- **Purpose**: Automated markdown link validation (internal + external), prevents broken documentation references
- **Includes**: scripts/validate-links.sh, capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger
- **Status**: ✅ Active (all 5 artifacts + script complete, Wave 2 Phase 1)
- **Scope**: Implementation
- **Key Features**: Internal link validation (100%), external link health checks, CI/CD integration, SAP audit workflow (Step 3), 4-domain architecture validation
- **Wave 2 Context**: Created as highest-priority foundation for auditing all 15 SAPs, ensures cross-domain reference integrity

---

## Status Legend

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **Draft** | In development, artifacts incomplete | Complete artifacts, test with agent |
| **Pilot** | Ready for limited adoption, feedback phase | Collect pilot feedback, iterate |
| **Active** | Production-ready, recommended for all adopters | Maintain, enhance, support |
| **Deprecated** | Superseded, upgrade recommended | Migrate to replacement SAP |
| **Archived** | No longer maintained | Reference only |

**Symbols**:
- ✅ Complete / In use
- 🔄 In progress
- 📋 Planned / Not started

---

## Priority Legend

| Priority | Meaning | Timing |
|----------|---------|--------|
| **P0** | Critical, required immediately | Phase 1-2 |
| **P1** | High value, next phase | Phase 3 |
| **P2** | Nice to have, future | Phase 4+ |

---

## Quick Links

**Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](sap-framework/) - Framework SAP
- [document-templates.md](document-templates.md) - SAP artifact templates
- [chora-base-sap-roadmap.md](chora-base-sap-roadmap.md) - Phased adoption plan

**Active/Pilot SAPs**:
- [sap-framework/](sap-framework/) - SAP-000 (Draft)
- [inbox/](inbox/) - SAP-001 (Pilot)

**Examples**:
- [inbox/examples/health-monitoring-w3/](inbox/examples/health-monitoring-w3/) - Complete capability evolution example

---

## Adoption Statistics

### By Phase

| Phase | Target SAPs | Completed | In Progress | Planned | Coverage |
|-------|-------------|-----------|-------------|---------|----------|
| Phase 1 | 3 | 3 | 0 | 0 | 21% ✅ Complete |
| Phase 2 | 4 | 4 | 0 | 0 | +29% ✅ Complete |
| Phase 3 | 6 | 6 | 0 | 0 | +43% ✅ Complete (All 6 Phase 3 SAPs) |
| Phase 4 | 1 | 1 | 0 | 0 | +7% ✅ Complete (SAP-013) |
| Wave 2 | 1 | 1 | 0 | 0 | +0% ✅ Complete (SAP-016) |
| **Total** | **15** | **15** | **0** | **0** | **100% 🎉 COMPLETE!** |

### By Priority

| Priority | Total | Completed | In Progress | Planned |
|----------|-------|-----------|-------------|---------|
| P0 | 8 | 8 | 0 | 0 |
| P1 | 6 | 6 | 0 | 0 |
| P2 | 1 | 1 | 0 | 0 |

### By Scope

| Scope | SAPs | Examples |
|-------|------|----------|
| Vision & Strategy | 3 | development-lifecycle, documentation-framework, chora-base-meta |
| Planning | 3 | inbox-coordination, documentation-framework, metrics-tracking |
| Implementation | 12 | Most capabilities |
| All (multi-scope) | 3 | chora-base-meta, development-lifecycle, documentation-framework |

---

## How to Use This Index

### For AI Agents

**Finding SAPs**:
1. Search by capability name (e.g., "testing-framework")
2. Check status (Draft, Pilot, Active)
3. Navigate to location link

**Installing SAPs**:
1. Find SAP in "Active SAPs" or "Draft SAPs" table
2. Navigate to SAP directory
3. Read `adoption-blueprint.md`
4. Execute installation steps

**Creating SAPs**:
1. Check "Planned SAPs" for next capability
2. Review dependencies
3. Follow framework: [sap-framework/](sap-framework/)
4. Update this index when complete

### For Humans

**Roadmap Planning**:
- Review "Planned SAPs" by phase
- Check effort estimates
- Plan sprint allocation

**Dependency Management**:
- Review "SAP Dependency Graph"
- Install dependencies first
- Track blockers

**Progress Tracking**:
- Check "Adoption Statistics"
- Review coverage percentages
- Monitor phase targets

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-11-09 | Week 11-12 Advanced Patterns Part 2: SAP-039 (react-e2e-testing), SAP-040 (react-monorepo-architecture) added - Playwright + Cypress, Turborepo + Nx + pnpm (92.5% coverage, 37/40 SAPs) | Claude Code |
| 2025-11-09 | Week 9-10 Advanced Patterns Part 1: SAP-037 (react-realtime-synchronization), SAP-038 (react-internationalization) added - WebSockets + 3 alternatives, next-intl + react-i18next (92% coverage, 35/38 SAPs) | Claude Code |
| 2025-11-10 | SAP-012 v1.5.0 version synchronization: All 7 artifacts synchronized to v1.5.0 (Light+ Planning Model, Vision Synthesis, CLAUDE.md), catalog and index updated (Priority 1 audit action complete) | Claude Code |
| 2025-11-10 | SAP-009 v2.1.0 complete: Nested awareness pattern with file size thresholds (1k/2k), Critical Workflows sections, automated validation tooling (validate-nested-awareness.py), 59% token reduction in 3 Tier 1 SAPs (Phase 3 + Phase 4 complete, 16h total) | Claude Code |
| 2025-11-09 | Week 7-8 User-Facing: SAP-035 (react-file-upload), SAP-036 (react-error-handling) added - UploadThing + 3 storage alternatives, Next.js 15 Error Boundaries + Sentry (92% coverage, 33/36 SAPs) | Claude Code |
| 2025-11-09 | Week 5-6 Foundation: SAP-033 (react-authentication), SAP-034 (react-database-integration), SAP-041 (react-form-validation) added - NextAuth.js v5, Prisma/Drizzle ORMs, React Hook Form + Zod (91% coverage, 31/34 SAPs) | Claude Code |
| 2025-11-02 | SAP-028 (publishing-automation) complete - Secure PyPI publishing with OIDC trusted publishing as default, eliminating long-lived API tokens (93% coverage, 26/28 SAPs) | Claude Code |
| 2025-11-01 | Wave 4: SAP-025 (react-performance) complete - Core Web Vitals optimization with Next.js 15 + Vite 7 templates (92% coverage, 24/26 SAPs) | Claude Code |
| 2025-11-01 | Wave 4: SAP-022 (react-linting) complete - ESLint 9 + Prettier 3 + pre-commit hooks (81% coverage, 21/26 SAPs) | Claude Code |
| 2025-10-31 | SAP-009 v1.1.0 complete: Bidirectional translation layer with 5 domain AGENTS.md files, inbox protocol integration (COORD-2025-004, v4.1.3) | Claude Code |
| 2025-10-28 | Wave 2: SAP-016 (link-validation-reference-management) complete - Foundational QA capability | Claude Code |
| 2025-10-28 | 🎉 100% COMPLETE! SAP-013 (metrics-tracking) completes Phase 4 - ALL 14 SAPs DONE! | Claude Code |
| 2025-10-28 | Phase 3 Complete: SAP-011 (docker-operations) completes Phase 3 (93% coverage, 13/14 SAPs) | Claude Code |
| 2025-10-28 | Phase 3 Batch 3: SAP-010 (memory-system/A-MEM) complete (86% coverage, 12/14 SAPs) | Claude Code |
| 2025-10-28 | Phase 3 Batch 2: SAP-012 (development-lifecycle), SAP-008 (automation-scripts) complete (79% coverage) | Claude Code |
| 2025-10-28 | Phase 3 Batch 1: SAP-007 (documentation-framework), SAP-009 (agent-awareness) complete (64% coverage) | Claude Code |
| 2025-10-28 | Phase 2 Complete: SAP-003, SAP-004, SAP-005, SAP-006 all artifacts complete (50% coverage) | Claude Code |
| 2025-10-27 | SAP-002 (chora-base-meta) marked as Draft (artifacts complete), Phase 1 complete | Claude Code |
| 2025-10-27 | Initial index creation with 14 capabilities identified | Claude Code |
| 2025-10-27 | SAP-000 (sap-framework) marked as Draft (artifacts complete) | Claude Code |
| 2025-10-27 | SAP-001 (inbox-coordination) marked as Pilot (reference implementation) | Claude Code |

---

**Maintainer**: Victor (chora-base owner)
**Review Cycle**: Updated with each SAP release
**Next Review**: 2026-01-31 (end of Phase 2, start of Phase 3)
