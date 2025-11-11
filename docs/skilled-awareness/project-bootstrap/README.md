# SAP-003: Project Bootstrap & Scaffolding

**Version:** 1.1.0 | **Status:** Active | **Maturity:** Production

> Zero-dependency Python project generation with blueprint-based templating—create production-ready projects in 1-2 minutes with 100+ files, quality gates, and AI agent support.

---

## Quick Start (5 minutes)

```bash
# Create new MCP server project from chora-base template
just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp

# Or use Python script directly
python scripts/create-model-mcp-server.py \
    --name "Weather MCP" \
    --namespace weather \
    --output ~/projects/weather-mcp
```

**Output**: Production-ready project with:
- ✅ 100+ files (src/, tests/, docs/, docker/, .github/)
- ✅ Quality gates (pytest 85%+ coverage, ruff, mypy)
- ✅ CI/CD (10 GitHub Actions workflows)
- ✅ Documentation (Diátaxis framework, AGENTS.md, CLAUDE.md)
- ✅ Git repository initialized with proper .gitignore

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete setup guide (5-min read)

---

## What Is It?

SAP-003 provides **zero-dependency project generation** using a blueprint-based templating system. It orchestrates copying static template files, renaming package directories, processing variable substitution, and initializing git repositories—all using only Python stdlib (no Copier, Cookiecutter, or Jinja2).

**Key Innovation**: 1-2 minute setup (vs 30-60 minutes manual) with 100% quality gate compliance out-of-the-box, using simple `{{ var }}` substitution for human and machine readability.

---

## When to Use

Use SAP-003 when you need to:

1. **Bootstrap new Python projects** - Start with production-ready structure in 1-2 minutes
2. **Create MCP servers** - Generate FastMCP-based Model Context Protocol servers
3. **Enforce project standards** - Ensure all projects follow consistent structure and quality gates
4. **Reduce setup friction** - Eliminate 30-60 minutes of manual configuration per project
5. **Support AI agents** - Provide agent-optimized project generation (20-40 second execution)

**Not needed for**: Adding SAPs to existing projects (use SAP adoption blueprints), or modifying template structure (edit static-template/ directly)

---

## Key Features

- ✅ **Zero Dependencies** - Uses only Python stdlib (no external templating libraries)
- ✅ **Blueprint-Based** - Simple `{{ var }}` substitution (human and machine readable)
- ✅ **Fast Setup** - 1-2 minutes from command to production-ready project
- ✅ **100+ Files Generated** - Complete project scaffold with src/, tests/, docs/, docker/, .github/
- ✅ **Quality Gates Included** - pytest (85%+ coverage), ruff (linting), mypy (types), pre-commit hooks
- ✅ **CI/CD Ready** - 10 GitHub Actions workflows (test, lint, security, release)
- ✅ **Documentation Framework** - Diátaxis structure, AGENTS.md, CLAUDE.md, README, ROADMAP
- ✅ **Agent-Optimized** - 20-40 second generation for AI agents
- ✅ **Validation-First** - Validates generated projects before declaring success

---

## Common Workflows

### 1 Primary Command

#### **create-mcp-server** - Generate MCP Server Project
```bash
just create-mcp-server "Project Name" namespace ~/output/path

# Examples:
just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp
just create-mcp-server "Task Manager" taskmgr ~/projects/task-manager-mcp
just create-mcp-server "Database Query" dbquery ~/projects/dbquery-mcp

# Requirements:
# - PROJECT_NAME: Human-readable name (e.g., "Weather MCP")
# - NAMESPACE: 3-20 chars, lowercase, alphanumeric, starts with letter (e.g., "weather")
# - OUTPUT_PATH: Directory to create project (must not exist)
```

### Direct Script Usage

```bash
# Full command with all options
python scripts/create-model-mcp-server.py \
    --name "Weather MCP" \
    --namespace weather \
    --output ~/projects/weather-mcp

# Interactive mode (prompts for inputs)
python scripts/create-model-mcp-server.py
```

---

## Integration

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-002** (Chora-Base) | Template Source | Bootstrap uses chora-base static-template/ as project scaffold |
| **SAP-014** (MCP Server) | MCP Generation | Creates FastMCP-based servers with Chora MCP Conventions v1.0 |
| **SAP-004** (Testing) | Quality Gates | Generated projects include pytest with 85%+ coverage target |
| **SAP-005** (CI/CD) | Automation | Generated projects include 10 GitHub Actions workflows |
| **SAP-006** (Quality Gates) | Pre-commit | Generated projects include pre-commit hooks (ruff, mypy) |
| **SAP-007** (Documentation) | Docs Framework | Generated projects use Diátaxis structure |
| **SAP-009** (Agent Awareness) | AI Support | Generated projects include AGENTS.md, CLAUDE.md |
| **SAP-011** (Docker) | Containerization | Generated projects include multi-stage Dockerfile |

**Cross-SAP Workflow Example**:
```bash
# 1. Generate project (SAP-003)
just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp

# 2. Navigate and verify (SAP-004)
cd ~/projects/weather-mcp
pytest --cov=src --cov-fail-under=85

# 3. Run quality gates (SAP-006)
pre-commit run --all-files

# 4. Start development (SAP-012)
just test                      # Run tests
just lint                      # Check linting
just format                    # Format code
just type-check                # Type checking

# 5. Adopt additional SAPs as needed
# - SAP-001 (Inbox): Cross-repo coordination
# - SAP-010 (A-MEM): Event-sourced memory
# - SAP-015 (Beads): Task tracking
```

---

## 📂 Generated Project Structure

```
my-project/
├── src/
│   └── my_project/            # Python package (renamed from __package_name__)
│       ├── __init__.py
│       ├── server.py          # FastMCP server entry point
│       └── mcp/               # Chora MCP Conventions v1.0
│           ├── __init__.py
│           └── utils.py
├── tests/                     # pytest test suite (85%+ coverage target)
│   ├── test_server.py
│   └── conftest.py
├── scripts/                   # Development automation (20 scripts)
│   ├── install-inbox-protocol.py
│   ├── validate-links.py
│   └── ...
├── docker/                    # Multi-stage Dockerfile + compose
│   ├── Dockerfile
│   ├── Dockerfile.test
│   └── docker-compose.yml
├── .github/workflows/         # 10 GitHub Actions workflows
│   ├── test.yml
│   ├── lint.yml
│   ├── security.yml
│   └── ...
├── docs/                      # Diátaxis documentation framework
│   ├── user-docs/
│   ├── dev-docs/
│   ├── project-docs/
│   └── skilled-awareness/
├── .pre-commit-config.yaml    # Pre-commit hooks (ruff, mypy)
├── pyproject.toml             # Python project config
├── justfile                   # Command automation (30+ recipes)
├── README.md                  # Project overview
├── AGENTS.md                  # AI agent guidance
├── CLAUDE.md                  # Claude-specific patterns
├── CHANGELOG.md               # Version history
└── ROADMAP.md                 # Future capabilities
```

**Total**: 100+ files, production-ready from day 1

---

## 🎓 Generation Workflow

### 5-Step Blueprint-Based Generation

```
┌─────────────────────────────────────────────────┐
│  Step 1: Gather Variables                      │
│  - Prompt: project_name, author_name, email    │
│  - Derive: project_slug, package_name,         │
│    mcp_namespace                                │
│  - Validate: email format, slug format, semver │
└─────────────────┬───────────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────────┐
│  Step 2: Copy Static Template                  │
│  - shutil.copytree(static-template/, target/)  │
│  - Copy 100+ files preserving structure        │
└─────────────────┬───────────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────────┐
│  Step 3: Rename Package Directories            │
│  - Find all __package_name__ directories       │
│  - Rename to actual package_name               │
│  - Example: src/__package_name__/ →            │
│    src/weather/                                 │
└─────────────────┬───────────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────────┐
│  Step 4: Process Blueprints                    │
│  - Load 12 .blueprint files                    │
│  - Replace {{ var }} with actual values        │
│  - Write to target files                       │
│  - Example: {{ project_name }} → "Weather MCP" │
└─────────────────┬───────────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────────┐
│  Step 5: Initialize Git Repository             │
│  - git init                                     │
│  - Add .gitignore (500+ patterns)              │
│  - Optional: git add . && git commit -m        │
│    "Initial commit"                             │
└─────────────────────────────────────────────────┘
```

**Time**: 20-40 seconds for AI agents, 1-2 minutes for humans (including prompts)

---

## Success Metrics

- **Setup Time**: 1-2 minutes (vs 30-60 minutes manual)
- **Quality Gate Compliance**: 100% out-of-the-box (pytest 85%+ coverage, ruff, mypy pass)
- **CI/CD Ready**: 10 GitHub Actions workflows included
- **File Count**: 100+ files generated with consistent structure
- **Agent Execution**: 20-40 seconds for automated generation
- **Time Savings**: 95% reduction (1-2 min vs 30-60 min manual setup)

---

## Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete technical specification (generation flow, validation, blueprints) (32KB)
- **[AGENTS.md](AGENTS.md)** - AI agent patterns for project generation (19KB, 10-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific workflows (13KB, 7-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Step-by-step usage guide (21KB, 10-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design (13KB)
- **[ledger.md](ledger.md)** - Production adoption metrics and version history (30KB)

---

## Troubleshooting

### Problem 1:`create-mcp-server` fails with "Output directory already exists"

**Solution**: Choose a different output path or remove existing directory:
```bash
# Remove existing directory
rm -rf ~/projects/weather-mcp

# Or choose new path
just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp-v2
```

---

### Problem 2:Invalid namespace error (must be 3-20 chars, lowercase, alphanumeric)

**Solution**: Choose valid namespace:
```bash
# ❌ Invalid namespaces
just create-mcp-server "Weather" Weather-MCP ~/output  # Contains hyphen, uppercase
just create-mcp-server "Weather" ab ~/output           # Too short (<3 chars)
just create-mcp-server "Weather" 123weather ~/output   # Starts with number

# ✅ Valid namespaces
just create-mcp-server "Weather MCP" weather ~/output
just create-mcp-server "Weather MCP" wthr ~/output
just create-mcp-server "Weather MCP" weathermcp ~/output
```

---

### Problem 3:Generated project fails pytest

**Solution**: This should NOT happen (100% quality gate compliance guaranteed). If it does, report bug:
```bash
cd ~/projects/weather-mcp
pytest -vv --tb=short  # Get detailed failure info

# Report issue with output
gh issue create --title "[SAP-003] Generated project fails pytest" --body "..."
```

---

### Problem 4:Want to customize template before generation

**Solution**: Edit static-template/ or blueprints/ in chora-base before running generation:
```bash
# Example: Add custom script to template
echo "#!/bin/bash\necho 'Custom script'" > static-template/scripts/custom.sh

# Generate project (will include custom script)
just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp
```

---

## 📞 Support

- **Documentation**: Read [protocol-spec.md](protocol-spec.md) for complete technical reference
- **Issues**: Report bugs via GitHub issues with `[SAP-003]` prefix
- **Feedback**: Log adoption feedback in [ledger.md](ledger.md)
- **Customization**: Edit static-template/ or blueprints/ in chora-base repository

---

## 🔍 Blueprint System

### 12 Blueprint Files

Blueprint files use simple `{{ var }}` substitution (no complex templating logic):

1. **pyproject.toml.blueprint** - Python project configuration
2. **README.md.blueprint** - Project overview
3. **AGENTS.md.blueprint** - AI agent guidance
4. **CHANGELOG.md.blueprint** - Version history
5. **ROADMAP.md.blueprint** - Future capabilities
6. **CLAUDE.md.blueprint** - Claude-specific patterns
7. **.gitignore.blueprint** - Git ignore patterns
8. **.env.example.blueprint** - Environment variables
9. **package__init__.py.blueprint** - Package init
10. **server.py.blueprint** - FastMCP server
11. **mcp__init__.py.blueprint** - MCP conventions
12. **conftest.py.blueprint** - pytest fixtures

**Example Blueprint**:
```python
# server.py.blueprint
"""{{ project_name }}: FastMCP server implementation."""

from fastmcp import FastMCP

mcp = FastMCP("{{ mcp_namespace }}")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
```

**After substitution** (with `project_name="Weather MCP"`, `mcp_namespace="weather"`):
```python
# server.py
"""Weather MCP: FastMCP server implementation."""

from fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
```

---

**Version History**:
- **1.1.0** (2025-11-04) - Added justfile recipe, FastMCP integration, Chora MCP Conventions v1.0
- **1.0.0** (2025-06-15) - Initial zero-dependency blueprint-based generation with 100+ files

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
