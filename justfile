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
