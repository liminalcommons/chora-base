"""
Test suite for utils/claude_metrics.py

Tests for ClaudeMetric data class and ClaudeROICalculator functionality.
"""

import json
import csv
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from utils.claude_metrics import ClaudeMetric, ClaudeROICalculator


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_metric():
    """Create a sample ClaudeMetric for testing."""
    return ClaudeMetric(
        session_id="session-001",
        timestamp=datetime(2025, 11, 5, 10, 0, 0),
        task_type="feature_implementation",
        lines_generated=250,
        time_saved_minutes=120,
        iterations_required=2,
        bugs_introduced=0,
        bugs_fixed=3,
        documentation_quality_score=8.5,
        test_coverage=0.92,
        metadata={"session_duration_minutes": 60}
    )


@pytest.fixture
def sample_metrics():
    """Create a list of sample metrics for testing."""
    return [
        ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature_implementation",
            lines_generated=250,
            time_saved_minutes=120,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=3,
            documentation_quality_score=8.5,
            test_coverage=0.92,
            metadata={"session_duration_minutes": 60}
        ),
        ClaudeMetric(
            session_id="session-002",
            timestamp=datetime(2025, 11, 5, 11, 0, 0),
            task_type="bugfix",
            lines_generated=50,
            time_saved_minutes=30,
            iterations_required=2,
            bugs_introduced=1,
            bugs_fixed=2,
            documentation_quality_score=7.0,
            test_coverage=0.85,
            metadata={"session_duration_minutes": 15}
        ),
        ClaudeMetric(
            session_id="session-003",
            timestamp=datetime(2025, 11, 5, 12, 0, 0),
            task_type="feature_implementation",
            lines_generated=300,
            time_saved_minutes=180,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=1,
            documentation_quality_score=9.0,
            test_coverage=0.95,
            metadata={"session_duration_minutes": 90}
        ),
    ]


@pytest.fixture
def calculator():
    """Create a ClaudeROICalculator for testing."""
    return ClaudeROICalculator(developer_hourly_rate=100.0)


# ============================================================================
# Test ClaudeMetric Data Class
# ============================================================================

class TestClaudeMetricCreation:
    """Test ClaudeMetric creation and initialization."""

    def test_create_metric_with_all_fields(self):
        """Test creating a metric with all fields."""
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature_implementation",
            lines_generated=250,
            time_saved_minutes=120,
            iterations_required=2,
            bugs_introduced=0,
            bugs_fixed=3,
            documentation_quality_score=8.5,
            test_coverage=0.92,
            metadata={"key": "value"}
        )

        assert metric.session_id == "session-001"
        assert metric.timestamp == datetime(2025, 11, 5, 10, 0, 0)
        assert metric.task_type == "feature_implementation"
        assert metric.lines_generated == 250
        assert metric.time_saved_minutes == 120
        assert metric.iterations_required == 2
        assert metric.bugs_introduced == 0
        assert metric.bugs_fixed == 3
        assert metric.documentation_quality_score == 8.5
        assert metric.test_coverage == 0.92
        assert metric.metadata == {"key": "value"}

    def test_create_metric_without_metadata(self):
        """Test creating a metric without metadata (default)."""
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="bugfix",
            lines_generated=50,
            time_saved_minutes=30,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=1,
            documentation_quality_score=7.0,
            test_coverage=0.80
        )

        assert metric.metadata == {}


class TestClaudeMetricValidation:
    """Test ClaudeMetric validation in __post_init__."""

    def test_validation_documentation_quality_too_high(self):
        """Test validation fails when documentation_quality_score > 10."""
        with pytest.raises(ValueError, match="documentation_quality_score must be between 0 and 10"):
            ClaudeMetric(
                session_id="session-001",
                timestamp=datetime(2025, 11, 5, 10, 0, 0),
                task_type="feature",
                lines_generated=100,
                time_saved_minutes=60,
                iterations_required=1,
                bugs_introduced=0,
                bugs_fixed=0,
                documentation_quality_score=11.0,
                test_coverage=0.8
            )

    def test_validation_documentation_quality_too_low(self):
        """Test validation fails when documentation_quality_score < 0."""
        with pytest.raises(ValueError, match="documentation_quality_score must be between 0 and 10"):
            ClaudeMetric(
                session_id="session-001",
                timestamp=datetime(2025, 11, 5, 10, 0, 0),
                task_type="feature",
                lines_generated=100,
                time_saved_minutes=60,
                iterations_required=1,
                bugs_introduced=0,
                bugs_fixed=0,
                documentation_quality_score=-1.0,
                test_coverage=0.8
            )

    def test_validation_test_coverage_too_high(self):
        """Test validation fails when test_coverage > 1."""
        with pytest.raises(ValueError, match="test_coverage must be between 0 and 1"):
            ClaudeMetric(
                session_id="session-001",
                timestamp=datetime(2025, 11, 5, 10, 0, 0),
                task_type="feature",
                lines_generated=100,
                time_saved_minutes=60,
                iterations_required=1,
                bugs_introduced=0,
                bugs_fixed=0,
                documentation_quality_score=8.0,
                test_coverage=1.5
            )

    def test_validation_test_coverage_too_low(self):
        """Test validation fails when test_coverage < 0."""
        with pytest.raises(ValueError, match="test_coverage must be between 0 and 1"):
            ClaudeMetric(
                session_id="session-001",
                timestamp=datetime(2025, 11, 5, 10, 0, 0),
                task_type="feature",
                lines_generated=100,
                time_saved_minutes=60,
                iterations_required=1,
                bugs_introduced=0,
                bugs_fixed=0,
                documentation_quality_score=8.0,
                test_coverage=-0.1
            )

    def test_validation_iterations_required_zero(self):
        """Test validation fails when iterations_required < 1."""
        with pytest.raises(ValueError, match="iterations_required must be at least 1"):
            ClaudeMetric(
                session_id="session-001",
                timestamp=datetime(2025, 11, 5, 10, 0, 0),
                task_type="feature",
                lines_generated=100,
                time_saved_minutes=60,
                iterations_required=0,
                bugs_introduced=0,
                bugs_fixed=0,
                documentation_quality_score=8.0,
                test_coverage=0.8
            )

    def test_validation_edge_cases_valid(self):
        """Test validation passes for edge cases (0, 1, 10)."""
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=0.0,  # Min valid
            test_coverage=1.0  # Max valid
        )
        assert metric.documentation_quality_score == 0.0
        assert metric.test_coverage == 1.0

        metric2 = ClaudeMetric(
            session_id="session-002",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=10.0,  # Max valid
            test_coverage=0.0  # Min valid
        )
        assert metric2.documentation_quality_score == 10.0
        assert metric2.test_coverage == 0.0


class TestClaudeMetricSerialization:
    """Test ClaudeMetric serialization (to_dict, from_dict)."""

    def test_to_dict(self, sample_metric):
        """Test converting metric to dictionary."""
        metric_dict = sample_metric.to_dict()

        assert metric_dict["session_id"] == "session-001"
        assert metric_dict["timestamp"] == "2025-11-05T10:00:00"
        assert metric_dict["task_type"] == "feature_implementation"
        assert metric_dict["lines_generated"] == 250
        assert metric_dict["time_saved_minutes"] == 120
        assert metric_dict["iterations_required"] == 2
        assert metric_dict["bugs_introduced"] == 0
        assert metric_dict["bugs_fixed"] == 3
        assert metric_dict["documentation_quality_score"] == 8.5
        assert metric_dict["test_coverage"] == 0.92
        assert metric_dict["metadata"] == {"session_duration_minutes": 60}

    def test_from_dict(self):
        """Test creating metric from dictionary."""
        metric_dict = {
            "session_id": "session-001",
            "timestamp": "2025-11-05T10:00:00",
            "task_type": "feature_implementation",
            "lines_generated": 250,
            "time_saved_minutes": 120,
            "iterations_required": 2,
            "bugs_introduced": 0,
            "bugs_fixed": 3,
            "documentation_quality_score": 8.5,
            "test_coverage": 0.92,
            "metadata": {"key": "value"}
        }

        metric = ClaudeMetric.from_dict(metric_dict)

        assert metric.session_id == "session-001"
        assert metric.timestamp == datetime(2025, 11, 5, 10, 0, 0)
        assert metric.task_type == "feature_implementation"
        assert metric.lines_generated == 250
        assert metric.time_saved_minutes == 120
        assert metric.iterations_required == 2
        assert metric.bugs_introduced == 0
        assert metric.bugs_fixed == 3
        assert metric.documentation_quality_score == 8.5
        assert metric.test_coverage == 0.92
        assert metric.metadata == {"key": "value"}

    def test_round_trip_serialization(self, sample_metric):
        """Test that to_dict -> from_dict preserves data."""
        metric_dict = sample_metric.to_dict()
        restored_metric = ClaudeMetric.from_dict(metric_dict)

        assert restored_metric.session_id == sample_metric.session_id
        assert restored_metric.timestamp == sample_metric.timestamp
        assert restored_metric.task_type == sample_metric.task_type
        assert restored_metric.lines_generated == sample_metric.lines_generated
        assert restored_metric.time_saved_minutes == sample_metric.time_saved_minutes
        assert restored_metric.iterations_required == sample_metric.iterations_required
        assert restored_metric.bugs_introduced == sample_metric.bugs_introduced
        assert restored_metric.bugs_fixed == sample_metric.bugs_fixed
        assert restored_metric.documentation_quality_score == sample_metric.documentation_quality_score
        assert restored_metric.test_coverage == sample_metric.test_coverage
        assert restored_metric.metadata == sample_metric.metadata


# ============================================================================
# Test ClaudeROICalculator Initialization
# ============================================================================

class TestClaudeROICalculatorInit:
    """Test ClaudeROICalculator initialization."""

    def test_init_with_hourly_rate(self):
        """Test initializing calculator with hourly rate."""
        calculator = ClaudeROICalculator(developer_hourly_rate=100.0)

        assert calculator.hourly_rate == 100.0
        assert calculator.metrics == []

    def test_init_with_different_rates(self):
        """Test initializing with different hourly rates."""
        calc1 = ClaudeROICalculator(developer_hourly_rate=75.0)
        calc2 = ClaudeROICalculator(developer_hourly_rate=150.0)

        assert calc1.hourly_rate == 75.0
        assert calc2.hourly_rate == 150.0

    def test_add_metric(self, calculator, sample_metric):
        """Test adding a metric to calculator."""
        calculator.add_metric(sample_metric)

        assert len(calculator.metrics) == 1
        assert calculator.metrics[0] == sample_metric

    def test_add_multiple_metrics(self, calculator, sample_metrics):
        """Test adding multiple metrics."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        assert len(calculator.metrics) == 3
        assert calculator.metrics[0].session_id == "session-001"
        assert calculator.metrics[1].session_id == "session-002"
        assert calculator.metrics[2].session_id == "session-003"


# ============================================================================
# Test Time Saved Calculations
# ============================================================================

class TestCalculateTimeSaved:
    """Test calculate_time_saved functionality."""

    def test_calculate_time_saved_no_metrics(self, calculator):
        """Test calculation with no metrics."""
        result = calculator.calculate_time_saved()

        assert result["hours_saved"] == 0.0
        assert result["cost_savings"] == 0.0
        assert result["average_acceleration"] == 0.0

    def test_calculate_time_saved_single_metric(self, calculator, sample_metric):
        """Test calculation with single metric."""
        calculator.add_metric(sample_metric)
        result = calculator.calculate_time_saved()

        # time_saved_minutes = 120, hourly_rate = 100
        assert result["hours_saved"] == 2.0
        assert result["cost_savings"] == 200.0
        # Has session_duration_minutes in metadata
        # manual_time = 60 + 120 = 180, acceleration = 180/60 = 3.0
        assert result["average_acceleration"] == 3.0

    def test_calculate_time_saved_multiple_metrics(self, calculator, sample_metrics):
        """Test calculation with multiple metrics."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        result = calculator.calculate_time_saved()

        # Total time saved: 120 + 30 + 180 = 330 minutes = 5.5 hours
        assert result["hours_saved"] == 5.5
        # Cost savings: 5.5 * 100 = 550
        assert result["cost_savings"] == 550.0

        # Accelerations:
        # session-001: manual=60+120=180, session=60, accel=3.0
        # session-002: manual=15+30=45, session=15, accel=3.0
        # session-003: manual=90+180=270, session=90, accel=3.0
        # Average: 3.0
        assert result["average_acceleration"] == 3.0

    def test_calculate_time_saved_without_session_duration(self, calculator):
        """Test calculation when metrics don't have session_duration_minutes."""
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=8.0,
            test_coverage=0.9,
            metadata={}  # No session_duration_minutes
        )

        calculator.add_metric(metric)
        result = calculator.calculate_time_saved()

        # Should use default acceleration of 2.0
        assert result["hours_saved"] == 1.0
        assert result["cost_savings"] == 100.0
        assert result["average_acceleration"] == 2.0

    def test_calculate_time_saved_mixed_metadata(self, calculator):
        """Test calculation with mixed metadata (some have duration, some don't)."""
        metric1 = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=8.0,
            test_coverage=0.9,
            metadata={"session_duration_minutes": 30}
        )
        metric2 = ClaudeMetric(
            session_id="session-002",
            timestamp=datetime(2025, 11, 5, 11, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=8.0,
            test_coverage=0.9,
            metadata={}  # No session_duration_minutes
        )

        calculator.add_metric(metric1)
        calculator.add_metric(metric2)
        result = calculator.calculate_time_saved()

        # Total time saved: 120 minutes = 2.0 hours
        assert result["hours_saved"] == 2.0
        assert result["cost_savings"] == 200.0

        # Only metric1 contributes to acceleration: (30+60)/30 = 3.0
        assert result["average_acceleration"] == 3.0


# ============================================================================
# Test Quality Metrics Calculations
# ============================================================================

class TestCalculateQualityMetrics:
    """Test calculate_quality_metrics functionality."""

    def test_calculate_quality_metrics_no_metrics(self, calculator):
        """Test calculation with no metrics."""
        result = calculator.calculate_quality_metrics()

        assert result["average_iterations"] == 0.0
        assert result["bug_introduction_rate"] == 0.0
        assert result["documentation_quality"] == 0.0
        assert result["test_coverage"] == 0.0
        assert result["first_pass_success_rate"] == 0.0

    def test_calculate_quality_metrics_single_metric(self, calculator, sample_metric):
        """Test calculation with single metric."""
        calculator.add_metric(sample_metric)
        result = calculator.calculate_quality_metrics()

        assert result["average_iterations"] == 2.0
        # Bug rate: 0 bugs / 250 lines * 1000 = 0.0
        assert result["bug_introduction_rate"] == 0.0
        assert result["documentation_quality"] == 8.5
        assert result["test_coverage"] == 0.92
        # First-pass success: 0/1 (iterations=2, not 1)
        assert result["first_pass_success_rate"] == 0.0

    def test_calculate_quality_metrics_multiple_metrics(self, calculator, sample_metrics):
        """Test calculation with multiple metrics."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        result = calculator.calculate_quality_metrics()

        # Average iterations: (1 + 2 + 1) / 3 = 1.333...
        assert abs(result["average_iterations"] - 1.333) < 0.01

        # Bug rate: 1 bug / 600 total lines * 1000 = 1.667 per 1000 LOC
        assert abs(result["bug_introduction_rate"] - 1.667) < 0.01

        # Documentation quality: (8.5 + 7.0 + 9.0) / 3 = 8.167
        assert abs(result["documentation_quality"] - 8.167) < 0.01

        # Test coverage: (0.92 + 0.85 + 0.95) / 3 = 0.907
        assert abs(result["test_coverage"] - 0.907) < 0.01

        # First-pass success: 2/3 (session-001 and session-003 have iterations=1)
        assert abs(result["first_pass_success_rate"] - 0.667) < 0.01

    def test_calculate_quality_metrics_zero_lines(self, calculator):
        """Test bug rate calculation when total lines is zero."""
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="refactor",
            lines_generated=0,
            time_saved_minutes=30,
            iterations_required=1,
            bugs_introduced=2,
            bugs_fixed=0,
            documentation_quality_score=5.0,
            test_coverage=0.5
        )

        calculator.add_metric(metric)
        result = calculator.calculate_quality_metrics()

        # Bug rate should be 0.0 when total_lines is 0
        assert result["bug_introduction_rate"] == 0.0


# ============================================================================
# Test Task Breakdown
# ============================================================================

class TestCalculateTaskBreakdown:
    """Test calculate_task_breakdown functionality."""

    def test_calculate_task_breakdown_no_metrics(self, calculator):
        """Test breakdown with no metrics."""
        result = calculator.calculate_task_breakdown()

        assert result == {}

    def test_calculate_task_breakdown_single_task_type(self, calculator, sample_metric):
        """Test breakdown with single task type."""
        calculator.add_metric(sample_metric)
        result = calculator.calculate_task_breakdown()

        assert "feature_implementation" in result
        breakdown = result["feature_implementation"]
        assert breakdown["count"] == 1
        assert breakdown["hours_saved"] == 2.0
        assert breakdown["average_iterations"] == 2.0
        assert breakdown["average_coverage"] == 0.92

    def test_calculate_task_breakdown_multiple_task_types(self, calculator, sample_metrics):
        """Test breakdown with multiple task types."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        result = calculator.calculate_task_breakdown()

        assert len(result) == 2
        assert "feature_implementation" in result
        assert "bugfix" in result

        # feature_implementation: 2 sessions (001, 003)
        feature_breakdown = result["feature_implementation"]
        assert feature_breakdown["count"] == 2
        # Hours saved: (120 + 180) / 60 = 5.0
        assert feature_breakdown["hours_saved"] == 5.0
        # Average iterations: (1 + 1) / 2 = 1.0
        assert feature_breakdown["average_iterations"] == 1.0
        # Average coverage: (0.92 + 0.95) / 2 = 0.935
        assert abs(feature_breakdown["average_coverage"] - 0.935) < 0.01

        # bugfix: 1 session (002)
        bugfix_breakdown = result["bugfix"]
        assert bugfix_breakdown["count"] == 1
        assert bugfix_breakdown["hours_saved"] == 0.5
        assert bugfix_breakdown["average_iterations"] == 2.0
        assert bugfix_breakdown["average_coverage"] == 0.85


# ============================================================================
# Test Report Generation
# ============================================================================

class TestGenerateReport:
    """Test generate_report functionality."""

    def test_generate_report_no_metrics(self, calculator):
        """Test report generation with no metrics."""
        report = calculator.generate_report()

        assert report == "No metrics tracked yet."

    def test_generate_report_single_metric(self, calculator, sample_metric):
        """Test report generation with single metric."""
        calculator.add_metric(sample_metric)
        report = calculator.generate_report()

        assert "Claude ROI Report" in report
        assert "Sessions Tracked: 1" in report
        assert "Hours saved: 2.0" in report
        assert "Cost savings: $200.00" in report
        assert "Acceleration factor: 3.0x" in report
        assert "Iterations per task: 2.0" in report
        assert "Bug rate: 0.00 per 1000 LOC" in report
        assert "Doc quality: 8.5/10" in report
        assert "Test coverage: 92.0%" in report

    def test_generate_report_multiple_metrics_single_task_type(self, calculator):
        """Test report with multiple metrics but single task type."""
        metric1 = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=60,
            iterations_required=1,
            bugs_introduced=0,
            bugs_fixed=0,
            documentation_quality_score=8.0,
            test_coverage=0.9
        )
        metric2 = ClaudeMetric(
            session_id="session-002",
            timestamp=datetime(2025, 11, 5, 11, 0, 0),
            task_type="feature",
            lines_generated=150,
            time_saved_minutes=90,
            iterations_required=2,
            bugs_introduced=1,
            bugs_fixed=1,
            documentation_quality_score=7.5,
            test_coverage=0.85
        )

        calculator.add_metric(metric1)
        calculator.add_metric(metric2)
        report = calculator.generate_report()

        assert "Sessions Tracked: 2" in report
        # Should NOT include task breakdown (only 1 task type)
        assert "Task Breakdown:" not in report

    def test_generate_report_multiple_task_types(self, calculator, sample_metrics):
        """Test report with multiple task types includes breakdown."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        report = calculator.generate_report()

        assert "Sessions Tracked: 3" in report
        assert "Task Breakdown:" in report
        assert "feature_implementation:" in report
        assert "bugfix:" in report
        assert "Sessions: 2" in report  # feature_implementation count
        assert "Sessions: 1" in report  # bugfix count


# ============================================================================
# Test Executive Summary
# ============================================================================

class TestGenerateExecutiveSummary:
    """Test generate_executive_summary functionality."""

    def test_generate_executive_summary_no_metrics(self, calculator):
        """Test executive summary with no metrics."""
        summary = calculator.generate_executive_summary()

        assert summary == "No metrics available for executive summary."

    def test_generate_executive_summary_basic(self, calculator, sample_metric):
        """Test executive summary with basic metrics."""
        calculator.add_metric(sample_metric)
        summary = calculator.generate_executive_summary()

        assert "EXECUTIVE SUMMARY: Claude AI Development Impact" in summary
        assert "INVESTMENT & RETURN" in summary
        assert "Claude Subscription: ~$20/month" in summary
        assert "Developer Savings: $200.00" in summary
        assert "Net Benefit: $180.00" in summary
        # ROI: (200-20)/20 * 100 = 900%
        assert "ROI: 900%" in summary

        assert "PRODUCTIVITY IMPACT" in summary
        assert "Sessions: 1" in summary
        assert "Time Saved: 2.0 hours" in summary
        assert "Acceleration: 3.0x faster than manual" in summary
        assert "Lines Generated: 250" in summary

        assert "QUALITY METRICS" in summary
        assert "First-Pass Success: 0%" in summary  # iterations=2, not 1
        assert "Average Iterations: 2.0" in summary
        assert "Bug Introduction Rate: 0.00 per 1000 LOC" in summary
        assert "Documentation Quality: 8.5/10" in summary
        assert "Test Coverage: 92%" in summary

        assert "TASK PERFORMANCE" in summary
        assert "feature_implementation: 1 sessions" in summary

        assert "RECOMMENDATIONS" in summary

    def test_generate_executive_summary_recommendations(self, calculator):
        """Test recommendation generation based on metrics."""
        # Create metrics that trigger all recommendations
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=30,
            iterations_required=5,  # > 3, triggers recommendation
            bugs_introduced=10,  # High bugs (100 per 1000 LOC), triggers recommendation
            bugs_fixed=0,
            documentation_quality_score=6.0,
            test_coverage=0.70,  # < 0.85, triggers recommendation
            metadata={"session_duration_minutes": 30}  # accel = (30+30)/30 = 2.0, ok
        )

        calculator.add_metric(metric)
        summary = calculator.generate_executive_summary()

        # First-pass success: 0% (iterations=5) triggers recommendation
        assert "Improve request clarity - first-pass success below 70%" in summary

        # Average iterations: 5.0 > 3, triggers recommendation
        assert "Provide more examples - high iteration count suggests unclear specs" in summary

        # Bug rate: 10/100 * 1000 = 100 per 1000 LOC > 5, triggers recommendation
        assert "Strengthen code review process - bug rate above industry average" in summary

        # Test coverage: 0.70 < 0.85, triggers recommendation
        assert "Emphasize test generation - coverage below target (85%)" in summary

    def test_generate_executive_summary_no_recommendations(self, calculator):
        """Test summary when all metrics are within target ranges."""
        # Create perfect metrics
        metrics = [
            ClaudeMetric(
                session_id=f"session-{i:03d}",
                timestamp=datetime(2025, 11, 5, 10 + i, 0, 0),
                task_type="feature",
                lines_generated=200,
                time_saved_minutes=120,
                iterations_required=1,  # First-pass success
                bugs_introduced=0,  # No bugs
                bugs_fixed=1,
                documentation_quality_score=9.0,
                test_coverage=0.95,  # > 0.85
                metadata={"session_duration_minutes": 30}  # accel = 5.0x
            )
            for i in range(3)
        ]

        for metric in metrics:
            calculator.add_metric(metric)

        summary = calculator.generate_executive_summary()

        assert "✅ All metrics within target ranges - continue current practices" in summary

    def test_generate_executive_summary_low_acceleration(self, calculator):
        """Test summary with low acceleration recommendation."""
        # Create metric with low acceleration (< 2.0)
        metric = ClaudeMetric(
            session_id="session-001",
            timestamp=datetime(2025, 11, 5, 10, 0, 0),
            task_type="feature",
            lines_generated=100,
            time_saved_minutes=30,
            iterations_required=1,  # Good first-pass
            bugs_introduced=0,  # No bugs
            bugs_fixed=0,
            documentation_quality_score=9.0,  # Good doc quality
            test_coverage=0.90,  # Good coverage
            metadata={"session_duration_minutes": 100}  # manual=(100+30)=130, accel=130/100=1.3 < 2.0
        )

        calculator.add_metric(metric)
        summary = calculator.generate_executive_summary()

        # Should trigger low acceleration recommendation
        assert "Review context management - acceleration below 2x may indicate inefficiency" in summary

    def test_generate_executive_summary_task_performance_sorting(self, calculator, sample_metrics):
        """Test that task performance is sorted by hours saved (descending)."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        summary = calculator.generate_executive_summary()

        # feature_implementation has more hours saved (5.0) than bugfix (0.5)
        # So it should appear first
        feature_pos = summary.find("feature_implementation")
        bugfix_pos = summary.find("bugfix")
        assert feature_pos < bugfix_pos


# ============================================================================
# Test Export Functionality
# ============================================================================

class TestExportToCSV:
    """Test export_to_csv functionality."""

    def test_export_to_csv_no_metrics(self, calculator, temp_workspace):
        """Test CSV export with no metrics."""
        csv_path = temp_workspace / "metrics.csv"
        calculator.export_to_csv(csv_path)

        # File should be created but empty (no data written)
        assert csv_path.exists()
        content = csv_path.read_text()
        assert content == ""

    def test_export_to_csv_single_metric(self, calculator, sample_metric, temp_workspace):
        """Test CSV export with single metric."""
        calculator.add_metric(sample_metric)
        csv_path = temp_workspace / "metrics.csv"
        calculator.export_to_csv(csv_path)

        assert csv_path.exists()

        # Read and verify CSV content
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1
        row = rows[0]
        assert row["session_id"] == "session-001"
        assert row["timestamp"] == "2025-11-05T10:00:00"
        assert row["task_type"] == "feature_implementation"
        assert row["lines_generated"] == "250"
        assert row["time_saved_minutes"] == "120"
        assert row["iterations_required"] == "2"
        assert row["bugs_introduced"] == "0"
        assert row["bugs_fixed"] == "3"
        assert row["documentation_quality_score"] == "8.5"
        assert row["test_coverage"] == "0.92"
        # metadata should not be in CSV
        assert "metadata" not in row

    def test_export_to_csv_multiple_metrics(self, calculator, sample_metrics, temp_workspace):
        """Test CSV export with multiple metrics."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        csv_path = temp_workspace / "metrics.csv"
        calculator.export_to_csv(csv_path)

        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 3
        assert rows[0]["session_id"] == "session-001"
        assert rows[1]["session_id"] == "session-002"
        assert rows[2]["session_id"] == "session-003"

    def test_export_to_csv_string_path(self, calculator, sample_metric, temp_workspace):
        """Test CSV export with string path instead of Path object."""
        calculator.add_metric(sample_metric)
        csv_path = str(temp_workspace / "metrics.csv")
        calculator.export_to_csv(csv_path)

        assert Path(csv_path).exists()


class TestExportToJSON:
    """Test export_to_json functionality."""

    def test_export_to_json_no_metrics(self, calculator, temp_workspace):
        """Test JSON export with no metrics."""
        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        assert json_path.exists()

        with open(json_path, 'r') as f:
            data = json.load(f)

        assert data["hourly_rate"] == 100.0
        assert data["metrics"] == []
        assert "summary" in data
        assert data["summary"]["time_saved"]["hours_saved"] == 0.0

    def test_export_to_json_single_metric(self, calculator, sample_metric, temp_workspace):
        """Test JSON export with single metric."""
        calculator.add_metric(sample_metric)
        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        assert json_path.exists()

        with open(json_path, 'r') as f:
            data = json.load(f)

        assert data["hourly_rate"] == 100.0
        assert len(data["metrics"]) == 1

        metric_data = data["metrics"][0]
        assert metric_data["session_id"] == "session-001"
        assert metric_data["task_type"] == "feature_implementation"
        assert metric_data["lines_generated"] == 250

        # Check summary
        assert "time_saved" in data["summary"]
        assert data["summary"]["time_saved"]["hours_saved"] == 2.0
        assert "quality" in data["summary"]
        assert "task_breakdown" in data["summary"]

    def test_export_to_json_multiple_metrics(self, calculator, sample_metrics, temp_workspace):
        """Test JSON export with multiple metrics."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        with open(json_path, 'r') as f:
            data = json.load(f)

        assert len(data["metrics"]) == 3
        assert data["summary"]["time_saved"]["hours_saved"] == 5.5

    def test_export_to_json_string_path(self, calculator, sample_metric, temp_workspace):
        """Test JSON export with string path instead of Path object."""
        calculator.add_metric(sample_metric)
        json_path = str(temp_workspace / "metrics.json")
        calculator.export_to_json(json_path)

        assert Path(json_path).exists()


class TestLoadFromJSON:
    """Test load_from_json class method."""

    def test_load_from_json_basic(self, calculator, sample_metrics, temp_workspace):
        """Test loading calculator from JSON file."""
        # First export
        for metric in sample_metrics:
            calculator.add_metric(metric)

        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        # Now load
        loaded_calculator = ClaudeROICalculator.load_from_json(json_path)

        assert loaded_calculator.hourly_rate == 100.0
        assert len(loaded_calculator.metrics) == 3
        assert loaded_calculator.metrics[0].session_id == "session-001"
        assert loaded_calculator.metrics[1].session_id == "session-002"
        assert loaded_calculator.metrics[2].session_id == "session-003"

    def test_load_from_json_preserves_calculations(self, calculator, sample_metrics, temp_workspace):
        """Test that loaded calculator produces same calculations as original."""
        for metric in sample_metrics:
            calculator.add_metric(metric)

        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        loaded_calculator = ClaudeROICalculator.load_from_json(json_path)

        # Compare calculations
        original_time = calculator.calculate_time_saved()
        loaded_time = loaded_calculator.calculate_time_saved()
        assert original_time == loaded_time

        original_quality = calculator.calculate_quality_metrics()
        loaded_quality = loaded_calculator.calculate_quality_metrics()
        assert original_quality == loaded_quality

        original_breakdown = calculator.calculate_task_breakdown()
        loaded_breakdown = loaded_calculator.calculate_task_breakdown()
        assert original_breakdown == loaded_breakdown

    def test_load_from_json_string_path(self, calculator, sample_metric, temp_workspace):
        """Test loading from JSON with string path instead of Path object."""
        calculator.add_metric(sample_metric)
        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        # Load using string path
        loaded_calculator = ClaudeROICalculator.load_from_json(str(json_path))

        assert loaded_calculator.hourly_rate == 100.0
        assert len(loaded_calculator.metrics) == 1

    def test_load_from_json_empty_metrics(self, calculator, temp_workspace):
        """Test loading JSON file with no metrics."""
        json_path = temp_workspace / "metrics.json"
        calculator.export_to_json(json_path)

        loaded_calculator = ClaudeROICalculator.load_from_json(json_path)

        assert loaded_calculator.hourly_rate == 100.0
        assert loaded_calculator.metrics == []
