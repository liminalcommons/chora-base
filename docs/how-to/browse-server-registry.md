---
title: Browse MCP Server Registry
wave: 1.1
version: v0.1.1
status: complete
last_updated: 2025-10-24
---

# How To: Browse MCP Server Registry

This guide covers discovering and exploring available MCP servers using the server registry.

## Objective

Learn how to:
- List all available MCP servers
- Filter servers by transport type
- Search for specific servers
- View detailed server information
- Understand server requirements and configuration

## Prerequisites

- MCP orchestration installed (`pip install mcp-orchestration`)
- Basic familiarity with command line

## Scenario 1: Discover All Available Servers

### Using CLI

List all servers in the registry:

```bash
mcp-orchestration-list-servers
```

**Expected Output:**

```
Found 15 server(s):

● Brave Search
  ID: brave-search
  Transport: stdio
  Description: Web search using Brave Search API
  Tags: search, web, internet
  NPM: @modelcontextprotocol/server-brave-search
  Requires: BRAVE_API_KEY

● Filesystem Access
  ID: filesystem
  Transport: stdio
  Description: Read, write, and search local files and directories
  Tags: files, storage, local
  NPM: @modelcontextprotocol/server-filesystem

... (more servers)

Summary:
  stdio: 13
  http:  1
  sse:   1
```

### Using MCP Tools (from Claude Desktop)

Once you've added the mcp-orchestration server to your Claude Desktop config:

```
User: "What MCP servers are available?"

Claude: [calls list_available_servers tool]
```

Claude will show you the full list of available servers with descriptions.

## Scenario 2: Filter by Transport Type

### Find Only stdio Servers

```bash
mcp-orchestration-list-servers --transport stdio
```

This shows only servers that use stdio transport (local processes).

### Find Only HTTP/SSE Servers

```bash
mcp-orchestration-list-servers --transport http
```

or

```bash
mcp-orchestration-list-servers --transport sse
```

This shows servers that use HTTP or SSE transport (remote servers).

**Note**: HTTP and SSE servers will be automatically wrapped with `mcp-remote` when added to client configurations, providing transparent stdio compatibility.

## Scenario 3: Search for Specific Servers

### Search by Keyword

Search for database-related servers:

```bash
mcp-orchestration-list-servers --search database
```

**Output:**

```
Found 2 server(s):

● PostgreSQL Database
  ID: postgres
  Transport: stdio
  Description: Query and manage PostgreSQL databases
  Tags: database, sql, postgres
  NPM: @modelcontextprotocol/server-postgres

● SQLite Database
  ID: sqlite
  Transport: stdio
  Description: Query and manage SQLite databases
  Tags: database, sql, sqlite
  NPM: @modelcontextprotocol/server-sqlite
```

Search is case-insensitive and matches against:
- Server ID
- Display name
- Description
- Tags

### Examples of Useful Searches

```bash
# Find search-related servers
mcp-orchestration-list-servers --search search

# Find file-related servers
mcp-orchestration-list-servers --search files

# Find automation servers
mcp-orchestration-list-servers --search automation

# Find monitoring/debugging servers
mcp-orchestration-list-servers --search monitoring
```

## Scenario 4: Get Detailed Server Information

### View Full Server Details

```bash
mcp-orchestration-describe-server filesystem
```

**Output:**

```
● Filesystem Access

Server ID:
  filesystem

Description:
  Read, write, and search local files and directories

Transport:
  Type: stdio
  Command: npx
  Args: -y @modelcontextprotocol/server-filesystem {path}

Parameters:
  • path (path, required)
    Root directory path to expose
    Example: /Users/you/Documents

Installation:
  NPM Package: @modelcontextprotocol/server-filesystem
  Install: npm install -g @modelcontextprotocol/server-filesystem
  Or use via: npx (no installation needed)

Documentation:
  https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Tags:
  files, storage, local

Usage Example:
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/you/Documents"
      ]
    }
  }
}
```

### Describe HTTP/SSE Server

```bash
mcp-orchestration-describe-server n8n
```

**Output Shows:**

```
Transport:
  Type: sse
  URL: http://localhost:{port}/mcp/sse
  Auth: bearer
  Note: Will be automatically wrapped with mcp-remote for stdio compatibility

Parameters:
  • port (int, optional)
    n8n server port
    Default: 5679
    Example: 5679

Environment Variables:
  • N8N_API_KEY (required)

Usage Example:
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/mcp-remote",
        "stdio",
        "http://localhost:5679/mcp/sse"
      ],
      "env": {
        "N8N_API_KEY": "${N8N_API_KEY}"
      }
    }
  }
}
```

**Notice**: The usage example shows how the HTTP/SSE server will be automatically wrapped with `mcp-remote`.

## Scenario 5: JSON Output for Scripting

### Get JSON Output

```bash
mcp-orchestration-list-servers --format json
```

**Output:**

```json
{
  "servers": [
    {
      "server_id": "filesystem",
      "display_name": "Filesystem Access",
      "description": "Read, write, and search local files and directories",
      "transport": "stdio",
      "npm_package": "@modelcontextprotocol/server-filesystem",
      "tags": ["files", "storage", "local"],
      "requires_env": []
    },
    ...
  ],
  "count": 15,
  "transport_counts": {
    "stdio": 13,
    "http": 1,
    "sse": 1
  }
}
```

This is useful for:
- Scripting and automation
- Building custom UIs
- Integration with other tools

### Get Server Details as JSON

```bash
mcp-orchestration-describe-server filesystem --format json
```

Returns the complete ServerDefinition as JSON.

## Understanding Server Information

### Transport Types

**stdio** (Standard Input/Output)
- Runs as a local subprocess
- Direct communication via stdin/stdout
- Lowest latency
- Most common type
- Examples: filesystem, brave-search, github

**http** (HTTP API)
- Runs as a remote HTTP server
- Automatically wrapped with mcp-remote
- Network latency applies
- Can be hosted remotely
- Examples: custom-api

**sse** (Server-Sent Events)
- Runs as a remote server with streaming
- Automatically wrapped with mcp-remote
- Supports real-time updates
- Can be hosted remotely
- Examples: n8n

### Parameters vs Environment Variables

**Parameters**:
- Configuration values specific to each server instance
- Example: `path` for filesystem server
- Substituted into command args or URLs
- Can have defaults and examples

**Environment Variables**:
- Secrets and API keys
- Example: `BRAVE_API_KEY`, `GITHUB_TOKEN`
- Never stored in configs (use `${VAR_NAME}` placeholders)
- Resolved at runtime from environment

### Required vs Optional

**Required Parameters/Env**:
- Must be provided to use the server
- Server won't start without them
- Marked clearly in descriptions

**Optional Parameters/Env**:
- Have sensible defaults
- Can be omitted
- Customize behavior when needed

## Next Steps

After browsing the registry, you can:

1. **Wave 1.2** (Coming Soon): Add servers to client configurations
2. **Wave 1.3** (Coming Soon): Validate draft configurations
3. **Wave 1.4** (Coming Soon): Publish and sign configurations

## Common Servers in Registry

### Local Development
- **filesystem**: File operations
- **memory**: Persistent key-value storage
- **sqlite**: Local database access

### Web & Search
- **brave-search**: Web search
- **fetch**: Fetch web content
- **puppeteer**: Browser automation

### Development Tools
- **github**: GitHub integration
- **slack**: Slack workspace management
- **sentry**: Error tracking

### Databases
- **postgres**: PostgreSQL access
- **sqlite**: SQLite access

### Remote/HTTP
- **n8n**: Workflow automation (SSE)
- **custom-api**: Example HTTP server

## Troubleshooting

### Command Not Found

```bash
mcp-orchestration-list-servers: command not found
```

**Solution**: Reinstall the package:
```bash
pip install --upgrade mcp-orchestration
```

### No Servers Found

If search returns no results, try:
- Broader search terms
- Check spelling
- Remove transport filter

### Server Not in Registry

If you can't find a server:
1. Check the [MCP Servers](https://github.com/modelcontextprotocol/servers) repository
2. Wait for next registry update
3. Or add custom servers (Wave 1.2+)

## Expected Result

You can now:
- ✅ Browse all available MCP servers
- ✅ Filter servers by transport type
- ✅ Search for specific functionality
- ✅ View detailed server information
- ✅ Understand server requirements
- ✅ See usage examples

## Reference

- Server Registry Code: [src/mcp_orchestrator/servers/](../../src/mcp_orchestrator/servers/)
- Default Catalog: [src/mcp_orchestrator/servers/defaults.py](../../src/mcp_orchestrator/servers/defaults.py)
- CLI Commands: [src/mcp_orchestrator/cli_servers.py](../../src/mcp_orchestrator/cli_servers.py)
- Tests: [tests/test_server_registry.py](../../tests/test_server_registry.py)
