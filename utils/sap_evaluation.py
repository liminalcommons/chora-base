"""
SAP Self-Evaluation Engine

Core evaluation logic for assessing SAP adoption depth.
Supports progressive evaluation: quick → deep → strategic.

Usage:
    from utils.sap_evaluation import SAPEvaluator

    evaluator = SAPEvaluator(repo_root=Path.cwd())
    result = evaluator.quick_check("SAP-004")
    print(result.current_level)
"""

import json
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Optional, Any
import sys


@dataclass
class Action:
    """Concrete step to improve adoption"""
    action_id: str
    description: str
    tool: str  # Read, Write, Edit, Bash, etc.
    file_path: Optional[str] = None
    location: Optional[str] = None
    content: Optional[str] = None
    command: Optional[str] = None
    rationale: str = ""
    expected_outcome: str = ""
    validation_command: Optional[str] = None
    estimated_minutes: int = 0
    sequence: int = 1
    depends_on: list[str] = field(default_factory=list)


@dataclass
class Gap:
    """Identified improvement opportunity"""
    gap_id: str
    gap_type: str  # installation, integration, quality, optimization
    title: str
    description: str
    impact: str  # high, medium, low
    effort: str  # high, medium, low
    priority: str  # P0, P1, P2
    urgency: str  # blocks_sprint, next_sprint, future
    current_state: str = ""
    desired_state: str = ""
    blocks: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    estimated_hours: float = 0.0
    validation: str = ""


@dataclass
class EvaluationResult:
    """Result of a single SAP evaluation"""
    # Identity
    sap_id: str
    sap_name: str
    evaluation_type: str  # quick, deep, strategic
    timestamp: datetime

    # Current state
    is_installed: bool
    current_level: int  # 0, 1, 2, or 3
    completion_percent: float = 0.0

    # Validation results
    validation_results: dict[str, bool] = field(default_factory=dict)
    quality_scores: dict[str, float] = field(default_factory=dict)

    # Gap analysis
    gaps: list[Gap] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    # Recommendations
    next_milestone: str = ""
    recommended_actions: list[Action] = field(default_factory=list)
    estimated_effort_hours: float = 0.0

    # Metadata
    duration_seconds: float = 0.0
    confidence: str = "medium"  # high, medium, low
    warnings: list[str] = field(default_factory=list)


@dataclass
class PrioritizedGap:
    """Gap with priority ranking"""
    rank: int
    sap_id: str
    gap: Gap
    reason: str = ""
    impact_score: float = 0.5
    effort_score: float = 0.5
    priority_score: float = 0.5
    sprint: str = "future"  # current, next, future
    deliverables: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)


@dataclass
class SprintPlan:
    """SAP adoption tasks for a sprint"""
    sprint_name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    focus_saps: list[str] = field(default_factory=list)
    target_levels: dict[str, int] = field(default_factory=dict)
    tasks: list[dict] = field(default_factory=list)
    total_estimated_hours: float = 0.0
    validation_commands: list[str] = field(default_factory=list)
    expected_outcomes: list[str] = field(default_factory=list)


@dataclass
class AdoptionRoadmap:
    """Strategic adoption plan over time"""
    # Metadata
    generated_at: datetime
    target_quarter: str
    next_review_date: Optional[date] = None

    # Current state
    total_saps_installed: int = 0
    adoption_distribution: dict[str, int] = field(default_factory=dict)
    average_adoption_level: float = 0.0
    total_hours_invested: float = 0.0

    # Goals
    quarterly_goals: dict[str, Any] = field(default_factory=dict)
    target_saps_to_install: list[str] = field(default_factory=list)
    target_level_2_count: int = 0
    target_roi: float = 3.0

    # Prioritized gaps
    priority_gaps: list[PrioritizedGap] = field(default_factory=list)

    # Sprint breakdown
    this_sprint: Optional[SprintPlan] = None
    next_sprint: Optional[SprintPlan] = None
    future_sprints: list[SprintPlan] = field(default_factory=list)


class SAPEvaluator:
    """Core SAP evaluation engine"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.catalog = self.load_catalog()

    def load_catalog(self) -> dict:
        """Load SAP catalog from sap-catalog.json"""
        catalog_path = self.repo_root / "sap-catalog.json"
        if not catalog_path.exists():
            print(f"Warning: sap-catalog.json not found at {catalog_path}", file=sys.stderr)
            return {}

        with open(catalog_path) as f:
            data = json.load(f)
            # Handle different catalog formats
            if isinstance(data, list):
                # Array of SAPs
                return {sap["id"]: sap for sap in data}
            elif isinstance(data, dict) and "saps" in data:
                # Object with 'saps' array (current format)
                return {sap["id"]: sap for sap in data["saps"]}
            else:
                # Assume it's already a dict of SAPs
                return data

    def get_sap_metadata(self, sap_id: str) -> Optional[dict]:
        """Get SAP metadata from catalog"""
        return self.catalog.get(sap_id)

    def check_sap_installed(self, sap_id: str) -> bool:
        """Check if SAP artifacts are present"""
        sap = self.get_sap_metadata(sap_id)
        if not sap:
            return False

        location = sap.get("location")
        if not location:
            return False

        sap_dir = self.repo_root / location
        if not sap_dir.exists():
            return False

        # Check for required artifacts
        required = [
            "capability-charter.md",
            "protocol-spec.md",
            "awareness-guide.md",
            "adoption-blueprint.md",
            "ledger.md"
        ]

        for artifact in required:
            if not (sap_dir / artifact).exists():
                return False

        return True

    def run_validation_command(self, command: str, timeout: int = 30) -> tuple[bool, str]:
        """
        Run a validation command and return success + output

        Returns:
            (success: bool, output: str)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.repo_root
            )
            success = result.returncode == 0
            output = result.stdout + result.stderr
            return success, output
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout}s"
        except Exception as e:
            return False, f"Command failed: {e}"

    def quick_check(self, sap_id: str) -> EvaluationResult:
        """
        Level 1: Quick automated validation (30 seconds)

        Process:
        1. Check installation (artifacts present)
        2. Run basic validation commands
        3. Determine adoption level
        4. Identify immediate blockers
        """
        start_time = datetime.now()
        sap = self.get_sap_metadata(sap_id)

        if not sap:
            return EvaluationResult(
                sap_id=sap_id,
                sap_name="unknown",
                evaluation_type="quick",
                timestamp=start_time,
                is_installed=False,
                current_level=0,
                warnings=[f"SAP {sap_id} not found in catalog"]
            )

        sap_name = sap.get("name", "unknown")

        # Check installation
        is_installed = self.check_sap_installed(sap_id)

        validation_results = {
            "artifacts_complete": is_installed
        }

        current_level = 0
        blockers = []

        if is_installed:
            current_level = 1  # At minimum Level 1 if installed

            # Try to run SAP-specific validation (if protocol defines it)
            # For now, basic check only
            validation_results["installed"] = True
        else:
            blockers.append(f"SAP {sap_id} not installed")

        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()

        return EvaluationResult(
            sap_id=sap_id,
            sap_name=sap_name,
            evaluation_type="quick",
            timestamp=start_time,
            is_installed=is_installed,
            current_level=current_level,
            completion_percent=0.0 if current_level == 0 else 33.3,  # Rough estimate
            validation_results=validation_results,
            blockers=blockers,
            next_milestone=f"Level {current_level + 1}" if current_level < 3 else "Fully adopted",
            estimated_effort_hours=2.0 if current_level == 0 else 3.0,
            duration_seconds=duration,
            confidence="high"  # Automated checks are high confidence
        )

    def quick_check_all(self) -> list[EvaluationResult]:
        """Run quick check on all SAPs in catalog"""
        results = []
        for sap_id in self.catalog.keys():
            result = self.quick_check(sap_id)
            results.append(result)
        return results

    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file, return None if doesn't exist"""
        try:
            if not file_path.exists():
                return None
            with open(file_path, 'r') as f:
                return f.read()
        except Exception:
            return None

    def count_lines(self, content: Optional[str]) -> int:
        """Count lines in content"""
        if not content:
            return 0
        return len(content.split('\n'))

    def analyze_sap_004_testing(self, sap_id: str) -> list[Gap]:
        """Analyze SAP-004 (Testing Framework) adoption"""
        gaps = []

        # Check test coverage
        success, output = self.run_validation_command("pytest --cov=src --cov-report=term 2>&1 || true")
        coverage_match = None
        if output:
            import re
            coverage_match = re.search(r'TOTAL.*?(\d+)%', output)

        current_coverage = int(coverage_match.group(1)) if coverage_match else 0

        if current_coverage < 85:
            gap = Gap(
                gap_id=f"{sap_id}-coverage",
                gap_type="quality",
                title=f"Test coverage {current_coverage}% < 85% target",
                description=f"Current test coverage is {85 - current_coverage}% below Level 2 requirement. Additional tests needed.",
                impact="high",
                effort="medium",
                priority="P0",
                urgency="blocks_sprint",
                current_state=f"{current_coverage}% coverage",
                desired_state="85% coverage (Level 2 requirement)",
                blocks=["SAP-005"],  # Blocks CI/CD coverage gates
                estimated_hours=3.0,
                validation="pytest --cov=src shows ≥85%"
            )
            gaps.append(gap)

        return gaps

    def analyze_sap_009_awareness(self, sap_id: str) -> list[Gap]:
        """Analyze SAP-009 (Agent Awareness) adoption"""
        gaps = []

        # Check AGENTS.md
        agents_md = self.repo_root / "AGENTS.md"
        content = self.read_file_safe(agents_md)
        line_count = self.count_lines(content)

        if line_count < 600:
            gap = Gap(
                gap_id=f"{sap_id}-agents-short",
                gap_type="quality",
                title=f"AGENTS.md too short ({line_count} lines < 600 recommended)",
                description="AGENTS.md should be comprehensive (≥600 lines for Level 2)",
                impact="medium",
                effort="medium",
                priority="P1",
                urgency="next_sprint",
                current_state=f"{line_count} lines in AGENTS.md",
                desired_state="≥600 lines with comprehensive sections",
                estimated_hours=2.0,
                validation="wc -l AGENTS.md shows ≥600"
            )
            gaps.append(gap)

        # Check for domain-specific AGENTS.md files
        test_agents = self.repo_root / "tests" / "AGENTS.md"
        if not test_agents.exists():
            gap = Gap(
                gap_id=f"{sap_id}-no-domain-files",
                gap_type="integration",
                title="No domain-specific AGENTS.md files",
                description="Level 2 requires domain-specific awareness files (tests/, docs/, etc.)",
                impact="medium",
                effort="low",
                priority="P1",
                urgency="next_sprint",
                current_state="Only root AGENTS.md",
                desired_state="Domain files: tests/AGENTS.md, docs/AGENTS.md",
                estimated_hours=1.5,
                validation="test -f tests/AGENTS.md && test -f docs/AGENTS.md"
            )
            gaps.append(gap)

        return gaps

    def analyze_sap_013_metrics(self, sap_id: str) -> list[Gap]:
        """Analyze SAP-013 (Metrics Tracking) adoption"""
        gaps = []

        # Check if metrics utilities exist
        metrics_file = self.repo_root / "utils" / "claude_metrics.py"
        if not metrics_file.exists():
            gap = Gap(
                gap_id=f"{sap_id}-not-installed",
                gap_type="installation",
                title="Metrics tracking not installed",
                description="SAP-013 utilities not found. Install to track ROI.",
                impact="high",
                effort="low",
                priority="P0",
                urgency="blocks_sprint",
                current_state="No metrics tracking",
                desired_state="ClaudeROICalculator available",
                estimated_hours=1.0,
                validation="python -c 'from utils.claude_metrics import ClaudeROICalculator'"
            )
            gaps.append(gap)

        return gaps

    def analyze_sap_generic(self, sap_id: str, sap_name: str) -> list[Gap]:
        """Generic gap analysis for any SAP"""
        gaps = []

        # Check if AGENTS.md mentions this SAP
        agents_md = self.repo_root / "AGENTS.md"
        content = self.read_file_safe(agents_md)

        if content and sap_name not in content:
            gap = Gap(
                gap_id=f"{sap_id}-not-in-agents",
                gap_type="integration",
                title=f"{sap_name} not documented in AGENTS.md",
                description=f"AGENTS.md should reference how to use {sap_name}",
                impact="low",
                effort="low",
                priority="P2",
                urgency="future",
                current_state="No AGENTS.md documentation",
                desired_state=f"AGENTS.md has section on {sap_name} usage",
                estimated_hours=0.5,
                validation=f"grep '{sap_name}' AGENTS.md"
            )
            gaps.append(gap)

        return gaps

    def deep_dive(self, sap_id: str) -> EvaluationResult:
        """
        Level 2: Rule-based content analysis (5 minutes)

        Process:
        1. Run quick check first
        2. Analyze SAP-specific integration patterns
        3. Identify gaps vs. Level 2 criteria
        4. Prioritize by impact × effort
        5. Generate actionable recommendations

        Sprint 2: Rule-based gap detection (can be upgraded to LLM in Sprint 3)
        """
        start_time = datetime.now()

        # Start with quick check
        quick_result = self.quick_check(sap_id)

        if not quick_result.is_installed:
            return quick_result  # Return quick check if not installed

        sap = self.get_sap_metadata(sap_id)
        sap_name = sap.get("name", "unknown") if sap else "unknown"

        # Run SAP-specific analysis
        gaps = []

        if sap_id == "SAP-004":
            gaps.extend(self.analyze_sap_004_testing(sap_id))
        elif sap_id == "SAP-009":
            gaps.extend(self.analyze_sap_009_awareness(sap_id))
        elif sap_id == "SAP-013":
            gaps.extend(self.analyze_sap_013_metrics(sap_id))

        # Always run generic analysis
        gaps.extend(self.analyze_sap_generic(sap_id, sap_name))

        # If no gaps found, SAP is well-integrated
        if not gaps:
            gaps.append(Gap(
                gap_id=f"{sap_id}-well-integrated",
                gap_type="optimization",
                title="SAP well-integrated, consider Level 3",
                description=f"{sap_name} appears well-adopted. Consider advanced Level 3 features.",
                impact="low",
                effort="medium",
                priority="P2",
                urgency="future",
                current_state="Level 2 criteria met",
                desired_state="Level 3 advanced features",
                estimated_hours=4.0,
                validation="Review adoption-blueprint.md Level 3 criteria"
            ))

        # Sort gaps by priority (P0 first)
        priority_order = {"P0": 0, "P1": 1, "P2": 2}
        gaps.sort(key=lambda g: priority_order.get(g.priority, 3))

        # Calculate estimated effort
        total_effort = sum(g.estimated_hours for g in gaps)

        # Determine current level based on gaps
        has_p0_gaps = any(g.priority == "P0" for g in gaps)
        current_level = 1 if has_p0_gaps else 2

        duration = (datetime.now() - start_time).total_seconds()

        return EvaluationResult(
            sap_id=quick_result.sap_id,
            sap_name=sap_name,
            evaluation_type="deep",
            timestamp=start_time,
            is_installed=quick_result.is_installed,
            current_level=current_level,
            completion_percent=50.0 if current_level == 1 else 75.0,
            validation_results=quick_result.validation_results,
            gaps=gaps,
            blockers=[g.title for g in gaps if g.priority == "P0"],
            next_milestone=f"Level {current_level + 1}" if current_level < 3 else "Fully adopted",
            estimated_effort_hours=total_effort,
            duration_seconds=duration,
            confidence="high",  # Rule-based analysis is deterministic
            warnings=[]  # No warnings for Sprint 2
        )

    def strategic_analysis(self) -> AdoptionRoadmap:
        """
        Level 3: Comprehensive roadmap generation (30 minutes)

        Process:
        1. Quick check all installed SAPs
        2. Calculate aggregate metrics
        3. Analyze timeline (if history available)
        4. Identify cross-SAP dependencies
        5. Prioritize gaps globally
        6. Generate sprint breakdown
        7. Project ROI
        """
        start_time = datetime.now()

        # 1. Quick check all SAPs
        all_results = self.quick_check_all()

        # 2. Calculate aggregate metrics
        installed_results = [r for r in all_results if r.is_installed]
        total_installed = len(installed_results)

        level_distribution = {
            "level_0": sum(1 for r in all_results if r.current_level == 0),
            "level_1": sum(1 for r in all_results if r.current_level == 1),
            "level_2": sum(1 for r in all_results if r.current_level == 2),
            "level_3": sum(1 for r in all_results if r.current_level == 3)
        }

        avg_level = (
            sum(r.current_level for r in installed_results) / total_installed
            if total_installed > 0 else 0.0
        )

        # 3. Build roadmap (basic version for Sprint 1)
        roadmap = AdoptionRoadmap(
            generated_at=start_time,
            target_quarter=self.calculate_next_quarter(),
            total_saps_installed=total_installed,
            adoption_distribution=level_distribution,
            average_adoption_level=avg_level,
            total_hours_invested=0.0,  # Would track from events.jsonl
            priority_gaps=[],  # Would populate from gap analysis
            this_sprint=None,  # Would generate from prioritized gaps
            next_sprint=None,
            future_sprints=[]
        )

        return roadmap

    def calculate_next_quarter(self) -> str:
        """Calculate next quarter identifier (e.g., Q1-2026)"""
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        year = now.year

        # Next quarter
        next_q = quarter + 1
        next_year = year
        if next_q > 4:
            next_q = 1
            next_year += 1

        return f"Q{next_q}-{next_year}"


def format_quick_results(results: list[EvaluationResult] | EvaluationResult) -> str:
    """Format quick check results for terminal output"""
    if isinstance(results, EvaluationResult):
        results = [results]

    output = []
    output.append("SAP Adoption Status (Quick Check)")
    output.append("=" * 50)
    output.append("")

    installed = [r for r in results if r.is_installed]
    total_saps = len(results)
    total_installed = len(installed)

    output.append(f"Installed: {total_installed}/{total_saps} SAPs ({total_installed/total_saps*100:.0f}%)")
    output.append("")

    for result in results:
        if not result.is_installed:
            continue  # Skip uninstalled for quick summary

        status = "✅" if result.current_level > 0 else "❌"
        output.append(f"{status} {result.sap_id} ({result.sap_name})")
        output.append(f"   Level: {result.current_level}")
        output.append(f"   Next: {result.next_milestone}")
        if result.blockers:
            output.append(f"   Blockers: {', '.join(result.blockers)}")
        output.append("")

    return "\n".join(output)
