---
title: "How-To: Persist Application State"
type: how-to
audience: developers
status: active
last_updated: {{ generation_date }}
version: 1.0.0
related: [../reference/python-patterns.md]
tags: [persistence, state, storage, json]
---

# How-To: Persist Application State

**Purpose:** Automatically persist object state to disk using the `StatefulObject` mixin class.

**Use Cases:**
- CLI tools - Save session state, user preferences
- Daemons - Persist configuration between restarts
- Services - Save draft/pending operations
- MCP servers - Persist draft configurations
- Applications - Cache computed results

---

## Quick Reference

| Method | When to Use | Example |
|--------|-------------|---------|
| `__init__(state_file=...)` | Initialize with persistence | `super().__init__(state_file="~/.app/state.json")` |
| `_save_state()` | Explicitly save state | `self._save_state()` after modifying state |
| `_get_state()` | Customize what gets saved | Override to select specific fields |
| `_set_state(state)` | Customize restoration | Override to validate/transform loaded data |
| `_clear_state()` | Delete state file | For testing or user-requested deletion |

---

## Basic Usage

### Example 1: Simple Counter with Persistence

```python
from {{ package_name }}.utils.persistence import StatefulObject

class Counter(StatefulObject):
    """Counter that persists across restarts."""

    def __init__(self, state_file: str = "~/.counter/state.json"):
        # Initialize parent with state file
        super().__init__(state_file=state_file)

        # Use loaded value or default to 0
        self.count = getattr(self, 'count', 0)

    def increment(self):
        """Increment counter and save."""
        self.count += 1
        self._save_state()  # Persist immediately

    def decrement(self):
        """Decrement counter and save."""
        self.count -= 1
        self._save_state()

# Usage:
>>> counter = Counter()
>>> counter.increment()
>>> counter.increment()
>>> counter.count
2

# Later, in new process:
>>> counter2 = Counter()
>>> counter2.count  # Restored from disk
2
```

**What it does:**
- Creates `~/.counter/` directory automatically
- Saves state to `~/.counter/state.json` on each modification
- Loads state on initialization if file exists
- Uses atomic writes to prevent corruption

---

### Example 2: Configuration Manager

```python
from {{ package_name }}.utils.persistence import StatefulObject

class ConfigManager(StatefulObject):
    """Manage application configuration with persistence."""

    def __init__(self):
        super().__init__(state_file="~/.myapp/config.json")

        # Use loaded config or default
        self.config = getattr(self, 'config', {
            "theme": "dark",
            "timeout": 30,
            "debug": False,
        })

    def update(self, **settings):
        """Update configuration settings."""
        self.config.update(settings)
        self._save_state()

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)

# Usage:
>>> config = ConfigManager()
>>> config.update(theme="light", timeout=60)
>>> config.get("theme")
"light"

# Restart:
>>> config2 = ConfigManager()
>>> config2.get("theme")  # Restored
"light"
```

---

### Example 3: Server Registry

```python
from {{ package_name }}.utils.persistence import StatefulObject

class ServerRegistry(StatefulObject):
    """Registry of servers with persistence."""

    def __init__(self):
        super().__init__(state_file="~/.myapp/servers.json")
        self.servers = getattr(self, 'servers', {})

    def add_server(self, name: str, config: dict):
        """Add a server to the registry."""
        self.servers[name] = config
        self._save_state()

    def remove_server(self, name: str):
        """Remove a server from the registry."""
        if name in self.servers:
            del self.servers[name]
            self._save_state()

    def get_server(self, name: str) -> dict | None:
        """Get server configuration."""
        return self.servers.get(name)

# Usage:
>>> registry = ServerRegistry()
>>> registry.add_server("prod", {
...     "host": "prod.example.com",
...     "port": 443,
... })
>>> registry.get_server("prod")
{"host": "prod.example.com", "port": 443}
```

---

## Use Case: CLI Tool with Session State

### Problem
CLI tool needs to remember last-used settings across invocations.

### Solution

```python
import click
from {{ package_name }}.utils.persistence import StatefulObject

class Session(StatefulObject):
    """CLI session state."""

    def __init__(self):
        super().__init__(state_file="~/.mycli/session.json")

        # Restore or use defaults
        self.last_profile = getattr(self, 'last_profile', 'default')
        self.recent_commands = getattr(self, 'recent_commands', [])
        self.preferences = getattr(self, 'preferences', {})

    def set_profile(self, profile: str):
        """Set active profile."""
        self.last_profile = profile
        self._save_state()

    def add_command(self, command: str):
        """Track command in history."""
        self.recent_commands.append(command)
        # Keep only last 10
        self.recent_commands = self.recent_commands[-10:]
        self._save_state()

# Global session
session = Session()

@click.group()
@click.option('--profile', default=None)
def cli(profile):
    """My CLI tool."""
    if profile:
        session.set_profile(profile)
    else:
        # Use last-used profile
        click.echo(f"Using profile: {session.last_profile}")

@cli.command()
def build():
    """Build project."""
    session.add_command("build")
    click.echo("Building...")

# Usage:
$ mycli --profile prod build
Using profile: prod
Building...

$ mycli build  # Different session
Using profile: prod  # Remembered!
Building...
```

---

## Use Case: MCP Server with Draft Configurations

### Problem
MCP server needs to save draft configurations before committing to actual config file.

### Solution

```python
from {{ package_name }}.utils.persistence import StatefulObject
from {{ package_name }}.utils.responses import Response

class DraftConfigManager(StatefulObject):
    """Manage draft server configurations."""

    def __init__(self):
        super().__init__(state_file="~/.mcp/drafts.json")
        self.drafts = getattr(self, 'drafts', {})

    def save_draft(self, server_id: str, config: dict):
        """Save draft configuration."""
        self.drafts[server_id] = {
            "config": config,
            "timestamp": time.time(),
        }
        self._save_state()

    def get_draft(self, server_id: str) -> dict | None:
        """Get draft configuration."""
        draft = self.drafts.get(server_id)
        return draft["config"] if draft else None

    def commit_draft(self, server_id: str):
        """Commit draft to actual config."""
        if server_id in self.drafts:
            config = self.drafts[server_id]["config"]
            # Write to actual config...
            write_server_config(server_id, config)

            # Remove draft
            del self.drafts[server_id]
            self._save_state()

# MCP tools
draft_manager = DraftConfigManager()

@mcp.tool()
async def draft_server_config(server_id: str, config: dict) -> dict:
    """Save draft server configuration."""
    draft_manager.save_draft(server_id, config)

    return Response.success(
        action="drafted",
        data={"server_id": server_id},
        draft_saved=True,
    )

@mcp.tool()
async def commit_server_config(server_id: str) -> dict:
    """Commit draft configuration."""
    draft = draft_manager.get_draft(server_id)
    if not draft:
        return Response.error(
            error_code="no_draft",
            message=f"No draft found for server '{server_id}'",
        )

    draft_manager.commit_draft(server_id)

    return Response.success(
        action="committed",
        data={"server_id": server_id},
    )
```

---

## Advanced: Custom State Selection

### Use Case: Selective Persistence

**Problem:** Only want to persist specific fields, not all attributes.

**Solution:** Override `_get_state()` and `_set_state()`

```python
from {{ package_name }}.utils.persistence import StatefulObject

class MyApp(StatefulObject):
    """App with selective persistence."""

    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")

        # Persistent fields (will be saved)
        self.config = getattr(self, 'config', {})
        self.user_data = getattr(self, 'user_data', {})

        # Temporary fields (won't be saved)
        self.cache = {}
        self.temp_results = []

    def _get_state(self) -> dict:
        """Only save config and user_data."""
        return {
            "config": self.config,
            "user_data": self.user_data,
        }

    def _set_state(self, state: dict):
        """Only restore config and user_data."""
        self.config = state.get("config", {})
        self.user_data = state.get("user_data", {})

# Usage:
>>> app = MyApp()
>>> app.config = {"theme": "dark"}
>>> app.cache = {"temp": "data"}  # Won't be persisted
>>> app._save_state()

# Restart:
>>> app2 = MyApp()
>>> app2.config
{"theme": "dark"}
>>> app2.cache
{}  # Not persisted
```

---

## Advanced: State Migration

### Use Case: Migrating Old State Format

**Problem:** Changed state structure, need to migrate old saved state.

**Solution:** Override `_set_state()` to detect and migrate

```python
from {{ package_name }}.utils.persistence import StatefulObject

class MyApp(StatefulObject):
    """App with state migration."""

    VERSION = 2  # Current state version

    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")

        # Ensure fields exist
        self.version = getattr(self, 'version', self.VERSION)
        self.config = getattr(self, 'config', {})

    def _set_state(self, state: dict):
        """Restore state with migration."""
        version = state.get("version", 1)

        if version == 1:
            # Migrate from v1 to v2
            old_config = state.get("settings", {})
            self.config = {
                "theme": old_config.get("ui_theme", "dark"),
                "timeout": old_config.get("request_timeout", 30),
            }
            self.version = 2
            # Save migrated state
            self._save_state()

        elif version == 2:
            # Current version
            self.config = state.get("config", {})
            self.version = version

        else:
            # Unknown version - start fresh
            self.config = {}
            self.version = self.VERSION

# Usage:
# Old state.json (v1):
# {"settings": {"ui_theme": "light", "request_timeout": 60}}

>>> app = MyApp()  # Auto-migrates on load
>>> app.config
{"theme": "light", "timeout": 60}
>>> app.version
2

# New state.json (v2):
# {"version": 2, "config": {"theme": "light", "timeout": 60}}
```

---

## Advanced: Nested Objects

### Use Case: Persisting Objects, Not Just Dicts

**Problem:** Need to persist custom objects, not just primitives/dicts.

**Solution:** Convert objects to/from dicts in `_get_state()` and `_set_state()`

```python
from dataclasses import dataclass, asdict
from {{ package_name }}.utils.persistence import StatefulObject

@dataclass
class Server:
    """Server configuration."""
    name: str
    host: str
    port: int

    def to_dict(self) -> dict:
        """Convert to dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Server":
        """Create from dict."""
        return cls(**data)

class ServerManager(StatefulObject):
    """Manage servers with object persistence."""

    def __init__(self):
        super().__init__(state_file="~/.servers/state.json")
        self.servers = getattr(self, 'servers', {})

    def _get_state(self) -> dict:
        """Convert Server objects to dicts."""
        return {
            "servers": {
                name: server.to_dict()
                for name, server in self.servers.items()
            }
        }

    def _set_state(self, state: dict):
        """Convert dicts back to Server objects."""
        servers_data = state.get("servers", {})
        self.servers = {
            name: Server.from_dict(data)
            for name, data in servers_data.items()
        }

    def add_server(self, server: Server):
        """Add a server."""
        self.servers[server.name] = server
        self._save_state()

# Usage:
>>> manager = ServerManager()
>>> manager.add_server(Server("prod", "prod.example.com", 443))
>>> manager.servers["prod"].host
"prod.example.com"

# Restart:
>>> manager2 = ServerManager()
>>> isinstance(manager2.servers["prod"], Server)
True
>>> manager2.servers["prod"].host
"prod.example.com"
```

---

## Atomic Writes

### How It Works

`StatefulObject` uses atomic writes to prevent data corruption:

1. **Write to temp file** in same directory
2. **Fsync** to ensure data on disk (not just OS buffer)
3. **Atomic rename** to target file

**Why this matters:**
- If process crashes during save, old file remains intact
- No partial/corrupted state files
- Safe for concurrent writes from multiple processes

**Example scenario:**
```python
app.count = 100
app._save_state()  # Starts writing...
# CRASH HERE - old file still has count=99, temp file deleted
```

Without atomic writes:
```
state.json (corrupted): {"count": 1
```

With atomic writes:
```
state.json (intact): {"count": 99}
temp file: deleted automatically
```

---

## Best Practices

### ✅ DO: Save After Each Modification

```python
# Good: Save immediately after changes
def add_item(self, item: dict):
    self.items.append(item)
    self._save_state()  # Persist change

# Bad: Rely on manual saves
def add_item(self, item: dict):
    self.items.append(item)
    # User might forget to call _save_state()
```

### ✅ DO: Use Defaults with getattr()

```python
# Good: Provide defaults for new installations
def __init__(self):
    super().__init__(state_file="state.json")
    self.config = getattr(self, 'config', {"default": "value"})

# Bad: Assume attribute exists
def __init__(self):
    super().__init__(state_file="state.json")
    # Will fail if no state file exists
    self.config = self.config
```

### ✅ DO: Keep State JSON-Serializable

```python
# Good: Use JSON-serializable types
self.data = {
    "items": [1, 2, 3],
    "config": {"key": "value"},
    "timestamp": time.time(),  # float is OK
}

# Bad: Non-serializable types
self.data = {
    "func": lambda x: x,  # ❌ Function not serializable
    "date": datetime.now(),  # ❌ Use .isoformat() instead
    "path": Path("/tmp"),  # ❌ Use str(path) instead
}
```

### ✅ DO: Handle State File Paths Carefully

```python
# Good: Use ~ for user directory
super().__init__(state_file="~/.myapp/state.json")

# Good: Use absolute paths in production
super().__init__(state_file="/var/lib/myapp/state.json")

# Bad: Relative paths (depends on cwd)
super().__init__(state_file="state.json")  # Where is this?
```

### ❌ DON'T: Store Sensitive Data Unencrypted

```python
# Bad: Plain passwords in state file
self.config = {
    "password": "secret123",  # ❌ Visible in JSON file
}

# Better: Use system keyring
import keyring
keyring.set_password("myapp", "user", "secret123")

# Or: Store hash, not password
import hashlib
self.config = {
    "password_hash": hashlib.sha256(b"secret").hexdigest()
}
```

### ❌ DON'T: Persist Large Binary Data

```python
# Bad: Store large binary data
self.cache = {
    "image": base64.b64encode(image_bytes),  # ❌ Makes file huge
}

# Better: Store file path, not content
self.cache = {
    "image_path": "/path/to/image.png",
}
```

---

## Common Patterns

### Pattern 1: Singleton State Manager

```python
# Global singleton for app-wide state
_state_manager = None

def get_state_manager() -> StateManager:
    """Get or create global state manager."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager

class StateManager(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")
        self.data = getattr(self, 'data', {})

# Usage in tools:
@mcp.tool()
async def save_data(key: str, value: str):
    state = get_state_manager()
    state.data[key] = value
    state._save_state()
```

### Pattern 2: Multi-Profile State

```python
class ProfileManager(StatefulObject):
    """Manage multiple profiles."""

    def __init__(self, profile: str = "default"):
        # Different file per profile
        state_file = f"~/.myapp/profiles/{profile}.json"
        super().__init__(state_file=state_file)
        self.profile = profile
        self.settings = getattr(self, 'settings', {})

# Usage:
>>> prod_profile = ProfileManager("production")
>>> dev_profile = ProfileManager("development")
```

### Pattern 3: Backup Before Save

```python
class BackupState(StatefulObject):
    """State with automatic backups."""

    def _save_state(self):
        """Save with backup of previous state."""
        # Backup existing file
        if self._state_file.exists():
            backup = self._state_file.with_suffix('.json.bak')
            shutil.copy2(self._state_file, backup)

        # Save normally
        super()._save_state()
```

---

## Troubleshooting

### Issue: State not persisting

**Check:**
1. Are you calling `_save_state()` after modifications?
2. Does the process have write permissions for the directory?
3. Is the state JSON-serializable?

**Debug:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Will show: "Saved state to /path/to/state.json"
app._save_state()
```

### Issue: State file corrupt

**Solution:** Delete and restart fresh

```python
app._clear_state()  # Delete state file
app.__init__()      # Reinitialize with defaults
```

### Issue: Large state file

**Solution:** Only persist essential data

```python
# Override _get_state to exclude large data
def _get_state(self) -> dict:
    return {
        "config": self.config,
        # Exclude: self.large_cache (don't persist)
    }
```

### Issue: Permission denied

**Check:**
```python
import os
state_file = Path("~/.myapp/state.json").expanduser()

# Check directory permissions
print(f"Dir: {state_file.parent}")
print(f"Writable: {os.access(state_file.parent, os.W_OK)}")

# Check file permissions (if exists)
if state_file.exists():
    print(f"File writable: {os.access(state_file, os.W_OK)}")
```

---

## Related Documentation

- [Python Patterns Reference](../reference/python-patterns.md) - Full pattern catalog
- [API Reference](../../src/{{ package_name }}/utils/persistence.py) - Source code
- [Tests](../../tests/utils/test_persistence.py) - More examples

---

**Last Updated:** {{ generation_date }}
**Version:** 1.0.0
**Maintained by:** {{ author_name }}
