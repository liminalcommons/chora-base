# Storage Layer Guide

**Purpose:** Guide for content-addressable storage layer (immutable artifacts).

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **Store artifact:** `storage.save_artifact(artifact)` → returns `artifact_id`
- **Retrieve artifact:** `storage.get_artifact(artifact_id)` → returns `artifact dict`
- **List artifacts:** `storage.list_artifacts(client_id, profile)` → returns `list of metadata`
- **Testing:** `pytest tests/unit/test_storage.py`
- **Verify integrity:** `storage.verify_storage_integrity()`

---

## Architecture

**Path:** `src/mcp_orchestrator/storage/`

**Design Pattern:** Content-Addressable Storage (CAS)

**Key Concept:** `artifact_id = SHA-256(payload)`

### Why Content-Addressable?

- **Immutable:** Content cannot change (hash collision prevention)
- **Deduplication:** Same content = same artifact_id (automatic dedup)
- **Verification:** Retrieve by hash, recompute to verify integrity
- **Caching:** Content never changes, cache forever
- **Distribution:** Works in distributed systems (no version conflicts)

**Precedent:** Git, Docker, IPFS, BitTorrent all use content-addressable storage.

### Files

```
storage/
├── __init__.py           # Public API exports
├── backend.py            # Storage backend interface (Protocol)
├── local.py              # Local filesystem storage implementation
└── paths.py              # Path resolution utilities
```

---

## Storage Layout

### Base Path

**Default:** `~/.mcp-orchestration/storage/`

**Custom:** Set `MCP_ORCHESTRATION_STORAGE_PATH` environment variable

### Directory Structure

```
~/.mcp-orchestration/storage/
├── artifacts/                    # Content-addressable artifacts
│   ├── aa/                       # 2-level sharding (first 2 hex chars)
│   │   └── bb/                   # (next 2 hex chars)
│   │       └── aabbccddee...ff.json  # Full SHA-256 as filename
│   ├── 12/
│   │   └── 34/
│   │       └── 1234567890abcdef....json
│   ├── index.json                # Artifact index (metadata)
│   └── manifest.json             # Storage manifest (version, stats)
├── clients/                      # Client-specific links
│   ├── claude-desktop/
│   │   ├── default/
│   │   │   └── current.link → ../../artifacts/aa/bb/aabbcc...ff.json
│   │   ├── development/
│   │   │   └── current.link → ../../artifacts/12/34/123456...ef.json
│   │   └── profiles.json
│   └── cursor/
│       └── ...
└── keys/                         # Cryptographic keys (see crypto/AGENTS.md)
    ├── signing.key               # Ed25519 private key (0600)
    └── signing.pub               # Ed25519 public key (0644)
```

### Why 2-Level Directory Sharding (aa/bb/)?

**Problem:** Filesystem limits on files per directory
- **ext4:** ~10M files/dir (performance degrades)
- **NTFS:** ~4M files/dir
- **HFS+:** ~2 million files/dir

**Solution:** Shard by first 4 hex chars (aa/bb/)
- **aa/:** 256 subdirectories (00-ff)
- **aa/bb/:** 256 subdirectories each = 65,536 total leaf dirs
- **Capacity:** Billions of artifacts with good performance

**Precedent:** Git uses `.git/objects/ab/cdef...`, Docker uses similar sharding.

---

## Content-Addressable Storage API

### Save Artifact

```python
from mcp_orchestrator.storage import save_artifact
import hashlib
import json

artifact = {
    "client_id": "claude-desktop",
    "profile": "default",
    "payload": {
        "mcpServers": {
            "filesystem": {
                "command": "mcp-filesystem",
                "args": ["--root", "/workspace"]
            }
        }
    },
    "metadata": {
        "created_at": "2025-10-24T12:00:00Z",
        "version": "1.0"
    }
}

# Computes SHA-256(payload), stores at artifacts/aa/bb/aabbcc...ff.json
artifact_id = save_artifact(artifact)

# Returns: "aabbccddee...ff" (SHA-256 hash)
# File written to: ~/.mcp-orchestration/storage/artifacts/aa/bb/aabbccddee...ff.json
```

### Retrieve Artifact

```python
from mcp_orchestrator.storage import get_artifact

artifact = get_artifact("aabbccddee...ff")

# Returns: Full artifact dict
# {
#   "artifact_id": "aabbccddee...ff",
#   "client_id": "claude-desktop",
#   "profile": "default",
#   "payload": {...},
#   "metadata": {...},
#   "signature": {...}  # If signed
# }

# Verifies: Recomputes SHA-256(payload), checks integrity
```

### List Artifacts

```python
from mcp_orchestrator.storage import list_artifacts

# List all artifacts
all_artifacts = list_artifacts()

# Filter by client
claude_artifacts = list_artifacts(client_id="claude-desktop")

# Filter by client + profile
default_artifacts = list_artifacts(
    client_id="claude-desktop",
    profile="default"
)

# Returns: List of artifact metadata
# [
#   {
#     "artifact_id": "aabbccddee...",
#     "client_id": "claude-desktop",
#     "profile": "default",
#     "created_at": "2025-10-24T12:00:00Z",
#     "size_bytes": 1024
#   },
#   ...
# ]
```

---

## Immutability Guarantees

### CRITICAL RULE: Storage is Immutable

**Never modify artifacts after saving.**

### Why Immutable?

1. **Content hash breaks:** `artifact_id = SHA-256(payload)`. Modify payload → hash no longer matches.
2. **Caching:** Content never changes, safe to cache forever.
3. **Distributed systems:** No version conflicts (content is identity).
4. **Cryptographic verification:** Hash = identity, signatures verify content.

### To Update Config

❌ **DON'T:**
```python
# BAD: Modifying existing artifact
artifact = get_artifact("aabbccddee...")
artifact["payload"]["new_field"] = "value"  # ❌ Breaks immutability
# artifact_id no longer matches SHA-256(payload)
```

✅ **DO:**
```python
# GOOD: Create new artifact
old_artifact = get_artifact("aabbccddee...")

# Create new artifact with updated payload
new_artifact = {
    "client_id": old_artifact["client_id"],
    "profile": old_artifact["profile"],
    "payload": {
        **old_artifact["payload"],
        "new_field": "value"  # Added field
    },
    "metadata": {
        "created_at": "2025-10-24T13:00:00Z",
        "version": "1.1",
        "previous_artifact_id": old_artifact["artifact_id"]  # Track history
    }
}

# Save creates NEW artifact with NEW artifact_id
new_artifact_id = save_artifact(new_artifact)

# Update profile pointer
update_profile_artifact(
    client_id="claude-desktop",
    profile="default",
    artifact_id=new_artifact_id  # Point to new artifact
)

# Old artifact remains (for diff, rollback, history)
```

---

## Migration & Versioning

### Storage Version

**Tracked in:** `~/.mcp-orchestration/storage/manifest.json`

```json
{
  "version": "1.0",
  "created_at": "2025-10-24T12:00:00Z",
  "updated_at": "2025-10-24T12:00:00Z",
  "stats": {
    "total_artifacts": 15,
    "total_size_bytes": 524288,
    "clients": ["claude-desktop", "cursor"]
  }
}
```

### Migration Pattern

**When:** Storage format changes (rare, breaking change).

**Process:**
1. Detect version mismatch (check `manifest.json`)
2. Run migration script (`storage/migrations/v1_to_v2.py`)
3. Update manifest version
4. Validate migrated data

```python
from mcp_orchestrator.storage.migrations import migrate

# Automatic migration
migrate(from_version="1.0", to_version="2.0")

# Manual migration
from mcp_orchestrator.storage.migrations.v1_to_v2 import migrate_v1_to_v2
migrate_v1_to_v2()
```

### Backward Compatibility

- **Old artifact format:** Remains readable (no breaking changes)
- **New features:** Use new optional fields (additive changes only)
- **Breaking changes:** Require major version bump + migration

---

## Testing Storage Operations

**Coverage Target:** ≥85% (≥95% for integrity checks)

### Test Categories

1. **Save/Retrieve:** Round-trip correctness
```python
def test_save_retrieve_round_trip():
    artifact = {"payload": "test data"}
    artifact_id = save_artifact(artifact)

    retrieved = get_artifact(artifact_id)
    assert retrieved["payload"] == "test data"
```

2. **Deduplication:** Same content = same artifact_id
```python
def test_content_addressable_deduplication():
    artifact_1 = {"payload": "identical content"}
    artifact_2 = {"payload": "identical content"}

    id_1 = save_artifact(artifact_1)
    id_2 = save_artifact(artifact_2)

    # Same content = same artifact_id
    assert id_1 == id_2

    # Only one file written (deduplication)
    artifacts = list_artifacts()
    assert len([a for a in artifacts if a["payload"] == "identical content"]) == 1
```

3. **Integrity:** Tampered artifacts rejected
```python
def test_tampered_artifact_detected():
    artifact = {"payload": "original"}
    artifact_id = save_artifact(artifact)

    # Manually tamper with file on disk
    artifact_path = resolve_artifact_path(artifact_id)
    with open(artifact_path, 'w') as f:
        json.dump({"payload": "tampered"}, f)

    # Retrieval should detect tampering (hash mismatch)
    with pytest.raises(IntegrityError):
        get_artifact(artifact_id)
```

4. **Concurrency:** Parallel writes/reads safe
```python
import concurrent.futures

def test_concurrent_writes_safe():
    def save_unique_artifact(i):
        return save_artifact({"payload": f"artifact-{i}"})

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(save_unique_artifact, i) for i in range(100)]
        artifact_ids = [f.result() for f in futures]

    # All writes successful, no corruption
    assert len(set(artifact_ids)) == 100  # All unique
    for aid in artifact_ids:
        assert get_artifact(aid) is not None
```

5. **Migration:** Version upgrades work correctly
```python
def test_storage_migration_v1_to_v2():
    # Create v1 storage
    create_v1_storage()

    # Run migration
    migrate(from_version="1.0", to_version="2.0")

    # Verify v2 format
    manifest = load_manifest()
    assert manifest["version"] == "2.0"

    # Old artifacts still readable
    old_artifact = get_artifact("old-artifact-id")
    assert old_artifact is not None
```

---

## Common Tasks

### Clear Storage (Development Only)

⚠️ **WARNING:** Deletes all artifacts. Cannot be undone.

```bash
# Remove all artifacts
rm -rf ~/.mcp-orchestration/storage/artifacts/*

# Or via API
python -c "
from mcp_orchestrator.storage import clear_storage
clear_storage(confirm=True)  # Requires explicit confirmation
"
```

### Verify Storage Integrity

```python
from mcp_orchestrator.storage import verify_storage_integrity

issues = verify_storage_integrity()

# Checks:
# 1. All artifact_ids match SHA-256(content)
# 2. No orphaned files (files without index entries)
# 3. Manifest consistent with filesystem
# 4. Symlinks valid (profile pointers)

if issues:
    for issue in issues:
        print(f"Integrity issue: {issue}")
else:
    print("Storage integrity verified ✓")
```

### Migrate Storage

```python
from mcp_orchestrator.storage.migrations import migrate

# Check current version
current_version = get_storage_version()
print(f"Current version: {current_version}")

# Migrate to latest
migrate(to_version="latest")

# Or specific version
migrate(from_version="1.0", to_version="2.0")
```

### Export/Import Artifacts

```python
from mcp_orchestrator.storage import export_artifacts, import_artifacts

# Export to archive
export_artifacts(
    output_file="/backup/artifacts-2025-10-24.tar.gz",
    client_id="claude-desktop",  # Optional filter
    profile="default"            # Optional filter
)

# Import from archive
import_artifacts(
    input_file="/backup/artifacts-2025-10-24.tar.gz",
    overwrite=False  # Skip duplicates
)
```

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Artifact saved
emit_event("storage.artifact_saved", status="success",
           metadata={"artifact_id": artifact_id, "size_bytes": size})

# Artifact retrieved
emit_event("storage.artifact_retrieved", status="success",
           metadata={"artifact_id": artifact_id})

# Integrity check failed
emit_event("storage.integrity_error", status="failure",
           metadata={"artifact_id": artifact_id, "error": "hash_mismatch"})

# Migration completed
emit_event("storage.migrated", status="success",
           metadata={"from_version": "1.0", "to_version": "2.0"})
```

**Create knowledge notes for:**
- Storage optimization techniques
- Migration strategies
- Integrity issue resolutions
- Performance tuning (sharding, caching)

**Tag pattern:** `storage`, `artifacts`, `cas`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../crypto/AGENTS.md](../crypto/AGENTS.md)** - Signature verification (uses artifact_id hashing)
- **[../registry/AGENTS.md](../registry/AGENTS.md)** - Artifact lookup (resolves artifact_id from profile)

---

## Common Errors & Solutions

### Error: "Artifact not found"

**Cause:** `artifact_id` doesn't exist in storage

**Solution:**
```python
# Check artifact_id spelling
print(f"Looking for: {artifact_id}")

# List all artifacts
artifacts = list_artifacts()
print(f"Available: {[a['artifact_id'] for a in artifacts]}")

# Ensure artifact was saved
artifact_id = save_artifact(artifact)
print(f"Saved with ID: {artifact_id}")
```

### Error: "Hash mismatch" / "Integrity check failed"

**Cause:** Artifact content modified on disk

**Solution:**
```python
# Storage corruption detected, restore from backup
import shutil

# Backup corrupted artifact
corrupted_path = resolve_artifact_path(artifact_id)
shutil.move(corrupted_path, f"{corrupted_path}.corrupted")

# Restore from backup or re-sign original
# ...
```

### Error: "Permission denied"

**Cause:** `~/.mcp-orchestration/` not writable

**Solution:**
```bash
# Check directory permissions
ls -la ~/.mcp-orchestration/

# Create if missing
mkdir -p ~/.mcp-orchestration/storage/artifacts

# Fix permissions
chmod 755 ~/.mcp-orchestration/
chmod 755 ~/.mcp-orchestration/storage/
```

### Error: "Disk full"

**Cause:** Storage directory out of space

**Solution:**
```bash
# Check disk usage
du -sh ~/.mcp-orchestration/storage/

# List largest artifacts
python -c "
from mcp_orchestrator.storage import list_artifacts
artifacts = sorted(list_artifacts(), key=lambda a: a['size_bytes'], reverse=True)
for a in artifacts[:10]:
    print(f\"{a['artifact_id']}: {a['size_bytes'] / 1024 / 1024:.2f} MB\")
"

# Archive old artifacts
# (See "Export/Import Artifacts" section)
```

---

**End of Storage Layer Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
