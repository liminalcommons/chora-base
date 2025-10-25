# chora-base Upgrade Philosophy

**Version:** 1.0
**Audience:** Human developers, AI coding agents, project maintainers
**Purpose:** Define upgrade guarantees, displacement policies, and decision frameworks

---

## Table of Contents

1. [Upgrade Promise](#upgrade-promise)
2. [Displacement Policy](#displacement-policy)
3. [Customization Preservation](#customization-preservation)
4. [Decision Framework for AI Agents](#decision-framework-for-ai-agents)
5. [Upgrade Strategy Patterns](#upgrade-strategy-patterns)
6. [Breaking Changes Policy](#breaking-changes-policy)

---

## Upgrade Promise

### What chora-base Guarantees

**Semantic Versioning Commitment:**
- **MAJOR (X.0.0)**: Breaking changes that require adopter action
- **MINOR (1.X.0)**: New features, additive changes, optional upgrades
- **PATCH (1.1.X)**: Bug fixes, documentation improvements, safe upgrades

**Current Status**: chora-base is at v1.4.0 - all changes so far have been MINOR (additive features) or PATCH (fixes/docs).

**Backward Compatibility:**
- Template variable names remain stable (no renaming existing variables)
- Existing copier answers (.copier-answers.yml) continue to work
- Generated projects from v1.0.0 remain functional (no forced upgrades)

**Upgrade Path Guarantee:**
- Every version can upgrade to the next version (v1.0→v1.1→v1.2→...)
- Version-specific upgrade guides provided for each transition
- Cumulative upgrade guides for multi-version jumps (e.g., v1.0→v1.4)

### What chora-base Does NOT Guarantee

**Not Guaranteed:**
- Generated project code remains identical across versions (improvements happen!)
- Workflow patterns remain unchanged (we evolve best practices)
- Documentation structure stays static (we improve organization)
- Optional features remain optional forever (some become recommended/default)

**Why This Matters:**
chora-base evolves based on real-world adoption feedback. When we discover better patterns (like v1.4.0's `just --list` for task discovery), we update templates to include them. This creates **displacement friction** for existing adopters.

---

## Displacement Policy

### Definition

**Displacement** occurs when a template update advocates replacing or restructuring something an adopter has already built.

### Displacement Types

#### Type 1: Bug Fixes (Required Displacement)
**Example**: v1.2.0 fixing `ImportError` in `memory/__init__.py`

**Policy**: Adopters MUST upgrade (correctness issue)

**Support Provided**:
- Clear identification in CHANGELOG as "CRITICAL" or "Fixed"
- Merge strategies for preserving customizations
- Step-by-step conflict resolution guides

**Decision Criteria for Agents**:
```
IF release contains CRITICAL fixes
  THEN: Upgrade required
  PRESERVE: Local customizations via documented merge strategy
  VALIDATE: All tests pass after merge
```

#### Type 2: Workflow Improvements (Optional Displacement)
**Example**: v1.4.0 making `just --list` the primary task discovery interface

**Policy**: Adopters MAY upgrade (DX improvement, not correctness)

**Support Provided**:
- Benefits analysis (why new approach is better)
- Cost analysis (what you have to change)
- Decision criteria (when to adopt vs keep existing)
- Hybrid strategies (adopt partially)

**Decision Criteria for Agents**:
```
IF working across multiple chora-base projects
  THEN: Adopt (ecosystem consistency benefit)
ELSE IF existing workflow is well-established
  THEN: Evaluate benefits vs costs
  CONSIDER: Hybrid approach (new tasks use new pattern, existing tasks preserved)
```

#### Type 3: Documentation/Structure Changes (Safe Displacement)
**Example**: v1.3.0 adding `dev-docs/vision/` directory

**Policy**: Adopters choose what to adopt (pure addition)

**Support Provided**:
- Integration guides (how to merge with existing docs)
- Conditional adoption (template variables control inclusion)
- Conflict resolution (if existing docs overlap)

**Decision Criteria for Agents**:
```
IF project has no existing [roadmap/vision/planning] docs
  THEN: Safe to adopt template structure
ELSE IF existing docs serve similar purpose
  THEN: Evaluate integration vs separation
  OPTIONS:
    1. Keep existing (skip template version)
    2. Migrate existing to template structure
    3. Hybrid (link existing docs from template structure)
```

### Displacement Transparency

**Every release CHANGELOG includes**:
- **Added**: New features/files (potential displacement)
- **Changed**: Modified templates (merge required)
- **Fixed**: Bug fixes (required upgrades)
- **Impact on Existing Adopters**: Explicit statement of displacement

**Every upgrade guide includes**:
- **Displacement Risk**: HIGH/MEDIUM/LOW
- **Required vs Optional**: Clear distinction
- **Preservation Strategy**: How to keep existing customizations

---

## Customization Preservation

### Principle

**Template updates MUST NOT destroy local customizations.** Upgrading should be a merge, not a replacement.

### Customization Types

#### 1. Script Customizations
**Example**: Modified `scripts/diagnose.sh` to check project-specific dependencies

**Preservation Strategy**:
1. Review template changes: `git diff v1.X..v1.Y template/scripts/diagnose.sh.jinja`
2. Identify template improvements vs local customizations
3. Merge: Apply template improvements, preserve local logic
4. Validate: Run script before/after to ensure functionality

**Tools**:
- Upgrade guides show diffs of template changes
- Merge strategies documented per-file
- Validation checklists ensure nothing breaks

#### 2. Documentation Customizations
**Example**: Enhanced `AGENTS.md` with project-specific task examples

**Preservation Strategy**:
1. Template sections are clearly marked (e.g., `## Common Tasks for Agents`)
2. Local additions go in separate sections or subsections
3. Template updates merge into template sections only
4. Local sections remain untouched

**Best Practice**:
```markdown
<!-- BEGIN TEMPLATE SECTION -->
## Common Tasks for Agents
[template content here]
<!-- END TEMPLATE SECTION -->

<!-- LOCAL CUSTOMIZATIONS -->
## Project-Specific Agent Workflows
[your custom content here - safe from template updates]
```

#### 3. Configuration Customizations
**Example**: Added new copier variables for project-specific needs

**Preservation Strategy**:
- Template adds variables but doesn't remove existing ones
- Local `.copier-answers.yml` additions are preserved
- Upgrade prompts only for NEW variables (existing answers kept)

**Validation**:
```bash
# Before upgrade
cp .copier-answers.yml .copier-answers.yml.backup

# After upgrade
diff .copier-answers.yml.backup .copier-answers.yml
# Only new variables should appear
```

### Merge Conflict Resolution

**When copier update creates conflicts:**

1. **Understand the conflict**:
   - What did template change?
   - What did you customize locally?
   - Why did each change happen?

2. **Choose merge strategy**:
   - **Accept template**: If template fix is critical and you can re-apply customization
   - **Keep local**: If customization is essential and template change is optional
   - **Merge both**: Combine template improvement with local customization (preferred)

3. **Document decision**:
   ```markdown
   # In project's UPGRADING.md or git commit message
   Merge conflict in scripts/diagnose.sh:
   - Template added: Python version check
   - Local customization: ANTHROPIC_API_KEY validation
   - Resolution: Merged both (added version check, kept API key validation)
   ```

4. **Validate**:
   - Run affected scripts/tests
   - Check that both template improvement AND customization work

---

## Decision Framework for AI Agents

### When to Upgrade

**Adopt upgrade IF:**
- [ ] Release contains CRITICAL fixes affecting project
- [ ] New features align with project needs
- [ ] Benefits outweigh cost of workflow changes
- [ ] No major customization conflicts

**Defer upgrade IF:**
- [ ] Project is stable and working
- [ ] Team is in critical sprint (no time for integration)
- [ ] Customizations are extensive and would require significant merge effort
- [ ] Waiting for cumulative guide (e.g., skip v1.1, v1.2, upgrade directly to v1.3)

**Skip upgrade IF:**
- [ ] Release changes are purely cosmetic (docs formatting, etc.)
- [ ] Features are not relevant to project type
- [ ] Existing alternative is equally good or better

### Workflow Replacement Decisions

**Example: v1.4.0 `just --list` as Primary Task Discovery**

#### Step 1: Evaluate Benefits
```
New approach (`just --list`):
+ Machine-readable task catalog (better for agents)
+ Ecosystem consistency (knowledge transfers across chora-base projects)
+ Self-documenting (no prose parsing needed)
+ Composable (just --show reveals implementation)

Current approach (parsing docs/reading scripts):
+ No dependencies (works without just)
+ Fully understood by agent
- Project-specific (doesn't transfer to other projects)
- Requires prose parsing or script directory inspection
```

#### Step 2: Evaluate Costs
```
To adopt `just --list`:
- Must install just (setup.sh does this automatically in v1.4.0)
- Must learn justfile syntax for future task additions
- Must update stored task knowledge (map old patterns to just commands)
- Documentation now assumes just (fallback to scripts shown but secondary)

To keep existing approach:
- No installation needed
- Agent keeps current task knowledge
- May miss benefits of ecosystem consistency
```

#### Step 3: Apply Decision Criteria

**For Multi-Project AI Agents** (working across chora-base ecosystem):
```
Recommendation: ADOPT

Reasoning:
- Knowledge learned in one chora-base project transfers to all others
- `just --list` is now standard across ecosystem (v1.4.0+)
- Investment in learning `just` pays off across projects
- Machine-readable catalog is superior for agent task discovery

Migration:
1. Map existing task knowledge to `just` commands
   OLD: "Run tests with ./scripts/smoke-test.sh"
   NEW: "Run tests with `just test` (smoke) or `just test-all` (full suite)"
2. Store as ecosystem-level pattern (not project-specific)
3. Create knowledge note documenting the migration
```

**For Single-Project AI Agents**:
```
Recommendation: EVALUATE CASE-BY-CASE

Criteria:
IF agent has extensive task knowledge already stored
  AND project is stable/mature
  AND no need for consistency with other chora-base projects
  THEN: Defer adoption (existing approach works fine)

IF project is new OR agent is learning tasks
  AND `just` installation is acceptable
  THEN: Adopt (start with ecosystem standard)

IF hybrid makes sense (some tasks via just, some via scripts)
  THEN: Adopt selectively (use just for new tasks, keep scripts for existing)
```

#### Step 4: Store Decision as Knowledge

**If adopting**:
```json
{
  "id": "chora-base-task-discovery-migration",
  "created": "2025-10-19",
  "tags": ["chora-base", "workflow", "task-discovery", "ecosystem-pattern"],
  "ecosystem": "chora-base",
  "pattern": {
    "discovery": "just --list",
    "execution": "just <task-name>",
    "inspection": "just --show <task-name>",
    "applies_to": "all chora-base v1.4.0+ projects"
  },
  "migration": {
    "from": "project-specific script knowledge",
    "to": "ecosystem-wide just commands",
    "benefit": "knowledge transfers across all chora-base projects"
  }
}
```

**If deferring**:
```json
{
  "id": "chora-base-v1.4.0-upgrade-deferred",
  "created": "2025-10-19",
  "tags": ["chora-base", "upgrade-decision"],
  "decision": "defer",
  "reasoning": "Existing task knowledge is extensive, project is stable, no multi-project benefit",
  "revisit": "when starting new chora-base project"
}
```

---

## Upgrade Strategy Patterns

### Pattern 1: Incremental (Version-by-Version)

**Use When**:
- You want to understand each change
- Project has extensive customizations
- You have time for careful review

**Approach**:
```bash
# v1.0.0 → v1.1.0
copier update --vcs-ref v1.1.0
# Review, test, commit

# v1.1.0 → v1.2.0
copier update --vcs-ref v1.2.0
# Review, test, commit

# etc.
```

**Benefits**:
- Small diffs (easier to review)
- Clear understanding of each change
- Easier conflict resolution

**Costs**:
- More time (multiple upgrade sessions)
- More commits (one per version)

### Pattern 2: Cumulative (Multi-Version Jump)

**Use When**:
- You're multiple versions behind
- Changes are mostly additive (low conflict risk)
- You want to batch the upgrade work

**Approach**:
```bash
# v1.0.0 → v1.4.0 directly
copier update --vcs-ref v1.4.0
# Review cumulative changes, resolve conflicts, commit
```

**Benefits**:
- Fewer upgrade sessions
- One comprehensive review
- Single commit captures full upgrade

**Costs**:
- Larger diffs (harder to review)
- More merge conflicts (multiple changes per file)
- Requires cumulative upgrade guide (not just version-to-version)

**Requires**:
- Cumulative upgrade guide (e.g., `project-docs/releases/CUMULATIVE_v1.0-to-v1.4.md`)
- Good test coverage (validate everything works after upgrade)

### Pattern 3: Selective (Cherry-Pick Features)

**Use When**:
- You only want specific features from new versions
- Template changes conflict with local customizations
- You want to adopt ecosystem patterns without full template update

**Approach**:
```bash
# Don't run copier update
# Instead, manually copy specific improvements

# Example: Adopt v1.4.0's just --list pattern without full upgrade
# 1. Review template changes:
git diff v1.3.0..v1.4.0 template/AGENTS.md.jinja
# 2. Copy "Task Discovery" section to local AGENTS.md
# 3. Update justfile to match template conventions
# 4. Update setup.sh to install just
# 5. Document in UPGRADING.md: "Adopted just pattern from v1.4.0 without full upgrade"
```

**Benefits**:
- Maximum control
- No unwanted changes
- Preserve customizations

**Costs**:
- Manual work (no automated merge)
- Must track which template features you've adopted
- May miss interdependencies between features

---

## Breaking Changes Policy

### Current Status

**v1.0.0 → v1.4.0**: Zero breaking changes

**All changes have been**:
- Additive (new features/files)
- Fixes (corrections to template bugs)
- Improvements (better patterns for existing features)

### When Breaking Changes May Occur

**MAJOR version bump (v2.0.0)** might include:
- Renamed copier variables (old names deprecated)
- Removed deprecated features
- Changed project structure (e.g., src/ layout changes)
- Python version requirement increase (e.g., 3.11 → 3.13)

**Commitment**:
- Breaking changes only in MAJOR versions
- At least 2 MINOR versions of deprecation warnings before removal
- Migration guides for all breaking changes
- Upgrade validation scripts to catch breaking changes

**Example** (hypothetical future):
```
v1.5.0: Deprecate `include_cli` variable, add deprecation warning
v1.6.0: Deprecation warning continues, new `cli_framework` variable added
v2.0.0: Remove `include_cli`, use `cli_framework` exclusively
         Migration guide: include_cli=true → cli_framework="click"
```

### Breaking Change Communication

**In CHANGELOG**:
```markdown
## [2.0.0] - Future

### BREAKING CHANGES
- **Removed**: `include_cli` copier variable
  - **Migration**: Set `cli_framework="click"` instead
  - **Guide**: project-docs/releases/v1.6-to-v2.0.md
```

**In Upgrade Guides**:
- Automated validation scripts detect breaking changes
- Step-by-step migration instructions
- Before/after examples
- Rollback procedures if migration fails

---

## Summary for AI Agents

**Key Takeaways**:

1. **Upgrades are safe**: Semantic versioning + preservation strategies protect customizations
2. **Displacement is transparent**: Every release documents impact on existing adopters
3. **Decisions are supported**: Clear criteria for adopt/defer/skip
4. **Ecosystem benefits are real**: Consistent patterns (like `just --list`) improve cross-project work
5. **You control the pace**: Incremental, cumulative, or selective upgrade strategies available

**When in doubt**:
1. Read version-specific upgrade guide: `project-docs/releases/vX.Y-to-vX.Z.md`
2. Check displacement risk: HIGH/MEDIUM/LOW
3. Apply decision framework: Required vs optional
4. Preserve customizations: Use documented merge strategies
5. Validate thoroughly: Tests must pass before/after

**Remember**: chora-base evolves based on real-world adoption. Your feedback on upgrade friction helps improve this process for all adopters.

---

**Next**: See [version-specific upgrade guides](.) for step-by-step instructions.
