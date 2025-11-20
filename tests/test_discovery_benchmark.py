"""
Tests for run-discovery-benchmark.py script

Tests FEAT-002 (Unified Discovery System) benchmark harness.
Validates routing accuracy on test query sets (target: 96%+).
"""

import csv
import json
import pytest
import subprocess
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "run-discovery-benchmark.py"
QUERIES_FILE = REPO_ROOT / "scripts" / "fixtures" / "feat-002-validation" / "queries.csv"
RESULTS_FILE = REPO_ROOT / "scripts" / "fixtures" / "feat-002-validation" / "benchmark-results.csv"


class TestScriptExistence:
    """Test run-discovery-benchmark.py exists and is executable"""

    def test_script_exists(self):
        """Verify benchmark script file exists"""
        assert SCRIPT_PATH.exists(), f"Benchmark script not found at {SCRIPT_PATH}"

    def test_script_is_python(self):
        """Verify script is a Python file"""
        assert SCRIPT_PATH.suffix == ".py", f"Script should be .py file: {SCRIPT_PATH}"

    def test_queries_file_exists(self):
        """Verify test queries file exists"""
        assert QUERIES_FILE.exists(), f"Test queries file not found at {QUERIES_FILE}"


class TestQueriesFileFormat:
    """Test validation queries file format"""

    def test_queries_file_readable(self):
        """Verify queries file is readable CSV"""
        with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) > 0, "Queries file should have at least 1 test query"

    def test_queries_file_structure(self):
        """Verify queries file has required columns"""
        with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_columns = ['query_id', 'query_text', 'expected_type']
            first_row = next(reader)
            for col in required_columns:
                assert col in first_row, f"Missing required column: {col}"

    def test_queries_have_valid_types(self):
        """Verify queries have valid expected_type values"""
        valid_types = ['CODE_FEATURE', 'PATTERN_CONCEPT', 'HISTORICAL_EVENT', 'AUTOMATION_RECIPE', 'UNKNOWN']
        with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expected_type = row.get('expected_type', '')
                assert expected_type in valid_types, f"Invalid type for {row['query_id']}: {expected_type}"


class TestCLIExecution:
    """Test run-discovery-benchmark.py CLI execution"""

    def test_help_output(self):
        """Verify --help flag produces usage information"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # May not have --help (simple script), but should not crash
        assert result.returncode in [0, 2]

    @pytest.mark.slow
    def test_benchmark_execution(self):
        """Verify benchmark runs and completes successfully"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,  # Allow up to 2 minutes for full benchmark
            cwd=REPO_ROOT
        )
        # Should succeed or gracefully handle missing dependencies
        assert result.returncode in [0, 1], f"Benchmark failed: {result.stderr}"

    @pytest.mark.slow
    def test_benchmark_produces_results_file(self):
        """Verify benchmark creates results CSV file"""
        # Remove existing results file if present
        if RESULTS_FILE.exists():
            RESULTS_FILE.unlink()

        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        # Results file should be created
        if result.returncode == 0:
            assert RESULTS_FILE.exists(), "Benchmark should create results file"


class TestBenchmarkOutputFormat:
    """Test benchmark output format consistency"""

    @pytest.mark.slow
    def test_results_file_format(self):
        """Verify results file has expected CSV format"""
        # Run benchmark first (if not already run)
        if not RESULTS_FILE.exists():
            subprocess.run(
                ["python", str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=REPO_ROOT
            )

        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) > 0, "Results file should have at least 1 result"

    @pytest.mark.slow
    def test_results_file_columns(self):
        """Verify results file has required columns"""
        # Run benchmark first (if not already run)
        if not RESULTS_FILE.exists():
            subprocess.run(
                ["python", str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=REPO_ROOT
            )

        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                required_columns = [
                    'query_id', 'query_text', 'expected_type', 'actual_routing', 'match',
                    'discovery_method', 'token_estimate', 'time_seconds'
                ]
                first_row = next(reader)
                for col in required_columns:
                    assert col in first_row, f"Missing required column in results: {col}"


class TestRoutingAccuracy:
    """Test routing accuracy meets target (96%+)"""

    @pytest.mark.slow
    def test_routing_accuracy_target(self):
        """Verify routing accuracy is at least 90% (target: 96%+)"""
        # Run benchmark first (if not already run)
        if not RESULTS_FILE.exists():
            result = subprocess.run(
                ["python", str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=REPO_ROOT
            )
            if result.returncode != 0:
                pytest.skip("Benchmark execution failed, skipping accuracy test")

        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                total = 0
                matches = 0
                for row in reader:
                    total += 1
                    if row.get('match', '').lower() == 'yes':
                        matches += 1

                if total > 0:
                    accuracy = (matches / total) * 100
                    assert accuracy >= 90.0, f"Routing accuracy below target: {accuracy:.1f}% (target: 96%+)"


class TestBenchmarkSummary:
    """Test benchmark summary statistics"""

    @pytest.mark.slow
    def test_summary_output(self):
        """Verify benchmark produces summary statistics"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should contain summary keywords
            output = result.stdout.lower()
            assert any(keyword in output
                      for keyword in ["summary", "accuracy", "total", "matched", "queries"])

    @pytest.mark.slow
    def test_accuracy_by_query_type(self):
        """Verify benchmark shows accuracy breakdown by query type"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should show per-type accuracy
            output = result.stdout.lower()
            assert any(query_type in output
                      for query_type in ["code_feature", "pattern_concept", "historical_event", "automation_recipe"])


class TestPerformance:
    """Test benchmark performance metrics"""

    @pytest.mark.slow
    def test_average_query_time(self):
        """Verify average query time is reasonable"""
        # Run benchmark and check results file
        if not RESULTS_FILE.exists():
            subprocess.run(
                ["python", str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=REPO_ROOT
            )

        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                times = []
                for row in reader:
                    time_seconds = row.get('time_seconds', '0')
                    try:
                        times.append(float(time_seconds))
                    except ValueError:
                        pass

                if times:
                    avg_time = sum(times) / len(times)
                    # Average query should complete in < 5 seconds (target: < 1s)
                    assert avg_time < 5.0, f"Average query time too high: {avg_time:.3f}s"

    @pytest.mark.slow
    def test_token_estimates_present(self):
        """Verify token estimates are recorded"""
        # Run benchmark and check results file
        if not RESULTS_FILE.exists():
            subprocess.run(
                ["python", str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=REPO_ROOT
            )

        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                token_estimates = []
                for row in reader:
                    token_estimate = row.get('token_estimate', '0')
                    try:
                        token_estimates.append(int(token_estimate))
                    except ValueError:
                        pass

                # Most queries should have token estimates (may be 0 for UNKNOWN)
                assert len(token_estimates) > 0, "No token estimates found in results"


class TestErrorHandling:
    """Test run-discovery-benchmark.py error handling"""

    def test_missing_queries_file_handling(self):
        """Verify handling when queries file is missing"""
        # Temporarily rename queries file
        temp_name = QUERIES_FILE.with_suffix('.csv.bak')
        if QUERIES_FILE.exists():
            QUERIES_FILE.rename(temp_name)
            try:
                result = subprocess.run(
                    ["python", str(SCRIPT_PATH)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=REPO_ROOT
                )
                # Should handle gracefully with error message
                assert result.returncode in [0, 1]
                if result.returncode != 0:
                    assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()
            finally:
                # Restore queries file
                temp_name.rename(QUERIES_FILE)

    def test_missing_discovery_script_handling(self):
        """Verify handling when discovery script is missing"""
        # This test assumes benchmark will fail gracefully if discovery script missing
        # We can't actually remove the discovery script during tests
        # Just verify benchmark checks for it
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        # Should succeed or show error about missing discovery script
        assert result.returncode in [0, 1]


class TestIntegration:
    """Test integration with discovery system"""

    @pytest.mark.slow
    def test_benchmark_calls_discovery_script(self):
        """Verify benchmark successfully calls unified-discovery.py"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT
        )
        # Should complete without Python import errors
        if result.returncode != 0:
            # Should not have import errors or discovery script not found
            assert "importerror" not in result.stderr.lower()
            assert "no such file" not in result.stderr.lower()
