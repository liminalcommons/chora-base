#!/usr/bin/env python3
"""install-sap.py - Install SAPs or SAP sets from chora-base

Purpose: Automated installation of Skilled Awareness Packages with dependency resolution

Usage:
    # Install individual SAP
    python scripts/install-sap.py SAP-004
    python scripts/install-sap.py SAP-004 --source /path/to/chora-base

    # Install SAP set
    python scripts/install-sap.py --set minimal-entry
    python scripts/install-sap.py --set recommended

    # List options
    python scripts/install-sap.py --list
    python scripts/install-sap.py --list-sets

    # Dry run
    python scripts/install-sap.py SAP-004 --dry-run
    python scripts/install-sap.py --set minimal-entry --dry-run

Exit codes:
    0 - Success
    1 - Error (validation, installation failure)
    2 - Invalid usage
"""

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("Warning: PyYAML not available. Custom sets from .chorabase won't work.")
    print("Install with: pip install PyYAML")
    yaml = None

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class InstallStats:
    """Track installation statistics"""
    def __init__(self):
        self.saps_installed = 0
        self.saps_skipped = 0
        self.errors = 0
        self.warnings = 0
        self.start_time = None
        self.current_sap_index = 0
        self.total_saps = 0

stats = InstallStats()

#############################################################################
# Helper Functions
#############################################################################

def print_header(text: str) -> None:
    """Print section header"""
    print(f"{Colors.BLUE}======================================={Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}======================================={Colors.NC}")
    print()

def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.NC} {text}")

def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {text}")
    stats.warnings += 1

def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.NC} {text}")
    stats.errors += 1

def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.NC} {text}")

def print_progress_bar(current: int, total: int, sap_name: str = "", bar_length: int = 40) -> None:
    """Print progress bar for SAP set installation

    Args:
        current: Current SAP number (0-indexed, but will display as 1-indexed)
        total: Total number of SAPs
        sap_name: Name of current SAP being installed
        bar_length: Length of the progress bar
    """
    if total == 0:
        return

    # Calculate progress
    progress = (current + 1) / total
    filled_length = int(bar_length * progress)

    # Build progress bar
    bar = '=' * filled_length + '>' if filled_length < bar_length else '=' * bar_length
    bar = bar.ljust(bar_length)

    # Calculate time estimate
    time_str = ""
    if stats.start_time and current > 0:
        elapsed = time.time() - stats.start_time
        avg_time_per_sap = elapsed / current
        remaining_saps = total - current
        estimated_remaining = avg_time_per_sap * remaining_saps

        if estimated_remaining < 60:
            time_str = f" ~{int(estimated_remaining)}s remaining"
        else:
            minutes = int(estimated_remaining / 60)
            time_str = f" ~{minutes}m remaining"

    # Print progress bar
    percentage = int(progress * 100)
    print(f"\r[{bar}] {current + 1}/{total} SAPs ({percentage}%){time_str}", end='', flush=True)

    if current + 1 == total:
        print()  # New line when complete

#############################################################################
# Catalog Functions
#############################################################################

def load_catalog(source_dir: Path) -> Dict:
    """Load SAP catalog from source directory"""
    catalog_file = source_dir / "sap-catalog.json"

    if not catalog_file.exists():
        print_error(f"Catalog not found: {catalog_file}")
        print_info("Expected: sap-catalog.json in chora-base root")
        sys.exit(1)

    try:
        with open(catalog_file, 'r') as f:
            catalog = json.load(f)
        print_success(f"Loaded catalog (v{catalog.get('version', 'unknown')}, {catalog.get('total_saps', 0)} SAPs)")
        return catalog
    except json.JSONDecodeError as e:
        print_error(f"Invalid catalog JSON: {e}")
        sys.exit(1)

def get_sap(sap_id: str, catalog: Dict) -> Optional[Dict]:
    """Get SAP metadata from catalog"""
    for sap in catalog.get('saps', []):
        if sap['id'] == sap_id:
            return sap
    return None

def load_custom_sets(target_dir: Path) -> Dict:
    """Load custom SAP sets from .chorabase if available"""
    if yaml is None:
        return {}

    chorabase_file = target_dir / ".chorabase"
    if not chorabase_file.exists():
        return {}

    try:
        with open(chorabase_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('sap_sets', {})
    except Exception as e:
        print_warning(f"Could not load custom sets from .chorabase: {e}")
        return {}

#############################################################################
# SAP Set Functions
#############################################################################

def list_sap_sets(catalog: Dict, target_dir: Path) -> None:
    """List all available SAP sets"""
    print_header("Available SAP Sets")

    # Standard sets from catalog
    standard_sets = catalog.get('sap_sets', {})
    if standard_sets:
        print(f"{Colors.GREEN}Standard Sets (from catalog):{Colors.NC}")
        print()
        for set_id, set_info in standard_sets.items():
            print(f"  {Colors.BLUE}{set_id}{Colors.NC}")
            print(f"    Name: {set_info['name']}")
            print(f"    SAPs: {len(set_info['saps'])} ({', '.join(set_info['saps'][:3])}{'...' if len(set_info['saps']) > 3 else ''})")
            print(f"    Tokens: ~{set_info['estimated_tokens']:,}")
            print(f"    Time: {set_info['estimated_hours']}")
            print(f"    Use: {set_info['description']}")
            if set_info.get('warnings'):
                print(f"    {Colors.YELLOW}⚠ Warnings: {len(set_info['warnings'])}{Colors.NC}")
            print()

    # Custom sets from .chorabase
    custom_sets = load_custom_sets(target_dir)
    if custom_sets:
        print(f"{Colors.GREEN}Custom Sets (from .chorabase):{Colors.NC}")
        print()
        for set_id, set_info in custom_sets.items():
            print(f"  {Colors.BLUE}{set_id}{Colors.NC}")
            print(f"    Name: {set_info.get('name', set_id)}")
            print(f"    SAPs: {len(set_info.get('saps', []))} ({', '.join(set_info.get('saps', [])[:3])})")
            if 'estimated_tokens' in set_info:
                print(f"    Tokens: ~{set_info['estimated_tokens']:,}")
            print()

    if not standard_sets and not custom_sets:
        print_info("No SAP sets available")

def get_sap_set(set_id: str, catalog: Dict, target_dir: Path) -> Optional[Dict]:
    """Get SAP set by ID (checks both standard and custom sets)"""
    # Check standard sets
    standard_sets = catalog.get('sap_sets', {})
    if set_id in standard_sets:
        return standard_sets[set_id]

    # Check custom sets
    custom_sets = load_custom_sets(target_dir)
    if set_id in custom_sets:
        return custom_sets[set_id]

    return None

def install_sap_set(set_id: str, source_dir: Path, target_dir: Path, catalog: Dict, dry_run: bool = False) -> bool:
    """Install a SAP set (multiple SAPs)"""
    sap_set = get_sap_set(set_id, catalog, target_dir)

    if not sap_set:
        print_error(f"SAP set '{set_id}' not found")
        print_info("Use --list-sets to see available sets")
        return False

    print_header(f"Installing SAP Set: {sap_set['name']}")

    print_info(f"Set: {set_id}")
    print_info(f"SAPs: {len(sap_set['saps'])} ({', '.join(sap_set['saps'])})")
    if 'estimated_tokens' in sap_set:
        print_info(f"Estimated tokens: ~{sap_set['estimated_tokens']:,}")
    if 'estimated_hours' in sap_set:
        print_info(f"Estimated time: {sap_set['estimated_hours']}")
    print()

    # Show warnings if any
    if sap_set.get('warnings'):
        print_warning("Warnings for this set:")
        for warning in sap_set['warnings']:
            print(f"  - {warning}")
        print()

    # Initialize progress tracking
    stats.total_saps = len(sap_set['saps'])
    stats.start_time = time.time()
    stats.current_sap_index = 0

    # Install each SAP in the set
    success = True
    for idx, sap_id in enumerate(sap_set['saps']):
        stats.current_sap_index = idx

        if not install_sap(sap_id, source_dir, target_dir, catalog, dry_run, indent=True):
            success = False
            # Continue with other SAPs even if one fails

        # Show progress bar (after installation)
        if not dry_run and stats.total_saps > 1:
            print_progress_bar(idx, stats.total_saps)

    return success

#############################################################################
# Installation Functions
#############################################################################

def check_sap_installed(sap_id: str, target_dir: Path) -> bool:
    """Check if SAP is already installed"""
    sap = get_sap(sap_id, load_catalog(Path.cwd()))  # This is a simplification
    if not sap or 'location' not in sap:
        return False

    sap_dir = target_dir / sap['location']
    return sap_dir.exists()

def validate_sap_installation(sap_id: str, sap: Dict, target_dir: Path) -> bool:
    """Validate that all required SAP files exist"""
    sap_dir = target_dir / sap['location']

    required_artifacts = ['capability-charter.md', 'protocol-spec.md',
                         'awareness-guide.md', 'adoption-blueprint.md', 'ledger.md']

    missing = []
    for artifact in required_artifacts:
        if not (sap_dir / artifact).exists():
            missing.append(artifact)

    if missing:
        print_error(f"Missing artifacts: {', '.join(missing)}")
        return False

    return True

def install_dependencies(sap: Dict, source_dir: Path, target_dir: Path, catalog: Dict, dry_run: bool, indent: bool = False) -> bool:
    """Install SAP dependencies recursively"""
    prefix = "  " if indent else ""
    dependencies = sap.get('dependencies', [])

    if not dependencies:
        return True

    print_info(f"{prefix}Checking dependencies: {', '.join(dependencies)}")

    success = True
    for dep_id in dependencies:
        if check_sap_installed(dep_id, target_dir):
            print_info(f"{prefix}  ✓ {dep_id} already installed")
            continue

        print_info(f"{prefix}  📦 Installing dependency: {dep_id}")
        if not install_sap(dep_id, source_dir, target_dir, catalog, dry_run, indent=True):
            print_error(f"{prefix}  Failed to install dependency: {dep_id}")
            success = False

    return success

def install_sap(sap_id: str, source_dir: Path, target_dir: Path, catalog: Dict, dry_run: bool = False, indent: bool = False) -> bool:
    """Install a single SAP with dependency resolution"""
    prefix = "  " if indent else ""

    # Get SAP metadata
    sap = get_sap(sap_id, catalog)
    if not sap:
        print_error(f"{prefix}SAP {sap_id} not found in catalog")
        return False

    # Check if already installed
    sap_dir = target_dir / sap['location']
    if sap_dir.exists():
        print_info(f"{prefix}✓ {sap_id} ({sap['name']}) already installed - skipping")
        stats.saps_skipped += 1
        return True

    print()
    print(f"{prefix}{Colors.BLUE}Installing {sap['name']} ({sap_id}){Colors.NC}")

    # Show warnings for pilot SAPs
    if sap.get('status') == 'pilot':
        print_warning(f"{prefix}This SAP is in Pilot status and may undergo changes")

    if dry_run:
        print_info(f"{prefix}[DRY RUN] Would install {sap_id}")
        stats.saps_installed += 1
        return True

    # Install dependencies first
    if not install_dependencies(sap, source_dir, target_dir, catalog, dry_run, indent):
        print_warning(f"{prefix}Some dependencies failed, continuing anyway")

    # Copy SAP directory
    sap_src = source_dir / sap['location']
    if not sap_src.exists():
        print_error(f"{prefix}SAP source not found: {sap_src}")
        return False

    try:
        shutil.copytree(sap_src, sap_dir)
        print_success(f"{prefix}Copied SAP directory")
    except Exception as e:
        print_error(f"{prefix}Failed to copy SAP directory: {e}")
        return False

    # Copy system files
    system_files = sap.get('system_files', [])
    for sys_file in system_files:
        src = source_dir / sys_file
        dest = target_dir / sys_file

        if not src.exists():
            print_warning(f"{prefix}System file not found: {sys_file}")
            continue

        try:
            # Create parent directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)

            if src.is_dir():
                if dest.exists():
                    print_info(f"{prefix}System directory already exists: {sys_file} - skipping")
                else:
                    shutil.copytree(src, dest)
                    print_success(f"{prefix}Copied system directory: {sys_file}")
            else:
                shutil.copy2(src, dest)
                print_success(f"{prefix}Copied system file: {sys_file}")
        except Exception as e:
            print_warning(f"{prefix}Failed to copy system file {sys_file}: {e}")

    # Validate installation
    if not validate_sap_installation(sap_id, sap, target_dir):
        print_error(f"{prefix}Installation validation failed")
        return False

    print_success(f"{prefix}{sap['name']} installed successfully!")
    stats.saps_installed += 1

    return True

def list_saps(catalog: Dict) -> None:
    """List all available SAPs"""
    print_header("Available SAPs")

    print(f"Total: {catalog.get('total_saps', 0)} SAPs")
    print()

    # Group by category
    categories = catalog.get('dependency_graph', {})

    for category, sap_ids in categories.items():
        print(f"{Colors.GREEN}{category.replace('_', ' ').title()}:{Colors.NC}")
        for sap_id in sap_ids:
            sap = get_sap(sap_id, catalog)
            if sap:
                status_icon = "✓" if sap['status'] == 'active' else "🔄" if sap['status'] == 'pilot' else "📋"
                print(f"  {status_icon} {sap_id}: {sap['name']}")
                print(f"      {sap['description'][:80]}{'...' if len(sap['description']) > 80 else ''}")
        print()

#############################################################################
# Summary Functions
#############################################################################

def print_summary(dry_run: bool) -> None:
    """Print installation summary"""
    print_header("Installation Summary")

    print(f"{Colors.GREEN}SAPs installed:{Colors.NC} {stats.saps_installed}")
    print(f"{Colors.BLUE}SAPs skipped (already installed):{Colors.NC} {stats.saps_skipped}")
    print(f"{Colors.YELLOW}Warnings:{Colors.NC} {stats.warnings}")
    print(f"{Colors.RED}Errors:{Colors.NC} {stats.errors}")
    print()

    if dry_run:
        print_info("DRY RUN - No changes were made")
        print()
    else:
        if stats.saps_installed > 0:
            print_info("Next steps:")
            print_info("  1. Review installed SAPs in docs/skilled-awareness/")
            print_info("  2. Update AGENTS.md with installed capabilities")
            print_info("  3. Read adoption-blueprint.md for each SAP")
            print_info("  4. Run validation: just test && just lint")
            print()

#############################################################################
# Main
#############################################################################

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Install SAPs or SAP sets from chora-base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install individual SAP
  python scripts/install-sap.py SAP-004

  # Install SAP set
  python scripts/install-sap.py --set minimal-entry

  # Preview without installing
  python scripts/install-sap.py --set recommended --dry-run

  # List available options
  python scripts/install-sap.py --list
  python scripts/install-sap.py --list-sets

More Info:
  See: docs/user-docs/how-to/install-sap-set.md
        """
    )

    parser.add_argument('sap_id', nargs='?', help='SAP ID to install (e.g., SAP-004)')
    parser.add_argument('--set', dest='set_id', help='Install a SAP set (e.g., minimal-entry)')
    parser.add_argument('--source', type=Path, default=Path.cwd(), help='Path to chora-base (default: current directory)')
    parser.add_argument('--target', type=Path, default=Path.cwd(), help='Target directory (default: current directory)')
    parser.add_argument('--list', action='store_true', help='List all available SAPs')
    parser.add_argument('--list-sets', action='store_true', help='List all available SAP sets')
    parser.add_argument('--dry-run', action='store_true', help='Preview without installing')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.sap_id, args.set_id, args.list, args.list_sets]):
        parser.print_help()
        sys.exit(2)

    # Load catalog
    catalog = load_catalog(args.source)

    # Handle list commands
    if args.list:
        list_saps(catalog)
        sys.exit(0)

    if args.list_sets:
        list_sap_sets(catalog, args.target)
        sys.exit(0)

    # Install SAP set
    if args.set_id:
        print_header("SAP Set Installation")
        if args.dry_run:
            print_warning("DRY RUN MODE - No changes will be made")
            print()

        success = install_sap_set(args.set_id, args.source, args.target, catalog, args.dry_run)
        print()
        print_summary(args.dry_run)

        sys.exit(0 if success else 1)

    # Install individual SAP
    if args.sap_id:
        print_header("SAP Installation")
        if args.dry_run:
            print_warning("DRY RUN MODE - No changes will be made")
            print()

        success = install_sap(args.sap_id, args.source, args.target, catalog, args.dry_run)
        print()
        print_summary(args.dry_run)

        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
