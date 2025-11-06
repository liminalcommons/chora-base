---
id: intention-inventory-{date}
type: intention-inventory
sources:
  inbox: 0
  github: 0
  dogfooding: 0
  research: 0
  a-mem: 0
tags: [intention-discovery, strategic-planning, backlog-refinement]
created: YYYY-MM-DDTHH:MM:SSZ
updated: YYYY-MM-DDTHH:MM:SSZ
---

# Intention Inventory - {Date}

## Overview

**Purpose**: This inventory consolidates scattered unfulfilled user intentions from multiple sources into a single document for strategic analysis and prioritization.

**Date**: {YYYY-MM-DD}

**Total Intentions**: {N}

**Evidence Distribution**:
- **High-Evidence (Level A)**: {N} ({XX}%)
- **Medium-Evidence (Level B)**: {N} ({XX}%)
- **Low-Evidence (Level C)**: {N} ({XX}%)

---

## Sources

| Source | Count | Description |
|--------|-------|-------------|
| **Inbox** | {N} | Coordination requests from `inbox/coordination/active.jsonl` |
| **GitHub** | {N} | Feature requests and issues with `label:feature-request` |
| **Dogfooding** | {N} | Feedback from SAP pilot usage (SAP-027) |
| **Research** | {N} | Industry research, standards, peer-reviewed papers |
| **A-MEM** | {N} | Knowledge notes with tags `user-request`, `feature-idea` |

**Total**: {N} unfulfilled intentions

---

## Evidence Level Definitions

### Level A: Standards & Research (High-Evidence)
- **IETF RFCs**: Internet standards (e.g., RFC 7519 for JWT)
- **W3C Specifications**: Web standards (e.g., WCAG 2.1 for accessibility)
- **ISO Standards**: Industry standards (e.g., ISO 27001 for security)
- **PEPs** (Python Enhancement Proposals): Python language standards
- **Peer-Reviewed Research**: Academic papers, systematic reviews
- **Production Data**: Direct measurements from production systems

### Level B: Case Studies & Industry Practice (Medium-Evidence)
- **Industry Case Studies**: Real-world implementations with documented outcomes (>100 users)
- **Production Usage**: Battle-tested patterns in ecosystem projects
- **Expert Consensus**: Multiple experts agreeing (e.g., PM best practices)
- **Framework Documentation**: Official recommendations from major frameworks
- **Ecosystem Patterns**: Widely adopted patterns in relevant ecosystems

### Level C: Expert Opinion & Blogs (Low-Evidence)
- **Blog Posts**: Individual developer perspectives
- **Expert Opinions**: Single expert recommendations without empirical backing
- **Single-User Requests**: Feature requests from individual users
- **Experimental Patterns**: Not yet validated in production
- **Anecdotal Evidence**: "I heard this works" without data

---

## High-Evidence Intentions (Level A: Standards, Research)

### {N}. {Intention Title}

**Source**: {inbox | github | dogfooding | research | a-mem}

**Evidence**:
- {Citation 1 - e.g., "IETF RFC XXXX - Standard Name"}
- {Citation 2 - e.g., "Peer-reviewed paper: Authors (Year), Journal"}
- {Production data - e.g., "Measured 40% time savings in chora-compose"}

**User Demand**: {N} explicit requests from {sources}

**Description**: {2-3 sentence description of the intention}

**Related SAPs**: {SAP-XXX, SAP-YYY}

**Priority**: HIGH | MEDIUM | LOW

**Recommended Wave**: Wave 1 | Wave 2 | Wave 3

---

### {N}. {Intention Title}

**Source**: {source}

**Evidence**:
- {Citation}

**User Demand**: {N} requests

**Description**: {Description}

**Related SAPs**: {SAP-XXX}

**Priority**: HIGH

**Recommended Wave**: Wave 1

---

## Medium-Evidence Intentions (Level B: Case Studies)

### {N}. {Intention Title}

**Source**: {source}

**Evidence**:
- {Case study citation - e.g., "Production usage in X projects (200+ users)"}
- {Framework docs - e.g., "Next.js official recommendation (2024)"}

**User Demand**: {N} requests

**Description**: {Description}

**Related SAPs**: {SAP-XXX}

**Priority**: MEDIUM | LOW

**Recommended Wave**: Wave 2 | Wave 3

---

### {N}. {Intention Title}

**Source**: {source}

**Evidence**:
- {Case study}

**User Demand**: {N} requests

**Description**: {Description}

**Related SAPs**: {SAP-XXX}

**Priority**: MEDIUM

**Recommended Wave**: Wave 2

---

## Low-Evidence Intentions (Level C: Expert Opinion)

### {N}. {Intention Title}

**Source**: {source}

**Evidence**:
- {Blog post citation - e.g., "Author Name (2024) - Blog Title"}
- {Expert opinion - e.g., "Recommended by [Expert] based on experience"}

**User Demand**: {N} requests

**Description**: {Description}

**Related SAPs**: {SAP-XXX}

**Priority**: LOW

**Recommended Wave**: Wave 3 | Defer

---

### {N}. {Intention Title}

**Source**: {source}

**Evidence**:
- {Single-user request}

**User Demand**: 1 request

**Description**: {Description}

**Related SAPs**: {SAP-XXX}

**Priority**: LOW

**Recommended Wave**: Defer (insufficient evidence and demand)

---

## Analysis Summary

### Evidence Distribution

| Evidence Level | Count | Percentage | Threshold Met? |
|----------------|-------|------------|----------------|
| Level A (Standards) | {N} | {XX}% | {✅/❌} |
| Level B (Case Studies) | {N} | {XX}% | {✅/❌} |
| **Total A+B** | {N} | {XX}% | {✅ if ≥60%, ❌ if <60%} |
| Level C (Opinion) | {N} | {XX}% | N/A |

**Quality Bar**: {XX}% of intentions have Level A+B evidence (target: ≥60% for Wave 2, ≥70% for Wave 1)

---

### Top 5 Strategic Themes (by Evidence × Demand)

**Methodology**: Ranked by `(evidence_score × user_demand_count × roi_potential)`

1. **{Theme Name}**: {N} intentions, {XX}% A+B, {N} user requests → **Recommend Wave {1|2|3}**
2. **{Theme Name}**: {N} intentions, {XX}% A+B, {N} user requests → **Recommend Wave {1|2|3}**
3. **{Theme Name}**: {N} intentions, {XX}% A+B, {N} user requests → **Recommend Wave {1|2|3}**
4. **{Theme Name}**: {N} intentions, {XX}% A+B, {N} user requests → **Recommend Wave {1|2|3}**
5. **{Theme Name}**: {N} intentions, {XX}% A+B, {N} user requests → **Recommend Wave {1|2|3}**

---

### Recommendations for Vision Synthesis

**Wave 1 Candidates** (Committed - 3 months):
- {Theme X}: {XX}% A+B evidence, {N} user requests, {X}x ROI potential
- {Theme Y}: {XX}% A+B evidence, {N} user requests, {X}x ROI potential

**Wave 2 Candidates** (Exploratory - 6 months):
- {Theme X}: {XX}% A+B evidence, {N} user requests, needs validation via dogfooding
- {Theme Y}: {XX}% A+B evidence, {N} user requests, needs more production data

**Wave 3 / Deferred**:
- {Theme X}: {XX}% A+B evidence (below 60%), {N} user requests (insufficient demand)
- {Theme Y}: Single-user request, insufficient evidence

---

## Next Steps

1. **Create Strategic Theme Matrix**: Use `strategic-theme-matrix-template.md` to cluster these intentions into themes
2. **Analyze Themes**: Calculate evidence × demand × ROI for each theme
3. **Draft Vision**: Use `vision-document-template.md` to create multi-wave vision from prioritized themes
4. **Review & Refine**: Validate wave assignments with stakeholders
5. **Cascade to Backlog**: Create roadmap milestones and beads epics for Wave 1

---

## Changelog

### {YYYY-MM-DD} - Inventory Created
- Scanned {N} sources ({inbox, github, dogfooding, research, a-mem})
- Catalogued {N} unfulfilled intentions
- Evidence distribution: {XX}% A, {XX}% B, {XX}% C
- Top theme: {Theme Name} ({N} intentions, HIGH priority)

### {YYYY-MM-DD} - Quarterly Review
- {Record updates to intention status, new intentions, closed intentions}

---

## Example: Chora-Base Intention Inventory (Nov 2025)

**Note**: This example shows how the template is used in practice.

---
id: intention-inventory-2025-11-05
type: intention-inventory
sources:
  inbox: 4
  github: 12
  dogfooding: 3
  research: 8
  a-mem: 15
tags: [intention-discovery, strategic-planning, backlog-refinement]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Intention Inventory - 2025-11-05

**Total Intentions**: 42

**Evidence Distribution**:
- **High-Evidence (Level A)**: 14 (33%)
- **Medium-Evidence (Level B)**: 18 (43%)
- **Low-Evidence (Level C)**: 10 (24%)

## High-Evidence Intentions (Level A)

### 1. Strategic Planning Workflow

**Source**: Research (PM methodologies), inbox coordination requests

**Evidence**:
- PM best practices: OKRs, roadmapping (Level A - industry standards)
- 4 explicit inbox coordination requests (2025-10 to 2025-11)
- Production validation: Used in 3 ecosystem projects

**User Demand**: 4 explicit requests in inbox, 10 GitHub feature requests

**Description**: Comprehensive workflow for consolidating scattered intentions → strategic themes → multi-wave vision → backlog cascade. Addresses the "scattered unfulfilled intentions" problem identified across ecosystem.

**Related SAPs**: SAP-006 (Development Lifecycle), SAP-010 (Memory System), SAP-015 (Task Tracking), SAP-027 (Dogfooding Patterns)

**Priority**: HIGH

**Recommended Wave**: Wave 1 (evidence 79% A+B, strong user demand, foundational capability)

---

### 2. OIDC Trusted Publishing for PyPI

**Source**: Research (PyPI documentation, PEP 740)

**Evidence**:
- PEP 740: Attestations require trusted publishing (Level A - Python standard)
- PyPI documentation: OIDC introduced 2023 as recommended default
- Security best practice: Eliminates long-lived tokens

**User Demand**: 3 developers requesting (security concern)

**Description**: Replace manual PyPI token publishing with OIDC trusted publishing via GitHub Actions. Improves security posture and aligns with Python ecosystem best practices.

**Related SAPs**: SAP-028 (Publishing Automation)

**Priority**: HIGH

**Recommended Wave**: Wave 1 (standards-based, security improvement)

---

## Medium-Evidence Intentions (Level B)

### 3. MCP Server Testing Patterns

**Source**: Dogfooding (chora-compose, mcp-n8n), MCP ecosystem discussions

**Evidence**:
- Production usage in 2 projects (chora-compose, mcp-n8n) (Level B - case studies)
- FastMCP examples show testing patterns
- 8 developers in MCP ecosystem requesting guidance

**User Demand**: 8 developers requesting

**Description**: Standardized testing patterns for MCP servers including tool invocation mocking, prompt testing, and integration testing with Claude Desktop/Code.

**Related SAPs**: SAP-014 (MCP Server Development)

**Priority**: MEDIUM

**Recommended Wave**: Wave 2 (validate via dogfooding before ecosystem commitment)

---

## Low-Evidence Intentions (Level C)

### 4. Advanced Jinja Templating Features

**Source**: Single user request (GitHub issue #142)

**Evidence**:
- Blog post: "Jinja best practices" (2024) (Level C - expert opinion)
- Single user request (insufficient demand)

**User Demand**: 1 request

**Description**: Add advanced Jinja features like custom filters, macros, and template inheritance to SAP generation workflow.

**Related SAPs**: SAP-029 (SAP Generation)

**Priority**: LOW

**Recommended Wave**: Defer (insufficient evidence and demand, 50% A+B)

---

## Analysis Summary

**Top 5 Themes**:
1. Strategic Planning (14 intentions, 79% A+B, 4 inbox + 10 GitHub) → Wave 1
2. Testing & Quality (8 intentions, 75% A+B, 8 developers) → Wave 1
3. MCP Integration (6 intentions, 83% A+B, 8 developers) → Wave 2
4. Performance (5 intentions, 60% A+B, 3 users) → Wave 2
5. Documentation (4 intentions, 50% A+B, 2 users) → Wave 3

---

## Usage Instructions

### How to Use This Template

1. **Copy Template**:
   ```bash
   cp .chora/memory/templates/intention-inventory-template.md \
      .chora/memory/knowledge/notes/intention-inventory-$(date +%Y-%m-%d).md
   ```

2. **Scan Sources** (monthly):
   ```bash
   # Inbox coordination requests
   cat inbox/coordination/active.jsonl | jq -r '.request'

   # GitHub feature requests
   gh issue list --label feature-request --state open

   # Dogfooding feedback
   grep '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md

   # Research reports
   ls docs/research/*-research.md

   # A-MEM user requests
   grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md
   ```

3. **Fill Frontmatter**:
   - Update `id` with current date
   - Count intentions per source, update `sources` object
   - Set `created` and `updated` timestamps

4. **Categorize by Evidence Level**:
   - **Level A**: Standards (RFCs, PEPs, ISO), peer-reviewed research, production data
   - **Level B**: Case studies (>100 users), ecosystem patterns, expert consensus
   - **Level C**: Blog posts, single-user requests, expert opinions

5. **For Each Intention**:
   - Title (descriptive)
   - Source (which source this came from)
   - Evidence (cite standards, papers, case studies)
   - User demand (count explicit requests)
   - Description (2-3 sentences)
   - Related SAPs
   - Priority (HIGH/MEDIUM/LOW)
   - Recommended Wave (1/2/3 based on evidence + demand)

6. **Calculate Evidence Distribution**:
   - Count Level A, B, C intentions
   - Calculate percentages
   - Check if total A+B ≥ 60% (quality bar for Wave 2) or ≥ 70% (Wave 1)

7. **Identify Top 5 Themes**:
   - Group intentions by strategic theme
   - Rank by (evidence % × user demand count × ROI potential)
   - Recommend wave assignment for each theme

8. **Next Step**: Create strategic theme matrix using `strategic-theme-matrix-template.md`

### Integration with Other Templates

**Inputs** (sources for intentions):
- `inbox/coordination/active.jsonl`
- GitHub issues with `label:feature-request`
- Knowledge notes with tags `dogfooding-feedback`, `user-request`
- Research documents in `docs/research/`

**Outputs** (created from this inventory):
- `strategic-themes-{date}.md` - Theme clustering and analysis
- `vision-{project}-{horizon}.md` - Vision document with wave assignments

### When to Update Inventory

**Monthly**: Create new intention inventory to capture new requests

**After Strategic Theme Analysis**: Update with theme assignments

**After Vision Synthesis**: Mark intentions as addressed in Wave 1/2/3

**Quarterly Review**: Archive old intentions, validate evidence levels still accurate
