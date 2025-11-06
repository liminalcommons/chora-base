# Generic Project Bootstrap Design

**Status**: Draft
**Date**: 2025-11-06
**Related**: SAP-003 (project-bootstrap), create-model-mcp-server.py v1.0.0

---

## Problem Statement

Currently, `create-model-mcp-server.py` is **MCP-server specific**. There's an opportunity to **genericize** the approach for:

1. **Generic Python Projects** (CLI tools, libraries, APIs)
2. **Other Server Types** (HTTP servers, WebSocket servers, gRPC servers)
3. **Multi-Language Support** (TypeScript, Go, Rust projects in the future)

---

## Current State

### create-model-mcp-server.py

**What it creates**:
- FastMCP server scaffold
- MCP namespace module (mcp/__init__.py)
- MCP-specific templates (server.py with @mcp.tool() decorators)
- Chora MCP Conventions v1.0 compliance

**What's generic** (can be reused):
- Directory structure creation
- Template rendering logic (Jinja2)
- SAP initialization (beads, inbox, A-MEM)
- Git initialization
- Validation framework
- Decision profiles

**What's MCP-specific**:
- Template selection (mcp-templates/)
- Variable derivation (mcp_namespace)
- Validation checks (MCP namespace module)
- Documentation references

---

## Proposed Architecture

### Option 1: Project Type Flag (Recommended)

Single script with `--type` flag:

```bash
# MCP Server
python scripts/create-project.py \
    --type mcp-server \
    --name "Weather MCP" \
    --namespace weather \
    --output ~/projects/weather-mcp

# Generic Python Project
python scripts/create-project.py \
    --type python-library \
    --name "My Utility Library" \
    --output ~/projects/my-library

# CLI Tool
python scripts/create-project.py \
    --type python-cli \
    --name "My CLI Tool" \
    --output ~/projects/my-cli
```

**Pros**:
- Single script to maintain
- Shared validation logic
- Consistent interface
- Easy to add new project types

**Cons**:
- Larger script file
- More complex conditional logic

---

### Option 2: Separate Scripts per Type

Multiple scripts, shared library:

```
scripts/
├── create-mcp-server.py         # MCP servers
├── create-python-library.py     # Libraries
├── create-python-cli.py         # CLI tools
└── lib/
    ├── project_generator.py     # Shared generator logic
    ├── template_renderer.py     # Jinja2 rendering
    ├── sap_initializer.py       # SAP setup
    └── validator.py             # Validation framework
```

**Pros**:
- Smaller, focused scripts
- Type-specific help text
- Easier to understand per-type

**Cons**:
- More files to maintain
- Code duplication risk
- Inconsistent interfaces

---

### Option 3: Plugin Architecture (Future)

Extensible plugin system:

```python
# scripts/create-project.py --plugin mcp-server
# scripts/create-project.py --plugin python-library

# plugins/
# ├── mcp_server.py
# ├── python_library.py
# └── python_cli.py
```

**Pros**:
- Highly extensible
- Community plugins
- Clean separation

**Cons**:
- More complex
- Overhead for small projects
- Requires plugin discovery mechanism

---

## Recommended Approach (Phased)

### Phase 1: Refactor Current Script (Week 1)

**Goal**: Extract generic logic into reusable functions

**Changes**:
1. Rename `create-model-mcp-server.py` → `create-mcp-server.py` (clarity)
2. Extract functions:
   - `create_directory_structure(output_dir, structure_spec)`
   - `render_templates(template_dir, output_dir, variables)`
   - `initialize_saps(output_dir, sap_list, variables)`
   - `validate_project(output_dir, requirements)`
3. Move to `scripts/lib/project_generator.py`

**Outcome**: Clean, testable library ready for reuse

**Time Estimate**: 4-6 hours

---

### Phase 2: Create Generic Python Project Script (Week 2)

**Goal**: Support non-MCP Python projects

**New Script**: `scripts/create-python-project.py`

```bash
python scripts/create-python-project.py \
    --type library \
    --name "My Utility Library" \
    --output ~/projects/my-library
```

**Project Types**:
- `library` - Installable Python package (no entry point)
- `cli` - Command-line tool (entry points in pyproject.toml)
- `api` - FastAPI/Flask HTTP API server
- `service` - Generic long-running service

**Templates**:
- Create `static-template/python-templates/` with generic templates
- Reuse common templates (pyproject.toml, AGENTS.md, CLAUDE.md)

**Time Estimate**: 8-12 hours

---

### Phase 3: Unified Interface (Month 2)

**Goal**: Single entry point with project type detection

**New Script**: `scripts/create-project.py` (replaces both)

```bash
# Auto-detect from --type
python scripts/create-project.py --type mcp-server --name "Weather" ...
python scripts/create-project.py --type python-library --name "Utils" ...

# Keep old scripts as symlinks for backwards compatibility
ln -s create-project.py create-mcp-server.py
ln -s create-project.py create-python-project.py
```

**Time Estimate**: 12-16 hours

---

## Template Organization

### Current Structure

```
static-template/
├── mcp-templates/          # MCP server specific
│   ├── server.py.template
│   ├── mcp__init__.py.template
│   └── ...
├── .github/workflows/      # Generic (all projects)
├── tests/                  # Generic structure
└── docs/                   # Generic structure
```

### Proposed Structure

```
static-template/
├── common/                 # All projects
│   ├── .github/workflows/
│   ├── .gitignore
│   ├── .editorconfig
│   └── docs/
├── mcp-server/             # MCP server specific
│   ├── server.py.template
│   ├── mcp__init__.py.template
│   └── pyproject.toml.template
├── python-library/         # Library specific
│   ├── __init__.py.template
│   ├── pyproject.toml.template
│   └── README.md.template
├── python-cli/             # CLI specific
│   ├── cli.py.template
│   ├── commands/
│   └── pyproject.toml.template
└── python-api/             # API specific
    ├── app.py.template
    ├── routers/
    └── pyproject.toml.template
```

---

## Variable Schema

### Common Variables (All Projects)

```python
{
    "project_name": str,           # "My Project"
    "project_slug": str,           # "my-project"
    "package_name": str,           # "my_project"
    "project_description": str,
    "author_name": str,
    "author_email": str,
    "github_username": str,
    "python_version": str,         # "3.11"
    "license": str,                # "MIT"
    "include_beads": bool,
    "include_inbox": bool,
    "include_memory": bool,
    "include_ci_cd": bool,
}
```

### MCP-Specific Variables

```python
{
    "mcp_namespace": str,          # "weather"
    "mcp_enable_namespacing": bool,
    "mcp_validate_names": bool,
}
```

### CLI-Specific Variables

```python
{
    "cli_command_name": str,       # "mytool"
    "cli_has_subcommands": bool,
}
```

### API-Specific Variables

```python
{
    "api_framework": str,          # "fastapi" or "flask"
    "api_port": int,               # 8000
    "api_include_auth": bool,
}
```

---

## Validation Framework

### Generic Validation Checks

**All Projects**:
1. AGENTS.md with YAML frontmatter
2. CLAUDE.md exists
3. Testing framework configured (pytest)
4. Quality gates configured (ruff, mypy)
5. Documentation structure (Diátaxis)
6. No unsubstituted variables

**Optional** (based on profile):
7. Beads initialized
8. Inbox initialized
9. Memory system initialized
10. CI/CD workflows configured

### Type-Specific Validation

**MCP Server**:
- FastMCP server exists
- MCP namespace module exists
- Chora MCP Conventions compliance

**Python Library**:
- `__init__.py` with version
- `py.typed` for type hints
- PyPI publish workflow

**CLI Tool**:
- Entry point defined in pyproject.toml
- `--help` text renders
- Click/Typer configuration

---

## Migration Path for Existing Script

### Backwards Compatibility

**Keep** `create-model-mcp-server.py` as:
```python
#!/usr/bin/env python3
"""DEPRECATED: Use create-mcp-server.py or create-project.py --type mcp-server

This script is kept for backwards compatibility.
"""
import sys
from create_mcp_server import main

if __name__ == "__main__":
    print("⚠️  Warning: create-model-mcp-server.py is deprecated")
    print("   Use: create-mcp-server.py or create-project.py --type mcp-server")
    print()
    sys.exit(main())
```

**Update** documentation to reference new script names

**Deprecation Timeline**:
- v4.9.0: Add deprecation warning
- v4.10.0: Redirect to new script
- v5.0.0: Remove old script

---

## Example Usage (Future State)

### MCP Server

```bash
python scripts/create-project.py \
    --type mcp-server \
    --name "Weather MCP Server" \
    --namespace weather \
    --output ~/projects/weather-mcp
```

### Python Library

```bash
python scripts/create-project.py \
    --type library \
    --name "My Utilities" \
    --output ~/projects/my-utils \
    --include-beads \
    --include-ci-cd
```

### CLI Tool

```bash
python scripts/create-project.py \
    --type cli \
    --name "My CLI Tool" \
    --cli-command mytool \
    --output ~/projects/my-cli
```

### API Server

```bash
python scripts/create-project.py \
    --type api \
    --name "My API" \
    --api-framework fastapi \
    --api-port 8000 \
    --output ~/projects/my-api
```

---

## Implementation Checklist

### Phase 1: Refactor (Week 1)

- [ ] Extract generic functions to `scripts/lib/project_generator.py`
- [ ] Rename `create-model-mcp-server.py` → `create-mcp-server.py`
- [ ] Update documentation references
- [ ] Add deprecation warning to old script name

### Phase 2: Generic Python Projects (Week 2)

- [ ] Create `static-template/python-library/` templates
- [ ] Create `static-template/python-cli/` templates
- [ ] Create `static-template/python-api/` templates
- [ ] Implement `create-python-project.py`
- [ ] Add type-specific validation checks
- [ ] Write tests for new project types

### Phase 3: Unified Interface (Month 2)

- [ ] Create `create-project.py` with `--type` flag
- [ ] Implement project type detection
- [ ] Create backwards compatibility symlinks
- [ ] Update all documentation
- [ ] Create migration guide

### Phase 4: Documentation & Examples (Month 2)

- [ ] Update quickstart guides for each project type
- [ ] Create example projects in `examples/`
- [ ] Add validation tests
- [ ] Write contributor guide for adding new project types

---

## Success Metrics

**Phase 1**:
- [ ] All existing MCP server generation works identically
- [ ] Generic functions have unit tests
- [ ] Code duplication reduced by 60%+

**Phase 2**:
- [ ] Can create Python library in <5 minutes
- [ ] Can create CLI tool in <5 minutes
- [ ] Validation passes for all project types

**Phase 3**:
- [ ] Single script handles 4+ project types
- [ ] Backwards compatibility maintained
- [ ] Documentation updated across 6+ files

---

## Future Extensions

### Multi-Language Support

- TypeScript/Node.js projects (MCP servers in TypeScript)
- Go projects (gRPC services, CLI tools)
- Rust projects (high-performance services)

### Template Marketplace

- Community-contributed templates
- Organization-specific templates
- Industry-specific templates (healthcare, finance, etc.)

### Interactive Mode

```bash
python scripts/create-project.py --interactive

? What type of project? (Use arrow keys)
  ❯ MCP Server
    Python Library
    CLI Tool
    API Server

? Project name: My Awesome Project
? Include task tracking (beads)? Yes
? Include CI/CD workflows? Yes
...
```

---

## Conclusion

**Immediate Action**: Keep `create-mcp-server.py` as-is (it works!)

**Short-Term** (1-2 months): Refactor to support generic Python projects

**Long-Term** (3-6 months): Unified interface with plugin architecture

**The genericization opportunity is real**, but the current MCP-server-specific script provides immediate value. Genericization can happen incrementally without disrupting existing workflows.

---

**Next Steps**:
1. Validate current MCP server generation works end-to-end
2. Gather requirements for generic Python projects
3. Start Phase 1 refactoring when time permits

**Status**: Design complete, awaiting prioritization
