#!/usr/bin/env bash
# Bisection script to find which content in NAMESPACES.md.jinja triggers Copier bug
#
# Strategy:
# 1. Start with full file (333 lines) - FAILS at line 134
# 2. Try first half (lines 1-166) - see if error persists
# 3. Try second half (lines 167-333) - see if error persists
# 4. Continue bisecting until we find the minimal triggering content

set -euo pipefail

ORIGINAL_FILE="/Users/victorpiper/code/chora-base/template/NAMESPACES.md.jinja"
BACKUP_FILE="/Users/victorpiper/code/chora-base/template/NAMESPACES.md.jinja.bisect-backup"
TEST_DIR="/tmp/chora-bisect-test"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== NAMESPACES.md.jinja Bisection Tool ===${NC}"
echo ""

# Backup original file
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Creating backup of original file..."
  cp "$ORIGINAL_FILE" "$BACKUP_FILE"
  echo -e "${GREEN}✓ Backup created: $BACKUP_FILE${NC}"
else
  echo -e "${YELLOW}Using existing backup: $BACKUP_FILE${NC}"
fi

# Function to test Copier with current file
test_copier() {
  local test_name="$1"
  echo ""
  echo -e "${YELLOW}Testing: $test_name${NC}"

  rm -rf "$TEST_DIR"

  if copier copy --force --trust /Users/victorpiper/code/chora-base "$TEST_DIR" \
    --data project_type=mcp_server \
    --data project_name="test-project" \
    --data project_slug=test-project \
    --data package_name=test_project \
    --data mcp_namespace=testproject \
    2>&1 | grep -q "TemplateSyntaxError"; then
    echo -e "${RED}✗ FAILED - Error still present${NC}"
    return 1
  else
    echo -e "${GREEN}✓ SUCCESS - No error!${NC}"
    return 0
  fi
}

# Function to extract lines from original file
extract_lines() {
  local start=$1
  local end=$2
  local output_file="$ORIGINAL_FILE"

  sed -n "${start},${end}p" "$BACKUP_FILE" > "$output_file"
  echo "Extracted lines $start-$end ($(wc -l < "$output_file") lines total)"
}

# Show usage
echo "Usage:"
echo "  ./bisect_namespaces.sh test <start_line> <end_line>  - Test specific line range"
echo "  ./bisect_namespaces.sh auto                           - Auto-bisect to find trigger"
echo "  ./bisect_namespaces.sh restore                        - Restore original file"
echo ""

# Parse command
COMMAND="${1:-}"

case "$COMMAND" in
  "test")
    START_LINE="${2:-1}"
    END_LINE="${3:-333}"
    extract_lines "$START_LINE" "$END_LINE"
    test_copier "Lines $START_LINE-$END_LINE"
    ;;

  "auto")
    echo "Starting automatic bisection..."
    echo "This will test progressively smaller sections until we find the trigger."
    echo ""

    # Test 1: First half (lines 1-166)
    echo "=== Test 1: First half (lines 1-166) ==="
    extract_lines 1 166
    if test_copier "First half"; then
      echo "First half works! Bug is in second half (lines 167-333)"
      SEARCH_START=167
      SEARCH_END=333
    else
      echo "First half fails! Bug is in first half (lines 1-166)"
      SEARCH_START=1
      SEARCH_END=166
    fi

    # Test 2: Narrow down further
    MID=$(( (SEARCH_START + SEARCH_END) / 2 ))
    echo ""
    echo "=== Test 2: Lines $SEARCH_START-$MID ==="
    extract_lines $SEARCH_START $MID
    if test_copier "Lines $SEARCH_START-$MID"; then
      echo "Lower half works! Bug is in lines $((MID+1))-$SEARCH_END"
      SEARCH_START=$((MID+1))
    else
      echo "Lower half fails! Bug is in lines $SEARCH_START-$MID"
      SEARCH_END=$MID
    fi

    # Test 3: Narrow down even more
    MID=$(( (SEARCH_START + SEARCH_END) / 2 ))
    echo ""
    echo "=== Test 3: Lines $SEARCH_START-$MID ==="
    extract_lines $SEARCH_START $MID
    if test_copier "Lines $SEARCH_START-$MID"; then
      echo "Lower quarter works! Bug is in lines $((MID+1))-$SEARCH_END"
      SEARCH_START=$((MID+1))
    else
      echo "Lower quarter fails! Bug is in lines $SEARCH_START-$MID"
      SEARCH_END=$MID
    fi

    echo ""
    echo -e "${GREEN}=== Bisection narrowed to approximately lines $SEARCH_START-$SEARCH_END ===${NC}"
    echo "Run manual tests to narrow further:"
    echo "  ./bisect_namespaces.sh test $SEARCH_START $SEARCH_END"
    echo ""
    echo "To see this content:"
    echo "  sed -n '${SEARCH_START},${SEARCH_END}p' $BACKUP_FILE"
    ;;

  "restore")
    echo "Restoring original file..."
    cp "$BACKUP_FILE" "$ORIGINAL_FILE"
    echo -e "${GREEN}✓ Original file restored${NC}"
    ;;

  *)
    echo -e "${RED}Error: Unknown command '$COMMAND'${NC}"
    echo "Use: test, auto, or restore"
    exit 1
    ;;
esac

echo ""
