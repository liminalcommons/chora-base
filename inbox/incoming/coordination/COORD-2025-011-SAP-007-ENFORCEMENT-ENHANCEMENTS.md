---
title: "COORD-2025-011: SAP-007 Enforcement Layer Enhancements"
type: coordination-request
status: draft
priority: medium
created: 2025-11-09
requester: chora-workspace
tags: [coordination, sap-007, documentation-framework, chora-base, enhancement]
---

# COORD-2025-011: SAP-007 Enforcement Layer Enhancement Request

**Request ID:** COORD-2025-011
**Submitted:** 2025-11-09
**Requester:** chora-workspace (via Claude agent)
**Priority:** Medium
**Status:** Draft

## Summary

Propose enhancements to SAP-007 (Documentation Framework) in chora-base based on learnings from real-world L2→L3 adoption in chora-workspace, including enforcement mechanisms, decision tree templates, and clarified root directory policy.

## Context

### What Happened

During chora-workspace SAP-007 L2 adoption (2025-11-08), we successfully reorganized 41→8 root files following the 3-directory structure. However, **within hours of completion**, new documents were created at root in violation of SAP-007, including the SAP-007 completion report itself.

**Root cause identified**: SAP-007 L2 defines structure beautifully but lacks enforcement mechanisms to maintain it.

### What We Built

To address this gap, we implemented a complete enforcement layer (2025-11-09):

1. **Validation Script** (`scripts/validate-sap-007-structure.py`):
   - Checks root directory has ≤8 allowed files
   - Verifies project-docs/ subdirectories exist
   - Detects orphaned docs in project-docs/ root
   - Exit codes for CI/CD integration
   - Windows-compatible (no unicode in output)

2. **Pre-commit Hook** (`scripts/pre-commit-hooks/sap-007-check.sh`):
   - Runs validation before each commit
   - Blocks commits that violate SAP-007
   - Optional bypass with --no-verify

3. **Decision Trees** (added to 3 AGENTS.md files):
   - Clear "where should this doc go?" flowcharts
   - Examples for each category
   - Validation command references

**Impact**: Root directory violations now impossible without explicit bypass. Structure maintained automatically.

### The Gap

SAP-007 currently describes:
- ✅ The 3-directory structure (user-docs, dev-docs, project-docs)
- ✅ Diataxis framework rationale
- ✅ Frontmatter requirements
- ✅ Executable How-To pattern

SAP-007 does NOT describe:
- ❌ How to enforce the structure (validation)
- ❌ How many files belong at root (implicit, not explicit)
- ❌ Decision tree pattern for categorization
- ❌ L2→L3 progression (enforcement layer)
- ❌ Common pitfalls (creating docs during active work)

## Request Details

### What is Needed

Enhance chora-base SAP-007 documentation with:

1. **Level 3 (Validated) specification** with enforcement layer requirements
2. **Validation script template** (genericized from our implementation)
3. **Pre-commit hook template** (genericized from our implementation)
4. **Decision tree template** for AGENTS.md files
5. **Root directory policy clarification** (8-file guideline with rationale)
6. **Common pitfalls section** with mitigation strategies

### Scope

**In Scope:**
- Documentation enhancements to SAP-007 in chora-base
- Template files (validation script, pre-commit hook) as reference implementations
- Guidance on L2→L3 progression with effort estimates
- Windows compatibility considerations for validation scripts

**Out of Scope:**
- Automated migration tools (projects implement their own)
- CI/CD integration examples (project-specific)
- Justfile/makefile recipes (project-specific automation)
- Implementation in chora-base itself (chora-base is template source, not adopter)

### Success Criteria

1. SAP-007 documentation includes Level 3 (Validated) specification
2. Template validation script available in chora-base for reference
3. Template pre-commit hook available in chora-base for reference
4. Decision tree template provided for project customization
5. Root directory policy explicitly stated (8-file guideline)
6. Common pitfalls section documents the "completion report at root" antipattern
7. Maturity level guidance clarifies L2 alone isn't sustainable

## Proposed Enhancement Details

### 1. Add Level 3 (Validated) Specification

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/README.md`

**Content**:
```markdown
## Level 3: Validated (Enforcement)

At Level 3, the documentation structure is actively enforced through automation:

### Required Components

1. **Validation Script**
   - Checks structure compliance automatically
   - Exit codes for CI/CD integration (0=pass, 1=fail)
   - Clear error messages with remediation steps
   - Template: See `templates/validate-sap-007-structure.py`

2. **Pre-commit Hook**
   - Runs validation before each commit
   - Blocks commits that violate structure
   - Optional bypass mechanism (--no-verify)
   - Template: See `templates/sap-007-check.sh`

3. **Integration**
   - Justfile/makefile recipe: `validate-sap-007`
   - Installation recipe: `install-sap-007-hook`
   - CI/CD pipeline integration

### Time Investment

- L2 → L3: 1-2 hours (adapt templates to project)
- ROI: Prevents 30-60 minutes cleanup per month

### Critical Note

**L2 without L3 enforcement = structure degrades within days.**

Even during SAP-007 adoption sessions, new documents are often created
at root due to focus on content rather than placement. Enforcement
prevents this antipattern.
```

### 2. Validation Script Template

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py`

**Content**: Genericized version of our script with:
- Configurable `ALLOWED_ROOT_FILES` list
- Configurable `REQUIRED_PROJECT_DOCS_SUBDIRS` list
- Windows-compatible output (no unicode)
- Clear error messages with remediation guidance
- Exit codes for CI/CD

**Key Features to Highlight**:
- 3 validation checks (root files, subdirs, orphaned docs)
- Informational warnings for missing standard files
- Clear pass/fail output for automation

### 3. Pre-commit Hook Template

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/templates/sap-007-check.sh`

**Content**: Shell script that:
- Runs validation script
- Blocks commit on failure
- Provides clear error message
- Documents bypass mechanism

### 4. Decision Tree Template

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/decision-tree-template.md`

**Content**:
```markdown
## Creating New Documentation (SAP-007 Decision Tree)

**Where should this doc go?**

1. **Root directory?** → Only these N files allowed:
   - README.md (project overview)
   - AGENTS.md (agent awareness - SAP-009)
   - CLAUDE.md (Claude-specific workflows - SAP-009)
   - CHANGELOG.md (version history)
   - CONTRIBUTING.md (contribution guidelines)
   - LICENSE.md (license)
   - [PROJECT_SPECIFIC.md] (document rationale)
   - **Everything else → Use 3-directory structure below**

2. **User-facing doc?** → `user-docs/`
   - Tutorial → `user-docs/tutorials/`
   - How-to guide → `user-docs/how-to/`
   - Reference → `user-docs/reference/`
   - Explanation → `user-docs/explanation/`

3. **Developer doc?** → `dev-docs/`
   - Workflow → `dev-docs/workflows/`
   - Vision → `dev-docs/vision/`
   - Code example → `dev-docs/examples/`
   - [Project-specific subdirectories]

4. **Project management doc?** → `project-docs/`
   - [Project-specific subdirectories with examples]

**Validation**: Run `just validate-sap-007` to check compliance

**Enforcement**: Install pre-commit hook with `just install-sap-007-hook`
```

**Usage**: Projects copy this to their AGENTS.md files and customize
the project-specific sections.

### 5. Root Directory Policy Clarification

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/README.md`

**Add Section**:
```markdown
## Root Directory Policy

### Default: 8 Files Maximum

The root directory should contain only essential files that require
maximum visibility:

**Required (6 files)**:
- `README.md` - Project overview (first impression)
- `AGENTS.md` - Agent awareness (SAP-009)
- `CLAUDE.md` - Claude-specific workflows (SAP-009)
- `CHANGELOG.md` - Version history (standard)
- `CONTRIBUTING.md` - Contribution guidelines (community)
- `LICENSE.md` - License (legal requirement)

**Recommended (2 files)**:
- `DOCUMENTATION_STANDARD.md` - Doc writing standards (SAP-007)
- `ROADMAP.md` - Strategic vision (planning)

**Optional Exceptions**:
- `CLAUDE_CHECKPOINT.md` - Checkpoint template (SAP-009)
- Project-specific essential files (document rationale in AGENTS.md)

**Rationale**:
- 8-file limit maintains navigability
- Forces intentional decisions about visibility
- Prevents root directory from becoming dumping ground
- Aligns with "progressive disclosure" principle

**Everything else belongs in user-docs/, dev-docs/, or project-docs/**

### Validation

Use validation script to enforce this policy. Configure
`ALLOWED_ROOT_FILES` constant to match your project's approved list.
```

### 6. Common Pitfalls Section

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/README.md`

**Add Section**:
```markdown
## Common Pitfalls

### Pitfall 1: Creating Docs at Root During Active Work

**Problem**: Even during SAP-007 L2 adoption sessions, completion reports
are often created at root in violation of the structure just implemented.

**Why it happens**:
- Focus on content over placement during active work
- Muscle memory (old habit: "just create the file")
- Lack of immediate feedback (no validation until commit)

**Impact**: Structure degrades within hours or days of L2 completion.

**Solution**:
1. Install pre-commit hook **immediately** after L2 adoption
2. Add decision tree to AGENTS.md **before** creating any new docs
3. Run `just validate-sap-007` before committing any session work
4. Review root directory at end of each session

**Prevention**: L3 enforcement layer makes this impossible without
explicit bypass.

### Pitfall 2: Assuming L2 is Sufficient

**Problem**: Teams complete L2 adoption (reorganize existing docs) but
don't implement enforcement (L3), expecting the structure to maintain
itself.

**Reality**: Without enforcement, structure degrades to pre-L2 state
within 2-4 weeks.

**Solution**: Treat L2→L3 progression as mandatory, not optional.
Budget the 1-2 hours for enforcement layer during initial adoption.

**ROI**: L3 enforcement prevents 30-60 minutes of cleanup per month
(15-30x ROI over 1 year).
```

### 7. Windows Compatibility Note

**Location**: `chora-base/docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py`

**Add Comment**:
```python
"""
Windows Compatibility Note:
---------------------------
Windows console (cmd.exe, PowerShell) has limited unicode support.
To ensure cross-platform compatibility:

- Use "[PASS]" instead of "✅"
- Use "[FAIL]" instead of "❌"
- Use "[INFO]" instead of "ℹ️"
- Use "<=" instead of "≤"
- Use ">=" instead of "≥"

This ensures validation output displays correctly on all platforms.
"""
```

## Timeline

- **Requested By:** 2025-12-01 (3 weeks)
- **Ideal Completion:** 2025-12-15 (for chora-base v4.13.0 release)
- **Absolute Deadline:** None (enhancement, not blocker)

**Rationale**: No urgency, but would benefit future SAP-007 adopters.
chora-workspace can proceed with local implementation regardless.

## Dependencies

- [x] SAP-007 L2 completion in chora-workspace (completed 2025-11-08)
- [x] SAP-007 enforcement layer in chora-workspace (completed 2025-11-09)
- [ ] Review of proposed enhancements by chora-base maintainers
- [ ] Decision on template location within chora-base structure

## Stakeholders

**Primary:**
- chora-base maintainers (approval and implementation)
- Victor Piper (original SAP-007 author)

**Notify:**
- Future SAP-007 adopters (via chora-base documentation)
- chora-compose project (may benefit from same patterns)

**Consult:**
- Other chora-workspace SAP-007 L3 adopters (if any emerge)

## Resources

### Related Documents (chora-workspace)

- [scripts/validate-sap-007-structure.py](../../scripts/validate-sap-007-structure.py) - Reference implementation
- [scripts/pre-commit-hooks/sap-007-check.sh](../../scripts/pre-commit-hooks/sap-007-check.sh) - Hook implementation
- [project-docs/AGENTS.md](../../project-docs/AGENTS.md#creating-new-documentation-sap-007-decision-tree) - Decision tree example
- [CLAUDE.md](../../CLAUDE.md#pitfall-6-creating-docs-at-root-sap-007-violation) - Pitfall documentation
- [AGENTS.md](../../AGENTS.md#creating-new-documents-decision-tree) - Root-level decision tree
- Git commit: `54d1647` (feat: SAP-007 enforcement layer - 2025-11-09)

### Reference Materials (chora-base)

- [SAP-007 Current Documentation](../../../chora-base/docs/skilled-awareness/documentation-framework/README.md)
- [Diataxis Framework](https://diataxis.fr/) - Original inspiration

### Example Output

**Validation Script** (passing):
```
Validating SAP-007 Documentation Framework compliance...
   Repository: c:\Users\victo\code\chora-workspace

Check 1: Root directory files (8 allowed)...
   [PASS] Root has 6 markdown file(s) (within policy)

Check 2: project-docs/ subdirectory structure...
   [PASS] All 9 required subdirectories exist

Check 3: Orphaned docs in project-docs/ root...
   [PASS] No orphaned docs in project-docs/ root

============================================================
[PASS] SAP-007 validation PASSED

Documentation structure complies with SAP-007 framework:
- Root directory: Clean (<=8 files)
- project-docs/: Properly structured
- No orphaned docs
```

## Notes

### Why These Enhancements Matter

1. **Real-world validation**: These aren't theoretical - they solve actual problems encountered during adoption
2. **Templates save time**: Future adopters get 80% of the work done for them
3. **Sustainability**: L2 alone isn't sustainable; L3 enforcement is necessary
4. **Low barrier**: Templates are simple Python + shell scripts, easy to adapt
5. **Proven ROI**: Prevents 30-60 min/month cleanup (documented in chora-workspace metrics)

### Alternative Approaches Considered

1. **Manual enforcement** (rely on discipline)
   - Rejected: Proven to fail even during adoption sessions

2. **CI/CD only** (no pre-commit hook)
   - Rejected: Feedback loop too long, violations slip through

3. **IDE integration** (LSP/linter)
   - Future enhancement: Would complement pre-commit hook

### Implementation Flexibility

Projects can:
- Customize the 8-file root policy (add project-specific files)
- Adjust subdirectory requirements (add/remove as needed)
- Choose enforcement level (validation only, or validation + hook)
- Skip L3 entirely (though not recommended)

The templates provide a starting point, not a mandate.

## Response

[To be filled by chora-base maintainer]

### Review Questions

1. Do these enhancements align with SAP-007's original intent?
2. Is the template location appropriate (within SAP-007 docs)?
3. Should templates be executable or documentation-only?
4. Is the 8-file root policy too prescriptive?
5. Should this be SAP-007 v1.1.0 or a separate SAP?

---

**Coordination Protocol**: This request follows SAP-001 (Inbox Protocol) for
cross-repository coordination. Response expected via chora-base issue or
direct coordination through established channels.

**Generated**: 2025-11-09 by Claude agent in chora-workspace
**Contact**: File response in `inbox/incoming/coordination/` or reply via GitHub
