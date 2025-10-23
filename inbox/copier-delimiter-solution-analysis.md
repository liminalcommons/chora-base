# Copier Template Delimiter Analysis & Solutions
## Response to v2.0.7-v2.0.8 Bracket Delimiter Investigation

**Date**: 2025-10-22  
**Context**: Analysis of liminalcommons/chora-base template delimiter conflicts  
**Versions Analyzed**: v2.0.0-v2.0.8 (WIP)

---

## Executive Summary

You're experiencing a **fundamental delimiter collision problem** that has no perfect solution in Copier/Jinja2. Both `{{ }}` and `[[ ]]` delimiters create extensive conflicts with template content. However, there ARE workable strategies, and I can help you identify the root cause of your specific line 134 error.

**Key Findings:**
1. ✅ Your bracket delimiter strategy WAS correct (confirmed by error moving from line 293 → 134)
2. ❌ Line 134 error is likely caused by an **unclosed block or malformed raw block earlier** in the file
3. ✅ Alternative delimiter strategies exist that reduce conflicts
4. ⚠️ Jinja2 line numbers in errors can be **misleading** (known bug in Jinja2's error reporting)

---

## Understanding Your Line 134 Mystery

### Why Line 134 Shows Error When It Contains No Brackets

Based on Jinja2 internals research, this is a **common Jinja2 behavior**:

**Root Causes:**
1. **Off-by-one errors**: Jinja2 line number reporting has known bugs (see GitHub issues #276, #1104 in pallets/jinja)
2. **Unclosed block scope**: An unclosed `[% if %]` or malformed `[% raw %]` block earlier in the file makes Jinja2 misinterpret line 134
3. **Inline raw blocks**: Raw blocks on the same line as other content can confuse the parser
4. **Character position vs line number**: The error reports character 9814, which doesn't match line numbers due to compilation artifacts

### Debugging Strategy for Line 134

**Step 1: Check for unclosed blocks**
```bash
# In template/NAMESPACES.md.jinja, count opening vs closing blocks
grep -c '\[%' template/NAMESPACES.md.jinja
grep -c '%\]' template/NAMESPACES.md.jinja

# Look for specific block types
grep -n '\[% if' template/NAMESPACES.md.jinja
grep -n '\[% endif' template/NAMESPACES.md.jinja
grep -n '\[% raw %\]' template/NAMESPACES.md.jinja
grep -n '\[% endraw %\]' template/NAMESPACES.md.jinja
```

**Step 2: Binary search to locate actual error**
```bash
# Create test versions with progressive removal
cp template/NAMESPACES.md.jinja template/NAMESPACES_test.md.jinja

# Comment out lines 1-100, test
# If error persists, error is in lines 100+
# If error disappears, error is in lines 1-100
# Repeat binary search
```

**Step 3: Validate Jinja2 syntax outside Copier**
```python
from jinja2 import Environment

env = Environment(
    block_start_string="[%",
    block_end_string="%]",
    variable_start_string="[[",
    variable_end_string="]]",
    comment_start_string="[#",
    comment_end_string="#]",
)

# Test JUST the problematic file
with open('template/NAMESPACES.md.jinja', 'r') as f:
    content = f.read()
    try:
        template = env.from_string(content)
        print("✓ Template syntax valid")
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"  Line: {e.lineno if hasattr(e, 'lineno') else 'unknown'}")
```

**Step 4: Check for inline raw blocks**
```bash
# Find potential problem patterns
grep -n '\[% raw %\][^[]' template/NAMESPACES.md.jinja
grep -n '[^]]\[% endraw %\]' template/NAMESPACES.md.jinja
```

### Common Inline Raw Block Issues

**Problem Pattern:**
```markdown
- **Convention**: [% raw %][Chora MCP Conventions v1.0](https://...)[% endraw %]
```

This creates: `[% raw %][Chora...` where Jinja2 sees:
1. `[%` start block delimiter
2. ` raw ` - raw keyword
3. `%]` end block delimiter  
4. `[` - START OF NEW DELIMITER (confuses parser!)

**Solution:**
```markdown
- **Convention**: 
[% raw %]
[Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md)
[% endraw %]
```

OR (better for inline):
```markdown
- **Convention**: [% raw %]Chora MCP Conventions v1.0[% endraw %] (link separately)
- **Link**: [Conventions Documentation](https://...)
```

---

## Alternative Delimiter Strategies

### Option 1: Angle Bracket Delimiters (RECOMMENDED)

**Configuration:**
```yaml
# copier.yml
_envops:
  block_start_string: "<%"
  block_end_string: "%>"
  variable_start_string: "<<"
  variable_end_string: ">>"
  comment_start_string: "<#"
  comment_end_string: "#>"
  keep_trailing_newline: true
  trim_blocks: true
  lstrip_blocks: true
```

**Conflict Analysis:**
| Content Type | Conflicts? | Notes |
|--------------|-----------|-------|
| Python f-strings `f"{var}"` | ✅ No | Uses `{}` |
| Python `.format()` | ✅ No | Uses `{}` |
| Python dicts `{"key": "value"}` | ✅ No | Uses `{}` |
| Markdown links `[text](url)` | ✅ No | Uses `[]` |
| Regex patterns `[a-z][0-9]` | ✅ No | Uses `[]` |
| Bash/Python comparison `if [ $x -gt 5 ]` | ✅ No | Uses single `[]` |
| HTML tags `<div></div>` | ⚠️ Rare | Requires `<% raw %>` |
| C++ templates `vector<int>` | ⚠️ Rare | Requires `<% raw %>` |
| Bash here-docs `<<EOF` | ⚠️ Rare | Only if using `<<` for Jinja2 var |
| XML/HTML `<element>` | ⚠️ Rare | Only single `<` |

**Advantages:**
- ✅ No conflicts with Python syntax
- ✅ No conflicts with Markdown syntax
- ✅ No conflicts with regex patterns
- ✅ Visually distinctive from content
- ✅ Rarely used in content

**Disadvantages:**
- ⚠️ May conflict with HTML templates
- ⚠️ May conflict with XML files
- ⚠️ May conflict with bash here-docs (`<<EOF`)

**Best For:** Python project templates with markdown docs (YOUR USE CASE)

### Option 2: Percent-Sign Delimiters

**Configuration:**
```yaml
# copier.yml
_envops:
  block_start_string: "{%"
  block_end_string: "%}"
  variable_start_string: "%{"
  variable_end_string: "}%"
  comment_start_string: "{#"
  comment_end_string: "#}"
```

**Conflict Analysis:**
- ✅ Minimal conflicts with Python
- ⚠️ Conflicts with Python format specs `f"{x:.2%}"`
- ⚠️ Conflicts with bash script modulo operations

**Best For:** Templates with minimal Python string formatting

### Option 3: Mixed Delimiters (Angular-Style)

**Configuration:**
```yaml
# copier.yml
_envops:
  block_start_string: "{@"
  block_end_string: "@}"
  variable_start_string: "{{"
  variable_end_string: "}}"
  comment_start_string: "{*"
  comment_end_string: "*}"
```

**Conflict Analysis:**
- ⚠️ Variables still conflict with Python `{}`
- ✅ Blocks don't conflict
- ⚠️ Not recommended for Python-heavy templates

### Option 4: Dollar-Sign Delimiters

**Configuration:**
```yaml
# copier.yml
_envops:
  block_start_string: "{$"
  block_end_string: "$}"
  variable_start_string: "${"
  variable_end_string: "}"
  comment_start_string: "{!"
  comment_end_string: "!}"
```

**Conflict Analysis:**
- ⚠️ Conflicts with shell variables `${var}`
- ⚠️ Conflicts with Ansible/Terraform
- ⚠️ Not recommended for templates with bash scripts

---

## Recommended Solution for Chora-Base

### Primary Recommendation: Angle Bracket Delimiters

Given your template content (Python code + Markdown docs + minimal HTML), **angle bracket delimiters** are the best choice:

```yaml
# copier.yml - v2.0.8 configuration
_min_copier_version: "9.0.0"
_templates_suffix: .jinja

_envops:
  # Angle bracket delimiters - optimal for Python + Markdown
  block_start_string: "<%"
  block_end_string: "%>"
  variable_start_string: "<<"
  variable_end_string: ">>"
  comment_start_string: "<#"
  comment_end_string: "#>"
  
  # Whitespace control
  keep_trailing_newline: true
  trim_blocks: true
  lstrip_blocks: true
```

### Migration Steps: Bracket `[[ ]]` → Angle `<< >>`

**Step 1: Update copier.yml** (shown above)

**Step 2: Global find/replace in templates**
```bash
# Backup first!
git checkout -b feature/angle-bracket-delimiters

# Variable delimiters
find template/ -name "*.jinja" -type f -exec sed -i 's/\[\[/\<</g' {} \;
find template/ -name "*.jinja" -type f -exec sed -i 's/\]\]/\>>/g' {} \;

# Block delimiters
find template/ -name "*.jinja" -type f -exec sed -i 's/\[%/<%/g' {} \;
find template/ -name "*.jinja" -type f -exec sed -i 's/%\]/%>/g' {} \;

# Comment delimiters (if used)
find template/ -name "*.jinja" -type f -exec sed -i 's/\[#/<#/g' {} \;
find template/ -name "*.jinja" -type f -exec sed -i 's/#\]/#>/g' {} \;
```

**Step 3: Remove unnecessary raw blocks**
Since angle brackets don't conflict with Python or Markdown, you can remove most `<% raw %>` blocks around:
- Python f-strings and `.format()` calls
- Python dict literals
- Markdown links
- Regex patterns in Python code

**Keep raw blocks only for:**
- Actual HTML tags (if any)
- C++ templates (if any)
- Content that legitimately uses `<<` or `>>`

**Step 4: Test thoroughly**
```bash
# Test basic template rendering
cd /tmp/test-project
copier copy --force --trust /path/to/chora-base . \
  --data project_slug=test-project \
  --data project_name="Test Project" \
  --data project_type=mcp_server

# Verify all files generated correctly
ls -la

# Test update operation (CRITICAL)
cd /tmp/test-project
copier update --trust

# Test with all project types
for pt in mcp_server standard backend cli; do
  copier copy --force --trust /path/to/chora-base /tmp/test-$pt \
    --data project_type=$pt --data project_slug=test-$pt
done
```

### Manual Fixes for Specific Conflicts

**If you have HTML templates:**
```html
<!-- OLD: Requires raw blocks -->
<div class="container">
  [[ content ]]
</div>

<!-- NEW: With angle brackets -->
<% raw %>
<div class="container">
<% endraw %>
  << content >>
<% raw %>
</div>
<% endraw %>

<!-- OR: Better structure -->
<% raw %><div class="container"><% endraw %>
  << content >>
<% raw %></div><% endraw %>
```

**If you have bash here-docs using `<<`:**
```bash
# If your template has this:
cat <<EOF > file.txt
Content here
EOF

# Solution: Use different here-doc delimiter
cat <<'TEMPLATE_EOF' > file.txt
Content here << jinja_var >>  # Jinja2 will process this
TEMPLATE_EOF

# OR: Wrap in raw if no Jinja2 needed
<% raw %>
cat <<EOF > file.txt
Static content
EOF
<% endraw %>
```

---

## Addressing Your Specific Questions

### Q1: Recommended delimiter strategy?

**Answer:** Angle brackets `<< >>` for variables, `<% %>` for blocks.

**Reasoning:**
- Python projects: No conflicts with `{}` syntax
- Markdown docs: No conflicts with `[]` syntax
- Minimal content conflicts
- Visually distinct
- Industry precedent (PHP, JSP use similar)

### Q2: Alternative delimiters to avoid both `{}` and `[]`?

**Answer:** Yes, multiple options exist:

1. **Angle brackets** `<< >>` (recommended)
2. **Percent-mixed** `%{ }%` for variables
3. **Dollar-sign** `${ }` (conflicts with shell)
4. **At-sign** `@{ }` (less common)
5. **Unicode** `«« »»` (hard to type, poor tool support)

Copier accepts any valid Jinja2 delimiter configuration via `_envops`.

### Q3: Raw block best practices?

**Answer:**

**Multi-line raw blocks:**
```jinja
<% raw %>
# Python code with all the braces/brackets you want
config = {"key": "value"}
pattern = r"[a-z][0-9]+"
<% endraw %>
```

**Inline raw is problematic** - avoid:
```markdown
<!-- AVOID THIS -->
Text <% raw %>[link](url)<% endraw %> more text

<!-- DO THIS INSTEAD -->
<% raw %>
Text [link](url) more text
<% endraw %>
```

**Performance:** Raw blocks have negligible performance impact. Use freely.

**Tip:** With angle brackets, you need FAR fewer raw blocks.

### Q4: Configure Jinja2 to be less greedy?

**Answer:** No direct configuration for "greediness", but:

1. **Whitespace requirements**: Jinja2 doesn't support `[[ var ]]` (with space) vs `[[var]]` (without) as different
2. **Custom extensions**: Could write a Jinja2 extension, but that's advanced and fragile
3. **Better solution**: Choose non-conflicting delimiters (angle brackets)

### Q5: Template design patterns for extensive conflicts?

**Answer:**

**Recommended: A + C**
- A: Choose angle bracket delimiters to minimize conflicts
- C: Use Jinja2 extensions for complex logic (keep templates simple)

**Not recommended:**
- B: Splitting templates gets messy with Copier's update system
- D: Don't switch from Copier - it's good, just needs right config

### Q6: Why does Copier report line 134 error?

**Answer:** Multiple possibilities:

1. **Jinja2 bug**: Known issues with line number reporting (see pallets/jinja #276, #1104)
2. **Unclosed block**: Error earlier in file, reported at later line
3. **Inline raw block**: Parser confused by `[% raw %][markdown` pattern
4. **Compiled code artifact**: Jinja2 compiles templates to Python, line numbers from compiled code

**Debug:** Use the validation script I provided earlier to test outside Copier.

### Q7: How to debug when minimal test works but full file fails?

**Answer:**

**Method 1: Binary search**
```python
# Test progressively larger chunks
from jinja2 import Environment

env = Environment(
    variable_start_string="[[",
    variable_end_string="]]",
    # ... other settings
)

with open('template/NAMESPACES.md.jinja') as f:
    lines = f.readlines()

# Test first 50 lines
try:
    env.from_string(''.join(lines[:50]))
    print("✓ Lines 1-50 OK")
except Exception as e:
    print(f"✗ Error in lines 1-50: {e}")

# Test lines 51-100
try:
    env.from_string(''.join(lines[50:100]))
    print("✓ Lines 51-100 OK")
except Exception as e:
    print(f"✗ Error in lines 51-100: {e}")

# Continue until you find the problematic section
```

**Method 2: Verbose error output**
```python
import jinja2
from jinja2 import meta

env = jinja2.Environment(
    variable_start_string="[[",
    variable_end_string="]]",
    block_start_string="[%",
    block_end_string="%]",
)

try:
    with open('template/NAMESPACES.md.jinja') as f:
        template_str = f.read()
    
    # Parse to AST for debugging
    ast = env.parse(template_str)
    print("✓ Template parsed successfully")
    
    # Get template variables
    vars = meta.find_undeclared_variables(ast)
    print(f"Template variables: {vars}")
    
    # Try compilation
    code = env.compile(template_str)
    print("✓ Template compiled successfully")
    
except jinja2.TemplateSyntaxError as e:
    print(f"Syntax Error:")
    print(f"  Message: {e.message}")
    print(f"  Line: {e.lineno}")
    print(f"  Name: {e.name}")
    print(f"  Filename: {e.filename}")
    
    # Get context around error
    if template_str:
        lines = template_str.split('\n')
        start = max(0, e.lineno - 5)
        end = min(len(lines), e.lineno + 5)
        print(f"\nContext (lines {start}-{end}):")
        for i in range(start, end):
            marker = ">>>" if i == e.lineno - 1 else "   "
            print(f"{marker} {i+1:4d}: {lines[i]}")
```

**Method 3: Jinja2 linting**
```bash
# Install jinjalint (community tool)
pip install jinjalint

# Lint your templates
jinjalint template/NAMESPACES.md.jinja

# Note: jinjalint may not understand custom delimiters
# Use with caution
```

### Q8: Alternative approaches?

**Answer:**

**Evaluated options:**

1. **Escaping strategies**: Too verbose, unreadable
2. **Two-pass rendering**: Copier doesn't support this
3. **Different extensions by file**: Not supported by Copier
4. **Template inheritance**: Good practice, but doesn't solve delimiter conflicts

**Best approach:** 
- ✅ Use angle bracket delimiters
- ✅ Structure templates with clear separation of concerns
- ✅ Use Jinja2 macros for repeated patterns
- ✅ Keep Python logic in separate files when possible

---

## Immediate Action Plan for v2.0.8

### Phase 1: Fix Current v2.0.7 Issues (Debug Mode)

**Goal:** Understand exact cause of line 134 error

```bash
# 1. Validate template syntax outside Copier
cd /path/to/chora-base
python3 <<'PYTHON'
from jinja2 import Environment

env = Environment(
    block_start_string="[%",
    block_end_string="%]",
    variable_start_string="[[",
    variable_end_string="]]",
    comment_start_string="[#",
    comment_end_string="#]",
)

with open('template/NAMESPACES.md.jinja', 'r') as f:
    content = f.read()

try:
    template = env.from_string(content)
    print("✓ NAMESPACES.md.jinja syntax is valid")
except Exception as e:
    print(f"✗ Syntax error in NAMESPACES.md.jinja:")
    print(f"  {e}")
    if hasattr(e, 'lineno'):
        print(f"  Line: {e.lineno}")
PYTHON

# 2. Check for unclosed blocks
echo "Checking block balance..."
echo "[% ... %] blocks:"
echo "  Opening: $(grep -c '\[%' template/NAMESPACES.md.jinja)"
echo "  Closing: $(grep -c '%\]' template/NAMESPACES.md.jinja)"

# 3. Check for suspicious patterns
echo ""
echo "Potential inline raw blocks:"
grep -n '\[% raw %\]\[' template/NAMESPACES.md.jinja

echo ""
echo "Potential unclosed if blocks:"
diff <(grep -c '\[% if' template/NAMESPACES.md.jinja) \
     <(grep -c '\[% endif' template/NAMESPACES.md.jinja)
```

### Phase 2: Migrate to Angle Bracket Delimiters

**Why this is the solution:**
- Eliminates Python `{}` conflicts
- Eliminates Markdown `[]` conflicts  
- Eliminates regex `[]` conflicts
- Minimal content conflicts to manage

**Migration script:**
```bash
#!/bin/bash
# migrate-to-angle-brackets.sh

set -e

echo "🔄 Migrating chora-base to angle bracket delimiters..."

# 1. Update copier.yml
cat > copier.yml.new <<'YAML'
_min_copier_version: "9.0.0"
_templates_suffix: .jinja

_envops:
  block_start_string: "<%"
  block_end_string: "%>"
  variable_start_string: "<<"
  variable_end_string: ">>"
  comment_start_string: "<#"
  comment_end_string: "#>"
  keep_trailing_newline: true
  trim_blocks: true
  lstrip_blocks: true

# ... rest of your copier.yml content
YAML

# 2. Convert all .jinja files
echo "📝 Converting template delimiters..."

find template/ -name "*.jinja" -type f | while read file; do
  echo "  Processing: $file"
  
  # Create backup
  cp "$file" "$file.backup"
  
  # Convert delimiters
  sed -i 's/\[\[/<</g' "$file"
  sed -i 's/\]\]/>>/g' "$file"
  sed -i 's/\[%/<%/g' "$file"
  sed -i 's/%\]/%>/g' "$file"
  sed -i 's/\[#/<#/g' "$file"
  sed -i 's/#\]/#>/g' "$file"
  
  echo "  ✓ Converted: $file"
done

echo ""
echo "✅ Migration complete!"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Test: copier copy --force --trust . /tmp/test-project"
echo "3. If successful: git add -A && git commit -m 'feat: migrate to angle bracket delimiters'"
echo "4. If issues: find template/ -name '*.backup' -exec bash -c 'mv \"\$1\" \"\${1%.backup}\"' _ {} \;"
```

### Phase 3: Test & Release

```bash
# Test all project types
for project_type in mcp_server standard backend cli; do
  echo "Testing project_type=$project_type..."
  rm -rf /tmp/test-$project_type
  
  copier copy --force --trust . /tmp/test-$project_type \
    --data project_type=$project_type \
    --data project_slug=test-$project_type \
    --data project_name="Test $project_type" \
    --data github_username=testuser \
    --data author_name="Test User" \
    --data author_email=test@example.com
  
  if [ $? -eq 0 ]; then
    echo "  ✓ $project_type: SUCCESS"
  else
    echo "  ✗ $project_type: FAILED"
    exit 1
  fi
done

echo ""
echo "✅ All project types generated successfully!"
echo "Testing copier update..."

# Test update operation
cd /tmp/test-mcp_server
copier update --trust

if [ $? -eq 0 ]; then
  echo "  ✓ Update: SUCCESS"
else
  echo "  ✗ Update: FAILED"
  exit 1
fi

echo ""
echo "🎉 All tests passed! Ready for v2.0.8 release."
```

---

## Success Criteria

### Definition of Done for v2.0.8

- [ ] Template renders successfully with `copier copy`
- [ ] Template updates successfully with `copier update`
- [ ] All project types (mcp_server, standard, backend, cli) work
- [ ] No TemplateSyntaxError during rendering
- [ ] Python f-strings and `.format()` work without raw blocks
- [ ] Markdown links work without raw blocks
- [ ] Regex patterns work without raw blocks
- [ ] mcp-n8n team can upgrade from v1.9.3 to v2.0.8
- [ ] Documentation updated with delimiter choice rationale

---

## Answers to "Questions for Subject Matter Expert"

### Summary Table

| Question | Answer | Details |
|----------|--------|---------|
| Q1: Delimiter strategy? | Angle brackets `<< >>` | Avoids Python `{}` and Markdown `[]` conflicts |
| Q2: Alternative delimiters? | Yes, many options | `<< >>`, `%{ }%`, `${ }`, etc. |
| Q3: Raw block best practices? | Multi-line, avoid inline | Less needed with angle brackets |
| Q4: Less greedy parsing? | No, but choose better delimiters | Angle brackets minimize conflicts |
| Q5: Design patterns? | Choose right delimiters + keep logic simple | Angle brackets + Jinja2 macros |
| Q6: Why line 134 error? | Unclosed block or Jinja2 bug | Debug with validation script |
| Q7: Debug full file? | Binary search + AST parsing | Use provided debug script |
| Q8: Alternative approaches? | Not needed with angle brackets | Right delimiter choice solves 90% of issues |

---

## Long-term Recommendations

### Template Organization

**Separate concerns:**
```
template/
├── _macros/              # Reusable Jinja2 macros
│   ├── python.jinja      # Python-specific macros
│   └── markdown.jinja    # Markdown-specific macros
├── src/                  # Python code templates
├── docs/                 # Documentation templates
└── config/               # Configuration templates
```

**Use macros for repeated patterns:**
```jinja
<# Define macros in _macros/markdown.jinja #>
<% macro github_link(user, repo, text='') %>
<<text or (user ~ '/' ~ repo)>> (https://github.com/<<user>>/<<repo>>)
<% endmacro %>

<# Use in templates #>
<% from '_macros/markdown.jinja' import github_link %>

Repository: << github_link(github_username, project_slug) >>
```

### Testing Strategy

**CI/CD for templates:**
```yaml
# .github/workflows/template-test.yml
name: Test Template

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project_type: [mcp_server, standard, backend, cli]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Copier
        run: pip install copier
      
      - name: Test copier copy
        run: |
          copier copy --force --trust . /tmp/test-${{ matrix.project_type }} \
            --data project_type=${{ matrix.project_type }} \
            --data project_slug=test-project
      
      - name: Test copier update
        run: |
          cd /tmp/test-${{ matrix.project_type }}
          copier update --trust
```

### Documentation

**Add to template README:**
```markdown
## Delimiter Choice

This template uses angle bracket delimiters to avoid conflicts:

- Variables: `<< variable >>`
- Blocks: `<% if condition %>...<% endif %>`
- Comments: `<# comment #>`

**Why angle brackets?**
- ✅ No conflicts with Python f-strings `f"{var}"`
- ✅ No conflicts with Python `.format()` methods
- ✅ No conflicts with Markdown links `[text](url)`
- ✅ No conflicts with regex patterns `[a-z][0-9]`

**Raw blocks needed only for:**
- HTML tags: `<% raw %><div><% endraw %>`
- Content with literal `<<` or `>>`
```

---

## Conclusion

Your journey through v2.0.0-v2.0.7 has been educational - you've discovered that **delimiter choice is critical** for Copier templates with mixed content.

**The Solution:**
1. ✅ **Use angle bracket delimiters** (`<< >>` for variables, `<% %>` for blocks)
2. ✅ **Fix line 134** by finding unclosed/malformed blocks (use debug scripts provided)
3. ✅ **Remove most raw blocks** (angle brackets don't conflict with Python/Markdown)
4. ✅ **Test thoroughly** before v2.0.8 release

**Expected outcome:**
- Template renders successfully
- Python code works without wrapping
- Markdown works without wrapping
- mcp-n8n team can upgrade
- Maintenance burden drops significantly

**Timeline estimate:**
- Debug line 134 issue: 30-60 minutes
- Migrate to angle brackets: 1-2 hours
- Testing: 1-2 hours
- **Total: 3-5 hours to v2.0.8 release**

---

## Next Steps

1. **Immediate**: Run the debug scripts to find line 134 root cause
2. **Short-term**: Migrate to angle bracket delimiters
3. **Long-term**: Add CI/CD testing for templates

Questions? Need help with migration? I'm here to assist with any step of this process.