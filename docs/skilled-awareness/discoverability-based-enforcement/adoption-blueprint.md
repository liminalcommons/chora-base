# Adoption Blueprint: Discoverability-Based Enforcement

**SAP ID**: SAP-031
**Version**: 1.0.0
**Last Updated**: 2025-11-08

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-031 Discoverability-Based Enforcement across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Discoverability only (Layer 1) | 2-4 hours | Quarterly review | Small teams, quick proof-of-concept, low-risk domains |
| **Level 2: Advanced** | + Pre-Commit + CI/CD (Layers 1-3) | 1-2 days | Monthly review | Medium teams, production projects, critical domains |
| **Level 3: Mastery** | All 5 layers + metrics | 1 week | Biweekly metrics, quarterly review | **Recommended for production** - Large teams, high-risk domains (security, cross-platform) |

**Recommended Path**: Level 1 (Week 1) → Level 2 (Week 2-3) → Level 3 (Week 4+)

---

## Level 1: Basic Adoption (Discoverability Only)

### Purpose

Level 1 adoption is suitable for:
- Getting started with enforcement framework
- Understanding core discoverability concepts
- Quick proof-of-concept (2-4 hours)
- Low-risk quality domains (formatting, style, documentation)
- Teams without CI/CD infrastructure

### Time Estimate

- **Setup**: 2-4 hours
- **Learning Curve**: Low (agents already familiar with SAP-009 patterns)

### Prerequisites

**Required**:
- SAP-009 (agent-awareness) adopted - root AGENTS.md + domain AGENTS.md structure
- Git repository (for version control)
- Quality domain identified (e.g., cross-platform, security, accessibility)

**Recommended**:
- Existing documentation for quality domain patterns
- Example violations to guide pattern selection

### Step-by-Step Instructions

#### Step 1.1: Identify Quality Domain and Core Patterns

**Action**:
```bash
# 1. Choose quality domain (e.g., cross-platform, security, accessibility)
# 2. Identify 3-5 core patterns to enforce
# 3. Document pattern rationale (why important)

# Example: Cross-platform domain
DOMAIN="cross-platform"
PATTERNS=(
    "UTF-8 console reconfiguration (Windows emoji support)"
    "File I/O encoding='utf-8' (prevent cp1252 corruption)"
    "Pathlib usage (cross-platform path handling)"
)
```

**Expected Output**:
- Quality domain selected
- 3-5 core patterns identified
- Business rationale documented

**Verification**:
- [ ] Can explain why each pattern matters in 1-2 sentences
- [ ] Patterns are specific and automatable (>70%)

---

#### Step 1.2: Update Root AGENTS.md with Enforcement Reminder

**Action**:
```bash
# Edit root AGENTS.md to add enforcement reminder at top
# Location: AGENTS.md (project root)
```

Add this section at the top of `AGENTS.md` (after title/intro):

```markdown
## 🔴 [QUALITY DOMAIN] REMINDER

**ALL code MUST [quality requirement without modification].**

Before [activity that requires patterns], read: **[path/to/domain/AGENTS.md]** for [quality domain] patterns.

**Quick Template**: Copy [templates/[domain]/template-file.[ext]](templates/[domain]/template-file.[ext])

---
```

**Example (Cross-Platform)**:
```markdown
## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST work on Windows, Mac, and Linux without modification.**

Before writing Python scripts, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)

---
```

**Expected Output**:
- Reminder added to root AGENTS.md
- Uses emoji (🔴) for visual attention
- Links to domain AGENTS.md (1-click navigation)
- Links to template file (production-ready starting point)

**Verification**:
```bash
# Check reminder exists
grep "REMINDER" AGENTS.md

# Expected: Lines with "🔴 [QUALITY DOMAIN] REMINDER"
```

---

#### Step 1.3: Create or Update Domain AGENTS.md with Patterns

**Action**:
```bash
# Create domain AGENTS.md if it doesn't exist
# Or update existing domain AGENTS.md with quality domain patterns section

# Example location: scripts/AGENTS.md, docs/[domain]/AGENTS.md, src/[domain]/AGENTS.md
DOMAIN_AGENTS_PATH="scripts/AGENTS.md"  # Adjust for your domain

# If file doesn't exist, create it
if [ ! -f "$DOMAIN_AGENTS_PATH" ]; then
    mkdir -p "$(dirname "$DOMAIN_AGENTS_PATH")"
    touch "$DOMAIN_AGENTS_PATH"
fi
```

Add this section to domain AGENTS.md:

```markdown
## [Quality Domain] Patterns

**Quick Template**: [templates/[domain]/template.[ext]](templates/[domain]/template.[ext])

### Pattern 1: [Name]

**Description**: [What this pattern enforces and why it matters]

**Example**:
```[language]
# Correct pattern
[code example showing correct implementation]
```

**Anti-Pattern**:
```[language]
# Incorrect - will cause [specific problem]
[code example showing what NOT to do]
```

---

### Pattern 2: [Name]

**Description**: [What this pattern enforces]

**Example**:
```[language]
[code example]
```

---

### Pattern 3: [Name]

[Repeat for all core patterns]

---

## Validation

**Check your code**:
```bash
# Manual validation command (if available)
python scripts/validate-[domain].py
```

**Template**: Use [templates/[domain]/template.[ext]](templates/[domain]/template.[ext]) as starting point
```

**Example (Cross-Platform)**:
```markdown
## Cross-Platform Patterns

**Quick Template**: [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)

### Pattern 1: UTF-8 Console Output

**Description**: Windows console defaults to cp1252 encoding, causing `UnicodeEncodeError` on emoji/Unicode output. Reconfigure to UTF-8 at script start.

**Example**:
```python
import sys

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

print("✅ Success!")  # Now works on Windows
```

**Anti-Pattern**:
```python
# Missing UTF-8 reconfiguration
print("✅ Success!")  # Crashes on Windows with UnicodeEncodeError
```

---

### Pattern 2: File I/O Encoding

**Description**: Always specify `encoding='utf-8'` for text file operations (Windows defaults to cp1252, causing silent corruption).

**Example**:
```python
from pathlib import Path

# Always specify encoding
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

---

### Pattern 3: Path Handling with Pathlib

**Description**: Use `pathlib.Path` for cross-platform path handling (not string concatenation).

**Example**:
```python
from pathlib import Path

# Cross-platform path building
config_path = Path.home() / ".config" / "app" / "config.json"
```
```

**Expected Output**:
- Domain AGENTS.md created/updated
- 3-5 patterns documented with examples
- Anti-patterns shown (what NOT to do)
- Template link at top for quick access
- Max 200 lines (quick reference, not comprehensive guide)

**Verification**:
```bash
# Check domain AGENTS.md exists
test -f scripts/AGENTS.md && echo "✅ Domain AGENTS.md exists"

# Check patterns section exists
grep "## Cross-Platform Patterns" scripts/AGENTS.md && echo "✅ Patterns section found"
```

---

#### Step 1.4: Create Template File with Patterns Pre-Implemented

**Action**:
```bash
# Create template directory
mkdir -p templates/[domain]

# Create template file with patterns pre-implemented
# This is easier to copy than write from scratch
```

Template file structure (Python example):

```python
#!/usr/bin/env python3
"""[SCRIPT_NAME] - [Brief description]

This script demonstrates [quality domain] best practices:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

Usage:
    python [script_name].py [args]
"""

# [QUALITY DOMAIN] Pattern 1: [Description]
# Example: UTF-8 console reconfiguration
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# [QUALITY DOMAIN] Pattern 2: [Description]
# Example: File I/O with encoding
from pathlib import Path

def load_config(config_path: Path) -> dict:
    """Load configuration with UTF-8 encoding"""
    import json
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_path: Path, config: dict) -> None:
    """Save configuration with UTF-8 encoding"""
    import json
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

# [QUALITY DOMAIN] Pattern 3: [Description]
# Example: Path handling with pathlib
def main():
    """Main entry point"""
    # Cross-platform home directory
    config_dir = Path.home() / ".config" / "app"
    config_path = config_dir / "config.json"

    # Ensure directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load or create config
    if config_path.exists():
        config = load_config(config_path)
    else:
        config = {"version": "1.0.0"}
        save_config(config_path, config)

    print(f"✅ Config loaded from {config_path}")

if __name__ == '__main__':
    main()
```

**Expected Output**:
- Template file created in `templates/[domain]/[template-name].[ext]`
- All core patterns pre-implemented (production-ready)
- Comments explain each pattern
- Copy-paste friendly (minimal customization needed)

**Verification**:
```bash
# Check template exists
test -f templates/cross-platform/python-script-template.py && echo "✅ Template file exists"

# Check template has patterns
grep "sys.stdout.reconfigure" templates/cross-platform/python-script-template.py && echo "✅ Pattern 1 found"
grep "encoding='utf-8'" templates/cross-platform/python-script-template.py && echo "✅ Pattern 2 found"
grep "pathlib" templates/cross-platform/python-script-template.py && echo "✅ Pattern 3 found"
```

---

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] Quality domain identified with 3-5 core patterns
- [ ] Root AGENTS.md has enforcement reminder (🔴 emoji, links to domain AGENTS.md + template)
- [ ] Domain AGENTS.md has patterns section (max 200 lines)
- [ ] Template file created with patterns pre-implemented
- [ ] Agent can navigate from root AGENTS.md → domain AGENTS.md → template in <30 seconds
- [ ] Template is production-ready (can copy + customize immediately)

#### Validation Commands

```bash
# Validate all Level 1 components exist
echo "=== Level 1 Validation ==="

# Check 1: Root AGENTS.md reminder
test -f AGENTS.md && grep "REMINDER" AGENTS.md && echo "✅ Root AGENTS.md reminder exists"

# Check 2: Domain AGENTS.md patterns
test -f scripts/AGENTS.md && grep "Patterns" scripts/AGENTS.md && echo "✅ Domain AGENTS.md patterns exist"

# Check 3: Template file
test -f templates/cross-platform/python-script-template.py && echo "✅ Template file exists"

# Check 4: Pattern discovery time (manual test)
echo "📊 Manual test: Time yourself navigating from root AGENTS.md → template"
echo "   Target: <30 seconds"
```

#### Success Criteria

**Level 1 Complete** when:
- ✅ All validation checks pass
- ✅ Agent can discover patterns in <30 seconds from session start
- ✅ Template file has all core patterns pre-implemented
- ✅ Documentation burden reduced (agents reference AGENTS.md, not scattered docs)

---

### Common Issues (Level 1)

**Issue 1**: Agent can't find domain AGENTS.md from root AGENTS.md

- **Cause**: Link path incorrect or missing
- **Solution**: Verify link in root AGENTS.md points to correct domain AGENTS.md path (relative path from project root)

**Issue 2**: Template file has placeholder code (not production-ready)

- **Cause**: Copied generic template without implementing patterns
- **Solution**: Template should have all patterns pre-implemented (not TODOs), easier to copy than write from scratch

**Issue 3**: Domain AGENTS.md too long (>200 lines)

- **Cause**: Included comprehensive guide instead of quick reference
- **Solution**: Keep domain AGENTS.md concise (3-5 patterns, examples only), move comprehensive docs to separate file

---

## Level 2: Advanced Adoption (+ Pre-Commit + CI/CD)

### Purpose

Level 2 adoption adds:
- **Layer 2 (Pre-Commit)**: Automated validation before commit (catch issues early)
- **Layer 3 (CI/CD)**: Automated testing on real platforms/environments (second line of defense)
- **Self-Service Fix Tools**: One-command remediation (reduce friction)
- **Prevention Rate**: Target 70%+ (vs 20% documentation-only)

### Time Estimate

- **Setup**: 1-2 days (incremental from Level 1)
- **Total from Start**: 1.5-2.5 days

### Prerequisites

**Required**:
- ✅ Level 1 adoption complete (discoverability layer)
- Git repository with commit workflow
- Python 3.8+ (for validation scripts)

**Recommended**:
- CI/CD platform (GitHub Actions, GitLab CI, etc.)
- Pre-commit framework installed (`pip install pre-commit`)

---

### Step-by-Step Instructions

#### Step 2.1: Create Validation Script

**Action**:
```bash
# Create validation script in scripts/validate-[domain].py
```

Example validation script:

```python
#!/usr/bin/env python3
"""Validate [Quality Domain] compliance

This script checks for common [quality domain] violations:
- [Pattern 1 violation]
- [Pattern 2 violation]
- [Pattern 3 violation]

Usage:
    python scripts/validate-[domain].py
    python scripts/validate-[domain].py --file path/to/file.py
"""

import sys
from pathlib import Path
import re
import argparse

# Configure UTF-8 output (cross-platform)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def validate_pattern_1(file_path: Path) -> list[str]:
    """Validate Pattern 1 compliance

    Returns:
        List of error messages (empty if compliant)
    """
    errors = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Example: Check for emoji without UTF-8 reconfiguration
    has_emoji = bool(re.search(r'[^\x00-\x7F]', content))
    has_reconfigure = 'sys.stdout.reconfigure(encoding=' in content

    if has_emoji and not has_reconfigure:
        errors.append(f"{file_path}: Uses emojis but missing UTF-8 reconfiguration")

    return errors

def validate_pattern_2(file_path: Path) -> list[str]:
    """Validate Pattern 2 compliance"""
    errors = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Example: Check for open() without encoding parameter
    open_calls = re.findall(r'open\([^)]+\)', content)
    for call in open_calls:
        if 'encoding=' not in call:
            errors.append(f"{file_path}: open() call missing encoding parameter: {call}")

    return errors

def validate_file(file_path: Path) -> list[str]:
    """Validate single file

    Returns:
        List of all errors for this file
    """
    errors = []
    errors.extend(validate_pattern_1(file_path))
    errors.extend(validate_pattern_2(file_path))
    # Add more pattern validations...
    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate [Quality Domain] compliance")
    parser.add_argument('--file', type=Path, help='Validate specific file')
    parser.add_argument('--scripts-only', action='store_true', help='Validate scripts/ directory only')
    args = parser.parse_args()

    # Determine which files to validate
    if args.file:
        files = [args.file]
    elif args.scripts_only:
        files = list(Path('scripts').glob('**/*.py'))
    else:
        files = list(Path('.').glob('**/*.py'))

    # Validate all files
    all_errors = []
    for file_path in files:
        if file_path.is_file():
            errors = validate_file(file_path)
            all_errors.extend(errors)

    # Report results
    if all_errors:
        print(f"❌ Found {len(all_errors)} [quality domain] issues:\n")
        for error in all_errors:
            print(f"  {error}")
        print(f"\n💡 Tip: Run 'python scripts/fix-[domain]-issues.py --apply' for automated fixes")
        return 1
    else:
        print(f"✅ All files comply with [quality domain] standards")
        return 0

if __name__ == '__main__':
    sys.exit(main())
```

**Expected Output**:
- Validation script created in `scripts/validate-[domain].py`
- Script validates all core patterns
- Script provides clear error messages
- Script suggests fix tool (if available)

**Verification**:
```bash
# Test validation script
python scripts/validate-cross-platform.py --scripts-only

# Expected: Report of violations (or "✅ All files comply")
```

---

#### Step 2.2: Create Pre-Commit Hook

**Action**:
```bash
# Create .githooks directory if it doesn't exist
mkdir -p .githooks

# Create pre-commit hook
# File: .githooks/pre-commit-[quality-domain]
```

Pre-commit hook template:

```python
#!/usr/bin/env python3
"""Pre-commit hook: Validate [Quality Domain]

This hook validates that all files follow [quality domain] best practices:
1. [Pattern 1]
2. [Pattern 2]
3. [Pattern 3]

Installation:
    git config core.hooksPath .githooks

Usage:
    This hook runs automatically on git commit.
    To bypass (not recommended): git commit --no-verify
"""

import subprocess
import sys
from pathlib import Path

# Configure UTF-8 output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def get_staged_files():
    """Get list of staged Python files"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f.endswith('.py')]
        return files
    except subprocess.CalledProcessError:
        return []

def main():
    """Main pre-commit hook logic"""
    print("🔍 Running [Quality Domain] validation...")

    staged_files = get_staged_files()

    if not staged_files:
        print("✅ No Python files to check")
        return 0

    # Run validation script on staged files
    for file_path in staged_files:
        result = subprocess.run(
            ['python', 'scripts/validate-[domain].py', '--file', file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("❌ ERROR: [Quality Domain] issues found in staged files!\n")
            print(result.stdout)
            print("\nRequired action:")
            print("  1. Run: python scripts/fix-[domain]-issues.py --apply")
            print("  2. Review changes and re-stage files (git add)")
            print("  3. Try commit again\n")
            print("To bypass this check (not recommended):")
            print("  git commit --no-verify\n")
            return 1

    print("✅ All [Quality Domain] checks passed")
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

**Expected Output**:
- Pre-commit hook created in `.githooks/pre-commit-[quality-domain]`
- Hook validates staged files only (fast)
- Hook provides educational error messages
- Hook suggests fix tool

**Verification**:
```bash
# Make hook executable
chmod +x .githooks/pre-commit-cross-platform

# Configure git to use .githooks/
git config core.hooksPath .githooks

# Test hook
git add scripts/some-file.py
git commit -m "test" --dry-run

# Expected: Hook runs and validates (or blocks if violations)
```

---

#### Step 2.3: Create Self-Service Fix Tool (Optional but Recommended)

**Action**:
```bash
# Create fix tool in scripts/fix-[domain]-issues.py
```

Fix tool template (see [protocol-spec.md](protocol-spec.md#contract-6-self-service-fix-tool) for complete example).

**Expected Output**:
- Fix tool provides one-command remediation
- Dry-run mode by default (safe exploration)
- --apply flag for execution

---

#### Step 2.4: Create CI/CD Validation Workflow

**Action**:
```bash
# Create CI/CD workflow
# File: .github/workflows/[quality-domain]-validation.yml
```

CI/CD workflow template:

```yaml
name: [Quality Domain] Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  validate:
    name: Validate on ${{ matrix.platform }}
    runs-on: ${{ matrix.platform }}

    strategy:
      fail-fast: false
      matrix:
        platform: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python info
        run: |
          python --version
          python -c "import sys; print(f'Platform: {sys.platform}')"

      - name: Run [Quality Domain] validation
        run: python scripts/validate-[domain].py

      - name: Upload validation report (if failure)
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report-${{ matrix.platform }}-py${{ matrix.python-version }}
          path: validation-report.txt
          retention-days: 30
```

**Expected Output**:
- CI/CD workflow created
- Matrix testing on all target platforms
- Validation reports uploaded on failure
- Runs on push + PR

**Verification**:
```bash
# Trigger workflow manually
gh workflow run [quality-domain]-validation.yml

# Check workflow status
gh run list --workflow=[quality-domain]-validation.yml
```

---

### Configuration

#### Level 2 Configuration File (Optional)

```yaml
# .chora/enforcement.yaml
enforcement:
  enabled: true

  domains:
    [quality-domain]:
      enabled: true
      severity: critical  # block | warn | info

      # Layer 2: Pre-Commit
      pre_commit:
        enabled: true
        performance_target_seconds: 10

      # Layer 3: CI/CD
      ci_cd:
        enabled: true
        platforms: [ubuntu-latest, macos-latest, windows-latest]

      patterns:
        - [pattern-1]
        - [pattern-2]
        - [pattern-3]
```

---

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] All Level 1 checks still pass
- [ ] Validation script created (`scripts/validate-[domain].py`)
- [ ] Pre-commit hook created and installed (`.githooks/pre-commit-[domain]`)
- [ ] Self-service fix tool created (optional: `scripts/fix-[domain]-issues.py`)
- [ ] CI/CD workflow created (`.github/workflows/[quality-domain]-validation.yml`)
- [ ] Pre-commit hook blocks commits with violations
- [ ] CI/CD workflow runs on push/PR
- [ ] Prevention rate measured (target: 70%+)

#### Validation Commands

```bash
# Validate all Level 2 components exist
echo "=== Level 2 Validation ==="

# Check 1: Validation script
test -f scripts/validate-cross-platform.py && echo "✅ Validation script exists"

# Check 2: Pre-commit hook
test -f .githooks/pre-commit-cross-platform && echo "✅ Pre-commit hook exists"
git config --get core.hooksPath | grep ".githooks" && echo "✅ Git configured to use .githooks"

# Check 3: CI/CD workflow
test -f .github/workflows/cross-platform-validation.yml && echo "✅ CI/CD workflow exists"

# Check 4: Pre-commit hook works
git commit --dry-run && echo "✅ Pre-commit hook runs"

# Check 5: Prevention rate (manual measurement - see [AGENTS.md](AGENTS.md#workflow-3-measuring-and-improving-prevention-rate))
```

---

### Common Issues (Level 2)

**Issue 1**: Pre-commit hook timeout (>10 seconds)

- **Cause**: Validating entire repository instead of staged files only
- **Solution**: Update hook to use `git diff --cached --name-only` (staged files only)

**Issue 2**: CI/CD validation passing locally but failing in CI

- **Cause**: Platform-specific behavior (e.g., Windows vs Linux)
- **Solution**: Download validation report artifact, reproduce locally on target platform

**Issue 3**: Developers frequently using --no-verify

- **Cause**: Too many false positives or blocking legitimate work
- **Solution**: Start in warn-only mode (don't block), refine rules, then promote to blocking

---

## Level 3: Mastery - **RECOMMENDED**

### Purpose

Level 3 adoption provides:
- **Layer 4 (Documentation)**: CONTRIBUTING.md guidelines + PR templates
- **Layer 5 (Review)**: Human verification checklist
- **Prevention Rate Metrics**: Track effectiveness over time (target: 90%+)
- **Production-Ready**: Complete enforcement stack with all safety nets
- **Continuous Improvement**: Quarterly reviews and refinement

### Time Estimate

- **Setup**: 1 week (incremental from Level 2)
- **Total from Start**: 2-3 weeks
- **Maintenance**: Biweekly metrics review, quarterly refinement

### Prerequisites

**Required**:
- ✅ Level 2 adoption complete (Layers 1-3)
- CONTRIBUTING.md file exists
- PR template exists (.github/pull_request_template.md)

**Recommended**:
- Metrics tracking system (spreadsheet, dashboard, etc.)
- Team buy-in for quarterly reviews

---

### Step-by-Step Instructions

#### Step 3.1: Update CONTRIBUTING.md with Quality Domain Guidelines

**Action**:
```markdown
# Add to CONTRIBUTING.md

## [Quality Domain] Requirements (REQUIRED)

**ALL code MUST [quality requirement].**

### Quick Checklist

Before writing [code type], ensure:

- [ ] Pattern 1: [Description]
- [ ] Pattern 2: [Description]
- [ ] Pattern 3: [Description]
- [ ] Read: [domain AGENTS.md path] for complete patterns
- [ ] Copy: [template file path] for production-ready starting point

### Validation

```bash
# Validate your changes
python scripts/validate-[domain].py

# Auto-fix common issues (if available)
python scripts/fix-[domain]-issues.py --apply

# Install pre-commit hook (REQUIRED)
git config core.hooksPath .githooks
```

### Resources

- **Quick Reference**: [domain AGENTS.md path]
- **Template**: [template file path]
- **Validation**: `scripts/validate-[domain].py`
- **Fix Tool**: `scripts/fix-[domain]-issues.py --apply`
```

---

#### Step 3.2: Update PR Template with Quality Domain Checklist

**Action**:
```markdown
# Add to .github/pull_request_template.md

## [Quality Domain] Checklist (REQUIRED)

- [ ] All [quality domain] patterns followed (see [domain AGENTS.md path])
- [ ] Pre-commit hook passed (or explained bypass reason below)
- [ ] CI/CD validation passing on all platforms
- [ ] Template used (if applicable): [template file path]
- [ ] Tested on at least one platform (specify below)

### Testing Platform

- [ ] Windows (version: _________)
- [ ] macOS (version: _________)
- [ ] Linux (distro: _________)
- [ ] CI/CD (GitHub Actions)

### Validation Output

```bash
$ python scripts/validate-[domain].py
# Paste output here
```
```

---

#### Step 3.3: Establish Prevention Rate Measurement Process

**Action**:
```bash
# Create metrics tracking spreadsheet or file

# Establish baseline (Week 0)
python scripts/validate-[domain].py > week-0-baseline.txt
BASELINE_VIOLATIONS=$(grep "ERROR" week-0-baseline.txt | wc -l)
echo "Baseline violations: $BASELINE_VIOLATIONS"

# Measure biweekly (Week 2, 4, 6, ...)
# Track: violations_current / violations_baseline
# Target: ≤10% (i.e., 90%+ prevention rate)
```

**Metrics Template**:

| Week | Violations | Prevention Rate | Notes |
|------|-----------|----------------|-------|
| 0 (Baseline) | 142 | 0% | Before enforcement |
| 2 | 20 | 86% | Layer 1+2 implemented |
| 4 | 5 | 96% | Layer 3 (CI/CD) added |
| 6 | 1 | 99% | Layer 4+5 complete |

---

#### Step 3.4: Schedule Quarterly Reviews

**Action**:
```markdown
# Add to project calendar or CONTRIBUTING.md

## [Quality Domain] Enforcement Reviews

**Frequency**: Quarterly (every 3 months)

**Review Checklist**:
- [ ] Review prevention rate trend (target: ≥90%)
- [ ] Collect false-positive reports (refine rules)
- [ ] Update patterns in domain AGENTS.md (if new patterns emerge)
- [ ] Update template file (if patterns change)
- [ ] Review bypass usage (git log --grep="--no-verify")
- [ ] Update CONTRIBUTING.md (if guidelines change)

**Next Review Date**: [YYYY-MM-DD]
```

---

### Configuration

#### Level 3 Configuration (Complete)

```yaml
# .chora/enforcement.yaml
enforcement:
  enabled: true

  # Layer 1: Discoverability
  discoverability:
    root_agents_reminder: true
    domain_agents_patterns: true
    templates_enabled: true

  # Layer 2: Pre-Commit
  pre_commit:
    enabled: true
    performance_target_seconds: 10
    educational_messages: true
    self_service_fixes: true

  # Layer 3: CI/CD
  ci_cd:
    enabled: true
    platforms: [ubuntu-latest, macos-latest, windows-latest]
    artifact_upload: true
    badge_enabled: true

  # Layer 4: Documentation
  documentation:
    contributing_md: true
    pr_template: true
    testing_procedures: true

  # Layer 5: Review
  review:
    human_verification: true
    domain_expertise: false  # optional

  # Quality Domain Configuration
  domains:
    [quality-domain]:
      enabled: true
      severity: critical

      patterns:
        - [pattern-1]
        - [pattern-2]
        - [pattern-3]

      metrics:
        prevention_rate_target: 0.90  # 90%
        review_frequency_days: 90  # Quarterly
```

---

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] All Level 1-2 checks still pass
- [ ] CONTRIBUTING.md updated with quality domain guidelines
- [ ] PR template updated with quality domain checklist
- [ ] Prevention rate measurement process established
- [ ] Quarterly review scheduled (calendar + reminder)
- [ ] Prevention rate ≥90% (or on track after initial refinement)
- [ ] All 5 layers operational (discoverability, pre-commit, CI/CD, documentation, review)

#### Validation Commands

```bash
# Validate all Level 3 components exist
echo "=== Level 3 Validation ==="

# Check 1: CONTRIBUTING.md guidelines
grep "[Quality Domain] Requirements" CONTRIBUTING.md && echo "✅ CONTRIBUTING.md updated"

# Check 2: PR template checklist
grep "[Quality Domain] Checklist" .github/pull_request_template.md && echo "✅ PR template updated"

# Check 3: Metrics tracking
test -f week-0-baseline.txt && echo "✅ Baseline metrics captured"

# Check 4: Prevention rate (manual)
echo "📊 Check prevention rate: violations_current / violations_baseline ≤ 10%"
```

#### Success Criteria

**Level 3 Complete** when:
- ✅ All validation checks pass
- ✅ Prevention rate ≥90% (or on track after 2 weeks)
- ✅ All 5 layers operational (tested end-to-end)
- ✅ Quarterly review scheduled
- ✅ Team aware of enforcement framework (no surprises)

---

### Common Issues (Level 3)

**Issue 1**: Prevention rate <90% despite all layers

- **Cause**: Patterns incomplete, bypass usage, or validation gaps
- **Solution**: See [AGENTS.md Workflow 3](AGENTS.md#workflow-3-measuring-and-improving-prevention-rate) for gap analysis

**Issue 2**: Quarterly reviews not happening

- **Cause**: No calendar reminder or accountability
- **Solution**: Add to project board, assign owner, send meeting invite

**Issue 3**: Team resistance to enforcement

- **Cause**: Too strict too fast, poor error messages, no escape hatch
- **Solution**: Progressive enforcement (warn first), educational messages, document --no-verify usage

---

## Maintenance

### Ongoing Maintenance (All Levels)

**Quarterly** (Level 1-3):
- Review prevention rate trend
- Refine validation rules (false positives)
- Update domain AGENTS.md patterns (if new patterns emerge)
- Update template file (align with patterns)

**Annually** (Level 3):
- Comprehensive review of enforcement architecture
- Update CONTRIBUTING.md and PR templates
- Team retrospective (what's working, what's not)
- Consider expanding to new quality domains

**Ad-Hoc** (All Levels):
- Respond to false-positive reports (1-2 weeks)
- Update for pattern changes (when patterns evolve)
- Refine error messages (based on user feedback)

---

## Migration Path

### From Documentation-Only to SAP-031

**Week 1**: Level 1 (Discoverability)
**Week 2**: Level 2 Phase 1 (Validation script + pre-commit warn-only)
**Week 3**: Level 2 Phase 2 (Pre-commit blocking + CI/CD)
**Week 4**: Level 3 (Documentation + review + metrics)

**Total**: 4 weeks to full enforcement (Level 3 mastery)

---

## Support Resources

### Within chora-base

- [capability-charter.md](capability-charter.md) - Problem statement and solution design
- [protocol-spec.md](protocol-spec.md) - Technical specifications
- [AGENTS.md](AGENTS.md) - AI agent quick reference
- [ledger.md](ledger.md) - Version history and adoption tracking

### SAP Integrations

- [SAP-009: Agent Awareness](../agent-awareness/adoption-blueprint.md) - Prerequisite for Layer 1
- [SAP-006: Quality Gates](../quality-gates/adoption-blueprint.md) - Pre-commit hook framework
- [SAP-005: CI/CD Workflows](../ci-cd-workflows/adoption-blueprint.md) - CI/CD automation
- [SAP-030: Cross-Platform Fundamentals](../cross-platform-fundamentals/adoption-blueprint.md) - Reference implementation

### Reference Implementation

- [chora-base cross-platform enforcement](../../project-docs/cross-platform-enforcement-strategy.md) - Case study
- [.githooks/pre-commit-windows-compat](../../../.githooks/pre-commit-windows-compat) - Pre-commit hook example
- [.github/workflows/cross-platform-test.yml](../../../.github/workflows/cross-platform-test.yml) - CI/CD workflow example

---

**Version History**:
- **1.0.0** (2025-11-08): Initial adoption blueprint for Discoverability-Based Enforcement
  - 3 progressive levels (Basic/Advanced/Mastery)
  - Step-by-step instructions for all 5 layers
  - Validation checklists and success criteria
  - Cross-platform reference implementation
  - 4-week migration path
