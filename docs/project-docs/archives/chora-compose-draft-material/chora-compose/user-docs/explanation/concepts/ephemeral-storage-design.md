# Explanation: Ephemeral Storage Design

**Diataxis Quadrant**: Explanation
**Purpose**: Understand the design rationale for 30-day ephemeral storage in conversational AI workflows

---

## Overview

chora-compose implements **ephemeral storage** with a **30-day retention policy** for generated content and artifacts. This design decision reflects a fundamental philosophical shift: from traditional **persistent automation** to **conversational, intent-driven workflows**.

This document explains:

- **Why ephemeral storage** exists (not just persistent files)
- **Why 30 days** (not 7, 90, or forever)
- **How it integrates** with MCP config lifecycle tools
- **What trade-offs** you accept when using ephemeral workflows
- **When to use** ephemeral vs persistent storage

---

## The Problem: Traditional Automation Assumes Permanence

### Traditional Workflow Pattern

Classic automation systems (Make, n8n, Zapier, cron jobs) assume:

1. **Inputs are persistent**: Files, databases, APIs
2. **Outputs are permanent**: Save to disk, commit to git, upload to S3
3. **Workflows are repeatable**: Same inputs → same outputs

**Example** (traditional documentation build):
```bash
# Inputs: Markdown files (persistent in git)
mkdocs build

# Outputs: HTML files (persistent in git or S3)
git add docs/
git commit -m "Update documentation"
```

### Why This Breaks with Conversational AI

Conversational AI workflows (Claude Code, ChatGPT, n8n with MCP) introduce **non-deterministic, intent-driven generation**:

1. **Inputs are conversational**: "Generate a report about last week's commits"
2. **Outputs are contextual**: The report is specific to *this conversation*
3. **Workflows are exploratory**: Same prompt ≠ same output (by design!)

**Example** (conversational workflow):
```
User: "Generate a daily standup report"
Claude: [Calls choracompose:generate_content, saves to ephemeral/]
User: "Actually, make it weekly"
Claude: [Regenerates, overwrites ephemeral file]
User: "Looks good, commit it to git"
Claude: [Copies from ephemeral/ to project/, commits]
```

**Problem**: If every exploratory generation is permanent, you pollute your file system with:
- Draft versions ("standup-v1.md", "standup-v2.md", "standup-final-FINAL.md")
- Abandoned experiments
- Intermediate outputs never meant for human review

---

## The Solution: Ephemeral Storage with 30-Day Retention

### Design Principles

1. **Conversational outputs are temporary by default**
   - Exploratory generations go to `ephemeral/`
   - Only deliberate saves go to persistent storage

2. **30-day retention balances convenience and cleanliness**
   - Long enough: Multi-day conversations, async reviews
   - Short enough: Automatic cleanup prevents accumulation

3. **Explicit promotion to persistence**
   - Use `choracompose:publish_config` to move from ephemeral → persistent
   - Git commit is the final "this is valuable" signal

4. **Tight integration with MCP lifecycle**
   - `draft_config` → `validate_config` → `publish_config` → `archive_config`
   - Ephemeral storage is the workspace for this lifecycle

---

## Why 30 Days? (Not 7, 90, or Forever)

### Rationale

| Duration | Pros | Cons | Use Case |
|----------|------|------|----------|
| **7 days** | Fast cleanup, minimal disk usage | Too short for async teams, interruptions | High-velocity teams, daily workflows |
| **30 days** ✅ | Spans sprint cycles, handles interruptions | Moderate disk usage | **Conversational workflows** |
| **90 days** | Covers quarterly planning | Accumulates unused files | Compliance, audit trails |
| **Forever** | Never lose anything | Disk bloat, git pollution | Traditional automation |

**Why chora-compose chose 30 days**:

1. **Aligns with sprint cycles**: Most Agile teams work in 2-week sprints
   - Generated drafts remain available through sprint planning → review → retro
   - Old sprints auto-clean after 2 cycles

2. **Handles interruptions gracefully**:
   - Friday experiment → Monday resume (within 3 days)
   - Pre-vacation draft → post-vacation review (within 2 weeks)
   - Monthly reports remain available for next month's comparison

3. **Balances disk usage**:
   - Typical usage: 100 MB/month of generated content
   - 30-day window: ~100 MB resident (not 1 GB+)

4. **Psychological clarity**:
   - "This month's work" is a natural mental model
   - Older content is assumed stale/irrelevant

### Adjustable via Configuration

You can override the default:

```json
{
  "ephemeral": {
    "retention_days": 7,  // Faster cleanup for high-velocity teams
    "max_size_mb": 500    // Or limit by size instead of time
  }
}
```

---

## How Ephemeral Storage Integrates with MCP

### The Config Lifecycle

chora-compose's MCP tools implement a **draft → validate → publish → archive** lifecycle:

```
┌─────────────────────────────────────────────────────────────┐
│ CONVERSATIONAL WORKFLOW LIFECYCLE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DRAFT (ephemeral/)                                      │
│     ├─ choracompose:draft_config                                   │
│     ├─ choracompose:generate_content   → ephemeral/outputs/       │
│     └─ Iterate, refine, experiment                          │
│                                                             │
│  2. VALIDATE (ephemeral/)                                   │
│     ├─ choracompose:validate_config                                │
│     ├─ choracompose:list_ephemeral                                 │
│     └─ Review outputs, check quality                        │
│                                                             │
│  3. PUBLISH (persistent configs/)                           │
│     ├─ choracompose:publish_config   → configs/                    │
│     ├─ Move from ephemeral/ to permanent storage            │
│     └─ Git commit (optional but recommended)                │
│                                                             │
│  4. ARCHIVE (optional, for historical configs)              │
│     ├─ choracompose:archive_config                                 │
│     └─ Preserve old versions without cluttering active set  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Example Workflow

**Scenario**: Creating a daily standup report configuration

```
# Phase 1: Draft (ephemeral)
User: "Draft a config for daily standup reports"
Claude: [Calls choracompose:draft_config]
  → ephemeral/configs/standup-report.json (created)

User: "Generate a test report"
Claude: [Calls choracompose:generate_content with ephemeral config]
  → ephemeral/outputs/standup-2025-10-21.md (created)

User: "Add a 'blockers' section"
Claude: [Edits ephemeral/configs/standup-report.json]

User: "Regenerate"
Claude: [Calls choracompose:generate_content]
  → ephemeral/outputs/standup-2025-10-21.md (overwritten)

# Phase 2: Validate
User: "Show me all my drafts"
Claude: [Calls choracompose:list_ephemeral]
  → Shows: standup-report.json (config), standup-2025-10-21.md (output)

User: "Validate the config"
Claude: [Calls choracompose:validate_config]
  → ✅ Config passes validation

# Phase 3: Publish (persistent)
User: "This looks good, publish it"
Claude: [Calls choracompose:publish_config]
  → configs/content/standup-report.json (created)
  → ephemeral/configs/standup-report.json (remains, will auto-clean in 30 days)

User: "Commit to git"
Claude: [Runs git add configs/ && git commit]
  → Permanent record in version control
```

**30 days later**:
- `ephemeral/configs/standup-report.json` → deleted (auto-cleanup)
- `ephemeral/outputs/standup-2025-10-21.md` → deleted (auto-cleanup)
- `configs/content/standup-report.json` → still exists (permanent)

---

## Trade-offs: Ephemeral vs Persistent Storage

### When to Use Ephemeral Storage

✅ **Use ephemeral/** when:

1. **Exploratory generation**: "Try this, see if it works"
2. **Draft configurations**: Iterating on templates, variables
3. **Throwaway outputs**: Test runs, debugging
4. **Conversational workflows**: AI-assisted content creation
5. **High-volume generation**: Daily reports that don't need long-term retention

**Examples**:
- "Generate 5 different versions of this README intro"
- "Draft a config for weekly newsletter"
- "Test this template with sample data"

### When to Use Persistent Storage

✅ **Use configs/** (persistent) when:

1. **Production configurations**: Configs used by automation
2. **Shared team resources**: Templates, shared configs
3. **Version-controlled content**: Docs, code, assets committed to git
4. **Long-term retention**: Compliance, audit trails
5. **Published artifacts**: Final deliverables for users/customers

**Examples**:
- Committed `README.md` in git
- Production API documentation config
- Shared team templates for onboarding docs

### Comparison Table

| Aspect | Ephemeral Storage | Persistent Storage |
|--------|-------------------|-------------------|
| **Location** | `ephemeral/` directory | `configs/`, `output/`, git-tracked files |
| **Retention** | 30 days (default) | Forever (until manually deleted) |
| **Use Case** | Drafts, experiments, conversational outputs | Production configs, final deliverables |
| **Git Tracking** | `.gitignore`'d (excluded) | Committed (tracked) |
| **Cleanup** | Automatic (cron, startup) | Manual (user-driven) |
| **MCP Tool** | `draft_config`, `generate_content` | `publish_config`, manual file ops |
| **Discoverability** | `choracompose:list_ephemeral` | File system, git log |

---

## Implementation Details

### Directory Structure

```
chora-compose/
├── ephemeral/               # 30-day retention
│   ├── configs/             # Draft configurations
│   │   └── *.json           # Work-in-progress configs
│   ├── outputs/             # Generated content
│   │   ├── *.md             # Markdown outputs
│   │   ├── *.py             # Generated code
│   │   └── *.txt            # Text artifacts
│   └── .ephemeral-metadata  # Cleanup tracking (timestamps)
│
├── configs/                 # Persistent configurations
│   ├── content/             # Published content configs
│   ├── artifact/            # Published artifact configs
│   └── templates/           # Reusable templates
│
└── output/                  # Persistent outputs (optional)
    └── *.md                 # Long-term generated files
```

### Cleanup Mechanism

**Two cleanup strategies**:

1. **Startup cleanup** (every server start):
   ```python
   # On chora-compose MCP server startup
   cleanup_ephemeral(retention_days=30)
   ```

2. **Scheduled cleanup** (optional cron):
   ```bash
   # Daily cleanup at 2 AM
   0 2 * * * cd /app && python -m chora_compose.cleanup_ephemeral
   ```

**How it works**:
- Scans `ephemeral/` directory
- Checks file modification time (`mtime`)
- Deletes files older than 30 days
- Logs cleanup actions to `ephemeral/.cleanup.log`

### Preventing Accidental Loss

**Safety mechanisms**:

1. **Clear separation**: `ephemeral/` vs `configs/` (different directories)
2. **Gitignore protection**: `ephemeral/` is never committed
3. **List before cleanup**: `choracompose:list_ephemeral` shows what will be deleted
4. **Manual export**: `choracompose:publish_config` promotes drafts to permanent
5. **Cleanup logs**: Track what was deleted and when

**Disaster recovery**:
```bash
# If you need to disable cleanup temporarily
export EPHEMERAL_CLEANUP_DISABLED=true

# Or extend retention for this project
export EPHEMERAL_RETENTION_DAYS=90
```

---

## Real-World Scenarios

### Scenario 1: Daily Report Generation

**Context**: Generate daily standup reports, keep for 7 days, discard old ones

**Workflow**:
```
Day 1: choracompose:generate_content → ephemeral/outputs/standup-2025-10-21.md
Day 2: choracompose:generate_content → ephemeral/outputs/standup-2025-10-22.md
...
Day 30: Auto-cleanup deletes standup-2025-10-21.md
```

**Why ephemeral?**
- Reports are time-sensitive (only useful for a few days)
- No need to pollute git with 365 standup files/year
- Automatic cleanup prevents manual housekeeping

### Scenario 2: Iterative Documentation Drafting

**Context**: Draft new API documentation, iterate 10 times, publish final version

**Workflow**:
```
Iteration 1-9: Edit ephemeral/configs/api-docs.json
             → Generate to ephemeral/outputs/api-v1.md, api-v2.md, ...
Iteration 10: Satisfied with api-v10.md
             → choracompose:publish_config → configs/content/api-docs.json
             → Copy api-v10.md to docs/api.md
             → git commit -m "Add API documentation"
```

**Why ephemeral?**
- 9 draft versions are noise (not valuable long-term)
- Only final version (v10) goes to git
- Ephemeral storage is the "workspace" for iteration

### Scenario 3: Multi-Person Collaboration

**Context**: Alice drafts config Monday, Bob reviews Friday (4 days later)

**Timeline**:
```
Monday:
  Alice: "Draft newsletter config"
       → ephemeral/configs/newsletter.json (created)

Friday:
  Bob: "Show me Alice's drafts"
     → choracompose:list_ephemeral
     → Sees: newsletter.json (age: 4 days, safe!)

  Bob: "Validate and publish Alice's newsletter config"
     → choracompose:publish_config
     → configs/content/newsletter.json (permanent)
```

**Why 30 days works**:
- 4-day delay is well within 30-day window
- Even 2-week sprint + 1-week vacation = 21 days (safe)
- Automatic cleanup doesn't interfere with async collaboration

---

## Philosophical Alignment: Conversational Workflows

### The Shift: From Scripts to Conversations

**Traditional scripting**:
```python
# write_report.py (deterministic, repeatable)
def generate_report(date):
    commits = get_commits(date)
    return render_template("report.j2", commits=commits)

# Run daily via cron
generate_report("2025-10-21")  # Same inputs → same output
```

**Conversational workflows**:
```
User: "Generate a report about last week's work"
Claude: [Interprets "last week", calls tools, generates]
      → Different interpretation, different output each time!

User: "Make it more concise"
Claude: [Regenerates with different approach]
      → Iterative refinement, not deterministic pipeline
```

### Why Ephemeral Storage Enables Conversations

Conversational workflows are:

1. **Non-deterministic**: Same prompt ≠ same output
2. **Iterative**: Multiple refinement cycles expected
3. **Exploratory**: "Try this, see if it works" mindset
4. **Intent-driven**: Human steers, AI executes

**Ephemeral storage supports this** by:
- Removing "file naming" burden ("Do I call this v1, v2, draft, final?")
- Enabling fearless iteration (overwrite without guilt)
- Auto-cleaning failed experiments (no manual housekeeping)
- Signaling intent (ephemeral = exploration, persistent = decision)

---

## Integration with MCP Config Lifecycle Tools

### MCP Tools Overview

chora-compose provides **4 config lifecycle tools**:

| Tool | Purpose | Storage Target |
|------|---------|---------------|
| `choracompose:draft_config` | Create work-in-progress config | `ephemeral/configs/` |
| `choracompose:validate_config` | Check config correctness | Reads from ephemeral or persistent |
| `choracompose:publish_config` | Promote draft to production | Copies ephemeral → `configs/` |
| `choracompose:archive_config` | Preserve old versions | Moves configs → `configs/archived/` |

### Lifecycle Flow

```
┌──────────────┐
│ USER INTENT  │ "I want to create a newsletter config"
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ DRAFT        │ choracompose:draft_config
│ (ephemeral)  │ → ephemeral/configs/newsletter.json
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ITERATE      │ Edit, test, regenerate
│ (ephemeral)  │ → ephemeral/outputs/newsletter-test.md
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ VALIDATE     │ choracompose:validate_config
│              │ → Check schema, required fields
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ PUBLISH      │ choracompose:publish_config
│ (persistent) │ → configs/content/newsletter.json
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ GIT COMMIT   │ git add configs/ && git commit
│              │ → Permanent version control
└──────────────┘
```

**Key insight**: Ephemeral storage is the **workspace** for the lifecycle. Only the `publish` step promotes content to permanence.

---

## When Ephemeral Storage is NOT Appropriate

### Anti-Patterns

❌ **Don't use ephemeral/** for:

1. **Production automation outputs**
   - Bad: Daily reports for compliance (need long-term retention)
   - Good: Exploratory reports during development

2. **Shared team resources**
   - Bad: Team-wide templates (could be deleted mid-sprint)
   - Good: Personal draft templates before sharing

3. **Customer-facing deliverables**
   - Bad: Generated API docs published to website (could vanish!)
   - Good: Draft versions of API docs before publishing

4. **Audit trails**
   - Bad: Historical records required by compliance
   - Good: Temporary debug logs during troubleshooting

### Migration Path

If you discover ephemeral content should be permanent:

```bash
# Manually copy from ephemeral to persistent
cp ephemeral/outputs/important-report.md docs/reports/

# Or use MCP tool
choracompose:publish_config --source ephemeral/configs/important.json

# Then commit to git
git add docs/reports/important-report.md
git commit -m "Preserve important report"
```

---

## Comparison: Other Tools & Approaches

### How Other Tools Handle Temporary Content

| Tool | Temporary Storage | Retention Policy |
|------|------------------|------------------|
| **Make/Zapier** | None (all outputs permanent) | Forever |
| **n8n** | Execution data (JSON only) | 7-168 days (configurable) |
| **GitHub Actions** | Artifacts | 90 days (default) |
| **Docker** | Container layers | Manual cleanup (`docker system prune`) |
| **chora-compose** | `ephemeral/` directory | **30 days** |

**Key difference**: chora-compose's ephemeral storage is **file-based** (not just execution logs), enabling:
- Human-readable drafts (Markdown, code)
- Multi-day iteration across conversations
- Explicit promotion to permanence (`publish_config`)

---

## Advanced: Customizing Retention

### Configuration Options

Override defaults in `configs/settings.json`:

```json
{
  "ephemeral": {
    "retention_days": 14,        // Shorter retention for high-velocity teams
    "max_size_mb": 1000,         // Size-based limit (alternative to time)
    "cleanup_schedule": "daily", // "startup", "daily", "weekly", "manual"
    "excluded_patterns": [
      "*.important.md",          // Never auto-delete files matching pattern
      "configs/keep-*.json"
    ]
  }
}
```

### Environment Variables

```bash
# Override retention for this session
export EPHEMERAL_RETENTION_DAYS=7

# Disable cleanup entirely (for debugging)
export EPHEMERAL_CLEANUP_DISABLED=true

# Change cleanup schedule
export EPHEMERAL_CLEANUP_SCHEDULE=weekly
```

### Manual Cleanup

```bash
# Force cleanup now (respects retention policy)
just cleanup-ephemeral

# Nuclear option: delete ALL ephemeral content
just cleanup-ephemeral-all  # Prompts for confirmation
```

---

## Conclusion

Ephemeral storage with 30-day retention is a **deliberate design choice** that enables:

1. **Conversational workflows**: Fearless iteration without file naming burden
2. **Automatic housekeeping**: No manual cleanup of abandoned drafts
3. **Clear intent signaling**: Ephemeral = exploration, persistent = decision
4. **MCP lifecycle integration**: Draft → validate → publish → archive

**Key takeaway**: Ephemeral storage is not just "temporary files" — it's the **workspace for conversational AI workflows**, where exploration happens before commitment.

**When in doubt**:
- Start in `ephemeral/` (you can always promote to persistent)
- Use `choracompose:publish_config` when satisfied
- Trust the 30-day window (longer than most workflows need)

---

## Related Documentation

**Diataxis References**:
- [How-To: Use Ephemeral Storage](../../how-to/workflows/use-ephemeral-storage.md) - Practical workflows
- [Tutorial: Your First Config Lifecycle](../../tutorials/intermediate/02-config-lifecycle.md) - Hands-on practice
- [Reference: MCP Config Lifecycle Tools](../../reference/mcp/config-lifecycle-tools.md) - API specifications

**Conceptual Relationships**:
- [Explanation: Human-AI Collaboration Philosophy](human-ai-collaboration-philosophy.md) - Why conversational workflows
- [Explanation: Configuration-Driven Development](configuration-driven-development.md) - CDD philosophy
- [Explanation: MCP Workflow Model](../integration/mcp-workflow-model.md) - How MCP enables workflows

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
