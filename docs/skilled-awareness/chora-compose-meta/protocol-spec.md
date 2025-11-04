# Protocol Specification: chora-compose Meta

**SAP ID**: SAP-018
**Version**: 2.0.0
**Status**: active
**Last Updated**: 2025-11-04

---

## 1. Overview

This document provides the complete technical specification for chora-compose Meta (v1.5.0), the architecture underlying chora-compose content generation framework.

### Key Capabilities

**24 MCP Tools** organized into 7 categories:
- **Core Generation (5 tools)**: generate_content, assemble_artifact, regenerate_content, preview_generation, batch_generate
- **Config Lifecycle (4 tools)**: draft_config, test_config, modify_config, save_config
- **Storage Management (2 tools)**: cleanup_ephemeral, delete_content
- **Discovery (6 tools)**: list_generators, list_content, list_artifacts, trace_dependencies, list_content_configs, list_artifact_configs
- **Validation (2 tools)**: validate_content, check_freshness
- **Collection Operations (4 tools)**: generate_collection, validate_collection_config, list_collection_members, check_collection_cache
- **Utility (1 tool)**: hello_world

**Collections Architecture**: 3-tier composition model (Content → Artifact → Collection) with context propagation (MERGE/OVERRIDE/ISOLATE modes), SHA-256 caching, parallel/sequential execution strategies

**5 Generators**: demonstration, jinja2, template_fill, bdd_scenario, code_generation (extensible via BaseGenerator interface)

**Context Resolution**: 6 source types (inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output)

**Event Emission**: OpenTelemetry format with 3 event types (content_generated, artifact_assembled, validation_completed)

**JSON Schemas**: v3.1 for content/artifact configs, v1.0 for collection configs

**Stigmergic Context Links**: Freshness tracking for collection members (v1.5.0)

---

## 2. MCP Tools Specification

This section documents all 24 Model Context Protocol (MCP) tools provided by chora-compose v1.5.0, organized by functional category.

### Tool Naming Convention

All tools use the namespace prefix `choracompose:` (e.g., `choracompose:generate_content`).

### Common Error Response Format

All tools return errors in this structure:

```json
{
  "success": false,
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

**Common Error Codes Across Tools**:
- `config_not_found`: Configuration file not found
- `validation_failed`: Input validation failed
- `generation_failed`: Content/artifact generation failed
- `invalid_context`: Context parameter not valid JSON
- `invalid_input`: Input parameter validation failed
- `storage_error`: Ephemeral storage operation failed
- `permission_denied`: File system permission error
- `internal_error`: Unexpected error (includes type name in details)

### Context Parameter Handling

Most generation tools accept `context` as either:
- **JSON object**: `{"key": "value"}`
- **JSON string**: `"{\"key\": \"value\"}"` (auto-parsed)

This accommodates Claude Desktop's behavior of serializing JSON objects as strings.

---

## 2.1. Core Generation Tools (5 tools)

### Tool: generate_content

**Purpose**: Generate content from a content configuration using the specified generator

**Category**: Core generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | Yes | - | ID of content config (matches filename in `configs/content/`, without `.json` extension) |
| `context` | object \| string | No | `{}` | Context variables for template substitution. Accepts JSON object or JSON string (auto-parsed). Merged with config context. |
| `force` | boolean | No | `false` | Force regeneration even if content already exists in ephemeral storage |

**Returns**:

```json
{
  "success": true,
  "content_id": "string",
  "content": "string",
  "generator": "string",
  "status": "generated|skipped|regenerated",
  "duration_ms": "number",
  "metadata": {
    "context_variables": ["string"],
    "ephemeral_stored": "boolean",
    "storage_path": "string"
  }
}
```

**Errors**:
- `config_not_found`: content_config_id does not exist
- `generator_not_found`: Generator type not available
- `generation_failed`: Generator failed to produce output
- `invalid_context`: Context data is not valid JSON object
- `storage_failed`: Failed to write to ephemeral storage

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:generate_content",
    "arguments": {
      "content_config_id": "welcome-message",
      "context": {"user": {"name": "Alice"}},
      "force": false
    }
  },
  "id": 1
}
```

---

### Tool: assemble_artifact

**Purpose**: Assemble final artifact by combining multiple content pieces

**Category**: Core generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `artifact_config_id` | string | Yes | - | ID of artifact config to use |
| `output_path` | string | No | - | Override output path from config |
| `force` | boolean | No | `false` | Force reassembly even if artifact exists |
| `context` | object \| string | No | `{}` | Optional context for child content generation (dict or JSON string) |

**Returns**:

```json
{
  "success": true,
  "artifact_id": "string",
  "output_path": "string",
  "content_count": "number",
  "size_bytes": "number",
  "status": "assembled|skipped|reassembled",
  "duration_ms": "number",
  "metadata": {
    "missing_content": ["string"],
    "generated_content": ["string"],
    "composition_strategy": "string"
  }
}
```

**Errors**:
- `config_not_found`: artifact_config_id does not exist
- `missing_content`: Required content pieces not found in storage
- `composition_failed`: Failed to assemble artifact
- `write_failed`: Failed to write artifact to filesystem
- `invalid_context`: Context parameter not valid JSON

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:assemble_artifact",
    "arguments": {
      "artifact_config_id": "project-documentation",
      "output_path": "outputs/docs/README.md",
      "force": false
    }
  },
  "id": 1
}
```

---

### Tool: regenerate_content

**Purpose**: Force regenerate content with change tracking and diff comparison

**Category**: Core generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | Yes | - | ID of content config to regenerate |
| `context` | object \| string | No | `{}` | Context variables (merged with config context). Can be dict or JSON string. |
| `reason` | string | No | - | Human-readable reason for regeneration (for audit trail) |
| `compare` | boolean | No | `true` | Whether to compare with previous version and calculate diff |

**Returns**:

```json
{
  "success": true,
  "content_id": "string",
  "status": "regenerated",
  "content": "string",
  "previous_version": {
    "content": "string",
    "hash": "string",
    "generated_at": "string"
  } | null,
  "changes": {
    "lines_added": "number",
    "lines_removed": "number",
    "lines_changed": "number",
    "diff_summary": "string"
  } | null,
  "reason": "string | null",
  "metadata": {
    "hash_new": "string",
    "hash_old": "string"
  },
  "duration_ms": "number"
}
```

**Errors**:
- `config_not_found`: content_config_id does not exist
- `generation_failed`: Generator failed
- `invalid_context`: Context not valid JSON

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:regenerate_content",
    "arguments": {
      "content_config_id": "api-docs",
      "context": {"version": "2.0"},
      "reason": "Updated for API v2.0",
      "compare": true
    }
  },
  "id": 1
}
```

---

### Tool: preview_generation

**Purpose**: Dry-run content generation without writing to storage

**Category**: Core generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | Yes | - | Content configuration ID to preview |
| `context` | object \| string | No | `{}` | Context variables for template substitution. Can be dict or JSON string. |
| `show_metadata` | boolean | No | `false` | Include detailed generation metadata |

**Returns**:

```json
{
  "success": true,
  "content_id": "string",
  "preview_content": "string",
  "content_length": "number",
  "content_hash": "string",
  "generator": "string",
  "metadata": {
    "context_variables": ["string"],
    "template_path": "string"
  } | null,
  "duration_ms": "number"
}
```

**Errors**:
- `config_not_found`: content_config_id does not exist
- `generation_failed`: Preview generation failed
- `invalid_context`: Context not valid JSON

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:preview_generation",
    "arguments": {
      "content_config_id": "email-template",
      "context": {"recipient": "user@example.com"},
      "show_metadata": true
    }
  },
  "id": 1
}
```

---

### Tool: batch_generate

**Purpose**: Generate multiple content pieces in parallel with shared context

**Category**: Core generation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_ids` | array[string] | Yes | - | Array of content configuration IDs to generate |
| `shared_context` | object \| string | No | `{}` | Context applied to all generations. Can be dict or JSON string. |
| `individual_contexts` | object | No | `{}` | Per-ID context overrides. Values can be dict or JSON string. |
| `force` | boolean | No | `false` | Force regeneration of existing content |
| `continue_on_error` | boolean | No | `true` | Continue if one generation fails |
| `max_parallel` | number | No | `4` | Maximum concurrent generations (1-10) |

**Returns**:

```json
{
  "success": true,
  "total": "number",
  "successful": "number",
  "failed": "number",
  "skipped": "number",
  "results": [
    {
      "content_id": "string",
      "success": "boolean",
      "status": "generated|skipped|failed",
      "error": "string | null"
    }
  ],
  "duration_ms": "number",
  "metadata": {
    "parallel_executions": "number"
  }
}
```

**Errors**:
- `invalid_input`: content_ids empty or invalid
- `invalid_context`: Context parameters not valid JSON

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:batch_generate",
    "arguments": {
      "content_ids": ["readme", "changelog", "license"],
      "shared_context": {"project": "myapp", "version": "1.0"},
      "force": false,
      "max_parallel": 3
    }
  },
  "id": 1
}
```

---

## 2.2. Config Lifecycle Tools (4 tools)

### Tool: draft_config

**Purpose**: Create a draft configuration in ephemeral storage for testing

**Category**: Config lifecycle

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config_type` | string | Yes | - | "content" or "artifact" |
| `config_data` | object | Yes | - | Configuration JSON conforming to schema |
| `description` | string | No | - | Optional description for this draft |

**Returns**:

```json
{
  "success": true,
  "draft_id": "string",
  "config_type": "string",
  "validation_status": "valid|invalid",
  "preview_path": "string",
  "created_at": "string",
  "duration_ms": "number"
}
```

**Errors**:
- `validation_error`: Schema validation failed
- `draft_creation_failed`: Failed to create draft

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:draft_config",
    "arguments": {
      "config_type": "content",
      "config_data": {
        "id": "test-content",
        "metadata": {"description": "Test content"},
        "generation": {"generator": {"type": "jinja2"}}
      },
      "description": "Testing new content config"
    }
  },
  "id": 1
}
```

---

### Tool: test_config

**Purpose**: Test a draft config by running generation without persisting output

**Category**: Config lifecycle

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `draft_id` | string | Yes | - | Draft config identifier to test |
| `context` | object \| string | No | `{}` | Optional context for generation (auto-parses JSON strings) |
| `dry_run` | boolean | No | `true` | Don't store output |

**Returns**:

```json
{
  "success": true,
  "draft_id": "string",
  "preview_content": "string",
  "content_length": "number",
  "generator_used": "string",
  "validation_issues": ["string"],
  "estimated_cost": "object | null",
  "duration_ms": "number"
}
```

**Errors**:
- `draft_not_found`: draft_id does not exist
- `test_failed`: Test configuration failed
- `test_execution_failed`: Test execution error

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:test_config",
    "arguments": {
      "draft_id": "draft-abc123",
      "context": {"name": "Test User"},
      "dry_run": true
    }
  },
  "id": 1
}
```

---

### Tool: modify_config

**Purpose**: Apply incremental updates to a draft or persisted config

**Category**: Config lifecycle

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config_id` | string | Yes | - | Draft ID (draft-*) or permanent config ID |
| `updates` | object | Yes | - | Dictionary of updates to apply (merge strategy) |
| `create_backup` | boolean | No | `true` | Backup before modifying |

**Returns**:

```json
{
  "success": true,
  "config_id": "string",
  "config_type": "string",
  "validation_status": "valid|invalid",
  "backup_path": "string | null",
  "draft_id": "string | null",
  "duration_ms": "number"
}
```

**Errors**:
- `config_not_found`: config_id does not exist
- `modification_failed`: Update failed
- `not_implemented`: Modifying persisted configs not yet implemented

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:modify_config",
    "arguments": {
      "config_id": "draft-abc123",
      "updates": {
        "metadata": {"description": "Updated description"}
      },
      "create_backup": true
    }
  },
  "id": 1
}
```

---

### Tool: save_config

**Purpose**: Save draft config to filesystem with proper directory structure

**Category**: Config lifecycle

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `draft_id` | string | Yes | - | Draft to persist |
| `config_id` | string | Yes | - | Permanent ID (e.g., "meeting-themes", kebab-case) |
| `overwrite` | boolean | No | `false` | Allow overwriting existing config |

**Returns**:

```json
{
  "success": true,
  "config_path": "string",
  "config_id": "string",
  "config_type": "string",
  "backup_path": "string | null",
  "duration_ms": "number"
}
```

**Errors**:
- `draft_not_found`: draft_id does not exist
- `save_failed`: Config already exists (set overwrite=true)
- `save_execution_failed`: Save operation failed

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:save_config",
    "arguments": {
      "draft_id": "draft-abc123",
      "config_id": "meeting-themes",
      "overwrite": false
    }
  },
  "id": 1
}
```

---

## 2.3. Storage Management Tools (2 tools)

### Tool: cleanup_ephemeral

**Purpose**: Clean up old ephemeral storage versions based on retention policy

**Category**: Storage management

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `retention` | object | No | See below | Retention policy (see structure below) |
| `filter` | object | No | - | Filter criteria (see structure below) |
| `dry_run` | boolean | No | `false` | Preview mode - show what would be deleted |

**Retention Policy Structure**:
- `keep_versions` (number, default: 3): Minimum versions to keep
- `keep_days` (number, default: 7): Keep versions newer than N days
- `keep_latest` (boolean, default: true): Always preserve latest

**Filter Structure**:
- `content_ids` (array[string]): Specific content IDs to clean
- `older_than_days` (number): Only clean versions older than N days

**Returns**:

```json
{
  "success": true,
  "total_content_checked": "number",
  "total_versions_deleted": "number",
  "bytes_freed": "number",
  "content_cleaned": [
    {
      "content_id": "string",
      "versions_before": "number",
      "versions_after": "number",
      "versions_deleted": "number"
    }
  ],
  "dry_run": "boolean",
  "duration_ms": "number"
}
```

**Errors**:
- `invalid_retention`: Invalid retention policy parameters
- `storage_error`: Failed to access ephemeral storage

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:cleanup_ephemeral",
    "arguments": {
      "retention": {"keep_versions": 2, "keep_days": 3},
      "dry_run": true
    }
  },
  "id": 1
}
```

---

### Tool: delete_content

**Purpose**: Remove content from ephemeral storage with safety checks

**Category**: Storage management

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_id` | string | Yes | - | Content ID to delete from ephemeral storage |
| `preserve_metadata` | boolean | No | `false` | Keep metadata file but delete content |
| `force` | boolean | No | `false` | Delete even if referenced by artifacts |

**Returns**:

```json
{
  "success": true,
  "content_id": "string",
  "versions_deleted": "number",
  "bytes_freed": "number",
  "metadata_preserved": "boolean",
  "warnings": ["string"],
  "duration_ms": "number"
}
```

**Errors**:
- `content_not_found`: Content not found in ephemeral storage
- `referenced_by_artifacts`: Content is referenced (use force=true)
- `deletion_failed`: Delete operation failed

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:delete_content",
    "arguments": {
      "content_id": "old-content",
      "force": false
    }
  },
  "id": 1
}
```

---

## 2.4. Discovery Tools (6 tools)

### Tool: list_generators

**Purpose**: List all available content generators with metadata

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `generator_type` | string | No | - | Filter by type ("builtin" or "plugin"). None = all. |
| `include_plugins` | boolean | No | `true` | Include plugin generators in results |

**Returns**:

```json
{
  "success": true,
  "generators": [
    {
      "name": "string",
      "type": "builtin|plugin",
      "version": "string",
      "description": "string",
      "capabilities": ["string"]
    }
  ],
  "total_count": "number",
  "filtered": "boolean"
}
```

**Errors**:
- None (returns empty list if no generators found)

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_generators",
    "arguments": {
      "generator_type": "builtin",
      "include_plugins": false
    }
  },
  "id": 1
}
```

---

### Tool: list_content

**Purpose**: List all available content configurations with generation status

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter` | object | No | - | Optional filters (see structure below) |
| `sort` | string | No | `"id"` | Sort order (id, title, generator, modified) |
| `limit` | number | No | `100` | Maximum results (1-500) |

**Filter Structure**:
- `generator_type` (string): Filter by generator type
- `generated` (boolean): Filter by generation status
- `stage` (string): Filter by evolution stage

**Returns**:

```json
{
  "success": true,
  "total": "number",
  "returned": "number",
  "content": [
    {
      "id": "string",
      "title": "string",
      "purpose": "string",
      "generator_type": "string",
      "generated": "boolean",
      "stage": "string",
      "output_format": "string"
    }
  ],
  "duration_ms": "number"
}
```

**Errors**:
- `invalid_input`: Invalid sort or limit parameter

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_content",
    "arguments": {
      "filter": {"generator_type": "jinja2"},
      "sort": "title",
      "limit": 50
    }
  },
  "id": 1
}
```

---

### Tool: list_artifacts

**Purpose**: List all available artifact configurations with assembly status

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter` | object | No | - | Optional filters (see structure below) |
| `sort` | string | No | `"id"` | Sort order (id, title, assembled, modified) |
| `limit` | number | No | `100` | Maximum results (1-500) |

**Filter Structure**:
- `type` (string): Filter by artifact type
- `stage` (string): Filter by evolution stage
- `assembled` (boolean): Filter by assembly status

**Returns**:

```json
{
  "success": true,
  "total": "number",
  "returned": "number",
  "artifacts": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "assembled": "boolean",
      "component_count": "number",
      "output_path": "string"
    }
  ],
  "duration_ms": "number"
}
```

**Errors**:
- `invalid_input`: Invalid sort or limit parameter

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_artifacts",
    "arguments": {
      "filter": {"assembled": true},
      "sort": "modified",
      "limit": 20
    }
  },
  "id": 1
}
```

---

### Tool: trace_dependencies

**Purpose**: Trace content dependencies for an artifact configuration

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `artifact_config_id` | string | Yes | - | ID of artifact config to analyze |
| `check_status` | boolean | No | `true` | Check if each content piece exists (slower but more informative) |
| `show_metadata` | boolean | No | `false` | Include detailed metadata for each content |

**Returns**:

```json
{
  "success": true,
  "artifact_id": "string",
  "status": "ready|incomplete|missing_config",
  "total_dependencies": "number",
  "ready": "number",
  "missing": "number",
  "dependencies": [
    {
      "content_id": "string",
      "path": "string",
      "required": "boolean",
      "status": "ready|missing",
      "order": "number"
    }
  ],
  "assembly_order": ["string"],
  "missing_content_ids": ["string"] | null,
  "duration_ms": "number"
}
```

**Errors**:
- `config_not_found`: artifact_config_id does not exist
- `invalid_config`: Artifact config malformed

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:trace_dependencies",
    "arguments": {
      "artifact_config_id": "project-docs",
      "check_status": true,
      "show_metadata": false
    }
  },
  "id": 1
}
```

---

### Tool: list_content_configs

**Purpose**: List all available content configuration files (basic metadata only)

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter_pattern` | string | No | - | Optional glob pattern (e.g., "api*", "*-intro") |

**Returns**:

```json
{
  "success": true,
  "total": "number",
  "configs": [
    {
      "id": "string",
      "file_path": "string",
      "generator_type": "string",
      "description": "string",
      "title": "string"
    }
  ],
  "duration_ms": "number"
}
```

**Errors**:
- None (returns empty list if no configs found)

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_content_configs",
    "arguments": {
      "filter_pattern": "api*"
    }
  },
  "id": 1
}
```

---

### Tool: list_artifact_configs

**Purpose**: List all available artifact configuration files (basic metadata only)

**Category**: Discovery

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter_pattern` | string | No | - | Optional glob pattern (e.g., "report*", "*-bundle") |

**Returns**:

```json
{
  "success": true,
  "total": "number",
  "configs": [
    {
      "id": "string",
      "file_path": "string",
      "description": "string",
      "title": "string",
      "component_count": "number"
    }
  ],
  "duration_ms": "number"
}
```

**Errors**:
- None (returns empty list if no configs found)

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_artifact_configs",
    "arguments": {
      "filter_pattern": "report*"
    }
  },
  "id": 1
}
```

---

## 2.5. Validation Tools (2 tools)

### Tool: validate_content

**Purpose**: Validate content configuration or generated content quality

**Category**: Validation

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_or_config_id` | string | Yes | - | ID of config or generated content to validate |
| `validation_rules` | array[object] | No | - | Optional custom validation rules (see structure below) |

**Validation Rule Structure**:
- `type` (string): Rule type ("length", "required_fields")
- Rule-specific fields (e.g., `min_length`, `max_length`, `fields`)

**Returns**:

```json
{
  "success": true,
  "valid": "boolean",
  "issues": [
    {
      "severity": "error|warning|info",
      "code": "string",
      "message": "string",
      "location": "string",
      "details": {}
    }
  ],
  "error_count": "number",
  "warning_count": "number",
  "info_count": "number"
}
```

**Errors**:
- `config_not_found`: content_or_config_id does not exist
- `validation_execution_failed`: Validation failed to run

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:validate_content",
    "arguments": {
      "content_or_config_id": "api-docs",
      "validation_rules": [
        {"type": "length", "min_length": 100, "max_length": 10000}
      ]
    }
  },
  "id": 1
}
```

---

### Tool: check_freshness

**Purpose**: Check freshness status of all members in a collection (v1.5.0 - stigmergic context links)

**Category**: Validation (stigmergic)

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_config_path` | string | Yes | - | Path to collection configuration file (relative to `configs/collection/` or absolute) |
| `output_path` | string | No | - | Override the output base path (default from config) |

**Returns**:

```json
{
  "success": true,
  "collection_id": "string",
  "freshness_enabled": "boolean",
  "members": [
    {
      "member_id": "string",
      "generated_at": "string",
      "age_days": "number",
      "max_age_days": "number",
      "freshness_status": "fresh|stale|expired",
      "expires_at": "string"
    }
  ],
  "fresh_count": "number",
  "stale_count": "number",
  "expired_count": "number",
  "recommendation": "all_fresh|regenerate_stale|regenerate_expired",
  "checked_at": "string",
  "metadata": {
    "oldest_age_days": "number",
    "newest_age_days": "number",
    "average_age_days": "number"
  }
}
```

**Errors**:
- `config_not_found`: Collection config not found
- `invalid_config_id`: Path traversal attempt
- `manifest_not_found`: Collection not generated yet

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:check_freshness",
    "arguments": {
      "collection_config_path": "sap-004-complete",
      "output_path": null
    }
  },
  "id": 1
}
```

---

## 2.6. Collection Operations Tools (4 tools)

### Tool: generate_collection

**Purpose**: Generate a complete collection by assembling all member artifacts/collections

**Category**: Collection operations

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_config_path` | string | Yes | - | Path to collection configuration file (relative to `configs/collection/` or absolute) |
| `force` | boolean | No | `false` | Force regeneration of all members even if cached |
| `force_members` | array[string] | No | - | List of specific member IDs to force regenerate |
| `output_path` | string | No | - | Override the output base path specified in collection config |

**Returns**:

```json
{
  "success": true,
  "collection_id": "string",
  "collection_name": "string",
  "members": [
    {
      "id": "string",
      "type": "artifact|collection",
      "status": "success|failed|skipped",
      "cache_used": "boolean",
      "error": "string | null"
    }
  ],
  "manifest_path": "string",
  "generation_time_seconds": "number",
  "total_members": "number",
  "successful_members": "number",
  "failed_members": "number",
  "metadata": {
    "cached_members": "number",
    "regenerated_members": "number",
    "propagation_mode": "string",
    "strategy": "string"
  }
}
```

**Errors**:
- `config_not_found`: Collection config not found
- `invalid_config_id`: Path traversal attempt
- `composition_failed`: Collection generation failed
- `validation_failed`: Validation rules not met
- `circular_reference`: Circular nesting detected
- `max_depth_exceeded`: Nesting depth > 10

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:generate_collection",
    "arguments": {
      "collection_config_path": "sap-004-testing-framework",
      "force": false,
      "force_members": ["charter", "protocol"]
    }
  },
  "id": 1
}
```

---

### Tool: validate_collection_config

**Purpose**: Validate collection configuration schema and member references

**Category**: Collection operations

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_config_path` | string | Yes | - | Path to collection configuration file |
| `check_member_configs` | boolean | No | `true` | Verify all member configs exist |

**Returns**:

```json
{
  "success": true,
  "valid": "boolean",
  "collection_id": "string",
  "issues": [
    {
      "severity": "error|warning|info",
      "code": "string",
      "message": "string",
      "member_id": "string | null"
    }
  ],
  "error_count": "number",
  "warning_count": "number",
  "metadata": {
    "total_members": "number",
    "missing_configs": ["string"]
  }
}
```

**Errors**:
- `config_not_found`: Collection config not found
- `validation_failed`: Schema validation failed

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:validate_collection_config",
    "arguments": {
      "collection_config_path": "sap-004-testing-framework",
      "check_member_configs": true
    }
  },
  "id": 1
}
```

---

### Tool: list_collection_members

**Purpose**: List all members of a collection with their status and metadata

**Category**: Collection operations

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_config_path` | string | Yes | - | Path to collection configuration file |
| `check_status` | boolean | No | `true` | Check if each member has been generated |
| `recursive` | boolean | No | `false` | Include nested collection members |

**Returns**:

```json
{
  "success": true,
  "collection_id": "string",
  "members": [
    {
      "id": "string",
      "type": "artifact|collection",
      "title": "string",
      "description": "string",
      "generated": "boolean",
      "output_path": "string | null",
      "member_count": "number | null"
    }
  ],
  "total_members": "number",
  "generated_members": "number",
  "duration_ms": "number"
}
```

**Errors**:
- `config_not_found`: Collection config not found

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:list_collection_members",
    "arguments": {
      "collection_config_path": "sap-004-testing-framework",
      "check_status": true,
      "recursive": false
    }
  },
  "id": 1
}
```

---

### Tool: check_collection_cache

**Purpose**: Check cache status for a collection to determine if regeneration is needed

**Category**: Collection operations

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_config_path` | string | Yes | - | Path to collection configuration file |
| `check_member_cache` | boolean | No | `true` | Check cache status for individual members |
| `output_path` | string | No | - | Override output base path |

**Returns**:

```json
{
  "success": true,
  "collection_id": "string",
  "cache_valid": "boolean",
  "manifest_exists": "boolean",
  "members_cached": "number",
  "members_stale": "number",
  "stale_members": ["string"],
  "recommendation": "use_cache|regenerate_all|regenerate_stale",
  "metadata": {
    "manifest_path": "string",
    "last_generated": "string | null"
  }
}
```

**Errors**:
- `config_not_found`: Collection config not found

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:check_collection_cache",
    "arguments": {
      "collection_config_path": "sap-004-testing-framework",
      "check_member_cache": true
    }
  },
  "id": 1
}
```

---

## 2.7. Utility Tools (1 tool)

### Tool: hello_world

**Purpose**: Test tool to validate MCP connection and server status

**Category**: Utility

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | string | No | `"World"` | Name to greet |

**Returns**:

```json
{
  "message": "string",
  "version": "string",
  "tools_available": "number",
  "status": "string",
  "transport": "string"
}
```

**Errors**:
- None (simple test tool always succeeds)

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "choracompose:hello_world",
    "arguments": {
      "name": "Claude"
    }
  },
  "id": 1
}
```

---

## 2.8. Tool Category Summary

| Category | Tool Count | Tools |
|----------|------------|-------|
| **Core Generation** | 5 | generate_content, assemble_artifact, regenerate_content, preview_generation, batch_generate |
| **Config Lifecycle** | 4 | draft_config, test_config, modify_config, save_config |
| **Storage Management** | 2 | cleanup_ephemeral, delete_content |
| **Discovery** | 6 | list_generators, list_content, list_artifacts, trace_dependencies, list_content_configs, list_artifact_configs |
| **Validation** | 2 | validate_content, check_freshness |
| **Collection Operations** | 4 | generate_collection, validate_collection_config, list_collection_members, check_collection_cache |
| **Utility** | 1 | hello_world |
| **TOTAL** | **24** | |

---

## 3. Integration Patterns

This section describes how SAP-018 (chora-compose Meta) integrates with the broader SAP ecosystem, external systems, and provides common usage patterns for AI agents and developers.

### SAP Framework Integration

#### Integration with SAP-000 (SAP Framework Core)

**Integration Point**: Protocol Conformance

SAP-018 implements the standard 5-document SAP structure defined in SAP-000:
- **capability-charter.md** - Problem statement and scope
- **protocol-spec.md** - This document (technical specification)
- **awareness-guide.md** - AI agent quick reference
- **adoption-blueprint.md** - Installation and setup guide
- **ledger.md** - Version history and adoption tracking

**Configuration**: None required (structural conformance)

**Example Reference**:
```markdown
# In any SAP document, reference SAP-018 tools:
See [SAP-018 Protocol Spec](../chora-compose-meta/protocol-spec.md#2-mcp-tools-specification)
for complete MCP tool documentation.
```

**Key Pattern**: SAP-018 serves as the **meta-documentation** for chora-compose itself, demonstrating self-documentation through the same MCP tools it documents.

---

#### Integration with SAP-017 (chora-compose Integration Guide)

**Integration Point**: Implementation Bridge

SAP-017 provides the **how-to adoption guide** for integrating chora-compose into projects, while SAP-018 provides the **technical specification** of what chora-compose can do.

**Relationship**:
- **SAP-017**: "Here's how to install and configure chora-compose MCP server"
- **SAP-018**: "Here's every MCP tool, its parameters, schemas, and behavior"

**Example Workflow**:
```markdown
1. Developer reads SAP-017 to install chora-compose
2. Developer reads SAP-018 to understand available MCP tools
3. Developer uses SAP-018 tool specs to build integrations
4. AI agent uses SAP-018 awareness-guide for tool selection
```

**Configuration**: None required (complementary documentation)

---

### MCP Protocol Integration

#### Claude Desktop Integration

**Integration Point**: Model Context Protocol (MCP) Server

chora-compose v1.5.0 exposes 24 MCP tools via `claude_desktop_config.json`:

**Configuration**:
```json
{
  "mcpServers": {
    "chora-compose": {
      "command": "poetry",
      "args": ["run", "chora-compose-mcp"],
      "cwd": "/path/to/chora-compose",
      "env": {
        "CHORA_BASE_PATH": "/path/to/chora-compose"
      }
    }
  }
}
```

**Tool Discovery**:
- Tools auto-register on server startup
- Claude Desktop shows all 24 tools in UI
- Tools use namespace: `choracompose:` (e.g., `choracompose:generate_content`)

**Example Usage** (via Claude Desktop):
```
User: "Generate the README content using the readme-content config"

Claude calls: choracompose:generate_content
  {
    "content_config_id": "readme-content",
    "context": {},
    "force": false
  }
```

---

#### Gateway/Orchestration Layer Integration (v1.3.0+)

**Integration Point**: Event Emission & Trace Propagation

**Event Emission**:
```bash
# Events written to OpenTelemetry-compatible JSONL
var/telemetry/events.jsonl
```

**Event Types**:
- `content_generated` - Content piece generated
- `artifact_assembled` - Artifact assembled from content
- `validation_completed` - Validation rules executed

**Trace Context Propagation**:
```bash
# Set trace ID before MCP server starts
export CHORA_TRACE_ID="trace-abc123"

# All events will include trace_id field
{"event_type": "content_generated", "trace_id": "trace-abc123", ...}
```

**Gateway Discovery**:
```json
// GET capabilities://server
{
  "name": "chora-compose",
  "version": "1.5.0",
  "concurrency_limits": {
    "max_parallel_generations": 4,
    "max_collection_concurrency": 3
  },
  "upstream_dependencies": ["jinja2", "anthropic"]
}
```

---

### Common Usage Patterns

#### Pattern 1: Conversational Config Creation

**Use Case**: AI agent creates config without file editing

**Workflow**:
```
1. draft_config (create ephemeral draft)
2. test_config (preview generation)
3. modify_config (refine based on feedback)
4. save_config (persist to filesystem)
```

**Example**:
```json
// Step 1: Draft
{
  "tool": "choracompose:draft_config",
  "arguments": {
    "config_type": "content",
    "config_data": {
      "id": "api-docs",
      "type": "content",
      "schemaRef": {"id": "content-schema", "version": "3.1"},
      "metadata": {
        "description": "API documentation",
        "version": "1.0.0"
      },
      "elements": [...]
    }
  }
}
// Returns: {"draft_id": "draft-abc123"}

// Step 2: Test
{
  "tool": "choracompose:test_config",
  "arguments": {
    "draft_id": "draft-abc123",
    "context": {"api_version": "2.0"}
  }
}
// Returns: {"preview_content": "# API Documentation v2.0..."}

// Step 3: Save
{
  "tool": "choracompose:save_config",
  "arguments": {
    "draft_id": "draft-abc123",
    "config_id": "api-docs"
  }
}
// Returns: {"config_path": "configs/content/api-docs.json"}
```

**Benefits**:
- 70% faster than file editing
- Zero IDE context switching
- Immediate preview feedback

---

#### Pattern 2: 3-Tier Collection Generation

**Use Case**: Generate complete documentation suite with shared context

**Workflow**:
```
1. generate_collection (orchestrates everything)
   ├─ Resolves shared context
   ├─ Generates artifacts in parallel
   │  ├─ Each artifact generates content pieces
   │  └─ Assembles into final output
   └─ Creates manifest with metadata
```

**Example**:
```json
{
  "tool": "choracompose:generate_collection",
  "arguments": {
    "collection_config_path": "sap-004-testing-framework",
    "force": false
  }
}
```

**Returns**:
```json
{
  "collection_id": "sap-004-testing-framework",
  "members": [
    {"id": "capability-charter", "status": "success", "cache_used": true},
    {"id": "protocol-spec", "status": "success", "cache_used": false},
    {"id": "awareness-guide", "status": "success", "cache_used": true},
    {"id": "adoption-blueprint", "status": "success", "cache_used": true},
    {"id": "ledger", "status": "success", "cache_used": true}
  ],
  "manifest_path": "outputs/collections/sap-004-testing-framework/manifest.json",
  "generation_time_seconds": 8.3
}
```

**Context Propagation Modes**:
- **MERGE** (default): Member context merges with shared context
- **OVERRIDE**: Member context overrides shared context
- **ISOLATE**: Members don't see shared context

---

#### Pattern 3: Batch Content Generation with Parallelism

**Use Case**: Generate multiple content pieces concurrently

**Example**:
```json
{
  "tool": "choracompose:batch_generate",
  "arguments": {
    "content_ids": ["readme-intro", "changelog", "license"],
    "shared_context": {"project": "myapp", "version": "2.0"},
    "max_parallel": 3,
    "force": false
  }
}
```

**Returns**:
```json
{
  "total": 3,
  "successful": 3,
  "failed": 0,
  "results": [
    {"content_id": "readme-intro", "status": "generated"},
    {"content_id": "changelog", "status": "generated"},
    {"content_id": "license", "status": "skipped"}  // Already cached
  ],
  "duration_ms": 1245
}
```

**Performance**:
- Parallel execution: 2.6-4.8× speedup vs sequential
- SHA-256 cache: 94%+ cache hit rates in CI/CD

---

#### Pattern 4: Freshness Validation (Stigmergic Context Links)

**Use Case**: Check if collection members need regeneration

**Example**:
```json
{
  "tool": "choracompose:check_freshness",
  "arguments": {
    "collection_config_path": "sap-004-complete"
  }
}
```

**Returns**:
```json
{
  "freshness_enabled": true,
  "members": [
    {
      "member_id": "charter",
      "age_days": 2,
      "max_age_days": 7,
      "freshness_status": "fresh"
    },
    {
      "member_id": "protocol",
      "age_days": 15,
      "max_age_days": 7,
      "freshness_status": "stale"
    }
  ],
  "recommendation": "regenerate_stale"
}
```

**Use Cases**:
- CI/CD: Regenerate stale docs before deployment
- Project maintenance: Identify outdated documentation
- Coordination: Track dependencies across repositories

---

## 4. Data Structures

This section defines the core data structures used by chora-compose v1.5.0, including JSON Schema specifications and runtime object formats.

### 4.1. Content Configuration Schema (JSON Schema v3.1)

**Description**: Defines atomic content pieces for ephemeral generation

**Format**: JSON (validated against JSON Schema Draft 2020-12)

**Schema Location**: `schemas/content/v3.1/schema.json`

**Required Fields**:
```json
{
  "type": "content",
  "id": "kebab-case-identifier",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Brief description (1-500 chars)",
    "version": "1.0.0"
  },
  "elements": [
    {
      "name": "element-name",
      "format": "markdown|code|text|json|yaml|gherkin|section"
    }
  ]
}
```

**Key Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "content" |
| `id` | string | Yes | Unique ID (kebab-case: `^[a-z][a-z0-9-]*$`) |
| `schemaRef` | object | Yes | Schema reference (`{id: "content-schema", version: "3.1"}`) |
| `metadata.description` | string | Yes | Brief description (1-500 chars) |
| `metadata.version` | string | Yes | Semver version (`1.0.0`) |
| `metadata.generation_frequency` | enum | No | `manual`, `on_demand`, `scheduled`, `continuous` |
| `metadata.output_format` | enum | No | Expected output format |
| `instructions.global` | string | No | High-level guidance for generation |
| `instructions.system_prompt` | string | No | AI system-level prompt |
| `instructions.user_prompt` | string | No | AI user-level task specification |
| `inputs.sources` | array | No | External data sources (see §4.4) |
| `ephemeralStorage` | object | No | Storage configuration |
| `elements` | array | Yes | Content elements (min 1) |
| `children` | array | No | Sub-content config references |
| `generation.patterns` | array | No | Generation strategies |
| `validation.rules` | array | No | Validation rules |
| `evolution.stage` | enum | No | `draft`, `review`, `approved`, `deprecated` |

**Element Structure**:
```json
{
  "name": "element-id",
  "description": "What this element represents",
  "prompt_guidance": "Specific guidance for generating this element",
  "format": "markdown|code|text|json|yaml|gherkin|section",
  "output_format": "python|javascript|typescript (for code format)",
  "example_output": "Actual content or example",
  "generation_source": "ai|human|template|mixed",
  "review_status": "pending|approved|needs_revision",
  "human_feedback": "Optional reviewer notes"
}
```

**Full Example**:
```json
{
  "type": "content",
  "id": "readme-intro",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Introduction section for project README",
    "version": "1.0.0",
    "generation_frequency": "manual",
    "output_format": "markdown"
  },
  "instructions": {
    "global": "Provide welcoming, concise introduction",
    "system_prompt": "You are a technical writer creating project documentation",
    "user_prompt": "Write an introduction explaining the project purpose"
  },
  "inputs": {
    "sources": [
      {
        "id": "project-metadata",
        "source_type": "external_file",
        "source_locator": "package.json",
        "data_selector": "$.description",
        "required": true
      }
    ]
  },
  "ephemeralStorage": {
    "basePath": "ephemeral/content",
    "subfolderPattern": "<content-id>/<version>",
    "filenamePattern": "<dttm-utc>.json",
    "format": "json"
  },
  "elements": [
    {
      "name": "intro-paragraph",
      "description": "Opening paragraph",
      "format": "markdown",
      "generation_source": "ai",
      "review_status": "approved"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "jinja2-generation",
        "type": "jinja2",
        "template": "intro.j2"
      }
    ]
  },
  "validation": {
    "rules": [
      {
        "id": "intro-presence",
        "check_type": "presence",
        "target": "element.intro-paragraph",
        "severity": "error"
      }
    ]
  },
  "evolution": {
    "stage": "approved",
    "history": [
      {
        "date": "2025-01-15",
        "type": "creation",
        "description": "Initial content config"
      }
    ]
  }
}
```

---

### 4.2. Artifact Configuration Schema (JSON Schema v3.1)

**Description**: Defines how content pieces are composed into final artifacts

**Format**: JSON (validated against JSON Schema Draft 2020-12)

**Schema Location**: `schemas/artifact/v3.1/schema.json`

**Required Fields**:
```json
{
  "type": "artifact",
  "id": "kebab-case-identifier",
  "schemaRef": {
    "id": "artifact-schema",
    "version": "3.1"
  },
  "metadata": {
    "title": "Human-readable title",
    "purpose": "Detailed explanation",
    "outputs": [
      {
        "file": "path/to/output.md",
        "format": "markdown"
      }
    ]
  },
  "content": {
    "children": [
      {
        "id": "content-config-id",
        "path": "configs/content/content-config-id.json"
      }
    ]
  }
}
```

**Key Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "artifact" |
| `id` | string | Yes | Unique ID (kebab-case) |
| `schemaRef` | object | Yes | Schema reference (`{id: "artifact-schema", version: "3.1"}`) |
| `metadata.title` | string | Yes | Human-readable title (1-200 chars) |
| `metadata.type` | enum | No | `documentation`, `test`, `code`, `configuration`, `report`, `mixed` |
| `metadata.purpose` | string | Yes | Detailed explanation (1-1000 chars) |
| `metadata.outputs` | array | Yes | Output file specifications (min 1) |
| `metadata.compositionStrategy` | enum | No | `concat` (default), `merge`, `template`, `custom` |
| `content.children` | array | Yes | Content config references (min 1) |
| `dependencies` | array | No | External dependencies for traceability |
| `validation.rules` | array | No | Artifact-level validation rules |
| `evolution.stage` | enum | No | `draft`, `review`, `approved`, `deprecated` |

**Output Specification**:
```json
{
  "file": "README.md",
  "format": "markdown|code|binary|bdd|test_results|json|yaml|text|html|xml",
  "language_dialect": "python|javascript|typescript|gherkin|java",
  "encoding": "utf-8"
}
```

**Child Reference Structure**:
```json
{
  "id": "readme-intro",
  "path": "configs/content/readme-intro.json",
  "required": true,
  "order": 1,
  "version": "1.0.0",
  "retrievalStrategy": "latest|all|version|approved_only",
  "expected_source": "ai|human|template|mixed|any",
  "review_required": false,
  "conditions": "Optional conditional logic",
  "notes": "Additional notes"
}
```

**Full Example**:
```json
{
  "type": "artifact",
  "id": "project-readme",
  "schemaRef": {
    "id": "artifact-schema",
    "version": "3.1"
  },
  "metadata": {
    "title": "Project README Documentation",
    "type": "documentation",
    "version": "2.0.0",
    "purpose": "Generate complete README.md from modular content pieces",
    "outputs": [
      {
        "file": "README.md",
        "format": "markdown",
        "encoding": "utf-8"
      }
    ],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "readme-intro",
        "path": "configs/content/readme-intro.json",
        "required": true,
        "order": 1,
        "retrievalStrategy": "latest",
        "review_required": true
      },
      {
        "id": "installation",
        "path": "configs/content/installation.json",
        "required": true,
        "order": 2,
        "retrievalStrategy": "approved_only"
      },
      {
        "id": "usage",
        "path": "configs/content/usage.json",
        "required": true,
        "order": 3
      }
    ]
  },
  "dependencies": [
    {
      "id": "api-reference",
      "type": "artifact",
      "locator": "api-docs-artifact",
      "relationship": "related_to",
      "notes": "README references API docs"
    }
  ],
  "validation": {
    "rules": [
      {
        "id": "completeness-check",
        "check_type": "completeness",
        "target": "content.children",
        "severity": "error"
      }
    ]
  },
  "evolution": {
    "stage": "approved"
  }
}
```

---

### 4.3. Collection Configuration Schema (JSON Schema v1.0)

**Description**: Defines multi-artifact collections with shared context and coordination

**Format**: JSON (validated against JSON Schema Draft 07)

**Schema Location**: `schemas/collection/v1.0/schema.json`

**Required Fields**:
```json
{
  "type": "collection",
  "id": "collection-id",
  "name": "Human-readable name",
  "members": [
    {
      "id": "member-id",
      "type": "artifact|collection",
      "path": "path/to/config.json"
    }
  ],
  "output": {
    "base_path": "output/path"
  }
}
```

**Key Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "collection" |
| `id` | string | Yes | Unique ID (lowercase alphanumeric + hyphens) |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Collection description |
| `members` | array | Yes | Artifact/collection members (min 1) |
| `context.shared.sources` | array | No | Shared context inputs |
| `context.propagation` | enum | No | `merge` (default), `override`, `isolate` |
| `context.overrides` | object | No | Per-member context overrides |
| `generation.strategy` | enum | No | `parallel` (default), `sequential` |
| `generation.concurrency_limit` | number | No | Max concurrent generations (default 3) |
| `generation.force` | boolean | No | Bypass cache (default false) |
| `generation.force_members` | array | No | Specific members to force regenerate |
| `output.base_path` | string | Yes | Base output path (supports Jinja2 templates) |
| `output.structure` | enum | No | `flat`, `nested` (default), `custom` |
| `output.manifest` | boolean | No | Generate manifest.json (default true) |
| `validation.rules` | array | No | Collection-level validation rules |

**Member Specification**:
```json
{
  "id": "capability-charter",
  "type": "artifact",
  "path": "sap-004/capability-charter.json",
  "order": 1,
  "required": true,
  "context_override": {
    "sources": [
      {
        "type": "inline_data",
        "data": {
          "artifact_focus": "Define capabilities"
        }
      }
    ]
  }
}
```

**Context Propagation Modes**:

1. **MERGE** (default):
   ```
   Final Context = Shared Context + Member Context
   (Member keys override shared keys on conflict)
   ```

2. **OVERRIDE**:
   ```
   Final Context = Member Context ONLY
   (Shared context ignored)
   ```

3. **ISOLATE**:
   ```
   Final Context = Member Context
   (Each member isolated, no shared context)
   ```

**Full Example**:
```json
{
  "type": "collection",
  "id": "sap-004-testing-framework",
  "name": "SAP-004: Testing Framework",
  "description": "Complete SAP documentation suite",
  "members": [
    {
      "id": "capability-charter",
      "type": "artifact",
      "path": "sap-004/capability-charter.json",
      "order": 1,
      "required": true
    },
    {
      "id": "protocol-spec",
      "type": "artifact",
      "path": "sap-004/protocol-spec.json",
      "order": 2,
      "required": true
    },
    {
      "id": "awareness-guide",
      "type": "artifact",
      "path": "sap-004/awareness-guide.json",
      "order": 3,
      "required": true
    }
  ],
  "context": {
    "shared": {
      "sources": [
        {
          "type": "inline_data",
          "data": {
            "sap_id": "SAP-004",
            "sap_name": "testing-framework",
            "project_name": "Chora Compose"
          }
        },
        {
          "type": "external_file",
          "path": "sap-catalog.json"
        }
      ]
    },
    "propagation": "merge"
  },
  "generation": {
    "strategy": "parallel",
    "concurrency_limit": 3,
    "force": false
  },
  "output": {
    "base_path": "outputs/collections/{{collection_id}}",
    "structure": "nested",
    "manifest": true
  },
  "validation": {
    "rules": [
      {
        "type": "all_members_present",
        "required": true
      }
    ],
    "fail_fast": true
  }
}
```

---

### 4.4. Context Input Sources

**Description**: Unified format for resolving external data into context

**Source Types** (6 types):

**1. `inline_data`**: Embedded JSON data
```json
{
  "type": "inline_data",
  "data": {
    "project": "myapp",
    "version": "2.0"
  }
}
```

**2. `external_file`**: Load from filesystem
```json
{
  "type": "external_file",
  "path": "package.json",
  "selector": "$.version"
}
```

**3. `git_reference`**: Load from git commit/branch
```json
{
  "type": "git_reference",
  "repo": "/path/to/repo",
  "file": "README.md",
  "selector": "# Installation"
}
```

**4. `content_config`**: Reference another content config
```json
{
  "type": "content_config",
  "config_id": "api-docs",
  "selector": "$.metadata.version"
}
```

**5. `artifact_config`**: Reference artifact config data
```json
{
  "type": "artifact_config",
  "config_id": "readme-artifact",
  "selector": "$.metadata.title"
}
```

**6. `ephemeral_output`**: Retrieve from ephemeral storage
```json
{
  "type": "ephemeral_output",
  "output_id": "readme-intro",
  "selector": "$.content"
}
```

---

### 4.5. Manifest Structure (Collection Output)

**Description**: Generated metadata for collection runs

**Format**: JSON

**Location**: `{output.base_path}/manifest.json`

**Structure**:
```json
{
  "collection_id": "sap-004-testing-framework",
  "collection_name": "SAP-004: Testing Framework",
  "generated_at": "2025-11-04T12:00:00Z",
  "generation_time_seconds": 8.3,
  "total_members": 5,
  "successful_members": 5,
  "failed_members": 0,
  "members": [
    {
      "id": "capability-charter",
      "type": "artifact",
      "status": "success",
      "output_path": "outputs/collections/sap-004/charter/capability-charter.md",
      "generation_time_seconds": 1.2,
      "cache_used": true,
      "context_hash": "sha256:abc123...",
      "error": null
    }
  ],
  "context": {
    "shared": {
      "sap_id": "SAP-004",
      "sap_name": "testing-framework"
    },
    "propagation_mode": "merge"
  },
  "validation": {
    "passed": true,
    "rules_evaluated": 1
  },
  "cache_stats": {
    "total_members": 5,
    "cache_hits": 4,
    "cache_misses": 1,
    "cache_hit_rate": 0.8
  }
}
```

---

### 4.6. Ephemeral Storage Format

**Description**: Versioned content storage structure

**Directory Layout**:
```
ephemeral/
├── content/
│   ├── readme-intro/
│   │   ├── v1/
│   │   │   ├── 2025-11-04T10-00-00Z.json
│   │   │   └── metadata.json
│   │   └── v2/
│   │       ├── 2025-11-04T11-00-00Z.json
│   │       └── metadata.json
│   └── changelog/
│       └── v1/
│           ├── 2025-11-04T10-05-00Z.json
│           └── metadata.json
└── drafts/
    ├── draft-abc123.json
    └── draft-def456.json
```

**Content File Format**:
```json
{
  "content_id": "readme-intro",
  "version": "1.0.0",
  "generated_at": "2025-11-04T10:00:00Z",
  "generator_type": "jinja2",
  "context_hash": "sha256:abc123...",
  "content": "# Project Introduction\n\nWelcome to...",
  "metadata": {
    "generation_time_ms": 345,
    "context_variables": ["project_name", "version"]
  }
}
```

**Metadata File Format**:
```json
{
  "content_id": "readme-intro",
  "version": "1.0.0",
  "total_generations": 12,
  "latest_generation": "2025-11-04T10:00:00Z",
  "oldest_generation": "2025-10-01T08:00:00Z",
  "retention_policy": {
    "keep_versions": 3,
    "keep_days": 30
  }
}
```

---

## 5. File Structure

This section documents the expected file and directory structure for chora-compose projects.

### 5.1. Standard chora-compose Project Layout

**Directory Layout**:
```
project-root/
├── configs/                      # Configuration directory
│   ├── content/                  # Content configurations (JSON v3.1)
│   │   ├── readme/
│   │   │   ├── readme-content.json
│   │   │   └── readme-data.json  # Optional: External data files
│   │   ├── changelog/
│   │   │   └── changelog-content.json
│   │   └── api-docs/
│   │       ├── api-docs-content.json
│   │       └── api-data.json
│   ├── artifact/                 # Artifact configurations (JSON v3.1)
│   │   ├── readme-artifact.json
│   │   ├── documentation-bundle/
│   │   │   └── documentation-bundle-artifact.json
│   │   └── api-docs-artifact.json
│   ├── collection/               # Collection configurations (JSON v1.0)
│   │   ├── sap-004-testing-framework.json
│   │   ├── documentation-suite.json
│   │   └── cross-repo-coordination.json
│   └── templates/                # Jinja2 templates
│       ├── readme.j2
│       ├── changelog.j2
│       └── api-docs/
│           ├── endpoint.j2
│           └── overview.j2
├── schemas/                      # JSON Schema definitions
│   ├── content/
│   │   └── v3.1/
│   │       └── schema.json       # Content config schema
│   ├── artifact/
│   │   └── v3.1/
│   │       └── schema.json       # Artifact config schema
│   └── collection/
│       └── v1.0/
│           └── schema.json       # Collection config schema
├── ephemeral/                    # Ephemeral storage (generated, gitignored)
│   ├── content/
│   │   ├── readme-intro/
│   │   │   └── v1/
│   │   │       ├── 2025-11-04T10-00-00Z.json
│   │   │       └── metadata.json
│   │   └── changelog/
│   │       └── v1/
│   │           ├── 2025-11-04T10-05-00Z.json
│   │           └── metadata.json
│   └── drafts/                   # Draft configs (30-day retention)
│       ├── draft-abc123.json
│       └── draft-def456.json
├── outputs/                      # Final artifacts (gitignored or committed)
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── collections/
│   │   └── sap-004-testing-framework/
│   │       ├── capability-charter.md
│   │       ├── protocol-spec.md
│   │       ├── awareness-guide.md
│   │       ├── adoption-blueprint.md
│   │       ├── ledger.md
│   │       └── manifest.json
│   └── docs/
│       └── api/
│           └── api-docs.md
├── var/                          # Runtime data
│   └── telemetry/
│       └── events.jsonl          # OpenTelemetry events
├── src/                          # Source code (for chora-compose itself)
│   └── chora_compose/
│       ├── core/
│       ├── generators/
│       ├── mcp/
│       └── storage/
├── tests/                        # Test suite
│   ├── test_content_generation.py
│   ├── test_artifact_assembly.py
│   ├── test_collection_generation.py
│   └── fixtures/
│       ├── configs/
│       └── data/
├── .gitignore                    # Ignore ephemeral/, outputs/, var/
├── claude_desktop_config.json    # MCP server configuration
├── pyproject.toml                # Python dependencies (Poetry)
└── README.md                     # Project documentation
```

---

### 5.2. Configuration Directory Structure

**configs/content/**:
- **Purpose**: Atomic content piece definitions
- **Format**: JSON (validated against `schemas/content/v3.1/schema.json`)
- **Naming Convention**: `{content-id}-content.json` or subdirectory `{content-id}/...`
- **Required**: At least 1 content config per project
- **Example**: `configs/content/readme/readme-content.json`

**configs/artifact/**:
- **Purpose**: Artifact composition definitions
- **Format**: JSON (validated against `schemas/artifact/v3.1/schema.json`)
- **Naming Convention**: `{artifact-id}-artifact.json` or subdirectory `{artifact-id}/...`
- **Required**: At least 1 artifact config per project
- **Example**: `configs/artifact/readme-artifact.json`

**configs/collection/**:
- **Purpose**: Multi-artifact collection definitions
- **Format**: JSON (validated against `schemas/collection/v1.0/schema.json`)
- **Naming Convention**: `{collection-id}.json`
- **Required**: No (collections are optional)
- **Example**: `configs/collection/sap-004-testing-framework.json`

**configs/templates/**:
- **Purpose**: Jinja2 template files for template-based generators
- **Format**: Jinja2 template syntax
- **Naming Convention**: `{template-name}.j2`
- **Required**: Only if using Jinja2 or template_fill generators
- **Example**: `configs/templates/readme.j2`

---

### 5.3. Ephemeral Storage Structure

**ephemeral/content/{content-id}/v{version}/**:
- **Purpose**: Versioned generated content with metadata
- **Format**: JSON files with UTC timestamps
- **Filename Pattern**: `{YYYY-MM-DDThh-mm-ssZ}.json`
- **Retention**: Configurable (default: 30 days, keep last 3 versions)
- **Gitignored**: Yes (ephemeral data, not committed)

**ephemeral/drafts/**:
- **Purpose**: Draft configurations created via `draft_config` tool
- **Format**: JSON (content or artifact schema)
- **Filename Pattern**: `draft-{uuid}.json`
- **Retention**: 30 days
- **Lifecycle**: draft → test → modify → save (persists to configs/)

**metadata.json** (per content version):
- **Purpose**: Aggregate metadata for content version
- **Contains**: Total generations, latest/oldest timestamps, retention policy
- **Updated**: On each generation

---

### 5.4. Output Directory Structure

**outputs/** (root):
- **Purpose**: Final generated artifacts
- **Format**: Various (markdown, JSON, YAML, code files)
- **Gitignored**: Configurable (ephemeral outputs: yes, documentation: no)
- **Example**: `outputs/README.md`, `outputs/CHANGELOG.md`

**outputs/collections/{collection-id}/**:
- **Purpose**: Collection member outputs with manifest
- **Structure**: Nested subdirectories per member (configurable: flat/nested/custom)
- **Manifest**: `manifest.json` (generation metadata, cache stats, member status)
- **Example**: `outputs/collections/sap-004-testing-framework/`

---

### 5.5. Schema Directory Structure

**schemas/{config-type}/v{version}/schema.json**:
- **Purpose**: JSON Schema definitions for validation
- **Versions**:
  - `content/v3.1/schema.json` - Content config schema (JSON Schema Draft 2020-12)
  - `artifact/v3.1/schema.json` - Artifact config schema (JSON Schema Draft 2020-12)
  - `collection/v1.0/schema.json` - Collection config schema (JSON Schema Draft 07)
- **Required**: Yes (for schema validation)
- **Committed**: Yes (versioned schemas in git)

---

### 5.6. Key Files

**claude_desktop_config.json**:
- **Purpose**: MCP server configuration for Claude Desktop
- **Format**: JSON
- **Required**: Yes (for MCP integration)
- **Location**: Project root
- **Example**:
  ```json
  {
    "mcpServers": {
      "chora-compose": {
        "command": "poetry",
        "args": ["run", "chora-compose-mcp"],
        "cwd": "/path/to/chora-compose"
      }
    }
  }
  ```

**pyproject.toml**:
- **Purpose**: Python project metadata and dependencies
- **Format**: TOML
- **Required**: Yes (Poetry projects)
- **Contains**: Dependencies, tool configs (ruff, mypy, pytest)

**.gitignore**:
- **Purpose**: Exclude generated/ephemeral files from git
- **Required**: Yes
- **Typical Exclusions**:
  ```
  ephemeral/
  outputs/  # Or selectively commit documentation
  var/telemetry/
  __pycache__/
  *.pyc
  .pytest_cache/
  ```

**var/telemetry/events.jsonl**:
- **Purpose**: OpenTelemetry-compatible event log
- **Format**: JSONL (JSON Lines)
- **Required**: No (optional event emission)
- **Gitignored**: Yes
- **Event Types**: `content_generated`, `artifact_assembled`, `validation_completed`

---

## 6. Workflows

This section documents common workflows for using chora-compose MCP tools and configurations.

### 6.1. Basic Content Generation Workflow

**Purpose**: Generate a single content piece from a configured template

**Steps**:

1. **Create content configuration** (if not exists):
   ```json
   // configs/content/readme-intro.json
   {
     "type": "content",
     "id": "readme-intro",
     "schemaRef": {"id": "content-schema", "version": "3.1"},
     "metadata": {
       "description": "README introduction section",
       "version": "1.0.0",
       "output_format": "markdown"
     },
     "elements": [
       {
         "name": "intro",
         "format": "markdown",
         "example_output": "# Welcome to MyProject..."
       }
     ]
   }
   ```

2. **Generate content via MCP tool**:
   ```json
   {
     "tool": "choracompose:generate_content",
     "arguments": {
       "content_config_id": "readme-intro",
       "context": {},
       "force": false
     }
   }
   ```

3. **Verify generation**:
   ```bash
   ls ephemeral/content/readme-intro/v1/
   # Output: 2025-11-04T10-00-00Z.json, metadata.json
   ```

**Expected Output**:
```json
{
  "success": true,
  "content_id": "readme-intro",
  "status": "generated",
  "content": "# Welcome to MyProject...",
  "duration_ms": 234
}
```

---

### 6.2. Artifact Assembly Workflow

**Purpose**: Assemble multiple content pieces into final artifact

**Steps**:

1. **Create artifact configuration**:
   ```json
   // configs/artifact/readme-artifact.json
   {
     "type": "artifact",
     "id": "readme-artifact",
     "schemaRef": {"id": "artifact-schema", "version": "3.1"},
     "metadata": {
       "title": "Project README",
       "purpose": "Complete README from content pieces",
       "outputs": [{"file": "outputs/README.md", "format": "markdown"}]
     },
     "content": {
       "children": [
         {"id": "readme-intro", "path": "configs/content/readme-intro.json", "order": 1},
         {"id": "installation", "path": "configs/content/installation.json", "order": 2},
         {"id": "usage", "path": "configs/content/usage.json", "order": 3}
       ]
     }
   }
   ```

2. **Generate all content pieces** (if not cached):
   ```json
   {
     "tool": "choracompose:batch_generate",
     "arguments": {
       "content_ids": ["readme-intro", "installation", "usage"],
       "shared_context": {"project": "myapp"}
     }
   }
   ```

3. **Assemble artifact**:
   ```json
   {
     "tool": "choracompose:assemble_artifact",
     "arguments": {
       "artifact_config_id": "readme-artifact",
       "force": false
     }
   }
   ```

4. **Verify output**:
   ```bash
   cat outputs/README.md
   ```

**Expected Output**:
```json
{
  "success": true,
  "artifact_id": "readme-artifact",
  "output_path": "outputs/README.md",
  "content_count": 3,
  "status": "assembled",
  "duration_ms": 456
}
```

---

### 6.3. Collection Generation Workflow

**Purpose**: Generate complete documentation suite with shared context

**Steps**:

1. **Create collection configuration**:
   ```json
   // configs/collection/docs-suite.json
   {
     "type": "collection",
     "id": "docs-suite",
     "name": "Documentation Suite",
     "members": [
       {"id": "readme", "type": "artifact", "path": "readme-artifact.json"},
       {"id": "changelog", "type": "artifact", "path": "changelog-artifact.json"},
       {"id": "api-docs", "type": "artifact", "path": "api-docs-artifact.json"}
     ],
     "context": {
       "shared": {
         "sources": [
           {"type": "inline_data", "data": {"project": "myapp", "version": "2.0"}}
         ]
       },
       "propagation": "merge"
     },
     "generation": {
       "strategy": "parallel",
       "concurrency_limit": 3
     },
     "output": {
       "base_path": "outputs/collections/docs-suite",
       "manifest": true
     }
   }
   ```

2. **Generate collection**:
   ```json
   {
     "tool": "choracompose:generate_collection",
     "arguments": {
       "collection_config_path": "docs-suite",
       "force": false
     }
   }
   ```

3. **Verify outputs**:
   ```bash
   ls outputs/collections/docs-suite/
   # Output: readme/, changelog/, api-docs/, manifest.json
   ```

**Expected Output**:
```json
{
  "success": true,
  "collection_id": "docs-suite",
  "members": [
    {"id": "readme", "status": "success", "cache_used": false},
    {"id": "changelog", "status": "success", "cache_used": true},
    {"id": "api-docs", "status": "success", "cache_used": false}
  ],
  "manifest_path": "outputs/collections/docs-suite/manifest.json",
  "generation_time_seconds": 3.2
}
```

---

### 6.4. Conversational Config Lifecycle Workflow

**Purpose**: Create and refine config through conversation (no file editing)

**Steps**:

1. **Draft config**:
   ```json
   {
     "tool": "choracompose:draft_config",
     "arguments": {
       "config_type": "content",
       "config_data": {
         "type": "content",
         "id": "api-overview",
         "schemaRef": {"id": "content-schema", "version": "3.1"},
         "metadata": {"description": "API overview", "version": "1.0.0"},
         "elements": [{"name": "overview", "format": "markdown"}]
       },
       "description": "Draft API overview config"
     }
   }
   ```
   **Returns**: `{"draft_id": "draft-abc123"}`

2. **Test draft** (preview generation):
   ```json
   {
     "tool": "choracompose:test_config",
     "arguments": {
       "draft_id": "draft-abc123",
       "context": {"api_version": "v2"},
       "dry_run": true
     }
   }
   ```
   **Returns**: `{"preview_content": "# API Overview v2..."}`

3. **Modify draft** (refine based on preview):
   ```json
   {
     "tool": "choracompose:modify_config",
     "arguments": {
       "config_id": "draft-abc123",
       "updates": {
         "metadata": {"description": "Updated: API overview with examples"}
       }
     }
   }
   ```

4. **Re-test** (verify changes):
   ```json
   {
     "tool": "choracompose:test_config",
     "arguments": {"draft_id": "draft-abc123"}
   }
   ```

5. **Save to filesystem** (persist when satisfied):
   ```json
   {
     "tool": "choracompose:save_config",
     "arguments": {
       "draft_id": "draft-abc123",
       "config_id": "api-overview"
     }
   }
   ```
   **Returns**: `{"config_path": "configs/content/api-overview.json"}`

**Benefits**:
- 70% faster than traditional file editing
- Immediate preview feedback
- Zero IDE context switching
- Conversational refinement

---

### 6.5. Freshness Validation Workflow (v1.5.0)

**Purpose**: Check and regenerate stale collection members

**Steps**:

1. **Check freshness status**:
   ```json
   {
     "tool": "choracompose:check_freshness",
     "arguments": {
       "collection_config_path": "docs-suite"
     }
   }
   ```

   **Returns**:
   ```json
   {
     "members": [
       {"member_id": "readme", "age_days": 2, "freshness_status": "fresh"},
       {"member_id": "changelog", "age_days": 15, "freshness_status": "stale"},
       {"member_id": "api-docs", "age_days": 30, "freshness_status": "expired"}
     ],
     "recommendation": "regenerate_stale"
   }
   ```

2. **Regenerate stale/expired members**:
   ```json
   {
     "tool": "choracompose:generate_collection",
     "arguments": {
       "collection_config_path": "docs-suite",
       "force_members": ["changelog", "api-docs"]
     }
   }
   ```

3. **Verify freshness restored**:
   ```json
   {
     "tool": "choracompose:check_freshness",
     "arguments": {"collection_config_path": "docs-suite"}
   }
   ```

**Use Cases**:
- CI/CD: Regenerate stale docs before deployment
- Project maintenance: Identify outdated documentation
- Coordination: Track dependencies across repositories

---

## 7. Validation & Testing

This section defines validation rules and testing procedures for chora-compose configurations and generated content.

### 7.1. Schema Validation Rules

**Rule 1: Content Config Schema Compliance**
- **Check**: Content configuration must conform to JSON Schema v3.1
- **Requirement**: All required fields present, types correct, pattern matching
- **Validation Tool**: `choracompose:validate_content`
- **Error Message**: "Schema validation failed: {field} is required" or "Schema validation failed: {field} must match pattern {pattern}"

**Rule 2: Artifact Config Schema Compliance**
- **Check**: Artifact configuration must conform to JSON Schema v3.1
- **Requirement**: Valid schemaRef, outputs array non-empty, children references valid
- **Validation Tool**: `choracompose:validate_collection_config` (for artifacts)
- **Error Message**: "Schema validation failed: metadata.outputs must have at least 1 item"

**Rule 3: Collection Config Schema Compliance**
- **Check**: Collection configuration must conform to JSON Schema v1.0
- **Requirement**: Valid members array, valid propagation mode, output base_path specified
- **Validation Tool**: `choracompose:validate_collection_config`
- **Error Message**: "Schema validation failed: members must have at least 1 item"

**Rule 4: ID Pattern Validation**
- **Check**: Config IDs must use kebab-case pattern
- **Requirement**: `^[a-z][a-z0-9-]*$` (lowercase start, alphanumeric + hyphens)
- **Error Message**: "Invalid ID '{id}': must start with lowercase letter and contain only lowercase, digits, hyphens"

**Rule 5: Version Format Validation**
- **Check**: Version fields must use semver format
- **Requirement**: `^\d+\.\d+\.\d+$` (e.g., "1.0.0")
- **Error Message**: "Invalid version '{version}': must be in semver format (e.g., 1.0.0)"

### 7.2. Content Validation Approaches

**Approach 1: Presence Validation**
- **Check Type**: `presence`
- **Target**: Element or field existence
- **Example**:
  ```json
  {
    "id": "intro-presence",
    "check_type": "presence",
    "target": "element.intro",
    "threshold": 1.0,
    "severity": "error"
  }
  ```

**Approach 2: Format Validation**
- **Check Type**: `format`
- **Target**: Output format compliance (markdown, JSON, YAML)
- **Example**:
  ```json
  {
    "id": "json-format",
    "check_type": "format",
    "target": "generated_output",
    "check_config": {"format": "json"},
    "severity": "error"
  }
  ```

**Approach 3: Lint Validation**
- **Check Type**: `lint`
- **Target**: Code quality (requires external linter)
- **Example**:
  ```json
  {
    "id": "python-lint",
    "check_type": "lint",
    "target": "element.code",
    "check_config": {"linter": "ruff", "options": "--select=E,F"},
    "severity": "warning"
  }
  ```

**Approach 4: Custom Validation**
- **Check Type**: `custom`
- **Target**: Plugin-based validation
- **Requires**: Custom validator plugin

### 7.3. Testing Protocols

**Unit Tests** (chora-compose framework):
```bash
# Run all unit tests
poetry run pytest tests/

# Run specific test module
poetry run pytest tests/test_content_generation.py

# Run with coverage
poetry run pytest --cov=chora_compose --cov-report=html
```

**Integration Tests** (MCP tools):
```bash
# Test MCP server startup
poetry run chora-compose-mcp

# Test specific tool via MCP client
poetry run pytest tests/mcp_tests/test_generate_content.py

# Test collection generation end-to-end
poetry run pytest tests/integration/test_collection_workflow.py
```

**Manual Verification** (Config validation):
1. Create test content config in `configs/content/test-content.json`
2. Validate schema: `choracompose:validate_content` with `content_or_config_id="test-content"`
3. Generate content: `choracompose:generate_content` with `content_config_id="test-content"`
4. Verify output: Check `ephemeral/content/test-content/v1/` for generated file
5. Expected: Success response with `status="generated"`

**Performance Testing** (Benchmarks):
```bash
# Benchmark cache performance
poetry run pytest tests/benchmarks/test_cache_performance.py

# Benchmark parallel execution
poetry run pytest tests/benchmarks/test_parallel_generation.py

# Measure collection generation time
poetry run pytest tests/benchmarks/test_collection_benchmarks.py
```

---

## 8. Error Handling

This section documents common error conditions, error codes, and resolution strategies for chora-compose.

### 8.1. Common Error Patterns

All MCP tools return errors in this standardized format:
```json
{
  "success": false,
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

**Common Error Codes** (see Section 2 for complete list):
- `config_not_found`
- `validation_failed`
- `generation_failed`
- `invalid_context`
- `storage_error`
- `permission_denied`
- `internal_error`

---

### 8.2. Error Examples with Resolutions

**Error 1: config_not_found**

**Condition**: Content/artifact/collection config file does not exist

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "config_not_found",
    "message": "Content config 'readme-intro' not found",
    "details": {
      "config_id": "readme-intro",
      "searched_paths": [
        "configs/content/readme-intro.json",
        "configs/content/readme-intro/readme-intro-content.json"
      ]
    }
  }
}
```

**Resolution**:
1. Verify config ID spelling: `choracompose:list_content_configs`
2. Check config file exists: `ls configs/content/`
3. Create config if missing: `choracompose:draft_config` → `choracompose:save_config`

**Prevention**:
- Use `list_content_configs` to discover available configs before generating
- Follow naming convention: `{config-id}-content.json` or `{config-id}/{config-id}-content.json`

---

**Error 2: validation_failed**

**Condition**: Config does not conform to JSON Schema

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "validation_failed",
    "message": "Schema validation failed",
    "details": {
      "schema_errors": [
        {
          "path": "metadata.version",
          "message": "'1.0' does not match '^\\d+\\.\\d+\\.\\d+$'",
          "expected": "semver format (e.g., 1.0.0)"
        }
      ]
    }
  }
}
```

**Resolution**:
1. Fix schema errors: Update `metadata.version` to "1.0.0" (add patch version)
2. Validate manually: `choracompose:validate_content`
3. Re-save config: `choracompose:save_config`

**Prevention**:
- Use `draft_config` → `test_config` workflow (validates before saving)
- Reference schema files in `schemas/` for field requirements
- Use `validate_content` before generation

---

**Error 3: generation_failed**

**Condition**: Generator fails to produce output (template error, AI error)

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "generation_failed",
    "message": "Jinja2 generator failed: template not found",
    "details": {
      "generator_type": "jinja2",
      "template_path": "readme.j2",
      "error_type": "TemplateNotFound"
    }
  }
}
```

**Resolution**:
1. Check template exists: `ls configs/templates/readme.j2`
2. Verify template path in config: `configs/content/{id}.json` → `generation.patterns[].template`
3. Create template if missing or fix path reference

**Prevention**:
- Use `preview_generation` to test before full generation
- Keep templates in `configs/templates/` directory
- Use relative paths from project root

---

**Error 4: invalid_context**

**Condition**: Context parameter is not valid JSON

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "invalid_context",
    "message": "Context must be a JSON object",
    "details": {
      "received_type": "string",
      "expected_type": "object"
    }
  }
}
```

**Resolution**:
1. Parse JSON string: Change `"context": "{...}"` to `"context": {...}`
2. Verify JSON syntax: Use JSON validator
3. Re-call tool with correct format

**Prevention**:
- MCP tools auto-parse JSON strings (Claude Desktop compatibility)
- Pass object directly: `{"context": {"key": "value"}}`
- Avoid double-stringified JSON

---

**Error 5: storage_error**

**Condition**: Ephemeral storage operation fails (disk full, permissions)

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "storage_error",
    "message": "Failed to write ephemeral content",
    "details": {
      "path": "ephemeral/content/readme-intro/v1/",
      "error_type": "PermissionError"
    }
  }
}
```

**Resolution**:
1. Check disk space: `df -h`
2. Verify permissions: `ls -la ephemeral/`
3. Create directory if missing: `mkdir -p ephemeral/content/`
4. Fix permissions: `chmod 755 ephemeral/`

**Prevention**:
- Ensure `ephemeral/` directory exists and is writable
- Add to `.gitignore` (not committed)
- Monitor disk space in CI/CD

---

**Error 6: circular_reference**

**Condition**: Collection has circular nesting (collection A → collection B → collection A)

**Error Message**:
```json
{
  "success": false,
  "error": {
    "code": "circular_reference",
    "message": "Circular collection nesting detected",
    "details": {
      "chain": ["collection-a", "collection-b", "collection-a"],
      "max_depth": 10
    }
  }
}
```

**Resolution**:
1. Review collection configs: Check `members` arrays
2. Break circular reference: Remove member causing loop
3. Flatten hierarchy if needed

**Prevention**:
- Limit nesting depth (max 10 levels)
- Use `validate_collection_config` before generation
- Document collection dependencies

---

### 8.3. Debugging Strategies

**Strategy 1: Verbose Logging**
```bash
# Enable debug logging
export CHORA_LOG_LEVEL=DEBUG
poetry run chora-compose-mcp
```

**Strategy 2: Test in Isolation**
```json
// Test single content generation
{
  "tool": "choracompose:preview_generation",
  "arguments": {
    "content_config_id": "test",
    "show_metadata": true
  }
}
```

**Strategy 3: Trace Dependencies**
```json
// Check artifact dependencies
{
  "tool": "choracompose:trace_dependencies",
  "arguments": {
    "artifact_config_id": "readme",
    "check_status": true
  }
}
```

**Strategy 4: Validate Early**
```json
// Validate config before use
{
  "tool": "choracompose:validate_content",
  "arguments": {"content_or_config_id": "test"}
}
```

---

## 9. Performance Considerations

This section documents performance characteristics, benchmarks, and optimization strategies for chora-compose v1.5.0.

### 9.1. Performance Benchmarks

**Measured Performance** (from chora-compose test suite):

| Operation | Time (avg) | Notes |
|-----------|-----------|-------|
| Content generation (Jinja2) | 50-200ms | Template complexity dependent |
| Content generation (demonstration) | 10-30ms | Example output only |
| Artifact assembly (3 content pieces) | 100-400ms | Includes retrieval + concat |
| Collection generation (5 artifacts, parallel) | 2-5s | Parallelism with concurrency_limit=3 |
| Collection generation (5 artifacts, sequential) | 8-12s | No parallelism |
| Schema validation | 5-15ms | JSON Schema v3.1/v1.0 |
| Cache lookup (SHA-256) | 2-5ms | In-memory hash comparison |

**Cache Performance**:
- **Cache hit rate**: 94%+ in CI/CD environments (repeated builds)
- **Cache speedup**: 10-50× faster (skip generation, return cached content)
- **Cache invalidation**: SHA-256 context hash comparison

**Parallel Execution Benchmarks**:
- **2 parallel members**: 1.8× speedup vs sequential
- **3 parallel members**: 2.6× speedup vs sequential
- **5 parallel members**: 4.8× speedup vs sequential (with concurrency_limit=3)

### 9.2. Optimization Strategies

1. **Leverage SHA-256 Caching**
   - **When to use**: Repeated generations with identical context
   - **Impact**: 10-50× speedup, 94%+ cache hit rate in CI/CD
   - **Example**: Pass `force: false` (default) to MCP tools

2. **Parallel Collection Generation**
   - **When to use**: Collection with independent members
   - **Impact**: 2.6-4.8× speedup vs sequential
   - **Example**: Use `generation.strategy: "parallel"` with `concurrency_limit: 3`

3. **Selective Cache Bypass**
   - **When to use**: Regenerate specific stale members only
   - **Impact**: Regenerate only what's needed (vs full `force: true`)
   - **Example**: Use `force_members: ["member1", "member2"]` array

4. **Context Propagation Modes**
   - **When to use**: Large shared context + many members
   - **Impact**: Reduce context resolution overhead
   - **Example**: Use `propagation: "isolate"` if members don't need shared context

5. **Batch Generation**
   - **When to use**: Generate multiple independent content pieces
   - **Impact**: Single MCP call vs multiple calls (reduced overhead)
   - **Example**: Use `batch_generate` tool with `max_parallel: 3`

---

## 10. Security Considerations

This section documents security implications, risks, and mitigation strategies for chora-compose.

### 10.1. Security Requirements

1. **Template Injection Prevention**
   - **Risk**: Untrusted input in Jinja2 templates can execute arbitrary code
   - **Mitigation**: Never use user input directly in templates without sanitization; use `autoescape=True`; validate context data

2. **File System Access Controls**
   - **Risk**: Path traversal allows reading/writing arbitrary files
   - **Mitigation**: Restrict config paths to `configs/` subdirectories; validate file paths; use `Path.resolve()` to prevent `../` traversal

3. **Context Data Handling**
   - **Risk**: Sensitive data (API keys, secrets) leaked to logs/outputs
   - **Mitigation**: Never log full context; redact sensitive fields; use environment variables for secrets; exclude `var/telemetry/` from git

4. **Path Traversal Prevention**
   - **Risk**: Malicious config references files outside project directory
   - **Mitigation**: Validate all file paths in configs; reject paths containing `..`; use absolute or project-relative paths only

5. **Schema Validation Enforcement**
   - **Risk**: Malformed configs bypass validation, cause unexpected behavior
   - **Mitigation**: Validate ALL configs against JSON Schema before use; fail fast on validation errors

### 10.2. Sensitive Data

**Data Types**:
- API Keys (ANTHROPIC_API_KEY): Store in environment variables, never in configs
- Database credentials: Use external_file source with restricted permissions
- User PII: Redact in event logs and telemetry

**Storage**:
- Secrets: Environment variables or `.env` files (chmod 600, in .gitignore)
- Ephemeral data: `ephemeral/` directory (gitignored)
- Event logs: `var/telemetry/events.jsonl` (redacted sensitive fields, gitignored)

**Access Controls**:
- Config files: `chmod 644` (read-only for group/others)
- Ephemeral storage: `chmod 755` (writable by owner)
- Templates: `chmod 644` (read-only)

---

## 11. Versioning & Compatibility

This section documents the versioning strategy and compatibility requirements.

### 11.1. Version History

| Version | Date | Changes | Breaking |
|---------|------|---------|----------|
| 1.0.0 | 2025-11-04 | Initial SAP-018 specification with 24 MCP tools | N/A |

### 11.2. Compatibility Matrix

| SAP-018 Version | chora-compose Version | Required SAPs | Python | Notes |
|------|------------------------------|-------|--------|-------|
| 1.0.0 | v1.5.0+ | SAP-000, SAP-017 | 3.12+ | Freshness validation, collection generation |

**Schema Compatibility**:
- Content Config: JSON Schema v3.1 (chora-compose v1.0.0+)
- Artifact Config: JSON Schema v3.1 (chora-compose v1.0.0+)
- Collection Config: JSON Schema v1.0 (chora-compose v1.4.0+)

### 11.3. Migration Guides

**Migrating from v1.0.0 to future v2.0.0**:
1. Review breaking changes in changelog
2. Update schema references if JSON Schema v4.0 migration required
3. Test configs with `validate_content` and `validate_collection_config` tools
4. Update MCP tool calls if signatures changed

**Backward Compatibility**:
- SAP-018 v1.0.0 documents are compatible with chora-compose v1.5.0+
- Older chora-compose versions (v1.0-v1.4) support subset of tools (no collections)
- See [SAP-017 Adoption Blueprint](../chora-compose-integration/adoption-blueprint.md) for version-specific guidance

---

## 12. Examples

This section provides complete, working examples for common use cases.

### 12.1. Example 1: Basic Content Generation

**Scenario**: Generate a simple README introduction

**Content Config** (`configs/content/readme-intro.json`):
```json
{
  "type": "content",
  "id": "readme-intro",
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "README introduction",
    "version": "1.0.0",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "intro",
      "format": "markdown",
      "example_output": "# MyProject\n\nWelcome to MyProject..."
    }
  ],
  "generation": {
    "patterns": [{"id": "demo", "type": "demonstration"}]
  }
}
```

**MCP Tool Call**:
```json
{
  "tool": "choracompose:generate_content",
  "arguments": {
    "content_config_id": "readme-intro",
    "context": {},
    "force": false
  }
}
```

**Expected Result**:
```json
{
  "success": true,
  "content_id": "readme-intro",
  "status": "generated",
  "content": "# MyProject\n\nWelcome to MyProject...",
  "duration_ms": 45
}
```

### 12.2. Example 2: Artifact Assembly

**Scenario**: Assemble README from multiple content pieces

**Artifact Config** (`configs/artifact/readme-artifact.json`):
```json
{
  "type": "artifact",
  "id": "readme-artifact",
  "schemaRef": {"id": "artifact-schema", "version": "3.1"},
  "metadata": {
    "title": "Project README",
    "purpose": "Complete README from content pieces",
    "outputs": [{"file": "outputs/README.md", "format": "markdown"}]
  },
  "content": {
    "children": [
      {"id": "readme-intro", "path": "configs/content/readme-intro.json", "order": 1},
      {"id": "installation", "path": "configs/content/installation.json", "order": 2}
    ]
  }
}
```

**MCP Tool Call**:
```json
{
  "tool": "choracompose:assemble_artifact",
  "arguments": {
    "artifact_config_id": "readme-artifact",
    "force": false
  }
}
```

**Expected Result**:
```json
{
  "success": true,
  "artifact_id": "readme-artifact",
  "output_path": "outputs/README.md",
  "content_count": 2,
  "status": "assembled",
  "duration_ms": 234
}
```

### 12.3. Example 3: Collection Generation

**Scenario**: Generate SAP documentation suite with shared context

**Collection Config** (`configs/collection/sap-004.json`):
```json
{
  "type": "collection",
  "id": "sap-004",
  "name": "SAP-004: Testing Framework",
  "members": [
    {"id": "charter", "type": "artifact", "path": "sap-004/charter.json"},
    {"id": "protocol", "type": "artifact", "path": "sap-004/protocol.json"}
  ],
  "context": {
    "shared": {
      "sources": [
        {
          "type": "inline_data",
          "data": {"sap_id": "SAP-004", "project": "chora-compose"}
        }
      ]
    },
    "propagation": "merge"
  },
  "generation": {
    "strategy": "parallel",
    "concurrency_limit": 2
  },
  "output": {
    "base_path": "outputs/collections/sap-004",
    "manifest": true
  }
}
```

**MCP Tool Call**:
```json
{
  "tool": "choracompose:generate_collection",
  "arguments": {
    "collection_config_path": "sap-004",
    "force": false
  }
}
```

**Expected Result**:
```json
{
  "success": true,
  "collection_id": "sap-004",
  "members": [
    {"id": "charter", "status": "success", "cache_used": false},
    {"id": "protocol", "status": "success", "cache_used": true}
  ],
  "manifest_path": "outputs/collections/sap-004/manifest.json",
  "generation_time_seconds": 2.1
}
```

### 12.4. Example 4: Conversational Config Creation

**Scenario**: Create config through conversation (no file editing)

**Step 1: Draft**:
```json
{
  "tool": "choracompose:draft_config",
  "arguments": {
    "config_type": "content",
    "config_data": {
      "type": "content",
      "id": "api-docs",
      "schemaRef": {"id": "content-schema", "version": "3.1"},
      "metadata": {"description": "API documentation", "version": "1.0.0"},
      "elements": [{"name": "overview", "format": "markdown"}]
    }
  }
}
```
**Returns**: `{"draft_id": "draft-abc123"}`

**Step 2: Test**:
```json
{
  "tool": "choracompose:test_config",
  "arguments": {
    "draft_id": "draft-abc123",
    "context": {"api_version": "v2"}
  }
}
```
**Returns**: `{"preview_content": "# API Documentation v2..."}`

**Step 3: Save**:
```json
{
  "tool": "choracompose:save_config",
  "arguments": {
    "draft_id": "draft-abc123",
    "config_id": "api-docs"
  }
}
```
**Returns**: `{"config_path": "configs/content/api-docs.json"}`

---

## 13. Troubleshooting

This section provides solutions for common issues encountered with chora-compose.

### 13.1. Issue 1: Config Not Found

**Symptoms**:
- Error code: `config_not_found`
- Message: "Content config 'xyz' not found"
- MCP tool returns 404-equivalent error

**Diagnosis**:
```bash
# List available configs
choracompose:list_content_configs

# Search filesystem
ls configs/content/
find configs/ -name "*xyz*"
```

**Solution**:
1. Verify config ID spelling in tool call
2. Check file exists: `configs/content/{id}-content.json` or `{id}/{id}-content.json`
3. Verify schemaRef.id matches config type ("content-schema" for content configs)
4. Create config if missing: Use `draft_config` → `save_config` workflow

---

### 13.2. Issue 2: Generation Failed (Template Not Found)

**Symptoms**:
- Error code: `generation_failed`
- Message: "Jinja2 generator failed: template not found"
- Template path shown in error details

**Diagnosis**:
```bash
# Check template exists
ls configs/templates/
cat configs/content/{id}.json | grep template
```

**Solution**:
1. Create missing template: `touch configs/templates/{name}.j2`
2. Fix template path in config: Update `generation.patterns[].template` field
3. Use project-relative paths (from project root)
4. Test template syntax: Verify Jinja2 syntax is valid

---

### 13.3. Issue 3: Cache Not Invalidating

**Symptoms**:
- Content unchanged despite config updates
- `cache_used: true` in response but content outdated
- Expected fresh generation, got cached result

**Diagnosis**:
```bash
# Check context hash
cat ephemeral/content/{id}/v1/metadata.json | grep context_hash
```

**Solution**:
1. **Force regeneration**: Pass `force: true` to MCP tool
2. **Change context**: Modify context variables to trigger cache invalidation
3. **Clear cache manually**: Remove `ephemeral/content/{id}/` directory
4. **Verify cache logic**: SHA-256 hash includes context + config content

---

### 13.4. Issue 4: Collection Generation Timeout

**Symptoms**:
- Collection generation exceeds timeout (default 120s)
- Parallel generation hangs or stalls
- No progress after initial members

**Diagnosis**:
```bash
# Check member count
cat configs/collection/{id}.json | grep -c '"id":'

# Monitor CPU/memory
top

# Validate collection
choracompose:validate_collection_config
```

**Solution**:
1. **Reduce concurrency_limit**: Lower from 3 to 2
2. **Use sequential strategy**: `generation.strategy: "sequential"`
3. **Check for circular nesting**: Validate with `validate_collection_config`
4. **Split collection**: Break into smaller sub-collections

---

### 13.5. Issue 5: Permission Denied (Ephemeral Storage)

**Symptoms**:
- Error code: `storage_error`
- Message: "PermissionError: [Errno 13] Permission denied"
- Cannot write to `ephemeral/` directory

**Diagnosis**:
```bash
# Check permissions
ls -la ephemeral/

# Check disk space
df -h

# Check ownership
ls -la | grep ephemeral
```

**Solution**:
1. **Fix permissions**: `chmod 755 ephemeral/` and `chmod 755 ephemeral/content/`
2. **Create directory**: `mkdir -p ephemeral/content ephemeral/drafts`
3. **Check ownership**: `chown -R $USER ephemeral/` (if running as different user)
4. **Verify .gitignore**: Ensure `ephemeral/` is gitignored

---

## 14. References

This section provides links to related documentation, resources, and external references.

### 14.1. Internal SAP Documentation

**Related SAPs**:
- [SAP-000: SAP Framework Core](../sap-framework/protocol-spec.md) - Standard 5-document structure
- [SAP-017: chora-compose Integration Guide](../chora-compose-integration/protocol-spec.md) - Installation and setup
- [SAP-018 Capability Charter](./capability-charter.md) - Problem statement and scope
- [SAP-018 Awareness Guide](./awareness-guide.md) - AI agent quick reference for tool selection
- [SAP-018 Adoption Blueprint](./adoption-blueprint.md) - Implementation roadmap and setup guide
- [SAP-018 Ledger](./ledger.md) - Version history and adoption tracking

**Additional Documentation**:
- [chora-compose README](https://github.com/liminalcommons/chora-compose/blob/main/README.md) - Project overview
- [chora-compose CHANGELOG](https://github.com/liminalcommons/chora-compose/blob/main/CHANGELOG.md) - Version history
- [MCP Tool Reference](https://github.com/liminalcommons/chora-compose/blob/main/docs/reference/mcp/tool-reference.md) - Complete tool specifications

---

### 14.2. Schema Documentation

**JSON Schema Files**:
- [Content Schema v3.1](https://github.com/liminalcommons/chora-compose/blob/main/schemas/content/v3.1/schema.json) - Content configuration schema
- [Artifact Schema v3.1](https://github.com/liminalcommons/chora-compose/blob/main/schemas/artifact/v3.1/schema.json) - Artifact configuration schema
- [Collection Schema v1.0](https://github.com/liminalcommons/chora-compose/blob/main/schemas/collection/v1.0/schema.json) - Collection configuration schema

**Schema Migration Guides**:
- [v3.0 → v3.1 Migration](https://github.com/liminalcommons/chora-compose/blob/main/docs/migration/v3.0-to-v3.1.md)
- [v2.x → v3.0 Migration](https://github.com/liminalcommons/chora-compose/blob/main/docs/migration/v2.x-to-v3.0.md)

---

### 14.3. External Resources

**Model Context Protocol (MCP)**:
- [MCP Specification](https://modelcontextprotocol.io/) - Official MCP protocol documentation
- [FastMCP Framework](https://github.com/jlowin/fastmcp) - MCP server framework used by chora-compose
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp) - Anthropic's MCP integration guide

**Related Technologies**:
- [Jinja2 Documentation](https://jinja.palletsprojects.com/) - Template engine used by chora-compose
- [JSON Schema](https://json-schema.org/) - Schema validation standard
- [Pydantic](https://docs.pydantic.dev/) - Data validation library
- [Poetry](https://python-poetry.org/) - Python dependency management

**SAP Framework Resources**:
- [Skilled Awareness Protocols (SAP) Overview](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness) - SAP framework documentation
- [SAP Development Guide](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/development-guide.md) - Creating new SAPs

---

### 14.4. Community & Support

**GitHub Repository**:
- [chora-compose Issues](https://github.com/liminalcommons/chora-compose/issues) - Bug reports and feature requests
- [chora-compose Discussions](https://github.com/liminalcommons/chora-compose/discussions) - Community Q&A
- [Contributing Guide](https://github.com/liminalcommons/chora-compose/blob/main/CONTRIBUTING.md) - How to contribute

**Contact**:
- Project Maintainers: See [CODEOWNERS](https://github.com/liminalcommons/chora-compose/blob/main/.github/CODEOWNERS)
- Liminal Commons: [Website](https://liminalcommons.org/)

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-04
**Status**: Complete - All sections filled with chora-compose architecture details
