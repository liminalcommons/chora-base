# SAP-014: MCP Server Development

**Version:** 1.0.0 | **Status:** ⚠️ **DEPRECATED** (as of 2025-11-12) | **Maturity:** Pilot
**Protocol Version:** MCP 2024-11-05 | **FastMCP:** >=0.2.0 | **Chora Conventions:** v1.0

---

## ⚠️ DEPRECATION NOTICE

**SAP-014 is deprecated as of 2025-11-12. For new projects, use SAP-047 (Capability Server Template).**

**Migration Guide**:
- **New projects**: Use `scripts/create-capability-server.py --enable-mcp` (5-minute setup)
- **Existing projects**: Continue using SAP-014 until 2025-12-31 (supported)
- **Migration path**: See [SAP-047 Documentation](../capability-server-template/)

**Why SAP-047?**
- Multi-interface support (CLI, REST, MCP) vs MCP-only
- Production-ready architectural patterns (registry, bootstrap, composition)
- 2,271% ROI (5 minutes vs 40-60 hours manual setup)

---

## Quick Start (5 minutes)

```bash
# Create MCP server from template (fast-setup)
just create-mcp-server "Task Manager MCP" taskmgr ~/projects/task-manager-mcp

# Navigate to project and install dependencies
cd ~/projects/task-manager-mcp
uv sync

# Implement tools (src/<package>/server.py)
# Add @mcp.tool() for functions AI can call
# Add @mcp.resource() for data AI can read
# Add @mcp.prompt() for AI interaction templates

# Test MCP server
just mcp-test

# Configure Claude Desktop
just mcp-claude-config task-manager-mcp ~/projects/task-manager-mcp task_manager_mcp
# Copy output to ~/Library/Application Support/Claude/claude_desktop_config.json

# Restart Claude Desktop to load server
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete MCP setup (10-min read)

---

## What Is It?

SAP-014 provides **MCP server development** using FastMCP library (Python SDK) + Chora MCP Conventions v1.0 (namespace:tool_name pattern). It enables AI assistants like Claude to call custom tools, read resources, and use prompts through the Model Context Protocol.

**Key Innovation**: **Chora MCP Conventions v1.0** - Standardized naming (namespace:tool_name) and URIs (namespace://type/id) for tool discovery, composability, and ecosystem consistency. 90% of MCP servers in chora ecosystem adopt this pattern.

---

## When to Use

Use SAP-014 when you need to:

1. **Extend Claude capabilities** - Add custom tools for file operations, API calls, data processing
2. **Integrate external systems** - Connect Claude to databases, APIs, enterprise tools
3. **Build domain-specific tools** - Task management, code analysis, research assistance
4. **Share reusable tools** - Publish MCP servers for community or team use
5. **Automate workflows** - Enable Claude to automate complex multi-step processes

**Not needed for**: One-time scripts (use Python directly), or if built-in Claude Code tools sufficient

---

## Key Features

- ✅ **FastMCP SDK** - Official Python library for MCP protocol compliance
- ✅ **Chora MCP Conventions v1.0** - namespace:tool_name pattern (90% adoption)
- ✅ **Fast-Setup Script** - 1-2 minutes vs 30-60 minutes manual setup (80% faster)
- ✅ **3 MCP Primitives** - Tools (functions), Resources (data), Prompts (templates)
- ✅ **100% Protocol Compliance** - MCP 2024-11-05 specification
- ✅ **Type-Safe** - Full TypeScript-style type hints for tool parameters
- ✅ **JSON-RPC 2.0** - Transport over stdio, SSE, or WebSocket
- ✅ **Namespace Validation** - 3-20 chars, lowercase, alphanumeric, starts with letter
- ✅ **Claude Desktop Integration** - One command to generate config
- ✅ **Zero Dependencies** - FastMCP handles all protocol details

---

## Common Workflows

### MCP Core Concepts

#### **1. Tools** - Functions AI Can Call

Tools are Python functions decorated with `@mcp.tool()` that AI assistants can invoke:

```python
from mcp import mcp

@mcp.tool()
def create_task(title: str, description: str, priority: int = 3) -> dict:
    """Create a new task.

    Args:
        title: Task title (required)
        description: Task description (required)
        priority: Priority 1-5, default 3 (optional)

    Returns:
        dict with status and task_id

    Raises:
        ValueError: If priority not in 1-5 range
    """
    if priority < 1 or priority > 5:
        raise ValueError("Priority must be 1-5")

    task_id = generate_task_id()
    return {"status": "created", "task_id": task_id, "title": title}
```

**Tool Naming (Chora MCP Conventions v1.0)**:
- Pattern: `namespace:tool_name`
- Example: `taskmgr:create_task`
- Benefit: AI can discover tools by namespace prefix

**Why Type Hints Matter**:
- MCP protocol requires parameter schemas (type, description, required/optional)
- FastMCP auto-generates schemas from Python type hints + docstrings
- AI sees complete function signature when choosing which tool to call

---

#### **2. Resources** - Data AI Can Read

Resources are URIs that AI assistants can read to access data:

```python
from mcp import mcp
from .mcp import make_resource_uri

@mcp.resource(uri=make_resource_uri("templates", "daily-report.md"))
def get_daily_template() -> str:
    """Get daily report template.

    Returns markdown template for daily reports.
    """
    return """# Daily Report

## Accomplishments
- Task 1
- Task 2

## Blockers
- Issue 1

## Tomorrow
- Plan 1
"""
```

**Resource URIs (Chora MCP Conventions v1.0)**:
- Pattern: `namespace://type/id`
- Example: `taskmgr://templates/daily-report.md`
- Benefit: Consistent URI structure across MCP servers

**Resource Use Cases**:
- Templates (report templates, config templates)
- Documentation (API docs, guides)
- Configuration (settings, schemas)
- Dynamic data (task lists, metrics dashboards)

---

#### **3. Prompts** - AI Interaction Templates

Prompts are pre-defined templates for AI assistant interactions:

```python
from mcp import mcp

@mcp.prompt()
def summarize_tasks() -> str:
    """Generate task summary prompt.

    Returns prompt instructing AI to analyze tasks and provide summary with metrics and recommendations.
    """
    return """Analyze all tasks in the system and provide:

1. Summary metrics (total tasks, completed %, avg completion time)
2. Priority distribution (high/medium/low counts)
3. Blockers and recommendations
4. Next steps for highest-priority items

Use the taskmgr:list_tasks tool to retrieve task data."""
```

**Prompt Use Cases**:
- Analysis workflows (summarize data, identify patterns)
- Report generation (daily reports, sprint summaries)
- Onboarding (explain how to use MCP server)
- Troubleshooting (diagnose issues, suggest fixes)

---

### Chora MCP Conventions v1.0

#### **Namespace Rules**

**Valid Namespaces** (3-20 chars, lowercase, alphanumeric, starts with letter):
```bash
# ✅ Valid
taskmgr    # Task manager
chora      # Chora ecosystem
myapp      # Custom app

# ❌ Invalid
tm         # Too short (<3 chars)
TaskMgr    # Uppercase not allowed
task-mgr   # Hyphen not allowed
123task    # Cannot start with number
verylongnamespacethatexceedstwentychars  # Too long (>20 chars)
```

**Validation**:
```bash
just mcp-validate-namespace taskmgr  # ✅ Valid
just mcp-validate-namespace tm       # ❌ Invalid (too short)
```

---

#### **Tool Naming Pattern**

**Format**: `namespace:tool_name`

**Examples**:
- `taskmgr:create_task` - Create task in task manager
- `taskmgr:list_tasks` - List all tasks
- `taskmgr:complete_task` - Mark task as complete
- `chora:create_coordination` - Create coordination request

**Benefits**:
- **Tool Discovery**: AI can list all tools by namespace prefix
- **Composability**: One MCP server can call another's tools
- **Consistency**: Predictable patterns across ecosystem

---

#### **Resource URI Pattern**

**Format**: `namespace://type/id`

**Examples**:
- `taskmgr://templates/daily.md` - Daily report template
- `taskmgr://templates/sprint.md` - Sprint report template
- `taskmgr://tasks/123` - Task details for task ID 123
- `chora://docs/api-reference` - API documentation

**Benefits**:
- **Consistent Structure**: All resources follow same URI pattern
- **Type Safety**: Type field categorizes resources
- **Discoverability**: AI can list resources by type

---

### Fast-Setup Script (SAP-003)

#### **create-mcp-server** - Generate MCP Server from Template

```bash
just create-mcp-server PROJECT_NAME NAMESPACE OUTPUT_PATH

# Example: Create task manager MCP server
just create-mcp-server "Task Manager MCP" taskmgr ~/projects/task-manager-mcp

# What it generates:
# - src/<package>/server.py      # MCP server entry point
# - src/<package>/mcp.py          # Chora MCP Conventions v1.0 helpers
# - pyproject.toml                # FastMCP dependency
# - AGENTS.md                     # MCP-specific agent guidance
# - CLAUDE.md                     # Claude Desktop config instructions
# - README.md                     # MCP server documentation
# - tests/                        # pytest tests with MCP mocking
# - .github/workflows/            # CI/CD for MCP testing
```

**Generated in 1-2 minutes** vs 30-60 minutes manual setup (80% time savings)

---

#### **mcp-claude-config** - Generate Claude Desktop Config

```bash
just mcp-claude-config PROJECT_NAME PROJECT_PATH PACKAGE_NAME

# Example:
just mcp-claude-config task-manager-mcp ~/projects/task-manager-mcp task_manager_mcp

# Output (copy to ~/Library/Application Support/Claude/claude_desktop_config.json):
{
  "mcpServers": {
    "task-manager-mcp": {
      "command": "uv",
      "args": ["--directory", "/Users/you/projects/task-manager-mcp", "run", "task_manager_mcp"],
      "env": {}
    }
  }
}
```

**Steps after copying config**:
1. Restart Claude Desktop app
2. Verify server loaded: "List all available tools" in Claude
3. Use tools: "Use the taskmgr:create_task tool to create a task"

---

### MCP Development Workflow

#### **Step 1: Create Server** (1-2 min)

```bash
just create-mcp-server "My MCP Server" mymcp ~/projects/my-mcp-server
cd ~/projects/my-mcp-server
uv sync
```

---

#### **Step 2: Implement Tools** (10-30 min)

Edit `src/<package>/server.py`:

```python
from mcp import mcp

@mcp.tool()
def hello(name: str) -> str:
    """Say hello.

    Args:
        name: Name to greet

    Returns:
        Greeting message
    """
    return f"Hello, {name}!"

@mcp.resource(uri=make_resource_uri("templates", "greeting.txt"))
def get_greeting_template() -> str:
    """Get greeting template."""
    return "Hello, {name}! Welcome to {project}."

@mcp.prompt()
def greet_user() -> str:
    """Generate user greeting prompt."""
    return "Use the mymcp:hello tool to greet the user warmly."
```

---

#### **Step 3: Test Locally** (1-5 min)

```bash
just mcp-test
# Runs: pytest tests/

# Or test manually:
uv run <package_name>
# Server starts, waits for stdin (JSON-RPC 2.0 messages)
# Press Ctrl+C to stop
```

---

#### **Step 4: Configure Claude Desktop** (1 min)

```bash
just mcp-claude-config my-mcp-server ~/projects/my-mcp-server my_mcp_server
# Copy output to ~/Library/Application Support/Claude/claude_desktop_config.json
```

---

#### **Step 5: Restart Claude Desktop** (30 sec)

Quit and reopen Claude Desktop app. Server loads automatically on startup.

---

#### **Step 6: Test in Claude** (1 min)

In Claude Desktop:
```
User: "List all available tools"
Claude: Shows tools including "mymcp:hello"

User: "Use the mymcp:hello tool with name 'World'"
Claude: Calls tool → Returns "Hello, World!"
```

---

### CLI Commands

#### **create-mcp-server** - Create MCP Server from Template
```bash
just create-mcp-server PROJECT_NAME NAMESPACE OUTPUT_PATH
# Example: just create-mcp-server "Weather MCP" weather ~/projects/weather-mcp
```

#### **mcp-validate-namespace** - Validate Namespace
```bash
just mcp-validate-namespace NAMESPACE
# Example: just mcp-validate-namespace taskmgr  # ✅ Valid
```

#### **mcp-claude-config** - Generate Claude Desktop Config
```bash
just mcp-claude-config PROJECT_NAME PROJECT_PATH PACKAGE_NAME
# Example: just mcp-claude-config weather-mcp ~/projects/weather-mcp weather_mcp
```

#### **mcp-test** - Run MCP Server Tests
```bash
just mcp-test
# Runs: pytest tests/ (MCP mocking included)
```

#### **mcp-help** - Show MCP Workflow
```bash
just mcp-help
# Output: MCP development workflow with commands
```

---

## Integration

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-003** (Bootstrap) | Fast-Setup | `just create-mcp-server` uses SAP-003 templates |
| **SAP-004** (Testing) | MCP Mocking | pytest tests with FastMCP test client |
| **SAP-005** (CI/CD) | GitHub Actions | CI workflows test MCP servers automatically |
| **SAP-006** (Quality Gates) | Pre-commit hooks | ruff + mypy validate MCP server code |
| **SAP-011** (Docker) | Containerization | Deploy MCP servers as Docker services |
| **SAP-012** (Lifecycle) | BDD for Tools | Write BDD scenarios for tool behaviors |

**Cross-SAP Workflow Example**:
```bash
# 1. Create MCP server (SAP-003 + SAP-014)
just create-mcp-server "Task MCP" taskmgr ~/projects/task-mcp
cd ~/projects/task-mcp

# 2. Implement tools (SAP-014)
# Edit src/task_mcp/server.py

# 3. Test with BDD (SAP-012 + SAP-004)
cat > features/create-task.feature <<EOF
Feature: Task Creation
  Scenario: Create task successfully
    When I call taskmgr:create_task with title "Test task"
    Then I receive task_id
    And status is "created"
EOF
pytest features/ --gherkin

# 4. Quality gates (SAP-006)
git add . && git commit -m "Add MCP server"  # Pre-commit hooks run

# 5. CI/CD (SAP-005)
git push origin main
# GitHub Actions test MCP server

# 6. Docker deployment (SAP-011)
just docker-build task-mcp latest
docker run -d task-mcp:latest
```

---

## Success Metrics

- **Setup Time**: 1-2 minutes (vs 30-60 minutes manual) - 80% faster
- **Protocol Compliance**: 100% (FastMCP handles all MCP 2024-11-05 details)
- **Namespace Consistency**: 90% of chora MCP servers use Chora MCP Conventions v1.0
- **Tool Discoverability**: 100% (namespace:tool_name pattern)
- **Type Safety**: 100% (FastMCP auto-generates schemas from type hints)

---

## Troubleshooting

### Problem 1:MCP server not loading in Claude Desktop

**Solution**: Check config path and syntax:
```bash
# 1. Verify config file location
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Verify JSON syntax (no trailing commas, proper quotes)
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 3. Check server installation
cd ~/projects/task-mcp
uv sync
uv run task_mcp  # Should start server (stdio transport)

# 4. Check Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp*.log

# 5. Restart Claude Desktop
# Quit completely (Cmd+Q), then reopen
```

---

### Problem 2:Tool parameters not validated correctly

**Solution**: Ensure type hints + docstrings follow FastMCP patterns:
```python
# ❌ BAD (no type hints, incomplete docstring)
@mcp.tool()
def create_task(title, priority=3):
    """Create task."""
    return {}

# ✅ GOOD (full type hints, complete docstring)
@mcp.tool()
def create_task(title: str, priority: int = 3) -> dict:
    """Create a new task.

    Args:
        title: Task title (required)
        priority: Priority 1-5 (optional, default 3)

    Returns:
        dict with status and task_id

    Raises:
        ValueError: If priority out of range
    """
    if priority < 1 or priority > 5:
        raise ValueError("Priority must be 1-5")
    return {"status": "created"}
```

**Why**: FastMCP generates MCP tool schemas from:
- Type hints → Parameter types (str, int, bool, etc.)
- Docstring "Args" section → Parameter descriptions
- Default values → Optional vs required

---

### Problem 3:Namespace validation fails

**Solution**: Check namespace against Chora MCP Conventions v1.0 rules:
```bash
just mcp-validate-namespace mynamespace

# Rules:
# - 3-20 characters
# - Lowercase only
# - Alphanumeric only (no hyphens, underscores)
# - Must start with letter (not number)

# ✅ Valid: taskmgr, chora, myapp
# ❌ Invalid: tm (too short), TaskMgr (uppercase), task-mgr (hyphen), 123task (starts with number)
```

---

### Problem 4:Resource URIs not working

**Solution**: Use `make_resource_uri()` helper from `mcp.py`:
```python
# ❌ BAD (hardcoded URI, namespace inconsistency)
@mcp.resource(uri="taskmgr://templates/daily.md")
def get_template() -> str:
    return "..."

# ✅ GOOD (make_resource_uri ensures namespace consistency)
from .mcp import make_resource_uri

@mcp.resource(uri=make_resource_uri("templates", "daily.md"))
def get_template() -> str:
    """Get daily report template."""
    return "..."
```

**Why**: `make_resource_uri()` auto-prefixes with configured namespace, ensuring consistency.

---

## Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete MCP technical specification (51KB, 25-min read)
- **[AGENTS.md](AGENTS.md)** - Agent MCP workflows (26KB, 13-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Desktop integration patterns (13KB, 7-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - MCP server setup guide (22KB, 10-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics
- **[MCP Specification](https://modelcontextprotocol.io/specification)** - Official MCP protocol docs
- **[FastMCP Docs](https://github.com/jlowin/fastmcp)** - FastMCP library reference

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial MCP server development with FastMCP + Chora MCP Conventions v1.0

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
