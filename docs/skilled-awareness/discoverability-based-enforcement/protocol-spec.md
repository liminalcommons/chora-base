# Protocol Specification: Discoverability-Based Enforcement

**SAP ID**: SAP-031
**Version**: 1.0.0
**Status**: pilot
**Last Updated**: 2025-11-08

---

## 1. Overview

Discoverability-Based Enforcement provides a multi-layer architecture for ensuring patterns and best practices are consistently followed through strategic placement at decision points, combined with automated validation and educational feedback.

### Key Capabilities

- 5-layer enforcement architecture (discoverability, pre-commit, CI/CD, documentation, review)
- Integration with SAP-009 (agent-awareness) for strategic pattern placement
- Progressive enforcement strategy (warn → educate → block)
- Self-service validation and fix tools
- Template-driven development (production-ready starting points)
- Educational error messages (explain why + how to fix)
- Prevention rate measurement (target: 90%+)
- Domain-agnostic framework (applicable to security, performance, accessibility, testing, etc.)

---

## 2. Core Contracts

### Contract 1: 5-Layer Enforcement Architecture

**Description**: Defines the complete enforcement stack from discoverability to validation

**Architecture**:

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

**Requirements**:
- Each layer must provide value independently
- Layers must integrate seamlessly (no gaps)
- Prevention rate must be measurable per layer
- Performance must not block workflow (<10 sec for pre-commit)

---

### Contract 2: Discoverability Layer (SAP-009 Integration)

**Description**: Strategic pattern placement using nested awareness hierarchy

**Interface**:

```markdown
# Root AGENTS.md
## 🔴 [QUALITY DOMAIN] REMINDER

**ALL code MUST [quality requirement without modification].**

Before [activity], read: **[domain AGENTS.md path]** for [quality domain] patterns.

**Quick Template**: Copy [template file path]
```

**Requirements**:
- Root AGENTS.md includes prominent reminder (visual attention: emoji, bold, H2)
- Reminder links to domain AGENTS.md (1 click navigation)
- Domain AGENTS.md includes 5 core patterns (max 200 lines for quick reference)
- Template file exists with patterns pre-implemented (production-ready)
- Template discovery time ≤30 seconds from session start

**Integration with SAP-009**:
```
Session Start → Root AGENTS.md (reminder)
              ↓
Task Start → Domain AGENTS.md (patterns + template link)
           ↓
Implementation → Template file (copy + customize)
```

---

### Contract 3: Pre-Commit Validation Hook

**Description**: Automated validation with educational feedback before commit

**Interface** (Python hook):

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

import sys
from pathlib import Path

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def get_staged_files():
    """Get list of staged files"""
    # Implementation
    pass

def validate_pattern_1(file_path: Path) -> list[str]:
    """Validate Pattern 1"""
    # Return list of error messages
    pass

def main():
    """Main pre-commit hook logic"""
    print("🔍 Running [Quality Domain] validation...")

    staged_files = get_staged_files()
    issues = []

    for file_path in staged_files:
        issues.extend(validate_pattern_1(file_path))

    if issues:
        print("❌ ERROR: [Quality Domain] issues found!\n")
        for issue in issues:
            print(f"  {issue}")
        print("\nRequired action:")
        print("  1. Run: python scripts/fix-[domain]-issues.py --apply")
        print("  2. Review changes and re-stage files")
        print("  3. Try commit again\n")
        print("To bypass (not recommended): git commit --no-verify")
        return 1

    print("✅ All [Quality Domain] checks passed")
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

**Requirements**:
- Hook performance <10 seconds (avoid blocking)
- Educational error messages (explain why + how to fix)
- Self-service fix tool reference (one-command remediation)
- Escape hatch documentation (--no-verify usage)
- Cross-platform compatibility (Windows/Mac/Linux)

---

### Contract 4: CI/CD Validation Workflow

**Description**: Automated testing on target platforms/environments

**Interface** (GitHub Actions):

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
      fail-fast: false  # Continue testing other platforms if one fails
      matrix:
        platform: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up environment
        run: |
          # Setup steps (Python, Node.js, etc.)

      - name: Run [Quality Domain] validation
        run: |
          python scripts/validate-[domain].py

      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report-${{ matrix.platform }}
          path: validation-report.md
          retention-days: 30
```

**Requirements**:
- Matrix testing on all target platforms/environments
- Validation reports uploaded as artifacts (audit trail)
- Status badge in README (visibility)
- Fail-fast: false (continue testing other platforms if one fails)
- Run on push + PR + manual trigger

---

### Contract 5: Template File Structure

**Description**: Production-ready starting point with patterns pre-implemented

**Interface** (Python script template):

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
# Implementation
# Example: UTF-8 console reconfiguration
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# [QUALITY DOMAIN] Pattern 2: [Description]
# Implementation
# Example: File I/O with encoding
from pathlib import Path

def load_config(config_path: Path) -> dict:
    """Load configuration with UTF-8 encoding"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# [QUALITY DOMAIN] Pattern 3: [Description]
# Implementation
# Example: Path handling with pathlib
def main():
    """Main entry point"""
    config_path = Path.home() / ".config" / "app" / "config.json"
    config = load_config(config_path)
    # ... rest of implementation

if __name__ == '__main__':
    main()
```

**Requirements**:
- Template file location in `templates/[domain]/[template-name].[ext]`
- Patterns commented with explanations
- Production-ready (not placeholder code)
- Copy-paste friendly (minimal customization required)
- Cross-platform by default (no platform-specific code unless necessary)

---

### Contract 6: Self-Service Fix Tool

**Description**: Automated remediation for common violations

**Interface**:

```python
#!/usr/bin/env python3
"""Fix [Quality Domain] issues automatically

This script automatically fixes common [quality domain] violations:
- [Pattern 1 fix]
- [Pattern 2 fix]
- [Pattern 3 fix]

Usage:
    # Dry-run (show what would be fixed)
    python scripts/fix-[domain]-issues.py

    # Apply fixes
    python scripts/fix-[domain]-issues.py --apply

    # Fix specific file
    python scripts/fix-[domain]-issues.py --file path/to/file.py --apply
"""

import argparse
from pathlib import Path
import sys

def fix_pattern_1(file_path: Path, dry_run: bool = True) -> list[str]:
    """Fix Pattern 1 violations

    Returns:
        List of changes made (or would be made if dry_run=False)
    """
    changes = []

    if dry_run:
        # Report what would be fixed
        pass
    else:
        # Apply fixes
        pass

    return changes

def main():
    parser = argparse.ArgumentParser(description="Fix [Quality Domain] issues")
    parser.add_argument('--apply', action='store_true', help='Apply fixes (default: dry-run)')
    parser.add_argument('--file', type=Path, help='Fix specific file')
    args = parser.parse_args()

    # ... implementation

    if args.apply:
        print("✅ Fixes applied")
    else:
        print("ℹ️  Dry-run complete. Use --apply to make changes")

if __name__ == '__main__':
    main()
```

**Requirements**:
- Dry-run mode by default (safe exploration)
- --apply flag for execution (explicit confirmation)
- --file flag for targeted fixes
- Clear reporting (what was fixed)
- Idempotent (safe to run multiple times)

---

## 3. Integration Patterns

### Dependencies Integration

#### Integration with SAP-009 (agent-awareness)

**Integration Point**: Nested awareness hierarchy provides foundation for discoverability layer

**Configuration**:

```markdown
# Root AGENTS.md (created by SAP-009)
## Navigation Tree
- Domain 1: [docs/[domain]/AGENTS.md]
- Domain 2: [scripts/AGENTS.md]  ← Add enforcement reminder here

# Domain AGENTS.md (created by SAP-009)
## [Quality Domain] Patterns  ← Add enforcement patterns section

### Pattern 1: [Name]
**Description**: [What this pattern enforces]

**Example**:
```[language]
[Code example]
```

**Template**: [path/to/template]
```

**Enforcement Workflow**:
1. Agent starts session → reads root AGENTS.md (SAP-009)
2. Sees enforcement reminder → navigates to domain AGENTS.md
3. Reads patterns → copies template → implements with patterns
4. Pre-commit hook validates → CI/CD validates → review checklist confirms

---

#### Integration with SAP-006 (quality-gates)

**Integration Point**: Pre-commit hook framework

**Configuration**:

```yaml
# .pre-commit-config.yaml (created by SAP-006)
repos:
  - repo: local
    hooks:
      - id: [quality-domain]-validation
        name: [Quality Domain] Validation
        entry: .githooks/pre-commit-[quality-domain]
        language: python
        pass_filenames: false
        always_run: true
```

**Enforcement Workflow**:
1. SAP-006 installs pre-commit framework
2. SAP-031 adds domain-specific hook (.githooks/pre-commit-[quality-domain])
3. Developer commits → pre-commit runs all hooks → blocks if validation fails

---

#### Integration with SAP-005 (ci-cd-workflows)

**Integration Point**: CI/CD automation framework

**Configuration**:

```yaml
# .github/workflows/[quality-domain]-validation.yml (created by SAP-031)
# Uses patterns from SAP-005 (matrix testing, artifact upload, status badges)

name: [Quality Domain] Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    # ... (see Contract 4 for complete workflow)
```

**Enforcement Workflow**:
1. SAP-005 provides CI/CD framework (GitHub Actions setup)
2. SAP-031 adds domain-specific validation workflow
3. Push/PR triggers → validation runs → uploads report → updates badge

---

### External Integrations

**Integration 1**: GitHub Actions

- **Purpose**: Automated validation on push/PR
- **Configuration**: Place workflow in `.github/workflows/[quality-domain]-validation.yml`
- **Requirements**: GitHub repository with Actions enabled

**Integration 2**: Pre-commit Framework (optional)

- **Purpose**: Unified hook management across multiple hooks
- **Configuration**: Install via `pip install pre-commit`, configure `.pre-commit-config.yaml`
- **Requirements**: Python 3.8+

**Integration 3**: VS Code / IDE Extensions

- **Purpose**: Real-time pattern validation during editing
- **Configuration**: Recommend extensions in `.vscode/extensions.json`
- **Requirements**: IDE with extension support

---

## 4. Configuration

### Configuration Schema

```yaml
# .chora/enforcement.yaml
enforcement:
  enabled: true  # Enable enforcement framework

  # Layer 1: Discoverability
  discoverability:
    root_agents_reminder: true  # Add reminder to root AGENTS.md
    domain_agents_patterns: true  # Add patterns to domain AGENTS.md
    templates_enabled: true  # Provide template files

  # Layer 2: Pre-Commit
  pre_commit:
    enabled: true  # Enable pre-commit hooks
    performance_target_seconds: 10  # Max hook execution time
    educational_messages: true  # Include explanations in errors
    self_service_fixes: true  # Provide fix tools

  # Layer 3: CI/CD
  ci_cd:
    enabled: true  # Enable CI/CD validation
    platforms:  # Target platforms for matrix testing
      - ubuntu-latest
      - macos-latest
      - windows-latest
    artifact_upload: true  # Upload validation reports
    badge_enabled: true  # Show status badge in README

  # Layer 4: Documentation
  documentation:
    contributing_md: true  # Update CONTRIBUTING.md
    pr_template: true  # Add PR template with checklist
    testing_procedures: true  # Document testing requirements

  # Layer 5: Review
  review:
    human_verification: true  # Require human review
    domain_expertise: false  # Require domain expert review (optional)

  # Quality Domains (configure per domain)
  domains:
    cross_platform:
      enabled: true
      severity: critical  # block | warn | info
      patterns:
        - utf8_console_reconfiguration
        - file_io_encoding
        - pathlib_usage

    security:
      enabled: false  # Example: not yet configured
      severity: critical
      patterns: []
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENFORCEMENT_ENABLED` | No | `true` | Enable/disable entire enforcement framework |
| `ENFORCEMENT_PRE_COMMIT_TIMEOUT` | No | `10` | Pre-commit hook timeout (seconds) |
| `ENFORCEMENT_CI_PLATFORMS` | No | `ubuntu,macos,windows` | Comma-separated platform list |
| `ENFORCEMENT_SEVERITY_[DOMAIN]` | No | `critical` | Severity level per domain (critical/warn/info) |

---

## 5. Error Handling

### Error Codes

| Code | Error | Cause | Resolution |
|------|-------|-------|------------|
| `SAP-031-001` | Pre-commit hook timeout | Hook execution >10 seconds | Optimize validation logic, reduce file set |
| `SAP-031-002` | Missing template file | Template referenced but not found | Create template or update AGENTS.md link |
| `SAP-031-003` | CI/CD validation failure | Platform-specific issue | Review validation report artifact |
| `SAP-031-004` | Invalid enforcement config | Malformed .chora/enforcement.yaml | Validate YAML syntax, check schema |
| `SAP-031-005` | Self-service fix failure | Fix tool unable to remediate | Manual intervention required, file issue |

### Common Errors

**Error: Pre-commit hook blocking legitimate code**

- **Cause**: Validation rule has false positives (e.g., pattern matches non-violation)
- **Solution**:
  1. Review error message for context
  2. If legitimate use case, bypass with `git commit --no-verify` and document reason in commit message
  3. File issue to refine validation rule (reduce false positives)

**Error: CI/CD validation passing locally but failing in CI**

- **Cause**: Platform-specific behavior (e.g., Windows vs Linux file paths)
- **Solution**:
  1. Download validation report artifact from failed CI run
  2. Reproduce locally on target platform (or use Docker container)
  3. Fix platform-specific issue using SAP-030 patterns

**Error: Template file out of sync with patterns**

- **Cause**: Patterns updated in AGENTS.md but template not updated
- **Solution**:
  1. Diff AGENTS.md patterns vs template file
  2. Update template to match current patterns
  3. Version template with SAP version (e.g., template-v1.1.0)

---

## 6. Security Considerations

### Escape Hatch Protection

**Risk**: --no-verify bypass allows circumventing enforcement

**Mitigation**:
- CI/CD validation as second line of defense (can't bypass)
- PR template checklist requires reviewer verification
- Audit trail via git log (commits with --no-verify visible)
- Policy: --no-verify requires explanation in commit message

### Hook Tampering

**Risk**: Malicious or accidental modification of pre-commit hooks

**Mitigation**:
- Hooks stored in .githooks/ (version-controlled)
- Git config points to .githooks/ (not .git/hooks/ which is gitignored)
- CI/CD validates hooks match repository version
- Quarterly hook integrity review

### False Sense of Security

**Risk**: Enforcement catches known patterns but misses novel violations

**Mitigation**:
- Layer 5 (human review) as final safety net
- 90%+ target (not 100%) acknowledges limits
- Continuous rule refinement based on false negatives
- Domain expertise review for critical code paths

---

## 7. Performance Requirements

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pre-Commit Hook Execution | < 10 sec | Time from git commit to hook completion |
| Pattern Discovery Time | < 30 sec | Time from session start to finding pattern |
| CI/CD Validation Time | < 5 min | Time for single platform validation |
| Self-Service Fix Time | < 30 sec | Time to run fix tool (dry-run + apply) |
| Template Copy Time | < 10 sec | Time to locate and copy template |

### Performance Optimization

**Pre-Commit Hooks**:
- Run only on staged files (not entire repository)
- Use compiled regex patterns (cache)
- Parallel validation for independent checks
- Early exit on first critical error (fail-fast)

**CI/CD Validation**:
- Matrix strategy with fail-fast: false (parallel platforms)
- Cache dependencies (Python packages, Node modules)
- Incremental validation (only changed files if possible)
- Artifact upload conditional (if: always() to capture failures)

---

## 8. Examples

### Example 1: Cross-Platform Enforcement (Reference Implementation)

**Scenario**: Enforce Windows/Mac/Linux compatibility for Python scripts

**Layer 1 (Discoverability)**:

```markdown
# Root AGENTS.md
## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST work on Windows, Mac, and Linux without modification.**

Before writing Python scripts, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)
```

```markdown
# scripts/AGENTS.md
## Cross-Platform Patterns

### Pattern 1: UTF-8 Console Output
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

### Pattern 2: File I/O Encoding
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

### Pattern 3: Path Handling
from pathlib import Path
path = Path(base_dir) / "subdir" / "file.txt"

**Template**: [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)
```

**Layer 2 (Pre-Commit)**:

```python
# .githooks/pre-commit-cross-platform
def check_emoji_without_utf8(file_path: Path) -> list[str]:
    """Check if Python file uses emojis without UTF-8 reconfiguration"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_emoji = bool(re.search(r'[^\x00-\x7F]', content))  # Non-ASCII
    has_reconfigure = 'sys.stdout.reconfigure(encoding=' in content

    if has_emoji and not has_reconfigure:
        return [f"{file_path}: Uses emojis but missing UTF-8 reconfiguration"]

    return []
```

**Layer 3 (CI/CD)**:

```yaml
# .github/workflows/cross-platform-test.yml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: ['3.8', '3.11']

steps:
  - name: Run cross-platform validation
    run: python scripts/validate-windows-compat.py
```

**Expected Output**:

```
✅ Prevention Rate: 99%+ (0 critical issues after enforcement)
✅ Pattern Discovery: <30 sec (scripts/AGENTS.md)
✅ Fix Time: 1-command (python scripts/fix-encoding-issues.py --apply)
```

---

### Example 2: Security Enforcement (SQL Injection Prevention)

**Scenario**: Prevent SQL injection via parameterized queries

**Layer 1 (Discoverability)**:

```markdown
# Root AGENTS.md
## 🔴 SECURITY REMINDER

**ALL database queries MUST use parameterized queries (no string concatenation).**

Before writing database code, read: **[src/database/AGENTS.md](src/database/AGENTS.md)** for security patterns.

**Quick Template**: Copy [templates/security/database-query-template.py](templates/security/database-query-template.py)
```

**Layer 2 (Pre-Commit)**:

```python
def check_sql_injection_risk(file_path: Path) -> list[str]:
    """Check for SQL injection vulnerabilities"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detect string concatenation in SQL queries
    dangerous_patterns = [
        r'execute\([\'"].*?\{.*?\}.*?[\'"]\)',  # f-string in execute()
        r'execute\([\'"].*?\+.*?[\'"]\)',  # String concatenation in execute()
    ]

    issues = []
    for pattern in dangerous_patterns:
        if re.search(pattern, content):
            issues.append(f"{file_path}: Potential SQL injection (use parameterized queries)")

    return issues
```

**Expected Output**:

```
❌ ERROR: Security issues found!

  src/database/users.py: Potential SQL injection (use parameterized queries)

Required action:
  1. Replace: cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
  2. With: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
  3. See: templates/security/database-query-template.py
```

---

## 9. Validation & Testing

### Validation Commands

```bash
# Validate enforcement framework is correctly configured
python scripts/validate-enforcement.py

# Validate specific quality domain
python scripts/validate-enforcement.py --domain cross-platform

# Validate pre-commit hooks
git commit --dry-run  # Should trigger hooks without committing

# Validate CI/CD workflows
gh workflow run cross-platform-test.yml --ref main
```

### Test Cases

**Test Case 1**: Discoverability Layer

- **Given**: New Claude Code session starts
- **When**: Agent reads root AGENTS.md
- **Then**:
  - Agent sees enforcement reminder (e.g., "🔴 CROSS-PLATFORM REMINDER")
  - Agent navigates to domain AGENTS.md in <30 seconds
  - Agent finds patterns with template link

**Test Case 2**: Pre-Commit Hook Validation

- **Given**: Python script with emoji but no UTF-8 reconfiguration
- **When**: Developer runs `git commit`
- **Then**:
  - Hook blocks commit with error message
  - Error message explains why (Windows compatibility)
  - Error message suggests fix tool (one-command remediation)

**Test Case 3**: CI/CD Validation

- **Given**: PR with cross-platform violation passing pre-commit (--no-verify used)
- **When**: CI/CD runs on Windows platform
- **Then**:
  - Validation fails on Windows
  - Report uploaded as artifact
  - PR status check fails (blocks merge)

**Test Case 4**: Self-Service Fix Tool

- **Given**: 10 files with missing `encoding='utf-8'`
- **When**: Developer runs `python scripts/fix-encoding-issues.py --apply`
- **Then**:
  - All 10 files updated automatically
  - Report shows 10 changes made
  - Re-running validation shows 0 issues

---

## 10. Versioning & Compatibility

### Version Compatibility

**Current Version**: 1.0.0

**Compatibility Guarantees**:
- Patch versions (1.0.x): Backward compatible bug fixes, new validation rules (warn-only)
- Minor versions (1.x.0): Backward compatible new features, promote warn → block rules
- Major versions (x.0.0): Breaking changes (e.g., remove deprecated patterns), migration guide required

### Dependency Compatibility

| Dependency | Minimum Version | Tested Version | Status |
|------------|----------------|----------------|--------|
| SAP-009 (agent-awareness) | 1.0.0 | 1.1.0 | ✅ Compatible |
| SAP-006 (quality-gates) | 1.0.0 | 1.0.0 | ✅ Compatible (optional) |
| SAP-005 (ci-cd-workflows) | 1.0.0 | 1.0.0 | ✅ Compatible (optional) |

### Migration Path

**From Documentation-Only to SAP-031**:

1. **Phase 1 (Week 1)**: Install discoverability layer
   - Add enforcement reminder to root AGENTS.md
   - Create domain AGENTS.md with patterns
   - Create template files

2. **Phase 2 (Week 2)**: Add pre-commit hooks
   - Install validation hooks
   - Start with warn-only mode
   - Collect false-positive reports

3. **Phase 3 (Week 3)**: Promote to block mode
   - Refine rules based on false positives
   - Promote critical rules to blocking
   - Add self-service fix tools

4. **Phase 4 (Week 4)**: Add CI/CD validation
   - Create CI/CD workflow
   - Enable status checks
   - Configure badge in README

---

## 11. Related Specifications

### Within chora-base

**SAP Artifacts**:
- [Capability Charter](./capability-charter.md) - Problem statement and solution design
- [Awareness Guide](./AGENTS.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - Core SAP protocols
- [SAP-009: Agent Awareness](../agent-awareness/protocol-spec.md) - Nested awareness hierarchy
- [SAP-006: Quality Gates](../quality-gates/protocol-spec.md) - Pre-commit hook framework
- [SAP-005: CI/CD Workflows](../ci-cd-workflows/protocol-spec.md) - CI/CD automation
- [SAP-030: Cross-Platform Fundamentals](../cross-platform-fundamentals/protocol-spec.md) - Reference implementation

**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

**Official Documentation**:
- [Pre-commit Framework](https://pre-commit.com/) - Hook management
- [GitHub Actions Matrix Strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs) - Multi-platform CI/CD
- [Shift-Left Testing (IBM)](https://www.ibm.com/garage/method/practices/code/shift-left-testing) - Early validation principles

**Community Resources**:
- [chora-base enforcement examples](https://github.com/your-org/chora-base/tree/main/.githooks) - Pre-commit hooks
- [chora-base CI/CD workflows](https://github.com/your-org/chora-base/tree/main/.github/workflows) - Validation workflows

---

**Version History**:
- **1.0.0** (2025-11-08): Initial protocol specification for Discoverability-Based Enforcement
  - 6 core contracts (architecture, discoverability, pre-commit, CI/CD, templates, fix tools)
  - Integration with SAP-009 (discoverability), SAP-006 (pre-commit), SAP-005 (CI/CD)
  - Cross-platform reference implementation examples
  - Security, performance, and error handling specifications
