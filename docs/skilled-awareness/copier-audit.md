# Copier Reference Audit (2025-10-28)

Purpose: Inventory all remaining mentions of Copier in chora-base so we can retire or reframe them as part of the blueprint + SAP transition.

| Location | Context | Action |
|----------|---------|--------|
| `AGENTS.md` (multiple lines) | Describes Copier as core tech, references `copier.yml`, `copier copy`, `.copier-answers.yml` | ✅ Rewritten for blueprint/SAP workflow |
| `AGENT_SETUP_GUIDE.md:124` | Lists Copier as required dependency | ✅ Updated to reflect blueprint workflow |
| `CLAUDE_SETUP_GUIDE.md:1115` | Mentions copier-based template history | Keep as historical reference or update for clarity |
| `CHANGELOG.md` (numerous entries) | Historical release notes for Copier features | Keep as history but add note about current blueprint workflow |
| `docs/DOCUMENTATION_PLAN.md` | References running `copier update` | ✅ Updated with blueprint maintenance workflow |
| `docs/BENEFITS.md` | Example showing `copier copy` usage | ✅ Updated to blueprint workflow |
| `docs/reference/chora-base/latest-conversation.md` | Transcript mentions Copier | Move to archive or annotate as legacy |
| `static-template/scripts/validate_mcp_names.py:259` | Script still expects `copier.yml` | ✅ References updated to `pyproject.toml` |
| `static-template/.dockerignore` | Ignores Copier files | ✅ Removed copier-specific entries |
| `static-template/user-docs/**` | Numerous instructions referencing Copier commands | ✅ Updated to blueprint/SAP onboarding |
| `docs/reference/chora-compose/**` | Adoption guides rely on `.copier-answers.yml` | Update to SAP adoption or mark as legacy |
| `static-template/user-docs/reference/python-patterns.md` | Uses `{{ _copier_conf.now }}` | ✅ Updated to use blueprint metadata variables |
| `static-template/user-docs/how-to/01-generate-new-mcp-server.md` | Direct Copier instructions | ✅ Rewritten for blueprint workflow |
| `docs/reference/skilled-awareness/chora-base-sap-roadmap.md` | Mentions legacy Copier era | Already acknowledges; ensure plan includes cleanup |
| `docs/releases/**` (historical notes) | Document Copier-era workflows | Treat as legacy; add footnote pointing readers to blueprint process if referenced |

This table will be updated as each reference is addressed. Additional matches were found across other files (see `rg -n "copier"`). Treat this as the master checklist for the transition.
