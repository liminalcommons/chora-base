# MCP Tool Reference

Complete API reference for Chora Compose MCP tools. Use these tools with Claude Desktop to generate content, assemble artifacts, and validate configurations through natural conversation.

**Last Updated:** 2025-10-17
**MCP Server Version:** 1.2.3

---

## Quick Reference

| Tool | Purpose | Common Use |
|------|---------|------------|
| **[hello_world](#hello_world)** | Test MCP connection | Verify server is responding |
| **[generate_content](#generate_content)** | Generate content from configurations | Create documentation, README files, code examples |
| **[assemble_artifact](#assemble_artifact)** | Combine content into final outputs | Assemble multi-section documentation |
| **[list_generators](#list_generators)** | Discover available generators | Explore generation capabilities |
| **[validate_content](#validate_content)** | Validate configurations | Check configs before generation |
| **[list_content](#list_content)** | List generated content | Browse generated content catalog |
| **[list_artifacts](#list_artifacts)** | List generated artifacts | Audit artifact output |
| **[regenerate_content](#regenerate_content)** | Force regeneration | Bypass cache |
| **[delete_content](#delete_content)** | Delete specific content | Clean up unwanted files |
| **[preview_generation](#preview_generation)** | Preview before creating files | Test without side effects |
| **[batch_generate](#batch_generate)** | Parallel generation | Generate multiple pieces efficiently |
| **[trace_dependencies](#trace_dependencies)** | Show artifact dependencies | Understand composition |
| **[cleanup_ephemeral](#cleanup_ephemeral)** | Remove expired files | Manage storage |
| **[draft_config](#draft_config)** | Create draft config | Conversational workflow authoring |
| **[test_config](#test_config)** | Test draft config | Preview config output |
| **[modify_config](#modify_config)** | Update draft config | Iterate on config design |
| **[save_config](#save_config)** | Persist draft config | Finalize config to filesystem |
| **[list_content_configs](#list_content_configs)** | List content config files | Discover available content types |
| **[list_artifact_configs](#list_artifact_configs)** | List artifact config files | Discover available artifact types |

---

## Common Workflows

### Content Generation Workflow

```
1. list_generators     → Discover what generators are available
2. generate_content    → Generate individual content pieces
3. validate_content    → Verify content (optional)
4. assemble_artifact   → Combine into final artifact
```

### Batch Generation Workflow (v1.1.0+)

```
1. list_content        → Browse available content configs
2. batch_generate      → Generate multiple pieces in parallel
3. list_artifacts      → Verify outputs were created
4. trace_dependencies  → Understand artifact composition
```

---

## Design Principles

Understanding these principles helps you use the tools effectively.

### Idempotent Operations

Tools check state before acting - you can safely retry operations:

```
First call:  generate_content("my-doc") → Generates content
Second call: generate_content("my-doc") → Skips (already exists)
Force regen: generate_content("my-doc", force=true) → Regenerates
```

### Structured Responses

All tools return consistent JSON structures:

**Success response:**
```json
{
  "success": true,
  "content": "Generated content here...",
  "duration_ms": 142,
  "metadata": {...}
}
```

**Error response:**
```json
{
  "success": false,
  "error": {
    "code": "config_not_found",
    "message": "Content config 'xyz' not found",
    "details": {...}
  }
}
```

### Performance Transparency

All operations report execution time:

- Simple queries: <100ms (typical)
- Content generation: <2s (typical)
- Artifact assembly: <5s (typical)

---

## Common Parameters

### Configuration IDs

All tools use string IDs to reference configurations:

```
content_config_id: "welcome-message"
artifact_config_id: "user-documentation"
```

**Requirements:**
- Valid filename (no path separators like `/` or `\`)
- Case-sensitive
- Use hyphens or underscores (not spaces)
- No parent directory references (`..`)

**Valid examples:**
- `"welcome-message"`
- `"user_profile"`
- `"api-v2-docs"`

**Invalid examples:**
- `"../secret"` (path traversal)
- `"config/nested"` (path separator)
- `"   "` (whitespace only)

### Context Objects

Context provides variable values for template generation:

```json
{
  "user": {
    "name": "Alice",
    "role": "admin"
  },
  "timestamp": "2025-10-15T12:00:00Z",
  "version": "1.0.0"
}
```

**Requirements:**
- Must be JSON-serializable
- Can contain nested objects and arrays
- Null values allowed
- No functions or circular references

### Force Flag

Override idempotency to force regeneration:

**When to use `force=true`:**
- Template has changed
- Context data updated
- Previous generation failed
- Testing or debugging

---

## Tool: generate_content

Generate content from a content configuration using the specified generator.

### Purpose

- Generate individual content pieces from templates
- Apply context variables to templates
- Store generated content in ephemeral storage
- Return generated content for immediate use

### When to Use

- Generate single content pieces
- Need immediate content output
- Want to inspect content before assembly
- Testing content configurations

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | **Yes** | - | ID of content configuration |
| `context` | object | No | `{}` | Context variables for templates |
| `force` | boolean | No | `false` | Force regeneration |

#### content_config_id (required)

**Description:** ID of the content configuration to use for generation.

**Details:**
- Must match filename in `configs/content/` directory
- Example: `"welcome-message"` → looks for `configs/content/welcome-message/welcome-message.json`
- Case-sensitive
- No path traversal allowed

**Example:**
```json
"content_config_id": "api-documentation"
```

#### context (optional)

**Description:** Context variables for template substitution.

**Details:**
- Accepts JSON object or string containing JSON
- Merged with config context
- Tool context overrides config context
- Empty object `{}` if not provided

**Example (object form):**
```json
"context": {
  "user": {"name": "Alice"},
  "version": "2.0"
}
```

**Example (string form - auto-parsed):**
```json
"context": "{\"user\": {\"name\": \"Alice\"}, \"version\": \"2.0\"}"
```

#### force (optional)

**Description:** Force regeneration even if content exists.

**Details:**
- `false` (default): Skip generation if content exists
- `true`: Always regenerate, replacing existing
- Use when template or context changed

**Example:**
```json
"force": true
```

### Returns

**Type:** Object

```json
{
  "success": true,
  "content_id": "welcome-message",
  "content": "# Welcome Alice!\n\nGenerated at: 2025-10-15",
  "generator": "jinja2",
  "status": "generated",
  "duration_ms": 142,
  "metadata": {
    "context_variables": ["user", "timestamp"],
    "ephemeral_stored": true,
    "ephemeral_path": "ephemeral://content/welcome-message",
    "output_size": 512
  }
}
```

#### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `true` for successful operations |
| `content_id` | string | ID of generated content |
| `content` | string | The generated content text |
| `generator` | string | Generator used (e.g., "jinja2") |
| `status` | string | "generated", "skipped", or "regenerated" |
| `duration_ms` | number | Execution time in milliseconds |
| `metadata` | object | Additional generation information |

#### Status Values

- **`generated`** - Content was newly generated
- **`skipped`** - Content exists, generation skipped
- **`regenerated`** - Content existed and was regenerated (force=true)

### Error Cases

| Error Code | When It Occurs | Solution |
|------------|----------------|----------|
| `config_not_found` | Config file doesn't exist | Check config ID, verify file exists |
| `generation_failed` | Generator execution failed | Check template syntax, verify variables |
| `invalid_context` | Context validation failed | Ensure valid JSON object |
| `generator_not_found` | Generator unavailable | Check generator name, verify it's registered |
| `invalid_config_id` | Invalid ID characters | Remove path separators, use valid names |

#### Error Examples

**config_not_found:**
```json
{
  "success": false,
  "error": {
    "code": "config_not_found",
    "message": "Content config 'missing-content' not found",
    "details": {
      "content_config_id": "missing-content",
      "searched_paths": ["/configs/content/missing-content.json"]
    }
  }
}
```

**generation_failed:**
```json
{
  "success": false,
  "error": {
    "code": "generation_failed",
    "message": "Template error: undefined variable 'username'",
    "details": {
      "generator": "jinja2",
      "missing_variable": "username",
      "available_variables": ["user", "timestamp"]
    }
  }
}
```

### Usage Examples

#### Example 1: Basic Generation

**Prompt to Claude:**
```
Generate content using the config ID 'simple-readme'
```

**Tool call:**
```json
{
  "content_config_id": "simple-readme",
  "context": {},
  "force": false
}
```

**Response:**
```json
{
  "success": true,
  "content_id": "simple-readme",
  "content": "# My Project\n\nWelcome to my project...",
  "generator": "demonstration",
  "status": "generated",
  "duration_ms": 85
}
```

#### Example 2: Generation with Context

**Prompt to Claude:**
```
Generate content from 'user-profile' with context: user name is Alice, role is admin
```

**Tool call:**
```json
{
  "content_config_id": "user-profile",
  "context": {
    "user": {
      "name": "Alice",
      "role": "admin"
    }
  },
  "force": false
}
```

**Response:**
```json
{
  "success": true,
  "content_id": "user-profile",
  "content": "# User: Alice\nRole: Administrator\n...",
  "generator": "jinja2",
  "status": "generated",
  "duration_ms": 156
}
```

#### Example 3: Force Regeneration

**Prompt to Claude:**
```
Regenerate the api-docs content, forcing a fresh generation
```

**Tool call:**
```json
{
  "content_config_id": "api-docs",
  "context": {},
  "force": true
}
```

**Response:**
```json
{
  "success": true,
  "content_id": "api-docs",
  "content": "# API Documentation...",
  "generator": "jinja2",
  "status": "regenerated",
  "duration_ms": 234
}
```

---

## Tool: assemble_artifact

Assemble a final artifact from multiple content pieces.

### Purpose

- Combine multiple content configs into single output
- Apply composition strategies (concat, merge, etc.)
- Write final artifacts to files
- Track assembly metadata

### When to Use

- Combine multiple sections into complete docs
- Assemble multi-part artifacts
- Generate final deliverables
- Create composite documentation

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `artifact_config_id` | string | **Yes** | - | ID of artifact configuration |
| `output_path` | string | No | (from config) | Override output file path |
| `force` | boolean | No | `false` | Force reassembly |

#### artifact_config_id (required)

**Description:** ID of the artifact configuration to assemble.

**Details:**
- Must match filename in `configs/artifacts/` directory
- Example: `"complete-docs"` → looks for `configs/artifacts/complete-docs.json`
- Case-sensitive

**Example:**
```json
"artifact_config_id": "user-documentation"
```

#### output_path (optional)

**Description:** Override default output file path from config.

**Details:**
- Relative to project root or absolute path
- Overrides `metadata.outputs[0].file` from config
- Useful for testing different output locations

**Example:**
```json
"output_path": "output/custom-location.md"
```

#### force (optional)

**Description:** Force reassembly even if artifact exists.

**Details:**
- `false` (default): Skip if output file exists
- `true`: Always reassemble, replacing existing
- Regenerates all child content

**Example:**
```json
"force": true
```

### Returns

**Type:** Object

```json
{
  "success": true,
  "artifact_id": "complete-docs",
  "output_path": "output/documentation.md",
  "content_count": 3,
  "total_size": 15420,
  "status": "assembled",
  "duration_ms": 456,
  "metadata": {
    "composition_strategy": "concat",
    "children_generated": 3,
    "children_skipped": 0,
    "ephemeral_used": true
  }
}
```

#### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `true` for successful operations |
| `artifact_id` | string | ID of assembled artifact |
| `output_path` | string | Path where artifact was written |
| `content_count` | number | Number of content pieces assembled |
| `total_size` | number | Size of final artifact in bytes |
| `status` | string | "assembled", "skipped", or "reassembled" |
| `duration_ms` | number | Execution time in milliseconds |
| `metadata` | object | Assembly details |

### Error Cases

| Error Code | When It Occurs | Solution |
|------------|----------------|----------|
| `config_not_found` | Artifact config doesn't exist | Verify artifact config file exists |
| `assembly_failed` | Assembly process failed | Check child configs, verify generators |
| `child_generation_failed` | Child content generation failed | Check individual content configs |
| `invalid_artifact_id` | Invalid ID characters | Use valid artifact ID format |
| `output_write_failed` | Cannot write output file | Check permissions, verify path |

### Usage Examples

#### Example 1: Basic Assembly

**Prompt to Claude:**
```
Assemble the complete-documentation artifact
```

**Tool call:**
```json
{
  "artifact_config_id": "complete-documentation",
  "force": false
}
```

**Response:**
```json
{
  "success": true,
  "artifact_id": "complete-documentation",
  "output_path": "output/DOCUMENTATION.md",
  "content_count": 5,
  "total_size": 28640,
  "status": "assembled",
  "duration_ms": 892
}
```

#### Example 2: Custom Output Path

**Prompt to Claude:**
```
Assemble user-guide to docs/guide.md
```

**Tool call:**
```json
{
  "artifact_config_id": "user-guide",
  "output_path": "docs/guide.md",
  "force": false
}
```

---

## Tool: list_generators

Query available content generators.

### Purpose

- Discover built-in generators
- Find loaded plugin generators
- Check generator capabilities
- Verify generator availability

### When to Use

- Explore available generation strategies
- Check if specific generator exists
- Understand generator capabilities
- Debug generator issues

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `generator_type` | string | No | (all) | Filter: "builtin" or "plugin" |
| `include_plugins` | boolean | No | `true` | Include plugin generators |

#### generator_type (optional)

**Description:** Filter generators by type.

**Values:**
- `"builtin"` - Only built-in generators
- `"plugin"` - Only plugin generators
- `null` - All generators (default)

**Example:**
```json
"generator_type": "builtin"
```

#### include_plugins (optional)

**Description:** Whether to include plugin generators.

**Details:**
- `true` (default): Include all generators
- `false`: Only built-in generators

**Example:**
```json
"include_plugins": false
```

### Returns

**Type:** Object

```json
{
  "success": true,
  "generators": [
    {
      "name": "jinja2",
      "type": "builtin",
      "status": "available",
      "description": "Full-featured Jinja2 template engine",
      "capabilities": ["variables", "loops", "conditionals", "filters"]
    },
    {
      "name": "demonstration",
      "type": "builtin",
      "status": "available",
      "description": "Example-based content generation"
    }
  ],
  "total_count": 5,
  "builtin_count": 5,
  "plugin_count": 0,
  "duration_ms": 12
}
```

#### Generator Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Generator name/identifier |
| `type` | string | "builtin" or "plugin" |
| `status` | string | "available", "unavailable", or "error" |
| `description` | string | Human-readable description |
| `capabilities` | array | List of supported features (optional) |

### Built-in Generators

- **jinja2** - Full Jinja2 template engine (variables, loops, conditionals)
- **demonstration** - Example-based generation
- **template_fill** - Simple variable substitution
- **code_generation** - AI-powered code generation (coming soon)
- **bdd_scenario_assembly** - BDD test scenarios (coming soon)

### Usage Examples

#### Example 1: List All Generators

**Prompt to Claude:**
```
What generators are available?
```

**Tool call:**
```json
{
  "include_plugins": true
}
```

**Response:**
```json
{
  "success": true,
  "generators": [
    {"name": "demonstration", "type": "builtin", "status": "available"},
    {"name": "jinja2", "type": "builtin", "status": "available"},
    {"name": "template_fill", "type": "builtin", "status": "available"}
  ],
  "total_count": 3,
  "builtin_count": 3,
  "plugin_count": 0
}
```

---

## Tool: validate_content

Validate content configurations against schemas.

### Purpose

- Verify configuration correctness
- Check schema compliance
- Validate before generation
- Debug configuration errors

### When to Use

- Before generating content
- Debugging config errors
- Ensuring schema compliance
- Testing new configurations

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_or_config_id` | string | **Yes** | - | Config ID to validate |
| `validation_rules` | object | No | (default) | Custom validation rules |

#### content_or_config_id (required)

**Description:** ID of content configuration to validate.

**Example:**
```json
"content_or_config_id": "api-documentation"
```

#### validation_rules (optional)

**Description:** Custom validation rules to apply.

**Details:**
- Extends default schema validation
- Can add stricter requirements
- Optional field

### Returns

**Type:** Object

```json
{
  "success": true,
  "valid": true,
  "config_id": "api-documentation",
  "issues": [],
  "schema_version": "3.1",
  "duration_ms": 45
}
```

#### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Tool execution success |
| `valid` | boolean | Whether config is valid |
| `config_id` | string | ID of validated config |
| `issues` | array | List of validation issues |
| `schema_version` | string | Schema version used |
| `duration_ms` | number | Execution time |

### Usage Examples

#### Example 1: Validate Config

**Prompt to Claude:**
```
Validate the api-docs configuration
```

**Tool call:**
```json
{
  "content_or_config_id": "api-docs"
}
```

**Response (valid):**
```json
{
  "success": true,
  "valid": true,
  "config_id": "api-docs",
  "issues": [],
  "schema_version": "3.1",
  "duration_ms": 34
}
```

**Response (invalid):**
```json
{
  "success": true,
  "valid": false,
  "config_id": "broken-config",
  "issues": [
    {
      "field": "elements",
      "message": "Required field missing",
      "severity": "error"
    }
  ],
  "schema_version": "3.1",
  "duration_ms": 28
}
```

---

## Claude Desktop Integration

### Using Tools in Conversation

Simply ask Claude naturally - the tools are called automatically:

**Examples:**
- "List available generators"
- "Generate content from api-docs config"
- "Assemble the user-documentation artifact"
- "Validate my-config"

### Context Passing

For templates requiring variables:

```
Generate user-profile with context:
- user name: Alice
- role: administrator
- department: Engineering
```

Claude will format the context appropriately for the tool.

### Troubleshooting Integration

See [Troubleshooting Guide](troubleshooting.md) for common MCP integration issues.

---

## Performance Guide

### Expected Performance

- **Simple queries:** <100ms
- **Content generation:** <2 seconds
- **Artifact assembly:** <5 seconds

### Optimization Tips

1. **Use force=false** - Let tools skip existing content
2. **Validate configs first** - Catch errors before generation
3. **Cache context** - Reuse context objects across calls
4. **Check generator availability** - List generators before using

---


## Additional Resources

- **[MCP Server Setup](README.md)** - Installation and configuration
- **[End-to-End Exercise](end-to-end-exercise.md)** - Complete testing workflow
- **[Troubleshooting](troubleshooting.md)** - Fix common issues
- **[Resource Providers](resource-providers.md)** - Access configs and content

---

**Tool Reference Complete**
**For support:** [GitHub Issues](https://github.com/liminalcommons/chora-compose/issues)
**MCP Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io/)
