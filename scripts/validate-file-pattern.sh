#!/usr/bin/env bash
# File Pattern Validation Script
#
# Validates glob patterns before work context registration.
# Part of chora.coordination.work_context (SAP L3 Phase 1.3)
#
# Usage:
#   validate-file-pattern.sh <pattern> [--strict]
#
# Arguments:
#   pattern : Glob pattern to validate (e.g., "docs/**/*.md", "justfile")
#   --strict: (Optional) Fail if pattern matches no files (default: warn only)
#
# Examples:
#   validate-file-pattern.sh "docs/**/*.md"
#   validate-file-pattern.sh "justfile" --strict
#
# Exit Codes:
#   0 : Valid pattern (matches ≥1 file OR warning-only mode)
#   1 : Invalid pattern syntax
#   2 : Pattern matches no files (--strict mode only)

set -uo pipefail

# ============================================================================
# Configuration
# ============================================================================

PATTERN="${1:-}"
STRICT_MODE=false

if [ "${2:-}" = "--strict" ]; then
    STRICT_MODE=true
fi

# ============================================================================
# Validation
# ============================================================================

if [ -z "$PATTERN" ]; then
    echo "Error: pattern is required"
    echo "Usage: $0 <pattern> [--strict]"
    exit 1
fi

# ============================================================================
# Pattern Syntax Validation
# ============================================================================

# Check for common syntax errors
SYNTAX_VALID=true
ERROR_MSG=""

# Check 1: Unmatched brackets
open_brackets=$(echo "$PATTERN" | grep -o '\[' | wc -l | tr -d ' ')
close_brackets=$(echo "$PATTERN" | grep -o '\]' | wc -l | tr -d ' ')
if [ "$open_brackets" -ne "$close_brackets" ]; then
    SYNTAX_VALID=false
    ERROR_MSG="Unmatched brackets: $open_brackets '[' vs $close_brackets ']'"
fi

# Check 2: Unmatched braces
open_braces=$(echo "$PATTERN" | grep -o '{' | wc -l | tr -d ' ')
close_braces=$(echo "$PATTERN" | grep -o '}' | wc -l | tr -d ' ')
if [ "$open_braces" -ne "$close_braces" ]; then
    SYNTAX_VALID=false
    ERROR_MSG="Unmatched braces: $open_braces '{' vs $close_braces '}'"
fi

# Check 3: Invalid ** usage (must be **/ or /**)
if echo "$PATTERN" | grep -q '\*\*[^/]' && ! echo "$PATTERN" | grep -q '\*\*$'; then
    # ** followed by non-slash (and not at end of string)
    SYNTAX_VALID=false
    ERROR_MSG="Invalid ** usage: must be '**/' or '/**' or '**' at end"
fi

# Check 4: Triple or more asterisks (likely typo)
if echo "$PATTERN" | grep -q '\*\*\*'; then
    SYNTAX_VALID=false
    ERROR_MSG="Invalid pattern: *** (triple asterisk)"
fi

# Check 5: Absolute paths (not recommended for work contexts)
if [[ "$PATTERN" = /* ]]; then
    echo "⚠️  Warning: Absolute path detected: $PATTERN"
    echo "   Recommendation: Use relative paths from repository root"
    echo "   Example: docs/file.md (not /Users/.../docs/file.md)"
fi

if [ "$SYNTAX_VALID" = false ]; then
    echo "❌ Invalid pattern syntax: $PATTERN"
    echo "   Error: $ERROR_MSG"
    echo ""
    echo "Common glob patterns:"
    echo "  - **/*           : All files recursively"
    echo "  - docs/**/*.md   : All markdown files in docs/"
    echo "  - *.{py,sh}      : All .py and .sh files"
    echo "  - src/*/test.py  : test.py in any subdirectory of src/"
    exit 1
fi

# ============================================================================
# Pattern Match Validation (Does it match any files?)
# ============================================================================

# Expand pattern to see if it matches files
# Use glob expansion with nullglob option
shopt -s nullglob globstar 2>/dev/null || true

# Check if pattern matches any files
MATCH_COUNT=0

# Strategy: Use find with -path for glob patterns
if [[ "$PATTERN" == *"**"* ]]; then
    # Recursive pattern - use find
    # Convert glob to find -path syntax
    FIND_PATTERN=$(echo "$PATTERN" | sed 's|\*\*/|\*/|g')

    if MATCHES=$(find . -path "./$FIND_PATTERN" 2>/dev/null | head -n 5); then
        MATCH_COUNT=$(echo "$MATCHES" | grep -c '.' || echo 0)
    fi
elif [[ "$PATTERN" == *"*"* ]] || [[ "$PATTERN" == *"?"* ]]; then
    # Simple glob pattern - use ls
    if MATCHES=$(ls -d $PATTERN 2>/dev/null | head -n 5); then
        MATCH_COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')
    fi
else
    # Exact file path - check if file exists
    if [ -e "$PATTERN" ]; then
        MATCH_COUNT=1
    fi
fi

if [ "$MATCH_COUNT" -eq 0 ]; then
    if [ "$STRICT_MODE" = true ]; then
        echo "❌ Pattern matches no files: $PATTERN"
        echo "   Either:"
        echo "   1. Files don't exist yet (will be created later)"
        echo "   2. Pattern syntax is incorrect"
        echo ""
        echo "   To register anyway (for future files), remove --strict flag"
        exit 2
    else
        echo "⚠️  Warning: Pattern matches no existing files: $PATTERN"
        echo "   This is OK if files will be created later"
        echo "   Use --strict to fail on zero matches"
    fi
else
    echo "✅ Valid pattern: $PATTERN (matches $MATCH_COUNT file(s))"

    # Show first few matches for confirmation
    if [ "$MATCH_COUNT" -le 5 ]; then
        echo "   Matched files:"
        if [[ "$PATTERN" == *"**"* ]]; then
            find . -path "./$FIND_PATTERN" 2>/dev/null | head -n 5 | sed 's|^\./|   - |'
        elif [[ "$PATTERN" == *"*"* ]] || [[ "$PATTERN" == *"?"* ]]; then
            ls -d $PATTERN 2>/dev/null | head -n 5 | sed 's|^|   - |'
        else
            echo "   - $PATTERN"
        fi
    else
        echo "   Showing first 5 matches:"
        if [[ "$PATTERN" == *"**"* ]]; then
            find . -path "./$FIND_PATTERN" 2>/dev/null | head -n 5 | sed 's|^\./|   - |'
        else
            ls -d $PATTERN 2>/dev/null | head -n 5 | sed 's|^|   - |'
        fi
        echo "   (and $((MATCH_COUNT - 5)) more...)"
    fi
fi

exit 0
