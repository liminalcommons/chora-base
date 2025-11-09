#!/bin/bash
#
# SAP-007 Documentation Framework - Pre-commit Hook
#
# Purpose:
#     Runs SAP-007 structure validation before each git commit to prevent
#     documentation structure violations from being committed.
#
# Installation:
#     1. Copy this file to: .git/hooks/pre-commit
#        OR: Copy to .githooks/pre-commit and run: git config core.hooksPath .githooks
#     2. Make executable: chmod +x .git/hooks/pre-commit
#     3. Test: git commit -m "test" (should run validation)
#
# Bypass (use sparingly):
#     git commit --no-verify -m "reason for bypass"
#     (Document bypass reason in commit message)
#
# SAP-031 Integration:
#     This pre-commit hook implements SAP-031 (Discoverability-Based Enforcement)
#     Layer 2 (Pre-Commit Validation) for SAP-007 (Documentation Framework).
#
#     See: docs/skilled-awareness/discoverability-based-enforcement/
#
# =============================================================================

echo ""
echo "==================================================================="
echo "Running SAP-007 Documentation Framework validation..."
echo "==================================================================="
echo ""

# Find the validation script
# Adjust path if your project has a different structure
VALIDATION_SCRIPT="docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py"

# Alternative: If you've copied the validation script to scripts/
# VALIDATION_SCRIPT="scripts/validate-sap-007-structure.py"

# Check if validation script exists
if [ ! -f "$VALIDATION_SCRIPT" ]; then
    echo "[ERROR] SAP-007 validation script not found!"
    echo ""
    echo "Expected location: $VALIDATION_SCRIPT"
    echo ""
    echo "Please ensure the validation script is available."
    echo "You can find it in chora-base:"
    echo "  docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py"
    echo ""
    echo "Bypass this check (not recommended):"
    echo "  git commit --no-verify -m 'your message'"
    echo ""
    exit 1
fi

# Run validation script
python "$VALIDATION_SCRIPT"
VALIDATION_EXIT_CODE=$?

echo ""

# Check validation result
if [ $VALIDATION_EXIT_CODE -eq 0 ]; then
    echo "==================================================================="
    echo "[PASS] SAP-007 validation passed - proceeding with commit"
    echo "==================================================================="
    echo ""
    exit 0
else
    echo "==================================================================="
    echo "[FAIL] SAP-007 validation failed - commit BLOCKED"
    echo "==================================================================="
    echo ""
    echo "Your commit violates SAP-007 Documentation Framework structure."
    echo ""
    echo "Required actions:"
    echo "  1. Review validation errors above"
    echo "  2. Fix violations (move files to appropriate directories)"
    echo "  3. Use decision tree: docs/skilled-awareness/documentation-framework/decision-tree-template.md"
    echo "  4. Re-run validation: python $VALIDATION_SCRIPT"
    echo "  5. Try commit again"
    echo ""
    echo "Resources:"
    echo "  - SAP-007 Documentation: docs/skilled-awareness/documentation-framework/"
    echo "  - Decision Tree Template: docs/skilled-awareness/documentation-framework/decision-tree-template.md"
    echo "  - Enforcement Guide: docs/skilled-awareness/documentation-framework/adoption-blueprint.md (Level 3)"
    echo ""
    echo "Bypass (use only if you have a valid reason):"
    echo "  git commit --no-verify -m 'reason for bypassing SAP-007 validation'"
    echo ""
    echo "Note: Bypassing validation degrades documentation structure."
    echo "      Document your reason in the commit message."
    echo ""
    exit 1
fi
