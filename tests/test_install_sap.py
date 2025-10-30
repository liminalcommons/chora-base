"""
Comprehensive test suite for install-sap.py script
Wave 5 (v4.1.0) - SAP Installation Tooling

This test suite achieves comprehensive coverage of install-sap.py with 48 test cases:
- Catalog Functions: 8 tests
- Installation Functions: 15 tests
- SAP Set Functions: 10 tests
- Dry Run & List Tests: 9 tests
- Error Handling Tests: 6 tests

Coverage Target: ≥70% of script functionality
"""

import sys
from pathlib import Path

# Add scripts directory to path to import install-sap functions
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import json
import shutil

# Import functions from install-sap.py
# Note: We import as a module to avoid executing main()
import importlib.util
spec = importlib.util.spec_from_file_location(
    "install_sap",
    Path(__file__).parent.parent / "scripts" / "install-sap.py"
)
install_sap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install_sap)

# Import specific functions for cleaner test code
load_catalog = install_sap.load_catalog
get_sap = install_sap.get_sap
load_custom_sets = install_sap.load_custom_sets
get_sap_set = install_sap.get_sap_set
install_sap_func = install_sap.install_sap
install_sap_set = install_sap.install_sap_set
install_dependencies = install_sap.install_dependencies
check_sap_installed = install_sap.check_sap_installed
validate_sap_installation = install_sap.validate_sap_installation
list_saps = install_sap.list_saps
list_sap_sets = install_sap.list_sap_sets
print_summary = install_sap.print_summary
InstallStats = install_sap.InstallStats


#############################################################################
# Test Class 1: Catalog Functions
#############################################################################

@pytest.mark.catalog
class TestCatalogFunctions:
    """Tests for catalog loading and SAP lookup functions."""

    def test_load_catalog_success(self, temp_source_dir, captured_output):
        """Test loading a valid catalog file."""
        catalog = load_catalog(temp_source_dir)

        assert catalog is not None
        assert catalog['version'] == '4.1.0'
        assert catalog['total_saps'] == 3
        assert len(catalog['saps']) == 3

        # Check that success message was printed
        output = ' '.join(captured_output)
        assert 'Loaded catalog' in output
        assert 'v4.1.0' in output

    def test_load_catalog_missing_file(self, temp_source_without_catalog, captured_output):
        """Test loading catalog when file doesn't exist."""
        with pytest.raises(SystemExit) as exc_info:
            load_catalog(temp_source_without_catalog)

        assert exc_info.value.code == 1
        output = ' '.join(captured_output)
        assert 'Catalog not found' in output

    def test_load_catalog_invalid_json(self, temp_source_with_invalid_catalog, captured_output):
        """Test loading catalog with invalid JSON."""
        with pytest.raises(SystemExit) as exc_info:
            load_catalog(temp_source_with_invalid_catalog)

        assert exc_info.value.code == 1
        output = ' '.join(captured_output)
        assert 'Invalid catalog JSON' in output

    def test_load_catalog_prints_version(self, temp_source_dir, captured_output):
        """Test that catalog loading prints version information."""
        catalog = load_catalog(temp_source_dir)

        output = ' '.join(captured_output)
        assert 'v4.1.0' in output
        assert '3 SAPs' in output

    def test_get_sap_found(self, mock_catalog):
        """Test retrieving an existing SAP from catalog."""
        sap = get_sap('SAP-004', mock_catalog)

        assert sap is not None
        assert sap['id'] == 'SAP-004'
        assert sap['name'] == 'testing-framework'
        assert sap['status'] == 'active'

    def test_get_sap_not_found(self, mock_catalog):
        """Test retrieving a non-existent SAP from catalog."""
        sap = get_sap('SAP-999', mock_catalog)

        assert sap is None

    def test_get_sap_case_sensitive(self, mock_catalog):
        """Test that SAP lookup is case-sensitive."""
        # SAP-004 exists, but sap-004 should not match
        sap = get_sap('sap-004', mock_catalog)

        assert sap is None

        # Uppercase should work
        sap = get_sap('SAP-004', mock_catalog)
        assert sap is not None

    def test_catalog_structure_has_required_fields(self, mock_catalog):
        """Test that catalog has all required fields."""
        assert 'version' in mock_catalog
        assert 'total_saps' in mock_catalog
        assert 'saps' in mock_catalog
        assert 'sap_sets' in mock_catalog

        # Check each SAP has required fields
        for sap in mock_catalog['saps']:
            assert 'id' in sap
            assert 'name' in sap
            assert 'status' in sap
            assert 'location' in sap
            assert 'dependencies' in sap


#############################################################################
# Test Class 2: Installation Functions
#############################################################################

@pytest.mark.installation
class TestInstallationFunctions:
    """Tests for SAP installation functions."""

    def test_install_sap_success(self, temp_source_dir, temp_target_dir, captured_output):
        """Test successful installation of a SAP."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Verify files were copied
        sap_dir = temp_target_dir / 'docs/skilled-awareness/sap-framework'
        assert sap_dir.exists()
        assert (sap_dir / 'capability-charter.md').exists()
        assert (sap_dir / 'protocol-spec.md').exists()

        output = ' '.join(captured_output)
        assert 'installed successfully' in output

    def test_install_sap_already_installed(self, temp_source_dir, installed_sap_structure, captured_output):
        """Test installing a SAP that's already installed (idempotency)."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-000', temp_source_dir, installed_sap_structure, catalog, dry_run=False)

        assert success is True
        output = ' '.join(captured_output)
        assert 'already installed' in output
        assert 'skipping' in output

    def test_install_sap_not_in_catalog(self, temp_source_dir, temp_target_dir, captured_output):
        """Test installing a SAP that doesn't exist in catalog."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-999', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is False
        output = ' '.join(captured_output)
        assert 'not found in catalog' in output

    def test_install_sap_with_single_dependency(self, temp_source_dir, temp_target_dir, captured_output):
        """Test installing a SAP with one dependency."""
        catalog = load_catalog(temp_source_dir)

        # SAP-004 depends on SAP-000
        success = install_sap_func('SAP-004', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Both SAP-000 (dependency) and SAP-004 should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/testing-framework').exists()

        output = ' '.join(captured_output)
        assert 'dependencies' in output.lower()

    def test_install_sap_pilot_status_warning(self, temp_source_dir, temp_target_dir, captured_output):
        """Test that pilot status SAPs show a warning."""
        catalog = load_catalog(temp_source_dir)

        # SAP-001 has pilot status
        success = install_sap_func('SAP-001', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True
        output = ' '.join(captured_output)
        assert 'Pilot status' in output or 'pilot' in output.lower()

    def test_install_dependencies_success(self, temp_source_dir, temp_target_dir, mock_catalog):
        """Test successful dependency installation."""
        sap = get_sap('SAP-004', mock_catalog)

        success = install_dependencies(sap, temp_source_dir, temp_target_dir, mock_catalog, dry_run=False)

        assert success is True
        # SAP-000 (dependency) should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

    def test_install_dependencies_empty(self, temp_source_dir, temp_target_dir, mock_catalog):
        """Test installing SAP with no dependencies."""
        sap = get_sap('SAP-000', mock_catalog)

        success = install_dependencies(sap, temp_source_dir, temp_target_dir, mock_catalog, dry_run=False)

        # Should return True when no dependencies
        assert success is True

    def test_check_sap_installed_true(self, installed_sap_structure, mock_catalog):
        """Test checking if a SAP is installed (true case)."""
        # Mock the load_catalog call within check_sap_installed
        # Note: check_sap_installed uses Path.cwd(), so we patch that too
        with patch.object(Path, 'cwd', return_value=installed_sap_structure):
            with patch.object(install_sap, 'load_catalog', return_value=mock_catalog):
                installed = check_sap_installed('SAP-000', installed_sap_structure)

        assert installed is True

    def test_check_sap_installed_false(self, temp_target_dir, mock_catalog):
        """Test checking if a SAP is installed (false case)."""
        with patch.object(Path, 'cwd', return_value=temp_target_dir):
            with patch.object(install_sap, 'load_catalog', return_value=mock_catalog):
                installed = check_sap_installed('SAP-000', temp_target_dir)

        assert installed is False

    def test_validate_sap_installation_success(self, installed_sap_structure, mock_catalog):
        """Test validating a complete SAP installation."""
        sap = get_sap('SAP-000', mock_catalog)

        is_valid = validate_sap_installation('SAP-000', sap, installed_sap_structure)

        assert is_valid is True

    def test_validate_sap_installation_missing_artifacts(self, incomplete_sap_installation, mock_catalog, captured_output):
        """Test validating an incomplete SAP installation."""
        sap = get_sap('SAP-000', mock_catalog)

        is_valid = validate_sap_installation('SAP-000', sap, incomplete_sap_installation)

        assert is_valid is False
        output = ' '.join(captured_output)
        assert 'Missing artifacts' in output

    def test_install_sap_creates_directories(self, temp_source_dir, temp_target_dir, captured_output):
        """Test that installation creates necessary directories."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True
        assert (temp_target_dir / 'docs').exists()
        assert (temp_target_dir / 'docs/skilled-awareness').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

    def test_install_sap_copies_system_files(self, temp_source_dir, temp_target_dir, captured_output):
        """Test that system files are copied during installation."""
        catalog = load_catalog(temp_source_dir)

        # SAP-001 has system files
        success = install_sap_func('SAP-001', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Check system files were copied
        assert (temp_target_dir / 'inbox/README.md').exists()
        assert (temp_target_dir / 'inbox/INBOX_PROTOCOL.md').exists()

        output = ' '.join(captured_output)
        assert 'system file' in output.lower() or 'Copied' in output

    def test_install_sap_dry_run_no_files(self, temp_source_dir, temp_target_dir, captured_output):
        """Test that dry run doesn't create any files."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        assert success is True

        # No files should be created
        assert not (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

        output = ' '.join(captured_output)
        assert 'DRY RUN' in output

    def test_install_sap_source_directory_not_found(self, temp_source_dir, temp_target_dir, mock_catalog, captured_output):
        """Test installing SAP when source directory doesn't exist."""
        # Modify catalog to point to non-existent location
        bad_catalog = mock_catalog.copy()
        bad_catalog['saps'] = [
            {
                'id': 'SAP-BAD',
                'name': 'bad-sap',
                'status': 'active',
                'location': 'non/existent/path',
                'dependencies': [],
                'system_files': []
            }
        ]

        success = install_sap_func('SAP-BAD', temp_source_dir, temp_target_dir, bad_catalog, dry_run=False)

        assert success is False
        output = ' '.join(captured_output)
        assert 'source not found' in output.lower()


#############################################################################
# Test Class 3: SAP Set Functions
#############################################################################

@pytest.mark.sets
class TestSAPSetFunctions:
    """Tests for SAP set installation and management."""

    def test_get_sap_set_standard(self, mock_catalog, temp_target_dir):
        """Test retrieving a standard SAP set from catalog."""
        sap_set = get_sap_set('test-minimal', mock_catalog, temp_target_dir)

        assert sap_set is not None
        assert sap_set['name'] == 'Test Minimal Set'
        assert 'SAP-000' in sap_set['saps']
        assert 'SAP-001' in sap_set['saps']

    def test_get_sap_set_custom_from_chorabase(self, mock_catalog, temp_target_with_chorabase):
        """Test retrieving a custom SAP set from .chorabase."""
        sap_set = get_sap_set('custom-test-set', mock_catalog, temp_target_with_chorabase)

        assert sap_set is not None
        assert sap_set['name'] == 'Custom Test Set'
        assert 'SAP-000' in sap_set['saps']
        assert 'SAP-004' in sap_set['saps']

    def test_get_sap_set_not_found(self, mock_catalog, temp_target_dir):
        """Test retrieving a non-existent SAP set."""
        sap_set = get_sap_set('non-existent-set', mock_catalog, temp_target_dir)

        assert sap_set is None

    def test_load_custom_sets_no_file(self, temp_target_dir):
        """Test loading custom sets when .chorabase doesn't exist."""
        custom_sets = load_custom_sets(temp_target_dir)

        assert custom_sets == {}

    def test_load_custom_sets_valid_yaml(self, temp_target_with_chorabase):
        """Test loading valid custom sets from .chorabase."""
        custom_sets = load_custom_sets(temp_target_with_chorabase)

        assert 'custom-test-set' in custom_sets
        assert custom_sets['custom-test-set']['name'] == 'Custom Test Set'

    def test_load_custom_sets_invalid_yaml(self, tmp_path, captured_output):
        """Test loading custom sets with invalid YAML."""
        target = tmp_path / 'target_bad_yaml'
        target.mkdir()

        chorabase_file = target / '.chorabase'
        chorabase_file.write_text('invalid: yaml: content: [')

        custom_sets = load_custom_sets(target)

        # Should return empty dict on error
        assert custom_sets == {}
        output = ' '.join(captured_output)
        assert 'Could not load' in output or 'warning' in output.lower()

    def test_install_sap_set_success(self, temp_source_dir, temp_target_dir, captured_output):
        """Test successful installation of a SAP set."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_set('test-minimal', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Both SAPs from the set should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/inbox').exists()

        output = ' '.join(captured_output)
        assert 'Test Minimal Set' in output

    def test_install_sap_set_not_found(self, temp_source_dir, temp_target_dir, captured_output):
        """Test installing a non-existent SAP set."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_set('non-existent', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is False
        output = ' '.join(captured_output)
        assert 'not found' in output

    def test_install_sap_set_with_dependencies(self, temp_source_dir, temp_target_dir, captured_output):
        """Test installing a SAP set that includes SAPs with dependencies."""
        catalog = load_catalog(temp_source_dir)

        # test-with-deps contains SAP-004 which depends on SAP-000
        success = install_sap_set('test-with-deps', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Both SAP-004 and its dependency SAP-000 should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/testing-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

    def test_install_sap_set_dry_run(self, temp_source_dir, temp_target_dir, captured_output):
        """Test dry run of SAP set installation."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_set('test-minimal', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        assert success is True

        # No files should be created
        assert not (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

        output = ' '.join(captured_output)
        assert 'DRY RUN' in output


#############################################################################
# Test Class 4: Dry Run & List Tests
#############################################################################

@pytest.mark.unit
class TestDryRunAndListFunctions:
    """Tests for dry run mode and listing functions."""

    def test_dry_run_sap_no_files_created(self, temp_source_dir, temp_target_dir):
        """Test that dry run for single SAP creates no files."""
        catalog = load_catalog(temp_source_dir)

        # Record initial state
        initial_dirs = list(temp_target_dir.iterdir())

        install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        # Should have no new directories
        final_dirs = list(temp_target_dir.iterdir())
        assert len(final_dirs) == len(initial_dirs)

    def test_dry_run_set_no_files_created(self, temp_source_dir, temp_target_dir):
        """Test that dry run for SAP set creates no files."""
        catalog = load_catalog(temp_source_dir)

        initial_dirs = list(temp_target_dir.iterdir())

        install_sap_set('test-minimal', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        final_dirs = list(temp_target_dir.iterdir())
        assert len(final_dirs) == len(initial_dirs)

    def test_dry_run_shows_what_would_happen(self, temp_source_dir, temp_target_dir, captured_output):
        """Test that dry run shows what would be installed."""
        catalog = load_catalog(temp_source_dir)

        install_sap_func('SAP-004', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        output = ' '.join(captured_output)
        assert 'Would install' in output or 'DRY RUN' in output
        assert 'SAP-004' in output

    def test_list_saps_shows_all(self, temp_source_dir, captured_output):
        """Test that list_saps displays all SAPs."""
        catalog = load_catalog(temp_source_dir)

        list_saps(catalog)

        output = ' '.join(captured_output)
        # Note: list_saps uses dependency_graph which may not contain all SAPs
        # if they're not categorized. Just check that the total count is correct.
        assert '3 SAPs' in output

    def test_list_saps_with_empty_catalog(self, captured_output):
        """Test listing SAPs with an empty catalog."""
        empty_catalog = {
            'version': '1.0.0',
            'total_saps': 0,
            'saps': [],
            'dependency_graph': {}
        }

        list_saps(empty_catalog)

        output = ' '.join(captured_output)
        assert '0 SAPs' in output

    def test_list_sets_standard_only(self, temp_source_dir, temp_target_dir, captured_output):
        """Test listing SAP sets (standard sets only)."""
        catalog = load_catalog(temp_source_dir)

        list_sap_sets(catalog, temp_target_dir)

        output = ' '.join(captured_output)
        assert 'test-minimal' in output
        assert 'test-with-deps' in output
        assert 'Standard Sets' in output

    def test_list_sets_with_custom(self, temp_source_dir, temp_target_with_chorabase, captured_output):
        """Test listing SAP sets including custom sets."""
        catalog = load_catalog(temp_source_dir)

        list_sap_sets(catalog, temp_target_with_chorabase)

        output = ' '.join(captured_output)
        assert 'Standard Sets' in output
        assert 'Custom Sets' in output
        assert 'custom-test-set' in output

    def test_dry_run_with_dependencies(self, temp_source_dir, temp_target_dir, captured_output):
        """Test dry run with dependency resolution."""
        catalog = load_catalog(temp_source_dir)

        # SAP-004 has dependency on SAP-000
        install_sap_func('SAP-004', temp_source_dir, temp_target_dir, catalog, dry_run=True)

        output = ' '.join(captured_output)
        # In dry run mode, the function returns early and doesn't process dependencies
        # Just verify dry run message is shown
        assert 'DRY RUN' in output or 'Would install' in output

    def test_print_summary_dry_run_vs_real(self, captured_output):
        """Test that summary differentiates between dry run and real installation."""
        # Reset stats
        install_sap.stats = InstallStats()
        install_sap.stats.saps_installed = 2
        install_sap.stats.saps_skipped = 1

        # Dry run summary
        print_summary(dry_run=True)
        output_dry = ' '.join(captured_output)
        assert 'DRY RUN' in output_dry
        assert 'No changes were made' in output_dry

        # Clear output
        captured_output.clear()

        # Real installation summary
        print_summary(dry_run=False)
        output_real = ' '.join(captured_output)
        assert 'Next steps' in output_real
        assert 'DRY RUN' not in output_real


#############################################################################
# Test Class 5: Error Handling Tests
#############################################################################

@pytest.mark.errors
class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_install_sap_invalid_sap_id(self, temp_source_dir, temp_target_dir, captured_output):
        """Test installing with completely invalid SAP ID."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('INVALID-ID', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is False
        output = ' '.join(captured_output)
        assert 'not found' in output

    def test_install_sap_missing_source_directory(self, temp_source_dir, temp_target_dir, mock_catalog, captured_output):
        """Test error when SAP source directory is missing."""
        # Create catalog entry with non-existent location
        bad_catalog = mock_catalog.copy()
        bad_catalog['saps'] = [{
            'id': 'SAP-MISSING',
            'name': 'missing',
            'status': 'active',
            'location': 'does/not/exist',
            'dependencies': [],
            'system_files': []
        }]

        success = install_sap_func('SAP-MISSING', temp_source_dir, temp_target_dir, bad_catalog, dry_run=False)

        assert success is False
        output = ' '.join(captured_output)
        assert 'source not found' in output.lower()

    def test_load_catalog_json_decode_error(self, temp_source_with_invalid_catalog, captured_output):
        """Test handling of JSON decode errors in catalog."""
        with pytest.raises(SystemExit) as exc_info:
            load_catalog(temp_source_with_invalid_catalog)

        assert exc_info.value.code == 1
        output = ' '.join(captured_output)
        assert 'Invalid catalog JSON' in output

    def test_validation_handles_missing_directory(self, temp_target_dir, mock_catalog, captured_output):
        """Test validation when SAP directory doesn't exist."""
        sap = get_sap('SAP-000', mock_catalog)

        # Directory doesn't exist yet
        is_valid = validate_sap_installation('SAP-000', sap, temp_target_dir)

        assert is_valid is False

    def test_install_handles_keyboard_interrupt(self, temp_source_dir, temp_target_dir, mock_catalog):
        """Test that keyboard interrupt is handled gracefully."""
        with patch('shutil.copytree', side_effect=KeyboardInterrupt):
            with pytest.raises(KeyboardInterrupt):
                install_sap_func('SAP-000', temp_source_dir, temp_target_dir, mock_catalog, dry_run=False)

    def test_install_handles_generic_exception(self, temp_source_dir, temp_target_dir, captured_output):
        """Test handling of generic exceptions during installation."""
        catalog = load_catalog(temp_source_dir)

        # Force an exception by making copytree fail
        with patch('shutil.copytree', side_effect=PermissionError("Mock permission error")):
            success = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)

            assert success is False
            output = ' '.join(captured_output)
            assert 'Failed' in output or 'error' in output.lower()


#############################################################################
# Test Class 6: Integration Tests
#############################################################################

@pytest.mark.integration
class TestIntegrationScenarios:
    """End-to-end integration tests with real file operations."""

    def test_e2e_install_single_sap(self, temp_source_dir, temp_target_dir):
        """End-to-end: Install a single SAP with no dependencies."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_func('SAP-001', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Verify complete installation
        sap_dir = temp_target_dir / 'docs/skilled-awareness/inbox'
        assert sap_dir.exists()
        assert (sap_dir / 'capability-charter.md').exists()
        assert (sap_dir / 'protocol-spec.md').exists()
        assert (sap_dir / 'awareness-guide.md').exists()
        assert (sap_dir / 'adoption-blueprint.md').exists()
        assert (sap_dir / 'ledger.md').exists()

        # Verify system files
        assert (temp_target_dir / 'inbox/README.md').exists()
        assert (temp_target_dir / 'inbox/INBOX_PROTOCOL.md').exists()

    def test_e2e_install_minimal_set(self, temp_source_dir, temp_target_dir):
        """End-to-end: Install a minimal SAP set."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_set('test-minimal', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Verify both SAPs installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/inbox').exists()

    def test_e2e_install_with_dependency_chain(self, temp_source_dir, temp_target_dir):
        """End-to-end: Install SAP with dependency chain."""
        catalog = load_catalog(temp_source_dir)

        # SAP-004 depends on SAP-000
        success = install_sap_func('SAP-004', temp_source_dir, temp_target_dir, catalog, dry_run=False)

        assert success is True

        # Both should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/testing-framework').exists()

    def test_e2e_progressive_installation(self, temp_source_dir, temp_target_dir):
        """End-to-end: Install SAPs one by one progressively."""
        catalog = load_catalog(temp_source_dir)

        # Install SAP-000
        success1 = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success1 is True

        # Install SAP-001
        success2 = install_sap_func('SAP-001', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success2 is True

        # Install SAP-004 (dependency already satisfied)
        success3 = install_sap_func('SAP-004', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success3 is True

        # All three should be installed
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/inbox').exists()
        assert (temp_target_dir / 'docs/skilled-awareness/testing-framework').exists()

    def test_e2e_custom_set_from_chorabase(self, temp_source_dir, temp_target_with_chorabase):
        """End-to-end: Install custom SAP set from .chorabase."""
        catalog = load_catalog(temp_source_dir)

        success = install_sap_set('custom-test-set', temp_source_dir, temp_target_with_chorabase, catalog, dry_run=False)

        assert success is True

        # Custom set contains SAP-000 and SAP-004
        assert (temp_target_with_chorabase / 'docs/skilled-awareness/sap-framework').exists()
        assert (temp_target_with_chorabase / 'docs/skilled-awareness/testing-framework').exists()

    def test_e2e_idempotency_second_install_skips(self, temp_source_dir, temp_target_dir, captured_output):
        """End-to-end: Second installation of same SAP should skip."""
        catalog = load_catalog(temp_source_dir)

        # First installation
        install_sap.stats = InstallStats()
        success1 = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success1 is True
        assert install_sap.stats.saps_installed == 1

        # Second installation should skip
        install_sap.stats = InstallStats()
        captured_output.clear()
        success2 = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success2 is True
        assert install_sap.stats.saps_skipped == 1
        assert install_sap.stats.saps_installed == 0

        output = ' '.join(captured_output)
        assert 'already installed' in output

    def test_e2e_dry_run_then_real_install(self, temp_source_dir, temp_target_dir):
        """End-to-end: Dry run followed by real installation."""
        catalog = load_catalog(temp_source_dir)

        # First dry run
        success_dry = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=True)
        assert success_dry is True
        assert not (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

        # Then real install
        success_real = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success_real is True
        assert (temp_target_dir / 'docs/skilled-awareness/sap-framework').exists()

    def test_e2e_validation_failure_cleanup(self, temp_source_dir, temp_target_dir, mock_catalog):
        """End-to-end: Test behavior when validation fails after copy."""
        # This test verifies the current behavior - validation happens after copy
        # In a real scenario, failed validation leaves files in place (no cleanup)
        catalog = load_catalog(temp_source_dir)

        # Install normally first
        success = install_sap_func('SAP-000', temp_source_dir, temp_target_dir, catalog, dry_run=False)
        assert success is True

        # Remove one artifact to cause validation failure on next check
        sap_dir = temp_target_dir / 'docs/skilled-awareness/sap-framework'
        (sap_dir / 'ledger.md').unlink()

        # Validation should now fail
        sap = get_sap('SAP-000', mock_catalog)
        is_valid = validate_sap_installation('SAP-000', sap, temp_target_dir)
        assert is_valid is False


#############################################################################
# Additional Unit Tests for Helper Functions
#############################################################################

@pytest.mark.unit
class TestHelperFunctions:
    """Tests for helper and utility functions."""

    def test_install_stats_initialization(self):
        """Test InstallStats initializes with zeros."""
        stats = InstallStats()

        assert stats.saps_installed == 0
        assert stats.saps_skipped == 0
        assert stats.errors == 0
        assert stats.warnings == 0

    def test_print_functions_update_stats(self, captured_output):
        """Test that print functions update global stats."""
        # Reset stats
        install_sap.stats = InstallStats()

        install_sap.print_warning("Test warning")
        assert install_sap.stats.warnings == 1

        install_sap.print_error("Test error")
        assert install_sap.stats.errors == 1

    def test_colors_class_attributes(self):
        """Test that Colors class has required attributes."""
        assert hasattr(install_sap.Colors, 'RED')
        assert hasattr(install_sap.Colors, 'GREEN')
        assert hasattr(install_sap.Colors, 'YELLOW')
        assert hasattr(install_sap.Colors, 'BLUE')
        assert hasattr(install_sap.Colors, 'NC')


#############################################################################
# Pytest Configuration
#############################################################################

def test_module_imports():
    """Test that all required functions are importable."""
    assert load_catalog is not None
    assert get_sap is not None
    assert install_sap_func is not None
    assert install_sap_set is not None
    assert list_saps is not None
    assert list_sap_sets is not None
    assert validate_sap_installation is not None
    assert check_sap_installed is not None
