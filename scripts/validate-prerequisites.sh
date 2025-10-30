#!/usr/bin/env bash
# validate-prerequisites.sh - Pre-flight validation for chora-base onboarding
#
# Purpose: Catch prerequisite issues before install-sap.py runs
# Exit codes: 0 = PASS, 1 = FAIL
#
# Usage:
#   bash scripts/validate-prerequisites.sh
#
# Based on: COORD-003 Sprint 1 requirements
# Target: Catch 90%+ of prerequisite issues before installation failure

set -euo pipefail

#############################################################################
# Colors and Output Helpers
#############################################################################

if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    BOLD=''
    NC=''
fi

print_header() {
    echo ""
    echo -e "${BLUE}${BOLD}=========================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}=========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_failure() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

#############################################################################
# Validation State
#############################################################################

CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0
VALIDATION_FAILED=0

#############################################################################
# Validation Functions
#############################################################################

validate_python() {
    print_info "Checking Python installation..."

    if ! command -v python3 &> /dev/null; then
        print_failure "Python 3 not found in PATH"
        print_info "    Install Python 3.8+ from: https://www.python.org/downloads/"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 8 ]]; then
        print_failure "Python $PYTHON_VERSION found (requires 3.8+)"
        print_info "    Upgrade Python from: https://www.python.org/downloads/"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    print_success "Python $PYTHON_VERSION (OK)"
    ((CHECKS_PASSED++))
    return 0
}

validate_git() {
    print_info "Checking Git installation..."

    if ! command -v git &> /dev/null; then
        print_failure "Git not found in PATH"
        print_info "    Install Git from: https://git-scm.com/downloads"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    GIT_VERSION=$(git --version 2>&1 | awk '{print $3}')
    GIT_MAJOR=$(echo "$GIT_VERSION" | cut -d. -f1)

    if [[ "$GIT_MAJOR" -lt 2 ]]; then
        print_warning "Git $GIT_VERSION found (recommend 2.0+)"
        print_info "    Consider upgrading from: https://git-scm.com/downloads"
        ((CHECKS_WARNING++))
    else
        print_success "Git $GIT_VERSION (OK)"
        ((CHECKS_PASSED++))
    fi

    return 0
}

validate_directory_structure() {
    print_info "Checking chora-base directory structure..."

    local missing_dirs=()
    local expected_dirs=(
        "docs"
        "docs/skilled-awareness"
        "scripts"
    )

    for dir in "${expected_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            missing_dirs+=("$dir")
        fi
    done

    if [[ ${#missing_dirs[@]} -gt 0 ]]; then
        print_failure "Missing required directories:"
        for dir in "${missing_dirs[@]}"; do
            print_info "    Missing: $dir"
        done
        print_info "    Are you running from chora-base root directory?"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    print_success "Directory structure (OK)"
    ((CHECKS_PASSED++))
    return 0
}

validate_sap_catalog() {
    print_info "Checking SAP catalog..."

    if [[ ! -f "sap-catalog.json" ]]; then
        print_failure "sap-catalog.json not found in root directory"
        print_info "    Expected file: sap-catalog.json"
        print_info "    Are you in the chora-base root directory?"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    # Validate JSON syntax
    if ! python3 -c "import json; json.load(open('sap-catalog.json'))" 2>/dev/null; then
        print_failure "sap-catalog.json has invalid JSON syntax"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    print_success "SAP catalog (OK)"
    ((CHECKS_PASSED++))
    return 0
}

validate_disk_space() {
    print_info "Checking disk space..."

    # Get available space in MB (works on macOS and Linux)
    if [[ "$(uname)" == "Darwin" ]]; then
        AVAILABLE_KB=$(df -k . | tail -1 | awk '{print $4}')
    else
        AVAILABLE_KB=$(df -k . | tail -1 | awk '{print $4}')
    fi

    AVAILABLE_MB=$((AVAILABLE_KB / 1024))

    if [[ "$AVAILABLE_MB" -lt 100 ]]; then
        print_warning "Low disk space: ${AVAILABLE_MB}MB available (recommend 100MB+)"
        print_info "    SAP installation typically uses 50-100MB"
        ((CHECKS_WARNING++))
    else
        print_success "Disk space: ${AVAILABLE_MB}MB available (OK)"
        ((CHECKS_PASSED++))
    fi

    return 0
}

validate_write_permissions() {
    print_info "Checking write permissions..."

    local test_dirs=(
        "docs/skilled-awareness"
        "."
    )

    local permission_errors=()

    for dir in "${test_dirs[@]}"; do
        if [[ ! -w "$dir" ]]; then
            permission_errors+=("$dir")
        fi
    done

    if [[ ${#permission_errors[@]} -gt 0 ]]; then
        print_failure "Insufficient write permissions:"
        for dir in "${permission_errors[@]}"; do
            print_info "    No write access: $dir"
        done
        print_info "    Check file permissions with: ls -la"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    print_success "Write permissions (OK)"
    ((CHECKS_PASSED++))
    return 0
}

validate_install_script() {
    print_info "Checking install-sap.py script..."

    if [[ ! -f "scripts/install-sap.py" ]]; then
        print_failure "scripts/install-sap.py not found"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    if [[ ! -x "scripts/install-sap.py" ]]; then
        print_warning "scripts/install-sap.py not executable (fixable with: chmod +x)"
        ((CHECKS_WARNING++))
    fi

    # Test if script can be parsed by Python
    if ! python3 -m py_compile scripts/install-sap.py 2>/dev/null; then
        print_failure "scripts/install-sap.py has syntax errors"
        ((CHECKS_FAILED++))
        VALIDATION_FAILED=1
        return 1
    fi

    print_success "install-sap.py script (OK)"
    ((CHECKS_PASSED++))
    return 0
}

validate_optional_yaml() {
    print_info "Checking optional PyYAML (for custom .chorabase files)..."

    if python3 -c "import yaml" 2>/dev/null; then
        print_success "PyYAML available (OK)"
        ((CHECKS_PASSED++))
    else
        print_warning "PyYAML not installed (optional - needed for custom .chorabase files)"
        print_info "    Install with: pip install PyYAML"
        print_info "    Not required for standard SAP set installation"
        ((CHECKS_WARNING++))
    fi

    return 0
}

#############################################################################
# Main Validation Flow
#############################################################################

main() {
    print_header "chora-base Pre-Flight Validation"

    echo "This script validates prerequisites before running install-sap.py"
    echo "Target: Catch 90%+ of installation issues before they occur"
    echo ""

    # Run all validation checks
    validate_python
    validate_git
    validate_directory_structure
    validate_sap_catalog
    validate_disk_space
    validate_write_permissions
    validate_install_script
    validate_optional_yaml

    # Print summary
    print_header "Validation Summary"

    echo -e "Checks passed:  ${GREEN}$CHECKS_PASSED${NC}"
    echo -e "Checks failed:  ${RED}$CHECKS_FAILED${NC}"
    echo -e "Warnings:       ${YELLOW}$CHECKS_WARNING${NC}"
    echo ""

    if [[ "$VALIDATION_FAILED" -eq 1 ]]; then
        print_failure "Pre-flight validation FAILED"
        echo ""
        print_info "Fix the issues above before running install-sap.py"
        print_info "For common issues, see: docs/user-docs/troubleshooting/onboarding-faq.md"
        echo ""
        exit 1
    elif [[ "$CHECKS_WARNING" -gt 0 ]]; then
        print_warning "Pre-flight validation PASSED with warnings"
        echo ""
        print_info "You can proceed with installation, but review warnings above"
        print_info "To install a SAP set, run:"
        echo ""
        echo "    python3 scripts/install-sap.py --set minimal-entry"
        echo ""
        exit 0
    else
        print_success "Pre-flight validation PASSED"
        echo ""
        print_info "All checks passed! You're ready to install SAPs."
        print_info "To see available SAP sets, run:"
        echo ""
        echo "    python3 scripts/install-sap.py --list-sets"
        echo ""
        print_info "To install a SAP set, run:"
        echo ""
        echo "    python3 scripts/install-sap.py --set minimal-entry"
        echo ""
        print_info "For help choosing a SAP set, see:"
        echo "    docs/user-docs/reference/sap-set-decision-tree.md"
        echo ""
        exit 0
    fi
}

# Run main function
main
