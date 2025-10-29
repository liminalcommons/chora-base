# How to Understand Versioning in Ephemeral Storage

**Goal**: Understand how versioning works in ephemeral storage, retrieve specific versions, inspect version history, and manage old versions.

**Time**: 15-20 minutes

**Prerequisites**:
- Chora Compose installed
- Basic understanding of [ephemeral storage](manage-ephemeral-storage.md)
- Familiarity with timestamps

---

## Overview

Ephemeral storage in chora-compose automatically **versions every save operation**. Each time you save content, a new version is created with a unique timestamp. This enables:

- **Version history** (see all versions)
- **Time-travel** (retrieve content from specific points in time)
- **Audit trails** (track when content was generated)
- **Rollback** (revert to previous versions)

**Key insight**: Versioning is **automatic** — you don't need to do anything special. Every save creates a new version.

---

## How Versioning Works

### Automatic Timestamp-Based Versioning

**Every save** creates a timestamped version:

```python
from chora_compose.storage.ephemeral import EphemeralStorageManager

storage = EphemeralStorageManager()

# Save #1 (creates version with timestamp)
version1 = storage.save(
    content_id="api-docs",
    content="# API Documentation v1.0",
    format="md"
)
print(version1.timestamp)  # 2025-10-21T10:30:00.123456+00:00

# Save #2 (creates new version with different timestamp)
version2 = storage.save(
    content_id="api-docs",  # Same content_id
    content="# API Documentation v1.1",  # Updated content
    format="md"
)
print(version2.timestamp)  # 2025-10-21T10:35:00.789012+00:00
```

**Result**:
```
ephemeral/api-docs/
├── 2025-10-21T10-30-00-123456+00-00.md  ← Version 1
├── 2025-10-21T10-30-00-123456+00-00.meta.json
├── 2025-10-21T10-35-00-789012+00-00.md  ← Version 2 (latest)
└── 2025-10-21T10-35-00-789012+00-00.meta.json
```

**Key points**:
- Each version has unique timestamp (ISO 8601 format with microseconds)
- Filename = timestamp (safe format: colons → dashes)
- Metadata file (`.meta.json`) stores version info
- Latest version = most recent timestamp

---

## Retrieving Versions

### Strategy 1: Latest Version (Default)

**Use case**: Get the most recent content

```python
# Retrieve latest version
content = storage.retrieve("api-docs", strategy="latest")
print(content)  # "# API Documentation v1.1"
```

**When to use**: 99% of the time (you usually want the latest)

### Strategy 2: All Versions

**Use case**: See version history

```python
# Retrieve all versions
all_versions = storage.retrieve("api-docs", strategy="all")

for i, content in enumerate(all_versions, 1):
    print(f"Version {i}: {content[:50]}...")
# Version 1: # API Documentation v1.0...
# Version 2: # API Documentation v1.1...
```

**When to use**: Auditing, comparing changes across versions

### Strategy 3: Specific Timestamp

**Use case**: Retrieve content from exact time

```python
# Retrieve from specific timestamp
content = storage.retrieve("api-docs", strategy="timestamp:2025-10-21T10:30")
print(content)  # "# API Documentation v1.0"
```

**Format**: `timestamp:YYYY-MM-DDTHH:MM` (partial matches work)

**When to use**: Rollback to specific point in time

### Strategy 4: Semantic Version (Metadata-Based)

**Use case**: Retrieve by semantic version number

```python
# Save with semantic version metadata
storage.save(
    content_id="api-docs",
    content="# API Documentation v2.0",
    format="md",
    metadata={"version": "2.0.0"}  # Semantic version
)

# Retrieve by semantic version
content = storage.retrieve("api-docs", strategy="version:2.0.0")
print(content)  # "# API Documentation v2.0"
```

**When to use**: Managing releases with semantic versioning

---

## Listing Versions

### Get Version List

```python
# List all versions for content
versions = storage.list_versions("api-docs")

for v in versions:
    print(f"Timestamp: {v.timestamp}")
    print(f"File: {v.file_path}")
    print(f"Size: {v.metadata.get('size', 'N/A')} bytes")
    print(f"Metadata: {v.metadata}")
    print()
```

**Output**:
```
Timestamp: 2025-10-21T10:30:00.123456+00:00
File: ephemeral/api-docs/2025-10-21T10-30-00-123456+00-00.md
Size: 28 bytes
Metadata: {'content_id': 'api-docs', 'timestamp': '2025-10-21T10:30:00.123456+00:00', 'format': 'md', 'size': 28}

Timestamp: 2025-10-21T10:35:00.789012+00:00
File: ephemeral/api-docs/2025-10-21T10-35-00-789012+00-00.md
Size: 28 bytes
Metadata: {'content_id': 'api-docs', 'timestamp': '2025-10-21T10:35:00.789012+00:00', 'format': 'md', 'size': 28}
```

### Filter Versions by Date Range

```python
from datetime import datetime, timezone

# Get versions from specific date
versions = storage.list_versions("api-docs")

# Filter: only versions from Oct 21, 2025
oct_21_versions = [
    v for v in versions
    if v.timestamp_dt.date() == datetime(2025, 10, 21, tzinfo=timezone.utc).date()
]

print(f"Versions on Oct 21: {len(oct_21_versions)}")
```

**Use case**: Audit trail for specific day

---

## Version History and Comparison

### Compare Two Versions

```python
# Get all versions
all_versions = storage.retrieve("api-docs", strategy="all")

# Compare first and last
if len(all_versions) >= 2:
    first = all_versions[0]
    last = all_versions[-1]

    print("First version:")
    print(first)
    print("\nLatest version:")
    print(last)

    # Simple diff
    if first != last:
        print("\n⚠️ Content has changed")
    else:
        print("\n✅ Content unchanged")
```

### Advanced: Diff with `difflib`

```python
import difflib

# Get two versions
v1_content = storage.retrieve("api-docs", strategy="timestamp:2025-10-21T10:30")
v2_content = storage.retrieve("api-docs", strategy="timestamp:2025-10-21T10:35")

# Generate unified diff
diff = difflib.unified_diff(
    v1_content.splitlines(keepends=True),
    v2_content.splitlines(keepends=True),
    fromfile="v1.0",
    tofile="v1.1",
    lineterm=""
)

print("".join(diff))
```

**Output**:
```diff
--- v1.0
+++ v1.1
@@ -1 +1 @@
-# API Documentation v1.0
+# API Documentation v1.1
```

**Use case**: See exactly what changed between versions

---

## Metadata Storage

### What's in Metadata?

Each version has a `.meta.json` file:

```json
{
  "content_id": "api-docs",
  "timestamp": "2025-10-21T10:30:00.123456+00:00",
  "format": "md",
  "size": 28,
  "version": "1.0.0",
  "generator": "jinja2",
  "context_hash": "abc123"
}
```

**Default metadata** (automatic):
- `content_id`: Identifier
- `timestamp`: When saved
- `format`: File extension
- `size`: Content size in bytes

**Custom metadata** (you provide):
- `version`: Semantic version
- `generator`: Which generator created this
- `context_hash`: Hash of generation context
- Any other key-value pairs

### Adding Custom Metadata

```python
# Save with rich metadata
storage.save(
    content_id="api-docs",
    content="# API Documentation v1.0",
    format="md",
    metadata={
        "version": "1.0.0",
        "generator": "jinja2",
        "author": "CI/CD Pipeline",
        "git_commit": "abc123def456",
        "context_hash": "md5:abc123"
    }
)

# Retrieve and inspect
versions = storage.list_versions("api-docs")
latest = versions[-1]
print(f"Generated by: {latest.metadata.get('generator')}")
print(f"Git commit: {latest.metadata.get('git_commit')}")
```

**Use case**: Track provenance (who/what/when/how generated)

---

## Rollback to Previous Version

### Scenario: Accidentally Generated Bad Content

```python
# Accidentally generate bad content
storage.save("api-docs", content="# BROKEN API DOCS (DELETE THIS)")

# Oops! Need to roll back

# Step 1: List versions
versions = storage.list_versions("api-docs")

# Step 2: Find good version (second-to-last)
good_version = versions[-2]  # -1 is bad, -2 is last good

# Step 3: Read good content
with open(good_version.file_path) as f:
    good_content = f.read()

# Step 4: Re-save as latest
storage.save("api-docs", content=good_content, format="md")

print("✅ Rolled back to good version")
```

**Alternative**: Use timestamp strategy

```python
# Get timestamp of last good version
versions = storage.list_versions("api-docs")
last_good_timestamp = versions[-2].timestamp

# Retrieve that version
good_content = storage.retrieve("api-docs", strategy=f"timestamp:{last_good_timestamp[:19]}")

# Re-save
storage.save("api-docs", content=good_content, format="md")
```

---

## Cleanup Strategies

### Strategy 1: Keep Only N Latest Versions

```python
def keep_n_latest(storage, content_id, n=5):
    """Keep only N latest versions, delete rest."""
    versions = storage.list_versions(content_id)

    if len(versions) <= n:
        print(f"Only {len(versions)} versions, nothing to clean")
        return

    # Versions to delete (all except last N)
    to_delete = versions[:-n]

    for version in to_delete:
        version.file_path.unlink()  # Delete content file
        meta_file = version.file_path.with_suffix(".meta.json")
        if meta_file.exists():
            meta_file.unlink()  # Delete metadata

    print(f"Deleted {len(to_delete)} old versions")

# Usage
keep_n_latest(storage, "api-docs", n=5)
```

### Strategy 2: Delete Versions Older Than N Days

```python
from datetime import datetime, timedelta, timezone

def delete_old_versions(storage, content_id, days=30):
    """Delete versions older than N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    versions = storage.list_versions(content_id)
    deleted = 0

    for version in versions:
        if version.timestamp_dt < cutoff:
            version.file_path.unlink()
            meta_file = version.file_path.with_suffix(".meta.json")
            if meta_file.exists():
                meta_file.unlink()
            deleted += 1

    print(f"Deleted {deleted} versions older than {days} days")

# Usage
delete_old_versions(storage, "api-docs", days=30)
```

**Note**: Chora Compose has built-in retention policy (default 30 days). See [cleanup-storage.md](cleanup-storage.md) for details.

---

## Advanced: Migration Between Versions

### Scenario: Schema Change (v1 → v2)

```python
# Migrate all v1 content to v2 format
def migrate_v1_to_v2(storage, content_id):
    """Migrate content from v1 to v2 schema."""
    versions = storage.list_versions(content_id)

    for version in versions:
        # Check if already v2
        if version.metadata.get("schema_version") == "v2":
            continue  # Skip, already migrated

        # Read v1 content
        with open(version.file_path) as f:
            v1_content = f.read()

        # Transform v1 → v2 (example: add header)
        v2_content = f"<!-- Schema v2 -->\n{v1_content}"

        # Save as new version
        storage.save(
            content_id,
            v2_content,
            format=version.format,
            metadata={"schema_version": "v2", "migrated_from": version.timestamp}
        )

    print(f"Migrated {content_id} to schema v2")

# Usage
migrate_v1_to_v2(storage, "api-docs")
```

---

## Best Practices

### Do ✅

1. **Use semantic versioning in metadata**
   ```python
   storage.save("api-docs", content, metadata={"version": "1.2.3"})
   ```

2. **Add context hash for cache invalidation**
   ```python
   import hashlib
   context_hash = hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()
   storage.save("api-docs", content, metadata={"context_hash": context_hash})
   ```

3. **Track generator for debugging**
   ```python
   storage.save("api-docs", content, metadata={"generator": "jinja2"})
   ```

4. **Use timestamp strategy for rollback**
   ```python
   # Rollback to 1 hour ago
   content = storage.retrieve("api-docs", strategy="timestamp:2025-10-21T09:30")
   ```

### Don't ❌

1. **Don't delete `.meta.json` files manually**
   ```python
   # ❌ Bad: Orphans metadata
   content_file.unlink()  # Deletes content
   # .meta.json still exists (orphaned)
   ```

2. **Don't rely on file ordering**
   ```python
   # ❌ Bad: File order not guaranteed
   files = list(content_dir.glob("*.md"))
   latest = files[-1]  # May not be latest!

   # ✅ Good: Use list_versions (sorted by timestamp)
   versions = storage.list_versions(content_id)
   latest = versions[-1]
   ```

3. **Don't store large binaries in ephemeral storage**
   ```python
   # ❌ Bad: Ephemeral storage not designed for large files
   storage.save("video", video_bytes, format="mp4")  # 100 MB

   # ✅ Good: Store path reference instead
   storage.save("video", video_path, format="txt")  # 50 bytes
   ```

---

## Troubleshooting

### Issue: "Content not found"

**Symptom**:
```python
storage.retrieve("api-docs")
# FileNotFoundError: Content not found: api-docs
```

**Cause**: Content ID doesn't exist or was cleaned up

**Fix**:
```python
# List all content IDs
from pathlib import Path
content_ids = [d.name for d in storage.base_path.iterdir() if d.is_dir()]
print(f"Available IDs: {content_ids}")
```

### Issue: Too many versions (disk space)

**Symptom**: Disk usage growing unbounded

**Fix**: Enable auto-cleanup
```python
storage = EphemeralStorageManager(retention_days=30, auto_cleanup=True)
# Auto-deletes versions older than 30 days on every save
```

Or manual cleanup:
```python
# Delete old versions manually
storage.cleanup(content_id="api-docs")
```

---

## Summary

**Versioning in ephemeral storage**:
- **Automatic**: Every save creates timestamped version
- **Retrieval strategies**: latest, all, timestamp, version
- **Metadata**: Track provenance, schema versions, context
- **History**: Compare versions, rollback, audit trail
- **Cleanup**: Retention policies, manual cleanup

**Common workflows**:
1. **Normal use**: Retrieve latest (`strategy="latest"`)
2. **Audit**: List all versions, inspect metadata
3. **Rollback**: Find good version, re-save as latest
4. **Cleanup**: Delete old versions (30-day retention)

**Key files**:
- `ephemeral/{content_id}/{timestamp}.{format}` - Content
- `ephemeral/{content_id}/{timestamp}.meta.json` - Metadata

---

## Related Documentation

### How-To
- [Manage Ephemeral Storage](manage-ephemeral-storage.md) - Storage basics
- [List and Retrieve Content](list-retrieve-content.md) - Retrieval operations
- [Clean Up Storage](cleanup-storage.md) - Cleanup strategies

### Reference
- [EphemeralStorageManager API](../../reference/api/storage/ephemeral-storage-manager.md) - API reference

---

**Last Updated**: 2025-10-21 | **Sprint**: 4 - Storage Documentation
