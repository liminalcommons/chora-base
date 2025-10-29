# UpstreamDependencies Model

**Version:** v1.3.0
**Category:** Models
**Status:** Stable
**Last Updated:** October 17, 2025

---

## Overview

The `UpstreamDependencies` model captures external service requirements and operational metadata for generators, enabling gateways to perform pre-flight validation and make intelligent routing decisions.

### Purpose

- **Pre-flight Validation**: Gateways can verify credentials exist before calling generators
- **Intelligent Routing**: Route requests based on service availability
- **Error Prevention**: Better error messages for missing credentials
- **Discovery**: Expose what services each generator requires
- **Timeout Configuration**: Set appropriate timeouts based on expected latency

### Use Cases

1. **Gateway Pre-validation**:
   ```python
   # Gateway reads generator dependencies
   deps = capabilities["generators"]["code_generation"]["upstream_dependencies"]

   # Check credentials before calling
   if "ANTHROPIC_API_KEY" in deps["credentials_required"]:
       if not os.getenv("ANTHROPIC_API_KEY"):
           return error("Missing ANTHROPIC_API_KEY")
   ```

2. **Automatic Timeout Configuration**:
   ```python
   # Set timeout based on expected latency
   p95_latency = deps["expected_latency_ms"]["p95"]
   timeout = p95_latency * 2  # 2x p95 for safety
   ```

3. **Concurrency Control**:
   ```python
   # Only run concurrent if safe
   if deps["concurrency_safe"]:
       asyncio.gather(*tasks)
   else:
       for task in tasks:
           await task  # Sequential execution
   ```

---

## API Reference

### Model Schema

**Source:** `src/chora_compose/models/upstream_dependencies.py`

```python
from typing import Literal
from pydantic import BaseModel, Field

class UpstreamDependencies(BaseModel):
    services: list[str]
    credentials_required: list[str]
    optional_services: list[str] = []
    expected_latency_ms: dict[str, int] = {}
    stability: Literal["stable", "beta", "experimental"] = "stable"
    concurrency_safe: bool = True
```

---

### Field Reference

#### `services`

**Type:** `list[str]`
**Required:** Yes
**Default:** `[]` (empty list)

External services required by the generator (e.g., "anthropic", "openai", "github").

**Examples:**
- `["anthropic"]` - Requires Anthropic API
- `["openai", "github"]` - Requires both OpenAI and GitHub APIs
- `[]` - No external services (local generator)

**Common Values:**
- `"anthropic"` - Anthropic Claude API
- `"openai"` - OpenAI GPT API
- `"github"` - GitHub API
- `"gitlab"` - GitLab API
- Custom service names for plugin generators

---

#### `credentials_required`

**Type:** `list[str]`
**Required:** Yes
**Default:** `[]` (empty list)

Environment variables that must be set for the generator to function.

**Examples:**
- `["ANTHROPIC_API_KEY"]` - Requires API key in environment
- `["OPENAI_API_KEY", "GITHUB_TOKEN"]` - Requires both
- `[]` - No credentials needed

**Naming Convention:**
- Use uppercase with underscores: `SERVICE_API_KEY`
- Match standard environment variable names
- Document in generator's README if custom

---

#### `optional_services`

**Type:** `list[str]`
**Required:** No
**Default:** `[]` (empty list)

Services that enhance functionality but aren't strictly required.

**Examples:**
- `["anthropic"]` - Falls back to template if API unavailable
- `["redis"]` - Caching optional but improves performance
- `[]` - No optional services

**Use Case:**
```python
# Generator can work without optional service
if "redis" in deps["optional_services"]:
    cache = connect_redis()  # Try to use cache
else:
    cache = None  # No cache, still works
```

---

#### `expected_latency_ms`

**Type:** `dict[str, int]`
**Required:** No
**Default:** `{}` (empty dict)

Expected latency percentiles in milliseconds for API-dependent generators.

**Structure:**
```python
{
    "p50": int,  # 50th percentile (median)
    "p95": int,  # 95th percentile
    "p99": int   # 99th percentile (optional)
}
```

**Examples:**
- `{"p50": 1500, "p95": 5000}` - Claude API (Anthropic)
- `{"p50": 500, "p95": 2000}` - Fast template rendering
- `{}` - Local generator (latency negligible)

**Usage:**
- Gateway timeout configuration
- SLA monitoring
- Performance expectations

---

#### `stability`

**Type:** `Literal["stable", "beta", "experimental"]`
**Required:** No
**Default:** `"stable"`

Stability level of the external service integration.

**Values:**
- `"stable"` - Production-ready, well-tested
- `"beta"` - Functional but may have issues
- `"experimental"` - Unstable, may change

**Examples:**
- `"stable"` - Anthropic API (established, documented)
- `"beta"` - New API with limited testing
- `"experimental"` - Proof-of-concept integration

---

#### `concurrency_safe`

**Type:** `bool`
**Required:** No
**Default:** `True`

Whether the generator can safely be called concurrently.

**Values:**
- `True` - Safe for concurrent execution (stateless, thread-safe)
- `False` - Must be called sequentially (stateful, not thread-safe)

**Examples:**
- `True` - Stateless generators (jinja2, demonstration)
- `True` - API generators with concurrent request support
- `False` - Generators with shared mutable state

---

## Examples

### Local Generator (No Dependencies)

```python
from chora_compose.models import UpstreamDependencies

# Jinja2 generator - pure local template rendering
dependencies = UpstreamDependencies(
    services=[],  # No external services
    credentials_required=[],  # No API keys needed
    concurrency_safe=True,  # Pure function, thread-safe
    stability="stable"
)
```

### API-Dependent Generator

```python
# Code generation with Anthropic Claude
dependencies = UpstreamDependencies(
    services=["anthropic"],
    credentials_required=["ANTHROPIC_API_KEY"],
    expected_latency_ms={"p50": 1500, "p95": 5000},
    stability="stable",
    concurrency_safe=True  # API supports concurrent requests
)
```

### Generator with Fallback

```python
# Tries AI, falls back to template
dependencies = UpstreamDependencies(
    services=[],  # No required services
    credentials_required=[],  # No required credentials
    optional_services=["anthropic"],  # AI enhancement optional
    concurrency_safe=True,
    stability="stable"
)
```

### Experimental Integration

```python
# New GitHub API integration (unstable)
dependencies = UpstreamDependencies(
    services=["github"],
    credentials_required=["GITHUB_TOKEN"],
    expected_latency_ms={"p50": 800, "p95": 2500},
    stability="experimental",  # Warning: may change
    concurrency_safe=True
)
```

---

## Discovery via MCP

Generators expose their `UpstreamDependencies` via the `capabilities://generators` MCP resource.

### Query Example

```python
# MCP client reads generator dependencies
from mcp import ClientSession

async with ClientSession(server_url) as session:
    result = await session.read_resource("capabilities://generators")
    generators = result["generators"]

    # Check code_generation dependencies
    code_gen = generators["code_generation"]
    deps = code_gen["upstream_dependencies"]

    print(f"Services: {deps['services']}")  # ['anthropic']
    print(f"Credentials: {deps['credentials_required']}")  # ['ANTHROPIC_API_KEY']
```

### Response Structure

```json
{
  "generators": {
    "code_generation": {
      "type": "code_generation",
      "name": "CodeGenerationGenerator",
      "upstream_dependencies": {
        "services": ["anthropic"],
        "credentials_required": ["ANTHROPIC_API_KEY"],
        "optional_services": [],
        "expected_latency_ms": {"p50": 1500, "p95": 5000},
        "stability": "stable",
        "concurrency_safe": true
      }
    },
    "jinja2": {
      "type": "jinja2",
      "name": "Jinja2Generator",
      "upstream_dependencies": {
        "services": [],
        "credentials_required": [],
        "optional_services": [],
        "expected_latency_ms": {},
        "stability": "stable",
        "concurrency_safe": true
      }
    }
  }
}
```

---

## Validation Rules

### Field Constraints

1. **services**: Must be non-empty if credentials_required is non-empty
2. **credentials_required**: Environment variable names (uppercase, underscores)
3. **expected_latency_ms**: Values must be positive integers, p95 ≥ p50
4. **stability**: Must be one of: "stable", "beta", "experimental"
5. **concurrency_safe**: Boolean only

### Pydantic Validation

```python
# Automatic validation when creating instance
try:
    deps = UpstreamDependencies(
        services=["anthropic"],
        credentials_required=[],  # Invalid: services without credentials
        stability="unstable"  # Invalid: not a valid Literal value
    )
except ValidationError as e:
    print(e.errors())
```

---

## Migration Guide

### Adding Dependencies to Custom Generators

```python
from chora_compose.generators.base import GeneratorStrategy
from chora_compose.models import UpstreamDependencies

class MyCustomGenerator(GeneratorStrategy):
    def __init__(self):
        # Add upstream_dependencies in __init__
        self.upstream_dependencies = UpstreamDependencies(
            services=["custom-api"],
            credentials_required=["CUSTOM_API_KEY"],
            expected_latency_ms={"p50": 1000, "p95": 3000},
            stability="beta",  # Mark as beta if new
            concurrency_safe=True
        )

    def generate(self, config, context=None):
        # Generator implementation
        pass
```

### Backward Compatibility

- **v1.0.x**: Generators without `upstream_dependencies` attribute
- **v1.1.x**: Generators with `upstream_dependencies` (optional)
- **v1.2.x+**: All generators MUST have `upstream_dependencies`

Gateways should handle `None` gracefully:

```python
deps = generator.get("upstream_dependencies")
if deps is None:
    # Legacy generator - assume no dependencies
    deps = {
        "services": [],
        "credentials_required": [],
        "concurrency_safe": True,
        "stability": "stable"
    }
```

---

## Related Documentation

- [Capabilities Resource API](../resources/capabilities.md) - How dependencies are exposed
- [Generator Strategy Pattern](../../../explanation/architecture/generator-strategy-pattern.md) - Generator architecture
- [Gateway Integration Guide](../../../how-to/mcp/use-with-gateway.md) - Using dependencies in gateways
- [Event Schema](../../../../specs/event-schema.md) - Related telemetry features

---

**Version:** v1.3.0
**Last Updated:** October 17, 2025
**Maintainer:** Chora Compose Team
