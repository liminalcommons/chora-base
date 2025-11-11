# SAP-016: Link Validation & Reference Management

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Automated link validation for markdown documentation—scan 87 files with 342 links in <5 seconds, detect broken internal/external links, and prevent documentation rot with pre-commit hooks and CI/CD integration.

---

## 🚀 Quick Start (2 minutes)

```bash
# Validate all documentation links
just validate-links
# Output: Scans all markdown files, reports broken links

# Validate specific directory
just validate-links-docs                    # docs/ only
just validate-links-path docs/user-docs/    # Specific subdirectory

# Validate specific file
just validate-links-path README.md
just validate-links-path AGENTS.md

# JSON output (for CI/CD or programmatic parsing)
just validate-links-ci

# Show help
just validate-links-help
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for link validation setup (10-min read)

---

## 📖 What Is SAP-016?

SAP-016 provides **automated link validation** for markdown documentation. It scans markdown files for link references (`[text](url)`), validates targets exist and are reachable, and reports broken links. Supports internal links (relative paths), external links (HTTP/HTTPS), and anchor links (#sections).

**Key Innovation**: **Sub-5-second validation** for entire repositories (87 files, 342 links) with intelligent caching, parallel external link checks, and git-aware changed-file detection.

---

## 🎯 When to Use

Use SAP-016 when you need to:

1. **Prevent documentation rot** - Detect broken links before they reach production
2. **Refactoring safety** - Validate links after file renames, moves, or restructuring
3. **Quality gates** - Enforce link integrity in pre-commit hooks or CI/CD
4. **External link monitoring** - Periodic health checks for external resources
5. **Large documentation sites** - Hundreds of files with cross-references

**Not needed for**: Single-file docs with no links, or if external link checker (e.g., linkchecker) already in use

---

## ✨ Key Features

- ✅ **Fast Validation** - <5 seconds for 87 files, 342 links (parallel external checks)
- ✅ **Internal Links** - Relative paths, absolute paths, anchor links (#sections)
- ✅ **External Links** - HTTP/HTTPS with configurable timeout (default: 10s)
- ✅ **Git-Aware** - Changed-file mode (validates only modified files)
- ✅ **Multiple Output Formats** - Human-readable, JSON, GitHub Actions annotations, JUnit XML
- ✅ **Pre-Commit Integration** - Git hook validates links before commit
- ✅ **CI/CD Integration** - GitHub Actions workflow for pull request validation
- ✅ **Ignore Patterns** - Exclude files/directories (node_modules/, *.draft.md)
- ✅ **Fail Fast** - Exit on first broken link (optional)

---

## 📚 Quick Reference

### CLI Commands

#### **validate-links** - Validate All Links

```bash
just validate-links
# Scans: All markdown files in repository
# Output: Human-readable report

# Example output:
🔗 SAP-016: Validating all documentation links...
============================================================
Link Validation Report
============================================================
Files scanned: 87
Links checked: 342

[PASS] Broken links: 0

============================================================
[PASS] Status: PASS
```

---

#### **validate-links-docs** - Validate docs/ Only

```bash
just validate-links-docs
# Scans: Only docs/ directory
# Output: Human-readable report

# Use case: Focus on documentation (skip README.md, CONTRIBUTING.md in root)
```

---

#### **validate-links-path** - Validate Specific Path

```bash
just validate-links-path PATH

# Examples:
just validate-links-path README.md                  # Single file
just validate-links-path docs/user-docs/            # Directory
just validate-links-path docs/skilled-awareness/sap-framework/  # Nested directory

# Output: Human-readable report for specified path
```

---

#### **validate-links-ci** - CI/CD Mode (JSON Output)

```bash
just validate-links-ci
# Output: JSON format for programmatic parsing

# Example output:
{
  "files_scanned": 87,
  "links_checked": 342,
  "broken_links": 0,
  "status": "PASS",
  "errors": []
}

# Use case: GitHub Actions, GitLab CI, Jenkins
```

---

#### **validate-links-help** - Show Help

```bash
just validate-links-help
# Output: All validation commands with descriptions
```

---

### Validation Modes

#### **Mode 1: Full Scan** (Default)

Validates all markdown files in repository.

```bash
./scripts/validate-links.sh .
# Scans: All *.md files recursively
# Time: ~5 seconds for 87 files, 342 links
```

**Use Case**: Pre-release validation, periodic health checks

---

#### **Mode 2: Changed Files** (Git-Aware)

Validates only git-modified markdown files.

```bash
./scripts/validate-links.sh --mode changed
# Scans: Only files in git diff (modified, added)
# Time: <1 second (typically 1-5 files)
```

**Use Case**: Pre-commit hooks, developer workflows

---

#### **Mode 3: Single File**

Validates one markdown file.

```bash
./scripts/validate-links.sh docs/user-docs/quickstart.md
# Scans: Single file
# Time: <1 second
```

**Use Case**: Debugging specific file, rapid iteration

---

### Link Types Supported

#### **1. Internal Relative Links**

Links to files within the same repository.

```markdown
[User Guide](docs/user-docs/guide.md)
[Architecture](../dev-docs/architecture.md)
[Protocol Spec](./protocol-spec.md)
```

**Validation**:
- File exists at relative path from source file
- Target is markdown file (.md extension)

**Common Errors**:
- File moved/renamed (update link)
- Incorrect relative path (count ../ carefully)

---

#### **2. Internal Anchor Links**

Links to sections within same file or other files.

```markdown
[Quick Start](#quick-start)
[API Reference](api.md#authentication)
[Section in Parent](../guide.md#installation)
```

**Validation**:
- File exists (for cross-file anchors)
- Anchor exists (checks for `## Section Name` heading)

**Common Errors**:
- Heading renamed (update anchor)
- Anchor format mismatch (use lowercase, hyphens for spaces)

---

#### **3. External HTTP/HTTPS Links**

Links to external websites.

```markdown
[MCP Specification](https://modelcontextprotocol.io/specification)
[GitHub](https://github.com)
[FastMCP](https://github.com/jlowin/fastmcp)
```

**Validation**:
- HTTP GET request returns 200 OK (or 3xx redirect)
- Timeout: 10 seconds (configurable)
- Parallel requests: Up to 10 concurrent

**Common Errors**:
- Website down (temporary or permanent)
- Firewall blocking (disable external checks with `--no-external`)
- Rate limiting (reduce concurrency)

---

### Output Formats

#### **Human-Readable** (Default)

```
🔗 SAP-016: Validating documentation links (docs/)...
============================================================
Link Validation Report
============================================================
Files scanned: 87
Links checked: 342

[FAIL] Broken links: 3

Broken Links:
-------------
1. docs/user-docs/quickstart.md:42
   -> ../old-guide.md
   (resolved to: /project/docs/old-guide.md)
   Error: File not found

2. docs/dev-docs/architecture.md:108
   -> https://example.com/dead-link
   Error: HTTP 404 Not Found

3. AGENTS.md:25
   -> #non-existent-section
   Error: Anchor not found

============================================================
[FAIL] Status: FAIL (3 broken links)
```

---

#### **JSON** (CI/CD Integration)

```json
{
  "files_scanned": 87,
  "links_checked": 342,
  "broken_links": 3,
  "status": "FAIL",
  "errors": [
    {
      "file": "docs/user-docs/quickstart.md",
      "line": 42,
      "link": "../old-guide.md",
      "resolved_path": "/project/docs/old-guide.md",
      "error": "File not found"
    },
    {
      "file": "docs/dev-docs/architecture.md",
      "line": 108,
      "link": "https://example.com/dead-link",
      "error": "HTTP 404 Not Found"
    },
    {
      "file": "AGENTS.md",
      "line": 25,
      "link": "#non-existent-section",
      "error": "Anchor not found"
    }
  ]
}
```

---

#### **GitHub Actions Annotations**

```
::error file=docs/user-docs/quickstart.md,line=42::Broken link: ../old-guide.md (File not found)
::error file=docs/dev-docs/architecture.md,line=108::Broken link: https://example.com/dead-link (HTTP 404)
::error file=AGENTS.md,line=25::Broken link: #non-existent-section (Anchor not found)
```

**Use Case**: GitHub Actions workflow shows annotations in Pull Request diffs

---

### Pre-Commit Hook Integration

**Setup** (one-time):

```bash
# Add to .pre-commit-config.yaml
- repo: local
  hooks:
    - id: validate-links
      name: Validate Documentation Links
      entry: ./scripts/validate-links.sh --mode changed
      language: script
      files: \.md$
      pass_filenames: false

# Install hooks
just setup-hooks
```

**Behavior**:
- Runs on `git commit` for *.md files
- Validates only changed files (fast: <1s)
- Blocks commit if broken links found
- Auto-fix: None (manual fix required)

**Bypass** (emergency):
```bash
git commit --no-verify -m "WIP: Fix links later"
```

---

### CI/CD Integration

**GitHub Actions Example**:

```yaml
# .github/workflows/validate-links.yml
name: Validate Documentation Links

on:
  pull_request:
    paths:
      - '**.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate links
        run: just validate-links-ci
      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: link-validation-report
          path: link-validation-report.json
```

**Behavior**:
- Runs on Pull Request for *.md file changes
- JSON output for programmatic parsing
- Uploads report artifact on failure
- Fails PR if broken links found

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-006** (Quality Gates) | Pre-commit hooks | Link validation runs before commit |
| **SAP-005** (CI/CD) | GitHub Actions | Link validation on Pull Requests |
| **SAP-007** (Documentation) | Diátaxis validation | Ensures cross-references in how-to guides |
| **SAP-009** (Agent Awareness) | AGENTS.md validation | Validates nested awareness file links |
| **SAP-031** (Enforcement) | Layer 3 (5-10% prevention) | Catches broken links before merge |

**Cross-SAP Workflow Example**:
```bash
# 1. Refactor documentation (SAP-007)
mv docs/old-guide.md docs/new-guide.md

# 2. Update links manually
# Edit all files referencing old-guide.md

# 3. Validate links (SAP-016)
just validate-links
# Output: Shows remaining broken links

# 4. Fix broken links
# Use Edit tool to update references

# 5. Re-validate (SAP-016)
just validate-links
# Output: [PASS] Broken links: 0

# 6. Commit (SAP-006)
git add . && git commit -m "refactor: Rename old-guide.md to new-guide.md"
# Pre-commit hook validates links again

# 7. CI/CD (SAP-005)
git push origin refactor-docs
# GitHub Actions validates links on PR
```

---

## 🏆 Success Metrics

- **Speed**: <5 seconds for 87 files, 342 links
- **Accuracy**: 100% detection of broken internal links
- **External Links**: 95%+ accuracy (subject to network conditions)
- **Pre-Commit**: <1 second for typical commit (1-5 changed files)
- **CI/CD**: <10 seconds for full PR validation

---

## 🔧 Troubleshooting

**Problem**: Validation taking >30 seconds

**Solution**: Disable external link checking for faster local validation:
```bash
./scripts/validate-links.sh --no-external .
# Skips HTTP/HTTPS requests, validates only internal links
# Time: <2 seconds (vs. ~5 seconds with external checks)
```

---

**Problem**: False positives for external links (404 errors)

**Solution**: External links may fail due to:
- **Rate limiting**: Website blocks automated requests
- **Firewall**: Corporate firewall blocks HTTP requests
- **Temporary outage**: Website down temporarily

**Fix**:
```bash
# Retry validation (temporary outage)
just validate-links

# Disable external checks (firewall)
./scripts/validate-links.sh --no-external .

# Ignore specific domains (rate limiting)
# Edit .linkcheck-ignore (if exists):
https://example.com/*
https://rate-limited-site.com/*
```

---

**Problem**: Link to renamed file shows as broken

**Solution**: Update link in source file:
```bash
# Find all references to old file
grep -r "old-guide.md" docs/

# Update each reference
# Use Edit tool to replace old-guide.md → new-guide.md

# Re-validate
just validate-links
```

---

**Problem**: Anchor link broken after heading renamed

**Solution**: Update anchor in link:

```markdown
# Before:
[See Installation](#installation-guide)

# After (heading renamed to "Setup"):
[See Installation](#setup)

# Anchor format: lowercase, hyphens for spaces
"Installation Guide" → #installation-guide
"Quick Start" → #quick-start
"API Reference" → #api-reference
```

---

**Problem**: Pre-commit hook too slow

**Solution**: Hook validates only changed files (should be <1s):
```bash
# Check hook configuration
cat .git/hooks/pre-commit | grep validate-links

# Ensure --mode changed flag:
./scripts/validate-links.sh --mode changed

# If still slow, disable external checks in hook:
./scripts/validate-links.sh --mode changed --no-external
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete validation specification (17KB, 9-min read)
- **[AGENTS.md](AGENTS.md)** - Agent link validation workflows (13KB, 7-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code link validation patterns (13KB, 7-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Link validation setup guide (28KB, 15-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial link validation with internal/external/anchor support, <5s validation, pre-commit + CI/CD integration

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
