# mcp-orchestration

MCP server orchestration and management tools

## Overview

**mcp-orchestration** is a Model Context Protocol (MCP) server that provides [describe your server's capabilities].

This project follows the MCP specification and can be integrated with:
- Claude Desktop
- Cursor
- Other MCP-compatible clients

## Features

- **[Feature 1]** - Description
- **[Feature 2]** - Description
- **Agent Memory System** - Cross-session learning with event log, knowledge graph, and trace correlation
- **CLI Interface** - Command-line tools for [describe CLI purpose]
- **Comprehensive Testing** - 85%+ test coverage with pytest
## Installation

### Quick Setup

```bash
# Clone repository
git clone https://github.com/liminalcommons/mcp-orchestration.git
cd mcp-orchestration

# One-command setup (installs dependencies, hooks, and runs checks)
./scripts/setup.sh
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Application configuration
MCP_ORCHESTRATION_LOG_LEVEL=INFO

# Add your configuration here
```

### Client Configuration

#### Claude Desktop (macOS)

**Development Mode (Editable Install):**
```json
{
  "mcpServers": {
    "mcp-orchestration-dev": {
      "command": "/path/to/mcp-orchestration/.venv/bin/python",
      "args": ["-m", "mcp_orchestration.server"],
      "cwd": "/path/to/mcp-orchestration",
      "env": {
        "MCP_ORCHESTRATION_DEBUG": "1"
      }
    }
  }
}
```

**Production Mode (Installed Package):**
```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration",
      "args": [],
      "env": {}
    }
  }
}
```
## Usage

```bash
# Example command
mcp-orchestration --help

# [Add your specific usage examples here]
```
## Development

### Quick Reference

**Discover all available commands:**
```bash
just --list
```

**Common tasks:**
```bash
just test            # Run test suite
just lint            # Check code style
just pre-merge       # Run all checks (required before PR)
just build           # Build distribution packages
just help            # Show common workflows
```

The [justfile](justfile) is self-documenting - run `just` or `just --list` to see all commands.

### Common Workflows

**Running tests:**
```bash
just test           # Full test suite
just smoke          # Quick smoke tests (~10 sec)
just test-coverage  # With coverage report
```

**Code quality:**
```bash
just lint           # Check style
just lint-fix       # Auto-fix issues
just format         # Format code
just typecheck      # Type checking
just check          # All quality checks
```

**Before creating PR:**
```bash
just pre-merge      # Run lint + test + coverage (required)
```

**Building & releasing:**
```bash
just build                  # Build distribution packages
just prepare-release patch  # Bump version, update CHANGELOG
just publish-test           # Publish to TestPyPI
just publish-prod           # Publish to PyPI
```

**Application:**
```bash
just run            # Start the application
mcp-orchestration  # Or run directly
```

### Without `just` (Fallback)

If `just` installation fails, use commands directly:

| Task | Command |
|------|---------|
| Run tests | `pytest` |
| Build | `./scripts/build-dist.sh` |
| Lint | `ruff check src/mcp_orchestration tests` |
| Format | `black src/mcp_orchestration tests` |
| Pre-merge | `./scripts/pre-merge.sh` |
| Type check | `mypy src/mcp_orchestration` |

See [justfile](justfile) for complete command mappings.
## Documentation

This project follows the [Diátaxis framework](https://diataxis.fr/) with three documentation directories:

### For End Users (user-docs/)
Learn how to **use** mcp-orchestration:
- **[Getting Started Tutorial](user-docs/tutorials/01-getting-started.md)** - Learn the basics
- **[How-To Guides](user-docs/how-to/)** - Solve specific problems
- **[API Reference](user-docs/reference/)** - Look up specifications
- **[Explanations](user-docs/explanation/)** - Understand concepts

### For Project Planning (project-docs/)
Project roadmap and architecture decisions:
- **[ROADMAP.md](project-docs/ROADMAP.md)** - Long-term vision and milestones
- **[Release Notes](project-docs/releases/)** - Version history and changes
- **[Architecture Decisions](project-docs/decisions/)** - ADRs and design choices

### For Contributors (dev-docs/)
Learn how to **build** mcp-orchestration:
- **[CONTRIBUTING.md](dev-docs/CONTRIBUTING.md)** - Contribution guidelines
- **[DEVELOPMENT.md](dev-docs/DEVELOPMENT.md)** - Developer setup and architecture
- **[TROUBLESHOOTING.md](dev-docs/TROUBLESHOOTING.md)** - Common development issues
- **[Vision Documents](dev-docs/vision/)** - Strategic design guidance
### For AI Coding Agents
- **[AGENTS.md](AGENTS.md)** - Machine-readable instructions (OpenAI/Google standard)
**Documentation Standard:**
- **[DOCUMENTATION_STANDARD.md](DOCUMENTATION_STANDARD.md)** - Writing guidelines and templates

## Project Principles

This project follows best practices for:

- **Code Quality** - Linting (ruff), formatting (black), type checking (mypy)
- **Testing** - Comprehensive test suite with 85%+ coverage
- **Documentation** - Clear, up-to-date documentation following Diátaxis framework
- **Agentic Coding** - Machine-readable instructions, stateful memory for AI agents
## License

MIT License - see [LICENSE](LICENSE)
## Related Projects

- [chora-base](https://github.com/liminalcommons/chora-base) - Python project template
- [chora-composer](https://github.com/liminalcommons/chora-composer) - Configuration-driven artifact generation
- [chora-platform](https://github.com/liminalcommons/chora-platform) - Shared platform tooling

---

🤖 Generated with [chora-base](https://github.com/liminalcommons/chora-base) template
