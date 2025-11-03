# Ecosystem Onboarding Guide - SAP-001 v1.1

**5-Minute Setup | Opinionated Tooling | Excellent DX**

## Quick Start

### One-Command Installation

```bash
# Full installation (recommended)
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/YOUR-REPO \
  --mode full \
  --verbose

# Takes <5 minutes, installs everything
```

### What You Get

✅ **Complete inbox directory structure**
- `incoming/coordination/` - New coordination requests
- `incoming/tasks/` - Implementation tasks
- `active/` - Work in progress
- `completed/` - Archived items
- `ecosystem/` - Ecosystem coordination
- `coordination/` - Event logs and capabilities

✅ **AI-powered generator** with 4 generation patterns
- Literal values (hardcoded)
- User input extraction
- Template rendering
- AI augmentation (Claude Sonnet 4.5)

✅ **Agent automation playbook** (`inbox/AGENTS.md`)
- Session startup checklist
- CLI command reference
- SLA commitments

✅ **Capability registry** (auto-filled with your repo name)

✅ **Event logging** (append-only JSONL)

---

## What is SAP-001?

**SAP-001 (Cross-Repository Inbox Protocol)** is a Git-native coordination protocol that enables seamless cross-repository collaboration across the Liminal Commons ecosystem.

**Core Benefits**:
- 🚀 **Zero configuration** - One command sets up everything
- 🤖 **AI-first design** - Optimized for LLM agent workflows
- 📊 **Proven effectiveness** - 70% acceptance rate, 82-142% ROI in production
- 🔍 **Full traceability** - Event logs track all coordination history
- 📈 **Ecosystem scale** - Works identically across all repositories

**Read the full spec**: [protocol-spec.md](../skilled-awareness/inbox/protocol-spec.md)

---

## Installation Modes

### Full Mode (Recommended)

**Best for**: Active ecosystem participants
**Time**: <5 minutes
**Includes**: All tools, generator, automation

```bash
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/your-repo \
  --mode full \
  --capabilities "mcp_server_hosting,service_orchestration" \
  --contact "team@example.com" \
  --verbose
```

### Minimal Mode

**Best for**: Protocol-only adoption
**Time**: <2 minutes
**Includes**: Directory structure, schemas, no tooling

```bash
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/your-repo \
  --mode minimal
```

### Generator-Only Mode

**Best for**: Manual inbox management with automated generation
**Time**: <3 minutes
**Includes**: Generator tools only

```bash
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/your-repo \
  --mode generator-only
```

---

## Post-Installation Setup

### 1. Review Capability Registry

Edit your capability registry to describe what your repo provides:

```bash
vim inbox/coordination/CAPABILITIES_your-repo.yaml
```

**Example**:
```yaml
capabilities:
  can_provide:
    - mcp_server_hosting      # MCP servers
    - api_gateway_services    # API gateways
    - data_processing         # ETL pipelines

  can_receive:
    - coordination_requests   # All repos
    - tasks                   # Implementation tasks
    - proposals               # Strategic proposals

contacts:
  primary: team@example.com
  team:
    - alice@example.com
    - bob@example.com

response_sla:
  acknowledgment: "1 business day"
  full_response: "3 business days (next_sprint), same day (blocks_sprint)"
```

### 2. Test the Generator

Create a test coordination request:

```bash
cd your-repo/
python scripts/generate-coordination-request.py --interactive
```

Follow the prompts to generate your first request!

### 3. Configure Agent Automation

Review the agent playbook:

```bash
cat inbox/AGENTS.md
```

**Key agent responsibilities**:
- ✅ Check inbox at session start
- ✅ Acknowledge items within 1 business day
- ✅ Escalate blockers immediately
- ✅ Emit events for all state transitions

### 4. Submit Ecosystem Registration

Create a PR to chora-base adding your capability registry:

```bash
# In chora-base repository
cp ../your-repo/inbox/coordination/CAPABILITIES_your-repo.yaml \
   inbox/coordination/CAPABILITIES_your-repo.yaml

git add inbox/coordination/CAPABILITIES_your-repo.yaml
git commit -m "feat(ecosystem): Register your-repo in ecosystem"
git push origin add-your-repo-capability
```

### 5. Start Monitoring

**Manual approach**:
```bash
# Check for new items
ls -la inbox/incoming/coordination/

# Read specific item
cat inbox/incoming/coordination/COORD-2025-006.json
```

**CLI approach** (recommended):
```bash
# Check for unacknowledged items
python scripts/inbox-query.py --incoming --unacknowledged

# View specific request
python scripts/inbox-query.py --request COORD-2025-006

# Count by status
python scripts/inbox-query.py --count-by-status
```

---

## Daily Workflows

### As a Repository Maintainer

#### Morning Routine (2-3 minutes)
```bash
# 1. Check inbox
python scripts/inbox-query.py --incoming --unacknowledged

# 2. View new requests
python scripts/inbox-query.py --request COORD-2025-XXX

# 3. Respond quickly
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status acknowledged \
  --notes "Reviewing, will respond by EOD"
```

#### Full Response (<10 minutes)
```bash
# Accept request
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status accepted \
  --effort "12-18 hours" \
  --notes "Starting next sprint, ETA 1 week" \
  --move-to-active

# Or decline
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status declined \
  --reason "Resource constraints, suggest deferring to Q2"
```

### As an AI Agent

#### Session Startup Checklist
```bash
# 1. Check inbox (add to session startup routine)
python scripts/inbox-query.py --incoming --unacknowledged

# 2. Acknowledge new items
for item in $(python scripts/inbox-query.py --incoming --unacknowledged --format json | jq -r '.[].id'); do
  python scripts/respond-to-coordination.py \
    --request "$item" \
    --status acknowledged \
    --notes "Received, reviewing requirements"
done

# 3. Check active work
python scripts/inbox-query.py --active

# 4. Escalate blockers
python scripts/inbox-query.py --active --status blocked
```

---

## Creating Coordination Requests

### Using Context Files

```bash
# 1. Create context
cat > context.json <<EOF
{
  "title": "Update Documentation for SAP-019",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-workspace",
  "priority": "P2",
  "urgency": "next_sprint",
  "background": "SAP-019 (Self-Evaluation Framework) released in v4.1.1 but documentation is incomplete. Users need clear examples and usage patterns.",
  "rationale": "Complete documentation enables adoption. Current gap blocks ecosystem onboarding."
}
EOF

# 2. Generate with AI
python scripts/generate-coordination-request.py \
  --context context.json \
  --post-process \
  --verbose
```

**Output**: Fully validated coordination request in `inbox/incoming/coordination/COORD-YYYY-NNN.json`

**Performance**: 10-15 seconds, ~$0.02-0.05 per request

### Interactive Mode

```bash
python scripts/generate-coordination-request.py --interactive
```

Prompts for each field interactively. Perfect for one-off requests!

### Direct CLI Arguments

```bash
python scripts/generate-coordination-request.py \
  --title "Implement Feature X" \
  --to-repo "github.com/liminalcommons/chora-workspace" \
  --priority P1 \
  --urgency blocks_sprint \
  --background "Feature X is required for milestone Y..." \
  --rationale "Evaluated alternatives A, B, C. Chose C because..." \
  --post-process
```

---

## Service Level Agreements (SLAs)

### Response Commitments

| Urgency | Acknowledgment | Full Response | Definition |
|---------|---------------|---------------|------------|
| `blocks_sprint` | 4 hours | Same day | Blocking current sprint work |
| `next_sprint` | 1 business day | 3 business days | Needed for next sprint |
| `backlog` | 1 business day | 1 week | Non-urgent |

**Acknowledgment includes**:
- Confirmation of receipt
- Initial feasibility assessment ("looks feasible", "need to investigate", "resource constrained")

**Full Response includes**:
- Accept/decline decision with justification
- Effort estimate (if accepted)
- Timeline/milestones (if applicable)
- Dependencies identified

### Participation Commitments

**Weekly** (every Sunday):
- Review ecosystem status dashboard
- Respond to broadcast questions within 2 business days
- Update capability registry if capabilities change

**Quarterly**:
- Assess protocol effectiveness
- Provide adoption feedback
- Propose improvements via strategic proposals

---

## Discovery & Addressing

### Finding Who Can Help

**Manual Discovery** (v1.1):
```bash
# Check ecosystem status
cat inbox/coordination/ECOSYSTEM_STATUS.yaml

# Find capabilities
grep -r "can_provide" inbox/coordination/CAPABILITIES_*.yaml
```

**Automated Discovery** (planned v1.2):
```bash
# Who can host MCP servers?
python scripts/discover-repos.py --capability mcp_server_hosting

# Who can receive coordination requests?
python scripts/discover-repos.py --can-receive coordination_requests

# Get contact info
python scripts/discover-repos.py --repo mcp-orchestration --format json
```

### Addressing Format

```json
{
  "to_repo": "github.com/liminalcommons/mcp-orchestration",
  "priority": "P1",
  "urgency": "blocks_sprint"
}
```

**Priority Levels**:
- `P0`: Critical (system down, security issue)
- `P1`: High (blocking work, significant impact)
- `P2`: Normal (standard request)

**Urgency Levels**:
- `blocks_sprint`: Blocking current sprint work → same-day response
- `next_sprint`: Needed for next sprint planning → 3-day response
- `backlog`: Non-urgent → 1-week response

---

## Troubleshooting

### Issue: Installer Fails with Permission Error

**Solution**:
```bash
# Ensure target directory is writable
chmod +w ../your-repo

# Try again with verbose output
python scripts/install-inbox-protocol.py \
  --repo github.com/liminalcommons/your-repo \
  --mode full \
  --verbose
```

### Issue: Generator Returns 404 Model Error

**Solution**: Update AI model ID in:
- `scripts/inbox_generator/generators/ai_augmented.py` (line 27)
- `scripts/generate-coordination-request.py` (line 137)

Current working model: `claude-sonnet-4-5-20250929`

### Issue: Events Not Being Logged

**Solution**:
```bash
# Ensure events file exists
mkdir -p inbox/coordination
touch inbox/coordination/events.jsonl

# Check permissions
chmod 644 inbox/coordination/events.jsonl
```

### Issue: Can't Find Coordination Request

**Solution**:
```bash
# Search all locations
python scripts/inbox-query.py --request COORD-2025-XXX

# If still not found, check if it exists in other repos
cd ../other-repo
python scripts/inbox-query.py --request COORD-2025-XXX
```

---

## Best Practices

### For Repository Maintainers

1. **Check inbox daily** - 2-3 minute morning routine prevents SLA violations
2. **Acknowledge immediately** - Buy time with quick acknowledgment, full response later
3. **Use templates** - Generator creates consistent, high-quality requests
4. **Track in event log** - All state transitions should emit events
5. **Update capability registry** - Keep capabilities current as features evolve

### For AI Agents

1. **Add to startup routine** - Check inbox at every session start
2. **Use CLI tools** - Structured commands better than manual file reading
3. **Emit events** - Log all actions for traceability
4. **Escalate blockers** - Same-day escalation for blocking items
5. **Follow playbook** - `inbox/AGENTS.md` contains full workflow

### For Ecosystem Coordination

1. **Weekly broadcasts** - Keep ecosystem informed (every Sunday)
2. **Quarterly reviews** - Assess protocol effectiveness
3. **Proactive communication** - Don't wait for requests, share status proactively
4. **Celebrate wins** - Share success stories in broadcasts
5. **Iterate continuously** - Propose improvements via strategic proposals

---

## Success Metrics

### Adoption Metrics
- **Target**: ≥5 repositories by end of November 2025
- **Target**: ≥10 repositories by Q1 2026
- **Measurement**: Active repos with ≥1 coordination item processed/month

### Quality Metrics
- **Acceptance Rate**: ≥70% (coordination requests accepted)
- **Response Time**: ≥90% acknowledgments within SLA
- **Completion Rate**: ≥80% of accepted items completed within estimated timeline

### Efficiency Metrics
- **Time to Onboard**: <5 minutes (vs 45 minutes manual)
- **Time to Generate Request**: <15 seconds (vs 30-60 minutes manual)
- **Cost per Coordination**: <$0.10 (generator + automation overhead)

---

## Next Steps

1. **Complete Installation** - Run installer in your repository
2. **Review Capability Registry** - Describe what your repo provides
3. **Test Generator** - Create a test coordination request
4. **Submit Ecosystem Registration** - PR to chora-base
5. **Start Monitoring** - Add inbox checks to daily routine
6. **Join Weekly Broadcasts** - Participate in ecosystem coordination

**Questions?**
- Read full spec: [protocol-spec.md](../skilled-awareness/inbox/protocol-spec.md)
- Review examples: [inbox/incoming/coordination/](../inbox/incoming/coordination/)
- Ask in coordination request: Generate with `--interactive` mode

---

**Version**: 1.1.0
**Last Updated**: 2025-11-02
**Maintained by**: Ecosystem Coordination Team (Victor Piper, capability owner)
