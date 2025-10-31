# Capability Charter: Cross-Repository Inbox Skilled Awareness Package

## 1. Context and Motivation
- **Problem Statement:** The ecosystem lacks a consistent, reproducible way for repositories to exchange strategic proposals, coordination requests, and implementation tasks while keeping documentation and agent guidance aligned.
- **Drivers:** Recent ecosystem review highlighted coordination friction, manual inbox adoption, and uneven agent behavior when handling cross-repo work.
- **Assumptions:** Repositories are Git-based; communication must remain file-centric; AI agents (Claude, Codex) will be primary operators alongside humans; no central SaaS dependency is acceptable.

## 2. Scope Definition
- **In Scope:** Git-native inbox structure, intake schemas (strategic, coordination, implementation), routing workflows, event logging conventions, agent operations guidance, adoption blueprint for downstream repos.
- **Out of Scope:** Non-file-based workflow tools, proprietary task systems, automated cross-repo execution (beyond logging and triage), organization-wide governance policy changes.
- **Intersections:**  
  - **Protocols:** Development lifecycle (DDD/BDD/TDD), memory system, release coordination.  
  - **Capabilities:** Ecosystem status reporting, governance repos (meta-blueprints), future status protocol.

## 3. Outcomes and Measures
- **Primary Outcomes:**  
  1. Repositories can install the inbox package with documented steps and validation.  
  2. Agents follow a consistent playbook when triaging and executing inbox items.  
  3. Ecosystem coordination visibility improves via shared ledger updates.
- **Leading Indicators:** Number of repos piloting the package, completion of agent dry runs without intervention, reduction in misrouted tasks.
- **Lagging Indicators:** Time-to-triage across repos, coordination issues caught before execution, adoption breadth across governance repos.

## 4. Stakeholders and Roles
- **Maintainer(s):** Victor Piper (Capability Owner), Codex assistant (supporting author).
- **Primary Users:** Claude Code and Codex agents, repository maintainers in Liminal Commons.
- **Review Cadence:** Charter revisit quarterly; protocol/awareness reviews on major iteration or adoption wave.

## 5. Lifecycle Plan
- **MVP Milestones:**  
  - M1: Publish SAP document set (charter, spec, awareness guide, blueprint, ledger).  
  - M2: Pilot installation in at least one additional repository beyond chora-base.  
  - M3: Collect feedback, update protocol/guide, and share ecosystem-wide announcement.
- **Open Questions:**  
  1. How should ledger updates integrate with existing status dashboards?  
  2. Do we need automation scripts for bulk adoption, or is manual adoption sufficient initially?  
  3. What escalation path handles stalled inbox triage?  
- **Sunset Criteria:** Package becomes obsolete if ecosystem consolidates into monorepo or adopts centralized orchestration tool; otherwise evolves into status protocol successor for v2.0.

