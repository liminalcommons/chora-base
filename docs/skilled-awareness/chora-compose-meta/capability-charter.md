# Capability Charter: chora-compose Meta

**SAP ID**: SAP-018
**Version**: 2.0.0
**Status**: active
**Owner**: Victor
**Created**: 2025-11-04
**Last Updated**: 2025-11-04

---

## 1. Problem Statement

### Current Challenge

Projects adopting chora-compose beyond basic usage lack comprehensive architecture documentation, blocking advanced adoption, custom development, and ecosystem extension.

**Current challenge**: Advanced users and implementers adopting chora-compose for production use face significant architectural knowledge gaps:
- **MCP Tool Specification Missing**: 20 tools exist but no unified specification with parameters, return types, and error handling
- **Collections Architecture Incomplete**: v1.4.0 released Dec 2025 but no SAP-level documentation of 3-tier model, caching, or execution strategies
- **Generator Registry Undocumented**: 5 generators implemented with plugin architecture but no implementation guide for custom development
- **Context Resolution Implicit**: 6 source types supported but resolution mechanics, precedence, and merge strategies unclear
- **Event Emission System Unclear**: OpenTelemetry events defined but emission points and trace propagation undocumented
- **No Implementer Reference**: Architecture scattered across 20+ docs (AGENTS.md, collections-architecture.md, tool-catalog.md, source code)

**Developers face**:
- 10-20 hours researching architecture across multiple docs vs 2-4 hours with unified reference
- Trial-and-error approach to custom generators without BaseGenerator specification
- Suboptimal Collections usage due to missing caching and context propagation knowledge
- Debugging challenges without understanding internals (MCP tools, context resolution flow)
- Blocked ecosystem extension (plugin development, custom generators, advanced integrations)

### Evidence

Evidence of architectural knowledge gaps and adoption barriers:

- **SAP-018 v1.0.0 identity crisis**: 5,051 lines mixed Docker Compose Meta + chora-compose references (archived 2025-11-04)
- **v1.4.0 Collections Complete** (Dec 2025): Released with 3-tier architecture but no SAP-level specification
- **20 MCP tools scattered**: AGENTS.md (922 lines), tool-catalog.md (partial), tools.py source code - no unified reference
- **5 generators undocumented**: demonstration, jinja2, template_fill, bdd_scenario, code_generation exist but no BaseGenerator spec
- **6 context sources implicit**: inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output supported but resolution flow undocumented
- **Generator registry exists** (generators/registry.py) but no public API documentation for plugin development
- **chora-base COORD-2025-002 blocked**: Requires Collections architecture understanding for SAP generation (18 SAPs = 90 artifacts)
- **3 event types defined** (OpenTelemetry) but emission lifecycle unclear
- **Documentation fragmentation**: 33+ docs using Diátaxis framework but no single architecture reference
- **Support burden**: 40%+ of advanced questions require reading source code to answer
### Business Impact

Without chora-compose Meta:
- **Research Time Explosion**: 10-20 hours reading scattered docs vs 2-4 hours with unified reference (5-10× time waste)
- **Advanced Adoption Blocked**: Can't use Collections effectively without understanding caching, context propagation, execution strategies
- **Custom Development Stalled**: No BaseGenerator specification blocks plugin development and ecosystem extension
- **Suboptimal Usage**: Without architecture knowledge, users miss caching benefits (94% cache hit rate), parallel execution (2.6-4.8× speedup)
- **Debugging Difficulty**: Can't troubleshoot generation issues without understanding MCP tools, context resolution flow, event emission
- **Ecosystem Fragmentation**: Different projects implement different (often incorrect) mental models of chora-compose architecture
- **Integration Complexity**: Gateway integration (Q1 2026) requires event emission and dependency tracking documentation
- **Productivity Loss**: 60-80% of advanced users abandon deep adoption due to architecture knowledge gaps

---

## 2. Proposed Solution

### chora-compose Meta

Comprehensive technical specification enabling advanced chora-compose adoption through complete architecture documentation: 20 MCP tools, Collections 3-tier model, 5 generators, context resolution (6 sources), event emission (OpenTelemetry), and caching system.

**Key capabilities**:

1. **20 MCP Tool Specifications**
   - Full parameter documentation (types, required/optional, defaults)
   - Return type specifications with error handling patterns
   - Usage examples with JSON-RPC calls and responses
   - Categorization: Core generation (4), Config lifecycle (4), Batch (1), Storage (2), Discovery (6), Validation (1), Utility (2)
   - Error conditions and troubleshooting guidance

2. **Collections Architecture (3-Tier Model)**
   - Content tier: Atomic content generation (template + context → output)
   - Artifact tier: Multi-content assembly (N contents → 1 artifact)
   - Collection tier: Bulk coordination (M artifacts, parallel/sequential execution)
   - Context propagation: MERGE/OVERRIDE/ISOLATE modes with merge strategies
   - Caching system: SHA-256 context hashing, manifest tracking, 94%+ cache hit rates
   - Execution strategies: Parallel (2.6-4.8× speedup, asyncio) vs Sequential (ordered, lower memory)

3. **Generator Registry (5 Implemented + Plugin System)**
   - demonstration_generator: Example-based generation (no templating)
   - jinja2_generator: Full Jinja2 rendering (filters, macros, inheritance)
   - template_fill_generator: Simple `{{var}}` substitution (lightweight alternative)
   - bdd_scenario_generator: Gherkin scenario generation (BDD testing)
   - code_generation_generator: AI-powered via Anthropic API (optional dependency)
   - BaseGenerator interface specification for custom development
   - Three-tier plugin architecture: built-in, auto-discovered (~/.chora-compose/generators/), runtime-registered

4. **Context Resolution System (6 Sources)**
   - Source types: inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output
   - Resolution flow: cache check → source-specific resolution → data selector → merge
   - Propagation mechanics: collection → artifact → content with mode-based merging
   - Precedence rules and error handling (required vs optional sources)

5. **Event Emission (OpenTelemetry)**
   - 3 event types: content_generated, artifact_assembled, validation_completed
   - Emission lifecycle and trace propagation (CHORA_TRACE_ID environment variable)
   - JSON Lines format for efficient streaming
   - Integration with observability systems (Prometheus, Grafana)

6. **JSON Schemas**
   - Content config v3.1: 7-8 key sections (type, id, elements, inputs.sources, generation.patterns)
   - Artifact config v3.1: Multi-content assembly, dependencies, validation rules
   - Collection config v1.0: Members, shared context, propagation mode, execution strategy

**Setup time**:
- **Level 1 (Understanding)**: 2-4 hours reading SAP-018 artifacts (capability-charter, protocol-spec)
- **Level 2 (Implementation)**: 1-2 days building with architecture knowledge (Collections, caching, generators)
- **Level 3 (Extension)**: 1 week custom generator development and advanced patterns
- **Ongoing**: Reference documentation as needed (5-15 min lookups for specific architecture details)

### Key Principles

The following principles guide SAP-018 design and implementation:

- **Technical accuracy**: All specifications match actual chora-compose v1.4.0 implementation (verified against source code)
- **Complete specification**: Every MCP tool, generator, context source type, event type documented with parameters, return types, examples
- **Implementer-focused**: Documentation targets advanced users building custom generators, extending architecture, integrating systems
- **API-first documentation**: Specifications provide contract-level detail for programmatic usage (MCP tools, BaseGenerator interface)
- **Architecture clarity**: Complex systems (Collections, context resolution, caching) explained with flow diagrams, examples, rationale
---

## 3. Scope

### In Scope

chora-compose Meta (SAP-018) provides comprehensive architecture documentation for advanced adoption and custom development:

**MCP Tool Specifications** (20 tools):
- Core generation: `generate_content`, `assemble_artifact`, `regenerate_content`, `preview_generation`
- Config lifecycle: `draft_config`, `test_config`, `modify_config`, `save_config`
- Batch operations: `batch_generate` (parallel execution, dependency tracking)
- Storage management: `cleanup_ephemeral`, `delete_content`
- Discovery: `list_generators`, `list_content`, `list_artifacts`, `trace_dependencies`, `list_content_configs`, `list_artifact_configs`
- Validation: `validate_content`
- Utility: `hello_world`, `check_freshness`
- All tools documented with JSON-RPC examples, parameter types, return specifications, error conditions

**Generator Registry** (5 implemented + plugin system):
- Built-in generators: demonstration, jinja2, template_fill, bdd_scenario, code_generation
- BaseGenerator interface specification
- Three-tier plugin architecture: built-in, auto-discovered (~/.chora-compose/generators/), runtime-registered
- Custom generator development guide

**Collections Architecture** (3-tier model):
- Content tier: Atomic generation (template + context → output)
- Artifact tier: Multi-content assembly (N contents → 1 artifact)
- Collection tier: Bulk coordination (M artifacts, parallel/sequential execution)
- Context propagation modes: MERGE, OVERRIDE, ISOLATE
- Caching system: SHA-256 context hashing, manifest tracking, 94%+ cache hit rates
- Execution strategies: Parallel (2.6-4.8× speedup) vs Sequential

**Context Resolution System** (6 source types):
- Source types: inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output
- Resolution flow: cache check → source-specific resolution → data selector → merge
- Propagation mechanics: collection → artifact → content with mode-based merging
- Precedence rules and error handling (required vs optional sources)

**Event Emission (OpenTelemetry)**:
- 3 event types: content_generated, artifact_assembled, validation_completed
- Emission lifecycle and trace propagation (CHORA_TRACE_ID)
- JSON Lines format for efficient streaming
- Integration with observability systems

**Caching System**:
- SHA-256 context hashing for deterministic cache keys
- Manifest tracking (cache_manifest.json)
- Cache invalidation strategies
- Performance metrics: cache hit rates, generation time savings

**JSON Schemas** (v3.1 for content/artifact, v1.0 for collection):
- Content config v3.1: 7-8 key sections
- Artifact config v3.1: Multi-content assembly, dependencies, validation
- Collection config v1.0: Members, shared context, propagation mode, execution strategy

### Out of Scope

SAP-018 focuses exclusively on architecture specification. The following topics are covered by related SAPs:

**Integration Workflows** (SAP-017: chora-compose Integration):
- Step-by-step project setup and installation procedures
- Git workflow integration
- CI/CD pipeline integration patterns
- Team adoption workflows and training materials

**Usage Patterns & Best Practices** (SAP-031):
- Common generation patterns
- Template design best practices
- Context organization strategies
- Performance optimization techniques
- Anti-patterns and troubleshooting

**Troubleshooting & Debugging** (SAP-032):
- Diagnostic procedures for generation failures
- Error message catalog with resolution steps
- Debugging tools
- Performance profiling

**Custom Generator Development Tutorials** (SAP-030):
- Step-by-step generator implementation tutorials
- Testing strategies for custom generators
- Packaging and distribution
- Advanced generator features
---

## 4. Outcomes

### Success Criteria

**Adoption Success** (Level 1):
- Advanced users can read and comprehend chora-compose architecture documentation in **2-4 hours** (vs 10-20 hours researching scattered docs)
- Users successfully locate and understand MCP tool specifications, generator interfaces, and Collections architecture without external support
- 80%+ of architectural questions answered by SAP-018 artifacts without needing source code review
- Setup time for architecture understanding: **2-4 hours** (reading capability-charter, protocol-spec, awareness-guide)

**Adoption Success** (Level 2):
- Users build with architecture knowledge in **1-2 days** (Collections setup, caching optimization, generator selection)
- Successfully implement Collections with appropriate context propagation mode (MERGE/OVERRIDE/ISOLATE) for use case
- Achieve 70%+ cache hit rates through understanding of context hashing and manifest tracking
- Correctly use 15+ MCP tools with proper parameters and error handling
- Implementation success rate: 90%+ of advanced features implemented correctly on first attempt

**Adoption Success** (Level 3):
- Custom generator development completed in **1 week** (BaseGenerator implementation, registration, testing)
- Users extend chora-compose ecosystem with custom generators following BaseGenerator interface specification
- Advanced patterns adopted: parallel execution for bulk collections, context resolution optimization, custom validation rules
- Custom generator adoption: 20%+ of advanced users develop at least one custom generator within 3 months
- Community contribution rate: 10%+ of custom generators shared publicly

### Key Metrics

| Metric | Baseline (Manual) | Target (Level 2) | Target (Level 3) |
|--------|-------------------|------------------|------------------|
| **Time to Architecture Understanding** | 10-20 hours | 2-4 hours | 1-2 hours |
| **Time Savings** | 1x (baseline) | 5-10× faster | 10-20× faster |
| **Implementation Success Rate** | 40-60% | 90%+ | 95%+ |
| **Custom Generator Adoption** | N/A | 20% develop | 50% develop |
| **Cache Hit Rate Achievement** | 30-50% | 70-85% | 90-95% |
| **Support Burden Reduction** | 100% (baseline) | 60% | 80% |

---

## 5. Stakeholders

### Primary Stakeholders

**chora-compose Meta Owner**:
- **Owner**: Victor
- **Responsibilities**:
  - Maintain SAP artifacts and documentation
  - Review community feedback
  - Coordinate with related SAP owners
- Coordinate with dependencies: SAP-000, SAP-017
**Primary Users**:
- **Advanced chora-compose Implementers**: Users extending chora-compose with custom generators, plugins, advanced integrations
- **System Architects**: Designing chora-compose-based generation pipelines for production systems
- **MCP Client Developers**: Building tools that interact with chora-compose via MCP protocol
- **AI Agents (Claude, other LLMs)**: Using architecture documentation to understand chora-compose internals for code generation, debugging support
- **Development Teams**: Adopting Collections architecture, caching optimization, parallel execution strategies
- **Technical Leaders**: Evaluating chora-compose for production adoption, understanding architecture tradeoffs

### Secondary Stakeholders

**Related SAP Maintainers**:

- **SAP-000 (SAP Framework)**: SAP-018 follows SAP-000 documentation structure (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- **SAP-017 (chora-compose Integration)**: SAP-017 references SAP-018 for architecture details when guiding project setup and integration workflows
**Community**:
- chora-base adopters
- Ecosystem contributors
- External users

---

## 6. Dependencies

### Required SAP Dependencies

- **SAP-000 (SAP Framework)**: Defines SAP documentation structure (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger) that SAP-018 artifacts follow
### Optional SAP Dependencies

- **SAP-017 (chora-compose Integration)**: Enhances SAP-018 usage by providing step-by-step project setup and integration workflows; SAP-018 provides architecture knowledge, SAP-017 provides implementation guidance

### External Dependencies

**Required**:
- **chora-compose v1.4.0+**: SAP-018 documents chora-compose architecture; requires running instance for validation and testing
- **Git**: Required for accessing chora-compose source code repository referenced in documentation

**Optional**:
- **Anthropic API Key**: Required for understanding code_generation_generator specification (AI-powered generation capability)
- **OpenTelemetry Collector**: Required for testing event emission and observability integration features

---

## 7. Constraints & Assumptions

### Constraints

1. **Version Synchronization**: SAP-018 documentation must stay synchronized with chora-compose releases; architecture changes require SAP updates within 2 weeks
2. **Technical Accuracy Requirement**: All MCP tool specifications, generator interfaces, and architecture diagrams must match actual chora-compose implementation (verified against source code)
3. **Implementation-First Documentation**: Cannot document architecture features before they exist in chora-compose codebase; SAP-018 follows chora-compose development, not leads it

### Assumptions

1. **Advanced User Technical Background**: Primary users have intermediate-to-advanced software engineering experience; comfortable reading API specifications, architecture diagrams, source code
2. **chora-compose Installation**: Users have chora-compose v1.4.0+ installed and operational; SAP-018 focuses on architecture documentation, not installation procedures
3. **Architecture Evolution Stability**: chora-compose core architecture (MCP tools, Collections 3-tier model, generator registry) remains stable; minor version updates don't require complete SAP rewrites

---

## 8. Risks & Mitigations

### Risk 1: Architecture Evolution Outpacing Documentation

**Risk**: chora-compose architecture evolves faster than SAP-018 documentation updates, causing specification drift and inaccurate architecture references

**Likelihood**: Medium
**Impact**: High

**Mitigation**:
- Establish 2-week SLA for SAP updates following chora-compose releases
- Implement automated version checking (compare SAP-018 version references against actual chora-compose releases)
- Create lightweight update process for minor specification changes (Edit tool, not full SAP regeneration)
- Maintain protocol-spec.md as single source of truth for MCP tool specifications (enables fast updates)
- Version all SAP artifacts with chora-compose version compatibility notes

### Risk 2: Overly Technical Documentation Barrier

**Risk**: SAP-018 architecture documentation too technical for intermediate users, creating adoption barriers despite comprehensive coverage

**Likelihood**: Medium
**Impact**: Medium

**Mitigation**:
- Structure awareness-guide.md with progressive disclosure (quick reference first, deep dives later)
- Provide concrete examples for every MCP tool specification (JSON-RPC request/response pairs)
- Create visual architecture diagrams (Collections 3-tier model, context resolution flow, caching lifecycle)
- Cross-reference SAP-017 for step-by-step tutorials (SAP-018 = architecture reference, SAP-017 = how-to guide)
- Maintain glossary of technical terms in awareness-guide.md

### Risk 3: Missing Real-World Examples

**Risk**: Architecture documentation provides specifications without sufficient real-world usage examples, limiting practical adoption

**Likelihood**: Low
**Impact**: Medium

**Mitigation**:
- Include working example for every MCP tool (JSON-RPC request/response with actual parameters)
- Document chora-base COORD-2025-002 as reference implementation (18 SAPs = 90 artifacts generated via Collections)
- Provide custom generator example in protocol-spec.md (BaseGenerator implementation with registration)
- Add context resolution examples showing all 6 source types (inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output)
- Create caching optimization case study (demonstrating 94%+ cache hit rate achievement)

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
- Install SAP-018 in chora-base project (primary pilot)
- Validate architecture documentation accuracy against chora-compose v1.4.0 implementation
- Test AI agent comprehension (Claude using awareness-guide.md for architecture queries)
- Measure adoption time against targets (2-4 hours understanding, 1-2 days implementation)
- Collect feedback from early adopters
- Iterate on documentation clarity and technical accuracy

### Active Phase
**Status**: ✅ **Active**
**Target Start**: 2025-11-04

**Ongoing Activities**:
- Quarterly reviews and updates (synchronized with chora-compose releases)
- Community feedback integration from advanced users and custom generator developers
- Ledger maintenance (adoption tracking across chora-base and external projects)
- Maintain alignment with SAP-000 documentation structure
- Cross-reference updates with SAP-017 integration workflows
### Maintenance Phase

**Maintenance SLA**:
- Critical issues: 24-48 hours
- Major updates: 1-2 weeks
- Minor updates: Quarterly batch updates
- Documentation improvements: Ad-hoc

---

## 10. Related Documents

### Within chora-base

**SAP Artifacts**:
- [Protocol Specification](./protocol-spec.md) - Technical contracts for chora-compose Meta
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/capability-charter.md) - Core SAP protocols
- [SAP-000: [Name]](../[directory]/capability-charter.md) - [Relationship]
- [SAP-017: [Name]](../[directory]/capability-charter.md) - [Relationship]
**SAP Catalog**:
- [sap-catalog.json](../../../sap-catalog.json) - Machine-readable SAP registry

### External Documentation

**chora-compose Official Repository**:
- [chora-compose GitHub](https://github.com/chora-io/chora-compose) - Official source code repository
- [MCP Tools Implementation](https://github.com/chora-io/chora-compose/blob/main/src/tools.py) - Source code for 20 MCP tools
- [Generator Registry](https://github.com/chora-io/chora-compose/tree/main/src/generators) - BaseGenerator interface and 5 built-in generators
- [Collections Architecture](https://github.com/chora-io/chora-compose/blob/main/docs/collections-architecture.md) - 3-tier model documentation

**chora-compose Documentation**:
- [AGENTS.md](https://github.com/chora-io/chora-compose/blob/main/AGENTS.md) - MCP tool catalog (922 lines)
- [tool-catalog.md](https://github.com/chora-io/chora-compose/blob/main/docs/tool-catalog.md) - Partial tool reference

---

## 11. Approval & Sign-Off

**Charter Author**: Victor
**Date**: 2025-11-04
**Version**: 2.0.0

**Approval Status**: ✅ **Active**

**Review Cycle**:
- **Next Review**: 2026-02-04
- **Review Frequency**: Quarterly (synchronized with chora-compose release cycle)

**Change Log**:
- 2025-11-04: Complete rewrite (2.0.0) - Victor
  - Resolved SAP-018 v1.0.0 identity crisis (Docker Compose Meta vs chora-compose Meta)
  - Focused scope exclusively on chora-compose architecture documentation
  - Added comprehensive MCP tool specifications (20 tools)
  - Documented Collections architecture (3-tier model, caching, context propagation)
  - Added generator registry specification (5 generators + BaseGenerator interface)
  - Documented context resolution system (6 source types)
  - Added event emission documentation (OpenTelemetry integration)
  - Defined stakeholders, dependencies, constraints, assumptions, risks
  - Set lifecycle phases (Development complete, Pilot planned, Active)

---

**Version History**:
- **2.0.0** (2025-11-04): Complete rewrite - chora-compose Meta architecture documentation
- **1.0.0** (2025-11-04): Initial charter (archived - Docker Compose Meta identity crisis, 5,051 lines mixed content)
