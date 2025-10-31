# MCP Development Workflow

**Workflow Type**: Development Process
**Purpose**: Guide developers through building MCP servers using DDD→BDD→TDD patterns
**Created**: 2025-10-29
**Version**: 1.0

---

## Overview

This workflow adapts SAP-012 (Development Lifecycle) for MCP server development, treating tools, resources, and prompts as domain entities.

**Pattern**: Domain-Driven Design → Behavior-Driven Development → Test-Driven Development

**For implementation details**: See [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/)

---

## Workflow Stages

### Stage 1: Domain Design (DDD)

**Goal**: Identify MCP capabilities as domain entities.

**Steps**:

1. **Identify domain boundaries**:
   - What problem does this MCP server solve?
   - What capabilities should it expose to AI assistants?
   - What data does it need to provide?

2. **Map entities to MCP primitives**:
   - **Actions** → Tools (e.g., create_task, update_status)
   - **Data sources** → Resources (e.g., templates, docs)
   - **Workflows** → Prompts (e.g., analyze_tasks)

3. **Define namespace** (Chora MCP Conventions v1.0):
   - Choose 3-20 char namespace (lowercase, alphanumeric)
   - Example: `taskmanager` for task management domain

**Example**:
```
Domain: Task Management
Entities:
  - Task (create, list, get, update, delete)
  - Template (daily report, sprint review)
  - Analysis (priority analysis, blocker detection)

MCP Mapping:
  Tools: taskmanager:create_task, taskmanager:list_tasks, ...
  Resources: taskmanager://templates/daily.md, ...
  Prompts: analyze_tasks(focus="priorities")
```

---

### Stage 2: Behavior Definition (BDD)

**Goal**: Define tool contracts and expected behaviors.

**Steps**:

1. **Write tool contracts**:
```python
# contracts/tools.py
"""
Tool: create_task
Input: {title: str, description: str, priority: int = 1}
Output: {status: str, task: {id: str, title: str, ...}}
Behavior: Creates new task, validates inputs, returns task with ID
"""
```

2. **Define resource schemas**:
```python
# contracts/resources.py
"""
Resource: taskmanager://templates/daily.md
Content-Type: text/markdown
Behavior: Returns markdown template for daily reports
"""
```

3. **Specify prompt behaviors**:
```python
# contracts/prompts.py
"""
Prompt: analyze_tasks
Parameters: {focus: "general" | "priorities" | "blockers"}
Behavior: Generates task analysis prompt based on focus
"""
```

---

### Stage 3: Test-Driven Development (TDD)

**Goal**: Write tests before implementation.

**Steps**:

1. **Write failing tests**:
```python
# tests/test_tools.py
def test_create_task():
    """Tool creates task with valid inputs."""
    result = create_task("New Task", "Description")

    assert result["status"] == "created"
    assert "id" in result["task"]

def test_create_task_validation():
    """Tool validates empty title."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("", "Description")
```

2. **Run tests** (expect failures):
```bash
pytest tests/ -v
# FAILED tests/test_tools.py::test_create_task
```

3. **Implement minimum code to pass**:
```python
# my_mcp_server/server.py
@mcp.tool(name=make_tool_name("create_task"))
def create_task(title: str, description: str) -> dict:
    """Create a new task."""
    if not title.strip():
        raise ValueError("Title cannot be empty")

    task_id = f"task-{uuid.uuid4().hex[:8]}"
    task = {"id": task_id, "title": title, "description": description}

    return {"status": "created", "task": task}
```

4. **Run tests** (expect pass):
```bash
pytest tests/ -v
# PASSED tests/test_tools.py::test_create_task
```

5. **Refactor**:
```python
# Extract validation
def validate_task_input(title: str, description: str):
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title too long (max 200 chars)")

@mcp.tool(name=make_tool_name("create_task"))
def create_task(title: str, description: str) -> dict:
    """Create a new task."""
    validate_task_input(title, description)
    # ... implementation
```

6. **Repeat** for each tool/resource/prompt.

---

## Example: Complete Workflow

### Scenario: Building Task Manager MCP Server

**Stage 1: Domain Design**

```
Domain Analysis:
- Users need to manage tasks via AI assistant
- Core operations: create, list, get, update, delete tasks
- Templates needed: daily report, sprint review
- Analysis prompts: priority analysis, blocker detection

MCP Design:
Namespace: taskmanager

Tools:
  - taskmanager:create_task(title, description, priority?)
  - taskmanager:list_tasks(status?, priority?, tag?)
  - taskmanager:get_task(task_id)
  - taskmanager:update_task(task_id, **updates)
  - taskmanager:delete_task(task_id)

Resources:
  - taskmanager://templates/daily.md
  - taskmanager://templates/sprint-review.md
  - taskmanager://tasks/{task_id} (dynamic)

Prompts:
  - analyze_tasks(focus="general|priorities|blockers")
```

**Stage 2: Behavior Definition**

```python
# contracts/create_task.md
"""
Tool: taskmanager:create_task

Input Schema:
  title: str (1-200 chars, required)
  description: str (0-2000 chars, optional)
  priority: int (1-5, optional, default: 1)
  tags: list[str] (optional)

Output Schema:
  status: "created"
  task: {
    id: str (format: "task-XXXXXXXX")
    title: str
    description: str
    priority: int
    tags: list[str]
    created_at: str (ISO 8601)
  }

Behavior:
  1. Validate inputs (title non-empty, priority 1-5)
  2. Generate unique task ID
  3. Store task in database/memory
  4. Return task with metadata

Error Cases:
  - ValueError: Empty title
  - ValueError: Priority out of range
  - RuntimeError: Storage failure
"""
```

**Stage 3: Test-Driven Development**

```python
# tests/test_create_task.py
import pytest
from my_mcp_server.server import create_task

def test_create_task_success():
    """Create task with valid inputs."""
    result = create_task("New Task", "Description", priority=2)

    assert result["status"] == "created"
    assert result["task"]["title"] == "New Task"
    assert result["task"]["priority"] == 2
    assert "id" in result["task"]
    assert result["task"]["id"].startswith("task-")

def test_create_task_empty_title():
    """Reject empty title."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("", "Description")

def test_create_task_invalid_priority():
    """Reject invalid priority."""
    with pytest.raises(ValueError, match="Priority must be 1-5"):
        create_task("Task", "Desc", priority=10)

def test_create_task_default_priority():
    """Default priority is 1."""
    result = create_task("Task", "Desc")

    assert result["task"]["priority"] == 1
```

---

## Integration with SAP-012

**SAP-012 Stage** → **MCP Adaptation**:

1. **Domain Design** → MCP capability identification (tools/resources/prompts)
2. **Behavior Definition** → MCP contracts (JSON Schema, docstrings)
3. **Test-Driven Development** → pytest for MCP tools/resources
4. **Implementation** → FastMCP decorators
5. **Integration Testing** → MCP client testing
6. **Documentation** → SAP-014 artifacts

---

## Best Practices

### DDD for MCP

**DO**:
- ✅ Map domain actions to tools
- ✅ Map domain data to resources
- ✅ Map domain workflows to prompts
- ✅ Use domain language in tool names

**DON'T**:
- ❌ Create tools for every function
- ❌ Expose internal implementation details
- ❌ Mix concerns (keep tools focused)

### BDD for MCP

**DO**:
- ✅ Write contracts before implementation
- ✅ Define clear input/output schemas
- ✅ Document error cases
- ✅ Specify expected behaviors

**DON'T**:
- ❌ Leave behaviors implicit
- ❌ Skip error case definitions
- ❌ Assume validations

### TDD for MCP

**DO**:
- ✅ Write tests first (red → green → refactor)
- ✅ Test each tool independently
- ✅ Test error cases explicitly
- ✅ Achieve 85%+ coverage

**DON'T**:
- ❌ Write tests after implementation
- ❌ Skip integration tests
- ❌ Forget async testing

---

## Tools and Automation

### Test Runner

```bash
# Run TDD cycle
pytest tests/ -v --cov=my_mcp_server --cov-report=term-missing
```

### Type Checking

```bash
# Validate type hints
mypy my_mcp_server/
```

### Linting

```bash
# Check code quality
ruff check my_mcp_server/
```

### CI/CD

See [Test MCP Tools](../../user-docs/how-to/test-mcp-tools.md#cicd-integration)

---

## Related Documentation

**SAP Documentation**:
- [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/) - Full MCP guide
- [SAP-012: Development Lifecycle](../../skilled-awareness/development-lifecycle/) - DDD→BDD→TDD base

**User Guides**:
- [Implement MCP Server](../../user-docs/how-to/implement-mcp-server.md) - Quick start
- [Test MCP Tools](../../user-docs/how-to/test-mcp-tools.md) - Testing guide
- [Why MCP Servers](../../user-docs/explanation/why-mcp-servers.md) - Conceptual understanding

**References**:
- [MCP Protocol Reference](../../user-docs/reference/mcp-protocol-spec.md) - Protocol details
- [FastMCP API Reference](../../user-docs/reference/fastmcp-api-reference.md) - API docs
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Naming standards

---

**Workflow Version**: 1.0
**Created**: 2025-10-29
**Status**: Active
