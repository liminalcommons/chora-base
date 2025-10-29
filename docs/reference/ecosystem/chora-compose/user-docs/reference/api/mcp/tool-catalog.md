# MCP Tool Catalog

**Complete reference for all 19 Chora Compose MCP tools available in v1.2.3.**

**Last Updated:** 2025-10-17
**Server Version:** 1.2.3
**MCP Protocol:** 2024-11-05

---

## Table of Contents

- [Tool Inventory](#tool-inventory)
- [Decision Tree](#decision-tree)
- [Tool Categories](#tool-categories)
  - [Core Generation Tools](#core-generation-tools)
  - [Config Lifecycle Tools](#config-lifecycle-tools)
  - [Batch Operations](#batch-operations)
  - [Storage Management](#storage-management)
  - [Discovery & Introspection](#discovery--introspection)
- [Comparison Matrices](#comparison-matrices)
- [Quick Reference Tables](#quick-reference-tables)
- [Error Codes](#error-codes)
- [Performance Characteristics](#performance-characteristics)

---

## Tool Inventory

### All 19 Tools at a Glance

| # | Tool Name | Category | Since | Common Use |
|---|-----------|----------|-------|------------|
| 1 | `hello_world` | Utility | v1.0.0 | Test MCP connection |
| 2 | `list_generators` | Discovery | v1.0.0 | List available generators |
| 3 | `generate_content` | Core Generation | v1.0.0 | Generate single content piece |
| 4 | `assemble_artifact` | Core Generation | v1.0.0 | Combine content into artifacts |
| 5 | `validate_content` | Validation | v1.0.0 | Validate content configs |
| 6 | `regenerate_content` | Core Generation | v1.1.0 | Force regeneration (bypass cache) |
| 7 | `delete_content` | Storage Management | v1.1.0 | Delete specific content file |
| 8 | `preview_generation` | Core Generation | v1.1.0 | Preview without creating files |
| 9 | `batch_generate` | Batch Operations | v1.1.0 | Parallel content generation |
| 10 | `trace_dependencies` | Discovery | v1.1.0 | Show artifact dependencies |
| 11 | `list_artifacts` | Discovery | v1.1.0 | List generated artifacts |
| 12 | `list_content` | Discovery | v1.1.0 | List generated content |
| 13 | `cleanup_ephemeral` | Storage Management | v1.1.0 | Remove expired ephemeral files |
| 14 | `draft_config` | Config Lifecycle | v1.2.0 | Create draft config in ephemeral storage |
| 15 | `test_config` | Config Lifecycle | v1.2.0 | Test draft config without persisting |
| 16 | `modify_config` | Config Lifecycle | v1.2.0 | Update draft config incrementally |
| 17 | `save_config` | Config Lifecycle | v1.2.0 | Persist draft config to filesystem |
| 18 | `list_content_configs` | Discovery | v1.2.2 | List all content configuration files |
| 19 | `list_artifact_configs` | Discovery | v1.2.2 | List all artifact configuration files |

---

## Decision Tree

**"Which tool should I use?"**

```
┌─ Need to CREATE content?
│  ├─ Single piece? → generate_content
│  ├─ Multiple pieces (3+)? → batch_generate
│  ├─ Test first? → preview_generation
│  └─ Combine content into artifact? → assemble_artifact
│
├─ Need to DISCOVER what's available?
│  ├─ What's been generated? → list_content or list_artifacts
│  ├─ What generators available? → list_generators
│  ├─ What does artifact use? → trace_dependencies
│  └─ Test MCP connection? → hello_world
│
├─ Need to MANAGE storage?
│  ├─ Clean up old files? → cleanup_ephemeral
│  ├─ Delete specific file? → delete_content
│  └─ Force regeneration? → regenerate_content
│
└─ Need to VALIDATE?
   ├─ Check config valid? → validate_content
   └─ Check dependencies? → trace_dependencies
```

---

## Tool Categories

### Utility Tools

Tools for testing and diagnostics.

#### hello_world

**Purpose:** Test MCP connection and verify server is responding.

**Signature:**
```typescript
hello_world(
  name?: string
): HelloWorldResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | string | ❌ No | `"World"` | Name to greet |

**Returns:**
```typescript
{
  success: boolean
  message: string
  server_version: string
  timestamp: string
}
```

**Use Cases:**
- Verify MCP connection is working
- Test stdio transport between client and server
- Validate server is responding
- Quick health check

**Example:**
```typescript
// Basic test
hello_world()
// Returns: { message: "Hello, World!", ... }

// Custom greeting
hello_world("Claude")
// Returns: { message: "Hello, Claude!", ... }
```

**See Also:**
- [Tutorial: MCP Integration Deep Dive](../../../tutorials/advanced/01-mcp-integration-deep-dive.md#step-1-verify-mcp-connection)

---

### Core Generation Tools

Tools for generating and assembling content.

#### generate_content

**Purpose:** Generate a single content piece from a content config.

**Signature:**
```typescript
generate_content(
  content_config_id: string,
  context?: Record<string, any>,
  force?: boolean
): GenerationResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | ✅ Yes | - | ID of content config to use |
| `context` | object | ❌ No | `{}` | Context variables for template |
| `force` | boolean | ❌ No | `false` | Bypass cache, force regeneration |

**Returns:**
```typescript
{
  success: boolean
  content: string
  output_path: string
  duration_ms: number
  from_cache: boolean
  metadata: {
    generator: string
    template: string
    generated_at: string
  }
}
```

**Use Cases:**
- Generate single documentation file
- Create README from template
- Generate API documentation
- Produce code examples

**Example:**
```typescript
// Basic generation
generate_content("user-guide")

// With context
generate_content("api-endpoint", {
  method: "GET",
  path: "/users/:id"
})

// Force regeneration
generate_content("daily-report", {}, true)
```

**See Also:**
- [How-To: Use Demonstration Generator](../../../how-to/generation/use-demonstration-generator.md)
- [Tutorial: Basic Content Generation](../../../tutorials/getting-started/02-basic-content-generation.md)

---

#### assemble_artifact

**Purpose:** Combine multiple content pieces into a single artifact file.

**Signature:**
```typescript
assemble_artifact(
  artifact_config_id: string,
  context?: Record<string, any>,
  force?: boolean
): AssemblyResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `artifact_config_id` | string | ✅ Yes | - | ID of artifact config to use |
| `context` | object | ❌ No | `{}` | Context for artifact assembly |
| `force` | boolean | ❌ No | `false` | Force reassembly |

**Returns:**
```typescript
{
  success: boolean
  artifact_path: string
  components: string[]
  duration_ms: number
  size_bytes: number
  metadata: {
    component_count: number
    assembled_at: string
  }
}
```

**Use Cases:**
- Combine API docs into single file
- Assemble multi-section documentation
- Create release notes bundle
- Build onboarding kit

**Example:**
```typescript
// Basic assembly
assemble_artifact("api-docs-bundle")

// With context
assemble_artifact("release-notes", {
  version: "2.0.0",
  date: "2025-10-16"
})
```

**See Also:**
- [How-To: Create Artifact Config](../../../how-to/configs/create-artifact-config.md)
- [Tutorial: Assembling Artifacts](../../../tutorials/getting-started/04-assembling-artifacts.md)

---

#### regenerate_content

**Purpose:** Force regeneration of content, bypassing cache.

**Signature:**
```typescript
regenerate_content(
  content_config_id: string,
  context?: Record<string, any>
): GenerationResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | ✅ Yes | - | ID of content config |
| `context` | object | ❌ No | `{}` | Context variables |

**Returns:** Same as `generate_content`

**Difference from generate_content:**
- **Always bypasses cache** (force=true is implicit)
- Use when data source has changed
- Use when template modified but config unchanged
- Use for testing template changes

**Use Cases:**
- Data source updated (database changed)
- Template modified
- Cache suspected stale
- Debugging generation issues

**Example:**
```typescript
// Force fresh generation
regenerate_content("daily-report")

// With updated context
regenerate_content("api-endpoint", {
  updated_at: "2025-10-16"
})
```

**See Also:**
- [How-To: Preview Before Generating](../../../how-to/generation/preview-before-generating.md#task-6-force-regeneration-cache-bypass)

---

#### preview_generation

**Purpose:** Preview content generation without creating files or side effects.

**Signature:**
```typescript
preview_generation(
  content_config_id: string,
  context?: Record<string, any>,
  generator_override?: string
): PreviewResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content_config_id` | string | ✅ Yes | - | ID of content config |
| `context` | object | ❌ No | `{}` | Context variables |
| `generator_override` | string | ❌ No | - | Override generator for testing |

**Returns:**
```typescript
{
  success: boolean
  preview_content: string
  duration_ms: number
  estimated_cost?: number
  metadata: {
    generator: string
    template: string
    content_length: number
    token_count?: number
  }
}
```

**Key Differences from generate_content:**
- ❌ No file creation
- ❌ No cache interaction
- ❌ No metadata updates
- ✅ Returns content as string
- ✅ Cost estimation (AI generators)

**Use Cases:**
- Test new templates
- Validate context data
- Estimate AI generation costs
- Debug template logic
- Iterate on designs without cleanup

**Example:**
```typescript
// Basic preview
preview_generation("user-guide")

// Test with edge case context
preview_generation("api-endpoint", {
  methods: [],
  auth_required: null
})

// Override generator for testing
preview_generation("technical-spec", {}, "demonstration")
```

**See Also:**
- [How-To: Preview Before Generating](../../../how-to/generation/preview-before-generating.md)
- [Tutorial: MCP Integration Deep Dive](../../../tutorials/advanced/01-mcp-integration-deep-dive.md#part-2-config-lifecycle-workflow)

---

### Batch Operations

Tools for efficient parallel operations.

#### batch_generate

**Purpose:** Generate multiple content pieces in parallel for 3-5× performance improvement.

**Signature:**
```typescript
batch_generate(
  requests: BatchRequest[],
  max_parallelism?: number
): BatchResult
```

**Types:**
```typescript
interface BatchRequest {
  content_config_id: string
  context?: Record<string, any>
  force?: boolean
}

interface BatchResult {
  success: boolean
  results: GenerationResult[]
  duration_ms: number
  total_items: number
  successful: number
  failed: number
  speedup: number  // e.g., 3.2× faster than sequential
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `requests` | array | ✅ Yes | - | Array of generation requests |
| `max_parallelism` | number | ❌ No | `5` | Max concurrent generations |

**Performance:**

| Items | Sequential | Batch | Speedup |
|-------|------------|-------|---------|
| 5 | 10s | 3-4s | 2.5-3.3× |
| 10 | 20s | 4-6s | 3.3-5× |
| 20 | 40s | 8-12s | 3.3-5× |

**Use Cases:**
- Generate multiple API docs
- Create batch reports
- Bulk content generation
- Parallel template testing

**Example:**
```typescript
// Generate 5 API endpoint docs
batch_generate([
  { content_config_id: "api-endpoint", context: { endpoint: "/users" }},
  { content_config_id: "api-endpoint", context: { endpoint: "/posts" }},
  { content_config_id: "api-endpoint", context: { endpoint: "/comments" }},
  { content_config_id: "api-endpoint", context: { endpoint: "/likes" }},
  { content_config_id: "api-endpoint", context: { endpoint: "/shares" }}
])

// Custom parallelism
batch_generate(requests, 10)  // Max 10 concurrent
```

**See Also:**
- [How-To: Batch Generate Content](../../../how-to/generation/batch-generate-content.md)
- [Tutorial: MCP Integration Deep Dive](../../../tutorials/advanced/01-mcp-integration-deep-dive.md#part-3-batch-operations)

---

### Storage Management

Tools for managing ephemeral and permanent storage.

#### cleanup_ephemeral

**Purpose:** Remove expired ephemeral files based on retention policy.

**Signature:**
```typescript
cleanup_ephemeral(
  dry_run?: boolean
): CleanupResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dry_run` | boolean | ❌ No | `false` | Preview without deleting |

**Returns:**
```typescript
{
  success: boolean
  dry_run: boolean
  files_removed: string[]
  files_kept: string[]
  total_freed_kb: number
  duration_ms: number
}
```

**Retention Policy:**
- **Default:** 30 days
- **Configurable:** `ephemeral/.metadata.json`
- **Automatic:** On server startup (configurable)
- **Manual:** Call this tool

**Use Cases:**
- Free up disk space
- Remove old drafts
- Maintain storage hygiene
- Scheduled CI/CD cleanup

**Example:**
```typescript
// Preview cleanup (safe)
cleanup_ephemeral(true)

// Execute cleanup
cleanup_ephemeral()
```

**See Also:**
- [How-To: Manage Ephemeral Storage](../../../how-to/storage/manage-ephemeral-storage.md)
- [Reference: EphemeralConfigManager](../storage/ephemeral-config-manager.md)

---

#### delete_content

**Purpose:** Delete a specific generated content file and its metadata.

**Signature:**
```typescript
delete_content(
  file_path: string,
  check_dependencies?: boolean
): DeleteResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_path` | string | ✅ Yes | - | Path to file (relative to workspace) |
| `check_dependencies` | boolean | ❌ No | `true` | Check if used by artifacts |

**Returns:**
```typescript
{
  success: boolean
  deleted_path: string
  dependencies_found: boolean
  blocked_by: string[]  // Artifact IDs using this content
  metadata_removed: boolean
  cache_invalidated: boolean
}
```

**Safety Features:**
- **Confirmation prompt** for permanent files
- **Dependency checking** (prevents broken artifacts)
- **Metadata cleanup** (cache invalidation)

**Use Cases:**
- Remove unwanted generated files
- Clean up test output
- Delete obsolete content
- Prepare for regeneration

**Example:**
```typescript
// Delete with dependency check
delete_content("output/old-api-docs.md")

// Force delete (skip dependency check)
delete_content("output/temp-file.md", false)
```

**See Also:**
- [How-To: Manage Ephemeral Storage](../../../how-to/storage/manage-ephemeral-storage.md#task-3-delete-specific-content)

---

### Discovery & Introspection

Tools for exploring configs, artifacts, and capabilities.

#### list_content

**Purpose:** List all available content configurations with generation status.

**Signature:**
```typescript
list_content(
  filter?: Record<string, any>,
  sort?: string,
  limit?: number
): ListContentResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter` | object | ❌ No | `{}` | Filters: `generator_type`, `generated`, `stage` |
| `sort` | string | ❌ No | `"id"` | Sort order: `id`, `title`, `generator`, `modified` |
| `limit` | number | ❌ No | `100` | Max results (1-500) |

**Returns:**
```typescript
{
  success: boolean
  total: number
  returned: number
  content: ContentSummary[]
  duration_ms: number
}

interface ContentSummary {
  id: string
  title: string
  file_path: string
  generator: string
  generated: boolean
  last_modified: string
  stage?: string
}
```

**Use Cases:**
- Browse content catalog
- Check generation status
- Discover available content
- Filter by generator type

**Example:**
```typescript
// List all content
list_content()

// Filter by generator
list_content({ generator_type: "jinja2" })

// Sort by modification date
list_content({}, "modified", 50)

// Find ungenerated content
list_content({ generated: false })
```

**See Also:**
- [How-To: Discover and Browse Configs](../../../how-to/configs/discover-and-browse-configs.md)

---

#### list_artifacts

**Purpose:** List all generated artifact files with metadata.

**Signature:**
```typescript
list_artifacts(
  filter_date?: string
): ArtifactList
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter_date` | string | ❌ No | - | ISO date or relative ("24h", "7d") |

**Returns:**
```typescript
{
  success: boolean
  artifacts: ArtifactInfo[]
  total_count: number
  total_size_kb: number
}

interface ArtifactInfo {
  path: string
  config_id: string
  size_kb: number
  generated_at: string
  component_count: number
  components: string[]
}
```

**Use Cases:**
- Audit generated artifacts
- Find recent artifacts
- Monitor storage usage
- Clean up old artifacts

**Example:**
```typescript
// List all
list_artifacts()

// Recent artifacts (24 hours)
list_artifacts("24h")

// Specific date
list_artifacts("2025-10-16")
```

**See Also:**
- [How-To: Discover and Browse Configs](../../../how-to/configs/discover-and-browse-configs.md#task-4-list-generated-artifacts)

---

#### trace_dependencies

**Purpose:** Show dependency graph for an artifact config.

**Signature:**
```typescript
trace_dependencies(
  artifact_config_id: string
): DependencyGraph
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `artifact_config_id` | string | ✅ Yes | - | ID of artifact config |

**Returns:**
```typescript
{
  success: boolean
  artifact_id: string
  dependencies: DependencyNode[]
  total_dependencies: number
  missing_dependencies: string[]
  ready_to_assemble: boolean
}

interface DependencyNode {
  content_config_id: string
  config_path: string
  template: string
  generator: string
  generated: boolean
  output_path?: string
  size_kb?: number
}
```

**Use Cases:**
- Pre-flight checks before assembly
- Identify missing content
- Understand artifact structure
- Debug assembly failures

**Example:**
```typescript
// Trace artifact dependencies
trace_dependencies("api-docs-bundle")

// Response shows:
// - All required content configs
// - Whether each is generated
// - Missing dependencies
// - Ready to assemble: true/false
```

**See Also:**
- [How-To: Discover and Browse Configs](../../../how-to/configs/discover-and-browse-configs.md#task-5-trace-artifact-dependencies)

---

#### list_generators

**Purpose:** List all available content generators.

**Signature:**
```typescript
list_generators(): GeneratorList
```

**Parameters:** None

**Returns:**
```typescript
{
  success: boolean
  generators: GeneratorInfo[]
  total_count: number
}

interface GeneratorInfo {
  id: string
  type: string
  description: string
  capabilities: string[]
  requires_context: boolean
  supports_streaming: boolean
}
```

**Built-in Generators:**
- `demonstration` - Uses example_output fields
- `jinja2` - Template rendering
- `ai-powered` - LLM-based generation (if configured)

**Use Cases:**
- Discover available generators
- Choose appropriate generator
- Agent initialization
- Capability discovery

**Example:**
```typescript
list_generators()

// Response:
// [
//   { id: "demonstration", type: "static", ... },
//   { id: "jinja2", type: "template", ... }
// ]
```

**See Also:**
- [Reference: Generator Types](../generators/types.md)

---

#### validate_content

**Purpose:** Validate a content config against JSON Schema.

**Signature:**
```typescript
validate_content(
  config_path: string
): ValidationResult
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config_path` | string | ✅ Yes | - | Path to config file |

**Returns:**
```typescript
{
  success: boolean
  valid: boolean
  errors: ValidationError[]
  warnings: string[]
  schema_version: string
}

interface ValidationError {
  field: string
  message: string
  location: string
}
```

**Validation Checks:**
- ✅ JSON Schema v3.1 compliance
- ✅ Required fields present
- ✅ Type correctness
- ✅ Pattern validity
- ✅ Template existence
- ⚠️  Best practice warnings

**Use Cases:**
- Validate before generation
- Check config syntax
- Troubleshoot errors
- CI/CD validation

**Example:**
```typescript
// Validate content config
validate_content("configs/content/api-endpoint.json")

// Response:
// {
//   valid: true,
//   errors: [],
//   warnings: ["Template file not found: templates/missing.jinja"]
// }
```

**See Also:**
- [Reference: Content Schema v3.1](../../../../schemas/content/v3.1/schema.json)

---

## Comparison Matrices

### Content Generation Tools

**When to use which content generation tool?**

| Tool | Creates Files | Uses Cache | Side Effects | Use Case |
|------|---------------|------------|--------------|----------|
| `generate_content` | ✅ Yes | ✅ Yes | ✅ Yes | Production generation |
| `regenerate_content` | ✅ Yes | ❌ No | ✅ Yes | Force fresh generation |
| `preview_generation` | ❌ No | ❌ No | ❌ No | Testing/validation |
| `batch_generate` | ✅ Yes | ✅ Yes | ✅ Yes | Bulk operations (3+ items) |

**Decision:**
- **Testing template?** → `preview_generation`
- **Data changed?** → `regenerate_content`
- **Multiple files (3+)?** → `batch_generate`
- **Normal generation?** → `generate_content`

---

### Config Management Tools

**Manual vs Conversational workflows:**

| Task | Manual Approach | Conversational Approach | Time Saved |
|------|----------------|-------------------------|------------|
| Create config | Edit JSON in IDE | `draft_config` + chat | 70% |
| Test config | Save + run + check | `test_config` in chat | 80% |
| Iterate | Edit + save + run + check | `modify_config` + `test_config` | 75% |
| Finalize | Manual save | `save_config` | 50% |

**Decision:**
- **Comfortable with JSON?** → Manual editing
- **Quick iteration?** → Conversational (draft→test→modify→save)
- **Complex config?** → Conversational (AI assistance)
- **Production config?** → Either (both produce valid configs)

---

### Discovery Tools

**Finding information:**

| Need | Tool | Output | Use Case |
|------|------|--------|----------|
| All content types | `list_content_configs` | Content config summaries | Inventory |
| All artifact types | `list_artifact_configs` | Artifact config summaries | Inventory |
| Generated files | `list_artifacts` | File paths + metadata | Audit |
| Artifact structure | `trace_dependencies` | Dependency graph | Pre-flight check |
| Available generators | `list_generators` | Generator capabilities | Discovery |

---

## Quick Reference Tables

### Tool Performance

**Typical execution times:**

| Tool | Typical Time | Max Time | Notes |
|------|--------------|----------|-------|
| `generate_content` | <2s | 10s | AI generators slower |
| `assemble_artifact` | <5s | 30s | Depends on component count |
| `preview_generation` | <2s | 10s | Slightly faster (no I/O) |
| `batch_generate` (5 items) | 3-4s | 15s | 2.5-3.3× speedup |
| `draft_config` | <100ms | 500ms | Fast (validation only) |
| `test_config` | <2s | 10s | Same as preview |
| `modify_config` | <100ms | 500ms | Fast (merge + validate) |
| `save_config` | <200ms | 1s | File I/O |
| `cleanup_ephemeral` | <1s | 10s | Depends on file count |
| `delete_content` | <200ms | 1s | File deletion |
| `list_*` tools | <100ms | 500ms | Disk reads |
| `trace_dependencies` | <200ms | 2s | Graph traversal |
| `validate_content` | <100ms | 500ms | Schema validation |

---

### Tool Categories by Version

| Category | v1.0.0 Tools | v1.1.0 Added | Total |
|----------|-------------|--------------|-------|
| Core Generation | 2 | 2 | 4 |
| Config Lifecycle | 0 | 4 | 4 |
| Batch Operations | 0 | 1 | 1 |
| Storage Management | 0 | 2 | 2 |
| Discovery | 2 | 4 | 6 |
| **Total** | **4** | **13** | **17** |

---

## Error Codes

### Common Error Codes Across All Tools

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `config_not_found` | Config file doesn't exist | Check config ID, verify path |
| `validation_failed` | Config invalid (schema violation) | Run `validate_content`, fix errors |
| `template_not_found` | Template file missing | Check template path in config |
| `generator_not_found` | Generator doesn't exist | Use `list_generators`, fix config |
| `context_missing` | Required context variables missing | Provide context parameter |
| `file_already_exists` | Output file exists, force=false | Use force=true or delete file |
| `dependency_missing` | Required content not generated | Generate dependencies first |
| `storage_limit_exceeded` | Ephemeral storage full | Run `cleanup_ephemeral` |
| `draft_not_found` | Draft ID doesn't exist | Check draft_id, may have expired |
| `draft_expired` | Draft older than retention period | Create new draft |
| `permission_denied` | File system permission error | Check file permissions |
| `invalid_json` | Malformed JSON in config | Validate JSON syntax |

### Tool-Specific Errors

**batch_generate:**
- `partial_failure` - Some items succeeded, some failed (check results array)

**save_config:**
- `config_exists` - Config ID exists, overwrite=false

**delete_content:**
- `has_dependencies` - File used by artifacts (blocked)

---

## Performance Characteristics

### Caching Behavior

| Tool | Uses Cache? | Writes Cache? | Cache Bypass |
|------|-------------|---------------|--------------|
| `generate_content` | ✅ Yes | ✅ Yes | force=true |
| `regenerate_content` | ❌ No | ✅ Yes | Always bypasses |
| `preview_generation` | ❌ No | ❌ No | N/A (never cached) |
| `batch_generate` | ✅ Yes | ✅ Yes | force=true per item |
| `assemble_artifact` | ❌ No | ❌ No | Artifacts not cached |

**Cache Invalidation:**
- `delete_content` invalidates cache for deleted file
- Modifying template invalidates related cache entries
- Cache keys: config_id + context hash + template hash

---

### Parallelism

| Tool | Parallel Execution | Max Concurrency | Notes |
|------|-------------------|-----------------|-------|
| `batch_generate` | ✅ Yes | 5 (configurable) | True parallel execution |
| `assemble_artifact` | ⚠️  Sequential | 1 | Components assembled in order |
| All other tools | ❌ No | 1 | Single-threaded |

---

### Resource Usage

| Tool | CPU | Memory | Disk I/O | Network |
|------|-----|--------|----------|---------|
| `generate_content` | Low | Low | Medium | Low (AI: High) |
| `preview_generation` | Low | Low | Low | Low (AI: High) |
| `batch_generate` | Medium | Medium | High | Medium (AI: High) |
| `assemble_artifact` | Low | Medium | High | None |
| `draft_config` | Low | Low | Low | None |
| `cleanup_ephemeral` | Low | Low | High | None |
| Discovery tools | Low | Low | Medium | None |

---

## Version History

### v1.1.0 (2025-10-15)

**Added (13 new tools):**
- Config Lifecycle: `draft_config`, `test_config`, `modify_config`, `save_config`
- Generation: `preview_generation`, `regenerate_content`, `batch_generate`
- Storage: `cleanup_ephemeral`, `delete_content`
- Discovery: `list_content_configs`, `list_artifact_configs`, `list_artifacts`, `trace_dependencies`

**Total:** 17 tools

### v1.0.0 (2025-09-15)

**Initial Release (4 tools):**
- `generate_content`
- `assemble_artifact`
- `list_generators`
- `validate_content`

**Total:** 4 tools

---

## Related Documentation

### Tutorials
- [Getting Started: Basic Content Generation](../../../tutorials/getting-started/02-basic-content-generation.md)
- [Intermediate: Conversational Config Creation](../../../tutorials/intermediate/02-conversational-config-creation.md)
- [Advanced: MCP Integration Deep Dive](../../../tutorials/advanced/01-mcp-integration-deep-dive.md)

### How-To Guides
- [Create Content Config](../../../how-to/configs/create-content-config.md)
- [Create Config Conversationally](../../../how-to/configs/create-config-conversationally.md)
- [Preview Before Generating](../../../how-to/generation/preview-before-generating.md)
- [Batch Generate Content](../../../how-to/generation/batch-generate-content.md)
- [Manage Ephemeral Storage](../../../how-to/storage/manage-ephemeral-storage.md)
- [Discover and Browse Configs](../../../how-to/configs/discover-and-browse-configs.md)

### Reference
- [Content Schema v3.1](../../../../schemas/content/v3.1/schema.json)
- [Artifact Schema v3.1](../../../../schemas/artifact/v3.1/schema.json)
- [EphemeralConfigManager API](../storage/ephemeral-config-manager.md)
- [Generator Types](../generators/types.md)

### Explanation
- [Conversational Workflow Authoring](../../../explanation/architecture/conversational-workflow-authoring.md)

---

**Last Updated:** 2025-10-16
**Chora Compose Version:** 1.1.0
**MCP Protocol Version:** 2024-11-05
