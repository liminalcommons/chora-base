---
title: MCP Tools API Reference
version: v0.1.3
wave: 1.0-1.3
last_updated: 2025-10-24
---

# MCP Tools API Reference

Complete reference for all MCP tools provided by mcp-orchestration server (v0.1.3).

## Tool Categories

- [Client & Profile Management](#client--profile-management) (4 tools)
- [Server Registry](#server-registry) (2 tools)
- [Configuration Building](#configuration-building) (6 tools)
- [Key Management](#key-management) (1 tool)

---

## Client & Profile Management

### list_clients

List supported MCP client families.

**Parameters:** None

**Returns:**
```typescript
{
  clients: Array<{
    client_id: string           // e.g., "claude-desktop"
    display_name: string        // e.g., "Claude Desktop"
    platform: string           // e.g., "macos"
    config_location: string    // File path to config
    available_profiles: string[] // e.g., ["default", "dev"]
  }>,
  count: number                // Total number of clients
}
```

**Performance:** p95 < 200ms

**Example:**
```json
{
  "clients": [
    {
      "client_id": "claude-desktop",
      "display_name": "Claude Desktop",
      "platform": "macos",
      "config_location": "~/Library/Application Support/Claude/claude_desktop_config.json",
      "available_profiles": ["default", "dev", "prod"]
    }
  ],
  "count": 1
}
```

---

### list_profiles

List available configuration profiles for a client.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_id` | string | Yes | Client family identifier (e.g., "claude-desktop") |

**Returns:**
```typescript
{
  client_id: string
  profiles: Array<{
    profile_id: string           // e.g., "default"
    display_name: string         // e.g., "Default Profile"
    description: string
    latest_artifact_id: string | null  // SHA-256 hash
    updated_at: string | null    // ISO 8601 timestamp
  }>,
  count: number
}
```

**Errors:**
- `ValueError`: Client not found

**Example:**
```json
{
  "client_id": "claude-desktop",
  "profiles": [
    {
      "profile_id": "default",
      "display_name": "Default Profile",
      "description": "Standard configuration",
      "latest_artifact_id": "8e91a062...",
      "updated_at": "2025-10-24T12:00:00Z"
    }
  ],
  "count": 1
}
```

---

### get_config

Retrieve signed configuration artifact.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `client_id` | string | Yes | - | Client family identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |
| `artifact_id` | string | No | `null` | Specific artifact hash (or latest if null) |

**Returns:**
```typescript
{
  artifact_id: string          // SHA-256 content address
  client_id: string
  profile_id: string
  created_at: string           // ISO 8601 timestamp
  payload: {
    mcpServers: {              // Client configuration
      [serverName: string]: {
        command: string
        args: string[]
        env?: Record<string, string>
      }
    }
  }
  signature: string            // Base64-encoded Ed25519 signature
  signing_key_id: string       // Key identifier
  metadata: {
    generator: string
    changelog?: string
  }
}
```

**Performance:** p95 < 300ms

**Errors:**
- `ValueError`: Client/profile/artifact not found

---

### diff_config

Compare configurations and detect updates.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `client_id` | string | Yes | - | Client family identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |
| `local_artifact_id` | string | No | `null` | SHA-256 hash of local config |
| `local_payload` | object | No | `null` | Local configuration payload |

**Note:** Must provide either `local_artifact_id` or `local_payload`.

**Returns:**
```typescript
{
  status: "up-to-date" | "outdated" | "diverged" | "unknown"
  local_artifact_id: string
  remote_artifact_id: string
  diff: {
    servers_added: string[]
    servers_removed: string[]
    servers_modified: Array<{
      server_name: string
      changes: Array<{
        field: string
        old_value: any
        new_value: any
      }>
    }>
    servers_unchanged: string[]
  }
  summary: {
    total_changes: number
    added_count: number
    removed_count: number
    modified_count: number
  }
  recommendation: string      // Human-readable action
}
```

**Performance:** p95 < 200ms

**Errors:**
- `ValueError`: Client not found or invalid parameters

---

## Server Registry

### list_available_servers

List all MCP servers in the registry.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `transport_filter` | string | No | `null` | Filter by transport: "stdio", "http", "sse" |
| `search_query` | string | No | `null` | Search name, description, tags |

**Returns:**
```typescript
{
  servers: Array<{
    server_id: string           // e.g., "filesystem"
    display_name: string        // e.g., "Filesystem Access"
    description: string
    transport: "stdio" | "http" | "sse"
    npm_package: string | null  // NPM package name
    tags: string[]             // e.g., ["files", "storage"]
    has_parameters: boolean    // Requires configuration
    requires_env: string[]     // Required env vars
  }>,
  count: number
  transport_counts: {
    stdio: number
    http: number
    sse: number
  }
  available_transports: string[]
}
```

**Example:**
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
      "has_parameters": true,
      "requires_env": []
    }
  ],
  "count": 15,
  "transport_counts": { "stdio": 13, "http": 1, "sse": 1 },
  "available_transports": ["stdio", "http", "sse"]
}
```

---

### describe_server

Get detailed information about a specific MCP server.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `server_id` | string | Yes | Server identifier (e.g., "filesystem") |

**Returns:**
```typescript
{
  server_id: string
  display_name: string
  description: string
  transport: {
    type: "stdio" | "http" | "sse"
    command?: string           // For stdio
    args?: string[]            // For stdio
    url?: string              // For http/sse
    auth_type?: string        // For http/sse
    note?: string             // Implementation notes
  }
  parameters: Array<{
    name: string
    type: string              // e.g., "path", "string", "number"
    description: string
    required: boolean
    default: any | null
    example: any | null
  }>
  env_vars: {
    required: string[]
    optional: string[]
  }
  installation: {
    npm_package: string
    install_command: string
    note: string
  } | {}
  documentation_url: string | null
  tags: string[]
  usage_example: string      // JSON string
}
```

**Errors:**
- `ValueError`: Server not found

---

## Configuration Building

### add_server_to_config

Add a server to the draft configuration.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `server_id` | string | Yes | - | Server from registry |
| `params` | object\|string | No | `null` | Parameter values (dict or JSON string) |
| `env_vars` | object\|string | No | `null` | Environment variables (dict or JSON string) |
| `server_name` | string | No | `server_id` | Custom name in config |
| `client_id` | string | No | `"claude-desktop"` | Client identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |

**Note:** `params` and `env_vars` accept both dict objects and JSON strings (Claude Desktop compatibility).

**Returns:**
```typescript
{
  status: "added"
  server_name: string
  draft: {
    mcpServers: {
      [name: string]: {
        command: string
        args: string[]
        env?: Record<string, string>
      }
    }
  }
  server_count: number
}
```

**Errors:**
- `ValueError`: Server not found or invalid parameters

**Example:**
```typescript
await add_server_to_config(
  server_id="filesystem",
  params={"path": "/Users/me/Documents"}
)
```

---

### remove_server_from_config

Remove a server from the draft configuration.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `server_name` | string | Yes | - | Server name in config |
| `client_id` | string | No | `"claude-desktop"` | Client identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |

**Returns:**
```typescript
{
  status: "removed"
  server_name: string
  draft: { mcpServers: {...} }
  server_count: number
}
```

**Errors:**
- `ValueError`: Server not found in draft

---

### view_draft_config

View current draft configuration without modifying it.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `client_id` | string | No | `"claude-desktop"` | Client identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |

**Returns:**
```typescript
{
  draft: { mcpServers: {...} }
  server_count: number
  servers: string[]          // Server names
}
```

**Example:**
```json
{
  "draft": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
      }
    }
  },
  "server_count": 1,
  "servers": ["filesystem"]
}
```

---

### clear_draft_config

Clear all servers from the draft configuration.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `client_id` | string | No | `"claude-desktop"` | Client identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |

**Returns:**
```typescript
{
  status: "cleared"
  previous_count: number     // Servers removed
}
```

---

### publish_config

Publish draft configuration as signed artifact.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `changelog` | string | No | `null` | Description of changes |
| `client_id` | string | No | `"claude-desktop"` | Client identifier |
| `profile_id` | string | No | `"default"` | Profile identifier |

**Prerequisites:** Signing keys must be initialized (use [initialize_keys](#initialize_keys)).

**Returns:**
```typescript
{
  status: "published"
  artifact_id: string        // SHA-256 content address
  client_id: string
  profile_id: string
  server_count: number
  changelog: string | null
  created_at: string         // ISO 8601 timestamp
}
```

**Errors:**
- `ValueError`: Draft empty, signing keys not found, or publishing fails

**Example:**
```typescript
await publish_config(
  changelog="Added filesystem and github servers"
)
```

---

## Key Management

### initialize_keys

Initialize Ed25519 signing keys for cryptographic artifact signing.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `regenerate` | boolean | No | `false` | Regenerate if keys exist |

**Returns:**
```typescript
{
  status: "initialized" | "already_exists" | "regenerated"
  key_dir: string           // Directory path
  public_key_path: string   // Public key file path
  message: string           // Status message
}
```

**Side Effects:**
- Creates `~/.mcp-orchestration/keys/` directory
- Generates `signing.key` (private, mode 0600)
- Generates `signing.pub` (public)

**Example:**
```json
{
  "status": "initialized",
  "key_dir": "/Users/me/.mcp-orchestration/keys",
  "public_key_path": "/Users/me/.mcp-orchestration/keys/signing.pub",
  "message": "Signing keys initialized successfully. You can now publish configurations."
}
```

---

## Common Patterns

### Complete Configuration Workflow

```typescript
// 1. Initialize keys (first time only)
await initialize_keys()

// 2. Browse available servers
const servers = await list_available_servers()

// 3. Get server details
const details = await describe_server(server_id="filesystem")

// 4. Add servers to draft
await add_server_to_config(
  server_id="filesystem",
  params={"path": "/Users/me/Documents"}
)

// 5. View draft
const draft = await view_draft_config()

// 6. Publish signed config
await publish_config(
  changelog="Added filesystem server"
)
```

### Check for Updates

```typescript
// Get local config
const local = await get_config(
  client_id="claude-desktop",
  profile_id="default"
)

// Compare with remote
const diff = await diff_config(
  client_id="claude-desktop",
  profile_id="default",
  local_payload=local.payload
)

// Check status
if (diff.status === "outdated") {
  console.log(diff.recommendation)
}
```

---

## Wave History

- **Wave 1.0 (v0.1.0)**: list_clients, list_profiles, get_config, diff_config
- **Wave 1.1 (v0.1.1)**: list_available_servers, describe_server
- **Wave 1.2 (v0.1.2)**: add_server_to_config, remove_server_from_config, publish_config
- **Wave 1.3 (v0.1.3)**: view_draft_config, clear_draft_config, initialize_keys + default parameters

---

## See Also

- [Tutorial: Your First Configuration](../tutorials/01-first-configuration.md) - Learn by doing
- [How-To: Manage Configs with Claude](../how-to/manage-configs-with-claude.md) - Task-oriented guide
- [Explanation: Cryptographic Signing](../explanation/cryptographic-signing.md) - Understand signatures
- [CLI Commands Reference](cli-commands.md) - Command-line tools
