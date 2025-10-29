# Agentic Workflow: End-to-End Content Generation with Claude Code

**Type:** Tutorial (Learning-Oriented)
**Level:** Advanced
**Duration:** ~50 minutes
**Prerequisites:**
- [Installation Tutorial](../getting-started/01-installation.md) completed
- [Your First Config](../getting-started/02-your-first-config.md) completed
- [MCP Integration Deep Dive](01-mcp-integration-deep-dive.md) completed
- Claude Code with MCP server configured

---

## What You'll Learn

This tutorial demonstrates the complete agentic workflow for creating, testing, and generating content using conversational AI through MCP (Model Context Protocol). You'll learn to:

1. ✅ Discover MCP capabilities dynamically
2. ✅ Create configs conversationally (no manual JSON editing)
3. ✅ Test before committing (zero-friction experimentation)
4. ✅ Generate and assemble content through conversation
5. ✅ Manage memory and context effectively
6. ✅ Apply agentic best practices (autonomy, tool use, self-correction)

**Why This Matters:**
- Traditional workflow: Write JSON manually → Generate → Debug → Repeat
- Agentic workflow: Describe what you need → AI drafts → Test → Refine → Done
- **10x faster** config creation through conversation
- **Zero context switching** - stay in your IDE/chat interface
- **Immediate feedback** - test before committing changes

---

## Prerequisites Check

Before starting, verify your MCP server is running:

```bash
# Check if server is running
ps aux | grep "chora-compose"

# Or start it manually
poetry run python -m chora_compose.mcp.server
```

**Expected Output:**
```
MCP server running on stdio
Server version: 1.1.0
Tools: 17, Resources: 5
```

---

## Step 1: Discovery - Understanding Available Capabilities

**Goal:** Learn what the MCP server can do without reading documentation.

### Use Capability Discovery

In your Claude Code chat or MCP client, ask:

```
What capabilities does the Chora Compose MCP server have?
```

**The agent will:**
1. Call `capabilities://server` resource
2. Call `capabilities://tools` resource
3. Summarize available features

**Expected Response Summary:**
```
The Chora Compose MCP server (v1.1.0) provides:

SERVER CAPABILITIES:
- 17 MCP tools for content generation
- 5 resource URI families (config://, capabilities://, generator://)
- Ephemeral storage with 30-day retention
- Plugin-aware generator registry

KEY TOOLS FOR WORKFLOW:
- draft_config: Create temporary configs
- test_config: Preview generation output
- modify_config: Update drafts iteratively
- save_config: Persist to filesystem
- generate_content: Generate from saved configs
- assemble_artifact: Compose final artifacts

AVAILABLE GENERATORS:
- jinja2: Template-based generation
- demonstration: Example-driven generation
- (+ any installed plugins)
```

**Key Insight:** The agent discovers capabilities dynamically. No hardcoded knowledge needed.

**Time:** ~5 minutes

---

## Step 2: Conversational Config Creation

**Goal:** Create a content config through conversation, not manual JSON editing.

### Describe What You Need

In Claude Code, describe your content generation goal:

```
I need to create a content config for generating a team status update.
The status update should include:
- Team name and date
- List of completed tasks (with descriptions)
- List of in-progress tasks (with assigned members)
- Blockers or challenges
- Next week's priorities

Use the demonstration generator with a clear example.
The output should be Markdown format.
```

**The agent will:**
1. Understand your requirements
2. Use `draft_config` tool to create temporary config
3. Generate appropriate config structure
4. Store in ephemeral storage (auto-cleanup after 30 days)

**Agent Response Example:**
```
I've created a draft content config for your team status update.

Draft ID: team-status-update
Location: ephemeral/drafts/content/team-status-update.json
Status: Draft (not yet saved to filesystem)

The config uses the demonstration generator with an example that includes:
- Team name and date placeholders
- Completed tasks with descriptions
- In-progress tasks with assignees
- Blockers section
- Priorities for next week

Would you like to test this config to see sample output?
```

**What Happened:**
- ✅ No manual JSON editing required
- ✅ Config stored in ephemeral storage (safe to experiment)
- ✅ Agent understood natural language requirements
- ✅ Appropriate generator selected (demonstration)

**Time:** ~10 minutes

---

## Step 3: Testing Before Committing

**Goal:** Preview generation output without side effects.

### Use test_config

Ask the agent:

```
Yes, please test the config with sample data to show me what the
output will look like.
```

**The agent will:**
1. Use `test_config` tool with the draft config
2. Provide sample context data
3. Generate preview output
4. Show you the result

**Agent Response Example:**
```
Here's a preview of the generated team status update:

---

# Team Alpha - Status Update
**Week of:** October 17, 2025

## ✅ Completed This Week

- **User Authentication Refactor**
  Migrated from session-based to JWT authentication. All tests passing.

- **API Rate Limiting**
  Implemented rate limiting middleware. Deployed to staging.

## 🔄 In Progress

- **Dashboard Redesign** (Sarah)
  Wireframes complete, starting implementation this week.

- **Database Migration** (Alex, Jordan)
  Schema changes ready, planning migration window.

## 🚧 Blockers

- Waiting for design approval on dashboard colors
- Need DevOps support for database migration scheduling

## 📋 Next Week's Priorities

1. Complete dashboard implementation
2. Execute database migration
3. Start performance optimization work

---

Does this format meet your needs? I can modify the config if you'd like
changes to the structure or content.
```

**What Happened:**
- ✅ Preview generated without creating files
- ✅ No filesystem changes (test-before-persist pattern)
- ✅ Agent can iterate based on your feedback
- ✅ Safe experimentation

**Time:** ~5 minutes

---

## Step 4: Refinement Through Conversation

**Goal:** Iterate on the config based on feedback.

### Request Modifications

Say:

```
This looks good, but can you add a section for "Team Metrics" that
shows the number of PRs merged, issues closed, and test coverage?
Also, use emoji indicators (🎯 for priorities, 📊 for metrics).
```

**The agent will:**
1. Use `modify_config` tool to update the draft
2. Add new sections
3. Update formatting
4. Test again automatically

**Agent Response Example:**
```
I've updated the config with:
- New "Team Metrics" section with PR count, issues closed, coverage
- Emoji indicators throughout (🎯 for priorities, 📊 for metrics)
- Enhanced demonstration example

Here's the updated preview:

---

# Team Alpha - Status Update
**Week of:** October 17, 2025

## 📊 Team Metrics

- **PRs Merged:** 12
- **Issues Closed:** 8
- **Test Coverage:** 94%

## ✅ Completed This Week
...
(rest of content with emoji indicators)

## 🎯 Next Week's Priorities

1. Complete dashboard implementation
2. Execute database migration
3. Start performance optimization work

---

The draft has been updated. Would you like to save this to the
filesystem, or make more changes?
```

**What Happened:**
- ✅ Iterative refinement through conversation
- ✅ Agent modified config based on natural language feedback
- ✅ Automatic re-testing to show updated output
- ✅ Fast iteration cycle (no manual file editing)

**Time:** ~5 minutes

---

## Step 5: Persistence to Filesystem

**Goal:** Save the validated draft to a permanent location.

### Save the Config

Confirm you're ready:

```
Perfect! Please save this config to configs/content/team-status-update.json
```

**The agent will:**
1. Use `save_config` tool
2. Validate config against JSON Schema v3.1
3. Write to filesystem at specified path
4. Confirm success

**Agent Response Example:**
```
✅ Config saved successfully!

Location: configs/content/team-status-update.json
Type: content
Generator: demonstration
Schema: v3.1 (validated)

The config is now ready to use for generation. You can:
- Generate content: Use the generate_content MCP tool
- Manual generation: poetry run python scripts/generate.py
- Include in artifact: Reference in artifact config

Next step: Generate your first team status update?
```

**What Happened:**
- ✅ Draft promoted to permanent config
- ✅ Schema validation ensured correctness
- ✅ Filesystem write confirmed
- ✅ Ready for production use

**Time:** ~5 minutes

---

## Step 6: Content Generation

**Goal:** Generate actual content from the saved config.

### Generate Content

Request generation:

```
Yes, generate a team status update using this config.
Use the following context:
- Team: Platform Engineering
- Date: October 17, 2025
- Completed: ["API Gateway v2 deployment", "Monitoring dashboard launch"]
- In Progress: ["Kubernetes upgrade", "Log aggregation pipeline"]
- Blockers: ["Waiting for security review"]
- Metrics: {prs: 15, issues: 10, coverage: "96%"}
```

**The agent will:**
1. Use `generate_content` tool
2. Pass your context data
3. Generate content using the demonstration generator
4. Store in ephemeral storage
5. Return the generated output

**Agent Response Example:**
```
✅ Content generated successfully!

Content ID: team-status-update
Output stored: ephemeral/content/team-status-update/v1.md
Generator: demonstration
Generated at: 2025-10-17 14:23:45 UTC

---

# Platform Engineering - Status Update
**Week of:** October 17, 2025

## 📊 Team Metrics

- **PRs Merged:** 15
- **Issues Closed:** 10
- **Test Coverage:** 96%

## ✅ Completed This Week

- **API Gateway v2 Deployment**
  Successfully deployed new API gateway with improved performance and routing.

- **Monitoring Dashboard Launch**
  New monitoring dashboard live with real-time metrics and alerts.

## 🔄 In Progress

- **Kubernetes Upgrade**
  Planning migration to v1.28, currently testing in staging.

- **Log Aggregation Pipeline**
  Implementing centralized logging with Elasticsearch backend.

## 🚧 Blockers

- Waiting for security review of API Gateway v2 configuration

## 🎯 Next Week's Priorities

1. Complete Kubernetes upgrade in production
2. Finalize log aggregation pipeline
3. Begin performance optimization work

---

The generated content is stored in ephemeral storage (30-day retention).
Would you like to assemble this into a final artifact or export it?
```

**What Happened:**
- ✅ Content generated from config + context
- ✅ Demonstration generator used example to format output
- ✅ Stored in ephemeral storage (versioned, retained 30 days)
- ✅ Production-ready output

**Time:** ~5 minutes

---

## Step 7: Artifact Assembly (Optional)

**Goal:** Compose multiple content pieces into a final artifact.

### Create Artifact Config

If you want to assemble multiple pieces (e.g., status update + changelog + metrics report):

```
Create an artifact config that assembles:
1. This team status update
2. A weekly metrics summary
3. Top 3 highlights

Output as a single Markdown file.
```

**The agent will:**
1. Use `draft_config` with type "artifact"
2. Define dependencies on content configs
3. Specify assembly order
4. Save artifact config

**Then assemble:**

```
Assemble the weekly team report artifact.
```

**Agent Response Example:**
```
✅ Artifact assembled successfully!

Artifact ID: weekly-team-report
Output: ephemeral/artifacts/weekly-team-report/v1.md
Components assembled:
  1. team-status-update (content)
  2. metrics-summary (content)
  3. highlights (content)

Size: 2,459 bytes
Format: Markdown

The final report combines all components in a cohesive document.
Export to artifacts/ directory or use as-is from ephemeral storage.
```

**What Happened:**
- ✅ Multiple content pieces composed
- ✅ Artifact config managed assembly order
- ✅ Single output file created
- ✅ Ready for distribution

**Time:** ~5 minutes

---

## Step 8: Memory Management Best Practices

**Goal:** Maintain context across workflow steps effectively.

### Understanding Agent Memory

**Three Memory Layers:**

1. **Session Memory** (Claude Code conversation)
   - Lasts for current chat session
   - Includes draft IDs, config names, context
   - Lost when session ends

2. **Ephemeral Storage** (Chora Compose)
   - Drafts: 30-day retention in `ephemeral/drafts/`
   - Generated content: 30-day retention in `ephemeral/content/`
   - Survives session restarts

3. **Permanent Storage** (Filesystem)
   - Saved configs: `configs/content/`, `configs/artifacts/`
   - Persists indefinitely
   - Version controlled (git)

### Best Practices

**✅ DO:**
- Reference draft IDs in conversation ("modify draft: team-status-update")
- Test configs before saving to filesystem
- Use ephemeral storage for experimentation
- Save configs when ready for production use
- Include context in generation requests

**❌ DON'T:**
- Assume agent remembers drafts across sessions (use draft IDs explicitly)
- Save untested configs to filesystem
- Hardcode data in configs (use context variables instead)
- Skip testing step (test-before-persist is key)

### Memory Optimization Strategies

**For Long Conversations:**
```
Summarize our current state:
- Draft configs created
- Configs saved to filesystem
- Generated content IDs
- Next steps
```

**For Session Continuity:**
```
I'm continuing from a previous session. Here's what I had:
- Config: team-status-update.json (saved to filesystem)
- Last generated: ephemeral/content/team-status-update/v1.md
- Need to: Generate v2 with updated metrics
```

**For Cross-Session Work:**
```
List all my draft configs in ephemeral storage.
```

**The agent will query ephemeral storage and report what's available.**

**Time:** ~5 minutes

---

## Summary: The Agentic Workflow

### Traditional Workflow

```
1. Manually write JSON config (15-30 min)
2. Debug schema errors (5-10 min)
3. Run generation script (2 min)
4. Review output, find issues (5 min)
5. Edit JSON config (10 min)
6. Repeat steps 3-5 until satisfied (20-30 min)

Total: 60-90 minutes per config
```

### Agentic Workflow

```
1. Describe what you need in conversation (2 min)
2. Agent drafts config (1 min)
3. Test and preview output (2 min)
4. Refine through conversation (5 min)
5. Save validated config (1 min)
6. Generate final content (2 min)

Total: 13-15 minutes per config
```

**Speedup: 5-6x faster**

### Key Principles Applied

✅ **Autonomy:** Agent makes decisions on config structure, generator selection
✅ **Tool Use:** Uses draft_config, test_config, modify_config, save_config, generate_content
✅ **Multi-Step Reasoning:** Breaks "create config" into draft → test → refine → save
✅ **Self-Correction:** Tests output, identifies issues, refines automatically

---

## Next Steps

### Practice Exercises

1. **Create a Changelog Config**
   - Use `draft_config` to create a changelog generator
   - Test with sample release data
   - Refine formatting based on Keep a Changelog spec
   - Save and generate your project's changelog

2. **Build a Multi-Artifact Workflow**
   - Create 3 content configs (README, CHANGELOG, API docs)
   - Create 1 artifact config assembling all three
   - Generate and assemble through conversation

3. **Implement Memory Persistence**
   - Start a workflow in one session
   - Close Claude Code
   - Resume in a new session using draft IDs
   - Complete the workflow

### Advanced Topics

- **[MCP Integration Deep Dive](01-mcp-integration-deep-dive.md)** - Detailed MCP internals
- **[AGENTS.md](../../../AGENTS.md)** - Complete agent instructions
- **[AGENT_BEST_PRACTICES.md](../../../dev-docs/process/AGENT_BEST_PRACTICES.md)** - Research-backed practices

### Reference Documentation

- **[MCP Tool Reference](../../reference/mcp/tool-reference.md)** - All 17 MCP tools
- **[Capability Discovery API](../../reference/api/resources/capabilities.md)** - Discovery resources
- **[Config Lifecycle Tools](../../how-to/mcp/create-configs-conversationally.md)** - How-to guide

---

## Troubleshooting

### Issue: "Draft not found"

**Symptom:** Agent says "draft with ID 'X' not found"

**Cause:** Draft may have expired (30-day retention) or was never created

**Solution:**
```
List all draft configs in ephemeral storage.
```

Then use the correct draft ID or create a new one.

---

### Issue: "Schema validation failed"

**Symptom:** `save_config` fails with validation error

**Cause:** Config structure doesn't match JSON Schema v3.1

**Solution:**
```
Show me the validation errors for draft: my-config.
Suggest fixes for the validation errors.
```

Agent will diagnose and propose corrections.

---

### Issue: "Generation failed - generator not found"

**Symptom:** `generate_content` fails with "generator 'X' not registered"

**Cause:** Generator type doesn't exist or plugin not installed

**Solution:**
```
What generators are available in the registry?
```

Use one of the available generators (jinja2, demonstration) or install required plugin.

---

### Issue: "Context variable not found"

**Symptom:** Generated content shows "{{variable_name}}" instead of value

**Cause:** Context data not provided or variable name mismatch

**Solution:**
```
Show me what context variables are required for config: my-config.
```

Provide all required context in the `generate_content` call.

---

## Conclusion

You've learned the complete agentic workflow for content generation:

1. ✅ **Discovery** - Capabilities exploration without documentation
2. ✅ **Drafting** - Conversational config creation
3. ✅ **Testing** - Preview before persistence
4. ✅ **Refinement** - Iterative improvement
5. ✅ **Persistence** - Save validated configs
6. ✅ **Generation** - Produce final content
7. ✅ **Assembly** - Compose multi-part artifacts
8. ✅ **Memory** - Effective context management

**Key Takeaway:** The agentic workflow transforms content generation from a manual, error-prone process into a conversational, iterative, and autonomous workflow. By leveraging AI agent capabilities, you focus on **what** you need, not **how** to configure it.

**Time Saved:** 5-6x faster than traditional JSON editing workflow

**Quality Improved:** Immediate testing and refinement reduce errors

**Experience Enhanced:** Stay in conversation flow, no context switching

---

**Version:** Chora Compose v1.1.0
**Last Updated:** 2025-10-17
**Tutorial Type:** Advanced (Learning-Oriented)
**Diátaxis Framework:** [Tutorial Quadrant](https://diataxis.fr/tutorials/)
