# Namespace Declaration: choracompose

**MCP Server Namespace:** `choracompose`

This document declares the MCP namespace for chora-compose following the [Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md).

## Namespace Format

- **Pattern:** `choracompose`
- **Format:** Lowercase alphanumeric, 3-20 characters
- **Validation:** ✅ Compliant with Chora MCP Conventions v1.0

## Tool Naming

All MCP tools exposed by chora-compose use the namespace prefix:

```
Pattern: choracompose:tool_name
```

**Examples:**
- `choracompose:generate_content`
- `choracompose:assemble_artifact`
- `choracompose:list_generators`
- `choracompose:validate_content`

## Resource URIs

All MCP resources use the namespace URI scheme:

```
Pattern: choracompose://resource_type/resource_id[?query]
```

**Examples:**
- `choracompose://templates/daily-report.md`
- `choracompose://capabilities/server`
- `choracompose://content/example-001`

## Ecosystem Integration

### Claude Desktop

chora-compose integrates with Claude Desktop as an MCP server. Tools are invoked using the namespaced format:

```json
{
  "tool": "choracompose:generate_content",
  "arguments": {
    "content_config_id": "example"
  }
}
```

### mcp-n8n Gateway

The `choracompose` namespace enables routing through the [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) gateway for workflow automation.

## Namespace Coordination

To avoid conflicts with other MCP servers:

1. **Search:** Check [MCP registry](https://github.com/modelcontextprotocol/servers) for existing namespaces
2. **Announce:** Document in this file and project README
3. **Register:** Submit PR to upstream registries if applicable

## Related Documentation

- [Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Namespace format standard
- [MCP Naming Best Practices](https://github.com/liminalcommons/chora-base/blob/main/docs/reference/mcp-naming-best-practices.md) - Practical naming guide

## Validation

Validate namespace usage:

```bash
# Run AST-based MCP name validation
python scripts/validate_mcp_names.py
```

Expected output:
```
✅ All MCP names follow Chora MCP Conventions v1.0
```

---

**Last Updated:** 2025-10-22
**Version:** chora-compose v1.5.0
**Template:** chora-base v1.9.0
