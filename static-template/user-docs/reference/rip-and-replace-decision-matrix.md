# Reference: Rip-and-Replace Decision Matrix

## Quick Lookup

When to use rip-and-replace vs cherry-pick adoption strategy

---

## Decision Matrix

| Criterion | Rip-and-Replace | Cherry-Pick Adoption | Net New Project |
|-----------|----------------|----------------------|-----------------|
| **Existing Infrastructure** | Fragmented, outdated | Partial, functional | None |
| **Time Investment** | 2-3 hours | 3-4 hours (higher) | 30 minutes |
| **Risk Level** | Medium (requires backup) | Low (additive only) | Low (greenfield) |
| **Code Preservation** | 100% (all project code) | 100% (all project code) | N/A |
| **Infrastructure Gain** | Complete replacement | Selective addition | All template features |
| **Major Version Bump** | Recommended (v0.x → v1.0) | Optional | N/A (v0.1.0 start) |
| **Git History** | Preserved (commit + tag) | Preserved (additive commits) | New repo |
| **Recommended When** | Missing 80%+ template features | Missing 20-50% features | Starting from scratch |

---

## Use Case Examples

### Rip-and-Replace (Recommended)

**Scenario:** mcp-server-coda
- ✅ Has: 21 source files, 33 tests, 3 workflows, comprehensive docs
- ❌ Missing: scripts/ (18 scripts), memory system, AGENTS.md, justfile, pre-commit hooks
- **Decision:** Rip-and-replace (missing 80% of infrastructure)

**Why:**
- Faster to regenerate infrastructure than add piecemeal
- Major version bump signals infrastructure overhaul
- Complete standardization with chora-base

**Outcome:**
- 2-3 hours work
- v1.0.0 release
- All template features + all project code

---

### Cherry-Pick Adoption (Alternative)

**Scenario:** chora-composer
- ✅ Has: Scripts (9 Python scripts), AGENTS.md (19K lines), justfile, pre-commit hooks
- ❌ Missing: Workflows (7 GitHub Actions), memory system, shell scripts (18 automation)
- **Decision:** Cherry-pick (missing 40% of infrastructure)

**Why:**
- Existing AGENTS.md is more comprehensive than template
- Python scripts are project-specific (docs generation)
- Merge is simpler than full regeneration

**Outcome:**
- 3-4 hours work
- v0.7.0 release (minor bump)
- Hybrid structure (existing + template features)

---

### Net New Project (Recommended)

**Scenario:** Starting new MCP server
- ❌ Has: Nothing (greenfield)
- **Decision:** `copier copy gh:liminalcommons/chora-base`

**Why:**
- Fastest path to production-ready structure
- No migration complexity
- All template features from day 1

**Outcome:**
- 30 minutes work
- v0.1.0 release
- Complete template features

---

## Feature Comparison Table

| Feature | Rip-and-Replace | Cherry-Pick | Net New |
|---------|----------------|-------------|---------|
| **Scripts (18)** | ✅ Replace all | ✅ Add missing | ✅ All included |
| **Workflows (7)** | ✅ Replace all | ✅ Add missing | ✅ All included |
| **Memory System** | ✅ Add new | ✅ Add new | ✅ All included |
| **AGENTS.md** | ✅ Replace + customize | ⚠️ Merge or keep | ✅ Customize template |
| **justfile** | ✅ Replace + customize | ⚠️ Merge tasks | ✅ Customize template |
| **Pre-commit** | ✅ Replace | ✅ Add if missing | ✅ All included |
| **pyproject.toml** | ⚠️ Merge (complex) | ⚠️ Merge (additive) | ✅ Template default |
| **README.md** | ⚠️ Merge (add origin) | ⚠️ Add badge | ✅ Customize template |
| **Project Code** | ✅ Preserve 100% | ✅ Preserve 100% | 🆕 Implement from scratch |

**Legend:**
- ✅ Full benefit
- ⚠️ Requires manual work
- 🆕 New implementation

---

## Complexity Comparison

### Rip-and-Replace Phases

1. Backup (10 min) - Low complexity
2. Extract Assets (15 min) - Low complexity
3. Generate Template (15 min) - Low complexity
4. Migrate Code (20 min) - Medium complexity
5. Merge Hybrid Files (30 min) - **High complexity** (pyproject.toml, README.md)
6. Adapt Features (20 min) - Medium complexity
7. Validate (15 min) - Low complexity
8. Replace Repo (10 min) - Low complexity

**Total:** 2h 15min, **Highest Risk:** Phase 5 (file merging)

---

### Cherry-Pick Adoption Phases

1. Identify Gaps (30 min) - Low complexity
2. Add Scripts (20 min) - Low complexity
3. Add Workflows (20 min) - Low complexity
4. Add AGENTS.md (40 min) - **High complexity** (template vs existing)
5. Add Memory System (30 min) - Medium complexity
6. Merge justfile (30 min) - Medium complexity
7. Update Docs (20 min) - Low complexity
8. Validate (15 min) - Low complexity

**Total:** 3h 25min, **Highest Risk:** Phase 4 (AGENTS.md conflict)

---

## When NOT to Rip-and-Replace

| Anti-Pattern | Reason | Alternative |
|--------------|--------|-------------|
| **Complex build system** | Regenerating pyproject.toml risks breaking builds | Cherry-pick scripts/, workflows/ only |
| **Custom AGENTS.md (5000+ lines)** | Template AGENTS.md is less comprehensive | Keep existing, add memory system separately |
| **Uses Poetry (template uses setuptools)** | Build system mismatch | Cherry-pick features, keep Poetry |
| **Non-standard structure** | Template assumes src/ layout | Cherry-pick docs/, workflows/ only |
| **Mature versioning (v5.0+)** | Major version bump loses semantic meaning | Cherry-pick, bump minor version |

---

## Validation Checklist

### Before Rip-and-Replace

- [ ] Backup branch created (`backup-pre-rip-replace`)
- [ ] Backup tag created (`backup-v0.x.y`)
- [ ] Test count documented (`pytest --collect-only > pre-rip-replace-tests.txt`)
- [ ] Dependencies documented (`cat pyproject.toml > pre-rip-replace-pyproject.toml`)

### After Rip-and-Replace

- [ ] All tests passing (same count as before)
- [ ] Test coverage ≥ threshold (85%)
- [ ] Lint checks passing (`ruff check`)
- [ ] Type checks passing (`mypy`)
- [ ] Format checks passing (`black --check`)
- [ ] Smoke tests passing (`./scripts/smoke-test.sh`)
- [ ] Integration tests passing (`./scripts/integration-test.sh`)
- [ ] Pre-merge validation passing (`./scripts/pre-merge.sh`)

---

## See Also

- [How-To: Rip-and-Replace Existing MCP Server](../how-to/02-rip-and-replace-existing-server.md)
- [Tutorial: Rip-and-Replace Migration](../tutorials/02-rip-and-replace-migration.md)
- [Explanation: Why Rip-and-Replace?](../explanation/why-rip-and-replace.md)
