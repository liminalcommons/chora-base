# Changelog

All notable changes to mcp-orchestration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Documentation Structure**: Migrated docs/ directory to three-directory structure
  - Moved ecosystem vision docs to `dev-docs/vision/`
  - Moved capability specs to `project-docs/capabilities/`
  - Moved telemetry signals to `project-docs/telemetry/signals/`
  - Moved developer E2E guide to `dev-docs/how-to/`
  - Updated all references in code, configs, and documentation
  - Removed obsolete documentation (superseded by user-docs)

### Added
- **Comprehensive Diataxis Documentation** (Wave 1.3):
  - Tutorial: "Your First MCP Configuration" ([user-docs/tutorials/01-first-configuration.md](user-docs/tutorials/01-first-configuration.md))
  - Reference: Complete MCP Tools API reference ([user-docs/reference/mcp-tools.md](user-docs/reference/mcp-tools.md))
  - Explanations: Cryptographic Signing and Draft Workflow concepts
  - How-To Guides: Get Started, Add/Remove Servers, Add Clients, Add to Registry
- **File Naming Standards**: Codified conventions in DOCUMENTATION_STANDARD.md
  - How-to guides: Descriptive names (task-oriented, non-sequential)
  - Tutorials: Numbered (sequential learning path)

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

