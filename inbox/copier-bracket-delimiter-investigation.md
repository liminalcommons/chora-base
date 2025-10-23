# Copier Bracket Delimiter Investigation Report

**Date**: 2025-10-22
**Project**: chora-base v2.0.7 → v2.0.8
**Issue**: Persistent TemplateSyntaxError with bracket delimiters
**Reporter**: mcp-n8n team (@vlct0rs-github-acct)

---

## Executive Summary

After 8 release attempts (v2.0.0-v2.0.7) to fix Jinja2 template syntax errors in the chora-base Copier template, we identified that **both curly brace `{{ }}` and bracket `[[ ]]` delimiter strategies have fundamental conflicts** with template content. This report documents the investigation, findings, and seeks expert guidance on the optimal delimiter strategy for a Python project template.

---

## Problem Background

### Original Issue (v2.0.0-v2.0.6)
- **Error**: `jinja2.exceptions.TemplateSyntaxError` at `template/scripts/extract_tests.py.jinja:293`
- **Root Cause**: Copier 6+ changed from bracket to curly brace delimiters `{{ }}` as default
- **Conflict**: Python f-strings and `.format()` methods use `{}` syntax, conflicting with `{{ }}`
- **Fix Attempts**:
  - v2.0.1-v2.0.3: Converted some f-strings to `.format()`
  - v2.0.4-v2.0.6: Wrapped `.format()` calls in `{% raw %}` blocks
  - **Result**: All failed - same error persisted

### Delimiter Change Approach (v2.0.7)
Based on research into Copier's Jinja2 configuration, we implemented bracket delimiters:

```yaml
# copier.yml
_envops:
  block_start_string: "[%"
  block_end_string: "%]"
  variable_start_string: "[["
  variable_end_string: "]]"
  comment_start_string: "[#"
  comment_end_string: "#]"
```

**Mass Conversion**: Changed ALL 1,717 Jinja2 syntax elements across 57 files from `{{ }}` to `[[ ]]`

### Current Issue (v2.0.7-v2.0.8)
- **Error**: `jinja2.exceptions.TemplateSyntaxError: unexpected ']'`
- **Location**: `template/NAMESPACES.md.jinja`, line 134
- **Progress**: Error location CHANGED (previously line 293), indicating bracket delimiters ARE being used
- **Problem**: Bracket delimiters conflict with markdown and regex syntax

---

## Technical Investigation

### Direct Testing Discovery

When we finally tested directly with `copier copy --force --trust`:

```bash
cd /tmp/test && copier copy --force --trust /path/to/chora-base . \
  --data project_slug=test-project \
  --data project_name="test-project" \
  --data project_description="Testing" \
  --data github_username=testuser \
  --data author_name="Test Author" \
  --data author_email=test@example.com \
  --data project_type=mcp_server
```

**Result**: NEW error at different location, confirming bracket delimiters ARE working, but have new conflicts.

### Identified Conflicts

#### 1. Triple Bracket Syntax Errors

**Pattern**: Markdown link syntax `[text](url)` with Jinja2 variable in text creates `[[[`:

```markdown
# BROKEN - Creates triple bracket
## [[[ project_version ]]] - 2025-10-17

# Also broken - Markdown [ + Jinja2 [[
| Repository | [[[ github_username ]]/[[ project_slug ]]](https://...) |
```

**Fixes Applied**:
- `template/CHANGELOG.md.jinja:13` - Removed extra bracket
- `template/NAMESPACES.md.jinja:134` - Converted table to bullet list
- `template/PYPI_SETUP.md.jinja:349` - Changed link text

#### 2. Markdown Link Conflicts

**Pattern**: Any markdown link starting with `[` can confuse Jinja2:

```markdown
# Jinja2 sees [ and looks for matching ]]
[Chora MCP Conventions v1.0](https://github.com/...)
[MCP Server Registry](https://github.com/...)
```

**Current Line 134** (from git):
```markdown
- **Convention**: [Chora MCP Conventions v1.0](https://github.com/...)
```

This line has NO Jinja2 variables but still causes "unexpected ']'" error, suggesting Jinja2 is confused by the markdown link `[Chora...`.

**Fix Attempted**: Wrapped in `[% raw %]` blocks:
```markdown
- **Convention**: [% raw %][Chora MCP Conventions v1.0](https://...)[% endraw %]
```

**Result**: Still fails.

#### 3. Regex Pattern Conflicts

**Pattern**: Regex character classes with adjacent brackets `[a-z][0-9]`:

```python
# In Python template files - Jinja2 sees ][ as potential delimiter
NAMESPACE_PATTERN = re.compile(r'^[a-z][a-z0-9]{2,19}$')
TOOL_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_]+:[a-z][a-z0-9_]+$')
```

**Occurrences**:
- `template/src/{{package_name}}/mcp/__init__.py.jinja` (3 patterns + 1 error message)
- `template/scripts/validate_mcp_names.py.jinja` (4 patterns)
- `template/scripts/migrate_namespace.sh.jinja` (bash grep pattern)

**Fix Applied**: Wrapped pattern definitions in `[% raw %]` blocks:
```python
[% raw %]
NAMESPACE_PATTERN = re.compile(r'^[a-z][a-z0-9]{2,19}$')
TOOL_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_]+:[a-z][a-z0-9_]+$')
[% endraw %]
```

**Result**: Still fails (but likely helped eliminate some errors).

#### 4. Markdown Tables with Jinja2 Variables

**Pattern**: Pipe delimiters `|` in tables with Jinja2 variables:

```markdown
| Tool Name | Full Name | Description | Version |
|-----------|-----------|-------------|---------|
| example_tool | [[ mcp_namespace ]]:example_tool | Example tool | [[ project_version ]] |
```

Unclear if this causes issues, but suspicious.

---

## Minimal Reproduction Test

Created isolated test to verify bracket delimiter syntax:

```python
from jinja2 import Environment

env = Environment(
    block_start_string="[%",
    block_end_string="%]",
    variable_start_string="[[",
    variable_end_string="]]",
)

template_str = """[% if True -%]
- **Namespace**: `[[ namespace ]]`
- **Project**: [[ project ]]
- **Repository**: [[ username ]]/[[ slug ]]
- **Status**: Active
[% endif -%]"""

template = env.from_string(template_str)
result = template.render(namespace="test", project="proj", username="user", slug="slug")
# SUCCESS! Renders correctly
```

**Finding**: Basic bracket delimiter syntax with `[[ var ]]/[[ var2 ]]` works perfectly in isolation.

**Conclusion**: The error is contextual - something in the FULL file context causes Jinja2 to misparse.

---

## Attempted Fixes Summary

### v2.0.8 Work-in-Progress

1. ✅ Fixed triple bracket syntax errors in 3 files
2. ✅ Wrapped regex patterns in `[% raw %]` blocks (5 files)
3. ✅ Wrapped markdown links in `[% raw %]` blocks (NAMESPACES.md.jinja)
4. ✅ Converted markdown table to bullet list (to avoid pipe conflicts)
5. ❌ Still fails with same error at line 134

### Debugging Attempts

- Checked for unclosed `[% if %]` blocks - all balanced
- Searched for `[[[` triple brackets - all fixed
- Searched for `]]]` triple close brackets - none found
- Removed NAMESPACES.md.jinja entirely - **still failed** (Copier uses cached clone)
- Verified line 134 content: `- **Status**: Active` (NO brackets at all!)
- Committed changes to force fresh clone - **still fails**

---

## The Delimiter Dilemma

### Current State

Both delimiter strategies have fundamental conflicts:

| Delimiter | Conflicts With | Requires Wrapping |
|-----------|---------------|-------------------|
| `{{ }}` (Copier 6+ default) | Python f-strings, `.format()`, dict literals, set literals | Extensive - all Python code blocks |
| `[[ ]]` (Copier <6 default) | Markdown links, regex patterns, arrays, any `[` in content | Extensive - all markdown links, regex, etc |

### Scope of Required Wrapping

For a Python project template with documentation:

**With `{{ }}` delimiters**:
- Every Python f-string: `f"Hello {name}"` → needs wrapping
- Every `.format()` call: `"Hello {}".format(name)` → needs wrapping
- Dict literals: `config = {"key": "value"}` → needs wrapping
- Set literals: `items = {1, 2, 3}` → needs wrapping
- **Estimate**: ~500+ occurrences across Python template files

**With `[[ ]]` delimiters**:
- Every markdown link: `[text](url)` → needs wrapping
- Every regex pattern: `[a-z][0-9]` → needs wrapping
- Markdown tables with variables → may need restructuring
- Any `[` that isn't Jinja2 → needs wrapping
- **Estimate**: ~300+ occurrences across markdown files

---

## Questions for Subject Matter Expert

### 1. Delimiter Strategy

**Q1**: Is there a recommended delimiter strategy for Copier templates that contain:
- Extensive Python code (with f-strings, .format(), dicts, sets)
- Extensive markdown documentation (with links, tables, code blocks)
- Regex patterns in both Python and bash scripts

**Q2**: Are there alternative delimiters that avoid both `{}` and `[]` conflicts?
- Custom delimiters: `{$ $}`, `<< >>`, `(( ))`, `{# #}` (wait, that's comments)?
- Unicode delimiters: `«« »»`, `⟦ ⟧`?
- Would Copier's Jinja2 environment accept these?

### 2. Raw Block Best Practices

**Q3**: When using `{% raw %}` / `[% raw %]` blocks:
- Should we wrap individual lines or entire sections?
- Can we wrap entire Python files in one large raw block and only "un-raw" Jinja2 variables?
- Are there performance implications for excessive raw blocks?

**Q4**: Is there a way to configure Jinja2 to be less greedy when parsing delimiters?
- Make it require whitespace: `[[ var ]]` vs `[[var]]`?
- Make it ignore brackets in certain contexts (inside code blocks, links)?

### 3. Template Design Patterns

**Q5**: For templates with extensive conflicts, what's the recommended pattern:
- A: Minimize Jinja2 variables, use more post-processing scripts?
- B: Split into multiple smaller templates with different delimiter configs?
- C: Use Jinja2 extensions or custom tags?
- D: Different templating engine entirely (Cookiecutter, custom)?

### 4. Specific Technical Questions

**Q6**: Why does Copier report line 134 error when:
- Line 134 content: `- **Status**: Active` (no brackets)
- Removing the entire file still fails (cached clone issue?)
- How can we debug the ACTUAL line causing the error?

**Q7**: The minimal test works, but full file fails. How to debug:
- Is there a way to get more verbose Jinja2 parsing errors?
- Can we see the preprocessed template before variable substitution?
- Is there a Jinja2 linting tool that understands bracket delimiters?

### 5. Alternative Approaches

**Q8**: Should we consider:
- Escaping strategies instead of raw blocks?
- Two-pass rendering (render Jinja2, then process Python)?
- Different file extensions for different delimiter configs?
- Template inheritance to separate code from docs?

---

## Repository Context

**Project**: liminalcommons/chora-base
**Purpose**: Opinionated Python project template with comprehensive tooling
**Key Features**:
- Multiple project types (mcp_server, standard, backend, cli)
- Extensive documentation generation
- MCP (Model Context Protocol) namespace conventions
- Docker support, testing infrastructure, CI/CD

**Template Stats**:
- 57 `.jinja` template files
- 1,717 Jinja2 variable references (converted to `[[ ]]`)
- ~102 `{% raw %}` blocks added (some converted to `[% raw %]`)
- Mix of Python, Markdown, YAML, Shell, Dockerfile templates

**Affected Users**: mcp-n8n team blocked from upgrading from v1.9.3 to v2.x since v2.0.0 release

---

## Reproduction Steps

### Minimum Reproduction

```bash
# Clone the template
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base
git checkout v2.0.7  # or main for v2.0.8 WIP

# Attempt to use template
cd /tmp/test-project
copier copy --force --trust /path/to/chora-base . \
  --data project_slug=test-project \
  --data project_name="test-project" \
  --data project_type=mcp_server

# Expected: Success
# Actual: TemplateSyntaxError: unexpected ']'
#   File "template/NAMESPACES.md.jinja", line 134
```

### Files of Interest

**Primary suspect**: `template/NAMESPACES.md.jinja`
- 257 lines
- Mix of Jinja2 conditionals, variables, markdown
- Contains tables, links, lists
- Line 134: `- **Status**: Active`

**Other files with conflicts**:
- `template/src/{{package_name}}/mcp/__init__.py.jinja` - Regex patterns
- `template/scripts/validate_mcp_names.py.jinja` - Regex patterns
- `template/CHANGELOG.md.jinja` - Version headers
- `template/PYPI_SETUP.md.jinja` - Markdown links

**Configuration**: `copier.yml`
- Defines `_envops` with bracket delimiters
- 322 lines of template questions and config

---

## Requested Guidance

### Immediate Need

**Primary Question**: What is the correct delimiter strategy for this use case?

We need to:
1. Successfully render Python template files with f-strings and `.format()` calls
2. Successfully render Markdown documentation with links and tables
3. Support regex patterns in Python and shell scripts
4. Minimize maintenance burden of wrapping content in raw blocks

### Long-term Strategy

**Secondary Question**: Best practices for complex Copier templates?

- Template organization patterns?
- Testing strategies for template syntax?
- CI/CD for template validation?
- Migration strategy for existing adopters (mcp-n8n stuck on v1.9.3)?

---

## Additional Resources

### Research Documents

1. `inbox/copier-jinja2-compatibility-research.md` - Research on Copier 6+ delimiter changes
2. `docs/research/copier-jinja2-compatibility-research.md` - Same, in docs folder
3. CHANGELOG.md - v2.0.0 through v2.0.7 release notes

### Bug Reports from mcp-n8n Team

1. `inbox/chora-base-v205-verification.md` - Verification that v2.0.5 failed
2. `inbox/chora-base-v206-still-fails.md` - Verification that v2.0.6 failed
3. `inbox/mcp-n8n-v207-comments.md` - Verification that v2.0.7 failed

### Relevant Commits

- v2.0.7: feat(template): Implement bracket delimiters to fix Jinja2 conflicts
- Work-in-progress: Multiple commits attempting v2.0.8 fixes

---

## Appendix: Example Content Conflicts

### Example 1: Python Regex in Template

**File**: `template/src/{{package_name}}/mcp/__init__.py.jinja`

```python
# Lines 28-35 (simplified)
NAMESPACE_PATTERN = re.compile(r'^[a-z][a-z0-9]{2,19}$')
TOOL_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_]+:[a-z][a-z0-9_]+$')

# Also has Jinja2 variables on other lines
NAMESPACE = "[[ mcp_namespace ]]"
ENABLE_VALIDATION = [[ mcp_validate_names | lower ]]
```

**Conflict**: Jinja2 parser sees `][` in regex and gets confused.

**Current Fix**: Wrapped in `[% raw %]` ... `[% endraw %]`

### Example 2: Markdown Link in Template

**File**: `template/NAMESPACES.md.jinja`

```markdown
## References

- [Chora MCP Conventions v1.0](https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
```

**Conflict**: Jinja2 sees `[Chora` and looks for matching `]]`.

**Current Fix**: Wrapped in `[% raw %]` ... `[% endraw %]`
**Status**: STILL FAILS - suggesting this isn't the fix

### Example 3: Markdown Table with Variables

**File**: `template/NAMESPACES.md.jinja`

```markdown
| Tool Name | Full Name | Description | Version |
|-----------|-----------|-------------|---------|
| example_tool | [[ mcp_namespace ]]:example_tool | Example tool | [[ project_version ]] |
```

**Conflict**: Pipe `|` characters and variables together - unclear if problematic.

### Example 4: The Mysterious Line 134

**Current Content**:
```markdown
133: - **Repository**: [[ github_username ]]/[[ project_slug ]]
134: - **Status**: Active
135: - **Convention**: [% raw %][Chora MCP Conventions v1.0](https://...)[% endraw %]
```

**Error**: Line 134 - "unexpected ']'"
**Mystery**: Line 134 has NO brackets!

**Theory**: Error line numbers in Jinja2 may be off, or error is from earlier line but reported at 134.

---

## Contact

For questions about this investigation:
- **Repository**: https://github.com/liminalcommons/chora-base
- **Issue Tracker**: https://github.com/liminalcommons/chora-base/issues
- **Affected User**: mcp-n8n team (@vlct0rs-github-acct)

**Current Status**: Blocked on finding working delimiter strategy for v2.0.8 release.

---

**Report Date**: 2025-10-22
**Template Version**: v2.0.7 (released), v2.0.8 (WIP)
**Copier Version**: 9.10.3
**Python Version**: 3.11+
**Jinja2 Version**: 3.1.x (via Copier)
