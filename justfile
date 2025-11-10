# justfile for chora-base automation
# https://github.com/casey/just

# Default recipe (show help)
default:
    @just --list

# Generate SAP artifacts from catalog metadata
generate-sap SAP_ID:
    python scripts/generate-sap.py {{SAP_ID}}

# Validate SAP structure (5 artifacts, frontmatter)
validate-sap-structure SAP_PATH:
    python scripts/sap-validate.py {{SAP_PATH}}

# Validate all SAPs in docs/skilled-awareness/
validate-all-saps:
    python scripts/sap-validate.py --all

# Validate SAP maturity with quick check
validate-sap SAP_ID:
    python scripts/sap-evaluator.py --quick {{SAP_ID}}

# Generate and validate SAP in one command
generate-and-validate SAP_ID:
    just generate-sap {{SAP_ID}}
    just validate-sap {{SAP_ID}}

# Generate SAP with dry-run (preview only)
generate-sap-dry-run SAP_ID:
    python scripts/generate-sap.py {{SAP_ID}} --dry-run

# Generate SAP and force overwrite existing files
generate-sap-force SAP_ID:
    python scripts/generate-sap.py {{SAP_ID}} --force

# Validate prerequisites before SAP installation
validate-prerequisites:
    python scripts/validate-prerequisites.py

# Validate internal markdown links
validate-links PATH=".":
    python scripts/validate-links.py {{PATH}}

# Check SAP awareness integration in adoption blueprint
check-sap-awareness SAP_PATH:
    python scripts/check-sap-awareness-integration.py {{SAP_PATH}}

# Rollback template migration (restore from .backup files)
rollback-migration:
    python scripts/rollback-migration.py

# Fix shell syntax in Jinja2 templates (for template projects)
fix-shell-syntax:
    python scripts/fix-shell-syntax.py

# Merge structural updates from chora-base upstream
merge-upstream:
    python scripts/merge-upstream-structure.py

# Merge upstream with dry-run (preview only)
merge-upstream-dry-run:
    python scripts/merge-upstream-structure.py --dry-run

# Bump version (creates git tag and updates CHANGELOG)
bump VERSION:
    python scripts/bump-version.py {{VERSION}}

# Preview version bump without making changes
bump-dry VERSION:
    python scripts/bump-version.py {{VERSION}} --dry-run

# Create GitHub release from current git tag
release:
    python scripts/create-release.py

# Preview GitHub release creation
release-dry:
    python scripts/create-release.py --dry-run

# Create GitHub release for specific version
release-version VERSION:
    python scripts/create-release.py --version {{VERSION}}

# Generate research report for a topic
research topic:
    @echo "📚 Generating research report for: {{topic}}"
    @echo "📄 Using template: docs/templates/research-prompt-template.md"
    @echo "💡 Next steps:"
    @echo "  1. Open docs/templates/research-prompt-template.md"
    @echo "  2. Fill in the {parameters} with your context"
    @echo "  3. Copy the filled prompt to Claude Code or your AI assistant"
    @echo "  4. Execute using WebSearch/WebFetch tools"
    @echo "  5. Save output to docs/research/{{topic}}-research.md"
    @echo ""
    @echo "📂 Output location: docs/research/{{topic}}-research.md"
    @mkdir -p docs/research

# ============================================================================
# SAP-004: Testing Framework (pytest)
# ============================================================================
# Automated testing with pytest, 85%+ coverage, parametrized tests, fixtures.
# See: AGENTS.md "Test Quality Metrics - SAP-004" section, tests/AGENTS.md

# Run all tests with coverage
# Example: just test
test:
    @pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85

# Run unit tests only (fast, <5s)
# Example: just test-unit
test-unit:
    @pytest -m unit -v

# Run integration tests only
# Example: just test-integration
test-integration:
    @pytest -m integration -v

# Run specific test file or pattern
# Example: just test-file tests/test_install_sap.py
test-file FILE:
    @pytest {{FILE}} -v

# Generate HTML coverage report
# Example: just test-coverage-report
test-coverage-report:
    @coverage run -m pytest && coverage html && echo "✅ Coverage report: htmlcov/index.html"

# Run tests with detailed output
# Example: just test-verbose
test-verbose:
    @pytest -vv --tb=short

# ============================================================================
# SAP-005: CI/CD Workflows (GitHub Actions)
# ============================================================================
# Automated testing, linting, security, and release workflows.
# See: .github/workflows/, AGENTS.md "CI/CD Workflows - SAP-005" section

# Show recent CI workflow runs (last 10)
# Example: just ci-status
ci-status:
    @gh run list --limit 10 2>/dev/null || echo "GitHub CLI not installed (run: brew install gh / apt install gh)"

# Show CI logs for specific run
# Example: just ci-logs 12345678
ci-logs RUN_ID:
    @gh run view {{RUN_ID}} --log 2>/dev/null || echo "GitHub CLI not installed or run not found"

# Retry failed CI run
# Example: just ci-retry 12345678
ci-retry RUN_ID:
    @gh run rerun {{RUN_ID}} 2>/dev/null || echo "GitHub CLI not installed or run not found"

# List all CI workflows
# Example: just ci-workflows
ci-workflows:
    @gh workflow list 2>/dev/null || echo "GitHub CLI not installed"

# Show CI workflow details
# Example: just ci-workflow-show test.yml
ci-workflow-show WORKFLOW:
    @gh workflow view {{WORKFLOW}} 2>/dev/null || echo "GitHub CLI not installed or workflow not found"

# Trigger manual workflow run
# Example: just ci-trigger release.yml
ci-trigger WORKFLOW:
    @gh workflow run {{WORKFLOW}} 2>/dev/null || echo "GitHub CLI not installed or workflow not found"

# ============================================================================
# SAP-009: Agent Awareness (Nested AGENTS.md/CLAUDE.md)
# ============================================================================
# Progressive context loading with domain-specific awareness files.
# See: AGENTS.md, CLAUDE.md, docs/skilled-awareness/agent-awareness/

# Validate AGENTS.md structure (7 required sections)
# Example: just validate-awareness-structure AGENTS.md
validate-awareness-structure FILE="AGENTS.md":
    @python scripts/validate-awareness-structure.py {{FILE}} 2>/dev/null || echo "Awareness structure validation not available (SAP-009 not fully installed)"

# Validate awareness link network (check for broken links)
# Example: just validate-awareness-links
validate-awareness-links:
    @python scripts/validate-awareness-links.py 2>/dev/null || echo "Awareness link validation not available (SAP-009 not fully installed)"

# Create domain-specific AGENTS.md from template
# Example: just create-domain-awareness tests
create-domain-awareness DOMAIN:
    @test -f docs/skilled-awareness/templates/AGENTS.md.template && cp docs/skilled-awareness/templates/AGENTS.md.template {{DOMAIN}}/AGENTS.md && echo "✅ Created {{DOMAIN}}/AGENTS.md from template" || echo "❌ Template not found (SAP-009 not fully installed)"

# Show awareness hierarchy (nested files)
# Example: just awareness-hierarchy
awareness-hierarchy:
    @echo "📂 Awareness File Hierarchy"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @find . -name "AGENTS.md" -o -name "CLAUDE.md" 2>/dev/null | grep -v node_modules | sort || echo "No awareness files found"

# List domain-specific awareness files
# Example: just awareness-domains
awareness-domains:
    @echo "📋 Domain-Specific Awareness Files"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "Root:"
    @test -f AGENTS.md && echo "  ✅ AGENTS.md ($(wc -l < AGENTS.md 2>/dev/null || echo 0) lines)" || echo "  ❌ AGENTS.md missing"
    @test -f CLAUDE.md && echo "  ✅ CLAUDE.md ($(wc -l < CLAUDE.md 2>/dev/null || echo 0) lines)" || echo "  ❌ CLAUDE.md missing"
    @echo ""
    @echo "Domain-specific:"
    @find tests scripts .chora docs/skilled-awareness -maxdepth 2 -name "AGENTS.md" -o -name "CLAUDE.md" 2>/dev/null | while read f; do echo "  ✅ $$f"; done || echo "  No domain files found"

# Show awareness statistics
# Example: just awareness-stats
awareness-stats:
    @echo "📊 Awareness System Statistics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "Total AGENTS.md files: $(find . -name 'AGENTS.md' 2>/dev/null | grep -v node_modules | wc -l || echo 0)"
    @echo "Total CLAUDE.md files: $(find . -name 'CLAUDE.md' 2>/dev/null | grep -v node_modules | wc -l || echo 0)"
    @echo "Root AGENTS.md lines: $(wc -l < AGENTS.md 2>/dev/null || echo 0)"
    @echo "Root CLAUDE.md lines: $(wc -l < CLAUDE.md 2>/dev/null || echo 0)"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ============================================================================
# SAP-010: Memory System (A-MEM)
# ============================================================================
# Event logging, knowledge notes, agent profiles for cross-session learning.
# See: .chora/AGENTS.md, .chora/CLAUDE.md

# Show last N memory events (default: 20)
# Example: just memory-events 50
memory-events N="20":
    @tail -n {{N}} .chora/memory/events/*.jsonl 2>/dev/null || echo "No memory events found (memory system may not be installed)"

# Search memory events by keyword
# Example: just memory-events-search "sap_adoption"
memory-events-search QUERY:
    @grep -i "{{QUERY}}" .chora/memory/events/*.jsonl 2>/dev/null || echo "No matching events found"

# List recent N knowledge notes (default: 20)
# Example: just knowledge-list 10
knowledge-list N="20":
    @ls -lt .chora/memory/knowledge/notes/*.md 2>/dev/null | head -n {{N}} || echo "No knowledge notes found"

# Create new knowledge note from template
# Example: just knowledge-note "async-error-handling"
knowledge-note NAME:
    @test -f .chora/memory/knowledge/templates/default.md && cp .chora/memory/knowledge/templates/default.md .chora/memory/knowledge/notes/{{NAME}}.md && echo "✅ Created .chora/memory/knowledge/notes/{{NAME}}.md" || echo "❌ Memory system not installed (no template found)"

# Search knowledge notes by keyword
# Example: just knowledge-search "beads"
knowledge-search QUERY:
    @grep -r -i "{{QUERY}}" .chora/memory/knowledge/notes/ 2>/dev/null || echo "No matching notes found"

# Log a memory event (event_type required)
# Example: just memory-log "learning_captured" '{"pattern":"test-pattern","confidence":0.9}'
memory-log EVENT_TYPE DATA='{}':
    @echo '{"event_type":"{{EVENT_TYPE}}","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","data":{{DATA}}}' >> .chora/memory/events/development.jsonl && echo "✅ Event logged to development.jsonl"

# Validate memory system integrity (JSONL format, schema)
# Checks: JSONL format, event schema, knowledge note structure
memory-health:
    @python scripts/memory-health-check.py 2>/dev/null || echo "Memory health check script not available"

# Show agent profile
# Example: just agent-profile-show "claude-code"
agent-profile-show NAME:
    @cat .chora/memory/profiles/{{NAME}}.yaml 2>/dev/null || echo "Profile '{{NAME}}' not found"

# Show memory system statistics
memory-stats:
    @echo "📊 Memory System Statistics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "Events: $(find .chora/memory/events/ -name '*.jsonl' -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0) total"
    @echo "Knowledge notes: $(find .chora/memory/knowledge/notes/ -name '*.md' 2>/dev/null | wc -l || echo 0)"
    @echo "Agent profiles: $(find .chora/memory/profiles/ -name '*.yaml' 2>/dev/null | wc -l || echo 0)"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ============================================================================
# SAP-015: Task Tracking (Beads)
# ============================================================================
# Persistent task tracking with .beads/ workflow for cross-session context.
# See: AGENTS.md "Task Tracking (Beads) - SAP-015" section

# Show ready tasks (no blockers, not assigned)
# Example: just beads-ready
beads-ready:
    @test -f .beads/issues.jsonl && grep '"status":"open"' .beads/issues.jsonl | grep -v '"blockers":\[' | jq -r '.id + " | " + .title' 2>/dev/null || echo "No beads system found (.beads/issues.jsonl missing)"

# Show all tasks grouped by status
# Example: just beads-status
beads-status:
    @test -f .beads/issues.jsonl && echo "📋 Task Status Summary" && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && echo "Open: $(grep -c '"status":"open"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "In Progress: $(grep -c '"status":"in_progress"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "Blocked: $(grep -c '"status":"blocked"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "Closed: $(grep -c '"status":"closed"' .beads/issues.jsonl 2>/dev/null || echo 0)" || echo "No beads system found"

# Create new task
# Example: just beads-create "Implement feature X"
beads-create TITLE:
    @test -f .beads/issues.jsonl && TASK_ID="task-$(date +%s)" && echo "{\"id\":\"$TASK_ID\",\"title\":\"{{TITLE}}\",\"status\":\"open\",\"created\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> .beads/issues.jsonl && echo "✅ Created task: $TASK_ID" || echo "❌ Beads system not installed"

# Show task details by ID
# Example: just beads-show task-123
beads-show TASK_ID:
    @test -f .beads/issues.jsonl && grep "\"id\":\"{{TASK_ID}}\"" .beads/issues.jsonl | jq '.' || echo "Task {{TASK_ID}} not found"

# List tasks by status
# Example: just beads-list-open
beads-list-open:
    @test -f .beads/issues.jsonl && grep '"status":"open"' .beads/issues.jsonl | jq -r '.id + " | " + .title' || echo "No open tasks"

# List tasks in progress
# Example: just beads-list-in-progress
beads-list-in-progress:
    @test -f .beads/issues.jsonl && grep '"status":"in_progress"' .beads/issues.jsonl | jq -r '.id + " | " + .assignee + " | " + .title' || echo "No tasks in progress"

# List blocked tasks
# Example: just beads-list-blocked
beads-list-blocked:
    @test -f .beads/issues.jsonl && grep '"status":"blocked"' .beads/issues.jsonl | jq -r '.id + " | " + .title + " | Blockers: " + (.blockers | join(", "))' || echo "No blocked tasks"

# List recently closed tasks
# Example: just beads-list-closed
beads-list-closed N="10":
    @test -f .beads/issues.jsonl && grep '"status":"closed"' .beads/issues.jsonl | tail -n {{N}} | jq -r '.id + " | " + .title + " | " + .completion_reason' || echo "No closed tasks"

# Search tasks by keyword
# Example: just beads-search "authentication"
beads-search QUERY:
    @test -f .beads/issues.jsonl && grep -i "{{QUERY}}" .beads/issues.jsonl | jq -r '.id + " | " + .status + " | " + .title' || echo "No tasks matching '{{QUERY}}'"

# Show task statistics
# Example: just beads-stats
beads-stats:
    @test -f .beads/issues.jsonl && echo "📊 Beads Statistics" && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && echo "Total tasks: $(wc -l < .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "Open: $(grep -c '"status":"open"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "In Progress: $(grep -c '"status":"in_progress"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "Blocked: $(grep -c '"status":"blocked"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "Closed: $(grep -c '"status":"closed"' .beads/issues.jsonl 2>/dev/null || echo 0)" && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" || echo "No beads system found"

# ============================================================================
# SAP-001: Inbox Coordination Protocol
# ============================================================================
# Cross-repo coordination with 5 CLI tools, event logging, and formalized SLAs.
# See: AGENTS.md "Inbox Coordination Protocol - SAP-001" section

# Show inbox status (visual terminal output)
# Example: just inbox-status
inbox-status:
    @python scripts/inbox-status.py 2>/dev/null || echo "Inbox protocol not installed (run: python scripts/install-inbox-protocol.py)"

# Query incoming coordination requests
# Example: just inbox-query-incoming
inbox-query-incoming:
    @python scripts/inbox-query.py --incoming --format summary 2>/dev/null || echo "Inbox protocol not installed"

# Query outgoing coordination requests
# Example: just inbox-query-outgoing
inbox-query-outgoing:
    @python scripts/inbox-query.py --outgoing --format summary 2>/dev/null || echo "Inbox protocol not installed"

# Query all coordination requests (JSON output)
# Example: just inbox-query-all
inbox-query-all:
    @python scripts/inbox-query.py --all --format json 2>/dev/null || echo "Inbox protocol not installed"

# Generate new coordination request with AI
# Example: just inbox-generate
inbox-generate:
    @python scripts/generate-coordination-request.py 2>/dev/null || echo "Inbox protocol not installed"

# Respond to coordination request
# Example: just inbox-respond COORD-123 accepted
inbox-respond COORD_ID STATUS:
    @python scripts/respond-to-coordination.py {{COORD_ID}} {{STATUS}} 2>/dev/null || echo "Inbox protocol not installed"

# Show recent coordination events
# Example: just inbox-events 20
inbox-events N="20":
    @tail -n {{N}} inbox/coordination/events.jsonl 2>/dev/null || echo "No coordination events found"

# Search coordination events by keyword
# Example: just inbox-search "SAP-001"
inbox-search QUERY:
    @grep -i "{{QUERY}}" inbox/coordination/*.jsonl 2>/dev/null || echo "No matching coordination items found"
