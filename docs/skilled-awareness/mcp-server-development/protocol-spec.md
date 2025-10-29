# SAP-014: MCP Server Development - Protocol Specification

**SAP ID**: SAP-014
**Version**: 1.0.0
**Protocol Version**: MCP 2024-11-05
**FastMCP Version**: >=0.2.0
**Chora MCP Conventions**: v1.0

---

## Overview

This document specifies the technical contracts, patterns, and guarantees for building MCP (Model Context Protocol) servers using the SAP-014 capability package.

**Scope**: Python-based MCP servers using FastMCP library with Chora MCP Conventions v1.0
**Audience**: AI agents, developers implementing MCP servers
**Compliance**: MCP protocol specification (2024-11-05), FastMCP API patterns

---

## Protocol Foundation

### MCP Protocol Specification

**Version**: 2024-11-05 (latest at time of SAP creation)
**Source**: https://modelcontextprotocol.io/specification
**Implementation**: FastMCP Python library (official SDK)

**Core Concepts**:
- **Tools**: Functions that AI assistants can call (request/response pattern)
- **Resources**: Data sources that AI assistants can read (URI-based access)
- **Prompts**: Pre-defined templates for AI assistant interactions
- **Transport**: JSON-RPC 2.0 over stdio, SSE, or WebSocket

### Chora MCP Conventions v1.0

**Purpose**: Standardize naming, namespacing, and URI patterns across MCP servers
**Status**: Optional but strongly recommended for interoperability
**Source**: docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md (in chora-base)

**Key Patterns**:
```
Tool Naming:      namespace:tool_name (e.g., "chora:create_task")
Resource URIs:    namespace://type/id  (e.g., "chora://templates/daily.md")
Namespace Rules:  3-20 chars, lowercase alphanumeric, starts with letter
```

**Benefits**:
- Tool discovery (AI can infer server capabilities from namespace)
- Composability (servers can reference each other's tools)
- Consistency (predictable patterns across ecosystem)

---

## Inputs

### Prerequisites

**System Requirements**:
- Python 3.9+ (for modern type hints, FastMCP compatibility)
- pip or uv (package management)
- Virtual environment (recommended)

**Development Tools**:
- pytest (testing)
- mypy (type checking)
- ruff (linting)

**MCP Client** (for testing):
- Claude Desktop, Cursor, Cline, or any MCP-compatible client

### Installation Inputs

**From SAP-014 Templates** (provided by this SAP):
```bash
# Templates location: static-template/mcp-templates/
- server.py.template          # FastMCP server entry point
- mcp__init__.py.template     # Chora MCP Conventions implementation
- pyproject.toml.template     # FastMCP dependency configuration
- AGENTS.md.template          # MCP-specific agent guidance
- CLAUDE.md.template          # MCP client configuration
- README.md.template          # MCP server documentation
- CHANGELOG.md.template       # Version history template
- ROADMAP.md.template         # Future capabilities planning
- package__init__.py.template # Python package initialization
```

**Configuration Variables** (customizable):
- `{{ project_name }}` - Human-readable project name
- `{{ package_name }}` - Python package name (snake_case)
- `{{ mcp_namespace }}` - MCP namespace (3-20 chars, lowercase)
- `{{ mcp_enable_namespacing }}` - Boolean (true/false)
- `{{ mcp_resource_uri_scheme }}` - Boolean (true/false)
- `{{ mcp_validate_names }}` - Boolean (true/false)

---

## Outputs

### Primary Deliverables

**1. FastMCP Server** (server.py):
```python
from fastmcp import FastMCP
from .mcp import make_tool_name, make_resource_uri

# Initialize server
mcp = FastMCP("{{ project_name }}")

# Tools (functions AI can call)
@mcp.tool()
def create_task(title: str, description: str) -> dict:
    """Create a new task."""
    # Implementation
    return {"status": "created", "task_id": "123"}

# Resources (data AI can read)
@mcp.resource(uri=make_resource_uri("templates", "daily.md"))
def get_template() -> str:
    """Get daily report template."""
    return "# Daily Report\\n..."

# Prompts (pre-defined interactions)
@mcp.prompt()
def project_summary() -> str:
    """Generate project summary prompt."""
    return "Analyze the project and summarize key metrics..."
```

**2. MCP Namespace Module** (mcp/__init__.py):
```python
NAMESPACE = "{{ mcp_namespace }}"

def make_tool_name(tool: str) -> str:
    """namespace:tool_name"""
    return f"{NAMESPACE}:{tool}"

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    """namespace://type/id"""
    return f"{NAMESPACE}://{resource_type}/{resource_id}"

def validate_tool_name(name: str) -> bool:
    """Validate tool name against Chora MCP Conventions v1.0"""
    return bool(re.match(r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$', name))

def validate_resource_uri(uri: str) -> bool:
    """Validate resource URI against Chora MCP Conventions v1.0"""
    return bool(re.match(r'^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+', uri))
```

**3. Dependencies** (pyproject.toml):
```toml
[project]
name = "{{ package_name }}"
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
```

**4. MCP Client Configuration** (for Claude Desktop):
```json
{
  "mcpServers": {
    "{{ project_name }}": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/{{ package_name }}",
        "run",
        "{{ package_name }}"
      ]
    }
  }
}
```

### Secondary Deliverables

**Documentation**:
- AGENTS.md - AI agent guidance for MCP server development
- CLAUDE.md - Claude-specific optimization patterns
- README.md - MCP server overview and usage
- CHANGELOG.md - Version history
- ROADMAP.md - Future capabilities

**Testing Infrastructure**:
- tests/ - pytest test suite
- tests/mcp/ - MCP-specific tests (tool/resource mocking)
- tests/conftest.py - Shared fixtures

---

## Technical Contracts

### Tool Contract

**Tool Signature**:
```python
@mcp.tool()
def tool_name(
    param1: str,           # Required parameter (type-annotated)
    param2: int = 0,       # Optional parameter with default
) -> dict | str | list:    # Return type (JSON-serializable)
    """Tool description (visible to AI assistant).

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 0)

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
        RuntimeError: When execution fails
    """
    # Implementation
    return {"status": "success", "data": ...}
```

**Naming Convention** (Chora MCP Conventions v1.0):
```python
# With namespacing (recommended):
@mcp.tool()
def create_task(...):  # → Exposed as "namespace:create_task"
    pass

# Without namespacing:
@mcp.tool()
def create_task(...):  # → Exposed as "create_task"
    pass
```

**Guarantees**:
- ✅ Type-safe (Pydantic validation on inputs/outputs)
- ✅ JSON-serializable (return types must be dict, str, list, int, float, bool, None)
- ✅ Documented (docstring visible to AI assistant)
- ✅ Error handling (exceptions converted to MCP error responses)

### Resource Contract

**Resource Signature**:
```python
@mcp.resource(uri="namespace://type/id")
def resource_name() -> str | bytes:
    """Resource description (visible to AI assistant).

    Returns:
        Resource content (text or binary)
    """
    # Implementation
    return "Resource content..."
```

**URI Pattern** (Chora MCP Conventions v1.0):
```
namespace://type/id[?query]

Examples:
- chora://templates/daily.md
- chora://docs/getting-started
- chora://data/users/123?format=json
```

**Guarantees**:
- ✅ URI-addressable (unique identifier for AI assistant)
- ✅ Content-typed (MIME type inferred from extension or explicit)
- ✅ Cacheable (AI assistant may cache resource content)

### Prompt Contract

**Prompt Signature**:
```python
@mcp.prompt()
def prompt_name(context: str = "") -> str:
    """Prompt description (visible to AI assistant).

    Args:
        context: Optional context for prompt customization

    Returns:
        Prompt text to send to AI assistant
    """
    # Implementation
    return f"Analyze {context} and summarize..."
```

**Guarantees**:
- ✅ Template-based (AI assistant fills in variables)
- ✅ Composable (prompts can reference tools/resources)
- ✅ Versioned (prompt evolution tracked in changelog)

---

## Guarantees

### Protocol Compliance

**MCP Protocol**:
- ✅ JSON-RPC 2.0 transport (handled by FastMCP)
- ✅ Tools list/call methods
- ✅ Resources list/read methods
- ✅ Prompts list/get methods
- ✅ Error handling (standard error codes)

**FastMCP SDK**:
- ✅ Decorator-based API (@mcp.tool, @mcp.resource, @mcp.prompt)
- ✅ Type safety (Pydantic validation)
- ✅ Async support (optional async def for I/O-bound operations)
- ✅ Context management (request context, cancellation)

**Chora MCP Conventions v1.0** (if enabled):
- ✅ Namespace validation (3-20 chars, lowercase, alphanumeric)
- ✅ Tool naming (namespace:tool_name, snake_case)
- ✅ Resource URIs (namespace://type/id)
- ✅ Runtime validation (optional, configurable)

### Quality Guarantees

**Type Safety**:
```python
# Type annotations enforced by mypy
def create_task(title: str, priority: int) -> dict[str, Any]:
    ...

# Pydantic validation at runtime
@mcp.tool()
def create_task(title: str, priority: int = 1) -> dict:
    if priority < 1 or priority > 5:
        raise ValueError("Priority must be 1-5")
    ...
```

**Test Coverage**:
- Target: 85%+ test coverage
- Tools: pytest for unit tests, pytest-mock for MCP mocking
- Pattern: Test each tool/resource/prompt independently

**Error Handling**:
```python
# Exceptions converted to MCP error responses
@mcp.tool()
def risky_operation() -> dict:
    try:
        result = perform_operation()
        return {"status": "success", "data": result}
    except ValueError as e:
        # Client sees: {"error": {"code": -32602, "message": "..."}}
        raise ValueError(f"Invalid operation: {e}")
    except Exception as e:
        # Client sees: {"error": {"code": -32603, "message": "..."}}
        raise RuntimeError(f"Operation failed: {e}")
```

---

## Constraints

### Technical Limitations

**Platform**:
- Python 3.9+ required (type hints, FastMCP compatibility)
- FastMCP library (Python-only, no TypeScript/Go/Rust equivalent via this SAP)

**Performance**:
- Synchronous by default (async optional for I/O-bound operations)
- Tools timeout: 30 seconds default (configurable by MCP client)
- Resources: No streaming (full content returned)

**Transport**:
- stdio (standard for most MCP clients)
- SSE (server-sent events, for web-based clients)
- WebSocket (bidirectional, for interactive clients)

### Operational Constraints

**Deployment**:
- Local development: Runs as subprocess (stdio transport)
- Docker: Requires exposed stdio or network transport
- Production: Requires process management (systemd, Docker, k8s)

**Security**:
- No authentication (MCP clients trusted by design)
- No authorization (tools/resources exposed to all clients)
- Sandboxing: Responsibility of deployment environment

**Versioning**:
- MCP protocol evolution (client/server version negotiation)
- FastMCP API changes (dependency pinning recommended)
- Chora conventions evolution (v1.0 → v2.0 migration path TBD)

---

## Dependencies

### Required Dependencies

**Python Packages**:
```toml
fastmcp>=0.2.0       # MCP protocol implementation
pydantic>=2.0        # Data validation
```

**Development Packages**:
```toml
pytest>=8.0          # Testing framework
pytest-mock>=3.12    # Mocking for MCP tools/resources
mypy>=1.8            # Type checking
ruff>=0.2            # Linting
```

### SAP Dependencies

**SAP-003 (Project Bootstrap)**:
- Python project structure
- pyproject.toml configuration
- src/ layout

**SAP-004 (Testing Framework)**:
- pytest infrastructure
- Test organization patterns
- Coverage requirements

**SAP-012 (Development Lifecycle)**:
- DDD→BDD→TDD workflow
- MCP tool/resource as domain entities

---

## API Reference

### Core FastMCP Patterns

**Server Initialization**:
```python
from fastmcp import FastMCP

# Basic initialization
mcp = FastMCP("server-name")

# With configuration
mcp = FastMCP(
    "server-name",
    version="1.0.0",
    description="Server description",
)
```

**Tool Definition**:
```python
@mcp.tool()
def tool_name(param: str) -> dict:
    """Tool description."""
    return {"result": param}

# With explicit name (override function name)
@mcp.tool(name="custom_tool_name")
def internal_name(param: str) -> dict:
    """Tool description."""
    return {"result": param}
```

**Resource Definition**:
```python
@mcp.resource(uri="namespace://type/id")
def get_resource() -> str:
    """Resource description."""
    return "Content..."

# With dynamic URIs
@mcp.resource(uri="namespace://docs/{doc_id}")
def get_doc(doc_id: str) -> str:
    """Get document by ID."""
    return f"Document {doc_id} content..."
```

**Prompt Definition**:
```python
@mcp.prompt()
def prompt_name(context: str = "") -> str:
    """Prompt description."""
    return f"Prompt with {context}..."

# With parameters
@mcp.prompt()
def summarize(topic: str, length: int = 100) -> str:
    """Summarize topic in length words."""
    return f"Summarize {topic} in {length} words..."
```

### Chora MCP Conventions Patterns

**Namespace Management**:
```python
from .mcp import NAMESPACE, make_tool_name, make_resource_uri

# Tool naming
tool_name = make_tool_name("create_task")  # → "namespace:create_task"

# Resource URIs
resource_uri = make_resource_uri("docs", "123")  # → "namespace://docs/123"

# Validation
from .mcp import validate_tool_name, validate_resource_uri

assert validate_tool_name("chora:create_task")  # True
assert validate_resource_uri("chora://docs/123")  # True
```

---

## Implementation Patterns

### Complete Server Example

**Real-world MCP server with multiple capabilities**:

```python
"""
Example MCP server: Task Management
Demonstrates: Tools, Resources, Prompts, Error Handling, Async Operations
"""
from fastmcp import FastMCP
from pathlib import Path
from typing import Optional
import json
import asyncio

# Initialize with metadata
mcp = FastMCP(
    "Task Manager",
    version="1.0.0",
    description="Task management MCP server with templates and reporting"
)

# Namespace configuration (Chora MCP Conventions v1.0)
NAMESPACE = "taskmanager"

def make_tool_name(tool: str) -> str:
    """Create namespaced tool name: taskmanager:tool_name"""
    return f"{NAMESPACE}:{tool}"

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    """Create namespaced resource URI: taskmanager://type/id"""
    return f"{NAMESPACE}://{resource_type}/{resource_id}"

# In-memory task storage (replace with database in production)
tasks = {}
task_counter = 0

# Tool: Create Task (synchronous, simple)
@mcp.tool(name=make_tool_name("create_task"))
def create_task(
    title: str,
    description: str,
    priority: int = 1,
    tags: Optional[list[str]] = None
) -> dict:
    """Create a new task.

    Args:
        title: Task title (required)
        description: Task description (required)
        priority: Priority level 1-5 (default: 1)
        tags: Optional list of tags

    Returns:
        dict: Created task with ID and metadata

    Raises:
        ValueError: If priority is out of range
    """
    global task_counter

    # Input validation
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if priority < 1 or priority > 5:
        raise ValueError("Priority must be between 1 and 5")

    # Create task
    task_counter += 1
    task_id = f"task-{task_counter:04d}"

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "tags": tags or [],
        "status": "open",
        "created_at": "2025-10-29T12:00:00Z"  # Use datetime.utcnow() in production
    }

    tasks[task_id] = task

    return {
        "status": "created",
        "task": task
    }

# Tool: List Tasks (with filtering)
@mcp.tool(name=make_tool_name("list_tasks"))
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    tag: Optional[str] = None
) -> dict:
    """List tasks with optional filtering.

    Args:
        status: Filter by status (open, in_progress, completed)
        priority: Filter by priority (1-5)
        tag: Filter by tag

    Returns:
        dict: List of matching tasks
    """
    filtered_tasks = []

    for task in tasks.values():
        # Apply filters
        if status and task["status"] != status:
            continue
        if priority and task["priority"] != priority:
            continue
        if tag and tag not in task["tags"]:
            continue

        filtered_tasks.append(task)

    return {
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }

# Tool: Async operation (I/O-bound)
@mcp.tool(name=make_tool_name("export_tasks"))
async def export_tasks(format: str = "json") -> dict:
    """Export all tasks to file (async I/O operation).

    Args:
        format: Export format (json, csv)

    Returns:
        dict: Export result with file path
    """
    # Simulate async I/O operation
    await asyncio.sleep(0.1)

    export_path = Path(f"tasks_export.{format}")

    if format == "json":
        # Async file write (use aiofiles in production)
        with open(export_path, "w") as f:
            json.dump(list(tasks.values()), f, indent=2)
    else:
        raise ValueError(f"Unsupported format: {format}")

    return {
        "status": "exported",
        "file": str(export_path),
        "count": len(tasks)
    }

# Resource: Task templates
@mcp.resource(uri=make_resource_uri("templates", "daily-standup.md"))
def get_standup_template() -> str:
    """Daily standup task template."""
    return """# Daily Standup - {{ date }}

## What I did yesterday
- {{ task_1 }}
- {{ task_2 }}

## What I'm doing today
- {{ task_3 }}
- {{ task_4 }}

## Blockers
- {{ blocker_1 }}
"""

@mcp.resource(uri=make_resource_uri("templates", "sprint-review.md"))
def get_sprint_review_template() -> str:
    """Sprint review task template."""
    return """# Sprint Review - {{ sprint_name }}

## Completed Tasks
{{ completed_tasks }}

## Incomplete Tasks
{{ incomplete_tasks }}

## Retrospective
- **Went Well:** {{ went_well }}
- **Needs Improvement:** {{ needs_improvement }}
- **Action Items:** {{ action_items }}
"""

# Resource: Dynamic resource (task by ID)
@mcp.resource(uri=make_resource_uri("tasks", "{task_id}"))
def get_task(task_id: str) -> str:
    """Get task by ID as formatted text.

    Args:
        task_id: Task identifier (e.g., task-0001)

    Returns:
        str: Formatted task details

    Raises:
        ValueError: If task not found
    """
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")

    task = tasks[task_id]

    return f"""# {task['title']}

**ID:** {task['id']}
**Status:** {task['status']}
**Priority:** {task['priority']}/5
**Tags:** {', '.join(task['tags']) if task['tags'] else 'None'}

## Description
{task['description']}

**Created:** {task['created_at']}
"""

# Prompt: Task analysis
@mcp.prompt(name="analyze_tasks")
def analyze_tasks_prompt(focus: str = "general") -> str:
    """Generate prompt for task analysis.

    Args:
        focus: Analysis focus (general, priorities, blockers)

    Returns:
        str: Analysis prompt for AI assistant
    """
    task_list = "\n".join([
        f"- [{t['id']}] {t['title']} (Priority: {t['priority']}, Status: {t['status']})"
        for t in tasks.values()
    ])

    if focus == "priorities":
        return f"""Analyze the following tasks and identify priority misalignments:

{task_list}

Focus on:
1. High-priority tasks that should be in progress but are not
2. Low-priority tasks blocking high-priority work
3. Recommendations for priority adjustments
"""
    elif focus == "blockers":
        return f"""Analyze the following tasks and identify potential blockers:

{task_list}

Focus on:
1. Tasks with dependencies
2. Tasks stuck in "in_progress" status
3. Resource constraints
4. Recommendations for unblocking
"""
    else:
        return f"""Analyze the following task list and provide insights:

{task_list}

Provide:
1. Overall project health assessment
2. Task distribution analysis
3. Completion trends
4. Actionable recommendations
"""

# Server entry point
if __name__ == "__main__":
    mcp.run()
```

### Namespace Module (Complete Implementation)

**Full namespace module with validation** (`mcp/__init__.py`):

```python
"""
MCP Namespace Module (Chora MCP Conventions v1.0)

Provides:
- Namespace constants
- Tool naming functions
- Resource URI functions
- Validation functions
- Runtime enforcement (optional)
"""
import re
from typing import Optional

# Namespace Configuration
NAMESPACE = "taskmanager"  # 3-20 chars, lowercase alphanumeric, starts with letter
VERSION = "1.0.0"
ENABLE_VALIDATION = True  # Enable runtime validation

# Namespace Rules (Chora MCP Conventions v1.0)
NAMESPACE_PATTERN = r'^[a-z][a-z0-9]{2,19}$'
TOOL_NAME_PATTERN = r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$'
RESOURCE_URI_PATTERN = r'^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+$'

# Validation Functions

def validate_namespace(namespace: str) -> bool:
    """Validate namespace against Chora MCP Conventions v1.0.

    Rules:
    - 3-20 characters
    - Lowercase alphanumeric only
    - Must start with a letter

    Args:
        namespace: Namespace string to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_namespace("taskmanager")
        True
        >>> validate_namespace("task-manager")  # No hyphens
        False
        >>> validate_namespace("TaskManager")  # No uppercase
        False
        >>> validate_namespace("tm")  # Too short
        False
    """
    return bool(re.match(NAMESPACE_PATTERN, namespace))

def validate_tool_name(name: str) -> bool:
    """Validate tool name against Chora MCP Conventions v1.0.

    Rules:
    - Format: namespace:tool_name
    - Namespace: 3-20 chars, lowercase alphanumeric
    - Tool name: lowercase, alphanumeric + underscores

    Args:
        name: Tool name to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_tool_name("taskmanager:create_task")
        True
        >>> validate_tool_name("taskmanager:createTask")  # No camelCase
        False
        >>> validate_tool_name("create_task")  # Missing namespace
        False
    """
    return bool(re.match(TOOL_NAME_PATTERN, name))

def validate_resource_uri(uri: str) -> bool:
    """Validate resource URI against Chora MCP Conventions v1.0.

    Rules:
    - Format: namespace://type/id[?query]
    - Namespace: 3-20 chars, lowercase alphanumeric
    - Path: alphanumeric + underscores, hyphens, slashes, dots

    Args:
        uri: Resource URI to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_resource_uri("taskmanager://templates/daily.md")
        True
        >>> validate_resource_uri("TaskManager://templates/daily.md")  # No uppercase
        False
        >>> validate_resource_uri("taskmanager:/templates/daily.md")  # Missing slash
        False
    """
    return bool(re.match(RESOURCE_URI_PATTERN, uri))

# Naming Functions

def make_tool_name(tool: str) -> str:
    """Create namespaced tool name.

    Args:
        tool: Tool name (snake_case recommended)

    Returns:
        str: Namespaced tool name (namespace:tool_name)

    Raises:
        ValueError: If validation enabled and result is invalid

    Examples:
        >>> make_tool_name("create_task")
        'taskmanager:create_task'
    """
    result = f"{NAMESPACE}:{tool}"

    if ENABLE_VALIDATION and not validate_tool_name(result):
        raise ValueError(
            f"Invalid tool name: {result}\n"
            f"Must match pattern: {TOOL_NAME_PATTERN}\n"
            f"Tool part: {tool}"
        )

    return result

def make_resource_uri(resource_type: str, resource_id: str, query: Optional[str] = None) -> str:
    """Create namespaced resource URI.

    Args:
        resource_type: Resource type (e.g., 'templates', 'docs')
        resource_id: Resource identifier (e.g., 'daily.md', 'user-123')
        query: Optional query string (without '?')

    Returns:
        str: Namespaced resource URI

    Raises:
        ValueError: If validation enabled and result is invalid

    Examples:
        >>> make_resource_uri("templates", "daily.md")
        'taskmanager://templates/daily.md'
        >>> make_resource_uri("data", "user-123", "format=json")
        'taskmanager://data/user-123?format=json'
    """
    uri = f"{NAMESPACE}://{resource_type}/{resource_id}"

    if query:
        uri += f"?{query}"

    # Validate without query for pattern matching
    base_uri = uri.split("?")[0]
    if ENABLE_VALIDATION and not validate_resource_uri(base_uri):
        raise ValueError(
            f"Invalid resource URI: {uri}\n"
            f"Must match pattern: {RESOURCE_URI_PATTERN}"
        )

    return uri

def parse_tool_name(name: str) -> tuple[str, str]:
    """Parse namespaced tool name into components.

    Args:
        name: Namespaced tool name (namespace:tool_name)

    Returns:
        tuple[str, str]: (namespace, tool_name)

    Raises:
        ValueError: If name format is invalid

    Examples:
        >>> parse_tool_name("taskmanager:create_task")
        ('taskmanager', 'create_task')
    """
    if ":" not in name:
        raise ValueError(f"Tool name missing namespace: {name}")

    parts = name.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid tool name format: {name}")

    return parts[0], parts[1]

def parse_resource_uri(uri: str) -> tuple[str, str, str, Optional[str]]:
    """Parse resource URI into components.

    Args:
        uri: Resource URI (namespace://type/id[?query])

    Returns:
        tuple[str, str, str, Optional[str]]: (namespace, resource_type, resource_id, query)

    Raises:
        ValueError: If URI format is invalid

    Examples:
        >>> parse_resource_uri("taskmanager://templates/daily.md")
        ('taskmanager', 'templates', 'daily.md', None)
        >>> parse_resource_uri("taskmanager://data/user-123?format=json")
        ('taskmanager', 'data', 'user-123', 'format=json')
    """
    # Split query string
    parts = uri.split("?", 1)
    base_uri = parts[0]
    query = parts[1] if len(parts) == 2 else None

    # Parse scheme and path
    if "://" not in base_uri:
        raise ValueError(f"Invalid resource URI (missing ://): {uri}")

    scheme, path = base_uri.split("://", 1)

    # Parse path components
    path_parts = path.split("/", 1)
    if len(path_parts) != 2:
        raise ValueError(f"Invalid resource path (missing /): {uri}")

    resource_type, resource_id = path_parts

    return scheme, resource_type, resource_id, query

# Runtime Checks

def check_namespace_compliance() -> dict:
    """Check namespace configuration compliance.

    Returns:
        dict: Compliance report with validation results
    """
    report = {
        "namespace": NAMESPACE,
        "version": VERSION,
        "validation_enabled": ENABLE_VALIDATION,
        "compliant": False,
        "issues": []
    }

    if not validate_namespace(NAMESPACE):
        report["issues"].append(
            f"Namespace '{NAMESPACE}' violates Chora MCP Conventions v1.0: "
            f"Must be 3-20 chars, lowercase alphanumeric, start with letter"
        )

    if not report["issues"]:
        report["compliant"] = True

    return report

# Export public API
__all__ = [
    "NAMESPACE",
    "VERSION",
    "ENABLE_VALIDATION",
    "validate_namespace",
    "validate_tool_name",
    "validate_resource_uri",
    "make_tool_name",
    "make_resource_uri",
    "parse_tool_name",
    "parse_resource_uri",
    "check_namespace_compliance",
]
```

---

## Deployment Patterns

### Local Development (stdio)

**Claude Desktop Configuration** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "taskmanager": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourname/projects/taskmanager",
        "run",
        "taskmanager"
      ]
    }
  }
}
```

**Alternative: Direct Python execution**:
```json
{
  "mcpServers": {
    "taskmanager": {
      "command": "python",
      "args": [
        "-m",
        "taskmanager.server"
      ],
      "cwd": "/Users/yourname/projects/taskmanager",
      "env": {
        "PYTHONPATH": "/Users/yourname/projects/taskmanager"
      }
    }
  }
}
```

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy server code
COPY taskmanager/ ./taskmanager/

# Expose stdio (no port needed for stdio transport)
# For SSE/WebSocket, expose port 8000
# EXPOSE 8000

# Run MCP server
CMD ["python", "-m", "taskmanager.server"]
```

**Docker Compose** (stdio transport):
```yaml
version: '3.8'

services:
  taskmanager:
    build: .
    stdin_open: true
    tty: true
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
```

### Production Deployment (systemd)

**systemd service file** (`/etc/systemd/system/taskmanager-mcp.service`):
```ini
[Unit]
Description=Task Manager MCP Server
After=network.target

[Service]
Type=simple
User=mcp
Group=mcp
WorkingDirectory=/opt/taskmanager
Environment="PYTHONPATH=/opt/taskmanager"
ExecStart=/usr/bin/python3 -m taskmanager.server
Restart=always
RestartSec=10
StandardInput=socket
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Socket file** (`/etc/systemd/system/taskmanager-mcp.socket`):
```ini
[Unit]
Description=Task Manager MCP Server Socket

[Socket]
ListenStream=/var/run/taskmanager-mcp.sock
SocketMode=0660
SocketUser=mcp
SocketGroup=mcp

[Install]
WantedBy=sockets.target
```

---

## Advanced Patterns

### Error Handling & Logging

**Comprehensive error handling**:

```python
import logging
from fastmcp import FastMCP
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskmanager")

mcp = FastMCP("Task Manager")

class TaskError(Exception):
    """Base exception for task operations."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when task is not found."""
    pass

class TaskValidationError(TaskError):
    """Raised when task validation fails."""
    pass

@mcp.tool()
def create_task_safe(title: str, description: str) -> dict:
    """Create task with comprehensive error handling."""
    try:
        logger.info(f"Creating task: {title}")

        # Validation
        if not title or not title.strip():
            logger.warning("Task creation failed: empty title")
            raise TaskValidationError("Title cannot be empty")

        if len(title) > 200:
            logger.warning(f"Task creation failed: title too long ({len(title)} chars)")
            raise TaskValidationError("Title must be 200 characters or less")

        # Business logic
        task = {"id": "task-001", "title": title, "description": description}
        logger.info(f"Task created successfully: {task['id']}")

        return {"status": "success", "task": task}

    except TaskValidationError as e:
        # Client receives: {"error": {"code": -32602, "message": "..."}}
        logger.error(f"Validation error: {e}")
        raise ValueError(str(e))

    except TaskError as e:
        # Application-level errors
        logger.error(f"Task error: {e}")
        raise RuntimeError(f"Task operation failed: {e}")

    except Exception as e:
        # Unexpected errors
        logger.exception("Unexpected error in create_task_safe")
        raise RuntimeError(f"Internal server error: {e}")
```

### Async Operations & Concurrency

**Async I/O operations**:

```python
import asyncio
import aiofiles
from fastmcp import FastMCP

mcp = FastMCP("Async Task Manager")

@mcp.tool()
async def batch_create_tasks(tasks: list[dict]) -> dict:
    """Create multiple tasks concurrently."""

    async def create_one(task_data: dict) -> dict:
        """Create single task (simulated async I/O)."""
        await asyncio.sleep(0.1)  # Simulate database write
        return {"id": f"task-{task_data['title']}", **task_data}

    # Create all tasks concurrently
    created = await asyncio.gather(*[create_one(t) for t in tasks])

    return {
        "status": "success",
        "count": len(created),
        "tasks": created
    }

@mcp.tool()
async def export_large_dataset(query: str) -> dict:
    """Export large dataset with async file I/O."""

    # Simulate database query
    await asyncio.sleep(0.5)
    results = [{"id": i, "data": f"row-{i}"} for i in range(10000)]

    # Async file write
    async with aiofiles.open("export.json", "w") as f:
        await f.write(json.dumps(results, indent=2))

    return {
        "status": "exported",
        "file": "export.json",
        "rows": len(results)
    }
```

### State Management

**Persistent state with database**:

```python
from fastmcp import FastMCP
import sqlite3
from contextlib import contextmanager

mcp = FastMCP("Stateful Task Manager")

# Database connection pool
DB_PATH = "tasks.db"

@contextmanager
def get_db():
    """Database connection context manager."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database schema."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

@mcp.tool()
def create_task_persistent(title: str, description: str) -> dict:
    """Create task with database persistence."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        conn.commit()

        task_id = cursor.lastrowid

        # Fetch created task
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return {
            "status": "created",
            "task": dict(row)
        }

# Initialize on server start
init_db()
```

### Resource Caching

**Cacheable resources**:

```python
from fastmcp import FastMCP
from functools import lru_cache
import time

mcp = FastMCP("Cached Task Manager")

@lru_cache(maxsize=128)
def load_template(template_id: str) -> str:
    """Load template with caching (expensive operation)."""
    time.sleep(1)  # Simulate slow file I/O
    return f"# Template: {template_id}\n\nContent..."

@mcp.resource(uri="taskmanager://templates/{template_id}")
def get_template_cached(template_id: str) -> str:
    """Get template (cached on server side).

    Note: MCP clients may also cache resources.
    """
    return load_template(template_id)

# Cache invalidation
def clear_template_cache():
    """Clear template cache (e.g., after update)."""
    load_template.cache_clear()
```

### Multi-Tenant Support

**Namespace-based multi-tenancy**:

```python
from fastmcp import FastMCP

mcp = FastMCP("Multi-Tenant Task Manager")

# Tenant-specific namespaces
TENANT_NAMESPACES = {
    "acme": "acmetasks",
    "globex": "globextasks"
}

def make_tenant_tool_name(tenant_id: str, tool: str) -> str:
    """Create tenant-specific tool name."""
    namespace = TENANT_NAMESPACES.get(tenant_id, "tasks")
    return f"{namespace}:{tool}"

@mcp.tool()
def create_task_multi_tenant(
    tenant_id: str,
    title: str,
    description: str
) -> dict:
    """Create task for specific tenant."""

    # Validate tenant
    if tenant_id not in TENANT_NAMESPACES:
        raise ValueError(f"Unknown tenant: {tenant_id}")

    # Create task with tenant isolation
    task = {
        "id": f"{tenant_id}-task-001",
        "tenant_id": tenant_id,
        "title": title,
        "description": description
    }

    return {
        "status": "created",
        "task": task,
        "namespace": TENANT_NAMESPACES[tenant_id]
    }
```

---

## Testing Patterns

### Tool Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_create_task():
    """Test create_task tool."""
    # Arrange
    title = "New Task"
    description = "Task description"

    # Act
    result = create_task(title, description)

    # Assert
    assert result["status"] == "created"
    assert "task_id" in result
    assert result["task"]["title"] == title

def test_create_task_validation():
    """Test create_task input validation."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("", "description")

    with pytest.raises(ValueError, match="Priority must be"):
        create_task("Task", "desc", priority=10)

@patch("taskmanager.server.tasks", {})
def test_create_task_isolated():
    """Test create_task with isolated state."""
    result = create_task("Task", "Description")
    assert result["status"] == "created"
    # State doesn't leak between tests
```

### Resource Testing

```python
def test_get_template():
    """Test template resource."""
    # Act
    content = get_template()

    # Assert
    assert "# Daily Report" in content
    assert len(content) > 0

def test_get_standup_template_structure():
    """Test standup template structure."""
    content = get_standup_template()

    # Check required sections
    assert "## What I did yesterday" in content
    assert "## What I'm doing today" in content
    assert "## Blockers" in content

    # Check template variables
    assert "{{ date }}" in content
    assert "{{ task_1 }}" in content
```

### Async Tool Testing

```python
import pytest

@pytest.mark.asyncio
async def test_export_tasks_async():
    """Test async export operation."""
    # Arrange
    tasks = {"task-001": {"title": "Test Task"}}

    # Act
    with patch("taskmanager.server.tasks", tasks):
        result = await export_tasks(format="json")

    # Assert
    assert result["status"] == "exported"
    assert result["count"] == 1
    assert Path(result["file"]).exists()

    # Cleanup
    Path(result["file"]).unlink()
```

### MCP Client Mocking

```python
@pytest.fixture
def mock_mcp_client(mocker):
    """Mock MCP client for testing."""
    client = mocker.Mock()
    client.call_tool = mocker.AsyncMock(return_value={"result": "success"})
    client.read_resource = mocker.AsyncMock(return_value="resource content")
    return client

async def test_with_mcp_client(mock_mcp_client):
    """Test tool with mocked MCP client."""
    result = await mock_mcp_client.call_tool("tool_name", {"param": "value"})
    assert result["result"] == "success"

async def test_tool_call_error_handling(mock_mcp_client):
    """Test MCP error handling."""
    # Simulate MCP error
    mock_mcp_client.call_tool.side_effect = Exception("MCP error")

    with pytest.raises(Exception, match="MCP error"):
        await mock_mcp_client.call_tool("tool_name", {})
```

### Integration Testing

```python
import subprocess
import json

def test_mcp_server_integration():
    """Test actual MCP server via stdio."""

    # Start MCP server as subprocess
    process = subprocess.Popen(
        ["python", "-m", "taskmanager.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "taskmanager:create_task",
            "arguments": {
                "title": "Integration Test Task",
                "description": "Created via integration test"
            }
        }
    }

    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    # Read response
    response_line = process.stdout.readline()
    response = json.loads(response_line)

    # Assert
    assert response["result"]["status"] == "created"

    # Cleanup
    process.terminate()
    process.wait()
```

---

## Security Considerations

### Input Validation

**Always validate tool inputs**:

```python
from pydantic import BaseModel, Field, validator

class TaskInput(BaseModel):
    """Validated task input."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    priority: int = Field(1, ge=1, le=5)

    @validator('title')
    def title_no_special_chars(cls, v):
        """Prevent special characters in title."""
        if any(c in v for c in ['<', '>', '&', '"']):
            raise ValueError('Title contains invalid characters')
        return v

@mcp.tool()
def create_task_validated(task: TaskInput) -> dict:
    """Create task with Pydantic validation."""
    # Input automatically validated by Pydantic
    return {"status": "created", "task": task.dict()}
```

### Path Traversal Prevention

**Secure file access**:

```python
from pathlib import Path

DATA_DIR = Path("/var/lib/taskmanager/data")

@mcp.resource(uri="taskmanager://files/{file_id}")
def get_file_safe(file_id: str) -> str:
    """Get file with path traversal prevention."""

    # Resolve absolute path
    file_path = (DATA_DIR / file_id).resolve()

    # Ensure path is within DATA_DIR
    if not file_path.is_relative_to(DATA_DIR):
        raise ValueError(f"Invalid file path: {file_id}")

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File not found: {file_id}")

    return file_path.read_text()
```

### Rate Limiting

**Tool rate limiting**:

```python
from time import time
from collections import defaultdict

# Simple in-memory rate limiter
rate_limits = defaultdict(list)
RATE_LIMIT = 10  # calls per minute

def check_rate_limit(tool_name: str) -> bool:
    """Check if rate limit exceeded."""
    now = time()
    cutoff = now - 60  # 1 minute ago

    # Remove old timestamps
    rate_limits[tool_name] = [
        ts for ts in rate_limits[tool_name] if ts > cutoff
    ]

    # Check limit
    if len(rate_limits[tool_name]) >= RATE_LIMIT:
        return False

    # Record call
    rate_limits[tool_name].append(now)
    return True

@mcp.tool()
def create_task_rate_limited(title: str, description: str) -> dict:
    """Create task with rate limiting."""
    if not check_rate_limit("create_task"):
        raise RuntimeError("Rate limit exceeded. Try again later.")

    # Normal processing
    return {"status": "created"}
```

---

## Performance Optimization

### Connection Pooling

**Database connection pooling**:

```python
from contextlib import contextmanager
import sqlite3
from queue import Queue, Empty

# Connection pool
pool_size = 5
connection_pool = Queue(maxsize=pool_size)

def init_pool():
    """Initialize connection pool."""
    for _ in range(pool_size):
        conn = sqlite3.connect("tasks.db", check_same_thread=False)
        connection_pool.put(conn)

@contextmanager
def get_pooled_connection():
    """Get connection from pool."""
    conn = connection_pool.get(timeout=5)
    try:
        yield conn
    finally:
        connection_pool.put(conn)

@mcp.tool()
def create_task_pooled(title: str) -> dict:
    """Create task with connection pooling."""
    with get_pooled_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        return {"status": "created", "id": cursor.lastrowid}

init_pool()
```

### Batch Operations

**Batch processing for efficiency**:

```python
@mcp.tool()
def batch_create_tasks_optimized(tasks: list[dict]) -> dict:
    """Create multiple tasks in single transaction."""
    with get_db() as conn:
        # Single transaction for all inserts
        created_ids = []
        for task in tasks:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (task["title"], task["description"])
            )
            created_ids.append(cursor.lastrowid)

        conn.commit()

        return {
            "status": "success",
            "count": len(created_ids),
            "ids": created_ids
        }
```

### Caching Strategies

**Multi-level caching**:

```python
from functools import lru_cache
import hashlib

# Memory cache (LRU)
@lru_cache(maxsize=256)
def get_cached_resource(resource_id: str) -> str:
    """Memory-cached resource loader."""
    # Expensive operation
    return load_from_disk(resource_id)

# Content-addressable cache
def get_content_hash(content: str) -> str:
    """Generate content hash for cache key."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]

@mcp.resource(uri="taskmanager://docs/{doc_id}")
def get_doc_cached(doc_id: str) -> str:
    """Get document with content-addressable caching."""
    content = get_cached_resource(doc_id)
    content_hash = get_content_hash(content)

    # Return with ETag-like header (if MCP supports)
    return content
```

---

## Monitoring & Observability

### Logging

**Structured logging**:

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """JSON log formatter."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)

# Configure JSON logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("taskmanager")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@mcp.tool()
def create_task_logged(title: str) -> dict:
    """Create task with structured logging."""
    logger.info(
        "Tool called",
        extra={
            "tool": "create_task",
            "title_length": len(title)
        }
    )

    result = {"status": "created"}

    logger.info(
        "Tool completed",
        extra={
            "tool": "create_task",
            "result_status": result["status"]
        }
    )

    return result
```

### Metrics

**Prometheus metrics**:

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
tool_calls = Counter(
    'mcp_tool_calls_total',
    'Total tool calls',
    ['tool_name', 'status']
)

tool_duration = Histogram(
    'mcp_tool_duration_seconds',
    'Tool execution duration',
    ['tool_name']
)

# Start metrics server
start_http_server(9090)

@mcp.tool()
def create_task_monitored(title: str) -> dict:
    """Create task with metrics."""
    start = time.time()

    try:
        result = {"status": "created"}
        tool_calls.labels(tool_name="create_task", status="success").inc()
        return result
    except Exception as e:
        tool_calls.labels(tool_name="create_task", status="error").inc()
        raise
    finally:
        duration = time.time() - start
        tool_duration.labels(tool_name="create_task").observe(duration)
```

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Protocol Support**:
- MCP protocol 2024-11-05
- FastMCP >=0.2.0
- Chora MCP Conventions v1.0

**Features**:
- Tool/resource/prompt contracts
- Chora MCP Conventions implementation
- Testing patterns
- Client configuration examples

**Templates Included**:
- 9 blueprint files (from chora-base v3.5.0)
- Enhanced with protocol specifications
- Ready for customization

---

## Related Documentation

**SAP Artifacts**:
- [capability-charter.md](capability-charter.md) - Business value, ROI
- [awareness-guide.md](awareness-guide.md) - Agent workflows, common pitfalls
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adoption tracking

**External References**:
- MCP Specification: https://modelcontextprotocol.io/specification
- FastMCP Documentation: https://github.com/jlowin/fastmcp
- Chora MCP Conventions v1.0: /docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md

**4-Domain Supporting Docs** (to be created):
- /docs/dev-docs/workflows/mcp-development-workflow.md
- /docs/user-docs/how-to/implement-mcp-server.md
- /docs/user-docs/reference/mcp-protocol-spec.md
- /docs/user-docs/explanation/why-mcp-servers.md

---

**Document Version**: 1.0.0
**Protocol Version**: MCP 2024-11-05
**FastMCP Version**: >=0.2.0
**Status**: Active
**Last Updated**: 2025-10-29
