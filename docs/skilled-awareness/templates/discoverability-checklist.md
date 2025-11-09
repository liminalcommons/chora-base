# SAP Discoverability Checklist

**SAP ID**: SAP-XXX
**SAP Name**: [sap-name]
**Completed by**: __________
**Date**: __________

---

## Purpose

Use this checklist to ensure your SAP meets L1 discoverability requirements (≥80/100 score).

**Why This Matters**: Implementation quality is irrelevant if agents cannot discover the capability exists. This checklist ensures SAPs are discoverable via root awareness files, enabling natural adoption from day 1.

**Target**: ≥80/100 discoverability score (required for L1 completion)
**Time Investment**: 3-5 hours (one-time)
**ROI**: 10-15 min saved per session per agent (break-even: 20-30 sessions)

---

## Touchpoint 1: README.md Section (30 points)

**Requirement**: Add dedicated section to project README.md (≥30 lines minimum)

### Checklist

- [ ] Section added: `### SAP-XXX: [Name]` or `### [SAP Name]`
- [ ] "When to use SAP-XXX" subsection (5 use cases)
- [ ] "What you get" subsection (detailed features)
- [ ] Quick-start code example (5-10 commands)
- [ ] Links to nested files (if SAP-009 pattern used)
- [ ] ROI statement (time/value saved, quantified)
- [ ] Documentation links (how-to, explanation, reference)
- [ ] All code examples tested and working
- [ ] No placeholder text (e.g., "TODO", "[TBD]")
- [ ] **Line count**: _____ lines (target: ≥30 lines)

### Template

```markdown
### [SAP Name]

**When to use SAP-XXX**:
- [Use case 1 with context]
- [Use case 2 with context]
- [Use case 3 with context]
- [Use case 4 with context]
- [Use case 5 with context]

**What you get**:
- [Feature 1 with details]
- [Feature 2 with details]
- [Feature 3 with details]

**Quick start**:
\```bash
# [Command 1 with comment]
just command-1

# [Command 2 with comment]
just command-2

# [Command 3 with comment]
just command-3
\```

**Documentation**: [Link to how-to guides or nested AGENTS.md]

**ROI**: [Time saved or value delivered per session, e.g., "10-15 min saved per session via context restoration"]
```

### Validation

```bash
# Check section exists and meets length requirement
grep -A 40 "### SAP-XXX\|### [SAP Name]" README.md | wc -l
# Target: ≥30 lines

# If result ≥30: ✅ Full credit (30/30 points)
# If result 10-29: ⚠️ Partial credit (15/30 points)
# If result 1-9: ⚠️ Minimal credit (5/30 points)
# If result 0: ❌ No credit (0/30 points)
```

**Estimated Score**: _____ / 30

---

## Touchpoint 2: AGENTS.md Section (20 points)

**Requirement**: Add dedicated section to project AGENTS.md (≥60 lines minimum)

### Checklist

- [ ] Section added: `### [SAP Name] (SAP-XXX)`
- [ ] "When to use SAP-XXX" subsection (5+ scenarios with context)
- [ ] "Quick-start approach" subsection with commands
- [ ] "What you get" subsection (detailed capabilities)
- [ ] Example workflow (complete scenario from start to finish)
- [ ] Integration patterns with other SAPs (list ≥2 related SAPs)
- [ ] Links to nested AGENTS.md (if applicable, e.g., `.chora/AGENTS.md`)
- [ ] ROI statement (quantified value)
- [ ] All code examples tested and working
- [ ] No placeholder text
- [ ] **Line count**: _____ lines (target: ≥60 lines)

### Template

```markdown
### [SAP Name] (SAP-XXX)

**When to use SAP-XXX**:
- [Scenario 1 with context - be specific]
- [Scenario 2 with context]
- [Scenario 3 with context]
- [Scenario 4 with context]
- [Scenario 5 with context]

**Quick-start approach** (recommended):
\```bash
# [Step 1 with explanation]
just step-1

# [Step 2 with explanation]
just step-2

# [Step 3 with explanation]
just step-3
\```

**What you get**:
- **[Feature 1 category]**: [Detailed explanation with specifics]
- **[Feature 2 category]**: [Detailed explanation with specifics]
- **[Feature 3 category]**: [Detailed explanation with specifics]

**Example workflow**:
\```bash
# Scenario: [Complete use case description - be concrete]

# 1. [Step description with rationale]
just command-1

# 2. [Step description with rationale]
just command-2

# 3. [Step description with rationale]
just command-3

# Result: [Expected outcome - what changed?]
\```

**Integration with other SAPs**:
- **SAP-XXX ([name])**: [How they integrate - specific pattern]
- **SAP-YYY ([name])**: [How they integrate - specific pattern]

**Documentation**: [Links to detailed docs, nested files]

**ROI**: [Time/value saved per session, quantified]
```

### Validation

```bash
# Check section exists and meets length requirement
grep -A 70 "### SAP-XXX\|### [SAP Name]" AGENTS.md | wc -l
# Target: ≥60 lines

# If result ≥60: ✅ Full credit (20/20 points)
# If result 30-59: ⚠️ Partial credit (10/20 points)
# If result 1-29: ⚠️ Minimal credit (5/20 points - catalog entry only)
# If result 0: ❌ No credit (0/20 points)
```

**Estimated Score**: _____ / 20

---

## Touchpoint 3: CLAUDE.md Coverage (15 points)

**Requirement**: Add dedicated section OR ensure domain section has direct links (if using SAP-009 nested hierarchy)

### Checklist

**Option A: Dedicated Section** (if SAP has Claude-specific patterns):
- [ ] Section added with Claude-specific workflows
- [ ] Token budget guidance (Phase 1/2/3 estimates)
- [ ] Claude-specific tips (≥2 tips for Claude Code or Claude Desktop)
- [ ] Example workflow with tool usage

**Option B: Domain Section with Direct Links** (if using nested hierarchy):
- [ ] Domain section updated in root CLAUDE.md
- [ ] Direct links to nested CLAUDE.md file
- [ ] "Navigation tip" with token savings statement
- [ ] Read time estimates and token counts
- [ ] "Use when" scenarios (≥2)

### Template (Option A: Dedicated Section)

```markdown
### [SAP Name] Claude Workflows

**Token budget guidance**:
- Phase 1 (orientation): [X]k tokens
- Phase 2 (implementation): [Y]k tokens

**Claude-specific tips**:
- [Tip 1 for Claude Code or Claude Desktop - be specific]
- [Tip 2 for Claude Code or Claude Desktop - be specific]

**Example workflow**:
\```markdown
User: "[Common user request]"

Claude:
1. [Step 1 with tool usage, e.g., "Read protocol-spec.md"]
2. [Step 2 with tool usage, e.g., "Edit config file"]
3. [Step 3 with tool usage, e.g., "Bash validation command"]
\```
```

### Template (Option B: Domain Section)

```markdown
### Domain X: [Domain Name] (path/)

**Path**: [path/AGENTS.md](path/AGENTS.md) + [path/CLAUDE.md](path/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [path/CLAUDE.md](path/CLAUDE.md) - Claude workflows (X-min, Yk tokens)
- [path/AGENTS.md](path/AGENTS.md) - [Domain] patterns (X-min, Yk tokens)

**Use when**:
- [Scenario 1 - working in this domain]
- [Scenario 2 - need domain-specific guidance]
```

### Validation

```bash
# Check CLAUDE.md mentions SAP
grep -i "SAP-XXX\|[sap-name]" CLAUDE.md && echo "✅ Mentioned" || echo "❌ Not found"

# If dedicated section exists: ✅ Full credit (15/15 points)
# If mentioned in context: ⚠️ Partial credit (7/15 points)
# If not mentioned: ❌ No credit (0/15 points)
```

**Estimated Score**: _____ / 15

---

## Touchpoint 4: justfile Recipes (15 points)

**Requirement**: Add ≥3 recipes with section header, comments, and examples

### Checklist

- [ ] Section header added (e.g., `# === SAP-XXX: [Name] ===`)
- [ ] Section comment explaining SAP purpose (1-2 sentences)
- [ ] Recipe 1: _____________________ (with inline comment & example)
- [ ] Recipe 2: _____________________ (with inline comment & example)
- [ ] Recipe 3: _____________________ (with inline comment & example)
- [ ] All recipes tested and working
- [ ] Default values for arguments (where appropriate)
- [ ] Usage examples for complex recipes (# Example: just ...)

### Template

```bash
# ============================================================================
# SAP-XXX: [SAP Name]
# ============================================================================
# [Brief description of SAP purpose, 1-2 sentences]
# See: [Link to AGENTS.md or nested files]

# [Recipe 1 description with details - what it does and why]
# Example: just recipe-1 arg-value
recipe-1 ARG="default":
    @command {{ARG}}

# [Recipe 2 description with details]
# Example: just recipe-2 arg-value
recipe-2 ARG="default":
    @command {{ARG}}

# [Recipe 3 description with details]
# Example: just recipe-3
recipe-3:
    @command
```

### Validation

```bash
# Check recipes exist
grep -A 20 "SAP-XXX\|[SAP Name]" justfile | grep "^[a-z]" | wc -l
# Target: ≥3 recipes

# If result ≥3: ✅ Full credit (15/15 points)
# If result 1-2 (with comments): ⚠️ Partial credit (10/15 points)
# If result 1-2 (no comments): ⚠️ Minimal credit (5/15 points)
# If result 0: ❌ No credit (0/15 points)
```

**Estimated Score**: _____ / 15

---

## Touchpoint 5: Documentation (10 points)

**Requirement**: Create ≥1 how-to guide, organize per SAP-007 structure (if applicable)

### Checklist

- [ ] How-to guide created: _____________________ (file path)
- [ ] Explanation doc created (optional): _____________________
- [ ] Reference doc created (optional): _____________________
- [ ] Docs organized in SAP-007 structure (docs/how-to/, docs/explanation/, docs/reference/)
- [ ] All docs linked from README.md

### Template (How-to Guide)

```markdown
# How to Use [SAP Name]

**Audience**: Developers and AI agents
**Time**: [X] minutes
**Prerequisites**: [List prerequisites, if any]

---

## Quick Start

1. [Step 1 with command]
2. [Step 2 with command]
3. [Step 3 with command]
4. [Step 4 with command]
5. [Step 5 with command]

---

## Common Tasks

### Task 1: [Name]

\```bash
# [Commands with explanations]
just command-1
just command-2
\```

### Task 2: [Name]

\```bash
# [Commands with explanations]
just command-3
just command-4
\```

---

## Troubleshooting

**Problem**: [Common issue description]
**Solution**: [Fix with commands or explanation]

**Problem**: [Another common issue]
**Solution**: [Fix]
```

### Validation

```bash
# Check documentation files exist
ls docs/how-to/*[sap-name]* docs/explanation/*[sap-name]* docs/reference/*[sap-name]* 2>/dev/null | wc -l
# Target: ≥1 file (≥3 for full credit)

# If result ≥3: ✅ Full credit (10/10 points)
# If result 1-2: ⚠️ Partial credit (5/10 points)
# If result 0: ❌ No credit (0/10 points)
```

**Estimated Score**: _____ / 10

---

## Touchpoint 6: Examples (10 points)

**Requirement**: Provide ≥5 working implementations or code samples

### Checklist

- [ ] Example 1: _____________________ (description & location)
- [ ] Example 2: _____________________
- [ ] Example 3: _____________________
- [ ] Example 4: _____________________
- [ ] Example 5: _____________________
- [ ] All examples tested and working
- [ ] Examples reference SAP-XXX or [sap-name]

### Validation

```bash
# Check examples exist
grep -r "SAP-XXX\|[sap-name]" examples/ tests/ 2>/dev/null | wc -l
# Target: ≥5 occurrences

# If result ≥5: ✅ Full credit (10/10 points)
# If result 1-4: ⚠️ Partial credit (5/10 points)
# If result 0: ❌ No credit (0/10 points)
```

**Estimated Score**: _____ / 10

---

## Special: Direct Links (Required if using SAP-009 nested hierarchy)

**Requirement**: If SAP uses nested AGENTS.md/CLAUDE.md files, add direct links in root files

### Checklist

- [ ] Root CLAUDE.md domain section updated
- [ ] "Navigation tip" added with token savings statement
- [ ] Direct link to domain CLAUDE.md
- [ ] Direct link to domain AGENTS.md
- [ ] Read time estimates provided (e.g., "8-min, 5k tokens")
- [ ] Token counts provided (e.g., "5k tokens")
- [ ] Root AGENTS.md references nested AGENTS.md

### Template (Root CLAUDE.md)

```markdown
### Domain X: [Domain Name] (path/)

**Path**: [path/AGENTS.md](path/AGENTS.md) + [path/CLAUDE.md](path/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [path/CLAUDE.md](path/CLAUDE.md) - Claude workflows (X-min, Yk tokens)
- [path/AGENTS.md](path/AGENTS.md) - [Domain] patterns (X-min, Yk tokens)

**Use when**:
- [Working in path/ directory]
- [Need domain-specific guidance]
```

### Validation

```bash
# Check links exist and are clickable
grep -o "\[.*AGENTS.md\](.*AGENTS.md)" CLAUDE.md && echo "✅ Direct links exist" || echo "❌ Missing"
```

**Status**: [ ] N/A (not using nested hierarchy) | [ ] Complete | [ ] Incomplete

---

## Quality Validation

### Quality Checklist

- [ ] All code examples tested and working
- [ ] All links are clickable and resolve correctly
- [ ] No placeholder text (e.g., "TODO", "[TBD]", "XXXX")
- [ ] Concrete examples provided (not abstract descriptions)
- [ ] ROI statement included with quantified value (e.g., "10 min saved per session")
- [ ] All validation commands run successfully

### Discovery Test

**Manual Test** (have another agent or developer try):
- [ ] Agent can find SAP by reading README.md alone (<2 min)
- [ ] Agent can find SAP by reading AGENTS.md alone (<2 min)
- [ ] Agent can discover recipes via `just --list` (<1 min)
- [ ] Navigation time from root to SAP docs <5 min total

---

## Final Score Calculation

| Touchpoint | Points Possible | Your Score | Notes |
|-----------|----------------|------------|-------|
| README.md | 30 | _____ | (≥30 lines) |
| AGENTS.md | 20 | _____ | (≥60 lines) |
| CLAUDE.md | 15 | _____ | (dedicated section OR domain links) |
| justfile | 15 | _____ | (≥3 recipes with comments) |
| Documentation | 10 | _____ | (≥1 how-to guide) |
| Examples | 10 | _____ | (≥5 occurrences) |
| **Total** | **100** | **_____** | |

---

## Score Interpretation

**Your Score**: _____ / 100

- **80-100 (HIGH)**: ✅ Excellent discoverability - Ready for L1 completion
  - Agents can find SAP easily (<5 min discovery time)
  - All touchpoints complete or near-complete
  - Natural adoption expected

- **50-79 (MEDIUM)**: ⚠️ Adequate, but gaps exist - L1 blocked until improved
  - Some touchpoints missing or below threshold
  - Discovery time: 5-15 minutes
  - Improvement needed before L1 completion

- **0-49 (LOW)**: ❌ Critical gap - Significant work needed
  - Major touchpoints missing
  - Discovery time: >15 minutes or never discovered
  - Cannot mark L1 complete

**L1 Requirement**: ≥80/100

---

## Improvement Plan (if score <80)

**Missing Touchpoints** (0 points):
- [ ] _____________________
- [ ] _____________________
- [ ] _____________________

**Below Threshold** (partial points):
- [ ] _____________________ (current: _____/_____)
- [ ] _____________________ (current: _____/_____)
- [ ] _____________________ (current: _____/_____)

**Estimated Effort to Reach ≥80**:
- Missing README section: 1-2 hours
- Missing AGENTS section: 2-3 hours
- Missing justfile recipes: 2-3 hours
- Below threshold adjustments: 0.5-1 hour each
- **Total Estimated**: _____ hours

**Priority Actions** (focus on highest-impact touchpoints first):
1. [ ] _____________________
2. [ ] _____________________
3. [ ] _____________________

---

## Automated Validation

**Run discoverability audit** (if available):

```bash
# Audit SAP discoverability
python scripts/sap-evaluator.py --disc SAP-XXX

# Or manual validation
echo "README.md: $(grep -A 40 '### SAP-XXX' README.md | wc -l) lines (target: ≥30)"
echo "AGENTS.md: $(grep -A 70 '### SAP-XXX' AGENTS.md | wc -l) lines (target: ≥60)"
echo "justfile recipes: $(grep -A 20 'SAP-XXX' justfile | grep '^[a-z]' | wc -l) (target: ≥3)"
echo "How-to guide: $(ls docs/how-to/*[sap-name]* 2>/dev/null | wc -l) (target: ≥1)"
```

---

## Approval

- [ ] **Discoverability score ≥80/100**
- [ ] **All validation commands pass**
- [ ] **Quality checklist complete**
- [ ] **Discovery test passed**
- [ ] **Ready for L1 completion**

**Approved by**: __________
**Date**: __________

---

## Notes & Observations

[Add any observations, challenges, or learnings from completing this checklist]

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-09
**Related**: [SAP-000 adoption-blueprint.md](../sap-framework/adoption-blueprint.md#5-l1-requirement-discoverability)
