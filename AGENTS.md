# AGENTS.md - chora-base Template Repository

**Purpose**: Machine-readable instructions for AI agents working on the chora-base template repository.

**Last Updated**: 2025-11-08 (Windows compatibility + cross-platform enforcement)

---

## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST work on Windows, Mac, and Linux without modification.**

Before writing Python scripts, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)

**Validation**: `python scripts/validate-windows-compat.py --file your-script.py`

---

## ⚠️ CRITICAL: chora-base is a TEMPLATE SOURCE

**DO NOT** try to "set up chora-base" as if it were a project to develop.

**chora-base** is a **template repository** used to **generate other projects**.

### Decision Tree for Agents

**Are you trying to CREATE A NEW PROJECT using chora-base?**

→ **YES**: Use the fast-setup script:

```bash
python scripts/create-model-mcp-server.py \
    --name "Your Project Name" \
    --namespace yournamespace \
    --output ~/projects/your-project
```

See: [README.md](README.md) for complete instructions, or [docs/user-docs/quickstart-mcp-server.md](docs/user-docs/quickstart-mcp-server.md)

**Time**: 5-10 minutes to fully-configured project

---

**Are you DEVELOPING chora-base itself** (contributing to the template)?

→ **YES**: Continue reading this file

**What you're working on**: The template source code, SAP definitions, scripts, documentation

**Key directories**:
- `static-template/` - Files that get copied to generated projects
- `docs/skilled-awareness/` - SAP documentation (30+ capabilities)
- `scripts/` - Automation scripts (create-model-mcp-server.py, install-sap.py, etc.)

---

## Project Overview

**chora-base** is a blueprint-driven Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates without relying on Copier.

**Repository Type**: Template repository (generates other projects)
**Primary Users**: Human developers and AI agents generating/maintaining Python projects
**Key Technology Stack**: Static scaffolding (`static-template/`), and Skilled Awareness Packages (SAP) for capability governance

### Key Concepts

- **Template vs Generated Project**: chora-base is the template; generated projects are adopters
- **Blueprint Generation**: `.blueprint` files define how adopters bootstrap projects via scripted or agent-led workflows
- **Static Assets**: `static-template/` contains ready-to-copy files used by blueprints
- **Skilled Awareness Packages (SAPs)**: Each major capability ships with charter, protocol, awareness guide, adoption blueprint, and ledger entry to guide humans and AI agents
- **Upgrade Path**: Adopters follow SAP adoption blueprints and ledger/broadcast updates to stay aligned with the template

---

## Skilled Awareness Packages (SAPs)

### Overview

chora-base packages all major capabilities as **Skilled Awareness Packages (SAPs)** — complete, installable bundles with clear contracts and agent-executable blueprints.

**Why SAPs Matter**:
- Clear contracts (explicit guarantees, no assumptions)
- Predictable upgrades (sequential adoption, migration blueprints)
- Machine-readable (AI agents can parse and execute)
- Governance (versioning, change management, tracking)

### SAP Structure

Every SAP includes:

1. **5 Core Artifacts**:
   - Capability Charter (problem, scope, outcomes)
   - Protocol Specification (technical contract)
   - Awareness Guide (agent execution patterns)
   - Adoption Blueprint (installation steps)
   - Traceability Ledger (adopter tracking)

2. **Infrastructure** (schemas, templates, configs, directories)

3. **Testing Layer** (optional validation)

### Key Documents

**Root Protocol**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- Defines what SAPs are and how they work
- Installation pattern (blueprint-based, not scripts)
- Integration with DDD → BDD → TDD
- Scope levels (Vision & Strategy, Planning, Implementation)

**SAP Index**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
- Registry of all 14 capabilities
- Current coverage: 2/14 (14%)
- Target coverage: 100% by Phase 4 (2026-05)
- Dependencies, priorities, effort estimates

**Framework SAP**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- Meta-SAP defining the SAP pattern itself
- Complete reference implementation
- Templates and guidelines

**Reference Implementation**: [docs/skilled-awareness/inbox/](docs/skilled-awareness/inbox/)
- Pilot SAP for cross-repo coordination
- Complete example with infrastructure and testing

### Creating SAPs

**When to Create SAP**:
- New major capability (e.g., testing-framework, docker-operations)
- Capability needs structured governance
- Multiple adopters will use capability
- Clear upgrade path needed

**Process**:
1. Read: [docs/skilled-awareness/document-templates.md](docs/skilled-awareness/document-templates.md)
2. Create directory: `docs/skilled-awareness/<capability-name>/`
3. Create 5 artifacts using templates
4. Add infrastructure (schemas, templates, etc.)
5. Update SAP Index: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
6. Follow DDD → BDD → TDD:
   - DDD: Create Charter + Protocol
   - BDD: Define acceptance criteria
   - TDD: Implement infrastructure + Awareness + Blueprint

**Time Estimate**: 8-20 hours per SAP (varies by complexity)

### Installing SAPs

**Process**:
1. Find SAP in INDEX.md
2. Navigate to SAP directory (e.g., `docs/skilled-awareness/inbox/`)
3. Read `adoption-blueprint.md`
4. Execute installation steps sequentially
5. Run validation commands
6. Update `ledger.md` (add adopter record)

**Example**:
```bash
# Find SAP
cat docs/skilled-awareness/INDEX.md

# Read blueprint
cat docs/skilled-awareness/inbox/adoption-blueprint.md

# Execute steps (agent-executable markdown instructions)
# ... follow blueprint step-by-step ...

# Validate
ls inbox/coordination/CAPABILITIES && echo "✅ Installed"
```

### Validating SAPs (SAP-008 L3)

**Automated SAP structure validation** using [scripts/sap-validate.py](scripts/sap-validate.py):

**Quick Commands**:
```bash
# Validate single SAP
just validate-sap-structure docs/skilled-awareness/testing-framework

# Validate all SAPs
just validate-all-saps

# Or call directly
python scripts/sap-validate.py docs/skilled-awareness/testing-framework
python scripts/sap-validate.py --all
```

**What It Checks**:
- ✅ 5 required artifacts present (charter, protocol, awareness, blueprint, ledger)
- ✅ Valid frontmatter in each artifact (---...---)
- ✅ SAP ID format (SAP-###)
- ✅ Version follows semver (X.Y.Z)
- ✅ Required frontmatter fields (sap_id, version, status)

**Output Example**:
```
[OK] docker-operations
[FAIL] testing-framework
  - capability-charter.md: Missing frontmatter (---...---)
  - protocol-spec.md: Missing frontmatter (---...---)

Summary: 1/2 SAPs passed
```

**Baseline Status** (2025-11-04):
- 2/28 SAPs have proper frontmatter (docker-operations, metrics-tracking)
- 26/28 SAPs need frontmatter added to artifacts
- Target: 100% SAP compliance by end of Phase 3

### SAP Roadmap

**Phase 1** (2025-10 → 2025-11): Framework Hardening
- ✅ SAP-000 (sap-framework)
- ✅ SAP-001 (inbox-coordination, pilot)
- 🔄 SAP-002 (chora-base-meta)

**Phase 2** (2025-11 → 2026-01): Core Capabilities
- SAP-003 (project-bootstrap)
- SAP-004 (testing-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)

**Phase 3** (2026-01 → 2026-03): Extended Capabilities
- SAP-007 (documentation-framework)
- SAP-008 (automation-scripts)
- SAP-009 (agent-awareness)
- SAP-010 (memory-system / A-MEM)
- SAP-011 (docker-operations)
- SAP-012 (development-lifecycle)

**Phase 4** (2026-03 → 2026-05): Optimization
- SAP-013 (metrics-tracking)

**See**: [docs/skilled-awareness/chora-base-sap-roadmap.md](docs/skilled-awareness/chora-base-sap-roadmap.md)

---

## Repository Structure

```
chora-base/
├── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  # Root SAP protocol
├── static-template/             # Static scaffolding copied into generated projects
│   ├── src/                     # Python source baseline
│   ├── tests/                   # Test baseline
│   ├── scripts/                 # Automation scripts
│   ├── .github/workflows/       # CI/CD workflows
│   └── ...                      # Other project files

│   ├── README.md.blueprint
│   ├── CLAUDE.md.blueprint
│   ├── AGENTS.md.blueprint
│   └── ...
├── docs/                        # Template documentation
│   ├── reference/
│   │   ├── skilled-awareness/   # SAP Framework & all SAPs
│   │   │   ├── INDEX.md         # SAP registry (all 14 capabilities)
│   │   │   ├── document-templates.md  # Templates for creating SAPs
│   │   │   ├── chora-base-sap-roadmap.md  # Phased adoption plan
│   │   │   ├── sap-framework/   # SAP-000: Framework SAP (meta-capability)
│   │   │   ├── inbox/           # SAP-001: Inbox coordination (pilot)
│   │   │   ├── chora-base/      # SAP-002: chora-base meta-SAP (planned)
│   │   │   └── ...              # Future SAPs (project-bootstrap, testing, etc.)
│   │   ├── template-configuration.md
│   │   └── ...
│   ├── upgrades/                # Version upgrade guides
│   │   ├── README.md            # Upgrade guide index
│   │   ├── PHILOSOPHY.md        # Upgrade philosophy
│   │   ├── UPGRADE_GUIDE_TEMPLATE.md  # Template for writing upgrade guides
│   │   ├── v1.9.2-to-v1.9.3.md  # Version-specific guides (naming: vX.Y-to-vX.Z.md)
│   │   └── ...
│   ├── how-to/                  # Task-oriented guides
│   │   ├── 01-setup-new-project.md
│   │   ├── 02-configure-testing.md
│   │   └── ...
│   ├── explanation/             # Conceptual explanations
│   ├── research/                # Research documents
│   │   └── Agentic Coding Best Practices Research.pdf
│   ├── BENEFITS.md              # ROI analysis
│   └── DOCUMENTATION_PLAN.md    # Documentation strategy
├── inbox/                       # Inbox coordination capability (SAP-001)
│   ├── INBOX_PROTOCOL.md        # Protocol
│   ├── CLAUDE.md                # Awareness
│   ├── schemas/                 # JSON schemas
│   ├── coordination/            # Coordination directory
│   └── examples/                # Complete examples (e.g., health-monitoring-w3)
├── examples/                    # Example generated projects
│   ├── full-featured-with-vision/
│   ├── full-featured-with-docs/
│   └── ...
├── CHANGELOG.md                 # Version history
├── README.md                    # Project overview
└── AGENTS.md                    # This file

**IMPORTANT**: This is the FIRST TIME chora-base has its own AGENTS.md. Previously, lack of guidance caused agents to misplace files (e.g., upgrade docs in repo root instead of docs/upgrades/).
```

---

## File Organization Conventions

### Upgrade Documentation

**Location**: `docs/upgrades/`
**Naming Pattern**: `vX.Y-to-vX.Z.md` (e.g., `v1.9.2-to-v1.9.3.md`)
**Not**: UPPERCASE naming, repo root placement

**Why This Matters**: Previous upgrade docs (v1.9.0-to-v1.9.1, v1.9.1-to-v1.9.2) were misplaced in repo root because chora-base lacked this AGENTS.md to guide agents.

**Template**: Use `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md` for structure

### Research Documents

**Location**: `docs/research/`
**Format**: PDF, markdown, or other documentation formats
**Purpose**: Background research informing template features

### How-To Guides

**Location**: `docs/how-to/`
**Naming Pattern**: `NN-kebab-case-title.md` (e.g., `01-setup-new-project.md`)
**Audience**: Humans + AI agents (task-oriented)

### Reference Documentation

**Location**: `docs/reference/`
**Naming Pattern**: `kebab-case-title.md` (e.g., `template-configuration.md`)
**Audience**: Humans + AI agents (information-oriented)

### Example Projects

**Location**: `examples/`
**Structure**: Full generated project directories
**Purpose**: Test template features, demonstrate usage patterns
**Status**: Examples may lag behind template (document drift in commit messages)

---

## Development Workflows

### Adding New Features to Template

1. **Research Phase**
   - Document research findings in `docs/research/`
   - Identify industry best practices
   - Review adopter feedback from real projects (mcp-n8n, chora-compose, and others across MCP, REST, CLI, library domains)

2. **Design Phase**
   - Update `CHANGELOG.md` under `## [Unreleased]`
   - Consider opt-in vs opt-out (new features usually opt-in)
   - Determine whether capability needs its own Skilled Awareness Package (SAP)
   - Update relevant blueprints and static assets to include the feature

3. **Implementation Phase**
   - Update `static-template/` and `blueprints/` assets
   - Add automation or install scripts if feature is optional
   - Run blueprint generation scripts (or agent-assisted flow) to validate outputs
   - Generate/update examples in `examples/` if demonstrating complex feature

4. **Documentation Phase**
   - Update `README.md` if user-facing feature
   - Add to `template/AGENTS.md.jinja` if relevant to AI agents
   - Document in appropriate `docs/` subdirectory
   - Update `docs/BENEFITS.md` if adding measurable value
   - Create/refresh SAP documents (charter, protocol, awareness guide, adoption blueprint, ledger entry)

5. **Validation Phase**
   - Generate fresh project using blueprint workflow (see setup guides)
   - Run generated project's tests: `cd /tmp/test-validation && ./scripts/setup.sh && pytest`
   - Test upgrade path: follow SAP adoption blueprint scenarios (e.g., apply updates to example repos)
   - Verify conditional combinations (Docker on/off, memory on/off, etc.)

### Releasing New Version

**Version Numbering**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR** (X.0.0): Breaking changes requiring adopter action
- **MINOR** (1.X.0): New features, additive changes (current: v1.9.3)
- **PATCH** (1.1.X): Bug fixes only

**Release Process**:

1. **Pre-Release Validation**
   ```bash
   # Generate project from blueprints (interactive; answer prompts as needed)
   # Use AI agent to generate projects from static-template/ and SAP templates
   cd /tmp/test-release && ./scripts/setup.sh && pytest

   # Test update path (use example project + SAP adoption blueprint)
   cd examples/full-featured-with-vision
   # Follow relevant SAP adoption blueprint to apply latest changes
   ./scripts/setup.sh && pytest
   ```

2. **Create Upgrade Guide**
   - Location: `docs/upgrades/vX.Y-to-vX.Z.md`
   - Use template: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`
   - Include decision tree for AI agents
   - Document displacement risk (ZERO/LOW/MEDIUM/HIGH)
   - Add migration steps, validation checklist

3. **Update Core Files**
   ```bash
   # Update CHANGELOG.md
   # Change: ## [Unreleased]
   # To:     ## [X.Y.Z] - 2025-MM-DD

   # Update README.md Recent Updates section
   # Add new version entry with key features

   # Update docs/upgrades/README.md
   # Add version to version-specific guides table
   ```

4. **Commit and Tag**
   ```bash
   git add -A
   git commit -m "feat(scope): Brief description (vX.Y.Z)

   Detailed changes:
   - Feature 1
   - Feature 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"

   git tag vX.Y.Z
   git push origin main --tags
   ```

5. **Create GitHub Release**
   ```bash
   gh release create vX.Y.Z \
     --title "vX.Y.Z - Brief Title" \
     --notes "Release notes here (benefits, changes, upgrade guide link)"
   ```

6. **Update docs/upgrades/README.md**
   - Update version table with new entry
   - Update "Status" line if completing a phase

### Creating Upgrade Documentation

**Template**: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`

**Required Sections**:
1. Quick Assessment (TL;DR, effort estimate)
2. Decision Tree for AI Agents (structured IF/THEN)
3. What Changed (file-by-file with line counts)
4. Migration Steps (bash commands)
5. Testing After Upgrade (validation checklist)
6. Rollback Instructions
7. FAQ

**AI-Optimized Format**:
- Machine-parseable decision criteria
- Clear displacement risk assessment (ZERO/LOW/MEDIUM/HIGH)
- Structured upgrade effort estimate (<10min, 10-20min, 1-2hrs, etc.)
- Benefits vs costs analysis for optional changes

---

## Testing Strategy

### Template Generation Tests

```bash
# Minimal configuration (accept defaults)
# Use AI agent to generate projects from static-template/ and SAP templates

# Full-featured configuration
# Use AI agent to generate projects from static-template/ and SAP templates
# Enable all optional features when prompted

# Specific project types (run setup script and choose appropriate options)
# Use AI agent to generate projects from static-template/ and SAP templates
# Use AI agent to generate projects from static-template/ and SAP templates
# Use AI agent to generate projects from static-template/ and SAP templates
```

### Generated Project Validation

```bash
# Validate generated project can setup and test
cd /tmp/test-project
./scripts/setup.sh
pytest
pre-commit run --all-files
just test  # if justfile included
```

### Update Path Testing

```bash
# Test template updates merge correctly (use SAP adoption blueprint)
cd examples/full-featured-with-vision
git checkout -b test-update
# Apply latest blueprint changes manually or via automation scripts
# Resolve any conflicts and verify diff is reasonable
```

### Conditional Feature Testing

Test feature combinations that users commonly choose:

1. **Minimal Python Project**: Basic structure, no optional features
2. **Full-Featured Python Project**: All optional features enabled
3. **Library Project**: No CLI, yes docs, yes tests
4. **CLI Tool Project**: Yes CLI, yes tests
5. **MCP Server** (with SAP-014): MCP-specific features, optional memory/Docker

### Test Quality Metrics (SAP-004 L3)

**Current Test Coverage**: 85.00% (achieved 2025-11-04)
**Target Coverage**: ≥85% (enforced in pytest.ini)
**Test Suite Performance**: 60 tests in 0.52s

**Quality Standards**:
- Test flakiness target: <5%
- Test execution time: <60s for full suite
- Coverage threshold: 85% minimum (fail_under in [pytest.ini:45](pytest.ini#L45))
- All tests must pass before PR merge

**Coverage Breakdown**:
- [scripts/install-sap.py:79%](scripts/install-sap.py) - Core SAP installation (79% coverage)
- [scripts/usage_tracker.py:17%](scripts/usage_tracker.py) - Usage tracking (17% coverage, low-priority)
- [tests/conftest.py:94%](tests/conftest.py) - Test fixtures
- [tests/test_install_sap.py:100%](tests/test_install_sap.py) - Install-SAP tests (60 tests, 100% coverage)

**Test Quality Metrics**:
- Total test count: 60
- Test failures: 0 (100% pass rate)
- Test categories:
  - Unit tests: 42 (70%)
  - Integration tests: 12 (20%)
  - End-to-end tests: 6 (10%)

**Test Patterns in Use** (reference: [docs/skilled-awareness/testing-framework/](docs/skilled-awareness/testing-framework/)):
- Basic tests: 60/60 (100%)
- Parametrized tests: ~35/60 (~58%)
- Fixtures: ~25/60 (~42%)
- Mocks: ~18/60 (~30%)
- Error handling tests: ~48/60 (~80%)

**Monitoring Commands**:
```bash
# Run tests with coverage
coverage run -m pytest && coverage report

# Generate HTML coverage report
coverage html
open htmlcov/index.html  # macOS

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Slow tests only
```

**Next Steps to Improve Coverage**:
1. Add tests for `scripts/usage_tracker.py` (current: 17%, target: 85%)
2. Increase `scripts/install-sap.py` coverage from 79% to 85%
3. Add async test patterns as examples (SAP-004 v1.1.0 planned)

---

### Agent Awareness (Nested AGENTS.md/CLAUDE.md) - SAP-009 L3

**Purpose**: Provide structured agent guidance through nested AGENTS.md/CLAUDE.md files using "nearest file wins" pattern for progressive context loading.

**Adoption Level**: L3 (Universal pattern adopted across all domains)

**Core Pattern**: Dual-file hierarchy with domain-specific awareness
- **AGENTS.md**: Generic agent patterns (all agents)
- **CLAUDE.md**: Claude-specific optimizations

**Nested Hierarchy (5 Levels)**:
```
/AGENTS.md, /CLAUDE.md                           ← Root (project overview)
├─ tests/AGENTS.md                               ← Domain: Testing
├─ scripts/AGENTS.md                             ← Domain: Scripts
├─ .chora/AGENTS.md, .chora/CLAUDE.md            ← Domain: Memory (SAP-010)
├─ docs/skilled-awareness/AGENTS.md              ← Domain: SAP capabilities
│  ├─ inbox/AGENTS.md, inbox/CLAUDE.md           ← SAP-001 (Inbox)
│  ├─ agent-awareness/AGENTS.md, CLAUDE.md       ← SAP-009 (this pattern)
│  ├─ memory-system/AGENTS.md, CLAUDE.md         ← SAP-010 (Memory)
│  └─ ... (30+ SAPs with nested awareness)
```

**Progressive Loading Phases**:
1. **Phase 1 (Essential, 0-10k tokens)**:
   - Read root AGENTS.md sections 1-2 (project overview, development process)
   - Load only files directly related to current task
   - **Result**: Quick orientation, minimal token usage

2. **Phase 2 (Extended, 10-50k tokens)**:
   - Read root AGENTS.md fully + domain-specific AGENTS.md
   - Read CLAUDE.md for Claude optimizations
   - Load related SAP protocol-spec.md if implementing capability
   - **Result**: Full context for implementation, 60-70% token savings vs loading everything

3. **Phase 3 (Comprehensive, 50-200k tokens)**:
   - Read all SAP artifacts (capability-charter.md, ledger.md)
   - Load full project history and all documentation
   - **Used only for**: Complex refactoring, architectural decisions, deep debugging

**Domain-Specific Files** (60-70% token reduction):
- **tests/AGENTS.md** (~200 lines, 5-min read): Testing patterns, fixtures, coverage targets
- **scripts/AGENTS.md** (~250 lines, 6-min read): Cross-platform script patterns, validation
- **.chora/AGENTS.md** (~400 lines, 13-min read): Memory system workflows, event logging
- **docs/skilled-awareness/{SAP}/AGENTS.md**: SAP-specific patterns and examples

**Session Startup Routine** (agents should execute this):
```bash
# 1. Read root awareness (Phase 1)
cat AGENTS.md | head -100     # First 100 lines for quick orientation

# 2. Navigate to domain-specific awareness (Phase 2)
cat tests/AGENTS.md           # If working on tests (60% token savings)
cat scripts/AGENTS.md         # If working on scripts (65% token savings)
cat .chora/AGENTS.md          # If working with memory (70% token savings)

# 3. Read Claude optimizations
cat CLAUDE.md                 # Claude-specific patterns (artifact-first, checkpoints)

# 4. Validate awareness structure
just validate-awareness-structure AGENTS.md
just validate-awareness-links
```

**Validation Commands**:
```bash
# Validate AGENTS.md structure (7 required sections)
python scripts/validate-awareness-structure.py AGENTS.md

# Check for broken links in awareness network
python scripts/validate-awareness-links.py

# Show awareness hierarchy
just awareness-hierarchy

# Show awareness statistics
just awareness-stats
```

**Creating Domain-Specific Awareness**:
```bash
# Copy template for new domain
cp docs/skilled-awareness/templates/AGENTS.md.template my-domain/AGENTS.md
cp docs/skilled-awareness/templates/CLAUDE.md.template my-domain/CLAUDE.md

# Edit to add domain-specific patterns
vim my-domain/AGENTS.md

# Validate structure
just validate-awareness-structure my-domain/AGENTS.md
```

**Token Efficiency Tracking** (integrated with SAP-013):
```python
from utils.claude_metrics import ClaudeROICalculator, TokenUsageMetric
from datetime import datetime

calculator = ClaudeROICalculator(developer_hourly_rate=100.0)

# Track a session with progressive loading
metric = TokenUsageMetric(
    session_id="session-2025-11-09-001",
    timestamp=datetime.now(),
    tokens_used=35000,                    # Used Phase 2 (extended context)
    tokens_available=200000,
    progressive_loading_phase=2,          # Loaded domain-specific AGENTS.md
    context_items_loaded=5,               # Root + domain + 3 files
    task_completed=True,
    metadata={"task_type": "feature_implementation", "domain": "tests"}
)
calculator.track_token_usage(metric)

# Generate token usage report
print(calculator.generate_token_usage_report())
```

**Integration with Other SAPs**:
- **ALL SAPs**: Every SAP uses nested awareness pattern for discoverability
- **SAP-010 (Memory)**: Domain-specific .chora/AGENTS.md for memory workflows
- **SAP-015 (Task Tracking)**: Document beads patterns in AGENTS.md
- **SAP-001 (Inbox)**: Domain-specific inbox/AGENTS.md for coordination
- **SAP-027 (Dogfooding)**: Validate awareness adoption completeness

**L3 Achievement Evidence** (2025-11-09):
- ✅ Nested hierarchy implemented (5 levels): root → domain → SAP → feature → component
- ✅ Domain-specific files created: tests/, scripts/, .chora/, inbox/, agent-awareness/
- ✅ Progressive loading documented in CLAUDE.md with 3 phases
- ✅ Token tracking integrated with SAP-013 metrics framework
- ✅ Validation scripts available: validate-awareness-structure.py, validate-awareness-links.py
- ✅ Justfile recipes: 7 awareness commands (validate, hierarchy, stats, create)
- ✅ Template files for creating new domain awareness: AGENTS.md.template, CLAUDE.md.template

**ROI Metrics**:
- **Token reduction**: 60-70% via domain-specific files (Phase 2 vs Phase 3)
- **Onboarding time**: 5-10 min faster per session (targeted reading vs full codebase scan)
- **Context restoration**: <2 min via "nearest file wins" pattern
- **Target**: <50k tokens average per session (current: ~35k baseline)
- **Progressive loading adoption**: ≥90% sessions using Phase 1-2 (vs Phase 3 full load)

**Documentation**:
- Protocol specification: [docs/skilled-awareness/agent-awareness/protocol-spec.md](docs/skilled-awareness/agent-awareness/protocol-spec.md)
- Adoption blueprint: [docs/skilled-awareness/agent-awareness/adoption-blueprint.md](docs/skilled-awareness/agent-awareness/adoption-blueprint.md)
- Domain-specific guide: [docs/skilled-awareness/agent-awareness/AGENTS.md](docs/skilled-awareness/agent-awareness/AGENTS.md)
- Claude patterns: [docs/skilled-awareness/agent-awareness/CLAUDE.md](docs/skilled-awareness/agent-awareness/CLAUDE.md)

**Troubleshooting**:
- **Broken links**: Run `just validate-awareness-links` to find and fix
- **Missing sections**: Run `just validate-awareness-structure FILE` to check 7 required sections
- **Duplicate content**: Keep root AGENTS.md generic, move specifics to domain files
- **Token overuse**: Check progressive loading phase, use domain-specific files for 60-70% reduction
- Phase 1 adoption: ≥90% of sessions
- Task completion rate: ≥95% (maintain current performance)

---

### CI/CD Workflows (GitHub Actions) - SAP-005 L3

**Purpose**: Provide automated testing, linting, security scanning, and release workflows using GitHub Actions for continuous integration and deployment.

**Adoption Level**: L3 (Fully automated, production-ready)

**Core Workflows** (.github/workflows/):

1. **test.yml** - Matrix testing across Python 3.11, 3.12, 3.13
   - Trigger: push (main, develop), pull_request
   - Coverage gate: 85%+ required
   - Duration: ~2-3 minutes
   - Status: ✅ Required for merge

2. **lint.yml** - Code quality gates (ruff + mypy)
   - Trigger: push (main, develop), pull_request
   - Checks: ruff (linting), mypy (type checking)
   - Duration: ~1-2 minutes
   - Status: ✅ Required for merge

3. **smoke.yml** - Quick validation (<1 min)
   - Trigger: push (main, develop), pull_request
   - Purpose: Server starts, basic operations
   - Duration: ~30-60 seconds
   - Status: ✅ Required for merge

4. **codeql.yml** - Security scanning
   - Trigger: push (main, develop), pull_request, schedule (weekly)
   - Purpose: Static security analysis, vulnerability detection
   - Duration: ~3-5 minutes
   - Status: ✅ Required for merge (security critical)

5. **dependency-review.yml** - Dependency security
   - Trigger: pull_request
   - Purpose: Check new dependencies for vulnerabilities
   - Duration: ~30-60 seconds
   - Status: ✅ Required for merge (security critical)

6. **release.yml** - PyPI publishing
   - Trigger: push (tags: 'v*'), workflow_dispatch
   - Purpose: Build wheel, publish to PyPI (OIDC trusted publishing)
   - Duration: ~2-3 minutes
   - Status: N/A (only for releases)

7. **cross-platform-test.yml** - Multi-OS validation
   - Trigger: push (main, develop), pull_request
   - Matrix: Ubuntu, Windows, macOS
   - Purpose: Cross-platform compatibility testing
   - Duration: ~5-7 minutes
   - Status: ✅ Required for merge

**CI Workflow Patterns** (agent should follow):

```bash
# 1. Check CI status at session startup
gh run list --limit 10
just ci-status

# 2. If CI failed, investigate logs
gh run view {run_id} --log
just ci-logs {run_id}

# 3. If transient failure, retry
gh run rerun {run_id}
just ci-retry {run_id}

# 4. If real failure, create bead to track fix (SAP-015)
bd create "Fix CI failure in test.yml" --priority high --blocker "ci-failure-{run_id}"

# 5. Fix locally first (pre-commit hooks via SAP-006)
pytest tests/               # Run tests locally
ruff check src/ tests/      # Run linting locally
mypy src/ tests/            # Run type checking locally

# 6. Push fix and verify CI passes
git push origin branch-name
gh run list --limit 5       # Verify new run passes
```

**Quality Gates** (enforced by CI):
- ✅ 85%+ test coverage (test.yml)
- ✅ Zero linting errors (lint.yml via ruff)
- ✅ Zero type errors (lint.yml via mypy)
- ✅ Zero security vulnerabilities (codeql.yml, dependency-review.yml)
- ✅ Cross-platform compatibility (cross-platform-test.yml)
- ✅ Smoke tests pass (smoke.yml)

**Integration with Other SAPs**:
- **SAP-004 (Testing)**: CI runs pytest test suites with 85%+ coverage gates
- **SAP-006 (Quality Gates)**: Pre-commit hooks (local) + CI workflows (remote) dual validation
- **SAP-028 (PyPI Publishing)**: OIDC trusted publishing in release.yml (zero long-lived tokens)
- **SAP-015 (Task Tracking)**: CI failure → Create bead to track fix with blocker
- **SAP-031 (Enforcement)**: CI/CD as Layer 3 enforcement (9% prevention rate)

**Release Workflow** (agents should execute):

```bash
# 1. Bump version and create tag
python scripts/bump-version.py 1.2.3

# 2. Push tag to trigger release workflow
git push --tags

# 3. Monitor release workflow
gh run list --workflow=release.yml
gh run view {run_id} --log

# 4. Verify PyPI publication
# Test PyPI: https://test.pypi.org/project/{package_name}/
# Prod PyPI: https://pypi.org/project/{package_name}/

# 5. Create GitHub release from tag
gh release create v1.2.3 --notes-from-tag
```

**Troubleshooting CI Failures**:

1. **Coverage below 85%**:
   ```bash
   # Run coverage locally
   pytest --cov=src/package_name --cov-report=term --cov-report=html
   open htmlcov/index.html

   # Add missing tests for uncovered lines
   # Update tests/ directory
   ```

2. **Lint errors**:
   ```bash
   # Run ruff locally
   ruff check src/ tests/

   # Auto-fix fixable issues
   ruff check --fix src/ tests/
   ```

3. **Type errors**:
   ```bash
   # Run mypy locally
   mypy src/ tests/

   # Add type annotations or suppressions
   # Fix type mismatches
   ```

4. **Security vulnerabilities**:
   ```bash
   # Check CodeQL alerts
   gh api repos/{owner}/{repo}/code-scanning/alerts

   # Review dependency vulnerabilities
   gh api repos/{owner}/{repo}/dependabot/alerts

   # Update vulnerable dependencies
   pip install --upgrade {vulnerable_package}
   ```

5. **Cross-platform failures**:
   ```bash
   # Check which OS failed
   gh run view {run_id}

   # Read cross-platform guide
   cat scripts/AGENTS.md  # Cross-platform patterns

   # Use cross-platform template
   cp templates/cross-platform/python-script-template.py scripts/new-script.py
   ```

**L3 Achievement Evidence** (2025-11-09):
- ✅ 7 production workflows deployed (.github/workflows/)
- ✅ Matrix testing: Python 3.11, 3.12, 3.13 (Ubuntu, Windows, macOS)
- ✅ Quality gates: 85%+ coverage, ruff, mypy, CodeQL, dependency review
- ✅ Release automation: OIDC trusted publishing to PyPI
- ✅ Fast feedback: <5 min average workflow execution
- ✅ Justfile recipes: 6 CI commands (status, logs, retry, workflows, show, trigger)
- ✅ Integration with SAP-004, SAP-006, SAP-015, SAP-028, SAP-031

**ROI Metrics**:
- **Setup time**: 90% reduction (hours → 5-10 minutes via pre-configured workflows)
- **Quality gates**: 95%+ preventable issues caught before merge
- **Feedback speed**: <5 min average workflow execution (cached dependencies, parallel jobs)
- **Security**: 100% automated scanning (CodeQL + dependency review)
- **Release time**: 80% reduction (manual publish → one-command automated)

**Documentation**:
- Protocol specification: [docs/skilled-awareness/ci-cd-workflows/protocol-spec.md](docs/skilled-awareness/ci-cd-workflows/protocol-spec.md)
- Adoption blueprint: [docs/skilled-awareness/ci-cd-workflows/adoption-blueprint.md](docs/skilled-awareness/ci-cd-workflows/adoption-blueprint.md)
- Workflow details: [docs/skilled-awareness/ci-cd-workflows/awareness-guide.md](docs/skilled-awareness/ci-cd-workflows/awareness-guide.md)

---

## Common Tasks for AI Agents

### Task 1: Add New Optional Feature

**Goal**: Add a new opt-in feature to the template

**Steps**:
1. Update relevant templates in technology-specific SAPs (e.g., static-template/mcp-templates/ for MCP) to include optional feature toggles.
2. Add conditional logic or installation hooks in `static-template/` and supporting scripts.
3. Refresh SAP documents (especially protocol + adoption blueprint) to describe the new capability.
4. Update `template/AGENTS.md.jinja` if feature affects AI agent workflows.
5. Document in `README.md` under "Features" section.
6. Add to `CHANGELOG.md` under `## [Unreleased]`.
7. Test blueprint generation with feature enabled/disabled via `python setup.py`.

### Task 2: Fix Bug in Template

**Goal**: Correct error in template that affects generated projects

**Steps**:
1. Reproduce in generated project:
   ```bash
   python setup.py /tmp/bug-test
   cd /tmp/bug-test
   # Reproduce issue
   ```

2. Fix in `template/` source files

3. Test fix:
   ```bash
   python setup.py /tmp/bug-fix-test
   cd /tmp/bug-fix-test
   # Verify fix works
   ```

4. Update `CHANGELOG.md` under `## [Unreleased]` in "Fixed" section

5. Commit with `fix(scope): description`

6. Create PATCH release if critical bug

### Task 3: Release New Version

**See**: "Releasing New Version" workflow above

**Checklist**:
- [ ] All tests pass (`python setup.py /tmp/test && cd /tmp/test && pytest`)
- [ ] CHANGELOG.md updated (Unreleased → [X.Y.Z])
- [ ] README.md updated (Recent Updates section)
- [ ] Upgrade guide created (`docs/upgrades/vX.Y-to-vX.Z.md`)
- [ ] Upgrade guide added to `docs/upgrades/README.md` table
- [ ] Commit with version in message
- [ ] Git tag created (`git tag vX.Y.Z`)
- [ ] Pushed to origin with tags (`git push origin main --tags`)
- [ ] GitHub release created (`gh release create vX.Y.Z`)

### Task 4: Update Research Documentation

**Goal**: Incorporate new research findings into template

**Steps**:
1. Save research document to `docs/research/`

2. Analyze research for actionable enhancements

3. Create plan with specific changes (e.g., Phase 1, 2, 3)

4. Implement changes (see Task 1: Add New Optional Feature)

5. Reference research in commit messages and upgrade guides

6. Update `README.md` or relevant docs with research-backed rationale

**Example**: v1.9.3 added super-tests, memory architecture, and query patterns based on "Agentic Coding Best Practices Research.pdf"

---

## Architecture Decisions

### Why Jinja2 Templating?

**Rationale**: Blueprints use Jinja2 placeholders for flexible customization and remain compatible with existing project content
**Trade-off**: Complex conditionals require disciplined structure; mitigate with helper scripts and clear template snippets

### Why Opt-In for Advanced Features?

**Rationale**: Prevent overwhelming new adopters, let users choose complexity
**Examples**: `documentation_advanced_features=false`, `include_docker=false`, `include_memory_system=true`

### Why Separate AGENTS.md.jinja (2,540 lines)?

**Known Issue**: AGENTS.md.jinja has grown 176% from v1.0.0 (782 lines) to v1.9.3 (2,540 lines) with zero refactoring
**Upcoming Change**: v2.0.0 will refactor to nested AGENTS.md structure per research recommendations
**Pattern**: Nearest file wins (tests/AGENTS.md, .chora/memory/AGENTS.md, etc.)
**Timeline**: v1.9.3 is final release before v2.0.0 refactoring

### Why docs/upgrades/ for Upgrade Guides?

**Rationale**: Centralized upgrade documentation, easy discovery, consistent structure
**Previous Mistake**: v1.9.0-to-v1.9.1 and v1.9.1-to-v1.9.2 were placed in repo root (lacked this AGENTS.md)
**Fix**: Moved to `docs/upgrades/` in v1.9.3 release

---

## Common Pitfalls & Prevention

### Pitfall 1: Misplaced Files

**Problem**: Placing files in wrong location (e.g., upgrade docs in repo root)
**Prevention**: Follow "File Organization Conventions" section above
**Detection**: Review `git status` before commit, check against conventions

### Pitfall 2: Forgetting Template Metadata

**Problem**: Creating blueprint files without required metadata or helper comments
**Prevention**: Follow blueprint conventions (header comments, clear placeholder instructions)
**Detection**: Run blueprint lint scripts or manual review before committing

### Pitfall 3: Breaking Conditional Logic

**Problem**: Adding `{% if ... %}` without updating supporting install scripts or awareness docs
**Prevention**: Test with feature on AND off via `python setup.py`; update SAP adoption blueprint accordingly
**Detection**: Generate project with feature disabled, verify files excluded and docs consistent

### Pitfall 4: Stale Examples

**Problem**: Example projects lag behind template changes
**Prevention**: Document in commit message: "Note: examples/ not updated (drift expected)"
**Detection**: Periodically regenerate examples using `python setup.py` and compare to current blueprint outputs

### Pitfall 5: Incomplete Upgrade Guides

**Problem**: Missing sections in upgrade guide (no rollback, no testing)
**Prevention**: Use `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md` as checklist
**Detection**: Review against template before committing

### Pitfall 6: Version Number Errors

**Problem**: Tagging wrong version or skipping version in CHANGELOG
**Prevention**: Update CHANGELOG first, then tag with matching version
**Detection**: `git log --oneline` and `git tag -l` should align

---

## Integration Points

### Blueprint Engine

**Tooling**: `setup.py` interactive generator (can be wrapped by automation scripts)
**Key Files**: `static-template/`, technology-specific SAP templates, `docs/skilled-awareness/`

### Generated Projects

**Update Mechanism**: Follow capability-specific SAP adoption blueprints and ledger guidance
**Configuration**: Project metadata stored in generated files (`pyproject.toml`, `AGENTS.md`, etc.); no `.copier-answers.yml`
**Merge Strategy**: Manual or scripted merge guided by SAP protocols (e.g., apply blueprint diffs, run tests, update docs)

### GitHub Actions

**Workflows**: Template includes 7+ CI/CD workflows in `template/.github/workflows/`
**Secrets Required**: `PYPI_TOKEN` (if PyPI publishing enabled)
**Dependabot**: Auto-merge workflow for dependency updates

### Docker

**Optional Feature**: `include_docker=true`
**Strategies**: `production` (multi-stage + compose) or `ci-only` (Dockerfile.test only)
**Integration**: justfile commands (`docker-build`, `docker-test`, etc.)

---

## Memory System (A-MEM) - SAP-010

**When to use SAP-010**:
- Capturing learnings, insights, or patterns discovered during work for reuse in future sessions
- Querying event logs to restore context after breaks (hours, days, or weeks between sessions)
- Logging significant events (milestones, decisions, errors) for audit trails
- Building knowledge graph with wikilink connections to relate discoveries
- Tracking agent behavior patterns and learned approaches across sessions

**Quick-start approach** (recommended):
```bash
# Work in memory system domain
cd .chora/

# Read domain-specific guidance (60-70% token savings vs root files)
cat AGENTS.md        # Generic memory patterns (13-min read)
cat CLAUDE.md        # Claude-specific workflows (8-min read)

# Log an event
echo '{"event_type":"learning_captured","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","data":{"pattern":"test-pattern"}}' >> memory/events/development.jsonl

# Create knowledge note
cp memory/knowledge/templates/default.md memory/knowledge/notes/my-pattern.md

# Query event logs
tail -n 20 memory/events/*.jsonl

# Check system health
python ../scripts/memory-health-check.py
```

**What you get**:
- **Event logging**: JSONL-format logs with trace correlation (CHORA_TRACE_ID), structured metadata, microsecond timestamps
- **Knowledge notes**: Markdown with YAML frontmatter, Zettelkasten wikilinks (`[[note-name]]`), confidence ratings (0.0-1.0)
- **Agent profiles**: YAML files capturing learned patterns, preferences, historical behavior
- **Query templates**: Reusable queries in `.chora/memory/queries/` for common analysis patterns
- **Nested awareness**: Domain-specific [.chora/AGENTS.md](.chora/AGENTS.md) and [.chora/CLAUDE.md](.chora/CLAUDE.md) for progressive context loading

**Example workflow**:
```bash
# Scenario: Capture learning from completed task integration

# 1. Complete task (SAP-015 beads)
bd close task-123 --reason "Implemented async error handling pattern"

# 2. Extract pattern → knowledge note
cp .chora/memory/knowledge/templates/default.md .chora/memory/knowledge/notes/async-error-handling.md
# Edit note: Document pattern, add wikilinks to related notes

# 3. Log learning event
echo '{"event_type":"learning_captured","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","data":{"task_id":"task-123","pattern":"async-error-handling","confidence":0.9}}' >> .chora/memory/events/development.jsonl

# 4. Link to related knowledge
# In note, add: [[error-handling-patterns]] [[async-best-practices]]

# 5. Later: Query for context restoration (new session)
grep "async-error" .chora/memory/events/development.jsonl
ls -lt .chora/memory/knowledge/notes/*.md | head -10

# Result: Pattern available for future tasks, context restored in <2 minutes
```

**Nested awareness guides**:
- [.chora/AGENTS.md](.chora/AGENTS.md) - Memory system patterns (13-min read, ~10k tokens)
- [.chora/CLAUDE.md](.chora/CLAUDE.md) - Claude workflows (8-min read, ~5k tokens)
- **Progressive loading**: Load only what you need (60-70% token savings vs loading full root AGENTS.md)

**Integration with other SAPs**:
- **SAP-001 (Inbox)**: Coordination request received → Log event in `events/inbox.jsonl`
- **SAP-015 (Task Tracking)**: Task completed → Create knowledge note with learnings
- **SAP-012 (Planning)**: Sprint retrospective → Distill insights to knowledge graph
- **SAP-009 (Awareness)**: Uses nested AGENTS.md/CLAUDE.md pattern for domain-specific guidance

**Documentation**:
- Domain guides: [.chora/AGENTS.md](.chora/AGENTS.md), [.chora/CLAUDE.md](.chora/CLAUDE.md)
- Protocol specification: [docs/skilled-awareness/memory-system/protocol-spec.md](docs/skilled-awareness/memory-system/protocol-spec.md)
- Adoption blueprint: [docs/skilled-awareness/memory-system/adoption-blueprint.md](docs/skilled-awareness/memory-system/adoption-blueprint.md)

**ROI**: 5-15 minutes saved per session via context restoration, 40-48 hours saved annually for active agents

**Note**: chora-base template repository itself does not use memory system (no `.chora/` directory in template repo). Memory system is included in generated projects when `include_memory_system=true`.

---

## Task Tracking (Beads) - SAP-015

**Status**: Pilot (v1.0.0) | **Adoption Level**: L0 (Available for installation)

SAP-015 provides persistent task tracking using `.beads/issues.jsonl` for cross-session context restoration. Eliminates work loss between Claude Code sessions by maintaining git-committed task state.

**Quick-start approach**:
```bash
# Domain-specific awareness files (if SAP-015 adopted in your project)
cd .beads/
cat AGENTS.md  # 10-min read: Beads workflow patterns
cat CLAUDE.md  # 7-min read: Claude-specific beads usage

# Alternative: Read full protocol specification
cat docs/skilled-awareness/task-tracking/protocol-spec.md  # 25-min read
```

**When to use SAP-015**:
- **Session startup**: Restore context from previous session (<2 min vs 5-10 min manual)
- **Multi-session work**: Track progress across multiple Claude Code sessions
- **Backlog management**: Prioritize tasks with dependencies and blockers
- **Audit trails**: Document completion reasons and link artifacts
- **Team coordination**: Share task state with other agents or humans

**Core CLI commands**:
```bash
# Session startup: Find unblocked work
bd ready --json                              # Programmatic (Claude Code)
bd ready                                     # Human-readable

# Claim task
bd update task-123 --status in_progress --assignee "claude-code"

# Add notes during work
bd update task-123 --notes "Implemented async error handling, tests passing"

# Complete task
bd close task-123 --reason "Feature implemented, tested, and documented"

# Query by status
bd list --status open --json                 # Open backlog
bd list --status in_progress --json          # Active work
bd list --status blocked --json              # Blocked tasks
bd list --status closed --json --limit 10   # Recent completions

# Query by assignee
bd list --assignee "claude-code" --json      # All Claude Code tasks
```

**Example workflow (multi-session coordination)**:
```bash
# Session 1: Start feature work
bd create --title "Implement user authentication" \
  --description "Add JWT-based auth with refresh tokens" \
  --priority high \
  --tags "feature,auth,security"

bd update task-456 --status in_progress --assignee "claude-code"

# Mid-session: Discover blocker
bd update task-456 --status blocked \
  --blockers "Waiting for API key from DevOps team" \
  --notes "Auth flow implemented, needs production API key for testing"

# Session 2 (next day): Check ready tasks
bd ready --json
# Output: [] (task-456 still blocked)

bd list --status blocked --json
# Output: Shows task-456 with blocker reason

# Session 3 (API key received): Resume work
bd update task-456 --status in_progress \
  --notes "API key received, testing auth flow"

# Complete task
bd close task-456 \
  --reason "Auth implemented, tested with production API, docs updated" \
  --artifacts "src/auth.py,tests/test_auth.py,docs/authentication.md"
```

**Task data structure**:
```json
{
  "id": "task-456",
  "title": "Implement user authentication",
  "description": "Add JWT-based auth with refresh tokens",
  "status": "closed",
  "priority": "high",
  "assignee": "claude-code",
  "tags": ["feature", "auth", "security"],
  "created": "2025-11-09T10:30:00Z",
  "updated": "2025-11-09T16:45:00Z",
  "closed": "2025-11-09T16:45:00Z",
  "blockers": [],
  "dependencies": [],
  "notes": "API key received, testing auth flow",
  "completion_reason": "Auth implemented, tested with production API, docs updated",
  "artifacts": ["src/auth.py", "tests/test_auth.py", "docs/authentication.md"]
}
```

**Integration with other SAPs**:
- **SAP-001 (Inbox)**: Coordination request → Decompose into beads tasks
  ```bash
  # Receive coordination request
  cat inbox/incoming/coordination/COORD-2025-042.md

  # Create tasks from coordination request
  bd create --title "Task 1 from COORD-2025-042" --tags "coordination,COORD-2025-042"
  bd create --title "Task 2 from COORD-2025-042" --tags "coordination,COORD-2025-042"
  ```

- **SAP-010 (Memory)**: Task completed → Extract learnings to knowledge notes
  ```bash
  # Complete task
  bd close task-789 --reason "Implemented async error handling pattern"

  # Extract pattern to knowledge note
  cp .chora/memory/knowledge/templates/default.md \
     .chora/memory/knowledge/notes/async-error-handling.md

  # Log learning event
  echo '{"event_type":"learning_captured","task_id":"task-789"}' >> \
    .chora/memory/events/development.jsonl
  ```

- **SAP-005 (CI/CD)**: CI failure → Create bead to track fix
  ```bash
  # CI failure detected
  bd create --title "Fix CI test failure in test_api.py" \
    --priority urgent \
    --tags "ci,bug,test-failure"
  ```

**Nested awareness guides**:
- [.beads/AGENTS.md](.beads/AGENTS.md) - Beads workflow patterns (10-min read, ~8k tokens)
- [.beads/CLAUDE.md](.beads/CLAUDE.md) - Claude beads workflows (7-min read, ~5k tokens)
- **Progressive loading**: Load only what you need (60-70% token savings)

**Documentation**:
- Protocol specification: [docs/skilled-awareness/task-tracking/protocol-spec.md](docs/skilled-awareness/task-tracking/protocol-spec.md)
- Adoption blueprint: [docs/skilled-awareness/task-tracking/adoption-blueprint.md](docs/skilled-awareness/task-tracking/adoption-blueprint.md)
- CLI reference: `bd --help` or see protocol-spec.md Section 3

**ROI**: 5-10 minutes saved per session via context restoration, 40-80 hours saved annually for active projects

**Note**: chora-base template repository does not use beads (no `.beads/` directory in template repo). Beads is included in generated projects when adopted.

---

## SAP Evaluation Workflow

### Purpose

SAP-019 (Self-Evaluation) enables you to assess SAP adoption depth, identify gaps, and generate improvement roadmaps.

### When to Evaluate

- **After installing new SAP**: Validate installation (`--quick`)
- **Sprint planning**: Generate roadmap for next sprint (`--strategic`)
- **User asks "How's our SAP adoption?"**: Quick status check
- **User asks "How can we improve SAP-X?"**: Deep dive analysis
- **Quarterly reviews**: Track progress over time

### Evaluation Modes

**Quick Check** (30 seconds):
```bash
# Check all installed SAPs
python scripts/sap-evaluator.py --quick

# Check specific SAP
python scripts/sap-evaluator.py --quick SAP-004
```

**Deep Dive** (5 minutes):
```bash
# Analyze specific SAP, save report
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
```

**Strategic Analysis** (30 minutes):
```bash
# Generate quarterly roadmap
python scripts/sap-evaluator.py --strategic --output docs/adoption-reports/sap-roadmap.yaml
```

### Common Workflow: "How can we improve SAP-X?"

1. **Run deep dive**:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
   ```

2. **Read report** (use Read tool):
   ```
   Read: docs/adoption-reports/SAP-004-assessment.md
   ```

3. **Extract top 3 gaps** from report:
   - Gap 1 (P0): [Title], [Impact], [Effort], [Actions]
   - Gap 2 (P1): [...]
   - Gap 3 (P2): [...]

4. **Present to user**:
   ```markdown
   ## SAP-004 Improvement Opportunities

   **Current Level**: 1 (Basic)
   **Next Milestone**: Level 2

   ### Priority Gaps
   1. **[Gap 1 Title]** (P0, 3 hours)
      - Impact: [description]
      - Actions: [concrete steps]

   2. **[Gap 2 Title]** (P1, 1.5 hours)
      - Impact: [description]
      - Actions: [concrete steps]

   Shall I create tasks and implement Gap 1?
   ```

5. **Offer to execute**: If user agrees, use TodoWrite to create tasks, then implement

### Report Structure

Generated reports include:
- **Current State**: Adoption level, completion %, next milestone
- **Validation Results**: Automated checks (✅/❌)
- **Gap Analysis**: Prioritized gaps (P0/P1/P2) with concrete actions
- **Sprint Plan**: This sprint focus, next sprint goals

Example gap:
```
### Gap 1: Test coverage 0% < 85% target (P0)
**Impact**: High - Blocks SAP-005 CI/CD coverage gates
**Effort**: Medium - 3 hours, 8 tests needed
**Actions**:
1. Generate coverage report (5 min)
2. Write 8 tests for API handlers (2.5 hours)
3. Validate ≥85% coverage (2 min)
```

### Integration with Sprint Planning

**Sprint Planning Workflow**:
1. Run strategic analysis to generate roadmap
2. Review priority gaps (top 5)
3. Select 1-2 gaps for current sprint
4. Add to sprint backlog with time estimates
5. Track progress via re-evaluation at sprint end

**Quarterly Review**:
1. Generate strategic roadmap
2. Compare to previous quarter
3. Calculate adoption velocity
4. Update quarterly goals

### Tips for AI Agents

- **Start with quick check**: Don't deep dive unless user asks
- **Focus on top 3 gaps**: Don't overwhelm with full list
- **Prioritize P0 gaps**: These block other SAPs
- **Be specific**: Reference exact commands, files, line numbers from reports
- **Track progress**: Re-run evaluation after implementing improvements

---

## Bidirectional Translation Layer (Mutual Ergonomics)

### Overview

**Purpose**: Enable natural conversational interaction while executing procedurally within the ecosystem ontology.

**Core Principle**: Meet users where they are. You adapt to their communication style; they don't need to memorize exact commands.

### Tools Available

#### 1. Intent Router (`scripts/intent-router.py`)

Translates natural language to formal actions with confidence scoring.

**Usage**:
```python
from intent_router import IntentRouter

router = IntentRouter("docs/dev-docs/patterns/INTENT_PATTERNS.yaml")
matches = router.route(user_input)

if matches and matches[0].confidence >= 0.7:
    # High confidence: execute
    action = matches[0].action
    execute_action(action, matches[0].parameters)
elif matches and matches[0].confidence >= 0.5:
    # Medium confidence: ask for clarification
    clarify_with_user(matches[0])
else:
    # Low confidence: show alternatives
    show_alternatives(matches[:3])
```

**Common Patterns**:
- "show inbox" → `run_inbox_status`
- "how are saps" → `run_sap_evaluator_quick`
- "i want to suggest a big change" → `create_strategic_proposal`
- "review coordination requests" → `review_coordination_requests`

**Pattern Learning**: When user says something repeatedly that maps successfully, add it to triggers.

#### 2. Glossary Search (`scripts/chora-search.py`)

Enables terminology discovery and reverse lookup.

**Usage**:
```bash
# Forward lookup: term → definition
python scripts/chora-search.py "coordination request"

# Reverse lookup: description → term
python scripts/chora-search.py --reverse "I want to suggest a big change"
# Returns: Strategic Proposal (95% confidence)

# Fuzzy matching: handles typos
python scripts/chora-search.py --fuzzy "coordenation"
```

**When to Use**:
- User asks "What is X?"
- User uses unfamiliar terminology
- User describes concept without using correct term
- User makes typos

#### 3. User Preferences (`.chora/user-preferences.yaml`)

Adapt behavior based on user working style.

**Key Preferences**:
- `verbosity`: concise | standard | verbose
- `formality`: casual | standard | formal
- `output_format`: terminal | markdown | json
- `require_confirmation`: always | destructive | never
- `progressive_disclosure`: true | false

**Loading**:
```python
import yaml
from pathlib import Path

prefs_file = Path(".chora/user-preferences.yaml")
if prefs_file.exists():
    with open(prefs_file) as f:
        prefs = yaml.safe_load(f)

    # Adapt verbosity
    if prefs["communication"]["verbosity"] == "concise":
        return brief_summary()
    elif prefs["communication"]["verbosity"] == "verbose":
        return detailed_report()
```

#### 4. Suggestion Engine (`scripts/suggest-next.py`)

Context-aware next action recommendations.

**Usage**:
```bash
# When user asks "what next?" or "what should I do?"
python scripts/suggest-next.py

# Proactive mode (high-priority suggestions only)
python scripts/suggest-next.py --mode proactive
```

**Context Signals**:
- Recent events (last 24 hours)
- Active work items (inbox/active/)
- Current phase (DDD/BDD/TDD detection)
- Quality metrics (coverage, tests, lint)
- Inbox backlog

### Communication Patterns

#### Pattern 1: Natural Input → Execution → Result

**Don't explain what you'll do, show what you did**:

```
❌ Bad:
User: "Create coordination request for traceability"
Agent: "To create a coordination request, you should:
       1. Create JSON in inbox/incoming/coordination/
       2. Use schema from inbox/schemas/
       3. ..."

✅ Good:
User: "Create coordination request for traceability"
Agent: ✅ Created coord-007-traceability-pilot.json
       ✅ Logged event: coordination_request_created
       Next: Submit for sprint planning (2025-11-15)?
```

#### Pattern 2: Progressive Formalization

Move from casual → formal as needed:

```
"I want to add health monitoring" (casual)
  → Strategic Proposal (semi-formal artifact)
  → RFC (formal discussion)
  → ADR (formal decision)
  → Coordination Request (fully formal)
  → Implementation (procedural)
```

#### Pattern 3: Adaptive Output

Match user preferences:

```python
# Concise user
"✅ 12 SAPs installed. Top gap: coverage 60%"

# Verbose user
"""
SAP Adoption Status
===================
- 12/18 SAPs installed (67%)
- Level 2: SAP-004, SAP-019
- Top gap: Test coverage at 60% (need 85%)
  Action: Add 45 tests, est. 4-6 hours
"""
```

#### Pattern 4: Context Retention

Remember conversation context:

```
User: "Show inbox"
Agent: [Shows 3 coordination requests]

User: "Review the first one"
Agent: [Recognizes "first one" = coord-003]
       [Shows coord-003 details]
```

### Anti-Patterns (Avoid These)

❌ **Forcing Exact Syntax**: "Command not recognized" when user says "show me the inbox"
❌ **Explaining Instead of Executing**: Long explanations of what to do instead of doing it
❌ **Ignoring Preferences**: Always verbose output even when user wants concise
❌ **No Context**: Asking "what do you mean by 'it'?" when referent is clear
❌ **Static Patterns**: Never learning new phrases user repeats successfully

### Learning & Adaptation

**Pattern Learning**:
- User says "what's cooking in the inbox?" 3+ times
- Intent router matches to `inbox_status` successfully
- Automatically add "what's cooking" to triggers
- Future queries: instant recognition

**Preference Evolution**:
- User says "too much detail" → Update `verbosity: concise`
- User repeatedly cancels confirmations → Suggest `require_confirmation: destructive`
- Track which features user uses → Recommend relevant SAPs

**Expertise Tracking**:
- User has used coordination requests 10+ times
- Next time: Brief reminder instead of full explanation
- Adapt detail level as user gains expertise

### Integration Points

**See Also**:
- [Bidirectional Communication Pattern Guide](docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md) - Complete pattern documentation
- [Intent Patterns Database](docs/dev-docs/patterns/INTENT_PATTERNS.yaml) - All recognized patterns
- [Glossary](docs/GLOSSARY.md) - Ecosystem terminology (75+ terms)
- [User Preferences Template](.chora/user-preferences.yaml.template) - Configuration options

---

## Inbox Coordination (SAP-001 v1.1.0)

### Session Startup Routine

**Every new session, check inbox for coordination requests**:

```bash
# Visual status dashboard (recommended for human-readable overview)
python scripts/inbox-status.py

# Quick inbox count summary
python scripts/inbox-query.py --count-by-status

# View unacknowledged items (if any)
python scripts/inbox-query.py --incoming --unacknowledged --format summary
```

**Expected Output**:
```
Inbox Status Counts:
  Incoming Coordination: 12
  Incoming Tasks: 0
  Incoming Proposals: 0
  Active: 3
  Completed: 45
  Unacknowledged: 12
```

### Daily Inbox Workflows

#### Morning Routine (2-3 minutes)

1. **Check for new items**:
   ```bash
   python scripts/inbox-query.py --incoming --unacknowledged
   ```

2. **Review high-priority items** (P0, blocks_sprint urgency):
   ```bash
   # View specific request
   python scripts/inbox-query.py --request COORD-2025-XXX --format json
   ```

3. **Acknowledge within SLA** (1 business day, 4 hours for blocks_sprint):
   ```bash
   python scripts/respond-to-coordination.py \
     --request COORD-2025-XXX \
     --status acknowledged \
     --notes "Reviewing - will respond by [date]"
   ```

#### Processing Coordination Requests

**Accept and Start Work**:
```bash
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status accepted \
  --effort "8-12 hours" \
  --timeline "Complete by 2025-11-15" \
  --notes "Starting implementation in current sprint" \
  --move-to-active
```

**Decline with Reason**:
```bash
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status declined \
  --reason "Outside current scope. Recommend proposing for Q1 2026 roadmap."
```

**Check Active Work**:
```bash
python scripts/inbox-query.py --status in_progress
```

### Creating Coordination Requests

**Interactive Mode** (recommended for new users):
```bash
python scripts/generate-coordination-request.py --interactive
```

**Context File Mode** (for AI agents):
```bash
# Create context file
cat > inbox/draft/my-request-context.json << 'EOF'
{
  "title": "Add Feature X to Repository Y",
  "description": "Brief description of what needs to be done",
  "background": "Why this is needed, current state",
  "rationale": "Benefits and justification",
  "priority": "P1",
  "urgency": "next_sprint",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/target-repo"
}
EOF

# Generate request with AI-powered deliverables and acceptance criteria
python scripts/generate-coordination-request.py \
  --context inbox/draft/my-request-context.json \
  --ai-model claude-sonnet-4-5-20250929 \
  --output inbox/draft/my-request.json
```

**Quality**: Generator produces 94.9% quality deliverables and SMART acceptance criteria

### Service Level Agreements (SLAs)

**Response Times by Urgency**:

| Urgency | Acknowledgment | Full Response | When to Use |
|---------|---------------|---------------|-------------|
| `blocks_sprint` | 4 hours | Same day | Blocking current sprint work |
| `next_sprint` | 1 business day | 3 business days | Needed for next sprint |
| `backlog` | 1 business day | 1 week | Non-urgent, future planning |

**SLA Compliance**:
- Check inbox at session startup
- Prioritize `blocks_sprint` items immediately
- Acknowledge all items within 1 business day
- Provide full response within urgency-based timeline

### Ecosystem Coordination

**Repository Status**: Active participant in ecosystem coordination

**Capabilities**:
- **Provides**: Template generation, SAP framework, coordination protocol
- **Receives**: Feature requests, bug reports, integration proposals

**Ecosystem Dashboard**: [inbox/ecosystem/ECOSYSTEM_STATUS.yaml](inbox/ecosystem/ECOSYSTEM_STATUS.yaml)

**Ecosystem Invitations**: See [inbox/ecosystem/invitations/](inbox/ecosystem/invitations/) for pending invitations

### Inbox Status Dashboard

**For generic agents and quick visual overview**:

```bash
# Full visual dashboard (recommended)
python scripts/inbox-status.py

# Detailed view with item listings
python scripts/inbox-status.py --detailed

# JSON export for programmatic access
python scripts/inbox-status.py --format json

# Markdown report for documentation
python scripts/inbox-status.py --format markdown > inbox-report.md

# Filter by priority
python scripts/inbox-status.py --priority P0 --detailed

# Recent activity (last 7 days)
python scripts/inbox-status.py --last 7d
```

**Dashboard Output Includes**:
- 📥 Incoming queue counts (coordination, tasks, context)
- 🔄 Active work items with details
- ⏱️ Recent activity timeline (last 20 events)
- ✅ Recent completions (last 30 days)
- 💡 Summary with actionable counts

**Use Cases**:
- Session startup: Get at-a-glance status
- Generic agent queries: "inbox status" → run this tool
- Status reports: Export markdown for weekly updates
- Priority triage: Filter by P0/P1 for urgent items
- Trace investigation: `--trace-id` to follow request chains

### Troubleshooting

**Issue: "Item not found"**
- Use full filename as request ID: `COORD-2025-XXX-description` not just `COORD-2025-XXX`
- Check file exists: `ls inbox/incoming/coordination/COORD-2025-XXX*`

**Issue: "No items found"**
- Verify working directory: Must run commands from project root
- Check inbox path: `ls inbox/incoming/coordination/`

**Issue: Post-processing error**
- Skip post-processing: Remove `--post-process` flag
- Use custom output: `--output inbox/draft/my-request.json`

### Key Resources

- **Protocol Spec**: [docs/skilled-awareness/inbox/protocol-spec.md](docs/skilled-awareness/inbox/protocol-spec.md) (SAP-001 v1.1.0)
- **Onboarding Guide**: [docs/ECOSYSTEM_ONBOARDING.md](docs/ECOSYSTEM_ONBOARDING.md)
- **Phase 1 Summary**: [docs/PHASE_1_COMPLETION_SUMMARY.md](docs/PHASE_1_COMPLETION_SUMMARY.md)
- **Validation Report**: [docs/PHASE_1_VALIDATION_REPORT.md](docs/PHASE_1_VALIDATION_REPORT.md)
- **v1.1.0 Announcement**: [inbox/ecosystem/announcements/SAP-001-v1.1.0-RELEASE.md](inbox/ecosystem/announcements/SAP-001-v1.1.0-RELEASE.md)

---

## SAP Adoption Quarterly Review

### Overview

**When**: End of each quarter (Q1: March 31, Q2: June 30, Q3: September 30, Q4: December 31)

**Purpose**: Systematically evaluate SAP adoption progress, identify gaps, and plan next quarter's adoption roadmap using SAP-019 (self-evaluation) tools.

**Duration**: 30-60 minutes per quarter

**Outputs**:
- Strategic roadmap YAML (`project-docs/sap-roadmap-QX-YYYY.yaml`)
- Quarterly review markdown (`docs/adoption-reports/QX-YYYY-review.md`)
- Updated adoption history (`adoption-history.jsonl`)

### Process

**Step 1: Generate Strategic Roadmap** (5 minutes)

```bash
python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
```

This analyzes all installed SAPs, identifies gaps, and creates a prioritized roadmap.

**Step 2: Create Review Document** (10 minutes)

```bash
python scripts/sap-evaluator.py --strategic --format markdown --output docs/adoption-reports/Q{X}-{YEAR}-review.md
```

Or manually create review document with:
- Progress since last quarter (SAPs installed, levels achieved)
- Velocity metrics (SAPs/month, level progressions/month)
- Successes and blockers
- Top 5 priority gaps from roadmap

**Step 3: Analyze Progress** (15 minutes)

Compare to previous quarter:
- How many SAPs progressed to higher levels?
- What was the adoption velocity?
- Which gaps were resolved?
- Which gaps remain unresolved (blockers)?

Calculate velocity:
- SAPs adopted per month
- Level progressions per month
- Hours invested vs hours saved (ROI)

**Step 4: Update Goals** (10 minutes)

Based on roadmap and analysis:
- Set targets for next quarter (# of SAPs to L2, # to L3)
- Prioritize 3-5 focus SAPs from roadmap
- Estimate ROI potential from priority gaps
- Identify blockers to address

**Step 5: Commit Review** (5 minutes)

```bash
git add project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
git add docs/adoption-reports/Q{X}-{YEAR}-review.md
git add adoption-history.jsonl  # If manually updated
git commit -m "docs(sap-019): Q{X}-{YEAR} adoption review

- Strategic roadmap generated
- Progress analysis completed
- Next quarter goals set

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Example Review Document Structure

```markdown
# Q4-2025 SAP Adoption Review

**Generated**: 2025-12-31
**Review Period**: October 1 - December 31, 2025

## Progress Summary

### SAPs Adopted
- Total SAPs: 8 (was 6 in Q3)
- New adoptions: SAP-004, SAP-019

### Level Progression
- Level 2: 4 SAPs (was 2 in Q3)
- Level 3: 1 SAP (was 0 in Q3)
- Average level: 1.75 (was 1.33 in Q3)

### Velocity
- SAPs adopted: 0.67/month (2 in 3 months)
- Level progressions: 1.0/month (3 in 3 months)
- Hours invested: 12 hours this quarter

## Successes

1. **SAP-019 to L3**: Self-evaluation operational, strategic roadmaps generated
2. **SAP-004 to L2**: Test coverage improved from 0% to 75%
3. **SAP-013 integration**: ROI tracking now includes SAP adoption

## Blockers

1. **SAP-004 test coverage gap**: Still below 85% target, blocked by missing pytest fixtures
2. **SAP-009 documentation**: No domain-specific AGENTS.md files created yet

## Next Quarter Goals (Q1-2026)

### Targets
- Bring SAP-004 to L3 (complete test coverage to 85%+)
- Adopt 2 new SAPs (SAP-014, SAP-016)
- Achieve 2.0 average adoption level

### Focus SAPs
1. SAP-004 (testing-framework) - Priority P0, blocks sprint
2. SAP-009 (agent-awareness) - Priority P1, improves documentation
3. SAP-014 (mcp-server-development) - Priority P2, enables MCP development

### Estimated ROI
- Hours to invest: 8-10 hours
- Hours to save: 15-20 hours/quarter
- Expected ROI: 1.75x

## Roadmap

See [project-docs/sap-roadmap-Q1-2026.yaml](../project-docs/sap-roadmap-Q1-2026.yaml) for detailed sprint breakdown.
```

### Tips

**Automate Data Collection**:
- `adoption-history.jsonl` tracks all SAP events automatically
- `python scripts/sap-evaluator.py --quick` shows current state
- Compare git history: `git log --since="3 months ago" --grep="sap-"`

**Focus on Value**:
- Prioritize gaps with highest ROI (hours_saved / hours_invested)
- Address blockers first (gaps blocking other gaps)
- Celebrate wins (completed levels, new adoptions)

**Keep It Short**:
- 30-60 minutes maximum
- Use tools to generate data
- Focus on decisions, not documentation

---

## Task Tracking with Beads (SAP-015)

### Overview

SAP-015 provides persistent task tracking for AI agents using [beads](https://github.com/steveyegge/beads), a git-backed issue tracker designed for agent memory across sessions.

**When to use**:
- ✅ Complex features (5+ steps spanning multiple sessions)
- ✅ Tasks with dependencies (what blocks what)
- ✅ Multi-agent coordination
- ✅ Feature decomposition (epics → subtasks)

**Don't use for**:
- ❌ Cross-repo coordination (use SAP-001 inbox)
- ❌ Event history (use SAP-010 A-MEM)
- ❌ Simple single-step tasks

### Quick Reference

**Session Start**:
```bash
bd ready --json                                    # Find unblocked work
bd update {id} --status in_progress --assignee {agent}  # Claim task
bd show {id} --json                                # Get task context
```

**During Work**:
```bash
bd create "Task title" --priority 0                # Add discovered subtask
bd dep add {blocked} {blocker}                     # Link dependency
bd update {parent} --status open                   # Parent now blocked
```

**Session End**:
```bash
bd close {id} --reason "Completed X"               # Mark done
bd ready --json                                    # Check newly-unblocked work
```

**Status Check**:
```bash
bd list --status in_progress --json                # Active tasks
bd dep tree {id}                                   # Visualize dependencies
bd status                                          # Database overview
```

### Integration with Other SAPs

**SAP-001 (Inbox)**:
- Decompose coordination requests into beads tasks
- Create epic for coordination, link subtasks
- See [Pattern H](docs/skilled-awareness/task-tracking/awareness-guide.md#pattern-h-integration-with-inbox-sap-001)

**SAP-010 (A-MEM)**:
- Correlate beads tasks with event traces
- Include trace_id in task description
- Log task events in A-MEM event log
- See [Pattern I](docs/skilled-awareness/task-tracking/awareness-guide.md#pattern-i-integration-with-a-mem-sap-010)

### Full Documentation

- **Adoption Blueprint**: [docs/skilled-awareness/task-tracking/adoption-blueprint.md](docs/skilled-awareness/task-tracking/adoption-blueprint.md)
- **Awareness Guide**: [docs/skilled-awareness/task-tracking/awareness-guide.md](docs/skilled-awareness/task-tracking/awareness-guide.md)
- **Protocol Spec**: [docs/skilled-awareness/task-tracking/protocol-spec.md](docs/skilled-awareness/task-tracking/protocol-spec.md)
- **Capability Charter**: [docs/skilled-awareness/task-tracking/capability-charter.md](docs/skilled-awareness/task-tracking/capability-charter.md)

---

## Questions & Support

### Where to Find Information

**Template configuration**: `docs/reference/template-configuration.md`
**Upgrade philosophy**: `docs/upgrades/PHILOSOPHY.md`
**Version history**: `CHANGELOG.md`
**ROI analysis**: `docs/BENEFITS.md`
**Research**: `docs/research/`

### Where to Report Issues

**GitHub Issues**: https://github.com/liminalcommons/chora-base/issues
**Discussions**: https://github.com/liminalcommons/chora-base/discussions

### Version Information

**Current Version**: v1.9.3 (2025-10-22)
**Next Version**: v2.0.0 (MAJOR - nested AGENTS.md refactoring)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-22 | Initial AGENTS.md for chora-base repository (Phase 2 of v1.9.3 release) |

---

**End of AGENTS.md**

This document is the **source of truth** for AI agents and human developers working on chora-base. When in doubt, refer here first.
