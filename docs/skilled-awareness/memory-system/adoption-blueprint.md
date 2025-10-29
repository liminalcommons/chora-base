---
sap_id: SAP-010
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: how-to
audience: developers, ai-agents
---

# Adoption Blueprint: Memory System (A-MEM)

**SAP ID**: SAP-010
**For**: Projects adopting Agentic Memory (A-MEM)
**Purpose**: Step-by-step guide to implement cross-session memory

---

## 1. Overview

This blueprint helps projects adopt the **A-MEM architecture** with event logs, knowledge graphs, and agent profiles for cross-session learning.

**Adoption Benefits**:
- 30% reduction in repeated mistakes (agents learn from past errors)
- Cross-session context preservation
- Multi-step workflow traceability
- Agent preference persistence

**Prerequisites**: chora-base generated project (includes `.chora/memory/` structure)

---

## 2. Quick Start (15 Minutes)

### Step 1: Verify Memory Structure Exists

```bash
ls -la .chora/memory/
# Expected:
# README.md, AGENTS.md, CLAUDE.md
# events/ (empty initially)
# knowledge/ (empty initially)
# profiles/ (empty initially)
# queries/ (optional)
```

### Step 2: Initialize Event Log

```bash
# Create monthly partition
mkdir -p .chora/memory/events/$(date +%Y-%m)/traces

# Create empty events file
touch .chora/memory/events/$(date +%Y-%m)/events.jsonl
```

### Step 3: Emit Your First Event

```python
import json
from datetime import datetime

event = {
    "timestamp": datetime.now().isoformat(),
    "trace_id": "test123",
    "status": "success",
    "schema_version": "1.0",
    "event_type": "agent.session_started",
    "source": "my-project",
    "metadata": {"agent": "test"}
}

with open(".chora/memory/events/2025-10/events.jsonl", "a") as f:
    f.write(json.dumps(event) + "\n")
```

### Step 4: Create Your First Knowledge Note

```bash
mkdir -p .chora/memory/knowledge/notes

cat > .chora/memory/knowledge/notes/first-learning.md << 'EOF'
---
id: first-learning
created: 2025-10-28T12:00:00Z
updated: 2025-10-28T12:00:00Z
tags: [test, learning]
confidence: high
source: agent-learning
status: validated
author: claude-code
---

# First Learning

## Problem
Testing A-MEM memory system

## Solution
Successfully created first knowledge note

## Evidence
This note exists!
EOF
```

### Step 5: Initialize Agent Profile

```bash
mkdir -p .chora/memory/profiles

cat > .chora/memory/profiles/claude-code.json << 'EOF'
{
  "agent_name": "claude-code",
  "agent_version": "sonnet-4.5",
  "last_active": "2025-10-28T12:00:00Z",
  "session_count": 1,
  "capabilities": {},
  "preferences": {},
  "context_switches": {"total": 0}
}
EOF
```

**Done!** You now have a working A-MEM system.

---

## 3. Adoption Levels

### Level 1: Basic Event Logging (Week 1)
- Emit events for key operations
- Query events for debugging
- Understand trace correlation

**Time**: 2 hours
**Goal**: Basic operation history

---

### Level 2: Knowledge Accumulation (Week 2-3)
- Create knowledge notes for learnings
- Link related notes
- Search by tags

**Time**: 4 hours over 2 weeks
**Goal**: Growing knowledge base

---

### Level 3: Full Cross-Session Learning (Month 1)
- Agent profiles with preferences
- Automated learning from failures
- Confidence-based decision making

**Time**: 8 hours over 1 month
**Goal**: Agents that improve over time

---

## 4. Level 1: Basic Event Logging

### 4.1 Implement Event Emission

**Create helper function**:

```python
# Add to your project (e.g., src/utils/memory.py)
import json
import os
from datetime import datetime
from pathlib import Path

def emit_event(event_type, trace_id, status="success", metadata=None):
    """Emit event to A-MEM event log."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "trace_id": trace_id,
        "status": status,
        "schema_version": "1.0",
        "event_type": event_type,
        "source": os.getenv("PROJECT_NAME", "unknown"),
        "metadata": metadata or {}
    }

    # Get monthly partition
    month = datetime.now().strftime("%Y-%m")
    events_dir = Path(".chora/memory/events") / month
    events_dir.mkdir(parents=True, exist_ok=True)

    # Append to monthly events file
    events_file = events_dir / "events.jsonl"
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    # Also write to per-trace file (for fast trace queries)
    traces_dir = events_dir / "traces"
    traces_dir.mkdir(exist_ok=True)
    trace_file = traces_dir / f"{trace_id}.jsonl"
    with open(trace_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event
```

---

### 4.2 Instrument Your Code

**Add event emission to key operations**:

```python
import uuid
from utils.memory import emit_event

def my_operation():
    """Example operation with event logging."""
    # Generate trace ID for this operation
    trace_id = str(uuid.uuid4())[:8]

    # Emit start event
    emit_event("operation.started", trace_id, metadata={"operation": "my_operation"})

    try:
        # ... do work ...
        result = perform_work()

        # Emit success event
        emit_event("operation.completed", trace_id, status="success", metadata={"result": result})
        return result

    except Exception as e:
        # Emit failure event
        emit_event("operation.failed", trace_id, status="failure", metadata={"error": str(e)})
        raise
```

---

### 4.3 Query Events for Debugging

**Query recent failures**:

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

def get_recent_failures(days=7):
    """Get all failure events in last N days."""
    failures = []
    since = datetime.now() - timedelta(days=days)

    events_dir = Path(".chora/memory/events")
    for month_dir in sorted(events_dir.glob("*"), reverse=True):
        if not month_dir.is_dir():
            continue

        events_file = month_dir / "events.jsonl"
        if not events_file.exists():
            continue

        with open(events_file) as f:
            for line in f:
                event = json.loads(line)
                event_time = datetime.fromisoformat(event["timestamp"])

                if event_time >= since and event["status"] == "failure":
                    failures.append(event)

    return failures

# Usage
failures = get_recent_failures(days=7)
print(f"Found {len(failures)} failures in last 7 days")
for f in failures[:5]:  # Show first 5
    print(f"  {f['timestamp']}: {f['event_type']} - {f['metadata'].get('error')}")
```

---

## 5. Level 2: Knowledge Accumulation

### 5.1 Create Knowledge Notes

**When to create**:
- Solved non-trivial problem (> 15 min)
- Pattern likely to recur
- Solution non-obvious

**Template**:

```markdown
---
id: descriptive-id
created: 2025-10-28T12:00:00Z
updated: 2025-10-28T12:00:00Z
tags: [category, subcategory]
confidence: medium
source: agent-learning
status: validated
author: claude-code
related_traces: [trace-id]
---

# Title

## Problem
[Clear problem description]

## Solution
[Solution with code examples]

```python
# Example code
```

## Evidence
- Trace {trace-id}: Success
- Tested on {date}

## Learned Pattern
1. Step 1
2. Step 2
3. Step 3
```

---

### 5.2 Implement Tag Index

**Create tag index script**:

```python
# scripts/update_knowledge_tags.py
import json
from pathlib import Path
import yaml

def update_tag_index():
    """Update tag index from all knowledge notes."""
    notes_dir = Path(".chora/memory/knowledge/notes")
    tags_index = {"tags": {}}

    for note_file in notes_dir.glob("*.md"):
        with open(note_file) as f:
            content = f.read()

        # Extract frontmatter
        if content.startswith("---\n"):
            _, frontmatter, _ = content.split("---\n", 2)
            metadata = yaml.safe_load(frontmatter)

            note_id = metadata["id"]
            tags = metadata.get("tags", [])

            # Add note to each tag
            for tag in tags:
                if tag not in tags_index["tags"]:
                    tags_index["tags"][tag] = {"note_count": 0, "notes": []}

                tags_index["tags"][tag]["notes"].append(note_id)
                tags_index["tags"][tag]["note_count"] += 1

    # Save tag index
    tags_file = Path(".chora/memory/knowledge/tags.json")
    with open(tags_file, "w") as f:
        json.dump(tags_index, f, indent=2)

    print(f"Updated tag index: {len(tags_index['tags'])} tags")

if __name__ == "__main__":
    update_tag_index()
```

**Run after creating/updating notes**:
```bash
python scripts/update_knowledge_tags.py
```

---

### 5.3 Search Knowledge by Tag

```python
import json
from pathlib import Path

def search_notes_by_tag(tag):
    """Find notes with given tag."""
    tags_file = Path(".chora/memory/knowledge/tags.json")
    with open(tags_file) as f:
        tags_index = json.load(f)

    return tags_index["tags"].get(tag, {}).get("notes", [])

# Usage
notes = search_notes_by_tag("troubleshooting")
print(f"Found {len(notes)} notes with tag 'troubleshooting'")
```

---

## 6. Level 3: Full Cross-Session Learning

### 6.1 Implement Agent Profile Management

**Create profile manager**:

```python
# src/utils/agent_profile.py
import json
from pathlib import Path
from datetime import datetime

class AgentProfile:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.profile_file = Path(f".chora/memory/profiles/{agent_name}.json")
        self.profile = self._load_or_create()

    def _load_or_create(self):
        """Load existing profile or create new one."""
        if self.profile_file.exists():
            with open(self.profile_file) as f:
                return json.load(f)
        else:
            return {
                "agent_name": self.agent_name,
                "agent_version": "unknown",
                "last_active": datetime.now().isoformat(),
                "session_count": 0,
                "capabilities": {},
                "preferences": {},
                "context_switches": {"total": 0}
            }

    def save(self):
        """Save profile to disk."""
        self.profile["last_active"] = datetime.now().isoformat()
        self.profile_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.profile_file, "w") as f:
            json.dump(self.profile, f, indent=2)

    def get_preference(self, key, default=None):
        """Get user preference."""
        return self.profile["preferences"].get(key, default)

    def set_preference(self, key, value):
        """Set user preference."""
        self.profile["preferences"][key] = value
        self.save()

    def increment_session(self):
        """Increment session count."""
        self.profile["session_count"] += 1
        self.save()

    def record_operation(self, capability, success=True):
        """Record operation for capability tracking."""
        if capability not in self.profile["capabilities"]:
            self.profile["capabilities"][capability] = {
                "skill_level": "novice",
                "successful_operations": 0,
                "failed_operations": 0,
                "learned_patterns": [],
                "common_mistakes": []
            }

        if success:
            self.profile["capabilities"][capability]["successful_operations"] += 1
        else:
            self.profile["capabilities"][capability]["failed_operations"] += 1

        # Update skill level
        count = self.profile["capabilities"][capability]["successful_operations"]
        if count > 100:
            self.profile["capabilities"][capability]["skill_level"] = "expert"
        elif count > 50:
            self.profile["capabilities"][capability]["skill_level"] = "advanced"
        elif count > 10:
            self.profile["capabilities"][capability]["skill_level"] = "intermediate"

        self.save()
```

---

### 6.2 Use Agent Profile in Code

```python
from utils.agent_profile import AgentProfile

# At session start
profile = AgentProfile("claude-code")
profile.increment_session()

# Load saved preferences
verbose = profile.get_preference("verbose_logging", False)
timeout = profile.get_preference("backend_timeout", 30)

# Use preferences
if verbose:
    print("Verbose logging enabled (from profile)")
set_backend_timeout(timeout)

# After operation
profile.record_operation("backend_management", success=True)

# Save new preference
profile.set_preference("backend_timeout", 60)
```

---

### 6.3 Automated Learning from Failures

**Implement learning loop**:

```python
def handle_failure_with_learning(operation, error, trace_id):
    """Handle failure and create knowledge note if new pattern."""
    # 1. Check if this error pattern exists in knowledge
    error_type = type(error).__name__
    notes = search_notes_by_tag(error_type.lower())

    if notes:
        # Known error, apply learned solution
        print(f"Known error pattern: {error_type}")
        note_id = notes[0]
        note = load_knowledge_note(note_id)
        print(f"Applying solution from: {note_id}")
        # Apply solution...
    else:
        # New error pattern, create knowledge note
        print(f"New error pattern: {error_type}, creating knowledge note")
        create_knowledge_note(
            id=f"{error_type.lower()}-fix",
            content=f"# {error_type} Fix\n\n## Problem\n{str(error)}\n\n## Solution\n[To be determined]\n",
            tags=["errors", error_type.lower(), operation],
            confidence="low",  # Start with low, upgrade as validated
            related_traces=[trace_id]
        )
```

---

## 7. Maintenance

### 7.1 Monthly: Compress Old Events

```bash
# Add to cron or run manually
# Compress events older than 1 month
find .chora/memory/events -name "events.jsonl" -mtime +30 -exec gzip {} \;
```

### 7.2 Quarterly: Archive Events

```bash
# Move events > 6 months to archive
find .chora/memory/events -name "*.jsonl.gz" -mtime +180 -exec mv {} /archive/ \;
```

### 7.3 As Needed: Update Knowledge Tags

```bash
# Run after creating/updating knowledge notes
python scripts/update_knowledge_tags.py
```

---

## 8. Success Metrics

### Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Event log populated** | > 0 events | Count events in `.chora/memory/events/` |
| **Knowledge notes created** | > 10 notes | Count files in `.chora/memory/knowledge/notes/` |
| **Agent profiles exist** | > 0 profiles | Count files in `.chora/memory/profiles/` |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Event schema compliance** | 100% | Validate all events against schema |
| **Knowledge note quality** | ≥80% high confidence | Count notes with `confidence: high` |
| **Tag consistency** | ≥90% | Check tag normalization (lowercase, hyphenated) |

### Efficiency Metrics

| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| **Repeated mistakes** | Varies | 30% reduction | Count duplicate error patterns |
| **Knowledge reuse** | 0 | ≥3 queries/session | Track knowledge note queries |
| **Preference persistence** | 0% | 100% | Check if preferences load at session start |

---

## 9. Troubleshooting

### Problem 1: Events File Growing Too Large

**Symptom**: `.chora/memory/events/2025-10/events.jsonl` is > 100MB

**Solution**:
```bash
# Compress immediately
gzip .chora/memory/events/2025-10/events.jsonl

# Future queries will need to decompress first
zcat .chora/memory/events/2025-10/events.jsonl.gz | grep "pattern"
```

---

### Problem 2: Duplicate Knowledge Notes

**Symptom**: Multiple notes for same issue

**Solution**:
```bash
# Search before creating
python -c "from utils.memory import search_notes_by_tag; print(search_notes_by_tag('issue-tag'))"

# If duplicates exist, merge manually
# Keep most comprehensive note, add links from others
```

---

### Problem 3: Agent Profile Schema Changed

**Symptom**: Profile has old schema, missing new fields

**Solution**:
```python
# Write migration script
def migrate_profile_v1_to_v2(profile):
    """Migrate profile from v1 to v2 schema."""
    if "schema_version" in profile and profile["schema_version"] == "2.0":
        return profile  # Already migrated

    # Add new fields with defaults
    profile["schema_version"] = "2.0"
    profile.setdefault("context_switches", {"total": 0})
    # ... map other fields

    return profile
```

---

## 10. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Memory System capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover A-MEM event logging and knowledge accumulation
- Quick reference for memory operations
- Links to memory system documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Memory System (A-MEM)

Cross-session memory with event logs, knowledge graphs, and agent profiles.

**Documentation**: [docs/skilled-awareness/memory-system/](docs/skilled-awareness/memory-system/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/memory-system/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/memory-system/awareness-guide.md)

**Key Features**:
- Event logs: .chora/memory/events/ (JSONL format)
- Knowledge notes: .chora/memory/knowledge/notes/
- Agent profiles: .chora/memory/profiles/
```

**Validation**:
```bash
grep "Memory System" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 11. Related Documents

**Memory Infrastructure**:
- [.chora/memory/README.md](/static-template/.chora/memory/README.md) - A-MEM architecture
- [protocol-spec.md](protocol-spec.md) - Memory system contracts

**Related SAPs**:
- [SAP-009: agent-awareness](../agent-awareness/) - Awareness files
- [SAP-013: metrics-tracking](../metrics-tracking/) - Event log queries

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for memory-system SAP
