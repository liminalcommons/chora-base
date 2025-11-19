# SAP-052 Templates: Ownership Zones

This directory contains reusable templates for implementing SAP-052 (Ownership Zones) in chora ecosystem projects.

## Templates

### CODEOWNERS-template

**Purpose**: Generate a CODEOWNERS file for automatic reviewer assignment in GitHub/GitLab repositories.

**Source**: Extracted from chora-workspace pilot validation (2025-11-18), which achieved 95.2% ownership coverage.

**Template Variables**:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name | chora-workspace, chora-gateway |
| `{{OWNER}}` | Default owner for all domains | @victorpiper |
| `{{DOCS_OWNER}}` | Documentation domain owner | @victorpiper or @doc-team |
| `{{SCRIPTS_OWNER}}` | Scripts/automation domain owner | @victorpiper or @devops-team |
| `{{INBOX_OWNER}}` | Coordination domain owner (optional) | @victorpiper |
| `{{MEMORY_OWNER}}` | Memory system domain owner (optional) | @victorpiper |
| `{{PROJECT_DOCS_OWNER}}` | Project management domain owner (optional) | @victorpiper or @pm-team |
| `{{TESTS_OWNER}}` | Tests domain owner | @victorpiper or @qa-team |
| `{{PACKAGES_OWNER}}` | Packages/submodules domain owner | @victorpiper |

**Usage**:

#### Option 1: Automated Generation (Recommended)

Use the `codeowners-generator.py` tool from `packages/chora-base/scripts/`:

```bash
# Generate CODEOWNERS with chora-workspace template
python3 packages/chora-base/scripts/codeowners-generator.py \
  --template chora-workspace \
  --owner @victorpiper \
  --output CODEOWNERS

# For custom templates, modify codeowners-generator.py TEMPLATES dict
```

#### Option 2: Manual Template Substitution

1. Copy `CODEOWNERS-template` to your project root as `CODEOWNERS`
2. Replace template variables with actual values:
   ```bash
   sed -i '' 's/{{PROJECT_NAME}}/your-project-name/g' CODEOWNERS
   sed -i '' 's/{{OWNER}}/@your-username/g' CODEOWNERS
   sed -i '' 's/{{DOCS_OWNER}}/@docs-team/g' CODEOWNERS
   # ... replace remaining variables
   ```
3. Remove domains that don't apply to your project (e.g., `/inbox/` for non-coordination repos)

#### Option 3: Domain-Specific Customization

For multi-developer teams, assign different owners per domain:

```diff
- {{DOCS_OWNER}}
+ @alice

- {{SCRIPTS_OWNER}}
+ @bob

- {{PACKAGES_OWNER}}
+ @carol
```

**Validation**:

After generating CODEOWNERS, validate with the ownership-coverage tool:

```bash
# Check coverage (target: 80%+)
python3 packages/chora-base/scripts/ownership-coverage.py \
  --repo /path/to/your/repo \
  --codeowners /path/to/your/repo/CODEOWNERS \
  --format json

# Expected output: coverage >= 80%
```

**Test Reviewer Suggestions**:

Validate auto-reviewer assignment with the reviewer-suggester tool:

```bash
# Test with specific files
python3 packages/chora-base/scripts/reviewer-suggester.py \
  --files docs/README.md scripts/validate.py \
  --format text

# Test with git diff (current branch vs main)
python3 packages/chora-base/scripts/reviewer-suggester.py \
  --base main \
  --format text
```

## Pilot Validation Results (chora-workspace)

**Date**: 2025-11-18
**Coverage**: 95.2% (11,845/12,444 files)
**Orphan Files**: 599 (4.8%) - Acceptable (mostly .DS_Store, build artifacts)
**Test Scenarios**: 10+ scenarios, 100% pass rate
**Time Invested**: 3 hours (0.4 days)

**Key Findings**:
- `/packages/` pattern contributed 76.3% of coverage (critical for monorepos)
- Root-level config patterns (`/*.yml`, `/*.json`, etc.) captured 0.4% additional coverage
- Single-owner configuration simplifies multi-domain PRs
- 6 edge cases discovered (all low-impact, documented in pilot report)

**Artifacts**:
- Pilot report: `project-docs/metrics/sap-052-phase3-pilot-report.md`
- Best practices: `.chora/memory/knowledge/notes/2025-11-18-sap-052-pilot-validation-findings.md`
- Coverage baseline: `project-docs/sap-052-coverage-baseline.json` (22.9%)
- Coverage final: `project-docs/sap-052-coverage-final.json` (95.2%)

## Domain Definitions

The CODEOWNERS template includes these domain patterns:

| Domain | Pattern | Purpose | Coverage (chora-workspace) |
|--------|---------|---------|---------------------------|
| **Root config** | `/*.yml`, `/*.json`, `/.*`, etc. | Root-level configuration files | 0.4% |
| **Documentation** | `/docs/`, `*.md` | All documentation | 1.5% |
| **Scripts** | `/scripts/`, `/justfile` | Automation and tooling | 1.4% |
| **Inbox** | `/inbox/` | Coordination layer (SAP-001) | 0.9% |
| **Memory** | `/.chora/` | Memory system (SAP-010) | 2.3% |
| **Project Docs** | `/project-docs/` | Project management artifacts | 2.2% |
| **Tests** | `/tests/` | Test suites | 1.6% |
| **Packages** | `/packages/` | Submodules, monorepo packages | 76.3% |
| **Shared** | `/AGENTS.md`, `/CLAUDE.md`, `/README.md` | Cross-cutting documentation | 0.02% |

**Notes**:
- `/packages/` pattern is **critical** for monorepos with submodules
- Remove optional domains (`/inbox/`, `/.chora/`, `/project-docs/`) if not applicable
- Adjust patterns based on your project structure

## Best Practices

### 1. Coverage Target: 80%+

Run ownership-coverage.py after generating CODEOWNERS. Aim for 80%+ coverage.

**Acceptable orphans**:
- Build artifacts (`.pyc`, `__pycache__`, `node_modules/`)
- System metadata (`.DS_Store`, `.git/`)
- Temporary files (`*.bak`, `*.orig`)

**Unacceptable orphans**:
- Source code
- Documentation
- Tests
- Configuration files

### 2. Test Before Committing

Validate reviewer suggestions with realistic file paths:

```bash
# Test single domain
python3 packages/chora-base/scripts/reviewer-suggester.py \
  --files docs/architecture.md

# Test cross-domain
python3 packages/chora-base/scripts/reviewer-suggester.py \
  --files docs/api.md src/server.py tests/test_api.py
```

### 3. Multi-Developer Setup

When onboarding a second developer:
1. Reassign domains by expertise (e.g., @alice for docs, @bob for scripts)
2. Establish consensus protocol for multi-domain PRs (SAP-052 Contract 4)
3. Monitor cross-domain PR metrics (review time, conflict rate)

### 4. Quarterly Audit

Review orphan files quarterly:

```bash
python3 packages/chora-base/scripts/ownership-coverage.py \
  --repo . \
  --codeowners CODEOWNERS \
  --format json | jq '.orphan_files[] | select(.file_type != "system_metadata")'
```

Add patterns if legitimate files are orphaned.

## Tooling

All SAP-052 tools are in `packages/chora-base/scripts/`:

- **codeowners-generator.py**: Generate CODEOWNERS from templates
- **ownership-coverage.py**: Analyze ownership coverage (target: 80%+)
- **reviewer-suggester.py**: Suggest reviewers for PRs/commits

See `packages/chora-base/scripts/README.md` for detailed usage.

## Related Documentation

- **SAP-052 Charter**: [capability-charter.md](../capability-charter.md) - Problem statement, solution, scope
- **SAP-052 Protocol**: [protocol-spec.md](../protocol-spec.md) - Ownership patterns, conflict jurisdiction rules
- **SAP-052 Awareness**: [awareness-guide.md](../awareness-guide.md) - Agent workflows, decision trees
- **SAP-052 Blueprint**: [adoption-blueprint.md](../adoption-blueprint.md) - 4-phase adoption plan
- **SAP-052 Ledger**: [ledger.md](../ledger.md) - Adoption history, metrics, ROI

## Support

For issues or questions:
1. Review pilot findings: `.chora/memory/knowledge/notes/2025-11-18-sap-052-pilot-validation-findings.md`
2. Check SAP-052 awareness guide: `awareness-guide.md`
3. Create coordination request: `inbox/incoming/coordination/`

---

**Template Version**: 1.0.0
**Based On**: chora-workspace pilot validation (2025-11-18)
**Maintainer**: SAP-052 Working Group
**Last Updated**: 2025-11-18
