# Wave 1.x Planning Document

**Status**: Living document
**Last Updated**: 2025-10-24
**Current Wave**: 1.1 (Server Registry)

---

## Overview

This document breaks down the remaining spec functionality into logical, incremental waves that build on Wave 1.0.0 (v0.1.0). Each wave delivers standalone value while building toward complete spec coverage.

---

## Wave 1.0 (v0.1.0) ✅ COMPLETED

**Released**: 2025-10-17
**Goal**: Foundation - Read-only config orchestration

### Delivered Features
- **MCP Server**: stdio-based server exposing tools/resources
- **4 MCP Tools**: `list_clients`, `list_profiles`, `get_config`, `diff_config`
- **2 MCP Resources**: `capabilities://server`, `capabilities://clients`
- **Client Registry**: Metadata for Claude Desktop, Cursor
- **Artifact Storage**: Content-addressable storage with Ed25519 signing
- **CLI**: `mcp-orchestration init-configs`, basic artifact management
- **Crypto**: Signing and verification infrastructure
- **Testing**: 70%+ coverage

### Spec Coverage
- ✅ FR-1: List supported client families
- ✅ FR-2: List available profiles per client
- ✅ FR-3: Expose compatibility notes
- ✅ FR-4: Return fully materialized ConfigArtifact
- ✅ FR-9: Support idempotent diff/status checks
- ⚠️ FR-5: Parameter injection (basic, via init only)

### Limitations
- **Read-only**: Users can fetch/diff configs but NOT create new ones
- **Hardcoded configs**: Only 3 sample configs from `init-configs`
- **No server registry**: Can't browse/add MCP servers
- **No validation**: Can't validate before publishing
- **No publishing workflow**: Can't create artifacts programmatically

---

## Wave 1.1 (v0.1.1) — MCP Server Registry

**Status**: Planning
**Goal**: Enable users to discover and register available MCP servers
**Estimated Timeline**: 3-5 days

### Scope

#### New Module: `src/mcp_orchestrator/servers/`

**1. Server Definition Model** (`servers/models.py`)
```python
class ServerDefinition(BaseModel):
    """Definition of an MCP server."""

    server_id: str  # e.g., "filesystem", "n8n"
    display_name: str
    description: str

    # Transport configuration
    transport: Literal["stdio", "http", "sse"]

    # For stdio servers
    stdio_command: str | None = None  # e.g., "npx", "python"
    stdio_args: list[str] = Field(default_factory=list)

    # For HTTP/SSE servers (will wrap with mcp-remote later)
    http_url: str | None = None
    http_auth_type: Literal["none", "bearer", "oauth"] | None = None

    # Configuration
    required_env: list[str] = Field(default_factory=list)
    optional_env: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)

    # Metadata
    documentation_url: str | None = None
    npm_package: str | None = None
```

**2. Server Registry** (`servers/registry.py`)
```python
class ServerRegistry:
    """Registry of known MCP servers."""

    def list_servers() -> list[ServerDefinition]
    def get_server(server_id: str) -> ServerDefinition
    def has_server(server_id: str) -> bool
    def search_servers(query: str) -> list[ServerDefinition]
```

**3. Default Catalog** (`servers/defaults.py`)

Initial servers (10-15):
- **stdio**: filesystem, brave-search, github, memory, fetch, postgres, sqlite
- **HTTP/SSE**: n8n (example), custom-api (example)

#### MCP Tools (2 new)

```python
@mcp.tool()
async def list_available_servers(
    transport_filter: str | None = None
) -> dict[str, Any]:
    """List all MCP servers in registry.

    Args:
        transport_filter: Optional filter by transport (stdio, http, sse)

    Returns:
        - servers: List of ServerDefinition objects
        - count: Total number of servers
        - transport_counts: Breakdown by transport type
    """

@mcp.tool()
async def describe_server(server_id: str) -> dict[str, Any]:
    """Get detailed information about a specific server.

    Args:
        server_id: Server identifier (e.g., "filesystem", "n8n")

    Returns:
        - Full ServerDefinition
        - Example usage
        - Setup instructions
    """
```

#### MCP Resources (1 new)

```python
@mcp.resource("server://registry")
async def server_registry_resource() -> str:
    """Full server registry as JSON."""

@mcp.resource("server://{server_id}")
async def server_definition_resource(server_id: str) -> str:
    """Detailed definition for a specific server."""
```

#### CLI Commands (2 new)

```bash
# List all available servers
mcp-orchestration list-servers [--transport stdio|http|sse]

# Get detailed info about a server
mcp-orchestration describe-server <server_id>
```

### Deliverables
- [ ] Server registry module (`src/mcp_orchestrator/servers/`)
- [ ] 10-15 server definitions in default catalog
- [ ] 2 MCP tools + 2 resources
- [ ] 2 CLI commands
- [ ] Unit tests (≥80% coverage)
- [ ] E2E guide: `docs/how-to/browse-server-registry.md`

### Spec Coverage
- Sets foundation for FR-5 (parameter injection)
- Enables future server-based config generation

### Success Criteria
- ✅ User can list all available MCP servers via CLI
- ✅ User can list all available MCP servers via MCP tool (in Claude)
- ✅ User can get detailed server info including setup instructions
- ✅ Registry includes both stdio and HTTP/SSE servers
- ✅ All tests passing with ≥80% coverage

---

## Wave 1.2 (v0.1.2) — Transport Abstraction + Config Generation

**Status**: Planned
**Goal**: Generate client configs from server registry with automatic mcp-remote wrapping
**Estimated Timeline**: 4-6 days

### Scope

#### Transport Abstraction Layer

**Key Feature**: Automatic mcp-remote wrapping for HTTP/SSE servers

```python
class ServerRegistry:
    def to_client_config(
        self,
        server_id: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate client config for a server (ALWAYS stdio).

        For stdio servers: Returns direct config
        For HTTP/SSE servers: Wraps with mcp-remote automatically
        """
```

**Example**: HTTP server definition:
```python
ServerDefinition(
    server_id="n8n",
    transport="sse",
    http_url="http://localhost:{port}/mcp/sse",
    ...
)
```

**Generated config** (automatic mcp-remote wrapper):
```json
{
  "n8n": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/mcp-remote",
      "stdio",
      "http://localhost:5679/mcp/sse"
    ],
    "env": {...}
  }
}
```

#### Config Builder Module

**New Module**: `src/mcp_orchestrator/building/`

```python
class ConfigBuilder:
    """Builder for constructing mcpServers payloads."""

    def __init__(self, client_id: str, profile_id: str)
    def add_server(server_id: str, params: dict) -> None
    def remove_server(server_name: str) -> None
    def get_servers() -> list[str]
    def build() -> dict[str, Any]  # Returns complete mcpServers payload
```

#### MCP Tools (2 new)

```python
@mcp.tool()
async def add_server_to_config(
    client_id: str,
    profile_id: str,
    server_id: str,
    params: dict[str, Any],
    env_vars: dict[str, str] | None = None
) -> dict[str, Any]:
    """Add a server to client configuration.

    Automatically handles stdio vs HTTP/SSE (wraps with mcp-remote if needed).
    Returns draft config preview (unsigned).
    """

@mcp.tool()
async def remove_server_from_config(
    client_id: str,
    profile_id: str,
    server_name: str
) -> dict[str, Any]:
    """Remove a server from client configuration.

    Returns updated draft config preview.
    """
```

#### MCP Resources (1 new)

```python
@mcp.resource("config://{client_id}/{profile_id}/draft")
async def draft_config_resource(client_id: str, profile_id: str) -> str:
    """Current draft configuration (unsigned)."""
```

#### CLI Commands (2 new)

```bash
# Add server to config (stdio or HTTP - auto-wrapped)
mcp-orchestration add-server <server_id> \
  --client <client> \
  --profile <profile> \
  --param key=value \
  --env VAR=value

# Remove server from config
mcp-orchestration remove-server <server_name> \
  --client <client> \
  --profile <profile>
```

### Deliverables
- [ ] Transport abstraction implementation
- [ ] ConfigBuilder class
- [ ] 2 MCP tools + 1 resource
- [ ] 2 CLI commands
- [ ] Unit tests for transport wrapping
- [ ] E2E guides:
  - `docs/how-to/add-stdio-server.md`
  - `docs/how-to/add-http-server-with-auto-wrapping.md`

### Spec Coverage
- ✅ FR-5: Parameter injection (full implementation)
- Foundation for FR-6 (validation)

### Success Criteria
- ✅ User can add stdio server to config
- ✅ User can add HTTP/SSE server to config (auto-wrapped with mcp-remote)
- ✅ Generated configs are valid for target client
- ✅ Parameters are substituted correctly
- ✅ Environment variables are included
- ✅ User never sees mcp-remote details (transparent)

---

## Wave 1.3 (v0.1.3) — Schema Validation

**Status**: Planned
**Goal**: Validate draft configs before publishing
**Estimated Timeline**: 2-3 days

### Scope

#### Validation Module

**New Module**: `src/mcp_orchestrator/validation/`

```python
class SchemaValidator:
    """Validate MCP client configurations against schema."""

    def validate_mcpservers(
        self,
        payload: dict,
        client_id: str
    ) -> ValidationReport:
        """Validate mcpServers structure.

        Checks:
        - mcpServers is dict
        - Each server has required fields (command, args)
        - env vars are dict[str, str]
        - No obvious issues
        """

class ValidationReport(BaseModel):
    """Validation result."""
    valid: bool
    errors: list[str]
    warnings: list[str]
    suggestions: list[str]
```

#### JSON Schemas

Create schemas for 3 clients:
- `schemas/claude-desktop.schema.json`
- `schemas/cursor.schema.json`
- `schemas/cline.schema.json`

#### MCP Tools (1 new)

```python
@mcp.tool()
async def validate_draft(
    client_id: str,
    profile_id: str,
    payload: dict[str, Any]
) -> dict[str, Any]:
    """Validate a draft configuration before publishing.

    Returns:
        ValidationReport with errors, warnings, suggestions
    """
```

#### CLI Commands (1 new)

```bash
# Validate draft config file
mcp-orchestration validate-draft \
  --client <client> \
  --profile <profile> \
  --file <draft.json>
```

### Deliverables
- [ ] Schema validator module
- [ ] JSON schemas for 3 clients
- [ ] 1 MCP tool
- [ ] 1 CLI command
- [ ] Unit tests for validation logic
- [ ] E2E guide: `docs/how-to/validate-config-draft.md`

### Spec Coverage
- ✅ FR-6: Validate payload against client schema
- ✅ FR-8: Machine-readable validation report

### Success Criteria
- ✅ Validation catches missing required fields
- ✅ Validation catches type errors (args not array, etc.)
- ✅ Warnings for unknown fields
- ✅ Helpful error messages
- ✅ Suggestions for fixes

---

## Wave 1.4 (v0.1.4) — Publishing Workflow

**Status**: Planned
**Goal**: Enable users to create and sign config artifacts
**Estimated Timeline**: 3-4 days

### Scope

#### Publishing Module

**New Module**: `src/mcp_orchestrator/publishing/`

```python
class PublishingWorkflow:
    """Workflow for publishing config artifacts."""

    def publish(
        self,
        client_id: str,
        profile_id: str,
        payload: dict[str, Any],
        changelog: str
    ) -> ConfigArtifact:
        """Publish a new configuration artifact.

        Steps:
        1. Validate payload
        2. Sign payload
        3. Create artifact
        4. Store artifact
        5. Update profile index

        Returns:
            Signed ConfigArtifact
        """
```

#### Enhanced Artifact Metadata

Update `ConfigArtifact` model:
```python
class ConfigArtifact(BaseModel):
    # ... existing fields ...

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata including generator and changelog"
    )
    # metadata["generator"]: "publish_config" | "init-configs"
    # metadata["changelog"]: str
```

#### MCP Tools (1 new)

```python
@mcp.tool()
async def publish_config(
    client_id: str,
    profile_id: str,
    payload: dict[str, Any],
    changelog: str
) -> dict[str, Any]:
    """Publish a new configuration artifact.

    Returns:
        - artifact_id
        - status: "published"
        - changelog
    """
```

#### CLI Commands (1 new)

```bash
# Publish config file
mcp-orchestration publish-config \
  --client <client> \
  --profile <profile> \
  --file <config.json> \
  --changelog "Added n8n server"
```

### Deliverables
- [ ] Publishing workflow module
- [ ] 1 MCP tool
- [ ] 1 CLI command
- [ ] Integration tests for publish flow
- [ ] E2E guides:
  - `docs/how-to/publish-config.md`
  - `docs/how-to/update-config.md`

### Spec Coverage
- ✅ FR-6: Validate before release (integration)
- ✅ FR-11: Include change metadata (changelog)
- Partial FR-12: Record release entries (no approvals yet)

### Success Criteria
- ✅ User can publish config from CLI
- ✅ User can publish config via MCP tool
- ✅ Validation runs before publishing
- ✅ Invalid configs are rejected
- ✅ Signed artifacts stored correctly
- ✅ Changelog included in metadata

---

## Wave 1.5 (v0.1.5) — End-to-End Config Management

**Status**: Planned
**Goal**: Complete user workflow from discovery → build → validate → publish → deploy
**Estimated Timeline**: 2-3 days

### Scope

#### Integrated Workflow

**Complete User Journey**:
1. **Discovery**: Browse server registry (`list_available_servers`)
2. **Build**: Add servers to draft config (`add_server_to_config`)
3. **Validate**: Check draft against schema (`validate_draft`)
4. **Publish**: Sign and store artifact (`publish_config`)
5. **Deploy**: Write to client config location (`deploy_config`)

#### Deploy Command

```python
class DeploymentWorkflow:
    """Deploy artifacts to client config locations."""

    def deploy(
        self,
        client_id: str,
        profile_id: str,
        artifact_id: str
    ) -> DeploymentResult:
        """Deploy artifact to client config location.

        Steps:
        1. Fetch artifact
        2. Verify signature
        3. Determine client config location
        4. Write config file
        5. Record deployment
        """
```

#### MCP Tools (1 new)

```python
@mcp.tool()
async def deploy_config(
    client_id: str,
    profile_id: str,
    artifact_id: str | None = None
) -> dict[str, Any]:
    """Deploy configuration to client.

    Args:
        artifact_id: Specific artifact to deploy (defaults to latest)

    Returns:
        - status: "deployed"
        - config_path: Where config was written
        - artifact_id: Deployed artifact
    """
```

#### MCP Resources (2 new)

```python
@mcp.resource("config://{client_id}/{profile_id}/latest")
async def latest_config_resource(client_id: str, profile_id: str) -> str:
    """Latest published artifact."""

@mcp.resource("config://{client_id}/{profile_id}/deployed")
async def deployed_config_resource(client_id: str, profile_id: str) -> str:
    """Currently deployed artifact."""
```

#### CLI Commands (1 new)

```bash
# Deploy config to client
mcp-orchestration deploy-config \
  --client <client> \
  --profile <profile> \
  [--artifact-id <id>]  # Optional, defaults to latest
```

### Deliverables
- [ ] Deployment workflow module
- [ ] 1 MCP tool + 2 resources
- [ ] 1 CLI command
- [ ] Integration tests for full workflow
- [ ] Comprehensive E2E guide: `docs/how-to/manage-config-lifecycle.md`
- [ ] User tutorial: `docs/tutorials/your-first-config.md`

### Spec Coverage
- Complete core loop (discovery → retrieval → update → deploy)
- Foundation for UC-1 (Bootstrap), UC-2 (Routine Update)

### Success Criteria
- ✅ User can complete full workflow: discover → add → validate → publish → deploy
- ✅ Both CLI and MCP tool workflows work
- ✅ Deployed configs work in target client (manual test)
- ✅ Tutorial walks through complete user journey

---

## Wave 1.6 (v0.1.6) — Audit & History

**Status**: Planned
**Goal**: Track config changes and provide audit trail
**Estimated Timeline**: 3-4 days

### Scope

#### Audit Log Module

**New Module**: `src/mcp_orchestrator/audit/`

```python
class AuditEvent(BaseModel):
    """Audit event record."""
    event_id: str  # UUID
    timestamp: str  # ISO 8601
    action: Literal["publish", "deploy", "revert"]
    client_id: str
    profile_id: str
    artifact_id: str
    changelog: str | None
    publisher_id: str  # Future: from auth, now "local"

class AuditLog:
    """Audit log manager."""

    def record_publish(artifact: ConfigArtifact) -> None
    def record_deploy(client_id, profile_id, artifact_id) -> None
    def get_history(client_id, profile_id, since: datetime) -> list[AuditEvent]
    def get_artifact_history(artifact_id) -> list[AuditEvent]
```

#### MCP Tools (2 new)

```python
@mcp.tool()
async def get_config_history(
    client_id: str,
    profile_id: str,
    limit: int = 10
) -> dict[str, Any]:
    """Get configuration change history.

    Returns:
        - artifacts: List of past artifacts with metadata
        - count: Total number of artifacts
    """

@mcp.tool()
async def get_audit_log(
    client_id: str,
    profile_id: str,
    since: str | None = None  # ISO 8601 or "7d", "30d"
) -> dict[str, Any]:
    """Get audit log for a client/profile.

    Returns:
        - events: List of audit events
        - count: Total number of events
    """
```

#### MCP Resources (1 new)

```python
@mcp.resource("audit://{client_id}/{profile_id}")
async def audit_log_resource(client_id: str, profile_id: str) -> str:
    """Audit log for client/profile as JSON."""
```

#### CLI Commands (2 new)

```bash
# View config history
mcp-orchestration config-history \
  --client <client> \
  --profile <profile> \
  [--limit 10]

# View audit log
mcp-orchestration audit-log \
  --client <client> \
  --profile <profile> \
  [--since 7d|30d|2024-01-01]
```

### Deliverables
- [ ] Audit log module
- [ ] 2 MCP tools + 1 resource
- [ ] 2 CLI commands
- [ ] Unit tests for audit logic
- [ ] E2E guide: `docs/how-to/audit-config-changes.md`

### Spec Coverage
- ✅ FR-12: Record immutable release entries
- ✅ FR-13: Read-only audit queries
- Partial UC-3 (Emergency Revert - foundation)

### Success Criteria
- ✅ All publish/deploy events are logged
- ✅ User can view config history
- ✅ User can query audit log
- ✅ Audit events are immutable
- ✅ Timestamps are accurate

---

## Summary Table

| Wave | Version | Goal | Tools | Resources | CLI Cmds | Days | Spec FRs |
|------|---------|------|-------|-----------|----------|------|----------|
| 1.0 | v0.1.0 | ✅ Foundation | 4 | 2 | 1 | - | FR-1,2,3,4,9 |
| 1.1 | v0.1.1 | Server Registry | +2 | +2 | +2 | 3-5 | (foundation) |
| 1.2 | v0.1.2 | Transport + Gen | +2 | +1 | +2 | 4-6 | FR-5 |
| 1.3 | v0.1.3 | Validation | +1 | 0 | +1 | 2-3 | FR-6,8 |
| 1.4 | v0.1.4 | Publishing | +1 | 0 | +1 | 3-4 | FR-11,12* |
| 1.5 | v0.1.5 | E2E Workflow | +1 | +2 | +1 | 2-3 | (integration) |
| 1.6 | v0.1.6 | Audit & History | +2 | +1 | +2 | 3-4 | FR-12,13 |
| **Total** | **1.0-1.6** | | **13** | **8** | **10** | **17-25** | **8/15 FRs** |

---

## Post-Wave 1.x (Wave 2.0+)

**Deferred to Wave 2**:
- **FR-7**: Policy enforcement (requires policy DSL design)
- **FR-10**: Subscription/push updates (requires streaming)
- **FR-14, FR-15**: Client telemetry (requires client-side integration)
- **UC-4**: Policy tightening
- Multi-signer approvals
- RBAC integration
- Enterprise governance features

**Rationale**: Wave 1.x focuses on core config management workflow. Wave 2 adds organizational governance and enterprise features after validating core functionality with users.

---

## Implementation Strategy

### Incremental Releases
- Each wave = 1 semantic version bump (v0.1.1, v0.1.2, ...)
- Version format: `0.MINOR.PATCH`
- Git tags for each release

### Testing Requirements
- **Each wave**: ≥70% coverage for new code
- **Integration tests**: Test interactions between waves
- **E2E tests**: Verify user workflows work end-to-end
- **Manual testing**: Test in real Claude Desktop/Cursor before release

### Documentation Updates

**Per wave, update**:
- `CHANGELOG.md`: Add version entry with features
- `docs/how-to/`: Add E2E guide
- `ROADMAP.md`: Mark wave complete
- `project-docs/WAVE_1X_PLAN.md`: Update status
- Git tag: `v0.1.X`

### Release Criteria

**Before releasing a wave**:
- [ ] All tests passing (CI green)
- [ ] Coverage ≥70%
- [ ] E2E guide complete and tested
- [ ] Manual testing performed
- [ ] CHANGELOG.md updated
- [ ] Git tag created
- [ ] PyPI package published (optional)

---

## Benefits of This Approach

1. **Incremental Value**: Each wave delivers standalone functionality users can use
2. **Low Risk**: Small changes (2-6 days) are easier to test and validate
3. **Fast Iteration**: Quick cycles enable rapid feedback and course correction
4. **Logical Dependencies**: Each wave builds on previous work in natural sequence
5. **Clear Milestones**: Easy to track progress and communicate status to stakeholders
6. **User-Centric**: Prioritizes complete workflows over isolated features
7. **Spec Alignment**: Maps directly to functional requirements from spec.md

---

## Wave Status Tracker

| Wave | Version | Status | Started | Completed | Notes |
|------|---------|--------|---------|-----------|-------|
| 1.0 | v0.1.0 | ✅ Done | 2025-10-17 | 2025-10-17 | Foundation release |
| 1.1 | v0.1.1 | 📋 Planned | - | - | Server registry |
| 1.2 | v0.1.2 | 📋 Planned | - | - | Transport abstraction |
| 1.3 | v0.1.3 | 📋 Planned | - | - | Schema validation |
| 1.4 | v0.1.4 | 📋 Planned | - | - | Publishing workflow |
| 1.5 | v0.1.5 | 📋 Planned | - | - | E2E workflow |
| 1.6 | v0.1.6 | 📋 Planned | - | - | Audit & history |

**Legend**:
- ✅ Done
- 🚧 In Progress
- 📋 Planned
- ⏸️ Paused
- ❌ Cancelled

---

## Next Steps

1. ✅ Create `project-docs/WAVE_1X_PLAN.md` (this document)
2. Update `ROADMAP.md` to reference this wave plan
3. Start Wave 1.1 (Server Registry) implementation
4. Follow wave sequence in order (no skipping!)
5. Update this document as waves progress

**Current Wave**: 1.1 (Server Registry)
**Recommendation**: Begin Wave 1.1 implementation

---

**Document Version**: 1.0
**Template**: Based on chora-base incremental delivery patterns
