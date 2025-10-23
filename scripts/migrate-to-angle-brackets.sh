#!/bin/bash
# Migrate chora-base template from bracket [[ ]] to angle << >> delimiters
# Part of v2.0.8 release to fix persistent TemplateSyntaxError issues

set -e

echo "🔄 Migrating chora-base template to angle bracket delimiters..."
echo ""

# Check we're in the right directory
if [ ! -f "copier.yml" ]; then
    echo "❌ Error: Must run from chora-base root directory"
    exit 1
fi

# Count files to convert
JINJA_COUNT=$(find template/ -name "*.jinja" -type f | wc -l | tr -d ' ')
echo "📝 Found $JINJA_COUNT .jinja template files to convert"
echo ""

# Track statistics
TOTAL_CONVERSIONS=0

# Convert all .jinja files
find template/ -name "*.jinja" -type f | sort | while read file; do
    # Create backup
    cp "$file" "$file.backup"

    # Count conversions in this file
    BRACKET_VAR_START=$(grep -o '\[\[' "$file" | wc -l | tr -d ' ')
    BRACKET_VAR_END=$(grep -o '\]\]' "$file" | wc -l | tr -d ' ')
    BRACKET_BLOCK_START=$(grep -o '\[%' "$file" | wc -l | tr -d ' ')
    BRACKET_BLOCK_END=$(grep -o '%\]' "$file" | wc -l | tr -d ' ')
    BRACKET_COMMENT_START=$(grep -o '\[#' "$file" | wc -l | tr -d ' ')
    BRACKET_COMMENT_END=$(grep -o '#\]' "$file" | wc -l | tr -d ' ')

    FILE_TOTAL=$((BRACKET_VAR_START + BRACKET_VAR_END + BRACKET_BLOCK_START + BRACKET_BLOCK_END + BRACKET_COMMENT_START + BRACKET_COMMENT_END))

    # Convert delimiters
    # Note: Order matters! Do comment delimiters first to avoid partial matches
    sed -i '' \
        -e 's/\[#/<#/g' \
        -e 's/#\]/#>/g' \
        -e 's/\[%/<%/g' \
        -e 's/%\]/%>/g' \
        -e 's/\[\[/<</g' \
        -e 's/\]\]/>>/g' \
        "$file"

    # Verify conversion
    ANGLE_VAR_START=$(grep -o '<<' "$file" | wc -l | tr -d ' ')
    ANGLE_VAR_END=$(grep -o '>>' "$file" | wc -l | tr -d ' ')

    if [ "$FILE_TOTAL" -gt 0 ]; then
        echo "  ✓ $(basename $file): Converted $FILE_TOTAL delimiter tokens"
    fi
done

echo ""
echo "✅ Delimiter conversion complete!"
echo ""

# Validation
echo "🔍 Validating conversion..."
REMAINING_BRACKETS=$(grep -r '\[\[' template/ --include="*.jinja" 2>/dev/null | wc -l | tr -d ' ')

if [ "$REMAINING_BRACKETS" -gt 0 ]; then
    echo "⚠️  Warning: Found $REMAINING_BRACKETS remaining [[ brackets in templates"
    echo "   These may be legitimate (markdown links, etc.) or missed conversions"
    grep -rn '\[\[' template/ --include="*.jinja" | head -5
else
    echo "✅ No remaining [[ brackets found"
fi

echo ""
echo "📊 Conversion Summary:"
echo "  Files processed: $JINJA_COUNT"
echo "  Backup files: $(find template/ -name "*.backup" | wc -l | tr -d ' ')"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff template/"
echo "  2. Test template: copier copy --force --trust . /tmp/test-project"
echo "  3. If successful: rm template/**/*.backup && git add -A"
echo "  4. If problems: ./scripts/rollback-migration.sh"
echo ""
