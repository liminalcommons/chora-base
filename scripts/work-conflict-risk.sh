#!/usr/bin/env bash
# Work Context Conflict Risk Scoring Script
#
# Calculates conflict risk scores (0-100) for files in work contexts.
# Part of chora.coordination.work_context (SAP L3 Phase 3.1)
#
# Usage:
#   work-conflict-risk.sh [file1] [file2] ...
#   work-conflict-risk.sh --all
#
# Arguments:
#   file1, file2, ... : Specific files to score (optional)
#   --all             : Score all files in work contexts
#
# Risk Score Calculation (0-100):
#   - Ownership count (40 points max):
#     - 0 owners: 0 points
#     - 1 owner: 10 points
#     - 2 owners: 25 points (conflict)
#     - 3+ owners: 40 points (high conflict)
#   - File type (30 points max):
#     - Infrastructure files: 30 points (justfile, AGENTS.md, INDEX.md, etc.)
#     - Config files: 20 points (.yaml, .json, .toml)
#     - Source code: 10 points (.py, .sh, .js, etc.)
#     - Documentation: 5 points (.md)
#   - Modification recency (20 points max):
#     - Modified in last hour: 20 points
#     - Last 24h: 15 points
#     - Last week: 10 points
#     - Last month: 5 points
#     - Older: 0 points
#   - CODEOWNERS mismatch (10 points max):
#     - Work context owner not in CODEOWNERS: 10 points
#     - All owners in CODEOWNERS: 0 points
#
# Risk Levels:
#   - LOW (0-33): Safe to edit
#   - MEDIUM (34-66): Coordinate before editing
#   - HIGH (67-100): High conflict risk
#
# Exit Codes:
#   0 : Success
#   1 : Error

set -uo pipefail

# ============================================================================
# Configuration
# ============================================================================

CONTEXTS_FILE=".chora/work-contexts.yaml"
WHO_SCRIPT="scripts/who-is-working-on.sh"
CODEOWNERS_FILE="CODEOWNERS"

FILES_TO_SCORE=()
SCORE_ALL=false

# Parse arguments
if [ "${1:-}" = "--all" ]; then
    SCORE_ALL=true
elif [ $# -gt 0 ]; then
    FILES_TO_SCORE=("$@")
fi

# ============================================================================
# Risk Scoring Functions
# ============================================================================

# Calculate ownership risk (0-40 points)
ownership_risk() {
    local file="$1"
    local owner_count=0

    if [ -f "$WHO_SCRIPT" ]; then
        local owner_output
        local exit_code

        # Capture output and exit code separately
        set +e
        owner_output=$(bash "$WHO_SCRIPT" "$file" 2>&1)
        exit_code=$?
        set -e

        case $exit_code in
            0)
                # Single owner
                owner_count=1
                ;;
            1)
                # Multiple owners - count them
                owner_count=$(echo "$owner_output" | grep -c "  - " || echo 2)
                ;;
            2)
                # No owner
                owner_count=0
                ;;
        esac
    fi

    case $owner_count in
        0) echo 0 ;;
        1) echo 10 ;;
        2) echo 25 ;;
        *) echo 40 ;;
    esac
}

# Calculate file type risk (0-30 points)
file_type_risk() {
    local file="$1"
    local filename
    filename=$(basename "$file")

    # Infrastructure files (highest risk)
    case "$filename" in
        justfile|Justfile|AGENTS.md|CLAUDE.md|INDEX.md|.chora/work-contexts.yaml)
            echo 30
            return
            ;;
    esac

    # Config files by extension
    case "$file" in
        *.yaml|*.yml|*.json|*.toml|*.ini|*.conf)
            echo 20
            return
            ;;
    esac

    # Source code
    case "$file" in
        *.py|*.sh|*.js|*.ts|*.go|*.rs|*.java|*.cpp|*.c|*.h)
            echo 10
            return
            ;;
    esac

    # Documentation
    case "$file" in
        *.md)
            echo 5
            return
            ;;
    esac

    # Default
    echo 5
}

# Calculate modification recency risk (0-20 points)
modification_risk() {
    local file="$1"

    if [ ! -f "$file" ]; then
        echo 0
        return
    fi

    # Get last modified time in seconds since epoch
    local mod_time
    if date --version 2>&1 | grep -q GNU; then
        # GNU date (Linux)
        mod_time=$(stat -c %Y "$file" 2>/dev/null || echo 0)
    else
        # BSD date (macOS)
        mod_time=$(stat -f %m "$file" 2>/dev/null || echo 0)
    fi

    local current_time
    current_time=$(date +%s)
    local age_seconds=$((current_time - mod_time))

    local age_hours=$((age_seconds / 3600))

    if [ "$age_hours" -lt 1 ]; then
        echo 20
    elif [ "$age_hours" -lt 24 ]; then
        echo 15
    elif [ "$age_hours" -lt 168 ]; then  # 1 week
        echo 10
    elif [ "$age_hours" -lt 720 ]; then  # 30 days
        echo 5
    else
        echo 0
    fi
}

# Calculate CODEOWNERS mismatch risk (0-10 points)
codeowners_risk() {
    local file="$1"

    # If no CODEOWNERS file, no risk
    if [ ! -f "$CODEOWNERS" ]; then
        echo 0
        return
    fi

    # Get work context owners
    local context_owners
    if [ -f "$WHO_SCRIPT" ]; then
        context_owners=$(bash "$WHO_SCRIPT" "$file" 2>&1 | grep "  - " | sed 's/  - //' | sed 's/ (.*//' || echo "")
    else
        echo 0
        return
    fi

    # If no context owners, no risk
    if [ -z "$context_owners" ]; then
        echo 0
        return
    fi

    # Check if file has CODEOWNERS entry
    # Simple grep check (not perfect, but works for most cases)
    if ! grep -q "$file" "$CODEOWNERS" 2>/dev/null; then
        # File not in CODEOWNERS
        echo 5
        return
    fi

    # File is in CODEOWNERS - assume low risk
    echo 0
}

# Calculate total risk score
calculate_risk_score() {
    local file="$1"

    local ownership_score
    ownership_score=$(ownership_risk "$file")

    local file_type_score
    file_type_score=$(file_type_risk "$file")

    local modification_score
    modification_score=$(modification_risk "$file")

    local codeowners_score
    codeowners_score=$(codeowners_risk "$file")

    local total=$((ownership_score + file_type_score + modification_score + codeowners_score))

    # Cap at 100
    if [ "$total" -gt 100 ]; then
        total=100
    fi

    echo "$total"
}

# Get risk level from score
get_risk_level() {
    local score="$1"

    if [ "$score" -lt 34 ]; then
        echo "LOW"
    elif [ "$score" -lt 67 ]; then
        echo "MEDIUM"
    else
        echo "HIGH"
    fi
}

# Get risk color code (for terminal output)
get_risk_color() {
    local level="$1"

    case "$level" in
        LOW) echo "🟢" ;;
        MEDIUM) echo "🟡" ;;
        HIGH) echo "🔴" ;;
        *) echo "⚪" ;;
    esac
}

# ============================================================================
# Main Scoring Logic
# ============================================================================

# Collect files to score
if [ "$SCORE_ALL" = true ]; then
    # Get all files from work contexts
    if [ ! -f "$CONTEXTS_FILE" ]; then
        echo "No work contexts registered"
        exit 0
    fi

    if command -v yq &> /dev/null; then
        # Extract all file patterns and expand them
        while IFS= read -r pattern; do
            [ -z "$pattern" ] && continue

            # Expand glob patterns
            if [[ "$pattern" == *"*"* ]]; then
                # Use find for glob expansion
                shopt -s nullglob globstar 2>/dev/null || true
                for expanded in $pattern; do
                    [ -f "$expanded" ] && FILES_TO_SCORE+=("$expanded")
                done
            else
                [ -f "$pattern" ] && FILES_TO_SCORE+=("$pattern")
            fi
        done < <(yq eval '.work_contexts[].files[]' "$CONTEXTS_FILE" 2>/dev/null | tr ',' '\n')
    else
        # Python fallback
        while IFS= read -r pattern; do
            [ -z "$pattern" ] && continue

            if [[ "$pattern" == *"*"* ]]; then
                shopt -s nullglob globstar 2>/dev/null || true
                for expanded in $pattern; do
                    [ -f "$expanded" ] && FILES_TO_SCORE+=("$expanded")
                done
            else
                [ -f "$pattern" ] && FILES_TO_SCORE+=("$pattern")
            fi
        done < <(python3 <<EOF 2>/dev/null || true
import yaml
with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f)
for ctx in data.get('work_contexts', []):
    for file_list in ctx.get('files', []):
        for file in file_list.split(','):
            print(file.strip())
EOF
)
    fi

    # Remove duplicates
    FILES_TO_SCORE=($(printf "%s\n" "${FILES_TO_SCORE[@]}" | sort -u))
fi

if [ ${#FILES_TO_SCORE[@]} -eq 0 ]; then
    echo "No files to score"
    echo "Usage: $0 [file1] [file2] ... OR $0 --all"
    exit 0
fi

# ============================================================================
# Score and Display Results
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Work Context Conflict Risk Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

printf "%-50s %6s  %-8s\n" "FILE" "SCORE" "RISK"
echo "────────────────────────────────────────────────────────────────"

for file in "${FILES_TO_SCORE[@]}"; do
    score=$(calculate_risk_score "$file")
    level=$(get_risk_level "$score")
    color=$(get_risk_color "$level")

    printf "%-50s %6d  %-8s %s\n" "$file" "$score" "$level" "$color"
done

echo ""
echo "Risk Levels:"
echo "  🟢 LOW (0-33):     Safe to edit"
echo "  🟡 MEDIUM (34-66): Coordinate before editing"
echo "  🔴 HIGH (67-100):  High conflict risk"
echo ""
echo "Next steps:"
echo "  - Check high-risk files: just who-is-working-on <file>"
echo "  - View dashboard: just work-dashboard"
echo "  - Coordinate with other contexts before editing high-risk files"
echo ""

exit 0
