# SAP-014: MCP Server Development - Adoption Blueprint

**SAP ID**: SAP-014
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This blueprint provides step-by-step instructions for adopting the MCP Server Development capability package (SAP-014) in your Python project. It covers prerequisites, installation, validation, and next steps.

**Time Estimate**: 30-60 minutes (first server), 10-15 minutes (subsequent servers)
**Complexity**: Intermediate (requires Python experience)
**Prerequisites**: Python 3.9+, pip or uv, MCP client (Claude Desktop, Cursor, etc.)

---

## Prerequisites

### System Requirements

**Required**:
- Python 3.9 or higher
- pip (Python package manager) or uv (fast Python installer)
- Text editor or IDE (VS Code, PyCharm, etc.)
- Terminal/command line access

**Recommended**:
- Virtual environment tool (venv, conda, virtualenv)
- Git (version control)
- pytest (testing framework)

**MCP Client** (choose one):
- [Claude Desktop](https://claude.ai/download) (recommended for beginners)
- [Cursor](https://cursor.sh/) (code editor with MCP support)
- [Cline](https://github.com/cline/cline) (VS Code extension)
- Custom MCP client (advanced users)

### Knowledge Prerequisites

**Required**:
- Basic Python programming (functions, classes, decorators)
- Command line basics (cd, ls, pip install)
- JSON basics (understanding key-value pairs)

**Helpful but not required**:
- FastAPI or Flask experience (similar patterns)
- Async Python (for advanced scenarios)
- pytest testing framework

---

## Installation Steps

### Step 1: Create Project Directory

```bash
# Create new directory for your MCP server
mkdir my-mcp-server
cd my-mcp-server

# Initialize virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

**Verification**:
```bash
which python  # Should show path inside venv/
python --version  # Should be 3.9+
```

---

### Step 2: Install Dependencies

```bash
# Install core MCP dependencies
pip install fastmcp>=0.2.0 pydantic>=2.0

# Install development dependencies (optional but recommended)
pip install pytest pytest-mock mypy ruff

# Verify installation
python -c "import fastmcp; print(f'FastMCP version: {fastmcp.__version__}')"
```

**Verification**:
```bash
pip list | grep fastmcp  # Should show fastmcp>=0.2.0
pip list | grep pydantic  # Should show pydantic>=2.0
```

**Troubleshooting**:
- If `pip install` fails, try `python -m pip install --upgrade pip` first
- If using uv: `uv pip install fastmcp>=0.2.0 pydantic>=2.0`

---

### Step 3: Create Project Structure

```bash
# Create directory structure
mkdir -p my_mcp_server/mcp
mkdir -p tests

# Create __init__.py files
touch my_mcp_server/__init__.py
touch my_mcp_server/mcp/__init__.py
touch tests/__init__.py

# Create main files
touch my_mcp_server/server.py
touch tests/test_server.py
touch pyproject.toml
touch README.md
```

**Expected structure**:
```
my-mcp-server/
├── venv/                   # Virtual environment (ignored by git)
├── my_mcp_server/          # Main package
│   ├── __init__.py
│   ├── server.py           # MCP server implementation
│   └── mcp/                # MCP namespace module
│       └── __init__.py
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_server.py
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # Project documentation
```

---

### Step 4: Configure Namespace Module

Edit `my_mcp_server/mcp/__init__.py`:

```python
"""
MCP Namespace Module (Chora MCP Conventions v1.0)

Namespace: myserver (change this to your project-specific namespace)
"""
import re
from typing import Optional

# ==============================
# CONFIGURATION (CUSTOMIZE THIS)
# ==============================

NAMESPACE = "myserver"  # 3-20 chars, lowercase alphanumeric, start with letter
VERSION = "1.0.0"
ENABLE_VALIDATION = True  # Enable runtime validation

# ==============================
# VALIDATION PATTERNS
# ==============================

NAMESPACE_PATTERN = r'^[a-z][a-z0-9]{2,19}$'
TOOL_NAME_PATTERN = r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$'
RESOURCE_URI_PATTERN = r'^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+$'

# ==============================
# NAMING FUNCTIONS
# ==============================

def make_tool_name(tool: str) -> str:
    """Create namespaced tool name: myserver:tool_name"""
    result = f"{NAMESPACE}:{tool}"
    if ENABLE_VALIDATION and not validate_tool_name(result):
        raise ValueError(f"Invalid tool name: {result}")
    return result

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    """Create namespaced resource URI: myserver://type/id"""
    uri = f"{NAMESPACE}://{resource_type}/{resource_id}"
    if ENABLE_VALIDATION and not validate_resource_uri(uri):
        raise ValueError(f"Invalid resource URI: {uri}")
    return uri

# ==============================
# VALIDATION FUNCTIONS
# ==============================

def validate_namespace(namespace: str) -> bool:
    """Validate namespace against Chora MCP Conventions v1.0."""
    return bool(re.match(NAMESPACE_PATTERN, namespace))

def validate_tool_name(name: str) -> bool:
    """Validate tool name against Chora MCP Conventions v1.0."""
    return bool(re.match(TOOL_NAME_PATTERN, name))

def validate_resource_uri(uri: str) -> bool:
    """Validate resource URI against Chora MCP Conventions v1.0."""
    return bool(re.match(RESOURCE_URI_PATTERN, uri))

# ==============================
# EXPORTS
# ==============================

__all__ = [
    "NAMESPACE",
    "VERSION",
    "make_tool_name",
    "make_resource_uri",
    "validate_namespace",
    "validate_tool_name",
    "validate_resource_uri",
]
```

**Customization**:
- Replace `"myserver"` with your project-specific namespace (3-20 chars, lowercase)
- Update `VERSION` to match your project version
- Set `ENABLE_VALIDATION = False` for production if validation overhead is a concern

**Verification**:
```bash
python -c "from my_mcp_server.mcp import NAMESPACE, make_tool_name; print(make_tool_name('hello'))"
# Should output: myserver:hello
```

---

### Step 5: Implement MCP Server

Edit `my_mcp_server/server.py`:

```python
"""
MCP Server Implementation

This is the main entry point for your MCP server.
"""
from fastmcp import FastMCP
from .mcp import make_tool_name, make_resource_uri

# Initialize MCP server
mcp = FastMCP(
    "My MCP Server",  # Server name (shown in MCP clients)
    version="1.0.0",  # Server version
    description="Example MCP server demonstrating basic capabilities"
)

# ==============================
# TOOLS (Functions AI can call)
# ==============================

@mcp.tool(name=make_tool_name("hello"))
def hello(name: str) -> dict:
    """Say hello to someone.

    Args:
        name: Name of the person to greet

    Returns:
        dict: Greeting message

    Example:
        >>> hello("Claude")
        {"message": "Hello, Claude!"}
    """
    return {
        "message": f"Hello, {name}!",
        "server": "My MCP Server"
    }

@mcp.tool(name=make_tool_name("add"))
def add(a: int, b: int) -> dict:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        dict: Sum and calculation details
    """
    result = a + b
    return {
        "operation": "add",
        "operands": [a, b],
        "result": result
    }

# ==============================
# RESOURCES (Data AI can read)
# ==============================

@mcp.resource(uri=make_resource_uri("docs", "readme.md"))
def get_readme() -> str:
    """Get README documentation."""
    return """# My MCP Server

This is an example MCP server.

## Available Tools
- hello: Say hello to someone
- add: Add two numbers

## Available Resources
- docs://readme.md: This documentation
"""

# ==============================
# PROMPTS (Pre-defined templates)
# ==============================

@mcp.prompt(name="greeting")
def greeting_prompt(name: str = "there") -> str:
    """Generate a friendly greeting prompt."""
    return f"Generate a warm, friendly greeting for {name}. Include a fun fact or interesting question to start a conversation."

# ==============================
# SERVER ENTRY POINT
# ==============================

if __name__ == "__main__":
    # Run the MCP server (stdio transport)
    mcp.run()
```

**Verification**:
```bash
python -m my_mcp_server.server
# Server should start and wait for JSON-RPC input
# Press Ctrl+C to stop
```

---

### Step 6: Write Tests

Edit `tests/test_server.py`:

```python
"""
Tests for MCP server.
"""
import pytest
from my_mcp_server.server import hello, add

def test_hello():
    """Test hello tool."""
    result = hello("World")
    assert result["message"] == "Hello, World!"
    assert "server" in result

def test_hello_custom_name():
    """Test hello with custom name."""
    result = hello("Claude")
    assert "Claude" in result["message"]

def test_add():
    """Test add tool."""
    result = add(2, 3)
    assert result["result"] == 5
    assert result["operation"] == "add"
    assert result["operands"] == [2, 3]

def test_add_negative():
    """Test add with negative numbers."""
    result = add(-5, 10)
    assert result["result"] == 5

def test_add_zero():
    """Test add with zero."""
    result = add(0, 0)
    assert result["result"] == 0
```

**Run tests**:
```bash
pytest tests/ -v

# Expected output:
# tests/test_server.py::test_hello PASSED
# tests/test_server.py::test_hello_custom_name PASSED
# tests/test_server.py::test_add PASSED
# tests/test_server.py::test_add_negative PASSED
# tests/test_server.py::test_add_zero PASSED
# ================ 5 passed in 0.05s ================
```

---

### Step 7: Configure pyproject.toml

Edit `pyproject.toml`:

```toml
[project]
name = "my-mcp-server"
version = "1.0.0"
description = "Example MCP server"
requires-python = ">=3.9"
dependencies = [
    "fastmcp>=0.2.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-mock>=3.12",
    "mypy>=1.8",
    "ruff>=0.2",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.ruff]
line-length = 100
target-version = "py39"
```

---

### Step 8: Configure MCP Client

**Claude Desktop** (macOS):

1. Open Claude Desktop configuration:
   ```bash
   # macOS
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Windows
   # notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add your MCP server:
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": [
           "-m",
           "my_mcp_server.server"
         ],
         "cwd": "/absolute/path/to/my-mcp-server",
         "env": {
           "PYTHONPATH": "/absolute/path/to/my-mcp-server"
         }
       }
     }
   }
   ```

   **Replace** `/absolute/path/to/my-mcp-server` with your actual path:
   ```bash
   pwd  # Run this in my-mcp-server/ directory
   ```

3. Restart Claude Desktop

**Alternative: Using uv**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/my-mcp-server",
        "run",
        "my_mcp_server.server"
      ]
    }
  }
}
```

### Step 9: Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the MCP Server Development capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover MCP server development patterns and tools
- Quick reference for MCP-related operations
- Links to detailed FastMCP documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### MCP Server Development

FastMCP-based Model Context Protocol server development patterns, tools, and best practices.

**Documentation**: [docs/skilled-awareness/mcp-server-development/](docs/skilled-awareness/mcp-server-development/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/mcp-server-development/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/mcp-server-development/awareness-guide.md)
- Setup: [setup-mcp-ecosystem.md](docs/skilled-awareness/mcp-server-development/setup-mcp-ecosystem.md)

**Key Patterns**:
- FastMCP server implementation
- Tool and resource definitions
- Testing with MCP Inspector
- Claude Desktop integration
```

**Validation**:
```bash
grep "MCP Server Development" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## Validation Checklist

### ✅ Step 1: Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9+

# Check FastMCP installation
python -c "import fastmcp; print(fastmcp.__version__)"  # Should print version

# Check namespace module
python -c "from my_mcp_server.mcp import NAMESPACE; print(NAMESPACE)"  # Should print "myserver"
```

### ✅ Step 2: Verify Tests Pass

```bash
pytest tests/ -v
# All tests should PASS
```

### ✅ Step 3: Verify Server Runs

```bash
python -m my_mcp_server.server
# Server should start without errors
# Press Ctrl+C to stop
```

### ✅ Step 4: Verify MCP Client Integration

1. Restart MCP client (Claude Desktop)
2. Check server status:
   - Claude Desktop: Look for "my-server" in MCP servers list
3. Test tool invocation:
   - Ask Claude: "Use myserver:hello with name 'Test'"
   - Expected response: {"message": "Hello, Test!", "server": "My MCP Server"}

### ✅ Step 5: Verify Namespace Compliance

```bash
python -c "
from my_mcp_server.mcp import validate_namespace, NAMESPACE
print('Namespace:', NAMESPACE)
print('Valid:', validate_namespace(NAMESPACE))
"
# Should print: Namespace: myserver, Valid: True
```

---

## Troubleshooting

### Issue: Server not appearing in Claude Desktop

**Symptoms**: Claude Desktop doesn't show your MCP server in the tools list.

**Solutions**:
1. **Check configuration path**:
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   # Verify path is absolute and correct
   ```

2. **Check server starts**:
   ```bash
   cd /absolute/path/to/my-mcp-server
   python -m my_mcp_server.server
   # Should start without errors
   ```

3. **Check Claude Desktop logs**:
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   # Look for errors related to your server
   ```

4. **Restart Claude Desktop completely**:
   - Quit Claude Desktop (Cmd+Q on macOS)
   - Wait 5 seconds
   - Reopen Claude Desktop

---

### Issue: Import errors when running server

**Symptoms**: `ModuleNotFoundError: No module named 'my_mcp_server'`

**Solutions**:
1. **Verify virtual environment is activated**:
   ```bash
   which python  # Should show venv/bin/python
   ```

2. **Verify PYTHONPATH in client config**:
   ```json
   {
     "env": {
       "PYTHONPATH": "/absolute/path/to/my-mcp-server"
     }
   }
   ```

3. **Try absolute imports**:
   ```python
   # In server.py, change:
   from .mcp import make_tool_name  # Relative import
   # To:
   from my_mcp_server.mcp import make_tool_name  # Absolute import
   ```

---

### Issue: Tool validation errors

**Symptoms**: `ValueError: Invalid tool name`

**Solutions**:
1. **Check namespace format**:
   - Must be 3-20 characters
   - Lowercase alphanumeric only
   - Start with a letter

2. **Check tool name format**:
   ```python
   # Valid:
   make_tool_name("hello")  # → myserver:hello ✅
   make_tool_name("create_task")  # → myserver:create_task ✅

   # Invalid:
   make_tool_name("createTask")  # camelCase not allowed ❌
   make_tool_name("my-tool")  # hyphens not allowed ❌
   ```

3. **Disable validation temporarily**:
   ```python
   # In mcp/__init__.py
   ENABLE_VALIDATION = False  # Disable for debugging
   ```

---

### Issue: JSON serialization errors

**Symptoms**: `TypeError: Object of type X is not JSON serializable`

**Solutions**:
1. **Return JSON-serializable types**:
   ```python
   # Bad:
   @mcp.tool()
   def get_task(id: int) -> Task:  # Task object ❌
       return Task(id=id)

   # Good:
   @mcp.tool()
   def get_task(id: int) -> dict:  # dict is JSON-serializable ✅
       task = Task(id=id)
       return {"id": task.id, "title": task.title}
   ```

2. **Use Pydantic .dict() method**:
   ```python
   from pydantic import BaseModel

   class Task(BaseModel):
       id: int
       title: str

   @mcp.tool()
   def get_task(id: int) -> dict:
       task = Task(id=id, title="Example")
       return task.dict()  # Convert to dict
   ```

---

## Next Steps

### Immediate Next Steps (5-10 minutes)

1. **Add your first custom tool**:
   - Think of a function your project needs
   - Add it to `server.py` with `@mcp.tool()` decorator
   - Write a test in `test_server.py`
   - Test with Claude Desktop

2. **Add a resource**:
   - Identify content AI assistants should access (docs, templates, data)
   - Add with `@mcp.resource()` decorator
   - Test with Claude: "Read the myserver://docs/readme.md resource"

3. **Update README.md**:
   - Document available tools and resources
   - Add usage examples
   - Include Claude Desktop configuration instructions

---

### Short-Term Goals (1-2 hours)

1. **Expand tool suite**:
   - Add 5-10 tools covering core functionality
   - Group related tools (e.g., tasks:create, tasks:list, tasks:update)
   - Add input validation with Pydantic

2. **Add comprehensive tests**:
   - Target 85%+ test coverage
   - Test edge cases and error handling
   - Add integration tests

3. **Improve documentation**:
   - Add docstrings with examples
   - Document error cases
   - Create user guide

---

### Long-Term Goals (1-2 weeks)

1. **Production readiness**:
   - Add logging (structured JSON logs)
   - Add error monitoring
   - Add performance metrics
   - Deploy with systemd or Docker

2. **Advanced features**:
   - Async operations for I/O-bound tools
   - Database integration (SQLite, PostgreSQL)
   - Caching for expensive operations
   - Rate limiting

3. **Ecosystem integration**:
   - Publish to MCP registry
   - Create usage examples
   - Build composable tool ecosystem

---

## Recording Your Adoption

Once you've successfully adopted SAP-014, record your adoption in [ledger.md](ledger.md):

```markdown
| Adopter | Version | Date | Project | Notes |
|---------|---------|------|---------|-------|
| Your Name | 1.0.0 | 2025-10-29 | my-mcp-server | First MCP server, 5 tools, works great! |
```

---

## Related Documentation

**SAP-014 Artifacts**:
- [capability-charter.md](capability-charter.md) - Business value, ROI
- [protocol-spec.md](protocol-spec.md) - Technical contracts, API reference
- [awareness-guide.md](awareness-guide.md) - Usage patterns, pitfalls
- [ledger.md](ledger.md) - Adoption tracking

**Templates** (Wave 3 Phase 5):
- [MCP Templates](../../../static-template/mcp-templates/) - Ready-to-use templates for MCP servers
- See [mcp-templates/README.md](../../../static-template/mcp-templates/README.md) for template variables and usage

**External Resources**:
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - FastMCP SDK reference
- [MCP Specification](https://modelcontextprotocol.io/specification) - Protocol spec
- [Claude Desktop Setup](https://claude.ai/download) - MCP client setup

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
