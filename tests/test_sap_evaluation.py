"""
Tests for utils/sap_evaluation.py - SAP Self-Evaluation Engine

This test suite covers:
- Data classes (Action, Gap, EvaluationResult, etc.)
- SAPEvaluator class methods
- Catalog loading and validation
- Installation checking
- Gap analysis
- Quick check, deep dive, and strategic analysis
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, date, timezone
from unittest.mock import Mock, patch, MagicMock
from dataclasses import asdict

from utils.sap_evaluation import (
    Action,
    Gap,
    EvaluationResult,
    PrioritizedGap,
    SprintPlan,
    AdoptionRoadmap,
    SAPEvaluator,
    format_quick_results
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_sap_artifacts(temp_workspace):
    """Create a mock SAP directory with required artifacts."""
    sap_dir = temp_workspace / "saps" / "SAP-004-testing-framework"
    sap_dir.mkdir(parents=True)

    artifacts = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]

    for artifact in artifacts:
        (sap_dir / artifact).write_text(f"# {artifact}\n\nMock content")

    return sap_dir


@pytest.fixture
def mock_catalog_with_location(temp_workspace, mock_sap_artifacts):
    """Create a mock catalog with SAP location metadata."""
    catalog = {
        "version": "1.0.0",
        "saps": [
            {
                "id": "SAP-004",
                "name": "testing-framework",
                "status": "active",
                "location": "saps/SAP-004-testing-framework"
            },
            {
                "id": "SAP-009",
                "name": "agent-awareness",
                "status": "active",
                "location": "saps/SAP-009-agent-awareness"
            }
        ]
    }

    catalog_file = temp_workspace / "sap-catalog.json"
    with open(catalog_file, 'w') as f:
        json.dump(catalog, f)

    return catalog_file


@pytest.fixture
def evaluator(temp_workspace, mock_catalog_with_location):
    """Create a SAPEvaluator instance with mock data."""
    return SAPEvaluator(repo_root=temp_workspace)


@pytest.fixture
def evaluator_no_catalog(temp_workspace):
    """Create a SAPEvaluator instance without a catalog."""
    # Don't create sap-catalog.json
    return SAPEvaluator(repo_root=temp_workspace)


# ============================================================================
# Data Class Tests
# ============================================================================

class TestDataClasses:
    """Test data classes and their serialization."""

    def test_action_creation(self):
        """Test Action dataclass creation."""
        action = Action(
            action_id="ACT-001",
            description="Write tests",
            tool="Write",
            file_path="tests/test_foo.py",
            rationale="Need test coverage",
            estimated_minutes=30
        )

        assert action.action_id == "ACT-001"
        assert action.description == "Write tests"
        assert action.tool == "Write"
        assert action.estimated_minutes == 30
        assert action.sequence == 1  # default value
        assert action.depends_on == []  # default factory

    def test_gap_creation(self):
        """Test Gap dataclass creation."""
        gap = Gap(
            gap_id="GAP-001",
            gap_type="quality",
            title="Low coverage",
            description="Coverage is below target",
            impact="high",
            effort="medium",
            priority="P0",
            urgency="blocks_sprint",
            estimated_hours=5.0
        )

        assert gap.gap_id == "GAP-001"
        assert gap.impact == "high"
        assert gap.priority == "P0"
        assert gap.estimated_hours == 5.0

    def test_evaluation_result_serialization(self):
        """Test EvaluationResult can be serialized to dict."""
        timestamp = datetime.now(timezone.utc)
        result = EvaluationResult(
            sap_id="SAP-004",
            sap_name="testing-framework",
            evaluation_type="quick",
            timestamp=timestamp,
            is_installed=True,
            current_level=1,
            completion_percent=33.3
        )

        result_dict = asdict(result)
        assert result_dict["sap_id"] == "SAP-004"
        assert result_dict["current_level"] == 1
        assert result_dict["is_installed"] is True

    def test_prioritized_gap_creation(self):
        """Test PrioritizedGap with nested Gap."""
        gap = Gap(
            gap_id="GAP-001",
            gap_type="quality",
            title="Test gap",
            description="Description",
            impact="high",
            effort="low",
            priority="P0",
            urgency="blocks_sprint"
        )

        prioritized = PrioritizedGap(
            rank=1,
            sap_id="SAP-004",
            gap=gap,
            priority_score=0.9,
            sprint="current"
        )

        assert prioritized.rank == 1
        assert prioritized.gap.gap_id == "GAP-001"
        assert prioritized.priority_score == 0.9

    def test_sprint_plan_creation(self):
        """Test SprintPlan dataclass."""
        plan = SprintPlan(
            sprint_name="Sprint 1",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 14),
            focus_saps=["SAP-004", "SAP-009"],
            total_estimated_hours=20.0
        )

        assert plan.sprint_name == "Sprint 1"
        assert len(plan.focus_saps) == 2
        assert plan.total_estimated_hours == 20.0

    def test_adoption_roadmap_creation(self):
        """Test AdoptionRoadmap dataclass."""
        roadmap = AdoptionRoadmap(
            generated_at=datetime.now(timezone.utc),
            target_quarter="Q1-2026",
            total_saps_installed=5,
            average_adoption_level=1.5
        )

        assert roadmap.target_quarter == "Q1-2026"
        assert roadmap.total_saps_installed == 5
        assert roadmap.average_adoption_level == 1.5


# ============================================================================
# SAPEvaluator Initialization Tests
# ============================================================================

class TestSAPEvaluatorInit:
    """Test SAPEvaluator initialization and catalog loading."""

    def test_init_with_catalog(self, evaluator):
        """Test initialization with valid catalog."""
        assert evaluator.repo_root is not None
        assert evaluator.catalog is not None
        assert len(evaluator.catalog) == 2
        assert "SAP-004" in evaluator.catalog

    def test_init_without_catalog(self, temp_workspace, capsys):
        """Test initialization without catalog file."""
        # Create evaluator inside test to capture stderr
        evaluator = SAPEvaluator(repo_root=temp_workspace)

        assert evaluator.catalog == {}

        # Check warning was printed
        captured = capsys.readouterr()
        assert "Warning: sap-catalog.json not found" in captured.err

    def test_load_catalog_array_format(self, temp_workspace):
        """Test loading catalog in array format."""
        catalog = [
            {"id": "SAP-001", "name": "test-sap-1"},
            {"id": "SAP-002", "name": "test-sap-2"}
        ]

        catalog_file = temp_workspace / "sap-catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(catalog, f)

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        assert len(evaluator.catalog) == 2
        assert evaluator.catalog["SAP-001"]["name"] == "test-sap-1"

    def test_load_catalog_object_with_saps_key(self, temp_workspace):
        """Test loading catalog in object format with 'saps' key."""
        catalog = {
            "version": "1.0.0",
            "saps": [
                {"id": "SAP-001", "name": "test-sap-1"},
                {"id": "SAP-002", "name": "test-sap-2"}
            ]
        }

        catalog_file = temp_workspace / "sap-catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(catalog, f)

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        assert len(evaluator.catalog) == 2

    def test_load_catalog_dict_format(self, temp_workspace):
        """Test loading catalog already in dict format."""
        catalog = {
            "SAP-001": {"name": "test-sap-1"},
            "SAP-002": {"name": "test-sap-2"}
        }

        catalog_file = temp_workspace / "sap-catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(catalog, f)

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        assert len(evaluator.catalog) == 2
        assert evaluator.catalog["SAP-001"]["name"] == "test-sap-1"


# ============================================================================
# Metadata and Installation Tests
# ============================================================================

class TestMetadataAndInstallation:
    """Test SAP metadata retrieval and installation checking."""

    def test_get_sap_metadata_exists(self, evaluator):
        """Test retrieving existing SAP metadata."""
        metadata = evaluator.get_sap_metadata("SAP-004")
        assert metadata is not None
        assert metadata["name"] == "testing-framework"

    def test_get_sap_metadata_not_exists(self, evaluator):
        """Test retrieving non-existent SAP metadata."""
        metadata = evaluator.get_sap_metadata("SAP-999")
        assert metadata is None

    def test_check_sap_installed_complete(self, evaluator, mock_sap_artifacts):
        """Test checking SAP with all artifacts present."""
        is_installed = evaluator.check_sap_installed("SAP-004")
        assert is_installed is True

    def test_check_sap_installed_missing_metadata(self, evaluator):
        """Test checking SAP not in catalog."""
        is_installed = evaluator.check_sap_installed("SAP-999")
        assert is_installed is False

    def test_check_sap_installed_no_location(self, temp_workspace):
        """Test checking SAP without location metadata."""
        catalog = {
            "saps": [
                {"id": "SAP-001", "name": "test-sap"}
                # No 'location' field
            ]
        }

        catalog_file = temp_workspace / "sap-catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(catalog, f)

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        is_installed = evaluator.check_sap_installed("SAP-001")
        assert is_installed is False

    def test_check_sap_installed_missing_directory(self, evaluator):
        """Test checking SAP when directory doesn't exist."""
        is_installed = evaluator.check_sap_installed("SAP-009")
        assert is_installed is False

    def test_check_sap_installed_missing_artifacts(self, temp_workspace):
        """Test checking SAP with incomplete artifacts."""
        # Create catalog
        catalog = {
            "saps": [
                {
                    "id": "SAP-004",
                    "name": "testing-framework",
                    "location": "saps/SAP-004-testing-framework"
                }
            ]
        }
        catalog_file = temp_workspace / "sap-catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(catalog, f)

        # Create directory but only some artifacts
        sap_dir = temp_workspace / "saps" / "SAP-004-testing-framework"
        sap_dir.mkdir(parents=True)
        (sap_dir / "capability-charter.md").write_text("content")
        (sap_dir / "protocol-spec.md").write_text("content")
        # Missing: awareness-guide.md, adoption-blueprint.md, ledger.md

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        is_installed = evaluator.check_sap_installed("SAP-004")
        assert is_installed is False


# ============================================================================
# Validation Command Tests
# ============================================================================

class TestValidationCommand:
    """Test running validation commands."""

    def test_run_validation_command_success(self, evaluator):
        """Test running successful validation command."""
        success, output = evaluator.run_validation_command("echo 'test'")
        assert success is True
        assert "test" in output

    def test_run_validation_command_failure(self, evaluator):
        """Test running failed validation command."""
        success, output = evaluator.run_validation_command("exit 1")
        assert success is False

    def test_run_validation_command_timeout(self, evaluator):
        """Test validation command timeout."""
        success, output = evaluator.run_validation_command("sleep 10", timeout=1)
        assert success is False
        assert "timed out" in output

    @patch('subprocess.run')
    def test_run_validation_command_exception(self, mock_run, evaluator):
        """Test validation command with exception."""
        mock_run.side_effect = Exception("Command error")

        success, output = evaluator.run_validation_command("some command")
        assert success is False
        assert "Command failed" in output


# ============================================================================
# Quick Check Tests
# ============================================================================

class TestQuickCheck:
    """Test quick_check functionality."""

    def test_quick_check_not_in_catalog(self, evaluator):
        """Test quick check for SAP not in catalog."""
        result = evaluator.quick_check("SAP-999")

        assert result.sap_id == "SAP-999"
        assert result.sap_name == "unknown"
        assert result.is_installed is False
        assert result.current_level == 0
        assert result.evaluation_type == "quick"
        assert len(result.warnings) == 1
        assert "not found in catalog" in result.warnings[0]

    def test_quick_check_installed(self, evaluator, mock_sap_artifacts):
        """Test quick check for installed SAP."""
        result = evaluator.quick_check("SAP-004")

        assert result.sap_id == "SAP-004"
        assert result.sap_name == "testing-framework"
        assert result.is_installed is True
        assert result.current_level == 1
        assert result.completion_percent == 33.3
        assert result.validation_results["installed"] is True
        assert result.confidence == "high"

    def test_quick_check_not_installed(self, evaluator):
        """Test quick check for non-installed SAP."""
        result = evaluator.quick_check("SAP-009")

        assert result.is_installed is False
        assert result.current_level == 0
        assert len(result.blockers) == 1
        assert "not installed" in result.blockers[0]

    def test_quick_check_all(self, evaluator, mock_sap_artifacts):
        """Test quick check for all SAPs in catalog."""
        results = evaluator.quick_check_all()

        assert len(results) == 2
        assert all(isinstance(r, EvaluationResult) for r in results)
        assert {r.sap_id for r in results} == {"SAP-004", "SAP-009"}


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestHelperFunctions:
    """Test helper functions."""

    def test_read_file_safe_exists(self, temp_workspace):
        """Test reading existing file safely."""
        test_file = temp_workspace / "test.txt"
        test_file.write_text("test content")

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        content = evaluator.read_file_safe(test_file)

        assert content == "test content"

    def test_read_file_safe_not_exists(self, temp_workspace):
        """Test reading non-existent file safely."""
        test_file = temp_workspace / "nonexistent.txt"

        evaluator = SAPEvaluator(repo_root=temp_workspace)
        content = evaluator.read_file_safe(test_file)

        assert content is None

    def test_count_lines(self, evaluator):
        """Test counting lines in content."""
        content = "line 1\nline 2\nline 3"
        count = evaluator.count_lines(content)
        assert count == 3

    def test_count_lines_none(self, evaluator):
        """Test counting lines with None content."""
        count = evaluator.count_lines(None)
        assert count == 0

    def test_count_lines_empty(self, evaluator):
        """Test counting lines with empty content."""
        count = evaluator.count_lines("")
        assert count == 0  # Empty string returns 0 (falsy check)

    def test_calculate_next_quarter_q1(self, evaluator):
        """Test calculating next quarter from Q1."""
        with patch('utils.sap_evaluation.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 15)
            next_q = evaluator.calculate_next_quarter()
            assert next_q == "Q2-2025"

    def test_calculate_next_quarter_q4(self, evaluator):
        """Test calculating next quarter from Q4."""
        with patch('utils.sap_evaluation.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 11, 15)
            next_q = evaluator.calculate_next_quarter()
            assert next_q == "Q1-2026"


# ============================================================================
# Gap Analysis Tests
# ============================================================================

class TestGapAnalysis:
    """Test SAP-specific gap analysis methods."""

    @patch.object(SAPEvaluator, 'run_validation_command')
    def test_analyze_sap_004_high_coverage(self, mock_cmd, evaluator):
        """Test SAP-004 analysis with high coverage (no gap)."""
        mock_cmd.return_value = (True, "TOTAL  90%")

        gaps = evaluator.analyze_sap_004_testing("SAP-004")
        assert len(gaps) == 0

    @patch.object(SAPEvaluator, 'run_validation_command')
    def test_analyze_sap_004_low_coverage(self, mock_cmd, evaluator):
        """Test SAP-004 analysis with low coverage (gap found)."""
        mock_cmd.return_value = (True, "TOTAL  50%")

        gaps = evaluator.analyze_sap_004_testing("SAP-004")
        assert len(gaps) == 1

        gap = gaps[0]
        assert gap.gap_id == "SAP-004-coverage"
        assert gap.gap_type == "quality"
        assert gap.priority == "P0"
        assert "50% < 85%" in gap.title
        assert gap.blocks == ["SAP-005"]

    def test_analyze_sap_009_short_agents_md(self, evaluator, temp_workspace):
        """Test SAP-009 analysis with short AGENTS.md."""
        agents_md = temp_workspace / "AGENTS.md"
        agents_md.write_text("\n".join(["line"] * 500))  # 500 lines

        gaps = evaluator.analyze_sap_009_awareness("SAP-009")

        # Should find gap for short file
        short_gap = [g for g in gaps if "too short" in g.title]
        assert len(short_gap) == 1
        assert short_gap[0].priority == "P1"

    def test_analyze_sap_009_no_domain_files(self, evaluator, temp_workspace):
        """Test SAP-009 analysis without domain-specific files."""
        gaps = evaluator.analyze_sap_009_awareness("SAP-009")

        # Should find gap for missing domain files
        domain_gap = [g for g in gaps if "domain-specific" in g.title]
        assert len(domain_gap) == 1
        assert domain_gap[0].priority == "P1"

    def test_analyze_sap_013_not_installed(self, evaluator, temp_workspace):
        """Test SAP-013 analysis when not installed."""
        # Don't create metrics file
        gaps = evaluator.analyze_sap_013_metrics("SAP-013")

        assert len(gaps) == 1
        gap = gaps[0]
        assert gap.gap_id == "SAP-013-not-installed"
        assert gap.priority == "P0"
        assert gap.urgency == "blocks_sprint"

    def test_analyze_sap_013_installed(self, evaluator, temp_workspace):
        """Test SAP-013 analysis when installed."""
        metrics_file = temp_workspace / "utils" / "claude_metrics.py"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        metrics_file.write_text("# metrics code")

        gaps = evaluator.analyze_sap_013_metrics("SAP-013")
        assert len(gaps) == 0

    def test_analyze_sap_generic_not_in_agents(self, evaluator, temp_workspace):
        """Test generic analysis when SAP not in AGENTS.md."""
        agents_md = temp_workspace / "AGENTS.md"
        agents_md.write_text("# Agents\n\nSome content")

        gaps = evaluator.analyze_sap_generic("SAP-999", "custom-sap")

        assert len(gaps) == 1
        gap = gaps[0]
        assert "not documented in AGENTS.md" in gap.title
        assert gap.priority == "P2"

    def test_analyze_sap_generic_in_agents(self, evaluator, temp_workspace):
        """Test generic analysis when SAP is in AGENTS.md."""
        agents_md = temp_workspace / "AGENTS.md"
        agents_md.write_text("# Agents\n\nUse custom-sap for testing")

        gaps = evaluator.analyze_sap_generic("SAP-999", "custom-sap")
        assert len(gaps) == 0


# ============================================================================
# Deep Dive Tests
# ============================================================================

class TestDeepDive:
    """Test deep_dive analysis."""

    def test_deep_dive_not_installed(self, evaluator):
        """Test deep dive for non-installed SAP returns quick check."""
        result = evaluator.deep_dive("SAP-009")

        assert result.evaluation_type == "quick"
        assert result.is_installed is False

    @patch.object(SAPEvaluator, 'run_validation_command')
    def test_deep_dive_sap_004(self, mock_cmd, evaluator, mock_sap_artifacts):
        """Test deep dive for SAP-004."""
        mock_cmd.return_value = (True, "TOTAL  50%")

        result = evaluator.deep_dive("SAP-004")

        assert result.evaluation_type == "deep"
        assert result.is_installed is True
        assert len(result.gaps) > 0
        assert result.current_level == 1  # Has P0 gap (low coverage)
        assert result.confidence == "high"

    def test_deep_dive_well_integrated(self, evaluator, temp_workspace, mock_sap_artifacts):
        """Test deep dive for well-integrated SAP."""
        # Create AGENTS.md with SAP mention
        agents_md = temp_workspace / "AGENTS.md"
        agents_md.write_text("\n".join(["line"] * 700) + "\ntesting-framework")

        # Create metrics file
        (temp_workspace / "utils").mkdir(exist_ok=True)
        (temp_workspace / "utils" / "claude_metrics.py").write_text("code")

        # Create tests directory with AGENTS.md
        tests_dir = temp_workspace / "tests"
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / "AGENTS.md").write_text("content")

        with patch.object(SAPEvaluator, 'run_validation_command') as mock_cmd:
            mock_cmd.return_value = (True, "TOTAL  90%")

            result = evaluator.deep_dive("SAP-004")

        # Should have "well-integrated" gap when no other gaps
        well_integrated_gap = [g for g in result.gaps if "well-integrated" in g.gap_id]
        assert len(well_integrated_gap) > 0
        assert result.current_level == 2  # No P0 gaps


# ============================================================================
# Strategic Analysis Tests
# ============================================================================

class TestStrategicAnalysis:
    """Test strategic_analysis roadmap generation."""

    def test_strategic_analysis_basic(self, evaluator, mock_sap_artifacts):
        """Test basic strategic analysis."""
        roadmap = evaluator.strategic_analysis()

        assert isinstance(roadmap, AdoptionRoadmap)
        assert roadmap.total_saps_installed >= 0
        assert roadmap.average_adoption_level >= 0
        assert "Q" in roadmap.target_quarter
        assert "-" in roadmap.target_quarter

    def test_strategic_analysis_level_distribution(self, evaluator, mock_sap_artifacts):
        """Test strategic analysis calculates level distribution."""
        roadmap = evaluator.strategic_analysis()

        dist = roadmap.adoption_distribution
        assert "level_0" in dist
        assert "level_1" in dist
        assert "level_2" in dist
        assert "level_3" in dist

        # Total should match catalog size
        total = sum(dist.values())
        assert total == len(evaluator.catalog)


# ============================================================================
# Format Output Tests
# ============================================================================

class TestFormatQuickResults:
    """Test format_quick_results output formatter."""

    def test_format_single_result(self):
        """Test formatting single EvaluationResult."""
        result = EvaluationResult(
            sap_id="SAP-004",
            sap_name="testing-framework",
            evaluation_type="quick",
            timestamp=datetime.now(timezone.utc),
            is_installed=True,
            current_level=1,
            next_milestone="Level 2"
        )

        output = format_quick_results(result)

        assert "SAP-004" in output
        assert "testing-framework" in output
        assert "Level: 1" in output
        assert "Next: Level 2" in output

    def test_format_multiple_results(self):
        """Test formatting multiple EvaluationResults."""
        results = [
            EvaluationResult(
                sap_id="SAP-004",
                sap_name="testing",
                evaluation_type="quick",
                timestamp=datetime.now(timezone.utc),
                is_installed=True,
                current_level=1
            ),
            EvaluationResult(
                sap_id="SAP-009",
                sap_name="awareness",
                evaluation_type="quick",
                timestamp=datetime.now(timezone.utc),
                is_installed=False,
                current_level=0
            )
        ]

        output = format_quick_results(results)

        assert "Installed: 1/2 SAPs" in output
        assert "SAP-004" in output
        # SAP-009 should not appear (not installed)
        assert "SAP-009" not in output

    def test_format_with_blockers(self):
        """Test formatting results with blockers."""
        result = EvaluationResult(
            sap_id="SAP-004",
            sap_name="testing",
            evaluation_type="quick",
            timestamp=datetime.now(timezone.utc),
            is_installed=True,
            current_level=1,
            blockers=["Low coverage", "Missing tests"]
        )

        output = format_quick_results(result)

        assert "Blockers:" in output
        assert "Low coverage" in output
