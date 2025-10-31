# How-To: Create Configurations Conversationally

> **⚠️ DEPRECATED (v1.2.0):** This guide describes config lifecycle tools (`draft_config`, `test_config`, `modify_config`, `save_config`) that are **planned for v1.3.0** but **not yet implemented**. Currently, configurations must be created manually as JSON files in the `configs/` directory. See [Schema Reference](../../reference/schema/README.md) for manual config creation.
>
> **Tracking:** [GitHub Issue #TBD](https://github.com/liminalcommons/chora-compose/issues) - Config Lifecycle Tools Implementation

**Goal:** Learn task-oriented workflows for creating and refining configurations through conversation with Claude Desktop, using the config lifecycle tools (planned for v1.3.0).

**Prerequisites:**
- Claude Desktop with Chora Compose MCP integration configured
- Basic understanding of content and artifact configs
- Familiarity with the [draft → test → modify → save workflow](../../tutorials/intermediate/02-conversational-config-creation.md)

**Time:** 15-30 minutes (depending on task)

---

## Quick Reference

### Config Lifecycle Tools

| Tool | Command Pattern | Use Case |
|------|----------------|----------|
| **draft_config** | "Create a config for [purpose]" | Start new config |
| **test_config** | "Test it with [context]" | Preview output |
| **modify_config** | "Add/change [feature]" | Refine config |
| **save_config** | "Save this config" | Persist to filesystem |

### Common Workflows

```
New Config:        draft → test → save
Iterative:         draft → test → modify → test → save
Multiple Options:  draft A → draft B → test both → save winner
Fix & Test:        draft → test → fix → test → save
```

---

## Task 1: Create a Simple Content Config

**Scenario:** You need a config for generating README files.

### Step 1: Draft the Config

**You:**
```
Create a content config for generating README files from project metadata
```

**Claude will:**
- Call `draft_config` with basic structure
- Return draft_id (e.g., "draft_a1b2c3")
- Validate against JSON Schema
- Store in ephemeral/drafts/content/

**Expected Response:**
```
✅ Draft created: draft_a1b2c3
Type: content
Generator: jinja2 (default)
Template: readme.md.jinja
Status: Valid

Next: Test this draft or add custom sections?
```

---

### Step 2: Test the Draft

**You:**
```
Test it with project name "MyProject" and description "A cool tool"
```

**Claude will:**
- Call `test_config(draft_id, context={...})`
- Generate preview without writing files
- Show you what the output would look like

**Expected Response:**
```
Preview:
─────────────────────
# MyProject

A cool tool

## Installation
[content here]
─────────────────────

Stats: 245 chars, 150ms generation
Looks good? Save it or refine further?
```

---

### Step 3: Save When Ready

**You:**
```
Perfect, save it
```

**Claude will:**
- Call `save_config(draft_id)`
- Atomic copy to configs/content/
- Validate one final time
- Remove from ephemeral (optional retention)

**Expected Response:**
```
✅ Saved: configs/content/readme-generator.json
Config ID: readme-generator

Use with:
  generate_content("readme-generator", context={...})
```

**Time Saved:** 5 minutes vs manual JSON editing

---

## Task 2: Create Config with Data Sources

**Scenario:** Generate API documentation from OpenAPI spec file.

### Step 1: Draft with Input Configuration

**You:**
```
Create a config that generates API docs from an OpenAPI spec file at data/openapi.json
```

**Claude will:**
- Include `inputs` section with file source
- Configure JSON file loading
- Set up context mapping

**Draft Structure:**
```json
{
  "id": "api-docs-from-openapi",
  "inputs": {
    "sources": [
      {
        "type": "file",
        "id": "openapi_spec",
        "path": "data/openapi.json",
        "format": "json"
      }
    ]
  },
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "api-docs.md.jinja",
      "generation_config": {
        "context": {
          "spec": "{{ openapi_spec }}"
        }
      }
    }]
  }
}
```

---

### Step 2: Test with Real File

**You:**
```
Test it with the actual file at data/openapi.json
```

**Claude will:**
- Load data/openapi.json
- Pass to test_config as context
- Render template with real data
- Show preview

**Expected Response:**
```
Preview (first 500 chars):
─────────────────────
# API Reference

## POST /users
Create a new user

**Parameters:**
- name (string, required)
- email (string, required)
...
─────────────────────

Found 12 endpoints, 3 schemas
Generation successful!
```

---

### Step 3: Add Error Handling

**You:**
```
Add validation to check if the OpenAPI file exists before generation
```

**Claude will:**
- Call `modify_config` to add validation rules
- Update inputs section with file_exists check
- Re-test to verify

**Modified Config:**
```json
{
  "inputs": {
    "sources": [
      {
        "type": "file",
        "id": "openapi_spec",
        "path": "data/openapi.json",
        "format": "json",
        "validation": {
          "file_exists": true,
          "schema_version": "3.0"
        }
      }
    ]
  }
}
```

---

## Task 3: Create Artifact Config with Multiple Sections

**Scenario:** Assemble a complete project documentation artifact from multiple content pieces.

### Step 1: Draft Artifact Config

**You:**
```
Create an artifact config that combines:
- README (intro)
- API Reference (main content)
- Installation Guide (appendix)
```

**Claude will:**
- Create artifact config type
- Set up children sections
- Configure assembly order

**Draft Structure:**
```json
{
  "type": "artifact",
  "id": "complete-project-docs",
  "content": {
    "children": [
      {
        "id": "intro",
        "path": "configs/content/readme-generator.json"
      },
      {
        "id": "api-ref",
        "path": "configs/content/api-docs-from-openapi.json"
      },
      {
        "id": "install",
        "path": "configs/content/installation-guide.json"
      }
    ]
  },
  "output": {
    "primary_file": "DOCUMENTATION.md"
  }
}
```

---

### Step 2: Test Assembly

**You:**
```
Test the artifact assembly with sample context
```

**Claude will:**
- Call `test_config` for artifact
- Generate each child section
- Assemble in order
- Show combined preview

**Expected Response:**
```
Artifact Preview:
─────────────────────
# MyProject                    ← from intro

API Reference                  ← from api-ref
...

Installation                   ← from install
...
─────────────────────

3 sections assembled
Total: 2,456 chars
Assembly successful!
```

---

### Step 3: Adjust Section Order

**You:**
```
Move Installation before API Reference
```

**Claude will:**
- Call `modify_config` with updated children order
- Re-test to show new assembly

**Modified:**
```json
{
  "content": {
    "children": [
      {"id": "intro", ...},
      {"id": "install", ...},      // ← moved up
      {"id": "api-ref", ...}        // ← moved down
    ]
  }
}
```

---

## Task 4: Iterate on Config Based on Preview

**Scenario:** Refine a config until the output is exactly right.

### Iterative Workflow

**Round 1: Initial Draft**
```
You: Create a config for weekly status reports
Claude: ✅ Draft created (draft_x1y2z3)
```

**Round 2: Test & Identify Issues**
```
You: Test with sample team data
Claude: [Shows preview]

Issue noticed: Missing "Blockers" section
```

**Round 3: Add Missing Section**
```
You: Add a blockers section
Claude: ✅ Modified draft
        [Shows updated preview]

Issue noticed: Metrics formatting unclear
```

**Round 4: Improve Formatting**
```
You: Format metrics as a table
Claude: ✅ Modified draft
        [Shows updated preview]

Looks good now!
```

**Round 5: Save Final Version**
```
You: Save it
Claude: ✅ Saved to configs/content/weekly-status-report.json
```

**Iterations:** 4 modify cycles
**Time:** 8 minutes (vs 20-25 minutes with manual editing)

---

## Task 5: Create Multiple Draft Options and Compare

**Scenario:** You're not sure which approach is best - try multiple and compare.

### Step 1: Create Two Different Approaches

**You:**
```
Create two configs for release notes:
1. Using Jinja2 template with Git log data
2. Using demonstration generator with example format
```

**Claude will:**
- Create draft_option1 (Jinja2 approach)
- Create draft_option2 (demonstration approach)
- Store both in ephemeral storage

**Expected Response:**
```
✅ Created 2 draft options:

Option 1 (draft_aaa111): Jinja2 Template
- Pros: Flexible, data-driven
- Cons: Requires template file
- Best for: Complex formatting

Option 2 (draft_bbb222): Demonstration
- Pros: Simple, no template needed
- Cons: Static structure
- Best for: Consistent format

Test both to compare?
```

---

### Step 2: Test Both with Same Context

**You:**
```
Test both with the same release data
```

**Claude will:**
- Test draft_aaa111 with context
- Test draft_bbb222 with same context
- Show side-by-side comparison

**Expected Response:**
```
Option 1 (Jinja2) Preview:
─────────────────────
# Release v1.2.0

## New Features
- Feature A (commit abc123)
- Feature B (commit def456)

## Bug Fixes
- Fixed X (commit ghi789)
─────────────────────

Option 2 (Demonstration) Preview:
─────────────────────
# Release Notes

**Version:** 1.2.0

**What's New:**
Feature A, Feature B

**Fixes:**
Fixed X
─────────────────────

Which style do you prefer?
```

---

### Step 3: Choose and Save Winner

**You:**
```
I prefer Option 1's detailed format. Save that one
```

**Claude will:**
- Save draft_aaa111 to filesystem
- Optionally delete draft_bbb222 (or let it expire)

**Expected Response:**
```
✅ Saved Option 1: configs/content/release-notes-detailed.json

The other draft (draft_bbb222) will auto-delete in 30 days,
or I can remove it now if you prefer.
```

---

## Task 6: Fix Schema Validation Errors

**Scenario:** Your draft has validation errors - fix them conversationally.

### Step 1: Encounter Validation Error

**You:**
```
Create a config with custom generator type "markdown"
```

**Claude encounters:**
```
❌ Schema Validation Error

Field: generation.patterns[0].type
Error: "markdown" is not a valid generator type
Allowed: jinja2, demonstration, template_fill

Would you like me to:
1. Use jinja2 instead (recommended for markdown)?
2. Check available generators?
3. Explain generator types?
```

---

### Step 2: Fix with Claude's Help

**You:**
```
Use jinja2 instead
```

**Claude will:**
- Retry draft_config with corrected type
- Validate successfully
- Create draft

**Expected Response:**
```
✅ Fixed! Draft created with jinja2 generator

The config will use:
- Generator: jinja2
- Template: [name].md.jinja
- Output: Markdown format

Test it?
```

**Key Learning:** Schema validation catches errors immediately - no invalid configs reach storage.

---

## Task 7: Manage Multiple Concurrent Drafts

**Scenario:** You're working on several configs simultaneously.

### List All Active Drafts

**You:**
```
What drafts do I have right now?
```

**Claude will:**
- Scan ephemeral/drafts/content/ and ephemeral/drafts/artifact/
- List all active drafts with metadata

**Expected Response:**
```
Active Drafts:

Content Configs (3):
- draft_a1b2c3: readme-generator (created Oct 16, expires Nov 15)
- draft_d4e5f6: api-docs (created Oct 15, expires Nov 14)
- draft_g7h8i9: release-notes (created Oct 14, expires Nov 13)

Artifact Configs (1):
- draft_j1k2l3: complete-docs (created Oct 16, expires Nov 15)

Which would you like to work on?
```

---

### Resume Work on Specific Draft

**You:**
```
Test the release-notes draft (draft_g7h8i9) with v1.2.0 data
```

**Claude will:**
- Load draft_g7h8i9 from ephemeral storage
- Test with provided context
- Show preview

**Benefit:** Pick up where you left off, even days later (within 30-day window)

---

### Clean Up Unwanted Drafts

**You:**
```
Delete the api-docs draft (draft_d4e5f6) - I don't need it anymore
```

**Claude will:**
- Remove draft from ephemeral storage
- Confirm deletion

**Expected Response:**
```
✅ Deleted draft_d4e5f6

Remaining drafts: 3
Storage freed: 2.3 KB
```

---

## Task 8: Convert Existing File-Based Config to Conversational

**Scenario:** You have an existing config file - load it as a draft to refine conversationally.

### Step 1: Load Existing Config as Draft

**You:**
```
Load configs/content/old-report.json as a draft so I can refine it
```

**Claude will:**
- Read the existing file
- Create new draft with same content
- Return draft_id

**Expected Response:**
```
✅ Loaded as draft: draft_m1n2o3

Original: configs/content/old-report.json
Draft: ephemeral/drafts/content/draft_m1n2o3.json

Changes to the draft won't affect the original until you save.
Test it or make changes?
```

---

### Step 2: Modify the Draft

**You:**
```
Add a "Next Steps" section to the report
```

**Claude will:**
- Call modify_config on draft_m1n2o3
- Add new section
- Test to show preview

---

### Step 3: Save Over Original or New File

**You (Option A - Overwrite):**
```
Save this back to configs/content/old-report.json
```

**You (Option B - New File):**
```
Save this as configs/content/new-report.json
```

**Claude will:**
- Save to specified path
- Preserve original if using new path
- Atomic write operation

---

## Common Patterns & Tips

### Pattern: Quick Prototype → Refine → Save

```
1. "Create a config for [X]"           ← Quick draft
2. "Test with minimal data"            ← Verify basics work
3. "Add [feature Y]"                   ← Iterate 3-5 times
4. "Test with real data"               ← Final validation
5. "Save it"                           ← Persist
```

**Time:** 5-10 minutes
**Use for:** Exploratory config creation

---

### Pattern: Compare Multiple Approaches

```
1. "Create 3 configs for [X] using different generators"
2. "Test all 3 with same context"
3. "Show me side-by-side comparison"
4. "Save the [jinja2/demonstration] version"
```

**Time:** 10-15 minutes
**Use for:** Finding best approach for complex use case

---

### Pattern: Incremental Migration

```
1. "Load existing-config.json as draft"
2. "Add [new feature]"
3. "Test with production data"
4. "Save as existing-config-v2.json"
5. "Compare outputs between v1 and v2"
```

**Time:** 15-20 minutes
**Use for:** Upgrading configs safely

---

## Troubleshooting

### Issue: Preview Too Long to Read

**Problem:**
```
You: Test the config
Claude: [Outputs 5000 lines of preview]
```

**Solution:**
```
You: Show just the first 500 characters of the preview
```

Or:
```
You: Summarize the preview instead of showing full output
```

---

### Issue: Draft Expired (After 30 Days)

**Problem:**
```
You: Test draft_xyz789
Claude: ❌ Draft not found (may have expired)
```

**Solution:**
```
You: Recreate the config for [original purpose]
```

**Prevention:** Save important drafts within 30 days

---

### Issue: Complex Nested Updates Difficult

**Problem:**
Trying to modify deeply nested field conversationally is clunky.

**Solution:**
```
You: Save this draft to a temp file so I can edit the nested structure manually
```

Then edit in IDE, and:
```
You: Load temp-config.json as a new draft
```

**Hybrid Approach:** Conversational for structure, IDE for complex nested edits

---

### Issue: Can't Remember Draft ID

**Problem:**
```
You: Test my release notes draft
Claude: Which draft? You have draft_a1b2c3 and draft_g7h8i9
```

**Solution:**
```
You: List my drafts and describe what each one is for
```

**Tip:** Add descriptions when creating drafts:
```
You: Create a config for release notes (DESCRIPTION: quarterly releases)
```

---

## Best Practices

### ✅ Do's

1. **Test Before Saving**
   ```
   draft → test → modify → test → save
   ```
   Never skip the test step!

2. **Use Descriptive IDs**
   ```
   Good: "weekly-team-report"
   Bad:  "report" or "config1"
   ```

3. **Iterate in Small Steps**
   ```
   ✅ "Add metrics section" → test → "Format as table" → test
   ❌ "Add metrics, format as table, and include charts" → test
   ```

4. **Clean Up Unneeded Drafts**
   ```
   After saving: Delete or let drafts expire
   Keep ephemeral storage tidy
   ```

5. **Save Early If Valuable**
   ```
   Don't wait 29 days to save important configs
   Save as soon as you're 80% confident
   ```

---

### ❌ Don'ts

1. **Don't Skip Validation**
   ```
   ❌ draft → save (no test!)
   ✅ draft → test → save
   ```

2. **Don't Rely on Drafts for Permanence**
   ```
   ❌ Keep important configs as drafts for months
   ✅ Save to filesystem, commit to git
   ```

3. **Don't Create Redundant Drafts**
   ```
   ❌ draft_report1, draft_report2, draft_report3 (same purpose)
   ✅ One draft, multiple modify iterations
   ```

4. **Don't Ignore Schema Errors**
   ```
   ❌ Try to save despite validation errors
   ✅ Fix errors before saving
   ```

---

## When to Use Conversational vs File-Based

### ✅ Use Conversational When:

- **Learning** config structure for the first time
- **Prototyping** new config ideas quickly
- **Simple configs** with 1-3 patterns
- **Non-technical users** creating configs
- **Immediate feedback** needed (preview-driven development)
- **Mobile/remote** scenarios without IDE access

### ✅ Use File-Based When:

- **Complex nested structures** (10+ levels deep)
- **Bulk updates** (changing 20+ fields at once)
- **Version control** critical (git history of changes)
- **Offline work** required
- **Team collaboration** on config design (PR reviews)
- **Advanced IDE features** needed (autocomplete, validation)

### ✅ Hybrid Approach:

```
1. Draft conversationally   (explore structure)
2. Save to filesystem      (get initial file)
3. Edit in IDE             (complex refinements)
4. Load as draft           (test changes conversationally)
5. Save final version      (persist)
6. Commit to git           (version control)
```

**Best of both worlds!**

---

## Quick Command Reference

### Essential Commands

```bash
# Create new config
"Create a [content/artifact] config for [purpose]"

# Test draft
"Test draft_[id] with [context]"
"Test it with [specific data]"

# Modify draft
"Add [feature] to the config"
"Change [field] to [value]"
"Remove [section]"

# Save draft
"Save this config"
"Save as configs/content/[name].json"

# Manage drafts
"List my drafts"
"Delete draft_[id]"
"Show me what's in draft_[id]"
```

---

## Next Steps

### Related Documentation

- **[Tutorial: Conversational Config Creation](../../tutorials/intermediate/02-conversational-config-creation.md)** - Hands-on learning path
- **[How-To: Manage Draft Configs](./manage-draft-configs.md)** - Ephemeral storage management
- **[Explanation: Conversational Workflow Authoring](../../explanation/architecture/conversational-workflow-authoring.md)** - Why this approach matters
- **[MCP Tool Reference](../../mcp/tool-reference.md)** - Complete tool documentation

### Advanced Topics

- **[Batch Config Creation](../../tutorials/advanced/01-mcp-integration-deep-dive.md)** - Create multiple configs in parallel
- **[Config Templating](../generation/use-template-inheritance.md)** - Reusable config patterns
- **[CI/CD Integration](../../guides/llm-agent-integration.md)** - Automated config generation in pipelines

---

**You're now equipped to create configurations conversationally!**
