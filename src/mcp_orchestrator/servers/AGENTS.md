# MCP Server Catalog Guide

**Purpose:** Guide for MCP server catalog (Wave 1.1) - discovery, registration, browsing.

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **List all servers:** `registry.list_servers()` → all registered servers
- **Search servers:** `registry.search_servers(tags=["filesystem"])` → matching servers
- **Get server details:** `registry.get_server(server_id)` → full metadata
- **Register server:** `registry.register_server(metadata)` → server_id
- **CLI browse:** `mcp-orchestration servers list`
- **Testing:** `pytest tests/unit/test_servers.py`

---

## Architecture

**Path:** `src/mcp_orchestrator/servers/`

**Wave 1.1 Focus:** Server catalog for MCP server discovery

### Files

```
servers/
├── __init__.py           # Public API exports
├── catalog.py            # Server catalog operations
├── metadata.py           # Server metadata schemas
└── search.py             # Search and filtering
```

---

## Server Catalog Overview

### Purpose (Wave 1.1)

**Goal:** Enable users to discover and register available MCP servers.

**Design:** Extensible server metadata catalog with search/filter capabilities.

**Use Cases:**
1. Browse available MCP servers by category/tag
2. Search servers by capabilities (tools, resources, prompts)
3. Get installation instructions and config templates
4. Discover official vs community servers
5. Find servers for specific use cases (filesystem, database, API, etc.)

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
    "platform": "cross-platform",  # macos | windows | linux | cross-platform
    "created_at": "2025-10-24T12:00:00Z",
    "updated_at": "2025-10-24T12:00:00Z",
    "metadata": {
        "documentation": "https://docs.example.com/mcp-filesystem",
        "stability": "stable",  # experimental | beta | stable
        "verified": true  # Anthropic-verified server
    }
}
```

---

## Catalog Operations

### List All Servers

**Purpose:** Retrieve all registered servers in catalog.

```python
from mcp_orchestrator.registry import list_servers

servers = list_servers()

# Returns: List of all registered servers
# [
#   {"server_id": "mcp-filesystem", "display_name": "Filesystem Server", ...},
#   {"server_id": "mcp-database", "display_name": "Database Server", ...},
#   ...
# ]

for server in servers:
    print(f"{server['server_id']}: {server['display_name']}")
    print(f"  Tags: {', '.join(server['tags'])}")
    print(f"  Install: {server['install']['method']} install {server['install']['package']}")
```

### Search Servers

**Purpose:** Filter servers by tags, capabilities, platform, stability.

**By Tags:**
```python
from mcp_orchestrator.registry import search_servers

# Find filesystem servers
filesystem_servers = search_servers(tags=["filesystem"])

# Find official servers
official_servers = search_servers(tags=["official"])

# Multiple tags (AND logic)
official_filesystem = search_servers(tags=["official", "filesystem"])
```

**By Capabilities:**
```python
# Find servers with tool capabilities
tool_servers = search_servers(capabilities=["tools"])

# Find servers with resources
resource_servers = search_servers(capabilities=["resources"])

# Combined search
servers = search_servers(
    tags=["official"],
    capabilities=["tools", "resources"]
)
```

**By Platform:**
```python
# Find cross-platform servers
cross_platform = search_servers(platform="cross-platform")

# Find macOS-specific servers
macos_servers = search_servers(platform="macos")
```

**By Stability:**
```python
# Find stable servers only
stable_servers = search_servers(stability="stable")

# Include beta servers
beta_or_stable = search_servers(stability=["beta", "stable"])
```

**Combined Search:**
```python
# Complex query
results = search_servers(
    tags=["official", "database"],
    capabilities=["tools"],
    platform="cross-platform",
    stability="stable"
)
```

### Get Server Details

**Purpose:** Retrieve full metadata for a specific server.

```python
from mcp_orchestrator.registry import get_server

server = get_server("mcp-filesystem")

# Returns: Full server metadata
print(f"Display name: {server['display_name']}")
print(f"Description: {server['description']}")
print(f"Install method: {server['install']['method']}")
print(f"Install package: {server['install']['package']}")
print(f"Config template: {server['config_template']}")
print(f"Tools: {server['capabilities']['tools']}")
print(f"Homepage: {server['homepage']}")
```

### Register Server

**Purpose:** Add a new server to the catalog.

```python
from mcp_orchestrator.registry import register_server

server_metadata = {
    "server_id": "mcp-custom",
    "display_name": "Custom MCP Server",
    "description": "Custom server for project X",
    "author": "Your Name",
    "version": "1.0.0",
    "homepage": "https://github.com/yourname/mcp-custom",
    "repository": "https://github.com/yourname/mcp-custom",
    "license": "MIT",
    "install": {
        "method": "pip",
        "package": "mcp-custom",
        "command": "mcp-custom"
    },
    "config_template": {
        "command": "mcp-custom",
        "args": ["--mode", "production"],
        "env": {
            "CUSTOM_LOG_LEVEL": "INFO"
        }
    },
    "capabilities": {
        "tools": ["custom_tool_1", "custom_tool_2"],
        "resources": ["custom://"],
        "prompts": []
    },
    "tags": ["custom", "project-x"],
    "platform": "cross-platform",
    "metadata": {
        "documentation": "https://docs.example.com/mcp-custom",
        "stability": "beta",
        "verified": false
    }
}

server_id = register_server(server_metadata)
print(f"Registered server: {server_id}")
```

### Update Server Metadata

**Purpose:** Update existing server metadata (version bump, config changes).

```python
from mcp_orchestrator.registry import update_server

# Update existing server
updated_metadata = {
    "server_id": "mcp-custom",
    "version": "1.1.0",  # Version bump
    "install": {
        "method": "pip",
        "package": "mcp-custom",
        "command": "mcp-custom"
    },
    # ... other fields
}

update_server("mcp-custom", updated_metadata)
```

---

## CLI Commands (Wave 1.1)

### Browse Server Catalog

**List all servers:**
```bash
mcp-orchestration servers list

# Output:
# Available MCP Servers:
#
# mcp-filesystem - Filesystem Server
#   Tags: filesystem, files, official
#   Install: pip install mcp-filesystem
#
# mcp-database - Database Server
#   Tags: database, sql, official
#   Install: pip install mcp-database
```

**Search by tag:**
```bash
mcp-orchestration servers search --tag filesystem

# Output:
# Found 2 servers with tag 'filesystem':
#
# mcp-filesystem - Filesystem Server
# mcp-file-utils - File Utilities
```

**Search by capability:**
```bash
mcp-orchestration servers search --capability tools

# Output:
# Found 5 servers with 'tools' capability
```

**Show server details:**
```bash
mcp-orchestration servers show mcp-filesystem

# Output:
# Server: mcp-filesystem
# Display Name: Filesystem Server
# Description: Access local filesystem via MCP tools
# Author: Anthropic
# Version: 1.0.0
# License: MIT
#
# Installation:
#   Method: pip
#   Package: mcp-filesystem
#   Command: mcp-filesystem
#
# Configuration Template:
#   {
#     "command": "mcp-filesystem",
#     "args": ["--root", "/path/to/workspace"]
#   }
#
# Capabilities:
#   Tools: read_file, write_file, list_directory
#   Resources: file://
#
# Tags: filesystem, files, official
# Homepage: https://github.com/anthropics/mcp-filesystem
```

---

## Integration with Registry

**Server catalog is part of the registry module.**

### Catalog Storage

**Location:** `~/.mcp-orchestration/registry/servers/`

**Format:** JSON files, one per server

```
~/.mcp-orchestration/registry/servers/
├── mcp-filesystem.json
├── mcp-database.json
├── mcp-api-client.json
└── ...
```

**Example file (`mcp-filesystem.json`):**
```json
{
  "server_id": "mcp-filesystem",
  "display_name": "Filesystem Server",
  "description": "Access local filesystem via MCP tools",
  ...
}
```

### Relationship to Client Configs

**Server catalog provides templates → Client configs use templates**

```python
# 1. Get server details
server = get_server("mcp-filesystem")
config_template = server["config_template"]

# 2. Customize template
customized_config = {
    "command": config_template["command"],
    "args": ["--root", "/my/workspace"]  # Customize args
}

# 3. Add to client config artifact
artifact = {
    "client_id": "claude-desktop",
    "profile": "default",
    "payload": {
        "mcpServers": {
            "filesystem": customized_config
        }
    }
}

# 4. Save and sign
artifact_id = save_artifact(artifact)
```

---

## Common Tasks

### Task 1: Browse Official Servers

**Goal:** Find Anthropic-verified servers for production use.

```python
from mcp_orchestrator.registry import search_servers

official = search_servers(tags=["official"], stability="stable")

for server in official:
    print(f"{server['display_name']}: {server['description']}")
```

### Task 2: Add Server to Client Config

**Current approach (Wave 1.1):**

1. Browse catalog: `mcp-orchestration servers list`
2. Get server details: `mcp-orchestration servers show mcp-filesystem`
3. Copy config template
4. Manually edit client config file

**Future approach (Wave 1.2):**
```bash
# Automated server addition (planned)
mcp-orchestration config add-server \
  --client claude-desktop \
  --profile default \
  --server mcp-filesystem \
  --args "--root /workspace"
```

### Task 3: Register Custom Server

**Goal:** Add your own MCP server to the catalog.

```python
from mcp_orchestrator.registry import register_server

metadata = {
    "server_id": "my-server",
    "display_name": "My Custom Server",
    "description": "Server for my specific use case",
    "author": "Your Name",
    "version": "1.0.0",
    "homepage": "https://github.com/yourname/my-server",
    "install": {
        "method": "pip",
        "package": "my-server",
        "command": "my-server"
    },
    "config_template": {
        "command": "my-server",
        "args": []
    },
    "capabilities": {
        "tools": ["my_tool"],
        "resources": [],
        "prompts": []
    },
    "tags": ["custom"],
    "platform": "cross-platform",
    "metadata": {
        "stability": "experimental",
        "verified": false
    }
}

server_id = register_server(metadata)
print(f"Registered: {server_id}")
```

### Task 4: Update Server Version

**Goal:** Update server metadata when new version released.

```python
from mcp_orchestrator.registry import get_server, update_server

# 1. Get current metadata
server = get_server("my-server")

# 2. Update version
server["version"] = "1.1.0"
server["updated_at"] = "2025-10-24T15:00:00Z"

# 3. Save updates
update_server("my-server", server)
```

---

## Testing Server Catalog

**Coverage Target:** ≥85%

### Test Categories

1. **CRUD Operations:** Create, read, update, delete servers
```python
def test_register_and_retrieve_server():
    metadata = {...}
    server_id = register_server(metadata)

    retrieved = get_server(server_id)
    assert retrieved["server_id"] == server_id
    assert retrieved["display_name"] == metadata["display_name"]
```

2. **Search Operations:** Tag, capability, platform filtering
```python
def test_search_by_tag():
    servers = search_servers(tags=["filesystem"])
    assert all("filesystem" in s["tags"] for s in servers)

def test_search_by_capability():
    servers = search_servers(capabilities=["tools"])
    assert all("tools" in s["capabilities"] for s in servers)
```

3. **Validation:** Schema validation for server metadata
```python
def test_invalid_metadata_rejected():
    invalid = {"server_id": "test"}  # Missing required fields
    with pytest.raises(ValidationError):
        register_server(invalid)
```

4. **CLI Commands:** Command-line interface tests
```python
def test_servers_list_command():
    result = subprocess.run(
        ["mcp-orchestration", "servers", "list"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "mcp-filesystem" in result.stdout
```

5. **Integration:** Server catalog → client configs
```python
def test_server_template_used_in_config():
    server = get_server("mcp-filesystem")
    template = server["config_template"]

    # Create artifact using template
    artifact = {
        "client_id": "claude-desktop",
        "payload": {
            "mcpServers": {
                "filesystem": template
            }
        }
    }

    artifact_id = save_artifact(artifact)
    assert artifact_id is not None
```

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Server registered
emit_event("servers.server_registered", status="success",
           metadata={"server_id": server_id, "display_name": display_name})

# Server search
emit_event("servers.search_performed", status="success",
           metadata={"tags": tags, "result_count": len(results)})

# Server details retrieved
emit_event("servers.server_retrieved", status="success",
           metadata={"server_id": server_id})

# Server updated
emit_event("servers.server_updated", status="success",
           metadata={"server_id": server_id, "fields_updated": ["version"]})

# Catalog sync (future)
emit_event("servers.catalog_synced", status="success",
           metadata={"source": "remote", "new_servers": count})
```

**Create knowledge notes for:**
- Server curation decisions (which servers to include)
- Server categorization strategies (tag taxonomy)
- Popular server combinations (common config patterns)
- Server compatibility issues (client-specific quirks)

**Tag pattern:** `servers`, `catalog`, `discovery`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../registry/AGENTS.md](../registry/AGENTS.md)** - Registry (server catalog is part of registry)
- **[../mcp/AGENTS.md](../mcp/AGENTS.md)** - MCP tools (future: expose catalog via tools)
- **[../../project-docs/WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md)** - Wave 1.1 plan (server catalog focus)

---

## Common Errors & Solutions

### Error: "Server not found"

**Cause:** Server ID doesn't exist in catalog

**Solution:**
```python
# List available servers
servers = list_servers()
print([s["server_id"] for s in servers])

# Check spelling
assert "mcp-filesystem" in [s["server_id"] for s in servers]
```

### Error: "Invalid server metadata"

**Cause:** Required fields missing or invalid format

**Solution:**
```python
# Validate metadata before registering
from mcp_orchestrator.servers import validate_server_metadata

try:
    validate_server_metadata(metadata)
    register_server(metadata)
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Fix metadata fields
```

### Error: "Server already exists"

**Cause:** Attempting to register server with duplicate ID

**Solution:**
```python
# Check if server exists
try:
    existing = get_server(server_id)
    print(f"Server {server_id} already exists")
    # Use update_server instead
    update_server(server_id, new_metadata)
except ServerNotFoundError:
    # Register new server
    register_server(metadata)
```

### Error: "Config template invalid"

**Cause:** Template doesn't match client requirements

**Solution:**
```python
# Get client schema
client = get_client("claude-desktop")
schema_ref = client["schema_ref"]

# Validate template against schema
from mcp_orchestrator.servers import validate_config_template
validate_config_template(template, schema_ref)
```

---

## Future Enhancements (Wave 1.2+)

### Planned Features

**Wave 1.2:**
- Automated server installation from catalog
- Server compatibility matrix (client × server)
- Server dependency resolution

**Wave 2:**
- Remote catalog sync (pull from central registry)
- Server ratings and reviews
- Security scanning for servers

**Wave 3:**
- AI-powered server recommendations
- Automatic config optimization
- Usage analytics per server

---

**End of MCP Server Catalog Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
