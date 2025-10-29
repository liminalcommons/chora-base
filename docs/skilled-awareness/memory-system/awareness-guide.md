---
sap_id: SAP-010
version: 1.0.0
status: Draft
last_updated: 2025-10-28
audience: ai-agents
---

# Awareness Guide: Memory System (A-MEM)

**SAP ID**: SAP-010
**For**: AI Coding Agents
**Purpose**: Workflows for using A-MEM cross-session memory

---

## 1. Quick Reference

### Memory Types

| Type | When to Use | Persistence |
|------|-------------|-------------|
| **Event Log** | Record all operations | Append-only, 6 months |
| **Knowledge Graph** | Save learned patterns | Indefinite (until deprecated) |
| **Agent Profiles** | Store preferences + capabilities | Indefinite (versioned) |

### Common Workflows

| User Request | Workflow |
|--------------|----------|
| "Learn from past errors" | [3.1 Learn from Past Failures](#31-learn-from-past-failures) |
| "Debug multi-step workflow" | [3.2 Trace Workflow](#32-trace-multi-step-workflow) |
| "Remember my preferences" | [3.3 Preserve Preferences](#33-preserve-agent-preferences) |
| "What did we learn about X?" | [3.4 Query Knowledge](#34-query-knowledge-notes) |

---

## 2. Core Agent Workflows

### 2.1 Before Taking Action: Query Memory

**Pattern**: Always check memory before repeating work

```python
# Example: Before fixing backend timeout
1. Read .chora/memory/knowledge/notes/ (check for existing solutions)
2. If found: Apply learned solution
3. If not found: Resolve issue, then create knowledge note
```

---

## 3. Detailed Workflows

### 3.1 Learn from Past Failures

**When**: Agent encounters error or failure

**Steps**:

**1. Query Recent Failures**
```python
# Check event log for similar failures
Read .chora/memory/events/2025-*/events.jsonl
# Filter by event_type and error pattern
# Example: Find all "backend_failed" events in last 30 days
```

**2. Check Knowledge Notes**
```python
# Search knowledge graph for solutions
Read .chora/memory/knowledge/tags.json
# Look for tags like "troubleshooting", "backend", "timeout"
# If matching note found, read it
Read .chora/memory/knowledge/notes/{note-id}.md
```

**3. Apply Known Solution**
```
If knowledge note exists:
  - Read solution from note
  - Apply solution (e.g., increase timeout)
  - Verify solution works
  - Update note confidence if needed (medium → high)
```

**4. Create Knowledge Note (if new)**
```markdown
Write .chora/memory/knowledge/notes/backend-timeout-fix.md

---
id: backend-timeout-fix
created: 2025-10-28T12:00:00Z
updated: 2025-10-28T12:00:00Z
tags: [troubleshooting, backend, timeout]
confidence: medium
source: agent-learning
status: validated
author: claude-code
related_traces: [abc123]
---

# Backend Timeout Fix

## Problem
[Describe problem]

## Solution
[Describe solution with code examples]

## Evidence
[Link to traces or test results]
```

**5. Update Indexes**
```json
# Update tags.json
Edit .chora/memory/knowledge/tags.json
# Add note to "troubleshooting", "backend", "timeout" tags

# Update links.json (if linking to other notes)
Edit .chora/memory/knowledge/links.json
# Add bidirectional links
```

---

### 3.2 Trace Multi-Step Workflow

**When**: Debugging failed multi-step operation

**Steps**:

**1. Generate Trace ID** (at workflow start)
```python
import uuid
trace_id = str(uuid.uuid4())[:8]  # e.g., "abc12345"
```

**2. Emit Events for Each Step**
```python
# Step 1: Start operation
emit_event({
    "timestamp": "2025-10-28T12:00:00.000Z",
    "trace_id": trace_id,
    "status": "success",
    "event_type": "agent.session_started",
    "source": "project-name",
    "metadata": {"agent": "claude-code"}
})

# Step 2: Tool call
emit_event({
    "timestamp": "2025-10-28T12:00:00.100Z",
    "trace_id": trace_id,
    "status": "success",
    "event_type": "gateway.tool_call",
    "source": "project-name",
    "metadata": {"tool": "generate_content"}
})

# ... more steps ...

# Final step: End operation
emit_event({
    "timestamp": "2025-10-28T12:00:02.000Z",
    "trace_id": trace_id,
    "status": "success",
    "event_type": "agent.session_ended",
    "source": "project-name",
    "metadata": {"duration_seconds": 2}
})
```

**3. Query Events by Trace**
```bash
# Find all events for trace_id
grep '"trace_id": "abc12345"' .chora/memory/events/2025-10/events.jsonl

# Or use per-trace file (faster)
Read .chora/memory/events/2025-10/traces/abc12345.jsonl
```

**4. Analyze Timeline**
```python
# Build timeline from events
events = [...]  # List of events for trace
timeline = []
for event in events:
    timeline.append({
        "timestamp": event["timestamp"],
        "step": event["event_type"],
        "status": event["status"],
        "duration": event["metadata"].get("duration_ms", 0)
    })

# Identify bottlenecks (steps > 1000ms)
bottlenecks = [s for s in timeline if s["duration"] > 1000]

# Identify failures
failures = [s for s in timeline if s["status"] == "failure"]
```

---

### 3.3 Preserve Agent Preferences

**When**: User sets preferences that should persist across sessions

**Steps**:

**1. Load Agent Profile** (at session start)
```python
Read .chora/memory/profiles/claude-code.json
# Get current preferences
preferences = profile["preferences"]
```

**2. Apply Preferences**
```python
# Example preferences
verbose_logging = preferences.get("verbose_logging", false)
backend_timeout = preferences.get("preferred_backend_timeout", 30)

# Use in agent logic
if verbose_logging:
    print("Verbose logging enabled")
set_backend_timeout(backend_timeout)
```

**3. Update Preferences** (when user changes setting)
```python
# User says: "Always use 60s timeout"
profile["preferences"]["preferred_backend_timeout"] = 60
profile["last_active"] = "2025-10-28T12:00:00Z"

Write .chora/memory/profiles/claude-code.json
# Save updated profile
```

**4. Track Capability Growth**
```python
# After successful operation
capability = "backend_management"
profile["capabilities"][capability]["successful_operations"] += 1

# Update skill level based on operation count
count = profile["capabilities"][capability]["successful_operations"]
if count > 100:
    profile["capabilities"][capability]["skill_level"] = "expert"
elif count > 50:
    profile["capabilities"][capability]["skill_level"] = "advanced"
```

---

### 3.4 Query Knowledge Notes

**When**: User asks "What did we learn about X?"

**Steps**:

**1. Search by Tag**
```python
Read .chora/memory/knowledge/tags.json
# Find notes with tag "X"
tag_index = tags_json["tags"]
notes_with_tag = tag_index.get("X", {}).get("notes", [])
```

**2. Search by Content** (if no tag match)
```bash
Grep: "pattern" .chora/memory/knowledge/notes/*.md
# Find notes mentioning keyword
```

**3. Read Matching Notes**
```python
for note_id in notes_with_tag:
    Read .chora/memory/knowledge/notes/{note_id}.md
    # Extract summary from note
    # Check confidence level
    # Return to user
```

**4. Present Results to User**
```markdown
Found 3 knowledge notes about "backend timeout":

1. **backend-timeout-fix** (confidence: high)
   - Problem: Backend fails to start within 30s
   - Solution: Increase timeout to 60s
   - Evidence: 5 successful traces

2. **backend-timeout-alternative** (confidence: medium)
   - Problem: Same as above
   - Solution: Use background startup process
   - Evidence: 2 successful traces

3. **backend-timeout-causes** (confidence: high)
   - Analysis: Common causes of backend timeouts
   - Related: [[system-load-patterns]]
```

---

## 4. Event Emission Patterns

### 4.1 When to Emit Events

**Always emit**:
- Session start/end (`agent.session_started`, `agent.session_ended`)
- Tool calls (`gateway.tool_call`)
- Errors/failures (`agent.error_encountered`, `backend.*_failed`)

**Optional emit**:
- Intermediate steps (for debugging multi-step workflows)
- Performance metrics (duration_ms)

### 4.2 Event Structure

```json
{
  "timestamp": "ISO 8601 timestamp",
  "trace_id": "Workflow correlation ID",
  "status": "success | failure | pending | timeout",
  "schema_version": "1.0",
  "event_type": "namespace.action",
  "source": "project-name",
  "metadata": {
    "... event-specific data ..."
  }
}
```

### 4.3 Emit Event Function

```python
def emit_event(event_type, trace_id, status="success", metadata=None):
    """Emit event to memory system."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "trace_id": trace_id,
        "status": status,
        "schema_version": "1.0",
        "event_type": event_type,
        "source": "project-name",
        "metadata": metadata or {}
    }

    # Append to monthly events file
    month = datetime.now().strftime("%Y-%m")
    event_file = f".chora/memory/events/{month}/events.jsonl"

    # Create directory if needed
    os.makedirs(os.path.dirname(event_file), exist_ok=True)

    # Append event (newline-delimited JSON)
    with open(event_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    # Also write to per-trace file (for fast trace queries)
    trace_file = f".chora/memory/events/{month}/traces/{trace_id}.jsonl"
    os.makedirs(os.path.dirname(trace_file), exist_ok=True)
    with open(trace_file, "a") as f:
        f.write(json.dumps(event) + "\n")
```

---

## 5. Knowledge Note Patterns

### 5.1 When to Create Knowledge Note

**Create note when**:
- Solving non-trivial problem (> 15 min to resolve)
- Pattern likely to recur
- Solution non-obvious from docs
- Learning applies to future sessions

**Don't create note when**:
- Trivial fix (typo, obvious bug)
- One-time issue (won't recur)
- Already documented elsewhere

### 5.2 Knowledge Note Template

```markdown
---
id: descriptive-kebab-case-id
created: 2025-10-28T12:00:00Z
updated: 2025-10-28T12:00:00Z
tags: [category, subcategory, keywords]
confidence: low | medium | high
source: agent-learning | human-curated | external | research
linked_to: [related-note-1, related-note-2]
status: draft | validated | deprecated
author: claude-code | human-name
related_traces: [trace-id-1, trace-id-2]
---

# Title (Clear, Descriptive)

## Problem
[Describe the problem or question]

## Solution
[Describe the solution with code examples]

## Evidence
[Link to traces, test results, or sources]

## Learned Pattern
[Generalizable pattern or checklist]

## Related Notes
- [[related-note-1]] - Description
- [[related-note-2]] - Description
```

---

## 6. Agent Profile Patterns

### 6.1 Initializing Agent Profile

**First session**:
```json
Write .chora/memory/profiles/claude-code.json

{
  "agent_name": "claude-code",
  "agent_version": "sonnet-4.5-20250929",
  "last_active": "2025-10-28T12:00:00Z",
  "session_count": 1,
  "capabilities": {},
  "preferences": {},
  "context_switches": {"total": 0}
}
```

### 6.2 Updating Capability Tracking

**After operation**:
```python
# Load profile
profile = load_agent_profile("claude-code")

# Update capability
capability = "backend_management"
if capability not in profile["capabilities"]:
    profile["capabilities"][capability] = {
        "skill_level": "novice",
        "successful_operations": 0,
        "failed_operations": 0,
        "learned_patterns": [],
        "common_mistakes": []
    }

# Increment counters
if operation_successful:
    profile["capabilities"][capability]["successful_operations"] += 1
else:
    profile["capabilities"][capability]["failed_operations"] += 1

# Add learned pattern (if new knowledge created)
if knowledge_note_created:
    profile["capabilities"][capability]["learned_patterns"].append(note_id)

# Update skill level
count = profile["capabilities"][capability]["successful_operations"]
if count > 100:
    profile["capabilities"][capability]["skill_level"] = "expert"
elif count > 50:
    profile["capabilities"][capability]["skill_level"] = "advanced"
elif count > 10:
    profile["capabilities"][capability]["skill_level"] = "intermediate"

# Save profile
save_agent_profile("claude-code", profile)
```

---

## 7. Memory Maintenance

### 7.1 Compress Old Events (Monthly)

```bash
# Compress events older than 1 month
find .chora/memory/events -name "events.jsonl" -mtime +30 -exec gzip {} \;
```

### 7.2 Archive Events (Quarterly)

```bash
# Move events older than 6 months to archive
find .chora/memory/events -name "*.jsonl.gz" -mtime +180 -exec mv {} /archive/ \;
```

### 7.3 Deprecate Old Knowledge Notes

```markdown
# Update note frontmatter
Edit .chora/memory/knowledge/notes/old-pattern.md

---
status: deprecated  # Changed from "validated"
---

# Old Pattern (DEPRECATED)

**Deprecated**: 2025-10-28
**Reason**: Superseded by new approach
**Replacement**: [[new-pattern]]

[Original content preserved]
```

---

## 8. Common Agent Mistakes

### Mistake 1: Not Checking Memory Before Acting
**Wrong**: Immediately fix issue without checking memory
**Correct**: Query knowledge graph first, apply known solution if exists
**Why**: Avoid repeating work, leverage past learnings

### Mistake 2: Creating Duplicate Knowledge Notes
**Wrong**: Create new note for similar issue without searching
**Correct**: Search by tag first, update existing note if similar
**Why**: Knowledge fragmentation makes search difficult

### Mistake 3: Low-Confidence Solutions Without Validation
**Wrong**: Apply low-confidence solution without testing
**Correct**: Check confidence level, validate before applying
**Why**: Low-confidence patterns may be context-specific or incorrect

### Mistake 4: Not Emitting Events for Multi-Step Workflows
**Wrong**: Skip event emission to "save time"
**Correct**: Emit events for all key steps (use trace_id for correlation)
**Why**: Impossible to debug multi-step failures without event trail

### Mistake 5: Ignoring Agent Profile Preferences
**Wrong**: Start each session with default settings
**Correct**: Load agent profile, apply saved preferences
**Why**: User frustration when preferences reset every session

---

## 9. Integration with Other SAPs

### SAP-009 (agent-awareness)
- `.chora/memory/AGENTS.md` - Generic memory guidance
- `.chora/memory/CLAUDE.md` - Claude-specific memory usage

### SAP-012 (development-lifecycle)
- Event log tracks lifecycle phase transitions
- Knowledge notes document process learnings

### SAP-013 (metrics-tracking)
- Metrics dashboard queries event log
- Process metrics derived from events

---

## 10. Related Documents

**Memory Infrastructure**:
- [.chora/memory/README.md](/static-template/.chora/memory/README.md) - A-MEM architecture
- [protocol-spec.md](protocol-spec.md) - Full memory system contracts

**Related SAPs**:
- [SAP-009: agent-awareness](../agent-awareness/) - Awareness files
- [SAP-013: metrics-tracking](../metrics-tracking/) - Event log queries

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for memory-system SAP
