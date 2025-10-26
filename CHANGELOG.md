# Changelog

All notable changes to mcp-orchestration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Claude-Specific Development Framework** (chora-base v3.3.0 upgrade):
  - **CLAUDE.md** - Claude-optimized development guide for mcp-orchestration
    - 200k context window optimization strategies
    - MCP-specific development patterns
    - Wave-based development guidance
    - Domain-specific context management
  - **Claude Pattern Library** (claude/ directory - 5 files):
    - [claude/README.md](claude/README.md) - Pattern library index and quick reference
    - [claude/CONTEXT_MANAGEMENT.md](claude/CONTEXT_MANAGEMENT.md) - Progressive loading strategies
    - [claude/CHECKPOINT_PATTERNS.md](claude/CHECKPOINT_PATTERNS.md) - Session state preservation
    - [claude/METRICS_TRACKING.md](claude/METRICS_TRACKING.md) - ROI measurement framework
    - [claude/FRAMEWORK_TEMPLATES.md](claude/FRAMEWORK_TEMPLATES.md) - Proven request templates
  - **Domain-Specific CLAUDE.md Files**:
    - [tests/CLAUDE.md](tests/CLAUDE.md) - Test generation patterns for MCP tools
    - [docker/CLAUDE.md](docker/CLAUDE.md) - Docker assistance for MCP server deployment
    - [scripts/CLAUDE.md](scripts/CLAUDE.md) - Script automation patterns
    - [.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md) - Memory integration for wave tracking
  - **ROI Calculator Utility** - [src/mcp_orchestrator/utils/claude_metrics.py](src/mcp_orchestrator/utils/claude_metrics.py)
    - ClaudeMetric dataclass for session tracking
    - ClaudeROICalculator for time/cost savings analysis
    - Quality metrics tracking (coverage, iterations, bug rate)
  - **CLAUDE_SETUP_GUIDE.md** - Comprehensive Claude setup guide (1,151 lines)

**Claude Advantages for mcp-orchestration:**
- 20-40 second setup advantage vs generic agents
- 2-minute session recovery from checkpoints (saves 13-18 minutes)
- Progressive context loading optimized for 200k token window
- Multi-tool orchestration for parallel MCP development
- Quantifiable ROI tracking for development metrics

### Changed
- **Documentation Structure**: Migrated docs/ directory to three-directory structure
  - Moved ecosystem vision docs to `dev-docs/vision/`
  - Moved capability specs to `project-docs/capabilities/`
  - Moved telemetry signals to `project-docs/telemetry/signals/`
  - Moved developer E2E guide to `dev-docs/how-to/`
  - Updated all references in code, configs, and documentation
  - Removed obsolete documentation (superseded by user-docs)

- **Comprehensive Diataxis Documentation** (Wave 1.3):
  - Tutorial: "Your First MCP Configuration" ([user-docs/tutorials/01-first-configuration.md](user-docs/tutorials/01-first-configuration.md))
  - Reference: Complete MCP Tools API reference ([user-docs/reference/mcp-tools.md](user-docs/reference/mcp-tools.md))
  - Explanations: Cryptographic Signing and Draft Workflow concepts
  - How-To Guides: Get Started, Add/Remove Servers, Add Clients, Add to Registry
- **File Naming Standards**: Codified conventions in DOCUMENTATION_STANDARD.md
  - How-to guides: Descriptive names (task-oriented, non-sequential)
  - Tutorials: Numbered (sequential learning path)

## 0.1.5 - 2025-10-26

### Added
- **Configuration Deployment Workflow** (Wave 1.5 - End-to-End Config Management):
  - **Deployment Workflow Module** ([src/mcp_orchestrator/deployment/workflow.py](src/mcp_orchestrator/deployment/workflow.py)):
    - `DeploymentWorkflow` - Domain service orchestrating fetch → verify → write → log
    - `DeploymentError` - Exception class for deployment failures with error codes
    - Atomic deployment operations with rollback on write failure
    - Signature verification before deployment
    - Parent directory creation if needed
    - Cross-platform support (macOS, Linux, Windows)

  - **Deployment Log Module** ([src/mcp_orchestrator/deployment/log.py](src/mcp_orchestrator/deployment/log.py)):
    - `DeploymentLog` - Repository for deployment history tracking
    - `DeploymentRecord` - Immutable deployment log entry
    - Methods: `record_deployment()`, `get_deployed_artifact()`, `get_deployment_history()`
    - Enables configuration drift detection

  - **MCP Tool**: `deploy_config` - Automated deployment to client config locations
    - Deploys latest or specific artifact version (rollback support)
    - Verifies Ed25519 signature before writing
    - Writes to client-specific config paths automatically
    - Records deployment in deployment log
    - Error codes: CLIENT_NOT_FOUND, ARTIFACT_NOT_FOUND, SIGNATURE_INVALID, WRITE_FAILED
    - Performance: Deployment completes in <2 seconds

  - **MCP Resources** (2 new):
    - `config://{client_id}/{profile_id}/latest` - Query latest published artifact
    - `config://{client_id}/{profile_id}/deployed` - Query currently deployed artifact
    - Includes drift detection (deployed vs latest comparison)

  - **CLI Command**: `mcp-orchestration-deploy-config` ([cli_building.py:deploy_config](src/mcp_orchestrator/cli_building.py))
    - Deploy configuration to client's config location
    - Supports version pinning with `--artifact-id` option
    - Text and JSON output formats
    - Helpful error messages with troubleshooting guidance
    - Example: `mcp-orchestration-deploy-config --client claude-desktop --profile default`

### Changed
- **Server Capabilities**: Updated to version 0.1.5
  - Added `deploy_config` to tools list (Total: 10 tools)
  - Added `config://latest` and `config://deployed` resources (Total: 7 resources)
  - Added `automated_deployment` and `deployment_logging` feature flags

- **CLI Building Module**: Updated docstring to include Wave 1.5 deployment commands

### Fixed
- **Critical: `publish_config` MCP Tool Serialization** ([server.py](src/mcp_orchestrator/mcp/server.py)):
  - Fixed "No result received from client-side tool execution" error
  - Added comprehensive logging throughout publish workflow
  - Added explicit JSON serialization of all result fields (str, int primitives)
  - Added comprehensive exception handling for ValidationError, ValueError, StorageError
  - Added nested try-catch around workflow.publish() to catch signing/storage failures
  - Result: 100% reliable publishing with detailed error messages
  - See: [project-docs/wave_1-5/PUBLISH_CONFIG_FIX.md](project-docs/wave_1-5/PUBLISH_CONFIG_FIX.md)

- **Test Coverage Gap: Publish Without Keys** ([tests/test_mcp_publish_tool.py](tests/test_mcp_publish_tool.py)):
  - Added `test_publish_without_signing_keys` - Tests workflow fails gracefully when keys missing
  - Added `test_publish_config_error_message_quality` - Tests error is JSON-serializable
  - Resolves Test 3.5 from E2E testing (was PARTIAL due to environmental limitation)
  - Phase 3 now at 100% pass rate (7/7 tests)
  - See: [project-docs/wave_1-5/TEST_3.5_FIX.md](project-docs/wave_1-5/TEST_3.5_FIX.md)

### Documentation
- **User Documentation Restructuring** (Wave 1.5 completion):
  - **New Unified Guide**: [user-docs/how-to/complete-workflow.md](user-docs/how-to/complete-workflow.md)
    - End-to-end workflow: Installation → Build → Validate → Publish → Deploy
    - Both conversational (Claude) and CLI workflows
    - Key concepts section defining draft/published/deployed states
    - Maintenance workflows (update, rollback, drift detection)
    - Comprehensive troubleshooting guide
    - Curated from 1,061 → 714 lines (32.7% reduction) for clarity

  - **Updated How-To Guides** (5 guides curated for clarity):
    - [user-docs/how-to/manage-configs-with-claude.md](user-docs/how-to/manage-configs-with-claude.md) - Added Step 7: Deploy
    - [user-docs/how-to/deploy-config.md](user-docs/how-to/deploy-config.md) - Curated 505 → 440 lines
    - [user-docs/how-to/publish-config.md](user-docs/how-to/publish-config.md) - Curated 431 → 408 lines
    - [user-docs/how-to/add-server-to-config.md](user-docs/how-to/add-server-to-config.md) - Curated 429 → 384 lines
    - [user-docs/how-to/remove-server-from-config.md](user-docs/how-to/remove-server-from-config.md) - Enhanced 337 → 339 lines

  - **Updated Tutorial**: [user-docs/tutorials/01-first-configuration.md](user-docs/tutorials/01-first-configuration.md)
    - Added Steps 9-11: Deploy, Restart, Test
    - Now covers complete workflow end-to-end

  - **Legacy Guide Markers**: 4 guides marked with warnings
    - [user-docs/how-to/verify-signatures.md](user-docs/how-to/verify-signatures.md) - Now automatic in deploy_config
    - [user-docs/how-to/check-config-updates.md](user-docs/how-to/check-config-updates.md) - Now built into drift detection
    - [user-docs/how-to/use-config.md](user-docs/how-to/use-config.md) - Now automated deployment
    - [user-docs/how-to/get-first-config.md](user-docs/how-to/get-first-config.md) - Now build your own

  - **Updated Navigation**: [user-docs/README.md](user-docs/README.md)
    - Restructured Quick Start with "START HERE" path
    - Clear beginner → advanced progression

### Testing
- **Unit Tests** (10 deployment tests - [tests/test_deployment_workflow.py](tests/test_deployment_workflow.py)):
  - Deploy latest artifact workflow
  - Deploy specific artifact by ID (version pinning)
  - Deploy to unknown client (error handling)
  - Invalid artifact ID handling
  - Signature verification before deployment
  - Invalid signature rejection
  - Parent directory creation
  - Atomic deployment with rollback on failure
  - Deployment logging
  - Query deployed vs latest (drift detection)

- **Publish Tool Tests** (5 tests - [tests/test_mcp_publish_tool.py](tests/test_mcp_publish_tool.py)):
  - Workflow returns JSON-serializable result
  - Error messages are JSON-serializable
  - Result format correctness (all fields primitive types)
  - Publish without signing keys (graceful failure)
  - Error message quality (helpful and actionable)

- **E2E Value Scenarios** (6 total):
  - Deployment scenarios (3 tests - [tests/value-scenarios/test_deploy_config.py](tests/value-scenarios/test_deploy_config.py))
  - Publishing scenarios (3 tests - [tests/value-scenarios/test_publish_config.py](tests/value-scenarios/test_publish_config.py))

- **Test Coverage**: **185 tests passing** (99.5%), 1 pre-existing telemetry test excluded
  - +5 new tests from publish_config fix and Test 3.5 resolution
  - All phases at 100% pass rate (Phases 1-5)

- **E2E Testing Report**: [project-docs/wave_1-5/FINDINGS-REPORT.md](project-docs/wave_1-5/FINDINGS-REPORT.md)
  - 35/35 test scenarios executed (100% coverage)
  - 34 passed, 1 partial (environmental limitation resolved with unit tests)
  - **Overall Assessment**: 🟢 PRODUCTION READY - RECOMMENDED FOR RELEASE
  - Phase 1 (Discovery): 100% ✅
  - Phase 2 (Draft Management): 100% ✅
  - Phase 3 (Validation & Publishing): 100% ✅
  - Phase 4 (Deployment): 100% ✅
  - Phase 5 (Advanced Workflows): 100% ✅

- **Capability Specification** ([project-docs/capabilities/config-deployment.md](project-docs/capabilities/config-deployment.md)):
  - Domain model: DeploymentWorkflow, DeploymentRecord, DeploymentResult, ClientConfigLocation
  - Behaviors, value scenarios, integrations
  - Success criteria and wave alignment
  - Future evolution roadmap (Wave 1.6: Audit & History, Wave 2.x: Remote Deployment API)

- **BDD Specification** ([project-docs/capabilities/behaviors/mcp-config-deploy.feature](project-docs/capabilities/behaviors/mcp-config-deploy.feature)):
  - 12 Gherkin scenarios covering deployment workflows
  - Happy paths: deploy latest, deploy specific version, CLI/MCP workflows
  - Error cases: unknown client, invalid artifact, signature verification, write failures
  - Security: signature verification before deployment
  - Infrastructure: parent directory creation, atomic rollback

- **How-To Guide** ([user-docs/how-to/deploy-config.md](user-docs/how-to/deploy-config.md)):
  - Complete deployment workflow guide (6,500+ words)
  - Step-by-step instructions for MCP tool and CLI deployment
  - Deploy specific versions (version pinning / rollback)
  - Configuration drift detection with resource queries
  - Complete end-to-end workflow example
  - Troubleshooting section with 6 common error scenarios
  - Deployment internals explanation (atomic operations, rollback guarantees)

- **API Reference**: Updated with:
  - `deploy_config` tool documentation
  - `config://latest` and `config://deployed` resource documentation
  - Complete workflow examples from discover → deploy

### Architecture
- **Domain-Driven Design**:
  - **Service**: `DeploymentWorkflow` - Orchestrates deployment with validation, verification, atomic writes
  - **Entity**: `DeploymentRecord` - Immutable deployment log entry
  - **Value Objects**: `DeploymentResult`, `ClientConfigLocation`
  - **Repository**: `DeploymentLog` - Deployment history storage and queries

- **Behavior-Driven Development**:
  - All features specified in Gherkin before implementation
  - 12 BDD scenarios with Given/When/Then structure
  - @behavior:MCP.CONFIG.DEPLOY tag for traceability

- **Test-Driven Development**:
  - All unit tests written before implementation (RED → GREEN → REFACTOR)
  - E2E tests validate how-to guides (living documentation)
  - 100% BDD scenario coverage

### Spec Coverage
- ✅ **UC-1**: Bootstrap (first-time client setup with automated deployment)
- ✅ **UC-2**: Routine Update (update existing configs with automated deployment)
- ⚠️ **UC-3** (partial): Emergency Revert (can deploy previous artifact, no rollback UX yet)
- ✅ **End-to-End Workflow**: Complete discover → build → validate → publish → deploy workflow operational

### Deployment Behavior
The deployment workflow ensures:
- **Security**: Ed25519 signature verification before every deployment
- **Safety**: Atomic file operations with automatic rollback on failure
- **Reliability**: Parent directory creation, proper error handling
- **Auditability**: Full deployment history with timestamps and changelogs
- **Drift Detection**: Query deployed vs latest to detect configuration staleness

### Client Config Locations
Configurations are deployed to client-specific locations:
- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor**: `~/.cursor/mcp_config.json`

After deployment, restart the client application to load the new configuration.

## 0.1.4 - 2025-10-25

### Added
- **Configuration Validation and Publishing Workflow** (Wave 1.4 - Full Scope):
  - **Publishing Workflow Module** ([src/mcp_orchestrator/publishing/workflow.py](src/mcp_orchestrator/publishing/workflow.py)):
    - `PublishingWorkflow` - Domain service orchestrating validation → signing → storage
    - `ValidationError` - Exception class for validation failures with detailed error reporting
    - Atomic publishing operations with automatic rollback on failure
    - Metadata enrichment (generator, changelog, server_count)

  - **MCP Tool**: `validate_config` - Comprehensive pre-publish configuration validation
    - Validates server structure (command, args, env format)
    - Checks client-specific limitations (max servers, max env vars per server)
    - Returns detailed errors and warnings with error codes
    - Performance: p95 < 100ms

  - **CLI Command**: `mcp-orchestration-publish-config` ([cli_building.py:publish_config](src/mcp_orchestrator/cli_building.py))
    - Publish configuration from JSON file with validation
    - Automatic cryptographic signing with Ed25519
    - Content-addressable storage (SHA-256)
    - Text and JSON output formats
    - Example: `mcp-orchestration-publish-config --client claude-desktop --profile default --file config.json --changelog "Initial setup"`

### Changed
- **Enhanced `publish_config` MCP Tool**:
  - Now uses `PublishingWorkflow` for integrated validation
  - Automatically validates configuration before signing
  - Provides detailed validation error messages with error codes
  - Updated workflow documentation: browse → add → view → **validate** → publish

- **Server Capabilities**: Updated to version 0.1.4
  - Added `validate_config` to tools list
  - Added `schema_validation` and `pre_publish_validation` feature flags

### Testing
- **Unit Tests** (10 tests - [tests/test_publishing_workflow.py](tests/test_publishing_workflow.py)):
  - Validation integration with publish workflow
  - Metadata enrichment (changelog, generator, server_count)
  - Atomic operations with rollback on failure
  - Cryptographic signing integration
  - Profile index updates

- **Validation Tests** (12 tests - [tests/test_validate_config.py](tests/test_validate_config.py)):
  - Empty config validation
  - Valid config scenarios
  - Structural validation (missing fields, invalid types)
  - Warning scenarios (empty env vars)
  - Client limitation enforcement

- **E2E Value Scenarios** (3 tests - [tests/value-scenarios/test_publish_config.py](tests/value-scenarios/test_publish_config.py)):
  - Full workflow: initialize → browse → add → validate → publish → verify
  - Publishing with validation errors
  - Empty config rejection
  - All tests validate corresponding how-to guide: [user-docs/how-to/publish-config.md](user-docs/how-to/publish-config.md)

- **Test Coverage**: All 167 tests passing (up from 155), excluding 1 pre-existing telemetry test failure

### Documentation
- **Development Process** ([project-docs/DEVELOPMENT_LIFECYCLE.md](project-docs/DEVELOPMENT_LIFECYCLE.md)):
  - Comprehensive 8-phase development lifecycle documentation
  - Vision-Driven Development with BDD/TDD/DDD practices
  - Value Scenarios as E2E tests (living documentation)
  - Templates and examples for each phase

- **Capability Specification** ([project-docs/capabilities/config-publishing.md](project-docs/capabilities/config-publishing.md)):
  - Domain model: PublishingWorkflow, ConfigArtifact, ValidationResult
  - Behaviors, value scenarios, integrations
  - Success criteria and wave alignment

- **BDD Specification** ([project-docs/capabilities/behaviors/mcp-config-publish.feature](project-docs/capabilities/behaviors/mcp-config-publish.feature)):
  - 12 Gherkin scenarios covering publish workflows
  - Happy paths, error cases, CLI/MCP integration

- **How-To Guide** ([user-docs/how-to/publish-config.md](user-docs/how-to/publish-config.md)):
  - Complete publishing workflow guide (6,500 words)
  - Step-by-step instructions with code examples
  - Troubleshooting section with common errors
  - Metadata and workflow internals explained

- **API Reference**: Updated [user-docs/reference/mcp-tools.md](user-docs/reference/mcp-tools.md) with:
  - `validate_config` tool documentation
  - Enhanced `publish_config` documentation showing validation integration
  - Complete workflow examples

### Architecture
- **Domain-Driven Design**:
  - **Service**: `PublishingWorkflow` - Coordinates validation, signing, storage
  - **Entity**: `ConfigArtifact` - Immutable signed configuration
  - **Value Objects**: `ValidationResult`, `PublishResult`
  - **Repository**: `ArtifactStore` - Content-addressable storage

- **Behavior-Driven Development**:
  - All features specified in Gherkin before implementation
  - 12 BDD scenarios with Given/When/Then structure
  - @behavior tags for traceability

- **Test-Driven Development**:
  - All unit tests written before implementation (RED → GREEN → REFACTOR)
  - E2E tests validate how-to guides (living documentation)
  - 100% BDD scenario coverage

### Spec Coverage
- ✅ **FR-6**: Validate before release (integrated validation in publish workflow)
- ✅ **FR-11**: Include change metadata (changelog in artifact.metadata)
- ⚠️ **FR-12** (partial): Record release entries (no approval workflow yet)

## 0.1.3 - 2025-10-24

### Added
- **Ergonomic Tools for Claude Desktop** (Wave 1.3):
  - `view_draft_config` - View current draft configuration without modifying it
  - `clear_draft_config` - Clear all servers from draft to start fresh
  - `initialize_keys` - Autonomous key generation (no CLI required)
- **Default Parameters**: All config management tools now default to `client_id="claude-desktop"` and `profile_id="default"` for easier usage
- **Improved Documentation**: Tool descriptions now include clearer examples and cross-references to related tools

### Changed
- **Parameter Order**: Reordered parameters in `add_server_to_config`, `remove_server_from_config`, and `publish_config` to put required params first, optional defaults last
- **Workflow Guidance**: Updated `publish_config` to reference `initialize_keys` tool instead of CLI command

## 0.1.2 - 2025-10-24

### Fixed
- **Claude Desktop Compatibility**: Fixed parameter validation in `add_server_to_config` tool to handle JSON string serialization of params and env_vars (Claude Desktop passes these as strings rather than objects)

### Added
- **Transport Abstraction**: Automatic mcp-remote wrapping for HTTP/SSE servers
  - `ServerRegistry.to_client_config()` method for generating client-ready configs
  - Stdio servers: Direct passthrough with parameter substitution
  - HTTP/SSE servers: Transparent mcp-remote wrapper (users never see implementation details)
  - Parameter substitution in `{placeholder}` format for URLs and command args
- **Config Builder Module** (`src/mcp_orchestrator/building/`):
  - `ConfigBuilder` class for managing draft configurations
  - Methods: `add_server()`, `remove_server()`, `build()`, `to_artifact()`
  - In-memory draft state management
  - Automatic transport abstraction when adding servers
- **MCP Tools** (3 new - Total: 9):
  - `add_server_to_config`: Add MCP server to draft configuration
  - `remove_server_from_config`: Remove server from draft configuration
  - `publish_config`: Publish draft as signed artifact (completes workflow)
- **MCP Resources** (1 new - Total: 5):
  - `config://{client_id}/{profile_id}/draft`: View current draft configuration
- **CLI Commands** (2 new - Total: 6):
  - `mcp-orchestration-add-server`: Add server to config via CLI
  - `mcp-orchestration-remove-server`: Remove server from config via CLI

### Changed
- Updated MCP server version to 0.1.2
- Updated capabilities resource to reflect Wave 1.2 features

### Testing
- Added 35 unit tests (16 transport abstraction + 19 config builder)
- All 126 tests passing (up from 91)
- 70%+ coverage maintained

### Spec Coverage
- ✅ FR-5: Full parameter injection support
- Foundation for FR-6 (schema validation - Wave 1.3)

## 0.1.1 - 2025-10-24

### Added
- **Server Registry**: Catalog of 15 known MCP servers with metadata
  - 13 stdio servers (filesystem, brave-search, github, memory, fetch, postgres, sqlite, slack, puppeteer, google-maps, everything, sequential-thinking, sentry)
  - 2 HTTP/SSE servers (n8n, custom-api)
- **MCP Tools** (2 new):
  - `list_available_servers`: Browse server catalog with filtering and search
  - `describe_server`: Get detailed server information including usage examples
- **MCP Resources** (2 new):
  - `server://registry`: Full server registry as JSON
  - `server://{server_id}`: Detailed server definition as JSON
- **CLI Commands** (2 new):
  - `mcp-orchestration-list-servers`: List and search servers
  - `mcp-orchestration-describe-server`: View server details
- **Server Models**:
  - `ServerDefinition`: Server metadata with transport configuration
  - `TransportType`: Enum for stdio, HTTP, SSE transports
  - `ParameterDefinition`: Configuration parameter definitions
  - `ServerRegistry`: Registry class with search and filtering

### Changed
- Updated MCP server version to 0.1.1
- Updated capabilities resource to reflect new tools and resources

### Documentation
- Added E2E guide: `docs/how-to/browse-server-registry.md`
- Added Wave 1.x planning document: `project-docs/WAVE_1X_PLAN.md`
- Updated ROADMAP.md with wave breakdown

### Testing
- Added 24 unit tests for server registry (100% coverage of new modules)
- All 91 tests passing

## 0.1.0 - 2025-10-17

### Added
- **Wave 1.0: Foundation**
- MCP server with stdio transport
- 4 MCP tools: list_clients, list_profiles, get_config, diff_config
- 2 MCP resources: capabilities://server, capabilities://clients
- Client registry for Claude Desktop and Cursor
- Content-addressable artifact storage with Ed25519 signing
- Cryptographic signing and verification
- Configuration diff engine
- CLI command: `mcp-orchestration-init` for sample configs
- Testing infrastructure with 70%+ coverage
- Project scaffolding from chora-base template
- Core infrastructure and documentation

