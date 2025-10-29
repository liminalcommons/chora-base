# Traceability Ledger: Project Bootstrap

**SAP ID**: SAP-003
**Current Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Generated Projects Registry

| Project | Template Version | Status | Generation Date | Last Upgrade | Notes |
|---------|------------------|--------|-----------------|--------------|-------|
| chora-compose | 3.0.0 | Active | 2025-10-15 | - | Meta-repository coordination |
| mcp-n8n | 3.0.0 | Active | 2025-10-18 | - | n8n automation MCP server |
| _No other known projects yet_ | - | - | - | - | Add entries as projects generated |

**Legend**:
- **Status**: Active (in development), Production (released), Archived (deprecated)
- **Generation Date**: Initial generation date (YYYY-MM-DD)
- **Last Upgrade**: Most recent template upgrade (YYYY-MM-DD)

---

## 2. Version History

| Version | Release Date | Type | Changes | Migration Required |
|---------|--------------|------|---------|-------------------|
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-003 release: Complete documentation of setup.py + blueprints + static-template generation system | N/A (initial) |

**Legend**:
- **Type**: MAJOR (breaking changes), MINOR (features), PATCH (fixes)
- **Migration Required**: Y/N, link to upgrade blueprint if yes

---

## 3. Active Deployments

### Template Versions in Use

**v3.3.0** (Current):
- **Projects**: chora-base (dogfooding), future generations
- **Status**: ✅ Active
- **Features**:
  - 12 blueprints (pyproject.toml, README, AGENTS, CHANGELOG, ROADMAP, CLAUDE, etc.)
  - 100+ static-template files
  - Zero-dependency generation (no Copier/Cookiecutter)
  - 85% test coverage threshold
  - Claude-optimized (20-40s generation)

**v3.0.0** (Previous):
- **Projects**: chora-compose, mcp-n8n
- **Status**: ✅ Active (supported)
- **Features**: Similar to v3.3.0 (minor differences)

**v2.x** (Legacy):
- **Projects**: Unknown (no tracking before v3.0)
- **Status**: ⚠️ Upgrade recommended
- **Features**: Pre-blueprint system (limited)

---

## 4. Generation Metrics

### Phase 2 (Current)

**Target**: Document generation system (SAP-003 complete)
**Actual**: SAP-003 complete (all 5 artifacts)
**Status**: ✅ On track

**Metrics**:
- **Generation Success Rate**: ~95% (baseline, 5% placeholder issues)
  - Target: 100% (with validation improvements)
- **Generation Time** (agent): 30-60s (baseline)
  - Target: 20-40s (with optimizations)
- **Known Projects Generated**: 2 (chora-compose, mcp-n8n)
  - Target: 5+ (Phase 2-3)
- **Support Issues** (generation-related): ~30% of all issues (baseline)
  - Target: <20% (Phase 3), <10% (Phase 4)

### Phase 3 (2026-01 → 2026-03)

**Target**: Improve generation reliability and performance

**Planned Metrics**:
- Generation success rate: 100% (zero placeholder issues)
- Generation time (agent): 25-45s (optimized)
- Known projects: 5-8 (more adopters)
- Support issues: <20% (better docs)

### Phase 4 (2026-03 → 2026-05)

**Target**: Automate validation and optimization

**Planned Metrics**:
- Generation success rate: 100% (automated validation)
- Generation time (agent): 20-40s (fully optimized)
- Known projects: 10+ (wider adoption)
- Support issues: <10% (comprehensive docs + automation)

---

## 5. Known Issues

### Active Issues

**Issue: Placeholder substitution edge cases**
- **Description**: Rare cases where {{ var | filter }} with specific spacing fails
- **Severity**: Low (affects <5% of generations)
- **Workaround**: Use consistent spacing ({{ var | upper }} not {{var|upper}})
- **Status**: Documented in Protocol Section 3.2
- **Fix**: Planned for v1.1.0 (normalize spacing in process_blueprints)

**Issue: Large static-template copy slow on network drives**
- **Description**: Copying 100+ files to network drive takes > 30 seconds
- **Severity**: Low (rare scenario)
- **Workaround**: Generate locally, then move to network drive
- **Status**: Documented in Troubleshooting
- **Fix**: Not planned (user configuration issue)

### Resolved Issues

_None yet_ - SAP-003 is new

---

## 6. Blueprint Inventory

### Current Blueprints (v3.3.0)

| Blueprint File | Target Path | Variables Used | Status |
|----------------|-------------|----------------|--------|
| pyproject.toml.blueprint | pyproject.toml | project_slug, project_version, project_description, author_name, author_email, python_version, package_name | ✅ Active |
| README.md.blueprint | README.md | project_name, project_description, github_username, project_slug, test_coverage_threshold, package_name | ✅ Active |
| AGENTS.md.blueprint | AGENTS.md | project_name, package_name, project_description | ✅ Active |
| CHANGELOG.md.blueprint | CHANGELOG.md | project_version, generation_date | ✅ Active |
| ROADMAP.md.blueprint | ROADMAP.md | project_name, project_version | ✅ Active |
| CLAUDE.md.blueprint | CLAUDE.md | project_name, package_name | ✅ Active |
| .gitignore.blueprint | .gitignore | (none) | ✅ Active |
| .env.example.blueprint | .env.example | (none) | ✅ Active |
| package__init__.py.blueprint | src/{package_name}/__init__.py | package_name, project_version | ✅ Active |
| server.py.blueprint | src/{package_name}/mcp/server.py | package_name, project_name, mcp_namespace | ✅ Active |
| mcp__init__.py.blueprint | src/{package_name}/mcp/__init__.py | package_name | ✅ Active |

**Total**: 11 blueprints (12 including potential future additions)

### Blueprint Coverage

- **Core Configuration**: 100% (pyproject.toml, .gitignore, .env.example)
- **Documentation**: 100% (README, AGENTS, CHANGELOG, ROADMAP, CLAUDE)
- **Source Code**: 100% (package __init__, server, mcp __init__)
- **Tests**: 0% (no test blueprints yet, static-template only)
- **CI/CD**: 0% (no workflow blueprints yet, static-template only)

---

## 7. Static Template Inventory

### Directory Structure (v3.3.0)

```
static-template/
├── src/
│   ├── __package_name__/          # Renamed to package_name during generation
│   │   ├── __init__.py
│   │   ├── cli/                   # CLI interface
│   │   ├── mcp/                   # MCP server implementation
│   │   ├── memory/                # A-MEM system (event_log, knowledge_graph, trace)
│   │   └── utils/                 # Utilities (validation, errors, responses, persistence)
│   └── {{package_name}}/          # Alternative naming (for specific blueprints)
├── tests/
│   ├── conftest.py                # Pytest configuration
│   ├── test_mcp_server.py         # Example MCP server tests
│   ├── memory/                    # Memory system tests
│   └── utils/                     # Utility tests
├── scripts/
│   ├── dev-server.sh              # Development server
│   ├── setup.sh                   # Environment setup
│   ├── build-dist.sh              # Build distribution
│   ├── publish-prod.sh            # Publish to PyPI
│   └── [16 other scripts]         # Various automation scripts
├── .github/workflows/
│   ├── test.yml                   # Test workflow (pytest + coverage)
│   ├── quality.yml                # Quality workflow (ruff, mypy)
│   ├── build.yml                  # Build workflow
│   ├── deploy.yml                 # Deployment workflow
│   └── [6 other workflows]        # Various CI/CD workflows
├── docker/
│   ├── Dockerfile                 # Production Docker image
│   ├── Dockerfile.dev             # Development Docker image
│   └── docker-compose.yml         # Multi-service setup
├── docs/
│   ├── dev-docs/                  # Developer documentation
│   ├── user-docs/                 # User documentation
│   └── project-docs/              # Project documentation
├── CLAUDE.md                      # Claude-specific guidance
├── AGENTS.md                      # Agent guidance (from blueprint)
├── README.md                      # Project overview (from blueprint)
├── CHANGELOG.md                   # Version history (from blueprint)
├── ROADMAP.md                     # Project roadmap (from blueprint)
├── pyproject.toml                 # Project configuration (from blueprint)
├── .gitignore                     # Git ignore (from blueprint)
└── .env.example                   # Environment template (from blueprint)
```

**Total Files**: ~100 files
**Total Directories**: ~27 directories

### File Categories

| Category | Count | Examples |
|----------|-------|----------|
| Source Code | ~15 | src/{package}/*.py |
| Tests | ~10 | tests/**/*.py |
| Scripts | ~20 | scripts/*.sh, scripts/*.py |
| CI/CD | ~10 | .github/workflows/*.yml |
| Docker | ~3 | Dockerfile, docker-compose.yml |
| Documentation | ~30 | docs/**/*.md, *.md files |
| Configuration | ~12 | pyproject.toml, .gitignore, justfile, etc. |

---

## 8. Upgrade Paths

### Template Upgrades

**v3.0 → v3.3**:
- **Status**: Upgrade blueprint available (docs/upgrades/v3.0-to-v3.3.md)
- **Breaking Changes**: None (backward compatible)
- **New Features**:
  - CLAUDE.md blueprint added
  - Enhanced AGENTS.md with SAP section
  - Updated workflows (quality.yml improvements)
- **Migration Time**: 1-2 hours (manual file updates)

**v2.x → v3.0**:
- **Status**: Major upgrade, blueprint recommended but not complete
- **Breaking Changes**: Yes (blueprint system introduced, directory structure changed)
- **Migration Time**: 4-8 hours (significant restructuring)
- **Recommendation**: Regenerate project if possible, or manual migration

**Future Upgrades**:
- **v3.3 → v4.0**: TBD (no breaking changes planned yet)
- **v4.0 → v5.0**: TBD (distant future)

---

## 9. Adoption Feedback

### Phase 2 Feedback (2025-10 → 2026-01)

**Collected From**: chora-base maintainer (Victor), early adopters (chora-compose, mcp-n8n)

**Key Themes**:
- ✅ **Generation speed**: Fast (30-60s with agent), acceptable
- ✅ **Clarity**: setup.py prompts clear, derived values helpful
- ⚠️ **Placeholder issues**: Rare but confusing (5% of generations)
- ✅ **Validation**: Validation step helpful, catches most issues
- ⚠️ **Upgrades**: No structured upgrade path yet (manual process)

**Action Items**:
- ✅ Document generation system (SAP-003 created)
- 🔄 Create upgrade blueprints (planned for Phase 3)
- 🔄 Improve placeholder detection (planned for v1.1.0)
- 🔄 Add automated generation testing in CI (planned for Phase 4)

### Phase 3 Feedback (Future)

_Not yet collected_

---

## 10. Compliance & Audit

### Generation Quality Gates

**Validation Checks** (setup.py:318-358):
- ✅ Critical files exist (7 files checked)
- ✅ No unreplaced placeholders in key files (3 files checked)
- ✅ Tests loadable (pytest --collect-only)
- ✅ Package imports (Python validity)
- ✅ Git initialized (repository ready)

**Success Criteria**:
- 100% of validation checks pass
- Zero {{ placeholders }} in key files
- All critical files present

### Blueprint Quality Gates

**Current** (Phase 2):
- ✅ All 11 blueprints documented
- ✅ Variable usage documented
- ✅ Blueprint mappings correct
- ⚠️ No automated blueprint testing (manual only)

**Planned** (Phase 4):
- Automated blueprint inventory check (CI)
- Automated variable coverage check (CI)
- Automated generation testing (CI)

### Audit Trail

| Date | Auditor | Finding | Resolution |
|------|---------|---------|------------|
| 2025-10-28 | Claude Code | SAP-003 created | Complete documentation of generation system |
| _Future audits_ | - | - | - |

---

## 11. Performance Tracking

### Generation Time (by Component)

| Component | Time (Agent) | Time (Human) | Target |
|-----------|--------------|--------------|--------|
| Copy static-template | 5-10s | 5-10s | 3-8s |
| Rename directories | 1-2s | 1-2s | 1-2s |
| Process blueprints | 3-5s | 3-5s | 2-4s |
| Initialize git | 2-5s | 2-5s | 2-5s |
| Validation | 2-5s | 2-5s | 1-3s |
| **Total** | **30-60s** | **60-90s** | **20-40s** |

**Notes**:
- Agent (Claude Code): Can parallelize blueprint reading, git config checks
- Human: Must wait for prompts (adds 30-60s)
- Target: Optimized parallel operations (Phase 4)

### Optimization Opportunities

1. **Parallel blueprint reading** - Read all blueprints at once (save 2-3s)
2. **Pre-computed mappings** - Cache blueprint mappings (save 1-2s)
3. **Incremental validation** - Validate during generation, not after (save 2-3s)
4. **Optimized file copy** - Batch copy operations (save 2-3s)

---

## 12. Related Documents

**SAP-003 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to generate projects

**Generation Components**:
- [setup.py](/setup.py) - Generation orchestrator (443 lines)
- [blueprints/](/blueprints/) - Variable templates (11 files)
- [static-template/](/static-template/) - Project scaffold (100+ files)

**Related SAPs**:
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP Section 3.2.1
- [chora-base/ledger.md](../chora-base/ledger.md) - Adopter tracking (chora-compose, mcp-n8n)
- [INDEX.md](../INDEX.md) - SAP registry

**Upgrade Documentation**:
- Upgrade blueprints (planned for `/docs/upgrades/`)
- [CHANGELOG.md](/CHANGELOG.md) - Version history

---

## 13. How to Update This Ledger

### Adding Generated Project

**When**: New project generated using setup.py

**Steps**:
1. Add row to "Generated Projects Registry" table:
   ```markdown
   | <project-name> | <template-version> | Active | <today> | - | <notes> |
   ```
2. If external project, create PR to chora-base
3. Commit message: `docs(SAP-003): Add <project-name> to generated projects registry`

### Recording Template Version Release

**When**: New chora-base version released (setup.py TEMPLATE_VERSION updated)

**Steps**:
1. Add row to "Version History" table
2. Update "Active Deployments" section (add new version, mark old as previous)
3. Create upgrade blueprint if breaking changes
4. Update "Upgrade Paths" section
5. Commit message: `release(chora-base): Release v<version>`

### Recording Generation Issues

**When**: Issue discovered with generation system

**Steps**:
1. Add to "Known Issues" → "Active Issues" section
2. Link to GitHub issue if reported
3. When resolved, move to "Resolved Issues" with resolution
4. Commit message: `docs(SAP-003): Document issue #<number>`

### Recording Blueprint Changes

**When**: Blueprint added, modified, or removed

**Steps**:
1. Update "Blueprint Inventory" table
2. Update "Blueprint Coverage" if new category
3. Update Protocol Section 3.3 (blueprint mappings)
4. Commit message: `feat(blueprints): Add/update <blueprint-name>`

### Recording Performance Metrics

**When**: Generation time measured or optimizations applied

**Steps**:
1. Update "Performance Tracking" table
2. Add optimization notes if improvements made
3. Update targets if achieved
4. Commit message: `perf(generation): <optimization description>`

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger for project-bootstrap SAP
