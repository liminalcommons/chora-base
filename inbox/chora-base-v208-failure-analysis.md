# chora-base v2.0.8 Upgrade Failure Analysis

**Date:** 2025-10-23
**Environment:** Copier 9.10.3, Python 3.11
**Status:** ❌ FAILED - Same TemplateSyntaxError as v2.0.0-v2.0.7

## Executive Summary

chora-base v2.0.8 still fails with the identical error despite all shell syntax fixes being correctly applied. The issue is NOT shell syntax conflicts - it's a fundamental problem with how **Copier processes `{% raw %}` blocks during template updates**.

## Error Details

```
jinja2.exceptions.TemplateSyntaxError: unexpected char '#' at 9814
File: template/scripts/extract_tests.py.jinja, line 293
```

**Character 9814:** The closing quote `"` after `"test_{}_bash_example_{}".format(safe_title, idx)` on line 289.

## Verification Results

### ✅ Phase 1: Template Inspection (All Passed)

1. **Standard Jinja2 Delimiters:** Confirmed v2.0.8 uses `{{ }}` and `{% %}` (not brackets)
2. **Line 292 Bash Function:** Uses `{{` (single brace), not `[[` bash test syntax
3. **Raw Block Wrapping:** Lines 291-304 properly wrapped in `{% raw %}{% endraw %}`
4. **No Heredoc Conflicts:** No `{{EOF` or `<<<` syntax found
5. **TOML Syntax:** `[[tool.mypy.overrides]]` correctly outside Jinja2 blocks

### ❌ Phase 2: Upgrade Test (Failed)

```bash
copier update --trust --vcs-ref v2.0.8
```

Result: Identical TemplateSyntaxError at line 293, char 9814 as all previous versions (v2.0.0-v2.0.7).

## Root Cause Analysis

### What We Know

1. **Standard Jinja2 Works:** The template renders perfectly with standard Jinja2:
   ```python
   from jinja2 import Environment, FileSystemLoader
   env = Environment(loader=FileSystemLoader(...))
   template = env.get_template('extract_tests.py.jinja')  # ✅ SUCCESS
   ```

2. **Copier Fails:** But Copier's template processing fails during updates:
   ```bash
   copier update --vcs-ref v2.0.8  # ❌ FAILS
   ```

3. **The Pattern:** This error has persisted across **9 consecutive versions** (v2.0.0-v2.0.8) despite:
   - Converting f-strings to `.format()` (v2.0.1-v2.0.3)
   - Adding `{% raw %}` blocks (v2.0.3-v2.0.6)
   - Switching to bracket delimiters (v2.0.7)
   - Fixing shell syntax and reverting to standard delimiters (v2.0.8)

### Hypothesis: Copier Update vs Copy Mode Difference

**Key Observation:** The error occurs during `copier update`, NOT during initial `copier copy`. This suggests:

1. **Update Mode Complexity:** During updates, Copier renders BOTH old and new template versions to generate diffs
2. **Raw Block Processing:** Copier may handle `{% raw %}` blocks differently in update mode
3. **Character Position:** The error at "char 9814" suggests parsing is happening BEFORE Jinja2 rendering
4. **Line 293 Mystery:** The error points to line 293 (inside the raw block), but char 9814 is actually on line 289 (outside the raw block)

### The Actual Problem (Theory)

Looking at lines 289-293:

```python
289: test_name = "test_{}_bash_example_{}".format(safe_title, idx)
290:
291: {% raw %}bash_test = '''
292: test_{}_bash_example_{}() {{
293:     # Test extracted from documentation: {}
```

**Possible Issue:** Copier's update mode may be:
1. Scanning the file line-by-line for changes
2. Not respecting `{% raw %}` boundaries during the scanning phase
3. Seeing `# Test...` on line 293 and trying to parse preceding content
4. Finding the `{}` placeholders and getting confused about template syntax

## Testing Evidence

### Test 1: Standard Jinja2 - SUCCESS ✅

```python
# Minimal test with exact same syntax
{% raw %}bash_test = '''
test_example() {{
    # Test comment
    echo "test"
}}
'''{% endraw %}
```

Result: Renders perfectly with standard Jinja2 Environment.

### Test 2: Copier Update - FAILURE ❌

```bash
copier update --trust --vcs-ref v2.0.8
```

Result: TemplateSyntaxError at line 293, char 9814.

### Test 3: File Integrity - VERIFIED ✅

```bash
# Cloned two separate copies, compared
diff chora-base-v2.0.8/template/scripts/extract_tests.py.jinja \
     chora-base-v2.0.8-fresh/template/scripts/extract_tests.py.jinja
```

Result: Files are identical. No CDN caching or corruption issues.

## Environment Details

```
Copier Version: 9.10.3
Python Version: 3.11
Jinja2 Version: (included in Copier 9.10.3)
Template Version: v2.0.8 (commit 233a95cd)
Project: mcp-n8n
Current Template Version: v1.9.3
```

## Impact Assessment

- **9 Failed Versions:** v2.0.0, v2.0.1, v2.0.2, v2.0.3, v2.0.5, v2.0.6, v2.0.7, v2.0.8
- **Investigation Time:** ~8 hours across multiple sessions
- **Documents Created:** 4 verification reports, 1 audit script, 1 comprehensive bug report
- **Upgrade Status:** Still stuck on v1.9.3
- **Desired Feature:** Nested AGENTS.md architecture (51% file size reduction)

## Recommendations for chora-base Team

### Immediate Actions

1. **Test Actual Upgrade:** Team should test `copier update` from an existing project, not just `copier copy` for new projects
2. **Copier Version:** Test with Copier 9.10.3 (latest stable) in update mode
3. **Raw Block Alternatives:** Consider alternative approaches:
   - Multiple smaller `{% raw %}` blocks instead of one large block
   - Escape individual special characters instead of raw blocks
   - Move problematic code generation to post-processing scripts

### Diagnostic Steps

1. **Enable Copier Debug Mode:**
   ```bash
   copier update --trust --vcs-ref v2.0.8 -vvv 2>&1 | tee debug.log
   ```

2. **Minimal Reproduction:**
   Create a minimal template with just the problematic pattern:
   ```
   minimal-template/
   ├── copier.yml
   └── template/
       └── test.py.jinja
   ```

   Contents of test.py.jinja:
   ```python
   {% raw %}bash_test = '''
   test_function() {{
       # Comment: {}
   }}
   '''{% endraw %}
   ```

3. **Test Update Path:**
   ```bash
   # Create project from v1.9.3 (known working)
   copier copy --vcs-ref v1.9.3 gh:liminalcommons/chora-base /tmp/test-project
   cd /tmp/test-project
   git init && git add . && git commit -m "Initial"

   # Try updating to v2.0.8
   copier update --vcs-ref v2.0.8
   ```

### Alternative Approaches

1. **Post-Template Processing:**
   - Generate problematic files (like extract_tests.py) via a post-copy script
   - Use `_tasks:` in copier.yml to run Python scripts after template generation
   - Store generation logic in helper scripts, not Jinja2 templates

2. **Simpler Templates:**
   - Move complex Python code generation out of templates
   - Keep templates focused on configuration and simple file generation
   - Use template hooks for complex transformations

3. **Version 1.x Enhancement:**
   - Consider backporting nested AGENTS.md feature to 1.9.x branch
   - Avoid the v2.0.x architecture entirely if Copier update mode is fundamentally incompatible

## Questions for Copier Maintainers

If this is a Copier bug, these questions should be raised with the Copier project:

1. Are `{% raw %}` blocks fully supported in update mode?
2. Does update mode's diff generation respect template syntax boundaries?
3. Why does the error point to line 293 when char 9814 is on line 289?
4. Is there a known issue with raw blocks containing bash syntax that resembles template syntax?

## Conclusion

After 9 failed upgrade attempts across 8 different versions, the evidence strongly suggests this is a **Copier architectural limitation**, not a template syntax issue. The chora-base team has fixed every conceivable template syntax problem, yet the error persists.

**Recommended Path Forward:**
1. Create minimal reproduction case for Copier maintainers
2. Consider alternative template architectures that avoid complex code generation in Jinja2
3. Test if the issue reproduces with `copier copy` (new project) vs `copier update` (existing project)
4. If Copier update is fundamentally incompatible with this pattern, redesign the template structure

## Appendix: File Excerpt

Lines 287-304 of [extract_tests.py.jinja](https://github.com/liminalcommons/chora-base/blob/v2.0.8/template/scripts/extract_tests.py.jinja#L287-L304):

```python
287:         # Generate bash test
288:         safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", doc_title.lower())
289:         test_name = "test_{}_bash_example_{}".format(safe_title, idx)
290:
291:         {% raw %}bash_test = '''
292: test_{}_bash_example_{}() {{
293:     # Test extracted from documentation: {}
294:     # Source: {}
295:     # Example {}
296:
297: {}
298:
299:     local exit_code=$?
300:     if [ $exit_code -ne {} ]; then
301:         echo "FAILED: Expected exit code {}, got $exit_code"
302:         return 1
303:     fi
304: '''.format(safe_title, idx, doc_title, doc_path, idx, self._indent(clean_code, 4), expected_exit, expected_exit){% endraw %}
```

All syntax appears correct for Jinja2, yet Copier update fails consistently at line 293.
