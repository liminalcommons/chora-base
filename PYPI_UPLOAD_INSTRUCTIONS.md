# PyPI Upload Instructions

The package has been successfully built and is ready for upload to PyPI.

## Built Packages

Located in `dist/`:
- `mcp_orchestration-0.1.0-py3-none-any.whl` (25K)
- `mcp_orchestration-0.1.0.tar.gz` (222K)

Both packages have been verified with `twine check` and **PASSED** validation.

## Upload to PyPI

### Option 1: Using API Token (Recommended)

1. Get your PyPI API token from https://pypi.org/manage/account/token/

2. Upload using the token:
```bash
python3 -m twine upload dist/* --username __token__ --password pypi-YOUR_API_TOKEN_HERE
```

### Option 2: Using Environment Variable

1. Set your PyPI token as an environment variable:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
```

2. Upload:
```bash
python3 -m twine upload dist/*
```

### Option 3: Using .pypirc

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
```

Then upload:
```bash
python3 -m twine upload dist/*
```

## Test Installation After Upload

Once uploaded, test the installation:

```bash
# In a fresh virtual environment
python3 -m venv test-env
source test-env/bin/activate
pip install mcp-orchestration

# Verify installation
mcp-orchestration-init --help
python3 -c "import mcp_orchestrator; print(mcp_orchestrator.__version__)"
```

## GitHub Release

A git tag `v0.1.0` has been pushed to GitHub. You can create a GitHub release at:
https://github.com/liminalcommons/mcp-orchestration/releases/new?tag=v0.1.0

Suggested release notes template:

```markdown
# Wave 1 Release: MCP Orchestration v0.1.0

## Overview

First public release of mcp-orchestration, providing centralized configuration management for MCP clients with cryptographic signatures and content-addressable storage.

## Features

- **Cryptographic Signatures** - Ed25519 signatures for configuration integrity
- **Content-Addressable Storage** - SHA-256 based artifact identification
- **Multi-Client Registry** - Support for Claude Desktop and Cursor
- **Configuration Diff** - Intelligent comparison with field-level change detection
- **MCP Server** - 4 tools (list_clients, list_profiles, get_config, diff_config) and 2 resources
- **CLI Initialization** - Quick-start command to generate signed configurations
- **Comprehensive Testing** - 67 passing tests with full integration coverage

## Installation

```bash
pip install mcp-orchestration
```

## Quick Start

1. Initialize configuration storage:
```bash
mcp-orchestration-init
```

2. Configure your MCP client (Claude Desktop or Cursor) - see README for details

3. Use the orchestration tools within your client

## Documentation

- [README](https://github.com/liminalcommons/mcp-orchestration#readme)
- [Wave 1 Specification](https://github.com/liminalcommons/mcp-orchestration/blob/main/docs/e2e-tests/wave-1/00-server-spec.md)

## What's Next

See [ROADMAP.md](https://github.com/liminalcommons/mcp-orchestration/blob/main/ROADMAP.md) for planned Wave 2 features.
```

## Package Metadata

- **Name**: mcp-orchestration
- **Version**: 0.1.0
- **Description**: MCP server for centralized configuration management with cryptographic signatures and content-addressable storage
- **Author**: Victor Piper <victor@liminalcommons.org>
- **License**: MIT
- **Python**: >=3.12
- **Homepage**: https://github.com/liminalcommons/mcp-orchestration

## Git Status

All changes have been committed and pushed to GitHub:
- Branch: `adopt-chora-base`
- Tag: `v0.1.0`
- Repository: https://github.com/liminalcommons/chora-base
- Latest commit: Fix project.urls placement in pyproject.toml

Note: The repository name appears to be `chora-base` but the package name is `mcp-orchestration`. You may want to verify this is correct or consider creating a dedicated repository for the mcp-orchestration package.
