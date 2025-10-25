---
title: Wave 2.x Coordination Plan - HTTP Transport & Ecosystem Integration
version: 1.0.0
status: planning
created: 2025-10-24
last_updated: 2025-10-24
wave: 2.0-2.x
ecosystem_partner: mcp-gateway
---

# Wave 2.x Coordination Plan

**Goal:** Deliver HTTP/SSE transport for mcp-orchestration to enable Pattern N3b ecosystem integration with mcp-gateway and n8n workflows.

**Timeline:** Q1 2026 (January - February 2026)
**Coordination:** [MCP Gateway Ecosystem Coordination](ecosystem/MCP_GATEWAY_COORDINATION.md)

---

## Executive Summary

Wave 2.x represents mcp-orchestration's transition from **stdio-only** to **multi-transport** architecture, enabling:
- ✅ HTTP/SSE transport for web integration
- ✅ Pattern N3b (n8n multi-server MCP client)
- ✅ Universal Loadability Format adoption
- ✅ Enhanced API ergonomics
- ✅ Testing infrastructure for ecosystem partners

**Critical Dependency:** mcp-gateway v1.3.0 HTTP transport (Weeks 7-9, Q4 2025)

---

## Table of Contents

1. [Wave 2.0: HTTP Transport Foundation](#wave-20-http-transport-foundation)
2. [Wave 2.1: API Enhancements](#wave-21-api-enhancements)
3. [Wave 2.2: Ecosystem Integration](#wave-22-ecosystem-integration)
4. [Timeline](#timeline)
5. [Technical Specifications](#technical-specifications)
6. [Testing Strategy](#testing-strategy)
7. [Success Criteria](#success-criteria)
8. [Risks and Mitigations](#risks-and-mitigations)

---

## Wave 2.0: HTTP Transport Foundation

**Version:** v0.2.0
**Timeline:** January 2026 (4-5 weeks)
**Status:** 🔴 Planning

### Goals

1. **HTTP Streamable Transport**
   - Replace stdio-only with multi-transport architecture
   - Support both stdio (backward compat) and HTTP
   - Align with MCP specification (post-2024-11-05)
   - Coordinate endpoint structure with mcp-gateway

2. **Transport Abstraction Layer**
   - Clean separation: transport ↔ business logic
   - Pluggable transport system
   - Configuration-driven transport selection

3. **Authentication & Security**
   - Bearer token authentication (primary)
   - API key support (secondary)
   - Rate limiting and CORS
   - TLS/HTTPS ready

### Deliverables

#### 1. HTTP Server Implementation

**Framework:** FastAPI (aligns with mcp-gateway's FastMCP/FastAPI stack)

**Endpoint Structure** (aligned with mcp-gateway v1.3.0):

```python
# Core MCP endpoints
POST   /mcp/message           # JSON-RPC 2.0 messages
GET    /mcp/sse               # Server-Sent Events
POST   /mcp/tools/list        # List available tools
POST   /mcp/tools/call        # Execute tool

# Health & metadata
GET    /health                # Health check
GET    /mcp/info              # Server info and capabilities

# Optional: RESTful convenience endpoints
GET    /api/clients           # List clients (convenience)
GET    /api/servers           # List servers (convenience)
POST   /api/config/build      # Build config (convenience)
```

**Implementation:**

```python
# src/mcp_orchestrator/transports/http_server.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI(title="MCP Orchestration Server")

@app.post("/mcp/message")
async def mcp_message(request: Request):
    """
    Handle JSON-RPC 2.0 MCP messages over HTTP.

    Supports:
    - initialize
    - tools/list
    - tools/call
    - resources/list (future)
    - prompts/list (future)
    """
    body = await request.json()

    # Validate JSON-RPC 2.0
    if body.get("jsonrpc") != "2.0":
        raise HTTPException(400, "Invalid JSON-RPC version")

    # Route to handler
    method = body.get("method")
    params = body.get("params", {})
    id = body.get("id")

    result = await handle_mcp_method(method, params)

    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": id
    }

@app.get("/mcp/sse")
async def mcp_sse(request: Request):
    """
    Server-Sent Events endpoint for notifications.

    Streams:
    - Configuration updates
    - Registry changes
    - System events
    """
    async def event_generator():
        # Subscribe to event bus
        queue = asyncio.Queue()
        event_bus.subscribe(queue)

        try:
            while True:
                event = await queue.get()
                yield {
                    "event": event["type"],
                    "data": json.dumps(event["data"])
                }
        finally:
            event_bus.unsubscribe(queue)

    return EventSourceResponse(event_generator())

@app.get("/health")
async def health_check():
    """Health check for load balancers."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "transport": "http"
    }
```

**Configuration:**

```yaml
# config/http.yaml

server:
  host: 0.0.0.0
  port: 8080
  workers: 4

transport:
  type: http  # or "stdio" for backward compat

auth:
  type: bearer  # or "api_key" or "none" (dev only)
  bearer_token_env: MCP_ORCH_BEARER_TOKEN

cors:
  enabled: true
  origins:
    - http://localhost:5678  # n8n
    - http://localhost:3000  # future UI

rate_limiting:
  enabled: true
  requests_per_minute: 60
```

#### 2. Transport Abstraction

**Interface:**

```python
# src/mcp_orchestrator/transports/base.py

from abc import ABC, abstractmethod
from typing import AsyncIterator

class Transport(ABC):
    """Base transport interface."""

    @abstractmethod
    async def start(self):
        """Start transport server."""
        pass

    @abstractmethod
    async def stop(self):
        """Stop transport server."""
        pass

    @abstractmethod
    async def receive_message(self) -> dict:
        """Receive MCP message."""
        pass

    @abstractmethod
    async def send_message(self, message: dict):
        """Send MCP message."""
        pass

    @abstractmethod
    async def send_notification(self, event: dict):
        """Send notification (SSE/callback)."""
        pass
```

**Implementations:**

```python
# src/mcp_orchestrator/transports/stdio_transport.py
class StdioTransport(Transport):
    """Existing stdio implementation."""
    pass

# src/mcp_orchestrator/transports/http_transport.py
class HttpTransport(Transport):
    """HTTP/SSE implementation."""
    pass
```

#### 3. Authentication System

**Bearer Token (Primary):**

```python
# src/mcp_orchestrator/auth/bearer.py

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """Verify Bearer token from Authorization header."""

    expected_token = os.getenv("MCP_ORCH_BEARER_TOKEN")

    if not expected_token:
        # Dev mode: no auth required
        return "dev-user"

    if credentials.credentials != expected_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    return "authenticated-user"

# Usage in endpoint:
@app.post("/mcp/tools/call")
async def call_tool(
    request: Request,
    user: str = Depends(verify_bearer_token)
):
    # user is authenticated
    ...
```

**API Key (Secondary):**

```python
# src/mcp_orchestrator/auth/api_key.py

from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """Verify API key from X-API-Key header."""

    expected_key = os.getenv("MCP_ORCH_API_KEY")

    if x_api_key != expected_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return "api-key-user"
```

#### 4. Migration Guide

**For Users:**

```markdown
# Migrating from stdio to HTTP

## Step 1: Update installation

```bash
pip install --upgrade mcp-orchestration  # v0.2.0+
```

## Step 2: Configure HTTP transport

```yaml
# config/http.yaml
server:
  port: 8080
transport:
  type: http
auth:
  type: bearer
  bearer_token_env: MCP_ORCH_BEARER_TOKEN
```

## Step 3: Start HTTP server

```bash
export MCP_ORCH_BEARER_TOKEN="your-secret-token"
mcp-orchestration serve --config config/http.yaml
```

## Step 4: Update client configuration

**Before (stdio):**
```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

**After (HTTP via mcp-remote):**
```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/mcp-remote",
        "stdio",
        "http://localhost:8080/mcp"
      ],
      "env": {
        "MCP_ORCH_BEARER_TOKEN": "${MCP_ORCH_BEARER_TOKEN}"
      }
    }
  }
}
```

**Or (direct HTTP in compatible clients):**
```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "url": "http://localhost:8080/mcp",
      "transport": "http",
      "auth": {
        "type": "bearer",
        "token": "${MCP_ORCH_BEARER_TOKEN}"
      }
    }
  }
}
```
```

### Success Criteria - Wave 2.0

- ✅ HTTP server starts on configurable port
- ✅ All existing tools accessible via HTTP
- ✅ stdio transport still works (backward compat)
- ✅ Bearer token authentication working
- ✅ CORS configured for n8n/UI origins
- ✅ Health check endpoint operational
- ✅ SSE notifications functional
- ✅ Migration guide complete
- ✅ Performance: p95 latency <500ms (vs stdio <300ms)
- ✅ Load test: 100 concurrent requests sustained

---

## Wave 2.1: API Enhancements

**Version:** v0.2.1
**Timeline:** February 2026 (2 weeks)
**Status:** 🔴 Planning

### Goals

1. **Add validate_config Tool**
   - Pre-publish configuration validation
   - Improves n8n workflow DX
   - Requested by mcp-gateway team

2. **Universal Loadability Format Adoption**
   - Implement `mcp-server.json` generation
   - Align with ecosystem standards
   - Enable auto-discovery

3. **Enhanced Error Messages**
   - Structured error responses
   - Error codes for automation
   - Retry guidance

### Deliverables

#### 1. validate_config Tool

**Purpose:** Check configuration validity without publishing

**Implementation:**

```python
# src/mcp_orchestrator/mcp/tools/validate_config.py

@mcp.tool()
async def validate_config(
    client_id: str,
    profile_id: str = "default",
    use_draft: bool = True
) -> dict:
    """
    Validate configuration without publishing.

    Performs checks:
    - All servers exist in registry
    - Required parameters provided
    - No conflicting server names
    - Env vars properly formatted
    - Transport compatibility
    - Signature validity (if artifact)

    Args:
        client_id: Client family identifier
        profile_id: Profile identifier (default: "default")
        use_draft: Validate draft vs. latest artifact

    Returns:
        {
            "valid": bool,
            "errors": [
                {
                    "code": "MISSING_SERVER",
                    "message": "Server 'custom-api' not found in registry",
                    "server_name": "custom-api",
                    "severity": "error"
                }
            ],
            "warnings": [
                {
                    "code": "DEPRECATED_PARAM",
                    "message": "Parameter 'api_url' is deprecated, use 'url'",
                    "server_name": "github-mcp",
                    "severity": "warning"
                }
            ],
            "stats": {
                "total_servers": 5,
                "valid_servers": 4,
                "error_count": 1,
                "warning_count": 1
            }
        }
    """

    # Load config (draft or artifact)
    if use_draft:
        config = draft_manager.get_draft(client_id, profile_id)
    else:
        artifact = artifact_store.get_latest(client_id, profile_id)
        config = artifact["payload"]

    errors = []
    warnings = []

    # Validate each server
    for server_name, server_config in config.get("mcpServers", {}).items():
        # Check server exists in registry
        if not registry.has_server(server_config):
            errors.append({
                "code": "MISSING_SERVER",
                "message": f"Server '{server_name}' not found in registry",
                "server_name": server_name,
                "severity": "error"
            })
            continue

        server_def = registry.get_server(server_config)

        # Check required parameters
        for param in server_def.required_params:
            if param.name not in server_config.get("env", {}):
                errors.append({
                    "code": "MISSING_PARAM",
                    "message": f"Required parameter '{param.name}' missing",
                    "server_name": server_name,
                    "param_name": param.name,
                    "severity": "error"
                })

        # Check deprecated parameters
        for param_name in server_config.get("env", {}).keys():
            if param_name in server_def.deprecated_params:
                warnings.append({
                    "code": "DEPRECATED_PARAM",
                    "message": f"Parameter '{param_name}' is deprecated",
                    "server_name": server_name,
                    "param_name": param_name,
                    "severity": "warning",
                    "suggestion": server_def.deprecated_params[param_name].replacement
                })

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_servers": len(config.get("mcpServers", {})),
            "valid_servers": len(config.get("mcpServers", {})) - len(set(e["server_name"] for e in errors)),
            "error_count": len(errors),
            "warning_count": len(warnings)
        }
    }
```

**Usage in n8n workflow:**

```
n8n: MCP Client Node → mcp-orchestration
  Tool: validate_config
  Params:
    client_id: "claude-desktop"
    profile_id: "production"
    use_draft: true

Response:
  {
    "valid": false,
    "errors": [
      {
        "code": "MISSING_PARAM",
        "message": "Required parameter 'GITHUB_TOKEN' missing",
        "server_name": "github-mcp"
      }
    ]
  }

n8n: IF node
  Condition: {{$json.valid}} == false
  True → Send Slack alert with errors
  False → Continue to publish_config
```

#### 2. Universal Loadability Format

**File:** `mcp-server.json` (generated)

**Implementation:**

```python
# src/mcp_orchestrator/loadability/generator.py

def generate_loadability_manifest() -> dict:
    """
    Generate Universal Loadability Format manifest.

    Spec: mcp-gateway v1.2.0
    """

    # Introspect tools
    tools = mcp.list_tools()

    manifest = {
        "name": "mcp-orchestration",
        "version": get_version(),
        "description": "MCP client configuration and server management",
        "author": "liminalcommons",
        "license": "MIT",
        "mcp": {
            "protocol_version": "2024-11-05",
            "transport": {
                "stdio": {
                    "command": "uvx",
                    "args": ["mcp-orchestration"]
                },
                "http": {
                    "url": os.getenv("MCP_ORCH_HTTP_URL", "http://localhost:8080"),
                    "auth": "bearer",
                    "sse_endpoint": "/mcp/sse"
                }
            },
            "capabilities": {
                "tools": True,
                "resources": False,
                "prompts": False
            },
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema
                }
                for tool in tools
            ]
        },
        "tags": ["configuration", "orchestration", "mcp-server-registry"],
        "homepage": "https://github.com/liminalcommons/mcp-orchestration",
        "documentation": "https://mcp-orchestration.dev/docs"
    }

    return manifest

# CLI command
@cli.command()
def generate_loadability():
    """Generate mcp-server.json manifest."""
    manifest = generate_loadability_manifest()

    with open("mcp-server.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("✅ Generated mcp-server.json")
```

**Result:**

```json
{
  "name": "mcp-orchestration",
  "version": "0.2.1",
  "description": "MCP client configuration and server management",
  "author": "liminalcommons",
  "license": "MIT",
  "mcp": {
    "protocol_version": "2024-11-05",
    "transport": {
      "stdio": {
        "command": "uvx",
        "args": ["mcp-orchestration"]
      },
      "http": {
        "url": "http://localhost:8080",
        "auth": "bearer",
        "sse_endpoint": "/mcp/sse"
      }
    },
    "capabilities": {
      "tools": true,
      "resources": false,
      "prompts": false
    },
    "tools": [
      {
        "name": "list_available_servers",
        "description": "List all MCP servers in registry",
        "input_schema": {
          "type": "object",
          "properties": {
            "transport_filter": {
              "type": "string",
              "enum": ["stdio", "http", "sse"]
            },
            "tag_filter": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        }
      },
      {
        "name": "validate_config",
        "description": "Validate configuration without publishing",
        "input_schema": {
          "type": "object",
          "properties": {
            "client_id": {"type": "string"},
            "profile_id": {"type": "string"},
            "use_draft": {"type": "boolean"}
          },
          "required": ["client_id"]
        }
      }
    ]
  },
  "tags": ["configuration", "orchestration", "mcp-server-registry"]
}
```

### Success Criteria - Wave 2.1

- ✅ `validate_config` tool implemented and tested
- ✅ Error codes standardized
- ✅ `mcp-server.json` generated correctly
- ✅ Universal Loadability Format adopted
- ✅ mcp-gateway can auto-discover via loadability file
- ✅ Documentation updated

---

## Wave 2.2: Ecosystem Integration

**Version:** v0.2.2
**Timeline:** February-March 2026 (2-3 weeks)
**Status:** 🔴 Planning

### Goals

1. **mcp-gateway Integration Testing**
   - Cross-system HTTP testing
   - Pattern N3b validation
   - Joint example workflows

2. **n8n Workflow Examples**
   - "Onboard Engineer" workflow
   - "Environment Config" workflow
   - "Health Monitor" workflow

3. **Performance Optimization**
   - HTTP endpoint optimization
   - Caching for registry queries
   - Connection pooling

### Deliverables

#### 1. Integration Testing with mcp-gateway

**Test Scenarios:**

```python
# tests/integration/test_mcp_gateway_integration.py

import pytest
import httpx
from n8n_client import N8nClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_pattern_n3b_dual_server_workflow():
    """
    Test Pattern N3b: n8n workflow consuming both systems.

    Workflow:
    1. Call mcp-orchestration:list_available_servers
    2. Call mcp-gateway:chora:assemble_artifact
    3. Verify both systems respond
    """

    # Start both servers
    orch_server = start_mcp_orchestration(port=8080)
    gateway_server = start_mcp_gateway(port=8678)

    async with httpx.AsyncClient() as client:
        # Test mcp-orchestration
        orch_response = await client.post(
            "http://localhost:8080/mcp/message",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "list_available_servers"
                },
                "id": 1
            },
            headers={"Authorization": f"Bearer {ORCH_TOKEN}"}
        )

        assert orch_response.status_code == 200
        orch_result = orch_response.json()
        assert "result" in orch_result
        assert len(orch_result["result"]["servers"]) > 0

        # Test mcp-gateway
        gateway_response = await client.post(
            "http://localhost:8678/mcp/message",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "chora:list_generators"
                },
                "id": 2
            },
            headers={"Authorization": f"Bearer {GATEWAY_TOKEN}"}
        )

        assert gateway_response.status_code == 200
        gateway_result = gateway_response.json()
        assert "result" in gateway_result

    # Test via n8n
    n8n = N8nClient("http://localhost:5678")

    workflow_result = await n8n.execute_workflow("test-pattern-n3b", {
        "orch_url": "http://localhost:8080/mcp",
        "gateway_url": "http://localhost:8678/mcp"
    })

    assert workflow_result["success"] == True
    assert "servers" in workflow_result["data"]
```

#### 2. Example n8n Workflows

**Workflow 1: Onboard Engineer**

```json
{
  "name": "Onboard Engineer MCP Environment",
  "nodes": [
    {
      "name": "Get Employee Data",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://hr-api.company.com/employees/{{$json.employee_id}}",
        "method": "GET"
      }
    },
    {
      "name": "List Available Servers",
      "type": "@chora/mcp-client",
      "parameters": {
        "serverUrl": "http://localhost:8080/mcp",
        "operation": "callTool",
        "toolName": "list_available_servers",
        "toolParams": "{}"
      }
    },
    {
      "name": "Filter by Role",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "code": "const role = $input.item.json.role;\nconst servers = $('List Available Servers').item.json.servers;\n\nconst roleServers = {\n  'frontend': ['github-mcp', 'figma-mcp', 'linear-mcp'],\n  'backend': ['github-mcp', 'postgres-mcp', 'redis-mcp'],\n  'devops': ['github-mcp', 'terraform-mcp', 'kubernetes-mcp']\n};\n\nreturn servers.filter(s => roleServers[role].includes(s.server_id));"
      }
    },
    {
      "name": "Add Servers Loop",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": {}
    },
    {
      "name": "Add Server to Config",
      "type": "@chora/mcp-client",
      "parameters": {
        "serverUrl": "http://localhost:8080/mcp",
        "operation": "callTool",
        "toolName": "add_server_to_config",
        "toolParams": "{{JSON.stringify({server_id: $json.server_id})}}"
      }
    },
    {
      "name": "Publish Config",
      "type": "@chora/mcp-client",
      "parameters": {
        "serverUrl": "http://localhost:8080/mcp",
        "operation": "callTool",
        "toolName": "publish_config",
        "toolParams": "{\"changelog\": \"Onboarded {{$('Get Employee Data').item.json.name}}\"}"
      }
    },
    {
      "name": "Create Sandbox Repo",
      "type": "@chora/mcp-client",
      "parameters": {
        "serverUrl": "http://localhost:8678/mcp",
        "operation": "callTool",
        "toolName": "github:create_repo",
        "toolParams": "{{JSON.stringify({name: $('Get Employee Data').item.json.username + '-sandbox'})}}"
      }
    },
    {
      "name": "Notify Slack",
      "type": "@chora/mcp-client",
      "parameters": {
        "serverUrl": "http://localhost:8678/mcp",
        "operation": "callTool",
        "toolName": "slack:send_message",
        "toolParams": "{{JSON.stringify({channel: '#onboarding', text: 'Onboarded ' + $('Get Employee Data').item.json.name})}}"
      }
    }
  ],
  "connections": {
    "Get Employee Data": {"main": [[{"node": "List Available Servers"}]]},
    "List Available Servers": {"main": [[{"node": "Filter by Role"}]]},
    "Filter by Role": {"main": [[{"node": "Add Servers Loop"}]]},
    "Add Servers Loop": {"main": [[{"node": "Add Server to Config"}]]},
    "Add Server to Config": {"main": [[{"node": "Publish Config"}]]},
    "Publish Config": {"main": [[{"node": "Create Sandbox Repo"}]]},
    "Create Sandbox Repo": {"main": [[{"node": "Notify Slack"}]]}
  }
}
```

**Workflow 2: Validate Before Deploy**

**Workflow 3: Health Monitor**

(Similar detailed workflow definitions)

#### 3. Performance Optimization

**Caching Layer:**

```python
# src/mcp_orchestrator/cache/registry_cache.py

from functools import lru_cache
from cachetools import TTLCache
import asyncio

# In-memory cache with TTL
registry_cache = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL

@lru_cache(maxsize=100)
def get_server_definition_cached(server_id: str):
    """Cache server definitions (rarely change)."""
    return registry.get_server(server_id)

async def list_available_servers_cached(transport_filter=None):
    """Cache registry listing for 5 minutes."""
    cache_key = f"list_servers:{transport_filter}"

    if cache_key in registry_cache:
        return registry_cache[cache_key]

    result = await registry.list_servers(transport_filter)
    registry_cache[cache_key] = result

    return result
```

**Connection Pooling:**

```python
# src/mcp_orchestrator/http/client_pool.py

import httpx

# Reusable HTTP client pool
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0),
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )
)
```

### Success Criteria - Wave 2.2

- ✅ Integration tests passing with mcp-gateway
- ✅ 3+ example n8n workflows published
- ✅ HTTP endpoint p95 latency <300ms (optimized from <500ms)
- ✅ Cache hit rate >80% for registry queries
- ✅ Pattern N3b validated end-to-end
- ✅ Joint documentation complete

---

## Timeline

### Detailed Schedule

**Week 1-2 (Late Dec 2025 / Early Jan 2026):**
- Complete Wave 1.x remaining items
- Review mcp-gateway Universal Loadability spec (v1.2.0)
- Finalize Wave 2.0 scope and design

**Week 3-6 (Mid-Jan to Early Feb 2026):**
- **Wave 2.0 Implementation**
- HTTP server implementation
- Transport abstraction
- Authentication system
- Migration guide
- Testing

**Week 7-8 (Mid Feb 2026):**
- **Wave 2.1 Implementation**
- Add `validate_config` tool
- Universal Loadability adoption
- Enhanced error messages

**Week 9-11 (Late Feb to Early Mar 2026):**
- **Wave 2.2 Implementation**
- Integration testing with mcp-gateway
- Example n8n workflows
- Performance optimization
- Joint documentation

**Week 12 (Mid Mar 2026):**
- **Wave 2.x Release**
- Final testing
- Documentation review
- Community announcement
- Pattern N3b coordination begins (Q2 2026)

### Coordination Points with mcp-gateway

| Week | mcp-orchestration | mcp-gateway | Joint Activity |
|------|-------------------|-------------|----------------|
| Week 6 | Review Loadability spec | v1.2.0 release (Loadability) | Specification alignment |
| Week 9 | HTTP implementation WIP | v1.3.0 release (HTTP) | Endpoint structure sync |
| Week 11 | Integration testing | Provide test server | Cross-system validation |
| Week 12 | Wave 2.x release | Begin Pattern N3b work | Joint documentation |

---

## Technical Specifications

### HTTP Endpoint Alignment

**Coordination:** Align with mcp-gateway v1.3.0 endpoint structure

| Endpoint | Method | Purpose | mcp-orch | mcp-gateway |
|----------|--------|---------|----------|-------------|
| `/mcp/message` | POST | JSON-RPC messages | ✅ | ✅ |
| `/mcp/sse` | GET | Server-Sent Events | ✅ | ✅ |
| `/mcp/tools/list` | POST | List tools | ✅ | ✅ |
| `/mcp/tools/call` | POST | Execute tool | ✅ | ✅ |
| `/health` | GET | Health check | ✅ | ✅ |
| `/mcp/info` | GET | Server info | ✅ | ✅ |

**Authentication Alignment:**

- **Primary:** Bearer tokens (`Authorization: Bearer <token>`)
- **Secondary:** API keys (`X-API-Key: <key>`)
- **Dev Mode:** No auth (configurable, localhost only)

**Response Format Alignment:**

```typescript
// Success (JSON-RPC 2.0)
{
  "jsonrpc": "2.0",
  "result": { /* tool result */ },
  "id": 1
}

// Error (JSON-RPC 2.0)
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,  // JSON-RPC error code
    "message": "Invalid request",
    "data": {
      "mcp_error_code": "VALIDATION_ERROR",  // Our error code
      "details": { /* additional context */ }
    }
  },
  "id": 1
}
```

### Dependencies

**New Dependencies:**

```toml
[tool.poetry.dependencies]
# HTTP server
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sse-starlette = "^1.6.5"

# HTTP client (for testing)
httpx = "^0.25.0"

# Caching
cachetools = "^5.3.0"

# CORS
fastapi-cors = "^0.0.6"
```

---

## Testing Strategy

### Test Phases

#### Phase 1: Unit Testing (Week 3-4)

**Focus:** HTTP transport implementation

```python
# tests/unit/test_http_transport.py

@pytest.mark.asyncio
async def test_http_message_endpoint():
    """Test /mcp/message endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/mcp/message",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert "result" in data

@pytest.mark.asyncio
async def test_bearer_auth():
    """Test Bearer token authentication."""
    # Without token
    response = await client.post("/mcp/message", json={...})
    assert response.status_code == 401

    # With valid token
    response = await client.post(
        "/mcp/message",
        json={...},
        headers={"Authorization": "Bearer valid-token"}
    )
    assert response.status_code == 200
```

**Coverage Target:** ≥85%

#### Phase 2: Integration Testing (Week 5-6)

**Focus:** stdio ↔ HTTP compatibility

```python
# tests/integration/test_transport_parity.py

@pytest.mark.integration
async def test_stdio_http_parity():
    """Verify stdio and HTTP transports return same results."""

    # Start HTTP server
    http_server = start_http_server(port=8080)

    # Call via stdio
    stdio_result = await call_via_stdio("list_available_servers", {})

    # Call via HTTP
    http_result = await call_via_http(
        "http://localhost:8080/mcp/tools/call",
        "list_available_servers",
        {}
    )

    # Results should match
    assert stdio_result == http_result
```

**Coverage Target:** All tools tested via both transports

#### Phase 3: Cross-System Testing (Week 11)

**Focus:** Integration with mcp-gateway

**Coordination:** Joint testing with mcp-gateway team

```python
# tests/integration/test_mcp_gateway_integration.py

@pytest.mark.integration
@pytest.mark.requires_mcp_gateway
async def test_n8n_dual_server_workflow():
    """
    Test n8n workflow consuming both systems.

    Prerequisites:
    - mcp-gateway running on localhost:8678
    - mcp-orchestration running on localhost:8080
    - n8n running on localhost:5678
    """

    # Deploy test workflow to n8n
    workflow_id = await n8n_client.create_workflow(
        pattern_n3b_test_workflow
    )

    # Execute workflow
    execution = await n8n_client.execute_workflow(workflow_id, {
        "test_param": "value"
    })

    # Verify success
    assert execution["status"] == "success"
    assert execution["data"]["mcp_orch_called"] == True
    assert execution["data"]["mcp_gateway_called"] == True

    # Verify timing
    assert execution["duration_ms"] < 5000  # <5s end-to-end
```

**Test Environment:**

```bash
# docker-compose.test.yml

version: "3.8"
services:
  mcp-orchestration:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MCP_ORCH_BEARER_TOKEN=test-token

  mcp-gateway:
    image: mcp-gateway:latest
    ports:
      - "8678:8678"
    environment:
      - MCP_GATEWAY_BEARER_TOKEN=test-token

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=false
```

#### Phase 4: Performance Testing (Week 11)

**Load Tests:**

```python
# tests/performance/test_http_load.py

import locust
from locust import HttpUser, task, between

class McpOrchestrationUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_servers(self):
        """Most common operation."""
        self.client.post(
            "/mcp/message",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "list_available_servers"
                },
                "id": 1
            },
            headers={"Authorization": "Bearer test-token"}
        )

    @task(1)
    def get_config(self):
        """Less common operation."""
        self.client.post(
            "/mcp/message",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "get_config",
                    "arguments": {
                        "client_id": "claude-desktop"
                    }
                },
                "id": 2
            },
            headers={"Authorization": "Bearer test-token"}
        )

# Run: locust -f tests/performance/test_http_load.py --host=http://localhost:8080
```

**Performance Targets:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| p50 latency | <200ms | Locust |
| p95 latency | <500ms | Locust |
| p99 latency | <1000ms | Locust |
| Throughput | >100 req/s | Locust |
| Concurrent users | 100 sustained | Locust |
| Error rate | <1% | Locust |
| Memory usage | <500MB | Docker stats |
| CPU usage | <50% (4 cores) | Docker stats |

---

## Success Criteria

### Wave 2.0 (HTTP Transport)

**Functional:**
- ✅ All 12 existing tools accessible via HTTP
- ✅ stdio transport still works (backward compatibility)
- ✅ Bearer token authentication functional
- ✅ SSE notifications working
- ✅ Health check endpoint operational
- ✅ CORS configured correctly
- ✅ Migration guide complete

**Performance:**
- ✅ p95 latency <500ms (HTTP)
- ✅ 100 concurrent users sustained
- ✅ Memory usage <500MB under load
- ✅ Error rate <1%

**Quality:**
- ✅ Unit test coverage ≥85%
- ✅ Integration tests passing
- ✅ No regressions in stdio mode
- ✅ Documentation complete

### Wave 2.1 (API Enhancements)

**Functional:**
- ✅ `validate_config` tool implemented
- ✅ Error codes standardized
- ✅ `mcp-server.json` generated
- ✅ Universal Loadability Format adopted

**Quality:**
- ✅ Test coverage ≥85%
- ✅ mcp-gateway can auto-discover
- ✅ Documentation updated

### Wave 2.2 (Ecosystem Integration)

**Functional:**
- ✅ Integration tests with mcp-gateway passing
- ✅ 3+ example n8n workflows published
- ✅ Performance optimizations deployed
- ✅ Pattern N3b validated

**Performance:**
- ✅ p95 latency <300ms (optimized)
- ✅ Cache hit rate >80%

**Ecosystem:**
- ✅ Joint documentation with mcp-gateway
- ✅ Pattern N3b coordination active
- ✅ Community announcement sent

---

## Risks and Mitigations

### Risk 1: Timeline Slip

**Risk:** Wave 2.0 implementation takes longer than 4-5 weeks

**Probability:** Medium (40%)
**Impact:** High - Delays Pattern N3b launch

**Mitigation:**
- Start scoping immediately (this week)
- Weekly progress check-ins
- 2-week buffer built into Q1 2026 timeline
- Phased delivery (Wave 2.0 → 2.1 → 2.2)
- Early warning if >1 week behind

**Fallback:**
- Reduce Wave 2.1/2.2 scope
- Delay Universal Loadability to Wave 2.3
- Focus on core HTTP transport first

### Risk 2: mcp-gateway Incompatibility

**Risk:** Endpoint structure or auth doesn't align with mcp-gateway v1.3.0

**Probability:** Low (15%)
**Impact:** Medium - Requires rework

**Mitigation:**
- Review mcp-gateway v1.3.0 spec early (Week 9)
- Async communication with mcp-gateway team
- Joint testing session before release
- Endpoint structure alignment documented

**Fallback:**
- Adapter layer for compatibility
- Document differences clearly

### Risk 3: Performance Degradation

**Risk:** HTTP transport slower than stdio

**Probability:** Medium (30%)
**Impact:** Medium - Poor user experience

**Mitigation:**
- Performance testing from Week 4
- Caching layer for hot paths
- Connection pooling
- Profiling and optimization

**Fallback:**
- Keep stdio as recommended for local use
- HTTP for n8n/web integration only

### Risk 4: n8n Custom Node Delay

**Risk:** `@chora/mcp-client` node not ready for Wave 2.2

**Probability:** Low (20%)
**Impact:** Medium - Can't demonstrate Pattern N3b

**Mitigation:**
- Use HTTP Request nodes as backup
- Early coordination with mcp-gateway team
- Example workflows work without custom node

**Fallback:**
- Manual HTTP Request node workflows
- Custom node in Q2 2026 instead

---

## Next Actions

### This Week (Week 1)

1. ✅ Finalize this plan document
2. ✅ Create Universal Loadability review template
3. ✅ Update WAVE_1X_PLAN.md with Wave 2.x section
4. 📋 Begin Wave 2.0 scoping and design
5. 📋 Set up development environment for HTTP testing

### Week 2-3

1. 📋 Review mcp-gateway Universal Loadability spec (when available)
2. 📋 Start Wave 2.0 implementation (HTTP server)
3. 📋 Set up testing infrastructure

### Week 6

1. 📋 Complete Wave 2.0 core implementation
2. 📋 Begin integration testing

### Week 12

1. 📋 Wave 2.x release
2. 📋 Joint announcement with mcp-gateway
3. 📋 Begin Pattern N3b coordination (Q2 2026)

---

**Maintained By:** mcp-orchestration team
**Review Cadence:** Weekly (during implementation)
**Last Updated:** 2025-10-24
**Next Review:** After mcp-gateway v1.2.0 spec review
