# How-To: Discover and Browse Configs

**Goal:** Find, list, and explore content configs, artifact configs, and generated artifacts across your Chora Compose workspace.

**Prerequisites:**
- Chora Compose v1.1.0+ with discovery tools
- At least one content or artifact config
- Understanding of [content configs](./create-content-config.md) and [artifact configs](./create-artifact-config.md)

**Time:** 10-15 minutes

---

## Overview

**Config discovery** allows you to explore your workspace without manually browsing directories. This is essential for:

- Finding existing configs to reuse or modify
- Understanding what content can be generated
- Tracing artifact dependencies
- Auditing your content inventory
- Building dynamic workflows that adapt to available configs

**Discovery Tools:**

| Tool | Purpose | Returns |
|------|---------|---------|
| `list_content_configs` | List all content configs | Array of content config summaries |
| `list_artifact_configs` | List all artifact configs | Array of artifact config summaries |
| `list_artifacts` | List all generated artifacts | Array of artifact file paths |
| `trace_dependencies` | Show artifact dependencies | Dependency graph for an artifact |

---

## Quick Reference

### Discovery Patterns

```
Inventory Pattern:
  list_content_configs → See all content types available
  list_artifact_configs → See all artifact types available
  list_artifacts → See what's been generated

Search Pattern:
  list_content_configs(filter="api*") → Find configs matching pattern

Dependency Pattern:
  list_artifacts → Pick artifact
  trace_dependencies → See what content it uses
  list_content_configs → Find source configs
```

### Common Use Cases

| Use Case | Tools | Pattern |
|----------|-------|---------|
| "What can I generate?" | list_content_configs | Discovery |
| "What artifacts exist?" | list_artifact_configs | Inventory |
| "What have I generated?" | list_artifacts | Status check |
| "What does this artifact use?" | trace_dependencies | Dependency analysis |
| "Find all API docs" | list_content_configs(filter) | Search |

---

## Task 1: List All Content Configs

**Scenario:** See all available content types you can generate.

### Step 1: List All Content Configs

**Using Claude Desktop:**
```
You: List all content configs
```

**What Claude Does:**

Calls `list_content_configs` tool:

```json
{}
```

**Expected Response:**
```
Claude: 📋 Content Configs Inventory

Found 12 content configs:

API Documentation:
├─ api-endpoint (configs/content/api-endpoint.json)
│  Generator: demonstration
│  Template: templates/api-endpoint.md.jinja
│  Description: API endpoint documentation
│
├─ api-reference (configs/content/api-reference.json)
│  Generator: demonstration
│  Template: templates/api-reference.md.jinja
│  Description: Complete API reference

Reports:
├─ daily-report (configs/content/daily-report.json)
│  Generator: jinja2
│  Template: templates/daily-report.md.jinja
│  Description: Daily team activity report
│
├─ weekly-summary (configs/content/weekly-summary.json)
│  Generator: jinja2
│  Template: templates/weekly-summary.md.jinja
│  Description: Weekly summary report

Guides:
├─ user-guide (configs/content/user-guide.json)
│  Generator: demonstration
│  Template: templates/user-guide.md.jinja
│  Description: User guide documentation
│
└─ installation-guide (configs/content/installation-guide.json)
   Generator: demonstration
   Template: templates/installation.md.jinja
   Description: Installation instructions

Total: 12 configs
By Generator:
  - demonstration: 8 configs
  - jinja2: 4 configs
```

**What You Learned:**
- Complete inventory of content types
- Organized by category
- Generator and template information
- Quick overview of capabilities

---

### Step 2: List Configs with Details

```
You: List all content configs with full details
```

**Expected Response:**
```
Claude: 📋 Content Configs (Detailed)

[1] api-endpoint
    File: configs/content/api-endpoint.json
    ID: api-endpoint
    Generator: demonstration
    Template: templates/api-endpoint.md.jinja
    Output Path: output/{config_id}.md
    Context Schema: {method, path, description, parameters[]}
    Created: 2025-09-15
    Last Modified: 2025-10-10
    Generated Count: 23 times

[2] daily-report
    File: configs/content/daily-report.json
    ID: daily-report
    Generator: jinja2
    Template: templates/daily-report.md.jinja
    Output Path: output/reports/{date}.md
    Context Schema: {team, date, activities[]}
    Created: 2025-08-20
    Last Modified: 2025-10-01
    Generated Count: 45 times

[... 10 more configs ...]

Total: 12 configs
```

**What You Learned:**
- Detailed metadata for each config
- Context schema requirements
- Usage statistics
- Modification history

---

## Task 2: Search Configs by Pattern

**Scenario:** Find all configs related to API documentation.

### Step 1: Filter by Name Pattern

```
You: Find all content configs with 'api' in the name
```

**What Claude Does:**

```json
{
  "filter": "api*"
}
```

**Expected Response:**
```
Claude: 🔍 Content Configs Matching 'api*'

Found 3 matches:

[1] api-endpoint
    Template: templates/api-endpoint.md.jinja
    Generator: demonstration
    Used by artifacts: api-docs-bundle, complete-docs

[2] api-reference
    Template: templates/api-reference.md.jinja
    Generator: demonstration
    Used by artifacts: api-docs-bundle

[3] api-changelog
    Template: templates/api-changelog.md.jinja
    Generator: jinja2
    Used by artifacts: release-notes

Total: 3 configs
```

**What You Learned:**
- Pattern matching finds related configs
- See artifact dependencies
- Narrow down large inventories

---

### Step 2: Filter by Generator Type

```
You: Find all content configs using the 'jinja2' generator
```

**Expected Response:**
```
Claude: 🔍 Content Configs Using 'jinja2' Generator

Found 4 matches:

[1] daily-report
    Template: templates/daily-report.md.jinja
    Output: output/reports/{date}.md

[2] weekly-summary
    Template: templates/weekly-summary.md.jinja
    Output: output/reports/weekly-{week}.md

[3] api-changelog
    Template: templates/api-changelog.md.jinja
    Output: output/changelog-{version}.md

[4] metrics-dashboard
    Template: templates/metrics.html.jinja
    Output: output/metrics/{date}.html

Total: 4 configs (33% of all configs use jinja2)
```

**What You Learned:**
- Filter by generator type
- See template distribution
- Audit generator usage

---

## Task 3: List All Artifact Configs

**Scenario:** See all artifact types you can assemble.

### Step 1: List Artifact Configs

```
You: List all artifact configs
```

**What Claude Does:**

Calls `list_artifact_configs` tool:

```json
{}
```

**Expected Response:**
```
Claude: 📦 Artifact Configs Inventory

Found 5 artifact configs:

Documentation Bundles:
├─ api-docs-bundle (configs/artifact/api-docs-bundle.json)
│  Description: Complete API documentation bundle
│  Components: 3 content pieces
│  Output: artifacts/api-docs.md
│
├─ complete-docs (configs/artifact/complete-docs.json)
│  Description: All documentation in one artifact
│  Components: 8 content pieces
│  Output: artifacts/complete-docs.md

Release Bundles:
├─ release-notes (configs/artifact/release-notes.json)
│  Description: Release notes with changelog and migration guide
│  Components: 3 content pieces
│  Output: artifacts/release-v{version}.md
│
├─ onboarding-kit (configs/artifact/onboarding-kit.json)
│  Description: New user onboarding materials
│  Components: 5 content pieces
│  Output: artifacts/onboarding.md

Reports:
└─ monthly-report-bundle (configs/artifact/monthly-report-bundle.json)
   Description: Monthly report with all team summaries
   Components: 4 content pieces
   Output: artifacts/monthly-{month}.md

Total: 5 artifact configs
Total Components: 23 content references
```

**What You Learned:**
- Available artifact types
- Number of components per artifact
- Output locations
- Organized by category

---

### Step 2: Show Artifact Details

```
You: Show details for 'api-docs-bundle' artifact config
```

**Expected Response:**
```
Claude: 📦 Artifact Config Details: api-docs-bundle

Config File: configs/artifact/api-docs-bundle.json

Basic Info:
  ID: api-docs-bundle
  Description: Complete API documentation bundle
  Output: artifacts/api-docs.md

Components (3):
  [1] api-reference
      Source: configs/content/api-reference.json
      Context: {version: "2.0"}

  [2] api-endpoint
      Source: configs/content/api-endpoint.json
      Context: {endpoint: "/users"}

  [3] api-changelog
      Source: configs/content/api-changelog.json
      Context: {version: "2.0"}

Assembly Strategy:
  Separator: "\n\n---\n\n"
  Include TOC: true
  TOC Position: top

Metadata:
  Created: 2025-09-20
  Last Assembled: 2025-10-15
  Assembly Count: 12 times
```

**What You Learned:**
- Detailed component breakdown
- Context requirements
- Assembly configuration
- Usage statistics

---

## Task 4: List Generated Artifacts

**Scenario:** See what artifacts have been generated.

### Step 1: List All Generated Artifacts

```
You: List all generated artifacts
```

**What Claude Does:**

Calls `list_artifacts` tool:

```json
{}
```

**Expected Response:**
```
Claude: 📄 Generated Artifacts

Found 8 artifacts:

Recent (Last 7 Days):
├─ artifacts/api-docs.md
│  Size: 45.2 KB
│  Config: api-docs-bundle
│  Generated: 2025-10-16 14:23:45 (today)
│  Components: 3 content pieces
│
├─ artifacts/onboarding.md
│  Size: 28.7 KB
│  Config: onboarding-kit
│  Generated: 2025-10-14 09:15:30 (2 days ago)
│  Components: 5 content pieces

Older:
├─ artifacts/release-v1.1.0.md
│  Size: 12.3 KB
│  Config: release-notes
│  Generated: 2025-10-01 16:00:00 (15 days ago)
│  Components: 3 content pieces
│
├─ artifacts/monthly-september.md
│  Size: 32.1 KB
│  Config: monthly-report-bundle
│  Generated: 2025-09-30 23:59:00 (16 days ago)
│  Components: 4 content pieces

[... 4 more artifacts ...]

Total: 8 artifacts (118.3 KB)
Average size: 14.8 KB
```

**What You Learned:**
- All generated artifacts with timestamps
- File sizes and component counts
- Freshness indicators
- Storage usage

---

### Step 2: Filter Artifacts by Date

```
You: Show artifacts generated in the last 24 hours
```

**Expected Response:**
```
Claude: 📄 Artifacts Generated (Last 24 Hours)

Found 2 artifacts:

[1] artifacts/api-docs.md
    Generated: 2025-10-16 14:23:45 (2 hours ago)
    Config: api-docs-bundle
    Size: 45.2 KB
    Components: api-reference, api-endpoint, api-changelog

[2] artifacts/test-artifact.md
    Generated: 2025-10-16 10:15:20 (6 hours ago)
    Config: test-bundle
    Size: 3.8 KB
    Components: test-content-1, test-content-2

Total: 2 artifacts (49.0 KB)
```

**What You Learned:**
- Time-based filtering
- Recent generation activity
- Quick status check

---

## Task 5: Trace Artifact Dependencies

**Scenario:** Understand what content pieces an artifact uses.

### Step 1: Trace Dependencies for Artifact

```
You: Trace dependencies for 'api-docs-bundle'
```

**What Claude Does:**

Calls `trace_dependencies` tool:

```json
{
  "artifact_config_id": "api-docs-bundle"
}
```

**Expected Response:**
```
Claude: 🔍 Dependency Trace: api-docs-bundle

Artifact: api-docs-bundle
Config: configs/artifact/api-docs-bundle.json
Output: artifacts/api-docs.md

Dependency Graph:

api-docs-bundle (artifact)
├─ api-reference (content)
│  ├─ Template: templates/api-reference.md.jinja
│  ├─ Generator: demonstration
│  ├─ Generated: output/api-reference.md (15.2 KB)
│  └─ Status: ✅ Generated (cached)
│
├─ api-endpoint (content)
│  ├─ Template: templates/api-endpoint.md.jinja
│  ├─ Generator: demonstration
│  ├─ Generated: output/api-endpoint.md (18.9 KB)
│  └─ Status: ✅ Generated (cached)
│
└─ api-changelog (content)
   ├─ Template: templates/api-changelog.md.jinja
   ├─ Generator: jinja2
   ├─ Generated: output/api-changelog.md (11.1 KB)
   └─ Status: ✅ Generated (cached)

Summary:
- Total Dependencies: 3 content configs
- All Content Generated: ✅ Yes
- Missing Content: 0
- Artifact Status: Ready to assemble

Template Dependencies:
- templates/api-reference.md.jinja (used by api-reference)
- templates/api-endpoint.md.jinja (used by api-endpoint)
- templates/api-changelog.md.jinja (used by api-changelog)
```

**What You Learned:**
- Complete dependency tree
- Status of each component
- Template dependencies
- Readiness for assembly

---

### Step 2: Trace with Missing Dependencies

**Scenario:** Some content not yet generated.

```
You: Trace dependencies for 'complete-docs'
```

**Expected Response:**
```
Claude: 🔍 Dependency Trace: complete-docs

Artifact: complete-docs
Config: configs/artifact/complete-docs.json
Output: artifacts/complete-docs.md

Dependency Graph:

complete-docs (artifact)
├─ user-guide (content) ✅
│  Status: Generated (output/user-guide.md, 5.8 KB)
│
├─ installation-guide (content) ✅
│  Status: Generated (output/installation-guide.md, 4.2 KB)
│
├─ api-reference (content) ✅
│  Status: Generated (output/api-reference.md, 15.2 KB)
│
├─ troubleshooting (content) ❌
│  Status: Not generated yet
│  Config: configs/content/troubleshooting.json
│
└─ faq (content) ❌
   Status: Not generated yet
   Config: configs/content/faq.json

Summary:
- Total Dependencies: 5 content configs
- Generated: 3/5 (60%)
- Missing: 2/5 (40%)
- Artifact Status: ⚠️  Cannot assemble (missing content)

Action Required:
Generate missing content before assembling artifact:
  1. generate_content --config troubleshooting
  2. generate_content --config faq
  3. assemble_artifact --config complete-docs
```

**What You Learned:**
- Identify missing dependencies
- Blockers preventing assembly
- Actionable steps to resolve
- Status indicators for each component

---

## Task 6: Build Dynamic Workflows

**Scenario:** Dynamically generate content based on available configs.

### Pattern: Auto-Generate All Available Content

**Agent Workflow:**

```python
# Step 1: Discover all content configs
content_configs = list_content_configs()

# Step 2: Filter for specific type (e.g., daily reports)
daily_reports = [
    c for c in content_configs
    if "daily" in c["id"] or "report" in c["id"]
]

# Step 3: Generate all matching configs
for config in daily_reports:
    generate_content(
        content_config_id=config["id"],
        context={"date": today()}
    )

# Output:
# Generated: daily-report.md
# Generated: daily-summary.md
# Generated: daily-metrics.md
```

**What You Learned:**
- Discovery enables dynamic workflows
- Filter configs programmatically
- Adapt to changing inventory

---

### Pattern: Validate All Artifact Dependencies

**Agent Workflow:**

```python
# Step 1: List all artifact configs
artifact_configs = list_artifact_configs()

# Step 2: Trace dependencies for each
for artifact in artifact_configs:
    deps = trace_dependencies(artifact["id"])

    # Step 3: Check if all content generated
    missing = [d for d in deps if not d["generated"]]

    if missing:
        print(f"⚠️  {artifact['id']}: Missing {len(missing)} dependencies")
        for m in missing:
            print(f"   - {m['id']}")
    else:
        print(f"✅ {artifact['id']}: Ready to assemble")

# Output:
# ✅ api-docs-bundle: Ready to assemble
# ⚠️  complete-docs: Missing 2 dependencies
#    - troubleshooting
#    - faq
# ✅ release-notes: Ready to assemble
```

**What You Learned:**
- Automated dependency validation
- Pre-flight checks before assembly
- Proactive issue detection

---

## Best Practices

### ✅ Do's

1. **Use Discovery for Inventory Audits**
   ```
   ✅ Good: Regularly list configs to track what exists
   ❌ Bad: Manually browse directories
   ```

2. **Trace Dependencies Before Assembly**
   ```python
   # Always check dependencies first
   deps = trace_dependencies("my-artifact")
   if all(d["generated"] for d in deps):
       assemble_artifact("my-artifact")
   else:
       print("Missing dependencies - generate content first")
   ```

3. **Filter Configs for Batch Operations**
   ```python
   # Find all API-related configs
   api_configs = list_content_configs(filter="api*")

   # Batch generate them
   batch_generate(config_ids=[c["id"] for c in api_configs])
   ```

4. **Use Discovery in Agent Initialization**
   ```python
   async def initialize_agent():
       # Discover capabilities
       content_types = await list_content_configs()
       artifact_types = await list_artifact_configs()

       # Adapt workflow to available configs
       if "api-endpoint" in [c["id"] for c in content_types]:
           enable_api_doc_generation()
   ```

---

### ❌ Don'ts

1. **Don't Hardcode Config IDs**
   ```
   ❌ Bad: generate_content("api-endpoint")  # Fails if renamed
   ✅ Good: configs = list_content_configs()
            if "api-endpoint" in [c["id"] for c in configs]:
                generate_content("api-endpoint")
   ```

2. **Don't Assume Configs Exist**
   ```
   ❌ Bad: assemble_artifact("bundle")  # Fails if config missing
   ✅ Good: artifacts = list_artifact_configs()
            if "bundle" in [a["id"] for a in artifacts]:
                assemble_artifact("bundle")
   ```

3. **Don't Skip Dependency Checks**
   ```
   ❌ Bad: assemble_artifact("complete-docs")  # May fail if content missing
   ✅ Good: deps = trace_dependencies("complete-docs")
            if all(d["generated"] for d in deps):
                assemble_artifact("complete-docs")
   ```

---

## Common Scenarios

### Scenario 1: "What Can I Generate Today?"

**Workflow:**
```
1. List all content configs
2. Filter by category or generator
3. Review descriptions and templates
4. Choose configs to generate

Agent Response:
"You have 12 content configs available:
 - 5 API documentation configs
 - 4 report configs
 - 3 guide configs

Which would you like to generate?"
```

---

### Scenario 2: "Why Won't My Artifact Assemble?"

**Workflow:**
```
1. Trace dependencies for artifact
2. Identify missing content
3. Generate missing content
4. Retry assembly

Agent Response:
"Artifact 'complete-docs' is missing 2 dependencies:
 - troubleshooting (config exists, not generated)
 - faq (config exists, not generated)

Generating missing content now..."
```

---

### Scenario 3: "Clean Up Old Artifacts"

**Workflow:**
```
1. List all artifacts
2. Filter by age (>30 days)
3. Check if still referenced by active artifact configs
4. Delete unreferenced old artifacts

Agent Response:
"Found 3 artifacts older than 30 days:
 - artifacts/release-v1.0.0.md (60 days, not referenced)
 - artifacts/old-docs.md (45 days, not referenced)
 - artifacts/archive.md (35 days, referenced by 'archive-bundle')

Safe to delete: 2 artifacts (105 days total age)"
```

---

## Troubleshooting

### Issue: Empty Config Lists

**Symptoms:**
```
list_content_configs() returns []
```

**Possible Causes:**

1. **No configs created yet**
   - Solution: Create at least one content config

2. **Wrong directory**
   - Check: configs/content/ exists and contains .json files
   - Solution: Verify working directory

3. **Invalid JSON in configs**
   - Solution: Validate all JSON files

---

### Issue: Trace Shows Circular Dependencies

**Error:**
```
Circular dependency detected:
  artifact-a → content-x → artifact-b → content-y → artifact-a
```

**Cause:** Artifacts referencing each other (not allowed).

**Solution:**
```
1. Review artifact configs
2. Remove circular references
3. Restructure dependency tree
```

**Chora Compose doesn't allow artifact→artifact dependencies**, only artifact→content.

---

### Issue: Missing Configs in List

**Symptoms:**
```
list_content_configs() doesn't show 'my-config'
```

**Possible Causes:**

1. **File not in configs/content/**
   - Solution: Move to correct directory

2. **File extension not .json**
   - Solution: Rename to my-config.json

3. **Invalid JSON schema**
   - Solution: Validate against config schema

---

## Related Documentation

- **[Tutorial: MCP Integration Deep Dive](../../tutorials/advanced/01-mcp-integration-deep-dive.md)** - Part 5 covers discovery patterns
- **[How-To: Create Content Config](./create-content-config.md)** - Creating configs that will be discoverable
- **[How-To: Create Artifact Config](./create-artifact-config.md)** - Creating artifact configs
- **[Reference: MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md)** - Complete tool reference
- **[E2E Test Suite: Configuration](../../mcp/E2E_CONFIGURATION.md)** - Test cases for discovery tools

---

**You can now discover, browse, and trace configs dynamically across your workspace!**
