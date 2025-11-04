#!/usr/bin/env bash
# Script: propagate-trace-id.sh
# Purpose: Propagate CHORA_TRACE_ID from coordination request to documentation and metrics
# Usage: ./scripts/propagate-trace-id.sh <trace_id> <doc_file>
# Example: ./scripts/propagate-trace-id.sh mcp-taskmgr-2025-003 docs/user-docs/how-to/create-task.md
#
# Part of GAP-001 resolution: End-to-end CHORA_TRACE_ID propagation
# See: docs/project-docs/workflow-continuity-gap-report.md (GAP-001)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
error() { echo -e "${RED}ERROR: $1${NC}" >&2; }
success() { echo -e "${GREEN}SUCCESS: $1${NC}"; }
info() { echo -e "${YELLOW}INFO: $1${NC}"; }

# Validate arguments
if [ $# -lt 2 ]; then
    error "Usage: $0 <trace_id> <doc_file>"
    echo "Example: $0 mcp-taskmgr-2025-003 docs/user-docs/how-to/create-task.md"
    exit 1
fi

TRACE_ID="$1"
DOC_FILE="$2"

# Validate trace_id format: {domain}-{yyyy}-{nnn}
if ! [[ "$TRACE_ID" =~ ^[a-z0-9-]+-[0-9]{4}-[0-9]{3}$ ]]; then
    error "Invalid trace_id format: $TRACE_ID"
    echo "Expected format: {domain}-{yyyy}-{nnn} (e.g., mcp-taskmgr-2025-003)"
    exit 1
fi

# Check if doc file exists
if [ ! -f "$DOC_FILE" ]; then
    error "Document file not found: $DOC_FILE"
    exit 1
fi

# Check if file has frontmatter
if ! grep -q "^---$" "$DOC_FILE"; then
    error "Document does not have YAML frontmatter: $DOC_FILE"
    echo "Add frontmatter first (see SAP-007 documentation-framework)"
    exit 1
fi

# Check if trace_id already exists
if grep -q "^trace_id:" "$DOC_FILE"; then
    EXISTING_TRACE=$(grep "^trace_id:" "$DOC_FILE" | awk '{print $2}')
    if [ "$EXISTING_TRACE" = "$TRACE_ID" ]; then
        info "Trace ID already set to $TRACE_ID in $DOC_FILE"
        exit 0
    else
        error "Document already has different trace_id: $EXISTING_TRACE"
        echo "Cannot overwrite with $TRACE_ID. Verify this is correct."
        exit 1
    fi
fi

# Find the line number where frontmatter ends (second occurrence of "---")
FRONTMATTER_END=$(grep -n "^---$" "$DOC_FILE" | head -2 | tail -1 | cut -d: -f1)

if [ -z "$FRONTMATTER_END" ]; then
    error "Could not find end of frontmatter in $DOC_FILE"
    exit 1
fi

# Insert trace_id before the closing "---" of frontmatter
# We'll add it after last_updated if it exists, otherwise before the closing ---
if grep -q "^last_updated:" "$DOC_FILE"; then
    # Find last_updated line number
    LAST_UPDATED_LINE=$(grep -n "^last_updated:" "$DOC_FILE" | cut -d: -f1)
    INSERT_LINE=$((LAST_UPDATED_LINE + 1))
else
    # Insert before closing ---
    INSERT_LINE=$FRONTMATTER_END
fi

# Create backup
cp "$DOC_FILE" "$DOC_FILE.bak"

# Insert trace_id
{
    head -n $((INSERT_LINE - 1)) "$DOC_FILE.bak"
    echo "trace_id: $TRACE_ID"
    tail -n +$INSERT_LINE "$DOC_FILE.bak"
} > "$DOC_FILE"

# Verify insertion
if grep -q "^trace_id: $TRACE_ID$" "$DOC_FILE"; then
    success "Added trace_id to $DOC_FILE"
    rm "$DOC_FILE.bak"

    # Show the updated frontmatter
    info "Updated frontmatter:"
    sed -n '1,/^---$/p' "$DOC_FILE" | tail -n +2 | head -n -1
else
    error "Failed to insert trace_id"
    mv "$DOC_FILE.bak" "$DOC_FILE"
    exit 1
fi

# Provide guidance on next steps
info "Next steps for end-to-end traceability:"
echo "  1. Add trace_id to SAP-013 metrics when tracking this work:"
echo "     ClaudeMetric(session_id='...', trace_id='$TRACE_ID', ...)"
echo "  2. Reference trace_id in commit messages:"
echo "     git commit -m 'feat: implement feature [trace: $TRACE_ID]'"
echo "  3. Query metrics by trace_id for lead time analysis:"
echo "     grep '$TRACE_ID' metrics/*.csv"

exit 0
