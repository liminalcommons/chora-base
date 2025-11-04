# Capability Charter: SAP Framework

**SAP ID**: SAP-000 (meta-capability)
**Version**: 1.0.0
**Status**: Draft → Active (Phase 1)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-27
**Last Updated**: 2025-10-27

---

## 1. Problem Statement

### Current Challenge

chora-base provides powerful capabilities (project bootstrap, testing, Docker, documentation, memory system, etc.) but lacks a **consistent, structured approach** for:

1. **Documenting** what each capability does and how it works
2. **Installing** capabilities with clear, reproducible steps
3. **Upgrading** capabilities across versions without breakage
4. **Tracking** which adopters use which versions
5. **Coordinating** cross-repository capability evolution

**Result**: Adopters face:
- Unclear contracts and guarantees ("What does this capability promise?")
- Fragmented guidance (documentation scattered across files)
- Difficult upgrades (no clear path from v1.0 to v2.0)
- Hidden dependencies (capability A requires capability B, but not documented)
- No visibility into adoption status

### Evidence

From [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md):

> "Adopters unclear on required coverage, when to enforce metrics, or how to extend"
>
> "No documented lifecycle for enabling/disabling Docker options; inconsistent adoption"
>
> "Standards for safety/idempotency assumed rather than contractually defined"

**Pain Point**: "Hard to reason about guarantees, versioning, and upgrade paths; no single source for expectations"

### Business Impact

Without structured capability packaging:
- **Adoption friction**: 4-8 hours per capability to understand and install
- **Upgrade risk**: Breaking changes discovered during upgrade, not before
- **Maintenance burden**: Capability owners field repetitive questions
- **Quality issues**: Adopters misuse capabilities due to unclear contracts

---

## 2. Proposed Solution

### Skilled Awareness Package (SAP) Framework

A **standardized capability packaging system** that provides:

1. **5 Core Artifacts** for every capability:
   - Capability Charter (problem, scope, outcomes)
   - Protocol Specification (technical contract)
   - Awareness Guide (agent execution patterns)
   - Adoption Blueprint (installation steps)
   - Traceability Ledger (adopter tracking)

2. **Infrastructure** (schemas, templates, configs, directories)

3. **Testing Layer** (optional validation)

4. **Governance** (versioning, change management, coordination)

### Key Principles

1. **Machine-Readable**: AI agents can parse and execute SAP artifacts
2. **Human-Friendly**: Clear structure, consistent format, easy to navigate
3. **Contract-First**: Protocol defines guarantees before implementation
4. **Blueprint-Based**: Agent-executable installation (not shell scripts)
5. **Version-Aware**: Sequential upgrades, clear migration paths
6. **Cross-Repository**: SAPs work across chora-base ecosystem

### Design Trade-offs and Rationale

**Why 5 artifacts instead of 1-2 comprehensive documents?**
- **Trade-off**: More files to maintain vs. clear separation of concerns
- **Decision**: Separate artifacts ensure each serves a distinct Diataxis category (explanation, reference, tutorial, how-to), making documentation easier to navigate and maintain
- **Alternative considered**: Single "capability.md" with all content → rejected due to mixing concerns and poor navigability

**Why blueprint-based installation instead of shell scripts?**
- **Trade-off**: Agent-parseable instructions vs. immediate executability
- **Decision**: Blueprints provide structured, validated steps that agents can reason about, rather than opaque bash scripts
- **Alternative considered**: Traditional install.sh scripts → rejected due to lack of visibility into what's happening and difficulty troubleshooting failures

**Why mandatory ledger tracking?**
- **Trade-off**: Privacy concerns vs. adoption visibility
- **Decision**: Ledger provides critical feedback loop for capability evolution and helps maintainers understand usage patterns
- **Alternative considered**: Optional tracking → rejected because it would lead to blind spots in capability adoption

**Why contract-first protocol specification?**
- **Trade-off**: Upfront design effort vs. implementation-driven evolution
- **Decision**: Defining contracts before implementation prevents breaking changes and ensures adopters can rely on stable APIs
- **Alternative considered**: Document-as-you-go approach → rejected due to resulting inconsistencies and unclear guarantees

---

## 3. Scope

### In Scope

**SAP Framework Capabilities**:
- ✅ Artifact templates (5 core documents)
- ✅ Blueprint-based installation pattern
- ✅ Versioning and upgrade protocol
- ✅ Ledger and adoption tracking
- ✅ Governance (RFC/ADR integration)
- ✅ SAP lifecycle (Draft → Pilot → Active → Deprecated → Archived)
- ✅ Integration with DDD → BDD → TDD workflow
- ✅ Scope levels (Vision & Strategy, Planning, Implementation)

**SAP Framework Deliverables**:
- Root protocol: `SKILLED_AWARENESS_PACKAGE_PROTOCOL.md`
- Framework SAP artifacts (this charter, protocol spec, etc.)
- SAP Index (`docs/skilled-awareness/INDEX.md`)
- Document templates (`docs/skilled-awareness/document-templates.md`)
- Roadmap (`docs/skilled-awareness/chora-base-sap-roadmap.md`)

**Target Capabilities** (14 total):
1. inbox-coordination (✅ Phase 1 pilot)
2. sap-framework (this SAP, Phase 1)
3. chora-base-meta (Phase 1)
4. project-bootstrap (Phase 2)
5. testing-framework (Phase 2)
6. ci-cd-workflows (Phase 2)
7. quality-gates (Phase 2)
8. documentation-framework (Phase 3)
9. automation-scripts (Phase 3)
10. agent-awareness (Phase 3)
11. memory-system (A-MEM, Phase 3)
12. docker-operations (Phase 3)
13. development-lifecycle (Phase 3)
14. metrics-tracking (Phase 4)

### Out of Scope (for v1.0)

- ❌ Automated SAP generation tools (Phase 4)
- ❌ SAP dashboard/status page (Phase 4)
- ❌ Cross-project SAP federation (Phase 4+)
- ❌ SAP marketplace or discovery service (future)
- ❌ Machine-executable validation (future)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 1):
- ✅ 100% of Phase 1 SAPs use framework (inbox, sap-framework, chora-base-meta)
- ✅ SAP Index exists and is complete
- ✅ Root protocol document exists
- ✅ All Phase 1 SAPs pass pilot validation

**Quality Success** (Phase 2-3):
- ✅ 100% of Phase 2 SAPs use framework (4 core capabilities)
- ✅ 80%+ of Phase 3 SAPs use framework (6 extended capabilities)
- ✅ All SAPs have complete 5-artifact structure
- ✅ Ledger tracks all adopter versions

**Adopter Success** (measured via feedback):
- ✅ Reduced onboarding time (target: 4-8h → 1-2h per capability)
- ✅ Zero upgrade failures (clear migration paths)
- ✅ 90%+ adopter satisfaction (feedback survey)
- ✅ Reduced capability owner support burden (fewer questions)

### Key Metrics

| Metric | Baseline | Target (Phase 2) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| SAP Coverage | 7% (1/14) | 36% (5/14) | 100% (14/14) |
| Onboarding Time | 4-8h | 2-4h | 1-2h |
| Upgrade Failures | Unknown | 0 | 0 |
| Adopter Satisfaction | N/A | 80%+ | 90%+ |
| Support Questions | Baseline | -50% | -80% |

---

## 5. Stakeholders

### Primary Stakeholders

**Capability Owners** (Write SAPs):
- Victor (chora-base owner, all capabilities)
- Future: Delegated capability maintainers

**Agent Operators** (Execute SAPs):
- Claude Code (AI coding agent)
- Cursor Composer (AI coding agent)
- Other LLM-based agents

**Adopter Maintainers** (Use SAPs):
- chora-compose maintainer
- chora-base example projects
- External adopters

### Secondary Stakeholders

**Governance Representatives** (Future):
- Approve major SAP changes
- Review RFCs for breaking changes
- Maintain SAP quality standards

**Ecosystem Projects**:
- ecosystem-manifest (capability registry)
- mcp-orchestration (coordination)
- mcp-gateway (integration)

---

## 6. Dependencies

### Framework Dependencies

**Phase 1 (this SAP depends on)**:
- ✅ Diataxis documentation framework
- ✅ DDD → BDD → TDD workflow
- ✅ inbox-coordination (reference implementation)
- ✅ chora-base v3.0+ (blueprint system, agent support)

**Phase 2+ (future SAPs depend on)**:
- ✅ SAP framework (this SAP)
- ✅ SAP Index
- ✅ Root protocol document

### External Dependencies

**Documentation**:
- Markdown format (universal)
- Diataxis structure (tutorial, how-to, reference, explanation)
- YAML frontmatter (machine-readable metadata)

**Tooling**:
- Git (versioning)
- GitHub (coordination, issues, PRs)
- AI agents (Claude Code, Cursor, etc.)

**Standards**:
- Semantic versioning (major.minor.patch)
- JSON Schema (for infrastructure)
- RFC process (for major changes)

---

## 7. Constraints & Assumptions

### Constraints

1. **No Additional Dependencies**: SAP framework cannot require new tools beyond chora-base defaults
2. **Backward Compatibility**: Existing capabilities must not break when SAP-ified
3. **Agent Compatibility**: All SAP artifacts must be machine-readable by current AI agents
4. **Incremental Adoption**: Adopters can use partial SAPs (e.g., only Charter + Protocol)

### Assumptions

1. **AI Agent Capabilities**: Agents can read markdown, parse YAML, execute blueprints
2. **Adopter Commitment**: Adopters willing to follow blueprint instructions
3. **Single Maintainer**: Victor maintains SAP framework through Phase 3
4. **Git Literacy**: Adopters understand Git, branches, PRs

---

## 8. Risks & Mitigation

### Risk 1: Adoption Overhead

**Risk**: Creating 5 artifacts per capability feels like too much work

**Likelihood**: Medium
**Impact**: High (blocks SAP creation)

**Mitigation**:
- Provide templates for all 5 artifacts
- Start with pilot (inbox SAP) to prove value
- Allow incremental creation (Charter → Protocol → rest)
- Automate where possible (Phase 4)

### Risk 2: Format Churn

**Risk**: SAP format changes frequently, invalidating existing SAPs

**Likelihood**: Medium
**Impact**: Medium (rework existing SAPs)

**Mitigation**:
- Use semantic versioning for SAP framework itself
- Provide upgrade blueprints for SAP format changes
- Stabilize format early (Phase 1-2)
- Minimize breaking changes

### Risk 3: Agent Execution Failures

**Risk**: Agents can't execute blueprints as expected

**Likelihood**: Low
**Impact**: High (SAPs unusable)

**Mitigation**:
- Test blueprints with Claude Code (primary agent)
- Use simple, explicit instructions
- Provide validation commands
- Allow human intervention

### Risk 4: Governance Overhead

**Risk**: RFC/ADR process slows down capability evolution

**Likelihood**: Low
**Impact**: Medium (slower releases)

**Mitigation**:
- Use RFC only for breaking changes
- Allow patch/minor changes without RFC
- 7-day FCP (fast enough for most changes)
- Defer complex governance to Phase 4

---

## 9. Lifecycle

### Phase 1: Framework Hardening (2025-10 → 2025-11)

**Goal**: Establish SAP framework, prove with 3 SAPs

**Deliverables**:
- ✅ Root protocol document (SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- ✅ SAP framework SAP (this charter + 4 other artifacts)
- ✅ SAP Index
- ✅ inbox SAP pilot complete
- ✅ chora-base-meta SAP

**Success**: 3 SAPs live, pilot feedback positive

### Phase 2: Core Capability Migration (2025-11 → 2026-01)

**Goal**: SAP-ify 4 core capabilities

**Deliverables**:
- SAPs: project-bootstrap, testing-framework, ci-cd-workflows, quality-gates
- Ledger entries for all Phase 2 SAPs
- Upgrade blueprints for existing adopters

**Success**: 5 SAPs live (Phase 1 + Phase 2), 36% coverage

### Phase 3: Extended Coverage (2026-01 → 2026-03)

**Goal**: SAP-ify 6 extended capabilities

**Deliverables**:
- SAPs: documentation-framework, automation-scripts, agent-awareness, memory-system, docker-operations, development-lifecycle
- Cross-SAP dependencies documented
- Examples updated to reference SAPs

**Success**: 11 SAPs live, 79% coverage

### Phase 4: Automation & Optimization (2026-03 → 2026-05)

**Goal**: Reduce manual burden, improve tooling

**Deliverables**:
- metrics-tracking SAP
- Automated SAP installation/upgrade tools
- SAP dashboard
- Cross-repo coordination automation

**Success**: 14 SAPs live (100% coverage), automation reduces manual effort by 50%

---

## 10. Related Documents

**Framework Documents**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [document-templates.md](../document-templates.md) - SAP artifact templates
- [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md) - Phased adoption plan
- [INDEX.md](../INDEX.md) - SAP registry

**Reference Implementation**:
- [inbox SAP](../inbox/) - Complete pilot SAP

**Development Process**:
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD → BDD → TDD
- [writing-executable-howtos.md](/docs/user-docs/how-to/write-executable-documentation.md) - Executable documentation

---

## 11. Approval

**Sponsor**: Victor (chora-base owner)
**Approval Date**: 2025-10-27
**Review Cycle**: Quarterly (align with roadmap phases)

**Next Review**: 2025-11-30 (end of Phase 1)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial charter
