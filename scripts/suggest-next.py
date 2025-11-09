#!/usr/bin/env python3
"""
Context-Aware Suggestion Engine for chora-base

Analyzes project state and suggests next actions based on:
- Recent activity (event log)
- Current phase (DDD/BDD/TDD)
- Outstanding gaps (SAP evaluation)
- Upcoming deadlines (sprint planning)
- Quality metrics

Usage:
    python scripts/suggest-next.py
    python scripts/suggest-next.py --context task-005
    python scripts/suggest-next.py --mode proactive  # Check without being asked
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add repo root to path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "scripts"))

from usage_tracker import track_usage


@dataclass
class Suggestion:
    """Represents a suggested next action."""

    action: str
    rationale: str
    priority: str  # high, medium, low
    category: str  # workflow, quality, planning, learning
    command: Optional[str] = None
    estimated_time: Optional[str] = None
    context_signals: list[str] = field(default_factory=list)


class ProjectContext:
    """Analyzes current project state for suggestions."""

    def __init__(self, project_root: Path):
        """Initialize with project root directory."""
        self.project_root = project_root
        self.inbox_dir = project_root / "inbox"
        self.event_log = self.inbox_dir / "coordination" / "events.jsonl"
        self.active_dir = self.inbox_dir / "active"

    def get_recent_events(self, hours: int = 24) -> list[dict]:
        """Get events from the last N hours."""
        if not self.event_log.exists():
            return []

        from datetime import timezone
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent = []

        with open(self.event_log, encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    timestamp_str = event.get("timestamp", "")
                    # Parse ISO format with timezone
                    event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    # Ensure event_time is timezone-aware
                    if event_time.tzinfo is None:
                        from datetime import timezone
                        event_time = event_time.replace(tzinfo=timezone.utc)
                    if event_time > cutoff:
                        recent.append(event)
                except (json.JSONDecodeError, ValueError):
                    continue

        return recent

    def get_active_work(self) -> list[str]:
        """Get list of active work items."""
        if not self.active_dir.exists():
            return []

        return [d.name for d in self.active_dir.iterdir() if d.is_dir()]

    def get_inbox_status(self) -> dict:
        """Get inbox status summary."""
        status = {
            "coordination_requests": 0,
            "implementation_tasks": 0,
            "active_items": 0,
            "blockers": [],
            "pending_triage": [],
            "accepted_items": [],
            "high_priority_items": [],
        }

        incoming_coord = self.inbox_dir / "incoming" / "coordination"
        incoming_tasks = self.inbox_dir / "incoming" / "tasks"

        if incoming_coord.exists():
            status["coordination_requests"] = len(list(incoming_coord.glob("*.json")))

        if incoming_tasks.exists():
            status["implementation_tasks"] = len(list(incoming_tasks.glob("*.json")))

        if self.active_dir.exists():
            status["active_items"] = len([d for d in self.active_dir.iterdir() if d.is_dir()])

        return status

    def get_ecosystem_status(self) -> Optional[dict]:
        """Parse ECOSYSTEM_STATUS.yaml for detailed inbox context."""
        ecosystem_file = self.inbox_dir / "coordination" / "ECOSYSTEM_STATUS.yaml"
        if not ecosystem_file.exists():
            return None

        try:
            with open(ecosystem_file, encoding='utf-8') as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, IOError):
            return None

    def get_coordination_requests(self) -> list[dict]:
        """Get active coordination requests with details from ECOSYSTEM_STATUS.yaml."""
        ecosystem = self.get_ecosystem_status()
        if not ecosystem:
            return []

        requests = []

        # Extract from repositories.chora-base.active_work
        chora_base = ecosystem.get("repositories", {}).get("chora-base", {})
        active_work = chora_base.get("active_work", [])

        for item in active_work:
            if isinstance(item, dict):
                requests.append({
                    "id": item.get("id", "unknown"),
                    "title": item.get("title", ""),
                    "status": item.get("status", ""),
                    "priority": item.get("priority", ""),
                    "phase": item.get("phase", ""),
                    "estimated_effort": item.get("estimated_effort", ""),
                    "from_repo": item.get("from", ""),
                    "blockers": [],  # Individual blockers would be in item
                })

        return requests

    def get_blockers(self) -> list[str]:
        """Get list of blockers from ECOSYSTEM_STATUS.yaml."""
        ecosystem = self.get_ecosystem_status()
        if not ecosystem:
            return []

        chora_base = ecosystem.get("repositories", {}).get("chora-base", {})
        return chora_base.get("blockers", [])

    def check_test_coverage(self) -> Optional[float]:
        """Check current test coverage percentage."""
        # Check if pytest is already running to avoid spawning duplicates
        try:
            ps_check = subprocess.run(
                ["pgrep", "-f", "pytest.*--cov"],
                capture_output=True,
                timeout=5,
            )
            if ps_check.returncode == 0:
                # pytest already running, skip to avoid duplicates
                return None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        try:
            result = subprocess.run(
                ["pytest", "--cov=src", "--cov-report=term", "--quiet"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_root,
            )

            # Parse coverage from output
            for line in result.stdout.split("\n"):
                if "TOTAL" in line:
                    parts = line.split()
                    for part in parts:
                        if "%" in part:
                            return float(part.rstrip("%"))
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        return None

    def check_quality_gates(self) -> dict[str, bool]:
        """Check if quality gates would pass."""
        gates = {
            "tests_passing": False,
            "lint_clean": False,
            "type_check_clean": False,
        }

        # Check if pytest is already running to avoid spawning duplicates
        try:
            ps_check = subprocess.run(
                ["pgrep", "-f", "pytest"],
                capture_output=True,
                timeout=5,
            )
            if ps_check.returncode == 0:
                # pytest already running, skip tests check
                return gates
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Check tests
        try:
            result = subprocess.run(
                ["pytest", "--quiet"],
                capture_output=True,
                timeout=30,
                cwd=self.project_root,
            )
            gates["tests_passing"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Check linting
        try:
            result = subprocess.run(
                ["ruff", "check", "."],
                capture_output=True,
                timeout=30,
                cwd=self.project_root,
            )
            gates["lint_clean"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Check type checking
        try:
            result = subprocess.run(
                ["mypy", "src/"],
                capture_output=True,
                timeout=30,
                cwd=self.project_root,
            )
            gates["type_check_clean"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return gates

    def detect_phase(self, context_item: Optional[str] = None) -> Optional[str]:
        """Detect current development phase for active work."""
        if not context_item:
            active_items = self.get_active_work()
            if not active_items:
                return None
            context_item = active_items[0]

        item_dir = self.active_dir / context_item

        # Check for DDD artifacts
        if (item_dir / "change-request.md").exists():
            # Check if has BDD scenarios
            features_dir = self.project_root / "features"
            if features_dir.exists() and any(features_dir.glob("*.feature")):
                # Check if has passing tests
                tests_dir = self.project_root / "tests"
                if tests_dir.exists():
                    return "tdd"  # Has tests, likely in TDD phase
                return "bdd"  # Has scenarios, moving to TDD
            return "ddd"  # Has change request, not yet BDD

        return None


class SuggestionEngine:
    """Generate context-aware next action suggestions."""

    def __init__(self, context: ProjectContext):
        """Initialize with project context."""
        self.context = context

    def suggest(self, mode: str = "reactive") -> list[Suggestion]:
        """
        Generate suggestions based on project state.

        Modes:
        - reactive: User asked "what next?" (show top 3-5 suggestions)
        - proactive: Background check (only show high-priority)
        - comprehensive: Deep analysis (show all possibilities)
        """
        suggestions = []

        # Workflow suggestions
        suggestions.extend(self._suggest_workflow())

        # Quality suggestions
        suggestions.extend(self._suggest_quality())

        # Planning suggestions
        suggestions.extend(self._suggest_planning())

        # Learning suggestions
        suggestions.extend(self._suggest_learning())

        # Filter by mode
        if mode == "proactive":
            suggestions = [s for s in suggestions if s.priority == "high"]
        elif mode == "reactive":
            suggestions = suggestions[:5]  # Top 5

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        suggestions.sort(key=lambda s: priority_order.get(s.priority, 3))

        return suggestions

    def _suggest_workflow(self) -> list[Suggestion]:
        """Suggest workflow-related next steps."""
        suggestions = []

        # Check for blockers first (highest priority)
        blockers = self.context.get_blockers()
        if blockers:
            suggestions.append(
                Suggestion(
                    action=f"Resolve {len(blockers)} blocker(s)",
                    rationale=f"Blockers detected: {', '.join(blockers[:2])}{'...' if len(blockers) > 2 else ''}",
                    priority="high",
                    category="workflow",
                    command="# Review ECOSYSTEM_STATUS.yaml for blocker details",
                    estimated_time="Varies by blocker",
                    context_signals=["blockers_detected"],
                )
            )

        # Check coordination requests from ECOSYSTEM_STATUS.yaml
        coord_requests = self.context.get_coordination_requests()

        # Prioritize by status and priority
        pending_triage = [r for r in coord_requests if r["status"] == "pending_triage"]
        accepted_p1 = [r for r in coord_requests if r["status"] == "accepted" and r["priority"] in ["P0", "P1"]]
        accepted_p2 = [r for r in coord_requests if r["status"] == "accepted" and r["priority"] == "P2"]

        # Suggest triaging pending requests
        if pending_triage:
            for req in pending_triage[:1]:  # Focus on first one
                suggestions.append(
                    Suggestion(
                        action=f"Triage coordination request {req['id']}",
                        rationale=f"{req['title']} is pending triage. Review and decide: accept, defer, or decline.",
                        priority="high" if req["priority"] in ["P0", "P1"] else "medium",
                        category="workflow",
                        command=f"# Review inbox/incoming/coordination/{req['id']}.json",
                        estimated_time=req["estimated_effort"] if req["estimated_effort"] else "30-60 minutes",
                        context_signals=["coordination_pending_triage", f"priority_{req['priority']}"],
                    )
                )

        # Suggest working on accepted P1/P2 requests
        if accepted_p1:
            for req in accepted_p1[:1]:
                phase = req.get("phase", "unknown")
                suggestions.append(
                    Suggestion(
                        action=f"Continue work on {req['id']} ({phase})",
                        rationale=f"High-priority request '{req['title']}' is in {phase} phase.",
                        priority="high",
                        category="workflow",
                        command=f"# Check inbox/active/{req['id']}/",
                        estimated_time=req["estimated_effort"] if req["estimated_effort"] else "Varies",
                        context_signals=["accepted_p1", f"phase_{phase}"],
                    )
                )

        if accepted_p2:
            for req in accepted_p2[:1]:
                phase = req.get("phase", "unknown")
                suggestions.append(
                    Suggestion(
                        action=f"Continue work on {req['id']} ({phase})",
                        rationale=f"'{req['title']}' is in {phase} phase.",
                        priority="medium",
                        category="workflow",
                        command=f"# Check inbox/active/{req['id']}/",
                        estimated_time=req["estimated_effort"] if req["estimated_effort"] else "Varies",
                        context_signals=["accepted_p2", f"phase_{phase}"],
                    )
                )

        # Check for active work (legacy detection)
        active_items = self.context.get_active_work()

        if active_items and not coord_requests:
            # Fallback to legacy phase detection if ECOSYSTEM_STATUS not available
            for item in active_items[:1]:  # Focus on first item
                phase = self.context.detect_phase(item)

                if phase == "ddd":
                    suggestions.append(
                        Suggestion(
                            action="Start BDD scenarios",
                            rationale=f"Change request complete for {item}. Ready to write Gherkin scenarios.",
                            priority="high",
                            category="workflow",
                            command=f"python scripts/start-bdd.py {item}",
                            estimated_time="1-2 hours",
                            context_signals=["ddd_complete", "active_work_exists"],
                        )
                    )
                elif phase == "bdd":
                    suggestions.append(
                        Suggestion(
                            action="Start TDD implementation",
                            rationale=f"BDD scenarios written for {item}. Begin RED-GREEN-REFACTOR cycles.",
                            priority="high",
                            category="workflow",
                            command=f"python scripts/start-tdd.py {item}",
                            estimated_time="4-8 hours",
                            context_signals=["bdd_complete", "scenarios_exist"],
                        )
                    )
                elif phase == "tdd":
                    suggestions.append(
                        Suggestion(
                            action="Run tests and check coverage",
                            rationale=f"Implementation in progress for {item}. Verify tests passing and coverage ≥85%.",
                            priority="medium",
                            category="workflow",
                            command="pytest --cov=src --cov-report=term",
                            estimated_time="5 minutes",
                            context_signals=["tdd_in_progress", "implementation_exists"],
                        )
                    )

        # If no active work at all, suggest reviewing inbox
        if not active_items and not coord_requests:
            inbox_status = self.context.get_inbox_status()
            if inbox_status["coordination_requests"] > 0:
                suggestions.append(
                    Suggestion(
                        action="Review coordination requests",
                        rationale=f"{inbox_status['coordination_requests']} pending coordination request(s) in inbox.",
                        priority="medium",
                        category="planning",
                        command="python scripts/inbox-status.py",
                        estimated_time="15-30 minutes",
                        context_signals=["inbox_not_empty", "coordination_pending"],
                    )
                )

        return suggestions

    def _suggest_quality(self) -> list[Suggestion]:
        """Suggest quality-related improvements."""
        suggestions = []

        # Check coverage
        coverage = self.context.check_test_coverage()
        if coverage is not None and coverage < 85:
            suggestions.append(
                Suggestion(
                    action=f"Improve test coverage (currently {coverage:.1f}%)",
                    rationale="Coverage below 85% target. Add tests for uncovered code.",
                    priority="high" if coverage < 70 else "medium",
                    category="quality",
                    command="pytest --cov=src --cov-report=html && open htmlcov/index.html",
                    estimated_time="1-3 hours",
                    context_signals=[f"coverage_below_target_{coverage:.0f}"],
                )
            )

        # Check quality gates
        gates = self.context.check_quality_gates()

        if not gates["tests_passing"]:
            suggestions.append(
                Suggestion(
                    action="Fix failing tests",
                    rationale="Tests are currently failing. Fix before proceeding.",
                    priority="high",
                    category="quality",
                    command="pytest -v",
                    estimated_time="30 minutes - 2 hours",
                    context_signals=["tests_failing"],
                )
            )

        if not gates["lint_clean"]:
            suggestions.append(
                Suggestion(
                    action="Fix linting errors",
                    rationale="Linting errors detected. Run ruff to fix.",
                    priority="medium",
                    category="quality",
                    command="ruff check --fix .",
                    estimated_time="15-30 minutes",
                    context_signals=["lint_errors"],
                )
            )

        if not gates["type_check_clean"]:
            suggestions.append(
                Suggestion(
                    action="Fix type errors",
                    rationale="Type checking errors detected. Run mypy to see details.",
                    priority="medium",
                    category="quality",
                    command="mypy src/",
                    estimated_time="30 minutes - 1 hour",
                    context_signals=["type_errors"],
                )
            )

        return suggestions

    def _suggest_planning(self) -> list[Suggestion]:
        """Suggest planning-related actions."""
        suggestions = []

        # Check for upcoming sprint planning
        # (This is placeholder - would integrate with sprint schedule)

        # Check for unreviewed inbox items
        inbox_status = self.context.get_inbox_status()
        total_pending = (
            inbox_status["coordination_requests"] + inbox_status["implementation_tasks"]
        )

        if total_pending > 5:
            suggestions.append(
                Suggestion(
                    action="Triage inbox backlog",
                    rationale=f"{total_pending} items in inbox. Review and prioritize.",
                    priority="medium",
                    category="planning",
                    command="python scripts/inbox-status.py",
                    estimated_time="30-60 minutes",
                    context_signals=["inbox_backlog_high"],
                )
            )

        return suggestions

    def _suggest_learning(self) -> list[Suggestion]:
        """Suggest learning and improvement opportunities."""
        suggestions = []

        # Suggest SAP evaluation if not done recently
        # (Placeholder - would check last evaluation date)

        recent_events = self.context.get_recent_events(hours=168)  # 1 week
        sap_evals = [e for e in recent_events if "sap_evaluator" in e.get("action", "")]

        if not sap_evals:
            suggestions.append(
                Suggestion(
                    action="Run SAP evaluation",
                    rationale="No SAP evaluation in the last week. Check adoption status.",
                    priority="low",
                    category="learning",
                    command="python scripts/sap-evaluator.py --quick",
                    estimated_time="30 seconds",
                    context_signals=["no_recent_sap_eval"],
                )
            )

        return suggestions


def display_suggestions(suggestions: list[Suggestion]) -> None:
    """Display suggestions in readable format."""
    if not suggestions:
        print("✅ No suggestions - everything looks good!")
        return

    print(f"\n{'='*70}")
    print("💡 Suggested Next Actions")
    print(f"{'='*70}\n")

    for i, suggestion in enumerate(suggestions, 1):
        # Priority indicator
        if suggestion.priority == "high":
            priority_icon = "🔴"
        elif suggestion.priority == "medium":
            priority_icon = "🟡"
        else:
            priority_icon = "🟢"

        # Category icon
        category_icons = {
            "workflow": "⚙️",
            "quality": "✅",
            "planning": "📋",
            "learning": "📚",
        }
        category_icon = category_icons.get(suggestion.category, "•")

        print(f"{i}. {priority_icon} {category_icon} {suggestion.action}")
        print(f"   {suggestion.rationale}")

        if suggestion.estimated_time:
            print(f"   ⏱️  Estimated time: {suggestion.estimated_time}")

        if suggestion.command:
            print(f"   📝 Command: {suggestion.command}")

        print()


@track_usage
def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Context-aware next action suggestions"
    )
    parser.add_argument(
        "--mode",
        choices=["reactive", "proactive", "comprehensive"],
        default="reactive",
        help="Suggestion mode (reactive=user asked, proactive=background, comprehensive=all)",
    )
    parser.add_argument(
        "--context",
        help="Specific context (e.g., task-005) for targeted suggestions",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory",
    )
    parser.add_argument(
        "--format",
        choices=["terminal", "json", "markdown"],
        default="terminal",
        help="Output format",
    )

    args = parser.parse_args()

    # Create context and engine
    context = ProjectContext(args.project_root)
    engine = SuggestionEngine(context)

    # Generate suggestions
    suggestions = engine.suggest(mode=args.mode)

    # Display based on format
    if args.format == "json":
        output = [
            {
                "action": s.action,
                "rationale": s.rationale,
                "priority": s.priority,
                "category": s.category,
                "command": s.command,
                "estimated_time": s.estimated_time,
            }
            for s in suggestions
        ]
        print(json.dumps(output, indent=2))
    elif args.format == "markdown":
        print("# Suggested Next Actions\n")
        for i, s in enumerate(suggestions, 1):
            print(f"## {i}. {s.action}\n")
            print(f"**Priority:** {s.priority.capitalize()}")
            print(f"**Category:** {s.category.capitalize()}\n")
            print(f"{s.rationale}\n")
            if s.command:
                print(f"**Command:**\n```bash\n{s.command}\n```\n")
    else:
        display_suggestions(suggestions)


if __name__ == "__main__":
    main()
