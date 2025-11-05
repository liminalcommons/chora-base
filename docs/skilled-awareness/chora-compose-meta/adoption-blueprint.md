# Adoption Blueprint: chora-compose Meta

**SAP ID**: SAP-018
**Version**: 1.0.0
**Last Updated**: 2025-11-04

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-018 chora-compose Meta across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Understanding core concepts and basic MCP tools | 2-4 hours | Daily cleanup | First-time users, proof-of-concept, learning the 3-tier architecture |
| **Level 2: Advanced** | Artifact assembly, collections, context propagation, caching optimization | 4-8 hours | Weekly cache reviews | Regular users, production workflows, multi-artifact projects |
| **Level 3: Mastery** | Custom generators, freshness tracking, production optimization, event telemetry | 8-16 hours | Monthly reviews | **Recommended for production**, custom development, ecosystem extension |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
- **First-time users** getting started with chora-compose Meta architecture
- **Understanding the 3-tier model** (Content → Artifact → Collection)
- **Running first content generation** with MCP tools via Claude Desktop
- **Development and testing environments** for proof-of-concept work
- **Learning basic caching mechanics** (SHA-256 deterministic keys)

### Time Estimate

- **Setup**: 2-4 hours (one-time investment)
- **Learning Curve**: Easy - Focus on understanding core concepts and testing 5-6 basic MCP tools

### Prerequisites

**Required**:
- **chora-compose v1.5.0+** installed (refer to SAP-017 for installation)
- **Python 3.12+** or **Node.js 22+** (depending on chora-compose installation method)
- **Claude Desktop with MCP configured** (chora-compose MCP server active)
- **SAP-000** (SAP Framework) completed for understanding SAP structure
- **SAP-017** (chora-compose Integration) installed and validated

**Recommended**:
- Familiarity with **JSON configuration files** (content configs, artifact configs)
- Basic understanding of **template engines** (Jinja2 experience helpful but not required)
- Access to **chora-compose documentation** (AGENTS.md, collections-architecture.md)

### Step-by-Step Instructions

#### Step 1.1: Verify MCP Server Connection

Test that chora-compose MCP server is running and accessible via Claude Desktop.

**Action**:
In Claude Desktop, ask Claude to call the hello_world tool:
```
"Call the choracompose:hello_world tool to verify the MCP server is running"
```

**Expected Output**:
```json
{
  "success": true,
  "message": "Hello from chora-compose MCP server!",
  "version": "1.5.0",
  "capabilities": ["generate_content", "assemble_artifact", "..."]
}
```

**Verification**:
- Response shows `success: true`
- Version is 1.5.0 or higher
- Capabilities list includes core tools (generate_content, assemble_artifact, etc.)

#### Step 1.2: Explore Available Generators

List all available generators to understand what content generation engines are available.

**Action**:
In Claude Desktop, ask:
```
"Use choracompose:list_generators to show all available generators"
```

**Expected Output**:
```json
{
  "success": true,
  "generators": [
    {
      "name": "demonstration",
      "description": "Example-based generation (no templating)",
      "supports_templates": false
    },
    {
      "name": "jinja2",
      "description": "Full Jinja2 template engine with filters, macros, inheritance",
      "supports_templates": true
    },
    {
      "name": "template_fill",
      "description": "Simple {{var}} substitution (lightweight)",
      "supports_templates": true
    },
    {
      "name": "bdd_scenario",
      "description": "Gherkin BDD scenario generation",
      "supports_templates": true
    },
    {
      "name": "code_generation",
      "description": "AI-powered code generation via Anthropic API",
      "supports_templates": false
    }
  ]
}
```

**Verification**:
- All 5 builtin generators are listed
- jinja2 and template_fill show `supports_templates: true`

#### Step 1.3: List Existing Content Configs

Discover what content configurations already exist in your project.

**Action**:
In Claude Desktop:
```
"Use choracompose:list_content_configs to show all content configurations"
```

**Expected Output**:
```json
{
  "success": true,
  "configs": [
    {
      "id": "welcome-message",
      "generator": "jinja2",
      "path": "configs/content/welcome-message.json"
    },
    {
      "id": "readme-intro",
      "generator": "template_fill",
      "path": "configs/content/readme-intro.json"
    }
  ],
  "total_count": 2
}
```

**Verification**:
- At least 1 content config exists (if starting fresh, you may see empty list - that's okay)
- Each config shows ID, generator type, and file path

#### Step 1.4: Generate Your First Content

Generate content from an existing config (or ask Claude to help create a simple test config first).

**Action**:
In Claude Desktop:
```
"Use choracompose:generate_content with content_config_id 'welcome-message' and context {"user": "Alice"}"
```

**Expected Output**:
```json
{
  "success": true,
  "content_id": "welcome-message",
  "content": "Welcome to chora-compose, Alice!",
  "generator": "jinja2",
  "status": "generated",
  "duration_ms": 87,
  "metadata": {
    "context_variables": ["user"],
    "ephemeral_stored": true,
    "storage_path": "~/.chora-compose/ephemeral/content/welcome-message/abc123.txt"
  }
}
```

**Verification**:
- `success: true`
- `status: "generated"` (first time) or `"skipped"` (if cached from previous run)
- Content shows template substitution worked (user name appears)
- Ephemeral storage path is provided

#### Step 1.5: Preview Generation Without Saving

Test preview_generation tool for dry-run content generation (doesn't save to cache).

**Action**:
In Claude Desktop:
```
"Use choracompose:preview_generation to preview content for 'welcome-message' with context {"user": "Bob"}"
```

**Expected Output**:
```json
{
  "success": true,
  "content_id": "welcome-message",
  "preview_content": "Welcome to chora-compose, Bob!",
  "content_length": 32,
  "content_hash": "def456",
  "generator": "jinja2",
  "duration_ms": 45
}
```

**Verification**:
- Preview shows generated content without saving to ephemeral storage
- Content differs from Step 1.4 due to different context (Bob vs Alice)
- Useful for testing templates before committing

#### Step 1.6: View Ephemeral Storage

Check ephemeral storage directory to see cached content.

**Action**:
In your terminal (outside Claude Desktop):
```bash
# List ephemeral storage contents
ls -la ~/.chora-compose/ephemeral/content/

# View a specific content piece (use ID from Step 1.4)
cat ~/.chora-compose/ephemeral/content/welcome-message/*.txt
```

**Expected Output**:
```
# Directory listing shows generated content folders
drwxr-xr-x  welcome-message/
drwxr-xr-x  readme-intro/

# Content file shows the generated output
Welcome to chora-compose, Alice!
```

**Verification**:
- Ephemeral directory exists at `~/.chora-compose/ephemeral/content/`
- Generated content from Step 1.4 is stored with SHA-256 hash filename
- Content matches what was returned in Step 1.4 response

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] MCP server responds successfully to `choracompose:hello_world`
- [ ] Can list all 5 builtin generators (demonstration, jinja2, template_fill, bdd_scenario, code_generation)
- [ ] Can list existing content configs (or see empty list if starting fresh)
- [ ] Successfully generated at least 1 content piece with `generate_content`
- [ ] Preview generation works with `preview_generation`
- [ ] Ephemeral storage directory exists at `~/.chora-compose/ephemeral/content/`
- [ ] Can view generated content files in ephemeral storage
- [ ] Understand the difference between generate_content (saves to cache) and preview_generation (dry-run)
- [ ] Understand SHA-256 caching (same context = cache hit, different context = new generation)

#### Validation Commands

```bash
# Primary validation
python scripts/sap-evaluator.py --quick SAP-018

# Expected output:
# ✅ SAP-018 (chora-compose-meta)
#    Level: 1
#    Next: Level 2
# ✅ Validation passed
```

### Common Issues (Level 1)

#### Issue 1: MCP Server Not Responding

**Symptoms**:
- `choracompose:hello_world` times out or returns error
- Claude Desktop says "Tool not found" or "MCP server not available"
- No chora-compose tools appear in Claude Desktop's tool list

**Solution**:
1. Check Claude Desktop MCP configuration in `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent
2. Verify chora-compose MCP server command is correct: `"command": "uvx", "args": ["--from", "chora-compose", "chora-compose-mcp"]` (for uvx) or similar
3. Restart Claude Desktop completely (Quit and reopen)
4. Check chora-compose logs for errors: `~/.chora-compose/logs/mcp-server.log`
5. Verify chora-compose is installed: `pip list | grep chora-compose` or `npm list -g | grep chora-compose`

**Prevention**:
- Follow SAP-017 adoption-blueprint carefully for MCP server configuration
- Keep chora-compose version up-to-date (v1.5.0+)
- Test MCP server connection after any Claude Desktop updates

#### Issue 2: No Content Configs Found

**Symptoms**:
- `choracompose:list_content_configs` returns empty array
- `generate_content` returns `config_not_found` error
- Fresh project with no existing configs

**Solution**:
1. Verify you're in the correct project directory (configs should be in `./configs/content/`)
2. Create your first content config:
   - In Claude Desktop, ask: "Help me create a simple content config for a welcome message using template_fill generator"
   - Claude will use `draft_config` → `test_config` → `save_config` lifecycle to create it
3. Alternatively, manually create `configs/content/test-config.json` following content config v3.1 schema
4. Verify config saved correctly: `ls -la configs/content/`

**Prevention**:
- Keep example/template configs in your project for reference
- Use `draft_config` for creating new configs (validates schema automatically)
- Document your project's content configs in a README

#### Issue 3: Generation Fails with Template Error

**Symptoms**:
- `generate_content` returns `generation_failed` error
- Error details mention "UndefinedError" or "TemplateSyntaxError"
- Jinja2 template has syntax issues

**Solution**:
1. Check error details in response for specific error (e.g., "variable 'user' is undefined")
2. Use `preview_generation` with minimal context to isolate the issue
3. For undefined variables: Add variable to context or make optional in template with `{{ var|default('fallback') }}`
4. For syntax errors: Review Jinja2 syntax (matching `{% if %}` with `{% endif %}`, `{% for %}` with `{% endfor %}`)
5. Test template incrementally (start simple, add complexity gradually)

**Prevention**:
- Always use `preview_generation` before `generate_content` for new templates
- Keep templates simple initially (avoid complex logic in Level 1)
- Use `template_fill` generator for simple substitution (no Jinja2 syntax to debug)

#### Issue 4: Cached Content Not Updating

**Symptoms**:
- Changed template but `generate_content` returns old output
- `status: "skipped"` even though you want new generation
- Context is same but template has changed

**Solution**:
1. Use `force: true` parameter to bypass cache:
   - In Claude Desktop: "Generate content with config 'welcome-message', context {"user": "Alice"}, and force regeneration"
2. Or cleanup ephemeral storage: In Claude Desktop, "Use choracompose:cleanup_ephemeral with keep_versions=1"
3. Understand caching: SHA-256 hash = content_config_id + context (template changes don't affect cache key)

**Prevention**:
- Use `force: true` when you know template changed but context is same
- Understand that caching is based on (config ID + context), not template content
- For development/testing, use `preview_generation` (never caches)

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds:
- **Artifact Assembly**: Combining multiple content pieces into single files (multi-section documents)
- **Collections Generation**: Bulk coordination of multiple artifacts with parallel execution
- **Context Propagation**: MERGE/OVERRIDE/ISOLATE modes for shared context across collection members
- **Cache Optimization**: Achieving 70-85% cache hit rates through proper context management
- **Parallel Execution**: 2.6-4.8× speedup using batch_generate and parallel collection strategies
- **Dependency Tracking**: Understanding and managing content/artifact dependencies

Suitable for:
- **Production workloads** requiring consistent multi-file generation
- **Team collaboration** with shared configs and templates
- **Regular usage patterns** generating documentation sets, API docs, project scaffolding

### Time Estimate

- **Additional Setup**: 4-8 hours (beyond Level 1)
- **Learning Curve**: Moderate - Understanding Collections 3-tier architecture, context propagation modes, caching strategies

### Prerequisites

**From Level 1**:
- All Level 1 steps completed and validated
- Successfully generated at least 3-5 content pieces
- Understand SHA-256 caching mechanics
- Comfortable using MCP tools via Claude Desktop

**Additional Requirements**:
- **Familiarity with JSON schemas** (artifact config v3.1, collection config v1.0)
- **Understanding of template composition** (how multiple content pieces combine)
- **Basic knowledge of context merging** (how MERGE mode combines contexts)
- **Understanding of parallel vs sequential execution** tradeoffs

### Step-by-Step Instructions

#### Step 2.1: Create and Test Artifact Config

Create an artifact config that combines multiple content pieces into a single file.

**Action**:
In Claude Desktop:
```
"Help me create an artifact config that combines 3 content pieces (header, body, footer) into a single README.md file using choracompose:draft_config"
```

Claude will guide you through creating an artifact config with:
- Multiple content members (header, body, footer)
- Composition strategy (concatenation)
- Output path
- Optional separators between sections

**Why This Matters**:
Artifacts are the core of multi-section document generation. Understanding artifact assembly lets you create complex documents from modular content pieces (e.g., README with 5 sections, API docs with multiple endpoints).

**Verification**:
```
"Use choracompose:list_artifact_configs to verify the artifact config was created"
```
Expected: New artifact config appears in list with correct members.

#### Step 2.2: Trace Artifact Dependencies

Before assembling an artifact, check what content dependencies are required.

**Action**:
In Claude Desktop:
```
"Use choracompose:trace_dependencies to check what content is needed for artifact 'complete-readme'"
```

**Expected Output**:
```json
{
  "success": true,
  "artifact_id": "complete-readme",
  "dependencies": {
    "required_content": ["readme-header", "readme-body", "readme-footer"],
    "optional_content": [],
    "missing": ["readme-body"]
  },
  "dependency_graph": "header → body → footer"
}
```

**Why This Matters**:
Prevents "missing_content" errors during artifact assembly. Shows you exactly what needs to be generated first.

**Verification**:
- All required content identified
- Missing content list shows what needs generation
- Dependency graph shows composition order

#### Step 2.3: Batch Generate Missing Content

Use batch_generate to create multiple content pieces in parallel (faster than sequential generation).

**Action**:
In Claude Desktop:
```
"Use choracompose:batch_generate to generate content for ['readme-header', 'readme-body', 'readme-footer'] with shared context {"project": "my-app", "version": "1.0"} and max_parallel=3"
```

**Expected Output**:
```json
{
  "success": true,
  "total": 3,
  "successful": 3,
  "failed": 0,
  "skipped": 0,
  "results": [
    {"content_id": "readme-header", "success": true, "status": "generated"},
    {"content_id": "readme-body", "success": true, "status": "generated"},
    {"content_id": "readme-footer", "success": true, "status": "generated"}
  ],
  "duration_ms": 234,
  "metadata": {"parallel_executions": 3}
}
```

**Why This Matters**:
Parallel execution achieves 2.6-4.8× speedup vs sequential generation. Essential for efficient bulk operations.

**Verification**:
- All 3 content pieces generated successfully
- Duration is significantly less than 3× single content generation time
- Parallel executions = 3 (confirms parallel processing)

#### Step 2.4: Assemble First Artifact

Combine generated content into a single artifact file.

**Action**:
In Claude Desktop:
```
"Use choracompose:assemble_artifact with artifact_config_id 'complete-readme' and output_path 'outputs/README.md'"
```

**Expected Output**:
```json
{
  "success": true,
  "artifact_id": "complete-readme",
  "output_path": "outputs/README.md",
  "content_count": 3,
  "size_bytes": 1542,
  "status": "assembled",
  "duration_ms": 123,
  "metadata": {
    "missing_content": [],
    "generated_content": ["readme-header", "readme-body", "readme-footer"],
    "composition_strategy": "concatenation"
  }
}
```

**Why This Matters**:
This is the core artifact assembly workflow. You've now generated a multi-section document from modular components.

**Verification**:
```bash
# Verify artifact file exists
ls -lh outputs/README.md

# Check contents
cat outputs/README.md
```
Expected: File contains all 3 sections concatenated with separators.

#### Step 2.5: Create Collection Config

Create a collection config to coordinate generation of multiple artifacts.

**Action**:
In Claude Desktop:
```
"Help me create a collection config that generates 3 artifacts (README, CHANGELOG, LICENSE) with shared context {"project": "my-app", "author": "Alice"} using MERGE propagation mode"
```

Claude will help create collection config with:
- Multiple artifact members
- Shared context (project-wide variables)
- Context propagation mode (MERGE to combine shared + member contexts)
- Execution strategy (parallel for speed)

**Why This Matters**:
Collections enable bulk generation with consistent context across all artifacts. Essential for documentation sets, multi-file projects.

**Verification**:
```
"Use choracompose:validate_collection_config to verify 'my-project-docs' collection config is valid"
```

#### Step 2.6: Generate Collection

Generate entire collection of artifacts in one command.

**Action**:
In Claude Desktop:
```
"Use choracompose:generate_collection with collection_config_id 'my-project-docs'"
```

**Expected Output**:
```json
{
  "success": true,
  "collection_id": "my-project-docs",
  "members_generated": 3,
  "total_artifacts": 3,
  "total_content": 9,
  "duration_ms": 1234,
  "execution_strategy": "parallel",
  "metadata": {
    "cache_hit_rate": 0.67,
    "parallel_workers": 3,
    "context_propagation_mode": "MERGE"
  }
}
```

**Why This Matters**:
Collection generation is the highest level of chora-compose orchestration. Generate entire documentation sets with one command.

**Verification**:
```bash
# Verify all artifacts generated
ls -lh outputs/
# Expected: README.md, CHANGELOG.md, LICENSE.md all present

# Check cache hit rate in response
# 67% cache hit rate means 6 of 9 content pieces were cached (reused from previous generations)
```

#### Step 2.7: Optimize Cache Hit Rate

Monitor and improve cache hit rates by managing context consistency.

**Action**:
1. Generate collection first time (low cache hit rate, ~10-30%)
2. Regenerate same collection (high cache hit rate, 90-100% expected)
3. Change shared context slightly and regenerate (partial cache hit, 50-70%)

In Claude Desktop:
```
"Generate collection 'my-project-docs' again without changing anything to see cache hit rate"
```

**Expected Behavior**:
- First generation: Low cache hit (10-30%) - most content is new
- Second generation: High cache hit (90-100%) - all content cached
- With context changes: Partial cache hit (depends on how many contexts changed)

**Why This Matters**:
Achieving 70-85% cache hit rates dramatically speeds up regeneration (4× faster). Understanding context consistency is key to cache optimization.

**Verification**:
- Check `cache_hit_rate` in response metadata
- Target: 70-85% for typical workflows with some context changes
- If < 50%: Review context structure for unnecessary variance

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] All Level 1 checks still pass
- [ ] Can create and save artifact configs (draft → test → save lifecycle)
- [ ] Can trace dependencies for artifacts (identifies missing content)
- [ ] Successfully used batch_generate with max_parallel for 3+ content pieces
- [ ] Assembled at least 1 artifact with 3+ content members
- [ ] Created and validated collection config with 3+ artifact members
- [ ] Successfully generated at least 1 collection (3+ artifacts)
- [ ] Achieving 70%+ cache hit rate on collection regeneration
- [ ] Understand MERGE context propagation (shared + member contexts combined)
- [ ] Understand difference between parallel and sequential execution strategies
- [ ] Can monitor cache hit rates in collection metadata

#### Validation Commands

```bash
# Primary validation
python scripts/sap-evaluator.py --quick SAP-018

# Expected output:
# ✅ SAP-018 (chora-compose-meta)
#    Level: 2
#    Next: Level 3
# ✅ Validation passed
```

### Common Issues (Level 2)

#### Issue 1: Artifact Assembly Fails with Missing Content

**Symptoms**:
- `assemble_artifact` returns `missing_content` error
- Metadata shows non-empty `missing_content` array
- Artifact file not generated

**Solution**:
1. Use `trace_dependencies` to identify all required content:
   ```
   "Use choracompose:trace_dependencies for artifact 'my-artifact'"
   ```
2. Check which content is missing from `dependencies.missing` array
3. Generate missing content with `batch_generate`:
   ```
   "Use batch_generate to generate ['missing-content-1', 'missing-content-2'] with appropriate context"
   ```
4. Retry artifact assembly

**Prevention**:
- Always run `trace_dependencies` before `assemble_artifact`
- Use batch_generate to pre-generate all dependencies
- Keep content configs organized and documented

#### Issue 2: Low Cache Hit Rate (< 50%)

**Symptoms**:
- Collection metadata shows `cache_hit_rate < 0.5`
- Regeneration takes almost as long as first generation
- Context appears similar but cache misses frequent

**Solution**:
1. Review context structure for unnecessary variance:
   - Remove timestamps, random IDs, or dynamic values from context
   - Use consistent formatting (e.g., always use ISO 8601 for dates)
   - Normalize data before passing to context (sort arrays, consistent key ordering)
2. Check if context includes large objects that change slightly:
   - Move large data to external_file context sources
   - Use data selectors (JSONPath) to extract only needed fields
3. Verify cache_key_fields in content configs:
   - Only include fields that actually affect output
   - Exclude fields used only for logging or metadata

**Prevention**:
- Design context schemas with caching in mind (stable, normalized data)
- Use external_file sources for large, frequently-changing data
- Monitor cache hit rates regularly (target 70-85%)

#### Issue 3: Collection Generation Times Out or Hangs

**Symptoms**:
- `generate_collection` doesn't complete within expected time
- No response or timeout error after several minutes
- Parallel execution seems stuck

**Solution**:
1. Check execution strategy:
   - If parallel with many members (10+), reduce max_workers to 4-6
   - Switch to sequential strategy temporarily to isolate issue
2. Check for circular dependencies:
   - Use `trace_dependencies` for each artifact member
   - Look for artifact A depending on artifact B depending on artifact A
3. Check individual artifact generation:
   - Test generating each artifact individually
   - Identify which specific artifact is causing delay
4. Review logs for errors:
   - Check `~/.chora-compose/logs/` for error details
   - Look for generator failures or API rate limits (for code_generation generator)

**Prevention**:
- Keep collections modular (< 20 artifacts per collection)
- Avoid circular dependencies in artifact configs
- Use sequential strategy for ordered dependencies

#### Issue 4: Context Propagation Not Working as Expected

**Symptoms**:
- Shared context variables not appearing in generated content
- MERGE mode seems to behave like ISOLATE
- Member-specific context overridden unexpectedly

**Solution**:
1. Verify context propagation mode in collection config:
   - MERGE: Combines shared + member contexts (most common)
   - OVERRIDE: Shared replaces member context (use cautiously)
   - ISOLATE: No propagation, member-only context
2. Check context merge strategy:
   - "deep" merge: Recursively merges nested objects
   - "shallow" merge: Only top-level keys merged
3. Debug context with preview:
   - Use `preview_generation` with expected merged context to test
   - Manually construct merged context to verify template behavior
4. Check for key conflicts:
   - If shared context has key "version" and member has "version", understand which wins based on merge strategy

**Prevention**:
- Document context propagation mode choice in collection config comments
- Use unique key names to avoid shared/member conflicts
- Test context propagation with simple examples before production use

---

## Level 3: Mastery Adoption

### Purpose

Level 3 adoption achieves:
- **Custom Generator Development**: Implementing BaseGenerator interface for domain-specific generation logic
- **Advanced Context Resolution**: Leveraging all 6 source types (inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output)
- **Freshness Validation**: Tracking stigmergic context links to detect stale collection members
- **Event Emission & Telemetry**: OpenTelemetry integration for observability (3 event types: content_generated, artifact_assembled, validation_completed)
- **Production Optimization**: Achieving 90-95% cache hit rates, fine-tuning parallel execution, minimizing context size
- **Schema Customization**: Extending JSON schemas for project-specific requirements

**This is the recommended production-ready configuration.**

### Time Estimate

- **Additional Setup**: 8-16 hours (beyond Level 2)
- **Learning Curve**: Steep - Requires Python development skills (for custom generators), understanding of chora-compose internals, production deployment experience

### Prerequisites

**From Level 2**:
- All Level 2 steps completed and validated
- Successfully generated multiple collections (5+)
- Achieving 70-85% cache hit rates consistently
- Comfortable with artifact/collection architecture

**Additional Requirements**:
- **Python development skills** (for custom generator development)
- **Understanding of SHA-256 caching mechanics** (how context hashing works)
- **Production deployment experience** (managing configs, monitoring, optimization)
- **Familiarity with OpenTelemetry** (optional, for event emission)
- **Understanding of JSON Schema** (for schema customization)

### Step-by-Step Instructions

#### Step 3.1: Study BaseGenerator Interface

Review the BaseGenerator interface in chora-compose source code to understand custom generator requirements.

**Action**:
1. Clone or access chora-compose repository:
   ```bash
   git clone https://github.com/chora-io/chora-compose
   cd chora-compose
   ```
2. Review BaseGenerator interface:
   ```bash
   cat src/generators/base.py
   ```
3. Study existing generator implementations (jinja2_generator.py, template_fill_generator.py) for patterns

**Why This Matters**:
Custom generators enable domain-specific generation logic beyond templates (e.g., API client generation, database schema generation, custom documentation formats).

**Verification**:
- Understand `generate()` method signature: `def generate(self, template: str, context: dict) -> str`
- Understand generator registration pattern (auto-discovery from `~/.chora-compose/generators/`)
- Identify generator options pattern (passed via config `generation.generator.options`)

#### Step 3.2: Develop Custom Generator

Implement a simple custom generator following BaseGenerator interface.

**Action**:
Create `~/.chora-compose/generators/my_custom_generator.py`:
```python
from chora_compose.generators.base import BaseGenerator

class MyCustomGenerator(BaseGenerator):
    def __init__(self, options=None):
        super().__init__(options or {})
        self.prefix = self.options.get('prefix', 'Generated:')

    def generate(self, template: str, context: dict) -> str:
        # Custom generation logic
        lines = [f"{self.prefix} Custom Output"]
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    @property
    def name(self) -> str:
        return "my_custom"

    @property
    def description(self) -> str:
        return "Custom generator for demonstration"
```

**Why This Matters**:
Demonstrates complete custom generator development cycle: interface implementation, registration, usage.

**Verification**:
```
"Use choracompose:list_generators to verify my_custom generator appears"
```
Expected: `my_custom` generator listed alongside builtin generators.

#### Step 3.3: Test Custom Generator

Create content config using your custom generator and test generation.

**Action**:
1. Create content config for custom generator:
   ```
   "Help me create content config 'test-custom' using generator 'my_custom' with options {"prefix": "Output:"}"
   ```
2. Generate content with custom generator:
   ```
   "Use choracompose:generate_content with content_config_id 'test-custom' and context {"user": "Alice", "project": "demo"}"
   ```

**Expected Output**:
```
Output: Custom Output
- user: Alice
- project: demo
```

**Why This Matters**:
Validates custom generator integration with chora-compose MCP tools and caching system.

**Verification**:
- Content generated successfully with custom generator
- Output matches custom generator logic
- Subsequent generation with same context hits cache (status: "skipped")

#### Step 3.4: Implement Freshness Tracking

Use check_freshness to validate collection members are up-to-date with source data.

**Action**:
1. Add freshness rules to collection config:
   - Track source file modification times
   - Set staleness threshold (e.g., 7 days)
2. Check freshness for collection member:
   ```
   "Use choracompose:check_freshness for content 'sap-capability-charter' with context {"sap_id": "SAP-018"}"
   ```

**Expected Output**:
```json
{
  "success": true,
  "is_fresh": false,
  "content_id": "sap-capability-charter",
  "last_generated": "2025-11-01T10:30:00Z",
  "context_changed": true,
  "stale_reason": "Context hash mismatch (expected: abc123, actual: def456)",
  "stigmergic_links": {
    "git_references": ["docs/sap-018/capability-charter.md"],
    "external_files": ["project-config.json"]
  }
}
```

**Why This Matters**:
Freshness validation enables incremental regeneration - only regenerate stale members, skip fresh ones. Critical for large collections (18 SAPs = 90 artifacts).

**Verification**:
- `is_fresh: false` when context changed
- `is_fresh: true` when regenerated with same context
- `stale_reason` explains why content is stale

#### Step 3.5: Configure Event Emission

Set up OpenTelemetry event emission for generation telemetry.

**Action**:
1. Set CHORA_TRACE_ID environment variable:
   ```bash
   export CHORA_TRACE_ID="trace-$(date +%s)"
   ```
2. Configure event output (JSON Lines format):
   ```bash
   export CHORA_EVENTS_OUTPUT="~/.chora-compose/logs/events.jsonl"
   ```
3. Generate content and check event emission:
   ```bash
   # Generate content
   # (via Claude Desktop MCP tools)

   # Check emitted events
   tail -f ~/.chora-compose/logs/events.jsonl
   ```

**Expected Output**:
```json
{"event_type": "content_generated", "content_id": "test-content", "timestamp": "2025-11-04T12:00:00Z", "trace_id": "trace-1730728800", "duration_ms": 87, "cache_hit": false}
{"event_type": "artifact_assembled", "artifact_id": "test-artifact", "timestamp": "2025-11-04T12:00:01Z", "trace_id": "trace-1730728800", "content_count": 3, "duration_ms": 234}
```

**Why This Matters**:
Event emission enables observability for production deployments: monitoring generation times, cache hit rates, error rates. Integrates with Prometheus, Grafana, etc.

**Verification**:
- Events appear in CHORA_EVENTS_OUTPUT file
- trace_id propagates across content → artifact → collection hierarchy
- Events include performance metrics (duration_ms, cache_hit)

#### Step 3.6: Optimize for Production (90-95% Cache Hit Rate)

Fine-tune cache policies and context management to achieve production-grade cache hit rates.

**Action**:
1. **Audit Context Schemas**:
   - Review all content configs for context.cache_key_fields
   - Remove unnecessary fields from cache key calculation
   - Normalize data formats (ISO 8601 dates, sorted arrays)

2. **Implement Context Normalization Layer**:
   ```python
   # Example: Normalize context before generation
   import json
   def normalize_context(ctx):
       # Sort dict keys
       normalized = {k: ctx[k] for k in sorted(ctx.keys())}
       # Normalize dates to ISO 8601
       if 'date' in normalized:
           normalized['date'] = datetime.fromisoformat(normalized['date']).isoformat()
       return normalized
   ```

3. **Monitor Cache Performance**:
   ```
   "Generate collection 'production-docs' and report cache_hit_rate from metadata"
   ```

4. **Iterate on Optimization**:
   - Target: 90-95% cache hit rate for production workflows
   - If < 90%: Review context variance, check for dynamic fields (timestamps, UUIDs)
   - Use external_file sources for large, infrequently-changing data

**Why This Matters**:
90-95% cache hit rate = 10-20× faster regeneration times. Critical for production workflows with frequent regeneration (CI/CD, documentation updates).

**Verification**:
- Collection metadata shows cache_hit_rate >= 0.90
- Regeneration time < 10% of initial generation time
- Consistent cache performance across multiple runs

#### Step 3.7: Implement Advanced Context Resolution

Leverage all 6 context source types for sophisticated context management.

**Action**:
Create content config using multiple context sources:
```json
{
  "inputs": {
    "sources": [
      {
        "type": "inline_data",
        "data": {"project": "chora-base"}
      },
      {
        "type": "external_file",
        "path": "project-config.json",
        "selector": "$.metadata",
        "required": true
      },
      {
        "type": "git_reference",
        "repo_path": ".",
        "reference": "HEAD",
        "file_path": "README.md",
        "selector": "$.version"
      },
      {
        "type": "content_config",
        "reference": "header-content",
        "output_as": "header_text"
      },
      {
        "type": "artifact_config",
        "reference": "project-metadata",
        "output_as": "metadata_artifact"
      },
      {
        "type": "ephemeral_output",
        "content_id": "generated-summary",
        "output_as": "summary"
      }
    ]
  }
}
```

**Why This Matters**:
Advanced context resolution enables sophisticated generation patterns: content depending on other content, artifact outputs as context, git-anchored data, external data sources.

**Verification**:
- All 6 source types resolve successfully
- Context merges correctly (deep merge strategy)
- Generated content reflects data from all sources

#### Step 3.8: Production Deployment Checklist

Finalize production-ready configuration and monitoring.

**Action**:
1. **Configuration Management**:
   - Version control all configs (content, artifact, collection)
   - Document config schemas and conventions
   - Implement config validation in CI/CD pipeline

2. **Monitoring & Alerting**:
   - Set up OpenTelemetry collector for event aggregation
   - Create dashboards for cache hit rates, generation times, error rates
   - Configure alerts for cache hit rate drops (< 80%), generation failures

3. **Performance Tuning**:
   - Optimize max_parallel for hardware (4-8 workers typical)
   - Tune ephemeral storage cleanup policies (keep_versions=3, keep_days=7)
   - Implement cache warming for cold starts

4. **Documentation**:
   - Document custom generators and their usage
   - Create runbooks for common operations (regeneration, cache cleanup, troubleshooting)
   - Train team on collections architecture and best practices

**Why This Matters**:
Production deployment requires operational readiness beyond just functional implementation. Monitoring, documentation, and team training ensure sustainable production usage.

**Verification**:
- All configs under version control
- Monitoring dashboards operational
- Team trained on chora-compose usage
- Runbooks documented and tested

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] All Level 1 and Level 2 checks still pass
- [ ] Developed and tested at least 1 custom generator (extends BaseGenerator)
- [ ] Custom generator auto-discovered and listed in `list_generators`
- [ ] Implemented freshness tracking with `check_freshness`
- [ ] Configured and tested event emission (OpenTelemetry)
- [ ] Achieving 90-95% cache hit rate in production workflows
- [ ] Implemented advanced context resolution (using 3+ source types)
- [ ] All configs under version control with documented schemas
- [ ] Monitoring dashboards operational (cache hit rates, generation times, errors)
- [ ] Team trained on collections architecture and custom generators
- [ ] Production runbooks documented and tested

#### Validation Commands

```bash
# Primary validation
python scripts/sap-evaluator.py --quick SAP-018

# Expected output:
# ✅ SAP-018 (chora-compose-meta)
#    Level: 3
#    Status: ✨ Optimized
# ✅ Validation passed

# Deep dive validation (recommended for Level 3)
python scripts/sap-evaluator.py --deep SAP-018
```

### Common Issues (Level 3)

#### Issue 1: Custom Generator Not Auto-Discovered

**Symptoms**:
- Custom generator file exists in `~/.chora-compose/generators/` but not listed in `list_generators`
- `generate_content` returns `generator_not_found` error when using custom generator
- MCP server doesn't recognize custom generator name

**Solution**:
1. Verify generator file location: `ls -la ~/.chora-compose/generators/`
2. Check generator class name matches file name pattern:
   - File: `my_custom_generator.py`
   - Class: `MyCustomGenerator` (PascalCase of filename)
3. Verify BaseGenerator imported and extended correctly
4. Check `name` property returns correct string (used for config reference)
5. Restart chora-compose MCP server (generators loaded at startup):
   - Restart Claude Desktop
   - Or restart MCP server process manually

**Prevention**:
- Follow naming conventions strictly (file name matches class name)
- Test generator immediately after creation
- Use existing generator files as templates

#### Issue 2: Freshness Tracking Reports False Staleness

**Symptoms**:
- `check_freshness` always returns `is_fresh: false` even after regeneration
- Staleness threshold seems not respected
- Context hash mismatch despite identical context

**Solution**:
1. Verify context normalization:
   - Check for dynamic fields (timestamps, UUIDs) in context
   - Ensure context serialization is deterministic (sorted keys)
2. Check stigmergic link tracking:
   - Verify git_reference sources point to correct paths
   - Ensure external_file sources exist and are accessible
3. Review freshness rules in collection config:
   - Staleness threshold should be reasonable (7+ days for documentation)
   - Cache manifest should be persisted correctly
4. Debug with manual hash calculation:
   ```python
   import hashlib, json
   context = {"key": "value"}
   hash_input = json.dumps(context, sort_keys=True)
   cache_key = hashlib.sha256(hash_input.encode()).hexdigest()
   # Compare with cache_key in check_freshness response
   ```

**Prevention**:
- Implement context normalization layer (Step 3.6)
- Avoid including volatile data in context (timestamps, random values)
- Test freshness tracking with simple, stable contexts first

#### Issue 3: Event Emission Not Working

**Symptoms**:
- CHORA_EVENTS_OUTPUT file empty or not created
- No events appearing in logs despite generation activity
- OpenTelemetry integration not working

**Solution**:
1. Verify environment variables set:
   ```bash
   echo $CHORA_TRACE_ID
   echo $CHORA_EVENTS_OUTPUT
   ```
2. Check file permissions for events output path:
   ```bash
   touch ~/.chora-compose/logs/events.jsonl
   chmod 644 ~/.chora-compose/logs/events.jsonl
   ```
3. Verify chora-compose version supports event emission (v1.5.0+)
4. Check event emission is enabled in chora-compose config:
   ```bash
   # Check if events feature flag enabled
   cat ~/.chora-compose/config.yaml | grep events
   ```
5. Test with simple generation and check logs immediately:
   ```bash
   # Generate content
   # Then immediately:
   cat ~/.chora-compose/logs/events.jsonl
   ```

**Prevention**:
- Set environment variables in shell profile (.bashrc, .zshrc) for persistence
- Create log directory upfront: `mkdir -p ~/.chora-compose/logs`
- Monitor event file during development (tail -f)

#### Issue 4: Production Cache Hit Rate Below Target (< 90%)

**Symptoms**:
- Collection metadata consistently shows cache_hit_rate < 0.90
- Regeneration times not significantly faster than initial generation
- Cache seems to miss frequently despite stable contexts

**Solution**:
1. **Profile Context Variance**:
   ```python
   # Log context hashes to identify variance
   import hashlib, json
   contexts = [ctx1, ctx2, ctx3]  # From multiple runs
   for i, ctx in enumerate(contexts):
       hash_val = hashlib.sha256(json.dumps(ctx, sort_keys=True).encode()).hexdigest()
       print(f"Run {i}: {hash_val}")
   # Look for hashes that should match but don't
   ```

2. **Audit cache_key_fields**:
   - Review each content config's `generation.patterns.cache_key_fields`
   - Remove fields not affecting output (logging metadata, timestamps)
   - Use only stable, business-relevant fields

3. **Implement Cache Warming**:
   - Pre-generate common contexts during deployment
   - Populate cache before production load
   ```
   "Generate collection 'production-docs' with canonical context to warm cache"
   ```

4. **Check Ephemeral Storage Cleanup**:
   - Ensure cleanup policies not too aggressive (keep_versions >= 3)
   - Verify cache manifest persisted correctly
   ```bash
   ls -lh ~/.chora-compose/cache/collections/*/manifest.json
   ```

**Prevention**:
- Design context schemas for caching from start (normalized, stable fields only)
- Implement automated cache hit rate monitoring with alerts (< 85% threshold)
- Regular cache performance reviews (monthly)

---

## Maintenance & Operations

### Regular Maintenance Tasks

**Daily/Per-Use**:
- **Cleanup Ephemeral Storage**: Use `choracompose:cleanup_ephemeral` with `keep_versions=3`, `keep_days=7` to prevent disk bloat
  ```
  "Use choracompose:cleanup_ephemeral to cleanup old content versions, keep last 3 versions and 7 days"
  ```
- **Monitor Generation Errors**: Check for failed generations in daily workflow, address issues immediately
- **Verify MCP Server Health**: Quick `hello_world` test at start of session

**Weekly**:
- **Review Cache Hit Rates**: Check collection metadata for cache_hit_rate trends
  - Target: Level 2 = 70-85%, Level 3 = 90-95%
  - Investigate if rates dropping below target
- **Validate Collection Freshness**: Run `check_freshness` on critical collections
  - Regenerate stale members as needed
- **Review Event Logs**: Check `~/.chora-compose/logs/events.jsonl` for patterns (errors, performance anomalies)

**Monthly**:
- **Update chora-compose Version**: Check for new releases, review changelog in ledger.md
  ```bash
  pip install --upgrade chora-compose  # or npm update -g chora-compose
  ```
- **Review and Update Configs**: Update content/artifact/collection configs based on usage patterns
- **Audit Custom Generators**: Review custom generator usage, update/deprecate unused generators
- **Performance Optimization**: Review cache policies, context schemas, parallel execution settings
- **Backup Configs**: Ensure all configs committed to version control

**Quarterly**:
- **SAP Adoption Level Review**: Use `python scripts/sap-evaluator.py --deep SAP-018` to assess adoption level
- **Schema Version Migration**: Check for new config schema versions (v3.2+), plan migration if needed
- **Team Training Review**: Assess team proficiency, provide additional training if needed
- **Documentation Updates**: Update runbooks, internal docs based on lessons learned

### Upgrade Path

**Upgrading to Next Level**:

**From Level 1 to Level 2**:
1. Complete all Level 1 validation checks
2. Work through Level 2 steps (artifact assembly, collections, batch generation)
3. Focus on: Creating artifact configs, using trace_dependencies, generating collections with MERGE propagation
4. Target: Achieve 70%+ cache hit rate on collection regeneration
5. Validate with `python scripts/sap-evaluator.py --quick SAP-018`
6. Expected time investment: 4-8 additional hours

**From Level 2 to Level 3**:
1. Complete all Level 2 validation checks
2. Work through Level 3 steps (custom generator, freshness tracking, event emission, production optimization)
3. Focus on: BaseGenerator implementation, advanced context resolution, achieving 90-95% cache hit rate
4. Implement: Custom generator, freshness validation, OpenTelemetry events, production monitoring
5. Validate with `python scripts/sap-evaluator.py --deep SAP-018`
6. Expected time investment: 8-16 additional hours

**Version Updates**:

When a new version of SAP-018 is released:
1. Review changelog in [ledger.md](./ledger.md)
2. Check for breaking changes in:
   - MCP tool signatures (parameter changes, new required fields)
   - JSON schema versions (content config v3.1 → v3.2+, collection config v1.0 → v1.1+)
   - Context resolution mechanics (new source types, changed precedence)
   - Generator interface changes (BaseGenerator updates)
3. Update configs for schema version compatibility
4. Test critical workflows (content generation, artifact assembly, collection generation)
5. Re-validate adoption level: `python scripts/sap-evaluator.py --quick SAP-018`
6. Update custom generators if BaseGenerator interface changed

When a new version of chora-compose is released:
1. Review chora-compose changelog and release notes
2. Test in non-production environment first
3. Update with package manager: `pip install --upgrade chora-compose` or `npm update -g chora-compose`
4. Restart MCP server (restart Claude Desktop)
5. Verify compatibility: `choracompose:hello_world` should return new version number
6. Re-test critical workflows before promoting to production

---

## Troubleshooting Guide

### Diagnostic Commands

```bash
# Check MCP server status and version
# Via Claude Desktop:
"Call choracompose:hello_world"
# Expected: success=true, version=1.5.0+

# List available generators (verify custom generators registered)
"Use choracompose:list_generators"
# Expected: All 5 builtin + custom generators

# List content configs (verify configs accessible)
"Use choracompose:list_content_configs"

# List artifact configs
"Use choracompose:list_artifact_configs"

# Check ephemeral storage
ls -lah ~/.chora-compose/ephemeral/content/
ls -lah ~/.chora-compose/cache/collections/

# Trace artifact dependencies (identify missing content)
"Use choracompose:trace_dependencies with artifact_config_id 'my-artifact'"

# Check collection cache status
"Use choracompose:check_collection_cache with collection_config_id 'my-collection'"

# Validate config before generation
"Use choracompose:validate_collection_config with collection_config_id 'my-collection'"

# Check freshness of content
"Use choracompose:check_freshness with content_config_id 'my-content' and context {}"

# Review event logs (if event emission configured)
tail -100 ~/.chora-compose/logs/events.jsonl

# Check chora-compose installation
pip show chora-compose  # For Python installation
npm list -g chora-compose  # For Node.js installation
```

### Getting Help

**Self-Service**:
1. **Review SAP-018 Documentation**:
   - [protocol-spec.md](./protocol-spec.md) - Complete MCP tool specifications, generator interfaces, architecture details
   - [awareness-guide.md](./awareness-guide.md) - Quick reference for AI agents (also useful for humans), common workflows
   - [capability-charter.md](./capability-charter.md) - Problem statement, solution overview, stakeholders
   - [ledger.md](./ledger.md) - Version history, known issues, adoption tracking
2. **Review chora-compose Official Docs**:
   - AGENTS.md in chora-compose repository (922 lines, MCP tool catalog)
   - collections-architecture.md (3-tier model deep dive)
   - tool-catalog.md (partial tool reference)
3. **Search Existing Issues**:
   - Check chora-compose GitHub Issues for similar problems
   - Review closed issues for solutions

**Community Support**:
- **GitHub Issues**: [chora-compose Issues](https://github.com/chora-io/chora-compose/issues) - Report bugs, request features
- **GitHub Discussions**: [chora-compose Discussions](https://github.com/chora-io/chora-compose/discussions) - Ask questions, share patterns
- **chora-base SAP Community**: For SAP-018 specific questions, file issues in chora-base repository

**Maintainer Contact**:
- **SAP-018 Owner**: Victor
- **Responsibility**: SAP-018 documentation maintenance, architecture evolution
- **Contact**: Via chora-workspace GitHub issues or chora-base project discussions
- **Response SLA**: 2-4 business days for questions, 24-48 hours for critical issues

---

## Success Metrics

### Level 1 Success

You've achieved Level 1 when:
- [ ] Can use 5+ core MCP tools confidently (generate_content, preview_generation, list_generators, list_content_configs, assemble_artifact)
- [ ] Generated 10+ content pieces successfully across different generators
- [ ] Understand 3-tier architecture (Content → Artifact → Collection)
- [ ] Understand SHA-256 caching mechanics (context hashing, cache hits/misses)
- [ ] Can complete basic workflows independently (content generation, preview, listing)
- [ ] Architecture understanding time: 2-4 hours (vs 10-20 hours without SAP-018)

### Level 2 Success

You've achieved Level 2 when:
- [ ] All Level 1 criteria met
- [ ] Assembled 5+ artifacts with 3+ content members each
- [ ] Generated 3+ collections with parallel execution
- [ ] Achieving 70-85% cache hit rate consistently
- [ ] Successfully using batch_generate for parallel content generation (3+ pieces)
- [ ] Understand context propagation modes (MERGE, OVERRIDE, ISOLATE)
- [ ] Can trace dependencies and resolve missing content proactively
- [ ] Regular usage in projects (weekly generation workflows)
- [ ] Implementation success rate: 90%+ of artifact/collection configs work on first attempt

### Level 3 Success

You've achieved Level 3 when:
- [ ] All Level 1 and Level 2 criteria met
- [ ] Developed 1+ custom generator extending BaseGenerator
- [ ] Custom generator in production use (generating content regularly)
- [ ] Implemented freshness tracking with check_freshness
- [ ] Configured event emission (OpenTelemetry) with monitoring dashboards
- [ ] Achieving 90-95% cache hit rate in production workflows
- [ ] Using 3+ context source types (inline_data, external_file, content_config, etc.)
- [ ] All configs under version control with documented schemas
- [ ] Team trained on collections architecture and custom generators
- [ ] Production deployment operational with monitoring and alerting
- [ ] Metrics improving monthly (cache hit rate trends upward, generation time decreasing)

---

## Additional Resources

### Learning Resources

**Recommended Reading Order**:
1. **[capability-charter.md](./capability-charter.md)** - Understand the problem (architecture knowledge gaps) and solution (comprehensive chora-compose Meta documentation)
   - Read time: 30-45 minutes
   - Focus: Problem statement, key capabilities, stakeholders, success criteria
2. **[awareness-guide.md](./awareness-guide.md)** - Quick reference for common tasks and workflows (primarily for AI agents but useful for humans)
   - Read time: 1-2 hours
   - Focus: Core concepts, decision trees, common workflows, error handling patterns
3. **This document (adoption-blueprint.md)** - Step-by-step adoption guide (you are here)
   - Complete time: 2-4 hours (Level 1) + 4-8 hours (Level 2) + 8-16 hours (Level 3)
   - Focus: Hands-on implementation, validation, troubleshooting
4. **[protocol-spec.md](./protocol-spec.md)** - Deep technical details (24 MCP tools, generator interfaces, JSON schemas)
   - Read time: 3-4 hours
   - Focus: API specifications, parameter types, return formats, error codes
   - Use as reference (don't read cover-to-cover initially)

### Related SAPs

**Dependencies** (install these first):
- **SAP-000 (SAP Framework)**: Core SAP protocols and documentation structure. SAP-018 follows SAP-000 conventions (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger).
  - Install first: SAP-000 provides foundational understanding of SAP structure
- **SAP-017 (chora-compose Integration)**: Installation guide and project integration workflows for chora-compose.
  - Install before SAP-018: Ensures chora-compose v1.5.0+ installed and MCP server configured
  - Provides: Step-by-step setup, Claude Desktop configuration, first-time onboarding

**Related Capabilities** (optional enhancements):
- **SAP-029 (Git-Anchored Content)** (future): Will extend chora-compose with enhanced git_reference context source type for version-controlled data
- **SAP-030 (Custom Generator Development Tutorials)** (future): Step-by-step tutorials for developing custom generators
- **SAP-031 (chora-compose Usage Patterns & Best Practices)** (future): Common generation patterns, template design, anti-patterns
- **SAP-032 (chora-compose Troubleshooting & Debugging)** (future): Diagnostic procedures, error catalog, performance profiling

### External Documentation

**chora-compose Official**:
- **[chora-compose GitHub Repository](https://github.com/chora-io/chora-compose)** - Source code, issues, discussions
- **[AGENTS.md](https://github.com/chora-io/chora-compose/blob/main/AGENTS.md)** - 922-line MCP tool catalog (official reference)
- **[collections-architecture.md](https://github.com/chora-io/chora-compose/blob/main/docs/collections-architecture.md)** - 3-tier model deep dive
- **[tool-catalog.md](https://github.com/chora-io/chora-compose/blob/main/docs/tool-catalog.md)** - Partial tool reference

**MCP Protocol**:
- **[Model Context Protocol Specification](https://modelcontextprotocol.io/)** - Official MCP protocol documentation
- **[MCP Tools Documentation](https://modelcontextprotocol.io/docs/concepts/tools)** - Understanding MCP tool interfaces

**Template Engines**:
- **[Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.1.x/)** - Template syntax, filters, macros (for jinja2 generator)
- **[Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)** - Practical template design guide

**JSON & Schemas**:
- **[JSON Schema Specification](https://json-schema.org/)** - Schema validation reference (for custom schema development)
- **[JSONPath Syntax](https://goessner.net/articles/JsonPath/)** - Data selectors for external_file context sources

**Observability**:
- **[OpenTelemetry Documentation](https://opentelemetry.io/docs/)** - Event emission, trace propagation (for Level 3)
- **[OpenTelemetry Events](https://opentelemetry.io/docs/concepts/events/)** - Event format specification

---

## Feedback

We value your feedback on this adoption blueprint! Your experience helps improve SAP-018 for future adopters.

**What worked well**:
- Share successes via GitHub Discussions in chora-base repository
- Document useful patterns you discovered
- Contribute example configs or custom generators

**What could be improved**:
- File issues in chora-base repository for:
  - Unclear instructions or missing steps
  - Inaccurate time estimates or difficulty ratings
  - Missing troubleshooting guidance
  - Outdated information (MCP tool changes, schema versions)

**Suggested changes**:
- Submit PRs to improve this blueprint:
  - Additional common issues and solutions
  - Better examples or clarifications
  - New validation checks or success criteria
- Propose new sections via GitHub Issues

**Feedback Priorities**:
1. **Critical errors** (instructions don't work): File issue immediately, include error details, environment (Python/Node version, chora-compose version, OS)
2. **Confusing instructions**: File issue with specific section, suggest clearer wording
3. **Missing content**: Identify gaps (e.g., missing Level 2 step, unclear prerequisite)
4. **Enhancement suggestions**: Propose additional resources, better examples, workflow optimizations

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
**Next Review**: 2026-02-04 (3 months from creation)
