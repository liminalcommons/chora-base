#!/usr/bin/env bash
# Work Context Auto-Registration Script
#
# Automatically detects current work and registers a work context with inferred file patterns.
# Part of chora.coordination.work_context (SAP L3 Phase 1.1)
#
# Usage:
#   work-context-auto-register.sh <context-id> <context-type> [branch]
#
# Arguments:
#   context-id   : Unique identifier (e.g., tab-1, alice, session-morning)
#   context-type : One of: tab, dev, session
#   branch       : (Optional) Git branch, defaults to current branch
#
# Examples:
#   work-context-auto-register.sh tab-1 tab
#   work-context-auto-register.sh alice dev feature/new-ui
#
# Exit Codes:
#   0 : Success (context registered/updated)
#   1 : Error (invalid arguments, git failure, etc.)

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CONTEXT_ID="${1:-}"
CONTEXT_TYPE="${2:-}"
BRANCH="${3:-}"
CONTEXTS_FILE=".chora/work-contexts.yaml"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ============================================================================
# Validation
# ============================================================================

if [ -z "$CONTEXT_ID" ]; then
    echo "Error: context-id is required"
    echo "Usage: $0 <context-id> <context-type> [branch]"
    exit 1
fi

if [ -z "$CONTEXT_TYPE" ]; then
    echo "Error: context-type is required"
    echo "Usage: $0 <context-id> <context-type> [branch]"
    exit 1
fi

# Validate context type
if [[ ! "$CONTEXT_TYPE" =~ ^(tab|dev|session)$ ]]; then
    echo "Error: context-type must be one of: tab, dev, session"
    echo "Got: $CONTEXT_TYPE"
    exit 1
fi

# ============================================================================
# Detect Current Branch
# ============================================================================

if [ -z "$BRANCH" ]; then
    if ! BRANCH=$(git branch --show-current 2>/dev/null); then
        echo "Error: Not in a git repository and no branch specified"
        exit 1
    fi

    if [ -z "$BRANCH" ]; then
        echo "Error: Could not detect current branch (detached HEAD?)"
        exit 1
    fi
fi

echo "Analyzing current work for context: $CONTEXT_ID ($CONTEXT_TYPE) on branch $BRANCH..."
echo ""

# ============================================================================
# Detect Modified/Staged Files
# ============================================================================

# Get all files that are:
# - Modified (both staged and unstaged)
# - Added
# - Renamed
# - Files from recent commits on this branch (last 3 commits if available)

MODIFIED_FILES=()

# Staged and unstaged changes
if git diff --name-only HEAD 2>/dev/null | grep -v "^$"; then
    while IFS= read -r file; do
        [ -n "$file" ] && MODIFIED_FILES+=("$file")
    done < <(git diff --name-only HEAD 2>/dev/null)
fi

# Untracked files (newly added)
if git ls-files --others --exclude-standard 2>/dev/null | grep -v "^$"; then
    while IFS= read -r file; do
        [ -n "$file" ] && MODIFIED_FILES+=("$file")
    done < <(git ls-files --others --exclude-standard 2>/dev/null)
fi

# Files from recent commits on current branch (last 3 commits)
if git log --name-only --pretty=format: -n 3 2>/dev/null | grep -v "^$"; then
    while IFS= read -r file; do
        [ -n "$file" ] && MODIFIED_FILES+=("$file")
    done < <(git log --name-only --pretty=format: -n 3 2>/dev/null | grep -v "^$")
fi

# Remove duplicates while preserving order
UNIQUE_FILES=($(printf "%s\n" "${MODIFIED_FILES[@]}" | awk '!seen[$0]++'))

if [ ${#UNIQUE_FILES[@]} -eq 0 ]; then
    echo "⚠️  No modified files detected in current work"
    echo "   Checked:"
    echo "   - git diff HEAD (staged + unstaged)"
    echo "   - git ls-files --others (untracked)"
    echo "   - git log -n 3 (recent commits)"
    echo ""
    echo "   Consider manually specifying file patterns:"
    echo "   just work-context-register $CONTEXT_ID $CONTEXT_TYPE $BRANCH \"path/to/files/**/*\""
    exit 1
fi

echo "Detected ${#UNIQUE_FILES[@]} files in current work:"
for file in "${UNIQUE_FILES[@]}"; do
    echo "  - $file"
done
echo ""

# ============================================================================
# Infer File Patterns
# ============================================================================

# Strategy: Create minimal set of glob patterns that cover all detected files
# 1. Group files by directory
# 2. If ≥3 files in same directory → use directory/**/* pattern
# 3. Otherwise, use exact file paths
# 4. Special handling for common shared files (justfile, AGENTS.md, etc.)

declare -A DIR_FILE_COUNT
EXACT_FILES=()

# Count files per directory
for file in "${UNIQUE_FILES[@]}"; do
    dir=$(dirname "$file")

    # Special case: root directory files
    if [ "$dir" = "." ]; then
        EXACT_FILES+=("$file")
        continue
    fi

    DIR_FILE_COUNT["$dir"]=$((${DIR_FILE_COUNT["$dir"]:-0} + 1))
done

# Generate patterns
PATTERNS=()

# Add directory patterns (if ≥3 files in directory)
for dir in "${!DIR_FILE_COUNT[@]}"; do
    count=${DIR_FILE_COUNT["$dir"]}

    if [ "$count" -ge 3 ]; then
        # Use directory/** pattern
        PATTERNS+=("$dir/**/*")
    else
        # Add individual files from this directory
        for file in "${UNIQUE_FILES[@]}"; do
            if [ "$(dirname "$file")" = "$dir" ]; then
                EXACT_FILES+=("$file")
            fi
        done
    fi
done

# Add exact files (not covered by directory patterns)
for file in "${EXACT_FILES[@]}"; do
    # Skip if already covered by a directory pattern
    covered=false
    for pattern in "${PATTERNS[@]}"; do
        # Check if file would match this pattern
        pattern_dir="${pattern%/**/*}"
        if [[ "$file" == "$pattern_dir"* ]]; then
            covered=true
            break
        fi
    done

    if [ "$covered" = false ]; then
        PATTERNS+=("$file")
    fi
done

# Remove duplicates
UNIQUE_PATTERNS=($(printf "%s\n" "${PATTERNS[@]}" | sort -u))

echo "Inferred ${#UNIQUE_PATTERNS[@]} file patterns:"
for pattern in "${UNIQUE_PATTERNS[@]}"; do
    echo "  - $pattern"
done
echo ""

# ============================================================================
# Register or Update Work Context
# ============================================================================

# Ensure .chora directory exists
mkdir -p .chora

# Initialize contexts file if it doesn't exist
if [ ! -f "$CONTEXTS_FILE" ]; then
    echo "work_contexts:" > "$CONTEXTS_FILE"
fi

# Check if context already exists
CONTEXT_EXISTS=false
if grep -q "id: $CONTEXT_ID" "$CONTEXTS_FILE" 2>/dev/null; then
    CONTEXT_EXISTS=true
fi

if [ "$CONTEXT_EXISTS" = true ]; then
    echo "⚠️  Context $CONTEXT_ID already exists. Updating file patterns..."

    # Remove old context entry
    # Strategy: Use awk to skip the old context block
    # This is fragile, but works for lightweight pilot
    # Future L4 (capability server) will handle updates properly

    # For now, simpler approach: Remove old entry and append new one
    if command -v yq &> /dev/null; then
        # Use yq to remove old context
        yq eval "del(.work_contexts[] | select(.id == \"$CONTEXT_ID\"))" -i "$CONTEXTS_FILE"
    else
        # Python fallback
        python3 <<EOF
import yaml
with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f) or {}

work_contexts = data.get('work_contexts', [])
work_contexts = [ctx for ctx in work_contexts if ctx.get('id') != "$CONTEXT_ID"]
data['work_contexts'] = work_contexts

with open("$CONTEXTS_FILE", 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
EOF
    fi
fi

# Append new context entry
{
    echo "  - id: $CONTEXT_ID"
    echo "    type: $CONTEXT_TYPE"
    echo "    branch: $BRANCH"
    echo "    files:"
    for pattern in "${UNIQUE_PATTERNS[@]}"; do
        echo "      - \"$pattern\""
    done
    echo "    started_at: $TIMESTAMP"
    echo "    last_activity: $TIMESTAMP"
} >> "$CONTEXTS_FILE"

# ============================================================================
# Output Summary
# ============================================================================

if [ "$CONTEXT_EXISTS" = true ]; then
    echo "✅ Updated context $CONTEXT_ID ($CONTEXT_TYPE) on branch $BRANCH"
else
    echo "✅ Registered context $CONTEXT_ID ($CONTEXT_TYPE) on branch $BRANCH"
fi

echo "   Patterns registered: ${#UNIQUE_PATTERNS[@]}"
echo "   Files covered: ${#UNIQUE_FILES[@]}"
echo ""
echo "Next steps:"
echo "  - View dashboard: just work-dashboard"
echo "  - Check conflicts: just who-is-working-on <file>"
echo "  - Update context: just work-context-auto-register $CONTEXT_ID $CONTEXT_TYPE"
echo ""

# ============================================================================
# A-MEM Event Logging (SAP-010 integration)
# ============================================================================

if [ -f "scripts/lib/emit-event.sh" ]; then
    source scripts/lib/emit-event.sh

    # Build context JSON (escape quotes for JSON)
    PATTERNS_JSON=$(printf '%s\n' "${UNIQUE_PATTERNS[@]}" | jq -R . | jq -s .)
    FILES_JSON=$(printf '%s\n' "${UNIQUE_FILES[@]}" | jq -R . | jq -s .)

    CONTEXT_JSON=$(cat <<EOF
{
  "context_id": "$CONTEXT_ID",
  "context_type": "$CONTEXT_TYPE",
  "branch": "$BRANCH",
  "patterns_count": ${#UNIQUE_PATTERNS[@]},
  "files_count": ${#UNIQUE_FILES[@]},
  "patterns": $PATTERNS_JSON,
  "detection_sources": ["git_diff", "git_status", "recent_commits"]
}
EOF
)

    emit_event "work_context_auto_registered" \
               "Auto-registered work context $CONTEXT_ID ($CONTEXT_TYPE) with ${#UNIQUE_PATTERNS[@]} patterns" \
               "work-context-$CONTEXT_ID" \
               "$CONTEXT_JSON"
fi

exit 0
