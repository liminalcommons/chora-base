# Adoption Blueprint: SAP Generation Automation

**SAP ID**: SAP-029
**Version**: 1.0.0
**Last Updated**: 2025-11-02

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-029 SAP Generation Automation across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Manual generation via Python script | 10-11 hours | Per-SAP basis (2-4h each) | First SAP, understanding the system, ad-hoc generation |
| **Level 2: Advanced** | Batch generation + extended schema | 12-15 hours | Monthly template updates (1-2h) | Multiple SAPs (5-10), domain-specific templates, team adoption |
| **Level 3: Mastery** | Automated pipeline + custom templates | 25-31 hours | Monthly refinements (1-2h) | **Recommended for production** - Large SAP ecosystems (20+ SAPs), CI/CD integration |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
- **First-time SAP generation**: Creating your first 1-2 SAPs to understand the workflow
- **Learning the system**: Understanding SAP structure, template logic, and catalog integration
- **Ad-hoc generation**: One-off SAP creation without ongoing automation needs
- **Small SAP ecosystems**: Projects with <5 SAPs total
- **Proof-of-concept**: Validating whether SAP generation fits your workflow before scaling

### Time Estimate

- **Setup**: 10-11 hours (one-time investment: 8.5h setup + 2-3h first SAP generation and manual fill)
- **Learning Curve**: Moderate - Requires understanding SAP structure, catalog JSON format, and Jinja2 basics

### Prerequisites

**Required**:
- Python 3.9+ installed and available in PATH
- Jinja2 library installed (`pip install jinja2`)
- Git repository with chora-base structure (or adopting chora-base patterns)
- Write access to `sap-catalog.json` in repository root
- Basic understanding of SAP structure (read 1-2 reference SAPs)

**Recommended**:
- `just` command runner installed for convenience recipes
- Familiarity with Jinja2 templating (for template customization)
- Read pilot documentation (docs/project-docs/dogfooding-pilot/)

### Step-by-Step Instructions

#### Step 1.1: Install Prerequisites and Create Templates Directory

**Action**:
```bash
# Install Python dependencies
pip install jinja2

# Verify Python 3.9+ and Jinja2 installed
python --version  # Should be 3.9 or higher
python -c "import jinja2; print(f'Jinja2 {jinja2.__version__}')"

# Create templates directory structure
mkdir -p templates/sap/
```

**Expected Output**:
```
Python 3.11.5
Jinja2 3.1.2
```

**Verification**:
```bash
# Verify directory structure exists
test -d templates/sap/ && echo "✅ Templates directory ready" || echo "❌ Directory missing"

# Verify Jinja2 is importable
python -c "import jinja2" && echo "✅ Jinja2 installed" || echo "❌ Jinja2 missing"
```

#### Step 1.2: Add SAP Entry to Catalog and Generate Artifacts

**Action**:
```bash
# Add new SAP entry to sap-catalog.json
# Manually add this entry to the "saps" array in sap-catalog.json:
cat <<EOF
{
  "id": "SAP-030",
  "name": "database-migrations",
  "status": "draft",
  "version": "0.1.0",
  "description": "Database migration automation for Python projects",
  "tags": ["backend", "database", "automation"],
  "dependencies": ["SAP-000"]
}
EOF

# Generate SAP artifacts using the generator script
python scripts/generate-sap.py SAP-030

# OR using justfile if available:
just generate-sap SAP-030
```

**Expected Output**:
```
🔍 Generating SAP-030 (database-migrations)...
✅ Created docs/skilled-awareness/database-migrations/
✅ Generated capability-charter.md (45 lines, 8 TODOs)
✅ Generated protocol-spec.md (120 lines, 15 TODOs)
✅ Generated awareness-guide.md (95 lines, 12 TODOs)
✅ Generated adoption-blueprint.md (180 lines, 25 TODOs)
✅ Generated AGENTS.md (85 lines, 6 TODOs)
✅ Generated CLAUDE.md (110 lines, 10 TODOs)
✅ Generated ledger.md (60 lines, 5 TODOs)

📊 Summary: 7 files created, 81 TODOs to fill
⏱️ Estimated manual fill time: 2-3 hours
```

#### Step 1.3: Fill TODOs and Validate Generated SAP

**Action**:
```bash
# Review generated files for TODO markers
grep -r "TODO" docs/skilled-awareness/database-migrations/

# Fill in TODOs manually (2-3 hours)
# Start with high-priority files:
# 1. protocol-spec.md (technical contracts)
# 2. awareness-guide.md (agent quick reference)
# 3. capability-charter.md (problem/solution)
# 4. adoption-blueprint.md (installation guide)

# Validate the completed SAP
python scripts/sap-evaluator.py --quick SAP-030

# OR using justfile:
just validate-sap SAP-030
```

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] Python 3.9+ and Jinja2 installed and working
- [ ] Templates directory created (templates/sap/)
- [ ] Generator script executable (scripts/generate-sap.py exists)
- [ ] First SAP generated successfully (7 artifact files created)
- [ ] SAP entry added to sap-catalog.json
- [ ] TODOs filled in generated artifacts (<10 TODOs remaining is acceptable for Level 1)
- [ ] sap-evaluator.py validates the generated SAP without errors
- [ ] Basic functionality works as expected

#### Validation Commands

```bash
# Primary validation
python scripts/sap-evaluator.py --quick SAP-029

# Expected output:
# ✅ SAP-029 (sap-generation)
#    Level: 1
#    Next: Level 2
# ✅ Validation passed
```

### Common Issues (Level 1)

**Issue 1**: Unicode encoding error when running sap-evaluator.py
- **Cause**: Windows console default encoding (cp1252) can't handle Unicode emoji characters (✅, ❌, 🔍)
- **Solution**: Use generator's validation integration (`python scripts/generate-sap.py SAP-029`) or justfile (`just validate-sap SAP-029`) which set UTF-8 environment variable
- **Alternative**: Add `sys.stdout.reconfigure(encoding='utf-8')` to sap-evaluator.py

**Issue 2**: High TODO count after generation (~60-105 placeholders)
- **Cause**: By design per 80/20 rule - MVP schema (9 fields) provides 50-60% automation, 40-50% manual fill required
- **Solution**: Expected behavior. Budget 2-4 hours for manual TODO fill. Technical SAPs (security/CI-CD) have +75% more TODOs than meta SAPs.
- **Note**: TODOs provide clear guidance on what content to add

**Issue 3**: "SAP not found in catalog" error
- **Cause**: Typo in SAP ID, or SAP entry missing from sap-catalog.json
- **Solution**: Check spelling (SAP-029 not SAP029), verify entry exists in catalog with correct `id` field

**Issue 4**: Generator wants to overwrite existing files
- **Cause**: SAP artifacts already exist from previous generation or manual creation
- **Solution**: Use `--force` flag to overwrite (`python scripts/generate-sap.py SAP-029 --force`) or delete existing files first

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds:
- **Extended schema**: Add custom fields beyond MVP 9-field schema (e.g., `stakeholders`, `metrics`, `integration_points`)
- **Batch generation**: Generate multiple SAPs in one command for domain-specific SAP families
- **Domain-specific templates**: Customize templates for technical domains (backend, frontend, DevOps)
- **Template inheritance**: Create base templates with domain-specific overrides
- **Validation automation**: Integrate sap-evaluator.py into generation workflow

### Time Estimate

- **Setup**: 25 minutes per additional SAP (5min generation + 20min validation/review)
- **Total from Start**: 10-11 hours + (N SAPs × 25 minutes) + (2-4 hours manual fill per SAP)

### Prerequisites

**Required**:
- ✅ Level 1 adoption complete
- Completed at least 2-3 SAPs using Level 1 (understand TODO patterns and domain needs)
- Git repository with organized SAP directory structure
- Understanding of Jinja2 template syntax (for customization)

### Step-by-Step Instructions

#### Step 2.1: Extend Schema with Custom Fields

**Action**:
```bash
# Edit generator script to add custom schema fields
# Add to SAP metadata in sap-catalog.json:
{
  "id": "SAP-031",
  "name": "routing-navigation",
  "status": "draft",
  "version": "0.1.0",
  "description": "Next.js routing and navigation patterns",
  "tags": ["frontend", "react", "nextjs"],
  "dependencies": ["SAP-000", "SAP-017"],
  "stakeholders": ["frontend-team", "ux-designers"],
  "metrics": {
    "time_savings_target": "5x",
    "satisfaction_target": 0.85
  }
}

# Customize templates to use extended schema
# Edit templates/sap/capability-charter.md.j2 to include:
# ## Stakeholders
# {{ sap.stakeholders | join(', ') }}
```

**Expected Output**:
```
✅ Extended schema fields added to SAP-031 catalog entry
✅ Templates updated to render custom fields
```

#### Step 2.2: Create Domain-Specific Templates

**Action**:
```bash
# Create domain-specific template directory
mkdir -p templates/sap/frontend/
mkdir -p templates/sap/backend/
mkdir -p templates/sap/devops/

# Copy base templates and customize for domain
cp templates/sap/protocol-spec.md.j2 templates/sap/frontend/protocol-spec.md.j2

# Edit frontend-specific template to add React patterns, component examples, etc.
# Update generator to support --domain flag:
python scripts/generate-sap.py SAP-031 --domain frontend
```

**Expected Output**:
```
🔍 Generating SAP-031 (routing-navigation) with frontend domain...
✅ Using domain-specific templates from templates/sap/frontend/
✅ Generated with frontend-specific patterns (React hooks, Next.js routing)
```

#### Step 2.3: Implement Batch Generation

**Action**:
```bash
# Create batch configuration file
cat > batch-generate.yaml <<EOF
batch:
  - id: SAP-031
    domain: frontend
  - id: SAP-032
    domain: frontend
  - id: SAP-033
    domain: backend
EOF

# Run batch generation
python scripts/generate-sap.py --batch batch-generate.yaml

# Validate all generated SAPs
for sap in SAP-031 SAP-032 SAP-033; do
  python scripts/sap-evaluator.py --quick $sap
done
```

### Configuration

#### Level 2 Configuration File

```yaml
# Configuration for Level 2 (.chora/config.yaml or project root)
sap-generation:
  enabled: true
  level: 2

  schema:
    # Extended schema fields beyond MVP
    extended_fields:
      - stakeholders
      - metrics
      - integration_points
      - external_apis

  templates:
    # Domain-specific template paths
    domains:
      frontend: templates/sap/frontend/
      backend: templates/sap/backend/
      devops: templates/sap/devops/

    # Template inheritance
    base_template: templates/sap/
    fallback_to_base: true

  generation:
    # Batch generation settings
    batch_mode: true
    validate_after_generation: true
    auto_add_to_catalog: true

  validation:
    # Auto-run sap-evaluator after generation
    auto_validate: true
    fail_on_error: false  # Allow manual TODO fill before strict validation
```

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] All Level 1 checks still pass
- [ ] Extended schema fields render correctly in generated SAPs
- [ ] Domain-specific templates exist for 2+ domains (frontend, backend, or devops)
- [ ] Batch generation successfully creates multiple SAPs in one command
- [ ] Auto-validation runs after generation (sap-evaluator.py integration)
- [ ] Template inheritance works (domain templates fall back to base templates)
- [ ] Level 2 configuration file (.chora/config.yaml) exists and is valid
- [ ] Advanced features working

#### Validation Commands

```bash
# Level 2 validation
python scripts/sap-evaluator.py --level 2 SAP-029

# Validate batch-generated SAPs
for sap in SAP-031 SAP-032 SAP-033; do
  python scripts/sap-evaluator.py --quick $sap
done

# Check template inheritance
python scripts/generate-sap.py SAP-034 --domain frontend --dry-run --verbose
```

### Common Issues (Level 2)

**Issue 1**: Extended schema fields not rendering in templates
- **Cause**: Templates not updated to use new schema fields, or catalog entry missing extended fields
- **Solution**: Edit Jinja2 templates to include `{{ sap.stakeholders }}` or other extended fields. Verify sap-catalog.json has the extended fields in the SAP entry.

**Issue 2**: Batch generation fails partway through
- **Cause**: One SAP ID in batch file is invalid or already exists without --force flag
- **Solution**: Add `--force` flag to batch generation command, or verify all SAP IDs in batch-generate.yaml are correct and not duplicates.

---

## Level 3: Mastery - **RECOMMENDED**

### Purpose

Level 3 adoption provides:
- **CI/CD integration**: Automated SAP generation in GitHub Actions, GitLab CI, or other pipelines
- **Custom template engine extensions**: Jinja2 filters, macros, and template functions for complex logic
- **SAP dependency resolution**: Auto-generate dependent SAPs (e.g., generate SAP-031 when it depends on SAP-017)
- **Quality gates**: Enforce TODO completion thresholds (<10 TODOs), link validation, and artifact completeness
- **SAP versioning automation**: Auto-increment versions, generate CHANGELOGs, create git tags
- **Production-ready configuration**: Monitoring, error handling, rollback strategies
- **Best practices and optimizations**: Template caching, parallel generation, incremental updates

### Time Estimate

- **Setup**: 15-20 hours (includes extended schema design, batch generation, domain-specific templates)
- **Total from Start**: 25-31 hours (Level 1 + Level 2 + Level 3 enhancements)
- **Maintenance**: Monthly template refinements (1-2 hours/month), schema expansions as needed

### Prerequisites

**Required**:
- ✅ Level 2 adoption complete
- Generated 5+ SAPs with Level 2 features (understand template patterns and domain needs)
- CI/CD pipeline infrastructure (GitHub Actions, GitLab CI, or equivalent)
- Git repository with branch protection and code review workflow

**Recommended**:
- SAP-005 (CI/CD Workflows) adopted for integration patterns
- SAP-016 (Link Validation) adopted for quality gates
- Monitoring infrastructure for generation metrics (success rate, generation time, TODO count)

### Step-by-Step Instructions

#### Step 3.1: Set Up CI/CD Integration

**Action**:
```bash
# Create GitHub Actions workflow for automated SAP generation
mkdir -p .github/workflows/
cat > .github/workflows/generate-sap.yml <<EOF
name: Generate SAP

on:
  workflow_dispatch:
    inputs:
      sap_id:
        description: 'SAP ID (e.g., SAP-035)'
        required: true
      domain:
        description: 'Domain (frontend/backend/devops)'
        required: false
        default: 'general'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install jinja2
      - name: Generate SAP
        run: python scripts/generate-sap.py \${{ github.event.inputs.sap_id }} --domain \${{ github.event.inputs.domain }}
      - name: Validate SAP
        run: python scripts/sap-evaluator.py --quick \${{ github.event.inputs.sap_id }}
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "feat: Generate \${{ github.event.inputs.sap_id }}"
          body: "Auto-generated SAP artifacts for \${{ github.event.inputs.sap_id }}"
          branch: "sap/\${{ github.event.inputs.sap_id }}"
EOF
```

**Expected Output**:
```
✅ GitHub Actions workflow created at .github/workflows/generate-sap.yml
✅ Workflow available in Actions tab (manually trigger with SAP ID input)
```

#### Step 3.2: Implement Quality Gates and Validation

**Action**:
```bash
# Create quality gate script
cat > scripts/quality-gate-sap.py <<EOF
#!/usr/bin/env python3
import sys
import subprocess
import json

sap_id = sys.argv[1]
max_todos = int(sys.argv[2]) if len(sys.argv) > 2 else 10

# Count TODOs
result = subprocess.run(
    ['grep', '-r', 'TODO', f'docs/skilled-awareness/{sap_id}/'],
    capture_output=True, text=True
)
todo_count = len(result.stdout.strip().split('\n')) if result.stdout else 0

# Run sap-evaluator
eval_result = subprocess.run(
    ['python', 'scripts/sap-evaluator.py', '--quick', sap_id, '--json'],
    capture_output=True, text=True
)

print(f"📊 Quality Gate Results for {sap_id}:")
print(f"  TODOs: {todo_count}/{max_todos} (threshold)")
print(f"  Validation: {'✅ PASS' if eval_result.returncode == 0 else '❌ FAIL'}")

if todo_count > max_todos:
    print(f"❌ Quality gate failed: {todo_count} TODOs exceeds threshold of {max_todos}")
    sys.exit(1)
if eval_result.returncode != 0:
    print(f"❌ Quality gate failed: sap-evaluator validation failed")
    sys.exit(1)

print("✅ Quality gate passed!")
EOF

chmod +x scripts/quality-gate-sap.py

# Test quality gate
python scripts/quality-gate-sap.py SAP-029 10
```

**Expected Output**:
```
📊 Quality Gate Results for SAP-029:
  TODOs: 8/10 (threshold)
  Validation: ✅ PASS
✅ Quality gate passed!
```

#### Step 3.3: Automate SAP Versioning and Changelog Generation

**Action**:
```bash
# Create versioning automation script
cat > scripts/bump-sap-version.py <<EOF
#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

sap_id = sys.argv[1]
bump_type = sys.argv[2]  # major, minor, patch

# Read catalog
with open('sap-catalog.json') as f:
    catalog = json.load(f)

# Find SAP and bump version
for sap in catalog['saps']:
    if sap['id'] == sap_id:
        version = sap['version']
        major, minor, patch = map(int, version.split('.'))

        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        else:
            patch += 1

        new_version = f"{major}.{minor}.{patch}"
        sap['version'] = new_version
        print(f"✅ Bumped {sap_id} version: {version} → {new_version}")
        break

# Write updated catalog
with open('sap-catalog.json', 'w') as f:
    json.dump(catalog, f, indent=2)

# Update version in all artifacts
sap_dir = Path(f"docs/skilled-awareness/{sap_id.lower().replace('sap-', '')}/")
for artifact in sap_dir.glob('*.md'):
    content = artifact.read_text()
    content = re.sub(
        r'(\*\*Version\*\*:)\s*\d+\.\d+\.\d+',
        f'\\1 {new_version}',
        content
    )
    artifact.write_text(content)

print(f"✅ Updated version in all {sap_id} artifacts")
EOF

chmod +x scripts/bump-sap-version.py

# Test version bump
python scripts/bump-sap-version.py SAP-029 patch
```

### Production Configuration

#### Level 3 Configuration File

```yaml
# Production configuration for Level 3 (.chora/config.yaml)
sap-generation:
  enabled: true
  level: 3
  production: true

  # All Level 2 settings plus:
  ci_cd:
    enabled: true
    platform: github_actions  # or gitlab_ci, jenkins, etc.
    auto_pr_creation: true
    pr_title_template: "feat: Generate {sap_id}"
    branch_name_template: "sap/{sap_id}"

  quality_gates:
    enabled: true
    todo_threshold: 10  # Max TODOs allowed
    require_validation: true
    require_link_validation: true  # Requires SAP-016
    fail_on_error: true  # Strict mode for production

  versioning:
    auto_bump: true
    bump_strategy: semantic  # major, minor, patch
    generate_changelog: true
    create_git_tags: true

  monitoring:
    enabled: true
    metrics:
      - generation_time
      - todo_count
      - validation_success_rate
      - artifact_completeness
    log_level: info
    alert_on_failure: true

  advanced:
    dependency_resolution: true  # Auto-generate dependent SAPs
    template_caching: true  # Cache compiled templates
    parallel_generation: true  # Generate multiple SAPs in parallel
    incremental_updates: true  # Only regenerate changed artifacts
```

### Best Practices (Level 3)

**Best Practice 1**: Use Quality Gates Before Merging
- **Why**: Prevents incomplete SAPs from entering main branch. Ensures <10 TODOs remaining and validation passes.
- **How**: Add quality gate script to CI/CD: `python scripts/quality-gate-sap.py {SAP_ID} 10` as a required check before PR merge.

**Best Practice 2**: Version SAPs Semantically
- **Why**: Clear communication of breaking changes (major), new features (minor), and bug fixes (patch)
- **How**: Use `scripts/bump-sap-version.py {SAP_ID} {major|minor|patch}` and document version changes in ledger.md

**Best Practice 3**: Cache Compiled Templates
- **Why**: Reduces generation time by 50-70% for large SAP ecosystems (20+ SAPs)
- **How**: Enable `template_caching: true` in config. Templates are compiled once and reused. Clear cache when templates change.

**Best Practice 4**: Generate SAPs in Parallel for Batch Operations
- **Why**: Reduces total generation time from 5min × N SAPs to ~5-10min total for batch of N SAPs
- **How**: Enable `parallel_generation: true`. Use Python's `multiprocessing` or `concurrent.futures` to generate multiple SAPs simultaneously.

**Best Practice 5**: Monitor Generation Metrics
- **Why**: Track system health, identify bottlenecks, detect quality regressions (TODO count creep)
- **How**: Enable monitoring in config. Export metrics to dashboard (Grafana, CloudWatch, etc.). Alert on generation failures or TODO threshold violations.

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] All Level 1 and Level 2 checks pass
- [ ] CI/CD workflow exists and can be triggered (.github/workflows/generate-sap.yml or equivalent)
- [ ] Quality gates script exists and enforces <10 TODO threshold (scripts/quality-gate-sap.py)
- [ ] Versioning automation script works (scripts/bump-sap-version.py)
- [ ] Level 3 production configuration file exists (.chora/config.yaml with level: 3)
- [ ] Generated at least 10+ SAPs with Level 3 features (quality gates, versioning, CI/CD)
- [ ] Template caching enabled and working (50-70% performance improvement)
- [ ] Parallel generation enabled and working (batch of 5 SAPs completes in <10min)
- [ ] Production-ready
- [ ] Monitoring configured (metrics dashboard tracking generation time, TODO count, success rate)
- [ ] Documentation updated (all TODOs filled, links validated)

#### Validation Commands

```bash
# Production validation
python scripts/sap-evaluator.py --level 3 SAP-029
python scripts/sap-evaluator.py --production SAP-029

# Performance check
time python scripts/generate-sap.py SAP-035  # Should complete in <5min
python scripts/generate-sap.py --batch batch-generate.yaml --benchmark  # Check parallel performance

# Quality gate check
python scripts/quality-gate-sap.py SAP-035 10  # Should pass with <10 TODOs

# CI/CD integration check
gh workflow run generate-sap.yml -f sap_id=SAP-036 -f domain=frontend  # Trigger GitHub Actions workflow
```

### Common Issues (Level 3)

**Issue 1**: CI/CD workflow fails due to missing dependencies
- **Cause**: GitHub Actions runner doesn't have Jinja2 installed, or Python version mismatch
- **Solution**: Add `pip install jinja2` step to workflow. Use `actions/setup-python@v4` with specific Python version (3.9+).

**Issue 2**: Quality gate fails with "TODO count exceeds threshold"
- **Cause**: Generated SAP has >10 TODOs remaining, violating production quality standard
- **Solution**: Complete more TODOs manually before triggering quality gate. Or adjust threshold in config if appropriate for domain (technical SAPs naturally have more TODOs).

**Issue 3**: Parallel generation causes race conditions or file conflicts
- **Cause**: Multiple SAP generations writing to same catalog file or directory simultaneously
- **Solution**: Implement file locking in generator script. Use atomic write operations. Serialize catalog updates.

---

## Troubleshooting Guide

### General Troubleshooting

**Problem**: Generated SAP has invalid Jinja2 syntax or template rendering errors
- **Symptoms**: `jinja2.exceptions.TemplateSyntaxError` or `UndefinedError` during generation
- **Diagnosis**:
  ```bash
  # Test template rendering with verbose output
  python scripts/generate-sap.py SAP-030 --dry-run --verbose

  # Check template syntax
  python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('templates/sap/')); env.get_template('capability-charter.md.j2').render()"
  ```
- **Solution**: Fix Jinja2 syntax errors in templates. Common issues: missing `{% endfor %}`, unescaped `{{`, undefined variables. Use Jinja2 linting tools.

### Debugging Commands

```bash
# Check SAP-029 status
python scripts/sap-evaluator.py --quick SAP-029 --verbose

# View generation logs (if logging enabled)
tail -f .chora/logs/sap-generation.log

# Test configuration
python -c "import yaml; print(yaml.safe_load(open('.chora/config.yaml'))['sap-generation'])"

# Dry-run generation to see what would be created
python scripts/generate-sap.py SAP-030 --dry-run

# Count TODOs in a SAP
grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l
```

### Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `SAP not found in catalog` | SAP ID doesn't exist in sap-catalog.json | Add SAP entry to catalog first, or check spelling |
| `Template not found: {template}.j2` | Template file missing or incorrect path | Verify templates/sap/ contains required .j2 files |
| `Permission denied: docs/skilled-awareness/` | Write permissions issue | Run with appropriate permissions, check directory ownership |
| `Jinja2 TemplateSyntaxError` | Invalid Jinja2 syntax in template | Fix template syntax, use Jinja2 linter |
| `Unicode encoding error` | Windows console encoding issue | Set `PYTHONIOENCODING=utf-8` or use UTF-8 console |

---

## Migration Paths

### From Other Solutions

#### Migrating from Manual SAP Creation

**Overview**: Transitioning from manually writing SAP artifacts to automated generation

**Steps**:
1. **Audit existing SAPs**: Identify common patterns in manually-created SAPs (structure, sections, phrasing)
2. **Create templates**: Convert common patterns to Jinja2 templates in `templates/sap/`
3. **Populate catalog**: Add all existing SAPs to `sap-catalog.json` with metadata
4. **Test generation**: Generate one SAP and compare to manually-created version
5. **Iterate templates**: Refine templates based on comparison (aim for 80% similarity)

**Validation**:
```bash
# Compare manually-created vs generated SAP
diff docs/skilled-awareness/manual-sap/ docs/skilled-awareness/generated-sap/
python scripts/sap-evaluator.py --quick {SAP_ID}
```

#### Migrating from Cookiecutter or Yeoman

**Overview**: Replacing existing code generation tools with SAP-029

**Steps**:
1. **Export templates**: Convert Cookiecutter/Yeoman templates to Jinja2 format
2. **Map variables**: Map Cookiecutter variables to SAP catalog schema
3. **Test generation**: Run parallel tests with both tools, compare outputs
4. **Deprecate old tool**: Once SAP-029 matches functionality, remove Cookiecutter/Yeoman config

**Validation**:
```bash
# Run both tools and compare
cookiecutter /path/to/template --no-input
python scripts/generate-sap.py SAP-030
diff cookiecutter-output/ docs/skilled-awareness/sap-030/
```

### Between Levels

#### From Level 1 to Level 2

**Steps**:
1. Complete Level 1 validation
2. Generate 2-3 more SAPs with Level 1 to identify template customization needs
3. Create domain-specific templates (frontend, backend, devops)
4. Implement batch generation script
5. Add extended schema fields to catalog
6. Validate Level 2

**Time**: 2-4 hours

#### From Level 2 to Level 3

**Steps**:
1. Complete Level 2 validation
2. Set up CI/CD workflow (GitHub Actions or equivalent)
3. Create quality gate script and integrate into CI/CD
4. Implement versioning automation
5. Enable template caching and parallel generation
6. Configure monitoring and alerting
7. Validate Level 3

**Time**: 10-15 hours

---

## Additional Resources

### Documentation

- **SAP-029 Protocol Spec**: [protocol-spec.md](./protocol-spec.md) - Technical contracts
- **SAP-029 Awareness Guide**: [awareness-guide.md](./awareness-guide.md) - AI agent instructions
- **SAP-029 Capability Charter**: [capability-charter.md](./capability-charter.md) - Problem and scope

### External Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/) - Official Jinja2 templating engine docs
- [Cookiecutter](https://cookiecutter.readthedocs.io/) - Alternative code generation tool for comparison
- [Yeoman](https://yeoman.io/) - Another code scaffolding tool
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - For CI/CD integration
- [Semantic Versioning](https://semver.org/) - Versioning best practices
- [Python Template Engines Comparison](https://www.fullstackpython.com/template-engines.html) - Context on Jinja2 vs alternatives

### Community Support

- GitHub Discussions: [Link to discussions]
- Issue Tracker: [Link to issues]
- Coordination: See [SAP-001 Inbox](../inbox/) for cross-repo support

---

## Adoption Metrics

### Success Criteria by Level

**Level 1 Success**:
- [ ] Basic functionality verified (generated first SAP with 7 artifacts)
- [ ] Time estimate: ≤ 12 hours actual (target: 10-11h)
- [ ] No blocking issues (able to generate SAPs and fill TODOs)
- [ ] TODO count: 60-105 per SAP (acceptable at this level)

**Level 2 Success**:
- [ ] Advanced features working (batch generation, domain templates, extended schema)
- [ ] Time estimate: ≤ 18 hours total (target: 12-15h from Level 1)
- [ ] Production-capable (can generate multiple SAPs efficiently)
- [ ] TODO count: 40-80 per SAP (improved from Level 1)

**Level 3 Success**:
- [ ] Full mastery achieved (CI/CD integration, quality gates, versioning, monitoring)
- [ ] Time estimate: ≤ 35 hours total (target: 25-31h from Level 1)
- [ ] Production-optimized (template caching, parallel generation, <10 TODO enforcement)
- [ ] Measurable improvements: 70-85% time savings vs manual at 50+ SAPs, <5min generation time
- [ ] TODO count: <10 per SAP (enforced by quality gates)

### Time Savings

**Before SAP-029** (Manual SAP Creation):
- First SAP: 10-12 hours (writing 7 artifacts from scratch, no templates)
- Subsequent SAPs: 8-10 hours each (copy-paste from previous SAPs, manual customization)
- Total for 10 SAPs: ~90-110 hours

**After SAP-029 (Level 1)**:
- Setup: 10-11 hours (one-time, includes first SAP)
- Subsequent SAPs: 2-4 hours each (generation + manual TODO fill)
- Total for 10 SAPs: 10h + (9 × 3h) = ~37 hours
- **Savings: 53-73 hours (60-66% time reduction)**

**After SAP-029 (Level 3)**:
- Setup: 25-31 hours (one-time, includes CI/CD, quality gates, versioning automation)
- Subsequent SAPs: 1-2 hours each (automated generation, quality gates, minimal manual work)
- Total for 10 SAPs: 30h + (9 × 1.5h) = ~44 hours
- **Savings: 46-66 hours for first 10 SAPs (50-60% time reduction)**
- **Break-even at ~20 SAPs**: After 20 SAPs, Level 3 time savings surpass Level 1
- **At 50 SAPs**: Level 3 saves ~150 hours vs manual, ~75 hours vs Level 1 (70-85% time reduction)

---

## Adoption Comparison

| Aspect | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| **Setup Time** | 10-11 hours | 12-15 hours | 25-31 hours |
| **Maintenance** | Per-SAP (2-4h each) | Monthly (1-2h) | Monthly (1-2h) |
| **Per-SAP Time** | 2-4 hours | 25 minutes | 1-2 hours |
| **Features** | Basic generation | Batch, domains, extended schema | CI/CD, quality gates, versioning, monitoring |
| **Production Ready** | No | Partial | **Yes** |
| **TODO Count** | 60-105 TODOs | 40-80 TODOs | <10 TODOs (enforced) |
| **Automation Level** | 50-60% | 70-80% | 90-95% |
| **Recommended For** | First 1-5 SAPs | 5-20 SAPs | **20+ SAPs, production ecosystems** |

**Target**: Achieve Level 3 for all production deployments.

---

**Version History**:
- **1.0.0** (2025-11-02): Initial adoption blueprint for SAP Generation Automation