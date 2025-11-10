# SAP-010: Memory System (A-MEM)

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Event-sourced agent memory with JSONL logs, knowledge notes, and trace correlation—restore context across sessions (hours, days, weeks) with structured event logging and Zettelkasten-style notes.

---

## 🚀 Quick Start (2 minutes)

```bash
# Log significant event
echo '{"timestamp":"2025-11-09T12:00:00Z","event_type":"milestone","description":"Completed SAP-009","trace_id":"BATCH-8"}' >> .chora/memory/events/development.jsonl

# Query recent events
tail -20 .chora/memory/events/development.jsonl

# Create knowledge note
cat > .chora/memory/knowledge/notes/agent-awareness-pattern.md <<EOF
# Agent Awareness Pattern

The nested AGENTS.md pattern enables 60-70% token savings.

Links: [[sap-009]] [[progressive-loading]]
EOF
```

**First time?** → Read [.chora/AGENTS.md](../../../.chora/AGENTS.md) for complete memory patterns

---

## 📖 What Is SAP-010?

SAP-010 provides **event-sourced agent memory** with JSONL event logs (development, coordination, testing, errors), knowledge notes (Zettelkasten-style with wikilinks), and trace correlation. Agents can restore context across sessions spanning hours, days, or weeks by querying events and reading knowledge notes—eliminating context re-establishment overhead.

**Key Innovation**: Event sourcing + knowledge graph = long-term agent memory. No database required (file-based JSONL + markdown).

---

## 🎯 When to Use

Use SAP-010 when you need to:

1. **Session continuity** - Restore context across sessions (hours/days/weeks apart)
2. **Event logging** - Track significant events (milestones, decisions, errors)
3. **Knowledge capture** - Create evergreen notes with wikilink connections
4. **Trace correlation** - Link events across SAPs (inbox, beads, memory)
5. **Audit trails** - Review project history, decisions, and learnings

**Not needed for**: Single-session work, or if project history not important

---

## ✨ Key Features

- ✅ **Event-Sourced** - Append-only JSONL logs (never delete history)
- ✅ **4 Event Categories** - development, coordination, testing, errors
- ✅ **Knowledge Notes** - Zettelkasten-style with [[wikilinks]]
- ✅ **Trace Correlation** - Link events via `trace_id` (e.g., COORD-2025-011)
- ✅ **Query Templates** - Pre-built queries for common patterns
- ✅ **Agent Profiles** - Track agent preferences, learnings, patterns
- ✅ **Zero Dependencies** - File-based (no database required)
- ✅ **Git-Friendly** - Text files in .chora/memory/ directory

---

## 📚 Quick Reference

### Directory Structure

```
.chora/memory/
├── events/                 # Event-sourced logs (JSONL)
│   ├── development.jsonl   # Development events (commits, milestones, refactors)
│   ├── coordination.jsonl  # Cross-repo coordination (SAP-001 integration)
│   ├── testing.jsonl       # Test events (failures, coverage, TDD cycles)
│   └── errors.jsonl        # Error events (exceptions, debugging sessions)
├── knowledge/              # Knowledge notes
│   └── notes/              # Zettelkasten-style notes with wikilinks
│       ├── sap-009.md
│       ├── agent-awareness-pattern.md
│       └── progressive-loading.md
├── agents/                 # Agent profiles
│   └── claude-sonnet-4.5.json
└── queries/                # Query templates
    ├── recent-milestones.sh
    └── error-patterns.sh
```

---

### Event Schema (JSONL)

```json
{
  "timestamp": "2025-11-09T12:00:00Z",
  "event_type": "milestone|decision|error|commit|test_failure",
  "description": "Human-readable event description",
  "trace_id": "COORD-2025-011",  // Optional: correlate across SAPs
  "metadata": {
    "sap_id": "SAP-009",
    "files_changed": ["AGENTS.md", "protocol-spec.md"],
    "lines_added": 164
  }
}
```

---

### Common Event Types

| Event Type | Category | Example |
|------------|----------|---------|
| **milestone** | development | "Completed SAP-009 discoverability" |
| **decision** | development | "Chose Diátaxis for documentation framework" |
| **error** | errors | "TypeError in server.py:42" |
| **commit** | development | "feat(SAP-009): Add comprehensive README" |
| **test_failure** | testing | "test_authentication.py::test_login FAILED" |
| **coordination_request** | coordination | "COORD-2025-011 received from project-x" |

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-001** (Inbox) | Event correlation | Coordination events → `.chora/memory/events/coordination.jsonl` |
| **SAP-015** (Beads) | Task tracking | Link beads to events via `trace_id` |
| **SAP-013** (Metrics) | ROI tracking | Track time saved, bugs fixed via events |
| **SAP-027** (Dogfooding) | Pilot validation | Log pilot candidates, research, decisions |
| **SAP-012** (Lifecycle) | Development history | Track DDD → BDD → TDD phases |

**Cross-SAP Workflow Example**:
```bash
# 1. Receive coordination request (SAP-001)
just inbox-query-incoming
# COORD-2025-011: "Add real-time sync to MCP server"

# 2. Log coordination event (SAP-010)
echo '{"timestamp":"'$(date -Iseconds)'","event_type":"coordination_request","description":"Received COORD-2025-011","trace_id":"COORD-2025-011"}' >> .chora/memory/events/coordination.jsonl

# 3. Create task (SAP-015)
bd create "Implement real-time sync for COORD-2025-011" --trace-id COORD-2025-011

# 4. Work on implementation (log milestones)
echo '{"timestamp":"'$(date -Iseconds)'","event_type":"milestone","description":"Completed Socket.IO integration","trace_id":"COORD-2025-011"}' >> .chora/memory/events/development.jsonl

# 5. Create knowledge note (SAP-010)
cat > .chora/memory/knowledge/notes/real-time-sync-pattern.md <<EOF
# Real-Time Sync Pattern

Used Socket.IO for bidirectional communication in MCP server.

Lessons: SSE simpler for one-way, Socket.IO for bidirectional.

Links: [[mcp-server]] [[COORD-2025-011]] [[SAP-014]]
EOF

# 6. Complete coordination (SAP-001)
just inbox-respond COORD-2025-011 completed
```

---

## 🏆 Success Metrics

- **Context Restoration**: 80-90% faster than re-reading docs (query events vs read all)
- **Session Continuity**: Resume work after days/weeks with full context
- **Trace Coverage**: 70%+ events have `trace_id` for correlation
- **Knowledge Growth**: Average 3-5 new notes per week
- **Event Volume**: 10-20 events per development session

---

## 🔧 Troubleshooting

**Problem**: `.chora/memory/` directory doesn't exist

**Solution**: Memory system only exists in generated projects (not in chora-base template):
```bash
# Initialize memory system in generated project
mkdir -p .chora/memory/{events,knowledge/notes,agents,queries}
touch .chora/memory/events/{development,coordination,testing,errors}.jsonl
```

---

**Problem**: JSONL files become large (>10MB)

**Solution**: Rotate event logs periodically:
```bash
# Archive old events (keep last 6 months)
mv .chora/memory/events/development.jsonl .chora/memory/events/development-$(date +%Y-%m).jsonl
touch .chora/memory/events/development.jsonl
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete A-MEM specification
- **[.chora/AGENTS.md](../../../.chora/AGENTS.md)** - Memory patterns (13-min read)
- **[.chora/CLAUDE.md](../../../.chora/CLAUDE.md)** - Claude workflows (8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Memory system setup guide
- **[capability-charter.md](capability-charter.md)** - Design rationale
- **[ledger.md](ledger.md)** - Production adoption metrics

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial event-sourced memory with 4 event categories, knowledge notes, trace correlation

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
