# Bash Scripts Status

## Overview

This directory contains automation scripts for chora-base. As part of our cross-platform support (Windows, Mac, Linux), we are migrating from bash scripts to Python equivalents.

## Migration Status

### ✅ Migrated to Python (bash versions deprecated)

The following bash scripts have been fully replaced with Python equivalents and moved to `scripts/deprecated/`:

- `check-sap-awareness-integration.sh` → `check-sap-awareness-integration.py`
- `fix-shell-syntax.sh` → `fix-shell-syntax.py`
- `merge-upstream-structure.sh` → `merge-upstream-structure.py`
- `rollback-migration.sh` → `rollback-migration.py`
- `validate-links.sh` → `validate-links.py`
- `validate-prerequisites.sh` → `validate-prerequisites.py`

**Action**: Use the Python versions (`.py`) instead of the bash versions (`.sh`).

---

### ⚠️ Bash Scripts Requiring WSL/Git Bash on Windows

The following bash scripts are still active and require a bash environment:

#### `propagate-trace-id.sh`

**Purpose**: Propagate CHORA_TRACE_ID from coordination request to documentation frontmatter

**Usage**:
```bash
./scripts/propagate-trace-id.sh <trace_id> <doc_file>
```

**Example**:
```bash
./scripts/propagate-trace-id.sh mcp-taskmgr-2025-003 docs/user-docs/how-to/create-task.md
```

**Windows Requirement**: Requires WSL (Windows Subsystem for Linux) or Git Bash

**Python Migration**: Planned for Phase 2 (see [cross-platform-next-scope.md](../docs/project-docs/cross-platform-next-scope.md))

---

#### `generate-doc-from-coordination.sh`

**Purpose**: Auto-generate documentation skeleton from SAP-001 coordination requests

**Usage**:
```bash
./scripts/generate-doc-from-coordination.sh <coordination_file> <output_doc>
```

**Example**:
```bash
./scripts/generate-doc-from-coordination.sh inbox/incoming/coordination/COORD-2025-042.json docs/user-docs/how-to/create-task.md
```

**Windows Requirement**: Requires WSL or Git Bash + `jq` utility

**Python Migration**: Planned for Phase 2 (see [cross-platform-next-scope.md](../docs/project-docs/cross-platform-next-scope.md))

---

## Windows Users: Setup Instructions

If you need to run the remaining bash scripts on Windows:

### Option 1: Git Bash (Recommended)

1. Install Git for Windows: https://git-scm.com/download/win
2. Git Bash is included automatically
3. For `generate-doc-from-coordination.sh`, install `jq`:
   ```bash
   # Download jq for Windows from: https://jqlang.github.io/jq/download/
   # Add jq.exe to your PATH
   ```

### Option 2: Windows Subsystem for Linux (WSL)

1. Install WSL:
   ```powershell
   wsl --install
   ```
2. Install `jq` inside WSL:
   ```bash
   sudo apt-get update && sudo apt-get install -y jq
   ```
3. Run scripts from WSL terminal

---

## Development Policy

**New scripts MUST be Python**:
- All new automation scripts must be written in Python 3.8+
- Use the UTF-8 encoding pattern (see existing scripts like `create-model-mcp-server.py`)
- Follow cross-platform best practices (see [SAP-030: cross-platform-fundamentals](../docs/skilled-awareness/cross-platform-fundamentals/))

**Pre-commit hook**: A pre-commit hook will be added to prevent new bash scripts from being committed.

---

## Related Documentation

- [Cross-Platform Fundamentals (SAP-030)](../docs/skilled-awareness/cross-platform-fundamentals/)
- [Bash to Python Migration Guide](../docs/user-docs/how-to/bash-to-python-migration.md)
- [Cross-Platform Next Steps](../docs/project-docs/cross-platform-next-scope.md)

---

**Last Updated**: 2025-11-08
**Migration Progress**: 75% complete (6 of 8 scripts migrated)
