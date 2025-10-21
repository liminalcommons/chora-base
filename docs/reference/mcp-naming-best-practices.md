# MCP Naming Best Practices

**Audience:** chora-base adopters implementing MCP servers
**Prerequisite:** Read [CHORA_MCP_CONVENTIONS_v1.0.md](../standards/CHORA_MCP_CONVENTIONS_v1.0.md)

---

## Quick Reference

### Default Naming Pattern

```python
# Your project: my-awesome-project
# Namespace: myawesomeproject (remove hyphens)

# Tool names
myawesomeproject:create_task
myawesomeproject:list_tasks
myawesomeproject:update_task

# Resource URIs
myawesomeproject://templates/daily-report.md
myawesomeproject://configs/settings.json
myawesomeproject://capabilities/server
```

### Generated Helper Functions

chora-base generates these for you:

```python
from myawesomeproject.mcp import make_tool_name, make_resource_uri

# Tools
tool = make_tool_name("create_task")  # → "myawesomeproject:create_task"

# Resources
uri = make_resource_uri("templates", "daily-report.md")
# → "myawesomeproject://templates/daily-report.md"
```

---

## When to Use Namespacing

### ✅ Use Namespacing When:

1. **Integrating with mcp-n8n gateway**
   - Gateway routes based on namespace prefixes
   - Your tools appear alongside other backends

2. **Building for multi-server ecosystems**
   - Multiple MCP servers in same client
   - Need collision avoidance

3. **Planning for future integration**
   - Even if standalone now, ecosystem later
   - Changing namespace later is breaking change

### ❓ Optional Namespacing When:

1. **Standalone single-purpose server**
   - Only MCP server in client configuration
   - No plans for ecosystem integration

2. **Internal/private tools**
   - Not exposed via gateway
   - Controlled environment

### ❌ Don't Skip Namespacing If:

- You're unsure about future use
- Server might be shared/reused
- Part of chora ecosystem

**Default recommendation:** Always namespace (it's easier than migrating later).

---

## Choosing a Good Namespace

### Rule 1: Use Your Project Slug (Default)

```yaml
# copier.yml answers
project_slug: my-awesome-server
mcp_namespace: myawesomeserver  # Auto-derived (hyphens removed)
```

**Why this works:**
- Predictable (project name = namespace)
- Self-documenting
- Unique within your organization

### Rule 2: Keep It Short but Meaningful

```
✅ Good namespaces:
  - chora (4 chars, clear meaning)
  - coda (4 chars, product name)
  - taskmaster (10 chars, descriptive)

⚠️  Acceptable but verbose:
  - myawesomeproject (17 chars, max recommended length)

❌ Too short/cryptic:
  - mp (2 chars, too short - min 3)
  - xyz (3 chars, meaningless)
```

### Rule 3: Avoid Collisions

Check before committing:

1. **Chora Ecosystem Registry:**
   - See [CHORA_MCP_CONVENTIONS_v1.0.md § Ecosystem Registry](../standards/CHORA_MCP_CONVENTIONS_v1.0.md#ecosystem-registry)

2. **Public MCP Servers:**
   - Search GitHub: `mcp-server-{name}`
   - Check npmjs.com: `@modelcontextprotocol/*`

3. **Your Organization:**
   - Internal server registry
   - Team naming conventions

---

## Resource URI Design Patterns

### Pattern 1: Hierarchical Resources

```python
# Templates organized by type
myproject://templates/reports/daily.md
myproject://templates/reports/weekly.md
myproject://templates/emails/welcome.md

# Configs organized by environment
myproject://configs/development/settings.json
myproject://configs/production/settings.json
```

### Pattern 2: Dated Resources

```python
# Time-series data
myproject://reports/2024-01/summary.pdf
myproject://logs/2024-10-21/application.log

# Versioned artifacts
myproject://artifacts/v1.0.0/release-notes.md
myproject://artifacts/v1.1.0/release-notes.md
```

### Pattern 3: Query Parameters for Filtering

```python
# Filter by attributes
myproject://docs/project-123?status=active&format=json

# Pagination
myproject://tasks/all?limit=100&offset=200

# Date ranges
myproject://events/all?since=2024-01-01&until=2024-12-31
```

### Pattern 4: Capabilities/Metadata Resources

```python
# Server capabilities (standard across ecosystem)
myproject://capabilities/server

# Tool-specific metadata
myproject://tools/create_task/schema
myproject://tools/create_task/examples
```

---

## Common Patterns from Ecosystem

### chora-compose Pattern (Content Generation)

```python
# Tools: Action-oriented names
chora:generate_content     # Generate from template
chora:assemble_artifact    # Combine content pieces
chora:list_generators      # List available generators
chora:validate_content     # Validate config

# Resources: Type-organized
chora://capabilities/server
chora://templates/daily-report.md
chora://generators/markdown-report/schema
```

**Lessons:**
- Use verb phrases for tools (`generate_`, `assemble_`, `list_`, `validate_`)
- Group resources by type (`templates/`, `generators/`)
- Include schema resources for tool documentation

### coda Pattern (Data Operations)

```python
# Tools: CRUD operations with clear scope
coda:list_docs             # List all documents
coda:list_tables           # List tables in doc
coda:list_rows             # List rows in table
coda:create_doc            # Create new document

# Resources: Hierarchical data access
coda://docs/abc123
coda://docs/abc123/tables/grid-1
coda://docs/abc123/tables/grid-1/rows?limit=100
```

**Lessons:**
- Scope tools to specific entity types
- Use hierarchical URIs matching data structure
- Support query params for filtering/pagination

### mcp-n8n Pattern (Orchestration)

```python
# Tools: Workflow and system operations
n8n:query_events           # Query event log
n8n:trace_workflow         # Trace by trace_id
n8n:get_backend_status     # Backend health

# Resources: System metadata
n8n://events?since=2024-10-20
n8n://workflows/trace/abc123
n8n://backends/chora/status
```

**Lessons:**
- System tools use present tense verbs
- Event/trace resources use query params for time ranges
- Status/health as resources (not tools)

---

## Tool Naming Conventions

### Verb Selection

```python
# CRUD operations
create_*     # Create new entity
get_*        # Retrieve single entity
list_*       # Retrieve multiple entities
update_*     # Modify existing entity
delete_*     # Remove entity

# Processing
generate_*   # Create from template/rules
process_*    # Transform input data
validate_*   # Check correctness
analyze_*    # Extract insights

# Workflow
start_*      # Begin async process
stop_*       # Halt async process
query_*      # Search/filter data
trace_*      # Follow execution path
```

### Naming Anti-Patterns

```python
# ❌ Too vague
myproject:do_thing         # What thing?
myproject:process          # Process what?
myproject:handle           # Handle what?

# ✅ Specific and clear
myproject:create_task
myproject:process_invoice
myproject:handle_webhook_event

# ❌ Redundant namespace in tool name
myproject:myproject_create_task  # Namespace appears twice!

# ✅ Namespace only in prefix
myproject:create_task

# ❌ Inconsistent naming style
myproject:CreateTask       # PascalCase (wrong)
myproject:create-task      # kebab-case (wrong)

# ✅ Consistent snake_case
myproject:create_task
```

---

## Validation Patterns

### Runtime Validation (Always Validate)

```python
# Generated by chora-base
from myproject.mcp import validate_tool_name, NAMESPACE

@mcp.tool()
async def create_task(title: str) -> dict:
    """Create task with validation."""

    # Validate at entry point
    tool_name = f"{NAMESPACE}:create_task"
    validate_tool_name(tool_name, expected_namespace=NAMESPACE)

    # Implementation...
    return {"id": generate_uuid(), "title": title}
```

### Pre-Commit Validation (Prevent Mistakes)

```yaml
# .pre-commit-config.yaml (generated by chora-base)
- repo: local
  hooks:
    - id: validate-mcp-names
      name: Validate MCP naming conventions
      entry: python scripts/validate_mcp_names.py
      language: system
      pass_filenames: false
```

### Test Validation (Ensure Compliance)

```python
# tests/test_mcp_conventions.py (generated by chora-base)
import pytest
from myproject.mcp import NAMESPACE, make_tool_name, make_resource_uri

def test_namespace_format():
    """Namespace follows convention."""
    assert NAMESPACE.islower()
    assert NAMESPACE.isalnum()
    assert 3 <= len(NAMESPACE) <= 20

def test_tool_names_follow_convention():
    """All tool names use namespace prefix."""
    tools = ["create_task", "list_tasks", "update_task"]

    for tool in tools:
        full_name = make_tool_name(tool)
        assert full_name.startswith(f"{NAMESPACE}:")
        assert full_name == f"{NAMESPACE}:{tool}"

def test_resource_uris_follow_convention():
    """Resource URIs match pattern."""
    uri = make_resource_uri("templates", "daily-report.md")
    assert uri == f"{NAMESPACE}://templates/daily-report.md"
```

---

## Migration Strategies

### Migrating from Non-Namespaced to Namespaced

**Scenario:** You built a server without namespacing, now need ecosystem integration.

**Strategy:**

1. **Add namespace support (backward compatible):**
   ```python
   # Support both forms during transition
   @mcp.tool()
   async def call_tool(name: str, args: dict):
       # Strip namespace if present (backward compat)
       tool_name = name.split(":", 1)[-1] if ":" in name else name

       if tool_name == "create_task":
           return await create_task(args)
   ```

2. **Generate namespaced aliases:**
   ```python
   # Register both names temporarily
   @mcp.tool(name="create_task")  # Old name
   @mcp.tool(name="myproject:create_task")  # New name
   async def create_task_impl(args: dict):
       return await create_task(args)
   ```

3. **Deprecate non-namespaced version:**
   ```python
   @mcp.tool(name="create_task")
   async def create_task_legacy(args: dict):
       logger.warning(
           "Non-namespaced tool name 'create_task' is deprecated. "
           "Use 'myproject:create_task' instead."
       )
       return await create_task(args)
   ```

4. **Remove after 2 releases:**
   - Release N: Add namespaced + deprecation warning
   - Release N+1: Keep both, increase warning severity
   - Release N+2: Remove non-namespaced

### Changing Namespace (Breaking Change)

**Scenario:** Need to rename namespace (e.g., company rebrand).

**Strategy:**

```bash
# Use generated migration script
./scripts/migrate_namespace.sh old_namespace new_namespace

# Review changes
git diff

# Update ecosystem registry
# Update client configurations
# Publish breaking change release
```

---

## Troubleshooting

### Problem: Namespace collision detected

**Symptoms:**
- Gateway routing fails
- Wrong backend handles request
- Tools appear duplicated

**Solution:**
```bash
# Check ecosystem registry
grep "your_namespace" docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md

# If collision found, choose new namespace
copier update --vcs-ref=v1.8.0  # Re-run with new namespace

# Update and document
vim NAMESPACES.md  # Document new namespace
git commit -m "fix: Resolve namespace collision"
```

### Problem: Tool names don't validate

**Symptoms:**
```
ValueError: Invalid tool name: MyProject:CreateTask
```

**Solution:**
```python
# ❌ Wrong: Uppercase
"MyProject:CreateTask"

# ✅ Correct: Lowercase snake_case
"myproject:create_task"

# Use helper functions (they enforce conventions)
from myproject.mcp import make_tool_name
tool_name = make_tool_name("create_task")  # Always correct
```

### Problem: Resource URIs don't match pattern

**Symptoms:**
```
ValueError: Invalid resource URI: myproject/templates/daily-report.md
```

**Solution:**
```python
# ❌ Wrong: Missing ://
"myproject/templates/daily-report.md"

# ✅ Correct: Full URI scheme
"myproject://templates/daily-report.md"

# Use helper functions
from myproject.mcp import make_resource_uri
uri = make_resource_uri("templates", "daily-report.md")  # Always correct
```

---

## References

- [Chora MCP Conventions v1.0](../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - Full specification
- [mcp-n8n Gateway](https://github.com/liminalcommons/mcp-n8n) - Routing implementation
- [chora-compose](https://github.com/liminalcommons/chora-compose) - Reference implementation
- [Model Context Protocol](https://modelcontextprotocol.io/) - Core protocol spec

---

**Questions?** Open an issue: https://github.com/liminalcommons/chora-base/issues
