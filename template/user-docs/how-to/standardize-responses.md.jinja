---
title: "How-To: Standardize Response Format"
type: how-to
audience: developers
status: active
last_updated: {{ _copier_conf.now }}
version: 1.0.0
related: [../reference/python-patterns.md]
tags: [responses, api, consistency, error-handling]
---

# How-To: Standardize Response Format

**Purpose:** Build consistent response dictionaries for success, error, and partial success cases across all endpoints/tools.

**Use Cases:**
- REST APIs - Consistent endpoint responses
- CLI tools - Structured command outputs
- MCP servers - Tool response formatting
- RPC methods - Standardized return values
- Microservices - Service-to-service communication

---

## Quick Reference

| Method | When to Use | Example |
|--------|-------------|---------|
| `Response.success()` | Operation succeeded | Created resource, retrieved data |
| `Response.error()` | Operation failed | Not found, invalid input |
| `Response.partial()` | Batch with mixed results | 5/10 items deleted successfully |

---

## Basic Usage

### Example 1: Success Response

```python
from {{ package_name }}.utils.responses import Response

def create_resource(name: str) -> dict:
    """Create a new resource."""
    # Perform creation...
    resource = {"id": 123, "name": name, "status": "active"}

    return Response.success(
        action="created",
        data=resource,
    )

# Result:
{
    "status": "success",
    "action": "created",
    "data": {"id": 123, "name": "test", "status": "active"},
    "metadata": {},
    "timestamp": 1698765432.123,
}
```

**What it does:**
- Sets `status` to `"success"`
- Records the action performed
- Includes the result data
- Adds current timestamp
- Logs at INFO level automatically

---

### Example 2: Error Response

```python
from {{ package_name }}.utils.responses import Response

def get_resource(resource_id: str) -> dict:
    """Get a resource by ID."""
    if resource_id not in available_resources:
        return Response.error(
            error_code="not_found",
            message=f"Resource '{resource_id}' not found",
            available=list(available_resources.keys()),
        )

    # Return resource...

# Result:
{
    "status": "error",
    "error_code": "not_found",
    "message": "Resource 'xyz' not found",
    "recoverable": True,
    "details": {"available": ["abc", "def"]},
    "timestamp": 1698765432.123,
}
```

**What it does:**
- Sets `status` to `"error"`
- Provides machine-readable error code
- Includes human-readable message
- Marks as recoverable (default: True)
- Adds context in details dict
- Logs at ERROR level automatically

---

### Example 3: Partial Success Response

```python
from {{ package_name }}.utils.responses import Response

def delete_resources(resource_ids: list[str]) -> dict:
    """Delete multiple resources."""
    succeeded = []
    failed = []

    for rid in resource_ids:
        try:
            delete_resource(rid)
            succeeded.append(rid)
        except Exception as e:
            failed.append({"id": rid, "reason": str(e)})

    return Response.partial(
        action="deleted",
        succeeded=succeeded,
        failed=failed,
    )

# Result:
{
    "status": "partial",
    "action": "deleted",
    "succeeded": ["item1", "item2"],
    "failed": [{"id": "item3", "reason": "not found"}],
    "metadata": {
        "succeeded_count": 2,
        "failed_count": 1,
    },
    "timestamp": 1698765432.123,
}
```

**What it does:**
- Sets `status` to `"partial"`
- Lists successful items
- Lists failed items with reasons
- Auto-calculates counts
- Logs at WARNING level (partial success is concerning)

---

## Use Case: REST API Endpoint

### Problem
REST endpoints manually construct response dicts with inconsistent fields.

### Solution

```python
from {{ package_name }}.utils.responses import Response

@app.post("/api/servers")
async def create_server(body: dict):
    """Create a new server."""
    # Validate input
    if "name" not in body:
        return Response.error(
            error_code="invalid_parameter",
            message="Missing required field: name",
            field="name",
        )

    # Check for duplicate
    if server_exists(body["name"]):
        return Response.error(
            error_code="already_exists",
            message=f"Server '{body['name']}' already exists",
            existing_id=get_server_id(body["name"]),
        )

    # Create server
    server = create_new_server(body)

    return Response.success(
        action="created",
        data=server,
        resource_type="server",
    )
```

**Before standardization:**
```python
# Manual dict construction (inconsistent)
return {
    "success": True,          # Different field name
    "result": server,         # Different field name
    "message": "Created",     # Redundant
}

# Or on error:
return {
    "error": "Server already exists",  # No error code
    # No structured details
}
```

**After standardization:**
- Consistent field names across all endpoints
- Machine-readable error codes
- Structured error details
- Automatic logging

---

## Use Case: CLI Tool Output

### Problem
CLI commands return inconsistent output formats, making them hard to parse or chain.

### Solution

```python
import click
from {{ package_name }}.utils.responses import Response

@click.command()
@click.argument('server_id')
def get_server(server_id: str):
    """Get server information."""
    try:
        server = fetch_server(server_id)
        result = Response.success(
            action="retrieved",
            data=server,
        )
    except ServerNotFound:
        result = Response.error(
            error_code="not_found",
            message=f"Server '{server_id}' not found",
            available=list_server_ids(),
        )

    # Output as JSON for parsing
    import json
    click.echo(json.dumps(result, indent=2))
```

**Usage:**
```bash
$ myapp get-server prod
{
  "status": "success",
  "action": "retrieved",
  "data": {
    "id": "prod",
    "host": "prod.example.com",
    "port": 443
  },
  ...
}

# Can be parsed by other tools
$ myapp get-server prod | jq '.data.host'
"prod.example.com"
```

---

## Use Case: MCP Server Tool

### Problem
MCP tools manually construct response dicts for every tool.

### Solution

```python
from {{ package_name }}.utils.responses import Response
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@mcp.tool()
@normalize_input(params=InputFormat.DICT_OR_JSON)
async def add_server(
    server_id: str,
    params: dict | None = None,
) -> dict:
    """Add a server to configuration.

    Args:
        server_id: Unique server identifier
        params: Server parameters (command, args, env)

    Returns:
        Standardized response dict
    """
    params = params or {}

    # Validate
    if not server_id:
        return Response.error(
            error_code="invalid_parameter",
            message="server_id cannot be empty",
            field="server_id",
        )

    # Check duplicate
    if server_id in get_server_ids():
        return Response.error(
            error_code="already_exists",
            message=f"Server '{server_id}' already exists",
            existing_id=server_id,
        )

    # Add server
    config = add_server_to_config(server_id, params)

    return Response.success(
        action="added",
        data={
            "server_id": server_id,
            "params": params,
        },
        config_updated=True,
    )
```

**Before:**
```python
# Manual dict construction (~10-15 lines per tool)
return {
    "content": [
        {
            "type": "text",
            "text": f"Added server: {server_id}",
        }
    ],
    "isError": False,
}

# Or on error:
return {
    "content": [
        {
            "type": "text",
            "text": f"Error: Server already exists",
        }
    ],
    "isError": True,
}
```

**After:**
- 2-3 lines per response (~85% reduction)
- Consistent format across all tools
- Machine-readable error codes
- Structured data for future tool chaining

---

## Advanced: Adding Metadata

### Use Case: Pagination

```python
def list_resources(page: int = 1, per_page: int = 10) -> dict:
    """List resources with pagination."""
    offset = (page - 1) * per_page
    items = fetch_resources(offset=offset, limit=per_page)
    total = count_resources()

    return Response.success(
        action="listed",
        data=items,
        count=len(items),
        total=total,
        page=page,
        per_page=per_page,
        has_more=(offset + len(items)) < total,
    )

# Result:
{
    "status": "success",
    "action": "listed",
    "data": [...],
    "metadata": {
        "count": 10,
        "total": 157,
        "page": 1,
        "per_page": 10,
        "has_more": true,
    },
    ...
}
```

### Use Case: Performance Tracking

```python
import time

def expensive_operation() -> dict:
    """Perform an expensive operation."""
    start = time.time()

    # Do work...
    result = perform_work()

    duration_ms = int((time.time() - start) * 1000)

    return Response.success(
        action="processed",
        data=result,
        duration_ms=duration_ms,
        cache_hit=False,
    )
```

---

## Error Handling Patterns

### Pattern 1: Not Found with Suggestions

```python
def get_server(server_id: str) -> dict:
    """Get server by ID."""
    if server_id not in servers:
        # Use ErrorFormatter for suggestions (see error formatting guide)
        from {{ package_name }}.utils.errors import ErrorFormatter

        message = ErrorFormatter.not_found(
            entity_type="server",
            entity_id=server_id,
            available=list(servers.keys()),
        )

        return Response.error(
            error_code="not_found",
            message=message,
            available=list(servers.keys()),
        )

    return Response.success(action="retrieved", data=servers[server_id])
```

### Pattern 2: Validation Errors

```python
def create_resource(data: dict) -> dict:
    """Create resource with validation."""
    required_fields = ["name", "type", "config"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return Response.error(
            error_code="invalid_parameter",
            message=f"Missing required fields: {', '.join(missing)}",
            missing_fields=missing,
            required_fields=required_fields,
        )

    # Create resource...
```

### Pattern 3: Fatal vs Recoverable Errors

```python
def authenticate(credentials: dict) -> dict:
    """Authenticate user."""
    if not valid_credentials(credentials):
        return Response.error(
            error_code="auth_failed",
            message="Invalid credentials",
            recoverable=False,  # Fatal error
        )

    # Generate token...
```

```python
def temporary_operation() -> dict:
    """Operation that might fail temporarily."""
    if rate_limit_exceeded():
        return Response.error(
            error_code="rate_limit",
            message="Rate limit exceeded, retry after 60s",
            recoverable=True,  # Can retry
            retry_after=60,
        )
```

---

## Best Practices

### ✅ DO: Use Past Tense for Actions

```python
# Good: Past tense (action completed)
Response.success(action="created", ...)
Response.success(action="updated", ...)
Response.success(action="deleted", ...)

# Bad: Present tense
Response.success(action="create", ...)
Response.success(action="update", ...)
```

### ✅ DO: Use Snake_Case for Error Codes

```python
# Good: Snake case, machine-readable
Response.error(error_code="not_found", ...)
Response.error(error_code="invalid_parameter", ...)
Response.error(error_code="already_exists", ...)

# Bad: Mixed case, spaces
Response.error(error_code="NotFound", ...)
Response.error(error_code="invalid parameter", ...)
```

### ✅ DO: Include Context in Details

```python
# Good: Actionable context
Response.error(
    error_code="not_found",
    message="Server 'xyz' not found",
    available=["abc", "def"],  # Show what IS available
    field="server_id",         # Which field was wrong
)

# Bad: No context
Response.error(
    error_code="not_found",
    message="Server not found",
)
```

### ❌ DON'T: Mix Response Formats

```python
# Bad: Inconsistent format
def endpoint_a():
    return {"success": True, "data": ...}  # Different format

def endpoint_b():
    return Response.success(action="...", data=...)  # Standardized

# Good: Always use Response
def endpoint_a():
    return Response.success(action="...", data=...)

def endpoint_b():
    return Response.success(action="...", data=...)
```

---

## Common Patterns

### Pattern 1: Try/Except with Responses

```python
def risky_operation() -> dict:
    """Operation that might fail."""
    try:
        result = perform_operation()
        return Response.success(action="completed", data=result)
    except ValueError as e:
        return Response.error(
            error_code="invalid_input",
            message=str(e),
        )
    except Exception as e:
        return Response.error(
            error_code="internal_error",
            message=f"Unexpected error: {e}",
            recoverable=False,
        )
```

### Pattern 2: Conditional Success/Error

```python
def conditional_operation(force: bool = False) -> dict:
    """Operation that checks before proceeding."""
    if not force and resource_exists():
        return Response.error(
            error_code="already_exists",
            message="Resource exists. Use force=true to override",
            force_required=True,
        )

    # Proceed with operation...
    return Response.success(action="created", ...)
```

### Pattern 3: Batch Operations

```python
def batch_create(items: list[dict]) -> dict:
    """Create multiple items."""
    if not items:
        return Response.success(action="created", data=[], count=0)

    succeeded = []
    failed = []

    for item in items:
        try:
            result = create_item(item)
            succeeded.append(result)
        except Exception as e:
            failed.append({
                "item": item,
                "reason": str(e),
            })

    # All succeeded
    if not failed:
        return Response.success(
            action="created",
            data=succeeded,
            count=len(succeeded),
        )

    # All failed
    if not succeeded:
        return Response.error(
            error_code="batch_failed",
            message="All items failed",
            failures=failed,
        )

    # Mixed results
    return Response.partial(
        action="created",
        succeeded=succeeded,
        failed=failed,
        total_attempted=len(items),
    )
```

---

## Troubleshooting

### Issue: Need to return MCP-specific format

**Solution:** Wrap Response in MCP format

```python
@mcp.tool()
async def my_tool() -> list[dict]:
    """MCP tool that returns TextContent."""
    # Build standardized response
    response = Response.success(action="completed", data={"result": 123})

    # Wrap in MCP format
    import json
    return [
        {
            "type": "text",
            "text": json.dumps(response, indent=2),
        }
    ]
```

### Issue: Need to add logging context

**Solution:** Response logs automatically, but you can add more

```python
import logging
logger = logging.getLogger(__name__)

def my_operation() -> dict:
    logger.info("Starting operation", extra={"user": "alice"})

    # Response will also log automatically
    return Response.success(action="completed", ...)
```

---

## Related Documentation

- [Python Patterns Reference](../reference/python-patterns.md) - Full pattern catalog
- [How-To: Use Input Validation](./use-input-validation.md) - Parameter normalization
- [How-To: Improve Error Messages](./improve-error-messages.md) - Error formatting
- [API Reference](../../src/{{ package_name }}/utils/responses.py) - Source code
- [Tests](../../tests/utils/test_responses.py) - More examples

---

**Last Updated:** {{ _copier_conf.now }}
**Version:** 1.0.0
**Maintained by:** {{ author_name }}
