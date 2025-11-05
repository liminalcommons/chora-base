# Research Reports

This directory contains evidence-based research reports generated using the research prompt template.

## Purpose

Research reports provide Level A/B/C evidence for:
- SAP creation (pre-pilot research for SAP-027, pre-generation research for SAP-029)
- Architecture decisions (ADRs)
- Tech stack evaluation (SAP-003 bootstrap decisions)
- CI/CD pipeline design (SAP-005 workflow architecture)

## Template

See [docs/templates/research-prompt-template.md](../templates/research-prompt-template.md) for the research prompt template.

## Usage

```bash
just research "your-topic-here"
```

## Format

Each research report should follow this structure:
- **Executive Summary**: 10-12 bullet takeaways
- **Principles**: The "why" (modularity, SOLID, 12-factor, etc.)
- **Practices**: The "how" (architecture, testing, CI/CD, etc.)
- **Decision Playbooks**: "Choose X when..." guidance
- **Metrics & Targets**: DORA, SLOs, security SLAs
- **Anti-Patterns**: What to avoid
- **Risk Register**: Top 10 risks with mitigations
- **Implementation Roadmap**: 90-day/6-month plan
- **Checklists**: Code review, release, incident, threat modeling
- **Appendix**: Annotated bibliography, glossary

## Evidence Levels

- **Level A** (≥30%): Standards, peer-reviewed, large-n studies
- **Level B** (≥40%): Industry case studies, postmortems
- **Level C** (≤30%): Expert opinion, blogs

## Example Reports

Once created, example reports will appear here:
- `database-migrations-research.md`
- `authentication-research.md`
- `react-framework-comparison.md`

