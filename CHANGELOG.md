# Changelog

All notable changes to mcp-orchestration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

