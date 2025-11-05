# Protocol Specification: Memory System (A-MEM)

**SAP ID**: SAP-010
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Overview

This protocol defines the **Agentic Memory (A-MEM) architecture** with 4 memory types: Ephemeral Session Memory, Event Log, Knowledge Graph, and Agent Profiles.

**Core Guarantee**: Agents learn from past executions, accumulate knowledge incrementally, and preserve context across sessions.

**Memory Types**: Ephemeral (current session) → Event Log (append-only history) → Knowledge Graph (linked notes) → Agent Profiles (preferences + capabilities)

---

## 2. Architecture

### 2.1 Memory System Overview

```
.chora/memory/
├── README.md                    # A-MEM architecture documentation
├── AGENTS.md                    # Generic agent guidance (~300 lines)
├── CLAUDE.md                    # Claude-specific guidance (~150 lines)
│
├── events/                      # EVENT LOG (append-only)
│   ├── 2025-01/                 # Monthly partitions
│   │   ├── events.jsonl         # All events for month
│   │   └── traces/              # Per-trace event grouping
│   │       ├── abc123.jsonl     # All events for trace_id=abc123
│   │       └── def456.jsonl     # All events for trace_id=def456
│   ├── 2025-02/                 # Next month
│   └── index.json               # Searchable event index
│
├── knowledge/                   # KNOWLEDGE GRAPH (Zettelkasten)
│   ├── notes/                   # Atomic knowledge notes
│   │   ├── backend-timeout-fix.md
│   │   ├── trace-context-pattern.md
│   │   └── error-handling-best-practices.md
│   ├── links.json               # Bidirectional link graph
│   └── tags.json                # Tag index for search
│
├── profiles/                    # AGENT PROFILES (per-agent)
│   ├── claude-code.json         # Claude Code profile
│   ├── cursor-composer.json     # Cursor profile
│   └── codex-agent.json         # Codex profile
│
└── queries/                     # SAVED QUERIES (templates)
    ├── recent-failures.sql      # Find recent failures
    ├── trace-lookup.sql         # Lookup events by trace_id
    └── knowledge-search.sql     # Search knowledge notes
```

### 2.2 Memory Type Characteristics

| Memory Type | Persistence | Format | Purpose | Retention |
|-------------|-------------|--------|---------|-----------|
| **Ephemeral Session Memory** | No (current session only) | In-memory | Real-time context | Until session ends |
| **Event Log** | Yes (append-only) | JSONL | Operation history | 6 months (configurable) |
| **Knowledge Graph** | Yes (cumulative) | Markdown + YAML | Learned patterns | Indefinite (until deprecated) |
| **Agent Profiles** | Yes (versioned) | JSON | Capabilities + preferences | Indefinite (versioned updates) |

---

## 3. Event Log Specification

### 3.1 Event Schema v1.0

**All events must follow this schema**:

```json
{
  "timestamp": "2025-01-17T12:00:00.123Z",
  "trace_id": "abc123",
  "status": "success",
  "schema_version": "1.0",
  "event_type": "gateway.tool_call",
  "source": "project-name",
  "metadata": {
    "tool_name": "example:tool_name",
    "backend": "example-backend",
    "duration_ms": 1234
  }
}
```

**Required Fields**:
- `timestamp` (ISO 8601): When event occurred
- `trace_id` (string): Correlation ID for multi-step workflows
- `status` (enum): `success` | `failure` | `pending` | `timeout`
- `schema_version` (string): Event schema version (currently "1.0")
- `event_type` (string): Hierarchical type (namespace.action, e.g., "gateway.tool_call")
- `source` (string): Project or component that emitted event

**Optional Fields**:
- `metadata` (object): Event-specific data (varies by event_type)
- `metadata.tags` (array of strings): Taxonomy tags for event categorization and search (see Section 3.2)
- `metadata.priority` (enum): Event priority (`critical` | `high` | `normal` | `low`)

---

### 3.2 Event Tag Taxonomy

**Purpose**: Structured vocabulary for consistent event categorization, enabling powerful search and analysis.

**Taxonomy File**: [schemas/event-tag-taxonomy.yaml](../../../schemas/event-tag-taxonomy.yaml)

#### 3.2.1 Tag Domains

The taxonomy organizes tags into **7 major domains**:

| Domain | Description | Example Tags |
|--------|-------------|--------------|
| **development** | Software development activities | `code-generation`, `doc-generation`, `test-execution` |
| **sap** | SAP framework operations | `sap-evaluation`, `sap-generation`, `catalog-update` |
| **automation** | Scripts and CI/CD | `script-invocation`, `ci-pipeline`, `deployment` |
| **coordination** | Cross-repo/agent coordination | `coord-request`, `context-handoff`, `multi-agent` |
| **memory** | A-MEM memory operations | `event-recorded`, `knowledge-learned`, `profile-updated` |
| **infrastructure** | System infrastructure | `gateway-started`, `backend-failed`, `tool-executed` |
| **errors** | Error handling and debugging | `error-encountered`, `retry-attempted`, `trace-analysis` |

**Cross-Cutting Tags**:
- **status**: `success`, `failure`, `pending`, `timeout`
- **priority**: `critical`, `high`, `normal`, `low`
- **impact**: `breaking-change`, `security`, `data-loss`, `performance-impact`

#### 3.2.2 Tag Usage Guidelines

**Best Practices**:
1. **Tag Count**: Use 1-5 tags per event (recommended: 2-3)
2. **Tag Selection**:
   - Always include domain tag (e.g., `sap`, `automation`)
   - Add status tag from event.status field
   - Add specific tags as needed
   - Avoid redundant tags
3. **Tag Naming**: Use lowercase kebab-case (e.g., `sap-evaluation`, `script-success`)

**Example Event with Tags**:
```json
{
  "timestamp": "2025-11-05T12:00:00Z",
  "trace_id": "trace-eval-001",
  "status": "success",
  "schema_version": "1.0",
  "event_type": "sap.evaluation",
  "source": "chora-base",
  "metadata": {
    "tags": ["sap-evaluation", "adoption-analysis"],
    "sap_id": "SAP-015",
    "evaluation_type": "deep",
    "duration_ms": 2400
  }
}
```

#### 3.2.3 Common Tag Patterns

**Pattern 1: SAP Evaluation Workflow**
- Tags: `["sap-evaluation", "adoption-analysis"]`
- Use: Running sap-evaluator.py to assess SAP maturity

**Pattern 2: Successful Script Execution**
- Tags: `["script-invocation", "script-success"]`
- Use: Automation scripts completing successfully

**Pattern 3: Learning from Trace**
- Tags: `["knowledge-learned", "trace-end"]`
- Use: Creating knowledge note after resolving issue in trace

**Pattern 4: Coordination Decomposition**
- Tags: `["coord-request", "coord-decomposition"]`
- Use: Breaking down coordination request into tasks (SAP-001 + SAP-015)

**Pattern 5: Error Recovery**
- Tags: `["error-encountered", "retry-attempted", "recovery-successful"]`
- Use: Error with successful recovery (e.g., backend timeout → retry → success)

#### 3.2.4 Querying Events by Tags

**Find all SAP evaluation events**:
```bash
cat .chora/memory/events/**/*.jsonl | \
  jq 'select(.metadata.tags? // [] | contains(["sap-evaluation"]))'
```

**Find recent failed scripts (last 7 days)**:
```bash
find .chora/memory/events -name "*.jsonl" -mtime -7 -exec \
  jq 'select(.status == "failure" and (.metadata.tags? // [] | contains(["script-failure"])))' {} \;
```

**Count events by tag**:
```bash
cat .chora/memory/events/**/*.jsonl | \
  jq -r '.metadata.tags? // [] | .[]' | \
  sort | uniq -c | sort -rn
```

**Find knowledge notes created from traces**:
```bash
cat .chora/memory/events/**/*.jsonl | \
  jq 'select((.metadata.tags? // [] | contains(["knowledge-learned", "trace-end"])))'
```

#### 3.2.5 Tag Evolution and Maintenance

**Review Policy**: Quarterly tag usage review
- **Deprecate**: Tags with < 10 events in 6 months
- **Add**: New tags when patterns emerge (> 20 events without suitable tag)
- **Version**: Bump taxonomy version on breaking changes

**Backward Compatibility**:
- Tags are optional in event schema (default: `[]`)
- Existing events without tags remain valid
- Scripts must handle missing tags gracefully

---

### 3.4 Event Types

#### Gateway Events

| Event Type | Status | Metadata | Description |
|------------|--------|----------|-------------|
| `gateway.started` | success | `{port, version}` | Gateway server started |
| `gateway.stopped` | success | `{uptime_seconds}` | Gateway server stopped |
| `gateway.tool_call` | success/failure | `{tool_name, backend, duration_ms}` | Tool routed to backend |
| `gateway.backend_registered` | success | `{backend, version}` | Backend registered with gateway |
| `gateway.backend_started` | success/failure | `{backend, startup_time_ms}` | Backend subprocess started |
| `gateway.backend_failed` | failure | `{backend, error, stderr}` | Backend startup/operation failed |

#### Backend Events

| Event Type | Status | Metadata | Description |
|------------|--------|----------|-------------|
| `backend.tool_executed` | success/failure | `{tool_name, duration_ms, result}` | Tool executed by backend |
| `backend.content_generated` | success/failure | `{template, tokens, duration_ms}` | Content generation completed |
| `backend.artifact_assembled` | success/failure | `{artifact_type, size_bytes, duration_ms}` | Artifact assembly completed |
| `backend.validation_completed` | success/failure | `{validator, passed, errors}` | Validation completed |

#### Agent Events

| Event Type | Status | Metadata | Description |
|------------|--------|----------|-------------|
| `agent.session_started` | success | `{agent_name, agent_version}` | Agent session started |
| `agent.session_ended` | success | `{agent_name, duration_minutes, operations_count}` | Agent session ended |
| `agent.error_encountered` | failure | `{error_type, error_message, recovery_action}` | Agent encountered error |
| `agent.knowledge_learned` | success | `{note_id, confidence, tags}` | Agent created knowledge note |

---

### 3.5 Trace Correlation

**Concept**: All events in a multi-step workflow share the same `trace_id`

**Example Workflow**:
```
User request: "Generate and deploy artifact X"

Events (trace_id=abc123):
1. timestamp=12:00:00.000, event_type=agent.session_started, status=success
2. timestamp=12:00:00.100, event_type=gateway.tool_call, status=success (chora:generate_content)
3. timestamp=12:00:00.600, event_type=backend.content_generated, status=success (500ms)
4. timestamp=12:00:00.720, event_type=gateway.tool_call, status=success (chora:assemble_artifact)
5. timestamp=12:00:01.920, event_type=backend.artifact_assembled, status=success (1200ms)
6. timestamp=12:00:02.000, event_type=agent.session_ended, status=success

Total workflow time: 2 seconds
```

**Query by Trace**:
```bash
# List all events for trace_id=abc123
grep '"trace_id": "abc123"' .chora/memory/events/2025-01/events.jsonl

# Or use per-trace file
cat .chora/memory/events/2025-01/traces/abc123.jsonl
```

---

### 3.6 Event Log Retention

**Policy**: Archive events older than 6 months

**Monthly Partitions**:
- Current month: `.chora/memory/events/2025-01/events.jsonl` (active, append-only)
- Previous months: Compressed to `.chora/memory/events/2024-12/events.jsonl.gz`
- Archive (> 6 months): Moved to cloud storage or deleted (configurable)

**Retention Script** (example):
```bash
# Archive events older than 6 months
find .chora/memory/events -name "events.jsonl" -mtime +180 -exec gzip {} \;

# Delete events older than 1 year (optional)
find .chora/memory/events -name "*.jsonl.gz" -mtime +365 -delete
```

---

## 4. Knowledge Graph Specification

### 4.1 Knowledge Note Schema

**Format**: Markdown file with YAML frontmatter

**Required Frontmatter Fields**:
```yaml
---
id: backend-timeout-fix          # Unique ID (kebab-case)
created: 2025-01-17T12:00:00Z    # ISO 8601 creation timestamp
updated: 2025-01-17T14:30:00Z    # ISO 8601 last update
tags: [troubleshooting, backend, timeout]  # Array of tags
---
```

**Optional Frontmatter Fields**:
```yaml
confidence: high                 # low | medium | high (solution reliability)
source: agent-learning           # agent-learning | human-curated | external | research
linked_to: [trace-context-pattern, error-handling-best-practices]  # Related note IDs
status: validated                # draft | validated | deprecated
author: claude-code              # Agent or human who created
related_traces: [abc123, def456] # Trace IDs that led to this learning
```

---

### 4.2 Knowledge Note Structure

**Atomic Note Pattern** (Zettelkasten):

```markdown
---
id: backend-timeout-fix
created: 2025-01-17T12:00:00Z
updated: 2025-01-17T14:30:00Z
tags: [troubleshooting, backend, timeout]
confidence: high
source: agent-learning
linked_to: [trace-context-pattern, error-handling-best-practices]
status: validated
author: claude-code
related_traces: [abc123, def456]
---

# Backend Timeout Fix

## Problem
Backend subprocess fails to start within default 30s timeout when running on slow machines or during high system load.

## Solution
Increase `backend_timeout` configuration to 60s for development environments:

```env
MCP_N8N_BACKEND_TIMEOUT=60
```

## Evidence
- Trace abc123: Backend started successfully at 45s
- Trace def456: Backend started successfully at 52s
- Both would have failed with 30s timeout

## Learned Pattern
When backend startup failures occur, check:
1. System load (via `top` or Activity Monitor)
2. Backend logs for slow initialization steps
3. Increase timeout if startup is legitimately slow

## Related Notes
- [[trace-context-pattern]] - How to trace multi-step workflows
- [[error-handling-best-practices]] - General error handling strategies
```

---

### 4.3 Links Graph

**File**: `.chora/memory/knowledge/links.json`

**Purpose**: Track bidirectional links between knowledge notes

**Structure**:
```json
{
  "notes": [
    {
      "id": "backend-timeout-fix",
      "outgoing_links": [
        "trace-context-pattern",
        "error-handling-best-practices"
      ],
      "incoming_links": [
        "troubleshooting-checklist"
      ],
      "strength": 0.8
    },
    {
      "id": "trace-context-pattern",
      "outgoing_links": [],
      "incoming_links": [
        "backend-timeout-fix",
        "multi-step-workflow-example"
      ],
      "strength": 0.9
    }
  ],
  "clusters": [
    {
      "name": "backend-troubleshooting",
      "notes": [
        "backend-timeout-fix",
        "subprocess-communication-errors",
        "backend-crash-recovery"
      ]
    }
  ]
}
```

**Link Strength**: 0.0 (weak/tangential) to 1.0 (strong/essential)

---

### 4.4 Tags Index

**File**: `.chora/memory/knowledge/tags.json`

**Purpose**: Fast search by tag

**Structure**:
```json
{
  "tags": {
    "troubleshooting": {
      "note_count": 15,
      "notes": [
        "backend-timeout-fix",
        "subprocess-communication-errors",
        "...more"
      ]
    },
    "backend": {
      "note_count": 8,
      "notes": [
        "backend-timeout-fix",
        "backend-crash-recovery",
        "...more"
      ]
    },
    "timeout": {
      "note_count": 3,
      "notes": [
        "backend-timeout-fix",
        "api-timeout-handling",
        "database-timeout-strategies"
      ]
    }
  }
}
```

---

## 5. Agent Profiles Specification

### 5.1 Agent Profile Schema

**Format**: JSON

**File**: `.chora/memory/profiles/{agent-name}.json`

**Structure**:
```json
{
  "agent_name": "claude-code",
  "agent_version": "sonnet-4.5-20250929",
  "last_active": "2025-01-17T14:30:00Z",
  "session_count": 42,
  "capabilities": {
    "backend_management": {
      "skill_level": "advanced",
      "successful_operations": 128,
      "failed_operations": 5,
      "learned_patterns": [
        "backend-timeout-fix",
        "trace-context-pattern"
      ]
    },
    "artifact_creation": {
      "skill_level": "expert",
      "preferred_tool": "chora:assemble_artifact",
      "common_mistakes": [
        "Forgetting to validate content before assembly"
      ]
    }
  },
  "preferences": {
    "verbose_logging": true,
    "auto_retry_on_timeout": true,
    "preferred_backend_timeout": 60
  },
  "context_switches": {
    "total": 15,
    "last_handoff": {
      "to": "other-project",
      "timestamp": "2025-01-16T16:00:00Z",
      "trace_id": "xyz789"
    }
  }
}
```

**Required Fields**:
- `agent_name` (string): Agent identifier (e.g., "claude-code")
- `agent_version` (string): Agent model version
- `last_active` (ISO 8601): Last session timestamp
- `session_count` (integer): Total sessions

**Optional Fields**:
- `capabilities` (object): Per-capability tracking
- `preferences` (object): Agent-specific preferences
- `context_switches` (object): Handoff tracking

---

### 5.2 Capability Tracking

**Structure**:
```json
"capabilities": {
  "capability-name": {
    "skill_level": "novice | intermediate | advanced | expert",
    "successful_operations": 128,
    "failed_operations": 5,
    "learned_patterns": ["pattern-1", "pattern-2"],
    "common_mistakes": ["mistake-1", "mistake-2"]
  }
}
```

**Skill Levels**:
- **novice**: 0-10 successful operations
- **intermediate**: 11-50 successful operations
- **advanced**: 51-100 successful operations
- **expert**: 100+ successful operations

---

## 6. Query Interfaces

### 6.1 Event Log Queries

#### Query Recent Failures
```python
def query_recent_failures(days=7):
    """Get all failure events in last N days."""
    since = datetime.now() - timedelta(days=days)
    failures = []

    for event_file in get_event_files_since(since):
        with open(event_file) as f:
            for line in f:
                event = json.loads(line)
                if event["status"] == "failure":
                    failures.append(event)

    return failures
```

#### Query by Trace ID
```python
def get_events_by_trace(trace_id):
    """Get all events for a trace_id."""
    # Try per-trace file first (fast)
    trace_file = f".chora/memory/events/*/traces/{trace_id}.jsonl"
    if os.path.exists(trace_file):
        return read_jsonl(trace_file)

    # Fallback: scan monthly partitions (slow)
    events = []
    for event_file in get_all_event_files():
        with open(event_file) as f:
            for line in f:
                event = json.loads(line)
                if event["trace_id"] == trace_id:
                    events.append(event)

    return events
```

---

### 6.2 Knowledge Graph Queries

#### Search by Tag
```python
def search_notes_by_tag(tag):
    """Find all notes with given tag."""
    with open(".chora/memory/knowledge/tags.json") as f:
        tags_index = json.load(f)

    return tags_index["tags"].get(tag, {}).get("notes", [])
```

#### Get Linked Notes
```python
def get_linked_notes(note_id):
    """Get all notes linked to/from given note."""
    with open(".chora/memory/knowledge/links.json") as f:
        links_graph = json.load(f)

    for note in links_graph["notes"]:
        if note["id"] == note_id:
            return {
                "outgoing": note["outgoing_links"],
                "incoming": note["incoming_links"]
            }

    return {"outgoing": [], "incoming": []}
```

---

### 6.3 Agent Profile Queries

#### Get Agent Capability Level
```python
def get_capability_level(agent_name, capability):
    """Get agent's skill level for capability."""
    profile = load_agent_profile(agent_name)
    return profile["capabilities"].get(capability, {}).get("skill_level", "novice")
```

#### Update Agent Preferences
```python
def update_preference(agent_name, key, value):
    """Update agent preference."""
    profile = load_agent_profile(agent_name)
    profile["preferences"][key] = value
    profile["last_active"] = datetime.now().isoformat()
    save_agent_profile(agent_name, profile)
```

---

## 7. Cross-Session Learning Patterns

### 7.1 Pattern 1: Learn from Past Failures

**Workflow**:
1. Agent encounters error (e.g., backend timeout)
2. Query event log for similar failures: `query_recent_failures()`
3. Check if knowledge note exists for this error pattern
4. If exists: Apply learned solution (e.g., increase timeout)
5. If not exists: Create knowledge note after resolving

**Example**:
```python
# Agent encounters backend timeout
error = "Backend failed to start (timeout 30s)"

# Query for similar failures
recent_failures = query_recent_failures(days=30)
similar_failures = [f for f in recent_failures if "timeout" in f["metadata"].get("error", "")]

# Check if knowledge exists
timeout_notes = search_notes_by_tag("timeout")
if "backend-timeout-fix" in timeout_notes:
    # Apply learned solution
    solution = load_knowledge_note("backend-timeout-fix")
    print(f"Applying known solution: {solution['content']}")
    increase_backend_timeout(60)  # From learned pattern
else:
    # No existing knowledge, resolve manually
    # After resolution, create knowledge note
    create_knowledge_note(
        id="backend-timeout-fix",
        content="Increase backend_timeout to 60s for slow machines",
        tags=["troubleshooting", "backend", "timeout"],
        confidence="medium"  # Will upgrade to "high" after more validations
    )
```

---

### 7.2 Pattern 2: Trace Multi-Step Workflows

**Workflow**:
1. Agent starts multi-step operation (generate trace_id)
2. Emit events for each step with same trace_id
3. If failure occurs, query all events for trace_id
4. Analyze timeline to identify bottleneck/failure point

**Example**:
```python
# Start workflow
trace_id = generate_trace_id()  # e.g., "abc123"

# Step 1: Generate content
emit_event("gateway.tool_call", trace_id=trace_id, metadata={"tool": "generate_content"})
# ... operation ...
emit_event("backend.content_generated", trace_id=trace_id, status="success")

# Step 2: Assemble artifact
emit_event("gateway.tool_call", trace_id=trace_id, metadata={"tool": "assemble_artifact"})
# ... operation fails ...
emit_event("backend.artifact_assembled", trace_id=trace_id, status="failure", metadata={"error": "Validation failed"})

# Analyze failure
events = get_events_by_trace(trace_id)
for event in events:
    print(f"{event['timestamp']}: {event['event_type']} - {event['status']}")

# Output:
# 12:00:00.000: gateway.tool_call - success
# 12:00:00.500: backend.content_generated - success
# 12:00:00.600: gateway.tool_call - success
# 12:00:01.800: backend.artifact_assembled - failure (Validation failed at step 2)
```

---

### 7.3 Pattern 3: Preserve Agent Preferences

**Workflow**:
1. Agent completes session with preferences (e.g., verbose_logging=true)
2. Save preferences to agent profile
3. Next session: Load agent profile, apply preferences automatically

**Example**:
```python
# Session 1: User sets preference
user_preference = {"verbose_logging": true, "preferred_backend_timeout": 60}
update_preference("claude-code", "verbose_logging", true)
update_preference("claude-code", "preferred_backend_timeout", 60)

# Session 2 (new session, hours later)
profile = load_agent_profile("claude-code")
verbose = profile["preferences"].get("verbose_logging", false)  # Gets true
timeout = profile["preferences"].get("preferred_backend_timeout", 30)  # Gets 60

# Agent uses preserved preferences
if verbose:
    print("Verbose logging enabled (from previous session)")
set_backend_timeout(timeout)  # Uses 60s (learned preference)
```

---

## 8. Retention and Archival

### 8.1 Event Log Retention

**Default Policy**: 6 months

**Archival Process**:
1. Monthly: Compress events older than 1 month (`.jsonl` → `.jsonl.gz`)
2. Quarterly: Move events older than 6 months to archive (cloud storage or delete)

**Script** (example):
```bash
# Compress old events (monthly)
find .chora/memory/events -name "events.jsonl" -mtime +30 -exec gzip {} \;

# Archive events > 6 months (quarterly)
find .chora/memory/events -name "*.jsonl.gz" -mtime +180 -exec mv {} /archive/ \;
```

---

### 8.2 Knowledge Note Retention

**Policy**: Indefinite (until marked deprecated)

**Deprecation Process**:
1. Update frontmatter: `status: deprecated`
2. Add deprecation reason to note content
3. Link to replacement note (if applicable)
4. Archive after 1 year of deprecation

**Example**:
```markdown
---
id: old-backend-pattern
status: deprecated
---

# Old Backend Pattern (DEPRECATED)

**Deprecated**: 2025-01-17
**Reason**: Superseded by new architecture
**Replacement**: [[new-backend-pattern]]

[Original content preserved for historical reference]
```

---

### 8.3 Agent Profile Retention

**Policy**: Indefinite (versioned updates)

**Versioning**:
- Major version change: Breaking schema change (e.g., rename fields)
- Minor version change: Add new fields (backward compatible)
- Patch version change: Update values only

**Migration** (on breaking change):
```python
def migrate_profile_v1_to_v2(profile_v1):
    """Migrate agent profile from v1 to v2 schema."""
    profile_v2 = {
        "agent_name": profile_v1["agent_name"],
        "agent_version": profile_v1["agent_version"],
        # ... map old fields to new fields
        "schema_version": "2.0"
    }
    return profile_v2
```

---

## 9. Integration with Other SAPs

### 9.1 SAP-009 (agent-awareness)
- **Awareness files**: `.chora/memory/AGENTS.md`, `.chora/memory/CLAUDE.md`
- **Nested pattern**: Memory directory has its own awareness files

### 9.2 SAP-013 (metrics-tracking)
- **Metrics source**: Event log provides raw data for process metrics
- **Query integration**: Metrics dashboard queries event log

---

## 10. Anti-Patterns

### Anti-Pattern 1: Mutating Event Log
**Wrong**: Edit or delete events in event log
**Correct**: Event log is append-only (never mutate)
**Why**: Audit trail integrity, trace correlation breaks if events deleted

### Anti-Pattern 2: Duplicate Knowledge Notes
**Wrong**: Create new note for every similar issue
**Correct**: Search existing notes first, update if exists
**Why**: Knowledge fragmentation, difficult to find authoritative source

### Anti-Pattern 3: Ignoring Confidence Levels
**Wrong**: Apply low-confidence solutions without validation
**Correct**: Check confidence level, validate low-confidence patterns
**Why**: Low-confidence patterns may be incorrect or context-specific

### Anti-Pattern 4: No Tag Discipline
**Wrong**: Inconsistent tags ("backend", "Backend", "backend-issues")
**Correct**: Use tag index, normalize tags (lowercase, hyphenated)
**Why**: Search fragmentation, tags lose value

---

## 10.5. Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/memory-system/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Quick Reference / Quick Start for Claude
- [ ] Common Workflows / Claude Code Workflows (6 workflows in AGENTS.md, 4 in CLAUDE.md)
- [ ] Best Practices / Claude-Specific Tips (5 each)
- [ ] Common Pitfalls (5 each)
- [ ] Integration with Other SAPs / Support & Resources

**Source Artifact Coverage (Both Files)**:
- [ ] capability-charter.md A-MEM architecture → "Memory Architecture" section
- [ ] protocol-spec.md event schema/retention → "Memory Types" section
- [ ] awareness-guide.md workflows → "Common Workflows" section
- [ ] adoption-blueprint.md installation → "Quick Reference" section
- [ ] ledger.md adoption tracking → referenced in "Best Practices"

**YAML Frontmatter Fields** (Required):
```yaml
sap_id: SAP-010
version: X.Y.Z
status: active | pilot | draft
last_updated: YYYY-MM-DD
type: reference
audience: agents | claude_code
complexity: beginner | intermediate | advanced
estimated_reading_time: N
progressive_loading:
  phase_1: "lines 1-X"
  phase_2: "lines X-Y"
  phase_3: "full"
phase_1_token_estimate: NNNN
phase_2_token_estimate: NNNN
phase_3_token_estimate: NNNN
```

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/memory-system/AGENTS.md && \
test -f docs/skilled-awareness/memory-system/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/memory-system/AGENTS.md | grep "progressive_loading:"
grep -A 10 "^---$" docs/skilled-awareness/memory-system/CLAUDE.md | grep "progressive_loading:"

# Check workflow count equivalence (should be within ±30%)
agents_workflows=$(grep "^### Workflow" docs/skilled-awareness/memory-system/AGENTS.md | wc -l)
claude_workflows=$(grep "^### Workflow" docs/skilled-awareness/memory-system/CLAUDE.md | wc -l)
echo "AGENTS workflows: $agents_workflows, CLAUDE workflows: $claude_workflows"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-010
```

**Expected Workflow Coverage**:
- AGENTS.md: 6 generic workflows (Learn from Failures, Trace Workflow, Preserve Preferences, Query Knowledge, Log Events, Query by Tag)
- CLAUDE.md: 4 Claude Code workflows (Learn with Read, Trace with Bash/Grep, Preserve with Edit, Query with Grep)
- Rationale: Different granularity acceptable - AGENTS.md covers all memory operations, CLAUDE.md focuses on Claude Code tool patterns (Read, Bash, Grep, Edit)

---

## 11. Related Documents

**Memory Infrastructure**:
- [.chora/memory/README.md](/static-template/.chora/memory/README.md) - A-MEM architecture documentation
- [.chora/memory/AGENTS.md](/static-template/.chora/memory/AGENTS.md) - Generic agent guidance
- [.chora/memory/CLAUDE.md](/static-template/.chora/memory/CLAUDE.md) - Claude-specific guidance

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Meta SAP framework
- [SAP-009: agent-awareness](../agent-awareness/) - Awareness files in memory directory
- [SAP-013: metrics-tracking](../metrics-tracking/) - Queries event log for metrics

**External References**:
- Chora ecosystem event schema v1.0
- Zettelkasten methodology (atomic notes, bidirectional linking)
- Agentic Coding Best Practices (A-MEM principles)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for memory-system SAP
