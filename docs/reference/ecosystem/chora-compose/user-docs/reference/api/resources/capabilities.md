# MCP Capabilities Resources

**Version:** v1.2.0
**Category:** Discovery & Introspection
**Status:** Stable
**Last Updated:** October 16, 2025

---

## Overview

The `capabilities://` resource family provides **structured discovery** of MCP server features, enabling LLM agents to introspect and self-configure without hardcoded knowledge.

### Available Capabilities

| URI Pattern | Purpose | Response Time |
|-------------|---------|---------------|
| `capabilities://server` | Server metadata, features, limits, runtime | <50ms |
| `capabilities://tools` | Tool inventory with complete schemas | <100ms |
| `capabilities://resources` | Resource URI catalog with parameters | <50ms |
| `capabilities://generators` | Generator registry with selection metadata | <50ms |

### Design Principles

1. **Self-Describing**: Resources include complete metadata for autonomous discovery
2. **Version-Aware**: Each capability reports version compatibility
3. **Plugin-Aware**: Automatically reflects dynamically registered components
4. **MCP-Aligned**: Follows Model Context Protocol discovery patterns

---

## Agent Self-Configuration Pattern

### Discovery Workflow

```
1. Fetch capabilities://server
   → Understand version, features, operational limits

2. Fetch capabilities://tools
   → Discover what operations are available
   → Review input/output schemas

3. Fetch capabilities://generators (if generating content)
   → Understand generator selection logic
   → Check requirements (API keys, dependencies)

4. Fetch capabilities://resources
   → Learn what data URIs to access
   → Understand URI parameters

5. Execute operations
   → Use discovered schemas to construct valid requests
```

### Example: Agent Creates Config Without Prior Knowledge

**Scenario**: Agent has never used chora-compose before

```
Agent: Let me discover what this server can do
→ Fetches capabilities://server
→ Sees "config_lifecycle": true feature flag

Agent: What tools are available for config creation?
→ Fetches capabilities://tools
→ Finds draft_config in "config" category
→ Reviews input_schema to understand parameters

Agent: How do I select a generator?
→ Fetches capabilities://generators
→ Learns jinja2 requires template field
→ Sees indicators for automatic selection

Agent: Now I can create a config
→ Uses draft_config with correct schema
→ No hardcoded knowledge needed!
```

---

## API Reference

### capabilities://server

**Purpose:** Server-level metadata and feature discovery

**MIME Type:** `application/json`

**Parameters:** None

**Response Schema:**

```typescript
{
  name: string;              // Server name ("chora-compose")
  version: string;           // Semver version ("1.2.0")
  mcp_version: string;       // MCP protocol version ("1.0")
  features: {
    [feature_name: string]: boolean;  // Feature flags
  };
  limits: {
    [limit_name: string]: number;     // Operational limits
  };
  runtime: {
    python: string;          // Python version ("3.12.x")
    fastmcp: string;         // FastMCP version
    platform: string;        // OS platform ("darwin", "linux", etc.)
  };
  tool_count: number;        // Total MCP tools available
  resource_count: number;    // Total resource URI patterns
  generator_count: number;   // Registered generators (builtin + plugin)
}
```

**Example Response:**

```json
{
  "name": "chora-compose",
  "version": "1.2.0",
  "mcp_version": "1.0",
  "features": {
    "content_generation": true,
    "artifact_assembly": true,
    "config_lifecycle": true,
    "batch_operations": true,
    "ephemeral_storage": true,
    "resource_providers": true,
    "generator_plugins": true,
    "capability_discovery": true,
    "validation_suggestions": false
  },
  "limits": {
    "max_content_size_bytes": 10000000,
    "max_artifact_components": 100,
    "ephemeral_retention_days": 30,
    "max_batch_size": 50
  },
  "runtime": {
    "python": "3.12.10",
    "fastmcp": "2.12.4",
    "platform": "darwin"
  },
  "tool_count": 17,
  "resource_count": 5,
  "generator_count": 5
}
```

**Feature Flags:**

| Flag | v1.0.0 | v1.2.0 | Description |
|------|--------|--------|-------------|
| content_generation | ✅ | ✅ | Core content generation tools |
| artifact_assembly | ✅ | ✅ | Artifact assembly from multiple content pieces |
| config_lifecycle | ❌ | ✅ | Conversational config authoring (NEW) |
| batch_operations | ✅ | ✅ | Parallel generation operations |
| ephemeral_storage | ✅ | ✅ | Temporary content storage |
| resource_providers | ✅ | ✅ | MCP resource URIs |
| generator_plugins | ✅ | ✅ | Dynamic generator registration |
| capability_discovery | ❌ | ✅ | capabilities:// resources (NEW) |
| validation_suggestions | ❌ | ❌ | Removed (was incomplete in v1.0.1) |

**Use Cases:**

- Check version compatibility before using features
- Understand operational limits for batch operations
- Verify runtime environment meets requirements
- Discover new features across versions

---

### capabilities://tools

**Purpose:** Complete tool inventory with schemas and usage patterns

**MIME Type:** `application/json`

**Parameters:** None

**Response Schema:**

```typescript
{
  tools_by_category: {
    [category: string]: Array<{
      name: string;
      category: "content" | "artifact" | "config" | "storage" | "query" | "validation" | "batch";
      description: string;
      version: string;
      input_schema: object;       // Pydantic JSON Schema
      output_schema: object;      // Pydantic JSON Schema
      examples: Array<{
        input?: object;
        description: string;
      }>;
      common_errors: Array<{
        code: string;
        message: string;
      }>;
      performance: {
        typical_ms: string;       // e.g., "500-2000"
        timeout_ms: string;       // e.g., "30000"
      };
    }>;
  };
  metadata: {
    total_count: number;
    version: string;
  };
}
```

**Tool Categories:**

- **content** - Content generation (generate_content, regenerate_content, preview_generation)
- **artifact** - Artifact assembly (assemble_artifact)
- **config** - Config lifecycle (draft_config, test_config, save_config, modify_config)
- **storage** - Storage management (query_ephemeral_storage, cleanup_ephemeral)
- **query** - Discovery (list_generators, list_content, list_artifacts)
- **validation** - Validation (validate_content)
- **batch** - Batch operations (batch_generate_content)

**Use Cases:**

- Discover what operations are supported
- Understand tool input/output schemas
- Find examples for common workflows
- Anticipate and handle common errors
- Estimate operation duration

---

### capabilities://resources

**Purpose:** Resource URI catalog with parameters and examples

**MIME Type:** `application/json`

**Parameters:** None

**Response Schema:**

```typescript
{
  resources: {
    [resource_family: string]: {
      patterns: string[];           // URI patterns
      mime_type: string;           // Response MIME type
      description: string;         // What this resource provides
      parameters: {
        [param_name: string]: {
          type: string;
          description: string;
          enum?: string[];         // Valid values if constrained
        };
      };
      examples: string[];          // Example URIs
    };
  };
  metadata: {
    total_count: number;
    version: string;
  };
}
```

**Resource Families:**

1. **config** - Configuration files
   - `config://artifact/{artifact_id}`
   - `config://content/{content_id}`

2. **schema** - JSON Schema definitions
   - `schema://{schema_name}`

3. **content** - Generated content from storage
   - `content://{content_id}`
   - `content://{content_id}/{version_id}`

4. **generator** - Generator metadata
   - `generator://{generator_type}`

5. **capabilities** - Capability discovery (self-referential)
   - `capabilities://{capability_type}`

**Use Cases:**

- Learn what data URIs are available
- Understand URI parameter requirements
- Construct valid resource requests
- Discover MIME types for parsing

---

### capabilities://generators

**Purpose:** Generator registry with selection metadata

**MIME Type:** `application/json`

**Parameters:** None

**Response Schema:**

```typescript
{
  generators: {
    [generator_type: string]: {
      type: string;
      name: string;                    // Class name
      version: string;
      source: "builtin" | "plugin";
      plugin_path?: string;            // If source=plugin
      status: "stable" | "experimental" | "deprecated";
      capabilities: string[];          // e.g., ["templates", "loops"]
      indicators: {
        config_field?: string;         // Field to check
        config_values?: string[];      // Expected values
        template_patterns?: string[];  // Syntax patterns
        confidence: "high" | "medium" | "low";
      };
      requirements: {
        fields: string[];              // Required config fields
        dependencies: string[];        // Python package dependencies
        env_vars: string[];            // Required environment variables
      };
      best_for: string[];              // Ideal use cases
      docs_uri: string;                // Documentation link
      upstream_dependencies: {         // v1.3.0+: Gateway integration
        services: string[];            // External services (e.g., ["anthropic"])
        credentials_required: string[];// Required env vars (e.g., ["ANTHROPIC_API_KEY"])
        optional_services: string[];   // Optional services
        expected_latency_ms: {         // Performance expectations
          p50?: number;                // 50th percentile latency (ms)
          p95?: number;                // 95th percentile latency (ms)
        };
        stability: "stable" | "beta" | "experimental";
        concurrency_safe: boolean;     // Safe for concurrent execution
      } | null;
    };
  };
  selection_strategy: {
    type: string;
    explanation: string;
    fallback: string;                  // Default generator
  };
  metadata: {
    version: string;
    generator_count: number;
    builtin_count: number;
    plugin_count: number;
  };
}
```

**Generator Selection Logic:**

1. **Explicit Type** (highest priority)
   - Check `generation.patterns[0].type` field
   - If matches generator type → use it (high confidence)

2. **Template Syntax Detection**
   - Jinja2: Contains `{{` or `{%` → jinja2
   - Template Fill: Contains `{{` but NOT `{%` → template_fill

3. **Structural Patterns**
   - Demonstration: Has `elements[].example_output` → demonstration

4. **Fallback**
   - If no matches → use jinja2 (most versatile)

**Use Cases:**

- Intelligent generator selection for configs
- Understanding generator capabilities
- Checking requirements (API keys, dependencies)
- Discovering plugin generators
- Learning best practices for each generator

**Example - Code Generation Requirements:**

```json
{
  "type": "code_generation",
  "requirements": {
    "fields": ["generation.patterns[0].specification"],
    "dependencies": ["anthropic"],
    "env_vars": ["ANTHROPIC_API_KEY"]
  },
  "upstream_dependencies": {
    "services": ["anthropic"],
    "credentials_required": ["ANTHROPIC_API_KEY"],
    "optional_services": [],
    "expected_latency_ms": {
      "p50": 1500,
      "p95": 5000
    },
    "stability": "stable",
    "concurrency_safe": true
  }
}
```

**Gateway Pre-flight Validation (v1.3.0+):**

```python
# Gateway reads generator dependencies
deps = generator["upstream_dependencies"]

if deps:
    # Check credentials before calling generator
    for cred in deps["credentials_required"]:
        if not os.getenv(cred):
            return error(f"Missing credential: {cred}")

    # Set timeout based on expected latency
    timeout = deps["expected_latency_ms"].get("p95", 5000) * 2

    # Check if concurrent execution is safe
    if deps["concurrency_safe"]:
        # Can run multiple generations in parallel
        await asyncio.gather(*generation_tasks)
```

Agent can check:
1. Config has `specification` field? ✓
2. `anthropic` package installed? ✓
3. `ANTHROPIC_API_KEY` set? → Check before using (via upstream_dependencies)
4. Expected latency? → Set appropriate timeout (1.5s p50, 5s p95)

---

## Replaces: generator://decision_tree

The `capabilities://generators` resource **replaces** the narrow `generator://decision_tree` resource from v1.0.x with a more comprehensive pattern:

### Migration Guide

**Before (v1.0.x):**
```
Read generator://decision_tree
→ Get hardcoded priority array
→ Manually evaluate conditions
```

**After (v1.2.0):**
```
Read capabilities://generators
→ Get live registry (includes plugins!)
→ Structured indicators (easier to evaluate)
→ Requirements clearly documented
→ Best practices included
```

### Key Improvements

1. **Live Registry**: Reflects current state, includes plugins
2. **Structured Indicators**: Dict format vs priority array
3. **Comprehensive Metadata**: capabilities, requirements, best_for
4. **Plugin-Aware**: Automatically includes dynamically registered generators
5. **Extensible Pattern**: Can add capabilities://validators, etc.

---

## Performance

All capability resources are optimized for fast response:

| Resource | Target | Typical | Caching |
|----------|--------|---------|---------|
| capabilities://server | <50ms | 10-30ms | No (dynamic counts) |
| capabilities://tools | <100ms | 40-80ms | Yes (static schemas) |
| capabilities://resources | <50ms | 10-30ms | Yes (static patterns) |
| capabilities://generators | <50ms | 15-35ms | No (live registry) |

**Note**: `capabilities://generators` is NOT cached because it reflects the live GeneratorRegistry state (plugins can be added at runtime).

---

## Error Handling

All capability resources return valid JSON or raise standard MCP errors:

**Possible Errors:**

- `resource_not_found` (404) - Invalid capability_type
- `server_error` (500) - Internal error generating capability data

**Best Practice:**

```python
try:
    server_caps = await fetch("capabilities://server")
    if server_caps["features"]["config_lifecycle"]:
        # Use config lifecycle tools
        ...
except ResourceNotFound:
    # Fall back to basic tools
    ...
```

---

## Version Compatibility

### v1.2.0+ (Current)

All 4 capability resources available:
- ✅ capabilities://server
- ✅ capabilities://tools
- ✅ capabilities://resources
- ✅ capabilities://generators

### v1.0.x (Legacy)

Only decision tree available:
- ⚠️ generator://decision_tree (deprecated)

**Migration**: Update resource URIs from `generator://decision_tree` to `capabilities://generators`

---

## Related

- **Tools**: All 17 MCP tools discoverable via `capabilities://tools`
- **Resources**: All resource URIs documented in `capabilities://resources`
- **E2E Tests**: [E2E_RESOURCES.md](../../mcp/E2E_RESOURCES.md) - Comprehensive testing guide
- **Generators**: [Generator Registry](../core/generator-registry.md) - Plugin system

---

## Examples

### Example 1: Feature Detection

```python
# Check if server supports config lifecycle tools
server_caps = await fetch("capabilities://server")

if server_caps["features"]["config_lifecycle"]:
    # Use draft_config, test_config, etc.
    result = await call_tool("draft_config", {...})
else:
    # Fall back to manual config creation
    ...
```

### Example 2: Schema-Driven Tool Use

```python
# Discover tool schema without hardcoding
tools = await fetch("capabilities://tools")

generate_content = next(
    tool for category in tools["tools_by_category"].values()
    for tool in category
    if tool["name"] == "generate_content"
)

# Use schema to validate input
input_schema = generate_content["input_schema"]
# ... validate against schema ...

# Call tool with confidence
result = await call_tool("generate_content", validated_input)
```

### Example 3: Generator Selection

```python
# Intelligent generator selection
generators = await fetch("capabilities://generators")

def select_generator(config):
    # Check explicit type first
    if config.get("generation", {}).get("patterns", [{}])[0].get("type"):
        return config["generation"]["patterns"][0]["type"]

    # Check template syntax
    template = config.get("generation", {}).get("patterns", [{}])[0].get("template", "")
    if "{{" in template and "{%" in template:
        return "jinja2"
    elif "{{" in template:
        return "template_fill"

    # Check for demonstration pattern
    if config.get("elements", [{}])[0].get("example_output"):
        return "demonstration"

    # Fallback
    return generators["selection_strategy"]["fallback"]
```

---

## Changelog

### v1.2.0 (2025-10-16)
- Initial release of capabilities:// resources
- Replaces generator://decision_tree with enhanced pattern
- Added 4 capability resources for complete discovery
- Plugin-aware generator registry
- Version-aware feature flags

---

**See Also:**
- [E2E Resource Testing](../../mcp/E2E_RESOURCES.md)
- [MCP Tools Reference](../../mcp/tool-reference.md)
- [Generator Registry](../core/generator-registry.md)
