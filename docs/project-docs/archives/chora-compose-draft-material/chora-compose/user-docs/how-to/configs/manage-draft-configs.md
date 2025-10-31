# How-To: Manage Draft Configurations

> **⚠️ DEPRECATED (v1.2.0):** This guide describes draft config management features that are **planned for v1.3.0** but **not yet implemented**. The tools `draft_config`, `test_config`, `modify_config`, and `save_config` referenced in this document do not exist in v1.2.0. See [create-config-conversationally.md](./create-config-conversationally.md) for status.

**Goal:** Understand and manage ephemeral draft storage, retention policies, and cleanup operations for conversational config workflows (planned for v1.3.0).

**Prerequisites:**
- Chora Compose v1.1.0+ installed
- Basic understanding of [conversational config creation](./create-config-conversationally.md)
- Familiarity with draft_config, test_config, save_config tools

**Time:** 10-20 minutes

---

## Overview

Draft configurations are stored in **ephemeral storage** with automatic 30-day retention. This guide covers:

- Understanding ephemeral vs permanent storage
- Listing and inspecting drafts
- Manual cleanup operations
- Retention policy management
- Recovery and backup strategies

---

## Ephemeral Storage Architecture

### Storage Structure

```
chora-compose/
├── configs/                    # Permanent storage (git-tracked)
│   ├── content/
│   │   └── my-report.json     # Saved configs (permanent)
│   └── artifact/
│       └── full-docs.json
│
├── ephemeral/                  # Temporary storage (.gitignore'd)
│   ├── drafts/                 # Draft configs (30-day retention)
│   │   ├── content/
│   │   │   ├── draft_abc123.json
│   │   │   └── draft_def456.json
│   │   └── artifact/
│   │       └── draft_ghi789.json
│   │
│   ├── output/                 # Test generations (30-day retention)
│   │   └── test_preview_*.md
│   │
│   └── .metadata.json          # Retention tracking
```

---

### Key Differences: Ephemeral vs Permanent

| Aspect | Ephemeral Storage | Permanent Storage |
|--------|------------------|-------------------|
| **Location** | `ephemeral/drafts/` | `configs/` |
| **Git tracking** | ❌ In `.gitignore` | ✅ Version controlled |
| **Retention** | 30 days (auto-cleanup) | Forever (manual delete only) |
| **Purpose** | Experimentation, iteration | Production configs |
| **Backup** | ❌ Not backed up | ✅ Backed up with repo |
| **File naming** | `draft_<random_id>.json` | `<descriptive-name>.json` |

---

## Task 1: List All Draft Configurations

### Using MCP Tools (Claude Desktop)

**You:**
```
List all my draft configurations
```

**Claude will:**
- Scan `ephemeral/drafts/content/` and `ephemeral/drafts/artifact/`
- Read metadata for each draft
- Display organized list

**Expected Response:**
```
Active Drafts (4 total):

Content Configurations (3):
┌─────────────────┬──────────────────────┬────────────┬──────────────┐
│ Draft ID        │ Description          │ Created    │ Expires      │
├─────────────────┼──────────────────────┼────────────┼──────────────┤
│ draft_abc123    │ Weekly team report   │ Oct 16     │ Nov 15       │
│ draft_def456    │ API documentation    │ Oct 14     │ Nov 13       │
│ draft_ghi789    │ Release notes v2     │ Oct 12     │ Nov 11       │
└─────────────────┴──────────────────────┴────────────┴──────────────┘

Artifact Configurations (1):
┌─────────────────┬──────────────────────┬────────────┬──────────────┐
│ Draft ID        │ Description          │ Created    │ Expires      │
├─────────────────┼──────────────────────┼────────────┼──────────────┤
│ draft_jkl012    │ Complete docs bundle │ Oct 15     │ Nov 14       │
└─────────────────┴──────────────────────┴────────────┴──────────────┘

Storage used: 45.6 KB
```

---

### Using Direct Filesystem Access

**Command:**
```bash
# List content drafts
ls -lh ephemeral/drafts/content/

# List artifact drafts
ls -lh ephemeral/drafts/artifact/

# Count total drafts
find ephemeral/drafts/ -name "draft_*.json" | wc -l
```

**Example Output:**
```
ephemeral/drafts/content/:
-rw-r--r--  1 user  staff   12K Oct 16 14:30 draft_abc123.json
-rw-r--r--  1 user  staff   8.5K Oct 14 09:15 draft_def456.json
-rw-r--r--  1 user  staff   15K Oct 12 11:45 draft_ghi789.json

Total: 3 drafts (35.5 KB)
```

---

## Task 2: Inspect a Specific Draft

### View Draft Contents

**Using Claude:**
```
You: Show me what's in draft_abc123
```

**Claude will:**
- Read draft file
- Parse JSON
- Summarize key fields

**Expected Response:**
```
Draft: draft_abc123
Type: content
Created: October 16, 2025 14:30
Expires: November 15, 2025

Configuration:
  ID: weekly-team-report
  Generator: jinja2
  Template: team-report.md.jinja

  Context Variables:
    - team_name
    - week
    - pr_count
    - story_points

  Input Sources:
    - github_prs (GitHub API)
    - jira_points (Jira API)

  Validation: ✅ Valid (JSON Schema v3.1)

This draft is ready to test or save.
```

---

### View Draft as Raw JSON

**Command:**
```bash
cat ephemeral/drafts/content/draft_abc123.json
```

**Or using jq for formatted view:**
```bash
cat ephemeral/drafts/content/draft_abc123.json | jq '.'
```

---

## Task 3: Clean Up Old Drafts

### Automatic Cleanup (Default Behavior)

**How It Works:**
- Drafts automatically deleted after 30 days of inactivity
- Cleanup runs periodically (daily cron or on-demand)
- Uses `cleanup_ephemeral` MCP tool

**You don't need to do anything** - cleanup happens automatically.

---

### Manual Cleanup Using MCP Tools

**Scenario:** You want to clean up drafts older than 7 days.

**Using Claude:**
```
You: Clean up draft configs older than 7 days
```

**Claude will:**
- Call `cleanup_ephemeral` tool with retention parameter
- Scan draft timestamps
- Delete expired drafts
- Return cleanup summary

**Expected Response:**
```
Cleanup Summary:

Deleted Drafts (2):
  - draft_xyz123 (content, 15 days old)
  - draft_uvw456 (artifact, 12 days old)

Retained Drafts (2):
  - draft_abc123 (content, 4 days old)
  - draft_def456 (content, 2 days old)

Storage freed: 28.3 KB
```

---

### Manual Cleanup Using Filesystem

**Delete specific draft:**
```bash
rm ephemeral/drafts/content/draft_abc123.json
```

**Delete all content drafts:**
```bash
rm ephemeral/drafts/content/draft_*.json
```

**Delete drafts older than 7 days (macOS/Linux):**
```bash
find ephemeral/drafts/ -name "draft_*.json" -mtime +7 -delete
```

**Verify before deleting:**
```bash
# List what would be deleted (dry run)
find ephemeral/drafts/ -name "draft_*.json" -mtime +7
```

---

## Task 4: Adjust Retention Policies

### Default Retention: 30 Days

**How It's Configured:**
- Default retention: 30 days from last modification
- Configurable via `EphemeralConfigManager`
- Applies to both drafts and test output

---

### Change Retention for Specific Project

**Edit configuration (future feature):**
```json
{
  "ephemeral_storage": {
    "retention_days": 60,
    "cleanup_schedule": "daily"
  }
}
```

**Current workaround (v1.1.0):**
Manually adjust cleanup schedule using cron or task scheduler.

---

### Disable Automatic Cleanup (Not Recommended)

**Why you might want this:**
- Long-term experimentation (>30 days)
- Offline development scenarios
- Testing retention behavior

**How:**
```bash
# Rename .metadata.json to disable cleanup
mv ephemeral/.metadata.json ephemeral/.metadata.json.disabled
```

**⚠️ Warning:** This can lead to unbounded storage growth. Re-enable after testing.

---

## Task 5: Back Up Important Drafts

### Save Draft to Permanent Storage

**Before 30-day expiration:**

**Using Claude:**
```
You: Save draft_abc123 to configs/content/
```

**Claude will:**
- Call `save_config(draft_id)`
- Atomic copy to permanent storage
- Validate before persisting

**Result:**
```
✅ Saved: configs/content/weekly-team-report.json

The draft is now permanent and won't expire.
Draft remains in ephemeral storage for potential rollback.
```

---

### Export Draft to External File

**Scenario:** You want to back up a draft outside the repo.

**Command:**
```bash
# Copy draft to backup directory
cp ephemeral/drafts/content/draft_abc123.json ~/backups/draft-backup-$(date +%Y%m%d).json
```

**Or using Claude:**
```
You: Export draft_abc123 to a backup file
```

---

### Bulk Export All Drafts

**Command:**
```bash
# Create timestamped backup archive
tar -czf draft-backups-$(date +%Y%m%d).tar.gz ephemeral/drafts/

# Or copy entire drafts directory
cp -r ephemeral/drafts/ ~/backups/drafts-$(date +%Y%m%d)/
```

**Restore from backup:**
```bash
# Extract backup archive
tar -xzf draft-backups-20251016.tar.gz -C ephemeral/

# Or copy directory back
cp -r ~/backups/drafts-20251016/ ephemeral/drafts/
```

---

## Task 6: Recover Expired Drafts

### Scenario 1: Draft Expired Recently (Within Backup Window)

**If you have backups:**
```bash
# Restore from backup
cp ~/backups/drafts-20251016/content/draft_abc123.json ephemeral/drafts/content/
```

**If using version control (hypothetical):**
```bash
# Restore from git history (if ephemeral/ was tracked)
git checkout HEAD~10 -- ephemeral/drafts/content/draft_abc123.json
```

---

### Scenario 2: Draft Expired Long Ago (No Backup)

**Bad news:** Draft is permanently deleted after cleanup.

**Prevention strategies:**
1. **Save important drafts within 30 days**
2. **Use longer retention for critical projects**
3. **Backup ephemeral/ directory periodically**

**Recreate approach:**
```
You: Recreate a config similar to my old team report draft
Claude: [Guides you through recreating from memory/description]
```

---

## Task 7: Monitor Storage Usage

### Check Ephemeral Storage Size

**Command:**
```bash
# Total ephemeral storage
du -sh ephemeral/

# Break down by subdirectory
du -h ephemeral/*/
```

**Example Output:**
```
45.6 KB    ephemeral/drafts/
12.3 KB    ephemeral/output/
57.9 KB    ephemeral/
```

---

### Check Draft Count by Age

**Using Claude:**
```
You: How many drafts do I have, grouped by age?
```

**Expected Response:**
```
Draft Age Distribution:

0-7 days:   4 drafts (32.1 KB)
8-14 days:  2 drafts (18.5 KB)
15-21 days: 1 draft (8.2 KB)
22-30 days: 1 draft (3.8 KB)

Total: 8 drafts (62.6 KB)

Recommendation: 1 draft is nearing expiration (28 days old)
```

---

### Set Up Monitoring Alerts

**Example cron job to warn about expiring drafts:**

```bash
#!/bin/bash
# File: ~/.local/bin/check-expiring-drafts.sh

# Find drafts older than 25 days
expiring=$(find ephemeral/drafts/ -name "draft_*.json" -mtime +25)

if [ -n "$expiring" ]; then
  echo "⚠️  Drafts expiring soon (>25 days old):"
  echo "$expiring"
  # Send notification (macOS)
  osascript -e 'display notification "Drafts expiring soon!" with title "Chora Compose"'
fi
```

**Add to crontab:**
```bash
# Run daily at 9 AM
0 9 * * * ~/.local/bin/check-expiring-drafts.sh
```

---

## Task 8: Manage Test Output Retention

### Test Output Storage

**Location:**
```
ephemeral/output/
├── test_preview_draft_abc123_20251016143045.md
├── test_preview_draft_def456_20251014091530.md
└── test_preview_draft_ghi789_20251012114500.md
```

**Purpose:**
- Store previews from `test_config` calls
- Help with comparing different test runs
- Temporary (30-day retention like drafts)

---

### List Test Outputs

**Command:**
```bash
ls -lh ephemeral/output/
```

**Using Claude:**
```
You: Show me all test outputs for draft_abc123
```

**Expected Response:**
```
Test Outputs for draft_abc123 (3):

1. 2025-10-16 14:30 - test_preview_draft_abc123_20251016143045.md (2.4 KB)
   Context: team=Engineering, week=2025-W42

2. 2025-10-16 15:15 - test_preview_draft_abc123_20251016151500.md (2.8 KB)
   Context: team=Engineering, week=2025-W42 (with metrics)

3. 2025-10-16 16:00 - test_preview_draft_abc123_20251016160000.md (3.1 KB)
   Context: team=Product, week=2025-W42

You can compare these to see evolution of your config.
```

---

### Clean Up Test Outputs

**Delete all test outputs:**
```bash
rm ephemeral/output/test_preview_*.md
```

**Delete for specific draft:**
```bash
rm ephemeral/output/test_preview_draft_abc123_*.md
```

**Using Claude:**
```
You: Delete all test outputs older than 7 days
```

---

## Common Scenarios & Solutions

### Scenario 1: Running Out of Disk Space

**Symptoms:**
```
❌ Error: Cannot create draft - disk space full
```

**Diagnosis:**
```bash
# Check ephemeral storage size
du -sh ephemeral/

# Check available disk space
df -h .
```

**Solution:**
```bash
# Clean up old drafts (>7 days)
find ephemeral/drafts/ -name "draft_*.json" -mtime +7 -delete

# Clean up all test outputs
rm ephemeral/output/test_preview_*.md

# Check freed space
du -sh ephemeral/
```

---

### Scenario 2: Accidentally Deleted Wrong Draft

**Problem:**
```bash
# Oops! Deleted wrong draft
rm ephemeral/drafts/content/draft_abc123.json
```

**Recovery (if recent):**
```bash
# Check trash/recycle bin (macOS)
open ~/.Trash

# Or restore from backup
cp ~/backups/drafts-20251016/content/draft_abc123.json ephemeral/drafts/content/
```

**Prevention:**
```bash
# Use safer delete with confirmation
rm -i ephemeral/drafts/content/draft_abc123.json

# Or move to archive first
mkdir -p ephemeral/archive/
mv ephemeral/drafts/content/draft_abc123.json ephemeral/archive/
```

---

### Scenario 3: Need to Preserve Drafts for >30 Days

**Use Case:** Long-term experimentation or research project.

**Option 1: Save as Permanent Configs**
```
You: Save all my drafts to configs/experiments/ directory
```

**Option 2: Extend Retention (Manual)**
```bash
# Touch files to reset modification time
find ephemeral/drafts/ -name "draft_*.json" -exec touch {} \;
```

**Option 3: Export to External Storage**
```bash
# Weekly backup cron job
tar -czf ~/archives/drafts-$(date +%Y%m%d).tar.gz ephemeral/drafts/
```

---

### Scenario 4: Sharing Drafts with Team

**Problem:** Drafts are local and not in git.

**Solution 1: Save to Shared Config Directory**
```
You: Save draft_abc123 to configs/team-shared/experimental/
```

Then commit to git:
```bash
git add configs/team-shared/experimental/
git commit -m "Add experimental team report config"
git push
```

**Solution 2: Export and Send**
```bash
# Export draft to shareable file
cp ephemeral/drafts/content/draft_abc123.json team-report-draft.json

# Send via email, Slack, etc.
```

Teammate can then:
```
You: Load team-report-draft.json as a new draft
```

---

## Best Practices

### ✅ Do's

1. **Save Important Drafts Early**
   - Don't wait until day 29 to save valuable configs
   - Save when 80% confident, refine in permanent storage

2. **Use Descriptive Draft Descriptions**
   ```json
   {
     "description": "Weekly team report - Engineering - Q4 2025 format"
   }
   ```
   Makes listing/searching easier.

3. **Periodic Backups**
   ```bash
   # Weekly backup script
   tar -czf ~/backups/drafts-$(date +%Y%m%d).tar.gz ephemeral/
   ```

4. **Monitor Storage Usage**
   - Check `du -sh ephemeral/` periodically
   - Clean up test outputs regularly
   - Don't let drafts accumulate indefinitely

5. **Use Drafts for Experimentation**
   - Ephemeral storage is perfect for trying ideas
   - Don't be afraid to create many drafts
   - Let cleanup handle the rest

---

### ❌ Don'ts

1. **Don't Commit Ephemeral Storage to Git**
   ```gitignore
   # .gitignore (already configured)
   ephemeral/
   ```
   Ephemeral should stay local.

2. **Don't Store Critical Data Only in Drafts**
   - Drafts are temporary by design
   - Save important configs to permanent storage
   - Back up if needed for >30 days

3. **Don't Disable Auto-Cleanup Without Good Reason**
   - Leads to unbounded storage growth
   - Makes draft management harder
   - Only disable temporarily for testing

4. **Don't Manually Edit .metadata.json**
   - Managed by EphemeralConfigManager
   - Manual edits can break retention tracking
   - Use MCP tools instead

---

## Troubleshooting

### Issue: Cleanup Not Running

**Symptoms:**
- Drafts older than 30 days still present
- Storage growing unbounded

**Diagnosis:**
```bash
# Check .metadata.json
cat ephemeral/.metadata.json

# Check draft ages
find ephemeral/drafts/ -name "draft_*.json" -mtime +30
```

**Solutions:**
1. **Manual cleanup:**
   ```bash
   find ephemeral/drafts/ -name "draft_*.json" -mtime +30 -delete
   ```

2. **Using MCP tool:**
   ```
   You: Run cleanup_ephemeral with default retention
   ```

3. **Check cron/scheduler:**
   ```bash
   # Verify cleanup is scheduled
   crontab -l | grep cleanup
   ```

---

### Issue: Can't Create New Drafts

**Error:**
```
❌ Failed to create draft: Permission denied
```

**Solution:**
```bash
# Check directory permissions
ls -ld ephemeral/drafts/

# Fix if needed
chmod 755 ephemeral/drafts/
chmod 755 ephemeral/drafts/content/
chmod 755 ephemeral/drafts/artifact/
```

---

### Issue: Draft Corrupted (Invalid JSON)

**Symptoms:**
```
❌ Error reading draft_abc123: Invalid JSON
```

**Diagnosis:**
```bash
# Validate JSON
cat ephemeral/drafts/content/draft_abc123.json | jq '.'
```

**Solutions:**
1. **Restore from backup:**
   ```bash
   cp ~/backups/draft_abc123.json ephemeral/drafts/content/
   ```

2. **Manual repair (if possible):**
   ```bash
   # Edit with text editor
   vim ephemeral/drafts/content/draft_abc123.json
   ```

3. **Recreate from scratch:**
   ```
   You: Recreate the team report draft from description
   ```

---

## Advanced: Programmatic Draft Management

### Python API Access

```python
from chora_compose.storage import get_ephemeral_config_manager

# Get manager instance
manager = get_ephemeral_config_manager()

# List all drafts
content_drafts = manager.list_drafts("content")
artifact_drafts = manager.list_drafts("artifact")

print(f"Content drafts: {len(content_drafts)}")
print(f"Artifact drafts: {len(artifact_drafts)}")

# Inspect specific draft
draft = manager.get_draft("draft_abc123", "content")
print(f"Draft ID: {draft['id']}")
print(f"Created: {draft['metadata']['created_at']}")

# Delete specific draft
manager.delete_draft("draft_abc123", "content")
print("Draft deleted")

# Run cleanup with custom retention
deleted_count = manager.cleanup_expired_drafts(retention_days=14)
print(f"Cleaned up {deleted_count} expired drafts")
```

---

## Quick Command Reference

```bash
# List drafts
ls -lh ephemeral/drafts/content/
ls -lh ephemeral/drafts/artifact/

# Count drafts
find ephemeral/drafts/ -name "draft_*.json" | wc -l

# Check storage size
du -sh ephemeral/

# Delete specific draft
rm ephemeral/drafts/content/draft_abc123.json

# Clean up old drafts (>7 days)
find ephemeral/drafts/ -name "draft_*.json" -mtime +7 -delete

# Backup drafts
tar -czf drafts-backup-$(date +%Y%m%d).tar.gz ephemeral/drafts/

# Restore from backup
tar -xzf drafts-backup-20251016.tar.gz -C ephemeral/

# View draft contents
cat ephemeral/drafts/content/draft_abc123.json | jq '.'
```

---

## Related Documentation

- **[How-To: Create Config Conversationally](./create-config-conversationally.md)** - Using drafts in workflow
- **[Tutorial: Conversational Config Creation](../../tutorials/intermediate/02-conversational-config-creation.md)** - Hands-on learning
- **[Reference: EphemeralConfigManager API](../../reference/api/storage/ephemeral-config-manager.md)** - API documentation
- **[MCP Tool Reference: cleanup_ephemeral](../../mcp/tool-reference.md#cleanup_ephemeral)** - Tool documentation

---

**You now know how to manage ephemeral draft storage effectively!**
