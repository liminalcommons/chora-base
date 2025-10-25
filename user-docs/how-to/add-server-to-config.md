---
title: Add an MCP Server to Your Configuration
audience: end-users
difficulty: beginner
time: 5 minutes
wave: 1.2-1.3
version: v0.1.3
---

# Add an MCP Server to Your Configuration

**Goal:** Add an MCP server (like filesystem, GitHub, memory) to your draft configuration.

**Time:** 5 minutes per server

**Prerequisites:**
- [Get Started](get-started.md) - mcp-orchestration installed and configured
- Signing keys initialized

---

## Quick Reference

Ask Claude:

> Add [server-name] server with [parameters]

**Examples:**
- "Add filesystem server for /Users/me/Documents"
- "Add memory server"
- "Add github server" (Claude will ask for your token)

---

## Step-by-Step

### Step 1: Find the Server You Want

Ask Claude:

> What MCP servers are available?

**Or be more specific:**

> Show me servers for file access

> What database servers are available?

> Search for servers with the word "search" in their description

### Step 2: Get Server Details (Optional)

If you want to understand what a server does:

> Describe the filesystem server

This shows:
- What the server does
- What parameters it needs
- Example configuration

### Step 3: Add the Server

**For servers without parameters** (like memory):

> Add memory server

**For servers with parameters** (like filesystem):

> Add filesystem server with path /Users/me/Documents

**For servers with environment variables** (like GitHub):

> Add github server

Claude will ask: "This server needs a GITHUB_TOKEN. What should I use?"

You respond:

> Use ${GITHUB_TOKEN}

(This tells the config to read from your environment variable)

### Step 4: Verify It Was Added

> Show me the current draft configuration

You should see the server listed.

---

## Server-Specific Examples

### Filesystem Server

**Purpose:** Give Claude access to read/write files in a directory

**Parameters:** `path` (required)

**Example:**

> Add filesystem server for /Users/me/Projects

**Result:**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Projects"]
  }
}
```

---

### GitHub Server

**Purpose:** Search repos, create issues, manage PRs

**Environment variables:** `GITHUB_TOKEN` (required)

**Example:**

> Add github server with token ${GITHUB_TOKEN}

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

---

### Memory Server

**Purpose:** Key-value storage for context across conversations

**Parameters:** None

**Example:**

> Add memory server

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

### Brave Search Server

**Purpose:** Web search capabilities

**Environment variables:** `BRAVE_API_KEY` (required)

**Example:**

> Add brave search server with API key ${BRAVE_API_KEY}

**Result:**
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "${BRAVE_API_KEY}"
    }
  }
}
```

---

### PostgreSQL Server

**Purpose:** Query and manage PostgreSQL databases

**Parameters:** `connection_string` (required)

**Example:**

> Add postgres server with connection string postgresql://localhost/mydb

**Result:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
  }
}
```

---

### Slack Server

**Purpose:** Read channels, send messages

**Environment variables:** `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID` (both required)

**Example:**

> Add slack server with bot token ${SLACK_BOT_TOKEN} and team ID ${SLACK_TEAM_ID}

**Result:**
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
      "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
    }
  }
}
```

---

## Advanced Usage

### Custom Server Name

By default, the server name matches the server ID. To use a custom name:

> Add filesystem server with name "my-docs" and path /Users/me/Documents

**Result:**
```json
{
  "my-docs": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
  }
}
```

**When to use:**
- Adding the same server type multiple times (e.g., two different filesystem paths)
- Descriptive names (e.g., "work-files" vs "personal-files")

### Multiple Servers at Once

You can add multiple servers before publishing:

> Add filesystem server for /Users/me/Documents

> Add memory server

> Add github server

> Show me the draft

All three will be in your draft.

### Add to Different Profile

By default, servers are added to `claude-desktop/default`. For other profiles:

**Via API (programmatic):**
```python
add_server_to_config(
    server_id="filesystem",
    params={"path": "/tmp"},
    profile_id="dev"
)
```

**Note:** Profile selection via Claude conversation not yet supported (coming in future wave).

---

## Common Patterns

### Pattern 1: Core Toolset

Many users start with these three:

1. **Filesystem** - Access your project files
2. **Memory** - Remember context
3. **GitHub** or **Slack** - Integration with your workflow

> Add filesystem server for /Users/me/Projects

> Add memory server

> Add github server

### Pattern 2: Development Environment

For coding projects:

1. **Filesystem** - Project directory
2. **GitHub** - Source control
3. **PostgreSQL** or **SQLite** - Database

### Pattern 3: Research & Writing

For content work:

1. **Filesystem** - Document folder
2. **Brave Search** - Web research
3. **Memory** - Track research findings

---

## Troubleshooting

### "Server not found"

**Symptom:** Claude says "Server 'xyz' not found in registry"

**Solutions:**

1. **Check server ID is correct**

   > What MCP servers are available?

   Use exact server_id from the list

2. **Server might not be in registry**

   See [Add a New MCP Server to Registry](add-server-to-registry.md) to add custom servers

### "Parameter required"

**Symptom:** Error about missing required parameter

**Solutions:**

1. **Check what parameters are needed**

   > Describe the [server-name] server

2. **Provide the parameter**

   > Add [server-name] server with [param-name] [value]

### "Server already exists"

**Symptom:** Error saying server name already in config

**Solutions:**

1. **Use a different name**

   > Add [server-name] server with name "[custom-name]" and [parameters]

2. **Remove the existing server first**

   > Remove [server-name] from config

   Then add with new parameters

### Draft disappeared

**Symptom:** Added servers but `view_draft_config` shows empty

**Possible causes:**

1. **MCP server restarted** (draft is in-memory)

   Solution: Add servers again, then publish immediately

2. **Using different profile**

   Solution: Ensure consistent client_id/profile_id (defaults to claude-desktop/default)

---

## What Happens When You Add a Server?

1. **Validation** - Server ID checked against registry
2. **Parameter substitution** - Your parameters injected into server template
3. **Transport handling** - HTTP/SSE servers automatically wrapped with mcp-remote
4. **Draft update** - Server added to in-memory draft
5. **Response** - Current draft returned with server count

**The server is NOT active yet** - it's only in the draft until you [publish](publish-config.md).

---

## Next Steps

After adding servers:

1. **View your draft**

   > Show me the current draft configuration

2. **Add more servers** (repeat this guide)

3. **Publish your configuration**

   See [Publish a Configuration](publish-config.md)

4. **Remove servers you don't need**

   See [Remove a Server](remove-server-from-config.md)

---

## See Also

- [Browse Available MCP Servers](browse-servers.md) - Explore all servers
- [Remove a Server from Config](remove-server-from-config.md) - Remove unwanted servers
- [Publish a Configuration](publish-config.md) - Save your configuration
- [Add a New MCP Server to Registry](add-server-to-registry.md) - Register custom servers
- [Reference: add_server_to_config](../reference/mcp-tools.md#add_server_to_config) - API details

---

**Quick tip:** You can add, view, and remove servers as many times as you need before publishing. The draft is your workspace!
