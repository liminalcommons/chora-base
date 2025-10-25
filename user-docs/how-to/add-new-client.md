---
title: Add a New MCP Client
audience: end-users
difficulty: advanced
time: 20 minutes
wave: 1.0
version: v0.1.3
---

# Add a New MCP Client

**Goal:** Register a new MCP client (like Cursor, Zed, or custom IDE) so you can manage configurations for it.

**Time:** 20 minutes

**Prerequisites:**
- Python programming knowledge
- Understanding of the client's MCP configuration format
- [Get Started](get-started.md) - mcp-orchestration installed

**Note:** Claude Desktop and Cursor are already registered. This guide is for adding NEW clients.

---

## When to Use This

You need to add a client to the registry when:

1. **New MCP-compatible tool** - Using an editor/IDE that supports MCP but isn't pre-registered
2. **Custom client** - You built your own MCP client application
3. **Experimental client** - Testing beta/unreleased MCP clients

**If using Claude Desktop or Cursor**, they're already registered - skip this guide.

---

## Understanding MCP Clients

An **MCP client** is any application that:
- Consumes MCP (Model Context Protocol) servers
- Has a configuration file specifying which servers to use
- Supports the MCP stdio transport (at minimum)

**Examples:**
- Claude Desktop (pre-registered)
- Cursor IDE (pre-registered)
- Zed Editor (could be registered)
- Custom AI assistants
- Your own tools

---

## Quick Reference

**Programmatic registration:**

```python
from mcp_orchestrator.registry import (
    ClientDefinition,
    ClientCapabilities,
    ProfileDefinition,
    get_default_registry
)

# Define client
my_client = ClientDefinition(
    client_id="my-editor",
    display_name="My Editor",
    platform="cross-platform",
    config_location="~/.my-editor/mcp-config.json",
    config_format="json",
    capabilities=ClientCapabilities(
        environment_variables=True,
        command_args=True,
        working_directory=False,
        multiple_servers=True
    ),
    default_profiles=[
        ProfileDefinition(
            profile_id="default",
            display_name="Default Profile",
            description="Standard configuration"
        )
    ]
)

# Register it
registry = get_default_registry()
registry.register(my_client)
```

---

## Step-by-Step

### Step 1: Gather Client Information

You need to know:

**Required:**
- **Client ID** - Unique identifier (e.g., "zed-editor")
- **Display name** - Human-readable name (e.g., "Zed Editor")
- **Platform** - "macos", "windows", "linux", or "cross-platform"
- **Config location** - Where the client reads its config file
- **Config format** - Usually "json"

**Optional but recommended:**
- **Capabilities** - What the client supports (env vars, working directory, etc.)
- **Limitations** - Max servers, etc.
- **Version requirements** - Min/max supported versions
- **Default profiles** - Standard configurations (default, dev, prod)

### Step 2: Inspect Client's Config Format

Look at an example config for the client. Most MCP clients use this structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
      "env": {
        "VAR": "value"
      }
    }
  }
}
```

**Key questions:**
- Does it use `mcpServers` key? (standard)
- Does it support `env` for environment variables?
- Does it support `cwd` for working directory?
- Can it have multiple servers?

### Step 3: Determine Capabilities

```python
ClientCapabilities(
    environment_variables=True,   # Supports "env" field?
    command_args=True,            # Supports "args" field?
    working_directory=False,      # Supports "cwd" field?
    multiple_servers=True         # Can have >1 server?
)
```

**Example: Limited client**
```python
ClientCapabilities(
    environment_variables=False,  # No env vars
    command_args=True,
    working_directory=False,
    multiple_servers=False        # Only 1 server allowed
)
```

### Step 4: Define Profiles

Most clients should have at least a "default" profile:

```python
default_profiles=[
    ProfileDefinition(
        profile_id="default",
        display_name="Default Profile",
        description="Standard configuration for everyday use"
    )
]
```

**Multiple profiles example:**
```python
default_profiles=[
    ProfileDefinition(
        profile_id="default",
        display_name="Default",
        description="Standard config"
    ),
    ProfileDefinition(
        profile_id="dev",
        display_name="Development",
        description="Config for development with debug servers"
    ),
    ProfileDefinition(
        profile_id="prod",
        display_name="Production",
        description="Minimal servers for production use"
    )
]
```

### Step 5: Create ClientDefinition

```python
from mcp_orchestrator.registry import ClientDefinition, ClientCapabilities, ClientLimitations, ProfileDefinition

zed_client = ClientDefinition(
    client_id="zed-editor",
    display_name="Zed Editor",
    platform="cross-platform",
    config_location="~/.config/zed/mcp-settings.json",
    config_format="json",
    version_min="0.1.0",  # Minimum Zed version with MCP support
    capabilities=ClientCapabilities(
        environment_variables=True,
        command_args=True,
        working_directory=True,
        multiple_servers=True
    ),
    limitations=ClientLimitations(
        max_servers=None,  # Unlimited
        max_env_vars_per_server=None  # Unlimited
    ),
    default_profiles=[
        ProfileDefinition(
            profile_id="default",
            display_name="Default Profile",
            description="Standard Zed configuration"
        )
    ]
)
```

### Step 6: Register the Client

```python
from mcp_orchestrator.registry import get_default_registry

registry = get_default_registry()
registry.register(zed_client)
```

---

## Complete Examples

### Example 1: Zed Editor

```python
from mcp_orchestrator.registry import (
    ClientDefinition,
    ClientCapabilities,
    ProfileDefinition,
    get_default_registry
)

# Define Zed Editor client
zed = ClientDefinition(
    client_id="zed-editor",
    display_name="Zed Editor",
    platform="cross-platform",
    config_location="~/.config/zed/mcp-settings.json",
    config_format="json",
    capabilities=ClientCapabilities(
        environment_variables=True,
        command_args=True,
        working_directory=True,
        multiple_servers=True
    ),
    default_profiles=[
        ProfileDefinition(
            profile_id="default",
            display_name="Default",
            description="Standard configuration"
        )
    ]
)

# Register
registry = get_default_registry()
registry.register(zed)
```

Verify:

```python
# Check it worked
> List supported MCP clients

# Should now show "Zed Editor"
```

### Example 2: Custom AI Assistant

```python
from mcp_orchestrator.registry import (
    ClientDefinition,
    ClientCapabilities,
    ClientLimitations,
    ProfileDefinition,
    get_default_registry
)

# Define custom client with limitations
my_assistant = ClientDefinition(
    client_id="my-ai-assistant",
    display_name="My AI Assistant",
    platform="linux",
    config_location="/opt/my-assistant/config/mcp.json",
    config_format="json",
    version_min="1.0.0",
    capabilities=ClientCapabilities(
        environment_variables=True,
        command_args=True,
        working_directory=False,  # Not supported
        multiple_servers=True
    ),
    limitations=ClientLimitations(
        max_servers=5,  # Limit to 5 servers
        max_env_vars_per_server=10  # Limit env vars
    ),
    default_profiles=[
        ProfileDefinition(
            profile_id="default",
            display_name="Default",
            description="Standard profile"
        ),
        ProfileDefinition(
            profile_id="minimal",
            display_name="Minimal",
            description="Minimal servers for faster startup"
        )
    ]
)

registry = get_default_registry()
registry.register(my_assistant)
```

---

## Platform-Specific Config Locations

### macOS

```python
config_location="~/Library/Application Support/MyApp/config.json"
```

### Windows

```python
config_location="%APPDATA%\\MyApp\\config.json"
```

### Linux

```python
config_location="~/.config/myapp/mcp-config.json"
```

### Cross-Platform

If the client uses the same location on all platforms:

```python
platform="cross-platform"
config_location="~/.myapp/config.json"
```

---

## Making it Permanent

Similar to [server registry](add-server-to-registry.md#making-it-permanent), client registrations are session-only unless persisted.

### Option 1: Python Module

Create `~/.mcp-orchestration/custom_clients.py`:

```python
"""Custom MCP client definitions."""

from mcp_orchestrator.registry import (
    ClientDefinition,
    ClientCapabilities,
    ProfileDefinition
)

def get_custom_clients():
    """Return list of custom client definitions."""
    return [
        ClientDefinition(
            client_id="zed-editor",
            display_name="Zed Editor",
            platform="cross-platform",
            config_location="~/.config/zed/mcp-settings.json",
            config_format="json",
            capabilities=ClientCapabilities(
                environment_variables=True,
                command_args=True,
                working_directory=True,
                multiple_servers=True
            ),
            default_profiles=[
                ProfileDefinition(
                    profile_id="default",
                    display_name="Default",
                    description="Standard configuration"
                )
            ]
        )
    ]
```

### Option 2: Registration Script

Create `~/.mcp-orchestration/register_clients.py`:

```python
#!/usr/bin/env python3
"""Register custom MCP clients on startup."""

import sys
sys.path.insert(0, "/Users/me/.mcp-orchestration")

from custom_clients import get_custom_clients
from mcp_orchestrator.registry import get_default_registry

def main():
    registry = get_default_registry()
    for client in get_custom_clients():
        try:
            registry.register(client)
            print(f"✓ Registered {client.client_id}")
        except Exception as e:
            print(f"✗ Failed to register {client.client_id}: {e}")

if __name__ == "__main__":
    main()
```

---

## Using the Registered Client

After registration, you can:

### 1. List Clients

```
> What MCP clients are supported?
```

Your client should appear in the list.

### 2. List Profiles

```
> List profiles for zed-editor
```

### 3. Build Configurations

```python
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.servers import get_default_registry as get_server_registry

# Build config for your custom client
builder = ConfigBuilder(
    client_id="zed-editor",
    profile_id="default",
    server_registry=get_server_registry()
)

builder.add_server(
    server_id="filesystem",
    params={"path": "/Users/me/code"}
)

config = builder.build()
```

### 4. Publish Configurations

```
> Add filesystem server for my Zed editor profile
```

(Requires API extension to support non-default clients - coming in future wave)

---

## Advanced: Client Registry API

### Register

```python
registry.register(client_definition)
```

### Get Client

```python
client = registry.get_client("client-id")
```

### List All Clients

```python
clients = registry.list_clients()
```

### Get Profiles

```python
profiles = registry.get_profiles("client-id")
```

### Get Specific Profile

```python
profile = registry.get_profile("client-id", "profile-id")
```

### Check if Client Exists

```python
has_client = registry.has_client("client-id")
```

---

## Troubleshooting

### "Client already registered"

**Symptom:** Registration fails because client_id exists

**Solutions:**

1. **Use different client_id**

   ```python
   client_id="zed-editor-custom"
   ```

2. **Modify existing registration**

   ```python
   # Get existing
   client = registry.get_client("zed-editor")
   # Modify fields
   client.config_location = "/new/path"
   # Re-register (will overwrite)
   registry.register(client)
   ```

### Client doesn't appear in list

**Symptom:** `list_clients` doesn't show your client

**Possible causes:**

1. **Not registered in same process**

   Solution: Ensure registration before MCP server starts

2. **Used wrong registry instance**

   Solution: Always use `get_default_registry()` singleton

### Config generation fails

**Symptom:** Error when building configs for custom client

**Possible causes:**

1. **Wrong config format specified**

   Solution: Verify client actually uses JSON (not YAML, TOML, etc.)

2. **Capabilities mismatch**

   Solution: Ensure capabilities match what client actually supports

---

## Next Steps

After registering a client:

1. **Test client listing**

   ```
   > What MCP clients are supported?
   ```

2. **Check profiles**

   ```
   > List profiles for [your-client-id]
   ```

3. **Build configurations**

   See [Add an MCP Server](add-server-to-config.md)

4. **Document your client**

   Create README explaining how others can use it

---

## See Also

- [Add an MCP Server to Config](add-server-to-config.md) - Use servers with your client
- [Reference: ClientDefinition](../reference/client-definition.md) - API details
- [Get Started](get-started.md) - Initial setup
- [MCP Specification](https://spec.modelcontextprotocol.io/) - Official MCP spec

---

**Future waves** will add:
- JSON-based client registry files
- UI for client registration
- Auto-detection of installed clients
- Client capability testing tools
