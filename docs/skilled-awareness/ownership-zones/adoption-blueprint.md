# Adoption Blueprint: Ownership Zones

**SAP ID**: SAP-052
**Version**: 1.0.0
**Last Updated**: 2025-11-17

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-052 Ownership Zones across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Manual CODEOWNERS creation, basic GitHub integration | 10-20 min | Low (quarterly ownership review) | New repositories, single-developer projects, pilot testing |
| **Level 2: Advanced** | Template generator, coverage analysis, reviewer suggester | 30-45 min | Medium (monthly coverage review) | Active multi-developer projects, established teams |
| **Level 3: Mastery** | Full automation, ownership rotation, metrics dashboard, CI/CD integration | 60-90 min | Medium (quarterly rotation + sprint reviews) | **Recommended for production** |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption over 3-6 weeks)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
- Getting started with code ownership patterns
- Creating CODEOWNERS file manually for simple repository
- GitHub/GitLab automatic reviewer assignment
- Single-developer or small team (2-3 developers)
- Quick proof-of-concept before full rollout

### Time Estimate

- **Setup**: 10-20 minutes
- **Learning Curve**: Minimal (CODEOWNERS syntax takes 1-2 PRs to internalize)

### Prerequisites

**Required**:
- GitHub or GitLab repository with multi-developer access
- Write access to repository (can commit CODEOWNERS file)
- Understanding of repository directory structure
- GitHub/GitLab account with username

**Recommended**:
- SAP-051 (Git Workflow Patterns) adopted (for PR automation)
- Familiarity with gitignore-style pattern syntax

### Step-by-Step Instructions

#### Step 1.1: Analyze Repository Structure

**Action**:
```bash
# List top-level directories
ls -d */

# Identify primary domains (filter out build/test directories)
ls -d */ | grep -v "node_modules\|\.git\|test-integration"
```

**Expected Output** (chora-workspace example):
```
docs/
scripts/
inbox/
.chora/
project-docs/
```

**Identify domains**:
- **docs/** - Documentation domain
- **scripts/** - Automation/Scripts domain
- **inbox/** - Coordination domain
- **.chora/** - Memory system domain
- **project-docs/** - Project management domain

---

#### Step 1.2: Create CODEOWNERS File

**Action**:
```bash
# Create CODEOWNERS file at repository root
touch CODEOWNERS

# Open in editor
nano CODEOWNERS  # or vim, code, etc.
```

**Template** (chora-workspace):
```
# chora-workspace CODEOWNERS
# Defines ownership for 5 primary domains

# Documentation domain
/docs/ @victorpiper
*.md @victorpiper

# Scripts/Automation domain
/scripts/ @victorpiper
justfile @victorpiper

# Coordination/Inbox domain
/inbox/ @victorpiper

# Memory system domain
/.chora/ @victorpiper

# Project management domain
/project-docs/ @victorpiper

# Shared files (multiple owners if team)
/AGENTS.md @victorpiper
/CLAUDE.md @victorpiper
/README.md @victorpiper
```

**For multi-developer team**:
```
# Documentation domain
/docs/ @alice @bob  # Multiple owners for fallback

# Scripts domain
/scripts/ @charlie  # Different owner per domain

# Use teams (requires GitHub organization)
/docs/ @org/docs-team
/scripts/ @org/automation-team
```

---

#### Step 1.3: Validate CODEOWNERS Syntax

**Action**:
```bash
# GitHub API validation (requires GitHub token)
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/codeowners/errors

# Manual validation checklist:
# ✓ File named CODEOWNERS (case-sensitive, no extension)
# ✓ File at repository root (not in subdirectory)
# ✓ Patterns start with / for absolute paths (/docs/ not docs/)
# ✓ Owners start with @ (@username not username)
# ✓ Team format: @org/team-name (requires organization)
```

**Expected Output** (GitHub API):
```json
{
  "errors": []
}
```

**Common Errors**:
- ❌ `docs/ @owner` → ✅ `/docs/ @owner` (missing leading /)
- ❌ `/docs/ owner` → ✅ `/docs/ @owner` (missing @)
- ❌ File named `codeowners` → ✅ Rename to `CODEOWNERS`

---

#### Step 1.4: Commit CODEOWNERS File

**Action**:
```bash
# Stage CODEOWNERS file
git add CODEOWNERS

# Commit with conventional commit message (if SAP-051 adopted)
git commit -m "feat(ownership): add CODEOWNERS file for 5 domains

Defines ownership for docs/, scripts/, inbox/, .chora/, project-docs/
domains. Enables automatic reviewer assignment on GitHub.

Refs: SAP-052"

# Push to main branch
git push origin main
```

**Expected Output**:
```
[main abc1234] feat(ownership): add CODEOWNERS file for 5 domains
 1 file changed, 25 insertions(+)
 create mode 100644 CODEOWNERS
```

---

#### Step 1.5: Test Automatic Reviewer Assignment

**Action**:
```bash
# Create test branch
git checkout -b test/codeowners-validation

# Make change to docs/ domain
echo "# Test" >> docs/test.md
git add docs/test.md
git commit -m "docs: add test file for CODEOWNERS validation"

# Push and create PR
git push origin test/codeowners-validation
gh pr create --title "Test CODEOWNERS" --body "Testing automatic reviewer assignment"
```

**Expected Result**:
- GitHub automatically assigns @victorpiper as reviewer (docs/ domain owner)
- PR shows "Requested reviewers: @victorpiper"

**Verification**:
```bash
# Check PR details via GitHub API
gh pr view --json reviewRequests

# Expected output:
# {
#   "reviewRequests": [
#     {"login": "victorpiper"}
#   ]
# }
```

---

### Level 1 Checklist

- [ ] Repository structure analyzed (5 domains identified)
- [ ] CODEOWNERS file created at repository root
- [ ] CODEOWNERS syntax validated (no errors from GitHub API)
- [ ] CODEOWNERS committed to main branch
- [ ] Test PR created with automatic reviewer assignment
- [ ] Reviewer correctly assigned based on changed files

**Success Criteria**: GitHub automatically assigns reviewers when PR is created

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds:
- **CODEOWNERS template generator** (automated file creation)
- **Ownership coverage analysis** (metrics dashboard)
- **Reviewer suggester** (git history-based suggestions)
- **Integration with SAP-001/015** (coordination + beads)

### Time Estimate

- **Setup**: 30-45 minutes
- **Learning Curve**: Low (tools are automated, focus on interpreting metrics)

### Prerequisites

**Required** (Level 1 complete):
- ✅ CODEOWNERS file exists and validated
- ✅ GitHub automatic reviewer assignment working

**Additional Requirements**:
- Python 3.11+ installed (`python --version`)
- Git log access (for reviewer suggester)
- Justfile recipes for ownership tools (included in chora-base)

### Step-by-Step Instructions

#### Step 2.1: Install Ownership Tools

**Action**:
```bash
# Verify Python version
python --version
# Expected: Python 3.11.0 or higher

# Ownership tools are in scripts/ directory
ls scripts/codeowners-generator.py
ls scripts/ownership-coverage.py
ls scripts/reviewer-suggester.py

# Make scripts executable (if needed)
chmod +x scripts/codeowners-generator.py
chmod +x scripts/ownership-coverage.py
chmod +x scripts/reviewer-suggester.py
```

**Expected Output**:
```
Python 3.11.6
scripts/codeowners-generator.py
scripts/ownership-coverage.py
scripts/reviewer-suggester.py
```

---

#### Step 2.2: Run Ownership Coverage Analysis

**Action**:
```bash
# Run coverage analysis via justfile recipe
just ownership-coverage

# Or run script directly
python scripts/ownership-coverage.py --repo .
```

**Expected Output** (JSON report):
```json
{
  "repository": "chora-workspace",
  "analysis_date": "2025-11-17T14:00:00Z",
  "total_files": 450,
  "covered_files": 360,
  "uncovered_files": 90,
  "coverage_percent": 80.0,

  "domain_coverage": [
    {"domain": "docs", "pattern": "/docs/", "owner": "@victorpiper", "files_covered": 120},
    {"domain": "scripts", "pattern": "/scripts/", "owner": "@victorpiper", "files_covered": 85}
  ],

  "orphan_files": [
    {"path": "temp/analysis.md", "last_modified": "2025-11-10"},
    {"path": "test-integration-all/...", "last_modified": "2025-10-15"}
  ],

  "recommendations": [
    {
      "type": "low_coverage",
      "message": "80% coverage meets target, but 90 orphan files should be reviewed",
      "action": "Review orphan_files list and add patterns to CODEOWNERS"
    }
  ]
}
```

**Interpret Results**:
- ✅ **80% coverage**: Meets target (≥80% production-ready)
- ⚠️ **90 orphan files**: Review list, add patterns or exclude from git
- ✅ **5 domains covered**: All primary domains have assigned owners

---

#### Step 2.3: Address Orphan Files

**Action**:
```bash
# Review orphan files list
cat coverage-report.json | jq '.orphan_files[] | .path'

# Common orphan file types:
# - temp/ (temporary files) → Add to .gitignore or add CODEOWNERS pattern
# - test-integration-*/ (build artifacts) → Add to .gitignore
# - *.log, *.tmp (temporary) → Already in .gitignore

# Option 1: Add pattern to CODEOWNERS
echo "/temp/ @victorpiper" >> CODEOWNERS

# Option 2: Exclude from git (if not needed)
echo "temp/" >> .gitignore

# Commit changes
git add CODEOWNERS .gitignore
git commit -m "fix(ownership): address orphan files in coverage report"
```

---

#### Step 2.4: Use Reviewer Suggester Tool

**Action**:
```bash
# Suggest reviewer for specific file based on git history
python scripts/reviewer-suggester.py --file docs/vision/mcp.md

# Output:
# Suggested reviewer: @victorpiper (18 commits to this file)
# Fallback reviewers: @alice (3 commits), @bob (1 commit)
```

**Use Case**:
- Orphan files without CODEOWNERS pattern
- Cross-domain files with unclear ownership
- Validating current ownership assignments (does git history match CODEOWNERS?)

**Example**:
```bash
# Check if CODEOWNERS owner matches git history
# 1. Get owner from CODEOWNERS
grep "/docs/" CODEOWNERS
# Output: /docs/ @victorpiper

# 2. Check git history for docs/
python scripts/reviewer-suggester.py --file docs/README.md
# Output: @victorpiper (25 commits)

# ✅ Match! CODEOWNERS aligns with git history
```

---

#### Step 2.5: Integrate with SAP-001 (Inbox)

**Action**:
```bash
# Route coordination requests based on domain ownership

# Example: CORD-2025-017 affects docs/ domain
# Check CODEOWNERS for docs/ owner
grep "/docs/" CODEOWNERS
# Output: /docs/ @victorpiper

# → Route CORD-2025-017 to @victorpiper for review
```

**Template for Coordination Request**:
```json
{
  "request_id": "CORD-2025-XXX",
  "to_repo": "chora-base",
  "target_domain": "docs/skilled-awareness/",
  "owner": "@victorpiper",  // From CODEOWNERS lookup
  "submitted_date": "2025-11-17"
}
```

---

#### Step 2.6: Integrate with SAP-015 (Beads)

**Action**:
```bash
# Assign beads tasks based on domain ownership

# Example: Task to fix docs/ links
bd create "Fix broken links in docs/ domain"

# Check CODEOWNERS for docs/ owner
grep "/docs/" CODEOWNERS
# Output: /docs/ @victorpiper

# → Assign beads task to @victorpiper (docs owner)
```

---

### Level 2 Checklist

- [ ] Ownership tools installed and executable
- [ ] Coverage analysis run (≥80% coverage achieved)
- [ ] Orphan files addressed (added patterns or excluded from git)
- [ ] Reviewer suggester tested on sample files
- [ ] Coordination requests routed based on ownership
- [ ] Beads tasks assigned based on ownership

**Success Criteria**:
- ≥80% ownership coverage
- Coverage analysis runs without errors
- Ownership guides coordination/task assignment

---

## Level 3: Mastery Adoption

### Purpose

Level 3 adoption adds:
- **Ownership rotation protocol** (quarterly handoff process)
- **Metrics dashboard** (coverage trends, review latency)
- **CI/CD integration** (automated coverage checks)
- **Conflict jurisdiction automation** (owner-based resolution)

### Time Estimate

- **Setup**: 60-90 minutes
- **Learning Curve**: Medium (rotation process, metrics interpretation)

### Prerequisites

**Required** (Level 2 complete):
- ✅ CODEOWNERS file with ≥80% coverage
- ✅ Ownership tools installed and tested
- ✅ SAP-001/015 integration complete

**Additional Requirements**:
- GitHub Actions or CI/CD pipeline access
- Multi-developer team (for rotation)
- Quarterly planning cadence (for ownership rotation)

### Step-by-Step Instructions

#### Step 3.1: Set Up Ownership Rotation Schedule

**Action**:
```bash
# Create ownership rotation calendar
# Q1 2025: Initial ownership assignments
# Q2 2025: First rotation review (identify rotation candidates)
# Q3 2025: Execute first rotation (1-2 domains)
# Q4 2025: Second rotation review

# Document rotation schedule in project-docs/
cat > project-docs/ownership-rotation-schedule.md << 'EOF'
# Ownership Rotation Schedule

## Q1 2025 (Initial Assignment)
- docs/ → @victorpiper
- scripts/ → @victorpiper
- inbox/ → @victorpiper
- .chora/ → @victorpiper
- project-docs/ → @victorpiper

## Q2 2025 (First Rotation Review)
- Target: Identify 1-2 domains for rotation
- Candidates: TBD (based on workload, developer skill alignment)

## Q3 2025 (First Rotation Execution)
- Rotate: TBD → TBD
- Knowledge transfer: Week 1-2
- Handoff: Week 3
EOF

git add project-docs/ownership-rotation-schedule.md
git commit -m "feat(ownership): add quarterly rotation schedule"
```

---

#### Step 3.2: Create Ownership Rotation Playbook

**Action**:
```bash
# Create knowledge transfer checklist template
cat > project-docs/ownership-rotation-playbook.md << 'EOF'
# Ownership Rotation Playbook

## Knowledge Transfer Checklist

### Week 1-2: Knowledge Transfer
- [ ] Outgoing owner creates knowledge doc (domain patterns, gotchas, tools)
- [ ] Outgoing owner pairs with incoming owner (1-2 sessions)
- [ ] Incoming owner shadows reviews (1-2 PRs)
- [ ] Knowledge doc added to domain AGENTS.md

### Week 3: Ownership Handoff
- [ ] Update CODEOWNERS (replace outgoing owner with incoming owner)
- [ ] Announce ownership change to team
- [ ] Incoming owner takes primary responsibility
- [ ] Outgoing owner available as fallback (1 month)

### Week 4: Post-Rotation Validation
- [ ] Monitor incoming owner review activity
- [ ] Incoming owner provides feedback on knowledge transfer
- [ ] Update rotation playbook based on learnings
- [ ] Log rotation in SAP-052 ledger

## Domain-Specific Knowledge Transfer

### docs/ Domain
- **Patterns**: Style guide, link validation, vision/ is aspirational
- **Tools**: validate-links.sh, doc-search.py
- **Gotchas**: research/ is archived, don't edit without approval

### scripts/ Domain
- **Patterns**: Python 3.11+, use justfile recipes
- **Tools**: sap-evaluator.py, memory-health-check.py
- **Gotchas**: Windows compatibility required (test on Git Bash)

### inbox/ Domain
- **Patterns**: Coordination request templates (SAP-001)
- **Tools**: inbox-status justfile recipe
- **Gotchas**: incoming/ is triage queue, coordination/ is active work

### .chora/ Domain
- **Patterns**: A-MEM event schema, knowledge note wikilinks
- **Tools**: memory-events, knowledge-list justfile recipes
- **Gotchas**: events/ is append-only, knowledge/ allows edits

### project-docs/ Domain
- **Patterns**: Sprint planning, retrospectives, metrics
- **Tools**: sap-roadmap, sprint-velocity justfile recipes
- **Gotchas**: metrics/ requires Python for dashboard generation
EOF

git add project-docs/ownership-rotation-playbook.md
git commit -m "feat(ownership): add rotation playbook with knowledge transfer checklists"
```

---

#### Step 3.3: Add CI/CD Coverage Check

**Action**:
```bash
# Create GitHub Actions workflow for ownership coverage
cat > .github/workflows/ownership-coverage.yml << 'EOF'
name: Ownership Coverage Check

on:
  pull_request:
    paths:
      - 'CODEOWNERS'
      - '.github/workflows/ownership-coverage.yml'
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  coverage-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run ownership coverage analysis
        run: |
          python scripts/ownership-coverage.py --repo .

      - name: Check coverage threshold
        run: |
          COVERAGE=$(jq -r '.coverage_percent' coverage-report.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "❌ Coverage is $COVERAGE% (below 80% threshold)"
            exit 1
          else
            echo "✅ Coverage is $COVERAGE% (meets 80% threshold)"
          fi

      - name: Comment PR with coverage report
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('coverage-report.json'));
            const body = `
            ## Ownership Coverage Report
            - **Coverage**: ${report.coverage_percent}%
            - **Covered files**: ${report.covered_files}/${report.total_files}
            - **Orphan files**: ${report.uncovered_files}
            ${report.coverage_percent >= 80 ? '✅' : '❌'} Target: ≥80%
            `;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
EOF

git add .github/workflows/ownership-coverage.yml
git commit -m "feat(ownership): add CI/CD coverage check workflow"
```

---

#### Step 3.4: Create Metrics Dashboard

**Action**:
```bash
# Create justfile recipe for metrics dashboard
cat >> justfile << 'EOF'

# Generate ownership metrics dashboard
ownership-dashboard:
    python scripts/ownership-coverage.py --repo . > coverage-report.json
    python scripts/ownership-dashboard.py --input coverage-report.json --output project-docs/metrics/ownership-dashboard.md
    @echo "Dashboard generated: project-docs/metrics/ownership-dashboard.md"
EOF

# Create dashboard generator script (simplified example)
cat > scripts/ownership-dashboard.py << 'EOF'
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def generate_dashboard(coverage_report):
    """Generate markdown dashboard from coverage report."""
    return f"""# Ownership Metrics Dashboard

**Generated**: {coverage_report['analysis_date']}

## Coverage Overview
- **Total files**: {coverage_report['total_files']}
- **Covered files**: {coverage_report['covered_files']}
- **Coverage**: {coverage_report['coverage_percent']}%
- **Status**: {'✅ Meets target' if coverage_report['coverage_percent'] >= 80 else '❌ Below target'}

## Domain Breakdown
{"".join([
    f"- **{d['domain']}**: {d['files_covered']} files ({d['percent_of_repo']}%) - {d['owner']}\n"
    for d in coverage_report['domain_coverage']
])}

## Orphan Files ({len(coverage_report['orphan_files'])})
{"".join([f"- {f['path']}\n" for f in coverage_report['orphan_files'][:10]])}
{"..." if len(coverage_report['orphan_files']) > 10 else ""}
"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        report = json.load(f)

    dashboard = generate_dashboard(report)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(dashboard)

    print(f"Dashboard generated: {args.output}")
EOF

chmod +x scripts/ownership-dashboard.py

git add justfile scripts/ownership-dashboard.py
git commit -m "feat(ownership): add metrics dashboard generator"
```

---

#### Step 3.5: Document Conflict Jurisdiction Process

**Action**:
```bash
# Add conflict jurisdiction documentation to AGENTS.md
cat >> .chora/AGENTS.md << 'EOF'

## Conflict Resolution (SAP-052)

When merge conflict occurs:

1. **Identify conflicted files**:
   ```bash
   git diff --name-only --diff-filter=U
   ```

2. **Lookup owner in CODEOWNERS**:
   ```bash
   grep "<file-pattern>" CODEOWNERS
   ```

3. **Apply jurisdiction rules**:
   - **Single domain**: Domain owner has authority → Owner resolves
   - **Cross-domain**: All owners collaborate → Seek consensus (24h)
   - **Deadlock**: Escalate to project lead → Final decision

4. **Document resolution**:
   - Add rationale in PR comment
   - Tag @domain-owner for final approval
EOF

git add .chora/AGENTS.md
git commit -m "docs(ownership): add conflict jurisdiction process to AGENTS.md"
```

---

### Level 3 Checklist

- [ ] Ownership rotation schedule created (quarterly)
- [ ] Rotation playbook with knowledge transfer checklists
- [ ] CI/CD coverage check integrated (GitHub Actions)
- [ ] Metrics dashboard generator created
- [ ] Conflict jurisdiction process documented
- [ ] First rotation executed (if multi-developer team)

**Success Criteria**:
- Quarterly rotation process operational
- CI/CD enforces ≥80% coverage threshold
- Metrics dashboard generated on-demand
- Conflict resolution follows documented jurisdiction

---

## Templates

### CODEOWNERS Template (chora-workspace)

```
# chora-workspace CODEOWNERS
# Defines ownership for 5 primary domains

# Documentation domain
/docs/ @victorpiper
*.md @victorpiper

# Scripts/Automation domain
/scripts/ @victorpiper
justfile @victorpiper

# Coordination/Inbox domain
/inbox/ @victorpiper

# Memory system domain
/.chora/ @victorpiper

# Project management domain
/project-docs/ @victorpiper

# Shared files
/AGENTS.md @victorpiper
/CLAUDE.md @victorpiper
/README.md @victorpiper
```

### Knowledge Transfer Document Template

```markdown
# Domain Ownership Knowledge Transfer

**Domain**: <domain-name>
**Outgoing Owner**: @username
**Incoming Owner**: @username
**Transfer Date**: YYYY-MM-DD

## Domain Overview
- **Scope**: What files/directories are included
- **Boundaries**: What's in vs out of scope
- **Key Files**: Most important files to understand

## Common Patterns
- **Code standards**: Coding conventions, style guide
- **Documentation**: Markdown format, link validation
- **Testing**: Test coverage expectations

## Gotchas
- **Edge Cases**: Tricky scenarios, known issues
- **Workarounds**: Temporary solutions, technical debt
- **Historical Context**: Why things are the way they are

## Tools
- **Scripts**: Automation scripts in scripts/
- **Justfile Recipes**: Domain-specific just commands
- **CI/CD**: GitHub Actions, validation workflows

## Pairing Sessions
- [ ] Session 1: Overview + code walkthrough (Date: ____)
- [ ] Session 2: Shadow review on real PR (Date: ____)

## Post-Handoff
- Incoming owner questions/feedback: ____
- Improvements to knowledge transfer process: ____
```

---

## Troubleshooting

### Issue 1: GitHub Doesn't Auto-Assign Reviewers

**Symptoms**: PR created but no reviewers assigned automatically

**Diagnose**:
```bash
# Check CODEOWNERS file exists
ls -la CODEOWNERS

# Check CODEOWNERS syntax errors
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/codeowners/errors

# Check file patterns match changed files
gh pr diff --name-only
grep "<changed-file-pattern>" CODEOWNERS
```

**Fix**:
1. Ensure CODEOWNERS at repository root (not subdirectory)
2. Validate pattern syntax (absolute paths with leading /)
3. Check owners use @ prefix (@username not username)
4. Verify PR changes files matching CODEOWNERS patterns

---

### Issue 2: Coverage Analysis Shows 0% Coverage

**Symptoms**: `coverage_percent: 0.0` despite CODEOWNERS file existing

**Diagnose**:
```bash
# Check CODEOWNERS patterns
cat CODEOWNERS

# Check if patterns are absolute paths
grep "^/" CODEOWNERS  # Should show patterns starting with /

# Check git tracked files
git ls-files | head -20
```

**Fix**:
1. CODEOWNERS patterns must be absolute paths (`/docs/` not `docs/`)
2. Patterns must match git-tracked files (not build artifacts)
3. Exclude .git, node_modules, build directories from analysis

---

### Issue 3: Ownership Rotation Causes Knowledge Loss

**Symptoms**: Incoming owner struggles after handoff, quality degrades

**Diagnose**:
- Was knowledge transfer checklist completed?
- Were pairing sessions conducted (1-2 minimum)?
- Is outgoing owner available as fallback?

**Fix**:
1. **Extend fallback period**: Outgoing owner stays as fallback for 2-3 months (not 1 month)
2. **Add more pairing sessions**: 3-4 sessions for complex domains
3. **Improve knowledge doc**: Add more examples, gotchas, historical context
4. **Gradual transition**: Incoming owner co-owns domain for 1 month before taking full ownership

---

**Created**: 2025-11-17 by chora-base maintainer + Claude (AI peer)
**Document Status**: Draft
**Last Updated**: 2025-11-17
