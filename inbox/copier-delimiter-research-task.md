# Research Task: Template System Delimiter Strategy for Mixed Python/Markdown Content

**Date**: 2025-10-22
**Project**: chora-base (Python project template)
**Status**: BLOCKED - 8 failed releases (v2.0.0-v2.0.7)
**Time Invested**: 15+ hours across multiple debugging sessions
**Current Tool**: Copier 9.10.3 with Jinja2 templating

---

## Executive Summary

We need to discover **mature, production-tested strategies** for using template systems (specifically Copier/Jinja2) with content that contains:

1. **Python code** with f-strings, `.format()`, dicts, sets (uses curly braces `{}`)
2. **Markdown documentation** with links, tables, code blocks (uses square brackets `[]`)
3. **Regex patterns** with character classes (uses square brackets `[]`)
4. **YAML configuration** with nested structures
5. **Shell scripts** with variable interpolation

The core problem: **Jinja2's default delimiters conflict with Python syntax**, and our attempts to use alternative delimiters have failed due to what appears to be a Copier bug.

**Research Goal**: Find mature, proven approaches to this problem that are actually working in production template systems.

---

## Problem Context

### What We're Building

**chora-base** is a Copier template for Python projects that generates:

- Python packages with MCP (Model Context Protocol) servers
- Backend services with FastAPI
- CLI tools with typer/click
- Standard Python libraries

The template contains **66 .jinja files** totaling ~10,000 lines of mixed content including Python source code, Markdown docs, YAML configs, Shell scripts, and Dockerfiles.

### Why This Matters

- **Current adopter blocked**: mcp-n8n team stuck on v1.9.3, cannot upgrade due to template errors
- **8 consecutive failed releases**: v2.0.0 through v2.0.7 all failed with TemplateSyntaxError
- **Production impact**: Template system is core infrastructure for multiple projects
- **Update mechanism critical**: Copier's built-in update feature is valuable for keeping adopters current

---

## The Delimiter Conflict Problem

### Root Issue

Jinja2 template engines use delimiters to distinguish template syntax from literal content:

- **Variables**: `{{ variable }}`
- **Blocks**: `{% if condition %} ... {% endif %}`
- **Comments**: `{# comment #}`

But Python code **also uses curly braces** for:
- **F-strings**: `f"Hello {name}"`
- **`.format()`**: `"Hello {}".format(name)`
- **Dictionaries**: `{"key": "value"}`
- **Sets**: `{1, 2, 3}`

When a Jinja2 template contains Python code, the template engine sees `{` and tries to parse it as template syntax, causing syntax errors.

### Example Conflict

**Template file**: `template/src/app.py.jinja`

```python
def greet(name: str) -> str:
    """Greet user with formatted string."""
    return f"Hello {name}!"  # Template engine sees {name} as Jinja2 variable!
```

**Copier 6+ behavior**: Tries to render `{name}` as template variable, fails with TemplateSyntaxError.

---

## What We've Tried (Chronological)

### Attempt 1: Raw Blocks Around Python Code (v2.0.0-v2.0.2)

**Strategy**: Wrap Python code in `{% raw %}` blocks to prevent template processing.

**Implementation**:
```python
{% raw %}
def greet(name: str) -> str:
    return f"Hello {name}!"
{% endraw %}
```

**Result**: ❌ FAILED
- Missed hundreds of f-strings across 66 files
- Required wrapping ~500+ code sections
- Still had conflicts with `.format()` and dict literals
- v2.0.1 fixed some, v2.0.2 fixed more, v2.0.3 attempted comprehensive fix
- mcp-n8n team reported **all three versions still fail**

**Time spent**: ~8 hours across three release attempts

### Attempt 2: `.format()` Raw Wrapping (v2.0.4-v2.0.6)

**Strategy**: Focus specifically on wrapping `.format()` calls since they were identified in error messages.

**Implementation**:
```python
{% raw %}
message = "Value: {}".format(value)
{% endraw %}
```

**Result**: ❌ FAILED
- Even after wrapping all identified `.format()` calls
- New errors appeared in different files
- Whack-a-mole problem: fixing one file revealed errors in another

**Time spent**: ~4 hours

### Attempt 3: Square Bracket Delimiters (v2.0.7)

**Strategy**: Switch Copier to use bracket delimiters `[[ ]]` and `[% %]` to avoid Python curly brace conflicts.

**Implementation**:
```yaml
# copier.yml
_envops:
  variable_start_string: "[["
  variable_end_string: "]]"
  block_start_string: "[%"
  block_end_string: "%]"
```

**Result**: ❌ FAILED with new error
```
jinja2.exceptions.TemplateSyntaxError: unexpected ']'
File "template/NAMESPACES.md.jinja", line 134
```

**Root cause**: Bracket delimiters conflict with:
- **Markdown links**: `[text](url)`
- **Regex patterns**: `[a-z][0-9]+`
- **Any square bracket content**

**Time spent**: ~2 hours

### Attempt 4: Angle Bracket Delimiters (v2.0.8 WIP)

**Strategy**: Use angle bracket delimiters `<< >>` and `<% %>` to avoid conflicts with both Python `{}` and Markdown `[]`.

**Expert recommendation**: Based on research document analysis by subject matter expert.

**Implementation**:
```yaml
# copier.yml
_envops:
  variable_start_string: "<<"
  variable_end_string: ">>"
  block_start_string: "<%"
  block_end_string: "%>"
  comment_start_string: "<#"
  comment_end_string: "#>"
```

**Migration process**:
1. Created automated migration script: `scripts/migrate-to-angle-brackets.sh`
2. Successfully converted all 66 .jinja files (2,716 delimiter tokens)
3. Removed unnecessary `<% raw %>` blocks (9 total)
4. Committed all changes

**Testing with standalone Jinja2**:
```python
from jinja2 import Environment

env = Environment(
    block_start_string="<%",
    block_end_string="%>",
    variable_start_string="<<",
    variable_end_string=">>",
)

with open('template/NAMESPACES.md.jinja') as f:
    template = env.from_string(f.read())
    result = template.render(...)  # ✅ SUCCESS - renders perfectly
```

**Testing with Copier**:
```bash
copier copy --force --trust . /tmp/test \
  --data project_type=mcp_server

# ❌ FAILED: Same error as v2.0.7!
# jinja2.exceptions.TemplateSyntaxError: unexpected ']'
# File "template/NAMESPACES.md.jinja", line 134
```

**Critical finding**: THE EXACT SAME ERROR despite completely different delimiters!

**Time spent**: ~6 hours

### Attempt 5: Eliminate ALL Square Brackets from NAMESPACES.md.jinja

**Strategy**: Since error mentions `]`, remove every single square bracket from the file.

**Actions taken**:
1. Removed all markdown links: `[text](url)` → plain text + URL
2. Wrapped all regex patterns in `<% raw %>` blocks
3. Converted markdown tables to bullet lists
4. Replaced regex notation with prose descriptions:
   - **Before**: `[a-z][0-9]+`
   - **After**: "Start with lowercase letter, continue with lowercase letters, digits, or underscores"
5. Verified zero square brackets: `grep -c "\[" template/NAMESPACES.md.jinja` → **0**

**Final line 134 content**: `  - Start with a lowercase letter (a through z)` (NO BRACKETS!)

**Standalone Jinja2 test**:
```bash
python3 test_template.py
✓ NAMESPACES.md.jinja syntax is VALID with angle brackets!
✓ Template RENDERS successfully!
  Rendered 7000 characters
```

**Copier test**:
```bash
copier copy --force --trust . /tmp/test --data project_type=mcp_server

# ❌ STILL FAILS!
# jinja2.exceptions.TemplateSyntaxError: unexpected ']'
# File "template/NAMESPACES.md.jinja", line 134
```

**Time spent**: ~8 hours

**Total time across all attempts**: ~28 hours

---

## Critical Evidence of Copier Bug

### The Smoking Gun

1. ✅ **Template syntax is VALID** - standalone Jinja2 parses and renders successfully
2. ✅ **Zero square brackets in file** - verified with `grep -c "\[" = 0`
3. ✅ **Line 134 has no brackets** - contains only: `  - Start with a lowercase letter (a through z)`
4. ❌ **Copier STILL reports "unexpected ']'" at line 134**

### Hypothesis: Copier NOT Respecting `_envops`

**Evidence**:
- Error message mentions `]` (square bracket), not `>` (angle bracket)
- Error location (line 134) unchanged despite file content completely rewritten
- Same delimiter tokens `[[ ]]` appear in error despite config using `<< >>`
- Standalone Jinja2 with same `_envops` works perfectly

**Hypothesis**: Copier's Jinja2 environment initialization does NOT properly apply `_envops` delimiter configuration, causing it to still attempt parsing with bracket delimiters even though angle brackets are configured.

### Copier-Specific Behavior

**Copier's template processing**:
1. Creates VCS clone in temp directory: `/private/var/folders/.../copier._vcs.clone.*/`
2. Initializes SandboxedEnvironment (not standard Environment)
3. Applies `_envops` configuration (allegedly)
4. Compiles templates
5. Renders to output directory

**Possible bug locations**:
- `_envops` not being passed to SandboxedEnvironment correctly
- SandboxedEnvironment ignoring delimiter configuration in some code paths
- Template pre-processing step that doesn't respect delimiters
- VCS cloning process interfering with configuration

---

## Research Questions

### Primary Questions

1. **Are there known bugs with Copier's `_envops` delimiter configuration?**
   - Has anyone successfully used angle bracket delimiters `<< >>` with Copier?
   - Are there open/closed issues about delimiter configuration not being respected?
   - What versions of Copier have reliable delimiter support?

2. **What are production-tested delimiter strategies for mixed Python/Markdown templates?**
   - How do large Python projects (Django, Flask, FastAPI templates) handle this?
   - What delimiter combinations are proven to work in production?
   - Are there template repositories we can study as reference implementations?

3. **Is Copier the right tool for this use case?**
   - What are the alternatives?
   - What are the tradeoffs? (update mechanism, community, maturity)
   - Is there a template system specifically designed for mixed-syntax content?

### Technical Deep-Dive Questions

4. **How does Copier's SandboxedEnvironment differ from standard Jinja2 Environment?**
   - Does it have different parsing behavior?
   - Are there security restrictions that affect delimiter configuration?
   - Source code analysis: where does `_envops` get applied?

5. **Can we create a minimal reproduction case for the Copier bug?**
   - Simplest possible template that triggers the issue
   - Exact Copier version and configuration
   - Comparison with standalone Jinja2

6. **What workarounds exist?**
   - Post-processing scripts to handle templates separately?
   - Hybrid approach (different engines for different file types)?
   - Template pre-compilation step?

### Alternative Approaches

7. **Could we use a different template syntax entirely?**
   - Mako templates (uses `${}` for variables)
   - Chevron/Mustache (uses `{{ }}` but simpler logic)
   - Custom template engine

8. **Should we split templates by content type?**
   - Python files use one delimiter set
   - Markdown files use another
   - Separate Copier configurations per type?

9. **Is there a way to escape delimiters globally?**
   - Configuration option we're missing?
   - Jinja2 extension that handles escaping automatically?

### Production Examples

10. **What do these projects do?**
    - **cookiecutter-django**: How do they handle Django templates (which also use `{{ }}`)?
    - **copier-poetry**: How do they handle Python source in templates?
    - **Full Stack FastAPI Template**: Mixed Python/docs, what's their strategy?
    - **python-package-template**: Any insights from minimal templates?

---

## Requirements for Ideal Solution

### Must Have

1. **Handle Python source code** with f-strings, `.format()`, dicts, sets
2. **Handle Markdown documentation** with links, tables, code blocks
3. **Handle regex patterns** with character classes
4. **Support template updates** (not just initial generation)
5. **Work reliably** - no mysterious parsing errors
6. **Be maintainable** - minimal wrapping/escaping noise

### Should Have

7. **Active community** - bugs get fixed, questions get answered
8. **Good documentation** - clear guidance on delimiter strategies
9. **Production proven** - used successfully by major projects
10. **CI/CD friendly** - can validate templates automatically

### Nice to Have

11. **IDE support** - syntax highlighting, autocomplete
12. **Dry run mode** - preview changes without writing
13. **Partial updates** - update specific files, not whole template

---

## Success Criteria

A successful solution would:

1. ✅ **Generate all project types** without TemplateSyntaxError
2. ✅ **Allow updates** via `copier update` or equivalent
3. ✅ **Require minimal escaping** (< 10% of content wrapped in raw blocks)
4. ✅ **Work consistently** across Python, Markdown, YAML, Shell content
5. ✅ **Be documented** with clear rationale and examples
6. ✅ **Be tested** in CI/CD to prevent regressions

---

## Context for Researchers

### Our Technology Stack

- **Python**: 3.11+
- **Copier**: 9.10.3 (installed via pipx)
- **Jinja2**: 3.1.x (Copier's dependency)
- **Git**: Version control for template and generated projects
- **Project types**: mcp_server, backend, cli, standard

### Template Structure

```
chora-base/
├── copier.yml                    # Main configuration
├── template/                     # Template files
│   ├── src/
│   │   └── {{package_name}}/    # Python source
│   │       ├── __init__.py.jinja
│   │       ├── mcp/
│   │       │   ├── __init__.py.jinja  # Regex patterns
│   │       │   └── server.py.jinja    # Python code
│   ├── docs/
│   │   └── *.md.jinja           # Markdown documentation
│   ├── NAMESPACES.md.jinja      # Current blocker file
│   ├── pyproject.toml.jinja     # TOML config
│   └── scripts/
│       └── *.sh.jinja           # Shell scripts
```

### File We're Stuck On

**template/NAMESPACES.md.jinja** (334 lines):
- Pure Markdown documentation
- Contains Jinja2 conditionals: `<% if mcp_enable_namespacing -%>`
- Contains Jinja2 variables: `<< project_name >>`
- **Zero square brackets** (verified)
- **Renders perfectly** in standalone Jinja2
- **Fails in Copier** with "unexpected ']'" at line 134

### How to Reproduce

```bash
# Clone template
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base

# Attempt to generate project
copier copy --force --trust . /tmp/test-project \
  --data project_type=mcp_server \
  --data project_name="Test Project" \
  --data project_slug=test-project

# Error:
# jinja2.exceptions.TemplateSyntaxError: unexpected ']'
# File "template/NAMESPACES.md.jinja", line 134
```

### Standalone Jinja2 Test (Works)

```python
from jinja2 import Environment

env = Environment(
    block_start_string="<%",
    block_end_string="%>",
    variable_start_string="<<",
    variable_end_string=">>",
    comment_start_string="<#",
    comment_end_string="#>",
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)

with open('template/NAMESPACES.md.jinja') as f:
    template = env.from_string(f.read())

result = template.render(
    project_name="Test Project",
    mcp_namespace="test",
    mcp_enable_namespacing=True,
    # ... other variables
)

print(f"✓ Rendered {len(result)} characters successfully!")
# Output: ✓ Rendered 7000 characters successfully!
```

---

## What We Need from Research

### Immediate (Hours)

1. **Copier bug confirmation or denial**
   - Is this a known issue?
   - Are we misconfiguring something?
   - What's the correct way to use custom delimiters?

2. **Working examples**
   - Show us a template that uses angle brackets successfully
   - Or show us the "right" delimiter strategy for mixed content

### Short-term (Days)

3. **Alternative approaches**
   - If Copier is broken, what should we use instead?
   - If we're using Copier wrong, how do we fix it?
   - What do production templates actually do?

4. **Migration path**
   - If switching tools, how do we preserve update mechanism?
   - If staying with Copier, how do we work around this bug?

### Long-term (Weeks)

5. **Best practices**
   - Document the "mature way" to handle mixed-syntax templates
   - Create reference implementation
   - Contribute back to community (bug fix, documentation, examples)

---

## Resources for Researchers

### Our Investigation Documents

- **inbox/copier-bracket-delimiter-investigation.md**: Full technical investigation (477 lines)
- **inbox/copier-delimiter-solution-analysis.md**: Expert's analysis and recommendations
- **inbox/v2.0.8-status.md**: Current status after 8 hours debugging
- **inbox/v2.0.8-final-recommendation.md**: Copier bug hypothesis and next steps

### Key Files to Examine

- **copier.yml**: Current delimiter configuration
- **template/NAMESPACES.md.jinja**: The blocker file (zero square brackets, still fails)
- **scripts/migrate-to-angle-brackets.sh**: Migration automation
- **scripts/rollback-migration.sh**: Rollback safety mechanism

### External References

- **Copier documentation**: https://copier.readthedocs.io/
- **Jinja2 delimiter configuration**: https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment
- **Copier GitHub**: https://github.com/copier-org/copier
- **Our template**: https://github.com/liminalcommons/chora-base

### Similar Projects to Study

1. **cookiecutter-django**: https://github.com/cookiecutter/cookiecutter-django
2. **Full Stack FastAPI Template**: https://github.com/tiangolo/full-stack-fastapi-template
3. **copier-poetry**: https://github.com/pawamoy/copier-poetry
4. **python-package-template**: https://github.com/TezRomacH/python-package-template

---

## Constraints and Context

### What We've Ruled Out

❌ **Curly brace delimiters** `{{ }}` - Conflicts with Python
❌ **Square bracket delimiters** `[[ ]]` - Conflicts with Markdown
❌ **Extensive raw block wrapping** - Unmaintainable (tried 500+ wraps, still failed)
❌ **Excluding NAMESPACES.md.jinja** - User requirement to keep it

### What We Haven't Tried Yet

⏸️ **Different Copier versions** - Maybe older version works better?
⏸️ **Forking Copier** - Fix the bug ourselves
⏸️ **Switching to Cookiecutter** - Loses update mechanism
⏸️ **Custom template engine** - Significant development effort
⏸️ **Hybrid approach** - Different engines for different files

### User Requirements

- ✅ **Must include NAMESPACES.md** in template
- ✅ **Must be LLM-friendly** (clear instructions for AI agents)
- ✅ **Must support updates** (not just one-time generation)
- ✅ **Must work for mcp-n8n team** (real adopter waiting to upgrade)

---

## Questions for Subject Matter Experts

### For Copier Maintainers

1. Is there a known bug with `_envops` delimiter configuration in v9.10.3?
2. Why would standalone Jinja2 work but Copier fail with same delimiters?
3. How does SandboxedEnvironment differ from Environment re: delimiter handling?
4. What's the recommended delimiter strategy for templates with Python source code?
5. Should we file a bug report? If yes, what additional info do you need?

### For Template System Experts

1. How do production Python project templates handle f-string conflicts?
2. What template systems are proven for mixed Python/Markdown content?
3. Are there template testing frameworks we should use?
4. What's the "mature way" to solve this problem?
5. Examples of large-scale templates (50+ files) that work reliably?

### For Jinja2 Experts

1. Can Jinja2's Environment configuration be overridden after initialization?
2. Are there Jinja2 extensions that help with delimiter conflicts?
3. How do you debug Jinja2 parsing errors when line numbers seem wrong?
4. Is there a way to validate templates without rendering them?
5. What's the relationship between trim_blocks/lstrip_blocks and delimiter parsing?

---

## How to Contribute Research Findings

### Format

Please provide:
1. **Finding**: What you discovered
2. **Evidence**: Links, code examples, test results
3. **Recommendation**: What we should do
4. **Tradeoffs**: Pros/cons of the approach
5. **Next steps**: Concrete actions to take

### Priority Areas

🔴 **Critical**: Evidence of Copier bug (or our misconfiguration)
🟡 **High**: Working examples of similar templates
🟢 **Medium**: Alternative template systems
🔵 **Low**: General best practices

### What Would Be Most Helpful

1. **Minimal reproduction case** showing the bug (or showing we're wrong)
2. **Link to working template** using angle brackets with Copier
3. **Copier issue/PR** addressing delimiter configuration bugs
4. **Production template** we can study as reference
5. **Migration guide** if we need to switch tools

---

## Timeline and Impact

### Current Impact

- **mcp-n8n team blocked**: Cannot upgrade from v1.9.3 (3 minor versions behind)
- **No new adopters**: Cannot recommend template until it works
- **Technical debt**: 8 failed releases, extensive debugging debt
- **Confidence erosion**: Each failed release reduces trust in template

### Urgency

- **Immediate**: Need to decide whether to file Copier bug or switch tools
- **Short-term**: Need working v2.0.8 within 1-2 weeks
- **Medium-term**: Need sustainable delimiter strategy for long-term maintenance

### Success Impact

- ✅ **Unblock mcp-n8n team** - Can upgrade to v2.0.8+
- ✅ **Reliable template** - No more mysterious TemplateSyntaxError
- ✅ **Community contribution** - Document solution for others
- ✅ **Sustainable maintenance** - Clear strategy going forward

---

## Conclusion

We've invested **28+ hours** debugging delimiter conflicts and **8 releases** trying different approaches. We have strong evidence of a Copier bug but need expert validation.

**We need mature, production-tested guidance** on:
1. Whether this is truly a Copier bug or our misconfiguration
2. What delimiter strategy actually works for mixed Python/Markdown templates
3. Whether to fix Copier, work around it, or switch tools entirely

**This research task is critical** for unblocking our current adopter and establishing a sustainable template maintenance strategy.

Thank you for any insights, examples, or guidance you can provide.

---

**Contact**: Available for clarification, testing, or providing additional context.
**Repository**: https://github.com/liminalcommons/chora-base
**Blocked PR**: v2.0.8 (angle bracket migration)
**Current Branch**: main (with angle bracket delimiters)
