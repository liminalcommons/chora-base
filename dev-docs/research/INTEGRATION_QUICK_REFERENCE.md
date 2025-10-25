---
title: MCP-Orchestration Integration Quick Reference
status: active
version: 1.0.0
last_updated: 2025-10-24
---

# MCP-Orchestration Integration Quick Reference

**TL;DR:** Fast answers for peer repositories integrating with mcp-orchestration.

For detailed guidance, see [ECOSYSTEM_INTEGRATION.md](./ECOSYSTEM_INTEGRATION.md).

---

## What is mcp-orchestration?

**MCP server** that manages MCP client configurations with:
- Server registry (15+ MCP servers)
- Configuration builder (draft workflow)
- Cryptographic signing (Ed25519)
- Diff detection

**Current Version:** v0.1.3 (Wave 1.3)
**Stability:** Stable
**Transport:** stdio (HTTP in Wave 2.x)

---

## 30-Second Integration

```bash
# Install
pip install mcp-orchestration

# Initialize
mcp-orchestration-init

# Add to your MCP client config
```

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

---

## Which Pattern Do I Use?

### I'm building an MCP client
→ **Pattern 1: Client Configuration Manager**
- Add mcp-orchestration as MCP server
- Use tools: `list_available_servers`, `add_server_to_config`, `publish_config`
- Status: ✅ Stable

### I'm building a config management UI
→ **Pattern 2: Frontend Configuration Builder**
- Use subprocess invocation (Wave 1.x workaround)
- Wait for HTTP transport (Wave 2.x)
- Status: ⚠️ Experimental

### I want n8n workflows as MCP tools
→ **Pattern 3: n8n Integration**
- Use `mcp-server-n8n` (not mcp-orchestration as gateway)
- Register n8n server in mcp-orchestration registry
- Status: 📋 Planned (awaits mcp-server-n8n extraction)

### I'm building an MCP gateway
→ **Pattern 4: MCP Gateway Integration**
- Mount mcp-orchestration as backend
- Requires HTTP transport (Wave 2.x)
- Status: 📋 Planned

---

## Quick Code Examples

### Pattern 1: Use as MCP Server

```typescript
// In your MCP client (e.g., Claude Desktop)
await client.callTool("list_available_servers", {
  transport_filter: "stdio"
});

await client.callTool("add_server_to_config", {
  server_id: "filesystem",
  params: { path: "/data" }
});

await client.callTool("publish_config", {
  changelog: "Added filesystem server"
});
```

### Pattern 2: Frontend Integration (Workaround)

```typescript
// Node.js subprocess
import { spawn } from 'child_process';

const proc = spawn('mcp-orchestration', []);

// Send MCP JSON-RPC via stdio
proc.stdin.write(JSON.stringify({
  jsonrpc: "2.0",
  method: "tools/call",
  params: { name: "list_available_servers" },
  id: 1
}) + '\n');
```

### Pattern 3: Register n8n Server

```python
# In server registry (future PR)
ServerDefinition(
    server_id="n8n",
    display_name="n8n Workflows",
    transport="stdio",
    npm_package="mcp-server-n8n",
    stdio_command="npx",
    stdio_args=["-y", "mcp-server-n8n"],
    required_env=["N8N_API_URL", "N8N_API_KEY"]
)
```

### Pattern 4: Mount in Gateway

```python
# mcp-gateway configuration (future)
from fastmcp import FastMCP, Client

gateway = FastMCP("Gateway")
orch_client = Client("http://localhost:8080/mcp")
proxy = FastMCP.as_proxy(orch_client, name="orch")
gateway.mount("orch", proxy)
```

---

## Available Tools (v0.1.3)

| Tool | Description | Wave |
|------|-------------|------|
| `list_clients` | List MCP clients | 1.0 |
| `list_profiles` | List profiles | 1.0 |
| `get_config` | Get signed config | 1.0 |
| `diff_config` | Compare configs | 1.0 |
| `list_available_servers` | Browse server registry | 1.1 |
| `describe_server` | Get server details | 1.1 |
| `add_server_to_config` | Add to draft | 1.2 |
| `remove_server_from_config` | Remove from draft | 1.2 |
| `view_draft_config` | View draft | 1.3 |
| `clear_draft_config` | Clear draft | 1.3 |
| `publish_config` | Sign & publish | 1.3 |
| `initialize_keys` | Generate keys | 1.3 |

---

## Capability Manifest

```yaml
id: mcp.orchestration
version: 0.1.3
owner: liminalcommons/mcp-orchestration
lifecycle_stage: operate
stability: stable
security_tier: moderate

capabilities:
  - mcp.orchestration.client.list
  - mcp.orchestration.config.get
  - mcp.orchestration.config.diff
  - mcp.orchestration.registry.list
  - mcp.orchestration.config.build
  - mcp.orchestration.config.publish

discovery:
  pypi_package: mcp-orchestration
  cli_commands: [mcp-orchestration, mcp-orchestration-init]
  repository: https://github.com/liminalcommons/mcp-orchestration
```

---

## Common Questions

### Can mcp-orchestration be an MCP gateway?
**No.** Use `mcp-gateway` (Python/FastMCP) instead. mcp-orchestration can be **mounted as a backend** in a gateway.

### Can n8n be an MCP gateway?
**No (45% feasibility).** Use n8n as an **MCP server** (exposes workflows as tools), not as a gateway.

### Does mcp-orchestration support HTTP transport?
**Not yet (Wave 2.x).** Current: stdio only. Workaround: subprocess invocation.

### Can I register custom MCP servers?
**Yes!** Add `ServerDefinition` to registry. See [ECOSYSTEM_INTEGRATION.md](./ECOSYSTEM_INTEGRATION.md#example-2-register-your-custom-mcp-server).

### How do I migrate from manual configs?
Use `add_server_to_config` → `publish_config`. See [Migration Paths](./ECOSYSTEM_INTEGRATION.md#migration-paths).

---

## Decision Tree

```
Need to manage MCP configs?
  YES → Are you building:
        • MCP client?          → Pattern 1 (Stable ✅)
        • Config UI?           → Pattern 2 (Planned 📋)
        • n8n integration?     → Pattern 3 (Planned 📋)
        • MCP gateway?         → Pattern 4 (Planned 📋)
  NO  → Consider other tools
```

---

## Roadmap

| Wave | Version | Focus | Status |
|------|---------|-------|--------|
| 1.0 | v0.1.0 | Foundation | ✅ |
| 1.1 | v0.1.1 | Server registry | ✅ |
| 1.2 | v0.1.2 | Config building | ✅ |
| 1.3 | v0.1.3 | Ergonomics | ✅ |
| 2.x | v0.2.x | HTTP transport | 📋 |
| 3.x | v0.3.x | Multi-user, RBAC | 📋 |

---

## Links

- **Full Integration Guide**: [ECOSYSTEM_INTEGRATION.md](./ECOSYSTEM_INTEGRATION.md)
- **User Docs**: [user-docs/README.md](../../user-docs/README.md)
- **MCP Tools Reference**: [user-docs/reference/mcp-tools.md](../../user-docs/reference/mcp-tools.md)
- **Research**: [MCP-n8n to MCP-Gateway Evolution.md](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md)
- **Ecosystem Standards**: [dev-docs/vision/ecosystem-intent.md](../../dev-docs/vision/ecosystem-intent.md)

---

## Getting Help

- **Issues**: https://github.com/liminalcommons/mcp-orchestration/issues
- **Documentation**: [user-docs/](../../user-docs/)
- **Ecosystem Coordination**: File change signal via ecosystem process

---

**Last Updated:** 2025-10-24
**Status:** Active
**Audience:** Peer repository developers
