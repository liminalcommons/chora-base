# Agent Integration Playbook

**Audience:** Developers building autonomous LLM agents that consume chora-compose
**Purpose:** Understand integration patterns, ecosystem positioning, and architectural decisions

---

## Overview

This document explains how chora-compose fits into multi-repo ecosystems and provides conceptual guidance for building autonomous agents that consume the framework. For step-by-step implementation instructions, see the [LLM Agent Integration Tutorial](../../tutorials/advanced/05-llm-agent-integration.md).

---

## Table of Contents

1. [Integration Philosophy](#integration-philosophy)
2. [Ecosystem Positioning](#ecosystem-positioning)
3. [Integration Contract](#integration-contract)
4. [Agent Patterns](#agent-patterns)
5. [Value Proposition for Consumer Repos](#value-proposition-for-consumer-repos)
6. [Guardrails and Best Practices](#guardrails-and-best-practices)
7. [Machine-Readable Contract](#machine-readable-contract)

---

## Integration Philosophy

### Declarative-First Consumption

Chora-compose is designed to be consumed as a **declarative artifact generation service**. Agents should:

1. **Focus on configs, not code** - Provide validated JSON configurations
2. **Trust the contract** - Rely on schema validation and structured outputs
3. **Emit lifecycle events** - Signal platform gates for orchestration
4. **Fail fast** - Validate early, abort on errors, clean up partial state

**Why this matters:**

Traditional approaches require agents to understand implementation details (templates, generators, rendering engines). Chora-compose abstracts these concerns behind a configuration contract, allowing agents to focus on **what** to generate, not **how**.

### Configuration-Driven Integration

```
Agent Task                        Chora-Compose Contract
┌─────────────────┐              ┌─────────────────────┐
│ Generate report │  ──────────▶ │ Content Config      │
│ for platform    │              │ + Context Data      │
└─────────────────┘              └─────────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────────┐
                                 │ Artifact Generated  │
                                 │ + Run Metadata      │
                                 └─────────────────────┘
```

---

## Ecosystem Positioning

### Where Chora Compose Sits

In multi-repo ecosystems (like chora-workspace), chora-compose occupies the **artifact generation layer**:

```
┌──────────────────────────────────────────────────┐
│ chora-workspace (Coordination Layer)             │
│   ├─ Orchestrates multi-repo workflows           │
│   └─ Defines standards and gates                 │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│ chora-platform (Standards & Discovery)           │
│   ├─ Capability registry                         │
│   ├─ Config schemas                              │
│   └─ Manifest management                         │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│ mcp-orchestration (Workflow Lifecycle)           │
│   ├─ Gate management (DRSO pattern)              │
│   ├─ Event correlation                           │
│   └─ Workflow state machine                      │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│ mcp-n8n (Workflow Automation)                    │
│   ├─ Scheduled triggers                          │
│   ├─ Agent orchestration                         │
│   └─ Service composition                         │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│ chora-compose (Content & Artifact Generation) ◀──┤ You are here
│   ├─ Config validation                           │
│   ├─ Content generation (17 MCP tools)           │
│   ├─ Artifact assembly                           │
│   └─ Run metadata emission                       │
└───────────────────────────────────────────────────┘
```

### What Chora Compose Produces

- **Typed artifacts** - Markdown, BDD scenarios, code, structured text
- **Run manifests** - Metadata about generation (timestamp, files, generator used)
- **Capability descriptors** - MCP resources for agent introspection (`capabilities://`)
- **Event telemetry** - JSONL events for observability and tracing

### What Chora Compose Consumes

- **Configurations** - Content + artifact configs registered in chora-platform
- **Orchestration prompts** - Workflow triggers from mcp-n8n
- **Storage providers** - Ephemeral (default) or custom storage backends
- **Context data** - Variables for template rendering

### Lifecycle Signals

Chora-compose integrates with DRSO (Design-Review-Stage-Operate) gate patterns:

1. **Config validated** → Ready for review
2. **Artifact generated** → Ready for staging
3. **Manifest emitted** → Ready for Ack gate

Agents emit these signals to platform orchestration layers for workflow coordination.

---

## Integration Contract

### Inputs: What You Must Provide

**1. Content Configs**
- JSON files adhering to `schemas/content/v3.1/schema.json`
- Reference templates, generators, and context requirements
- Located in `configs/content/` by convention

Example:
```json
{
  "content_id": "api-docs",
  "format": "markdown",
  "generation": {
    "patterns": [
      {
        "type": "jinja2",
        "template_path": "templates/api-docs.md.j2"
      }
    ]
  }
}
```

**2. Artifact Configs**
- JSON files adhering to `schemas/artifact/v3.1/schema.json`
- Link multiple content configs into composite artifacts
- Define output destinations

Example:
```json
{
  "artifact_id": "documentation-bundle",
  "components": [
    {"content_id": "api-docs"},
    {"content_id": "user-guide"}
  ],
  "output": {
    "directory": "dist/docs"
  }
}
```

**3. Source Materials**
- Template files (`.j2`, `.md.j2`)
- Context data (JSON, environment variables)
- Accessible relative to repo root

### Execution: How You Invoke

**CLI Interface:**
```bash
# Validate config
poetry run chora-compose validate configs/content/api-docs.json

# Generate artifact
poetry run chora-compose compose configs/artifact/documentation-bundle.json
```

**Python API:**
```python
from chora_compose.core.composer import ArtifactComposer
from chora_compose.storage import get_ephemeral_storage_manager

composer = ArtifactComposer(storage=get_ephemeral_storage_manager())
result = composer.compose("configs/artifact/documentation-bundle.json")
```

**MCP Tools (for AI agents):**
```python
# Via MCP client
await mcp_client.call_tool("choracompose:generate_content", {
    "content_config_id": "api-docs",
    "context": {"version": "1.0.0"}
})
```

### Outputs: What You Get Back

**1. Artifact Files**
- Written to configured output directory (default: `dist/`)
- Format depends on config (markdown, JSON, code, etc.)
- Atomic writes (tmp → rename for consistency)

**2. Run Metadata**
- `dist/latest_run_manifest.json` - Contains:
  - Artifact paths
  - Generation timestamp
  - Generator used
  - Content config IDs
  - File hashes (SHA256)

Example:
```json
{
  "artifact_id": "documentation-bundle",
  "timestamp": "2025-10-21T14:30:00Z",
  "artifacts": [
    "dist/docs/api-docs.md",
    "dist/docs/user-guide.md"
  ],
  "generator": "jinja2",
  "duration_ms": 1250,
  "status": "success"
}
```

**3. Event Telemetry (Optional)**
- JSONL events in `var/telemetry/events.jsonl`
- Correlated via `CHORA_TRACE_ID` environment variable
- For observability and debugging

---

## Agent Patterns

### Pattern 1: Bootstrap a New Consumer Repo

**Use case:** Integrate chora-compose into a new repository

**Steps:**
1. Clone both target repo and chora-compose
2. Copy config templates from `dev-docs/templates/`
3. Validate configs with `chora-compose validate`
4. Register manifest snippet with chora-platform
5. Execute compose and verify output

**When to use:**
- Setting up new ecosystem repos
- Initial integration
- Creating config blueprints

**Example:**
```python
def bootstrap_consumer_repo(repo_path: Path):
    """Bootstrap a new repo with chora-compose integration."""
    # Clone chora-compose
    run(["git", "clone", CHORA_COMPOSE_REPO, repo_path / "vendor/chora-compose"])

    # Copy templates
    template_src = repo_path / "vendor/chora-compose/dev-docs/templates"
    config_dest = repo_path / "configs"

    shutil.copytree(template_src, config_dest / "templates")

    # Validate
    run(["poetry", "run", "chora-compose", "validate", config_dest])
```

### Pattern 2: Refresh Existing Artifacts on Schedule

**Use case:** Automated regeneration (nightly builds, scheduled updates)

**Steps:**
1. Pull latest chora-compose tags
2. Re-run validation (check for schema version bumps)
3. Execute artifact generation
4. Capture run metadata
5. Emit change signal via mcp-orchestration

**When to use:**
- Scheduled documentation updates
- Nightly builds
- Automated refreshes

**Example:**
```python
def scheduled_refresh():
    """Nightly artifact refresh workflow."""
    # Pull latest
    run(["git", "-C", "vendor/chora-compose", "pull"])

    # Re-validate (schemas may have changed)
    configs = Path("configs").glob("**/*.json")
    for config in configs:
        run(["poetry", "run", "chora-compose", "validate", config])

    # Generate
    run(["poetry", "run", "chora-compose", "compose", "configs/artifact/main.json"])

    # Emit event
    manifest = json.loads(Path("dist/latest_run_manifest.json").read_text())
    emit_platform_event("artifact-refreshed", manifest)
```

### Pattern 3: Extend Generator Capabilities

**Use case:** Add custom generators for specialized content types

**Steps:**
1. Inspect existing generators in `src/chora_compose/generators/`
2. Implement new generator following `BaseGenerator` contract
3. Add schema extension if needed
4. Update documentation
5. Publish release notes

**When to use:**
- Custom content types (diagrams, DSLs, proprietary formats)
- Organization-specific patterns
- Experimental generators

**Example:**
```python
from chora_compose.generators.base import BaseGenerator

class DiagramGenerator(BaseGenerator):
    """Generate Mermaid diagrams from structured data."""

    def generate(self, config: ContentConfig, context: dict) -> str:
        # Implementation
        nodes = context.get("nodes", [])
        edges = context.get("edges", [])

        diagram = "graph TD\n"
        for node in nodes:
            diagram += f"  {node['id']}[{node['label']}]\n"
        for edge in edges:
            diagram += f"  {edge['from']} --> {edge['to']}\n"

        return diagram
```

### Pattern 4: Batch Processing Multiple Artifacts

**Use case:** Generate many artifacts in parallel

**Steps:**
1. Collect artifact configs
2. Validate all configs first (fail fast)
3. Generate in parallel (threading/multiprocessing)
4. Aggregate results
5. Emit batch completion event

**When to use:**
- Large documentation sets
- Multi-artifact releases
- Performance-critical workflows

**Example:**
```python
from concurrent.futures import ThreadPoolExecutor

def batch_generate(artifact_configs: list[Path]) -> list[dict]:
    """Generate multiple artifacts in parallel."""
    # Validate all first
    for config in artifact_configs:
        validate_config(config)

    # Generate in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(generate_artifact, config)
            for config in artifact_configs
        ]
        results = [f.result() for f in futures]

    return results
```

---

## Value Proposition for Consumer Repos

### 1. Declarative-First Development

**Problem:** Ad hoc scripting leads to inconsistent output and hard-to-maintain generation logic.

**Solution:** Configs as the source of truth. Scripts consume configs, not vice versa.

**Benefit:**
- Configs are versionable, reviewable, and testable
- Changes to generation logic don't require script rewrites
- New team members understand "what" without learning "how"

### 2. Composable Pipeline

**Problem:** Monolithic generation scripts mix concerns (content creation, assembly, output).

**Solution:** Separate content fragments (`configs/content/`) from artifact assembly (`configs/artifact/`).

**Benefit:**
- Reuse content across multiple artifacts
- Mix and match components
- Independent evolution of content and assembly logic

### 3. Validated Contracts

**Problem:** Schema drift between producer and consumer.

**Solution:** Versioned JSON schemas at `schemas/content/v3.1` and `schemas/artifact/v3.1`.

**Benefit:**
- Pre-flight validation catches errors early
- Breaking changes are explicit (schema version bump)
- Agents can introspect capabilities programmatically

### 4. Generator Hub

**Problem:** Reinventing generation logic for each content type.

**Solution:** Registry of battle-tested generators (Jinja2, Demonstration, BDD, Code Generation, Template Fill).

**Benefit:**
- Leverage proven patterns
- Focus on content, not rendering
- Extend with custom generators as needed

### 5. Workflow Ready

**Problem:** Generated artifacts lack metadata for downstream workflows.

**Solution:** Structured run manifests and event telemetry.

**Benefit:**
- Platform gates can verify artifacts were generated
- Observability for debugging failed runs
- Audit trail for compliance

---

## Guardrails and Best Practices

### Pre-Execution Checklist

Before invoking chora-compose, verify:

- ✅ **Schema validation passes** - Use `chora-compose validate`
- ✅ **Source resolution succeeds** - Templates and data are accessible
- ✅ **Storage writable** - Output directory has write permissions
- ✅ **Tests updated** - If generator behavior changes, update tests
- ✅ **Telemetry hooks configured** - Platform notified on success/failure

**If any condition fails, abort and raise an alert.**

### Error Handling Patterns

**1. Fail Fast**
```python
# Validate all configs before generating any artifacts
for config in configs:
    if not validate_config(config):
        raise ConfigValidationError(config)

# Now generate (all validated)
for config in configs:
    generate_artifact(config)
```

**2. Retry with Backoff**
```python
@retry(max_attempts=3, backoff=exponential)
def generate_artifact(config):
    return run_compose(config)
```

**3. Cleanup on Failure**
```python
try:
    result = generate_artifact(config)
except Exception:
    cleanup_partial_artifacts()
    raise
```

### Observability Recommendations

**1. Structured Logging**
```python
logger.info("artifact_generation_started", extra={
    "artifact_id": artifact_id,
    "trace_id": trace_id,
    "timestamp": datetime.now().isoformat()
})
```

**2. Trace Context Propagation**
```python
import os

trace_id = generate_trace_id()
os.environ["CHORA_TRACE_ID"] = trace_id

# Chora-compose will emit events with this trace_id
compose(artifact_config)
```

**3. Event Correlation**
```python
# Read telemetry events
events = read_jsonl("var/telemetry/events.jsonl")

# Filter by trace ID
run_events = [e for e in events if e["trace_id"] == trace_id]
```

---

## Machine-Readable Contract

For programmatic consumption, use this YAML specification:

```yaml
chora_compose_integration:
  version: 1.1.0
  persona: autonomous_llm_agent

  inputs:
    content_config_schema:
      path: schemas/content/v3.1/schema.json
      version: "3.1"
    artifact_config_schema:
      path: schemas/artifact/v3.1/schema.json
      version: "3.1"
    storage_manager:
      default: chora_compose.storage.ephemeral.EphemeralStorageManager
      interface: chora_compose.storage.base.BaseStorageManager

  entrypoints:
    cli:
      command: poetry run chora-compose compose <artifact-config>
      validate: poetry run chora-compose validate <config>
    python_api:
      module: chora_compose.core.composer
      class: ArtifactComposer
      method: compose(artifact_config_path)
    mcp_tools:
      namespace: chora
      tools:
        - generate_content
        - validate_content
        - list_content_configs
        - compose_artifact

  outputs:
    artifacts:
      directory: dist/
      naming: "{{ artifact_id }}.{{ format }}"
    manifest:
      path: dist/latest_run_manifest.json
      schema:
        artifact_id: string
        timestamp: ISO8601
        artifacts: list[string]
        generator: string
        duration_ms: integer
        status: enum[success, failed]
    telemetry:
      events_file: var/telemetry/events.jsonl
      format: JSONL
      correlation: CHORA_TRACE_ID environment variable

  dependencies:
    coordinating_repos:
      - chora-platform        # Standards and schemas
      - mcp-orchestration     # Workflow lifecycle
      - mcp-n8n               # Automation

  verification_steps:
    - validate_schemas      # Pre-flight check
    - dry_run_preview       # Optional: test without side effects
    - compose_execute       # Generate artifacts
    - verify_output         # Check artifacts exist
    - emit_ack_signal       # Notify platform gate

  lifecycle_gates:
    - gate: config-validated
      signal: validation_passed
      payload: {config_id, schema_version}

    - gate: artifact-generated
      signal: generation_complete
      payload: {artifact_id, manifest_path}

    - gate: ready-for-deployment
      signal: verification_passed
      payload: {manifest, artifact_hashes}
```

---

## Related Documentation

### Tutorials
- [LLM Agent Integration](../../tutorials/advanced/05-llm-agent-integration.md) - Step-by-step implementation
- [MCP Integration Deep Dive](../../tutorials/advanced/01-mcp-integration-deep-dive.md) - MCP protocol details
- [Agentic Workflow](../../tutorials/advanced/02-agentic-workflow.md) - End-to-end workflows

### How-To Guides
- [Generate Content](../../how-to/generation/generate-content.md) - Generation basics
- [Validate Configs](../../how-to/configs/validate-configs.md) - Validation procedures
- [Use MCP Tools](../../how-to/mcp/use-mcp-tools.md) - MCP tool reference

### Explanation
- [Position in AI Tooling](position-in-ai-tooling.md) - Ecosystem context
- [Integration with Orchestration](integration-with-orchestration.md) - Gateway patterns
- [MCP Workflow Model](../integration/mcp-workflow-model.md) - MCP philosophy

### Reference
- [MCP Tool Reference](../../reference/mcp/tool-reference.md) - 17 MCP tools
- [Capabilities Discovery](../../reference/api/resources/capabilities.md) - Introspection patterns
