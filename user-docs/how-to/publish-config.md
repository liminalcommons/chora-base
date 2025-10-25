---
title: How to Publish a Configuration
audience: Developers
prerequisites:
  - Signing keys initialized
  - Draft configuration created
related:
  - validate-config.md
  - add-server-to-config.md
  - update-config.md
---

# How to Publish a Configuration

**Goal:** Publish a validated, cryptographically signed configuration for your MCP client.

**Audience:** Developers managing MCP configurations

**Prerequisites:**
- Signing keys initialized (see [initialize_keys tool](../reference/mcp-tools.md#initialize_keys))
- At least one server added to draft configuration
- Python 3.12+ with mcp-orchestration installed

---

## Overview

Publishing a configuration:
1. Validates the draft configuration for errors
2. Signs the configuration with your Ed25519 private key
3. Stores it as a content-addressable artifact (SHA-256)
4. Updates the profile index to point to the new configuration

After publishing, the configuration can be retrieved and verified by MCP clients.

---

## Method 1: Publish via MCP Tool (Recommended)

### Step 1: View Current Draft

First, check what's in your draft configuration:

```python
result = await view_draft_config()
print(f"Draft has {result['server_count']} servers")
print(f"Servers: {', '.join(result['servers'])}")
```

**Expected output:**
```json
{
  "draft": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
      },
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
          "GITHUB_TOKEN": "ghp_..."
        }
      }
    }
  },
  "server_count": 2,
  "servers": ["filesystem", "github"]
}
```

### Step 2: Validate Configuration

**Always validate before publishing** to catch errors early:

```python
validation = await validate_config()

if not validation["valid"]:
    print("⚠️  Configuration has errors:")
    for error in validation["errors"]:
        print(f"  - [{error['code']}] {error['message']}")
    # Fix errors and try again
else:
    print("✓ Configuration is valid")
```

**Expected output (valid config):**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "server_count": 2,
  "validated_at": "2025-10-24T10:30:00Z"
}
```

**Example output (invalid config):**
```json
{
  "valid": false,
  "errors": [
    {
      "code": "EMPTY_ENV_VAR",
      "message": "Server 'github' has empty environment variable 'GITHUB_TOKEN'.",
      "severity": "error",
      "server": "github"
    }
  ],
  "server_count": 2
}
```

### Step 3: Fix Any Validation Errors

If validation fails, fix the errors:

```python
# Example: Fix missing environment variable
await add_server_to_config(
    server_id="github",
    env_vars={"GITHUB_TOKEN": "ghp_actual_token_here"}
)

# Validate again
validation = await validate_config()
assert validation["valid"] == true
```

### Step 4: Publish Configuration

Once validation passes, publish with a descriptive changelog:

```python
result = await publish_config(
    changelog="Added filesystem and github servers for development"
)

print(f"✓ Published successfully!")
print(f"  Artifact ID: {result['artifact_id']}")
print(f"  Server count: {result['server_count']}")
print(f"  Created: {result['created_at']}")
```

**Expected output:**
```json
{
  "status": "published",
  "artifact_id": "8e91a062f1c4a8ef2b5c3d9f7e6a4b1c8d2e9f0a3b5c7d1e4f6a2b8c9d0e1f2a",
  "client_id": "claude-desktop",
  "profile_id": "default",
  "server_count": 2,
  "changelog": "Added filesystem and github servers for development",
  "created_at": "2025-10-24T10:35:00Z"
}
```

### Step 5: Verify Publication

Retrieve the published configuration to verify:

```python
config = await get_config(
    client_id="claude-desktop",
    profile_id="default"
)

print(f"✓ Retrieved config {config['artifact_id'][:8]}...")
print(f"  Servers: {list(config['payload']['mcpServers'].keys())}")
print(f"  Signature valid: {config['signature_valid']}")
```

---

## Method 2: Publish via CLI

### Step 1: Prepare Configuration File

Create a JSON file with your configuration:

```bash
cat > my-config.json <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
EOF
```

### Step 2: Validate Configuration File

```bash
# Validate using the MCP tool (CLI validation coming in future wave)
python -c "
import asyncio
import json
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.servers import get_default_registry

# Load config from file
with open('my-config.json') as f:
    config = json.load(f)

# Validate (simplified check)
if 'mcpServers' not in config:
    print('ERROR: Missing mcpServers key')
    exit(1)

if not config['mcpServers']:
    print('ERROR: No servers in configuration')
    exit(1)

print('✓ Configuration structure valid')
"
```

### Step 3: Publish via CLI

```bash
mcp-orchestration publish-config \
  --client claude-desktop \
  --profile default \
  --file my-config.json \
  --changelog "Initial configuration for development environment"
```

**Expected output:**
```
✓ Configuration validated successfully
✓ Configuration signed with Ed25519
✓ Artifact stored: 8e91a062f1c4a8ef...
✓ Published successfully!

Artifact ID: 8e91a062f1c4a8ef2b5c3d9f7e6a4b1c8d2e9f0a3b5c7d1e4f6a2b8c9d0e1f2a
Client: claude-desktop
Profile: default
Server count: 2
Changelog: Initial configuration for development environment
```

---

## Complete Workflow Example

Here's a complete end-to-end workflow:

```python
# 1. Initialize keys (first time only)
keys = await initialize_keys()
print(f"✓ Keys initialized at {keys['key_dir']}")

# 2. Browse available servers
servers = await list_available_servers()
print(f"Found {servers['count']} available servers")

# 3. Add servers to draft
await add_server_to_config(
    server_id="filesystem",
    params={"path": "/Users/me/Documents"}
)

await add_server_to_config(
    server_id="github",
    env_vars={"GITHUB_TOKEN": "ghp_..."}
)

# 4. View draft
draft = await view_draft_config()
print(f"Draft has {draft['server_count']} servers")

# 5. Validate configuration
validation = await validate_config()
if not validation["valid"]:
    print("Errors found:", validation["errors"])
    # Fix errors and validate again
    raise ValueError("Configuration has validation errors")

print("✓ Configuration is valid")

# 6. Publish configuration
result = await publish_config(
    changelog="Added filesystem and github servers"
)

print(f"✓ Published successfully!")
print(f"  Artifact ID: {result['artifact_id'][:16]}...")
print(f"  Server count: {result['server_count']}")
```

---

## Troubleshooting

### Error: "Signing key not found"

**Problem:** You haven't initialized signing keys yet.

**Solution:**
```python
await initialize_keys()
```

Or via CLI:
```bash
mcp-orchestration-init-keys
```

### Error: "Cannot publish empty configuration"

**Problem:** No servers in draft configuration.

**Solution:** Add at least one server before publishing:
```python
await add_server_to_config(
    server_id="filesystem",
    params={"path": "/tmp"}
)
```

### Error: "Validation failed: MISSING_COMMAND"

**Problem:** Server configuration is corrupted or incomplete.

**Solution:** Remove and re-add the server:
```python
await remove_server_from_config(server_name="problematic-server")
await add_server_to_config(server_id="filesystem", params={...})
```

### Error: "Validation failed: TOO_MANY_SERVERS"

**Problem:** Configuration exceeds client's maximum server limit.

**Solution:** Remove some servers or use a different client:
```python
# Check client limitations
clients = await list_clients()
print(clients["clients"][0]["limitations"])

# Remove excess servers
await remove_server_from_config(server_name="extra-server")
```

### Warning: "EMPTY_ENV_VAR"

**Problem:** Environment variable is empty or whitespace-only.

**Solution:** This is a warning, not an error. The configuration is still valid, but you should provide a value:
```python
await add_server_to_config(
    server_id="github",
    env_vars={"GITHUB_TOKEN": "ghp_actual_token"}
)
```

---

## What Happens During Publishing?

1. **Validation:** The draft configuration is validated for:
   - At least one server present
   - All required fields present (command, args)
   - Valid data types
   - Client-specific limitations (max servers, max env vars)

2. **Signing:** The configuration payload is:
   - Serialized to canonical JSON
   - Signed with Ed25519 private key
   - Signature is base64-encoded

3. **Storage:** The signed artifact is:
   - Given a content-addressable ID (SHA-256 of payload)
   - Stored immutably at `~/.mcp-orchestration/artifacts/{artifact_id}.json`
   - Metadata enriched with generator, changelog, server_count

4. **Indexing:** The profile index is updated:
   - Points to the new artifact ID
   - Records update timestamp
   - Enables retrieval via `get_config`

---

## Metadata Included in Published Configs

Every published configuration includes metadata:

```json
{
  "metadata": {
    "generator": "ConfigBuilder",
    "changelog": "Your changelog message here",
    "server_count": 2
  }
}
```

This metadata helps you:
- Track what tool generated the config
- Understand what changed in this version
- Know how many servers are configured

---

## Next Steps

- [Update an existing configuration](update-config.md)
- [Verify configuration signatures](verify-signatures.md)
- [Check for configuration updates](check-config-updates.md)
- [Deploy configuration to clients](use-config.md)

---

## See Also

- [API Reference: publish_config](../reference/mcp-tools.md#publish_config)
- [API Reference: validate_config](../reference/mcp-tools.md#validate_config)
- [Explanation: Cryptographic Signing](../explanation/cryptographic-signing.md)
- [Explanation: Draft Workflow](../explanation/draft-workflow.md)
