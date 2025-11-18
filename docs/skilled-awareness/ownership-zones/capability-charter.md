# Capability Charter: Ownership Zones

**SAP ID**: SAP-052
**Version**: 1.0.0
**Status**: In Development
**Owner**: chora-base maintainer
**Created**: 2025-11-17
**Last Updated**: 2025-11-17

---

## 1. Problem Statement

### Current Challenge

Without clear code ownership zones, multi-developer teams experience review bottlenecks, conflicting changes in shared files, and unclear accountability for code quality. As the chora ecosystem transitions from single-developer to multi-developer collaboration, the lack of formal ownership creates several critical problems:

**What's missing**:
1. **No code ownership mapping** - No formal definition of which developers or teams own which parts of the codebase
2. **Manual reviewer assignment** - Every PR requires manual decision-making about who should review ("who should review this?")
3. **Unclear accountability** - No clear ownership for code quality, documentation, or maintenance in specific domains
4. **No automatic reviewer assignment** - GitHub/GitLab CODEOWNERS features not utilized
5. **No ownership metrics** - No visibility into ownership coverage (% of files with assigned owners)
6. **No conflict jurisdiction rules** - When two developers modify the same file, unclear who has decision authority

**Impact on multi-developer workflows**:
- Review coordination overhead wastes 10-15 minutes per PR asking "who should review this?"
- PRs blocked waiting for correct reviewer to be identified and assigned
- Merge conflicts have unclear resolution authority (who decides when both developers are right?)
- Code quality inconsistent across domains (no clear owner to enforce standards)
- Knowledge silos form when ownership is implicit rather than explicit

### Evidence

- Currently: **100% manual reviewer assignment** for all PRs across chora ecosystem
- Average "who should review?" coordination time: **10-15 min per PR** (5-10 PRs/week = 50-150 min/week wasted)
- **No CODEOWNERS files** in any ecosystem repo (chora-base, chora-workspace, chora-compose)
- **Zero ownership coverage** - 0% of files have explicit ownership assignments
- Merge conflicts resolved ad-hoc with no clear jurisdiction rules
- Review bottlenecks when specific domain expert unavailable (blocks PRs)
- Knowledge transfer difficult because ownership relationships are implicit/tribal

### Business Impact

**Immediate costs** (quantified):
- **Review coordination overhead**: 5-10 PRs/week × 10-15 min = 50-150 min/week = 43-130 hours/year wasted
- **Blocked PRs waiting for reviewer**: 2-3 PRs/week × 30-60 min delay = 60-180 min/week = 52-156 hours/year wasted
- **Conflict resolution delays**: 1-2 conflicts/week × 15-30 min extra (unclear jurisdiction) = 13-52 hours/year wasted
- **Total**: 108-338 hours/year wasted ($16,200-$50,700 at $150/hour)

**Strategic risks**:
- **Scaling bottleneck**: Current manual coordination prevents scaling beyond 2-3 developers effectively
- **Quality degradation**: Unclear ownership leads to "tragedy of the commons" where no one feels responsible
- **Onboarding friction**: New developers don't know who to ask for reviews in different domains
- **Review latency**: Without automatic assignment, PRs sit idle until manually triaged
- **Knowledge loss**: Implicit ownership relationships disappear when developers leave

**Urgency**: With SAP-051 (Git Workflow Patterns) now complete and second developer joining chora-workspace, the lack of ownership zones becomes the next critical bottleneck for effective collaboration. SAP-052 is a prerequisite for SAP-053 (Conflict Resolution) and SAP-054 (Work Partitioning).

---

## 2. Proposed Solution

### Ownership Zones Pattern

Define **SAP-052: Ownership Zones** establishing clear code ownership through CODEOWNERS-based domain mapping, automatic reviewer assignment, and conflict jurisdiction rules. This SAP provides:

1. **Domain Ownership Mapping** - Map repository directories to domain owners (docs/, scripts/, .chora/, inbox/, project-docs/)
2. **CODEOWNERS File** - GitHub/GitLab-compatible file enabling automatic reviewer assignment
3. **Ownership Coverage Metrics** - Dashboard showing % of files with assigned owners, coverage gaps
4. **Reviewer Assignment Automation** - GitHub auto-assigns reviewers based on file changes in PR
5. **Conflict Jurisdiction Rules** - Clear authority structure for resolving ownership-based conflicts

**How it solves the problem**:
- **Eliminates "who reviews?" overhead**: Automatic assignment based on file patterns (10-15 min → 0 min per PR)
- **Accelerates review assignment**: GitHub assigns reviewers immediately on PR creation (no manual triage)
- **Establishes accountability**: Each domain has explicit owner responsible for quality
- **Provides fallback reviewers**: CODEOWNERS supports multiple owners per domain
- **Enables conflict resolution**: Ownership determines jurisdiction when conflicts arise

**Alignment with ecosystem**:
- **SAP-001 (Inbox)**: Ownership zones align with coordination request routing
- **SAP-010 (Memory)**: Domain ownership guides knowledge note categorization
- **SAP-015 (Beads)**: Ownership mapping helps assign beads tasks to correct developers
- **SAP-051 (Git Workflow)**: Branch naming conventions integrate with ownership patterns

### Key Principles

1. **Directory-level ownership** - Ownership at directory level (not file-level) for maintainability
2. **Explicit over implicit** - Formal CODEOWNERS file makes ownership visible and queryable
3. **Multiple owners supported** - Domains can have primary + fallback reviewers
4. **Coverage is measurable** - Track % of files covered by ownership patterns
5. **GitHub/GitLab integration** - Use platform features for automatic reviewer assignment
6. **Ownership rotation** - Support quarterly ownership rotation to prevent knowledge silos
7. **Graceful degradation** - System works even without GitHub integration (manual assignment with guidance)
8. **Conflict jurisdiction** - Owner has authority to resolve conflicts in their domain

---

## 3. Scope

### In Scope

- **CODEOWNERS file format** (GitHub and GitLab compatible syntax)
- **Domain ownership mapping** (5 chora-workspace domains: docs/, scripts/, inbox/, .chora/, project-docs/)
- **Ownership coverage metrics** (% files covered, uncovered files list, coverage dashboard)
- **Automatic reviewer assignment** (via GitHub/GitLab CODEOWNERS integration)
- **Conflict jurisdiction rules** (owner resolves conflicts in domain, escalation protocol)
- **Ownership rotation protocol** (quarterly handoff process, knowledge transfer checklist)
- **Template generator** (script to generate CODEOWNERS from directory structure)
- **Coverage analysis tool** (script to calculate ownership metrics)
- **Reviewer suggester** (tool to recommend reviewers based on git history)
- **Documentation** (5 SAP artifacts: charter, spec, guide, blueprint, ledger)
- **Pilot adoption** (chora-workspace validation with 5 domains)

### Out of Scope

- **File-level ownership** - Too granular, use directory-level patterns instead
- **Code review automation** - Separate concern (review workflow automation is future work)
- **Automated merge conflict resolution** - Ownership provides jurisdiction, not automation
- **Performance reviews based on ownership** - Organizational policy, not technical pattern
- **Cross-repo ownership** - Focus on single-repo ownership patterns first
- **Dynamic ownership** - Static CODEOWNERS file, not runtime ownership computation
- **Ownership enforcement** - CODEOWNERS provides guidance, not blocking enforcement

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- SAP-052 installed in chora-base (5 artifacts present: charter, spec, guide, blueprint, ledger)
- CODEOWNERS template generator functional (generates valid GitHub CODEOWNERS syntax)
- Ownership coverage analysis script operational (calculates % coverage)
- Reviewer suggester tool works (identifies domain experts from git log)
- Documentation complete (adoption blueprint available for repos)

**Operational Success** (Level 2):
- chora-workspace pilot completed (CODEOWNERS file created for 5 domains)
- 80%+ of chora-workspace files covered by ownership patterns
- GitHub recognizes CODEOWNERS file (auto-assigns reviewers on test PRs)
- 90%+ reviewer assignment accuracy on pilot PRs (correct owner assigned)
- Baseline metrics established (coverage %, assignment accuracy, review latency by domain)

**Impact Success** (Level 3):
- 40-60% reduction in "who should review?" coordination time (10-15 min → <5 min per PR)
- 15-25% faster PR reviews via automatic assignment (no manual triage delay)
- 100% domain coverage (all 5 chora-workspace domains have assigned owners)
- Conflict jurisdiction rules validated in pilot (owner-based conflict resolution tested)
- Foundation complete for SAP-053 (Conflict Resolution), SAP-054 (Work Partitioning)

**Qualitative indicators**:
- Developers report clarity on "who owns what" reduces decision fatigue
- PRs no longer sit idle waiting for manual reviewer assignment
- Merge conflicts resolve faster due to clear jurisdiction rules
- New contributors understand ownership structure from CODEOWNERS file

### Expected Metrics

**Performance**:
- CODEOWNERS template generation: <30 seconds per repo
- Ownership coverage analysis: <10 seconds per repo
- Reviewer suggestion query: <5 seconds (git log analysis)

**Adoption**:
- Time to create CODEOWNERS for new repo: <15 min (use template generator)
- Ownership coverage in pilot: 80%+ files covered
- Reviewer assignment accuracy: 90%+ correct assignments
- Repos using SAP-052: 100% of chora ecosystem repos within 6 weeks of publication

**ROI**:
- Year 1 ROI: 125-440% (benefits $10k-35k vs investment ~$8k)
- Year 2+ ROI: 500-900% (benefits continue, investment is one-time)
- Payback period: 2-4 months

---

## 5. Stakeholders & Governance

### Primary Stakeholders

**Maintainers**:
- chora-base team: Owns SAP-052 definition, CODEOWNERS generator, coverage analysis tools
- chora-workspace team: Pilot validation, defines 5-domain ownership structure
- chora-compose team: Integration into project generation template (deferred until SAP-055)

**Users**:
- All developers in chora ecosystem (current: 1 developer, target: 2+ developers)
- Code reviewers: Benefit from automatic assignment reducing coordination overhead
- AI agents (Claude): Use ownership mapping for code navigation and question routing

**Affected Parties**:
- Domain owners: Accountable for code quality in their ownership zones
- New developers: Learn ownership structure during onboarding (simplified by CODEOWNERS visibility)

### Governance Model

**Decision authority**:
- chora-base maintainer: Final approval for SAP-052 definition changes
- chora-workspace lead (Victor): Pilot validation sign-off, domain owner assignments

**Review cadence**:
- Quarterly: Review ownership assignments (rotation, coverage gaps, reassignments)
- On-demand: Update CODEOWNERS when directory structure changes

**Change process**:
- Minor updates (ownership reassignments): Direct commits to CODEOWNERS file
- Major changes (domain structure redesign): RFC process via SAP-001 inbox

**Success review**:
- After chora-workspace pilot (Week 2): Validate success criteria before ecosystem distribution
- After 3 months: Review Level 3 success criteria (coordination time reduction, PR review speed, ROI)

---

## 6. Lifecycle Plan

### Development Phases

**Phase 1: Design & Specification (2025-11-17 to 2025-11-24, 22-29 hours)** 🔄 IN PROGRESS
- Draft SAP-052 charter, protocol specification (CODEOWNERS format, domain mapping)
- Write awareness guide (how to create CODEOWNERS, update ownership, resolve conflicts)
- Create adoption blueprint (templates, checklists)
- Define ownership coverage metrics schema
- Establish conflict jurisdiction rules

**Phase 2: Infrastructure Development (2025-11-24 to 2025-12-01, 22-28 hours)** ⏳ PLANNED
- Build CODEOWNERS template generator (analyze directory structure, generate patterns)
- Create ownership coverage analysis script (calculate % coverage, identify orphans)
- Build reviewer suggester tool (git log analysis, domain expert identification)
- Write validation tests for ownership tools
- Document tools in adoption blueprint

**Phase 3: Pilot Validation (2025-12-01 to 2025-12-14, 16-24 hours)** ⏳ PLANNED
- Create chora-workspace CODEOWNERS file (5 domains: docs/, scripts/, inbox/, .chora/, project-docs/)
- Assign domain owners (can be single owner for pilot)
- Test automatic reviewer assignment (5-10 test PRs)
- Collect ownership coverage metrics (target: 80%+ coverage)
- Validate conflict jurisdiction rules (simulate ownership-based conflict resolution)
- Measure success criteria (assignment accuracy, coordination time reduction)
- Refine SAP-052 based on pilot feedback

**Phase 4: Ecosystem Distribution (Deferred until SAP-055)** ⏳ DEFERRED
- Integrate CODEOWNERS generation into chora-compose project templates
- Publish SAP-052 announcement via SAP-001 inbox
- Provide adoption support to ecosystem repos
- **Note**: Deferred as part of multi-dev suite batch integration strategy

### Open Questions

- **Q1**: Should CODEOWNERS support file-level patterns or only directory-level?
  - **Risk**: File-level patterns more precise but harder to maintain
  - **Mitigation**: Start with directory-level, add file-level only for shared files (e.g., justfile, AGENTS.md)

- **Q2**: How to handle cross-domain changes (PRs touching multiple domains)?
  - **Risk**: CODEOWNERS assigns all domain owners as reviewers (review overload)
  - **Mitigation**: Document "primary reviewer" pattern (first matching pattern is primary, others are FYI)

- **Q3**: How to prevent ownership from becoming stale as code evolves?
  - **Risk**: Ownership patterns don't update when directory structure changes
  - **Mitigation**: Quarterly ownership review cadence, coverage analysis reports orphaned files

- **Q4**: How to handle ownership when developer is unavailable (vacation, leave)?
  - **Risk**: PRs blocked if primary owner not available
  - **Mitigation**: Require fallback owners for each domain, document escalation protocol

### Sunset Criteria

SAP-052 would be retired or superseded if:

1. **GitHub deprecates CODEOWNERS** (unlikely, widely adopted feature)
2. **Ecosystem moves to single-developer model** (unlikely, growth trajectory is multi-dev)
3. **More advanced ownership system emerges** (possible: dynamic ownership based on git history)
4. **Zero adoption** after 6 months (indicates SAP doesn't solve real problem)

**Likely evolution path**: SAP-052 becomes foundation for more advanced capabilities (automated conflict resolution, workload balancing, ownership analytics) rather than being replaced.

---

## 7. Related SAPs & Dependencies

### Dependencies

- **SAP-051 (Git Workflow Patterns)**: ✅ COMPLETE - Provides PR infrastructure, branch naming conventions used in ownership patterns

### Dependents (SAPs that build on SAP-052)

- **SAP-053 (Conflict Resolution)**: Uses ownership jurisdiction for conflict resolution authority
- **SAP-054 (Work Partitioning)**: Uses ownership mapping to partition work across developers
- **SAP-055 (Multi-Dev Awareness)**: Documents ownership zones in AGENTS.md awareness files

### Complementary SAPs

- **SAP-001 (Inbox)**: Ownership zones guide coordination request routing
- **SAP-010 (Memory)**: Domain ownership helps categorize knowledge notes
- **SAP-015 (Beads)**: Ownership mapping aids task assignment to developers

---

## 8. Implementation Summary

**Status**: 🔄 **IN DEVELOPMENT**

**Progress**:
- ✅ Phase 1 started: Charter drafted (this file)
- ⏳ Remaining Phase 1: Specification, guide, blueprint, ledger
- ⏳ Phase 2: Infrastructure development (tools)
- ⏳ Phase 3: Pilot validation (chora-workspace)
- ⏳ Phase 4: Ecosystem distribution (deferred)

**Coordination**:
- CORD-2025-017: chora-base SAP-052 Definition & Tooling (48-67 hours)
- CORD-2025-018: chora-workspace SAP-052 Pilot Validation (16-24 hours)

**Tracking**:
- Epic: .beads-0fv5 (SAP-052 Ownership Zones)
- Task 1: .beads-26v4 (CORD-2025-017 execution)
- Task 2: .beads-6uj4 (CORD-2025-018 execution)

**Timeline**:
- Start: 2025-11-17
- Target completion: 2025-12-14 (4 weeks)
- Ecosystem distribution: Deferred until SAP-055 complete

**Next Steps**: Complete Phase 1 artifacts (spec, guide, blueprint, ledger)

---

**Created**: 2025-11-17 by chora-base maintainer + Claude (AI peer)
**Document Status**: In Development
**Last Updated**: 2025-11-17
