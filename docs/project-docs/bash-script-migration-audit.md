# Bash Script Migration Audit

**Date**: 2025-11-03
**Status**: Complete
**Purpose**: Assess 6 bash scripts for Python migration (SAP-008 enhancement)

---

## Summary

**Total Scripts**: 6
**Complexity Range**: Simple → Very Complex
**Estimated Migration Time**: 20-30 hours total
**Recommended Priority Order**: Simplest → Complex (validate early, reduce risk)

---

## Script Analysis

### 1. validate-prerequisites.sh (PRIORITY 1 - SIMPLE)

**Purpose**: Pre-flight validation for chora-base onboarding
**Lines**: 349 lines
**Complexity**: ⭐⭐ (Simple-Medium)
**Dependencies**: Python 3, Git

**Key Functionality**:
- Validates Python 3.8+ installed
- Validates Git 2.0+ installed
- Checks directory structure (docs/, scripts/)
- Validates sap-catalog.json exists and is valid JSON
- Checks disk space (100MB+ recommended)
- Checks write permissions
- Validates install-sap.py script
- Checks optional PyYAML

**Cross-Platform Concerns**:
- ✅ Already uses Python for JSON validation
- ✅ Uses `command -v` (portable)
- ⚠️ Color output (ANSI escape codes) - needs terminal detection
- ⚠️ Disk space check uses `df` (different on macOS/Linux, N/A on Windows)
- ⚠️ Unicode symbols (✓✗⚠ℹ) - Will fail on Windows (same issue we fixed in platform-info.py)

**Migration Strategy**:
- **Pattern**: Similar to check-python-env.py (tool availability checks)
- **Time Estimate**: 2-3 hours
- **Key Changes**:
  - Use `shutil.which()` for tool checking
  - Use `psutil` or `shutil.disk_usage()` for disk space (cross-platform)
  - ASCII-compatible output (avoid Unicode symbols)
  - Color output via `colorama` (cross-platform) or ASCII fallback

**Python Advantages**:
- Better subprocess handling (Python `subprocess` vs bash `command -v`)
- Better JSON validation (already using Python!)
- Better error handling and reporting
- Windows-compatible disk space checking

---

### 2. rollback-migration.sh (PRIORITY 2 - SIMPLE)

**Purpose**: Rollback migration to angle brackets (restore from backups)
**Lines**: 29 lines
**Complexity**: ⭐ (Very Simple)
**Dependencies**: None (only uses `find`, `cp`)

**Key Functionality**:
- Finds all `.backup` files in `template/` directory
- Counts backup files
- Restores each backup file to original (removes `.backup` extension)
- Reports success/failure

**Cross-Platform Concerns**:
- ✅ `find` works everywhere (but syntax differs slightly)
- ✅ `cp` works everywhere
- ⚠️ Unicode emoji (🔄📦✅❌) - Will fail on Windows
- ⚠️ Uses `wc -l | tr -d ' '` for counting (not needed in Python)

**Migration Strategy**:
- **Pattern**: Use `pathlib.Path` for file operations
- **Time Estimate**: 1 hour
- **Key Changes**:
  - `Path.glob("**/*.backup")` instead of `find`
  - `shutil.copy()` for file copying
  - ASCII output (avoid Unicode)
  - Better error handling (per-file failures)

**Python Advantages**:
- Simpler code (`Path.glob()` vs `find` pipeline)
- Better error handling (try/except per file)
- Cross-platform file operations (pathlib)
- No Unicode issues

---

### 3. validate-links.sh (PRIORITY 3 - MEDIUM)

**Purpose**: MVP link validation for internal markdown links
**Lines**: 109 lines
**Complexity**: ⭐⭐⭐ (Medium)
**Dependencies**: Python 3 (for path normalization), grep

**Key Functionality**:
- Scans markdown files for internal links `[text](path)`
- Excludes external links (http, mailto, tel, javascript)
- Resolves relative paths (uses Python for `../` handling!)
- Validates link targets exist (file or directory)
- Reports broken links with details

**Cross-Platform Concerns**:
- ✅ Already uses Python 3 for path normalization!
- ⚠️ Uses `grep -oE` (regex) - complex bash pipeline
- ⚠️ Color output (ANSI codes)
- ⚠️ Uses `find ... -print0` and `while read -d ''` (bash-specific)
- ⚠️ Unicode emoji (❌✅) - Windows issue

**Migration Strategy**:
- **Pattern**: Pure Python regex and path validation
- **Time Estimate**: 2-3 hours
- **Key Changes**:
  - Use `re` module for link extraction
  - Use `pathlib.Path` for all path operations
  - Remove Python subprocess call (do it natively)
  - ASCII output
  - Iterate files with `Path.glob("**/*.md")`

**Python Advantages**:
- Already using Python for path resolution!
- Simpler regex with `re` module
- Better path handling (pathlib)
- No bash pipeline complexity
- Easier to test and maintain

---

### 4. check-sap-awareness-integration.sh (PRIORITY 4 - MEDIUM)

**Purpose**: Quick pattern detection for AGENTS.md/CLAUDE.md integration in SAP adoption blueprints
**Lines**: 152 lines
**Complexity**: ⭐⭐⭐ (Medium)
**Dependencies**: None (only uses `grep`)

**Key Functionality**:
- Checks if `adoption-blueprint.md` exists in SAP directory
- Validates 4 patterns using `grep`:
  1. Post-install section exists
  2. AGENTS.md mentioned
  3. Validation command present (grep check)
  4. Agent-executable instructions
- Reports pass/warning/fail counts
- Exit codes: 0 = pass, 1 = fail, 2 = invalid usage

**Cross-Platform Concerns**:
- ⚠️ Uses `grep -q`, `grep -i` (portable but different implementations)
- ⚠️ Color output (ANSI codes)
- ⚠️ Unicode emoji (✅❌⚠️ℹ️) - Windows issue
- ⚠️ Uses `((PASS_COUNT++))` bash arithmetic

**Migration Strategy**:
- **Pattern**: Simple file reading and pattern matching
- **Time Estimate**: 1-2 hours
- **Key Changes**:
  - Read file with `Path.read_text()`
  - Use `in` operator or `re.search()` for pattern matching
  - ASCII output
  - Simple counters (no bash arithmetic)

**Python Advantages**:
- Simpler pattern matching (`"AGENTS.md" in content`)
- Better error handling
- Easier to extend (more complex validation rules)
- Cross-platform by default

---

### 5. fix-shell-syntax.sh (PRIORITY 5 - COMPLEX)

**Purpose**: Fix shell syntax that was incorrectly converted by delimiter migration (Jinja2 → shell)
**Lines**: 35 lines
**Complexity**: ⭐⭐⭐⭐ (Complex)
**Dependencies**: sed (GNU sed with `-i ''` syntax)

**Key Functionality**:
- Fixes heredocs: `{{EOF` → `<<EOF`, `{{'EOF'` → `<<'EOF'`
- Fixes shell test expressions: `if {{ condition }}` → `if [[ condition ]]`
- Fixes while loops: `while {{ condition }}` → `while [[ condition ]]`
- Fixes array access: `arr{{i}}` → `arr[i]` (only in `.sh.jinja` files)
- Uses `find` + `sed -i` for in-place editing

**Cross-Platform Concerns**:
- ❌ Uses `sed -i ''` (macOS syntax) - doesn't work on Linux or Windows!
- ❌ GNU sed required - Windows doesn't have sed
- ⚠️ Uses `find` with `-exec`
- ⚠️ Regular expressions in sed (complex)

**Migration Strategy**:
- **Pattern**: Text processing with regex substitutions
- **Time Estimate**: 2-3 hours
- **Key Changes**:
  - Use `re.sub()` for regex replacements
  - Use `Path.read_text()` / `Path.write_text()` for in-place editing
  - Process files with `Path.glob("**/*.jinja")`
  - Test regex patterns carefully

**Python Advantages**:
- Cross-platform regex (`re` module)
- Safer in-place editing (read → transform → write)
- Easier to test regex patterns
- No sed portability issues

**Note**: This script is specific to Jinja2 template fixes - may not be needed long-term.

---

### 6. merge-upstream-structure.sh (PRIORITY 6 - VERY COMPLEX)

**Purpose**: Safely merge structural updates from chora-base upstream while preserving project content
**Lines**: 515 lines (!!)
**Complexity**: ⭐⭐⭐⭐⭐ (Very Complex)
**Dependencies**: Git, yq (YAML parser), bash

**Key Functionality**:
- Reads `.chorabase` YAML metadata
- Validates prerequisites (git repo, yq available)
- Checks/adds upstream remote
- Fetches from upstream
- Creates timestamped backup (commit hash + branch)
- Parses `structure_only` files from `.chorabase`
- Expands glob patterns using `git ls-tree`
- Merges files with `git checkout upstream/main -- file`
- Detects hybrid files (require manual merge)
- Runs validation commands from `.chorabase`
- Provides rollback instructions
- Supports `--dry-run` and `--no-backup` flags

**Cross-Platform Concerns**:
- ❌ Requires `yq` (YAML parser) - separate installation
- ⚠️ Git operations (subprocess intensive)
- ⚠️ Color output (ANSI codes)
- ⚠️ Unicode emoji (✓✗⚠ℹ🔄) - Windows issue
- ⚠️ Uses `eval` for validation commands (security concern)
- ⚠️ Complex bash string processing

**Migration Strategy**:
- **Pattern**: Git automation with YAML config parsing
- **Time Estimate**: 4-6 hours (!!)
- **Key Changes**:
  - Use `PyYAML` for `.chorabase` parsing (already available)
  - Use `subprocess` for git operations (explicit, testable)
  - Use `pathlib.Path` for file operations
  - ASCII output
  - Better error handling (try/except per operation)
  - Safer command execution (avoid `eval`, use `subprocess.run`)

**Python Advantages**:
- Native YAML parsing (`yaml.load()`)
- Better subprocess handling (`subprocess.run()` with capture_output)
- Safer command execution (no shell injection via `eval`)
- Better error reporting (exceptions with context)
- Easier to test (mock git operations)

**Note**: This is the most complex script - requires careful migration and extensive testing.

---

## Migration Priority Order (Recommended)

Based on complexity, dependencies, and risk:

| Priority | Script | Complexity | Time | Why This Order |
|----------|--------|------------|------|----------------|
| 1 | `validate-prerequisites.sh` | ⭐⭐ | 2-3h | Similar to existing `check-python-env.py`, validates migration patterns |
| 2 | `rollback-migration.sh` | ⭐ | 1h | Very simple, builds confidence, tests file operations |
| 3 | `validate-links.sh` | ⭐⭐⭐ | 2-3h | Already uses Python! Clean win, important for SAP-016 |
| 4 | `check-sap-awareness-integration.sh` | ⭐⭐⭐ | 1-2h | Simple pattern matching, validates SAP integration |
| 5 | `fix-shell-syntax.sh` | ⭐⭐⭐⭐ | 2-3h | Complex regex, template-specific, may deprecate |
| 6 | `merge-upstream-structure.sh` | ⭐⭐⭐⭐⭐ | 4-6h | Very complex, many dependencies, test thoroughly |

**Total Estimated Time**: 12-18 hours (conservative: 20-25 hours with testing)

---

## Cross-Platform Issues Summary

### Common Issues Across All Scripts

1. **Unicode Symbols** ✅❌⚠️ℹ️🔄
   - **Impact**: ALL scripts fail on Windows
   - **Fix**: Use ASCII alternatives `[OK]`, `[FAIL]`, `[WARN]`, `[INFO]`
   - **Pattern**: Already solved in `platform-info.py`

2. **ANSI Color Codes**
   - **Impact**: May not work on all terminals
   - **Fix**: Use `colorama` library (cross-platform) or detect terminal support
   - **Pattern**: Check `sys.stdout.isatty()` before coloring

3. **Bash-Specific Constructs**
   - `((VAR++))` arithmetic
   - `[[ condition ]]` tests
   - `while read -d ''` null-delimited input
   - **Fix**: Native Python equivalents

### Script-Specific Issues

| Script | Unique Issue | Fix |
|--------|--------------|-----|
| `validate-prerequisites.sh` | `df` disk space check | `shutil.disk_usage()` |
| `validate-links.sh` | Already uses Python! | Pure Python migration easy |
| `fix-shell-syntax.sh` | `sed -i ''` macOS-only | `re.sub()` + file I/O |
| `merge-upstream-structure.sh` | Requires `yq` (YAML) | `PyYAML` (pip install) |

---

## Dependencies Analysis

### Current Dependencies (Bash Scripts)

- **Python 3**: Used by 2/6 scripts (`validate-prerequisites.sh`, `validate-links.sh`)
- **Git**: Used by 1/6 scripts (`merge-upstream-structure.sh`)
- **yq**: Used by 1/6 scripts (`merge-upstream-structure.sh`) - **BLOCKER**
- **sed**: Used by 1/6 scripts (`fix-shell-syntax.sh`)
- **find, grep, cp**: Used by all (standard Unix tools)

### Python Migration Dependencies

- **Standard Library**: `pathlib`, `subprocess`, `shutil`, `re`, `sys`, `json`
- **Optional**: `colorama` (for colors), `PyYAML` (for `.chorabase` parsing)

**Advantage**: Fewer external dependencies (no `yq` needed!)

---

## Testing Strategy

### Per-Script Testing

1. **Unit Tests**: Test individual functions (validators, parsers)
2. **Integration Tests**: Test full script flow
3. **Cross-Platform Tests**: Run on Windows (primary goal!)
4. **Regression Tests**: Compare output to bash version

### Test Environments

- **Windows**: Primary target (where bash scripts fail)
- **macOS**: Validate no regression
- **Linux**: Validate no regression

### Test Data

- Use existing repository structure
- Create test fixtures for edge cases
- Mock git operations for `merge-upstream-structure.sh`

---

## Risk Assessment

### Low Risk (Priorities 1-4)

- **Scripts 1-4**: Simple logic, few dependencies
- **Mitigation**: Keep bash scripts as fallback during validation

### Medium Risk (Priority 5)

- **Script 5** (`fix-shell-syntax.sh`): Complex regex, template-specific
- **Mitigation**: Extensive regex testing, may deprecate if not needed

### High Risk (Priority 6)

- **Script 6** (`merge-upstream-structure.sh`): Very complex, 515 lines, git operations
- **Mitigation**:
  - Thorough testing with mock git repos
  - `--dry-run` mode validation
  - Extensive error handling
  - Keep bash version as fallback longer

---

## Success Criteria

### Per-Script Success

- ✅ Python script produces identical output to bash version
- ✅ Runs on Windows without errors
- ✅ No Unicode encoding issues
- ✅ No hardcoded path separators
- ✅ Proper error handling (try/except)
- ✅ Exit codes match bash version (0 = success, 1 = fail, 2 = usage error)

### Overall Success

- ✅ All 6 scripts migrated to Python
- ✅ All tested on Windows, macOS, Linux
- ✅ justfile updated to call Python scripts
- ✅ Bash scripts moved to `scripts/deprecated/`
- ✅ SAP-008 documentation updated (Python-first policy)
- ✅ Zero active bash scripts in production use

---

## Next Steps

1. **Start with Priority 1** (`validate-prerequisites.sh`)
   - Validates migration patterns
   - Similar to `check-python-env.py` (already works)
   - Builds confidence

2. **Iterate through priorities 2-4**
   - Quick wins (priorities 2-4 are 4-8 hours total)
   - Test on Windows after each migration
   - Update justfile incrementally

3. **Tackle Priority 5 & 6**
   - More complex, allocate extra time
   - Extensive testing required
   - Consider keeping bash fallbacks longer

4. **Update SAP-008**
   - Document Python-first policy
   - Add cross-platform guidance
   - Link to SAP-030 patterns

---

**Audit Completed**: 2025-11-03
**Ready for Migration**: ✅
**Recommended Start**: Priority 1 (`validate-prerequisites.sh`)
