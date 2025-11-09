#!/usr/bin/env bash
#
# ============================================================================
# DEPRECATED: This script has been migrated to Python for cross-platform support
# ============================================================================
#
# Use: python scripts/validate-links.py [PATH]
# Or:  just validate-links [PATH]
#
# Migration Guide: docs/user-docs/how-to/bash-to-python-migration.md
# Deprecated: v4.3.0 (2025-11-03)
# Removal: v5.0.0 (planned)
#
# Reason: Windows compatibility - this bash script:
#   - Already called Python for path normalization!
#   - Uses grep -oE (regex) with bash pipelines
#   - Uses find ... -print0 (bash-specific)
#   - Unicode emoji in output (❌✅)
#
# ============================================================================
#
# Link Validation Script v1.0-mvp
# Part of SAP-016: Link Validation & Reference Management
#
# Simplified MVP focusing on internal markdown link validation
# Usage: ./scripts/validate-links-simple.sh [PATH]  (DEPRECATED)
#        python scripts/validate-links.py [PATH]    (RECOMMENDED)

VERSION="1.0-mvp"
TARGET_PATH="${1:-.}"

# Counters
TOTAL_FILES=0
TOTAL_LINKS=0
BROKEN_LINKS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Link Validation Script v${VERSION}${NC}"
echo "Scanning: $TARGET_PATH"
echo ""

# Function to validate a single file
validate_file() {
    local file="$1"
    ((TOTAL_FILES++))

    # Extract internal links (non-http, non-mailto, non-anchor-only)
    local links=$(grep -oE '\[[^]]+\]\([^)]+\)' "$file" 2>/dev/null | \
                  grep -oE '\([^)]+\)' | \
                  tr -d '()' | \
                  grep -v '^http' | \
                  grep -v '^#$' | \
                  grep -v '^mailto' | \
                  grep -v '^tel' | \
                  grep -v '^javascript' || true)

    if [ -z "$links" ]; then
        return 0
    fi

    # Get base directory of file for resolving relative paths
    local base_dir="$(dirname "$file")"

    # Check each link
    while IFS= read -r link; do
        [ -z "$link" ] && continue

        ((TOTAL_LINKS++))

        # Strip anchor from link
        local link_file="${link%%#*}"

        # Resolve path using python for correct ../ handling
        local resolved_path
        if [[ "$link_file" == /* ]]; then
            # Absolute from repo root (remove leading /)
            resolved_path="${link_file:1}"
        else
            # Relative path - use python to normalize
            resolved_path="$(python3 -c "import os; print(os.path.normpath('$base_dir/$link_file'))" 2>/dev/null || echo "$base_dir/$link_file")"
        fi

        # Check if file or directory exists
        if [ -f "$resolved_path" ] || [ -d "$resolved_path" ]; then
            : # Valid link, do nothing
        else
            ((BROKEN_LINKS++))
            echo -e "${RED}❌ BROKEN:${NC} $file"
            echo "   → $link"
            echo "   (resolved to: $resolved_path)"
            echo ""
        fi
    done <<< "$links"
}

# Find and validate all markdown files
if [ -f "$TARGET_PATH" ]; then
    # Single file mode
    validate_file "$TARGET_PATH"
else
    # Directory mode
    while IFS= read -r -d '' file; do
        validate_file "$file"
    done < <(find "$TARGET_PATH" -type f -name "*.md" -print0)
fi

# Summary
echo "========================================"
echo "Link Validation Report"
echo "========================================"
echo "Files scanned: $TOTAL_FILES"
echo "Links checked: $TOTAL_LINKS"

if [ "$BROKEN_LINKS" -eq 0 ]; then
    echo -e "${GREEN}Broken links: 0 ✅${NC}"
    echo ""
    echo -e "${GREEN}Status: PASS ✅${NC}"
    exit 0
else
    echo -e "${RED}Broken links: $BROKEN_LINKS ❌${NC}"
    echo ""
    echo -e "${RED}Status: FAIL ❌${NC}"
    exit 1
fi
