# Chora-Base: Claude Agent Awareness (Root)

**Project**: chora-base
**Version**: 4.11.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-09

---

## ⚠️ CRITICAL: Read This First!

**chora-base is a TEMPLATE SOURCE, not a project to set up.**

### Quick Decision for Claude

**Are you trying to CREATE A NEW PROJECT using chora-base?**

**✅ YES** → Use the fast-setup script (recommended):

```bash
python scripts/create-model-mcp-server.py \
    --name "Your Project Name" \
    --namespace yournamespace \
    --output ~/projects/your-project
```

**What happens**: 1-2 minutes of automated setup creating a fully-configured model citizen MCP server with all chora-base infrastructure (testing, CI/CD, quality gates, beads, inbox, A-MEM, documentation).

**See**: [README.md](README.md#-start-here-ai-agent-quick-decision-tree) or [Quickstart Guide](docs/user-docs/quickstart-mcp-server.md)

---

**Are you DEVELOPING chora-base itself?**

**✅ YES** → Continue reading this file for Claude-specific navigation patterns

---

## Quick Start for Claude

This file provides Claude-specific navigation and context loading strategies for working with the chora-base template repository.

### First-Time Navigation

**New to chora-base?**
1. You're reading the right file (root `CLAUDE.md`)
2. Determine your task domain (see Navigation Tree below)
3. Navigate to the appropriate domain's `AGENTS.md` file
4. Read the domain-specific `CLAUDE.md` for Claude patterns
5. Dive into specific SAP documentation as needed

**Returning to chora-base?**
1. Check your task domain
2. Navigate directly to relevant SAP or documentation
3. Use progressive context loading (see below)

---

## What is Chora-Base?

**Chora-base** is a comprehensive template and framework for AI-assisted software development, built around the **SAP (Skilled Awareness Package) framework**. It provides:

- 📦 **30+ Skilled Awareness Packages (SAPs)**: Modular capabilities for development workflows
- 🤖 **Agent-First Design**: Built for Claude Code, Claude Desktop, and other AI agents
- 📋 **Nested Awareness Pattern**: Progressive context loading via AGENTS.md/CLAUDE.md hierarchy
- 🎯 **Production-Ready Templates**: Bootstrap projects with battle-tested patterns
- 🔄 **Coordination Infrastructure**: Cross-repo inbox, event memory (A-MEM), task tracking (beads)

---

## Architecture Overview

### SAP Framework (SAP-000)

The foundation of chora-base is the **SAP framework**, which packages capabilities into five standardized artifacts:

1. **Capability Charter**: Problem statement, solution design, success criteria
2. **Protocol Spec**: Complete technical specification, commands, workflows
3. **Awareness Guide**: Operating patterns for agents (AGENTS.md or awareness-guide.md)
4. **Adoption Blueprint**: Step-by-step installation guide
5. **Ledger**: Adoption tracking, metrics, feedback, version history

Every SAP follows this pattern, making it easy to learn and adopt new capabilities.

### Nested Awareness Pattern (SAP-009)

Chora-base uses a **5-level nested awareness hierarchy**:

```
/CLAUDE.md                                    ← You are here (Root)
│
├─ docs/skilled-awareness/                    ← Domain: SAP Capabilities
│  ├─ AGENTS.md                               ← Generic agent patterns
│  ├─ CLAUDE.md                               ← Claude-specific patterns
│  │
│  ├─ sap-framework/                          ← SAP-000 (Capability Level)
│  │  ├─ AGENTS.md                            ← SAP-000 patterns
│  │  ├─ capability-charter.md
│  │  ├─ protocol-spec.md
│  │  ├─ awareness-guide.md
│  │  └─ ledger.md
│  │
│  ├─ inbox/                                  ← SAP-001 (Capability Level)
│  │  ├─ AGENTS.md
│  │  ├─ CLAUDE.md
│  │  └─ ... (5 artifacts)
│  │
│  └─ ... (30+ SAPs)
│
├─ docs/dev-docs/                             ← Domain: Developer Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (architecture, contributing, etc.)
│
├─ docs/user-docs/                            ← Domain: User Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (getting started, tutorials, reference)
│
└─ docs/project-docs/                         ← Domain: Project Management
   ├─ AGENTS.md
   ├─ CLAUDE.md
   └─ ... (plans, decisions, retrospectives)
```

**Principle**: "Nearest file wins" - navigate from root → domain → capability → feature → component, progressively loading context as needed.

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand task domain and high-level approach

**Read**:
1. This file (`/CLAUDE.md`) for project overview
2. Target domain's `AGENTS.md` (e.g., `docs/skilled-awareness/AGENTS.md`)
3. Target domain's `CLAUDE.md` for Claude-specific patterns

**Output**: Clear understanding of where to find detailed information

---

### Phase 2: Specification (10-50k tokens)

**Goal**: Load detailed technical specifications for the task

**Read**:
1. Target SAP's `protocol-spec.md` for complete technical details
2. Target SAP's `awareness-guide.md` (or `AGENTS.md`) for operating patterns
3. Related SAPs' `AGENTS.md` files if integration needed

**Output**: Complete technical understanding of commands, workflows, APIs

---

### Phase 3: Deep Dive (50-200k tokens)

**Goal**: Understand design rationale and adoption history

**Read**:
1. Target SAP's `capability-charter.md` for problem/solution design
2. Target SAP's `ledger.md` for adoption metrics and feedback
3. Target SAP's `adoption-blueprint.md` if implementing from scratch
4. Source code files as needed

**Output**: Comprehensive understanding for complex implementations

---

## Navigation Tree: Where Should Claude Go?

### Domain 1: User-Facing Documentation

**Path**: [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)

**Use when**:
- User asks "how do I use chora-base?"
- User needs tutorials or getting started guides
- User wants reference documentation
- User is new to chora-base ecosystem

**Contents**:
- Getting started guides
- Tutorials and examples
- Reference documentation
- FAQ and troubleshooting

---

### Domain 2: Developer Documentation

**Path**: [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)

**Use when**:
- Contributing to chora-base
- Understanding chora-base architecture
- Setting up development environment
- Debugging chora-base internals

**Contents**:
- Developer setup
- Architecture documentation
- Contributing guidelines
- Testing and debugging

---

### Domain 3: Project Management Documentation

**Path**: [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

**Use when**:
- User asks about project plans or roadmap
- User wants to understand governance or decisions
- Coordinating work across the project
- Reviewing retrospectives or lessons learned

**Contents**:
- Project plans (like PLAN-2025-11-04-SAP-009-FULL)
- Decision records (ADRs)
- Retrospectives
- Coordination requests

---

### Domain 4: Skilled Awareness (SAP Capabilities)

**Path**: [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)

**Use when**:
- User wants to adopt a specific SAP
- Understanding SAP framework
- Implementing or extending capabilities
- Exploring available SAPs (30+ capabilities)

**Contents**:
- SAP Framework (SAP-000)
- 30+ SAP capabilities
- SAP catalog and index
- Integration patterns

**Key SAPs to Know**:
- **SAP-000** (sap-framework): Foundation for all SAPs
- **SAP-001** (inbox): Cross-repo coordination
- **SAP-009** (agent-awareness): This nested awareness pattern
- **SAP-010** (A-MEM): Agent memory and event tracking
- **SAP-015** (task-tracking): Persistent task management with beads
- **SAP-027** (dogfooding-patterns): How to validate SAPs
- **SAP-029** (sap-generation): Generate new SAPs

---

### Domain 5: Memory System (.chora/)

**Path**: [.chora/AGENTS.md](.chora/AGENTS.md) + [.chora/CLAUDE.md](.chora/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.chora/CLAUDE.md](.chora/CLAUDE.md) - Claude workflows (8-min, ~5k tokens)
- [.chora/AGENTS.md](.chora/AGENTS.md) - Memory patterns (13-min, ~10k tokens)

**Use when**:
- Creating knowledge notes to capture learnings
- Querying event logs for context restoration
- Logging significant events (milestones, decisions, errors)
- Restoring context across sessions (hours, days, or weeks apart)
- Building knowledge graph with wikilink connections

**Contents**:
- Event logging patterns (JSONL format, trace correlation)
- Knowledge note workflows (Zettelkasten-style)
- Agent profile management
- Query template examples
- Context restoration workflows

**Note**: Memory system (`.chora/`) only exists in generated projects, not in chora-base template repository itself.

---

### Domain 6: Task Tracking (.beads/)

**Path**: [.beads/AGENTS.md](.beads/AGENTS.md) + [.beads/CLAUDE.md](.beads/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.beads/CLAUDE.md](.beads/CLAUDE.md) - Claude beads workflows (7-min, ~5k tokens)
- [.beads/AGENTS.md](.beads/AGENTS.md) - Beads patterns (10-min, ~8k tokens)

**Use when**:
- Restoring context at session startup (finding unblocked work)
- Tracking multi-session work (progress, blockers, dependencies)
- Managing backlog and task prioritization
- Coordinating with other agents or team members
- Creating audit trails for completed work

**Contents**:
- Session startup patterns (`bd ready --json`)
- Task lifecycle workflows (create, update, block, close)
- Query patterns by status/assignee/tags
- Integration with SAP-001 (inbox) and SAP-010 (memory)
- Context restoration workflows

**Note**: Beads (`.beads/`) only exists in generated projects when SAP-015 is adopted, not in chora-base template repository itself.

---

### Domain 7: Inbox Coordination Protocol (inbox/)

**Path**: [docs/skilled-awareness/inbox/AGENTS.md](docs/skilled-awareness/inbox/AGENTS.md) + [docs/skilled-awareness/inbox/CLAUDE.md](docs/skilled-awareness/inbox/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [docs/skilled-awareness/inbox/CLAUDE.md](docs/skilled-awareness/inbox/CLAUDE.md) - Claude inbox workflows (8-min, ~6k tokens)
- [docs/skilled-awareness/inbox/AGENTS.md](docs/skilled-awareness/inbox/AGENTS.md) - Inbox patterns (12-min, ~9k tokens)

**Use when**:
- Creating or responding to coordination requests
- Querying inbox status at session startup
- Generating AI-powered coordination requests
- Managing cross-repo collaboration with formalized SLAs
- Tracking coordination events and ecosystem participation

**Contents**:
- 5 CLI tools (install, query, respond, generate, status)
- Session startup routines and daily workflows
- SLA guidelines (48h default, 4h urgent, 1-week backlog)
- Ecosystem coordination patterns
- Integration with SAP-010 (memory) and SAP-015 (beads)

**Note**: Inbox coordination (SAP-001) is included in chora-base for ecosystem collaboration. Active coordination happens in `inbox/` directory.

---

### Domain 8: Agent Awareness (agent-awareness/)

**Path**: [docs/skilled-awareness/agent-awareness/AGENTS.md](docs/skilled-awareness/agent-awareness/AGENTS.md) + [docs/skilled-awareness/agent-awareness/CLAUDE.md](docs/skilled-awareness/agent-awareness/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [docs/skilled-awareness/agent-awareness/CLAUDE.md](docs/skilled-awareness/agent-awareness/CLAUDE.md) - Claude progressive loading patterns (10-min, ~7k tokens)
- [docs/skilled-awareness/agent-awareness/AGENTS.md](docs/skilled-awareness/agent-awareness/AGENTS.md) - Nested awareness patterns (15-min, ~11k tokens)

**Use when**:
- Understanding the nested AGENTS.md/CLAUDE.md pattern (SAP-009)
- Implementing progressive context loading (200k token management)
- Creating domain-specific awareness files (tests/, scripts/, .chora/)
- Validating awareness structure (7 required sections)
- Optimizing token usage with "nearest file wins" pattern

**Contents**:
- Nested hierarchy pattern (5 levels: root → domain → SAP → feature → component)
- Progressive loading phases (Essential 0-10k, Extended 10-50k, Comprehensive 50-200k)
- Domain-specific awareness examples (tests/, scripts/, .chora/, inbox/)
- Validation workflows (structure, links, token tracking)
- Integration patterns (ALL SAPs use this pattern)

**Progressive Loading Strategy**:
```markdown
Phase 1 (0-10k): Read root AGENTS.md sections 1-2 only
Phase 2 (10-50k): Read root + domain-specific AGENTS.md + CLAUDE.md (60-70% savings)
Phase 3 (50-200k): Read all SAP artifacts (only for complex tasks)
```

**Note**: Agent awareness (SAP-009) is the META-SAP that ALL other SAPs depend on for discoverability. This pattern enables 60-70% token reduction via domain-specific files.

---

### Testing Framework (SAP-004) - Quick Reference

**No domain-specific CLAUDE.md** (tests/ may have AGENTS.md if complex test patterns exist)

**Claude patterns for testing**:
```markdown
# Session startup: Run tests first
pytest --cov=src --cov-fail-under=85
just test

# If tests fail: Investigate and fix
pytest -vv --tb=short                    # Detailed output
pytest --lf                              # Re-run last failures
pytest tests/test_specific.py -v         # Run specific test file

# Writing new tests (use TDD)
# 1. Write test first (RED)
def test_new_feature():
    assert new_feature() == expected

# 2. Implement feature (GREEN)
# 3. Refactor (REFACTOR)

# Check coverage gaps
coverage report --show-missing
coverage html && open htmlcov/index.html
```

**Progressive loading strategy**:
- **Phase 1**: No loading needed (just run pytest)
- **Phase 2**: Read [tests/AGENTS.md](tests/AGENTS.md) if complex test patterns (if exists)
- **Phase 3**: Read [docs/skilled-awareness/testing-framework/protocol-spec.md](docs/skilled-awareness/testing-framework/protocol-spec.md) for pytest configuration

**ROI**: 90% bug prevention via TDD, 15-20 min saved per session (avoid manual testing)

---

### CI/CD Workflows (SAP-005) - Quick Reference

**No domain-specific CLAUDE.md** (workflows are infrastructure, not code)

**Claude patterns for CI/CD**:
```markdown
# Session startup: Check CI status
gh run list --limit 10
just ci-status

# If CI failed: Investigate and fix
gh run view {run_id} --log          # Read logs
just ci-logs {run_id}               # Alternative

# Create bead for tracking (SAP-015)
bd create "Fix test.yml failure" --priority high

# Fix locally BEFORE pushing (SAP-006)
pytest tests/                       # Run tests
ruff check --fix src/ tests/        # Auto-fix linting
mypy src/ tests/                    # Type check

# Push and verify
git push origin branch
gh run list --limit 5               # Verify new run
```

**Progressive loading strategy**:
- **Phase 1**: No loading needed (CI is automated)
- **Phase 2**: Read [.github/workflows/](../.github/workflows/) if debugging CI failures
- **Phase 3**: Read [docs/skilled-awareness/ci-cd-workflows/protocol-spec.md](docs/skilled-awareness/ci-cd-workflows/protocol-spec.md) for workflow specifications

**ROI**: Automated quality gates catch 95%+ preventable issues before merge, <5 min feedback loops

---

### Documentation Framework (SAP-007) - Quick Reference

**No domain-specific CLAUDE.md** (documentation is infrastructure, not code)

**Claude patterns for documentation**:
```markdown
# User wants to add documentation → Use Diátaxis decision tree
# 1. Learning-oriented? → docs/user-docs/tutorials/
# 2. Task-oriented? → docs/user-docs/how-to/
# 3. Understanding-oriented? → docs/user-docs/explanation/
# 4. Information-oriented? → docs/user-docs/reference/

# Validate documentation structure
just doc-structure            # Show 4-domain hierarchy
just validate-docs            # Run DOCUMENTATION_STANDARD.md checks
just validate-frontmatter     # Check YAML frontmatter

# Extract tests from how-to guides
just extract-doc-tests        # Generate tests from code blocks

# Common workflows
# 1. Create new how-to guide with frontmatter
cat > docs/user-docs/how-to/example.md <<'EOF'
---
audience: [developers, agents]
time: 10 minutes
prerequisites: [Python 3.11+]
difficulty: intermediate
---

# How to [Task]

## Quick Start
\```bash
# Step 1
command-1
\```
EOF

just validate-frontmatter     # Validate YAML

# 2. Extract tests from docs
just extract-doc-tests
pytest tests/extracted/       # Run extracted tests

# 3. Check completeness
just doc-completeness         # Verify all 4 domains exist
```

**Progressive loading strategy**:
- **Phase 1**: Read [DOCUMENTATION_STANDARD.md](DOCUMENTATION_STANDARD.md) for rules (10-min read)
- **Phase 2**: Read [docs/skilled-awareness/documentation-framework/protocol-spec.md](docs/skilled-awareness/documentation-framework/protocol-spec.md) for complete spec
- **Phase 3**: Read Diátaxis reference (https://diataxis.fr/) for deep understanding

**ROI**: 40-60% documentation quality improvement, 15-20 min saved per session (avoid doc inconsistencies)

**Integration with other SAPs**:
- SAP-031 (Enforcement): Doc validation as Layer 3 enforcement (5-10% prevention)
- SAP-006 (Quality Gates): Pre-commit hooks validate frontmatter
- SAP-004 (Testing): Extracted doc tests run in pytest

**Diátaxis Quick Reference**:
- **Tutorials**: Learning-oriented, step-by-step lessons (e.g., "Getting Started")
- **How-To**: Task-oriented, practical guides (e.g., "How to Add a SAP")
- **Explanation**: Understanding-oriented, concepts (e.g., "Why Diátaxis?")
- **Reference**: Information-oriented, technical details (e.g., "API Docs")

---

### Automation Scripts (SAP-008) - Quick Reference

**No domain-specific CLAUDE.md** (automation is infrastructure, not code)

**Claude patterns for automation**:
```markdown
# User wants to automate workflows → Use justfile interface
just automation-help              # Show all 30+ commands grouped by category
just --list                       # List all available commands

# Setup workflows
just install                      # Install project in editable mode
just setup-hooks                  # Install pre-commit hooks
just check-env                    # Validate environment

# Development workflows
just test                         # Run pytest suite
just smoke                        # Quick smoke tests (~5-10s)
just integration                  # Integration tests
just diagnose                     # Environment diagnostics

# Quality gates
just lint                         # Run ruff linter
just format                       # Format code with ruff
just type-check                   # Run mypy type checker
just pre-merge                    # All quality gates before merge

# Version management
just bump-patch                   # 1.0.0 → 1.0.1 (bug fixes)
just bump-minor                   # 1.0.0 → 1.1.0 (new features)
just bump-major                   # 1.0.0 → 2.0.0 (breaking changes)

# Release & publishing
just build                        # Build distribution packages
just publish-test                 # Publish to test PyPI
just publish-prod                 # Publish to production PyPI

# Common workflows
# 1. Setup new development environment
just install
just setup-hooks
just check-env
just smoke

# 2. Development workflow (test → lint → format → type-check)
just test                         # Run tests
just lint                         # Check code quality
just format                       # Format code
just type-check                   # Validate types
just pre-merge                    # Run all gates

# 3. Release workflow
just bump-minor                   # Bump version
just build                        # Build packages
just publish-test                 # Publish to test PyPI (validate)
just publish-prod                 # Publish to production PyPI

# 4. Troubleshooting
just diagnose                     # Run diagnostics
just check-env                    # Validate environment
just smoke                        # Quick health check
```

**Progressive loading strategy**:
- **Phase 1**: Run `just automation-help` for command reference (instant)
- **Phase 2**: Read [docs/skilled-awareness/automation-scripts/protocol-spec.md](docs/skilled-awareness/automation-scripts/protocol-spec.md) for complete contracts
- **Phase 3**: Read individual scripts in scripts/ directory for implementation details

**ROI**: 30-45 min saved per day (consistent automation, no manual workflows), 90%+ reduction in setup errors

**8 Script Categories**:
- **Setup & Environment**: install, setup-hooks, check-env
- **Development**: test, smoke, integration, diagnose
- **Quality**: lint, format, type-check, pre-merge
- **Version Management**: bump-patch, bump-minor, bump-major
- **Release & Publishing**: build, publish-test, publish-prod
- **Documentation**: validate-docs, extract-doc-tests, doc-structure
- **Safety & Recovery**: rollback-dev, handoff
- **MCP & Specialized**: mcp-tool, validate-mcp-names

---

### Docker Operations (SAP-011) - Quick Reference

**No domain-specific CLAUDE.md** (Docker is infrastructure, not code)

**Claude patterns for Docker**:
```markdown
# User wants to containerize application → Use Docker artifacts
just docker-build myproject latest    # Build production image
just docker-build-test myproject test # Build CI test image
just docker-test myproject            # Run tests in container
just docker-up                        # Start with docker-compose
just docker-health                    # Check service health

# Production workflows
# 1. Build and run production container
just docker-build myproject latest
docker run -d -p 8000:8000 -v ./configs:/app/configs:ro myproject:latest
docker logs -f myproject

# 2. Build and test in CI (GitHub Actions)
just docker-build-test myproject test
just docker-test myproject

# 3. Docker Compose orchestration
just docker-up                        # Start all services
just docker-health                    # Check health
just docker-logs                      # View logs
just docker-down                      # Stop services

# 4. Volume management (3-tier strategy)
# Tier 1: Configs (read-only hot-reload)
#   ./configs:/app/configs:ro
# Tier 2: Ephemeral (session data)
#   ./ephemeral:/app/ephemeral
# Tier 3: Persistent (long-term data)
#   ./logs:/app/logs, ./data:/app/data, ./.chora/memory:/app/.chora/memory

# Debugging
docker-compose logs -f myproject      # View logs
docker-compose exec myproject bash    # Shell access
docker inspect myproject              # Configuration
docker stats myproject                # Resource usage
```

**Progressive loading strategy**:
- **Phase 1**: Run Docker commands via justfile (instant)
- **Phase 2**: Read [docs/skilled-awareness/docker-operations/protocol-spec.md](docs/skilled-awareness/docker-operations/protocol-spec.md) for multi-stage build patterns
- **Phase 3**: Read Dockerfile, Dockerfile.test, docker-compose.yml for implementation details

**ROI**: 40% smaller images (150-250MB vs 500MB+), 6x faster CI builds (3 min → 30 sec), 100% reproducible environments

**5 Docker Artifacts**:
- **Dockerfile**: Production multi-stage build (builder + runtime, wheel distribution, non-root)
- **Dockerfile.test**: CI test environment (editable install, dev dependencies, cache-friendly)
- **docker-compose.yml**: Service orchestration (volumes, networks, health checks)
- **.dockerignore**: Build context optimization (81% reduction)
- **DOCKER_BEST_PRACTICES.md**: Guidance, troubleshooting, security patterns

**Multi-Stage Build Pattern**:
- **Stage 1 (Builder)**: Install build dependencies → Build wheel → Output to /dist/
- **Stage 2 (Runtime)**: Install wheel (not editable) → Create non-root user → Health check → CMD

**Why Wheel Distribution?**:
- Eliminates namespace import conflicts (vs editable install)
- 40% smaller images (no build tools in production)
- Matches PyPI distribution format

---

### Chora-Base Meta Package (SAP-002) - Quick Reference

**No domain-specific CLAUDE.md** (chora-base documentation IS the awareness system)

**Claude patterns for chora-base navigation**:
```markdown
# User wants to understand chora-base → Navigate 4-domain docs
cat README.md                         # Overview, features, quick start
just list-saps                        # List all 30+ SAPs
cat docs/skilled-awareness/INDEX.md   # SAP catalog

# Explore documentation domains
cat docs/user-docs/AGENTS.md          # User guides, tutorials
cat docs/dev-docs/AGENTS.md           # Architecture, contributing
cat docs/project-docs/AGENTS.md       # Plans, decisions
cat docs/skilled-awareness/AGENTS.md  # SAP capabilities

# Verify structure
just verify-structure                 # Validate integrity
just chora-info                       # Show meta information

# Common workflows
# 1. New user wants to understand chora-base
cat README.md
just explore-docs

# 2. Developer wants to contribute
cat docs/dev-docs/AGENTS.md
cat CONTRIBUTING.md

# 3. Find specific SAP
just list-saps | grep "SAP-015"
cat docs/skilled-awareness/INDEX.md

# 4. Learn SAP framework by example
ls docs/skilled-awareness/chora-base/  # SAP-002 artifacts (5 files)
ls docs/skilled-awareness/testing-framework/  # Compare pattern
```

**Progressive loading strategy**:
- **Phase 1**: Read [README.md](README.md) for overview (5-min read)
- **Phase 2**: Read domain-specific AGENTS.md ([docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md), [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)) based on task
- **Phase 3**: Read [docs/skilled-awareness/chora-base/protocol-spec.md](docs/skilled-awareness/chora-base/protocol-spec.md) for complete architecture

**ROI**: 60-70% token savings via progressive loading, zero documentation debt (self-documenting architecture)

**Navigation principle**: "Nearest file wins" - navigate from root (AGENTS.md, CLAUDE.md) → domain → capability → feature

---

### Project Bootstrap (SAP-003) - Quick Reference

**No domain-specific CLAUDE.md** (fast-setup is a script, not infrastructure)

**Claude patterns for project bootstrap**:
```markdown
# User wants to create new project → Use fast-setup
python scripts/create-model-mcp-server.py \
    --name "Project Name" \
    --namespace namespace \
    --output ~/projects/output

# Before fast-setup: Verify template integrity
just verify-template

# After fast-setup: Validate generated project
just validate-project ~/projects/output

# Common workflows
# 1. Create new MCP server
python scripts/create-model-mcp-server.py --name "Weather MCP" --namespace weather --output ~/projects/weather-mcp
cd ~/projects/weather-mcp
pytest --cov=src --cov-fail-under=85  # Verify tests pass

# 2. Verify template before fast-setup
just verify-template                  # Check template integrity

# 3. Validate generated project
just validate-project ~/projects/weather-mcp  # Full validation

# 4. List available templates
just list-templates                   # Show available templates
```

**Progressive loading strategy**:
- **Phase 1**: No loading needed (just run fast-setup script)
- **Phase 2**: Read [scripts/create-model-mcp-server.py](scripts/create-model-mcp-server.py) if debugging script
- **Phase 3**: Read [docs/skilled-awareness/project-bootstrap/protocol-spec.md](docs/skilled-awareness/project-bootstrap/protocol-spec.md) for copier specifications

**ROI**: 95% time reduction (30-60 min manual → 1-2 min fast-setup), zero-config production readiness

**Integration with other SAPs**:
- Fast-setup adopts 6+ SAPs automatically: SAP-004 (Testing), SAP-005 (CI/CD), SAP-006 (Quality Gates), SAP-001 (Inbox), SAP-010 (Memory), SAP-015 (Beads)
- Generated projects are "model citizens" (pass all quality gates out-of-the-box)
- Use fast-setup to bootstrap new projects, NOT manual setup

---

### Quality Gates (SAP-006) - Quick Reference

**No domain-specific CLAUDE.md** (pre-commit is infrastructure, not code)

**Claude patterns for pre-commit hooks**:
```markdown
# Session startup: Run pre-commit hooks first
pre-commit run --all-files
just pre-commit-all

# If hooks fail: Fix and retry
ruff check --fix src/ tests/ scripts/   # Auto-fix linting
just lint-fix
mypy src/ tests/ scripts/               # Type check
just typecheck

# Emergency bypass (ONLY if justified)
git commit --no-verify -m "Emergency: Brief justification"

# Common workflows
# 1. Normal commit with hooks
git add .
git commit -m "Add feature"             # Hooks run automatically

# 2. Fix linting errors
git add file.py
git commit -m "Add feature"
# [ruff fails]
ruff check --fix file.py                # Auto-fix
git add file.py
git commit -m "Add feature"             # Success

# 3. Fix type errors
git add file.py
git commit -m "Add feature"
# [mypy fails]
# Edit file.py to fix type errors
git add file.py
git commit -m "Add feature"             # Success
```

**Progressive loading strategy**:
- **Phase 1**: No loading needed (hooks auto-run on commit)
- **Phase 2**: Read [.pre-commit-config.yaml](.pre-commit-config.yaml) if debugging hook failures
- **Phase 3**: Read [docs/skilled-awareness/quality-gates/protocol-spec.md](docs/skilled-awareness/quality-gates/protocol-spec.md) for hook specifications

**ROI**: Catch 95%+ preventable issues locally in <5s (vs 3-5 min in CI), 10-15 min saved per session

**Integration with SAP-004 (Testing) and SAP-005 (CI/CD)**:
- Pre-commit hooks run locally BEFORE CI (SAP-006)
- CI validates remotely AFTER push (SAP-005)
- Both use same pytest configuration (SAP-004)
- Dual validation: 99%+ issue prevention before merge

---

## Common Claude Code Workflows

### Workflow 1: Adopting a SAP

```markdown
User: "I want to add task tracking to my project"

Claude:
1. Navigate to docs/skilled-awareness/AGENTS.md
2. Find SAP-015 (task-tracking) in the SAP catalog
3. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
4. Follow step-by-step installation guide
5. Update project AGENTS.md with SAP-015 patterns
```

**Progressive Loading**:
- Phase 1: Read `docs/skilled-awareness/AGENTS.md` + `docs/skilled-awareness/task-tracking/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/task-tracking/protocol-spec.md` + `adoption-blueprint.md`
- Phase 3 (if needed): Read `capability-charter.md` + `ledger.md` for design rationale

---

### Workflow 2: Understanding Chora-Base Architecture

```markdown
User: "How does chora-base work?"

Claude:
1. Read this file (CLAUDE.md) for overview
2. Navigate to docs/dev-docs/CLAUDE.md for developer perspective
3. Read docs/skilled-awareness/sap-framework/protocol-spec.md
4. Review sap-catalog.json for capability inventory
```

**Progressive Loading**:
- Phase 1: Read `/CLAUDE.md` + `docs/dev-docs/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/sap-framework/protocol-spec.md`
- Phase 3 (if deep dive): Read architecture documentation, source code

---

### Workflow 3: Contributing to Chora-Base

```markdown
User: "I want to contribute a new SAP"

Claude:
1. Read docs/dev-docs/AGENTS.md for contributing guidelines
2. Navigate to docs/skilled-awareness/sap-generation/
3. Read SAP-029 adoption-blueprint.md for generation workflow
4. Use SAP templates to scaffold new capability
5. Follow SAP-000 protocol-spec.md for artifact requirements
```

**Progressive Loading**:
- Phase 1: Read `docs/dev-docs/AGENTS.md` + `docs/skilled-awareness/CLAUDE.md`
- Phase 2: Read `docs/skilled-awareness/sap-generation/protocol-spec.md` + `sap-framework/protocol-spec.md`
- Phase 3: Review existing SAPs for examples (e.g., SAP-015)

---

### Workflow 4: Multi-Session Task Tracking

```markdown
User: "Continue working on the feature from yesterday"

Claude:
1. Check if SAP-015 (beads) is adopted: ls .beads/
2. If yes: bd ready --json to find unblocked work
3. Read task details: bd show {id} --json
4. Resume work with full context from task description
```

**Why This Matters**: Beads (SAP-015) provides persistent memory across sessions, eliminating context re-establishment overhead.

---

## Claude-Specific Tips

### Tip 1: Use Domain-Level CLAUDE.md Files

Each domain has a `CLAUDE.md` file with Claude-specific patterns:
- [docs/skilled-awareness/CLAUDE.md](docs/skilled-awareness/CLAUDE.md) - SAP navigation
- [docs/dev-docs/CLAUDE.md](docs/dev-docs/CLAUDE.md) - Development workflows
- [docs/user-docs/CLAUDE.md](docs/user-docs/CLAUDE.md) - User documentation tips
- [docs/project-docs/CLAUDE.md](docs/project-docs/CLAUDE.md) - Project navigation

**Always read the domain CLAUDE.md after navigating to a domain.**

---

### Tip 2: Leverage SAP Integration Patterns

Many SAPs integrate with each other:
- **SAP-001 (inbox) + SAP-015 (beads)**: Decompose coordination requests into tasks
- **SAP-010 (A-MEM) + SAP-015 (beads)**: Correlate tasks with event traces
- **SAP-009 (awareness) + all SAPs**: Every SAP uses nested awareness pattern

Look for "Integration with Other SAPs" sections in AGENTS.md files.

---

### Tip 3: Use JSON Output for Programmatic Workflows

Many SAP CLIs provide `--json` flags for Claude Code:
- `bd ready --json` (beads task tracking)
- `bd show {id} --json` (task details)
- `bd list --status open --json` (backlog)

Parse JSON in Claude Code sessions for structured data.

---

### Tip 4: Respect Progressive Loading

**Don't over-read**:
- If user asks "what is SAP-015?", read `docs/skilled-awareness/task-tracking/AGENTS.md` (5min), NOT all 5 artifacts (30min)
- Only read `protocol-spec.md` when implementing
- Only read `capability-charter.md` when understanding design rationale

**Do progressive loading**:
- Phase 1: Quick reference (AGENTS.md)
- Phase 2: Implementation (protocol-spec.md, adoption-blueprint.md)
- Phase 3: Deep understanding (capability-charter.md, ledger.md)

---

### Tip 5: Check Adoption Status Before Recommending SAPs

Always check SAP status in `sap-catalog.json` before recommending:
- **production**: Battle-tested, recommend freely
- **pilot**: Dogfooding phase, use with caution
- **draft**: Experimental, only recommend if explicitly requested
- **deprecated**: Don't recommend, suggest alternatives

Example:
```json
{
  "id": "SAP-015",
  "name": "task-tracking",
  "status": "pilot",  ← Pilot phase, validate before broad recommendation
  "version": "1.0.0"
}
```

---

## Key Files for Claude

### High-Frequency Files (Read Often)

- `/CLAUDE.md` (this file) - Root navigation
- `sap-catalog.json` - Machine-readable SAP registry
- `AGENTS.md` (project root) - Quick reference for all agents
- `docs/skilled-awareness/INDEX.md` - SAP capability index

### Configuration Files

- `.chora/config.yaml` - Chora configuration
- `.beads/config.yaml` - Beads task tracking (if SAP-015 adopted)
- `package.json` - npm dependencies
- `pyproject.toml` - Python dependencies

### Coordination Files (If SAP-001 Adopted)

- `inbox/coordination/active.jsonl` - Active coordination requests
- `inbox/coordination/archived.jsonl` - Historical requests
- `inbox/coordination/events.jsonl` - Coordination event log

### Memory Files (If SAP-010 Adopted)

- `.chora/memory/events/*.jsonl` - Event-sourced history
- `.chora/memory/events/development.jsonl` - Development events
- `.chora/memory/events/inbox.jsonl` - Coordination events

### Task Files (If SAP-015 Adopted)

- `.beads/issues.jsonl` - Task source of truth (git-committed)
- `.beads/beads.db` - SQLite cache (gitignored, auto-generated)

---

## Integration with Claude Code vs Claude Desktop

### Claude Code (VSCode Extension)

**Strengths**:
- Direct file system access (Read, Write, Edit tools)
- Shell command execution (Bash tool)
- Git integration
- Multi-file editing workflows

**Recommended SAPs**:
- SAP-015 (task-tracking): Persistent memory across sessions
- SAP-005 (ci-cd-workflows): GitHub Actions integration
- SAP-011 (docker-operations): Container management
- SAP-003 (project-bootstrap): Scaffold new projects

**Patterns**:
- Use beads CLI directly via Bash tool
- Edit AGENTS.md files as you work
- Commit task progress regularly

---

### Claude Desktop (Chat Interface)

**Strengths**:
- Interactive guidance
- Exploratory conversations
- Documentation generation
- Planning and architecture

**Recommended SAPs**:
- SAP-009 (agent-awareness): Navigate documentation
- SAP-027 (dogfooding-patterns): Validate adoption
- SAP-029 (sap-generation): Generate new capabilities
- SAP-001 (inbox): Coordinate across contexts

**Patterns**:
- Use progressive context loading heavily
- Generate plans and documentation
- Provide architectural guidance
- Coordinate multi-session work via inbox

---

## Common Pitfalls for Claude

### Pitfall 1: Over-Reading Documentation

**Problem**: Reading all 5 SAP artifacts when only AGENTS.md is needed

**Fix**: Use progressive loading:
- Quick question? Read AGENTS.md only
- Implementation? Read protocol-spec.md + adoption-blueprint.md
- Design rationale? Then read capability-charter.md

---

### Pitfall 2: Ignoring SAP Status

**Problem**: Recommending `draft` SAPs as production-ready

**Fix**: Always check `status` in sap-catalog.json:
```bash
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status
```

---

### Pitfall 3: Not Using Task Tracking

**Problem**: Losing context between sessions, forgetting subtasks

**Fix**: If SAP-015 adopted, ALWAYS use beads:
```bash
bd ready --json                                    # Find work
bd update {id} --status in_progress --assignee me  # Claim
bd close {id} --reason "Completed X"              # Finish
```

---

### Pitfall 4: Not Updating AGENTS.md

**Problem**: Implementing features without updating agent awareness

**Fix**: After implementing a feature, update relevant AGENTS.md:
- Root AGENTS.md for project-wide patterns
- Domain AGENTS.md for domain-specific patterns
- SAP AGENTS.md for capability-specific patterns

---

### Pitfall 5: Broken Link Networks

**Problem**: Creating AGENTS.md/CLAUDE.md files with broken links

**Fix**: After creating awareness files, validate links:
```bash
bash scripts/validate-awareness-links.sh
```

---

## Quick Reference: SAP Catalog

### Core Infrastructure (Adopt First)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-000 | sap-framework | production | Foundation for all SAPs |
| SAP-009 | agent-awareness | production | This nested awareness pattern |
| SAP-001 | inbox | production | Cross-repo coordination |
| SAP-010 | memory-system | production | Event-sourced agent memory |

### Development Workflow

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-003 | project-bootstrap | draft | Scaffold new projects |
| SAP-005 | ci-cd-workflows | production | GitHub Actions automation |
| SAP-011 | docker-operations | production | Container management |
| SAP-015 | task-tracking | pilot | Persistent task memory (beads) |

### SAP Ecosystem

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-027 | dogfooding-patterns | production | Validate SAP adoption |
| SAP-029 | sap-generation | production | Generate new SAPs |
| SAP-028 | publishing-automation | draft | Automated SAP distribution |

### Frontend Development (React Ecosystem)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-016 | link-validation | draft | Reference management |
| SAP-017 | state-management | draft | React state patterns |
| SAP-018 | form-validation | draft | Form handling |
| SAP-026 | ui-component-library | draft | Design system |
| SAP-030 | data-fetching | draft | API integration |
| SAP-031 | routing-navigation | draft | Next.js routing |
| SAP-032 | performance-optimization | draft | React performance |

**Full Catalog**: See [sap-catalog.json](sap-catalog.json) or [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

---

## React Development with SAPs

**Quick Access**: [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md)

chora-base includes **16 specialized React SAPs** for Next.js 15 + React 19 development, providing production-ready implementations with an average of **89.8% time savings**.

### React SAP Categories (16 SAPs)

**Foundation (4 SAPs)**: Core building blocks for any React application

- [SAP-020](docs/skilled-awareness/react-foundation/) - Next.js 15 Foundation (App Router, Server Components)
- [SAP-033](docs/skilled-awareness/react-authentication/) - Authentication (NextAuth v5, Clerk, Supabase, Auth0)
- [SAP-034](docs/skilled-awareness/react-database-integration/) - Database (Prisma, Drizzle ORM)
- [SAP-041](docs/skilled-awareness/react-form-validation/) - Forms (React Hook Form + Zod validation)

**Developer Experience (6 SAPs)**: Quality and productivity tools

- [SAP-021](docs/skilled-awareness/react-testing/) - Testing (Vitest + React Testing Library)
- [SAP-022](docs/skilled-awareness/react-linting/) - Linting (ESLint 9 + Prettier)
- [SAP-023](docs/skilled-awareness/react-state-management/) - State (TanStack Query, Zustand)
- [SAP-024](docs/skilled-awareness/react-styling/) - Styling (Tailwind CSS + shadcn/ui)
- [SAP-025](docs/skilled-awareness/react-performance/) - Performance (Core Web Vitals optimization)
- [SAP-026](docs/skilled-awareness/react-accessibility/) - Accessibility (WCAG 2.2 Level AA)

**User-Facing (2 SAPs)**: Production features

- [SAP-035](docs/skilled-awareness/react-file-upload/) - File Upload (UploadThing, Vercel Blob, Supabase, S3)
- [SAP-036](docs/skilled-awareness/react-error-handling/) - Error Handling (Sentry, Error Boundaries)

**Advanced (4 SAPs)**: Enterprise capabilities

- [SAP-037](docs/skilled-awareness/react-realtime-synchronization/) - Real-Time (Socket.IO, SSE, Pusher, Ably)
- [SAP-038](docs/skilled-awareness/react-internationalization/) - i18n (next-intl, react-i18next)
- [SAP-039](docs/skilled-awareness/react-e2e-testing/) - E2E Testing (Playwright, Cypress)
- [SAP-040](docs/skilled-awareness/react-monorepo-architecture/) - Monorepo (Turborepo, Nx, pnpm workspaces)

---

### Progressive Loading for React Development

**Phase 1: Foundation** (Read these first - 20 min total)

Start with AGENTS.md files for quick overviews:
- [SAP-020 AGENTS.md](docs/skilled-awareness/react-foundation/AGENTS.md) (5 min) - Next.js 15 baseline
- [SAP-033 AGENTS.md](docs/skilled-awareness/react-authentication/AGENTS.md) (5 min) - Authentication overview
- [SAP-034 AGENTS.md](docs/skilled-awareness/react-database-integration/AGENTS.md) (5 min) - Database overview
- [SAP-041 AGENTS.md](docs/skilled-awareness/react-form-validation/AGENTS.md) (5 min) - Forms overview

**Phase 2: Implementation** (Read when building - 15-30 min per SAP)

For each SAP you're adopting:
- Read `protocol-spec.md` for complete technical reference
- Read `adoption-blueprint.md` for step-by-step setup instructions
- Review code examples in protocol-spec (25+ examples per SAP)

**Phase 3: Deep Dive** (Read when troubleshooting - 5-15 min per SAP)

Only when you need design rationale or evidence:
- Read `capability-charter.md` for problem statement and solution design
- Read `ledger.md` for production case studies and metrics
- Review integration patterns with other SAPs

**Token Savings**: Progressive loading saves 60-70% tokens vs reading all artifacts at once.

---

### Common React Workflows

**Workflow 1: New Next.js Project**

```markdown
User: "I want to build a new Next.js app with auth and database"

Claude:
1. Read [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md#foundation-stack)
2. Follow Foundation Stack tutorial (30 minutes):
   - SAP-020: Initialize Next.js 15 with App Router
   - SAP-034: Setup database (Prisma or Drizzle)
   - SAP-033: Add authentication (NextAuth v5, Clerk, etc.)
   - SAP-041: Setup forms with validation
3. Result: Production-ready app with signup/login flow
```

**Progressive Loading**:
- Phase 1: Read Integration Guide Foundation Stack section (10 min)
- Phase 2: Read adoption blueprints for SAP-020, SAP-034, SAP-033, SAP-041 (30 min total)
- Phase 3 (if needed): Read protocol-spec.md for specific SAPs

---

**Workflow 2: Add Feature to Existing Next.js Project**

```markdown
User: "Add file upload to my Next.js app"

Claude:
1. Check dependencies in sap-catalog.json
   - SAP-035 depends on: SAP-020, SAP-033, SAP-034
2. Verify dependencies are met (auth + database already set up)
3. Read [SAP-035 adoption-blueprint.md](docs/skilled-awareness/react-file-upload/adoption-blueprint.md)
4. Follow step-by-step installation (20 minutes):
   - Choose provider (UploadThing, Vercel Blob, Supabase, S3)
   - Setup upload API route
   - Configure file router with auth middleware
   - Add upload component
5. Test integration with existing auth + database
```

**Progressive Loading**:
- Phase 1: Read SAP-035 AGENTS.md (5 min)
- Phase 2: Read SAP-035 adoption-blueprint.md (10 min)
- Phase 3 (if troubleshooting): Read protocol-spec.md for complete API reference

---

**Workflow 3: Build Enterprise-Scale App**

```markdown
User: "I need a monorepo with multiple apps, shared UI components, and E2E testing"

Claude:
1. Read [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md#enterprise-stack)
2. Follow Enterprise Stack tutorial (90 minutes):
   - Foundation Stack (SAP-020, SAP-033, SAP-034, SAP-041)
   - SAP-040: Setup monorepo (Turborepo, Nx, or pnpm)
   - Create shared packages (@acme/ui, @acme/utils)
   - SAP-039: Add E2E testing (Playwright or Cypress)
   - Configure remote caching (90% build time reduction)
3. Result: Multi-app monorepo with shared packages and comprehensive testing
```

**Progressive Loading**:
- Phase 1: Read Integration Guide Enterprise Stack section (15 min)
- Phase 2: Read SAP-040 and SAP-039 adoption blueprints (40 min total)
- Phase 3 (if needed): Read monorepo case studies in ledger.md

---

**Workflow 4: Troubleshooting Cross-SAP Issues**

```markdown
User: "Getting type errors between NextAuth and Prisma"

Claude:
1. Check [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md#troubleshooting)
2. Look for specific issue: "NextAuth + Prisma Type Conflicts"
3. Apply documented fix:
   - Extend NextAuth types with session.user.id
   - Use PrismaAdapter for session storage
4. If issue not documented:
   - Read SAP-033 and SAP-034 protocol-spec.md for integration patterns
   - Review production case studies in ledger.md
```

**Progressive Loading**:
- Phase 1: Read Integration Guide Troubleshooting section (5 min)
- Phase 2 (if not found): Read relevant SAP AGENTS.md files (10 min)
- Phase 3 (if still stuck): Read protocol-spec.md for both SAPs (20 min)

---

### React SAP Decision Trees

**Which authentication provider?**

```
Need self-hosted?
  ✅ Yes → NextAuth v5 (unlimited free tier)
  ❌ No → Continue

Need quick start with managed auth?
  ✅ Yes → Clerk (10k MAU free)
  ❌ No → Continue

Already using Supabase?
  ✅ Yes → Supabase Auth (50k MAU free)
  ❌ No → Auth0 (enterprise compliance)
```

See [SAP-033 protocol-spec.md](docs/skilled-awareness/react-authentication/protocol-spec.md) for complete decision matrix.

---

**Which database ORM?**

```
Priority: Type safety + performance?
  ✅ Yes → Drizzle ORM
  ❌ No → Continue

Priority: Rapid development + ease of use?
  ✅ Yes → Prisma
  ❌ No → Either (both excellent)
```

See [SAP-034 protocol-spec.md](docs/skilled-awareness/react-database-integration/protocol-spec.md) for comparison.

---

**Which real-time solution?**

```
Need bidirectional communication?
  ❌ No → Server-Sent Events (simplest, free)
  ✅ Yes → Continue

Need self-hosted?
  ✅ Yes → Socket.IO
  ❌ No → Pusher ($49/mo) or Ably ($29/mo)
```

See [SAP-037 protocol-spec.md](docs/skilled-awareness/react-realtime-synchronization/protocol-spec.md) for complete comparison.

---

### React SAP Stack Combinations

**Minimal Startup** (Blog, Portfolio)
- SAP-020 (Next.js 15) + SAP-024 (Styling)
- **Time**: 15 minutes
- **Use case**: Static pages, SEO-optimized content

**SaaS Starter** (MVP, Small Apps)
- Foundation Stack: SAP-020, SAP-033, SAP-034, SAP-041
- **Time**: 30 minutes
- **Use case**: Auth + database + forms

**Production SaaS** (Customer-Facing Apps)
- Foundation + User-Facing: +SAP-035, +SAP-036
- **Time**: 50 minutes
- **Use case**: File uploads + error tracking

**Global SaaS** (International Markets)
- Production SaaS + SAP-038 (i18n)
- **Time**: 70 minutes
- **Use case**: Multi-language support, RTL layouts

**Real-Time Collaboration** (Chat, Collaboration Tools)
- Production SaaS + SAP-037 (Real-Time)
- **Time**: 80 minutes
- **Use case**: Live updates, WebSocket communication

**Enterprise Application** (Large Teams, Multi-Product)
- Advanced + Enterprise: +SAP-039, +SAP-040
- **Time**: 90 minutes
- **Use case**: Monorepo, E2E testing, CI/CD

See [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md#stack-combinations-quick-reference) for complete stack guide.

---

### React SAP Integration Patterns

React SAPs are designed to work together seamlessly. Common integration patterns:

**Auth + Database** (SAP-033 + SAP-034)
- PrismaAdapter syncs NextAuth sessions with database
- Automatic user account linking
- Type-safe session access in Server Components

**Auth + Forms** (SAP-033 + SAP-041)
- Protected Server Actions with session validation
- User context injection in form handlers
- Type-safe form data with Zod + Prisma schemas

**Real-Time + State** (SAP-037 + SAP-023)
- WebSocket events trigger TanStack Query invalidation
- Optimistic updates with automatic rollback
- Efficient cache synchronization

**i18n + Routing** (SAP-038 + SAP-020)
- Locale-based routing with Next.js middleware
- SEO-friendly URLs with hreflang tags
- Type-safe translations with TypeScript inference

**Monorepo + All** (SAP-040 + All SAPs)
- Shared packages for UI, auth, database, forms
- Remote caching for 90% build time reduction
- Consistent configuration across apps

See [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md#common-integration-patterns) for complete code examples.

---

### React SAP Time Savings

| Stack | Setup Time | Manual Time | Time Savings |
|-------|------------|-------------|--------------|
| **Foundation** (4 SAPs) | 30 min | 10 hours | 95% |
| **User-Facing** (+2 SAPs) | 50 min | 15 hours | 94% |
| **Advanced** (+2 SAPs) | 70 min | 25 hours | 95% |
| **Enterprise** (+2 SAPs) | 90 min | 35 hours | 96% |

**Average across all 16 React SAPs**: 89.8% time reduction

---

### React SAP Quick Tips for Claude

**Tip 1: Multi-Provider Support**

All React SAPs offer multiple provider options (no vendor lock-in):
- Authentication: 4 providers (NextAuth, Clerk, Supabase, Auth0)
- Database: 2 ORMs (Prisma, Drizzle)
- File Upload: 4 providers (UploadThing, Vercel Blob, Supabase, S3)
- Real-Time: 4 solutions (Socket.IO, SSE, Pusher, Ably)

Always present options and decision criteria to users.

**Tip 2: TypeScript-First**

All React SAPs use TypeScript with full type inference:
- 100% type-safe examples
- Zod schemas with `z.infer<typeof schema>`
- Prisma/Drizzle type generation
- Next.js type-safe routes

Never compromise type safety.

**Tip 3: Check Dependencies**

Before adopting a SAP, check dependencies in sap-catalog.json:
```bash
grep -A 10 '"id": "SAP-035"' sap-catalog.json | grep dependencies
# SAP-035 depends on: SAP-000, SAP-020, SAP-033, SAP-034
```

Ensure dependencies are met before installation.

**Tip 4: Use Integration Guide**

For cross-SAP questions, always reference the Integration Guide:
- [React SAP Integration Guide](docs/user-docs/guides/react-sap-integration-guide.md)
- Complete tutorials for all 4 stacks
- 7 common integration patterns
- 4 migration guides
- Comprehensive troubleshooting

This saves 60-70% tokens vs reading individual SAP docs.

**Tip 5: Evidence-Based Recommendations**

All React SAPs are backed by:
- 30+ production case studies (Vercel, Google, Microsoft, Linear, etc.)
- Validated time savings metrics
- Real-world performance benchmarks
- RT-019 research extraction

Reference case studies when explaining benefits.

---

## Example Claude Code Session

```markdown
User: "Help me set up task tracking for this project"

Claude (Phase 1: Orientation):
- Read /CLAUDE.md (this file) for project overview
- Navigate to docs/skilled-awareness/AGENTS.md
- Find SAP-015 (task-tracking) in catalog
- Read docs/skilled-awareness/task-tracking/AGENTS.md for quick overview

Claude (Phase 2: Implementation):
- Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
- Follow step-by-step installation:
  1. Install beads CLI: npm install -g @beads/bd
  2. Initialize: bd init
  3. Create first tasks
  4. Update AGENTS.md with beads patterns

Claude (Phase 3: If Needed):
- Read protocol-spec.md for complete CLI reference
- Read capability-charter.md for design rationale
- Review integration patterns with SAP-001 and SAP-010

Result: SAP-015 successfully adopted, task tracking operational
```

---

## Support & Resources

### Documentation

- **SAP Framework**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- **Agent Awareness**: [docs/skilled-awareness/agent-awareness/](docs/skilled-awareness/agent-awareness/)
- **SAP Catalog**: [sap-catalog.json](sap-catalog.json)
- **SAP Index**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

### Key Commands

```bash
# SAP discovery
cat sap-catalog.json | grep -A 10 '"id": "SAP-'

# Task tracking (if SAP-015 adopted)
bd ready --json
bd list --status open --json

# Coordination (if SAP-001 adopted)
cat inbox/coordination/active.jsonl

# Event history (if SAP-010 adopted)
tail -n 20 .chora/memory/events/development.jsonl
```

### Navigation

- **Need SAP documentation?** → [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)
- **Need developer setup?** → [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)
- **Need user guides?** → [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)
- **Need project plans?** → [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

---

## Version History

- **1.1.0** (2025-11-09): React SAP Excellence Initiative completion
  - Added comprehensive React Development with SAPs section
  - 16 React SAPs categorized and documented
  - Progressive loading strategy for React development
  - 4 common React workflows with examples
  - Decision trees for provider selection
  - Stack combinations and integration patterns
  - Quick reference to React SAP Integration Guide

- **1.0.0** (2025-11-04): Initial root CLAUDE.md for chora-base
  - Complete navigation tree to 4 domains
  - Progressive context loading strategy
  - Claude Code vs Claude Desktop patterns
  - Common workflows and pitfalls
  - SAP catalog quick reference

---

**Next Steps**:
1. Determine your task domain (user docs, dev docs, project docs, SAPs)
2. Navigate to appropriate domain AGENTS.md
3. Read domain CLAUDE.md for Claude-specific patterns
4. Dive into specific SAP or documentation as needed

**Remember**: "Nearest file wins" - progressively load context from root → domain → capability → feature → component.

Happy navigating! 🚀
