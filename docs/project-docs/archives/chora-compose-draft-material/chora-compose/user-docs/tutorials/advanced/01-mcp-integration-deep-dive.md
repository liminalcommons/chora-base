# Tutorial: MCP Integration Deep Dive

**Learning Goals:**
- Master all 13 MCP tools for comprehensive AI-powered workflows
- Use capability discovery for agent self-configuration
- Implement batch operations for performance optimization
- Manage ephemeral storage and config lifecycle
- Build end-to-end documentation generation pipelines

**Prerequisites:**
- Completed [Tutorial: Conversational Config Creation](../intermediate/02-conversational-config-creation.md)
- Claude Desktop with Chora Compose MCP integration configured
- Understanding of content and artifact configs
- 60-90 minutes of time

**Difficulty:** Advanced

**Version:** v1.2.0+

---

## What You'll Build

By the end of this tutorial, you'll have:

1. **Discovered server capabilities** dynamically (no hardcoded knowledge)
2. **Created configs conversationally** using the full lifecycle workflow
3. **Generated content in batches** with 3-5× performance improvement
4. **Managed ephemeral storage** with retention policies
5. **Built a complete documentation pipeline** from scratch

**Real-world outcome:** End-to-end automated documentation system using all 17 MCP tools.

---

## Part 1: MCP Fundamentals & Capability Discovery (15 min)

### Understanding the 13 MCP Tools

Chora Compose v1.2.0 provides **13 tools + 5 resources** for comprehensive integration:

**Tool Categories:**

```
Core Generation Tools (5):
├─ generate_content      - Generate single content piece
├─ assemble_artifact     - Combine content into artifacts
├─ regenerate_content    - Force regeneration (bypass cache)
├─ preview_generation    - Preview without persistence
└─ batch_generate        - Parallel content generation

Config Lifecycle Tools (4):
├─ draft_config          - Create temporary draft configs
├─ test_config           - Preview draft output
├─ modify_config         - Update draft incrementally
└─ save_config           - Persist draft to filesystem

Discovery Tools (4):
├─ list_generators       - Query available generators
├─ list_content_configs  - Browse content configurations
├─ list_artifact_configs - Browse artifact configurations
└─ list_artifacts        - List generated artifacts

Storage Management Tools (3):
├─ cleanup_ephemeral     - Clean up expired drafts/outputs
├─ delete_content        - Remove specific generated content
└─ trace_dependencies    - Analyze artifact dependencies

Validation Tools (1):
└─ validate_content      - Validate generated content
```

**Resources (5):**
```
capabilities://server      - Server metadata, features, limits
capabilities://tools       - Tool inventory with schemas
capabilities://resources   - Resource URI catalog
capabilities://generators  - Generator registry
(plus legacy: config://, schema://, content://, generator://)
```

---

### Step 1: Discover Server Capabilities

**Goal:** Learn what's available without hardcoded knowledge.

Open Claude Desktop and start:

```
You: Query the chora-compose server capabilities to see what version and features are available
```

**What Claude Does:**

Fetches `capabilities://server` resource:

```json
{
  "server_name": "chora-compose",
  "server_version": "1.1.0",
  "protocol_version": "1.0",
  "features": {
    "conversational_workflow_authoring": true,
    "batch_generation": true,
    "capability_discovery": true,
    "plugin_generators": true
  },
  "limits": {
    "max_batch_size": 10,
    "draft_retention_days": 30,
    "max_content_size_mb": 100
  }
}
```

**Expected Response:**

```
Claude: The chora-compose server is running version 1.1.0 with these capabilities:

✅ Conversational workflow authoring (draft → test → save)
✅ Batch generation (up to 10 items in parallel)
✅ Capability discovery (dynamic introspection)
✅ Plugin generators (extensible generator system)

Limits:
- Max batch size: 10 items
- Draft retention: 30 days
- Max content size: 100 MB

Would you like to explore the available tools or generators?
```

**What You Learned:**
- Server is v1.2.0 (has all latest features)
- Conversational workflow is supported
- Batch operations limited to 10 items
- Drafts expire after 30 days

---

### Step 2: Discover Available Tools

```
You: Show me all available MCP tools organized by category
```

**What Claude Does:**

Fetches `capabilities://tools` resource, which returns complete tool inventory.

**Expected Response:**

```
Claude: Here are all 17 available tools:

**Core Generation (5 tools):**
1. generate_content - Generate single content piece
2. assemble_artifact - Combine content into artifacts
3. regenerate_content - Force regeneration bypassing cache
4. preview_generation - Preview without persistence
5. batch_generate - Parallel content generation

**Config Lifecycle (4 tools):**
6. draft_config - Create temporary draft configs
7. test_config - Preview draft output
8. modify_config - Update draft incrementally
9. save_config - Persist draft to filesystem

**Discovery (4 tools):**
10. list_generators - Query available generators
11. list_content_configs - Browse content configurations
12. list_artifact_configs - Browse artifact configurations
13. list_artifacts - List generated artifacts

**Storage Management (3 tools):**
14. cleanup_ephemeral - Clean up expired drafts/outputs
15. delete_content - Remove specific generated content
16. trace_dependencies - Analyze artifact dependencies

**Validation (1 tool):**
17. validate_content - Validate generated content

Which category would you like to explore?
```

**What You Learned:**
- No hardcoded knowledge needed - agent discovered tools dynamically
- Tools are organized into logical categories
- Each tool has a clear purpose

---

### Step 3: Discover Available Generators

```
You: What content generators are available? Show their capabilities and requirements
```

**What Claude Does:**

Fetches `capabilities://generators` resource.

**Expected Response:**

```
Claude: Available generators (2 built-in + any plugins):

**1. jinja2**
- Type: Template-based generation
- Capabilities:
  - Dynamic content with variables
  - Template inheritance
  - Filters and functions
  - Complex logic (loops, conditionals)
- Requirements:
  - Template file (*.jinja, *.jinja2, *.j2)
  - Context data (optional)
- Best for: Complex, data-driven documents

**2. demonstration**
- Type: Example-based generation
- Capabilities:
  - Static content from example
  - Simple placeholders
  - Fast, no templating engine
- Requirements:
  - example_output field in config
- Best for: Static documents, quick prototypes

**Selection Guidance:**
- Use jinja2 when: Dynamic data, complex formatting, reusable templates
- Use demonstration when: Simple static content, rapid prototyping

Would you like to create a config using one of these generators?
```

**What You Learned:**
- 2 built-in generators available
- Each has different capabilities and requirements
- Selection guidance helps choose the right one

---

## Part 2: Complete Config Lifecycle Workflow (20 min)

**Scenario:** Create a monthly sales report config using the full draft → test → modify → save cycle.

### Step 1: Draft Initial Config

```
You: Create a content config for monthly sales reports that:
- Uses jinja2 generator
- Includes sections for: revenue, top customers, regional breakdown
- Accepts month and year as context variables
```

**What Claude Does:**

Calls `draft_config`:

```json
{
  "config_type": "content",
  "config_data": {
    "id": "monthly-sales-report",
    "generation": {
      "patterns": [{
        "type": "jinja2",
        "template": "sales-report.md.jinja",
        "generation_config": {
          "context": {
            "month": "{{ month }}",
            "year": "{{ year }}",
            "revenue": "{{ revenue }}",
            "top_customers": "{{ top_customers }}",
            "regional_breakdown": "{{ regional_breakdown }}"
          }
        }
      }]
    }
  },
  "description": "Monthly sales report with revenue, customers, and regions"
}
```

**Expected Response:**

```
Claude: ✅ Draft created: draft-20251016T201530-abc123

Configuration:
- Type: content
- Generator: jinja2
- Template: sales-report.md.jinja
- Validation: ✅ Valid (JSON Schema v3.1)
- Expires: November 15, 2025

The config expects these context variables:
- month (e.g., "October")
- year (e.g., "2025")
- revenue (sales data)
- top_customers (list)
- regional_breakdown (data by region)

Would you like to test this draft with sample data?
```

---

### Step 2: Test Draft with Sample Data

```
You: Test it with sample October 2025 data:
- Revenue: $450,000
- Top customers: ["Acme Corp", "TechStart Inc", "Global Solutions"]
- Regional breakdown: {"North": 120000, "South": 150000, "East": 100000, "West": 80000}
```

**What Claude Does:**

Calls `test_config`:

```json
{
  "draft_id": "draft-20251016T201530-abc123",
  "context": {
    "month": "October",
    "year": "2025",
    "revenue": 450000,
    "top_customers": ["Acme Corp", "TechStart Inc", "Global Solutions"],
    "regional_breakdown": {
      "North": 120000,
      "South": 150000,
      "East": 100000,
      "West": 80000
    }
  }
}
```

**Expected Response:**

```
Claude: Preview generated successfully (2.4 KB, 185ms):

─────────────────────────────────────────
# Monthly Sales Report
## October 2025

### Total Revenue: $450,000

### Top Customers
1. Acme Corp
2. TechStart Inc
3. Global Solutions

### Regional Breakdown
- North: $120,000 (27%)
- South: $150,000 (33%)
- East: $100,000 (22%)
- West: $80,000 (18%)

─────────────────────────────────────────

The preview looks good! Would you like to:
1. Add more sections (e.g., trends, forecasts)?
2. Adjust formatting?
3. Save this config?
```

---

### Step 3: Iterate - Add Trends Section

```
You: Add a trends section that compares to previous month
```

**What Claude Does:**

Calls `modify_config`:

```json
{
  "draft_id": "draft-20251016T201530-abc123",
  "updates": {
    "generation": {
      "patterns": [{
        "type": "jinja2",
        "template": "sales-report.md.jinja",
        "generation_config": {
          "context": {
            "month": "{{ month }}",
            "year": "{{ year }}",
            "revenue": "{{ revenue }}",
            "top_customers": "{{ top_customers }}",
            "regional_breakdown": "{{ regional_breakdown }}",
            "previous_month_revenue": "{{ previous_month_revenue }}",
            "revenue_change_pct": "{{ revenue_change_pct }}"
          }
        }
      }]
    }
  }
}
```

Then automatically calls `test_config` again with updated context.

**Expected Response:**

```
Claude: ✅ Draft updated

New preview with trends section:

─────────────────────────────────────────
# Monthly Sales Report
## October 2025

### Total Revenue: $450,000
📈 +12% from September ($402,000)

[...rest of sections...]

### Trends
Compared to September 2025:
- Revenue increased by $48,000 (+12%)
- Top performer: South region (+15%)
- Slight decline in West region (-3%)

─────────────────────────────────────────

Would you like to save this config?
```

---

### Step 4: Save Final Config

```
You: Yes, save it to configs/content/monthly-sales-report.json
```

**What Claude Does:**

Calls `save_config`:

```json
{
  "draft_id": "draft-20251016T201530-abc123",
  "destination_path": "configs/content/monthly-sales-report.json"
}
```

**Expected Response:**

```
Claude: ✅ Config saved successfully!

Saved to: configs/content/monthly-sales-report.json
Config ID: monthly-sales-report

Next steps:
1. Create template file: templates/sales-report.md.jinja
2. Generate first report: generate_content("monthly-sales-report", context={...})
3. Automate monthly: Schedule with cron/n8n

The draft is preserved in ephemeral storage for potential rollback.
```

**What You Learned:**
- Full lifecycle: draft → test → modify → test → save
- Iterative refinement based on previews
- Context variables validated before saving
- Time saved: ~10 minutes vs manual JSON editing

---

## Part 3: Batch Operations for Performance (15 min)

**Scenario:** Generate documentation for 5 API endpoints simultaneously.

### Understanding Batch Generation

**Sequential vs Parallel:**

```
Sequential (traditional):
  generate("endpoint-1") → 2s
  generate("endpoint-2") → 2s
  generate("endpoint-3") → 2s
  generate("endpoint-4") → 2s
  generate("endpoint-5") → 2s
  Total: 10 seconds

Parallel (batch_generate):
  batch_generate([1,2,3,4,5]) → 3s
  Total: 3 seconds
  Speedup: 3.3×
```

---

### Step 1: Prepare Multiple Configs

First, create 5 content configs for API endpoints (using conversational workflow):

```
You: Create 5 content configs for API endpoint documentation:
1. users-endpoint (GET /users)
2. posts-endpoint (GET /posts)
3. comments-endpoint (GET /comments)
4. auth-endpoint (POST /auth)
5. search-endpoint (GET /search)

All should use the jinja2 generator with template "api-endpoint.md.jinja"
```

**Expected Response:**

```
Claude: Created 5 content configs:

✅ users-endpoint (draft-abc111)
✅ posts-endpoint (draft-abc222)
✅ comments-endpoint (draft-abc333)
✅ auth-endpoint (draft-abc444)
✅ search-endpoint (draft-abc555)

All configs use jinja2 with api-endpoint.md.jinja template.
Would you like to test these as a batch before saving?
```

---

### Step 2: Batch Test Drafts

```
You: Test all 5 drafts as a batch with sample endpoint data
```

**What Claude Does:**

Calls `batch_generate` (or series of `test_config` calls):

```json
{
  "config_ids": [
    "users-endpoint",
    "posts-endpoint",
    "comments-endpoint",
    "auth-endpoint",
    "search-endpoint"
  ],
  "contexts": [
    {"method": "GET", "path": "/users", "description": "Get all users"},
    {"method": "GET", "path": "/posts", "description": "Get all posts"},
    {"method": "GET", "path": "/comments", "description": "Get comments"},
    {"method": "POST", "path": "/auth", "description": "Authenticate user"},
    {"method": "GET", "path": "/search", "description": "Search resources"}
  ]
}
```

**Expected Response:**

```
Claude: ✅ Batch test completed

Results:
- Successful: 5/5
- Failed: 0/5
- Total time: 2.8 seconds
- Average per item: 0.56 seconds
- Speedup: 3.6× vs sequential

All previews look good! Would you like to save all configs?
```

---

### Step 3: Batch Save Configs

```
You: Save all 5 configs to configs/content/api-endpoints/
```

**What Claude Does:**

Calls `save_config` for each draft:

```
Saved configs:
- configs/content/api-endpoints/users-endpoint.json
- configs/content/api-endpoints/posts-endpoint.json
- configs/content/api-endpoints/comments-endpoint.json
- configs/content/api-endpoints/auth-endpoint.json
- configs/content/api-endpoints/search-endpoint.json
```

---

### Step 4: Batch Generate Final Content

Now generate actual documentation for all endpoints:

```
You: Generate documentation for all 5 API endpoints in parallel
```

**What Claude Does:**

Calls `batch_generate`:

```json
{
  "content_config_ids": [
    "users-endpoint",
    "posts-endpoint",
    "comments-endpoint",
    "auth-endpoint",
    "search-endpoint"
  ],
  "output_dir": "output/api-docs"
}
```

**Expected Response:**

```
Claude: ✅ Batch generation completed

Results:
- Generated: 5/5 endpoints
- Failed: 0/5
- Total size: 45.2 KB
- Total time: 3.1 seconds
- Parallelization factor: 3.2×

Output files:
- output/api-docs/users-endpoint.md
- output/api-docs/posts-endpoint.md
- output/api-docs/comments-endpoint.md
- output/api-docs/auth-endpoint.md
- output/api-docs/search-endpoint.md

Next: Assemble these into complete API reference?
```

**What You Learned:**
- Batch operations are 3-5× faster than sequential
- Ideal for generating multiple similar pieces
- Error handling works per-item (partial failures don't block others)
- Perfect for automated documentation pipelines

---

## Part 4: Storage Management (10 min)

**Scenario:** Clean up old drafts and test outputs after completing work.

### Understanding Ephemeral Storage

```
ephemeral/
├── drafts/
│   ├── content/
│   │   ├── draft-20251014-*.json  (30 days old - should delete)
│   │   ├── draft-20251015-*.json  (29 days old - keep)
│   │   └── draft-20251016-*.json  (today - keep)
│   └── artifact/
│       └── draft-20251016-*.json
├── output/
│   ├── test_preview_*.md  (old test outputs)
│   └── temp_generation_*.md
└── .metadata.json
```

---

### Step 1: List Ephemeral Storage Contents

```
You: Show me all drafts and their ages
```

**What Claude Does:**

Uses file listing or internal MCP tool:

**Expected Response:**

```
Claude: Ephemeral storage contents:

**Content Drafts (3):**
- draft-20251014T091530-abc123 (31 days old - EXPIRED)
- draft-20251015T143022-def456 (30 days old - EXPIRES SOON)
- draft-20251016T201530-ghi789 (0 days old)

**Artifact Drafts (1):**
- draft-20251016T153000-jkl012 (0 days old)

**Test Outputs (12 files, 2.4 MB):**
- Various test_preview_* files from last 7 days

Storage usage: 3.1 MB
Recommendation: Clean up expired drafts and old test outputs
```

---

### Step 2: Clean Up Expired Drafts

```
You: Clean up all drafts older than 30 days
```

**What Claude Does:**

Calls `cleanup_ephemeral`:

```json
{
  "retention_days": 30,
  "target": "drafts"
}
```

**Expected Response:**

```
Claude: ✅ Cleanup completed

Deleted:
- 2 content drafts (31-35 days old)
- 0 artifact drafts
- Space freed: 24.5 KB

Retained:
- 2 content drafts (0-29 days old)
- 1 artifact draft (0 days old)

Storage now: 3.1 MB → 3.07 MB
```

---

### Step 3: Clean Up Old Test Outputs

```
You: Delete all test outputs older than 7 days
```

**What Claude Does:**

Calls `cleanup_ephemeral` targeting outputs:

```json
{
  "retention_days": 7,
  "target": "outputs"
}
```

**Expected Response:**

```
Claude: ✅ Cleanup completed

Deleted:
- 8 test output files (8-14 days old)
- Space freed: 1.8 MB

Retained:
- 4 test output files (0-7 days old)

Storage now: 3.07 MB → 1.27 MB
```

**What You Learned:**
- Ephemeral storage has automatic 30-day cleanup
- Manual cleanup available for immediate space freeing
- Separate retention policies for drafts vs outputs
- Safe cleanup (only deletes old/expired items)

---

## Part 5: End-to-End Documentation Pipeline (20 min)

**Scenario:** Build complete automated documentation system using all 17 tools.

### Pipeline Architecture

```
1. Discovery Phase
   ├─ capabilities://server (check version/features)
   ├─ capabilities://generators (check what's available)
   └─ list_content_configs (discover existing configs)

2. Config Creation Phase
   ├─ draft_config (create new configs)
   ├─ test_config (preview outputs)
   ├─ modify_config (refine based on preview)
   └─ save_config (persist when ready)

3. Content Generation Phase (Parallel)
   ├─ batch_generate (multiple pieces simultaneously)
   ├─ preview_generation (optional dry-run)
   └─ regenerate_content (force updates)

4. Artifact Assembly Phase
   ├─ trace_dependencies (check what's needed)
   ├─ assemble_artifact (combine into final docs)
   └─ validate_content (quality check)

5. Storage Management Phase
   ├─ list_artifacts (inventory what was created)
   ├─ cleanup_ephemeral (remove temp files)
   └─ delete_content (remove old versions)
```

---

### Step 1: Discovery & Planning

```
You: I want to build complete project documentation. First, discover:
1. What generators are available
2. What existing configs I have
3. What artifacts have been generated
```

**What Claude Does:**

```
1. Fetches capabilities://generators
2. Calls list_content_configs()
3. Calls list_artifacts()
```

**Expected Response:**

```
Claude: Documentation System Discovery:

**Available Generators (2):**
- jinja2 (template-based, dynamic)
- demonstration (example-based, static)

**Existing Content Configs (8):**
- readme-generator
- api-docs-from-openapi
- installation-guide
- user-guide
- developer-guide
- release-notes
- changelog-generator
- contributing-guide

**Generated Artifacts (3):**
- complete-project-docs (assembled 6 days ago)
- api-reference (assembled 2 days ago)
- user-documentation (assembled today)

Recommendation: Create artifact that combines all 8 configs into master documentation.
```

---

### Step 2: Create Master Artifact Config

```
You: Create an artifact config that combines all 8 existing content configs into complete project documentation
```

**What Claude Does:**

Calls `draft_config` for artifact:

```json
{
  "config_type": "artifact",
  "config_data": {
    "id": "master-project-docs",
    "content": {
      "children": [
        {"id": "readme", "path": "configs/content/readme-generator.json"},
        {"id": "install", "path": "configs/content/installation-guide.json"},
        {"id": "user-guide", "path": "configs/content/user-guide.json"},
        {"id": "api-docs", "path": "configs/content/api-docs-from-openapi.json"},
        {"id": "dev-guide", "path": "configs/content/developer-guide.json"},
        {"id": "changelog", "path": "configs/content/changelog-generator.json"},
        {"id": "contributing", "path": "configs/content/contributing-guide.json"},
        {"id": "release-notes", "path": "configs/content/release-notes.json"}
      ]
    },
    "output": {
      "primary_file": "COMPLETE_DOCUMENTATION.md"
    }
  }
}
```

---

### Step 3: Analyze Dependencies

```
You: Before assembling, analyze dependencies to see what content needs to be generated
```

**What Claude Does:**

Calls `trace_dependencies`:

```json
{
  "artifact_id": "master-project-docs"
}
```

**Expected Response:**

```
Claude: Dependency Analysis:

**Required Content (8 pieces):**
✅ readme (exists, fresh)
⚠️  install (exists, 7 days old - consider regenerating)
✅ user-guide (exists, fresh)
✅ api-docs (exists, fresh)
❌ dev-guide (missing - needs generation)
✅ changelog (exists, fresh)
✅ contributing (exists, fresh)
⚠️  release-notes (exists, 14 days old - stale)

**Recommendation:**
1. Generate missing: dev-guide
2. Regenerate stale: install, release-notes
3. Then assemble artifact

Shall I proceed with this plan?
```

---

### Step 4: Batch Generate Missing/Stale Content

```
You: Yes, generate the missing and stale content in parallel
```

**What Claude Does:**

Calls `batch_generate`:

```json
{
  "content_config_ids": [
    "developer-guide",
    "installation-guide",
    "release-notes"
  ],
  "force": true
}
```

**Expected Response:**

```
Claude: ✅ Batch generation completed

Results:
- developer-guide: Generated (new, 12.5 KB)
- installation-guide: Regenerated (updated, 8.2 KB)
- release-notes: Regenerated (updated, 6.1 KB)

All 8 required pieces now fresh and ready for assembly.
Total time: 4.2 seconds (3.1× speedup vs sequential)
```

---

### Step 5: Assemble Master Documentation

```
You: Assemble the complete master documentation artifact
```

**What Claude Does:**

Calls `assemble_artifact`:

```json
{
  "artifact_config_id": "master-project-docs",
  "output_path": "COMPLETE_DOCUMENTATION.md"
}
```

**Expected Response:**

```
Claude: ✅ Artifact assembled successfully

Output: COMPLETE_DOCUMENTATION.md
Size: 125.4 KB
Sections: 8
Assembly time: 2.1 seconds

Contents:
1. README (12.3 KB)
2. Installation Guide (8.2 KB)
3. User Guide (24.1 KB)
4. API Documentation (35.6 KB)
5. Developer Guide (12.5 KB)
6. Changelog (15.3 KB)
7. Contributing Guide (9.8 KB)
8. Release Notes (6.1 KB)

The complete documentation is ready at: COMPLETE_DOCUMENTATION.md
```

---

### Step 6: Validate & Cleanup

```
You: Validate the generated documentation and clean up any temporary files
```

**What Claude Does:**

```
1. Calls validate_content(content, rules=[...])
2. Calls cleanup_ephemeral(retention_days=30)
```

**Expected Response:**

```
Claude: ✅ Validation completed

Quality Checks:
- Heading hierarchy: ✅ Pass
- Broken links: ✅ Pass (0 broken)
- Markdown formatting: ✅ Pass
- Code blocks: ✅ Pass (all have language tags)
- Total issues: 0

✅ Cleanup completed

Deleted:
- 12 test preview files (old)
- 3 expired drafts
- Space freed: 2.1 MB

Your complete documentation is ready and validated!
```

**What You Learned:**
- Full end-to-end pipeline using all 17 tools
- Discovery → Creation → Generation → Assembly → Validation → Cleanup
- Batch operations save significant time (3-5× speedup)
- Dependency analysis prevents missing content errors
- Automated quality validation ensures correctness

---

## Part 6: Advanced Patterns & Best Practices (10 min)

### Pattern 1: Preview-Driven Development

**Workflow:**
```
1. draft_config (create structure)
2. test_config (preview output)
3. modify_config (adjust based on preview)
4. test_config (re-preview)
5. Repeat 3-4 until satisfied
6. save_config (persist)
```

**Benefit:** See output before committing, catch issues early.

---

### Pattern 2: Batch-First for Performance

**When generating multiple pieces:**
```
❌ Don't:
  for config in configs:
      generate_content(config)

✅ Do:
  batch_generate(configs)
```

**Speedup:** 3-5× faster, same results.

---

### Pattern 3: Dependency-Aware Assembly

**Before assembling artifacts:**
```
1. trace_dependencies(artifact_id)
2. Check what's missing/stale
3. batch_generate missing items
4. assemble_artifact
```

**Benefit:** Ensures all required content exists and is fresh.

---

### Pattern 4: Ephemeral-First, Persist When Ready

**Config creation:**
```
1. Start in ephemeral (draft_config)
2. Iterate freely (test, modify)
3. Save to permanent when confident (save_config)
4. Clean up old drafts periodically (cleanup_ephemeral)
```

**Benefit:** Safe experimentation without cluttering permanent storage.

---

### Pattern 5: Capability Discovery for Robustness

**Agent startup:**
```
1. Query capabilities://server (check version)
2. Query capabilities://tools (discover available operations)
3. Query capabilities://generators (check what's installed)
4. Adapt workflow based on discovered capabilities
```

**Benefit:** Works across versions, detects plugins, no hardcoded assumptions.

---

## Summary & Next Steps

### What You've Mastered

✅ **All 17 MCP Tools**
- Core generation (5 tools)
- Config lifecycle (4 tools)
- Discovery (4 tools)
- Storage management (3 tools)
- Validation (1 tool)

✅ **Capability Discovery**
- Dynamic server introspection
- Plugin detection
- Version-aware workflows

✅ **Performance Optimization**
- Batch operations (3-5× speedup)
- Parallel generation
- Resource management

✅ **Complete Pipelines**
- End-to-end documentation generation
- Dependency-aware assembly
- Quality validation

✅ **Best Practices**
- Preview-driven development
- Ephemeral-first workflow
- Automated cleanup

---

### Time Savings Achieved

**Traditional Workflow (Manual):**
- Create 8 configs: 2-3 hours (JSON editing)
- Generate 8 pieces: 10-15 minutes (sequential)
- Assemble artifact: 5-10 minutes
- **Total: 2.5-3.5 hours**

**MCP-Powered Workflow (This Tutorial):**
- Create 8 configs: 30-45 minutes (conversational)
- Generate 8 pieces: 3-5 minutes (batch)
- Assemble artifact: 2-3 minutes (automated)
- **Total: 35-53 minutes**

**Savings: 75-80% time reduction**

---

### Advanced Topics to Explore

1. **[How-To: Batch Generate Content](../../how-to/generation/batch-generate-content.md)**
   - Advanced batch patterns
   - Error recovery strategies
   - Performance tuning

2. **[How-To: Use Capability Discovery](../../how-to/mcp/use-capability-discovery.md)**
   - Building adaptive agents
   - Plugin detection patterns
   - Version compatibility checks

3. **[How-To: Manage Ephemeral Storage](../../how-to/storage/manage-ephemeral-storage.md)**
   - Storage optimization
   - Retention policy tuning
   - Backup and recovery

4. **[Reference: MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md)**
   - Complete tool comparison
   - Decision trees
   - Cross-references

---

### Practice Exercises

**Exercise 1: Multi-Language Documentation**
Create documentation in 3 languages (English, Spanish, French) using batch operations.

**Exercise 2: Automated Weekly Reports**
Build pipeline that:
1. Pulls data from APIs
2. Generates 5 section reports
3. Assembles into weekly summary
4. Validates quality
5. Cleans up drafts

**Exercise 3: Plugin Generator Integration**
1. Discover available plugins via capabilities://
2. Create configs using plugin generators
3. Compare output to built-in generators

---

**You're now an MCP integration expert! You can build sophisticated, automated documentation systems using all 17 tools.**

---

**Questions?**
- See [MCP Tool Reference](../../mcp/tool-reference.md) for complete tool documentation
- See [How-To Guides](../../how-to/) for task-specific instructions
- See [Explanation: Conversational Workflow Authoring](../../explanation/architecture/conversational-workflow-authoring.md) for architectural details
