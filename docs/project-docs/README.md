# Project Documentation

**Purpose**: Living documents generated/updated during project lifecycle

**Audience**: Project managers, stakeholders, future maintainers, leadership

---

## What's Here

This directory contains project management artifacts:

- **[sprints/](sprints/)** - Sprint plans, retrospectives, velocity tracking
  - [wave-1-sprint-plan.md](sprints/wave-1-sprint-plan.md) - Wave 1 execution plan

- **[releases/](releases/)** - Release notes, plans, post-mortems
  - v2.x and v3.x release notes
  - Upgrade guides and migration documentation

- **[metrics/](metrics/)** - Quality metrics, process metrics, ROI calculations
  - (To be populated during wave execution)

- **[integration/](integration/)** - Integration plans, coordination documents
  - v3.2.0 and v3.3.0 integration plans

- **[inventory/](inventory/)** - Repository audits, coherence reports
  - [COHERENCE_REPORT.md](inventory/COHERENCE_REPORT.md) - 100% coherence achievement
  - SAP coverage analysis and gap reports

- **Root files**:
  - [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md) - v4.0 transformation roadmap
  - [v4-cleanup-manifest.md](v4-cleanup-manifest.md) - Cleanup tracking for v4.0 waves
  - [DOCUMENTATION_PLAN.md](DOCUMENTATION_PLAN.md) - Documentation strategy

---

## Characteristics

**Living**: Updated throughout project lifecycle
- Sprint plans evolve as work progresses
- Metrics accumulate over time
- Release notes written as features ship

**Historical**: Permanent record of decisions and progress
- Sprint retrospectives capture learnings
- Integration plans document coordination
- Inventory reports track structural evolution

**Stakeholder-facing**: Often shared with PMs, leadership
- Metrics demonstrate ROI
- Release notes communicate value delivered
- Integration plans coordinate across teams

**Generated**: Created as part of PM process, not written upfront
- Sprint plans created at sprint start
- Metrics collected during execution
- Release notes written at release time

---

## Not Here

- **Development processes**: See [../dev-docs/workflows/](../dev-docs/workflows/)
- **User guides**: See [../user-docs/](../user-docs/)
- **Code examples**: See [../dev-docs/examples/](../dev-docs/examples/)
- **SAP documentation**: See [../skilled-awareness/](../skilled-awareness/)

---

## Related Documentation

**Other Domains**:
- [Developer Documentation](../dev-docs/) - For developers working on the product
- [User Documentation](../user-docs/) - For product users
- [Skilled Awareness](../skilled-awareness/) - SAP Framework (capability packages)

**Root Documentation**:
- [Architecture](../ARCHITECTURE.md) - 4-domain model explained
- [ROADMAP.md](../../ROADMAP.md) - Product roadmap
- [CHANGELOG.md](../../CHANGELOG.md) - Version history

**Examples from static-template**:
- [static-template/project-docs/sprints/](../../static-template/project-docs/sprints/) - Sprint templates
- [static-template/project-docs/metrics/](../../static-template/project-docs/metrics/) - Metrics examples

---

## How to Use This Domain

### For Project Managers

1. **Planning**: Create sprint plans in sprints/
2. **Tracking**: Update metrics in metrics/ during execution
3. **Releasing**: Document releases in releases/
4. **Coordinating**: Create integration plans in integration/

### For Stakeholders

1. **Progress**: Check sprints/ for current status
2. **Quality**: Review metrics/ for process adherence
3. **History**: Browse releases/ for what shipped when
4. **Audits**: Review inventory/ for structural coherence

### For AI Agents

1. **Sprint start**: Read sprint plan to understand committed work
2. **During execution**: Update metrics as you work
3. **Sprint end**: Contribute to retrospective learnings
4. **Release time**: Help draft release notes

### For Future Maintainers

1. **Context**: Read integration/ and inventory/ to understand decisions
2. **Patterns**: Review sprint retrospectives for learnings
3. **History**: Browse releases/ to see evolution over time

---

## Meta-Demonstration

Wave 1 demonstrates this domain in action:
- **Sprint plan**: [sprints/wave-1-sprint-plan.md](sprints/wave-1-sprint-plan.md) - Planning document
- **Vision**: [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md) - Strategic roadmap
- **Cleanup**: [v4-cleanup-manifest.md](v4-cleanup-manifest.md) - Tracking cleanup items
- **Metrics**: metrics/wave-1-execution-metrics.md (to be created)

This is "dogfooding" - chora-base uses its own project-docs/ structure for its own development.

---

**Domain Version**: 1.0 (Wave 1)
**Last Updated**: 2025-10-28
**Status**: Active
