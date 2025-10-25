---
title: Add a New MCP Server to Registry
audience: end-users
difficulty: advanced
time: 15 minutes
wave: 1.1
version: v0.1.3
---

# Add a New MCP Server to Registry

**Goal:** Register a custom MCP server so it's available via `list_available_servers` and `add_server_to_config`.

**Time:** 15 minutes

**Prerequisites:**
- Python programming knowledge
- Understanding of MCP server structure
- [Get Started](get-started.md) - mcp-orchestration installed

**Note:** This is an advanced topic. Most users will only use the 15 pre-registered servers.

---

## When to Use This

You need to add a server to the registry when:

1. **Custom MCP server** - You built your own MCP server
2. **Third-party server** - Using a server not in the default 15
3. **Modified server** - Customized version of existing server
4. **Unreleased server** - Pre-release or beta MCP server

**If using a default server** (filesystem, github, etc.), you don't need this guide - they're already registered.

---

## Quick Reference

**Programmatic registration:**

```python
from mcp_orchestrator.servers import ServerDefinition, TransportType, ParameterDefinition, get_default_registry

# Define your server
my_server = ServerDefinition(
    server_id="my-custom-server",
    display_name="My Custom Server",
    description="Does custom things",
    transport=TransportType.STDIO,
    stdio_command="python",
    stdio_args=["/path/to/my_server.py"],
    parameters=[],
    tags=["custom"]
)

# Register it
registry = get_default_registry()
registry.register(my_server)
```

---

## Step-by-Step

### Step 1: Understand Your Server

Gather information about the server you want to register:

**Required information:**
- **Server ID** - Unique identifier (e.g., "my-custom-server")
- **Display name** - Human-readable name
- **Description** - What it does
- **Transport type** - stdio, HTTP, or SSE
- **Command** - How to start it

**Optional information:**
- Parameters (if configurable)
- Environment variables (if needed)
- NPM package (if installable via npm)
- Documentation URL
- Tags (for search/categorization)

### Step 2: Determine Transport Configuration

#### For stdio servers:

```python
transport=TransportType.STDIO
stdio_command="python"  # or "node", "npx", etc.
stdio_args=["/path/to/server.py"]
```

#### For HTTP servers:

```python
transport=TransportType.HTTP
http_url="http://localhost:8080/mcp"
http_auth_type="bearer"  # or "none", "basic"
```

#### For SSE servers:

```python
transport=TransportType.SSE
http_url="http://localhost:8080/sse"
http_auth_type="none"
```

### Step 3: Define Parameters (If Any)

If your server accepts configuration parameters:

```python
parameters=[
    ParameterDefinition(
        name="api_key",
        type="string",
        description="API key for authentication",
        required=True,
        example="sk_test_1234"
    ),
    ParameterDefinition(
        name="timeout",
        type="number",
        description="Request timeout in seconds",
        required=False,
        default=30
    )
]
```

### Step 4: Create ServerDefinition

```python
from mcp_orchestrator.servers import ServerDefinition, TransportType, ParameterDefinition

my_server = ServerDefinition(
    server_id="my-api-server",
    display_name="My API Server",
    description="Connects to my custom API",
    transport=TransportType.STDIO,
    stdio_command="python",
    stdio_args=["-m", "my_mcp_server"],
    parameters=[
        ParameterDefinition(
            name="api_endpoint",
            type="url",
            description="API base URL",
            required=True,
            example="https://api.example.com"
        )
    ],
    required_env=["API_KEY"],
    optional_env=["DEBUG"],
    tags=["api", "custom"],
    documentation_url="https://github.com/me/my-mcp-server",
    npm_package="@me/my-mcp-server"  # if published to npm
)
```

### Step 5: Register the Server

```python
from mcp_orchestrator.servers import get_default_registry

# Get the registry
registry = get_default_registry()

# Register your server
registry.register(my_server)
```

**Note:** This registers in the current Python session. For persistent registration, see [Making it Permanent](#making-it-permanent) below.

---

## Complete Examples

### Example 1: Simple Custom Server

```python
from mcp_orchestrator.servers import ServerDefinition, TransportType, get_default_registry

# Define a simple Python script server
weather_server = ServerDefinition(
    server_id="weather-local",
    display_name="Local Weather Server",
    description="Provides local weather data",
    transport=TransportType.STDIO,
    stdio_command="python",
    stdio_args=["/Users/me/mcp-servers/weather.py"],
    parameters=[],
    tags=["weather", "local"]
)

# Register it
registry = get_default_registry()
registry.register(weather_server)
```

Now you can use it:

```
> Add weather-local server
```

### Example 2: Server with Parameters

```python
from mcp_orchestrator.servers import ServerDefinition, TransportType, ParameterDefinition, get_default_registry

# Define a server that needs configuration
api_server = ServerDefinition(
    server_id="my-api",
    display_name="My Custom API",
    description="Connects to my backend API",
    transport=TransportType.STDIO,
    stdio_command="node",
    stdio_args=["/path/to/server.js", "{endpoint}"],
    parameters=[
        ParameterDefinition(
            name="endpoint",
            type="url",
            description="API endpoint URL",
            required=True,
            example="https://api.myservice.com"
        )
    ],
    required_env=["API_TOKEN"],
    tags=["api"]
)

registry = get_default_registry()
registry.register(api_server)
```

Use it:

```
> Add my-api server with endpoint https://api.myservice.com
```

### Example 3: HTTP Server

```python
from mcp_orchestrator.servers import ServerDefinition, TransportType, get_default_registry

# Define an HTTP-based server
remote_server = ServerDefinition(
    server_id="remote-mcp",
    display_name="Remote MCP Service",
    description="Remote MCP server over HTTP",
    transport=TransportType.HTTP,
    http_url="https://mcp.example.com/api",
    http_auth_type="bearer",
    parameters=[],
    required_env=["BEARER_TOKEN"],
    tags=["remote", "http"]
)

registry = get_default_registry()
registry.register(remote_server)
```

**Note:** HTTP servers are automatically wrapped with mcp-remote when added to configs.

---

## Making it Permanent

The above examples register servers for the current Python session only. For permanent registration:

### Option 1: Create a Python Module

Create `/Users/you/.mcp-orchestration/custom_servers.py`:

```python
"""Custom MCP server definitions."""

from mcp_orchestrator.servers import ServerDefinition, TransportType, ParameterDefinition

def get_custom_servers():
    """Return list of custom server definitions."""
    return [
        ServerDefinition(
            server_id="weather-local",
            display_name="Local Weather",
            description="Local weather data",
            transport=TransportType.STDIO,
            stdio_command="python",
            stdio_args=["/Users/me/weather.py"],
            parameters=[],
            tags=["weather"]
        ),
        ServerDefinition(
            server_id="my-api",
            display_name="My API",
            description="My custom API",
            transport=TransportType.STDIO,
            stdio_command="node",
            stdio_args=["/path/to/api.js", "{endpoint}"],
            parameters=[
                ParameterDefinition(
                    name="endpoint",
                    type="url",
                    description="API URL",
                    required=True
                )
            ],
            tags=["api"]
        )
    ]
```

### Option 2: Modify Defaults (Not Recommended)

**Warning:** Editing mcp-orchestration source code means your changes will be lost on upgrade.

Edit `src/mcp_orchestrator/servers/defaults.py` and add your servers to the list.

### Option 3: Runtime Registration Script

Create a startup script that registers servers:

`~/.mcp-orchestration/register_servers.py`:

```python
#!/usr/bin/env python3
"""Register custom MCP servers on startup."""

import sys
sys.path.insert(0, "/Users/me/.mcp-orchestration")

from custom_servers import get_custom_servers
from mcp_orchestrator.servers import get_default_registry

def main():
    registry = get_default_registry()
    for server in get_custom_servers():
        try:
            registry.register(server)
            print(f"✓ Registered {server.server_id}")
        except ValueError as e:
            print(f"✗ Failed to register {server.server_id}: {e}")

if __name__ == "__main__":
    main()
```

Run on MCP server startup (modify Claude Desktop config):

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "sh",
      "args": [
        "-c",
        "python ~/.mcp-orchestration/register_servers.py && mcp-orchestration"
      ]
    }
  }
}
```

---

## Advanced: Server Registry API

### Register

```python
registry.register(server_definition)
```

Raises `ValueError` if server_id already exists.

### Update

```python
registry.update(server_definition)
```

Updates existing server (creates if doesn't exist).

### Unregister

```python
registry.unregister("server-id")
```

Removes server from registry.

### Get

```python
server = registry.get("server-id")
```

Returns `ServerDefinition` or raises `ServerNotFoundError`.

### List All

```python
servers = registry.list_all()
```

### Search

```python
servers = registry.search("keyword")
```

Searches name, description, and tags.

### Filter by Transport

```python
from mcp_orchestrator.servers import TransportType

stdio_servers = registry.list_by_transport(TransportType.STDIO)
```

---

## Troubleshooting

### "Server ID already registered"

**Symptom:** `ValueError` when calling `register()`

**Solutions:**

1. **Use `update()` instead**

   ```python
   registry.update(my_server)  # Overwrites existing
   ```

2. **Choose different server_id**

   ```python
   server_id="my-custom-api-v2"
   ```

3. **Unregister first**

   ```python
   registry.unregister("my-custom-api")
   registry.register(my_server)
   ```

### Server doesn't appear in list

**Symptom:** `list_available_servers` doesn't show your server

**Possible causes:**

1. **Not registered in same process**

   Solution: Ensure registration happens before MCP server starts

2. **Registered in different registry instance**

   Solution: Use `get_default_registry()` singleton

3. **Registration failed silently**

   Solution: Check for exceptions during `register()`

### Parameters not substituted correctly

**Symptom:** Parameter placeholders like `{endpoint}` appear literally in config

**Solutions:**

1. **Check placeholder format**

   Use `{param_name}` in stdio_args or http_url

2. **Verify parameter name matches**

   Parameter definition name must match placeholder

3. **Check transport type**

   Parameters work with stdio_args and http_url, not stdio_command

---

## Security Considerations

**When registering custom servers:**

1. **Validate commands** - Ensure stdio_command paths are safe
2. **Sanitize parameters** - Don't allow arbitrary command injection
3. **Document env vars** - Clearly mark which are required/optional
4. **Test in isolation** - Verify server works before registering

**Don't register servers that:**
- Execute arbitrary code from parameters
- Access sensitive data without authentication
- Have known security vulnerabilities

---

## Next Steps

After registering a custom server:

1. **Test it**

   > What MCP servers are available?

   Verify your server appears

2. **Add to configuration**

   > Add [your-server-id] server with [parameters]

3. **Publish and use**

   See [Publish a Configuration](publish-config.md)

---

## See Also

- [Add an MCP Server to Config](add-server-to-config.md) - Use registered servers
- [Reference: ServerDefinition](../reference/server-definition.md) - API details
- [Explanation: Transport Abstraction](../explanation/transport-abstraction.md) - How transports work
- [MCP Server Specification](https://spec.modelcontextprotocol.io/) - Official MCP spec

---

**Future waves** will add:
- JSON-based server registry files
- UI for server registration
- Server validation and testing tools
- Community server sharing
