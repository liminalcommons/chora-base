---
title: Manage Draft Configuration Workflow
wave: 1.3
version: v0.1.3
status: complete
last_updated: 2025-10-24
---

# How To: Manage Draft Configuration Workflow

This guide covers the ergonomic workflow for managing MCP server configurations using draft management tools. These tools were added in Wave 1.3 to improve the user experience when working with Claude Desktop.

## Objective

Learn how to:
- Initialize cryptographic signing keys
- Build configuration drafts incrementally
- View draft state at any time
- Clear drafts to start over
- Publish signed configurations

## Prerequisites

- MCP orchestration installed (`pip install mcp-orchestration`)
- MCP orchestration server added to Claude Desktop config
- Basic understanding of MCP servers

## Overview

Wave 1.3 introduces **ergonomic tools** that make configuration management more intuitive:

- **`initialize_keys`** - Generate signing keys (no CLI required!)
- **`view_draft_config`** - Inspect draft without modifying it
- **`clear_draft_config`** - Start fresh if you make mistakes
- **Default parameters** - No need to specify `client_id` and `profile_id` repeatedly

## Complete Workflow

### Step 1: Initialize Signing Keys

Before publishing configurations, you need cryptographic keys for signing artifacts.

**Using Claude Desktop:**

```
User: "Initialize the signing keys"

Claude: [calls initialize_keys tool]
```

**Expected Response:**

```json
{
  "status": "initialized",
  "key_dir": "/Users/you/.mcp-orchestration/keys",
  "public_key_path": "/Users/you/.mcp-orchestration/keys/signing.pub",
  "message": "Signing keys initialized successfully. You can now publish configurations."
}
```

**Notes:**
- Keys are stored in `~/.mcp-orchestration/keys/`
- Private key has restricted permissions (0600)
- If keys already exist, you'll get `status: "already_exists"`
- Use `regenerate=True` to recreate keys

### Step 2: Browse Available Servers

Discover what servers you can add:

```
User: "What MCP servers are available?"

Claude: [calls list_available_servers tool]
```

This shows all 15+ servers in the registry with descriptions and requirements.

### Step 3: Add Servers to Draft

Add servers one by one. The draft persists between operations:

```
User: "Add filesystem server with path /Users/me/Documents"

Claude: [calls add_server_to_config with simplified syntax]
```

**Behind the scenes:**
```python
await add_server_to_config(
    server_id="filesystem",
    params={"path": "/Users/me/Documents"}
    # client_id defaults to "claude-desktop"
    # profile_id defaults to "default"
)
```

**Response shows:**
- `status: "added"`
- `server_name: "filesystem"`
- `server_count: 1`
- Full draft configuration preview

### Step 4: View Draft State

Check what's in your draft at any time:

```
User: "Show me the current draft configuration"

Claude: [calls view_draft_config tool]
```

**Response:**
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

**Why this matters:**
- Confirms servers persist in draft
- Shows exact configuration that will be published
- Helps catch mistakes before publishing

### Step 5: Add More Servers

Continue building your configuration:

```
User: "Add memory server"

Claude: [calls add_server_to_config]
```

```
User: "Add github server with my token"

Claude: [calls add_server_to_config with env_vars]
```

### Step 6: View Draft Again (Optional)

Verify all servers are present:

```
User: "View the draft again"

Claude: [calls view_draft_config]
```

**Response shows:**
```json
{
  "server_count": 3,
  "servers": ["filesystem", "github", "memory"]
}
```

### Step 7: Publish Configuration

When satisfied, publish the draft as a signed artifact:

```
User: "Publish this configuration with changelog 'Added filesystem, github, and memory servers'"

Claude: [calls publish_config]
```

**Response:**
```json
{
  "status": "published",
  "artifact_id": "7941a154d02dae62345198ae9b858d4db2aaa8546a62fb50b8302c56ae653afd",
  "client_id": "claude-desktop",
  "profile_id": "default",
  "server_count": 3,
  "changelog": "Added filesystem, github, and memory servers",
  "created_at": "2025-10-24T23:46:34.824246Z"
}
```

**What happens:**
1. Draft is validated (not empty)
2. Configuration is signed with your private key
3. Artifact is stored in `~/.mcp-orchestration/artifacts/`
4. Content-addressable ID (SHA-256) is generated

## Recovery Workflow: Starting Over

If you make mistakes or want to start fresh:

### Clear the Draft

```
User: "Clear the draft configuration"

Claude: [calls clear_draft_config]
```

**Response:**
```json
{
  "status": "cleared",
  "previous_count": 3
}
```

All servers are removed from the draft. You can now start building again from scratch.

### Verify Draft is Empty

```
User: "View the draft"

Claude: [calls view_draft_config]
```

**Response:**
```json
{
  "draft": {"mcpServers": {}},
  "server_count": 0,
  "servers": []
}
```

## Common Patterns

### Pattern 1: Iterative Development

Build configuration incrementally with frequent checks:

1. Add server
2. View draft (verify it worked)
3. Add another server
4. View draft (confirm both present)
5. Continue...
6. Publish when satisfied

### Pattern 2: Replace Server

To replace a server with different parameters:

1. Remove the server: `remove_server_from_config(server_name="filesystem")`
2. Add it back with new params: `add_server_to_config(server_id="filesystem", params={...})`

### Pattern 3: Complete Reset

To completely start over:

1. Clear draft: `clear_draft_config()`
2. View to confirm empty: `view_draft_config()`
3. Build new configuration from scratch

## Tool Reference

### initialize_keys

```python
await initialize_keys(regenerate=False)
```

**Parameters:**
- `regenerate` (optional): If True, regenerate even if keys exist

**Returns:**
- `status`: "initialized", "already_exists", or "regenerated"
- `key_dir`: Path to keys directory
- `public_key_path`: Path to public key
- `message`: Human-readable status

**When to use:**
- First time setup
- After reinstalling mcp-orchestration
- If keys are corrupted (use `regenerate=True`)

### view_draft_config

```python
await view_draft_config(
    client_id="claude-desktop",  # default
    profile_id="default"         # default
)
```

**Parameters:**
- `client_id` (optional): Defaults to "claude-desktop"
- `profile_id` (optional): Defaults to "default"

**Returns:**
- `draft`: Complete mcpServers configuration
- `server_count`: Number of servers in draft
- `servers`: List of server names

**When to use:**
- After adding servers to verify they're present
- Before publishing to review what will be published
- To check if draft is empty

### clear_draft_config

```python
await clear_draft_config(
    client_id="claude-desktop",  # default
    profile_id="default"         # default
)
```

**Parameters:**
- `client_id` (optional): Defaults to "claude-desktop"
- `profile_id` (optional): Defaults to "default"

**Returns:**
- `status`: "cleared"
- `previous_count`: Number of servers that were removed

**When to use:**
- Made a mistake and want to start over
- Switching to a completely different server set
- Testing/experimentation

### add_server_to_config

```python
await add_server_to_config(
    server_id="filesystem",
    params={"path": "/tmp"},           # optional
    env_vars={"TOKEN": "..."},         # optional
    server_name="custom-name",         # optional
    client_id="claude-desktop",        # default
    profile_id="default"               # default
)
```

**Note:** Parameters can be passed as dict or JSON string (Claude Desktop compatibility).

### publish_config

```python
await publish_config(
    changelog="Added servers",         # optional
    client_id="claude-desktop",        # default
    profile_id="default"               # default
)
```

**Requirements:**
- Signing keys must be initialized
- Draft must not be empty (at least 1 server)

## Troubleshooting

### Error: "Signing key not found"

**Problem:** Keys haven't been initialized yet.

**Solution:** Run `initialize_keys` first.

### Error: "Cannot publish empty configuration"

**Problem:** Draft has no servers.

**Solution:** Add at least one server before publishing.

### Draft seems to disappear after adding servers

**Problem:** This shouldn't happen in MCP tools (only affects CLI).

**Solution:** Use `view_draft_config` to verify. If draft is truly empty, report a bug.

### Keys already exist, can't initialize

**Problem:** Keys were created previously.

**Solution:** This is normal. Use `initialize_keys(regenerate=True)` only if you need new keys.

## Comparison: Wave 1.2 vs Wave 1.3

### Wave 1.2 (Old Way)

```python
# Had to specify client_id and profile_id every time
await add_server_to_config(
    client_id="claude-desktop",
    profile_id="default",
    server_id="filesystem",
    params={"path": "/tmp"}
)

# No way to view draft without modifying it
# No way to clear draft
# Had to run CLI command for keys
```

### Wave 1.3 (New Way)

```python
# Simpler syntax with defaults
await add_server_to_config(
    server_id="filesystem",
    params={"path": "/tmp"}
)

# Can view draft anytime
await view_draft_config()

# Can clear draft if needed
await clear_draft_config()

# Can initialize keys from Claude
await initialize_keys()
```

## Expected Result

After completing this guide, you should be able to:
- ✅ Initialize signing keys autonomously
- ✅ Build configuration drafts incrementally
- ✅ View draft state at any point
- ✅ Clear draft and start over if needed
- ✅ Publish signed configurations
- ✅ Understand the complete workflow

## Next Steps

1. **Deploy Configuration** (Wave 1.5): Learn how to deploy published artifacts to Claude Desktop
2. **View History** (Wave 1.6): Track configuration changes over time
3. **Validate Configurations** (Wave 1.4): Validate drafts before publishing

## Reference

- Ergonomic Tools Design: [docs/wave-1-3-ergonomics.md](../wave-1-3-ergonomics.md)
- MCP Server Code: [src/mcp_orchestrator/mcp/server.py](../../src/mcp_orchestrator/mcp/server.py)
- Tests: [tests/test_mcp_ergonomic_tools.py](../../tests/test_mcp_ergonomic_tools.py)
- CHANGELOG: [CHANGELOG.md](../../CHANGELOG.md#013---2025-10-24)
