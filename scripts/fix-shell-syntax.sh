#!/usr/bin/env bash
# Fix shell syntax that was incorrectly converted by delimiter migration
# This script restores shell constructs that got converted to Jinja2 syntax

set -euo pipefail

echo "Fixing shell syntax in template files..."

# Fix heredocs: {{EOF → <<EOF, {{'EOF' → <<'EOF'
find template/ -name "*.jinja" -type f -exec sed -i '' \
  -e 's/{{EOF/<<EOF/g' \
  -e "s/{{'EOF'/<<'EOF'/g" \
  -e "s/}}'EOF'/<<'EOF'/g" \
  {} \;

# Fix shell test expressions: if {{ condition }} → if [[ condition ]]
find template/ -name "*.jinja" -type f -exec sed -i '' -E \
  's/if \{\{ /if [[ /g; s/ \}\}; then/ ]]; then/g' \
  {} \;

# Fix while loops: while {{ condition }} → while [[ condition ]]
find template/ -name "*.jinja" -type f -exec sed -i '' -E \
  's/while \{\{ /while [[ /g; s/ \}\}; do/ ]]; do/g' \
  {} \;

# Fix array access: arr{{i}} → arr[i]  (but not Jinja2 variables)
# This is tricky - only fix in .sh.jinja files where array syntax is common
find template/scripts/ -name "*.sh.jinja" -type f -exec sed -i '' -E \
  's/\$\{([A-Z_]+){{([0-9]+)}}}/\${\1[\2]}/g' \
  {} \;

echo "✓ Fixed shell syntax"
echo ""
echo "To verify: git diff template/"
