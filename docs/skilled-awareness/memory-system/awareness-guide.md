---
sap_id: SAP-010
version: 1.0.0
status: Draft
last_updated: 2025-10-28
audience: ai-agents
---

# Awareness Guide: Memory System (A-MEM)

**SAP ID**: SAP-009
**Version**: 1.0.1
**For**: AI Coding Agents
**Purpose**: Workflows for using A-MEM cross-session memory

---

## 1. Quick Reference

### When to Use This SAP

**Use the Memory System SAP when**:
- Learning from past failures (query knowledge graph for solutions)
- Debugging multi-step workflows (trace events by trace_id)
- Preserving user preferences across sessions (agent profiles)
- Tracking capability growth over time (successful_operations counter)
- Understanding what was previously learned about topic X (search knowledge notes)

**Don't use for**:
- Session-specific context - use in-memory variables instead, not disk storage
- Sensitive data storage - memory files are not encrypted, use secret manager
- Real-time metrics - use SAP-013 (metrics-tracking) for live dashboards
- File system backups - use version control (git) for code backup

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

## 9. Common Pitfalls

### Pitfall 1: Not Checking Memory Before Acting

**Scenario**: Agent encounters error, immediately starts debugging without checking if solution already exists in knowledge graph.

**Example**:
```python
# User reports: "Backend timeout error"

# Agent workflow (WRONG):
# 1. Start investigating backend code
# 2. Check logs
# 3. Try various solutions (30 minutes)
# 4. Finally fix by increasing timeout

# Wastes 30 minutes on known problem!
```

**Fix**: Always query knowledge graph FIRST:
```python
# Correct workflow:
# 1. Query knowledge notes for "backend" + "timeout":
Read .chora/memory/knowledge/tags.json
# Find notes tagged with "backend", "timeout"

# 2. Read matching note:
Read .chora/memory/knowledge/notes/backend-timeout-fix.md
# Shows: "Increase timeout from 30s to 60s"

# 3. Apply known solution (confidence: high)
# Takes 2 minutes vs 30 minutes debugging

# 4. Update note if solution worked:
# Increment confidence, add trace_id as evidence
```

**Why it matters**: Knowledge graph exists to prevent re-solving problems. Not checking wastes time. One query takes 30 seconds, debugging from scratch takes 10-60 minutes. Protocol Section 3.1 mandates checking knowledge before new solutions.

### Pitfall 2: Creating Duplicate Knowledge Notes

**Scenario**: Agent creates new knowledge note without searching for similar existing notes, fragments knowledge.

**Example**:
```python
# Agent solves "backend fails to start"
# Creates note: backend-startup-issue.md

# Later, agent solves "backend won't initialize"
# Creates note: backend-initialization-problem.md

# Result: TWO notes for SAME problem!
# User searches for "backend startup" → finds one note, misses other
```

**Fix**: Search by tag BEFORE creating new note:
```python
# Before creating note:
# 1. Search existing notes by tag:
Read .chora/memory/knowledge/tags.json
tag_index["backend"]["notes"]  # Lists all backend-related notes

# 2. Read similar notes:
for note_id in similar_notes:
    Read .chora/memory/knowledge/notes/{note_id}.md
    # Check if same problem

# 3. If similar note exists:
# - UPDATE existing note (don't create new)
# - Add new evidence/trace_id
# - Increment confidence if solution confirmed

# 4. If truly different problem:
# - Create new note
# - Link to related notes (linked_to: [related-note-1])
```

**Why it matters**: Duplicate notes fragment knowledge, make search harder. Protocol Section 5.2 requires checking for duplicates before creating notes. Consolidating notes takes 5 minutes, searching fragmented knowledge wastes 10-20 minutes per search.

### Pitfall 3: Applying Low-Confidence Solutions Without Validation

**Scenario**: Agent finds knowledge note with confidence: low, applies solution without testing, breaks system.

**Example**:
```python
# Agent finds note:
# backend-timeout-fix.md
# confidence: low
# source: agent-learning
# status: draft

# Agent applies solution WITHOUT validation:
# "Increase timeout to 120s"

# Result: Backend now takes 120s to fail (was 30s)
# User waits 4x longer for failures!
```

**Fix**: Check confidence level, validate low-confidence solutions:
```python
# Read note confidence:
note = parse_frontmatter(.chora/memory/knowledge/notes/{note_id}.md)
confidence = note["confidence"]  # low | medium | high

# Apply based on confidence:
if confidence == "high":
    # Apply solution directly (validated by multiple uses)
    apply_solution()
elif confidence == "medium":
    # Apply with caution, monitor results
    apply_solution()
    # Update to "high" if works, "low" if fails
elif confidence == "low":
    # TEST solution in isolated environment first
    test_solution()  # Don't apply to production yet
    if test_passes:
        apply_solution()
        # Promote to "medium" confidence
    else:
        # Update note: status=deprecated, add failure context
```

**Why it matters**: Low-confidence patterns may be context-specific or incorrect. Protocol Section 5.2 defines confidence levels. Applying untested low-confidence solutions can break systems. Testing takes 5-10 minutes, recovering from broken system takes 30-120 minutes.

### Pitfall 4: Not Emitting Events for Multi-Step Workflows

**Scenario**: Multi-step workflow fails, agent can't debug because no event trail exists.

**Example**:
```python
# Agent runs 5-step workflow:
# 1. Fetch data from API
# 2. Transform data
# 3. Validate data
# 4. Write to database
# 5. Update cache

# Workflow fails at step 3
# Agent tries to debug:
# - Which step failed? Unknown
# - How long did each step take? Unknown
# - What was the error? Unknown

# No events emitted, impossible to debug!
```

**Fix**: Emit events for each key step with trace_id:
```python
import uuid

# Generate trace_id at workflow start:
trace_id = str(uuid.uuid4())[:8]

# Step 1: Start workflow
emit_event("workflow.started", trace_id, status="success",
           metadata={"workflow": "data_pipeline"})

# Step 2: Fetch data
emit_event("api.fetch", trace_id, status="success",
           metadata={"records": 100, "duration_ms": 500})

# Step 3: Transform
emit_event("data.transform", trace_id, status="success",
           metadata={"input": 100, "output": 95})

# Step 4: Validate (FAILS)
emit_event("data.validate", trace_id, status="failure",
           metadata={"errors": ["missing_field_X"]})

# Now can query events by trace_id:
# grep '"trace_id": "abc12345"' .chora/memory/events/2025-10/events.jsonl
# Shows complete timeline: Started → Fetched → Transformed → Failed at Validate
```

**Why it matters**: Events enable debugging multi-step failures. Protocol Section 4 mandates events for workflows. Without events, debugging is guesswork. Emitting events adds <1ms per step, debugging without events takes 30-60 minutes.

### Pitfall 5: Overwriting Knowledge Notes Instead of Updating with Versioning

**Scenario**: Agent overwrites existing knowledge note, loses previous solution that was working.

**Example**:
```markdown
# Original note (working solution):
---
id: backend-timeout-fix
confidence: high
---
# Solution: Increase timeout to 60s
(This worked for 10+ traces)

# Agent encounters new timeout issue, overwrites:
---
id: backend-timeout-fix
confidence: medium
---
# Solution: Use background startup
(New approach, only 1 trace)

# Result: Lost high-confidence solution (60s timeout)
# If new solution fails, can't recover old solution!
```

**Fix**: Update notes with versioning, preserve history:
```markdown
# Correct approach:
# 1. Read existing note first
# 2. Add new solution as alternative, don't replace
# 3. Update frontmatter: updated timestamp, add related_traces

---
id: backend-timeout-fix
created: 2025-10-01T12:00:00Z
updated: 2025-10-28T12:00:00Z  # Updated timestamp
confidence: high
related_traces: [abc123, def456, ghi789]  # Added new trace
---

# Backend Timeout Fix

## Solution 1: Increase Timeout (RECOMMENDED)
**Confidence**: High (validated by 10+ traces)
- Increase timeout from 30s to 60s
- Works for 95% of cases

## Solution 2: Background Startup (Alternative)
**Confidence**: Medium (validated by 1 trace)
- Use background process for startup
- Useful when timeout increase not sufficient

[Preserve all historical context]
```

**Why it matters**: Overwriting loses knowledge. Protocol Section 5.2 requires preserving note history. Lost solutions must be re-discovered (wasted effort). Updating notes properly takes 2-3 minutes, re-discovering lost solutions takes 30-60 minutes.

---

## 10. Integration with Other SAPs

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

## 11. Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-010 --source /path/to/chora-base
```

This will automatically install:
- SAP-010 (Memory System / A-MEM)
- SAP-000 (SAP Framework)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Dependencies

This SAP depends on:
- SAP-000 (SAP Framework)

All dependencies are automatically installed.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/memory-system/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

# Verify memory directory structure exists
ls .chora/memory/
# Should show: event/, knowledge/, profile/, trace/ subdirectories
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## 12. Related Content

### Within This SAP (skilled-awareness/memory-system/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-009
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (event schema, knowledge note spec, agent profiles)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for implementing A-MEM
- [ledger.md](ledger.md) - Memory system adoption tracking, version history
- **This document** (awareness-guide.md) - Agent workflows for using cross-session memory

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/debugging-workflow.md](../../dev-docs/workflows/debugging-workflow.md) - Debugging with event traces
- [dev-docs/workflows/knowledge-management.md](../../dev-docs/workflows/knowledge-management.md) - Creating and updating knowledge notes

**Tools**:
- [dev-docs/tools/event-log-query.md](../../dev-docs/tools/event-log-query.md) - Querying event logs
- [dev-docs/tools/knowledge-search.md](../../dev-docs/tools/knowledge-search.md) - Searching knowledge graph

**Development Guidelines**:
- [dev-docs/development/event-emission.md](../../dev-docs/development/event-emission.md) - Standards for emitting events
- [dev-docs/development/knowledge-curation.md](../../dev-docs/development/knowledge-curation.md) - Best practices for knowledge notes

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [static-template/.chora/memory/](/static-template/.chora/memory/) - Memory system directory structure
- [static-template/.chora/memory/README.md](/static-template/.chora/memory/README.md) - A-MEM architecture documentation
- [static-template/.chora/memory/knowledge/](/static-template/.chora/memory/knowledge/) - Knowledge graph structure

**Guides**:
- [project-docs/guides/memory-system-setup.md](../../project-docs/guides/memory-system-setup.md) - Setting up A-MEM in projects
- [project-docs/guides/event-log-analysis.md](../../project-docs/guides/event-log-analysis.md) - Analyzing event logs

**Audits & Releases**:
- [project-docs/audits/](../../project-docs/audits/) - SAP audits including SAP-009 validation
- [project-docs/releases/](../../project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/cross-session-memory.md](../../user-docs/guides/cross-session-memory.md) - Understanding A-MEM

**Tutorials**:
- [user-docs/tutorials/creating-knowledge-notes.md](../../user-docs/tutorials/creating-knowledge-notes.md) - Create knowledge notes
- [user-docs/tutorials/tracing-workflows.md](../../user-docs/tutorials/tracing-workflows.md) - Debug with event traces

**Reference**:
- [user-docs/reference/event-schema.md](../../user-docs/reference/event-schema.md) - Event schema reference
- [user-docs/reference/knowledge-note-template.md](../../user-docs/reference/knowledge-note-template.md) - Knowledge note template

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.7 (documents SAP-009)

**Dependent Capabilities**:
- [agent-awareness/](../agent-awareness/) - SAP-011 (AGENTS.md, CLAUDE.md in .chora/memory/)
- [metrics-tracking/](../metrics-tracking/) - SAP-013 (queries event log for metrics)
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates .chora/memory/ structure)

**Supporting Capabilities**:
- [automation-scripts/](../automation-scripts/) - SAP-008 (scripts can emit events)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (CI runs can emit events)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-009 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings (5 scenarios: checking memory first, duplicate notes, low-confidence solutions, event emission, note versioning), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide for memory-system SAP
