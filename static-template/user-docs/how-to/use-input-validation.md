---
title: "How-To: Use Input Validation"
type: how-to
audience: developers
status: active
last_updated: {{ generation_date }}
version: 1.0.0
related: [../reference/python-patterns.md]
tags: [validation, api, cli, input-handling]
---

# How-To: Use Input Validation

**Purpose:** Normalize inputs from multiple sources (JSON strings, dicts, key=value pairs) into consistent Python types.

**Use Cases:**
- REST APIs accepting JSON bodies
- CLI tools parsing `--param key=value` arguments
- MCP servers handling protocol variations
- Config parsers supporting multiple formats

---

## Quick Reference

| Scenario | InputFormat | Example |
|----------|-------------|---------|
| Accept dict or JSON string | `DICT_OR_JSON` | API body, config file |
| Accept list of key=value | `KV_PAIRS` | CLI arguments |
| Accept dict OR key=value | `DICT_OR_KV` | Flexible input |
| Only accept dict | `DICT_ONLY` | Strict validation |

---

## Basic Usage

### Example 1: Normalize JSON String or Dict

```python
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@normalize_input(params=InputFormat.DICT_OR_JSON)
async def my_function(params: dict | None = None):
    """Accept params as dict or JSON string."""
    print(params)

# Usage:
await my_function(params={"key": "value"})           # Dict: ✅ Works
await my_function(params='{"key": "value"}')         # JSON: ✅ Converted to dict
await my_function(params=None)                       # None: ✅ Pass-through
```

**What it does:**
- If `params` is a dict → pass through unchanged
- If `params` is JSON string → parse to dict
- If `params` is None → pass through unchanged
- Otherwise → raise `TypeError`

---

## Use Case: MCP Server Tool

### Problem
MCP tools receive parameters from multiple sources:
- MCP protocol sends `dict`
- Claude Desktop sometimes serializes as JSON `string`
- Need to handle both formats

### Solution

```python
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@mcp.tool()
@normalize_input(
    params=InputFormat.DICT_OR_JSON,
    env_vars=InputFormat.DICT_OR_JSON,
)
async def add_server(
    server_id: str,
    params: dict | None = None,
    env_vars: dict | None = None,
) -> dict:
    """Add server with normalized parameters.

    Args:
        server_id: Server identifier
        params: Server parameters (dict or JSON string)
        env_vars: Environment variables (dict or JSON string)
    """
    # params and env_vars are GUARANTEED to be dict or None here
    # No manual JSON parsing needed!

    return {
        "server_id": server_id,
        "params": params or {},
        "env_vars": env_vars or {},
    }
```

**Before normalization:**
```python
# Manual parsing (repeated in every tool)
if isinstance(params, str):
    import json
    params = json.loads(params)
elif params is None:
    params = {}
elif not isinstance(params, dict):
    raise TypeError(f"params must be dict or JSON string")

# Same for env_vars... (~20 lines of boilerplate)
```

**After normalization:**
```python
# Just add decorator - done! (~1 line)
@normalize_input(
    params=InputFormat.DICT_OR_JSON,
    env_vars=InputFormat.DICT_OR_JSON,
)
```

---

## Use Case: CLI Tool with Key=Value Args

### Problem
CLI tools receive `--param key=value` arguments as tuple of strings.
Need to parse into dict.

### Solution with `@normalize_input`

```python
import click
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@click.command()
@click.option('--param', multiple=True, help='Parameters as key=value')
@click.option('--env', multiple=True, help='Environment variables as key=value')
@normalize_input(
    param=InputFormat.KV_PAIRS,
    env=InputFormat.KV_PAIRS,
)
def configure(param: dict, env: dict):
    """Configure with key=value arguments."""
    print(f"Parameters: {param}")
    print(f"Environment: {env}")
```

**Usage:**
```bash
$ myapp configure --param host=localhost --param port=8080 --env DEBUG=true
Parameters: {'host': 'localhost', 'port': '8080'}
Environment: {'DEBUG': 'true'}
```

### Alternative: `parse_kv_args()` Helper

For simpler cases without decorator:

```python
import click
from {{ package_name }}.utils.validation import parse_kv_args

@click.command()
@click.option('--param', multiple=True)
def configure(param: tuple[str, ...]):
    """Configure with key=value arguments."""
    params_dict = parse_kv_args(param)
    print(f"Parameters: {params_dict}")
```

---

## Use Case: REST API Endpoint

### Problem
Framework might pass JSON body as:
- Already-parsed dict (most frameworks)
- Raw JSON string (some minimal frameworks)

### Solution

```python
from {{ package_name }}.utils.validation import normalize_input, InputFormat

@app.post("/api/create")
@normalize_input(body=InputFormat.DICT_OR_JSON)
async def create_resource(body: dict):
    """Create resource with normalized body.

    Accepts:
    - {"name": "test"} - Already parsed dict
    - '{"name": "test"}' - Raw JSON string
    """
    name = body.get("name")
    value = body.get("value", 0)

    return {"created": {"name": name, "value": value}}
```

---

## Advanced: Multiple Parameters

### Normalize Several Parameters at Once

```python
@normalize_input(
    data=InputFormat.DICT_OR_JSON,      # Accept dict or JSON
    options=InputFormat.KV_PAIRS,       # Accept list of key=value
    config=InputFormat.DICT_OR_KV,      # Accept either dict or key=value
)
async def process(
    data: dict,
    options: dict | None = None,
    config: dict | None = None,
):
    """Process with multiple normalized inputs."""
    print(f"Data: {data}")
    print(f"Options: {options}")
    print(f"Config: {config}")

# Usage examples:
await process(
    data='{"key": "value"}',                      # JSON string → dict
    options=["verbose=true", "mode=fast"],        # KV pairs → dict
    config={"debug": True},                       # Dict → pass-through
)
```

---

## InputFormat Types Reference

### `DICT_ONLY`
**Use:** Strict validation, only accept dict.

```python
@normalize_input(data=InputFormat.DICT_ONLY)
def my_func(data: dict):
    pass

my_func(data={"key": "value"})    # ✅ OK
my_func(data='{"key": "value"}')  # ❌ TypeError
```

### `DICT_OR_JSON`
**Use:** Accept dict or JSON string.

```python
@normalize_input(data=InputFormat.DICT_OR_JSON)
def my_func(data: dict):
    pass

my_func(data={"key": "value"})    # ✅ OK
my_func(data='{"key": "value"}')  # ✅ OK (converted)
my_func(data='[1, 2]')            # ❌ ValueError (must be object)
```

### `KV_PAIRS`
**Use:** Accept list of "key=value" strings or dict.

```python
@normalize_input(opts=InputFormat.KV_PAIRS)
def my_func(opts: dict):
    pass

my_func(opts=["k1=v1", "k2=v2"])  # ✅ OK (converted)
my_func(opts={"k1": "v1"})        # ✅ OK (pass-through)
my_func(opts="k1=v1")             # ❌ TypeError (must be list or dict)
```

### `DICT_OR_KV`
**Use:** Accept dict OR list of "key=value" strings.

```python
@normalize_input(data=InputFormat.DICT_OR_KV)
def my_func(data: dict):
    pass

my_func(data={"k1": "v1"})        # ✅ OK
my_func(data=["k1=v1", "k2=v2"])  # ✅ OK (converted)
my_func(data='{"k1": "v1"}')      # ❌ TypeError (no JSON support)
```

---

## Error Handling

### Errors Are Automatically Clear

```python
@normalize_input(params=InputFormat.DICT_OR_JSON)
def my_func(params: dict):
    pass

# Invalid JSON
my_func(params='{bad json}')
# ValueError: Parameter 'params' is invalid JSON: Expecting property name...
#            Expected: dict or JSON string

# Wrong type
my_func(params=123)
# TypeError: Parameter 'params' must be dict or JSON string, got int

# JSON array instead of object
my_func(params='[1, 2, 3]')
# ValueError: Parameter 'params' JSON must be object/dict, got list
```

### Catch and Handle Errors

```python
@normalize_input(data=InputFormat.DICT_OR_JSON)
def my_func(data: dict):
    return data

try:
    result = my_func(data='{bad json}')
except ValueError as e:
    print(f"Invalid input: {e}")
    # Handle error gracefully
```

---

## Works with Both Sync and Async

### Async Functions

```python
@normalize_input(params=InputFormat.DICT_OR_JSON)
async def async_func(params: dict):
    await asyncio.sleep(0.1)
    return params

await async_func(params='{"key": "value"}')  # ✅ Works
```

### Sync Functions

```python
@normalize_input(params=InputFormat.DICT_OR_JSON)
def sync_func(params: dict):
    return params

sync_func(params='{"key": "value"}')  # ✅ Works
```

The decorator **automatically detects** whether your function is async or sync.

---

## Best Practices

### ✅ DO: Use for External Inputs

```python
# Good: API inputs from external sources
@normalize_input(body=InputFormat.DICT_OR_JSON)
async def api_endpoint(body: dict):
    pass

# Good: CLI arguments from users
@normalize_input(config=InputFormat.KV_PAIRS)
def cli_command(config: dict):
    pass
```

### ❌ DON'T: Use for Internal Functions

```python
# Bad: Internal helper function (already has dict)
@normalize_input(data=InputFormat.DICT_OR_JSON)  # Unnecessary
def _internal_helper(data: dict):
    pass

# Good: No decorator needed
def _internal_helper(data: dict):
    pass
```

### ✅ DO: Specify Type Hints

```python
# Good: Clear type hints show what you get
@normalize_input(params=InputFormat.DICT_OR_JSON)
def my_func(params: dict | None = None):
    # params is dict or None (guaranteed)
    pass
```

### ✅ DO: Handle None Explicitly

```python
@normalize_input(params=InputFormat.DICT_OR_JSON)
def my_func(params: dict | None = None):
    # None passes through - handle it
    if params is None:
        params = {}  # Provide default

    return params
```

---

## Common Patterns

### Pattern 1: Optional Parameters with Defaults

```python
@normalize_input(
    params=InputFormat.DICT_OR_JSON,
    env_vars=InputFormat.DICT_OR_JSON,
)
def my_func(
    params: dict | None = None,
    env_vars: dict | None = None,
):
    params = params or {}        # Default to empty dict
    env_vars = env_vars or {}

    # Use params and env_vars...
```

### Pattern 2: Required Parameters

```python
@normalize_input(data=InputFormat.DICT_OR_JSON)
def my_func(data: dict):  # No default - required
    # Caller MUST provide data
    return data
```

### Pattern 3: Mix Normalized and Raw

```python
@normalize_input(config=InputFormat.DICT_OR_JSON)
def my_func(
    name: str,           # Raw parameter (no normalization)
    config: dict,        # Normalized parameter
    verbose: bool = False,  # Raw parameter
):
    print(f"{name}: {config} (verbose={verbose})")
```

---

## Troubleshooting

### Issue: "Parameter 'X' must be dict or JSON string"

**Cause:** Passing wrong type (e.g., integer, list).

**Solution:** Check what you're passing:
```python
# Wrong
my_func(params=123)         # ❌ int

# Right
my_func(params={"val": 123})  # ✅ dict
my_func(params='{"val": 123}')  # ✅ JSON string
```

### Issue: "Parameter 'X' is invalid JSON"

**Cause:** Malformed JSON string.

**Solution:** Validate JSON syntax:
```python
# Wrong
my_func(params="{key: 'value'}")  # ❌ Not valid JSON (no quotes on key)

# Right
my_func(params='{"key": "value"}')  # ✅ Valid JSON
```

### Issue: Decorator doesn't work with positional args

**Cause:** Decorator only normalizes **keyword arguments**.

**Solution:** Pass parameters as keywords:
```python
@normalize_input(data=InputFormat.DICT_OR_JSON)
def my_func(name: str, data: dict):
    pass

# Wrong
my_func("test", '{"key": "val"}')  # ❌ data is positional

# Right
my_func("test", data='{"key": "val"}')  # ✅ data is keyword
my_func(name="test", data='{"key": "val"}')  # ✅ Both keywords
```

---

## Related Documentation

- [Python Patterns Reference](../reference/python-patterns.md) - Full pattern catalog
- [API Reference](../../src/{{ package_name }}/utils/validation.py) - Source code
- [Tests](../../tests/utils/test_validation.py) - More examples

---

**Last Updated:** {{ generation_date }}
**Version:** 1.0.0
**Maintained by:** {{ author_name }}
