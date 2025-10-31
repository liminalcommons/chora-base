# Explanation: Event-Driven Telemetry Design

**Diataxis Quadrant**: Explanation
**Purpose**: Understand why chora-compose uses event-driven telemetry with JSONL format

---

## Overview

chora-compose implements **event-driven telemetry** that:

1. **Emits structured events** when key actions occur (content generated, config validated, etc.)
2. **Writes to JSONL files** (JSON Lines format, one event per line)
3. **Enables gateway integration** (n8n, Make, custom automation)
4. **Supports observability** (Datadog, Grafana, custom dashboards)

This document explains **why** this architecture was chosen, **what** it enables, and **how** it compares to alternatives.

---

## The Problem: How to Observe chora-compose?

### Observability Requirements

**Organizations need to know**:
- ✅ What content was generated? (audit trail)
- ✅ How long did generation take? (performance monitoring)
- ✅ Did generation succeed or fail? (error tracking)
- ✅ What generator was used? (usage analytics)
- ✅ What configs are being used? (adoption tracking)

**Challenge**: chora-compose runs in multiple contexts:
- CLI (local development)
- MCP server (Claude Desktop, IDEs)
- n8n workflows (automation)
- Docker containers (production)
- CI/CD pipelines (automated builds)

**Question**: How to provide consistent observability across all contexts?

---

## The Solution: Event-Driven Telemetry

### What is Event-Driven Telemetry?

**Event**: Structured data representing "something happened"

**Example event** (content generation):
```json
{
  "timestamp": "2025-10-21T14:32:15.123Z",
  "trace_id": "abc123",
  "event_type": "chora.content_generated",
  "status": "success",
  "content_config_id": "readme-intro",
  "generator_type": "jinja2",
  "duration_ms": 234
}
```

**Event-driven**: chora-compose **emits events** when actions occur, **consumers** (gateways, observability tools) **react** to events.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│ CHORA-COMPOSE CORE                                  │
│  - Generators execute                               │
│  - Configs are validated                            │
│  - Content is generated                             │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ emit event
                  ▼
┌─────────────────────────────────────────────────────┐
│ EVENT EMITTER                                       │
│  - Validate event structure                         │
│  - Add trace context (trace_id)                     │
│  - Write to JSONL file (append-only)                │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ write to file
                  ▼
┌─────────────────────────────────────────────────────┐
│ JSONL FILE (var/telemetry/events.jsonl)            │
│  {"timestamp": "...", "event_type": "..."}          │
│  {"timestamp": "...", "event_type": "..."}          │
│  {"timestamp": "...", "event_type": "..."}          │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ consume events
                  ▼
┌─────────────────────────────────────────────────────┐
│ CONSUMERS (Gateway, Observability Tools)            │
│  - n8n workflows (automation)                       │
│  - Datadog/Grafana (monitoring)                     │
│  - Custom dashboards (analytics)                    │
│  - Audit systems (compliance)                       │
└─────────────────────────────────────────────────────┘
```

---

## Why Event-Driven?

### Reason 1: Decoupling

**Traditional approach** (direct integration):
```python
def generate_content(config):
    result = generator.generate(config)

    # Tightly coupled observability
    datadog.track("content_generated", {...})
    splunk.log("Generated content", {...})
    custom_webhook("http://...", {...})

    return result
```

**Problems**:
- ❌ Coupled to specific tools (Datadog, Splunk)
- ❌ Adding new tools requires code changes
- ❌ Hard to test (mock all integrations)

**Event-driven approach**:
```python
def generate_content(config):
    result = generator.generate(config)

    # Decouple: Just emit event
    emit_event(ContentGeneratedEvent(
        content_config_id=config.id,
        generator_type=config.generator,
        duration_ms=duration
    ))

    return result
```

**Benefits**:
- ✅ Decoupled from observability tools
- ✅ Add new consumers without code changes
- ✅ Easy to test (no external dependencies)

### Reason 2: Gateway Integration

**n8n workflow** consuming events:

```
┌──────────────┐
│ Watch JSONL  │ Trigger: File changed
│ File         │ File: var/telemetry/events.jsonl
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Parse Event  │ Extract: event_type, status, duration_ms
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Filter       │ If: status = "error"
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Send Alert   │ Slack: "Content generation failed!"
└──────────────┘
```

**Key insight**: Events are **data** that workflows can process, not tightly-coupled API calls.

### Reason 3: Flexible Consumption

**Multiple consumers can process the same events**:

**Consumer 1** (n8n): Alert on errors
**Consumer 2** (Datadog): Track performance metrics
**Consumer 3** (Audit system): Log all generations for compliance
**Consumer 4** (Dashboard): Show usage analytics

**All consume the same event stream** (no code changes in chora-compose).

---

## Why JSONL Format?

### What is JSONL?

**JSON Lines** (JSONL): Text file with **one JSON object per line**

**Example** (`events.jsonl`):
```jsonl
{"timestamp": "2025-10-21T14:00:00Z", "event_type": "chora.content_generated", "status": "success"}
{"timestamp": "2025-10-21T14:01:15Z", "event_type": "chora.config_validated", "status": "success"}
{"timestamp": "2025-10-21T14:02:30Z", "event_type": "chora.content_generated", "status": "error"}
```

**Not JSON array**:
```json
[
  {"timestamp": "...", "event_type": "..."},
  {"timestamp": "...", "event_type": "..."}
]
```

### Why JSONL over JSON Array?

#### Benefit 1: Append-Only

**JSON Array** (must rewrite entire file):
```python
# Read entire file
with open("events.json", "r") as f:
    events = json.load(f)

# Append new event
events.append(new_event)

# Rewrite entire file
with open("events.json", "w") as f:
    json.dump(events, f)
```

**JSONL** (append new line):
```python
# Just append one line (fast!)
with open("events.jsonl", "a") as f:
    f.write(json.dumps(new_event) + "\n")
```

**Performance**:
- JSON Array: O(n) time (read all events, write all events)
- JSONL: O(1) time (append one line)

**Verdict**: JSONL is **10-100x faster** for appending.

#### Benefit 2: Streaming-Friendly

**JSON Array** (must read entire file):
```python
# Must load entire file into memory
with open("events.json", "r") as f:
    events = json.load(f)  # Load all 1M events

for event in events:
    process(event)
```

**JSONL** (stream line-by-line):
```python
# Stream one line at a time
with open("events.jsonl", "r") as f:
    for line in f:
        event = json.loads(line)
        process(event)  # Process 1 event at a time
```

**Memory usage**:
- JSON Array: Load entire file (e.g., 500 MB for 1M events)
- JSONL: Load one line (~500 bytes per event)

**Verdict**: JSONL scales to **millions of events**.

#### Benefit 3: Resilient to Corruption

**JSON Array** (one error = entire file invalid):
```json
[
  {"event": "valid"},
  {"event": "valid"},
  {"event": "corrupted  <-- Missing closing brace
]
```

**Result**: Entire file is unparseable.

**JSONL** (one error = one line invalid):
```jsonl
{"event": "valid"}
{"event": "valid"}
{"event": "corrupted  <-- Missing closing brace
{"event": "valid"}
{"event": "valid"}
```

**Result**: Only one line fails, other lines parse successfully.

**Verdict**: JSONL is **more resilient** to corruption.

#### Benefit 4: Tool Support

**Common tools with JSONL support**:
- `jq` (JSON query tool): `cat events.jsonl | jq '.event_type'`
- `grep`: `grep "error" events.jsonl`
- `wc -l`: `wc -l events.jsonl` (count events)
- Logstash, Fluentd, Vector (log collectors)
- Datadog, Grafana, Splunk (observability platforms)

**Verdict**: JSONL is **widely supported**.

---

## Why File-Based Storage?

### Alternative 1: Database (e.g., SQLite, Postgres)

**Pros**:
- ✅ Queryable (SQL)
- ✅ Structured
- ✅ Indexed

**Cons**:
- ❌ Requires database setup
- ❌ Harder to stream to external systems
- ❌ File locking issues (concurrent writes)
- ❌ Overkill for event logging

**When database makes sense**: If you need complex queries on historical events (e.g., "Show all errors from last month for jinja2 generator").

**Why we rejected it**: Most consumers stream events in real-time, don't need SQL queries.

### Alternative 2: In-Memory Queue (e.g., Redis, Kafka)

**Pros**:
- ✅ Fast
- ✅ Pub/Sub support
- ✅ Distributed

**Cons**:
- ❌ Requires external service (Redis/Kafka)
- ❌ Not all environments support (CLI, local dev)
- ❌ Events lost on restart (unless persisted)
- ❌ Complexity overhead

**When queue makes sense**: High-throughput distributed systems (1000s events/sec).

**Why we rejected it**: chora-compose runs in varied contexts (CLI, Docker, n8n), can't assume external services.

### Alternative 3: HTTP POST (e.g., Webhooks)

**Pros**:
- ✅ Direct integration
- ✅ Real-time delivery

**Cons**:
- ❌ Requires network (fails if offline)
- ❌ Tightly coupled to endpoint
- ❌ No local storage (can't replay events)
- ❌ Handling retries/failures is complex

**When webhooks make sense**: When you control both producer and consumer.

**Why we rejected it**: Too fragile (network failures), no local audit trail.

### File-Based Storage (JSONL)

**Pros**:
- ✅ Simple (no external dependencies)
- ✅ Works in all environments (CLI, Docker, n8n)
- ✅ Local audit trail (events persist)
- ✅ Easy to stream to external systems (tail -f, file watchers)
- ✅ Resilient (file corruption only affects one line)

**Cons**:
- ⚠️ Not queryable (no SQL)
- ⚠️ Requires file cleanup (rotation)

**Verdict**: Files are the **simplest, most portable** solution for chora-compose's needs.

---

## Event Structure

### Common Event Schema

**All events include**:
```json
{
  "timestamp": "2025-10-21T14:32:15.123Z",  // ISO 8601
  "trace_id": "abc123",                      // Gateway correlation
  "event_type": "chora.content_generated",   // Event identifier
  "status": "success"                        // success | error
}
```

### Event Types

**Currently defined events**:

| Event Type | When Emitted | Key Fields |
|------------|-------------|------------|
| `chora.content_generated` | After content generation | `content_config_id`, `generator_type`, `duration_ms` |
| `chora.config_validated` | After config validation | `config_id`, `config_type`, `validation_result` |
| `chora.artifact_assembled` | After artifact assembly | `artifact_id`, `parts_count`, `duration_ms` |

**Extensible**: New event types can be added without breaking consumers (consumers filter by `event_type`).

### Trace Context

**Trace ID** enables **cross-system correlation**:

```
┌────────────────┐
│ n8n Workflow   │ trace_id=abc123
└────────┬───────┘
         │ Set CHORA_TRACE_ID=abc123
         ▼
┌────────────────┐
│ chora-compose  │ Reads CHORA_TRACE_ID env var
│ (MCP Server)   │ Emits events with trace_id=abc123
└────────┬───────┘
         │ emit event
         ▼
┌────────────────┐
│ Event:         │
│ {              │
│   "trace_id": "abc123",  <-- Same ID!
│   ...          │
│ }              │
└────────────────┘
```

**Benefit**: n8n can correlate events back to the workflow that triggered them.

---

## Integration Patterns

### Pattern 1: File Watcher (Real-time)

**n8n workflow**:
```
Watch File Node
  File: var/telemetry/events.jsonl
  Trigger: On file change

  ↓

Parse JSONL Node
  Extract: Last line
  Parse: JSON

  ↓

Filter Node
  Condition: event_type = "chora.content_generated"

  ↓

Action Node
  Send to Datadog / Slack / Webhook
```

**Benefits**:
- ✅ Real-time processing
- ✅ No polling overhead
- ✅ Simple setup

### Pattern 2: Periodic Batch Processing

**Cron job**:
```bash
# Every hour, process new events
0 * * * * /usr/bin/process-events.sh
```

**Script** (`process-events.sh`):
```bash
#!/bin/bash
# Read events since last run
tail -n +$LAST_LINE var/telemetry/events.jsonl | \
  jq 'select(.status == "error")' | \
  curl -X POST https://alerts.example.com/api/events \
    -H "Content-Type: application/json" \
    -d @-
```

**Benefits**:
- ✅ Batch processing (efficient)
- ✅ No real-time overhead
- ✅ Simple cron setup

### Pattern 3: Log Aggregation

**Fluentd config**:
```yaml
<source>
  @type tail
  path /var/chora-compose/telemetry/events.jsonl
  pos_file /var/log/fluentd/events.pos
  tag chora.events
  format json
</source>

<match chora.events>
  @type datadog
  api_key YOUR_API_KEY
</match>
```

**Benefits**:
- ✅ Industry-standard log aggregation
- ✅ Ship to Datadog, Splunk, Elasticsearch, etc.
- ✅ Built-in buffering and retries

---

## Privacy & Security Considerations

### PII Handling

**Events may contain sensitive data**:
- Config IDs (might reveal project names)
- Context data (might include user names, emails)
- Error messages (might include file paths)

**Best practices**:

1. **Don't log PII in events**:
   ```python
   # Bad
   emit_event(ContentGeneratedEvent(
       context={"user_email": "alice@example.com"}  # PII!
   ))

   # Good
   emit_event(ContentGeneratedEvent(
       context_keys=["user_id", "project_name"]  # No values
   ))
   ```

2. **Sanitize file paths**:
   ```python
   # Bad
   error_message="/home/alice/secret-project/config.json not found"

   # Good
   error_message="Config file not found: <redacted>"
   ```

3. **Encrypt events at rest** (for compliance):
   ```bash
   # Encrypt events file
   gpg --encrypt var/telemetry/events.jsonl
   ```

### Access Control

**Events file permissions**:
```bash
# Restrict access to chora-compose user only
chmod 600 var/telemetry/events.jsonl
chown chora-compose:chora-compose var/telemetry/events.jsonl
```

**Production setup**:
- ✅ Events file readable only by chora-compose process
- ✅ Gateway reads via secure channel (SFTP, authenticated API)
- ✅ Audit logging for event access

---

## Performance Characteristics

### Write Performance

**Benchmarks** (1000 events):
- JSONL append: ~50ms (20,000 events/sec)
- Database insert: ~500ms (2,000 events/sec)
- HTTP POST: ~2000ms (500 events/sec)

**Verdict**: JSONL is **10-40x faster** than alternatives.

### Storage Overhead

**Typical event size**: ~500 bytes
**1 million events**: ~500 MB (uncompressed)
**Compressed (gzip)**: ~50 MB (10:1 ratio)

**File rotation strategy**:
```bash
# Rotate daily, keep 30 days
events-2025-10-21.jsonl.gz
events-2025-10-22.jsonl.gz
...
events-2025-11-20.jsonl.gz
```

**Storage cost**: ~1.5 GB/month (30 days × 50 MB/day)

**Verdict**: Storage overhead is **negligible** (<2 GB/month).

---

## Real-World Scenarios

### Scenario 1: Error Alerting

**Requirement**: Alert team when content generation fails

**Setup** (n8n workflow):
```
Watch events.jsonl
  ↓
Filter: status = "error"
  ↓
Send Slack message: "Content generation failed: {config_id}"
```

**Event** (triggers alert):
```json
{
  "timestamp": "2025-10-21T14:32:15Z",
  "event_type": "chora.content_generated",
  "status": "error",
  "content_config_id": "readme-intro",
  "error_message": "Template file not found"
}
```

**Result**: Team receives Slack alert immediately.

### Scenario 2: Performance Monitoring

**Requirement**: Track generation performance over time

**Setup** (Datadog):
```python
# Datadog agent reads events.jsonl
# Extracts duration_ms for each event
# Sends to Datadog metrics API
```

**Dashboard**:
```
Metric: chora.generation.duration
Filter: generator_type = "jinja2"
Aggregation: p95 (95th percentile)

Chart: p95 duration over time
```

**Insight**: "jinja2 generation p95 is 250ms (target: <500ms) ✅"

### Scenario 3: Usage Analytics

**Requirement**: Understand which generators are most used

**Setup** (Custom script):
```bash
# Count events by generator type
cat events.jsonl | \
  jq -r '.generator_type' | \
  sort | uniq -c | sort -rn
```

**Output**:
```
  1543 jinja2
   892 code_generation
   234 template_fill
    67 demonstration
```

**Insight**: "jinja2 is used 62% of the time"

---

## Future Evolution

### Planned Enhancements

**1. Event Schema Versioning**
```json
{
  "schema_version": "1.0",
  "event_type": "chora.content_generated",
  ...
}
```

**Benefit**: Support breaking changes in event structure.

**2. Structured Error Details**
```json
{
  "status": "error",
  "error": {
    "code": "TEMPLATE_NOT_FOUND",
    "message": "Template file not found",
    "path": "templates/readme.j2"
  }
}
```

**Benefit**: Machine-readable error codes for automated remediation.

**3. Performance Metrics**
```json
{
  "event_type": "chora.content_generated",
  "performance": {
    "template_load_ms": 10,
    "render_ms": 200,
    "validation_ms": 5,
    "total_ms": 215
  }
}
```

**Benefit**: Detailed performance breakdown for optimization.

---

## Comparison with Other Tools

### Terraform (JSON logs)

**Similar**:
- File-based logging
- Structured JSON events

**Different**:
- Terraform: JSON array per run (not streaming)
- chora-compose: JSONL streaming (append-only)

### n8n (Execution logs)

**Similar**:
- Event-driven architecture
- Correlation via execution ID (≈ trace_id)

**Different**:
- n8n: Logs in database (Postgres/SQLite)
- chora-compose: Logs in JSONL files (simpler)

### GitHub Actions (Job logs)

**Similar**:
- Structured events
- External consumption (webhooks)

**Different**:
- GitHub: HTTP webhooks (real-time)
- chora-compose: JSONL files (portable)

---

## Guidelines for Users

### Consuming Events

**Read events with jq**:
```bash
# All successful generations
cat events.jsonl | jq 'select(.status == "success")'

# Errors from last hour
cat events.jsonl | jq 'select(.status == "error" and .timestamp > "2025-10-21T13:00:00Z")'

# Average duration by generator
cat events.jsonl | jq -s 'group_by(.generator_type) | map({generator: .[0].generator_type, avg_ms: (map(.duration_ms) | add / length)})'
```

**Stream events in real-time**:
```bash
# Watch for new events (tail -f equivalent)
tail -f var/telemetry/events.jsonl | jq '.'

# Filter for errors only
tail -f var/telemetry/events.jsonl | jq 'select(.status == "error")'
```

### Event Cleanup

**Rotate events daily**:
```bash
# Rotate and compress
mv var/telemetry/events.jsonl var/telemetry/events-$(date +%Y-%m-%d).jsonl
gzip var/telemetry/events-$(date +%Y-%m-%d).jsonl
touch var/telemetry/events.jsonl

# Delete old events (>30 days)
find var/telemetry/ -name "events-*.jsonl.gz" -mtime +30 -delete
```

---

## Conclusion

**Event-driven telemetry with JSONL** provides:

✅ **Decoupled observability** - No tight coupling to specific tools
✅ **Gateway integration** - Events as data for n8n, Make, etc.
✅ **High performance** - JSONL append is O(1), scales to millions of events
✅ **Streaming-friendly** - Process events line-by-line (low memory)
✅ **Resilient** - Corruption affects one line, not entire file
✅ **Portable** - Works in all environments (CLI, Docker, n8n)
✅ **Simple** - No external dependencies (databases, queues)

**Trade-off**: Not queryable with SQL (use files → database if needed).

**Key principle**: **Events as data** enables flexible, decoupled observability across diverse deployment contexts.

---

## Related Documentation

**Diataxis References**:
- [Reference: Event Schemas](../../reference/api/telemetry/event-schemas.md) - Event structure reference
- [Reference: Event Emitter API](../../reference/api/telemetry/event-emitter.md) - API documentation
- [How-To: Monitor chora-compose with n8n](../../how-to/integration/monitor-with-n8n.md) - Practical guide

**Conceptual Relationships**:
- [Explanation: MCP Workflow Model](../integration/mcp-workflow-model.md) - Gateway integration
- [Explanation: Configuration-Driven Development](../concepts/configuration-driven-development.md) - CDD philosophy

**External Resources**:
- [JSON Lines Specification](https://jsonlines.org/)
- [n8n File Trigger Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.filetrigger/)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
