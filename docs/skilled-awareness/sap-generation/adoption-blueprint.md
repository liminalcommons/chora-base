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
| **Level 1: Basic** | [Basic approach] | [X-Y hours] | [Frequency] | [Use cases] |
| **Level 2: Advanced** | [Advanced approach] | [X-Y hours] | [Frequency] | [Use cases] |
| **Level 3: Mastery** | [Complete approach] | [X-Y hours] | [Frequency] | **Recommended for production** |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
<!-- TODO: Define when Level 1 is appropriate -->
- Getting started with SAP Generation Automation
- Understanding core concepts
- Development and testing environments
- Quick proof-of-concept

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

#### Step 1.1: [First Step Name]

<!-- TODO: Provide detailed instructions for first step -->

**Action**:
```bash
# Command or configuration
# TODO: Add command
```

**Expected Output**:
```
# TODO: Show expected output
```

**Verification**:
```bash
# How to verify this step succeeded
# TODO: Add verification command
```

#### Step 1.2: [Second Step Name]

**Action**:
```bash
# TODO: Add command or configuration
```

**Expected Output**:
```
# TODO: Show expected output
```

#### Step 1.3: [Third Step Name]

**Action**:
```bash
# TODO: Add command
```

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
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
<!-- TODO: Define what Level 2 adds -->
- [Advanced feature 1]
- [Advanced feature 2]
- [Advanced feature 3]

### Time Estimate

- **Setup**: 25 minutes per additional SAP (5min generation + 20min validation/review)
- **Total from Start**: 10-11 hours + (N SAPs × 25 minutes) + (2-4 hours manual fill per SAP)

### Prerequisites

**Required**:
- ✅ Level 1 adoption complete
- [Additional prerequisite 1]
- [Additional prerequisite 2]

### Step-by-Step Instructions

#### Step 2.1: [First Advanced Step]

**Action**:
```bash
# TODO: Add command or configuration
```

**Expected Output**:
```
# TODO: Show expected output
```

#### Step 2.2: [Second Advanced Step]

**Action**:
```bash
# TODO: Add command
```

**Expected Output**:
```
# TODO: Show expected output
```

#### Step 2.3: [Third Advanced Step]

**Action**:
```bash
# TODO: Add command
```

### Configuration

#### Level 2 Configuration File

<!-- TODO: Provide Level 2 configuration example -->

```yaml
# Configuration for Level 2
sap-generation:
  enabled: true
  level: 2
  # TODO: Add Level 2 specific settings
```

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] All Level 1 checks still pass
- [ ] [Level 2 check 1]
- [ ] [Level 2 check 2]
- [ ] [Level 2 check 3]
- [ ] Advanced features working

#### Validation Commands

```bash
# Level 2 validation
# TODO: Add validation command
```

### Common Issues (Level 2)

**Issue 1**: [Advanced problem]
- **Cause**: [Why this happens]
- **Solution**: [How to fix]

---

## Level 3: Mastery - **RECOMMENDED**

### Purpose

Level 3 adoption provides:
<!-- TODO: Define what Level 3 adds -->
- [Mastery feature 1]
- [Mastery feature 2]
- [Mastery feature 3]
- Production-ready configuration
- Best practices and optimizations

### Time Estimate

- **Setup**: 15-20 hours (includes extended schema design, batch generation, domain-specific templates)
- **Total from Start**: 25-31 hours (Level 1 + Level 2 + Level 3 enhancements)
- **Maintenance**: Monthly template refinements (1-2 hours/month), schema expansions as needed

### Prerequisites

**Required**:
- ✅ Level 2 adoption complete
- [Production prerequisite 1]
- [Production prerequisite 2]

**Recommended**:
- [Optional enhancement 1]

### Step-by-Step Instructions

#### Step 3.1: [First Mastery Step]

**Action**:
```bash
# TODO: Add production-grade command or configuration
```

**Expected Output**:
```
# TODO: Show expected output
```

#### Step 3.2: [Second Mastery Step]

**Action**:
```bash
# TODO: Add command
```

**Expected Output**:
```
# TODO: Show expected output
```

#### Step 3.3: [Third Mastery Step]

**Action**:
```bash
# TODO: Add command
```

### Production Configuration

#### Level 3 Configuration File

<!-- TODO: Provide production-grade configuration -->

```yaml
# Production configuration for Level 3
sap-generation:
  enabled: true
  level: 3
  production: true
  # TODO: Add production-specific settings
```

### Best Practices (Level 3)

<!-- TODO: Document production best practices -->

**Best Practice 1**: [Name]
- **Why**: [Benefit]
- **How**: [Implementation]

**Best Practice 2**: [Name]
- **Why**: [Benefit]
- **How**: [Implementation]

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] All Level 1 and Level 2 checks pass
- [ ] [Level 3 check 1]
- [ ] [Level 3 check 2]
- [ ] [Level 3 check 3]
- [ ] Production-ready
- [ ] Monitoring configured
- [ ] Documentation updated

#### Validation Commands

```bash
# Production validation
# TODO: Add comprehensive validation command

# Performance check
# TODO: Add performance validation
```

### Common Issues (Level 3)

**Issue 1**: [Production problem]
- **Cause**: [Why this happens]
- **Solution**: [How to fix]

---

## Troubleshooting Guide

### General Troubleshooting

**Problem**: [Common problem across all levels]
- **Symptoms**: [What users see]
- **Diagnosis**:
  ```bash
  # TODO: Add diagnostic command
  ```
- **Solution**: [How to fix]

### Debugging Commands

```bash
# Check SAP-029 status
# TODO: Add status check command

# View logs
# TODO: Add log viewing command

# Test configuration
# TODO: Add configuration test command
```

### Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| [Error 1] | [Cause] | [Solution] |
| [Error 2] | [Cause] | [Solution] |

---

## Migration Paths

### From Other Solutions

<!-- TODO: Document migration from alternatives -->

#### Migrating from [Alternative 1]

**Overview**: How to migrate from [Alternative 1] to SAP-029

**Steps**:
1. [Migration step 1]
2. [Migration step 2]
3. [Migration step 3]

**Validation**:
```bash
# TODO: Add migration validation command
```

### Between Levels

#### From Level 1 to Level 2

**Steps**:
1. Complete Level 1 validation
2. [Upgrade step 1]
3. [Upgrade step 2]
4. Validate Level 2

#### From Level 2 to Level 3

**Steps**:
1. Complete Level 2 validation
2. [Upgrade step 1]
3. [Upgrade step 2]
4. Validate Level 3

---

## Additional Resources

### Documentation

- **SAP-029 Protocol Spec**: [protocol-spec.md](./protocol-spec.md) - Technical contracts
- **SAP-029 Awareness Guide**: [awareness-guide.md](./awareness-guide.md) - AI agent instructions
- **SAP-029 Capability Charter**: [capability-charter.md](./capability-charter.md) - Problem and scope

### External Resources

<!-- TODO: Link to helpful external resources -->

- [External Guide 1](https://example.com) - [Description]
- [External Guide 2](https://example.com) - [Description]

### Community Support

- GitHub Discussions: [Link to discussions]
- Issue Tracker: [Link to issues]
- Coordination: See [SAP-001 Inbox](../inbox/) for cross-repo support

---

## Adoption Metrics

### Success Criteria by Level

**Level 1 Success**:
- [ ] Basic functionality verified
- [ ] Time estimate: ≤ [X] hours actual
- [ ] No blocking issues

**Level 2 Success**:
- [ ] Advanced features working
- [ ] Time estimate: ≤ [Y] hours total
- [ ] Production-capable

**Level 3 Success**:
- [ ] Full mastery achieved
- [ ] Time estimate: ≤ [Z] hours total
- [ ] Production-optimized
- [ ] Measurable improvements achieved

### Time Savings

<!-- TODO: Document expected time savings -->

**Before SAP-029**: [Baseline time/effort]
**After SAP-029 (Level 3)**: [New time/effort]
**Savings**: [Percentage or absolute savings]

---

## Adoption Comparison

| Aspect | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| **Setup Time** | [X-Y hours] | [X-Y hours] | [X-Y hours] |
| **Maintenance** | [Frequency] | [Frequency] | [Frequency] |
| **Features** | Basic | Advanced | Complete |
| **Production Ready** | No | Partial | **Yes** |
| **Recommended For** | Development | Staging | **Production** |

**Target**: Achieve Level 3 for all production deployments.

---

**Version History**:
- **1.0.0** (2025-11-02): Initial adoption blueprint for SAP Generation Automation