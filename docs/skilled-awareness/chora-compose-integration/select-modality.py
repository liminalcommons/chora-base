#!/usr/bin/env python3
"""
Interactive Modality Selector for chora-compose

Helps users choose the right integration modality (pip, MCP, CLI, Docker)
based on their use case, environment, and requirements.

Usage:
    python select-modality.py              # Interactive mode
    python select-modality.py --quick      # Quick mode (fewer questions)
    python select-modality.py --export md  # Export selection as markdown guide
"""

import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Modality(Enum):
    """chora-compose integration modalities."""
    PIP = "pip"
    MCP = "mcp"
    CLI = "cli"
    DOCKER = "docker"


class UserRole(Enum):
    """User role categories."""
    DEVELOPER = "developer"
    AI_AGENT = "ai_agent"
    TEAM = "team"
    DEVOPS = "devops"


@dataclass
class ModalityScore:
    """Scoring for modality recommendation."""
    modality: Modality
    score: int
    reasons: List[str]
    considerations: List[str]


class ModalitySelector:
    """Interactive modality selector."""

    def __init__(self, quick_mode: bool = False):
        self.quick_mode = quick_mode
        self.answers = {}
        self.scores = {
            Modality.PIP: 0,
            Modality.MCP: 0,
            Modality.CLI: 0,
            Modality.DOCKER: 0
        }
        self.reasons = {
            Modality.PIP: [],
            Modality.MCP: [],
            Modality.CLI: [],
            Modality.DOCKER: []
        }

    def run(self) -> ModalityScore:
        """Run interactive questionnaire and return recommendation."""
        print("=" * 70)
        print("chora-compose Modality Selector")
        print("=" * 70)
        print()
        print("This tool will help you choose the right integration modality")
        print("for your use case. Answer a few questions to get a recommendation.")
        print()

        # Question 1: Primary use case
        self._ask_use_case()

        # Question 2: Environment
        self._ask_environment()

        # Question 3: Team size
        if not self.quick_mode:
            self._ask_team()

        # Question 4: Technical constraints
        if not self.quick_mode:
            self._ask_constraints()

        # Calculate scores and return recommendation
        return self._get_recommendation()

    def _ask_use_case(self):
        """Ask about primary use case."""
        print("Question 1: What is your primary use case?")
        print()
        print("  1. AI agent (Claude Desktop/Cursor) generating content")
        print("  2. Python project needing programmatic content generation")
        print("  3. Command-line testing and experimentation")
        print("  4. Team automation (n8n workflows, scheduled generation)")
        print("  5. CI/CD integration for automated builds")
        print()

        choice = self._get_choice(1, 5)

        if choice == 1:
            self.scores[Modality.MCP] += 10
            self.reasons[Modality.MCP].append("AI agent use case (primary MCP scenario)")
            self.answers['use_case'] = 'ai_agent'
        elif choice == 2:
            self.scores[Modality.PIP] += 10
            self.reasons[Modality.PIP].append("Python project integration (library usage)")
            self.answers['use_case'] = 'python_project'
        elif choice == 3:
            self.scores[Modality.CLI] += 10
            self.reasons[Modality.CLI].append("Testing and experimentation (interactive CLI)")
            self.answers['use_case'] = 'testing'
        elif choice == 4:
            self.scores[Modality.DOCKER] += 10
            self.reasons[Modality.DOCKER].append("Team automation (n8n/scheduled workflows)")
            self.answers['use_case'] = 'team_automation'
        elif choice == 5:
            self.scores[Modality.PIP] += 5
            self.scores[Modality.DOCKER] += 5
            self.reasons[Modality.PIP].append("CI/CD integration possible with pip")
            self.reasons[Modality.DOCKER].append("CI/CD integration possible with Docker")
            self.answers['use_case'] = 'ci_cd'

    def _ask_environment(self):
        """Ask about development environment."""
        print()
        print("Question 2: What is your development environment?")
        print()
        print("  1. Python development environment (venv/conda)")
        print("  2. Claude Desktop or AI-enabled IDE (Cursor, VSCode)")
        print("  3. Docker Desktop installed")
        print("  4. CI/CD system (GitHub Actions, GitLab CI)")
        print("  5. No Python installed (CLI/Docker only)")
        print()

        choice = self._get_choice(1, 5)

        if choice == 1:
            self.scores[Modality.PIP] += 5
            self.scores[Modality.CLI] += 3
            self.reasons[Modality.PIP].append("Python environment available")
            self.answers['environment'] = 'python'
        elif choice == 2:
            self.scores[Modality.MCP] += 7
            self.reasons[Modality.MCP].append("AI-enabled IDE (MCP native integration)")
            self.answers['environment'] = 'ai_ide'
        elif choice == 3:
            self.scores[Modality.DOCKER] += 5
            self.scores[Modality.MCP] += 3  # MCP also uses Docker
            self.reasons[Modality.DOCKER].append("Docker Desktop available")
            self.answers['environment'] = 'docker'
        elif choice == 4:
            self.scores[Modality.PIP] += 4
            self.scores[Modality.DOCKER] += 4
            self.reasons[Modality.PIP].append("CI/CD integration via pip")
            self.reasons[Modality.DOCKER].append("CI/CD integration via Docker")
            self.answers['environment'] = 'ci_cd'
        elif choice == 5:
            self.scores[Modality.CLI] += 7
            self.scores[Modality.DOCKER] += 7
            self.reasons[Modality.CLI].append("Standalone CLI (no Python dependency)")
            self.reasons[Modality.DOCKER].append("Docker (no Python dependency)")
            self.answers['environment'] = 'no_python'

    def _ask_team(self):
        """Ask about team size and collaboration."""
        print()
        print("Question 3: How many people will use chora-compose?")
        print()
        print("  1. Just me (solo developer)")
        print("  2. Small team (2-5 people)")
        print("  3. Medium team (6-15 people)")
        print("  4. Large team (15+ people)")
        print()

        choice = self._get_choice(1, 4)

        if choice == 1:
            self.scores[Modality.PIP] += 2
            self.scores[Modality.CLI] += 2
            self.scores[Modality.MCP] += 2
            self.reasons[Modality.PIP].append("Solo usage (pip simple for one developer)")
            self.answers['team_size'] = 'solo'
        elif choice == 2:
            self.scores[Modality.PIP] += 1
            self.scores[Modality.DOCKER] += 2
            self.reasons[Modality.DOCKER].append("Small team collaboration (Docker consistency)")
            self.answers['team_size'] = 'small'
        elif choice >= 3:
            self.scores[Modality.DOCKER] += 5
            self.reasons[Modality.DOCKER].append("Team usage (Docker ensures consistency)")
            self.answers['team_size'] = 'medium_large'

    def _ask_constraints(self):
        """Ask about technical constraints."""
        print()
        print("Question 4: Do you have any technical constraints?")
        print()
        print("  1. Must work offline (no internet after setup)")
        print("  2. Security-sensitive (prefer no external dependencies)")
        print("  3. Need reproducible builds (strict version control)")
        print("  4. Limited disk space")
        print("  5. No specific constraints")
        print()

        choice = self._get_choice(1, 5)

        if choice == 1:
            self.scores[Modality.PIP] += 3
            self.scores[Modality.CLI] += 3
            self.reasons[Modality.PIP].append("Offline capability (pip cache)")
            self.reasons[Modality.CLI].append("Offline capability (standalone binary)")
            self.answers['constraints'] = 'offline'
        elif choice == 2:
            self.scores[Modality.PIP] += 4
            self.reasons[Modality.PIP].append("Security (direct dependency control)")
            self.answers['constraints'] = 'security'
        elif choice == 3:
            self.scores[Modality.DOCKER] += 5
            self.reasons[Modality.DOCKER].append("Reproducibility (pinned Docker image)")
            self.answers['constraints'] = 'reproducibility'
        elif choice == 4:
            self.scores[Modality.PIP] += 3
            self.scores[Modality.CLI] += 3
            self.reasons[Modality.PIP].append("Disk space (no Docker image overhead)")
            self.answers['constraints'] = 'disk_space'
        else:
            self.answers['constraints'] = 'none'

    def _get_choice(self, min_val: int, max_val: int) -> int:
        """Get validated choice from user."""
        while True:
            try:
                choice_str = input(f"Your choice ({min_val}-{max_val}): ").strip()
                choice = int(choice_str)
                if min_val <= choice <= max_val:
                    return choice
                print(f"Please enter a number between {min_val} and {max_val}.")
            except (ValueError, KeyboardInterrupt):
                if choice_str.lower() in ('q', 'quit', 'exit'):
                    print("\nExiting modality selector.")
                    sys.exit(0)
                print("Invalid input. Please enter a number.")
            except EOFError:
                print("\nExiting modality selector.")
                sys.exit(0)

    def _get_recommendation(self) -> ModalityScore:
        """Calculate and return top recommendation."""
        # Find modality with highest score
        top_modality = max(self.scores.items(), key=lambda x: x[1])
        modality = top_modality[0]
        score = top_modality[1]

        # Get considerations for this modality
        considerations = self._get_considerations(modality)

        result = ModalityScore(
            modality=modality,
            score=score,
            reasons=self.reasons[modality],
            considerations=considerations
        )

        self._print_recommendation(result)
        return result

    def _get_considerations(self, modality: Modality) -> List[str]:
        """Get considerations for selected modality."""
        considerations = {
            Modality.PIP: [
                "Requires Python 3.12+ installed",
                "Direct access to Python API",
                "Best for programmatic integration",
                "Setup time: 5-10 minutes"
            ],
            Modality.MCP: [
                "Requires Docker Desktop installed",
                "Provides 24 MCP tools for AI agents",
                "Best for AI-assisted content generation",
                "Setup time: 10-15 minutes"
            ],
            Modality.CLI: [
                "Interactive command-line interface",
                "Great for testing and exploration",
                "No coding required",
                "Setup time: 5 minutes"
            ],
            Modality.DOCKER: [
                "Requires Docker Desktop installed",
                "Ensures consistency across team",
                "Integrates with n8n, webhooks, CI/CD",
                "Setup time: 15-20 minutes"
            ]
        }
        return considerations.get(modality, [])

    def _print_recommendation(self, result: ModalityScore):
        """Print recommendation to console."""
        print()
        print("=" * 70)
        print("RECOMMENDATION")
        print("=" * 70)
        print()
        print(f"✅ Recommended Modality: {result.modality.value.upper()}")
        print(f"   Confidence Score: {result.score}/20")
        print()

        if result.reasons:
            print("Why this modality?")
            for reason in result.reasons:
                print(f"  • {reason}")
            print()

        if result.considerations:
            print("Key Considerations:")
            for consideration in result.considerations:
                print(f"  • {consideration}")
            print()

        print("Next Steps:")
        print(f"  1. See protocol-spec.md §2 for detailed {result.modality.value.upper()} setup")
        print(f"  2. Follow adoption-blueprint.md Workflow {self._get_workflow_number(result.modality)}")
        print("  3. Complete setup in < 30 minutes")
        print()

        # Show alternative if score is close
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_scores) > 1:
            second_best = sorted_scores[1]
            if second_best[1] >= result.score * 0.7:  # Within 30% of top score
                print(f"Alternative: {second_best[0].value.upper()} (score: {second_best[1]})")
                print(f"  Consider if: {', '.join(self.reasons[second_best[0]][:2])}")
                print()

    def _get_workflow_number(self, modality: Modality) -> str:
        """Get workflow number from adoption-blueprint.md."""
        workflow_map = {
            Modality.PIP: "1 (Python Project)",
            Modality.MCP: "2 (AI Agent)",
            Modality.CLI: "1 or 2",
            Modality.DOCKER: "3 (Team/Docker)"
        }
        return workflow_map.get(modality, "1-3")

    def export_markdown(self, result: ModalityScore, output_path: Optional[str] = None) -> str:
        """Export recommendation as markdown guide."""
        md = f"""# chora-compose Integration Guide

**Selected Modality**: {result.modality.value.upper()}
**Confidence Score**: {result.score}/20
**Generated**: {self._get_timestamp()}

---

## Why {result.modality.value.upper()}?

"""
        for reason in result.reasons:
            md += f"- {reason}\n"

        md += f"""
---

## Key Considerations

"""
        for consideration in result.considerations:
            md += f"- {consideration}\n"

        md += f"""
---

## Setup Steps

See [protocol-spec.md §2](./protocol-spec.md) for detailed {result.modality.value.upper()} setup instructions.

Quick start:

"""

        # Add modality-specific quick start
        quick_starts = {
            Modality.PIP: """
```bash
# Install chora-compose
pip install chora-compose

# Verify installation
python -c "import chora_compose; print(chora_compose.__version__)"

# Generate first content
python -c "from chora_compose import ContentGenerator; print('Setup complete!')"
```
""",
            Modality.MCP: """
```bash
# Pull Docker image
docker pull ghcr.io/liminalcommons/chora-compose-mcp:latest

# Add to Claude Desktop config (~/.config/claude/config.json)
{
  "mcpServers": {
    "chora-compose": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "${workspaceFolder}:/workspace",
               "ghcr.io/liminalcommons/chora-compose-mcp:latest"]
    }
  }
}

# Restart Claude Desktop
# Test with: "List available chora-compose tools"
```
""",
            Modality.CLI: """
```bash
# Download CLI (choose your platform)
# macOS:
curl -L https://github.com/liminalcommons/chora-compose/releases/latest/download/chora-compose-macos -o chora-compose
chmod +x chora-compose

# Linux:
curl -L https://github.com/liminalcommons/chora-compose/releases/latest/download/chora-compose-linux -o chora-compose
chmod +x chora-compose

# Windows: Download .exe from releases

# Test CLI
./chora-compose --version
./chora-compose list-generators
```
""",
            Modality.DOCKER: """
```bash
# Pull Docker image
docker pull ghcr.io/liminalcommons/chora-compose:latest

# Test Docker image
docker run --rm -v $(pwd):/workspace ghcr.io/liminalcommons/chora-compose:latest --version

# For n8n integration, see protocol-spec.md §4.4
```
"""
        }

        md += quick_starts.get(result.modality, "")

        md += """
---

## Next Steps

1. Complete setup using instructions above
2. Explore example configs in `examples/` directory
3. Generate your first content (target: < 30 min to first success)
4. Review troubleshooting guide if issues arise

**Questions?** See [adoption-blueprint.md](./adoption-blueprint.md) for role-based workflows.
"""

        if output_path:
            with open(output_path, 'w') as f:
                f.write(md)
            print(f"✅ Exported guide to: {output_path}")

        return md

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactive modality selector for chora-compose integration"
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick mode (fewer questions)'
    )
    parser.add_argument(
        '--export',
        metavar='FORMAT',
        choices=['md', 'markdown'],
        help='Export recommendation as markdown guide'
    )
    parser.add_argument(
        '--output',
        metavar='PATH',
        help='Output path for exported guide (default: modality-guide.md)'
    )

    args = parser.parse_args()

    # Run selector
    selector = ModalitySelector(quick_mode=args.quick)
    result = selector.run()

    # Export if requested
    if args.export:
        output_path = args.output or 'modality-guide.md'
        selector.export_markdown(result, output_path)

    print("=" * 70)
    print("Thank you for using the chora-compose modality selector!")
    print("=" * 70)


if __name__ == '__main__':
    main()
