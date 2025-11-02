# Traceability Ledger: Agent Awareness

**SAP ID**: SAP-009
**Current Version**: 1.1.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-31

---

## 1. Projects Using Agent Awareness

| Project | Root AGENTS.md | Root CLAUDE.md | Nested Files | Last Updated |
|---------|----------------|----------------|--------------|--------------|
| chora-base | ✅ Yes | ✅ Yes | 4 (tests, scripts, docker, memory) | 2025-10-28 |
| chora-compose | ✅ Yes | ❌ No | 0 | 2025-10-20 |
| mcp-n8n | ✅ Yes | ❌ No | 0 | 2025-10-22 |

---

## 2. Version History

| Version | Release Date | Type | Changes |
|---------|--------------|------|---------|
| 1.1.0 | 2025-10-31 | MINOR | Bidirectional translation layer: intent routing, glossary search, context-aware suggestions, 5 domain AGENTS.md files (COORD-2025-004) |
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-009 release: AGENTS.md/CLAUDE.md patterns, nested awareness |

---

## 3. Awareness File Coverage

### By Project

| Project | Total Awareness Files | Coverage |
|---------|----------------------|----------|
| chora-base | 20 (root + 9 domains × 2) | ✅ Complete |
| chora-compose | 2 (root only) | ⚠️ Partial |
| mcp-n8n | 2 (root only) | ⚠️ Partial |

### By Domain (chora-base)

| Domain | AGENTS.md | CLAUDE.md | Lines (AGENTS) |
|--------|-----------|-----------|----------------|
| Root | ✅ | ✅ | ~900 |
| tests/ | ✅ | ✅ | ~250 |
| scripts/ | ✅ | ✅ | ~200 |
| docker/ | ✅ | ✅ | ~200 |
| .chora/memory/ | ✅ | ✅ | ~300 |
| **SAP domains (v1.1.0)**: | | | |
| inbox/ (SAP-001) | ✅ | ❌ | ~150 |
| testing-framework/ (SAP-004) | ✅ | ❌ | ~180 |
| agent-awareness/ (SAP-009) | ✅ | ❌ | ~240 |
| development-lifecycle/ (SAP-012) | ✅ | ❌ | ~290 |
| metrics-framework/ (SAP-013) | ✅ | ❌ | ~240 |

---

## 4. Context Optimization Metrics

**Token Usage** (chora-base, Claude sessions):
- Average per session: 35k tokens
- Peak sessions: 120k tokens (complex refactoring)
- Checkpoint frequency: Every 7 interactions (avg)

**Progressive Loading Adoption**:
- Phase 1 only: 60% of sessions
- Phase 2: 30% of sessions
- Phase 3: 10% of sessions (complex only)

---

## 5. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint)
- [CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint)

---

**Version History**:
- **1.1.0** (2025-10-31): Released bidirectional translation layer, updated version tracking, added 5 SAP domain AGENTS.md files
- **1.0.0** (2025-10-28): Initial ledger
