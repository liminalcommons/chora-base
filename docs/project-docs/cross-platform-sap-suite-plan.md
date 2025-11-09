# Cross-Platform SAP Suite Implementation Plan

**Version**: 1.0.0
**Date**: 2025-11-03
**Status**: Planning
**Priority**: Critical (driven by chora-compose Windows→Mac migration pain)

---

## Executive Summary

This plan establishes comprehensive cross-platform (Mac/Windows/Linux) support through:
- **3 new SAPs** (030-032) covering fundamentals, Python environments, and CI/CD
- **3 enhanced SAPs** (003, 005, 008) for cross-platform generation, workflows, and Python-first scripting
- **Migration from bash to Python** for all automation scripts
- **Multi-OS CI testing as standard quality gate**

**Business Driver**: chora-compose required significant rework to diagnose and fix platform-specific issues when migrating from Windows to Mac development. This must never happen again.

---

## Background: The Problem

### Real Pain from chora-compose
- **Initial development**: Exclusively on Windows
- **Migration**: Moved to Mac
- **Result**: Significant rework needed to diagnose and fix platform-specific issues
- **Root cause**: No systematic cross-platform development patterns or validation

### Current State Analysis
**Strengths**:
- Python 3.11+ (cross-platform by nature)
- Docker with multi-architecture support (amd64 + arm64)
- Cross-platform tools: `just`, `pytest`, `ruff`, `mypy`
- React/Node.js stack (naturally cross-platform)

**Gaps**:
- No dedicated cross-platform SAP
- SAP-008 explicitly states "Linux + macOS only"
- Bash scripts not portable to Windows (without WSL/Git Bash)
- CI only tests on Ubuntu (no macOS/Windows validation)
- Platform-specific concerns scattered across SAPs (not centralized)

---

## Solution: Cross-Platform SAP Suite

### New SAPs (3)

#### SAP-030: Cross-Platform Development Fundamentals

**Purpose**: Core patterns and practices for developing code that works seamlessly on Mac, Windows, and Linux.

**Scope**:
1. **Platform Setup Guides**
   - Python installation (pyenv, python.org, Microsoft Store, Linux repos)
   - Node.js installation (nvm, official installers, system packages)
   - Tool installation (just, git, Docker Desktop vs Engine)
   - IDE setup (VS Code cross-platform configuration)

2. **Scripting Standards**
   - **Policy**: Python-first for all automation (works everywhere)
   - Bash only when absolutely necessary (Linux/Mac)
   - No PowerShell-only scripts (Windows lock-in)
   - Cross-platform shebang patterns

3. **File System Patterns**
   - **Paths**: Always use `pathlib.Path`, never string concatenation
   - **Line endings**: .gitattributes configuration (LF for code, CRLF for .bat)
   - **Case sensitivity**: Design for Windows (case-insensitive), works everywhere
   - **Permissions**: Avoid chmod patterns, use platform detection

4. **Path Separator Handling**
   - `os.path.join()` or `pathlib.Path()` (never hardcoded `/` or `\`)
   - Environment variable PATH handling (`:` vs `;`)
   - UNC paths on Windows (`\\server\share`)

5. **Platform Detection Utilities**
   - `scripts/platform-info.py` - Report current platform details
   - `scripts/validate-cross-platform.py` - Test script portability
   - Integration with SAP-006 (Quality Gates)

**Artifacts** (5):
- `capability-charter.md` - Business case, stakeholders, value proposition
- `protocol-spec.md` - Technical contracts (platform detection API, path handling)
- `awareness-guide.md` - How to use, decision trees (when Python vs bash)
- `adoption-blueprint.md` - Step-by-step setup for Mac/Windows/Linux
- `ledger.md` - Adoption tracking

**Success Metrics**:
- Zero platform-specific rework in new projects (vs significant chora-compose pain)
- 2-4 hours saved per project on platform setup
- 100% of developers can contribute (regardless of OS)

---

#### SAP-031: Cross-Platform Python Environments

**Purpose**: Standardize Python installation and environment management across all platforms.

**Scope**:
1. **Python Installation**
   - **macOS**: pyenv (via Homebrew) - Recommended
   - **Linux**: pyenv (via curl) or system package managers
   - **Windows**: py launcher (python.org installer) or pyenv-win
   - Version management strategies

2. **Virtual Environment Patterns**
   - `python -m venv .venv` (works everywhere, no virtualenv dependency)
   - Activation scripts: `.venv/bin/activate` (Mac/Linux) vs `.venv\Scripts\activate` (Windows)
   - Cross-platform activation in documentation

3. **Dependency Isolation**
   - `pyproject.toml` + `pip` (standard, cross-platform)
   - Lock files: `requirements.txt` vs `pip-tools` vs `poetry.lock`
   - Platform-specific dependencies (`sys_platform` markers)

4. **Platform-Specific Python Quirks**
   - **Windows**: Symlinks disabled by default (affects venv, node_modules)
   - **macOS**: Framework builds vs unix builds (impacts native extensions)
   - **Linux**: System Python vs user Python (avoid breaking system packages)

5. **Troubleshooting Guide**
   - "Python not found" on Windows (PATH issues)
   - "Permission denied" on macOS (Gatekeeper, notarization)
   - "Module not found" (venv not activated, wrong Python version)

**Artifacts** (5):
- `capability-charter.md` - Why Python environment management matters
- `protocol-spec.md` - Python version matrix (3.11-3.13), venv contracts
- `awareness-guide.md` - When to use pyenv vs system Python
- `adoption-blueprint.md` - Step-by-step Python setup for each platform
- `ledger.md` - Adoption tracking

**Success Metrics**:
- Zero "Python not found" issues in onboarding
- All developers use same Python version (consistency)
- Virtual environment activation works first try (all platforms)

---

#### SAP-032: Cross-Platform CI/CD & Quality Gates

**Purpose**: Multi-OS testing as a standard quality gate. All code must pass on Mac, Windows, and Linux before merge.

**Scope**:
1. **GitHub Actions Multi-OS Matrix**
   - Standard template:
     ```yaml
     strategy:
       matrix:
         os: [ubuntu-latest, macos-latest, windows-latest]
         python-version: ['3.11', '3.12', '3.13']
     runs-on: ${{ matrix.os }}
     ```
   - Cost optimization (run full matrix on main, subset on PRs)

2. **Platform-Specific Test Patterns**
   - Skip Docker tests on Windows (unless WSL detected)
   - Path separator tests (validate cross-platform path handling)
   - Permission tests (chmod on Linux/Mac, ACLs on Windows)
   - Line ending validation (ensure .gitattributes works)

3. **Conditional Workflow Steps**
   - OS-specific setup:
     ```yaml
     - name: Install just (macOS)
       if: runner.os == 'macOS'
       run: brew install just

     - name: Install just (Windows)
       if: runner.os == 'Windows'
       run: choco install just

     - name: Install just (Linux)
       if: runner.os == 'Linux'
       run: sudo snap install just --classic
     ```

4. **Quality Gate Standards**
   - **Policy**: All tests must pass on all 3 platforms
   - No merging with platform-specific failures
   - Platform-specific skips must be documented (why, when to remove)

5. **Cost Management**
   - Ubuntu runners: Free (public repos) or cheapest (private)
   - macOS runners: 10x cost of Ubuntu (use strategically)
   - Windows runners: 2x cost of Ubuntu
   - Recommendation: Full matrix on `main` + releases, Ubuntu-only on PRs (with weekly full matrix)

**Artifacts** (5):
- `capability-charter.md` - Business case for multi-OS CI
- `protocol-spec.md` - CI matrix contracts, quality gate thresholds
- `awareness-guide.md` - When to run full matrix vs subset
- `adoption-blueprint.md` - Step-by-step GitHub Actions setup
- `ledger.md` - Adoption tracking

**Success Metrics**:
- 15-20% more bugs caught pre-release (platform-specific)
- Zero post-release platform-specific hotfixes
- CI confidence: "Works on my machine" → "Works on all machines"

---

### Enhanced SAPs (3)

#### SAP-003: Project Bootstrap (Cross-Platform Generation)

**Current State**: Generates Python projects with zero dependencies, portable by default.

**Enhancements**:
1. **Generate .gitattributes**
   ```gitattributes
   # Normalize line endings (LF in repo, platform-native on checkout)
   * text=auto

   # Force LF for specific files
   *.py text eol=lf
   *.sh text eol=lf
   *.md text eol=lf

   # Force CRLF for Windows batch files
   *.bat text eol=crlf
   *.ps1 text eol=crlf
   ```

2. **Add Platform Detection Utility**
   - Generate `scripts/platform-info.py` in all new projects
   - Reports: OS, Python version, architecture, PATH, tool availability

3. **Cross-Platform Path Handling in Templates**
   - All generated code uses `pathlib.Path`
   - No hardcoded `/` or `\` separators
   - Template examples show cross-platform patterns

4. **Platform-Specific Setup Instructions**
   - Generated README.md includes platform-specific setup sections
   - Links to SAP-030 (fundamentals) and SAP-031 (Python environments)

**Files Modified**:
- `scripts/generate-project.py` (add .gitattributes, platform-info.py)
- `templates/project/README.md` (add platform-specific sections)
- `templates/project/scripts/` (add platform utilities)

**Success Criteria**:
- All generated projects include .gitattributes (line endings normalized)
- All generated projects include platform detection utility
- README includes platform-specific setup instructions

---

#### SAP-005: CI/CD Workflows (Multi-OS Matrix by Default)

**Current State**: GitHub Actions templates test on Ubuntu only.

**Enhancements**:
1. **Update Default Template to Multi-OS Matrix**
   - Current: `runs-on: ubuntu-latest`
   - New:
     ```yaml
     strategy:
       matrix:
         os: [ubuntu-latest, macos-latest, windows-latest]
         python-version: ['3.11', '3.12', '3.13']
     runs-on: ${{ matrix.os }}
     ```

2. **Add Platform-Specific Examples**
   - New workflow: `.github/workflows/platform-specific-tests.yml`
   - Demonstrates conditional steps, OS detection, skip patterns

3. **Cost Optimization Template**
   - New workflow: `.github/workflows/pr-checks.yml` (Ubuntu only)
   - Existing workflow: `.github/workflows/full-matrix.yml` (all platforms, on main)

4. **Documentation Updates**
   - Link to SAP-032 for multi-OS testing standards
   - Explain when to use full matrix vs Ubuntu-only

**Files Modified**:
- `templates/workflows/.github/workflows/ci.yml` (add multi-OS matrix)
- `templates/workflows/.github/workflows/pr-checks.yml` (new, Ubuntu-only)
- `templates/workflows/.github/workflows/platform-tests.yml` (new, conditional steps)
- `docs/skilled-awareness/sap-005-ci-cd-workflows/protocol-spec.md` (add multi-OS contracts)

**Success Criteria**:
- Default CI template includes multi-OS matrix
- Projects have both full matrix (main) and subset (PR) workflows
- Documentation explains cost tradeoffs

---

#### SAP-008: Automation Scripts (Python-First Migration)

**Current State**:
- "Platform support: Linux + macOS only"
- "Scripts not portable (Linux vs macOS)" identified as medium risk
- Open question: "Bash for simplicity vs Python for portability?"

**Decision**: **Python for portability** (driven by Windows support requirement)

**Enhancements**:
1. **Migrate All Bash Scripts to Python**
   - Current bash scripts in `scripts/`:
     - `setup-dev-env.sh` → `setup-dev-env.py`
     - `run-tests.sh` → `run-tests.py`
     - `build.sh` → `build.py`
     - Any other `.sh` files

   - Keep justfile, but have it call Python scripts:
     ```just
     # Cross-platform by default
     test:
         python scripts/run-tests.py

     setup:
         python scripts/setup-dev-env.py
     ```

2. **Document "Python-First" Scripting Policy**
   - **Tier 1 (Preferred)**: Pure Python scripts (cross-platform by default)
   - **Tier 2 (Acceptable)**: Portable shell (POSIX sh, not bash-specific)
   - **Tier 3 (Avoid)**: Platform-specific (bash, PowerShell, batch)

   - Decision tree: "Should I use Python or bash?"
     - Needs to run on Windows? → Python
     - Complex logic, error handling, testing? → Python
     - Simple one-liner, Linux/Mac only? → bash (document why)

3. **Add Windows Validation to CI**
   - Update SAP-008's own CI to test scripts on Windows
   - Use SAP-032 multi-OS matrix

4. **Remove "Linux + macOS only" Limitation**
   - Update capability-charter.md: "Platform support: Mac, Windows, Linux"
   - Remove platform limitation from protocol-spec.md
   - Update adoption-blueprint.md with Windows instructions

**Files Modified**:
- `scripts/*.sh` → `scripts/*.py` (migrate all bash scripts)
- `justfile` (call Python scripts instead of bash)
- `docs/skilled-awareness/sap-008-automation-scripts/capability-charter.md` (remove platform limitation)
- `docs/skilled-awareness/sap-008-automation-scripts/protocol-spec.md` (add Python-first policy)
- `docs/skilled-awareness/sap-008-automation-scripts/awareness-guide.md` (add decision tree)

**Success Criteria**:
- Zero bash scripts in `scripts/` (all migrated to Python)
- Documentation states "Python-first" policy
- CI tests scripts on Windows (validates cross-platform)
- justfile calls Python scripts (cross-platform by default)

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Goal**: Create SAP-030 (Cross-Platform Fundamentals) as the cornerstone.

1. **Draft SAP-030 Artifacts** (5 files)
   - `capability-charter.md` - Business case, value proposition
   - `protocol-spec.md` - Technical contracts (path handling, platform detection)
   - `awareness-guide.md` - How to use, decision trees
   - `adoption-blueprint.md` - Step-by-step setup for Mac/Windows/Linux
   - `ledger.md` - Adoption tracking template

2. **Create Cross-Platform Utilities**
   - `scripts/platform-info.py` - Report platform details
   - `scripts/validate-cross-platform.py` - Test script portability
   - Add to repository root

3. **Update sap-catalog.json**
   - Add SAP-030 entry (ID, title, status: "active")
   - Update roadmap (29 → 30 SAPs)

**Deliverables**:
- ✅ SAP-030 complete (5 artifacts)
- ✅ 2 cross-platform utilities created
- ✅ sap-catalog.json updated

---

### Phase 2: Python Environments (Week 2)

**Goal**: Create SAP-031 (Cross-Platform Python Environments).

1. **Draft SAP-031 Artifacts** (5 files)
   - `capability-charter.md` - Why Python environment management matters
   - `protocol-spec.md` - Python version matrix, venv contracts
   - `awareness-guide.md` - When to use pyenv vs system Python
   - `adoption-blueprint.md` - Step-by-step Python setup for each platform
   - `ledger.md` - Adoption tracking template

2. **Create Python Environment Utilities**
   - `scripts/check-python-env.py` - Validate Python setup
   - `scripts/setup-python-env.py` - Automated Python environment setup

3. **Update sap-catalog.json**
   - Add SAP-031 entry

**Deliverables**:
- ✅ SAP-031 complete (5 artifacts)
- ✅ 2 Python environment utilities created
- ✅ sap-catalog.json updated

---

### Phase 3: CI/CD & Quality Gates (Week 2-3)

**Goal**: Create SAP-032 (Cross-Platform CI/CD) and enhance SAP-005.

1. **Draft SAP-032 Artifacts** (5 files)
   - `capability-charter.md` - Business case for multi-OS CI
   - `protocol-spec.md` - CI matrix contracts, quality gates
   - `awareness-guide.md` - When to run full matrix vs subset
   - `adoption-blueprint.md` - Step-by-step GitHub Actions setup
   - `ledger.md` - Adoption tracking template

2. **Enhance SAP-005**
   - Update `protocol-spec.md` (add multi-OS matrix contracts)
   - Create multi-OS workflow templates:
     - `.github/workflows/ci.yml` (full matrix)
     - `.github/workflows/pr-checks.yml` (Ubuntu-only)
     - `.github/workflows/platform-tests.yml` (conditional steps)

3. **Update sap-catalog.json**
   - Add SAP-032 entry
   - Update SAP-005 status (enhanced)

**Deliverables**:
- ✅ SAP-032 complete (5 artifacts)
- ✅ SAP-005 enhanced (3 new workflow templates)
- ✅ sap-catalog.json updated

---

### Phase 4: Automation Script Migration (Week 3-4)

**Goal**: Migrate all bash scripts to Python (SAP-008 enhancement).

1. **Audit Existing Bash Scripts**
   - List all `.sh` files in repository
   - Prioritize by usage frequency
   - Document migration plan for each

2. **Migrate Scripts**
   - `scripts/setup-dev-env.sh` → `setup-dev-env.py`
   - `scripts/run-tests.sh` → `run-tests.py`
   - `scripts/build.sh` → `build.py`
   - Any other `.sh` files found

3. **Update justfile**
   - Replace bash script calls with Python script calls
   - Ensure cross-platform compatibility

4. **Enhance SAP-008 Documentation**
   - Update `capability-charter.md` (remove "Linux + macOS only")
   - Update `protocol-spec.md` (add Python-first policy)
   - Update `awareness-guide.md` (add decision tree: Python vs bash)
   - Update `adoption-blueprint.md` (add Windows instructions)

5. **Add Windows CI Validation**
   - Update SAP-008's CI workflow to test on Windows
   - Use SAP-032 multi-OS matrix pattern

**Deliverables**:
- ✅ All bash scripts migrated to Python
- ✅ justfile updated (calls Python scripts)
- ✅ SAP-008 documentation enhanced
- ✅ SAP-008 CI tests on Windows

---

### Phase 5: Project Bootstrap Enhancement (Week 4)

**Goal**: Enhance SAP-003 for cross-platform project generation.

1. **Update Project Templates**
   - Add `.gitattributes` template (line ending normalization)
   - Add `scripts/platform-info.py` to generated projects
   - Update README.md template (platform-specific setup sections)

2. **Update Generation Script**
   - Modify `scripts/generate-project.py` to include new templates
   - Add platform detection to generated projects

3. **Enhance SAP-003 Documentation**
   - Update `protocol-spec.md` (add .gitattributes, platform utilities)
   - Update `awareness-guide.md` (link to SAP-030, SAP-031)
   - Update `adoption-blueprint.md` (mention cross-platform generation)

**Deliverables**:
- ✅ SAP-003 enhanced (cross-platform generation)
- ✅ .gitattributes template added
- ✅ platform-info.py added to generated projects
- ✅ README.md includes platform-specific instructions

---

### Phase 6: Validation & Documentation (Week 5)

**Goal**: Comprehensive testing and documentation updates.

1. **Cross-Platform Validation**
   - Test all SAPs on Mac, Windows, Linux
   - Validate all scripts work on all platforms
   - Document any platform-specific quirks discovered

2. **Update Master Documentation**
   - Update main README.md (link to new SAPs)
   - Update CHANGELOG.md (document new SAPs, enhancements)
   - Update roadmap (30 → 32 SAPs, 96% coverage)

3. **Community Testing**
   - Recruit Windows developers for pilot testing
   - Gather feedback on SAP-030, SAP-031, SAP-032
   - Iterate based on real-world usage

4. **Final sap-catalog.json Update**
   - Mark all SAPs as "active"
   - Update coverage metrics
   - Update roadmap

**Deliverables**:
- ✅ All SAPs validated on 3 platforms
- ✅ Master documentation updated
- ✅ Community feedback incorporated
- ✅ Final sap-catalog.json update

---

## Success Metrics

### Primary Metrics

1. **Zero Platform-Specific Rework**
   - Target: 0 hours spent on platform-specific bug fixes (vs significant chora-compose pain)
   - Measure: Track time spent on platform-specific issues in new projects

2. **Multi-Platform CI Coverage**
   - Target: 100% of projects use multi-OS CI matrix
   - Measure: % of projects with GitHub Actions testing on Mac/Windows/Linux

3. **Script Portability**
   - Target: 100% of automation scripts work on all platforms
   - Measure: Run all scripts on Mac/Windows/Linux, track failures

4. **Developer Onboarding**
   - Target: 2-4 hours saved per project on platform setup
   - Measure: Time from clone to first successful test run

### Secondary Metrics

5. **Bug Detection Rate**
   - Target: 15-20% more bugs caught pre-release (platform-specific)
   - Measure: Platform-specific bugs found in CI vs production

6. **Developer Satisfaction**
   - Target: 100% of developers can contribute regardless of OS
   - Measure: Survey developers on platform-specific friction

7. **SAP Adoption**
   - Target: SAP-030, SAP-031, SAP-032 adopted by all new projects
   - Measure: % of projects with ledger entries for these SAPs

---

## Risks & Mitigations

### Risk 1: CI Cost Increase (macOS/Windows runners)

**Impact**: High (macOS runners 10x cost, Windows 2x cost)

**Mitigation**:
- Run full matrix on `main` + releases only
- Run Ubuntu-only on PRs (with weekly full matrix)
- Document cost tradeoffs in SAP-032
- Use GitHub's free minutes for public repos (2,000 min/month)

### Risk 2: Bash Script Migration Complexity

**Impact**: Medium (some scripts may be complex)

**Mitigation**:
- Start with simple scripts, iterate to complex
- Test each migration thoroughly on all platforms
- Keep original bash scripts temporarily (fallback)
- Document any migration challenges in SAP-008

### Risk 3: Windows-Specific Bugs Not Caught

**Impact**: Medium (Windows quirks may slip through)

**Mitigation**:
- Recruit Windows developers for pilot testing
- Add Windows-specific test cases to CI
- Document known Windows quirks in SAP-030
- Use WSL as fallback for Windows developers

### Risk 4: Developer Resistance to Python Scripts

**Impact**: Low (bash simpler for one-liners)

**Mitigation**:
- Allow bash for simple one-liners (document exception)
- Show benefits: better error handling, testing, cross-platform
- Provide migration examples in SAP-008
- Emphasize "Python-first" not "Python-only"

---

## Dependencies

### Internal Dependencies

- **SAP-003** (Project Bootstrap) - Used by SAP-030 for project generation
- **SAP-005** (CI/CD Workflows) - Enhanced by SAP-032 for multi-OS testing
- **SAP-006** (Quality Gates) - Uses SAP-032 for platform validation
- **SAP-008** (Automation Scripts) - Enhanced for Python-first scripting

### External Dependencies

- **GitHub Actions** - Multi-OS runners (ubuntu, macos, windows)
- **Python 3.11+** - Required for all platforms
- **just** - Task runner (must be installable on all platforms)
- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)

### Tool Availability

| Tool | macOS | Windows | Linux |
|------|-------|---------|-------|
| Python 3.11+ | ✅ (pyenv, Homebrew) | ✅ (python.org, pyenv-win) | ✅ (system, pyenv) |
| just | ✅ (brew) | ✅ (choco, scoop) | ✅ (snap, apt) |
| Docker | ✅ (Docker Desktop) | ✅ (Docker Desktop, WSL2) | ✅ (Docker Engine) |
| git | ✅ (Xcode, Homebrew) | ✅ (Git for Windows) | ✅ (system) |

---

## Timeline

| Phase | Duration | Deliverables | Status |
|-------|----------|--------------|--------|
| Phase 1: Foundation | Week 1 | SAP-030, utilities | Planning |
| Phase 2: Python Envs | Week 2 | SAP-031, utilities | Planning |
| Phase 3: CI/CD | Week 2-3 | SAP-032, SAP-005 enhancements | Planning |
| Phase 4: Script Migration | Week 3-4 | SAP-008 enhancements, bash→Python | Planning |
| Phase 5: Bootstrap | Week 4 | SAP-003 enhancements | Planning |
| Phase 6: Validation | Week 5 | Testing, documentation | Planning |

**Total Duration**: 5 weeks
**Expected Completion**: 2025-12-08

---

## Stakeholders

### Primary Stakeholders

- **Development Team** - Will adopt SAPs, use cross-platform patterns
- **Contributors** - Need consistent experience on Mac/Windows/Linux
- **Project Maintainers** - Responsible for CI/CD, quality gates

### Secondary Stakeholders

- **Windows Developers** - Primary beneficiaries (currently unsupported)
- **macOS Developers** - Benefit from consistency, multi-OS CI
- **Linux Developers** - Ensure no regression from current state

---

## Related Documents

- [SAP Catalog](../../sap-catalog.json)
- [SAP Framework (SAP-000)](../skilled-awareness/sap-000-framework/)
- [Automation Scripts (SAP-008)](../skilled-awareness/sap-008-automation-scripts/)
- [CI/CD Workflows (SAP-005)](../skilled-awareness/sap-005-ci-cd-workflows/)
- [Project Bootstrap (SAP-003)](../skilled-awareness/sap-003-project-bootstrap/)
- [chora-compose Repository](https://github.com/your-org/chora-compose) - Origin of platform pain

---

## Appendix: Lessons from chora-compose

### What Went Wrong

1. **Windows-first development** without macOS validation
2. **Platform assumptions** (file paths, line endings, permissions)
3. **No CI testing** on macOS (only caught issues post-merge)
4. **Bash scripts** didn't work on Windows (required WSL workarounds)

### What We Learned

1. **Test on all platforms** from day 1 (not just when porting)
2. **Multi-OS CI** catches issues early (pre-merge)
3. **Python scripts** are more portable than bash (for Windows support)
4. **Line endings matter** (.gitattributes essential for mixed teams)
5. **Path separators matter** (pathlib > string concatenation)

### What We're Fixing

✅ SAP-030: Codifies cross-platform patterns (no more assumptions)
✅ SAP-031: Standardizes Python environments (all platforms)
✅ SAP-032: Multi-OS CI as standard (catches issues pre-merge)
✅ SAP-008: Python-first scripting (works on Windows)
✅ SAP-003: Generates .gitattributes (line endings normalized)

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Approve plan** (or request changes)
3. **Begin Phase 1** (SAP-030 Foundation)
4. **Track progress** using this document
5. **Update status** as phases complete

---

**Plan Author**: Claude (AI Assistant)
**Reviewed By**: [Pending]
**Approved By**: [Pending]
**Approval Date**: [Pending]
