# How-To: Manage Ephemeral Storage

**Goal:** Understand, monitor, and manage ephemeral storage for draft configs and temporary output.

**Prerequisites:**
- Chora Compose v1.1.0+ with ephemeral storage support
- Understanding of [conversational config creation](../configs/create-config-conversationally.md)
- Basic knowledge of storage architecture

**Time:** 15-20 minutes

---

## Overview

**Ephemeral storage** is Chora Compose's temporary storage system for draft configs, test outputs, and experimental content. It provides:

- **Automatic cleanup** - 30-day retention by default
- **Safe experimentation** - Not version controlled, safe to abandon
- **Resource management** - Prevents disk bloat from temporary files
- **Fast iteration** - No manual cleanup between experiments

**Storage Architecture:**
```
ephemeral/
├── drafts/                 # Draft configs (30-day retention)
│   ├── content/
│   │   └── draft_abc123.json
│   └── artifact/
│       └── draft_xyz789.json
├── output/                 # Test generations (30-day retention)
│   └── test-artifact.md
└── .metadata.json          # Retention tracking

configs/                    # Permanent storage (forever)
├── content/
└── artifact/

output/                     # Permanent output (forever)
```

**Key Concepts:**
- **Ephemeral**: Temporary, auto-cleaned, .gitignore'd
- **Permanent**: Forever, git-tracked, manual deletion only
- **Retention**: Time before automatic cleanup (default: 30 days)
- **Cleanup**: Process of removing expired ephemeral files

---

## Quick Reference

### Storage Comparison

| Aspect | Ephemeral Storage | Permanent Storage |
|--------|------------------|------------------|
| **Location** | ephemeral/ | configs/, output/ |
| **Retention** | 30 days (configurable) | Forever |
| **Git Tracking** | ❌ (.gitignore'd) | ✅ (tracked) |
| **Cleanup** | Automatic | Manual only |
| **Use Case** | Drafts, tests, experiments | Production configs, final output |
| **Safety** | Safe to abandon | Requires explicit deletion |

### Cleanup Tools

| Tool | Purpose | Scope | Risk |
|------|---------|-------|------|
| `cleanup_ephemeral` | Remove expired files | Entire ephemeral/ tree | Low (only expired) |
| `delete_content` | Delete specific content | Single file + metadata | Medium (permanent) |

---

## Task 1: Monitor Ephemeral Storage

**Scenario:** Check current ephemeral storage usage and identify what's stored.

### Step 1: Check Storage Status

**Using Claude Desktop:**
```
You: Show me what's in ephemeral storage
```

**What Claude Does:**

Lists all ephemeral content:

```bash
ls -lR ephemeral/
```

**Expected Response:**
```
Claude: 📊 Ephemeral Storage Status

Drafts (ephemeral/drafts/):
├─ content/ (3 drafts)
│  ├─ draft_2025101601_abc123.json (created 2 days ago)
│  ├─ draft_2025101402_def456.json (created 5 days ago)
│  └─ draft_2025100901_ghi789.json (created 10 days ago)
└─ artifact/ (1 draft)
   └─ draft_2025101501_jkl012.json (created 3 days ago)

Test Output (ephemeral/output/):
├─ test-report-2025-10-14.md (created 5 days ago)
└─ test-artifact.md (created 10 days ago)

Total Usage:
- Draft configs: 4 files (12.3 KB)
- Test outputs: 2 files (8.7 KB)
- Total: 6 files (21.0 KB)

Retention Status:
- Expires in < 7 days: 0 files
- Expires in 7-14 days: 1 file
- Expires in 14-21 days: 2 files
- Expires in 21-30 days: 3 files
```

**What You Learned:**
- Visibility into all temporary files
- Age of each draft/output
- Storage usage metrics
- Which files are close to expiration

---

### Step 2: Check Retention Policy

```
You: What's the current retention policy for ephemeral storage?
```

**Expected Response:**
```
Claude: 📋 Ephemeral Storage Retention Policy

Default Retention: 30 days
Custom Retention: Not configured

Configuration Location:
File: ephemeral/.metadata.json (auto-generated)

Policy Details:
- Draft configs (ephemeral/drafts/): 30 days
- Test output (ephemeral/output/): 30 days
- Cleanup schedule: Automatic on server startup + manual via cleanup_ephemeral
- Grace period: None (expires exactly at 30 days)

Expired Files: 0 (next cleanup will remove these)
```

---

## Task 2: Manual Cleanup of Expired Files

**Scenario:** Free up disk space by removing expired ephemeral files.

### Step 1: Preview Cleanup (Safe Check)

```
You: What ephemeral files would be cleaned up right now?
```

**What Claude Does:**

Checks for expired files without deleting:

```python
# Internal logic
current_time = datetime.now()
retention_days = 30

for file in ephemeral_files:
    age_days = (current_time - file.created_time).days
    if age_days > retention_days:
        print(f"Would delete: {file.path} (age: {age_days} days)")
```

**Expected Response:**
```
Claude: 🔍 Cleanup Preview (Dry Run)

Files that would be removed:
❌ ephemeral/drafts/content/draft_2025091501_old123.json
   Age: 32 days (expired 2 days ago)

❌ ephemeral/output/test-old-report.md
   Age: 45 days (expired 15 days ago)

Total: 2 files (3.1 KB) would be removed
Remaining: 4 files (17.9 KB) would be kept

Run cleanup_ephemeral to delete these files.
```

---

### Step 2: Execute Cleanup

```
You: Clean up expired ephemeral files
```

**What Claude Does:**

Calls `cleanup_ephemeral` tool:

```json
{
  "dry_run": false
}
```

**Expected Response:**
```
Claude: ✅ Ephemeral cleanup completed

Removed Files:
❌ ephemeral/drafts/content/draft_2025091501_old123.json (32 days old)
❌ ephemeral/output/test-old-report.md (45 days old)

Summary:
- Deleted: 2 files (3.1 KB freed)
- Kept: 4 files (17.9 KB)
- Errors: 0

Storage Status:
Before: 21.0 KB (6 files)
After: 17.9 KB (4 files)
Freed: 3.1 KB (14.8%)
```

**What You Learned:**
- Manual cleanup on demand
- Safe removal of only expired files
- Storage metrics before/after

---

## Task 3: Delete Specific Content

**Scenario:** Remove a specific generated content file that's no longer needed.

### Step 1: Identify Content to Delete

```
You: List all generated content files
```

**Expected Response:**
```
Claude: 📄 Generated Content Files

Permanent Output (output/):
├─ daily-report-2025-10-16.md (generated today)
├─ api-docs-v2.md (generated 3 days ago)
├─ changelog-v1.1.0.md (generated 5 days ago)
└─ user-guide.md (generated 10 days ago)

Ephemeral Output (ephemeral/output/):
├─ test-report-2025-10-14.md (generated 5 days ago)
└─ test-artifact.md (generated 10 days ago)

Total: 6 files
```

---

### Step 2: Delete Specific File

```
You: Delete api-docs-v2.md from permanent output
```

**What Claude Does:**

Calls `delete_content` tool:

```json
{
  "file_path": "output/api-docs-v2.md"
}
```

**Expected Response:**
```
Claude: ⚠️  About to delete permanent content

File: output/api-docs-v2.md
Size: 4.2 KB
Created: 2025-10-13 14:23:45
Generated by: api-endpoint config

This action is irreversible. Confirm deletion? [yes/no]

[After user confirms "yes"]

✅ Deleted: output/api-docs-v2.md

Cleanup Actions:
- Removed file: output/api-docs-v2.md
- Updated metadata: Removed generation record
- Updated cache: Invalidated cache entry

The content can be regenerated using generate_content with the same config.
```

**Safety Features:**
- Confirmation prompt for permanent files
- Detailed file information before deletion
- Cache invalidation
- Metadata cleanup

---

### Step 3: Delete with Dependencies

**Advanced:** Some outputs are referenced by artifacts.

```
You: Delete user-guide.md
```

**Expected Response (Has Dependencies):**
```
Claude: ⚠️  Dependency Warning

File: output/user-guide.md
Size: 5.8 KB

❌ Cannot delete - File is referenced by:
  - Artifact: "documentation-bundle" (artifact-docs.json)
  - Artifact: "onboarding-kit" (artifact-onboarding.json)

Options:
1. Delete artifacts first, then this file
2. Remove this file from artifact dependencies
3. Cancel deletion

What would you like to do?
```

**What You Learned:**
- Dependency tracking prevents broken artifacts
- Safe deletion workflow
- Multiple resolution options

---

## Task 4: Configure Retention Policy

**Scenario:** Change retention period from 30 days to 14 days for faster cleanup.

### Step 1: Check Current Configuration

```
You: Show current retention configuration
```

**Expected Response:**
```
Claude: 📋 Current Retention Configuration

Location: ephemeral/.metadata.json

Current Settings:
{
  "retention_days": 30,
  "last_cleanup": "2025-10-15T10:23:45Z",
  "cleanup_on_startup": true
}

To change retention:
1. Edit ephemeral/.metadata.json
2. Restart server (for cleanup_on_startup)
3. Or run cleanup_ephemeral manually
```

---

### Step 2: Update Retention Policy

```
You: Change retention to 14 days
```

**What Claude Does:**

Updates configuration:

```json
{
  "retention_days": 14,
  "last_cleanup": "2025-10-16T14:23:45Z",
  "cleanup_on_startup": true
}
```

**Expected Response:**
```
Claude: ✅ Retention policy updated

Previous: 30 days
New: 14 days

Impact:
- Files older than 14 days will be removed on next cleanup
- Current files affected: 3 files (now eligible for cleanup)

Would you like to run cleanup_ephemeral now to apply the new policy?
```

**Warning:**
```
⚠️  Reducing retention period immediately affects cleanup.
Files between old and new thresholds will be removed on next cleanup.

Example:
- Old policy: 30 days
- New policy: 14 days
- Files aged 15-30 days: Now eligible for deletion
```

---

## Task 5: Monitor Storage Limits

**Scenario:** Prevent disk space issues by monitoring storage usage.

### Step 1: Check Storage Quotas

```
You: What are the storage limits for ephemeral content?
```

**Expected Response:**
```
Claude: 💾 Storage Limits and Quotas

Default Limits:
- Max draft configs: 100 (current: 4)
- Max ephemeral output size: 100 MB (current: 17.9 KB)
- Max single file size: 10 MB

Configurable in: server configuration

Current Usage:
Ephemeral Storage:
├─ Drafts: 4/100 (4%)
├─ Size: 17.9 KB / 100 MB (0.02%)
└─ Largest file: 8.7 KB

Status: ✅ Well within limits

Alerts:
- None (all usage healthy)
```

---

### Step 2: Handle Storage Limit Exceeded

**Scenario:** Too many drafts accumulated.

**Expected Response:**
```
Claude: ⚠️  Storage Limit Approaching

Ephemeral Storage:
├─ Drafts: 95/100 (95%) ⚠️
├─ Size: 87.3 MB / 100 MB (87.3%)
└─ Oldest draft: 28 days old

Recommendations:
1. Run cleanup_ephemeral to remove expired files
2. Save important drafts to permanent storage using save_config
3. Delete abandoned drafts manually

Would you like me to:
- Clean up expired files now?
- List drafts older than 21 days for review?
```

**What You Learned:**
- Proactive monitoring prevents issues
- Clear warning thresholds
- Actionable recommendations

---

## Task 6: Recovery Strategies

**Scenario:** Accidentally deleted important content or need to recover from cleanup.

### Strategy 1: Regenerate from Config

**Problem:** Deleted output file, but config still exists.

```
You: I accidentally deleted user-guide.md, can I recover it?
```

**Expected Response:**
```
Claude: ✅ Recovery possible

Deleted file: output/user-guide.md
Config: configs/content/user-guide.json (still exists)

Recovery steps:
1. Regenerate using existing config:
   generate_content --config user-guide

Claude will:
generate_content(content_config_id="user-guide")

✅ Regenerated: output/user-guide.md
Content: Identical to deleted version (deterministic generator)
```

**What You Learned:**
- Configs enable recovery
- Deterministic generators recreate exact output
- No data loss if config exists

---

### Strategy 2: Recover Draft Before Expiration

**Problem:** Draft is about to expire (day 29/30), but you need it.

```
You: My draft is expiring tomorrow, save it!
```

**What Claude Does:**

```json
{
  "draft_id": "draft_2025091701_abc123",
  "config_id": "my-saved-config"
}
```

Calls `save_config` to move draft to permanent storage.

**Expected Response:**
```
Claude: ✅ Draft saved before expiration

Draft: draft_2025091701_abc123 (age: 29 days)
Saved to: configs/content/my-saved-config.json

Status:
- Removed from ephemeral storage
- Added to permanent storage (configs/)
- Now version controlled
- No longer subject to retention cleanup

The config is now permanent and safe from expiration.
```

---

### Strategy 3: Export Before Cleanup

**Problem:** Want to keep record of drafts before cleanup.

```
You: Export all drafts to archive before cleanup
```

**What Claude Does:**

```bash
# Create archive directory
mkdir -p archives/drafts-2025-10-16/

# Copy all drafts
cp -r ephemeral/drafts/* archives/drafts-2025-10-16/

# Create manifest
ls -lR ephemeral/drafts/ > archives/drafts-2025-10-16/MANIFEST.txt
```

**Expected Response:**
```
Claude: ✅ Drafts archived

Archive location: archives/drafts-2025-10-16/
Contents:
- 4 draft configs (12.3 KB)
- MANIFEST.txt (listing)
- README.md (archive info)

Drafts are preserved outside ephemeral storage.
Safe to run cleanup_ephemeral now.
```

---

## Task 7: CI/CD Integration

**Scenario:** Clean up ephemeral storage in CI/CD pipelines.

### CI/CD Cleanup Script

**GitHub Actions Example:**

```yaml
# .github/workflows/cleanup-ephemeral.yml
name: Cleanup Ephemeral Storage

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday at midnight
  workflow_dispatch:     # Manual trigger

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Chora Compose
        run: pip install chora-compose

      - name: Run Ephemeral Cleanup
        run: |
          # Start MCP server
          python -m chora_compose.mcp.server &
          SERVER_PID=$!

          # Wait for server startup
          sleep 5

          # Call cleanup via MCP client
          # (Actual implementation depends on your CI setup)
          python scripts/cleanup_ephemeral.py

          # Stop server
          kill $SERVER_PID

      - name: Report Cleanup Results
        run: |
          echo "Cleanup completed at $(date)"
          echo "Ephemeral storage size: $(du -sh ephemeral/)"
```

**Python Cleanup Script (scripts/cleanup_ephemeral.py):**

```python
#!/usr/bin/env python3
"""CI/CD script to clean up ephemeral storage."""

import asyncio
from chora_compose.storage.ephemeral_config import EphemeralConfigManager

async def main():
    manager = EphemeralConfigManager()

    # Get cleanup preview
    preview = manager.preview_cleanup()
    print(f"Files to remove: {len(preview['expired_files'])}")
    print(f"Space to free: {preview['total_size_kb']} KB")

    # Execute cleanup
    result = manager.cleanup_expired()
    print(f"Removed: {result['removed_count']} files")
    print(f"Freed: {result['freed_kb']} KB")

    # Report final state
    status = manager.get_storage_status()
    print(f"Remaining: {status['total_files']} files ({status['total_kb']} KB)")

if __name__ == "__main__":
    asyncio.run(main())
```

**What You Learned:**
- Automated cleanup in CI/CD
- Scheduled maintenance
- Monitoring and reporting

---

## Best Practices

### ✅ Do's

1. **Run Cleanup Regularly**
   ```
   ✅ Good: Weekly automated cleanup (CI/CD)
   ❌ Bad: Manual cleanup only when disk is full
   ```

2. **Save Important Drafts Before Expiration**
   ```python
   # Check draft age before it expires
   if draft.age_days > 25:  # 5-day buffer
       save_config(draft_id, config_id)
   ```

3. **Monitor Storage Proactively**
   ```
   ✅ Good: Check storage weekly, alert at 80% capacity
   ❌ Bad: Wait for disk full errors
   ```

4. **Use Ephemeral for Experiments**
   ```
   ✅ Good: Draft → Test → Iterate → Save when ready
   ❌ Bad: Edit production configs directly
   ```

5. **Archive Before Major Cleanup**
   ```
   For retention policy changes: Export drafts first
   ```

---

### ❌ Don'ts

1. **Don't Rely on Ephemeral for Important Data**
   ```
   ❌ Bad: Only draft exists, expires → data lost
   ✅ Good: Save important drafts to permanent storage
   ```

2. **Don't Disable Automatic Cleanup**
   ```
   ❌ Bad: Set retention_days = 999999 (defeats purpose)
   ✅ Good: Use appropriate retention (14-30 days)
   ```

3. **Don't Delete Permanent Content Carelessly**
   ```
   ❌ Bad: delete_content without checking dependencies
   ✅ Good: Check dependencies → Remove references → Delete
   ```

4. **Don't Ignore Storage Warnings**
   ```
   ❌ Bad: "95% full" warning → ignore until disk full
   ✅ Good: Act on warnings before limits reached
   ```

---

## Troubleshooting

### Issue: Cleanup Not Running Automatically

**Symptoms:**
```
Expired files (35+ days old) still in ephemeral/
```

**Possible Causes:**

1. **Server not restarted since files expired**
   - Solution: Restart server or run `cleanup_ephemeral` manually

2. **Cleanup on startup disabled**
   - Check: `ephemeral/.metadata.json` → `cleanup_on_startup: false`
   - Solution: Set to `true` or run manual cleanup

3. **Metadata file missing**
   - Solution: Server will recreate on next startup

---

### Issue: Files Cleaned Up Too Early

**Symptoms:**
```
Draft was only 10 days old, but got cleaned up
```

**Cause:** Retention policy was changed from 30 days → 7 days.

**Solution:**
```
1. Check ephemeral/.metadata.json for retention_days
2. Restore retention_days to desired value
3. Drafts cannot be recovered after cleanup
4. For important work: Use save_config to persist drafts immediately
```

**Prevention:**
```python
# Save important drafts immediately
if draft.is_important:
    save_config(draft_id, permanent_config_id)
```

---

### Issue: Storage Limit Exceeded

**Error:**
```
Error: Ephemeral storage limit exceeded (100 drafts)
Cannot create new draft.
```

**Solutions:**

1. **Clean up expired drafts**
   ```
   cleanup_ephemeral()
   ```

2. **Save and remove unneeded drafts**
   ```
   # Save important ones
   save_config("draft_abc", "my-config")

   # Delete abandoned ones
   delete_draft("draft_xyz")
   ```

3. **Adjust retention policy**
   ```json
   {
     "retention_days": 14  // Reduce from 30
   }
   ```

---

### Issue: Accidentally Deleted Important File

**Recovery Options:**

1. **Regenerate from config** (if config exists)
   ```
   generate_content(content_config_id="...")
   ```

2. **Restore from Git** (if permanently saved)
   ```bash
   git log -- path/to/file.md
   git checkout <commit> -- path/to/file.md
   ```

3. **Use backup** (if you have one)
   ```bash
   cp backup/file.md output/file.md
   ```

**Prevention:**
```
✅ Good: Version control permanent configs
✅ Good: Regular backups
✅ Good: Confirm before deleting
```

---

## Related Documentation

- **[Tutorial: Conversational Config Creation](../../tutorials/intermediate/02-conversational-config-creation.md)** - Part 5 covers draft lifecycle
- **[How-To: Create Config Conversationally](../configs/create-config-conversationally.md)** - Draft management workflows
- **[Explanation: Conversational Workflow Authoring](../../explanation/architecture/conversational-workflow-authoring.md)** - Design rationale for ephemeral storage
- **[Reference: EphemeralConfigManager API](../../reference/api/storage/ephemeral-config-manager.md)** - Complete API reference
- **[E2E Test Suite: Storage Management](../../mcp/E2E_STORAGE.md)** - Test cases for cleanup and deletion

---

**You can now effectively manage ephemeral storage and maintain a clean, efficient workspace!**
