#!/usr/bin/env bash
# detect-conflicts.sh - Find files edited by multiple work contexts
#
# Usage: ./detect-conflicts.sh
#
# Exit codes:
#   0: No conflicts detected
#   1: Conflicts detected

set -euo pipefail

CONTEXTS_FILE=".chora/work-contexts.yaml"

if [ ! -f "$CONTEXTS_FILE" ]; then
    echo "No work contexts registered (missing $CONTEXTS_FILE)" >&2
    exit 0
fi

# Check if yq is available (preferred)
if command -v yq &> /dev/null; then
    # Extract all file patterns, count occurrences
    FILE_PATTERNS=$(yq eval '.work_contexts[].files[]' "$CONTEXTS_FILE" 2>/dev/null | sort)

    # Find duplicates (files referenced by multiple contexts)
    CONFLICTS=$(echo "$FILE_PATTERNS" | uniq -d)

    if [ -z "$CONFLICTS" ]; then
        exit 0
    else
        echo "$CONFLICTS"
        exit 1
    fi
else
    # Fallback: Use Python for YAML parsing
    python3 <<EOF
import sys
import yaml
from collections import Counter

try:
    with open("$CONTEXTS_FILE", "r") as f:
        data = yaml.safe_load(f)

    contexts = data.get("work_contexts", [])
    file_counts = Counter()

    # Count how many contexts reference each file pattern
    for ctx in contexts:
        files = ctx.get("files", [])
        for file_pattern in files:
            file_counts[file_pattern] += 1

    # Find patterns referenced by multiple contexts
    conflicts = [pattern for pattern, count in file_counts.items() if count > 1]

    if not conflicts:
        sys.exit(0)
    else:
        for conflict in conflicts:
            print(conflict)
        sys.exit(1)

except FileNotFoundError:
    # No contexts file = no conflicts
    sys.exit(0)
except Exception as e:
    print(f"Error parsing work contexts: {e}", file=sys.stderr)
    sys.exit(1)
EOF
fi
