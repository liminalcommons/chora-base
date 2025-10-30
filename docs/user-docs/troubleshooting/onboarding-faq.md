# Common Onboarding Issues FAQ

**Last Updated**: 2025-10-30
**Based on**: COORD-003 pilot adoption feedback and common support issues

This guide addresses the most frequent issues encountered during chora-base onboarding. If you're stuck, start here before opening an issue.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [SAP Set Selection](#sap-set-selection)
3. [Validation Issues](#validation-issues)
4. [File Location & Structure](#file-location--structure)
5. [Prerequisites & Dependencies](#prerequisites--dependencies)
6. [Permission Errors](#permission-errors)
7. [Platform-Specific Issues](#platform-specific-issues)

---

## Installation Issues

### Issue: Python version mismatch

**Symptoms**:
```
Error: Python 3.7 found (requires 3.8+)
```

**Solution**:
1. Check your Python version: `python3 --version`
2. Install Python 3.8+ from: https://www.python.org/downloads/
3. On macOS with Homebrew: `brew install python@3.12`
4. On Linux: `sudo apt install python3.12` (Ubuntu/Debian) or `sudo yum install python312` (RHEL/CentOS)
5. Verify: `python3 --version` should show 3.8 or higher

**Prevention**: Run `bash scripts/validate-prerequisites.sh` before installation

---

### Issue: Git not found

**Symptoms**:
```
bash: git: command not found
```
or
```
Error: Git not found in PATH
```

**Solution**:
1. Install Git from: https://git-scm.com/downloads
2. On macOS with Homebrew: `brew install git`
3. On Linux: `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (RHEL/CentOS)
4. On Windows: Download from git-scm.com or install Git Bash
5. Verify: `git --version` should show 2.0 or higher

**Prevention**: Run `bash scripts/validate-prerequisites.sh` before installation

---

### Issue: install-sap.py fails mid-installation

**Symptoms**:
- Installation stops partway through
- Error messages about missing files or directories
- "File not found" errors

**Solution**:
1. **Check you're in the chora-base root directory**:
   ```bash
   pwd  # Should show /path/to/chora-base
   ls   # Should show: docs/, scripts/, sap-catalog.json
   ```

2. **Verify prerequisitesusing pre-flight validator**:
   ```bash
   bash scripts/validate-prerequisites.sh
   ```

3. **Check for disk space** (needs 100MB+):
   ```bash
   df -h .
   ```

4. **Try dry-run first** to see what will happen:
   ```bash
   python3 scripts/install-sap.py --set minimal-entry --dry-run
   ```

5. **If still failing, check install-sap.py output** for specific errors

**Prevention**: Always run `validate-prerequisites.sh` before `install-sap.py`

---

### Issue: "Module not found" errors during installation

**Symptoms**:
```
ModuleNotFoundError: No module named 'yaml'
```

**Solution**:

For **PyYAML** (optional - only needed for custom .chorabase files):
```bash
pip install PyYAML
```

For **other missing modules**, the installation should work without them for standard SAP sets. If you see errors for required modules, your Python installation may be incomplete.

**Prevention**: PyYAML is optional. Standard SAP sets don't require it.

---

## SAP Set Selection

### Issue: Which SAP set should I choose?

**Quick Decision Tree**:

1. **First-time adopter or setting up new project?**
   - YES → Use `minimal-entry` (4 essential SAPs)
   - NO → Continue to question 2

2. **Do you need custom SAP configuration?**
   - YES → Use `comprehensive` (9 curated SAPs)
   - NO → Continue to question 3

3. **Do you want all SAPs for reference?**
   - YES → Use `full-adoption` (18 SAPs)
   - NO → Use `balanced` (6 SAPs)

**See also**: [docs/user-docs/reference/sap-set-decision-tree.md](../reference/sap-set-decision-tree.md) for visual flowchart

**Detailed Comparison**:

| SAP Set | SAP Count | Use Case | Time |
|---------|-----------|----------|------|
| **minimal-entry** | 4 | First-time adopters, quick start | ~5 min |
| **balanced** | 6 | Standard projects, typical workflows | ~8 min |
| **comprehensive** | 9 | Advanced features, customization | ~12 min |
| **full-adoption** | 18 | Complete reference, all capabilities | ~20 min |

**Still unsure?** Start with `minimal-entry`. You can always install additional SAPs later:
```bash
python3 scripts/install-sap.py SAP-005
```

---

### Issue: Can I change SAP set later?

**Answer**: Yes! SAP sets are not exclusive.

**Options**:

1. **Install additional SAPs individually**:
   ```bash
   python3 scripts/install-sap.py SAP-005
   ```

2. **Install a different SAP set** (additive, doesn't remove existing):
   ```bash
   python3 scripts/install-sap.py --set comprehensive
   ```

3. **See what's installed**:
   ```bash
   ls docs/skilled-awareness/ | grep SAP-
   ```

**Note**: Installing overlapping sets is safe - the installer skips already-installed SAPs.

---

### Issue: What's the difference between SAP-000 and SAP-001?

**Answer**:

- **SAP-000**: Protocol specification - defines what a SAP is and how SAPs work
- **SAP-001**: Inbox coordination protocol - specific implementation for cross-repo coordination

Think of it like:
- SAP-000 = "What is HTTP?"
- SAP-001 = "How to build a REST API"

**Recommendation**: Start with `minimal-entry` set which includes both foundational SAPs.

---

## Validation Issues

### Issue: How do I know installation succeeded?

**Quick Check**:
```bash
# Check if SAPs are installed
ls docs/skilled-awareness/ | grep SAP-

# Should see SAP directories like:
# SAP-000-protocol-specification/
# SAP-001-inbox-coordination/
# (etc.)
```

**Thorough Validation**:

1. **Count installed SAPs**:
   ```bash
   ls -d docs/skilled-awareness/SAP-* | wc -l
   ```
   - minimal-entry: 4 SAPs
   - balanced: 6 SAPs
   - comprehensive: 9 SAPs
   - full-adoption: 18 SAPs

2. **Check each SAP has required artifacts**:
   ```bash
   # Each SAP should have 5 files:
   # - BLUEPRINT.md
   # - INDEX.md
   # - AGENTS.md
   # - README.md
   # - SPECIFICATION.md

   ls docs/skilled-awareness/SAP-001-inbox-coordination/
   ```

3. **Verify with install-sap.py**:
   ```bash
   python3 scripts/install-sap.py --list
   ```

**See also**: Success criteria checklists in adoption blueprint files:
- [docs/skilled-awareness/adoption-blueprint-minimal-entry.md](../../skilled-awareness/adoption-blueprint-minimal-entry.md)

---

### Issue: SAP awareness check failed

**Symptoms**:
- Missing artifacts (expected 5, found fewer)
- File not found errors when accessing SAP documentation

**Solution**:

1. **Re-install the affected SAP**:
   ```bash
   python3 scripts/install-sap.py SAP-001 --force
   ```
   (Note: `--force` flag may not exist - check `install-sap.py --help`)

2. **Verify source sap-catalog.json**:
   ```bash
   python3 -m json.tool sap-catalog.json > /dev/null
   # No output = valid JSON
   ```

3. **Check file permissions**:
   ```bash
   ls -la docs/skilled-awareness/SAP-001-inbox-coordination/
   # All files should be readable
   ```

4. **Clean install** (remove and reinstall):
   ```bash
   rm -rf docs/skilled-awareness/SAP-001-inbox-coordination/
   python3 scripts/install-sap.py SAP-001
   ```

---

## File Location & Structure

### Issue: "No such file or directory" errors

**Common Causes**:

1. **Not running from chora-base root directory**:
   ```bash
   # Wrong:
   cd docs/
   python3 scripts/install-sap.py --set minimal-entry
   # Error: scripts/install-sap.py not found

   # Correct:
   cd /path/to/chora-base/  # Root directory
   python3 scripts/install-sap.py --set minimal-entry
   ```

2. **Incorrect paths in commands**:
   ```bash
   # Wrong:
   python3 install-sap.py --set minimal-entry

   # Correct:
   python3 scripts/install-sap.py --set minimal-entry
   ```

3. **Missing sap-catalog.json**:
   ```bash
   # Verify it exists:
   ls -la sap-catalog.json

   # If missing, you may not be in chora-base root
   ```

**Solution**: Always run commands from the chora-base root directory where `sap-catalog.json` exists.

---

### Issue: Where are SAPs installed?

**Answer**: `docs/skilled-awareness/SAP-XXX-name/`

**Full Structure**:
```
chora-base/
├── docs/
│   └── skilled-awareness/
│       ├── SAP-000-protocol-specification/
│       │   ├── BLUEPRINT.md
│       │   ├── INDEX.md
│       │   ├── AGENTS.md
│       │   ├── README.md
│       │   └── SPECIFICATION.md
│       ├── SAP-001-inbox-coordination/
│       │   └── (5 artifacts)
│       └── (etc.)
├── scripts/
│   ├── install-sap.py
│   └── validate-prerequisites.sh
└── sap-catalog.json
```

**To verify a specific SAP location**:
```bash
find docs/skilled-awareness -name "SAP-001*" -type d
```

---

## Prerequisites & Dependencies

### Issue: What do I need before starting?

**Minimum Requirements**:
- **Python 3.8+** (check: `python3 --version`)
- **Git 2.0+** (check: `git --version`)
- **100MB+ disk space** (check: `df -h .`)
- **Write permissions** to chora-base directory

**Optional**:
- **PyYAML** (only for custom .chorabase files): `pip install PyYAML`

**Quick Check**:
```bash
bash scripts/validate-prerequisites.sh
```

---

### Issue: Do I need Docker?

**Answer**: No, Docker is not required for basic SAP installation.

Docker is only needed for:
- **Advanced tier** infrastructure validation
- Running containerized tools/services (if you choose to)

For standard onboarding (essential/recommended tiers), Docker is optional.

---

### Issue: Do I need a git repository?

**Answer**: No, chora-base itself is a git repository, but your target project doesn't need to be.

**However**:
- If using SAP-001 (inbox coordination), git is required for the inbox protocol
- If you want version control for SAP documentation, git is recommended

**For evaluation/learning**: No git repository needed beyond cloning chora-base itself.

---

## Permission Errors

### Issue: "Permission denied" when installing

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied: 'docs/skilled-awareness/SAP-001-inbox-coordination'
```

**Solution**:

1. **Check directory ownership**:
   ```bash
   ls -la docs/skilled-awareness/
   # Should show your username as owner
   ```

2. **Fix permissions** if needed:
   ```bash
   chmod -R u+w docs/skilled-awareness/
   ```

3. **Don't use sudo** unless absolutely necessary:
   ```bash
   # Avoid:
   sudo python3 scripts/install-sap.py --set minimal-entry

   # This can create files owned by root, causing future issues
   ```

4. **If you accidentally used sudo**, fix ownership:
   ```bash
   sudo chown -R $USER:$USER docs/skilled-awareness/
   ```

---

### Issue: "Read-only file system"

**Symptoms**:
```
OSError: [Errno 30] Read-only file system
```

**Solution**:

1. **Check if you're on a read-only filesystem**:
   ```bash
   mount | grep "$(df . | tail -1 | awk '{print $1}')"
   ```

2. **Possible causes**:
   - Network drive mounted read-only
   - Docker volume with wrong permissions
   - System protection on certain directories

3. **Workaround**: Clone chora-base to a writeable location:
   ```bash
   cd ~/projects/  # Or another writeable directory
   git clone https://github.com/org/chora-base.git
   cd chora-base/
   python3 scripts/install-sap.py --set minimal-entry
   ```

---

## Platform-Specific Issues

### macOS: "Python not found" despite Python 3 installed

**Issue**: macOS may have Python 2.7 as `python`, but no `python3` command.

**Solution**:
1. Install Python 3 via Homebrew:
   ```bash
   brew install python@3.12
   ```

2. Or download from python.org: https://www.python.org/downloads/mac-osx/

3. Verify: `python3 --version`

---

### Windows: "bash: command not found"

**Issue**: Windows doesn't have bash by default.

**Solution**:

**Option 1: Git Bash** (recommended for chora-base):
1. Install Git for Windows: https://git-scm.com/download/win
2. Use "Git Bash" terminal (included with Git for Windows)
3. Run commands in Git Bash

**Option 2: WSL (Windows Subsystem for Linux)**:
1. Install WSL: https://docs.microsoft.com/en-us/windows/wsl/install
2. Use Ubuntu or another Linux distribution in WSL
3. Follow Linux instructions

**Option 3: PowerShell** (may need adapted commands):
- Replace `bash scripts/validate-prerequisites.sh` with PowerShell equivalents
- Or use `wsl bash scripts/validate-prerequisites.sh` if WSL is installed

---

### Linux: Python 3.8 not available in package manager

**Issue**: Older Linux distributions may only have Python 3.6 or 3.7.

**Solution**:

**Option 1: Use pyenv**:
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.12
pyenv install 3.12.0
pyenv global 3.12.0

# Verify
python3 --version
```

**Option 2: Build from source** (advanced):
```bash
# Install build dependencies
sudo apt install build-essential zlib1g-dev libssl-dev

# Download and build Python 3.12
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar -xf Python-3.12.0.tgz
cd Python-3.12.0/
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall  # Use altinstall to not override system python
```

**Option 3: Use a PPA** (Ubuntu):
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
```

---

## Still Having Issues?

### Before Opening an Issue:

1. **Run the pre-flight validator**:
   ```bash
   bash scripts/validate-prerequisites.sh
   ```

2. **Try a dry-run**:
   ```bash
   python3 scripts/install-sap.py --set minimal-entry --dry-run
   ```

3. **Check this FAQ** for your specific error message

4. **Search existing issues**: https://github.com/org/chora-base/issues

### Opening a New Issue:

Include:
- Output of `bash scripts/validate-prerequisites.sh`
- Output of `python3 --version` and `git --version`
- Operating system and version (e.g., macOS 14.0, Ubuntu 22.04)
- Full error message and stack trace
- What you were trying to do (which SAP set, which command)

---

## Quick Reference

### Essential Commands

```bash
# Pre-flight check (run first!)
bash scripts/validate-prerequisites.sh

# List available SAP sets
python3 scripts/install-sap.py --list-sets

# Install a SAP set (dry-run first)
python3 scripts/install-sap.py --set minimal-entry --dry-run
python3 scripts/install-sap.py --set minimal-entry

# Verify installation
ls docs/skilled-awareness/ | grep SAP-

# Install individual SAP
python3 scripts/install-sap.py SAP-001
```

### Common Fixes

```bash
# Fix permissions
chmod -R u+w docs/skilled-awareness/

# Check you're in root directory
pwd  # Should be chora-base/
ls sap-catalog.json  # Should exist

# Verify disk space
df -h .

# Reinstall a SAP
rm -rf docs/skilled-awareness/SAP-001-inbox-coordination/
python3 scripts/install-sap.py SAP-001
```

---

**Helpful Resources**:
- [SAP Set Decision Tree](../reference/sap-set-decision-tree.md) - Visual guide for choosing SAP sets
- [Installation Guide](../installation-guide.md) - Step-by-step onboarding
- [SAP Index](../../skilled-awareness/INDEX.md) - Complete SAP catalog
- [Adoption Blueprints](../../skilled-awareness/adoption-blueprint-minimal-entry.md) - Success criteria per tier

---

**Contributing to this FAQ**: If you encountered an issue not covered here, please open an issue or pull request to help future adopters!
