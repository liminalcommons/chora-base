#!/bin/bash
#
# ============================================================================
# DEPRECATED: This script has been migrated to Python for cross-platform support
# ============================================================================
#
# Use: python scripts/rollback-migration.py
# Or:  just rollback-migration
#
# Migration Guide: docs/user-docs/how-to/bash-to-python-migration.md
# Deprecated: v4.3.0 (2025-11-03)
# Removal: v5.0.0 (planned)
#
# Reason: Windows compatibility - this bash script fails on Windows due to:
#   - find command with bash-specific flags
#   - Unicode emoji in output (🔄📦✅❌)
#   - Bash pipelines (wc -l | tr -d)
#
# ============================================================================
#
# Rollback migration to angle brackets (restore from backups)

set -e

echo "🔄 Rolling back migration..."

BACKUP_COUNT=$(find template/ -name "*.backup" -type f | wc -l | tr -d ' ')

if [ "$BACKUP_COUNT" -eq 0 ]; then
    echo "❌ No backup files found. Cannot rollback."
    exit 1
fi

echo "📦 Found $BACKUP_COUNT backup files"
echo ""

# Restore all backups
find template/ -name "*.backup" -type f | while read backup; do
    original="${backup%.backup}"
    cp "$backup" "$original"
    echo "  ✓ Restored: $(basename $original)"
done

echo ""
echo "✅ Rollback complete! Original files restored."
echo ""
echo "To remove backup files: find template/ -name '*.backup' -delete"
