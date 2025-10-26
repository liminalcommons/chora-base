---
title: How to Publish a Configuration
audience: Developers
prerequisites:
  - Signing keys initialized
  - Draft configuration created
related:
  - complete-workflow.md
  - validate-config.md
  - add-server-to-config.md
---

# How to Publish a Configuration

> **💡 Looking for the complete workflow?** See [Complete Workflow Guide](complete-workflow.md) for end-to-end instructions including setup, validation, publishing, and deployment.

**Goal:** Deep dive into validation, signing, and publishing workflow for MCP configurations.

**Audience:** Developers who need detailed validation error reference and publishing internals.

**Prerequisites:**
- Signing keys initialized (see [initialize_keys tool](../reference/mcp-tools.md#initialize_keys))
- At least one server added to draft configuration
- Python 3.12+ with mcp-orchestration installed

---

## Overview

Publishing transforms a draft configuration into a cryptographically signed artifact:

1. **Validation** - Checks configuration for structural errors and client limitations
2. **Signing** - Ed25519 signature over canonical JSON payload
3. **Storage** - Content-addressable artifact (SHA-256) with metadata
4. **Indexing** - Profile index updated to point to new artifact

After publishing, the configuration can be retrieved and verified by MCP clients.

---

## Publishing Methods

### Method 1: MCP Tool (Recommended)

Best for conversational workflow with Claude:

```python
# Validate
validation = await validate_config()
if not validation["valid"]:
    print(f"Errors: {validation['errors']}")
    # Fix errors, then retry

# Publish
result = await publish_config(
    changelog="Added filesystem and github servers"
)
print(f"Published: {result['artifact_id']}")
```

### Method 2: CLI (From Files)

Best for scripting and CI/CD:

```bash
# Validate (automatic on publish)
# Publish from JSON file
mcp-orchestration publish-config \
  --client claude-desktop \
  --profile default \
  --file my-config.json \
  --changelog "Initial configuration"
```

**Expected output:**
```
✓ Configuration validated successfully
✓ Configuration signed with Ed25519
✓ Artifact stored: 8e91a062f1c4a8ef...
✓ Published successfully!

Artifact ID: 8e91a062f1c4a8ef2b5c3d9f7e6a4b1c...
Server count: 2
```

---

## Validation Deep Dive

### Validation Checks

Publishing validates configurations against three categories:

#### 1. Structural Validation
- **EMPTY_CONFIG** - No servers present
- **MISSING_COMMAND** - Server lacks `command` field
- **MISSING_ARGS** - Server lacks `args` field
- **INVALID_ARGS_TYPE** - Args is not a list
- **INVALID_ENV_TYPE** - Env is not a dictionary

#### 2. Data Validation
- **EMPTY_ENV_VAR** (warning) - Environment variable is empty or whitespace-only

#### 3. Client Limitations
- **TOO_MANY_SERVERS** - Exceeds client's max server limit
- **TOO_MANY_ENV_VARS** - Server exceeds client's max env vars per server
- **UNKNOWN_CLIENT** (warning) - Client not found in registry

### Validation Error Reference

#### EMPTY_CONFIG
```json
{
  "code": "EMPTY_CONFIG",
  "message": "Configuration is empty. Add at least one server before publishing.",
  "severity": "error"
}
```

**Solution:** Add at least one server to draft.

---

#### MISSING_COMMAND / MISSING_ARGS
```json
{
  "code": "MISSING_COMMAND",
  "message": "Server 'github' is missing required 'command' field.",
  "severity": "error",
  "server": "github"
}
```

**Solution:** Server configuration is corrupted. Remove and re-add:
```python
await remove_server_from_config(server_name="github")
await add_server_to_config(server_id="github", env_vars={...})
```

---

#### INVALID_ARGS_TYPE / INVALID_ENV_TYPE
```json
{
  "code": "INVALID_ARGS_TYPE",
  "message": "Server 'filesystem' has invalid 'args' type (must be list).",
  "severity": "error",
  "server": "filesystem"
}
```

**Solution:** Fix data type. Args must be list, env must be dict.

---

#### EMPTY_ENV_VAR (Warning)
```json
{
  "code": "EMPTY_ENV_VAR",
  "message": "Server 'github' has empty environment variable 'GITHUB_TOKEN'.",
  "severity": "warning",
  "server": "github"
}
```

**Solution:** This is a warning, not an error. Configuration can still publish, but provide value:
```python
await add_server_to_config(
    server_id="github",
    env_vars={"GITHUB_TOKEN": "ghp_actual_token"}
)
```

---

#### TOO_MANY_SERVERS
```json
{
  "code": "TOO_MANY_SERVERS",
  "message": "Configuration has 25 servers, but claude-desktop supports max 20.",
  "severity": "error",
  "limit": 20,
  "actual": 25
}
```

**Solution:** Remove servers or use different client:
```python
# Check limitations
clients = await list_clients()
print(clients["clients"][0]["limitations"])

# Remove excess servers
await remove_server_from_config(server_name="extra-server")
```

---

#### TOO_MANY_ENV_VARS
```json
{
  "code": "TOO_MANY_ENV_VARS",
  "message": "Server 'database' has 15 env vars, but claude-desktop supports max 10.",
  "severity": "error",
  "server": "database",
  "limit": 10,
  "actual": 15
}
```

**Solution:** Reduce environment variables for that server.

---

## Publishing Internals

### Signing Process

1. **Canonical JSON** - Configuration payload serialized to deterministic JSON (sorted keys, no whitespace)
2. **Ed25519 Signature** - Private key signs the canonical payload
3. **Base64 Encoding** - Signature encoded for JSON storage

```python
# Simplified signing flow
canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
signature_bytes = signing_key.sign(canonical_json.encode('utf-8'))
signature_b64 = base64.b64encode(signature_bytes).decode('ascii')
```

### Artifact Structure

Published artifacts are stored at `~/.mcp-orchestration/artifacts/{artifact_id}.json`:

```json
{
  "artifact_id": "8e91a062f1c4a8ef2b5c3d9f7e6a4b1c8d2e9f0a3b5c7d1e4f6a2b8c9d0e1f2a",
  "metadata": {
    "generator": "PublishingWorkflow",
    "changelog": "Added filesystem and github servers",
    "server_count": 2
  },
  "payload": {
    "mcpServers": {
      "filesystem": { "command": "npx", "args": [...] },
      "github": { "command": "npx", "args": [...], "env": {...} }
    }
  },
  "signature": {
    "algorithm": "ed25519",
    "key_id": "default",
    "value": "base64_encoded_signature_here"
  },
  "created_at": "2025-10-24T10:35:00Z"
}
```

### Content Addressing

Artifact ID is SHA-256 hash of canonical payload:

```python
artifact_id = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
```

This ensures:
- **Immutability** - Same content always produces same ID
- **Deduplication** - Identical configs share same artifact
- **Integrity** - ID changes if payload is modified

### Metadata Enrichment

Every published config includes metadata for tracking:

- **generator** - Tool that created artifact (`PublishingWorkflow`)
- **changelog** - User-provided description of changes
- **server_count** - Number of servers in configuration
- **created_at** - ISO 8601 timestamp

---

## Advanced Publishing Scenarios

### Publishing from Existing Files

If you have an existing Claude Desktop config, publish it directly:

```bash
# Prepare your config file
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json > my-config.json

# Publish it
mcp-orchestration publish-config \
  --client claude-desktop \
  --profile default \
  --file my-config.json \
  --changelog "Imported existing configuration"
```

### Programmatic Publishing

For automation and CI/CD:

```python
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.publishing import PublishingWorkflow
from mcp_orchestrator.storage import ArtifactStore
from mcp_orchestrator.registry import ClientRegistry

# Initialize dependencies
store = ArtifactStore()
client_registry = ClientRegistry()
workflow = PublishingWorkflow(store, client_registry)

# Build configuration
builder = ConfigBuilder(client_id="claude-desktop", profile_id="default")
builder.add_server("filesystem", command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"])

# Publish
result = workflow.publish(
    builder=builder,
    private_key_path="~/.mcp-orchestration/keys/signing.key",
    signing_key_id="default",
    changelog="Automated deployment from CI/CD"
)

print(f"Published artifact: {result['artifact_id']}")
```

---

## Troubleshooting

### Publishing Failures

**Error: "Signing key not found"**

Solution:
```bash
mcp-orchestration-init-keys
```

**Error: "Cannot publish empty configuration"**

Solution: Add at least one server before publishing.

**Error: "Validation failed"**

Solution: Run `validate_config` to see specific error codes, fix errors, then retry.

### Post-Publishing Issues

**Config published but not available**

Cause: Profile index not updated.

Solution: Re-publish the configuration.

**Signature verification failed**

Cause: Artifact corrupted or keys changed.

Solution: Re-publish with current signing keys.

**Artifact ID mismatch**

Cause: Draft modified after validation.

Solution: This is expected. Validation runs on snapshot; changes after validation require re-validation.

---

## Verification After Publishing

Always verify published configurations:

```python
# Retrieve published config
config = await get_config(
    client_id="claude-desktop",
    profile_id="default"
)

# Check signature
assert config["signature_valid"] == True

# Verify content
print(f"Artifact ID: {config['artifact_id']}")
print(f"Servers: {list(config['payload']['mcpServers'].keys())}")
print(f"Server count: {config['metadata']['server_count']}")
```

---

## Next Steps

- [Deploy configuration to clients](use-config.md)
- [Update existing configuration](update-config.md)
- [Verify configuration signatures](verify-signatures.md)
- [Check for configuration updates](check-config-updates.md)

---

## See Also

- [API Reference: publish_config](../reference/mcp-tools.md#publish_config)
- [API Reference: validate_config](../reference/mcp-tools.md#validate_config)
- [Explanation: Cryptographic Signing](../explanation/cryptographic-signing.md)
- [Explanation: Draft Workflow](../explanation/draft-workflow.md)
