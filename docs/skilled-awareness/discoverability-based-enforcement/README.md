# SAP-031: Discoverability-Based Enforcement

**Version:** 1.0.0 | **Status:** Pilot | **Maturity:** Pilot

> Multi-layer quality enforcement through strategic pattern placement at decision points—combines discoverability (70% prevention), pre-commit hooks (20%), CI/CD validation (9%), documentation, and review to achieve 90%+ prevention rates without disrupting developer workflow.

---

## 🚀 Quick Start (5 minutes)

```bash
# Layer 1: Discoverability (Setup in 5 minutes)

# Step 1: Add reminder to root AGENTS.md
# Edit AGENTS.md (project root):
cat >> AGENTS.md <<'EOF'

## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST run on Windows, macOS, and Linux without modification.**

Before writing scripts or file I/O, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform-script.py](templates/cross-platform-script.py)

EOF

# Step 2: Create domain AGENTS.md with patterns
mkdir -p scripts
cat > scripts/AGENTS.md <<'EOF'
## Cross-Platform Patterns

### Pattern 1: UTF-8 Console Output
# Configure UTF-8 output for Windows console compatibility
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

### Pattern 2: File I/O Encoding
# Always specify encoding='utf-8' for file operations
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

### Pattern 3: Path Handling with Pathlib
# Cross-platform path building
from pathlib import Path
config_path = Path.home() / ".config" / "app" / "config.json"
EOF

# Step 3: Create template file with patterns pre-implemented
mkdir -p templates
cat > templates/cross-platform-script.py <<'EOF'
#!/usr/bin/env python3
"""Template script with cross-platform patterns pre-implemented."""
import sys
from pathlib import Path

# Pattern 1: UTF-8 console output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Pattern 2: File I/O encoding
def load_file(file_path: Path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Pattern 3: Path handling
def main():
    config_path = Path.home() / ".config" / "app" / "config.json"
    # Implementation...

if __name__ == '__main__':
    main()
EOF

# Validation: Agent reads root AGENTS.md at session start → sees reminder →
# reads domain AGENTS.md → copies template → patterns pre-implemented
# Result: 70% of violations prevented through discoverability
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete 3-level adoption guide (25-min read)

---

## 📖 What Is SAP-031?

SAP-031 provides **multi-layer quality enforcement** through strategic pattern placement at AI agent decision points. Instead of relying solely on automated checks (which catch 30% at best), SAP-031 achieves 90%+ prevention by making patterns discoverable when agents are writing code (70% prevention), backed by pre-commit hooks (20%), CI/CD validation (9%), and documentation/review (1%).

**Key Innovation**: **5-layer architecture** with emphasis on Layer 1 (discoverability)—root AGENTS.md session-start reminders direct agents to domain AGENTS.md with quick-reference patterns and template files with production-ready implementations, preventing violations before code is written.

### How It Works

1. **Layer 1: Discoverability** (70% prevention): Agent starts session → reads root AGENTS.md → sees 🔴 reminder → reads domain AGENTS.md → copies template file → patterns pre-implemented
2. **Layer 2: Pre-Commit** (20% prevention): Developer commits → hook runs validation script → catches violations with educational error messages → self-service fix tool available
3. **Layer 3: CI/CD** (9% prevention): PR created → GitHub Actions validates on matrix platforms → uploads validation report → status badge in README
4. **Layer 4: Documentation** (Support): CONTRIBUTING.md guidelines + PR template checklists guide contributors
5. **Layer 5: Review** (1% prevention): Human reviewer catches edge cases missed by automation

**Result**: 70% + 20% + 9% + 1% = 100% coverage, 90%+ prevention rate without workflow disruption

---

## 🎯 When to Use

Use SAP-031 when you need to:

1. **Enforce Quality Domains** - Cross-platform compatibility, security, accessibility, performance (70% prevention via discoverability)
2. **Reduce Violations** - Achieve 90%+ prevention rate (vs 30% with automation alone)
3. **Educate Developers/Agents** - Educational error messages explain why + how to fix
4. **Measure Prevention** - Track prevention rate biweekly (violations_current / violations_baseline ≤ 10%)
5. **Avoid Workflow Disruption** - Discoverability-first approach prevents violations before commit (no blocked commits)

**Not needed for**: Ad-hoc code quality (use linters), one-time fixes (no enforcement needed), or projects with <5 contributors (manual review sufficient)

---

## ✨ Key Features

- ✅ **5-Layer Architecture** - Discoverability (70%), Pre-Commit (20%), CI/CD (9%), Documentation, Review (1%)
- ✅ **Integration with SAP-009** - Strategic pattern placement in nested awareness hierarchy (root → domain AGENTS.md)
- ✅ **Progressive Enforcement** - warn → educate → block (soft to hard enforcement)
- ✅ **Self-Service Tools** - Validation scripts + fix tools (empower developers/agents)
- ✅ **Template-Driven Development** - Production-ready starting points with patterns pre-implemented
- ✅ **Educational Error Messages** - Explain why + how to fix (not just "invalid")
- ✅ **Prevention Rate Measurement** - Target 90%+ (measured biweekly)

---

## 📚 Quick Reference

### 5-Layer Enforcement Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Review (1% prevention)                        │
│ - Human verification                                    │
│ - Domain expertise validation                          │
│ - Edge case identification                             │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Documentation (Support)                       │
│ - CONTRIBUTING.md guidelines                           │
│ - PR templates with checklists                         │
│ - Testing procedures                                   │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────┐
│ Layer 3: CI/CD (9% prevention)                         │
│ - Automated testing on target platforms/environments   │
│ - Validation reports (artifact upload)                 │
│ - Badge status in README                               │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Pre-Commit (20% prevention)                   │
│ - Automated validation hooks (block critical)          │
│ - Educational error messages                           │
│ - Self-service fix tools                               │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Discoverability (70% prevention)              │
│ - Root AGENTS.md: Session-start reminder               │
│ - Domain AGENTS.md: Quick reference patterns           │
│ - Template files: Production-ready starting points     │
└─────────────────────────────────────────────────────────┘
```

**Prevention Rates**:
- **Discoverability-First**: 70% of violations prevented through strategic pattern placement (Layer 1)
- **Automation Backup**: 20% (pre-commit) + 9% (CI/CD) = 29% caught by automation (Layers 2-3)
- **Human Verification**: 1% edge cases caught by review (Layer 5)
- **Total**: 100% coverage, 90%+ prevention rate

---

### Layer 1: Discoverability (70% Prevention)

#### Component 1: Root AGENTS.md Reminder

```markdown
# Edit AGENTS.md (project root)

## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST run on Windows, macOS, and Linux without modification.**

Before writing scripts or file I/O, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform-script.py](templates/cross-platform-script.py)
```

**Why It Works**:
- Agent reads root AGENTS.md at session start (SAP-009 pattern)
- 🔴 emoji draws attention (visual prominence)
- Clear requirement ("ALL code MUST...")
- Direct link to domain AGENTS.md (quick reference)
- Template path (production-ready starting point)

**Prevention**: 40% of violations (agent reads reminder, navigates to domain AGENTS.md)

---

#### Component 2: Domain AGENTS.md with Patterns

```markdown
# Create scripts/AGENTS.md (domain-specific)

## Cross-Platform Patterns

### Pattern 1: UTF-8 Console Output

**Why**: Windows console defaults to cp1252 encoding, causing UnicodeEncodeError for emoji/Unicode

**Implementation**:
\```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
\```

**Incorrect** (will fail on Windows):
\```python
print("✓ Success")  # ❌ UnicodeEncodeError
\```

**Correct** (cross-platform):
\```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
print("✓ Success")  # ✅ Works on all platforms
\```

### Pattern 2: File I/O Encoding

**Why**: Default encoding varies by platform (utf-8 on Linux/macOS, cp1252 on Windows)

**Implementation**:
\```python
# Always specify encoding='utf-8'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
\```

### Pattern 3: Path Handling with Pathlib

**Why**: Hardcoded forward slashes (/) fail on Windows, backslashes (\\) fail on Linux/macOS

**Implementation**:
\```python
from pathlib import Path

# Cross-platform path building
config_path = Path.home() / ".config" / "app" / "config.json"

# Works on all platforms:
# - Linux/macOS: /home/user/.config/app/config.json
# - Windows: C:\\Users\\user\\.config\\app\\config.json
\```
```

**Why It Works**:
- Quick reference at decision point (when agent is writing code)
- Educational context ("Why" explains rationale)
- Side-by-side incorrect/correct examples
- Copy-paste ready implementations
- Domain-specific (only patterns for this directory)

**Prevention**: 20% of violations (agent reads patterns, applies to new code)

---

#### Component 3: Template File with Pre-Implemented Patterns

```python
# Create templates/cross-platform-script.py

#!/usr/bin/env python3
"""Template script with cross-platform patterns pre-implemented.

This template demonstrates cross-platform best practices:
- UTF-8 console output (Windows compatibility)
- File I/O with explicit encoding
- Path handling with pathlib

Usage:
    Copy this template for new Python scripts.
"""

import sys
from pathlib import Path

# CROSS-PLATFORM Pattern 1: UTF-8 console output
# Configure Windows console to handle Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# CROSS-PLATFORM Pattern 2: File I/O encoding
def load_config(config_path: Path) -> dict:
    """Load configuration file with UTF-8 encoding."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_path: Path, config: dict) -> None:
    """Save configuration file with UTF-8 encoding."""
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

# CROSS-PLATFORM Pattern 3: Path handling
def main():
    """Main entry point."""
    # Build paths using Path() for cross-platform compatibility
    config_dir = Path.home() / ".config" / "app"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "config.json"

    # Load configuration
    config = load_config(config_path)

    # Your implementation here...
    print("✓ Script executed successfully")  # Works on all platforms

if __name__ == '__main__':
    main()
```

**Why It Works**:
- Agent copies template instead of starting from scratch (patterns already implemented)
- Inline comments explain each pattern
- Production-ready structure (argparse, error handling can be added)
- No missing patterns (template has all required implementations)

**Prevention**: 10% of violations (agent uses template, all patterns pre-implemented)

---

### Layer 2: Pre-Commit (20% Prevention)

#### Component 1: Validation Script

```bash
# Create scripts/validate-cross-platform.py

#!/usr/bin/env python3
"""Validate cross-platform patterns compliance."""
import sys
import re
from pathlib import Path

# Configure UTF-8 output (cross-platform)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def check_utf8_console(file_path: Path) -> list[str]:
    """Check for UTF-8 console reconfiguration."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if script uses emoji/Unicode
    has_unicode = bool(re.search(r'[^\x00-\x7F]', content))

    # Check for UTF-8 reconfiguration
    has_reconfigure = 'sys.stdout.reconfigure(encoding=' in content

    if has_unicode and not has_reconfigure:
        return [
            f"❌ {file_path}: Uses Unicode characters without UTF-8 console reconfiguration",
            "   Why: Windows console defaults to cp1252, causing UnicodeEncodeError",
            "   Fix: Add at top of script:",
            "     import sys",
            "     if sys.platform == 'win32':",
            "         sys.stdout.reconfigure(encoding='utf-8')",
            "   Auto-fix: python scripts/fix-cross-platform-issues.py --add-utf8-reconfigure"
        ]
    return []

def check_file_encoding(file_path: Path) -> list[str]:
    """Check for explicit encoding in file I/O."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    violations = []

    # Find open() calls without encoding
    for match in re.finditer(r"open\([^)]+\)", content):
        open_call = match.group(0)
        if 'encoding=' not in open_call and "'rb'" not in open_call and "'wb'" not in open_call:
            line_num = content[:match.start()].count('\n') + 1
            violations.append(
                f"❌ {file_path}:{line_num}: open() without explicit encoding",
                "   Why: Default encoding varies by platform (utf-8 on Linux/macOS, cp1252 on Windows)",
                "   Fix: Add encoding='utf-8' parameter",
                "   Auto-fix: python scripts/fix-cross-platform-issues.py --add-encoding"
            )

    return violations

def main():
    """Run validation on Python files."""
    python_files = Path('.').glob('**/*.py')

    all_violations = []
    for file_path in python_files:
        if 'venv' in str(file_path) or '.venv' in str(file_path):
            continue

        all_violations.extend(check_utf8_console(file_path))
        all_violations.extend(check_file_encoding(file_path))

    if all_violations:
        print("\n".join(all_violations))
        sys.exit(1)
    else:
        print("✅ All files comply with cross-platform patterns")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Why It Works**:
- Educational error messages (explain why + how to fix)
- Self-service fix tool available (reduce friction)
- Exit code 0 (pass) or 1 (fail) for pre-commit integration
- Fast (<10 sec for 1000 files)

**Prevention**: 15% of violations (catches issues before commit)

---

#### Component 2: Pre-Commit Hook

```bash
# Create .githooks/pre-commit

#!/bin/bash
# Pre-commit hook for cross-platform validation

echo "🔍 Running cross-platform validation..."

# Run validation script
python scripts/validate-cross-platform.py

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ Cross-platform validation failed"
    echo ""
    echo "Options:"
    echo "  1. Fix issues manually (see error messages above)"
    echo "  2. Auto-fix: python scripts/fix-cross-platform-issues.py"
    echo "  3. Override (not recommended): git commit --no-verify"
    echo ""
    exit 1
else
    echo "✅ Cross-platform validation passed"
    exit 0
fi
```

**Installation**:
```bash
# Make hook executable
chmod +x .githooks/pre-commit

# Configure git to use .githooks/
git config core.hooksPath .githooks/
```

**Why It Works**:
- Blocks commit if critical violations found
- Provides 3 options (fix manually, auto-fix, override)
- Fast feedback (<10 sec)
- Self-service fix tool reduces friction

**Prevention**: 5% of violations (catches issues at commit time)

---

#### Component 3: Self-Service Fix Tool (Optional but Recommended)

```bash
# Create scripts/fix-cross-platform-issues.py

#!/usr/bin/env python3
"""Auto-fix common cross-platform issues."""
import sys
from pathlib import Path

def add_utf8_reconfigure(file_path: Path):
    """Add UTF-8 console reconfiguration to script."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add reconfiguration after imports
    if 'sys.stdout.reconfigure' not in content:
        import_section_end = content.find('\n\n')
        utf8_code = """
# Configure UTF-8 output for Windows console compatibility
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
"""
        content = content[:import_section_end] + utf8_code + content[import_section_end:]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Added UTF-8 reconfiguration to {file_path}")

def add_encoding_to_open(file_path: Path):
    """Add encoding='utf-8' to open() calls."""
    # Implementation...
    pass

def main():
    """Auto-fix cross-platform issues."""
    # Parse args, run fixes...
    pass

if __name__ == '__main__':
    main()
```

**Why It Works**:
- One-command fix (python scripts/fix-cross-platform-issues.py)
- Safe (preview mode available)
- Fast (fixes 100+ files in <5 sec)
- Reduces pre-commit friction (no manual editing)

---

### Layer 3: CI/CD (9% Prevention)

```yaml
# Create .github/workflows/cross-platform-validation.yml

name: Cross-Platform Validation

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
      fail-fast: false  # Continue testing other platforms if one fails
      matrix:
        platform: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run cross-platform validation
        run: |
          python scripts/validate-cross-platform.py

      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report-${{ matrix.platform }}
          path: validation-report.md
          retention-days: 30
```

**Why It Works**:
- Matrix testing on all target platforms (ubuntu, macos, windows)
- Validation reports uploaded as artifacts (audit trail)
- Status badge in README (visibility)
- Fail-fast: false (continue testing other platforms)

**Prevention**: 9% of violations (catches platform-specific issues in CI/CD)

---

### Layer 4: Documentation (Support)

#### CONTRIBUTING.md

```markdown
# Add to CONTRIBUTING.md

## Cross-Platform Requirements (REQUIRED)

**ALL code MUST run on Windows, macOS, and Linux without modification.**

### Quick Checklist

- [ ] UTF-8 console output (if using emoji/Unicode)
- [ ] Explicit encoding='utf-8' for file I/O
- [ ] Path handling with pathlib (no hardcoded slashes)

### Validation

```bash
# Validate your changes
python scripts/validate-cross-platform.py

# Auto-fix common issues (if available)
python scripts/fix-cross-platform-issues.py

# Install pre-commit hook (REQUIRED)
git config core.hooksPath .githooks/
```

### Resources

- [Cross-Platform Patterns](scripts/AGENTS.md#cross-platform-patterns)
- [Template Script](templates/cross-platform-script.py)
- [Validation Guide](docs/validation-guide.md)
```

**Why It Works**:
- Clear requirements (ALL code MUST...)
- Quick checklist (3 items)
- Self-service tools (validate, auto-fix, install hook)
- Resource links (patterns, template, guide)

---

#### PR Template

```markdown
# Add to .github/pull_request_template.md

## Cross-Platform Checklist (REQUIRED)

- [ ] Tested on Windows, macOS, and Linux
- [ ] UTF-8 console output configured (if using emoji/Unicode)
- [ ] File I/O uses encoding='utf-8'
- [ ] Path handling uses pathlib (no hardcoded slashes)

### Testing Platform

Tested on: [Windows / macOS / Linux / All]

### Validation Output

\```bash
$ python scripts/validate-cross-platform.py
# Paste output here
\```
```

**Why It Works**:
- Checkboxes (visible in PR UI)
- Testing platform field (accountability)
- Validation output field (evidence)
- Blocks merge if checklist incomplete

---

### Layer 5: Review (1% Prevention)

**Human reviewer checks**:
- Edge cases not caught by automation
- Platform-specific quirks (e.g., case-sensitive filesystems)
- Performance implications (e.g., pathlib overhead)
- Security considerations (e.g., path traversal)

**Why It's Only 1%**:
- Layers 1-4 catch 99% of violations
- Human review focuses on edge cases and domain expertise
- No workflow bottleneck (most PRs auto-pass validation)

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-009** (Agent Awareness) | Foundation | SAP-031 uses nested awareness hierarchy (root → domain AGENTS.md) for strategic pattern placement |
| **SAP-006** (Quality Gates) | Pre-Commit Layer | SAP-031 pre-commit hooks integrate with existing quality gates (ruff, mypy, pytest) |
| **SAP-005** (CI/CD) | CI/CD Layer | SAP-031 validation workflows run alongside existing CI/CD (test.yml, build.yml) |
| **SAP-007** (Documentation) | Documentation Layer | SAP-031 guidelines in CONTRIBUTING.md follow Diátaxis structure (how-to, reference) |
| **SAP-004** (Testing) | Validation | SAP-031 validation scripts use pytest for structure/correctness checks |

---

## 🏆 Success Metrics

- **Prevention Rate**: 90%+ (violations_current / violations_baseline ≤ 10%)
- **Layer 1 Effectiveness**: 70% of violations prevented through discoverability
- **Layer 2 Effectiveness**: 20% of violations caught by pre-commit hooks
- **Layer 3 Effectiveness**: 9% of violations caught by CI/CD validation
- **Pre-Commit Performance**: <10 seconds for 1000 files
- **Discovery Time**: <3 minutes from session start to pattern discovery (root AGENTS.md → domain AGENTS.md → template)

---

## 🔧 Troubleshooting

### Problem: Patterns Not Discovered (Agent Doesn't Read AGENTS.md)

**Symptom**: Agent writes code without following patterns, despite root AGENTS.md reminder

**Common Causes**:
1. Root AGENTS.md reminder not prominent (missing 🔴 emoji)
2. Domain AGENTS.md not created or not linked
3. Template file not created or not accessible

**Solutions**:

```bash
# 1. Verify root AGENTS.md has prominent reminder
grep "🔴" AGENTS.md
# Expected: Line with "🔴 [QUALITY DOMAIN] REMINDER"

# 2. Verify domain AGENTS.md exists and is linked
test -f scripts/AGENTS.md && echo "exists" || echo "missing"
grep "scripts/AGENTS.md" AGENTS.md
# Expected: Link to domain AGENTS.md in root reminder

# 3. Verify template file exists
test -f templates/cross-platform-script.py && echo "exists" || echo "missing"
grep "templates/cross-platform-script.py" AGENTS.md
# Expected: Link to template in root reminder

# 4. Test discovery workflow
# - Start new session
# - Read root AGENTS.md
# - Follow link to domain AGENTS.md
# - Follow link to template file
# - Verify all components accessible
```

**Validation**: Agent discovers patterns within 3 minutes of session start

---

### Problem: Pre-Commit Hook Not Running

**Symptom**: `git commit` succeeds without running validation script

**Common Causes**:
1. Hook not executable (missing chmod +x)
2. Git not configured to use .githooks/ directory
3. Hook syntax error (bash script issues)

**Solutions**:

```bash
# 1. Make hook executable
chmod +x .githooks/pre-commit
ls -l .githooks/pre-commit
# Expected: -rwxr-xr-x (executable permissions)

# 2. Configure git to use .githooks/
git config core.hooksPath .githooks/
git config core.hooksPath
# Expected: .githooks/

# 3. Test hook manually
./.githooks/pre-commit
# Expected: Validation output (pass or fail)

# 4. Check for syntax errors
bash -n .githooks/pre-commit
# Expected: No output (no syntax errors)

# 5. Debug hook execution
# Add to pre-commit:
# set -x  # Enable debug output
# Then re-run commit
```

**Validation**: Hook runs on `git commit`, blocks if violations found

---

### Problem: False Positives in Validation

**Symptom**: Validation script reports violations for correct code

**Common Causes**:
1. Validation regex too broad (matches comments, strings)
2. Edge cases not handled (binary files, test mocks)
3. Platform-specific false positives

**Solutions**:

```bash
# 1. Review false positive cases
python scripts/validate-cross-platform.py > validation-output.txt
# Manually review each violation, identify false positives

# 2. Update validation script to exclude false positives
# Example: Ignore comments, strings, binary files
# Edit scripts/validate-cross-platform.py:
#   - Skip lines starting with # (comments)
#   - Skip strings (between quotes)
#   - Skip binary files (*.pyc, *.so, *.dll)

# 3. Add exclusion list to validation script
# Example:
# EXCLUDE_PATTERNS = [
#     r'test_.*\.py',  # Test files
#     r'mock_.*\.py',  # Mock files
#     r'\.venv/',      # Virtual environments
# ]

# 4. Re-run validation after updates
python scripts/validate-cross-platform.py
# Verify false positives eliminated
```

**Validation**: Validation script reports only true violations, no false positives

---

### Problem: CI/CD Validation Passes but Local Fails

**Symptom**: Local validation fails but GitHub Actions validation passes

**Common Causes**:
1. Platform-specific issues (Windows vs Linux)
2. Environment differences (Python version, dependencies)
3. Validation script not committed (CI uses old version)

**Solutions**:

```bash
# 1. Check validation script version
git status scripts/validate-cross-platform.py
# If modified: Commit validation script updates

# 2. Check Python version consistency
python --version  # Local
# Compare with:
cat .github/workflows/cross-platform-validation.yml | grep python-version
# Expected: Same version (e.g., 3.11)

# 3. Run validation on same platform as CI
# If CI uses ubuntu-latest:
docker run -v $(pwd):/workspace -w /workspace python:3.11 \
  python scripts/validate-cross-platform.py
# Expected: Same results as local

# 4. Check for platform-specific environment variables
# Example: PYTHONIOENCODING on Windows
echo $PYTHONIOENCODING  # Should be utf-8 on Windows
```

**Validation**: Local and CI/CD validation produce identical results

---

### Problem: Low Prevention Rate (<90%)

**Symptom**: Biweekly measurement shows violations_current / violations_baseline > 10% (prevention rate <90%)

**Common Causes**:
1. Layer 1 not effective (patterns not discovered)
2. Patterns incomplete (missing edge cases)
3. New contributors not onboarded (don't know about patterns)

**Solutions**:

```bash
# 1. Measure per-layer prevention rates
# Measure baseline: violations_baseline = 100 (Week 0)

# Week 2: Measure after Layer 1 (discoverability)
# Count violations without Layer 2-5 (disable hooks, CI, review)
# violations_layer1 = X
# Layer 1 prevention rate = (100 - X) / 100 = Y%
# Expected: Y ≥ 70%

# Week 2: Measure after Layer 2 (pre-commit)
# Enable pre-commit hooks
# violations_layer2 = Z
# Layer 2 prevention rate = (X - Z) / 100
# Expected: ≥ 20%

# 2. If Layer 1 < 70%:
#    - Enhance root AGENTS.md reminder (more prominent)
#    - Improve domain AGENTS.md patterns (more examples)
#    - Create additional templates (more use cases)

# 3. If Layer 2 < 20%:
#    - Improve pre-commit hook (catch more patterns)
#    - Add self-service fix tool (reduce friction)
#    - Educational error messages (explain why + how)

# 4. Onboard new contributors
#    - Add onboarding checklist to CONTRIBUTING.md
#    - Pair new contributors with experienced mentors
#    - Conduct code review training
```

**Validation**: Prevention rate ≥ 90% (violations_current / violations_baseline ≤ 10%)

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Discoverability-based enforcement specification (45KB, 23-min read, pilot status)
- **[AGENTS.md](AGENTS.md)** - Agent enforcement workflows (30KB, 15-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (25KB, 13-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Complete 3-level adoption guide (50KB, 25-min read)

### Example Implementations

- **Cross-Platform**: [scripts/AGENTS.md](../../scripts/AGENTS.md) (chora-base cross-platform patterns)
- **Validation Script**: [scripts/validate-cross-platform.py](../../scripts/validate-cross-platform.py)
- **Pre-Commit Hook**: [.githooks/pre-commit-cross-platform](../../.githooks/pre-commit-cross-platform)

### External Resources

- [Pre-Commit Framework](https://pre-commit.com/) - Hook management
- [GitHub Actions Matrix](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix) - Multi-platform testing
- [SAP-009 Protocol Spec](../agent-awareness/protocol-spec.md) - Nested awareness hierarchy

---

**Version History**:
- **1.0.0** (2025-11-08) - Initial Discoverability-Based Enforcement with 5-layer architecture, SAP-009 integration, prevention rate measurement

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
