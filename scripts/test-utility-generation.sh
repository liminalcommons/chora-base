#!/usr/bin/env bash
# Test template generation with different utility flag combinations
# Tests that utilities and documentation generate correctly

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEST_OUTPUT_DIR="${PROJECT_ROOT}/test-output"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Testing chora-base utility generation"
echo "========================================="
echo ""

# Clean up previous test output
if [ -d "$TEST_OUTPUT_DIR" ]; then
    echo "Cleaning up previous test output..."
    rm -rf "$TEST_OUTPUT_DIR"
fi
mkdir -p "$TEST_OUTPUT_DIR"

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local project_name="$2"
    local api_utilities="$3"
    local persistence_helpers="$4"

    TESTS_RUN=$((TESTS_RUN + 1))

    echo "----------------------------------------"
    echo "Test ${TESTS_RUN}: ${test_name}"
    echo "  include_api_utilities: ${api_utilities}"
    echo "  include_persistence_helpers: ${persistence_helpers}"
    echo "----------------------------------------"

    local output_dir="${TEST_OUTPUT_DIR}/${project_name}"

    # Generate project with copier
    if copier copy --force \
        -d project_name="${test_name}" \
        -d project_slug="${project_name}" \
        -d package_name="$(echo $project_name | tr '-' '_')" \
        -d project_type="mcp_server" \
        -d author_name="Test Author" \
        -d author_email="test@example.com" \
        -d github_username="testuser" \
        -d python_version="3.11" \
        -d include_api_utilities="${api_utilities}" \
        -d include_persistence_helpers="${persistence_helpers}" \
        -d include_tests=true \
        -d include_pre_commit=false \
        -d include_github_actions=false \
        -d include_justfile=false \
        -d include_docker=false \
        -d include_vision_docs=false \
        -d include_memory_system=false \
        "${PROJECT_ROOT}" \
        "${output_dir}" > /dev/null 2>&1; then

        echo -e "${GREEN}✓ Project generated successfully${NC}"

        # Verify expected files exist
        local validation_passed=true

        # Check utils/__init__.py always exists if any utilities enabled
        if [ "$api_utilities" = "true" ] || [ "$persistence_helpers" = "true" ]; then
            if [ ! -f "${output_dir}/src/$(echo $project_name | tr '-' '_')/utils/__init__.py" ]; then
                echo -e "${RED}✗ Missing utils/__init__.py${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ utils/__init__.py exists${NC}"
            fi
        fi

        # Check API utilities
        if [ "$api_utilities" = "true" ]; then
            for file in validation.py responses.py errors.py; do
                if [ ! -f "${output_dir}/src/$(echo $project_name | tr '-' '_')/utils/${file}" ]; then
                    echo -e "${RED}✗ Missing utils/${file}${NC}"
                    validation_passed=false
                else
                    echo -e "${GREEN}✓ utils/${file} exists${NC}"
                fi
            done

            # Check API utility tests
            for file in test_validation.py test_responses.py test_errors.py; do
                if [ ! -f "${output_dir}/tests/utils/${file}" ]; then
                    echo -e "${RED}✗ Missing tests/utils/${file}${NC}"
                    validation_passed=false
                else
                    echo -e "${GREEN}✓ tests/utils/${file} exists${NC}"
                fi
            done

            # Check API utility documentation
            for file in use-input-validation.md standardize-responses.md improve-error-messages.md; do
                if [ ! -f "${output_dir}/user-docs/how-to/${file}" ]; then
                    echo -e "${RED}✗ Missing user-docs/how-to/${file}${NC}"
                    validation_passed=false
                else
                    echo -e "${GREEN}✓ user-docs/how-to/${file} exists${NC}"
                fi
            done
        else
            # Verify API utilities NOT generated
            for file in validation.py responses.py errors.py; do
                if [ -f "${output_dir}/src/$(echo $project_name | tr '-' '_')/utils/${file}" ]; then
                    echo -e "${RED}✗ utils/${file} should NOT exist${NC}"
                    validation_passed=false
                fi
            done
        fi

        # Check persistence utilities
        if [ "$persistence_helpers" = "true" ]; then
            if [ ! -f "${output_dir}/src/$(echo $project_name | tr '-' '_')/utils/persistence.py" ]; then
                echo -e "${RED}✗ Missing utils/persistence.py${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ utils/persistence.py exists${NC}"
            fi

            if [ ! -f "${output_dir}/tests/utils/test_persistence.py" ]; then
                echo -e "${RED}✗ Missing tests/utils/test_persistence.py${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ tests/utils/test_persistence.py exists${NC}"
            fi

            if [ ! -f "${output_dir}/user-docs/how-to/persist-application-state.md" ]; then
                echo -e "${RED}✗ Missing user-docs/how-to/persist-application-state.md${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ user-docs/how-to/persist-application-state.md exists${NC}"
            fi
        else
            # Verify persistence NOT generated
            if [ -f "${output_dir}/src/$(echo $project_name | tr '-' '_')/utils/persistence.py" ]; then
                echo -e "${RED}✗ utils/persistence.py should NOT exist${NC}"
                validation_passed=false
            fi
        fi

        # Check reference guide (should exist if any utilities enabled)
        if [ "$api_utilities" = "true" ] || [ "$persistence_helpers" = "true" ]; then
            if [ ! -f "${output_dir}/user-docs/reference/python-patterns.md" ]; then
                echo -e "${RED}✗ Missing user-docs/reference/python-patterns.md${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ user-docs/reference/python-patterns.md exists${NC}"

                # Verify conditional content in reference guide
                if [ "$api_utilities" = "true" ]; then
                    if ! grep -q "Pattern 1: Input Normalization" "${output_dir}/user-docs/reference/python-patterns.md"; then
                        echo -e "${RED}✗ Reference guide missing API utilities content${NC}"
                        validation_passed=false
                    else
                        echo -e "${GREEN}✓ Reference guide contains API utilities content${NC}"
                    fi
                fi

                if [ "$persistence_helpers" = "true" ]; then
                    if ! grep -q "Pattern 4: State Persistence" "${output_dir}/user-docs/reference/python-patterns.md"; then
                        echo -e "${RED}✗ Reference guide missing persistence content${NC}"
                        validation_passed=false
                    else
                        echo -e "${GREEN}✓ Reference guide contains persistence content${NC}"
                    fi
                fi
            fi

            # Check AGENTS.md has utility section
            if ! grep -q "## Python Utilities" "${output_dir}/AGENTS.md"; then
                echo -e "${RED}✗ AGENTS.md missing Python Utilities section${NC}"
                validation_passed=false
            else
                echo -e "${GREEN}✓ AGENTS.md contains Python Utilities section${NC}"
            fi
        fi

        if [ "$validation_passed" = true ]; then
            echo -e "${GREEN}✓ All validations passed${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}✗ Some validations failed${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi

    else
        echo -e "${RED}✗ Project generation failed${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    echo ""
}

# Run test matrix
echo "Running test matrix..."
echo ""

# Test 1: Both utilities enabled
run_test "Test Both Utilities" "test-both" "true" "true"

# Test 2: API utilities only
run_test "Test API Utilities Only" "test-api-only" "true" "false"

# Test 3: Persistence utilities only
run_test "Test Persistence Only" "test-persistence-only" "false" "true"

# Test 4: No utilities
run_test "Test No Utilities" "test-none" "false" "false"

# Summary
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Tests run:    ${TESTS_RUN}"
echo -e "Tests passed: ${GREEN}${TESTS_PASSED}${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "Tests failed: ${RED}${TESTS_FAILED}${NC}"
else
    echo -e "Tests failed: ${TESTS_FAILED}"
fi
echo ""

# Cleanup option
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    read -p "Delete test output directory? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$TEST_OUTPUT_DIR"
        echo "Test output cleaned up."
    else
        echo "Test output preserved at: ${TEST_OUTPUT_DIR}"
    fi
else
    echo -e "${RED}Some tests failed.${NC}"
    echo "Test output preserved at: ${TEST_OUTPUT_DIR}"
    echo "Review failed projects for details."
    exit 1
fi
