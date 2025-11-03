# Adoption Blueprint: Publishing Automation

**SAP ID**: SAP-028
**Version**: 1.0.0
**Last Updated**: 2025-11-02

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-028 Publishing Automation across three progressive levels.

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
- Getting started with Publishing Automation
- Understanding core concepts
- Development and testing environments
- Quick proof-of-concept

### Time Estimate

- **Setup**: 5 minutes (new projects) / 15 minutes (token migration)
- **Learning Curve**: Low - Straightforward PyPI publisher configuration, follow PyPI OIDC setup wizard

### Prerequisites

**Required**:
- PyPI account with verified email address
- GitHub repository with Actions enabled
- Publisher permissions on PyPI for target package name
- GitHub repository owner/admin access (for OIDC configuration)
- Familiarity with GitHub Actions workflows

**Recommended**:
- Read PyPI trusted publishing documentation
- Understand PEP 740 attestation concepts
- Review GitHub OIDC integration guide
- Test with TestPyPI first before production PyPI

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
python scripts/sap-evaluator.py --quick SAP-028

# Expected output:
# ✅ SAP-028 (publishing-automation)
#    Level: 1
#    Next: Level 2
# ✅ Validation passed

# Test OIDC publishing setup
gh workflow run release.yml --ref main -f environment=test
```

### Common Issues (Level 1)

**Issue 1**: OIDC trusted publisher configuration fails on PyPI
- **Cause**: PyPI requires exact match of repository owner, repository name, workflow filename, and environment name (if specified)
- **Solution**: Verify PyPI publisher configuration matches exactly: Go to PyPI → Account → Publishing → Add new publisher → Check owner, repo, workflow name (.github/workflows/release.yml), and environment. Case-sensitive.
- **Alternative**: Use TestPyPI first to validate configuration before production PyPI

**Issue 2**: PEP 740 attestation missing from published package
- **Cause**: GitHub Actions workflow doesn't have `id-token: write` permission, or pypa/gh-action-pypi-publish version < v1.8.0
- **Solution**: Update workflow file to include `permissions: id-token: write` at job level, and upgrade to pypa/gh-action-pypi-publish@release/v1 (latest)
- **Note**: Attestations are automatic when OIDC is configured correctly

**Issue 3**: Token-based fallback publishing not working
- **Cause**: GitHub Secret name mismatch (e.g., PYPI_TOKEN vs PYPI_API_TOKEN), or token expired/revoked
- **Solution**: Check secret name in workflow matches GitHub Secrets repository settings exactly. For PyPI, generate new API token with package scope, add to GitHub Secrets as `PYPI_API_TOKEN`

**Issue 4**: Workflow fails with "Resource not accessible by integration" error
- **Cause**: GitHub Actions workflow missing required permissions for OIDC token exchange
- **Solution**: Add `permissions: id-token: write` and `contents: read` to workflow file at top-level or job-level. Verify repository settings allow Actions to create tokens (Settings → Actions → General → Workflow permissions)

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds:
<!-- TODO: Define what Level 2 adds -->
- [Advanced feature 1]
- [Advanced feature 2]
- [Advanced feature 3]

### Time Estimate

- **Setup**: 30 minutes (configure 2+ repositories, test multi-project workflows)
- **Total from Start**: 45 minutes (Level 1 + Level 2 multi-project setup)

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
publishing-automation:
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

- **Setup**: 1-2 hours (organization-wide rollout, security monitoring, advanced attestation verification)
- **Total from Start**: 2-3 hours (Level 1 + Level 2 + Level 3 advanced security)
- **Maintenance**: Quarterly security audits (30min), attestation policy reviews as needed

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
publishing-automation:
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
# Check SAP-028 status
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

**Overview**: How to migrate from [Alternative 1] to SAP-028

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

- **SAP-028 Protocol Spec**: [protocol-spec.md](./protocol-spec.md) - Technical contracts
- **SAP-028 Awareness Guide**: [awareness-guide.md](./awareness-guide.md) - AI agent instructions
- **SAP-028 Capability Charter**: [capability-charter.md](./capability-charter.md) - Problem and scope

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

**Before SAP-028**: [Baseline time/effort]
**After SAP-028 (Level 3)**: [New time/effort]
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
- **1.0.0** (2025-11-02): Initial adoption blueprint for Publishing Automation