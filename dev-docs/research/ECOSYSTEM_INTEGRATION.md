---
title: MCP-Orchestration Ecosystem Integration Guide
status: active
version: 1.1.0
last_updated: 2025-10-24
audience: peer repositories and ecosystem developers
related_research: MCP-n8n to MCP-Gateway Evolution.md
changelog: v1.1.0 - Added Pattern 5 (N3b) for mcp-gateway collaboration
---

# MCP-Orchestration Ecosystem Integration Guide

This document helps peer repositories in the Chora ecosystem understand **mcp-orchestration**'s role, capabilities, and integration patterns. It addresses how mcp-orchestration fits into the broader MCP ecosystem evolution from specialized tools to general-purpose orchestration.

**Context:** This document references the [MCP-n8n to MCP-Gateway Evolution](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md) research for architectural patterns and ecosystem alignment described in [solution-neutral-intent.md](../../dev-docs/vision/ecosystem-intent.md).

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [What is mcp-orchestration?](#what-is-mcp-orchestration)
3. [Integration Patterns](#integration-patterns)
4. [Capability Manifest](#capability-manifest)
5. [Architecture Patterns](#architecture-patterns)
6. [Decision Framework](#decision-framework)
7. [Implementation Examples](#implementation-examples)
8. [Migration Paths](#migration-paths)
9. [References](#references)

---

## Executive Summary

**mcp-orchestration** is a Model Context Protocol (MCP) server that provides:

- **Centralized configuration management** for MCP clients (Claude Desktop, Cursor, etc.)
- **Server registry** with 15+ MCP servers (filesystem, github, brave-search, etc.)
- **Configuration building tools** with draft workflow and cryptographic signing
- **Transport abstraction** - automatic mcp-remote wrapping for HTTP/SSE servers
- **Diff detection** - intelligent comparison and update recommendations

### Key Capabilities

| Capability ID | Description | Wave | Status |
|---------------|-------------|------|--------|
| `mcp.orchestration.client.list` | List supported MCP clients | 1.0 | ✅ Stable |
| `mcp.orchestration.config.get` | Retrieve signed configs | 1.0 | ✅ Stable |
| `mcp.orchestration.config.diff` | Compare configs | 1.0 | ✅ Stable |
| `mcp.orchestration.registry.list` | Browse MCP servers | 1.1 | ✅ Stable |
| `mcp.orchestration.config.build` | Build draft configs | 1.2 | ✅ Stable |
| `mcp.orchestration.config.publish` | Sign and publish configs | 1.3 | ✅ Stable |

### When to Integrate

✅ **USE mcp-orchestration if you need:**
- Centralized MCP client configuration management
- Cryptographically signed, content-addressable configs
- Discovery and registration of MCP servers
- Automated diff detection and update workflows
- Multi-client, multi-profile configuration support

❌ **DO NOT use mcp-orchestration if you need:**
- Dynamic MCP server aggregation/gateway (see: mcp-gateway pattern below)
- Real-time protocol routing (Pattern N4 - 45% feasibility)
- Runtime service orchestration (different use case)

---

## What is mcp-orchestration?

### Purpose

**mcp-orchestration** solves the **MCP configuration management problem**: as users adopt multiple MCP servers across multiple clients, managing configurations becomes complex, error-prone, and lacks version control.

### Core Architecture

```
┌─────────────────────────────────────────────────┐
│           MCP Client (Claude Desktop)           │
│  ┌───────────────────────────────────────────┐  │
│  │  mcp-orchestration (MCP Server)           │  │
│  │  ├── list_clients                         │  │
│  │  ├── list_available_servers               │  │
│  │  ├── add_server_to_config                 │  │
│  │  ├── publish_config                       │  │
│  │  └── get_config                           │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│     Content-Addressable Storage                 │
│  ~/.mcp-orchestration/                          │
│  ├── keys/           # Ed25519 signing keys     │
│  ├── artifacts/      # Signed configs (SHA-256) │
│  └── registry/       # Server definitions       │
└─────────────────────────────────────────────────┘
```

### Technology Stack

- **Language:** Python 3.10+
- **MCP SDK:** FastMCP (Python)
- **Transport:** stdio (primary), HTTP (planned Wave 2.x)
- **Crypto:** Ed25519 signatures via cryptography library
- **Storage:** File-based content-addressable (CAS) with SHA-256
- **Distribution:** PyPI package (`mcp-orchestration`)

---

## Integration Patterns

Based on the [MCP-n8n to MCP-Gateway Evolution](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md) research, there are **four primary integration patterns** for mcp-orchestration in the ecosystem.

### Pattern 1: Client Configuration Manager (RECOMMENDED - Current Implementation)

**Use Case:** Your application is an MCP client (like Claude Desktop) that needs configuration management.

**Architecture:**
```
Your MCP Client (e.g., Cursor IDE)
    ↓
mcp-orchestration (stdio MCP server)
    ↓
Local configuration storage
```

**Integration Steps:**

1. **Add to client config** (e.g., Claude Desktop):
   ```json
   {
     "mcpServers": {
       "mcp-orchestration": {
         "command": "mcp-orchestration"
       }
     }
   }
   ```

2. **Use MCP tools** in your client:
   ```typescript
   // List available servers
   await client.call_tool("list_available_servers")

   // Add server to config
   await client.call_tool("add_server_to_config", {
     server_id: "filesystem",
     params: {path: "/Users/me/Documents"}
   })

   // Publish signed config
   await client.call_tool("publish_config", {
     changelog: "Added filesystem server"
   })
   ```

**Capability Consumed:** `mcp.orchestration.config.*`, `mcp.orchestration.registry.*`

**Status:** ✅ Stable (Waves 1.0-1.3)

---

### Pattern 2: Frontend Configuration Builder

**Use Case:** You're building a web UI or desktop app that helps users configure MCP clients.

**Architecture:**
```
Your Frontend (React/Electron/etc.)
    ↓
mcp-orchestration HTTP API (future)
    ↓
Configuration storage + signing
```

**Current Workaround (Wave 1.x):**
Since HTTP transport is not yet available, use **subprocess invocation**:

```typescript
// TypeScript/Node.js example
import { spawn } from 'child_process';

async function listServers() {
  const proc = spawn('python3', [
    '-m', 'mcp_orchestrator.mcp.server'
  ], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // Send MCP JSON-RPC request via stdio
  const request = {
    jsonrpc: "2.0",
    method: "tools/call",
    params: {
      name: "list_available_servers"
    },
    id: 1
  };

  proc.stdin.write(JSON.stringify(request) + '\n');

  // Parse response...
}
```

**Future (Wave 2.x - Planned):**
```typescript
// HTTP transport with mcp-remote
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

const client = new Client({
  name: "config-builder-ui",
  version: "1.0.0"
}, {
  capabilities: {}
});

await client.connect("http://localhost:8080/mcp");
const servers = await client.listTools();
```

**Capability Provided:** Your app becomes a configuration UI for MCP ecosystem

**Status:** ⚠️ Experimental (stdio workaround), 📋 Planned (HTTP transport in Wave 2.x)

---

### Pattern 3: n8n Integration as MCP Server

**Use Case:** You want n8n workflows to be accessible as MCP tools.

**Architecture:**
```
MCP Client (Claude Desktop)
    ↓
mcp-server-n8n (standalone MCP server)
    ↓
n8n Instance (workflows)
```

**NOT THIS:**
```
❌ mcp-orchestration
    ↓
   n8n as gateway (Pattern N4 - 45% feasibility)
```

**Recommended Approach:**

Use **mcp-server-n8n** as a standalone MCP server (to be extracted from mcp-n8n, per [migration plan](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md#6-repository-migration-plan)):

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "mcp-server-n8n"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "${N8N_API_KEY}"
      }
    }
  }
}
```

Then **register with mcp-orchestration**:

```python
# In mcp-orchestration server registry
ServerDefinition(
    server_id="n8n",
    display_name="n8n Workflows",
    description="Execute n8n workflows via MCP",
    transport="stdio",
    npm_package="mcp-server-n8n",
    stdio_command="npx",
    stdio_args=["-y", "mcp-server-n8n"],
    required_env=["N8N_API_URL", "N8N_API_KEY"]
)
```

**Why Not Pattern N4 (n8n as gateway)?**

Per the [feasibility analysis](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md#4-pattern-n4-feasibility-report), using n8n as an MCP gateway achieves only **45% feasibility** due to:
- ❌ No dynamic node generation
- ❌ No SSE proxy support
- ❌ Static routing only
- ❌ No native JSON-RPC

**Status:** 📋 Planned (awaits mcp-server-n8n extraction)

---

### Pattern 4: MCP Gateway Integration

**Use Case:** You need to aggregate multiple MCP servers behind a single endpoint.

**Architecture:**
```
MCP Client
    ↓
mcp-gateway (Python - FastMCP)
    ↓
├── Backend A (mcp-orchestration)
├── Backend B (mcp-server-filesystem)
└── Backend C (mcp-server-n8n)
```

**mcp-orchestration as Backend:**

```python
# In mcp-gateway configuration
from fastmcp import FastMCP, Client

gateway = FastMCP("MCP Gateway")

# Mount mcp-orchestration as backend
orch_client = Client("http://localhost:8080/mcp")  # future HTTP transport
async with orch_client:
    tools = await orch_client.list_tools()

proxy = FastMCP.as_proxy(orch_client, name="orchestration")
gateway.mount("orch", proxy)

# Now mcp-orchestration tools available as:
# - orch_list_clients
# - orch_get_config
# - orch_publish_config
```

**When to Use This Pattern:**
- ✅ Building a multi-tenant MCP service
- ✅ Need tool namespacing (prefix-based routing)
- ✅ Centralized authentication/authorization
- ✅ Cross-server tool orchestration

**Status:** 📋 Planned (requires HTTP transport in mcp-orchestration Wave 2.x)

---

### Pattern 5: n8n Multi-Server MCP Client (Pattern N3b)

**Use Case:** You want n8n workflows to consume tools from BOTH mcp-orchestration AND mcp-gateway simultaneously for complete automation.

**Status:** 🔬 Design Phase - Ecosystem Coordination (Q2 2026 target)

**Ecosystem Partner:** [mcp-gateway](https://github.com/liminalcommons/mcp-gateway) (formerly mcp-n8n)

**Architecture:**
```
n8n Workflow: "Auto-Configure Engineer MCP Environment"
    │
    ├─ MCP Client Node → mcp-orchestration (localhost:8080)
    │       ↓
    │   [Server registry & config management]
    │       ├─ list_available_servers (15+ servers)
    │       ├─ add_server_to_config
    │       └─ publish_config
    │
    └─ MCP Client Node → mcp-gateway (localhost:8678)
            ↓
        [Aggregated backend tools]
            ├─ chora:assemble_artifact
            ├─ github:create_issue
            ├─ slack:send_message
            └─ [10+ other backends]
```

**Why This Pattern:**
- ✅ **Dynamic server discovery** (mcp-orchestration strength)
- ✅ **Multi-backend tool execution** (mcp-gateway strength)
- ✅ **Complete automation** in visual workflows
- ✅ **No manual configuration** steps
- ✅ **Real-time adaptation** to environment changes

**Example Workflow:** "Onboard Engineer MCP Environment"

```
Trigger: New employee record in HR system
    ↓
1. HTTP Request → Get employee role (Frontend Engineer)
    ↓
2. MCP Client → mcp-orchestration:list_available_servers
    ↓
3. Function: Filter servers by role requirements
   - github-mcp (required for all engineers)
   - figma-mcp (required for frontend)
   - linear-mcp (required for all)
    ↓
4. Loop: For each required server
   - MCP Client → mcp-orchestration:add_server_to_config
    ↓
5. MCP Client → mcp-orchestration:publish_config
    ↓
6. MCP Client → mcp-gateway:github:create_repo
   - Create personal sandbox repo
    ↓
7. MCP Client → mcp-gateway:linear:create_issue
   - Create onboarding tasks
    ↓
8. MCP Client → mcp-gateway:slack:send_message
   - Notify team channel
    ↓
9. MCP Client → mcp-gateway:chora:assemble_artifact
   - Generate onboarding guide from template
```

**Business Value:**
- **Automation:** Complete onboarding in <5 minutes (vs. 2-3 hours manual)
- **Consistency:** Same setup for every engineer, no missed steps
- **Visibility:** n8n dashboard shows onboarding progress
- **Flexibility:** Role-based configurations easily updated

**Technical Requirements:**

**mcp-orchestration:**
- ✅ Wave 2.0: HTTP/SSE transport (Q1 2026 target)
- ✅ Universal Loadability Format adoption
- ✅ API ergonomics for visual workflows
- ✅ Testing with gateway endpoints

**mcp-gateway:**
- ✅ v1.3.0: HTTP Streamable transport (Weeks 7-9)
- ✅ v1.2.0: Universal Loadability Format specification
- ✅ Pattern P5 fixes for multi-backend aggregation
- ✅ Integration documentation

**Joint Deliverable:**
- ✅ Custom n8n node: `@chora/mcp-client` (generic MCP client)
- ✅ Example workflow library (3+ workflows)
- ✅ Integration testing and validation
- ✅ Joint documentation

**Additional Use Cases:**

**Environment-Specific MCP Configurations:**
```
Trigger: Deployment to environment (dev/staging/prod)
    ↓
1. Get target environment
2. mcp-orchestration:list_available_servers
3. Filter by environment requirements
4. mcp-orchestration:validate_config
5. mcp-orchestration:publish_config
6. mcp-gateway:slack:send_message (notify team)
```

**MCP Server Health Monitoring:**
```
Schedule: Every 5 minutes
    ↓
1. mcp-orchestration:list_available_servers
2. Loop: Check each server health
3. If unhealthy:
   - mcp-orchestration:remove_server_from_config
   - mcp-gateway:linear:create_issue
   - mcp-gateway:slack:send_message
4. On recovery:
   - mcp-orchestration:add_server_to_config
   - mcp-gateway:linear:update_issue
```

**Coordination Status:**

**Timeline:**
| Milestone | mcp-orchestration | mcp-gateway | Status |
|-----------|-------------------|-------------|--------|
| Universal Loadability Review | Week 6 | v1.2.0 (Weeks 5-6) | 📋 Planned |
| HTTP Transport | Wave 2.0 (Q1 2026) | v1.3.0 (Weeks 7-9) | 🎯 Critical Sync |
| Pattern N3b Launch | Wave 2.2+ (Q2 2026) | v2.1.0 (Q2 2026) | 🎯 Joint Milestone |

**Communication:**
- Primary: GitHub Discussions (location TBD)
- Cadence: Asynchronous-first, quarterly sync calls
- Decision Framework: Joint decisions documented in both repos

**References:**
- [Integration Briefing from mcp-gateway](../../inbox/mcp-n8n(to%20be%20mcp-gateway)/integration-briefing-for-mcp-orchestration.md)
- [mcp-orchestration Response](../../inbox/mcp-n8n(to%20be%20mcp-gateway)/RESPONSE.md)
- [mcp-gateway Strategic Roadmap](../../inbox/mcp-n8n(to%20be%20mcp-gateway)/STRATEGIC_ROADMAP.md)
- [MCP-n8n to MCP-Gateway Evolution Research](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md)

**When to Use Pattern N3b:**
- ✅ Need both configuration management AND tool execution
- ✅ Building complex multi-step automation workflows
- ✅ Visual workflow interface preferred
- ✅ Role-based or environment-specific configurations
- ✅ Automated server health monitoring and failover

**Status:** 📋 Planned (requires coordination with mcp-gateway team)

---

## Capability Manifest

Following the [ecosystem standards](../../dev-docs/vision/ecosystem-intent.md#minimum-manifest-requirements), here is mcp-orchestration's capability manifest:

```yaml
id: mcp.orchestration
version: 0.1.3
owner: liminalcommons/mcp-orchestration
lifecycle_stage: operate
stability: stable

inputs:
  - name: client_id
    type: string
    description: MCP client identifier (e.g., "claude-desktop")
  - name: server_id
    type: string
    description: MCP server registry identifier
  - name: draft_payload
    type: object
    description: Configuration payload to build/publish

outputs:
  - name: config_artifact
    type: object
    description: Signed configuration artifact (SHA-256 addressed)
  - name: diff_result
    type: object
    description: Configuration comparison with change summary

dependencies:
  - name: fastmcp
    version: ">=0.5.0"
  - name: cryptography
    version: ">=41.0.0"

security_tier: moderate
  rationale: Handles signing keys and configuration data
  controls:
    - Ed25519 key storage (mode 0600)
    - Content-addressable storage (SHA-256)
    - Cryptographic signatures on all artifacts

adr_links:
  - dev-docs/vision/CAPABILITY_EVOLUTION.example.md
  - project-docs/WAVE_1X_PLAN.md

validation_status:
  last_run: 2025-10-24T12:00:00Z
  result: pass
  coverage: 85%
  tool: pytest

capabilities:
  - id: mcp.orchestration.client.list
    description: List supported MCP client families
    status: stable
    wave: 1.0

  - id: mcp.orchestration.config.get
    description: Retrieve signed configuration artifact
    status: stable
    wave: 1.0

  - id: mcp.orchestration.config.diff
    description: Compare local vs remote configs
    status: stable
    wave: 1.0

  - id: mcp.orchestration.registry.list
    description: Browse available MCP servers
    status: stable
    wave: 1.1

  - id: mcp.orchestration.config.build
    description: Build draft configuration
    status: stable
    wave: 1.2

  - id: mcp.orchestration.config.publish
    description: Sign and publish configuration
    status: stable
    wave: 1.3

value_scenarios:
  - id: mcp.orchestration.config.bootstrap
    description: Bootstrap first configuration for new user
    guide: user-docs/tutorials/01-first-configuration.md
    automated_test: tests/integration/test_end_to_end_workflow.py
    change_signal: SIG-wave-1-3-complete

  - id: mcp.orchestration.config.update
    description: Detect and apply configuration updates
    guide: user-docs/how-to/check-config-updates.md
    automated_test: tests/test_diff_engine.py
    change_signal: SIG-wave-1-0-complete

telemetry:
  signals:
    - name: mcp.orchestration.tool_usage
      type: counter
      labels: [tool_name, client_id, status]

    - name: mcp.orchestration.config_published
      type: counter
      labels: [client_id, profile_id, server_count]

    - name: mcp.orchestration.diff_detected
      type: counter
      labels: [status, change_count]

discovery:
  cli_commands:
    - mcp-orchestration
    - mcp-orchestration-init
  docs:
    - user-docs/README.md
    - user-docs/reference/mcp-tools.md
  pypi_package: mcp-orchestration
  repository: https://github.com/liminalcommons/mcp-orchestration
```

---

## Architecture Patterns

### Content-Addressable Storage (CAS)

mcp-orchestration uses **SHA-256 content addressing** for immutable, cryptographically verifiable configurations:

```
~/.mcp-orchestration/
├── keys/
│   ├── signing.key        # Ed25519 private key (mode 0600)
│   └── signing.pub        # Ed25519 public key
├── artifacts/
│   ├── 8e91a062...json    # Signed config artifact (SHA-256 hash)
│   └── a4f2d89c...json
└── clients/
    └── claude-desktop/
        └── default/
            └── latest.json  # Pointer to latest artifact
```

**Benefits:**
- ✅ Immutable history
- ✅ Cryptographic verification
- ✅ Deduplication (identical configs = same hash)
- ✅ Audit trail

### Transport Abstraction Layer

**Problem:** MCP servers use different transports (stdio, HTTP, SSE), but all MCP clients expect stdio.

**Solution:** mcp-orchestration **auto-wraps HTTP/SSE servers** with `mcp-remote`:

```python
# Input: HTTP server definition
ServerDefinition(
    server_id="custom-api",
    transport="http",
    http_url="https://api.example.com/mcp"
)

# Output: stdio-compatible config
{
  "custom-api": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/mcp-remote",
      "stdio",
      "https://api.example.com/mcp"
    ]
  }
}
```

**User never sees mcp-remote** - it's transparent wrapping.

### Draft Workflow Pattern

**Problem:** Users need to experiment with configs without breaking their current setup.

**Solution:** Draft → Validate → Publish workflow:

```
1. add_server_to_config()     → Modifies draft (unsigned)
2. view_draft_config()         → Preview changes
3. add_server_to_config()     → Add more servers
4. publish_config()           → Sign + store as artifact
5. get_config()               → Retrieve for deployment
```

**Benefits:**
- ✅ Safe experimentation
- ✅ Rollback (just clear draft)
- ✅ Atomic publishing
- ✅ Signed artifacts only after validation

---

## Decision Framework

### When to Use mcp-orchestration

Use this decision tree to determine if mcp-orchestration is right for your use case:

```
┌─────────────────────────────────────┐
│ Do you need to manage MCP client    │
│ configurations programmatically?    │
└──────────┬──────────────────────────┘
           │
    ┌──────┴──────┐
    │ YES         │ NO → Consider other tools
    │             │
    │             └────────────────────────────┐
    │                                          │
    │  Are you building:                       │
    │  • MCP client itself?         ───────────┤→ Pattern 1
    │  • Config management UI?      ───────────┤→ Pattern 2
    │  • n8n integration?           ───────────┤→ Pattern 3
    │  • MCP gateway/aggregator?    ───────────┤→ Pattern 4
    └──────────────────────────────────────────┘
```

### Comparison with Alternatives

| Feature | mcp-orchestration | Manual Config Files | Custom Scripts | MCP Gateway |
|---------|-------------------|---------------------|----------------|-------------|
| **Config Management** | ✅ Built-in | ❌ Manual editing | ⚠️ Custom | ❌ Not focused |
| **Crypto Signatures** | ✅ Ed25519 | ❌ None | ⚠️ DIY | ❌ None |
| **Server Registry** | ✅ 15+ servers | ❌ None | ❌ None | ⚠️ Custom |
| **Transport Abstraction** | ✅ Auto-wrapping | ❌ Manual | ⚠️ Custom | ✅ Built-in |
| **Diff Detection** | ✅ Intelligent | ❌ Manual diff | ⚠️ Basic | ❌ None |
| **Multi-Client Support** | ✅ Yes | ⚠️ Manual | ⚠️ Custom | ❌ N/A |
| **Version Control** | ✅ CAS + history | ⚠️ Git | ⚠️ Custom | ❌ None |
| **Tool Aggregation** | ❌ Not primary | ❌ N/A | ❌ N/A | ✅ Primary |

---

## Implementation Examples

### Example 1: Integrate as MCP Server (Your App is MCP Client)

```json
// your-app/config/mcp-servers.json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

**Usage from your app:**

```typescript
// TypeScript pseudo-code
import { MCPClient } from '@modelcontextprotocol/sdk/client';

const client = new MCPClient();
await client.connect();

// List available MCP servers
const response = await client.callTool("list_available_servers", {
  transport_filter: "stdio"
});

// Build a config
await client.callTool("add_server_to_config", {
  server_id: "filesystem",
  params: { path: "/data" }
});

await client.callTool("publish_config", {
  changelog: "Added filesystem server"
});
```

### Example 2: Register Your Custom MCP Server

```python
# In your fork/PR to mcp-orchestration

from mcp_orchestrator.servers.models import ServerDefinition

# Add to src/mcp_orchestrator/servers/defaults.py
custom_server = ServerDefinition(
    server_id="my-custom-server",
    display_name="My Custom Server",
    description="Does amazing things",
    transport="stdio",
    npm_package="@myorg/mcp-server-custom",
    stdio_command="npx",
    stdio_args=["-y", "@myorg/mcp-server-custom"],
    parameters=[
        ServerParameter(
            name="api_key",
            type="string",
            description="API key for authentication",
            required=True
        )
    ],
    required_env=["CUSTOM_API_KEY"],
    documentation_url="https://docs.myorg.com/mcp",
    tags=["api", "custom"]
)
```

### Example 3: Consume mcp-orchestration from Python

```python
# Your Python application
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_orchestration():
    server_params = StdioServerParameters(
        command="mcp-orchestration",
        args=[]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool(
                "list_available_servers",
                arguments={}
            )
            print(result.content)

asyncio.run(use_orchestration())
```

### Example 4: Ecosystem Capability Discovery

Following the [ecosystem discovery model](../../dev-docs/vision/ecosystem-intent.md#discovery-expectations):

```python
# Your platform tooling / discovery indexer
import httpx
from typing import List

async def discover_mcp_orchestration_capabilities() -> dict:
    """Discover mcp-orchestration capabilities from manifest."""

    # Future: fetch from .well-known/capability-manifest.yaml
    # For now: embedded manifest

    manifest = {
        "id": "mcp.orchestration",
        "version": "0.1.3",
        "capabilities": [
            {
                "id": "mcp.orchestration.client.list",
                "description": "List supported MCP clients",
                "status": "stable"
            },
            # ... more capabilities
        ],
        "discovery": {
            "cli_commands": ["mcp-orchestration"],
            "docs": ["user-docs/reference/mcp-tools.md"],
            "pypi_package": "mcp-orchestration"
        }
    }

    return manifest

# Register with ecosystem index
async def register_with_chora_platform():
    capabilities = await discover_mcp_orchestration_capabilities()

    # Publish to change signal queue
    signal = {
        "id": "SIG-mcp-orch-capability-update",
        "type": "capability-registration",
        "manifest": capabilities,
        "owner": "liminalcommons/mcp-orchestration"
    }

    # Send to ecosystem message bus
    await publish_change_signal(signal)
```

---

## Migration Paths

### From Manual Config Management

**Before:**
```json
// Manually edited ~/.config/claude/config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
    }
  }
}
```

**After (using mcp-orchestration):**
```typescript
// Use MCP tools in Claude
await add_server_to_config({
  server_id: "filesystem",
  params: { path: "/data" }
})

await publish_config({
  changelog: "Migrated from manual config"
})
```

**Benefits:**
- ✅ Version control
- ✅ Cryptographic signatures
- ✅ Diff detection
- ✅ Rollback capability

### From mcp-n8n to mcp-orchestration + mcp-server-n8n

Based on the [migration plan](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md#6-repository-migration-plan):

**Phase 1: Install mcp-orchestration**
```bash
pip install mcp-orchestration
mcp-orchestration-init
```

**Phase 2: Wait for mcp-server-n8n extraction** (planned)
```bash
# Future
npm install -g mcp-server-n8n
```

**Phase 3: Register n8n as MCP server**
```typescript
await add_server_to_config({
  server_id: "n8n",
  env_vars: {
    N8N_API_URL: "http://localhost:5678",
    N8N_API_KEY: process.env.N8N_API_KEY
  }
})
```

---

## References

### Related Documentation

- **User Documentation**: [user-docs/README.md](../../user-docs/README.md)
- **MCP Tools Reference**: [user-docs/reference/mcp-tools.md](../../user-docs/reference/mcp-tools.md)
- **Wave Plan**: [project-docs/WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md)
- **Ecosystem Intent**: [dev-docs/vision/ecosystem-intent.md](../../dev-docs/vision/ecosystem-intent.md)

### Research Documents

- **MCP-n8n to MCP-Gateway Evolution**: [MCP-n8n to MCP-Gateway Evolution.md](./MCP-n8n%20to%20MCP-Gateway%20Evolution.md)
- **Claude Desktop MCP HTTP Transport**: [claude_desktop_mcp_http_transport_briefing.md](./claude_desktop_mcp_http_transport_briefing.md)
- **n8n API Key Bootstrap**: [n8n-api-key-bootstrap.md](./n8n-api-key-bootstrap.md)

### External Specifications

- **Model Context Protocol**: https://modelcontextprotocol.io/
- **FastMCP**: https://github.com/jlowin/fastmcp
- **mcp-remote**: https://github.com/modelcontextprotocol/servers/tree/main/src/mcp-remote
- **Sigstore**: https://www.sigstore.dev/

### Ecosystem Standards

Following the [Chora ecosystem naming conventions](../../dev-docs/vision/ecosystem-intent.md#naming-guidelines):

- **Repository Pattern**: `<domain>-<capability-provider>` → `mcp-orchestration`
- **Capability ID Pattern**: `<domain>.<capability>.<action>` → `mcp.orchestration.config.publish`
- **Change Signal Pattern**: `SIG.<scope>.<subject>.<state>` → `SIG-wave-1-3-complete`

---

## Integration Support

### Quick Start Checklist

- [ ] Review [integration patterns](#integration-patterns) and choose yours
- [ ] Check [decision framework](#decision-framework) to validate fit
- [ ] Install mcp-orchestration: `pip install mcp-orchestration`
- [ ] Initialize storage: `mcp-orchestration-init`
- [ ] Add to your MCP client config (Pattern 1/4)
- [ ] Test with `list_available_servers` tool
- [ ] Read [user documentation](../../user-docs/README.md)

### Common Issues

**Issue: "Signing keys not found"**
```bash
# Solution: Initialize keys first
mcp-orchestration-init
# Or via MCP tool:
await initialize_keys()
```

**Issue: "Server not in registry"**
```python
# Solution: Add custom server definition
# See Example 2 above
```

**Issue: "Transport not supported (HTTP)"**
```
Status: Planned for Wave 2.x
Workaround: Use stdio transport or subprocess invocation (Pattern 2)
```

### Getting Help

- **Documentation**: [user-docs/README.md](../../user-docs/README.md)
- **Issues**: https://github.com/liminalcommons/mcp-orchestration/issues
- **Discussions**: GitHub Discussions (TBD)
- **Ecosystem Coordination**: File change signal via [ecosystem process](../../dev-docs/vision/ecosystem-intent.md#change-signaling-workflow)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-24 | Initial ecosystem integration guide |

---

**Maintained by:** liminalcommons/mcp-orchestration
**Ecosystem Coordination:** chora-platform
**Last Updated:** 2025-10-24
**Next Review:** 2025-11-24 (or when Wave 2.x ships HTTP transport)

---

## Appendix: Integration Pattern Matrix

| Your Use Case | Pattern | mcp-orch Role | Transport | Status |
|---------------|---------|---------------|-----------|--------|
| Building MCP client app | Pattern 1 | Config manager | stdio | ✅ Stable |
| Building config UI | Pattern 2 | Backend service | HTTP* | 📋 Planned |
| Exposing n8n workflows | Pattern 3 | Registry entry | stdio | 📋 Planned |
| Building MCP gateway | Pattern 4 | Backend server | HTTP* | 📋 Planned |
| Managing configs (end user) | Pattern 1 | Direct usage | stdio | ✅ Stable |

*HTTP transport planned for Wave 2.x

---

## Appendix: Capability Evolution Roadmap

See [CAPABILITY_EVOLUTION.example.md](../../dev-docs/vision/CAPABILITY_EVOLUTION.example.md) for mcp-orchestration's long-term capability roadmap.

**Current Focus (Wave 1.x):** Configuration management, server registry, draft workflow
**Future Focus (Wave 2.x):** HTTP transport, multi-user, RBAC, cloud sync
**Future Focus (Wave 3.x):** Policy enforcement, compliance, enterprise features

---

**🔗 Integration Status:** Active
**📊 Stability:** Stable (v0.1.3)
**🎯 Recommended For:** MCP client configuration management
**⚠️ Not Recommended For:** Dynamic MCP gateway (use mcp-gateway instead)
