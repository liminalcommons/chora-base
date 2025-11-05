# Workflow Diagrams README

Quick reference guide for [workflow-diagrams.md](./workflow-diagrams.md).

---

## Purpose

Visual Mermaid diagrams for 10 core chora-compose Meta workflows, complementing the textual descriptions in [protocol-spec.md §6](./protocol-spec.md#6-workflows).

---

## Quick Access

| Diagram | Purpose | Best For |
|---------|---------|----------|
| [§1 Basic Content Generation](./workflow-diagrams.md#1-basic-content-generation-workflow) | Generate single content piece | Understanding cache resolution, error handling |
| [§2 Artifact Assembly](./workflow-diagrams.md#2-artifact-assembly-workflow) | Assemble multi-piece artifact | Understanding automatic content generation |
| [§3 Collection Generation](./workflow-diagrams.md#3-collection-generation-workflow-3-tier-architecture) | Generate full documentation suite | Understanding 3-tier architecture, context propagation |
| [§4 Interactive Config Creation](./workflow-diagrams.md#4-interactive-config-creation-workflow) | Draft → test → save cycle | Building configs in AI agent sessions |
| [§5 Freshness Validation](./workflow-diagrams.md#5-freshness-validation-workflow-stigmergic-context-links) | Check for stale content | CI/CD integration, maintenance workflows |
| [§6 Error Recovery](./workflow-diagrams.md#6-error-recovery-workflow) | Diagnose and recover from errors | Troubleshooting generation failures |
| [§7 Cache Resolution](./workflow-diagrams.md#7-cache-resolution-workflow) | SHA-256 cache lookup logic | Understanding performance optimization |
| [§8 Context Propagation](./workflow-diagrams.md#8-context-propagation-flow-collection-generation) | MERGE/OVERRIDE/ISOLATE modes | Collection context design |
| [§9 Tool Selection](./workflow-diagrams.md#9-tool-selection-decision-tree) | Choose right MCP tool for task | Agent developers, new users |
| [§10 Parallel vs Sequential](./workflow-diagrams.md#10-parallel-vs-sequential-collection-generation) | Performance comparison | Understanding execution strategies |

---

## Usage

### In GitHub/GitLab
Diagrams render automatically in web view.

### In VS Code
1. Install [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) extension
2. Open `workflow-diagrams.md`
3. Preview: `Cmd+Shift+V` (macOS) or `Ctrl+Shift+V` (Windows/Linux)

### Export to PNG/SVG
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Export all diagrams
mmdc -i workflow-diagrams.md -o workflow-diagrams.pdf

# Export single diagram (extract to temp file first)
mmdc -i single-diagram.mmd -o diagram.png
```

### In Obsidian
Obsidian renders Mermaid diagrams natively. Open `workflow-diagrams.md` in reading view.

---

## Diagram Types

- **Flowcharts**: All workflows (§1-9) use `flowchart TD` (top-down)
- **Gantt Chart**: §10 uses `gantt` for timing comparison
- **Color Coding**:
  - 🟢 Green: Success paths, cache hits
  - 🔴 Red: Error paths, failures
  - 🟡 Yellow: Decision points, cache misses
  - 🟦 Blue: Information/status operations
  - 🟪 Purple: User interaction points

---

## Cross-References

Each workflow in [protocol-spec.md §6](./protocol-spec.md#6-workflows) now links to its corresponding diagram:

- §6.1 Basic Content Generation → [workflow-diagrams.md §1](./workflow-diagrams.md#1-basic-content-generation-workflow)
- §6.2 Artifact Assembly → [workflow-diagrams.md §2](./workflow-diagrams.md#2-artifact-assembly-workflow)
- §6.3 Collection Generation → [workflow-diagrams.md §3](./workflow-diagrams.md#3-collection-generation-workflow-3-tier-architecture)
- §6.4 Conversational Config Lifecycle → [workflow-diagrams.md §4](./workflow-diagrams.md#4-interactive-config-creation-workflow)
- §6.5 Freshness Validation → [workflow-diagrams.md §5](./workflow-diagrams.md#5-freshness-validation-workflow-stigmergic-context-links)

---

## Common Use Cases

### For AI Agents
1. **Tool selection**: Start with [§9 Tool Selection Decision Tree](./workflow-diagrams.md#9-tool-selection-decision-tree)
2. **Error recovery**: Bookmark [§6 Error Recovery](./workflow-diagrams.md#6-error-recovery-workflow) for troubleshooting
3. **Performance optimization**: Review [§7 Cache Resolution](./workflow-diagrams.md#7-cache-resolution-workflow) and [§10 Parallel vs Sequential](./workflow-diagrams.md#10-parallel-vs-sequential-collection-generation)

### For Developers
1. **Understanding architecture**: Start with [§3 Collection Generation](./workflow-diagrams.md#3-collection-generation-workflow-3-tier-architecture) (3-tier model)
2. **Context design**: Review [§8 Context Propagation](./workflow-diagrams.md#8-context-propagation-flow-collection-generation) (MERGE/OVERRIDE/ISOLATE)
3. **Integration**: Check [§1 Basic Content Generation](./workflow-diagrams.md#1-basic-content-generation-workflow) for Python integration patterns

### For Teams
1. **Onboarding**: Walk through [§1-§5](./workflow-diagrams.md#1-basic-content-generation-workflow) in sequence
2. **Training materials**: Export diagrams to PNG for presentations
3. **Documentation**: Embed diagrams in internal wikis/Confluence

---

## Feedback

Found an error or have suggestions?
- File issue: [chora-base Issues](https://github.com/liminalcommons/chora-base/issues)
- Slack: #chora-workspace channel
- Email: Victor (maintainer)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
