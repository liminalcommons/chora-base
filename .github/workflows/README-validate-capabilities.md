# Validate Capability Manifests Workflow

**Version**: 1.0.0
**Status**: Active
**Part of**: Ecosystem Ontology & Composition Vision - Phase 1, Week 3.2

---

## Overview

The `validate-capabilities.yml` GitHub Actions workflow provides automated validation for capability YAML manifests in pull requests and commits. It ensures all capabilities comply with the chora ecosystem ontology specification before merging.

**Implemented in**: ONT-010 (Week 3.2)

---

## Features

### 1. **Namespace Validation**
- Validates namespace format (`chora.{domain}.{capability}`)
- Checks domain exists in domain-taxonomy.md
- Detects duplicate namespaces
- Validates SemVer compliance

### 2. **JSON Schema Validation**
- Validates Service-type capabilities against `capability-service.schema.json`
- Validates Pattern-type capabilities against `capability-pattern.schema.json`
- Ensures all required fields are present
- Validates field types and constraints

### 3. **Namespace Collision Detection**
- Scans all capability manifests
- Reports duplicate namespace usage
- Provides file paths for each collision

### 4. **PR Comment Reporting**
- Posts validation results as PR comments
- Provides expandable details for each validation check
- Updates existing comments to avoid spam
- Shows ✅ or ❌ status for each check

---

## Triggers

The workflow runs automatically when:

**Pull Requests**:
- PR targets `main` or `develop` branch
- PR modifies files in `capabilities/**/*.yaml`
- PR modifies `docs/ontology/domain-taxonomy.md`
- PR modifies `schemas/*.json`
- PR modifies `scripts/validate-namespaces.py`

**Pushes**:
- Push to `main` or `develop` branch
- Commits modify capability YAML files

**Manual**:
- Via GitHub Actions UI (workflow_dispatch)

---

## Jobs

### 1. validate-namespaces

**Purpose**: Runs `scripts/validate-namespaces.py` on all capability manifests

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Install PyYAML
4. Run namespace validation script
5. Upload validation results as artifact

**Output**: `validation-output.txt` (saved for 30 days)

**Exit Codes**:
- `0`: All validations passed
- `1`: Validation errors found

---

### 2. validate-json-schema

**Purpose**: Validates capability manifests against JSON Schema

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Install PyYAML + jsonschema
4. Create inline validation script
5. Validate each YAML file against appropriate schema
6. Upload validation results as artifact

**Output**: `schema-validation-output.txt` (saved for 30 days)

**Validation Logic**:
```python
if dc_type == "Service":
    schema = capability-service.schema.json
elif dc_type == "Pattern":
    schema = capability-pattern.schema.json
```

---

### 3. check-collisions

**Purpose**: Detects duplicate namespace usage across all manifests

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Install PyYAML
4. Create inline collision detection script
5. Collect all namespaces from capabilities/
6. Report any duplicates
7. Upload collision check results as artifact

**Output**: `collision-check-output.txt` (saved for 30 days)

---

### 4. post-pr-comment

**Purpose**: Posts validation results as PR comment

**Steps**:
1. Download validation artifacts from previous jobs
2. Combine results into markdown comment
3. Find existing validation comment (if any)
4. Update existing comment or create new one

**Comment Format**:
```markdown
## 🔍 Capability Validation Results

### Namespace Validation
✅ **Passed** - All namespaces valid

<details><summary>View Details</summary>
...
</details>

### JSON Schema Validation
✅ **Passed** - All manifests comply with JSON Schema

### Namespace Collision Detection
✅ **Passed** - No duplicate namespaces found

---
_Automated validation from Ecosystem Ontology & Composition Vision_
```

**Conditions**:
- Only runs on `pull_request` events
- Always runs (even if validation fails)
- Requires all validation jobs to complete

---

### 5. summary

**Purpose**: Provides overall validation status

**Steps**:
1. Check results from all validation jobs
2. Print summary to workflow log
3. Exit with failure if any validation failed

**Exit Codes**:
- `0`: All validations passed
- `1`: One or more validations failed

---

## Usage

### Automatic Validation (Recommended)

**For Pull Requests**:
1. Create PR with capability manifest changes
2. Workflow runs automatically
3. Review validation results in PR comment
4. Fix any errors reported
5. Push fixes to PR
6. Workflow re-runs automatically

**Example PR Comment**:
```markdown
## 🔍 Capability Validation Results

### Namespace Validation
❌ **Failed** - Namespace validation errors found

<details><summary>View Details</summary>

[NAMESPACE_DUPLICATE] Duplicate namespace 'chora.registry.lookup' found.
Already defined in: capabilities/chora.registry.lookup.yaml

</details>
```

---

### Manual Validation

**Run workflow manually**:
1. Go to GitHub Actions tab
2. Select "Validate Capability Manifests" workflow
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow" button

**Local validation** (recommended before push):
```bash
# Run namespace validation
python scripts/validate-namespaces.py capabilities/

# Run pre-commit hooks (includes namespace validation)
pre-commit run --all-files
```

---

## Validation Failure Examples

### Namespace Format Error

**Trigger**: Invalid namespace format

**PR Comment**:
```markdown
### Namespace Validation
❌ **Failed** - Namespace validation errors found

<details><summary>View Details</summary>

[NAMESPACE_FORMAT_INVALID] Namespace 'chora.React.FormValidation' does not match
required format: chora.{domain}.{capability} (lowercase, snake_case, capability 1-50 chars)

</details>
```

**Fix**: Use lowercase snake_case
```yaml
# Before
metadata:
  dc_identifier: chora.React.FormValidation

# After
metadata:
  dc_identifier: chora.react.form_validation
```

---

### Domain Invalid Error

**Trigger**: Domain not in domain-taxonomy.md

**PR Comment**:
```markdown
### Namespace Validation
❌ **Failed** - Namespace validation errors found

<details><summary>View Details</summary>

[DOMAIN_INVALID] Domain 'backend' in namespace 'chora.backend.api' is not defined
in domain-taxonomy.md.

</details>
```

**Fix**: Use valid domain from [domain-taxonomy.md](../../docs/ontology/domain-taxonomy.md)

---

### JSON Schema Error

**Trigger**: Missing required field or invalid field type

**PR Comment**:
```markdown
### JSON Schema Validation
❌ **Failed** - Schema validation errors found

<details><summary>View Details</summary>

capabilities/chora.example.service.yaml: 'dc_hasVersion' is a required property

</details>
```

**Fix**: Add missing required fields
```yaml
metadata:
  dc_identifier: chora.example.service
  dc_title: "Example Service"
  dc_description: "Example service description"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"  # Add missing version
```

---

### Namespace Collision Error

**Trigger**: Duplicate namespace across multiple files

**PR Comment**:
```markdown
### Namespace Collision Detection
❌ **Failed** - Namespace collisions detected

<details><summary>View Details</summary>

Namespace: chora.registry.lookup
  - capabilities/chora.registry.lookup.yaml
  - capabilities/chora.registry.lookup-v2.yaml

</details>
```

**Fix**: Choose unique namespace or remove duplicate file

---

## Artifacts

All validation results are saved as artifacts for 30 days:

**Available Artifacts**:
1. **validation-results** - Namespace validation output
2. **schema-validation-results** - JSON Schema validation output
3. **collision-check-results** - Collision detection output

**Download Artifacts**:
1. Go to workflow run page
2. Scroll to "Artifacts" section
3. Download desired artifact
4. Extract and view `.txt` file

---

## Integration with Pre-commit

This workflow complements the pre-commit hook:

**Pre-commit (Local)**:
- Runs before commit
- Fast feedback loop
- Prevents invalid commits

**GitHub Actions (CI/CD)**:
- Runs on PR
- Catches issues missed locally
- Validates cross-file dependencies
- Provides PR comment feedback

**Recommended Workflow**:
```bash
# 1. Local validation
pre-commit run validate-namespaces --files capabilities/new-capability.yaml

# 2. Commit if passing
git add capabilities/new-capability.yaml
git commit -m "feat(ontology): add new capability"

# 3. Push and create PR
git push origin feature/new-capability

# 4. GitHub Actions validates automatically
# 5. Review PR comment for results
```

---

## Troubleshooting

### Workflow Not Triggering

**Symptom**: Workflow doesn't run on PR

**Possible Causes**:
1. PR doesn't modify capability YAML files
2. PR targets branch other than `main` or `develop`
3. Workflow file has syntax errors

**Fix**:
```bash
# Validate workflow YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/validate-capabilities.yml', encoding='utf-8'))"

# Check PR target branch
git branch -r | grep origin
```

---

### Validation Passes Locally but Fails in CI

**Symptom**: Pre-commit passes but GitHub Actions fails

**Possible Causes**:
1. Different Python version (local vs CI)
2. Cached pre-commit results
3. Missing files in git commit

**Fix**:
```bash
# Clear pre-commit cache
pre-commit clean

# Run with same Python version as CI (3.11)
python3.11 scripts/validate-namespaces.py capabilities/

# Ensure all files committed
git status
```

---

### PR Comment Not Posted

**Symptom**: Workflow runs but no PR comment appears

**Possible Causes**:
1. GitHub token permissions insufficient
2. PR comment job failed
3. Artifact download failed

**Fix**:
1. Check workflow logs for errors in `post-pr-comment` job
2. Verify `GITHUB_TOKEN` has `pull-requests: write` permission
3. Check artifact upload/download steps succeeded

---

## Performance

**Typical Runtime**:
- **validate-namespaces**: 10-20 seconds
- **validate-json-schema**: 15-30 seconds
- **check-collisions**: 10-20 seconds
- **post-pr-comment**: 5-10 seconds

**Total**: ~40-80 seconds for complete validation

**Optimization**:
- Jobs run in parallel (except `post-pr-comment` and `summary`)
- Python package caching enabled (`cache: 'pip'`)
- Concurrency group prevents duplicate runs for same PR

---

## Future Enhancements (Not in Week 3.2)

**Planned for Later Phases**:
- [ ] Cross-type dependency validation (Week 4.3)
- [ ] PyPI package name collision detection
- [ ] Auto-fix capabilities for common errors
- [ ] Slack/Discord notification integration
- [ ] Validation performance metrics
- [ ] GitHub App for enhanced PR integration

---

## References

### Documentation
- [Namespace Specification](../../docs/ontology/namespace-spec.md)
- [Domain Taxonomy](../../docs/ontology/domain-taxonomy.md)
- [JSON Schemas](../../schemas/)
- [Pre-commit Hook](../../scripts/README-namespace-validation.md)

### Related Tasks
- **ONT-009** (Week 3.1): Implement pre-commit hook
- **ONT-010** (Week 3.2): Create CI/CD workflow (this deliverable)
- **ONT-011** (Week 3.3): Implement migration script
- **ONT-012** (Week 3.4): Create artifact extractor

### Files
- `.github/workflows/validate-capabilities.yml` - Workflow definition
- `scripts/validate-namespaces.py` - Namespace validator
- `schemas/*.schema.json` - JSON Schema validators

---

## Support

**Issues**: Report workflow bugs or feature requests in beads:
```bash
bd create --title "CI/CD validation: <issue>" --label "ontology,cicd"
```

**Questions**: See workflow logs in GitHub Actions tab for detailed error messages.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Author**: Claude (ONT-010)
**Status**: Active ✅
