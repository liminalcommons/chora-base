# Installation Guide

**Audience**: New users setting up chora-base projects
**Time**: 10-15 minutes
**Prerequisites**: Python 3.11+, Git

---

## Quick Start

```bash
# 1. Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git my-project
cd my-project

# 2. Remove chora-base git history
rm -rf .git
git init

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Run tests to verify setup
pytest

# 5. Start customizing
# Edit AGENTS.md, README.md, src/ with your project details
```

---

## Detailed Installation

### Step 1: System Requirements

**Required**:
- Python 3.11, 3.12, or 3.13
- Git 2.x+
- pip or poetry

**Optional**:
- Docker (for containerized development)
- GitHub CLI (`gh`) for workflow management

**Check versions**:
```bash
python --version  # Should be 3.11+
git --version     # Should be 2.x+
pip --version
```

### Step 2: Clone Repository

```bash
# Clone to new directory
git clone https://github.com/liminalcommons/chora-base.git my-project
cd my-project

# Or clone and rename
git clone https://github.com/liminalcommons/chora-base.git
mv chora-base my-project
cd my-project
```

### Step 3: Initialize as New Project

```bash
# Remove chora-base git history
rm -rf .git

# Initialize new git repo
git init
git add .
git commit -m "Initial commit from chora-base v3.8.0"
```

### Step 4: Install Dependencies

**Using pip**:
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

**Using poetry**:
```bash
# Convert from pyproject.toml
poetry install --with dev
```

**Verify installation**:
```bash
# Check installed packages
pip list | grep pytest
pip list | grep ruff

# Should see:
# pytest            7.x.x
# pytest-cov        4.x.x
# ruff              0.x.x
# mypy              1.x.x
```

### Step 5: Run Initial Tests

```bash
# Run tests (should all pass out of the box)
pytest

# Run with coverage
pytest --cov=src --cov-report=term

# Run linting
ruff check .
mypy src
```

**Expected output**:
```
============================= test session starts ==============================
collected 0 items

======================== no tests ran in 0.01s =================================
```
(No tests initially - you'll add them for your project)

---

## Project Customization

### Customize Project Metadata

**Edit `pyproject.toml`**:
```toml
[project]
name = "my-project"  # Change from "chora-base"
version = "0.1.0"    # Your initial version
description = "My awesome project description"
authors = [{name = "Your Name", email = "your@email.com"}]
```

### Customize Documentation

**Edit `AGENTS.md`**:
```markdown
## Project Overview

**Project Name**: My Project
**Purpose**: [Describe your project]
**Current Version**: 0.1.0
```

**Edit `README.md`**:
- Update project name
- Update description
- Update features list
- Update installation instructions for your project

### Remove Unnecessary SAPs

```bash
# List SAPs
ls docs/skilled-awareness/

# Remove SAPs you don't need
rm -rf docs/skilled-awareness/docker-operations  # If not using Docker
rm -rf docs/skilled-awareness/mcp-server-development  # If not building MCP servers

# Update INDEX.md
vim docs/skilled-awareness/INDEX.md  # Remove deleted SAPs from table
```

---

## Development Environment Setup

### IDE Configuration

**VS Code** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests",
    "--cov=src",
    "--cov-report=term"
  ]
}
```

**PyCharm**:
1. Settings → Project → Python Interpreter → Add interpreter → Existing environment
2. Select `.venv/bin/python`
3. Settings → Tools → Python Integrated Tools → Default test runner → pytest

### Git Hooks (Optional)

**Pre-commit hooks** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
ruff check . || exit 1
mypy src || exit 1
pytest --cov=src --cov-fail-under=85 || exit 1
```

```bash
chmod +x .git/hooks/pre-commit
```

---

## Troubleshooting

### "No module named 'src'"

**Solution**: Install in editable mode
```bash
pip install -e .
```

### Python Version Mismatch

**Solution**: Use pyenv
```bash
pyenv install 3.11.5
pyenv local 3.11.5
pip install -e ".[dev]"
```

### Permission Errors

**Solution**: Use virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

---

## Next Steps

- [Quickstart Guide](quickstart.md) - Build your first feature
- [GitHub Actions Guide](github-actions.md) - Set up CI/CD
- [SAP-003: Project Bootstrap](../../skilled-awareness/project-bootstrap/) - Project structure guide

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
