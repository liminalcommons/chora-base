# Phase 2: Findings and Recommendations

**Generated**: 2025-10-28
**Phase**: SAP Coverage Mapping
**Status**: Complete

---

## Executive Summary

Phase 2 analysis reveals **202 uncovered files (47.2%)** across the chora-base repository. The gaps fall into clear patterns that suggest specific remediation strategies.

### Key Findings

1. **Root-level files need SAP assignment** (5 critical files)
2. **Documentation sprawl** in `/docs/` (135 files, mostly in `docs/reference/chora-compose/`)
3. **Examples directory ambiguity** (34 files need policy decision)
4. **Legacy template artifacts** (17 files in `static-template/src/`)
5. **Scripts directory gap** (3 utility scripts uncovered)

---

## Pattern Analysis

### Pattern 1: Root-Level Documentation Not in SAP-002

**Files**:
- `AGENTS.md` (23.0 KB)
- `CLAUDE_SETUP_GUIDE.md` (33.3 KB)

**Analysis**: These are core chora-base documentation files that should be covered by SAP-002 (chora-base). They provide critical setup and usage information.

**Recommendation**: **ADD to SAP-002**
- Update `SAP-002` (chora-base) `protocol-spec.md` to explicitly include these files
- Update inventory script's SAP-002 patterns to include:
  - `AGENTS.md`
  - `CLAUDE_SETUP_GUIDE.md`

**Action**: Phase 3 task

---

### Pattern 2: Root-Level Code/Config Files

**Files**:
- `repo-dump.py` (4.6 KB) - Utility script for repository analysis
- `setup.py` (14.3 KB) - Python package setup (possibly obsolete if using pyproject.toml)
- `.gitignore` (0.4 KB) - Git configuration

**Analysis**:
- `.gitignore` should be covered by SAP-003 (project-bootstrap) as a blueprint artifact
- `setup.py` may be obsolete (check if using pyproject.toml instead)
- `repo-dump.py` should be covered by SAP-008 (automation-scripts) or archived

**Recommendation**:
1. **`.gitignore`** → ADD to SAP-003 (project-bootstrap)
2. **`setup.py`** → INVESTIGATE (may be obsolete, archive if unused)
3. **`repo-dump.py`** → ADD to SAP-008 (automation-scripts) OR archive if obsolete

**Action**: Phase 3 investigation + decision

---

### Pattern 3: /docs/ Directory Sprawl

**Breakdown**:
- `docs/BENEFITS.md` (1 file) - Core documentation
- `docs/DOCUMENTATION_PLAN.md` (1 file) - Core documentation
- `docs/integration/` (2 files) - Integration plans for v3.2.0 and v3.3.0
- `docs/releases/` (8 files) - Release notes for v2.1.0 through v3.3.0
- `docs/research/` (3 files) - Adopter learnings and research
- `docs/reference/` (121 files) - Massive concentration, mostly `docs/reference/chora-compose/`

**Analysis**:

#### 3.1. Root docs/ files
`BENEFITS.md` and `DOCUMENTATION_PLAN.md` should be covered by SAP-007 (documentation-framework) or SAP-002 (chora-base).

**Recommendation**: ADD to SAP-007 (documentation-framework)

#### 3.2. docs/integration/
Integration plans are project planning documents. Should be covered by SAP-002 (chora-base) as historical project documentation.

**Recommendation**: ADD to SAP-002 (chora-base)

#### 3.3. docs/releases/
Release notes are historical records of releases. Should be covered by SAP-002 (chora-base) as project history.

**Recommendation**: ADD to SAP-002 (chora-base)

#### 3.4. docs/research/
Research documents are valuable for understanding design decisions. Should be covered by SAP-007 (documentation-framework) as design documentation.

**Recommendation**: ADD to SAP-007 (documentation-framework)

#### 3.5. docs/reference/chora-compose/
**CRITICAL FINDING**: 121 files in `docs/reference/chora-compose/docs/` are not covered by any SAP.

**Analysis**: This appears to be documentation for the `chora-compose` package, which is a separate MCP server project. These files include:
- Tutorials (getting-started, intermediate, advanced)
- How-to guides (configs, deployment, generation, mcp, storage, testing, etc.)
- Explanation documents (architecture, concepts, design decisions, ecosystem, workflows)
- Reference documentation (API, generators, MCP)
- Project documentation (adoption audits, quality baselines, handoffs)

**Recommendation**: **MAJOR DECISION REQUIRED**
- **Option A**: Move to separate `chora-compose` repository (if it's a separate package)
- **Option B**: Create new SAP-014 for "Chora-Compose Documentation"
- **Option C**: Archive if chora-compose is obsolete/deprecated
- **Option D**: Integrate relevant parts into SAP-007 (documentation-framework) as examples

**Action**: **USER DECISION REQUIRED** - Is chora-compose:
1. A separate package that needs its own repo?
2. Part of chora-base that needs its own SAP?
3. Obsolete and should be archived?

#### 3.6. docs/reference/skilled-awareness/ uncovered files
Several skilled-awareness files are uncovered:
- `INDEX.md` (16.0 KB) - Should be SAP-000 (sap-framework)
- `quality-gates.md` (4.8 KB) - Planning document for SAP-006
- `inputs-audit.md` (5.7 KB) - Audit document
- `chora-base-sap-roadmap.md` (7.6 KB) - Roadmap for SAPs
- `document-templates.md` (7.6 KB) - Templates
- `workflow-mapping.md` (5.6 KB) - Workflow mapping
- `copier-audit.md` (2.4 KB) - Audit document

**Recommendation**: ADD these to SAP-000 (sap-framework) as SAP planning/audit artifacts

#### 3.7. docs/reference/ecosystem/ uncovered files
- `multi-repo-capability-evolution-to-w3.md` (33.3 KB)
- `ARCHITECTURE_CLARIFICATION.md` (13.1 KB)
- `how-to-setup-mcp-ecosystem.md` (15.7 KB)

**Recommendation**: ADD to SAP-002 (chora-base) as architecture documentation

#### 3.8. docs/reference/chora-base/ uncovered
- `latest-conversation.md` (488.6 KB) - HUGE file, likely temporary

**Recommendation**: **ARCHIVE** (temporary conversation log, not permanent documentation)

---

### Pattern 4: Examples Directory

**34 uncovered files** in `examples/full-featured-with-vision/`

**Analysis**: This appears to be a complete example project with:
- Scripts (15 files)
- Documentation (AGENTS.md, CONTRIBUTING.md, README.md, ROADMAP.md, etc.)
- Config files (.github workflows, pyproject.toml, justfile, .pre-commit-config.yaml)
- Dev-docs (vision documents, memory)

**Recommendation**: **USER DECISION REQUIRED**
- **Option A**: Cover by SAP-003 (project-bootstrap) as reference example
- **Option B**: Archive if obsolete
- **Option C**: Keep intentionally outside SAP coverage (examples are meant to be templates, not SAP-controlled)

**Preferred**: **Option C** - Examples should remain outside SAP coverage as they are reference implementations, not part of the core framework.

**Action**: Document this policy in SAP framework

---

### Pattern 5: static-template/ Uncovered Files

**Breakdown**:
- `static-template/PYPI_SETUP.md` (9.7 KB) - Should be SAP-007 (documentation-framework)
- `static-template/NAMESPACES.md` (9.5 KB) - Should be SAP-007 (documentation-framework)
- `static-template/ROADMAP.md` (9.1 KB) - Should be SAP-002 (chora-base)
- `static-template/UPGRADING.md` (4.5 KB) - Should be SAP-007 (documentation-framework)
- `static-template/.gitignore` (3.1 KB) - Should be SAP-003 (project-bootstrap)
- `static-template/docker/AGENTS.md` (4.2 KB) - Should be SAP-011 (docker-operations)
- `static-template/docker/CLAUDE.md` (12.7 KB) - Should be SAP-011 (docker-operations)
- `static-template/src/{{package_name}}/memory/*.py` (4 files, 32 KB) - Legacy template code
- `static-template/src/__package_name__/memory/*.py` (2 files, 17 KB) - Template code
- `static-template/src/__package_name__/utils/*.py` (5 files, 56 KB) - Template code (except claude_metrics.py which is covered)

**Analysis**:
- Documentation files should be added to appropriate SAPs
- `.gitignore` should be added to SAP-003
- `docker/` CLAUDE/AGENTS files should be added to SAP-011
- Template source code files are intentionally templates (Jinja2 placeholders), but should still be covered by a SAP

**Recommendation**:
1. Documentation → Add to SAP-007
2. `.gitignore` → Add to SAP-003
3. `docker/` docs → Add to SAP-011
4. Template source code → ADD to SAP-010 (memory-system) for memory files
5. Template utils code → Create patterns to cover template source code

**Action**: Phase 3 updates

---

### Pattern 6: Scripts Directory Gap

**3 uncovered scripts**:
- `scripts/rollback-migration.sh` (0.7 KB)
- `scripts/inventory-chora-base.py` (12.0 KB)
- `scripts/fix-shell-syntax.sh` (1.2 KB)

**Analysis**: These are utility scripts created during recent work:
- `rollback-migration.sh` - Migration utility
- `inventory-chora-base.py` - Phase 1 inventory script
- `fix-shell-syntax.sh` - Shell syntax fixer

**Recommendation**: ADD to SAP-008 (automation-scripts)

**Action**: Phase 3 update

---

## Recommended Actions by Priority

### Priority 1: Critical Root-Level Files
- [ ] Add `AGENTS.md` to SAP-002
- [ ] Add `CLAUDE_SETUP_GUIDE.md` to SAP-002
- [ ] Investigate `setup.py` (obsolete?)
- [ ] Add `.gitignore` to SAP-003
- [ ] Add/archive `repo-dump.py` (SAP-008 or archive)

### Priority 2: USER DECISION - chora-compose Documentation
- [ ] **USER**: Decide fate of 121 `docs/reference/chora-compose/` files
  - Separate repo?
  - New SAP-014?
  - Archive?
  - Integrate into SAP-007?

### Priority 3: USER DECISION - Examples Directory
- [ ] **USER**: Decide policy for `examples/` directory
  - Cover by SAP-003?
  - Archive?
  - Keep outside SAP coverage? (RECOMMENDED)

### Priority 4: docs/ Directory Assignments
- [ ] Add `docs/BENEFITS.md` to SAP-007
- [ ] Add `docs/DOCUMENTATION_PLAN.md` to SAP-007
- [ ] Add `docs/integration/*.md` to SAP-002
- [ ] Add `docs/releases/*.md` to SAP-002
- [ ] Add `docs/research/*.md` to SAP-007
- [ ] Add `docs/reference/ecosystem/*.md` to SAP-002
- [ ] Add `docs/reference/skilled-awareness/INDEX.md` and audit files to SAP-000
- [ ] Archive `docs/reference/chora-base/latest-conversation.md`

### Priority 5: static-template/ Assignments
- [ ] Add `static-template/PYPI_SETUP.md` to SAP-007
- [ ] Add `static-template/NAMESPACES.md` to SAP-007
- [ ] Add `static-template/ROADMAP.md` to SAP-002
- [ ] Add `static-template/UPGRADING.md` to SAP-007
- [ ] Add `static-template/.gitignore` to SAP-003
- [ ] Add `static-template/docker/AGENTS.md` to SAP-011
- [ ] Add `static-template/docker/CLAUDE.md` to SAP-011
- [ ] Add template source code files to appropriate SAPs

### Priority 6: Scripts Gap
- [ ] Add `scripts/rollback-migration.sh` to SAP-008
- [ ] Add `scripts/inventory-chora-base.py` to SAP-008
- [ ] Add `scripts/fix-shell-syntax.sh` to SAP-008

---

## Phase 3 Preparation

### Files Ready for Immediate Assignment (No User Decision Needed)
**Count**: ~50 files

These can be assigned to SAPs in Phase 3 without user input.

### Files Requiring User Decision
**Count**: ~155 files (121 chora-compose + 34 examples)

These require user decisions before proceeding.

### Files Ready for Archive
**Count**: 1-2 files
- `docs/reference/chora-base/latest-conversation.md` (488 KB temporary file)
- Possibly `setup.py` if obsolete

---

## Recommended Phase 3 Approach

1. **Start with Priority 1 & 4-6** (no user decisions needed)
   - Update SAP protocol-specs to include newly assigned files
   - Update inventory script patterns
   - Re-run inventory to confirm coverage improvement
   - Expected: ~50 files added to SAP coverage

2. **USER DECISIONS for Priority 2 & 3**
   - Present chora-compose options to user
   - Present examples policy options to user
   - Wait for decisions

3. **Complete Phase 3 based on decisions**
   - Implement chosen approach for chora-compose
   - Implement chosen policy for examples
   - Final inventory re-run
   - Target: 90%+ coverage (or 100% with intentional exclusions documented)

---

## Success Metrics

**Current State** (Phase 2 complete):
- Coverage: 52.8% (226/428 files)
- Uncovered: 47.2% (202 files)

**After Priority 1, 4-6** (Phase 3 partial):
- Expected: ~65% coverage (+50 files)
- Remaining: ~150 files (pending user decisions)

**After User Decisions** (Phase 3 complete):
- Target: 90%+ coverage
- Intentional exclusions: Documented in SAP framework

---

## Next Steps

1. **Present this report to user** for Priority 2 & 3 decisions
2. **Proceed with Priority 1, 4-6** if user approves
3. **Update SAP protocol-specs** with new file patterns
4. **Re-run inventory** to measure progress
5. **Phase 3 line-by-line audit** of remaining files
