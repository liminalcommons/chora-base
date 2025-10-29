# Traceability Ledger: chora-base Template Repository

**SAP ID**: SAP-002
**Current Version**: 1.0.0 (SAP), 3.3.0 (chora-base)
**Status**: Draft (Phase 1)
**Last Updated**: 2025-10-27

---

## 1. Adopter Registry

| Adopter | chora-base Version | Status | Generated Date | Last Upgrade | Notes |
|---------|-------------------|--------|----------------|--------------|-------|
| chora-compose | 1.9.x | Active | 2024 | - | MCP composition server |
| mcp-n8n | 1.8.x | Active | 2024 | - | MCP gateway for n8n |
| examples/full-featured-with-vision | 3.3.0 | Active | 2025-10-25 | - | Example project (in chora-base repo) |
| examples/full-featured-with-docs | 3.3.0 | Active | 2025-10-25 | - | Example project (in chora-base repo) |
| _External adopters unknown_ | - | - | - | - | Not tracked yet |

**Legend**:
- **Status**: Active (in use), Inactive (deprecated), Migrated (to different template)
- **Generated Date**: When project was first generated from chora-base
- **Last Upgrade**: Most recent chora-base version upgrade

**Note**: External adopter tracking not yet implemented. Future: adopters self-report via PR.

---

## 2. Version History

| chora-base Version | Release Date | Type | Key Changes | SAP Updates |
|-------------------|--------------|------|-------------|-------------|
| 3.3.0 | 2025-10-25 | MINOR | Claude-Specific Development Framework: CLAUDE.md, pattern library, ROI calculator | SAP-002 v1.0.0 created |
| 3.2.0 | 2025-10-26 | MINOR | Agentic Development Framework: 8-phase lifecycle, DDD/BDD/TDD, sprint planning | - |
| 3.0.0 | 2025-10-25 | MAJOR | AI-Agent-First Architecture: Removed Copier, blueprint-based generation, AGENTS.md | BREAKING |
| 2.x | 2024 | - | Copier-based template | Deprecated |
| 1.x | 2023 | - | Initial template | Deprecated |

**Note**: SAP-002 (chora-base-meta) created at v3.3.0. Prior versions not covered by SAP.

---

## 3. Active Deployments

### Known Adopters (Production)

**chora-compose** (v1.9.x):
- **Purpose**: MCP composition server
- **Deployed**: Production
- **Contact**: chora-compose maintainer
- **Health**: ✅ Healthy
- **Notes**: Generated before v3.0.0 (Copier-based), needs upgrade

**mcp-n8n** (v1.8.x):
- **Purpose**: MCP gateway for n8n
- **Deployed**: Production
- **Contact**: mcp-n8n maintainer
- **Health**: ✅ Healthy
- **Notes**: Generated before v3.0.0 (Copier-based), needs upgrade

### Example Projects (Reference)

**examples/full-featured-with-vision** (v3.3.0):
- **Purpose**: Example with vision docs
- **Deployed**: chora-base repository
- **Health**: ✅ Healthy

**examples/full-featured-with-docs** (v3.3.0):
- **Purpose**: Example with Diataxis docs
- **Deployed**: chora-base repository
- **Health**: ✅ Healthy

---

## 4. Capability Coverage

### Phase 1 (Current): Framework Hardening

| SAP ID | Capability | Status | Completion |
|--------|------------|--------|------------|
| SAP-000 | sap-framework | Draft | ✅ 100% |
| SAP-001 | inbox-coordination | Pilot | ✅ 100% |
| SAP-002 | chora-base-meta | Draft | ✅ 100% |

**Phase 1 Target**: 3/14 SAPs (21% coverage)
**Phase 1 Actual**: 3/14 SAPs (21% coverage) ✅ ON TRACK

### Phase 2 (2025-11 → 2026-01): Core Capabilities

| SAP ID | Capability | Priority | Target Completion |
|--------|------------|----------|-------------------|
| SAP-003 | project-bootstrap | P0 | 2025-12 |
| SAP-004 | testing-framework | P0 | 2025-12 |
| SAP-005 | ci-cd-workflows | P0 | 2026-01 |
| SAP-006 | quality-gates | P0 | 2026-01 |

**Phase 2 Target**: 7/14 SAPs (50% coverage)

### Phase 3 (2026-01 → 2026-03): Extended Capabilities

| SAP ID | Capability | Priority | Target Completion |
|--------|------------|----------|-------------------|
| SAP-007 | documentation-framework | P1 | 2026-01 |
| SAP-008 | automation-scripts | P1 | 2026-02 |
| SAP-009 | agent-awareness | P1 | 2026-02 |
| SAP-010 | memory-system (A-MEM) | P1 | 2026-02 |
| SAP-011 | docker-operations | P1 | 2026-03 |
| SAP-012 | development-lifecycle | P1 | 2026-03 |

**Phase 3 Target**: 13/14 SAPs (93% coverage)

### Phase 4 (2026-03 → 2026-05): Optimization

| SAP ID | Capability | Priority | Target Completion |
|--------|------------|----------|-------------------|
| SAP-013 | metrics-tracking | P2 | 2026-05 |

**Phase 4 Target**: 14/14 SAPs (100% coverage)

---

## 5. Adoption Metrics

### chora-base Usage (Estimated)

| Metric | Baseline | Phase 1 | Phase 2 Target | Phase 4 Target |
|--------|----------|---------|----------------|----------------|
| Known Adopters | 2 | 2 | 5-10 | 20+ |
| Generation Time | N/A | 20-40s | <30s | <20s |
| Onboarding Time | 4h | 2-4h | 1-2h | <1h |
| SAP Coverage | 0% | 21% | 50% | 100% |

**Measurement**:
- **Known Adopters**: Self-reported (via ledger PRs)
- **Generation Time**: Measured during setup
- **Onboarding Time**: Surveyed from new adopters
- **SAP Coverage**: Tracked in INDEX.md

---

## 6. Known Issues

### Active Issues

**Issue #1**: External adopter tracking not implemented
- **Impact**: Can't track adoption outside chora-base org
- **Workaround**: Manual tracking in this ledger
- **Resolution**: Phase 4 (automated registry)

**Issue #2**: v2.x → v3.x upgrade path manual
- **Impact**: Adopters must manually upgrade (no automation)
- **Workaround**: Upgrade guides in `docs/upgrades/`
- **Resolution**: Phase 4 (automated upgrade tooling)

### Resolved Issues

_None yet_ - SAP is new

---

## 7. Deprecation Notices

### v2.x (Copier-Based) - DEPRECATED

**Deprecation Date**: 2025-10-25 (v3.0.0 release)
**End of Support**: 2026-01-01
**Migration**: See [docs/upgrades/v2-to-v3-migration.md](../../../../docs/upgrades/v2-to-v3-migration.md)

**Reason**: v3.0.0 introduces breaking change (no Copier dependency, blueprint-based generation)

**Affected Adopters**:
- chora-compose (v1.9.x)
- mcp-n8n (v1.8.x)

**Migration Path**:
1. Generate new project with v3.3.0
2. Copy custom code from old project
3. Update imports, configs as needed
4. Test thoroughly
5. Update ledger

---

## 8. Roadmap Integration

### Current Phase: Phase 1 - Framework Hardening (2025-10 → 2025-11)

**Status**: ✅ Complete
**Deliverables**:
- ✅ SAP-000 (sap-framework)
- ✅ SAP-001 (inbox-coordination)
- ✅ SAP-002 (chora-base-meta)
- ✅ SAP Index
- ✅ Root protocol

**Success Criteria**:
- ✅ 3 SAPs complete
- ✅ Framework proven (dogfooding)
- ✅ Pilot feedback collected (inbox SAP)

### Next Phase: Phase 2 - Core Capability Migration (2025-11 → 2026-01)

**Planned Deliverables**:
- SAP-003 (project-bootstrap)
- SAP-004 (testing-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)

**Success Criteria**:
- 7 SAPs total (50% coverage)
- Core capabilities documented
- Adopter feedback positive

---

## 9. Feedback Summary

### Phase 1 Feedback (2025-10 → 2025-11)

**Collected From**: _TBD_ (chora-base-meta just created)

**Key Themes**: _TBD_

**Action Items**: _TBD_

---

## 10. Compliance & Audit

### SAP Quality Gates (Phase 1)

**chora-base-meta SAP**:
- ✅ All 5 artifacts present
- ✅ All required sections complete
- ✅ YAML frontmatter valid
- ✅ Comprehensive (all 14 capabilities documented)
- ✅ Aligned with v3.3.0

**Audit Trail**:

| Date | Auditor | Finding | Resolution |
|------|---------|---------|------------|
| 2025-10-27 | Claude Code | Created SAP-002 | Initial creation complete |
| _Future audits_ | - | - | - |

---

## 11. Migration History

### v2.x → v3.x (BREAKING)

**Migration Date**: 2025-10-25 (v3.0.0 release)

**Breaking Changes**:
- Removed Copier dependency
- Blueprint-based generation (not Copier-based)
- New AGENTS.md structure
- SAP framework introduced

**Affected Adopters**: All v2.x adopters (chora-compose, mcp-n8n)

**Migration Path**: [docs/upgrades/v2-to-v3-migration.md](../../../../docs/upgrades/v2-to-v3-migration.md)

---

## 12. How to Update This Ledger

### Adding New Adopter

**When**: Project generated from chora-base

**Steps**:
1. Add row to "Adopter Registry" table
2. Include: Project name, chora-base version, date
3. Create PR to chora-base (if external project)
4. Commit: `docs(SAP-002): Add <project> to adopter registry`

### Recording Upgrade

**When**: Adopter upgrades chora-base version

**Steps**:
1. Update "Adopter Registry" table:
   - Change version
   - Update "Last Upgrade" date
2. Create PR if external
3. Commit: `docs(SAP-002): <project> upgraded to v<version>`

### Adding SAP

**When**: New SAP created

**Steps**:
1. Update "Capability Coverage" tables
2. Update Protocol Spec (link to new SAP)
3. Update INDEX.md
4. Commit: `docs(SAP-002): Add SAP-<NNN> to coverage tracking`

---

## 13. Related Documents

**chora-base-meta SAP**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - All 14 capabilities
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt chora-base

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [INDEX.md](../INDEX.md) - All SAPs
- [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md) - Phased plan

**chora-base Core**:
- [README.md](../../../../README.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [docs/upgrades/](../../../../docs/upgrades/) - Upgrade guides

---

**Version History**:
- **1.0.0** (2025-10-27): Initial ledger for chora-base meta-SAP
