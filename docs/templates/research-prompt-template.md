# Software Engineering Best Practices Research Prompt Template

**Version**: 1.0.0
**Last Updated**: 2025-11-04
**Compatible With**: Claude Code, Claude Desktop, GPT-4+
**Output**: research-report.md (10-20 pages) + checklists.md (2-3 pages)

---

## Quick Start

This template generates comprehensive, evidence-based research reports on software engineering best practices and first principles. Fill in the parameters below, then execute the prompt using your AI assistant (Claude Code WebSearch, GPT-4, etc.).

### Usage

1. **Fill Parameters**: Replace all `{placeholder}` values with your context
2. **Execute Prompt**: Copy the filled prompt to your AI assistant
3. **Review Output**: Validate evidence levels (Level A ≥30%, Level B ≥40%, Level C ≤30%)
4. **Save Report**: Store in `docs/research/{topic}-research.md`
5. **Integrate**: Use research findings in capability charters, ADRs, protocol specs

---

## Full Research Prompt (Copy & Fill)

```markdown
**Context & Goal**
You are a meticulous research analyst. Produce a practitioner-ready report on **best practices and first principles of software engineering** tailored to the context below.

**My Context**

* Organization / team: `{org_size_and_type}` (e.g., 30-engineer product org; multiple cross-functional squads)
* Domain: `{domain}` (e.g., fintech web + mobile, open-source framework, internal tooling)
* Tech stack: `{stack}` (e.g., TypeScript/Node, React, Postgres, Kubernetes on AWS)
* Constraints: `{constraints}` (e.g., SOC 2, HIPAA, EU data residency, tight release cycles, open-source license)
* Audience & depth: `{audience}` (e.g., CTO + Staff Engineers; hands-on depth)
* Time horizon: `{time_horizon}` (e.g., next 6–12 months adoption)

**Deliverables**

1. A **10–20 page report** with:

   * **Executive summary**: 10–12 bullet takeaways, "what to adopt now vs later."
   * **Principles** (the why): e.g., modularity, cohesion/coupling, KISS, YAGNI, DRY, SOLID, design-by-contract, 12-factor, reliability, safety, security, privacy-by-design, observability, operability, cost awareness.
   * **Practices** (the how): requirements, architecture, API design & versioning, data modeling/migrations, code review, testing strategy (pyramid + property-based + fuzz), CI/CD, trunk-based dev, branch strategies, release/rollback, feature flags, infra-as-code, change management, incident response/postmortems, SRE/SLI/SLO error budgets, documentation, tech-debt management, performance engineering, secure SDLC, compliance mapping.
   * **Quality attributes**: maintainability, reliability, scalability, performance, security, portability, usability—define and tie to measurable outcomes.
   * **Decision playbooks**: monolith vs microservices; synchronous vs async; REST vs gRPC; schema evolution; cloud tenancy; build vs buy. Provide "choose-x-when…" guidance.
   * **Metrics & targets**: DORA (lead time, deploy frequency, change failure rate, MTTR), code health signals, reliability (SLOs), security (vuln SLAs), cost (unit economics), data quality.
   * **Anti-patterns**: e.g., excessive branching/long-lived PRs, flaky tests, premature microservices, cargo-cult tooling, "test coverage worship," unbounded queues, hidden data coupling.
   * **Risk register**: top 10 risks, likelihood/impact, mitigations.
   * **Implementation roadmap**: 90-day/6-month plan with owners, dependencies, and expected KPI deltas.

2. **Checklists**: code review, release, incident, threat modeling, readiness to run (prod checklist).

3. **One-page summary**: for execs.

4. **Appendix**: annotated bibliography + glossary.

**Method & Evidence Requirements**

* **Prioritize primary sources and standards** (e.g., ISO/IEC/IEEE software lifecycle & quality standards; SRE/DORA research; OWASP; NIST), peer-reviewed literature, and reputable industry reports. Distinguish **evidence level**:

  * Level A: standards, peer-reviewed/meta-analyses, large-n studies
  * Level B: well-documented industry case studies/postmortems
  * Level C: expert essays/blogs with limited data

* For each major recommendation, include **at least one Level A or B citation**. Provide **direct quotes** (1–3 sentences max) for pivotal claims with page/section anchors.

* Note **controversies** (e.g., TDD effectiveness, microservices vs modular monolith, GitFlow vs trunk-based); present balanced "works-best-when" conditions.

* Prefer **recent sources** (last 5–7 years) and call out when older but canonical sources are cited.

**Structure & Formatting**

* Write for **practitioners**: concise, unambiguous, avoid buzzwords. Use RFC-2119 verbs (MUST/SHOULD/MAY) in checklists and policies.

* Provide **tables** for: metrics, trade-offs, tooling options, and roadmap.

* Include **"Adopt / Trial / Assess / Hold"** tags next to practices (Technology-Radar style).

* Output two artifacts:
  * `report.md` – the full narrative
  * `checklists.md` – all checklists grouped by lifecycle stage

**Scope Cues**

* Emphasize practices that move the chosen metrics (e.g., reduce lead time, raise SLO compliance).

* Include **security & privacy-by-design** throughout: threat modeling, SBOMs, SCA, secrets mgmt, least privilege, secure defaults, SDL activities at each phase.

* Cover **operational excellence**: runbooks, progressive delivery (blue/green, canaries), rollback strategies, error budgets, on-call health, incident reviews.

* Address **data**: schema versioning, migrations, backward compatibility, data contracts, retention, governance.

**Output Checklist (Researcher Must Confirm in Final Section)**

* [ ] All claims map to citations with dates and links
* [ ] Evidence levels labeled A/B/C
* [ ] Clear "when not to use" notes for each practice
* [ ] A 90-day plan that is feasible within `{constraints}`
* [ ] KPIs have baseline → target deltas and measurement method
* [ ] Glossary defines all acronyms
* [ ] Accessibility, privacy, compliance requirements integrated (not a separate bolt-on)

**Customization Parameters**

* `{org_size_and_type}`: {FILL THIS}
* `{domain}`: {FILL THIS}
* `{stack}`: {FILL THIS}
* `{constraints}`: {FILL THIS}
* `{audience}`: {FILL THIS}
* `{time_horizon}`: {FILL THIS}
* Optional emphases: `{e.g., reliability-first, cost-first, compliance-first}` {FILL THIS}

**Tone & Style**

* Direct, neutral, decision-oriented. Provide examples and short code/config snippets **only** when they clarify a principle or practice.

**Final Section to Include**

* "Top 20 Practices to Adopt Now" (ranked, with effort/impact matrix)
* "What We Stop Doing" list (anti-practices to sunset)
* "Open Questions & Risks" with proposed experiments
```

---

## Quick Prompt (One-Paragraph Version)

For faster execution, use this condensed version:

```markdown
Research and write a practitioner-ready report on the best practices and first principles of software engineering for `{org_size_and_type}` working in `{domain}` using `{stack}` under `{constraints}`. Cover principles (why) and practices (how) across requirements, architecture, code quality, testing, CI/CD, release, operations/SRE, security/privacy, data, and documentation. Include decision playbooks (monolith vs microservices, API design/versioning, schema evolution), metrics (DORA, reliability/SLOs, security SLAs, cost), anti-patterns, and a 90-day/6-month adoption roadmap. Cite primary/standards and peer-reviewed or large case-study sources, label evidence levels, call out controversies with "works-best-when," and provide checklists for code review, release, incident response, and threat modeling. Deliver `report.md` + `checklists.md`, concise, with an executive summary and annotated bibliography.
```

---

## Parameter Guidelines

### `{org_size_and_type}`
- **Examples**: "5-person startup", "30-engineer product org", "200-engineer platform team", "open-source project with 50 contributors"
- **What to include**: Team size, structure (e.g., squads, guilds), maturity (startup vs established)

### `{domain}`
- **Examples**: "fintech web + mobile", "B2B SaaS", "internal tooling", "open-source framework", "healthcare HIPAA-compliant apps"
- **What to include**: Industry, compliance requirements, user base

### `{stack}`
- **Examples**: "TypeScript/Node, React, Postgres, Kubernetes on AWS", "Python/Django, PostgreSQL, Docker, GitHub Actions", "Next.js 15, Vite 7, SQLite, Vercel"
- **What to include**: Languages, frameworks, databases, infrastructure, CI/CD tools

### `{constraints}`
- **Examples**: "SOC 2, HIPAA, EU data residency", "tight release cycles (daily deploys)", "open-source license (MIT)", "budget-constrained (serverless-first)"
- **What to include**: Compliance, velocity, licensing, cost constraints

### `{audience}`
- **Examples**: "CTO + Staff Engineers; hands-on depth", "Mid-level engineers; tutorial-style", "Product team; high-level overview"
- **What to include**: Who reads the report, desired depth

### `{time_horizon}`
- **Examples**: "next 6–12 months adoption", "next quarter (3 months)", "long-term (18-24 months)"
- **What to include**: Implementation timeline

---

## Evidence Level Criteria

Use these criteria to validate research output quality:

### Level A: Standards and Peer-Reviewed
- **Sources**: ISO/IEC/IEEE standards, NIST, OWASP, W3C, IETF RFCs, peer-reviewed journals (ACM, IEEE), DORA State of DevOps
- **Examples**: "ISO/IEC 25010 quality model", "NIST Cybersecurity Framework", "DORA 2024 Accelerate State of DevOps Report"
- **Target**: ≥30% of citations

### Level B: Industry Case Studies
- **Sources**: Well-documented case studies from established companies, postmortems from major incidents, technical blogs from industry leaders (Google, Meta, Netflix, etc.), conference talks with data
- **Examples**: "Google SRE Book", "Netflix Chaos Engineering blog", "Stripe incident postmortem"
- **Target**: ≥40% of citations

### Level C: Expert Opinion
- **Sources**: Expert essays, blog posts without data, opinion pieces, "best practices" without evidence
- **Examples**: Medium articles, personal blogs, Twitter threads
- **Target**: ≤30% of citations

---

## Output Validation Checklist

Before using research report, validate:

- [ ] **Evidence levels**: Level A ≥30%, Level B ≥40%, Level C ≤30%
- [ ] **Citations**: All major claims have at least one Level A or B citation
- [ ] **Direct quotes**: Pivotal claims include 1-3 sentence quotes with page/section anchors
- [ ] **Controversies noted**: TDD, microservices, GitFlow, etc. have "works-best-when" conditions
- [ ] **Decision playbooks**: Include "choose-x-when…" guidance
- [ ] **Metrics defined**: DORA, SLOs, security SLAs have baseline → target deltas
- [ ] **Anti-patterns listed**: At least 5 anti-patterns with explanations
- [ ] **Risk register**: Top 10 risks with likelihood/impact/mitigations
- [ ] **90-day plan**: Actionable roadmap with owners, dependencies, KPI deltas
- [ ] **Checklists actionable**: Code review, release, incident, threat modeling
- [ ] **Executive summary**: 10-12 bullet takeaways
- [ ] **Glossary**: All acronyms defined

---

## Integration with Chora-Base SAPs

### SAP-027 (Dogfooding Patterns): Week 0 Research Phase

**When**: Before starting 5-week pilot (build weeks 1-3, validate week 4, decide week 5)

**How**:
1. Fill research template with SAP domain context
2. Execute prompt (15-30min research)
3. Generate `docs/research/{sap-name}-research.md`
4. Extract principles for pilot planning

**Example**:
```bash
# Research SAP-030 (database-migrations) before pilot
just research "database migration best practices for Python projects"
# Output: docs/research/database-migrations-research.md
# Extract: Rollback strategies (Level A: Flyway docs), state tracking (Level B: Alembic case studies)
# Use in Week 1-3 pilot build
```

### SAP-029 (SAP Generation): Step 0 Research

**When**: Before adding SAP to `sap-catalog.json`

**How**:
1. Fill research template with capability domain
2. Execute prompt
3. Extract problem/solution/principles for `sap-catalog.json` generation
4. Use decision playbooks for protocol-spec.md integration patterns

**Example**:
```bash
# Before creating SAP-033 (authentication)
just research "authentication best practices: OAuth2, OIDC, passkeys for web apps"
# Output: docs/research/authentication-research.md
# Extract principles → sap-catalog.json generation.principles field
# Extract decision playbooks → protocol-spec.md Section 5 (Integration with Other SAPs)
```

### SAP-003 (Project Bootstrap): Tech Stack Evaluation

**When**: Before choosing tech stack for bootstrap template

**How**:
1. Fill research template for tech stack comparison
2. Execute prompt
3. Use decision playbooks to justify template choices
4. Cite research in awareness-guide.md

**Example**:
```bash
# Evaluate React frameworks
just research "React SSR frameworks comparison: Next.js 15, Remix, Vite SSR"
# Output: docs/research/react-framework-comparison.md
# Use in SAP-003 awareness-guide.md: "Why Next.js 15? See research report..."
```

### SAP-005 (CI/CD Workflows): Pipeline Architecture Research

**When**: Before designing CI/CD workflows

**How**:
1. Fill research template for CI/CD best practices
2. Execute prompt
3. Extract DORA metrics, deployment strategies
4. Cite research in capability-charter.md evidence section

**Example**:
```bash
# Research CI/CD patterns
just research "CI/CD best practices: GitHub Actions, trunk-based development, DORA metrics"
# Output: docs/research/cicd-research.md
# Cite in SAP-005 capability-charter.md Section 1 (Problem Statement): "Level A: DORA 2024 report shows..."
```

---

## Optional Toggles

Append these to the full prompt as needed:

### Strict Citation Format
```markdown
**Citation Format**: Use APA with links; include publication year and page/section numbers.
```

### Jurisdictional Compliance
```markdown
**Compliance Mapping**: Map recommendations to `{frameworks}` (e.g., SOC 2, ISO 27001, HIPAA, PCI DSS), indicating which controls each practice supports.
```

### Tooling Neutrality
```markdown
**Tooling Guidance**: Discuss categories and selection criteria; avoid vendor lock-in recommendations unless explicitly justified.
```

### Maturity Model
```markdown
**Maturity Assessment**: Score current vs target maturity (1–5) per domain; include heatmap and transition steps.
```

### Budget Guardrail
```markdown
**Budget Constraint**: Cap recommendations to `{budget}` in tooling/infra changes; favor process/practice improvements first.
```

### Enterprise Appendix
```markdown
**Change Management**: Add change-management plan, RACI, and communication rhythms.
```

---

## Example Filled Prompt (Chora-Base Context)

```markdown
**Context & Goal**
You are a meticulous research analyst. Produce a practitioner-ready report on **best practices and first principles of software engineering** tailored to the context below.

**My Context**

* Organization / team: `Open-source framework project with 1 core maintainer, 5-10 contributors`
* Domain: `Developer tooling, AI-assisted development, SAP framework`
* Tech stack: `TypeScript/Node, React, Next.js 15, Vite 7, Python, pytest, GitHub Actions, Vercel`
* Constraints: `MIT license, open-source friendly, budget-constrained (serverless-first), Claude Code integration`
* Audience & depth: `Open-source contributors + downstream adopters; hands-on depth`
* Time horizon: `Next 6–12 months adoption`

[... rest of full prompt ...]

**Customization Parameters**

* `{org_size_and_type}`: Open-source framework project with 1 core maintainer, 5-10 contributors
* `{domain}`: Developer tooling, AI-assisted development, SAP framework
* `{stack}`: TypeScript/Node, React, Next.js 15, Vite 7, Python, pytest, GitHub Actions, Vercel
* `{constraints}`: MIT license, open-source friendly, budget-constrained (serverless-first), Claude Code integration
* `{audience}`: Open-source contributors + downstream adopters; hands-on depth
* `{time_horizon}`: Next 6–12 months adoption
* Optional emphases: `Reliability-first, agent-first design, progressive enhancement`
```

---

## Justfile Integration

Add this recipe to your `justfile`:

```just
# Generate research report for a topic
research topic:
    @echo "📚 Generating research report for: {{topic}}"
    @echo "📄 Using template: docs/templates/research-prompt-template.md"
    @echo "💡 Next steps:"
    @echo "  1. Open docs/templates/research-prompt-template.md"
    @echo "  2. Fill in the {parameters} with your context"
    @echo "  3. Copy the filled prompt to Claude Code or your AI assistant"
    @echo "  4. Execute using WebSearch/WebFetch tools"
    @echo "  5. Save output to docs/research/{{topic}}-research.md"
    @echo ""
    @echo "📂 Output location: docs/research/{{topic}}-research.md"
    @mkdir -p docs/research
```

---

## Version History

- **1.0.0** (2025-11-04): Initial research prompt template for chora-base
  - Full prompt (10-20 page reports)
  - Quick prompt (one-paragraph)
  - Evidence level criteria (Level A/B/C)
  - Integration with SAP-027, SAP-029, SAP-003, SAP-005
  - Validation checklist
  - Optional toggles

---

## Support & Resources

### Related SAPs

- **SAP-027** (dogfooding-patterns): Week 0 research phase
- **SAP-029** (sap-generation): Step 0 research before generation
- **SAP-003** (project-bootstrap): Tech stack evaluation research
- **SAP-005** (ci-cd-workflows): CI/CD research for pipeline architecture

### Example Research Reports

Once created, example reports will be available at:
- `docs/research/database-migrations-research.md`
- `docs/research/authentication-research.md`
- `docs/research/react-framework-comparison.md`

### Feedback

If you use this template, please provide feedback:
- Did the research report help your decision-making?
- Were evidence levels adequate (Level A ≥30%)?
- Were decision playbooks actionable?
- What could be improved?

Add feedback to the SAP ledger that used the research (e.g., SAP-027 ledger, SAP-029 ledger).

---

**Next Steps**:
1. Fill in the parameters for your research topic
2. Execute the prompt using Claude Code WebSearch or your AI assistant
3. Save the output to `docs/research/{topic}-research.md`
4. Use the research findings in your SAP creation or architecture decisions
5. Provide feedback to improve the template

Happy researching! 🔬
