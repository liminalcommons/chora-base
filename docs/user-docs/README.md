# User Documentation

**Purpose**: Documentation for users of the delivered product (chora-base)

**Audience**: End-users consuming chora-base, developers adopting it, operators deploying projects built with it

---

## What's Here

This directory contains end-user documentation using **Diátaxis**:

- **[how-to/](how-to/)** - Task-oriented guides
  - [write-executable-documentation.md](how-to/write-executable-documentation.md) - Guide for writing executable how-tos
  - [setup-mcp-ecosystem.md](how-to/setup-mcp-ecosystem.md) - How to set up MCP ecosystem

- **[explanation/](explanation/)** - Conceptual understanding
  - [benefits-of-chora-base.md](explanation/benefits-of-chora-base.md) - Why use chora-base
  - [architecture-clarification.md](explanation/architecture-clarification.md) - Architectural concepts
  - [multi-repo-capability-evolution.md](explanation/multi-repo-capability-evolution.md) - Multi-repo patterns

- **[reference/](reference/)** - Technical specifications
  - (See static-template/user-docs/reference/ for examples)

- **[tutorials/](tutorials/)** - Learning-oriented lessons
  - (To be populated in future waves)

---

## Diátaxis Structure

This domain uses **Diátaxis for product usage**:

| Type | Purpose | When to Use | Example |
|------|---------|-------------|---------|
| **tutorials/** | Learning-oriented | Studying, acquiring skills | "Your First Chora-Base Project" |
| **how-to/** | Task-oriented | Working, solving problems | "How to Install SAP-004" |
| **reference/** | Information-oriented | Looking up facts | "SAP Protocol Specification" |
| **explanation/** | Understanding-oriented | Studying concepts | "4-Domain Architecture Explained" |

---

## Not Here

- **Development processes**: See [../dev-docs/](../dev-docs/)
- **Sprint plans**: See [../project-docs/sprints/](../project-docs/sprints/)
- **Research learnings**: See [../dev-docs/research/](../dev-docs/research/)
- **SAP installation details**: See [../skilled-awareness/](../skilled-awareness/) (each SAP has adoption-blueprint.md)

---

## Related Documentation

**Other Domains**:
- [Developer Documentation](../dev-docs/) - For developers working ON chora-base
- [Project Documentation](../project-docs/) - Project lifecycle artifacts
- [Skilled Awareness](../skilled-awareness/) - SAP Framework (capability packages)

**Root Documentation**:
- [Architecture](../ARCHITECTURE.md) - 4-domain model explained
- [README.md](../../README.md) - Project overview
- [AGENTS.md](../../AGENTS.md) - Complete guide for AI agents
- [ROADMAP.md](../../ROADMAP.md) - Product roadmap

**Examples from static-template**:
- [static-template/user-docs/](../../static-template/user-docs/) - Complete user documentation structure

---

## How to Use This Domain

### For New Adopters

1. **Start here**: Read [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md)
2. **Understand architecture**: Read [../ARCHITECTURE.md](../ARCHITECTURE.md)
3. **Learn by doing**: Follow tutorials/ (when available)
4. **Get things done**: Use how-to/ for specific tasks

### For Integrators

1. **Setup**: Follow [how-to/setup-mcp-ecosystem.md](how-to/setup-mcp-ecosystem.md)
2. **Reference**: Use reference/ for API specs and configs
3. **Understand**: Read explanation/ for conceptual clarity

### For Operators

1. **Deploy**: Use how-to/ for deployment guides
2. **Configure**: Reference reference/ for configuration specs
3. **Troubleshoot**: Combine how-to/ and explanation/

### For AI Agents

1. **Onboarding**: Read explanation/ to understand chora-base concepts
2. **Tasks**: Use how-to/ for step-by-step guidance
3. **Lookup**: Use reference/ for quick facts
4. **Learning**: Follow tutorials/ for structured lessons

---

## Contributing to User Docs

### Adding How-To Guides

**Structure**:
```markdown
# How to [Accomplish Task]

**Goal**: [What user will achieve]
**Time**: [Estimated time]
**Prerequisites**: [What user needs]

## Steps

1. [Action step]
2. [Action step]
...

## Validation

How to verify success

## Troubleshooting

Common issues and solutions
```

**Placement**: Ensure task is user-facing (not development process)

### Adding Explanations

**Structure**:
```markdown
# [Concept] Explained

**Purpose**: [Why this matters]

## Overview
High-level summary

## How It Works
Technical details

## Benefits
Why users care

## Related Concepts
Cross-links
```

**Placement**: Ensure concept is about the product (not internal development)

### Adding Reference Material

**Structure**:
```markdown
# [Thing] Reference

## Specification
Dry, accurate, complete information

## Parameters / Options
Detailed parameter docs

## Examples
Minimal, focused examples
```

**Placement**: Technical specifications, API docs, config schemas

### Adding Tutorials

**Structure**:
```markdown
# Tutorial: [Learning Goal]

**What you'll learn**: [Skills acquired]
**Time**: [Estimated time]
**Prerequisites**: [Required knowledge]

## Lesson 1: [Topic]
Step-by-step, beginner-friendly

## Lesson 2: [Topic]
...

## Summary
What was learned

## Next Steps
Where to go next
```

**Placement**: Learning-oriented, for beginners

---

## Quality Standards

**All user docs should**:
- Use clear, simple language
- Include examples
- Provide next steps or related docs
- Be tested with actual users (human or AI)
- Follow Diátaxis classification

**Avoid**:
- Internal jargon without explanation
- Development process details (→ dev-docs/)
- Project management content (→ project-docs/)

---

**Domain Version**: 1.0 (Wave 1)
**Last Updated**: 2025-10-28
**Status**: Active
