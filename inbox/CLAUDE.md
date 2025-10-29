# Claude Code Patterns: Cross-Repository Inbox Management

**Purpose:** Guide Claude Code through cross-repo inbox workflows
**Audience:** Claude Code (AI assistant)
**Last Updated:** 2025-10-27

---

## Quick Reference

**You are working with a cross-repository inbox system that coordinates work across multiple repos in the Liminal Commons ecosystem.**

**Three intake types:**
1. **Strategic Proposals** (Type 1) → Quarterly review → Vision & Strategy
2. **Coordination Requests** (Type 2) → Sprint planning → Cross-repo dependencies
3. **Implementation Tasks** (Type 3) → Continuous → Your existing DDD → BDD → TDD workflow

**Key locations:**
- `inbox/ecosystem/` - Strategic proposals, RFCs, ADRs
- `inbox/incoming/` - New coordination requests and tasks
- `inbox/active/` - Work in progress
- `inbox/completed/` - Archived completed work
- `inbox/coordination/` - Event logs, capabilities, ecosystem status

---

## Pattern 1: Processing Incoming Coordination Requests

**When the user says:** "Review coordination requests" or "Check inbox/incoming/coordination/"

### Your Workflow

1. **List all coordination requests:**
   ```bash
   ls -1 inbox/incoming/coordination/*.json
   ```

2. **For each request, read and summarize:**
   ```bash
   cat inbox/incoming/coordination/coord-NNN.json
   ```

3. **Check if we can handle it:**
   ```bash
   # Read our capabilities
   cat inbox/coordination/CAPABILITIES/chora-base.yaml

   # Check if category matches what we can receive
   yq '.capabilities.can_receive[] | select(.type == "coordination")' \
     inbox/coordination/CAPABILITIES/chora-base.yaml
   ```

4. **Provide triage recommendation:**
   ```markdown
   ## Coordination Request: coord-NNN

   **From:** {from_repo}
   **To:** {to_repo}
   **Title:** {title}
   **Priority:** {priority}
   **Urgency:** {urgency}

   **Deliverables:**
   - {list deliverables}

   **Can we handle this?** {Yes/No based on capabilities}

   **Blocks:** {what this blocks}

   **Recommendation:** {This Sprint / Next Sprint / Reject}
   **Rationale:** {why}
   ```

5. **If accepted for this sprint:**
   ```bash
   # Move to active
   mkdir -p inbox/active/coord-NNN-{title}/
   mv inbox/incoming/coordination/coord-NNN.json \
      inbox/active/coord-NNN-{title}/coordination.json

   # Emit event
   echo '{"event_type": "coordination_request_accepted", "request_id": "coord-NNN", "trace_id": "...", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl

   # Ask user: "Should I begin Phase 3 (DDD) and create change-request.md?"
   ```

---

## Pattern 2: Starting Work on a Task

**When the user says:** "Work on task-NNN" or "Start inbox/active/task-NNN/"

### Your Workflow

1. **Check if task exists:**
   ```bash
   # In active?
   ls inbox/active/task-NNN-*/task.json 2>/dev/null

   # Or in incoming?
   ls inbox/incoming/tasks/task-NNN.json 2>/dev/null
   ```

2. **If in incoming/, move to active:**
   ```bash
   mkdir -p inbox/active/task-NNN-{title}/
   mv inbox/incoming/tasks/task-NNN.json \
      inbox/active/task-NNN-{title}/task.json

   # Set trace ID
   export CHORA_TRACE_ID=$(jq -r '.trace_id // "task-NNN-trace"' \
     inbox/active/task-NNN-{title}/task.json)

   # Emit event
   echo '{"event_type": "task_started", "task_id": "task-NNN", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

3. **Read task to understand requirements:**
   ```bash
   cat inbox/active/task-NNN-{title}/task.json
   ```

4. **Phase 3: DDD - Create change request (if doesn't exist):**
   ```markdown
   ---
   title: {task title}
   type: change-request
   task_id: task-NNN
   phase: 3-ddd
   created: {date}
   ---

   # Change Request: {title}

   ## Explanation
   ### Context
   {from task.json context.background}

   ### Problem Statement
   {infer from title and deliverables}

   ### Business Value
   {infer or ask user}

   ### Stakeholders
   {infer from task.json}

   ### Dependencies
   {from task.json dependencies[]}

   ## How-to Guide
   ### User Workflow
   {infer from deliverables and acceptance_criteria}

   ### Expected Journey
   {describe step-by-step}

   ### Common Use Cases
   {infer from context}

   ### Error Scenarios
   {consider edge cases}

   ## Reference
   ### API Design
   {design based on deliverables}

   ### Parameters & Types
   {define interfaces}

   ### Examples
   {provide code examples}

   ### Performance Requirements
   {from task.json estimated_effort}

   ## Acceptance Criteria
   {copy from task.json acceptance_criteria[]}

   Given-When-Then format:
   {convert to Gherkin-style}

   ## Tutorial (Optional)
   {if complex, provide end-to-end walkthrough}
   ```

5. **Ask user for approval:**
   ```markdown
   I've created the DDD change request: inbox/active/task-NNN-{title}/change-request.md

   **Next steps:**
   1. Review the change request
   2. I'll create BDD scenarios (Phase 4: BDD)
   3. Then implement using TDD (Phase 4: TDD)

   Ready to proceed with BDD?
   ```

6. **Emit phase completion event:**
   ```bash
   echo '{"event_type": "phase_completed", "phase": "ddd", "duration_hours": 1.5, "task_id": "task-NNN", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

---

## Pattern 3: Implementing with BDD + TDD

**After DDD change request is approved**

### Phase 4: BDD (Behavior Driven Development)

1. **Create features/ directory:**
   ```bash
   mkdir -p inbox/active/task-NNN-{title}/features/
   ```

2. **Write Gherkin scenarios from acceptance criteria:**
   ```gherkin
   # inbox/active/task-NNN-{title}/features/feature-name.feature

   Feature: {Feature Name from change request}

   Scenario: {Acceptance Criterion 1}
     Given {precondition}
     When {action}
     Then {expected result}

   Scenario: {Acceptance Criterion 2}
     Given {precondition}
     When {action}
     Then {expected result}
   ```

3. **Emit event:**
   ```bash
   echo '{"event_type": "phase_completed", "phase": "bdd", "duration_hours": 0.5, "task_id": "task-NNN", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

### Phase 4: TDD (Test Driven Development)

1. **For each behavior:**
   - Write test (RED - fails)
   - Implement minimal code (GREEN - passes)
   - Refactor (improve design, tests stay GREEN)

2. **Run tests frequently:**
   ```bash
   pytest inbox/active/task-NNN-{title}/tests/ -v
   ```

3. **Check coverage:**
   ```bash
   pytest inbox/active/task-NNN-{title}/tests/ --cov=src/ --cov-report=term
   ```

4. **When all tests pass with ≥85% coverage:**
   ```bash
   echo '{"event_type": "tests_passing", "total": 12, "passed": 12, "coverage": 95.2, "task_id": "task-NNN", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl

   echo '{"event_type": "phase_completed", "phase": "tdd", "duration_hours": 4.0, "task_id": "task-NNN", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

5. **Ask user:**
   ```markdown
   ✅ All tests passing (95.2% coverage)
   ✅ All acceptance criteria met
   ✅ Code quality checks passed

   Ready to move to completed/?
   ```

---

## Pattern 4: Completing Work

**When work is done and approved**

### Your Workflow

1. **Create completion directory:**
   ```bash
   mkdir -p inbox/completed/task-NNN-{title}/
   ```

2. **Move artifacts:**
   ```bash
   mv inbox/active/task-NNN-{title}/* \
      inbox/completed/task-NNN-{title}/
   ```

3. **Filter events by trace_id:**
   ```bash
   grep '"trace_id": "'$CHORA_TRACE_ID'"' inbox/coordination/events.jsonl \
     > inbox/completed/task-NNN-{title}/events.jsonl
   ```

4. **Create metadata.json:**
   ```json
   {
     "task_id": "task-NNN",
     "title": "{title}",
     "type": "task",
     "started": "{from first event}",
     "completed": "{now}",
     "duration_hours": {calculate from events},
     "phase_durations": {
       "ddd": {from events},
       "bdd": {from events},
       "tdd": {from events}
     },
     "test_results": {
       "total_tests": 12,
       "passed": 12,
       "failed": 0,
       "coverage_percent": 95.2
     },
     "deliverables": [
       {list from task.json}
     ],
     "trace_id": "{CHORA_TRACE_ID}"
   }
   ```

5. **Add test and coverage reports:**
   ```bash
   cp test-output/report.json \
      inbox/completed/task-NNN-{title}/test-report.json

   cp coverage-output/report.json \
      inbox/completed/task-NNN-{title}/coverage-report.json
   ```

6. **Create release notes fragment:**
   ```markdown
   ### Added
   - {what was added}

   ### Changed
   - {what changed}

   ### Fixed
   - {what was fixed}

   ### Documentation
   - {docs updated}

   ### Tests
   - {test coverage}
   ```

7. **Emit completion event:**
   ```bash
   echo '{"event_type": "task_completed", "task_id": "task-NNN", "duration_hours": 6.5, "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

8. **If this fulfilled a coordination request, notify:**
   ```bash
   # Check if task has parent coordination request
   if jq -e '.parent.type == "coordination"' inbox/completed/task-NNN-{title}/task.json; then
     parent_id=$(jq -r '.parent.id' inbox/completed/task-NNN-{title}/task.json)

     echo '{"event_type": "coordination_request_fulfilled", "request_id": "'$parent_id'", "to_repo": "{from_repo}", "trace_id": "'$CHORA_TRACE_ID'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
       >> inbox/coordination/events.jsonl

     echo "✅ Notified {from_repo} that coordination request $parent_id is fulfilled"
   fi
   ```

9. **Summary to user:**
   ```markdown
   ✅ Task task-NNN completed and archived

   **Duration:** 6.5 hours
   - DDD: 1.5 hours
   - BDD: 0.5 hours
   - TDD: 4.0 hours
   - Review: 0.5 hours

   **Quality:**
   - Tests: 12 passing
   - Coverage: 95.2%
   - Mypy: 0 errors
   - Ruff: 0 violations

   **Artifacts:**
   - inbox/completed/task-NNN-{title}/change-request.md
   - inbox/completed/task-NNN-{title}/events.jsonl
   - inbox/completed/task-NNN-{title}/metadata.json
   - inbox/completed/task-NNN-{title}/test-report.json
   - inbox/completed/task-NNN-{title}/release-notes-fragment.md

   **Next steps:**
   - Ready for PR
   - Or should I commit changes first?
   ```

---

## Pattern 5: Checking Ecosystem Status

**When the user says:** "Check ecosystem status" or "What's blocked?"

### Your Workflow

1. **Read ecosystem status:**
   ```bash
   cat inbox/coordination/ECOSYSTEM_STATUS.yaml
   ```

2. **Summarize current state:**
   ```markdown
   ## Liminal Commons Ecosystem Status

   **Updated:** {from ECOSYSTEM_STATUS.yaml}

   ### Repositories ({total})
   {for each repo:}
   - **{repo_name}** - {status} - v{version}
     - Active work: {list active_work}
     - Pending coordination: {list pending_coordination}
     - Blocked by: {list blocked_by}
     - Health: {health}

   ### Waypoints
   {for each waypoint:}
   - **{name}** - {status} - {progress}%
     - Blocked by: {list blocked_by}

   ### Coordination
   - Active requests: {count}
   - Pending fulfillment: {count}

   ### Current Sprint
   - **{sprint}** ({start_date} to {end_date})
   - Focus: {focus}
   - Velocity target: {velocity_target}
   ```

3. **Highlight blockers:**
   ```bash
   # Find all blocked work
   yq '.repositories[] | select(.blocked_by | length > 0) |
       {repo: .name, blocked_by: .blocked_by}' \
     inbox/coordination/ECOSYSTEM_STATUS.yaml

   yq '.waypoints[] | select(.blocked_by | length > 0) |
       {waypoint: .name, blocked_by: .blocked_by}' \
     inbox/coordination/ECOSYSTEM_STATUS.yaml
   ```

4. **Provide recommendations:**
   ```markdown
   ### Recommendations

   {if blockers exist:}
   **Unblock:**
   - {blocker 1} - Suggested action: {action}
   - {blocker 2} - Suggested action: {action}

   {if no blockers:}
   **All clear!** No blockers detected.

   **Next priorities:**
   1. {highest priority pending work}
   2. {next priority}
   ```

---

## Pattern 6: Creating a Coordination Request

**When user needs something from another repo**

### Your Workflow

1. **Check target repo's capabilities:**
   ```bash
   # Does ecosystem-manifest handle coordination requests?
   yq '.capabilities.can_receive[] | select(.type == "coordination")' \
     inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

   # What categories can it handle?
   yq '.capabilities.can_receive[] |
       select(.type == "coordination") | .category[]' \
     inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml
   ```

2. **Create coordination request JSON:**
   ```json
   {
     "type": "coordination",
     "request_id": "coord-NNN",
     "title": "{brief description}",
     "created": "{YYYY-MM-DD}",
     "from_repo": "chora-base",
     "to_repo": "ecosystem-manifest",
     "priority": "P0",
     "urgency": "blocks_sprint",
     "blocks": [
       "{what this blocks}"
     ],
     "requested_by": "{user or team}",
     "requested_delivery": "Week N",
     "context": {
       "waypoint": "W3",
       "related_rfc": "rfcs/0001-health-monitoring.md",
       "background": "{why needed}"
     },
     "deliverables": [
       "{what needs to be delivered}"
     ],
     "acceptance_criteria": [
       "{how to verify completion}"
     ],
     "dependencies": [
       "{prerequisites}"
     ],
     "estimated_effort": "4-8 hours",
     "trace_id": "{generate unique ID}"
   }
   ```

3. **Save to incoming/coordination/:**
   ```bash
   echo '{json}' > inbox/incoming/coordination/coord-NNN.json
   ```

4. **Emit event:**
   ```bash
   trace_id=$(jq -r '.trace_id' inbox/incoming/coordination/coord-NNN.json)

   echo '{"event_type": "coordination_request_created", "request_id": "coord-NNN", "from_repo": "chora-base", "to_repo": "ecosystem-manifest", "trace_id": "'$trace_id'", "timestamp": "'$(date -Iseconds)'", "repo": "chora-base"}' \
     >> inbox/coordination/events.jsonl
   ```

5. **Inform user:**
   ```markdown
   ✅ Created coordination request: coord-NNN

   **To:** ecosystem-manifest
   **Title:** {title}
   **Priority:** P0
   **Urgency:** blocks_sprint

   **Next steps:**
   1. This will be reviewed in next sprint planning (every 2 weeks)
   2. ecosystem-manifest team will triage and respond
   3. If accepted, they'll create implementation task
   4. When delivered, you'll receive notification event

   **Track progress:**
   - Watch `inbox/coordination/events.jsonl` for updates
   - Or check `inbox/coordination/ECOSYSTEM_STATUS.yaml`
   ```

---

## Pattern 7: Viewing Event Timeline

**When user says:** "Show me what happened with task-NNN" or "Event timeline for W3"

### Your Workflow

1. **Get trace ID:**
   ```bash
   # From completed task
   trace_id=$(jq -r '.trace_id' inbox/completed/task-NNN-{title}/task.json)

   # Or user-provided
   trace_id="ecosystem-w3-health-monitoring"
   ```

2. **Filter events:**
   ```bash
   grep '"trace_id": "'$trace_id'"' inbox/coordination/events.jsonl
   ```

3. **Pretty-print timeline:**
   ```bash
   grep '"trace_id": "'$trace_id'"' inbox/coordination/events.jsonl | \
     jq -r '"\(.timestamp) | \(.event_type) | \(.repo) | \(.task_id // .request_id // "-")"' | \
     column -t -s '|'
   ```

4. **Summarize to user:**
   ```markdown
   ## Event Timeline: {trace_id}

   | Timestamp | Event | Repo | ID |
   |-----------|-------|------|-----|
   {formatted timeline}

   **Duration:** {calculate from first to last event}
   **Repos involved:** {unique repos}
   **Total events:** {count}
   ```

---

## Tips for Claude Code

### 1. **Always Set Trace Context**
```bash
# At start of any multi-step work
export CHORA_TRACE_ID=$(jq -r '.trace_id // "task-NNN-trace"' task.json)

# Use in all event emissions
echo '{"trace_id": "'$CHORA_TRACE_ID'", ...}' >> inbox/coordination/events.jsonl
```

### 2. **Check Capabilities Before Routing**
```bash
# Don't create tasks for wrong repo
yq '.capabilities.can_receive[]' \
  inbox/coordination/CAPABILITIES/{repo}.yaml
```

### 3. **Follow Existing Process**
Your DDD → BDD → TDD workflow is unchanged. Inbox just adds:
- Intake routing (Type 1, 2, 3)
- Event logging
- Cross-repo notifications
- Archiving

### 4. **Emit Events Frequently**
At every phase transition:
- task_started
- phase_started
- phase_completed
- task_completed

### 5. **Archive Thoroughly**
When completing work, include:
- Original task/coordination JSON
- Change request markdown
- Filtered events (by trace_id)
- Metadata (durations, metrics)
- Test/coverage reports
- PR link
- Release notes fragment

### 6. **Update Ecosystem Status**
After significant work (waypoints completed, releases published), suggest updating:
```bash
inbox/coordination/ECOSYSTEM_STATUS.yaml
```

---

## Common Commands Reference

```bash
# List incoming coordination requests
ls -1 inbox/incoming/coordination/*.json

# List incoming tasks
ls -1 inbox/incoming/tasks/*.json

# List active work
ls -d inbox/active/*/

# Check capabilities for a repo
yq '.capabilities' inbox/coordination/CAPABILITIES/{repo}.yaml

# View ecosystem status
cat inbox/coordination/ECOSYSTEM_STATUS.yaml

# Filter events by trace ID
grep '"trace_id": "{trace_id}"' inbox/coordination/events.jsonl

# Filter events by repo
grep '"repo": "{repo}"' inbox/coordination/events.jsonl

# Count active coordination requests
ls inbox/incoming/coordination/*.json 2>/dev/null | wc -l

# Find blocked work
yq '.repositories[] | select(.blocked_by | length > 0)' \
  inbox/coordination/ECOSYSTEM_STATUS.yaml
```

---

## Questions?

See:
- [INBOX_PROTOCOL.md](INBOX_PROTOCOL.md) - Complete system documentation
- [INTAKE_TRIAGE_GUIDE.md](INTAKE_TRIAGE_GUIDE.md) - Decision criteria
- Directory READMEs - Detailed guidance for each directory

---

**Remember:** The inbox system is designed to **coordinate cross-repo work** while **preserving your existing development process**. Use it for coordination, not as a replacement for your DDD → BDD → TDD workflow.
