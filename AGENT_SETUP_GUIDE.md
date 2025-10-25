# Chora-Base v3.0 Setup Guide for AI Agents

**Version:** 3.0.0
**Last Updated:** 2025-10-25
**Target Audience:** AI coding agents (Claude Code, Cursor, Aider, etc.)
**Compatibility:** Python 3.11+, MCP Protocol

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Architecture Overview](#2-architecture-overview)
3. [Variable Reference](#3-variable-reference)
4. [Setup Procedure](#4-setup-procedure)
5. [Feature Flags](#5-feature-flags)
6. [Validation Checklist](#6-validation-checklist)
7. [Troubleshooting](#7-troubleshooting)
8. [Advanced Customization](#8-advanced-customization)
9. [Complete Examples](#9-complete-examples)

---

## 1. Quick Start

### 1.1 One-Command Setup

When a user requests chora-base setup, execute this autonomous workflow:

```
INPUT: "Set up chora-base for mcp-github project"

PROCESS:
1. Gather requirements (project name, author info)
2. Copy static-template/ → project root
3. Rename src/__package_name__/ → src/{package_name}/
4. Process 10 blueprint files (variable substitution)
5. Initialize git repository
6. Validate setup

OUTPUT: Fully functional MCP server project
```

### 1.2 Expected Timeline

- **Simple setup** (defaults): 30-60 seconds
- **Custom features**: 2-3 minutes
- **Full validation**: Additional 30 seconds

### 1.3 Prerequisites

**User's Environment:**
- Git installed
- Python 3.11+ available
- Empty git repository OR new directory

**Agent Capabilities Required:**
- File system operations (read, write, copy, move)
- String substitution / template processing
- Git operations (init, add, commit)

### 1.4 Success Criteria

After setup completes, the project MUST have:

✅ Valid `pyproject.toml` with correct package name
✅ `src/{package_name}/mcp/server.py` with FastMCP server
✅ All static files copied correctly
✅ Tests passing: `pytest tests/`
✅ Linting passing: `ruff check src/`
✅ Git repository initialized with initial commit

---

## 2. Architecture Overview

### 2.1 What is Chora-Base?

Chora-base is a production-ready Python project template designed for:
- **MCP Servers** (Model Context Protocol)
- **Python Libraries**
- **CLI Tools**
- **Web Services**

**Core Philosophy:**
- AI-agent-first design
- Zero external dependencies for setup
- All features enabled by default
- Static files whenever possible (70% of template)

### 2.2 Repository Structure

```
chora-base/
├── AGENT_SETUP_GUIDE.md          ← You are here!
├── static-template/               ← 70+ static files
│   ├── .editorconfig
│   ├── .github/workflows/        ← CI/CD configs
│   ├── src/__package_name__/     ← Placeholder directory
│   │   ├── memory/               ← Agent memory system (event log, knowledge graph)
│   │   ├── utils/                ← Python utilities (validation, responses, errors, persistence)
│   │   └── mcp/                  ← MCP server code (from blueprint)
│   ├── tests/                    ← Full test suite
│   ├── scripts/                  ← Development scripts
│   ├── user-docs/                ← Documentation
│   └── [60+ more files]
│
├── blueprints/                   ← 10 files needing variable substitution
│   ├── pyproject.toml.blueprint
│   ├── README.md.blueprint
│   ├── AGENTS.md.blueprint
│   ├── server.py.blueprint
│   └── [6 more files]
│
├── setup.py                      ← Optional CLI helper
└── examples/                     ← Reference implementations
```

### 2.3 Why This Architecture?

**Problem with Previous Approach (Copier):**
- Required external dependencies (copier, Jinja2, questionary)
- Interactive prompts failed in AI agent contexts
- `--defaults` flag broken, unreliable generation
- Complex conditional logic in 60+ .jinja files
- Opaque errors, difficult debugging

**Benefits of AI-Agent-First Approach:**
- ✅ Zero dependencies (pure file operations)
- ✅ Agents control the entire process
- ✅ Transparent (all steps visible)
- ✅ Deterministic (works every time)
- ✅ Fast (no compilation, no CLI prompts)
- ✅ Maintainable (70% static files, 10 simple blueprints)

### 2.4 Feature Coverage

**All features from v2.1.0 preserved:**
- Agent Memory System (.chora/memory/)
- Python Utilities (validation, responses, errors, persistence)
- MCP Server scaffolding (FastMCP-based)
- GitHub Actions CI/CD
- Pre-commit hooks (ruff, mypy, pytest)
- Docker support (production + CI)
- Comprehensive documentation (Diátaxis framework)
- Vision-driven development support
- MCP namespace conventions
- Test suite with 95%+ coverage goals

---

## 3. Variable Reference

### 3.1 Core Variables (Required)

All blueprints use these variables. Gather from user or derive automatically.

#### `{{project_name}}`
- **Type:** String
- **Example:** `"MCP GitHub"`, `"Slack Integration Server"`
- **Usage:** Human-readable project name
- **Appears in:** README.md, AGENTS.md, CHANGELOG.md
- **Validation:** Non-empty, max 100 characters

#### `{{project_slug}}`
- **Type:** String (kebab-case)
- **Example:** `"mcp-github"`, `"slack-integration-server"`
- **Derivation:** `project_name.lower().replace(" ", "-").replace("_", "-")`
- **Usage:** GitHub repo name, package name on PyPI
- **Appears in:** pyproject.toml, README clone URLs
- **Validation:** Regex `^[a-z][a-z0-9-]+$` (lowercase, hyphens only)

#### `{{package_name}}`
- **Type:** String (snake_case)
- **Example:** `"mcp_github"`, `"slack_integration_server"`
- **Derivation:** `project_slug.replace("-", "_")`
- **Usage:** Python package name, imports, directory names
- **Appears in:** pyproject.toml, imports, src/ directory rename
- **Validation:** Regex `^[a-z][a-z0-9_]+$` (valid Python identifier)

#### `{{author_name}}`
- **Type:** String
- **Example:** `"John Doe"`, `"Acme Corp"`
- **Source:** User input OR `git config user.name`
- **Usage:** Project metadata, LICENSE, CONTRIBUTING
- **Appears in:** pyproject.toml, README, LICENSE
- **Validation:** Non-empty

#### `{{author_email}}`
- **Type:** String (email)
- **Example:** `"john@example.com"`
- **Source:** User input OR `git config user.email`
- **Usage:** Project metadata, security contact
- **Appears in:** pyproject.toml, SECURITY.md
- **Validation:** Valid email format

#### `{{github_username}}`
- **Type:** String
- **Example:** `"johndoe"`, `"acme-corp"`
- **Source:** User input OR infer from git remote
- **Usage:** GitHub URLs, clone instructions
- **Appears in:** README.md, GitHub Actions
- **Validation:** Valid GitHub username format

#### `{{project_description}}`
- **Type:** String
- **Example:** `"GitHub API integration for Claude Code"`
- **Source:** User input (required)
- **Usage:** README, pyproject.toml description
- **Appears in:** Multiple places
- **Validation:** Non-empty, max 500 characters

### 3.2 Optional Variables (Have Defaults)

#### `{{python_version}}`
- **Default:** `"3.11"`
- **Options:** `"3.11"`, `"3.12"`, `"3.13"`
- **Usage:** pyproject.toml `requires-python` field
- **When to override:** If user has specific Python requirement

#### `{{project_version}}`
- **Default:** `"0.1.0"`
- **Usage:** pyproject.toml version field
- **Validation:** Semantic versioning (X.Y.Z)

#### `{{license}}`
- **Default:** `"MIT"`
- **Options:** `"MIT"`, `"Apache-2.0"`, `"GPL-3.0"`, `"BSD-3-Clause"`
- **Usage:** LICENSE file, pyproject.toml

#### `{{mcp_namespace}}`
- **Default:** `package_name` (without underscores)
- **Example:** For `mcp_github` → `"mcpgithub"`
- **Usage:** MCP tool/resource prefixing (e.g., `mcpgithub:create_issue`)
- **Validation:** Lowercase alphanumeric, 3-20 chars

### 3.3 Variable Derivation Rules

**Automatic Derivation** (agents should compute these):

```python
# Example derivation logic
def derive_variables(project_name: str) -> dict:
    """Derive all variables from project_name."""

    # Basic transformations
    project_slug = project_name.lower().replace(" ", "-").replace("_", "-")
    package_name = project_slug.replace("-", "_")
    mcp_namespace = package_name.replace("_", "")

    # Git config fallbacks
    author_name = git_config("user.name") or "Your Name"
    author_email = git_config("user.email") or "your.email@example.com"

    # GitHub username from remote
    github_username = extract_github_username() or author_name.lower().replace(" ", "")

    return {
        "project_name": project_name,
        "project_slug": project_slug,
        "package_name": package_name,
        "mcp_namespace": mcp_namespace,
        "author_name": author_name,
        "author_email": author_email,
        "github_username": github_username,
        "python_version": "3.11",  # default
        "project_version": "0.1.0",  # default
        "license": "MIT",  # default
    }
```

### 3.4 Variable Validation

Before processing blueprints, validate ALL variables:

**Required Checks:**
- ✅ `project_name` is not empty
- ✅ `project_slug` matches regex `^[a-z][a-z0-9-]+$`
- ✅ `package_name` matches regex `^[a-z][a-z0-9_]+$`
- ✅ `author_email` is valid email format
- ✅ `project_version` is valid semver (X.Y.Z)

**If validation fails:**
- Prompt user for correction
- Do NOT proceed with invalid values
- Explain what's wrong clearly

---

## 4. Setup Procedure

### 4.1 Pre-Setup Checks

Before beginning setup, verify:

```
1. Current directory is empty OR is a git repository
2. User has confirmed project name and description
3. All required variables are gathered
4. Agent has file system write permissions
```

### 4.2 Step 1: Gather Requirements

**Prompt user for essential information:**

```
AGENT: "I'll set up chora-base for your project. I need a few details:

1. Project name? (e.g., 'MCP GitHub', 'Slack Integration')
2. Brief description? (e.g., 'GitHub API integration for Claude')
3. Author name? [defaults to: {git config user.name}]
4. Author email? [defaults to: {git config user.email}]
5. GitHub username? [defaults to: {inferred from git remote}]

I'll use Python 3.11 and enable all features by default."
```

**Derive remaining variables:**

```python
# After gathering user input, compute:
project_slug = derive_slug(project_name)
package_name = derive_package_name(project_slug)
mcp_namespace = derive_namespace(package_name)

# Confirm with user:
print(f"""
Derived values:
- Package name: {package_name}
- Project slug: {project_slug}
- MCP namespace: {mcp_namespace}

Proceed? [yes/no]
""")
```

### 4.3 Step 2: Copy Static Template

**Copy ALL files from `static-template/` to project root:**

```bash
# Pseudo-code for agents
source_dir = "https://github.com/liminalcommons/chora-base/static-template/"
target_dir = "./"  # Current directory

copy_recursive(source_dir, target_dir, preserve_structure=True)
```

**Files being copied** (70+ files, all ready to use):

```
✓ .editorconfig                   # Editor configuration
✓ .github/                         # CI/CD workflows (6 files)
  ├── dependabot.yml
  └── workflows/
      ├── test.yml
      ├── lint.yml
      ├── smoke.yml
      ├── release.yml
      ├── codeql.yml
      └── dependency-review.yml
✓ src/__package_name__/           # Source code
  ├── memory/                      # Agent memory system
  │   ├── __init__.py
  │   ├── event_log.py             # Event logging
  │   ├── knowledge_graph.py       # Knowledge graph
  │   └── trace.py                 # Trace context
  └── utils/                       # Python utilities
      ├── __init__.py
      ├── errors.py                # Error formatting
      ├── persistence.py           # State persistence
      ├── responses.py             # Response builders
      └── validation.py            # Input validation
✓ tests/                           # Test suite
  ├── AGENTS.md                    # Test instructions
  └── utils/                       # Utility tests
      ├── __init__.py
      ├── test_errors.py
      ├── test_persistence.py
      ├── test_responses.py
      └── test_validation.py
✓ scripts/                         # Development scripts
  ├── AGENTS.md
  ├── setup.sh
  ├── dev-server.sh
  ├── smoke-test.sh
  ├── pre-merge.sh
  └── [20+ more scripts]
✓ user-docs/                       # Documentation
  ├── README.md
  ├── explanation/
  │   └── vision-driven-development.md
  ├── how-to/
  │   ├── use-input-validation.md
  │   ├── standardize-responses.md
  │   ├── improve-error-messages.md
  │   └── persist-application-state.md
  └── reference/
      ├── mcp-conventions.md
      ├── mcp-naming-best-practices.md
      └── python-patterns.md
✓ .chora/memory/                   # Agent memory directory
  ├── AGENTS.md
  └── README.md
✓ Dockerfile                       # Production Docker image
✓ docker-compose.yml               # Docker Compose config
✓ .dockerignore                    # Docker ignore patterns
✓ justfile                         # Task runner recipes
✓ NAMESPACES.md                    # MCP naming conventions
✓ .pre-commit-config.yaml          # Pre-commit hooks config
```

**Important:** All these files are 100% static - no variable substitution needed!

### 4.4 Step 3: Rename Placeholder Directories

The static template uses `__package_name__` as a literal placeholder directory name.

**Rename operation:**

```bash
# Before
src/__package_name__/

# After (example: package_name = "mcp_github")
src/mcp_github/
```

**Implementation:**

```python
# Pseudo-code
import os
import shutil

old_path = "src/__package_name__"
new_path = f"src/{package_name}"

# Rename directory
shutil.move(old_path, new_path)

# Verify
assert os.path.exists(new_path)
assert os.path.exists(f"{new_path}/memory/event_log.py")
assert os.path.exists(f"{new_path}/utils/validation.py")
```

**No other renames needed** - all files inside are already correct!

### 4.5 Step 4: Process Blueprints

Now process the 10 blueprint files that need variable substitution.

**Blueprint files to process:**

1. `blueprints/pyproject.toml.blueprint` → `pyproject.toml`
2. `blueprints/README.md.blueprint` → `README.md`
3. `blueprints/AGENTS.md.blueprint` → `AGENTS.md`
4. `blueprints/CHANGELOG.md.blueprint` → `CHANGELOG.md`
5. `blueprints/CONTRIBUTING.md.blueprint` → `CONTRIBUTING.md`
6. `blueprints/ROADMAP.md.blueprint` → `ROADMAP.md`
7. `blueprints/.gitignore.blueprint` → `.gitignore`
8. `blueprints/.env.example.blueprint` → `.env.example`
9. `blueprints/server.py.blueprint` → `src/{package_name}/mcp/server.py`
10. `blueprints/__init__.py.blueprint` → `src/{package_name}/__init__.py`

**Processing algorithm:**

```python
# Pseudo-code for each blueprint
def process_blueprint(blueprint_path: str, output_path: str, variables: dict):
    """
    Read blueprint, replace variables, write output.

    Variables use {{variable_name}} syntax.
    """
    # Read blueprint content
    with open(blueprint_path, 'r') as f:
        content = f.read()

    # Replace all variables
    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"  # {{var_name}}
        content = content.replace(placeholder, var_value)

    # Verify no unreplaced placeholders remain
    if "{{" in content:
        remaining = extract_placeholders(content)
        raise ValueError(f"Unreplaced placeholders: {remaining}")

    # Write output
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"✓ Generated {output_path}")
```

**Example - pyproject.toml.blueprint:**

```toml
# Input: blueprints/pyproject.toml.blueprint
[project]
name = "{{project_slug}}"
version = "{{project_version}}"
description = "{{project_description}}"
authors = [
    {name = "{{author_name}}", email = "{{author_email}}"}
]
requires-python = ">={{python_version}}"

[project.scripts]
{{package_name}} = "{{package_name}}.mcp.server:main"

# After substitution (example: mcp-github)
[project]
name = "mcp-github"
version = "0.1.0"
description = "GitHub API integration for Claude Code"
authors = [
    {name = "John Doe", email = "john@example.com"}
]
requires-python = ">=3.11"

[project.scripts]
mcp_github = "mcp_github.mcp.server:main"
```

### 4.6 Step 5: Initialize Git Repository

**If not already a git repository:**

```bash
git init
git add .
git commit -m "Initial commit from chora-base v3.0

Generated project structure:
- Project: {{project_name}}
- Package: {{package_name}}
- Template: https://github.com/liminalcommons/chora-base
- Version: 3.0.0

All features enabled by default.
"
```

**If already a git repository:**

```bash
git add .
git commit -m "Apply chora-base v3.0 template

Template: https://github.com/liminalcommons/chora-base v3.0.0
Project: {{project_name}}
"
```

### 4.7 Step 6: Validate Setup

Run validation checks to ensure setup succeeded:

**File existence checks:**

```python
# Critical files must exist
required_files = [
    "pyproject.toml",
    "README.md",
    "AGENTS.md",
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/mcp/server.py",
    f"src/{package_name}/memory/event_log.py",
    f"src/{package_name}/utils/validation.py",
    "tests/utils/test_validation.py",
    ".gitignore",
    ".pre-commit-config.yaml",
]

for file in required_files:
    assert os.path.exists(file), f"Missing required file: {file}"
```

**Content validation:**

```python
# Verify no unreplaced placeholders
def check_no_placeholders(filepath: str):
    with open(filepath, 'r') as f:
        content = f.read()

    if "{{" in content:
        raise ValueError(f"{filepath} contains unreplaced placeholders")

# Check key files
check_no_placeholders("pyproject.toml")
check_no_placeholders("README.md")
check_no_placeholders(f"src/{package_name}/mcp/server.py")
```

**Import validation:**

```bash
# Verify package can be imported
python -c "import sys; sys.path.insert(0, 'src'); import {{package_name}}"
```

**Test validation:**

```bash
# Verify tests can run (may have 0 actual tests initially)
pytest tests/ --collect-only
```

**Lint validation:**

```bash
# Verify code passes linting
ruff check src/
```

**If all checks pass:**

```
✅ Setup complete!

Project: {{project_name}}
Package: {{package_name}}
Location: {os.getcwd()}

Next steps:
1. Run tests: pytest
2. Start dev server: ./scripts/dev-server.sh
3. Implement your first MCP tool in src/{package_name}/mcp/server.py

Documentation: user-docs/README.md
```

---

## 5. Feature Flags

### 5.1 Default Configuration

**ALL features are enabled by default.** Users get the complete chora-base experience:

✅ Agent Memory System
✅ Python Utilities (validation, responses, errors, persistence)
✅ MCP Server scaffolding
✅ GitHub Actions CI/CD
✅ Pre-commit hooks
✅ Docker support
✅ Comprehensive documentation
✅ Vision-driven development support
✅ Test suite

**This is the recommended configuration** for most projects.

### 5.2 Disabling Features

If user requests minimal setup, features can be disabled by **deleting files/directories**.

#### Disable Memory System

```bash
# Remove memory system
rm -rf src/{package_name}/memory/
rm -rf .chora/memory/

# Remove memory docs
rm -f user-docs/how-to/*memory*.md
```

**Impact:** ~10% smaller project, lose event logging and knowledge graph

#### Disable Python Utilities

```bash
# Remove utilities
rm -rf src/{package_name}/utils/
rm -rf tests/utils/

# Remove utility docs
rm -f user-docs/how-to/use-input-validation.md
rm -f user-docs/how-to/standardize-responses.md
rm -f user-docs/how-to/improve-error-messages.md
rm -f user-docs/how-to/persist-application-state.md
rm -f user-docs/reference/python-patterns.md

# Update pyproject.toml to remove utility tests
# (manual edit required)
```

**Impact:** ~20% smaller project, lose validation/response helpers

#### Disable Docker

```bash
# Remove Docker files
rm -f Dockerfile
rm -f docker-compose.yml
rm -f .dockerignore

# Remove Docker docs
rm -f user-docs/how-to/03-docker-deployment.md
```

**Impact:** ~5% smaller project, lose containerization

#### Disable Vision Docs

```bash
# Remove vision documentation
rm -rf dev-docs/vision/

# Remove vision guide
rm -f user-docs/explanation/vision-driven-development.md
rm -f user-docs/how-to/06-maintain-vision-documents.md
```

**Impact:** ~10% smaller project, lose strategic planning docs

#### Disable Pre-commit Hooks

```bash
# Remove pre-commit config
rm -f .pre-commit-config.yaml
```

**Impact:** Minimal size change, lose automated code quality checks

#### Disable GitHub Actions

```bash
# Remove all workflows
rm -rf .github/
```

**Impact:** ~5% smaller project, lose CI/CD automation

### 5.3 When to Disable Features

**Disable features when:**
- User explicitly requests minimal setup
- Project is a library (may not need MCP server scaffolding)
- User has custom CI/CD (don't need GitHub Actions)
- Prototyping / learning (want simpler structure)

**Keep all features when:**
- Building production MCP server (recommended)
- Want battle-tested best practices
- Team collaboration (need CI/CD, docs, etc.)
- Long-term maintained project

**Default recommendation:** Keep all features enabled unless user has specific reason to disable.

---

## 6. Validation Checklist

### 6.1 Post-Setup Validation

After completing setup, run through this checklist:

#### File Structure

```
✓ pyproject.toml exists and contains correct package_name
✓ README.md exists and contains correct project_name
✓ AGENTS.md exists (instructions for future AI agents)
✓ src/{package_name}/ directory exists
✓ src/{package_name}/__init__.py exists
✓ src/{package_name}/mcp/ directory exists
✓ src/{package_name}/mcp/server.py exists
✓ src/{package_name}/memory/ directory exists (3 files)
✓ src/{package_name}/utils/ directory exists (5 files)
✓ tests/ directory exists with test files
✓ .gitignore exists
✓ .pre-commit-config.yaml exists
✓ .github/workflows/ exists (6 workflow files)
```

#### Content Validation

```
✓ No {{placeholder}} variables remain in any file
✓ Package name is valid Python identifier (src/{package_name}/)
✓ All imports use correct package name
✓ pyproject.toml [project.scripts] uses correct package name
✓ README.md has correct clone URL (github_username)
```

#### Functional Validation

```
✓ Python can import the package: python -c "import {package_name}"
✓ Tests can be collected: pytest --collect-only
✓ Linting passes: ruff check src/
✓ Type checking passes: mypy src/ (if mypy installed)
✓ Git repository initialized
✓ Initial commit created
```

### 6.2 Common Validation Failures

**Problem:** Import fails with `ModuleNotFoundError`
- **Cause:** `src/{package_name}/__init__.py` missing
- **Fix:** Ensure file exists (should be auto-created from blueprint)

**Problem:** Pytest can't find tests
- **Cause:** `tests/` directory not copied
- **Fix:** Re-copy static-template/tests/

**Problem:** Ruff reports errors
- **Cause:** Usually unreplaced {{placeholders}} in Python files
- **Fix:** Search for "{{" in src/ directory, replace manually

**Problem:** Git commit fails
- **Cause:** Git not configured (user.name, user.email)
- **Fix:** Run `git config --global user.name "..."` and `git config --global user.email "..."`

### 6.3 Validation Script

Agents can run this validation script after setup:

```python
#!/usr/bin/env python3
"""
Validate chora-base setup.
Run after completing setup procedure.
"""
import os
import sys
import subprocess
from pathlib import Path

def validate_setup(package_name: str) -> bool:
    """Validate chora-base project setup."""
    errors = []

    # Check critical files
    required_files = [
        "pyproject.toml",
        "README.md",
        "AGENTS.md",
        f"src/{package_name}/__init__.py",
        f"src/{package_name}/mcp/server.py",
        ".gitignore",
    ]

    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Missing: {file}")

    # Check for unreplaced placeholders
    for file in required_files:
        if Path(file).exists():
            content = Path(file).read_text()
            if "{{" in content:
                errors.append(f"Unreplaced placeholder in: {file}")

    # Check package import
    try:
        subprocess.run(
            [sys.executable, "-c", f"import sys; sys.path.insert(0, 'src'); import {package_name}"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        errors.append(f"Cannot import package: {package_name}")

    # Check pytest
    try:
        subprocess.run(
            ["pytest", "--collect-only"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        errors.append("Pytest collection failed")

    # Report results
    if errors:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Validation passed!")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_setup.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]
    success = validate_setup(package_name)
    sys.exit(0 if success else 1)
```

---

## 7. Troubleshooting

### 7.1 Common Setup Issues

#### Issue: "Directory not empty" error

**Symptom:** Cannot copy static-template/ because directory has existing files

**Diagnosis:**
```bash
ls -la  # Check what files exist
```

**Solutions:**
1. **If empty git repo:** Safe to proceed, files will merge
2. **If has unrelated files:** Ask user if okay to proceed
3. **If has conflicting files:** Ask user to back up and clean directory

**Prevention:** Check directory state before starting setup

---

#### Issue: Package name contains hyphens

**Symptom:** Python import fails with `SyntaxError`

**Diagnosis:**
```bash
# Bad: package name has hyphens
src/mcp-github/  # ❌ Python can't import "mcp-github"

# Good: package name has underscores
src/mcp_github/  # ✅ Python can import "mcp_github"
```

**Solutions:**
1. Ensure `package_name = project_slug.replace("-", "_")`
2. Never use hyphens in package names

**Prevention:** Follow variable derivation rules in Section 3.3

---

#### Issue: Unreplaced placeholders in generated files

**Symptom:** Files contain `{{variable_name}}` after setup

**Diagnosis:**
```bash
# Search for unreplaced placeholders
grep -r "{{" src/ README.md pyproject.toml
```

**Solutions:**
1. Check that all variables were provided
2. Check variable names match exactly (case-sensitive)
3. Re-process affected blueprint files

**Prevention:** Run validation checks (Section 6) after setup

---

#### Issue: Import fails with "No module named 'package_name'"

**Symptom:** `python -c "import package_name"` fails

**Diagnosis:**
```bash
# Check __init__.py exists
ls -la src/{package_name}/__init__.py

# Check Python path
python -c "import sys; print(sys.path)"
```

**Solutions:**
1. Ensure `src/{package_name}/__init__.py` exists
2. Install package: `pip install -e .`
3. Or add to PYTHONPATH: `export PYTHONPATH="${PWD}/src:${PYTHONPATH}"`

**Prevention:** Follow Step 4.4 (rename directories) carefully

---

#### Issue: Git commit fails with "Please tell me who you are"

**Symptom:** Git operations fail with identity error

**Diagnosis:**
```bash
git config user.name
git config user.email
```

**Solutions:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Prevention:** Check git config before attempting commits

---

### 7.2 Advanced Troubleshooting

#### Issue: Tests fail after setup

**Diagnosis:**
```bash
pytest tests/ -v  # Verbose output
```

**Common causes:**
1. Missing dependencies (run `pip install -e ".[dev]"`)
2. Incorrect package name in imports
3. Missing __init__.py files

**Solutions:**
1. Install all dependencies
2. Verify all imports use correct package_name
3. Check all directories have __init__.py

---

#### Issue: Ruff linting fails

**Diagnosis:**
```bash
ruff check src/ --show-source
```

**Common causes:**
1. Unreplaced placeholders (syntax errors)
2. Missing imports
3. Code style issues

**Solutions:**
1. Search and fix any {{placeholders}}
2. Add missing imports
3. Run `ruff format src/` to auto-fix style

---

### 7.3 Getting Help

If issues persist:

1. **Check setup.py logs** (if using CLI helper)
2. **Review AGENT_SETUP_GUIDE.md** (this file)
3. **Check examples/** directory for reference
4. **File GitHub issue** at https://github.com/liminalcommons/chora-base/issues

Include:
- Project name, package name used
- Steps taken
- Error messages (full output)
- Files generated (ls -R output)

---

## 8. Advanced Customization

### 8.1 Custom Project Types

While chora-base defaults to MCP servers, it supports other project types:

#### Library Project

**Changes from default:**
1. Remove `src/{package_name}/mcp/` directory
2. Update `pyproject.toml` to remove MCP dependencies
3. Update README.md to remove MCP usage instructions

**When to use:** Creating reusable Python library (not MCP-specific)

#### CLI Tool

**Changes from default:**
1. Keep or remove `src/{package_name}/mcp/` (based on need)
2. Add CLI entry point in pyproject.toml
3. Update README with CLI usage examples

**When to use:** Building command-line tool

#### Web Service

**Changes from default:**
1. Remove `src/{package_name}/mcp/` directory
2. Add web framework dependencies (FastAPI, Flask, etc.)
3. Update Dockerfile for web service deployment

**When to use:** Building REST API or web application

### 8.2 Custom Dependencies

**Adding dependencies:**

Edit `pyproject.toml`:

```toml
[project]
dependencies = [
    "fastmcp>=0.3.0",
    "pydantic>=2.0.0",
    # Add your dependencies here
    "requests>=2.31.0",
    "asyncpg>=0.29.0",
]
```

**Development dependencies:**

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    # Add dev dependencies here
    "ipython>=8.0.0",
]
```

### 8.3 Custom GitHub Workflows

The default GitHub Actions workflows cover:
- Testing (test.yml)
- Linting (lint.yml)
- Smoke tests (smoke.yml)
- Releases (release.yml)
- Security (codeql.yml, dependency-review.yml)

**To customize:**

1. Edit files in `.github/workflows/`
2. Add new workflow files as needed
3. Update AGENTS.md to document workflow changes

**Common customizations:**
- Add deployment workflow
- Add documentation build workflow
- Add performance testing workflow
- Add E2E testing workflow

### 8.4 Custom Documentation Structure

The default uses Diátaxis framework:
- `user-docs/explanation/` - Understanding-oriented
- `user-docs/how-to/` - Task-oriented
- `user-docs/reference/` - Information-oriented
- `user-docs/tutorials/` - Learning-oriented (optional)

**To customize:**

1. Add/remove sections as needed
2. Update `user-docs/README.md` navigation
3. Update AGENTS.md to reference new docs

### 8.5 Custom Memory System

The default memory system provides:
- Event logging (`event_log.py`)
- Knowledge graphs (`knowledge_graph.py`)
- Trace context (`trace.py`)

**To extend:**

1. Add new files to `src/{package_name}/memory/`
2. Follow existing patterns (Pydantic models, async APIs)
3. Add tests in `tests/memory/`
4. Document in AGENTS.md

**Example custom memory type:**

```python
# src/{package_name}/memory/user_preferences.py
"""User preference persistence for long-term memory."""
from typing import Dict, Any
from pydantic import BaseModel

class UserPreferences(BaseModel):
    """Track user preferences across sessions."""
    user_id: str
    preferences: Dict[str, Any]

    def save(self):
        """Persist to .chora/memory/preferences/"""
        # Implementation here
```

---

## 9. Complete Examples

### 9.1 Example 1: MCP Server for GitHub

**User request:**
> "Set up chora-base for an MCP server that integrates with GitHub"

**Agent conversation:**

```
AGENT: I'll set up chora-base for your GitHub integration MCP server. Let me gather some details:

1. Project name: MCP GitHub
2. Description: GitHub API integration for Claude Code
3. Author: [reads from git config] John Doe
4. Email: john@example.com
5. GitHub username: johndoe

I'll derive:
- Package name: mcp_github
- Project slug: mcp-github
- MCP namespace: mcpgithub

Proceeding with setup...

[Step 1] ✓ Copied static-template/ (72 files)
[Step 2] ✓ Renamed src/__package_name__/ → src/mcp_github/
[Step 3] ✓ Processed 10 blueprints:
  - pyproject.toml
  - README.md
  - AGENTS.md
  - CHANGELOG.md
  - CONTRIBUTING.md
  - ROADMAP.md
  - .gitignore
  - .env.example
  - src/mcp_github/mcp/server.py
  - src/mcp_github/__init__.py
[Step 4] ✓ Initialized git repository
[Step 5] ✓ Created initial commit
[Step 6] ✓ Validation passed (all checks green)

Setup complete! Your MCP GitHub server is ready.

Next steps:
1. Implement your first GitHub tool in src/mcp_github/mcp/server.py
2. Run dev server: ./scripts/dev-server.sh
3. Run tests: pytest

Documentation: user-docs/README.md
```

**Generated file structure:**

```
mcp-github/
├── pyproject.toml                 # name = "mcp-github"
├── README.md                      # # MCP GitHub
├── AGENTS.md                      # Project: MCP GitHub
├── src/
│   └── mcp_github/               # Python package
│       ├── __init__.py
│       ├── mcp/
│       │   ├── __init__.py
│       │   └── server.py         # FastMCP server entry point
│       ├── memory/               # Event log, knowledge graph
│       └── utils/                # Validation, responses, errors
├── tests/
│   └── utils/                    # Utility tests
├── .github/workflows/            # CI/CD pipelines
├── user-docs/                    # Documentation
└── [70+ more files]
```

**Key customizations made:**
- Project name: "MCP GitHub" → All markdown files
- Package name: "mcp_github" → Directory names, imports, pyproject.toml
- GitHub username: "johndoe" → README clone URLs
- MCP namespace: "mcpgithub" → Tool/resource prefixes

**Time elapsed:** ~45 seconds

---

### 9.2 Example 2: Minimal Library

**User request:**
> "Set up chora-base for a Python library, I don't need MCP or Docker"

**Agent conversation:**

```
AGENT: I'll set up chora-base for your Python library with minimal features.

Project details:
1. Project name: String Utils Pro
2. Description: Advanced string manipulation utilities
3. Author: Jane Smith
4. Email: jane@example.com

Derived:
- Package name: string_utils_pro
- Project slug: string-utils-pro

I'll enable:
✓ Core Python utilities
✓ Testing infrastructure
✓ GitHub Actions CI/CD
✓ Documentation

I'll disable:
✗ MCP server scaffolding (not needed for library)
✗ Docker (not needed for library)
✗ Memory system (not needed for library)

Proceeding...

[Setup steps...]

✓ Setup complete

Post-setup cleanup:
- Removed src/string_utils_pro/mcp/ (not needed)
- Removed src/string_utils_pro/memory/ (not needed)
- Removed Dockerfile, docker-compose.yml (not needed)
- Updated README.md for library usage

Your library is ready!

Next steps:
1. Implement functions in src/string_utils_pro/
2. Add tests in tests/
3. Update README with API documentation
```

**Generated structure** (simplified):

```
string-utils-pro/
├── pyproject.toml
├── README.md
├── src/
│   └── string_utils_pro/
│       ├── __init__.py
│       └── utils/                # Utility functions only
├── tests/
├── .github/workflows/
└── user-docs/
```

**Time elapsed:** ~60 seconds (includes feature removal)

---

### 9.3 Example 3: Full-Featured Production Server

**User request:**
> "Set up chora-base for a production MCP server with all features enabled"

**Agent conversation:**

```
AGENT: I'll set up chora-base with ALL features enabled (recommended for production).

Project details:
1. Project name: Slack Integration Server
2. Description: Enterprise-grade Slack integration for Claude
3. Author: Acme Corp Engineering
4. Email: eng@acme.com
5. GitHub username: acme-corp

Derived:
- Package name: slack_integration_server
- Project slug: slack-integration-server
- MCP namespace: slackintegrationserver

All features enabled:
✓ MCP Server scaffolding (FastMCP)
✓ Agent Memory System (event log, knowledge graph, trace)
✓ Python Utilities (validation, responses, errors, persistence)
✓ Docker support (production + CI)
✓ GitHub Actions (6 workflows)
✓ Pre-commit hooks (ruff, mypy, pytest)
✓ Vision-driven development docs
✓ Comprehensive test suite
✓ Full documentation (Diátaxis framework)

Proceeding with full setup...

[Setup steps...]

✓ Setup complete (82 files generated)

Validation:
✓ All imports working
✓ Tests passing (12 utility tests)
✓ Linting passing (ruff)
✓ Docker builds successfully
✓ Git repository initialized

Production checklist:
✓ CI/CD configured (.github/workflows/)
✓ Security scanning enabled (CodeQL, Dependabot)
✓ Documentation complete (user-docs/)
✓ Pre-commit hooks ready (.pre-commit-config.yaml)
✓ Docker deployment ready (Dockerfile, docker-compose.yml)

Your production MCP server is ready!

Next steps:
1. Review AGENTS.md for project-specific AI agent instructions
2. Implement Slack tools in src/slack_integration_server/mcp/server.py
3. Run pre-merge checks: ./scripts/pre-merge.sh
4. Deploy with Docker: docker-compose up

Documentation: user-docs/README.md
Vision docs: dev-docs/vision/README.md
```

**Generated structure** (full):

```
slack-integration-server/
├── pyproject.toml
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── .gitignore
├── .env.example
├── .editorconfig
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── justfile
├── NAMESPACES.md
├── src/
│   └── slack_integration_server/
│       ├── __init__.py
│       ├── mcp/
│       │   ├── __init__.py
│       │   └── server.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── event_log.py
│       │   ├── knowledge_graph.py
│       │   └── trace.py
│       └── utils/
│           ├── __init__.py
│           ├── errors.py
│           ├── persistence.py
│           ├── responses.py
│           └── validation.py
├── tests/
│   ├── AGENTS.md
│   └── utils/
│       ├── __init__.py
│       ├── test_errors.py
│       ├── test_persistence.py
│       ├── test_responses.py
│       └── test_validation.py
├── scripts/
│   ├── AGENTS.md
│   ├── setup.sh
│   ├── dev-server.sh
│   ├── smoke-test.sh
│   ├── pre-merge.sh
│   ├── build-dist.sh
│   ├── publish-prod.sh
│   └── [15+ more scripts]
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── test.yml
│       ├── lint.yml
│       ├── smoke.yml
│       ├── release.yml
│       ├── codeql.yml
│       └── dependency-review.yml
├── .chora/
│   └── memory/
│       ├── AGENTS.md
│       └── README.md
├── user-docs/
│   ├── README.md
│   ├── explanation/
│   │   └── vision-driven-development.md
│   ├── how-to/
│   │   ├── use-input-validation.md
│   │   ├── standardize-responses.md
│   │   ├── improve-error-messages.md
│   │   ├── persist-application-state.md
│   │   ├── 01-generate-new-mcp-server.md
│   │   ├── 02-rip-and-replace-existing-server.md
│   │   ├── 03-docker-deployment.md
│   │   └── 06-maintain-vision-documents.md
│   └── reference/
│       ├── mcp-conventions.md
│       ├── mcp-naming-best-practices.md
│       ├── python-patterns.md
│       └── template-configuration.md
└── dev-docs/
    ├── README.md
    ├── CONTRIBUTING.md
    └── vision/
        ├── README.md
        └── CAPABILITY_EVOLUTION.example.md
```

**Time elapsed:** ~90 seconds (larger project, more files)

---

## 10. Appendix

### 10.1 Blueprint File Reference

Complete list of blueprint files and their purposes:

| Blueprint File | Output Location | Purpose | Variables Used |
|----------------|-----------------|---------|----------------|
| `pyproject.toml.blueprint` | `pyproject.toml` | Python project metadata | project_slug, project_version, project_description, author_name, author_email, python_version, package_name |
| `README.md.blueprint` | `README.md` | Project overview, installation, usage | project_name, project_description, project_slug, package_name, github_username |
| `AGENTS.md.blueprint` | `AGENTS.md` | AI agent instructions | project_name, package_name, project_description |
| `CHANGELOG.md.blueprint` | `CHANGELOG.md` | Version history | project_version |
| `CONTRIBUTING.md.blueprint` | `CONTRIBUTING.md` | Contribution guidelines | project_name, github_username |
| `ROADMAP.md.blueprint` | `ROADMAP.md` | Development roadmap | project_name, project_version |
| `.gitignore.blueprint` | `.gitignore` | Git ignore patterns | package_name |
| `.env.example.blueprint` | `.env.example` | Environment variables | package_name |
| `server.py.blueprint` | `src/{package_name}/mcp/server.py` | MCP server entry point | package_name, mcp_namespace |
| `__init__.py.blueprint` | `src/{package_name}/__init__.py` | Package initialization | project_version |

### 10.2 Static File Inventory

Complete list of static files (no variable substitution needed):

**Configuration Files (8):**
- `.editorconfig` - Editor configuration
- `.pre-commit-config.yaml` - Pre-commit hooks config
- `justfile` - Task runner recipes
- `.dockerignore` - Docker ignore patterns
- `Dockerfile` - Production Docker image
- `docker-compose.yml` - Docker Compose config
- `NAMESPACES.md` - MCP naming conventions
- `.github/dependabot.yml` - Dependabot configuration

**GitHub Workflows (6):**
- `.github/workflows/test.yml` - Test suite execution
- `.github/workflows/lint.yml` - Code linting
- `.github/workflows/smoke.yml` - Smoke testing
- `.github/workflows/release.yml` - Release automation
- `.github/workflows/codeql.yml` - Security scanning
- `.github/workflows/dependency-review.yml` - Dependency security

**Source Code (9 Python files):**
- `src/__package_name__/memory/event_log.py` - Event logging
- `src/__package_name__/memory/knowledge_graph.py` - Knowledge graph
- `src/__package_name__/memory/trace.py` - Trace context
- `src/__package_name__/memory/__init__.py` - Memory package init
- `src/__package_name__/utils/validation.py` - Input validation
- `src/__package_name__/utils/responses.py` - Response builders
- `src/__package_name__/utils/errors.py` - Error formatting
- `src/__package_name__/utils/persistence.py` - State persistence
- `src/__package_name__/utils/__init__.py` - Utils package init

**Tests (5 files):**
- `tests/AGENTS.md` - Test instructions for agents
- `tests/utils/__init__.py` - Test package init
- `tests/utils/test_validation.py` - Validation tests
- `tests/utils/test_responses.py` - Response tests
- `tests/utils/test_errors.py` - Error tests
- `tests/utils/test_persistence.py` - Persistence tests

**Scripts (25+):**
- `scripts/AGENTS.md` - Script documentation
- `scripts/setup.sh` - Project setup
- `scripts/dev-server.sh` - Development server
- `scripts/smoke-test.sh` - Smoke testing
- `scripts/pre-merge.sh` - Pre-merge checks
- `scripts/build-dist.sh` - Build distribution
- `scripts/publish-prod.sh` - Publish to PyPI
- `scripts/publish-test.sh` - Publish to TestPyPI
- `scripts/bump-version.sh` - Version bumping
- `scripts/check-env.sh` - Environment checks
- `scripts/diagnose.sh` - Diagnostics
- `scripts/handoff.sh` - Session handoff
- `scripts/integration-test.sh` - Integration tests
- `scripts/prepare-release.sh` - Release preparation
- `scripts/rollback-dev.sh` - Development rollback
- `scripts/verify-stable.sh` - Stability checks
- `scripts/venv-create.sh` - Virtual environment creation
- `scripts/venv-clean.sh` - Virtual environment cleanup
- [Additional scripts...]

**Documentation (15+ files):**
- `.chora/memory/README.md` - Memory system docs
- `.chora/memory/AGENTS.md` - Memory agent instructions
- `user-docs/README.md` - Documentation index
- `user-docs/explanation/vision-driven-development.md` - Vision docs explanation
- `user-docs/how-to/use-input-validation.md` - Validation how-to
- `user-docs/how-to/standardize-responses.md` - Response how-to
- `user-docs/how-to/improve-error-messages.md` - Error formatting how-to
- `user-docs/how-to/persist-application-state.md` - Persistence how-to
- `user-docs/how-to/01-generate-new-mcp-server.md` - Generation how-to
- `user-docs/how-to/02-rip-and-replace-existing-server.md` - Migration how-to
- `user-docs/how-to/03-docker-deployment.md` - Docker how-to
- `user-docs/how-to/06-maintain-vision-documents.md` - Vision maintenance
- `user-docs/reference/mcp-conventions.md` - MCP conventions reference
- `user-docs/reference/mcp-naming-best-practices.md` - Naming best practices
- `user-docs/reference/python-patterns.md` - Python patterns reference
- [Additional docs...]

**Total static files:** 70+

### 10.3 Variable Substitution Patterns

Common patterns agents should recognize:

**Simple substitution:**
```
{{project_name}}  → "MCP GitHub"
{{package_name}}  → "mcp_github"
```

**In URLs:**
```
https://github.com/{{github_username}}/{{project_slug}}
→ https://github.com/johndoe/mcp-github
```

**In Python code:**
```python
from {{package_name}}.utils import validation
→ from mcp_github.utils import validation
```

**In TOML:**
```toml
name = "{{project_slug}}"
→ name = "mcp-github"
```

**In bash scripts:**
```bash
#!/usr/bin/env bash
# {{project_name}} - {{project_description}}
→ # MCP GitHub - GitHub API integration for Claude Code
```

### 10.4 Maintenance Notes

**For template maintainers:**

When adding new files to chora-base:

1. **If file is static** (no variables):
   - Add to `static-template/` directory
   - No further processing needed

2. **If file needs variables:**
   - Add to `blueprints/` directory
   - Use `.blueprint` suffix
   - Document in this guide (Section 10.1)

3. **If file is conditional:**
   - Still add to `static-template/`
   - Document deletion instructions in Section 5.2

**Updating this guide:**
- Keep comprehensive (agents read fast)
- Include code examples
- Update examples when adding features
- Maintain table of contents

### 10.5 Version History

**v3.0.0** (2025-10-25)
- Complete rewrite: AI-agent-first architecture
- Removed copier dependency
- 70% static files, 10 simple blueprints
- Comprehensive 2000-line agent guide
- Optional setup.py CLI helper
- All features enabled by default

**v2.1.0** (2025-10-24)
- Added Python utilities (validation, responses, errors, persistence)
- Generalized from mcp-orchestration learnings
- 40-50% code reduction when using patterns

**v2.0.9** (2025-10-23)
- Fixed Jinja2 template delimiter issues
- Wrapped .format() calls in {% raw %} blocks

**v2.0.0** (2025-10-18)
- Switched to standard Jinja2 delimiters
- Major template restructuring

**v1.x** (Earlier)
- Initial copier-based releases
- Custom delimiter experimentation

---

## End of Guide

**Summary:** This guide provides complete instructions for AI agents to autonomously set up chora-base projects. Follow the step-by-step procedure in Section 4, validate using Section 6, and refer to examples in Section 9.

**For Users:** Share this guide with your AI coding agent and say: "Set up chora-base for [your project]"

**For Agents:** Follow Section 4 procedure exactly. Validate every step. Report success/failure clearly.

**Questions?** File issues at: https://github.com/liminalcommons/chora-base/issues

---

*Generated by chora-base v3.0.0*
*https://github.com/liminalcommons/chora-base*
