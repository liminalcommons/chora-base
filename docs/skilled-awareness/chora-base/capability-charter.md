# Capability Charter: chora-base Template Repository

**SAP ID**: SAP-002
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-27
**Last Updated**: 2025-10-27

---

## 1. Problem Statement

### Current Challenge

chora-base is a **Python project template for AI-agent-first development**, providing production-ready scaffolding, documentation, and quality gates. However, chora-base itself lacks a **unified, structured definition** of:

1. **What chora-base is** - Comprehensive capability inventory
2. **How chora-base works** - Technical architecture, interfaces, guarantees
3. **How to use chora-base** - Agent execution patterns, workflows
4. **How to adopt chora-base** - Installation, upgrade, customization
5. **Who uses chora-base** - Adopter tracking, version status

**Result**:
- **New adopters**: Uncertain where to start, what capabilities exist, what's optional vs required
- **AI agents**: Fragmented guidance across multiple files (README, AGENTS.md, setup guides, docs)
- **Maintainers**: No single source of truth for chora-base's own structure and evolution
- **Ecosystem**: Unclear relationship between chora-base and related repos (meta, governance, ecosystem-manifest)

### Evidence

**From adopter feedback**:
- "I don't know which features are core vs optional"
- "Setup documentation is spread across 3+ files"
- "Not clear what version I should use or how to upgrade"

**From agent behavior**:
- Agents read README, AGENTS.md, setup guides, and docs separately
- Redundant context loading (same information in multiple files)
- Missed capabilities (didn't know they existed)

**From maintenance burden**:
- Updates require changing 4+ files (README, AGENTS.md, CHANGELOG, docs)
- Inconsistencies between files
- No structured governance for capability evolution

### Business Impact

Without structured self-definition:
- **Adoption friction**: 2-4 hours to understand chora-base fully (should be <1 hour)
- **Agent inefficiency**: 10-20k tokens of redundant context (should be 5-10k)
- **Maintenance overhead**: 30-60 minutes per capability update (should be 15-30 minutes)
- **Ecosystem confusion**: Unclear how chora-base relates to meta/governance

---

## 2. Proposed Solution

### chora-base Meta-SAP

A **comprehensive SAP describing chora-base itself** using the SAP framework (dogfooding). This meta-SAP serves as:

1. **Single Source of Truth**: Definitive description of chora-base
2. **Agent Entry Point**: Primary document for AI agents working with chora-base
3. **Adopter Guide**: Complete onboarding resource
4. **Framework Validation**: Proves SAP framework works by applying it to itself

### Key Principles

1. **Meta-Reflexive**: chora-base uses its own SAP framework to describe itself
2. **Comprehensive**: Covers all 14 capabilities (current + planned)
3. **Multi-Scope**: Addresses Vision & Strategy, Planning, Implementation
4. **Agent-First**: Optimized for AI agent consumption
5. **Maintainable**: Updates flow through structured SAP governance

---

## 3. Scope

### In Scope

**chora-base Meta-SAP Artifacts**:
- ✅ Capability Charter (this document) - Problem, scope, outcomes
- ✅ Protocol Specification - Technical architecture, all 14 capabilities, interfaces
- ✅ Awareness Guide - Agent workflows for template generation, upgrade, maintenance
- ✅ Adoption Blueprint - How to adopt chora-base (generate projects, upgrade)
- ✅ Traceability Ledger - Adopter projects, versions, status

**Capabilities Covered** (14 total):
1. sap-framework (SAP-000)
2. inbox-coordination (SAP-001)
3. chora-base-meta (SAP-002, this SAP)
4. project-bootstrap
5. testing-framework
6. ci-cd-workflows
7. quality-gates
8. documentation-framework
9. automation-scripts
10. agent-awareness
11. memory-system (A-MEM)
12. docker-operations
13. development-lifecycle
14. metrics-tracking

**Scope Levels Covered**:
- **Vision & Strategy**: Roadmap, quarterly capability evolution, ecosystem coordination
- **Planning & Prioritization**: Sprint planning, release planning, feature prioritization
- **Implementation**: Daily development, feature implementation, bug fixes

### Out of Scope (for v1.0)

- ❌ Detailed implementation of all 14 SAPs (only overview in this meta-SAP)
- ❌ Executable blueprints for each capability (covered by individual SAPs)
- ❌ Cross-repository governance (covered by ecosystem coordination)
- ❌ Historical migrations (focus on current v3.3.0 forward)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 1):
- ✅ chora-base-meta SAP complete (all 5 artifacts)
- ✅ New adopters reference meta-SAP first (measured by feedback)
- ✅ Agents load meta-SAP as primary context (measured by token efficiency)

**Quality Success** (Phase 2-3):
- ✅ All 14 capabilities documented in Protocol Spec
- ✅ Single source of truth (no contradictions with README/AGENTS.md)
- ✅ Adopter onboarding time reduced (4h → 1h)

**Maintenance Success** (Phase 2-4):
- ✅ Capability updates follow SAP governance (versioning, RFCs)
- ✅ Update time reduced (60min → 30min per capability)
- ✅ Consistency maintained (automated checks)

### Key Metrics

| Metric | Baseline | Target (Phase 1) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Onboarding Time | 2-4h | 1-2h | <1h |
| Agent Context (initial) | 15-25k tokens | 10-15k tokens | 5-10k tokens |
| Update Time | 60min | 45min | 30min |
| Documentation Consistency | ~80% | 95% | 99% |
| Adopter Comprehension | ~70% | 90% | 95% |

**Measurement**:
- **Onboarding Time**: Survey new adopters
- **Agent Context**: Measure token usage in setup sessions
- **Update Time**: Track maintainer time per capability update
- **Consistency**: Automated doc validation (future)
- **Comprehension**: Quiz after onboarding (future)

---

## 5. Stakeholders

### Primary Stakeholders

**Template Maintainer**:
- Victor (chora-base owner)
- Maintains meta-SAP
- Updates as capabilities evolve

**AI Agents** (Execute/Install):
- Claude Code (primary agent)
- Cursor Composer
- Other LLM-based agents
- Use meta-SAP for project generation, maintenance

**Adopter Maintainers** (Use chora-base):
- chora-compose maintainer
- mcp-n8n maintainer
- Example project maintainers
- External adopters
- Reference meta-SAP for understanding, upgrades

### Secondary Stakeholders

**Capability Owners**:
- Maintain individual SAPs (SAP-003 through SAP-013)
- Reference meta-SAP for chora-base context

**Ecosystem Projects**:
- chora-meta (meta-repository)
- chora-governance (governance repository)
- ecosystem-manifest (capability registry)
- Reference meta-SAP for chora-base integration

**Documentation Consumers**:
- New users evaluating chora-base
- Contributors learning chora-base internals
- Researchers studying agentic coding patterns

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure, templates
- ✅ Root protocol (SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- ✅ SAP Index (INDEX.md)

**Capability Dependencies**:
- SAP-001 (inbox-coordination) - Referenced as example
- All other SAPs (SAP-003 through SAP-013) - Documented in Protocol Spec

**Documentation Dependencies**:
- README.md - High-level overview (should align with meta-SAP)
- AGENTS.md - Agent guidance (should reference meta-SAP)
- CHANGELOG.md - Version history (tracked in Ledger)

### External Dependencies

**Tooling**:
- Git (version tracking)
- Python 3.11+ (template target)
- GitHub (repository hosting, coordination)

**Standards**:
- Semantic versioning (template releases)
- Diataxis (documentation structure)
- DDD → BDD → TDD (development workflow)

**Ecosystem**:
- chora-meta (meta-repository patterns)
- chora-governance (governance patterns)
- MCP protocol (for MCP-based projects)

---

## 7. Constraints & Assumptions

### Constraints

1. **Backward Compatibility**: Meta-SAP must align with v3.3.0 (current version)
2. **Maintenance Burden**: Must be maintainable by single owner (Victor)
3. **Agent Compatibility**: Must work with Claude Code, Cursor, other agents
4. **Token Budget**: Protocol Spec must be <15k tokens for agent efficiency

### Assumptions

1. **SAP Framework Stable**: SAP-000 (framework) won't change significantly during Phase 1
2. **Adopter Commitment**: Adopters willing to reference meta-SAP
3. **Agent Capabilities**: Agents can parse YAML, markdown, execute blueprints
4. **Single Template**: chora-base remains single template (not split into multiple templates)

---

## 8. Risks & Mitigation

### Risk 1: Meta-SAP Divergence

**Risk**: Meta-SAP description diverges from actual chora-base implementation

**Likelihood**: Medium
**Impact**: High (defeats purpose of single source of truth)

**Mitigation**:
- Automated consistency checks (Phase 2)
- Update meta-SAP with every chora-base release
- Include meta-SAP review in release checklist
- Agents validate against actual structure

### Risk 2: Overwhelming Complexity

**Risk**: Meta-SAP becomes too large/complex (>30k tokens)

**Likelihood**: Medium
**Impact**: Medium (reduces agent efficiency)

**Mitigation**:
- Keep Protocol Spec focused (high-level overview + pointers)
- Detailed implementation in individual SAPs (SAP-003 through SAP-013)
- Use progressive loading patterns (Essential → Extended → Full)
- Link to detailed docs instead of duplicating

### Risk 3: Maintenance Overhead

**Risk**: Updating meta-SAP for every capability change becomes burdensome

**Likelihood**: Low
**Impact**: Medium (delays, inconsistencies)

**Mitigation**:
- Streamlined update process (templates, checklists)
- Batch minor updates (weekly/bi-weekly)
- Automate where possible (Phase 4)
- Clear ownership and responsibility

### Risk 4: Adoption Resistance

**Risk**: Adopters ignore meta-SAP, continue using old docs

**Likelihood**: Low
**Impact**: Medium (wasted effort)

**Mitigation**:
- Promote meta-SAP in README, AGENTS.md
- Add value (better than existing docs)
- Collect feedback, iterate quickly
- Show ROI (time savings, clarity)

---

## 9. Lifecycle

### Phase 1: Meta-SAP Creation (2025-10 → 2025-11)

**Goal**: Create complete chora-base meta-SAP

**Deliverables**:
- ✅ Capability Charter (this document)
- 🔄 Protocol Specification (all 14 capabilities overview)
- 🔄 Awareness Guide (agent workflows)
- 🔄 Adoption Blueprint (project generation, upgrade)
- 🔄 Traceability Ledger (adopter tracking)

**Success**: Meta-SAP complete, Phase 1 complete (3/3 SAPs)

### Phase 2: Core Capability SAPs (2025-11 → 2026-01)

**Goal**: Create SAPs for 4 core capabilities

**Deliverables**:
- SAP-003 (project-bootstrap)
- SAP-004 (testing-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)
- Update meta-SAP Protocol with links to new SAPs

**Success**: 7/14 SAPs complete (50% coverage)

### Phase 3: Extended Capability SAPs (2026-01 → 2026-03)

**Goal**: Create SAPs for 6 extended capabilities

**Deliverables**:
- SAP-007 through SAP-012
- Update meta-SAP Protocol with links
- Consistency validation

**Success**: 13/14 SAPs complete (93% coverage)

### Phase 4: Optimization & Automation (2026-03 → 2026-05)

**Goal**: Automate maintenance, optimize workflows

**Deliverables**:
- SAP-013 (metrics-tracking)
- Automated consistency checks
- Meta-SAP dashboard
- ROI validation

**Success**: 14/14 SAPs complete (100% coverage), meta-SAP validation automated

---

## 10. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](../sap-framework/) - SAP-000 (framework SAP)
- [INDEX.md](../INDEX.md) - SAP registry (all 14 capabilities)
- [document-templates.md](../document-templates.md) - SAP templates

**chora-base Core Docs**:
- [README.md](/README.md) - Project overview
- [AGENTS.md](/AGENTS.md) - Agent guidance
- [CHANGELOG.md](/CHANGELOG.md) - Version history
- [CLAUDE_SETUP_GUIDE.md](/CLAUDE_SETUP_GUIDE.md) - Claude-specific setup

**Capability Documentation**:
- [inbox/](../inbox/) - SAP-001 (pilot implementation)
- [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md) - Phased adoption plan

**Development Process**:
- [static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD → BDD → TDD
- [docs/user-docs/explanation/benefits-of-chora-base.md](/docs/user-docs/explanation/benefits-of-chora-base.md) - ROI analysis and benefits

---

## 11. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-27
**Review Cycle**: Monthly (align with release cycles)

**Next Review**: 2025-11-30 (end of Phase 1)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial charter for chora-base meta-SAP
