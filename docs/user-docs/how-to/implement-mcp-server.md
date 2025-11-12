# How to Implement an MCP Server

**Last Updated**: 2025-11-12
**Time Estimate**: 5 minutes (using SAP-047 template)
**Difficulty**: Beginner

---

## ⚠️ RECOMMENDED APPROACH

**For new projects, use SAP-047 (Capability Server Template) instead of this guide.**

**Quick start**:
```bash
python scripts/create-capability-server.py \
    --name "YourCapability" \
    --namespace yournamespace \
    --enable-mcp \
    --output ~/projects/your-capability
```

**Benefits of SAP-047**:
- 5-minute setup vs 30-60 minutes manual
- Multi-interface support (CLI, REST, MCP)
- Production-ready architectural patterns
- Comprehensive documentation and tests included

**See**: [SAP-047 Adoption Blueprint](../../skilled-awareness/capability-server-template/adoption-blueprint.md)

---

## Legacy Manual Implementation (SAP-014)

This guide describes the legacy manual approach to implementing MCP-only servers. For reference only.

**Status**: This approach is deprecated as of 2025-11-12. Use SAP-047 for new projects.

---

## Overview

This guide walks you through implementing your first MCP server from scratch. For detailed reference, see [SAP-014 Adoption Blueprint](../../skilled-awareness/mcp-server-development/adoption-blueprint.md) (deprecated).

---

## Prerequisites

- ✅ Python 3.9+ installed
- ✅ Claude Desktop or MCP client installed
- ✅ Basic Python knowledge
- ✅ 30-60 minutes of time

---

## Step 1: Set Up Project

```bash
mkdir my-mcp-server && cd my-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastmcp>=0.2.0 pydantic>=2.0
```

---

## Step 2: Create Project Structure

```bash
mkdir -p my_mcp_server/mcp tests
touch my_mcp_server/__init__.py
touch my_mcp_server/mcp/__init__.py
touch my_mcp_server/server.py
touch tests/__init__.py
```

---

## Step 3: Configure Namespace

Edit `my_mcp_server/mcp/__init__.py`:

```python
import re

NAMESPACE = "myserver"  # Change this to your namespace
VERSION = "1.0.0"

def make_tool_name(tool: str) -> str:
    return f"{NAMESPACE}:{tool}"

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    return f"{NAMESPACE}://{resource_type}/{resource_id}"
```

---

## Step 4: Implement Server

Edit `my_mcp_server/server.py`:

```python
from fastmcp import FastMCP
from .mcp import make_tool_name, make_resource_uri

mcp = FastMCP("My MCP Server", version="1.0.0")

@mcp.tool(name=make_tool_name("hello"))
def hello(name: str) -> dict:
    """Say hello to someone."""
    return {"message": f"Hello, {name}!"}

@mcp.resource(uri=make_resource_uri("docs", "readme.md"))
def get_readme() -> str:
    """Get README documentation."""
    return "# My MCP Server\n\nThis is my first MCP server!"

if __name__ == "__main__":
    mcp.run()
```

---

## Step 5: Test Server

```bash
python -m my_mcp_server.server
# Server should start and wait for input
# Press Ctrl+C to stop
```

---

## Step 6: Configure Claude Desktop

Find config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add your server:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server.server"],
      "cwd": "/absolute/path/to/my-mcp-server",
      "env": {"PYTHONPATH": "/absolute/path/to/my-mcp-server"}
    }
  }
}
```

Replace `/absolute/path/to/my-mcp-server` with your actual path (run `pwd` in project directory).

---

## Step 7: Test in Claude

1. Restart Claude Desktop
2. Ask Claude: "List your available MCP tools"
3. Should see: `myserver:hello`
4. Ask Claude: "Use myserver:hello to greet Alice"
5. Should get response: `{"message": "Hello, Alice!"}`

---

## Next Steps

**Add more tools**:
```python
@mcp.tool(name=make_tool_name("add"))
def add(a: int, b: int) -> dict:
    """Add two numbers."""
    return {"result": a + b}
```

**Add resources**:
```python
@mcp.resource(uri=make_resource_uri("templates", "daily.md"))
def get_template() -> str:
    """Get daily template."""
    return "# Daily Report\n..."
```

**Add tests** (see [Test MCP Tools](test-mcp-tools.md))

**Learn more**: [SAP-014 Documentation](../../skilled-awareness/mcp-server-development/)

---

## Related Documentation

- [SAP-014 Adoption Blueprint](../../skilled-awareness/mcp-server-development/adoption-blueprint.md) - Detailed guide
- [Configure MCP Client](configure-mcp-client.md) - Client configuration
- [Test MCP Tools](test-mcp-tools.md) - Testing guide
- [FastMCP API Reference](../reference/fastmcp-api-reference.md) - API docs

---

**Last Updated**: 2025-10-29
