# chora-compose Design RFC & Ecosystem Invitation

**Status**: Pre-Alpha | **Adopters**: 0 | **Version**: 2.0.1
**Date**: November 2025
**Purpose**: Invite ecosystem partners to help shape chora-compose's tool design

---

## Executive Summary

**chora-compose** is an MCP (Model Context Protocol) server providing AI-powered content generation capabilities with template-based composition, stigmergic coordination, and freshness management. We've built a functional system with 25 MCP tools (23 fully operational), but **we have zero adopters and are pre-alpha**.

This is your opportunity to help us design the tool interface **around your actual use cases**, not our assumptions.

**We're asking:**
- How might chora-compose fit into YOUR project's workflow?
- What use cases do you envision within YOUR domain?
- What would make these tools powerful and ergonomic for YOUR AI agents?

**We're offering:**
- A functional content generation system ready to be shaped by real needs
- Complete flexibility to redesign (pre-alpha = no backward compatibility constraints)
- Partnership in co-creating the right abstractions

---

## What is chora-compose?

### Core Value Proposition

chora-compose enables **AI-coordinated content generation** across multiple repositories through:

1. **Template-Based Generation**
   - Jinja2 templates with custom filters
   - LLM-powered generation (Claude Sonnet via structured prompts)
   - Code generation, BDD scenarios, documentation

2. **Stigmergic Coordination**
   - Indirect coordination through generated artifacts
   - Freshness policies (content age tracking)
   - Dependency tracing across composition layers

3. **Multi-Layer Composition**
   - **Layer 1: Configuration** - Define what to generate
   - **Layer 2: Generation** - Create content from templates
   - **Layer 3: Composition** - Assemble multi-part artifacts
   - **Layer 4: Collection** - Coordinate groups with freshness policies

4. **MCP Integration**
   - Native integration with Claude Desktop, Cline, and other MCP clients
   - 25 tools for discovery, generation, composition, and coordination
   - Server-Sent Events transport for real-time updates

### Key Capabilities

- ✅ **Generate content** from Jinja2 templates or LLM prompts
- ✅ **Track freshness** and regenerate stale content automatically
- ✅ **Compose artifacts** from multiple content pieces
- ✅ **Coordinate collections** with dependency tracking
- ✅ **Validate configurations** against JSON schemas
- ✅ **Cache generated content** with version history
- ✅ **Preview generation** without side effects (dry-run)

### Example Use Cases (Proven)

- **Documentation Generation**: Multi-file documentation suites with consistent formatting
- **Test Suite Generation**: BDD scenarios with Gherkin syntax
- **Configuration Templates**: Docker Compose files with environment-specific overrides
- **Project Scaffolding**: Boilerplate code from templates
- **Report Generation**: Status reports from structured data

---

## Current State: 25 MCP Tools

### Tool Categories

| Category | Tools | Status |
|----------|-------|--------|
| **Discovery** (9 tools) | `about`, `validate_setup`, `list_generators`, `list_content_configs`, `list_artifact_configs`, `list_content`, `list_artifacts`, `list_collection_members` | ✅ 9/9 functional |
| **Content Generation** (6 tools) | `generate_content`, `regenerate_content`, `delete_content`, `preview_generation`, `validate_content`, `batch_generate` | ✅ 6/6 functional |
| **Artifact Assembly** (3 tools) | `assemble_artifact`, `trace_dependencies`, `list_artifacts` | ✅ 3/3 functional |
| **Collection Management** (5 tools) | `generate_collection`, `validate_collection_config`, `check_collection_cache`, `check_freshness` | ⚠️ 4/5 functional (check_freshness has path resolution issue) |
| **Config Lifecycle** (4 tools) | `draft_config`, `test_config`, `save_config`, `modify_config` | ⚠️ 3/4 functional (modify_config needs better syntax) |
| **Cleanup** (1 tool) | `cleanup_ephemeral` | ✅ 1/1 functional |

**Overall: 23/25 tools fully functional** (2 have minor ergonomic issues)

---

## Ergonomic Analysis: What We've Learned

### Finding 1: Verb Inconsistency (High Impact)

**Problem**: 15 of 25 tools use domain-specific verbs instead of universal verbs.

| Domain Verb | CRUD Equivalent | Example |
|-------------|-----------------|---------|
| `generate_content` | CREATE | `create_content` |
| `regenerate_content` | UPDATE | `update_content` |
| `assemble_artifact` | CREATE | `create_artifact` |
| `trace_dependencies` | READ | `read_dependencies` |
| `check_freshness` | READ | `read_freshness` |
| `draft_config` | CREATE | `create_draft` |
| `save_config` | UPDATE | `persist_draft` |
| `modify_config` | UPDATE | `update_draft` |

**Impact**: AI agents must learn 15+ verbs (generate, regenerate, assemble, trace, check, draft, save, modify...) instead of 4 (CREATE, READ, UPDATE, DELETE).

**Question for partners**: Do you prefer:
- **Domain verbs** (`generate`, `assemble`, `trace`) - more expressive but more to learn?
- **Universal verbs** (`create`, `read`, `update`) - less expressive but predictable?
- **Something else** entirely?

### Finding 2: Parameter Naming Inconsistency (Critical)

**Problem**: Same concept has 6 different parameter names across tools.

| Concept | Parameter Names Used | Tools |
|---------|---------------------|-------|
| Config ID | `content_config_id`, `artifact_config_id`, `collection_config_path`, `content_or_config_id`, `draft_id`, `config_id` | 15 tools |
| Context Variables | `context`, `shared_context`, `individual_contexts` | 6 tools |
| Force Regeneration | `force`, `force_members` | 8 tools |

**Example confusion**:
```python
generate_content(content_config_id="abc")     # uses "_config_id"
assemble_artifact(artifact_config_id="def")   # uses "_config_id"
generate_collection(collection_config_path="ghi.json")  # uses "_config_path"!
validate_content(content_or_config_id="jkl")  # uses ambiguous "_or_config_id"
```

**Impact**: AI agents must guess which parameter name to use.

**Question for partners**: Should we standardize on:
- Short IDs: `content_id`, `artifact_id`, `collection_id`?
- Explicit paths: `content_config_path`, `artifact_config_path`?
- Flexible: `id_or_path` that accepts both?

### Finding 3: Semantic Overlap (Blocking)

**Problem**: `save_config` and `modify_config` both UPDATE but have different semantics.

- `save_config(draft_id, config_id)` - Persists draft to filesystem
- `modify_config(config_id, updates)` - Modifies draft OR persisted config (but only drafts implemented!)

**Impact**: Confusing workflow. AI agents don't know which to use when.

**Question for partners**: Should config management be:
- **CRUD-style**: `create_config`, `read_config`, `update_config`, `delete_config`?
- **Workflow-style**: `create_draft` → `preview_draft` → `update_draft` → `persist_draft`?
- **Something else**?

### Finding 4: Tool Count (25 tools = High Cognitive Load)

**Question**: Is 25 tools too many, or is granularity good?

**Alternative approaches**:
1. **Consolidate to ~5 high-level workflows** (create, refresh, inspect, configure, discover)
2. **Keep granular tools** (25 atomic operations, agent chains them)
3. **Hybrid approach** (10-12 tools, medium granularity)

---

## Design Options Under Consideration

We're presenting 3 design directions. **We want YOUR input** on which would best serve your use cases.

### Option A: Layer-Oriented Design (12 tools)

**Philosophy**: Match the 4-layer architecture explicitly.

| Layer | Tools | Purpose |
|-------|-------|---------|
| **Layer 1: Configuration** | `configure`, `list_configs`, `preview_config` | Manage configurations |
| **Layer 2: Generation** | `generate`, `preview_generation`, `delete_generated` | Create content |
| **Layer 3: Composition** | `compose`, `trace_composition` | Assemble artifacts |
| **Layer 4: Collection** | `coordinate`, `inspect_collection` | Manage collections |
| **Meta** | `about`, `discover` | Discovery |

**Total: 12 tools** (down from 25)

**Pros**:
- Tools match conceptual model (layers)
- Clear separation of concerns
- Still relatively granular

**Cons**:
- Requires understanding the 4-layer model
- May still have parameter consistency issues

**Best for**: Partners who think in architectural layers.

---

### Option B: Workflow-Oriented Design (5 tools)

**Philosophy**: Match AI agent goals, not system architecture.

| Tool | Purpose | What It Does |
|------|---------|--------------|
| `create` | Create new content/artifact/collection | Auto-detects type from config, orchestrates entire pipeline, handles dependencies |
| `refresh` | Update stale content | Checks freshness policies, regenerates only what's needed |
| `inspect` | Read status/content | Works on content/artifacts/collections, returns metadata + freshness + content |
| `configure` | Manage configurations | CRUD operations for configs, supports draft → test → save workflow |
| `discover` | List available resources | Single discovery tool with filters (configs, generators, content, artifacts) |

**Total: 5 tools** (down from 25!)

**Example usage**:
```python
# Agent: "Create documentation suite"
create(config_id="user-docs")  # Detects collection, generates all members, assembles artifacts

# Agent: "Is documentation fresh?"
inspect(id="user-docs")  # Returns freshness status for all members

# Agent: "Refresh stale content"
refresh(id="user-docs")  # Regenerates only stale content
```

**Contrast with current (requires 6+ tool calls)**:
```python
list_collection_members(collection_config_path="user-docs.json")
batch_generate(content_ids=[...], ...)
validate_content(content_id=...)
assemble_artifact(artifact_config_id=...)
generate_collection(collection_config_path="user-docs.json")
check_freshness(collection_config_path="user-docs.json")
```

**Pros**:
- Minimal cognitive load (5 tools, not 25)
- Idempotent (safe to retry)
- Handles complexity internally
- Tools match agent thinking ("create", "refresh", "inspect")

**Cons**:
- Less granular control
- Tools are more "magical" (hide orchestration)
- May not expose all capabilities

**Best for**: Partners who want simple, high-level interfaces. AI agents who think in workflows.

---

### Option C: Resource-Oriented Design (20 tools)

**Philosophy**: REST-like, consistent operations per resource.

| Resource | Operations | Purpose |
|----------|-----------|---------|
| `content.*` | create, read, update, delete, list | Manage content instances |
| `artifact.*` | create, read, update, delete, list | Manage artifacts |
| `collection.*` | create, read, update, delete, list | Manage collections |
| `config.*` | create, read, update, delete, list | Manage configurations |
| `generator.*` | read, list | Discover generators (read-only) |

**Example**:
```python
content.create(content_id, context)
content.read(content_id)
content.update(content_id, context, reason)
content.delete(content_id)
content.list(filter)

artifact.create(artifact_id, context)
artifact.read(artifact_id)
artifact.update(artifact_id, force_members)
artifact.delete(artifact_id)
artifact.list(filter)
```

**Total: ~20 tools** (5 resources × 4 operations, plus discovery)

**Pros**:
- Predictable patterns (if you know `content.*`, you know `artifact.*`)
- RESTful consistency
- Clear resource boundaries

**Cons**:
- Still ~20 tools (moderate cognitive load)
- Requires understanding resource types
- May need chaining for complex workflows

**Best for**: Partners familiar with REST APIs, who value consistency over minimalism.

---

## Use Case Examples by Domain

### Use Case 1: Multi-Repo Documentation (GitHub Actions Team)

**Scenario**: You maintain 50 action repos, each needs consistent README, API docs, changelog.

**With chora-compose**:
```yaml
# config: docs-suite.json
{
  "type": "collection",
  "id": "github-actions-docs",
  "members": [
    {"content_id": "readme", "template": "templates/readme.md.j2"},
    {"content_id": "api-docs", "template": "templates/api-reference.md.j2"},
    {"content_id": "changelog", "generator": "structured_generation"}
  ],
  "freshness": {
    "policy": "time_based",
    "max_age_days": 30
  }
}
```

**AI Agent workflow**:
```
Option B (5 tools):
  1. create(config_id="github-actions-docs") → Generates all docs
  2. refresh(id="github-actions-docs") → Regenerates stale docs monthly

Option C (20 tools):
  1. collection.create(id="github-actions-docs") → Same result
  2. collection.update(id="github-actions-docs", refresh_stale_only=true)
```

**Questions for you**:
- How often do docs become stale? (freshness policy)
- Do different repos need different templates? (context overrides)
- Do you want granular control or automated coordination?

---

### Use Case 2: Test Suite Generation (Testing Framework Team)

**Scenario**: Generate BDD scenarios from API specifications.

**With chora-compose**:
```yaml
# config: api-tests.json
{
  "type": "content",
  "id": "user-api-tests",
  "generation": {
    "patterns": [{
      "type": "bdd_scenario_assembly",
      "template": "templates/bdd-scenario.feature.j2"
    }]
  },
  "context_sources": ["openapi-spec.yaml"]
}
```

**AI Agent workflow**:
```
Option B (5 tools):
  1. create(config_id="user-api-tests", context={"api_version": "v2"})
  2. inspect(id="user-api-tests") → Check generated scenarios
  3. refresh(id="user-api-tests", reason="API spec updated")

Option A (12 tools):
  1. generate(content_id="user-api-tests", context={...})
  2. preview_generation(content_id="user-api-tests") → Dry-run
  3. generate(content_id="user-api-tests", force=true) → Regenerate
```

**Questions for you**:
- Do you need preview before generation? (dry-run important?)
- How do you track API spec changes? (freshness trigger)
- Do you generate tests for multiple APIs? (batch operations)

---

### Use Case 3: Docker Compose Configuration (Infrastructure Team)

**Scenario**: Generate environment-specific docker-compose files from base templates.

**With chora-compose**:
```yaml
# config: docker-compose-prod.json
{
  "type": "content",
  "id": "docker-compose-production",
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "templates/docker-compose.yml.j2"
    }]
  },
  "context": {
    "environment": "production",
    "replicas": 5,
    "resources": {"memory": "4GB"}
  }
}
```

**AI Agent workflow**:
```
Option B (5 tools):
  1. configure(operation="create", config_type="content", data={...})
  2. create(config_id="docker-compose-production")
  3. inspect(id="docker-compose-production", include_content=true)

Option C (20 tools):
  1. config.create(type="content", data={...})
  2. content.create(content_id="docker-compose-production")
  3. content.read(content_id="docker-compose-production")
```

**Questions for you**:
- Do you need version history? (rollback to previous configs)
- Do you validate before deploying? (preview + validate workflow)
- How many environments? (dev, staging, prod → context overrides)

---

### Use Case 4: Status Report Generation (Project Management Team)

**Scenario**: Weekly status reports aggregating data from Jira, GitHub, Slack.

**With chora-compose**:
```yaml
# config: weekly-status.json
{
  "type": "artifact",
  "id": "weekly-status-report",
  "content": {
    "children": [
      {"content_id": "jira-summary"},
      {"content_id": "github-prs"},
      {"content_id": "slack-highlights"}
    ]
  },
  "composition": {
    "strategy": "concatenate",
    "template": "templates/status-report.md.j2"
  }
}
```

**AI Agent workflow**:
```
Option B (5 tools):
  1. create(config_id="weekly-status-report")
     → Generates all 3 content pieces + assembles artifact
  2. refresh(id="weekly-status-report") → Next week's report

Option A (12 tools):
  1. generate(content_id="jira-summary")
  2. generate(content_id="github-prs")
  3. generate(content_id="slack-highlights")
  4. compose(artifact_id="weekly-status-report")
```

**Questions for you**:
- Do you need individual content pieces accessible? (granular control)
- Is report composition always the same? (or dynamic based on data)
- How do you handle missing data? (error handling preferences)

---

### Use Case 5: Code Scaffolding (Framework Team)

**Scenario**: Generate project boilerplate from templates.

**With chora-compose**:
```yaml
# config: react-app-scaffold.json
{
  "type": "collection",
  "id": "react-app-scaffold",
  "members": [
    {"content_id": "package-json", "template": "templates/package.json.j2"},
    {"content_id": "tsconfig", "template": "templates/tsconfig.json.j2"},
    {"content_id": "app-component", "generator": "code_generation"}
  ]
}
```

**AI Agent workflow**:
```
Option B (5 tools):
  1. configure(operation="create", ...) → Define scaffold config
  2. create(config_id="react-app-scaffold", context={"app_name": "my-app"})

Option C (20 tools):
  1. config.create(type="collection", data={...})
  2. collection.create(id="react-app-scaffold", context={...})
```

**Questions for you**:
- Do you scaffold once or repeatedly? (one-time vs iterative)
- Do you need conditional file generation? (optional files based on context)
- How do you handle file conflicts? (overwrite policies)

---

## Call for Collaboration

### We Need Your Input

**We're pre-alpha with zero adopters** - this is the BEST time to shape the design around real needs.

**What would help us**:

1. **Your use case**: What would you use chora-compose for in YOUR project?
2. **Your workflow**: How do you think about content generation? (layers, workflows, resources?)
3. **Your preferences**: Which design option resonates with you? (A, B, C, or something else?)
4. **Your constraints**: What would make adoption easier? (naming conventions, parameter patterns, error messages?)
5. **Your pain points**: What's missing from existing tools that chora-compose could solve?

### How to Engage

#### Option 1: GitHub Issues
Create an issue in [chora-compose repo](https://github.com/your-org/chora-compose/issues) with:
- **Title**: `[Use Case] Your project name - Your domain`
- **Body**: Describe your use case, preferred design, questions

#### Option 2: Coordination Request
Submit a coordination request via the inbox system:
```json
{
  "trace_id": "CHORA-COORD-2025-XXX",
  "type": "design_input",
  "from": "your-repo-name",
  "subject": "chora-compose use case: [your domain]",
  "body": {
    "use_case": "...",
    "preferred_design": "Option B",
    "questions": ["..."]
  }
}
```

#### Option 3: Direct Collaboration
Propose joint development:
- **Pair on a prototype**: We implement your use case together
- **Co-design the interface**: Weekly sync to shape the tools
- **Dogfooding partnership**: You use pre-alpha, we iterate based on feedback

### What We'll Do With Your Input

1. **Synthesize use cases**: Identify common patterns across partners
2. **Prototype top options**: Implement the most-requested design
3. **Share early access**: Get your feedback on prototypes
4. **Co-design iteration**: Refine based on real usage
5. **Document patterns**: Capture learnings for ecosystem

---

## Technical Appendix

### Complete Tool Catalog (Current v2.0.1)

#### Discovery Tools (9 tools)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `about` | none | Server metadata, capabilities, 25 tools | ✅ |
| `validate_setup` | none | Environment validation, schema checks | ✅ |
| `list_generators` | `generator_type`, `include_plugins` | Generator list (jinja2, demonstration, etc.) | ✅ |
| `list_content_configs` | `filter_pattern` | Content config summaries | ✅ |
| `list_artifact_configs` | `filter_pattern` | Artifact config summaries | ✅ |
| `list_content` | `filter`, `sort`, `limit` | Generated content list | ✅ |
| `list_artifacts` | `filter`, `sort`, `limit` | Assembled artifacts list | ✅ |
| `list_collection_members` | `collection_config_path`, `expand_nested`, `max_depth` | Collection member tree | ✅ |

#### Content Generation Tools (6 tools)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `generate_content` | `content_config_id`, `context`, `force` | Generated content + metadata | ✅ |
| `regenerate_content` | `content_config_id`, `context`, `reason`, `compare` | Regenerated content + diff | ✅ |
| `delete_content` | `content_id`, `preserve_metadata`, `force` | Deletion status | ✅ |
| `preview_generation` | `content_config_id`, `context`, `show_metadata` | Preview (dry-run) | ✅ |
| `validate_content` | `content_or_config_id`, `validation_rules` | Validation result | ✅ |
| `batch_generate` | `content_ids`, `shared_context`, `individual_contexts`, `force`, `continue_on_error`, `max_parallel` | Batch results | ✅ |

#### Artifact Assembly Tools (3 tools)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `assemble_artifact` | `artifact_config_id`, `output_path`, `force`, `context` | Assembled artifact path | ✅ |
| `trace_dependencies` | `artifact_config_id`, `check_status`, `show_metadata` | Dependency tree + status | ✅ |

#### Collection Management Tools (5 tools)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `generate_collection` | `collection_config_path`, `force`, `force_members`, `output_path` | Collection manifest | ✅ |
| `validate_collection_config` | `collection_config_path`, `check_member_configs` | Validation result | ✅ |
| `check_collection_cache` | `collection_config_path`, `output_path` | Cache status | ✅ |
| `check_freshness` | `collection_config_path`, `output_path` | Freshness status | ⚠️ Path resolution issue |

#### Config Lifecycle Tools (4 tools)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `draft_config` | `config_type`, `config_data`, `description` | Draft ID | ✅ |
| `test_config` | `draft_id`, `context`, `dry_run` | Preview result | ✅ |
| `save_config` | `draft_id`, `config_id`, `overwrite` | Saved config path | ✅ |
| `modify_config` | `config_id`, `updates`, `create_backup` | Modified config | ⚠️ Needs JSON path syntax |

#### Cleanup Tools (1 tool)

| Tool | Parameters | Returns | Status |
|------|-----------|---------|--------|
| `cleanup_ephemeral` | `retention`, `filter`, `dry_run` | Cleanup report | ✅ |

### Parameter Naming Patterns (Current)

| Concept | Variations Found | Count | Tools Affected |
|---------|-----------------|-------|----------------|
| Config ID | `content_config_id`, `artifact_config_id`, `collection_config_path`, `content_or_config_id`, `draft_id`, `config_id` | 6 | 15 tools |
| Context | `context`, `shared_context`, `individual_contexts` | 3 | 6 tools |
| Force | `force` (bool), `force_members` (list) | 2 | 8 tools |
| Output Path | `output_path` (optional in some, required in others) | 1 | 4 tools |

### Error Message Quality (Scored 1-5)

| Tool | Score | Strengths | Needs Improvement |
|------|-------|-----------|-------------------|
| `assemble_artifact` | 5/5 | Counts problems, lists missing items, suggests exact tool calls | None |
| `trace_dependencies` | 5/5 | Shows dependency tree, highlights issues, batch_generate hint | None |
| `generate_content` | 4/5 | Good path hints, clear error codes | Could suggest fixes for missing configs |
| `validate_content` | 2/5 | Basic error reporting | Raw Pydantic errors, no actionable suggestions |
| `draft_config` | 3/5 | Shows config type | No parsing of validation errors |

**Pattern to replicate** (from `assemble_artifact`):
```json
{
  "error": {
    "code": "content_missing",
    "message": "Cannot assemble artifact: 5 content pieces not generated yet",
    "details": {
      "missing_content": ["intro", "body", "conclusion", "references", "appendix"],
      "available_content": ["title", "abstract"],
      "suggestion": "Generate missing content first:\n" +
                   "  choracompose:generate_content(content_config_id='intro')\n" +
                   "  choracompose:generate_content(content_config_id='body')\n" +
                   "  ...\n" +
                   "Or use: choracompose:batch_generate(content_ids=['intro', 'body', ...])"
    }
  }
}
```

### Return Value Structure (Consistent Across All Tools)

All tools follow this Pydantic-based structure:

```python
class ToolResult(BaseModel):
    success: bool                    # Always present
    <domain_specific_fields>: ...    # Tool-specific data
    duration_ms: int                 # Execution timing
    metadata: dict | None = None     # Optional extra context
```

**Examples**:
```python
# generate_content result
{
  "success": true,
  "content_id": "intro",
  "file_path": "content/intro.md",
  "generator_type": "jinja2",
  "status": "generated",
  "cache_hit": false,
  "content_preview": "# Introduction\n\n...",
  "duration_ms": 234,
  "metadata": {
    "template": "templates/intro.md.j2",
    "context_vars": ["project_name", "version"]
  }
}

# assemble_artifact result
{
  "success": true,
  "artifact_id": "user-guide",
  "output_path": "artifacts/user-guide.pdf",
  "component_count": 7,
  "status": "assembled",
  "duration_ms": 1523,
  "metadata": {
    "dependencies": ["intro", "getting-started", "api-reference", ...],
    "composition_strategy": "concatenate"
  }
}
```

**This consistency is EXCELLENT** - we plan to keep it across all design options.

---

## Conclusion: Your Voice Matters

chora-compose has powerful capabilities, but **we don't know yet what the right interface is** because we don't have real adopters.

**This is your opportunity to shape a tool around YOUR needs**, not our assumptions.

Whether you prefer:
- **5 high-level workflow tools** (minimal, opinionated)
- **12 layer-oriented tools** (architectural clarity)
- **20 resource-oriented tools** (REST-like consistency)
- **Something completely different**

...we want to hear from you.

**The best design is the one that fits real use cases.** Tell us yours.

---

**Contact**:
- GitHub: [chora-compose issues](https://github.com/your-org/chora-compose/issues)
- Coordination: Submit RFC via inbox system
- Direct: Propose joint development session

**Status**: Pre-Alpha, v2.0.1, November 2025
**Adopters**: 0 (waiting for YOU!)
**Next Steps**: Your input → Design synthesis → Prototype → Iterate

Let's build this together.
