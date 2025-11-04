#!/usr/bin/env bash
# Script: generate-doc-from-coordination.sh
# Purpose: Auto-generate documentation skeleton from SAP-001 coordination requests
# Usage: ./scripts/generate-doc-from-coordination.sh <coordination_file> <output_doc>
# Example: ./scripts/generate-doc-from-coordination.sh inbox/incoming/coordination/COORD-2025-042.json docs/user-docs/how-to/create-task.md
#
# Part of GAP-002 resolution: Manual Coordination → Documentation Handoff
# See: docs/project-docs/workflow-continuity-gap-report.md (GAP-002)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
error() { echo -e "${RED}ERROR: $1${NC}" >&2; }
success() { echo -e "${GREEN}SUCCESS: $1${NC}"; }
info() { echo -e "${YELLOW}INFO: $1${NC}"; }
section() { echo -e "${BLUE}$1${NC}"; }

# Validate arguments
if [ $# -lt 2 ]; then
    error "Usage: $0 <coordination_file> <output_doc>"
    echo "Example: $0 inbox/incoming/coordination/COORD-2025-042.json docs/user-docs/how-to/create-task.md"
    exit 1
fi

COORD_FILE="$1"
OUTPUT_DOC="$2"

# Check if coordination file exists
if [ ! -f "$COORD_FILE" ]; then
    error "Coordination file not found: $COORD_FILE"
    exit 1
fi

# Check if output file already exists
if [ -f "$OUTPUT_DOC" ]; then
    error "Output document already exists: $OUTPUT_DOC"
    echo "Remove it first or choose a different path"
    exit 1
fi

# Ensure jq is available for JSON parsing
if ! command -v jq &> /dev/null; then
    error "jq is required but not installed"
    echo "Install with: sudo apt-get install jq (Ubuntu) or brew install jq (Mac)"
    exit 1
fi

# Extract fields from coordination request
TRACE_ID=$(jq -r '.trace_id // empty' "$COORD_FILE")
TITLE=$(jq -r '.title // empty' "$COORD_FILE")
DESCRIPTION=$(jq -r '.description // empty' "$COORD_FILE")
DOC_OUTLINE=$(jq -r '.documentation_outline // empty' "$COORD_FILE")
COORD_TYPE=$(jq -r '.type // "coordination_request"' "$COORD_FILE")

# Validate required fields
if [ -z "$TITLE" ]; then
    error "Coordination request missing 'title' field"
    exit 1
fi

# Detect Diataxis type based on coordination type and title
suggest_diataxis_type() {
    local title_lower=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]')
    local desc_lower=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]')

    # How-To patterns
    if [[ "$title_lower" =~ ^how\ to ]] || [[ "$title_lower" =~ guide$ ]] || [[ "$desc_lower" =~ solve|implement|create|configure ]]; then
        echo "how-to"
    # Tutorial patterns
    elif [[ "$title_lower" =~ tutorial|learn|introduction|getting\ started ]] || [[ "$desc_lower" =~ step-by-step|lesson ]]; then
        echo "tutorial"
    # Reference patterns
    elif [[ "$title_lower" =~ api|schema|reference|specification ]] || [[ "$desc_lower" =~ parameters|fields|options ]]; then
        echo "reference"
    # Explanation patterns
    elif [[ "$title_lower" =~ why|rationale|concept|architecture ]] || [[ "$desc_lower" =~ understand|explain|design ]]; then
        echo "explanation"
    else
        # Default based on coordination type
        if [ "$COORD_TYPE" = "strategic_proposal" ]; then
            echo "explanation"
        else
            echo "how-to"
        fi
    fi
}

DOC_TYPE=$(suggest_diataxis_type)

# Suggest audience based on title/description
suggest_audience() {
    local title_lower=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]')
    local desc_lower=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]')

    if [[ "$title_lower" =~ beginner|introduction|getting\ started|first ]] || [[ "$desc_lower" =~ beginner|new\ user ]]; then
        echo "beginner"
    elif [[ "$title_lower" =~ advanced|expert ]] || [[ "$desc_lower" =~ advanced|expert ]]; then
        echo "advanced"
    elif [[ "$title_lower" =~ maintainer|internal ]] || [[ "$desc_lower" =~ maintainer ]]; then
        echo "maintainer"
    else
        echo "all"
    fi
}

AUDIENCE=$(suggest_audience)

# Create output directory if needed
OUTPUT_DIR=$(dirname "$OUTPUT_DOC")
mkdir -p "$OUTPUT_DIR"

# Generate frontmatter
CURRENT_DATE=$(date +%Y-%m-%d)

# Generate documentation skeleton
cat > "$OUTPUT_DOC" <<EOF
---
title: $TITLE
type: $DOC_TYPE
status: draft
audience: $AUDIENCE
last_updated: $CURRENT_DATE
EOF

# Add trace_id if present
if [ -n "$TRACE_ID" ]; then
    echo "trace_id: $TRACE_ID" >> "$OUTPUT_DOC"
fi

cat >> "$OUTPUT_DOC" <<EOF
---

# $TITLE

## Overview

$DESCRIPTION

---

EOF

# Add outline sections if provided
if [ -n "$DOC_OUTLINE" ] && [ "$DOC_OUTLINE" != "null" ]; then
    info "Using documentation outline from coordination request..."
    echo "$DOC_OUTLINE" >> "$OUTPUT_DOC"
    echo "" >> "$OUTPUT_DOC"
else
    # Generate default sections based on Diataxis type
    case "$DOC_TYPE" in
        "how-to")
            cat >> "$OUTPUT_DOC" <<'EOF'
## Prerequisites

Before you begin, ensure you have:
- [ ] TODO: List prerequisites

---

## Steps

### Step 1: TODO

TODO: Describe first step

```bash
# TODO: Add command or code example
```

### Step 2: TODO

TODO: Describe second step

---

## Verification

TODO: How to verify the solution works

```bash
# TODO: Add verification command
```

---

## Troubleshooting

**Problem**: TODO
**Solution**: TODO

---

## Related Documentation

- TODO: Link to related docs
EOF
            ;;
        "tutorial")
            cat >> "$OUTPUT_DOC" <<'EOF'
## Learning Objectives

By the end of this tutorial, you will:
- [ ] TODO: Learning objective 1
- [ ] TODO: Learning objective 2

---

## Prerequisites

- TODO: List prerequisites

---

## Lesson 1: TODO

TODO: First lesson with step-by-step instructions

```bash
# TODO: Add example
```

**Expected Output**:
```
TODO: Show expected output
```

---

## Lesson 2: TODO

TODO: Second lesson

---

## Summary

TODO: Recap what was learned

---

## Next Steps

- TODO: Suggest next tutorials or guides
EOF
            ;;
        "reference")
            cat >> "$OUTPUT_DOC" <<'EOF'
## Synopsis

TODO: Brief description of what this reference covers

---

## Fields / Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| TODO  | TODO | TODO     | TODO        |

---

## Examples

### Example 1: TODO

```bash
# TODO: Add example
```

---

## Related References

- TODO: Link to related references
EOF
            ;;
        "explanation")
            cat >> "$OUTPUT_DOC" <<'EOF'
## Context

TODO: Provide background and context

---

## Rationale

TODO: Explain the "why" behind design decisions

---

## Trade-offs

**Approach A**:
- Pros: TODO
- Cons: TODO

**Approach B**:
- Pros: TODO
- Cons: TODO

**Decision**: TODO

---

## Related Concepts

- TODO: Link to related explanations
EOF
            ;;
    esac
fi

# Add footer
cat >> "$OUTPUT_DOC" <<EOF

---

**Generated from**: [$COORD_FILE]($COORD_FILE)
**Trace ID**: ${TRACE_ID:-N/A}
**Auto-generated on**: $CURRENT_DATE
EOF

success "Generated documentation skeleton: $OUTPUT_DOC"
echo ""
section "Document Details:"
echo "  Type: $DOC_TYPE"
echo "  Audience: $AUDIENCE"
echo "  Trace ID: ${TRACE_ID:-N/A}"
echo "  Status: draft"
echo ""
info "Next steps:"
echo "  1. Review and fill in TODOs in $OUTPUT_DOC"
echo "  2. Add code examples and expected outputs"
echo "  3. Update status from 'draft' to 'current' when ready"
if [ -n "$TRACE_ID" ]; then
    echo "  4. Track metrics with trace_id: $TRACE_ID"
fi

exit 0
