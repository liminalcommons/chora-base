# Development Workflows: chora-base

**Purpose**: Quick reference guide for chora-base development workflows, processes, and automation.

**Navigation**:
- [← Back to root AGENTS.md](../AGENTS.md) - Project overview
- [→ SAPs Quick Reference](../saps/AGENTS.md) - SAP catalog
- [→ Getting Started](../getting-started/AGENTS.md) - Onboarding guide

---

## What's in This File?

This file documents chora-base **development workflows and processes**:

1. **Development Lifecycle** - Adding features, releasing versions, creating upgrade guides
2. **Testing Strategy** - Template generation tests, validation, quality gates
3. **Quality Gates** - Pre-commit hooks, CI/CD validation (SAP-006)
4. **Automation Scripts** - 25 script toolkit, justfile interface (SAP-008)
5. **Documentation Framework** - Diátaxis 4-domain structure, frontmatter validation (SAP-007)
6. **Docker Operations** - Production containerization, multi-stage builds (SAP-011)
7. **File Organization** - Naming conventions, location patterns

For **SAP-specific patterns**, see [saps/AGENTS.md](../saps/AGENTS.md).

---

## Development Lifecycle

### Adding New Features to Template

**5-Phase Workflow**:

```bash
# Phase 1: Research
# - Document findings in docs/research/
# - Review adopter feedback from real projects (mcp-n8n, chora-compose, etc.)
# - Identify industry best practices

# Phase 2: Design
# - Update CHANGELOG.md under ## [Unreleased]
# - Consider opt-in vs opt-out (new features usually opt-in)
# - Determine if feature needs its own SAP
# - Update relevant blueprints and static assets

# Phase 3: Implementation
# - Update static-template/ and blueprints/ assets
# - Add automation or install scripts if optional
# - Run blueprint generation to validate outputs
# - Generate/update examples/ if demonstrating complex feature

# Phase 4: Documentation
# - Update README.md if user-facing
# - Add to template/AGENTS.md.jinja if relevant to AI agents
# - Document in appropriate docs/ subdirectory
# - Update docs/BENEFITS.md if adding measurable value
# - Create/refresh SAP documents (charter, protocol, awareness, blueprint, ledger)

# Phase 5: Validation
# - Generate fresh project using blueprint workflow
cd /tmp/test-validation && ./scripts/setup.sh && pytest
# - Test upgrade path following SAP adoption blueprint
# - Verify conditional combinations (Docker on/off, memory on/off, etc.)
```

**Example**: Adding a new optional feature
```bash
# 1. Research phase
cat docs/research/feature-name.md

# 2. Design phase
vim CHANGELOG.md  # Add to [Unreleased] section

# 3. Implementation phase
vim static-template/src/feature.py
vim blueprints/feature.blueprint

# 4. Documentation phase
vim README.md
vim docs/how-to/use-feature.md

# 5. Validation phase
# Generate test project
cd /tmp/test && ./scripts/setup.sh && pytest
```

---

### Releasing New Version

**Version Numbering**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR** (X.0.0): Breaking changes requiring adopter action
- **MINOR** (1.X.0): New features, additive changes (current: v1.9.3)
- **PATCH** (1.1.X): Bug fixes only

**6-Step Release Process**:

```bash
# Step 1: Pre-Release Validation
# Generate project from blueprints (interactive)
cd /tmp/test-release && ./scripts/setup.sh && pytest

# Test update path (use example project + SAP adoption blueprint)
cd examples/full-featured-with-vision
# Follow relevant SAP adoption blueprint to apply latest changes
./scripts/setup.sh && pytest

# Step 2: Create Upgrade Guide
# Location: docs/upgrades/vX.Y-to-vX.Z.md
# Template: docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md
# Include:
# - Decision tree for AI agents
# - Displacement risk (ZERO/LOW/MEDIUM/HIGH)
# - Migration steps, validation checklist

# Step 3: Update Core Files
# Update CHANGELOG.md
# Change: ## [Unreleased]
# To:     ## [X.Y.Z] - 2025-MM-DD

# Update README.md Recent Updates section
# Add new version entry with key features

# Update docs/upgrades/README.md
# Add version to version-specific guides table

# Step 4: Commit and Tag
git add -A
git commit -m "feat(scope): Brief description (vX.Y.Z)

Detailed changes:
- Feature 1
- Feature 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git tag vX.Y.Z
git push origin main --tags

# Step 5: Create GitHub Release
gh release create vX.Y.Z \
  --title "vX.Y.Z - Brief Title" \
  --notes "Release notes here (benefits, changes, upgrade guide link)"

# Step 6: Update docs/upgrades/README.md
# Update version table with new entry
# Update "Status" line if completing a phase
```

**Example**: Releasing v1.10.0
```bash
# 1. Validate
cd /tmp/test-v1.10.0 && ./scripts/setup.sh && pytest

# 2. Create upgrade guide
cp docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md docs/upgrades/v1.9-to-v1.10.md
vim docs/upgrades/v1.9-to-v1.10.md

# 3. Update core files
vim CHANGELOG.md  # Change [Unreleased] to [1.10.0] - 2025-11-10
vim README.md     # Add v1.10.0 to Recent Updates

# 4. Commit and tag
git add -A
git commit -m "feat(saps): Add 5 new React SAPs (v1.10.0)"
git tag v1.10.0
git push origin main --tags

# 5. GitHub release
gh release create v1.10.0 --title "v1.10.0 - React Excellence" --notes "..."

# 6. Update upgrade docs index
vim docs/upgrades/README.md
```

---

### Creating Upgrade Documentation

**Template**: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`

**7 Required Sections**:

1. **Quick Assessment** (TL;DR, effort estimate)
2. **Decision Tree for AI Agents** (structured IF/THEN)
3. **What Changed** (file-by-file with line counts)
4. **Migration Steps** (bash commands)
5. **Testing After Upgrade** (validation checklist)
6. **Rollback Instructions**
7. **FAQ**

**AI-Optimized Format**:
- Machine-parseable decision criteria
- Clear displacement risk assessment (ZERO/LOW/MEDIUM/HIGH)
- Structured upgrade effort estimate (<10min, 10-20min, 1-2hrs, etc.)
- Benefits vs costs analysis for optional changes

**Example**: Upgrade guide structure
```markdown
# Upgrade Guide: v1.9 to v1.10

## Quick Assessment

**TL;DR**: 5 new React SAPs added, 16 total now available. No breaking changes.

**Effort**: <10 minutes (minimal, opt-in only)
**Displacement Risk**: ZERO (purely additive)
**Benefits**: 89.8% time savings for React development

## Decision Tree for AI Agents

IF project uses React THEN:
  RECOMMEND: Adopt foundation stack (SAP-020, SAP-033, SAP-034, SAP-041)
  EFFORT: 30 minutes
  BENEFIT: Production-ready auth + database + forms
ELSE:
  SKIP: No action needed

## What Changed

- Added: docs/skilled-awareness/react-foundation/ (1,500 lines)
- Added: docs/skilled-awareness/react-authentication/ (1,800 lines)
- Added: 3 more React SAPs
- Updated: sap-catalog.json (5 new entries)

## Migration Steps

\```bash
# No migration needed (purely additive)
# To adopt React SAPs:
cd docs/skilled-awareness/react-foundation/
cat adoption-blueprint.md
\```

## Testing After Upgrade

- [ ] Verify sap-catalog.json has 16 React SAPs
- [ ] Check docs/skilled-awareness/react-foundation/ exists
- [ ] Run: just list-saps | grep react

## Rollback Instructions

\```bash
git checkout v1.9.3
\```

## FAQ

**Q**: Do existing projects need updates?
**A**: No, purely additive. Adopt React SAPs only if using React.
```

---

## Testing Strategy

### Template Generation Tests

**3 Test Configurations**:

```bash
# 1. Minimal configuration (accept defaults)
# Use AI agent to generate from static-template/ and SAP templates

# 2. Full-featured configuration
# Use AI agent to generate from static-template/ and SAP templates
# Enable all optional features when prompted

# 3. Specific project types (MCP, CLI, library)
# Use AI agent to generate from static-template/ and SAP templates
# Choose appropriate options for project type
```

**Example**: Generating test projects
```bash
# Minimal project
python scripts/create-model-mcp-server.py \
  --name "Minimal Test" \
  --namespace mintest \
  --output /tmp/minimal

# Full-featured project
python scripts/create-model-mcp-server.py \
  --name "Full Featured Test" \
  --namespace fulltest \
  --output /tmp/full
# Enable all optional features when prompted
```

---

### Generated Project Validation

**4-Step Validation**:

```bash
# Step 1: Navigate to generated project
cd /tmp/test-project

# Step 2: Run setup script
./scripts/setup.sh

# Step 3: Run tests
pytest

# Step 4: Verify quality gates
pre-commit run --all-files
just test  # if justfile included
```

**Example**: Validating generated project
```bash
cd /tmp/weather-mcp
./scripts/setup.sh  # Install dependencies, setup pre-commit
pytest              # Should pass 100%
just test           # Should pass with 85%+ coverage
just pre-merge      # Should pass all quality gates
```

---

### Update Path Testing

**Test template updates merge correctly**:

```bash
# Use example project to test update path
cd examples/full-featured-with-vision
git checkout -b test-update

# Apply latest blueprint changes manually or via automation scripts
# Resolve any conflicts and verify diff is reasonable

# Test that updated project still works
./scripts/setup.sh
pytest
```

**Example**: Testing update path
```bash
cd examples/full-featured-with-vision
git checkout -b test-v1.10-update

# Apply changes (follow upgrade guide)
cp ../static-template/new-feature.py src/

# Validate
pytest
just pre-merge
```

---

### Conditional Feature Testing

**Test feature combinations**:

1. **Minimal Python Project**: Basic structure, no optional features
2. **Full-Featured Python Project**: All optional features enabled
3. **Library Project**: No CLI, yes docs, yes tests
4. **CLI Tool Project**: Yes CLI, yes tests
5. **MCP Server** (with SAP-014): MCP-specific features, optional memory/Docker

**Example**: Testing combinations
```bash
# Test minimal project (no optional features)
python scripts/create-model-mcp-server.py \
  --name "Minimal" --namespace min --output /tmp/min
cd /tmp/min && pytest

# Test full-featured project (all optional features)
python scripts/create-model-mcp-server.py \
  --name "Full" --namespace full --output /tmp/full
# Enable all features when prompted
cd /tmp/full && pytest
```

---

## Quality Gates (SAP-006)

**Purpose**: Automated code quality enforcement via pre-commit hooks (ruff, mypy, black), catching 95%+ preventable issues locally before CI.

**Adoption Level**: L3 (Fully automated, production-ready)

### Core Quality Gates

- **ruff**: Fast Python linting (10-100x faster than flake8)
- **mypy**: Static type checking (catch type errors pre-runtime)
- **black**: Automated code formatting (consistent style)
- **trailing-whitespace**: Remove trailing whitespace
- **end-of-file-fixer**: Ensure files end with newline

### Hook Execution Flow

```bash
# 1. Stage files
git add file.py

# 2. Attempt commit
git commit -m "Add feature"

# 3. Pre-commit hooks run automatically (in order):
#    a. ruff check (linting)
#    b. mypy (type checking)
#    c. black (formatting)
#    d. trailing-whitespace
#    e. end-of-file-fixer

# 4a. If hooks pass → Commit succeeds
# 4b. If hooks fail → Commit blocked, files modified, re-stage and retry

# 5. Re-stage modified files (if hooks auto-fixed)
git add file.py
git commit -m "Add feature"  # Try again
```

### Session Startup Routine

```bash
# 1. Verify pre-commit is installed
pre-commit --version || pip install pre-commit

# 2. Install hooks (if not already installed)
pre-commit install

# 3. Run hooks on all files to check status
pre-commit run --all-files
just pre-commit-all

# 4. Fix any issues reported
ruff check --fix src/ tests/ scripts/
just lint-fix

# 5. Verify type checking passes
mypy src/ tests/ scripts/
just typecheck
```

### Common Workflows

**Workflow 1: Normal commit (hooks pass)**:
```bash
# Make changes
vim src/module.py

# Stage and commit
git add src/module.py
git commit -m "Add feature"  # Hooks run, pass, commit succeeds
```

**Workflow 2: Hooks fail (linting errors)**:
```bash
# Make changes
vim src/module.py

# Stage and commit
git add src/module.py
git commit -m "Add feature"  # Hooks fail with linting errors

# Fix linting automatically
ruff check --fix src/module.py
just lint-fix

# Re-stage and commit
git add src/module.py
git commit -m "Add feature"  # Hooks pass, commit succeeds
```

**Workflow 3: Hooks fail (type errors)**:
```bash
# Make changes
vim src/module.py

# Stage and commit
git add src/module.py
git commit -m "Add feature"  # Hooks fail with type errors

# Fix type errors manually
vim src/module.py  # Add type annotations

# Re-stage and commit
git add src/module.py
git commit -m "Add feature"  # Hooks pass, commit succeeds
```

**Workflow 4: Emergency bypass (NOT recommended)**:
```bash
# Only use in emergency (hotfix, urgent production issue)
git commit -m "Hotfix" --no-verify  # Skip hooks

# Create follow-up task to fix quality issues
bd create "Fix quality issues from emergency commit" --priority high
```

### Hook Configuration

**File**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

### Integration with Other SAPs

- **SAP-005 (CI/CD)**: Dual validation (pre-commit local + CI remote)
  - Pre-commit: Fast (<5s), runs on every commit
  - CI: Comprehensive (matrix testing), runs on push/PR
  - Pattern: Pre-commit catches 95%+ issues, CI catches edge cases

- **SAP-004 (Testing)**: Optional pytest hook
  ```yaml
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
  ```

- **SAP-031 (Enforcement)**: Pre-commit as Layer 2 enforcement
  - Layer 1: Discoverability (70% prevention via patterns in AGENTS.md)
  - Layer 2: Pre-commit hooks (20% prevention via automated checks)
  - Layer 3: CI/CD (9% prevention via comprehensive testing)

### Troubleshooting

**1. Hooks not running**:
```bash
# Re-install hooks
pre-commit uninstall
pre-commit install
```

**2. Hooks failing after update**:
```bash
# Update hook versions
pre-commit autoupdate
just pre-commit-update
```

**3. Ruff linting errors**:
```bash
# Auto-fix fixable issues
ruff check --fix src/ tests/ scripts/
just lint-fix

# Manual fix required for complex issues
ruff check src/ tests/ scripts/  # See error details
```

**4. Mypy type errors**:
```bash
# Run mypy to see errors
mypy src/ tests/ scripts/
just typecheck

# Add type annotations or suppressions
# Example: # type: ignore[arg-type]
```

### ROI Metrics

- **Issue prevention**: 95%+ preventable issues caught locally
- **Time savings**: <5s local checks vs 5-10 min CI failure cycle
- **CI cost reduction**: 90% fewer CI failures (avoid wasted CI minutes)
- **Code quality**: Consistent style, type safety, reduced bugs

**Documentation**:
- Protocol: [docs/skilled-awareness/quality-gates/protocol-spec.md](../docs/skilled-awareness/quality-gates/protocol-spec.md)
- Adoption: [docs/skilled-awareness/quality-gates/adoption-blueprint.md](../docs/skilled-awareness/quality-gates/adoption-blueprint.md)
- Config: [.pre-commit-config.yaml](../.pre-commit-config.yaml)

---

## Automation Scripts (SAP-008)

**Purpose**: Provide 25 automation scripts (shell + Python) organized in 8 categories with justfile unified interface, idempotent operations, and safety contracts.

**Adoption Level**: L1 (Fully operational)

### 8 Script Categories

```bash
scripts/
├── Category 1: Setup & Environment
│   ├── setup.sh, venv-create.sh, venv-clean.sh, check-env.sh
├── Category 2: Development Workflows
│   ├── dev-server.sh, smoke-test.sh, integration-test.sh, diagnose.sh
├── Category 3: Version Management
│   ├── bump-version.sh, prepare-release.sh
├── Category 4: Release & Publishing
│   ├── build-dist.sh, publish-test.sh, publish-prod.sh, verify-stable.sh
├── Category 5: Safety & Recovery
│   ├── rollback-dev.sh, pre-merge.sh
├── Category 6: Documentation
│   ├── validate_docs.py, extract_tests.py, docs_metrics.py
├── Category 7: MCP & Specialized
│   ├── mcp-tool.sh, validate_mcp_names.py
└── Category 8: Migration & Handoff
    ├── migrate_namespace.sh, handoff.sh
```

### Session Startup Routine

```bash
# 1. Check available automation commands
just automation-help                # Show all 30+ commands grouped by category
just --list                         # Show all commands

# 2. Validate environment
just check-env                      # Check prerequisites (Python, Git, etc.)
just diagnose                       # Run diagnostics if issues found

# 3. Run quick health check
just smoke                          # Quick smoke tests (~5-10s)
```

### Common Workflows

**1. Setup new development environment**:
```bash
# Install project in editable mode
just install                        # pip install -e ".[dev]"

# Install pre-commit hooks
just setup-hooks                    # pre-commit install

# Validate environment
just check-env                      # Check Python, Git, dependencies

# Run smoke tests
just smoke                          # Quick validation (<10s)
```

**2. Development workflow (test → lint → format → type-check)**:
```bash
# Run tests with coverage
just test                           # pytest with coverage report

# Lint code
just lint                           # ruff check (find issues)
just lint-fix                       # ruff check --fix (auto-fix)

# Format code
just format                         # ruff format

# Type checking
just type-check                     # mypy static analysis

# All quality gates before merge
just pre-merge                      # Run all checks (test + lint + format + type-check)
```

**3. Version bump and release**:
```bash
# Bump version (semver)
just bump-patch                     # 1.0.0 → 1.0.1 (bug fixes)
just bump-minor                     # 1.0.0 → 1.1.0 (new features)
just bump-major                     # 1.0.0 → 2.0.0 (breaking changes)

# Build distribution packages
just build                          # Build wheel and sdist

# Publish to test PyPI (validate first)
just publish-test                   # Publish to test.pypi.org

# Publish to production PyPI
just publish-prod                   # Publish to pypi.org
```

**4. Documentation workflows**:
```bash
# Validate documentation standards
just validate-docs                  # Run DOCUMENTATION_STANDARD.md checks

# Validate frontmatter schema
just validate-frontmatter           # Check YAML frontmatter

# Extract tests from how-to guides
just extract-doc-tests              # Generate tests from code blocks

# Show documentation structure
just doc-structure                  # Display Diátaxis 4-domain hierarchy

# Check completeness
just doc-completeness               # Verify all 4 domains exist
```

**5. Safety and recovery**:
```bash
# Run all pre-merge quality gates
just pre-merge                      # Test + lint + format + type-check

# Generate handoff checklist
just handoff                        # Create handoff report

# Rollback development changes (if needed)
just rollback-dev                   # Restore to clean state
```

**6. Diagnostics and troubleshooting**:
```bash
# Diagnose environment issues
just diagnose                       # Run comprehensive diagnostics

# Check specific prerequisites
just check-env                      # Validate Python, Git, dependencies

# Run smoke tests
just smoke                          # Quick health check

# Run integration tests
just integration                    # Full integration test suite
```

### Integration with Other SAPs

- **SAP-012 (Python Patterns)**: Scripts follow Python best practices
- **SAP-006 (Quality Gates)**: `just pre-merge` orchestrates all gates
- **SAP-005 (CI/CD)**: Scripts power GitHub Actions workflows
- **SAP-007 (Documentation)**: Documentation scripts validate Diátaxis
- **SAP-014 (MCP Server)**: MCP-specific automation scripts

### ROI Metrics

- **Time savings**: 30-45 min per day (consistent automation)
- **Error reduction**: 90%+ reduction in setup errors
- **Consistency**: 100% standardized workflows
- **Discoverability**: `just automation-help` provides instant reference

---

## Documentation Framework (SAP-007)

**Purpose**: Provide Diátaxis-based documentation architecture with frontmatter validation, executable how-to guides, and Level 3 enforcement layer.

**Adoption Level**: L3 (Fully enforced via pre-commit hooks and CI)

### Diátaxis 4-Domain Structure

```bash
docs/
├── user-docs/
│   ├── tutorials/        # Learning-oriented (step-by-step lessons)
│   ├── how-to/           # Task-oriented (practical guides)
│   ├── explanation/      # Understanding-oriented (concepts, design rationale)
│   └── reference/        # Information-oriented (API docs, technical specs)
├── dev-docs/             # Developer documentation (architecture, contributing)
├── project-docs/         # Project management (plans, decisions, retrospectives)
└── skilled-awareness/    # SAP capabilities (30+ modular packages)
```

### Session Startup Routine

```bash
# 1. Check documentation structure
just doc-structure                # Show 4-domain hierarchy

# 2. Validate documentation standards
just validate-docs                # Run DOCUMENTATION_STANDARD.md checks
just validate-frontmatter         # Check YAML frontmatter schema

# 3. Check completeness
just doc-completeness             # Verify all 4 domains exist

# 4. Extract tests from docs (if writing how-to guides)
just extract-doc-tests            # Generate tests from code blocks
```

### Common Workflows

**1. Create new how-to guide**:

```markdown
---
audience: [developers, agents]
time: 10 minutes
prerequisites: [Python 3.11+, git]
difficulty: intermediate
related: [other-guide.md]
---

# How to [Task Name]

**Goal**: [Clear objective in 1 sentence]

## Quick Start

\```bash
# Step 1: [Description]
command-1

# Step 2: [Description]
command-2
\```

## Detailed Steps

### Step 1: [Name]
[Explanation]

### Step 2: [Name]
[Explanation]

## Troubleshooting

**Problem**: [Common issue]
**Solution**: [Fix]
```

Validate:
```bash
just validate-frontmatter
just extract-doc-tests
```

**2. Validate documentation**:
```bash
# Run all validation checks
just validate-docs                # DOCUMENTATION_STANDARD.md compliance
just validate-frontmatter         # YAML schema validation

# Pre-commit hooks (L3 enforcement)
pre-commit run --all-files        # Includes doc validation
```

**3. Organize documentation using Diátaxis**:
```bash
# Decision tree: Where does this doc belong?
# 1. Is it learning-oriented? → tutorials/
# 2. Is it task-oriented? → how-to/
# 3. Is it understanding-oriented? → explanation/
# 4. Is it information-oriented? → reference/

# Example decisions:
# "Getting Started with chora-base" → tutorials/ (learning)
# "How to Add a New SAP" → how-to/ (task)
# "Why Diátaxis?" → explanation/ (understanding)
# "SAP Framework API" → reference/ (information)

# Show current structure
just doc-structure
```

**4. Extract tests from how-to guides**:
```bash
# Extract code blocks from how-to guides as tests
just extract-doc-tests

# Generated tests location
ls tests/extracted/               # Test files from docs

# Run extracted tests
pytest tests/extracted/           # Verify docs are executable
```

**5. Check documentation completeness**:
```bash
# Verify all 4 Diátaxis domains exist
just doc-completeness

# Expected output:
# ✅ Tutorials
# ✅ How-To Guides
# ✅ Explanations
# ✅ References
```

### Integration with Other SAPs

- **SAP-031 (Enforcement)**: Documentation validation as Layer 3 enforcement (5-10% prevention)
- **SAP-006 (Quality Gates)**: Pre-commit hooks validate doc structure
- **SAP-004 (Testing)**: Extracted doc tests run in pytest suite
- **SAP-002 (Chora-Base Meta)**: 4-domain structure demonstrated
- **SAP-000 (Framework)**: Every SAP follows Diátaxis pattern

### ROI Metrics

- **Documentation quality**: 40-60% improvement
- **Time savings**: 15-20 min per session
- **Test coverage**: +5-10% from extracted doc tests
- **Discoverability**: 2-3x faster doc discovery

**Documentation**:
- Standard: [DOCUMENTATION_STANDARD.md](../DOCUMENTATION_STANDARD.md)
- Protocol: [docs/skilled-awareness/documentation-framework/protocol-spec.md](../docs/skilled-awareness/documentation-framework/protocol-spec.md)
- Diátaxis: https://diataxis.fr/

---

## Docker Operations (SAP-011)

**Purpose**: Provide production-ready Docker containerization with multi-stage builds, CI-optimized test containers, docker-compose orchestration, and 40% smaller images.

**Adoption Level**: L1 (Fully operational)

### Docker Architecture

**5 Docker Artifacts**:
```bash
project/
├── Dockerfile                     # Production multi-stage build (150-250MB)
├── Dockerfile.test                # CI test environment (editable install)
├── docker-compose.yml             # Service orchestration
├── .dockerignore                  # Build context optimization (81% reduction)
└── DOCKER_BEST_PRACTICES.md       # Guidance and troubleshooting
```

**Multi-stage Build Pattern**:
- **Stage 1 (Builder)**: Build wheel → Output to /dist/
- **Stage 2 (Runtime)**: Install wheel (not editable), non-root user, health check
- **Result**: 150-250MB images (vs 500MB+ with editable install)

**CI-Optimized Test Pattern**:
- Single-stage: editable install + dev dependencies
- GitHub Actions cache: 6x faster builds (3 min → 30 sec)

### Session Startup Routine

```bash
# 1. Check if Docker artifacts exist
ls -la Dockerfile Dockerfile.test docker-compose.yml .dockerignore

# 2. Build production image
just docker-build myproject latest

# 3. Build test image (for CI)
just docker-build-test myproject test

# 4. Run tests in container (validate)
just docker-test myproject

# 5. Start services with compose
just docker-up
just docker-health
```

### Common Workflows

**1. Build and run production container**:
```bash
# Build production image (multi-stage)
just docker-build myproject latest

# Run production container
docker run -d \
  -p 8000:8000 \
  -v ./configs:/app/configs:ro \
  -v ./logs:/app/logs \
  --name myproject-prod \
  myproject:latest

# Check health
docker inspect myproject-prod | grep -A 10 Health

# View logs
docker logs -f myproject-prod

# Stop and remove
docker stop myproject-prod && docker rm myproject-prod
```

**2. Build and test in CI (GitHub Actions integration)**:
```bash
# Build CI test image (with GitHub Actions cache)
just docker-build-test myproject test

# Run tests in container
just docker-test myproject

# Extract coverage report (if needed)
docker cp $(docker create --name tmp myproject:test):/app/htmlcov ./htmlcov
docker rm tmp
```

**3. Docker Compose orchestration (multi-service)**:
```bash
# Start all services (main app + dependencies)
just docker-up

# Check service health
just docker-health
docker-compose ps

# View logs (all services)
just docker-logs

# View logs (specific service)
docker-compose logs -f myproject

# Execute command in running container
docker-compose exec myproject bash

# Restart specific service
docker-compose restart myproject

# Stop all services
just docker-down
```

**4. Volume management (3-tier strategy)**:
```bash
# Tier 1: Configs (read-only hot-reload)
# - Mount: ./configs:/app/configs:ro
# - Use: Configuration files that can be updated without rebuild
# - Example: YAML configs, JSON settings

# Tier 2: Ephemeral (session data)
# - Mount: ./ephemeral:/app/ephemeral
# - Use: Temporary data that survives restarts
# - Example: Cache, session storage

# Tier 3: Persistent (long-term data)
# - Mount: ./logs:/app/logs, ./data:/app/data, ./.chora/memory:/app/.chora/memory
# - Use: Critical data that must survive container removal
# - Example: Logs, database, event memory (SAP-010)

# Validate volume mounts
docker-compose config
docker inspect myproject | grep -A 20 Mounts
```

**5. Optimize Docker build context**:
```bash
# Check current build context size
du -sh .

# Review .dockerignore patterns
cat .dockerignore

# Expected exclusions (81% reduction):
# - .git/ (largest contributor)
# - tests/, docs/ (not needed in production)
# - .venv/, __pycache__/ (Python artifacts)
# - *.md (documentation)
# - .github/ (CI configs)

# Verify build context reduction
docker build --no-cache -t myproject:latest . 2>&1 | grep "Sending build context"
```

**6. Debug Docker containers**:
```bash
# Check container logs
docker-compose logs -f myproject

# Execute shell in running container
docker-compose exec myproject bash

# Inspect container configuration
docker inspect myproject

# Check resource usage
docker stats myproject

# View container processes
docker-compose top myproject
```

### Integration with Other SAPs

- **SAP-005 (CI/CD)**: GitHub Actions uses Dockerfile.test for testing
- **SAP-010 (Memory)**: Volume mounts for .chora/memory persistence
- **SAP-014 (MCP Server)**: MCP server containerization
- **SAP-003 (Bootstrap)**: Docker artifacts included in fast-setup

### ROI Metrics

- **Image size**: 40% smaller (150-250MB vs 500MB+)
- **CI speed**: 6x faster builds (30 sec vs 3 min)
- **Build context**: 81% reduction via .dockerignore
- **Reproducibility**: 100% (consistent environments)

---

## File Organization Conventions

### Upgrade Documentation

**Location**: `docs/upgrades/`
**Naming Pattern**: `vX.Y-to-vX.Z.md` (e.g., `v1.9.2-to-v1.9.3.md`)
**Not**: UPPERCASE naming, repo root placement

**Why This Matters**: Previous upgrade docs were misplaced in repo root because chora-base lacked AGENTS.md guidance.

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

## Related Resources

**Navigation**:
- [← Root AGENTS.md](../AGENTS.md) - Project overview and architecture
- [→ SAPs Quick Reference](../saps/AGENTS.md) - All SAP capabilities
- [→ Getting Started](../getting-started/AGENTS.md) - Onboarding guide

**Documentation**:
- [Automation Scripts (SAP-008)](../docs/skilled-awareness/automation-scripts/protocol-spec.md)
- [Quality Gates (SAP-006)](../docs/skilled-awareness/quality-gates/protocol-spec.md)
- [Documentation Framework (SAP-007)](../docs/skilled-awareness/documentation-framework/protocol-spec.md)
- [Docker Operations (SAP-011)](../docs/skilled-awareness/docker-operations/protocol-spec.md)

**Tools**:
- [justfile](../justfile) - Unified automation interface
- [.pre-commit-config.yaml](../.pre-commit-config.yaml) - Quality gates configuration
- [scripts/](../scripts/) - Automation scripts directory

---

**Version**: 1.0.0
**Last Updated**: 2025-11-10
**Status**: Active (nested awareness pattern v2.1.0)
