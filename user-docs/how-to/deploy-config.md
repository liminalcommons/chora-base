# How to Deploy Configurations

> **💡 New to deployment?** See [Complete Workflow Guide](complete-workflow.md) for step-by-step instructions covering installation, building configurations, and your first deployment.

This guide provides a **deep dive into deployment** - the process of applying published configurations to MCP clients like Claude Desktop or Cursor.

## Overview

Deployment takes a signed, published configuration and writes it to your client's config file location. This guide covers:

1. How deployment works (internals)
2. Deploy via MCP tool vs CLI
3. Version pinning and rollback
4. Query deployed vs latest (drift detection)
5. Troubleshooting deployment issues

**Prerequisites:**
- [Initialized signing keys](get-started.md#initialize-keys)
- [Published configuration](publish-config.md)

---

## How Deployment Works

Understanding deployment internals helps troubleshoot issues and use advanced features.

### The Deployment Process

1. **Resolve Artifact**
   - If `artifact_id` specified → use that specific version
   - If not specified → fetch latest artifact for client/profile

2. **Verify Signature**
   - Load artifact from `~/.mcp-orchestration/artifacts/{artifact_id}.json`
   - Verify Ed25519 signature using public key
   - **Reject deployment if signature invalid** (prevents tampering)

3. **Resolve Config Path**
   - Lookup client in registry to get `config_location`
   - Expand `~` to actual home directory
   - Create parent directories if needed

4. **Write Atomically**
   - Write to temporary file: `{config_path}.tmp`
   - Verify write succeeded
   - Rename to final location (atomic operation)
   - On failure → rollback (delete temp file)

5. **Log Deployment**
   - Record to `~/.mcp-orchestration/deployments/{client_id}/{profile_id}.json`
   - Include artifact_id, timestamp, config_path, changelog

### Atomic Guarantees

Deployment is **all-or-nothing**:

- ✅ **Success:** Config written, deployment logged
- ❌ **Failure:** No partial writes, original config untouched

**Rollback scenarios:**
- Signature verification fails → no write
- Disk write fails → temp file deleted
- Permission denied → no changes

This prevents corrupt configuration files that could break your client.

---

## Deploy Latest Configuration

Deploy the most recent published configuration.

### Via MCP Tool (from Claude Desktop)

```python
result = await deploy_config(
    client_id="claude-desktop",
    profile_id="default"
    # artifact_id omitted → deploys latest
)
```

**Response:**
```json
{
  "status": "deployed",
  "config_path": "/Users/you/Library/Application Support/Claude/claude_desktop_config.json",
  "artifact_id": "abc123...",
  "deployed_at": "2025-10-25T14:30:00Z"
}
```

**Restart required:** Claude Desktop must be restarted to load new configuration.

```bash
# macOS
killall Claude && open -a "Claude"
```

---

### Via CLI (from terminal)

```bash
mcp-orchestration deploy-config \
  --client claude-desktop \
  --profile default
```

**Output:**
```
✓ Configuration deployed successfully!

Artifact ID: abc123...
Config path: /Users/you/Library/Application Support/Claude/claude_desktop_config.json
Deployed at: 2025-10-25T14:30:00Z

⚠️  Restart the client application for changes to take effect
```

**JSON output (for scripting):**
```bash
mcp-orchestration deploy-config \
  --client claude-desktop \
  --profile default \
  --format json
```

Returns structured JSON for parsing in scripts or CI/CD pipelines.

---

## Deploy Specific Version (Version Pinning)

Deploy a specific artifact instead of latest. Useful for rollback or testing older configurations.

### Step 1: Identify Artifact ID

You need the artifact ID from a previous publish operation. Example:

```
v1: abc123... (initial config)
v2: def456... (added github)
v3: ghi789... (current latest)
```

**Note:** Wave 1.6 will add `list_deployment_history` tool. For now, track artifact IDs manually from publish output.

---

### Step 2: Deploy Specific Version

**Via MCP Tool:**
```python
result = await deploy_config(
    client_id="claude-desktop",
    profile_id="default",
    artifact_id="abc123..."  # Pin to specific version
)
```

**Via CLI:**
```bash
mcp-orchestration deploy-config \
  --client claude-desktop \
  --profile default \
  --artifact-id abc123...
```

---

### Step 3: Verify Correct Version

```python
# Query what's currently deployed
deployed = await get_config(
    client_id="claude-desktop",
    profile_id="default",
    source="deployed"
)

print(f"Deployed artifact: {deployed['artifact_id']}")  # abc123...
```

**Or via resource URI:**
```python
deployed = await get_resource("config://claude-desktop/default/deployed")
latest = await get_resource("config://claude-desktop/default/latest")

print(f"Deployed: {deployed['artifact_id']}")
print(f"Latest:   {latest['artifact_id']}")
```

---

## Detect Configuration Drift

**Drift** occurs when the deployed configuration differs from the latest published version.

### Quick Check

```python
deployed = await get_resource("config://claude-desktop/default/deployed")
latest = await get_resource("config://claude-desktop/default/latest")

if deployed['artifact_id'] != latest['artifact_id']:
    print("⚠️ Configuration drift detected!")
    print(f"  Deployed: {deployed['artifact_id']}")
    print(f"  Latest:   {latest['artifact_id']}")
else:
    print("✓ Deployed configuration is up-to-date")
```

**Fix drift:**
```python
# Deploy latest to sync
await deploy_config(client_id="claude-desktop", profile_id="default")
```

**Via CLI:**
```bash
# Check for drift
mcp-orchestration diff-config claude-desktop default

# Deploy if drift detected
mcp-orchestration deploy-config --client claude-desktop --profile default
```

---

## What Gets Written to Disk

Deployment writes the **payload** from your signed artifact directly to the client's config location.

**Example output (Claude Desktop):**

File: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/me/Documents"
      ]
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
```

**Note:** The `mcp-orchestration` server itself is NOT included in deployed configs. You must manually add it to your initial Claude Desktop config for the tools to work.

---

## Deployment Log Format

Each deployment is logged for audit and history tracking.

**File:** `~/.mcp-orchestration/deployments/claude-desktop/default.json`

```json
{
  "client_id": "claude-desktop",
  "profile_id": "default",
  "current_deployment": {
    "artifact_id": "abc123...",
    "config_path": "/Users/me/Library/Application Support/Claude/claude_desktop_config.json",
    "deployed_at": "2025-10-25T14:30:00Z",
    "changelog": "Added filesystem and github servers"
  },
  "history": [
    {
      "artifact_id": "def456...",
      "deployed_at": "2025-10-24T10:15:00Z",
      "changelog": "Initial setup"
    }
  ]
}
```

Wave 1.6 will add tools to query this history directly.

---

## Troubleshooting

### Error: "Client 'xxx' not found in registry"

**Cause:** Invalid client_id.

**Solution:** Use `list_clients()` to see valid clients. Supported: `claude-desktop`, `cursor`

---

### Error: "Artifact 'xxx' not found"

**Cause:** Specified artifact_id doesn't exist.

**Solution:** Omit `artifact_id` to deploy latest, or verify ID from publish output.

---

### Error: "Signature verification failed"

**Cause:** Artifact signature is invalid (corrupted storage or tampering detected).

**Solution:**

1. Re-publish configuration:
```python
published = await publish_config(changelog="Re-published due to signature issue")
```

2. Deploy newly published artifact:
```python
await deploy_config()
```

**Prevention:** Ensure `~/.mcp-orchestration/` directory has correct permissions and isn't modified externally.

---

### Error: "Permission denied" (WRITE_FAILED)

**Cause:** No write permission to config file or parent directory.

**Solution:**
```bash
# macOS (Claude Desktop)
chmod 755 ~/Library/Application\ Support/Claude/

# Linux (Cursor)
chmod 755 ~/.cursor/
```

---

### Parent Directory Doesn't Exist

**Automatic Fix:** Deployment creates parent directories automatically.

If issues persist, manually create:
```bash
mkdir -p ~/Library/Application\ Support/Claude/  # macOS
mkdir -p ~/.cursor/                               # Linux
```

---

### Config Deployed But Client Doesn't See Changes

**Cause:** Client hasn't reloaded configuration.

**Solution (restart client):**
- **Claude Desktop (macOS):** `killall Claude && open -a "Claude"`
- **Claude Desktop (Windows):** Close completely, reopen from Start menu
- **Cursor:** Command Palette → "Developer: Reload Window"

Then verify servers: `"What MCP servers do I have available?"`

If still not visible: Check config file exists, verify JSON valid, check client logs.

---

## Advanced Scenarios

### Deploy to Multiple Clients

```bash
mcp-orchestration deploy-config --client claude-desktop --profile default
mcp-orchestration deploy-config --client cursor --profile default
```

Each client gets appropriate config location automatically.

---

### Scripted Deployments

```bash
#!/bin/bash
mcp-orchestration deploy-config \
  --client claude-desktop --profile default \
  --artifact-id "$ARTIFACT_ID" \
  --format json > result.json

[ $? -eq 0 ] && echo "✓ Deployed" || echo "✗ Failed"
```

---

### Profile-Based Deployments

```bash
mcp-orchestration deploy-config --client claude-desktop --profile dev
mcp-orchestration deploy-config --client claude-desktop --profile prod
```

Note: Each profile overwrites the same config location.

---

## Related Guides

- [Complete Workflow](complete-workflow.md) - End-to-end walkthrough including deployment
- [Publish Config](publish-config.md) - Create signed configurations for deployment
- [Get Started](get-started.md) - Initialize keys and first-time setup

**Reference:**
- [MCP Tools API](../reference/mcp-tools.md) - Complete API specifications
- [Cryptographic Signing](../explanation/cryptographic-signing.md) - How signatures protect deployments

---

## Next Steps

After successful deployment:

1. **Restart client** to load new configuration
2. **Verify servers** by testing tools from deployed servers
3. **Monitor drift** periodically to detect when deployed differs from latest
4. **Track artifact IDs** for rollback capability (until Wave 1.6 adds history tools)

**Ongoing workflow:**
- Update config (add/remove servers)
- Validate → Publish → Deploy
- Restart client
- Test changes

This ensures your MCP client always has the latest, validated configuration.
