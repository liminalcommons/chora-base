# Example MCP Server with Vision



## Overview

**Example MCP Server with Vision** is a Model Context Protocol (MCP) server that provides [describe your server's capabilities].

This project follows the MCP specification and can be integrated with:
- Claude Desktop
- Cursor
- Other MCP-compatible clients

## Features

- **[Feature 1]** - Description
- **[Feature 2]** - Description
- **Agent Memory System** - Cross-session learning with event log, knowledge graph, and trace correlation
## Installation

### Quick Setup

```bash
# Clone repository
git clone https://github.com//example-mcp-vision.git
cd example-mcp-vision

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

```

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Application configuration
_LOG_LEVEL=INFO

# Add your configuration here
```

### Client Configuration

#### Claude Desktop (macOS)

**Development Mode (Editable Install):**
```json
{
  "mcpServers": {
    "example-mcp-vision-dev": {
      "command": "/path/to/example-mcp-vision/.venv/bin/python",
      "args": ["-m", ".server"],
      "cwd": "/path/to/example-mcp-vision",
      "env": {
        "_DEBUG": "1"
      }
    }
  }
}
```

**Production Mode (Installed Package):**
```json
{
  "mcpServers": {
    "example-mcp-vision": {
      "command": "example-mcp-vision",
      "args": [],
      "env": {}
    }
  }
}
```
## Development

### Common Development Tasks

```bash
# Build distribution packages
./scripts/build-dist.sh

# Run smoke tests (quick validation)
./scripts/smoke-test.sh

# Run pre-merge checks (lint + test + coverage)
./scripts/pre-merge.sh

# Clean build artifacts
rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/

# Run application
example-mcp-vision
```

## Documentation

**For Human Contributors:**
- **[README.md](README.md)** - This file (project overview)
**For AI Coding Agents:**
- **[AGENTS.md](AGENTS.md)** - Machine-readable project instructions (OpenAI/Google/Sourcegraph standard)

## Project Principles

This project follows best practices for:

- **Code Quality** - Linting (ruff), formatting (black), type checking (mypy)
- **Documentation** - Clear, up-to-date documentation following Diátaxis framework
- **Agentic Coding** - Machine-readable instructions, stateful memory for AI agents
## License



## Related Projects

- [chora-base](https://github.com/liminalcommons/chora-base) - Python project template
- [chora-composer](https://github.com/liminalcommons/chora-composer) - Configuration-driven artifact generation
- [chora-platform](https://github.com/liminalcommons/chora-platform) - Shared platform tooling

---

🤖 Generated with [chora-base](https://github.com/liminalcommons/chora-base) template
