# Capability Charter: Cross-Repository Inbox Coordination Protocol

**SAP ID**: SAP-001
**Version**: 1.0.0
**Status**: Pilot (Phase 1)
**Owner**: Victor Piper (chora-base maintainer)
**Created**: 2025-10-27
**Last Updated**: 2025-11-02

---

## 1. Problem Statement

### Current Challenge

The chora-base ecosystem lacks a **consistent, reproducible way** for repositories to exchange strategic proposals, coordination requests, and implementation tasks while keeping documentation and agent guidance aligned.

**Specific Issues**:
1. **Coordination Friction** - No standard format for cross-repo task exchange
2. **Manual Inbox Adoption** - Each repo creates ad-hoc task tracking systems
3. **Uneven Agent Behavior** - Agents handle cross-repo work inconsistently
4. **No Shared Context** - Task status and dependencies invisible across repos
5. **Siloed Communication** - Strategic proposals and implementation tasks mixed together

### Evidence

**From ecosystem review**:
- Coordination friction identified in multi-repo workflows
- Manual inbox adoption varies widely (no standard structure)
- Agent behavior inconsistent when handling cross-repo tasks

**From adopter feedback**:
- "Where should I put strategic proposals?" - No clear answer
- "How do agents know what to work on?" - No coordination protocol
- "How do I track cross-repo dependencies?" - No visibility mechanism

### Business Impact

Without structured inbox coordination:
- **Coordination Overhead**: 30-60 min per task to understand context and dependencies
- **Missed Dependencies**: 20% of cross-repo tasks miss critical dependencies
- **Agent Confusion**: Agents spend 2-4 hours per session searching for tasks
- **Strategic Drift**: Proposals lost in issue trackers, not actioned

---

## 2. Proposed Solution

### Inbox Coordination Protocol SAP

A **Git-native inbox structure** with intake schemas, routing workflows, event logging, and agent operations guidance.

**Key Components**:
1. **Inbox Structure** - `inbox/` directory with strategic/, coordination/, implementation/ subdirectories
2. **Intake Schemas** - JSONL format for proposals, requests, and tasks
3. **Routing Workflows** - Agent playbook for triaging and executing inbox items
4. **Event Logging** - Append-only audit trail for all coordination activities
5. **Adoption Blueprint** - Step-by-step guide for downstream repos

### Key Principles

1. **Git-Native** - File-centric, no SaaS dependencies
2. **Machine-Readable** - JSONL format for agent parsing
3. **Append-Only Events** - Immutable audit trail
4. **Agent-First** - Designed for AI agents (Claude, Cursor) as primary operators
5. **Cross-Repo** - Works across chora-base ecosystem

### Design Trade-offs and Rationale

**Why Git-native file structure instead of issue tracker integration?**
- **Trade-off**: Familiar UI (GitHub Issues) vs. git-versionable coordination
- **Decision**: File-based approach enables offline work, version control, and agent accessibility without API rate limits
- **Alternative considered**: GitHub Projects API integration → rejected due to SaaS dependency and API rate limits

**Why JSONL format instead of markdown or YAML?**
- **Trade-off**: Human readability (markdown) vs. machine parseability (JSONL)
- **Decision**: JSONL provides append-only semantics, line-based parsing for agents, and git-friendly diffs
- **Alternative considered**: Markdown with frontmatter → rejected because append-only events require line-based format

**Why three intake levels (strategic/coordination/implementation) instead of flat structure?**
- **Trade-off**: Simplicity (single inbox/) vs. clear categorization
- **Decision**: Three levels separate long-term proposals from immediate tasks, reducing agent confusion about priority
- **Alternative considered**: Single inbox/ with tags → rejected because directory structure provides clearer mental model

**Why agent-first design instead of human-first?**
- **Trade-off**: Optimized for human reading vs. optimized for agent parsing
- **Decision**: Agents are primary operators in chora-base ecosystem, human-readable formats add overhead
- **Alternative considered**: Human-friendly markdown → rejected because agents need structured data for reliable parsing

**Why shared ledger instead of per-repo tracking?**
- **Trade-off**: Independent tracking (per-repo) vs. ecosystem visibility (shared ledger)
- **Decision**: Shared ledger enables cross-repo dependency tracking and coordination visibility
- **Alternative considered**: Independent tracking → rejected because it hides critical dependencies between repos

---

## 3. Scope

### In Scope

**Inbox Coordination SAP Artifacts**:
- ✅ Capability Charter (this document)
- ✅ Protocol Specification - JSONL schema, event types, routing rules
- ✅ Awareness Guide - Agent workflows for inbox triage and execution
- ✅ Adoption Blueprint - Installation steps for downstream repos
- ✅ Traceability Ledger - Adoption tracking across ecosystem

**Components Covered**:
1. **Inbox Structure** - `inbox/strategic/`, `inbox/coordination/`, `inbox/implementation/`
2. **Event Schema** - JSONL format with trace_id, priority, status, dependencies
3. **Routing Workflows** - Agent decision trees for task triage
4. **Event Logging** - Append-only audit trail conventions
5. **Cross-Repo Integration** - Shared ledger for dependency tracking

**Capability Intersections**:
- **SAP-012** (development-lifecycle): DDD/BDD/TDD workflow integration
- **SAP-010** (memory-system): Event log correlation with A-MEM traces
- **SAP-002** (chora-base-meta): Release coordination patterns

### Out of Scope (for v1.0)

- ❌ Non-file-based workflow tools (Jira, Linear, etc.)
- ❌ Automated cross-repo execution (beyond logging and triage)
- ❌ Real-time synchronization (git-based, eventual consistency)
- ❌ Organization-wide governance policy changes
- ❌ Proprietary task systems (GitHub Projects API integration)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 1 Pilot):
- ✅ SAP-001 complete (all 5 artifacts)
- ✅ Pilot installation in ≥1 additional repo beyond chora-base
- ✅ Agent dry runs complete without intervention
- ✅ Shared ledger tracks pilot feedback

**Quality Success** (Phase 2-3):
- ✅ 80% of ecosystem repos adopt inbox structure
- ✅ Time-to-triage reduced from 30-60 min to <10 min per task
- ✅ Missed dependencies reduced from 20% to <5%
- ✅ Agent confusion time reduced from 2-4h to <30 min per session

### Key Metrics

| Metric | Baseline | Target (Phase 1) | Target (Phase 3) |
|--------|----------|------------------|------------------|
| Repos with Inbox | 1/10 (10%) | 3/10 (30%) | 8/10 (80%) |
| Time-to-Triage | 30-60 min | 15-30 min | <10 min |
| Missed Dependencies | 20% | 10% | <5% |
| Agent Confusion Time | 2-4h/session | 1-2h/session | <30 min/session |
| Coordination Overhead | 60 min/task | 30 min/task | 15 min/task |

---

## 5. Stakeholders

### Primary Stakeholders

**Capability Owner**:
- Victor Piper (chora-base maintainer)
- Maintains SAP-001 protocol and artifacts
- Reviews adoption feedback

**Agent Operators** (Execute Inbox Protocol):
- Claude Code (AI coding agent)
- Cursor Composer (AI coding agent)
- Other LLM-based agents
- Follow awareness-guide workflows

**Repository Maintainers** (Adopt Inbox):
- chora-base (reference implementation)
- chora-compose (pilot adopter)
- Other ecosystem repos
- Install via adoption-blueprint

### Secondary Stakeholders

**Governance Representatives**:
- Review strategic proposals in inbox/strategic/
- Approve major cross-repo coordination
- Maintain ecosystem coherence

**Ecosystem Contributors**:
- Submit coordination requests
- Track dependencies via shared ledger
- Provide adoption feedback

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure and governance
- ✅ chora-base v3.0+ - Git-based coordination infrastructure

**Capability Dependencies** (Optional):
- SAP-010 (memory-system) - Event log correlation with A-MEM traces
- SAP-012 (development-lifecycle) - DDD/BDD/TDD workflow integration
- SAP-002 (chora-base-meta) - Release coordination patterns

### External Dependencies

**Technical Requirements**:
- Git (version control for inbox/)
- JSONL parser (jq, Python json module, etc.)
- AI agents with file system access

**Standards**:
- JSONL format (newline-delimited JSON)
- RFC 4122 (UUID v4 for trace_id)
- Git conventions (branches, commits, PRs)

---

## 7. Risks & Mitigation

### Risk 1: Low Adoption Rate

**Risk**: Ecosystem repos don't adopt inbox structure
**Likelihood**: Medium
**Impact**: High (protocol value depends on network effects)

**Mitigation**:
- Start with pilot in high-visibility repo (chora-compose)
- Document clear value proposition (time savings, dependency visibility)
- Provide automation scripts for bulk adoption (Phase 2)
- Collect and share success stories

### Risk 2: Schema Churn

**Risk**: JSONL schema changes frequently, breaking existing inboxes
**Likelihood**: Medium
**Impact**: Medium (requires migration across all adopters)

**Mitigation**:
- Use semantic versioning for schema (major.minor.patch)
- Provide upgrade blueprints for breaking changes
- Stabilize schema early (Phase 1-2)
- Minimize breaking changes via additive evolution

### Risk 3: Agent Confusion

**Risk**: Agents misinterpret inbox structure or routing rules
**Likelihood**: Low
**Impact**: High (incorrect task execution)

**Mitigation**:
- Test awareness-guide with multiple agents (Claude, Cursor)
- Provide clear decision trees and validation commands
- Include concrete examples in protocol-spec
- Collect agent execution feedback in ledger

### Risk 4: Coordination Overhead

**Risk**: Inbox maintenance adds overhead rather than reducing it
**Likelihood**: Low
**Impact**: Medium (adoption fails)

**Mitigation**:
- Automate common tasks (event creation, status updates)
- Provide templates for common coordination patterns
- Measure time-to-triage before/after adoption
- Iterate based on adopter feedback

---

## 8. Open Questions

1. **Ledger Integration**: How should ledger updates integrate with existing status dashboards?
2. **Bulk Adoption**: Do we need automation scripts for bulk adoption, or is manual sufficient initially?
3. **Escalation Path**: What escalation path handles stalled inbox triage?
4. **Retention Policy**: How long should completed events remain in inbox/ before archival?

---

## 9. Related Documents

**SAP-001 Artifacts**:
- [protocol-spec.md](protocol-spec.md) - JSONL schema, event types, routing rules
- [awareness-guide.md](awareness-guide.md) - Agent workflows for inbox operations
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide for repos
- [ledger.md](ledger.md) - Adoption tracking and feedback

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Framework foundation
- [SAP-002: chora-base-meta](../chora-base/) - Release coordination
- [SAP-010: memory-system](../memory-system/) - Event log correlation
- [SAP-012: development-lifecycle](../development-lifecycle/) - DDD/BDD/TDD integration

**Chora-base Documentation**:
- [INDEX.md](../INDEX.md) - SAP registry
- [ROADMAP.md](/ROADMAP.md) - Ecosystem roadmap

---

## 10. Approval

**Sponsor**: Victor Piper (chora-base owner)
**Approval Date**: 2025-10-27
**Review Cadence**: Quarterly (align with pilot feedback cycles)

**Next Review**: 2026-01-31 (end of Phase 1 pilot)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial charter for inbox coordination SAP
- **1.0.1** (2025-11-02): Added trade-offs section and expanded structure

