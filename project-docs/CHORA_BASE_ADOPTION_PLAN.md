---
title: Chora-Base v4.1.0 Full Adoption Plan
status: planning
timeline: 4 weeks
type: adoption-plan
created: 2025-10-31
last_updated: 2025-10-31
owner: mcp-orchestration
target_version: chora-base v4.1.0
total_saps: 18
estimated_hours: 77
---

# Chora-Base v4.1.0 Full Adoption Plan

**Goal:** Achieve 100% chora-base v4.1.0 adoption (all 18 SAPs) for mcp-orchestration

**Timeline:** 4 weeks (November-December 2025)
**Approach:** Incremental weekly adoption
**Total Effort:** ~77 hours (~20 hours/week)
**Status:** 📋 Planning

---

## Executive Summary

mcp-orchestration will adopt the complete chora-base v4.1.0 Skilled Awareness Package (SAP) framework to standardize development practices, improve documentation quality, enable ecosystem coordination, and integrate advanced MCP server development patterns.

### Current State
- **Starting Point:** 0% SAP adoption (treating as fresh start)
- **Generated From:** chora-base v2.0.9 template
- **Has:** Basic project structure, some documentation, testing, CI/CD
- **Missing:** SAP framework, formal protocols, 4-domain documentation, development lifecycle patterns

### Target State
- **Goal:** 100% SAP adoption (all 18 SAPs installed and adopted)
- **Deliverable:** `docs/skilled-awareness/` with 90+ artifacts (5 per SAP)
- **Outcome:** Full chora-base v4.1.0 compliance with ecosystem coordination capability

### Key Benefits
1. **Formal Protocols** - SAP-000 framework for structured capability documentation
2. **Ecosystem Coordination** - SAP-001 inbox protocol for cross-repo collaboration
3. **Agent Awareness** - SAP-009 comprehensive AGENTS.md/CLAUDE.md patterns
4. **Quality Gates** - SAP-006 pre-commit hooks, 85%+ coverage enforcement
5. **MCP Patterns** - SAP-014 FastMCP development templates and conventions
6. **Automation** - SAP-008 justfile with 30+ commands
7. **Documentation** - SAP-007 4-domain Diátaxis structure
8. **Metrics** - SAP-013 ROI tracking for development velocity

---

## Adoption Timeline Overview

| Week | Focus | SAPs | Cumulative | Hours | Status |
|------|-------|------|------------|-------|--------|
| 1 | Foundation | 5 | 5/18 (28%) | 15 | 📋 Planned |
| 2 | Development Workflow | 5 | 10/18 (56%) | 20 | 📋 Planned |
| 3 | Developer Experience | 4 | 14/18 (78%) | 20 | 📋 Planned |
| 4 | MCP-Specific & Metrics | 4 | 18/18 (100%) | 22 | 📋 Planned |
| **Total** | **4 weeks** | **18** | **100%** | **77** | 📋 **Planning** |

---

## Week 1: Foundation (minimal-entry set)

**Timeline:** Week of Nov XX, 2025
**Focus:** SAP framework, inbox coordination, agent awareness, link validation
**SAPs:** 5 (SAP-000, SAP-001, SAP-002, SAP-009, SAP-016)
**Effort:** ~15 hours
**Status:** 📋 Planned

### Installation

```bash
# Clone chora-base v4.1.0
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base
cd /tmp/chora-base
git checkout v4.1.0

# Preview installation (dry-run)
python scripts/install-sap.py --set minimal-entry \
  --source /tmp/chora-base \
  --dry-run

# Install minimal-entry SAP set
cd /Users/victorpiper/code/mcp-orchestration
python /tmp/chora-base/scripts/install-sap.py --set minimal-entry \
  --source /tmp/chora-base
```

### SAPs to Adopt

#### SAP-000: SAP Framework
- **Size:** 125 KB
- **Dependencies:** None
- **Description:** Core SAP framework and protocols defining how Skilled Awareness Packages work
- **Capabilities:** SAP protocol specification, governance standards, document templates, installation patterns, awareness integration
- **Time:** 1 hour
- **Activities:**
  - Read `capability-charter.md` and `protocol-spec.md`
  - Understand 5-artifact pattern (charter, spec, guide, blueprint, ledger)
  - Review SAP governance and contribution process
  - Understand adoption workflow

#### SAP-001: Inbox Coordination Protocol
- **Size:** 45 KB
- **Dependencies:** None
- **Status:** ⚠️ Pilot (may undergo changes)
- **Description:** Cross-repo coordination protocol using inbox directory for capability discovery and coordination requests
- **Capabilities:** Cross-repo coordination, capability registry, broadcast workflow, async collaboration
- **Time:** 2-3 hours
- **Activities:**
  - Copy JSON schemas to `inbox/schemas/`:
    - `coordination-request.schema.json`
    - `implementation-task.schema.json`
    - `strategic-proposal.schema.json`
  - Validate existing coordination requests against schemas
  - Update `inbox/README.md` with formal protocol references
  - Document schema-compliant request examples
  - Set up inbox coordination workflow

#### SAP-002: Chora-Base Meta Package
- **Size:** 78 KB
- **Dependencies:** SAP-000
- **Description:** Meta-capability describing chora-base itself using SAP framework (dogfooding demonstration)
- **Capabilities:** Project charter, architecture overview, 4-domain documentation, SAP framework integration, universal foundation patterns
- **Time:** 2-3 hours
- **Activities:**
  - Read chora-base architecture documentation
  - Understand meta-SAP pattern
  - Document mcp-orchestration as a capability using SAP pattern
  - Create `.chorabase` file for version tracking
  - Link to chora-base patterns in documentation

#### SAP-009: Agent Awareness System
- **Size:** 98 KB
- **Dependencies:** SAP-000, SAP-007
- **Description:** AGENTS.md/CLAUDE.md patterns with nested awareness files and progressive context loading
- **Capabilities:** Dual-file pattern (AGENTS + CLAUDE), nested awareness hierarchy, nearest file wins, progressive context loading, 200k token budget management
- **Time:** 4-5 hours
- **Activities:**
  - Review existing AGENTS.md files (if any)
  - Create/enhance root AGENTS.md following SAP-009 patterns
  - Create/enhance root CLAUDE.md following SAP-009 patterns
  - Create nested AGENTS.md files for key directories:
    - `src/mcp_orchestrator/AGENTS.md`
    - `tests/AGENTS.md`
    - `scripts/AGENTS.md`
    - `docs/AGENTS.md`
  - Implement progressive context loading patterns
  - Document 200k token budget management

#### SAP-016: Link Validation & Reference Management
- **Size:** 62 KB
- **Dependencies:** None (foundational)
- **Description:** Automated markdown link validation (internal + external) preventing broken documentation references
- **Capabilities:** Internal link validation (100%), external link health checks, CI/CD integration, 4-domain architecture validation, SAP audit workflow support
- **Time:** 2-3 hours
- **Activities:**
  - Copy `scripts/validate-links.sh` to project
  - Run initial link validation across all documentation
  - Fix any broken links found
  - Add link validation to GitHub Actions CI/CD
  - Configure pre-commit hook for link validation
  - Document link validation workflow

### Week 1 Deliverables

- [x] `docs/skilled-awareness/` directory created with 5 SAPs (25 artifacts)
- [ ] `.chorabase` file tracking chora-base v4.1.0
- [ ] Root AGENTS.md created/enhanced following SAP-009 patterns
- [ ] Root CLAUDE.md created/enhanced following SAP-009 patterns
- [ ] `inbox/schemas/` directory with 3 JSON schemas
- [ ] `scripts/validate-links.sh` installed and operational
- [ ] Link validation integrated into CI/CD
- [ ] All existing documentation links validated and fixed
- [ ] Commit: "feat: Week 1 - Adopt chora-base minimal-entry SAPs (5/18)"

### Week 1 Success Criteria

- ✅ SAP-000 framework understood and documented
- ✅ 5 SAPs installed with all 25 artifacts present
- ✅ AGENTS.md and CLAUDE.md functional for AI agents
- ✅ Inbox protocol schemas validate existing coordination requests
- ✅ Link validation passing (0 broken links)
- ✅ CI/CD runs link validation on all PRs
- ✅ `.chorabase` file tracks v4.1.0 adoption

---

## Week 2: Development Workflow

**Timeline:** Week of Nov XX, 2025
**Focus:** Testing framework, CI/CD workflows, quality gates, documentation
**SAPs:** 5 (SAP-003, SAP-004, SAP-005, SAP-006, SAP-007)
**Effort:** ~20 hours
**Status:** 📋 Planned

### Installation

```bash
# Install additional SAPs (dependencies auto-resolved)
cd /Users/victorpiper/code/mcp-orchestration
python /tmp/chora-base/scripts/install-sap.py \
  SAP-003 SAP-004 SAP-005 SAP-006 SAP-007 \
  --source /tmp/chora-base
```

### SAPs to Adopt

#### SAP-003: Project Bootstrap & Scaffolding
- **Size:** 92 KB
- **Dependencies:** SAP-000
- **Description:** Copier-based project generation from static-template with variable substitution
- **Capabilities:** Project scaffolding, template generation, variable substitution, directory structure setup
- **Time:** 2 hours
- **Activities:**
  - Review Copier patterns (mcp-orchestration already generated)
  - Audit project structure against chora-base template
  - Update `.copier-answers.yml` if needed
  - Document any mcp-orchestration-specific deviations
  - Review static-template patterns for future reference

#### SAP-004: Testing Framework
- **Size:** 89 KB
- **Dependencies:** SAP-000, SAP-003
- **Description:** pytest-based testing framework with 85%+ coverage patterns and async support
- **Capabilities:** pytest configuration, coverage enforcement (85%+), test fixtures, async testing patterns, 6 test pattern templates
- **Time:** 6-8 hours
- **Activities:**
  - Review current test coverage: `pytest --cov=src --cov-report=term-missing`
  - Enhance `pyproject.toml` with SAP-004 pytest configuration
  - Update `.coveragerc` to enforce 85%+ coverage
  - Add comprehensive test fixtures in `tests/conftest.py`
  - Implement async testing patterns for MCP tools
  - Write tests to reach 85%+ coverage threshold
  - Add 6 test pattern templates from SAP-004
  - Configure coverage enforcement in CI/CD

#### SAP-005: CI/CD Workflows
- **Size:** 67 KB
- **Dependencies:** SAP-000, SAP-004
- **Description:** GitHub Actions workflows for testing, linting, security, and release automation
- **Capabilities:** Matrix testing (Python 3.11-3.13), automated linting, security scanning (CodeQL), dependency review, release automation
- **Time:** 3-4 hours
- **Activities:**
  - Review current `.github/workflows/` (9 workflows present)
  - Enhance workflows with SAP-005 patterns:
    - Matrix testing across Python 3.11, 3.12, 3.13
    - Automated linting integration
    - Security scanning (CodeQL) enhancement
    - Dependency review workflow
  - Add release automation workflow
  - Configure workflow artifacts and caching
  - Test all workflows on feature branch

#### SAP-006: Quality Gates
- **Size:** 54 KB
- **Dependencies:** SAP-000, SAP-004
- **Description:** Pre-commit hooks, ruff linting, mypy type checking, and coverage enforcement
- **Capabilities:** Pre-commit hooks (7 hooks), Ruff linting (200x faster), Mypy type checking, coverage enforcement, security scanning
- **Time:** 3-4 hours
- **Activities:**
  - Review current `.pre-commit-config.yaml`
  - Add all 7 SAP-006 pre-commit hooks:
    - trailing-whitespace, end-of-file-fixer, check-yaml
    - check-added-large-files, ruff, mypy, pytest-cov
  - Configure ruff for 200x faster linting
  - Configure mypy for strict type checking
  - Add coverage enforcement hook (85%+)
  - Run: `pre-commit run --all-files`
  - Fix any issues found
  - Document quality gate workflow

#### SAP-007: Documentation Framework
- **Size:** 112 KB
- **Dependencies:** SAP-000
- **Description:** Diátaxis-based 4-domain documentation architecture with frontmatter schema and test extraction
- **Capabilities:** Diátaxis 4-domain structure, frontmatter schema validation, executable how-to guides, test extraction from docs, DOCUMENTATION_STANDARD.md (700 lines)
- **Time:** 4-6 hours
- **Activities:**
  - Review current documentation structure
  - Reorganize into 4-domain Diátaxis architecture:
    - `docs/user-docs/tutorials/` (learning-oriented)
    - `docs/user-docs/how-to/` (task-oriented)
    - `docs/user-docs/reference/` (information-oriented)
    - `docs/user-docs/explanation/` (understanding-oriented)
  - Copy `DOCUMENTATION_STANDARD.md` (700 lines) to root
  - Add frontmatter schema validation
  - Implement executable how-to guides pattern
  - Add `scripts/extract_tests.py` for test extraction from docs
  - Update all documentation with proper frontmatter
  - Run validation: `scripts/validate-links.sh`

### Week 2 Deliverables

- [ ] 10 SAPs total installed (50 artifacts)
- [ ] Test coverage ≥85% enforced in CI/CD
- [ ] Pre-commit hooks configured and functional (7 hooks)
- [ ] Enhanced GitHub Actions workflows (matrix testing, security)
- [ ] 4-domain documentation structure implemented
- [ ] `DOCUMENTATION_STANDARD.md` (700 lines) added
- [ ] `scripts/extract_tests.py` for executable documentation
- [ ] All documentation updated with frontmatter
- [ ] Quality gates passing: `pre-commit run --all-files`
- [ ] Commit: "feat: Week 2 - Adopt development workflow SAPs (10/18)"

### Week 2 Success Criteria

- ✅ Test coverage ≥85% across entire codebase
- ✅ Pre-commit hooks prevent commits that fail quality gates
- ✅ CI/CD runs matrix testing (Python 3.11-3.13)
- ✅ Documentation organized in 4-domain Diátaxis structure
- ✅ DOCUMENTATION_STANDARD.md guides all documentation work
- ✅ Ruff linting 200x faster than previous linter
- ✅ Mypy type checking enforced

---

## Week 3: Developer Experience

**Timeline:** Week of Nov XX, 2025
**Focus:** Development lifecycle, automation scripts, Docker optimization, memory system
**SAPs:** 4 (SAP-012, SAP-008, SAP-011, SAP-010)
**Effort:** ~20 hours
**Status:** 📋 Planned

### Installation

```bash
# Install workflow and tooling SAPs
cd /Users/victorpiper/code/mcp-orchestration
python /tmp/chora-base/scripts/install-sap.py \
  SAP-012 SAP-008 SAP-011 SAP-010 \
  --source /tmp/chora-base
```

### SAPs to Adopt

#### SAP-012: Development Lifecycle
- **Size:** 156 KB
- **Dependencies:** SAP-000
- **Description:** 8-phase lifecycle (Vision → Monitoring) with DDD → BDD → TDD workflow and anti-patterns guide
- **Capabilities:** 8-phase development lifecycle, DDD → BDD → TDD integration, 40-80% defect reduction, sprint/release templates, ANTI_PATTERNS.md (1,309 lines)
- **Time:** 5-6 hours
- **Activities:**
  - Copy `ANTI_PATTERNS.md` (1,309 lines) to `dev-docs/`
  - Document 8-phase lifecycle:
    1. Vision (strategic planning)
    2. Design (DDD - document first)
    3. Specification (BDD - behavioral specs)
    4. Implementation (TDD - test first)
    5. Integration (E2E testing)
    6. Deployment (automation)
    7. Operation (monitoring)
    8. Evolution (iteration)
  - Update `DEVELOPMENT_LIFECYCLE.md` with DDD → BDD → TDD workflow
  - Create sprint/release templates in `docs/dev-docs/workflows/`
  - Document defect reduction metrics (target: 40-80%)
  - Add lifecycle phase checklists
  - Update CONTRIBUTING.md with lifecycle references

#### SAP-008: Automation Scripts
- **Size:** 145 KB
- **Dependencies:** SAP-000, SAP-012
- **Description:** 25 automation scripts (shell + Python) with justfile unified interface and safety contracts
- **Capabilities:** 25 automation scripts, justfile with 30+ commands, idempotent operations, safety contracts, 8 script categories
- **Time:** 6-7 hours
- **Activities:**
  - Review current `justfile` (if exists)
  - Copy SAP-008 `justfile` with 30+ commands:
    - Development: `test`, `lint`, `format`, `type-check`
    - Build: `build`, `install`, `clean`
    - Docker: `docker-build`, `docker-test`, `docker-run`
    - CI: `pre-merge`, `ci-local`, `smoke-test`
    - Release: `release-check`, `bump-version`, `publish`
    - Documentation: `docs-build`, `docs-serve`, `docs-validate`
    - MCP: `mcp-inspector`, `mcp-test`, `mcp-publish`
    - Maintenance: `update-deps`, `security-audit`
  - Copy 25 automation scripts to `scripts/`:
    - 8 categories (build, test, deploy, maintain, validate, generate, analyze, orchestrate)
  - Document safety contracts (idempotent, fail-fast, verbose)
  - Add script usage guide to README
  - Test all justfile commands: `just --list`

#### SAP-011: Docker Operations
- **Size:** 73 KB
- **Dependencies:** SAP-000
- **Description:** Multi-stage Dockerfiles, docker-compose patterns, and container optimization (150-250MB images)
- **Capabilities:** Multi-stage builds, CI-optimized test containers, GitHub Actions cache integration, non-root execution, 81% build context reduction
- **Time:** 4-5 hours
- **Activities:**
  - Review current `Dockerfile` and `docker-compose.yml`
  - Enhance Dockerfile with multi-stage builds:
    - Stage 1: Dependencies (cached)
    - Stage 2: Build
    - Stage 3: Runtime (150-250MB target)
  - Create `Dockerfile.test` for CI-optimized testing
  - Update `.dockerignore` (81% build context reduction)
  - Copy `DOCKER_BEST_PRACTICES.md` to `docker/`
  - Configure non-root execution
  - Add GitHub Actions Docker cache integration
  - Test builds: `just docker-build && just docker-test`
  - Measure image size reduction

#### SAP-010: Memory System (A-MEM)
- **Size:** 87 KB
- **Dependencies:** SAP-000
- **Description:** Agent Memory Architecture with event log, knowledge graph, profiles, and trace correlation
- **Capabilities:** 4 memory types (event, knowledge, profile, trace), Zettelkasten knowledge graph, cross-session learning, event schema v1.0, 30% reduction in repeated mistakes
- **Time:** 4-5 hours (Optional)
- **Activities:**
  - Review current `.chora/memory/` infrastructure
  - Implement 4 memory types:
    1. Event log (JSONL) - `var/telemetry/events.jsonl`
    2. Knowledge graph (Markdown + wikilinks) - `.chora/memory/knowledge/`
    3. Profiles (YAML) - `.chora/memory/profiles/`
    4. Trace correlation - `.chora/memory/traces/`
  - Create `mcp-orchestration-memory` CLI command:
    - `query --type [event-type] --since [time]`
    - `knowledge search --tag [tag]`
    - `knowledge create [title] --content [text] --tag [tag]`
  - Implement Zettelkasten knowledge graph
  - Add event schema v1.0
  - Document memory system usage in AGENTS.md
  - Test memory CLI: `mcp-orchestration-memory --help`

### Week 3 Deliverables

- [ ] 14 SAPs total installed (70 artifacts)
- [ ] `ANTI_PATTERNS.md` (1,309 lines) in `dev-docs/`
- [ ] `DEVELOPMENT_LIFECYCLE.md` with DDD → BDD → TDD workflow
- [ ] `justfile` with 30+ automation commands
- [ ] 25 automation scripts in `scripts/` (8 categories)
- [ ] Multi-stage Dockerfile (150-250MB images)
- [ ] `DOCKER_BEST_PRACTICES.md` in `docker/`
- [ ] Memory system CLI (`mcp-orchestration-memory`) operational
- [ ] 4 memory types implemented (event, knowledge, profile, trace)
- [ ] Commit: "feat: Week 3 - Adopt developer experience SAPs (14/18)"

### Week 3 Success Criteria

- ✅ DDD → BDD → TDD workflow documented and enforced
- ✅ justfile provides unified interface for all automation
- ✅ Docker image size reduced to 150-250MB (multi-stage)
- ✅ 81% build context reduction via `.dockerignore`
- ✅ Memory system enables cross-session agent learning
- ✅ 30% reduction in repeated mistakes (tracked via memory)
- ✅ All automation scripts idempotent and safe

---

## Week 4: MCP-Specific & Metrics

**Timeline:** Week of Nov XX, 2025
**Focus:** MCP server development patterns, metrics tracking, polish
**SAPs:** 4 (SAP-014, SAP-013, SAP-017, SAP-018)
**Effort:** ~22 hours
**Status:** 📋 Planned

### Installation

```bash
# Install technology-specific SAPs
cd /Users/victorpiper/code/mcp-orchestration
python /tmp/chora-base/scripts/install-sap.py \
  SAP-014 SAP-013 \
  --source /tmp/chora-base

# Optional: Install chora-compose integration SAPs (deferred per decision)
# python /tmp/chora-base/scripts/install-sap.py \
#   SAP-017 SAP-018 \
#   --source /tmp/chora-base
```

### SAPs to Adopt

#### SAP-014: MCP Server Development
- **Size:** 234 KB (largest SAP)
- **Dependencies:** SAP-000, SAP-003, SAP-004, SAP-012
- **Description:** FastMCP-based Model Context Protocol server development patterns with 11 templates and 8 guides
- **Capabilities:** FastMCP patterns, 11 MCP templates, tool definition patterns, testing strategies, deployment workflows
- **Time:** 10-12 hours
- **Activities:**
  - Read all SAP-014 artifacts (234 KB total):
    - `capability-charter.md`
    - `protocol-spec.md` (49 KB - largest protocol spec)
    - `awareness-guide.md`
    - `adoption-blueprint.md`
    - `ledger.md`
    - `setup-mcp-ecosystem.md` (additional guide)
    - `mcp_conventions` (6th artifact - MCP-specific conventions)
  - Copy 11 MCP templates to `mcp-templates/`:
    1. Basic tool template
    2. Resource template
    3. Prompt template
    4. Context-aware tool template
    5. Async tool template
    6. Error handling template
    7. Tool with dependencies template
    8. Multi-tool coordinated template
    9. Resource family template
    10. Dynamic resource template
    11. Complete server template
  - Adopt Chora MCP Conventions v1.0:
    - Tool naming: verb-noun format
    - Resource URIs: hierarchical paths
    - Error schemas: structured JSON
    - Testing patterns: pytest + MCP Inspector
  - Review mcp-orchestration tools against SAP-014 patterns
  - Document MCP development workflow
  - Add MCP-specific test patterns
  - Update AGENTS.md with MCP context

#### SAP-013: Metrics Tracking
- **Size:** 94 KB
- **Dependencies:** SAP-000
- **Description:** ClaudeROICalculator, process metrics, sprint velocity tracking with $109k/year savings estimates
- **Capabilities:** Claude ROI calculation, quality/velocity/adherence tracking, research-backed targets, sprint dashboards, $109k/year savings estimate
- **Time:** 4-5 hours
- **Activities:**
  - Copy `utils/claude_metrics.py` (ClaudeROICalculator)
  - Copy `docs/project-docs/PROCESS_METRICS.md`
  - Configure metrics tracking:
    - Quality metrics (test coverage, defect rate, code review findings)
    - Velocity metrics (story points, cycle time, lead time)
    - Adherence metrics (DDD/BDD/TDD compliance)
  - Set research-backed targets:
    - Test coverage: 85%+
    - Defect density: <0.5/KLOC
    - Code review coverage: 100%
    - CI/CD success rate: >95%
  - Create sprint dashboard template
  - Document ROI calculation methodology
  - Run initial metrics: `python utils/claude_metrics.py --report`

#### SAP-017: Chora-Compose Integration (Deferred)
- **Size:** 108 KB
- **Dependencies:** SAP-003
- **Description:** How to adopt chora-compose for content generation (pip, MCP, CLI) with role-based usage patterns
- **Status:** ⏸️ Deferred (install but don't prioritize adoption)
- **Time:** 2-3 hours (if adopted)
- **Activities:** Install SAP but defer detailed adoption per decision

#### SAP-018: Chora-Compose Meta Package (Deferred)
- **Size:** 187 KB
- **Dependencies:** SAP-017
- **Description:** Complete chora-compose architecture specification: 17 tools + 5 resources + 4 modalities
- **Status:** ⏸️ Deferred (install but don't prioritize adoption)
- **Time:** 2-3 hours (if adopted)
- **Activities:** Install SAP but defer detailed adoption per decision

### Additional Week 4 Activities

#### Polish & Integration (4-5 hours)
- Run comprehensive validation:
  - `just test` - All tests passing, 85%+ coverage
  - `just lint` - All linting passing
  - `pre-commit run --all-files` - All hooks passing
  - `scripts/validate-links.sh` - No broken links
- Update all AGENTS.md files with SAP references
- Update CLAUDE.md with full chora-base integration notes
- Review all 18 SAP ledgers and update adoption status
- Create `.chorabase` file with final configuration
- Generate adoption completion report
- Update PROJECT_OVERVIEW.md with chora-base integration
- Prepare adoption retrospective

### Week 4 Deliverables

- [ ] 18 SAPs total installed (90+ artifacts) ✅ **100% ADOPTION**
- [ ] 11 MCP templates in `mcp-templates/`
- [ ] Chora MCP Conventions v1.0 adopted
- [ ] `utils/claude_metrics.py` (ClaudeROICalculator) operational
- [ ] `PROCESS_METRICS.md` with sprint dashboard
- [ ] All quality gates passing
- [ ] All documentation links validated
- [ ] `.chorabase` file with final v4.1.0 configuration
- [ ] Adoption completion report
- [ ] Commit: "feat: Week 4 - Complete chora-base adoption (18/18, 100%)"

### Week 4 Success Criteria

- ✅ All 18 SAPs installed and adopted
- ✅ MCP server patterns documented (234 KB SAP-014)
- ✅ 11 MCP templates available for future development
- ✅ Chora MCP Conventions v1.0 compliance
- ✅ ROI metrics tracking operational
- ✅ Sprint velocity dashboard created
- ✅ All tests passing (85%+ coverage)
- ✅ All linting passing
- ✅ All pre-commit hooks passing
- ✅ Zero broken documentation links
- ✅ 100% chora-base v4.1.0 adoption achieved

---

## Complete SAP Catalog Reference

### All 18 SAPs with Metadata

| SAP | Name | Size | Dependencies | Phase | Priority | Status |
|-----|------|------|--------------|-------|----------|--------|
| SAP-000 | SAP Framework | 125 KB | None | Phase 1 | P0 | Active |
| SAP-001 | Inbox Coordination | 45 KB | None | Phase 1 | P0 | Pilot ⚠️ |
| SAP-002 | Chora-Base Meta | 78 KB | SAP-000 | Phase 1 | P0 | Active |
| SAP-003 | Project Bootstrap | 92 KB | SAP-000 | Phase 2 | P0 | Active |
| SAP-004 | Testing Framework | 89 KB | SAP-000, SAP-003 | Phase 2 | P0 | Active |
| SAP-005 | CI/CD Workflows | 67 KB | SAP-000, SAP-004 | Phase 2 | P0 | Active |
| SAP-006 | Quality Gates | 54 KB | SAP-000, SAP-004 | Phase 2 | P0 | Active |
| SAP-007 | Documentation Framework | 112 KB | SAP-000 | Phase 3 | P1 | Active |
| SAP-008 | Automation Scripts | 145 KB | SAP-000, SAP-012 | Phase 3 | P1 | Active |
| SAP-009 | Agent Awareness | 98 KB | SAP-000, SAP-007 | Phase 3 | P1 | Active |
| SAP-010 | Memory System (A-MEM) | 87 KB | SAP-000 | Phase 3 | P1 | Active |
| SAP-011 | Docker Operations | 73 KB | SAP-000 | Phase 3 | P1 | Active |
| SAP-012 | Development Lifecycle | 156 KB | SAP-000 | Phase 3 | P1 | Active |
| SAP-013 | Metrics Tracking | 94 KB | SAP-000 | Phase 4 | P2 | Active |
| SAP-014 | MCP Server Development | 234 KB | SAP-000, SAP-003, SAP-004, SAP-012 | Wave 3 | P1 | Active |
| SAP-015 | Reserved | 0 KB | N/A | N/A | N/A | Reserved |
| SAP-016 | Link Validation | 62 KB | None | Wave 2 | P0 | Active |
| SAP-017 | Chora-Compose Integration | 108 KB | SAP-003 | Wave 3 | P1 | Active |
| SAP-018 | Chora-Compose Meta | 187 KB | SAP-017 | Wave 3 | P1 | Active |

**Total Size:** ~1.8 MB of documentation
**Total Artifacts:** 90+ files (5 per SAP × 18 SAPs)
**Active SAPs:** 17
**Pilot SAPs:** 1 (SAP-001)
**Reserved SAPs:** 1 (SAP-015)

### SAP Dependency Graph

```
Foundational (no dependencies):
  - SAP-000 (SAP Framework)
  - SAP-001 (Inbox Coordination) [PILOT]
  - SAP-016 (Link Validation)

Core Infrastructure (depends on SAP-000):
  - SAP-002 (Chora-Base Meta) → SAP-000
  - SAP-003 (Project Bootstrap) → SAP-000
  - SAP-007 (Documentation) → SAP-000
  - SAP-010 (Memory System) → SAP-000
  - SAP-011 (Docker Operations) → SAP-000
  - SAP-012 (Development Lifecycle) → SAP-000
  - SAP-013 (Metrics Tracking) → SAP-000

Testing & Quality (depends on SAP-003, SAP-004):
  - SAP-004 (Testing) → SAP-000, SAP-003
  - SAP-005 (CI/CD) → SAP-000, SAP-004
  - SAP-006 (Quality Gates) → SAP-000, SAP-004

Advanced Features (multiple dependencies):
  - SAP-008 (Automation) → SAP-000, SAP-012
  - SAP-009 (Agent Awareness) → SAP-000, SAP-007
  - SAP-014 (MCP Server) → SAP-000, SAP-003, SAP-004, SAP-012
  - SAP-017 (Chora-Compose Integration) → SAP-003
  - SAP-018 (Chora-Compose Meta) → SAP-017
```

---

## Dependencies & Prerequisites

### System Requirements

| Requirement | Version | Status | Notes |
|-------------|---------|--------|-------|
| Python | 3.11+ | ✅ | mcp-orchestration uses 3.11+ |
| Git | 2.0+ | ✅ | Repository initialized |
| chora-base | v4.1.0 | ⬜ | Clone to `/tmp/chora-base` |
| GitHub CLI | latest | ⬜ | Optional for `gh` commands |
| Docker | 20.10+ | ✅ | For Docker SAPs |
| pytest | latest | ✅ | For testing SAPs |
| pre-commit | latest | ⬜ | For quality gate SAPs |

### Repository Access

| Resource | Location | Status | Required By |
|----------|----------|--------|-------------|
| chora-base repo | `https://github.com/liminalcommons/chora-base.git` | ⬜ | Week 1 |
| chora-base v4.1.0 tag | `git checkout v4.1.0` | ⬜ | Week 1 |
| SAP installation script | `/tmp/chora-base/scripts/install-sap.py` | ⬜ | Week 1 |
| SAP catalog | `/tmp/chora-base/sap-catalog.json` | ⬜ | Week 1 |

### Installation Prerequisites

**Week 1 Setup:**
```bash
# Verify Python version
python --version  # Should be 3.11+

# Clone chora-base v4.1.0
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base
cd /tmp/chora-base
git checkout v4.1.0

# Verify installation script
ls scripts/install-sap.py  # Should exist

# Verify SAP catalog
cat sap-catalog.json  # Should show 18 SAPs

# List available SAP sets
python scripts/install-sap.py --list-sets

# List all SAPs
python scripts/install-sap.py --list
```

**Week 2+ Prerequisites:**
- Week 1 completion (5 SAPs installed)
- All Week 1 success criteria met
- Git repository clean (no uncommitted changes)

---

## Success Metrics

### Adoption Completion Metrics

| Metric | Baseline | Target | Tracking Method |
|--------|----------|--------|-----------------|
| SAPs Installed | 0/18 | 18/18 | `ls docs/skilled-awareness/` |
| SAP Artifacts | 0 | 90+ | `find docs/skilled-awareness -name "*.md" \| wc -l` |
| Test Coverage | Current | 85%+ | `pytest --cov=src --cov-report=term` |
| Documentation Links | Unknown | 100% valid | `scripts/validate-links.sh` |
| Pre-commit Hooks | 0 | 7 | `.pre-commit-config.yaml` |
| Justfile Commands | 0 | 30+ | `just --list` |
| Docker Image Size | Current | 150-250MB | `docker images \| grep mcp-orchestration` |
| MCP Templates | 0 | 11 | `ls mcp-templates/` |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Coverage | ≥85% | `pytest --cov=src --cov-fail-under=85` |
| Lint Pass Rate | 100% | `ruff check src/ tests/` |
| Type Check Pass Rate | 100% | `mypy src/` |
| CI/CD Success Rate | >95% | GitHub Actions dashboard |
| Documentation Links | 0 broken | `scripts/validate-links.sh` |
| Pre-commit Success | 100% | `pre-commit run --all-files` |

### Adoption Depth Metrics

Use SAP-019 self-evaluation (if available) to measure adoption depth:

```bash
# Quick adoption assessment
python /tmp/chora-base/scripts/sap-evaluator.py --quick

# Deep assessment for specific SAP
python /tmp/chora-base/scripts/sap-evaluator.py \
  --deep SAP-009 \
  --output docs/adoption-reports/SAP-009-assessment.md
```

**Target:** 100% adoption depth for all 18 SAPs

---

## Risks & Mitigations

### High-Priority Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SAP-001 Pilot changes | Medium | Medium | Monitor chora-base releases; update if SAP-001 stabilizes |
| Documentation reorganization breaks links | High | Medium | Run `scripts/validate-links.sh` after every change |
| 85% coverage threshold too aggressive | Medium | High | Start at current coverage, incrementally improve weekly |
| Multi-stage Docker breaks existing deployment | Low | High | Test Docker builds on feature branch before merging |
| Pre-commit hooks slow down development | Low | Low | Optimize hooks; allow `--no-verify` for WIP commits |
| justfile conflicts with existing automation | Low | Medium | Review existing scripts; integrate or migrate gradually |

### Medium-Priority Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Week 1 takes longer than 15 hours | Medium | Low | Buffer 20% extra time; defer SAP-002 if needed |
| Chora-base v4.1.0 has breaking changes | Low | Medium | Review CHANGELOG; test installation on feature branch |
| SAP dependencies not auto-resolved | Low | Medium | Manually install dependencies in correct order |
| Memory system CLI implementation complex | Medium | Medium | Start with basic functionality; iterate incrementally |

### Low-Priority Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SAP documentation unclear | Low | Low | Reference chora-base examples; ask in community |
| Git merge conflicts during adoption | Low | Low | Commit after each week; use feature branches |
| CI/CD resource limits exceeded | Low | Low | Optimize workflows; use caching |

### Risk Monitoring

**Weekly Risk Review:**
- Review risks at end of each week
- Update probability/impact based on actual experience
- Add new risks as discovered
- Document mitigations that worked

---

## Rollback Plan

### Per-Week Rollback Strategy

#### Week 1 Rollback
```bash
# If adoption fails, remove installed SAPs
rm -rf docs/skilled-awareness/
git checkout .chorabase AGENTS.md CLAUDE.md inbox/schemas/
git checkout scripts/validate-links.sh
git restore .github/workflows/*  # If link validation added

# Revert commit
git reset --hard HEAD~1
```

#### Week 2 Rollback
```bash
# Remove Week 2 SAPs only
rm -rf docs/skilled-awareness/project-bootstrap/
rm -rf docs/skilled-awareness/testing-framework/
rm -rf docs/skilled-awareness/ci-cd-workflows/
rm -rf docs/skilled-awareness/quality-gates/
rm -rf docs/skilled-awareness/documentation-framework/

# Restore previous configurations
git checkout pyproject.toml .coveragerc .pre-commit-config.yaml
git restore .github/workflows/*
git checkout DOCUMENTATION_STANDARD.md

# Revert Week 2 commit
git reset --hard HEAD~1
```

#### Week 3 Rollback
```bash
# Remove Week 3 SAPs
rm -rf docs/skilled-awareness/{development-lifecycle,automation-scripts,docker-operations,memory-system}/

# Restore configurations
git checkout dev-docs/ANTI_PATTERNS.md
git checkout DEVELOPMENT_LIFECYCLE.md
git checkout justfile
git checkout Dockerfile docker-compose.yml
git restore scripts/*

# Revert Week 3 commit
git reset --hard HEAD~1
```

#### Week 4 Rollback
```bash
# Remove Week 4 SAPs
rm -rf docs/skilled-awareness/{mcp-server-development,metrics-tracking}/

# Restore configurations
git restore mcp-templates/
git checkout utils/claude_metrics.py
git checkout docs/project-docs/PROCESS_METRICS.md

# Revert Week 4 commit
git reset --hard HEAD~1
```

### Complete Rollback

If full rollback needed (all 4 weeks):

```bash
# Nuclear option: revert all adoption changes
git log --oneline | grep "chora-base"  # Find adoption commits
git revert <commit-hash-week-4>
git revert <commit-hash-week-3>
git revert <commit-hash-week-2>
git revert <commit-hash-week-1>

# Or reset to pre-adoption state
git reset --hard <pre-adoption-commit-hash>

# Remove all SAP artifacts
rm -rf docs/skilled-awareness/
```

### Partial Adoption Strategy

If full adoption not feasible:

1. **Keep minimal-entry (Week 1)** - Core value with minimal effort
2. **Add selective SAPs from Week 2-4** - Choose high-value SAPs only
3. **Document partial adoption** - Update `.chorabase` with adopted SAPs
4. **Defer remaining SAPs** - Plan future adoption waves

---

## Communication Plan

### Stakeholders

| Stakeholder | Role | Update Frequency | Method |
|-------------|------|------------------|--------|
| mcp-orchestration maintainers | Owners | Weekly | Git commits + this document |
| mcp-orchestration contributors | Users | Bi-weekly | README updates + CHANGELOG |
| chora-base team | Upstream | On completion | Coordination request in inbox/ |
| Ecosystem partners | Collaborators | On completion | Ecosystem broadcast |

### Update Schedule

**Weekly Updates:**
- Update this document with progress (Status Tracker section)
- Commit adoption changes with descriptive messages
- Update `.chorabase` file with newly adopted SAPs

**Bi-Weekly Updates:**
- Update PROJECT_OVERVIEW.md with adoption status
- Update README.md with new capabilities
- Update CHANGELOG.md with adoption milestones

**On Completion:**
- Create `CHORA_BASE_ADOPTION_COMPLETE.md` retrospective
- Submit coordination request to chora-base via inbox/
- Broadcast completion to ecosystem partners
- Update all AGENTS.md files with final SAP references

---

## Status Tracker

### Weekly Progress

| Week | Timeline | SAPs | Status | Started | Completed | Notes |
|------|----------|------|--------|---------|-----------|-------|
| 1 | Oct 31 | 6 | ✅ Complete | 2025-10-31 | 2025-10-31 | Foundation (5+1 dependency: SAP-007) |
| 2 | Nov XX-XX | 5 | 📋 Planned | - | - | Development Workflow |
| 3 | Dec XX-XX | 4 | 📋 Planned | - | - | Developer Experience |
| 4 | Dec XX-XX | 4 | 📋 Planned | - | - | MCP-Specific & Metrics |

**Overall Status:** 🚧 In Progress (6/18 SAPs, 33.3%)

### SAP Installation Tracker

| SAP | Name | Week | Status | Installed | Adopted | Notes |
|-----|------|------|--------|-----------|---------|-------|
| SAP-000 | SAP Framework | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | Core protocol |
| SAP-001 | Inbox Coordination | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | Pilot status ⚠️, schemas created |
| SAP-002 | Chora-Base Meta | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | .chorabase file created |
| SAP-007 | Documentation Framework | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | Dependency of SAP-009 |
| SAP-009 | Agent Awareness | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | AGENTS.md enhanced |
| SAP-016 | Link Validation | 1 | ✅ Complete | 2025-10-31 | 2025-10-31 | Script installed, 20+ broken links identified |
| SAP-003 | Project Bootstrap | 2 | 📋 Planned | - | - | Already generated |
| SAP-004 | Testing Framework | 2 | 📋 Planned | - | - | 85%+ coverage |
| SAP-005 | CI/CD Workflows | 2 | 📋 Planned | - | - | Matrix testing |
| SAP-006 | Quality Gates | 2 | 📋 Planned | - | - | Pre-commit hooks |
| SAP-012 | Development Lifecycle | 3 | 📋 Planned | - | - | DDD→BDD→TDD |
| SAP-008 | Automation Scripts | 3 | 📋 Planned | - | - | justfile + 25 scripts |
| SAP-011 | Docker Operations | 3 | 📋 Planned | - | - | Multi-stage builds |
| SAP-010 | Memory System | 3 | 📋 Planned | - | - | A-MEM (optional) |
| SAP-014 | MCP Server Development | 4 | 📋 Planned | - | - | 234KB, 11 templates |
| SAP-013 | Metrics Tracking | 4 | 📋 Planned | - | - | ROI calculator |
| SAP-017 | Chora-Compose Integration | 4 | ⏸️ Deferred | - | - | Install but defer |
| SAP-018 | Chora-Compose Meta | 4 | ⏸️ Deferred | - | - | Install but defer |

**Legend:**
- 📋 Planned - Not yet started
- 🚧 In Progress - Currently working on
- ✅ Complete - Installed and adopted
- ⏸️ Deferred - Installed but adoption deferred
- ❌ Blocked - Cannot proceed (with reason)

---

## Resources

### Chora-Base Resources

- **Repository:** https://github.com/liminalcommons/chora-base
- **Version:** v4.1.0 (2025-10-30)
- **SAP Catalog:** `/tmp/chora-base/sap-catalog.json`
- **Installation Script:** `/tmp/chora-base/scripts/install-sap.py`
- **Quickstart Guide:** `inbox/incoming/coordination/quickstart-claude.md`

### Documentation

- **PROJECT_OVERVIEW.md** - Strategic overview
- **AGENTS.md** - Machine-readable project instructions
- **CLAUDE.md** - Claude-specific optimization guide
- **DEVELOPMENT_LIFECYCLE.md** - Development process
- **DOCUMENTATION_STANDARD.md** - Documentation guidelines (post-Week 2)

### SAP Documentation

Once installed, SAPs will be in:
- `docs/skilled-awareness/sap-framework/` (SAP-000)
- `docs/skilled-awareness/inbox/` (SAP-001)
- `docs/skilled-awareness/chora-base/` (SAP-002)
- ... (15 more SAPs)

Each SAP contains 5 artifacts:
1. `capability-charter.md` - Problem, scope, outcomes
2. `protocol-spec.md` - Technical contract, interfaces
3. `awareness-guide.md` - How to work with capability (AI agent focus)
4. `adoption-blueprint.md` - Step-by-step installation
5. `ledger.md` - Adopters, versions, status

### Useful Commands

```bash
# List all SAPs in catalog
python /tmp/chora-base/scripts/install-sap.py --list

# List available SAP sets
python /tmp/chora-base/scripts/install-sap.py --list-sets

# Dry-run installation (preview)
python /tmp/chora-base/scripts/install-sap.py --set minimal-entry \
  --source /tmp/chora-base \
  --dry-run

# Install SAP set
python /tmp/chora-base/scripts/install-sap.py --set minimal-entry \
  --source /tmp/chora-base

# Install individual SAPs
python /tmp/chora-base/scripts/install-sap.py SAP-004 SAP-005 \
  --source /tmp/chora-base

# Validate installation
ls docs/skilled-awareness/*/capability-charter.md

# Run tests with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=85

# Run link validation
scripts/validate-links.sh

# Run pre-commit hooks
pre-commit run --all-files

# List justfile commands
just --list

# Quick adoption assessment
python /tmp/chora-base/scripts/sap-evaluator.py --quick
```

---

## Appendix: Decision Log

### Key Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| Full SAP catalog (18 SAPs) | User requested 100% adoption (Option C) | 2025-10-31 |
| 4-week incremental approach | Manageable weekly chunks, reduces risk (Option A) | 2025-10-31 |
| GitHub access via clone | Use `git clone` and `gh` CLI (Option 2) | 2025-10-31 |
| Defer ecosystem participation | Decide later after SAPs installed (Option C) | 2025-10-31 |
| Defer chora-compose v1.9.0 | Install SAP-017/018 but don't prioritize (Option B) | 2025-10-31 |
| Document as Adoption Plan | Not a Wave Plan (4 weeks too long) | 2025-10-31 |
| Location: `project-docs/` | Consistent with planning document convention | 2025-10-31 |
| UPPERCASE filename | Follows `WAVE_1X_PLAN.md` pattern | 2025-10-31 |

### Alternative Approaches Considered

1. **Minimal-entry only (5 SAPs)** - Rejected: User wants 100%
2. **All-at-once installation** - Rejected: High risk, prefer incremental
3. **Manual SAP installation** - Rejected: `install-sap.py` more reliable
4. **Skip SAP-001 (Pilot status)** - Rejected: Part of minimal-entry set
5. **Start with Week 2 (skip foundation)** - Rejected: SAPs have dependencies

---

## Next Steps

### Immediate Actions (Before Week 1)

1. ✅ **Create this adoption plan document** - COMPLETE
2. ⬜ Review plan with stakeholders
3. ⬜ Set start date for Week 1
4. ⬜ Clone chora-base v4.1.0 to `/tmp/chora-base`
5. ⬜ Run dry-run installation: `python /tmp/chora-base/scripts/install-sap.py --set minimal-entry --dry-run`
6. ⬜ Verify prerequisites (Python 3.11+, Git, Docker)
7. ⬜ Create feature branch: `git checkout -b feat/chora-base-adoption`

### Week 1 Kickoff

8. ⬜ Update Status Tracker: Set Week 1 status to 🚧 In Progress
9. ⬜ Run Week 1 installation commands
10. ⬜ Follow Week 1 adoption activities
11. ⬜ Track progress in this document
12. ⬜ Commit at end of Week 1: "feat: Week 1 - Adopt chora-base minimal-entry SAPs (5/18)"

---

## Document Status

**Status:** 📋 Planning
**Created:** 2025-10-31
**Last Updated:** 2025-10-31
**Next Review:** Start of Week 1
**Approval Status:** Pending stakeholder review
**Version:** 1.0.0
**Document Type:** Living document (update weekly during adoption)

---

**Questions or Issues?**
- Open issue in mcp-orchestration repository
- Reference this adoption plan: `project-docs/CHORA_BASE_ADOPTION_PLAN.md`
- Tag with: `chora-base`, `adoption`, `documentation`

**End of Adoption Plan**
