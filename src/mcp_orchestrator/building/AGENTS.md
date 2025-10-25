# AGENTS.md - Config Building Module

This file provides machine-readable instructions for AI agents working on the `mcp_orchestrator.building` module.

---

## Module Overview

**Purpose:** Draft configuration management and building for MCP client configurations

The `building` module provides the `ConfigBuilder` class, which implements the **draft → view → publish pattern** introduced in Wave 1.2. This pattern enables users (via Claude Desktop or other MCP clients) to iteratively construct configurations before publishing them as signed artifacts.

**Wave Context:**
- **Wave 1.2 (v0.1.2):** ConfigBuilder introduced, 3 new MCP tools (add_server_to_config, remove_server_from_config, publish_config)
- **Wave 1.3 (v0.1.3):** Ergonomic improvements (view_draft_config, clear_draft_config, default client/profile parameters)

**Key Responsibilities:**
- Manage in-memory draft state (add/remove servers)
- Integrate with ServerRegistry for server definitions
- Build final `mcpServers` payload
- Convert draft to signed `ConfigArtifact` (integrates with crypto + storage layers)

---

## Key Components

### ConfigBuilder Class

**Location:** `src/mcp_orchestrator/building/builder.py`

**Core Methods:**
- `add_server(server_id, params, env_vars, server_name)` - Add server from registry to draft
- `remove_server(server_name)` - Remove server from draft
- `clear()` - Remove all servers from draft
- `build()` - Generate `{"mcpServers": {...}}` payload
- `to_artifact(signing_key_id, private_key_path, changelog)` - Convert draft to signed ConfigArtifact

**State Management:**
- `_servers: dict[str, dict]` - In-memory draft (server_name → config)
- `client_id: str` - Target client family (e.g., "claude-desktop")
- `profile_id: str` - Target profile (e.g., "default", "dev")
- `_registry: ServerRegistry` - Server definitions catalog

**Custom Exceptions:**
- `ServerAlreadyAddedError` - Raised when adding duplicate server_name
- `ServerNotInConfigError` - Raised when removing non-existent server

---

## Code Style & Patterns

### Draft-Publish Pattern

**Philosophy:** Separate draft construction (mutable) from publishing (immutable)

```python
# GOOD: Draft → Build → Publish (Wave 1.2+ pattern)
builder = ConfigBuilder("claude-desktop", "default")
builder.add_server("filesystem", params={"path": "/docs"})
builder.add_server("memory")
artifact = builder.to_artifact(
    signing_key_id="prod-key",
    private_key_path="~/.mcp-orchestration/keys/signing.key",
    changelog="Initial config"
)
store.save(artifact)

# BAD: Direct artifact creation (bypasses draft workflow)
# Don't create ConfigArtifact directly - use ConfigBuilder.to_artifact()
```

### Error Handling

**Validation Errors:** Raised during `add_server()` if:
- `ServerNotFoundError` - server_id not in registry
- `ValueError` - Required parameters missing
- `ServerAlreadyAddedError` - server_name already in draft

**Recovery Pattern:**
```python
try:
    builder.add_server("github", env_vars={"GITHUB_TOKEN": token})
except ServerAlreadyAddedError:
    # Server exists - either remove first or use different server_name
    builder.remove_server("github")
    builder.add_server("github", env_vars={"GITHUB_TOKEN": token})
except ServerNotFoundError:
    # Registry doesn't have "github" - check registry.list_servers()
    available = registry.list_servers()
    raise ValueError(f"Unknown server. Available: {available}")
```

### Transport Abstraction

**Integration with ServerRegistry:**

ConfigBuilder delegates transport configuration to `ServerRegistry.to_client_config()`:
- **Stdio servers:** Command + args directly in config
- **HTTP/SSE servers:** Wrapped with mcp-remote (transparent to users)

```python
# ConfigBuilder calls registry.to_client_config() internally
config = self._registry.to_client_config(
    server_id="filesystem",
    params={"path": "/docs"},
    env_vars=None,
    server_name="filesystem"
)
# Returns: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/docs"]}
```

**Implication:** When modifying ConfigBuilder, do NOT handle transport logic here. Delegate to ServerRegistry.

---

## Testing Instructions

### Unit Tests

**Location:** `tests/test_building.py` (Wave 1.2+)

**Coverage Requirements:**
- ConfigBuilder initialization (client_id, profile_id, registry)
- add_server() - happy path, error cases (duplicate, not found, missing params)
- remove_server() - happy path, not found error
- clear() - empties draft
- build() - generates correct mcpServers payload
- to_artifact() - creates signed ConfigArtifact with metadata

**Running Tests:**
```bash
# All building tests
pytest tests/test_building.py -v

# Specific test
pytest tests/test_building.py::test_config_builder_add_server -v

# With coverage
pytest tests/test_building.py --cov=src/mcp_orchestrator/building --cov-report=term-missing
```

### Integration Tests

**Cross-Module Dependencies:**
- **ServerRegistry** (`src/mcp_orchestrator/servers/`) - Server definitions
- **ArtifactSigner** (`src/mcp_orchestrator/crypto/`) - Signing
- **ArtifactStore** (`src/mcp_orchestrator/storage/`) - Artifact ID computation

**Integration Test Pattern:**
```python
def test_config_builder_integration():
    """Test ConfigBuilder with real registry + crypto + storage"""
    # 1. Real registry
    registry = get_default_registry()

    # 2. Real builder
    builder = ConfigBuilder("claude-desktop", "default", registry)
    builder.add_server("filesystem", params={"path": "/tmp"})

    # 3. Real signing + storage
    artifact = builder.to_artifact(
        signing_key_id="test-key",
        private_key_path="tests/fixtures/test_key.pem",
        changelog="Test config"
    )

    # 4. Verify artifact structure
    assert artifact.client_id == "claude-desktop"
    assert artifact.profile_id == "default"
    assert artifact.metadata["server_count"] == 1
    assert artifact.payload == {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        }
    }
```

### End-to-End Tests

**Location:** `tests/e2e/test_draft_workflow.py` (Wave 1.3)

**E2E Workflow Validation:**
1. Initialize keys (crypto layer)
2. Add servers via ConfigBuilder (building layer)
3. View draft (no side effects)
4. Clear draft (reset state)
5. Re-add servers
6. Publish as artifact (crypto + storage layers)

---

## Common Tasks for Agents

### Adding a New ConfigBuilder Method

**Example:** Add `update_server()` method to modify existing server params

**Steps:**
1. Add method to `ConfigBuilder` class in `builder.py`
2. Raise `ServerNotInConfigError` if server_name not found
3. Update `_servers` dict with new config (call `registry.to_client_config()`)
4. Add unit test in `tests/test_building.py`
5. Add docstring with Args, Returns, Raises, Example
6. Update this AGENTS.md file if workflow changes

**Example Implementation:**
```python
def update_server(
    self,
    server_name: str,
    params: dict[str, Any] | None = None,
    env_vars: dict[str, str] | None = None,
) -> None:
    """Update an existing server's configuration.

    Args:
        server_name: Name of server in config
        params: New parameter values
        env_vars: New environment variables

    Raises:
        ServerNotInConfigError: If server_name not in config
    """
    if server_name not in self._servers:
        raise ServerNotInConfigError(
            f"Server '{server_name}' not found. Available: {sorted(self._servers.keys())}"
        )

    # Get server_id from existing config (assumes it's stored or can be inferred)
    # For now, use server_name as server_id (since server_name defaults to server_id)
    config = self._registry.to_client_config(
        server_id=server_name,
        params=params,
        env_vars=env_vars,
        server_name=server_name
    )

    self._servers[server_name] = config
```

### Modifying Draft State Validation

**When:** Adding business rules for draft configs (e.g., "max 10 servers", "filesystem required")

**Where to Add:**
- Simple validation: Add to `add_server()`, `build()`, or `to_artifact()`
- Complex validation: Create separate `validate()` method
- Pre-publish validation: Add to `to_artifact()` (fail before signing)

**Example:**
```python
def to_artifact(self, ...) -> ConfigArtifact:
    # Validate before publishing
    if self.count() == 0:
        raise ValueError("Cannot publish empty config (0 servers)")

    if self.count() > 50:
        raise ValueError(f"Too many servers ({self.count()}). Max: 50")

    # Rest of method...
    payload = self.build()
    # ...
```

### Debugging Draft State Issues

**Check draft contents:**
```python
builder = ConfigBuilder("claude-desktop", "default")
builder.add_server("filesystem", params={"path": "/tmp"})

# Inspect draft
print(f"Server count: {builder.count()}")
print(f"Server names: {builder.get_servers()}")
print(f"Has filesystem? {builder.has_server('filesystem')}")
print(f"Full payload: {builder.build()}")
```

**Common Issues:**
- **ServerAlreadyAddedError:** server_name collision (use `builder.has_server(name)` before adding)
- **Empty build():** Check `builder.count()` - draft might be empty (call `add_server()` first)
- **Signature fails:** Verify private_key_path exists and has correct permissions (0600)

---

## Architecture & Integration

### Layer Position

```
┌─────────────────────────────────────────────────┐
│              MCP Server Layer                   │
│   Tools: add_server_to_config,                  │
│          remove_server_from_config,             │
│          publish_config, view_draft_config,     │
│          clear_draft_config                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│          Building Layer (YOU ARE HERE)          │
│   ConfigBuilder: Draft state management         │
└────┬──────────┬──────────┬──────────────────────┘
     │          │          │
     │          │          └──────────────┐
     ▼          ▼                         ▼
┌─────────┐ ┌──────────┐        ┌───────────────┐
│ Storage │ │  Crypto  │        │    Registry   │
│  Layer  │ │  Layer   │        │     Layer     │
│ (CAS)   │ │(Ed25519) │        │ (Servers)     │
└─────────┘ └──────────┘        └───────────────┘
```

### Cross-Module Dependencies

**Upstream (Building depends on):**
- **ServerRegistry** (`src/mcp_orchestrator/servers/registry.py`)
  - Purpose: Server definitions catalog
  - Usage: `registry.to_client_config(server_id, params, env_vars, server_name)` → server config
  - See: [src/mcp_orchestrator/servers/AGENTS.md](../servers/AGENTS.md)

- **ArtifactSigner** (`src/mcp_orchestrator/crypto/signer.py`)
  - Purpose: Sign payloads with Ed25519 keys
  - Usage: `signer.sign(payload)` → base64 signature
  - See: [src/mcp_orchestrator/crypto/AGENTS.md](../crypto/AGENTS.md)

- **ArtifactStore** (`src/mcp_orchestrator/storage/store.py`)
  - Purpose: Compute artifact IDs (SHA-256 hashing)
  - Usage: `store.compute_artifact_id(payload)` → artifact_id
  - See: [src/mcp_orchestrator/storage/AGENTS.md](../storage/AGENTS.md)

**Downstream (Depends on Building):**
- **MCP Server Tools** (`src/mcp_orchestrator/mcp/server.py`)
  - Tools: `add_server_to_config`, `remove_server_from_config`, `publish_config`, `view_draft_config`, `clear_draft_config`
  - Usage: Maintain singleton `ConfigBuilder` instance, expose methods as MCP tools
  - See: [src/mcp_orchestrator/mcp/AGENTS.md](../mcp/AGENTS.md)

### Data Flow Example

**User Workflow (via Claude Desktop):**

```
User: "Add filesystem server for /Users/me/Documents"
  │
  ▼
MCP Server: add_server_to_config(server_id="filesystem", params={"path": "/Users/me/Documents"})
  │
  ▼
ConfigBuilder.add_server("filesystem", {"path": "/Users/me/Documents"})
  │
  ├─→ ServerRegistry.to_client_config("filesystem", {"path": "/Users/me/Documents"})
  │   │
  │   └─→ Returns: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]}
  │
  └─→ Stores in _servers["filesystem"] = {...}

User: "Publish this config"
  │
  ▼
MCP Server: publish_config(changelog="Added filesystem")
  │
  ▼
ConfigBuilder.to_artifact(signing_key_id, private_key_path, changelog)
  │
  ├─→ ConfigBuilder.build() → {"mcpServers": {"filesystem": {...}}}
  │
  ├─→ ArtifactSigner.sign(payload) → signature_b64
  │
  ├─→ ArtifactStore.compute_artifact_id(payload) → artifact_id
  │
  └─→ Returns: ConfigArtifact(artifact_id, client_id, profile_id, payload, signature, metadata)
```

---

## Design Constraints

### Immutability After Publishing

**Constraint:** Once `to_artifact()` is called, the draft can continue to be modified, but the published artifact is immutable.

**Rationale:** Content-addressable storage (CAS) requires immutability. Artifact ID = SHA-256(payload), so modifying payload would change ID.

**Implication:** ConfigBuilder can be reused after publishing (draft persists), but published artifacts cannot be edited.

**Example:**
```python
builder = ConfigBuilder("claude-desktop", "default")
builder.add_server("filesystem", params={"path": "/tmp"})

# Publish version 1
artifact_v1 = builder.to_artifact(signing_key_id, private_key_path, changelog="v1")
store.save(artifact_v1)

# Modify draft (add another server)
builder.add_server("memory")

# Publish version 2 (new artifact_id)
artifact_v2 = builder.to_artifact(signing_key_id, private_key_path, changelog="v2")
store.save(artifact_v2)

# artifact_v1 and artifact_v2 are DIFFERENT artifacts (different artifact_ids)
# artifact_v1 remains unchanged in storage
```

### Server Name Uniqueness

**Constraint:** server_name must be unique within a single draft

**Rationale:** MCP client configs use server names as keys in `mcpServers` object. Duplicate keys would overwrite previous entries.

**Enforcement:** `add_server()` raises `ServerAlreadyAddedError` if server_name already exists.

**Workaround:** Use custom server_name parameter to add same server_id multiple times:
```python
# Add filesystem server twice with different paths
builder.add_server("filesystem", params={"path": "/docs"}, server_name="filesystem-docs")
builder.add_server("filesystem", params={"path": "/code"}, server_name="filesystem-code")

# Result: Two separate entries in mcpServers
# {
#   "mcpServers": {
#     "filesystem-docs": {...},
#     "filesystem-code": {...}
#   }
# }
```

### Registry-Driven Configuration

**Constraint:** All servers must be defined in ServerRegistry

**Rationale:** Registry provides:
- Transport abstraction (stdio vs HTTP/SSE)
- Parameter validation (required/optional params)
- Default values
- Schema enforcement

**Implication:** ConfigBuilder cannot add arbitrary servers. To add new server:
1. Add ServerDefinition to registry (see [src/mcp_orchestrator/servers/AGENTS.md](../servers/AGENTS.md))
2. Then use `builder.add_server(server_id)` with new server_id

---

## Related Files

**Cross-reference these AGENTS.md files when working on building module:**

- **[src/mcp_orchestrator/servers/AGENTS.md](../servers/AGENTS.md)** - Server registry, transport abstraction
- **[src/mcp_orchestrator/crypto/AGENTS.md](../crypto/AGENTS.md)** - Signing, key management
- **[src/mcp_orchestrator/storage/AGENTS.md](../storage/AGENTS.md)** - Artifact storage, CAS
- **[src/mcp_orchestrator/mcp/AGENTS.md](../mcp/AGENTS.md)** - MCP tools that use ConfigBuilder
- **[src/mcp_orchestrator/registry/AGENTS.md](../registry/AGENTS.md)** - Client metadata

**Root AGENTS.md:**
- **[AGENTS.md](../../../AGENTS.md)** - Project overview, all nested guides

---

**Version:** 0.1.3 (Wave 1.3 - Ergonomic Tools)
**Last Updated:** 2025-10-24
**Format:** AGENTS.md standard (nested module guide)
