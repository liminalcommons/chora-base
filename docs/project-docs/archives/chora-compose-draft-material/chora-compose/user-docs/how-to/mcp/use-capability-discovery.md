# How-To: Use Capability Discovery

**Goal:** Learn how to use the `capabilities://` resources for dynamic server introspection and agent self-configuration.

**Prerequisites:**
- Chora Compose v1.2.0+ installed
- Claude Desktop or other MCP client configured
- Basic understanding of MCP resources

**Time:** 15-20 minutes

---

## Overview

Capability discovery enables AI agents to **dynamically learn** what a server can do, rather than relying on hardcoded knowledge. This makes agents:

- **Version-aware**: Adapt to server updates automatically
- **Plugin-aware**: Detect and use custom generators
- **Self-configuring**: Determine available operations without pre-programming
- **Robust**: Work across different server versions

---

## Quick Reference

### Capability Resources (5)

| URI | Purpose | Response Time |
|-----|---------|---------------|
| `capabilities://server` | Server metadata, features, limits | <50ms |
| `capabilities://tools` | Complete tool inventory with schemas | <100ms |
| `capabilities://resources` | Resource URI catalog | <50ms |
| `capabilities://generators` | Generator registry with selection metadata | <50ms |
| `capabilities://` | Overview of all capabilities (summary) | <50ms |

---

## Task 1: Query Server Metadata

**Use Case:** Determine server version and available features before executing operations.

### Using Claude Desktop

**You:**
```
Query the chora-compose server to find its version and available features
```

**Expected Response:**
```
Claude: The chora-compose server reports:

Version: 1.2.0
Protocol: MCP 1.0

Available Features:
✅ conversational_workflow_authoring
✅ batch_generation
✅ capability_discovery
✅ plugin_generators
✅ ephemeral_storage

Operational Limits:
- Max batch size: 10 items
- Draft retention: 30 days
- Max content size: 100 MB
- Max artifact children: 50

The server has all v1.2.0 features enabled.
```

---

### Direct MCP Resource Access

**Request:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "capabilities://server"
  }
}
```

**Response:**
```json
{
  "contents": [{
    "uri": "capabilities://server",
    "mimeType": "application/json",
    "text": "{
      \"server_name\": \"chora-compose\",
      \"server_version\": \"1.2.0\",
      \"protocol_version\": \"1.0\",
      \"features\": {
        \"conversational_workflow_authoring\": true,
        \"batch_generation\": true,
        \"capability_discovery\": true,
        \"plugin_generators\": true,
        \"ephemeral_storage\": true
      },
      \"limits\": {
        \"max_batch_size\": 10,
        \"draft_retention_days\": 30,
        \"max_content_size_mb\": 100,
        \"max_artifact_children\": 50
      },
      \"runtime\": {
        \"python_version\": \"3.12.0\",
        \"platform\": \"darwin\"
      }
    }"
  }]
}
```

---

### Interpreting Server Metadata

**Version Checking:**
```python
# Agent pseudo-code
server_info = fetch("capabilities://server")

if server_info["server_version"] >= "1.2.0":
    # Use config lifecycle tools
    use_draft_config()
else:
    # Fallback to file-based workflow
    suggest_manual_config()
```

**Feature Detection:**
```python
features = server_info["features"]

if features["batch_generation"]:
    # Use batch operations for performance
    batch_generate(items)
else:
    # Sequential generation
    for item in items:
        generate_content(item)
```

**Limits Enforcement:**
```python
limits = server_info["limits"]

if len(batch_items) > limits["max_batch_size"]:
    # Split into chunks
    chunks = split_into_chunks(batch_items, limits["max_batch_size"])
    for chunk in chunks:
        batch_generate(chunk)
```

---

## Task 2: Discover Available Tools

**Use Case:** Find all available MCP tools without hardcoded knowledge.

### Query All Tools

**You:**
```
Show me all available MCP tools with their descriptions and schemas
```

**Expected Response:**
```
Claude: Available tools (17):

**Core Generation:**
1. generate_content
   - Purpose: Generate single content piece
   - Input: config_id, context, output_path
   - Returns: Generated content + metadata

2. assemble_artifact
   - Purpose: Combine content into artifacts
   - Input: artifact_config_id, output_path
   - Returns: Assembled artifact + metadata

[... 15 more tools ...]

Would you like details on any specific tool?
```

---

### Direct Resource Access

**Request:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "capabilities://tools"
  }
}
```

**Response (excerpt):**
```json
{
  "contents": [{
    "uri": "capabilities://tools",
    "mimeType": "application/json",
    "text": "{
      \"tools\": [
        {
          \"name\": \"draft_config\",
          \"description\": \"Create ephemeral draft configuration\",
          \"category\": \"config_lifecycle\",
          \"input_schema\": {
            \"type\": \"object\",
            \"properties\": {
              \"config_type\": {\"type\": \"string\", \"enum\": [\"content\", \"artifact\"]},
              \"config_data\": {\"type\": \"object\"},
              \"description\": {\"type\": \"string\"}
            },
            \"required\": [\"config_type\", \"config_data\"]
          },
          \"examples\": [{
            \"config_type\": \"content\",
            \"config_data\": {\"id\": \"example\", \"generation\": {...}}
          }],
          \"errors\": [
            {\"code\": \"SCHEMA_VALIDATION_ERROR\", \"retryable\": false},
            {\"code\": \"STORAGE_ERROR\", \"retryable\": true}
          ]
        }
      ]
    }"
  }]
}
```

---

### Tool Selection Logic

**Agent Decision Tree:**
```python
tools = fetch("capabilities://tools")["tools"]

# Find tools by category
generation_tools = [t for t in tools if t["category"] == "core_generation"]
lifecycle_tools = [t for t in tools if t["category"] == "config_lifecycle"]

# Check if specific tool exists
if "batch_generate" in [t["name"] for t in tools]:
    # Use batch operations
    use_batch_generate()
else:
    # Fallback to sequential
    use_generate_content()
```

**Validation Before Use:**
```python
def can_use_tool(tool_name, available_tools):
    tool = next((t for t in available_tools if t["name"] == tool_name), None)
    return tool is not None

if can_use_tool("draft_config", tools):
    # Safe to use conversational workflow
    draft_config(...)
else:
    # Server doesn't support config lifecycle
    print("Feature not available on this server version")
```

---

## Task 3: Discover Available Generators

**Use Case:** Find what content generators are installed (builtin + plugins).

### Query Generator Registry

**You:**
```
What content generators are available? Include any plugins.
```

**Expected Response:**
```
Claude: Generator Registry (2 built-in + 0 plugins):

**Built-in Generators:**

1. jinja2
   - Type: Template-based
   - Version: 3.1.2
   - Requirements: Template file (*.jinja, *.jinja2, *.j2)
   - Capabilities: Dynamic content, template inheritance, filters
   - Best for: Complex, data-driven documents
   - Indicators:
     ✅ Dynamic data required
     ✅ Template reuse needed
     ✅ Complex formatting

2. demonstration
   - Type: Example-based
   - Version: 1.0.0
   - Requirements: example_output field in config
   - Capabilities: Static content, simple placeholders
   - Best for: Static documents, quick prototypes
   - Indicators:
     ✅ Static content
     ✅ No dynamic data
     ✅ Rapid prototyping

No plugin generators detected.

Selection guidance: Use jinja2 for dynamic content, demonstration for static.
```

---

### Direct Resource Access

**Request:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "capabilities://generators"
  }
}
```

**Response:**
```json
{
  "contents": [{
    "uri": "capabilities://generators",
    "mimeType": "application/json",
    "text": "{
      \"generators\": [
        {
          \"id\": \"jinja2\",
          \"name\": \"Jinja2 Template Generator\",
          \"type\": \"template\",
          \"version\": \"3.1.2\",
          \"builtin\": true,
          \"requirements\": {
            \"template_file\": true,
            \"api_key\": false,
            \"dependencies\": [\"jinja2>=3.1.0\"]
          },
          \"capabilities\": [
            \"dynamic_content\",
            \"template_inheritance\",
            \"filters\",
            \"macros\"
          ],
          \"indicators\": [
            {\"name\": \"has_dynamic_data\", \"weight\": 0.8},
            {\"name\": \"needs_template_reuse\", \"weight\": 0.9},
            {\"name\": \"complex_formatting\", \"weight\": 0.7}
          ]
        }
      ]
    }"
  }]
}
```

---

### Generator Selection Logic

**Agent Recommendation System:**
```python
generators = fetch("capabilities://generators")["generators"]

def recommend_generator(requirements):
    scores = {}
    for gen in generators:
        score = 0
        for indicator in gen["indicators"]:
            if requirements.get(indicator["name"]):
                score += indicator["weight"]
        scores[gen["id"]] = score

    best = max(scores, key=scores.get)
    return best

# Example usage
requirements = {
    "has_dynamic_data": True,
    "needs_template_reuse": True,
    "complex_formatting": False
}

recommended = recommend_generator(requirements)
# Returns: "jinja2" (score: 1.7)
```

**Plugin Detection:**
```python
generators = fetch("capabilities://generators")["generators"]
plugins = [g for g in generators if not g["builtin"]]

if plugins:
    print(f"Detected {len(plugins)} plugin generators:")
    for plugin in plugins:
        print(f"  - {plugin['name']} (v{plugin['version']})")
else:
    print("No plugin generators installed")
```

---

## Task 4: Check Resource Catalog

**Use Case:** Discover all available resource URIs.

### Query Resource Catalog

**You:**
```
List all available MCP resources
```

**Expected Response:**
```
Claude: Available Resources:

**Capability Discovery (5):**
- capabilities://server - Server metadata
- capabilities://tools - Tool inventory
- capabilities://resources - This catalog
- capabilities://generators - Generator registry
- capabilities:// - Capability overview

**Legacy Resources (4):**
- config:// - Configuration access
- schema:// - JSON Schema access
- content:// - Generated content access
- generator:// - Generator metadata (deprecated in favor of capabilities://generators)

Total: 9 resource URIs available
```

---

### Direct Resource Access

**Request:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "capabilities://resources"
  }
}
```

**Response:**
```json
{
  "contents": [{
    "uri": "capabilities://resources",
    "mimeType": "application/json",
    "text": "{
      \"resources\": [
        {
          \"uri_pattern\": \"capabilities://server\",
          \"description\": \"Server metadata, features, limits\",
          \"parameters\": [],
          \"examples\": [\"capabilities://server\"],
          \"response_type\": \"application/json\"
        },
        {
          \"uri_pattern\": \"capabilities://generators\",
          \"description\": \"Generator registry with selection metadata\",
          \"parameters\": [],
          \"examples\": [\"capabilities://generators\"],
          \"response_type\": \"application/json\"
        }
      ]
    }"
  }]
}
```

---

## Task 5: Build Adaptive Agent Startup Routine

**Use Case:** Agent initializes by discovering server capabilities.

### Startup Sequence

**Agent Pseudo-code:**
```python
async def initialize_agent():
    print("Initializing agent...")

    # Step 1: Check server version
    server_info = await fetch("capabilities://server")
    print(f"Connected to: {server_info['server_name']} v{server_info['server_version']}")

    # Step 2: Discover available tools
    tools_info = await fetch("capabilities://tools")
    available_tools = [t["name"] for t in tools_info["tools"]]
    print(f"Available tools: {len(available_tools)}")

    # Step 3: Discover generators
    gen_info = await fetch("capabilities://generators")
    generators = gen_info["generators"]
    print(f"Available generators: {[g['id'] for g in generators]}")

    # Step 4: Check features
    features = server_info["features"]
    if features.get("conversational_workflow_authoring"):
        print("✅ Conversational workflow supported")
        enable_conversational_mode()
    else:
        print("⚠️  Conversational workflow not available")
        use_traditional_mode()

    if features.get("batch_generation"):
        print("✅ Batch operations supported")
        enable_batch_mode()

    # Step 5: Set limits
    limits = server_info["limits"]
    set_batch_size_limit(limits["max_batch_size"])
    set_draft_retention(limits["draft_retention_days"])

    print("Agent initialized successfully")
```

**Example Output:**
```
Initializing agent...
Connected to: chora-compose v1.2.0
Available tools: 13
Available generators: ['jinja2', 'demonstration']
✅ Conversational workflow supported
✅ Batch operations supported
Agent initialized successfully
```

---

## Task 6: Version Compatibility Checks

**Use Case:** Ensure agent works across different server versions.

### Version-Aware Workflows

**Check Minimum Version:**
```python
def check_minimum_version(required_version):
    server_info = fetch("capabilities://server")
    server_version = server_info["server_version"]

    # Simple version comparison (production would use semver library)
    return version_compare(server_version, required_version) >= 0

if check_minimum_version("1.2.0"):
    # Use v1.2.0 features
    use_draft_config()
    use_batch_generate()
else:
    # Fallback to v1.0.x behavior
    use_file_based_configs()
    use_sequential_generation()
```

**Feature-Based Branching:**
```python
server_info = fetch("capabilities://server")
features = server_info["features"]

# Branch based on feature availability, not version
if "conversational_workflow_authoring" in features and features["conversational_workflow_authoring"]:
    workflow = ConversationalWorkflow()
else:
    workflow = TraditionalWorkflow()

if "batch_generation" in features and features["batch_generation"]:
    generator = BatchGenerator()
else:
    generator = SequentialGenerator()
```

---

## Task 7: Plugin Detection and Usage

**Use Case:** Detect and use custom generators installed as plugins.

### Plugin Discovery

**Check for Plugins:**
```python
gen_info = fetch("capabilities://generators")
generators = gen_info["generators"]

builtin_count = len([g for g in generators if g["builtin"]])
plugin_count = len([g for g in generators if not g["builtin"]])

print(f"Built-in generators: {builtin_count}")
print(f"Plugin generators: {plugin_count}")

if plugin_count > 0:
    print("\nDetected plugins:")
    for gen in generators:
        if not gen["builtin"]:
            print(f"  - {gen['name']} v{gen['version']}")
            print(f"    Requirements: {gen['requirements']}")
```

**Use Plugin Generator:**
```python
# Agent dynamically discovers "code-generator" plugin
generators = fetch("capabilities://generators")["generators"]
code_gen = next((g for g in generators if g["id"] == "code-generator"), None)

if code_gen:
    # Plugin detected, use it
    print(f"Using plugin: {code_gen['name']}")

    # Check requirements
    if code_gen["requirements"].get("api_key"):
        print("⚠️  This generator requires an API key")
        if not has_api_key():
            print("❌ Cannot use generator - missing API key")
            return

    # Create config using plugin generator
    draft_config(
        config_type="content",
        config_data={
            "id": "code-example",
            "generation": {
                "patterns": [{
                    "type": "code-generator",  # Plugin generator
                    "generation_config": {...}
                }]
            }
        }
    )
else:
    print("Plugin not found, using builtin generator")
```

---

## Common Patterns

### Pattern 1: Graceful Degradation

**Agent adapts to missing features:**
```python
server_info = fetch("capabilities://server")

# Try advanced feature first
if "batch_generation" in server_info["features"]:
    try:
        result = batch_generate(items)
    except Exception as e:
        print(f"Batch failed: {e}, falling back to sequential")
        result = sequential_generate(items)
else:
    # Feature not available, use fallback
    result = sequential_generate(items)
```

---

### Pattern 2: Progressive Enhancement

**Start with basics, add features as available:**
```python
# Base workflow
workflow = BasicWorkflow()

# Enhance based on capabilities
features = fetch("capabilities://server")["features"]

if features.get("conversational_workflow_authoring"):
    workflow = enhance_with_conversational(workflow)

if features.get("batch_generation"):
    workflow = enhance_with_batch(workflow)

if features.get("capability_discovery"):
    workflow = enhance_with_dynamic_discovery(workflow)

# Execute enhanced workflow
workflow.run()
```

---

### Pattern 3: Tool Availability Check

**Before calling any tool:**
```python
def safe_tool_call(tool_name, *args, **kwargs):
    tools_info = fetch("capabilities://tools")
    available_tools = [t["name"] for t in tools_info["tools"]]

    if tool_name in available_tools:
        return call_tool(tool_name, *args, **kwargs)
    else:
        raise ToolNotAvailableError(f"{tool_name} not available on this server")

# Usage
try:
    result = safe_tool_call("batch_generate", items)
except ToolNotAvailableError as e:
    print(f"Error: {e}")
    # Use fallback
```

---

## Troubleshooting

### Issue: Capability Resource Not Found

**Error:**
```
Resource not found: capabilities://server
```

**Cause:** Server version < 1.2.0 (doesn't support capability discovery).

**Solution:**
```python
try:
    server_info = fetch("capabilities://server")
except ResourceNotFoundError:
    print("⚠️  Server doesn't support capability discovery")
    print("Falling back to hardcoded assumptions")
    # Use v1.0.x behavior
```

---

### Issue: Tool List Out of Date

**Problem:** Agent caches tool list, misses newly added tools.

**Solution:** Refresh capabilities periodically:
```python
def get_tools(cache_ttl=300):  # 5 minute cache
    if cache_expired(cache_ttl):
        tools_info = fetch("capabilities://tools")
        update_cache(tools_info)
    return get_cached_tools()
```

---

### Issue: Plugin Not Detected

**Problem:** Plugin generator installed but not showing in capabilities.

**Diagnosis:**
```python
# Check generator registry
generators = fetch("capabilities://generators")["generators"]
print(f"Detected generators: {[g['id'] for g in generators]}")

# Check if plugin is registered
plugin_ids = [g["id"] for g in generators if not g["builtin"]]
if "my-plugin" not in plugin_ids:
    print("Plugin not registered. Check installation.")
```

**Common causes:**
- Plugin not installed in correct directory
- Plugin not registered in GeneratorRegistry
- Server restart needed after plugin installation

---

## Best Practices

### ✅ Do's

1. **Always Query Capabilities on Startup**
   ```python
   # Initialize agent
   server_info = fetch("capabilities://server")
   tools = fetch("capabilities://tools")
   generators = fetch("capabilities://generators")
   ```

2. **Cache Capability Results (With TTL)**
   ```python
   # Cache for 5 minutes to avoid excessive queries
   cached_capabilities = cache_with_ttl(
       fetch("capabilities://server"),
       ttl=300
   )
   ```

3. **Use Feature Flags, Not Version Checks**
   ```python
   # ✅ Good: Feature-based
   if features["batch_generation"]:
       use_batch()

   # ❌ Bad: Version-based
   if version >= "1.2.0":
       use_batch()
   ```

4. **Provide Fallbacks**
   ```python
   if tool_available("batch_generate"):
       batch_generate(items)
   else:
       for item in items:
           generate_content(item)
   ```

---

### ❌ Don'ts

1. **Don't Hardcode Tool Lists**
   ```python
   # ❌ Don't do this
   TOOLS = ["generate_content", "assemble_artifact"]

   # ✅ Do this instead
   tools = [t["name"] for t in fetch("capabilities://tools")["tools"]]
   ```

2. **Don't Assume Features Exist**
   ```python
   # ❌ Don't assume
   batch_generate(items)  # Might not exist!

   # ✅ Check first
   if "batch_generate" in available_tools:
       batch_generate(items)
   ```

3. **Don't Cache Indefinitely**
   ```python
   # ❌ Stale cache
   CACHED_TOOLS = fetch_once("capabilities://tools")

   # ✅ Refresh periodically
   tools = fetch_with_ttl("capabilities://tools", ttl=300)
   ```

---

## Related Documentation

- **[Tutorial: MCP Integration Deep Dive](../../tutorials/advanced/01-mcp-integration-deep-dive.md)** - Complete MCP workflow tutorial
- **[Reference: Capabilities Resources API](../../reference/api/resources/capabilities.md)** - API documentation
- **[Reference: MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md)** - All tools reference
- **[How-To: Batch Generate Content](../generation/batch-generate-content.md)** - Batch operations guide

---

**You can now build adaptive AI agents that discover and use server capabilities dynamically!**
