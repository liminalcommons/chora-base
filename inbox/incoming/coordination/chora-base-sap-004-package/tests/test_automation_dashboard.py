"""Tests for scripts/automation-dashboard.py"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Import automation-dashboard.py using importlib
repo_root = Path(__file__).parent.parent
automation_dashboard_path = repo_root / "scripts" / "automation-dashboard.py"
spec = importlib.util.spec_from_file_location("automation_dashboard", automation_dashboard_path)
automation_dashboard = importlib.util.module_from_spec(spec)
sys.modules['automation_dashboard'] = automation_dashboard
spec.loader.exec_module(automation_dashboard)

AutomationDashboard = automation_dashboard.AutomationDashboard
main = automation_dashboard.main
VERSION = automation_dashboard.VERSION


# Fixtures
@pytest.fixture
def tmp_workspace(tmp_path):
    """Create temporary workspace structure."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Create directories
    (workspace / "scripts").mkdir()
    (workspace / ".chora" / "metrics").mkdir(parents=True)

    return workspace


@pytest.fixture
def sample_justfile(tmp_workspace):
    """Create sample justfile."""
    justfile = tmp_workspace / "justfile"
    content = """# Sample justfile

# This is a comment
default:
    @just --list

# Build recipe
build:
    echo "Building..."

# Test recipe
test:
    pytest tests/

# Deploy recipe
deploy:
    echo "Deploying..."

_private-recipe:
    echo "Private"

# Another recipe
lint:
    ruff check .

format:
    ruff format .
"""
    justfile.write_text(content)
    return justfile


@pytest.fixture
def sample_usage_log(tmp_workspace):
    """Create sample usage log."""
    log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"

    entries = [
        {"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"},
        {"timestamp": "2025-11-02T10:00:00Z", "recipe": "test", "status": "success"},
        {"timestamp": "2025-11-03T10:00:00Z", "recipe": "build", "status": "success"},
        {"timestamp": "2025-11-04T10:00:00Z", "recipe": "lint", "status": "success"},
        {"timestamp": "2025-11-05T10:00:00Z", "recipe": "build", "status": "success"},
        {"timestamp": "2025-11-06T10:00:00Z", "recipe": "deploy", "status": "success"},
    ]

    with log_file.open('w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')

    return log_file


@pytest.fixture
def sample_scripts(tmp_workspace):
    """Create sample scripts."""
    scripts_dir = tmp_workspace / "scripts"

    # Python scripts
    (scripts_dir / "script1.py").write_text("#!/usr/bin/env python3\nprint('hello')")
    (scripts_dir / "script2.py").write_text("#!/usr/bin/env python3\nprint('world')")
    (scripts_dir / "script3.py").write_text("#!/usr/bin/env python3\nprint('test')")

    # Shell scripts
    (scripts_dir / "script1.sh").write_text("#!/bin/bash\necho 'hello'")
    (scripts_dir / "script2.sh").write_text("#!/bin/bash\necho 'world'")

    return scripts_dir


# Test AutomationDashboard initialization
class TestAutomationDashboardInit:
    def test_init_default_workspace(self):
        dashboard = AutomationDashboard()
        assert dashboard.workspace_root == Path.cwd()
        assert dashboard.justfile == Path.cwd() / "justfile"
        assert dashboard.scripts_dir == Path.cwd() / "scripts"

    def test_init_custom_workspace(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.workspace_root == tmp_workspace
        assert dashboard.justfile == tmp_workspace / "justfile"
        assert dashboard.scripts_dir == tmp_workspace / "scripts"


# Test counting methods
class TestCountMethods:
    def test_count_justfile_recipes(self, tmp_workspace, sample_justfile):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        # Should count: default, build, test, deploy, _private-recipe, lint, format = 7
        assert count == 7

    def test_count_justfile_recipes_no_file(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        assert count == 0

    def test_count_justfile_recipes_empty_file(self, tmp_workspace):
        justfile = tmp_workspace / "justfile"
        justfile.write_text("")
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        assert count == 0

    def test_count_justfile_recipes_only_comments(self, tmp_workspace):
        justfile = tmp_workspace / "justfile"
        justfile.write_text("# Comment 1\n# Comment 2\n")
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        assert count == 0

    def test_count_justfile_recipes_skip_indented(self, tmp_workspace):
        justfile = tmp_workspace / "justfile"
        justfile.write_text("recipe:\n\techo 'indented'\n    echo 'spaces'\n")
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        assert count == 1  # Only 'recipe:', indented lines are skipped

    def test_count_justfile_recipes_error_handling(self, tmp_workspace):
        # Create a directory instead of a file to trigger error
        justfile = tmp_workspace / "justfile"
        justfile.mkdir()
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_justfile_recipes()
        assert count == 0

    def test_count_python_scripts(self, tmp_workspace, sample_scripts):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_python_scripts()
        assert count == 3

    def test_count_python_scripts_no_directory(self, tmp_workspace):
        (tmp_workspace / "scripts").rmdir()
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_python_scripts()
        assert count == 0

    def test_count_shell_scripts(self, tmp_workspace, sample_scripts):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_shell_scripts()
        assert count == 2

    def test_count_shell_scripts_no_directory(self, tmp_workspace):
        (tmp_workspace / "scripts").rmdir()
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        count = dashboard.count_shell_scripts()
        assert count == 0


# Test usage statistics
class TestUsageStats:
    def test_get_recipe_usage_stats(self, tmp_workspace, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        assert stats["total_executions"] == 6
        assert stats["unique_recipes"] == 4  # build, test, lint, deploy
        assert len(stats["top_recipes"]) == 4
        assert stats["top_recipes"][0]["recipe"] == "build"
        assert stats["top_recipes"][0]["count"] == 3

    def test_get_recipe_usage_stats_no_log(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        assert stats["total_executions"] == 0
        assert stats["unique_recipes"] == 0
        assert stats["top_recipes"] == []

    def test_get_recipe_usage_stats_empty_log(self, tmp_workspace):
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        log_file.write_text("")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        assert stats["total_executions"] == 0
        assert stats["unique_recipes"] == 0
        assert stats["top_recipes"] == []

    def test_get_recipe_usage_stats_top_5_limit(self, tmp_workspace):
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"

        # Create 10 different recipes
        entries = []
        for i in range(10):
            for j in range(i + 1):  # Recipe 0: 1 exec, Recipe 1: 2 execs, etc.
                entries.append({
                    "timestamp": "2025-11-01T10:00:00Z",
                    "recipe": f"recipe{i}",
                    "status": "success"
                })

        with log_file.open('w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        assert len(stats["top_recipes"]) == 5  # Only top 5
        assert stats["top_recipes"][0]["recipe"] == "recipe9"  # Most executions (10)
        assert stats["top_recipes"][0]["count"] == 10

    def test_get_recipe_usage_stats_error_handling(self, tmp_workspace):
        # Create log file with malformed JSON
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        log_file.write_text("not valid json\n")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        # Should return empty stats on error
        assert stats["total_executions"] == 0
        assert stats["unique_recipes"] == 0
        assert stats["top_recipes"] == []

    def test_get_recipe_usage_stats_skip_empty_lines(self, tmp_workspace):
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        content = """{"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"}

{"timestamp": "2025-11-02T10:00:00Z", "recipe": "test", "status": "success"}
"""
        log_file.write_text(content)

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        stats = dashboard.get_recipe_usage_stats()

        assert stats["total_executions"] == 2


# Test scoring and maturity
class TestScoringAndMaturity:
    def test_calculate_automation_score_zero(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        assert score == 0

    def test_calculate_automation_score_recipes_only(self, tmp_workspace, sample_justfile):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # 7 recipes / 30 target * 40 points = 9.33 -> 9
        assert 9 <= score <= 10

    def test_calculate_automation_score_scripts_only(self, tmp_workspace, sample_scripts):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # 5 scripts / 10 target * 30 points = 15
        assert 14 <= score <= 16

    def test_calculate_automation_score_usage_only(self, tmp_workspace, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # 6 executions / 10 target * 30 points = 18
        assert 17 <= score <= 19

    def test_calculate_automation_score_full(self, tmp_workspace, sample_justfile, sample_scripts, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # Recipe score + script score + usage score
        # Should be 9 + 15 + 18 = 42
        assert 40 <= score <= 45

    def test_calculate_automation_score_max_recipes(self, tmp_workspace):
        justfile = tmp_workspace / "justfile"
        # Create 40 recipes (more than 30 target)
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(40)])
        justfile.write_text(content)

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # Recipe score capped at 40 points
        assert score == 40

    def test_calculate_automation_score_max_scripts(self, tmp_workspace):
        scripts_dir = tmp_workspace / "scripts"
        # Create 15 scripts (more than 10 target)
        for i in range(15):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # Script score capped at 30 points
        assert score == 30

    def test_calculate_automation_score_max_usage(self, tmp_workspace):
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        # Create 20 usage entries (more than 10 target)
        entries = [{"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"} for _ in range(20)]
        with log_file.open('w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        score = dashboard.calculate_automation_score()
        # Usage score capped at 30 points
        assert score == 30

    def test_get_maturity_level_minimal(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.get_maturity_level(0) == "Level 0 - Minimal"
        assert dashboard.get_maturity_level(29) == "Level 0 - Minimal"

    def test_get_maturity_level_basic(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.get_maturity_level(30) == "Level 1 - Basic"
        assert dashboard.get_maturity_level(49) == "Level 1 - Basic"

    def test_get_maturity_level_integrated(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.get_maturity_level(50) == "Level 2 - Integrated"
        assert dashboard.get_maturity_level(69) == "Level 2 - Integrated"

    def test_get_maturity_level_advanced(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.get_maturity_level(70) == "Level 2+ - Advanced"
        assert dashboard.get_maturity_level(89) == "Level 2+ - Advanced"

    def test_get_maturity_level_optimized(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        assert dashboard.get_maturity_level(90) == "Level 3 - Optimized"
        assert dashboard.get_maturity_level(100) == "Level 3 - Optimized"


# Test metrics generation
class TestGenerateMetrics:
    def test_generate_metrics(self, tmp_workspace, sample_justfile, sample_scripts, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()

        assert "generated_at" in metrics
        assert "automation_score" in metrics
        assert "recipes" in metrics
        assert "scripts" in metrics
        assert "usage" in metrics
        assert "maturity_level" in metrics

        # Check recipes
        assert metrics["recipes"]["total"] == 7
        assert metrics["recipes"]["target"] == 30
        assert metrics["recipes"]["percentage"] == 23  # 7/30 * 100 = 23.33 -> 23

        # Check scripts
        assert metrics["scripts"]["python"] == 3
        assert metrics["scripts"]["shell"] == 2
        assert metrics["scripts"]["total"] == 5
        assert metrics["scripts"]["target"] == 10

        # Check usage
        assert metrics["usage"]["total_executions"] == 6
        assert metrics["usage"]["unique_recipes"] == 4

        # Check timestamp format
        assert metrics["generated_at"].endswith('Z')
        assert 'T' in metrics["generated_at"]

    def test_generate_metrics_empty_workspace(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()

        assert metrics["automation_score"] == 0
        assert metrics["recipes"]["total"] == 0
        assert metrics["scripts"]["total"] == 0
        assert metrics["usage"]["total_executions"] == 0
        assert metrics["maturity_level"] == "Level 0 - Minimal"

    def test_generate_metrics_percentage_capped_at_100(self, tmp_workspace):
        justfile = tmp_workspace / "justfile"
        # Create 40 recipes (more than target of 30)
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(40)])
        justfile.write_text(content)

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()

        assert metrics["recipes"]["percentage"] == 100  # Capped at 100


# Test formatting
class TestFormatting:
    def test_create_progress_bar_zero(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        bar = dashboard.create_progress_bar(0)
        assert bar == "`[--------------------------------------------------]` 0%"

    def test_create_progress_bar_fifty(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        bar = dashboard.create_progress_bar(50)
        assert bar == "`[=========================-------------------------]` 50%"

    def test_create_progress_bar_hundred(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        bar = dashboard.create_progress_bar(100)
        assert bar == "`[==================================================]` 100%"

    def test_create_progress_bar_custom_width(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        bar = dashboard.create_progress_bar(50, width=10)
        assert bar == "`[=====-----]` 50%"

    def test_format_markdown(self, tmp_workspace, sample_justfile, sample_scripts, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        # Check YAML frontmatter
        assert markdown.startswith("---")
        assert "title: Automation Metrics Dashboard" in markdown
        assert "type: reference" in markdown
        assert "status: active" in markdown

        # Check main sections
        assert "# Automation Metrics Dashboard" in markdown
        assert "## Overall Automation Score" in markdown
        assert "## Recipe Coverage" in markdown
        assert "## Script Inventory" in markdown
        assert "## Usage Statistics" in markdown
        assert "## Maturity Targets" in markdown

        # Check metrics values
        assert "**Total Recipes:** 7" in markdown
        assert "**Python Scripts:** 3" in markdown
        assert "**Shell Scripts:** 2" in markdown
        assert "**Total Executions:** 6" in markdown

        # Check progress bar is included
        assert "`[" in markdown
        assert "]`" in markdown

        # Check footer
        assert "*This dashboard is auto-generated by `scripts/automation-dashboard.py`*" in markdown

    def test_format_markdown_with_top_recipes(self, tmp_workspace, sample_usage_log):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        # Check top recipes section
        assert "### Top 5 Most Used Recipes" in markdown
        assert "`build` - 3 executions" in markdown

    def test_format_markdown_without_top_recipes(self, tmp_workspace):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        # Should not have top recipes section when no usage
        assert "### Top 5 Most Used Recipes" not in markdown

    def test_format_markdown_recommendations_low_recipes(self, tmp_workspace):
        # Create justfile with only 5 recipes
        justfile = tmp_workspace / "justfile"
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(5)])
        justfile.write_text(content)

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "- Add 25 more recipes to reach target" in markdown

    def test_format_markdown_recommendations_low_scripts(self, tmp_workspace):
        # Create only 3 scripts
        scripts_dir = tmp_workspace / "scripts"
        for i in range(3):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "- Create 7 more utility scripts" in markdown

    def test_format_markdown_recommendations_low_usage(self, tmp_workspace):
        # Create usage log with only 5 executions
        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        entries = [{"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"} for _ in range(5)]
        with log_file.open('w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "- Increase automation usage through daily workflows" in markdown

    def test_format_markdown_recommendations_all_good(self, tmp_workspace):
        # Create workspace that meets all targets
        justfile = tmp_workspace / "justfile"
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(30)])
        justfile.write_text(content)

        scripts_dir = tmp_workspace / "scripts"
        for i in range(10):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        entries = [{"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"} for _ in range(15)]
        with log_file.open('w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "- Continue maintaining current automation standards" in markdown

    def test_format_markdown_status_level_3(self, tmp_workspace):
        # Create workspace with score >= 90
        justfile = tmp_workspace / "justfile"
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(40)])
        justfile.write_text(content)

        scripts_dir = tmp_workspace / "scripts"
        for i in range(15):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        log_file = tmp_workspace / ".chora" / "metrics" / "recipe-usage.jsonl"
        entries = [{"timestamp": "2025-11-01T10:00:00Z", "recipe": "build", "status": "success"} for _ in range(20)]
        with log_file.open('w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "**Status:** Achieved Level 3 - Fully Optimized" in markdown

    def test_format_markdown_status_level_2_plus(self, tmp_workspace):
        # Create workspace with score between 70-89
        # Need: recipes (40 max) + scripts (30 max) + usage (30 max) = 70-89
        # 30 recipes = 40 points, 10 scripts = 30 points, 0 usage = 70 points
        justfile = tmp_workspace / "justfile"
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(30)])
        justfile.write_text(content)

        scripts_dir = tmp_workspace / "scripts"
        for i in range(10):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "**Status:** Level 2+ - Advanced (Close to Level 3)" in markdown

    def test_format_markdown_status_level_2(self, tmp_workspace):
        # Create workspace with score between 50-69
        # Need 50-69 points: 25 recipes = 33 points, 10 scripts = 30 points = 63 points
        justfile = tmp_workspace / "justfile"
        content = "\n".join([f"recipe{i}:\n\techo 'test'" for i in range(25)])
        justfile.write_text(content)

        scripts_dir = tmp_workspace / "scripts"
        for i in range(10):
            (scripts_dir / f"script{i}.py").write_text(f"print({i})")

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "**Status:** Level 2 - Integrated (Making progress)" in markdown

    def test_format_markdown_status_level_1_or_below(self, tmp_workspace):
        # Create workspace with score < 50
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        metrics = dashboard.generate_metrics()
        markdown = dashboard.format_markdown(metrics)

        assert "**Status:** Level 1 or below (Needs improvement)" in markdown


# Test generate_dashboard
class TestGenerateDashboard:
    def test_generate_dashboard_markdown_stdout(self, tmp_workspace, sample_justfile, capsys):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard()

        captured = capsys.readouterr()
        assert "# Automation Metrics Dashboard" in captured.out
        assert "**Total Recipes:** 7" in captured.out

    def test_generate_dashboard_json_stdout(self, tmp_workspace, sample_justfile, capsys):
        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(format_type="json")

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert "automation_score" in output
        assert "recipes" in output
        assert output["recipes"]["total"] == 7

    def test_generate_dashboard_markdown_file(self, tmp_workspace, sample_justfile, capsys):
        output_file = tmp_workspace / "dashboard.md"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "# Automation Metrics Dashboard" in content

        captured = capsys.readouterr()
        assert f"Dashboard generated: {output_file}" in captured.out

    def test_generate_dashboard_json_file(self, tmp_workspace, sample_justfile):
        output_file = tmp_workspace / "dashboard.json"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file, format_type="json")

        assert output_file.exists()
        data = json.loads(output_file.read_text())
        assert "automation_score" in data

    def test_generate_dashboard_creates_parent_directory(self, tmp_workspace, sample_justfile):
        output_file = tmp_workspace / "subdir" / "nested" / "dashboard.md"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file)

        assert output_file.exists()
        assert output_file.parent.exists()


# Test main CLI
class TestMainCLI:
    def test_main_default(self, tmp_workspace, sample_justfile, capsys):
        with patch('sys.argv', ['automation-dashboard.py']):
            with patch('automation_dashboard.AutomationDashboard') as MockDashboard:
                mock_instance = MockDashboard.return_value

                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                MockDashboard.assert_called_once()
                mock_instance.generate_dashboard.assert_called_once_with(None, 'markdown')

    def test_main_with_output_file(self, tmp_workspace):
        output_file = tmp_workspace / "output.md"

        with patch('sys.argv', ['automation-dashboard.py', '--output', str(output_file)]):
            with patch('automation_dashboard.AutomationDashboard') as MockDashboard:
                mock_instance = MockDashboard.return_value

                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                mock_instance.generate_dashboard.assert_called_once_with(output_file, 'markdown')

    def test_main_with_json_format(self):
        with patch('sys.argv', ['automation-dashboard.py', '--format', 'json']):
            with patch('automation_dashboard.AutomationDashboard') as MockDashboard:
                mock_instance = MockDashboard.return_value

                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                mock_instance.generate_dashboard.assert_called_once_with(None, 'json')

    def test_main_with_all_options(self, tmp_workspace):
        output_file = tmp_workspace / "output.json"

        with patch('sys.argv', ['automation-dashboard.py', '--output', str(output_file), '--format', 'json']):
            with patch('automation_dashboard.AutomationDashboard') as MockDashboard:
                mock_instance = MockDashboard.return_value

                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0
                mock_instance.generate_dashboard.assert_called_once_with(output_file, 'json')

    def test_main_version(self):
        with patch('sys.argv', ['automation-dashboard.py', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_exits_zero(self):
        with patch('sys.argv', ['automation-dashboard.py']):
            with patch('automation_dashboard.AutomationDashboard'):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0


# Integration tests
class TestIntegration:
    def test_full_dashboard_generation_workflow(self, tmp_workspace, sample_justfile, sample_scripts, sample_usage_log):
        """Test complete workflow from initialization to dashboard generation."""
        output_file = tmp_workspace / "dashboard.md"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file)

        assert output_file.exists()
        content = output_file.read_text()

        # Verify complete dashboard structure
        assert "---" in content  # YAML frontmatter
        assert "# Automation Metrics Dashboard" in content
        assert "**Total Recipes:** 7" in content
        assert "**Python Scripts:** 3" in content
        assert "**Total Executions:** 6" in content
        assert "`build` - 3 executions" in content
        assert "*This dashboard is auto-generated" in content

    def test_json_export_import_workflow(self, tmp_workspace, sample_justfile, sample_scripts, sample_usage_log):
        """Test JSON export can be parsed correctly."""
        output_file = tmp_workspace / "metrics.json"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file, format_type="json")

        # Load and verify JSON structure
        data = json.loads(output_file.read_text())

        assert data["automation_score"] > 0
        assert data["recipes"]["total"] == 7
        assert data["scripts"]["total"] == 5
        assert data["usage"]["total_executions"] == 6
        assert data["maturity_level"] in ["Level 0 - Minimal", "Level 1 - Basic", "Level 2 - Integrated"]

    def test_empty_workspace_workflow(self, tmp_workspace):
        """Test dashboard generation for empty workspace."""
        output_file = tmp_workspace / "empty-dashboard.md"

        dashboard = AutomationDashboard(workspace_root=tmp_workspace)
        dashboard.generate_dashboard(output_path=output_file)

        content = output_file.read_text()

        assert "**Score:** 0/100" in content
        assert "**Maturity Level:** Level 0 - Minimal" in content
        assert "**Total Recipes:** 0" in content
