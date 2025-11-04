"""Claude metrics tracking and ROI calculation.

This module provides utilities for tracking Claude's effectiveness and
calculating return on investment for AI-assisted development.

Example:
    >>> from {{ package_name }}.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator
    >>> calculator = ClaudeROICalculator(developer_hourly_rate=100)
    >>> metric = ClaudeMetric(
    ...     session_id="session-001",
    ...     timestamp=datetime.now(),
    ...     task_type="feature_implementation",
    ...     lines_generated=250,
    ...     time_saved_minutes=120,
    ...     iterations_required=2,
    ...     bugs_introduced=0,
    ...     bugs_fixed=3,
    ...     documentation_quality_score=8.5,
    ...     test_coverage=0.92
    ... )
    >>> calculator.add_metric(metric)
    >>> print(calculator.generate_report())
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import csv
import json
import statistics


@dataclass
class ClaudeMetric:
    """Track metrics for a single Claude interaction session.

    Attributes:
        session_id: Unique identifier for this session
        timestamp: When this session occurred
        task_type: Type of task (feature_implementation, bugfix, refactor, etc.)
        lines_generated: Number of lines of code generated
        time_saved_minutes: Time saved vs manual implementation (minutes)
        iterations_required: Number of iterations needed to complete
        bugs_introduced: Number of bugs introduced by Claude's code
        bugs_fixed: Number of bugs fixed by Claude
        documentation_quality_score: Quality rating (1-10) of generated documentation
        test_coverage: Test coverage percentage (0.0-1.0)
        metadata: Optional additional metadata (JSON-serializable dict)
    """

    session_id: str
    timestamp: datetime
    task_type: str
    lines_generated: int
    time_saved_minutes: int
    iterations_required: int
    bugs_introduced: int
    bugs_fixed: int
    documentation_quality_score: float
    test_coverage: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metric values."""
        if not 0 <= self.documentation_quality_score <= 10:
            raise ValueError("documentation_quality_score must be between 0 and 10")
        if not 0 <= self.test_coverage <= 1:
            raise ValueError("test_coverage must be between 0 and 1")
        if self.iterations_required < 1:
            raise ValueError("iterations_required must be at least 1")

    def to_dict(self) -> dict[str, Any]:
        """Convert metric to dictionary for serialization.

        Returns:
            Dictionary representation of the metric
        """
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "task_type": self.task_type,
            "lines_generated": self.lines_generated,
            "time_saved_minutes": self.time_saved_minutes,
            "iterations_required": self.iterations_required,
            "bugs_introduced": self.bugs_introduced,
            "bugs_fixed": self.bugs_fixed,
            "documentation_quality_score": self.documentation_quality_score,
            "test_coverage": self.test_coverage,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClaudeMetric":
        """Create metric from dictionary.

        Args:
            data: Dictionary representation of metric

        Returns:
            ClaudeMetric instance
        """
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


@dataclass
class SAPAdoptionMetric:
    """Track SAP adoption progress for ROI analysis.

    Attributes:
        sap_id: SAP identifier (e.g., "SAP-004")
        adoption_level: Current adoption level (0-3)
        hours_invested: Total hours spent adopting this SAP
        estimated_hours_saved: Estimated productivity hours saved per quarter
        timestamp: When this metric was recorded
        metadata: Optional additional metadata
    """
    sap_id: str
    adoption_level: int
    hours_invested: float
    estimated_hours_saved: float
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metric values."""
        if not 0 <= self.adoption_level <= 3:
            raise ValueError("adoption_level must be between 0 and 3")
        if self.hours_invested < 0:
            raise ValueError("hours_invested must be non-negative")
        if self.estimated_hours_saved < 0:
            raise ValueError("estimated_hours_saved must be non-negative")


class ClaudeROICalculator:
    """Calculate return on investment for Claude usage.

    This calculator tracks metrics across multiple Claude sessions and
    provides analytics on time savings, quality improvements, and ROI.

    Example:
        >>> calculator = ClaudeROICalculator(developer_hourly_rate=100)
        >>> # Add metrics from sessions
        >>> calculator.add_metric(metric1)
        >>> calculator.add_metric(metric2)
        >>> # Generate report
        >>> print(calculator.generate_report())
        >>> # Export to CSV
        >>> calculator.export_to_csv("metrics.csv")
    """

    def __init__(self, developer_hourly_rate: float):
        """Initialize ROI calculator.

        Args:
            developer_hourly_rate: Developer's hourly rate in dollars
        """
        self.hourly_rate = developer_hourly_rate
        self.metrics: list[ClaudeMetric] = []
        self.sap_adoption_metrics: list[SAPAdoptionMetric] = []

    def add_metric(self, metric: ClaudeMetric) -> None:
        """Add a metric to the calculator.

        Args:
            metric: ClaudeMetric to track
        """
        self.metrics.append(metric)

    def calculate_time_saved(self) -> dict[str, float]:
        """Calculate time and cost savings metrics.

        Returns:
            Dictionary with hours_saved, cost_savings, and acceleration_factor
        """
        if not self.metrics:
            return {
                "hours_saved": 0.0,
                "cost_savings": 0.0,
                "average_acceleration": 0.0,
            }

        total_time_saved = sum(m.time_saved_minutes for m in self.metrics)
        hours_saved = total_time_saved / 60
        cost_savings = hours_saved * self.hourly_rate

        # Calculate acceleration factor
        # Acceleration = (manual_time) / (claude_time)
        # manual_time = claude_time + time_saved
        # For simplicity, assume claude_time = time_saved / 2 (meaning 2x faster)
        # More accurate: track actual session duration
        average_acceleration = 2.0  # Default assumption
        if self.metrics and "session_duration_minutes" in self.metrics[0].metadata:
            accelerations = []
            for m in self.metrics:
                session_duration = m.metadata.get("session_duration_minutes", 0)
                if session_duration > 0:
                    manual_time = session_duration + m.time_saved_minutes
                    acceleration = manual_time / session_duration
                    accelerations.append(acceleration)
            if accelerations:
                average_acceleration = statistics.mean(accelerations)

        return {
            "hours_saved": hours_saved,
            "cost_savings": cost_savings,
            "average_acceleration": average_acceleration,
        }

    def calculate_quality_metrics(self) -> dict[str, float]:
        """Calculate quality-related metrics.

        Returns:
            Dictionary with quality metrics
        """
        if not self.metrics:
            return {
                "average_iterations": 0.0,
                "bug_introduction_rate": 0.0,
                "documentation_quality": 0.0,
                "test_coverage": 0.0,
                "first_pass_success_rate": 0.0,
            }

        total_iterations = sum(m.iterations_required for m in self.metrics)
        total_lines = sum(m.lines_generated for m in self.metrics)
        total_bugs = sum(m.bugs_introduced for m in self.metrics)

        # Bug rate per 1000 lines
        bug_rate = (total_bugs / total_lines * 1000) if total_lines > 0 else 0.0

        # First-pass success rate (1 iteration = success)
        first_pass_successes = sum(1 for m in self.metrics if m.iterations_required == 1)
        first_pass_rate = (
            first_pass_successes / len(self.metrics) if self.metrics else 0.0
        )

        return {
            "average_iterations": total_iterations / len(self.metrics),
            "bug_introduction_rate": bug_rate,
            "documentation_quality": statistics.mean(
                m.documentation_quality_score for m in self.metrics
            ),
            "test_coverage": statistics.mean(m.test_coverage for m in self.metrics),
            "first_pass_success_rate": first_pass_rate,
        }

    def calculate_task_breakdown(self) -> dict[str, dict[str, Any]]:
        """Calculate metrics broken down by task type.

        Returns:
            Dictionary mapping task_type to metrics for that type
        """
        task_types: dict[str, list[ClaudeMetric]] = {}
        for metric in self.metrics:
            if metric.task_type not in task_types:
                task_types[metric.task_type] = []
            task_types[metric.task_type].append(metric)

        breakdown = {}
        for task_type, metrics in task_types.items():
            total_time_saved = sum(m.time_saved_minutes for m in metrics)
            breakdown[task_type] = {
                "count": len(metrics),
                "hours_saved": total_time_saved / 60,
                "average_iterations": statistics.mean(
                    m.iterations_required for m in metrics
                ),
                "average_coverage": statistics.mean(m.test_coverage for m in metrics),
            }

        return breakdown

    def generate_report(self) -> str:
        """Generate executive summary report.

        Returns:
            Formatted report string
        """
        if not self.metrics:
            return "No metrics tracked yet."

        time_metrics = self.calculate_time_saved()
        quality_metrics = self.calculate_quality_metrics()

        report = f"""
Claude ROI Report
=================

Sessions Tracked: {len(self.metrics)}

Time & Cost Savings:
- Hours saved: {time_metrics['hours_saved']:.1f}
- Cost savings: ${time_metrics['cost_savings']:.2f}
- Acceleration factor: {time_metrics['average_acceleration']:.1f}x

Quality Metrics:
- Iterations per task: {quality_metrics['average_iterations']:.1f}
- Bug rate: {quality_metrics['bug_introduction_rate']:.2f} per 1000 LOC
- Doc quality: {quality_metrics['documentation_quality']:.1f}/10
- Test coverage: {quality_metrics['test_coverage']:.1%}
- First-pass success: {quality_metrics['first_pass_success_rate']:.1%}
"""

        # Add task breakdown if multiple task types
        breakdown = self.calculate_task_breakdown()
        if len(breakdown) > 1:
            report += "\nTask Breakdown:\n"
            for task_type, metrics in breakdown.items():
                report += f"  {task_type}:\n"
                report += f"    Sessions: {metrics['count']}\n"
                report += f"    Hours saved: {metrics['hours_saved']:.1f}\n"
                report += f"    Avg iterations: {metrics['average_iterations']:.1f}\n"

        return report

    def generate_executive_summary(self) -> str:
        """Generate detailed executive summary with recommendations.

        Returns:
            Formatted executive summary
        """
        if not self.metrics:
            return "No metrics available for executive summary."

        time_metrics = self.calculate_time_saved()
        quality_metrics = self.calculate_quality_metrics()
        breakdown = self.calculate_task_breakdown()

        # Calculate ROI percentage (assuming monthly Claude subscription cost)
        claude_cost_monthly = 20  # Approximate Claude Pro cost
        monthly_savings = time_metrics["cost_savings"]
        roi_percentage = (
            ((monthly_savings - claude_cost_monthly) / claude_cost_monthly * 100)
            if claude_cost_monthly > 0
            else 0
        )

        summary = f"""
EXECUTIVE SUMMARY: Claude AI Development Impact
================================================

INVESTMENT & RETURN
-------------------
Claude Subscription: ~${claude_cost_monthly}/month
Developer Savings: ${monthly_savings:.2f}
Net Benefit: ${monthly_savings - claude_cost_monthly:.2f}
ROI: {roi_percentage:.0f}%

PRODUCTIVITY IMPACT
-------------------
Sessions: {len(self.metrics)}
Time Saved: {time_metrics['hours_saved']:.1f} hours
Acceleration: {time_metrics['average_acceleration']:.1f}x faster than manual
Lines Generated: {sum(m.lines_generated for m in self.metrics):,}

QUALITY METRICS
---------------
First-Pass Success: {quality_metrics['first_pass_success_rate']:.0%}
Average Iterations: {quality_metrics['average_iterations']:.1f}
Bug Introduction Rate: {quality_metrics['bug_introduction_rate']:.2f} per 1000 LOC
Documentation Quality: {quality_metrics['documentation_quality']:.1f}/10
Test Coverage: {quality_metrics['test_coverage']:.0%}

TASK PERFORMANCE
----------------
"""
        for task_type, metrics in sorted(
            breakdown.items(), key=lambda x: x[1]["hours_saved"], reverse=True
        ):
            summary += f"{task_type}: {metrics['count']} sessions, "
            summary += f"{metrics['hours_saved']:.1f} hours saved\n"

        summary += f"""
RECOMMENDATIONS
---------------
"""
        # Generate recommendations based on metrics
        recommendations = []

        if quality_metrics["first_pass_success_rate"] < 0.7:
            recommendations.append(
                "• Improve request clarity - first-pass success below 70%"
            )

        if quality_metrics["average_iterations"] > 3:
            recommendations.append(
                "• Provide more examples - high iteration count suggests unclear specs"
            )

        if quality_metrics["bug_introduction_rate"] > 5:
            recommendations.append(
                "• Strengthen code review process - bug rate above industry average"
            )

        if quality_metrics["test_coverage"] < 0.85:
            recommendations.append(
                "• Emphasize test generation - coverage below target (85%)"
            )

        if time_metrics["average_acceleration"] < 2.0:
            recommendations.append(
                "• Review context management - acceleration below 2x may indicate inefficiency"
            )

        if recommendations:
            summary += "\n".join(recommendations)
        else:
            summary += "✅ All metrics within target ranges - continue current practices"

        return summary

    def track_sap_adoption(self, metric: SAPAdoptionMetric) -> None:
        """Add SAP adoption metric to ROI tracking.

        Args:
            metric: SAPAdoptionMetric to track
        """
        self.sap_adoption_metrics.append(metric)

    def generate_sap_adoption_report(self) -> str:
        """Generate SAP adoption ROI analysis.

        Returns:
            Formatted report string showing SAP adoption ROI
        """
        if not self.sap_adoption_metrics:
            return "## SAP Adoption ROI\n\nNo SAP adoption metrics tracked yet."

        total_invested = sum(m.hours_invested for m in self.sap_adoption_metrics)
        total_saved = sum(m.estimated_hours_saved for m in self.sap_adoption_metrics)
        roi = total_saved / total_invested if total_invested > 0 else 0

        avg_level = (
            sum(m.adoption_level for m in self.sap_adoption_metrics) /
            len(self.sap_adoption_metrics)
        )

        # Calculate distribution
        level_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for m in self.sap_adoption_metrics:
            level_counts[m.adoption_level] += 1

        report = f"""## SAP Adoption ROI

**Investment**: {total_invested:.1f} hours (SAP learning & integration)
**Return**: {total_saved:.1f} hours/quarter (productivity gains from SAPs)
**ROI**: {roi:.2f}x

**Adopted SAPs**: {len(self.sap_adoption_metrics)}
**Average Level**: {avg_level:.1f}

**Distribution by Level**:
- Level 0 (Not started): {level_counts[0]} SAPs
- Level 1 (Basic capability): {level_counts[1]} SAPs
- Level 2 (Standard usage): {level_counts[2]} SAPs
- Level 3 (Fully automated): {level_counts[3]} SAPs

**Top SAPs by ROI**:
"""
        # Sort by ROI (hours_saved / hours_invested)
        sap_rois = [
            (m.sap_id, m.estimated_hours_saved / m.hours_invested if m.hours_invested > 0 else 0)
            for m in self.sap_adoption_metrics
        ]
        sap_rois.sort(key=lambda x: x[1], reverse=True)

        for sap_id, sap_roi in sap_rois[:5]:
            report += f"- {sap_id}: {sap_roi:.2f}x\n"

        return report

    def export_to_csv(self, filepath: str | Path) -> None:
        """Export metrics to CSV file.

        Args:
            filepath: Path to CSV file to create/overwrite
        """
        filepath = Path(filepath)

        with filepath.open("w", newline="") as f:
            if not self.metrics:
                return

            fieldnames = [
                "session_id",
                "timestamp",
                "task_type",
                "lines_generated",
                "time_saved_minutes",
                "iterations_required",
                "bugs_introduced",
                "bugs_fixed",
                "documentation_quality_score",
                "test_coverage",
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for metric in self.metrics:
                row = metric.to_dict()
                # Remove metadata for CSV export
                row.pop("metadata", None)
                writer.writerow(row)

    def export_to_json(self, filepath: str | Path) -> None:
        """Export metrics to JSON file.

        Args:
            filepath: Path to JSON file to create/overwrite
        """
        filepath = Path(filepath)

        with filepath.open("w") as f:
            data = {
                "hourly_rate": self.hourly_rate,
                "metrics": [m.to_dict() for m in self.metrics],
                "summary": {
                    "time_saved": self.calculate_time_saved(),
                    "quality": self.calculate_quality_metrics(),
                    "task_breakdown": self.calculate_task_breakdown(),
                },
            }
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str | Path) -> "ClaudeROICalculator":
        """Load calculator from JSON file.

        Args:
            filepath: Path to JSON file to load

        Returns:
            ClaudeROICalculator with loaded metrics
        """
        filepath = Path(filepath)

        with filepath.open("r") as f:
            data = json.load(f)

        calculator = cls(developer_hourly_rate=data["hourly_rate"])
        for metric_data in data["metrics"]:
            calculator.add_metric(ClaudeMetric.from_dict(metric_data))

        return calculator
