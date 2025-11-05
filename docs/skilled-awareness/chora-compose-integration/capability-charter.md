# Capability Charter: chora-compose Integration

**SAP ID**: SAP-017
**Version**: 2.0.0
**Status**: active
**Owner**: Victor
**Created**: 2025-11-04
**Last Updated**: 2025-11-04

---

## 1. Problem Statement

### Current Challenge

Projects wanting to adopt chora-compose lack unified integration guide across 4 modalities (pip, MCP, CLI, Docker), unclear adoption paths, and missing role-based workflows.

**Current challenge**: Projects wanting to adopt chora-compose for content generation face significant integration barriers:
- **Modality Confusion**: Which integration path to choose (pip vs MCP vs CLI vs Docker)?
- **Missing Decision Trees**: No guidance on "when to use which modality"
- **Role Ambiguity**: Unclear workflows for developers vs AI agents vs teams
- **Scattered Documentation**: Installation in README, MCP in AGENTS.md, Docker in how-to guides
- **No Adoption Journey**: Missing path from install → first success → production use

**Developers face**:
- 2-4 hours exploring different integration options before finding the right path
- 50-80% choose wrong modality initially and need to restart
- Lack of role-specific guidance (developer path vs AI agent path vs team deployment)
- Missing quick-win examples (time-to-first-success unclear)
- No structured adoption journey from basic to production use

### Evidence

Evidence of adoption friction and blocked projects:

- **COORD-2025-002 coordination request blocked**: chora-base waiting for integration guide to adopt chora-compose Collections for SAP generation
- **SAP-017 identity crisis**: 823 lines of Docker Compose content (wrong tool entirely) - catalog says "chora-compose integration" but file documents container orchestration
- **Documentation scattered across 10+ files**: README, AGENTS.md, multiple how-to guides - no single integration reference
- **Zero decision trees for modality selection**: Users consistently ask "which path is right for me?"
- **Time-to-first-success unclear**: Ranges from 5 minutes (with guide) to 2 hours (without), averaging 45-60 minutes
- **4 modalities undocumented at SAP level**: pip, MCP server, CLI, Docker integration patterns not unified
- **High support burden**: 30-40% of questions are "how do I integrate chora-compose?"

### Business Impact

Without chora-compose Integration:
- **Adoption Friction**: 50-80% of users choose wrong modality, waste time restarting (2-4 hours lost)
- **Wasted Time**: 2-4 hours exploring options vs 30 minutes with guided integration
- **Support Burden**: 30-40% of questions are integration-related, consuming maintainer time
- **Missed Productivity Gains**: 5x+ content generation productivity delayed by adoption complexity
- **Ecosystem Gap**: chora-base SAP generation blocked (COORD-2025-002), preventing 18 SAPs (90 artifacts) bulk generation
- **Developer Frustration**: Poor first experience reduces adoption and community growth
- **Inconsistent Usage**: Without role-based workflows, teams adopt different (often suboptimal) patterns

---

## 2. Proposed Solution

### chora-compose Integration

Comprehensive integration guide with 4 modalities, decision trees for modality selection, role-based workflows (developer/AI agent/team), adoption journey (install → first success → production).

**Key capabilities**:

1. **4 Integration Modalities**
   - **pip (library)**: For Python project integration
   - **MCP server**: For AI agent access (Claude Desktop, Cursor)
   - **CLI (interactive)**: For testing and manual workflows
   - **Docker**: For n8n workflows and team deployment

2. **Decision Trees**
   - "I want to integrate as a library" → pip modality
   - "I want AI agent access" → MCP server modality
   - "I want interactive testing" → CLI modality
   - "I want team deployment or n8n workflows" → Docker modality

3. **Role-Based Workflows**
   - **Developer path**: pip → code integration → generate in Python
   - **AI Agent path**: MCP tools → conversational creation → tool-driven generation
   - **Team Lead path**: Docker deployment → shared configs → collaboration
   - **DevOps path**: n8n integration → automated workflows → CI/CD

4. **Quick Wins (< 30 minutes)**
   - Install → Create first config → Generate content → Validate output
   - Measured from "command 1" to "first generated artifact"
   - All 4 modalities provide <30 min path

5. **Adoption Journey**
   - **Level 1**: Install and first success (Day 1, < 30 min)
   - **Level 2**: Production integration (Week 1, 1-2 days)
   - **Level 3**: Advanced patterns (Month 1, ongoing)

6. **Troubleshooting**
   - Common errors by modality (pip conflicts, MCP config, Docker networking)
   - Diagnostic commands (`chora-compose --version`, `docker ps`, etc.)
   - Resolution workflows (step-by-step fixes)

**Setup time**:
- **Level 1 (Basic)**: 30 minutes (install + first content generation)
- **Level 2 (Production)**: 1-2 days (integrate in real project, team workflows)
- **Level 3 (Advanced)**: 1-2 weeks (multi-modality, advanced patterns, custom configs)

### Key Principles

The following principles guide SAP-017 design and implementation:

- **Modality flexibility**: Support multiple integration paths (pip, MCP, CLI, Docker) to match diverse user needs and environments
- **Role-based guidance**: Provide tailored workflows for different roles (developer, AI agent, team lead, DevOps)
- **Time-to-value optimization**: Minimize time from first encounter to first success (target: <30 minutes)
- **Decision-driven adoption**: Clear decision trees eliminate confusion, guide users to optimal modality
- **Progressive enhancement**: Enable staged adoption (basic → production → advanced) without requiring full commitment upfront

---

## 3. Scope

### In Scope

The following are explicitly included in this SAP:

- **pip integration**: Library usage patterns, installation, Python API usage
- **MCP server deployment**: Docker setup, Claude Desktop config, volume mounts
- **CLI usage**: Interactive commands, config creation wizards, generation workflows
- **Docker deployment**: docker-compose configuration, n8n workflow integration, team access patterns
- **Decision trees**: Modality selection guidance, role-based decision flows
- **Role-based workflows**: Developer, AI agent, team lead, DevOps paths
- **Quick wins (< 30 min)**: Time-to-first-success paths for all modalities
- **Adoption journey**: Install → first success → production integration
- **Troubleshooting**: Common errors, diagnostic commands, resolution workflows
- **Validation**: Verify integration working (smoke tests, example commands)

### Out of Scope

The following are explicitly excluded (see referenced SAPs for coverage):

- **Deep architecture details** → SAP-018 (chora-compose Architecture)
- **Collections patterns** → SAP-031 (Collections Patterns & Anti-Patterns)
- **Custom generator development** → SAP-030 (Generator Selection & Customization)
- **Performance optimization** → SAP-032 (Troubleshooting Runbook)
- **Gateway integration** → Future (Q1 2026)

---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- Install chora-compose via chosen modality (pip/MCP/CLI/Docker)
- Create first content config (YAML or conversational)
- Generate first content piece (validate output exists)
- Time-to-success: < 30 minutes from zero to first generated content
- Validation: `chora-compose --version` works, first artifact generated successfully
- User can answer "which modality did I choose and why?"

**Adoption Success** (Level 2):
- Integrate chora-compose in real project (not toy example)
- Generate production content (documentation, configs, tests, etc.)
- Use 2+ modalities (e.g., MCP for creation + pip for generation)
- Team collaboration (shared configs, version control, documentation)
- Time-to-production: 1-2 days from Level 1 completion
- ROI positive: Productivity ≥2x vs manual content creation
- Usage frequency: ≥1x per week for content generation tasks

**Adoption Success** (Level 3):
- Multi-modality usage (hybrid workflows combining 2+ modalities)
- Advanced patterns (Collections, recursive generation, complex configs)
- Custom configs (domain-specific templates, organization-specific patterns)
- Community contribution (share configs, templates, patterns with ecosystem)
- Time-to-mastery: 1-2 weeks from Level 2 completion
- Productivity: ≥5x vs manual content creation
- Team adoption: ≥80% of team using chora-compose for relevant content tasks

### Key Metrics

| Metric | Baseline (Manual) | Target (Level 2) | Target (Level 3) |
|--------|-------------------|------------------|------------------|
| **Time-to-First-Success** | N/A | < 30 min | < 15 min |
| **Adoption Time** | N/A | 1-2 days | < 1 day |
| **Productivity Multiplier** | 1x | 2-5x | 5-10x |
| **Modality Flexibility** | 0 modalities | 1 modality | 2+ modalities |
| **Developer Satisfaction** | N/A | ≥85% | ≥90% |
| **Integration Success Rate** | N/A | ≥80% | ≥95% |
| **Support Questions** | High | Medium | Low |

---

## 5. Stakeholders

### Primary Stakeholders

**chora-compose Integration Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback and integration reports
  - Coordinate with related SAP owners (SAP-018, SAP-027, SAP-029)
  - Update integration patterns as chora-compose evolves
  - Track adoption metrics and success rates
- **Coordinate with dependencies**: SAP-000 (sap-framework)

**Primary Users**:
- **Python Developers**: Integrating chora-compose in Python projects (pip modality)
- **AI Agents**: Claude Desktop, Cursor users leveraging MCP tools
- **Team Leads**: Setting up shared environments for team collaboration
- **DevOps Engineers**: Deploying chora-compose for n8n workflows and CI/CD
- **Technical Leaders**: Evaluating chora-compose for organizational adoption

### Secondary Stakeholders

**Related SAP Maintainers**:
- **SAP-000 (sap-framework)**: Integration point for SAP structure and protocols
- **SAP-018 (chora-compose Architecture)**: Deep architecture reference for advanced users
- **SAP-027 (dogfooding-patterns)**: Methodology for piloting chora-compose adoption
- **SAP-029 (sap-generation)**: Leverages chora-compose for SAP artifact generation

**Community**:
- chora-base adopters (primary ecosystem users)
- Ecosystem contributors (providing feedback and patterns)
- External users (adopting chora-compose in their own projects)
- MCP ecosystem developers (leveraging MCP server integration)

---

## 6. Dependencies

### Required SAP Dependencies

Required SAPs that MUST be installed before SAP-017:

- **SAP-000 (sap-framework)**: Required for understanding SAP structure (5 artifacts), adoption levels, and SAP protocols. Provides foundation for SAP-017 itself.

### Optional SAP Dependencies

Optional dependencies that enhance SAP-017 usage:

- **SAP-027 (dogfooding-patterns)**: Provides 5-week pilot methodology for structured chora-compose adoption with GO/NO-GO gates
- **SAP-029 (sap-generation)**: Demonstrates chora-compose usage for automated SAP artifact generation (80% time savings)
- **SAP-018 (chora-compose Architecture)**: Deep dive into Collections, MCP tools, generator registry for advanced usage

### External Dependencies

**Required**:
- **Python 3.12+**: Required for pip and CLI modalities
- **Docker Desktop**: Required for MCP server and Docker modalities
- **Git**: Recommended for version control of configs and collaboration
- **chora-compose v1.4.0+**: The tool being integrated (Collections Complete release)

**Optional**:
- **Claude Desktop**: For MCP server AI agent integration
- **Cursor IDE**: Alternative MCP client for AI agent integration
- **n8n**: For workflow automation using Docker modality
- **Poetry or pipenv**: For Python dependency management (alternative to pip)

---

## 7. Constraints & Assumptions

### Constraints

Technical and organizational constraints:

1. **Constraint 1: Python Version Requirement**
   - chora-compose requires Python 3.12+ (async generators, structural pattern matching)
   - Users on older Python versions must upgrade before adoption
   - Impact: May block adoption in environments with strict Python version policies

2. **Constraint 2: Docker Requirement for MCP**
   - MCP server modality requires Docker Desktop installed and running
   - Some environments (corporate, security-restricted) may prohibit Docker
   - Workaround: Use pip or CLI modality instead

3. **Constraint 3: Documentation Scope**
   - SAP-017 covers integration, not deep architecture (see SAP-018)
   - Cannot provide exhaustive troubleshooting (see SAP-032)
   - Focuses on time-to-first-success, not advanced optimization

### Assumptions

Assumptions about users, environment, and capabilities:

1. **Assumption 1: Basic Technical Proficiency**
   - Users have basic command-line skills (cd, ls, running commands)
   - Users understand concepts like "environment variables" and "file paths"
   - Users can edit YAML files and understand basic structure

2. **Assumption 2: Development Environment Access**
   - Users have write access to project directory for output generation
   - Users can install Python packages (pip) or Docker containers
   - Users have internet connection for package downloads

3. **Assumption 3: Clear Use Case**
   - Users adopt chora-compose with specific content generation need in mind
   - Users are motivated to learn and integrate (not passive observers)
   - Users can articulate "what content do I want to generate?"

---

## 8. Risks & Mitigations

### Risk 1: Modality Selection Confusion

**Risk**: Users choose wrong modality, waste time, get frustrated, abandon adoption

**Likelihood**: Medium
**Impact**: High

**Mitigation**:
- Provide clear decision tree in awareness-guide.md and adoption-blueprint.md
- Include "when to use" guidance prominently in each modality section
- Offer interactive selector: "Answer 3 questions → recommended modality"
- Document common wrong choices and how to course-correct

### Risk 2: MCP Server Configuration Complexity

**Risk**: MCP server modality has highest barrier (Docker + config.json + volume mounts), causing high failure rate

**Likelihood**: Medium
**Impact**: Medium

**Mitigation**:
- Provide copy-paste ready config.json examples for Claude Desktop
- Document common Docker issues (volume mount permissions, port conflicts)
- Create troubleshooting section specifically for MCP server setup
- Offer validation commands to confirm MCP server working

### Risk 3: chora-compose Evolution Outpacing Documentation

**Risk**: chora-compose adds features (v1.5.0, v1.6.0), SAP-017 becomes outdated

**Likelihood**: High
**Impact**: Medium

**Mitigation**:
- Version SAP-017 to match chora-compose major versions (v2.0 for chora-compose v1.4+)
- Establish quarterly review cycle for SAP-017 updates
- Monitor chora-compose CHANGELOG for breaking changes or new modalities
- Coordinate with chora-compose maintainers for advance notice of changes

---

## 9. Lifecycle

### Development Phase
**Status**: ✅ **Complete**
**Target Completion**: 2025-11-04

**Milestones**:
- [x] SAP catalog entry created
- [x] capability-charter.md (this document)
- [x] protocol-spec.md (technical contracts)
- [x] awareness-guide.md (AI agent guidance)
- [x] adoption-blueprint.md (installation guide)
- [x] ledger.md (adoption tracking)

### Pilot Phase
**Status**: ⏳ **Planned**
**Target Start**: 2025-11-05
**Duration**: 1-2 weeks

**Activities**:
- Install SAP-017 in chora-base (COORD-2025-002)
- Validate all 4 modalities with test projects
- Measure adoption time (target: <30 min for Level 1)
- Agent execution validation (Claude Desktop using MCP server)
- Collect feedback from chora-base team
- Iterate on decision trees and troubleshooting sections

### Active Phase
**Status**: ⏳ **Planned**
**Target Start**: 2025-11-18

**Ongoing Activities**:
- Quarterly reviews and updates (aligned with chora-compose releases)
- Community feedback integration (GitHub issues, discussions)
- Ledger maintenance (adoption tracking, project usage)
- Integration with SAP-000 (ensure SAP framework consistency)
- Expand modality coverage if new integration paths emerge

### Maintenance Phase

**Maintenance SLA**:
- **Critical issues**: 24-48 hours (e.g., broken installation commands, config errors)
- **Major updates**: 1-2 weeks (e.g., new chora-compose version, new modality)
- **Minor updates**: Quarterly batch updates (documentation improvements, clarifications)
- **Documentation improvements**: Ad-hoc (community PRs, feedback-driven)

---

## 10. Related Documents

### Within chora-base

**SAP Artifacts**:
- [Protocol Specification](./protocol-spec.md) - Technical contracts for 4 integration modalities
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference and decision trees
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step Level 1/2/3 adoption guide
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols
- [SAP-018: chora-compose Architecture](../chora-compose-meta/capability-charter.md) - Deep architecture reference
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/capability-charter.md) - 5-week pilot methodology
- [SAP-029: SAP Generation](../sap-generation/capability-charter.md) - Automated SAP artifact generation

**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

**Official Documentation**:
- [chora-compose README](https://github.com/liminalcommons/chora-compose) - Project overview and quick start
- [chora-compose AGENTS.md](https://github.com/liminalcommons/chora-compose/blob/main/AGENTS.md) - MCP tools documentation
- [chora-compose Documentation](https://github.com/liminalcommons/chora-compose/tree/main/docs) - Comprehensive docs (Diátaxis framework)

**Community Resources**:
- [chora-compose Discussions](https://github.com/liminalcommons/chora-compose/discussions) - Community Q&A and patterns
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification and tools

---

## 11. Approval & Sign-Off

**Charter Author**: Victor
**Date**: 2025-11-04
**Version**: 2.0.0

**Approval Status**: ✅ **Active**

**Review Cycle**:
- **Next Review**: 2026-02-04 (Quarterly)
- **Review Frequency**: Quarterly (aligned with chora-compose release cycle)

**Change Log**:
- 2025-11-04: Complete rewrite (2.0.0) - Victor
  - Replaced Docker Compose content with chora-compose integration guide
  - Added 4 modalities (pip, MCP, CLI, Docker)
  - Added decision trees and role-based workflows
  - Defined Level 1/2/3 success criteria
  - Archived v1.0.0 Docker Compose content

---

**Version History**:
- **2.0.0** (2025-11-04): Complete rewrite - chora-compose integration guide (correct tool)
- **1.0.0** (2025-10-29): Initial charter - Docker Compose orchestration (wrong tool, archived)
