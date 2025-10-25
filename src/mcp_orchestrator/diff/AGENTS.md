# Configuration Diff Engine Guide

**Purpose:** Guide for configuration diff engine (field-level change detection).

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **Diff configs:** `diff_engine.diff(local_payload, canonical_payload)` → DiffResult
- **Diff status:** `DiffResult.status` (up-to-date | outdated | diverged)
- **Recommendation:** `DiffResult.recommendation` (update | review | safe)
- **Testing:** `pytest tests/unit/test_diff.py`

---

## Architecture

**Path:** `src/mcp_orchestrator/diff/`

**Design Pattern:** Recursive structural diff with semantic interpretation

**Responsibilities:**
1. **Field-Level Comparison:** Detect added/removed/modified fields in nested structures
2. **Semantic Classification:** Categorize changes (breaking | compatible | cosmetic)
3. **Update Recommendation:** Advise user on action (update, review, safe to ignore)

### Files

```
diff/
├── __init__.py           # Public API exports
├── engine.py             # Core diff algorithm (recursive comparison)
├── semantic.py           # Semantic change classification
└── formatter.py          # Diff output formatting (markdown, JSON, colored)
```

---

## Diff Algorithm

### Input

- **local_payload** (dict): User's current configuration
- **canonical_payload** (dict): Authoritative configuration from storage

### Output: DiffResult

```python
{
    "status": "outdated",  # up-to-date | outdated | diverged
    "changes": [
        {
            "type": "added",  # added | removed | modified
            "path": "mcpServers.new-server",
            "canonical_value": {"command": "new-server", "args": []},
            "local_value": null,
            "semantic": "compatible"  # breaking | compatible | cosmetic
        },
        {
            "type": "modified",
            "path": "mcpServers.existing-server.args",
            "canonical_value": ["--new-flag"],
            "local_value": ["--old-flag"],
            "semantic": "breaking"
        }
    ],
    "recommendation": "review",  # update | review | safe
    "metadata": {
        "canonical_artifact_id": "aabbccddee...",
        "change_count": 2,
        "breaking_changes": 1,
        "compatible_changes": 1,
        "cosmetic_changes": 0
    }
}
```

---

## Diff Statuses

### up-to-date

**Meaning:** Local payload exactly matches canonical

**Behavior:**
- No changes detected
- User has latest version
- No action needed

**Recommendation:** `"safe"`

**Example:**
```python
local = {"mcpServers": {"fs": {"command": "mcp-fs"}}}
canonical = {"mcpServers": {"fs": {"command": "mcp-fs"}}}

result = diff_configs(local, canonical)
assert result.status == "up-to-date"
assert result.changes == []
```

### outdated

**Meaning:** Canonical has changes not in local

**Behavior:**
- User is behind latest version
- Canonical added/modified fields
- Local missing updates

**Recommendation:**
- `"update"` if only compatible changes
- `"review"` if breaking changes present

**Example:**
```python
local = {"mcpServers": {"fs": {"command": "mcp-fs"}}}
canonical = {"mcpServers": {
    "fs": {"command": "mcp-fs"},
    "new-server": {"command": "new"}  # Added in canonical
}}

result = diff_configs(local, canonical)
assert result.status == "outdated"
assert len(result.changes) == 1
assert result.changes[0]["type"] == "added"
```

### diverged

**Meaning:** Both local and canonical have unique changes

**Behavior:**
- User made customizations
- Canonical also updated
- Manual merge required

**Recommendation:** `"review"` (always requires manual inspection)

**Example:**
```python
local = {
    "mcpServers": {
        "fs": {"command": "mcp-fs"},
        "custom": {"command": "custom"}  # User added
    }
}
canonical = {
    "mcpServers": {
        "fs": {"command": "mcp-fs"},
        "new-server": {"command": "new"}  # Canonical added
    }
}

result = diff_configs(local, canonical)
assert result.status == "diverged"
# Both have unique changes
```

---

## Semantic Classification

### breaking

**Definition:** Changes that may cause errors or break existing functionality

**Examples:**
- Removes required fields
- Changes field types (string → number)
- Incompatible value changes (command renamed)
- Removes server from config

**Action:** Manual review required

**Classification Logic:**
```python
def is_breaking(change):
    if change["type"] == "removed":
        # Removing fields often breaking
        return True
    if change["type"] == "modified":
        # Type change is breaking
        if type(change["local_value"]) != type(change["canonical_value"]):
            return True
        # Command/critical field change
        if "command" in change["path"]:
            return True
    return False
```

### compatible

**Definition:** Backward-compatible changes, safe to auto-apply

**Examples:**
- Adds new optional fields
- Updates non-critical values
- Adds new server to config
- Documentation/comment updates

**Action:** Safe to auto-update

**Classification Logic:**
```python
def is_compatible(change):
    if change["type"] == "added":
        # Adding optional fields is compatible
        return True
    if change["type"] == "modified":
        # Non-critical field updates
        if any(field in change["path"] for field in ["description", "env", "metadata"]):
            return True
    return False
```

### cosmetic

**Definition:** No functional impact, formatting/style changes

**Examples:**
- Whitespace changes
- Comment updates
- Field order changes (JSON objects)
- Formatting differences

**Action:** Safe to ignore or auto-apply

**Classification Logic:**
```python
def is_cosmetic(change):
    # JSON normalization differences
    if json.dumps(change["local_value"], sort_keys=True) == \
       json.dumps(change["canonical_value"], sort_keys=True):
        return True
    # Comment-only changes
    if "comment" in change["path"] or "description" in change["path"]:
        return True
    return False
```

---

## Recursive Diff Algorithm

### Core Algorithm

```python
def recursive_diff(local: dict, canonical: dict, path: str = "") -> list:
    """Recursively compare nested dictionaries."""
    changes = []

    # Added fields (in canonical, not in local)
    for key in canonical.keys() - local.keys():
        changes.append({
            "type": "added",
            "path": f"{path}.{key}" if path else key,
            "canonical_value": canonical[key],
            "local_value": None,
            "semantic": classify_semantic("added", key, canonical[key])
        })

    # Removed fields (in local, not in canonical)
    for key in local.keys() - canonical.keys():
        changes.append({
            "type": "removed",
            "path": f"{path}.{key}" if path else key,
            "canonical_value": None,
            "local_value": local[key],
            "semantic": "breaking"  # Removal often breaking
        })

    # Modified fields (in both, but different values)
    for key in local.keys() & canonical.keys():
        local_val = local[key]
        canonical_val = canonical[key]

        # Recurse into nested dicts
        if isinstance(local_val, dict) and isinstance(canonical_val, dict):
            nested_path = f"{path}.{key}" if path else key
            changes.extend(recursive_diff(local_val, canonical_val, nested_path))

        # Compare values
        elif local_val != canonical_val:
            changes.append({
                "type": "modified",
                "path": f"{path}.{key}" if path else key,
                "canonical_value": canonical_val,
                "local_value": local_val,
                "semantic": classify_semantic("modified", key, canonical_val, local_val)
            })

    return changes
```

### Semantic Classification

```python
def classify_semantic(change_type: str, key: str, canonical_value, local_value=None) -> str:
    """Classify semantic impact of change."""

    if change_type == "removed":
        # Removals are breaking unless optional/deprecated
        if key.startswith("_") or key in ["deprecated", "optional"]:
            return "cosmetic"
        return "breaking"

    if change_type == "added":
        # Additions are compatible unless required
        if key in ["required", "critical"]:
            return "breaking"
        return "compatible"

    if change_type == "modified":
        # Type changes are breaking
        if type(local_value) != type(canonical_value):
            return "breaking"

        # Command/critical field changes are breaking
        if key in ["command", "required", "critical"]:
            return "breaking"

        # Non-critical updates are compatible
        if key in ["description", "env", "metadata", "optional"]:
            return "compatible"

        # Default: compatible for modifications
        return "compatible"

    return "cosmetic"
```

---

## Common Tasks

### Diff Two Configs

```python
from mcp_orchestrator.diff import diff_configs

local_payload = {
    "mcpServers": {
        "filesystem": {
            "command": "mcp-filesystem",
            "args": ["--root", "/old/path"]
        }
    }
}

canonical_payload = {
    "mcpServers": {
        "filesystem": {
            "command": "mcp-filesystem",
            "args": ["--root", "/new/path"]
        },
        "new-server": {
            "command": "mcp-new",
            "args": []
        }
    }
}

result = diff_configs(local_payload, canonical_payload)

print(f"Status: {result.status}")  # outdated
print(f"Changes: {len(result.changes)}")  # 2
print(f"Recommendation: {result.recommendation}")  # review or update
```

### Format Diff for Display

```python
from mcp_orchestrator.diff import format_diff

# Format as markdown
markdown = format_diff(diff_result, format="markdown")
print(markdown)
# Output:
# ## Configuration Diff
# **Status:** outdated
# **Changes:** 2
#
# ### Added
# - `mcpServers.new-server` (compatible)
#
# ### Modified
# - `mcpServers.filesystem.args` (breaking)
#   - Old: `["--root", "/old/path"]`
#   - New: `["--root", "/new/path"]`

# Format as JSON
json_output = format_diff(diff_result, format="json")

# Format with colors (terminal)
colored = format_diff(diff_result, format="colored")
```

### Apply Changes

```python
from mcp_orchestrator.diff import apply_changes

# Apply only compatible changes
updated_payload = apply_changes(
    local_payload,
    diff_result.changes,
    strategy="safe"  # Only apply compatible changes
)

# Apply all changes (dangerous)
updated_payload = apply_changes(
    local_payload,
    diff_result.changes,
    strategy="all"  # Apply all changes (including breaking)
)

# Manual selective apply
selected_changes = [c for c in diff_result.changes if c["semantic"] != "breaking"]
updated_payload = apply_changes(local_payload, selected_changes, strategy="all")
```

---

## Testing Diff Engine

**Coverage Target:** ≥90% (diff algorithm is critical path)

### Test Categories

1. **Happy Path:** Identical configs → up-to-date
```python
def test_identical_configs_are_up_to_date():
    config = {"mcpServers": {"fs": {"command": "mcp-fs"}}}
    result = diff_configs(config, config)
    assert result.status == "up-to-date"
    assert len(result.changes) == 0
```

2. **Additions:** Canonical adds field → outdated
```python
def test_canonical_adds_field_is_outdated():
    local = {"mcpServers": {"fs": {}}}
    canonical = {"mcpServers": {"fs": {}, "new": {}}}

    result = diff_configs(local, canonical)
    assert result.status == "outdated"
    assert len(result.changes) == 1
    assert result.changes[0]["type"] == "added"
```

3. **Removals:** Local removes field → diverged
```python
def test_local_removes_field_is_diverged():
    local = {"mcpServers": {"fs": {}}}
    canonical = {"mcpServers": {"fs": {}, "old": {}}}

    result = diff_configs(local, canonical)
    assert result.status == "diverged"  # Local removed "old"
```

4. **Modifications:** Field value changed → outdated/diverged
```python
def test_field_modification_detected():
    local = {"mcpServers": {"fs": {"command": "old"}}}
    canonical = {"mcpServers": {"fs": {"command": "new"}}}

    result = diff_configs(local, canonical)
    assert result.status == "outdated"
    assert result.changes[0]["type"] == "modified"
    assert result.changes[0]["semantic"] == "breaking"  # command change
```

5. **Nested Changes:** Deep object modifications
```python
def test_nested_changes_detected():
    local = {"a": {"b": {"c": "old"}}}
    canonical = {"a": {"b": {"c": "new"}}}

    result = diff_configs(local, canonical)
    assert len(result.changes) == 1
    assert result.changes[0]["path"] == "a.b.c"
```

6. **Semantic Classification:** Correct breaking/compatible labels
```python
def test_breaking_change_detected():
    local = {"server": {"command": "old-binary"}}
    canonical = {"server": {"command": "new-binary"}}

    result = diff_configs(local, canonical)
    assert result.status == "outdated"
    assert any(c["semantic"] == "breaking" for c in result.changes)
    assert result.recommendation == "review"

def test_compatible_change_detected():
    local = {"server": {"command": "cmd"}}
    canonical = {"server": {"command": "cmd", "env": {"NEW": "val"}}}

    result = diff_configs(local, canonical)
    assert any(c["semantic"] == "compatible" for c in result.changes)
    assert result.recommendation == "update"
```

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Diff computed
emit_event("diff.computed", status="success",
           metadata={"status": result.status, "change_count": len(result.changes)})

# Breaking change detected
if any(c["semantic"] == "breaking" for c in result.changes):
    emit_event("diff.breaking_change", status="warning",
               metadata={"changes": [c["path"] for c in result.changes if c["semantic"] == "breaking"]})

# Auto-update applied
emit_event("diff.auto_updated", status="success",
           metadata={"strategy": "safe", "changes_applied": count})
```

**Create knowledge notes for:**
- Semantic classification refinements
- Common diff patterns discovered
- Breaking change patterns

**Tag pattern:** `diff`, `config`, `changes`, `[semantic-type]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../storage/AGENTS.md](../storage/AGENTS.md)** - Canonical artifact retrieval
- **[../registry/AGENTS.md](../registry/AGENTS.md)** - Profile lookup (resolves artifact_id)
- **[../mcp/AGENTS.md](../mcp/AGENTS.md)** - diff_config tool (exposes diff via MCP)

---

## Common Errors & Solutions

### Error: "Cannot diff incompatible types"

**Cause:** Local and canonical have different root types

**Solution:**
```python
# Ensure both are dicts
assert isinstance(local_payload, dict)
assert isinstance(canonical_payload, dict)
```

### Error: "Semantic classification failed"

**Cause:** Unexpected field type or structure

**Solution:**
```python
# Add custom semantic rules
from mcp_orchestrator.diff.semantic import register_semantic_rule

def custom_rule(change):
    if "custom_field" in change["path"]:
        return "cosmetic"
    return None  # Fallback to default rules

register_semantic_rule(custom_rule)
```

### Error: "Diff too large"

**Cause:** Configs vastly different (>1000 changes)

**Solution:**
```python
# Limit diff output
result = diff_configs(local, canonical, max_changes=100)

# Or use summary mode
result = diff_configs(local, canonical, summary_only=True)
# Returns: {"status": "diverged", "change_count": 1523, "changes": []}
```

---

**End of Configuration Diff Engine Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
