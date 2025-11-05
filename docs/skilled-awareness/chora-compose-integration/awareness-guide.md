# Awareness Guide: chora-compose Integration

**SAP ID**: SAP-017
**Version**: 2.0.0
**For**: AI Agents, LLM-Based Assistants
**Last Updated**: 2025-11-04

---

## Quick Start for AI Agents

### One-Sentence Summary

Integration guide for chora-compose content generation framework: 4 modalities (pip/MCP/CLI/Docker), decision trees for modality selection, role-based workflows, time-to-first-success <30 minutes.

### When to Use This SAP

Use SAP-017 when:
- ✅ User wants to adopt chora-compose for content generation
- ✅ User asks "how do I integrate chora-compose?"
- ✅ User needs to choose between pip, MCP server, CLI, or Docker integration
- ✅ User wants quick start guidance (< 30 minutes to first generated content)
- ✅ User needs role-specific workflows (developer, AI agent, team, DevOps)
- ✅ Project needs automated content generation (documentation, configs, etc.)
- ✅ User mentions "chora-compose" and needs integration help

Don't use SAP-017 for:
- ❌ Deep architecture questions about chora-compose → use SAP-018 (chora-compose Architecture)
- ❌ Collections patterns and anti-patterns → use SAP-031 (Collections Patterns)
- ❌ Custom generator development → use SAP-030 (Generator Selection)
- ❌ Performance tuning and optimization → use SAP-032 (Troubleshooting Runbook)
- ❌ Docker Compose orchestration (container tool) → see archived SAP-017 v1.0.0

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1: Four Integration Modalities**
- **Description**: chora-compose supports 4 different integration paths (modalities), each optimized for different use cases
- **Modalities**:
  - **pip**: Library integration for Python projects
  - **MCP server**: AI agent access via Model Context Protocol
  - **CLI**: Interactive command-line usage
  - **Docker**: Team deployment and n8n workflows
- **When to use**: Help user choose correct modality based on use case (see Decision Tree below)
- **Example**: User says "I want Claude Desktop to generate content" → MCP server modality

**Concept 2: Decision-Driven Adoption**
- **Description**: Users should choose ONE modality first based on their role and needs, not try all four
- **When to use**: When user is confused about which integration path to take
- **Key questions**: "What's your role?" (developer/AI user/team lead), "What's your goal?" (Python integration/AI agent access/team deployment)
- **Example**: Developer in Python project → recommend pip modality first

**Concept 3: Time-to-First-Success < 30 minutes**
- **Description**: All modalities support < 30 minute path from zero to first generated content
- **When to use**: Set user expectations, provide "quick win" workflow
- **Workflow**: Choose modality (5 min) → Install (5-10 min) → Create config (5-10 min) → Generate (1-2 min) → Validate (1-2 min)
- **Example**: User wants to "try it out quickly" → guide through hello-world example in chosen modality

**Concept 4: Adoption Levels (1/2/3)**
- **Description**: Progressive adoption journey from basic to production to advanced
- **Levels**:
  - **Level 1**: Install + first success (< 30 min)
  - **Level 2**: Production integration (1-2 days)
  - **Level 3**: Advanced patterns (1-2 weeks)
- **When to use**: Help user understand adoption stages and set realistic timelines
- **Example**: User asks "how long does this take?" → explain Level 1 is <30 min, production (Level 2) is 1-2 days

### Decision Tree: Choosing Integration Modality

```
User wants to integrate chora-compose
   │
   ├─ Role: Python Developer?
   │   ├─ Yes → Want library integration in code?
   │   │   ├─ Yes → ✅ pip modality (install: pip install chora-compose)
   │   │   └─ No → Want CLI for testing?
   │   │       └─> ✅ CLI modality (install: pip install "chora-compose[cli]")
   │   └─ No → Continue...
   │
   ├─ Role: AI Agent User (Claude Desktop, Cursor)?
   │   ├─ Yes → ✅ MCP server modality
   │   │       (requires Docker Desktop + config.json setup)
   │   └─ No → Continue...
   │
   ├─ Role: Team Lead / DevOps?
   │   ├─ Team deployment needed?
   │   │   └─> ✅ Docker modality (docker-compose deployment)
   │   └─ n8n workflow integration?
   │       └─> ✅ Docker modality (HTTP API access)
   │
   └─ Use Case: Just exploring/testing?
       └─> ✅ CLI modality (easiest for exploration)
```

### Decision Tree: Common User Requests

```
User request about chora-compose
   │
   ├─ "How do I install chora-compose?"
   │   └─> Ask: "What's your role?" → Use modality decision tree above
   │
   ├─ "I want to generate [content type]"
   │   └─> Guide: Choose modality → Install → Create config → Generate
   │
   ├─ "Which modality should I use?"
   │   └─> Use modality decision tree (developer → pip, AI user → MCP, etc.)
   │
   ├─ "Can Claude Desktop use chora-compose?"
   │   └─> Yes! MCP server modality → guide through setup
   │
   ├─ "How do I create a config?"
   │   ├─ MCP modality? → Use `create_content_config` tool
   │   └─ pip/CLI modality? → Provide YAML template + example
   │
   └─ "It's not working" / troubleshooting
       └─> See Common Issues section below
```

---

## 2. Common Agent Workflows

### Workflow 1: Help User Choose Modality

**User Request**: "I want to use chora-compose. How do I integrate it?"

**Agent Actions**:
1. **Ask clarifying question**: "What's your role or use case?"
   - Python developer integrating in project?
   - Using Claude Desktop or Cursor (AI agent access)?
   - Setting up for a team?
   - Just want to explore/test?

2. **Recommend modality** based on response:
   - Developer → pip modality
   - AI user → MCP server modality
   - Team/DevOps → Docker modality
   - Exploring → CLI modality

3. **Provide installation instructions** for chosen modality:
   - pip: `pip install chora-compose`
   - MCP: Docker Desktop + config.json setup
   - CLI: `pip install "chora-compose[cli]"`
   - Docker: docker-compose.yml + `docker-compose up`

4. **Offer quick start**: "Would you like me to guide you through generating your first content?"

**Validation**:
```bash
# pip/CLI: Check installation
python -c "import chora_compose; print(chora_compose.__version__)"
chora-compose --version

# MCP: Check Docker image
docker images | grep chora-compose-mcp

# Docker: Check service running
docker-compose ps
```

**Expected Output**: User has clear understanding of which modality to use and has installation instructions.

---

### Workflow 2: MCP Modality - Generate Content Conversationally

**User Request**: "Generate API documentation using chora-compose"

**Context**: User has MCP server configured (agent has access to chora-compose MCP tools)

**Agent Actions**:

1. **Check if MCP tools available**:
   - Tool available: `create_content_config`, `generate_content`
   - If not available: Guide user through MCP server setup (Docker + config.json)

2. **Gather requirements conversationally**:
   - "What type of content? (docs, config, test data, etc.)"
   - "What source data? (file path, inline data, etc.)"
   - "Where should output be generated? (output path)"

3. **Use `create_content_config` tool**:
   ```json
   {
     "generator_type": "jinja2",
     "content_id": "api-docs",
     "output_path": "docs/api-reference.md",
     "template": "[Jinja2 template based on user needs]",
     "context_sources": [...]
   }
   ```

4. **Use `generate_content` tool**:
   - Pass config to generate content
   - Capture output path

5. **Validate and show result**:
   - "✓ Generated: docs/api-reference.md"
   - Offer to show content or make changes

**Validation**:
```bash
# Check output exists
ls docs/api-reference.md

# View content
cat docs/api-reference.md
```

**Expected Output**: Content generated conversationally without manual config file creation.

**Variations**:
- User wants to save config for reuse → use `save_draft_config` tool
- User wants to iterate on config → use `load_draft_config`, modify, regenerate
- User wants to generate multiple pieces → repeat with different `content_id`

---

### Workflow 3: pip/CLI Modality - Guide First Config Creation

**User Request**: "How do I create a chora-compose config?"

**Context**: User chose pip or CLI modality

**Agent Actions**:

1. **Explain config structure** (brief):
   - YAML file with required fields: `version`, `content_id`, `generator_type`, `output_path`
   - Template (inline or file path)
   - Context sources (where data comes from)

2. **Provide hello-world example**:
   ```yaml
   version: "3.1"
   content_id: hello-world
   generator_type: jinja2
   output_path: output/hello-world.md

   template: |
     # Hello World

     Generated at: {{ timestamp }}

   context:
     inline_data:
       timestamp: "2025-11-04T12:00:00"
   ```

3. **Guide creation**:
   - "Save this to configs/hello-world.yaml"
   - "Create configs/ directory if it doesn't exist: mkdir -p configs/"

4. **Provide generation command**:
   - pip: Show Python code to load config and generate
   - CLI: `chora-compose generate content --config configs/hello-world.yaml`

5. **Validation**:
   - "Check output: ls output/hello-world.md"
   - "View content: cat output/hello-world.md"

**Validation**:
```bash
# Check config file exists
ls configs/hello-world.yaml

# Generate (CLI example)
chora-compose generate content --config configs/hello-world.yaml

# Check output
ls output/hello-world.md
```

**Expected Output**: User has first working config and generated content.

---

### Workflow 4: Troubleshoot "Not Working" Issues

**User Request**: "chora-compose isn't working" / "I'm getting an error"

**Agent Actions**:

1. **Gather diagnostics**:
   - "Which modality are you using? (pip/MCP/CLI/Docker)"
   - "What's the exact error message?"
   - "What command did you run?"

2. **Check common issues by modality**:

   **pip modality**:
   - ModuleNotFoundError → not installed: `pip install chora-compose`
   - Version check: `python -c "import chora_compose; print(chora_compose.__version__)"`

   **MCP modality**:
   - Tools not showing in Claude Desktop → check Docker running: `docker ps`
   - config.json syntax → validate JSON
   - Restart Claude Desktop

   **CLI modality**:
   - Command not found → check installation: `chora-compose --version`
   - Install CLI extras: `pip install "chora-compose[cli]"`

   **Docker modality**:
   - Service not starting → check logs: `docker-compose logs -f`
   - Port conflicts → check `docker-compose ps`

3. **Check config syntax** (if generation failing):
   - "Can you share your config file?"
   - Validate required fields: `version`, `content_id`, `generator_type`, `output_path`
   - Check YAML syntax (no tabs, proper indentation)

4. **Check generator exists**:
   - List available generators: `chora-compose list capabilities` (CLI)
   - Common generators: `jinja2`, `demonstration`, `template_fill`

5. **Provide fix** based on diagnosis:
   - Installation issue → provide install command
   - Config issue → fix YAML syntax, add missing fields
   - Permission issue → `chmod` or `mkdir` commands
   - Docker issue → restart Docker Desktop, verify running

**Validation**: Re-run failing command, verify success.

**Expected Output**: Issue diagnosed and resolved, user can proceed.

---

## 3. Quick Reference

### Installation Commands

```bash
# pip modality
pip install chora-compose

# CLI modality
pip install "chora-compose[cli]"

# MCP modality
# 1. Install Docker Desktop
# 2. Edit ~/.config/claude/config.json (macOS/Linux)
#    or %APPDATA%\Claude\config.json (Windows)
# 3. Add:
{
  "mcpServers": {
    "chora-compose": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${workspaceFolder}:/workspace",
        "ghcr.io/liminalcommons/chora-compose-mcp:latest"
      ]
    }
  }
}
# 4. Restart Claude Desktop

# Docker modality
# Create docker-compose.yml, then:
docker-compose up -d
```

### Common Commands (CLI)

```bash
# Generate content from config
chora-compose generate content --config configs/my-config.yaml

# Create content config interactively
chora-compose create content --output configs/new-config.yaml

# List available generators
chora-compose list capabilities

# Validate config syntax
chora-compose validate --config configs/my-config.yaml

# Check version
chora-compose --version
```

### MCP Tools (22 tools)

**Config Creation** (6 tools):
- `create_content_config` - Create content config
- `create_artifact_config` - Create artifact config
- `create_collection_config` - Create collection config
- `save_draft_config` - Save draft to ephemeral storage
- `load_draft_config` - Load draft from ephemeral storage
- `delete_draft_config` - Delete draft

**Generation** (3 tools):
- `generate_content` - Generate single content piece
- `assemble_artifact` - Assemble artifact from multiple pieces
- `assemble_collection` - Bulk generate collection

**Utilities** (13 tools):
- `list_capabilities` - List available generators
- `get_generator_info` - Get generator details
- `test_generator` - Test generator with sample data
- `validate_config` - Validate config syntax
- `store_ephemeral_output` - Store temporary output
- `retrieve_ephemeral_output` - Retrieve temporary output
- `list_ephemeral_outputs` - List ephemeral outputs
- `delete_ephemeral_output` - Delete ephemeral output
- `list_collections` - List collections
- `get_collection_status` - Get collection status
- `invalidate_cache` - Force cache rebuild
- `resolve_context` - Resolve context from sources
- `check_freshness` - Check if cache is fresh

### Minimal Config Example

```yaml
version: "3.1"
content_id: my-content
generator_type: jinja2
output_path: output/my-file.md

template: |
  # {{ title }}

  {{ content }}

context:
  inline_data:
    title: "My Title"
    content: "My content here"
```

### File Paths Reference

```
project-root/
├── configs/               # Config files (YAML)
│   ├── content/          # Content configs
│   ├── artifacts/        # Artifact configs
│   └── collections/      # Collection configs
├── templates/            # Reusable Jinja2 templates (.j2)
├── output/               # Generated content (exclude from git)
└── .chora-compose/       # Ephemeral storage (exclude from git)
```

---

## 4. Common Issues & Quick Fixes

### Issue: "ModuleNotFoundError: No module named 'chora_compose'"

**Fix**: Install chora-compose
```bash
pip install chora-compose
```

**Verify**:
```bash
python -c "import chora_compose; print(chora_compose.__version__)"
```

---

### Issue: "MCP tools not showing in Claude Desktop"

**Fix**: Check Docker running, restart Claude Desktop
```bash
# 1. Check Docker
docker ps

# 2. If Docker not running: start Docker Desktop

# 3. Pull image manually (if needed)
docker pull ghcr.io/liminalcommons/chora-compose-mcp:latest

# 4. Restart Claude Desktop (quit completely, reopen)
```

---

### Issue: "Unknown generator: {generator_type}"

**Fix**: Check available generators, fix config
```bash
# List generators
chora-compose list capabilities

# Update config with valid generator (case-sensitive):
# - jinja2
# - demonstration
# - template_fill (v1.5.0+)
```

---

### Issue: "Invalid config" / "Missing required field"

**Fix**: Check required fields, validate YAML syntax

**Required fields**:
- `version` (e.g., "3.1")
- `content_id` (unique identifier)
- `generator_type` (e.g., "jinja2")
- `output_path` (e.g., "output/file.md")
- `template` or `template_path`
- `context` (inline_data, external_file, etc.)

**Validate**:
```bash
chora-compose validate --config configs/my-config.yaml
```

---

### Issue: "Permission denied" writing output

**Fix**: Check directory exists, fix permissions
```bash
# Create output directory
mkdir -p output/

# Fix permissions
chmod -R u+w output/
```

---

## 5. Agent Best Practices

### When Helping Users with chora-compose Integration:

1. **Always ask about role/use case FIRST** before recommending modality
   - Don't assume user knows which modality is right
   - Use decision tree to guide recommendation

2. **Provide complete, copy-paste ready examples**
   - Config examples should be valid YAML (proper indentation, no syntax errors)
   - Commands should be complete (not "run the command...")
   - Include validation steps

3. **Set realistic expectations for time**
   - Level 1 (first success): < 30 minutes
   - Level 2 (production): 1-2 days
   - Level 3 (advanced): 1-2 weeks

4. **For MCP modality users: leverage tools**
   - Don't tell user to write config manually if you have MCP tools
   - Use `create_content_config` + `generate_content` for conversational workflow
   - Show both approaches: "I can generate this for you, or guide you to do it yourself"

5. **Troubleshooting: gather diagnostics first**
   - Modality, error message, command run
   - Don't guess - ask specific questions
   - Use validation commands to verify fixes

6. **Progressive disclosure**
   - Start simple (hello-world example)
   - Then real-world example (API docs, test data)
   - Then advanced patterns (artifacts, collections)

7. **Reference protocol-spec.md for technical details**
   - Integration contracts (Section 2)
   - Workflows (Section 4)
   - Troubleshooting (Section 12)

---

## 6. Related SAPs

**Required Foundation**:
- [SAP-000: SAP Framework](../sap-framework/awareness-guide.md) - Understanding SAP structure and protocols

**Advanced Usage**:
- [SAP-018: chora-compose Architecture](../chora-compose-meta/awareness-guide.md) - Deep architecture for power users
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/awareness-guide.md) - 5-week pilot methodology
- [SAP-029: SAP Generation](../sap-generation/awareness-guide.md) - Automated SAP artifact generation

**Future SAPs** (out of scope for SAP-017):
- SAP-030: Generator Selection & Customization
- SAP-031: Collections Patterns & Anti-Patterns
- SAP-032: Troubleshooting Runbook

---

## 7. External Resources

**Official Documentation**:
- [chora-compose README](https://github.com/liminalcommons/chora-compose) - Project overview
- [AGENTS.md](https://github.com/liminalcommons/chora-compose/blob/main/AGENTS.md) - Complete MCP tools documentation
- [chora-compose Docs](https://github.com/liminalcommons/chora-compose/tree/main/docs) - Comprehensive documentation (Diátaxis framework)

**Community**:
- [chora-compose Discussions](https://github.com/liminalcommons/chora-compose/discussions) - Q&A and patterns

**Specifications**:
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification

---

**Document Version**: 2.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
