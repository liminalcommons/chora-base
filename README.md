# chora-base

**Python Project Template for AI-Agent-First Development**

A production-ready Python project template designed FOR AI coding agents, not retrofitted. Zero dependencies, one-line setup, works every time.

## What is chora-base?

chora-base is a production-ready Python project template featuring:

- **🤖 AI Agent Support** - Machine-readable AGENTS.md, stateful memory system
- **🎯 Python Utilities** - Optional ergonomic patterns (40-50% code reduction, production-ready)
- **📝 Comprehensive Documentation** - README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING
- **✅ Quality Gates** - Pre-commit hooks, 85%+ test coverage, type checking, linting
- **🔄 CI/CD Ready** - GitHub Actions workflows (test, lint, release, security)
- **🐳 Docker Support** - Production-ready containerization (40% smaller images, 6x faster builds)
- **🧠 Memory Infrastructure** - Event log, knowledge graph, trace context for cross-session learning
- **🛠️ Developer Experience** - Setup scripts, justfile tasks, automated tooling

**📖 [Read the full benefits guide](docs/user-docs/explanation/benefits-of-chora-base.md)** - Learn how chora-base saves 52+ hours per project and delivers ROI through automation, AI-native workflows, and production-ready infrastructure.

## Recent Updates

### v4.2.0 (2025-11-02) - SAP-001 Inbox Coordination Protocol v1.1.0 📥

**NEW:** Production-ready cross-repository coordination system with 5 CLI tools, AI-powered generation, and formalized SLAs.

**What's Included:**
- **5 Production CLI Tools** (2,158 lines total) - Complete inbox protocol automation
  - `install-inbox-protocol.py` (659 lines) - One-command 5-minute installation
  - `inbox-query.py` (531 lines) - Query and filter coordination items (<100ms)
  - `respond-to-coordination.py` (249 lines) - Response automation (<50ms, 94.9% quality)
  - `generate-coordination-request.py` (277 lines) - AI-powered request generation (50% faster drafts)
  - `inbox-status.py` (442 lines) - Visual status dashboard with terminal colors/JSON/markdown output
- **5 SAP Artifacts** (1,202 lines) - Complete documentation package
  - Capability Charter, Protocol Spec, Awareness Guide, Adoption Blueprint, Ledger
- **Event Logging & Traceability** - Append-only JSONL log for coordination history
- **Formalized SLAs** - 48h default, 4h urgent, 1-week backlog response times
- **AGENTS.md Integration** - Inbox status at session startup for generic agents

**Performance & Quality Metrics:**
- **<100ms query time** - Instant coordination item filtering and status checks
- **<50ms response time** - Sub-second response generation
- **94.9% AI quality score** - High-quality automated responses
- **90% time reduction** - Coordination effort cut from hours to minutes
- **Level 3 adoption** - Fully automated, optimized, comprehensive usage

**Quick Start:**
```bash
# Install inbox protocol in your repository (5 minutes)
python scripts/install-inbox-protocol.py --repo-path /path/to/your/repo

# Get visual inbox status (recommended for humans)
python scripts/inbox-status.py

# Query incoming items (filter, format, summarize)
python scripts/inbox-query.py --incoming --format summary

# Generate coordination request with AI assistance
python scripts/generate-coordination-request.py

# Respond to coordination requests with automation
python scripts/respond-to-coordination.py COORD-123 accepted
```

**Use Cases:**
- Cross-repository collaboration in multi-repo ecosystems
- Formal coordination requests with SLAs and event tracking
- Ecosystem-wide capability discovery and coordination
- AI agent queries ("inbox status") with instant visual feedback

📄 [SAP-001 Documentation](docs/skilled-awareness/inbox/) | [CLI Tools Guide](docs/skilled-awareness/inbox/awareness-guide.md) | [CHANGELOG](CHANGELOG.md#420---2025-11-02)

---

### v3.3.0 (2025-10-25) - Claude-Specific Development Framework 🧠

**NEW:** Comprehensive Claude optimization layer with 200k context window strategies, checkpoint patterns, and ROI tracking.

**What's Included:**
- **CLAUDE.md Blueprint** - Claude-specific development guide (peer to AGENTS.md)
- **Pattern Library** (`/claude/`) - 4 comprehensive guides (1,765 lines total)
  - Context Management (progressive loading strategies)
  - Checkpoint Patterns (session state preservation)
  - Metrics Tracking (ROI measurement framework)
  - Framework Templates (proven request patterns)
- **Domain-Specific Guides** - 5 nested CLAUDE.md files (1,353 lines)
  - Tests, Memory, Docker, Scripts, Root template
- **ROI Calculator Utility** - Python metrics tracking (`utils/claude_metrics.py`)
- **CLAUDE_SETUP_GUIDE.md** - Comprehensive Claude setup guide (1,151 lines)

**Claude Advantages:**
- **20-40 second setup** (vs 30-60s for generic agents)
- **2-minute session recovery** (from checkpoints, saves 13-18 minutes)
- **Progressive context loading** (optimize 200k token window)
- **Multi-tool orchestration** (parallel operations)
- **Quantifiable ROI** (time saved, cost savings, quality metrics)

**Quick Start for Claude:**
```bash
# Generate project with Claude optimizations
# See SAP-014 for MCP server setup: docs/skilled-awareness/mcp-server-development/

# Read Claude-specific guides

cat CLAUDE.md                          # Project-specific patterns
cat claude/CONTEXT_MANAGEMENT.md      # Context optimization
cat claude/CHECKPOINT_PATTERNS.md     # State preservation
```

📄  | [Pattern Library](claude/) | [CHANGELOG](CHANGELOG.md#330---2025-10-25)

---

### v3.2.0 (2025-10-26) - Agentic Development Framework 📋

**NEW:** Complete evidence-based development process with 7,440+ lines of workflow documentation.

**What's Included:**
- **8-Phase Development Lifecycle** - Vision → Monitoring with time scales for each phase
- **5,115 lines of workflow docs** - DEVELOPMENT_PROCESS, DDD, BDD, TDD, LIFECYCLE guides
- **1,309 lines of anti-patterns** - Common mistakes and evidence-based solutions
- **1,016 line walkthrough example** - OAuth2 feature from start to finish (14 days, real data)
- **Sprint Planning Templates** - Capacity planning, velocity tracking, burndown charts
- **Release Planning Templates** - RC testing, quality gates, deployment automation
- **Process Metrics Dashboard** - Track quality, velocity, and process adherence

**Evidence-Based Impact:**
- **40-80% defect reduction** (Microsoft Research on TDD)
- **27% efficiency gain** (real-world ROI from OAuth2 walkthrough)
- **8-15 hours saved per feature** (DDD prevents rework)
- **Predictable sprint velocity** (80-90% target with <80% commitment)

**Quick Start:**
```bash
# Generate project with workflows
# See SAP-014 for MCP server setup: docs/skilled-awareness/mcp-server-development/

# Explore workflow documentation
cd my-project
cat dev-docs/workflows/README.md         # Overview
cat dev-docs/workflows/DEVELOPMENT_PROCESS.md  # Complete lifecycle
cat dev-docs/examples/FEATURE_WALKTHROUGH.md   # Real-world example
```

📄 [Workflow Documentation](static-template/dev-docs/workflows/) | [Sprint Planning](static-template/project-docs/sprints/) | [CHANGELOG](CHANGELOG.md#320---2025-10-26)

---

### v3.0.0 (2025-10-25) - AI-Agent-First Architecture 🤖

**BREAKING CHANGE**: Complete architecture redesign for AI coding agents. Zero-dependency setup, no Copier required.

**What Changed:**
- **70% Static Files**: Most files need no variable substitution
- **10 Core Blueprints**: Simple `{{ variable }}` placeholders for essential files
- **Zero Dependencies**: No Copier, no Jinja2 - agents do string replacement
- **One-Line Setup**: `# See SAP-014 for MCP server setup: docs/skilled-awareness/mcp-server-development/` or ask your AI agent
- **Agent-First Guide**: 2,000+ line comprehensive setup guide for autonomous agents

**Migration:**
- v2.x users: See [v2-to-v3 Migration Guide](docs/project-docs/releases/v2-to-v3-migration.md)
- New users: Read [AGENTS.md](AGENTS.md) or ask your AI agent for guidance

📄 [Release Notes](docs/project-docs/releases/v3.0.0-release-notes.md) | [CHANGELOG](CHANGELOG.md#300---2025-10-25)

## Features

### Core Infrastructure

- ✅ **Project Structure** - Well-organized src layout with clear separation of concerns
- ✅ **Dependency Management** - Modern pyproject.toml configuration
- ✅ **Documentation** - 5-doc hierarchy (README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING, AGENTS)
- ✅ **Testing** - pytest setup with coverage reporting (85%+ threshold)
- ✅ **Code Quality** - ruff (linting), black (formatting), mypy (type checking)
- ✅ **Git Hooks** - Pre-commit hooks for quality enforcement
- ✅ **Docker** - Production containerization with multi-stage builds (optional)

### Python Utilities (Optional Ergonomics)

**NEW in v2.1.0** - Production-ready patterns extracted from real-world adopter learnings:

- 🎯 **Input Validation** - Normalize dict/JSON/KV parameters with `@normalize_input()` decorator (~90% less boilerplate)
- 📦 **Response Builders** - Standardized success/error/partial responses with `Response` class (~80-85% reduction)
- 💬 **Error Formatting** - User-friendly messages with fuzzy matching suggestions via `ErrorFormatter`
- 💾 **State Persistence** - Crash-safe JSON storage with `StatefulObject` mixin (~70-75% reduction)

**Benefits:**
- 40-50% code reduction when using all patterns
- Consistent APIs/CLIs out-of-the-box
- Better UX (error suggestions, structured responses)
- Production-ready reliability (atomic writes, type safety)

**Examples:**
```python
# Input normalization (works for REST, CLI, MCP, libraries)
@normalize_input(params=InputFormat.DICT_OR_JSON)
def create_resource(params: dict | None):
    # Accepts both dict and JSON string

# Standardized responses
return Response.success(action="created", data=resource)
return Response.error(error_code="not_found", message=ErrorFormatter.not_found(...))

# Crash-safe state persistence
class MyApp(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")
```

**Documentation:**
- 📖 [Python Patterns Reference](template/user-docs/reference/python-patterns.md.jinja) - Complete API docs
- 📚 [How-To Guides](template/user-docs/how-to/) - Task-oriented usage examples
- 🔬 [Adopter Learnings](docs/dev-docs/research/adopter-learnings-mcp-orchestration.md) - Extraction process

**Source:** Generalized from production Python projects including [mcp-orchestration](https://github.com/chrishayuk/mcp-orchestration) v0.1.3 learnings (tested across multiple project types: Python libraries, CLI tools, API servers, MCP servers)

### AI Agent Features (Optional)

- 🤖 **AGENTS.md** - Machine-readable instructions (OpenAI/Google/Sourcegraph standard)
- 🧠 **CLAUDE.md** (NEW v3.3.0) - Claude-specific optimizations
  - 200k context window management strategies
  - Checkpoint patterns for session continuity
  - Progressive context loading (Phase 1/2/3)
  - Artifact-first development guidance
  - Multi-tool orchestration patterns
- 🎯 **Vision & Strategic Design** - Long-term capability evolution framework
  - Exploratory vision documents (non-committed future directions)
  - Strategic design guidance for AI agents
  - Decision frameworks (refactor now vs. defer)
  - Quarterly review process
- 🧠 **Memory System** - Event log, knowledge graph, trace context
  - Event correlation via `CHORA_TRACE_ID`
  - Zettelkasten-inspired knowledge notes
  - Per-agent profiles and learned patterns
- 📊 **ROI Tracking** (NEW v3.3.0) - Measure AI effectiveness
  - ClaudeROICalculator Python utility
  - Time/cost savings calculation
  - Quality metrics (bug rate, coverage, iterations)
  - Executive summary generation
- 🔧 **CLI Tools** - Query events, manage knowledge, track learning
- 📋 **Task Tracking** (NEW v4.9.0 - SAP-015) - Persistent agent memory with beads
  - Git-backed JSONL task storage
  - Dependency-aware task management (blocks, related, parent-child)
  - Automatic ready-work detection
  - Multi-agent coordination support
  - Integration with inbox (SAP-001) and A-MEM (SAP-010)

### Project Types Supported

- **Library/Package** - Python libraries for PyPI distribution
- **CLI Tool** - Command-line applications
- **Web Service/API** - FastAPI or similar web services
- **MCP Server** - Model Context Protocol servers (with SAP-014)

### Technology-Specific Capabilities

chora-base provides universal Python project infrastructure. For technology-specific capabilities:

- **MCP Server Development**: See [SAP-014 (MCP Server Development)](docs/skilled-awareness/mcp-server-development/) - Comprehensive MCP server development guide with FastMCP patterns, testing strategies, and deployment workflows
- **Future frameworks**: Django, FastAPI, React (planned SAPs)

## Quick Start

### Prerequisites

- Python 3.11+ (3.12+ recommended)
- Git

### With AI Agent (Recommended)

Ask your AI coding agent:

> "Set up a new Python project using chora-base called [project-name]"

Your agent will:
1. Read [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md)
2. Copy static files from [static-template/](static-template/)
3. Copy and customize templates from [static-template/](static-template/)
4. Replace `{{ variables }}` with your project details
5. Initialize git and create first commit

**What the agent needs:**
- `project_name` - Your project name (e.g., "my-awesome-project")
- `author_name` - Your name
- `author_email` - Your email
- `github_username` - Your GitHub username

All other variables are auto-derived or use sensible defaults (see [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md)).

### Manual Setup

For non-agent setup or manual control:

```bash
# Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base

# Run setup script
# Use AI agent to generate from templates my-new-project

# Follow prompts for author, email, GitHub username, etc.

# Start developing
cd my-new-project
./scripts/setup.sh
```

### What You Get

All features are **enabled by default** (v3.0.0 philosophy: comprehensive, not minimal):

- ✅ **Agent Memory System** - Event log, knowledge graph, trace context
- ✅ **Machine-readable AGENTS.md** - Comprehensive agent instructions
- ✅ **Testing Infrastructure** - pytest, 85%+ coverage threshold
- ✅ **Code Quality** - Pre-commit hooks (ruff, black, mypy)
- ✅ **CI/CD** - 7 GitHub Actions workflows
- ✅ **Task Automation** - justfile with common commands
- ✅ **Docker Support** - Production-ready containerization
- ✅ **Full Documentation** - 5-doc hierarchy (README, CONTRIBUTING, DEVELOPMENT, TROUBLESHOOTING, AGENTS)

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
│       ├── main.py              # (application entry point) or
│       ├── cli/                 # (CLI tool) or
│       └── memory/              # (Memory system, optional)
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
│   ├── 01-first-python-project.md
│   └── 02-migrating-existing-project.md
├── how-to/                   # Task-oriented (humans + agents)
│   ├── 01-setup-new-project.md
│   ├── 02-configure-testing.md
│   └── ...
├── reference/                # Information-oriented (humans + agents)
│   ├── template-configuration.md
│   ├── migration-decision-matrix.md
│   └── ...
└── explanation/              # Understanding-oriented (for humans)
    ├── benefits-of-chora-base.md
    ├── memory-system-architecture.md
    └── ...
```

### For Human Developers

- **New to chora-base?** Start with the [Benefits Guide](docs/user-docs/explanation/benefits-of-chora-base.md)
- **Building an MCP server?** See [SAP-014 (MCP Server Development)](docs/skilled-awareness/mcp-server-development/)
- **Need quick reference?** Check [Template Configuration](template/user-docs/reference/template-configuration.md)
- **Want to understand concepts?** Explore [template/user-docs/explanation/](template/user-docs/explanation/)

### For AI Agents

- **Quick start:** [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md)
- **Complete reference:** [Template Configuration](template/user-docs/reference/template-configuration.md)
- **MCP server development:** [SAP-014 Awareness Guide](docs/skilled-awareness/mcp-server-development/awareness-guide.md)
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

chora-base v3.0.0 uses a **static file + blueprint** approach instead of Copier. To update your project:

```bash
# Review what changed in chora-base
cd /path/to/chora-base
git pull
git log --oneline v3.0.0..HEAD

# Manually merge improvements you want
# Compare your project against [static-template/](static-template/)
# Apply changes selectively

# Or ask your AI agent:
# "Update my project to latest chora-base v3.x improvements"
```

**Migration from v2.x to v3.0.0:**
See [v2-to-v3 Migration Guide](docs/project-docs/releases/v2-to-v3-migration.md) for detailed upgrade instructions.

### Upgrade Guides for AI Agents & Humans

chora-base provides comprehensive upgrade documentation with AI-optimized decision trees:

**Upgrade Philosophy**:
- [Upgrade Philosophy & Decision Framework](template/project-docs/project-docs/releases/upgrade-philosophy.md) - Understand chora-base's upgrade promise, displacement policy, and customization preservation strategies

**Upgrade Guide Template**:
- [Upgrade Guide Template](template/project-docs/project-docs/releases/upgrade-guide-template.md) - Template for creating upgrade guides in your projects
- See [CHANGELOG.md](CHANGELOG.md) for chora-base template version history

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

- **minimal-project** - Minimal Python project (no optional features, basic structure)
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

**Solution:** chora-base provides all of this out-of-the-box, validated in production across multiple project types.

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

chora-base was extracted from production Python projects including [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) (an exemplar MCP Gateway & Aggregator project).

**Evolution:**
- Validated across multiple project types (MCP servers, CLI tools, libraries, API services)
- Generalized from real-world patterns and best practices
- Continuously refined through adopter feedback and production usage

**See**: [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) for an example of chora-base in production use.

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

🤖 Universal Python Project Template for AI-Agent-First Development
