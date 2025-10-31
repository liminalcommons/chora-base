# Integration with Orchestration Layers

**Purpose**: Understand the philosophy and patterns for integrating chora-compose with orchestration layers like n8n, Zapier, and custom gateways.

**Audience**: Platform engineers designing integration points, developers building gateway layers, technical leads evaluating orchestration strategies.

---

## Overview

Chora Compose is designed for **gateway consumption** — it exposes capabilities that orchestration layers can discover, validate, and invoke. This document explains the architectural patterns, integration philosophies, and design decisions that enable seamless orchestration integration.

**Key insight**: Chora Compose is NOT an orchestration layer itself. It's a **specialized content generation service** designed to be orchestrated.

---

## Orchestration vs Service Layers

### Understanding the Separation

```
┌─────────────────────────────────────────────────────────────┐
│ Orchestration Layer (What happens when)                    │
│   - Workflow sequencing                                     │
│   - Conditional logic (if this, then that)                  │
│   - Error handling (retry, fallback)                        │
│   - Integration (connect multiple services)                 │
│   Examples: n8n, Zapier, Airflow, Temporal                  │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ Invokes
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Service Layer (What it does)                                │
│   - Specialized capabilities                                │
│   - Stateless execution                                     │
│   - Clear input/output contracts                            │
│   - Observable operations                                   │
│                                                             │
│   ┌─────────────────────────────────────────────┐         │
│   │ Chora Compose ← YOU ARE HERE                │         │
│   │ (Specialized: Content Generation)           │         │
│   └─────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

**Chora Compose's Role**: **Service layer** (specialized content generation)

**Orchestration layer's role**: Decide **when** and **how** to call Chora Compose

**Why this separation**:
- **Single Responsibility**: Chora Compose focuses on content generation excellence
- **Composability**: Any orchestration layer can integrate (n8n, Zapier, custom)
- **Testability**: Service can be tested independently
- **Scalability**: Orchestration and service scale separately

---

## Gateway Consumption Model

### Core Principles

**1. Discoverability**: Gateways can introspect capabilities dynamically

**2. Validation**: Gateways can verify prerequisites before invocation

**3. Traceability**: Gateways can correlate requests/responses across services

**4. Observability**: Gateways can monitor operations via event streams

### Capability Discovery

**Problem**: Gateway doesn't know what chora-compose can do (version changes, plugins)

**Solution**: MCP resources expose capabilities programmatically

**Implementation**:

```python
# Gateway discovers capabilities
caps = await mcp_client.read_resource("capabilities://server")

# Extract features
features = caps["features"]
if features["batch_operations"]:
    # Use batch_generate tool
    result = await mcp_client.call_tool("batch_generate", {...})
else:
    # Fall back to sequential
    for config in configs:
        result = await mcp_client.call_tool("generate_content", {...})
```

**Benefits**:
- ✅ Gateway adapts to server capabilities (future-proof)
- ✅ No hardcoded assumptions (flexible integration)
- ✅ Graceful degradation (fallback if feature unavailable)

**Chora Compose resources** (v1.3.0):
- `capabilities://server` - Server metadata and limits
- `capabilities://tools` - Available MCP tools
- `capabilities://generators` - Generator capabilities and dependencies
- `capabilities://resources` - Resource URIs

### Pre-flight Validation

**Problem**: Gateway calls generator, discovers credentials missing mid-execution

**Solution**: `upstream_dependencies` in generator metadata

**Implementation**:

```python
# Gateway checks generator dependencies before calling
generators = await mcp_client.read_resource("capabilities://generators")

for gen in generators:
    if gen["type"] == "code_generation":
        # Check dependencies
        deps = gen["upstream_dependencies"]
        if "anthropic" in deps["services"]:
            # Validate credential exists
            if not os.getenv("ANTHROPIC_API_KEY"):
                raise CredentialMissingError("code_generation requires ANTHROPIC_API_KEY")

# Only proceed if all credentials valid
result = await mcp_client.call_tool("generate_content", {
    "content_config_id": "my-config",
    "generator": "code_generation"
})
```

**Benefits**:
- ✅ Fail fast (before expensive operations)
- ✅ Clear error messages (know exactly what's missing)
- ✅ Gateway can prompt user for credentials
- ✅ Prevent partial execution (all-or-nothing)

**Example `upstream_dependencies`**:

```json
{
  "generator_type": "code_generation",
  "upstream_dependencies": {
    "services": ["anthropic"],
    "credentials_required": ["ANTHROPIC_API_KEY"],
    "concurrency_safe": true,
    "stability": "stable"
  }
}
```

### Trace Context Propagation

**Problem**: Gateway orchestrates multiple services, needs to correlate operations

**Solution**: `CHORA_TRACE_ID` environment variable

**Implementation**:

```python
import uuid
import os
import subprocess

# Gateway generates trace ID
trace_id = f"workflow-{uuid.uuid4()}"

# Set environment variable before invoking
os.environ["CHORA_TRACE_ID"] = trace_id

# All operations inherit trace ID
result = await mcp_client.call_tool("generate_content", {...})

# Events emitted with trace_id
# var/telemetry/events.jsonl:
# {"event_type": "content_generated", "trace_id": "workflow-abc123", ...}
```

**Benefits**:
- ✅ End-to-end tracing (correlate across services)
- ✅ Debugging workflows (filter events by trace_id)
- ✅ Performance analysis (identify bottlenecks)
- ✅ Audit trails (who requested what)

**Trace propagation example**:

```
Gateway (trace_id=workflow-123)
  ↓
Chora Compose (inherits trace_id=workflow-123)
  ├─ generate_content (trace_id=workflow-123)
  ├─ validate_content (trace_id=workflow-123)
  └─ Events emitted (trace_id=workflow-123)
  ↓
Gateway reads events filtered by trace_id=workflow-123
```

### Event Streaming

**Problem**: Gateway needs real-time progress updates (batch operations take minutes)

**Solution**: JSONL event file (`var/telemetry/events.jsonl`)

**Implementation**:

```python
import json
from pathlib import Path

# Gateway starts batch operation
trace_id = "batch-abc123"
os.environ["CHORA_TRACE_ID"] = trace_id

# Start batch
batch_future = await mcp_client.call_tool("batch_generate", {
    "content_config_ids": [...],  # 50 configs
})

# Meanwhile, monitor events
events_file = Path("var/telemetry/events.jsonl")

def watch_events(trace_id):
    """Watch events in real-time."""
    with open(events_file) as f:
        # Seek to end (only new events)
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            event = json.loads(line)
            if event.get("trace_id") == trace_id:
                yield event

# Process events as they arrive
for event in watch_events(trace_id):
    if event["event_type"] == "content_generated":
        print(f"Progress: {event['content_config_id']} completed")
    elif event["event_type"] == "batch_completed":
        print(f"Batch done: {event['successful']}/{event['total']}")
        break
```

**Benefits**:
- ✅ Real-time progress (don't wait for completion)
- ✅ Streaming-friendly (JSONL append-only)
- ✅ Gateway can update UI (progress bars, notifications)
- ✅ Resilient (file survives crashes)

---

## Integration Patterns

### Pattern 1: Request-Response (Synchronous)

**Use case**: Simple, one-off generation (user waits for result)

**Workflow**:
```
Gateway → generate_content → Chora Compose → Generated Content → Gateway
```

**Implementation**:

```python
# n8n HTTP Request node
POST /mcp/tools/generate_content
{
  "content_config_id": "release-notes",
  "context": {"version": "1.3.0", "date": "2025-10-21"}
}

# Response
{
  "success": true,
  "content": "# Release v1.3.0...",
  "duration_ms": 45
}
```

**Characteristics**:
- **Simple**: Single request, single response
- **Blocking**: Gateway waits for completion
- **Fast**: <1 second for most generators

**When to use**: Small operations (1-5 items, <10s total time)

### Pattern 2: Batch with Polling (Asynchronous)

**Use case**: Large batch operations (10+ items, >30s total time)

**Workflow**:
```
Gateway → batch_generate → Chora Compose (returns immediately)
  ↓
Gateway polls for completion
  ↓
Chora Compose → Batch result
```

**Implementation**:

```python
# Step 1: Start batch
batch_id = await mcp_client.call_tool("batch_generate", {
    "content_config_ids": [...],  # 50 configs
    "async": true  # Don't block
})

# Step 2: Poll for completion
while True:
    status = await mcp_client.call_tool("batch_status", {"batch_id": batch_id})
    if status["completed"]:
        break
    await asyncio.sleep(5)  # Poll every 5 seconds

# Step 3: Retrieve results
result = await mcp_client.call_tool("batch_results", {"batch_id": batch_id})
```

**Characteristics**:
- **Non-blocking**: Gateway can do other work
- **Scalable**: Handles long-running operations
- **Complex**: Requires polling logic

**When to use**: Large batches (10+ items, >30s total time)

### Pattern 3: Event-Driven (Push)

**Use case**: Real-time monitoring, complex workflows

**Workflow**:
```
Gateway → batch_generate → Chora Compose
  ↓
Chora Compose emits events → Gateway webhook
  ↓
Gateway processes events → Next workflow step
```

**Implementation**:

```python
# n8n workflow
# Node 1: Start batch generation
POST /mcp/tools/batch_generate
{
  "content_config_ids": [...],
  "webhook_url": "https://my-n8n.com/webhook/batch-progress"
}

# Chora Compose emits events to webhook
POST https://my-n8n.com/webhook/batch-progress
{
  "event_type": "content_generated",
  "content_config_id": "endpoint-users",
  "trace_id": "batch-abc123"
}

# Node 2: n8n catches events, updates progress
# Node 3: On batch_completed event, trigger next workflow
```

**Characteristics**:
- **Real-time**: Immediate updates
- **Decoupled**: Gateway and service independent
- **Complex**: Requires webhook infrastructure

**When to use**: Real-time dashboards, complex multi-step workflows

### Pattern 4: Queue-Based (Asynchronous, Scalable)

**Use case**: High-throughput, distributed systems

**Workflow**:
```
Gateway → Queue (Kafka, RabbitMQ) → Worker → Chora Compose
  ↓
Results queue → Gateway
```

**Implementation**:

```python
# Producer (Gateway)
await kafka_producer.send("chora-compose-requests", {
    "tool": "generate_content",
    "params": {"content_config_id": "api-docs"},
    "trace_id": "req-123"
})

# Consumer (Worker)
async for message in kafka_consumer:
    request = message.value
    result = await mcp_client.call_tool(request["tool"], request["params"])
    await kafka_producer.send("chora-compose-results", {
        "trace_id": request["trace_id"],
        "result": result
    })

# Gateway consumes results
async for message in kafka_consumer:
    if message.value["trace_id"] == "req-123":
        # Process result
        break
```

**Characteristics**:
- **Scalable**: Multiple workers process queue
- **Resilient**: Queue persists requests (survives crashes)
- **Complex**: Requires queue infrastructure

**When to use**: High-volume, production systems (1000+ requests/day)

---

## n8n Integration Patterns

### Specific Patterns for n8n

#### Pattern N1: HTTP Request Node

**Use case**: Direct MCP tool invocation

```
n8n HTTP Request
  ↓
POST http://localhost:8000/mcp/tools/generate_content
  ↓
Parse response
  ↓
Next node
```

**Example**:

```json
// n8n HTTP Request node config
{
  "method": "POST",
  "url": "http://localhost:8000/mcp/tools/generate_content",
  "body": {
    "content_config_id": "{{$json.config_id}}",
    "context": "{{$json.context}}"
  },
  "headers": {
    "Content-Type": "application/json",
    "X-Trace-ID": "{{$workflow.id}}"
  }
}
```

#### Pattern N2: Webhook Trigger

**Use case**: Chora Compose events trigger n8n workflows

```
Chora Compose → Event (JSONL) → Parse → HTTP Request → n8n Webhook
  ↓
n8n catches event
  ↓
Workflow continues (e.g., commit to git, post to Slack)
```

**Example**:

```python
# Chora Compose (post-generation)
import requests

event = {
    "event_type": "content_generated",
    "content_config_id": "api-docs",
    "trace_id": "workflow-123"
}

# Trigger n8n webhook
requests.post("https://my-n8n.com/webhook/content-generated", json=event)
```

```json
// n8n Webhook node
{
  "path": "/webhook/content-generated",
  "method": "POST",
  "response": {
    "statusCode": 200,
    "body": {"received": true}
  }
}
```

#### Pattern N3: MCP Client Node (Future)

**Use case**: Native MCP protocol support in n8n

```
n8n MCP Client Node
  ↓
Discovers chora-compose capabilities
  ↓
Calls tools directly (no HTTP wrapping)
  ↓
Streams events
```

**Benefits**:
- ✅ Native MCP support (no HTTP wrapping)
- ✅ Capability discovery built-in
- ✅ Event streaming integrated

**Status**: Proposed for n8n v2.0+

---

## Scaling Considerations

### Horizontal Scaling

**Pattern**: Multiple chora-compose instances behind load balancer

```
        ┌─────────────┐
        │   Gateway   │
        └──────┬──────┘
               │
        Load Balancer
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│ CC #1 │  │ CC #2 │  │ CC #3 │
└───────┘  └───────┘  └───────┘
```

**Challenges**:

1. **Stateless operations** (solved: chora-compose is stateless)
2. **Shared ephemeral storage** (solved: use shared filesystem or S3)
3. **Event aggregation** (solved: centralized event log)

**Implementation**:

```yaml
# docker-compose.yml
services:
  chora-compose-1:
    image: chora-compose:latest
    environment:
      CHORA_TRACE_ID: ${TRACE_ID}
    volumes:
      - shared-storage:/app/var

  chora-compose-2:
    image: chora-compose:latest
    environment:
      CHORA_TRACE_ID: ${TRACE_ID}
    volumes:
      - shared-storage:/app/var

  nginx:
    image: nginx
    depends_on:
      - chora-compose-1
      - chora-compose-2

volumes:
  shared-storage:
```

**Benefit**: Linear scaling (2x instances = 2x throughput)

### Rate Limiting

**Problem**: Chora Compose uses external APIs (Claude), subject to rate limits

**Pattern**: Gateway implements rate limiting before calling chora-compose

**Implementation**:

```python
from aiolimiter import AsyncLimiter

# Rate limiter: 60 requests/minute (Claude API limit)
limiter = AsyncLimiter(60, 60)

async def generate_with_limit(config_id):
    async with limiter:
        return await mcp_client.call_tool("generate_content", {
            "content_config_id": config_id
        })

# Use in batch
results = await asyncio.gather(*[
    generate_with_limit(id) for id in config_ids
])
```

**Benefit**: Respects API rate limits, prevents 429 errors

### Caching

**Pattern**: Gateway caches generated content to reduce redundant generation

**Implementation**:

```python
import hashlib

def cache_key(config_id, context):
    """Generate cache key from config and context."""
    context_hash = hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()
    return f"{config_id}:{context_hash}"

# Check cache before generating
key = cache_key("api-docs", {"version": "1.3.0"})
cached = redis_client.get(key)

if cached:
    return json.loads(cached)  # Cache hit

# Generate
result = await mcp_client.call_tool("generate_content", {...})

# Cache for 1 hour
redis_client.setex(key, 3600, json.dumps(result))
```

**Benefit**: Faster response (cache hit ~1ms vs generation ~50ms)

**Caveat**: Invalidate cache when config or templates change

---

## Best Practices

### Do ✅

1. **Discover capabilities before invoking**
   ```python
   # ✅ Good: Check if feature exists
   caps = await read_resource("capabilities://server")
   if caps["features"]["batch_operations"]:
       use_batch()
   else:
       use_sequential()
   ```

2. **Set trace context for all operations**
   ```python
   # ✅ Good: Correlate operations
   os.environ["CHORA_TRACE_ID"] = workflow_id
   generate_content(...)
   ```

3. **Validate credentials pre-flight**
   ```python
   # ✅ Good: Fail fast
   deps = generator["upstream_dependencies"]
   for cred in deps["credentials_required"]:
       if not os.getenv(cred):
           raise CredentialMissingError(cred)
   ```

4. **Monitor events for long-running operations**
   ```python
   # ✅ Good: Real-time progress
   for event in watch_events(trace_id):
       update_progress_bar(event)
   ```

### Don't ❌

1. **Don't hardcode capabilities**
   ```python
   # ❌ Bad: Assumes feature exists
   result = batch_generate(...)  # What if batch_operations disabled?
   ```

2. **Don't skip trace context**
   ```python
   # ❌ Bad: Can't correlate events
   generate_content(...)  # No trace_id set
   ```

3. **Don't ignore event failures**
   ```python
   # ❌ Bad: Silent failures
   for event in watch_events(trace_id):
       if event["event_type"] == "content_generated":
           # Process success
           pass
       # Didn't check for "generation_failed" events
   ```

4. **Don't call generators without validating dependencies**
   ```python
   # ❌ Bad: Discovers missing credential mid-execution
   result = generate_content(generator="code_generation")  # API key missing!
   ```

---

## Summary

**Key Principles**:

1. **Discoverability**: Use `capabilities://` resources to introspect dynamically
2. **Pre-flight Validation**: Check `upstream_dependencies` before invoking
3. **Traceability**: Set `CHORA_TRACE_ID` for request correlation
4. **Observability**: Monitor `var/telemetry/events.jsonl` for real-time updates

**Integration Patterns**:
- **Request-Response**: Simple, synchronous (small operations)
- **Batch with Polling**: Asynchronous, scalable (large operations)
- **Event-Driven**: Real-time, decoupled (complex workflows)
- **Queue-Based**: High-throughput, distributed (production systems)

**n8n Specific**:
- **HTTP Request Node**: Direct MCP tool invocation
- **Webhook Trigger**: Event-driven workflows
- **MCP Client Node**: Future native support

**Scaling**:
- **Horizontal**: Multiple instances + load balancer
- **Rate Limiting**: Respect API limits
- **Caching**: Reduce redundant generation

**Philosophy**: Chora Compose is a **service**, not an orchestration layer. It exposes capabilities that gateways **discover, validate, invoke, and monitor**.

---

## Related Documentation

### How-To Guides
- [Use with Gateway](../../how-to/mcp/use-with-gateway.md) - Step-by-step n8n integration
- [Use Capability Discovery](../../how-to/mcp/use-capability-discovery.md) - Capability introspection

### Explanation
- [Position in AI Tooling](position-in-ai-tooling.md) - Ecosystem positioning
- [Event-Driven Telemetry](../design-decisions/event-driven-telemetry.md) - Event architecture

### Reference
- [Capabilities Discovery](../../reference/api/resources/capabilities.md) - Capability resources
- [MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md) - All MCP tools

---

**Last Updated**: 2025-10-21 | **Phase**: Sprint 4 - Ecosystem Expansion
