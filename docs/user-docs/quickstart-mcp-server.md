# Quickstart: Create Your First Capability Server (with MCP)

**Time to First Server**: 5 minutes

This guide shows the fastest way to create a production-ready **capability server with multi-interface support** (CLI, REST, and MCP) using chora-base's SAP-047 (Capability Server Template).

**⚠️ SAP-014 Deprecation**: This guide replaces the old MCP-only approach (SAP-014). SAP-047 provides multi-interface capability servers vs. MCP-only servers.

---

## What You'll Get

A production-ready capability server with MCP interface:

- ✅ **Multi-interface support** - CLI, REST, and MCP (SAP-043)
- ✅ **Core/interface separation** - Clean architecture (SAP-042)
- ✅ **Service registry** - Manifest-based discovery (SAP-044)
- ✅ **Bootstrap startup** - Dependency-ordered initialization (SAP-045)
- ✅ **Composition patterns** - Saga, circuit breaker, events (SAP-046)
- ✅ **Task tracking** - Beads for multi-session memory (SAP-015)
- ✅ **Testing** - pytest with 85% coverage target (SAP-004)
- ✅ **CI/CD** - GitHub Actions workflows (SAP-005)
- ✅ **Quality gates** - ruff, mypy, pre-commit hooks (SAP-006)
- ✅ **Documentation** - Comprehensive AGENTS.md, API.md, CLI.md (SAP-007, 009)

**Total setup time**: 5 minutes (vs. 40-60 hours manual setup)

---

## Prerequisites

- **Python 3.11+** (or 3.9+)
- **Git** configured (user.name, user.email)
- **Claude Desktop** (or Cursor, Cline)
- **Terminal** access

---

## Step 1: Clone chora-base

```bash
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base
```

**Time**: 30 seconds

---

## Step 2: Run Fast-Setup Script

```bash
python scripts/create-capability-server.py \
    --name "Weather" \
    --namespace weather \
    --enable-mcp \
    --output ~/projects/weather-mcp
```

**What happens**:
1. Creates project structure (src/, tests/, docs/, .beads/, inbox/, .chora/)
2. Renders templates with your project details
3. Initializes beads, inbox, A-MEM
4. Creates git repository with initial commit
5. Validates all 12 model citizen requirements

**Time**: 1-2 minutes

**Output**:
```
================================================================================
✅ Model Citizen Capability Server Created Successfully!
================================================================================

📁 Location: /Users/you/projects/weather-mcp

📝 Next Steps:
  1. cd /Users/you/projects/weather-mcp
  2. Create virtual environment: python -m venv venv && source venv/bin/activate
  3. Install dependencies: pip install -e .[dev]
  4. Run tests: pytest

🚀 Happy coding!
```

---

## Step 3: Install Dependencies

```bash
cd ~/projects/weather-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e .[dev]
```

**Time**: 1-2 minutes

---

## Step 4: Verify Setup

```bash
# Run tests (should pass out of the box)
pytest

# Check code quality
ruff check .
mypy src/

# Validate model citizen compliance
python /path/to/chora-base/scripts/validate-model-citizen.py
```

**Expected**:
```
✅ Project is MODEL CITIZEN COMPLIANT!
```

**Time**: 30 seconds

---

## Step 5: Configure Claude Desktop

Add your MCP server to Claude Desktop:

```bash
# Open Claude Desktop config
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
# On Windows: %APPDATA%\Claude\claude_desktop_config.json
```

Add this JSON (update paths for your system):

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["-m", "weather_mcp.server"],
      "cwd": "/Users/you/projects/weather-mcp"
    }
  }
}
```

**Save and restart Claude Desktop**.

**Time**: 1-2 minutes

---

## Step 6: Implement Your First Tool

Edit `src/weather_mcp/server.py`:

```python
from fastmcp import FastMCP
from .mcp import make_tool_name

mcp = FastMCP("Weather MCP Server")

@mcp.tool()
def get_current_weather(location: str, units: str = "fahrenheit") -> dict:
    """Get current weather for a location.

    Args:
        location: City name or zip code
        units: Temperature units (fahrenheit or celsius)

    Returns:
        Current weather data
    """
    # TODO: Implement actual weather API call
    return {
        "location": location,
        "temperature": 72,
        "units": units,
        "conditions": "sunny",
        "humidity": 45,
    }
```

**Time**: 2-3 minutes

---

## Step 7: Test Your Tool in Claude

1. **Restart Claude Desktop** (to load your MCP server)
2. **Start a conversation** in Claude Desktop
3. **Ask**: "What's the weather in San Francisco?"

Claude will use your `weather:get_current_weather` tool!

**Expected**:
```
The weather in San Francisco is currently sunny with a temperature of 72°F
and 45% humidity.
```

**Time**: 30 seconds

---

## Next Steps

### 🎯 Add More Tools

```python
@mcp.tool()
def get_forecast(location: str, days: int = 7) -> dict:
    """Get weather forecast."""
    # Your implementation
    pass
```

### 📚 Add Resources

```python
@mcp.resource(uri="weather://locations/{location_id}")
def get_location_data(location_id: str) -> str:
    """Get detailed location information."""
    # Your implementation
    pass
```

### ✅ Track Tasks with Beads

```bash
# Create a task
bd create "Implement 5-day forecast" --assignee me

# List tasks
bd list

# Mark task in progress
bd update weather-a3f --status in_progress

# Complete task
bd close weather-a3f --reason "Implemented forecast endpoint"
```

### 🧪 Write Tests

```python
# tests/test_weather.py
def test_get_current_weather():
    result = get_current_weather("San Francisco")
    assert result["location"] == "San Francisco"
    assert "temperature" in result
```

### 📖 Read Documentation

- **AGENTS.md** - Agent-specific patterns for your MCP server
- **CLAUDE.md** - Claude Code workflows
- **docs/user-docs/** - User guides
- **docs/dev-docs/** - Developer documentation

---

## Troubleshooting

### MCP Server Not Showing in Claude Desktop

1. **Check config path**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Validate JSON**: Ensure no trailing commas, proper quotes

3. **Check logs**: Claude Desktop → Developer → View Logs

4. **Restart Claude Desktop**: Fully quit and reopen

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall in editable mode
pip install -e .[dev]
```

### Tests Failing

```bash
# Check Python version
python --version  # Should be 3.9+

# Run tests with verbose output
pytest -v

# Check coverage
pytest --cov=weather_mcp
```

---

## Summary

You've created a production-ready **capability server with MCP interface** in **5-10 minutes** with:

1. ✅ Multi-interface architecture (CLI, REST, MCP)
2. ✅ Full testing infrastructure
3. ✅ CI/CD pipelines
4. ✅ Quality gates (ruff, mypy)
5. ✅ Task tracking (beads)
6. ✅ Memory system (A-MEM)
7. ✅ Documentation structure
8. ✅ Agent awareness files
9. ✅ Your first MCP tool working in Claude Desktop

**Time saved**: 25-30 minutes (vs. manual setup)

**Next**: Build more tools, add resources, deploy to production!

---

## Resources

- **SAP-047 (Capability Server Template)**: [docs/skilled-awareness/capability-server-template/](../skilled-awareness/capability-server-template/)
- **SAP-042 (Interface Design)**: [docs/skilled-awareness/interface-design/](../skilled-awareness/interface-design/)
- **SAP-043 (Multi-Interface)**: [docs/skilled-awareness/multi-interface/](../skilled-awareness/multi-interface/)
- **SAP-014 (MCP Server Development)**: ⚠️ **DEPRECATED** - Use SAP-047 instead
- **SAP-003 (Project Bootstrap)**: [docs/skilled-awareness/project-bootstrap/](../skilled-awareness/project-bootstrap/)
- **Chora MCP Conventions v1.0**: [docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md](../standards/CHORA_MCP_CONVENTIONS_v1.0.md)
- **FastMCP Documentation**: [FastMCP API Reference](reference/fastmcp-api-reference.md)
- **MCP Protocol Spec**: [MCP Protocol Specification](reference/mcp-protocol-spec.md)

---

**Questions?** Check [AGENTS.md](../../AGENTS.md) for common patterns or create an issue in the chora-base repository.

**Feedback?** We'd love to hear how fast-setup worked for you! Share your experience in [chora-base discussions](https://github.com/liminalcommons/chora-base/discussions).
