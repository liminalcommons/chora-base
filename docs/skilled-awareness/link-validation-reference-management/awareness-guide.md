# Link Validation & Reference Management
## Awareness Guide

**SAP ID**: SAP-016
**Audience**: Developers, Documentation Authors, CI/CD Engineers
**Reading Time**: 15 minutes

---

## What This SAP Does

**Link validation ensures every reference in your documentation actually works.**

When you write documentation with links:
```markdown
See the [Architecture Guide](../../ARCHITECTURE.md) for details.
Check out [SAP-007](../documentation-framework/awareness-guide.md).
External reference: [Diátaxis Framework](https://diataxis.fr/)
```

This SAP automatically:
- ✅ Verifies `ARCHITECTURE.md` exists at that path
- ✅ Verifies `awareness-guide.md` exists in `documentation-framework/`
- ✅ Checks `https://diataxis.fr/` is reachable
- ❌ Reports broken links before users encounter them

**Why this matters**:
- Broken links waste developer time (2-4 hours per month tracking down references)
- Documentation with broken links loses user trust
- File refactors often break references across multiple files
- External resources move or disappear over time

---

## When to Use This SAP

### Use Link Validation When:

**1. Restructuring Documentation**
- Moving files between directories (like Wave 1's 4-domain migration)
- Renaming files or directories
- Consolidating or splitting documentation

**Example**: Wave 1 moved 279 files across 4 domains - link validation caught all broken references.

**2. Before Releasing**
- Validating release documentation
- Ensuring user-facing docs are complete
- Quality gate before tagging releases

**Example**: Wave 2 release requires 100% link validation pass.

**3. In CI/CD Pipelines**
- Block pull requests with broken links
- Prevent broken references from reaching main branch
- Automate documentation quality checks

**Example**: GitHub Actions workflow fails PR if link validation fails.

**4. Auditing Existing Documentation**
- Periodic health checks (monthly or quarterly)
- Identifying link rot in long-lived docs
- Finding references to moved or deleted content

**Example**: External link health check runs weekly, reports degraded links.

**5. During SAP Audits**
- Step 3 of SAP Audit Workflow
- Ensuring cross-domain references are valid
- Validating awareness-guide.md references work

**Example**: Each of 15 SAPs audited with link validation in Wave 2.

### Don't Use Link Validation For:

❌ **Code comments** - Too noisy, often hypothetical examples
❌ **Commit messages** - Historical, immutable
❌ **Draft documentation** - Work-in-progress, links not finalized
❌ **Content quality** - Use SAP audit workflow instead
❌ **Spell checking** - Different tool (markdownlint, aspell)

---

## How to Use This SAP

### Quick Start (5 Minutes)

**1. Validate a single file**:
```bash
./scripts/validate-links.sh docs/ARCHITECTURE.md
```

**Output**:
```
✅ Link Validation Report

Scanned: 1 file
Total links: 23 links
  - Internal: 21 (100% valid)
  - External: 2 (100% valid)

Status: PASS ✅
Runtime: 3 seconds
```

**2. Validate a directory** (e.g., single SAP):
```bash
./scripts/validate-links.sh docs/skilled-awareness/sap-framework/
```

**3. Validate entire repository**:
```bash
./scripts/validate-links.sh .
```

**4. Validate only changed files** (git required):
```bash
./scripts/validate-links.sh --mode changed
```

### Understanding the Output

**Success (Exit Code 0)**:
```
✅ Link Validation Report

Scanned: 127 markdown files
Total links: 1,543 links
  - Internal: 1,401 (100% valid)
  - External: 142 (98% valid, 3 warnings)

Status: PASS ✅

Warnings:
  - docs/foo.md:42 → https://example.com (timeout, may be temporary)

Runtime: 47 seconds
```

**What to do**: Nothing! All links are valid. Warnings are non-blocking (temporary network issues).

---

**Failure (Exit Code 1)**:
```
❌ Link Validation Report

Scanned: 127 markdown files
Total links: 1,543 links
  - Internal: 1,401 (3 broken)
  - External: 142 (2 broken, 3 warnings)

Status: FAIL ❌

Broken Links:
  1. docs/skilled-awareness/sap-framework/awareness-guide.md:89
     → ../../dev-docs/workflows/missing-workflow.md
     ERROR: File does not exist

  2. README.md:23
     → https://deadlink.example.com/page
     ERROR: 404 Not Found

Runtime: 51 seconds
```

**What to do**:
1. Open the file listed (`awareness-guide.md`)
2. Go to line 89
3. Fix the broken link:
   - Update path to correct location
   - Remove link if target no longer exists
   - Create missing file if it should exist

---

### Advanced Usage

**Disable external link checking** (faster, for local validation):
```bash
./scripts/validate-links.sh --no-external .
```

**Output as JSON** (for scripting):
```bash
./scripts/validate-links.sh --format json . > link-report.json
```

**Ignore specific patterns** (exclude drafts, dependencies):
```bash
./scripts/validate-links.sh --ignore "*.draft.md" --ignore "node_modules/*" .
```

**Fail fast** (stop on first broken link):
```bash
./scripts/validate-links.sh --fail-fast .
```

**Custom timeout** (for slow networks):
```bash
./scripts/validate-links.sh --timeout 30 .
```

---

## Integration Examples

### Git Pre-Commit Hook

**Validate changed files before committing**:

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash

# Validate links in staged markdown files
CHANGED_MD_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ -n "$CHANGED_MD_FILES" ]; then
  echo "Validating links in changed markdown files..."

  for file in $CHANGED_MD_FILES; do
    ./scripts/validate-links.sh "$file" || exit 1
  done

  echo "✅ All links valid"
fi

exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

**Result**: Cannot commit broken links.

---

### GitHub Actions CI/CD

**Block PRs with broken links**:

Create `.github/workflows/link-validation.yml`:
```yaml
name: Link Validation

on:
  pull_request:
    paths:
      - '**.md'

jobs:
  validate-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate Markdown Links
        run: |
          chmod +x scripts/validate-links.sh
          ./scripts/validate-links.sh .

      - name: Comment on PR (if failed)
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Link validation failed. Please fix broken links before merging.'
            })
```

**Result**: PRs cannot merge with broken links.

---

### Periodic External Link Health Check

**Weekly cron job to detect link rot**:

Create `.github/workflows/weekly-link-check.yml`:
```yaml
name: Weekly Link Health Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC

jobs:
  check-external-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate External Links
        run: |
          chmod +x scripts/validate-links.sh
          ./scripts/validate-links.sh --format json . > link-report.json

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: link-health-report
          path: link-report.json

      - name: Notify Team (if warnings)
        if: failure()
        run: |
          # Send Slack notification or create GitHub issue
          echo "External link health check found issues"
```

**Result**: Team notified of link degradation before users encounter broken links.

---

### SAP Audit Workflow Integration

**Step 3 of SAP Audit (from SAP Audit Workflow)**:

```bash
# Run link validation on SAP directory
./scripts/validate-links.sh docs/skilled-awareness/[sap-name]/

# Review report
# - Critical: Internal broken links → Must fix
# - High: External 404s → Should fix
# - Warning: External timeouts → Note for monitoring
```

**See**: [SAP Audit Workflow - Step 3](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md#step-3-run-link-validation-30-minutes)

---

## Cross-Domain Integration

This SAP validates references across all 4 chora-base domains:

### Developer Process (dev-docs/)

**Workflow References**:
```markdown
<!-- In awareness-guide.md -->
**Developer Workflows**:
- [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) - Uses link validation in Step 3
- [Documentation Migration Workflow](../../dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) - Run link validation after file moves
```

**Link validation ensures**:
- SAP awareness-guides reference valid workflows
- Workflows reference valid examples
- Examples reference actual system files

---

### Project Lifecycle (project-docs/)

**Sprint Planning References**:
```markdown
<!-- In awareness-guide.md -->
**Project Tracking**:
- [Wave 2 Sprint Plan](../../project-docs/sprints/wave-2-sprint-plan.md) - Link validation in Phase 1
```

**Link validation ensures**:
- Sprint plans reference valid release notes
- Metrics reference actual data files
- Integration plans reference valid architecture docs

---

### Product Documentation (user-docs/)

**User-Facing Guides**:
```markdown
<!-- In awareness-guide.md -->
**User Documentation**:
- [How to Write Executable Documentation](../../user-docs/how-to/write-executable-documentation.md) - References link validation
- [Benefits of chora-base](../../user-docs/explanation/benefits-of-chora-base.md) - Quality assurance mention
```

**Link validation ensures**:
- How-to guides reference valid tutorials
- Tutorials reference working examples
- Reference docs link to actual system files

---

### System Files

**Validation Script**:
- `scripts/validate-links.sh` - Core implementation (see Adoption Blueprint)

**CI/CD Integration**:
- `.github/workflows/link-validation.yml` - GitHub Actions example
- `.gitlab-ci.yml` - GitLab CI example (in adoption-blueprint.md)

**Link validation ensures**:
- Documentation references scripts that exist
- Scripts referenced in multiple SAPs are found
- CI/CD workflows reference valid configuration files

---

## Common Pitfalls

### Pitfall 1: Relative Path Confusion

**Symptom**: Link works in file but validation reports broken.

**Example**:
```markdown
<!-- File: docs/skilled-awareness/sap-framework/awareness-guide.md -->
[Workflow](../workflows/foo.md)  ❌ BROKEN
```

**Cause**: Relative path is from current file, not from repository root.

**Solution**:
```markdown
<!-- Correct relative path -->
[Workflow](../../dev-docs/workflows/foo.md)  ✅ WORKS

<!-- Or use absolute from repo root -->
[Workflow](/docs/dev-docs/workflows/foo.md)  ✅ WORKS
```

**Prevention**: Always test links after writing them.

---

### Pitfall 2: Anchor Links to Renamed Sections

**Symptom**: File exists but anchor link fails.

**Example**:
```markdown
[See Security](./protocol-spec.md#security-considerations)  ❌ BROKEN
```

**Cause**: Section was renamed from "Security Considerations" to "Security".

**Solution**: Update anchor to match new section:
```markdown
[See Security](./protocol-spec.md#security)  ✅ WORKS
```

**Prevention**: Search destination file for section headings before linking.

**Note**: Anchor validation requires content parsing (coming in v2.0).

---

### Pitfall 3: External Link Changes

**Symptom**: External link worked yesterday, broken today.

**Example**:
```markdown
[Old Docs](https://example.com/docs/v1/guide)  ❌ 404
```

**Cause**: External resource moved or was deleted.

**Solution**: Update to new URL or remove link:
```markdown
[New Docs](https://example.com/docs/v2/guide)  ✅ WORKS
```

**Prevention**:
- Use permalink URLs when available (e.g., GitHub blob URLs with commit hash)
- Monitor external links with weekly health checks
- Document critical external dependencies

---

### Pitfall 4: Case-Sensitive File Systems

**Symptom**: Link works on macOS/Windows but fails on Linux CI.

**Example**:
```markdown
<!-- File is README.md, but linked as: -->
[See Readme](./readme.md)  ❌ BROKEN (on Linux)
```

**Cause**: macOS/Windows are case-insensitive, Linux is case-sensitive.

**Solution**: Match exact file name:
```markdown
[See Readme](./README.md)  ✅ WORKS (all platforms)
```

**Prevention**: Run link validation in CI (Linux environment) to catch these.

---

### Pitfall 5: Forgetting to Update After File Moves

**Symptom**: Moved file but didn't update references.

**Example**:
```markdown
<!-- Before Wave 1: -->
[Benefits](./docs/BENEFITS.md)  ✅ WORKS

<!-- After Wave 1 migration: -->
[Benefits](./docs/BENEFITS.md)  ❌ BROKEN (file moved to user-docs/)
```

**Cause**: File moved, references not updated.

**Solution**: Run link validation after migrations:
```bash
# Wave 1 example:
mv docs/BENEFITS.md docs/user-docs/explanation/benefits-of-chora-base.md

# Update references:
sed -i '' 's|docs/BENEFITS.md|docs/user-docs/explanation/benefits-of-chora-base.md|g' README.md

# Validate:
./scripts/validate-links.sh .
```

**Prevention**:
- Use link validation in CI (catches missed updates)
- Run validation immediately after file moves
- Update references before committing moves

---

## Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-016 --source /path/to/chora-base
```

This will automatically install:
- SAP-016 (Link Validation & Reference Management)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `minimal-entry` - 5 essential SAPs for quick ecosystem onboarding
- `recommended` - 10 SAPs covering core development workflows
- `testing-focused` - 6 SAPs emphasizing testing and quality
- `mcp-server` - 10 SAPs for building MCP servers
- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Dependencies

This SAP has no dependencies.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/link-validation-reference-management/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

# Verify link validation script exists
ls scripts/validate-links.sh
# Should exist and be executable
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## Related Content

This SAP integrates with content across all 4 domains:

### Developer Process (dev-docs/)

**Workflows**:
- [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) - Uses link validation in Step 3
- [Documentation Migration Workflow](../../dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) - Validation after file moves

**Examples** (to be created in Phase 5):
- `dev-docs/examples/link-validation-in-ci.md` - GitHub Actions integration example
- `dev-docs/examples/pre-commit-link-check.md` - Git hook setup walkthrough

### Project Lifecycle (project-docs/)

**Planning**:
- [Wave 2 Sprint Plan](../../project-docs/sprints/wave-2-sprint-plan.md) - SAP-016 creation in Phase 1

**Metrics** (to be created in Phase 5):
- `project-docs/metrics/link-validation-metrics.md` - Track link health over time

### Product Documentation (user-docs/)

**How-To Guides**:
- [How to Write Executable Documentation](../../user-docs/how-to/write-executable-documentation.md) - References link validation

**Reference** (to be created in Phase 5):
- `user-docs/reference/link-validation-cli.md` - Complete CLI reference

### System Files

**Scripts**:
- `scripts/validate-links.sh` - Core validation script (see adoption-blueprint.md)

**CI/CD**:
- `.github/workflows/link-validation.yml` - GitHub Actions workflow (example in adoption-blueprint.md)

### Skilled Awareness (SAPs)

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/awareness-guide.md) - SAP structure this SAP follows
- [SAP-007: Documentation Framework](../documentation-framework/awareness-guide.md) - Enhanced by link validation
- [SAP-006: Quality Gates](../quality-gates/awareness-guide.md) - Integrates link validation as quality criterion

---

## Measuring Success

### For chora-base (Wave 2)

**Quantitative Metrics**:
- ✅ 100% of 279 files validated
- ✅ All 15 SAPs pass link validation
- ✅ Zero broken internal links in v3.4.0 release
- ✅ Link validation runtime <2 minutes for full repository

**Qualitative Indicators**:
- Developers report confidence in documentation references
- SAP audits complete faster (Step 3 automated)
- External adopters report high documentation quality

### For External Projects

**Adoption Indicators**:
- Link validation script included in cloned projects
- CI/CD pipeline runs link validation
- At least 1 external project reports catching broken links before release

**Impact Metrics**:
- Time saved: 2-4 hours per developer per month
- User trust: Measurable through documentation usage analytics
- Maintenance cost: Reduced documentation debt

---

## Frequently Asked Questions

**Q: How long does link validation take?**
A: ~1 minute for 200 files, ~2 minutes for 500 files. Single file validation takes <2 seconds.

**Q: Does link validation modify any files?**
A: No, it's read-only. It only reports broken links, does not fix them automatically.

**Q: What if external link is temporarily down?**
A: Marked as WARNING (not ERROR). Warnings don't fail validation. Re-run to confirm persistent issues.

**Q: Can I validate links in code comments?**
A: Not in v1.0 (too noisy). Markdown files only. Future enhancement possible.

**Q: Does it validate image links?**
A: Not in v1.0. Image asset validation is a separate future enhancement.

**Q: What if I have intentionally broken links (examples, templates)?**
A: Use `--ignore` flag to exclude specific files or patterns.

**Q: Can I validate anchor links within the same document?**
A: Not in v1.0 (requires content parsing). Coming in v2.0.

**Q: How do I integrate with CI systems other than GitHub Actions?**
A: Use the bash script directly. Exits with code 0 (pass) or 1 (fail). See adoption-blueprint.md for GitLab CI, Jenkins examples.

---

## Next Steps

**If you're new to link validation**:
1. Read the [Adoption Blueprint](./adoption-blueprint.md) for installation
2. Run your first validation: `./scripts/validate-links.sh .`
3. Review the output, fix any broken links
4. Set up CI/CD integration (examples in adoption-blueprint.md)

**If you're auditing SAPs**:
1. Follow [SAP Audit Workflow - Step 3](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md#step-3-run-link-validation-30-minutes)
2. Run validation on SAP directory
3. Document broken links in gap report
4. Fix critical issues (blocking SAP usage)

**If you're releasing a version**:
1. Run full repository validation: `./scripts/validate-links.sh .`
2. Ensure 100% pass (zero errors)
3. Address warnings (external link issues)
4. Include link validation report in release notes

---

**SAP Version**: 1.0
**Created**: 2025-10-28 (Wave 2)
**Status**: Active

This awareness guide demonstrates chora-base's skilled-awareness/ domain: comprehensive "how to use" documentation for a portable capability package.
