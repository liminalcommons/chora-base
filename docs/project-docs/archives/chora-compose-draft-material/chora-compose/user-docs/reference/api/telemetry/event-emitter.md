# EventEmitter API Reference

**Version:** v1.3.0
**Category:** Telemetry
**Status:** Stable
**Last Updated:** October 17, 2025

---

## Overview

The `EventEmitter` class provides **thread-safe event emission** to JSON Lines files, enabling gateway integration through request/response correlation and event-driven monitoring.

### Key Features

- **Thread-Safe File Writing**: Multiple generators can emit events concurrently
- **Trace Context Propagation**: Automatic correlation via `CHORA_TRACE_ID` environment variable
- **JSON Lines Format**: One event per line for streaming parsers
- **Automatic Directory Creation**: Creates `var/telemetry/` directory if needed
- **Global Emitter Pattern**: Singleton for convenient use across generators

---

## Quick Start

### Basic Usage

```python
from chora_compose.telemetry import emit_event, ContentGeneratedEvent

# Emit an event (uses global emitter)
emit_event(ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
))
```

### Custom Emitter

```python
from chora_compose.telemetry import EventEmitter, ContentGeneratedEvent

# Create custom emitter (e.g., for testing)
emitter = EventEmitter(events_file="tmp/test-events.jsonl")

event = ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
)

emitter.emit(event)
```

---

## API Reference

### EventEmitter Class

**Source:** `src/chora_compose/telemetry/event_emitter.py`

```python
class EventEmitter:
    """Thread-safe event emitter that writes to JSON Lines files."""

    def __init__(
        self,
        events_file: str | Path = "var/telemetry/events.jsonl"
    ) -> None:
        """Initialize the event emitter."""

    def emit(self, event: TelemetryEvent) -> None:
        """Emit an event to the events file (thread-safe)."""

    def read_events(
        self,
        trace_id: str | None = None
    ) -> list[dict[str, Any]]:
        """Read events from file (for testing/debugging)."""

    def clear(self) -> None:
        """Clear all events (for testing only)."""
```

---

### Constructor: `__init__`

**Signature:**
```python
def __init__(
    self,
    events_file: str | Path = "var/telemetry/events.jsonl"
) -> None
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `events_file` | `str \| Path` | `"var/telemetry/events.jsonl"` | Path to events file (absolute or relative to CWD) |

**Behavior:**
1. Creates `events_file.parent` directory if it doesn't exist
2. Initializes thread lock for concurrent writes
3. Does NOT create the events file yet (created on first `emit()`)

**Examples:**

```python
# Use default location (var/telemetry/events.jsonl)
emitter = EventEmitter()

# Custom location for testing
emitter = EventEmitter(events_file="tmp/test-events.jsonl")

# Absolute path
emitter = EventEmitter(events_file=Path("/var/log/chora/events.jsonl"))
```

---

### Method: `emit`

**Signature:**
```python
def emit(self, event: TelemetryEvent) -> None
```

**Purpose:** Emit an event to the events file with thread-safe file appending.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `event` | `TelemetryEvent` | Event instance (ContentGeneratedEvent, ArtifactAssembledEvent, etc.) |

**Behavior:**
1. If `event.trace_id` is `None`, reads `CHORA_TRACE_ID` environment variable
2. Serializes event to JSON using Pydantic's `model_dump_json()`
3. Acquires thread lock
4. Appends JSON string + newline to events file
5. Releases lock

**Thread Safety:** YES - Uses `threading.Lock` to prevent interleaved writes

**Performance:** ~1-5ms per event (file I/O overhead)

**Examples:**

```python
from chora_compose.telemetry import EventEmitter, ContentGeneratedEvent

emitter = EventEmitter()

# Basic event
event = ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
)
emitter.emit(event)

# Event with explicit trace_id
event = ContentGeneratedEvent(
    content_config_id="readme-body",
    generator_type="template_fill",
    status="success",
    duration_ms=120,
    trace_id="workflow-abc123"  # Explicit trace ID
)
emitter.emit(event)

# Error event
event = ContentGeneratedEvent(
    content_config_id="readme-footer",
    generator_type="jinja2",
    status="error",
    duration_ms=50,
    error_message="Template syntax error: unexpected end of template"
)
emitter.emit(event)
```

**Trace Context Propagation:**

```bash
# Gateway sets trace ID before calling chora-compose
export CHORA_TRACE_ID="workflow-abc123"

# Now all emitted events will have trace_id="workflow-abc123"
python -m chora_compose.mcp.server
```

```python
# Event emitted without explicit trace_id
event = ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
    # trace_id not set - will be populated from CHORA_TRACE_ID
)
emitter.emit(event)

# Resulting JSON includes trace_id from environment
# {"trace_id": "workflow-abc123", "content_config_id": "readme-intro", ...}
```

---

### Method: `read_events`

**Signature:**
```python
def read_events(
    self,
    trace_id: str | None = None
) -> list[dict[str, Any]]
```

**Purpose:** Read events from the events file (primarily for testing/debugging).

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trace_id` | `str \| None` | `None` | Filter events by trace ID (if provided) |

**Returns:** `list[dict[str, Any]]` - List of event dictionaries

**Behavior:**
1. Returns empty list if events file doesn't exist
2. Reads entire file line-by-line
3. Parses each line as JSON
4. Filters by `trace_id` if provided
5. Returns all matching events

**WARNING:** This method loads the entire file into memory. For production systems with large event files, use streaming parsers instead.

**Examples:**

```python
from chora_compose.telemetry import EventEmitter

emitter = EventEmitter()

# Read all events
all_events = emitter.read_events()
print(f"Total events: {len(all_events)}")

# Read events for specific trace
workflow_events = emitter.read_events(trace_id="workflow-abc123")
print(f"Events in workflow: {len(workflow_events)}")

# Analyze events
for event in workflow_events:
    print(f"{event['event_type']}: {event['status']} ({event['duration_ms']}ms)")
```

**Production Alternative (Streaming):**

```python
import json
from pathlib import Path

# Stream events without loading entire file
def stream_events(events_file: Path, trace_id: str):
    with open(events_file, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("trace_id") == trace_id:
                yield event

# Usage
for event in stream_events(Path("var/telemetry/events.jsonl"), "workflow-abc123"):
    process_event(event)
```

---

### Method: `clear`

**Signature:**
```python
def clear(self) -> None
```

**Purpose:** Delete the events file (for testing only).

**Returns:** `None`

**Behavior:**
1. If events file exists, deletes it
2. If file doesn't exist, does nothing (no error)
3. Does NOT recreate the file (created on next `emit()`)

**WARNING:** This is destructive and should ONLY be used in tests. Production systems should use log rotation or archival instead.

**Examples:**

```python
from chora_compose.telemetry import EventEmitter

emitter = EventEmitter(events_file="tmp/test-events.jsonl")

# Emit some test events
emitter.emit(event1)
emitter.emit(event2)

# Read and verify
events = emitter.read_events()
assert len(events) == 2

# Clean up after test
emitter.clear()

# Verify cleanup
events = emitter.read_events()
assert len(events) == 0
```

**Production Alternative (Log Rotation):**

```bash
# Use logrotate for production systems
# /etc/logrotate.d/chora-compose
/var/log/chora/events.jsonl {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 chora chora
}
```

---

## Global Emitter Pattern

### Function: `get_emitter`

**Signature:**
```python
def get_emitter() -> EventEmitter
```

**Purpose:** Get the global singleton EventEmitter instance.

**Returns:** `EventEmitter` - Global emitter (created on first call)

**Behavior:**
- First call: Creates `EventEmitter(events_file="var/telemetry/events.jsonl")`
- Subsequent calls: Returns existing instance
- Thread-safe singleton initialization

**Examples:**

```python
from chora_compose.telemetry.event_emitter import get_emitter

# Get global emitter
emitter = get_emitter()

# All calls return the same instance
assert get_emitter() is get_emitter()
```

---

### Function: `emit_event`

**Signature:**
```python
def emit_event(event: TelemetryEvent) -> None
```

**Purpose:** Convenience function to emit events using the global emitter.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `event` | `TelemetryEvent` | Event to emit |

**Behavior:**
1. Calls `get_emitter()` to get global instance
2. Calls `emitter.emit(event)`

**This is the recommended way to emit events from generators.**

**Examples:**

```python
from chora_compose.telemetry import emit_event, ContentGeneratedEvent

# Simple - no emitter management needed
emit_event(ContentGeneratedEvent(
    content_config_id="readme-intro",
    generator_type="jinja2",
    status="success",
    duration_ms=234
))
```

**Generator Integration:**

```python
from chora_compose.telemetry import emit_event, ContentGeneratedEvent
from chora_compose.generators.base import GeneratorStrategy
import time

class MyGenerator(GeneratorStrategy):
    def generate(self, config, context=None):
        start_time = time.time()
        status = "success"
        error_message = None

        try:
            # Generate content
            result = self._generate_content(config, context)
            return result
        except Exception as e:
            status = "error"
            error_message = str(e)
            raise
        finally:
            # Always emit event (success or error)
            duration_ms = int((time.time() - start_time) * 1000)
            emit_event(ContentGeneratedEvent(
                content_config_id=config.id,
                generator_type="my_generator",
                status=status,
                duration_ms=duration_ms,
                error_message=error_message
            ))
```

---

## File Format

### JSON Lines Format

Events are written in **JSON Lines** format (one JSON object per line):

```jsonl
{"timestamp": "2025-10-17T12:00:00.123Z", "trace_id": "workflow-abc123", "event_type": "chora.content_generated", "content_config_id": "readme-intro", "generator_type": "jinja2", "status": "success", "duration_ms": 234, "error_message": null}
{"timestamp": "2025-10-17T12:00:01.456Z", "trace_id": "workflow-abc123", "event_type": "chora.content_generated", "content_config_id": "readme-body", "generator_type": "template_fill", "status": "success", "duration_ms": 120, "error_message": null}
{"timestamp": "2025-10-17T12:00:02.789Z", "trace_id": "workflow-abc123", "event_type": "chora.artifact_assembled", "artifact_config_id": "readme-full", "section_count": 2, "output_path": "dist/README.md", "status": "success", "duration_ms": 45, "error_message": null}
```

**Benefits:**
- **Streaming-Friendly**: Can parse incrementally without loading entire file
- **Append-Safe**: New events added without parsing existing data
- **Tool Support**: `jq`, `grep`, and other Unix tools work well

**Parsing:**

```bash
# View all events
cat var/telemetry/events.jsonl | jq .

# Filter by trace_id
cat var/telemetry/events.jsonl | jq 'select(.trace_id == "workflow-abc123")'

# Count events by type
cat var/telemetry/events.jsonl | jq -r .event_type | sort | uniq -c
```

---

## Thread Safety

### Concurrent Event Emission

The EventEmitter is **fully thread-safe** for concurrent writes:

```python
import threading
from chora_compose.telemetry import emit_event, ContentGeneratedEvent

def worker(worker_id):
    for i in range(100):
        emit_event(ContentGeneratedEvent(
            content_config_id=f"worker-{worker_id}-item-{i}",
            generator_type="test_generator",
            status="success",
            duration_ms=50
        ))

# Spawn 10 workers emitting 100 events each
threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# All 1000 events written correctly (no corruption)
```

**Implementation:**
- Uses `threading.Lock` around file write
- Prevents interleaved writes from concurrent threads
- Safe for asyncio concurrent tasks (GIL protects lock)

---

## Environment Variables

### CHORA_TRACE_ID

**Purpose:** Propagate trace context from gateways to chora-compose

**Type:** `str` (arbitrary string, gateway-defined)

**Behavior:**
- If set: All events emitted with `trace_id = $CHORA_TRACE_ID`
- If not set: Events have `trace_id = null`
- Can be overridden by setting `event.trace_id` explicitly

**Examples:**

```bash
# Gateway sets trace ID before calling MCP server
export CHORA_TRACE_ID="req-12345-workflow-abc"
python -m chora_compose.mcp.server

# All events in this process have trace_id="req-12345-workflow-abc"
```

**Best Practices:**
- Use UUIDs or request IDs: `req-{uuid}` or `workflow-{timestamp}-{counter}`
- Include workflow context: `{gateway_id}-{workflow_id}-{request_id}`
- Keep under 200 characters for efficiency

---

## Testing

### Test Patterns

#### Pattern 1: Custom Emitter for Isolation

```python
import pytest
from chora_compose.telemetry import EventEmitter, ContentGeneratedEvent

def test_event_emission(tmp_path):
    # Use tmp_path for test isolation
    events_file = tmp_path / "test-events.jsonl"
    emitter = EventEmitter(events_file=str(events_file))

    # Emit test event
    emitter.emit(ContentGeneratedEvent(
        content_config_id="test-config",
        generator_type="test_generator",
        status="success",
        duration_ms=100
    ))

    # Verify
    events = emitter.read_events()
    assert len(events) == 1
    assert events[0]["status"] == "success"
```

#### Pattern 2: Clear Global Emitter

```python
import pytest
from chora_compose.telemetry import emit_event, ContentGeneratedEvent
from chora_compose.telemetry.event_emitter import get_emitter

@pytest.fixture(autouse=True)
def clear_events():
    """Clear global emitter before each test."""
    get_emitter().clear()
    yield
    get_emitter().clear()

def test_with_global_emitter():
    # Emit event
    emit_event(ContentGeneratedEvent(
        content_config_id="test-config",
        generator_type="test_generator",
        status="success",
        duration_ms=100
    ))

    # Verify
    events = get_emitter().read_events()
    assert len(events) == 1
```

#### Pattern 3: Trace ID Filtering

```python
import os
from chora_compose.telemetry import emit_event, ContentGeneratedEvent
from chora_compose.telemetry.event_emitter import get_emitter

def test_trace_context(monkeypatch):
    get_emitter().clear()

    # Set trace ID via environment
    monkeypatch.setenv("CHORA_TRACE_ID", "test-trace-123")

    # Emit events
    emit_event(ContentGeneratedEvent(
        content_config_id="config-1",
        generator_type="jinja2",
        status="success",
        duration_ms=100
    ))

    # Verify trace context propagation
    events = get_emitter().read_events()
    assert events[0]["trace_id"] == "test-trace-123"
```

---

## Performance

### Benchmarks

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| `emit(event)` | 1-5ms | Includes file I/O |
| `emit(event)` (concurrent) | 1-10ms | With lock contention |
| `read_events()` (1000 events) | 50-100ms | Loads entire file |
| `clear()` | <1ms | File deletion |

### Optimization Tips

1. **Batch Writes (Advanced)**: For high-throughput scenarios, buffer events and flush periodically
2. **Separate File Per Workflow**: Use `events_file=f"var/telemetry/{trace_id}.jsonl"` to avoid lock contention
3. **Use Streaming Parsers**: Don't use `read_events()` for large files in production

---

## Error Handling

### Possible Errors

**Permission Denied:**
```python
# Directory not writable
emitter = EventEmitter(events_file="/root/events.jsonl")
# Raises PermissionError during emit()
```

**Disk Full:**
```python
# Disk space exhausted
emitter.emit(event)
# Raises OSError: [Errno 28] No space left on device
```

**Invalid Event:**
```python
# Pydantic validation error
event = ContentGeneratedEvent(
    content_config_id="test",
    generator_type=123,  # Invalid type (should be str)
    status="success",
    duration_ms=100
)
# Raises ValidationError before emit()
```

### Best Practices

```python
import logging
from chora_compose.telemetry import emit_event, ContentGeneratedEvent

logger = logging.getLogger(__name__)

def safe_emit(event):
    """Emit event with error handling."""
    try:
        emit_event(event)
    except Exception as e:
        # Log but don't crash generator
        logger.error(f"Failed to emit event: {e}")
```

---

## Related Documentation

- [Event Schemas Reference](event-schemas.md) - All event types and fields
- [UpstreamDependencies Model](../models/upstream-dependencies.md) - Generator dependencies
- [Capabilities Resource](../resources/capabilities.md) - MCP discovery
- [Gateway Integration Guide](../../../how-to/mcp/use-with-gateway.md) - End-to-end workflow

---

**Version:** v1.3.0
**Last Updated:** October 17, 2025
**Maintainer:** Chora Compose Team
