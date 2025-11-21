#!/usr/bin/env bash
# who-is-working-on.sh - Query which work context is editing a file
#
# Usage: ./who-is-working-on.sh <file-path>
# Example: ./who-is-working-on.sh justfile
#
# Exit codes:
#   0: File owned by exactly 1 context
#   1: File owned by multiple contexts (conflict)
#   2: File not owned by any context

set -euo pipefail

FILE="${1:-}"
CONTEXTS_FILE=".chora/work-contexts.yaml"

if [ -z "$FILE" ]; then
    echo "Usage: $0 <file-path>" >&2
    echo "Example: $0 justfile" >&2
    exit 3
fi

if [ ! -f "$CONTEXTS_FILE" ]; then
    echo "No work contexts registered (missing $CONTEXTS_FILE)" >&2
    exit 2
fi

# Check if yq is available (preferred)
if command -v yq &> /dev/null; then
    # Use yq for YAML parsing
    MATCHES=$(yq eval ".work_contexts[] | select(.files[] | test(\"$FILE\")) | .id" "$CONTEXTS_FILE" 2>/dev/null || echo "")

    if [ -z "$MATCHES" ]; then
        echo "No context editing $FILE"
        exit 2
    fi

    # Count matches
    MATCH_COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')

    if [ "$MATCH_COUNT" -eq 1 ]; then
        # Single owner
        CONTEXT_ID="$MATCHES"
        CONTEXT_TYPE=$(yq eval ".work_contexts[] | select(.id == \"$CONTEXT_ID\") | .type" "$CONTEXTS_FILE")
        echo "$CONTEXT_ID ($CONTEXT_TYPE)"
        exit 0
    else
        # Multiple owners (conflict)
        echo "$FILE is edited by multiple contexts: [CONFLICT]"
        echo "$MATCHES" | while read -r ctx_id; do
            ctx_type=$(yq eval ".work_contexts[] | select(.id == \"$ctx_id\") | .type" "$CONTEXTS_FILE")
            echo "  - $ctx_id ($ctx_type)"
        done
        exit 1
    fi
else
    # Fallback: Use Python for YAML parsing
    python3 <<EOF
import sys
import yaml
import fnmatch

try:
    with open("$CONTEXTS_FILE", "r") as f:
        data = yaml.safe_load(f)

    contexts = data.get("work_contexts", [])
    matches = []

    for ctx in contexts:
        ctx_id = ctx.get("id", "unknown")
        ctx_type = ctx.get("type", "unknown")
        files = ctx.get("files", [])

        for pattern in files:
            if fnmatch.fnmatch("$FILE", pattern) or "$FILE" in pattern:
                matches.append((ctx_id, ctx_type))
                break

    if not matches:
        print("No context editing $FILE")
        sys.exit(2)
    elif len(matches) == 1:
        ctx_id, ctx_type = matches[0]
        print(f"{ctx_id} ({ctx_type})")
        sys.exit(0)
    else:
        print("$FILE is edited by multiple contexts: [CONFLICT]")
        for ctx_id, ctx_type in matches:
            print(f"  - {ctx_id} ({ctx_type})")
        sys.exit(1)

except FileNotFoundError:
    print("No work contexts registered (missing $CONTEXTS_FILE)", file=sys.stderr)
    sys.exit(2)
except Exception as e:
    print(f"Error parsing work contexts: {e}", file=sys.stderr)
    sys.exit(3)
EOF
fi
