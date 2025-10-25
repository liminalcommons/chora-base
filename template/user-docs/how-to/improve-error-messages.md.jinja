---
title: "How-To: Improve Error Messages"
type: how-to
audience: developers
status: active
last_updated: {{ _copier_conf.now }}
version: 1.0.0
related: [../reference/python-patterns.md, ./standardize-responses.md]
tags: [errors, user-experience, fuzzy-matching, validation]
---

# How-To: Improve Error Messages

**Purpose:** Generate user-friendly error messages with actionable suggestions using fuzzy matching and context.

**Use Cases:**
- CLI tools - Suggest correct commands/flags
- APIs - Suggest valid endpoints/parameters
- Config validation - Suggest corrections
- Database queries - Suggest similar records
- MCP servers - Suggest valid tool/resource names

---

## Quick Reference

| Method | When to Use | Example |
|--------|-------------|---------|
| `not_found()` | Entity doesn't exist | "Server 'tset' not found. Did you mean 'test'?" |
| `already_exists()` | Duplicate entity | "Server 'prod' already exists." |
| `invalid_parameter()` | Wrong parameter type/value | "Invalid parameter 'port': got str, expected integer" |
| `missing_required_field()` | Required field missing | "Missing required field 'name' in request" |
| `invalid_combination()` | Conflicting parameters | "Invalid combination of 'all' and 'ids': ..." |

---

## Basic Usage

### Example 1: Not Found with Suggestion

```python
from {{ package_name }}.utils.errors import ErrorFormatter

def get_server(server_id: str) -> dict:
    """Get server by ID."""
    available_servers = ["production", "staging", "development"]

    if server_id not in available_servers:
        error_message = ErrorFormatter.not_found(
            entity_type="server",
            entity_id=server_id,
            available=available_servers,
        )
        raise ValueError(error_message)

    # Get server...

# Usage:
>>> get_server("prod")
ValueError: Server 'prod' not found. Did you mean 'production'?
```

**What it does:**
- Uses fuzzy matching (difflib) to find similar names
- Suggests closest match if found
- Lists available options if no close match
- Capitalizes entity type automatically

---

### Example 2: Already Exists Error

```python
from {{ package_name }}.utils.errors import ErrorFormatter

def create_server(server_id: str) -> dict:
    """Create a new server."""
    if server_id in existing_servers:
        error_message = ErrorFormatter.already_exists(
            entity_type="server",
            entity_id=server_id,
        )
        raise ValueError(error_message)

    # Create server...

# Usage:
>>> create_server("production")
ValueError: Server 'production' already exists.
```

---

### Example 3: Invalid Parameter Error

```python
from {{ package_name }}.utils.errors import ErrorFormatter

def set_port(port: int) -> dict:
    """Set server port."""
    if not isinstance(port, int):
        error_message = ErrorFormatter.invalid_parameter(
            param_name="port",
            value=port,
            expected="integer",
        )
        raise TypeError(error_message)

    # Set port...

# Usage:
>>> set_port("8080")
TypeError: Invalid parameter 'port': got str, expected integer
```

---

## Use Case: CLI Tool with Fuzzy Command Matching

### Problem
Users make typos in command names. Error messages don't help them find the right command.

### Solution

```python
import click
from {{ package_name }}.utils.errors import ErrorFormatter
from {{ package_name }}.utils.responses import Response

# Define available commands
COMMANDS = ["build", "test", "deploy", "clean", "lint"]

@click.command()
@click.argument('command')
def cli(command: str):
    """Execute a command."""
    if command not in COMMANDS:
        error_message = ErrorFormatter.not_found(
            entity_type="command",
            entity_id=command,
            available=COMMANDS,
        )

        result = Response.error(
            error_code="command_not_found",
            message=error_message,
            available_commands=COMMANDS,
        )

        import json
        click.echo(json.dumps(result, indent=2), err=True)
        raise click.Abort()

    # Execute command...
    click.echo(f"Executing: {command}")
```

**Usage:**
```bash
$ myapp biuld
{
  "status": "error",
  "error_code": "command_not_found",
  "message": "Command 'biuld' not found. Did you mean 'build'?",
  "recoverable": true,
  "details": {
    "available_commands": ["build", "test", "deploy", "clean", "lint"]
  },
  ...
}

$ myapp build
Executing: build
```

**Impact:**
- Immediate correction for typos
- No need to run `--help` to see available commands
- Reduced support burden

---

## Use Case: REST API with Parameter Validation

### Problem
API validation errors are cryptic and don't guide users to fix issues.

### Solution

```python
from {{ package_name }}.utils.errors import ErrorFormatter
from {{ package_name }}.utils.responses import Response

@app.post("/api/servers")
async def create_server(body: dict):
    """Create server with validation."""
    # Check required fields
    required_fields = ["name", "type", "config"]
    missing = [f for f in required_fields if f not in body]

    if missing:
        # Use missing_required_field for clarity
        if len(missing) == 1:
            error_message = ErrorFormatter.missing_required_field(
                field_name=missing[0],
                container="request body",
            )
        else:
            error_message = f"Missing required fields in request body: {', '.join(missing)}"

        return Response.error(
            error_code="invalid_request",
            message=error_message,
            missing_fields=missing,
            required_fields=required_fields,
        )

    # Validate server type
    valid_types = ["production", "staging", "development"]
    if body["type"] not in valid_types:
        error_message = ErrorFormatter.not_found(
            entity_type="server type",
            entity_id=body["type"],
            available=valid_types,
        )

        return Response.error(
            error_code="invalid_parameter",
            message=error_message,
            field="type",
            valid_types=valid_types,
        )

    # Create server...
    return Response.success(action="created", data={"id": 123})
```

**Before:**
```json
{
  "error": "Invalid request"
}
```

**After:**
```json
{
  "status": "error",
  "error_code": "invalid_parameter",
  "message": "Server type 'prod' not found. Did you mean 'production'?",
  "details": {
    "field": "type",
    "valid_types": ["production", "staging", "development"]
  }
}
```

---

## Use Case: MCP Server Tool Validation

### Problem
MCP tools need to validate server IDs, tool names, and parameters. Errors should guide Claude to correct usage.

### Solution

```python
from {{ package_name }}.utils.errors import ErrorFormatter
from {{ package_name }}.utils.responses import Response
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@mcp.tool()
@normalize_input(params=InputFormat.DICT_OR_JSON)
async def remove_server(server_id: str, params: dict | None = None) -> dict:
    """Remove a server from configuration.

    Args:
        server_id: Server to remove
        params: Optional parameters (force: bool)
    """
    params = params or {}
    available_servers = get_server_ids()

    # Validate server exists
    if server_id not in available_servers:
        error_message = ErrorFormatter.not_found(
            entity_type="server",
            entity_id=server_id,
            available=available_servers,
            max_suggestions=3,
        )

        return Response.error(
            error_code="not_found",
            message=error_message,
            available_servers=available_servers,
        )

    # Check if server is running
    if is_server_running(server_id) and not params.get("force"):
        return Response.error(
            error_code="server_running",
            message=f"Server '{server_id}' is currently running",
            hint="Use force=true to remove anyway",
            force_required=True,
        )

    # Remove server
    remove_server_from_config(server_id)

    return Response.success(
        action="removed",
        data={"server_id": server_id},
    )
```

**Usage:**
```python
# Typo in server name
>>> remove_server("githbu")
{
  "status": "error",
  "error_code": "not_found",
  "message": "Server 'githbu' not found. Did you mean 'github'?",
  "details": {
    "available_servers": ["github", "gitlab", "filesystem"]
  }
}

# Server running
>>> remove_server("github")
{
  "status": "error",
  "error_code": "server_running",
  "message": "Server 'github' is currently running",
  "details": {
    "hint": "Use force=true to remove anyway",
    "force_required": true
  }
}
```

---

## Advanced: Combining Error Formatters

### Pattern 1: Validation with Multiple Checks

```python
def validate_server_config(config: dict) -> dict | None:
    """Validate server configuration.

    Returns:
        Error response dict if invalid, None if valid.
    """
    # Check required fields
    required = ["name", "command", "args"]
    missing = [f for f in required if f not in config]

    if len(missing) == 1:
        error_message = ErrorFormatter.missing_required_field(
            field_name=missing[0],
            container="server configuration",
        )
        return Response.error(
            error_code="invalid_config",
            message=error_message,
            missing_fields=missing,
        )
    elif len(missing) > 1:
        return Response.error(
            error_code="invalid_config",
            message=f"Missing required fields: {', '.join(missing)}",
            missing_fields=missing,
        )

    # Validate command type
    if not isinstance(config["command"], str):
        error_message = ErrorFormatter.invalid_parameter(
            param_name="command",
            value=config["command"],
            expected="string",
        )
        return Response.error(
            error_code="invalid_parameter",
            message=error_message,
            field="command",
        )

    # Validate args type
    if not isinstance(config["args"], list):
        error_message = ErrorFormatter.invalid_parameter(
            param_name="args",
            value=config["args"],
            expected="list of strings",
            hint="wrap in square brackets: [\"arg1\", \"arg2\"]",
        )
        return Response.error(
            error_code="invalid_parameter",
            message=error_message,
            field="args",
        )

    return None  # Valid
```

### Pattern 2: Conflicting Parameters

```python
def delete_servers(all: bool = False, ids: list[str] | None = None) -> dict:
    """Delete servers by ID or all."""
    # Validate parameter combination
    if all and ids:
        error_message = ErrorFormatter.invalid_combination(
            field1="all",
            field2="ids",
            reason="specify either 'all=true' or specific IDs, not both",
        )
        return Response.error(
            error_code="invalid_parameters",
            message=error_message,
        )

    if not all and not ids:
        return Response.error(
            error_code="invalid_parameters",
            message="Must specify either 'all=true' or provide 'ids'",
            required_parameters=["all OR ids"],
        )

    # Delete servers...
    if all:
        deleted = delete_all_servers()
    else:
        deleted = delete_servers_by_ids(ids)

    return Response.success(action="deleted", data=deleted)
```

---

## Fuzzy Matching Details

### How Fuzzy Matching Works

The `not_found()` method uses Python's `difflib.get_close_matches()`:
- **Cutoff:** 0.6 (60% similarity required)
- **Algorithm:** Gestalt pattern matching
- **Case-sensitive:** Yes (normalize inputs if needed)

**Examples of matches:**
```python
# Single character typo
"githbu" → "github" ✅ (high similarity)
"tset" → "test" ✅ (high similarity)

# Multiple character errors
"prod" → "production" ✅ (partial match)
"dev" → "development" ✅ (partial match)

# Too different
"xyz" → "github" ❌ (low similarity, won't suggest)
```

### Customizing Fuzzy Matching

```python
# Increase suggestions
ErrorFormatter.not_found(
    entity_type="server",
    entity_id="prod",
    available=["production", "prod-eu", "prod-us", "prod-asia"],
    max_suggestions=4,  # Show up to 4 suggestions
)
# Result: "Did you mean one of: 'production', 'prod-eu', 'prod-us', 'prod-asia'?"

# Case-insensitive matching
def case_insensitive_not_found(entity_type, entity_id, available):
    """Fuzzy match ignoring case."""
    # Normalize to lowercase
    entity_id_lower = entity_id.lower()
    available_lower = [a.lower() for a in available]

    # Create mapping back to original case
    original_map = {a.lower(): a for a in available}

    error_message = ErrorFormatter.not_found(
        entity_type=entity_type,
        entity_id=entity_id_lower,
        available=available_lower,
    )

    # Replace suggestions with original case
    for lower, original in original_map.items():
        error_message = error_message.replace(f"'{lower}'", f"'{original}'")

    return error_message
```

---

## Best Practices

### ✅ DO: Provide Context in Error Messages

```python
# Good: Specific, actionable
ErrorFormatter.not_found(
    entity_type="server",
    entity_id="githbu",
    available=["github", "gitlab"],  # Shows what IS available
)

# Bad: Generic, unhelpful
raise ValueError("Server not found")
```

### ✅ DO: Use Hints for Complex Validation

```python
# Good: Explains how to fix
ErrorFormatter.invalid_parameter(
    param_name="port",
    value="8080",
    expected="integer",
    hint="remove quotes: port=8080 instead of port=\"8080\"",
)

# Bad: No guidance
ErrorFormatter.invalid_parameter(
    param_name="port",
    value="8080",
    expected="integer",
)
```

### ✅ DO: Limit Available List Length

```python
# Good: Don't overwhelm user
available_servers = get_all_servers()  # Could be 100+ servers

ErrorFormatter.not_found(
    entity_type="server",
    entity_id="xyz",
    available=available_servers,  # Automatically truncates to 5
)
# Result: "Available servers: a, b, c, d, e (and 95 more)"

# Alternative: Filter to relevant subset
relevant_servers = [s for s in available_servers if s.startswith("prod")]
ErrorFormatter.not_found(
    entity_type="server",
    entity_id="prod-xyz",
    available=relevant_servers,  # More focused suggestions
)
```

### ❌ DON'T: Use for Non-Entity Errors

```python
# Bad: ErrorFormatter is for entity/parameter errors
ErrorFormatter.not_found(
    entity_type="connection",
    entity_id="database",
    available=[],
)
# Better: Use Response.error directly
Response.error(
    error_code="connection_failed",
    message="Failed to connect to database",
    reason="Connection timeout after 30s",
)
```

---

## Integration with Response Builder

### Recommended Pattern

```python
from {{ package_name }}.utils.errors import ErrorFormatter
from {{ package_name }}.utils.responses import Response

def get_resource(resource_id: str) -> dict:
    """Get resource with helpful errors."""
    if resource_id not in resources:
        # Generate helpful message
        error_message = ErrorFormatter.not_found(
            entity_type="resource",
            entity_id=resource_id,
            available=list(resources.keys()),
        )

        # Wrap in standardized response
        return Response.error(
            error_code="not_found",
            message=error_message,
            available=list(resources.keys()),
        )

    # Success case
    return Response.success(
        action="retrieved",
        data=resources[resource_id],
    )
```

**Result:**
```json
{
  "status": "error",
  "error_code": "not_found",
  "message": "Resource 'tset' not found. Did you mean 'test'?",
  "recoverable": true,
  "details": {
    "available": ["test", "prod", "dev"]
  },
  "timestamp": 1698765432.123
}
```

---

## Common Patterns

### Pattern 1: Configuration Validation

```python
def validate_config(config: dict) -> list[str]:
    """Validate configuration, return list of errors."""
    errors = []

    # Check required fields
    for field in ["name", "version", "author"]:
        if field not in config:
            errors.append(
                ErrorFormatter.missing_required_field(
                    field_name=field,
                    container="configuration",
                )
            )

    # Check field types
    if "port" in config and not isinstance(config["port"], int):
        errors.append(
            ErrorFormatter.invalid_parameter(
                param_name="port",
                value=config["port"],
                expected="integer",
            )
        )

    return errors
```

### Pattern 2: Batch Validation with Suggestions

```python
def validate_server_ids(server_ids: list[str]) -> dict:
    """Validate multiple server IDs."""
    available = get_server_ids()
    invalid = []

    for sid in server_ids:
        if sid not in available:
            error_message = ErrorFormatter.not_found(
                entity_type="server",
                entity_id=sid,
                available=available,
            )
            invalid.append({"id": sid, "error": error_message})

    if invalid:
        return Response.error(
            error_code="invalid_server_ids",
            message=f"{len(invalid)} invalid server IDs",
            invalid=invalid,
        )

    return Response.success(action="validated", data=server_ids)
```

---

## Troubleshooting

### Issue: Fuzzy matching suggests wrong results

**Solution:** Adjust available list or use manual matching

```python
# Filter available list to relevant subset
relevant = [s for s in all_servers if s.startswith(prefix)]
ErrorFormatter.not_found(..., available=relevant)

# Or skip fuzzy matching for very different inputs
if entity_id.startswith("prod"):
    available = [s for s in all_servers if s.startswith("prod")]
else:
    available = all_servers
```

### Issue: Too many suggestions

**Solution:** Reduce max_suggestions

```python
ErrorFormatter.not_found(
    ...,
    max_suggestions=1,  # Only show closest match
)
```

### Issue: Need case-insensitive matching

**Solution:** Normalize inputs before calling ErrorFormatter

```python
entity_id_lower = entity_id.lower()
available_lower = [a.lower() for a in available]

# Create original case mapping
original_case = {a.lower(): a for a in available}

message = ErrorFormatter.not_found(
    entity_type="server",
    entity_id=entity_id_lower,
    available=available_lower,
)

# Restore original case in suggestions
for lower, original in original_case.items():
    message = message.replace(f"'{lower}'", f"'{original}'")
```

---

## Related Documentation

- [Python Patterns Reference](../reference/python-patterns.md) - Full pattern catalog
- [How-To: Standardize Responses](./standardize-responses.md) - Response formatting
- [How-To: Use Input Validation](./use-input-validation.md) - Parameter validation
- [API Reference](../../src/{{ package_name }}/utils/errors.py) - Source code
- [Tests](../../tests/utils/test_errors.py) - More examples

---

**Last Updated:** {{ _copier_conf.now }}
**Version:** 1.0.0
**Maintained by:** {{ author_name }}
