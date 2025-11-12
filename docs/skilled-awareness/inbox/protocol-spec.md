# Cross-Repository Inbox Skilled Awareness Package
## Protocol Specification

**Version:** 1.2.0
**Status:** Active (Level 3 - Production)
**Maintainer:** Capability Owner (Victor Piper)
**Last Updated:** 2025-11-11  

---

## 1. Overview
- **Purpose:** Provide a Git-native coordination protocol that standardizes intake, routing, and lifecycle management for cross-repository work across the Liminal Commons ecosystem.
- **Intended Consumers:**  
  - Repository maintainers implementing cross-repo coordination.  
  - AI agents (Claude, Codex) executing inbox triage and task processing.  
  - Ecosystem governance teams tracking strategic proposals and dependencies.
- **Modes of Operation:**  
  - **Planning Mode:** Focused on strategic proposals and coordination requests; quarterly and sprint-level cadences.  
  - **Execution Mode:** Handles approved implementation tasks through the DDD → BDD → TDD lifecycle.

---

## 2. Design Principles
1. **Git-First Coordination** — All state lives in the repository; no external services required.  
2. **Respect Lifecycle Phases** — Strategic, coordination, and implementation workflows align with evidence-based development phases.  
3. **Traceability by Default** — Every action emits structured events and maintains audit trails.  
4. **Agent Accessibility** — Protocol must be operable via machine-readable instructions with clearly defined command patterns.  
5. **Composable Adoption** — Downstream repos may enable protocol components incrementally while retaining compatibility.

---

## 3. Functional Requirements
- **FR-1:** Support three intake types (strategic, coordination, implementation) with distinct review cadences and schemas.  
- **FR-2:** Provide deterministic directory structure enabling queue states: `incoming`, `active`, `completed`, `ecosystem`, `coordination`.  
- **FR-3:** Maintain JSON schemas for each intake type; validation must succeed before progression.  
- **FR-4:** Emit append-only JSONL events capturing state transitions with `CHORA_TRACE_ID`.  
- **FR-5:** Offer triage workflow that aligns with development phases, including escalation paths.  
- **FR-6:** Integrate with capability-based routing per repository (e.g., `CAPABILITIES/<repo>.yaml`).  
- **FR-7:** Document operational patterns for AI agents (commands, move instructions, event emission).  
- **FR-8:** Provide adoption instructions and verification steps for downstream repositories.

---

## 4. Interfaces and Artifacts
- **Inputs:**  
  - Markdown documents for strategic proposals (`ecosystem/proposals/`).  
  - JSON payloads for coordination requests and implementation tasks (`incoming/coordination/`, `incoming/tasks/`).  
  - Capability descriptors (`coordination/CAPABILITIES/<repo>.yaml`).  
- **Outputs:**  
  - Event log (`coordination/events.jsonl`).  
  - Status snapshots (`coordination/ECOSYSTEM_STATUS.yaml`).  
  - Completed artifacts stored in `completed/` with archival metadata.  
- **CLI Hooks / Commands:**  
  - Standard shell commands for listing, moving, and validating files (e.g., `ls`, `cat`, `mkdir`, `mv`).  
  - Optional script hooks (future automation) for schema validation or reporting.

---

## 5. Operational Workflow
### Lifecycle Stages
1. **Intake:** Item added to `incoming/` (coordination or tasks) or `ecosystem/proposals/`.  
2. **Review:** Item evaluated at appropriate cadence (quarterly, sprint, continuous).  
3. **Activation:** Accepted items moved to `active/`; trace ID ensured.  
4. **Execution:** DDD → BDD → TDD phases executed; progress checkpoints recorded.  
5. **Completion:** Results stored and summarized in `completed/`; events emitted.  
6. **Feedback:** Lessons captured, ledger updated (see SAP ledger).

### Decision Branches
- **Planning vs Execution Mode:**  
  - Planning mode items require coordination review before activation.  
  - Execution mode tasks can be activated once prerequisites met.
- **Escalation Paths:** If capability mismatch or resource constraints observed, escalate via coordination request or strategic proposal update.

---

## 6. Governance & Compliance
- **Versioning Policy:** Semantic versioning; patch updates for documentation tweaks, minor for schema or workflow improvements, major for breaking structural changes.  
- **Compatibility Guarantees:** Downstream repos implementing `v1.x` must remain compatible with later `v1.y`; major version bump signals migration guide requirement.  
- **Audit Requirements:** Event log and status snapshots must be reviewable; adoption ledger to log version and feedback.  
- **Security / Privacy Considerations:** Protocol stores coordination data in repository; ensure sensitive information is sanitized before commit.

---

## 7. Coordination Request Schema Enhancements

### 7.1 Relationship Metadata (v1.1.1+)

**Purpose**: Enable graph-based curation and relationship tracking across coordination requests, tasks, and SAPs.

**New Fields**:

#### `relationships` Object (Optional)

Structured relationships to other coordination requests and work items:

```json
{
  "relationships": {
    "blocks": ["COORD-2025-020"],
    "blocked_by": [],
    "related_to": ["COORD-2025-004", "task-abc123"],
    "spawns_tasks": ["chora-base-def456"],
    "supersedes": "COORD-2025-001",
    "superseded_by": null
  }
}
```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `blocks` | array[string] | Work items blocked by this coordination request (COORD-YYYY-NNN or task IDs) |
| `blocked_by` | array[string] | Work items blocking this coordination request |
| `related_to` | array[string] | Related coordination requests or tasks (informational, no blocking) |
| `spawns_tasks` | array[string] | Task IDs created from this coordination request (for beads/SAP-015 integration) |
| `supersedes` | string | Coordination request ID that this request replaces/supersedes |
| `superseded_by` | string | Coordination request ID that replaces/supersedes this request |

**Use Cases**:

1. **Dependency Tracking**: Identify what's blocking work or what work is blocked
2. **Impact Analysis**: Find all coordination requests affected by a given request
3. **Task Decomposition**: Link coordination requests to decomposed beads tasks (SAP-015)
4. **Version Management**: Track superseded/superseding requests for continuity
5. **Graph Visualization**: Build relationship graphs for project planning

#### `affects_saps` Array (Optional)

SAP IDs affected by this coordination request:

```json
{
  "affects_saps": ["SAP-015", "SAP-009", "SAP-001"]
}
```

**Benefits**:
- SAP awareness: Know which SAPs are impacted by coordination work
- Impact analysis: Find all coordination requests affecting a specific SAP
- Adoption tracking: Correlate coordination with SAP adoption phases
- Cross-SAP visibility: Understand dependencies between SAP implementations

**Example Queries**:

```bash
# Find all coordination requests affecting SAP-015
jq 'select(.affects_saps? // [] | contains(["SAP-015"]))' inbox/**/*.json

# Count coordination requests by SAP
jq -r '.affects_saps[]? // empty' inbox/**/*.json | sort | uniq -c
```

#### `affects_domains` Array (Optional)

Documentation/code domains affected by this coordination request:

```json
{
  "affects_domains": [
    "docs/skilled-awareness/task-tracking",
    "implementation",
    "docs/user-docs",
    "scripts"
  ]
}
```

**Standard Domains**:
- `docs/skilled-awareness/*` - SAP documentation
- `docs/user-docs/*` - User-facing documentation
- `docs/dev-docs/*` - Developer documentation
- `docs/project-docs/*` - Project management documentation
- `implementation` - Source code
- `scripts` - Automation scripts
- `tests` - Test suites
- `.chora/*` - Chora configuration

**Benefits**:
- File impact awareness: Know which domains will change
- Cross-domain coordination: Identify work spanning multiple domains
- Scope estimation: Understand breadth of coordination work
- Curation: Filter coordination by affected domains

**Example Queries**:

```bash
# Find coordination affecting documentation
jq 'select(.affects_domains? // [] | any(. | startswith("docs/")))' inbox/**/*.json

# Find coordination affecting multiple domains
jq 'select((.affects_domains? // [] | length) > 2)' inbox/**/*.json
```

### 7.2 Integration with Other SAPs

**SAP-015 (Task Tracking / Beads)**:
- Use `relationships.spawns_tasks` to link coordination requests to beads tasks
- Use `affects_saps` in beads metadata to correlate task work with SAPs
- Example:
  ```json
  // Coordination request
  {
    "request_id": "COORD-2025-010",
    "relationships": {
      "spawns_tasks": ["chora-base-sap015-abc", "chora-base-sap015-def"]
    }
  }

  // Beads task metadata
  {
    "metadata": {
      "coord_request": "COORD-2025-010",
      "affects_saps": ["SAP-015"]
    }
  }
  ```

**SAP-000 (SAP Framework)**:
- Use `affects_saps` to track which SAPs are enhanced/modified
- Use `affects_domains` to understand scope of SAP work
- Correlate coordination requests with SAP adoption phases

**SAP-009 (Agent Awareness)**:
- Tag `affects_domains` with awareness file paths
- Track AGENTS.md/CLAUDE.md updates via coordination
- Enable awareness file graph navigation

**SAP-010 (A-MEM)**:
- Emit events with `coord_request` field for correlation
- Use `affects_saps` tags for event categorization
- Build event graphs linking coordination → implementation → completion

### 7.3 Migration Guidance

**For Existing Coordination Requests**:

New fields are **optional** - existing coordination requests remain valid. To enhance existing requests:

```bash
# Add relationships to existing coordination request
jq '. + {
  "relationships": {
    "blocks": [],
    "blocked_by": [],
    "related_to": [],
    "spawns_tasks": [],
    "supersedes": null,
    "superseded_by": null
  },
  "affects_saps": ["SAP-001"],
  "affects_domains": ["docs/skilled-awareness/inbox"]
}' inbox/active/COORD-2025-010.json > temp.json && mv temp.json inbox/active/COORD-2025-010.json
```

**For New Coordination Requests**:

Generators should include these fields by default:
- `scripts/generate-coordination-request.py` updated to include relationship fields
- Content blocks added for `affects_saps` and `affects_domains`
- Default to empty arrays/null for relationships

**Validation**:

Schema validation remains backward-compatible:
```bash
# Validate enhanced coordination request
python -m jsonschema -i inbox/active/COORD-2025-010.json schemas/coordination-request.json
```

---

## 8. Reference Materials
- **Schemas:**
  - `schemas/coordination-request.json` (v1.1.1+ with relationship metadata)
  - `schemas/implementation-task.json`
  - `schemas/strategic-proposal.json`
- **Examples:**
  - `inbox/completed/` records for retrospectives
  - `inbox/incoming/coordination/COORD-2025-*` (live coordination requests)
- **Related Protocols:**
  - Evidence-Based Development Workflow (DDD/BDD/TDD)
  - Memory system protocols (for event capture)
  - Future Status Protocol (planning)

---

## 9. Opinionated Tooling & Reference Implementation

**Philosophy**: While the protocol itself remains tool-agnostic (pure Git + JSON/JSONL), this section documents the **recommended reference implementation** that provides excellent developer experience and AI agent ergonomics.

### 9.1 Reference Implementation Components

**Core Tooling Stack**:
- **Generator**: `scripts/generate-coordination-request.py` - AI-powered coordination request creation
- **Installer**: `scripts/install-inbox-protocol.py` - One-command ecosystem onboarding
- **Query Interface**: `scripts/inbox-query.py` - Agent-friendly inbox management
- **Response Tool**: `scripts/respond-to-coordination.py` - Structured response generation

**Design Principles**:
1. **Batteries Included** - All tools ship with protocol, zero configuration required
2. **AI-First Design** - CLI optimized for LLM agent invocation (clear commands, structured output)
3. **Excellent DX** - 5-minute onboarding, one command per action
4. **Ecosystem Scale** - Tools work identically across all adopting repositories

### 9.2 Installation

**One-Command Setup**:
```bash
# Full installation (recommended for ecosystem adoption)
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/YOUR-REPO \
  --mode full \
  --verbose

# Minimal installation (protocol only, no generation tools)
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/YOUR-REPO \
  --mode minimal
```

**What Gets Installed**:
- Directory structure (`incoming/`, `active/`, `completed/`, `ecosystem/`, `coordination/`)
- Content generator with 14 content blocks and 4 generation patterns
- Capability registry template (auto-filled with repo name)
- Agent automation playbook (`inbox/AGENTS.md`)
- Event log initialization
- Ecosystem registration placeholder

**Time to Onboard**: <5 minutes for full setup

### 9.3 Generator Architecture

**Four Generation Patterns**:

1. **Literal** - Hardcoded values (e.g., `type: "coordination"`)
2. **User Input** - Extract from user context with intelligent key matching
3. **Template** - Jinja2 rendering for dynamic content
4. **AI Augmented** - Claude Sonnet 4.5 generation (deliverables, acceptance criteria)

**Usage**:
```bash
# Create context file
cat > context.json <<EOF
{
  "title": "Update Documentation for SAP-019",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-workspace",
  "priority": "P2",
  "urgency": "next_sprint",
  "background": "SAP-019 released but docs incomplete...",
  "rationale": "Complete docs enable adoption..."
}
EOF

# Generate with full pipeline (schema validation + ID allocation + event emission)
python scripts/generate-coordination-request.py \
  --context context.json \
  --post-process \
  --verbose
```

**Output**: Schema-validated coordination request in `inbox/incoming/coordination/COORD-YYYY-NNN.json`

**Performance**: 10-15 seconds, ~$0.02-0.05 per request (Claude Sonnet 4.5)

### 9.4 Agent Automation

**Inbox Monitoring Workflow**:
```bash
# 1. Check for new items (run at session start)
python scripts/inbox-query.py --incoming --unacknowledged

# 2. View specific request
python scripts/inbox-query.py --request COORD-2025-006

# 3. Respond to coordination
python scripts/respond-to-coordination.py \
  --request COORD-2025-006 \
  --status accepted \
  --notes "Starting implementation, ETA 3 days"

# 4. Update status
python scripts/update-coordination-status.py \
  --request COORD-2025-006 \
  --status in_progress
```

**Agent Responsibilities** (documented in `inbox/AGENTS.md`):
- Check inbox at every session start
- Acknowledge items within SLA (see Section 9)
- Escalate blockers immediately
- Emit events for all state transitions

### 9.5 Discovery & Addressing

**Capability Registry** (`inbox/coordination/CAPABILITIES_<repo>.yaml`):
```yaml
repository:
  name: mcp-orchestration
  github_url: github.com/liminalcommons/mcp-orchestration

capabilities:
  can_provide:
    - mcp_server_hosting
    - service_orchestration
  can_receive:
    - coordination_requests
    - tasks

contacts:
  primary: team@example.com

status:
  active: true
  health: healthy
```

**Addressing Format**:
```json
{
  "to_repo": "github.com/liminalcommons/mcp-orchestration",
  "priority": "P1",
  "urgency": "blocks_sprint"
}
```

**Discovery** (manual in v1.1, automated registry planned for v1.2):
- Check `inbox/coordination/ECOSYSTEM_STATUS.yaml` for active repositories
- Query capability registry files to find providers
- Future: `python scripts/discover-repos.py --capability mcp_server_hosting`

### 9.6 Ecosystem Dashboard

**Status Tracking** (`inbox/coordination/ECOSYSTEM_STATUS.yaml`):
- Updated weekly (every Sunday)
- Shows: Repository status, active work, blockers, health metrics
- Distributed via weekly broadcasts

**Event Correlation** (`inbox/coordination/events.jsonl`):
- Append-only log of all coordination events
- Trace IDs link related work across repos (format: `kebab-case-name-YYYY`)
- Example: W3 Health Monitoring traced 47 events across 4 repos

### 9.7 Customization & Extension

**Adding Custom Content Blocks**:
1. Create `inbox/content-blocks/content-block-YOUR_FIELD.json`
2. Choose generation pattern (literal, user_input, template_fill, ai_augmented)
3. Add to `coordination-request-artifact.json` children array
4. Regenerate requests with new field

**Custom AI Prompts**:
- Edit `prompt_template` in content block configs
- Use Jinja2 conditionals: `{% if field %}{{field}}{% endif %}`
- Specify output format clearly (JSON array, string, etc.)
- Include examples and constraints in prompt

**Integration Points**:
- Post-processing: Hook into `scripts/process-generated-artifact.py`
- Event handlers: Subscribe to `events.jsonl` for notifications
- Custom validators: Add to schema validation pipeline

---

## 10. Service Level Agreements (SLAs)

**Formalized Response Commitments**:

### 10.1 Acknowledgment SLA

**All repositories adopting SAP-001 commit to**:
- **Acknowledgment Time**: Within **1 business day** of coordination item arrival
- **Acknowledgment Content**: Confirmation of receipt + initial feasibility assessment
- **Mechanism**: Move item to `active/` or respond via `scripts/respond-to-coordination.py`

**Escalation**:
- If no acknowledgment within 1 business day → Escalate to GitHub issues
- If no acknowledgment within 3 business days → Escalate to ecosystem coordinator

### 10.2 Full Response SLA (Urgency-Based)

| Urgency | Full Response Time | Definition |
|---------|-------------------|------------|
| `blocks_sprint` | Same business day | Blocking current sprint work; immediate action required |
| `next_sprint` | 3 business days | Needed for next sprint planning; prioritized review |
| `backlog` | 1 week | Non-urgent; queued for future consideration |

**Full Response Includes**:
- Accept/decline decision with justification
- Effort estimate (if accepted)
- Timeline/milestones (if applicable)
- Dependencies identified

### 10.3 Status Update Cadence

**For Active Coordination** (`inbox/active/`):
- **Progress Updates**: Weekly (every Monday)
- **Blocker Escalation**: Immediate (same day as blocker identified)
- **Completion Notification**: Within 1 day of work completion

**Update Mechanism**:
```bash
python scripts/update-coordination-status.py \
  --request COORD-2025-006 \
  --status in_progress \
  --notes "Completed phase 1, starting phase 2. ETA: 4 days"
```

### 10.4 Ecosystem Participation SLA

**Weekly Broadcasts** (published every Sunday):
- Review ecosystem status dashboard
- Respond to broadcast questions within 2 business days
- Update capability registry if capabilities change

**Quarterly Reviews**:
- Assess protocol effectiveness
- Provide adoption feedback
- Propose improvements via strategic proposals

### 10.5 SLA Monitoring & Enforcement

**Automated Tracking**:
- `inbox/coordination/events.jsonl` timestamps all acknowledgments
- Ecosystem dashboard shows response time metrics
- Overdue items flagged in weekly broadcasts

**Non-Compliance Handling**:
1. **First Violation**: Reminder notification (automated)
2. **Repeated Violations**: Escalation to repository maintainers
3. **Persistent Non-Compliance**: Mark repository as "degraded" in ecosystem status
4. **Extended Unavailability**: Move to "maintenance mode" (paused coordination)

**Exceptions**:
- Holidays and planned maintenance windows (communicated via capability registry)
- Force majeure events (documented in event log)
- Transition periods during onboarding (30-day grace period)

---

## 11. Adoption Strategy & Rollout

### 11.1 Current Adoption Status (as of 2025-11-02)

**Production Deployments**:
- ✅ **chora-base** - 4 sprints of proven usage (70% acceptance rate, 82-142% ROI)
- ✅ **chora-workspace** - Ecosystem coordination hub (active)

**Invitations Sent** (responses due 2025-11-14):
- ecosystem-manifest (standards authority)
- mcp-orchestration (service layer)
- mcp-gateway (interface layer)

**Participation Options Offered**:
1. **Full Onboarding** (45 min setup + 10 min/week)
2. **Capability Registration Only** (15 min one-time)
3. **Observer Mode** (0 min commitment, receive broadcasts)
4. **Decline** (no participation)

### 11.2 Phased Rollout Plan

**Phase 1: Foundation (Nov 2025 - Completed)**
- ✅ SAP-001 v1.0.0 published
- ✅ Internal adoption (chora-base, chora-workspace)
- ✅ Proven effectiveness (94.9% quality, 70% acceptance)

**Phase 2: Tooling (Nov 2025 - In Progress)**
- ✅ Opinionated tooling layer (v1.1.0)
- ✅ One-command installer
- ✅ AI-powered generator
- ⏳ Agent automation playbooks
- ⏳ Ecosystem onboarding of first 3-5 repos

**Phase 3: Discovery (Q1 2026 - Planned)**
- ⏳ Centralized service registry
- ⏳ Automated discovery tools
- ⏳ Real-time ecosystem dashboard
- ⏳ Webhook/notification automation

**Phase 4: Scale (Q2 2026 - Planned)**
- ⏳ 10-20 repository adoption
- ⏳ Cross-organizational coordination patterns
- ⏳ Advanced routing and load balancing
- ⏳ Governance formalization

### 11.3 Ecosystem Invitation Process

**For Repository Maintainers**:
1. Receive invitation email/coordination request
2. Review SAP-001 protocol specification
3. Choose participation level (full/registration/observer/decline)
4. If full: Run `install-inbox-protocol.py --interactive`
5. Review and customize capability registry
6. Submit ecosystem registration PR to chora-base
7. Receive first coordination request within 1 week

**For AI Agents**:
1. Read `inbox/AGENTS.md` playbook
2. Add inbox monitoring to session startup routine
3. Learn CLI commands for common workflows
4. Practice with test coordination request
5. Begin monitoring `inbox/incoming/coordination/`

### 11.4 Success Metrics

**Adoption Metrics**:
- **Target**: ≥5 repositories by end of November 2025
- **Target**: ≥10 repositories by Q1 2026
- **Measurement**: Active repos with ≥1 coordination item processed/month

**Quality Metrics**:
- **Acceptance Rate**: ≥70% (coordination requests accepted)
- **Response Time**: ≥90% acknowledgments within SLA
- **Completion Rate**: ≥80% of accepted items completed within estimated timeline

**Efficiency Metrics**:
- **Time to Onboard**: <5 minutes (vs 45 minutes manual)
- **Time to Generate Request**: <15 seconds (vs 30-60 minutes manual)
- **Cost per Coordination**: <$0.10 (generator + automation overhead)

---

## 12. Governance & Long-Term Maintenance

### 12.1 Protocol Evolution Process

**Version Control**:
- **Patch releases** (1.1.x): Documentation fixes, schema clarifications
- **Minor releases** (1.x.0): New features, backward-compatible changes
- **Major releases** (x.0.0): Breaking changes, require migration guide

**Change Proposal Process**:
1. Submit strategic proposal to `inbox/ecosystem/proposals/`
2. Quarterly review by ecosystem coordination team
3. Consensus decision (≥70% of active repositories)
4. Migration guide published (for major changes)
5. 30-day transition period before enforcement

### 12.2 Capability Owner Responsibilities

**Primary**: Victor Piper (as of 2025-11-02)
- Quarterly review of protocol effectiveness
- Ecosystem status monitoring
- Breaking tie votes on protocol changes
- Escalation point for SLA violations

**Backup/Succession**:
- Quarterly review to confirm coverage
- Nominate backup capability owner
- Document handoff procedures

### 12.3 Data Handling & Security

**Current Policy** (v1.1.0):
- **Assumption**: Trusted ecosystem of collaborators
- **Data Storage**: All coordination data in Git repositories (public by default)
- **Sensitive Information**: Manual sanitization before commit (no encryption)
- **Audit Trail**: Event logs provide full history

**Future Considerations** (v2.0+ or addendum):
- When collaboration expands beyond trusted circle → Draft data-handling addendum
- Consider: Encryption for sensitive fields, access control, audit requirements
- Regulatory compliance (if needed for specific ecosystems)

### 12.4 Ecosystem Coordination Team

**Composition** (Proposed):
- 1 Capability Owner (Victor Piper)
- 2-3 Repository Representatives (rotating quarterly)
- 1 AI Agent Operations Lead

**Responsibilities**:
- Weekly ecosystem status updates
- Quarterly protocol reviews
- Conflict resolution
- Adoption support

**Meetings**:
- **Weekly**: Async status via ecosystem broadcasts
- **Monthly**: 30-minute sync (optional, as needed)
- **Quarterly**: 90-minute strategic review

---

## 13. Future Enhancements (Roadmap)

### 13.1 Planned for v1.2 (Q1 2026)

**Discovery & Registry**:
- Centralized service registry (`inbox/ecosystem/REGISTRY.json`)
- Discovery CLI: `python scripts/discover-repos.py --capability X`
- Auto-registration on installer run

**Monitoring & Automation**:
- Inbox monitoring daemon: `python scripts/inbox-monitor.py`
- Webhook notifications (Slack, email, GitHub issues)
- Auto-acknowledgment with "received, reviewing" response

**Dashboard Improvements**:
- HTML/JSON ecosystem dashboard (real-time updates)
- Health metrics visualization
- Blocker tracking and alerts

### 13.2 Considered for v2.0 (Q2 2026+)

**Advanced Routing**:
- Multi-recipient coordination with delivery modes (all/any/round_robin)
- Role-based addressing (service_owner, maintainer, reviewer)
- Smart routing with capability-based fallbacks

**Integration Layer**:
- MCP server integration (chora-compose collaboration)
- GitHub Actions workflows for automation
- API endpoints for programmatic access

**Status Protocol Migration**:
- Unified status tracking across multiple coordination protocols
- Cross-protocol event correlation
- Federated ecosystem coordination

### 13.3 Open Questions for Community Input

1. **Should discovery be centralized or federated?**
   - Option A: Central registry in chora-base (simple, single point of failure)
   - Option B: Distributed DHT-style discovery (complex, resilient)

2. **How should we handle multi-organizational coordination?**
   - Access control requirements?
   - Cross-boundary security model?
   - Compliance frameworks needed?

3. **What level of automation is appropriate?**
   - Fully autonomous agents (auto-accept low-risk items)?
   - Human-in-the-loop for all decisions?
   - Risk-based thresholds?

4. **Should we standardize on MCP or remain protocol-agnostic?**
   - Benefit: Tighter integration with Claude Desktop
   - Risk: Lock-in to specific tooling

---

## Appendix A: Changelog

### v1.2.0 (2025-11-11)

**Added**:
- Section 15: Light+ Planning Framework Integration
  - Coordination requests as intentions (Evidence Level A/B/C)
  - Wave assignment criteria (Wave 1/Wave 2)
  - Schema enhancements (light_plus_metadata object)
  - Query patterns for retrospectives
  - Integration workflows and operational patterns

**Changed**:
- Updated version from 1.1.0 to 1.2.0
- Status changed from "Active (ecosystem adoption phase)" to "Active (Level 3 - Production)"
- Fixed section numbering (13.6 → 14.6, 13.7 → 14.7)

**Rationale**:
- Light+ integration connects coordination requests to strategic planning
- Evidence-based intention categorization enables data-driven roadmap decisions
- Wave assignment provides transparency for ecosystem partners
- Traceability from COORD → intention → Wave → shipped enables lead time metrics
- Level 3 status reflects production-ready state with 60x ROI

---

### v1.1.0 (2025-11-02)

**Added**:
- Section 8: Opinionated Tooling & Reference Implementation
- Section 9: Service Level Agreements (SLAs)
- Section 10: Adoption Strategy & Rollout
- Section 11: Governance & Long-Term Maintenance
- Section 12: Future Enhancements (Roadmap)
- Section 14: CHORA_TRACE_ID Propagation Protocol (GAP-001 resolution)
- Appendix A: Changelog

**Changed**:
- Updated version from 1.0.0 to 1.1.0
- Status changed from "Draft" to "Active (ecosystem adoption phase)"

**Rationale**:
- Opinionated tooling enables seamless ecosystem adoption
- Formalized SLAs provide clear response expectations
- Governance structure ensures long-term protocol health
- Roadmap transparency helps adopters plan integration
- End-to-end traceability enables lead time metrics and retrospectives

---

## 14. CHORA_TRACE_ID Propagation Protocol

**Purpose**: Enable end-to-end traceability from coordination request → documentation → implementation → metrics → retrospectives.

**Problem Statement** (GAP-001):
- CHORA_TRACE_ID emitted by SAP-001 but not propagated to downstream SAPs (SAP-007 docs, SAP-013 metrics, SAP-004 tests, SAP-011 Docker, SAP-005 CI)
- Manual handoffs lose context, preventing "lead time" analysis (idea → production)
- Retrospectives require manual correlation across artifacts

**Solution**: Standardized trace propagation protocol across 5 SAP touchpoints.

### 14.1 Trace ID Format

**Standard Format**: `{domain}-{yyyy}-{nnn}`

**Examples**:
- `mcp-taskmgr-2025-003` - MCP server for task management, 3rd request in 2025
- `chora-base-2025-042` - chora-base improvement, 42nd request in 2025
- `sap-synergy-2025-001` - SAP synergy work, 1st request in 2025

**Components**:
- `{domain}`: Project/feature domain (lowercase, hyphenated)
- `{yyyy}`: 4-digit year
- `{nnn}`: 3-digit sequential number (zero-padded)

### 14.2 Propagation Workflow

**Step 1: Coordination Request Creation** (SAP-001)
```json
{
  "trace_id": "mcp-taskmgr-2025-003",
  "title": "Create task management MCP server",
  "type": "coordination_request",
  "status": "active",
  "created": "2025-11-03T10:00:00Z"
}
```

**Step 2: Documentation** (SAP-007)
```bash
# Auto-propagate trace_id to documentation frontmatter
./scripts/propagate-trace-id.sh mcp-taskmgr-2025-003 docs/user-docs/how-to/create-task.md
```

Result:
```yaml
---
title: How to Create Tasks
type: how-to
status: current
audience: all
last_updated: 2025-11-03
trace_id: mcp-taskmgr-2025-003
---
```

**Step 3: Metrics Tracking** (SAP-013)
```python
metric = ClaudeMetric(
    session_id="session-456",
    timestamp=datetime.now(),
    task_type="feature_implementation",
    lines_generated=250,
    time_saved_minutes=120,
    trace_id="mcp-taskmgr-2025-003",  # Propagated from coordination
    ...
)
calculator.add_metric(metric)
```

**Step 4: Commit Messages** (Best Practice)
```bash
git commit -m "feat: implement task creation endpoint [trace: mcp-taskmgr-2025-003]"
```

**Step 5: CI/CD Logs** (SAP-005)
```yaml
# .github/workflows/ci.yml
- name: Run tests
  env:
    CHORA_TRACE_ID: ${{ github.event.inputs.trace_id || 'ci-auto' }}
  run: pytest --trace-id="$CHORA_TRACE_ID"
```

### 14.3 Trace Propagation Tools

**Script: `scripts/propagate-trace-id.sh`**

Automatically adds trace_id to documentation frontmatter:
```bash
./scripts/propagate-trace-id.sh <trace_id> <doc_file>
```

**Features**:
- Validates trace_id format
- Inserts trace_id into YAML frontmatter after `last_updated`
- Creates backup before modification
- Provides guidance on next steps (metrics, commits, CI)

**Example**:
```bash
./scripts/propagate-trace-id.sh mcp-taskmgr-2025-003 docs/user-docs/tutorials/01-first-task.md
# SUCCESS: Added trace_id to docs/user-docs/tutorials/01-first-task.md
# Next steps for end-to-end traceability:
#   1. Add trace_id to SAP-013 metrics when tracking this work
#   2. Reference trace_id in commit messages
#   3. Query metrics by trace_id for lead time analysis
```

### 14.4 Lead Time Analysis

**Query Metrics by Trace ID**:
```bash
# Find all metrics for a trace_id
grep 'mcp-taskmgr-2025-003' metrics/*.csv

# Calculate lead time (coordination → production)
./scripts/calculate-lead-time.sh mcp-taskmgr-2025-003
# Result: 14 days (from coordination request to deployment)
```

**Benefits**:
- Identify bottlenecks in workflow
- Measure time savings by development phase
- Retrospectives with complete context
- Evidence-based process improvements

### 14.5 Adoption Guidance

**For Repository Maintainers**:
1. Add `trace_id` field to SAP-007 documentation frontmatter schema (optional)
2. Add `trace_id` parameter to SAP-013 ClaudeMetric class (optional)
3. Install `scripts/propagate-trace-id.sh` utility
4. Document trace propagation in SAP-001 adoption-blueprint
5. Train team on trace_id format and commit message conventions

**For AI Agents**:
1. Extract `trace_id` from coordination requests (SAP-001)
2. Pass `trace_id` to documentation generation (SAP-007)
3. Include `trace_id` in metrics tracking (SAP-013)
4. Reference `trace_id` in commit messages
5. Query metrics by `trace_id` for retrospectives

**Compatibility**: Trace propagation is **optional** - repos can adopt incrementally without breaking existing workflows.

### 14.6 Related Documents

- [Workflow Continuity Gap Report](../../../project-docs/workflow-continuity-gap-report.md) - GAP-001 details
- [Context Flow Diagram](../../../project-docs/context-flow-diagram.md) - CHORA_TRACE_ID flow visualization
- [SAP-007 Documentation Framework](../documentation-framework/protocol-spec.md) - Frontmatter schema
- [SAP-013 Metrics Tracking](../metrics-tracking/protocol-spec.md) - ClaudeMetric class

---

### 14.7 Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/inbox/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Overview / Quick Start for Claude
- [ ] User Signal Patterns / Common Workflows (AGENTS.md has pattern tables, CLAUDE.md has 3 workflows)
- [ ] Best Practices / Claude-Specific Tips (5 each)
- [ ] Common Pitfalls (5 each)
- [ ] Integration / Support & Resources

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/inbox/AGENTS.md && \
test -f docs/skilled-awareness/inbox/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/inbox/CLAUDE.md | grep "progressive_loading:"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-001
```

**Expected Workflow Coverage**:
- AGENTS.md: User signal pattern tables (Inbox Operations, Coordination Requests, Ecosystem Status)
- CLAUDE.md: 3 Claude Code workflows (Show Status with Read, Create Request with Write/Bash, Triage with Edit)
- Rationale: AGENTS.md uses pattern tables for intent translation, CLAUDE.md focuses on Read/Write/Edit/Bash tool patterns

---

## 15. Light+ Planning Framework Integration

**Purpose**: Document how SAP-001 coordination requests feed into SAP-012 Light+ strategic planning framework, enabling coordination-driven product development.

### 15.1 Overview

The **Light+ framework** (SAP-012) is a 4-level planning construct hierarchy that defines **WHAT** we build, while the 8-phase lifecycle defines **HOW**. SAP-001 coordination requests serve as a primary input source for strategic planning in Phase 1.1 Discovery.

**Light+ Planning Levels**:
1. **Strategy** (Quarterly) - ROADMAP.md, vision statements, strategic themes
2. **Releases** (Sprint-based) - Sprint planning, version milestones, velocity tracking
3. **Features** (Per feature) - DDD/BDD/TDD workflow, feature specifications
4. **Tasks** (Daily) - Beads task tracking (SAP-015), 2-8 hour chunks

**Integration Point**: Coordination requests from `inbox/coordination/active.jsonl` are analyzed during **Phase 1.1 Discovery** to populate the intention inventory, which drives strategic theme development.

---

### 15.2 Coordination Requests as Intentions

**Definition**: An **intention** is a user need or strategic opportunity that may become part of the product roadmap. Coordination requests represent formalized intentions from ecosystem partners.

**Phase 1.1 Discovery Workflow**:
```bash
# 1. Read active coordination requests
cat inbox/coordination/active.jsonl

# 2. For each COORD, extract intention characteristics:
#    - User need (from description, context)
#    - Evidence level (from source, priority, urgency)
#    - Effort estimate (from estimated_effort field)
#    - User demand (from requesting_repo, affected domains)

# 3. Add to intention inventory
echo '{
  "intention_id": "INT-2025-001",
  "source": "COORD-2025-003",
  "description": "Update SAP-019 verification documentation",
  "evidence_level": "A",
  "user_demand": 8,
  "effort_hours": 12
}' >> .chora/planning/intentions/2025-Q4.jsonl
```

**Evidence Level Mapping**:

| COORD Characteristics | Evidence Level | Wave Assignment |
|----------------------|----------------|-----------------|
| P0/P1 priority + urgent + external partner | **Level A** (Direct feedback) | Wave 1 candidate |
| P1/P2 priority + next_sprint + team request | **Level B** (Inferred need) | Wave 1 or 2 |
| P2/P3 priority + backlog + internal improvement | **Level C** (Hypothetical) | Wave 2 candidate |

---

### 15.3 Evidence Level Categorization

**Level A: Direct User Feedback** (Coordination from external partners):
- Coordination requests from ecosystem repos (ecosystem-manifest, mcp-orchestration)
- High urgency (`blocks_sprint` or `next_sprint`)
- Clear user impact documented in `context.rationale`
- **Example**: `COORD-2025-006` (ecosystem-manifest requesting SAP-019 update)

**Level B: Inferred User Need** (Internal coordination):
- Coordination requests from chora-base internal teams
- Medium priority (P1-P2)
- Supports documented user workflows
- **Example**: `COORD-2025-003` (chora-workspace requesting documentation improvements)

**Level C: Hypothetical** (Strategic improvements):
- Coordination requests for technical debt, refactoring
- Low priority (P3) or deferred
- No direct user request, but supports long-term goals
- **Example**: `COORD-2025-012` (internal refactoring for performance optimization)

---

### 15.4 Coordination Schema Enhancements for Light+

**New Optional Fields** (v1.2.0+):

```json
{
  "request_id": "COORD-2025-010",
  "title": "Add React state management SAP",
  "priority": "P1",
  "urgency": "next_sprint",

  // Light+ integration metadata (optional)
  "light_plus_metadata": {
    "intention_id": "INT-2025-005",
    "evidence_level": "A",
    "user_demand_score": 12,
    "effort_estimate_hours": 24,
    "vision_wave_assignment": 1,
    "assigned_to_roadmap": "2025-Q4",
    "status": "in_wave_1"
  },

  // Existing relationship metadata
  "relationships": {
    "spawns_tasks": ["chora-base-react-state-001"],
    "blocks": [],
    "blocked_by": []
  }
}
```

**Field Definitions**:
- `intention_id`: Link to intention inventory entry
- `evidence_level`: A/B/C categorization (derived from COORD characteristics)
- `user_demand_score`: Calculated from requesting_repo count, affected_domains, affected_saps
- `effort_estimate_hours`: Mapped from COORD `estimated_effort` field
- `vision_wave_assignment`: 1 (Q4), 2 (Q1), or null (not assigned)
- `assigned_to_roadmap`: Quarter assigned (2025-Q4, 2026-Q1)
- `status`: Tracking through Light+ phases (discovery, analysis, wave_1, wave_2, backlog)

---

### 15.5 Wave Assignment Criteria

**Wave 1 Criteria** (High Priority Intentions):
- Evidence Level A+B ≥ 70% of total intentions
- User demand score ≥ 10 (ecosystem-wide need)
- Effort estimate < 50 hours per intention
- Alignment with strategic themes (e.g., "SAP ecosystem maturity")

**Wave 2 Criteria** (Deferred or Validation-Needed):
- Evidence Level C or low user demand (<5)
- Effort estimate > 50 hours (epic-sized)
- Requires pilot validation (via SAP-027 dogfooding)
- Strategic "bet" on future direction

**Example Wave Assignment**:
```
COORD-2025-003: Evidence A, demand 12, effort 18h → Wave 1
COORD-2025-007: Evidence B, demand 8, effort 32h → Wave 1
COORD-2025-012: Evidence C, demand 3, effort 60h → Wave 2 (pilot first)
```

---

### 15.6 Query Patterns for Retrospectives

**Find all COORDs that became Wave 1 intentions**:
```bash
jq 'select(.light_plus_metadata.vision_wave_assignment == 1)' inbox/coordination/*.json
```

**Calculate lead time (COORD created → shipped)**:
```bash
# 1. Find COORD creation date
created=$(jq -r '.created' inbox/coordination/COORD-2025-003.json)

# 2. Find shipped date (from A-MEM events or git tags)
shipped=$(git log --grep="COORD-2025-003" --date=short --format="%ad" | head -1)

# 3. Calculate days
echo "Lead time: $(( ($(date -d "$shipped" +%s) - $(date -d "$created" +%s)) / 86400 )) days"
```

**Find bottlenecks (COORDs stuck in discovery phase)**:
```bash
jq 'select(.light_plus_metadata.status == "discovery" and
    (.created | fromdateiso8601) < (now - 14*86400))' \
    inbox/coordination/*.json
```

---

### 15.7 Integration Workflows

**Workflow 1: COORD Created → Phase 1.1 Discovery**

1. **User creates coordination request** (via `generate-coordination-request.py`)
2. **Inbox triage** (sprint planning): Accept/reject decision, priority assignment
3. **Phase 1.1 Discovery** (quarterly): Read active COORDs, extract intentions
4. **Intention analysis**: Categorize evidence level, calculate user demand
5. **Add to intention inventory**: Create INT entry linked to COORD
6. **Update COORD**: Add `light_plus_metadata.intention_id` field

**Workflow 2: Intention → Wave Assignment → Backlog**

1. **Phase 1.2 Analysis**: Apply Wave 1 criteria to intention inventory
2. **Wave assignment**: Intentions meeting criteria → Wave 1
3. **Phase 1.4 Backlog Cascade**: Create beads epic from Wave 1 intentions
4. **Update COORD**: Set `vision_wave_assignment: 1` and `status: in_wave_1`
5. **Traceability**: Epic metadata includes `from_coord: "COORD-2025-003"`

**Workflow 3: Quarterly Review → COORD Status Update**

1. **Quarterly vision synthesis**: Run Phase 1.1-1.4 workflow
2. **For each COORD**: Update `light_plus_metadata.status` based on wave assignment
3. **Communicate decisions**: Send coordination responses to requesting repos
4. **SLA compliance**: Acknowledge COORD decisions within SLA (48h default)

---

### 15.8 Operational Patterns for AI Agents

**Agent Workflow: Analyze COORDs as Intentions**

```markdown
User: "Run Phase 1.1 Discovery for Q4 2025"

Agent:
1. Read active coordination requests:
   cat inbox/coordination/active.jsonl | jq 'select(.status == "active")'

2. For each COORD, extract:
   - Description → intention description
   - Priority/urgency → evidence level (A/B/C)
   - Requesting_repo + affected_domains → user demand score
   - Estimated_effort → effort hours

3. Create intention inventory entry:
   echo '{
     "intention_id": "INT-2025-NNN",
     "source": "COORD-2025-XXX",
     "evidence_level": "A",
     "user_demand": 12,
     "effort_hours": 24
   }' >> .chora/planning/intentions/2025-Q4.jsonl

4. Update COORD with Light+ metadata:
   jq '.light_plus_metadata.intention_id = "INT-2025-NNN"' \
      inbox/coordination/COORD-2025-XXX.json > tmp.json && \
      mv tmp.json inbox/coordination/COORD-2025-XXX.json
```

**Agent Workflow: Quarterly COORD Status Update**

```markdown
User: "Update COORD status after Wave 1 assignment"

Agent:
1. Read Wave 1 assignments from ROADMAP.md

2. For each intention in Wave 1:
   - Find source COORD via intention_id
   - Update COORD status: active → in_wave_1
   - Set vision_wave_assignment: 1

3. For COORDs not in Wave 1:
   - Update status: active → wave_2_candidate
   - Add rationale: "Deferred to Wave 2 due to capacity constraints"

4. Emit coordination_request_updated events to events.jsonl
```

---

### 15.9 Benefits of Light+ Integration

**For Product Planning**:
- Coordination requests drive strategic planning (evidence-based roadmap)
- Clear prioritization framework (Wave 1 vs Wave 2 criteria)
- Traceability from ecosystem need → shipped feature

**For Ecosystem Partners**:
- Transparency: See how coordination requests become roadmap items
- Predictability: Understand Wave 1 vs Wave 2 assignment criteria
- Accountability: Track lead time from COORD → delivery

**For Retrospectives**:
- Measure lead time (coordination → production)
- Identify bottlenecks (COORDs stuck in discovery phase)
- Calculate % of shipped features sourced from ecosystem coordination
- Evidence-based process improvements

---

### 15.10 Related Documents

- [SAP-012: Development Lifecycle](../development-lifecycle/protocol-spec.md) - Light+ framework specification
- [SAP-015: Task Tracking](../task-tracking/protocol-spec.md) - Beads epic creation from intentions
- [SAP-010: Memory System](../memory-system/protocol-spec.md) - A-MEM event correlation
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/protocol-spec.md) - Wave 2 validation methodology
- [LIGHT_PLUS_REFERENCE.md](../../../docs/dev-docs/LIGHT_PLUS_REFERENCE.md) - Quick reference guide

---

### v1.0.0 (2025-10-25 - Initial Release)

**Initial protocol specification**:
- Core directory structure
- Three intake types (strategic, coordination, implementation)
- Event logging with JSONL
- Git-first coordination model
- Basic capability routing

