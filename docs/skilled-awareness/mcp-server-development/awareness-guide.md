# SAP-014: MCP Server Development - Awareness Guide

**SAP ID**: SAP-014
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This guide provides comprehensive awareness for AI agents and developers working with the MCP Server Development capability package (SAP-014). It covers workflows, decision trees, common pitfalls, and cross-domain integration patterns.

**Audience**: AI agents (Claude, GPT-4, etc.), developers implementing MCP servers
**Prerequisite SAPs**: SAP-003 (Project Bootstrap), SAP-004 (Testing Framework)

---

## When to Use SAP-014

### Use Case 1: Exposing Business Logic to AI Assistants

**Scenario**: You have existing Python business logic (task management, data processing, workflow automation) that you want to make accessible to Claude Desktop, Cursor, or other MCP clients.

**Why SAP-014**:
- ✅ FastMCP provides declarative API (tools, resources, prompts)
- ✅ Chora MCP Conventions ensure namespacing consistency
- ✅ Battle-tested patterns reduce setup time from 8-16h to 30-60min

**Example**:
```python
# Expose task management API as MCP tools
@mcp.tool(name="tasks:create")
def create_task(title: str, description: str) -> dict:
    return task_manager.create(title, description)

@mcp.tool(name="tasks:list")
def list_tasks(status: str = "open") -> list:
    return task_manager.query(status=status)
```

**Alternatives**:
- REST API + Claude function calling (more complex, requires API hosting)
- CLI tools + bash (limited type safety, no structured data)
- Direct code modification (not portable, breaks on updates)

---

### Use Case 2: Building Reusable AI Tool Ecosystems

**Scenario**: You're creating a suite of related tools (e.g., project management, documentation generation, code analysis) that need to work together and share namespaces.

**Why SAP-014**:
- ✅ Chora MCP Conventions v1.0 enable tool discovery across servers
- ✅ Namespace-based composability (tools can reference each other)
- ✅ Consistent naming patterns make AI assistants more effective

**Example**:
```python
# Project management server (namespace: "projectmgr")
@mcp.tool(name="projectmgr:create_issue")
def create_issue(...): ...

# Documentation server (namespace: "docgen")
@mcp.tool(name="docgen:generate_from_issue")
def generate_from_issue(issue_id: str):
    # Can reference projectmgr:create_issue in prompts
    ...
```

**Alternatives**:
- Monolithic MCP server (harder to maintain, tight coupling)
- Separate non-MCP tools (no discoverability, manual integration)

---

### Use Case 3: Providing Context to AI Assistants (Resources)

**Scenario**: You need to give AI assistants access to project templates, documentation, configuration files, or dynamic data without copying content into prompts.

**Why SAP-014**:
- ✅ MCP resources provide URI-addressable content
- ✅ AI assistants can read resources on-demand (reduces token usage)
- ✅ Cacheable resources improve performance

**Example**:
```python
# Static resource (template)
@mcp.resource(uri="templates://daily-report.md")
def get_daily_report_template() -> str:
    return Path("templates/daily-report.md").read_text()

# Dynamic resource (runtime data)
@mcp.resource(uri="project://status/{project_id}")
def get_project_status(project_id: str) -> str:
    return generate_status_report(project_id)
```

**Alternatives**:
- Paste content into prompts (wastes tokens, outdated data)
- File system access (security concerns, no namespacing)
- External APIs (more complex, requires auth)

---

### Use Case 4: Guiding AI Assistant Interactions (Prompts)

**Scenario**: You want to provide pre-defined prompt templates that AI assistants can use for common workflows (e.g., code reviews, report generation, data analysis).

**Why SAP-014**:
- ✅ MCP prompts are first-class entities (discoverable)
- ✅ Parameterized prompts adapt to context
- ✅ Versioned prompts evolve with your workflows

**Example**:
```python
@mcp.prompt(name="analyze_codebase")
def analyze_codebase_prompt(focus: str = "security") -> str:
    if focus == "security":
        return "Review the codebase for security vulnerabilities..."
    elif focus == "performance":
        return "Analyze the codebase for performance bottlenecks..."
    return "Provide a general codebase analysis..."
```

**Alternatives**:
- Manual prompt engineering (inconsistent, not reusable)
- Hardcoded system prompts (not dynamic)

---

### Use Case 5: Integrating with Existing Python Projects

**Scenario**: You already have a Python project (Django app, Flask API, data pipeline) and want to add MCP capabilities without major refactoring.

**Why SAP-014**:
- ✅ FastMCP is a library, not a framework (minimal intrusion)
- ✅ Can wrap existing functions with decorators
- ✅ Compatible with async Python (FastAPI, aiohttp, etc.)

**Example**:
```python
# Existing business logic
class TaskManager:
    def create_task(self, title: str) -> Task:
        # Existing implementation
        ...

# Add MCP wrapper
@mcp.tool(name="tasks:create")
def mcp_create_task(title: str) -> dict:
    task = task_manager.create_task(title)
    return task.to_dict()
```

**Alternatives**:
- Rewrite application as MCP-first (high effort)
- Build separate MCP server (duplicates logic)

---

## Anti-Patterns (When NOT to Use SAP-014)

### Anti-Pattern 1: Non-Python Projects

**Scenario**: Your project is written in TypeScript, Go, Rust, or another language.

**Why NOT SAP-014**:
- ❌ SAP-014 is Python-specific (FastMCP library)
- ❌ No official MCP SDKs for other languages yet (as of 2025-10-29)

**Alternative**:
- Wait for language-specific MCP SDKs
- Implement MCP protocol directly (JSON-RPC 2.0 over stdio)
- Create Python wrapper for non-Python code (FFI, subprocess)

---

### Anti-Pattern 2: Simple CLI Tools

**Scenario**: You have a simple bash script or CLI tool that doesn't need structured data or type safety.

**Why NOT SAP-014**:
- ❌ MCP overhead not justified for simple scripts
- ❌ Bash tools already work with Claude via terminal

**Alternative**:
- Keep as CLI tool, use Claude's bash tool integration
- Convert to MCP only if you need structured data or composability

---

### Anti-Pattern 3: Real-Time Streaming Data

**Scenario**: You need to stream large amounts of data (logs, video, real-time metrics) to AI assistants.

**Why NOT SAP-014**:
- ❌ MCP protocol doesn't support streaming (as of 2024-11-05 spec)
- ❌ Resources return full content, not streams

**Alternative**:
- Use WebSocket or SSE transport with chunking
- Provide paginated resources (e.g., `logs://2025-10-29?page=1`)
- Wait for MCP streaming support in future protocol versions

---

### Anti-Pattern 4: Public APIs / Multi-User Services

**Scenario**: You're building a public-facing API that needs authentication, rate limiting, and multi-user support.

**Why NOT SAP-014**:
- ❌ MCP has no built-in authentication (clients trusted by design)
- ❌ No authorization or user management
- ❌ Designed for local/trusted environments

**Alternative**:
- Build REST API with proper auth (OAuth, JWT)
- Use MCP for internal/development tools only
- Add auth layer in front of MCP server (reverse proxy, gateway)

---

## Agent Workflows

### Workflow 1: Creating a New MCP Server

**Goal**: Scaffold a new MCP server project using SAP-014 patterns.

**Steps**:

1. **Initialize Python Project** (using SAP-003):
   ```bash
   mkdir my-mcp-server && cd my-mcp-server
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install fastmcp>=0.2.0 pydantic>=2.0
   pip install --dev pytest pytest-mock mypy ruff
   ```

3. **Create Project Structure**:
   ```
   my-mcp-server/
   ├── pyproject.toml
   ├── my_mcp_server/
   │   ├── __init__.py
   │   ├── server.py          # Main server file
   │   └── mcp/
   │       └── __init__.py    # Namespace module
   └── tests/
       ├── __init__.py
       └── test_server.py
   ```

4. **Define Namespace** (`my_mcp_server/mcp/__init__.py`):
   ```python
   import re
   from typing import Optional

   NAMESPACE = "myserver"  # 3-20 chars, lowercase

   def make_tool_name(tool: str) -> str:
       return f"{NAMESPACE}:{tool}"

   def make_resource_uri(resource_type: str, resource_id: str) -> str:
       return f"{NAMESPACE}://{resource_type}/{resource_id}"

   def validate_tool_name(name: str) -> bool:
       return bool(re.match(r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$', name))
   ```

5. **Implement Server** (`my_mcp_server/server.py`):
   ```python
   from fastmcp import FastMCP
   from .mcp import make_tool_name, make_resource_uri

   mcp = FastMCP("My MCP Server")

   @mcp.tool(name=make_tool_name("hello"))
   def hello(name: str) -> dict:
       """Say hello to someone."""
       return {"message": f"Hello, {name}!"}

   @mcp.resource(uri=make_resource_uri("docs", "readme.md"))
   def get_readme() -> str:
       """Get README content."""
       return "# My MCP Server\n\nDocumentation here..."

   if __name__ == "__main__":
       mcp.run()
   ```

6. **Test Server** (`tests/test_server.py`):
   ```python
   from my_mcp_server.server import hello

   def test_hello():
       result = hello("World")
       assert result["message"] == "Hello, World!"
   ```

7. **Configure MCP Client** (Claude Desktop):
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["-m", "my_mcp_server.server"],
         "cwd": "/path/to/my-mcp-server"
       }
     }
   }
   ```

8. **Test End-to-End**:
   - Restart Claude Desktop
   - Check available tools: `myserver:hello` should appear
   - Test: Ask Claude to "use myserver:hello with name 'Claude'"

**Decision Points**:
- **Q**: Do I need async operations?
  - **A**: Use `async def` for I/O-bound tools (database, file, network)
- **Q**: Should I enable namespace validation?
  - **A**: Yes in development, optional in production (performance trade-off)

---

### Workflow 2: Adding Tools to Existing Server

**Goal**: Extend an existing MCP server with new tools.

**Steps**:

1. **Define Tool Function**:
   ```python
   @mcp.tool(name=make_tool_name("new_operation"))
   def new_operation(param1: str, param2: int = 0) -> dict:
       """Tool description visible to AI assistant.

       Args:
           param1: Description of param1
           param2: Description of param2 (default: 0)

       Returns:
           dict: Operation result

       Raises:
           ValueError: If validation fails
       """
       # Input validation
       if not param1:
           raise ValueError("param1 is required")

       # Business logic
       result = perform_operation(param1, param2)

       return {"status": "success", "data": result}
   ```

2. **Write Tests**:
   ```python
   def test_new_operation():
       result = new_operation("test", 42)
       assert result["status"] == "success"

   def test_new_operation_validation():
       with pytest.raises(ValueError, match="param1 is required"):
           new_operation("", 0)
   ```

3. **Run Tests**:
   ```bash
   pytest tests/test_server.py -v
   ```

4. **Update Documentation**:
   - Add tool to README.md tool list
   - Document parameters and return values
   - Add examples

5. **Restart MCP Server**:
   - Restart Claude Desktop or reload MCP client
   - Verify new tool appears

**Decision Points**:
- **Q**: Should I use Pydantic models for complex inputs?
  - **A**: Yes if >3 parameters or nested data structures
- **Q**: Should I batch multiple related operations into one tool?
  - **A**: Generally no (keep tools atomic), unless they form a logical transaction

---

### Workflow 3: Debugging MCP Server Issues

**Goal**: Diagnose and fix issues with MCP server behavior.

**Steps**:

1. **Enable Logging**:
   ```python
   import logging

   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   logger = logging.getLogger("myserver")

   @mcp.tool()
   def debug_tool(param: str) -> dict:
       logger.info(f"Tool called with param: {param}")
       result = process(param)
       logger.debug(f"Processing result: {result}")
       return result
   ```

2. **Check MCP Client Logs**:
   - **Claude Desktop**: Check logs at:
     - macOS: `~/Library/Logs/Claude/mcp*.log`
     - Windows: `%APPDATA%\Claude\logs\mcp*.log`
   - Look for JSON-RPC errors, connection issues

3. **Test Server Standalone**:
   ```bash
   # Run server with manual JSON-RPC input
   python -m my_mcp_server.server

   # Send test request (copy-paste JSON):
   {"jsonrpc":"2.0","id":1,"method":"tools/list"}
   ```

4. **Common Issues & Fixes**:

   **Issue**: Tool not appearing in client
   - **Check**: Namespace validation (run `validate_tool_name()`)
   - **Check**: Server restart (client may cache tool list)
   - **Check**: MCP client config (correct path, command)

   **Issue**: Tool returns error
   - **Check**: Exception in tool function (add try/except)
   - **Check**: Type validation (Pydantic errors)
   - **Check**: Return type (must be JSON-serializable)

   **Issue**: Resource not found
   - **Check**: URI pattern match (dynamic URIs need `{param}`)
   - **Check**: Resource function implementation (exceptions?)

5. **Use pytest for Isolation**:
   ```python
   @patch("my_mcp_server.server.external_dependency")
   def test_tool_isolated(mock_dep):
       mock_dep.return_value = "mocked"
       result = tool_function("test")
       assert result["status"] == "success"
   ```

**Decision Points**:
- **Q**: Should I add health check endpoints?
  - **A**: Consider @mcp.tool(name="health:check") for diagnostics
- **Q**: How verbose should logging be in production?
  - **A**: INFO for tool calls, DEBUG for development only

---

### Workflow 4: Migrating Existing Python Code to MCP

**Goal**: Wrap existing Python application with MCP interface.

**Steps**:

1. **Identify Capabilities to Expose**:
   - List public functions/methods users want AI to access
   - Group by domain (data access, processing, reporting, etc.)

2. **Create Adapter Layer**:
   ```python
   # Existing code (unchanged)
   class TaskManager:
       def create_task(self, title: str, priority: int) -> Task:
           # Existing implementation
           task = Task(title=title, priority=priority)
           self.db.save(task)
           return task

   # MCP adapter (new)
   task_manager = TaskManager()

   @mcp.tool(name="tasks:create")
   def mcp_create_task(title: str, priority: int = 1) -> dict:
       """Create a new task (MCP wrapper)."""
       task = task_manager.create_task(title, priority)
       return {
           "id": task.id,
           "title": task.title,
           "priority": task.priority,
           "created_at": task.created_at.isoformat()
       }
   ```

3. **Handle Data Serialization**:
   ```python
   from pydantic import BaseModel

   class Task(BaseModel):
       id: int
       title: str
       priority: int

   @mcp.tool()
   def mcp_get_task(task_id: int) -> dict:
       task = task_manager.get_task(task_id)
       return task.dict()  # Pydantic model to dict
   ```

4. **Expose Configuration as Resources**:
   ```python
   @mcp.resource(uri="config://app-settings")
   def get_app_settings() -> str:
       config = app.get_config()
       return json.dumps(config, indent=2)
   ```

5. **Test Both Interfaces**:
   ```python
   def test_existing_interface():
       # Test original code
       task = task_manager.create_task("Test", 1)
       assert task.title == "Test"

   def test_mcp_interface():
       # Test MCP wrapper
       result = mcp_create_task("Test", 1)
       assert result["title"] == "Test"
   ```

6. **Deploy with Minimal Changes**:
   - Run MCP server alongside existing app (separate process)
   - Or embed MCP server in existing app (shared process)

**Decision Points**:
- **Q**: Should I modify existing code?
  - **A**: No, create adapter layer (separation of concerns)
- **Q**: How to handle async existing code?
  - **A**: Use `async def` for MCP tools that call async functions

---

## Common Pitfalls

### Pitfall 1: Forgetting JSON Serialization

**Scenario**: Tool returns custom Python object, causing MCP error.

**Example (Broken)**:
```python
class Task:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

@mcp.tool()
def create_task(title: str) -> Task:  # ❌ Task is not JSON-serializable
    return Task(id=1, title=title)
```

**Fix**:
```python
@mcp.tool()
def create_task(title: str) -> dict:  # ✅ dict is JSON-serializable
    task = Task(id=1, title=title)
    return {"id": task.id, "title": task.title}

# Or use Pydantic
from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    title: str

@mcp.tool()
def create_task(title: str) -> dict:
    task = Task(id=1, title=title)
    return TaskResponse(id=task.id, title=task.title).dict()
```

**Why This Happens**: FastMCP serializes tool responses to JSON for MCP protocol. Python objects need explicit conversion.

**Prevention**: Always use JSON-serializable return types (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`).

---

### Pitfall 2: Missing Error Handling

**Scenario**: Tool throws unhandled exception, client sees cryptic error.

**Example (Broken)**:
```python
@mcp.tool()
def get_task(task_id: int) -> dict:
    task = tasks[task_id]  # ❌ KeyError if task_id not found
    return task
```

**Fix**:
```python
@mcp.tool()
def get_task(task_id: int) -> dict:
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")  # ✅ Clear error message

    task = tasks[task_id]
    return task

# Or with logging
import logging
logger = logging.getLogger(__name__)

@mcp.tool()
def get_task(task_id: int) -> dict:
    try:
        task = tasks[task_id]
        return task
    except KeyError:
        logger.error(f"Task lookup failed: {task_id}")
        raise ValueError(f"Task not found: {task_id}")
```

**Why This Happens**: MCP converts Python exceptions to JSON-RPC errors, but raw exceptions (KeyError, AttributeError) are confusing to AI assistants.

**Prevention**:
- Use `ValueError` for validation errors (MCP code: -32602)
- Use `RuntimeError` for execution errors (MCP code: -32603)
- Add clear error messages
- Log errors for debugging

---

### Pitfall 3: Blocking Operations in Tools

**Scenario**: Tool performs slow operation (network request, file I/O), blocking other tool calls.

**Example (Broken)**:
```python
import requests
import time

@mcp.tool()
def fetch_data(url: str) -> dict:
    # ❌ Synchronous blocking call (takes 2+ seconds)
    response = requests.get(url, timeout=30)
    return response.json()

@mcp.tool()
def process_file(path: str) -> dict:
    # ❌ Synchronous blocking I/O
    time.sleep(5)  # Simulate slow processing
    return {"status": "done"}
```

**Fix**:
```python
import asyncio
import aiofiles
from aiohttp import ClientSession

@mcp.tool()
async def fetch_data(url: str) -> dict:
    # ✅ Async non-blocking call
    async with ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            return await response.json()

@mcp.tool()
async def process_file(path: str) -> dict:
    # ✅ Async non-blocking I/O
    await asyncio.sleep(5)  # Simulate async processing
    async with aiofiles.open(path, "r") as f:
        content = await f.read()
    return {"status": "done", "size": len(content)}
```

**Why This Happens**: Synchronous blocking operations prevent MCP server from handling other requests. AI assistants may call multiple tools concurrently.

**Prevention**:
- Use `async def` for I/O-bound tools
- Use async libraries (aiohttp, aiofiles, asyncpg, motor)
- Profile tool execution time (log duration)

---

### Pitfall 4: Namespace Collisions

**Scenario**: Multiple MCP servers use generic namespaces, causing tool name conflicts.

**Example (Broken)**:
```python
# Server 1: tasks.py
NAMESPACE = "tasks"  # ❌ Too generic

@mcp.tool(name="tasks:create")
def create_task(...): ...

# Server 2: todo.py
NAMESPACE = "tasks"  # ❌ Collision!

@mcp.tool(name="tasks:create")  # Same name!
def create_todo(...): ...
```

**Fix**:
```python
# Server 1: tasks.py
NAMESPACE = "projecttasks"  # ✅ Specific to project domain

@mcp.tool(name="projecttasks:create")
def create_task(...): ...

# Server 2: todo.py
NAMESPACE = "personaltodo"  # ✅ Specific to personal domain

@mcp.tool(name="personaltodo:create")
def create_todo(...): ...
```

**Why This Happens**: MCP clients aggregate tools from all configured servers. Generic namespaces like "tasks", "data", "api" are likely to collide.

**Prevention**:
- Use specific namespaces (3-20 chars, describe domain)
- Check [MCP registry](https://github.com/modelcontextprotocol/servers) for existing namespaces
- Document namespace in project README
- Consider organizational prefix (e.g., "acmetasks", "globexdata")

---

### Pitfall 5: Overly Complex Tool Signatures

**Scenario**: Tool has too many parameters, making it hard for AI assistants to use correctly.

**Example (Broken)**:
```python
@mcp.tool()
def create_task(
    title: str,
    description: str,
    priority: int,
    tags: list[str],
    assignee: str,
    due_date: str,
    project_id: int,
    parent_task_id: Optional[int],
    estimated_hours: float,
    actual_hours: float,
    status: str,
    notes: str
) -> dict:  # ❌ 12 parameters! Too complex.
    ...
```

**Fix**:
```python
from pydantic import BaseModel, Field

class TaskInput(BaseModel):
    """Task creation input."""
    title: str = Field(..., description="Task title")
    description: str = Field("", description="Task description")
    priority: int = Field(1, ge=1, le=5, description="Priority (1-5)")
    tags: list[str] = Field(default_factory=list, description="Tags")
    assignee: Optional[str] = Field(None, description="Assignee username")
    due_date: Optional[str] = Field(None, description="Due date (ISO 8601)")
    project_id: Optional[int] = Field(None, description="Project ID")

@mcp.tool()
def create_task(input: TaskInput) -> dict:  # ✅ Structured input with defaults
    """Create a new task."""
    return {"id": 123, **input.dict()}

# Or split into multiple tools
@mcp.tool()
def create_simple_task(title: str, description: str = "") -> dict:
    """Create task with minimal info."""
    ...

@mcp.tool()
def set_task_assignee(task_id: int, assignee: str) -> dict:
    """Assign task to user."""
    ...
```

**Why This Happens**: Tools with many parameters are error-prone (AI assistants may pass wrong types, forget required params).

**Prevention**:
- Limit to 3-5 parameters per tool
- Use Pydantic models for complex inputs
- Provide sensible defaults
- Split into atomic operations

---

## Related Content

### 4-Domain Cross-References

**Development Documentation** (`docs/dev-docs/`):
- [MCP Development Workflow](../../dev-docs/workflows/mcp-development-workflow.md) - Step-by-step MCP development process 
- [Testing Framework](../../dev-docs/workflows/TDD_WORKFLOW.md) - TDD patterns for MCP tools
- [Git Workflows](../../dev-docs/workflows/git-workflows.md) - Version control for MCP servers

**User Documentation** (`docs/user-docs/`):
- [How to Implement MCP Server](../../user-docs/how-to/implement-mcp-server.md) - User-facing implementation guide
- [How to Configure Claude Desktop](../../user-docs/how-to/configure-mcp-client.md) - MCP client configuration
- [How to Set Up MCP Ecosystem](setup-mcp-ecosystem.md) - Complete MCP gateway + orchestration setup in 10 minutes
- [MCP Protocol Reference](../../user-docs/reference/mcp-protocol-spec.md) - Technical reference
- [Why Use MCP Servers](../../user-docs/explanation/why-mcp-servers.md) - Conceptual explanation 

**Project Documentation** (`docs/project-docs/`):
- [MCP Specificity Audit](../../project-docs/mcp-specificity-audit.md) - Analysis of MCP-specific content
- [Wave 3 Execution Plan](../../project-docs/wave-3-execution-plan.md) - SAP-014 creation roadmap
- [v4.0 Vision](../../project-docs/CHORA-BASE-4.0-VISION.md) - Universal foundation vision

**SAP Documentation** (`docs/skilled-awareness/`):
- [SAP-003: Project Bootstrap](../project-bootstrap/awareness-guide.md) - Python project structure
- [SAP-004: Testing Framework](../testing-framework/awareness-guide.md) - pytest patterns
- [SAP-007: Documentation Framework](../documentation-framework/awareness-guide.md) - Documentation standards
- [SAP-012: Development Lifecycle](../development-lifecycle/awareness-guide.md) - DDD→BDD→TDD workflow

### System Files

**Static Templates** (`/static-template/`):
- (MCP templates to be moved from blueprints/ in Phase 5)

**Scripts** (`/scripts/`):
- (MCP validation scripts to be created)

**Root Documentation** (`/`):
- [AGENTS.md](/AGENTS.md) - Agent guidance (to be generalized in Phase 4)
- [CLAUDE.md](/CLAUDE.md) - Claude-specific patterns (to be generalized in Phase 4)
- [README.md](/README.md) - Project overview (to be updated in Phase 4)

### External References

**MCP Protocol**:
- [MCP Specification](https://modelcontextprotocol.io/specification) - Official protocol spec (2024-11-05)
- [MCP GitHub](https://github.com/modelcontextprotocol/servers) - Server registry and examples
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - Python SDK

**Chora Ecosystem**:
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Namespace standards 
- [chora-compose](https://github.com/liminalcommons/chora-compose) - Content generation MCP server (example)
- [mcp-n8n](https://github.com/liminalcommons/mcp-n8n) - Workflow automation gateway

**Python Ecosystem**:
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Async patterns (compatible with FastMCP)

---

## Quick Reference

### Essential Commands

```bash
# Install dependencies
pip install fastmcp>=0.2.0 pydantic>=2.0

# Run MCP server
python -m my_mcp_server.server

# Test MCP server
pytest tests/ -v

# Type check
mypy my_mcp_server/

# Lint
ruff check my_mcp_server/
```

### Essential Patterns

```python
# Tool with validation
from pydantic import BaseModel, Field

class Input(BaseModel):
    name: str = Field(..., min_length=1)
    count: int = Field(1, ge=1, le=100)

@mcp.tool()
def process(input: Input) -> dict:
    return {"result": f"Processed {input.name} x{input.count}"}

# Async tool
@mcp.tool()
async def fetch_data(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Resource with error handling
@mcp.resource(uri="data://items/{item_id}")
def get_item(item_id: str) -> str:
    if item_id not in items:
        raise ValueError(f"Item not found: {item_id}")
    return items[item_id]

# Prompt with parameters
@mcp.prompt()
def analyze_prompt(focus: str = "general") -> str:
    return f"Analyze the data with focus on {focus}..."
```

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Features**:
- When to Use / Anti-Patterns (5 use cases, 4 anti-patterns)
- Agent Workflows (4 detailed workflows)
- Common Pitfalls (5 scenarios with fixes)
- Related Content (4-domain cross-references)

**Cross-Domain Integration**:
- 12 cross-references to dev-docs/, user-docs/, project-docs/
- 4 SAP dependencies documented
- External ecosystem references

---

## Related Documentation

**SAP-014 Artifacts**:
- [capability-charter.md](capability-charter.md) - Business value, ROI
- [protocol-spec.md](protocol-spec.md) - Technical contracts, API reference
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adoption tracking

**SAP Framework**:
- [SAP-000](../sap-framework/) - SAP framework overview
- [INDEX.md](../INDEX.md) - SAP registry

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
