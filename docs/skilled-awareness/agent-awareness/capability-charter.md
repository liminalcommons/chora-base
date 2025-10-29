# Capability Charter: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

chora-base provides **AGENTS.md + CLAUDE.md patterns with nested awareness** files, but lacks:

1. **Explicit Awareness Contracts** - No documented structure for AGENTS.md/CLAUDE.md content
2. **Nesting Rationale** - Why nested awareness files (tests/AGENTS.md, scripts/AGENTS.md) not explained
3. **Context Optimization** - Progressive loading, token budgets not standardized
4. **Claude-Specific Patterns** - What makes CLAUDE.md different from AGENTS.md unclear

**Result**: Inconsistent awareness files, agents lack domain-specific guidance, context loading inefficient

---

## 2. Proposed Solution

A **comprehensive SAP describing AGENTS.md/CLAUDE.md structure, nesting patterns, and context optimization**.

**Key Principles**:
1. **Dual-File Pattern** - AGENTS.md (generic) + CLAUDE.md (Claude-specific)
2. **Nested Awareness** - Domain-specific files in subdirectories (tests/, scripts/, docker/)
3. **Nearest File Wins** - Agents read awareness file nearest to working code
4. **Progressive Loading** - Essential → Extended → Full context phases
5. **Context Budgets** - Token budgets by task type

---

## 3. Scope

**In Scope**: AGENTS.md.blueprint (~900 lines), CLAUDE.md.blueprint (~450 lines), nested patterns (tests/AGENTS.md, scripts/AGENTS.md, docker/AGENTS.md, .chora/memory/AGENTS.md), context management

**Out of Scope**: Agent-specific integrations (non-Claude agents)

---

## 4. Outcomes

**Success Criteria** (Phase 3):
- ✅ SAP-009 complete (all 5 artifacts)
- ✅ AGENTS.md and CLAUDE.md structures documented
- ✅ Nesting pattern explained
- ✅ Context optimization patterns catalogued

---

## 5. Stakeholders

**Template Maintainer**: Victor
**AI Agents**: Use SAP-009 to read awareness files, optimize context
**Project Developers**: Write AGENTS.md/CLAUDE.md for projects

---

## 6. Dependencies

- ✅ SAP-000 (sap-framework)
- SAP-007 (documentation-framework) - Awareness files are documentation

---

## 7. Lifecycle

**Phase 3**: Create SAP-009 (all 5 artifacts)
**Phase 4**: Enhance with automated validation

---

## 8. Related Documents

- [blueprints/AGENTS.md.blueprint](../../../../blueprints/AGENTS.md.blueprint)
- [blueprints/CLAUDE.md.blueprint](../../../../blueprints/CLAUDE.md.blueprint)
- [static-template/tests/AGENTS.md](../../../../static-template/tests/AGENTS.md)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for agent-awareness SAP
