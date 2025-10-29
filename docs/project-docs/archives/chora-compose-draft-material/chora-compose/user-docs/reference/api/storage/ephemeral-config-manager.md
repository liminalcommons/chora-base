# API Reference: EphemeralConfigManager

**Module:** `chora_compose.storage.ephemeral_config`
**Class:** `EphemeralConfigManager`
**Version:** v1.1.0+
**Status:** Stable

---

## Overview

The `EphemeralConfigManager` class manages draft configurations in ephemeral storage (30-day retention) before persistence to the permanent `configs/` directory. It provides create, read, update, delete (CRUD) operations with atomic file writes and JSON Schema validation.

**Primary Use Case:** Conversational config creation workflow via MCP tools.

> **Note (v1.2.0):** While this storage class is implemented and functional, the MCP tools that use it (`draft_config`, `test_config`, `modify_config`, `save_config`) are planned for v1.3.0. The class is currently used internally by the system but not exposed through MCP tools.

---

## Class Definition

```python
class EphemeralConfigManager:
    """Manages draft configs in ephemeral storage before persistence.

    Draft configs are temporary configurations stored in ephemeral/drafts/
    that can be tested and iterated on before being persisted to the
    configs/ directory.

    Storage structure:
        ephemeral/
          drafts/
            content/
              draft-20251016T153045-a1b2c3.json
            artifact/
              draft-20251016T153045-xyz789.json
    """
```

---

## Constructor

### `__init__(base_path=None)`

Initialize ephemeral config manager.

**Signature:**
```python
def __init__(self, base_path: Path | str | None = None) -> None
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_path` | `Path \| str \| None` | `None` | Root directory for ephemeral storage. If None, uses `"ephemeral/"` in current directory. |

**Behavior:**
- Creates base directory if it doesn't exist
- Creates `content/` and `artifact/` subdirectories
- Uses `parents=True, exist_ok=True` (safe for concurrent init)

**Example:**
```python
from chora_compose.storage import get_ephemeral_config_manager

# Default location (ephemeral/ in current directory)
manager = get_ephemeral_config_manager()

# Custom location
from pathlib import Path
manager = EphemeralConfigManager(base_path="/tmp/my-drafts")
```

**Storage Structure Created:**
```
ephemeral/
└── drafts/
    ├── content/      # Content config drafts
    └── artifact/     # Artifact config drafts
```

---

## Instance Methods

### `create_draft(config_type, config_data, description=None)`

Create a new draft config with JSON Schema validation.

**Signature:**
```python
def create_draft(
    self,
    config_type: str,
    config_data: dict[str, Any],
    description: str | None = None,
) -> DraftConfig
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `config_type` | `str` | Yes | `"content"` or `"artifact"` |
| `config_data` | `dict[str, Any]` | Yes | Configuration JSON (must conform to JSON Schema v3.1) |
| `description` | `str \| None` | No | Optional human-readable description |

**Returns:** `DraftConfig` object with generated `draft_id` and metadata.

**Raises:**
- `ValueError`: If `config_type` is invalid (not "content" or "artifact")
- `ValueError`: If `config_data` fails JSON Schema validation

**Behavior:**
1. Validates `config_type` is "content" or "artifact"
2. Validates `config_data` against JSON Schema v3.1 (content or artifact schema)
3. Generates unique `draft_id` (format: `draft-{timestamp}-{random}`)
4. Adds `created_at` and `updated_at` timestamps (ISO 8601, UTC)
5. Writes to filesystem with atomic rename (temp file → final file)
6. Returns `DraftConfig` object

**Example:**
```python
from chora_compose.storage import get_ephemeral_config_manager

manager = get_ephemeral_config_manager()

# Create content config draft
config_data = {
    "id": "weekly-report",
    "generation": {
        "patterns": [{
            "type": "jinja2",
            "template": "report.md.jinja",
            "generation_config": {
                "context": {}
            }
        }]
    }
}

draft = manager.create_draft(
    config_type="content",
    config_data=config_data,
    description="Weekly team report config"
)

print(f"Draft ID: {draft.draft_id}")
print(f"Created: {draft.created_at}")
# Output:
# Draft ID: draft-20251016T153045-a1b2c3
# Created: 2025-10-16T15:30:45.123456+00:00
```

**Schema Validation Example:**
```python
# Invalid config (missing required fields)
invalid_config = {
    "id": "test"
    # Missing "generation" field
}

try:
    draft = manager.create_draft("content", invalid_config)
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: Validation error: Schema validation failed: 'generation' is a required property
```

**Atomic Write Guarantee:**
- Uses `tempfile.NamedTemporaryFile` + atomic `rename()`
- Never leaves partial/corrupted files
- Safe for concurrent operations

---

### `get_draft(draft_id)`

Retrieve a draft config by ID.

**Signature:**
```python
def get_draft(self, draft_id: str) -> DraftConfig
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `draft_id` | `str` | Yes | Draft identifier (e.g., "draft-20251016T153045-a1b2c3") |

**Returns:** `DraftConfig` object

**Raises:**
- `FileNotFoundError`: If draft doesn't exist in either content/ or artifact/

**Behavior:**
1. Searches in `ephemeral/drafts/content/` for `{draft_id}.json`
2. If not found, searches in `ephemeral/drafts/artifact/`
3. Reads JSON file and deserializes to `DraftConfig`
4. Raises `FileNotFoundError` if not found in either location

**Example:**
```python
# Retrieve draft
draft = manager.get_draft("draft-20251016T153045-a1b2c3")

print(f"Type: {draft.config_type}")
print(f"Data: {draft.config_data}")
print(f"Updated: {draft.updated_at}")

# Output:
# Type: content
# Data: {'id': 'weekly-report', 'generation': {...}}
# Updated: 2025-10-16T15:30:45.123456+00:00
```

**Error Handling:**
```python
try:
    draft = manager.get_draft("draft-nonexistent")
except FileNotFoundError as e:
    print(f"Draft not found: {e}")
    # Output: Draft not found: Draft not found: draft-nonexistent
```

**Performance:** O(1) - direct file read (not a directory scan)

---

### `update_draft(draft_id, updates)`

Update a draft config with incremental changes.

**Signature:**
```python
def update_draft(
    self,
    draft_id: str,
    updates: dict[str, Any]
) -> DraftConfig
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `draft_id` | `str` | Yes | Draft identifier |
| `updates` | `dict[str, Any]` | Yes | Dictionary of updates to apply (shallow merge) |

**Returns:** Updated `DraftConfig` object

**Raises:**
- `FileNotFoundError`: If draft doesn't exist
- `ValueError`: If validation fails after applying updates

**Behavior:**
1. Loads existing draft via `get_draft()`
2. Merges updates into `config_data` (shallow merge: `{**draft.config_data, **updates}`)
3. Validates merged config against JSON Schema
4. If valid:
   - Updates `config_data`
   - Updates `updated_at` timestamp
   - Writes back to filesystem (atomic)
   - Returns updated `DraftConfig`
5. If invalid:
   - Raises `ValueError` with schema errors
   - Original draft remains unchanged (transaction rollback)

**Example:**
```python
# Update draft with new fields
draft = manager.update_draft(
    draft_id="draft-20251016T153045-a1b2c3",
    updates={
        "inputs": {
            "sources": [{
                "type": "file",
                "path": "data.json",
                "format": "json"
            }]
        }
    }
)

print(f"Updated at: {draft.updated_at}")
# Output: Updated at: 2025-10-16T15:35:22.789012+00:00
```

**Merge Behavior (Shallow):**
```python
# Original draft config_data:
# {
#   "id": "report",
#   "generation": {...}
# }

# Update with:
updates = {"id": "new-report", "extra": "field"}

# Result (shallow merge):
# {
#   "id": "new-report",          ← updated
#   "generation": {...},         ← unchanged
#   "extra": "field"             ← added
# }
```

**Deep Nested Updates (Not Supported Directly):**
```python
# To update nested field like generation.patterns[0].template,
# you must provide full parent object:

updates = {
    "generation": {
        "patterns": [{
            "type": "jinja2",
            "template": "new-template.j2",  # ← nested change
            "generation_config": {...}
        }]
    }
}

# This replaces entire "generation" object
```

**Atomicity:**
- Update succeeds completely or fails completely (no partial state)
- Original draft preserved on validation failure
- Atomic file write ensures consistency

---

### `delete_draft(draft_id)`

Delete a draft config.

**Signature:**
```python
def delete_draft(self, draft_id: str) -> bool
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `draft_id` | `str` | Yes | Draft identifier |

**Returns:** `True` if deleted, `False` if not found

**Raises:** None (returns `False` instead of raising exception)

**Behavior:**
1. Searches in `content/` directory for draft file
2. If found: deletes file and returns `True`
3. If not found in `content/`, searches in `artifact/`
4. If found: deletes file and returns `True`
5. If not found in either: returns `False`

**Example:**
```python
# Delete draft
deleted = manager.delete_draft("draft-20251016T153045-a1b2c3")

if deleted:
    print("Draft deleted successfully")
else:
    print("Draft not found")
```

**Idempotent:** Safe to call multiple times (returns `False` after first deletion).

**File System Operation:** Direct `unlink()` - no atomic transaction needed.

---

### `list_drafts(config_type=None)`

List all draft configs, optionally filtered by type.

**Signature:**
```python
def list_drafts(self, config_type: str | None = None) -> list[DraftConfig]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config_type` | `str \| None` | `None` | Filter by `"content"` or `"artifact"`. If `None`, returns all drafts. |

**Returns:** List of `DraftConfig` objects, sorted by `created_at` (oldest first)

**Raises:**
- `ValueError`: If `config_type` is provided but invalid (not "content" or "artifact")

**Behavior:**
1. Scans specified directory (or both if `config_type=None`)
2. Reads all files matching `draft-*.json` pattern
3. Deserializes to `DraftConfig` objects
4. Skips malformed files (logs error but doesn't raise)
5. Sorts by `created_at` timestamp
6. Returns sorted list

**Example:**
```python
# List all drafts
all_drafts = manager.list_drafts()
print(f"Total drafts: {len(all_drafts)}")

for draft in all_drafts:
    print(f"  {draft.draft_id}: {draft.description or draft.config_type}")

# Output:
# Total drafts: 3
#   draft-20251014T091530-abc123: API docs
#   draft-20251015T143022-def456: artifact
#   draft-20251016T153045-a1b2c3: Weekly team report config
```

**Filter by Type:**
```python
# List only content drafts
content_drafts = manager.list_drafts(config_type="content")
print(f"Content drafts: {len(content_drafts)}")

# List only artifact drafts
artifact_drafts = manager.list_drafts(config_type="artifact")
print(f"Artifact drafts: {len(artifact_drafts)}")
```

**Error Handling (Malformed Files):**
```python
# If ephemeral/drafts/content/corrupted.json has invalid JSON,
# it's skipped silently (logged but not raised)

drafts = manager.list_drafts()  # Returns valid drafts only
```

**Performance:** O(n) where n = number of draft files (full directory scan + read)

---

### `persist_draft(draft_id, config_id)`

Persist a draft config to permanent `configs/` directory.

**Signature:**
```python
def persist_draft(self, draft_id: str, config_id: str) -> Path
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `draft_id` | `str` | Yes | Draft identifier |
| `config_id` | `str` | Yes | Permanent config ID (kebab-case, no slashes/dots) |

**Returns:** `Path` to persisted config file

**Raises:**
- `FileNotFoundError`: If draft doesn't exist
- `ValueError`: If `config_id` is invalid (contains `/`, `\`, `..`, or is empty)

**Behavior:**
1. Validates `config_id` (must be kebab-case, no path traversal)
2. Loads draft via `get_draft()`
3. Creates directory structure: `configs/{type}/{config_id}/`
4. Writes config to: `configs/{type}/{config_id}/{config_id}-{type}.json`
5. Uses atomic write (temp file → rename)
6. Returns path to persisted file

**Example:**
```python
# Persist draft to permanent storage
path = manager.persist_draft(
    draft_id="draft-20251016T153045-a1b2c3",
    config_id="weekly-team-report"
)

print(f"Saved to: {path}")
# Output: Saved to: configs/content/weekly-team-report/weekly-team-report-content.json
```

**Directory Structure Created:**
```
configs/
└── content/
    └── weekly-team-report/
        └── weekly-team-report-content.json  ← persisted config
```

**For Artifact Configs:**
```python
path = manager.persist_draft(
    draft_id="draft-20251015T143022-def456",
    config_id="complete-docs"
)

# Output: configs/artifact/complete-docs/complete-docs-artifact.json
```

**Validation:**
```python
# Invalid config_id (path traversal attempt)
try:
    manager.persist_draft("draft-xyz", "../evil-config")
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Invalid config_id: ../evil-config.
    #         Must be kebab-case, no path separators or parent refs.
```

**Atomicity:**
- Uses atomic file write (temp + rename)
- Never leaves partial files
- Safe even if process crashes mid-write

**Note:** Does NOT delete draft after persistence - draft remains in ephemeral storage.

---

## Private Methods

### `_generate_draft_id()`

Generate unique draft identifier.

**Signature:**
```python
def _generate_draft_id(self) -> str
```

**Returns:** Draft ID string

**Format:** `draft-{timestamp}-{random}`

**Example:** `draft-20251016T153045-a1b2c3`

**Components:**
- `draft-`: Fixed prefix
- `20251016T153045`: UTC timestamp (YYYYMMDDThhmmss)
- `a1b2c3`: 6-character hex random suffix (from `secrets.token_hex(3)`)

**Uniqueness:** Timestamp + cryptographically random suffix ensures uniqueness.

---

### `_get_draft_path(draft_id, config_type)`

Get filesystem path for a draft config.

**Signature:**
```python
def _get_draft_path(self, draft_id: str, config_type: str) -> Path
```

**Parameters:**
- `draft_id`: Draft identifier
- `config_type`: "content" or "artifact"

**Returns:** `Path` object

**Example:**
```python
path = manager._get_draft_path(
    "draft-20251016T153045-a1b2c3",
    "content"
)
# Returns: Path("ephemeral/drafts/content/draft-20251016T153045-a1b2c3.json")
```

---

### `_validate_config_type(config_type)`

Validate config type parameter.

**Signature:**
```python
def _validate_config_type(self, config_type: str) -> None
```

**Parameters:**
- `config_type`: Config type to validate

**Raises:**
- `ValueError`: If not "content" or "artifact"

**Example:**
```python
manager._validate_config_type("content")   # OK
manager._validate_config_type("artifact")  # OK
manager._validate_config_type("invalid")   # Raises ValueError
```

---

## Supporting Classes

### `DraftConfig`

Represents a draft configuration with metadata.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `draft_id` | `str` | Unique draft identifier |
| `config_type` | `str` | "content" or "artifact" |
| `config_data` | `dict[str, Any]` | Configuration JSON |
| `created_at` | `str` | ISO 8601 timestamp (UTC) of creation |
| `updated_at` | `str` | ISO 8601 timestamp (UTC) of last update |
| `description` | `str \| None` | Optional description |

**Methods:**

#### `to_dict()`

Convert to dictionary representation.

**Returns:** `dict[str, Any]`

**Example:**
```python
draft_dict = draft.to_dict()
print(draft_dict)
# {
#   "draft_id": "draft-20251016T153045-a1b2c3",
#   "config_type": "content",
#   "config_data": {...},
#   "created_at": "2025-10-16T15:30:45.123456+00:00",
#   "updated_at": "2025-10-16T15:35:22.789012+00:00",
#   "description": "Weekly team report config"
# }
```

---

## Singleton Access

### `get_ephemeral_config_manager()`

Get singleton instance of `EphemeralConfigManager`.

**Module:** `chora_compose.storage`

**Signature:**
```python
def get_ephemeral_config_manager() -> EphemeralConfigManager
```

**Returns:** Shared `EphemeralConfigManager` instance (default location)

**Example:**
```python
from chora_compose.storage import get_ephemeral_config_manager

# Get singleton instance
manager = get_ephemeral_config_manager()

# All calls return same instance
manager2 = get_ephemeral_config_manager()
assert manager is manager2  # True
```

**Why Singleton:**
- Ensures single source of truth for ephemeral storage
- Prevents conflicts from multiple manager instances
- Simplifies integration with MCP tools

---

## Usage Examples

### Example 1: Create → Test → Save Workflow

```python
from chora_compose.storage import get_ephemeral_config_manager
from chora_compose.generators.registry import GeneratorRegistry

manager = get_ephemeral_config_manager()
registry = GeneratorRegistry()

# 1. Create draft
config_data = {
    "id": "api-docs",
    "generation": {
        "patterns": [{
            "type": "jinja2",
            "template": "api-docs.md.jinja",
            "generation_config": {"context": {}}
        }]
    }
}

draft = manager.create_draft("content", config_data)
print(f"Draft created: {draft.draft_id}")

# 2. Test draft (preview generation)
generator = registry.get_generator("jinja2")
# ... use generator to render with draft.config_data ...
print("Preview looks good!")

# 3. Save to permanent storage
path = manager.persist_draft(draft.draft_id, "api-documentation")
print(f"Saved to: {path}")
```

---

### Example 2: Iterative Refinement

```python
manager = get_ephemeral_config_manager()

# Create initial draft
draft = manager.create_draft("content", {
    "id": "report",
    "generation": {"patterns": [{"type": "jinja2", ...}]}
})

# Iteration 1: Add inputs
draft = manager.update_draft(draft.draft_id, {
    "inputs": {"sources": [{"type": "file", "path": "data.json"}]}
})

# Iteration 2: Change template
draft = manager.update_draft(draft.draft_id, {
    "generation": {
        "patterns": [{
            "type": "jinja2",
            "template": "new-template.j2",
            "generation_config": {"context": {}}
        }]
    }
})

# Final: Save when satisfied
path = manager.persist_draft(draft.draft_id, "final-report")
```

---

### Example 3: Manage Multiple Drafts

```python
manager = get_ephemeral_config_manager()

# Create multiple draft options
draft_a = manager.create_draft("content", {...}, description="Option A: Jinja2")
draft_b = manager.create_draft("content", {...}, description="Option B: Demonstration")

# List and compare
drafts = manager.list_drafts(config_type="content")
for draft in drafts:
    print(f"{draft.draft_id}: {draft.description}")

# Choose winner and persist
manager.persist_draft(draft_a.draft_id, "chosen-approach")

# Clean up loser
manager.delete_draft(draft_b.draft_id)
```

---

## Integration with MCP Tools

The `EphemeralConfigManager` is used by the following MCP tools:

| MCP Tool | Manager Method |
|----------|---------------|
| `draft_config` | `create_draft()` |
| `test_config` | `get_draft()` |
| `modify_config` | `update_draft()` |
| `save_config` | `persist_draft()` |
| `cleanup_ephemeral` | `list_drafts()` + `delete_draft()` |

**Example MCP Tool Usage:**
```python
# In src/chora_compose/mcp/config_tools.py

@mcp.tool()
async def draft_config(config_type: str, config_data: dict[str, Any]) -> dict:
    manager = get_ephemeral_config_manager()
    draft = manager.create_draft(config_type, config_data)

    return {
        "draft_id": draft.draft_id,
        "config_type": draft.config_type,
        "created_at": draft.created_at,
        "validation_status": "valid"
    }
```

---

## Error Handling Guide

### Common Errors and Solutions

#### 1. Schema Validation Error

**Error:**
```python
ValueError: Schema validation failed: 'generation' is a required property
```

**Cause:** `config_data` missing required fields.

**Solution:**
```python
# Ensure all required fields present
config_data = {
    "id": "my-config",
    "generation": {  # ← Required field
        "patterns": [...]
    }
}
```

---

#### 2. Draft Not Found

**Error:**
```python
FileNotFoundError: Draft not found: draft-xyz123
```

**Cause:** Draft ID doesn't exist or was deleted.

**Solution:**
```python
# List available drafts
drafts = manager.list_drafts()
print("Available drafts:", [d.draft_id for d in drafts])
```

---

#### 3. Invalid Config ID

**Error:**
```python
ValueError: Invalid config_id: ../evil. Must be kebab-case, no path separators.
```

**Cause:** `config_id` contains invalid characters.

**Solution:**
```python
# Use kebab-case, alphanumeric + hyphens only
valid_id = "my-config-name"
manager.persist_draft(draft_id, valid_id)
```

---

## Performance Characteristics

| Operation | Time Complexity | Disk I/O |
|-----------|----------------|----------|
| `create_draft()` | O(1) | 1 write (atomic) |
| `get_draft()` | O(1) | 1 read |
| `update_draft()` | O(1) | 1 read + 1 write (atomic) |
| `delete_draft()` | O(1) | 1 delete |
| `list_drafts()` | O(n) | n reads (directory scan) |
| `persist_draft()` | O(1) | 1 read + 1 write (atomic) |

**where n = number of drafts**

---

## Thread Safety

**Current Status:** Not thread-safe (v1.1.0)

**Atomic Operations:**
- File writes use atomic rename (safe for single process)
- No locks for concurrent access

**Concurrent Access:**
- Multiple processes can safely write different drafts
- Concurrent writes to **same draft** may result in lost updates (last-write-wins)

**Future Enhancement:** Consider file locking for multi-process safety.

---

## Related Documentation

- **[How-To: Create Config Conversationally](../../../how-to/configs/create-config-conversationally.md)** - Using the manager in workflows
- **[How-To: Manage Draft Configs](../../../how-to/configs/manage-draft-configs.md)** - Storage management
- **[Tutorial: Conversational Config Creation](../../../tutorials/intermediate/02-conversational-config-creation.md)** - Hands-on learning
- **[Explanation: Conversational Workflow Authoring](../../../explanation/architecture/conversational-workflow-authoring.md)** - Architecture deep dive
- **[MCP Tool Reference](../../../mcp/tool-reference.md)** - MCP tools using this manager

---

## Source Code

**Location:** `src/chora_compose/storage/ephemeral_config.py`

**Classes:**
- `DraftConfig` - Draft config data model
- `EphemeralConfigManager` - Main manager class

**Functions:**
- `get_ephemeral_config_manager()` - Singleton accessor

---

**Last Updated:** October 16, 2025
**Version:** 1.1.0
