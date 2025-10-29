# Wave 3 Execution Plan: MCP Extraction + chora-compose SAPs (v3.6.0)

**Created**: 2025-10-29
**Status**: Planning
**Target Release**: v3.6.0

---

## Overview

Wave 3 executes two parallel tracks:
1. **Primary Track**: SAP-014 (MCP Server Development) - Extract MCP-specific content
2. **Parallel Track**: SAP-017/018 (chora-compose ecosystem integration) - Inbox protocol demonstration

**Total Estimated Effort**: 80-108 hours (3-4 weeks)
**Target Release**: v3.6.0

---

## Strategic Context

**Why Wave 3 Matters**:
- Transforms chora-base from "MCP server template" → "Universal project foundation"
- Makes MCP an **optional capability** (SAP-014) rather than core assumption
- Demonstrates **ecosystem integration** (chora-compose SAPs)
- Validates **inbox protocol** for cross-conversation coordination
- Creates **template** for future framework SAPs (Django, FastAPI, React)

---

## Track 1: SAP-014 MCP Server Development (60-80h)

### Phase 1: MCP Specificity Audit (8-10h)

**Task 1.1: Create audit document**
- File: `docs/project-docs/mcp-specificity-audit.md`
- Categorize all content as:
  - **Pure MCP** → Move to SAP-014
  - **Python patterns** → Keep, ensure language-neutral
  - **Universal patterns** → Keep

**Task 1.2: Audit blueprints/** (9 files)
- All blueprints are MCP-specific → SAP-014
- server.py.blueprint, pyproject.toml.blueprint, etc.
- Document what each provides

**Task 1.3: Audit static-template/**
- Note: No `/mcp/` directory found (may not exist or already removed)
- Audit for MCP references in existing files

**Task 1.4: Audit root files**
- AGENTS.md - MCP server references
- CLAUDE.md - MCP client config examples
- README.md - "MCP server template" language

### Phase 2: Create SAP-014 Structure (15-20h)

**Task 2.1: Create SAP directory**
```
docs/skilled-awareness/mcp-server-development/
├── capability-charter.md      (why MCP servers, business value)
├── protocol-spec.md           (FastMCP, tools, resources, technical contracts)
├── awareness-guide.md         (agent guidance, development workflows)
├── adoption-blueprint.md      (how to add MCP to any project)
└── ledger.md                  (adoption tracking)
```

**Task 2.2: Write capability-charter.md**
- What: MCP server development capability
- Why: Enable LLM integration, tool exposure
- Who: MCP server developers, AI platform builders
- Dependencies: Python, FastMCP
- ROI: Rapid MCP server scaffolding

**Task 2.3: Write protocol-spec.md**
- MCP specification (version, protocol details)
- FastMCP vs alternatives
- Tool/resource/prompt patterns
- Testing patterns (mocking tools/resources)
- Deployment strategies
- Include code from blueprints/ as reference

**Task 2.4: Write awareness-guide.md**
- "When to Use" - 5 use cases + 4 anti-patterns
- MCP development workflow
- Common Pitfalls (5 scenarios)
- Related Content (4-domain coverage)
- Wave 2 enhancement pattern applied

**Task 2.5: Write adoption-blueprint.md**
- Prerequisites
- Installation steps (add MCP to existing project)
- Validation checklist
- Example: Transform generic Python project → MCP server

**Task 2.6: Write ledger.md**
- Initial adoption entry for chora-base itself
- Version 1.0.0

### Phase 3: Create 4-Domain Supporting Content (10-15h)

**Task 3.1: dev-docs/workflows/**
- `mcp-development-workflow.md` - How to build MCP servers (DDD/BDD/TDD for MCP)

**Task 3.2: user-docs/how-to/**
- `implement-mcp-server.md` - Step-by-step MCP server creation
- `configure-mcp-client.md` - Claude Desktop, Cursor configuration
- `test-mcp-tools.md` - Testing MCP tools/resources

**Task 3.3: user-docs/reference/**
- `mcp-protocol-spec.md` - MCP protocol reference
- `fastmcp-api-reference.md` - FastMCP API documentation

**Task 3.4: user-docs/explanation/**
- `why-mcp-servers.md` - Architecture, use cases, benefits

**Task 3.5: static-template/mcp-templates/**
- Move blueprints/ content here for SAP-014 installation
- server.py template, pyproject.toml template, etc.

### Phase 4: Generalize Root Documentation (8-12h)

**Task 4.1: Update AGENTS.md**
- Remove: "MCP server" assumptions
- Add: Language/framework-agnostic project description
- Add: "For MCP servers, see SAP-014"

**Task 4.2: Update CLAUDE.md**
- Remove: MCP client configuration examples
- Keep: Universal Claude guidance
- Add: Link to SAP-014 for MCP-specific patterns

**Task 4.3: Update README.md**
- Change: "MCP server template" → "Universal project foundation"
- Add: "Technology Stack" section (customizable)
- Add: "Suitable for" list (Python apps, MCP servers with SAP-014, web services, CLI tools)

**Task 4.4: Create new how-to guides**
- `docs/user-docs/how-to/start-new-project-from-chora-base.md`
- `docs/user-docs/how-to/customize-project-content.md`
- `docs/user-docs/how-to/upgrade-from-upstream.md`

### Phase 5: Delete blueprints/ and setup.py (2-3h)

**Task 5.1: Archive current state**
- Git tag: `v3.5.1-with-blueprints` (preserve history)

**Task 5.2: Move blueprints/ content**
- Copy to `static-template/mcp-templates/` (for SAP-014)
- Document in SAP-014 adoption-blueprint.md

**Task 5.3: Delete files**
- `blueprints/` directory (9 files)
- `setup.py` (443 lines)
- `AGENT_SETUP_GUIDE.md` (if exists)

**Task 5.4: Update references**
- SAP-003 (Project Bootstrap) - remove blueprints references
- Any other docs referencing setup.py

### Phase 6: Validation & Documentation (5-8h)

**Task 6.1: Update INDEX.md**
- Add SAP-014 entry
- Document as first "technology-specific SAP"

**Task 6.2: Run link validation**
- Validate SAP-014 links
- Validate updated root docs

**Task 6.3: Create wave-3-track-1-summary.md**
- Document MCP extraction process
- Metrics (files moved, lines added, etc.)

**Task 6.4: Test new workflow**
- Manually test clone & customize workflow
- Verify projects can be created with/without MCP

---

## Track 2: SAP-017/018 chora-compose Integration (20-28h)

### Phase 1: SAP-017 chora-compose-integration (8-12h)

**Task 1.1: Read coordination context**
- Review `inbox/active/coord-001-chora-compose-sap/coord-001-chora-compose-sap-CONTEXT.md`
- Review chora-compose docs in `docs/reference/ecosystem/chora-compose/user-docs/`

**Task 1.2: Create SAP-017 structure**
```
docs/skilled-awareness/chora-compose-integration/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md
├── adoption-blueprint.md
└── ledger.md
```

**Task 1.3: Write capability-charter.md**
- What: chora-compose adoption guide
- Why: Enable config-driven content generation
- Who: App developers, MCP server developers, platform engineers
- Dependencies: Python, chora-compose package

**Task 1.4: Write protocol-spec.md**
- Installation methods (pip, MCP, CLI)
- Role-based usage patterns
- Integration with chora-base workflows
- Current capabilities (v1.2.0) vs future roadmap

**Task 1.5: Write awareness-guide.md**
- "When to Use" - Decision guide for chora-compose
- "Common Pitfalls" - 5 scenarios
- "Related Content" - 4-domain coverage
- Wave 2 enhancement pattern

**Task 1.6: Write adoption-blueprint.md**
- How to install chora-compose
- How to configure for different roles
- Example workflows

**Task 1.7: Write ledger.md**
- Version 1.0.0

### Phase 2: SAP-018 chora-compose-meta (12-16h)

**Task 2.1: Study SAP-002 pattern**
- Review `docs/skilled-awareness/chora-base/` structure
- SAP-018 mirrors SAP-002 (meta-SAP pattern)

**Task 2.2: Create SAP-018 structure**
```
docs/skilled-awareness/chora-compose-meta/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md
├── adoption-blueprint.md
└── ledger.md
```

**Task 2.3: Write capability-charter.md**
- Complete chora-compose overview
- Position in AI tooling ecosystem
- Strategic value

**Task 2.4: Write protocol-spec.md**
- Complete architecture (config-driven, MCP-native, observable)
- All 17 MCP tools + 5 resource URI families
- 4 access modalities (pip, SAP, MCP, API)
- Technical contracts and guarantees

**Task 2.5: Write awareness-guide.md**
- Comprehensive usage guide
- All 17 tools documented
- Agent workflows
- Wave 2 enhancements applied

**Task 2.6: Write adoption-blueprint.md**
- Full installation guide
- Configuration examples
- Integration patterns

**Task 2.7: Write ledger.md**
- Version 1.0.0

### Phase 3: Integration & Validation (2-3h)

**Task 3.1: Update INDEX.md**
- Add SAP-017 and SAP-018 entries
- Document as "ecosystem integration SAPs"

**Task 3.2: Optional: Update SAP-001 (Inbox)**
- Add chora-compose coordination example
- Demonstrate inbox protocol in action

**Task 3.3: Run link validation**
- Validate SAP-017 links
- Validate SAP-018 links
- Ensure references to chora-compose docs are correct

**Task 3.4: Move to completed**
- Move `inbox/active/coord-001-chora-compose-sap/` → `inbox/completed/`
- Emit completion event to `inbox/coordination/events.jsonl`

---

## Integration & Release (5-8h)

### Task 1: Create Wave 3 Summary Documentation

**Files to create**:
- `docs/project-docs/wave-3-complete-summary.md`
- `docs/project-docs/wave-3-sap-014-audit.md`
- `docs/project-docs/wave-3-sap-017-audit.md`
- `docs/project-docs/wave-3-sap-018-audit.md`

### Task 2: Update CHANGELOG

**v3.6.0 entry**:
- SAP-014: MCP Server Development
- SAP-017/018: chora-compose integration
- blueprints/ and setup.py removed
- Root docs generalized
- Clone & customize workflow established

### Task 3: Run Full Link Validation

- Validate all SAPs (including new SAP-014, 017, 018)
- Fix any broken links
- Create final validation report

### Task 4: Commit & Tag

- Commit all Wave 3 changes
- Create git tag: `v3.6.0`
- Push to remote

### Task 5: GitHub Release

- Create v3.6.0 release
- Link to wave-3-complete-summary.md
- Highlight key achievements

---

## Success Criteria

**SAP-014 (MCP Server Development)**:
- ✅ All 5 artifacts created
- ✅ All MCP content from blueprints/ preserved in SAP-014
- ✅ 4-domain supporting docs created
- ✅ Root docs generalized (no MCP assumptions)
- ✅ blueprints/ and setup.py deleted
- ✅ Clone & customize workflow documented
- ✅ Projects can be created with/without MCP

**SAP-017 (chora-compose-integration)**:
- ✅ All 5 artifacts created
- ✅ References actual chora-compose documentation
- ✅ Decision guide for when to use chora-compose
- ✅ Wave 2 enhancements applied

**SAP-018 (chora-compose-meta)**:
- ✅ All 5 artifacts created
- ✅ Documents all 17 MCP tools + 5 resource families
- ✅ 4 access modalities documented
- ✅ Mirrors SAP-002 pattern

**Overall**:
- ✅ INDEX.md updated with SAP-014, 017, 018
- ✅ Link validation passes
- ✅ Inbox coordination completed (coord-001)
- ✅ v3.6.0 released and tagged

---

## Risk Mitigation

**Risk 1**: Losing MCP expertise during extraction
- **Mitigation**: Preserve ALL blueprints/ content in SAP-014, enhance with additional patterns

**Risk 2**: Breaking existing MCP server projects
- **Mitigation**: Git tag v3.5.1-with-blueprints before deletion, clear migration guide

**Risk 3**: chora-compose docs may be incomplete
- **Mitigation**: Reference actual docs, mark future features as "roadmap"

**Risk 4**: Time estimation too optimistic
- **Mitigation**: Execute in phases, track progress, adjust as needed

---

## Execution Order

**Recommended sequence**:
1. Start Track 1, Phase 1 (MCP audit) - 8-10h
2. **Parallel**: Start Track 2, Phase 1 (SAP-017) - 8-12h
3. Continue Track 1, Phases 2-3 (SAP-014 creation) - 25-35h
4. **Parallel**: Start Track 2, Phase 2 (SAP-018) - 12-16h
5. Complete Track 1, Phases 4-6 (generalize, delete, validate) - 15-23h
6. Complete Track 2, Phase 3 (integrate, validate) - 2-3h
7. Integration & Release - 5-8h

**Why this order?**:
- MCP audit first (informs SAP-014 creation)
- SAP-017 early (simpler, builds momentum)
- Parallelization where possible (SAP-017 + SAP-014 creation, SAP-018 + Track 1 Phases 4-5)
- Generalization and deletion last (ensures everything preserved in SAP-014 first)

---

## Timeline

**Week 1** (30-35h):
- Track 1: Phases 1-2 (audit + SAP-014 structure)
- Track 2: Phase 1 (SAP-017)

**Week 2** (30-35h):
- Track 1: Phase 3 (4-domain content)
- Track 2: Phase 2 (SAP-018)

**Week 3** (20-25h):
- Track 1: Phases 4-6 (generalize, delete, validate)
- Track 2: Phase 3 (integrate, validate)

**Week 4** (5-13h):
- Integration & Release
- Buffer for adjustments

**Total**: 85-108 hours over 3-4 weeks

---

**Document Version**: 1.0
**Status**: Planning
**Created**: 2025-10-29
**Ready for Execution**: Pending approval
