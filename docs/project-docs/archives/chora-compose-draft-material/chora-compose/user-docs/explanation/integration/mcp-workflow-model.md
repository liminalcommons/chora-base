# Explanation: MCP Workflow Model

**Diataxis Quadrant**: Explanation
**Purpose**: Understand how MCP (Model Context Protocol) enables conversational workflows in chora-compose

---

## Overview

The **Model Context Protocol (MCP)** is an open protocol that standardizes how AI assistants (Claude, ChatGPT, etc.) interact with tools and data sources. chora-compose implements MCP to transform traditional automation into **conversational, AI-driven workflows**.

This document explains:

- **What MCP is** and why it matters
- **How chora-compose uses MCP** (tools vs resources)
- **Why MCP enables conversational workflows** (vs traditional APIs)
- **What patterns** chora-compose implements (resource-based, tool-based, capability discovery)
- **How MCP integrates** with ephemeral storage and config lifecycle

---

## What is MCP?

### The Problem MCP Solves

**Before MCP**, every AI platform had custom integrations:

```
Claude Desktop → Custom Claude Tools API
ChatGPT       → Custom OpenAI Plugins API
n8n           → Custom n8n Nodes API
Zapier        → Custom Zapier Actions API
```

**Result**: Developers write 4+ integrations for the same functionality.

**With MCP**, there's one standard protocol:

```
Claude Desktop ──┐
ChatGPT         ─┼──→ MCP Server (chora-compose) ──→ Tools & Resources
n8n             ─┤
Zapier          ─┘
```

**Result**: Write once, run everywhere (that supports MCP).

### MCP Key Concepts

MCP defines three primitives:

1. **Tools**: Functions AI can call (e.g., `generate_content`, `validate_config`)
2. **Resources**: Structured data AI can read (e.g., config files, templates)
3. **Prompts**: Pre-defined prompts AI can use (e.g., "Generate API docs")

**chora-compose focuses on**: Tools (17 total) + Resources (configs, templates)

---

## chora-compose's MCP Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ AI ASSISTANT (Claude, ChatGPT, n8n)                         │
│  - Interprets user intent                                   │
│  - Discovers available tools via MCP                        │
│  - Calls tools with natural language context               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ MCP Protocol (SSE, stdio)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ MCP SERVER (chora-compose)                                  │
│  - Exposes 17 tools (13 content + 4 config lifecycle)      │
│  - Exposes resources (configs, templates, capabilities)     │
│  - Validates inputs, handles errors                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ Python API
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ CHORA-COMPOSE CORE                                          │
│  - Generators (jinja2, code_generation, etc.)               │
│  - Config management (draft, validate, publish, archive)    │
│  - Ephemeral storage (30-day retention)                     │
│  - Artifact assembly (multi-part compositions)              │
└─────────────────────────────────────────────────────────────┘
```

### Transport Options

chora-compose supports two MCP transports:

1. **stdio** (default for Claude Desktop):
   ```json
   {
     "transport": "stdio",
     "command": "chora-compose"
   }
   ```

2. **SSE** (Server-Sent Events, for HTTP clients like n8n):
   ```json
   {
     "transport": "sse",
     "url": "http://localhost:8000/sse"
   }
   ```

**Why two transports?**
- **stdio**: Tight integration with desktop apps (Claude Desktop)
- **SSE**: Network-accessible for web apps, automation (n8n, Make)

---

## MCP Tools in chora-compose

### The 17 Tools

chora-compose exposes **17 MCP tools** divided into two categories:

#### Content Generation Tools (13 total)

| Tool | Purpose | Example |
|------|---------|---------|
| `choracompose:generate_content` | Generate single content piece | Daily report, README intro |
| `choracompose:assemble_artifact` | Compose multi-part artifact | Full documentation suite |
| `choracompose:list_generators` | Discover available generators | See jinja2, code_generation, etc. |
| `choracompose:list_content_configs` | List available content configs | Show all configs in `configs/content/` |
| `choracompose:list_artifact_configs` | List available artifact configs | Show all configs in `configs/artifact/` |
| `choracompose:get_config` | Read specific config file | Fetch `newsletter.json` |
| `choracompose:list_capabilities` | Show system capabilities | Generators, features, limits |
| `choracompose:list_ephemeral` | List ephemeral drafts | Show work-in-progress files |
| `choracompose:cleanup_ephemeral` | Delete old ephemeral files | Remove files > 30 days |
| `choracompose:get_content_output` | Retrieve generated content | Fetch generated report |
| `choracompose:list_templates` | Show available templates | List Jinja2 templates |
| `choracompose:preview_template` | Render template preview | Test template with sample data |
| `choracompose:get_generation_metadata` | Get generation details | Timing, tokens, generator used |

#### Config Lifecycle Tools (4 total)

| Tool | Purpose | Example |
|------|---------|---------|
| `choracompose:draft_config` | Create draft config in ephemeral/ | Draft newsletter config |
| `choracompose:validate_config` | Check config correctness | Validate schema, required fields |
| `choracompose:publish_config` | Promote ephemeral → persistent | Move draft to `configs/` |
| `choracompose:archive_config` | Preserve old config versions | Archive deprecated config |

### Tool Design Philosophy

**Principle**: Tools should map to **user intent**, not implementation details.

**Good** (intent-based):
- `choracompose:generate_content` (user wants: content)
- `choracompose:draft_config` (user wants: draft a config)

**Bad** (implementation-based):
- `choracompose:call_jinja2_with_template` (too specific)
- `choracompose:write_json_file` (too low-level)

**Why?** AI assistants translate user intent → tool calls. Intent-based tools are easier to map from natural language.

---

## Resource-Based Pattern

### MCP Resources

MCP **resources** are structured data AI can read (but not write):

```
Resource URI: choracompose://configs/content/newsletter.json

Content:
{
  "metadata": {
    "id": "newsletter",
    "title": "Weekly Newsletter"
  },
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/newsletter.j2",
      ...
    }
  }
}
```

### chora-compose Resources

chora-compose exposes:

1. **Config files**: `choracompose://configs/content/*.json`, `choracompose://configs/artifact/*.json`
2. **Templates**: `choracompose://templates/*.j2`
3. **Capabilities**: `choracompose://capabilities` (system info)
4. **Ephemeral files**: `choracompose://ephemeral/configs/*.json`

### Why Resources Matter

**Resources enable AI context**:

```
User: "Update my newsletter config to add a 'featured projects' section"

AI:   [Reads resource: choracompose://configs/content/newsletter.json]
      [Understands current structure]
      [Generates tool call: choracompose:draft_config with updated JSON]
```

**Key insight**: Resources provide **context** (what exists), tools provide **actions** (what to do).

---

## Capability Discovery Pattern

### The Problem: AI Doesn't Know What You Can Do

**Scenario**: User asks to "generate a report"

**Questions AI needs answers to**:
- What generators are available? (jinja2? code_generation?)
- What configs exist already? (can I reuse one?)
- What limits exist? (max file size? rate limits?)

**Traditional approach**: Hard-code capabilities in AI's system prompt

**MCP approach**: AI discovers capabilities dynamically

### chora-compose's Capability Discovery

**Tool**: `choracompose:list_capabilities`

**Output**:
```json
{
  "generators": [
    {
      "id": "jinja2",
      "name": "Jinja2 Generator",
      "description": "Template-based generation with loops, conditionals",
      "features": ["loops", "conditionals", "filters", "includes"]
    },
    {
      "id": "code_generation",
      "name": "AI Code Generation",
      "description": "Natural language generation via Claude API",
      "features": ["natural_language", "code_generation", "non_deterministic"],
      "requires_api_key": true
    }
  ],
  "features": {
    "ephemeral_storage": true,
    "retention_days": 30,
    "max_file_size_mb": 10,
    "config_lifecycle": true
  },
  "limits": {
    "max_generations_per_minute": 60,
    "max_artifact_parts": 50
  }
}
```

**Usage**:
```
User: "Can you generate code?"

AI:   [Calls choracompose:list_capabilities]
      [Sees code_generation generator available]
      "Yes! I can use the code_generation generator. Note: it requires
       an Anthropic API key. Do you have one configured?"
```

**Key insight**: AI adapts to system capabilities, not hard-coded assumptions.

---

## Config Lifecycle Integration

### The Lifecycle: Draft → Validate → Publish → Archive

MCP tools implement a **conversational config lifecycle**:

```
┌──────────────────────────────────────────────────────────┐
│ CONVERSATIONAL CONFIG LIFECYCLE VIA MCP                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. DRAFT                                                │
│     User: "Draft a newsletter config"                    │
│     AI:   [Calls choracompose:draft_config]                     │
│           → ephemeral/configs/newsletter.json            │
│                                                          │
│  2. ITERATE                                              │
│     User: "Add a 'featured projects' section"            │
│     AI:   [Reads ephemeral config via resource]          │
│           [Calls choracompose:draft_config with updates]        │
│           → ephemeral/configs/newsletter.json (updated)  │
│                                                          │
│  3. PREVIEW                                              │
│     User: "Show me what this looks like"                 │
│     AI:   [Calls choracompose:generate_content with ephemeral config] │
│           → ephemeral/outputs/newsletter-preview.md      │
│                                                          │
│  4. VALIDATE                                             │
│     User: "Is this config valid?"                        │
│     AI:   [Calls choracompose:validate_config]                  │
│           → ✅ Valid (or ❌ errors listed)                │
│                                                          │
│  5. PUBLISH                                              │
│     User: "Looks good, publish it"                       │
│     AI:   [Calls choracompose:publish_config]                   │
│           → configs/content/newsletter.json              │
│                                                          │
│  6. COMMIT (optional)                                    │
│     User: "Commit to git"                                │
│     AI:   [Calls git via bash tool]                      │
│           → Permanent version control                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Why MCP Enables This Workflow

**Traditional automation**:
```bash
# Must know exact schema upfront
cat > config.json <<EOF
{
  "metadata": { ... },
  "generatorSpecific": { ... }
}
EOF

# Validate manually
chora-compose validate config.json

# Move manually
mv config.json configs/content/
```

**MCP conversational workflow**:
```
User: "Create a newsletter config"
AI:   [Handles all boilerplate via MCP tools]
      "Draft created. Want to preview it?"

User: "Yes"
AI:   [Calls choracompose:generate_content]
      "Here's the preview. Any changes?"

User: "Add a section for events"
AI:   [Updates draft config]
      "Updated. Preview again?"

User: "No, publish it"
AI:   [Calls choracompose:publish_config]
      "Published to configs/content/newsletter.json"
```

**Key difference**: Conversational iteration vs upfront specification.

---

## Ephemeral Storage Integration

### MCP Tools + Ephemeral Storage = Safe Sandbox

MCP tools route outputs to **ephemeral storage by default**:

| Tool | Default Output | Purpose |
|------|---------------|---------|
| `choracompose:draft_config` | `ephemeral/configs/` | Safe sandbox for drafts |
| `choracompose:generate_content` | `ephemeral/outputs/` | Throwaway test outputs |
| `choracompose:publish_config` | `configs/` (persistent) | Approved configs only |

**Why this matters**:
- AI can explore freely without polluting permanent storage
- Users explicitly promote valuable content (via `publish_config`)
- Automatic cleanup (30-day retention) prevents accumulation

### Example: Exploratory Generation

```
User: "Generate 5 different intro paragraphs for our README"

AI:   [Calls choracompose:generate_content 5 times]
      → ephemeral/outputs/readme-intro-v1.md
      → ephemeral/outputs/readme-intro-v2.md
      → ephemeral/outputs/readme-intro-v3.md
      → ephemeral/outputs/readme-intro-v4.md
      → ephemeral/outputs/readme-intro-v5.md

User: "I like v3. Use that one."

AI:   [Copies v3 to project README.md]
      → README.md (committed to git)

# 30 days later: v1, v2, v4, v5 auto-deleted (cleanup)
```

**Key insight**: Ephemeral storage enables fearless exploration.

---

## Tool-Based vs Resource-Based Patterns

### When to Use Tools

✅ **Use MCP tools** when:

1. **Mutation required**: Creating, updating, deleting
2. **Complex operations**: Multi-step workflows
3. **Side effects**: Writing files, calling APIs
4. **Validation needed**: Check correctness before executing

**Examples**:
- `choracompose:generate_content` (creates output file)
- `choracompose:publish_config` (moves file, validates schema)
- `choracompose:cleanup_ephemeral` (deletes old files)

### When to Use Resources

✅ **Use MCP resources** when:

1. **Read-only access**: AI needs context, not mutation
2. **Structured data**: JSON, YAML, TOML configs
3. **Discovery**: List available options
4. **Reference**: Templates, schemas, examples

**Examples**:
- `choracompose://configs/content/*.json` (read existing configs)
- `choracompose://templates/*.j2` (browse available templates)
- `choracompose://capabilities` (discover system features)

### Combining Both

**Pattern**: Resources provide context → Tools perform actions

```
User: "Update my newsletter config"

Step 1 (AI reads resource):
  AI: [Reads choracompose://configs/content/newsletter.json]
      [Understands current structure]

Step 2 (AI calls tool):
  AI: [Calls choracompose:draft_config with updated JSON]
      → ephemeral/configs/newsletter.json (new draft)

Step 3 (AI reads resource again):
  AI: [Reads choracompose://ephemeral/configs/newsletter.json]
      "I've created a draft with the new section. Want to preview?"
```

**Key insight**: Resources = context, Tools = actions.

---

## Real-World MCP Workflows

### Workflow 1: Daily Standup Report

**User intent**: "Generate today's standup report"

**MCP conversation**:

```
User: "Generate today's standup report"

AI Step 1 (Capability discovery):
  [Calls choracompose:list_content_configs]
  [Finds "daily-standup" config]

AI Step 2 (Read config):
  [Reads choracompose://configs/content/daily-standup.json]
  [Sees it uses jinja2 generator]

AI Step 3 (Generate):
  [Calls choracompose:generate_content with config_id="daily-standup"]
  → ephemeral/outputs/standup-2025-10-21.md

AI Step 4 (Present):
  "I've generated today's standup report. Here's the preview:
   [shows content]

   Should I commit this to the project?"

User: "Yes"

AI Step 5 (Commit):
  [Copies to docs/standup-2025-10-21.md]
  [Commits to git]
```

**MCP tools used**:
- `choracompose:list_content_configs` (discovery)
- `choracompose:generate_content` (generation)
- Resources: `choracompose://configs/content/daily-standup.json`

---

### Workflow 2: Create New Config from Scratch

**User intent**: "Create a weekly newsletter config"

**MCP conversation**:

```
User: "Create a weekly newsletter config"

AI Step 1 (Capability discovery):
  [Calls choracompose:list_generators]
  [Sees jinja2, code_generation, etc.]
  "Which generator should I use? I recommend jinja2 for structured newsletters."

User: "Use jinja2"

AI Step 2 (Draft config):
  [Calls choracompose:draft_config]
  → ephemeral/configs/weekly-newsletter.json

AI Step 3 (Show draft):
  "I've created a draft config with sections: intro, featured_projects, events.
   Want to preview the output?"

User: "Yes"

AI Step 4 (Preview):
  [Calls choracompose:generate_content with ephemeral config]
  → ephemeral/outputs/weekly-newsletter-preview.md
  "Here's the preview. Any changes?"

User: "Add a 'community highlights' section"

AI Step 5 (Update draft):
  [Reads choracompose://ephemeral/configs/weekly-newsletter.json]
  [Updates JSON to add section]
  [Calls choracompose:draft_config with updated JSON]

AI Step 6 (Validate):
  [Calls choracompose:validate_config]
  "Config is valid. Ready to publish?"

User: "Yes"

AI Step 7 (Publish):
  [Calls choracompose:publish_config]
  → configs/content/weekly-newsletter.json
  "Published! Want me to commit to git?"
```

**MCP tools used**:
- `choracompose:list_generators`
- `choracompose:draft_config`
- `choracompose:generate_content`
- `choracompose:validate_config`
- `choracompose:publish_config`
- Resources: `choracompose://ephemeral/configs/*.json`

---

## Gateway Integration Model

### chora-compose as MCP Gateway

**Design pattern**: chora-compose acts as a **gateway** between AI and content generation:

```
┌─────────────────────────────────────────────────────────┐
│ AI ASSISTANT (Claude, n8n)                              │
│  - Natural language understanding                       │
│  - Intent interpretation                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ MCP Protocol (intent-based tools)
                  ▼
┌─────────────────────────────────────────────────────────┐
│ CHORA-COMPOSE MCP GATEWAY                               │
│  - Translates MCP calls → Python API calls              │
│  - Validates inputs, handles errors                     │
│  - Manages ephemeral storage, config lifecycle          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ Python API (implementation-specific)
                  ▼
┌─────────────────────────────────────────────────────────┐
│ GENERATORS (jinja2, code_generation, etc.)              │
│  - Template rendering (jinja2)                          │
│  - Claude API calls (code_generation)                   │
│  - BDD scenario generation (demonstration)              │
└─────────────────────────────────────────────────────────┘
```

**Why gateway pattern?**
- **Abstraction**: AI doesn't need to know implementation details (Jinja2 syntax, Claude API)
- **Flexibility**: Swap generators without changing MCP interface
- **Safety**: Gateway validates inputs, enforces limits

---

## Error Handling in MCP Workflows

### Traditional Automation: Fail Fast

```bash
# Script fails on first error
chora-compose generate --config invalid.json
Error: Config file not found

# Entire workflow stops
```

### MCP Conversational Error Handling

```
User: "Generate content with 'my-config'"

AI:   [Calls choracompose:generate_content with config_id="my-config"]
      [Tool returns error: "Config 'my-config' not found"]

      "I couldn't find a config named 'my-config'.
       Let me check what configs are available..."

      [Calls choracompose:list_content_configs]

      "I found these configs:
       - daily-standup
       - weekly-newsletter
       - api-docs

       Did you mean one of these?"

User: "Yes, weekly-newsletter"

AI:   [Calls choracompose:generate_content with config_id="weekly-newsletter"]
      "Generated! Here's the output..."
```

**Key difference**: Errors become **conversation turns**, not failures.

---

## Performance Considerations

### MCP Overhead

| Operation | Latency | Notes |
|-----------|---------|-------|
| **Tool discovery** | 10-50ms | Cached after first call |
| **Resource read** | 5-20ms | File I/O dependent |
| **Tool call** | 50-500ms | Depends on generator |
| **SSE round-trip** | 10-30ms | Network overhead |

**Optimization**: Use resources (read-only) instead of tools when possible.

**Example**:
- ❌ Slow: `choracompose:get_config` (tool call)
- ✅ Fast: Read `choracompose://configs/content/my-config.json` (resource)

### Batching Tool Calls

MCP supports batching:

```python
# Bad: Multiple round-trips
ai.call_tool("choracompose:list_generators")
ai.call_tool("choracompose:list_content_configs")
ai.call_tool("choracompose:list_templates")

# Good: Single batch request
ai.call_tools([
    "choracompose:list_generators",
    "choracompose:list_content_configs",
    "choracompose:list_templates"
])
```

---

## Security Considerations

### MCP Security Model

**Principle**: AI assistants are untrusted clients.

**Protections**:

1. **Input validation**: All tool inputs validated against JSON schema
2. **Path traversal prevention**: Configs restricted to `configs/` directory
3. **Rate limiting**: Max 60 generations/minute (configurable)
4. **File size limits**: Max 10 MB per file
5. **Sandbox isolation**: Ephemeral files isolated from persistent storage

### Example: Path Traversal Attack

**Attempted attack**:
```
User: "Read config '../../../etc/passwd'"

AI:   [Calls choracompose:get_config with config_id="../../../etc/passwd"]

MCP Server:
  [Validates input]
  [Detects path traversal]
  [Returns error: "Invalid config_id"]
```

**Protection**: Config IDs are validated to only access `configs/` directory.

---

## Comparison: MCP vs Traditional APIs

| Aspect | Traditional REST API | MCP |
|--------|---------------------|-----|
| **Discovery** | Static docs, OpenAPI spec | Dynamic capability discovery |
| **Error Handling** | HTTP status codes | Conversational clarification |
| **Batching** | Custom batch endpoints | Built-in batch support |
| **Streaming** | WebSockets, SSE | SSE transport native |
| **Client Integration** | Custom per client | Standard MCP SDK |
| **Context** | Stateless (must pass all context) | Resources provide shared context |

---

## Future: Advanced MCP Features

### Planned Features (v2.x)

**1. Streaming generation**:
```
User: "Generate a long report"

AI:   [Calls choracompose:generate_content with stream=true]
      [Shows progress as it generates]

      "Section 1: Complete (20%)
       Section 2: In progress (40%)
       ..."
```

**2. Multi-step workflows**:
```
User: "Create a documentation suite"

AI:   [Calls choracompose:create_workflow]
      [Workflow orchestrates: draft → validate → preview → publish]
      [Shows progress at each step]
```

**3. Context-aware prompts**:
```
MCP Prompt: "Generate API documentation"

Context (auto-injected):
  - Available generators: [jinja2, code_generation]
  - Existing configs: [api-docs-template.json]
  - Recent generations: [api-v1.md, api-v2.md]

AI uses context to generate better prompts
```

---

## Conclusion

**MCP transforms chora-compose from automation tool → conversational platform**:

1. **Tools** (17 total) provide intent-based actions
2. **Resources** provide context (configs, templates, capabilities)
3. **Capability discovery** enables AI to adapt to system features
4. **Config lifecycle** (draft → validate → publish) supports iteration
5. **Ephemeral storage** provides safe sandbox for exploration
6. **Gateway pattern** abstracts implementation details

**Key insight**: MCP is not just an API — it's a **collaboration protocol** that enables human-AI workflows.

**Remember**:
- Tools = actions (generate, validate, publish)
- Resources = context (configs, templates, capabilities)
- Ephemeral storage = safe sandbox for iteration
- Conversational errors = clarification, not failure

---

## Related Documentation

**Diataxis References**:
- [Tutorial: Your First MCP Workflow](../../tutorials/beginner/02-first-mcp-workflow.md) - Hands-on MCP experience
- [How-To: Use MCP Tools Effectively](../../how-to/integration/use-mcp-tools.md) - Practical MCP patterns
- [Reference: MCP Tools API](../../reference/mcp/tools-api.md) - Complete tool specifications

**Conceptual Relationships**:
- [Explanation: Human-AI Collaboration Philosophy](../concepts/human-ai-collaboration-philosophy.md) - Why conversational workflows
- [Explanation: Ephemeral Storage Design](../concepts/ephemeral-storage-design.md) - MCP + ephemeral integration
- [Explanation: Configuration-Driven Development](../concepts/configuration-driven-development.md) - CDD via MCP

**External Resources**:
- [MCP Specification](https://modelcontextprotocol.io) - Official MCP docs
- [FastMCP Framework](https://gofastmcp.com) - Python MCP implementation (used by chora-compose)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
