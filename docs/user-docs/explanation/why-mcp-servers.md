# Why MCP Servers?

**Document Type**: Explanation
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This document explains the Model Context Protocol (MCP), why it exists, and when you should use MCP servers versus alternative approaches. It provides conceptual understanding rather than implementation details.

**For implementation**: See [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/)

---

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI assistants (like Claude, GPT-4, etc.) connect to **tools**, **data sources**, and **computational resources**.

**Think of it as**:
- USB for AI assistants (standard interface for capabilities)
- REST API for local/trusted environments
- Plugin system with discoverability and type safety

**Key innovation**: AI assistants can **discover** what capabilities are available without hardcoding.

---

## The Problem MCP Solves

### Before MCP

**Scenario**: You want Claude to help manage your project tasks.

**Options**:
1. **Copy-paste data**: Manually paste task list into Claude's context
   - ❌ Tedious, error-prone
   - ❌ Data quickly becomes outdated
   - ❌ Token-heavy (wastes Claude's context window)

2. **Function calling with REST API**:
   - Build REST API for tasks
   - Deploy API with auth, rate limiting, CORS
   - Configure Claude to call API endpoints
   - ❌ Over-engineered for local/personal use
   - ❌ Requires hosting, domain, SSL certificates
   - ❌ Security complexity (API keys, OAuth)

3. **CLI tools**:
   - `claude run "task-cli create 'New task'"`
   - ❌ No type safety (Claude guesses command syntax)
   - ❌ Poor discoverability (Claude doesn't know what commands exist)
   - ❌ No structured data (parsing text output)

**Result**: Friction prevents you from building helpful AI workflows.

---

### After MCP

**With MCP**:
1. Build MCP server with task management tools (1-2 hours using SAP-014)
2. Configure Claude Desktop to connect to server (1 minute)
3. Claude automatically discovers tools: `taskmanager:create_task`, `taskmanager:list_tasks`
4. Claude knows parameter types, descriptions, return values
5. You ask: "Create a task for fixing that bug we discussed"
6. Claude calls tool with structured parameters
7. Done! No copy-paste, no API hosting, no token waste

**Result**: Seamless AI-human collaboration.

---

## Core Benefits

### 1. Discoverability

**Problem**: How does Claude know what capabilities you have?

**Solution**: MCP servers expose `tools/list` method listing all available tools.

**Example**:
```json
{
  "tools": [
    {"name": "taskmanager:create_task", "description": "Create new task"},
    {"name": "taskmanager:list_tasks", "description": "List all tasks"},
    {"name": "taskmanager:update_status", "description": "Update task status"}
  ]
}
```

Claude sees this list and knows:
- "I can create tasks using `taskmanager:create_task`"
- "I can list tasks using `taskmanager:list_tasks`"
- "I should suggest these capabilities to the user"

---

### 2. Type Safety

**Problem**: How does Claude know what parameters a tool needs?

**Solution**: Tools include JSON Schema for input validation.

**Example**:
```json
{
  "name": "taskmanager:create_task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "minLength": 1, "maxLength": 200},
      "priority": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["title"]
  }
}
```

Claude knows:
- `title` is required, must be 1-200 characters
- `priority` is optional, must be 1-5

**Result**: Fewer errors, better UX.

---

### 3. Composability

**Problem**: Can different capabilities work together?

**Solution**: Namespace-based tool naming enables tool discovery across servers.

**Example**:
You have two MCP servers running:
- `projectmgr` server: `projectmgr:create_project`, `projectmgr:list_projects`
- `taskmanager` server: `taskmanager:create_task`, `taskmanager:list_tasks`

Claude can compose workflows:
```
User: "Set up Project X and create initial tasks"

Claude's plan:
1. Call projectmgr:create_project(name="Project X")
2. Call taskmanager:create_task(title="Set up repository", project_id=<from step 1>)
3. Call taskmanager:create_task(title="Write README", project_id=<from step 1>)
```

**Result**: Tools from different servers work together seamlessly.

---

### 4. Data Access Without Token Waste

**Problem**: Large documents waste Claude's context window.

**Solution**: MCP resources provide URI-addressable content.

**Example**:
```
Resource: taskmanager://templates/daily-report.md
Content: 5KB markdown template
```

Claude can:
1. See resource exists (via `resources/list`)
2. Read resource on-demand (via `resources/read`)
3. Only use tokens when actually reading content

**Benefit**: 10KB project documentation? Claude reads only when needed, not upfront.

---

## When to Use MCP

### Use Case 1: Local Development Tools

**Perfect fit**: You're building tools for personal/team use with trusted AI assistants.

**Why MCP**:
- ✅ No hosting required (runs locally)
- ✅ No authentication complexity (trusted environment)
- ✅ Fast to build (30-60 min with SAP-014)
- ✅ Native integration with Claude Desktop

**Examples**:
- Task management
- Code analysis
- Documentation generation
- Project automation

---

### Use Case 2: Data-Heavy Workflows

**Perfect fit**: You have large datasets/documents that don't fit in Claude's context.

**Why MCP**:
- ✅ Resources provide on-demand data access
- ✅ No token waste on unused content
- ✅ Dynamic data (always up-to-date)

**Examples**:
- Project knowledge base
- API documentation
- Configuration files
- Database queries

---

### Use Case 3: Multi-Tool Ecosystems

**Perfect fit**: You're building suite of related capabilities.

**Why MCP**:
- ✅ Composability (tools reference each other)
- ✅ Namespace isolation (no name collisions)
- ✅ Discoverability (Claude sees all capabilities)

**Examples**:
- Development environment (linting + testing + deployment)
- Content pipeline (generation + editing + publishing)
- Analytics suite (data extraction + analysis + visualization)

---

## When NOT to Use MCP

### Anti-Pattern 1: Public APIs

**Scenario**: You're building public-facing API for web/mobile apps.

**Why NOT MCP**:
- ❌ No authentication (MCP trusts clients)
- ❌ No authorization (no per-user permissions)
- ❌ No rate limiting (protocol-level)
- ❌ Designed for trusted environments

**Alternative**: Build REST API with proper auth (OAuth, JWT) + maybe MCP server for internal use.

---

### Anti-Pattern 2: Real-Time Streaming

**Scenario**: You need to stream large data (logs, video, metrics).

**Why NOT MCP**:
- ❌ No streaming support (as of 2024-11-05 spec)
- ❌ Resources return full content

**Alternative**: WebSocket or SSE + chunking, or wait for future MCP streaming support.

---

### Anti-Pattern 3: Simple Scripts

**Scenario**: You have bash script that doesn't need structured data.

**Why NOT MCP**:
- ❌ Overhead not justified for simple tasks
- ❌ Claude already has bash tool integration

**Alternative**: Keep as bash script, use Claude's native bash integration.

---

## Architecture Patterns

### Pattern 1: Direct Integration

```
Claude Desktop
     ↓ (stdio)
MCP Server (Python, local)
     ↓
Your Application (direct function calls)
```

**Use when**: MCP server is thin wrapper around existing app.

---

### Pattern 2: Gateway Pattern

```
Claude Desktop
     ↓ (stdio)
MCP Gateway
     ↓ (HTTP/gRPC)
Multiple Backend Services
```

**Use when**: MCP tools need to coordinate multiple services.

---

### Pattern 3: Multi-Server

```
Claude Desktop
     ├─ (stdio) → projectmgr MCP Server
     ├─ (stdio) → taskmanager MCP Server
     └─ (stdio) → docgen MCP Server
```

**Use when**: You have multiple independent capabilities.

---

## Trade-Offs

### MCP vs REST API

| Aspect | MCP | REST API |
|--------|-----|----------|
| **Setup time** | 30-60 min | Hours to days |
| **Authentication** | None (trusted) | OAuth, JWT, API keys |
| **Discoverability** | Built-in | Manual (OpenAPI) |
| **Type safety** | JSON Schema | OpenAPI Schema |
| **Hosting** | Local process | Web server + domain |
| **Use case** | Trusted/local | Public/untrusted |

**Recommendation**: Use MCP for trusted environments, REST for public APIs.

---

### MCP vs CLI Tools

| Aspect | MCP | CLI |
|--------|-----|-----|
| **Type safety** | Strong (JSON Schema) | Weak (text parsing) |
| **Discoverability** | Automatic | Manual (--help) |
| **Structured data** | Native (JSON) | Text output |
| **Error handling** | Standardized | Custom |
| **Setup** | Client config | PATH setup |

**Recommendation**: Use MCP for structured workflows, CLI for quick ad-hoc tasks.

---

## Future of MCP

### Protocol Evolution

**Expected developments**:
- Streaming support (long-running operations)
- Subscription model (push notifications)
- Authentication mechanisms (optional)
- Enhanced capability negotiation

**Current status** (2024-11-05): Protocol is stable, improvements planned.

---

### Ecosystem Growth

**Trends**:
- More MCP clients (beyond Claude Desktop)
- Public MCP server registry
- Language-specific SDKs (TypeScript, Go, Rust)
- Enterprise MCP gateways

**chora-base role**: Provide best practices (SAP-014, Chora MCP Conventions v1.0) as ecosystem grows.

---

## Related Documentation

**chora-base**:
- [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/) - Implementation guide
- [MCP Protocol Reference](../reference/mcp-protocol-spec.md) - Protocol details
- [FastMCP API Reference](../reference/fastmcp-api-reference.md) - Python SDK
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Naming standards

**How-to Guides**:
- [Implement MCP Server](../how-to/implement-mcp-server.md) - Step-by-step guide
- [Configure MCP Client](../how-to/configure-mcp-client.md) - Client setup
- [Test MCP Tools](../how-to/test-mcp-tools.md) - Testing guide

**Workflows**:
- [MCP Development Workflow](../../dev-docs/workflows/mcp-development-workflow.md) - Developer workflow

**External**:
- [MCP Specification](https://modelcontextprotocol.io/specification) - Official spec
- [MCP GitHub](https://github.com/modelcontextprotocol/servers) - Server registry

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
