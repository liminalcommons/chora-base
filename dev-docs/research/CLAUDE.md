# Claude Research Patterns - Technical Investigation

**Purpose:** Claude-specific patterns for research tasks and technical investigation.

**Parent:** See [../../CLAUDE.md](../../CLAUDE.md) for project-level patterns, [../CLAUDE.md](../CLAUDE.md) for development guide, and [README.md](README.md) for research overview.

---

## Claude's Strengths for Research

### 1. Comprehensive Literature Review (200k Context)

Claude can analyze massive amounts of research material simultaneously:

```markdown
"Research integration approach: [topic]

Load research materials (200k window):
1. All related documents in dev-docs/research/
2. External API documentation
3. Relevant vision documents (dev-docs/vision/)
4. Current implementation (src/mcp_orchestrator/)
5. Similar projects documentation (if available)

Analysis:
- What approaches exist?
- What are the tradeoffs?
- What fits our architecture?
- What are the risks?

Synthesize findings into research document."
```

### 2. Multi-Source Synthesis

Claude excels at connecting insights across sources:

```markdown
"Synthesize research findings across sources:

Sources:
1. Academic papers: [list]
2. Documentation: [list]
3. Code examples: [list]
4. Community discussions: [list]
5. Our codebase patterns: [list]

Task:
- Extract key insights from each
- Identify common patterns
- Spot contradictions
- Synthesize best practices
- Recommend approach for mcp-orchestration

Provide comprehensive synthesis."
```

### 3. Proof-of-Concept Development

Claude can rapidly prototype research findings:

```markdown
"Develop proof-of-concept for [research_topic]:

Context:
- Research findings: [document]
- Integration point: [where it fits]
- Success criteria: [what validates approach]

POC Requirements:
1. Minimal implementation (< 200 lines)
2. Demonstrates key concept
3. Tests critical assumptions
4. Documents learnings

Don't integrate with full codebase yet.
Do validate feasibility and measure performance."
```

---

## Research Workflow Patterns

### Pattern: Conduct Research Investigation

```markdown
"Research investigation: [topic]

## Phase 1: Problem Definition (Day 1)
1. **Problem Statement**
   - What problem are we solving?
   - Why is this research needed?
   - What decisions does this inform?

2. **Research Questions**
   - List specific questions to answer
   - Prioritize by importance
   - Define success criteria

3. **Scope**
   - What's in scope?
   - What's out of scope?
   - What's the timeline?

## Phase 2: Information Gathering (Days 2-3)
1. **Literature Review**
   - Academic papers
   - Technical documentation
   - Open source examples
   - Community best practices

2. **Code Analysis**
   - Existing implementations
   - Similar projects
   - Framework patterns
   - Our codebase constraints

3. **Expert Consultation** (if applicable)
   - Technical forums
   - Documentation feedback
   - Community input

## Phase 3: Analysis (Day 4)
1. **Synthesize Findings**
   - What did we learn?
   - What patterns emerged?
   - What contradictions exist?

2. **Evaluate Options**
   - List approaches (3-5 options)
   - Tradeoffs for each
   - Cost/benefit analysis
   - Risk assessment

3. **Recommendation**
   - Recommended approach
   - Why this choice?
   - What are the risks?
   - What's the mitigation plan?

## Phase 4: Validation (Day 5)
1. **Proof-of-Concept**
   - Implement minimal POC
   - Test critical assumptions
   - Measure performance
   - Document learnings

2. **Documentation**
   - Research findings document
   - POC code with comments
   - Integration plan
   - Recommendation summary

Provide research plan before starting."
```

### Pattern: Integration Research

```markdown
"Research integration with [external_system]:

## Context
- External system: [name, purpose, documentation]
- Integration goal: [what we want to achieve]
- mcp-orchestration touchpoints: [where it integrates]

## Research Questions
1. **Feasibility**
   - Can we integrate with current architecture?
   - What APIs/interfaces exist?
   - What are the technical constraints?

2. **Approach**
   - What integration patterns apply?
   - What's the recommended approach?
   - What libraries/tools help?

3. **Effort**
   - How complex is integration?
   - Time estimate (story points)?
   - What skills needed?

4. **Risks**
   - What could go wrong?
   - What are the dependencies?
   - What's the maintenance burden?

## Deliverables
1. Integration research document
2. Proof-of-concept (if feasible)
3. Integration architecture diagram
4. Recommendation (integrate now/later/never)

## Timeline
- Week 1: Research questions 1-2
- Week 2: POC development
- Week 3: Documentation and recommendation

Begin research investigation."
```

### Pattern: Technical Spike

```markdown
"Technical spike: [technology/approach]

## Spike Objective
- Validate: [specific technical assumption]
- Learn: [what we need to understand]
- Decide: [what decision this informs]

## Time Box
- Duration: [1-3 days]
- Stop condition: [when do we stop researching?]

## Investigation Steps
1. **Quick Research** (2 hours)
   - Read documentation
   - Find examples
   - Identify key concepts

2. **Proof-of-Concept** (4-6 hours)
   - Minimal implementation
   - Test critical path
   - Measure performance

3. **Integration Test** (2-4 hours)
   - Test with our architecture
   - Identify integration points
   - Document obstacles

4. **Documentation** (1-2 hours)
   - Findings summary
   - Code examples
   - Recommendation

## Success Criteria
- [ ] Validated technical assumption
- [ ] Measured performance/feasibility
- [ ] Identified integration approach
- [ ] Documented learnings

Start technical spike (time-boxed)."
```

---

## Research Documentation Patterns

### Pattern: Research Findings Document

```markdown
"Create research findings document:

## Structure

### Executive Summary
- Problem statement
- Recommendation (one sentence)
- Key findings (3-5 bullets)

### Research Questions & Answers
For each question:
- Question
- Answer (evidence-based)
- Supporting data

### Approach Evaluation
For each approach (3-5 options):
- Name and description
- Pros and cons
- Cost estimate
- Risk assessment
- Fit with architecture

### Recommendation
- Recommended approach
- Reasoning (why this choice?)
- Implementation plan (high-level)
- Risks and mitigation

### Proof-of-Concept Results
- What was tested
- Code examples
- Performance data
- Lessons learned

### Next Steps
- Immediate actions
- Long-term actions
- Follow-up research needed

Generate research findings document following this structure."
```

---

## Ecosystem Integration Research

### Pattern: Research External System Integration

```markdown
"Research integration with [system_name]:

## System Analysis
1. **Purpose and Capabilities**
   - What does system do?
   - What value does it provide?
   - What's the user base?

2. **Technical Architecture**
   - How is it built?
   - What APIs exist?
   - What protocols/formats?

3. **Integration Points**
   - Where can we integrate?
   - What hooks/callbacks exist?
   - What's the integration model?

## Integration Patterns Review
Reference: [ECOSYSTEM_INTEGRATION.md](ECOSYSTEM_INTEGRATION.md)

Which pattern applies?
1. **Client Integration** - MCP client uses mcp-orchestration
2. **Frontend Integration** - Web UI for config management
3. **n8n Integration** - Workflow automation
4. **Gateway Integration** - Multi-service orchestration

## Feasibility Analysis
1. **Technical Feasibility**
   - Can we build this?
   - What's blocking us?
   - What dependencies exist?

2. **Value Proposition**
   - What user value?
   - What's the ROI?
   - What's the priority?

3. **Effort Estimate**
   - Story points
   - Timeline
   - Resources needed

## Recommendation
- Integrate: [Yes/No/Later]
- Pattern: [which integration pattern]
- Wave: [when to build]
- Reasoning: [why this decision]

Provide integration research analysis."
```

---

## Performance Research

### Pattern: Performance Investigation

```markdown
"Investigate performance of [component/operation]:

## Baseline Measurement
1. **Current Performance**
   - Operation: [what we're measuring]
   - Metric: [latency, throughput, etc]
   - Baseline: [current measurement]
   - Target: [desired performance]

2. **Measurement Methodology**
   - Test scenario
   - Data size
   - Environment
   - Tools used

## Performance Analysis
1. **Profiling**
   - Where is time spent?
   - What are the bottlenecks?
   - What's the memory usage?

2. **Root Causes**
   - Algorithmic complexity
   - I/O operations
   - Network latency
   - Cryptographic operations

## Optimization Options
For each option:
- Approach description
- Expected improvement
- Implementation effort
- Risks

## Recommendation
- Recommended optimization
- Performance improvement estimate
- Implementation plan
- Validation approach

Conduct performance investigation."
```

---

## Research Task Management

### Pattern: Create Research Task

```markdown
"Create new research task: [task_name]

## Task Definition
Use template from [README.md](README.md):

- **Status:** Active
- **Priority:** P0/P1/P2/P3
- **Blocks:** What this unblocks
- **Timeline:** Research + implementation duration

## Content
1. Problem Statement
2. Research Questions (3-5)
3. Success Criteria
4. Deliverables
5. Timeline (weekly breakdown)

## Integration
1. Add to README.md active research table
2. Link to relevant vision documents
3. Reference ecosystem context
4. Assign owner and timeline

Create research task document."
```

### Pattern: Complete Research Task

```markdown
"Complete research task: [task_name]

## Completion Checklist
- [ ] All research questions answered
- [ ] Findings document created
- [ ] Proof-of-concept developed (if applicable)
- [ ] Recommendation documented
- [ ] Integration plan defined
- [ ] README.md updated (move to completed)

## Documentation
1. **Findings Document**
   - Save as: [task-name]-findings.md
   - Include all deliverables
   - Link from README.md

2. **Update README.md**
   - Move from active to completed
   - Add completion date
   - Link to findings
   - Link to implementation (if built)

## Knowledge Capture
1. Update vision documents (if relevant)
2. Create .chora/memory note (lessons learned)
3. Share findings with team

Mark research task as completed."
```

---

## Best Practices for Research

### ✅ Do's

1. **Define clear questions** - Specific, answerable research questions
2. **Time-box investigations** - Don't research forever
3. **Build POCs** - Validate assumptions with code
4. **Document findings** - Write comprehensive research docs
5. **Measure performance** - Quantify with data
6. **Consider alternatives** - Evaluate 3-5 options
7. **Link to ecosystem** - Reference integration patterns
8. **Validate with code** - Theory → Practice

### ❌ Don'ts

1. **Don't research indefinitely** - Time-box and decide
2. **Don't skip documentation** - Findings must be written
3. **Don't ignore integration** - Consider ecosystem fit
4. **Don't build without research** - Validate first
5. **Don't forget follow-up** - Update README.md
6. **Don't lose context** - Link to vision/architecture
7. **Don't work in isolation** - Share findings early
8. **Don't skip POCs** - Code validates theory

---

## Resources

### Research Documents (This Directory)
- **[README.md](README.md)** - Research overview and task index
- **[ECOSYSTEM_INTEGRATION.md](ECOSYSTEM_INTEGRATION.md)** - Integration patterns
- **[INTEGRATION_QUICK_REFERENCE.md](INTEGRATION_QUICK_REFERENCE.md)** - Quick reference
- **[UNIVERSAL_LOADABILITY_REVIEW.md](UNIVERSAL_LOADABILITY_REVIEW.md)** - Loadability research

### Parent Guides
- **[../../CLAUDE.md](../../CLAUDE.md)** - Project-level Claude patterns
- **[../CLAUDE.md](../CLAUDE.md)** - Development guide
- **[../vision/CLAUDE.md](../vision/CLAUDE.md)** - Vision planning patterns

### Related Documentation
- **[../../dev-docs/vision/](../../dev-docs/vision/)** - Vision documents
- **[../../project-docs/](../../project-docs/)** - Project documentation
- **[../../.chora/memory/CLAUDE.md](../../.chora/memory/CLAUDE.md)** - Memory integration

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
