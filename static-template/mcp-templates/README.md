# MCP Templates

**Status**: Placeholder (Wave 3 Track 1 Phase 5)
**Last Updated**: 2025-10-29

---

## Overview

This directory will contain MCP server templates extracted from `blueprints/` during Wave 3 Track 1 Phase 5.

**Timeline**: Phase 5 (scheduled after Phase 3 and Phase 4)

---

## Planned Templates

The following blueprint files will be moved here in Phase 5:

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
⏳ **Phase 4** (Pending): Generalize root documentation
⏳ **Phase 5** (Pending): Move blueprints/ to this directory
⏳ **Phase 6** (Pending): Validation & cleanup

---

## Usage (After Phase 5)

Once templates are moved here, SAP-014 adoption will use these files:

```bash
# Example: Create new MCP server using SAP-014
cp -r static-template/mcp-templates my-mcp-server/
cd my-mcp-server
# Customize templates with your namespace and tools
```

---

## Related Documentation

- [SAP-014: MCP Server Development](../../docs/skilled-awareness/mcp-server-development/) - Full MCP guide
- [Wave 3 Execution Plan](../../docs/project-docs/wave-3-execution-plan.md) - Wave 3 roadmap
- [MCP Specificity Audit](../../docs/project-docs/mcp-specificity-audit.md) - Blueprint analysis

---

**Last Updated**: 2025-10-29
**Phase**: 3 (4-domain documentation)
**Next**: Phase 4 (root doc generalization)
