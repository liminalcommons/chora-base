# chora-base Upgrade Guides

**Purpose**: Help adopters upgrade between chora-base template versions with AI agent-friendly decision frameworks.

---

## Quick Navigation

### Start Here

- **[Upgrade Philosophy](PHILOSOPHY.md)** - Understand chora-base's approach to upgrades, displacement policy, and decision frameworks

### Version-Specific Guides

| From | To | Guide | Effort | Displacement Risk |
|------|----|----|--------|-------------------|
| v1.0.0 | v1.1.0 | [v1.0-to-v1.1.md](v1.0-to-v1.1.md) | 30 min | LOW (docs only) |
| v1.1.0 | v1.2.0 | [v1.1-to-v1.2.md](v1.1-to-v1.2.md) | 1-2 hrs | HIGH (fixes + customizations) |
| v1.2.0 | v1.3.0 | [v1.2-to-v1.3.md](v1.2-to-v1.3.md) | 2-3 hrs | MEDIUM (vision framework) |
| v1.3.1 | v1.4.0 | [v1.3-to-v1.4.md](v1.3-to-v1.4.md) | 2-4 hrs | MEDIUM (workflow change) |
| v1.7.0 | v1.8.0 | [v1.7-to-v1.8.md](v1.7-to-v1.8.md) | 15-30 min | LOW (MCP naming) |
| v1.8.1 | v1.8.2 | [v1.8.1-to-v1.8.2.md](v1.8.1-to-v1.8.2.md) | 5-10 min | LOW (version fix) |
| v1.8.2 | v1.9.0 | [v1.8.2-to-v1.9.0.md](v1.8.2-to-v1.9.0.md) | 10-20 min | LOW (Docker opt-in) |
| v1.9.0 | v1.9.1 | [v1.9.0-to-v1.9.1.md](v1.9.0-to-v1.9.1.md) | 10-15 min | LOW (Docker enhancements) |
| v1.9.1 | v1.9.2 | [v1.9.1-to-v1.9.2.md](v1.9.1-to-v1.9.2.md) | 5-10 min | ZERO (docs discovery) |
| v1.9.2 | v1.9.3 | [v1.9.2-to-v1.9.3.md](v1.9.2-to-v1.9.3.md) | <10 min | ZERO (docs-only) |
| v1.9.3 | v2.0.0 | [v1.9.3-to-v2.0.0.md](v1.9.3-to-v2.0.0.md) | <10 min | ZERO (docs structure) |
| v2.0.1 | v2.0.2 | [v2.0.1-to-v2.0.2.md](v2.0.1-to-v2.0.2.md) | <5 min | ZERO (bug fix) |
| v2.0.2 | v2.0.3 | [v2.0.2-to-v2.0.3.md](v2.0.2-to-v2.0.3.md) | <2 min | ZERO (complete fix) |
| v2.0.3 | v2.0.4 | [v2.0.3-to-v2.0.4.md](v2.0.3-to-v2.0.4.md) | <1 min | ZERO (audit fix) |
| v2.0.4 | v2.0.5 | [v2.0.4-to-v2.0.5.md](v2.0.4-to-v2.0.5.md) | <1 min | ⚠️ FAILS (skip to v2.0.6) |
| v2.0.5 | v2.0.6 | [v2.0.5-to-v2.0.6.md](v2.0.5-to-v2.0.6.md) | <1 min | ZERO (actual root cause) |

**Status**:
- ✅ All version-specific guides complete (100% coverage v1.0.0 → v1.9.0)
- ✅ Cumulative guides complete (Phase 3)

### Cumulative Guides (Multi-Version Jumps)

For adopters multiple versions behind:

| From | To | Guide | Effort | vs Incremental |
|------|----|----|--------|----------------|
| v1.0.0 | v1.4.0 | [CUMULATIVE_v1.0-to-v1.4.md](CUMULATIVE_v1.0-to-v1.4.md) | 4-6 hrs | 30-40% faster |

**Status**: ✅ Complete (Phase 3) - Priority for original adopters (chora-compose, mcp-n8n teams)

### For Upgrade Guide Authors

- **[Upgrade Guide Template](UPGRADE_GUIDE_TEMPLATE.md)** - AI-optimized format for writing new upgrade guides

---

## How to Use These Guides

### For Human Developers

1. **Read Philosophy first**: [PHILOSOPHY.md](PHILOSOPHY.md) explains the upgrade approach
2. **Find your upgrade path**: Use the Version-Specific Guides table above
3. **Follow step-by-step**: Each guide has:
   - Time estimates
   - Conflict resolution strategies
   - Example upgrade sessions (real transcripts)
   - Rollback procedures

### For AI Agents

Each upgrade guide provides:

**Decision Trees**:
```
IF release contains CRITICAL fixes
  THEN: Upgrade required
ELSE IF new features align with project needs
  THEN: Evaluate benefits vs costs
...
```

**Structured Criteria**:
- Displacement analysis (required vs optional changes)
- File-by-file change summaries
- Merge strategies for customization preservation
- Validation checklists

**Knowledge Migration Patterns**:
- How to store ecosystem-wide patterns (e.g., `just --list`)
- How to update project-specific knowledge
- Example knowledge notes in JSON format

### For Multi-Version Jumps

If you're multiple versions behind (e.g., v1.0.0 → v1.4.0):

**Option 1: Incremental** (recommended if heavily customized)
```bash
# Upgrade one version at a time
copier update --vcs-ref v1.1.0
# Test, commit
copier update --vcs-ref v1.2.0
# Test, commit
copier update --vcs-ref v1.3.0
# Test, commit
copier update --vcs-ref v1.4.0
# Test, commit
```

**Option 2: Cumulative** (faster if low customization)
```bash
# Jump directly to target version
copier update --vcs-ref v1.4.0
# Use cumulative guide to resolve conflicts
```

See [PHILOSOPHY.md - Upgrade Strategy Patterns](PHILOSOPHY.md#upgrade-strategy-patterns) for detailed comparison.

---

## Upgrade Guide Format

All upgrade guides follow a consistent, AI-optimized format:

### Structure

1. **Quick Assessment** - TL;DR with effort, risk, decision criteria
2. **Decision Tree** - Structured IF/THEN logic for adoption decision
3. **What Changed** - File-by-file change summary with diffs
4. **Displacement Analysis** - Required vs optional vs additive changes
5. **Upgrade Steps** - Prerequisites → Execution → Validation
6. **Conflict Resolution** - Merge strategies for common conflicts
7. **Workflow Replacement Decision** (if applicable) - Benefits analysis, migration guide
8. **Validation Checklist** - Core functionality, template integration, quality gates
9. **Example Upgrade Session** - Real step-by-step transcript
10. **Rollback Procedure** - Recovery if upgrade fails
11. **Common Issues** - Known problems and solutions
12. **For AI Agents: Decision Documentation** - Knowledge note format

### Why This Format?

**For AI Agents**:
- Machine-parseable decision trees (no narrative prose required)
- Structured criteria (clear IF/THEN logic)
- Knowledge storage patterns (JSON examples)

**For Humans**:
- Time estimates up front (plan your work)
- Real examples (see exactly what to expect)
- Rollback procedures (safety net)

---

## Displacement Types

chora-base upgrades may involve **displacement** - when template changes advocate replacing existing workflows or code.

### Type 1: Required Displacement (Bug Fixes)

**Example**: v1.2.0 fixing `ImportError` in `memory/__init__.py`

**Policy**: Adopters MUST upgrade (correctness issue)

**Support**: Merge strategies for preserving customizations while applying fixes

### Type 2: Optional Displacement (Workflow Improvements)

**Example**: v1.4.0 making `just --list` the primary task discovery interface

**Policy**: Adopters MAY upgrade (DX improvement, not correctness)

**Support**:
- Benefits analysis (why new approach is better)
- Cost analysis (what changes)
- Decision criteria (when to adopt vs keep existing)
- Hybrid strategies (partial adoption)

### Type 3: Additive (Safe Enhancements)

**Example**: v1.3.0 adding `dev-docs/vision/` directory

**Policy**: Adopters choose what to adopt (pure addition)

**Support**: Integration guides for merging with existing docs

See [PHILOSOPHY.md - Displacement Policy](PHILOSOPHY.md#displacement-policy) for full details.

---

## Key Principles

### 1. Upgrades Are Safe

**Semantic Versioning**:
- MAJOR (X.0.0): Breaking changes (require adopter action)
- MINOR (1.X.0): New features (additive, optional)
- PATCH (1.1.X): Bug fixes (safe, recommended)

**Current Status**: v1.0.0 → v1.4.0 contains zero breaking changes

### 2. Customizations Are Preserved

**Template updates merge with local changes** (not blind overwrite)

**Merge Strategies**:
- Script customizations: Merge template improvements with local logic
- Documentation: Template sections + local sections coexist
- Configuration: New variables added, existing preserved

### 3. Decisions Are Supported

**Every upgrade guide provides**:
- Clear criteria for adopt/defer/skip
- Benefits analysis for workflow changes
- Time estimates and rollback procedures

### 4. Transparency Is Required

**Every release CHANGELOG includes**:
- Impact on existing adopters
- Displacement risk (HIGH/MEDIUM/LOW)
- Required vs optional designation

---

## Feedback Welcome

This is a living system based on real adoption experiences:

- **v1.4.0 upgrade guide**: Reference implementation based on mcp-n8n team feedback
- **Upgrade philosophy**: Informed by chora-compose adoption (98.75% parity achieved)
- **AI-optimized format**: Designed for LLM-intelligent agents

**Contribute**:
- Report upgrade friction via GitHub issues
- Suggest decision criteria improvements
- Share real upgrade session transcripts

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-19 | Initial upgrade documentation system (Phase 1) |
|  |  | - PHILOSOPHY.md created |
|  |  | - UPGRADE_GUIDE_TEMPLATE.md created |
|  |  | - v1.3-to-v1.4.md (reference implementation) |
|  |  | - template/UPGRADING.md.jinja added |
| 2.0 | 2025-10-19 | Complete upgrade guide coverage (Phase 2) |
|  |  | - v1.0-to-v1.1.md (docs enhancements) |
|  |  | - v1.1-to-v1.2.md (critical fixes) |
|  |  | - v1.2-to-v1.3.md (vision framework) |
|  |  | - 100% coverage for v1.0.0 → v1.4.0 |
| 3.0 | 2025-10-19 | Cumulative upgrade guide (Phase 3) |
|  |  | - CUMULATIVE_v1.0-to-v1.4.md (multi-version jump) |
|  |  | - Strategy comparison (cumulative vs incremental vs hybrid) |
|  |  | - 30-40% time savings for original adopters |

**Roadmap**:
- **Phase 2** (Complete): ✅ All version-specific guides (v1.0→v1.4)
- **Phase 3** (Complete): ✅ CUMULATIVE_v1.0-to-v1.4.md for original adopters
- **Phase 4** (Next): Add copier.yml upgrade mode prompts
- **Phase 5**: Validate with real-world upgrade case study

---

**Questions?** See [PHILOSOPHY.md](PHILOSOPHY.md) or open a GitHub issue.
