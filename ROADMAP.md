# Roadmap - mcp-orchestration

This document outlines **committed features and timelines** for mcp-orchestration.

**Status:** Living document (updated with each release)
**Current Version:** 0.1.5 (Wave 1.x complete)
**Next Milestone:** 0.2.0 (Wave 2.0 - HTTP Transport)

---

## Current Focus

### v0.2.0 (Wave 2.0 - HTTP/SSE Transport Foundation) — IN PROGRESS

**Target:** Feb 2026 (6-8 weeks)
**Status:** Planning → Implementation (Started 2025-10-25)

**Goal:** Multi-transport architecture (stdio + HTTP/SSE) with authentication for ecosystem integration

**Features:**

- [ ] **HTTP Transport Server** - FastAPI-based HTTP server exposing all MCP tools
- [ ] **Authentication** - Bearer token + API key support
- [ ] **10 HTTP Endpoints** - All MCP tools available via REST API
- [ ] **CLI Commands** - `serve-http`, `generate-token`
- [ ] **Migration Guide** - stdio → HTTP migration path
- [ ] **API Documentation** - Complete HTTP API reference
- [ ] **Docker Support** - Containerized deployment (optional)
- [ ] **Backward Compatibility** - stdio transport still supported

**Success Criteria:**
- All 10 MCP tools available via HTTP endpoints
- Bearer token authentication enforced
- p95 < 300ms for HTTP requests (NFR-3)
- stdio backward compatible (no breaking changes)
- Coverage ≥85% for new HTTP code
- 3 E2E value scenarios pass

**See**: [project-docs/WAVE_2X_PLAN.md](project-docs/WAVE_2X_PLAN.md) for complete wave breakdown

---

## Near-Term Roadmap (Wave 2.x Series)

### Upcoming Waves

The roadmap follows an incremental wave-based delivery model. Each wave builds on the previous:

**Wave 2.1 (v0.2.1)** - API Enhancements (Late Feb - Early Mar 2026)
- Universal Loadability Format adoption (mcp-gateway alignment)
- Enhanced error responses with error codes
- Remote validation API improvements
- Structured error messages

**Wave 2.2 (v0.2.2)** - Ecosystem Integration (Mar 2026)
- Integration testing with mcp-gateway
- Example n8n workflows (3+)
- Pattern N3b implementation
- Performance optimization (caching, connection pooling)
- Metrics & monitoring integration

**Wave 3.x** - Governance & Intelligence (Q2+ 2026 - Exploratory)
- Policy engine for configuration governance
- Approval workflows
- Multi-signer support
- Configuration analytics
- Multi-tenant architecture

**See**: [project-docs/WAVE_2X_PLAN.md](project-docs/WAVE_2X_PLAN.md) for detailed Wave 2.x planning

---

## Future Vision: Capability Evolution

**See:** [dev-docs/vision/](dev-docs/vision/) for long-term capability vision.

**Note:** Vision documents describe **potential evolutionary directions** based on
founding vision and anticipated needs. These are **NOT committed features** - they
represent possible future development after current roadmap stabilizes.

**Current Priority:** v0.1.0 remains the focus. Future capabilities will be
evaluated after v0.1.0 based on user needs and adoption.

### Vision Highlights

The evolution explores potential capability waves beyond v0.1.0:

**Wave 1: Foundation** (Current)
- Status: In development (v0.1.0)
- Focus: Core functionality, essential features
- Delivery: [Target date]

**Wave 2: [Next Capability Theme]** (Post-v0.1.0 Vision)
- Status: Exploratory (not committed)
- Focus: [Brief description of next wave]
- Decision: After v0.1.0 stabilizes, based on:
  - User demand signals (issues, feedback, adoption)
  - Technical validation (architecture supports extensions)
  - Team capacity (resources available for next phase)

**Example Wave 2 Themes (Exploratory):**
- Tool chaining and composition
- External API integrations
- Data persistence and caching
- Advanced configuration
**See [dev-docs/vision/CAPABILITY_EVOLUTION.md](dev-docs/vision/CAPABILITY_EVOLUTION.md) for:**
- Detailed wave descriptions
- Decision criteria (go/no-go frameworks)
- Success metrics
- Technical sketches
- Quarterly review process

**Key Principle:** Build for today, design for tomorrow. Vision guides architectural
decisions *today* without committing to timelines *tomorrow*.

---

## Release History

### v0.1.5 (Wave 1.5 - Deployment) ✅

**Released:** 2025-10-25
**Status:** Current

**Features:**
- **Deployment Workflow**: Automated config deployment to client locations
- **MCP Tool**: `deploy_config` - Deploy latest or specific artifact
- **MCP Resources**: `config://latest`, `config://deployed` (drift detection)
- **CLI Command**: `mcp-orchestration-deploy-config`
- **Deployment Log**: Track deployment history
- **Testing**: 185 tests passing (99.5%)

**Spec Coverage**: UC-1 (Bootstrap), UC-2 (Routine Update)

---

### v0.1.4 (Wave 1.4 - Validation + Publishing) ✅

**Released:** 2025-10-24

**Features:**
- **Publishing Workflow**: Validated configuration publishing
- **MCP Tool**: `validate_config`, enhanced `publish_config`
- **CLI Command**: `mcp-orchestration-publish-config`
- **Testing**: 167 tests passing

**Spec Coverage**: FR-6 (Validation), FR-11 (Change metadata)

---

### v0.1.3 (Wave 1.3 - Ergonomics) ✅

**Released:** 2025-10-24

**Features:**
- **Ergonomic Tools**: `view_draft_config`, `clear_draft_config`, `initialize_keys`
- **Default Parameters**: Reduced boilerplate by 50%+
- **Testing**: 143 tests passing

---

### v0.1.2 (Wave 1.2 - Config Generation) ✅

**Released:** 2025-10-24

**Features:**
- **Transport Abstraction**: Auto mcp-remote wrapping for HTTP/SSE
- **Config Builder**: Draft configuration management
- **MCP Tools**: `add_server_to_config`, `remove_server_from_config`, `publish_config`
- **Testing**: 126 tests passing

**Spec Coverage**: FR-5 (Parameter injection)

---

### v0.1.1 (Wave 1.1 - Server Registry) ✅

**Released:** 2025-10-24

**Features:**
- **Server Registry**: Catalog of 15 MCP servers
- **MCP Tools**: `list_available_servers`, `describe_server`
- **MCP Resources**: `server://registry`, `server://{id}`
- **Testing**: 91 tests passing

---

### v0.1.0 (Wave 1.0 - Foundation) ✅

**Released:** 2025-10-17

**Features:**
- **MCP Server**: stdio-based server exposing tools/resources
- **4 MCP Tools**: `list_clients`, `list_profiles`, `get_config`, `diff_config`
- **2 MCP Resources**: `capabilities://server`, `capabilities://clients`
- **Client Registry**: Metadata for Claude Desktop, Cursor
- **Artifact Storage**: Content-addressable storage with Ed25519 signing
- **CLI**: `mcp-orchestration init-configs`, basic artifact management
- **Testing**: 70%+ coverage

**Spec Coverage**: FR-1, FR-2, FR-3, FR-4, FR-9

---

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

---

## Roadmap Philosophy

### Committed vs. Exploratory

| Type | Description | Location | Changes |
|------|-------------|----------|---------|
| **Committed** | Features with timelines | This document (ROADMAP.md) | Stable, changes = scope change |
| **Exploratory** | Potential future directions | [dev-docs/vision/](dev-docs/vision/) | Fluid, updated quarterly |
### Roadmap Updates

**Frequency:** Updated with each release and major milestone
**Process:**
1. Delivered features move to Release History
2. Next version features move to Current Focus
3. Planned features shift to Near-Term Roadmap
4. Exploratory features stay in vision documents until committed
### Feedback & Requests

**Feature Requests:** [GitHub Issues](https://github.com/liminalcommons/mcp-orchestration/issues)
**Discussions:** [GitHub Discussions](https://github.com/liminalcommons/mcp-orchestration/discussions)

**Note:** All requests are considered, but inclusion in roadmap depends on:
- Alignment with project vision
- User demand and adoption
- Team capacity and resources
- Technical feasibility

---

## Contributing to Roadmap

Want to influence the roadmap?

1. **Use the project** - Adoption signals value
2. **File issues** - Describe your needs clearly
3. **Contribute code** - PRs for features you need
4. **Join discussions** - Share your use cases
5. **Review vision docs** - Comment on exploratory waves in [dev-docs/vision/](dev-docs/vision/)
---

**Last Updated:** 2025-10-25
**Version:** v0.1.5 → v0.2.0 (in progress)
**Status:** Living document

🗺️ This roadmap reflects committed work. See:
- [project-docs/WAVE_2X_PLAN.md](project-docs/WAVE_2X_PLAN.md) for detailed Wave 2.x planning
- [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for Wave 1.x history
- [dev-docs/vision/](dev-docs/vision/) for long-term possibilities