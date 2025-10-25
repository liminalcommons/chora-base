---
title: "Reference: Python Patterns"
type: reference
audience: developers
status: active
last_updated: {{ _copier_conf.now }}
version: 1.0.0
tags: [patterns, reference, best-practices, utilities]
---

# Reference: Python Patterns

**Purpose:** Comprehensive reference for reusable Python patterns and utilities available in {{ project_name }}.

**Audience:** Developers building with {{ project_name }}, looking for proven patterns to solve common problems.

---

## Overview

This project includes optional utilities that implement proven patterns from production Python projects. These patterns are **project-type agnostic** — they work equally well for MCP servers, REST APIs, CLI tools, libraries, and services.

### Available Utilities

{% if include_api_utilities -%}
| Utility | Purpose | Use Cases |
|---------|---------|-----------|
| **validation.py** | Input normalization | REST APIs, CLI args, config parsing, RPC |
| **responses.py** | Response standardization | API endpoints, CLI output, service responses |
| **errors.py** | Error formatting | User-facing errors, API errors, validation |
{% endif -%}
{% if include_persistence_helpers -%}
| **persistence.py** | State persistence | CLI sessions, daemon config, drafts, caches |
{% endif -%}

### When to Use

**Use these utilities when:**
- Building APIs (REST, RPC, GraphQL)
- Creating CLI tools with structured output
- Developing stateful services or daemons
- Implementing libraries with consistent error handling
- Need production-ready patterns quickly

**Skip these utilities when:**
- Building simple scripts (<100 lines)
- Prototyping (can add later)
- Have strict zero-dependency requirements
- Framework provides equivalent features (e.g., FastAPI validation)

---

{% if include_api_utilities -%}
## Pattern 1: Input Normalization

**Problem:** APIs accept inputs in multiple formats (JSON strings, dicts, key=value pairs) requiring repetitive parsing code.

**Solution:** Use `normalize_input()` decorator to automatically convert inputs to expected format.

### API Reference

```python
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@normalize_input(
    params: InputFormat = InputFormat.DICT_OR_JSON,
    env_vars: InputFormat = InputFormat.DICT_OR_KV,
    # ... any parameter name
)
def my_function(params: dict | None, env_vars: dict | None):
    # params and env_vars are guaranteed to be dict or None
    pass
```

### InputFormat Enum

| Format | Accepts | Converts To | Use Case |
|--------|---------|-------------|----------|
| `DICT_ONLY` | dict only | dict | Type safety, strict APIs |
| `DICT_OR_JSON` | dict or JSON string | dict | REST APIs, config files |
| `KV_PAIRS` | list of "k=v" strings | dict | CLI arguments, env vars |
| `DICT_OR_KV` | dict or list of "k=v" | dict | Flexible CLIs |

### When to Use

✅ **Use when:**
- Accepting user input in multiple formats
- Building CLIs with `key=value` arguments
- Parsing configuration (JSON/YAML/TOML)
- Implementing REST/RPC endpoints
- Need consistent parameter validation

❌ **Don't use when:**
- Parameters are always same type
- Framework handles validation (FastAPI, Click)
- Building internal functions (not user-facing)

### Examples

**REST API:**
```python
@app.post("/api/servers")
@normalize_input(config=InputFormat.DICT_OR_JSON)
async def create_server(name: str, config: dict | None = None):
    # config accepts: {"key": "value"} OR '{"key": "value"}'
    pass
```

**CLI Tool:**
```python
@cli.command()
@normalize_input(settings=InputFormat.KV_PAIRS)
def configure(settings: list[str]):
    # settings: ["theme=dark", "timeout=30"] → {"theme": "dark", "timeout": 30}
    pass
```

**MCP Server:**
```python
@mcp.tool()
@normalize_input(params=InputFormat.DICT_OR_JSON, env=InputFormat.DICT_OR_JSON)
async def add_server(server_id: str, params: dict | None, env: dict | None):
    # Handles both dict and JSON string from MCP client
    pass
```

### Code Reduction

**Before:** ~15-20 lines per function
**After:** ~1 line (decorator)
**Savings:** ~90% reduction

### Related Documentation

- [How-To: Use Input Validation](../how-to/use-input-validation.md)
- [Source Code](../../src/{{ package_name }}/utils/validation.py)
- [Tests](../../tests/utils/test_validation.py)

---

## Pattern 2: Response Standardization

**Problem:** Inconsistent response formats across endpoints/tools make APIs hard to consume and debug.

**Solution:** Use `Response` class methods to build standardized success/error/partial responses.

### API Reference

```python
from {{ package_name }}.utils.responses import Response

# Success response
Response.success(
    action: str,           # Past tense: "created", "updated", "deleted"
    data: Any = None,      # Result data (any JSON-serializable type)
    **metadata: Any        # Additional metadata (count, page, etc.)
) -> dict

# Error response
Response.error(
    error_code: str,       # Machine-readable: "not_found", "invalid_parameter"
    message: str,          # Human-readable error message
    recoverable: bool = True,  # Whether error is recoverable
    **details: Any         # Error context (available, field, etc.)
) -> dict

# Partial success response (batch operations)
Response.partial(
    action: str,           # Action attempted
    succeeded: list[Any],  # Successfully processed items
    failed: list[dict],    # Failed items with reasons
    **metadata: Any        # Additional metadata
) -> dict
```

### Response Structure

All responses include:
- `status`: "success", "error", or "partial"
- `timestamp`: Unix timestamp (float)
- Automatic logging at appropriate level (INFO/ERROR/WARNING)

**Success:**
```json
{
  "status": "success",
  "action": "created",
  "data": {"id": 123, "name": "test"},
  "metadata": {"count": 1},
  "timestamp": 1698765432.123
}
```

**Error:**
```json
{
  "status": "error",
  "error_code": "not_found",
  "message": "Server 'xyz' not found",
  "recoverable": true,
  "details": {"available": ["abc", "def"]},
  "timestamp": 1698765432.123
}
```

**Partial:**
```json
{
  "status": "partial",
  "action": "deleted",
  "succeeded": ["item1", "item2"],
  "failed": [{"id": "item3", "reason": "not found"}],
  "metadata": {
    "succeeded_count": 2,
    "failed_count": 1
  },
  "timestamp": 1698765432.123
}
```

### When to Use

✅ **Use when:**
- Building APIs (REST, RPC, GraphQL)
- Creating CLI tools with JSON output
- Implementing MCP server tools
- Need consistent response format
- Want automatic logging/telemetry

❌ **Don't use when:**
- Framework enforces different format (Django REST, FastAPI)
- Building internal functions (not API surface)
- Simple scripts with print() output

### Examples

**REST API:**
```python
@app.post("/api/servers")
def create_server(body: dict):
    if "name" not in body:
        return Response.error(
            error_code="invalid_request",
            message="Missing required field: name",
        )

    server = create_new_server(body)
    return Response.success(action="created", data=server)
```

**CLI Tool:**
```python
@click.command()
def list_servers():
    servers = get_all_servers()
    result = Response.success(
        action="listed",
        data=servers,
        count=len(servers),
    )
    click.echo(json.dumps(result, indent=2))
```

**Batch Operation:**
```python
def delete_servers(server_ids: list[str]):
    succeeded = []
    failed = []

    for sid in server_ids:
        try:
            delete_server(sid)
            succeeded.append(sid)
        except Exception as e:
            failed.append({"id": sid, "reason": str(e)})

    return Response.partial(
        action="deleted",
        succeeded=succeeded,
        failed=failed,
    )
```

### Code Reduction

**Before:** ~10-15 lines per response
**After:** ~2-3 lines
**Savings:** ~80-85% reduction

### Related Documentation

- [How-To: Standardize Responses](../how-to/standardize-responses.md)
- [Source Code](../../src/{{ package_name }}/utils/responses.py)
- [Tests](../../tests/utils/test_responses.py)

---

## Pattern 3: Error Formatting with Suggestions

**Problem:** Generic error messages don't help users fix issues. No guidance on what went wrong or how to correct it.

**Solution:** Use `ErrorFormatter` methods to generate helpful error messages with fuzzy matching suggestions.

### API Reference

```python
from {{ package_name }}.utils.errors import ErrorFormatter

# Entity not found with suggestions
ErrorFormatter.not_found(
    entity_type: str,      # "server", "command", "resource"
    entity_id: str,        # ID that wasn't found
    available: list[str],  # List of valid IDs
    max_suggestions: int = 3  # Max suggestions to show
) -> str

# Entity already exists
ErrorFormatter.already_exists(
    entity_type: str,      # "server", "user", "file"
    entity_id: str,        # ID that already exists
    existing_id: str | None = None  # Optional existing ID reference
) -> str

# Invalid parameter type/value
ErrorFormatter.invalid_parameter(
    param_name: str,       # Parameter name
    value: Any,            # Invalid value provided
    expected: str,         # Description of expected type/value
    hint: str | None = None  # Optional hint for fixing
) -> str

# Missing required field
ErrorFormatter.missing_required_field(
    field_name: str,       # Missing field name
    container: str = "request"  # Where field should be
) -> str

# Conflicting parameters
ErrorFormatter.invalid_combination(
    field1: str,           # First conflicting field
    field2: str,           # Second conflicting field
    reason: str            # Why invalid
) -> str
```

### Fuzzy Matching

`not_found()` uses `difflib.get_close_matches()` with 60% similarity cutoff:
- Suggests typo corrections: "githbu" → "github"
- Handles partial matches: "prod" → "production"
- Falls back to listing available options if no close match

### When to Use

✅ **Use when:**
- Building CLIs with commands/subcommands
- Validating API endpoints/parameters
- Parsing configuration files
- Need user-friendly error messages
- Want to reduce support burden

❌ **Don't use when:**
- Errors are for internal debugging only
- Security concerns (don't reveal available options)
- Building libraries (let application handle messages)

### Examples

**CLI Command Not Found:**
```python
commands = ["build", "test", "deploy", "clean"]
user_input = "biuld"

error_message = ErrorFormatter.not_found(
    entity_type="command",
    entity_id=user_input,
    available=commands,
)
# Result: "Command 'biuld' not found. Did you mean 'build'?"
```

**API Parameter Validation:**
```python
valid_types = ["production", "staging", "development"]
server_type = "prod"

if server_type not in valid_types:
    error_message = ErrorFormatter.not_found(
        entity_type="server type",
        entity_id=server_type,
        available=valid_types,
    )
    # Result: "Server type 'prod' not found. Did you mean 'production'?"
```

**Type Validation:**
```python
if not isinstance(port, int):
    error_message = ErrorFormatter.invalid_parameter(
        param_name="port",
        value=port,
        expected="integer",
        hint="remove quotes around the number",
    )
    # Result: "Invalid parameter 'port': got str, expected integer. Hint: remove quotes..."
```

### Integration with Response

```python
from {{ package_name }}.utils.responses import Response
from {{ package_name }}.utils.errors import ErrorFormatter

def get_server(server_id: str):
    if server_id not in servers:
        error_message = ErrorFormatter.not_found(
            entity_type="server",
            entity_id=server_id,
            available=list(servers.keys()),
        )
        return Response.error(
            error_code="not_found",
            message=error_message,
            available=list(servers.keys()),
        )
```

### Code Reduction

**Before:** Manual error messages, no suggestions
**After:** One-line formatter call
**Benefit:** Better UX, reduced support burden

### Related Documentation

- [How-To: Improve Error Messages](../how-to/improve-error-messages.md)
- [Source Code](../../src/{{ package_name }}/utils/errors.py)
- [Tests](../../tests/utils/test_errors.py)

---
{% endif -%}

{% if include_persistence_helpers -%}
## Pattern 4: State Persistence

**Problem:** Applications need to save/restore state between runs, requiring repetitive file I/O code.

**Solution:** Inherit from `StatefulObject` mixin for automatic JSON persistence with atomic writes.

### API Reference

```python
from {{ package_name }}.utils.persistence import StatefulObject

class MyApp(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")
        # Restore attributes or use defaults
        self.config = getattr(self, 'config', {})

    def update(self, data: dict):
        self.config = data
        self._save_state()  # Explicitly save

# Protected methods (customize behavior):
def _get_state(self) -> dict:
    """Override to customize what gets saved."""
    return {"config": self.config}  # Default: all non-private attrs

def _set_state(self, state: dict):
    """Override to customize restoration."""
    self.config = state.get("config", {})  # Default: setattr all

def _clear_state(self):
    """Delete state file from disk."""
```

### Atomic Writes

Persistence uses atomic write pattern to prevent corruption:
1. Write to temp file in same directory
2. Fsync to flush OS buffers
3. Atomic rename to target file

**Crash safety:** Process crash during save doesn't corrupt state.

### When to Use

✅ **Use when:**
- Building CLI tools (session state, preferences)
- Creating daemons (persist config between restarts)
- Implementing services (save drafts, pending operations)
- Need crash-safe state persistence
- Want automatic save/restore

❌ **Don't use when:**
- Building stateless services
- Using database for persistence
- State is too large for JSON (>10MB)
- Need multi-process coordination (add locking)

### Examples

**CLI Session State:**
```python
class Session(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.mycli/session.json")
        self.last_profile = getattr(self, 'last_profile', 'default')
        self.recent_commands = getattr(self, 'recent_commands', [])

    def set_profile(self, profile: str):
        self.last_profile = profile
        self._save_state()

# Usage:
session = Session()
session.set_profile("production")

# Later, new process:
session2 = Session()  # Restores last_profile="production"
```

**MCP Draft Manager:**
```python
class DraftManager(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.mcp/drafts.json")
        self.drafts = getattr(self, 'drafts', {})

    def save_draft(self, server_id: str, config: dict):
        self.drafts[server_id] = config
        self._save_state()
```

**Custom State Selection:**
```python
class MyApp(StatefulObject):
    def __init__(self):
        super().__init__(state_file="state.json")
        self.config = getattr(self, 'config', {})
        self.cache = {}  # Don't persist cache

    def _get_state(self) -> dict:
        # Only save config, not cache
        return {"config": self.config}
```

### Code Reduction

**Before:** ~25-30 lines (file I/O, JSON, error handling)
**After:** ~7-8 lines (inherit + init)
**Savings:** ~70-75% reduction

**Bonus:** Atomic writes add ~15 lines manually, error handling ~10 lines
**Total savings:** ~85-90% reduction with features

### Related Documentation

- [How-To: Persist Application State](../how-to/persist-application-state.md)
- [Source Code](../../src/{{ package_name }}/utils/persistence.py)
- [Tests](../../tests/utils/test_persistence.py)

---
{% endif -%}

## Pattern Combinations

### Full Stack Example

Combining all utilities for maximum benefit:

```python
from {{ package_name }}.utils.validation import normalize_input, InputFormat
from {{ package_name }}.utils.responses import Response
from {{ package_name }}.utils.errors import ErrorFormatter
{% if include_persistence_helpers -%}
from {{ package_name }}.utils.persistence import StatefulObject

class ServerManager(StatefulObject):
    """MCP server manager with full utility integration."""

    def __init__(self):
        super().__init__(state_file="~/.mcp/servers.json")
        self.servers = getattr(self, 'servers', {})
{% else -%}

class ServerManager:
    """Server manager with utility integration."""

    def __init__(self):
        self.servers = {}
{% endif -%}

    @normalize_input(params=InputFormat.DICT_OR_JSON)
    def add_server(self, server_id: str, params: dict | None = None):
        """Add server with full validation and error handling."""
        params = params or {}

        # Validate doesn't exist
        if server_id in self.servers:
            return Response.error(
                error_code="already_exists",
                message=ErrorFormatter.already_exists("server", server_id),
            )

        # Validate required fields
        required = ["command", "args"]
        missing = [f for f in required if f not in params]
        if missing:
            return Response.error(
                error_code="invalid_parameters",
                message=ErrorFormatter.missing_required_field(
                    missing[0], "params"
                ),
                missing_fields=missing,
            )

        # Add server
        self.servers[server_id] = params
{% if include_persistence_helpers -%}
        self._save_state()  # Persist
{% endif -%}

        return Response.success(
            action="added",
            data={"server_id": server_id, "params": params},
{% if include_persistence_helpers -%}
            persisted=True,
{% endif -%}
        )
```

**Impact:**
- ✅ Input normalization: Handles dict or JSON string
- ✅ Error formatting: Helpful messages with context
- ✅ Response standardization: Consistent format
{% if include_persistence_helpers -%}
- ✅ State persistence: Crash-safe storage
{% endif -%}
- **Code reduction:** ~60-70 lines → ~35 lines (40-50% savings)

---

## Best Practices

### General Guidelines

**✅ DO:**
- Use utilities for user-facing interfaces (APIs, CLIs)
- Combine utilities for maximum benefit
- Override hooks (`_get_state`, etc.) when needed
- Write tests using utilities (consistent test fixtures)
- Document expected input/output formats

**❌ DON'T:**
- Use utilities for internal functions (not user-facing)
- Mix response formats (use Response everywhere or nowhere)
- Store sensitive data in plain JSON{% if include_persistence_helpers %} (use encryption){% endif %}
- Skip error messages (always provide context)

### Performance Considerations

**Input Validation:**
- Minimal overhead (~microseconds per call)
- JSON parsing is main cost (cache if possible)

**Response Building:**
- Negligible overhead (dict construction)
- Logging can be disabled if needed

**Error Formatting:**
- Fuzzy matching is fast (<1ms for <1000 items)
- Pre-filter available list for huge datasets

{% if include_persistence_helpers -%}
**State Persistence:**
- Fsync adds ~5-10ms latency (ensures durability)
- Keep state files <1MB for best performance
- Don't persist on every tiny change (batch updates)
{% endif -%}

### Security Considerations

**Input Validation:**
- ✅ Prevents injection (structured data vs strings)
- ⚠️ Still validate values (type != security)

**Error Formatting:**
- ⚠️ Don't reveal sensitive data in suggestions
- ✅ Filter available list before passing to formatter

{% if include_persistence_helpers -%}
**State Persistence:**
- ❌ Don't store passwords/secrets in plain JSON
- ✅ Use system keyring or encrypt sensitive fields
- ✅ Set proper file permissions (0600)
{% endif -%}

---

## Migration Guide

### Adding Utilities to Existing Project

**Step 1:** Copy utility files
```bash
# If generated new project with utilities
cp new-project/src/myapp/utils/*.py existing-project/src/myapp/utils/
cp new-project/tests/utils/*.py existing-project/tests/utils/
```

**Step 2:** Install if needed (no external dependencies)
```bash
# Utilities use Python stdlib only
# No additional packages needed
```

**Step 3:** Gradually adopt patterns
```python
# Start with one pattern at a time
from myapp.utils.responses import Response

# Convert one endpoint
@app.get("/api/servers")
def list_servers():
    servers = get_all_servers()
    return Response.success(action="listed", data=servers)  # New
    # return {"servers": servers}  # Old
```

**Step 4:** Update tests
```python
def test_list_servers():
    result = list_servers()
    assert result["status"] == "success"  # New format
    assert result["action"] == "listed"
    assert "data" in result
```

### From Manual to Utilities

**Input Parsing:**
```python
# Before
params = json.loads(params_str) if isinstance(params_str, str) else params_str

# After
@normalize_input(params=InputFormat.DICT_OR_JSON)
def my_function(params: dict | None):
    # params is dict or None
```

**Response Building:**
```python
# Before
return {"success": True, "data": result, "message": "Created"}

# After
return Response.success(action="created", data=result)
```

**Error Messages:**
```python
# Before
return {"error": f"Server {server_id} not found"}

# After
error_msg = ErrorFormatter.not_found("server", server_id, list(servers.keys()))
return Response.error(error_code="not_found", message=error_msg)
```

{% if include_persistence_helpers -%}
**State Persistence:**
```python
# Before
class MyApp:
    def __init__(self):
        if Path("state.json").exists():
            with open("state.json") as f:
                self.state = json.load(f)

    def save(self):
        with open("state.json", "w") as f:
            json.dump(self.state, f)

# After
class MyApp(StatefulObject):
    def __init__(self):
        super().__init__(state_file="state.json")
        self.state = getattr(self, 'state', {})

    def save(self):
        self._save_state()
```
{% endif -%}

---

## Troubleshooting

### Common Issues

**Issue: Decorator doesn't transform parameters**
```python
# ❌ Wrong: Decorator after other decorators that change signature
@click.command()
@normalize_input(params=InputFormat.DICT_OR_JSON)
def my_command(params):
    pass

# ✅ Right: Put normalize_input closest to function
@normalize_input(params=InputFormat.DICT_OR_JSON)
@click.command()
def my_command(params):
    pass
```

**Issue: Response missing timestamp**
```python
# Check that you're using Response methods, not manual dicts
result = Response.success(action="test", data={})
assert "timestamp" in result  # Should be present
```

**Issue: Fuzzy matching suggests wrong results**
```python
# Filter available list to relevant subset
relevant = [s for s in all_servers if s.startswith(prefix)]
ErrorFormatter.not_found("server", server_id, relevant)
```

{% if include_persistence_helpers -%}
**Issue: State not persisting**
```python
# ❌ Forgot to call _save_state()
self.data = new_value

# ✅ Explicitly save
self.data = new_value
self._save_state()
```

**Issue: Large state file**
```python
# Override _get_state to exclude large data
def _get_state(self) -> dict:
    return {"config": self.config}  # Exclude self.large_cache
```
{% endif -%}

---

## Version History

### v1.0.0 ({{ _copier_conf.now }})

**Added:**
{% if include_api_utilities -%}
- Input normalization pattern (validation.py)
- Response standardization pattern (responses.py)
- Error formatting pattern (errors.py)
{% endif -%}
{% if include_persistence_helpers -%}
- State persistence pattern (persistence.py)
{% endif -%}

**Source:** Extracted from mcp-orchestration v0.1.3 learnings, generalized for all Python projects.

---

## Related Documentation

### How-To Guides
{% if include_api_utilities -%}
- [How-To: Use Input Validation](../how-to/use-input-validation.md)
- [How-To: Standardize Responses](../how-to/standardize-responses.md)
- [How-To: Improve Error Messages](../how-to/improve-error-messages.md)
{% endif -%}
{% if include_persistence_helpers -%}
- [How-To: Persist Application State](../how-to/persist-application-state.md)
{% endif -%}

### Source Code & Tests
{% if include_api_utilities -%}
- [validation.py](../../src/{{ package_name }}/utils/validation.py)
- [responses.py](../../src/{{ package_name }}/utils/responses.py)
- [errors.py](../../src/{{ package_name }}/utils/errors.py)
{% endif -%}
{% if include_persistence_helpers -%}
- [persistence.py](../../src/{{ package_name }}/utils/persistence.py)
{% endif -%}

### External Resources
- [Diátaxis Documentation Framework](https://diataxis.fr/) - Documentation structure
- [Python difflib](https://docs.python.org/3/library/difflib.html) - Fuzzy matching
- [Atomic file writes](https://www.notthewizard.com/2014/06/17/are-files-appends-really-atomic/) - Crash safety

---

**Last Updated:** {{ _copier_conf.now }}
**Version:** 1.0.0
**Maintained by:** {{ author_name }}
