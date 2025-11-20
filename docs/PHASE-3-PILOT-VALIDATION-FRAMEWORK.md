# Phase 3 Pilot Validation Framework

**Date**: 2025-11-21
**Context**: CORD-2025-023 Phase 3 Preparation
**Purpose**: Define validation criteria, testing methodology, and success metrics for Phase 3 pilot testing
**Status**: 📋 Ready for Use (Awaiting Phase 3 Start)

---

## Overview

Phase 3 validates the chora-base Copier template through real-world pilot testing in three environments:
1. **Phase 3.1 (chora-workspace-lwhs)**: Internal pilot in chora-workspace
2. **Phase 3.2 (chora-workspace-3ub6)**: External pilots in castalia and external project
3. **Phase 3.3 (chora-workspace-duyr)**: Pilot validation report

This document provides the validation framework for systematic testing and metrics collection.

---

## Validation Objectives

### Primary Objectives

1. **Template Generation**: Validate that `copier copy` creates functional projects with all SAPs
2. **Update Propagation**: Validate that `copier update` successfully propagates template changes
3. **Conflict Resolution**: Validate that merge conflicts are handled correctly
4. **SAP Integration**: Validate that all 8 SAPs work as expected in generated projects
5. **User Experience**: Validate that installation and update workflows are intuitive

### Secondary Objectives

1. **Performance**: Measure template generation time and update propagation time
2. **Error Handling**: Validate error messages and recovery workflows
3. **Documentation**: Validate that generated documentation is accurate and helpful
4. **Automation**: Validate that justfile recipes work correctly in generated projects

---

## Pilot Testing Methodology

### Phase 3.1: Internal Pilot (chora-workspace)

**Goal**: Validate template generation and update propagation in controlled environment

**Test Scenarios**:

#### Scenario 1.1: Minimal Mode Generation
```bash
# Generate project with minimal SAP mode
copier copy <template-url> test-minimal \
  --data sap_selection_mode=minimal

# Validate:
- inbox/ directory exists (SAP-001)
- .beads/ directory exists (SAP-015)
- justfile contains inbox and beads recipes
- README.md reflects 2 SAPs
```

**Expected Results**:
- ✅ Project generates successfully in <3 minutes
- ✅ Only SAP-001 and SAP-015 files present
- ✅ justfile contains ~50 lines (minimal recipes)
- ✅ README.md lists 2 SAPs

**Validation Checklist**:
- [ ] Project generates without errors
- [ ] Directory structure matches expectations
- [ ] justfile recipes execute successfully
- [ ] SAP-001: `just inbox-status` works
- [ ] SAP-015: `bd list` works
- [ ] README.md accurate

---

#### Scenario 1.2: Standard Mode Generation
```bash
# Generate project with standard SAP mode
copier copy <template-url> test-standard \
  --data sap_selection_mode=standard

# Validate:
- All minimal mode files (SAP-001, SAP-015)
- SAP-053: scripts/conflict-checker.py exists
- SAP-010: .chora/memory/ directories exist
- justfile contains ~100 lines
- README.md reflects 4 SAPs
```

**Expected Results**:
- ✅ Project generates successfully in <3 minutes
- ✅ SAP-001, SAP-015, SAP-053, SAP-010 files present
- ✅ justfile contains ~100 lines
- ✅ README.md lists 4 SAPs

**Validation Checklist**:
- [ ] All minimal mode validations pass
- [ ] SAP-053: `just conflict-check` works
- [ ] SAP-010: `.chora/memory/events/` exists
- [ ] Python dependencies installable (`poetry install` or `pip install -r requirements.txt`)
- [ ] README.md accurate

---

#### Scenario 1.3: Comprehensive Mode Generation
```bash
# Generate project with comprehensive SAP mode
copier copy <template-url> test-comprehensive \
  --data sap_selection_mode=comprehensive

# Validate:
- All standard mode files
- SAP-051: scripts/pre-push-check.sh exists
- SAP-052: scripts/ownership-coverage.py exists
- SAP-056: scripts/validate-manifest.py exists
- SAP-008: justfile has ~200 lines
- README.md reflects 8 SAPs
```

**Expected Results**:
- ✅ Project generates successfully in <3 minutes
- ✅ All 8 SAPs present
- ✅ justfile contains ~200 lines
- ✅ README.md lists 8 SAPs

**Validation Checklist**:
- [ ] All standard mode validations pass
- [ ] SAP-051: `just pre-push-check` works
- [ ] SAP-052: `just ownership-coverage` works
- [ ] SAP-056: `just feature-manifest-validate` works
- [ ] SAP-008: `just automation-stats` works
- [ ] README.md accurate

---

#### Scenario 1.4: Template Update Propagation
```bash
# 1. Generate project (v1)
copier copy <template-url> test-update \
  --data sap_selection_mode=standard

# 2. Customize project
cd test-update
echo "# Custom Section\n\nMy custom content." >> README.md
git add README.md
git commit -m "Add custom section to README"

# 3. Update template (v2)
# (Maintainer: Make change to template, commit, push)

# 4. Update project
copier update

# Validate:
- Update fetches template changes
- Merge process prompts for conflicts (if any)
- Custom section preserved in README.md
- New template content added
```

**Expected Results**:
- ✅ `copier update` runs successfully
- ✅ Custom section preserved in README.md
- ✅ New template content added
- ✅ No unexpected conflicts
- ✅ Update completes in <2 minutes

**Validation Checklist**:
- [ ] `copier update` command succeeds
- [ ] Custom changes preserved
- [ ] Template changes applied
- [ ] Conflict resolution (if any) works correctly
- [ ] Project still functional after update
- [ ] justfile recipes still work

---

#### Scenario 1.5: Conflict Resolution Testing

**Test Setup**: Create intentional conflicts to validate resolution workflow

**Conflict Type 1: Low-Conflict (Automatic Merge)**
```bash
# User change: Add custom section at end of README
# Template change: Add new section in middle of README
# Expected: Both sections preserved, no conflict
```

**Conflict Type 2: High-Conflict (Manual Resolution)**
```bash
# User change: Modify "Quick Start" section
# Template change: Update "Quick Start" section
# Expected: Merge conflict, user resolves manually
```

**Validation Checklist**:
- [ ] Low-conflict scenarios merge automatically
- [ ] High-conflict scenarios present clear conflict markers
- [ ] Conflict resolution instructions clear
- [ ] Manual resolution preserves both changes
- [ ] Project functional after resolution

---

### Phase 3.2: External Pilots

**Goal**: Validate template in real-world projects with external users

#### Pilot 3.2A: castalia Project

**Project Type**: Existing chora ecosystem project (game development)

**Test Scenarios**:
1. Generate new castalia project with comprehensive mode
2. Integrate existing castalia code into generated structure
3. Validate SAP-053 conflict detection with game branches
4. Validate SAP-015 beads tasks for game development workflow
5. Test template update after 1 week of development

**Validation Checklist**:
- [ ] Template generation successful
- [ ] Integration with existing code smooth
- [ ] SAPs work in game development context
- [ ] Update propagation successful
- [ ] Developer feedback collected

---

#### Pilot 3.2B: External Project

**Project Type**: Non-chora project (ideally from different domain)

**Test Scenarios**:
1. Generate project with standard mode
2. Customize for external project needs
3. Validate SAP-001 coordination workflow
4. Validate justfile recipes for external use case
5. Test template update after customization

**Validation Checklist**:
- [ ] Template generation successful
- [ ] Customization straightforward
- [ ] SAPs work in external context
- [ ] Documentation clear for non-chora users
- [ ] Update propagation successful

---

## Success Criteria

### Phase 3.1 Success Criteria (Internal Pilot)

**Must Have** (100% required):
1. ✅ All 3 preset modes generate successfully
2. ✅ justfile recipes execute without errors
3. ✅ `copier update` successfully propagates changes
4. ✅ Custom changes preserved after update
5. ✅ No blocking bugs in core SAPs (001, 015, 053, 010)

**Should Have** (80% required):
1. ✅ Generation completes in <3 minutes
2. ✅ Update completes in <2 minutes
3. ✅ Conflict resolution works for 4/5 test scenarios
4. ✅ Documentation accurate for all SAPs
5. ✅ Python dependencies install without issues

**Nice to Have** (50% desired):
1. ✅ All justfile recipes documented with examples
2. ✅ Template includes troubleshooting guide
3. ✅ SAP-052, SAP-056, SAP-008 fully functional
4. ✅ CI/CD examples included

---

### Phase 3.2 Success Criteria (External Pilots)

**Must Have**:
1. ✅ Both external pilots complete successfully
2. ✅ No blocking issues reported by external users
3. ✅ SAPs work in diverse project contexts
4. ✅ Documentation sufficient for external users

**Should Have**:
1. ✅ Positive feedback from external users
2. ✅ Less than 3 clarification questions per pilot
3. ✅ Update workflow understood without support
4. ✅ Customization straightforward

---

### Phase 3.3 Success Criteria (Validation Report)

**Must Have**:
1. ✅ Comprehensive validation report created
2. ✅ All metrics collected and analyzed
3. ✅ Lessons learned documented
4. ✅ Phase 4 recommendations provided

---

## Metrics Collection

### Template Generation Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Generation Time** | <3 minutes | `time copier copy ...` |
| **File Count** | 11-17 files | `find test-project -type f \| wc -l` |
| **Directory Count** | 5-8 directories | `find test-project -type d \| wc -l` |
| **Error Rate** | 0 errors | Count errors during generation |
| **Questionnaire Time** | <3 minutes | User timing (manual) |

**Collection Script**:
```bash
#!/bin/bash
# collect-generation-metrics.sh

START_TIME=$(date +%s)

copier copy <template-url> test-metrics \
  --data sap_selection_mode=standard

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

FILE_COUNT=$(find test-metrics -type f | wc -l)
DIR_COUNT=$(find test-metrics -type d | wc -l)

echo "Generation Time: ${DURATION}s"
echo "File Count: ${FILE_COUNT}"
echo "Directory Count: ${DIR_COUNT}"
```

---

### Update Propagation Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Update Time** | <2 minutes | `time copier update` |
| **Conflict Rate** | <30% | Count conflicts / total updates |
| **Resolution Time** | <5 minutes | User timing (manual) |
| **Success Rate** | 100% | Updates complete without errors |

**Collection Script**:
```bash
#!/bin/bash
# collect-update-metrics.sh

START_TIME=$(date +%s)

cd test-project
copier update --defaults

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Check for conflicts
CONFLICTS=$(git diff --name-only --diff-filter=U | wc -l)

echo "Update Time: ${DURATION}s"
echo "Conflicts: ${CONFLICTS}"
```

---

### SAP Functionality Metrics

| SAP | Validation Command | Expected Result |
|-----|-------------------|-----------------|
| **SAP-001** | `just inbox-status` | Exit code 0, shows dashboard |
| **SAP-015** | `bd list` | Exit code 0, lists tasks |
| **SAP-053** | `just conflict-check` | Exit code 0, detects conflicts |
| **SAP-010** | `just memory-events 10` | Shows 10 recent events |
| **SAP-051** | `just pre-push-check` | Exit code 0, runs validation |
| **SAP-052** | `just ownership-coverage` | Exit code 0, shows coverage |
| **SAP-056** | `just feature-manifest-validate` | Exit code 0, validates manifest |
| **SAP-008** | `just automation-stats` | Exit code 0, shows stats |

**Collection Script**:
```bash
#!/bin/bash
# collect-sap-metrics.sh

cd test-project

SAPS=("SAP-001:just inbox-status" \
      "SAP-015:bd list" \
      "SAP-053:just conflict-check" \
      "SAP-010:just memory-events 10")

for SAP_CMD in "${SAPS[@]}"; do
  SAP="${SAP_CMD%%:*}"
  CMD="${SAP_CMD#*:}"

  echo "Testing ${SAP}: ${CMD}"
  if $CMD &>/dev/null; then
    echo "✅ ${SAP} PASS"
  else
    echo "❌ ${SAP} FAIL"
  fi
done
```

---

### User Experience Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Questionnaire Clarity** | 4+/5 | User survey |
| **Documentation Clarity** | 4+/5 | User survey |
| **Customization Ease** | 4+/5 | User survey |
| **Update Workflow Clarity** | 4+/5 | User survey |
| **Overall Satisfaction** | 4+/5 | User survey |

**Survey Template** (see below)

---

## Validation Checklist

### Pre-Pilot Checklist (Before Phase 3.1)

- [ ] Distribution strategy decided (Option A/B/C)
- [ ] Template pushed to chosen distribution channel
- [ ] v1.0.0 tag created
- [ ] README.md updated with installation instructions
- [ ] Test environment prepared (clean workspace)
- [ ] Metrics collection scripts ready

---

### Phase 3.1 Checklist (chora-workspace Pilot)

**Generation Tests**:
- [ ] Scenario 1.1: Minimal mode generation (PASS/FAIL)
- [ ] Scenario 1.2: Standard mode generation (PASS/FAIL)
- [ ] Scenario 1.3: Comprehensive mode generation (PASS/FAIL)

**Update Tests**:
- [ ] Scenario 1.4: Template update propagation (PASS/FAIL)
- [ ] Scenario 1.5: Conflict resolution (PASS/FAIL)

**Metrics**:
- [ ] Generation metrics collected
- [ ] Update metrics collected
- [ ] SAP functionality metrics collected

**Artifacts**:
- [ ] Test projects created (minimal, standard, comprehensive)
- [ ] Update test project with before/after snapshots
- [ ] Metrics report generated

---

### Phase 3.2 Checklist (External Pilots)

**castalia Pilot**:
- [ ] Project generated successfully
- [ ] SAPs integrated with game development workflow
- [ ] Template update tested
- [ ] Developer feedback collected
- [ ] Metrics collected

**External Pilot**:
- [ ] Project generated successfully
- [ ] SAPs work in external context
- [ ] Template update tested
- [ ] User feedback collected
- [ ] Metrics collected

---

### Phase 3.3 Checklist (Validation Report)

- [ ] All metrics compiled and analyzed
- [ ] Lessons learned documented
- [ ] Phase 4 recommendations prepared
- [ ] Validation report reviewed
- [ ] A-MEM event logged for Phase 3 completion

---

## Pilot Report Template

Use this template for Phase 3.3 validation report:

```markdown
# Phase 3 Pilot Validation Report

**Date**: [YYYY-MM-DD]
**Trace ID**: cord-2025-023-phase-3
**Status**: [In Progress / Complete]

---

## Executive Summary

[2-3 paragraph summary of pilot results]

**Overall Result**: [SUCCESS / PARTIAL / FAILURE]
**Key Findings**: [3-5 bullet points]
**Recommendation**: [Proceed to Phase 4 / Address issues / Major revision]

---

## Phase 3.1 Results (Internal Pilot)

### Generation Tests

| Scenario | Result | Time | Notes |
|----------|--------|------|-------|
| 1.1: Minimal | PASS/FAIL | Xs | ... |
| 1.2: Standard | PASS/FAIL | Xs | ... |
| 1.3: Comprehensive | PASS/FAIL | Xs | ... |

### Update Tests

| Scenario | Result | Time | Conflicts | Notes |
|----------|--------|------|-----------|-------|
| 1.4: Update | PASS/FAIL | Xs | N | ... |
| 1.5: Conflicts | PASS/FAIL | Xs | N | ... |

### Metrics Summary

**Generation**:
- Average generation time: Xs (target: <3min)
- Average file count: N files
- Error rate: X%

**Update**:
- Average update time: Xs (target: <2min)
- Conflict rate: X% (target: <30%)
- Success rate: X% (target: 100%)

**SAPs**:
- SAP-001: [PASS/FAIL]
- SAP-015: [PASS/FAIL]
- SAP-053: [PASS/FAIL]
- SAP-010: [PASS/FAIL]
- SAP-051: [PASS/FAIL]
- SAP-052: [PASS/FAIL]
- SAP-056: [PASS/FAIL]
- SAP-008: [PASS/FAIL]

---

## Phase 3.2 Results (External Pilots)

### castalia Pilot

**Duration**: [N days]
**Developer**: [Name]
**Project Type**: Game development

**Results**:
- Generation: [PASS/FAIL]
- Integration: [PASS/FAIL]
- SAP Usage: [PASS/FAIL]
- Update: [PASS/FAIL]

**Feedback**:
- [Positive feedback 1]
- [Positive feedback 2]
- [Issue 1]
- [Issue 2]

---

### External Pilot

**Duration**: [N days]
**User**: [Name/Org]
**Project Type**: [Description]

**Results**:
- Generation: [PASS/FAIL]
- Customization: [PASS/FAIL]
- SAP Usage: [PASS/FAIL]
- Update: [PASS/FAIL]

**Feedback**:
- [Positive feedback 1]
- [Positive feedback 2]
- [Issue 1]
- [Issue 2]

---

## Issues Discovered

### Blocking Issues (Must Fix Before Phase 4)

1. **[Issue Title]**
   - **Severity**: Blocking
   - **Description**: [...]
   - **Impact**: [...]
   - **Fix**: [...]

### Non-Blocking Issues (Nice to Fix)

1. **[Issue Title]**
   - **Severity**: Minor
   - **Description**: [...]
   - **Impact**: [...]
   - **Fix**: [...]

---

## Lessons Learned

### What Worked Well

1. [Lesson 1]
2. [Lesson 2]
3. [Lesson 3]

### What Could Be Improved

1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

### Surprises

1. [Surprise 1]
2. [Surprise 2]

---

## Recommendations for Phase 4

### Must Do

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Should Do

1. [Recommendation 1]
2. [Recommendation 2]

### Nice to Have

1. [Recommendation 1]
2. [Recommendation 2]

---

## Appendices

### Appendix A: Metrics Data

[Raw metrics data, charts, graphs]

### Appendix B: User Survey Results

[Survey responses, feedback]

### Appendix C: Test Artifacts

[Links to test projects, before/after snapshots]

---

**Prepared By**: [Name]
**Reviewed By**: [Name]
**Status**: [Draft / Final]
**Next Steps**: [Phase 4 planning / Issue resolution]
```

---

## User Survey Template

### chora-base Template Pilot Survey

**Thank you for piloting the chora-base Copier template!**

Your feedback helps us improve the template before public release.

---

**1. Template Generation**

Rate your experience generating a project from the template:
- [ ] 5 - Excellent (effortless, intuitive)
- [ ] 4 - Good (smooth with minor questions)
- [ ] 3 - Acceptable (worked but unclear at times)
- [ ] 2 - Poor (confusing, needed support)
- [ ] 1 - Very Poor (broken, couldn't complete)

**Comments**:
[Your feedback]

---

**2. Questionnaire Clarity**

How clear were the copier questionnaire questions?
- [ ] 5 - Very clear (understood all questions)
- [ ] 4 - Clear (understood most questions)
- [ ] 3 - Somewhat clear (needed to guess a few)
- [ ] 2 - Unclear (guessed on many)
- [ ] 1 - Very unclear (confused throughout)

**Comments**:
[Your feedback]

---

**3. Documentation Quality**

How helpful was the generated project documentation?
- [ ] 5 - Very helpful (answered all questions)
- [ ] 4 - Helpful (answered most questions)
- [ ] 3 - Somewhat helpful (found some answers)
- [ ] 2 - Not helpful (had to search elsewhere)
- [ ] 1 - Not helpful at all (documentation missing/wrong)

**Comments**:
[Your feedback]

---

**4. Template Update Experience**

Rate your experience updating the project after template changes:
- [ ] 5 - Excellent (seamless, no issues)
- [ ] 4 - Good (smooth with minor conflicts)
- [ ] 3 - Acceptable (conflicts resolved easily)
- [ ] 2 - Poor (difficult conflict resolution)
- [ ] 1 - Very Poor (couldn't complete update)
- [ ] N/A - Did not test update

**Comments**:
[Your feedback]

---

**5. SAP Integration**

Which SAPs did you use, and how well did they work?

| SAP | Used? | Rating (1-5) | Comments |
|-----|-------|--------------|----------|
| SAP-001 (Inbox) | ☐ Yes ☐ No | ___/5 | |
| SAP-015 (Beads) | ☐ Yes ☐ No | ___/5 | |
| SAP-053 (Conflict) | ☐ Yes ☐ No | ___/5 | |
| SAP-010 (Memory) | ☐ Yes ☐ No | ___/5 | |
| SAP-051 (Pre-merge) | ☐ Yes ☐ No | ___/5 | |
| SAP-052 (Ownership) | ☐ Yes ☐ No | ___/5 | |
| SAP-056 (Traceability) | ☐ Yes ☐ No | ___/5 | |
| SAP-008 (Automation) | ☐ Yes ☐ No | ___/5 | |

---

**6. Overall Satisfaction**

How satisfied are you with the chora-base template overall?
- [ ] 5 - Very satisfied (would recommend)
- [ ] 4 - Satisfied (good experience)
- [ ] 3 - Neutral (acceptable)
- [ ] 2 - Dissatisfied (had issues)
- [ ] 1 - Very dissatisfied (would not use again)

**Comments**:
[Your feedback]

---

**7. Open Feedback**

**What did you like most?**
[Your answer]

**What needs improvement?**
[Your answer]

**Any bugs or issues encountered?**
[Your answer]

**Would you use this template for future projects?**
- [ ] Yes, definitely
- [ ] Yes, probably
- [ ] Maybe
- [ ] Probably not
- [ ] No

---

**Thank you for your feedback!**

Your input directly shapes Phase 4 improvements.

---

## References

### Related Documents

- **Phase 1 Completion**: [.chora/memory/knowledge/notes/2025-11-21-phase-1-copier-template-completion.md](../../.chora/memory/knowledge/notes/2025-11-21-phase-1-copier-template-completion.md)
- **Phase 2.1 Completion**: [.chora/memory/knowledge/notes/2025-11-21-phase-2-1-test-suite-completion.md](../../.chora/memory/knowledge/notes/2025-11-21-phase-2-1-test-suite-completion.md)
- **Phase 2.2 Completion**: [.chora/memory/knowledge/notes/2025-11-21-phase-2-2-copier-update-validation.md](../../.chora/memory/knowledge/notes/2025-11-21-phase-2-2-copier-update-validation.md)
- **Distribution Strategy**: [DISTRIBUTION-STRATEGY.md](DISTRIBUTION-STRATEGY.md)

### External Resources

- **Copier Documentation**: https://copier.readthedocs.io
- **SAP-060 Protocol**: [docs/skilled-awareness/strategic-opportunity-management/protocol-spec.md](../docs/skilled-awareness/strategic-opportunity-management/protocol-spec.md)

---

**Created**: 2025-11-21
**Status**: 📋 Ready for Use
**Trace ID**: cord-2025-023-phase-3-validation
**SAP**: SAP-060 Strategic Opportunity Management
