# Capability: Config Deployment

Automated deployment of signed configuration artifacts to MCP client config locations with verification, logging, and rollback capabilities.

## Behaviors
- @behavior:MCP.CONFIG.DEPLOY
- @status:ready

Behavior Specs:
- [project-docs/capabilities/behaviors/mcp-config-deploy.feature](behaviors/mcp-config-deploy.feature)

## Value Scenarios

### Scenario 1: Deploy Latest Config
- **ID:** mcp.config.deploy.latest
- **Status:** ready
- **Guide:** [user-docs/how-to/deploy-config.md](../../user-docs/how-to/deploy-config.md)
- **Tests:** [tests/value-scenarios/test_deploy_config.py](../../tests/value-scenarios/test_deploy_config.py)
- **Description:** Deploy latest published artifact to client config location

### Scenario 2: Deploy Specific Version
- **ID:** mcp.config.deploy.specific-version
- **Status:** ready
- **Guide:** [user-docs/how-to/deploy-config.md](../../user-docs/how-to/deploy-config.md)
- **Tests:** [tests/value-scenarios/test_deploy_config.py](../../tests/value-scenarios/test_deploy_config.py)
- **Description:** Deploy specific artifact by ID (version pinning)

### Scenario 3: Query Deployed vs Latest
- **ID:** mcp.config.deploy.query-status
- **Status:** ready
- **Guide:** [user-docs/how-to/deploy-config.md](../../user-docs/how-to/deploy-config.md)
- **Tests:** [tests/value-scenarios/test_deploy_config.py](../../tests/value-scenarios/test_deploy_config.py)
- **Description:** Query to detect configuration drift

## Integrations

### MCP Tools
- `deploy_config` - Deploy artifact to client config location
  - Parameters: client_id, profile_id, artifact_id (optional)
  - Returns: status, config_path, artifact_id, deployed_at

### MCP Resources
- `config://{client_id}/{profile_id}/latest` - Latest published artifact
- `config://{client_id}/{profile_id}/deployed` - Currently deployed artifact

### CLI Commands
- `mcp-orchestration deploy-config` - Deploy configuration from command line
  - Options: --client, --profile, --artifact-id, --format

### Domain Model

#### Entities

**DeploymentWorkflow** (Service)
- Orchestrates fetch → verify → write workflow
- Determines client config paths from ClientRegistry
- Records deployment events in DeploymentLog
- Handles atomic file operations with rollback
- Methods:
  - `deploy(client_id, profile_id, artifact_id) -> DeploymentResult`
  - `_resolve_artifact(client_id, profile_id, artifact_id) -> ConfigArtifact`
  - `_verify_signature(artifact) -> bool`
  - `_get_config_path(client_id) -> Path`
  - `_write_config_atomic(path, config) -> None`

**DeploymentRecord** (Entity)
- Tracks deployment history
- Links artifact_id to deployed location and timestamp
- Immutable deployment log entry
- Fields:
  - deployment_id (UUID)
  - client_id, profile_id
  - artifact_id
  - config_path
  - deployed_at (ISO 8601)

#### Value Objects

**DeploymentResult**
- Contains deployment outcome
- Immutable
- Fields:
  - status: "deployed" | "failed"
  - config_path: str
  - artifact_id: str
  - deployed_at: str (ISO 8601)

**ClientConfigLocation**
- Encapsulates OS-specific path logic
- Handles ~ expansion and path validation
- Ensures parent directories exist
- Methods:
  - `resolve(client_id) -> Path`
  - `create_parent_dirs() -> None`
  - `validate_writable() -> bool`

#### Repositories

**ArtifactStore** (existing)
- Fetch artifacts for deployment
- Verify artifact existence
- Get latest artifact for profile

**DeploymentLog** (new)
- Record deployment events
- Query deployment history
- Get currently deployed artifact
- Methods:
  - `record_deployment(client_id, profile_id, artifact_id, config_path) -> None`
  - `get_deployed_artifact(client_id, profile_id) -> str | None`
  - `get_deployment_history(client_id, profile_id, limit) -> list[DeploymentRecord]`

**ClientRegistry** (existing)
- Lookup client configuration paths
- Validate client_id existence

## Dependencies

### From Other Capabilities
- **Config Publishing:** Published artifacts from PublishingWorkflow
- **Cryptographic Signing:** Signature verification before deployment
- **Content Addressing:** Artifact retrieval by SHA-256 ID
- **Client Registry:** Config path lookup

### External Dependencies
- `pathlib` - Path operations
- `shutil` - Atomic file operations
- `cryptography` - Signature verification
- Filesystem - Config file writing

## Success Criteria

### Functional
- [ ] User can deploy latest artifact via MCP tool
- [ ] User can deploy latest artifact via CLI
- [ ] User can deploy specific artifact by ID
- [ ] Signature is verified before deployment
- [ ] Invalid signature prevents deployment
- [ ] Parent directories created if needed
- [ ] Deployment is atomic (rollback on failure)
- [ ] Deployment logged to deployment log
- [ ] User can query deployed vs latest artifact
- [ ] Error messages are clear and actionable

### Non-Functional
- [ ] Deployment completes in <2 seconds
- [ ] Test coverage ≥70%
- [ ] All BDD scenarios pass
- [ ] All E2E value scenarios pass
- [ ] No data loss on deployment failure
- [ ] Cross-platform (macOS, Linux, Windows)

## Wave Alignment

**Wave 1.5 (v0.1.5) - End-to-End Config Management**
- Goal: Complete workflow: discover → build → validate → publish → deploy
- Deliverables:
  - Deployment workflow module
  - MCP tool and resources
  - CLI command
  - E2E documentation
  - Deployment logging

## Spec Coverage

- ✅ **UC-1:** Bootstrap (first-time client setup with automated deployment)
- ✅ **UC-2:** Routine Update (update existing configs with automated deployment)
- ⚠️ **UC-3:** Emergency Revert (partial - can deploy previous artifact, no rollback UX yet)

## Future Evolution

### Wave 1.6: Audit & History
- Query full deployment history
- Audit trail for compliance
- Time-based rollback ("deploy config from yesterday")

### Wave 2.x: Remote Deployment API
- HTTP endpoint for remote deployment
- Webhook notifications on deployment
- Multi-client deployment (deploy to all profiles)

### Wave 3.x: Advanced Deployment
- Staged rollout (deploy to subset first)
- Deployment approval workflows
- Automatic rollback on client errors

## References

- [WAVE_1X_PLAN.md](../WAVE_1X_PLAN.md) - Wave 1.5 scope
- [DEVELOPMENT_LIFECYCLE.md](../DEVELOPMENT_LIFECYCLE.md) - Development process
- [config-publishing.md](config-publishing.md) - Related publishing capability
- [mcp-tools.md](../../user-docs/reference/mcp-tools.md) - Tool API reference
