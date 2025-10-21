# Chora MCP Conventions v1.0

**Version:** 1.0.0
**Status:** Stable
**Adopted:** 2025-10-21
**Scope:** All chora-base generated MCP servers

---

## Overview

This document defines the **canonical naming conventions** for Model Context Protocol (MCP) tools and resources within the Chora ecosystem. These conventions ensure:

- **Interoperability** - Servers work together in multi-server environments
- **Discoverability** - Tools/resources are predictably named and documented
- **Collision Avoidance** - Namespace isolation prevents naming conflicts
- **Evolution** - Clear versioning and deprecation patterns

### Audience

- **chora-base adopters** - Generating new MCP servers
- **Ecosystem developers** - Building integrated capability servers
- **Gateway implementers** - Routing tools across multiple backends
- **AI agents** - Programmatically discovering and calling tools

---

## Principles

### 1. Namespace Everything (Ecosystem Mode)

**Rule:** All tools and resources MUST be namespaced when integrating with gateway/orchestration layers.

**Rationale:**
- Prevents collisions when multiple servers expose similar tools
- Enables routing based on namespace (e.g., `chora:*` → chora-compose backend)
- Makes tool origins explicit in traces and logs

**Example:**
```python
# ✅ GOOD - Namespaced (ecosystem-aware)
@mcp.tool()
async def call_tool(name: str, args: dict):
    if name == "myproject:create_task":  # Namespace prefix
        return await create_task(args)

# ❌ BAD - Non-namespaced (collision-prone)
@mcp.tool()
async def call_tool(name: str, args: dict):
    if name == "create_task":  # Could collide with other servers
        return await create_task(args)
```

### 2. Use Resource URIs (Not Plain Strings)

**Rule:** Resources MUST use URI-like identifiers following `{namespace}://{type}/{id}` pattern.

**Rationale:**
- Provides hierarchical organization
- Supports query parameters for filtering
- Compatible with gateway resource aggregation
- Self-documenting structure

**Example:**
```python
# ✅ GOOD - URI scheme
@mcp.resource(uri="myproject://templates/daily-report.md")
async def get_template():
    return template_content

# ❌ BAD - Plain string
@mcp.resource(uri="/templates/daily-report")  # Ambiguous namespace
async def get_template():
    return template_content
```

### 3. Prefer Evolution Over Versioning

**Rule:** Avoid versioned names (`tool_v2`) unless breaking changes are unavoidable.

**Rationale:**
- Reduces cognitive load (one canonical name)
- Simplifies discovery (no version guessing)
- Encourages backward compatibility

**Migration Path:**
1. Design for backward compatibility (add optional params)
2. If breaking change required: Add `_v2` suffix
3. Deprecate v1 (warn in logs)
4. Migrate clients (2-release cycle)
5. Remove v1

---

## Specifications

### Tool Naming

#### Format
```
{namespace}:{tool_name}

namespace   ::= [a-z][a-z0-9]{2,19}      # 3-20 chars, lowercase alphanumeric
tool_name   ::= [a-z][a-z0-9_]+          # Snake_case, lowercase
```

#### Examples
```
✅ Valid:
  - chora:generate_content
  - myproject:create_task
  - coda:list_docs
  - n8n:execute_workflow

❌ Invalid:
  - MyProject:CreateTask     # Uppercase not allowed
  - my-project:create-task   # Hyphens not allowed in tool_name
  - mp:tool                  # Namespace too short (< 3 chars)
  - create_task              # Missing namespace prefix
```

#### Helper Function Pattern
chora-base generates helper functions to ensure consistency:

```python
# Generated in src/{package}/mcp/__init__.py
NAMESPACE = "myproject"

def make_tool_name(tool: str) -> str:
    """Generate namespaced tool name."""
    return f"{NAMESPACE}:{tool}"

# Usage
tool_name = make_tool_name("create_task")  # → "myproject:create_task"
```

### Resource URI Scheme

#### Format
```
{namespace}://{resource_type}/{resource_id}[?query_params]

namespace       ::= [a-z][a-z0-9]{2,19}          # Same as tool namespace
resource_type   ::= [a-z][a-z0-9_]+              # Plural nouns (templates, configs)
resource_id     ::= [a-z0-9_\-\.]+               # Kebab-case or snake_case
query_params    ::= key=value(&key=value)*       # Optional filters
```

#### Examples
```
✅ Valid URIs:
  - myproject://templates/daily-report.md
  - myproject://configs/settings.json
  - chora://capabilities/server
  - coda://docs/abc123/tables/grid-1?limit=100
  - myproject://artifacts/2024-01/report-v2.pdf

❌ Invalid URIs:
  - myproject/templates/daily-report.md    # Missing ://
  - MyProject://Templates/DailyReport.md   # Uppercase not allowed
  - my-project://templates/daily report    # Spaces not allowed
  - templates/daily-report.md              # Missing namespace
```

#### Helper Function Pattern
```python
# Generated in src/{package}/mcp/__init__.py
def make_resource_uri(
    resource_type: str,
    resource_id: str,
    query: dict[str, str] | None = None
) -> str:
    """Generate resource URI following Chora conventions."""
    uri = f"{NAMESPACE}://{resource_type}/{resource_id}"
    if query:
        params = "&".join(f"{k}={v}" for k, v in query.items())
        uri += f"?{params}"
    return uri

# Usage
uri = make_resource_uri("templates", "daily-report.md")
# → "myproject://templates/daily-report.md"

uri = make_resource_uri("docs", "123", {"format": "json", "limit": "10"})
# → "myproject://docs/123?format=json&limit=10"
```

### Namespace Registry

#### Reserved Namespaces
The following namespaces are **reserved** for ecosystem infrastructure:

| Namespace | Owner | Purpose |
|-----------|-------|---------|
| `chora` | chora-compose | Content generation, artifact assembly |
| `coda` | mcp-server-coda | Coda document operations |
| `n8n` | mcp-n8n | Workflow orchestration, gateway routing |
| `mcp` | Core MCP | Protocol-level tools (reserved, not yet used) |

#### Choosing a Namespace

**Default:** Use your `project-slug` without hyphens.

```python
# If project_slug = "my-awesome-server"
namespace = "myawesomeserver"  # Remove hyphens

# Alternative: Abbreviated form
namespace = "mas"  # If full name is too long (discouraged unless >20 chars)
```

**Rules:**
1. Check [Chora Ecosystem Namespace Registry](#ecosystem-registry) for conflicts
2. Document in your `NAMESPACES.md` file
3. Use consistently across all tools/resources
4. Never change after first release (treat as immutable)

#### Ecosystem Registry

**Current Registered Namespaces (2025-10-21):**

| Namespace | Project | Repository | Status |
|-----------|---------|------------|--------|
| `chora` | chora-compose | [liminalcommons/chora-compose](https://github.com/liminalcommons/chora-compose) | Active |
| `coda` | mcp-server-coda | [liminalcommons/mcp-server-coda](https://github.com/liminalcommons/mcp-server-coda) | Active |
| `n8n` | mcp-n8n | [liminalcommons/mcp-n8n](https://github.com/liminalcommons/mcp-n8n) | Active |

**How to Register:**
1. Check for conflicts in table above
2. Submit PR to chora-base adding your namespace
3. Update `NAMESPACES.md` in your project
4. Announce in ecosystem discussions

---

## Validation

### Runtime Validation

chora-base generates validation functions to catch mistakes early:

```python
# Generated in src/{package}/mcp/__init__.py
import re

NAMESPACE_PATTERN = re.compile(r'^[a-z][a-z0-9]{2,19}$')
TOOL_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_]+:[a-z][a-z0-9_]+$')
RESOURCE_URI_PATTERN = re.compile(r'^[a-z][a-z0-9]+://[a-z0-9_/\-\.]+(\?.*)?$')

def validate_tool_name(name: str, expected_namespace: str | None = None) -> None:
    """Validate tool name follows Chora MCP Conventions v1.0."""
    if not TOOL_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid tool name: {name}. "
            f"Must match pattern: {expected_namespace or 'namespace'}:tool_name"
        )

    if expected_namespace:
        actual_ns, _ = name.split(":", 1)
        if actual_ns != expected_namespace:
            raise ValueError(
                f"Wrong namespace in tool name. "
                f"Expected: {expected_namespace}:*, got: {name}"
            )

def validate_resource_uri(uri: str, expected_namespace: str | None = None) -> None:
    """Validate resource URI follows Chora MCP Conventions v1.0."""
    if not RESOURCE_URI_PATTERN.match(uri):
        raise ValueError(
            f"Invalid resource URI: {uri}. "
            f"Must match pattern: namespace://type/id"
        )

    if expected_namespace:
        actual_ns = uri.split("://", 1)[0]
        if actual_ns != expected_namespace:
            raise ValueError(
                f"Wrong namespace in resource URI. "
                f"Expected: {expected_namespace}://*, got: {uri}"
            )
```

### Pre-Commit Validation

chora-base can include a pre-commit hook to validate naming conventions:

```yaml
# .pre-commit-config.yaml (generated)
- repo: local
  hooks:
    - id: validate-mcp-names
      name: Validate MCP naming conventions
      entry: python scripts/validate_mcp_names.py
      language: system
      pass_filenames: false
```

---

## Versioning & Evolution

### Backward-Compatible Changes (Preferred)

**Add optional parameters:**
```python
# v1 - Original
async def generate_content(config_id: str) -> str:
    ...

# v2 - Add optional param (backward compatible)
async def generate_content(
    config_id: str,
    format: str = "markdown"  # New optional param
) -> str:
    ...
```

**Expand return types (with defaults):**
```python
# v1 - Simple return
return {"content": "..."}

# v2 - Add metadata (clients ignore unknown fields)
return {
    "content": "...",
    "metadata": {"version": "2.0", "generated_at": "..."}  # New fields
}
```

### Breaking Changes (Last Resort)

If breaking changes are unavoidable:

1. **Add versioned tool:**
   ```python
   # Keep v1 for compatibility
   @mcp.tool()
   async def process_data(legacy_format: dict) -> dict:
       """Legacy format (deprecated)."""
       logger.warning("process_data is deprecated. Use process_data_v2.")
       return legacy_handler(legacy_format)

   # Add v2 with new signature
   @mcp.tool()
   async def process_data_v2(new_format: dict) -> dict:
       """New format (recommended)."""
       return new_handler(new_format)
   ```

2. **Deprecation timeline:**
   - **Release N:** Add `_v2`, mark v1 deprecated (warning logs)
   - **Release N+1:** Remove v1 from docs, keep implementation (error logs)
   - **Release N+2:** Remove v1 entirely

3. **Migration guide:**
   - Document in `UPGRADING.md`
   - Provide code examples
   - Offer migration script if complex

---

## Integration with mcp-n8n Gateway

chora-base servers are designed to integrate seamlessly with [mcp-n8n](https://github.com/liminalcommons/mcp-n8n), the gateway/orchestration layer.

### Gateway Routing

mcp-n8n routes tool calls based on namespace prefixes:

```python
# Gateway configuration (mcp-n8n/src/mcp_n8n/config.py)
backends = {
    "chora": BackendConfig(
        namespace="chora",
        command="chora-compose"
    ),
    "myproject": BackendConfig(
        namespace="myproject",
        command="myproject-server"  # Your chora-base server
    )
}

# Routing logic
tool_name = "myproject:create_task"
namespace, tool = tool_name.split(":", 1)  # → "myproject", "create_task"
backend = backends[namespace]  # → Route to myproject backend
result = await backend.call_tool(tool, args)
```

### Tool Discovery

Gateway aggregates tools from all backends:

```python
# List all tools across ecosystem
tools = [
    "chora:generate_content",
    "chora:assemble_artifact",
    "myproject:create_task",    # Your tools appear here
    "myproject:list_tasks",
    "coda:list_docs"
]
```

### Resource Aggregation

Gateway merges resources from all backends:

```python
# List all resources
resources = [
    "chora://capabilities/server",
    "myproject://templates/daily-report.md",  # Your resources
    "coda://docs/abc123"
]
```

---

## Examples

### Complete MCP Server (chora-base Generated)

```python
"""Example MCP server following Chora MCP Conventions v1.0."""

from fastmcp import FastMCP
from .mcp import make_tool_name, make_resource_uri, validate_tool_name

# Server metadata
mcp = FastMCP(
    name="myproject",
    version="1.0.0"
)

# Tool implementation
@mcp.tool()
async def create_task(title: str, description: str) -> dict:
    """Create a new task.

    Tool name: myproject:create_task

    Args:
        title: Task title
        description: Task description

    Returns:
        Task metadata with ID and timestamps
    """
    # Validate we're using correct naming
    tool_name = make_tool_name("create_task")
    validate_tool_name(tool_name, expected_namespace="myproject")

    # Implementation...
    task_id = generate_uuid()
    return {
        "id": task_id,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat()
    }

# Resource implementation
@mcp.resource(uri=make_resource_uri("templates", "daily-report.md"))
async def get_daily_report_template() -> str:
    """Daily report template resource.

    Resource URI: myproject://templates/daily-report.md
    """
    return Path("templates/daily-report.md").read_text()

# Main entry point
if __name__ == "__main__":
    mcp.run()
```

### NAMESPACES.md (Project Documentation)

```markdown
# MCP Namespace Registry

**Project:** myproject
**Namespace:** `myproject`
**Convention:** Chora MCP Conventions v1.0
**Status:** Active

---

## Registered Tools

| Tool Name | Full Name | Description | Version |
|-----------|-----------|-------------|---------|
| create_task | myproject:create_task | Create new task | 1.0.0 |
| list_tasks | myproject:list_tasks | List all tasks | 1.0.0 |
| update_task | myproject:update_task | Update existing task | 1.0.0 |

---

## Registered Resources

| Resource URI | Description | Type |
|--------------|-------------|------|
| myproject://templates/daily-report.md | Daily report template | text/markdown |
| myproject://configs/settings.json | Server configuration | application/json |
| myproject://capabilities/server | Server capabilities | application/json |

---

## Namespace Rules

- **Format:** `myproject:{tool_name}` for tools
- **Format:** `myproject://{type}/{id}` for resources
- **Validation:** Runtime validation enabled (see `src/myproject/mcp/__init__.py`)
- **Registry:** Registered in Chora Ecosystem (2025-10-21)

---

## References

- [Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md)
- [mcp-n8n Gateway](https://github.com/liminalcommons/mcp-n8n)
```

---

## FAQ

### When should I use namespacing?

**Always** when your server will integrate with:
- mcp-n8n gateway
- Multi-server MCP clients
- Chora ecosystem workflows

**Optional** for standalone servers with single-client usage.

### Can I use hyphens in tool names?

**No.** Use snake_case for tool names. Hyphens are reserved for kebab-case resource IDs.

### What if my project name is too long (>20 chars)?

Use an abbreviated namespace (e.g., `myawesomelongproject` → `malp`), but:
- Prefer full name if possible
- Document abbreviation in `NAMESPACES.md`
- Ensure abbreviation is still meaningful

### Can I change my namespace later?

**Strongly discouraged.** Treat namespace as immutable after first release. Changing requires:
1. Version bump (breaking change)
2. Migration script for clients
3. Gateway configuration updates
4. Documentation updates

### How do I handle tool name collisions within my namespace?

Use descriptive prefixes within tool names:
```python
# ❌ Collision-prone
myproject:get      # Ambiguous
myproject:create   # What are we creating?

# ✅ Clear
myproject:get_task
myproject:create_task
myproject:get_user
myproject:create_user
```

---

## Changelog

### v1.0.0 (2025-10-21)
- Initial stable release
- Established tool naming pattern (`namespace:tool_name`)
- Defined resource URI scheme (`namespace://type/id`)
- Created namespace registry
- Documented validation patterns
- Integrated with mcp-n8n gateway architecture

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification)
- [mcp-n8n Gateway Architecture](https://github.com/liminalcommons/mcp-n8n)
- [chora-compose MCP Tools](https://github.com/liminalcommons/chora-compose)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

**Maintained by:** chora-base project
**Contact:** https://github.com/liminalcommons/chora-base/issues
**License:** MIT
