# Skilled Awareness Package Document Templates

**Purpose:** Provide solution-neutral structures for the five core artefacts that define a Skilled Awareness Package (SAP). These templates translate the audit findings into reusable scaffolds that any capability team can adopt without prescribing implementation details.

---

## 1. Capability Charter Template

**Audience:** Maintainers, stakeholders, governance bodies  
**Goal:** Establish shared intent, scope, and success measures before protocols/blueprints are developed.

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

**Audience:** Engineers, architects, tooling maintainers  
**Goal:** Define the normative behavior, interfaces, and governance for the capability.

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

**Audience:** AI agents (Claude, Codex, etc.) and human operators following playbooks  
**Goal:** Translate the protocol into actionable behaviors, decision prompts, and context-loading strategies.

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

**Audience:** Repository maintainers adopting the capability  
**Goal:** Provide a neutral installation/upgrade path that can be implemented via scripts, templates, or manual steps.

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
- **Awareness Enablement:** {{ add references to AGENTS/CLAUDE }}
- **Status Ledger Update:** {{ log adoption state }}
- **Feedback Loop:** {{ how to report issues or improvements }}
`````

---

## 5. Traceability Ledger Template

**Audience:** Ecosystem coordinators, governance teams  
**Goal:** Maintain a living record of adoption status, feedback, and lifecycle events across repositories.

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

