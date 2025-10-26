---
title: Add an MCP Server to Your Configuration
audience: end-users
difficulty: intermediate
time: 5-15 minutes
wave: 1.2-1.3
version: v0.1.5
---

# Add an MCP Server to Your Configuration

> **💡 First time?** See [Complete Workflow Guide](complete-workflow.md) Part 2A for the basic workflow. This guide is a **deep dive on server configuration**.

**Goal:** Understand how to add and configure different types of MCP servers with correct parameters, environment variables, and transport handling.

**Prerequisites:**
- [Get Started](get-started.md) - mcp-orchestration installed
- Signing keys initialized

---

## Understanding Server Types

MCP servers use two transport types:

**stdio (Most Common):** Local processes communicating via stdin/stdout. Examples: filesystem, memory, postgres. No special handling needed.

**HTTP/SSE:** HTTP services using Server-Sent Events. Examples: brave-search, custom APIs. Automatically wrapped with mcp-remote for Claude Desktop compatibility.

**Key insight:** mcp-orchestration detects transport type and handles wrapping transparently.

---

## Configuration Methods

### Via Claude (Recommended)

```
> Add filesystem server for /Users/me/Documents
> Add github server with token ${GITHUB_TOKEN}
> Add memory server
```

**Process:**
1. Server ID validated against registry
2. Parameters substituted into template
3. HTTP/SSE servers wrapped with mcp-remote
4. Configuration added to draft

### Via CLI

```bash
mcp-orchestration list-servers           # Browse available
mcp-orchestration describe-server <id>   # Get details
```

For programmatic access, see [Reference: MCP Tools API](../reference/mcp-tools.md).

---

## Server-Specific Configuration

### Filesystem Server

**Use case:** Local file/directory access | **Transport:** stdio

**Parameters:** `path` (required) - Directory to expose

**Example:**
```
> Add filesystem server for /Users/me/Projects
```

**Result:**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Projects"]
  }
}
```

**Multiple paths:** Use custom names:
```
> Add filesystem server with name "work" and path /Users/me/Work
> Add filesystem server with name "personal" and path /Users/me/Personal
```

---

### GitHub Server

**Use case:** Repository operations, issues, PRs | **Transport:** stdio

**Environment variables:** `GITHUB_TOKEN` (required)

**Example:**
```
> Add github server with token ${GITHUB_TOKEN}
```

**Result:**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

**Note:** `${GITHUB_TOKEN}` reads from environment variable at runtime.

---

### Memory Server

**Use case:** Persistent key-value storage | **Transport:** stdio

**Parameters:** None | **Environment variables:** None

**Example:**
```
> Add memory server
```

**Result:**
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  }
}
```

---

### PostgreSQL Server

**Use case:** Database queries | **Transport:** stdio

**Parameters:** `connection_string` (required)

**Example:**
```
> Add postgres server with connection string postgresql://localhost/mydb
```

**Security tip:** Use environment variables for credentials:
```
> Add postgres server with connection string postgresql://${DB_USER}:${DB_PASS}@localhost/mydb
```

---

### Brave Search Server

**Use case:** Web search | **Transport:** HTTP/SSE (auto-wrapped)

**Environment variables:** `BRAVE_API_KEY` (required)

**Example:**
```
> Add brave search server with API key ${BRAVE_API_KEY}
```

**Note:** mcp-orchestration detects HTTP/SSE and wraps automatically.

---

### Slack Server

**Use case:** Channel access, messaging | **Transport:** stdio

**Environment variables:** `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID` (both required)

**Example:**
```
> Add slack server with bot token ${SLACK_BOT_TOKEN} and team ID ${SLACK_TEAM_ID}
```

---

## Advanced Configuration

### Custom Server Names

**Use case:** Multiple instances of same server type

**Syntax:**
```
> Add [server-id] server with name "[custom-name]" and [parameters]
```

**Example:**
```
> Add filesystem server with name "project-a" and path /Users/me/ProjectA
> Add filesystem server with name "project-b" and path /Users/me/ProjectB
```

---

### Environment Variable Patterns

**Direct substitution:**
```json
{"env": {"API_KEY": "${MY_API_KEY}"}}
```

**Embedded in parameters:**
```json
{"args": ["server", "postgresql://${DB_USER}:${DB_PASS}@localhost/db"]}
```

**Multiple variables:**
```json
{
  "env": {
    "TOKEN": "${SLACK_BOT_TOKEN}",
    "TEAM": "${SLACK_TEAM_ID}"
  }
}
```

---

### Profile-Specific Configuration

**Default:** `claude-desktop/default`

**Programmatic selection:**
```python
from mcp_orchestrator.mcp.tools import add_server_to_config

add_server_to_config(
    server_id="filesystem",
    params={"path": "/tmp/dev"},
    profile_id="dev"
)
```

**Note:** Conversation-based profile selection coming in Wave 2.x.

---

## Common Server Combinations

**Development Stack:**
- filesystem: /Users/me/code/myproject
- github: Repository operations
- postgres: Database access
- memory: Persistent context

**Research Workflow:**
- filesystem: /Users/me/Research
- brave-search: Web searches
- memory: Track findings

**Team Collaboration:**
- slack: Communication
- github: Code review
- filesystem: Shared docs

---

## Troubleshooting

### Error: "Server not found in registry"

**Cause:** Invalid server_id

**Solution:** `> What MCP servers are available?`

Use exact server_id from registry. For custom servers, see [Add Server to Registry](add-server-to-registry.md).

---

### Error: "Required parameter missing"

**Cause:** Missing required parameter

**Solution:** `> Describe the [server-name] server`

Then provide the parameter:
```
> Add [server-name] server with [param-name] [value]
```

---

### Error: "Server already exists in config"

**Cause:** Name collision in draft

**Solution 1 - Custom name:**
```
> Add [server-name] server with name "[custom-name]" and [parameters]
```

**Solution 2 - Remove first:**
```
> Remove [server-name] from config
> Add [server-name] server with [new-parameters]
```

---

### Draft Lost After Restart

**Cause:** Draft is in-memory, cleared on MCP server restart

**Solution:** Add and publish immediately:
```
> Add filesystem server for /Users/me/Docs
> Add memory server
> Publish the configuration
```

---

## Technical Details

### How add_server_to_config Works

1. **Validation:** Server ID checked against registry
2. **Template retrieval:** Fetch server template with metadata
3. **Parameter substitution:** Inject user values
4. **Transport detection:** Flag HTTP/SSE servers
5. **Auto-wrapping:** HTTP/SSE wrapped with mcp-remote
6. **Draft merge:** Add to in-memory draft
7. **Response:** Return updated draft

### Server Registry Structure

```json
{
  "server_id": "filesystem",
  "transport": "stdio",
  "required_params": ["path"],
  "optional_params": [],
  "env_vars": [],
  "template": { /* Claude Desktop config */ }
}
```

### Transport Abstraction

**stdio:** Direct pass-through to Claude Desktop

**HTTP/SSE:** Wrapped with mcp-remote:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/mcp-remote", "http://localhost:8080/sse"]
}
```

---

## Next Steps

1. **View draft:** `> Show me the current draft configuration`
2. **Add more servers:** Repeat this guide
3. **Publish:** See [Publish a Configuration](publish-config.md)
4. **Deploy:** See [Complete Workflow Guide](complete-workflow.md) Part 3

---

## See Also

- [Complete Workflow Guide](complete-workflow.md) - End-to-end workflow
- [Browse Available MCP Servers](browse-servers.md) - Server catalog
- [Add Server to Registry](add-server-to-registry.md) - Custom servers
- [Remove Server from Config](remove-server-from-config.md) - Remove servers
- [Reference: MCP Tools API](../reference/mcp-tools.md) - Programmatic usage

---

**Key insight:** The draft is your workspace. Add, remove, and modify servers freely before publishing. Nothing is permanent until you publish and deploy.
