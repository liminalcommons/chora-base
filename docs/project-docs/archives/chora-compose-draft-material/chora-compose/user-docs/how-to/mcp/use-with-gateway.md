# How to Integrate Chora-Compose with a Gateway

**Version:** v1.3.0
**Difficulty:** Intermediate
**Time:** 30-45 minutes
**Prerequisites:** MCP server running, basic Python knowledge

---

## Overview

This guide shows how to integrate **chora-compose** with a gateway or orchestration layer, leveraging v1.3.0 features:

- **Generator Dependencies**: Pre-flight credential validation via `upstream_dependencies`
- **Event Emission**: Request/response correlation via trace context
- **Capability Discovery**: Dynamic feature detection via `capabilities://` resources

### What You'll Build

A simple Python gateway that:
1. Discovers chora-compose capabilities dynamically
2. Validates credentials before calling generators
3. Sets trace context for request correlation
4. Parses emitted events for monitoring

---

## Architecture

```
┌─────────────┐
│   Gateway   │
│  (Your Code)│
└──────┬──────┘
       │
       │ 1. Discover capabilities
       ├────────────────────────────────────┐
       │                                    │
       │ capabilities://server              │
       │ capabilities://generators          │
       │                                    │
       │ 2. Validate credentials            │
       ├────────────────────────────────────┤
       │                                    │
       │ Check upstream_dependencies        │
       │ Verify ANTHROPIC_API_KEY exists    │
       │                                    │
       │ 3. Set trace context               │
       ├────────────────────────────────────┤
       │                                    │
       │ export CHORA_TRACE_ID=workflow-123 │
       │                                    │
       │ 4. Call MCP tools                  │
       ├────────────────────────────────────┤
       │                                    │
       │ generate_content(...)              │
       │                                    │
       │ 5. Parse events                    │
       ├────────────────────────────────────┤
       │                                    │
       │ Read var/telemetry/events.jsonl    │
       │ Filter by trace_id                 │
       │                                    │
       └────────────────────────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  chora-compose   │
           │   MCP Server     │
           └──────────────────┘
```

---

## Step 1: Discover Server Capabilities

Before using chora-compose, query its capabilities to understand what features are available.

### Query Server Metadata

```python
from mcp import ClientSession
import os

async def discover_server():
    """Discover chora-compose server capabilities."""
    server_url = os.getenv("CHORA_COMPOSE_MCP_URL", "http://localhost:8000")

    async with ClientSession(server_url) as session:
        # Read server capabilities
        result = await session.read_resource("capabilities://server")
        server_caps = result.contents[0].text  # JSON string

        import json
        caps = json.loads(server_caps)

        print(f"Server: {caps['name']} v{caps['version']}")
        print(f"MCP Version: {caps['mcp_version']}")
        print(f"Tools Available: {caps['tool_count']}")
        print(f"Generators: {caps['generator_count']}")
        print()

        # Check feature flags
        print("Features:")
        for feature, enabled in caps["features"].items():
            status = "✅" if enabled else "❌"
            print(f"  {status} {feature}")
        print()

        # Check operational limits
        print("Limits:")
        for limit, value in caps["limits"].items():
            print(f"  {limit}: {value}")

        return caps

# Usage
import asyncio
caps = asyncio.run(discover_server())
```

**Example Output:**

```
Server: chora-compose v1.3.0
MCP Version: 1.0
Tools Available: 17
Generators: 5

Features:
  ✅ content_generation
  ✅ artifact_assembly
  ✅ config_lifecycle
  ✅ batch_operations
  ✅ ephemeral_storage
  ✅ resource_providers
  ✅ generator_plugins
  ✅ capability_discovery
  ❌ validation_suggestions

Limits:
  max_content_size_bytes: 10000000
  max_artifact_components: 100
  ephemeral_retention_days: 30
  max_batch_size: 50
```

### Check Feature Availability

```python
async def check_feature(session, feature_name):
    """Check if a specific feature is available."""
    result = await session.read_resource("capabilities://server")
    caps = json.loads(result.contents[0].text)

    if caps["features"].get(feature_name):
        print(f"✅ {feature_name} is available")
        return True
    else:
        print(f"❌ {feature_name} is NOT available")
        return False

# Example: Check if config lifecycle tools exist
has_config_lifecycle = await check_feature(session, "config_lifecycle")

if has_config_lifecycle:
    # Use draft_config, test_config, etc.
    result = await session.call_tool("draft_config", {...})
else:
    # Fall back to manual config creation
    config = create_config_manually()
```

---

## Step 2: Query Generator Dependencies

Before calling a generator, check its dependencies to validate credentials and estimate latency.

### Discover All Generators

```python
async def discover_generators(session):
    """Discover all available generators and their dependencies."""
    result = await session.read_resource("capabilities://generators")
    gen_data = json.loads(result.contents[0].text)

    generators = gen_data["generators"]

    print(f"Found {len(generators)} generators:\n")

    for gen_type, gen_info in generators.items():
        print(f"Generator: {gen_type}")
        print(f"  Status: {gen_info['status']}")
        print(f"  Source: {gen_info['source']}")

        deps = gen_info.get("upstream_dependencies")
        if deps:
            print(f"  Services: {deps['services']}")
            print(f"  Credentials: {deps['credentials_required']}")
            print(f"  Concurrency Safe: {deps['concurrency_safe']}")

            if deps.get("expected_latency_ms"):
                p50 = deps["expected_latency_ms"].get("p50", "N/A")
                p95 = deps["expected_latency_ms"].get("p95", "N/A")
                print(f"  Expected Latency: p50={p50}ms, p95={p95}ms")
        else:
            print(f"  No external dependencies")

        print()

    return generators

# Usage
generators = await discover_generators(session)
```

**Example Output:**

```
Found 5 generators:

Generator: jinja2
  Status: stable
  Source: builtin
  No external dependencies

Generator: code_generation
  Status: stable
  Source: builtin
  Services: ['anthropic']
  Credentials: ['ANTHROPIC_API_KEY']
  Concurrency Safe: True
  Expected Latency: p50=1500ms, p95=5000ms

Generator: template_fill
  Status: stable
  Source: builtin
  No external dependencies

Generator: demonstration
  Status: stable
  Source: builtin
  No external dependencies

Generator: bdd_scenario
  Status: experimental
  Source: builtin
  No external dependencies
```

### Validate Credentials Before Calling

```python
import os

async def validate_generator_credentials(session, generator_type):
    """Validate that required credentials exist for a generator."""
    result = await session.read_resource("capabilities://generators")
    gen_data = json.loads(result.contents[0].text)

    generator = gen_data["generators"].get(generator_type)
    if not generator:
        raise ValueError(f"Unknown generator: {generator_type}")

    deps = generator.get("upstream_dependencies")
    if not deps:
        # No dependencies - always valid
        return True

    # Check required credentials
    missing = []
    for cred in deps["credentials_required"]:
        if not os.getenv(cred):
            missing.append(cred)

    if missing:
        raise ValueError(
            f"Missing credentials for {generator_type}: {', '.join(missing)}"
        )

    print(f"✅ Credentials validated for {generator_type}")
    return True

# Example: Validate before using code_generation
try:
    await validate_generator_credentials(session, "code_generation")
    # Safe to call generate_content with type=code_generation
    result = await session.call_tool("generate_content", {...})
except ValueError as e:
    print(f"❌ Cannot use code_generation: {e}")
    # Fall back to jinja2
    result = await session.call_tool("generate_content", {
        "config_id": "readme-intro",
        "generator_type": "jinja2"  # Fallback
    })
```

### Set Timeouts Based on Expected Latency

```python
import asyncio

async def call_with_timeout(session, generator_type, tool_name, params):
    """Call MCP tool with timeout based on generator latency."""
    result = await session.read_resource("capabilities://generators")
    gen_data = json.loads(result.contents[0].text)

    generator = gen_data["generators"].get(generator_type)
    deps = generator.get("upstream_dependencies", {})

    # Default timeout: 30 seconds
    timeout_ms = 30000

    # Use 2x p95 latency if available
    if deps.get("expected_latency_ms"):
        p95 = deps["expected_latency_ms"].get("p95", 5000)
        timeout_ms = p95 * 2

    timeout_sec = timeout_ms / 1000
    print(f"Setting timeout to {timeout_sec}s for {generator_type}")

    try:
        result = await asyncio.wait_for(
            session.call_tool(tool_name, params),
            timeout=timeout_sec
        )
        return result
    except asyncio.TimeoutError:
        raise TimeoutError(
            f"{tool_name} timed out after {timeout_sec}s "
            f"(expected p95: {deps.get('expected_latency_ms', {}).get('p95')}ms)"
        )

# Example: Call code_generation with automatic timeout
result = await call_with_timeout(
    session,
    generator_type="code_generation",
    tool_name="generate_content",
    params={
        "config_id": "readme-intro",
        "context": {"project_name": "my-project"}
    }
)
```

---

## Step 3: Set Trace Context for Correlation

Set the `CHORA_TRACE_ID` environment variable before calling chora-compose to enable request/response correlation.

### Propagate Trace ID to MCP Server

```python
import os
import uuid
import subprocess

def call_chora_with_trace(trace_id, mcp_command):
    """Call chora-compose MCP server with trace context."""
    env = os.environ.copy()
    env["CHORA_TRACE_ID"] = trace_id

    # Run MCP server with trace context
    result = subprocess.run(
        mcp_command,
        env=env,
        capture_output=True,
        text=True
    )

    return result

# Example: Generate content with trace context
trace_id = f"workflow-{uuid.uuid4()}"
print(f"Trace ID: {trace_id}")

result = call_chora_with_trace(
    trace_id=trace_id,
    mcp_command=[
        "python", "-m", "chora_compose.mcp.server",
        "--tool", "generate_content",
        "--config-id", "readme-intro"
    ]
)

print(f"Result: {result.stdout}")
```

### Async MCP Session with Trace Context

```python
import os
import uuid

async def generate_with_trace(session, config_id, context=None):
    """Generate content with automatic trace context."""
    # Generate trace ID
    trace_id = f"req-{uuid.uuid4()}"

    # Set environment variable for this request
    os.environ["CHORA_TRACE_ID"] = trace_id

    print(f"🔍 Trace ID: {trace_id}")

    try:
        # Call generate_content
        result = await session.call_tool("generate_content", {
            "config_id": config_id,
            "context": context or {}
        })

        print(f"✅ Content generated: {result}")
        return trace_id, result
    finally:
        # Clean up (optional - can keep for multiple calls)
        pass

# Usage
trace_id, result = await generate_with_trace(
    session,
    config_id="readme-intro",
    context={"project_name": "my-project"}
)

# Later: Query events by trace_id
events = parse_events_by_trace(trace_id)
```

### Multi-Step Workflow with Trace Context

```python
import os
import uuid

async def run_workflow_with_trace(session):
    """Run multi-step workflow with trace correlation."""
    trace_id = f"workflow-{uuid.uuid4()}"
    os.environ["CHORA_TRACE_ID"] = trace_id

    print(f"🔍 Starting workflow: {trace_id}\n")

    # Step 1: Generate intro
    print("Step 1: Generating intro...")
    await session.call_tool("generate_content", {
        "config_id": "readme-intro",
        "context": {"project_name": "my-project"}
    })

    # Step 2: Generate body
    print("Step 2: Generating body...")
    await session.call_tool("generate_content", {
        "config_id": "readme-body",
        "context": {"features": ["feature1", "feature2"]}
    })

    # Step 3: Assemble artifact
    print("Step 3: Assembling artifact...")
    await session.call_tool("assemble_artifact", {
        "config_id": "readme-full",
        "output_path": "dist/README.md"
    })

    print(f"\n✅ Workflow completed: {trace_id}")

    # All events have the same trace_id for correlation
    return trace_id

# Usage
trace_id = await run_workflow_with_trace(session)

# Query all events for this workflow
events = parse_events_by_trace(trace_id)
print(f"Workflow emitted {len(events)} events")
```

---

## Step 4: Parse Emitted Events

Read and parse events from `var/telemetry/events.jsonl` to monitor workflows.

### Read All Events

```python
import json
from pathlib import Path

def read_events(events_file="var/telemetry/events.jsonl"):
    """Read all events from the events file."""
    events_path = Path(events_file)

    if not events_path.exists():
        return []

    events = []
    with open(events_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            events.append(event)

    return events

# Usage
all_events = read_events()
print(f"Total events: {len(all_events)}")

for event in all_events:
    print(f"{event['timestamp']}: {event['event_type']} - {event['status']}")
```

### Filter Events by Trace ID

```python
def parse_events_by_trace(trace_id, events_file="var/telemetry/events.jsonl"):
    """Parse events for a specific trace ID."""
    events = read_events(events_file)

    # Filter by trace_id
    workflow_events = [e for e in events if e.get("trace_id") == trace_id]

    return workflow_events

# Usage
trace_id = "workflow-abc123"
events = parse_events_by_trace(trace_id)

print(f"Workflow {trace_id}: {len(events)} events\n")

for event in events:
    event_type = event["event_type"]
    status = event["status"]
    duration = event.get("duration_ms", 0)

    if event_type == "chora.content_generated":
        config_id = event["content_config_id"]
        generator = event["generator_type"]
        print(f"  Generated {config_id} with {generator}: {status} ({duration}ms)")

    elif event_type == "chora.artifact_assembled":
        artifact_id = event["artifact_config_id"]
        sections = event["section_count"]
        output = event["output_path"]
        print(f"  Assembled {artifact_id} ({sections} sections) → {output}: {status} ({duration}ms)")
```

### Stream Events in Real-Time

```python
import time
import json
from pathlib import Path

def stream_events(events_file="var/telemetry/events.jsonl", trace_id=None):
    """Stream events in real-time (tail -f style)."""
    events_path = Path(events_file)

    # Wait for file to exist
    while not events_path.exists():
        time.sleep(0.1)

    with open(events_path, encoding="utf-8") as f:
        # Seek to end
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                # No new data, wait
                time.sleep(0.1)
                continue

            if not line.strip():
                continue

            event = json.loads(line)

            # Filter by trace_id if provided
            if trace_id is None or event.get("trace_id") == trace_id:
                yield event

# Usage: Monitor workflow events in real-time
trace_id = "workflow-abc123"

print(f"Streaming events for {trace_id}...\n")

for event in stream_events(trace_id=trace_id):
    print(f"{event['timestamp']}: {event['event_type']} - {event['status']}")

    if event["status"] == "error":
        print(f"  ERROR: {event['error_message']}")
```

### Analyze Workflow Performance

```python
def analyze_workflow(trace_id, events_file="var/telemetry/events.jsonl"):
    """Analyze performance metrics for a workflow."""
    events = parse_events_by_trace(trace_id, events_file)

    if not events:
        print(f"No events found for trace_id: {trace_id}")
        return

    print(f"Workflow Analysis: {trace_id}\n")
    print(f"Total Events: {len(events)}")

    # Count by event type
    by_type = {}
    for event in events:
        event_type = event["event_type"]
        by_type[event_type] = by_type.get(event_type, 0) + 1

    print("\nEvent Types:")
    for event_type, count in by_type.items():
        print(f"  {event_type}: {count}")

    # Count by status
    success_count = sum(1 for e in events if e["status"] == "success")
    error_count = sum(1 for e in events if e["status"] == "error")

    print(f"\nStatus:")
    print(f"  Success: {success_count}")
    print(f"  Error: {error_count}")

    # Total duration
    total_duration = sum(e.get("duration_ms", 0) for e in events)
    print(f"\nTotal Duration: {total_duration}ms")

    # Per-generator breakdown
    by_generator = {}
    for event in events:
        if event["event_type"] == "chora.content_generated":
            generator = event["generator_type"]
            duration = event.get("duration_ms", 0)

            if generator not in by_generator:
                by_generator[generator] = {"count": 0, "total_ms": 0}

            by_generator[generator]["count"] += 1
            by_generator[generator]["total_ms"] += duration

    if by_generator:
        print("\nGenerator Performance:")
        for generator, stats in by_generator.items():
            avg_ms = stats["total_ms"] / stats["count"] if stats["count"] > 0 else 0
            print(f"  {generator}: {stats['count']} calls, avg {avg_ms:.0f}ms")

    # Errors
    errors = [e for e in events if e["status"] == "error"]
    if errors:
        print("\nErrors:")
        for event in errors:
            print(f"  {event['event_type']}: {event.get('error_message', 'Unknown error')}")

# Usage
analyze_workflow("workflow-abc123")
```

**Example Output:**

```
Workflow Analysis: workflow-abc123

Total Events: 5

Event Types:
  chora.content_generated: 4
  chora.artifact_assembled: 1

Status:
  Success: 5
  Error: 0

Total Duration: 2134ms

Generator Performance:
  jinja2: 2 calls, avg 150ms
  template_fill: 1 calls, avg 120ms
  code_generation: 1 calls, avg 1819ms
```

---

## Step 5: Complete Gateway Example

Here's a complete gateway implementation combining all the above patterns:

```python
"""Simple Gateway for Chora-Compose Integration.

This gateway demonstrates:
1. Capability discovery
2. Credential validation
3. Trace context propagation
4. Event parsing and monitoring
"""

import asyncio
import json
import os
import uuid
from pathlib import Path
from mcp import ClientSession


class ChoraGateway:
    """Gateway for chora-compose MCP server."""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.generators = None
        self.server_caps = None

    async def initialize(self):
        """Discover server capabilities."""
        async with ClientSession(self.server_url) as session:
            # Discover server
            result = await session.read_resource("capabilities://server")
            self.server_caps = json.loads(result.contents[0].text)

            print(f"✅ Connected to {self.server_caps['name']} v{self.server_caps['version']}")

            # Discover generators
            result = await session.read_resource("capabilities://generators")
            gen_data = json.loads(result.contents[0].text)
            self.generators = gen_data["generators"]

            print(f"✅ Discovered {len(self.generators)} generators")

    def validate_credentials(self, generator_type: str):
        """Validate credentials for a generator."""
        if not self.generators:
            raise RuntimeError("Call initialize() first")

        generator = self.generators.get(generator_type)
        if not generator:
            raise ValueError(f"Unknown generator: {generator_type}")

        deps = generator.get("upstream_dependencies")
        if not deps:
            return True  # No dependencies

        missing = []
        for cred in deps["credentials_required"]:
            if not os.getenv(cred):
                missing.append(cred)

        if missing:
            raise ValueError(
                f"Missing credentials for {generator_type}: {', '.join(missing)}\n"
                f"Required: {deps['credentials_required']}"
            )

        return True

    async def generate_content(
        self,
        config_id: str,
        context: dict = None,
        trace_id: str = None
    ):
        """Generate content with automatic trace context."""
        if trace_id is None:
            trace_id = f"req-{uuid.uuid4()}"

        # Set trace context
        os.environ["CHORA_TRACE_ID"] = trace_id

        print(f"🔍 Trace ID: {trace_id}")

        async with ClientSession(self.server_url) as session:
            # Call generate_content
            result = await session.call_tool("generate_content", {
                "config_id": config_id,
                "context": context or {}
            })

            print(f"✅ Content generated")

            return trace_id, result

    async def run_workflow(
        self,
        steps: list[dict],
        trace_id: str = None
    ):
        """Run multi-step workflow with trace correlation."""
        if trace_id is None:
            trace_id = f"workflow-{uuid.uuid4()}"

        os.environ["CHORA_TRACE_ID"] = trace_id

        print(f"🔍 Starting workflow: {trace_id}")
        print(f"   Steps: {len(steps)}\n")

        async with ClientSession(self.server_url) as session:
            for i, step in enumerate(steps, 1):
                tool = step["tool"]
                params = step["params"]

                print(f"Step {i}/{len(steps)}: {tool}...")

                try:
                    result = await session.call_tool(tool, params)
                    print(f"  ✅ Success")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    raise

        print(f"\n✅ Workflow completed: {trace_id}")
        return trace_id

    def parse_events(self, trace_id: str):
        """Parse events for a workflow."""
        events_file = Path("var/telemetry/events.jsonl")

        if not events_file.exists():
            return []

        events = []
        with open(events_file, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                event = json.loads(line)
                if event.get("trace_id") == trace_id:
                    events.append(event)

        return events

    def analyze_workflow(self, trace_id: str):
        """Analyze workflow performance."""
        events = self.parse_events(trace_id)

        print(f"\n📊 Workflow Analysis: {trace_id}")
        print(f"   Total Events: {len(events)}")

        success = sum(1 for e in events if e["status"] == "success")
        errors = sum(1 for e in events if e["status"] == "error")

        print(f"   Success: {success}")
        print(f"   Errors: {errors}")

        total_duration = sum(e.get("duration_ms", 0) for e in events)
        print(f"   Total Duration: {total_duration}ms")

        return events


# Example Usage
async def main():
    """Example gateway usage."""
    gateway = ChoraGateway(server_url="http://localhost:8000")

    # Step 1: Initialize
    await gateway.initialize()

    # Step 2: Validate credentials (if using code_generation)
    try:
        gateway.validate_credentials("code_generation")
        print("✅ Credentials validated")
    except ValueError as e:
        print(f"❌ {e}")
        print("   Using jinja2 fallback instead")

    # Step 3: Run workflow
    trace_id = await gateway.run_workflow([
        {
            "tool": "generate_content",
            "params": {
                "config_id": "readme-intro",
                "context": {"project_name": "my-project"}
            }
        },
        {
            "tool": "generate_content",
            "params": {
                "config_id": "readme-body",
                "context": {"features": ["feature1", "feature2"]}
            }
        },
        {
            "tool": "assemble_artifact",
            "params": {
                "config_id": "readme-full",
                "output_path": "dist/README.md"
            }
        }
    ])

    # Step 4: Analyze events
    gateway.analyze_workflow(trace_id)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Troubleshooting

### Events Not Appearing

**Problem:** `var/telemetry/events.jsonl` doesn't exist or is empty

**Solutions:**
1. Check MCP server is actually calling generators (events only emitted on generation)
2. Verify write permissions on `var/telemetry/` directory
3. Check for errors in MCP server logs

### Missing Trace ID in Events

**Problem:** Events have `trace_id: null`

**Solutions:**
1. Verify `CHORA_TRACE_ID` is set BEFORE starting MCP server
2. Check environment variable propagation to subprocess
3. Set `event.trace_id` explicitly if environment variable approach doesn't work

### Credential Validation Failing

**Problem:** `validate_credentials()` raises "Missing credentials"

**Solutions:**
1. Set required environment variables: `export ANTHROPIC_API_KEY=sk-...`
2. Check `.env` file is loaded: `python-dotenv` integration
3. Verify credentials are in the correct environment (not just shell, but Python process)

### Performance Issues

**Problem:** Generators taking longer than expected latency

**Solutions:**
1. Check `upstream_dependencies.expected_latency_ms` for realistic expectations
2. Verify network connectivity to external services (Anthropic API, etc.)
3. Increase timeout based on p95 latency: `timeout = p95 * 2`

---

## Next Steps

- **Advanced Topics**:
  - [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
  - [Capability Discovery](use-capability-discovery.md) - Deep dive into capabilities
  - [Event Schema Specification](../../../specs/event-schema.md) - Formal event format

- **API Reference**:
  - [UpstreamDependencies Model](../../reference/api/models/upstream-dependencies.md)
  - [Event Schemas](../../reference/api/telemetry/event-schemas.md)
  - [EventEmitter API](../../reference/api/telemetry/event-emitter.md)

---

**Version:** v1.3.0
**Last Updated:** October 17, 2025
**Maintainer:** Chora Compose Team
