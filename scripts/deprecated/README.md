# Deprecated Bash Scripts

**Status**: Deprecated as of v4.3.0 (2025-11-03)
**Removal**: Planned for v5.0.0
**Reason**: Migrated to Python for cross-platform support (Windows, macOS, Linux)

---

## Migration Context

These 6 bash scripts were migrated to Python following the bash-script-migration-audit completed in November 2025. The migration was driven by:

1. **Windows compatibility**: Historical pain from chora-compose Windows→Mac migration
2. **Cross-platform development**: Enable Windows developers to contribute immediately
3. **Better error handling**: Python provides superior error messages and exception handling
4. **Reduced dependencies**: No need for platform-specific tools (sed, yq, find)

**Migration Documentation**: [bash-to-python-migration.md](../../docs/user-docs/how-to/bash-to-python-migration.md)

---

## Python Equivalents

| Deprecated Bash Script | Python Equivalent | Purpose |
|------------------------|-------------------|---------|
| validate-prerequisites.sh | validate-prerequisites.py | Pre-flight validation (Python version, Git, disk space, SAP catalog) |
| rollback-migration.sh | rollback-migration.py | Restore `.backup` files to original filenames |
| validate-links.sh | validate-links.py | Internal markdown link validation |
| check-sap-awareness-integration.sh | check-sap-awareness-integration.py | SAP adoption blueprint validation (AGENTS.md integration) |
| fix-shell-syntax.sh | fix-shell-syntax.py | Fix Jinja2 template shell syntax (heredocs, test expressions) |
| merge-upstream-structure.sh | merge-upstream-structure.py | Merge structural updates from chora-base upstream (Git + YAML) |

**Location**: All Python scripts are in `scripts/` directory (parent of this deprecated folder)

**Usage**: Replace `bash scripts/<script>.sh` with `python scripts/<script>.py` or use `just <task>` recipes

---

## Justfile Recipes (Recommended)

Instead of calling scripts directly, use the justfile interface:

```bash
# Validate prerequisites
just validate-prerequisites

# Validate markdown links
just validate-links docs/

# Check SAP awareness integration
just check-sap-awareness docs/skilled-awareness/testing-framework

# Rollback migration
just rollback-migration

# Fix shell syntax in templates
just fix-shell-syntax

# Merge upstream structural updates
just merge-upstream
just merge-upstream-dry-run  # Preview first
```

---

## Migration Timeline

- **v4.3.0** (2025-11-03): Bash scripts deprecated, moved to `scripts/deprecated/`
- **v4.4.0 - v4.x.x**: Deprecation warnings in place, Python versions stable
- **v5.0.0** (TBD): Remove bash scripts entirely from repository

---

## Why These Scripts Were Kept

These bash scripts are kept temporarily for:

1. **Backwards compatibility**: Projects using old onboarding guides
2. **Reference**: Comparison with Python versions during adoption
3. **Migration guide examples**: Real-world before/after comparison

**Do NOT use these scripts in new workflows** - use the Python equivalents.

---

## Cross-Platform Issues (Why We Migrated)

All 6 bash scripts had cross-platform compatibility issues:

### Common Issues
- **Unicode symbols** (✓✗⚠ℹ🔄): Fail on Windows console with `UnicodeEncodeError`
- **ANSI color codes**: Terminal-dependent, inconsistent rendering
- **Bash-specific constructs**: `((VAR++))`, `[[condition]]`, `while read -d` don't work outside bash

### Script-Specific Issues

**validate-prerequisites.sh**:
- ❌ `df` disk space check (no `df` on Windows)
- ✅ Fixed with `shutil.disk_usage()` in Python

**rollback-migration.sh**:
- ❌ `find ... -print0 | while read -d ''` (bash-specific)
- ✅ Fixed with `Path.glob("**/*.backup")` in Python

**validate-links.sh**:
- ❌ Already called Python for path normalization!
- ✅ Pure Python now (no bash subprocess)

**check-sap-awareness-integration.sh**:
- ❌ `grep -q`, `grep -i` (different implementations)
- ✅ Fixed with `re.search()` in Python

**fix-shell-syntax.sh**:
- ❌ `sed -i ''` (macOS-only syntax, fails on Linux)
- ✅ Fixed with `re.sub()` + file I/O in Python

**merge-upstream-structure.sh**:
- ❌ Requires `yq` (YAML parser, separate installation)
- ✅ Fixed with `import yaml` (PyYAML) in Python

---

## For Maintainers

### Removing a Deprecated Script

When a script has been deprecated for 2+ minor versions:

1. Verify no active documentation references it
2. Check justfile doesn't call bash version
3. Search codebase: `grep -r "<script-name>.sh" docs/`
4. Delete bash script from `scripts/deprecated/`
5. Update this README

### Adding a New Deprecated Script

If deprecating a new bash script:

1. Migrate to Python following [migration guide](../../docs/user-docs/how-to/bash-to-python-migration.md)
2. Move bash version to `scripts/deprecated/`
3. Add entry to table above
4. Add deprecation warning header (see Phase 2.3)
5. Update justfile to call Python version

---

## Related Resources

**Documentation**:
- [Bash to Python Migration Guide](../../docs/user-docs/how-to/bash-to-python-migration.md) - Complete migration workflow
- [bash-script-migration-audit.md](../../docs/project-docs/bash-script-migration-audit.md) - Technical audit (v4.3.0)
- [cross-platform-sap-suite-plan.md](../../docs/project-docs/cross-platform-sap-suite-plan.md) - Strategic plan

**SAPs**:
- [SAP-030: Cross-Platform Fundamentals](../../docs/skilled-awareness/cross-platform-fundamentals/awareness-guide.md)
- [SAP-031: Python Environments](../../docs/skilled-awareness/cross-platform-python-environments/awareness-guide.md)
- [SAP-032: CI/CD Quality Gates](../../docs/skilled-awareness/cross-platform-ci-cd-quality-gates/awareness-guide.md)
- [SAP-008: Automation Scripts](../../docs/skilled-awareness/automation-scripts/protocol-spec.md#23-cross-platform-support)

---

**Last Updated**: 2025-11-03
**Status**: Active deprecation (v4.3.0)
**Contact**: See [AGENTS.md](../../AGENTS.md) for maintainer information
