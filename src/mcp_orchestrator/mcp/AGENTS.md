# MCP Server Implementation Guide

**Purpose:** Guide for MCP server implementation (protocol, tools, resources).

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **MCP spec:** [../../dev-docs/vision/MCP_SERVER_SPEC.md](../../dev-docs/vision/MCP_SERVER_SPEC.md)
- **Start server:** `mcp-orchestration` or `python -m mcp_orchestrator.mcp.server`
- **Add tool:** See "Adding New MCP Tools" section
- **Testing:** `pytest tests/integration/test_mcp_server.py`

---

## Architecture

**Path:** `src/mcp_orchestrator/mcp/`

**MCP Protocol:** Model Context Protocol 2024-11-05

**Server Implementation:** FastMCP (stdio transport)

### Files

```
mcp/
├── __init__.py           # Public API exports
├── server.py             # Main server (entry point, @mcp.tool decorators)
├── tools.py              # MCP tool implementations
└── resources.py          # MCP resource implementations
```

---

## MCP Server Overview

### Server Identity

```json
{
  "name": "mcp-orchestration",
  "version": "0.1.0",
  "description": "MCP client configuration orchestration and distribution",
  "protocol_version": "2024-11-05",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": false,
    "sampling": false
  }
}
```

### Entry Points

**CLI:**
```bash
# Production
mcp-orchestration

# Development (with hot reload)
python -m mcp_orchestrator.mcp.server

# With debug logging
MCP_ORCHESTRATION_DEBUG=1 mcp-orchestration
```

**Programmatic:**
```python
from mcp_orchestrator.mcp.server import run_server

# Blocking
run_server()

# Or async
import asyncio
asyncio.run(run_server())
```

### Protocol: stdio

**Transport:** Standard input/output (stdin/stdout)

**Why stdio?**
- Simple: No network configuration, no ports
- Secure: Runs as subprocess, inherits parent permissions
- Standard: MCP spec default transport
- Debuggable: Can capture stdin/stdout for inspection

**Communication Format:**
- **Request:** JSON-RPC 2.0 over stdin
- **Response:** JSON-RPC 2.0 over stdout
- **Errors:** Structured error responses with error codes

---

## MCP Tools (4)

### Tool 1: `list_clients`

**Purpose:** Discover supported MCP client families (FR-1)

**Input:** None

**Output:**
```json
{
  "clients": [
    {
      "client_id": "claude-desktop",
      "display_name": "Claude Desktop",
      "platform": "macos",
      "available_profiles": ["default", "development"]
    },
    {
      "client_id": "cursor",
      "display_name": "Cursor IDE",
      "platform": "cross-platform",
      "available_profiles": ["default"]
    }
  ],
  "count": 2
}
```

**Implementation:**
```python
@mcp.tool()
async def list_clients() -> dict:
    """List supported MCP client families."""
    from mcp_orchestrator.registry import list_clients

    clients = list_clients()
    return {"clients": clients, "count": len(clients)}
```

### Tool 2: `list_profiles`

**Purpose:** List available profiles for a client (FR-2)

**Input:**
```json
{
  "client_id": "claude-desktop"
}
```

**Output:**
```json
{
  "profiles": [
    {
      "profile_id": "default",
      "artifact_id": "aabbccddee...",
      "created_at": "2025-10-24T12:00:00Z"
    },
    {
      "profile_id": "development",
      "artifact_id": "112233...ef",
      "created_at": "2025-10-24T13:00:00Z"
    }
  ],
  "count": 2
}
```

**Implementation:**
```python
@mcp.tool()
async def list_profiles(client_id: str) -> dict:
    """List profiles for a client."""
    from mcp_orchestrator.registry import list_profiles

    profiles = list_profiles(client_id)
    return {"profiles": profiles, "count": len(profiles)}
```

### Tool 3: `get_config`

**Purpose:** Retrieve signed configuration artifact (FR-4)

**Input:**
```json
{
  "client_id": "claude-desktop",
  "profile_id": "default"
}
```

**Output:**
```json
{
  "artifact_id": "aabbccddee...",
  "client_id": "claude-desktop",
  "profile": "default",
  "payload": {
    "mcpServers": {
      "filesystem": {
        "command": "mcp-filesystem",
        "args": ["--root", "/workspace"]
      }
    }
  },
  "signature": {
    "algorithm": "ed25519",
    "value": "base64-signature...",
    "timestamp": "2025-10-24T12:00:00Z"
  },
  "metadata": {
    "created_at": "2025-10-24T12:00:00Z",
    "version": "1.0"
  }
}
```

**Implementation:**
```python
@mcp.tool()
async def get_config(client_id: str, profile_id: str = "default") -> dict:
    """Retrieve signed configuration artifact."""
    from mcp_orchestrator.registry import get_profile
    from mcp_orchestrator.storage import get_artifact
    from mcp_orchestrator.crypto import verify_signature

    # 1. Get profile (resolves artifact_id)
    profile = get_profile(client_id, profile_id)
    artifact_id = profile["artifact_id"]

    # 2. Retrieve artifact from storage
    artifact = get_artifact(artifact_id)

    # 3. Verify signature
    if not verify_signature(artifact):
        raise SecurityError("Signature verification failed")

    return artifact
```

### Tool 4: `diff_config`

**Purpose:** Compare local config against canonical (FR-9)

**Input:**
```json
{
  "client_id": "claude-desktop",
  "profile_id": "default",
  "local_payload": {
    "mcpServers": {
      "filesystem": {
        "command": "mcp-filesystem",
        "args": ["--root", "/old/path"]
      }
    }
  }
}
```

**Output:**
```json
{
  "status": "outdated",
  "changes": [
    {
      "type": "modified",
      "path": "mcpServers.filesystem.args",
      "canonical_value": ["--root", "/new/path"],
      "local_value": ["--root", "/old/path"],
      "semantic": "breaking"
    }
  ],
  "recommendation": "review",
  "metadata": {
    "canonical_artifact_id": "aabbccddee...",
    "change_count": 1,
    "breaking_changes": 1
  }
}
```

**Implementation:**
```python
@mcp.tool()
async def diff_config(
    client_id: str,
    profile_id: str,
    local_payload: dict
) -> dict:
    """Compare local config against canonical."""
    from mcp_orchestrator.diff import diff_configs

    # 1. Get canonical config
    canonical_artifact = await get_config(client_id, profile_id)
    canonical_payload = canonical_artifact["payload"]

    # 2. Diff
    diff_result = diff_configs(local_payload, canonical_payload)

    return diff_result
```

---

## MCP Resources (2)

### Resource 1: `capabilities://server`

**Purpose:** Server capabilities and metadata

**URI:** `capabilities://server`

**Output:**
```json
{
  "name": "mcp-orchestration",
  "version": "0.1.0",
  "protocol_version": "2024-11-05",
  "capabilities": {
    "tools": ["list_clients", "list_profiles", "get_config", "diff_config"],
    "resources": ["capabilities://server", "capabilities://clients"]
  },
  "metadata": {
    "wave": "1.1",
    "features": ["config-orchestration", "crypto-signing", "diff-engine"]
  }
}
```

### Resource 2: `capabilities://clients`

**Purpose:** Supported client families

**URI:** `capabilities://clients`

**Output:**
```json
{
  "clients": [
    {
      "client_id": "claude-desktop",
      "display_name": "Claude Desktop",
      "platform": "macos",
      "capabilities": {
        "tools": true,
        "resources": true,
        "prompts": true
      }
    },
    {
      "client_id": "cursor",
      "display_name": "Cursor IDE",
      "platform": "cross-platform",
      "capabilities": {
        "tools": true,
        "resources": true,
        "prompts": false
      }
    }
  ]
}
```

---

## Adding New MCP Tools

### When to Add

- Exposes new functionality from orchestrator modules
- Aligns with roadmap (check [../../project-docs/AGENTS.md](../../project-docs/AGENTS.md))
- Follows MCP specification (see [../../dev-docs/vision/MCP_SERVER_SPEC.md](../../dev-docs/vision/MCP_SERVER_SPEC.md))
- Wave-appropriate (don't add Wave 2 tools in Wave 1)

### Steps

**1. Define tool in `server.py`:**

```python
@mcp.tool()
async def new_tool(param: str) -> dict:
    """Tool description for LLM (will appear in tool list).

    Args:
        param: Parameter description (visible to LLM)

    Returns:
        Result dictionary
    """
    # Implementation
    result = orchestrator.some_operation(param)
    return {"success": True, "data": result}
```

**2. Add input validation:**

```python
from mcp_orchestrator.telemetry import validate_input

@mcp.tool()
async def new_tool(param: str) -> dict:
    """Tool description."""
    # Validate input
    if not param or len(param) > 1000:
        raise ValueError("param must be 1-1000 characters")

    # Implementation
    ...
```

**3. Integrate memory events:**

```python
from mcp_orchestrator.memory import emit_event, TraceContext

@mcp.tool()
async def new_tool(param: str) -> dict:
    """Tool description."""
    with TraceContext() as trace_id:
        emit_event(
            "mcp.tool.new_tool.started",
            trace_id=trace_id,
            status="pending",
            metadata={"param": param}
        )

        try:
            result = orchestrator.some_operation(param)

            emit_event(
                "mcp.tool.new_tool.completed",
                trace_id=trace_id,
                status="success",
                metadata={"result_size": len(result)}
            )

            return {"success": True, "data": result}

        except Exception as e:
            emit_event(
                "mcp.tool.new_tool.failed",
                trace_id=trace_id,
                status="failure",
                metadata={"error": str(e), "error_type": type(e).__name__}
            )
            raise
```

**4. Add tests:**

```python
# tests/integration/test_new_tool.py
import pytest
from mcp_orchestrator.mcp.server import create_server

@pytest.mark.asyncio
async def test_new_tool_success():
    server = create_server()
    result = await server.call_tool("new_tool", {"param": "value"})

    assert result["success"] is True
    assert "data" in result

@pytest.mark.asyncio
async def test_new_tool_validation():
    server = create_server()

    with pytest.raises(ValueError):
        await server.call_tool("new_tool", {"param": ""})  # Invalid
```

**5. Update documentation:**

- Add to [../../README.md](../../README.md) tool list
- Update [../../dev-docs/vision/MCP_SERVER_SPEC.md](../../dev-docs/vision/MCP_SERVER_SPEC.md)
- Update [../../AGENTS.md](../../AGENTS.md) if workflow changes

---

## Testing MCP Server

**Coverage Target:** ≥85% (integration tests required)

### Test Categories

1. **Tool Tests:** Each tool (happy path, error cases)
```python
@pytest.mark.asyncio
async def test_list_clients_returns_all():
    server = create_server()
    result = await server.call_tool("list_clients", {})

    assert "clients" in result
    assert result["count"] >= 2  # claude-desktop, cursor
```

2. **Resource Tests:** Each resource (valid output)
```python
@pytest.mark.asyncio
async def test_capabilities_server_resource():
    server = create_server()
    result = await server.get_resource("capabilities://server")

    assert result["name"] == "mcp-orchestration"
    assert "capabilities" in result
```

3. **Protocol Tests:** MCP compliance (handshake, error format)
```python
@pytest.mark.asyncio
async def test_mcp_handshake():
    server = create_server()
    capabilities = await server.get_capabilities()

    assert capabilities["protocol_version"] == "2024-11-05"
    assert "tools" in capabilities
```

4. **Integration Tests:** Full workflows (get_config → diff_config)
```python
@pytest.mark.asyncio
async def test_config_retrieval_and_diff_flow():
    server = create_server()

    # 1. Get config
    config = await server.call_tool("get_config", {
        "client_id": "claude-desktop",
        "profile_id": "default"
    })
    assert config["artifact_id"] is not None

    # 2. Diff against itself (should be up-to-date)
    diff = await server.call_tool("diff_config", {
        "client_id": "claude-desktop",
        "profile_id": "default",
        "local_payload": config["payload"]
    })
    assert diff["status"] == "up-to-date"
```

5. **Memory Tests:** Events emitted correctly
```python
@pytest.mark.asyncio
async def test_tool_emits_memory_events():
    from mcp_orchestrator.memory import query_events

    server = create_server()
    await server.call_tool("get_config", {
        "client_id": "claude-desktop",
        "profile_id": "default"
    })

    # Verify events emitted
    events = query_events(
        event_type="mcp.tool.get_config",
        since_hours=1
    )
    assert len(events) > 0
```

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Server started
emit_event("mcp.server_started", status="success",
           metadata={"protocol_version": "2024-11-05"})

# Tool called
emit_event("mcp.tool_called", status="pending",
           metadata={"tool": tool_name, "params": params})

# Tool completed
emit_event("mcp.tool_completed", status="success",
           metadata={"tool": tool_name, "duration_ms": duration})

# Tool failed
emit_event("mcp.tool_failed", status="failure",
           metadata={"tool": tool_name, "error": str(error)})

# Server stopped
emit_event("mcp.server_stopped", status="success",
           metadata={"uptime_seconds": uptime})
```

**Create knowledge notes for:**
- MCP protocol edge cases discovered
- Tool performance optimizations
- Error handling patterns

**Tag pattern:** `mcp`, `tools`, `[tool-name]`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../registry/AGENTS.md](../registry/AGENTS.md)** - Registry (list_clients, list_profiles)
- **[../storage/AGENTS.md](../storage/AGENTS.md)** - Storage (get_config)
- **[../diff/AGENTS.md](../diff/AGENTS.md)** - Diff engine (diff_config)
- **[../../dev-docs/vision/MCP_SERVER_SPEC.md](../../dev-docs/vision/MCP_SERVER_SPEC.md)** - MCP spec

---

## Common Errors & Solutions

### Error: "Server won't start"

**Cause:** Port already in use, permission denied

**Solution:**
```bash
# Check if another instance running
ps aux | grep mcp-orchestration

# Kill existing instance
pkill -f mcp-orchestration

# Restart
mcp-orchestration
```

### Error: "Tool not found"

**Cause:** Tool not registered with @mcp.tool() decorator

**Solution:**
```python
# Verify tool registration
from mcp_orchestrator.mcp.server import mcp

@mcp.tool()  # ← Must have decorator
async def your_tool():
    ...
```

### Error: "Invalid input schema"

**Cause:** Tool parameters don't match MCP schema

**Solution:**
```python
# Use type hints (required by MCP)
@mcp.tool()
async def your_tool(param: str) -> dict:  # ← Type hints required
    ...
```

### Error: "Signature verification failed" (in get_config)

**Cause:** Artifact tampered or keys mismatched

**Solution:**
```bash
# Regenerate keys and re-sign artifacts
mcp-orchestration init-configs --regenerate-keys
```

---

**End of MCP Server Implementation Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
