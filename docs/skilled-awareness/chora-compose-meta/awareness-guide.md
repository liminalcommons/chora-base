# Awareness Guide: chora-compose Meta

**SAP ID**: SAP-018
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants
**Last Updated**: 2025-11-04

---

## Quick Start for AI Agents

### One-Sentence Summary

chora-compose Meta provides 24 MCP tools for content generation using a 3-tier architecture (Content → Artifact → Collection) with SHA-256 caching, context propagation, and parallel execution strategies.

### When to Use This SAP

Use SAP-018 when:
- ✅ User asks to generate SAP documentation or multi-file artifacts (Collections are designed for this)
- ✅ User wants to create content from templates with dynamic context (5 generators available: jinja2, template_fill, demonstration, bdd_scenario, code_generation)
- ✅ User needs to batch generate multiple related content pieces efficiently (batch_generate with parallel execution)
- ✅ User wants to test configuration changes before saving (draft → test → modify → save lifecycle)
- ✅ User needs to validate collection freshness or trace content dependencies (stigmergic context tracking)

Don't use SAP-018 for:
- ❌ Simple file read/write operations without templates (use standard file I/O instead)
- ❌ One-off text generation without reusable templates or configs (creates unnecessary overhead)
- ❌ Real-time editing of existing files (chora-compose generates from configs, not in-place edits)
- ❌ Projects without chora-compose installed or MCP server configured (requires adoption-blueprint.md setup first)

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1**: 3-Tier Architecture (Content → Artifact → Collection)
- **Description**: chora-compose uses a compositional model where Content (atomic units) → Artifact (assembled multi-content files) → Collection (bulk coordination of multiple artifacts). Each tier has its own config type and MCP tools.
- **When to use**: Content tier for single template generations, Artifact tier for multi-section documents (README with 5 sections), Collection tier for bulk operations (18 SAP docs = 90 artifacts).
- **Example**: To generate a complete SAP, you'd use `choracompose:generate_collection` which orchestrates multiple `assemble_artifact` calls, each of which generates individual contents. Don't call generate_content 90 times manually.

**Concept 2**: Context Propagation (MERGE/OVERRIDE/ISOLATE modes)
- **Description**: Collections propagate shared context to artifacts/contents using three modes: MERGE (combine collection + member context), OVERRIDE (collection replaces member context), ISOLATE (no propagation, member-only context).
- **When to use**: MERGE for shared variables (project_name across all SAPs), OVERRIDE for forcing consistent values (version: "1.0.0"), ISOLATE for independent members with unrelated contexts.
- **Example**: Collection context `{"project": "chora-base", "version": "2.0"}` with MERGE mode means each artifact gets these variables plus its own specific context merged together.

**Concept 3**: SHA-256 Caching (Deterministic Cache Keys)
- **Description**: Content generation uses SHA-256 hashing of (content_config_id + context) to create deterministic cache keys. If context hasn't changed, cached output is reused (94%+ hit rate in production). Set `force=true` to bypass cache.
- **When to use**: Let caching work automatically for unchanged contexts. Use `force=true` only when troubleshooting or template has changed but context hasn't.
- **Example**: If you generate with context `{"user": "Alice"}` twice, second call hits cache. Changing to `{"user": "Bob"}` generates new content (different cache key).

**Concept 4**: 6 Context Source Types
- **Description**: Context can come from inline_data (JSON in config), external_file (JSON/YAML file), git_reference (file in git repo), content_config (reuse another content's output), artifact_config (reference artifact output), ephemeral_output (generated content in storage).
- **When to use**: inline_data for simple static values, external_file for shared config files, git_reference for version-controlled data, content_config/artifact_config for dependencies, ephemeral_output for chaining generations.
- **Example**: Artifact config can specify `"sources": [{"type": "content_config", "reference": "header-content"}]` to inject previously generated content as context for another generation.

### Decision Tree

```
User request about content generation
   │
   ├─ Single template with context?
   │   └─> Use choracompose:generate_content
   │       (Example: "Generate README intro with project name")
   │
   ├─ Multi-section document (N contents → 1 file)?
   │   └─> Use choracompose:assemble_artifact
   │       (Example: "Create README with header, features, installation, usage")
   │
   ├─ Bulk operation (M artifacts)?
   │   └─> Use choracompose:generate_collection
   │       (Example: "Generate all 18 SAP documentation sets")
   │
   ├─ Want to test config before saving?
   │   └─> Use draft_config → test_config → modify_config → save_config
   │       (Iterative refinement without committing changes)
   │
   ├─ Need to validate dependencies or freshness?
   │   └─> Use choracompose:trace_dependencies or check_freshness
   │       (Check if artifact members need regeneration)
   │
   └─ Unsure which tool to use?
       └─> Use choracompose:list_generators (see available generators)
           or choracompose:list_content_configs (see existing configs)
```

---

## 2. Common Agent Workflows

### Workflow 1: Generate Single Content Piece

**User Request**: "Generate a README introduction section with project name 'chora-base'"

**Agent Actions**:
1. Call `choracompose:list_content_configs` to verify config exists (e.g., "readme-intro")
2. Call `choracompose:generate_content` with:
   ```json
   {
     "content_config_id": "readme-intro",
     "context": {"project_name": "chora-base"},
     "force": false
   }
   ```
3. Check response `success: true` and `status: "generated"` (or "skipped" if cached)

**Validation**:
```bash
# Check ephemeral storage for generated content
ls ~/.chora-compose/ephemeral/content/readme-intro/
# Verify content exists
cat ~/.chora-compose/ephemeral/content/readme-intro/<hash>.txt
```

**Expected Output**:
```json
{
  "success": true,
  "content_id": "readme-intro",
  "content": "# chora-base\n\nWelcome to chora-base...",
  "generator": "jinja2",
  "status": "generated",
  "duration_ms": 45,
  "metadata": {
    "context_variables": ["project_name"],
    "ephemeral_stored": true,
    "storage_path": "~/.chora-compose/ephemeral/content/readme-intro/abc123.txt"
  }
}
```

**Common Variations**:
- **Variation 1**: If config doesn't exist, use `draft_config` → `test_config` → `save_config` to create it first
- **Variation 2**: If template changed but context same, use `force: true` to bypass cache

### Workflow 2: Assemble Multi-Content Artifact

**User Request**: "Create complete README.md with header, features, installation, and usage sections"

**Agent Actions**:
1. Call `choracompose:list_artifact_configs` to verify config exists (e.g., "complete-readme")
2. Call `choracompose:trace_dependencies` to check if content dependencies exist:
   ```json
   {"artifact_config_id": "complete-readme"}
   ```
3. Generate missing content pieces if needed using `batch_generate`:
   ```json
   {
     "content_ids": ["readme-header", "readme-features", "readme-install", "readme-usage"],
     "shared_context": {"project": "chora-base"},
     "max_parallel": 4
   }
   ```
4. Call `choracompose:assemble_artifact`:
   ```json
   {
     "artifact_config_id": "complete-readme",
     "output_path": "outputs/README.md",
     "force": false
   }
   ```

**Validation**:
```bash
# Verify artifact file exists
ls -lh outputs/README.md
# Check artifact was assembled (not skipped)
# Response should show status: "assembled"
```

**Expected Output**:
```json
{
  "success": true,
  "artifact_id": "complete-readme",
  "output_path": "outputs/README.md",
  "content_count": 4,
  "size_bytes": 5432,
  "status": "assembled",
  "duration_ms": 123,
  "metadata": {
    "missing_content": [],
    "generated_content": ["readme-header", "readme-features", "readme-install", "readme-usage"],
    "composition_strategy": "concatenation"
  }
}
```

**Common Variations**:
- **Variation 1**: If dependencies missing and can't auto-generate, notify user which content configs need creation
- **Variation 2**: If output_path already exists, artifact will be skipped unless `force: true`

### Workflow 3: Generate Complete Collection

**User Request**: "Generate all SAP documentation (18 SAPs with 5 artifacts each)"

**Agent Actions**:
1. Call `choracompose:validate_collection_config` to verify collection config is valid:
   ```json
   {"collection_config_id": "all-sap-docs"}
   ```
2. Call `choracompose:list_collection_members` to preview what will be generated:
   ```json
   {"collection_config_id": "all-sap-docs"}
   ```
3. Call `choracompose:generate_collection`:
   ```json
   {
     "collection_config_id": "all-sap-docs",
     "force": false,
     "force_members": false
   }
   ```
4. Monitor progress (Collections emit events if OpenTelemetry configured)

**Validation**:
```bash
# Check collection cache status
# Use choracompose:check_collection_cache
# Verify all artifacts generated
ls -R outputs/sap-docs/
```

**Expected Output**:
```json
{
  "success": true,
  "collection_id": "all-sap-docs",
  "members_generated": 18,
  "total_artifacts": 90,
  "total_content": 450,
  "duration_ms": 8734,
  "execution_strategy": "parallel",
  "metadata": {
    "cache_hit_rate": 0.94,
    "parallel_workers": 8,
    "context_propagation_mode": "MERGE"
  }
}
```

**Common Variations**:
- **Variation 1**: Use `force: true` to regenerate collection-level config, `force_members: true` to force all member regeneration
- **Variation 2**: Use sequential execution for ordered generation: set `execution_strategy: "sequential"` in collection config

### Workflow 4: Conversational Config Creation (Draft → Test → Modify → Save)

**User Request**: "I want to create a new content config for generating API documentation"

**Agent Actions**:
1. Call `choracompose:draft_config` to create draft:
   ```json
   {
     "config_type": "content",
     "config_id": "api-docs",
     "template": {
       "type": "content_config",
       "id": "api-docs",
       "generator": {"type": "jinja2"},
       "elements": {
         "template": "# API Documentation\n\n{{ description }}\n\n## Endpoints\n{% for endpoint in endpoints %}..."
       },
       "inputs": {
         "sources": [{"type": "inline_data", "data": {"description": "API for chora-base"}}]
       }
     }
   }
   ```
2. Call `choracompose:test_config` to validate without saving:
   ```json
   {
     "config_id": "api-docs",
     "test_context": {"endpoints": [{"name": "/health", "method": "GET"}]}
   }
   ```
3. If user requests changes, call `choracompose:modify_config`:
   ```json
   {
     "config_id": "api-docs",
     "modifications": {
       "inputs.sources[0].data.description": "Updated API description"
     }
   }
   ```
4. When satisfied, call `choracompose:save_config`:
   ```json
   {"config_id": "api-docs"}
   ```

**Validation**:
```bash
# Verify config saved to disk
ls configs/content/api-docs.json
# Test generation with saved config
# Use generate_content with api-docs config
```

**Common Variations**:
- **Variation 1**: User wants to start from existing config → use `list_content_configs` to find similar, then draft_config with that as template
- **Variation 2**: Test fails → modify_config → test_config again (iterate until valid)

### Workflow 5: Validate Collection Freshness (Stigmergic Context)

**User Request**: "Check if my SAP documentation is up to date with latest content changes"

**Agent Actions**:
1. Call `choracompose:check_freshness` for each artifact in collection:
   ```json
   {
     "content_config_id": "sap-capability-charter",
     "context": {"sap_id": "SAP-018"}
   }
   ```
2. Check response for `is_fresh: false` indicating stale content
3. Call `choracompose:trace_dependencies` to find affected artifacts:
   ```json
   {"artifact_config_id": "sap-018-complete"}
   ```
4. Regenerate stale artifacts using `assemble_artifact` with `force: true`

**Validation**:
```bash
# Check collection cache manifest
cat ~/.chora-compose/cache/collections/<collection-id>/manifest.json
# Verify stigmergic_context timestamps updated
```

**Expected Output**:
```json
{
  "success": true,
  "is_fresh": false,
  "content_id": "sap-capability-charter",
  "last_generated": "2025-11-01T10:30:00Z",
  "context_changed": true,
  "stale_reason": "Context hash mismatch (expected: abc123, actual: def456)"
}
```

**Common Variations**:
- **Variation 1**: All content fresh → no regeneration needed, report to user
- **Variation 2**: Cascading staleness → regenerate dependencies in correct order (use trace_dependencies for topological sort)

---

## 3. Quick Reference for Agents

### Key Commands (Top 10 MCP Tools)

```bash
# 1. Generate single content from config + context
choracompose:generate_content {"content_config_id": "id", "context": {}, "force": false}

# 2. Assemble multi-content artifact into single file
choracompose:assemble_artifact {"artifact_config_id": "id", "output_path": "path", "force": false}

# 3. Generate entire collection (bulk operation)
choracompose:generate_collection {"collection_config_id": "id", "force": false, "force_members": false}

# 4. Batch generate multiple contents in parallel
choracompose:batch_generate {"content_ids": ["id1", "id2"], "shared_context": {}, "max_parallel": 4}

# 5. List available generators and their capabilities
choracompose:list_generators {}

# 6. List all content configs with metadata
choracompose:list_content_configs {"include_metadata": true}

# 7. Trace dependencies for artifact (check what content needed)
choracompose:trace_dependencies {"artifact_config_id": "id"}

# 8. Check if content is fresh (stigmergic context validation)
choracompose:check_freshness {"content_config_id": "id", "context": {}}

# 9. Preview generation without saving (dry-run)
choracompose:preview_generation {"content_config_id": "id", "context": {}}

# 10. Validate collection config before generation
choracompose:validate_collection_config {"collection_config_id": "id"}
```

### Important File Paths

| File Path | Purpose | Required |
|-----------|---------|----------|
| `configs/content/*.json` | Content config definitions (template + generator + context sources) | Yes (for generate_content) |
| `configs/artifacts/*.json` | Artifact config definitions (multi-content assembly rules) | Yes (for assemble_artifact) |
| `configs/collections/*.json` | Collection config definitions (bulk coordination with context propagation) | Yes (for generate_collection) |
| `~/.chora-compose/ephemeral/content/` | Ephemeral storage for generated content (SHA-256 cached) | Auto-created |
| `~/.chora-compose/cache/collections/` | Collection cache manifests (track generation history) | Auto-created |
| `~/.chora-compose/generators/` | Custom generator plugins (auto-discovered) | No (optional) |
| `outputs/` | Default artifact output directory (configurable per artifact) | No (configurable) |
| `templates/` | Jinja2 template files (referenced by content configs) | Yes (if using jinja2 generator) |

### Configuration Snippets

**Configuration 1: Content Config (Jinja2 Generator)**
```json
{
  "type": "content_config",
  "version": "3.1",
  "id": "readme-intro",
  "generator": {
    "type": "jinja2",
    "options": {
      "template_path": "templates/readme-intro.j2"
    }
  },
  "elements": {
    "template": "# {{ project_name }}\n\n{{ description }}\n\n## Features\n{% for feature in features %}- {{ feature }}\n{% endfor %}"
  },
  "inputs": {
    "sources": [
      {
        "type": "inline_data",
        "data": {
          "project_name": "chora-base",
          "description": "SAP framework for chora-compose"
        }
      },
      {
        "type": "external_file",
        "path": "project-config.json",
        "selector": "$.features",
        "required": true
      }
    ]
  },
  "generation": {
    "patterns": {
      "cache_key_fields": ["project_name", "features"],
      "output_format": "markdown"
    }
  }
}
```

**Configuration 2: Artifact Config (Multi-Content Assembly)**
```json
{
  "type": "artifact_config",
  "version": "3.1",
  "id": "complete-readme",
  "output": {
    "path": "outputs/README.md",
    "format": "markdown"
  },
  "composition": {
    "strategy": "concatenation",
    "members": [
      {
        "content_config_id": "readme-header",
        "order": 1
      },
      {
        "content_config_id": "readme-features",
        "order": 2
      },
      {
        "content_config_id": "readme-installation",
        "order": 3
      },
      {
        "content_config_id": "readme-usage",
        "order": 4
      }
    ],
    "separator": "\n\n---\n\n"
  },
  "inputs": {
    "sources": [
      {
        "type": "inline_data",
        "data": {
          "project": "chora-base",
          "version": "2.0.0"
        }
      }
    ]
  },
  "validation": {
    "required_sections": ["header", "features", "installation"],
    "min_size_bytes": 500
  }
}
```

**Configuration 3: Collection Config (Bulk Coordination)**
```json
{
  "type": "collection_config",
  "version": "1.0",
  "id": "all-sap-docs",
  "members": [
    {"artifact_config_id": "sap-000-docs"},
    {"artifact_config_id": "sap-017-docs"},
    {"artifact_config_id": "sap-018-docs"}
  ],
  "shared_context": {
    "project": "chora-base",
    "version": "2.0.0",
    "author": "Victor"
  },
  "context_propagation": {
    "mode": "MERGE",
    "merge_strategy": "deep"
  },
  "execution": {
    "strategy": "parallel",
    "max_workers": 8,
    "timeout_seconds": 300
  },
  "cache": {
    "enabled": true,
    "manifest_path": "~/.chora-compose/cache/collections/all-sap-docs/manifest.json"
  }
}
```

---

## 4. Error Handling for Agents

### Error 1: config_not_found

**Recognition**:
- Response contains `"error": {"code": "config_not_found"}`
- Error message: "Configuration file not found: configs/content/{id}.json" (or artifacts/collections)
- Occurs when calling generate_content, assemble_artifact, or generate_collection with non-existent config ID

**Agent Response**:
```
"I couldn't find the configuration '{config_id}' in the configs/{type}/ directory. This usually means the config hasn't been created yet or the ID is misspelled.

To resolve this:
1. Check for typos in the config ID
2. List available configs using choracompose:list_content_configs (or list_artifact_configs)
3. Create the missing config using choracompose:draft_config → test_config → save_config

Would you like me to:
a) List available configs to find the correct ID?
b) Create a new config with this ID?
"
```

**Remediation**:
1. Call `choracompose:list_content_configs` to show available configs
2. If config truly missing, guide user through draft_config → test_config → save_config lifecycle
3. If typo, retry with corrected ID

**Escalation Criteria**:
- Escalate to user if: Multiple config IDs are close matches (user needs to choose), or user needs to provide template content for new config

### Error 2: generation_failed

**Recognition**:
- Response contains `"error": {"code": "generation_failed"}`
- Error details often include generator-specific error (e.g., Jinja2 syntax error, missing template file)
- Occurs during generate_content, preview_generation, or batch_generate

**Agent Response**:
```
"Content generation failed for '{content_config_id}'. The error was: {error_details}

Common causes:
1. Jinja2 template syntax error (missing {% endfor %}, undefined variable)
2. Missing template file referenced in config
3. Context data doesn't match template expectations
4. Generator-specific issue (e.g., Anthropic API key missing for code_generation)

To resolve this:
1. Use choracompose:preview_generation to test with simplified context
2. Check template syntax in config.elements.template
3. Verify all template variables are provided in context
4. Check generator options (template_path exists, API keys configured)

Would you like me to:
a) Preview generation with minimal context to isolate the issue?
b) Show the content config for manual inspection?
"
```

**Remediation**:
1. Call `preview_generation` with simplified context to isolate issue
2. If Jinja2 error, guide user to fix template syntax
3. If missing variable, add to context or make optional in template (use `{{ var|default('fallback') }}`)
4. If missing file, verify template_path in config

**Escalation Criteria**:
- Escalate to user if: Complex template logic needs debugging, API credentials need configuration, or generator requires domain-specific knowledge

### Error 3: invalid_context

**Recognition**:
- Response contains `"error": {"code": "invalid_context"}`
- Error message: "Context parameter is not valid JSON" or "Failed to parse context string"
- Occurs when context parameter is malformed JSON string

**Agent Response**:
```
"The context data provided couldn't be parsed as valid JSON. This usually means:
1. JSON string has syntax errors (missing quotes, trailing commas)
2. Context was passed as string instead of object (or vice versa)
3. Claude Desktop serialized context in unexpected format

To resolve this:
- If passing JSON string: Ensure it's properly formatted: '{\"key\": \"value\"}'
- If passing object: Pass as {"key": "value"} directly
- Check for special characters needing escaping

Let me retry with properly formatted context.
"
```

**Remediation**:
1. Validate JSON syntax (use JSON.parse equivalent)
2. If passing as string, ensure double escaping for nested quotes
3. Prefer passing context as object (not string) when possible
4. Retry generation with corrected context format

**Escalation Criteria**:
- Escalate to user if: Context contains user-specific data that needs validation, or complex nested structures require user review

### Error 4: circular_reference

**Recognition**:
- Response contains `"error": {"code": "circular_reference"}` or similar dependency error
- Error message: "Circular dependency detected" or "Infinite recursion in artifact members"
- Occurs when artifact A references content that references artifact A (or longer cycles)

**Agent Response**:
```
"I detected a circular dependency in the artifact configuration. This means:
- Artifact A depends on Content X
- Content X depends on Artifact A (or through other intermediaries)

This creates an infinite loop and cannot be generated.

To resolve this:
1. Use choracompose:trace_dependencies to visualize the dependency graph
2. Identify the cycle (e.g., A → B → C → A)
3. Break the cycle by removing one dependency or restructuring

Would you like me to trace the dependencies to show you where the cycle occurs?
"
```

**Remediation**:
1. Call `trace_dependencies` to visualize dependency graph
2. Show user the cycle path
3. Suggest restructuring: either remove circular reference or create intermediate artifact
4. If collection-level cycle, check that collections don't reference themselves as members

**Escalation Criteria**:
- Escalate to user if: Cycle involves multiple artifacts requiring architectural decision, or user needs to choose which dependency to break

### Error Interpretation Guide

**Understanding Error Response Format**:

All chora-compose MCP tools return errors in a consistent format:
```json
{
  "success": false,
  "error": {
    "code": "error_code",
    "message": "Human-readable description",
    "details": {
      /* Error-specific context */
    }
  }
}
```

**Error Code Categories** (24 tools across 7 categories):

1. **Core Generation Errors** (5 tools):
   - `config_not_found` - Content/artifact config missing
   - `generation_failed` - Template/generator execution failed
   - `composition_failed` - Artifact assembly failed (missing content pieces)
   - `write_failed` - Output file write permission/disk issues
   - `invalid_context` - Context JSON parsing failed

2. **Config Lifecycle Errors** (4 tools):
   - `validation_error` - Config schema validation failed
   - `draft_creation_failed` - Ephemeral storage issue
   - `draft_not_found` - Draft ID doesn't exist
   - `save_failed` - Config file already exists (need overwrite=true)
   - `modification_failed` - Config update merge failed

3. **Storage Management Errors** (2 tools):
   - `invalid_retention` - Retention policy parameters invalid
   - `storage_error` - File permission or path issues
   - `content_not_found` - Content ID not in ephemeral storage
   - `referenced_by_artifacts` - Can't delete content in use (force=true needed)

4. **Discovery Errors** (6 tools):
   - `invalid_input` - Parameter constraint violation (limit, sort)
   - Note: Most discovery tools return empty lists instead of errors

5. **Validation Errors** (2 tools):
   - `validation_execution_failed` - Validation rule syntax error
   - `manifest_not_found` - Collection not generated yet (freshness check)

6. **Collection Operation Errors** (4 tools):
   - `circular_reference` - Nested collection cycle detected
   - `max_depth_exceeded` - Collection nesting > 10 levels

7. **Utility Errors** (1 tool):
   - None - `hello_world` always succeeds

**Quick Error Recovery Table**:

| Error Code | Quick Fix | Tool to Use |
|------------|-----------|-------------|
| `config_not_found` | List configs, verify ID | `list_content_configs` / `list_artifact_configs` |
| `generation_failed` | Test with preview, check template | `preview_generation` |
| `invalid_context` | Validate JSON, fix syntax | Retry with corrected context |
| `composition_failed` | Check dependencies | `trace_dependencies` |
| `circular_reference` | Trace deps, break cycle | `trace_dependencies` |
| `draft_not_found` | List drafts | `list_content_configs` (ephemeral=true) |
| `validation_error` | Check schema | `list_generators` for schema info |
| `storage_error` | Check permissions | Verify file system access |
| `referenced_by_artifacts` | Use force=true or remove refs | `trace_dependencies` |

**Agent Error Handling Best Practices**:

1. **Always check error.details first** - Contains specific context (file paths, IDs, constraints)
2. **Use discovery tools for recovery** - list_* tools help identify correct IDs/configs
3. **Preview before retrying** - Use `preview_generation` or `test_config` to validate fixes
4. **Explain to user clearly** - Translate technical error codes to plain language
5. **Offer actionable choices** - "Would you like me to: a) List configs, b) Create new config?"
6. **Don't retry blindly** - Understand error cause before retrying same operation
7. **Escalate when stuck** - If 2+ attempts fail with same error, ask user for guidance

**Additional Important Errors**:

### Error 5: composition_failed

**Recognition**: Artifact assembly failed due to missing content pieces

**Agent Response**:
```
"Artifact assembly failed because some content pieces are missing or failed to generate:
{list missing content IDs from error.details}

To resolve this:
1. Use choracompose:trace_dependencies to see all required content
2. Generate missing content pieces individually
3. Retry artifact assembly
"
```

**Remediation**: Call `trace_dependencies`, generate missing content, retry

### Error 6: validation_error

**Recognition**: Config doesn't match schema requirements

**Agent Response**:
```
"Configuration validation failed: {error.details.issue}
Field: {error.details.field}

Common causes:
1. Missing required field (e.g., generation.generator.type)
2. Invalid value type (string vs number)
3. Unknown generator type

To resolve:
1. Check generator schema with choracompose:list_generators
2. Fix config structure
3. Test with choracompose:test_config before saving
"
```

**Remediation**: Use `list_generators` to show schema, guide user to fix config

### Error 7: max_depth_exceeded

**Recognition**: Collection nesting depth > 10

**Agent Response**:
```
"Collection nesting is too deep (>10 levels). This usually indicates a design issue.

To resolve:
1. Flatten collection structure
2. Consider splitting into multiple top-level collections
3. Review nesting necessity - most use cases need ≤3 levels
"
```

**Remediation**: Explain nesting limits, suggest architecture changes

---

## 5. Integration Patterns for Agents

### Integration with Dependencies

**SAP-000 (SAP Framework)**:
- **Integration Point**: chora-compose Meta follows SAP-000 protocols for capability documentation structure
- **Usage Pattern**: When generating SAP documentation, validate output against SAP-000 requirements (5 core artifacts: capability-charter, protocol-spec, adoption-blueprint, awareness-guide, ledger)
- **Example**:
  ```bash
  # User requests: "Generate SAP-019 documentation"
  # Agent workflow:
  # 1. Validate request follows SAP-000 structure
  # 2. Use choracompose:generate_collection with sap-019-docs collection
  # 3. Verify all 5 artifacts generated (charter, spec, blueprint, awareness, ledger)
  # 4. Report completion with SAP-000 compliance confirmed
  ```

**SAP-017 (chora-compose Integration Guide)**:
- **Integration Point**: SAP-017 provides onboarding guide for setting up chora-compose, SAP-018 provides architecture reference
- **Usage Pattern**: When user new to chora-compose, reference SAP-017 for installation/setup, then use SAP-018 for advanced usage patterns
- **Example**:
  ```bash
  # User requests: "How do I use chora-compose?"
  # Agent response:
  # 1. Check if chora-compose installed (choracompose:hello_world)
  # 2. If not installed → point to SAP-017 adoption-blueprint for setup
  # 3. If installed → use SAP-018 awareness-guide for usage patterns
  # 4. For architecture questions → reference SAP-018 protocol-spec
  ```

### Common Integration Patterns

**Pattern 1: SAP Documentation Generation Workflow**
- **Scenario**: User requests "Generate complete SAP documentation for new capability"
- **Steps**:
  1. Validate SAP follows SAP-000 framework (5 core artifacts required)
  2. Create collection config for SAP (e.g., `sap-029-docs.json`) with 5 artifact members
  3. Create artifact configs for each document (capability-charter, protocol-spec, etc.)
  4. Create content configs for document sections (problem statement, solution, scope, etc.)
  5. Use `choracompose:generate_collection` to generate entire SAP
  6. Validate output against SAP-000 requirements
- **Result**: Complete SAP documentation set (5 artifacts) generated from templates with consistent structure

**Pattern 2: Iterative Config Development with User Feedback**
- **Scenario**: User wants to create custom content config through conversation
- **Steps**:
  1. Use `draft_config` to create initial config based on user requirements
  2. Use `test_config` to preview generation with sample context
  3. Show preview to user, gather feedback
  4. Use `modify_config` to apply changes based on feedback
  5. Repeat test → feedback → modify until satisfied
  6. Use `save_config` to persist final version
- **Result**: User-validated content config created conversationally without manual JSON editing

**Pattern 3: Dependency-Aware Artifact Assembly**
- **Scenario**: User requests artifact that depends on multiple content pieces
- **Steps**:
  1. Use `trace_dependencies` to identify all required content pieces
  2. Check which content exists in ephemeral storage
  3. Use `batch_generate` to generate missing content in parallel (max_parallel=4-8)
  4. Use `assemble_artifact` to combine all content into final artifact
  5. Validate artifact output meets requirements
- **Result**: Artifact assembled efficiently with automatic dependency resolution and parallel generation

**Pattern 4: Collection Freshness Validation Loop**
- **Scenario**: User has existing collection and wants to ensure it's up to date
- **Steps**:
  1. Use `list_collection_members` to enumerate all artifacts in collection
  2. Use `check_freshness` for each member to detect stale content
  3. If stale detected, use `trace_dependencies` to find cascading staleness
  4. Regenerate stale content/artifacts in topological order (dependencies first)
  5. Use `check_collection_cache` to verify collection cache updated
- **Result**: Collection incrementally updated with only stale members regenerated (efficient)

---

## 6. Agent Best Practices

### DO

✅ **Always validate config existence before generation**
   - **Reason**: Prevents config_not_found errors and wasted API calls
   - **Example**:
     ```bash
     # Before generate_content, call:
     choracompose:list_content_configs {"include_metadata": false}
     # Verify config_id in returned list, then proceed
     ```

✅ **Use preview_generation for testing before saving**
   - **Reason**: Catch template errors, missing variables, and output issues before committing to ephemeral storage
   - **Example**:
     ```bash
     # When creating new config, test first:
     choracompose:draft_config {...}
     choracompose:test_config {"config_id": "new-config", "test_context": {...}}
     # Review output, iterate with modify_config, then save_config
     ```

✅ **Leverage batch_generate for multiple contents**
   - **Reason**: Parallel execution (max_parallel=4-10) reduces total generation time by 2.6-4.8× vs sequential
   - **Example**:
     ```bash
     # Instead of 5 sequential generate_content calls:
     choracompose:batch_generate {
       "content_ids": ["header", "features", "install", "usage", "faq"],
       "shared_context": {"project": "chora-base"},
       "max_parallel": 5
     }
     ```

✅ **Let SHA-256 caching work automatically**
   - **Reason**: Caching achieves 94%+ hit rates in production, dramatically speeds up regeneration of unchanged content
   - **Example**:
     ```bash
     # Default force=false lets cache work:
     choracompose:generate_content {"content_config_id": "readme", "context": {"version": "2.0"}}
     # Second call with same context hits cache (instant return)
     ```

✅ **Check dependencies before assembling artifacts**
   - **Reason**: Prevents missing_content errors and allows proactive generation of missing pieces
   - **Example**:
     ```bash
     # Before assemble_artifact:
     choracompose:trace_dependencies {"artifact_config_id": "complete-readme"}
     # If missing dependencies found, generate them first with batch_generate
     ```

✅ **Use MERGE context propagation for collections**
   - **Reason**: Allows shared variables (project name, version) while preserving member-specific context
   - **Example**:
     ```json
     {
       "shared_context": {"project": "chora-base", "version": "2.0"},
       "context_propagation": {"mode": "MERGE"},
       "members": [
         {"artifact_config_id": "readme", "context": {"author": "Alice"}},
         {"artifact_config_id": "license", "context": {"author": "Bob"}}
       ]
     }
     // Each member gets shared + their own context merged
     ```

### DON'T

❌ **Don't skip config validation before generation**
   - **Reason**: Results in cryptic errors and wasted generation attempts
   - **Instead**: Always call list_content_configs or validate_collection_config first to verify config exists and is valid

❌ **Don't use force=true unnecessarily**
   - **Reason**: Bypasses SHA-256 cache, wastes computation, and increases generation time
   - **Instead**: Only use force when template has changed but context hasn't, or when explicitly troubleshooting cache issues

❌ **Don't generate without checking dependencies**
   - **Reason**: Artifacts fail with missing_content if dependencies not generated first, requiring manual retry
   - **Instead**: Use trace_dependencies to identify missing content, then batch_generate before assembling

❌ **Don't call generate_content in loops for bulk operations**
   - **Reason**: Sequential generation is 2.6-4.8× slower than batch_generate with parallel execution
   - **Instead**: Collect all content IDs and use batch_generate with max_parallel=4-10

❌ **Don't ignore error details in generation_failed responses**
   - **Reason**: Error details contain specific information (Jinja2 syntax error line, missing variable name) needed for remediation
   - **Instead**: Parse error.details field and use specifics to guide user to fix root cause

❌ **Don't use OVERRIDE context propagation without understanding implications**
   - **Reason**: OVERRIDE replaces all member context with shared context, losing member-specific data
   - **Instead**: Use MERGE for most cases (combines contexts), use OVERRIDE only when forcing uniform values across all members

---

## 7. Validation & Verification

### Pre-Flight Checks

Before executing SAP-018 functionality, verify:
- [ ] chora-compose MCP server is running and accessible
- [ ] Config files exist for requested operation (content/artifact/collection)
- [ ] Dependencies resolved (for artifacts: all content configs exist; for collections: all artifact configs exist)
- [ ] Context data is valid JSON (no syntax errors, required fields present)
- [ ] Templates referenced in configs exist on filesystem (for jinja2 generator with template_path)

**Verification Command**:
```bash
# 1. Test MCP server connection
choracompose:hello_world {}
# Expected: {"success": true, "message": "Hello from chora-compose!"}

# 2. List available configs
choracompose:list_content_configs {}
choracompose:list_artifact_configs {}

# 3. For artifacts, check dependencies
choracompose:trace_dependencies {"artifact_config_id": "target-artifact"}

# 4. For collections, validate config
choracompose:validate_collection_config {"collection_config_id": "target-collection"}
```

### Post-Execution Validation

After completing work, agents should:

**Validation Step 1**: Verify success field in response
```bash
# Check response structure
{
  "success": true,  // Must be true
  "status": "generated|assembled|...",  // Check status appropriate for operation
  ...
}
```
**Expected**: `success: true` and status indicates operation completed (not skipped unless expected)

**Validation Step 2**: Verify output exists on filesystem (for artifacts)
```bash
# For artifacts, check output file created
ls -lh <output_path>
# For content, check ephemeral storage
ls ~/.chora-compose/ephemeral/content/<content_config_id>/
```
**Expected**: File exists with non-zero size

**Validation Step 3**: Validate against schema (for collections/artifacts)
```bash
# For collections, check all members generated
choracompose:list_collection_members {"collection_config_id": "target"}
# Compare members_generated count against expected

# For artifacts, check content_count matches expected
# Response metadata should show all content pieces included
```
**Expected**: Counts match configuration (no missing members)

### Success Criteria

Operation succeeds when:
1. **Response validation**: `success: true`, no error field, appropriate status (generated/assembled, not failed)
2. **Output verification**: All expected files exist with non-zero content (artifacts on filesystem, content in ephemeral storage)
3. **Dependency resolution**: For artifacts/collections, all dependencies generated (metadata.missing_content empty)
4. **Cache efficiency** (for collections): Cache hit rate > 70% indicates effective caching (check metadata.cache_hit_rate)
5. **Consistency checks**: For collections, all members use consistent context propagation mode, no circular dependencies

---

## 8. Performance Guidelines for Agents

### Performance Targets

| Operation | Target Time | Notes |
|-----------|-------------|-------|
| `generate_content` (cached) | < 50ms | SHA-256 cache hit returns immediately |
| `generate_content` (uncached, jinja2) | 50-200ms | Template rendering overhead |
| `assemble_artifact` (4 contents) | 100-300ms | Depends on content generation time |
| `batch_generate` (10 contents, parallel) | 200-500ms | 2.6-4.8× faster than sequential |
| `generate_collection` (18 artifacts, parallel) | 5-15s | 94%+ cache hit rate reduces to 2-5s |
| `validate_collection_config` | < 100ms | JSON schema validation only |

### Optimization Tips for Agents

**Tip 1: Use batch_generate with optimal max_parallel**
- **When**: Generating 3+ content pieces with no dependencies between them
- **Benefit**: 2.6-4.8× speedup vs sequential generation (measured with asyncio parallel execution)
- **How**:
  ```json
  {
    "content_ids": ["piece1", "piece2", "piece3", "piece4"],
    "max_parallel": 4
  }
  ```
  - Sweet spot: max_parallel=4-10 (diminishing returns beyond 10 due to I/O contention)
  - Don't use max_parallel=1 (defeats parallelization)

**Tip 2: Leverage SHA-256 caching (don't use force unnecessarily)**
- **When**: Context hasn't changed between generations
- **Benefit**: 94%+ cache hit rate reduces generation time from 200ms → 50ms (4× speedup)
- **How**:
  - Default `force=false` enables caching
  - Cache key = SHA-256(content_config_id + context)
  - Identical context → cache hit (instant return)
  - Only use `force=true` when template changed but context same

**Tip 3: Use parallel execution strategy for collections**
- **When**: Collection members have no ordering dependencies
- **Benefit**: Parallel strategy achieves 2.6-4.8× speedup over sequential (8 workers on typical hardware)
- **How**:
  ```json
  {
    "execution": {
      "strategy": "parallel",
      "max_workers": 8
    }
  }
  ```
  - Use sequential only when order matters (e.g., numbered chapters)
  - Parallel execution requires sufficient system resources (CPU, memory)

**Tip 4: Reuse ephemeral storage between operations**
- **When**: Multiple artifacts reference same content pieces
- **Benefit**: Content generated once, reused by multiple artifacts (avoids redundant generation)
- **How**:
  - Content automatically stored in `~/.chora-compose/ephemeral/content/`
  - Artifacts check ephemeral storage before regenerating
  - Don't call cleanup_ephemeral until entire workflow complete

**Tip 5: Minimize context size for cache efficiency**
- **When**: Context includes large data structures or unnecessary fields
- **Benefit**: Smaller contexts → faster cache key computation, less memory usage
- **How**:
  - Only include fields actually used in template (check cache_key_fields in config)
  - Use external_file sources for large data instead of inline_data
  - Example: Instead of embedding 1000-line JSON in context, reference file path

---

## 9. Examples for Agent Learning

### Example 1: Generate README for New Project

**User Request**:
```
"Generate a README for my project called 'data-pipeline' that processes CSV files"
```

**Agent Analysis**:
- Identified need for: Content generation with template + context
- Dependencies checked: chora-compose installed (choracompose:hello_world)
- Approach: Check for existing readme config, generate with project-specific context

**Agent Response**:
```
"I'll generate a README for your 'data-pipeline' project. Let me check if a README template config exists and generate it with your project details."
```

**Execution**:
```bash
# Step 1: Check for readme configs
choracompose:list_content_configs {"include_metadata": false}

# Step 2: Generate README with context (assuming "project-readme" config exists)
choracompose:generate_content {
  "content_config_id": "project-readme",
  "context": {
    "project_name": "data-pipeline",
    "description": "Processes CSV files for data transformation",
    "features": ["CSV parsing", "Data validation", "ETL pipeline"]
  },
  "force": false
}
```

**Result**:
```json
{
  "success": true,
  "content_id": "project-readme",
  "content": "# data-pipeline\n\nProcesses CSV files for data transformation...",
  "generator": "jinja2",
  "status": "generated",
  "duration_ms": 87,
  "metadata": {
    "context_variables": ["project_name", "description", "features"],
    "ephemeral_stored": true,
    "storage_path": "~/.chora-compose/ephemeral/content/project-readme/abc123.txt"
  }
}
```

**Agent Follow-Up**:
```
"I've generated the README for 'data-pipeline' using the project-readme template. The content includes your project name, description, and features. You can find it in ephemeral storage at ~/.chora-compose/ephemeral/content/project-readme/abc123.txt. Would you like me to save this to a file or make any modifications?"
```

### Example 2: Create Complete SAP Documentation (Collection)

**User Request**:
```
"Generate all documentation for SAP-029 (Git-Anchored Content)"
```

**Agent Analysis**:
- Identified need for: Collection generation (5 artifacts per SAP-000 framework)
- Dependencies checked: SAP-000 compliance (5 core artifacts required), SAP-029 collection config exists
- Approach: Validate collection config, preview members, generate with parallel execution

**Agent Response**:
```
"I'll generate the complete SAP-029 documentation set following the SAP-000 framework (5 core artifacts: capability-charter, protocol-spec, adoption-blueprint, awareness-guide, ledger). Let me validate the collection config first."
```

**Execution**:
```bash
# Step 1: Validate collection config
choracompose:validate_collection_config {"collection_config_id": "sap-029-docs"}

# Step 2: Preview collection members
choracompose:list_collection_members {"collection_config_id": "sap-029-docs"}

# Step 3: Generate collection with parallel execution
choracompose:generate_collection {
  "collection_config_id": "sap-029-docs",
  "force": false,
  "force_members": false
}
```

**Result**:
```json
{
  "success": true,
  "collection_id": "sap-029-docs",
  "members_generated": 5,
  "total_artifacts": 5,
  "total_content": 25,
  "duration_ms": 3421,
  "execution_strategy": "parallel",
  "metadata": {
    "cache_hit_rate": 0.12,
    "parallel_workers": 5,
    "context_propagation_mode": "MERGE",
    "artifacts": [
      "capability-charter.md",
      "protocol-spec.md",
      "adoption-blueprint.md",
      "awareness-guide.md",
      "ledger.md"
    ]
  }
}
```

**Agent Follow-Up**:
```
"I've successfully generated all SAP-029 documentation (5 artifacts: capability-charter, protocol-spec, adoption-blueprint, awareness-guide, ledger). Generation took 3.4 seconds with 12% cache hit rate (most content was new). All artifacts follow SAP-000 framework structure and are ready for review. The files are in the outputs/sap-029/ directory."
```

### Example 3: Handle Missing Config with Conversational Creation

**User Request**:
```
"Generate a changelog for my releases"
```

**Agent Analysis**:
- Challenge: No "changelog" config exists, need to create one conversationally
- Solution: Use draft → test → modify → save lifecycle to create config interactively

**Agent Response**:
```
"I don't see an existing changelog config. Let me create one for you. What information should the changelog include? (e.g., version, date, changes, contributors)"
```

**User Follow-Up**: "Include version, date, and a list of changes"

**Execution**:
```bash
# Step 1: Draft config based on requirements
choracompose:draft_config {
  "config_type": "content",
  "config_id": "changelog",
  "template": {
    "type": "content_config",
    "version": "3.1",
    "id": "changelog",
    "generator": {"type": "jinja2"},
    "elements": {
      "template": "# Changelog\n\n## {{ version }} ({{ date }})\n\n{% for change in changes %}- {{ change }}\n{% endfor %}"
    },
    "inputs": {
      "sources": [{"type": "inline_data", "data": {}}]
    }
  }
}

# Step 2: Test with sample data
choracompose:test_config {
  "config_id": "changelog",
  "test_context": {
    "version": "1.0.0",
    "date": "2025-11-04",
    "changes": ["Initial release", "Added feature X", "Fixed bug Y"]
  }
}

# Step 3: Save config after user approves preview
choracompose:save_config {"config_id": "changelog"}

# Step 4: Generate with actual data
choracompose:generate_content {
  "content_config_id": "changelog",
  "context": {
    "version": "1.0.0",
    "date": "2025-11-04",
    "changes": ["Initial release", "Added feature X", "Fixed bug Y"]
  }
}
```

**Result**:
```
# Changelog

## 1.0.0 (2025-11-04)

- Initial release
- Added feature X
- Fixed bug Y
```

**Agent Follow-Up**:
```
"I've created and saved the changelog config. The generated changelog includes version 1.0.0 with your changes. For future releases, you can regenerate with updated context (new version, date, and changes). The config is saved at configs/content/changelog.json for reuse."
```

---

## 10. Frequently Asked Questions (Agent-Focused)

**Q1: When should I use generate_content vs preview_generation?**

**A**: Use `preview_generation` when testing templates or troubleshooting errors (dry-run, doesn't save to ephemeral storage). Use `generate_content` for actual production generation that you want cached and reusable.

**Decision tree**:
- Testing new template → `preview_generation` (iterate without polluting cache)
- Production generation → `generate_content` (saves to ephemeral storage for reuse)
- Debugging generation_failed error → `preview_generation` with simplified context

**Example**:
```bash
# Testing: Use preview_generation
choracompose:preview_generation {
  "content_config_id": "new-template",
  "context": {"test": "value"}
}
# Review output, fix template, retry

# Production: Use generate_content
choracompose:generate_content {
  "content_config_id": "new-template",
  "context": {"production": "data"}
}
```

---

**Q2: How do I handle missing dependencies in artifacts?**

**A**: Use `trace_dependencies` to identify missing content, then generate missing pieces with `batch_generate` before assembling artifact.

**Workflow**:
1. Call `trace_dependencies` → returns list of required content configs
2. Check which exist in ephemeral storage
3. Generate missing content with `batch_generate` (parallel)
4. Retry `assemble_artifact`

**Example**:
```bash
# Step 1: Trace dependencies
choracompose:trace_dependencies {"artifact_config_id": "complete-readme"}
# Returns: {"required_content": ["header", "features", "install", "usage"]}

# Step 2: Generate missing (assuming "install" and "usage" missing)
choracompose:batch_generate {
  "content_ids": ["install", "usage"],
  "shared_context": {"project": "chora-base"},
  "max_parallel": 2
}

# Step 3: Assemble artifact
choracompose:assemble_artifact {"artifact_config_id": "complete-readme"}
```

---

**Q3: What's the difference between force and force_members in collections?**

**A**: `force=true` regenerates the collection-level config/manifest (forces recomputation of collection metadata). `force_members=true` forces regeneration of all member artifacts (bypasses their caches).

**Use cases**:
- `force=true, force_members=false`: Collection config changed, but member artifacts unchanged → regenerate collection logic only
- `force=false, force_members=true`: Collection config unchanged, but want to regenerate all members (e.g., templates changed)
- `force=true, force_members=true`: Nuclear option, regenerate everything (rarely needed)

**Example**:
```bash
# Collection config changed (context propagation mode updated)
choracompose:generate_collection {
  "collection_config_id": "sap-docs",
  "force": true,
  "force_members": false
}

# All templates changed, need to regenerate outputs
choracompose:generate_collection {
  "collection_config_id": "sap-docs",
  "force": false,
  "force_members": true
}
```

---

**Q4: How do I debug generation_failed errors?**

**A**: Parse error.details for specifics (Jinja2 syntax error, missing variable, etc.), then use `preview_generation` with simplified context to isolate issue.

**Debugging workflow**:
1. Check error.details for error type (template syntax, undefined variable, missing file)
2. If template error → review template syntax (missing {% endfor %}, unescaped braces)
3. If missing variable → use `preview_generation` with minimal context to identify which variable
4. If missing file → verify template_path in config points to existing file
5. Fix issue, retry with `generate_content`

**Example**:
```bash
# Error: "UndefinedError: 'project_version' is undefined"
# Debug with preview_generation and minimal context
choracompose:preview_generation {
  "content_config_id": "readme",
  "context": {"project_name": "test"}
}
# Error persists → add project_version to context

choracompose:preview_generation {
  "content_config_id": "readme",
  "context": {"project_name": "test", "project_version": "1.0"}
}
# Success → now use full context with generate_content
```

---

**Q5: When should I use batch_generate vs individual generate_content calls?**

**A**: Use `batch_generate` when generating 3+ independent content pieces (no dependencies between them) for 2.6-4.8× speedup via parallel execution. Use individual `generate_content` for single pieces or when generation order matters.

**Decision criteria**:
- 1-2 content pieces → individual `generate_content` (no parallelization benefit)
- 3+ independent pieces → `batch_generate` with max_parallel=4-10
- Dependencies between pieces → sequential `generate_content` (or generate dependencies first)
- Need granular error handling → individual calls (batch_generate has coarser error reporting)

**Example**:
```bash
# BAD: Loop with individual calls (slow)
for content_id in ["header", "features", "install", "usage", "faq"]:
  choracompose:generate_content {"content_config_id": content_id}
# Total time: 5 × 200ms = 1000ms

# GOOD: Batch with parallelization (fast)
choracompose:batch_generate {
  "content_ids": ["header", "features", "install", "usage", "faq"],
  "max_parallel": 5
}
# Total time: ~250ms (4× faster)
```

---

## 11. Related SAP Awareness

**Agents should be aware of**:

- **SAP-000 (SAP Framework)**:
  - **Relationship**: chora-compose Meta (SAP-018) documents the architecture for generating SAP-000 compliant documentation
  - **When to use together**: When generating any SAP documentation, validate structure against SAP-000 requirements (5 core artifacts: capability-charter, protocol-spec, adoption-blueprint, awareness-guide, ledger)
  - **Cross-reference workflow**:
    1. User requests SAP documentation generation
    2. Check SAP-000 for structural requirements (what artifacts needed)
    3. Use SAP-018 tools (choracompose:generate_collection) to generate artifacts
    4. Validate output follows SAP-000 framework conventions

- **SAP-017 (chora-compose Integration Guide)**:
  - **Relationship**: SAP-017 is the onboarding guide (installation, setup, first-time usage), SAP-018 is the advanced architecture reference (MCP tools, Collections, generators, caching)
  - **When to use together**: SAP-017 for getting started, SAP-018 for understanding how it works and advanced patterns
  - **Cross-reference workflow**:
    1. User new to chora-compose → Point to SAP-017 adoption-blueprint for setup
    2. User has setup questions → Reference SAP-017 protocol-spec for configuration
    3. User needs advanced usage (Collections, custom generators) → Reference SAP-018 protocol-spec and awareness-guide
    4. User troubleshooting → SAP-017 for installation issues, SAP-018 for generation/architecture issues

- **SAP-029 (Git-Anchored Content)** (future/proposed):
  - **Relationship**: Would extend chora-compose with git_reference context source type for version-controlled data
  - **How it complements**: Enables content generation from git repository files (e.g., pull README from specific commit SHA for context)
  - **Integration pattern**: Use choracompose:generate_content with context sources referencing git objects

**Cross-SAP Decision Tree**:
```
User request involves documentation generation
   │
   ├─ "How do I install chora-compose?"
   │   └─> SAP-017 adoption-blueprint
   │
   ├─ "How does chora-compose caching work?"
   │   └─> SAP-018 protocol-spec (SHA-256 caching section)
   │
   ├─ "Generate SAP documentation"
   │   └─> SAP-000 (structure) + SAP-018 (tools)
   │
   └─ "What MCP tools are available?"
       └─> SAP-018 awareness-guide (Quick Reference section)
```

---

## 12. Changelog for Agents

### Version 1.0.0 (2025-11-04)

**Initial Release**:
- Complete awareness guide for 24 MCP tools in chora-compose v1.5.0
- 12 sections: Quick Start, Core Concepts, Workflows, Quick Reference, Error Handling, Integration, Best Practices, Validation, Performance, Examples, FAQs, Related SAPs
- 5 detailed workflows: single content, multi-content artifact, collection, conversational config, freshness validation
- 4 error handling patterns: config_not_found, generation_failed, invalid_context, circular_reference
- 4 integration patterns: SAP documentation generation, iterative config development, dependency-aware assembly, freshness validation loop
- 6 DOs and 6 DON'Ts for agent best practices
- 5 performance optimization tips (batch_generate, caching, parallel execution, ephemeral reuse, context minimization)
- 3 complete examples with analysis, execution, results, and follow-up
- 5 FAQs with actionable guidance and examples
- Cross-references to SAP-000 (framework) and SAP-017 (integration guide)

**Agent Impact**:
- Agents can now quickly understand when to use chora-compose tools (Quick Start section)
- Decision trees guide tool selection (Core Concepts section)
- Step-by-step workflows reduce implementation time from 10-20 hours to 2-4 hours
- Error handling templates provide consistent user-facing error messages
- Best practices prevent common mistakes (unnecessary force=true, sequential generation for bulk operations)
- Performance tips enable 2.6-4.8× speedup through batch_generate and parallel execution
- Examples demonstrate real-world usage patterns for agent learning
- FAQs answer common questions without needing to read protocol-spec

---

## References for Agents

**Related Documentation**:
- [capability-charter.md](./capability-charter.md) - Full problem/solution context
- [protocol-spec.md](./protocol-spec.md) - Technical specifications
- [adoption-blueprint.md](./adoption-blueprint.md) - Installation guide
- [ledger.md](./ledger.md) - Version history

**External Resources**:
- [Model Context Protocol (MCP) Specification](https://spec.modelcontextprotocol.io/) - MCP protocol documentation for understanding tool interfaces
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/) - Template syntax reference for jinja2 generator
- [JSON Schema Specification](https://json-schema.org/) - Schema validation reference for config files
- [OpenTelemetry Events](https://opentelemetry.io/docs/concepts/events/) - Event emission format for observability integration
- [Anthropic API Documentation](https://docs.anthropic.com/claude/reference/) - API reference for code_generation generator (optional dependency)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-04
**Maintained by**: Victor
**Agent Feedback**: [Contact Victor with agent usage feedback]
