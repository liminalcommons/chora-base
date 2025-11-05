"""
Awareness File Validation Utility

Validates AGENTS.md and CLAUDE.md files against SAP-009 protocol requirements.
Supports structural validation, content equivalence, and source artifact coverage.

Usage:
    from utils.awareness_validation import AwarenessFileValidator

    validator = AwarenessFileValidator(repo_root=Path.cwd())
    issues = validator.validate_awareness_files("SAP-011")
    for issue in issues:
        print(f"{issue['severity']}: {issue['message']}")
"""

import re
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any


class AwarenessFileValidator:
    """Validate AGENTS.md and CLAUDE.md files against SAP-009 spec"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def extract_yaml_frontmatter(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Extract YAML frontmatter from a markdown file.

        Returns:
            Dict of frontmatter fields, or None if no frontmatter found
        """
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter (--- at start and end)
            if not content.startswith('---\n'):
                return None

            # Find the closing ---
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                # Try alternative ending (--- at end of file)
                end_marker = content.find('\n---', 4)
                if end_marker == -1:
                    return None

            # Extract frontmatter
            frontmatter_text = content[4:end_marker]

            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_text)

            return frontmatter if isinstance(frontmatter, dict) else None

        except Exception:
            return None

    def extract_sections(self, file_path: Path) -> List[str]:
        """
        Extract ## level section headings from markdown file.

        Returns:
            List of section names (without ## prefix)
        """
        if not file_path.exists():
            return []

        sections = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Match ## Section Name (but not ###)
                    match = re.match(r'^##\s+([^#].*)$', line.strip())
                    if match:
                        sections.append(match.group(1).strip())
        except Exception:
            return []

        return sections

    def extract_workflows(self, file_path: Path) -> List[str]:
        """
        Extract ### Workflow headings from markdown file.

        Returns:
            List of workflow names
        """
        if not file_path.exists():
            return []

        workflows = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Match ### Workflow N: Name
                    match = re.match(r'^###\s+Workflow\s+\d+:\s+(.+)$', line.strip())
                    if match:
                        workflows.append(match.group(1).strip())
        except Exception:
            return []

        return workflows

    def count_lines(self, file_path: Path) -> int:
        """Count non-empty lines in file"""
        if not file_path.exists():
            return 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0

    def validate_yaml_frontmatter(
        self,
        file_path: Path,
        required_fields: List[str]
    ) -> List[str]:
        """
        Validate YAML frontmatter has required fields.

        Args:
            file_path: Path to markdown file
            required_fields: List of required field names

        Returns:
            List of validation issues (empty if valid)
        """
        issues = []

        frontmatter = self.extract_yaml_frontmatter(file_path)

        if frontmatter is None:
            issues.append(f"No YAML frontmatter found in {file_path.name}")
            return issues

        # Check required fields
        for field in required_fields:
            if field not in frontmatter:
                issues.append(f"Missing required field '{field}' in {file_path.name} frontmatter")

        # Validate progressive_loading structure if present
        if 'progressive_loading' in frontmatter:
            pl = frontmatter['progressive_loading']
            if not isinstance(pl, dict):
                issues.append(f"progressive_loading should be a dict in {file_path.name}")
            else:
                for phase in ['phase_1', 'phase_2', 'phase_3']:
                    if phase not in pl:
                        issues.append(f"Missing '{phase}' in progressive_loading in {file_path.name}")

        # Validate token estimates if present
        for field in ['phase_1_token_estimate', 'phase_2_token_estimate', 'phase_3_token_estimate']:
            if field in frontmatter:
                if not isinstance(frontmatter[field], int):
                    issues.append(f"'{field}' should be an integer in {file_path.name}")

        return issues

    def check_source_artifact_mentioned(
        self,
        awareness_file: Path,
        source_artifact: Path
    ) -> bool:
        """
        Check if source artifact is mentioned in awareness file.

        This is a simple heuristic: checks if source artifact filename
        appears in awareness file content.

        Returns:
            True if mentioned, False otherwise
        """
        if not awareness_file.exists() or not source_artifact.exists():
            return False

        try:
            with open(awareness_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for source artifact filename
            artifact_name = source_artifact.name
            if artifact_name in content:
                return True

            # Check for references like "capability charter", "protocol spec"
            artifact_refs = {
                "capability-charter.md": ["capability charter", "charter"],
                "protocol-spec.md": ["protocol spec", "protocol"],
                "awareness-guide.md": ["awareness guide", "guide"],
                "adoption-blueprint.md": ["adoption blueprint", "blueprint"],
                "ledger.md": ["ledger"]
            }

            if artifact_name in artifact_refs:
                for ref in artifact_refs[artifact_name]:
                    if ref.lower() in content.lower():
                        return True

            return False

        except Exception:
            return False

    def compare_parallel_coverage(
        self,
        agents_md: Path,
        claude_md: Path
    ) -> Dict[str, Any]:
        """
        Compare workflow/section coverage across AGENTS.md and CLAUDE.md.

        Returns:
            Dict with comparison results:
            - agents_workflows: list of workflow names
            - claude_workflows: list of workflow names
            - workflow_count_diff: percentage difference
            - agents_sections: list of section names
            - claude_sections: list of section names
            - missing_in_claude: sections in AGENTS but not CLAUDE
            - missing_in_agents: sections in CLAUDE but not AGENTS
        """
        agents_workflows = self.extract_workflows(agents_md)
        claude_workflows = self.extract_workflows(claude_md)

        agents_sections = self.extract_sections(agents_md)
        claude_sections = self.extract_sections(claude_md)

        # Calculate workflow count difference
        if len(agents_workflows) > 0:
            workflow_diff = abs(len(claude_workflows) - len(agents_workflows)) / len(agents_workflows)
        else:
            workflow_diff = 1.0 if len(claude_workflows) > 0 else 0.0

        # Find section mismatches (normalize to lower case for comparison)
        agents_sections_lower = {s.lower() for s in agents_sections}
        claude_sections_lower = {s.lower() for s in claude_sections}

        # Core sections that should appear in both
        core_sections = {
            "quick start", "quick start for claude",
            "common workflows", "claude code workflows",
            "best practices", "claude-specific tips",
            "common pitfalls", "troubleshooting"
        }

        missing_in_claude = []
        missing_in_agents = []

        for section in core_sections:
            # Check if concept exists in either file
            agents_has = any(section in s.lower() for s in agents_sections_lower)
            claude_has = any(section in s.lower() for s in claude_sections_lower)

            if agents_has and not claude_has:
                missing_in_claude.append(section)
            elif claude_has and not agents_has:
                missing_in_agents.append(section)

        return {
            "agents_workflows": agents_workflows,
            "claude_workflows": claude_workflows,
            "workflow_count_diff": workflow_diff,
            "agents_sections": agents_sections,
            "claude_sections": claude_sections,
            "missing_in_claude": missing_in_claude,
            "missing_in_agents": missing_in_agents
        }

    def validate_awareness_files(
        self,
        sap_id: str,
        sap_location: str
    ) -> List[Dict[str, str]]:
        """
        Validate AGENTS.md and CLAUDE.md for a SAP.

        Args:
            sap_id: SAP identifier (e.g., "SAP-011")
            sap_location: Relative path to SAP directory (e.g., "docs/skilled-awareness/docker-operations")

        Returns:
            List of validation issues, each with:
            - severity: "error", "warning", "info"
            - category: "presence", "structure", "equivalence", "coverage"
            - message: Human-readable description
        """
        issues = []

        sap_dir = self.repo_root / sap_location
        if not sap_dir.exists():
            issues.append({
                "severity": "error",
                "category": "presence",
                "message": f"SAP directory not found: {sap_location}"
            })
            return issues

        agents_md = sap_dir / "AGENTS.md"
        claude_md = sap_dir / "CLAUDE.md"

        # 1. Presence checks
        if not agents_md.exists():
            issues.append({
                "severity": "error",
                "category": "presence",
                "message": f"{sap_id} missing AGENTS.md"
            })

        if not claude_md.exists():
            issues.append({
                "severity": "error",
                "category": "presence",
                "message": f"{sap_id} missing CLAUDE.md (violates equivalent support requirement)"
            })

        # If either file missing, can't do further validation
        if not agents_md.exists() or not claude_md.exists():
            return issues

        # 2. Structure checks (YAML frontmatter)
        required_fields = ['sap_id', 'version', 'status', 'last_updated', 'type', 'audience']

        agents_frontmatter_issues = self.validate_yaml_frontmatter(agents_md, required_fields)
        for issue in agents_frontmatter_issues:
            issues.append({
                "severity": "warning",
                "category": "structure",
                "message": issue
            })

        claude_frontmatter_issues = self.validate_yaml_frontmatter(claude_md, required_fields)
        for issue in claude_frontmatter_issues:
            issues.append({
                "severity": "warning",
                "category": "structure",
                "message": issue
            })

        # 3. Equivalence checks (parallel coverage)
        comparison = self.compare_parallel_coverage(agents_md, claude_md)

        # Check workflow count equivalence (allow ±30% difference)
        if comparison['workflow_count_diff'] > 0.3:
            issues.append({
                "severity": "warning",
                "category": "equivalence",
                "message": f"{sap_id} workflow count mismatch: AGENTS.md has {len(comparison['agents_workflows'])} workflows, "
                          f"CLAUDE.md has {len(comparison['claude_workflows'])} workflows ({comparison['workflow_count_diff']:.0%} difference)"
            })

        # Check for missing parallel sections
        if comparison['missing_in_claude']:
            issues.append({
                "severity": "warning",
                "category": "equivalence",
                "message": f"{sap_id} CLAUDE.md missing sections present in AGENTS.md: {', '.join(comparison['missing_in_claude'])}"
            })

        if comparison['missing_in_agents']:
            issues.append({
                "severity": "info",
                "category": "equivalence",
                "message": f"{sap_id} AGENTS.md missing sections present in CLAUDE.md: {', '.join(comparison['missing_in_agents'])}"
            })

        # 4. Source artifact coverage checks
        source_artifacts = [
            "capability-charter.md",
            "protocol-spec.md",
            "awareness-guide.md",
            "adoption-blueprint.md",
            "ledger.md"
        ]

        for artifact_name in source_artifacts:
            artifact_path = sap_dir / artifact_name
            if not artifact_path.exists():
                continue  # Skip if source artifact doesn't exist

            agents_mentions = self.check_source_artifact_mentioned(agents_md, artifact_path)
            claude_mentions = self.check_source_artifact_mentioned(claude_md, artifact_path)

            if not agents_mentions and not claude_mentions:
                issues.append({
                    "severity": "info",
                    "category": "coverage",
                    "message": f"{sap_id} {artifact_name} not referenced in either AGENTS.md or CLAUDE.md"
                })
            elif not agents_mentions:
                issues.append({
                    "severity": "info",
                    "category": "coverage",
                    "message": f"{sap_id} {artifact_name} not referenced in AGENTS.md"
                })
            elif not claude_mentions:
                issues.append({
                    "severity": "info",
                    "category": "coverage",
                    "message": f"{sap_id} {artifact_name} not referenced in CLAUDE.md"
                })

        return issues
