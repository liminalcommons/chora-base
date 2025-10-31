# SAP Self-Evaluation - Capability Charter

**Pattern ID**: SAP-019
**Pattern Name**: sap-self-evaluation
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-30

## 1. Problem Statement

### The Challenge

Organizations and AI agents adopting chora-base SAPs (Skilled Awareness Patterns) lack systematic ways to:

1. **Assess adoption depth** - Beyond "installed vs. not installed," there's no measurement of integration quality or maturity level
2. **Identify prioritized gaps** - No clear guidance on what to improve next or which gaps block the most value
3. **Track progress over time** - No historical view of adoption journey or velocity metrics
4. **Generate actionable roadmaps** - No translation from assessment results to sprint-ready action plans
5. **Demonstrate value** - No evidence for stakeholders showing ROI of SAP adoption investments

### Current State

**What exists**:
- ✅ 18 SAPs with 3-level adoption frameworks (Level 1 → 2 → 3)
- ✅ Installation tooling (`install-sap.py`)
- ✅ Validation scripts (`check-sap-awareness-integration.sh`)
- ✅ Ledger tracking per SAP
- ✅ Metrics framework (SAP-013)

**What's missing**:
- ❌ Multi-dimensional maturity assessment beyond binary installed/not-installed
- ❌ Automated usage detection (are installed SAPs actually being used?)
- ❌ Aggregate adoption analytics across all SAPs
- ❌ Prioritized gap identification with effort estimates
- ❌ Integration with strategic roadmap planning
- ❌ Comparative benchmarking (project vs. baseline)

### Impact

**Without self-evaluation capability**:
- Adopters don't know if they're using SAPs effectively (partial adoption, surface-level integration)
- No clear path from current state to mastery (which Level 2 features to adopt next?)
- Progress is invisible to stakeholders (can't demonstrate value delivered)
- Optimization opportunities are missed (installed but underutilized SAPs)
- Resource allocation is guesswork (which SAP investments yield highest ROI?)

**With self-evaluation capability**:
- Clear visibility into adoption maturity (12/18 SAPs at Level 2+, 67% mature)
- Prioritized action plans (adopt SAP-004 Level 2 next, 3 hours, unblocks CI/CD)
- Evidence-based stakeholder communication (3x ROI, 75 hours saved from 25 invested)
- Continuous improvement framework (quarterly goals, sprint tracking)
- AI agents self-assess and optimize their own SAP usage patterns

## 2. Capability Overview

**SAP Self-Evaluation** provides a progressive framework for AI agents and teams to assess their SAP adoption depth, identify prioritized improvement opportunities, and generate actionable roadmaps integrated with sprint planning.

### Core Capabilities

1. **Progressive Evaluation** (Quick → Deep → Strategic)
   - Quick Check (30 seconds): Automated validation, instant status
   - Deep Dive (5 minutes): LLM-driven content analysis, gap identification
   - Strategic Analysis (30 minutes): Timeline trends, roadmap generation

2. **LLM-Native Intelligence**
   - Agent-executable prompts with concrete validation criteria
   - Structured checklists for Level 1/2/3 assessment per SAP
   - Content quality scoring (AGENTS.md completeness, integration depth)

3. **Prioritized Gap Analysis**
   - Impact × Effort scoring for each gap
   - Dependency-aware prioritization (what blocks what)
   - Sprint-ready action plans with time estimates

4. **Tracking Over Time**
   - Version-controlled adoption reports (git history)
   - Event timeline (events.jsonl for trend analysis)
   - Ledger updates (milestone tracking per SAP)

5. **Multi-Format Reporting**
   - Terminal: Quick status with color-coded indicators
   - Markdown: Detailed assessment reports (updateable)
   - YAML: Strategic roadmaps (integrated with planning)
   - JSON: Machine-readable for automation/dashboards
   - HTML: Interactive dashboards for stakeholders

## 3. Scope

### In Scope

**Evaluation Engine**:
- Automated quick checks (file existence, validation commands)
- LLM-driven content analysis (quality assessment, integration depth)
- Gap identification (comparing current state to protocol criteria)
- Priority ranking (impact, effort, dependencies, blockers)

**Reporting & Planning**:
- Multi-level reports (quick/detailed/strategic)
- Adoption roadmap generation (quarterly goals, sprint breakdown)
- Progress tracking over time (historical analysis)
- Dashboard generation (visual analytics)

**Integration Points**:
- SAP-013 integration (adoption metrics alongside ROI)
- Per-SAP protocol extensions (evaluation criteria in protocol-spec.md)
- Event logging (adoption events to events.jsonl)
- Ledger updates (milestone tracking)

**Target Audience**:
- AI agents (Claude, other LLMs) - Self-assessment capability
- Development teams - Sprint planning integration
- Technical leaders - Strategic roadmap visibility
- Stakeholders - ROI evidence via dashboards

### Out of Scope

**Not included**:
- Cross-repo adoption analytics (ecosystem-wide benchmarking) - Future SAP
- Real-time monitoring/alerting - Use existing observability tools
- Prescriptive AI recommendations - Agents identify gaps, humans prioritize
- Automated remediation - Evaluation only, not execution
- Web service/API - CLI and file-based reports only (v1.0.0)

### Future Enhancements (Post-1.0.0)

- Comparative benchmarking (project vs. recommended baseline)
- Ecosystem analytics (adoption trends across all chora-base users)
- ROI prediction modeling (estimate value of adopting SAP-X next)
- Automated usage detection (scan codebase for SAP artifact usage)
- Interactive web dashboard (beyond static HTML)

## 4. Success Criteria

### Adoption Success

**Level 1 Adoption** (1-2 hours):
- SAP-019 installed (5 artifacts present)
- CLI tool functional (`sap-evaluator.py --quick`)
- Quick check runs in <30 seconds
- Terminal output shows adoption status for all installed SAPs

**Level 2 Adoption** (4-6 hours cumulative):
- Deep dive evaluations completed for 3+ SAPs
- Markdown reports generated and committed to repo
- Gaps prioritized with effort estimates
- First roadmap generated (sap-roadmap.yaml)

**Level 3 Adoption** (8-12 hours cumulative):
- Quarterly evaluation cadence established
- Historical tracking via events.jsonl
- Dashboard generated for stakeholder communication
- Adoption metrics integrated with SAP-013 ROI analysis

### Quality Metrics

**Evaluation Accuracy**:
- Quick check: 95%+ correlation with manual assessment (automated validation)
- Deep dive: 85%+ accuracy in gap identification (LLM-driven)
- Strategic: 100% actionable recommendations (no hypothetical suggestions)

**Performance**:
- Quick check: <30 seconds for 12 installed SAPs
- Deep dive per SAP: <5 minutes (LLM inference + analysis)
- Strategic roadmap: <30 minutes (all SAPs + timeline analysis)

**Usability**:
- Agent can self-evaluate without human guidance (AGENTS.md sufficient)
- Reports are actionable (specific file, tool, location, content)
- Roadmap integrates with existing planning workflows (YAML format)

### Value Delivered

**Visibility**:
- 100% of installed SAPs have adoption level assessment
- Gaps identified with priority ranking (P0/P1/P2)
- Progress tracked quarter-over-quarter

**Efficiency**:
- 50% reduction in time to identify next adoption step (vs. manual review)
- 80% reduction in roadmap planning time (automated generation)
- 3x increase in stakeholder communication frequency (dashboards available)

**Outcomes**:
- 25% increase in SAP adoption depth (more Level 2+ vs. Level 1 only)
- 40% improvement in adoption velocity (time from install to Level 2)
- Evidence-based prioritization (no guesswork on what SAP to adopt next)

## 5. Key Stakeholders

### Primary Users

**AI Agents (Claude, other LLMs)**:
- Self-assessment of SAP adoption patterns
- Progressive guidance (quick check → deep dive)
- Agent-executable action plans
- **Need**: Structured prompts, concrete validation criteria, step-by-step guidance

**Development Teams**:
- Sprint planning with SAP adoption tasks
- Quarterly roadmap updates
- Progress tracking over time
- **Need**: Time estimates, priority ranking, integration with existing workflows

### Secondary Users

**Technical Leaders**:
- Strategic planning (which SAPs to invest in)
- Resource allocation (effort vs. value)
- Team capability development
- **Need**: ROI evidence, gap analysis, comparative benchmarking

**Stakeholders**:
- Visibility into engineering capability maturity
- Evidence of continuous improvement
- Justification for tooling investments
- **Need**: Executive dashboards, trend analysis, business value translation

## 6. Dependencies

### Required SAPs

**Hard Dependencies** (must be installed):
- **SAP-000** (sap-framework) - Defines SAP structure, governance
- **SAP-007** (documentation-framework) - Provides documentation standards
- **SAP-009** (agent-awareness) - LLM-driven assessment patterns

**Soft Dependencies** (recommended):
- **SAP-013** (metrics-tracking) - Integration point for adoption metrics
- **SAP-008** (automation-scripts) - CLI patterns, justfile tasks
- **SAP-004** (testing-framework) - Testing the evaluation engine itself

### External Dependencies

**Python Libraries**:
- `json`, `yaml` - Report generation
- `pathlib` - File system navigation
- `subprocess` - Git integration, validation command execution
- `dataclasses` - Structured metric collection
- `typing` - Type safety

**System Requirements**:
- Git (for timeline analysis, ledger tracking)
- Python 3.9+ (for modern syntax, dataclasses)
- Access to sap-catalog.json (SAP metadata)

**Optional Integrations**:
- GitHub CLI (`gh`) - For project management integration
- pytest (for testing the evaluator itself)
- Plotly/matplotlib (for dashboard generation - future)

## 7. Constraints & Assumptions

### Constraints

**Technical**:
- File-based reports only (no web service in v1.0.0)
- LLM-driven analysis requires API access (Claude, OpenAI, etc.)
- Git history required for timeline analysis
- Single-repo scope (no cross-repo analytics in v1.0.0)

**Performance**:
- LLM inference adds latency (5 min for deep dive acceptable)
- Large repos (100+ SAPs hypothetically) may need batching
- Dashboard generation may be slow for extensive history

**Operational**:
- Requires discipline to run evaluations regularly (not automated)
- Roadmap generation requires human validation/prioritization
- Ledger updates require manual commits

### Assumptions

**About Adopters**:
- AI agents have access to Read, Bash, and other standard tools
- Projects have git version control
- Adopters understand SAP framework (SAP-000)
- Python environment available for CLI execution

**About SAPs**:
- All SAPs follow 3-level adoption pattern (Level 1 → 2 → 3)
- Protocol-spec.md contains validation criteria
- Adoption-blueprint.md has concrete step-by-step instructions
- Ledger.md follows standard format

**About Usage**:
- Evaluations run on-demand (not continuous monitoring)
- Reports committed to repo (version-controlled)
- Quarterly cadence is sufficient (not real-time)

## 8. Risks & Mitigations

### Risk 1: LLM Hallucination in Gap Identification

**Impact**: Medium - Incorrect gaps lead to wasted effort
**Likelihood**: Medium - LLMs can misinterpret criteria

**Mitigation**:
- Use structured prompts with concrete checklists (boolean criteria)
- Combine LLM analysis with automated validation (file checks, grep)
- Provide confidence scores (high/medium/low) for each gap
- Human review required before committing roadmap

### Risk 2: Stale Evaluation Results

**Impact**: Medium - Decisions based on outdated assessments
**Likelihood**: High - Teams forget to re-evaluate

**Mitigation**:
- Timestamp all reports prominently
- Warning if evaluation >30 days old
- Integration with sprint retrospectives (quarterly review)
- Git commit hook reminder (optional)

### Risk 3: Evaluation Overhead

**Impact**: Low - Teams skip evaluations due to time cost
**Likelihood**: Medium - 30 min strategic analysis is non-trivial

**Mitigation**:
- Progressive evaluation (quick check is only 30 seconds)
- Clear ROI messaging (5 min evaluation saves 1+ hour of planning)
- Integration with existing meetings (sprint planning, retrospectives)
- Automated quick checks in CI/CD (future enhancement)

### Risk 4: Inconsistent Criteria Across SAPs

**Impact**: Medium - Evaluation quality varies per SAP
**Likelihood**: Medium - 18 SAPs may have different standards

**Mitigation**:
- Standardize protocol-spec.md evaluation sections (template)
- Validation during SAP audit workflow (SAP_AUDIT_WORKFLOW.md)
- Meta-evaluation (SAP-019 evaluates itself using same criteria)
- Community feedback loop (ledger.md for improvement suggestions)

## 9. Related Patterns

### Complementary SAPs

- **SAP-000** (sap-framework) - Defines what to evaluate
- **SAP-009** (agent-awareness) - How agents self-assess
- **SAP-013** (metrics-tracking) - Where adoption metrics go
- **SAP-012** (development-lifecycle) - When to evaluate (sprint/quarterly)

### Integration Points

- **SAP-001** (inbox-coordination) - Coordination requests can reference adoption gaps
- **SAP-007** (documentation-framework) - Reports follow Diataxis structure
- **SAP-008** (automation-scripts) - CLI tool follows justfile patterns

## 10. Version History

### 1.0.0 (2025-10-30)

**Initial Release**:
- Progressive evaluation framework (quick/deep/strategic)
- LLM-driven gap identification
- Multi-format reporting (terminal/markdown/YAML/JSON/HTML)
- CLI tool (`sap-evaluator.py`)
- Core evaluation engine
- Integration with SAP-013 metrics

**Baseline Established**:
- 18 SAPs evaluatable
- 3-level maturity assessment
- Prioritized roadmap generation

**Next Steps**:
- Validate with 3 pilot projects
- Gather feedback on report formats
- Iterate on prompt templates for accuracy
