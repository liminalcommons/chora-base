# Protocol Specification: Dogfooding Patterns

**SAP ID**: SAP-027
**Version**: 1.1.0
**Status**: pilot
**Last Updated**: 2025-11-05

---

## 1. Overview

Formalized 6-week dogfooding pilot methodology for validating patterns through internal use before ecosystem adoption


### Key Capabilities


- 4-phase pilot design (research, build, validate, decide)

- GO/NO-GO criteria framework (time savings, satisfaction, bugs, adoption)

- ROI analysis with break-even calculation

- Metrics collection templates (time tracking, validation reports)

- Pilot documentation structure (weekly metrics, final summary)

- Template refinement workflow (TODO completion, production readiness)



---

## 2. Core Contracts

### Contract 0: Week -1 Pre-Pilot Discovery

**Description**: Systematic discovery process to identify and select high-value pilot candidates from the intention inventory before committing to a 6-week pilot.

**Purpose**: Reduce risk of investing 6 weeks in low-ROI pilots by validating strategic fit, evidence availability, and user demand upfront.

**Interface**:
```bash
# Query intention inventory for pilot candidates
cat .chora/memory/knowledge/notes/intention-inventory-*.md | grep -A 5 "^## "

# Score and select pilot candidates
python scripts/score-pilot-candidates.py --inventory intention-inventory-2025-11-05.md --output pilot-candidates-2025-11-05.md

# Output: .chora/memory/knowledge/notes/pilot-candidates-{date}.md
```

**Discovery Workflow**:

**Step 1: Query Intention Inventory**
- Read latest intention inventory from SAP-010: `.chora/memory/knowledge/notes/intention-inventory-{date}.md`
- Filter intentions by status: `proposed`, `validated`, `prioritized`
- Expected input: 50-150 intentions across multiple strategic themes

**Step 2: Score Pilot Candidates**
- Apply weighted scoring criteria:
  - **Evidence availability (40%)**: Level A/B evidence exists for domain research
    - 10 points: Multiple Level A sources (standards, peer-reviewed papers)
    - 7 points: Mix of Level A + Level B (industry case studies)
    - 4 points: Primarily Level B sources
    - 1 point: Limited to Level C (expert opinion, blogs)
  - **Strategic alignment (30%)**: Fits current Wave 1/Wave 2 vision priorities
    - 10 points: Wave 1 committed feature with explicit success criteria
    - 7 points: Wave 2 exploratory feature with strategic rationale
    - 4 points: Wave 3 future consideration
    - 1 point: Not in current vision document
  - **User demand (20%)**: Evidence of real user need
    - 10 points: ≥10 explicit requests in coordination inbox or user feedback
    - 7 points: 5-9 requests or clear pain point articulation
    - 4 points: 1-4 requests or inferred need
    - 1 point: Internal hypothesis, no user validation
  - **Feasibility (10%)**: Effort estimate and complexity assessment
    - 10 points: 1-2 week build, low technical risk
    - 7 points: 2-3 week build, moderate risk
    - 4 points: 3-4 week build, high risk
    - 1 point: >4 weeks or blocked dependencies
- Calculate weighted score: `(E×0.4) + (S×0.3) + (U×0.2) + (F×0.1)`
- Target threshold: ≥7.0 for pilot consideration

**Step 3: Select Top 3-5 Candidates**
- Rank intentions by weighted score (descending)
- Select top 3-5 candidates above threshold
- Ensure diversity across strategic themes if possible
- Document rationale for selections and rejections

**Step 4: Create Pilot-Candidates Note**
- Generate structured note: `.chora/memory/knowledge/notes/pilot-candidates-{date}.md`
- Include for each candidate:
  - Intention ID, name, description
  - Weighted score breakdown (evidence, alignment, demand, feasibility)
  - Target SAP ID (if creating new) or enhancement scope (if extending existing)
  - Estimated pilot timeline (6-week breakdown)
  - Key risks and mitigation strategies
  - Expected success metrics (time savings, satisfaction)

**Step 5: Stakeholder Review (Optional)**
- Share pilot-candidates note with team or stakeholders
- Collect feedback on selections
- Adjust ranking if new information emerges
- Document review outcomes

**Step 6: Make Selection Decision**
- Choose 1 candidate from top 3-5 for immediate pilot
- Document decision rationale in pilot-candidates note
- Log decision event to `.chora/memory/events/dogfooding.jsonl`:
  ```json
  {
    "timestamp": "2025-11-05T10:30:00Z",
    "event_type": "pilot_candidate_selected",
    "pilot_id": "pilot-2025-11-05-sap-015",
    "candidate": {
      "intention_id": "INT-089",
      "name": "Backlog Organization Patterns",
      "weighted_score": 8.2,
      "scores": {"evidence": 9, "alignment": 8, "demand": 7, "feasibility": 9}
    },
    "rationale": "Highest score (8.2) with strong evidence base and immediate user need from 3 active projects"
  }
  ```
- Proceed to Contract 1 (Week 0 Research Phase)

**Output Artifacts**:
```markdown
## Pilot Candidates: {Date}

### Selection Summary
- **Candidates evaluated**: 89
- **Above threshold (≥7.0)**: 12
- **Top 3-5 finalists**: 5
- **Selected for pilot**: SAP-015 Backlog Organization Patterns

### Top 5 Candidates

#### 1. SAP-015: Backlog Organization Patterns (Score: 8.2)
- **Evidence (9/10)**: Strong Level A evidence from JIRA, Linear case studies
- **Alignment (8/10)**: Wave 2 exploratory feature, fits strategic priorities
- **Demand (7/10)**: 7 explicit requests from 3 active projects
- **Feasibility (9/10)**: 2-week build, existing beads CLI foundation
- **Rationale**: Immediate pain point, strong evidence, fast build

#### 2. SAP-030: Data Fetching Patterns (Score: 7.8)
[...]

### Selection Decision
**Pilot ID**: pilot-2025-11-05-sap-015
**Candidate**: SAP-015 Backlog Organization Patterns
**Rationale**: [...]
**Next steps**: Proceed to Week 0 research phase
```

**Requirements**:
- MUST query latest intention inventory from SAP-010
- MUST score candidates using 4-criteria weighted model
- MUST select ≥3 candidates above threshold (7.0)
- MUST create pilot-candidates note with structured output
- MUST log selection decision to A-MEM (dogfooding.jsonl)
- MUST complete discovery in ≤2 hours
- SHOULD consider strategic theme diversity when selecting finalists

**Success Metrics**:
- Discovery completion time: ≤2 hours
- Pilot candidates above threshold: ≥3
- Final selection score: ≥7.0
- Selection confidence: High (clear rationale, no major objections)

**Integration Points**:
- **SAP-010 (Memory System)**: Read intention inventory, write pilot-candidates note
- **SAP-006 (Vision Synthesis)**: Query Wave 1/Wave 2 priorities for alignment scoring
- **SAP-001 (Inbox)**: Count coordination requests for demand scoring
- **SAP-015 (Task Tracking)**: Optionally create P3 discovery task for tracking

---

### Contract 1: 6-Week Pilot Timeline

**Description**: Structured dogfooding pilot with 4 phases: research, build, validate, decide

**Timeline Structure**:
```markdown
Week 0 (Research Phase):
  - Fill research prompt template with SAP domain context
  - Execute research using Claude Code WebSearch or AI assistant
  - Generate docs/research/{sap-name}-research.md (10-20 pages)
  - Extract principles, decision playbooks, anti-patterns for pilot planning
  - Validate evidence levels (Level A ≥30%, Level B ≥40%, Level C ≤30%)

Weeks 1-3 (Build Phase):
  - Build capability to minimum viable state
  - Use research insights to inform design decisions
  - Track setup time for ROI analysis

Week 4 (Validation Phase):
  - Use capability 2+ times in real scenarios
  - Collect metrics per use (time, satisfaction, bugs)
  - Document adoption cases

Week 4 End (Decision Phase):
  - Review metrics against GO/NO-GO criteria
  - Calculate time savings, satisfaction avg, bug count
  - Write go-no-go-decision.md with data-driven recommendation

Week 5 (Formalization Phase, if GO):
  - Complete artifact TODOs
  - Update ledger with adoption tracking
  - Mark SAP as production-ready
```

**Requirements**:
- Week 0 research report must have ≥30% Level A evidence citations
- Research must inform Week 1-3 build phase (cite research in design decisions)
- Week 4 validation requires ≥2 adoption cases
- GO decision requires all criteria met (time savings ≥5x, satisfaction ≥85%, bugs = 0)

### Contract 2: Week 0 Research Contract

**Description**: Evidence-based research phase before pilot build

**Interface**:
```bash
# Execute research workflow
just research "{sap-domain-topic}"

# Example: Before creating SAP-030 (database-migrations)
just research "database migration best practices for Python projects"

# Output: docs/research/{topic}-research.md
```

**Research Output Structure**:
```markdown
## Research Report: {Topic}

### Executive Summary
- 10-12 bullet takeaways
- "Adopt now vs later" recommendations

### Principles (The Why)
- Modularity, SOLID, 12-factor, etc.
- Level A/B/C evidence citations

### Practices (The How)
- Architecture, testing, CI/CD patterns
- Code examples, configuration snippets

### Decision Playbooks
- "Choose X when..." guidance
- Trade-off tables

### Metrics & Targets
- DORA, SLOs, security SLAs
- Baseline → target deltas

### Anti-Patterns
- What to avoid
- Why these fail

### Risk Register
- Top 10 risks
- Likelihood/impact/mitigations

### Implementation Roadmap
- 90-day/6-month plan
- Dependencies, KPI deltas

### Checklists
- Code review, release, incident, threat modeling

### Appendix
- Annotated bibliography (Level A/B/C labeled)
- Glossary
```

**Requirements**:
- MUST use research prompt template from docs/templates/research-prompt-template.md
- MUST achieve ≥30% Level A evidence (standards, peer-reviewed)
- MUST achieve ≥40% Level B evidence (industry case studies)
- MUST limit Level C evidence (expert opinion) to ≤30%
- MUST include decision playbooks for key architectural choices
- MUST save output to docs/research/{topic}-research.md

---

## 3. Integration Patterns

SAP-027 (Dogfooding Patterns) integrates deeply with the strategic planning and task management ecosystem, creating feedback loops from pilot results back to vision and backlog.

### Core SAP Integrations

#### Integration with SAP-001 (Inbox)

**Integration Point**: Coordination Requests → Intention Discovery

**Purpose**: Transform coordination requests from cross-repo inbox into validated intentions for pilot consideration.

**Workflow**:
1. User submits coordination request to `inbox/coordination/active.jsonl`
2. During Week -1 Discovery, query inbox for demand signals:
   ```bash
   # Count coordination requests related to a capability
   grep -i "task tracking" inbox/coordination/active.jsonl | wc -l
   ```
3. Use request count as input to demand scoring (20% weight)
4. Reference coordination request IDs in pilot-candidates note

**Data Flow**:
```
Coordination Request (SAP-001)
  ↓
Demand Signal (Count requests)
  ↓
Pilot Candidate Scoring (SAP-027)
  ↓
Selected Pilot (If score ≥7.0)
```

**Configuration**:
```yaml
dogfooding:
  discovery:
    demand_sources:
      - type: inbox
        path: inbox/coordination/active.jsonl
        weight: 0.2  # 20% of total score
```

---

#### Integration with SAP-006 (Vision Synthesis)

**Integration Point**: Pilot GO/NO-GO → Wave Promotion/Demotion

**Purpose**: Create feedback loop from pilot results to strategic vision, promoting validated features from Wave 2 (exploratory) to Wave 1 (committed), or demoting failed pilots to Wave 3 (future).

**Workflow - Pilot GO (Promote)**:
1. Pilot evaluation scores ≥60% (satisfaction ≥85%, time savings ≥5x, bugs = 0)
2. Update vision document Wave 2 → Wave 1:
   ```bash
   # Read current vision
   cat .chora/memory/knowledge/notes/vision-chora-base-2025.md | grep -A 10 "## Wave 2"

   # Promote feature to Wave 1
   # Manual edit: Move feature from Wave 2 to Wave 1 with pilot evidence
   ```
3. Add pilot evidence to Wave 1 decision criteria:
   ```markdown
   ## Wave 1: Committed Features (Next 3 Months)

   ### Backlog Organization Patterns (SAP-015)
   **Decision**: Adopt
   **Evidence**: 4-week pilot, 85% satisfaction, 6x time savings
   **Pilot ID**: pilot-2025-11-05-sap-015
   **Success criteria**: Reduce task triage time from 30min → 5min
   ```
4. Log vision update to A-MEM:
   ```json
   {
     "timestamp": "2025-11-05T16:00:00Z",
     "event_type": "vision_updated",
     "change": "wave_promotion",
     "feature": "Backlog Organization Patterns",
     "from_wave": 2,
     "to_wave": 1,
     "pilot_id": "pilot-2025-11-05-sap-015",
     "evidence": {"satisfaction": 85, "time_savings": "6x", "bugs": 0}
   }
   ```

**Workflow - Pilot NO-GO (Demote)**:
1. Pilot evaluation fails criteria (satisfaction <85% OR time savings <5x OR bugs >0)
2. Update vision document Wave 2 → Wave 3:
   ```markdown
   ## Wave 3: Future Considerations (6+ Months)

   ### Advanced Code Generation (SAP-033)
   **Decision**: Defer
   **Rationale**: 4-week pilot showed only 2x time savings (target: 5x), 3 bugs in generated code
   **Pilot ID**: pilot-2025-10-15-sap-033
   **Lessons learned**: Need better prompt engineering, template validation
   ```
3. Log vision update to A-MEM (same structure, different change type)

**Data Flow**:
```
Pilot Evaluation (SAP-027)
  ↓
GO (≥60%) / NO-GO (<60%)
  ↓
Vision Update (SAP-006)
  - GO → Wave 2 → Wave 1
  - NO-GO → Wave 2 → Wave 3
  ↓
Strategic Alignment Updated
```

**Configuration**:
```yaml
dogfooding:
  vision_integration:
    enabled: true
    promotion_threshold: 0.6  # 60% composite score
    promotion_criteria:
      satisfaction: 0.85  # 85% satisfaction
      time_savings: 5     # 5x time savings
      bugs: 0             # Zero bugs
    vision_path: .chora/memory/knowledge/notes/vision-{project}-{horizon}.md
    update_strategy: manual  # or 'automated' for auto-promotion
```

---

#### Integration with SAP-010 (Memory System / A-MEM)

**Integration Point**: Event Logging + Intention Inventory

**Purpose**:
1. Query intention inventory during Week -1 Discovery
2. Log pilot lifecycle events (candidate selection, research, evaluation, decision)
3. Store pilot-candidates notes and lessons learned

**Workflow - Read Intention Inventory**:
```bash
# Query latest intention inventory
cat .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md

# Filter by status
grep -A 10 "^### Status: validated" .chora/memory/knowledge/notes/intention-inventory-*.md
```

**Workflow - Write Pilot Events**:
```bash
# Log pilot candidate selection
echo '{"timestamp":"2025-11-05T10:30:00Z","event_type":"pilot_candidate_selected","pilot_id":"pilot-2025-11-05-sap-015","candidate":{"intention_id":"INT-089","name":"Backlog Organization Patterns","weighted_score":8.2}}' >> .chora/memory/events/dogfooding.jsonl

# Log pilot completion
echo '{"timestamp":"2025-12-03T16:00:00Z","event_type":"pilot_completed","pilot_id":"pilot-2025-11-05-sap-015","decision":"GO","scores":{"satisfaction":85,"time_savings":"6x","bugs":0}}' >> .chora/memory/events/dogfooding.jsonl
```

**Workflow - Store Knowledge Notes**:
```bash
# Create pilot-candidates note
cat > .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md <<EOF
## Pilot Candidates: 2025-11-05
[Selection summary, top 5 candidates, decision rationale]
EOF

# Create lessons learned note (if NO-GO)
cat > .chora/memory/knowledge/notes/lessons-learned-pilot-2025-10-15-sap-033.md <<EOF
## Lessons Learned: Advanced Code Generation Pilot
[What worked, what didn't, recommendations]
EOF
```

**Event Types Logged**:
- `pilot_candidate_selected`: Week -1 discovery selection
- `pilot_started`: Week 0 research begins
- `pilot_research_completed`: Week 0 research report finished
- `pilot_build_completed`: Weeks 1-3 build phase done
- `pilot_validation_completed`: Week 4 validation data collected
- `pilot_decision_made`: GO/NO-GO decision
- `pilot_completed`: Week 5 formalization done (if GO)
- `vision_updated`: Wave promotion/demotion logged
- `backlog_updated`: Beads epic created/closed

**Data Flow**:
```
Intention Inventory (SAP-010)
  ↓
Week -1 Discovery (SAP-027)
  ↓
Pilot Lifecycle Events → dogfooding.jsonl (SAP-010)
  ↓
Pilot-Candidates Note → knowledge/notes/ (SAP-010)
  ↓
Query for historical analysis
```

**Configuration**:
```yaml
dogfooding:
  memory_integration:
    enabled: true
    event_streams:
      - dogfooding.jsonl        # Pilot lifecycle events
      - vision-updates.jsonl    # Wave promotion/demotion
      - backlog-updates.jsonl   # Epic creation/closure
    knowledge_notes:
      pilot_candidates: .chora/memory/knowledge/notes/pilot-candidates-{date}.md
      lessons_learned: .chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md
    intention_inventory: .chora/memory/knowledge/notes/intention-inventory-{date}.md
```

---

#### Integration with SAP-015 (Task Tracking / Beads)

**Integration Point**: Pilot GO → Beads Epic Creation, Pilot NO-GO → Task Closure

**Purpose**: Cascade pilot decisions into actionable backlog, creating P1 epics for validated features or closing P3 discovery tasks for failed pilots.

**Workflow - Pilot GO (Create Epic)**:
1. Pilot evaluation scores ≥60%
2. Create beads epic with metadata:
   ```bash
   bd create \
     --title "SAP-015: Backlog Organization Patterns" \
     --description "$(cat <<EOF
   Implement backlog organization patterns validated in 4-week pilot.

   **Pilot Evidence**:
   - Satisfaction: 85%
   - Time savings: 6x (30min → 5min)
   - Bugs: 0
   - Pilot ID: pilot-2025-11-05-sap-015

   **Scope**:
   - Priority classification (P0-P3)
   - Status tracking workflow
   - Beads CLI integration
   - Documentation updates
   EOF
   )" \
     --priority P1 \
     --labels "epic,pilot-validated,sap-015" \
     --metadata pilot_id=pilot-2025-11-05-sap-015 \
     --metadata pilot_score=8.2 \
     --metadata satisfaction=85 \
     --metadata time_savings=6x

   # Output: Created issue chora-base-abc (P1 epic)
   ```
3. Break down epic into tasks:
   ```bash
   bd create --title "Implement priority classification" --parent chora-base-abc --priority P1
   bd create --title "Add status tracking workflow" --parent chora-base-abc --priority P1
   bd create --title "Integrate with beads CLI" --parent chora-base-abc --priority P1
   bd create --title "Update documentation" --parent chora-base-abc --priority P2
   ```
4. Log epic creation to A-MEM:
   ```json
   {
     "timestamp": "2025-11-05T16:05:00Z",
     "event_type": "backlog_updated",
     "change": "epic_created",
     "epic_id": "chora-base-abc",
     "pilot_id": "pilot-2025-11-05-sap-015",
     "priority": "P1",
     "estimated_tasks": 12
   }
   ```

**Workflow - Pilot NO-GO (Close Discovery Task)**:
1. Pilot evaluation fails criteria (<60%)
2. Close discovery task (if exists):
   ```bash
   bd close chora-base-xyz \
     --reason "Pilot failed validation (satisfaction: 62%, target: 85%)" \
     --labels "pilot-failed,no-go" \
     --metadata pilot_id=pilot-2025-10-15-sap-033 \
     --metadata lessons_learned_note=lessons-learned-pilot-2025-10-15-sap-033.md

   # Output: Closed issue chora-base-xyz (NO-GO pilot)
   ```
3. Optionally create P3 future task:
   ```bash
   bd create \
     --title "Revisit: Advanced Code Generation (SAP-033)" \
     --description "Pilot showed only 2x time savings. Revisit after improving prompt templates." \
     --priority P3 \
     --labels "deferred,pilot-no-go,sap-033"
   ```
4. Log closure to A-MEM:
   ```json
   {
     "timestamp": "2025-10-22T14:00:00Z",
     "event_type": "backlog_updated",
     "change": "task_closed",
     "task_id": "chora-base-xyz",
     "pilot_id": "pilot-2025-10-15-sap-033",
     "reason": "no_go_decision",
     "lessons_learned": "lessons-learned-pilot-2025-10-15-sap-033.md"
   }
   ```

**Data Flow**:
```
Pilot Decision (SAP-027)
  ↓
  ├─ GO (≥60%)
  │   ↓
  │   Create P1 Epic (SAP-015)
  │   ↓
  │   Break down into tasks
  │   ↓
  │   Log to backlog-updates.jsonl (SAP-010)
  │
  └─ NO-GO (<60%)
      ↓
      Close discovery task (SAP-015)
      ↓
      Create P3 future task (optional)
      ↓
      Log to backlog-updates.jsonl (SAP-010)
```

**Configuration**:
```yaml
dogfooding:
  backlog_integration:
    enabled: true
    go_action:
      create_epic: true
      priority: P1
      labels: ["epic", "pilot-validated"]
      metadata_fields: ["pilot_id", "pilot_score", "satisfaction", "time_savings"]
    no_go_action:
      close_discovery_task: true
      create_future_task: false  # Set to true to create P3 task
      labels: ["pilot-failed", "no-go"]
    time_budget:
      epic_creation: 300  # 5 minutes max
      lessons_logging: 300  # 5 minutes max
```

---

### External Integrations

**GitHub Actions (CI/CD)**:
- **Purpose**: Automate pilot timeline tracking, send reminders for evaluation deadlines
- **Configuration**: `.github/workflows/dogfooding-reminders.yml`
  ```yaml
  name: Dogfooding Pilot Reminders
  on:
    schedule:
      - cron: '0 9 * * 1'  # Every Monday 9am
  jobs:
    check_pilots:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Check active pilots
          run: |
            python scripts/check-pilot-status.py
            # Sends Slack notification if Week 4 evaluation due
  ```

**Slack / Discord (Notifications)**:
- **Purpose**: Notify team of pilot milestones (Week 0 research done, Week 4 evaluation due, GO/NO-GO decision)
- **Configuration**: Webhook URL in `.chora/config.yaml`
  ```yaml
  dogfooding:
    notifications:
      enabled: true
      webhook_url: "https://hooks.slack.com/services/..."
      events: ["research_completed", "evaluation_due", "decision_made"]
  ```

**Claude Code / Claude Desktop (Agent Assistance)**:
- **Purpose**: Execute research, generate pilot-candidates notes, automate scoring calculations
- **Integration**: Via bash scripts and A-MEM context loading
  ```bash
  # Claude Code can query A-MEM for pilot history
  cat .chora/memory/events/dogfooding.jsonl | jq 'select(.event_type == "pilot_completed")'

  # Claude Desktop can generate pilot-candidates note from intention inventory
  # (Provide intention inventory + scoring criteria → output pilot-candidates.md)
  ```

---

## 4. Configuration

SAP-027 configuration is stored in `.chora/config.yaml` under the `dogfooding` section. All settings are optional with sensible defaults.

### Configuration Schema

```yaml
# .chora/config.yaml
dogfooding:
  # Week -1 Discovery Phase
  discovery:
    enabled: true
    time_budget: 7200  # 2 hours in seconds
    scoring:
      evidence_weight: 0.4      # 40%
      alignment_weight: 0.3     # 30%
      demand_weight: 0.2        # 20%
      feasibility_weight: 0.1   # 10%
      threshold: 7.0            # Minimum score for pilot consideration
    demand_sources:
      - type: inbox
        path: inbox/coordination/active.jsonl
        weight: 0.2
      - type: user_feedback
        path: .chora/memory/events/user-feedback.jsonl
        weight: 0.2
    candidate_count:
      min_above_threshold: 3
      max_finalists: 5
      selected: 1

  # 6-Week Pilot Timeline
  pilot:
    timeline:
      research_weeks: 1    # Week 0
      build_weeks: 3       # Weeks 1-3
      validation_weeks: 1  # Week 4
      formalization_weeks: 1  # Week 5 (if GO)
    go_criteria:
      satisfaction_min: 0.85     # 85%
      time_savings_min: 5        # 5x
      bugs_max: 0
      adoption_cases_min: 2
      composite_threshold: 0.6   # 60% overall
    research:
      evidence_levels:
        level_a_min: 0.3    # 30% Level A (standards, peer-reviewed)
        level_b_min: 0.4    # 40% Level B (industry case studies)
        level_c_max: 0.3    # 30% Level C (expert opinion)
      output_path: docs/research/{topic}-research.md
      template_path: docs/templates/research-prompt-template.md

  # Vision Integration (SAP-006)
  vision_integration:
    enabled: true
    promotion_threshold: 0.6  # 60% composite score
    promotion_criteria:
      satisfaction: 0.85
      time_savings: 5
      bugs: 0
    vision_path: .chora/memory/knowledge/notes/vision-{project}-{horizon}.md
    update_strategy: manual  # 'manual' or 'automated'
    wave_mapping:
      promote_from: 2  # Wave 2 (exploratory)
      promote_to: 1    # Wave 1 (committed)
      demote_from: 2
      demote_to: 3     # Wave 3 (future)

  # Memory Integration (SAP-010)
  memory_integration:
    enabled: true
    event_streams:
      - dogfooding.jsonl        # Pilot lifecycle events
      - vision-updates.jsonl    # Wave promotion/demotion
      - backlog-updates.jsonl   # Epic creation/closure
    knowledge_notes:
      pilot_candidates: .chora/memory/knowledge/notes/pilot-candidates-{date}.md
      lessons_learned: .chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md
    intention_inventory: .chora/memory/knowledge/notes/intention-inventory-{date}.md
    event_retention_days: 365  # Keep events for 1 year

  # Backlog Integration (SAP-015)
  backlog_integration:
    enabled: true
    go_action:
      create_epic: true
      priority: P1
      labels:
        - epic
        - pilot-validated
      metadata_fields:
        - pilot_id
        - pilot_score
        - satisfaction
        - time_savings
        - bugs
      auto_breakdown: false  # Auto-create child tasks
    no_go_action:
      close_discovery_task: true
      create_future_task: false  # Create P3 task for revisit
      labels:
        - pilot-failed
        - no-go
    time_budget:
      epic_creation: 300        # 5 minutes max
      lessons_logging: 300      # 5 minutes max

  # Notifications
  notifications:
    enabled: false
    provider: slack  # 'slack', 'discord', 'teams'
    webhook_url: ""  # Set via environment variable
    events:
      - pilot_started
      - research_completed
      - evaluation_due
      - decision_made
      - vision_updated
      - epic_created
    reminder_days_before_deadline: 2

  # Automation
  automation:
    github_actions:
      enabled: false
      workflow_path: .github/workflows/dogfooding-reminders.yml
    scripts:
      score_candidates: scripts/score-pilot-candidates.py
      check_status: scripts/check-pilot-status.py
      generate_report: scripts/generate-pilot-report.py
```

### Configuration Defaults

If `.chora/config.yaml` does not exist or `dogfooding` section is missing, the following defaults are used:

```yaml
dogfooding:
  discovery:
    enabled: true
    time_budget: 7200
    scoring: {evidence_weight: 0.4, alignment_weight: 0.3, demand_weight: 0.2, feasibility_weight: 0.1, threshold: 7.0}
  pilot:
    go_criteria: {satisfaction_min: 0.85, time_savings_min: 5, bugs_max: 0, composite_threshold: 0.6}
  vision_integration: {enabled: true, update_strategy: "manual"}
  memory_integration: {enabled: true}
  backlog_integration: {enabled: true}
  notifications: {enabled: false}
  automation: {github_actions: {enabled: false}}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CHORA_DOGFOODING_ENABLED` | No | `true` | Enable/disable dogfooding patterns |
| `CHORA_DOGFOODING_NOTIFICATION_WEBHOOK` | No | `""` | Webhook URL for notifications (Slack/Discord) |
| `CHORA_DOGFOODING_VISION_PATH` | No | `.chora/memory/knowledge/notes/vision-{project}-{horizon}.md` | Path to vision document |
| `CHORA_DOGFOODING_AUTO_PROMOTION` | No | `false` | Enable automated vision Wave promotion |
| `CHORA_DOGFOODING_AUTO_EPIC_CREATION` | No | `false` | Enable automated beads epic creation on GO |
| `CHORA_DOGFOODING_TIME_BUDGET` | No | `7200` | Time budget for Week -1 discovery (seconds) |

Environment variables override `.chora/config.yaml` settings.

### Configuration Validation

On startup or when running `chora dogfooding validate-config`, the following validations are performed:

1. **Scoring weights sum to 1.0**:
   ```
   evidence_weight + alignment_weight + demand_weight + feasibility_weight = 1.0
   ```
2. **Thresholds in valid ranges**:
   - `scoring.threshold`: 0.0 - 10.0
   - `pilot.go_criteria.*`: satisfaction (0-1), time_savings (>0), bugs (≥0)
   - `vision_integration.promotion_threshold`: 0.0 - 1.0
3. **Required paths exist**:
   - `.chora/memory/events/` directory
   - `.chora/memory/knowledge/notes/` directory (if memory_integration enabled)
   - Vision document path (if vision_integration enabled)
   - `.beads/` directory (if backlog_integration enabled)
4. **Wave mapping consistency**:
   - `promote_from` > `promote_to` (promote to earlier wave)
   - `demote_from` < `demote_to` (demote to later wave)

Validation errors are logged to stderr and prevent dogfooding workflows from running.

### Example Configurations

**Minimal Configuration (Manual Workflow)**:
```yaml
dogfooding:
  discovery:
    enabled: true
  pilot:
    go_criteria:
      satisfaction_min: 0.8  # Lower threshold for experimental projects
  vision_integration:
    enabled: false  # Manual vision updates
  backlog_integration:
    enabled: false  # Manual task creation
```

**Automated Configuration (Production Projects)**:
```yaml
dogfooding:
  discovery:
    enabled: true
    time_budget: 3600  # 1 hour for rapid iteration
  vision_integration:
    enabled: true
    update_strategy: automated  # Auto-promote on GO
  backlog_integration:
    enabled: true
    go_action:
      auto_breakdown: true  # Auto-create child tasks from epic
  notifications:
    enabled: true
    provider: slack
    webhook_url: "${SLACK_WEBHOOK_URL}"  # From environment
  automation:
    github_actions:
      enabled: true
```

---

## 5. Error Handling

SAP-027 defines error codes for discovery, pilot execution, and integration failures. All errors are logged to `.chora/memory/events/errors.jsonl` with timestamps and context.

### Error Codes

| Code | Error | Cause | Resolution |
|------|-------|-------|------------|
| `SAP-027-001` | Discovery timeout | Week -1 discovery exceeded time budget | Increase `discovery.time_budget` in config or manually complete discovery |
| `SAP-027-002` | Insufficient pilot candidates | Fewer than 3 candidates scored above threshold (7.0) | Lower `scoring.threshold` or add more intentions to inventory |
| `SAP-027-003` | Intention inventory not found | Missing `.chora/memory/knowledge/notes/intention-inventory-*.md` | Create intention inventory using SAP-010 or run `chora memory create-intention-inventory` |
| `SAP-027-004` | Invalid scoring weights | Scoring weights don't sum to 1.0 | Adjust weights in config: `evidence + alignment + demand + feasibility = 1.0` |
| `SAP-027-005` | Pilot decision conflict | Manual decision contradicts automated evaluation | Review pilot metrics and update GO/NO-GO criteria in config |
| `SAP-027-006` | Vision update failed | Unable to update vision document (SAP-006) | Check vision path exists, file permissions, and retry manually |
| `SAP-027-007` | Beads epic creation failed | Unable to create beads task (SAP-015) | Verify `.beads/` directory exists, run `bd init`, check beads CLI version |
| `SAP-027-008` | A-MEM logging failed | Unable to write to event stream | Check `.chora/memory/events/` directory exists and is writable |
| `SAP-027-009` | Research phase incomplete | Week 0 research failed evidence level requirements | Revisit research sources, add more Level A/B evidence, or adjust thresholds |
| `SAP-027-010` | Validation phase incomplete | Week 4 validation has fewer than 2 adoption cases | Extend validation period or lower `adoption_cases_min` in config |

### Common Errors

#### Error: Discovery Timeout (SAP-027-001)

**Error Message**:
```
ERROR: Week -1 discovery exceeded time budget (7200s)
Context: Scored 45/89 intentions, 2 hours elapsed
Suggestion: Increase time_budget or complete scoring manually
```

**Cause**:
- Intention inventory too large (>150 intentions)
- Slow evidence lookup or strategic alignment queries
- Network latency when querying remote services

**Solution**:
1. **Quick fix**: Increase time budget in config:
   ```yaml
   dogfooding:
     discovery:
       time_budget: 10800  # 3 hours
   ```
2. **Long-term fix**: Pre-filter intention inventory to exclude low-priority or archived intentions
3. **Manual workaround**: Complete discovery manually, skip automation:
   ```bash
   # Manually create pilot-candidates note
   cat > .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md <<EOF
   [Manual selection summary]
   EOF
   ```

**Logging**:
```json
{"timestamp": "2025-11-05T12:30:00Z", "event_type": "error", "error_code": "SAP-027-001", "message": "Discovery timeout", "context": {"intentions_scored": 45, "intentions_total": 89, "elapsed_seconds": 7200}}
```

---

#### Error: Insufficient Pilot Candidates (SAP-027-002)

**Error Message**:
```
ERROR: Only 2 candidates scored above threshold (7.0), minimum required: 3
Candidates: SAP-015 (8.2), SAP-030 (7.5)
Suggestion: Lower threshold to 6.5 or add more intentions
```

**Cause**:
- Threshold too high for current intention quality
- Intention inventory lacks strategic alignment or evidence
- Demand sources (inbox, user feedback) have low signal

**Solution**:
1. **Adjust threshold**: Lower scoring threshold:
   ```yaml
   dogfooding:
     discovery:
       scoring:
         threshold: 6.5  # Was 7.0
   ```
2. **Enrich intentions**: Add more evidence, strategic rationale, or user requests to existing intentions
3. **Proceed with 2 candidates**: Override minimum if confident in selections:
   ```yaml
   dogfooding:
     discovery:
       candidate_count:
         min_above_threshold: 2  # Was 3
   ```

**Logging**:
```json
{"timestamp": "2025-11-05T11:00:00Z", "event_type": "error", "error_code": "SAP-027-002", "message": "Insufficient pilot candidates", "context": {"candidates_above_threshold": 2, "min_required": 3, "threshold": 7.0}}
```

---

#### Error: Vision Update Failed (SAP-027-006)

**Error Message**:
```
ERROR: Unable to update vision document
Path: .chora/memory/knowledge/notes/vision-chora-base-2025.md
Reason: File not found or permission denied
```

**Cause**:
- Vision document doesn't exist (SAP-006 not adopted)
- Incorrect path in configuration
- File permissions prevent write access

**Solution**:
1. **Check vision file exists**:
   ```bash
   ls -la .chora/memory/knowledge/notes/vision-*.md
   ```
2. **Create vision document** (if missing):
   ```bash
   # Use SAP-006 to create vision
   chora vision create --project chora-base --horizon 2025
   ```
3. **Fix path in config**:
   ```yaml
   dogfooding:
     vision_integration:
       vision_path: .chora/memory/knowledge/notes/vision-chora-base-2025.md  # Correct path
   ```
4. **Manual update**: Edit vision document manually and log event to A-MEM:
   ```bash
   echo '{"timestamp":"2025-11-05T16:00:00Z","event_type":"vision_updated","change":"wave_promotion","feature":"Backlog Organization","from_wave":2,"to_wave":1}' >> .chora/memory/events/vision-updates.jsonl
   ```

**Logging**:
```json
{"timestamp": "2025-11-05T16:00:00Z", "event_type": "error", "error_code": "SAP-027-006", "message": "Vision update failed", "context": {"vision_path": ".chora/memory/knowledge/notes/vision-chora-base-2025.md", "reason": "file_not_found"}}
```

---

#### Error: Beads Epic Creation Failed (SAP-027-007)

**Error Message**:
```
ERROR: Unable to create beads epic for pilot-2025-11-05-sap-015
Command: bd create --title "SAP-015: Backlog Organization Patterns" ...
Exit code: 1
Stderr: Error: .beads/ directory not initialized. Run 'bd init' first.
```

**Cause**:
- Beads not initialized (`.beads/` directory missing)
- Beads CLI not installed or wrong version
- Git repository not configured

**Solution**:
1. **Initialize beads** (if not initialized):
   ```bash
   bd init
   ```
2. **Install beads CLI** (if missing):
   ```bash
   npm install -g @beads/bd
   # Or use project-local install
   npm install --save-dev @beads/bd
   ```
3. **Check beads version**:
   ```bash
   bd --version  # Should be ≥1.0.0
   ```
4. **Manual epic creation**: If automation fails, create task manually via beads CLI or web UI, then log to A-MEM:
   ```bash
   bd create --title "SAP-015: Backlog Organization Patterns" --priority P1
   # Log event
   echo '{"timestamp":"2025-11-05T16:05:00Z","event_type":"backlog_updated","change":"epic_created","epic_id":"chora-base-abc"}' >> .chora/memory/events/backlog-updates.jsonl
   ```

**Logging**:
```json
{"timestamp": "2025-11-05T16:05:00Z", "event_type": "error", "error_code": "SAP-027-007", "message": "Beads epic creation failed", "context": {"pilot_id": "pilot-2025-11-05-sap-015", "command": "bd create", "exit_code": 1, "stderr": "Error: .beads/ directory not initialized"}}
```

---

#### Error: Research Phase Incomplete (SAP-027-009)

**Error Message**:
```
ERROR: Week 0 research failed evidence level requirements
Evidence levels: Level A: 18%, Level B: 35%, Level C: 47%
Required: Level A ≥30%, Level B ≥40%, Level C ≤30%
```

**Cause**:
- Insufficient high-quality research sources (Level A: standards, peer-reviewed papers)
- Too much reliance on blogs, expert opinion (Level C)
- Topic has limited published research

**Solution**:
1. **Add more Level A/B sources**:
   - Search academic databases (IEEE, ACM, arXiv)
   - Review official standards (IETF RFCs, W3C specs, OWASP guidelines)
   - Find industry case studies (engineering blogs from major companies)
2. **Adjust thresholds** (if domain inherently has low research):
   ```yaml
   dogfooding:
     pilot:
       research:
         evidence_levels:
           level_a_min: 0.2  # Lower to 20%
           level_c_max: 0.4  # Allow 40% Level C
   ```
3. **Document rationale**: If evidence is unavailable, log why and proceed:
   ```markdown
   ## Research Report: {Topic}

   **Evidence Limitation**: This domain has limited published research.
   Proceeding with 18% Level A, rationale: [Explanation]
   ```

**Logging**:
```json
{"timestamp": "2025-11-05T10:00:00Z", "event_type": "error", "error_code": "SAP-027-009", "message": "Research phase incomplete", "context": {"evidence_levels": {"level_a": 0.18, "level_b": 0.35, "level_c": 0.47}, "required": {"level_a_min": 0.3, "level_b_min": 0.4, "level_c_max": 0.3}}}
```

---

### Recovery Strategies

When errors occur, SAP-027 provides automatic recovery strategies based on error severity:

| Error Code | Severity | Auto-Recovery | Manual Recovery Required |
|------------|----------|---------------|-------------------------|
| SAP-027-001 | Warning | Extend time budget | No |
| SAP-027-002 | Warning | Lower threshold | No |
| SAP-027-003 | Critical | Abort | Yes - Create intention inventory |
| SAP-027-004 | Critical | Abort | Yes - Fix config weights |
| SAP-027-005 | Warning | Use manual decision | No |
| SAP-027-006 | Warning | Skip vision update | Optional - Update manually |
| SAP-027-007 | Warning | Skip epic creation | Optional - Create manually |
| SAP-027-008 | Warning | Continue without logging | Optional - Fix event stream |
| SAP-027-009 | Warning | Proceed with rationale | Optional - Add more evidence |
| SAP-027-010 | Warning | Extend validation period | Optional - Lower adoption minimum |

**Auto-Recovery Behavior**:
- **Warning**: Log error, attempt recovery (extend timeout, adjust threshold), continue workflow
- **Critical**: Log error, abort workflow, require manual intervention

**Manual Recovery Workflow**:
1. Check error logs: `cat .chora/memory/events/errors.jsonl | grep SAP-027`
2. Identify root cause from error context
3. Apply resolution from table above
4. Retry workflow: `chora dogfooding retry {pilot-id}`
5. Verify success: Check A-MEM for completion events

---

### Debugging Guidance

**Enable Debug Logging**:
```bash
export CHORA_LOG_LEVEL=debug
export CHORA_DOGFOODING_DEBUG=true
```

**Query Error History**:
```bash
# All dogfooding errors
cat .chora/memory/events/errors.jsonl | jq 'select(.error_code | startswith("SAP-027"))'

# Errors for specific pilot
cat .chora/memory/events/errors.jsonl | jq 'select(.context.pilot_id == "pilot-2025-11-05-sap-015")'

# Error frequency by code
cat .chora/memory/events/errors.jsonl | jq -r 'select(.error_code | startswith("SAP-027")) | .error_code' | sort | uniq -c
```

**Common Debug Scenarios**:

1. **Discovery scoring produces unexpected results**:
   ```bash
   # Dry-run scoring with verbose output
   python scripts/score-pilot-candidates.py --dry-run --verbose
   ```

2. **Vision integration not working**:
   ```bash
   # Validate vision path
   echo $CHORA_DOGFOODING_VISION_PATH
   cat .chora/config.yaml | grep vision_path
   ls -la .chora/memory/knowledge/notes/vision-*.md
   ```

3. **Beads epic creation fails silently**:
   ```bash
   # Test beads CLI manually
   bd list --status open
   bd create --title "Test Epic" --priority P1 --dry-run
   ```

**Log Levels**:
- `ERROR`: Critical failures, workflow aborted
- `WARN`: Recoverable failures, workflow continues
- `INFO`: Normal operations (candidate scored, epic created)
- `DEBUG`: Detailed trace (config loaded, query executed)

---

## 6. Security Considerations

SAP-027 stores pilot data (metrics, decisions, evidence) in plaintext files within the repository. The following security considerations apply:

### Data Sensitivity

**Low-Sensitivity Data** (no special protection needed):
- Pilot timelines, phase dates
- GO/NO-GO decisions (binary outcomes)
- Time savings calculations, satisfaction scores
- Adoption case descriptions (if anonymized)

**Medium-Sensitivity Data** (protect from public exposure):
- User feedback verbatims (may contain names, team details)
- Internal strategic priorities (Wave 1/Wave 2 vision details)
- Failed pilot details (competitive intelligence if disclosed)

**High-Sensitivity Data** (exclude from repository):
- Personally identifiable information (PII) - names, emails, demographics
- Proprietary algorithms or trade secrets
- Customer data or confidential partnerships

### Secret Management

**Webhook URLs** (Slack, Discord notifications):
- Store in environment variables, NOT in `.chora/config.yaml`:
  ```yaml
  dogfooding:
    notifications:
      webhook_url: "${SLACK_WEBHOOK_URL}"  # Read from env
  ```
- Use `.env` files with `.gitignore` protection
- Rotate webhooks if leaked

**API Keys** (if querying external services for research):
- Use environment variables: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
- Never commit to git
- Use secret managers in CI/CD (GitHub Secrets, AWS Secrets Manager)

### Access Control

**Repository Permissions**:
- `.chora/memory/events/*.jsonl`: Readable by all contributors
- `.chora/memory/knowledge/notes/`: Readable by all contributors
- `docs/pilots/`: Readable by all contributors
- Sensitive pilot reports: Use private repos or branch protection

**Pilot Report Redaction**:
- Before committing pilot reports, redact:
  - User names → "User A", "User B"
  - Team names → "Team 1", "Team 2"
  - Proprietary metrics → "X% improvement" (no absolute numbers if sensitive)

### Security Best Practices

1. **Anonymize user feedback**: Replace names with pseudonyms before logging
2. **Review pilot reports before commit**: Check for accidental PII or secrets
3. **Use private repos for sensitive pilots**: If pilot involves unreleased features
4. **Rotate secrets regularly**: Webhooks, API keys every 90 days
5. **Audit event logs periodically**: Check for accidental data leaks

### Known Vulnerabilities and Mitigations

**Vulnerability 1: Plaintext Storage of Strategic Plans**
- **Risk**: Competitors could access vision documents in public repos
- **Mitigation**: Use private repos for strategic planning, or use code names for features
- **Severity**: Medium

**Vulnerability 2: Webhook URL Exposure**
- **Risk**: Leaked webhook URLs allow unauthorized notifications
- **Mitigation**: Store in environment variables, rotate on leak
- **Severity**: Low

**Vulnerability 3: Pilot Report PII Leakage**
- **Risk**: User names/emails in feedback quotes committed to git history
- **Mitigation**: Pre-commit hook to scan for PII patterns, manual review
- **Severity**: High (compliance risk if GDPR/CCPA applies)

**Mitigation Script** (pre-commit hook):
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Scan for PII in pilot reports before commit

FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'docs/pilots/.*\.md')

for FILE in $FILES; do
  # Check for email patterns
  if grep -qE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$FILE"; then
    echo "❌ ERROR: Email address detected in $FILE"
    echo "Please anonymize before committing."
    exit 1
  fi

  # Check for phone numbers
  if grep -qE '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b' "$FILE"; then
    echo "❌ ERROR: Phone number detected in $FILE"
    exit 1
  fi
done

exit 0
```

**No Critical Vulnerabilities**: SAP-027 does not handle authentication, network requests, or code execution beyond shell scripts. Attack surface is minimal.

---

## 7. Performance Requirements

SAP-027 is a human-driven methodology, not a high-throughput system. Performance targets focus on **time-to-completion** and **human efficiency** rather than computational speed.

### Performance Targets

| Phase | Target Time | Acceptable Range | Measurement |
|-------|-------------|------------------|-------------|
| **Week -1: Discovery** | ≤2 hours | 1-3 hours | Start scoring → pilot selection |
| **Week 0: Research** | 4-6 hours | 3-8 hours | Research initiation → report completion |
| **Weeks 1-3: Build** | 15-30 hours | 10-40 hours | First commit → feature complete |
| **Week 4: Validation** | 2-4 hours | 1-6 hours | First use → final metrics logged |
| **Week 4 End: Decision** | ≤1 hour | 30 min - 2 hours | Metrics review → GO/NO-GO written |
| **Week 5: Formalization** | 4-8 hours | 3-12 hours | TODO completion → production-ready |
| **Total Pilot Duration** | 25-50 hours | 20-70 hours | Discovery → formalization |

**Target Definition**:
- **Target Time**: Optimal time for experienced practitioners
- **Acceptable Range**: Expected variation based on complexity, research availability, pilot scope
- **Measurement**: Wall-clock time from phase start event to phase completion event (logged in A-MEM)

### Throughput Targets

SAP-027 is serial by design (one pilot at a time per capability domain). Parallelization is possible across independent domains.

| Scenario | Target Throughput | Notes |
|----------|-------------------|-------|
| **Sequential Pilots** | 1 pilot / 6 weeks | Standard single-pilot workflow |
| **Parallel Pilots** (independent domains) | 2-3 pilots / 6 weeks | Requires dedicated resources per pilot |
| **Continuous Pipeline** | 8-10 pilots / year | Realistic for small teams (1-2 people) |
| **High-Velocity Pipeline** | 15-20 pilots / year | Requires dedicated team (3-5 people) |

**Bottlenecks**:
- Week 0 research (4-6 hours per pilot, requires focused time)
- Week 5 formalization (4-8 hours TODO completion)
- Validation phase requires real-world usage (cannot be accelerated)

### Resource Usage Limits

SAP-027 has minimal computational footprint:

| Resource | Target | Limit | Notes |
|----------|--------|-------|-------|
| **Disk Space** | <10 MB / pilot | 50 MB / pilot | Pilot reports, research PDFs, A-MEM events |
| **Memory** | <50 MB | 200 MB | Python scoring scripts, CLI tools |
| **Network** | <100 MB / pilot | 500 MB / pilot | Research sources, documentation fetches |
| **Git Commits** | 10-20 / pilot | 50 / pilot | Phase milestones, formalization edits |

**Storage Growth**:
- Per pilot: ~5-10 MB (pilot report, research, A-MEM events)
- Per year (10 pilots): ~50-100 MB
- 5-year projection (50 pilots): ~250-500 MB (negligible)

### Scalability Considerations

**Horizontal Scaling** (more pilots in parallel):
- **Constraint**: Human attention (each pilot requires focused design work)
- **Recommendation**: Max 3 parallel pilots per person
- **Team scaling**: Linear (2 people → 6 pilots, 5 people → 15 pilots per 6-week cycle)

**Vertical Scaling** (faster pilots):
- **Optimization 1**: Pre-research (maintain evidence library, reduce Week 0 from 6h → 2h)
- **Optimization 2**: Template reuse (standardize adoption-blueprint TODOs, reduce Week 5 from 8h → 3h)
- **Optimization 3**: Automation (auto-generate pilot-candidates notes, reduce Week -1 from 2h → 30min)
- **Realistic speedup**: 50% time savings after 10+ pilots (cumulative learning)

**Limits**:
- Cannot parallelize within a single pilot (phases are sequential)
- Cannot accelerate validation phase (requires real-world usage over time)
- Diminishing returns after 20+ pilots (most patterns already validated)

### Performance Monitoring

**Key Metrics** (logged to A-MEM):
```json
{
  "timestamp": "2025-11-05T16:00:00Z",
  "event_type": "pilot_completed",
  "pilot_id": "pilot-2025-11-05-sap-015",
  "performance": {
    "discovery_hours": 1.5,
    "research_hours": 5.2,
    "build_hours": 22.0,
    "validation_hours": 3.5,
    "decision_hours": 0.8,
    "formalization_hours": 6.5,
    "total_hours": 39.5
  }
}
```

**Dashboard Query**:
```bash
# Average pilot duration (last 10 pilots)
cat .chora/memory/events/dogfooding.jsonl | jq -r 'select(.event_type == "pilot_completed") | .performance.total_hours' | tail -10 | awk '{sum+=$1; count++} END {print "Average:", sum/count, "hours"}'

# Expected output: Average: 42.3 hours
```

**Performance Alerts**:
- If discovery > 3 hours: Consider intention inventory pre-filtering
- If research > 8 hours: Delegate research to assistant, focus on synthesis
- If build > 40 hours: Reduce pilot scope or split into 2 pilots
- If formalization > 12 hours: Improve template quality, reduce TODOs

**Optimization Feedback Loop**:
1. Log pilot performance metrics to A-MEM
2. Quarterly review: Analyze average duration per phase
3. Identify bottlenecks (e.g., "Research phase averaging 9h, target: 6h")
4. Implement optimization (e.g., pre-research templates)
5. Measure improvement in next 3 pilots

**Performance SLA**: None (internal workflow, no external SLA). Target: 80% of pilots complete within 6 weeks (42 days).

---

## 8. Examples

### Example 1: Level 1 Pilot (Build + Validate Only)

**Scenario**: First-time user wants to validate a simple capability (priority classification for tasks) using the simplified Level 1 workflow.

**Context**:
- User has 3 projects needing task prioritization
- No strategic vision document yet (SAP-006 not adopted)
- Beads not yet integrated (SAP-015 not adopted)
- Time budget: 3-4 hours

**Workflow**:

```bash
# Step 1: Create pilot plan (simplified, no discovery phase)
mkdir -p docs/pilots/
cat > docs/pilots/pilot-2025-11-05-priority-classification.md <<'EOF'
# Pilot: Task Priority Classification

## Goal
Reduce task triage time from 30 minutes → 5 minutes using P0-P3 priority framework.

## Build Phase (Weeks 1-2)
- [ ] Define P0-P3 criteria (urgency, impact, effort)
- [ ] Document priority decision tree
- [ ] Create examples for each priority level

## Validate Phase (Week 3)
- [ ] Apply to 3 projects (10 tasks each)
- [ ] Track time per project (before: 30min, after: ?)
- [ ] Rate satisfaction (1-5 scale)
- [ ] Note any bugs or confusion

## Decision
- Continue if: Time savings ≥5x, satisfaction ≥4/5, bugs = 0
- Next steps: Formalize into SAP if GO
EOF

# Step 2: Build the capability (Weeks 1-2)
# (User implements priority classification system)

# Step 3: Validation (Week 3) - Use 3 times
# Project 1: 10 tasks prioritized
# Time: 6 minutes (was 30 min)
# Satisfaction: 5/5 (clear criteria, easy to apply)
# Bugs: 0

# Project 2: 10 tasks prioritized
# Time: 4 minutes
# Satisfaction: 5/5
# Bugs: 0

# Project 3: 10 tasks prioritized
# Time: 5 minutes
# Satisfaction: 4/5 (slight confusion on P1 vs P2 boundary)
# Bugs: 0

# Step 4: Calculate metrics
echo "Average time: (6+4+5)/3 = 5 minutes (was 30 min)"
echo "Time savings: 30/5 = 6x ✅"
echo "Satisfaction: (5+5+4)/3 = 4.67/5 = 93% ✅"
echo "Bugs: 0 ✅"

# Step 5: GO decision
cat >> docs/pilots/pilot-2025-11-05-priority-classification.md <<'EOF'

## Results
- **Time savings**: 6x (30 min → 5 min) ✅
- **Satisfaction**: 93% (4.67/5) ✅
- **Bugs**: 0 ✅
- **Decision**: GO - Formalize into SAP-015 enhancement

## Next Steps
1. Complete TODO markers in adoption-blueprint.md
2. Add priority classification to protocol-spec.md
3. Update ledger with pilot results
EOF
```

**Expected Output**:
```
✅ Pilot completed in 3 hours
✅ GO decision (6x time savings, 93% satisfaction, 0 bugs)
✅ Ready for formalization
```

**Time Breakdown**:
- Build: 1.5 hours (documentation, examples)
- Validation: 0.5 hours (3 uses × 10 min)
- Decision: 1 hour (metrics calculation, write-up)
- **Total**: 3 hours

---

### Example 2: Level 2 Full Pilot (Research + Build + Validate + Decide)

**Scenario**: Experienced user wants to validate a complex capability (database migration patterns) using the complete 6-week workflow with research phase.

**Context**:
- SAP-010 (Memory System) adopted: Intention inventory exists
- SAP-006 (Vision Synthesis) adopted: Wave 2 feature to validate
- SAP-015 (Beads) adopted: Will create epic if GO
- Time budget: 6-8 hours

**Workflow**:

```bash
# Week -1: Discovery (1.5 hours)
# Query intention inventory for database-related intentions
cat .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md | grep -i "database\|migration"

# Output:
# INT-042: Database migration automation (status: validated, evidence: medium)
# INT-089: Schema versioning patterns (status: proposed, evidence: low)
# INT-103: Zero-downtime migrations (status: prioritized, evidence: high)

# Score candidates using 4-criteria model
python scripts/score-pilot-candidates.py \
  --inventory intention-inventory-2025-11-05.md \
  --filter "database" \
  --output pilot-candidates-2025-11-05.md

# Output: pilot-candidates-2025-11-05.md
# Top candidate: INT-103 (Zero-downtime migrations), score: 8.5
# - Evidence: 9/10 (multiple Level A sources: Stripe, GitHub eng blogs)
# - Alignment: 8/10 (Wave 2 exploratory, fits strategic priorities)
# - Demand: 9/10 (12 coordination requests from 4 projects)
# - Feasibility: 8/10 (2-week build, moderate risk)

# Select INT-103 for pilot
echo "Selected: INT-103 (Zero-downtime migrations)"

# Week 0: Research Phase (5 hours)
# Use research prompt template
just research "zero-downtime database migrations for Python projects"

# Output: docs/research/zero-downtime-migrations-research.md
# - 10-page report
# - Evidence: 35% Level A, 45% Level B, 20% Level C ✅
# - Principles: Blue-green deployments, backward-compatible schema changes
# - Decision playbooks: "Use expand-contract for breaking changes"
# - Metrics: Target <1s downtime, 99.99% success rate

# Weeks 1-3: Build Phase (22 hours)
# Implement zero-downtime migration patterns based on research
# (User implements capability, tracks time)

# Week 4: Validation Phase (3.5 hours)
# Apply to 2 production migrations
# Migration 1: Add column (backward-compatible)
#   - Time: 45 min (was 2 hours planning + 1 hour downtime)
#   - Downtime: 0 seconds ✅
#   - Satisfaction: 5/5
#   - Bugs: 0

# Migration 2: Rename column (breaking change, expand-contract)
#   - Time: 90 min (was 3 hours + 5 min downtime)
#   - Downtime: 0 seconds ✅
#   - Satisfaction: 5/5
#   - Bugs: 0

# Week 4 End: Decision Phase (45 min)
# Calculate metrics
echo "Time savings: (180+185)/(45+90) = 2.7x ❌ (target: 5x)"
echo "Satisfaction: 100% ✅"
echo "Bugs: 0 ✅"
echo "Downtime: 0s ✅ (was 65s)"

# NO-GO decision (time savings < 5x)
cat > docs/pilots/go-no-go-decision-2025-11-05-zero-downtime.md <<'EOF'
## GO/NO-GO Decision: Zero-Downtime Migrations

### Metrics
- Time savings: 2.7x ❌ (target: 5x)
- Satisfaction: 100% ✅
- Bugs: 0 ✅
- Downtime reduction: 100% (65s → 0s) ✅

### Decision: NO-GO (conditional)
**Rationale**: Time savings (2.7x) below threshold (5x). However, downtime elimination is strategically critical for production systems.

**Lessons Learned**:
1. Expand-contract pattern adds upfront complexity (90 min vs 45 min)
2. Value is in risk reduction (downtime), not time savings
3. Recommend revisiting with different success criteria (downtime < 1s instead of time savings 5x)

### Next Steps
1. Close discovery task (SAP-015)
2. Create P3 future task: "Revisit zero-downtime migrations with risk-focused criteria"
3. Log to A-MEM and vision document (demote to Wave 3)
EOF

# Integration: Close beads task, demote in vision
bd close chora-base-xyz --reason "NO-GO: Time savings 2.7x < 5x threshold"
# (Manual: Update vision-chora-base-2025.md: Move INT-103 from Wave 2 → Wave 3)

# Log to A-MEM
echo '{"timestamp":"2025-11-19T16:00:00Z","event_type":"pilot_decision_made","pilot_id":"pilot-2025-11-05-int-103","decision":"NO_GO","reason":"time_savings_below_threshold","scores":{"time_savings":"2.7x","satisfaction":1.0,"bugs":0}}' >> .chora/memory/events/dogfooding.jsonl
```

**Expected Output**:
```
❌ NO-GO decision (time savings 2.7x < 5x)
✅ Lessons learned documented
✅ Vision updated (Wave 2 → Wave 3)
✅ P3 task created for future revisit
```

**Time Breakdown**:
- Discovery: 1.5 hours
- Research: 5 hours
- Build: 22 hours
- Validation: 3.5 hours
- Decision: 0.75 hours
- **Total**: 32.75 hours

---

### Example 3: Level 3 Multi-Pilot Automation

**Scenario**: Production team running 3 pilots simultaneously with automation infrastructure.

**Context**:
- All SAPs integrated (SAP-006, SAP-010, SAP-015)
- Automation scripts deployed (score-candidates, check-status, dashboard)
- GitHub Actions reminders configured
- Time budget: 1-2 hours per pilot (after 12-16 hour infrastructure setup)

**Workflow**:

```bash
# Infrastructure setup (one-time, 12-16 hours)
# (Already completed: start-pilot.sh, dashboard.py, sync-to-vision.sh)

# Daily workflow (5 minutes)
# Check pilot dashboard
python scripts/pilot-dashboard.py

# Output:
# ============================================================
# PILOT DASHBOARD
# ============================================================
# Active Pilots: 3
# Completed Pilots: 7
#
# Success Rate: 70% (7 GO, 3 NO-GO)
#
# Recent Pilots:
#   - pilot-2025-11-01-sap-030: pilot_completed (GO)
#   - pilot-2025-10-25-sap-016: pilot_no_go_decision
#   - pilot-2025-10-18-sap-017: pilot_completed (GO)
#
# Active Pilots (Week 4 evaluation due):
#   - pilot-2025-11-05-sap-015 (Backlog Organization) - Due: 2025-12-03
#   - pilot-2025-11-12-sap-018 (Form Validation) - Due: 2025-12-10
#   - pilot-2025-11-19-sap-019 (Self-Evaluation) - Due: 2025-12-17

# Start new pilot (automated, 1 hour)
# Discovery already done (intention inventory pre-filtered to top 10)
bash scripts/start-pilot.sh --intention INT-156 --fast

# Output:
# ✅ Pilot started: pilot-2025-11-26-sap-020
# ✅ Research prompt generated: docs/research/error-handling-research.md
# ✅ A-MEM event logged: pilot_started
# ✅ Beads task created: chora-base-def (P3 discovery)
# ✅ Slack notification sent
#
# Next steps:
# 1. Execute research (4-6 hours): just research "error handling patterns"
# 2. Build capability (Weeks 1-3)
# 3. Reminder: Week 4 evaluation due 2025-12-24

# Complete pilot evaluation (automated, 30 min)
# (User has collected validation metrics manually)
bash scripts/complete-pilot.sh \
  --pilot pilot-2025-11-05-sap-015 \
  --time-before 30 \
  --time-after 5 \
  --satisfaction 0.85 \
  --bugs 0 \
  --adoption-cases 4

# Output:
# ✅ Metrics calculated:
#   - Time savings: 6x ✅
#   - Satisfaction: 85% ✅
#   - Bugs: 0 ✅
#   - Adoption cases: 4 ✅
# ✅ GO decision (composite score: 0.87)
# ✅ Beads epic created: chora-base-abc (P1)
# ✅ Vision updated: Wave 2 → Wave 1
# ✅ A-MEM events logged (pilot_completed, vision_updated, backlog_updated)
# ✅ Slack notification sent
#
# Next steps:
# 1. Formalize SAP-015 (Week 5, 4-8 hours)
# 2. Break down epic into tasks: bd create --parent chora-base-abc ...

# Sync all pilots to vision (weekly, 10 minutes)
bash scripts/sync-to-vision.sh

# Output:
# ✅ Synced 7 completed pilots to vision document
# ✅ 5 GO decisions → Wave 1
# ✅ 2 NO-GO decisions → Wave 3
# ✅ Vision coherence score: 0.92 (high alignment)
```

**Expected Output**:
```
✅ 3 pilots running in parallel
✅ New pilot started in 1 hour (was 2 hours)
✅ Pilot evaluation completed in 30 min (was 1 hour)
✅ Vision sync automated (weekly, 10 min)
✅ Time savings: 60% per pilot
```

**Time Breakdown (per pilot after infrastructure)**:
- Discovery: 30 min (was 2 hours)
- Research: 5 hours (same, cannot automate)
- Build: 20 hours (same)
- Validation: 3 hours (same)
- Decision: 30 min (was 1 hour)
- **Total**: 29 hours (was 32.5 hours, 11% savings)

**Cumulative Savings** (10 pilots):
- Manual: 10 × 32.5h = 325 hours
- Level 3: 16h setup + (10 × 29h) = 306 hours
- **Savings**: 19 hours (6%)

**Note**: Level 3 pays off after 20+ pilots (50% savings on discovery, decision, and vision sync tasks).

---

## 9. Validation & Testing

SAP-027 validation ensures pilot methodology is correctly implemented and integrated with SAP-006, SAP-010, and SAP-015.

### Validation Commands

```bash
# Quick validation (30 seconds) - Verify SAP-027 artifacts and configuration
python scripts/sap-evaluator.py --quick SAP-027

# Expected output:
# ✅ SAP-027 (dogfooding-patterns)
#    Level: 1 (Basic Adoption)
#    Next: Level 2 (requires 2+ pilots completed)
# ✅ Configuration valid
# ✅ Integration SAPs detected: SAP-010 (Memory), SAP-015 (Task Tracking)
# ⚠️  SAP-006 (Vision Synthesis) not detected - optional

# Full validation (detailed report)
python scripts/sap-evaluator.py SAP-027

# Expected output:
# SAP-027: Dogfooding Patterns
# Status: pilot
# Version: 1.1.0
#
# Artifacts:
# ✅ capability-charter.md (complete)
# ✅ protocol-spec.md (complete)
# ✅ awareness-guide.md (complete)
# ✅ adoption-blueprint.md (complete)
# ✅ ledger.md (complete)
#
# Integration Health:
# ✅ SAP-010 integration: .chora/memory/events/dogfooding.jsonl exists
# ✅ SAP-015 integration: .beads/ directory exists
# ⚠️  SAP-006 integration: vision document not found (optional)
#
# Pilot History:
# 📊 Pilots completed: 2
# 📊 GO decisions: 1 (50%)
# 📊 NO-GO decisions: 1 (50%)
# 📊 Average pilot duration: 38.5 hours

# Validate configuration file
python scripts/validate-dogfooding-config.py

# Expected output:
# ✅ Configuration valid
# ✅ Scoring weights sum to 1.0
# ✅ GO criteria thresholds in valid ranges
# ✅ Required directories exist
# ✅ Event streams writable

# Check for active pilots
cat .chora/memory/events/dogfooding.jsonl | jq 'select(.event_type == "pilot_started")' | tail -5

# Expected output (if pilots active):
# {"timestamp":"2025-11-05T10:00:00Z","event_type":"pilot_started","pilot_id":"pilot-2025-11-05-sap-015"}

# Validate pilot report structure
python scripts/validate-pilot-report.py docs/pilots/pilot-2025-11-05-sap-015.md

# Expected output:
# ✅ Pilot ID present
# ✅ Metrics section exists
# ✅ GO/NO-GO decision documented
# ✅ Time savings calculated
# ✅ Satisfaction score recorded
# ✅ Bug count recorded
```

### Test Cases

**Test Case 1: Week -1 Discovery (Happy Path)**
- **Given**: Intention inventory with 89 intentions, 12 above threshold (7.0)
- **When**: Run `python scripts/score-pilot-candidates.py --inventory intention-inventory-2025-11-05.md`
- **Then**:
  - Pilot-candidates note created in `.chora/memory/knowledge/notes/`
  - Top 5 candidates identified
  - Weighted scores calculated correctly
  - Selection decision logged to A-MEM (dogfooding.jsonl)
  - Completion time ≤2 hours

**Test Case 2: Week 0 Research Phase (Happy Path)**
- **Given**: Selected pilot candidate with domain topic
- **When**: Execute research workflow `just research "task tracking patterns"`
- **Then**:
  - Research report generated in `docs/research/`
  - Evidence levels: ≥30% Level A, ≥40% Level B, ≤30% Level C
  - Report includes principles, practices, decision playbooks, anti-patterns
  - Research completion event logged to A-MEM
  - Completion time: 4-6 hours

**Test Case 3: Week 4 GO Decision (Happy Path)**
- **Given**: Pilot with metrics: time savings 6x, satisfaction 85%, bugs 0, adoption cases 4
- **When**: Run `bash scripts/complete-pilot.sh --pilot pilot-2025-11-05-sap-015 --time-before 30 --time-after 5 --satisfaction 0.85 --bugs 0 --adoption-cases 4`
- **Then**:
  - GO decision calculated (composite score ≥0.6)
  - Beads epic created (P1) with pilot metadata
  - Vision document updated (Wave 2 → Wave 1)
  - A-MEM events logged: `pilot_completed`, `vision_updated`, `backlog_updated`
  - Slack notification sent (if enabled)

**Test Case 4: Week 4 NO-GO Decision (Failure Path)**
- **Given**: Pilot with metrics: time savings 2.7x, satisfaction 100%, bugs 0
- **When**: Manual evaluation (time savings < 5x threshold)
- **Then**:
  - NO-GO decision documented with rationale
  - Beads discovery task closed with reason
  - Vision document updated (Wave 2 → Wave 3)
  - Lessons learned note created in `.chora/memory/knowledge/notes/`
  - A-MEM event logged: `pilot_decision_made` (decision: NO_GO)

**Test Case 5: Configuration Validation (Error Path)**
- **Given**: `.chora/config.yaml` with invalid scoring weights (sum = 0.95, not 1.0)
- **When**: Run `python scripts/validate-dogfooding-config.py`
- **Then**:
  - Validation fails with error: `SAP-027-004: Invalid scoring weights`
  - Stderr output: "Scoring weights sum to 0.95, expected 1.0"
  - Suggested fix: "Adjust weights: evidence + alignment + demand + feasibility = 1.0"
  - Exit code: 1

**Test Case 6: Discovery Timeout (Error Path)**
- **Given**: Intention inventory with 200 intentions, time budget 2 hours (7200s)
- **When**: Discovery process runs for 2 hours without completing
- **Then**:
  - Discovery aborts with error: `SAP-027-001: Discovery timeout`
  - Partial results saved (intentions scored so far)
  - A-MEM error event logged
  - Suggested recovery: Increase time budget or pre-filter inventory
  - Exit code: 1

**Test Case 7: Integration with SAP-015 (Beads) - Epic Creation**
- **Given**: GO decision for pilot-2025-11-05-sap-015, beads initialized (`.beads/` exists)
- **When**: Run `bd create --title "SAP-015: Backlog Organization" --priority P1 --metadata pilot_id=pilot-2025-11-05-sap-015`
- **Then**:
  - Beads epic created with ID (e.g., `chora-base-abc`)
  - Epic contains pilot metadata (pilot_id, pilot_score, satisfaction, time_savings)
  - Epic priority set to P1
  - Epic labels include "epic", "pilot-validated"
  - A-MEM event logged: `backlog_updated` (change: epic_created)

**Test Case 8: Integration with SAP-010 (A-MEM) - Event Logging**
- **Given**: Active pilot at Week 4 validation phase
- **When**: Validation phase completes
- **Then**:
  - Event logged to `.chora/memory/events/dogfooding.jsonl`:
    ```json
    {"timestamp":"2025-12-03T16:00:00Z","event_type":"pilot_validation_completed","pilot_id":"pilot-2025-11-05-sap-015","metrics":{"time_savings":"6x","satisfaction":0.85,"bugs":0,"adoption_cases":4}}
    ```
  - Event is valid JSON (parseable by `jq`)
  - Event contains all required fields (timestamp, event_type, pilot_id, metrics)

**Test Case 9: Multi-Pilot Parallelization (Scalability Test)**
- **Given**: 3 pilots running simultaneously (pilot-2025-11-05-sap-015, pilot-2025-11-12-sap-018, pilot-2025-11-19-sap-019)
- **When**: Run `python scripts/pilot-dashboard.py`
- **Then**:
  - Dashboard displays all 3 active pilots
  - Each pilot shows phase, due date, estimated completion
  - No resource conflicts (disk, memory, network)
  - Dashboard response time <1 second

**Test Case 10: Evidence Level Validation (Research Phase)**
- **Given**: Research report with 18% Level A, 35% Level B, 47% Level C evidence
- **When**: Run `python scripts/validate-research-evidence.py docs/research/task-tracking-research.md`
- **Then**:
  - Validation fails with error: `SAP-027-009: Research phase incomplete`
  - Error details: "Level A: 18% (required ≥30%), Level C: 47% (required ≤30%)"
  - Suggested fix: "Add more Level A sources (standards, peer-reviewed papers)"
  - Exit code: 1

### Continuous Testing

**Pre-Commit Hook** (validate pilot reports before commit):
```bash
#!/bin/bash
# .git/hooks/pre-commit

FILES=$(git diff --cached --name-only | grep -E 'docs/pilots/.*\.md')

for FILE in $FILES; do
  python scripts/validate-pilot-report.py "$FILE"
  if [ $? -ne 0 ]; then
    echo "❌ Pilot report validation failed: $FILE"
    exit 1
  fi
done

exit 0
```

**CI/CD Workflow** (GitHub Actions):
```yaml
name: Validate Dogfooding Patterns
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate SAP-027 Configuration
        run: python scripts/validate-dogfooding-config.py
      - name: Validate Pilot Reports
        run: |
          for report in docs/pilots/*.md; do
            python scripts/validate-pilot-report.py "$report"
          done
      - name: Check A-MEM Events
        run: |
          cat .chora/memory/events/dogfooding.jsonl | jq . > /dev/null
          # Ensure all events are valid JSON
```

---

## 10. Versioning & Compatibility

SAP-027 follows [Semantic Versioning 2.0.0](https://semver.org/) with extensions for SAP-specific compatibility.

### Version Numbering Scheme

**Format**: `MAJOR.MINOR.PATCH`

**Version Increments**:
- **PATCH** (1.0.x → 1.0.y): Bug fixes, documentation updates, no breaking changes
  - Example: Fix scoring calculation bug, clarify configuration schema
  - Migration: None required
- **MINOR** (1.x.0 → 1.y.0): New features, backward-compatible enhancements
  - Example: Add Level 3 automation scripts, new integration with SAP-019
  - Migration: Optional adoption of new features
- **MAJOR** (x.0.0 → y.0.0): Breaking changes to contracts, configuration, or workflows
  - Example: Change GO criteria formula, restructure pilot phases
  - Migration: Required, migration guide provided

**Current Version**: 1.1.0 (added Level 3 automation patterns)

### Version Compatibility

**Compatibility Guarantees**:
- **Patch versions (1.1.x)**: Backward compatible bug fixes
  - Pilot reports from 1.1.0 work with 1.1.5
  - Configuration schema unchanged
  - Event format unchanged
- **Minor versions (1.x.0)**: Backward compatible new features
  - Pilot reports from 1.1.0 work with 1.2.0
  - New configuration options added (with defaults)
  - New event types may be added (existing parsers continue to work)
- **Major versions (x.0.0)**: Breaking changes allowed with migration guide
  - Pilot reports from 1.x may require updates for 2.0
  - Configuration schema may change (migration script provided)
  - Event format may change (backwards compatibility may break)

### Breaking Changes Policy

**Definition of Breaking Change**:
1. **Configuration Schema Change**: Removing or renaming fields in `.chora/config.yaml`
2. **Event Format Change**: Changing required fields in A-MEM events (dogfooding.jsonl)
3. **Pilot Report Structure Change**: Changing required sections or metrics
4. **GO Criteria Formula Change**: Altering how composite score is calculated
5. **Workflow Phase Change**: Adding, removing, or reordering pilot phases

**Non-Breaking Changes** (allowed in MINOR versions):
- Adding new configuration options (with defaults)
- Adding new event types (existing event types unchanged)
- Adding new optional pilot report sections
- Adding new integration points (existing integrations unchanged)
- Performance improvements, bug fixes

**Breaking Change Process**:
1. **Deprecation Warning** (1 minor version before breaking change):
   ```yaml
   # Version 1.2.0 - Deprecation warning
   dogfooding:
     pilot:
       go_criteria:
         satisfaction_min: 0.85  # DEPRECATED: Will be replaced by satisfaction_threshold in 2.0.0
   ```
2. **Migration Guide** (in release notes for 2.0.0):
   - What changed and why
   - Step-by-step migration instructions
   - Migration script (if applicable)
   - Estimated migration time
3. **Support Window**: Old version supported for 6 months after breaking release

### Dependency Compatibility

| Dependency | Minimum Version | Tested Version | Notes | Status |
|------------|----------------|----------------|-------|--------|
| **SAP-000** (SAP Framework) | 1.0.0 | 1.5.0 | Core SAP protocols | ✅ Compatible |
| **SAP-006** (Vision Synthesis) | 1.0.0 | 1.2.0 | Optional - Wave promotion/demotion | ⚠️ Optional |
| **SAP-010** (Memory System) | 1.0.0 | 1.3.0 | Required - A-MEM event logging | ✅ Required |
| **SAP-015** (Task Tracking) | 1.0.0 | 1.1.0 | Optional - Beads epic creation | ⚠️ Optional |
| **Python** | 3.9+ | 3.11 | Automation scripts | ✅ Compatible |
| **jq** | 1.6+ | 1.7 | JSON query tool | ✅ Compatible |
| **Bash** | 4.0+ | 5.2 | Shell scripts | ✅ Compatible |

**Version Pinning Recommendations**:
- **Production**: Pin to MINOR version (e.g., `~>1.1.0` allows 1.1.x, not 1.2.0)
- **Development**: Pin to MAJOR version (e.g., `^1.0.0` allows 1.x.x, not 2.0.0)
- **Experimentation**: Use latest (`*`)

### Backward Compatibility

**1.0.0 → 1.1.0 Migration** (current):
- **No breaking changes**
- New features: Level 3 automation, pilot dashboard, sync-to-vision.sh
- Migration: Optional, adopt new automation scripts if desired
- Time: 0 hours (no migration required)

**Hypothetical 1.x → 2.0 Migration** (example):
- **Breaking change**: GO criteria formula change
  - Old: Composite score = simple average of 4 criteria
  - New: Weighted score = (satisfaction × 0.4) + (time_savings × 0.3) + (bugs × 0.2) + (adoption × 0.1)
- **Migration steps**:
  1. Update `.chora/config.yaml` with new `go_criteria.weights` section
  2. Re-calculate composite scores for historical pilots (script: `migrate-pilots-to-v2.py`)
  3. Validate updated pilot reports pass new GO threshold
- **Migration script**:
  ```bash
  python scripts/migrate-pilots-to-v2.py --dry-run  # Preview changes
  python scripts/migrate-pilots-to-v2.py --execute  # Apply migration
  ```
- **Estimated time**: 30-60 minutes

### Deprecation Policy

**Deprecation Timeline**:
1. **Announcement** (version N): Feature marked as deprecated in documentation, warning added to code
2. **Transition Period** (versions N+1 to N+2): Feature still works, warnings emitted, migration guide available
3. **Removal** (version N+3, or next MAJOR version): Feature removed, breaking change

**Example Deprecation**:
```
Version 1.2.0 (Announcement):
  - discovery.time_budget (seconds) DEPRECATED
  - Use discovery.time_budget_minutes instead
  - Old config still works, emits warning

Version 1.3.0 (Transition):
  - Both time_budget and time_budget_minutes supported
  - Migration guide published
  - Auto-conversion script available

Version 2.0.0 (Removal):
  - discovery.time_budget removed
  - Only time_budget_minutes supported
  - Old config causes validation error
```

**Deprecation Support**: Deprecated features supported for minimum 2 MINOR versions (6-12 months).

### Migration Paths

**Upgrading from 1.0.0 to 1.1.0**:
```bash
# No migration required, but optionally adopt new features
git pull origin main  # Update to 1.1.0

# Optional: Add Level 3 automation scripts
cp scripts/pilot-dashboard.py /path/to/your/project/scripts/
cp scripts/sync-to-vision.sh /path/to/your/project/scripts/

# Optional: Update .chora/config.yaml with new automation settings
cat >> .chora/config.yaml <<'EOF'
dogfooding:
  automation:
    github_actions:
      enabled: true
EOF
```

**Downgrading from 1.1.0 to 1.0.0** (not recommended):
```bash
# Backup current config
cp .chora/config.yaml .chora/config.yaml.bak

# Checkout older version
git checkout v1.0.0

# Remove 1.1.0-specific config sections
# (Manual edit: remove automation.github_actions section)

# Validation
python scripts/validate-dogfooding-config.py
```

### Changelog

**Version 1.1.0** (2025-11-05):
- Added: Level 3 automation patterns (pilot dashboard, sync-to-vision)
- Added: Week -1 discovery phase (Contract 0)
- Added: Multi-pilot parallelization support
- Enhanced: Error handling (10 error codes defined)
- Enhanced: Performance monitoring (per-phase time tracking)
- Fixed: Scoring weights validation bug

**Version 1.0.0** (2025-11-03):
- Initial release
- 6-week pilot methodology (research, build, validate, decide)
- GO/NO-GO criteria framework
- Integration with SAP-006, SAP-010, SAP-015
- Configuration schema (`.chora/config.yaml`)
- A-MEM event logging (dogfooding.jsonl)

---

## 11. Related Specifications

### Within chora-base

**SAP Artifacts**:
- [Capability Charter](./capability-charter.md) - Problem statement and scope
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - Core SAP protocols and artifact structure
- [SAP-006: Vision Synthesis](../vision-synthesis/protocol-spec.md) - Strategic Wave planning and pilot integration
- [SAP-010: Memory System (A-MEM)](../memory-system/protocol-spec.md) - Event logging, intention inventory, knowledge notes
- [SAP-015: Task Tracking (Beads)](../task-tracking/protocol-spec.md) - Epic creation, backlog management, pilot task tracking
- [SAP-019: Self-Evaluation](../self-evaluation/protocol-spec.md) - SAP maturity assessment and validation
- [SAP-029: SAP Generation](../sap-generation/protocol-spec.md) - Artifact generation for validated pilots

**Integration Patterns**:
- [SAP-001: Inbox](../inbox/protocol-spec.md) - Demand signal extraction from coordination requests
- [SAP-003: Project Bootstrap](../project-bootstrap/protocol-spec.md) - Initial SAP setup for new projects
- [SAP-005: CI/CD Workflows](../ci-cd-workflows/protocol-spec.md) - Pilot reminder automation via GitHub Actions

### External Specifications

**Dogfooding Methodology**:
- [Eating Your Own Dog Food (Wikipedia)](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) - History and industry practices
- [Building on Quicksand (Google Research, 2008)](https://research.google/pubs/pub37633/) - Early validation of infrastructure before broad adoption
- [Amazon's "Working Backwards" Process](https://www.allthingsdistributed.com/2006/11/working_backwards.html) - Customer-first validation methodology

**Evidence-Based Research**:
- [Evidence Levels (Oxford Centre for Evidence-Based Medicine)](https://www.cebm.ox.ac.uk/resources/levels-of-evidence) - Level A/B/C classification system
- [Systematic Review Methodology (Cochrane Handbook)](https://training.cochrane.org/handbook) - Research synthesis best practices

**GO/NO-GO Decision Frameworks**:
- [Stage-Gate Process (Robert G. Cooper)](https://www.stage-gate.com/) - Phase-gate product development methodology
- [Google's HEART Metrics](https://www.dtelepathy.com/ux-metrics/) - User experience measurement framework
- [RICE Scoring (Intercom)](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) - Reach, Impact, Confidence, Effort prioritization

**Semantic Versioning**:
- [Semantic Versioning 2.0.0](https://semver.org/) - Version numbering scheme for APIs and software
- [Keep a Changelog](https://keepachangelog.com/) - Changelog format and best practices

**Pilot Methodology References**:
- [Lean Startup Build-Measure-Learn](http://theleanstartup.com/principles) - Rapid validation cycle methodology
- [Design Sprint (Google Ventures)](https://www.gv.com/sprint/) - 5-day rapid prototyping and validation process
- [Six Sigma DMAIC](https://www.isixsigma.com/methodology/dmaic-methodology/) - Define, Measure, Analyze, Improve, Control process improvement

**Time Savings Measurement**:
- [ROI Calculation Methods (PMI)](https://www.pmi.org/) - Project Management Institute ROI guidelines
- [DORA Metrics](https://dora.dev/) - DevOps Research and Assessment performance metrics
- [Time Motion Study (Taylor, 1911)](https://en.wikipedia.org/wiki/Time_and_motion_study) - Efficiency measurement methodology

**Configuration Management**:
- [YAML Specification 1.2](https://yaml.org/spec/1.2/spec.html) - Configuration file format
- [JSON Lines (JSONL)](https://jsonlines.org/) - Streaming JSON event log format
- [The Twelve-Factor App: Config](https://12factor.net/config) - Environment-based configuration best practices

**Event Sourcing**:
- [Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html) - Event-driven architecture pattern
- [CQRS (Command Query Responsibility Segregation)](https://martinfowler.com/bliki/CQRS.html) - Separation of read/write models

---

**Version History**:
- **1.1.0** (2025-11-05): Complete protocol specification with all sections filled
  - Added: Security considerations, performance requirements, examples, validation, versioning
  - Added: Error handling (10 error codes), configuration schema, integration patterns
  - Enhanced: External specifications with 15+ references
- **1.0.0** (2025-11-03): Initial protocol specification for Dogfooding Patterns