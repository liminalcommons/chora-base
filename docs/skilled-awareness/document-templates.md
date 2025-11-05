# Skilled Awareness Package Document Templates

**Purpose:** Provide solution-neutral structures for the five core artefacts that define a Skilled Awareness Package (SAP). These templates translate the audit findings into reusable scaffolds that any capability team can adopt without prescribing implementation details.

---

## 1. Capability Charter Template

**Diataxis Category:** Explanation (Understanding-oriented)
**Audience:** Maintainers, stakeholders, governance bodies
**Goal:** Establish shared intent, scope, and success measures before protocols/blueprints are developed.

**Diataxis Writing Guidelines**:
- ✅ **DO**: Explain WHY this capability exists (problem context, motivation)
- ✅ **DO**: Discuss design trade-offs and alternatives considered
- ✅ **DO**: Provide rationale for key decisions
- ✅ **DO**: Connect to broader strategic goals
- ❌ **DON'T**: Include step-by-step installation instructions (belongs in adoption-blueprint)
- ❌ **DON'T**: Document API specifications or schemas (belongs in protocol-spec)
- ❌ **DON'T**: Describe specific task-solving workflows (belongs in awareness-guide)

**Key Question**: "Why does this capability exist, and why did we design it this way?"

See [SAP Diataxis Mapping](../../user-docs/reference/sap-diataxis-mapping.md#quadrant-4-explanation-understanding-oriented) for more guidance.

````markdown
# Capability Charter: {{ capability_name }}

## 1. Context and Motivation
- **Problem Statement:** {{ why this capability exists }}
- **Drivers:** {{ strategic goals, stakeholder needs, triggering events }}
- **Assumptions:** {{ known constraints, dependencies, invariants }}

## 2. Scope Definition
- **In Scope:** {{ concrete functions included }}
- **Out of Scope:** {{ explicit exclusions }}
- **Intersections:** {{ related capabilities, ecosystem touchpoints }}

## 3. Outcomes and Measures
- **Primary Outcomes:** {{ what success looks like }}
- **Leading Indicators:** {{ measurable signals during rollout }}
- **Lagging Indicators:** {{ long-term metrics }}

## 4. Stakeholders and Roles
- **Maintainer(s):** {{ names or roles }}
- **Primary Users:** {{ teams, agents }}
- **Review Cadence:** {{ e.g., quarterly retro }}

## 5. Lifecycle Plan
- **MVP Milestones:** {{ phased objectives }}
- **Open Questions:** {{ risks, research items }}
- **Sunset Criteria:** {{ when/how capability retires or evolves }}
`````

---

## 2. Protocol Specification Template

**Diataxis Category:** Reference (Information-oriented)
**Audience:** Engineers, architects, tooling maintainers
**Goal:** Define the normative behavior, interfaces, and governance for the capability.

**Diataxis Writing Guidelines**:
- ✅ **DO**: Provide factual, comprehensive technical specifications
- ✅ **DO**: Document data models, schemas, APIs, and interfaces
- ✅ **DO**: Specify guarantees, constraints, and error cases
- ✅ **DO**: Use consistent, predictable structure
- ❌ **DON'T**: Use tutorial language ("Let's create...", "You'll learn...")
- ❌ **DON'T**: Include problem-solving patterns (belongs in awareness-guide)
- ❌ **DON'T**: Explain design rationale or why (belongs in capability-charter)

**Key Question**: "What exactly does this capability do, and how is it technically specified?"

See [SAP Diataxis Mapping](../../user-docs/reference/sap-diataxis-mapping.md#quadrant-3-reference-information-oriented) for more guidance.

````markdown
# {{ capability_name }} Protocol Specification

**Version:** {{ semver }}  
**Status:** {{ Draft | Proposed | Active }}  
**Maintainer:** {{ role/team }}

## 1. Overview
- **Purpose:** {{ succinct description }}
- **Intended Consumers:** {{ repos, agents, systems }}
- **Modes of Operation:** {{ e.g., planning vs execution, automated vs manual }}

## 2. Design Principles
1. {{ principle name }} — {{ rationale }}
2. {{ principle name }} — {{ rationale }}

## 3. Functional Requirements
- **FR-1:** {{ requirement }} (Acceptance criteria / validation notes)
- …

## 4. Interfaces and Artifacts
- **Inputs:** {{ file formats, schemas, message contracts }}
- **Outputs:** {{ expected artefacts, event logs }}
- **API / CLI Hooks:** {{ commands, endpoints }}

## 5. Operational Workflow
- **Lifecycle Stages:** {{ stage name → description, entry/exit criteria }}
- **Decision Branches:** {{ conditions that change behavior }}
- **Escalation Paths:** {{ error handling, fallback processes }}

## 6. Governance & Compliance
- **Versioning Policy:** {{ how updates are managed }}
- **Compatibility:** {{ guarantees, breaking-change policy }}
- **Audit Requirements:** {{ logs, checklists }}

## 7. Reference Materials
- **Schemas:** {{ links }}
- **Examples:** {{ sample scenarios }}
- **Related Protocols:** {{ dependencies, peers }}
`````

---

## 3. Agent Awareness Guide Template

**Diataxis Category:** How-To Guide (Task-oriented)
**Audience:** AI agents (Claude, Codex, etc.) and human operators following playbooks
**Goal:** Translate the protocol into actionable behaviors, decision prompts, and context-loading strategies.

**Diataxis Writing Guidelines**:
- ✅ **DO**: Solve specific problems (task-oriented, goal → solution)
- ✅ **DO**: Provide concrete examples for each workflow
- ✅ **DO**: Assume reader understands basics (from adoption-blueprint)
- ✅ **DO**: Include cross-domain references (dev-docs/, project-docs/, user-docs/)
- ✅ **DO**: Document common pitfalls and troubleshooting
- ❌ **DON'T**: Teach fundamentals step-by-step (belongs in adoption-blueprint)
- ❌ **DON'T**: Provide pure technical specs without context (belongs in protocol-spec)
- ❌ **DON'T**: Use hypothetical examples (use real, concrete ones)

**Key Question**: "How do I use this capability to solve specific problems or complete specific tasks?"

See [SAP Diataxis Mapping](../../user-docs/reference/sap-diataxis-mapping.md#quadrant-2-how-to-guides-task-oriented) for more guidance.

````markdown
# {{ capability_name }} Awareness Guide

**Audience:** {{ agent / operator }}  
**Last Updated:** {{ date }}  
**Prerequisites:** {{ files or knowledge to load first }}

## 1. Quick Orientation
- **What This Capability Does:** {{ short description }}
- **When You Use It:** {{ triggers, common requests }}
- **Key Directories / Files:** {{ pointers with purpose }}

## 2. Operating Patterns
### Pattern A: {{ task name }}
1. **Recognize:** {{ commands or cues }}
2. **Act:** {{ steps (code snippets, CLI, markdown responses) }}
3. **Confirm:** {{ verification, logs }}

### Pattern B: {{ task name }}
- …

## 3. Decision Support
- **Checklist:** {{ go/no-go questions }}
- **Escalation Rules:** {{ when to defer to human/stakeholder }}
- **Context Management:** {{ what to keep in memory, checkpoint cadence }}

## 4. Collaboration Protocols
- **Artifacts to produce:** {{ summaries, updates }}
- **Event Logging:** {{ structure, emit commands }}
- **Handoff Notes:** {{ maintaining continuity }}

## 5. Troubleshooting
- **Common Issues:** {{ symptoms → corrective actions }}
- **Fallback Patterns:** {{ alternate workflows }}
- **Ask-for-help Template:** {{ structured request }}

## 6. Continuous Learning Hooks
- **Feedback Capture:** {{ where to log improvements }}
- **Updates Subscription:** {{ how agents learn about protocol changes }}
`````

---

## 4. Adoption Blueprint Template

**Diataxis Category:** Tutorial (Learning-oriented)
**Audience:** Repository maintainers adopting the capability
**Goal:** Provide a neutral installation/upgrade path that can be implemented via scripts, templates, or manual steps.

**Diataxis Writing Guidelines**:
- ✅ **DO**: Create a learning journey (teaches while doing)
- ✅ **DO**: Provide sequential steps with expected outcomes at each stage
- ✅ **DO**: Include validation checkpoints ("You should now have X")
- ✅ **DO**: Make it beginner-friendly (minimal assumed knowledge beyond prerequisites)
- ✅ **DO**: Ensure it's safe to experiment (clear rollback/validation)
- ✅ **DO**: Include post-install awareness enablement (AGENTS.md updates)
- ❌ **DON'T**: Focus on problem-solving or troubleshooting (belongs in awareness-guide)
- ❌ **DON'T**: Include detailed API specifications (belongs in protocol-spec)
- ❌ **DON'T**: Explain design rationale (belongs in capability-charter)

**Key Question**: "How do I install and get started with this capability for the first time?"

See [SAP Diataxis Mapping](../../user-docs/reference/sap-diataxis-mapping.md#quadrant-1-tutorials-learning-oriented) for more guidance.

````markdown
# Adoption Blueprint: {{ capability_name }}

## 1. Read Before You Begin
- **Capability Charter:** {{ link }}
- **Protocol Spec:** {{ link }}
- **Prerequisites:** {{ repo state, tooling, permissions }}

## 2. Installation Paths
- **Option A (Automated):** {{ scripts or templates }}
- **Option B (Manual):** {{ manual copy/migrate steps }}
- **Fallback:** {{ minimal viable adoption if full install blocked }}

## 3. Files & Directories
| Path | Purpose | Optional? | Notes |
|------|---------|-----------|-------|
| {{ path }} | {{ description }} | {{ yes/no }} | {{ extra context }} |

## 4. Configuration Checklist
- [ ] {{ configuration step }} (link to reference)
- …

## 5. Verification
- **Smoke Tests:** {{ commands / checks }}
- **Acceptance Tests:** {{ expected outcomes }}
- **Rollback Plan:** {{ how to revert if validation fails }}

## 6. Post-Install Tasks

### Awareness Enablement

**Update Root AGENTS.md**:

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Capabilities", "Project Structure", or "SAPs")
3. Add:

```markdown
### SAP-{{ id }}: {{ capability_name }}

**Quick Start**: {{ essential commands or patterns }}
**Detailed Guide**: {{ link to awareness-guide or domain-specific AGENTS.md }}
**Related SAPs**: {{ dependencies or related capabilities }}
```

**Validation**:
```bash
grep "SAP-{{ id }}\|{{ capability_name }}" AGENTS.md && echo "✅ AGENTS.md updated"
```

**Update Domain-Specific AGENTS.md** (if applicable):
{{ If SAP creates/modifies files in specific domain (tests/, scripts/, docker/), include: }}
- Copy: `static-template/{{ domain }}/AGENTS.md` → `{{ domain }}/AGENTS.md`
- Customize with {{ capability-specific patterns }}

**Update CLAUDE.md** (if applicable):
{{ If SAP involves Claude-specific patterns or context optimization: }}
- Add cross-reference to new capability
- Update context loading guidance for {{ capability_name }}

---

### Status Ledger Update

Update the SAP ledger to record your adoption:

**For agents** (use Edit tool):
1. Open: `docs/skilled-awareness/{{ sap-directory }}/ledger.md`
2. Find "Adopter Registry" table
3. Add row:

```markdown
| {{ project-name }} | {{ version }} | Active | {{ date }} | Initial adoption |
```

---

### Feedback Loop

{{ How to report issues, request enhancements, or share learnings }}
- Create issue in {{ repository }}
- Tag with `SAP-{{ id }}` label
- {{ Additional feedback channels }}
`````

---

## 5. Traceability Ledger Template

**Diataxis Category:** Reference (Information-oriented)
**Audience:** Ecosystem coordinators, governance teams
**Goal:** Maintain a living record of adoption status, feedback, and lifecycle events across repositories.

**Diataxis Writing Guidelines**:
- ✅ **DO**: Record factual adoption data (who, when, version, status)
- ✅ **DO**: Track version history with dates
- ✅ **DO**: Use structured format (tables recommended)
- ✅ **DO**: Keep it purely factual and objective
- ❌ **DON'T**: Include tutorial or explanatory content
- ❌ **DON'T**: Explain why or provide rationale (belongs in capability-charter)
- ❌ **DON'T**: Include how-to or troubleshooting content (belongs in awareness-guide)

**Key Question**: "What is the adoption status and version history of this capability?"

See [SAP Diataxis Mapping](../../user-docs/reference/sap-diataxis-mapping.md#quadrant-3-reference-information-oriented) for more guidance.

````markdown
# Skilled Awareness Package Ledger: {{ capability_name }}

## 1. Snapshot
- **Protocol Version:** {{ semver }}
- **Maintainer:** {{ role }}
- **Last Review:** {{ date }}

## 2. Adoption Table
| Repository | Protocol Version | Awareness Installed | Blueprint Status | Notes | Last Updated |
|-----------|------------------|----------------------|------------------|-------|--------------|
| {{ repo }} | {{ version }} | {{ yes/no }} | {{ Not Started / In Progress / Complete }} | {{ blockers, feedback }} | {{ date }} |

## 3. Feedback Log
- **Date:** {{ yyyy-mm-dd }}  
  **Source:** {{ repo / contributor }}  
  **Summary:** {{ key points }}  
  **Action Taken:** {{ decision or follow-up }}

## 4. Upcoming Actions
- [ ] {{ action item }} (Owner: {{ name }}, Due: {{ date }})

## 5. Change History
- **YYYY-MM-DD:** {{ event description }} (e.g., protocol v1.1 released, ledger updated)
`````

---

### Usage Notes
- Each template intentionally references the others (e.g., blueprint links to charter/spec). This ensures consistency without hard-coding implementation specifics.
- Teams may convert these markdown templates into Copier blueprints, docs-as-code checklists, or other tooling, so long as sections remain discoverable.
- Version control: treat templates as living standards; when updated, flag downstream repositories via the Traceability Ledger.

