# A-MEM: Agent Memory System

This directory implements the A-MEM (Agent Memory) pattern from SAP-010, providing structured memory for AI agents working with chora-base.

## Directory Structure

```
.chora/memory/
├── events/          # Event logs (JSONL format)
├── knowledge/       # Knowledge notes (Markdown)
├── profiles/        # Agent profiles (JSON)
│   └── agents/      # Individual agent profiles
└── traces/          # Trace correlation (JSONL per trace)
```

## Memory Types

### 1. Event Logs (`events/`)

Record significant actions and state changes. Format: JSONL (one event per line).

**Schema**:
```json
{
  "event_id": "evt-001",
  "timestamp": "2025-11-04T12:00:00Z",
  "actor": "claude-code",
  "action": "sap_evaluation",
  "outcome": "success",
  "duration_minutes": 45,
  "metadata": {
    "saps_evaluated": 29,
    "issues_found": 3
  },
  "trace_id": "trace-2025-11-04-sap-maturity"
}
```

**Example**: [events/2025-11-chora-base.jsonl](events/2025-11-chora-base.jsonl)

### 2. Knowledge Notes (`knowledge/`)

Durable insights, patterns, and learnings. Format: Markdown with YAML frontmatter.

**Schema**:
```yaml
---
note_id: know-001
created: 2025-11-04
updated: 2025-11-04
author: claude-code
tags: [sap, maturity, evaluation]
confidence: high
related_events: [evt-001, evt-002]
---

# Title

Content...
```

**Example**: [knowledge/sap-maturity-findings.md](knowledge/sap-maturity-findings.md)

### 3. Agent Profiles (`profiles/agents/`)

Agent capabilities, preferences, and performance history. Format: JSON.

**Schema**:
```json
{
  "agent_id": "claude-code",
  "version": "sonnet-4.5",
  "capabilities": ["code_generation", "analysis", "documentation"],
  "preferences": {
    "context_budget": 10000,
    "progressive_loading": true
  },
  "performance": {
    "sessions": 10,
    "success_rate": 0.95
  }
}
```

**Example**: [profiles/agents/claude-code.json](profiles/agents/claude-code.json)

### 4. Trace Correlation (`traces/`)

Link related events across sessions. Format: JSONL per trace.

**Schema**:
```json
{
  "trace_id": "trace-2025-11-04-sap-maturity",
  "start_time": "2025-11-04T10:00:00Z",
  "end_time": "2025-11-04T14:00:00Z",
  "events": ["evt-001", "evt-002", "evt-003"],
  "outcome": "success",
  "summary": "SAP maturity assessment complete"
}
```

**Example**: [traces/trace-2025-11-04-sap-maturity.jsonl](traces/trace-2025-11-04-sap-maturity.jsonl)

## Usage

### Recording Events

```python
import json
from datetime import datetime
from pathlib import Path

event = {
    "event_id": "evt-001",
    "timestamp": datetime.now().isoformat(),
    "actor": "claude-code",
    "action": "sap_evaluation",
    "outcome": "success",
    "metadata": {"saps_evaluated": 29}
}

events_file = Path(".chora/memory/events/2025-11-chora-base.jsonl")
with events_file.open("a") as f:
    f.write(json.dumps(event) + "\n")
```

### Creating Knowledge Notes

```bash
cat > .chora/memory/knowledge/sap-maturity-findings.md <<'EOF'
---
note_id: know-001
created: 2025-11-04
tags: [sap, maturity]
---

# SAP Maturity Findings

Only 2/29 SAPs at true L3 maturity...
EOF
```

### Updating Agent Profile

```python
import json
from pathlib import Path

profile = {
    "agent_id": "claude-code",
    "capabilities": ["code_generation", "analysis"],
    "performance": {"sessions": 10, "success_rate": 0.95}
}

profile_file = Path(".chora/memory/profiles/agents/claude-code.json")
with profile_file.open("w") as f:
    json.dump(profile, f, indent=2)
```

## Documentation

For complete A-MEM specification, see:
- [SAP-010 Protocol Spec](../../docs/skilled-awareness/memory-system/protocol-spec.md)
- [SAP-010 Awareness Guide](../../docs/skilled-awareness/memory-system/awareness-guide.md)
- [SAP-010 Adoption Blueprint](../../docs/skilled-awareness/memory-system/adoption-blueprint.md)

## Privacy

- **events/**: Public (project history)
- **knowledge/**: Public (insights and patterns)
- **profiles/**: May contain sensitive data - see [.gitignore](.gitignore)
- **traces/**: May contain sensitive data - see [.gitignore](.gitignore)

Adjust `.gitignore` based on your project's privacy requirements.
