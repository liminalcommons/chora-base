# How to Migrate Bash Scripts to Python (Cross-Platform)

**Purpose**: Migrate bash automation scripts to Python for Windows, macOS, and Linux compatibility

**When to Use**: When adopting chora-base patterns or creating new automation scripts for multi-platform teams

**Time**: 1-4 hours per script (depending on complexity)

---

## Overview

This guide documents the bash→Python migration strategy used in chora-base v4.3.0, enabling **Windows developers to contribute immediately** without platform-specific workarounds.

**Business Driver**: The chora-compose project experienced **significant rework** when migrating from Windows→Mac development due to bash-only scripts. This migration prevents that pain for all adopters.

**What You'll Learn**:
- ✅ When to migrate (and when not to)
- ✅ Cross-platform patterns (pathlib, subprocess, ASCII output)
- ✅ Step-by-step migration workflow
- ✅ Testing on Windows
- ✅ Common pitfalls and solutions

**Migration Stats** (chora-base v4.3.0):
- **Scripts migrated**: 6 bash scripts → 6 Python scripts
- **Lines of code**: 1,189 bash → 1,800 Python (50% increase for robustness)
- **Time invested**: ~18 hours (audit + migration + testing)
- **Windows compatibility**: 100% (all scripts tested on Windows 11)
- **Platforms supported**: Windows, macOS, Linux

---

## Prerequisites

### 1. Python Environment

```bash
# Python 3.11+ required (3.8+ minimum)
python --version

# Install cross-platform libraries
pip install PyYAML  # For YAML parsing (optional, only if needed)
```

### 2. Understanding Your Script

Before migrating, answer:
- **What does it do?** (file operations, git commands, validation, etc.)
- **What's the complexity?** (lines of code, dependencies)
- **What are the inputs/outputs?** (args, exit codes, file writes)
- **What's platform-specific?** (sed, find, grep, disk space checks)

### 3. Reference Documentation

Read these SAPs first:
- [SAP-030: Cross-Platform Fundamentals](../../skilled-awareness/cross-platform-fundamentals/awareness-guide.md)
- [SAP-008: Automation Scripts](../../skilled-awareness/automation-scripts/protocol-spec.md#23-cross-platform-support)

---

## When to Migrate (Decision Tree)

### ✅ Migrate to Python If:

1. **Script uses platform-specific commands**:
   - `sed -i` (different on macOS vs Linux)
   - `find` with complex flags
   - `df` for disk space (fails on Windows)
   - `yq` (requires separate installation)

2. **Script will be used by Windows developers**

3. **Script does complex text processing** (regex, parsing)

4. **Script needs robust error handling**

5. **Script is part of CI/CD** (multi-OS testing)

### ❌ Keep Bash If:

1. **Script is a simple wrapper** (e.g., `docker-compose up`)

2. **Script only runs in CI** (Linux-only environment)

3. **Migration cost exceeds benefit** (5-line script, rarely used)

---

## Step 1: Audit the Bash Script

### 1.1 Analyze Complexity

Create an audit document (see `docs/project-docs/bash-script-migration-audit.md` for template):

```bash
# Count lines
wc -l scripts/your-script.sh

# Identify dependencies
grep -E "command -v|which" scripts/your-script.sh

# Find platform-specific patterns
grep -E "sed -i|find.*-exec|df|yq" scripts/your-script.sh
```

**Complexity Rating**:
- ⭐ (Simple): <50 lines, basic file ops
- ⭐⭐ (Medium): 50-150 lines, some validation
- ⭐⭐⭐ (Complex): 150-300 lines, regex, multiple deps
- ⭐⭐⭐⭐ (Very Complex): 300-500 lines, git ops, YAML parsing
- ⭐⭐⭐⭐⭐ (Extremely Complex): 500+ lines, orchestration, multiple scripts

**Time Estimates**:
- ⭐: 1 hour
- ⭐⭐: 2-3 hours
- ⭐⭐⭐: 3-4 hours
- ⭐⭐⭐⭐: 4-6 hours
- ⭐⭐⭐⭐⭐: 6-10 hours

### 1.2 Identify Cross-Platform Issues

Common issues to document:

| Bash Pattern | Cross-Platform Issue | Python Solution |
|--------------|----------------------|-----------------|
| Unicode symbols (✓✗⚠ℹ) | **Fails on Windows console** | Use ASCII: `[OK]` `[FAIL]` `[WARN]` |
| `df` (disk space) | **No df on Windows** | `shutil.disk_usage()` |
| `sed -i ''` (macOS) | **Different on Linux** | `re.sub()` + file I/O |
| `find ... -exec` | **Complex, bash-specific** | `Path.glob("**/*.ext")` |
| `grep -oE` | **Regex differences** | `re.findall()` |
| `yq` (YAML parser) | **Requires installation** | `import yaml` (PyYAML) |
| ANSI color codes | **Terminal-dependent** | Use ASCII or detect terminal |

---

## Step 2: Set Up Python Script Structure

### 2.1 Create Python File

```bash
# Create Python equivalent
touch scripts/your-script.py
chmod +x scripts/your-script.py
```

### 2.2 Standard Template

```python
#!/usr/bin/env python3
"""One-line description of what this script does.

Purpose: Detailed explanation
Usage: python scripts/your-script.py [OPTIONS]

Part of SAP-008: Cross-Platform Automation Scripts
"""

import sys
from pathlib import Path

# Optional imports (only if needed)
import subprocess  # For running commands
import json       # For JSON output
import re         # For regex
import yaml       # For YAML (requires pip install PyYAML)


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()

    # Validate prerequisites
    validate_environment()

    # Do the work
    result = do_work(args)

    # Exit with appropriate code
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
```

---

## Step 3: Apply Cross-Platform Patterns

### Pattern 1: File Operations (pathlib)

```python
# ✅ Cross-platform
from pathlib import Path

# Find files
markdown_files = list(Path("docs").glob("**/*.md"))

# Read file
content = Path("config.json").read_text(encoding='utf-8')

# Write file
Path("output.txt").write_text(content, encoding='utf-8')

# Check existence
if Path("file.txt").exists():
    print("[OK] File exists")

# ❌ Avoid
# os.system("find docs -name '*.md'")  # Platform-specific
# subprocess.run(["cat", "file.txt"])  # No 'cat' on Windows
```

### Pattern 2: Command Execution (subprocess)

```python
# ✅ Cross-platform
import subprocess

result = subprocess.run(
    ["git", "status"],
    capture_output=True,
    text=True,
    check=True  # Raises exception on error
)

# ❌ Avoid
# subprocess.run("git status", shell=True)  # Security risk + platform-specific
```

### Pattern 3: Output Formatting (ASCII)

```python
# ✅ Cross-platform (ASCII)
print("[OK] Task completed")
print("[FAIL] Task failed")
print("[WARN] Warning message")
print("[INFO] Information")

# ❌ Avoid (Unicode - fails on Windows)
# print("✓ Task completed")  # UnicodeEncodeError
# print("✗ Task failed")
# print("⚠ Warning")
```

### Pattern 4: Path Separators

```python
# ✅ Cross-platform
config_path = Path("config") / "settings.json"
script_path = Path("scripts") / "utils.py"

# ❌ Avoid
# config_path = "config/settings.json"  # Fails on Windows (should be config\\)
```

### Pattern 5: Disk Space (Cross-Platform)

```python
# ✅ Cross-platform
import shutil

disk_usage = shutil.disk_usage(".")
available_mb = disk_usage.free // (1024 * 1024)

if available_mb < 100:
    print(f"[WARN] Low disk space: {available_mb}MB")

# ❌ Avoid
# subprocess.run(["df", "-h", "."])  # No 'df' on Windows
```

### Pattern 6: Error Handling

```python
# ✅ Proper error handling
try:
    result = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"[FAIL] Git command failed: {e.stderr}")
    sys.exit(1)
except FileNotFoundError:
    print("[FAIL] Git not found - install from https://git-scm.com")
    sys.exit(1)
```

---

## Step 4: Migrate Step-by-Step

### 4.1 Priority Order (Simple → Complex)

Migrate in this order to build confidence:

1. **Simple file operations** (glob, read, write)
2. **Validation logic** (checks, validation)
3. **Command execution** (git, subprocess)
4. **Complex logic** (parsing, regex, YAML)

### 4.2 Incremental Testing

Test after each function:

```python
# Test file finding
def test_find_files():
    files = list(Path("docs").glob("**/*.md"))
    print(f"[INFO] Found {len(files)} markdown files")
    for f in files[:5]:  # Show first 5
        print(f"  - {f}")

if __name__ == "__main__":
    test_find_files()
```

---

## Step 5: Test on Windows

### 5.1 Windows Testing Checklist

- [ ] Run `python scripts/your-script.py --help`
- [ ] Verify output (no Unicode errors)
- [ ] Test with paths containing spaces: `C:\Program Files\`
- [ ] Test with backslashes in paths
- [ ] Check exit codes: `echo %ERRORLEVEL%` (Windows CMD)
- [ ] Test JSON output mode (if applicable)

### 5.2 Common Windows Issues

**Issue**: `UnicodeEncodeError: 'charmap' codec can't encode character`

**Solution**: Use ASCII output only (no ✓✗⚠ symbols)

```python
# Before: print("✓ Success")
# After:  print("[OK] Success")
```

**Issue**: `FileNotFoundError` with forward slashes

**Solution**: Use `pathlib.Path` everywhere

```python
# Before: open("docs/file.md")
# After:  Path("docs") / "file.md"
```

**Issue**: Command not found (e.g., `sed`, `grep`)

**Solution**: Use Python equivalents

```python
# Before: subprocess.run(["sed", "-i", "s/foo/bar/", "file.txt"])
# After:  use re.sub() with file I/O
```

---

## Step 6: Add Quality Features

### 6.1 Add --dry-run Mode

```python
def process_files(files, dry_run=False):
    """Process files with dry-run support."""
    for file_path in files:
        if dry_run:
            print(f"[DRY RUN] Would process: {file_path}")
        else:
            # Actually process
            process_file(file_path)
            print(f"[OK] Processed: {file_path}")
```

### 6.2 Add --json Output

```python
import json

def output_results(results, json_mode=False):
    """Output results in human or JSON format."""
    if json_mode:
        print(json.dumps(results, indent=2))
    else:
        print(f"[INFO] Processed {results['count']} files")
        print(f"[OK] Success: {results['success']}")
        print(f"[FAIL] Failed: {results['failed']}")
```

### 6.3 Add Progress Indicators

```python
def process_many_files(files):
    """Process files with progress."""
    total = len(files)
    for i, file_path in enumerate(files, 1):
        print(f"[INFO] Processing {i}/{total}: {file_path.name}")
        process_file(file_path)
```

---

## Step 7: Update Documentation

### 7.1 Update justfile

```makefile
# Add recipe for new Python script
your-task:
    python scripts/your-script.py

# With arguments
your-task-with-args ARG:
    python scripts/your-script.py {{ARG}}
```

### 7.2 Update README/Docs

Replace bash references:

```markdown
<!-- Before -->
Run validation: `bash scripts/validate.sh`

<!-- After -->
Run validation: `python scripts/validate.py` or `just validate`
```

---

## Step 8: Deprecate Bash Script

### 8.1 Add Deprecation Warning

```bash
#!/usr/bin/env bash
# DEPRECATED: This script has been migrated to Python for cross-platform support
# Use: python scripts/your-script.py
# See: docs/user-docs/how-to/bash-to-python-migration.md
#
# This file will be removed in v5.0.0 (deprecated v4.3.0)

echo "[WARN] This bash script is deprecated!"
echo "[INFO] Use: python scripts/your-script.py"
echo ""

# Original script continues below (for backwards compatibility)
# ...
```

### 8.2 Move to Deprecated Directory (Optional)

```bash
# After 1-2 release cycles
mkdir -p scripts/deprecated
mv scripts/your-script.sh scripts/deprecated/
```

---

## Troubleshooting

### Issue: "No module named 'yaml'"

**Fix**: Install PyYAML

```bash
pip install PyYAML
```

### Issue: Script works on Mac but fails on Windows

**Check**:
1. Unicode symbols in output → Use ASCII `[OK]` `[FAIL]`
2. Hardcoded `/` separators → Use `pathlib.Path`
3. Bash commands (`sed`, `grep`) → Use Python equivalents
4. Line endings (LF vs CRLF) → Add `.gitattributes`

### Issue: pathlib doesn't work with subprocess

**Fix**: Convert Path to string

```python
file_path = Path("docs/file.md")

# ❌ subprocess.run(["cat", file_path])
# ✅ subprocess.run(["cat", str(file_path)])
```

---

## Real-World Examples

See these successful migrations in chora-base v4.3.0:

1. **validate-prerequisites.py** (400 lines, ⭐⭐)
   - Before: 349-line bash script with `df` disk checks
   - After: `shutil.disk_usage()`, tool version validation
   - Time: 2-3 hours

2. **rollback-migration.py** (106 lines, ⭐)
   - Before: 29-line bash script with `find` command
   - After: `Path.glob("**/*.backup")`
   - Time: 1 hour

3. **validate-links.py** (226 lines, ⭐⭐⭐)
   - Before: 109-line bash script calling Python for path normalization!
   - After: Pure Python with `re.findall()` and pathlib
   - Time: 2-3 hours

4. **merge-upstream-structure.py** (486 lines, ⭐⭐⭐⭐⭐)
   - Before: 515-line bash script requiring `yq`
   - After: PyYAML, Git operations via subprocess
   - Time: 4-6 hours (most complex)

**Audit Document**: [bash-script-migration-audit.md](../../project-docs/bash-script-migration-audit.md)

---

## Success Criteria

Migration is complete when:

- ✅ Python script produces identical output to bash version
- ✅ Runs on Windows without errors
- ✅ No Unicode encoding issues
- ✅ No hardcoded path separators
- ✅ Proper error handling (try/except)
- ✅ Exit codes match bash version (0 = success, 1 = fail)
- ✅ Documentation updated (README, justfile)
- ✅ Tested on Windows, macOS, Linux

---

## Related Resources

**SAPs**:
- [SAP-030: Cross-Platform Fundamentals](../../skilled-awareness/cross-platform-fundamentals/awareness-guide.md) - Core patterns
- [SAP-031: Python Environments](../../skilled-awareness/cross-platform-python-environments/awareness-guide.md) - Python setup
- [SAP-032: CI/CD Quality Gates](../../skilled-awareness/cross-platform-ci-cd-quality-gates/awareness-guide.md) - Multi-OS testing
- [SAP-008: Automation Scripts](../../skilled-awareness/automation-scripts/protocol-spec.md) - Script standards

**Tools**:
- `scripts/platform-info.py` - Platform detection utility
- `scripts/check-python-env.py` - Python environment validation

**Project Documentation**:
- `docs/project-docs/bash-script-migration-audit.md` - Migration audit (v4.3.0)
- `docs/project-docs/cross-platform-sap-suite-plan.md` - Strategic plan

---

**Last Updated**: 2025-11-03 (v4.3.0)
**Maintainer**: chora-base core team
**Status**: Active (6/6 bash scripts migrated successfully)
