# Cross-Platform SAP Suite - Next Scope Implementation Plan

**Version**: 1.0.0
**Date**: 2025-11-03
**Status**: Planning
**Priority**: P0 (Continuation of Week 1-2 success)

---

## Context: What We've Completed

### ✅ Week 1-2 Deliverables (Completed in ~2 hours!)

1. **SAP-030: Cross-Platform Fundamentals** - Foundation patterns
2. **SAP-031: Python Environments** - Python setup across platforms
3. **SAP-032: CI/CD Quality Gates** - Multi-OS testing
4. **Utilities**: platform-info.py, check-python-env.py
5. **Templates**: .gitattributes, multi-OS CI workflows
6. **Catalog**: 29 → 32 SAPs, 94% coverage

**Key Learnings**:
- SAP generation works brilliantly (80% time savings validated)
- Real Windows issues found & fixed (Unicode, symlinks, encoding)
- Dogfooding successful (.gitattributes applied to chora-base)

---

## Next Scope: Phase 4 - Bash Script Migration (Week 3-4)

### Goal

Migrate 6 bash scripts to Python, enhancing SAP-008 to remove "Linux + macOS only" limitation and enable Windows contributions.

### Current State Analysis

**Bash Scripts Found** (6 total):
1. `check-sap-awareness-integration.sh` - Validates SAP awareness patterns
2. `fix-shell-syntax.sh` - Fixes shell script syntax issues
3. `merge-upstream-structure.sh` - Merges upstream changes
4. `rollback-migration.sh` - Rolls back failed migrations
5. `validate-links.sh` - Validates documentation links
6. `validate-prerequisites.sh` - Checks prerequisite tools

**SAP-008 Current Status**:
- Version: 1.0.0 (Draft, Phase 3)
- **Limitation**: No explicit platform restriction documented yet
- Focus: Safety contracts (idempotency, error handling, rollback)
- 25 total scripts (bash + Python mix)

**Blocker Identified**: SAP-008 is currently **Draft** status, needs to be formalized first before enhancement.

---

## Revised Priority Order

### Option A: Formalize SAP-008 First (Recommended)

**Rationale**: SAP-008 is in Draft status. Should formalize existing capability before adding cross-platform enhancement.

**Sequence**:
1. Formalize SAP-008 v1.0.0 (existing 25 scripts, current state)
2. Create SAP-008 v1.1.0 enhancement (Python-first + Windows support)
3. Migrate bash scripts as part of v1.1.0 adoption

**Timeline**: 1-2 weeks
- Week 3: Formalize SAP-008 v1.0.0 (document existing scripts, safety contracts)
- Week 4: Enhance to v1.1.0 (Python-first policy, script migration)

### Option B: Direct Migration (Faster but risky)

**Rationale**: Migrate scripts now, document in SAP-008 afterward.

**Sequence**:
1. Migrate 6 bash scripts to Python immediately
2. Update SAP-008 to reflect new reality (Python-first)
3. Formalize SAP-008 with cross-platform support included

**Timeline**: 1 week
- Risk: Changing SAP-008 while it's still Draft (less risky than changing Active SAP)

---

## Recommended Approach: **Option B** (Direct Migration)

### Justification

1. **SAP-008 is Draft**: Still in formalization phase, easier to evolve now
2. **Cross-platform is urgent**: Real pain from chora-compose (documented)
3. **Small scope**: Only 6 scripts to migrate (manageable in 1 week)
4. **Foundation ready**: SAP-030 Python-first patterns already defined
5. **Validation ready**: SAP-032 multi-OS CI patterns available

### Risk Mitigation

1. **Keep bash scripts temporarily**: Don't delete, mark as deprecated
2. **Test on Windows**: Use check-python-env.py and platform-info.py patterns
3. **Validate each migration**: Run on Windows before committing
4. **Update justfile gradually**: One script at a time

---

## Detailed Implementation Plan: Next 1-2 Weeks

### Week 3: Bash Script Migration

#### Day 1: Audit & Prioritize (2 hours)

**Tasks**:
1. Read all 6 bash scripts, understand functionality
2. Identify dependencies (do any scripts call others?)
3. Prioritize by complexity (simplest first)
4. Document migration plan for each script

**Deliverable**: Migration priority list with complexity estimates

**Proposed Priority** (simplest → complex):
1. `validate-prerequisites.sh` - Simple tool checking (like check-python-env.py)
2. `rollback-migration.sh` - File operations (use pathlib)
3. `validate-links.sh` - Link validation (might use existing Python script)
4. `check-sap-awareness-integration.sh` - SAP validation logic
5. `fix-shell-syntax.sh` - Text processing
6. `merge-upstream-structure.sh` - Git operations

#### Day 2-3: Migrate Priority 1-3 (4-6 hours)

**Script 1: validate-prerequisites.sh → validate-prerequisites.py**
- **Pattern**: Similar to check-python-env.py (tool availability checks)
- **Effort**: 1 hour
- **Test**: Run on Windows, validate tool detection

**Script 2: rollback-migration.sh → rollback-migration.py**
- **Pattern**: Use pathlib for file operations
- **Effort**: 1-2 hours
- **Test**: Create test migration, rollback on Windows

**Script 3: validate-links.sh → validate-links.py**
- **Pattern**: Check if existing Python link validator exists (might already be Python!)
- **Effort**: 1-2 hours
- **Test**: Run on docs/ directory, validate on Windows

**Deliverable**: 3 Python scripts, bash scripts marked deprecated

#### Day 4-5: Migrate Priority 4-6 (6-8 hours)

**Script 4: check-sap-awareness-integration.sh → check-sap-awareness-integration.py**
- **Pattern**: SAP validation logic (similar to sap-evaluator.py patterns)
- **Effort**: 2-3 hours
- **Test**: Run against existing SAPs on Windows

**Script 5: fix-shell-syntax.sh → fix-shell-syntax.py**
- **Pattern**: Text processing (use re module, pathlib)
- **Effort**: 2-3 hours
- **Test**: Create test shell script with syntax errors, fix on Windows

**Script 6: merge-upstream-structure.sh → merge-upstream-structure.py**
- **Pattern**: Git operations (use subprocess for git commands)
- **Effort**: 2-3 hours
- **Test**: Test on non-critical branch on Windows

**Deliverable**: 6 Python scripts total, all tested on Windows

#### Day 6: Update justfile (2 hours)

**Tasks**:
1. Replace bash script calls with Python script calls
2. Test all justfile commands on Windows
3. Update justfile documentation (if any)

**Example Changes**:
```just
# Before
validate-links:
    bash scripts/validate-links.sh

# After
validate-links:
    python scripts/validate-links.py
```

**Deliverable**: justfile updated, all commands cross-platform

#### Day 7: Enhance SAP-008 Documentation (2-3 hours)

**Files to Update**:

1. **capability-charter.md**
   - Add "Cross-platform support (Mac, Windows, Linux)" to capabilities
   - Update problem statement: Reference chora-compose Windows→Mac pain
   - Add "Python-first scripting policy" as key principle

2. **protocol-spec.md**
   - Add Section: "3.8 Cross-Platform Scripting Standards"
   - Document Python-first policy (Tier 1: Python, Tier 2: Portable sh, Tier 3: Platform-specific)
   - Add decision tree: "When to use Python vs bash"
   - Reference SAP-030 for cross-platform patterns

3. **awareness-guide.md**
   - Add cross-reference to SAP-030 (Cross-Platform Fundamentals)
   - Add cross-reference to SAP-031 (Python Environments)
   - Add Windows-specific notes (PYTHONIOENCODING, symlinks)

4. **adoption-blueprint.md**
   - Add "Platform Compatibility" section
   - Windows setup instructions (Python, justfile via choco)
   - Document how to test scripts on Windows

**Deliverable**: SAP-008 enhanced for cross-platform support

---

### Week 4: Validation & SAP-003 Enhancement

#### Phase 4A: Cross-Platform Validation (2-3 hours)

**Tasks**:
1. Run all 6 Python scripts on Windows (already done during migration)
2. Test justfile commands on Windows
3. Document any platform-specific quirks discovered
4. Update SAP-008 with findings

**Validation Checklist**:
- [ ] All Python scripts run on Windows without errors
- [ ] All justfile commands work on Windows
- [ ] No hardcoded path separators (/, \)
- [ ] No Unicode issues (use ASCII or handle encoding)
- [ ] File operations use pathlib.Path
- [ ] Git operations use subprocess with proper encoding

**Deliverable**: Validation report, SAP-008 quirks documented

#### Phase 4B: SAP-003 Enhancement (4-6 hours)

**Goal**: Enhance Project Bootstrap (SAP-003) to generate cross-platform projects by default.

**Tasks**:

1. **Add .gitattributes to static-template** (30 min)
   - Copy templates/cross-platform/.gitattributes → static-template/.gitattributes
   - Test generation with Copier/setup.py

2. **Add platform-info.py to static-template** (30 min)
   - Copy scripts/platform-info.py → static-template/scripts/platform-info.py
   - Update README to mention platform detection utility

3. **Add check-python-env.py to static-template** (30 min)
   - Copy scripts/check-python-env.py → static-template/scripts/check-python-env.py
   - Add to justfile: `just check-env` command

4. **Update README.md template** (1-2 hours)
   - Add "Platform Compatibility" section
   - Document Python 3.11+ requirement for all platforms
   - Add platform-specific setup instructions:
     - macOS: pyenv via Homebrew
     - Windows: python.org or pyenv-win
     - Linux: pyenv or system packages
   - Link to SAP-030, SAP-031 for details

5. **Update setup.py (or generation script)** (2-3 hours)
   - Ensure .gitattributes is copied
   - Ensure platform utilities are copied
   - Add platform detection to generation process
   - Test generation on Windows

6. **Enhance SAP-003 Documentation** (1 hour)
   - Update capability-charter.md: Add "Cross-platform by default" capability
   - Update protocol-spec.md: Document .gitattributes, platform utilities
   - Update awareness-guide.md: Link to SAP-030, SAP-031
   - Update adoption-blueprint.md: Mention cross-platform generation

**Deliverable**: SAP-003 enhanced, generated projects are cross-platform by default

---

## Success Criteria

### Week 3 Success Criteria

1. ✅ All 6 bash scripts migrated to Python
2. ✅ All Python scripts tested on Windows
3. ✅ justfile updated to call Python scripts
4. ✅ SAP-008 documentation enhanced for cross-platform
5. ✅ No bash scripts remain in active use (deprecated only)

### Week 4 Success Criteria

1. ✅ All Python scripts validated on Windows (no failures)
2. ✅ SAP-003 generates cross-platform projects by default
3. ✅ Generated projects include .gitattributes, platform utilities
4. ✅ README templates include platform-specific setup
5. ✅ SAP-003 documentation enhanced

### Overall Success Metrics

- **Zero bash scripts** in active use (Python-first achieved)
- **Windows developers** can contribute immediately (no WSL required)
- **Generated projects** work on Mac/Windows/Linux from day 1
- **chora-compose pain** prevented (no future platform-specific rework)

---

## Risks & Mitigations

### Risk 1: Bash Scripts Have Complex Logic

**Impact**: Medium (migration takes longer than estimated)

**Mitigation**:
- Prioritize simplest scripts first (validate-prerequisites.sh)
- Keep bash scripts temporarily (fallback if Python version fails)
- Test each migration before moving to next
- Budget extra time for complex scripts (merge-upstream-structure.sh)

### Risk 2: Python Scripts Don't Work on Windows

**Impact**: High (breaks cross-platform goal)

**Mitigation**:
- Test on Windows after each migration
- Use patterns from platform-info.py, check-python-env.py (already work on Windows)
- Use pathlib, subprocess with encoding='utf-8'
- Avoid platform-specific features (symlinks, chmod)

### Risk 3: justfile Commands Break on Windows

**Impact**: Medium (developers can't use automation)

**Mitigation**:
- Test justfile on Windows after updates
- Use `python scripts/foo.py` syntax (works everywhere)
- Avoid bash-specific syntax in justfile recipes
- Document Windows-specific commands if needed (if: runner.os == 'Windows')

### Risk 4: SAP-003 Generation Breaks

**Impact**: High (can't generate new projects)

**Mitigation**:
- Test generation on Windows before committing
- Use setup.py (zero dependencies, works everywhere)
- Validate generated projects on Windows
- Keep original static-template if needed (backup)

---

## Time Estimates

| Phase | Tasks | Estimated Time | Buffer | Total |
|-------|-------|----------------|--------|-------|
| **Week 3: Migration** | | | | |
| Audit & Prioritize | Read 6 scripts, plan | 2h | 0h | 2h |
| Migrate Scripts 1-3 | Simple scripts | 4-6h | 2h | 6-8h |
| Migrate Scripts 4-6 | Complex scripts | 6-8h | 2h | 8-10h |
| Update justfile | Replace bash calls | 2h | 1h | 3h |
| Enhance SAP-008 Docs | 4 files | 2-3h | 1h | 3-4h |
| **Week 3 Total** | | **16-21h** | **6h** | **22-27h** |
| | | | | |
| **Week 4: Validation** | | | | |
| Cross-Platform Validation | Test all scripts | 2-3h | 1h | 3-4h |
| SAP-003: Add templates | .gitattributes, utils | 1.5h | 0.5h | 2h |
| SAP-003: Update README | Platform setup | 1-2h | 1h | 2-3h |
| SAP-003: Update generation | setup.py changes | 2-3h | 1h | 3-4h |
| SAP-003: Enhance docs | 4 files | 1h | 0h | 1h |
| **Week 4 Total** | | **7.5-11h** | **3.5h** | **11-14.5h** |
| | | | | |
| **Grand Total (2 weeks)** | | **23.5-32h** | **9.5h** | **33-41.5h** |

**Realistic Estimate**: 35-40 hours over 2 weeks (~20 hours/week)

---

## Dependencies

### Internal Dependencies

- **SAP-030**: Python-first patterns, pathlib usage → Used in all migrations
- **SAP-031**: Python environment setup → Referenced in SAP-003 README
- **SAP-032**: Multi-OS CI patterns → Used for SAP-008 validation
- **SAP-029**: SAP generation → Already used for SAP-030, 031, 032

### External Dependencies

- **Python 3.11+**: Required for all platforms
- **just**: Task runner (installable via choco/brew/snap)
- **git**: Version control (available on all platforms)
- **Windows testing environment**: Need Windows machine or VM

---

## Deliverables Summary

### Week 3 Deliverables

1. **6 Python scripts** (migrated from bash)
   - validate-prerequisites.py
   - rollback-migration.py
   - validate-links.py
   - check-sap-awareness-integration.py
   - fix-shell-syntax.py
   - merge-upstream-structure.py

2. **justfile updates** (all commands cross-platform)

3. **SAP-008 v1.1.0** (enhanced for cross-platform)
   - capability-charter.md (updated)
   - protocol-spec.md (Python-first policy)
   - awareness-guide.md (cross-references)
   - adoption-blueprint.md (Windows setup)

4. **6 bash scripts deprecated** (kept as fallback)

### Week 4 Deliverables

1. **Validation report** (all scripts tested on Windows)

2. **SAP-003 v1.1.0** (cross-platform generation)
   - static-template/.gitattributes (added)
   - static-template/scripts/platform-info.py (added)
   - static-template/scripts/check-python-env.py (added)
   - static-template/README.md (platform setup added)
   - setup.py or generation script (updated)

3. **SAP-003 documentation enhanced**
   - capability-charter.md (updated)
   - protocol-spec.md (cross-platform features)
   - awareness-guide.md (cross-references)
   - adoption-blueprint.md (updated)

---

## Next Steps After This Scope

### Phase 6: Final Validation (Week 5)

As per original plan:
1. Test all SAPs on Mac, Windows, Linux
2. Update master documentation (README, CHANGELOG)
3. Community testing (recruit Windows developers)
4. Final sap-catalog.json update (mark SAPs as Active)

### Future Enhancements (Q1 2026)

1. **Multi-OS CI in chora-base itself**
   - Apply SAP-032 patterns to chora-base CI
   - Test on Mac/Windows/Linux runners
   - Validate all scripts on all platforms

2. **Docker Multi-Architecture** (SAP-011 v1.1.0)
   - Enhance for M1/M2 Mac support
   - ARM64 + AMD64 builds
   - Reference SAP-030, SAP-032 patterns

3. **Cross-Platform CLI Tools** (SAP-015?)
   - Unified CLI for all platforms
   - Click or Typer framework
   - Replaces justfile for complex operations

---

## Questions for Review

Before proceeding, please confirm:

1. **Approach**: Direct migration (Option B) vs Formalize SAP-008 first (Option A)?
2. **Priority**: Bash migration (Week 3-4) vs SAP-003 enhancement first?
3. **Scope**: All 6 scripts or subset (3 simplest first, validate, then 3 complex)?
4. **Validation**: Windows testing available? (VM, WSL, or native Windows?)
5. **Timeline**: 2 weeks aggressive or 3 weeks comfortable?

---

**Plan Author**: Claude (AI Assistant)
**Reviewed By**: [Pending]
**Approved By**: [Pending]
**Approval Date**: [Pending]
