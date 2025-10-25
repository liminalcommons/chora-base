# Capability: Config Publishing

Provides validated configuration publishing with cryptographic signing, changelog tracking, and metadata management.

## Behaviors
- @behavior:MCP.CONFIG.PUBLISH
- @status:ready

Behavior Specs:
- [project-docs/capabilities/behaviors/mcp-config-publish.feature](behaviors/mcp-config-publish.feature)

## Value Scenarios

### Scenario 1: Full Publishing Workflow
- **ID:** mcp.config.publish.full-workflow
- **Status:** ready
- **Guide:** [user-docs/how-to/publish-config.md](../../user-docs/how-to/publish-config.md)
- **Tests:** [tests/value-scenarios/test_publish_config.py](../../tests/value-scenarios/test_publish_config.py)
- **Description:** Complete workflow from draft creation → validation → publishing

### Scenario 2: Update Existing Config
- **ID:** mcp.config.publish.update-workflow
- **Status:** planned
- **Guide:** [user-docs/how-to/update-config.md](../../user-docs/how-to/update-config.md)
- **Tests:** [tests/value-scenarios/test_update_config.py](../../tests/value-scenarios/test_update_config.py)
- **Description:** Update existing configuration with new servers

## Integrations

### MCP Tools
- `validate_config` - Validate draft configuration before publishing
- `publish_config` - Publish validated draft as signed artifact

### CLI Commands
- `mcp-orchestration publish-config` - Publish config from CLI with validation

### Domain Model

#### Entities

**PublishingWorkflow** (Service)
- Orchestrates validation → signing → storage workflow
- Ensures atomic publish operations
- Manages metadata enrichment

**ConfigArtifact** (Entity)
- Immutable signed configuration artifact
- Content-addressable via SHA-256
- Includes metadata (generator, changelog)

#### Value Objects

**ValidationResult**
- Contains validation status, errors, warnings
- Immutable validation outcome

**PublishResult**
- Contains artifact_id, status, metadata
- Immutable publish outcome

#### Repositories

**ArtifactStore**
- Content-addressable storage
- Profile index management
- Atomic write operations

## Dependencies

### From Other Capabilities
- **Config Building:** Draft configuration from ConfigBuilder
- **Cryptographic Signing:** Ed25519 signature generation
- **Content Addressing:** SHA-256 artifact ID computation
- **Schema Validation:** Configuration validation from validate_config

### External Dependencies
- `cryptography` - Ed25519 signing
- `pydantic` - Data validation
- Filesystem - Artifact storage

## Success Criteria

### Functional
- [ ] User can validate config before publishing
- [ ] User can publish valid configs via MCP tool
- [ ] User can publish valid configs via CLI
- [ ] Invalid configs are rejected with clear errors
- [ ] Changelog is included in published artifacts
- [ ] Generator metadata is automatically added
- [ ] Artifacts are cryptographically signed
- [ ] Artifacts are content-addressable (SHA-256)

### Non-Functional
- [ ] Publishing completes in <1 second
- [ ] Validation completes in <100ms
- [ ] Test coverage ≥70%
- [ ] All BDD scenarios pass
- [ ] E2E value scenario passes

## Wave Alignment

**Wave 1.4 (v0.1.4) - Schema Validation**
- Goal: Validate draft configs before publishing
- Deliverables:
  - Publishing workflow module
  - Enhanced metadata support
  - Validation integration
  - CLI command
  - E2E documentation

## Spec Coverage

- ✅ **FR-6:** Validate before release (validate_config integration)
- ✅ **FR-11:** Include change metadata (changelog in artifact.metadata)
- ⚠️ **FR-12:** Record release entries (partial - no approval workflow yet)

## Future Evolution

### Wave 2.x: HTTP Publishing API
- REST API for remote publishing
- Webhook notifications on publish
- Multi-client publishing support

### Wave 3.x: Approval Workflow
- Multi-signature approval
- Policy-based publishing gates
- Audit trail of approvals

## References

- [WAVE_1X_PLAN.md](../WAVE_1X_PLAN.md) - Wave 1.4 scope
- [DEVELOPMENT_LIFECYCLE.md](../DEVELOPMENT_LIFECYCLE.md) - Development process
- [mcp-tools.md](../../user-docs/reference/mcp-tools.md) - Tool API reference
