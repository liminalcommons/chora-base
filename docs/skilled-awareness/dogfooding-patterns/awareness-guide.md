# Awareness Guide: Dogfooding Patterns

**SAP ID**: SAP-027
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants
**Last Updated**: 2025-11-03

---

## Quick Start for AI Agents

### One-Sentence Summary

SAP-027 provides a formalized 5-week dogfooding pilot methodology for validating patterns through internal use, achieving GO decisions at 90% confidence (Week 4) and formalization at 100% confidence (Week 5) before ecosystem adoption.

### When to Use This SAP

Use SAP-027 when:
- ✅ User wants to validate a new capability/pattern before broad adoption
- ✅ User has multiple candidate features and needs evidence-based selection (Week -1 discovery scoring)
- ✅ User needs structured pilot methodology with GO/NO-GO decision framework
- ✅ User wants to collect time savings, satisfaction, and bug metrics during validation
- ✅ Project has SAP-010 (A-MEM) for event logging and SAP-015 (beads) for task tracking
- ✅ User wants to promote/demote features in vision document based on pilot outcomes

Don't use SAP-027 for:
- ❌ Trivial features with no validation risk (e.g., documentation typo fixes, color scheme changes)
- ❌ Externally-driven features that must ship regardless of pilot outcome (client contracts, regulatory requirements)
- ❌ Features with <2 weeks build time (pilot overhead not justified)
- ❌ Projects without event logging infrastructure (SAP-010) - pilot metrics cannot be tracked
- ❌ One-time experiments with no intention to adopt (use ad-hoc testing instead)

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1: Weighted Scoring (Week -1 Discovery)**
- **Description**: Use 4-factor weighted scoring to select pilot candidates from intention inventory: Evidence (40%), Alignment (30%), Demand (20%), Feasibility (10%). Threshold: 7.0 out of 10.
- **When to use**: User has 5+ candidate features and needs data-driven selection (not gut feel)
- **Example**: "Priority classification" scores 8.2 (strong evidence: 9, wave 1 alignment: 8, user demand: 7, feasibility: 9). "Advanced code generation" scores 6.5 (weak evidence: 5, wave 2 alignment: 7, demand: 8, feasibility: 6) → Reject, below threshold.

**Concept 2: GO/NO-GO Composite Scoring (Week 4 Decision)**
- **Description**: Calculate composite score from 4 metrics with different weights: Time savings (40%), Satisfaction (30%), Bugs (20% penalty), Adoption (10%). GO threshold: ≥60%. Individual hard gates: time_savings ≥5x, satisfaction ≥85%, bugs = 0.
- **When to use**: Week 4 pilot evaluation - determines if feature gets promoted to Wave 1 (GO) or demoted to Wave 3 (NO-GO)
- **Example**: SAP-015 pilot: time_savings=6x (24pts), satisfaction=85% (25.5pts), bugs=0 (0 penalty), adoption=3 projects (10pts) = 59.5pts → NO-GO (just below 60% threshold). However, hard gates failed (satisfaction < 85%), so NO-GO is correct.

**Concept 3: Evidence Pyramid (Week 0 Research)**
- **Description**: Research evidence has 3 levels with required percentages: Level A (standards, peer-reviewed, ≥30%), Level B (case studies, benchmarks, ≥40%), Level C (expert opinion, blogs, ≤30%). Total must be ≥10 sources.
- **When to use**: Week 0 research phase - prevents premature pilots based on weak evidence
- **Example**: User proposes "GraphQL adoption" with 1 blog post (Level C) → BLOCK pilot. Require 3+ Level A sources (RFC specs, W3C docs), 4+ Level B sources (Netflix/Airbnb case studies), then proceed.

**Concept 4: Integration Triggers (SAP-006 + SAP-015)**
- **Description**: GO decisions trigger 2 automatic actions: (1) Vision promotion (Wave 2→Wave 1 in SAP-006), (2) Epic creation (P1 in SAP-015 beads). NO-GO triggers: (1) Vision demotion (Wave 2→Wave 3), (2) Task closure + lessons learned note.
- **When to use**: After Week 4 GO/NO-GO decision - automate vision and backlog updates
- **Example**: SAP-015 GO decision → Auto-promote in vision doc, auto-create epic "SAP-015: Backlog Organization Patterns" with 7 child tasks, log to A-MEM dogfooding.jsonl.

### Decision Tree

```
User request about Dogfooding Patterns
   │
   ├─ "Help me choose which feature to pilot"?
   │   └─> Workflow 1: Week -1 Discovery
   │       - Query intention inventory (SAP-010)
   │       - Score candidates (weighted criteria)
   │       - Select top candidate (≥7.0 threshold)
   │       - Create pilot plan
   │
   ├─ "The pilot succeeded, what next"?
   │   └─> Workflow 2: GO Decision
   │       - Verify GO criteria (time_savings ≥5x, satisfaction ≥85%, bugs=0)
   │       - Promote in vision (Wave 2 → Wave 1)
   │       - Create P1 epic in beads
   │       - Log to A-MEM (vision-updates.jsonl, backlog-updates.jsonl)
   │
   ├─ "The pilot failed, what should I do"?
   │   └─> Workflow 3: NO-GO Decision
   │       - Document lessons learned (root causes, recommendations)
   │       - Demote in vision (Wave 2 → Wave 3)
   │       - Close discovery task
   │       - Create P3 future task (if revisit planned)
   │       - Log to A-MEM
   │
   ├─ "How do I validate the pilot is set up correctly"?
   │   └─> Run validation:
   │       python scripts/sap-evaluator.py --quick SAP-027
   │       - Check adoption level (1, 2, or 3)
   │       - Verify configuration (dogfooding-patterns section)
   │       - Confirm integration (SAP-006, SAP-010, SAP-015)
   │
   └─ "What's the fastest way to run a pilot"?
       └─> Recommend Level 1 (simplified):
           - Skip Week -1 discovery (user already knows what to pilot)
           - Skip Week 0 research (for low-risk features)
           - Focus on Weeks 1-3 build + Week 4 validation
           - 3-4 hour setup (vs 6-8 hours for full pilot)
```

---

## 2. Common Agent Workflows

This section provides step-by-step examples for the three most common dogfooding workflows: pre-pilot discovery, pilot GO decision (promotion), and pilot NO-GO decision (demotion with lessons learned).

### Workflow 1: Week -1 Pre-Pilot Discovery

**User Request**: "Help me select the best pilot candidate from our intention inventory"

**Agent Actions**:

1. **Query intention inventory from SAP-010**:
   ```bash
   # Find latest intention inventory
   ls -lt .chora/memory/knowledge/notes/intention-inventory-*.md | head -1

   # Read inventory (89 intentions in this example)
   cat .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md
   ```

2. **Score candidates using weighted criteria**:
   ```python
   # For each intention, calculate weighted score:
   # Evidence (40%): Level A/B availability → 1-10 points
   # Alignment (30%): Wave 1/2/3 positioning → 1-10 points
   # Demand (20%): User request count → 1-10 points
   # Feasibility (10%): Effort estimate → 1-10 points

   # Example scoring for "Backlog Organization Patterns" (SAP-015):
   scores = {
       "evidence": 9,      # Strong Level A evidence (JIRA, Linear case studies)
       "alignment": 8,     # Wave 2 exploratory feature
       "demand": 7,        # 7 explicit requests from 3 projects
       "feasibility": 9    # 2-week build, low risk
   }
   weighted_score = (9*0.4) + (8*0.3) + (7*0.2) + (9*0.1) = 8.2
   ```

3. **Select top 3-5 candidates above threshold (7.0)**:
   ```markdown
   Top 5 Candidates (scores ≥7.0):
   1. SAP-015: Backlog Organization Patterns (8.2)
   2. SAP-030: Data Fetching Patterns (7.8)
   3. SAP-026: UI Component Library (7.5)
   4. SAP-032: Performance Optimization (7.2)
   5. SAP-018: Form Validation (7.1)

   Below threshold: 84 candidates (scores <7.0)
   ```

4. **Create pilot-candidates note**:
   ```bash
   cat > .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md <<'EOF'
   ## Pilot Candidates: 2025-11-05

   ### Selection Summary
   - **Candidates evaluated**: 89
   - **Above threshold (≥7.0)**: 5
   - **Selected for pilot**: SAP-015 Backlog Organization Patterns

   ### Top 5 Candidates

   #### 1. SAP-015: Backlog Organization Patterns (Score: 8.2)
   - **Evidence (9/10)**: Strong Level A evidence from JIRA, Linear case studies
   - **Alignment (8/10)**: Wave 2 exploratory feature, aligns with Q1 2025 priorities
   - **Demand (7/10)**: 7 explicit requests from 3 active projects (chora-base, chora-compose, chora-studio)
   - **Feasibility (9/10)**: 2-week build, existing beads CLI foundation, low technical risk
   - **Rationale**: Immediate pain point (task triage takes 30min), strong evidence, fast ROI

   #### 2. SAP-030: Data Fetching Patterns (Score: 7.8)
   [Similar structure for other candidates...]

   ### Selection Decision
   **Pilot ID**: pilot-2025-11-05-sap-015
   **Candidate**: SAP-015 Backlog Organization Patterns
   **Rationale**: Highest score (8.2), immediate pain point across 3 projects, strong evidence base
   **Expected outcome**: Reduce task triage time from 30min → 5min (6x improvement)
   **Next steps**: Proceed to Week 0 research phase
   EOF
   ```

5. **Log selection to A-MEM**:
   ```bash
   echo '{"timestamp":"2025-11-05T10:30:00Z","event_type":"pilot_candidate_selected","pilot_id":"pilot-2025-11-05-sap-015","candidate":{"intention_id":"INT-089","name":"Backlog Organization Patterns","weighted_score":8.2,"scores":{"evidence":9,"alignment":8,"demand":7,"feasibility":9}},"rationale":"Highest score with immediate pain point and strong evidence"}' >> .chora/memory/events/dogfooding.jsonl
   ```

6. **Proceed to Week 0 research**:
   ```bash
   just research "backlog organization and task prioritization patterns"
   ```

**Validation**:
```bash
# Verify pilot-candidates note created
test -f .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md && echo "✓ Candidates note created"

# Verify A-MEM event logged
grep "pilot_candidate_selected" .chora/memory/events/dogfooding.jsonl | tail -1 | jq .

# Verify at least 3 candidates above threshold
grep "Above threshold" .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md
```

**Expected Output**:
```
✓ Candidates note created
{
  "timestamp": "2025-11-05T10:30:00Z",
  "event_type": "pilot_candidate_selected",
  "pilot_id": "pilot-2025-11-05-sap-015",
  "candidate": {
    "weighted_score": 8.2
  }
}
- **Above threshold (≥7.0)**: 5
```

**Time Budget**: ≤2 hours (target: 1.5 hours)

**Common Variations**:
- **Variation 1: Low candidates above threshold (<3)**: Lower threshold to 6.5 or enrich intentions with more evidence
- **Variation 2: Multiple high-scoring candidates (≥5 above 8.0)**: Consider running parallel pilots or selecting based on strategic theme diversity
- **Variation 3: Missing intention inventory**: Create one first using SAP-010 intention inventory workflow

---

### Workflow 2: Pilot GO → Vision Promotion + Beads Epic Creation

**User Request**: "The SAP-015 pilot succeeded! Help me promote it to Wave 1 and create the implementation epic"

**Context**: 4-week pilot completed, evaluation shows 85% satisfaction, 6x time savings, 0 bugs

**Agent Actions**:

1. **Review pilot evaluation metrics**:
   ```bash
   # Read pilot evaluation report
   cat docs/pilots/pilot-2025-11-05-sap-015/go-no-go-decision.md
   ```
   ```markdown
   ## GO/NO-GO Decision: SAP-015 Backlog Organization Patterns

   **Decision**: ✅ GO

   ### Evaluation Metrics
   - **Time savings**: 6x (30min → 5min for task triage) ✅ Target: ≥5x
   - **Satisfaction**: 85% (17/20 users very satisfied) ✅ Target: ≥85%
   - **Bugs**: 0 critical/major bugs ✅ Target: 0
   - **Adoption**: 3 projects (chora-base, chora-compose, chora-studio) ✅ Target: ≥2

   **Composite Score**: 72% (GO threshold: ≥60%)

   **Recommendation**: Proceed with formalization (Week 5)
   ```

2. **Update vision document (Wave 2 → Wave 1 promotion)**:
   ```bash
   # Find vision document
   ls -lt .chora/memory/knowledge/notes/vision-chora-base-*.md | head -1

   # Edit vision document
   # BEFORE (Wave 2):
   # ## Wave 2: Exploratory Features (3-6 Months)
   # ### Backlog Organization Patterns
   # **Status**: Validating via pilot
   # **Hypothesis**: Priority classification reduces triage time

   # AFTER (Wave 1):
   ## Wave 1: Committed Features (Next 3 Months)

   ### Backlog Organization Patterns (SAP-015) ✅ Pilot Validated
   **Decision**: Adopt
   **Evidence**: 4-week pilot (pilot-2025-11-05-sap-015)
     - Satisfaction: 85% (17/20 users)
     - Time savings: 6x (30min → 5min)
     - Bugs: 0
     - Adoption: 3 projects
   **Success criteria**: Reduce task triage time from 30min → 5min across all projects
   **Timeline**: Implement in Q1 2025 (Weeks 1-6)
   **Priority**: P1 (High impact, validated ROI)
   ```

3. **Log vision update to A-MEM**:
   ```bash
   echo '{"timestamp":"2025-11-05T16:00:00Z","event_type":"vision_updated","change":"wave_promotion","feature":"Backlog Organization Patterns","from_wave":2,"to_wave":1,"pilot_id":"pilot-2025-11-05-sap-015","evidence":{"satisfaction":85,"time_savings":"6x","bugs":0,"adoption":3},"rationale":"Pilot exceeded all GO criteria (72% composite score)"}' >> .chora/memory/events/vision-updates.jsonl
   ```

4. **Create beads P1 epic with pilot metadata**:
   ```bash
   bd create \
     --title "SAP-015: Backlog Organization Patterns" \
     --description "$(cat <<EOF
   Implement backlog organization patterns validated in 4-week pilot.

   **Pilot Evidence** (pilot-2025-11-05-sap-015):
   - Satisfaction: 85% (17/20 users very satisfied)
   - Time savings: 6x (30min → 5min for task triage)
   - Bugs: 0 critical/major issues
   - Adoption: 3 projects validated

   **Scope**:
   - Priority classification (P0-P3) with semantic rules
   - Status tracking workflow (open, in_progress, blocked, done)
   - Beads CLI enhancements for filtering and reporting
   - Documentation updates (adoption blueprint, examples)

   **Success Metrics**:
   - Task triage time: <5min per session (baseline: 30min)
   - User satisfaction: ≥85% (maintain pilot level)
   - Zero bugs in P0/P1 classification logic

   **Timeline**: 6 weeks (Q1 2025)
   EOF
   )" \
     --priority P1 \
     --labels "epic,pilot-validated,sap-015,q1-2025" \
     --metadata pilot_id=pilot-2025-11-05-sap-015 \
     --metadata pilot_score=8.2 \
     --metadata satisfaction=85 \
     --metadata time_savings=6x \
     --metadata bugs=0

   # Output: Created issue chora-base-a1b2c3d (P1 epic)
   ```

5. **Break down epic into implementation tasks**:
   ```bash
   # Get epic ID from previous command
   EPIC_ID="chora-base-a1b2c3d"

   bd create --title "Implement P0-P3 priority classification" --parent $EPIC_ID --priority P1 --labels "backend,priority"
   bd create --title "Add status tracking workflow (open/in_progress/blocked/done)" --parent $EPIC_ID --priority P1 --labels "backend,status"
   bd create --title "Enhance beads CLI with filter/sort by priority+status" --parent $EPIC_ID --priority P1 --labels "cli"
   bd create --title "Add priority/status to beads web UI" --parent $EPIC_ID --priority P1 --labels "frontend"
   bd create --title "Write priority classification guide" --parent $EPIC_ID --priority P2 --labels "docs"
   bd create --title "Update adoption blueprint with backlog patterns" --parent $EPIC_ID --priority P2 --labels "docs"
   bd create --title "Add 3 backlog organization examples" --parent $EPIC_ID --priority P2 --labels "docs,examples"

   # 7 tasks created
   ```

6. **Log epic creation to A-MEM**:
   ```bash
   echo '{"timestamp":"2025-11-05T16:05:00Z","event_type":"backlog_updated","change":"epic_created","epic_id":"chora-base-a1b2c3d","pilot_id":"pilot-2025-11-05-sap-015","priority":"P1","child_tasks":7,"estimated_effort":"6 weeks"}' >> .chora/memory/events/backlog-updates.jsonl
   ```

**Validation**:
```bash
# Verify vision updated (Wave 1 has SAP-015)
grep -A 5 "SAP-015" .chora/memory/knowledge/notes/vision-chora-base-2025.md | grep "Wave 1"

# Verify vision update logged to A-MEM
grep "vision_updated.*pilot-2025-11-05-sap-015" .chora/memory/events/vision-updates.jsonl | jq .

# Verify epic created in beads
bd show chora-base-a1b2c3d --json | jq '{id, title, priority, labels, metadata}'

# Verify 7 child tasks created
bd list --parent chora-base-a1b2c3d --json | jq 'length'

# Verify backlog update logged to A-MEM
grep "epic_created.*pilot-2025-11-05-sap-015" .chora/memory/events/backlog-updates.jsonl | jq .
```

**Expected Output**:
```
### Backlog Organization Patterns (SAP-015) ✅ Pilot Validated
**Decision**: Adopt
{
  "event_type": "vision_updated",
  "change": "wave_promotion",
  "from_wave": 2,
  "to_wave": 1
}
{
  "id": "chora-base-a1b2c3d",
  "title": "SAP-015: Backlog Organization Patterns",
  "priority": "P1",
  "labels": ["epic", "pilot-validated", "sap-015"]
}
7
{
  "event_type": "backlog_updated",
  "change": "epic_created",
  "child_tasks": 7
}
```

**Time Budget**: ≤5 minutes for epic creation (target: 3 minutes)

**Common Variations**:
- **Variation 1: Automated promotion**: If `vision_integration.update_strategy: automated`, vision update happens automatically
- **Variation 2: Epic auto-breakdown**: If `backlog_integration.go_action.auto_breakdown: true`, child tasks created automatically from template
- **Variation 3: Manual vision update**: If SAP-006 not adopted, skip vision update, only create epic

---

### Workflow 3: Pilot NO-GO → Lessons Learned + Vision Demotion

**User Request**: "The SAP-033 pilot didn't meet our criteria. Help me document lessons learned and demote it in the vision"

**Context**: 4-week pilot completed, evaluation shows only 2x time savings (target: 5x), 3 bugs, 62% satisfaction (target: 85%)

**Agent Actions**:

1. **Review pilot evaluation metrics**:
   ```bash
   cat docs/pilots/pilot-2025-10-15-sap-033/go-no-go-decision.md
   ```
   ```markdown
   ## GO/NO-GO Decision: SAP-033 Advanced Code Generation

   **Decision**: ❌ NO-GO

   ### Evaluation Metrics
   - **Time savings**: 2x (15min → 7.5min for boilerplate code) ❌ Target: ≥5x
   - **Satisfaction**: 62% (12/20 users satisfied) ❌ Target: ≥85%
   - **Bugs**: 3 critical bugs (incorrect prop types, missing imports, broken tests) ❌ Target: 0
   - **Adoption**: 2 projects (chora-base, chora-compose) ✅ Target: ≥2

   **Composite Score**: 35% (NO-GO threshold: <60%)

   **Recommendation**: Defer to Wave 3 (Future), revisit after improving prompt templates and validation
   ```

2. **Create lessons learned note**:
   ```bash
   cat > .chora/memory/knowledge/notes/lessons-learned-pilot-2025-10-15-sap-033.md <<'EOF'
   ## Lessons Learned: Advanced Code Generation Pilot

   **Pilot ID**: pilot-2025-10-15-sap-033
   **SAP**: SAP-033 Advanced Code Generation
   **Duration**: 4 weeks (Oct 15 - Nov 12, 2025)
   **Decision**: ❌ NO-GO (35% composite score)

   ### What Worked
   - **Simple code generation**: Basic CRUD operations, form components generated correctly (80% success rate)
   - **Template architecture**: Jinja2 template system was flexible and maintainable
   - **Developer interest**: 20 developers tried the feature, indicating demand exists

   ### What Didn't Work
   - **Complex code generation**: Generated code for complex state management had 3 critical bugs
     - Bug 1: Incorrect TypeScript prop types (generic constraints missing)
     - Bug 2: Missing ES6 imports (module resolution failed)
     - Bug 3: Broken unit tests (mocks not generated)
   - **Prompt engineering gaps**: LLM prompts lacked sufficient context for complex patterns
   - **Validation insufficient**: No pre-commit validation to catch errors before developer review

   ### Root Causes
   1. **Insufficient prompt examples**: Only 5 examples provided, needed 15-20 for complex patterns
   2. **No validation step**: Generated code went straight to developer without linting/type-checking
   3. **Complexity underestimated**: Assumed LLM could generalize from simple examples to complex cases

   ### Recommendations for Future Work
   1. **Improve prompt templates**:
      - Add 10-15 more examples covering edge cases (generics, async/await, error boundaries)
      - Include negative examples (what NOT to generate)
   2. **Add validation pipeline**:
      - Run TypeScript type-checking on generated code
      - Run ESLint + Prettier before showing to developer
      - Run unit tests (if test templates exist)
   3. **Reduce scope**:
      - Focus on simple boilerplate only (CRUD, forms, list views)
      - Defer complex patterns (state machines, advanced hooks) to manual coding
   4. **Iterate in smaller chunks**:
      - Run 2-week pilots for specific code types (e.g., "form generation only")
      - Validate each chunk before expanding scope

   ### Decision
   **Action**: Demote from Wave 2 (exploratory) to Wave 3 (future considerations)
   **Revisit when**: After completing 3 recommendations above (estimated: Q3 2025)
   **Alternative approaches**: Consider simpler code scaffolding (vs full generation), or adopt existing tools (Copilot, GitHub Codespaces templates)

   ### Metrics for Re-evaluation
   - Time savings: ≥5x (15min → 3min)
   - Satisfaction: ≥85%
   - Bugs: 0 critical bugs in generated code
   - Validation pass rate: ≥95% (generated code passes type-checking + linting)
   EOF
   ```

3. **Update vision document (Wave 2 → Wave 3 demotion)**:
   ```bash
   # Edit vision document
   # BEFORE (Wave 2):
   # ## Wave 2: Exploratory Features (3-6 Months)
   # ### Advanced Code Generation (SAP-033)
   # **Status**: Validating via pilot

   # AFTER (Wave 3):
   ## Wave 3: Future Considerations (6+ Months)

   ### Advanced Code Generation (SAP-033) ❌ Pilot Failed
   **Decision**: Defer
   **Rationale**: 4-week pilot (pilot-2025-10-15-sap-033) showed insufficient ROI
     - Time savings: Only 2x (target: 5x)
     - Satisfaction: 62% (target: 85%)
     - Bugs: 3 critical bugs in generated code
   **Lessons learned**: Prompt templates need 15-20 examples, validation pipeline required, scope too broad
   **Revisit when**: Q3 2025 after improving prompt engineering and adding validation
   **Alternative**: Consider simpler scaffolding or existing tools (GitHub Copilot)
   ```

4. **Log vision update to A-MEM**:
   ```bash
   echo '{"timestamp":"2025-11-12T14:00:00Z","event_type":"vision_updated","change":"wave_demotion","feature":"Advanced Code Generation","from_wave":2,"to_wave":3,"pilot_id":"pilot-2025-10-15-sap-033","evidence":{"satisfaction":62,"time_savings":"2x","bugs":3,"adoption":2},"rationale":"Pilot failed GO criteria (35% composite score), needs prompt + validation improvements"}' >> .chora/memory/events/vision-updates.jsonl
   ```

5. **Close discovery task (if exists in beads)**:
   ```bash
   # Find discovery task
   bd list --labels "sap-033,discovery" --status open --json | jq -r '.[0].id'
   # Output: chora-base-xyz123

   bd close chora-base-xyz123 \
     --reason "Pilot failed validation (satisfaction: 62%, time savings: 2x, bugs: 3)" \
     --comment "See lessons learned: lessons-learned-pilot-2025-10-15-sap-033.md" \
     --labels "pilot-failed,no-go"
   ```

6. **Optionally create P3 future task for revisit**:
   ```bash
   bd create \
     --title "Revisit: Advanced Code Generation (SAP-033)" \
     --description "Pilot showed only 2x time savings (target: 5x). Revisit after:
   1. Adding 10-15 more prompt examples
   2. Building validation pipeline (TypeScript + ESLint)
   3. Reducing scope to simple boilerplate only

   See lessons learned: lessons-learned-pilot-2025-10-15-sap-033.md" \
     --priority P3 \
     --labels "deferred,pilot-no-go,sap-033,q3-2025"

   # Output: Created issue chora-base-def456 (P3)
   ```

7. **Log backlog updates to A-MEM**:
   ```bash
   echo '{"timestamp":"2025-11-12T14:05:00Z","event_type":"backlog_updated","change":"task_closed","task_id":"chora-base-xyz123","pilot_id":"pilot-2025-10-15-sap-033","reason":"no_go_decision","lessons_learned":"lessons-learned-pilot-2025-10-15-sap-033.md"}' >> .chora/memory/events/backlog-updates.jsonl

   echo '{"timestamp":"2025-11-12T14:06:00Z","event_type":"backlog_updated","change":"future_task_created","task_id":"chora-base-def456","pilot_id":"pilot-2025-10-15-sap-033","revisit_date":"Q3 2025"}' >> .chora/memory/events/backlog-updates.jsonl
   ```

**Validation**:
```bash
# Verify lessons learned note created
test -f .chora/memory/knowledge/notes/lessons-learned-pilot-2025-10-15-sap-033.md && echo "✓ Lessons learned documented"

# Verify vision updated (Wave 3 has SAP-033)
grep -A 5 "SAP-033" .chora/memory/knowledge/notes/vision-chora-base-2025.md | grep "Wave 3"

# Verify vision demotion logged to A-MEM
grep "vision_updated.*pilot-2025-10-15-sap-033" .chora/memory/events/vision-updates.jsonl | jq .

# Verify discovery task closed
bd show chora-base-xyz123 --json | jq '.status'  # Should be "done"

# Verify P3 future task created
bd show chora-base-def456 --json | jq '{id, title, priority, labels}'

# Verify backlog updates logged
grep "backlog_updated.*pilot-2025-10-15-sap-033" .chora/memory/events/backlog-updates.jsonl | jq .
```

**Expected Output**:
```
✓ Lessons learned documented
### Advanced Code Generation (SAP-033) ❌ Pilot Failed
**Decision**: Defer
{
  "event_type": "vision_updated",
  "change": "wave_demotion",
  "from_wave": 2,
  "to_wave": 3
}
"done"
{
  "id": "chora-base-def456",
  "title": "Revisit: Advanced Code Generation (SAP-033)",
  "priority": "P3",
  "labels": ["deferred", "pilot-no-go", "sap-033"]
}
[2 backlog_updated events]
```

**Time Budget**: ≤5 minutes for lessons logging (target: 4 minutes)

**Common Variations**:
- **Variation 1: No future task**: If pilot failure is fundamental (not fixable), skip P3 task creation, only close discovery task
- **Variation 2: Partial success**: If some components succeeded (e.g., simple code generation worked), create narrower-scope pilot for successful subset
- **Variation 3: Manual vision update**: If SAP-006 not adopted, skip vision document changes, focus on lessons learned documentation

---

## 3. Quick Reference for Agents

### Key Commands

```bash
# Validate SAP-027 adoption (30 seconds)
python scripts/sap-evaluator.py --quick SAP-027

# Find pilot candidates from intention inventory
cat .chora/memory/knowledge/notes/intention-inventory-$(date +%Y-%m-%d).md

# Query A-MEM dogfooding events
grep "pilot_" .chora/memory/events/dogfooding.jsonl | jq .

# Create pilot plan (Level 1 simplified)
mkdir -p docs/pilots/ && cat > docs/pilots/pilot-$(date +%Y-%m-%d)-{name}.md

# Run evidence-based research (Level 2)
just research "{search query}" --evidence-levels A,B,C --min-sources 10

# Check GO/NO-GO criteria
cat docs/pilots/pilot-{date}-{name}/go-no-go-decision.md

# Promote feature to Wave 1 (GO decision)
vim .chora/memory/knowledge/notes/vision-{project}-2025.md  # Move from Wave 2 → Wave 1

# Create P1 epic from pilot (GO decision)
bd create --title "SAP-XXX: {Feature Name}" --priority P1 --labels "epic,pilot-validated"

# Document lessons learned (NO-GO decision)
cat > .chora/memory/knowledge/notes/lessons-learned-pilot-{date}-{name}.md

# View multi-pilot dashboard (Level 3)
python scripts/pilot-dashboard.py

# Sync pilot outcomes to vision document (Level 3 automation)
bash scripts/sync-to-vision.sh
```

### Important File Paths

| File | Purpose | Agent Action |
|------|---------|--------------|
| `.chora/memory/events/dogfooding.jsonl` | A-MEM pilot event log | Log `pilot_started`, `pilot_completed`, `pilot_go_decision`, `pilot_no_go_decision` events |
| `.chora/memory/knowledge/notes/intention-inventory-*.md` | Candidate features for pilots | Query during Week -1 discovery to find pilot candidates |
| `.chora/memory/knowledge/notes/pilot-candidates-*.md` | Week -1 scoring results | Create after scoring candidates, includes weighted scores + rationale |
| `.chora/memory/knowledge/notes/vision-{project}-2025.md` | Vision document (SAP-006) | Update to promote/demote features based on GO/NO-GO decisions |
| `.chora/memory/knowledge/notes/lessons-learned-pilot-*.md` | NO-GO pilot retrospectives | Create after NO-GO decision, document root causes + recommendations |
| `docs/pilots/pilot-{date}-{name}/` | Individual pilot directory | Create for each pilot, contains build plan, metrics, GO/NO-GO decision |
| `docs/pilots/pilot-{date}-{name}/go-no-go-decision.md` | Week 4 evaluation report | Document time savings, satisfaction, bugs, adoption, composite score |
| `.chora/config.yaml` | Chora configuration | Add `dogfooding-patterns` section for SAP-027 integration settings |
| `.beads/issues.jsonl` | Beads task tracking (SAP-015) | Create P1 epics for GO decisions, close tasks for NO-GO decisions |

### Configuration Snippets

**Configuration: SAP-027 Integration Settings** (add to `.chora/config.yaml`)
```yaml
dogfooding-patterns:
  enabled: true

  # Week -1 Discovery scoring weights
  discovery:
    scoring_weights:
      evidence: 0.40      # Level A/B availability
      alignment: 0.30     # Wave 1/2/3 positioning
      demand: 0.20        # User request count
      feasibility: 0.10   # Effort estimate
    threshold: 7.0        # Minimum weighted score to proceed

  # Week 0 Research evidence requirements
  research:
    evidence_requirements:
      level_a_min: 0.30   # ≥30% standards, peer-reviewed
      level_b_min: 0.40   # ≥40% case studies, benchmarks
      level_c_max: 0.30   # ≤30% expert opinion, blogs
      total_sources_min: 10

  # Week 4 GO/NO-GO criteria
  evaluation:
    composite_weights:
      time_savings: 0.40
      satisfaction: 0.30
      bugs: 0.20          # Penalty weight
      adoption: 0.10
    go_threshold: 0.60    # 60% composite score
    hard_gates:
      time_savings_min: 5 # ≥5x improvement
      satisfaction_min: 85 # ≥85% satisfied
      bugs_max: 0         # 0 critical/major bugs
      adoption_min: 2     # ≥2 adoption cases

  # Integration with SAP-006 (Vision Synthesis)
  vision_integration:
    enabled: true
    auto_promote: true    # GO → Wave 2 to Wave 1
    auto_demote: true     # NO-GO → Wave 2 to Wave 3
    update_strategy: "automated"  # or "manual"

  # Integration with SAP-015 (Task Tracking)
  backlog_integration:
    enabled: true
    go_action: "create_epic"  # Create P1 epic on GO
    nogo_action: "close_task" # Close discovery task on NO-GO
    auto_breakdown: false     # Manually create child tasks

  # Integration with SAP-010 (Memory System)
  memory_integration:
    enabled: true
    event_stream: "dogfooding.jsonl"
    knowledge_notes:
      - intention_inventory
      - pilot_candidates
      - lessons_learned
```

### Common Patterns

**Pattern 1: Scoring Pilot Candidates (Week -1)**
```python
#!/usr/bin/env python3
"""Score pilot candidates using weighted criteria"""

def score_candidate(candidate, intentions_db):
    """Calculate weighted score (0-10) for a pilot candidate"""
    # Extract scores from intention record
    evidence_score = intentions_db[candidate]["evidence_level"]  # 1-10
    alignment_score = intentions_db[candidate]["wave_alignment"]  # 1-10 (Wave 1=10, Wave 2=7, Wave 3=4)
    demand_score = min(10, intentions_db[candidate]["request_count"])  # Normalize to 1-10
    feasibility_score = 11 - intentions_db[candidate]["effort_weeks"]  # Inverse: 1 week=10, 10 weeks=1

    # Apply weights: Evidence (40%), Alignment (30%), Demand (20%), Feasibility (10%)
    weighted_score = (
        evidence_score * 0.40 +
        alignment_score * 0.30 +
        demand_score * 0.20 +
        feasibility_score * 0.10
    )

    return round(weighted_score, 1)

# Example usage
intentions = {
    "SAP-015": {
        "evidence_level": 9,      # Strong Level A evidence
        "wave_alignment": 8,      # Wave 2 feature
        "request_count": 7,       # 7 user requests
        "effort_weeks": 2         # 2-week build
    }
}

score = score_candidate("SAP-015", intentions)
print(f"SAP-015 weighted score: {score}")  # Output: 8.2
if score >= 7.0:
    print("✅ Above threshold, proceed to pilot")
else:
    print("❌ Below threshold, defer or enrich")
```

**Pattern 2: GO/NO-GO Composite Scoring (Week 4)**
```python
#!/usr/bin/env python3
"""Calculate composite score for GO/NO-GO decision"""

def calculate_composite_score(metrics):
    """
    Calculate composite score (0-100) from pilot evaluation metrics.

    Args:
        metrics (dict): {
            "time_savings": float (e.g., 6.0 for 6x),
            "satisfaction": float (0-100, e.g., 85.0 for 85%),
            "bugs": int (critical/major bugs count),
            "adoption": int (number of adoption cases)
        }

    Returns:
        float: Composite score (0-100)
    """
    # Normalize time savings: Cap at 10x (100 points)
    time_savings_points = min(100, (metrics["time_savings"] / 10.0) * 100) * 0.40

    # Satisfaction is already 0-100
    satisfaction_points = metrics["satisfaction"] * 0.30

    # Bugs are penalty: 0 bugs = 0 penalty, 1+ bugs = 100% penalty (lose all points)
    bug_penalty = 100 * 0.20 if metrics["bugs"] > 0 else 0

    # Normalize adoption: Cap at 5 cases (100 points)
    adoption_points = min(100, (metrics["adoption"] / 5.0) * 100) * 0.10

    composite_score = time_savings_points + satisfaction_points - bug_penalty + adoption_points

    return round(composite_score, 1)

# Example: SAP-015 pilot
metrics = {
    "time_savings": 6.0,    # 6x improvement
    "satisfaction": 85.0,   # 85% satisfied
    "bugs": 0,              # 0 bugs
    "adoption": 3           # 3 projects
}

score = calculate_composite_score(metrics)
print(f"Composite score: {score}%")  # Output: 72.0%
print(f"Decision: {'✅ GO' if score >= 60 else '❌ NO-GO'}")

# Check hard gates
if metrics["time_savings"] < 5:
    print("❌ Hard gate failed: time_savings < 5x")
if metrics["satisfaction"] < 85:
    print("❌ Hard gate failed: satisfaction < 85%")
if metrics["bugs"] > 0:
    print("❌ Hard gate failed: bugs > 0")
if metrics["adoption"] < 2:
    print("❌ Hard gate failed: adoption < 2")
```

---

## 4. Integration with Other SAPs

### Required Dependencies

#### SAP-000 (SAP Framework)

**Relationship**: SAP-027 follows SAP-000 artifact structure (capability charter, protocol spec, awareness guide, adoption blueprint, ledger)

**Agent Workflow**:
1. When using SAP-027, verify SAP-000 is installed: `test -f docs/skilled-awareness/sap-framework/protocol-spec.md`
2. If not found, recommend installing SAP-000 first (foundation for all SAPs)
3. Use SAP-000 evaluation criteria for pilot candidates (5 artifacts completeness, version consistency)

#### SAP-010 (Memory System / A-MEM)

**Relationship**: SAP-027 requires A-MEM event logging for pilot metrics tracking (dogfooding.jsonl, vision-updates.jsonl, backlog-updates.jsonl)

**Agent Workflow**:
1. Before starting pilot, verify SAP-010 is installed: `test -d .chora/memory/events/`
2. If not found, recommend installing SAP-010 first (required for pilot event tracking)
3. Log all pilot events to `.chora/memory/events/dogfooding.jsonl` (pilot_started, pilot_completed, pilot_go_decision, pilot_no_go_decision)
4. Use intention inventory for Week -1 discovery: `cat .chora/memory/knowledge/notes/intention-inventory-*.md`
5. Create knowledge notes for lessons learned: `.chora/memory/knowledge/notes/lessons-learned-pilot-*.md`

### Complementary SAPs

**SAP-006 (Vision Synthesis)** - Strategic Planning Integration
- **Use together when**: User maintains vision document with Wave 1/2/3 roadmap structure
- **Benefit**: GO decisions auto-promote features to Wave 1 (committed), NO-GO decisions auto-demote to Wave 3 (deferred)
- **Integration point**: After Week 4 decision, agent updates vision document and logs to `vision-updates.jsonl`
- **Optional**: Can run pilots without SAP-006, but vision promotion/demotion must be done manually

**SAP-015 (Task Tracking / Beads)** - Backlog Management Integration
- **Use together when**: User tracks work in beads (`.beads/issues.jsonl`)
- **Benefit**: GO decisions auto-create P1 epics with pilot metadata, NO-GO decisions auto-close discovery tasks
- **Integration point**: After Week 4 decision, agent creates/closes beads tasks and logs to `backlog-updates.jsonl`
- **Optional**: Can run pilots without SAP-015, but backlog updates must be done manually

**SAP-019 (Self-Evaluation)** - SAP Quality Validation
- **Use together when**: Piloting a new SAP capability (not just a feature)
- **Benefit**: Use `sap-evaluator.py` to check artifact completeness, version consistency, link validity
- **Integration point**: Week 0 research phase - validate candidate SAP has ≥3 of 5 artifacts before piloting
- **Example**: Before piloting SAP-029, run `python scripts/sap-evaluator.py SAP-029` to check readiness

**SAP-016 (Link Validation)** - Documentation Quality
- **Use together when**: Pilot includes documentation artifacts with cross-references
- **Benefit**: Validate links in pilot reports and adoption blueprints before GO decision
- **Integration point**: Week 4 validation phase - run `bash scripts/validate-awareness-links.sh` on pilot docs
- **Example**: Before promoting pilot to Wave 1, ensure all internal links work correctly

---

## 5. Error Patterns & Troubleshooting

### Error Pattern 1: "Pilot score below threshold (6.2), but user wants to proceed anyway"

**Symptoms**:
- Week -1 discovery scoring produces weighted score <7.0 (e.g., 6.2)
- User says "Let's pilot it anyway" or "I have a gut feeling about this"
- Agent is unsure whether to override threshold

**Cause**: Discovery scoring is a guide, not a hard rule. Low-risk pilots can proceed below threshold if user accepts trade-offs.

**Agent Solution**:
1. **Acknowledge the low score**: "SAP-XXX scored 6.2, below the 7.0 threshold. This suggests higher risk or lower ROI."
2. **Identify weak factors**: "Evidence score is 4/10 (weak). Would adding 2-3 Level A sources improve confidence?"
3. **Offer pilot modifications**: "For low-scoring candidates, recommend Level 1 (simplified) pilot to reduce investment (3-4 hours vs 6-8 hours)."
4. **User's choice**: If user still wants to proceed, document the risk in pilot plan:
   ```markdown
   ## Risk Assessment
   **Discovery Score**: 6.2/10 (below 7.0 threshold)
   **Weak factors**: Evidence (4/10), Feasibility (5/10)
   **Risk acceptance**: User acknowledged risk, proceeding with Level 1 pilot to minimize investment
   ```
5. **Verify**: Log risk acceptance to A-MEM: `{"event_type":"pilot_started","risk_acceptance":true,"weighted_score":6.2}`

**Prevention**: Use discovery scoring as a discussion tool, not a gate. User has final say.

---

### Error Pattern 2: "GO/NO-GO composite score is 58%, but 1 hard gate passed (satisfaction 90%)"

**Symptoms**:
- Week 4 evaluation shows composite score 58% (below 60% GO threshold)
- However, satisfaction is 90% (above 85% hard gate)
- User asks "Should we GO because satisfaction is high?"

**Cause**: Composite score and hard gates are both required. High satisfaction doesn't compensate for failed time savings or bugs.

**Agent Solution**:
1. **Check all hard gates individually**:
   ```bash
   time_savings: 3x < 5x ❌ FAIL
   satisfaction: 90% ≥ 85% ✅ PASS
   bugs: 2 > 0 ❌ FAIL
   adoption: 3 ≥ 2 ✅ PASS
   ```
2. **Explain decision logic**: "Composite score (58%) is below 60%, AND 2 hard gates failed (time_savings, bugs). This is a NO-GO decision."
3. **Recommend narrower scope**: "High satisfaction (90%) indicates user value. Consider narrowing scope to fix bugs and improve time savings, then re-pilot in Q2."
4. **Document lessons learned**: Create `lessons-learned-pilot-*.md` with root causes for low time savings and bugs
5. **Demote to Wave 3**: Update vision document with "Revisit when bugs fixed and time savings improved to 5x"

**Prevention**: Always check BOTH composite score AND all 4 hard gates. ANY failure → NO-GO.

---

### Error Pattern 3: "A-MEM events not logged - can't calculate pilot metrics"

**Symptoms**:
- Week 4 evaluation - agent tries to calculate time savings from A-MEM events
- `grep "pilot_" .chora/memory/events/dogfooding.jsonl` returns empty
- No `pilot_started` event found

**Cause**: SAP-010 (Memory System) not installed, or events not logged during pilot

**Agent Solution**:
1. **Check SAP-010 adoption**: `test -d .chora/memory/events/ && echo "✅ SAP-010 installed" || echo "❌ SAP-010 missing"`
2. **If missing**: "SAP-010 (Memory System) is required for SAP-027. Install SAP-010 first: see adoption-blueprint.md"
3. **If installed but no events**: "Pilot events were not logged. For Week 4 evaluation, manually document metrics in `go-no-go-decision.md`:
   ```markdown
   ### Manually Collected Metrics
   - Time savings: 6x (baseline: 30min, after: 5min) - measured from 3 team members
   - Satisfaction: 85% (17/20 users rated 4-5 stars)
   - Bugs: 0 critical/major bugs (checked issue tracker)
   - Adoption: 3 projects (chora-base, chora-compose, chora-studio)
   ```
4. **Prevent future issues**: Add A-MEM logging to pilot checklist:
   - [ ] Log `pilot_started` event (Week 1)
   - [ ] Log `pilot_completed` event (Week 4)
   - [ ] Log `pilot_go_decision` or `pilot_no_go_decision` (Week 4)

**Prevention**: Before starting pilot, verify SAP-010 is installed and create `pilot_started` event as first action.

---

### Error Pattern 4: "User wants to skip Week 0 research for a high-risk capability"

**Symptoms**:
- Week -1 discovery selected candidate with evidence_score 3/10 (very weak)
- User says "Let's skip research and go straight to build"
- Agent is concerned about lack of evidence

**Cause**: User underestimates risk or is time-pressured. Research phase prevents costly failed pilots.

**Agent Solution**:
1. **Assess risk level**: "Evidence score is 3/10 (weak). Skipping research increases risk of NO-GO decision."
2. **Quantify research investment**: "Week 0 research takes 4-6 hours. Failed pilot costs 25-50 hours. Research ROI is 5-10x."
3. **Offer compromise**: "Run abbreviated research (2 hours):
   - Find 3 Level A sources (standards, peer-reviewed)
   - Find 3 Level B sources (case studies)
   - Document in `research-report.md`
   This gives 60% confidence (Level A: 50%, Level B: 50%) - borderline acceptable."
4. **User's choice**: If user insists on skipping:
   ```markdown
   ## Risk Assessment
   **Research skipped**: Yes (user decision)
   **Evidence score**: 3/10 (weak)
   **Risk**: High likelihood of NO-GO decision if assumptions are wrong
   **Mitigation**: Build MVP in Week 1, validate assumptions early, pivot if needed
   ```
5. **Log risk**: `{"event_type":"pilot_started","research_skipped":true,"evidence_score":3,"risk_level":"high"}`

**Prevention**: For candidates with evidence_score <5, require Week 0 research (non-negotiable for Level 2/3 pilots). Only allow skipping for Level 1 (simplified) pilots.

---

## 6. Agent Communication Patterns

### Explaining Dogfooding Patterns to Users

**Simple Explanation** (for beginners):
> "Dogfooding means using your own product before shipping it. SAP-027 gives you a 4-week pilot process: build a feature internally, use it yourself 2+ times, measure if it saves time and satisfies users, then decide GO (ship it) or NO-GO (defer or redesign)."

**Technical Explanation** (for experienced users):
> "SAP-027 is a formalized 6-week pilot methodology (Week -1: discovery scoring, Week 0: evidence-based research, Weeks 1-3: build, Week 4: validation with GO/NO-GO decision at ≥60% composite score from 4 weighted metrics). Integrates with SAP-006 (vision promotion/demotion), SAP-010 (A-MEM event logging), and SAP-015 (beads epic/task management)."

### Common User Questions

**Q: How long does a full pilot take?**

**Agent Response**:
- **Level 1 (simplified)**: 3-4 hours (skip discovery & research, focus on build + validation only)
- **Level 2 (full pilot)**: 25-42 hours total (Week -1: 2h discovery, Week 0: 4-6h research, Weeks 1-3: 15-30h build, Week 4: 2-4h validation)
- **Level 3 (production)**: Same 25-42 hours per pilot, but setup investment (12-16h) amortizes across 10+ pilots

Recommend starting with Level 1 for first pilot, upgrade to Level 2 after 2-3 pilots, Level 3 after 5+ pilots.

---

**Q: What if my pilot scores 58% (below 60% GO threshold) but users love it (95% satisfaction)?**

**Agent Response**:
NO-GO is the correct decision. Here's why:
1. **Composite score (58% < 60%)**: Indicates overall metrics don't meet bar
2. **High satisfaction (95%)**: Great signal, but check other factors:
   - Time savings: If <5x, feature is valuable but inefficient
   - Bugs: If >0, feature is valuable but unstable
   - Adoption: If <2, not validated across diverse use cases

**Recommendation**: Narrow scope to fix the weak factors (improve time savings, fix bugs, expand adoption), then re-pilot in Q2. High satisfaction means the core idea is sound.

See protocol-spec.md Section 4.2 (GO/NO-GO Decision Logic) for scoring details.

---

**Q: Can I pilot a feature without SAP-006 (vision) or SAP-015 (beads)?**

**Agent Response**:
Yes, SAP-027 works standalone:
- **Required**: SAP-010 (Memory System) for event logging and metrics tracking
- **Optional**: SAP-006 (vision promotion/demotion), SAP-015 (epic/task management)

Without SAP-006: Manually update your roadmap/vision document after GO/NO-GO decision
Without SAP-015: Manually create/close tasks in your existing task tracker (Jira, Linear, GitHub Issues)

However, integration saves time:
- SAP-006 integration: 5 minutes → 30 seconds (vision update)
- SAP-015 integration: 10 minutes → 2 minutes (epic creation + breakdown)

See adoption-blueprint.md Section 2.2 (Level 2 Integrations) for setup instructions.

---

**Q: How do I choose which feature to pilot when I have 20 candidates?**

**Agent Response**:
Use Week -1 discovery scoring (Workflow 1 in awareness-guide.md):

1. **Query intention inventory**: `cat .chora/memory/knowledge/notes/intention-inventory-*.md`
2. **Score each candidate** (0-10) using weighted criteria:
   - Evidence (40%): Level A/B sources available?
   - Alignment (30%): Wave 1 (strategic) vs Wave 3 (nice-to-have)?
   - Demand (20%): User request count
   - Feasibility (10%): Build effort estimate
3. **Threshold**: Select candidates ≥7.0 (below 7.0 = higher risk)
4. **Top 3-5**: Create `pilot-candidates-*.md` note with top scorers
5. **Select 1**: Pick highest score, or tie-break by strategic theme

**Time budget**: 1.5-2 hours for 20 candidates

**Example**: SAP-015 (Backlog Organization) scored 8.2 (evidence: 9, alignment: 8, demand: 7, feasibility: 9) → Selected. SAP-033 (Advanced Code Generation) scored 6.5 (evidence: 5, alignment: 7, demand: 8, feasibility: 6) → Deferred.

---

**Q: What's the difference between Level 1, Level 2, and Level 3 adoption?**

**Agent Response**:
| Aspect | Level 1 (Simplified) | Level 2 (Full Pilot) | Level 3 (Production) |
|--------|---------------------|---------------------|----------------------|
| **Setup time** | 3-4 hours | 6-8 hours | 12-16 hours (one-time) |
| **Phases** | Build + Validate | Discovery + Research + Build + Validate | Same as Level 2 + Automation |
| **Automation** | Manual | Manual | Multi-pilot dashboard, vision sync |
| **Evidence requirements** | None (skip research) | ≥30% Level A, ≥40% Level B | Same as Level 2 |
| **Suitable for** | First-time users, low-risk features | Serious validation, medium-risk | **Production** (5+ pilots/year) |

**Recommendation**: Start with Level 1 (simplest), then upgrade to Level 2 after 2-3 successful pilots, then Level 3 after 5+ pilots.

See adoption-blueprint.md for detailed setup instructions for each level.

---

## 7. Best Practices for Agents

### Do's ✅

- ✅ **Always verify SAP-010 (Memory System) before starting pilot** - Required for event logging and metrics tracking. Check: `test -d .chora/memory/events/`
- ✅ **Log pilot_started event immediately in Week 1** - Establishes pilot start time for time-to-completion metrics
- ✅ **Check BOTH composite score AND hard gates for GO/NO-GO decision** - ANY failure (composite <60% OR any hard gate fail) → NO-GO
- ✅ **Document lessons learned for NO-GO decisions** - Create `lessons-learned-pilot-*.md` with root causes and recommendations (prevents repeat failures)
- ✅ **Use weighted scoring (7.0 threshold) as a guide, not a gate** - User has final say on pilot candidates; document risk if proceeding below threshold
- ✅ **Recommend Level 1 (simplified) for first-time users** - 3-4 hour setup reduces adoption friction (vs 6-8 hours for Level 2)
- ✅ **Integrate with SAP-006 (vision) and SAP-015 (beads) if available** - Automates promotion/demotion and epic/task management (5-10 min time savings per pilot)

### Don'ts ❌

- ❌ **Don't skip Week 0 research for high-risk pilots (evidence_score <5)** - Research investment (4-6h) prevents failed pilots (25-50h waste)
- ❌ **Don't override NO-GO decision based on single metric** - High satisfaction alone doesn't justify GO if time savings, bugs, or adoption fail
- ❌ **Don't pilot trivial features (<2 weeks build)** - Pilot overhead (6-8h for Level 2) not justified for low-risk features
- ❌ **Don't forget to close discovery tasks after NO-GO** - Prevents stale tasks from cluttering backlog
- ❌ **Don't start pilots without intention inventory** - Week -1 discovery requires candidate features; create inventory first if missing
- ❌ **Don't run pilots without SAP-010** - Can't track metrics without A-MEM event logging; install SAP-010 first
- ❌ **Don't batch multiple pilots without Level 3 automation** - Level 1/2 pilots are manual; running 3+ pilots simultaneously creates chaos

### Efficiency Tips

**Tip 1: Reuse scoring scripts for Week -1 discovery**
- **Why**: Scoring 20 candidates manually takes 2 hours; script reduces to 15 minutes
- **How**: Create `scripts/score-pilot-candidates.py` using Pattern 1 from Section 3 (Quick Reference). Pass intention inventory JSON, output sorted candidates ≥7.0 threshold.

**Tip 2: Create pilot plan template for Level 1 (simplified)**
- **Why**: Reduces pilot setup from 3-4 hours to 1 hour (template pre-fills boilerplate)
- **How**: Save Level 1 pilot plan template to `docs/pilots/pilot-template-level-1.md`:
  ```markdown
  # Pilot: {Capability Name}

  ## Goal
  {What you want to achieve}

  ## Build Phase (Weeks 1-2)
  - [ ] {Build task 1}
  - [ ] {Build task 2}

  ## Validate Phase (Week 3)
  - [ ] Use capability 2+ times
  - [ ] Collect satisfaction feedback (1-5 scale)
  - [ ] Note any bugs or issues

  ## Decision
  - Continue? Yes/No
  - Next steps: {What to do after pilot}
  ```
  Copy template: `cp docs/pilots/pilot-template-level-1.md docs/pilots/pilot-$(date +%Y-%m-%d)-{name}.md`

**Tip 3: Batch A-MEM logging at end of each phase**
- **Why**: Logging every action individually is time-consuming; batch logging takes 1 minute per phase
- **How**:
  - Week 1 (build start): Log `pilot_started`
  - Week 4 (validation complete): Log `pilot_completed` + `pilot_go_decision` or `pilot_no_go_decision`
  - Post-decision: Log `vision_updated` + `backlog_updated` (if SAP-006/015 integrated)

**Tip 4: Automate vision sync at Level 3**
- **Why**: Manual vision updates take 5 minutes per pilot; automation reduces to 30 seconds
- **How**: Use `scripts/sync-to-vision.sh` from adoption-blueprint.md Section 3.2 (Level 3). Reads GO/NO-GO decisions from A-MEM, auto-promotes/demotes features in vision document.

---

## 8. Validation & Quality Checks

### Agent Self-Check Checklist

Before completing a task with SAP-027, agents should verify:

#### Week -1 Discovery Checklist
- [ ] Intention inventory queried successfully: `test -f .chora/memory/knowledge/notes/intention-inventory-*.md`
- [ ] ≥3 candidates scored above 7.0 threshold
- [ ] `pilot-candidates-*.md` note created with weighted scores and rationale
- [ ] Top candidate selected and user approved

#### Week 0 Research Checklist (Level 2+ only)
- [ ] ≥10 total sources collected
- [ ] ≥30% Level A sources (standards, peer-reviewed papers)
- [ ] ≥40% Level B sources (case studies, industry benchmarks)
- [ ] ≤30% Level C sources (expert opinion, blogs)
- [ ] Research report documented: `docs/pilots/pilot-{date}-{name}/research-report.md`

#### Week 1-3 Build Checklist
- [ ] `pilot_started` event logged to A-MEM: `grep "pilot_started" .chora/memory/events/dogfooding.jsonl`
- [ ] Feature built and internally deployed
- [ ] Pilot plan tracked: `docs/pilots/pilot-{date}-{name}/pilot-plan.md`
- [ ] ≥2 team members using feature (adoption requirement)

#### Week 4 Validation Checklist
- [ ] Feature used ≥2 times by team
- [ ] Time savings measured (baseline vs after)
- [ ] Satisfaction collected (1-5 scale, ≥85% target = 4.25/5)
- [ ] Bug count tracked (critical/major only)
- [ ] Adoption count verified (≥2 projects/teams)
- [ ] GO/NO-GO decision documented: `docs/pilots/pilot-{date}-{name}/go-no-go-decision.md`
- [ ] `pilot_completed` event logged to A-MEM

#### Post-Decision Checklist (GO)
- [ ] Composite score ≥60%
- [ ] All hard gates passed (time_savings ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2)
- [ ] Vision document updated (Wave 2 → Wave 1 promotion)
- [ ] `vision_updated` event logged to A-MEM
- [ ] P1 epic created in beads (if SAP-015 adopted)
- [ ] `backlog_updated` event logged to A-MEM
- [ ] User confirmed next steps

#### Post-Decision Checklist (NO-GO)
- [ ] Composite score <60% OR any hard gate failed
- [ ] Lessons learned documented: `.chora/memory/knowledge/notes/lessons-learned-pilot-*.md`
- [ ] Root causes identified (weak evidence, scope too broad, technical challenges)
- [ ] Recommendations provided (narrow scope, add validation, defer to Q3)
- [ ] Vision document updated (Wave 2 → Wave 3 demotion)
- [ ] `vision_updated` event logged to A-MEM
- [ ] Discovery task closed in beads (if SAP-015 adopted)
- [ ] P3 future task created (if revisit planned)
- [ ] `backlog_updated` event logged to A-MEM

### Validation Commands

```bash
# Primary validation: Check SAP-027 adoption status
python scripts/sap-evaluator.py --quick SAP-027
# Expected: ✅ SAP-027 (dogfooding-patterns), Level: 1/2/3, Next: [upgrade path]

# Verify SAP-010 (Memory System) installed (required)
test -d .chora/memory/events/ && echo "✅ SAP-010 installed" || echo "❌ SAP-010 missing - install first"

# Verify pilot events logged to A-MEM
grep "pilot_" .chora/memory/events/dogfooding.jsonl | jq .
# Expected: pilot_started, pilot_completed, pilot_go_decision OR pilot_no_go_decision

# Check intention inventory exists (for Week -1 discovery)
ls -lt .chora/memory/knowledge/notes/intention-inventory-*.md | head -1
# Expected: Recent intention-inventory-YYYY-MM-DD.md file

# Verify pilot directory structure
test -d docs/pilots/pilot-$(date +%Y-%m-%d)-{name}/ && echo "✅ Pilot directory exists" || echo "❌ Create pilot directory"

# Check GO/NO-GO decision document
test -f docs/pilots/pilot-{date}-{name}/go-no-go-decision.md && echo "✅ Decision documented" || echo "❌ Document decision"

# Verify vision integration (if SAP-006 adopted)
grep "pilot-{date}-{name}" .chora/memory/knowledge/notes/vision-{project}-2025.md
# Expected: Feature promoted to Wave 1 (GO) or demoted to Wave 3 (NO-GO)

# Verify beads integration (if SAP-015 adopted)
bd list --labels "pilot-validated" --json | jq '.[].title'
# Expected: P1 epics for GO decisions

# Check lessons learned (NO-GO only)
test -f .chora/memory/knowledge/notes/lessons-learned-pilot-{date}-{name}.md && echo "✅ Lessons documented" || echo "⚠️  Document lessons for NO-GO"
```

---

## 9. Version Compatibility

**Current Version**: 1.0.0

### Compatibility Notes

- **SAP-027 1.0.0** is compatible with:


  - SAP-000 1.0.0+

  - SAP-029 1.0.0+



### Breaking Changes

**No breaking changes** (initial release)

---

## 10. Additional Resources

### Within chora-base

- [Protocol Specification](./protocol-spec.md) - Technical contracts
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Capability Charter](./capability-charter.md) - Problem statement and scope

### External Resources

**Dogfooding Methodology**:
- [Wikipedia: Eating your own dog food](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) - History and overview of dogfooding practice
- [Google Research: Dogfooding at Scale](https://research.google/pubs/pub43146/) - Large-scale internal product validation
- [Amazon's "Working Backwards" Process](https://www.product-frameworks.com/Amazon-Product-Management.html) - Customer-centric validation (similar to dogfooding)

**Evidence-Based Research**:
- [Oxford Centre for Evidence-Based Medicine Levels](https://www.cebm.ox.ac.uk/resources/levels-of-evidence) - Evidence quality pyramid (Level A/B/C)
- [Cochrane Handbook for Systematic Reviews](https://training.cochrane.org/handbook) - Research evidence standards

**GO/NO-GO Decision Frameworks**:
- [Stage-Gate Process (Robert G. Cooper)](https://www.stage-gate.com/) - Product development gates with GO/KILL decisions
- [Google's HEART Framework](https://www.dtelepathy.com/ux-metrics/#happiness) - Happiness, Engagement, Adoption, Retention, Task Success metrics
- [RICE Prioritization (Intercom)](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) - Reach, Impact, Confidence, Effort scoring

**Pilot Metrics & KPIs**:
- [Atlassian: Team Playbook - Pilot Programs](https://www.atlassian.com/team-playbook/plays/pilot-program) - Internal validation patterns
- [ProductPlan: How to Run a Product Pilot](https://www.productplan.com/glossary/product-pilot/) - Pilot program best practices

**Vision & Roadmap Integration**:
- [Amplitude: Product Waves Framework](https://amplitude.com/blog/product-roadmap) - Wave 1/2/3 strategic planning
- [Pragmatic Institute: Strategic Roadmaps](https://www.pragmaticinstitute.com/resources/articles/product/strategic-product-roadmaps/) - Roadmap prioritization with evidence

---

**For Agents**: This awareness guide is your quick reference. For detailed technical specifications, see [protocol-spec.md](./protocol-spec.md). For installation instructions, see [adoption-blueprint.md](./adoption-blueprint.md).

**Version**: 1.0.0 (2025-11-03)