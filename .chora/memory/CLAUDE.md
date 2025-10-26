# Claude Memory Integration - mcp-orchestration

**Purpose:** Claude-specific patterns for memory integration and cross-session learning in mcp-orchestration.

**Parent:** See [../../CLAUDE.md](../../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic memory guide.

---

## Claude + Memory Integration for MCP Development

Claude's 200k context window + memory system create powerful cross-session learning for MCP server development:

- **Session memory** (Claude's context) → **Persistent memory** (event log)
- **Working knowledge** (current wave) → **Permanent knowledge** (solved patterns)
- **Ephemeral insights** (implementation) → **Distilled learnings** (architectural decisions)

---

## Memory Tier Strategy for mcp-orchestration

### Tier 1: Claude's Context Window (Ephemeral)

**What:** Current wave, active files, working implementation

**Use for:**
- Current MCP tool development
- Active cryptographic implementation
- Storage layer modifications
- Wave-specific features

**Claude optimization:**
```markdown
"Load essential context for Wave 1.5:
- Current wave plan: project-docs/WAVE_1X_PLAN.md
- Active MCP tool: src/mcp_orchestrator/mcp/server.py
- Recent decisions: .chora/memory/sessions/latest-checkpoint.md

This is Tier 1 - ephemeral session memory."
```

### Tier 2: Event Log (Persistent Operations)

**What:** Timestamped MCP operations, signature verifications, storage operations

**Query pattern for Claude:**
```markdown
"Query recent MCP tool failures to avoid repeating mistakes:

Check var/telemetry/events.jsonl for:
- tool.failed events (last 7 days)
- signature.failed events (authentication issues)
- storage.error events (content-addressable storage problems)

Show me what failed recently so I don't repeat those approaches."
```

**Claude can learn from:**
- Past MCP tool failures (what didn't work)
- Successful signature verification patterns (what did work)
- Storage operation performance (how long operations took)
- Config retrieval patterns (most common client requests)

### Tier 3: Knowledge Graph (Permanent Learnings)

**What:** Architectural decisions, cryptographic patterns, MCP best practices

**Future enhancement:** Once mcp-orchestration implements knowledge graph

**Planned patterns:**
- Ed25519 signature best practices
- Content-addressable storage optimizations
- Multi-client registry patterns
- MCP protocol edge cases

---

## Progressive Memory Loading for MCP Development

### Pattern: Start Wave Development with Memory

```markdown
# Session Start Pattern - Wave 1.5

"Starting work on Wave 1.5 deployment feature. Load memory context:

## Tier 1: Essential (Claude's Context)
- Wave plan: project-docs/WAVE_1X_PLAN.md
- MCP server: src/mcp_orchestrator/mcp/server.py
- Recent checkpoint: .chora/memory/sessions/wave-1-5-checkpoint.md

## Tier 2: Recent Events (Telemetry)
# Check for recent tool failures
tail -50 var/telemetry/events.jsonl | grep -E '(tool.failed|signature.failed)'

## Tier 3: Past Wave Learnings
# Review what worked in previous waves
- Wave 1.4 lessons: Publishing workflow patterns
- Wave 1.3 lessons: User documentation approach
- Wave 1.2 lessons: Draft config builder design

Synthesize these to inform Wave 1.5 implementation."
```

### Pattern: Query Before Implementing MCP Tool

```markdown
# Before implementing new MCP tool
"Before I implement deploy_config tool, check memory:

1. Similar tools implemented?
   - Check src/mcp_orchestrator/mcp/server.py for pattern
   - Review publish_config (Wave 1.4) for similarities

2. Past storage/crypto challenges?
   grep 'storage\|crypto\|signature' var/telemetry/events.jsonl | tail -100

3. What testing patterns worked?
   - Review tests/test_mcp_publish_tool.py (Wave 1.4)
   - Check coverage from previous wave

Use learnings to inform deploy_config implementation."
```

---

## Telemetry Event Integration

### Key Events in mcp-orchestration

```jsonl
{"name": "tool.invoked", "ts": "...", "fields": {"tool": "get_config", "client": "claude-desktop"}}
{"name": "tool.success", "ts": "...", "fields": {"tool": "get_config", "duration_ms": 45}}
{"name": "tool.failed", "ts": "...", "fields": {"tool": "get_config", "error": "..."}}
{"name": "signature.verified", "ts": "...", "fields": {"hash": "...", "valid": true}}
{"name": "signature.failed", "ts": "...", "fields": {"hash": "...", "reason": "..."}}
{"name": "storage.stored", "ts": "...", "fields": {"hash": "...", "size_bytes": 1234}}
{"name": "config.retrieved", "ts": "...", "fields": {"client": "...", "hash": "..."}}
```

### Querying Telemetry with Claude

```markdown
"Analyze recent MCP tool performance:

1. Count tool invocations by type:
   grep 'tool.invoked' var/telemetry/events.jsonl | \
     jq -r '.fields.tool' | sort | uniq -c

2. Find slowest operations:
   grep 'tool.success' var/telemetry/events.jsonl | \
     jq -r 'select(.fields.duration_ms > 100)'

3. Identify error patterns:
   grep 'tool.failed' var/telemetry/events.jsonl | \
     jq -r '.fields.error' | sort | uniq -c

Use insights to optimize current implementation."
```

---

## Checkpoint Patterns for MCP Development

### Wave Development Checkpoints

```markdown
# Checkpoint: Wave 1.5 - Config Deployment - Day 2

## Context
- **Wave:** 1.5 - Configuration Deployment
- **Feature:** deploy_config MCP tool
- **Status:** Implementation 60% complete

## Progress
- ✅ Tool signature defined
- ✅ Storage integration working
- ✅ Signature generation implemented
- ⏳ Client profile deployment (in progress)
- ⏸ Testing (not started)

## Key Decisions
1. Deploy to client profile directly (not draft)
2. Validate config schema before deployment
3. Backup existing config before overwrite
4. Emit telemetry for deployment tracking

## Next Steps
1. Complete client profile deployment logic
2. Add rollback capability
3. Write comprehensive tests
4. Update user documentation

## Files Modified
- src/mcp_orchestrator/mcp/server.py (+85 lines)
- src/mcp_orchestrator/storage/cas.py (+20 lines)
- tests/test_deployment_workflow.py (created)

## Learnings
- Client config format varies (claude-desktop vs cursor)
- Need atomic write for config deployment (temp file + rename)
- Signature verification critical before deployment

## Blockers
None

## Telemetry Notes
- 3 test failures in storage layer (resolved)
- Average tool response time: 45ms (good)
```

### Resume from Checkpoint

```markdown
"Resuming Wave 1.5 development from checkpoint:

Load:
1. .chora/memory/sessions/wave-1-5-day-2.md
2. Files modified: [list from checkpoint]
3. Recent telemetry: last 50 events

Context loaded. Ready to continue with client profile deployment logic.
What's the implementation approach for atomic config writes?"
```

---

## Cross-Wave Learning Patterns

### Pattern: Review Previous Wave Retrospective

```markdown
"Before starting Wave 1.6, review Wave 1.5 retrospective:

Questions to answer:
1. What went well in Wave 1.5?
2. What challenges did we face?
3. What would we do differently?
4. What patterns should we reuse?
5. What technical debt was created?

Document in: .chora/memory/retrospectives/wave-1-5.md
Use learnings for Wave 1.6 planning."
```

---

## Best Practices for Memory Integration

### ✅ Do's

1. **Create checkpoints daily** - Especially during wave development
2. **Query telemetry before debugging** - Learn from past failures
3. **Document wave retrospectives** - Capture learnings for future waves
4. **Use trace IDs** - Correlate related operations in telemetry
5. **Preserve architectural decisions** - Why we chose Ed25519, content-addressable storage
6. **Track performance metrics** - Tool response times, signature verification speed

### ❌ Don'ts

1. **Don't lose context between sessions** - Always save checkpoint
2. **Don't ignore telemetry** - Past failures predict future issues
3. **Don't skip retrospectives** - Wave learnings inform future work
4. **Don't duplicate solutions** - Check memory before implementing
5. **Don't commit without checkpoint** - Session state should be recoverable

---

## Memory Directory Structure

```
.chora/memory/
├── AGENTS.md                    # Generic memory guide
├── CLAUDE.md                    # This file - Claude-specific patterns
├── sessions/                    # Session checkpoints
│   ├── wave-1-5-day-1.md
│   ├── wave-1-5-day-2.md
│   └── latest-checkpoint.md    # Symlink to most recent
└── retrospectives/              # Wave retrospectives
    ├── wave-1-4.md
    ├── wave-1-5.md
    └── lessons-learned.md       # Cross-wave patterns
```

---

## Resources

- **Telemetry Events:** var/telemetry/events.jsonl
- **Parent Claude Guide:** [../../CLAUDE.md](../../CLAUDE.md)
- **Generic Memory Guide:** [AGENTS.md](AGENTS.md)
- **Checkpoint Templates:** [../../claude/CHECKPOINT_PATTERNS.md](../../claude/CHECKPOINT_PATTERNS.md)

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
