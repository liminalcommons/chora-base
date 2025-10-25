# Client & Server Registry Guide

**Purpose:** Guide for client/server registry (metadata, profiles, server catalog).

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **List clients:** `registry.list_clients()` → list of client families
- **Get profile:** `registry.get_profile(client_id, profile_id)` → profile metadata + artifact_id
- **List profiles:** `registry.list_profiles(client_id)` → profiles for client
- **Register server:** `registry.register_server(server_metadata)` → server_id
- **Search servers:** `registry.search_servers(tags=["filesystem"])` → matching servers
- **Testing:** `pytest tests/unit/test_registry.py`

---

## Architecture

**Path:** `src/mcp_orchestrator/registry/`

**Responsibilities:**
1. **Client Registry:** Metadata for MCP client families (Claude Desktop, Cursor)
2. **Profile Management:** Configuration profiles per client (default, dev, prod, custom)
3. **Server Catalog:** Available MCP servers for Wave 1.1+ (registry of servers users can add)

### Files

```
registry/
├── __init__.py           # Public API exports
├── clients.py            # Client family registry
├── profiles.py           # Profile management
└── servers.py            # MCP server catalog (Wave 1.1)
```

---

## Client Registry

### Client Family

**Definition:** Group of related MCP clients (e.g., Claude Desktop for macOS/Windows).

**Client Metadata:**
```python
{
    "client_id": "claude-desktop",
    "display_name": "Claude Desktop",
    "platform": "macos",  # macos | windows | linux | cross-platform
    "config_location": "~/Library/Application Support/Claude/claude_desktop_config.json",
    "schema_ref": "https://modelcontextprotocol.io/schemas/claude-desktop-v1.json",
    "available_profiles": ["default", "development", "production"],
    "capabilities": {
        "tools": true,
        "resources": true,
        "prompts": true,
        "sampling": false
    },
    "metadata": {
        "vendor": "Anthropic",
        "documentation": "https://docs.anthropic.com/claude/desktop",
        "version_range": ">=1.0.0"
    }
}
```

### Supported Clients (Wave 1.0)

**Claude Desktop:**
- Platform: macOS, Windows
- Config: JSON file in application support directory
- Capabilities: Full MCP support (tools, resources, prompts)

**Cursor:**
- Platform: macOS, Windows, Linux (cross-platform)
- Config: JSON file in user config directory
- Capabilities: Tools, resources

### List Clients

```python
from mcp_orchestrator.registry import list_clients

clients = list_clients()

# Returns: List of all registered client families
# [
#   {
#     "client_id": "claude-desktop",
#     "display_name": "Claude Desktop",
#     "platform": "macos",
#     "available_profiles": ["default", "development"],
#     ...
#   },
#   {
#     "client_id": "cursor",
#     "display_name": "Cursor IDE",
#     "platform": "cross-platform",
#     ...
#   }
# ]
```

### Get Client Details

```python
from mcp_orchestrator.registry import get_client

client = get_client("claude-desktop")

# Returns: Full client metadata
print(f"Platform: {client['platform']}")
print(f"Config location: {client['config_location']}")
print(f"Profiles: {client['available_profiles']}")
```

### Adding New Client Family

**Steps:**

1. **Define metadata in `clients.py`:**
```python
# registry/clients.py
CLIENTS = {
    "new-client": {
        "client_id": "new-client",
        "display_name": "New MCP Client",
        "platform": "cross-platform",
        "config_location": "~/.new-client/config.json",
        "schema_ref": "https://example.com/schema.json",
        "available_profiles": ["default"],
        "capabilities": {
            "tools": true,
            "resources": true,
            "prompts": false,
            "sampling": false
        }
    }
}
```

2. **Create default profile artifact:**
```python
from mcp_orchestrator.storage import save_artifact

default_config = {
    "client_id": "new-client",
    "profile": "default",
    "payload": {
        "mcpServers": {}  # Empty default config
    },
    "metadata": {
        "created_at": "2025-10-24T12:00:00Z",
        "version": "1.0"
    }
}

artifact_id = save_artifact(default_config)
```

3. **Register default profile:**
```python
from mcp_orchestrator.registry import register_profile

register_profile(
    client_id="new-client",
    profile_id="default",
    artifact_id=artifact_id,
    metadata={
        "description": "Default configuration for New Client"
    }
)
```

4. **Add unit tests:**
```python
# tests/unit/test_registry.py
def test_new_client_registered():
    clients = list_clients()
    new_client = [c for c in clients if c["client_id"] == "new-client"]
    assert len(new_client) == 1
    assert new_client[0]["display_name"] == "New MCP Client"
```

5. **Update documentation:**
- Add to [../../README.md](../../README.md) supported clients list
- Update [../../AGENTS.md](../../AGENTS.md) if workflow changes

---

## Profile Management

### Profile

**Definition:** Named configuration variant for a client.

**Profile Types:**
- **default:** Baseline configuration (shipped with init-configs)
- **development:** Local dev settings (debug logging, custom servers)
- **production:** Optimized for production (minimal logging, stable servers)
- **custom-\*:** User-defined profiles (e.g., custom-project-x)

### Profile Structure

```python
{
    "profile_id": "default",
    "client_id": "claude-desktop",
    "artifact_id": "aabbccddee...",  # Points to artifact in storage
    "created_at": "2025-10-24T12:00:00Z",
    "updated_at": "2025-10-24T12:00:00Z",
    "metadata": {
        "description": "Default Claude Desktop configuration",
        "tags": ["baseline", "stable"],
        "author": "mcp-orchestration",
        "version": "1.0"
    }
}
```

### Get Profile

```python
from mcp_orchestrator.registry import get_profile

profile = get_profile(
    client_id="claude-desktop",
    profile_id="default"
)

# Returns: Profile metadata + artifact_id
# {
#   "profile_id": "default",
#   "client_id": "claude-desktop",
#   "artifact_id": "aabbccddee...",
#   "created_at": "2025-10-24T12:00:00Z",
#   "metadata": {...}
# }

# Use artifact_id to retrieve actual config
from mcp_orchestrator.storage import get_artifact
artifact = get_artifact(profile["artifact_id"])
```

### List Profiles

```python
from mcp_orchestrator.registry import list_profiles

profiles = list_profiles(client_id="claude-desktop")

# Returns: List of all profiles for client
# [
#   {"profile_id": "default", "artifact_id": "aabbcc...", ...},
#   {"profile_id": "development", "artifact_id": "112233...", ...},
#   {"profile_id": "production", "artifact_id": "445566...", ...}
# ]
```

### Create New Profile

```python
from mcp_orchestrator.registry import create_profile
from mcp_orchestrator.storage import save_artifact

# 1. Create config artifact
custom_config = {
    "client_id": "claude-desktop",
    "profile": "custom-ai-research",
    "payload": {
        "mcpServers": {
            "research-tools": {
                "command": "mcp-research",
                "args": ["--mode", "advanced"]
            }
        }
    },
    "metadata": {
        "created_at": "2025-10-24T14:00:00Z"
    }
}

artifact_id = save_artifact(custom_config)

# 2. Register profile
create_profile(
    client_id="claude-desktop",
    profile_id="custom-ai-research",
    artifact_id=artifact_id,
    metadata={
        "description": "Custom config for AI research project",
        "tags": ["research", "advanced"]
    }
)
```

### Update Profile (Point to New Artifact)

```python
from mcp_orchestrator.registry import update_profile

# Profile update means pointing to new artifact
# (artifacts are immutable, so we create new one)

new_artifact_id = "updated-artifact-id..."

update_profile(
    client_id="claude-desktop",
    profile_id="default",
    artifact_id=new_artifact_id  # Point to updated artifact
)
```

---

## MCP Server Catalog (Wave 1.1)

### Purpose

**Wave 1.1 Goal:** Enable users to discover and register available MCP servers.

**Design:** Extensible server metadata catalog.

### Server Metadata Schema

```python
{
    "server_id": "mcp-filesystem",
    "display_name": "Filesystem Server",
    "description": "Access local filesystem via MCP tools",
    "author": "Anthropic",
    "version": "1.0.0",
    "homepage": "https://github.com/anthropics/mcp-filesystem",
    "repository": "https://github.com/anthropics/mcp-filesystem",
    "license": "MIT",
    "install": {
        "method": "pip",  # pip | npm | docker | binary
        "package": "mcp-filesystem",
        "command": "mcp-filesystem"
    },
    "config_template": {
        "command": "mcp-filesystem",
        "args": ["--root", "/path/to/workspace"],
        "env": {
            "FS_LOG_LEVEL": "INFO"
        }
    },
    "capabilities": {
        "tools": ["read_file", "write_file", "list_directory"],
        "resources": ["file://"],
        "prompts": []
    },
    "tags": ["filesystem", "files", "official"],
    "created_at": "2025-10-24T12:00:00Z",
    "updated_at": "2025-10-24T12:00:00Z"
}
```

### List All Servers

```python
from mcp_orchestrator.registry import list_servers

servers = list_servers()

# Returns: List of all registered servers
for server in servers:
    print(f"{server['server_id']}: {server['display_name']}")
```

### Search Servers

```python
from mcp_orchestrator.registry import search_servers

# By tags
filesystem_servers = search_servers(tags=["filesystem"])

# By capabilities
tool_servers = search_servers(capabilities=["tools"])

# Combined
official_filesystem = search_servers(
    tags=["official", "filesystem"],
    capabilities=["tools"]
)

# Returns: Matching servers
```

### Get Server Details

```python
from mcp_orchestrator.registry import get_server

server = get_server("mcp-filesystem")

# Returns: Full server metadata
print(f"Install: {server['install']['method']} install {server['install']['package']}")
print(f"Config template: {server['config_template']}")
```

### Register Server

```python
from mcp_orchestrator.registry import register_server

server_metadata = {
    "server_id": "mcp-custom",
    "display_name": "Custom MCP Server",
    "description": "Custom server for project X",
    "author": "Your Name",
    "version": "1.0.0",
    "homepage": "https://github.com/yourname/mcp-custom",
    "install": {
        "method": "pip",
        "package": "mcp-custom",
        "command": "mcp-custom"
    },
    "config_template": {
        "command": "mcp-custom",
        "args": []
    },
    "capabilities": {
        "tools": ["custom_tool_1", "custom_tool_2"],
        "resources": [],
        "prompts": []
    },
    "tags": ["custom", "project-x"]
}

server_id = register_server(server_metadata)
print(f"Registered: {server_id}")
```

---

## Common Tasks

### Browse Server Catalog (CLI)

```bash
# List all servers
mcp-orchestration servers list

# Search by tag
mcp-orchestration servers search --tag filesystem

# Show server details
mcp-orchestration servers show mcp-filesystem
```

### Add Server to Client Config

**Manual (current Wave 1.0):**
1. Get server metadata: `mcp-orchestration servers show mcp-filesystem`
2. Copy config template
3. Edit client config file manually

**Automated (future Wave 1.2):**
```bash
# Future: Add server to config
mcp-orchestration config add-server \
  --client claude-desktop \
  --profile default \
  --server mcp-filesystem \
  --args "--root /workspace"
```

---

## Testing Registry Operations

**Coverage Target:** ≥85%

### Test Categories

1. **Client CRUD:** Add, list, update, delete clients
```python
def test_list_clients_returns_all_registered():
    clients = list_clients()
    assert len(clients) >= 2  # claude-desktop, cursor
    assert all("client_id" in c for c in clients)
```

2. **Profile CRUD:** Create, retrieve, update profiles
```python
def test_create_and_retrieve_profile():
    create_profile("claude-desktop", "test-profile", "artifact-id-123")
    profile = get_profile("claude-desktop", "test-profile")
    assert profile["artifact_id"] == "artifact-id-123"
```

3. **Server Catalog:** Register, search, retrieve servers
```python
def test_search_servers_by_tag():
    servers = search_servers(tags=["filesystem"])
    assert all("filesystem" in s["tags"] for s in servers)
```

4. **Validation:** Schema validation for clients/profiles/servers
```python
def test_invalid_client_metadata_rejected():
    invalid_client = {"client_id": "invalid"}  # Missing required fields
    with pytest.raises(ValidationError):
        register_client(invalid_client)
```

5. **Integration:** Profile points to valid artifact
```python
def test_profile_points_to_valid_artifact():
    profile = get_profile("claude-desktop", "default")
    artifact_id = profile["artifact_id"]

    # Artifact must exist in storage
    from mcp_orchestrator.storage import get_artifact
    artifact = get_artifact(artifact_id)
    assert artifact is not None
    assert artifact["client_id"] == "claude-desktop"
```

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Client registered
emit_event("registry.client_added", status="success",
           metadata={"client_id": client_id})

# Profile created
emit_event("registry.profile_created", status="success",
           metadata={"client_id": client_id, "profile_id": profile_id})

# Server catalog updated
emit_event("registry.server_registered", status="success",
           metadata={"server_id": server_id})

# Profile updated (artifact pointer changed)
emit_event("registry.profile_updated", status="success",
           metadata={"client_id": client_id, "profile_id": profile_id,
                     "old_artifact_id": old_id, "new_artifact_id": new_id})
```

**Create knowledge notes for:**
- New client integration patterns
- Profile management strategies
- Server catalog curation decisions

**Tag pattern:** `registry`, `clients`, `profiles`, `servers`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../storage/AGENTS.md](../storage/AGENTS.md)** - Artifact storage (profiles point to artifacts)
- **[../mcp/AGENTS.md](../mcp/AGENTS.md)** - MCP tools (list_clients, list_profiles expose registry)
- **[../servers/AGENTS.md](../servers/AGENTS.md)** - Server registry deep dive (Wave 1.1 focus)
- **[../../project-docs/WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md)** - Wave 1.1 plan (server catalog)

---

## Common Errors & Solutions

### Error: "Client not found"

**Cause:** Client ID doesn't exist in registry

**Solution:**
```python
# List available clients
clients = list_clients()
print([c["client_id"] for c in clients])

# Check spelling
assert "claude-desktop" in [c["client_id"] for c in clients]
```

### Error: "Profile not found"

**Cause:** Profile ID doesn't exist for client

**Solution:**
```python
# List profiles for client
profiles = list_profiles("claude-desktop")
print([p["profile_id"] for p in profiles])

# Create profile if missing
create_profile("claude-desktop", "missing-profile", artifact_id)
```

### Error: "Artifact not found for profile"

**Cause:** Profile points to non-existent artifact_id

**Solution:**
```python
profile = get_profile("claude-desktop", "default")
artifact_id = profile["artifact_id"]

# Verify artifact exists
from mcp_orchestrator.storage import get_artifact
try:
    artifact = get_artifact(artifact_id)
except ArtifactNotFoundError:
    print(f"Profile points to missing artifact: {artifact_id}")
    # Fix by updating profile to valid artifact
    update_profile("claude-desktop", "default", new_artifact_id)
```

---

**End of Client & Server Registry Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
