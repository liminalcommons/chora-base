# Reference: Template Configuration Options

## Quick Lookup

All configuration options for `copier copy gh:liminalcommons/chora-base`

---

## Project Metadata

| Variable | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `project_name` | str | *required* | Project name (kebab-case) | `my-mcp-server` |
| `project_slug` | str | *auto* | Auto-derived from project_name | `my-mcp-server` |
| `package_name` | str | *auto* | Python package name (snake_case) | `my_mcp_server` |
| `project_description` | str | *required* | Short description | "MCP server for Coda" |
| `project_version` | str | `"0.1.0"` | Initial version | `"1.0.0"` |

## Author Information

| Variable | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `author_name` | str | *required* | Your name | "Jane Doe" |
| `author_email` | str | *required* | Your email | "jane@example.com" |
| `github_username` | str | *required* | GitHub username/org | "liminalcommons" |

## Python Configuration

| Variable | Type | Choices | Default | Description |
|----------|------|---------|---------|-------------|
| `python_version` | str | `3.11`, `3.12`, `3.13` | `"3.11"` | Minimum Python version |

## Project Type

| Variable | Type | Choices | Default | Description | Impact |
|----------|------|---------|---------|-------------|--------|
| `project_type` | str | `mcp_server`, `library`, `cli_tool`, `web_service` | `mcp_server` | Project type | Determines dependencies, entry points, README structure |

## Features

| Variable | Type | Default | Description | Files Added/Modified |
|----------|------|---------|-------------|----------------------|
| `include_cli` | bool | `true` | CLI interface | `src/{{package_name}}/cli/main.py`, entry point in pyproject.toml |
| `cli_framework` | str | `click` | CLI framework (if include_cli=true) | click or typer dependency |
| `include_memory_system` | bool | `true` | Agent Memory System | `src/{{package_name}}/memory/`, `.chora/memory/`, memory CLI |
| `include_agents_md` | bool | `true` | Machine-readable instructions | `AGENTS.md` (900+ lines) |
| `include_tests` | bool | `true` | Testing infrastructure | `tests/`, pytest config |
| `test_coverage_threshold` | int | `85` | Test coverage % required | `--cov-fail-under` in pytest config |
| `include_pre_commit` | bool | `true` | Pre-commit hooks | `.pre-commit-config.yaml` |
| `include_github_actions` | bool | `true` | CI/CD workflows | `.github/workflows/` (7 workflows) |
| `include_justfile` | bool | `true` | Task automation | `justfile` (20+ tasks) |
| `include_docker` | bool | `false` | Docker configuration | `Dockerfile`, `docker-compose.yml` |

## Documentation

| Variable | Type | Default | Description | Files Added |
|----------|------|---------|-------------|-------------|
| `include_contributing` | bool | `true` | CONTRIBUTING.md | `CONTRIBUTING.md` |
| `include_development_docs` | bool | `true` | DEVELOPMENT.md | `docs/DEVELOPMENT.md` |
| `include_troubleshooting` | bool | `true` | TROUBLESHOOTING.md | `docs/TROUBLESHOOTING.md` |

## License

| Variable | Type | Choices | Default | Description |
|----------|------|---------|---------|-------------|
| `license` | str | `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`, `Proprietary` | `MIT` | Project license |

---

## Configuration Examples

### Minimal MCP Server

```bash
copier copy gh:liminalcommons/chora-base my-project
```

**Answers:**
```yaml
project_name: my-project
author_name: Jane Doe
python_version: "3.11"
project_type: mcp_server
include_memory_system: false  # Minimal
include_agents_md: false      # Minimal
include_cli: false            # Minimal
include_justfile: false       # Minimal
```

**Result:** Basic MCP server with tests, workflows, no memory system

---

### Full-Featured MCP Server (Recommended)

```bash
copier copy gh:liminalcommons/chora-base my-project
```

**Answers:**
```yaml
project_name: my-project
author_name: Jane Doe
python_version: "3.12"
project_type: mcp_server
include_memory_system: true   # Agent learning
include_agents_md: true       # AI instructions
include_cli: true             # Memory CLI
cli_framework: click
include_tests: true
test_coverage_threshold: 90   # Stricter
include_github_actions: true
include_justfile: true
```

**Result:** MCP server with memory, AGENTS.md, CLI, workflows, justfile (all features)

---

### Python Library

```bash
copier copy gh:liminalcommons/chora-base my-library
```

**Answers:**
```yaml
project_name: my-library
project_type: library         # Not MCP server
include_memory_system: false  # Libraries don't need memory
include_agents_md: true       # Still useful for contributors
include_cli: false            # No CLI for library
```

**Result:** Python library with AGENTS.md, tests, workflows (no MCP-specific features)

---

## File Inventory by Configuration

### Always Included

```
.editorconfig
.gitignore
CHANGELOG.md
LICENSE
README.md
pyproject.toml
```

### If `include_memory_system=true`

```
.chora/memory/README.md
src/{{package_name}}/memory/__init__.py
src/{{package_name}}/memory/event_log.py
src/{{package_name}}/memory/knowledge_graph.py
src/{{package_name}}/memory/trace.py
```

### If `include_agents_md=true`

```
AGENTS.md (900+ lines)
```

### If `include_cli=true`

```
src/{{package_name}}/cli/__init__.py
src/{{package_name}}/cli/main.py
[project.scripts] entry point
```

### If `include_tests=true`

```
tests/conftest.py
tests/test_example.py
[tool.pytest.ini_options] in pyproject.toml
```

### If `include_github_actions=true`

```
.github/workflows/test.yml
.github/workflows/lint.yml
.github/workflows/smoke.yml
.github/workflows/release.yml
.github/workflows/codeql.yml
.github/workflows/dependency-review.yml
.github/workflows/dependabot-automerge.yml
```

### If `include_justfile=true`

```
justfile (20+ tasks)
```

### If `project_type=mcp_server`

```
src/{{package_name}}/server.py
Dependencies: fastmcp>=0.3.0, pydantic>=2.0.0
```

---

## See Also

- [How-To: Generate New MCP Server](../how-to/01-generate-new-mcp-server.md)
- [Explanation: Project Type Comparison](../explanation/project-types.md)
- [Reference: Generated File Structure](generated-file-structure.md)
