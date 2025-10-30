# How to Create Custom SAP Sets

**Goal**: Define organization-specific or project-specific SAP sets for standardized onboarding.

**Prerequisites**:
- Understanding of SAP framework (read SAP-000)
- Familiarity with YAML syntax
- Knowledge of which SAPs your organization needs

**Time**: 15-30 minutes

---

## Overview

While chora-base provides 5 standard SAP sets (minimal-entry, recommended, testing-focused, mcp-server, full), you may want to create custom sets for:

- **Organization standards** - Define "YourOrg Minimal" with your required SAPs
- **Project types** - Different sets for web apps vs. libraries vs. CLI tools
- **Team preferences** - QA team set, frontend team set, backend team set
- **Progressive onboarding** - Level 1, Level 2, Level 3 sets

Custom sets are defined in your repository's `.chorabase` file.

---

## Quick Start

### Step 1: Create `.chorabase` File

In your repository root:

```bash
touch .chorabase
```

### Step 2: Define Your Custom Set

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  my-org-minimal:
    name: "MyOrg Minimal Entry"
    description: "Our organization's standard minimal set"
    saps:
      - SAP-000  # Framework (required)
      - SAP-001  # Inbox coordination
      - SAP-004  # Testing (required by our org)
      - SAP-009  # Agent awareness
      - SAP-016  # Link validation
    estimated_tokens: 34000
    estimated_hours: "4-6"
    use_cases:
      - "New repos in our organization"
      - "Ecosystem participation with testing focus"
```

### Step 3: Install Your Custom Set

```bash
python scripts/install-sap.py --set my-org-minimal --source /path/to/chora-base
```

**Done!** Your custom set works just like standard sets.

---

## Custom Set Schema

### Required Fields

```yaml
sap_sets:
  your-set-id:                          # Unique identifier (kebab-case)
    name: "Human-Readable Name"         # Display name
    description: "What this set is for" # Brief description
    saps:                               # List of SAP IDs
      - SAP-000
      - SAP-001
      # ...
```

### Optional Fields

```yaml
sap_sets:
  your-set-id:
    name: "..."
    description: "..."
    saps: [...]

    # Optional fields:
    estimated_tokens: 35000              # Approximate token count
    estimated_hours: "5-8"               # Time to adopt
    use_cases:                           # List of use cases
      - "Use case 1"
      - "Use case 2"
    warnings:                            # Important notes
      - "SAP-XXX is in Pilot status"
    prerequisites:                       # Prerequisites for this set
      - "Python 3.12+"
      - "Git installed"
```

---

## Example Custom Sets

### Example 1: Organization Standard

**Scenario**: Your organization requires testing and documentation for all repos.

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  acme-corp-standard:
    name: "ACME Corp Standard"
    description: "Standard SAP set for all ACME repos"
    saps:
      - SAP-000  # Framework
      - SAP-001  # Inbox coordination
      - SAP-003  # GitHub Actions CI/CD
      - SAP-004  # Testing framework (required by ACME)
      - SAP-007  # Documentation structure (required by ACME)
      - SAP-009  # Agent awareness
      - SAP-010  # Changelog management
      - SAP-011  # Type safety (mypy)
      - SAP-012  # Code quality (ruff)
      - SAP-016  # Link validation
    estimated_tokens: 62000
    estimated_hours: "1.5-2 weeks"
    use_cases:
      - "New ACME repositories"
      - "Standardized onboarding for contractors"
    prerequisites:
      - "Python 3.12+"
      - "pytest installed"
      - "GitHub repository"
```

### Example 2: Progressive Onboarding Levels

**Scenario**: You want to onboard developers progressively.

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  level-1-foundation:
    name: "Level 1: Foundation"
    description: "Basic structure and coordination"
    saps:
      - SAP-000  # Framework
      - SAP-001  # Inbox
      - SAP-009  # Agent awareness
    estimated_tokens: 18000
    estimated_hours: "2-3"
    use_cases:
      - "Day 1 onboarding"
      - "Minimum viable setup"

  level-2-quality:
    name: "Level 2: Quality Assurance"
    description: "Add testing and code quality"
    saps:
      - SAP-000  # Framework (already installed if Level 1 done)
      - SAP-001  # Inbox (already installed)
      - SAP-003  # CI/CD
      - SAP-004  # Testing
      - SAP-009  # Agent awareness (already installed)
      - SAP-011  # Type safety
      - SAP-012  # Code quality
      - SAP-016  # Link validation
    estimated_tokens: 45000
    estimated_hours: "5-8"
    use_cases:
      - "After Level 1, when ready for testing"
    prerequisites:
      - "level-1-foundation installed"

  level-3-production:
    name: "Level 3: Production Ready"
    description: "Complete production workflow"
    saps:
      - SAP-000
      - SAP-001
      - SAP-003
      - SAP-004
      - SAP-005  # Dependency management
      - SAP-006  # Docker containerization
      - SAP-007  # Documentation
      - SAP-008  # Release automation
      - SAP-009
      - SAP-010  # Changelog
      - SAP-011
      - SAP-012
      - SAP-013  # Git workflow
      - SAP-016
    estimated_tokens: 78000
    estimated_hours: "2-3 weeks"
    use_cases:
      - "Production deployments"
      - "Complete project maturity"
    prerequisites:
      - "level-2-quality installed"
```

**Progressive installation**:
```bash
# Week 1: Foundation
python scripts/install-sap.py --set level-1-foundation --source /path/to/chora-base

# Week 2: Quality
python scripts/install-sap.py --set level-2-quality --source /path/to/chora-base
# (Already-installed SAPs skipped automatically)

# Month 2: Production
python scripts/install-sap.py --set level-3-production --source /path/to/chora-base
```

### Example 3: Project Type Sets

**Scenario**: Different project types need different SAPs.

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  web-app-stack:
    name: "Web Application Stack"
    description: "Full-stack web app development"
    saps:
      - SAP-000  # Framework
      - SAP-003  # CI/CD
      - SAP-004  # Testing
      - SAP-005  # Dependencies
      - SAP-006  # Docker
      - SAP-007  # Documentation
      - SAP-009  # Agent awareness
      - SAP-016  # Link validation
    estimated_tokens: 52000
    estimated_hours: "1 week"
    use_cases:
      - "Django applications"
      - "FastAPI services"

  library-stack:
    name: "Python Library Stack"
    description: "Reusable library development"
    saps:
      - SAP-000  # Framework
      - SAP-003  # CI/CD
      - SAP-004  # Testing
      - SAP-005  # Dependencies
      - SAP-007  # Documentation (critical for libraries)
      - SAP-008  # Release automation
      - SAP-009  # Agent awareness
      - SAP-010  # Changelog (critical for libraries)
      - SAP-011  # Type safety
      - SAP-012  # Code quality
      - SAP-016  # Link validation
    estimated_tokens: 68000
    estimated_hours: "1.5 weeks"
    use_cases:
      - "PyPI packages"
      - "Shared utilities"
    warnings:
      - "Requires public documentation"

  mcp-server-stack:
    name: "MCP Server Development"
    description: "Model Context Protocol servers"
    saps:
      - SAP-000
      - SAP-003
      - SAP-004
      - SAP-005
      - SAP-006  # Docker for MCP deployment
      - SAP-007
      - SAP-009
      - SAP-011
      - SAP-012
      - SAP-014  # MCP-specific patterns
      - SAP-016
    estimated_tokens: 64000
    estimated_hours: "1-2 weeks"
    use_cases:
      - "Claude Code MCP servers"
      - "LLM tool servers"
```

### Example 4: Team-Specific Sets

**Scenario**: Different teams focus on different aspects.

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  qa-team-focus:
    name: "QA Team Focus"
    description: "Testing and quality assurance"
    saps:
      - SAP-000  # Framework
      - SAP-003  # CI/CD
      - SAP-004  # Testing (core)
      - SAP-011  # Type safety
      - SAP-012  # Code quality
      - SAP-016  # Link validation
    estimated_tokens: 35000
    estimated_hours: "5-8"
    use_cases:
      - "QA contributors"
      - "Test-driven development"

  frontend-team-focus:
    name: "Frontend Team Focus"
    description: "Frontend development patterns"
    saps:
      - SAP-000  # Framework
      - SAP-007  # Documentation
      - SAP-009  # Agent awareness
      - SAP-016  # Link validation
    estimated_tokens: 28000
    estimated_hours: "4-6"
    use_cases:
      - "React developers"
      - "UI/UX contributors"
    warnings:
      - "Limited Python-specific tooling"

  devops-team-focus:
    name: "DevOps Team Focus"
    description: "Deployment and infrastructure"
    saps:
      - SAP-000  # Framework
      - SAP-003  # CI/CD (core)
      - SAP-006  # Docker (core)
      - SAP-008  # Release automation
      - SAP-013  # Git workflow
    estimated_tokens: 38000
    estimated_hours: "6-10"
    use_cases:
      - "Infrastructure engineers"
      - "Release managers"
```

---

## Best Practices

### 1. Always Include SAP-000

SAP-000 (sap-framework) is the foundation for all other SAPs. Always include it:

```yaml
saps:
  - SAP-000  # Required foundation
  - SAP-004
  - SAP-007
  # ...
```

### 2. Check Dependencies

Ensure your set includes dependencies for each SAP:

```yaml
# BAD - Missing SAP-000 dependency
saps:
  - SAP-004  # Depends on SAP-000 and SAP-003
  - SAP-003  # Depends on SAP-000

# GOOD - Includes all dependencies
saps:
  - SAP-000  # Foundation
  - SAP-003  # CI/CD (depends on SAP-000)
  - SAP-004  # Testing (depends on SAP-000, SAP-003)
```

**The install script handles dependencies automatically**, but it's clearer to list them explicitly.

### 3. Use Descriptive IDs

```yaml
# BAD - Unclear ID
sap_sets:
  set-1:
    name: "Our Set"

# GOOD - Clear, descriptive ID
sap_sets:
  acme-corp-minimal-2025:
    name: "ACME Corp Minimal Entry (2025)"
```

### 4. Document Use Cases

Help users understand when to use this set:

```yaml
use_cases:
  - "New repos in our organization"
  - "Ecosystem participation"
  - "Contractors onboarding"
```

### 5. Estimate Token Count

Use the catalog to estimate tokens:

```bash
# List SAP sizes from catalog
cat sap-catalog.json | jq '.saps[] | {id: .id, size_kb: .size_kb}'

# Sum for your set:
# SAP-000: 5.2k tokens
# SAP-004: 8.9k tokens
# SAP-007: 12.3k tokens
# Total: ~26.4k tokens
```

### 6. Version Your Sets

```yaml
# Use versioned IDs for evolving standards
sap_sets:
  acme-minimal-v1:
    name: "ACME Minimal v1.0"
    # ...

  acme-minimal-v2:
    name: "ACME Minimal v2.0 (adds testing)"
    # ...
```

### 7. Add Warnings for Pilot SAPs

If your set includes Pilot-status SAPs:

```yaml
warnings:
  - "SAP-001 (inbox-coordination) is in Pilot status"
  - "May undergo breaking changes"
```

---

## Sharing Custom Sets

### Option 1: Commit to Your Repository

```bash
git add .chorabase
git commit -m "feat: Add custom SAP sets for our organization"
git push
```

Team members clone the repo and immediately have access to custom sets.

### Option 2: Share `.chorabase` File

```bash
# Share the file directly
cat .chorabase | pbcopy  # macOS
# or
cat .chorabase | xclip   # Linux
```

Recipients paste into their `.chorabase` file.

### Option 3: Contribute to chora-base

If your custom set is broadly useful, propose adding it to chora-base's standard sets:

1. Create coordination request in `inbox/outgoing/`
2. Describe the use case and SAP composition
3. chora-base maintainers review and potentially add to catalog

---

## Testing Custom Sets

### Dry Run Test

```bash
# Test without installing
python scripts/install-sap.py --set your-custom-set --dry-run --source /path/to/chora-base
```

### Validation Checklist

- [ ] Set ID is unique (doesn't conflict with standard sets)
- [ ] All SAP IDs exist in catalog
- [ ] SAP-000 is included (foundation requirement)
- [ ] Dependencies are satisfied (automatically handled by script)
- [ ] Token estimate is reasonable (~5k per SAP average)
- [ ] Time estimate reflects adoption complexity
- [ ] Use cases clearly describe when to use this set
- [ ] Warnings document any Pilot-status SAPs

### Test Installation

Test in a temporary repository:

```bash
# Create test repo
mkdir /tmp/test-custom-set
cd /tmp/test-custom-set
git init

# Copy your .chorabase
cp /path/to/your/.chorabase .

# Test installation
python /path/to/chora-base/scripts/install-sap.py \
  --set your-custom-set \
  --source /path/to/chora-base

# Verify all SAPs installed
ls docs/skilled-awareness/

# Clean up
cd ..
rm -rf /tmp/test-custom-set
```

---

## Troubleshooting

### Issue: Custom set not found

**Symptom**:
```
Error: SAP set 'my-custom-set' not found
```

**Solution**: Ensure `.chorabase` is in the **current directory** (where you're running the command):

```bash
# Check if .chorabase exists
ls -la .chorabase

# If not, create it
cat > .chorabase <<'YAML'
version: "4.1.0"
project_type: "custom"
sap_sets:
  my-custom-set:
    # ...
YAML
```

### Issue: YAML syntax error

**Symptom**:
```
Error: Invalid YAML in .chorabase
```

**Solution**: Validate YAML syntax:

```bash
# Validate YAML (requires yq or python)
python -c "import yaml; yaml.safe_load(open('.chorabase'))"

# Or use online validator: https://www.yamllint.com/
```

Common issues:
- Missing quotes around strings with special characters
- Incorrect indentation (use 2 spaces)
- Missing colons after keys

### Issue: SAP not in catalog

**Symptom**:
```
Error: SAP-XXX not found in catalog
```

**Solution**: Check SAP ID spelling:

```bash
# List all available SAP IDs
cat /path/to/chora-base/sap-catalog.json | jq -r '.saps[].id'

# Correct spelling:
# SAP-000 (not SAP-0 or SAP-00)
# SAP-004 (not SAP-4)
```

---

## Advanced: Dynamic Sets

For advanced users, you can generate `.chorabase` dynamically:

```bash
#!/bin/bash
# generate-chorabase.sh

# Detect project type and generate appropriate .chorabase
if [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="library-stack"
elif [ -f "Dockerfile" ]; then
  PROJECT_TYPE="web-app-stack"
else
  PROJECT_TYPE="minimal-entry"
fi

cat > .chorabase <<YAML
version: "4.1.0"
project_type: "custom"

sap_sets:
  auto-detected:
    name: "Auto-Detected Set ($PROJECT_TYPE)"
    description: "Automatically selected based on project structure"
    saps:
      - SAP-000
      # Add SAPs based on $PROJECT_TYPE
YAML
```

---

## Related Documentation

- [Install SAP Set](install-sap-set.md) - How to install sets
- [Standard SAP Sets Reference](../reference/standard-sap-sets.md) - Available standard sets
- [.chorabase Metadata Spec](../reference/chorabase-metadata-spec.md) - Complete specification
- [SAP Catalog](../../sap-catalog.json) - All available SAPs

---

## Summary

**Quick custom set creation**:

```yaml
# .chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  my-org-minimal:
    name: "MyOrg Minimal"
    description: "Organization standard"
    saps:
      - SAP-000
      - SAP-001
      - SAP-004
      - SAP-009
      - SAP-016
    estimated_tokens: 34000
    estimated_hours: "4-6"
    use_cases:
      - "New organization repos"
```

**Installation**:
```bash
python scripts/install-sap.py --set my-org-minimal --source /path/to/chora-base
```

**Result**: Organization-specific SAP sets that standardize onboarding and capability adoption across your repositories.
