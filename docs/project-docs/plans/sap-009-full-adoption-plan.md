# SAP-009 Full Adoption + Strategic SAP Enhancement Plan

**Plan ID**: PLAN-2025-11-04-SAP-009-FULL
**Created**: 2025-11-04
**Owner**: Victor Piper
**Status**: Proposed
**Total Effort**: 40-56 hours (core), 59-83 hours (with optional)

---

## Executive Summary

This plan achieves **full SAP-009 (Agent Awareness) adoption** in chora-base by creating 34-39 nested awareness files (AGENTS.md + CLAUDE.md) across all domains and capabilities, plus **strategic enhancements to 10 high-value SAPs** to refine their artifacts during the awareness file creation process.

### Key Outcomes

1. **Complete SAP-009 dogfooding**: Chora-base will use the nested awareness pattern it provides to others
2. **Enhanced agent discoverability**: Agents can progressively load context from root → domain → SAP → feature → component
3. **Refined SAP artifacts**: 10 SAPs will receive improved awareness guides, ledgers, and CLAUDE.md files
4. **Ecosystem readiness**: All SAPs will have complete awareness documentation for downstream adopters

### Success Metrics

- ✅ 34-39 awareness files created and committed
- ✅ 10 SAPs enhanced with refined artifacts
- ✅ Agent context loading time reduced by 30%+
- ✅ Zero broken links in awareness file network
- ✅ All SAPs have both AGENTS.md and CLAUDE.md

---

## Phase 1: Foundation (Root + Domain Awareness) — 7-10 hours

### Deliverables

1. **Root CLAUDE.md** (1 file) — 2-3 hours
   - Location: `/CLAUDE.md`
   - Content:
     - Project philosophy and architecture overview
     - How to navigate chora-base as an agent
     - Link tree to domain awareness files
     - Progressive context loading guidance
     - Integration with Claude Code, Claude Desktop, other agents
   - Example structure:
     ```markdown
     # Chora-Base: Agent Awareness (Root)

     ## Quick Start for Agents
     - New to chora-base? Start here: [Project Bootstrap](docs/project-docs/...)
     - Looking for user docs? Navigate: [User Documentation](docs/user-docs/AGENTS.md)
     - Need dev setup? Go to: [Developer Documentation](docs/dev-docs/AGENTS.md)

     ## Architecture Overview
     - SAP framework: Skilled Awareness Packages
     - Nested awareness pattern (SAP-009)
     - Progressive context loading (0-10k → 10-50k → 50-200k tokens)

     ## Context Loading Strategy
     1. Phase 1 (0-10k): Root awareness + target domain
     2. Phase 2 (10-50k): Domain + specific SAP
     3. Phase 3 (50-200k): SAP + feature + component details
     ```

2. **Domain-Level AGENTS.md Files** (4 files) — 3-4 hours total
   - `/docs/user-docs/AGENTS.md` (1h)
     - Overview of user-facing documentation
     - Getting started guides, tutorials, references
     - Link map to user guides
   - `/docs/dev-docs/AGENTS.md` (1h)
     - Developer setup, architecture, contributing
     - Link map to technical documentation
   - `/docs/project-docs/AGENTS.md` (1h)
     - Project management, governance, decisions
     - Link map to project plans, RFCs, retrospectives
   - `/docs/skilled-awareness/AGENTS.md` (1h)
     - SAP registry overview
     - How to navigate SAP documentation
     - Link map to all 30+ SAPs

3. **Domain-Level CLAUDE.md Files** (4 files) — 2-3 hours total
   - `/docs/user-docs/CLAUDE.md` (30-45min)
     - Claude-specific tips for understanding user documentation
     - How Claude Code vs Claude Desktop should use these docs
   - `/docs/dev-docs/CLAUDE.md` (30-45min)
     - Claude-specific development workflows
     - Integration with Claude Code IDE features
   - `/docs/project-docs/CLAUDE.md` (30-45min)
     - Claude-specific project navigation patterns
     - How to read plans, decisions, retrospectives
   - `/docs/skilled-awareness/CLAUDE.md` (30-45min)
     - Claude-specific SAP navigation
     - How to progressively load SAP context

### Success Criteria

- [ ] All 9 files created and committed
- [ ] Root CLAUDE.md has complete link tree
- [ ] All domain files cross-reference appropriately
- [ ] No broken links in awareness network
- [ ] Validated by agent reading test (Claude Code session)

---

## Phase 2: P0 SAP Enhancements (Critical SAPs) — 8-11 hours

### SAP-027: Dogfooding Patterns — 3-4 hours ⭐ **HIGHEST PRIORITY**

**Why Critical**: This SAP defines how to dogfood SAPs, yet lacks complete awareness

**Deliverables**:
1. `/docs/skilled-awareness/dogfooding-patterns/AGENTS.md` (1-1.5h)
   - Generic agent patterns for dogfooding
   - How to validate SAP adoption
   - Metrics collection workflows
2. `/docs/skilled-awareness/dogfooding-patterns/CLAUDE.md` (1-1.5h)
   - Claude-specific dogfooding workflows
   - Integration with Claude Code for validation
3. Ledger TODOs completed (30-60min)
   - Fill in adoption metrics
   - Document pilot feedback
   - Update version history

**Impact**: Enables systematic validation of all SAPs, critical for ecosystem trust

---

### SAP-029: SAP Generation — 3-4 hours

**Why Critical**: Generates new SAPs but lacks complete awareness for agents to use it

**Deliverables**:
1. `/docs/skilled-awareness/sap-generation/AGENTS.md` (1-1.5h)
   - Generic patterns for generating SAPs
   - Template selection guidance
   - Validation workflows
2. `/docs/skilled-awareness/sap-generation/CLAUDE.md` (1-1.5h)
   - Claude-specific generation patterns
   - How Claude Code should use templates
   - Interactive generation workflows
3. Ledger TODOs completed (30-60min)
   - Document SAP-015 generation experience
   - Update adoption metrics

**Impact**: Accelerates SAP ecosystem growth, reduces friction for new capabilities

---

### SAP-028: Publishing Automation — 2-3 hours

**Why Critical**: Automates SAP distribution but lacks awareness for adoption

**Deliverables**:
1. `/docs/skilled-awareness/publishing-automation/AGENTS.md` (45-60min)
   - Publishing workflows for agents
   - How to trigger releases
2. `/docs/skilled-awareness/publishing-automation/CLAUDE.md` (45-60min)
   - Claude-specific publishing patterns
3. Ledger baseline (30-60min)
   - Initial adoption entry
   - Metrics framework

**Impact**: Enables automated SAP distribution, critical for ecosystem scalability

---

## Phase 3: P1 SAP Enhancements (High-Value SAPs) — 9-12 hours

### SAP-015: Task Tracking (Beads) — 2-3 hours

**Why Important**: Newly created SAP-015 lacks CLAUDE.md and integration examples

**Deliverables**:
1. `/docs/skilled-awareness/task-tracking/CLAUDE.md` (1-1.5h)
   - Claude Code-specific beads workflows
   - How Claude should use beads CLI
   - Integration with Claude Code task management
2. Enhanced integration examples (30-60min)
   - Concrete inbox → beads decomposition examples
   - A-MEM → beads correlation examples with real traces
3. Ledger updates (30min)
   - Document first month of dogfooding feedback

**Impact**: Improves agent adoption of beads, validates pilot phase

---

### SAP-003: Project Bootstrap — 3-4 hours

**Why Important**: Critical first-contact SAP but only at `draft` status

**Deliverables**:
1. `/docs/skilled-awareness/project-bootstrap/AGENTS.md` (1-1.5h)
   - Comprehensive bootstrap workflows
   - Template selection guidance
   - Post-bootstrap validation patterns
2. `/docs/skilled-awareness/project-bootstrap/CLAUDE.md` (1-1.5h)
   - Claude-specific bootstrap patterns
   - Interactive setup workflows
3. Ledger expansion (30-60min)
   - Complete adoption history
   - Document all bootstrap cases
4. Status elevation (15min)
   - Update to `pilot` or `production` status
   - Update sap-catalog.json

**Impact**: Improves first-contact experience, critical for ecosystem adoption

---

### SAP-005: CI/CD Workflows — 4-5 hours

**Why Important**: Production SAP but weak awareness and minimal ledger

**Deliverables**:
1. `/docs/skilled-awareness/ci-cd-workflows/AGENTS.md` (1.5-2h)
   - Generic CI/CD patterns for agents
   - How to work with GitHub Actions
   - Quality gate workflows
2. `/docs/skilled-awareness/ci-cd-workflows/CLAUDE.md` (1.5-2h)
   - Claude-specific CI/CD patterns
   - How to debug workflow failures
   - Integration with Claude Code for rapid iteration
3. Ledger expansion (1-1.5h)
   - Document all workflow adoptions
   - Metrics and feedback summary
   - Version history

**Impact**: Improves CI/CD adoption and debugging, high-frequency use case

---

## Phase 4: P1 Infrastructure SAPs — 6-8 hours

### SAP-011: Docker Operations — 4-5 hours

**Why Important**: Production status but zero awareness, minimal ledger

**Deliverables**:
1. `/docs/skilled-awareness/docker-operations/AGENTS.md` (1.5-2h)
   - Docker patterns for agents
   - How to work with docker-compose
   - Troubleshooting workflows
2. `/docs/skilled-awareness/docker-operations/CLAUDE.md` (1.5-2h)
   - Claude-specific docker patterns
   - Integration with Claude Code for rapid iteration
3. Ledger baseline (1-1.5h)
   - Initial adoption entries
   - Metrics framework
   - Feedback collection structure

**Impact**: Enables agent-driven containerization, critical for deployment SAPs

---

### SAP-012: Development Lifecycle — 2-3 hours

**Why Important**: Production SAP but no CLAUDE.md, minimal ledger

**Deliverables**:
1. `/docs/skilled-awareness/development-lifecycle/CLAUDE.md` (1-1.5h)
   - Claude-specific lifecycle patterns
   - Integration with Claude Code workflows
2. Ledger TODOs (1-1.5h)
   - Complete adoption tracking
   - Document version history
   - Feedback summary

**Impact**: Improves agent understanding of development workflows

---

## Phase 5: Remaining SAP Awareness Files — 10-15 hours

### Scope

Create AGENTS.md and/or CLAUDE.md for ~12 SAPs currently lacking awareness files:

| SAP | Priority | Effort | Status |
|-----|----------|--------|--------|
| SAP-004 | P1 | 1-1.5h | Draft, needs awareness |
| SAP-006 | P1 | 1-1.5h | Draft, needs awareness |
| SAP-007 | P1 | 1-1.5h | Pilot, needs awareness |
| SAP-008 | P1 | 1-1.5h | Production, needs awareness |
| SAP-013 | P1 | 1-1.5h | Draft, needs awareness |
| SAP-019 | P1 | 1-1.5h | Production, needs awareness |
| SAP-020 | P1 | 1-1.5h | Pilot, needs awareness |
| SAP-021 | P2 | 45-60min | Draft, needs awareness |
| SAP-022 | P2 | 45-60min | Draft, needs awareness |
| SAP-023 | P2 | 45-60min | Draft, needs awareness |
| SAP-024 | P2 | 45-60min | Draft, needs awareness |
| SAP-025 | P2 | 45-60min | Draft, needs awareness |

### Approach

- **Batch processing**: Group by domain similarity
- **Template reuse**: Use SAP-015 as reference for structure
- **Progressive refinement**: Start with AGENTS.md, add CLAUDE.md if SAP is high-frequency

### Success Criteria

- [ ] All 12 SAPs have at least AGENTS.md
- [ ] High-frequency SAPs (6+) have both AGENTS.md and CLAUDE.md
- [ ] All files integrated into domain-level awareness link maps

---

## Phase 6: Optional (Lower Priority) — 19-27 hours

### SAP-014: MCP Server Development — 5-6 hours (Optional)

**Why Optional**: Important but lower frequency use case

**Deliverables**:
1. `/docs/skilled-awareness/mcp-server-development/AGENTS.md` (2-2.5h)
   - MCP server patterns for agents
   - How to scaffold and test MCP servers
2. `/docs/skilled-awareness/mcp-server-development/CLAUDE.md` (2-2.5h)
   - Claude-specific MCP patterns
   - Integration with Claude Desktop
3. Ledger expansion (1-1.5h)

**Impact**: Enables MCP ecosystem growth, but narrow audience

---

### React SAPs (7 SAPs) — 14-21 hours (Optional)

**Why Optional**: React-specific, only relevant if building React apps

**SAPs**: SAP-016, SAP-017, SAP-018, SAP-026, SAP-030, SAP-031, SAP-032

**Approach**:
- 2-3h per SAP for full awareness (AGENTS.md + CLAUDE.md)
- Batch process for consistency
- Low priority unless React ecosystem adoption increases

---

## Execution Strategy

### Option 1: Sprint-Based (Recommended)

**Sprint 1 (16-21 hours)**: Foundation + P0 SAPs
- Week 1: Phase 1 (7-10h) + Phase 2 (8-11h)
- Deliverable: Root awareness + 3 critical SAPs enhanced
- GO/NO-GO: Validate agent discoverability improvement

**Sprint 2 (15-20 hours)**: P1 SAP Enhancements
- Week 2: Phase 3 (9-12h) + Phase 4 (6-8h)
- Deliverable: 5 high-value SAPs enhanced
- Validate: Agent context loading time reduction

**Sprint 3 (10-15 hours)**: Remaining SAPs
- Week 3: Phase 5 (10-15h)
- Deliverable: All SAPs have awareness files
- Final validation: Complete awareness network

**Total**: 40-56 hours over 3 weeks (13-19h/week)

---

### Option 2: Phased Rollout

**Phase A (7-10 hours)**: Foundation only
- Create root + domain awareness
- Validate pattern before scaling
- GO/NO-GO after 1 week

**Phase B (23-31 hours)**: Strategic SAP enhancements
- Phases 2, 3, 4 combined
- Focus on 8 high-value SAPs
- 2-3 weeks execution

**Phase C (10-15 hours)**: Complete coverage
- Phase 5: Remaining SAPs
- 1-2 weeks execution

**Total**: 40-56 hours over 4-6 weeks

---

### Option 3: Incremental (Domain-by-Domain)

**Domain 1**: `/docs/skilled-awareness/` (30-40h)
- All SAP awareness files
- Highest priority domain

**Domain 2**: `/docs/dev-docs/` (3-5h)
- Developer awareness
- Lower priority

**Domain 3**: `/docs/user-docs/` + `/docs/project-docs/` (4-6h)
- User and project awareness
- Lowest priority

**Total**: 37-51 hours over 5-7 weeks

---

## Risk Mitigation

### Risk 1: Scope Creep

**Mitigation**:
- Strict adherence to 5 artifact pattern (charter, spec, guide, blueprint, ledger)
- No new features during awareness creation
- Park enhancement ideas in inbox for future coordination

### Risk 2: Inconsistent Quality

**Mitigation**:
- Use SAP-015 as quality reference
- Create checklist for awareness file completeness
- Peer review after each phase

### Risk 3: Broken Link Network

**Mitigation**:
- Create automated link checker script
- Run after each awareness file creation
- Fix broken links immediately

### Risk 4: Agent Confusion (Too Much Context)

**Mitigation**:
- Adhere to progressive loading pattern (Phase 1/2/3)
- Test with Claude Code in real sessions
- Gather agent feedback after Phase 1

---

## Success Metrics

### Quantitative

- [ ] **34-39 awareness files created** (100% target)
- [ ] **10 SAPs enhanced** (8/10 minimum, 80% target)
- [ ] **Zero broken links** in awareness network
- [ ] **30% reduction in agent context loading time** (measured via Claude Code sessions)
- [ ] **100% SAP coverage** (all SAPs have at least AGENTS.md)

### Qualitative

- [ ] **Agent discoverability improved**: Agents can navigate from root → SAP in <2 steps
- [ ] **Agent feedback positive**: Claude Code sessions report easier context loading
- [ ] **Ecosystem readiness**: Downstream adopters can easily understand SAPs
- [ ] **Dogfooding validated**: Chora-base uses the pattern it provides

---

## Dependencies

### Hard Dependencies

- [ ] SAP-009 (agent-awareness) at `production` status — **Already met** ✅
- [ ] SAP-000 (sap-framework) at `production` status — **Already met** ✅
- [ ] Git repository initialized — **Already met** ✅

### Soft Dependencies

- [ ] SAP-001 (inbox) useful for coordination tracking — **Already met** ✅
- [ ] SAP-010 (A-MEM) useful for event correlation — **Already met** ✅
- [ ] SAP-015 (task-tracking) useful for task decomposition — **Already met** ✅ (just created)

---

## Deliverables Summary

| Phase | Deliverables | Effort | Priority |
|-------|--------------|--------|----------|
| Phase 1 | 9 files (root + domain awareness) | 7-10h | P0 |
| Phase 2 | 3 SAPs enhanced (P0 SAPs) | 8-11h | P0 |
| Phase 3 | 3 SAPs enhanced (P1 high-value) | 9-12h | P1 |
| Phase 4 | 2 SAPs enhanced (P1 infrastructure) | 6-8h | P1 |
| Phase 5 | 12 SAPs with awareness files | 10-15h | P1 |
| Phase 6 | 8 SAPs (optional) | 19-27h | P2 |
| **Total** | **34-39 files, 10 SAPs enhanced** | **40-56h core, 59-83h with optional** | **P0-P2** |

---

## Next Steps

1. **Review and Approve Plan**: Victor reviews this document, approves execution strategy
2. **Create Beads Epic** (if SAP-015 adopted):
   ```bash
   bd create "PLAN-2025-11-04: SAP-009 Full Adoption + SAP Enhancements" \
     --priority 0 \
     --description "Execute 40-56h plan for full SAP-009 adoption and 10 SAP enhancements"
   ```
3. **Create Phase 1 Subtasks**: Break down Phase 1 into actionable tasks
4. **Begin Execution**: Start with root CLAUDE.md creation
5. **Weekly Check-ins**: Review progress, adjust strategy as needed

---

## Appendix A: Awareness File Template

### Template: AGENTS.md

```markdown
# {SAP Name} - Agent Awareness

**SAP ID**: {SAP-NNN}
**Version**: {X.Y.Z}
**Last Updated**: {YYYY-MM-DD}

---

## Quick Reference

**Key Commands**:
```bash
# Command 1: Description
{command}

# Command 2: Description
{command}
```

**When to Use This SAP**:
- ✅ Use case 1
- ✅ Use case 2
- ❌ Don't use for X (use {alternative} instead)

---

## Common Workflows

### Workflow 1: {Name}

**Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Example**:
```bash
{concrete example}
```

### Workflow 2: {Name}

...

---

## Integration with Other SAPs

- **{SAP-NNN}**: {How they integrate}
- **{SAP-MMM}**: {How they integrate}

---

## Troubleshooting

### Issue 1: {Description}

**Solution**:
```bash
{fix}
```

### Issue 2: {Description}

**Solution**:
```bash
{fix}
```

---

## Full Documentation

- [Capability Charter](capability-charter.md)
- [Protocol Spec](protocol-spec.md)
- [Awareness Guide](awareness-guide.md)
- [Adoption Blueprint](adoption-blueprint.md)
- [Ledger](ledger.md)
```

---

### Template: CLAUDE.md

```markdown
# {SAP Name} - Claude-Specific Awareness

**SAP ID**: {SAP-NNN}
**Claude Version**: Sonnet 4.5+
**Last Updated**: {YYYY-MM-DD}

---

## Quick Start for Claude

**First-Time Use**:
1. Read [protocol-spec.md](protocol-spec.md) for complete technical details
2. Read [awareness-guide.md](awareness-guide.md) for operating patterns
3. Use this file for quick reference during sessions

**Session Resumption**:
- Check [AGENTS.md](AGENTS.md) for generic patterns
- Use this file for Claude-specific shortcuts

---

## Claude Code Integration

### Tool Usage Patterns

**When using Bash tool**:
```bash
# Pattern 1: {Description}
{command}
```

**When using Read tool**:
```bash
# Pattern 1: {Description}
{command}
```

### Common Pitfalls for Claude

1. **Pitfall 1**: {Description}
   - **Fix**: {Solution}

2. **Pitfall 2**: {Description}
   - **Fix**: {Solution}

---

## Context Loading Strategy

**Phase 1 (0-10k tokens)**:
- Read [AGENTS.md](AGENTS.md) for quick reference

**Phase 2 (10-50k tokens)**:
- Read [protocol-spec.md](protocol-spec.md) for complete spec
- Read [awareness-guide.md](awareness-guide.md) for patterns

**Phase 3 (50-200k tokens)**:
- Read [capability-charter.md](capability-charter.md) for design rationale
- Read [ledger.md](ledger.md) for adoption history

---

## Example Claude Code Session

```markdown
User: "Set up {SAP feature}"

Claude:
1. Read /path/to/{SAP}/AGENTS.md for quick reference
2. {Step 2}
3. {Step 3}

[Claude executes workflow using Bash, Read, Write tools]
```

---

## Claude-Specific Tips

- **Tip 1**: {Description}
- **Tip 2**: {Description}
- **Tip 3**: {Description}

---

## Full Documentation

See [AGENTS.md](AGENTS.md) for complete awareness guide.
```

---

## Appendix B: Link Checker Script

Create automated link validation for awareness network:

```bash
#!/bin/bash
# scripts/validate-awareness-links.sh

echo "Validating awareness file link network..."

# Find all AGENTS.md and CLAUDE.md files
awareness_files=$(find . -name "AGENTS.md" -o -name "CLAUDE.md")

broken_links=0

for file in $awareness_files; do
  echo "Checking $file..."

  # Extract markdown links [text](path)
  links=$(grep -o '\](.*\.md)' "$file" | sed 's/][(]//g' | sed 's/)//g')

  for link in $links; do
    # Resolve relative path
    dir=$(dirname "$file")
    target="$dir/$link"

    if [ ! -f "$target" ]; then
      echo "  ❌ Broken link: $link in $file"
      broken_links=$((broken_links + 1))
    fi
  done
done

if [ $broken_links -eq 0 ]; then
  echo "✅ All links valid!"
  exit 0
else
  echo "❌ Found $broken_links broken links"
  exit 1
fi
```

---

## Appendix C: Effort Estimation Methodology

**Baseline**: SAP-015 creation took ~6 hours for 5 artifacts (charter, spec, guide, blueprint, ledger)

**Awareness File Estimates**:
- **AGENTS.md** (generic): 1-1.5h per SAP (shorter, reuses spec/guide)
- **CLAUDE.md** (Claude-specific): 1-1.5h per SAP (similar length)
- **Root CLAUDE.md**: 2-3h (comprehensive, link tree)
- **Domain AGENTS.md**: 1h each (overview, link map)
- **Domain CLAUDE.md**: 30-45min each (shorter, specific tips)

**Enhancement Estimates**:
- **Ledger TODOs**: 30-60min (fill in adoption, metrics, feedback)
- **Status elevation**: 15-30min (update status, catalog)
- **Integration examples**: 30-60min (concrete examples for patterns)

**Buffers**:
- 20% buffer for unexpected complexity
- 10% buffer for review/revision cycles

---

**Version History**:
- **1.0.0** (2025-11-04): Initial plan for SAP-009 full adoption + 10 SAP enhancements
