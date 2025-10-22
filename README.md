# chora-base

**Python Project Template for LLM-Intelligent Development**

A comprehensive [Copier](https://copier.readthedocs.io/) template for Python projects with built-in support for AI coding agents, following agentic coding best practices.

## What is chora-base?

chora-base is a production-ready Python project template featuring:

- **🤖 AI Agent Support** - Machine-readable AGENTS.md, stateful memory system
- **📝 Comprehensive Documentation** - README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING
- **✅ Quality Gates** - Pre-commit hooks, 85%+ test coverage, type checking, linting
- **🔄 CI/CD Ready** - GitHub Actions workflows (test, lint, release, security)
- **🐳 Docker Support** - Production-ready containerization (40% smaller images, 6x faster builds)
- **🧠 Memory Infrastructure** - Event log, knowledge graph, trace context for cross-session learning
- **🛠️ Developer Experience** - Setup scripts, justfile tasks, automated tooling

**📖 [Read the full benefits guide](docs/BENEFITS.md)** - Learn how chora-base saves 52+ hours per project and delivers ROI through automation, AI-native workflows, and production-ready infrastructure.

## Recent Updates

### v2.0.0 (2025-10-22) - Nested AGENTS.md Architecture 🏗️

**BREAKING CHANGE**: Refactored monolithic AGENTS.md into modular, topic-specific guides.

**"Nearest File Wins" Principle** - Agents read the AGENTS.md closest to the code they're working on:
- **Main AGENTS.md**: Project overview, architecture, PR workflow (1,239 lines, 51% reduction)
- **tests/AGENTS.md**: Testing guide (run tests, coverage, linting, troubleshooting)
- **.chora/memory/AGENTS.md**: Memory system (event log, knowledge graph, A-MEM workflows)
- **docker/AGENTS.md**: Docker operations (build, deploy, optimization)
- **scripts/AGENTS.md**: Automation scripts reference

**Benefits**: Reduced cognitive load, improved discoverability, scalable architecture

**Impact**: Documentation-only change (no code changes required)

📄 [CHANGELOG](CHANGELOG.md) | 📦 [Upgrade Guide](docs/upgrades/v1.9.3-to-v2.0.0.md) | 📖 [Research](docs/research/)

### v1.9.3 (2025-10-22) - Advanced Agent Patterns 🧠

**Research-Aligned Enhancements**

Based on "Agentic Coding Best Practices Research," added ~150 lines of advanced agent documentation:

- **Super-Tests** - System-level validation guidance (test workflows, not just units)
- **Memory Architecture** - 3-tier model documentation (ephemeral → persistent → structured)
- **Advanced Query Patterns** - 5 production-ready patterns (semantic search, temporal analysis, confidence filtering)

📄 [CHANGELOG](CHANGELOG.md) | 📦 [Upgrade Guide](docs/upgrades/v1.9.2-to-v1.9.3.md)

### v1.9.2 (2025-10-22) - Ergonomic Agent Interfaces 🤖

**AGENTS.md Enhancements - Feature Discoverability**

Made optional features discoverable for AI agents by surfacing them in AGENTS.md:

- **Docker Operations** - 17 commands now documented with workflows
- **Documentation System** - Health metrics, query API, extraction tools
- **CI/CD Expectations** - What CI checks, how to verify locally
- **Pattern Established** - Standard template for future features

**Key Principle:** AGENTS.md is the **capability catalog** linking to detailed guides, with clear template vs. adopter responsibilities.

📄 [CHANGELOG](CHANGELOG.md) | 📦 [Upgrade Guide](docs/upgrades/v1.9.1-to-v1.9.2.md)

### v1.9.1 (2025-10-22) - Docker Enhancements 🐳

Production-proven Docker patterns integrated from three adopter projects:

- **40% smaller images** (500MB → 150-250MB via wheel builds)
- **6x faster builds** (GitHub Actions cache: 3min → 30sec)
- **100% CI reliability** (eliminates system package conflicts)
- **Multi-platform support** (native ARM64 for Apple Silicon)

New justfile commands: `docker-build-multi`, `docker-verify`, `docker-shell`, `docker-push`, `docker-release`

📄 [CHANGELOG](CHANGELOG.md) | 📦 [Upgrade Guide](docs/upgrades/v1.9.0-to-v1.9.1.md)

## Features

### Core Infrastructure

- ✅ **Project Structure** - Well-organized src layout with clear separation of concerns
- ✅ **Dependency Management** - Modern pyproject.toml configuration
- ✅ **Documentation** - 5-doc hierarchy (README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING, AGENTS)
- ✅ **Testing** - pytest setup with coverage reporting (85%+ threshold)
- ✅ **Code Quality** - ruff (linting), black (formatting), mypy (type checking)
- ✅ **Git Hooks** - Pre-commit hooks for quality enforcement
- ✅ **Docker** - Production containerization with multi-stage builds (optional)

### AI Agent Features (Optional)

- 🤖 **AGENTS.md** - Machine-readable instructions (OpenAI/Google/Sourcegraph standard)
- 🎯 **Vision & Strategic Design** - Long-term capability evolution framework
  - Exploratory vision documents (non-committed future directions)
  - Strategic design guidance for AI agents
  - Decision frameworks (refactor now vs. defer)
  - Quarterly review process
- 🧠 **Memory System** - Event log, knowledge graph, trace context
  - Event correlation via `CHORA_TRACE_ID`
  - Zettelkasten-inspired knowledge notes
  - Per-agent profiles and learned patterns
- 🔧 **CLI Tools** - Query events, manage knowledge, track learning

### Project Types Supported

- **MCP Server** - Model Context Protocol servers (e.g., Claude Desktop, Cursor)
- **Library/Package** - Python libraries for PyPI distribution
- **CLI Tool** - Command-line applications
- **Web Service/API** - FastAPI or similar web services

## Quick Start

### Prerequisites

- Python 3.11+ (3.12+ recommended)
- [Copier](https://copier.readthedocs.io/) (`pipx install copier`)
- Git

### New Project

```bash
# Install copier
pipx install copier

# Generate project from template
copier copy gh:liminalcommons/chora-base my-new-project

# Answer prompts (project name, author, features, etc.)

# Setup and start developing
cd my-new-project
./scripts/setup.sh
```

### Existing Project (Adoption)

Want to adopt chora-base infrastructure in your existing Python project? **No submodule required** - Copier generates files directly into your repo.

```bash
# In your existing repo (make sure you have a clean git state!)
copier copy gh:liminalcommons/chora-base .

# Answer prompts (use your existing project name/details)

# Review what changed
git diff

# Selectively keep what you want
git add -p  # Interactive staging
git commit -m "feat: Adopt chora-base template infrastructure"

# Later: Update incrementally (smart merge, not rip-and-replace)
copier update
```

**How It Works:**
- Copier generates files directly into your repo (no linking/submodule)
- You review changes with `git diff` and keep what makes sense
- `.copier-answers.yml` tracks template version for future updates
- `copier update` merges improvements like `git merge` (not blind overwrite)

**See Also:**
- [How-To: Rip-and-Replace Existing Server](docs/how-to/02-rip-and-replace-existing-server.md) - Complete 8-phase migration guide
- [Rip-and-Replace Decision Matrix](docs/reference/rip-and-replace-decision-matrix.md) - When to adopt vs stay custom

### Template Questions

When you run `copier copy`, you'll be asked:

**Project Metadata:**
- `project_name` - Your project name (kebab-case)
- `project_description` - Short description
- `author_name`, `author_email` - Your contact info
- `github_username` - GitHub username/org

**Python Configuration:**
- `python_version` - Minimum Python version (3.11, 3.12, 3.13)

**Project Type:**
- `project_type` - mcp_server, library, cli_tool, or web_service

**Features:**
- `include_memory_system` - Agent Memory System (.chora/memory/)
- `include_agents_md` - Machine-readable AGENTS.md
- `include_cli` - CLI interface (Click or Typer)
- `include_tests` - Testing infrastructure (pytest)
- `include_pre_commit` - Pre-commit hooks (ruff, black, mypy)
- `include_github_actions` - CI/CD workflows
- `include_justfile` - Task automation with just
- `include_docker` - Docker configuration (**v1.9.1: Enhanced with production patterns**)
  - `production` strategy: Multi-stage builds + docker-compose orchestration
  - `ci-only` strategy: Dockerfile.test for CI isolation
  - **New in v1.9.1:** 40% smaller images, 6x faster builds, multi-arch support

**Documentation:**
- `include_contributing` - CONTRIBUTING.md
- `include_development_docs` - DEVELOPMENT.md
- `include_troubleshooting` - TROUBLESHOOTING.md

**License:**
- `license` - MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, or Proprietary

## What You Get

### Directory Structure

```
my-awesome-project/
├── .chora/                      # Agent memory (optional)
│   └── memory/
│       ├── README.md            # Memory system docs
│       ├── events/              # Event log (gitignored)
│       ├── knowledge/           # Knowledge notes (gitignored)
│       └── profiles/            # Agent profiles (gitignored)
├── .github/                     # GitHub Actions workflows
│   └── workflows/
│       ├── test.yml             # Run tests on push/PR
│       ├── lint.yml             # Linting checks
│       ├── smoke.yml            # Quick smoke tests
│       ├── release.yml          # Automated releases
│       ├── codeql.yml           # Security scanning
│       └── ...
├── docs/                        # Documentation
│   ├── DEVELOPMENT.md           # Developer deep dive
│   └── TROUBLESHOOTING.md       # Common issues
├── scripts/                     # Automation scripts
│   ├── setup.sh                 # One-command setup
│   ├── check-env.sh             # Environment validation
│   ├── integration-test.sh      # Integration testing
│   └── ...
├── src/                         # Source code
│   └── my_awesome_project/
│       ├── __init__.py
│       ├── server.py            # (MCP server) or
│       ├── cli/                 # (CLI tool) or
│       └── memory/              # (Memory system)
├── tests/                       # Test suite
│   ├── test_*.py
│   └── conftest.py
├── .dockerignore                # Docker build exclusions (optional)
├── .editorconfig                # Editor configuration
├── .gitignore                   # Git ignore patterns
├── .pre-commit-config.yaml      # Pre-commit hooks
├── AGENTS.md                    # Machine-readable docs
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # How to contribute
├── Dockerfile                   # Production build (optional)
├── Dockerfile.test              # CI/test build (optional)
├── docker-compose.yml           # Service orchestration (optional)
├── justfile                     # Task automation
├── pyproject.toml               # Project config
└── README.md                    # This file
```

## Documentation

chora-base uses the [Diátaxis framework](https://diataxis.fr/) to serve two first-class audiences:
1. **Human Developers** - Learning, understanding, decision-making
2. **AI Agents** - Task execution, reference lookup, machine-readable instructions

### Documentation Structure

```
docs/
├── DOCUMENTATION_PLAN.md     # Complete documentation strategy
├── tutorials/                # Learning-oriented (for humans)
│   ├── 01-first-mcp-server.md
│   └── 02-rip-and-replace-migration.md
├── how-to/                   # Task-oriented (humans + agents)
│   ├── 01-generate-new-mcp-server.md
│   ├── 02-rip-and-replace-existing-server.md
│   └── ...
├── reference/                # Information-oriented (humans + agents)
│   ├── template-configuration.md
│   ├── rip-and-replace-decision-matrix.md
│   └── ...
└── explanation/              # Understanding-oriented (for humans)
    ├── why-rip-and-replace.md
    ├── memory-system-architecture.md
    └── ...
```

### For Human Developers

- **New to chora-base?** Start with [Tutorial: Your First MCP Server](docs/tutorials/01-first-mcp-server.md) (coming soon)
- **Migrating existing project?** See [How-To: Rip-and-Replace](docs/how-to/02-rip-and-replace-existing-server.md)
- **Need quick reference?** Check [Template Configuration](docs/reference/template-configuration.md)
- **Want to understand concepts?** Read [Explanations](docs/explanation/)

### For AI Agents

- **Quick start:** [How-To: Generate New MCP Server](docs/how-to/01-generate-new-mcp-server.md)
- **Complete reference:** [Template Configuration](docs/reference/template-configuration.md)
- **Decision support:** [Rip-and-Replace Decision Matrix](docs/reference/rip-and-replace-decision-matrix.md)
- **Machine-readable instructions:** AGENTS.md (generated for each project)

---

## Generated Project Structure

```
my-awesome-project/
├── .chora/memory/            # Agent memory (if included)
├── .github/workflows/        # CI/CD (7 workflows)
├── docs/                     # Documentation
├── scripts/                  # Automation (18 scripts)
├── CONTRIBUTING.md              # Contribution guide
├── justfile                     # Task automation
├── LICENSE                      # Project license
├── pyproject.toml               # Python project config
└── README.md                    # Project overview
```

### Scripts Included

All projects get these automation scripts:

- `setup.sh` - One-command setup (venv, deps, hooks, tests)
- `check-env.sh` - Validate environment (Python version, dependencies)
- `venv-create.sh`, `venv-clean.sh` - Virtual environment management
- `smoke-test.sh` - Quick smoke tests (<30s)
- `integration-test.sh` - Full integration testing
- `pre-merge.sh` - Pre-merge validation (quality gates)
- `diagnose.sh` - Automated diagnostics

### GitHub Actions Workflows

- **test.yml** - Run tests on Python 3.11 and 3.12
- **lint.yml** - Linting with ruff, formatting with black, type checking with mypy
- **smoke.yml** - Quick smoke tests on every push
- **release.yml** - Automated releases to PyPI with version bumping
- **codeql.yml** - Security scanning with CodeQL
- **dependency-review.yml** - Dependency vulnerability scanning
- **dependabot-automerge.yml** - Auto-merge Dependabot PRs

## Customization

### After Generation

1. **Update README.md** - Fill in project-specific features, usage examples
2. **Configure .env** - Add your environment variables
3. **Customize pyproject.toml** - Add dependencies, adjust metadata
4. **Write your code** - Start in `src/your_package/`
5. **Add tests** - Tests in `tests/`
6. **Update AGENTS.md** - Add project-specific agent workflows (if included)

### Optional Components

You can remove optional components after generation:

```bash
# Remove memory system
rm -rf .chora/memory src/your_package/memory

# Remove CLI tools
rm -rf src/your_package/cli

# Remove justfile (use scripts directly)
rm justfile

# Remove Docker
rm Dockerfile docker-compose.yml
```

## Updating from Template

Copier supports updating projects when the template evolves:

```bash
# Update to latest template version
cd /path/to/your-project
copier update

# Or update to specific version
copier update --vcs-ref=v1.4.0
```

This will:
1. Merge template changes with your project
2. Ask about conflicts
3. Preserve your customizations

### Upgrade Guides for AI Agents & Humans

chora-base provides comprehensive upgrade documentation with AI-optimized decision trees:

**Upgrade Philosophy**:
- [Upgrade Philosophy & Decision Framework](docs/upgrades/PHILOSOPHY.md) - Understand chora-base's upgrade promise, displacement policy, and customization preservation strategies

**Version-Specific Guides**:
- [v1.3 → v1.4](docs/upgrades/v1.3-to-v1.4.md) - PyPI setup + `just` as primary interface
- [More upgrade guides...](docs/upgrades/) - Step-by-step migration instructions

**For AI Agents**:
Each upgrade guide includes:
- Decision trees (structured IF/THEN criteria)
- Displacement analysis (required vs optional changes)
- Merge strategies (preserve customizations)
- Knowledge migration patterns (ecosystem-wide vs project-specific)

**For Human Developers**:
Each upgrade guide includes:
- Time estimates and effort assessment
- Example upgrade sessions (real transcripts)
- Conflict resolution strategies
- Rollback procedures

**In Generated Projects**:
Every generated project includes `UPGRADING.md` with:
- Customization tracking (document what you've changed)
- Upgrade workflow (step-by-step checklist)
- Version history (track your upgrade path)

## Examples

See `examples/` directory for sample projects:

- **minimal-mcp** - Minimal MCP server (no memory, basic structure)
- **full-featured** - All features enabled (memory, CLI, tests, docs)
- **python-library** - Library/package template

## Architecture

### Memory System (.chora/memory/)

When `include_memory_system=true`, you get:

**Event Log** (`src/your_package/memory/event_log.py`):
- Append-only JSONL storage with monthly partitions
- Query by trace_id, event_type, status, time range
- Aggregate statistics (count, avg_duration)

**Knowledge Graph** (`src/your_package/memory/knowledge_graph.py`):
- Markdown notes with YAML frontmatter (Zettelkasten-inspired)
- Bidirectional linking between notes
- Tag-based organization and search
- Confidence tracking (low/medium/high)

**Trace Context** (`src/your_package/memory/trace.py`):
- `CHORA_TRACE_ID` environment variable propagation
- TraceContext context manager for scoped trace IDs
- OpenTelemetry-compatible UUID format

**CLI Tools** (`src/your_package/cli/main.py`):
- Query events: `your-project-memory query --type "..." --since "24h"`
- Trace timeline: `your-project-memory trace abc123`
- Knowledge search: `your-project-memory knowledge search --tag "..."`

### AGENTS.md Structure

When `include_agents_md=true`, you get machine-readable documentation following the OpenAI/Google/Sourcegraph standard:

- **Project Overview** - Architecture, key components
- **Dev Environment Tips** - Prerequisites, installation
- **Testing Instructions** - Test tiers, coverage requirements
- **PR Instructions** - Branch naming, commit format
- **Architecture Overview** - Design patterns, constraints
- **Common Tasks** - Detailed workflows for agents
- **Project Structure** - Annotated directory tree
- **Troubleshooting** - Common issues with solutions

## Rationale

### Why chora-base?

**Problem:** Every new Python project requires:
- Setting up testing, linting, formatting
- Configuring CI/CD workflows
- Writing boilerplate docs (README, CONTRIBUTING)
- Implementing quality gates
- Adding AI agent support (AGENTS.md, memory system)

**Solution:** chora-base provides all of this out-of-the-box, validated in production through mcp-n8n (Phase 0-4.6).

### Design Principles

1. **Agentic Coding Best Practices**
   - AGENTS.md standard (OpenAI/Google/Sourcegraph)
   - Stateful memory (A-MEM principles)
   - Zettelkasten-inspired knowledge organization

2. **Developer Experience First**
   - One-command setup (`./scripts/setup.sh`)
   - Automated quality gates (pre-commit hooks)
   - Comprehensive documentation (5-doc hierarchy)

3. **Production-Ready Defaults**
   - 85%+ test coverage threshold
   - Type checking with mypy strict mode
   - Security scanning with CodeQL
   - Automated dependency updates

4. **Ecosystem Integration**
   - Compatible with chora-composer, chora-platform
   - Event schema v1.0 compliance
   - CHORA_TRACE_ID propagation

## Origin Story

chora-base was extracted from [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) after completing Phase 4.5 (LLM-Intelligent Developer Experience) and Phase 4.6 (Agent Self-Service Tools).

**Key Milestones:**
- **Phase 0** - Gateway architecture validation, integration smoke tests
- **Phase 4.5** - AGENTS.md (1,189 lines), memory infrastructure, 14 tests
- **Phase 4.6** - CLI tools (chora-memory), agent profiles
- **Extraction** - Template-ization for chora-base (v1.0.0)

See [docs/PHASE_4.5_SUMMARY.md](https://github.com/liminalcommons/mcp-n8n/blob/main/docs/PHASE_4.5_SUMMARY.md) in mcp-n8n for details.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to improve the template
- Adding new features
- Reporting issues
- Submitting pull requests

## License

MIT License - see [LICENSE](LICENSE)

## Related Projects

- [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) - MCP Gateway & Aggregator (exemplar project)
- [chora-composer](https://github.com/liminalcommons/chora-composer) - Configuration-driven artifact generation
- [chora-platform](https://github.com/liminalcommons/chora-platform) - Shared platform tooling

## Support

- **Issues** - [GitHub Issues](https://github.com/liminalcommons/chora-base/issues)
- **Discussions** - [GitHub Discussions](https://github.com/liminalcommons/chora-base/discussions)
- **Examples** - See `examples/` directory

---

🤖 Generated from mcp-n8n Phase 4.5/4.6 - LLM-Intelligent Developer Experience
