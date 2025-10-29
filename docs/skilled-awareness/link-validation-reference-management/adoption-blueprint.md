# Link Validation & Reference Management
## Adoption Blueprint

**SAP ID**: SAP-016
**Target Audience**: DevOps Engineers, Documentation Maintainers, Project Leads
**Adoption Time**: 1-2 hours (initial setup + validation run)

---

## Adoption Overview

This blueprint guides you through installing and integrating link validation into your project.

**What you'll accomplish**:
- ✅ Install link validation script
- ✅ Run first validation on your documentation
- ✅ Fix any broken links found
- ✅ Integrate into CI/CD pipeline
- ✅ Set up optional pre-commit hooks

**Prerequisites**:
- Bash 4.0+ (Linux, macOS, or WSL on Windows)
- `curl` or `wget` (for external link checking)
- Git repository (for changed-files mode and hooks)
- Markdown documentation (`.md` files)

**Estimated time**:
- Installation: 10 minutes
- First validation run: 5-15 minutes (depends on repository size)
- Fix broken links: Variable (30 minutes to 2 hours)
- CI/CD integration: 20-30 minutes
- Pre-commit hooks (optional): 15 minutes

---

## Phase 1: Installation (10 minutes)

### Step 1.1: Copy Validation Script

**For chora-base itself** (already included):
```bash
# Script already exists at:
ls -la scripts/validate-links.sh
```

**For external projects** (cloning from chora-base):
```bash
# If you cloned chora-base, the script is already in scripts/
# If you're integrating into an existing project:

# Option A: Copy from chora-base clone
cp /path/to/chora-base/scripts/validate-links.sh ./scripts/

# Option B: Download directly (once published)
curl -o scripts/validate-links.sh https://raw.githubusercontent.com/[org]/chora-base/main/scripts/validate-links.sh

# Make executable
chmod +x scripts/validate-links.sh
```

### Step 1.2: Verify Dependencies

**Check Bash version**:
```bash
bash --version
# Required: GNU bash, version 4.0+ or higher
```

**Check curl (preferred)**:
```bash
curl --version
# If installed, you're good
```

**Or check wget (alternative)**:
```bash
wget --version
# Script will use wget if curl not available
```

**Check other standard tools** (should be present on all Unix-like systems):
```bash
which grep sed find
# All should return paths
```

### Step 1.3: Test Installation

**Run help command**:
```bash
./scripts/validate-links.sh --help
```

**Expected output**:
```
Link Validation Script v1.0

Usage: validate-links.sh [OPTIONS] [PATH]

OPTIONS:
  --mode MODE          Validation mode: full (default), changed, single
  --no-external        Disable external link checking
  --format FORMAT      Output format: human (default), json, github, junit
  --ignore PATTERN     Exclude files matching pattern (can be repeated)
  --fail-fast          Exit on first broken link
  --timeout SECONDS    External link timeout (default: 10)
  --help               Show this help message

EXAMPLES:
  validate-links.sh .
  validate-links.sh docs/skilled-awareness/sap-framework/
  validate-links.sh --mode changed
  validate-links.sh --no-external --format json .
```

**Validation**: If you see this output, installation is successful!

---

## Phase 2: First Validation Run (5-15 minutes)

### Step 2.1: Start with Small Scope

**Validate a single file** (fastest test):
```bash
./scripts/validate-links.sh README.md
```

**Expected output** (if README.md has valid links):
```
✅ Link Validation Report

Scanned: 1 file
Total links: 15 links
  - Internal: 12 (100% valid)
  - External: 3 (100% valid)

Status: PASS ✅
Runtime: 2 seconds
```

**If broken links found**:
```
❌ Link Validation Report

Scanned: 1 file
Total links: 15 links
  - Internal: 12 (1 broken)
  - External: 3 (100% valid)

Status: FAIL ❌

Broken Links:
  1. README.md:42
     → docs/old-file.md
     ERROR: File does not exist

Runtime: 2 seconds
```

**Action**: Note broken links for fixing in Step 2.3.

---

### Step 2.2: Validate Full Repository

**Run full validation**:
```bash
./scripts/validate-links.sh .
```

**What happens**:
1. Script scans all `.md` files in repository
2. Extracts all markdown links
3. Validates internal links (file existence)
4. Validates external links (HTTP reachability)
5. Reports broken links with file paths and line numbers

**Performance expectations**:
- Small repo (~50 files): 10-15 seconds
- Medium repo (~200 files): 30-60 seconds
- Large repo (~500 files): 90-120 seconds
- External links add 5-10 seconds per 100 links

**Save output for review**:
```bash
./scripts/validate-links.sh . | tee link-validation-report.txt
```

---

### Step 2.3: Fix Broken Links

**For each broken link reported**:

**Example broken link**:
```
  1. docs/skilled-awareness/sap-framework/awareness-guide.md:89
     → ../../dev-docs/workflows/missing-workflow.md
     ERROR: File does not exist
```

**How to fix**:

1. **Open the file**:
   ```bash
   # Open in your editor
   code docs/skilled-awareness/sap-framework/awareness-guide.md:89
   # Or vim, nano, etc.
   ```

2. **Locate the broken link** (line 89):
   ```markdown
   See the [Migration Workflow](../../dev-docs/workflows/missing-workflow.md).
   ```

3. **Determine fix strategy**:

   **Strategy A: Update path** (file exists elsewhere):
   ```markdown
   <!-- Find correct path -->
   find docs -name "missing-workflow.md"
   # Result: docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md

   <!-- Update link -->
   See the [Migration Workflow](../../dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md).
   ```

   **Strategy B: Remove link** (file doesn't exist and shouldn't):
   ```markdown
   <!-- Remove link, keep text -->
   See the Migration Workflow (coming soon).
   ```

   **Strategy C: Create missing file** (file should exist):
   ```bash
   # Create the missing file
   touch docs/dev-docs/workflows/missing-workflow.md
   # Add minimal content (don't leave empty)
   echo "# Missing Workflow\n\nTODO: Document this workflow." > docs/dev-docs/workflows/missing-workflow.md
   ```

4. **Re-validate after fixing**:
   ```bash
   ./scripts/validate-links.sh docs/skilled-awareness/sap-framework/awareness-guide.md
   ```

5. **Repeat for all broken links** until validation passes.

**Efficiency tip**: Group similar fixes (e.g., all references to moved file) and use `sed`:
```bash
# If docs/BENEFITS.md moved to docs/user-docs/explanation/benefits-of-chora-base.md
# Update all references at once:
find docs -name "*.md" -exec sed -i '' 's|docs/BENEFITS.md|docs/user-docs/explanation/benefits-of-chora-base.md|g' {} +

# Re-validate
./scripts/validate-links.sh .
```

---

### Step 2.4: Validate Success

**Run validation again** (should pass now):
```bash
./scripts/validate-links.sh .
```

**Expected**:
```
✅ Link Validation Report

Scanned: 127 markdown files
Total links: 1,543 links
  - Internal: 1,401 (100% valid)
  - External: 142 (100% valid)

Status: PASS ✅
Runtime: 47 seconds
```

**Commit fixes**:
```bash
git add -A
git commit -m "fix: Resolve all broken markdown links

- Updated paths after documentation restructure
- Removed references to deleted files
- Created placeholder docs for missing references

✅ Link validation passing (0 broken links)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Phase 3: CI/CD Integration (20-30 minutes)

### GitHub Actions Integration

**Create workflow file**: `.github/workflows/link-validation.yml`

```yaml
name: Link Validation

on:
  pull_request:
    paths:
      - '**.md'
      - 'scripts/validate-links.sh'
  push:
    branches:
      - main
    paths:
      - '**.md'

jobs:
  validate-links:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Make Script Executable
        run: chmod +x scripts/validate-links.sh

      - name: Validate Markdown Links
        id: validation
        run: |
          ./scripts/validate-links.sh --format github .
        continue-on-error: true

      - name: Comment on PR (if failed)
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ **Link validation failed**\n\nPlease fix broken links before merging. Run `./scripts/validate-links.sh .` locally to see details.'
            })

      - name: Fail if Validation Failed
        if: steps.validation.outcome == 'failure'
        run: exit 1
```

**Commit and push**:
```bash
git add .github/workflows/link-validation.yml
git commit -m "ci: Add link validation to CI pipeline

- Validates markdown links on all PRs
- Blocks merge if broken links found
- Comments on PR with failure message

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

**Test**:
1. Create a branch with a broken link
2. Open a pull request
3. CI should fail with link validation error
4. PR should show comment about broken links

---

### GitLab CI Integration

**Add job to `.gitlab-ci.yml`**:

```yaml
stages:
  - test

link-validation:
  stage: test
  image: ubuntu:latest
  script:
    - apt-get update && apt-get install -y curl
    - chmod +x scripts/validate-links.sh
    - ./scripts/validate-links.sh --format junit . > link-validation-report.xml
  artifacts:
    reports:
      junit: link-validation-report.xml
  only:
    changes:
      - "**/*.md"
      - scripts/validate-links.sh
```

**Commit**:
```bash
git add .gitlab-ci.yml
git commit -m "ci: Add link validation to GitLab CI"
git push
```

---

### Jenkins Integration

**Add stage to Jenkinsfile**:

```groovy
pipeline {
  agent any

  stages {
    stage('Link Validation') {
      when {
        changeset "**/*.md"
      }
      steps {
        sh 'chmod +x scripts/validate-links.sh'
        sh './scripts/validate-links.sh --format junit . > link-validation-report.xml'
      }
      post {
        always {
          junit 'link-validation-report.xml'
        }
      }
    }
  }
}
```

---

### Other CI Systems

**Generic bash integration** (works with any CI):

```bash
#!/bin/bash
# ci-link-validation.sh

set -e

# Make script executable
chmod +x scripts/validate-links.sh

# Run validation
if ./scripts/validate-links.sh .; then
  echo "✅ Link validation passed"
  exit 0
else
  echo "❌ Link validation failed"
  exit 1
fi
```

**Use in CI**:
- CircleCI: Add to `.circleci/config.yml` as a step
- Travis CI: Add to `.travis.yml` in `script:` section
- Bitbucket Pipelines: Add to `bitbucket-pipelines.yml`

---

## Phase 4: Pre-Commit Hook (Optional, 15 minutes)

**Benefits**:
- Catch broken links before committing
- Faster feedback loop (no waiting for CI)
- Only validates changed files (very fast)

**Drawbacks**:
- Requires manual setup per developer
- Can slow down commits slightly
- Not enforced (developers can skip with `--no-verify`)

### Step 4.1: Create Pre-Commit Hook

**Create file**: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit hook for link validation

# Get staged markdown files
STAGED_MD_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)

if [ -z "$STAGED_MD_FILES" ]; then
  # No markdown files staged, skip validation
  exit 0
fi

echo "Validating links in staged markdown files..."

# Validate each staged file
VALIDATION_FAILED=0
for file in $STAGED_MD_FILES; do
  if [ -f "$file" ]; then
    if ! ./scripts/validate-links.sh "$file" > /dev/null 2>&1; then
      echo "❌ Broken links found in: $file"
      ./scripts/validate-links.sh "$file"
      VALIDATION_FAILED=1
    fi
  fi
done

if [ $VALIDATION_FAILED -eq 1 ]; then
  echo ""
  echo "❌ Link validation failed. Please fix broken links before committing."
  echo "   Or skip validation with: git commit --no-verify"
  exit 1
fi

echo "✅ All links valid"
exit 0
```

**Make executable**:
```bash
chmod +x .git/hooks/pre-commit
```

### Step 4.2: Test Pre-Commit Hook

**Create test commit with broken link**:
```bash
# Edit a markdown file with broken link
echo "[Broken Link](./nonexistent.md)" >> README.md

# Try to commit
git add README.md
git commit -m "test: broken link"
```

**Expected output**:
```
Validating links in staged markdown files...
❌ Broken links found in: README.md

❌ Link Validation Report
...
  1. README.md:XX
     → ./nonexistent.md
     ERROR: File does not exist
...

❌ Link validation failed. Please fix broken links before committing.
   Or skip validation with: git commit --no-verify
```

**Fix and retry**:
```bash
# Remove broken link
git checkout README.md

# Commit should succeed
git commit -m "test: valid commit"
```

**Expected output**:
```
Validating links in staged markdown files...
✅ All links valid
[main abc1234] test: valid commit
 1 file changed, 1 insertion(+)
```

---

### Step 4.3: Share with Team (Optional)

**Git hooks are not version controlled**, so each developer must set up manually.

**Create setup script**: `scripts/setup-git-hooks.sh`

```bash
#!/bin/bash
# Setup Git hooks for link validation

echo "Setting up Git hooks..."

# Copy pre-commit hook
cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed"
echo ""
echo "Link validation will run automatically on markdown files."
echo "To skip validation, use: git commit --no-verify"
```

**Add template to version control**: `scripts/git-hooks/pre-commit`
```bash
# Move the hook template to version-controlled location
mkdir -p scripts/git-hooks
cp .git/hooks/pre-commit scripts/git-hooks/pre-commit

# Commit
git add scripts/git-hooks/pre-commit scripts/setup-git-hooks.sh
git commit -m "chore: Add link validation pre-commit hook template"
```

**Document in README**:
```markdown
## Developer Setup

After cloning the repository:

1. Install Git hooks:
   ```bash
   ./scripts/setup-git-hooks.sh
   ```

This enables automatic link validation before committing.
```

---

## Phase 5: Periodic Health Checks (Optional, 10 minutes)

**Purpose**: Detect external link rot over time.

**Setup**: GitHub Actions scheduled workflow

**Create file**: `.github/workflows/weekly-link-check.yml`

```yaml
name: Weekly Link Health Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  check-links:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Validate All Links
        run: |
          chmod +x scripts/validate-links.sh
          ./scripts/validate-links.sh --format json . > link-report.json
        continue-on-error: true

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: link-health-report
          path: link-report.json
          retention-days: 30

      - name: Check for Failures
        id: check
        run: |
          if ! ./scripts/validate-links.sh . ; then
            echo "has_failures=true" >> $GITHUB_OUTPUT
          else
            echo "has_failures=false" >> $GITHUB_OUTPUT
          fi

      - name: Create Issue (if failures)
        if: steps.check.outputs.has_failures == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '⚠️ Weekly Link Health Check Failed',
              body: 'Broken links detected in documentation. See [workflow run](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}) for details.',
              labels: ['documentation', 'maintenance']
            })
```

**Commit**:
```bash
git add .github/workflows/weekly-link-check.yml
git commit -m "ci: Add weekly link health check

- Runs every Monday at 9am UTC
- Creates GitHub issue if broken links found
- Uploads detailed report as artifact

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Phase 6: Validation & Success Criteria

### Validation Checklist

Before considering SAP-016 fully adopted:

- [ ] **Installation Complete**
  - [ ] `scripts/validate-links.sh` exists and is executable
  - [ ] Script runs successfully (`--help` works)
  - [ ] Dependencies verified (bash, curl/wget, grep, sed)

- [ ] **First Validation Passed**
  - [ ] Full repository validation run
  - [ ] All broken links identified and fixed
  - [ ] Validation passes with 0 errors

- [ ] **CI/CD Integrated**
  - [ ] Workflow file created (GitHub Actions, GitLab CI, etc.)
  - [ ] Test PR created and validated (CI runs link validation)
  - [ ] PR merge blocked when links broken (quality gate working)

- [ ] **Optional Enhancements**
  - [ ] Pre-commit hook installed (optional)
  - [ ] Weekly health check scheduled (optional)
  - [ ] Team documentation updated (README, CONTRIBUTING)

### Success Criteria

**Minimum Viable Adoption** (required):
- ✅ Link validation script functional
- ✅ Full repository validation passes (0 broken internal links)
- ✅ CI/CD integration complete (blocks broken links)

**Full Adoption** (recommended):
- ✅ All above
- ✅ Pre-commit hooks documented for team
- ✅ Weekly external link health checks
- ✅ Link validation mentioned in documentation quality guidelines

**Excellence** (aspirational):
- ✅ All above
- ✅ Link health metrics tracked over time
- ✅ External adopters report successful link validation
- ✅ Zero broken links in every release

---

## Troubleshooting

### Issue 1: Script Not Executable

**Symptom**:
```
bash: ./scripts/validate-links.sh: Permission denied
```

**Solution**:
```bash
chmod +x scripts/validate-links.sh
```

---

### Issue 2: Curl Not Found

**Symptom**:
```
validate-links.sh: line 42: curl: command not found
```

**Solution** (install curl):
```bash
# macOS
brew install curl

# Ubuntu/Debian
sudo apt-get install curl

# CentOS/RHEL
sudo yum install curl

# Or use wget (script will fall back automatically)
```

---

### Issue 3: False Positive - Link Works But Validation Fails

**Symptom**:
```
README.md:42 → docs/foo.md
ERROR: File does not exist
```

But `docs/foo.md` exists when you check manually.

**Possible causes**:
1. **Case sensitivity**: Linux is case-sensitive, macOS/Windows are not
   - Solution: Ensure exact case match (`Foo.md` ≠ `foo.md`)

2. **Relative path from wrong location**: Link is relative to wrong directory
   - Solution: Update link to correct relative path or use absolute path

3. **File in .gitignore**: File exists locally but not in repository
   - Solution: Remove from .gitignore or use `--ignore` flag

---

### Issue 4: External Link False Positive (Timeout)

**Symptom**:
```
README.md:42 → https://valid-site.com
WARNING: Timeout (may be temporary)
```

But the site loads fine in your browser.

**Possible causes**:
1. **Network latency**: Site is slow to respond
   - Solution: Increase timeout (`--timeout 30`)

2. **Rate limiting**: Too many requests to same domain
   - Solution: Re-run validation after a few minutes

3. **Firewall/VPN**: Network restrictions
   - Solution: Check network configuration, or disable external validation locally (`--no-external`)

---

### Issue 5: CI Validation Fails But Local Passes

**Symptom**: CI reports broken links, but `./scripts/validate-links.sh .` passes locally.

**Possible causes**:
1. **File not committed**: Link target exists locally but not in git
   - Solution: `git add` missing files

2. **Case sensitivity**: Works on macOS/Windows, fails on Linux CI
   - Solution: Fix case to match exactly

3. **Network issues in CI**: External links timing out in CI environment
   - Solution: Disable external validation in CI (`--no-external`)

---

## Customization

### Ignore Patterns

**Exclude specific files or directories**:

```bash
# Ignore drafts
./scripts/validate-links.sh --ignore "*.draft.md" .

# Ignore multiple patterns
./scripts/validate-links.sh --ignore "node_modules/*" --ignore "vendor/*" --ignore "*.tmp.md" .

# Create wrapper script with default ignores
# scripts/validate-links-custom.sh
#!/bin/bash
./scripts/validate-links.sh \
  --ignore "node_modules/*" \
  --ignore "vendor/*" \
  --ignore ".archive/*" \
  "$@"
```

### Disable External Validation

**For faster local validation** (skip external HTTP checks):

```bash
./scripts/validate-links.sh --no-external .
```

**In CI** (if external links are unreliable):

```yaml
# .github/workflows/link-validation.yml
- name: Validate Markdown Links (Internal Only)
  run: ./scripts/validate-links.sh --no-external .
```

### Custom Output Format

**JSON output** (for scripting):

```bash
./scripts/validate-links.sh --format json . > report.json

# Parse with jq
jq '.errors | length' report.json  # Count errors
jq '.errors[] | .file' report.json  # List files with errors
```

**JUnit XML** (for CI reporting):

```bash
./scripts/validate-links.sh --format junit . > junit-report.xml
```

---

## Project-Specific Adaptations

### For Monorepos

**Validate specific packages**:

```bash
# Validate docs in specific package
./scripts/validate-links.sh packages/my-package/docs/

# Or create per-package wrapper scripts
# packages/my-package/scripts/validate-docs.sh
#!/bin/bash
cd "$(dirname "$0")/../.."
./scripts/validate-links.sh packages/my-package/docs/
```

### For Multi-Language Projects

**Validate language-specific docs**:

```bash
# English docs only
./scripts/validate-links.sh docs/en/

# All languages
for lang in en es fr de; do
  echo "Validating $lang docs..."
  ./scripts/validate-links.sh docs/$lang/
done
```

### For Generated Documentation

**Validate after build**:

```bash
# Build docs
npm run build:docs

# Validate generated markdown
./scripts/validate-links.sh dist/docs/
```

---

## Migration from Other Tools

### From markdown-link-check

**markdown-link-check** is a popular Node.js-based link checker.

**Key differences**:
- SAP-016: Bash script, no dependencies beyond standard Unix tools
- markdown-link-check: Node.js package, requires npm install

**Migration steps**:
1. Remove markdown-link-check from package.json
2. Install SAP-016 validation script
3. Update CI/CD to use new script
4. Test validation on full repository

**Command mapping**:
```bash
# markdown-link-check
npx markdown-link-check README.md

# SAP-016 equivalent
./scripts/validate-links.sh README.md
```

---

### From lychee

**lychee** is a Rust-based link checker.

**Key differences**:
- SAP-016: Markdown-focused, simpler output
- lychee: Multi-format (HTML, Markdown), more complex

**Migration steps**:
1. Remove lychee binary or cargo install
2. Install SAP-016 validation script
3. Update CI/CD configuration
4. Test validation on documentation

**Command mapping**:
```bash
# lychee
lychee docs/

# SAP-016 equivalent
./scripts/validate-links.sh docs/
```

---

## Support & Resources

### Documentation

- [Capability Charter](./capability-charter.md) - Business value and scope
- [Protocol Specification](./protocol-spec.md) - Technical details
- [Awareness Guide](./awareness-guide.md) - Usage examples and patterns
- [Ledger](./ledger.md) - Adoption history and feedback

### Related Workflows

- [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) - Uses link validation in Step 3
- [Documentation Migration Workflow](../../dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) - Link validation after file moves

### Community

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions, share use cases
- Pull Requests: Contribute improvements

---

## Next Steps

**After completing adoption**:

1. **Document in your project**:
   - Add link validation section to README
   - Update CONTRIBUTING guide with validation requirements
   - Mention in documentation quality guidelines

2. **Monitor link health**:
   - Review weekly health check reports
   - Track broken link trends over time
   - Address external link rot proactively

3. **Share learnings**:
   - Update SAP-016 ledger with your feedback
   - Contribute improvements to validation script
   - Help other projects adopt link validation

4. **Expand quality gates**:
   - Integrate with other quality tools (markdownlint, spell check)
   - Add link validation to release checklists
   - Include link health in project metrics

---

**Blueprint Version**: 1.0
**Created**: 2025-10-28 (Wave 2)
**Status**: Active

This adoption blueprint demonstrates chora-base's skilled-awareness/ domain: step-by-step installation and integration guide for a portable capability package.
