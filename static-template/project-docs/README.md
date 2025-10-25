# Project Documentation

This directory contains **project management and planning documentation** for {{ project_name }}.

## Contents

- **[sprints/](sprints/)** - Sprint planning, capacity tracking, retrospectives
- **[releases/](releases/)** - Release planning, notes, deployment checklists
- **[metrics/](metrics/)** - Process KPIs, quality metrics, velocity tracking
- **[ROADMAP.md](../ROADMAP.md)** - Committed features, timelines, strategic goals

## How This Connects to Development Workflows

**Planning → Execution:**
1. **Roadmap** ([../ROADMAP.md](../ROADMAP.md)) defines committed features
2. **Sprint Planning** ([sprints/](sprints/)) breaks work into iterations
3. **Development Workflows** ([../dev-docs/workflows/](../dev-docs/workflows/)) execute with DDD → BDD → TDD
4. **Metrics** ([metrics/](metrics/)) track quality, velocity, process adherence
5. **Releases** ([releases/](releases/)) deliver features to production

**Key Integration Points:**
- Sprint capacity planning uses workflow time estimates (DDD: 3-5h, BDD: 2-4h, TDD: 40%)
- Quality gates enforce coverage (≥{{ test_coverage_threshold }}%), process adherence (≥90%)
- Metrics validate workflow effectiveness (defect reduction, velocity predictability)

## Audience

- **Product Managers** - Roadmap planning, feature prioritization, release coordination
- **Engineering Leads** - Sprint planning, capacity allocation, process metrics
- **AI Agents** - Sprint planning templates, time estimates, quality gate criteria
- **Stakeholders** - Project status, milestone tracking, delivery confidence

## Related Documentation

**Development:**
- **[dev-docs/workflows/](../dev-docs/workflows/)** - 8-phase development lifecycle (DDD, BDD, TDD)
- **[dev-docs/examples/](../dev-docs/examples/)** - Complete feature walkthroughs with real data
- **[dev-docs/ANTI_PATTERNS.md](../dev-docs/ANTI_PATTERNS.md)** - Common mistakes to avoid

**Usage:**
- **[user-docs/](../user-docs/)** - End-user documentation (how to use {{ project_name }})

**Project:**
- **[AGENTS.md](../AGENTS.md)** - Complete project guide for AI agents
- **[CONTRIBUTING.md](../dev-docs/CONTRIBUTING.md)** - Contribution guidelines

---

**Note:** This directory is for **planning and managing** {{ project_name }}. For development execution, see [dev-docs/workflows/](../dev-docs/workflows/). For product usage, see [user-docs/](../user-docs/).
