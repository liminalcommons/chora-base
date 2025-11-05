# Capability Charter: Agent Task Tracking with Beads

**SAP ID**: SAP-015
**Version**: 1.0.0
**Status**: Pilot (Phase 1)
**Owner**: Victor Piper (chora-base maintainer)
**Created**: 2025-11-04
**Last Updated**: 2025-11-04

---

## 1. Problem Statement

### Current Challenge

AI coding agents lack **persistent task memory** across sessions, leading to lost context, forgotten subtasks, and repeated mistakes when handling complex multi-step projects.

**Specific Issues**:
1. **Session Amnesia** - Agents forget task state when context resets
2. **Lost Dependencies** - No tracking of blocking relationships between tasks
3. **Manual Tracking** - Developers manually maintain task lists in markdown/issues
4. **No Cross-Session Continuity** - Complex projects span multiple sessions without memory
5. **Coordination Overhead** - Multi-agent scenarios lack shared task visibility

### Evidence

**From ecosystem experience**:
- Agents frequently ask "What should I work on?" at session start
- Complex features (5+ steps) often have abandoned subtasks
- Developers maintain external task lists (Notion, Linear, etc.) for agent coordination
- Session context loss causes 20-30% rework on multi-day projects

**From beads project**:
- Steve Yegge created beads specifically to solve agent amnesia
- Git-backed JSONL format provides persistent task storage
- Hash-based IDs prevent multi-agent collision
- Dependency tracking enables "ready work" detection

### Business Impact

Without persistent agent task tracking:
- **Lost Productivity**: 20-30% time spent re-establishing context at session start
- **Abandoned Work**: Complex features incomplete due to forgotten subtasks
- **Manual Overhead**: 10-20 min per session maintaining external task lists
- **Coordination Friction**: Multi-agent workflows require manual synchronization
- **Rework**: 15-25% duplicate effort from forgotten completed tasks

---

## 2. Proposed Solution

### Agent Task Tracking SAP (Beads Integration)

A **git-backed task tracking system** designed for AI agents, providing persistent memory across sessions with dependency management and multi-agent coordination.

**Key Components**:
1. **Beads CLI** - Command-line interface for issue/task management
2. **Git-Backed Storage** - `.beads/issues.jsonl` as source of truth (committed)
3. **Local SQLite Cache** - `.beads/beads.db` for fast queries (gitignored)
4. **Dependency Management** - Tracks blocks, related, parent-child relationships
5. **Agent Workflows** - Integration patterns for Claude Code, Cursor, other agents

### Key Principles

1. **Git-Native** - Storage in `.beads/issues.jsonl`, distributed via git
2. **Agent-First** - Designed for AI agents as primary operators
3. **Persistent Memory** - Tasks survive context resets and session boundaries
4. **Dependency-Aware** - Automatic ready-work detection based on blockers
5. **Multi-Agent Safe** - Hash-based IDs prevent collision across agents/machines

### Design Trade-offs and Rationale

**Why beads instead of GitHub Issues?**
- **Trade-off**: Familiar UI (GitHub) vs. git-native accessibility (beads)
- **Decision**: Beads provides offline access, no API rate limits, agent-friendly CLI
- **Alternative considered**: GitHub Issues API → rejected due to online requirement and API complexity

**Why git-backed JSONL instead of SQLite only?**
- **Trade-off**: Simplicity (SQLite) vs. distributed coordination (JSONL + git)
- **Decision**: JSONL enables multi-machine sync via git, SQLite provides performance
- **Alternative considered**: SQLite only → rejected due to lack of distribution mechanism

**Why optional SAP instead of built-in?**
- **Trade-off**: Universal availability vs. external dependency management
- **Decision**: Optional adoption allows validation before committing ecosystem
- **Alternative considered**: Built-in requirement → rejected due to external Go dependency

**Why beads instead of integrating with SAP-001 (inbox)?**
- **Trade-off**: Consistency (reuse inbox) vs. specialized tool (beads)
- **Decision**: Beads provides mature dependency tracking, ready-work detection
- **Alternative considered**: Extend SAP-001 → rejected to avoid disrupting v1.1.0

**Why separate from SAP-010 (A-MEM)?**
- **Trade-off**: Unified memory system vs. specialized task tracking
- **Decision**: A-MEM tracks "what was done", beads tracks "what to do"
- **Alternative considered**: Merge with A-MEM → rejected due to different purposes

---

## 3. Scope

### In Scope

**Task Tracking SAP Artifacts**:
- ✅ Capability Charter (this document)
- ✅ Protocol Specification - Beads CLI commands, workflows, schema
- ✅ Awareness Guide - Agent workflows for task creation, triage, completion
- ✅ Adoption Blueprint - Installation steps, beads initialization
- ✅ Traceability Ledger - Adoption tracking across ecosystem

**Components Covered**:
1. **Beads Installation** - npm package, CLI verification
2. **Repository Initialization** - `bd init`, git hooks, config
3. **Task Workflows** - Create, list, update, close, dependency management
4. **Agent Integration** - AGENTS.md patterns, awareness guide integration
5. **Integration Scripts** - `beads-init.py`, `beads-sync.py`, `beads-export.py`

**Capability Intersections**:
- **SAP-001** (inbox): Coordination tasks can reference beads issues
- **SAP-010** (memory-system): A-MEM events can correlate with beads task IDs
- **SAP-009** (agent-awareness): AGENTS.md includes beads workflow patterns

### Out of Scope (for v1.0)

- ❌ Replacing SAP-001 inbox protocol (separate concerns)
- ❌ Merging with SAP-010 A-MEM (different memory purposes)
- ❌ Custom beads server development (use upstream beads)
- ❌ Web UI for beads (CLI-first design)
- ❌ Beads daemon management (optional background sync)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Phase 1 Pilot):
- ✅ SAP-015 complete (all 5 artifacts)
- ✅ Beads initialized in chora-base (dogfooding)
- ✅ Integration scripts functional (`beads-init.py`, etc.)
- ✅ Pilot installation in ≥1 additional repo beyond chora-base
- ✅ Agent dry runs complete without intervention

**Quality Success** (Phase 2-3):
- ✅ 20%+ reduction in session context re-establishment time
- ✅ 30%+ reduction in forgotten subtasks on complex features
- ✅ 50%+ reduction in manual task list maintenance overhead
- ✅ 30%+ adoption rate in generated projects (opt-in)
- ✅ 80%+ developer satisfaction with beads workflow

### Key Metrics

| Metric | Baseline | Target (Phase 1) | Target (Phase 3) |
|--------|----------|------------------|------------------|
| Context Re-establishment Time | 10-20 min/session | 5-15 min/session | <5 min/session |
| Forgotten Subtasks (Complex Features) | 30-40% | 15-25% | <10% |
| Manual Task List Maintenance | 10-20 min/session | 5-10 min/session | <3 min/session |
| Adoption Rate (Generated Projects) | 0% | 10-20% | 30%+ |
| Developer Satisfaction | N/A | 70%+ | 80%+ |

---

## 5. Stakeholders

### Primary Stakeholders

**Capability Owner**:
- Victor Piper (chora-base maintainer)
- Maintains SAP-015 protocol and artifacts
- Reviews adoption feedback

**Agent Operators** (Use Beads for Task Tracking):
- Claude Code (AI coding agent)
- Cursor Composer (AI coding agent)
- Other LLM-based agents
- Follow awareness-guide workflows

**Repository Maintainers** (Adopt Beads):
- chora-base (reference implementation, dogfooding)
- Ecosystem repos (optional adoption)
- Install via adoption-blueprint

### Secondary Stakeholders

**Beads Project**:
- Steve Yegge (beads creator/maintainer)
- Upstream beads development
- Feature requests and bug reports

**Ecosystem Contributors**:
- Provide adoption feedback
- Report integration issues
- Share workflow patterns

---

## 6. Dependencies

### Internal Dependencies

**Framework Dependencies**:
- ✅ SAP-000 (sap-framework) - Provides SAP structure and governance
- ✅ chora-base v4.9.0+ - Git-based project infrastructure

**Capability Dependencies** (Optional):
- SAP-001 (inbox) - Coordination tasks can reference beads issues
- SAP-010 (memory-system) - A-MEM events can correlate with task IDs
- SAP-009 (agent-awareness) - AGENTS.md includes beads patterns

### External Dependencies

**Technical Requirements**:
- Git (version control for `.beads/issues.jsonl`)
- Node.js 18+ (for npm package `@beads/bd`)
- Beads CLI v0.21.6+ (installed via npm)

**Standards**:
- JSONL format (newline-delimited JSON)
- Hash-based IDs (beads v0.20.1+ collision-resistant IDs)
- Git conventions (branches, commits, PRs)

**External Project**:
- [beads](https://github.com/steveyegge/beads) - Upstream project (Go)
- npm package: `@beads/bd` (official distribution)
- Active maintenance (as of November 2025)

---

## 7. Risks & Mitigation

### Risk 1: External Dependency

**Risk**: Beads project could become unmaintained or breaking changes
**Likelihood**: Low-Medium
**Impact**: High (SAP-015 becomes non-functional)

**Mitigation**:
- SAP-015 as optional capability (can be skipped)
- Document alternative approaches (manual task lists, SAP-001 only)
- Monitor beads project health quarterly
- Consider forking if upstream becomes unmaintained

### Risk 2: Learning Curve

**Risk**: Developers/agents struggle with beads CLI commands
**Likelihood**: Medium
**Impact**: Medium (adoption friction)

**Mitigation**:
- Comprehensive awareness guide with examples
- Integration scripts abstract common workflows
- AGENTS.md patterns for agent self-guidance
- Tutorial documentation with step-by-step examples

### Risk 3: Overlap Confusion

**Risk**: Confusion about when to use beads vs inbox (SAP-001) vs A-MEM (SAP-010)
**Likelihood**: Medium
**Impact**: Medium (suboptimal capability usage)

**Mitigation**:
- Clear capability charter defining boundaries:
  - **Beads**: Agent task tracking ("what to do")
  - **Inbox**: Cross-repo coordination ("strategic alignment")
  - **A-MEM**: Event history ("what was done")
- Decision tree in awareness guide
- Concrete examples in protocol spec

### Risk 4: Installation Friction

**Risk**: npm package installation fails or beads not in PATH
**Likelihood**: Low
**Impact**: Medium (blocks adoption)

**Mitigation**:
- Detailed installation instructions in adoption blueprint
- Verification steps (`bd version`, `bd doctor`)
- Troubleshooting guide for common issues
- Alternative installation methods (Homebrew, manual)

### Risk 5: Git Merge Conflicts

**Risk**: Multiple agents editing `.beads/issues.jsonl` causes merge conflicts
**Likelihood**: Low (hash-based IDs prevent most conflicts)
**Impact**: Medium (manual resolution required)

**Mitigation**:
- Beads v0.20.1+ uses hash-based IDs (collision-resistant)
- JSONL format is line-based (git-friendly)
- Git hooks installed by `bd init` prevent race conditions
- Sync workflows documented in protocol spec

---

## 8. Open Questions

1. **Daemon Mode**: Should SAP-015 recommend running `bd daemon` for background sync, or keep it manual?
2. **Integration Depth**: Should integration scripts provide bidirectional sync between beads and A-MEM events?
3. **Issue Templates**: Should SAP-015 provide beads issue templates for common chora-base workflows?
4. **Bulk Migration**: Do we need scripts to import existing GitHub Issues into beads for project migration?
5. **Adoption Incentives**: What success stories or metrics would drive adoption beyond pilot phase?

---

## 9. Related Documents

**SAP-015 Artifacts**:
- [protocol-spec.md](protocol-spec.md) - Beads CLI commands, workflows, schema
- [awareness-guide.md](awareness-guide.md) - Agent workflows for task tracking
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide for repos
- [ledger.md](ledger.md) - Adoption tracking and feedback

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Framework foundation
- [SAP-001: inbox](../inbox/) - Cross-repo coordination protocol
- [SAP-009: agent-awareness](../agent-awareness/) - AGENTS.md patterns
- [SAP-010: memory-system](../memory-system/) - A-MEM event history

**External Resources**:
- [beads GitHub Repository](https://github.com/steveyegge/beads)
- [beads npm Package](https://www.npmjs.com/package/@beads/bd)
- [beads Documentation](https://github.com/steveyegge/beads/blob/main/README.md)

**Chora-base Documentation**:
- [INDEX.md](../INDEX.md) - SAP registry
- [ROADMAP.md](/ROADMAP.md) - Ecosystem roadmap

---

## 10. Approval

**Sponsor**: Victor Piper (chora-base owner)
**Approval Date**: 2025-11-04
**Review Cadence**: Quarterly (align with pilot feedback cycles)

**Next Review**: 2026-02-04 (end of Phase 1 pilot - 3 months)

---

**Version History**:
- **1.0.0** (2025-11-04): Initial charter for agent task tracking with beads integration
