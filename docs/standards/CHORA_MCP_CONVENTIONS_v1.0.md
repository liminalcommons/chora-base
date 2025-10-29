# Chora MCP Conventions v1.0

**Version**: 1.0.0
**Status**: Stable
**Date**: 2025-10-29
**Applies to**: Model Context Protocol (MCP) servers in the Chora ecosystem

---

## Overview

The Chora MCP Conventions provide standardized naming, namespacing, and URI patterns for Model Context Protocol (MCP) servers. These conventions ensure consistency, discoverability, and composability across the Chora ecosystem and beyond.

**Purpose**:
- Enable AI assistants to discover and understand MCP server capabilities
- Prevent tool name collisions when multiple MCP servers are active
- Support composability (servers referencing other servers' tools)
- Facilitate ecosystem coordination and registry management

**Compliance**: Optional but strongly recommended for all MCP servers in the Chora ecosystem.

---

## Scope

This specification covers:
- ✅ Namespace format rules
- ✅ Tool naming conventions
- ✅ Resource URI patterns
- ✅ Validation patterns
- ✅ Registry coordination

This specification does NOT cover:
- ❌ MCP protocol implementation details (see [MCP Specification](https://modelcontextprotocol.io/specification))
- ❌ Tool/resource semantics or behavior
- ❌ Authentication or authorization
- ❌ Programming language-specific implementations

---

## Namespace Format

### Rule N1: Namespace Structure

**Format**: `[a-z][a-z0-9]{2,19}`

**Requirements**:
- **Length**: 3-20 characters
- **Characters**: Lowercase alphanumeric only (`a-z`, `0-9`)
- **Start**: Must begin with a letter (`a-z`)
- **Case**: Lowercase only (no uppercase letters)
- **Special characters**: NOT allowed (no hyphens, underscores, dots)

**Rationale**:
- Lowercase prevents case-sensitivity issues across platforms
- Alphanumeric-only ensures URI compatibility
- 3-char minimum prevents overly generic namespaces
- 20-char maximum keeps namespaces concise

**Examples**:
```
✅ Valid namespaces:
- taskmanager
- chora
- choracompose
- projectmgr
- docgen

❌ Invalid namespaces:
- TaskManager       (uppercase not allowed)
- task-manager      (hyphens not allowed)
- task_manager      (underscores not allowed)
- tm                (too short - minimum 3 chars)
- verylongnamespacethatexceedslimit  (too long - maximum 20 chars)
```

---

### Rule N2: Namespace Uniqueness

**Requirement**: Namespaces MUST be unique across all MCP servers in a given deployment.

**Collision Prevention**:
1. **Search**: Check [MCP Server Registry](https://github.com/modelcontextprotocol/servers) for existing namespaces
2. **Specificity**: Use domain-specific names (not generic like "api", "data", "tools")
3. **Organizational prefix**: Consider organizational prefixes for clarity
   - Example: `acmetasks` (Acme Corp task manager)
   - Example: `globexdocs` (Globex Corp documentation)

**Handling Collisions**:
- If namespace is taken, append organizational prefix or domain qualifier
- Document namespace reservation in project README
- Submit namespace to public registries (if applicable)

---

## Tool Naming

### Rule T1: Tool Name Format

**Format**: `namespace:tool_name`

**Pattern**: `^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$`

**Requirements**:
- **Namespace part**: Follows Rule N1 (3-20 chars, lowercase, alphanumeric, starts with letter)
- **Separator**: Colon (`:`) separates namespace from tool name
- **Tool name part**: Lowercase alphanumeric + underscores, starts with letter
- **Case**: snake_case for multi-word tool names

**Rationale**:
- Colon separator is URI-safe and visually clear
- snake_case aligns with Python conventions (primary MCP SDK language)
- Namespace prefix enables tool discovery and prevents collisions

**Examples**:
```
✅ Valid tool names:
- taskmanager:create_task
- chora:generate_content
- projectmgr:list_projects
- docgen:validate

❌ Invalid tool names:
- create_task              (missing namespace)
- taskmanager-create_task  (wrong separator - should be colon)
- taskmanager:createTask   (camelCase not allowed - use snake_case)
- taskmanager:Create_Task  (uppercase not allowed)
- tm:create_task           (namespace too short)
```

---

### Rule T2: Tool Name Semantics

**Requirement**: Tool names SHOULD follow verb-noun patterns for clarity.

**Recommended patterns**:
```
create_[entity]    - Create new entity (e.g., create_task, create_project)
list_[entities]    - List multiple entities (e.g., list_tasks, list_users)
get_[entity]       - Get single entity (e.g., get_task, get_user)
update_[entity]    - Update existing entity (e.g., update_task, update_status)
delete_[entity]    - Delete entity (e.g., delete_task, delete_project)
search_[entities]  - Search entities (e.g., search_docs, search_code)
validate_[entity]  - Validate entity (e.g., validate_config, validate_data)
```

**Anti-patterns**:
```
❌ Too generic:
- taskmanager:do       (what does it do?)
- taskmanager:process  (process what?)
- taskmanager:execute  (execute what?)

❌ Too verbose:
- taskmanager:create_a_new_task_in_the_database  (overly descriptive)

❌ Unclear semantics:
- taskmanager:task  (is this create, get, or list?)
```

---

## Resource URIs

### Rule R1: Resource URI Format

**Format**: `namespace://resource_type/resource_id[?query]`

**Pattern**: `^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+(\?[a-z0-9_=&]+)?$`

**Requirements**:
- **Scheme**: Namespace (follows Rule N1) + `://`
- **Resource type**: Category or collection name (e.g., `templates`, `docs`, `data`)
- **Resource ID**: Specific resource identifier (may include slashes for hierarchy)
- **Query string**: Optional parameters (standard URL query format)

**Rationale**:
- URI format is familiar and well-understood
- Namespace as scheme prevents URI collisions
- Hierarchical paths support nested resources
- Query strings enable parameterized resources

**Examples**:
```
✅ Valid resource URIs:
- taskmanager://templates/daily-report.md
- chora://docs/getting-started
- projectmgr://data/project-123
- docgen://schemas/v1/task.json
- taskmanager://templates/report.md?format=pdf

❌ Invalid resource URIs:
- templates/daily-report.md              (missing namespace scheme)
- taskmanager:/templates/daily-report.md (missing slash in ://)
- TaskManager://templates/report.md      (uppercase in namespace)
- taskmanager://Templates/report.md      (uppercase in resource type)
```

---

### Rule R2: Resource URI Hierarchies

**Requirement**: Resource URIs MAY use hierarchical paths for organization.

**Hierarchy patterns**:
```
namespace://type/id                 - Flat structure
namespace://type/category/id        - Single-level hierarchy
namespace://type/category/sub/id    - Multi-level hierarchy
```

**Examples**:
```
✅ Hierarchical resources:
- chora://templates/daily/standup.md
- chora://templates/weekly/review.md
- projectmgr://data/2025/q1/projects
- docgen://schemas/v2/entities/task.json

✅ Flat resources:
- chora://templates/standup.md
- projectmgr://projects
- docgen://config.json
```

**Best practices**:
- Use hierarchies for large resource collections
- Keep depth reasonable (2-3 levels max)
- Use consistent naming across hierarchy levels

---

## Validation

### Rule V1: Runtime Validation

**Requirement**: MCP servers SHOULD validate namespace, tool names, and resource URIs at runtime (during server initialization).

**Validation patterns**:

```python
import re

# Namespace validation
NAMESPACE_PATTERN = r'^[a-z][a-z0-9]{2,19}$'

def validate_namespace(namespace: str) -> bool:
    """Validate namespace against Chora MCP Conventions v1.0."""
    return bool(re.match(NAMESPACE_PATTERN, namespace))

# Tool name validation
TOOL_NAME_PATTERN = r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$'

def validate_tool_name(name: str) -> bool:
    """Validate tool name against Chora MCP Conventions v1.0."""
    return bool(re.match(TOOL_NAME_PATTERN, name))

# Resource URI validation (base pattern, excludes query string)
RESOURCE_URI_PATTERN = r'^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+$'

def validate_resource_uri(uri: str) -> bool:
    """Validate resource URI against Chora MCP Conventions v1.0."""
    # Strip query string for validation
    base_uri = uri.split('?')[0]
    return bool(re.match(RESOURCE_URI_PATTERN, base_uri))
```

**Error handling**:
- If validation fails, raise descriptive error during server initialization
- Include specific violation in error message
- Provide suggestion for correction

---

### Rule V2: Optional Validation Modes

**Requirement**: MCP servers MAY provide configurable validation strictness.

**Validation modes**:
1. **Strict**: Validation enabled, server fails to start if violations found (recommended for development)
2. **Warn**: Validation enabled, warnings logged but server starts (recommended for production)
3. **Off**: Validation disabled (not recommended except for performance-critical scenarios)

**Example**:
```python
ENABLE_VALIDATION = True  # Set to False to disable
VALIDATION_MODE = "strict"  # "strict", "warn", or "off"

def make_tool_name(tool: str) -> str:
    result = f"{NAMESPACE}:{tool}"

    if ENABLE_VALIDATION:
        if not validate_tool_name(result):
            msg = f"Invalid tool name: {result}"
            if VALIDATION_MODE == "strict":
                raise ValueError(msg)
            elif VALIDATION_MODE == "warn":
                logger.warning(msg)

    return result
```

---

## Ecosystem Coordination

### Rule E1: Namespace Registration

**Requirement**: Public MCP servers SHOULD register their namespaces to prevent collisions.

**Registration process**:
1. **Search**: Check existing registries for namespace availability
2. **Document**: Add namespace to project README with usage examples
3. **Submit**: Submit PR to public MCP registries (if applicable)
4. **Update**: Keep registration updated when namespace changes

**Public registries**:
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Chora Ecosystem Registry](https://github.com/liminalcommons/chora-base) (this repository)

---

### Rule E2: Namespace Documentation

**Requirement**: MCP servers MUST document their namespace in a top-level file.

**Recommended pattern**: Create `NAMESPACE.md` or document in `README.md`:

```markdown
# MCP Server Namespace

**Namespace**: `projectmgr`
**Version**: 1.0.0
**Compliance**: Chora MCP Conventions v1.0

## Tools

- `projectmgr:create_project` - Create new project
- `projectmgr:list_projects` - List all projects
- `projectmgr:get_project` - Get project by ID

## Resources

- `projectmgr://templates/project.md` - Project template
- `projectmgr://docs/api.md` - API documentation

## Namespace Declaration

This server follows [Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md).

Namespace validation:
- Format: ✅ Valid (3-20 chars, lowercase, alphanumeric)
- Uniqueness: ✅ Verified (not found in public registries)
```

---

## Rationale and Benefits

### Why Namespacing?

**Problem without namespacing**:
- Two MCP servers with `create_task` tool → collision, only one visible
- AI assistant can't distinguish between tools from different servers
- No way to reference tools from other servers

**Solution with namespacing**:
- `projectmgr:create_task` vs `taskmanager:create_task` → no collision
- AI assistant can see all tools and understand their source
- Tools can reference each other: "Use `projectmgr:create_project` then `taskmanager:create_task`"

---

### Why URI Format for Resources?

**Benefits**:
- Familiar pattern (HTTP URIs, file:// URIs)
- Supports hierarchical organization
- Query strings enable parameterization
- Namespace as scheme prevents collisions

**Example**: Multiple servers can provide templates without collision:
```
projectmgr://templates/daily.md
taskmanager://templates/daily.md
docgen://templates/daily.md
```

---

### Why Strict Format Rules?

**Benefits**:
- **Cross-platform compatibility**: Lowercase prevents case-sensitivity issues
- **URI-safe**: Alphanumeric-only ensures no encoding needed
- **Readability**: Consistent format improves discoverability
- **Predictability**: AI assistants can infer patterns

---

## Migration Path

### From Non-Namespaced Tools

**Scenario**: Existing MCP server with non-namespaced tools (e.g., `create_task`)

**Migration steps**:

1. **Choose namespace**: Select compliant namespace (e.g., `taskmanager`)

2. **Update tool definitions**:
   ```python
   # Before (non-namespaced):
   @mcp.tool()
   def create_task(title: str) -> dict:
       ...

   # After (namespaced):
   @mcp.tool(name="taskmanager:create_task")
   def create_task(title: str) -> dict:
       ...
   ```

3. **Update resource URIs**:
   ```python
   # Before:
   @mcp.resource(uri="templates/daily.md")
   def get_template() -> str:
       ...

   # After:
   @mcp.resource(uri="taskmanager://templates/daily.md")
   def get_template() -> str:
       ...
   ```

4. **Add validation**:
   - Implement namespace validation module
   - Enable runtime validation
   - Test all tools/resources

5. **Update documentation**:
   - Add namespace declaration to README
   - Update examples to use namespaced names
   - Document migration in CHANGELOG

6. **Deprecation period** (optional):
   - Support both old and new names temporarily
   - Log warnings when old names used
   - Remove old names in next major version

---

### Version Upgrades (Future)

**If Chora MCP Conventions v2.0 is released**:

1. **Backward compatibility**: v2.0 SHOULD be backward-compatible with v1.0 where possible
2. **Migration guide**: v2.0 spec will include migration guide
3. **Deprecation period**: v1.0 will have deprecation period before removal
4. **Version declaration**: Servers can declare compliance version

---

## Compliance Levels

### Level 1: Namespace Compliant

**Requirements**:
- ✅ Namespace follows Rule N1 (format)
- ✅ Tools use namespace prefix (Rule T1)
- ✅ Resources use namespace URI scheme (Rule R1)

**Badge**: ![Chora MCP Conventions v1.0 - Level 1](https://img.shields.io/badge/Chora_MCP_Conventions-v1.0_Level_1-blue)

---

### Level 2: Validated Compliant

**Requirements**:
- ✅ All Level 1 requirements
- ✅ Runtime validation enabled (Rule V1)
- ✅ Tool names follow semantic conventions (Rule T2)

**Badge**: ![Chora MCP Conventions v1.0 - Level 2](https://img.shields.io/badge/Chora_MCP_Conventions-v1.0_Level_2-green)

---

### Level 3: Ecosystem Registered

**Requirements**:
- ✅ All Level 2 requirements
- ✅ Namespace registered in public registry (Rule E1)
- ✅ Namespace documented in project (Rule E2)

**Badge**: ![Chora MCP Conventions v1.0 - Level 3](https://img.shields.io/badge/Chora_MCP_Conventions-v1.0_Level_3-gold)

---

## Examples

### Complete Example: Task Manager MCP Server

```python
"""
Task Manager MCP Server
Compliance: Chora MCP Conventions v1.0 (Level 2)
"""
from fastmcp import FastMCP
import re

# Namespace configuration
NAMESPACE = "taskmanager"  # ✅ Compliant: 3-20 chars, lowercase, alphanumeric
VERSION = "1.0.0"
ENABLE_VALIDATION = True

# Validation patterns
NAMESPACE_PATTERN = r'^[a-z][a-z0-9]{2,19}$'
TOOL_NAME_PATTERN = r'^[a-z][a-z0-9]{2,19}:[a-z][a-z0-9_]+$'
RESOURCE_URI_PATTERN = r'^[a-z][a-z0-9]{2,19}://[a-z0-9_/\-\.]+$'

def validate_namespace(namespace: str) -> bool:
    return bool(re.match(NAMESPACE_PATTERN, namespace))

def validate_tool_name(name: str) -> bool:
    return bool(re.match(TOOL_NAME_PATTERN, name))

def validate_resource_uri(uri: str) -> bool:
    base_uri = uri.split('?')[0]
    return bool(re.match(RESOURCE_URI_PATTERN, base_uri))

def make_tool_name(tool: str) -> str:
    """Create namespaced tool name: taskmanager:tool_name"""
    result = f"{NAMESPACE}:{tool}"
    if ENABLE_VALIDATION and not validate_tool_name(result):
        raise ValueError(f"Invalid tool name: {result}")
    return result

def make_resource_uri(resource_type: str, resource_id: str) -> str:
    """Create namespaced resource URI: taskmanager://type/id"""
    uri = f"{NAMESPACE}://{resource_type}/{resource_id}"
    if ENABLE_VALIDATION and not validate_resource_uri(uri):
        raise ValueError(f"Invalid resource URI: {uri}")
    return uri

# Validate namespace on module load
if not validate_namespace(NAMESPACE):
    raise ValueError(f"Invalid namespace: {NAMESPACE}")

# Initialize MCP server
mcp = FastMCP("Task Manager")

# Tools (compliant naming)
@mcp.tool(name=make_tool_name("create_task"))  # → taskmanager:create_task
def create_task(title: str, description: str) -> dict:
    """Create a new task."""
    return {"id": "task-001", "title": title, "description": description}

@mcp.tool(name=make_tool_name("list_tasks"))  # → taskmanager:list_tasks
def list_tasks(status: str = "open") -> list:
    """List tasks by status."""
    return [{"id": "task-001", "title": "Example", "status": status}]

# Resources (compliant URIs)
@mcp.resource(uri=make_resource_uri("templates", "daily.md"))  # → taskmanager://templates/daily.md
def get_daily_template() -> str:
    """Get daily report template."""
    return "# Daily Report\n\n..."

if __name__ == "__main__":
    mcp.run()
```

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Status**: Stable

**Features**:
- Namespace format rules (Rule N1, N2)
- Tool naming conventions (Rule T1, T2)
- Resource URI patterns (Rule R1, R2)
- Validation patterns (Rule V1, V2)
- Ecosystem coordination (Rule E1, E2)
- Compliance levels (Level 1-3)

**Adoption**:
- chora-base v3.6.0+ (SAP-014)
- chora-compose v1.5.0+

---

## Related Documentation

**chora-base**:
- [SAP-014: MCP Server Development](../skilled-awareness/mcp-server-development/) - Full MCP server implementation guide
- [MCP Development Workflow](../dev-docs/workflows/mcp-development-workflow.md) - Developer workflow

**External**:
- [MCP Specification](https://modelcontextprotocol.io/specification) - Official MCP protocol spec
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - Python SDK
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers) - Public MCP servers

**Ecosystem Examples**:
- [chora-compose](https://github.com/liminalcommons/chora-compose) - Compliant MCP server (Level 3)

---

**Specification Version**: 1.0.0
**Status**: Stable
**Last Updated**: 2025-10-29
**Maintainers**: chora-base contributors
**License**: MIT
