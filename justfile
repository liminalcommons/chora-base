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
