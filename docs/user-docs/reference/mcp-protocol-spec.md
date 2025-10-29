# MCP Protocol Reference

**Protocol Version**: 2024-11-05
**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Reference

---

## Overview

The Model Context Protocol (MCP) is an open protocol that standardizes how AI assistants connect to tools, data sources, and computational resources. This reference document provides technical details about the MCP protocol specification.

**Official Specification**: [https://modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)

**Purpose**:
- Provide quick reference for MCP protocol details
- Document message formats and exchanges
- Explain transport mechanisms
- Clarify error handling patterns

**Audience**: Developers implementing MCP servers or clients, AI agents working with MCP

---

## Protocol Foundation

### JSON-RPC 2.0

MCP is built on [JSON-RPC 2.0](https://www.jsonrpc.org/specification), a stateless, lightweight remote procedure call protocol.

**Key characteristics**:
- Request/response pattern
- JSON serialization
- Batch requests supported
- Standardized error codes

**Message structure**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": { ...parameters... }
}
```

---

## Core Concepts

### Tools

**Definition**: Functions that AI assistants can invoke to perform actions.

**Characteristics**:
- **Callable**: AI assistants send requests, servers execute and return results
- **Typed**: Parameters and return values have defined types
- **Documented**: Description visible to AI assistant
- **Synchronous**: Request → Execution → Response (async tools use callbacks)

**Example**:
```json
{
  "name": "create_task",
  "description": "Create a new task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {"type": "string"},
      "priority": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["title"]
  }
}
```

---

### Resources

**Definition**: Data sources that AI assistants can read to access information.

**Characteristics**:
- **URI-addressable**: Each resource has unique identifier
- **Read-only**: AI assistants read content, cannot modify (use tools for writes)
- **Cacheable**: Clients may cache resource content
- **Content-typed**: MIME type indicates content format

**Example**:
```json
{
  "uri": "file:///project/README.md",
  "name": "Project README",
  "description": "Project documentation",
  "mimeType": "text/markdown"
}
```

---

### Prompts

**Definition**: Pre-defined templates that guide AI assistant interactions.

**Characteristics**:
- **Template-based**: May include variables for customization
- **Discoverable**: Listed via protocol methods
- **Composable**: Can reference tools and resources
- **Versioned**: Evolution tracked in server changelog

**Example**:
```json
{
  "name": "analyze_code",
  "description": "Analyze code for issues",
  "arguments": [
    {
      "name": "focus",
      "description": "Analysis focus area",
      "required": false
    }
  ]
}
```

---

## Transport Mechanisms

### Standard I/O (stdio)

**Description**: Communication over standard input/output streams.

**Use case**: Local MCP servers run as subprocesses.

**Message format**: JSON-RPC messages, one per line (newline-delimited).

**Example flow**:
1. Client launches server process: `python -m my_mcp_server`
2. Client writes JSON-RPC to stdin: `{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n`
3. Server reads from stdin, processes request
4. Server writes JSON-RPC to stdout: `{"jsonrpc":"2.0","id":1,"result":{...}}\n`

**Claude Desktop configuration**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "cwd": "/path/to/server"
    }
  }
}
```

---

### Server-Sent Events (SSE)

**Description**: HTTP-based server-to-client streaming.

**Use case**: Web-based MCP clients, remote servers.

**Message format**: SSE event stream with JSON-RPC payloads.

**Example**:
```
POST /sse HTTP/1.1
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{...}}

---

HTTP/1.1 200 OK
Content-Type: text/event-stream

event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

---

### WebSocket

**Description**: Bidirectional communication over WebSocket.

**Use case**: Interactive MCP clients, real-time updates.

**Message format**: JSON-RPC messages over WebSocket frames.

**Example**:
```javascript
const ws = new WebSocket('ws://localhost:8000/mcp');

ws.onopen = () => {
  ws.send(JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "tools/list"
  }));
};

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log(response);
};
```

---

## Protocol Methods

### Initialization

#### `initialize`

**Purpose**: Negotiate protocol version and capabilities.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "clientInfo": {
      "name": "Claude Desktop",
      "version": "1.0.0"
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "My MCP Server",
      "version": "1.0.0"
    }
  }
}
```

---

### Tools

#### `tools/list`

**Purpose**: List all available tools.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "create_task",
        "description": "Create a new task",
        "inputSchema": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"}
          },
          "required": ["title"]
        }
      }
    ]
  }
}
```

---

#### `tools/call`

**Purpose**: Invoke a tool with parameters.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "create_task",
    "arguments": {
      "title": "New Task",
      "description": "Task description"
    }
  }
}
```

**Success Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"id\": \"task-001\", \"title\": \"New Task\", \"status\": \"created\"}"
      }
    ]
  }
}
```

**Error Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Invalid params: title is required"
  }
}
```

---

### Resources

#### `resources/list`

**Purpose**: List all available resources.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/list"
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "resources": [
      {
        "uri": "file:///project/README.md",
        "name": "Project README",
        "description": "Project documentation",
        "mimeType": "text/markdown"
      }
    ]
  }
}
```

---

#### `resources/read`

**Purpose**: Read resource content by URI.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/read",
  "params": {
    "uri": "file:///project/README.md"
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "contents": [
      {
        "uri": "file:///project/README.md",
        "mimeType": "text/markdown",
        "text": "# Project Name\n\nProject description..."
      }
    ]
  }
}
```

---

### Prompts

#### `prompts/list`

**Purpose**: List all available prompts.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "prompts/list"
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "prompts": [
      {
        "name": "analyze_code",
        "description": "Analyze code for issues",
        "arguments": [
          {
            "name": "focus",
            "description": "Analysis focus area",
            "required": false
          }
        ]
      }
    ]
  }
}
```

---

#### `prompts/get`

**Purpose**: Get prompt content with arguments.

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "prompts/get",
  "params": {
    "name": "analyze_code",
    "arguments": {
      "focus": "security"
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "description": "Analyze code for security issues",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Analyze the codebase for security vulnerabilities..."
        }
      }
    ]
  }
}
```

---

## Error Handling

### Standard Error Codes

MCP uses JSON-RPC 2.0 error codes plus MCP-specific codes:

| Code | Name | Description |
|------|------|-------------|
| `-32700` | Parse error | Invalid JSON received |
| `-32600` | Invalid Request | JSON-RPC request malformed |
| `-32601` | Method not found | Method does not exist |
| `-32602` | Invalid params | Invalid method parameters |
| `-32603` | Internal error | Server internal error |
| `-32000` to `-32099` | Server error | MCP-specific errors |

---

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params: title is required",
    "data": {
      "parameter": "title",
      "reason": "missing_required_field"
    }
  }
}
```

---

### Error Handling Best Practices

**For server implementers**:
1. Use `-32602` for validation errors (invalid parameters)
2. Use `-32603` for execution errors (runtime failures)
3. Include descriptive error messages
4. Add `data` field with additional context
5. Log errors for debugging

**For client implementers**:
1. Check error code to determine error type
2. Display error message to user
3. Parse `data` field for additional context
4. Implement retry logic for transient errors
5. Handle unknown errors gracefully

---

## Data Types

### Input Schema (JSON Schema)

Tools use JSON Schema to define parameter types:

```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "default": 1
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"}
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": ["title"]
}
```

---

### Content Types

**Text content**:
```json
{
  "type": "text",
  "text": "Plain text content"
}
```

**Image content** (base64-encoded):
```json
{
  "type": "image",
  "data": "iVBORw0KGgoAAAANS...",
  "mimeType": "image/png"
}
```

**Resource reference**:
```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///path/to/file",
    "mimeType": "text/plain"
  }
}
```

---

## Protocol Versioning

### Version Format

**Pattern**: `YYYY-MM-DD` (ISO 8601 date)

**Examples**:
- `2024-11-05` - Current stable version
- `2024-06-15` - Previous version

---

### Version Negotiation

1. **Client sends** preferred protocol version in `initialize` request
2. **Server responds** with supported protocol version
3. **If mismatch**: Server uses highest version supported by both
4. **If incompatible**: Server returns error

**Example negotiation**:
```json
// Client request
{"method": "initialize", "params": {"protocolVersion": "2024-11-05"}}

// Server response (compatible)
{"result": {"protocolVersion": "2024-11-05"}}

// Server response (downgrade to older version)
{"result": {"protocolVersion": "2024-06-15"}}

// Server response (incompatible)
{"error": {"code": -32000, "message": "Unsupported protocol version"}}
```

---

## Capabilities

### Server Capabilities

Servers declare capabilities in `initialize` response:

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "logging": {}
  }
}
```

**Capability flags**:
- `listChanged`: Server can notify when list changes (tools/resources/prompts)
- `subscribe`: Server supports subscriptions (resources)
- `logging`: Server supports logging protocol

---

### Client Capabilities

Clients declare capabilities in `initialize` request:

```json
{
  "capabilities": {
    "sampling": {},
    "roots": {
      "listChanged": true
    }
  }
}
```

---

## Notifications

### `notifications/tools/list_changed`

**Purpose**: Notify client that tool list has changed.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

**Client action**: Re-fetch tool list via `tools/list`.

---

### `notifications/resources/list_changed`

**Purpose**: Notify client that resource list has changed.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/list_changed"
}
```

**Client action**: Re-fetch resource list via `resources/list`.

---

### `notifications/resources/updated`

**Purpose**: Notify client that resource content has changed.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///project/README.md"
  }
}
```

**Client action**: Re-fetch resource content via `resources/read` (if subscribed).

---

## Security Considerations

### Authentication

**Current state**: MCP protocol does not define authentication mechanisms (as of 2024-11-05).

**Implications**:
- MCP servers trust their clients
- Suitable for local/trusted environments
- NOT suitable for public-facing services without additional auth layer

**Workarounds**:
- Deploy MCP servers behind authenticated gateways
- Use OS-level permissions (file system, network)
- Implement custom auth in MCP server (non-standard)

---

### Authorization

**Current state**: No built-in authorization system.

**Implications**:
- All clients have full access to all tools/resources
- No per-user or per-role permissions

**Workarounds**:
- Implement authorization logic in tool implementations
- Use environment-based access control
- Deploy separate MCP servers per user/role

---

### Input Validation

**Requirement**: Servers MUST validate all input parameters.

**Best practices**:
1. Use JSON Schema for type validation
2. Validate ranges and constraints
3. Sanitize string inputs (prevent injection attacks)
4. Check file paths for traversal attacks
5. Implement rate limiting

---

## Performance

### Response Times

**Recommendations**:
- **Tool calls**: Complete within 30 seconds (MCP clients may timeout)
- **Resource reads**: Complete within 10 seconds
- **Listings** (`tools/list`, `resources/list`): Complete within 2 seconds

**For long-running operations**:
- Return status immediately
- Provide polling mechanism (e.g., resource with status)
- Or use async patterns (callbacks, webhooks)

---

### Caching

**Client caching**:
- Clients MAY cache resource content
- Cache invalidated by `notifications/resources/updated`
- No standard cache control headers

**Server caching**:
- Servers MAY cache expensive operations
- Servers responsible for cache invalidation

---

## Related Documentation

**chora-base**:
- [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/) - Full implementation guide
- [FastMCP API Reference](fastmcp-api-reference.md) - Python SDK reference
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Naming conventions

**How-to Guides**:
- [Implement MCP Server](../how-to/implement-mcp-server.md) - Step-by-step guide
- [Configure MCP Client](../how-to/configure-mcp-client.md) - Client setup
- [Test MCP Tools](../how-to/test-mcp-tools.md) - Testing guide

**Explanations**:
- [Why MCP Servers](../explanation/why-mcp-servers.md) - Conceptual overview

**External**:
- [Official MCP Specification](https://modelcontextprotocol.io/specification) - Authoritative source
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) - Protocol foundation
- [JSON Schema](https://json-schema.org/) - Input schema format

---

**Document Version**: 1.0.0
**Protocol Version**: 2024-11-05
**Last Updated**: 2025-10-29
**Status**: Reference
