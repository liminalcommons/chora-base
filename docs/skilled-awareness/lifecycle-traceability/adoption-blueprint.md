---
sap_id: SAP-056
version: 1.0.0
status: Draft
last_updated: 2025-11-16
type: how-to
feature_id: FEAT-SAP-056
requirement_refs:
  - REQ-SAP-056-004
  - REQ-SAP-056-005
  - REQ-SAP-056-006
---

# Adoption Blueprint: Lifecycle Traceability

**SAP ID**: SAP-056
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Last Updated**: 2025-11-16

---

## 1. Overview

This blueprint guides adopters through 4 maturity levels (L0→L4) for achieving 100% lifecycle traceability.

**Maturity Levels**:
- **L0 (Aware)**: Read SAP-056, understand traceability value (~30 min)
- **L1 (Pilot)**: feature-manifest.yaml for 1 feature (~2-4 hours)
- **L2 (Configured)**: Extend to 5+ features, add frontmatter (~8-12 hours)
- **L3 (Active)**: 100% coverage, pre-commit hooks (~20-30 hours)
- **L4 (Community)**: CI/CD enforcement, metrics dashboard (~40-60 hours)

**Time to L3**: 4-6 weeks (cumulative work)

---

## 2. Prerequisites

Before adopting SAP-056, ensure:

- [ ] **SAP-004** (testing-framework) at L1+ - Pytest conventions established
- [ ] **SAP-007** (documentation-framework) at L1+ - Frontmatter in use
- [ ] **SAP-010** (memory-system) at L1+ - Event logging active
- [ ] **SAP-012** (development-lifecycle) at L1+ - Features/sprints tracked
- [ ] **SAP-015** (task-tracking) at L1+ - Beads tasks in use
- [ ] **Git repository** initialized
- [ ] **Python 3.10+** installed (for validation scripts)

**Dependency Check**:
```bash
# Check SAP adoption levels:
python scripts/sap-evaluator.py SAP-004 SAP-007 SAP-010 SAP-012 SAP-015
# → All should be L1 or higher
```

---

## 3. L0 → L1: Pilot (1 Feature)

**Goal**: Create feature-manifest.yaml with 1 complete feature entry

**Time**: 2-4 hours

**Success Criteria**:
- [ ] feature-manifest.yaml exists in project root
- [ ] 1 feature with complete linkage (vision→requirements→code→tests→docs)
- [ ] Validation script passes 100% for this feature

### Step 1: Read SAP-056 Documentation

**Time**: 30 minutes

**Actions**:
1. Read [capability-charter.md](capability-charter.md) (problem, solution, benefits)
2. Skim [protocol-spec.md](protocol-spec.md) (linkage schemas, validation rules)
3. Read [awareness-guide.md](awareness-guide.md) Section 2 (agent patterns)

**Outcome**: Understand why traceability matters and how it works

---

### Step 2: Choose Pilot Feature

**Time**: 15 minutes

**Actions**:
1. Select recently completed feature (status=implemented)
2. Feature should have:
   - Clear vision/goal
   - 1-3 requirements
   - 1-3 code files
   - ≥2 tests
   - ≥1 doc

**Why Recent Feature**: Easier to remember context, likely has complete artifacts

**Example**: Authentication feature with email/password + OAuth

---

### Step 3: Create Feature Manifest

**Time**: 1-2 hours

**Actions**:

1. **Create file** `feature-manifest.yaml` in project root:
   ```yaml
   schema_version: "1.0.0"
   project:
     name: "my-project"
     repository: "https://github.com/org/my-project"

   features: []
   ```

2. **Add first feature entry**:
   ```yaml
   features:
     - id: FEAT-001
       name: "User Authentication"
       description: "Email/password and OAuth2 authentication"
       vision_ref: "CHARTER-001:Outcome-2"  # Reference to capability charter
       status: implemented
       created: "2025-10-01"
       completed: "2025-11-15"

       requirements:
         - id: REQ-001
           description: "Support email/password login"
           acceptance_criteria:
             - "User can register with email/password"
             - "Password hashed with bcrypt"
             - "Login returns JWT token"

       code:
         - path: src/auth/providers.py
           lines_of_code: 256

       tests:
         - path: tests/test_auth.py::test_email_login
           type: unit
           requirement: REQ-001

       documentation:
         - path: docs/how-to/authentication.md
           type: how-to
           audience: users
   ```

3. **Fill in actual paths** from your project

**Tips**:
- Start minimal (1 requirement, 1-2 code files, 1-2 tests, 1 doc)
- Use git log to find commits for this feature
- Use `bd list` to find related beads tasks
- Add `tasks` and `commits` arrays (optional but recommended)

---

### Step 4: Add Pytest Markers

**Time**: 30 minutes

**Actions**:

1. **Add markers to test file** (tests/test_auth.py):
   ```python
   import pytest

   @pytest.mark.feature("FEAT-001")
   @pytest.mark.requirement("REQ-001")
   @pytest.mark.unit
   def test_email_login():
       """Test email/password authentication."""
       # ... test code
   ```

2. **Update all tests** for this feature with markers

**Validation**:
```bash
# Check markers present:
grep -r "@pytest.mark.feature" tests/test_auth.py
# → Should find all tests marked
```

---

### Step 5: Add Documentation Frontmatter

**Time**: 15 minutes

**Actions**:

1. **Add frontmatter to doc** (docs/how-to/authentication.md):
   ```yaml
   ---
   title: "How to Use Authentication"
   type: how-to
   feature_id: FEAT-001
   code_references:
     - src/auth/providers.py
   test_references:
     - tests/test_auth.py::test_email_login
   last_updated: "2025-11-15"
   ---

   # How to Use Authentication
   ...
   ```

2. **Verify** frontmatter is valid YAML

---

### Step 6: Validate Manifest

**Time**: 30 minutes

**Actions**:

1. **Run validation script**:
   ```bash
   python scripts/validate-traceability.py --feature FEAT-001
   ```

2. **Fix any failures**:
   - Broken file paths → Update paths in manifest
   - Missing bidirectional links → Add doc to manifest or manifest ref to doc
   - Schema violations → Correct YAML syntax/structure

3. **Re-run until 100% pass**:
   ```
   ✓ Rule 1: Forward Linkage (PASS)
   ✓ Rule 2: Bidirectional Linkage (PASS)
   ✓ Rule 3: Evidence Requirement (PASS)
   ... (all 10 rules PASS)

   Overall: 100% (10/10 checks passed)
   ```

---

### Step 7: Document Learnings

**Time**: 15 minutes

**Actions**:

1. **Create knowledge note** `.chora/memory/knowledge/notes/sap-056-l1-adoption.md`:
   ```markdown
   ---
   title: "SAP-056 L1 Adoption Experience"
   date: 2025-11-16
   tags: [sap-056, traceability, adoption]
   ---

   # SAP-056 L1 Adoption

   Adopted SAP-056 L1 for feature FEAT-001 (User Authentication).

   **Time Spent**: 3 hours

   **Challenges**:
   - Finding correct vision_ref took 20 min (unclear which charter outcome)
   - Pytest markers required modifying 5 test files

   **Learnings**:
   - Start with recently completed feature (fresh memory)
   - Use git log to find commits → faster than manual search
   - Validation script caught 3 broken links before commit

   **Next Steps**: Extend to 5 features for L2
   ```

2. **Emit A-MEM event**:
   ```bash
   python scripts/emit-event.py sap.adopted \
     --sap-id SAP-056 \
     --level L1 \
     --feature FEAT-001
   ```

---

### L1 Validation Checklist

- [ ] feature-manifest.yaml exists with schema_version + project metadata
- [ ] 1 feature entry with all required fields (id, name, description, vision_ref, status, requirements, code, tests, documentation)
- [ ] All file paths in manifest are valid (files exist)
- [ ] Pytest markers added to all tests (`@pytest.mark.feature`, `@pytest.mark.requirement`)
- [ ] Documentation has frontmatter with `feature_id` and `code_references`
- [ ] Validation script: 100% pass (10/10 rules)
- [ ] Knowledge note documenting L1 adoption experience
- [ ] A-MEM event emitted for SAP-056 L1 adoption

**Time Invested**: 2-4 hours
**Next**: Proceed to L2 (5+ features)

---

## 4. L1 → L2: Configured (5+ Features)

**Goal**: Extend manifest to 5+ features, add frontmatter to docs systematically

**Time**: 8-12 hours

**Success Criteria**:
- [ ] ≥5 features in manifest
- [ ] Features→Requirements linkage for all features
- [ ] Frontmatter in ≥50% of docs
- [ ] Validation pass rate ≥80%

### Step 1: Identify Next 4 Features

**Time**: 30 minutes

**Actions**:

1. **Review project history**:
   ```bash
   # List recent features from git log:
   git log --oneline --since="6 months ago" | grep -i "feat:"

   # List recent beads tasks:
   bd list --status closed | head -20
   ```

2. **Select 4 more features**:
   - Mix of recently completed + older features
   - Vary complexity (simple, medium, complex)
   - Different domains (backend, frontend, docs, scripts)

**Example Selection**:
- FEAT-002: Backend API versioning (medium complexity)
- FEAT-003: Documentation site generator (simple)
- FEAT-004: CI/CD pipeline (complex)
- FEAT-005: Error handling framework (medium)

---

### Step 2: Create Feature Entries

**Time**: 4-6 hours (1 hour per feature)

**Actions**:

1. **For each feature**, add entry to feature-manifest.yaml:
   - Define 1-3 requirements
   - List code files (use git log for hints)
   - List tests (search test files for feature-specific tests)
   - List docs (search docs/ for feature mentions)

2. **Use template** (templates/feature-manifest-entry.j2):
   ```yaml
   - id: FEAT-00X
     name: "Feature Name"
     description: "Brief description"
     vision_ref: "CHARTER-001:Outcome-X"
     status: implemented  # or in_progress, planned
     created: "YYYY-MM-DD"
     completed: "YYYY-MM-DD"  # if implemented

     requirements:
       - id: REQ-00X
         description: "Requirement description"
         acceptance_criteria:
           - "Criterion 1"
           - "Criterion 2"

     code:
       - path: src/module.py

     tests:
       - path: tests/test_module.py::test_case
         type: unit
         requirement: REQ-00X

     documentation:
       - path: docs/how-to/feature.md
         type: how-to
         audience: users
   ```

3. **Validate incrementally**:
   ```bash
   # After each feature addition:
   python scripts/validate-traceability.py --feature FEAT-00X
   ```

---

### Step 3: Add Frontmatter to Docs

**Time**: 2-3 hours

**Actions**:

1. **Identify docs without frontmatter**:
   ```bash
   # Find docs missing frontmatter:
   for doc in docs/**/*.md; do
     if ! head -1 "$doc" | grep -q "^---$"; then
       echo "$doc"
     fi
   done
   ```

2. **Add frontmatter to ≥50% of docs**:
   - Prioritize how-tos and tutorials first
   - Reference docs second
   - Conceptual docs last

3. **Template**:
   ```yaml
   ---
   title: "Doc Title"
   type: how-to | tutorial | reference | explanation
   feature_id: FEAT-XXX
   code_references:
     - src/file.py
   test_references:
     - tests/test_file.py::test_name
   last_updated: "YYYY-MM-DD"
   ---
   ```

---

### Step 4: Add Pytest Markers Systematically

**Time**: 1-2 hours

**Actions**:

1. **Create migration script** (or manual):
   ```bash
   # Find tests without markers:
   grep -r "^def test_" tests/ | grep -v "@pytest.mark.feature"
   ```

2. **Add markers to all tests**:
   - Infer feature from file path or test name
   - Add `@pytest.mark.feature("FEAT-XXX")`
   - Add `@pytest.mark.requirement("REQ-XXX")`
   - Add `@pytest.mark.unit | .integration | .e2e`

3. **Validate coverage**:
   ```bash
   pytest --collect-only | grep "@pytest.mark.feature" | wc -l
   # → Should show significant count
   ```

---

### Step 5: Run Full Validation

**Time**: 30 minutes

**Actions**:

1. **Validate all features**:
   ```bash
   python scripts/validate-traceability.py --output validation-report.md
   ```

2. **Review failures**:
   - Target: ≥80% pass rate
   - Fix high-impact failures first (Rule 3: Evidence, Rule 8: Requirement Coverage)
   - Defer low-impact failures (Rule 10: Event Correlation)

3. **Iterate until ≥80% pass**

---

### Step 6: Create Justfile Helpers

**Time**: 1 hour

**Actions**:

1. **Add recipes to justfile**:
   ```bash
   # justfile

   # Validate traceability
   validate-trace:
       python scripts/validate-traceability.py --output validation-report.md
       @echo "Report: validation-report.md"

   # Validate specific feature
   validate-feature FEATURE_ID:
       python scripts/validate-traceability.py --feature {{FEATURE_ID}}

   # Query manifest
   query-feature FEATURE_ID:
       python scripts/query-manifest.py feature {{FEATURE_ID}}

   query-requirement REQ_ID:
       python scripts/query-manifest.py requirement {{REQ_ID}}
   ```

2. **Test recipes**:
   ```bash
   just validate-trace
   just query-feature FEAT-001
   ```

---

### L2 Validation Checklist

- [ ] ≥5 features in feature-manifest.yaml
- [ ] All features have requirements defined (≥1 requirement per feature)
- [ ] Frontmatter added to ≥50% of documentation files
- [ ] Pytest markers on ≥80% of tests
- [ ] Validation pass rate ≥80% (8+/10 rules passing)
- [ ] Justfile helpers for validation and querying
- [ ] Knowledge note documenting L2 adoption challenges/learnings
- [ ] A-MEM event emitted for SAP-056 L2 elevation

**Time Invested**: 8-12 hours (cumulative: 10-16 hours)
**Next**: Proceed to L3 (100% coverage)

---

## 5. L2 → L3: Active (100% Coverage)

**Goal**: Achieve 100% traceability coverage with automated enforcement

**Time**: 20-30 hours

**Success Criteria**:
- [ ] All features in manifest
- [ ] Git commits link to tasks (`[.beads-XXX]` suffix)
- [ ] Tasks link to features (`[Feature: FEAT-XXX]` prefix)
- [ ] Validation pass rate 100% (10/10 rules)
- [ ] Pre-commit hooks enforce linkage

### Step 1: Complete Feature Manifest

**Time**: 10-15 hours

**Actions**:

1. **Add ALL remaining features**:
   - Historical features (from git history)
   - Current in-progress features
   - Deprecated features (status=deprecated)

2. **For each feature**:
   - Define requirements exhaustively
   - List all code files (use `git log --follow`)
   - List all tests (grep test files)
   - List all docs (grep docs directory)

3. **Validate incrementally** (every 5 features):
   ```bash
   just validate-trace
   ```

---

### Step 2: Frontmatter on ALL Docs

**Time**: 3-5 hours

**Actions**:

1. **Identify remaining docs**:
   ```bash
   # Find docs without frontmatter:
   python scripts/find-docs-without-frontmatter.py
   ```

2. **Add frontmatter to all**:
   - How-tos, tutorials, references → feature_id + code_references
   - Conceptual docs (vision, ADRs) → mark as conceptual (no code_references required)

3. **Validation**:
   ```bash
   python scripts/validate-traceability.py --rule 9
   # → Documentation Coverage: 100%
   ```

---

### Step 3: Pytest Markers on ALL Tests

**Time**: 2-4 hours

**Actions**:

1. **Find unmarked tests**:
   ```bash
   pytest --collect-only | grep -v "@pytest.mark.feature"
   ```

2. **Add markers to remaining tests**

3. **Validate requirement coverage**:
   ```bash
   python scripts/validate-traceability.py --rule 8
   # → Requirement Coverage: 100%
   ```

---

### Step 4: Git Commit Linkage

**Time**: 2-3 hours

**Actions**:

1. **Install pre-commit hook**:
   ```bash
   # .git/hooks/prepare-commit-msg
   #!/bin/bash
   commit_msg_file=$1
   commit_msg=$(cat "$commit_msg_file")

   if ! echo "$commit_msg" | grep -q "\[\.beads-"; then
       # Extract task ID from branch name
       branch=$(git branch --show-current)
       if [[ $branch =~ \.beads-[a-z0-9]+ ]]; then
           task_id=$(echo "$branch" | grep -o '\.beads-[a-z0-9]*')
           echo "# Suggested task ID: [$task_id]" >> "$commit_msg_file"
       fi
   fi
   ```

2. **Make executable**:
   ```bash
   chmod +x .git/hooks/prepare-commit-msg
   ```

3. **Test hook**:
   ```bash
   git commit --dry-run
   # → Should suggest task ID
   ```

4. **Document convention** in CONTRIBUTING.md:
   ```markdown
   ## Commit Message Format

   ```
   <type>(<scope>): <description> [<task-id>]
   ```

   Example:
   ```
   feat(auth): add OAuth2 [.beads-abc123]
   ```
   ```

---

### Step 5: Task→Feature Linkage

**Time**: 1-2 hours

**Actions**:

1. **Update ALL beads tasks** to include `[Feature: FEAT-XXX]` prefix:
   ```bash
   # For each task:
   bd update .beads-abc123 --title "[Feature: FEAT-001] Original title"
   ```

2. **Validate linkage**:
   ```bash
   python scripts/validate-traceability.py --rule 4
   # → Closed Loop: 100%
   ```

---

### Step 6: Achieve 100% Validation Pass

**Time**: 2-4 hours (iterative fixing)

**Actions**:

1. **Run full validation**:
   ```bash
   python scripts/validate-traceability.py --verbose
   ```

2. **Fix ALL failures**:
   - Broken file paths → Update or remove
   - Missing bidirectional links → Add reverse linkage
   - Orphaned artifacts → Add to manifest or mark deprecated
   - Missing tests/docs → Create or mark feature as in_progress

3. **Re-validate until 100%**:
   ```
   Overall Pass Rate: 100% (120/120 checks)
   ```

---

### L3 Validation Checklist

- [ ] ALL features in feature-manifest.yaml (nothing orphaned)
- [ ] Frontmatter on 100% of docs (or marked as conceptual)
- [ ] Pytest markers on 100% of tests
- [ ] Pre-commit hook installed (suggests task IDs)
- [ ] ALL beads tasks have `[Feature: FEAT-XXX]` prefix
- [ ] Validation pass rate: 100% (10/10 rules, all features)
- [ ] Query time <1 minute ("which code implements REQ-X?")
- [ ] Knowledge note documenting L3 adoption effort and ROI
- [ ] A-MEM event emitted for SAP-056 L3 elevation

**Time Invested**: 20-30 hours (cumulative: 30-46 hours)
**Next**: Proceed to L4 (automation + metrics)

---

## 6. L3 → L4: Community (Automation + Metrics)

**Goal**: Automate enforcement via CI/CD, publish metrics, enable community adoption

**Time**: 40-60 hours

**Success Criteria**:
- [ ] CI/CD validates traceability on every PR
- [ ] Pre-commit hooks block incomplete linkage
- [ ] Traceability metrics dashboard (HTML + JSON)
- [ ] Knowledge notes documenting patterns
- [ ] 3+ downstream projects adopt SAP-056

### Step 1: CI/CD Integration

**Time**: 4-6 hours

**Actions**:

1. **Create GitHub Actions workflow** (.github/workflows/traceability.yml):
   ```yaml
   name: Traceability Validation

   on: [pull_request, push]

   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         - name: Validate Traceability
           run: |
             python scripts/validate-traceability.py --output validation-report.md
             # Fail if <100% pass rate
             if grep -q "Pass Rate.*100%" validation-report.md; then
               echo "✓ Traceability validation passed"
               exit 0
             else
               echo "✗ Traceability validation failed"
               cat validation-report.md
               exit 1
             fi
   ```

2. **Test workflow**:
   - Create PR with broken linkage
   - Verify CI fails
   - Fix linkage
   - Verify CI passes

---

### Step 2: Enhanced Pre-commit Hooks

**Time**: 2-3 hours

**Actions**:

1. **Block commits with broken linkage**:
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash

   # Run validation
   python scripts/validate-traceability.py --changed-only > /tmp/validation.txt

   if grep -q "FAIL" /tmp/validation.txt; then
       echo "✗ Traceability validation failed:"
       cat /tmp/validation.txt
       echo ""
       echo "Fix linkage before committing or use --no-verify to skip"
       exit 1
   fi

   echo "✓ Traceability validation passed"
   exit 0
   ```

2. **Make executable**:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

---

### Step 3: Metrics Dashboard

**Time**: 10-15 hours

**Actions**:

1. **Create dashboard script** (scripts/traceability-dashboard.py):
   - Feature coverage: % features in manifest
   - Linkage completeness: % features with all linkages
   - Validation trends: Pass rate over time
   - Top features by code size, test coverage, doc completeness
   - Orphaned artifacts count

2. **Generate HTML dashboard**:
   ```bash
   python scripts/traceability-dashboard.py --output dashboard.html
   ```

3. **Publish to GitHub Pages** (or internal wiki)

4. **Automate monthly reports**:
   ```yaml
   # .github/workflows/monthly-report.yml
   on:
     schedule:
       - cron: '0 0 1 * *'  # 1st of each month

   jobs:
     report:
       steps:
         - name: Generate Dashboard
           run: python scripts/traceability-dashboard.py --output dashboard.html
         - name: Publish to Pages
           uses: peaceiris/actions-gh-pages@v3
   ```

---

### Step 4: Knowledge Documentation

**Time**: 8-12 hours

**Actions**:

1. **Create 3+ knowledge notes**:
   - `.chora/memory/knowledge/notes/traceability-patterns.md` - Common linkage patterns
   - `.chora/memory/knowledge/notes/traceability-antipatterns.md` - What NOT to do
   - `.chora/memory/knowledge/notes/traceability-roi.md` - ROI calculation from adoption

2. **Document traceability in CONTRIBUTING.md**:
   ```markdown
   ## Traceability Requirements

   All changes MUST maintain traceability:
   1. Features in feature-manifest.yaml
   2. Tests with @pytest.mark.feature markers
   3. Docs with feature_id frontmatter
   4. Commits with [.beads-XXX] suffix
   5. Beads tasks with [Feature: FEAT-XXX] prefix

   Validation: `just validate-trace`
   ```

---

### Step 5: Enable Community Adoption

**Time**: 16-24 hours

**Actions**:

1. **Create adoption guide** for downstream projects:
   - How-to for new projects adopting SAP-056
   - Template feature-manifest.yaml
   - Copy validation scripts
   - Copy pre-commit hooks

2. **Pilot in 3 downstream projects**:
   - chora-base (dogfooding)
   - chora-compose (template generation)
   - chora-workspace (full adoption)

3. **Update SAP-056 ledger** with adopter tracking

4. **Present at team meeting** (ROI, lessons learned)

---

### L4 Validation Checklist

- [ ] CI/CD workflow validates traceability on every PR/push
- [ ] Pre-commit hooks block commits with broken linkage (configurable)
- [ ] Traceability metrics dashboard generated monthly (HTML + JSON)
- [ ] ≥3 knowledge notes documenting patterns, antipatterns, ROI
- [ ] CONTRIBUTING.md includes traceability requirements
- [ ] ≥3 downstream projects adopting SAP-056 (L1+)
- [ ] Monthly traceability report published (metrics trends)
- [ ] Presentation delivered to team (ROI, lessons learned)
- [ ] A-MEM event emitted for SAP-056 L4 elevation

**Time Invested**: 40-60 hours (cumulative: 70-106 hours)
**ROI**: ~100+ hours saved annually per project (break-even: 6-8 months)

---

## 7. Troubleshooting

### Issue: Validation Script Fails to Run

**Symptom**: `ModuleNotFoundError: No module named 'yaml'`

**Solution**:
```bash
pip install pyyaml jsonschema
```

---

### Issue: High False Positive Rate

**Symptom**: Validation reports many failures for valid linkages

**Solution**:
- Review validation rules in protocol-spec.md
- Check file paths (relative vs absolute)
- Verify YAML syntax in frontmatter
- Update validation script if rules too strict

---

### Issue: Pre-commit Hook Too Slow

**Symptom**: Commit takes >30 seconds due to validation

**Solution**:
- Use `--changed-only` flag in validation script
- Cache parsed manifest
- Run full validation in CI only, pre-commit does incremental

---

### Issue: Team Resistance to Adoption

**Symptom**: Developers complain about "too much process"

**Solution**:
- Show ROI (time saved in context restoration, impact analysis)
- Use git hooks for automation (minimal manual work)
- Start with L1 (1 feature) to demonstrate value
- Highlight compliance benefits (audits, onboarding)

---

## 8. Version History

**1.0.0** (2025-11-16): Initial adoption blueprint
- L0→L4 progression (4 maturity levels)
- Detailed steps with time estimates
- Validation checklists per level
- Troubleshooting guide
