# Roadmap - mcp-orchestration

This document outlines **committed features and timelines** for mcp-orchestration.

**Status:** Living document (updated with each release)
**Current Version:** 0.1.0

---

## Current Focus

### v0.1.1 (Wave 1.1 - Server Registry) — IN PROGRESS

**Target:** TBD
**Status:** Planning

**Goal:** Enable users to discover and register available MCP servers

**Features:**

- [ ] **Server Registry Module** - Catalog of known MCP servers
- [ ] **Server Definitions** - 10-15 default servers (stdio + HTTP/SSE)
- [ ] **MCP Tools** - `list_available_servers`, `describe_server`
- [ ] **MCP Resources** - `server://registry`, `server://{id}`
- [ ] **CLI Commands** - `list-servers`, `describe-server`
- [ ] **Documentation** - E2E guide for browsing server registry

**Success Criteria:**
- Users can browse available MCP servers via CLI and MCP tools
- Registry includes both stdio and HTTP/SSE servers
- Coverage ≥70% for new code
- E2E guide complete

**See**: [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for complete wave breakdown

---

## Near-Term Roadmap (Wave 1.x Series)

### Upcoming Waves

The roadmap follows an incremental wave-based delivery model. Each wave builds on the previous:

**Wave 1.2 (v0.1.2)** - Transport Abstraction + Config Generation
- Generate client configs from server registry
- Automatic mcp-remote wrapping for HTTP/SSE servers
- `add_server_to_config`, `remove_server_from_config` tools

**Wave 1.3 (v0.1.3)** - Schema Validation
- Validate draft configs before publishing
- `validate_draft` tool with detailed error reporting
- Client-specific JSON schemas

**Wave 1.4 (v0.1.4)** - Publishing Workflow
- Create and sign config artifacts
- `publish_config` tool
- Changelog support

**Wave 1.5 (v0.1.5)** - E2E Config Management
- Complete workflow: discover → build → validate → publish → deploy
- `deploy_config` tool
- End-to-end user tutorials

**Wave 1.6 (v0.1.6)** - Audit & History
- Config change tracking
- `get_config_history`, `get_audit_log` tools
- Immutable audit trail

**See**: [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for detailed planning

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

### v0.1.0 (Wave 1.0 - Foundation) ✅

**Released:** 2025-10-17
**Status:** Current

**Features:**
- **MCP Server**: stdio-based server exposing tools/resources
- **4 MCP Tools**: `list_clients`, `list_profiles`, `get_config`, `diff_config`
- **2 MCP Resources**: `capabilities://server`, `capabilities://clients`
- **Client Registry**: Metadata for Claude Desktop, Cursor
- **Artifact Storage**: Content-addressable storage with Ed25519 signing
- **CLI**: `mcp-orchestration init-configs`, basic artifact management
- **Testing**: 70%+ coverage

**Spec Coverage**: FR-1, FR-2, FR-3, FR-4, FR-9

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

**Last Updated:** 2025-10-24
**Version:** v0.1.0 → v0.1.1 (in progress)
**Status:** Living document

🗺️ This roadmap reflects committed work. See:
- [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for detailed wave planning
- [dev-docs/vision/](dev-docs/vision/) for long-term possibilities