# Copier Jinja2 template syntax error: Root cause and solution

**Copier uses a fundamentally different Jinja2 environment than standard Jinja2, with multiple architectural differences that cause the paradoxical parsing behavior you're experiencing. The error persists because Python comments inside improperly scoped Jinja2 blocks are being parsed as template syntax, not because of format strings.**

## Root cause: Python comments inside Jinja2 context

The error "unexpected char '#' at 9814" on line 293 indicates **a Python comment character (`#`) appearing where Jinja2 expects template syntax**. Character position 9814 at line 293 averages 33.5 characters per line—completely reasonable for Python code with imports, docstrings, and whitespace.

### Why this happens

Jinja2's lexer calculates character position as an **absolute offset from file start**, counting every character including content inside `{% raw %}` blocks. When Jinja2 encounters `#` at position 9814, it's attempting to parse that location as template syntax, which means either:

1. **Broken raw block scope**: A `{% raw %}` block isn't properly closed, causing subsequent Python code to be parsed as Jinja2
2. **Comment inside Jinja2 block**: Python-style `#` comments appearing inside `{{ }}` or `{% %}` blocks
3. **Extension preprocessing conflict**: Custom Jinja2 extensions modifying template before parsing

### The critical difference: Copier vs standard Jinja2

Your templates successfully parse with standard Jinja2 but fail with Copier because **Copier uses `SandboxedEnvironment` with pre-loaded extensions**, not the standard `Environment`:

```python
# Copier's initialization (copier/main.py)
env = jinja2.sandbox.SandboxedEnvironment(
    loader=loader,
    extensions=extensions,  # Multiple extensions auto-loaded
    **self.template.envops
)
```

**Extensions automatically loaded by Copier**:
- `jinja2_ansible_filters.AnsibleCoreFiltersExtension`
- `jinja2_copier_extension.CopierExtension` 
- Custom `YieldExtension` for file generation loops
- Any extensions specified in `_jinja_extensions`

These extensions can preprocess templates, modify parsing behavior, and introduce subtle incompatibilities—especially during `copier update` operations.

## Why copier update fails but standard parsing succeeds

**Update operation complexity**: Unlike `copier copy`, the update command:

1. Clones **old template version** to temporary directory
2. Clones **new template version** to separate temporary directory  
3. Regenerates old version output with potentially incompatible dependencies
4. Performs three-way merge (old output, current project, new output)
5. Each version may use different Jinja2 configurations or extension versions

**GitHub Issue #1170** documents this exact problem: "Update fails when Jinja extension has breaking changes." The update algorithm regenerates the old template with new dependencies, causing `TemplateAssertionError` or `TemplateSyntaxError` that wouldn't occur during simple copy operations.

### Delimiter history matters

**Critical version change**: Copier 6.0 switched from bracket delimiters `[[ ]]` to curly braces `{{ }}` as defaults. If your template was created before Copier 6 or users have older Copier versions cached:

- **Copier 5 defaults**: `[[` `]]` for variables, `[%` `%]` for blocks  
- **Copier 6+ defaults**: `{{` `}}` for variables, `{%` `%}` for blocks

Python `.format()` strings with `{}` **would not conflict** with Copier 5's bracket delimiters, but **do conflict** with Copier 6+'s curly brace delimiters.

## Recommended fix: Configure custom delimiters via _envops

**This is the Copier-approved solution** documented in best practices and official configuration guides. Add this to your `copier.yml`:

```yaml
_min_copier_version: "6.0.0"
_templates_suffix: .jinja

_envops:
  # Use bracket delimiters to avoid conflicts with Python's {}
  block_start_string: "[%"
  block_end_string: "%]"
  variable_start_string: "[["
  variable_end_string: "]]"
  comment_start_string: "[#"
  comment_end_string: "#]"
  
  # Whitespace control for clean output
  trim_blocks: true
  keep_trailing_newline: true
  lstrip_blocks: true
```

### Benefits of this approach

1. **No escaping required**: Python code with `{}`, `.format()`, f-strings, and dictionaries works without modification
2. **Clean, readable templates**: No verbose `{% raw %}{% endraw %}` blocks cluttering code
3. **Maintainable**: Easier to read and modify compared to extensive raw blocks
4. **Recommended by Copier community**: Explicitly documented in "Effective Repository Templates with Copier" best practices guide
5. **Prevents future issues**: Eliminates entire class of delimiter conflicts

### Example: Your Python template with bracket delimiters

```python
# extract_tests.py.jinja (using bracket delimiters)
#!/usr/bin/env python3
"""
[[ project_name ]] - Test extraction script
"""

def extract_test_data(test_file: str) -> dict:
    """Extract test data using format strings."""
    # These {} braces are literal - no conflicts!
    pattern = "test_{}"
    result = pattern.format(test_file)
    
    config = {
        'project': '[[ project_name ]]',  # Template variable
        'version': '[[ version ]]',       # Template variable
        'test_pattern': 'test_{}',        # Literal Python - no escaping
        'data_format': '{key}={value}'    # Literal Python - no escaping
    }
    
    # Python comments work fine outside Jinja2 blocks
    # Even with # characters, no parsing conflicts
    return config
```

## Alternative solutions (if custom delimiters aren't viable)

### Option 1: Fix raw block scope issues

If you must continue using `{% raw %}` blocks, ensure they have proper scope. The most common issue is **nesting or unclosed blocks**:

```python
# INCORRECT - comment after raw block
{% raw %}
config = "test_{}"
{% endraw %}  # This comment breaks parsing in some contexts

# CORRECT - no trailing content
{% raw %}
config = "test_{}"
{% endraw %}

# CORRECT - multi-line with clean boundaries  
{% raw %}
def format_test(name):
    # Python comments inside raw blocks are fine
    return "test_{}".format(name)
{% endraw %}
```

**Key insight from research**: Inline `{% raw %}{% endraw %}` blocks are discouraged. Use multi-line raw blocks with clear opening/closing on separate lines when possible.

### Option 2: Escape with string literals

For occasional literal braces, use Jinja2 string expressions:

```python
# Template with mixed Jinja2 and literal braces
config_template = {{ "'{}'"|format(variable_name) }}

# For dictionaries
dict_pattern = {{ '{}' }}  # Outputs literal {}
```

**Disadvantage**: Extremely hard to read and maintain for extensive Python code. The community consensus is this "looks awful" and should be avoided.

### Option 3: Use numbered format placeholders

Python's format strings support numbered placeholders:

```python
# Instead of positional
"test_{}".format(value)

# Use numbered (easier to escape if needed)
"test_{0}".format(value)
"pattern_{0}_{1}".format(key, value)
```

This doesn't solve the Copier issue but makes code more explicit and slightly easier to escape when necessary.

## Configuration checklist for immediate fix

**Step 1**: Verify your Copier version and template compatibility
```bash
copier --version  # Should be 6.0.0+
```

**Step 2**: Add `_envops` configuration to `copier.yml`
```yaml
_min_copier_version: "6.0.0"

_envops:
  block_start_string: "[%"
  block_end_string: "%]"
  variable_start_string: "[["  
  variable_end_string: "]]"
  comment_start_string: "[#"
  comment_end_string: "#]"
  keep_trailing_newline: true
```

**Step 3**: Convert existing Jinja2 syntax in templates
```bash
# Find all template files
find template/ -name "*.jinja" -type f

# Convert {{ variable }} to [[ variable ]]
# Convert {% block %} to [% block %]
# Convert {# comment #} to [# comment #]
```

**Step 4**: Remove unnecessary `{% raw %}` blocks
Since Python's `{}` won't conflict with `[[ ]]` delimiters, you can remove all the raw blocks wrapping `.format()` calls.

**Step 5**: Test both operations
```bash
# Test copy
copier copy . /tmp/test-copy

# Test update (critical - this is where failures occur)
copier update /tmp/test-copy
```

## Special consideration for line 293

To debug the specific error at character position 9814, line 293:

1. **Count 9814 characters** from file start (including newlines) to find the exact error location
2. **Look for these patterns** near that position:
   - `{{ variable # comment }}` - Python comment inside Jinja2 expression
   - `{% if condition # comment %}` - Python comment inside Jinja2 statement  
   - `{% endraw %}` followed by Python code with `#` - raw block scope issue
3. **Check for unclosed blocks** before line 293 that would cause subsequent Python to be parsed as Jinja2

The '#' character error almost always indicates Python comments being interpreted as Jinja2 syntax, which means a scoping issue in your template structure.

## Why format() wrapping failed (v2.0.1-v2.0.6)

Your attempts to wrap all `.format()` calls in `{% raw %}` blocks failed because:

1. **The problem isn't format strings**: It's Python `#` comments being parsed as Jinja2 syntax
2. **Raw blocks don't prevent all parsing**: Extensions can still preprocess content; raw blocks only affect core Jinja2 lexer
3. **Update operation regenerates with different context**: Old template version parsed with new dependencies causes incompatibilities
4. **Delimiter conflicts remain**: Even with raw blocks, `{{ }}` delimiters in Copier 6+ conflict with Python's `{}`

## Copier bug or misuse?

**This is documented behavior, not a bug**, but the interaction is poorly explained:

- **Intended**: Copier 6.0 changed delimiters for better IDE support
- **Intended**: Update operation regenerates old templates for three-way merge
- **Intended**: Extensions modify parsing behavior
- **Poorly documented**: How extensions interact during updates
- **Poorly documented**: Migration path for templates with Python code
- **Known limitation**: Issue #1170 documents update failures with extension changes

## Success metrics

Your fix will be successful when:

1. ✅ **Standard rendering works**: `copier copy` executes without errors
2. ✅ **Update operations succeed**: `copier update` completes successfully  
3. ✅ **Clean template code**: No verbose `{% raw %}` blocks required
4. ✅ **Version compatibility**: Works across Copier 6.0+ versions
5. ✅ **Extension compatibility**: Update works even with extension version changes

## Immediate workaround (if configuration change isn't possible)

If you cannot modify `copier.yml` immediately:

1. **Use `copier recopy`** instead of `copier update` to bypass smart merge:
```bash
copier recopy --force /path/to/project
```

2. **Pin Copier version** to avoid delimiter changes:
```bash
pip install copier==5.1.0  # Uses bracket delimiters by default
```

3. **Manually fix line 293**: Find and remove Python `#` comments from inside any `{{ }}` or `{% %}` blocks at that location

## Additional resources

- **Copier configuration docs**: https://copier.readthedocs.io/en/stable/configuring/
- **Best practices guide**: "Effective Repository Templates with Copier" (browniantech.com)
- **Issue #1170**: Update failures with extension changes
- **Issue #247**: Delimiter change discussion (Copier 6.0 breaking change)
- **Jinja2 escaping**: https://jinja.palletsprojects.com/en/stable/templates/#escaping

## Conclusion

The root cause is **Copier 6+'s curly brace delimiters conflicting with Python syntax**, combined with **the update operation's complex three-way merge** that regenerates templates with potentially incompatible extensions. The solution is **configuring bracket delimiters via `_envops`** in `copier.yml`, which eliminates all conflicts and is the officially recommended approach for templates containing Python code.

Your seven release attempts failed because wrapping format strings in raw blocks doesn't address the underlying delimiter conflict or the Python comments being parsed as Jinja2 syntax. Custom delimiters solve both problems cleanly and permanently.