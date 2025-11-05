# Traceability Ledger: Publishing Automation

**SAP ID**: SAP-028
**Current Version**: 1.0.0
**Status**: pilot
**Last Updated**: 2025-11-02

---

## 1. Version History

### v1.0.0 (2025-11-02) - Initial Release

**Status**: Pilot
**Release Type**: Major (Initial SAP formalization)
**Phase**: Immediate

**Summary**:
First formalization of Publishing Automation as SAP-028.

**Key Features**:


- OIDC trusted publishing (recommended default)

- Token-based publishing (backward compatibility)

- Manual publishing (local development)

- PEP 740 attestations for build provenance

- GitHub Actions workflow integration

- Migration protocols (token → trusted publishing)

- Template integration via pypi_auth_method variable



**Rationale**:
Created to address the security risks of token-based PyPI publishing: long-lived PYPI_API_TOKEN secrets in GitHub Secrets pose leakage risk, require manual 90-day rotation, lack build provenance (PEP 740), and don't provide fine-grained trust relationships. PyPI introduced OIDC trusted publishing in 2023 as the recommended default, enabling zero-secret publishing with ephemeral tokens, automatic PEP 740 attestations, and repository-scoped trust. However, chora-base static templates defaulted to token-based publishing, requiring manual migration. SAP-028 provides secure-by-default publishing automation: OIDC trusted publishing as template default, token-based fallback for legacy compatibility, migration guide for existing projects, and integration with SAP-003/SAP-005 for seamless adoption in new projects.

**Dependencies**:


- SAP-003

- SAP-005



**Related Releases**:
- Publishing Automation v1.0.0 (2025-11-02)

**Adoption Targets**:

- All new projects using chora-base
- Existing projects (migration guide provided)


---

## 2. Adoption Tracking

### Project Adoption

| Project | Adoption Level | Features Used | Installation Date | Status |
|---------|---------------|---------------|-------------------|--------|
| chora-compose | Level 2 (Advanced) | Migrated from token to OIDC trusted publishing. PEP 740 attestations enabled. Zero security incidents post-migration. | 2024-Q4 (prior to SAP-028) | ✅ Active (production validation) |
| chora-base (static-template) | Level 1 (Basic) | OIDC trusted publishing as template default. pypi_auth_method variable for flexibility. Documentation (PYPI_SETUP.md). | 2025-11-02 | ✅ Active (templates updated) |
| Future adopters (TBD) | Level 1 (Basic) | New projects bootstrapped with SAP-003 will inherit SAP-028 publishing automation by default. | Ongoing | ⏳ Pending (ecosystem adoption)|

**Adoption Metrics**:
- **Projects using SAP-028**: 2/∞ (chora-compose + static-template, ecosystem adoption ongoing)
- **Target**: 5+ new projects adopt trusted publishing by 2025-12-31

### Adoption by Level

| Level | Projects | Percentage |
|-------|----------|------------|
| Level 1 (Basic) | 1 (static-template) | 50% |
| Level 2 (Advanced) | 1 (chora-compose migration) | 50% |
| Level 3 (Mastery) | 0 | 0% |

---

## 3. Integration Points

### SAP Integration

| SAP | Integration Type | Details |
|-----|-----------------|---------| 

| **SAP-003** | Dependency | New projects bootstrapped with SAP-003 inherit SAP-028 publishing automation by default. static-template/.github/workflows/release.yml configured for OIDC trusted publishing (pypi_auth_method: oidc). |

| **SAP-005** | Dependency | GitHub Actions workflows (SAP-005) provide CI/CD infrastructure for SAP-028 release automation. Release workflow triggers on git tags, builds package, generates attestations, publishes to PyPI. |



### External Integration

| External System | Integration Type | Version/Link |
|----------------|------------------|--------------|
| PyPI | Publishing Platform | https://pypi.org (OIDC trusted publishing, PEP 740 attestations) |
| GitHub Actions | CI/CD Platform | https://github.com/features/actions (OIDC token provider, workflow automation) |
| pypa/gh-action-pypi-publish | GitHub Action | v1.8.0+ https://github.com/pypa/gh-action-pypi-publish (official PyPI publish action) |
| PEP 740 | Build Attestation Spec | https://peps.python.org/pep-0740/ (build provenance standard) |
| GitHub OIDC | Authentication Protocol | https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect (ephemeral token generation) |

---

## 4. Performance Metrics

### Usage Benchmarks

| Metric | Value | Measurement Date | Notes |
|--------|-------|------------------|-------|
| OIDC setup time (new project) | 5 minutes | 2025-11-02 | Configure PyPI publisher (2min) + add workflow (3min). One-time setup per project. |
| Token→OIDC migration time | 15 minutes | 2024-Q4 | chora-compose migration: PyPI config (5min) + workflow update (5min) + validation (5min). |
| Security incidents (post-OIDC) | 0 | 2024-Q4 to present | Zero token leakage incidents in chora-compose after OIDC migration. |
| PEP 740 attestation coverage | 100% | 2025-11-02 | All OIDC-published releases include build provenance attestations. |
| Token rotation burden eliminated | 100% | 2024-Q4 | chora-compose: No 90-day PYPI_API_TOKEN rotation required post-migration. |

**Key Insights**: OIDC setup adds 5min one-time overhead but eliminates ongoing rotation burden (4x/year × 15min = 60min/year saved per project). Migration takes 15min, breaks even after 4 months. Zero security incidents validate OIDC security model.

---

## 5. Security Events

### Incident Log

No security incidents recorded for SAP-028.

**Preventive Measures**:
- OIDC trusted publishing as template default (eliminates token leakage attack surface)
- Repository-scoped trust configuration (limits blast radius if workflow compromised)
- Environment protection rules (optional approval gate for release environment)
- PEP 740 attestations (build provenance verification for supply chain attacks)

---

## 6. Changes Since Last Version

### v1.0.0 (2025-11-02)

**Changes from**: Initial release (no previous version)

**New Features**:


- ✅ OIDC trusted publishing (recommended default)

- ✅ Token-based publishing (backward compatibility)

- ✅ Manual publishing (local development)

- ✅ PEP 740 attestations for build provenance

- ✅ GitHub Actions workflow integration

- ✅ Migration protocols (token → trusted publishing)

- ✅ Template integration via pypi_auth_method variable



**Modified**:
- N/A (initial release)

**Deprecated**:
- N/A (initial release)

**Removed**:
- N/A (initial release)

**Migration Required**:
- No migration needed (initial release)

---

## 7. Testing & Validation

### Manual Testing Results

| Test Case | Status | Date | Notes |
|-----------|--------|------|-------|
| chora-compose token→OIDC migration | ✅ Pass | 2024-Q4 | Migrated from PYPI_API_TOKEN to OIDC trusted publishing. Release v1.2.3 published successfully. PEP 740 attestations verified on PyPI. |
| static-template OIDC default | ✅ Pass | 2025-11-02 | Template .github/workflows/release.yml configured with OIDC. pypi_auth_method variable supports oidc/token/manual. |
| PyPI publisher configuration | ✅ Pass | 2024-Q4 | Configured trusted publisher for chora-compose: repository liminalcommons/chora-compose, workflow release.yml, environment release. |
| PEP 740 attestation generation | ✅ Pass | 2024-Q4 | All OIDC-published releases include build attestations. Verified via PyPI Attestations tab. |

### Validation Status

| Validation Type | Status | Last Run | Result |
|----------------|--------|----------|--------|
| Artifact completeness | ✅ Pass | 2025-11-02 | All 5 SAP artifacts present (capability-charter, protocol-spec, awareness-guide with AGENTS.md + CLAUDE.md, adoption-blueprint, ledger) |
| Link validation | ⏳ Pending | N/A | Will run during Phase 2 validation |
| Example validation | ✅ Pass | 2024-Q4 | chora-compose production validation confirms OIDC publishing works as documented |

---

## 8. Known Issues & Limitations

### Current Limitations

**L1**: GitHub Actions only (no GitLab/Bitbucket CI support yet)
- **Issue**: OIDC trusted publishing implementation only supports GitHub Actions workflows
- **Workaround**: Use token-based publishing for non-GitHub CI platforms
- **Status**: Planned enhancement
- **Planned Fix**: v1.1.0 GitLab CI OIDC support, v1.2.0 Bitbucket Pipelines

**L2**: PyPI only (no private registry support)
- **Issue**: OIDC configuration specific to PyPI, does not work with Artifactory, Nexus, or other private registries
- **Workaround**: Use token-based publishing for private registries
- **Status**: Planned enhancement
- **Planned Fix**: v1.2.0 investigate private registry OIDC patterns

**L3**: Requires GitHub repository ownership for OIDC setup
- **Issue**: OIDC trusted publisher configuration requires repository admin/owner permissions
- **Workaround**: Request repo admin to configure OIDC, then contributors can publish
- **Status**: By design (GitHub security model)
- **Planned Fix**: None - inherent to OIDC trust model

### Resolved Issues

None (initial release)

---

## 9. Documentation Links

### SAP-028 Artifacts

- [Capability Charter](./capability-charter.md) - SAP-028 overview, problem statement, scope
- [Protocol Specification](./protocol-spec.md) - Technical contracts and specifications
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference and workflows
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step adoption guide (Level 1-3)
- [Traceability Ledger](./ledger.md) - This document

### Related SAPs

- [SAP-000: SAP Framework](../sap-framework/) - Core SAP protocols


- [SAP-003: Project Bootstrap](../project-bootstrap/) - New project scaffolding with SAP-028 publishing automation by default

- [SAP-005: CI/CD Workflows](../ci-cd-workflows/) - GitHub Actions infrastructure for release automation



### External Resources

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) - Official PyPI documentation for OIDC trusted publishing
- [PEP 740: Index Support for Digital Attestations](https://peps.python.org/pep-0740/) - Build provenance specification
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) - Official GitHub Action for PyPI publishing
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) - GitHub Actions OIDC token generation
- [PyPI Security Model](https://warehouse.pypa.io/security.html) - PyPI security best practices

---

## 10. Future Enhancements

### Planned Features (v1.1.0 - 2025-12-31)

**F1**: GitLab CI OIDC Support
- **Description**: Add GitLab CI trusted publishing support (analogous to GitHub Actions OIDC)
- **Scope**: New workflow template for GitLab CI, documentation updates, adoption-blueprint GitLab section
- **Effort**: 4-6 hours
- **Priority**: Medium
- **Blocking**: GitLab CI OIDC token provider availability

**F2**: TestPyPI Environment Support
- **Description**: Add TestPyPI publishing workflow for pre-release testing
- **Scope**: New workflow template for TestPyPI, PYPI_SETUP.md section on TestPyPI trusted publisher configuration
- **Effort**: 2-3 hours
- **Priority**: Medium
- **Blocking**: None

### Planned Features (v1.2.0 - 2026-Q1)

**F3**: Bitbucket Pipelines OIDC Support
- **Description**: Add Bitbucket Pipelines trusted publishing support
- **Scope**: New workflow template for Bitbucket Pipelines, documentation updates
- **Effort**: 4-6 hours
- **Priority**: Low
- **Blocking**: Bitbucket Pipelines OIDC token provider availability

**F4**: Private Registry OIDC Patterns
- **Description**: Investigate OIDC trusted publishing patterns for Artifactory, Nexus, private registries
- **Scope**: Research spike, documentation of feasibility, proof-of-concept if viable
- **Effort**: 8-10 hours
- **Priority**: Low
- **Blocking**: Private registry OIDC support

---

## 11. Stakeholder Feedback

### Feedback Log

**Feedback 1**: 2024-Q4 - Victor (chora-compose migration)
- **Feedback**: "OIDC migration took 15 minutes, eliminated 90-day token rotation burden. Zero friction after initial setup."
- **Action**: Validated as production-ready pattern, made OIDC default in static-template
- **Status**: Closed (incorporated into SAP-028 v1.0.0)

**Feedback 2**: 2025-11-02 - Claude Code Agent (template review)
- **Feedback**: "pypi_auth_method variable provides good flexibility for token fallback without sacrificing OIDC-first approach."
- **Action**: Retained variable design in static-template release workflow
- **Status**: Closed (design confirmed)

**Feedback 3**: 2025-11-02 - Victor (future roadmap)
- **Feedback**: "Need TestPyPI support for pre-release testing before production publish."
- **Action**: Added F2 (TestPyPI Environment Support) to v1.1.0 roadmap
- **Status**: Open (planned for v1.1.0)

---

## 12. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| **1.0.0** | 2025-11-02 | chora-base | Initial release: Formalized Publishing Automation as SAP-028 |

---

## 13. Appendix: SAP-028 Metadata

### Artifact Completeness

| Artifact | Status | Lines | Last Updated |
|----------|--------|-------|--------------| | **capability-charter.md** | ✅ Complete | ~TBD | 2025-11-02 |
| **protocol-spec.md** | ✅ Complete | ~TBD | 2025-11-02 |
| **awareness-guide.md** | ✅ Complete | ~TBD | 2025-11-02 |
| **adoption-blueprint.md** | ✅ Complete | ~TBD | 2025-11-02 |
| **ledger.md** | ✅ Complete | ~TBD | 2025-11-02 |

**Total Documentation**: ~TBD lines

### SAP-028 Metadata

```json
{
  "id": "SAP-028",
  "name": "publishing-automation",
  "full_name": "Publishing Automation",
  "version": "1.0.0",
  "status": "pilot",
  "size_kb": 125,
  "description": "Secure PyPI publishing with OIDC trusted publishing as default, eliminating long-lived API tokens for chora-base generated projects",
  "capabilities": ["OIDC trusted publishing (recommended default)", "Token-based publishing (backward compatibility)", "Manual publishing (local development)", "PEP 740 attestations for build provenance", "GitHub Actions workflow integration", "Migration protocols (token \u2192 trusted publishing)", "Template integration via pypi_auth_method variable"],
  "dependencies": ["SAP-003", "SAP-005"],
  "tags": ["security", "publishing", "ci-cd", "pypi", "oidc", "production"],
  "author": "chora-base",
  "location": "docs/skilled-awareness/publishing-automation",
  "phase": "Immediate",
  "priority": "P0"
}
```

---

**Ledger Maintained By**: chora-base
**Next Review**: [Date] (quarterly or upon major feature addition)
**Change Frequency**: Quarterly or upon major release
