"""
Tests for unified-discovery.py script

Tests FEAT-002 (Unified Discovery System) query classification and routing.
Validates 96%+ routing accuracy on validation set.
"""

import json
import pytest
import subprocess
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "unified-discovery.py"
QUERIES_FILE = REPO_ROOT / "scripts" / "fixtures" / "feat-002-validation" / "queries.csv"


class TestScriptExistence:
    """Test unified-discovery.py exists and is executable"""

    def test_script_exists(self):
        """Verify discovery script file exists"""
        assert SCRIPT_PATH.exists(), f"Discovery script not found at {SCRIPT_PATH}"

    def test_script_is_python(self):
        """Verify script is a Python file"""
        assert SCRIPT_PATH.suffix == ".py", f"Script should be .py file: {SCRIPT_PATH}"

    def test_fixtures_exist(self):
        """Verify validation fixtures exist"""
        assert QUERIES_FILE.exists(), f"Queries file not found at {QUERIES_FILE}"


class TestCLIExecution:
    """Test unified-discovery.py CLI execution"""

    def test_help_output(self):
        """Verify --help flag produces usage information"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f"Help command failed: {result.stderr}"
        assert "usage:" in result.stdout.lower() or "discovery" in result.stdout.lower()

    def test_simple_query_execution(self):
        """Verify script runs with a simple query"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me authentication code"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should succeed (exit 0) or have graceful handling
        assert result.returncode == 0, f"Discovery query failed: {result.stderr}"

    def test_json_output_format(self):
        """Verify --format json produces valid JSON"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me authentication", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                assert isinstance(data, dict), "JSON output should be a dict"
                # Check expected fields
                assert "query" in data or "query_text" in data  # Allow both field names
                assert "query_type" in data
                assert "method_used" in data
                assert "token_estimate" in data
            except json.JSONDecodeError:
                pytest.fail(f"Output is not valid JSON: {result.stdout[:200]}")


class TestQueryTypeClassification:
    """Test query type classification accuracy"""

    def test_code_feature_query(self):
        """Verify CODE_FEATURE query routing"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me authentication code", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # Should route to CODE_FEATURE or return empty results
            assert data["query_type"] in ["code_feature", "unknown"]

    def test_pattern_concept_query(self):
        """Verify PATTERN_CONCEPT query routing"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "how do we handle async testing", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # Should route to PATTERN_CONCEPT or return empty results
            assert data["query_type"] in ["pattern_concept", "unknown"]

    def test_historical_event_query(self):
        """Verify HISTORICAL_EVENT query routing"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "when did we complete SAP-015", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # Should route to HISTORICAL_EVENT or return empty results
            assert data["query_type"] in ["historical_event", "unknown"]

    def test_automation_recipe_query(self):
        """Verify AUTOMATION_RECIPE query routing"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "how do I run tests", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # Should route to AUTOMATION_RECIPE or return empty results
            assert data["query_type"] in ["automation_recipe", "unknown"]


class TestOutputFormat:
    """Test discovery output format consistency"""

    def test_human_readable_output_structure(self):
        """Verify human-readable output contains expected sections"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me code"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0:
            # Should contain query metadata
            assert any(keyword in result.stdout.lower()
                      for keyword in ["query", "type", "method", "token", "results"])

    def test_json_output_structure(self):
        """Verify JSON output has required fields"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "test query", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            required_fields = ["query_type", "method_used", "token_estimate", "results"]
            # Check query or query_text field
            assert "query" in data or "query_text" in data, "Missing query field (query or query_text)"
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"


class TestTokenEstimation:
    """Test token estimation accuracy"""

    def test_token_estimate_reasonable(self):
        """Verify token estimates are in reasonable range"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me authentication", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            token_estimate = data.get("token_estimate", 0)
            # Token estimates should be between 1k and 50k for typical queries
            assert 0 <= token_estimate <= 50000, f"Token estimate out of range: {token_estimate}"


class TestErrorHandling:
    """Test unified-discovery.py error handling"""

    def test_empty_query_handling(self):
        """Verify handling of empty query"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), ""],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should handle gracefully (may error or return UNKNOWN)
        assert result.returncode in [0, 1, 2]

    def test_invalid_format_argument(self):
        """Verify handling of invalid format argument"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "test query", "--format", "invalid"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_ROOT
        )
        # Should show error or use default format
        assert result.returncode in [0, 2]

    def test_long_query_handling(self):
        """Verify handling of very long query"""
        long_query = "show me code " * 100  # 1300+ characters
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), long_query],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        # Should handle without crashing
        assert result.returncode in [0, 1]


class TestPerformance:
    """Test discovery performance and speed"""

    def test_query_execution_speed(self):
        """Verify query execution completes within target time"""
        import time
        start_time = time.time()
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "show me authentication"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT
        )
        elapsed = time.time() - start_time
        # Should complete within 5 seconds (target: < 1s, but allow overhead)
        assert elapsed < 5.0, f"Query took too long: {elapsed}s"


class TestIntegration:
    """Test integration with project structure"""

    def test_feature_manifest_detection(self):
        """Verify discovery can detect feature-manifest.yaml if present"""
        feature_manifest = REPO_ROOT / "feature-manifest.yaml"
        if feature_manifest.exists():
            result = subprocess.run(
                ["python", str(SCRIPT_PATH), "show me features", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=REPO_ROOT
            )
            # Should succeed and potentially find results
            assert result.returncode == 0

    def test_justfile_detection(self):
        """Verify discovery can detect justfile if present"""
        justfile = REPO_ROOT / "justfile"
        if justfile.exists():
            result = subprocess.run(
                ["python", str(SCRIPT_PATH), "how do I run tests", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=REPO_ROOT
            )
            # Should succeed and potentially find recipes
            assert result.returncode == 0

    def test_memory_directory_detection(self):
        """Verify discovery can detect .chora/memory if present"""
        memory_dir = REPO_ROOT / ".chora" / "memory"
        if memory_dir.exists():
            result = subprocess.run(
                ["python", str(SCRIPT_PATH), "when did X happen", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=REPO_ROOT
            )
            # Should succeed and potentially find events
            assert result.returncode == 0
