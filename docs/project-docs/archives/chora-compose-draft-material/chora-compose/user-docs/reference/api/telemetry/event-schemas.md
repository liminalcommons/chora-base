# Telemetry Event Schemas

**Version:** v1.3.0
**Category:** Telemetry
**Status:** Stable
**Last Updated:** October 17, 2025

---

## Overview

Chora Compose emits structured telemetry events in JSON Lines format to enable gateway integration, request/response correlation, and observability across distributed workflows.

### Key Features

- **Trace Context Propagation**: `CHORA_TRACE_ID` environment variable flows through all events
- **JSON Lines Format**: One event per line for efficient streaming and parsing
- **Thread-Safe**: Concurrent event emission from multiple generators
- **Automatic Timestamps**: ISO 8601 format with timezone
- **Success/Error Tracking**: All events include status and optional error_message

### Event File Location

**Default**: `var/telemetry/events.jsonl`

**Format**: JSON Lines (`.jsonl`)
- One JSON object per line
- No commas between lines
- Easy to stream and parse incrementally

---

## Base Event Schema

All events inherit from `TelemetryEvent` base model.

### Common Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | `string` | Yes | ISO 8601 timestamp (UTC) |
| `trace_id` | `string \| null` | Yes | Trace ID for correlation (from `CHORA_TRACE_ID` env var) |
| `event_type` | `string` | Yes | Event type identifier (e.g., "chora.content_generated") |
| `status` | `"success" \| "error"` | Yes | Event outcome |

### Example

```json
{
  "timestamp": "2025-10-17T12:00:00.123456Z",
  "trace_id": "abc123-def456",
  "event_type": "chora.content_generated",
  "status": "success"
}
```

---

## Event Types

### 1. ContentGeneratedEvent

**Event Type**: `chora.content_generated`

**Emitted By**: All 5 generators (demonstration, jinja2, template_fill, bdd_scenario, code_generation)

**When**: After content generation completes (success or error)

**Purpose**: Track content generation performance, errors, and trace workflows

#### Schema

```python
class ContentGeneratedEvent(TelemetryEvent):
    event_type: Literal["chora.content_generated"] = "chora.content_generated"
    content_config_id: str
    generator_type: str
    duration_ms: int  # >= 0
    error_message: str | None = None
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_config_id` | `string` | Yes | ID of the content config that was generated |
| `generator_type` | `string` | Yes | Generator used (jinja2, demonstration, code_generation, etc.) |
| `duration_ms` | `integer` | Yes | Generation duration in milliseconds (≥ 0) |
| `error_message` | `string \| null` | No | Error message if status is "error" |

#### Examples

**Success Event:**
```json
{
  "timestamp": "2025-10-17T12:00:00.123Z",
  "trace_id": "workflow-abc123",
  "event_type": "chora.content_generated",
  "status": "success",
  "content_config_id": "readme-intro",
  "generator_type": "jinja2",
  "duration_ms": 234,
  "error_message": null
}
```

**Error Event:**
```json
{
  "timestamp": "2025-10-17T12:00:05.456Z",
  "trace_id": "workflow-abc123",
  "event_type": "chora.content_generated",
  "status": "error",
  "content_config_id": "api-docs",
  "generator_type": "code_generation",
  "duration_ms": 1520,
  "error_message": "Missing ANTHROPIC_API_KEY environment variable"
}
```

---

### 2. ArtifactAssembledEvent

**Event Type**: `chora.artifact_assembled`

**Emitted By**: ArtifactComposer

**When**: After artifact assembly completes (success or error)

**Purpose**: Track artifact assembly performance, section count, output paths

#### Schema

```python
class ArtifactAssembledEvent(TelemetryEvent):
    event_type: Literal["chora.artifact_assembled"] = "chora.artifact_assembled"
    artifact_config_id: str
    section_count: int  # >= 0
    duration_ms: int  # >= 0
    output_path: str | None = None
    error_message: str | None = None
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `artifact_config_id` | `string` | Yes | ID of the artifact config that was assembled |
| `section_count` | `integer` | Yes | Number of content sections assembled (≥ 0) |
| `duration_ms` | `integer` | Yes | Assembly duration in milliseconds (≥ 0) |
| `output_path` | `string \| null` | No | Path where artifact was written |
| `error_message` | `string \| null` | No | Error message if status is "error" |

#### Examples

**Success Event:**
```json
{
  "timestamp": "2025-10-17T12:00:10.789Z",
  "trace_id": "workflow-abc123",
  "event_type": "chora.artifact_assembled",
  "status": "success",
  "artifact_config_id": "weekly-report",
  "section_count": 4,
  "duration_ms": 1234,
  "output_path": "output/weekly-report.md",
  "error_message": null
}
```

**Error Event:**
```json
{
  "timestamp": "2025-10-17T12:00:15.123Z",
  "trace_id": "workflow-abc123",
  "event_type": "chora.artifact_assembled",
  "status": "error",
  "artifact_config_id": "complex-report",
  "section_count": 2,
  "duration_ms": 876,
  "output_path": null,
  "error_message": "Failed to generate required content 'summary': Template not found"
}
```

---

### 3. ValidationCompletedEvent

**Event Type**: `chora.validation_completed`

**Emitted By**: Validation framework (future implementation)

**When**: After content validation completes

**Purpose**: Track validation rule execution and results

**Status**: **STUB** - Event schema defined but not yet emitted in v1.3.0

#### Schema

```python
class ValidationCompletedEvent(TelemetryEvent):
    event_type: Literal["chora.validation_completed"] = "chora.validation_completed"
    content_config_id: str
    validation_passed: bool
    rule_count: int  # >= 0
    duration_ms: int  # >= 0
    error_message: str | None = None
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_config_id` | `string` | Yes | ID of the content config that was validated |
| `validation_passed` | `boolean` | Yes | Whether all validation rules passed |
| `rule_count` | `integer` | Yes | Number of validation rules executed (≥ 0) |
| `duration_ms` | `integer` | Yes | Validation duration in milliseconds (≥ 0) |
| `error_message` | `string \| null` | No | Error message if status is "error" |

#### Example (Future)

```json
{
  "timestamp": "2025-10-17T12:00:20.456Z",
  "trace_id": "workflow-abc123",
  "event_type": "chora.validation_completed",
  "status": "success",
  "content_config_id": "api-docs",
  "validation_passed": true,
  "rule_count": 5,
  "duration_ms": 123,
  "error_message": null
}
```

---

## Trace Context Propagation

### Environment Variable

**Name**: `CHORA_TRACE_ID`

**Purpose**: Enable request/response correlation across distributed systems

**Set By**: Gateway or orchestration layer

**Read By**: All generators and ArtifactComposer

### Example Workflow

```bash
# Gateway sets trace ID
export CHORA_TRACE_ID="gateway-request-abc123"

# Generate content (emits event with trace_id)
chora generate readme-intro

# Assemble artifact (emits event with same trace_id)
chora assemble weekly-report

# All events share trace_id for correlation
```

### Event Correlation

**Read events by trace_id:**
```python
import json

def read_events_by_trace_id(trace_id: str, events_file: str = "var/telemetry/events.jsonl"):
    events = []
    with open(events_file) as f:
        for line in f:
            event = json.loads(line)
            if event.get("trace_id") == trace_id:
                events.append(event)
    return events

# Get all events for workflow
workflow_events = read_events_by_trace_id("gateway-request-abc123")
for event in workflow_events:
    print(f"{event['event_type']}: {event['status']} ({event['duration_ms']}ms)")
```

---

## JSON Lines Format

### File Structure

```jsonl
{"timestamp": "2025-10-17T12:00:00.123Z", "trace_id": "trace-1", "event_type": "chora.content_generated", "status": "success", "content_config_id": "intro", "generator_type": "jinja2", "duration_ms": 100}
{"timestamp": "2025-10-17T12:00:01.234Z", "trace_id": "trace-1", "event_type": "chora.content_generated", "status": "success", "content_config_id": "body", "generator_type": "jinja2", "duration_ms": 150}
{"timestamp": "2025-10-17T12:00:02.345Z", "trace_id": "trace-1", "event_type": "chora.artifact_assembled", "status": "success", "artifact_config_id": "report", "section_count": 2, "duration_ms": 50, "output_path": "output/report.md"}
```

### Benefits

- **Streaming**: Parse line-by-line without loading entire file
- **Append-Only**: Thread-safe appending with file locks
- **No Commas**: Each line is valid JSON independently
- **Tools**: Standard tools like `jq`, `grep`, `tail -f` work well

### Parsing Examples

**Shell (jq):**
```bash
# Get all error events
cat var/telemetry/events.jsonl | jq 'select(.status == "error")'

# Get events by trace_id
cat var/telemetry/events.jsonl | jq 'select(.trace_id == "trace-123")'

# Calculate average duration
cat var/telemetry/events.jsonl | jq '.duration_ms' | awk '{sum+=$1; n++} END {print sum/n}'
```

**Python:**
```python
import json

def parse_events(events_file: str):
    with open(events_file) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

# Process events
for event in parse_events("var/telemetry/events.jsonl"):
    if event["status"] == "error":
        print(f"Error: {event['error_message']}")
```

---

## Event Lifecycle

### 1. Event Creation

```python
from chora_compose.telemetry import ContentGeneratedEvent

event = ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
)
# trace_id automatically read from CHORA_TRACE_ID env var
# timestamp automatically generated (ISO 8601)
```

### 2. Event Emission

```python
from chora_compose.telemetry import emit_event

emit_event(event)
# Written to var/telemetry/events.jsonl
# Thread-safe appending with file lock
```

### 3. Event Reading

```python
from chora_compose.telemetry.event_emitter import EventEmitter

emitter = EventEmitter()
events = emitter.read_events(trace_id="trace-123")
# Returns list of event dictionaries filtered by trace_id
```

---

## Performance Considerations

### Thread Safety

- EventEmitter uses threading.Lock for file writes
- Safe to call emit_event() from multiple threads
- No event loss or corruption under concurrent load

### File Size Management

- JSON Lines format grows indefinitely
- Implement log rotation for production:
  ```bash
  # Rotate when > 100MB
  if [ $(stat -f%z var/telemetry/events.jsonl) -gt 104857600 ]; then
      mv var/telemetry/events.jsonl var/telemetry/events-$(date +%Y%m%d).jsonl
      gzip var/telemetry/events-$(date +%Y%m%d).jsonl
  fi
  ```

### Streaming Parsing

```python
# Don't load entire file
# BAD: events = json.loads(f.read())

# GOOD: Stream line by line
for line in f:
    event = json.loads(line)
    process(event)
```

---

## Migration & Compatibility

### v1.3.0 Initial Release

- All 3 event types defined
- ContentGeneratedEvent and ArtifactAssembledEvent actively emitted
- ValidationCompletedEvent schema defined (stub, not emitted)

### Future Additions (Planned)

- v1.2.x: Additional event types (workflow_started, workflow_completed)
- v1.3.x: Structured metadata fields (user_id, session_id)
- v2.0.x: Breaking changes (if needed)

### Backward Compatibility

- Additive-only changes (new fields, new event types)
- Parsers should ignore unknown event_type values
- Parsers should ignore unknown fields

```python
# Robust parsing
event = json.loads(line)
event_type = event.get("event_type")

if event_type == "chora.content_generated":
    process_content_event(event)
elif event_type == "chora.artifact_assembled":
    process_artifact_event(event)
else:
    # Unknown event type - ignore gracefully
    pass
```

---

## Related Documentation

- [EventEmitter API](event-emitter.md) - Event emission implementation
- [Event Schema Specification](../../../specs/event-schema.md) - Detailed specification
- [Gateway Integration Guide](../../../how-to/mcp/use-with-gateway.md) - Using events in gateways
- [Trace Context Guide](../../../how-to/telemetry/trace-workflows.md) - Trace ID propagation patterns

---

**Version:** v1.3.0
**Last Updated:** October 17, 2025
**Maintainer:** Chora Compose Team
