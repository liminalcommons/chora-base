# MCP Templates

**Status**: Active (Phase 5 Complete - 2025-10-29)
**Last Updated**: 2025-10-29

---

## Overview

This directory contains MCP server templates for use with SAP-014 (MCP Server Development). These templates were extracted from `blueprints/` during Wave 3 Track 1 Phase 5.

**Timeline**: Phase 5 completed on 2025-10-29

---

## Available Templates

The following template files are now available:

1. **server.py.template** - FastMCP server entry point
2. **mcp__init__.py.template** - MCP namespace module (Chora MCP Conventions v1.0)
3. **pyproject.toml.template** - Python project configuration with FastMCP
4. **AGENTS.md.template** - MCP server agent guidance
5. **CLAUDE.md.template** - MCP client configuration
6. **README.md.template** - MCP server documentation
7. **CHANGELOG.md.template** - Version history template
8. **ROADMAP.md.template** - Future capabilities planning
9. **package__init__.py.template** - Python package initialization

**Total**: 9 template files (~77KB)

---

## Current Status

✅ **Phase 1** (Complete): MCP specificity audit
✅ **Phase 2** (Complete): SAP-014 artifact creation (5 files, ~4,400 lines)
✅ **Phase 3** (Complete): 4-domain supporting documentation (8 files, ~3,000 lines)
✅ **Phase 4** (Complete): Generalize root documentation
✅ **Phase 5** (Complete): Move blueprints/ to this directory (11 templates, ~2,700 lines)
⏳ **Phase 6** (Pending): Validation & cleanup

---

## Usage

SAP-014 adoption uses these templates to create new MCP servers:

```bash
# Example: Create new MCP server using SAP-014
cp -r static-template/mcp-templates my-mcp-server/
cd my-mcp-server
# Customize templates with your namespace and tools
```

## Template Variables

All templates use these variables (replace during adoption):

| Variable | Example | Description |
|----------|---------|-------------|
| `{{ project_name }}` | my-mcp-server | Project name (kebab-case) |
| `{{ package_name }}` | my_mcp_server | Python package (snake_case) |
| `{{ author_name }}` | Jane Doe | Your full name |
| `{{ author_email }}` | jane@example.com | Your email |
| `{{ github_username }}` | janedoe | GitHub username |
| `{{ namespace }}` | myapp | MCP namespace (3-20 chars, lowercase) |
| `{{ project_short_description }}` | My MCP Server | One-line description |

---

## Related Documentation

- [SAP-014: MCP Server Development](../../docs/skilled-awareness/mcp-server-development/) - Full MCP guide
- [Wave 3 Execution Plan](../../docs/project-docs/wave-3-execution-plan.md) - Wave 3 roadmap
- [MCP Specificity Audit](../../docs/project-docs/mcp-specificity-audit.md) - Blueprint analysis

---

**Last Updated**: 2025-10-29
**Phase**: 3 (4-domain documentation)
**Next**: Phase 4 (root doc generalization)
