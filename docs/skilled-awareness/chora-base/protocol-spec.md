# Protocol Specification: chora-base Template Repository

**SAP ID**: SAP-002
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Last Updated**: 2025-10-28

---

## 1. Overview

This protocol defines the **technical architecture** of chora-base: a Python project template for AI-agent-first development.

**Core Guarantee**: chora-base generates production-ready Python projects with comprehensive documentation, quality gates, and AI agent support. All capabilities are packagedas SAPs with clear contracts.

**Version**: 3.3.0 (current), targeting Python 3.11+

---

## 2. Architecture

### 2.1 Repository Structure

```
chora-base/
├── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  # Root SAP protocol
├── setup.py                    # Project generator (blueprint-based)
├── blueprints/                 # Jinja2 templates for generated files
├── static-template/            # Ready-to-copy scaffolding
├── docs/reference/skilled-awareness/  # All SAPs (14 capabilities)
├── inbox/                      # Inbox coordination (SAP-001)
├── claude/                     # Claude-specific patterns
├── examples/                   # Example generated projects
├── README.md                   # Project overview
├── AGENTS.md                   # Agent guidance
├── CHANGELOG.md                # Version history
└── CLAUDE_SETUP_GUIDE.md       # Claude setup guide
```

### 2.2 Generation Architecture

**Blueprint-Based Generation**:
```
User Request
    ↓
setup.py (generator)
    ↓
1. Collect inputs (project name, author, options)
2. Copy static-template/ → target directory
3. Process blueprints/ with Jinja2 (variable substitution)
4. Rename directories (src/__package_name__/ → src/{name}/)
5. Initialize git repository
    ↓
Generated Project (production-ready)
```

**Not Copier**: chora-base v3.0+ uses custom `setup.py` for zero dependencies.

---

## 3. Capabilities (14 Total)

### 3.1 Meta & Foundational (3 capabilities)

#### SAP-000: sap-framework
**Status**: Draft (Phase 1, complete)
**Location**: [sap-framework/](../sap-framework/)

**Purpose**: Meta-capability defining how SAPs work

**Includes**:
- Root protocol (SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- 5-artifact structure (Charter, Protocol, Awareness, Blueprint, Ledger)
- Blueprint-based installation
- Integration with DDD → BDD → TDD
- Scope levels (Vision & Strategy, Planning, Implementation)

**Interfaces**:
- Document templates: [document-templates.md](../document-templates.md)
- SAP Index: [INDEX.md](../INDEX.md)

**Guarantees**:
- All SAPs follow same structure
- Blueprints are agent-executable
- Sequential upgrades supported

#### SAP-001: inbox-coordination
**Status**: Pilot (Phase 1)
**Location**: [inbox/](../inbox/)

**Purpose**: Cross-repo coordination, capability registry, broadcast workflow

**Includes**:
- `inbox/` directory structure
- JSON schemas (coordination-request, broadcast, capability)
- `coordination/CAPABILITIES/` registry
- `ECOSYSTEM_STATUS.yaml` dashboard
- Examples (health-monitoring-w3)

**Interfaces**:
- Coordination request format: `inbox/schemas/coordination-request.json`
- Broadcast format: `inbox/schemas/broadcast.json`
- CLI: Bash commands for inbox management

**Guarantees**:
- Coordination requests triaged (this_sprint, next_sprint, backlog)
- Weekly broadcast cadence
- Trace IDs for multi-step workflows

#### SAP-002: chora-base-meta
**Status**: Draft (Phase 1, this SAP)
**Location**: [chora-base/](../chora-base/)

**Purpose**: chora-base describes itself (dogfooding)

**Includes**:
- This charter, protocol, awareness, blueprint, ledger
- Comprehensive overview of all 14 capabilities
- Agent workflows for template generation, upgrade

**Interfaces**:
- Entry point: This protocol spec
- Agent workflows: [awareness-guide.md](awareness-guide.md)
- Adoption: [adoption-blueprint.md](adoption-blueprint.md)

**Guarantees**:
- Single source of truth for chora-base
- All 14 capabilities documented
- Aligned with current version (v3.3.0)

---

### 3.2 Core Infrastructure (4 capabilities)

#### SAP-003: project-bootstrap
**Status**: Draft (Phase 2) ✅ Complete
**Location**: [project-bootstrap/](../project-bootstrap/)
**Priority**: P0 (critical)

**Purpose**: Blueprint generation, static-template scaffolding, `setup.py` workflow

**Includes**:
- `setup.py` (443 lines, generation orchestrator)
- `blueprints/` directory (12 templates)
- `static-template/` structure (100+ files)
- Generation workflow (copy → rename → process → init → validate)

**Interfaces**:
- **CLI**: `python setup.py <project-name> [options]`
- **Input**: Project name, author, email, Python version
- **Output**: Generated project in `<project-name>/` directory

**Guarantees**:
- Zero-dependency generation (no Copier/Cookiecutter)
- All critical files exist (validated)
- No unreplaced {{ placeholders }}
- Tests loadable (pytest --collect-only)
- Git repository initialized
- Generated project follows chora-base conventions
- Idempotent (safe to re-run with `--force`)

**Current Adopter Pain**: "Hard to reason about guarantees, versioning, and upgrade paths"

#### SAP-004: testing-framework
**Status**: Draft (Phase 2) ✅ Complete
**Location**: [testing-framework/](../testing-framework/)
**Priority**: P0 (critical)

**Purpose**: pytest, coverage, fixtures, test patterns

**Includes**:
- `static-template/tests/` structure
- `pyproject.toml` pytest config (pytest 8.3.0, pytest-asyncio 0.24.0, pytest-cov 6.0.0)
- Test patterns: basic, parametrized, async, fixture, mock, error testing

**Interfaces**:
- **CLI**: `pytest` (run all tests)
- **CLI**: `pytest --cov=src --cov-report=term-missing` (coverage report)
- **Config**: `pyproject.toml` [tool.pytest.ini_options]

**Guarantees**:
- Coverage ≥85% enforced (industry best practice, based on research)
- Async tests supported (pytest-asyncio auto mode)
- 6 test patterns documented
- Tests isolated (no side effects)
- Fast test execution (<60s for development workflow)

#### SAP-005: ci-cd-workflows
**Status**: Draft (Phase 2) ✅ Complete
**Location**: [ci-cd-workflows/](../ci-cd-workflows/)
**Priority**: P0 (critical)

**Purpose**: GitHub Actions (test, lint, release, security, docs-quality)

**Includes**:
- `static-template/.github/workflows/` (10 workflow files)
- Core: test.yml (matrix Python 3.11-3.13), lint.yml (ruff + mypy), smoke.yml
- Security: codeql.yml, dependency-review.yml, dependabot-automerge.yml
- Docs: docs-quality.yml
- Release: release.yml

**Interfaces**:
- **Triggers**: push, pull_request, release, schedule
- **Best Practices**: Matrix testing, pip caching, parallel execution, security-first
- **Outputs**: Test results, coverage reports, release artifacts

**Guarantees**:
- Tests run on all PRs (Python 3.11, 3.12, 3.13)
- Coverage ≥85% enforced in CI
- Security scans on every PR (CodeQL, dependency review)
- Releases automated (tag → build → publish to PyPI)
- Total CI time <5 minutes (parallel execution)

#### SAP-006: quality-gates
**Status**: Draft (Phase 2) ✅ Complete
**Location**: [quality-gates/](../quality-gates/)
**Priority**: P0 (critical)

**Purpose**: pre-commit hooks, linting, type checking, coverage enforcement

**Includes**:
- `.pre-commit-config.yaml` (3 repos, 7 hooks)
- Hooks: check-yaml, end-of-file-fixer, trailing-whitespace, check-added-large-files, ruff (check), ruff-format, mypy
- Quality standards in `pyproject.toml` (ruff rules: E, F, I, N, W, UP)

**Interfaces**:
- **CLI**: `pre-commit run --all-files` (manual run)
- **Git hook**: Automatic on `git commit`
- **Config**: `.pre-commit-config.yaml`, `pyproject.toml` [tool.ruff], [tool.mypy]

**Guarantees**:
- All commits pass quality checks (7 hooks)
- Ruff-based (200x faster than flake8+isort+black)
- Correct hook order (ruff-check before ruff-format, critical)
- Mypy strict mode (disallow_untyped_defs)
- Total hook execution time <5 seconds

---

### 3.3 Developer Experience (3 capabilities)

#### SAP-007: documentation-framework
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [documentation-framework/](../documentation-framework/)
**Priority**: P1 (high value)

**Purpose**: Diataxis structure, frontmatter schema, executable How-Tos, test extraction

**Includes**:
- `static-template/DOCUMENTATION_STANDARD.md` (~700 lines)
- Diataxis directories: `user-docs/`, `dev-docs/`, `project-docs/`
- Subdirectories: `tutorials/`, `how-to/`, `reference/`, `explanation/`
- Frontmatter schema (YAML metadata with 8 fields)
- Test extraction (`scripts/extract_tests.py` ~400 lines)

**Interfaces**:
- **Diataxis Structure**: 4 document types (tutorial, how-to, reference, explanation)
- **Frontmatter**: YAML with title, type, status, audience, last_updated, version, tags, test_extraction, related
- **Test Extraction**: `python scripts/extract_tests.py --input <how-to> --output <test>`
- **Validation**: `python scripts/validate_docs.py --check-frontmatter --check-links`

**Guarantees**:
- All docs follow Diataxis organization (4 types by user intent)
- Frontmatter validated (required fields present, enum values correct)
- Executable How-Tos generate pytest tests (test_extraction: true)
- Test extraction automated (scripts/extract_tests.py)
- Documentation stays synchronized with code (DDD → BDD → TDD)

#### SAP-008: automation-scripts
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [automation-scripts/](../automation-scripts/)
**Priority**: P1 (high value)

**Purpose**: `scripts/` directory (25 scripts), justfile tasks (30+ commands), release automation

**Includes**:
- `static-template/scripts/` (25 shell + Python scripts, 8 categories)
- `static-template/justfile` (~150 lines, 30+ commands)
- **Category 1**: Setup & Environment (setup.sh, venv-create.sh, venv-clean.sh, check-env.sh)
- **Category 2**: Development (dev-server.sh, smoke-test.sh, integration-test.sh, diagnose.sh)
- **Category 3**: Version Management (bump-version.sh, prepare-release.sh)
- **Category 4**: Release & Publishing (build-dist.sh, publish-test.sh, publish-prod.sh, verify-stable.sh)
- **Category 5**: Safety & Recovery (rollback-dev.sh, pre-merge.sh)
- **Category 6**: Documentation (validate_docs.py, extract_tests.py, docs_metrics.py, generate_docs_map.py, query_docs.py)
- **Category 7**: MCP & Specialized (mcp-tool.sh, validate_mcp_names.py)
- **Category 8**: Migration & Handoff (migrate_namespace.sh, handoff.sh)

**Interfaces**:
- **CLI** (primary): `just <task>` (e.g., `just test`, `just pre-merge`, `just bump-patch`)
- **Scripts** (direct): `./scripts/<script>.sh` (discouraged, use justfile)
- **Python**: `python scripts/<script>.py --help` (utility scripts)

**Guarantees**:
- All scripts idempotent (check-before-act, cleanup-before-create patterns)
- All scripts have safety flags (`set -euo pipefail` for bash)
- All scripts document purpose (header comments: usage, safety, rollback)
- Error handling standardized (clear messages, non-zero exit codes)
- Rollback mechanisms for destructive operations
- Justfile provides unified interface (90% adoption target)
- Validation standards enforced (8 checks per script)

#### SAP-009: agent-awareness
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [agent-awareness/](../agent-awareness/)
**Priority**: P1 (high value)

**Purpose**: AGENTS.md/CLAUDE.md patterns, nested awareness files

**Includes**:
- `blueprints/AGENTS.md.blueprint` (~900 lines, generic agent guidance)
- `blueprints/CLAUDE.md.blueprint` (~450 lines, Claude-specific optimizations)
- Nested patterns: `static-template/tests/AGENTS.md` (~250 lines), `static-template/scripts/AGENTS.md` (~200 lines), `static-template/docker/AGENTS.md` (~200 lines), `static-template/.chora/memory/AGENTS.md` (~300 lines)
- Pattern library: `claude/` (CONTEXT_MANAGEMENT, CHECKPOINT_PATTERNS, METRICS_TRACKING, FRAMEWORK_TEMPLATES)

**Interfaces**:
- **AGENTS.md**: Generic agent entry point (9 sections: overview, process, structure, concepts, tasks, testing, PRs, troubleshooting)
- **CLAUDE.md**: Claude-specific entry point (7 sections: quick start, capabilities matrix, context management, artifacts, checkpoints, token budgets, ROI tracking)
- **Nested Files**: "Nearest File Wins" - agents read closest awareness file
- **Progressive Context Loading**: Phase 1 (0-10k), Phase 2 (10-50k), Phase 3 (50-200k)

**Guarantees**:
- AGENTS.md in every generated project (root + 4 nested)
- CLAUDE.md optional (if Claude features enabled, root + 4 nested)
- Dual-file pattern consistent (AGENTS = generic, CLAUDE = optimizations)
- Context optimization (token budgets by task: feature 15-30k, bug 5-10k, refactor 20-40k)
- Checkpoint patterns every 5-10 interactions (Claude)
- "Nearest File Wins" navigation supported

#### SAP-010: memory-system (A-MEM)
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [memory-system/](../memory-system/)
**Priority**: P1 (high value)

**Purpose**: `.chora/memory/` structure, event log, knowledge graph, agent profiles, cross-session learning

**Includes**:
- `static-template/.chora/memory/README.md` (~300 lines, A-MEM architecture)
- `static-template/.chora/memory/AGENTS.md` (~200 lines, generic memory guidance)
- `static-template/.chora/memory/CLAUDE.md` (~150 lines, Claude-specific memory usage)
- **Event Log**: `events/` (append-only JSONL, monthly partitions, per-trace files)
- **Knowledge Graph**: `knowledge/` (Markdown notes with YAML frontmatter, Zettelkasten methodology)
- **Agent Profiles**: `profiles/` (JSON per agent: capabilities, preferences, learned patterns)
- **Queries**: `queries/` (SQL/scripts for common patterns)

**Interfaces**:
- **Event Emission**: `emit_event(event_type, trace_id, status, metadata)` → `.chora/memory/events/<month>/events.jsonl`
- **Event Schema**: Chora ecosystem event schema v1.0 (timestamp, trace_id, status, schema_version, event_type, source, metadata)
- **Knowledge Notes**: Markdown with YAML frontmatter (id, created, updated, tags, confidence, source, linked_to, status, author, related_traces)
- **Agent Profiles**: JSON (agent_name, agent_version, last_active, session_count, capabilities, preferences, context_switches)
- **Query Interfaces**: Python functions for event/knowledge/profile queries

**Guarantees**:
- Event log append-only (audit trail, never deleted)
- Event schema v1.0 compliance (100% validation)
- Knowledge notes follow Zettelkasten (atomic notes, bidirectional links)
- Agent profiles persistent (preferences preserved across sessions)
- Cross-session learning enabled (30% reduction in repeated mistakes target)
- Retention policies enforced (events archived after 6 months)
- Trace correlation via trace_id (multi-step workflows linked)

---

### 3.4 Advanced Features (2 capabilities)

#### SAP-011: docker-operations
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [docker-operations/](../docker-operations/)
**Priority**: P1 (high value)

**Purpose**: Dockerfiles, docker-compose, container optimization, MCP deployment

**Includes**:
- `static-template/Dockerfile` (~194 lines, production multi-stage)
- `static-template/Dockerfile.test` (~104 lines, CI-optimized)
- `static-template/docker-compose.yml` (~223 lines, orchestration)
- `static-template/.dockerignore` (~167 lines, build context optimization)
- `static-template/DOCKER_BEST_PRACTICES.md` (~453 lines, guidance)

**Interfaces**:
- **Production Build**: `docker build -t <project>:latest .` (multi-stage: builder + runtime)
- **Test Build**: `docker build -t <project>:test -f Dockerfile.test .` (single-stage, editable)
- **docker-compose**: `docker-compose up -d` (start), `docker-compose logs -f` (monitor), `docker-compose down` (stop)
- **Multi-arch**: `docker buildx build --platform linux/amd64,linux/arm64 -t <project>:latest .`
- **Config**: Environment variables via `.env` file (12-factor app pattern)

**Guarantees**:
- Production image size ≤250MB (multi-stage wheel build, 40% smaller than editable)
- Test image optimized for CI (GitHub Actions cache: 6x faster, 3 min → 30 sec)
- Non-root execution (UID 1000, security best practice)
- No secrets in images (audit via `docker history`)
- Build context ≤20MB (.dockerignore: 81% reduction, mcp-n8n pattern)
- Health checks: Import-based (<100ms, MCP) or HTTP (<500ms, web)
- Idempotent builds (cache-friendly layer ordering)
- Security scans pass (Trivy HIGH/CRITICAL = 0 target)

**Current Adopter Pain**: "No documented lifecycle for enabling/disabling Docker options; inconsistent adoption"

#### SAP-012: development-lifecycle
**Status**: Draft (Phase 3) ✅ Complete
**Location**: [development-lifecycle/](../development-lifecycle/)
**Priority**: P1 (high value)

**Purpose**: DDD → BDD → TDD workflow, 8-phase lifecycle (Vision → Monitoring), sprint planning

**Includes**:
- `static-template/dev-docs/workflows/` (6 workflow docs, 5,285 lines)
  - **DEVELOPMENT_PROCESS.md** (1,108 lines) - 8-phase lifecycle overview
  - **DEVELOPMENT_LIFECYCLE.md** (753 lines) - DDD→BDD→TDD integration
  - **DDD_WORKFLOW.md** (919 lines) - Documentation Driven Design
  - **BDD_WORKFLOW.md** (1,148 lines) - Behavior Driven Development
  - **TDD_WORKFLOW.md** (1,187 lines) - Test Driven Development
  - **README.md** (170 lines) - Workflow index
- **8-phase lifecycle**: Vision (months) → Planning (weeks) → Requirements (days) → Development (days-weeks) → Testing (hours-days) → Review (hours-days) → Release (hours) → Monitoring (continuous)
- **DDD → BDD → TDD integration**: Docs-first → Gherkin scenarios → RED-GREEN-REFACTOR cycles
- **Templates** (9 files): Sprint planning, release planning, process metrics
- **Anti-Patterns**: `dev-docs/ANTI_PATTERNS.md` (1,309 lines)

**Interfaces**:
- **Phase Contracts**: Each phase has inputs, activities, outputs, quality gates
- **Workflows**: 6 comprehensive workflow guides (tutorial + decision trees)
- **Templates**: sprint-template.md, release-template.md, PROCESS_METRICS.md
- **Decision Trees**: When to use DDD vs BDD vs TDD, time investment by complexity

**Guarantees**:
- All 8 phases documented with time scales (minutes to months)
- Phase-to-phase quality gates (prevent bad code from advancing)
- DDD → BDD → TDD proven to reduce defects 40-80% (research-backed)
- Sprint planning templates reduce overhead by 50%
- Process metrics track quality (defects, coverage), velocity (story points), adherence (DDD/BDD/TDD adoption)
- Integration with SAP-004 (testing), SAP-006 (quality gates), SAP-008 (scripts)

---

### 3.5 Cross-Repository & Optimization (1 capability)

#### SAP-013: metrics-tracking
**Status**: Draft (Phase 4) ✅ Complete
**Location**: [metrics-tracking/](../metrics-tracking/)
**Priority**: P2 (optimization)

**Purpose**: ClaudeROICalculator, process metrics, sprint velocity tracking

**Includes**:
- `static-template/src/<package>/utils/claude_metrics.py` (~459 lines, ClaudeMetric + ClaudeROICalculator)
- `static-template/project-docs/metrics/PROCESS_METRICS.md` (~855 lines, comprehensive KPI tracking)
- Sprint/release dashboard templates (quality, velocity, adherence, adoption metrics)

**Interfaces**:
- **Python API**: `ClaudeROICalculator(developer_hourly_rate=100)`
- **ClaudeMetric**: Track session (task_type, lines_generated, time_saved_minutes, iterations_required, bugs, quality_score, test_coverage)
- **Methods**: `add_metric()`, `calculate_time_saved()`, `calculate_quality_metrics()`, `generate_report()`, `export_to_csv()`, `export_to_json()`
- **Metrics Dashboard**: 4 categories (Quality, Velocity, Process Adherence, Adoption) with research-backed targets

**Guarantees**:
- Claude ROI calculated (hours_saved, cost_savings, acceleration_factor)
- Quality metrics tracked (iterations, bug_rate, doc_quality, coverage, first_pass_success_rate)
- Sprint velocity tracked (story_points_completed / story_points_committed)
- Process adherence measured (DDD/BDD/TDD adoption ≥80-90% targets)
- Defect rate tracked (<3 per release target, 40-80% reduction with TDD)
- ROI estimate: ~$109,200/year per developer (from reduced rework)

---

## 4. Interfaces

### 4.1 Project Generation Interface

**Command**:
```bash
python setup.py <project-name> \
  --author "Your Name" \
  --email "your.email@example.com" \
  [--no-docker] \
  [--no-memory] \
  [--no-claude] \
  [--force]
```

**Inputs**:
- `project-name`: Project name (required, kebab-case)
- `--author`: Author name (optional, prompts if not provided)
- `--email`: Author email (optional, prompts if not provided)
- `--no-docker`: Skip Docker files
- `--no-memory`: Skip A-MEM system
- `--no-claude`: Skip Claude-specific files
- `--force`: Overwrite existing directory

**Outputs**:
- Generated project directory: `<project-name>/`
- Git repository initialized
- All tests passing
- README with project details

**Guarantees**:
- Idempotent with `--force`
- All placeholders substituted
- Valid Python package structure
- Documented in generated README

### 4.2 Testing Interface

**Commands**:
```bash
pytest                    # Run all tests
pytest --cov              # Run with coverage
pytest --collect-only     # List tests without running
pytest -k <pattern>       # Run tests matching pattern
pytest -v                 # Verbose output
```

**Config**: `pyproject.toml` [tool.pytest.ini_options]

**Guarantees**:
- Coverage ≥85% enforced
- Tests pass in <30 seconds (unit tests)
- No test pollution (isolation)

### 4.3 Quality Gates Interface

**Commands**:
```bash
pre-commit install              # Install hooks
pre-commit run --all-files      # Run all hooks manually
just pre-merge                  # Run all pre-merge checks
```

**Hooks**:
1. trailing-whitespace
2. end-of-file-fixer
3. check-yaml
4. ruff (formatting + linting)
5. mypy (type checking)

**Guarantees**:
- All commits pass quality gates
- Consistent code formatting
- No type errors

### 4.4 CI/CD Interface

**Triggers**:
- `push` → test.yml, lint.yml
- `pull_request` → test.yml, lint.yml, dependency-review.yml
- `release` → release.yml
- `schedule` (weekly) → security.yml (CodeQL, dependency review)

**Workflows**:
- **test.yml**: Run pytest, upload coverage
- **lint.yml**: Run ruff, mypy
- **release.yml**: Build, test, publish to PyPI
- **security.yml**: CodeQL scanning, dependency review

**Guarantees**:
- All PRs pass CI before merge
- Releases automated (tag → publish)
- Security scans weekly

### 4.5 Documentation Interface

**Structure**:
```
<project>/
├── README.md                  # Project overview
├── AGENTS.md                  # Agent guidance
├── CLAUDE.md                  # Claude-specific (optional)
├── user-docs/                 # User-facing docs (Diataxis)
│   ├── tutorials/
│   ├── how-to/
│   ├── reference/
│   └── explanation/
├── dev-docs/                  # Developer docs
│   ├── workflows/
│   ├── examples/
│   └── vision/
└── project-docs/              # Project management
    ├── sprints/
    ├── releases/
    └── metrics/
```

**Frontmatter**:
```yaml
---
title: Document Title
type: tutorial | how-to | reference | explanation
status: current | draft | deprecated
audience: users | developers | agents | all
test_extraction: true | false
---
```

**Guarantees**:
- Diataxis structure enforced
- Frontmatter validated
- Executable How-Tos testable

---

## 5. Data Models

### 5.1 Project Metadata Model

```yaml
project:
  name: string                 # Project name (kebab-case)
  package_name: string         # Python package name (snake_case)
  version: string              # Semver (e.g., 0.1.0)
  author: string               # Author name
  email: string                # Author email
  description: string          # Short description
  python_version: string       # Min Python version (e.g., 3.11)
  chora_base_version: string   # chora-base version used (e.g., 3.3.0)
  optional_features:
    docker: boolean            # Docker files included
    memory: boolean            # A-MEM system included
    claude: boolean            # Claude-specific files included
```

**Location**: Encoded in `pyproject.toml`, `README.md`, generated files

### 5.2 Blueprint Variable Model

```yaml
variables:
  project_name: string         # "my-project"
  project_slug: string         # "my_project"
  package_name: string         # "my_project"
  author: string               # "Victor"
  email: string                # "victor@example.com"
  project_version: string      # "0.1.0"
  python_version: string       # "3.11"
  current_year: string         # "2025"
```

**Usage**: Jinja2 substitution in `.blueprint` files

### 5.3 Capability Model (in SAP Index)

```yaml
capability:
  sap_id: string               # SAP-NNN
  name: string                 # capability-name (kebab-case)
  version: string              # Semver
  status: enum                 # Draft | Pilot | Active | Deprecated | Archived
  phase: enum                  # Phase 1 | Phase 2 | Phase 3 | Phase 4
  priority: enum               # P0 | P1 | P2
  location: path               # docs/reference/skilled-awareness/<name>/
  dependencies: array[string]  # [SAP-000, SAP-003]
  estimated_effort: string     # "10-14 hours"
```

**Location**: [INDEX.md](../INDEX.md)

---

## 6. Behavior

### 6.1 Project Generation Workflow

```
1. Collect Inputs
   - Project name (required)
   - Author info (prompt if missing)
   - Optional features (flags)

2. Validate Inputs
   - Project name: kebab-case, unique
   - Author/email: non-empty
   - Directory: doesn't exist (unless --force)

3. Copy Static Template
   - cp -r static-template/ <project-name>/
   - Preserve permissions

4. Process Blueprints
   - For each .blueprint file:
     - Load template (Jinja2)
     - Substitute variables
     - Write to target (remove .blueprint extension)

5. Rename Directories
   - src/__package_name__/ → src/<package_name>/

6. Initialize Git
   - git init
   - git add .
   - git commit -m "Initial commit from chora-base v<version>"

7. Validate Generation
   - Check all placeholders substituted
   - Run pytest --collect-only (verify tests loadable)
   - Check README contains project name

8. Report Success
   - Output project directory
   - Show next steps
```

### 6.2 Testing Workflow

```
1. Run Tests
   - pytest (all tests)
   - pytest --cov (with coverage)

2. Collect Results
   - Pass/fail for each test
   - Coverage percentage
   - Duration

3. Enforce Quality Gates
   - Coverage ≥85% required
   - All tests must pass
   - Duration <30s for unit tests

4. Report
   - Summary (passed/failed/skipped)
   - Coverage report
   - Failures with traceback
```

### 6.3 Quality Gate Workflow

```
1. Git Commit Triggered
   - User runs: git commit

2. Pre-Commit Hook Executes
   - trailing-whitespace
   - end-of-file-fixer
   - check-yaml
   - ruff (format + lint)
   - mypy (type check)

3. Hooks Pass/Fail
   - Pass: Commit proceeds
   - Fail: Commit blocked, show errors

4. User Fixes Issues
   - Address hook failures
   - Re-run commit
```

### 6.4 SAP Adoption Workflow (for chora-base itself)

```
1. New Capability Identified
   - Add to SAP Index (status: Planned)

2. Create SAP (DDD → BDD → TDD)
   - DDD: Charter + Protocol
   - BDD: Acceptance criteria
   - TDD: Infrastructure + Awareness + Blueprint + Ledger

3. Pilot Adoption
   - 1-3 adopters install SAP
   - Collect feedback

4. Production Release
   - Update SAP status: Pilot → Active
   - Broadcast to ecosystem
   - Update chora-base-meta SAP Protocol

5. Maintenance
   - Version updates (semver)
   - Upgrade blueprints for MAJOR changes
   - Ledger tracking
```

---

## 7. Quality Gates

### 7.1 Generated Project Quality

**Requirements**:
- ✅ All tests pass (`pytest`)
- ✅ Coverage ≥85% (`pytest --cov`)
- ✅ No placeholder strings ({{variable}})
- ✅ Valid Python imports
- ✅ README has project details
- ✅ Git initialized

### 7.2 chora-base Template Quality

**Requirements**:
- ✅ All 14 capabilities documented (this Protocol)
- ✅ Blueprints valid Jinja2
- ✅ Static template passes quality gates
- ✅ Generation tested with examples/
- ✅ SAPs follow framework (5 artifacts)

### 7.3 SAP Quality

**Requirements** (per [sap-framework/protocol-spec.md](../sap-framework/protocol-spec.md)):
- ✅ All 5 artifacts present
- ✅ YAML frontmatter valid
- ✅ Blueprints agent-executable
- ✅ Ledger tracks adopters
- ✅ Examples provided

---

## 8. Dependencies

### 8.1 All Capabilities Depend On

- **SAP-000** (sap-framework): Provides structure, templates, governance
- **Python 3.11+**: Target platform
- **Git**: Version control

### 8.2 Capability Dependencies

```
SAP-000 (sap-framework) [FOUNDATIONAL]
   ↓
   ├─→ SAP-001 (inbox-coordination)
   ├─→ SAP-002 (chora-base-meta, this SAP)
   ├─→ SAP-003 (project-bootstrap)
   │      ↓
   │      └─→ SAP-004 (testing-framework)
   │             ↓
   │             ├─→ SAP-005 (ci-cd-workflows)
   │             └─→ SAP-006 (quality-gates)
   ├─→ SAP-007 (documentation-framework)
   │      ↓
   │      └─→ SAP-009 (agent-awareness)
   ├─→ SAP-012 (development-lifecycle)
   │      ↓
   │      └─→ SAP-008 (automation-scripts)
   ├─→ SAP-010 (memory-system)
   ├─→ SAP-011 (docker-operations)
   └─→ SAP-013 (metrics-tracking)
```

---

## 9. Versioning

### 9.1 chora-base Versioning

**Current Version**: 3.3.0

**Format**: MAJOR.MINOR.PATCH (semantic versioning)

**Version History**:
- **v3.3.0** (2025-10-25): Claude-Specific Development Framework
- **v3.2.0** (2025-10-26): Agentic Development Framework
- **v3.0.0** (2025-10-25): AI-Agent-First Architecture (BREAKING)
- **v2.x**: Copier-based (deprecated)
- **v1.x**: Initial template (deprecated)

**Compatibility**:
- Projects generated with v3.x compatible with each other
- v3.x BREAKS compatibility with v2.x (no Copier)
- Upgrade guides in `docs/upgrades/`

### 9.2 SAP Versioning

Each SAP follows semantic versioning independently.

**Example** (chora-base-meta SAP):
- **v1.0.0**: Initial release
- **v1.1.0**: Add new capability (SAP-014)
- **v2.0.0**: BREAKING change (restructure capabilities)

**Upgrade Blueprints**: `chora-base/upgrades/vX.Y-to-vA.B.md`

---

## 10. Security

### 10.1 Generated Project Security

**GitHub Actions**:
- CodeQL scanning (weekly)
- Dependency review (on PR)
- Dependabot (automated dependency updates)

**Pre-Commit**:
- No secrets committed (future: detect-secrets hook)

**Docker**:
- Multi-stage builds (minimize attack surface)
- Non-root user
- Minimal base images

### 10.2 chora-base Template Security

**Blueprint Safety**:
- No hardcoded credentials
- All secrets via environment variables
- `.env.example` provided (not `.env`)

**Static Template**:
- `.gitignore` prevents secret commits
- No API keys, tokens in template

---

## 11. Examples

### 11.1 Generated Project Example

**chora-compose**:
- Generated from chora-base v1.9.x
- 14k lines of code
- Complete MCP server with chora-base patterns
- Location: External repository

**mcp-n8n**:
- Generated from chora-base v1.8.x
- MCP gateway for n8n
- Location: External repository

### 11.2 Example Projects (in chora-base)

**examples/full-featured-with-vision/**:
- Complete project with all features
- Demonstrates dev-docs/vision/ patterns

**examples/full-featured-with-docs/**:
- Complete project with Diataxis docs
- Demonstrates documentation framework

---

## 12. Related Documents

**Core chora-base Docs**:
- [README.md](../../../../README.md) - Project overview
- [AGENTS.md](../../../../AGENTS.md) - Agent guidance
- [CHANGELOG.md](../../../../CHANGELOG.md) - Version history
- [CLAUDE_SETUP_GUIDE.md](../../../../CLAUDE_SETUP_GUIDE.md) - Claude setup

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000
- [INDEX.md](../INDEX.md) - SAP registry
- [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md) - Roadmap

**Other chora-base-meta SAP Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - Installation
- [ledger.md](ledger.md) - Adopter tracking

---

**Version History**:
- **1.0.0** (2025-10-27): Initial protocol specification for chora-base meta-SAP
- **1.0.0** (2025-10-28): Updated with Phase 3 Batch 1 SAPs (SAP-007, SAP-009 complete)
- **1.0.0** (2025-10-28): Updated with Phase 3 Batch 2 SAPs (SAP-012, SAP-008 complete)
- **1.0.0** (2025-10-28): Updated with Phase 3 Batch 3 SAP-010 (memory-system/A-MEM complete)
- **1.0.0** (2025-10-28): Phase 3 Complete! SAP-011 (docker-operations) added - 93% coverage (13/14 SAPs)
- **1.0.0** (2025-10-28): 🎉 100% COMPLETE! SAP-013 (metrics-tracking) completes Phase 4 - ALL 14 SAPs DONE!
