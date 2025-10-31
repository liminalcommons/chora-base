# FastMCP API Reference

**Library Version**: >=0.2.0
**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Reference

---

## Overview

FastMCP is the official Python SDK for implementing MCP (Model Context Protocol) servers. This reference documents the FastMCP API for chora-base users implementing SAP-014 (MCP Server Development).

**Installation**:
```bash
pip install fastmcp>=0.2.0
```

**Official Documentation**: [https://github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)

---

## FastMCP Class

### Constructor

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name: str,                    # Server name (shown to AI assistants)
    version: str = "1.0.0",       # Server version
    description: str = "",        # Server description
)
```

**Parameters**:
- `name` (required): Human-readable server name
- `version` (optional): Semantic version (e.g., "1.0.0")
- `description` (optional): Server description for documentation

**Example**:
```python
mcp = FastMCP(
    "Task Manager",
    version="1.0.0",
    description="Task management MCP server"
)
```

---

## Decorators

### @mcp.tool()

**Purpose**: Register a function as an MCP tool (callable by AI assistants).

```python
@mcp.tool(
    name: Optional[str] = None,        # Override tool name (default: function name)
    description: Optional[str] = None  # Override description (default: docstring)
)
def tool_function(param1: str, param2: int = 0) -> dict:
    """Tool description."""
    return {"result": "success"}
```

**Parameters**:
- `name` (optional): Tool name override (default: function name with namespace)
- `description` (optional): Description override (default: function docstring)

**Return types**: JSON-serializable (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`)

**Example**:
```python
@mcp.tool(name="taskmanager:create_task")
def create_task(title: str, description: str, priority: int = 1) -> dict:
    """Create a new task.

    Args:
        title: Task title
        description: Task description
        priority: Priority (1-5, default: 1)

    Returns:
        dict: Created task with ID
    """
    return {"id": "task-001", "title": title, "priority": priority}
```

**Async support**:
```python
@mcp.tool()
async def async_tool(param: str) -> dict:
    """Async tool for I/O-bound operations."""
    await asyncio.sleep(1)
    return {"result": param}
```

---

### @mcp.resource()

**Purpose**: Register a function as an MCP resource (readable by AI assistants).

```python
@mcp.resource(
    uri: str,                          # Resource URI (required)
    name: Optional[str] = None,        # Resource name
    description: Optional[str] = None, # Resource description
    mime_type: Optional[str] = None    # MIME type (default: inferred)
)
def resource_function() -> str | bytes:
    """Resource description."""
    return "Resource content..."
```

**Parameters**:
- `uri` (required): Resource URI (e.g., "namespace://type/id")
- `name` (optional): Human-readable resource name
- `description` (optional): Resource description
- `mime_type` (optional): MIME type (default: inferred from content)

**Return types**: `str` (text) or `bytes` (binary)

**Example**:
```python
@mcp.resource(uri="taskmanager://templates/daily.md")
def get_daily_template() -> str:
    """Get daily report template."""
    return """# Daily Report

## Tasks Completed
- {{ task_1 }}

## Tasks In Progress
- {{ task_2 }}
"""
```

**Dynamic URIs**:
```python
@mcp.resource(uri="taskmanager://tasks/{task_id}")
def get_task(task_id: str) -> str:
    """Get task by ID."""
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")
    return tasks[task_id].to_markdown()
```

---

### @mcp.prompt()

**Purpose**: Register a function as an MCP prompt template.

```python
@mcp.prompt(
    name: Optional[str] = None,        # Prompt name (default: function name)
    description: Optional[str] = None  # Prompt description
)
def prompt_function(param: str = "") -> str:
    """Prompt description."""
    return f"Prompt text with {param}..."
```

**Parameters**:
- `name` (optional): Prompt name override
- `description` (optional): Description override

**Return type**: `str` (prompt text)

**Example**:
```python
@mcp.prompt(name="analyze_tasks")
def analyze_tasks_prompt(focus: str = "general") -> str:
    """Generate task analysis prompt.

    Args:
        focus: Analysis focus (general, priorities, blockers)
    """
    if focus == "priorities":
        return "Analyze tasks and identify priority misalignments..."
    return "Provide general task analysis..."
```

---

## Type Hints and Validation

### Pydantic Integration

FastMCP uses Pydantic for automatic type validation.

**Simple types**:
```python
@mcp.tool()
def simple_tool(
    string_param: str,
    int_param: int,
    float_param: float,
    bool_param: bool,
    list_param: list[str],
    dict_param: dict[str, int]
) -> dict:
    # Automatic validation of all parameters
    return {"status": "success"}
```

**Complex types with Pydantic models**:
```python
from pydantic import BaseModel, Field

class TaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    priority: int = Field(1, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)

@mcp.tool()
def create_task_validated(input: TaskInput) -> dict:
    """Create task with Pydantic validation."""
    # input.title guaranteed to be 1-200 chars
    # input.priority guaranteed to be 1-5
    return {"status": "created", "task": input.dict()}
```

---

## Running the Server

### Development Mode

```python
if __name__ == "__main__":
    mcp.run()
```

**Default transport**: stdio (standard input/output)

**Run server**:
```bash
python -m my_mcp_server.server
```

---

### Production Deployment

**With uvicorn (SSE/WebSocket)**:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
```

**With gunicorn**:
```bash
gunicorn my_mcp_server.server:mcp.app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## Error Handling

### Raising Errors

**Validation errors** (MCP code -32602):
```python
@mcp.tool()
def create_task(title: str) -> dict:
    if not title.strip():
        raise ValueError("Title cannot be empty")  # → -32602
    return {"status": "created"}
```

**Execution errors** (MCP code -32603):
```python
@mcp.tool()
def risky_operation() -> dict:
    try:
        result = perform_operation()
        return {"result": result}
    except Exception as e:
        raise RuntimeError(f"Operation failed: {e}")  # → -32603
```

---

### Custom Exception Handling

```python
from fastmcp import FastMCP

class CustomError(Exception):
    pass

mcp = FastMCP("My Server")

@mcp.tool()
def custom_error_tool() -> dict:
    try:
        # Business logic
        raise CustomError("Something went wrong")
    except CustomError as e:
        # Log for debugging
        logger.error(f"Custom error: {e}")
        # Return error to client
        raise RuntimeError(str(e))
```

---

## Async Support

### Async Tools

```python
import asyncio
import aiofiles
from aiohttp import ClientSession

@mcp.tool()
async def async_fetch(url: str) -> dict:
    """Fetch data asynchronously."""
    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return {"data": data}

@mcp.tool()
async def async_file_read(path: str) -> dict:
    """Read file asynchronously."""
    async with aiofiles.open(path, "r") as f:
        content = await f.read()
        return {"content": content, "size": len(content)}
```

---

### Mixing Sync and Async

```python
# Sync tool
@mcp.tool()
def sync_tool(param: str) -> dict:
    return {"result": param}

# Async tool
@mcp.tool()
async def async_tool(param: str) -> dict:
    await asyncio.sleep(0.1)
    return {"result": param}

# FastMCP handles both automatically
```

---

## Configuration

### Server Metadata

```python
mcp = FastMCP(
    "Task Manager",
    version="1.0.0",
    description="Task management server"
)

# Access metadata
print(mcp.name)        # "Task Manager"
print(mcp.version)     # "1.0.0"
print(mcp.description) # "Task management server"
```

---

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_mcp_server")

@mcp.tool()
def logged_tool(param: str) -> dict:
    logger.info(f"Tool called with param: {param}")
    result = process(param)
    logger.debug(f"Result: {result}")
    return result
```

---

## Best Practices

### Tool Design

**DO**:
- ✅ Use type hints for all parameters
- ✅ Provide clear docstrings
- ✅ Return JSON-serializable types
- ✅ Validate inputs explicitly
- ✅ Use async for I/O-bound operations

**DON'T**:
- ❌ Return custom Python objects
- ❌ Forget error handling
- ❌ Use blocking operations in sync tools
- ❌ Over-complicate parameter lists (>5 params)

---

### Resource Design

**DO**:
- ✅ Use consistent URI schemes
- ✅ Document URI patterns
- ✅ Handle missing resources gracefully
- ✅ Cache expensive resource loads

**DON'T**:
- ❌ Return large resources (>10MB) without pagination
- ❌ Perform expensive computations in resource functions
- ❌ Forget to validate dynamic URI parameters

---

### Prompt Design

**DO**:
- ✅ Make prompts parameterizable
- ✅ Provide sensible defaults
- ✅ Document parameter meanings
- ✅ Version prompts (track in changelog)

**DON'T**:
- ❌ Hardcode context-specific details
- ❌ Make prompts too long (>2000 chars)
- ❌ Forget to test with different parameters

---

## Related Documentation

**chora-base**:
- [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/) - Full implementation guide
- [MCP Protocol Reference](mcp-protocol-spec.md) - Protocol details
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Naming conventions

**How-to Guides**:
- [Implement MCP Server](../how-to/implement-mcp-server.md) - Step-by-step guide
- [Test MCP Tools](../how-to/test-mcp-tools.md) - Testing guide

**Workflows**:
- [MCP Development Workflow](../../dev-docs/workflows/mcp-development-workflow.md) - Developer workflow

**External**:
- [FastMCP GitHub](https://github.com/jlowin/fastmcp) - Official repository
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation

---

**Document Version**: 1.0.0
**Library Version**: >=0.2.0
**Last Updated**: 2025-10-29
**Status**: Reference
