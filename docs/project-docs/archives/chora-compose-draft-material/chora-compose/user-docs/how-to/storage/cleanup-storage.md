# How to Clean Up Ephemeral Storage

**Goal**: Learn manual and automated cleanup procedures, implement retention policies, manage storage size, and follow best practices for storage maintenance.

**Time**: 15-20 minutes

**Prerequisites**:
- Chora Compose installed
- Understanding of [ephemeral storage](manage-ephemeral-storage.md)
- Understanding of [versioning](understand-versioning.md)

---

## Overview

Ephemeral storage accumulates versions over time. Without cleanup, storage grows unbounded. This guide covers:

- **Manual cleanup** (on-demand deletion)
- **Automated cleanup** (retention policies)
- **Storage size management** (monitoring and limits)
- **Best practices** (what to keep, what to delete)

**Default retention**: 30 days (configurable)

---

## Quick Reference

| Task | Command | When to Use |
|------|---------|-------------|
| Manual cleanup (all old) | `cleanup(content_id)` | One-time cleanup |
| Auto-cleanup on save | `auto_cleanup=True` | Automatic maintenance |
| Delete specific content | `delete(content_id)` | Remove content entirely |
| Check storage size | `get_storage_size()` | Monitor disk usage |
| Set retention policy | `retention_days=N` | Configure how long to keep |

---

## Manual Cleanup Procedures

### Cleanup Single Content Item

```python
from chora_compose.storage.ephemeral import EphemeralStorageManager

storage = EphemeralStorageManager(retention_days=30)

# Clean up old versions (keeps versions < 30 days old)
result = storage.cleanup("api-docs")

print(f"Files removed: {result.files_removed}")
print(f"Versions removed: {result.versions_removed}")
print(f"Space freed: {result.space_freed / 1024:.2f} KB")
```

**What it does**:
- Deletes versions older than `retention_days`
- Keeps recent versions
- Returns cleanup statistics

### Cleanup All Content

```python
def cleanup_all(storage):
    """Clean up all content in storage."""
    total_files = 0
    total_space = 0

    for content_id in storage.list_content():
        result = storage.cleanup(content_id)
        total_files += result.files_removed
        total_space += result.space_freed

    print(f"Total cleanup:")
    print(f"  Files removed: {total_files}")
    print(f"  Space freed: {total_space / 1024 / 1024:.2f} MB")

# Usage
cleanup_all(storage)
```

### Delete Entire Content Item

```python
# Delete all versions of content
storage.delete("api-docs")

print("✅ Deleted all versions of api-docs")
```

**Warning**: This is permanent! Use with caution.

---

## Automated Cleanup Strategies

### Strategy 1: Auto-Cleanup on Save

```python
# Enable auto-cleanup
storage = EphemeralStorageManager(
    retention_days=30,
    auto_cleanup=True  # Cleanup after every save
)

# Save triggers automatic cleanup
storage.save("api-docs", content="# API Docs v1.0", format="md")
# Old versions automatically deleted
```

**Pros**:
- ✅ Automatic (no manual intervention)
- ✅ Storage stays bounded
- ✅ Simple to enable

**Cons**:
- ❌ Slight overhead on each save (~5-10ms)
- ❌ Not customizable (uses retention_days)

**When to use**: Most production deployments

### Strategy 2: Scheduled Cleanup (Cron)

```bash
# Add to crontab (daily at 2 AM)
0 2 * * * cd /path/to/chora-compose && python -m chora_compose.cli cleanup-storage
```

**Python script** (`cleanup_script.py`):
```python
#!/usr/bin/env python3
"""Scheduled cleanup script."""

from chora_compose.storage.ephemeral import EphemeralStorageManager

def main():
    storage = EphemeralStorageManager(retention_days=30)

    total_freed = 0
    for content_id in storage.list_content():
        result = storage.cleanup(content_id)
        total_freed += result.space_freed

    print(f"Cleanup complete: {total_freed / 1024 / 1024:.2f} MB freed")

if __name__ == "__main__":
    main()
```

**Pros**:
- ✅ No overhead on save operations
- ✅ Runs during off-peak hours
- ✅ Centralized (one cleanup job for all content)

**Cons**:
- ❌ Requires cron/scheduler setup
- ❌ Storage can grow between cleanups

**When to use**: Large deployments, scheduled maintenance windows

### Strategy 3: Event-Driven Cleanup

```python
# Cleanup triggered by storage size threshold
def check_and_cleanup(storage, max_size_mb=100):
    """Cleanup if storage exceeds threshold."""
    current_size = get_storage_size(storage.base_path)
    current_size_mb = current_size / 1024 / 1024

    if current_size_mb > max_size_mb:
        print(f"⚠️ Storage at {current_size_mb:.2f} MB (limit: {max_size_mb} MB)")
        print("Running cleanup...")

        for content_id in storage.list_content():
            storage.cleanup(content_id)

        new_size = get_storage_size(storage.base_path) / 1024 / 1024
        print(f"✅ Cleaned up: {current_size_mb - new_size:.2f} MB freed")

# Check before/after operations
check_and_cleanup(storage, max_size_mb=100)
```

**Pros**:
- ✅ Reactive (cleanup only when needed)
- ✅ Prevents storage exhaustion
- ✅ Customizable thresholds

**Cons**:
- ❌ Requires monitoring
- ❌ Cleanup during operation (may impact performance)

**When to use**: Strict storage limits, unpredictable usage patterns

---

## Retention Policies

### Policy 1: Time-Based (Default)

```python
# Keep versions for 30 days
storage = EphemeralStorageManager(retention_days=30)
```

**Use case**: General-purpose retention

### Policy 2: Keep N Latest Versions

```python
def cleanup_keep_n(storage, content_id, keep_n=5):
    """Keep only N latest versions."""
    versions = storage.list_versions(content_id)

    if len(versions) <= keep_n:
        return  # Nothing to cleanup

    # Delete all except last N
    to_delete = versions[:-keep_n]

    for version in to_delete:
        version.file_path.unlink()
        meta_file = version.file_path.with_suffix(".meta.json")
        if meta_file.exists():
            meta_file.unlink()

    print(f"Kept {keep_n} versions, deleted {len(to_delete)}")

# Usage
cleanup_keep_n(storage, "api-docs", keep_n=5)
```

**Use case**: Limit version count (e.g., only keep 5 most recent)

### Policy 3: Hybrid (Time + Count)

```python
def cleanup_hybrid(storage, content_id, min_keep=3, max_age_days=30):
    """Keep min_keep versions OR versions newer than max_age_days."""
    from datetime import datetime, timedelta, timezone

    versions = storage.list_versions(content_id)
    if len(versions) <= min_keep:
        return  # Keep minimum count

    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    to_delete = []

    # Always keep at least min_keep versions
    for version in versions[:-min_keep]:
        if version.timestamp_dt < cutoff:
            to_delete.append(version)

    for version in to_delete:
        version.file_path.unlink()
        meta_file = version.file_path.with_suffix(".meta.json")
        if meta_file.exists():
            meta_file.unlink()

    print(f"Deleted {len(to_delete)} old versions (kept {len(versions) - len(to_delete)})")

# Usage
cleanup_hybrid(storage, "api-docs", min_keep=3, max_age_days=30)
```

**Use case**: Balance between history and storage (keep recent, but not too many)

---

## Storage Size Management

### Monitor Storage Size

```python
def get_storage_size(path):
    """Calculate total storage size."""
    total = 0
    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total

# Usage
size_bytes = get_storage_size(storage.base_path)
print(f"Storage size: {size_bytes / 1024 / 1024:.2f} MB")
```

### Storage Report

```python
def storage_report(storage):
    """Generate detailed storage report."""
    report = {
        "content_count": 0,
        "version_count": 0,
        "total_size": 0,
        "items": []
    }

    for content_id in storage.list_content():
        versions = storage.list_versions(content_id)
        item_size = sum(
            version.file_path.stat().st_size
            for version in versions
            if version.file_path.exists()
        )

        report["content_count"] += 1
        report["version_count"] += len(versions)
        report["total_size"] += item_size

        report["items"].append({
            "content_id": content_id,
            "versions": len(versions),
            "size_mb": item_size / 1024 / 1024
        })

    # Sort by size
    report["items"].sort(key=lambda x: x["size_mb"], reverse=True)

    return report

# Usage
report = storage_report(storage)
print(f"Total: {report['total_size'] / 1024 / 1024:.2f} MB")
print(f"Items: {report['content_count']}")
print(f"Versions: {report['version_count']}")
print("\nTop 5 by size:")
for item in report["items"][:5]:
    print(f"  {item['content_id']}: {item['size_mb']:.2f} MB ({item['versions']} versions)")
```

### Set Storage Limits

```python
class StorageQuotaExceeded(Exception):
    """Raised when storage quota exceeded."""
    pass

def save_with_quota(storage, content_id, content, quota_mb=100):
    """Save with storage quota enforcement."""
    current_size = get_storage_size(storage.base_path) / 1024 / 1024

    if current_size >= quota_mb:
        raise StorageQuotaExceeded(
            f"Storage quota exceeded: {current_size:.2f} MB / {quota_mb} MB"
        )

    return storage.save(content_id, content)

# Usage
try:
    save_with_quota(storage, "api-docs", content, quota_mb=100)
except StorageQuotaExceeded as e:
    print(f"❌ {e}")
    # Trigger cleanup or alert admin
```

---

## Best Practices

### What to Keep

✅ **Keep**:
- Recent versions (last 7 days)
- Tagged releases (semantic versions)
- Versions with important metadata (git commits, CI builds)
- Minimum count (e.g., always keep last 3 versions)

### What to Delete

❌ **Delete**:
- Versions older than retention period (default 30 days)
- Duplicate content (same hash)
- Orphaned metadata files
- Temporary/draft versions

### Cleanup Schedule

**Recommended**:
1. **Auto-cleanup on save** (production)
2. **Daily cron job** (additional safety net)
3. **Weekly manual review** (check for anomalies)

### Example Production Setup

```python
# Production storage configuration
storage = EphemeralStorageManager(
    base_path="/var/chora-compose/ephemeral",
    retention_days=30,
    auto_cleanup=True
)

# Monitoring
def monitor_storage():
    """Check storage health."""
    size_mb = get_storage_size(storage.base_path) / 1024 / 1024

    if size_mb > 500:  # Alert threshold
        print(f"⚠️ Storage high: {size_mb:.2f} MB")
        # Send alert

    if size_mb > 1000:  # Critical threshold
        print(f"🚨 Storage critical: {size_mb:.2f} MB")
        # Aggressive cleanup
        for content_id in storage.list_content():
            storage.cleanup(content_id)

# Run daily via cron
monitor_storage()
```

---

## Troubleshooting

### Issue: Storage Growing Despite Cleanup

**Symptom**: Disk usage increasing even with auto-cleanup enabled

**Causes**:
1. Retention period too long
2. Many new content items created
3. Large individual files

**Fixes**:
```python
# Reduce retention
storage = EphemeralStorageManager(retention_days=7)  # Was 30

# Limit versions per item
cleanup_keep_n(storage, "api-docs", keep_n=3)  # Keep only 3

# Check for large files
report = storage_report(storage)
# Investigate items with size_mb > 10
```

### Issue: Deleted Content Still Exists

**Symptom**: Called `cleanup()` but files still present

**Cause**: Versions within retention period

**Fix**:
```python
# Check retention period
print(f"Retention: {storage.retention_days} days")

# Force delete all versions
storage.delete("api-docs")  # Complete removal
```

---

## Summary

**Cleanup strategies**:
1. **Auto-cleanup**: Enable `auto_cleanup=True` (recommended for production)
2. **Scheduled**: Daily cron job for comprehensive cleanup
3. **Event-driven**: Cleanup when storage threshold exceeded

**Retention policies**:
- **Time-based**: Keep versions < N days (default 30)
- **Count-based**: Keep last N versions
- **Hybrid**: Combine time + count

**Monitoring**:
- Check storage size regularly
- Generate reports (top items by size)
- Set quotas and alerts

**Best practices**:
- Keep recent versions (7 days minimum)
- Delete old versions (30 days default)
- Monitor storage growth
- Automate cleanup (cron or auto-cleanup)

---

## Related Documentation

- [Manage Ephemeral Storage](manage-ephemeral-storage.md) - Storage basics
- [Understand Versioning](understand-versioning.md) - Version management
- [List and Retrieve Content](list-retrieve-content.md) - Content access

---

**Last Updated**: 2025-10-21 | **Sprint**: 4 - Storage Documentation
