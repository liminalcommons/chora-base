# Link Validation & Reference Management
## Capability Charter

**SAP ID**: SAP-016
**Category**: Quality Assurance
**Maturity**: Initial (v1.0)
**Created**: 2025-10-28 (Wave 2)

---

## Business Value

Documentation without valid links is a broken promise. A single broken reference can block a user's entire workflow, waste hours of developer time, and erode trust in the entire documentation system.

**Link validation transforms documentation from "hopefully works" to "guaranteed accurate".**

This SAP provides:
- **Automated link integrity checking** - Catch broken references before they reach users
- **Cross-domain validation** - Ensure 4-domain architecture references are valid
- **CI/CD integration** - Block merges that introduce broken links
- **Adoption tracking** - Verify external projects maintain valid references

**ROI Measurement**:
- **Time saved**: 2-4 hours per developer per month (eliminating "link hunting")
- **Trust increase**: Measurable through documentation usage metrics
- **Quality gates**: 100% link validity as release criterion

---

## Problem Statement

**Without systematic link validation**:
- ❌ Broken internal links (documentation refactors break references)
- ❌ Broken external links (third-party resources move or disappear)
- ❌ Ambiguous relative paths (work locally but fail in production)
- ❌ Missing anchor links (sections renamed, fragment identifiers outdated)
- ❌ Cross-domain reference failures (4-domain architecture changes break links)

**Real impact**:
- Wave 1 created 279 files across 4 domains - manual link checking would take 8+ hours
- 14 SAPs reference content across dev-docs/, project-docs/, user-docs/, system files
- External adopters clone chora-base - broken links undermine credibility

**The gap**: No automated way to validate all markdown references in the repository.

---

## Capability Scope

### In Scope

**Link Types Validated**:
- ✅ Internal markdown links (relative paths: `../foo.md`, `./bar.md`)
- ✅ Absolute repository paths (`/docs/foo.md`)
- ✅ Anchor links within documents (`#section-name`)
- ✅ Cross-document anchor links (`../foo.md#section`)
- ✅ External HTTP/HTTPS links (basic reachability check)
- ✅ File references in code blocks (when explicitly marked)

**Documentation Types Covered**:
- ✅ All markdown files (`.md`)
- ✅ README files
- ✅ Documentation in all 4 domains
- ✅ SAP artifacts (all 15 SAPs)
- ✅ System documentation (AGENTS.md, CONTRIBUTING.md, etc.)

**Validation Modes**:
- ✅ Full repository scan (all markdown files)
- ✅ Directory-specific scan (e.g., single SAP)
- ✅ Single file validation
- ✅ Changed files only (CI/CD optimization)

### Out of Scope

**Not Validated**:
- ❌ Links in code comments (too noisy, often intentionally hypothetical)
- ❌ Links in commit messages (historical, immutable)
- ❌ Image files (separate image asset validation needed)
- ❌ Deep external link validation (checking for 200 OK vs 404 is sufficient)
- ❌ External link content freshness (we check reachability, not accuracy)

**Intentionally Excluded**:
- ❌ Spell checking (separate concern)
- ❌ Markdown linting (separate tool: markdownlint)
- ❌ Content quality (separate: SAP audit workflow)

---

## Outcomes & Guarantees

### Guaranteed Outcomes

When this SAP is fully adopted:

1. **100% internal link validity** - Zero broken references within repository
2. **External link baseline** - All external links reachable at validation time
3. **CI/CD quality gate** - Pull requests cannot merge with broken links
4. **Refactor safety** - File moves automatically caught by CI/CD
5. **Cross-domain integrity** - 4-domain architecture references validated

### Measurable Success Criteria

**For chora-base itself** (Wave 2):
- [ ] All 279 files validated (100% coverage)
- [ ] All 15 SAPs pass link validation
- [ ] CI/CD workflow enforces link validation on PRs
- [ ] Wave 2 release has zero broken internal links

**For external adopters**:
- [ ] Link validation script included in cloned projects
- [ ] Documentation references validation in quality checklist
- [ ] At least 1 external project reports successful link validation

**Quality Metrics**:
- Link validation runtime: <60 seconds for full repository scan
- False positive rate: <5% (minimize noise)
- CI/CD overhead: <30 seconds added to pipeline

---

## Adoption Prerequisites

**Required**:
- Bash shell (Linux, macOS, or WSL on Windows)
- `grep` (standard on all Unix-like systems)
- `curl` or `wget` (for external link checking)
- Markdown documentation (`.md` files)

**Recommended**:
- Git repository (for changed-files-only validation)
- CI/CD system (GitHub Actions, GitLab CI, etc.)
- Pre-commit hooks support

**Optional**:
- `jq` (for JSON output parsing)
- Slack/Discord webhook (for validation failure notifications)

---

## Integration Points

### Cross-Domain Integration

**dev-docs/**:
- Validates workflows reference valid system files
- Checks examples reference existing code

**project-docs/**:
- Validates sprint plans link to valid releases
- Checks metrics reference actual data files

**user-docs/**:
- Validates how-to guides reference valid workflows
- Checks tutorials link to working examples

**skilled-awareness/**:
- Validates all SAP cross-references (5 artifacts × 15 SAPs)
- Ensures awareness-guides reference valid dev-docs/, user-docs/, system files

### System Integration

**Git Hooks**:
- Pre-commit: Validate changed files only (fast feedback)
- Pre-push: Full validation (comprehensive check)

**CI/CD Pipelines**:
- GitHub Actions: `.github/workflows/link-validation.yml`
- GitLab CI: `.gitlab-ci.yml` job
- Other systems: Integrate via bash script

**Quality Gates**:
- Block PR merge if validation fails
- Mark releases as "not ready" if links broken
- Alert team via Slack/Discord on CI failures

---

## Key Constraints & Assumptions

### Constraints

1. **Markdown-only focus**: This SAP validates markdown links, not HTML or other formats
2. **Repository-relative paths**: Assumes documentation lives in a git repository
3. **Static analysis**: Link validation is syntax-based, not runtime execution
4. **External link limitations**: We check reachability, not content correctness

### Assumptions

1. **Standard markdown syntax**: Assumes CommonMark-compatible markdown
2. **Relative path conventions**: Assumes POSIX-style paths (`/`, not `\`)
3. **File system access**: Script can read all repository files
4. **Network access**: External link checking requires internet connectivity

### Trade-offs

**Speed vs. Thoroughness**:
- ✅ Chosen: Fast validation (~60s full repo) with basic external checks
- ❌ Rejected: Deep external validation (would take 5-10 minutes)

**False Positives vs. False Negatives**:
- ✅ Chosen: Allow some false positives (flag ambiguous links for manual review)
- ❌ Rejected: Silent failures (missing broken links is worse than noise)

**Automation vs. Flexibility**:
- ✅ Chosen: Strict validation by default, opt-out via ignore patterns
- ❌ Rejected: Lenient validation (defeats the purpose)

---

## Related SAPs

**Depends on**:
- None (foundational SAP)

**Enhances**:
- **SAP-007 (Documentation Framework)** - Ensures Diátaxis structure has valid links
- **SAP-000 (SAP Framework)** - Validates all SAP cross-references
- **SAP-012 (Development Lifecycle)** - Adds quality gate for documentation changes

**Enhanced by**:
- **SAP-006 (Quality Gates)** - Integrates link validation into release criteria
- **SAP-005 (CI/CD Workflows)** - Automates validation in pipelines

---

## Version History

**v1.0 (2025-10-28)** - Initial creation during Wave 2
- Created as highest-priority foundational SAP
- Supports Wave 2 SAP audit workflow
- Enables 4-domain architecture validation

---

## Adoption Commitment

**For chora-base**:
- SAP-016 will be fully implemented in Wave 2 (Phase 1)
- Link validation script will validate all 15 SAPs
- CI/CD integration will be completed before Wave 2 release

**For external projects**:
- SAP-016 included in all cloned projects (via `docs/skilled-awareness/`)
- Adoption blueprint provides integration guide
- Link validation script included in `scripts/` directory

---

## Success Stories (To Be Updated)

**Wave 2 (chora-base itself)**:
- Validated 279 files across 4-domain architecture
- Caught X broken links before Wave 2 release
- Prevented Y broken references in SAP audits

**External Adopter 1** (TBD):
- Link validation caught broken references during project customization
- Saved Z hours of manual link hunting

---

**SAP Owner**: chora-base core team
**Status**: Active (Wave 2 implementation in progress)
**Next Review**: Post-Wave 2 (estimated 2025-11-XX)

This capability charter demonstrates chora-base's skilled-awareness/ domain: meta-layer SAP documentation defining a portable capability package.
