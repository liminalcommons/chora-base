# install-sap.py CLI Reference

**Complete command-line reference for the SAP installation script.**

**Script Location**: `scripts/install-sap.py`
**Python Version**: 3.12+
**Dependencies**: PyYAML (optional, for custom sets)

---

## Synopsis

```bash
python scripts/install-sap.py <sap_id> [options]
python scripts/install-sap.py --set <set_id> [options]
python scripts/install-sap.py --list [options]
python scripts/install-sap.py --list-sets [options]
```

---

## Description

`install-sap.py` automates the installation of Skilled Awareness Packages (SAPs) from chora-base into your repository. It handles:

- **Individual SAP installation** with automatic dependency resolution
- **SAP set installation** for curated bundles
- **Dry-run mode** for previewing changes
- **Validation** of installed SAPs
- **System file copying** (scripts, templates, configs)

---

## Commands

### Install Individual SAP

```bash
python scripts/install-sap.py SAP-004
```

Install a single SAP by ID. Dependencies are automatically installed first.

**Example**:
```bash
# Install testing framework (SAP-004)
# Automatically installs SAP-000 (framework) and SAP-003 (ci-cd) first
python scripts/install-sap.py SAP-004 --source /path/to/chora-base
```

### Install SAP Set

```bash
python scripts/install-sap.py --set minimal-entry
```

Install a curated bundle of SAPs. See [Standard SAP Sets](standard-sap-sets.md) for available sets.

**Example**:
```bash
# Install minimal-entry set (5 SAPs)
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### List Available SAPs

```bash
python scripts/install-sap.py --list
```

Display all available SAPs from the catalog.

**Example Output**:
```
Available SAPs (18 total):

SAP-000: sap-framework
  Description: Core SAP framework and protocols
  Status: active
  Size: 125 KB
  Dependencies: (none)

SAP-001: inbox-coordination
  Description: Cross-repo coordination protocol
  Status: pilot
  Size: 45 KB
  Dependencies: (none)

[... continues for all 18 SAPs]
```

### List Available Sets

```bash
python scripts/install-sap.py --list-sets
```

Display all available SAP sets (standard and custom).

**Example Output**:
```
Available SAP Sets:

1. minimal-entry
   Name: Minimal Ecosystem Entry
   SAPs: 5 (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)
   Estimated tokens: ~29,000
   Estimated time: 3-5 hours
   Use cases:
   - First-time chora ecosystem adoption
   - Cross-repo coordination
   - Lightweight onboarding

2. recommended
   Name: Recommended Foundation
   SAPs: 10
   Estimated tokens: ~60,000
   Estimated time: 1-2 days
   Use cases:
   - Production development workflow
   - Full-featured project setup

[... continues for all sets]
```

---

## Options

### `sap_id` (positional)

**Type**: String
**Required**: Yes (unless `--set` is used)
**Format**: `SAP-XXX` where XXX is 3-digit number (e.g., `SAP-004`, `SAP-016`)

SAP identifier to install.

**Examples**:
```bash
python scripts/install-sap.py SAP-000
python scripts/install-sap.py SAP-004
python scripts/install-sap.py SAP-014
```

---

### `--set <set_id>`

**Type**: String
**Required**: No (mutually exclusive with `sap_id`)
**Values**: `minimal-entry`, `recommended`, `testing-focused`, `mcp-server`, `full`, or custom set ID

Install a SAP set instead of individual SAP.

**Examples**:
```bash
# Standard sets
python scripts/install-sap.py --set minimal-entry
python scripts/install-sap.py --set recommended
python scripts/install-sap.py --set testing-focused
python scripts/install-sap.py --set mcp-server
python scripts/install-sap.py --set full

# Custom set (from .chorabase)
python scripts/install-sap.py --set my-org-minimal
```

---

### `--source <path>`

**Type**: Path
**Default**: Current directory (`.`)
**Required**: No

Path to chora-base repository (source of SAPs).

**Examples**:
```bash
# Absolute path
python scripts/install-sap.py SAP-004 --source /tmp/chora-base

# Relative path
python scripts/install-sap.py SAP-004 --source ../chora-base

# Sibling directory
python scripts/install-sap.py SAP-004 --source ~/projects/chora-base
```

**Notes**:
- Must point to **root** of chora-base directory
- Must contain `sap-catalog.json`
- Must contain `docs/skilled-awareness/` directory

---

### `--target <path>`

**Type**: Path
**Default**: Current directory (`.`)
**Required**: No

Target directory where SAPs will be installed.

**Examples**:
```bash
# Install to specific project
python scripts/install-sap.py SAP-004 \
  --source /tmp/chora-base \
  --target /path/to/my-project

# Install to subdirectory
python scripts/install-sap.py SAP-004 \
  --source ../chora-base \
  --target ./subproject
```

**Notes**:
- Creates `docs/skilled-awareness/` if it doesn't exist
- Copies system files relative to target directory

---

### `--list`

**Type**: Flag
**Default**: `false`
**Required**: No

List all available SAPs from catalog without installing.

**Example**:
```bash
python scripts/install-sap.py --list --source /path/to/chora-base
```

**Output**: Displays SAP ID, name, description, status, size, dependencies for all SAPs.

---

### `--list-sets`

**Type**: Flag
**Default**: `false`
**Required**: No

List all available SAP sets (standard and custom) without installing.

**Example**:
```bash
python scripts/install-sap.py --list-sets --source /path/to/chora-base
```

**Output**: Displays set ID, name, SAP count, token estimate, time estimate, use cases.

---

### `--dry-run`

**Type**: Flag
**Default**: `false`
**Required**: No

Preview installation without making any changes to filesystem.

**Examples**:
```bash
# Dry run for individual SAP
python scripts/install-sap.py SAP-004 --dry-run --source /path/to/chora-base

# Dry run for SAP set
python scripts/install-sap.py --set minimal-entry --dry-run --source /path/to/chora-base
```

**Output**:
```
[DRY RUN] Would install:
  ✓ SAP-000: sap-framework
  ✓ SAP-004: testing-framework

[DRY RUN] Would create directories:
  docs/skilled-awareness/sap-framework/
  docs/skilled-awareness/testing-framework/

[DRY RUN] Would copy system files:
  static-template/tests/
  static-template/.github/workflows/test.yml
```

**Use Cases**:
- Preview what will be installed before committing
- Check if SAPs are already installed
- Verify dependencies will be resolved correctly
- Review which system files will be copied

---

## Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| `0` | Success | All SAPs installed successfully |
| `1` | Error | Validation failure, installation error, missing catalog |
| `2` | Invalid usage | Missing required arguments, invalid SAP ID |

**Examples**:
```bash
# Check exit code
python scripts/install-sap.py SAP-004 --source /path/to/chora-base
echo $?  # Prints: 0 (success)

# Handle errors
python scripts/install-sap.py SAP-999 --source /path/to/chora-base
echo $?  # Prints: 1 (error - invalid SAP ID)

# Invalid usage
python scripts/install-sap.py
echo $?  # Prints: 2 (invalid usage - missing SAP ID or --set)
```

---

## Environment

### Python Version

**Required**: Python 3.12+

**Check version**:
```bash
python --version  # or python3 --version
```

### Dependencies

#### Required
- Python standard library (pathlib, argparse, json, shutil)

#### Optional
- **PyYAML** - Required for custom SAP sets from `.chorabase`

**Install PyYAML**:
```bash
pip install PyYAML
# or
pip3 install PyYAML
```

**Without PyYAML**: Standard sets work, but custom sets from `.chorabase` won't be available.

---

## How It Works

### Installation Process

1. **Load Catalog**
   - Read `sap-catalog.json` from source directory
   - Parse standard sets
   - Load custom sets from `.chorabase` (if present)

2. **Resolve Dependencies**
   - Build dependency tree for requested SAP(s)
   - Topological sort to determine installation order
   - Check for already-installed SAPs

3. **Install SAPs** (in dependency order)
   - Create `docs/skilled-awareness/<sap-name>/` directory
   - Copy 5 SAP artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
   - Copy system files (if any) to appropriate locations

4. **Validate Installation**
   - Check all 5 artifacts exist
   - Verify system files copied correctly
   - Report warnings for Pilot-status SAPs

5. **Report Results**
   - Display installed SAPs
   - Show skipped SAPs (already installed)
   - Report any errors or warnings

### Dependency Resolution

```
SAP-004 (testing-framework)
  ├─ requires: SAP-003 (ci-cd-workflows)
  │   └─ requires: SAP-000 (sap-framework)
  └─ requires: SAP-000 (sap-framework)

Installation order:
1. SAP-000 (foundation)
2. SAP-003 (CI/CD)
3. SAP-004 (testing)
```

**The script automatically handles this** - you don't need to install dependencies manually.

### Idempotency

**Already-installed SAPs are skipped automatically**:

```bash
# First run: Installs SAP-000, SAP-004
python scripts/install-sap.py SAP-004

# Second run: Skips both (already installed)
python scripts/install-sap.py SAP-004
```

**Output**:
```
✓ SAP-000 already installed - skipping
✓ SAP-004 already installed - skipping
```

This makes progressive installation safe:
```bash
# Install minimal-entry (5 SAPs)
python scripts/install-sap.py --set minimal-entry

# Later, upgrade to recommended (10 SAPs total)
python scripts/install-sap.py --set recommended
# Only installs 5 new SAPs - skips the 5 already installed
```

---

## Examples

### Example 1: First-Time Installation

```bash
# Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# Install minimal-entry set
cd /path/to/your-repo
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base
```

### Example 2: Progressive Adoption

```bash
# Week 1: Start small
python scripts/install-sap.py --set minimal-entry --source ../chora-base

# Week 2: Add testing
python scripts/install-sap.py SAP-004 --source ../chora-base

# Week 3: Add documentation
python scripts/install-sap.py SAP-007 --source ../chora-base

# Month 2: Upgrade to full recommended set
python scripts/install-sap.py --set recommended --source ../chora-base
# Only installs SAPs not already present
```

### Example 3: Dry Run Before Installing

```bash
# Preview what will be installed
python scripts/install-sap.py --set recommended --dry-run --source /tmp/chora-base

# Review output, then install
python scripts/install-sap.py --set recommended --source /tmp/chora-base
```

### Example 4: Organization Standard

```bash
# Define custom set in .chorabase
cat > .chorabase <<'YAML'
version: "4.1.0"
sap_sets:
  acme-standard:
    name: "ACME Corp Standard"
    saps: ["SAP-000", "SAP-004", "SAP-007", "SAP-009"]
YAML

# Install custom set
python /path/to/chora-base/scripts/install-sap.py \
  --set acme-standard \
  --source /path/to/chora-base
```

### Example 5: CI/CD Integration

```bash
#!/bin/bash
# .github/workflows/install-saps.sh

set -e

# Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# Install SAPs
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base

# Verify installation
if [ -d "docs/skilled-awareness/sap-framework" ]; then
  echo "✓ SAPs installed successfully"
  exit 0
else
  echo "✗ SAP installation failed"
  exit 1
fi
```

### Example 6: Query Available Options

```bash
# List all SAPs
python scripts/install-sap.py --list --source /path/to/chora-base

# List all sets
python scripts/install-sap.py --list-sets --source /path/to/chora-base

# Get help
python scripts/install-sap.py --help
```

---

## Troubleshooting

### Error: "Catalog not found"

**Full Error**:
```
✗ Catalog not found: /path/to/source/sap-catalog.json
ℹ Expected: sap-catalog.json in chora-base root
```

**Cause**: `--source` doesn't point to chora-base root

**Solution**:
```bash
# Wrong: Points to subdirectory
python scripts/install-sap.py SAP-004 --source /path/to/chora-base/scripts

# Correct: Points to root
python scripts/install-sap.py SAP-004 --source /path/to/chora-base
```

---

### Error: "SAP not found in catalog"

**Full Error**:
```
✗ SAP-999 not found in catalog
```

**Cause**: Invalid SAP ID

**Solution**: Use `--list` to see available SAPs:
```bash
python scripts/install-sap.py --list --source /path/to/chora-base
```

---

### Error: "SAP set not found"

**Full Error**:
```
✗ SAP set 'my-custom-set' not found
```

**Cause**: Set doesn't exist in catalog or `.chorabase`

**Solution**: Use `--list-sets` to see available sets:
```bash
python scripts/install-sap.py --list-sets --source /path/to/chora-base
```

Or create custom set in `.chorabase`.

---

### Warning: "PyYAML not available"

**Full Warning**:
```
⚠ PyYAML not available. Custom sets from .chorabase won't work.
ℹ Install with: pip install PyYAML
```

**Impact**: Standard sets work, but custom sets don't

**Solution**:
```bash
pip install PyYAML
```

---

### Warning: "SAP-XXX is in Pilot status"

**Full Warning**:
```
⚠ SAP-001 (inbox-coordination) is in Pilot status - may undergo changes
```

**Impact**: SAP may change in future chora-base versions

**Recommendation**: Still safe to adopt, but be aware of potential updates

---

## Advanced Usage

### Scripting

```bash
#!/bin/bash
# install-saps-batch.sh - Install multiple SAPs

CHORA_BASE="/path/to/chora-base"
SAPS=("SAP-004" "SAP-007" "SAP-009")

for sap in "${SAPS[@]}"; do
  echo "Installing $sap..."
  python "$CHORA_BASE/scripts/install-sap.py" \
    "$sap" \
    --source "$CHORA_BASE"

  if [ $? -ne 0 ]; then
    echo "Error installing $sap"
    exit 1
  fi
done

echo "All SAPs installed successfully"
```

### Conditional Installation

```bash
#!/bin/bash
# Install testing SAPs only if tests/ directory exists

if [ -d "tests/" ]; then
  echo "Tests directory found - installing testing SAPs"
  python scripts/install-sap.py SAP-004 --source /path/to/chora-base
else
  echo "No tests directory - skipping testing SAPs"
fi
```

### Validation Script

```bash
#!/bin/bash
# validate-sap-installation.sh - Check if SAPs installed correctly

EXPECTED_SAPS=("sap-framework" "testing-framework" "documentation-structure")

for sap in "${EXPECTED_SAPS[@]}"; do
  if [ -d "docs/skilled-awareness/$sap" ]; then
    # Check for all 5 artifacts
    artifacts=(
      "capability-charter.md"
      "protocol-spec.md"
      "awareness-guide.md"
      "adoption-blueprint.md"
      "ledger.md"
    )

    all_present=true
    for artifact in "${artifacts[@]}"; do
      if [ ! -f "docs/skilled-awareness/$sap/$artifact" ]; then
        echo "✗ Missing: $sap/$artifact"
        all_present=false
      fi
    done

    if [ "$all_present" = true ]; then
      echo "✓ $sap (5 artifacts)"
    fi
  else
    echo "✗ SAP not installed: $sap"
  fi
done
```

---

## Related Documentation

- [Install SAP Set How-To](../how-to/install-sap-set.md) - Step-by-step installation guide
- [Create Custom SAP Sets](../how-to/create-custom-sap-sets.md) - Define organization sets
- [Standard SAP Sets](standard-sap-sets.md) - Available standard sets
- [Agent Onboarding Guide](../guides/agent-onboarding-chora-base.md) - Complete onboarding

---

## Quick Reference

### Common Commands

```bash
# Install individual SAP
python scripts/install-sap.py SAP-004 --source /path/to/chora-base

# Install SAP set
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base

# Dry run
python scripts/install-sap.py --set recommended --dry-run --source /path/to/chora-base

# List SAPs
python scripts/install-sap.py --list --source /path/to/chora-base

# List sets
python scripts/install-sap.py --list-sets --source /path/to/chora-base

# Help
python scripts/install-sap.py --help
```

### Common Patterns

```bash
# Progressive adoption
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
python scripts/install-sap.py --set recommended --source /path/to/chora-base
python scripts/install-sap.py --set full --source /path/to/chora-base

# Custom installation
python scripts/install-sap.py SAP-004 --source /path/to/chora-base
python scripts/install-sap.py SAP-007 --source /path/to/chora-base
python scripts/install-sap.py SAP-014 --source /path/to/chora-base
```

---

## Summary

**install-sap.py** provides automated, idempotent installation of SAPs with:
- ✅ Automatic dependency resolution
- ✅ Dry-run mode for safe previewing
- ✅ SAP set installation (5 standard sets)
- ✅ Custom set support via `.chorabase`
- ✅ Validation of installed artifacts
- ✅ Clear error messages and warnings

**Installation**: One-line command to adopt chora-base capabilities.
