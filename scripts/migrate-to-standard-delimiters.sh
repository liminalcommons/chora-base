#!/usr/bin/env bash
# Migration script: Angle brackets → Standard Jinja2 delimiters
# Converts all .jinja files from << >> <% %> to {{ }} {% %}
#
# This migration adopts industry-standard Jinja2 delimiters used by
# all production Copier templates (copier-uv, Full Stack FastAPI, etc.)
#
# Background: After 8 failed releases (v2.0.0-v2.0.7) attempting custom
# delimiters, research revealed that all production templates use standard
# {{ }} syntax. The .jinja file suffix prevents delimiter conflicts.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Migrating to Standard Jinja2 Delimiters ===${NC}"
echo ""
echo "Converting angle brackets to curly braces:"
echo "  << variable >>  →  {{ variable }}"
echo "  <% block %>     →  {% block %}"
echo "  <# comment #>   →  {# comment #}"
echo ""

# Safety check: Are we in the right directory?
if [ ! -f "copier.yml" ]; then
  echo -e "${RED}Error: copier.yml not found. Run from repository root.${NC}"
  exit 1
fi

# Safety check: Backup template directory
BACKUP_DIR="template.backup-$(date +%Y%m%d-%H%M%S)"
echo -e "${YELLOW}Creating backup: ${BACKUP_DIR}${NC}"
cp -r template "$BACKUP_DIR"

# Count total files to process
TOTAL_FILES=$(find template/ -name "*.jinja" -type f | wc -l | tr -d ' ')
echo -e "${GREEN}Found ${TOTAL_FILES} .jinja files to migrate${NC}"
echo ""

# Counter for processed files
PROCESSED=0
TOTAL_REPLACEMENTS=0

# Process each .jinja file
find template/ -name "*.jinja" -type f | while read -r file; do
  # Count replacements in this file before migration
  BEFORE_COUNT=$(grep -o '<<\|<#\|<%' "$file" | wc -l | tr -d ' ')

  # Perform migration using sed
  # Order matters: Do longer patterns first to avoid partial matches
  sed -i '' \
    -e 's/<#/{#/g' \
    -e 's/#>/#}/g' \
    -e 's/<%/{%/g' \
    -e 's/%>/%}/g' \
    -e 's/<</{{/g' \
    -e 's/>>/}}/g' \
    "$file"

  # Count replacements after migration (should be 0)
  AFTER_COUNT=$(grep -o '<<\|<#\|<%' "$file" | wc -l | tr -d ' ')

  # Calculate replacements made
  REPLACEMENTS=$((BEFORE_COUNT))
  TOTAL_REPLACEMENTS=$((TOTAL_REPLACEMENTS + REPLACEMENTS))

  PROCESSED=$((PROCESSED + 1))

  # Show progress for files with changes
  if [ "$REPLACEMENTS" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} $(printf '%-60s' "$file") ${REPLACEMENTS} delimiters"
  fi
done

echo ""
echo -e "${GREEN}=== Migration Complete ===${NC}"
echo "Files processed: $TOTAL_FILES"
echo "Total delimiter conversions: $TOTAL_REPLACEMENTS"
echo ""
echo -e "${YELLOW}Backup location: ${BACKUP_DIR}${NC}"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff template/"
echo "2. Test templates: copier copy --force --trust . /tmp/test"
echo "3. If successful: rm -rf $BACKUP_DIR"
echo "4. If failed: rm -rf template && mv $BACKUP_DIR template"
echo ""
