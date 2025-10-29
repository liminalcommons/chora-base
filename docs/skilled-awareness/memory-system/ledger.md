---
sap_id: SAP-010
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: ledger
---

# Ledger: Memory System (A-MEM)

**SAP ID**: SAP-010
**Capability Name**: memory-system (A-MEM)
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Adoption Overview

### Coverage Statistics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Projects with A-MEM** | 0 | 70% of chora-base adopters | 🔴 Not started |
| **Event log populated** | 0 | > 0 events per project | 🔴 Not started |
| **Knowledge notes created** | 0 | > 10 notes per project | 🔴 Not started |
| **Agent profiles exist** | 0 | > 0 profiles per project | 🔴 Not started |
| **Schema compliance** | N/A | 100% | 🔴 Not measured |

**Status Legend**:
- 🟢 Target met
- 🟡 Progressing (>50% to target)
- 🔴 Not started or <50% to target

---

## 2. Memory System Usage Metrics

### 2.1 Event Log Statistics

**By Month** (empty - awaiting adoption):

| Month | Events Logged | Traces | Avg Events/Trace | Failures | Success Rate |
|-------|---------------|--------|------------------|----------|--------------|
| 2025-10 | 0 | 0 | 0 | 0 | N/A |
| 2025-11 | 0 | 0 | 0 | 0 | N/A |
| 2025-12 | 0 | 0 | 0 | 0 | N/A |

**Event Type Distribution** (empty - awaiting adoption):

| Event Type | Count | % of Total |
|------------|-------|------------|
| `gateway.tool_call` | 0 | 0% |
| `gateway.tool_result` | 0 | 0% |
| `backend.started` | 0 | 0% |
| `backend.stopped` | 0 | 0% |
| `agent.session_started` | 0 | 0% |
| `agent.session_ended` | 0 | 0% |

**Top 10 Traces by Event Count** (empty):

| Trace ID | Events | Status | Duration | Last Event |
|----------|--------|--------|----------|------------|
| - | - | - | - | - |

---

### 2.2 Knowledge Graph Statistics

**Knowledge Base Size** (empty - awaiting adoption):

| Metric | Value | Baseline | Target |
|--------|-------|----------|--------|
| **Total notes** | 0 | 0 | > 10 per project |
| **Notes by confidence** | | | |
| - High confidence | 0 | 0 | ≥80% of notes |
| - Medium confidence | 0 | 0 | ≤20% of notes |
| - Low confidence | 0 | 0 | 0% (should be upgraded) |
| **Total tags** | 0 | 0 | > 20 unique tags |
| **Total links** | 0 | 0 | > 10 bidirectional links |
| **Avg links per note** | 0 | 0 | ≥ 2 links/note |

**Top 10 Tags by Note Count** (empty):

| Tag | Note Count | % of Total Notes |
|-----|------------|------------------|
| - | - | - |

**Knowledge Note Quality** (empty):

| Status | Count | % of Total |
|--------|-------|------------|
| `validated` | 0 | 0% |
| `draft` | 0 | 0% |
| `deprecated` | 0 | 0% |

**Most Linked Notes** (empty):

| Note ID | Inbound Links | Outbound Links | Total Links |
|---------|---------------|----------------|-------------|
| - | - | - | - |

---

### 2.3 Agent Profile Statistics

**Active Agents** (empty - awaiting adoption):

| Agent Name | Version | Last Active | Session Count | Capabilities Tracked |
|------------|---------|-------------|---------------|----------------------|
| - | - | - | - | - |

**Capability Tracking** (empty):

| Capability | Agents with Capability | Avg Skill Level | Success Rate |
|------------|------------------------|-----------------|--------------|
| - | - | - | - |

**Top 5 Preferences Set** (empty):

| Preference Key | Agents Using | Most Common Value |
|----------------|--------------|-------------------|
| - | - | - |

---

## 3. Event Log Inventory

### 3.1 Monthly Partitions

**Storage by Month** (empty):

| Month | Events File Size | Traces Count | Compression | Status |
|-------|------------------|--------------|-------------|--------|
| 2025-10 | 0 KB | 0 | None | 🔴 Empty |
| 2025-11 | 0 KB | 0 | None | 🔴 Empty |
| 2025-12 | 0 KB | 0 | None | 🔴 Empty |

**Compression Schedule**:
- **Monthly**: Compress events > 1 month old (.jsonl → .jsonl.gz)
- **Quarterly**: Archive events > 6 months old (move to /archive/)

---

### 3.2 Event Schema Compliance

**Schema Version Distribution** (empty):

| Schema Version | Event Count | % of Total | Status |
|----------------|-------------|------------|--------|
| 1.0 | 0 | 0% | 🟢 Current |

**Validation Failures** (empty):

| Month | Total Events | Validation Failures | Failure Rate | Top Error |
|-------|--------------|---------------------|--------------|-----------|
| - | - | - | - | - |

**Target**: 100% schema compliance (0% failure rate)

---

## 4. Cross-Session Learning Metrics

### 4.1 Knowledge Reuse

**Query Statistics** (empty):

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Knowledge queries per session** | 0 | ≥ 3 | 🔴 Not started |
| **Notes reused (cited in new sessions)** | 0 | ≥ 50% of notes | 🔴 Not started |
| **Solutions applied from memory** | 0 | > 0 | 🔴 Not started |

---

### 4.2 Error Pattern Learning

**Repeated Mistakes** (baseline vs current):

| Error Pattern | Baseline (before A-MEM) | Current (with A-MEM) | Reduction % | Target |
|---------------|-------------------------|----------------------|-------------|--------|
| - | - | - | - | 30% |

**Target**: 30% reduction in repeated mistakes

---

### 4.3 Agent Preference Persistence

**Preference Persistence Rate**:

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Sessions with preferences loaded** | 0 | 100% | 🔴 Not started |
| **Preferences overridden per session** | 0 | < 10% | 🔴 Not measured |

---

## 5. Adoption by Project

### 5.1 Project Inventory

**Projects using A-MEM** (empty - awaiting adoption):

| Project Name | chora-base Version | Memory Structure Present | Events Logged | Notes Created | Status |
|--------------|-------------------|--------------------------|---------------|---------------|--------|
| - | - | - | - | - | - |

---

### 5.2 Adoption Levels

**By Level** (empty):

| Adoption Level | Projects | % of Total | Target |
|----------------|----------|------------|--------|
| **Level 1: Basic Event Logging** | 0 | 0% | 30% |
| **Level 2: Knowledge Accumulation** | 0 | 0% | 50% |
| **Level 3: Full Cross-Session Learning** | 0 | 0% | 70% |

**Level Definitions**:
- **Level 1**: Events logged, basic querying
- **Level 2**: Knowledge notes created, tag index used
- **Level 3**: Agent profiles active, automated learning from failures

---

## 6. Quality Metrics

### 6.1 Event Log Quality

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Required fields present** | N/A | 100% | 🔴 Not measured |
| **Valid timestamps** | N/A | 100% | 🔴 Not measured |
| **Valid trace_id format** | N/A | 100% | 🔴 Not measured |
| **Recognized event_type** | N/A | 100% | 🔴 Not measured |

---

### 6.2 Knowledge Note Quality

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Frontmatter complete** | N/A | 100% | 🔴 Not measured |
| **Tags normalized** | N/A | ≥ 90% | 🔴 Not measured |
| **High confidence notes** | N/A | ≥ 80% | 🔴 Not measured |
| **Bidirectional links** | N/A | ≥ 2 per note | 🔴 Not measured |

---

### 6.3 Agent Profile Quality

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Schema version current** | N/A | 100% | 🔴 Not measured |
| **Capabilities tracked** | N/A | > 0 per agent | 🔴 Not measured |
| **Preferences set** | N/A | > 0 per agent | 🔴 Not measured |

---

## 7. Efficiency Metrics

### 7.1 Time Savings

**Estimated Time Saved** (via cross-session learning):

| Activity | Baseline Time | Current Time | Savings | Target |
|----------|---------------|--------------|---------|--------|
| **Debug repeated errors** | Varies | N/A | 0% | 30% |
| **Find relevant past solutions** | Varies | N/A | 0% | 50% |
| **Restore session context** | Varies | N/A | 0% | 80% |

**Target**: 30% time savings overall

---

### 7.2 Developer Experience

**Subjective Metrics** (from adopter feedback):

| Metric | Rating (1-5) | Target |
|--------|--------------|--------|
| **Ease of memory adoption** | N/A | ≥ 4.0 |
| **Memory query performance** | N/A | ≥ 4.0 |
| **Knowledge note discoverability** | N/A | ≥ 4.0 |
| **Agent context preservation** | N/A | ≥ 4.0 |

---

## 8. ROI Analysis

### 8.1 Cost-Benefit

**Costs**:
- Setup time: 15 minutes (Quick Start)
- Level 1 adoption: 2 hours
- Level 2 adoption: 4 hours (cumulative)
- Level 3 adoption: 8 hours (cumulative)
- Maintenance: ~1 hour/month (compress, archive)

**Benefits** (after 3 months at Level 3):
- 30% reduction in repeated mistakes
- Knowledge reuse ≥ 3 queries/session
- Agent preference persistence (100% of sessions)
- Cross-session context (80% time saved on context restoration)

**Break-even**: Estimated 1 month for Level 1, 2 months for Level 3

---

### 8.2 ROI by Adoption Level

| Level | Setup Time | Monthly Maintenance | Benefits (3 months) | ROI |
|-------|------------|---------------------|---------------------|-----|
| **Level 1** | 2 hours | 0.5 hours | 10% time saved on debugging | 2x |
| **Level 2** | 4 hours | 0.5 hours | 20% time saved + knowledge reuse | 3x |
| **Level 3** | 8 hours | 1 hour | 30% time saved + full learning | 5x |

**ROI Calculation**: (Time saved over 3 months) / (Setup + 3 months maintenance)

---

## 9. Maintenance Log

### 9.1 Schema Migrations

**Event Schema Migrations** (empty):

| Date | From Version | To Version | Migration Script | Affected Events |
|------|--------------|------------|------------------|-----------------|
| - | - | - | - | - |

---

### 9.2 Agent Profile Migrations

**Profile Schema Migrations** (empty):

| Date | From Version | To Version | Migration Script | Affected Profiles |
|------|--------------|------------|------------------|-------------------|
| - | - | - | - | - |

---

### 9.3 Cleanup Operations

**Event Log Cleanup** (empty):

| Date | Operation | Files Affected | Space Freed | Status |
|------|-----------|----------------|-------------|--------|
| - | - | - | - | - |

**Operations**:
- **Compress**: Monthly compression of events > 1 month old
- **Archive**: Quarterly archival of events > 6 months old
- **Prune**: (Optional) Delete events > 1 year old

---

## 10. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-10-28 | Initial ledger for memory-system SAP | Claude Code |

---

## 11. Changelog

### 2025-10-28 - SAP-010 Initial Release (v1.0.0)

**Added**:
- Event log tracking (Chora ecosystem schema v1.0)
- Knowledge graph statistics (Zettelkasten methodology)
- Agent profile metrics (capabilities, preferences)
- Cross-session learning metrics (30% reduction target)
- ROI analysis (5x ROI at Level 3)

**Baseline Established**:
- 0 projects with A-MEM (target: 70%)
- 0 events logged (target: > 0 per project)
- 0 knowledge notes (target: > 10 per project)
- 0 agent profiles (target: > 0 per project)

**Next Steps**:
- Monitor adoption (monthly)
- Collect efficiency metrics (quarterly)
- Update ROI analysis (after 3 months of data)

---

## 12. Related Documents

**Memory Infrastructure**:
- [.chora/memory/README.md](/static-template/.chora/memory/README.md) - A-MEM architecture
- [protocol-spec.md](protocol-spec.md) - Memory system contracts
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption guide

**Related SAPs**:
- [SAP-009: agent-awareness](../agent-awareness/) - Awareness files
- [SAP-013: metrics-tracking](../metrics-tracking/) - Event log queries

---

**Ledger Maintenance Schedule**:
- **Weekly**: Update project inventory
- **Monthly**: Update memory usage metrics
- **Quarterly**: Update efficiency metrics, ROI analysis
- **As needed**: Record schema migrations, cleanup operations
