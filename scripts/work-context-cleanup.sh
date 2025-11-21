#!/usr/bin/env bash
# Work Context Cleanup Script
#
# Remove stale or specific work contexts from the registry.
# Part of chora.coordination.work_context (SAP L3 Phase 1.2)
#
# Usage:
#   work-context-cleanup.sh [context-id] [--ttl HOURS]
#
# Arguments:
#   context-id : (Optional) Specific context ID to remove
#   --ttl      : (Optional) Time-to-live in hours (default: 24)
#
# Examples:
#   work-context-cleanup.sh                    # Clean stale contexts (24h TTL)
#   work-context-cleanup.sh --ttl 48           # Clean contexts older than 48h
#   work-context-cleanup.sh tab-1              # Remove specific context
#
# Exit Codes:
#   0 : Success (contexts cleaned or none to clean)
#   1 : Error (invalid arguments, git failure, etc.)

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CONTEXT_ID="${1:-}"
TTL_HOURS=24
CONTEXTS_FILE=".chora/work-contexts.yaml"
ARCHIVE_FILE=".chora/work-contexts-archive.yaml"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Parse --ttl flag
if [ "$CONTEXT_ID" = "--ttl" ]; then
    if [ -z "${2:-}" ]; then
        echo "Error: --ttl requires a value in hours"
        exit 1
    fi
    TTL_HOURS="$2"
    CONTEXT_ID=""
elif [ -n "$CONTEXT_ID" ] && [ "${2:-}" = "--ttl" ]; then
    if [ -z "${3:-}" ]; then
        echo "Error: --ttl requires a value in hours"
        exit 1
    fi
    TTL_HOURS="$3"
fi

# ============================================================================
# Validation
# ============================================================================

if [ ! -f "$CONTEXTS_FILE" ]; then
    echo "No work contexts registered (file not found: $CONTEXTS_FILE)"
    exit 0
fi

# Ensure archive file exists
mkdir -p .chora
if [ ! -f "$ARCHIVE_FILE" ]; then
    echo "archived_contexts:" > "$ARCHIVE_FILE"
fi

# ============================================================================
# Cleanup Functions
# ============================================================================

# Calculate if a timestamp is stale (older than TTL_HOURS)
is_stale() {
    local activity_time="$1"
    local ttl_seconds=$((TTL_HOURS * 3600))

    # Convert ISO 8601 timestamp to epoch seconds
    if date --version 2>&1 | grep -q GNU; then
        # GNU date (Linux)
        activity_epoch=$(date -d "$activity_time" +%s 2>/dev/null || echo 0)
    else
        # BSD date (macOS)
        activity_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$activity_time" +%s 2>/dev/null || echo 0)
    fi

    current_epoch=$(date +%s)
    age_seconds=$((current_epoch - activity_epoch))

    if [ "$age_seconds" -gt "$ttl_seconds" ]; then
        return 0  # Stale
    else
        return 1  # Not stale
    fi
}

# Archive a context before removing it
archive_context() {
    local ctx_id="$1"
    local ctx_type="$2"
    local ctx_branch="$3"
    local ctx_started="$4"
    local ctx_activity="$5"
    local ctx_files="$6"

    echo "Archiving context $ctx_id..."

    # Append to archive file
    {
        echo "  - id: $ctx_id"
        echo "    type: $ctx_type"
        echo "    branch: $ctx_branch"
        echo "    started_at: $ctx_started"
        echo "    last_activity: $ctx_activity"
        echo "    archived_at: $TIMESTAMP"
        echo "    files:"
        # Parse file list (comma-separated)
        IFS=',' read -ra FILES <<< "$ctx_files"
        for file in "${FILES[@]}"; do
            file=$(echo "$file" | xargs)  # Trim whitespace
            echo "      - \"$file\""
        done
    } >> "$ARCHIVE_FILE"
}

# ============================================================================
# Manual Cleanup (Specific Context ID)
# ============================================================================

if [ -n "$CONTEXT_ID" ]; then
    echo "Removing context: $CONTEXT_ID"
    echo ""

    # Check if context exists
    CONTEXT_EXISTS=false
    if grep -q "id: $CONTEXT_ID" "$CONTEXTS_FILE" 2>/dev/null; then
        CONTEXT_EXISTS=true
    fi

    if [ "$CONTEXT_EXISTS" = false ]; then
        echo "⚠️  Context $CONTEXT_ID not found in registry"
        exit 0
    fi

    # Extract context details for archiving
    if command -v yq &> /dev/null; then
        CTX_TYPE=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .type" "$CONTEXTS_FILE")
        CTX_BRANCH=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .branch" "$CONTEXTS_FILE")
        CTX_STARTED=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .started_at" "$CONTEXTS_FILE")
        CTX_ACTIVITY=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .last_activity" "$CONTEXTS_FILE")
        CTX_FILES=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .files | join(\",\")" "$CONTEXTS_FILE")
    else
        # Python fallback
        read -r CTX_TYPE CTX_BRANCH CTX_STARTED CTX_ACTIVITY CTX_FILES <<< $(python3 <<EOF
import yaml
with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f)

for ctx in data.get('work_contexts', []):
    if ctx.get('id') == "$CONTEXT_ID":
        print(ctx.get('type', 'unknown'), ctx.get('branch', 'unknown'), ctx.get('started_at', ''), ctx.get('last_activity', ''), ','.join(ctx.get('files', [])))
        break
EOF
)
    fi

    # Archive context
    archive_context "$CONTEXT_ID" "$CTX_TYPE" "$CTX_BRANCH" "$CTX_STARTED" "$CTX_ACTIVITY" "$CTX_FILES"

    # Remove from active registry
    if command -v yq &> /dev/null; then
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

    echo "✅ Removed context $CONTEXT_ID"
    echo "   Archived to: $ARCHIVE_FILE"
    echo ""
    exit 0
fi

# ============================================================================
# Automatic Cleanup (Stale Contexts)
# ============================================================================

echo "Cleaning stale work contexts (TTL: ${TTL_HOURS}h)..."
echo ""

CLEANED_COUNT=0
STALE_CONTEXTS=()

# Read all contexts and check staleness
if command -v yq &> /dev/null; then
    # Use yq
    CONTEXT_IDS=$(yq eval '.work_contexts[].id' "$CONTEXTS_FILE" 2>/dev/null || echo "")

    if [ -n "$CONTEXT_IDS" ]; then
        while IFS= read -r ctx_id; do
            [ -z "$ctx_id" ] && continue

            ctx_activity=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .last_activity" "$CONTEXTS_FILE")

            if is_stale "$ctx_activity"; then
                STALE_CONTEXTS+=("$ctx_id")
            fi
        done <<< "$CONTEXT_IDS"
    fi
else
    # Python fallback
    STALE_CONTEXTS=($(python3 <<EOF
import yaml
from datetime import datetime, timedelta, timezone

with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f)

ttl_seconds = $TTL_HOURS * 3600
current_time = datetime.now(timezone.utc)

for ctx in data.get('work_contexts', []):
    activity_str = ctx.get('last_activity', '')
    if not activity_str:
        continue

    try:
        activity_time = datetime.fromisoformat(activity_str.replace('Z', '+00:00'))
        age_seconds = (current_time - activity_time).total_seconds()

        if age_seconds > ttl_seconds:
            print(ctx.get('id'))
    except:
        pass
EOF
))
fi

# Clean stale contexts
if [ ${#STALE_CONTEXTS[@]} -eq 0 ]; then
    echo "✅ No stale contexts found (all activity within ${TTL_HOURS}h)"
    exit 0
fi

echo "Found ${#STALE_CONTEXTS[@]} stale context(s):"
for ctx_id in "${STALE_CONTEXTS[@]}"; do
    echo "  - $ctx_id"
done
echo ""

for ctx_id in "${STALE_CONTEXTS[@]}"; do
    # Extract context details for archiving
    if command -v yq &> /dev/null; then
        CTX_TYPE=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .type" "$CONTEXTS_FILE")
        CTX_BRANCH=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .branch" "$CONTEXTS_FILE")
        CTX_STARTED=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .started_at" "$CONTEXTS_FILE")
        CTX_ACTIVITY=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .last_activity" "$CONTEXTS_FILE")
        CTX_FILES=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .files | join(\",\")" "$CONTEXTS_FILE")
    else
        # Python fallback
        read -r CTX_TYPE CTX_BRANCH CTX_STARTED CTX_ACTIVITY CTX_FILES <<< $(python3 <<EOF
import yaml
with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f)

for ctx in data.get('work_contexts', []):
    if ctx.get('id') == "$ctx_id":
        print(ctx.get('type', 'unknown'), ctx.get('branch', 'unknown'), ctx.get('started_at', ''), ctx.get('last_activity', ''), ','.join(ctx.get('files', [])))
        break
EOF
)
    fi

    # Archive context
    archive_context "$ctx_id" "$CTX_TYPE" "$CTX_BRANCH" "$CTX_STARTED" "$CTX_ACTIVITY" "$CTX_FILES"

    # Remove from active registry
    if command -v yq &> /dev/null; then
        yq eval "del(.work_contexts[] | select(.id == \"$ctx_id\"))" -i "$CONTEXTS_FILE"
    else
        # Python fallback
        python3 <<EOF
import yaml
with open("$CONTEXTS_FILE", 'r') as f:
    data = yaml.safe_load(f) or {}

work_contexts = data.get('work_contexts', [])
work_contexts = [ctx for ctx in work_contexts if ctx.get('id') != "$ctx_id"]
data['work_contexts'] = work_contexts

with open("$CONTEXTS_FILE", 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
EOF
    fi

    CLEANED_COUNT=$((CLEANED_COUNT + 1))
done

echo "✅ Cleaned $CLEANED_COUNT stale context(s)"
echo "   Archived to: $ARCHIVE_FILE"
echo ""
echo "Next steps:"
echo "  - View remaining contexts: just work-dashboard"
echo "  - Restore archived context: Manually edit $ARCHIVE_FILE and $CONTEXTS_FILE"
echo ""

# ============================================================================
# A-MEM Event Logging (SAP-010 integration)
# ============================================================================

if [ -f "scripts/lib/emit-event.sh" ] && [ "$CLEANED_COUNT" -gt 0 ]; then
    source scripts/lib/emit-event.sh

    # Build context JSON with cleaned contexts
    CLEANED_IDS_JSON=$(printf '%s\n' "${STALE_CONTEXTS[@]}" | jq -R . | jq -s .)

    CONTEXT_JSON=$(cat <<EOF
{
  "cleaned_count": $CLEANED_COUNT,
  "ttl_hours": $TTL_HOURS,
  "cleaned_context_ids": $CLEANED_IDS_JSON,
  "archive_file": "$ARCHIVE_FILE",
  "operation": "$OPERATION"
}
EOF
)

    emit_event "work_contexts_cleaned" \
               "Cleaned $CLEANED_COUNT stale work context(s) with TTL ${TTL_HOURS}h" \
               "work-context-cleanup-$(date +%Y%m%d)" \
               "$CONTEXT_JSON"
fi

exit 0
