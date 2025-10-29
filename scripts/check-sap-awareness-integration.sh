#!/bin/bash
# SAP Awareness Integration Checker
#
# Purpose: Quick pattern detection for AGENTS.md/CLAUDE.md integration in SAP adoption blueprints
# Scope: SIMPLE checks only - complex validation requires LLM-based audit (SAP_AWARENESS_INTEGRATION_CHECKLIST.md)
#
# Usage:
#   ./scripts/check-sap-awareness-integration.sh <sap-directory>
#   ./scripts/check-sap-awareness-integration.sh docs/skilled-awareness/testing-framework
#
# Exit codes:
#   0 - All basic patterns found (still requires full LLM audit for quality)
#   1 - Missing critical patterns
#   2 - Invalid usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Usage
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <sap-directory>"
    echo ""
    echo "Example:"
    echo "  $0 docs/skilled-awareness/testing-framework"
    echo ""
    exit 2
fi

SAP_DIR="$1"
BLUEPRINT="${SAP_DIR}/adoption-blueprint.md"

echo "==================================="
echo "SAP Awareness Integration Checker"
echo "==================================="
echo ""
echo "SAP Directory: $SAP_DIR"
echo "Blueprint: $BLUEPRINT"
echo ""

# Check if blueprint exists
if [ ! -f "$BLUEPRINT" ]; then
    echo -e "${RED}❌ FAIL: adoption-blueprint.md not found${NC}"
    echo ""
    echo "Expected: $BLUEPRINT"
    exit 1
fi

echo "✅ adoption-blueprint.md exists"
echo ""

# Initialize results
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

echo "Running pattern checks..."
echo "-----------------------------------"

# Check 1: Post-install section
echo -n "Check 1: Post-install section exists... "
if grep -q -i "post-install\|awareness enablement" "$BLUEPRINT"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "  → No 'post-install' or 'awareness enablement' section found"
    ((FAIL_COUNT++))
fi

# Check 2: AGENTS.md mentioned
echo -n "Check 2: AGENTS.md mentioned... "
if grep -q "AGENTS\.md" "$BLUEPRINT"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "  → 'AGENTS.md' not mentioned in blueprint"
    ((FAIL_COUNT++))
fi

# Check 3: Validation command (grep check)
echo -n "Check 3: Validation command present... "
if grep -q "grep.*AGENTS\.md" "$BLUEPRINT"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  WARN${NC}"
    echo "  → No validation command found (grep check)"
    ((WARN_COUNT++))
fi

# Check 4: Agent-executable guidance ("use Edit tool" or similar)
echo -n "Check 4: Agent-executable instructions... "
if grep -q -i "use edit tool\|use Edit\|For agents" "$BLUEPRINT"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  WARN${NC}"
    echo "  → No explicit agent-executable instructions found"
    ((WARN_COUNT++))
fi

echo ""
echo "==================================="
echo "Summary"
echo "==================================="
echo ""
echo "✅ Passed: $PASS_COUNT"
echo "⚠️  Warnings: $WARN_COUNT"
echo "❌ Failed: $FAIL_COUNT"
echo ""

# Final assessment
if [ $FAIL_COUNT -eq 0 ]; then
    if [ $WARN_COUNT -eq 0 ]; then
        echo -e "${GREEN}✅ RESULT: All basic patterns found${NC}"
        echo ""
        echo "⚠️  IMPORTANT: This script only checks for basic patterns."
        echo "   Full quality audit requires LLM-based review using:"
        echo "   docs/dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md"
        echo ""
        exit 0
    else
        echo -e "${YELLOW}⚠️  RESULT: Basic patterns found with warnings${NC}"
        echo ""
        echo "Recommended action:"
        echo "  - Review warnings above"
        echo "  - Run full LLM audit: SAP_AWARENESS_INTEGRATION_CHECKLIST.md"
        echo ""
        exit 0
    fi
else
    echo -e "${RED}❌ RESULT: Missing critical awareness integration patterns${NC}"
    echo ""
    echo "Required actions:"
    echo "  1. Review failed checks above"
    echo "  2. Add missing post-install awareness enablement section"
    echo "  3. Include AGENTS.md update instructions"
    echo "  4. Run full LLM audit: SAP_AWARENESS_INTEGRATION_CHECKLIST.md"
    echo ""
    echo "Reference examples:"
    echo "  - SAP-000: docs/skilled-awareness/sap-framework/adoption-blueprint.md"
    echo "  - SAP-001: docs/skilled-awareness/inbox/adoption-blueprint.md"
    echo ""
    exit 1
fi
