# Cross-Platform Enforcement Strategy

**Date**: 2025-11-08
**Status**: Draft
**Purpose**: Ensure all new code follows Windows/Mac/Linux compatibility patterns

---

## Problem Statement

**Current State**: Patterns exist (SAP-030, good examples in code) but aren't consistently applied.

**Root Cause**: Developers and AI agents aren't encountering the patterns at the right moment:
- Patterns are documented but buried in SAP-030 docs
- No enforcement at commit time
- No CI/CD validation on Windows
- No discoverable examples at point-of-need

**Goal**: Make cross-platform patterns **impossible to miss** and **easy to follow**.

---

## Strategy: 5-Layer Defense

### Layer 1: Discoverability (SAP-009) - "Learn the Right Way"

**Principle**: Put cross-platform patterns where agents look first

#### 1.1 Enhanced AGENTS.md at Root

Update `/AGENTS.md` with cross-platform section:

```markdown
## Cross-Platform Development (CRITICAL)

chora-base supports Windows, Mac, and Linux. Follow these patterns:

### Python Scripts with Emojis

**ALWAYS add UTF-8 reconfiguration**:
```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

**Reference**: scripts/create-model-mcp-server.py:46-49

### File I/O Operations

**ALWAYS use encoding='utf-8'**:
```python
# Good
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Bad (breaks on Windows)
with open(file_path, 'r') as f:  # Missing encoding!
    content = f.read()
```

**Reference**: scripts/generate-sap.py:24

### Path Handling

**ALWAYS use pathlib**:
```python
from pathlib import Path

# Good
output_dir = Path(args.output)
file_path = output_dir / "subdir" / "file.txt"

# Bad (Unix-only)
file_path = f"{args.output}/subdir/file.txt"
```

**Reference**: scripts/create-model-mcp-server.py

### New Scripts Policy

**NO bash scripts allowed**:
- All automation must be Python 3.8+
- Bash scripts won't work on Windows without WSL
- See: scripts/BASH_SCRIPTS_README.md

**Validation**: Pre-commit hook blocks new .sh files
```

---

#### 1.2 scripts/AGENTS.md with Quick Reference

Create `scripts/AGENTS.md`:

```markdown
# Scripts - Agent Awareness

## Quick Reference: Cross-Platform Patterns

**Before writing ANY new script, read these patterns:**

### Template: New Python Script

```python
#!/usr/bin/env python3
"""Script description"""

import sys
from pathlib import Path

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Rest of imports
import argparse
import json

# Use pathlib for all file paths
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)  # Not str!
    args = parser.parse_args()

    # File I/O with explicit encoding
    with open(args.output / "file.txt", 'w', encoding='utf-8') as f:
        f.write("content")

if __name__ == '__main__':
    sys.exit(main())
```

### Examples to Copy

| Pattern | Reference File | Lines |
|---------|----------------|-------|
| UTF-8 console setup | scripts/create-model-mcp-server.py | 46-49 |
| File I/O with encoding | scripts/generate-sap.py | 24 |
| Pathlib usage | scripts/create-model-mcp-server.py | Throughout |
| Home directory detection | scripts/platform-info.py | 66 |

### Validation

Before committing:
```bash
# Check your script
python scripts/validate-windows-compat.py --file path/to/your-script.py
```
```

---

#### 1.3 Template Files in templates/cross-platform/

Create reference templates agents can copy:

**templates/cross-platform/python-script-template.py**:
```python
#!/usr/bin/env python3
"""[Description]

Usage:
    python scripts/[name].py --arg value
"""

import argparse
import json
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VERSION = "1.0.0"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="[Description]")
    parser.add_argument('--output', type=Path, help='Output directory')
    args = parser.parse_args()

    # File reading with explicit encoding
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # File writing with explicit encoding
    with open(args.output / 'result.txt', 'w', encoding='utf-8') as f:
        f.write("Result\\n")

    print("✅ Done")
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

---

### Layer 2: Pre-Commit Hook - "Catch Mistakes Early"

**Principle**: Block non-compliant code before it's committed

#### 2.1 Enhanced Pre-Commit Hook

Update `.githooks/pre-commit-windows-compat` to check:

1. ✅ **Bash scripts blocked** (already implemented)
2. ✅ **Critical issues blocked** (already implemented)
3. 🆕 **Missing encoding parameters** (add warning)
4. 🆕 **String path concatenation** (detect `f"{path}/subdir"`)
5. 🆕 **Home directory hardcoded** (detect `~/` in Python)

**Enhancement**:
```python
# Add to pre-commit hook
def check_path_patterns(staged_files):
    """Detect unsafe path patterns"""
    issues = []
    for file in [f for f in staged_files if f.endswith('.py')]:
        with open(file, encoding='utf-8') as f:
            content = f.read()

            # Check for string concatenation with /
            if re.search(r'f["\'].*\{.*\}/', content):
                issues.append(f"{file}: String path concatenation detected (use pathlib)")

            # Check for hardcoded ~/
            if '~/' in content and 'Path.home()' not in content:
                issues.append(f"{file}: Hardcoded ~/ detected (use Path.home())")

    return issues
```

---

#### 2.2 Install Instructions in CONTRIBUTING.md

Make hook installation mandatory:

```markdown
## Developer Setup

### 1. Install Pre-Commit Hook (REQUIRED)

```bash
git config core.hooksPath .githooks
```

This hook prevents Windows compatibility regressions by:
- Blocking new bash scripts
- Detecting missing UTF-8 encoding
- Validating path handling

**To bypass** (not recommended):
```bash
git commit --no-verify
```
```

---

### Layer 3: CI/CD Validation - "Test on Real Windows"

**Principle**: Automated testing on Windows, Mac, Linux

#### 3.1 GitHub Actions Multi-OS Matrix

Create `.github/workflows/cross-platform-test.yml`:

```yaml
name: Cross-Platform Compatibility

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.11']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Validate Windows compatibility
        run: python scripts/validate-windows-compat.py

      - name: Test core scripts (emoji output)
        run: |
          python scripts/create-model-mcp-server.py --help
          python scripts/install-sap.py --list
          python scripts/validate-sap-infrastructure.py --help

      - name: Test file I/O encoding
        run: python scripts/platform-info.py

      - name: Run fast-setup dry-run
        run: |
          python scripts/create-model-mcp-server.py \
            --name "Test MCP" \
            --namespace testmcp \
            --output ./test-output \
            --skip-validation \
            --skip-git
        shell: bash  # Use bash even on Windows (Git Bash)

      - name: Verify generated files have UTF-8 encoding
        if: matrix.os == 'windows-latest'
        run: |
          # Check that README.md was created with UTF-8
          python -c "
          from pathlib import Path
          readme = Path('test-output/README.md')
          if readme.exists():
              content = readme.read_text(encoding='utf-8')
              print(f'✅ README.md has {len(content)} chars')
          else:
              exit(1)
          "
```

---

#### 3.2 Status Badge in README

Add CI badge to show Windows compatibility:

```markdown
# chora-base

[![Cross-Platform](https://github.com/yourorg/chora-base/workflows/Cross-Platform%20Compatibility/badge.svg)](https://github.com/yourorg/chora-base/actions/workflows/cross-platform-test.yml)
[![Windows](https://img.shields.io/badge/Windows-Compatible-blue)](docs/project-docs/windows-compatibility-summary.md)
```

---

### Layer 4: Documentation - "Easy to Find, Hard to Miss"

**Principle**: Put patterns where developers look

#### 4.1 CONTRIBUTING.md Section

Add prominent section:

```markdown
## Cross-Platform Development (Windows/Mac/Linux)

chora-base MUST work on Windows, Mac, and Linux without modification.

### Quick Checklist

Before writing code, ensure:

- [ ] Using pathlib for file paths (not string concatenation)
- [ ] File I/O uses `encoding='utf-8'`
- [ ] Scripts with emojis have UTF-8 console reconfiguration
- [ ] No bash scripts (use Python)
- [ ] Tested on Windows (or rely on CI/CD)

### Resources

- **Patterns**: See [scripts/AGENTS.md](scripts/AGENTS.md)
- **Template**: See [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)
- **Validation**: Run `python scripts/validate-windows-compat.py`
- **Complete Guide**: [SAP-030: Cross-Platform Fundamentals](docs/skilled-awareness/cross-platform-fundamentals/)

### Common Mistakes

❌ **DON'T**:
```python
with open("file.txt") as f:  # Missing encoding!
path = f"{base_dir}/subdir/file.txt"  # Windows uses backslashes!
```

✅ **DO**:
```python
with open("file.txt", encoding='utf-8') as f:
path = Path(base_dir) / "subdir" / "file.txt"
```
```

---

#### 4.2 Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description
[Description of changes]

## Cross-Platform Checklist

- [ ] No new bash scripts added
- [ ] All file I/O uses `encoding='utf-8'`
- [ ] All paths use `pathlib.Path`
- [ ] Scripts with emojis have UTF-8 console reconfiguration
- [ ] Ran `python scripts/validate-windows-compat.py`
- [ ] Pre-commit hook passed (or explained bypass reason)

## Testing

- [ ] Tested on Windows (or CI passed)
- [ ] Tested on Mac (or CI passed)
- [ ] Tested on Linux (or CI passed)

## Related Issues

Closes #[issue number]
```

---

### Layer 5: AI Agent Context - "Proactive Guidance"

**Principle**: Agents should remind themselves about cross-platform patterns

#### 5.1 Enhanced CLAUDE.md

Add to root `CLAUDE.md`:

```markdown
## Cross-Platform Development Reminders

**CRITICAL**: Before writing ANY new Python script, check:

1. **Emoji output?** → Add UTF-8 reconfiguration
   ```python
   if sys.platform == 'win32':
       sys.stdout.reconfigure(encoding='utf-8')
       sys.stderr.reconfigure(encoding='utf-8')
   ```

2. **File I/O?** → Add `encoding='utf-8'`
   ```python
   with open(path, 'r', encoding='utf-8') as f:
   ```

3. **Path manipulation?** → Use pathlib
   ```python
   from pathlib import Path
   file_path = output_dir / "subdir" / "file.txt"
   ```

4. **New automation?** → Python only, NO bash

**Reference Template**: [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)

**Validation**: `python scripts/validate-windows-compat.py --file your-script.py`

**Why This Matters**: Windows has 1 billion+ users. Cross-platform support is non-negotiable.
```

---

#### 5.2 Session Startup Reminder

Add to root `AGENTS.md` at the top:

```markdown
# chora-base - Agent Awareness

⚠️ **CROSS-PLATFORM REMINDER**: All code MUST work on Windows/Mac/Linux.
See [Cross-Platform Patterns](docs/skilled-awareness/cross-platform-fundamentals/) before writing code.

## Quick Start
[Rest of AGENTS.md...]
```

---

## Implementation Roadmap

### Phase 3A: Enhanced Discoverability (Week 1)

**Goal**: Make patterns unmissable

- [ ] Update root AGENTS.md with cross-platform section
- [ ] Create scripts/AGENTS.md with quick reference
- [ ] Create templates/cross-platform/python-script-template.py
- [ ] Add session startup reminder to root AGENTS.md
- [ ] Update CLAUDE.md with development reminders

**Effort**: 4 hours
**Impact**: Agents encounter patterns at point-of-need

---

### Phase 3B: Enhanced Enforcement (Week 1)

**Goal**: Block non-compliant code

- [ ] Enhance pre-commit hook with path pattern detection
- [ ] Update CONTRIBUTING.md with mandatory hook installation
- [ ] Create .github/pull_request_template.md with checklist
- [ ] Add pre-commit hook test to validate-windows-compat.py

**Effort**: 4 hours
**Impact**: 90% of issues caught before commit

---

### Phase 3C: CI/CD Multi-OS Testing (Week 2)

**Goal**: Automated validation on real Windows

- [ ] Create .github/workflows/cross-platform-test.yml
- [ ] Test workflow on actual Windows runner
- [ ] Add status badge to README.md
- [ ] Configure fail-fast: false for debugging

**Effort**: 6 hours
**Impact**: 100% of issues caught before merge

---

### Phase 3D: Documentation Consolidation (Week 2)

**Goal**: Single source of truth

- [ ] Update CONTRIBUTING.md with cross-platform section
- [ ] Add "Common Mistakes" section with examples
- [ ] Create troubleshooting guide for Windows-specific errors
- [ ] Link all documentation to SAP-030

**Effort**: 2 hours
**Impact**: Clear guidance for all contributors

---

## Success Metrics

### Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pre-commit hook install rate | 100% | Git config check in CI |
| New scripts following template | 95%+ | Code review checklist |
| CI passing on Windows | 100% | GitHub Actions badge |
| Validation script usage | 80%+ | Track via A-MEM events |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| New cross-platform issues | 0/month | validation-windows-compat.py |
| Windows CI failures | <1/month | GitHub Actions history |
| Windows compatibility score | 95+/100 | Quarterly audit |

---

## Integration with Existing SAPs

### SAP-009 (agent-awareness) ✅

**How**: Nested awareness pattern
- Root AGENTS.md → Cross-platform reminder
- scripts/AGENTS.md → Quick reference
- SAP-030 AGENTS.md → Deep patterns

**Benefit**: Progressive disclosure - agents load patterns as needed

---

### SAP-030 (cross-platform-fundamentals) ✅

**How**: SAP-030 becomes authoritative reference
- All awareness files link to SAP-030
- SAP-030 protocol-spec has complete patterns
- Templates extract patterns from SAP-030

**Benefit**: Single source of truth, no duplication

---

### SAP-010 (A-MEM) - Optional Enhancement

**How**: Track cross-platform pattern usage

```python
# In create-model-mcp-server.py
log_event({
    "type": "cross_platform_pattern_used",
    "pattern": "utf8_console_reconfiguration",
    "script": "create-model-mcp-server.py"
})
```

**Benefit**: Measure adoption, identify gaps

---

### SAP-027 (dogfooding-patterns) ✅

**How**: Validate enforcement strategy
- Use validation script on chora-base itself
- Test pre-commit hook with intentional violations
- Run fast-setup on Windows in CI

**Benefit**: Prove patterns work in production

---

## Discoverability Integration Points

### Point 1: Session Start

**When**: Agent begins new session

**Where**: Root AGENTS.md (first file read)

**What**: Cross-platform reminder at top

**Why**: Sets expectations immediately

---

### Point 2: Creating New Script

**When**: Agent creates file in scripts/

**Where**: scripts/AGENTS.md + template file

**What**:
1. Read scripts/AGENTS.md for patterns
2. Copy templates/cross-platform/python-script-template.py
3. Modify template for use case

**Why**: Easier to copy correct pattern than write from scratch

---

### Point 3: Pre-Commit

**When**: Agent runs `git commit`

**Where**: .githooks/pre-commit-windows-compat

**What**: Validation + helpful error messages with fix guidance

**Why**: Last chance to catch issues before code review

---

### Point 4: Pull Request

**When**: Agent creates PR

**Where**: .github/pull_request_template.md

**What**: Cross-platform checklist (must check boxes)

**Why**: Explicit confirmation of compliance

---

### Point 5: CI Failure

**When**: Windows CI fails

**Where**: GitHub Actions log

**What**: Link to troubleshooting guide + validation tool

**Why**: Fast resolution path

---

## Example: Agent Journey with Discoverability

### Scenario: Claude Creates New Script

**Step 1: Session Start**
- Claude reads `/AGENTS.md`
- Sees: "⚠️ CROSS-PLATFORM REMINDER" at top
- Mental note: "Cross-platform matters here"

**Step 2: User Request**
> User: "Create a script to export metrics to CSV"

**Step 3: Claude Checks scripts/AGENTS.md**
- Reads: "Before writing ANY new script, read these patterns"
- Finds template reference
- Decision: "I should use the template"

**Step 4: Claude Copies Template**
```bash
cp templates/cross-platform/python-script-template.py scripts/export-metrics.py
```

**Step 5: Claude Modifies Template**
- Keeps UTF-8 reconfiguration ✅
- Keeps `encoding='utf-8'` in file I/O ✅
- Uses pathlib for output path ✅

**Step 6: Claude Validates**
```bash
python scripts/validate-windows-compat.py --file scripts/export-metrics.py
```
- Output: "✅ No issues found"

**Step 7: Claude Commits**
```bash
git add scripts/export-metrics.py
git commit -m "feat: Add metrics export to CSV"
```
- Pre-commit hook runs
- Output: "✅ All Windows compatibility checks passed"

**Step 8: CI Validates**
- GitHub Actions runs on Windows/Mac/Linux
- All platforms pass ✅

**Result**: **Zero cross-platform issues introduced**

---

## Comparison: With vs Without Discoverability

### Without Discoverability (Current State)

```
User Request → Claude writes script → Uses defaults
                                    → Missing encoding='utf-8'
                                    → Missing UTF-8 reconfiguration
                                    → Uses string concatenation for paths
                                    → Commits
                                    → Merges to main
                                    → Windows users report crashes
                                    → 2-day fix cycle
```

**Time to Fix**: 2 days
**User Impact**: Windows users blocked

---

### With Discoverability (Proposed)

```
User Request → Claude reads AGENTS.md → Sees cross-platform reminder
            → Checks scripts/AGENTS.md → Finds template
            → Copies template → Inherits all patterns
            → Validates → Pre-commit hook catches issues
            → Fixes → Commits
            → CI validates on Windows → Passes
            → Merges to main → No user impact
```

**Time to Fix**: 0 (prevented)
**User Impact**: None

---

## Cost-Benefit Analysis

### Implementation Cost

| Phase | Effort | Calendar Time |
|-------|--------|---------------|
| 3A: Discoverability | 4 hours | 1 day |
| 3B: Enforcement | 4 hours | 1 day |
| 3C: CI/CD | 6 hours | 2 days |
| 3D: Documentation | 2 hours | 1 day |
| **Total** | **16 hours** | **1 week** |

---

### Benefit

| Benefit | Value |
|---------|-------|
| Issues prevented | 90%+ of cross-platform bugs |
| Time saved per prevented issue | 2 days/issue |
| Developer friction reduced | No "works on my machine" |
| User trust increased | Reliable cross-platform support |
| Maintenance burden reduced | Self-documenting patterns |

**ROI**: Prevents 1 issue → Saves 2 days → Pays for entire implementation

**Break-even**: After preventing **4 issues** (expected: first month)

---

## Recommended Next Actions

### Immediate (Today)

1. ✅ **Enable pre-commit hook**
   ```bash
   git config core.hooksPath .githooks
   ```

2. ✅ **Create scripts/AGENTS.md**
   - Quick reference for script development
   - Link to template

3. ✅ **Create template file**
   - templates/cross-platform/python-script-template.py
   - Reference implementation of all patterns

---

### Short Term (This Week)

4. ✅ **Update root AGENTS.md**
   - Add cross-platform reminder at top
   - Link to SAP-030 and scripts/AGENTS.md

5. ✅ **Update CONTRIBUTING.md**
   - Add cross-platform section
   - Make pre-commit hook mandatory

6. ✅ **Create PR template**
   - Cross-platform checklist
   - Testing requirements

---

### Medium Term (Next 2 Weeks)

7. ⏳ **Create GitHub Actions workflow**
   - Multi-OS matrix (Windows/Mac/Linux)
   - Run validation script
   - Test core scripts

8. ⏳ **Add status badge**
   - Show Windows compatibility in README
   - Link to test results

9. ⏳ **Document troubleshooting**
   - Windows-specific errors
   - Quick fixes guide

---

## Conclusion

**The Key Insight**: Patterns are useless if agents can't discover them.

**The Solution**: Multi-layer enforcement leveraging SAP-009 (agent-awareness):

1. **Discoverability**: Patterns at point-of-need (AGENTS.md hierarchy)
2. **Enforcement**: Pre-commit hook blocks violations
3. **Validation**: CI tests on real Windows
4. **Documentation**: Easy to find, hard to miss
5. **AI Context**: Proactive reminders in agent files

**Expected Outcome**:
- 0 new cross-platform issues (target: 95%+ prevention)
- 95+/100 Windows compatibility score (current: 85/100)
- Developer friction eliminated
- Windows users get same experience as Mac/Linux users

**Investment**: 16 hours (1 week)
**Payoff**: Permanent prevention of cross-platform issues

---

**Next Step**: Implement Phase 3A (Enhanced Discoverability) - 4 hours

Ready to proceed?

---

**Version**: 1.0.0
**Last Updated**: 2025-11-08
**Status**: Proposed
**Decision Needed**: Approve implementation plan
