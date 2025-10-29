---
sap_id: SAP-010
version: 1.0.0
status: Draft
last_updated: 2025-10-28
scope: Implementation
---

# Capability Charter: Memory System (A-MEM)

**SAP ID**: SAP-010
**Capability Name**: memory-system (A-MEM)
**Version**: 1.0.0
**Status**: Draft (Phase 3)

---

## 1. Problem Statement

### Current State

chora-base includes the Agentic Memory (A-MEM) architecture in `.chora/memory/` with event logs, knowledge graph, agent profiles, and trace correlation, but **lacks a single authoritative SAP** that:

1. **Defines memory contracts** for event schema, knowledge note format, agent profiles
2. **Documents query interfaces** for accessing memory across sessions
3. **Specifies retention policies** for event cleanup and knowledge archival
4. **Establishes cross-session learning** patterns for agents
5. **Tracks adoption** of A-MEM patterns across projects

### User Pain Points

**From INDEX.md**:
> "Note: User explicitly mentioned A-MEM as needing SAP"

**Specific Issues**:
- Agents lose context between sessions (no memory persistence)
- Repeated mistakes due to lack of learning from past errors
- No structured knowledge accumulation (tribal knowledge lost)
- Difficult to correlate multi-step workflows across sessions
- No standard agent profile format (preferences not portable)

### Impact

**Without this SAP**:
- ❌ Agents repeat same mistakes across sessions (low learning efficiency)
- ❌ Knowledge isolated in individual sessions (no accumulation)
- ❌ Multi-step workflows difficult to debug (no trace correlation)
- ❌ Agent preferences not portable (reset every session)
- ❌ No systematic knowledge sharing between agents

**With this SAP**:
- ✅ Agents learn from past executions (avoid repeating mistakes)
- ✅ Knowledge accumulates incrementally (Zettelkasten-style graph)
- ✅ Multi-step workflows traceable (trace_id correlation)
- ✅ Agent profiles persistent (preferences preserved)
- ✅ Cross-session context enables smarter decisions

---

## 2. Proposed Solution

A **comprehensive SAP defining the A-MEM architecture** with 4 memory types: Ephemeral Session Memory, Event Log, Knowledge Graph, and Agent Profiles.

**Key Principles**:
1. **Append-Only Event Log** - All operations logged, never deleted (audit trail)
2. **Zettelkasten Knowledge Graph** - Atomic notes with bidirectional links
3. **Agent Profiles** - Per-agent capabilities, preferences, learned patterns
4. **Trace Correlation** - Multi-step workflows linked by trace_id
5. **Cross-Session Learning** - Agents query past executions before acting

**Scope**: Implementation level only
- Memory infrastructure for agent learning
- Query interfaces for cross-session context
- Retention policies for long-term storage

---

## 3. Capability Definition

### What This SAP Includes

**Memory Infrastructure** (`.chora/memory/` structure):

**1. Event Log** (`events/`):
- Append-only JSONL event storage
- Monthly partitions (events/2025-01/)
- Per-trace directories (events/2025-01/traces/abc123.jsonl)
- Event index (events/index.json) for fast queries
- Chora ecosystem event schema v1.0
- Event types: gateway.*, backend.*, agent.*

**2. Knowledge Graph** (`knowledge/`):
- Markdown notes with YAML frontmatter
- Zettelkasten methodology (atomic notes, bidirectional links)
- Frontmatter schema: id, created, updated, tags, confidence, source, linked_to, status
- Links index (knowledge/links.json)
- Tags index (knowledge/tags.json)
- Compatible with Obsidian, Zettlr, LogSeq, Foam

**3. Agent Profiles** (`profiles/`):
- JSON format per agent (claude-code.json, cursor-composer.json)
- Capabilities tracking (what agent can do)
- Preferences (coding style, test patterns)
- Learned patterns (successful strategies)
- Session history (past interactions)

**4. Queries** (`queries/`):
- Saved SQL queries for common patterns
- Examples: recent-failures.sql, trace-lookup.sql
- Query templates for agents to use

**Documentation**:
- `.chora/memory/README.md` - A-MEM architecture overview
- `.chora/memory/AGENTS.md` - Generic agent guidance for memory
- `.chora/memory/CLAUDE.md` - Claude-specific memory usage

### What This SAP Excludes

- Event emission logic (covered by application code)
- Real-time monitoring dashboards (covered by SAP-013: metrics-tracking)
- Memory visualization tools (future enhancement)

---

## 4. Success Criteria

### Adoption Metrics

**Target**: 70% of chora-base adopters use A-MEM for cross-session learning

**Measurement**:
- Presence of `.chora/memory/` structure
- Event log populated (> 0 events)
- Knowledge notes created (> 0 notes)
- Agent profiles exist (> 0 profiles)

### Quality Metrics

**Target**: 100% of events follow schema v1.0

**Measurement**:
- Event schema validation passes
- All required fields present (timestamp, trace_id, status, event_type)
- Knowledge note frontmatter validated

### Efficiency Metrics

**Target**: 30% reduction in repeated mistakes (via cross-session learning)

**Measurement**:
- Count of repeated error patterns (before A-MEM vs after)
- Knowledge note reuse rate (queries per session)
- Agent profile preference persistence (session-to-session)

---

## 5. Dependencies

### Upstream Dependencies

- **SAP-000** (sap-framework): Provides SAP structure and governance
- **JSON/JSONL**: Event log format
- **Markdown + YAML**: Knowledge note format

### Downstream Dependencies

- **SAP-013** (metrics-tracking): May query event log for metrics
- **Application code**: Emits events to event log
- **Agent implementations**: Query memory for cross-session context

### Cross-References

- **Chora ecosystem event schema v1.0**: Standardizes event format across chora-* projects
- **Zettelkasten methodology**: Atomic notes with bidirectional linking
- **A-MEM principles**: From "Agentic Coding Best Practices"

---

## 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Event log grows unbounded** | High | Implement retention policy (archive events > 6 months) |
| **Knowledge notes duplicate** | Medium | Deduplication script, link to existing notes |
| **Agent profiles diverge** | Medium | Schema validation, migration guide for breaking changes |
| **Privacy concerns** (sensitive data in events) | High | Sanitization hooks, exclude patterns for sensitive fields |
| **Disk space usage** | Medium | Monthly compression, cloud archive for old events |

---

## 7. Open Questions

1. **Event retention**: 6 months vs 1 year vs indefinite?
2. **Knowledge note limit**: Max notes before archival/pruning?
3. **Agent profile versioning**: How to handle breaking changes?
4. **Privacy**: PII scrubbing before event emission?

---

## 8. Related Capabilities

- **SAP-000** (sap-framework): Meta-framework for all SAPs
- **SAP-009** (agent-awareness): Awareness files in `.chora/memory/` (AGENTS.md, CLAUDE.md)
- **SAP-013** (metrics-tracking): May query event log for process metrics

---

## 9. Approval & Sign-Off

**Charter Author**: Claude Code
**Date**: 2025-10-28
**Status**: Draft - Ready for Protocol Spec

**Approved By**: _(Pending Victor review)_

---

**Next Steps**:
1. Create [protocol-spec.md](protocol-spec.md) - Define event schema, knowledge note format, agent profile schema, query interfaces
2. Create [awareness-guide.md](awareness-guide.md) - Agent workflows for memory usage
3. Create [adoption-blueprint.md](adoption-blueprint.md) - How to adopt A-MEM in projects
4. Create [ledger.md](ledger.md) - Track A-MEM adoption and metrics
