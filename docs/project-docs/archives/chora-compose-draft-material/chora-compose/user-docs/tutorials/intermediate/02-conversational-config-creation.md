# Tutorial: Conversational Config Creation

> **⚠️ DEPRECATED (v1.2.0):** This tutorial describes the config lifecycle workflow (`draft_config`, `test_config`, `modify_config`, `save_config`) which is **planned for v1.3.0** but **not yet implemented**. This content remains as design documentation for the planned feature. For current config creation, use manual JSON editing - see [Your First Config](../getting-started/02-your-first-config.md).

**Learning Goals:**
- Create configurations through conversation with Claude (no file editing) [PLANNED v1.3.0]
- Use the draft → test → modify → save workflow [PLANNED v1.3.0]
- Understand ephemeral storage and 30-day retention [IMPLEMENTED]
- Iterate on configs using preview feedback [PLANNED v1.3.0]
- Know when to use conversational vs file-based authoring [PLANNED v1.3.0]

**Prerequisites:**
- Completed [Tutorial: Your First Config](../getting-started/02-your-first-config.md)
- Claude Desktop with Chora Compose MCP integration configured
- Basic understanding of content configs and artifact configs
- 30-40 minutes of time

**Difficulty:** Intermediate

**Version:** v1.2.0 (feature planned for v1.3.0)

---

## What You'll Build

By the end of this tutorial, you'll have created a **weekly team report config** entirely through conversation with Claude Desktop - without editing a single JSON file.

**What makes this different:**
- Traditional: Open IDE → create JSON → save → test → fix errors → repeat
- Conversational: Chat with Claude → preview instantly → refine → save when ready
- Time savings: 20-30 minutes → 5-10 minutes

---

## Part 1: Understanding Config Lifecycle Tools

### The Four Config Lifecycle Tools

Chora Compose v1.1.0 introduces four new MCP tools for conversational workflow authoring:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **draft_config** | Create temporary config in ephemeral storage | Start a new config conversationally |
| **test_config** | Preview generation output without persistence | Validate config before saving |
| **modify_config** | Update draft config fields | Refine based on preview feedback |
| **save_config** | Persist draft to filesystem | Finalize and make permanent |

### The Conversational Workflow

```
┌─────────────────────────────────────────────────────────┐
│         Conversational Config Creation                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. DRAFT                                                 │
│     "Create a config for weekly reports"                  │
│     ↓                                                     │
│     Claude calls: draft_config()                          │
│     Returns: draft_id = "draft_abc123"                    │
│     Stored in: ephemeral/drafts/content/draft_abc123.json│
│                                                           │
│  2. TEST                                                  │
│     "Show me what it would generate"                      │
│     ↓                                                     │
│     Claude calls: test_config(draft_id)                   │
│     Returns: Preview of generated content                 │
│                                                           │
│  3. ITERATE (Repeat as needed)                            │
│     "Add a section for team metrics"                      │
│     ↓                                                     │
│     Claude calls: modify_config(draft_id, updates)        │
│     Then calls: test_config(draft_id)                     │
│     Returns: Updated preview                              │
│                                                           │
│  4. SAVE                                                  │
│     "Perfect! Save this config"                           │
│     ↓                                                     │
│     Claude calls: save_config(draft_id)                   │
│     Saved to: configs/content/weekly-team-report.json     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Ephemeral Storage (30-Day Retention)

**Key Concepts:**
- **Drafts are temporary**: Stored in `ephemeral/drafts/` directory
- **30-day retention**: Automatically deleted after 30 days of inactivity
- **Safe experimentation**: Test ideas without cluttering your configs/ directory
- **No commitment**: Can abandon drafts without cleanup

---

## Part 2: Hands-On - Create Your First Conversational Config

Let's create a weekly team report config entirely through conversation.

### Step 1: Start Conversation with Claude Desktop

Open Claude Desktop and start a new conversation:

```
You: Create a content config for a weekly team report
```

**What Claude Does Behind the Scenes:**

Claude will call the `draft_config` tool with a structure like:

```json
{
  "config_type": "content",
  "config_data": {
    "id": "weekly-team-report",
    "generation": {
      "patterns": [{
        "type": "jinja2",
        "template": "team-report.md.jinja",
        "generation_config": {
          "context": {}
        }
      }]
    }
  },
  "description": "Weekly team report configuration"
}
```

**Expected Response:**

```
Claude: I've created a draft configuration for a weekly team report.

Draft ID: draft_8f3a2b1c
Config Type: content
Validation: ✅ Valid (passes JSON Schema v3.1)
Expires: November 15, 2025

The config is set up with:
- Jinja2 template generator
- Template file: team-report.md.jinja
- Basic structure ready for customization

Would you like me to:
1. Test this config with sample data to see what it generates?
2. Add specific sections (metrics, accomplishments, blockers)?
3. Configure context data sources?
```

**What Just Happened:**
- ✅ Config created in `ephemeral/drafts/content/draft_8f3a2b1c.json`
- ✅ Validated against JSON Schema
- ✅ Assigned unique draft_id for this session
- ✅ Set to expire in 30 days (auto-cleanup)

---

### Step 2: Test Your Draft Config

Let's see what this config would generate:

```
You: Test it with sample data for the Engineering team, week of Oct 16
```

**What Claude Does:**

Calls `test_config`:

```json
{
  "draft_id": "draft_8f3a2b1c",
  "context": {
    "team_name": "Engineering",
    "week": "2025-W42",
    "report_date": "October 16, 2025"
  }
}
```

**Expected Response:**

```
Claude: Here's a preview of what your config would generate:

─────────────────────────────────────────
# Engineering Team Weekly Report
Week of October 16, 2025

## This Week's Updates

[Content would appear here based on template]

## Metrics

[Metrics section - currently empty]

## Upcoming

[Upcoming items section]

─────────────────────────────────────────

Preview Stats:
- Generated: 342 characters
- Generator: jinja2
- Generation time: 145ms
- Warnings: None

The basic structure is working! Would you like to:
1. Add more sections (metrics, accomplishments, blockers)?
2. Customize the template styling?
3. Add data sources for automatic population?
```

**What Just Happened:**
- ✅ Generated preview without creating any files
- ✅ Used test context to simulate real generation
- ✅ Showed what output would look like
- ❌ No side effects (no files written to output/)

---

### Step 3: Iterate - Add Team Metrics Section

Let's improve the config by adding a metrics section:

```
You: Add a metrics section that shows:
- Pull requests merged
- Story points completed
- Bugs fixed
```

**What Claude Does:**

Calls `modify_config`:

```json
{
  "draft_id": "draft_8f3a2b1c",
  "updates": {
    "generation.patterns[0].generation_config.context": {
      "metrics": {
        "pull_requests": "{{ pr_count }}",
        "story_points": "{{ story_points }}",
        "bugs_fixed": "{{ bugs_fixed }}"
      }
    }
  }
}
```

Then immediately calls `test_config` again to show updated preview.

**Expected Response:**

```
Claude: I've updated the config to include metrics. Here's the new preview:

─────────────────────────────────────────
# Engineering Team Weekly Report
Week of October 16, 2025

## This Week's Updates

[Content]

## Metrics

- **Pull Requests Merged**: {{ pr_count }}
- **Story Points Completed**: {{ story_points }}
- **Bugs Fixed**: {{ bugs_fixed }}

## Upcoming

[Upcoming items]

─────────────────────────────────────────

Changes Made:
✅ Added metrics object to context
✅ Template now includes metrics section
✅ Variables ready for dynamic data

The metrics section is now included! Would you like to:
1. Add more metrics (deployment frequency, test coverage)?
2. Configure data sources to auto-populate these values?
3. Save this config and start using it?
```

**What Just Happened:**
- ✅ Modified draft config in ephemeral storage
- ✅ Draft_id remains the same (draft_8f3a2b1c)
- ✅ Previous version overwritten (no version history in drafts)
- ✅ New preview generated automatically

---

### Step 4: Iterate Again - Add Data Sources

Let's connect the metrics to real data sources:

```
You: Configure the metrics to pull from:
- GitHub API for PR count
- Jira API for story points
- GitHub Issues for bugs fixed
```

**What Claude Does:**

Calls `modify_config` with input source configuration:

```json
{
  "draft_id": "draft_8f3a2b1c",
  "updates": {
    "inputs": {
      "sources": [
        {
          "type": "external_api",
          "id": "github_prs",
          "endpoint": "https://api.github.com/repos/{org}/{repo}/pulls",
          "selector": "count"
        },
        {
          "type": "external_api",
          "id": "jira_points",
          "endpoint": "https://your-domain.atlassian.net/rest/api/3/search",
          "selector": "issues[*].fields.customfield_10016"
        }
      ]
    }
  }
}
```

**Expected Response:**

```
Claude: I've added data sources for automatic metric population.

Configuration added:
✅ GitHub API integration for PR count
✅ Jira API integration for story points
✅ GitHub Issues API for bug count

Note: You'll need to configure API credentials in your environment:
- GITHUB_TOKEN for GitHub API access
- JIRA_API_TOKEN for Jira API access

Would you like to:
1. Test with mock data to verify the structure?
2. Add error handling for API failures?
3. Save this config and set up credentials?
```

---

### Step 5: Final Test with Mock Data

Let's verify everything works:

```
You: Test it with mock data: 15 PRs, 34 story points, 8 bugs
```

**What Claude Does:**

```json
{
  "draft_id": "draft_8f3a2b1c",
  "context": {
    "team_name": "Engineering",
    "week": "2025-W42",
    "report_date": "October 16, 2025",
    "pr_count": 15,
    "story_points": 34,
    "bugs_fixed": 8
  }
}
```

**Expected Response:**

```
Claude: Here's the final preview with your mock data:

─────────────────────────────────────────
# Engineering Team Weekly Report
Week of October 16, 2025

## This Week's Updates

[Content sections]

## Metrics

- **Pull Requests Merged**: 15
- **Story Points Completed**: 34
- **Bugs Fixed**: 8

## Upcoming

[Upcoming items]

─────────────────────────────────────────

Perfect! Everything looks good. The config is ready to save.

Would you like me to save this to your configs/ directory?
```

---

### Step 6: Save Your Config

You're satisfied with the preview. Let's make it permanent:

```
You: Yes, save it
```

**What Claude Does:**

Calls `save_config`:

```json
{
  "draft_id": "draft_8f3a2b1c",
  "destination_path": "configs/content/weekly-team-report.json"
}
```

**Expected Response:**

```
Claude: ✅ Configuration saved successfully!

Saved to: configs/content/weekly-team-report.json
Config ID: weekly-team-report
Config Type: content

You can now use this config with:
- generate_content tool: generate_content("weekly-team-report", context={...})
- CLI: poetry run chora-compose generate --config weekly-team-report
- MCP: Call generate_content from any MCP client

The draft has been moved from ephemeral storage to your configs directory.
Next steps:
1. Create the template file: templates/team-report.md.jinja
2. Set up API credentials for data sources
3. Test generation with real data
```

**What Just Happened:**
- ✅ Config atomically copied from ephemeral/ to configs/content/
- ✅ Validated one final time before persistence
- ✅ Draft retained in ephemeral storage (for potential rollback)
- ✅ Ready to use in production workflows

---

## Part 3: Understanding What You Just Did

### Compare: Traditional vs Conversational

**Traditional Workflow (File-Based):**
```
1. Open VS Code / text editor                    (30 sec)
2. Create new file: configs/content/report.json  (15 sec)
3. Write JSON structure manually                 (5 min)
4. Save file                                     (5 sec)
5. Run generate command to test                  (10 sec)
6. Check output                                  (30 sec)
7. Find JSON syntax error                        (2 min)
8. Fix error, save                               (1 min)
9. Test again                                    (10 sec)
10. Repeat steps 7-9 until working               (5-10 min)

Total time: 20-30 minutes
Context switches: 6-8 (editor ↔ terminal ↔ output viewer)
```

**Conversational Workflow (What You Just Did):**
```
1. "Create a config for weekly reports"          (5 sec + 2 sec tool call)
2. "Test it with sample data"                    (5 sec + 1 sec tool call)
3. "Add metrics section"                         (5 sec + 2 sec tool call)
4. "Connect to GitHub and Jira APIs"             (10 sec + 2 sec tool call)
5. "Test with mock data"                         (5 sec + 1 sec tool call)
6. "Save it"                                     (2 sec + 1 sec tool call)

Total time: 5-10 minutes
Context switches: 0 (everything in Claude Desktop)
```

**Savings:**
- ⏱️ **Time**: 60-70% faster (20-30 min → 5-10 min)
- 🧠 **Context**: Zero IDE switching
- 🐛 **Errors**: Instant schema validation (no JSON syntax errors)
- 👁️ **Visibility**: See output preview before committing

---

### The Ephemeral Storage Advantage

**Why Drafts Are Stored Separately:**

```
Project Structure:
chora-compose/
├── configs/                    # ← Permanent, version controlled
│   ├── content/
│   │   └── weekly-team-report.json  # ← Saved here (Step 6)
│   └── artifact/
├── ephemeral/                  # ← Temporary, .gitignore'd
│   ├── drafts/
│   │   ├── content/
│   │   │   └── draft_8f3a2b1c.json  # ← Draft here (Steps 1-5)
│   │   └── artifact/
│   └── output/                 # ← Test generations
```

**Benefits:**

1. **Safe Experimentation**
   - Try ideas without committing
   - No git history pollution
   - Easy to abandon bad drafts

2. **Automatic Cleanup**
   - 30-day retention policy
   - No manual deletion needed
   - Reclaims disk space

3. **Separation of Concerns**
   - Drafts ≠ Production configs
   - Clear boundary between exploration and commitment
   - Version control only tracks finalized configs

---

## Part 4: Advanced Scenarios

### Scenario 1: Fix Validation Errors

What if your config has schema validation errors?

```
You: Create a config with context data from an external file
```

**Claude Might Encounter:**

```json
{
  "error": {
    "code": "SCHEMA_VALIDATION_ERROR",
    "message": "Config violates JSON Schema v3.1",
    "details": {
      "field": "inputs.sources[0].selector",
      "error": "Missing required field 'type'"
    }
  }
}
```

**Claude Would Respond:**

```
Claude: I encountered a validation error while creating the draft:

❌ Missing required field: inputs.sources[0].type

The schema requires that each input source specify a 'type' field.
Let me fix that and create the draft again...

[Claude automatically retries with correct schema]

✅ Draft created successfully with corrected structure!
```

**What You Learned:**
- Validation happens immediately on `draft_config`
- Errors are descriptive and actionable
- Claude can auto-correct common schema issues
- No invalid configs reach ephemeral storage

---

### Scenario 2: Compare Multiple Draft Approaches

You can create multiple drafts and compare:

```
You: Create two drafts:
1. Weekly report using Jinja2
2. Weekly report using demonstration generator
```

**Claude Would Create:**

```
Draft 1: draft_abc123 (Jinja2 approach)
- Uses template with dynamic variables
- Requires template file creation
- Flexible, powerful, complex

Draft 2: draft_def456 (Demonstration approach)
- Uses example_output field
- No template needed
- Simple, fast, limited

Would you like to test both and compare?
```

Then you can:
```
You: Test both with the same context
```

And see side-by-side previews to decide which approach fits better.

---

### Scenario 3: Recover from Mistakes

Made a change you regret?

```
You: Actually, remove the metrics section - go back to simple version
```

**Two Options:**

**Option A: Modify Current Draft**
```
Claude: I'll remove the metrics section from draft_8f3a2b1c

[Calls modify_config to remove metrics]

Done! The metrics section has been removed. Preview?
```

**Option B: Start Fresh**
```
Claude: Would you like me to:
1. Modify the current draft (draft_8f3a2b1c)?
2. Create a new draft from scratch?

If you choose (2), I can create a clean draft and you can compare.
```

**Note:** Drafts don't have version history. If you need to preserve previous states, create multiple drafts with different IDs.

---

## Part 5: Best Practices

### When to Use Conversational Config Creation

**✅ Great For:**
- **Learning**: Exploring config structure without reading docs
- **Prototyping**: Rapid iteration on config ideas
- **Simple Configs**: Content configs with 1-2 patterns
- **Collaboration**: Discussing config design with Claude
- **Non-Technical Users**: Team members without JSON experience

**❌ Not Ideal For:**
- **Complex Nested Structures**: Artifacts with 10+ sections (better in files)
- **Bulk Changes**: Updating 20 fields at once (file editing faster)
- **Git History**: When you need version control for drafts (save to filesystem)
- **Offline Work**: When you don't have internet access

**Hybrid Approach:**
```
1. Draft conversationally  (explore structure)
2. Save to filesystem     (persist)
3. Edit in IDE            (bulk refinements)
4. Commit to git          (version control)
```

---

### Managing Ephemeral Drafts

**View All Drafts:**
```
You: List all my draft configs
```

Claude will use filesystem access to show:
```
Active Drafts:
- draft_8f3a2b1c (content) - Created Oct 16, expires Nov 15
- draft_def456 (artifact) - Created Oct 14, expires Nov 13

You can test, modify, or save any of these drafts.
```

**Manual Cleanup:**
```
You: Delete draft_def456 - I don't need it anymore
```

Claude can use file operations to remove the draft.

**Automatic Cleanup:**
- Happens automatically after 30 days
- Uses `cleanup_ephemeral` tool (runs periodically)
- No action needed from you

---

### Testing Best Practices

**Always Test Before Saving:**
```
✅ Good workflow:
  draft_config → test_config → modify_config → test_config → save_config

❌ Risky workflow:
  draft_config → save_config (no testing!)
```

**Test with Realistic Data:**
```
✅ Use real-like context:
  {
    "team_name": "Engineering",
    "week": "2025-W42",
    "pr_count": 15,         # Realistic number
    "story_points": 34      # Realistic number
  }

❌ Avoid placeholder data:
  {
    "team_name": "Team",
    "week": "WEEK",
    "pr_count": 999,        # Unrealistic
    "story_points": 0       # Edge case, not typical
  }
```

**Test Edge Cases:**
```
You: Test with zero metrics (no PRs, no bugs, no points)
```

This reveals potential template issues (division by zero, empty sections, etc.)

---

## Part 6: Troubleshooting

### Issue: "Draft not found"

**Problem:**
```
You: Test draft_xyz789
```
```
Claude: ❌ Error: Draft draft_xyz789 not found

Possible reasons:
- Draft ID typo (check spelling)
- Draft expired (30-day retention)
- Draft was deleted
```

**Solution:**
```
You: List all drafts
```

Then use the correct draft_id from the list.

---

### Issue: "Schema validation failed"

**Problem:**
```
❌ Config violates JSON Schema v3.1
Field: generation.patterns[0].type
Error: Must be one of: jinja2, demonstration, template_fill
```

**What Went Wrong:**
Invalid generator type specified.

**Solution:**
Claude will typically auto-correct, but if not:
```
You: Fix the validation error - use jinja2 generator type
```

---

### Issue: "Template file not found" (during test)

**Problem:**
```
You: Test draft_abc123
```
```
⚠️ Warning: Template file 'team-report.md.jinja' not found
Preview cannot be generated without template.

Would you like me to:
1. Create a basic template structure?
2. Change to demonstration generator (no template needed)?
3. Skip testing until template exists?
```

**Solution (Option 1):**
```
You: Create a basic template
```

Claude can draft a template structure or guide you to create it.

---

### Issue: Test is slow (>5 seconds)

**Problem:**
Preview taking too long to generate.

**Possible Causes:**
- Large context data (MB+)
- Complex Jinja2 template with loops
- External API calls in data sources

**Solutions:**
```
1. Simplify context: Use smaller test dataset
2. Mock APIs: Test with static data first
3. Profile template: Identify slow Jinja2 operations
```

---

## Part 7: Next Steps

### What You've Learned

✅ **Conversational workflow**: draft → test → modify → save
✅ **Four config lifecycle tools**: When and how to use each
✅ **Ephemeral storage**: 30-day retention, safe experimentation
✅ **Iteration patterns**: Preview-driven refinement
✅ **Best practices**: When conversational beats file-based

---

### Recommended Next Tutorials

1. **[MCP Integration Deep Dive](../advanced/01-mcp-integration-deep-dive.md)**
   - Master all 17 MCP tools
   - Batch operations
   - Storage management

2. **[Dynamic Content with Jinja2](./01-dynamic-content-with-jinja2.md)**
   - Create templates for conversational configs
   - Template inheritance
   - Advanced Jinja2 patterns

3. **[Artifact Assembly](../getting-started/04-compose-your-first-artifact.md)**
   - Create artifact configs conversationally
   - Multi-section documents
   - Dependency management

---

### Practice Exercises

**Exercise 1: Simple Report Config**
Create a daily standup report config with:
- Team member name
- Yesterday's accomplishments (list)
- Today's plan (list)
- Blockers (optional)

**Exercise 2: Multi-Format Config**
Create a config that generates the same content in 3 formats:
- Markdown (for docs/)
- HTML (for web)
- Plain text (for email)

**Exercise 3: Data-Driven Config**
Create a config that pulls data from:
- GitHub API (recent commits)
- Current date/time (timestamp)
- Environment variables (team name)

---

## Summary

**What Makes Conversational Config Creation Powerful:**

1. **Zero IDE Context Switching**
   - Everything in Claude Desktop
   - No file juggling
   - Instant feedback

2. **Preview-Driven Development**
   - See output before committing
   - Test-driven config creation
   - Catch errors early

3. **Safe Experimentation**
   - Ephemeral storage for drafts
   - 30-day automatic cleanup
   - Easy to abandon ideas

4. **Accessibility**
   - Non-technical users can create configs
   - Natural language interface
   - No JSON syntax knowledge required

5. **Efficiency**
   - 60-70% time savings vs file-based
   - Automated validation
   - Intelligent error correction

**You're now ready to create configurations conversationally!**

---

**Questions?**
- See [How-To: Create Config Conversationally](../../how-to/configs/create-config-conversationally.md) for task-oriented guidance
- See [Explanation: Conversational Workflow Authoring](../../explanation/architecture/conversational-workflow-authoring.md) for architectural deep dive
- See [MCP Tool Reference](../../mcp/tool-reference.md) for complete tool documentation
