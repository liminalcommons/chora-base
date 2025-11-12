# Windows Testing Checklist

**Purpose**: Ensure chora-base works correctly on Windows systems

**Frequency**: Run before major releases or when modifying cross-platform code

**Platform**: Windows 10/11 (PowerShell or CMD)

---

## Quick Start

### Minimal Test (5 minutes)

Run these essential tests to verify basic Windows compatibility:

```powershell
# 1. Validate encoding
python scripts/validate-windows-compat.py --scripts-only

# 2. Test fast-setup
python scripts/create-capability-server.py --help

# 3. Test SAP listing (emoji output)
python scripts/install-sap.py --list
```

**Expected**: No errors, emojis display correctly

---

## Full Test Suite

### Environment Setup

**Python Version**: 3.8+

```powershell
# Check Python version
python --version

# Check encoding
python scripts/platform-info.py

# Install dependencies (if needed)
pip install -r requirements.txt
```

**Expected Output**:
```
Platform: win32
Python Version: 3.x.x
Default Encoding: utf-8 or cp1252 (both work after our fixes)
```

---

## Test Category 1: Emoji Output

**Purpose**: Verify scripts display emojis correctly (no `UnicodeEncodeError`)

### Test 1.1: Fast-Setup Script

```powershell
python scripts/create-capability-server.py --help
```

**Expected**:
- ✅ Help text displays
- ✅ No encoding errors
- ✅ Emojis render (or show as ? boxes, which is acceptable)

---

### Test 1.2: SAP Installation

```powershell
python scripts/install-sap.py --list
```

**Expected**:
- ✅ SAP list displays with checkmarks (✓)
- ✅ No `UnicodeEncodeError`
- ✅ Color codes work or degrade gracefully

---

### Test 1.3: SAP Validation

```powershell
python scripts/validate-sap-infrastructure.py --help
```

**Expected**:
- ✅ Help displays
- ✅ No encoding errors

---

### Test 1.4: Generate SAP (with emojis)

```powershell
python scripts/generate-sap.py SAP-999 --dry-run
```

**Expected**:
- ✅ Dry run output displays
- ✅ Status emojis (🔍, ✅, ⚠️) render or degrade gracefully
- ✅ No crashes

---

## Test Category 2: File I/O Encoding

**Purpose**: Verify file operations preserve UTF-8 encoding

### Test 2.1: Create Project with Unicode Characters

```powershell
# Create test output directory
mkdir C:\test-chora-output -ErrorAction SilentlyContinue

# Create project with emojis in description
python scripts/create-capability-server.py --name "Test Server" --output C:\test-chora-output\test-proj --namespace testns --description "Test with emoji: 🚀"
```

**Expected**:
- ✅ Project created successfully
- ✅ Files contain correct UTF-8 encoding
- ✅ README.md preserves emoji in description

**Validation**:
```powershell
# Check created files
cat C:\test-chora-output\test-proj\README.md | Select-String "🚀"
```

---

### Test 2.2: SAP Catalog Reading

```powershell
python -c "import json; data = json.load(open('sap-catalog.json', encoding='utf-8')); print(f'Loaded {len(data[\"saps\"])} SAPs')"
```

**Expected**:
- ✅ Catalog loads without errors
- ✅ Outputs: `Loaded 30 SAPs`

---

### Test 2.3: Event Log Writing (if SAP-010 adopted)

```powershell
# Check if A-MEM is present
if (Test-Path .chora\memory\events\development.jsonl) {
    python scripts/a-mem-query.py --query "test" --limit 5
}
```

**Expected**:
- ✅ Query runs without encoding errors
- ✅ Results display correctly

---

## Test Category 3: Path Handling

**Purpose**: Verify Windows paths work correctly

### Test 3.1: Absolute Windows Paths

```powershell
python scripts/create-capability-server.py --name "Path Test" --output C:\Users\Public\test-mcp --namespace pathtest
```

**Expected**:
- ✅ Accepts Windows absolute path
- ✅ Creates project in correct location

**Cleanup**:
```powershell
Remove-Item -Recurse -Force C:\Users\Public\test-mcp
```

---

### Test 3.2: User Profile Path

```powershell
python scripts/create-capability-server.py --name "Profile Test" --output $env:USERPROFILE\Desktop\test-mcp --namespace proftest
```

**Expected**:
- ✅ Resolves `%USERPROFILE%` correctly
- ✅ Creates project on Desktop

**Cleanup**:
```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\Desktop\test-mcp
```

---

## Test Category 4: Validation Tools

**Purpose**: Verify our Windows compatibility tools work

### Test 4.1: Validation Script

```powershell
python scripts/validate-windows-compat.py --scripts-only
```

**Expected**:
- ✅ Runs without errors
- ✅ Reports 0 critical issues (or only false positives in comments)

---

### Test 4.2: Fix Script (Dry Run)

```powershell
python scripts/fix-encoding-issues.py --dry-run --file scripts\test-mcp-template-render.py
```

**Expected**:
- ✅ Analyzes file
- ✅ Shows what would be fixed (or "No issues found")

---

## Test Category 5: Bash Scripts (if needed)

**Purpose**: Verify remaining bash scripts work with Git Bash

### Test 5.1: Git Bash Availability

```bash
# From Git Bash terminal:
bash --version
```

**Expected**:
- ✅ Git Bash installed (comes with Git for Windows)
- ✅ Version 4.x or higher

---

### Test 5.2: Propagate Trace ID (if using)

```bash
# From Git Bash:
bash scripts/propagate-trace-id.sh test-2025-001 docs/README.md
```

**Expected**:
- ✅ Script runs (or reports file format error if README doesn't have frontmatter)
- ✅ No bash syntax errors

---

## Test Category 6: Pre-Commit Hook

**Purpose**: Verify pre-commit hook prevents regressions

### Test 6.1: Hook Installation

```powershell
git config core.hooksPath .githooks
```

**Expected**:
- ✅ Command completes successfully

---

### Test 6.2: Hook Blocks Bash Scripts

```powershell
# Create dummy bash script
echo "#!/bin/bash" > scripts/test-new.sh
git add scripts/test-new.sh
git commit -m "test: should be blocked"
```

**Expected**:
- ❌ Commit blocked
- ✅ Error message explains bash scripts not allowed

**Cleanup**:
```powershell
git reset HEAD scripts/test-new.sh
del scripts\test-new.sh
```

---

## Test Category 7: Error Scenarios

**Purpose**: Verify errors display correctly on Windows

### Test 7.1: Intentional Error with Emoji

```powershell
python scripts/create-capability-server.py --name "Test" --output C:\nonexistent\path\project --namespace test
```

**Expected**:
- ✅ Error message displays (may include ❌ emoji)
- ✅ No `UnicodeEncodeError` crash
- ✅ Helpful error message about directory

---

### Test 7.2: Missing Dependency

```powershell
# Temporarily rename jinja2 (if you're brave!)
# python scripts/create-capability-server.py --help
```

**Expected**:
- ✅ Error message displays (includes ❌ emoji)
- ✅ Suggests installing jinja2
- ✅ No encoding crash

---

## Smoke Test Results Template

Copy this template for each test run:

```markdown
## Windows Test Run

**Date**: YYYY-MM-DD
**Windows Version**: Windows 10/11
**Python Version**: 3.x.x
**Tester**: Name

### Results

- [ ] Category 1: Emoji Output (4/4 tests pass)
- [ ] Category 2: File I/O Encoding (3/3 tests pass)
- [ ] Category 3: Path Handling (2/2 tests pass)
- [ ] Category 4: Validation Tools (2/2 tests pass)
- [ ] Category 5: Bash Scripts (2/2 tests pass or N/A)
- [ ] Category 6: Pre-Commit Hook (2/2 tests pass)
- [ ] Category 7: Error Scenarios (2/2 tests pass)

### Issues Found

(List any issues discovered during testing)

### Overall Status

- ✅ PASS / ❌ FAIL

```

---

## Automated Testing (Future)

**Planned for Phase 3**: GitHub Actions workflow running on Windows

```yaml
# .github/workflows/windows-test.yml (planned)
name: Windows Compatibility

on: [push, pull_request]

jobs:
  windows-test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/validate-windows-compat.py
      - run: python scripts/create-capability-server.py --help
      - run: python scripts/install-sap.py --list
```

---

## Troubleshooting

### Issue: Emojis Show as Question Marks

**Cause**: Windows console doesn't support Unicode emojis

**Solution**: This is expected. Emojis may render as `?` or boxes. The important thing is **no crashes**.

**Workaround**: Use Windows Terminal (supports emojis) instead of CMD

---

### Issue: `UnicodeEncodeError` Still Occurs

**Diagnosis**:
```powershell
python -c "import sys; print(sys.stdout.encoding)"
```

**If output is not `utf-8`**:
```powershell
# Set environment variable
$env:PYTHONIOENCODING = "utf-8"

# Or permanently in PowerShell profile:
Add-Content $PROFILE "`n`$env:PYTHONIOENCODING='utf-8'"
```

---

### Issue: `ModuleNotFoundError: jinja2`

**Solution**:
```powershell
pip install jinja2
# OR
pip install -r requirements.txt
```

---

### Issue: Git Bash Not Found

**Solution**:
1. Install Git for Windows: https://git-scm.com/download/win
2. Git Bash is included automatically
3. Access via: Right-click in folder → "Git Bash Here"

---

## CI/CD Integration

### GitHub Actions (when Windows runner added)

```yaml
- name: Windows Compatibility Check
  run: python scripts/validate-windows-compat.py --format json
```

### Local Pre-Commit

```bash
git config core.hooksPath .githooks
```

---

## Related Documentation

- [Windows Compatibility Summary](../../project-docs/windows-compatibility-summary.md)
- [Bash to Python Migration](../../user-docs/how-to/bash-to-python-migration.md)
- [Bash Scripts README](../../../scripts/BASH_SCRIPTS_README.md)

---

**Last Updated**: 2025-11-08
**Status**: v1.0.0 (Phase 1-2 complete)
**Next**: Add to GitHub Actions (Phase 3)
