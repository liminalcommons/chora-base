#!/usr/bin/env python3
"""SAP artifact generator from catalog metadata.

This script generates all 5 SAP artifacts (capability-charter, protocol-spec,
awareness-guide, adoption-blueprint, ledger) from a SAP entry in sap-catalog.json.

Usage:
    python scripts/generate-sap.py SAP-029
    python scripts/generate-sap.py SAP-029 --dry-run
    python scripts/generate-sap.py SAP-029 --force
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def load_catalog(catalog_path='sap-catalog.json'):
    """Load sap-catalog.json"""
    with open(catalog_path, encoding='utf-8') as f:
        return json.load(f)


def get_sap_entry(catalog, sap_id):
    """Find SAP entry by ID in catalog"""
    for sap in catalog['saps']:
        if sap['id'] == sap_id:
            return sap
    raise ValueError(f"SAP {sap_id} not found in catalog")


def render_template(template_name, data):
    """Render Jinja2 template with data"""
    env = Environment(loader=FileSystemLoader('templates/sap'))
    template = env.get_template(template_name)
    return template.render(**data)


def run_validation(sap_id, dry_run=False):
    """Run sap-evaluator.py --quick validation

    Args:
        sap_id: SAP ID to validate
        dry_run: If True, show what would be validated without running

    Returns:
        Boolean indicating validation success (or None if skipped/dry-run)
    """
    if dry_run:
        print(f"\n🔍 Validation preview:")
        print(f"   Would run: python scripts/sap-evaluator.py --quick {sap_id}")
        return None

    print(f"\n🔍 Running validation...")
    try:
        # Set UTF-8 encoding environment variable for subprocess
        import os
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        result = subprocess.run(
            [sys.executable, 'scripts/sap-evaluator.py', '--quick', sap_id],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60,
            env=env
        )

        # Print the validation output
        if result.stdout:
            print(result.stdout)

        if result.returncode == 0:
            print("✅ Validation passed")
            return True
        else:
            print(f"⚠️  Validation completed with warnings (exit code: {result.returncode})")
            if result.stderr:
                print(f"   {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️  Validation timed out (>60s)")
        return False
    except FileNotFoundError:
        print("⚠️  sap-evaluator.py not found, skipping validation")
        return None
    except Exception as e:
        print(f"⚠️  Validation error: {e}")
        return False


def update_index(sap_data, index_path='docs/skilled-awareness/INDEX.md', dry_run=False):
    """Update INDEX.md with new SAP entry

    Args:
        sap_data: SAP metadata dictionary
        index_path: Path to INDEX.md file
        dry_run: If True, show what would be updated without writing

    Returns:
        Boolean indicating success
    """
    index_file = Path(index_path)

    if not index_file.exists():
        print(f"⚠️  INDEX.md not found at {index_path}, skipping index update")
        return False

    # Read current INDEX.md
    content = index_file.read_text(encoding='utf-8')

    # Check if SAP already exists in index
    sap_id = sap_data['id']
    if f"| {sap_id} |" in content:
        print(f"ℹ️  {sap_id} already in INDEX.md, skipping index update")
        return False

    # Extract location for relative path (remove docs/skilled-awareness/ prefix)
    location = sap_data['location'].replace('docs/skilled-awareness/', '')

    # Format dependencies
    deps = sap_data.get('dependencies', [])
    if deps:
        deps_str = ', '.join(deps)
    else:
        deps_str = "None (foundational)"

    # Determine awareness score (default to pending for new SAPs)
    awareness = "-"

    # Create new table row
    new_row = f"| {sap_id} | {sap_data['name']} | {sap_data['version']} | {sap_data['status'].title()} | {sap_data.get('phase', 'Pilot')} | {awareness} | [{location}/]({location}/) | {deps_str} |"

    # Find the Active SAPs table and insert before the closing marker
    # Insert after the last SAP row (before the blank line after the table)
    table_pattern = r'(\| SAP-\d+ \|[^\n]+\n)(\n\*\*Awareness Score Legend\*\*:)'

    match = re.search(table_pattern, content)
    if match:
        # Insert new row after the last SAP row
        updated_content = content[:match.end(1)] + new_row + '\n' + content[match.end(1):]

        # Update coverage count
        # Find "Current Coverage": 26/28 SAPs (93%)
        coverage_pattern = r'\*\*Current Coverage\*\*: (\d+)/(\d+) SAPs \((\d+)%\)'
        coverage_match = re.search(coverage_pattern, updated_content)

        if coverage_match:
            current = int(coverage_match.group(1))
            total = int(coverage_match.group(2))
            new_current = current + 1
            new_total = total + 1  # Increment total since this is a new capability
            new_percentage = round((new_current / new_total) * 100)

            updated_content = re.sub(
                coverage_pattern,
                f'**Current Coverage**: {new_current}/{new_total} SAPs ({new_percentage}%)',
                updated_content
            )

            # Also update "XX capabilities" text at the top
            capabilities_pattern = r'This index tracks all \*\*(\d+) capabilities\*\*'
            updated_content = re.sub(
                capabilities_pattern,
                f'This index tracks all **{new_total} capabilities**',
                updated_content
            )

        # Update "Last Updated" date
        today = datetime.now().strftime('%Y-%m-%d')
        updated_content = re.sub(
            r'\*\*Last Updated\*\*: \d{4}-\d{2}-\d{2}',
            f'**Last Updated**: {today}',
            updated_content
        )

        # Add changelog entry
        changelog_entry = f"| {today} | {sap_id} ({sap_data['name']}) generated - {sap_data.get('description', 'New capability')} | Claude Code |"

        # Find changelog table and insert at the top (after header row)
        changelog_pattern = r'(## Changelog\n\n\| Date \| Change \| Author \|\n\|------|--------|--------\|\n)'
        changelog_match = re.search(changelog_pattern, updated_content)

        if changelog_match:
            updated_content = updated_content[:changelog_match.end()] + changelog_entry + '\n' + updated_content[changelog_match.end():]

        if dry_run:
            print(f"\n📝 INDEX.md update preview:")
            print(f"   Would add row: {new_row}")
            print(f"   Would update coverage: {current}/{total} → {new_current}/{new_total} ({new_percentage}%)")
            print(f"   Would update capabilities: {total} → {new_total}")
            print(f"   Would add changelog: {changelog_entry}")
        else:
            # Write updated INDEX.md
            index_file.write_text(updated_content, encoding='utf-8')
            print(f"\n📝 Updated INDEX.md:")
            print(f"   ✅ Added {sap_id} to Active SAPs table")
            print(f"   ✅ Updated coverage: {current}/{total} → {new_current}/{new_total} ({new_percentage}%)")
            print(f"   ✅ Updated capabilities: {total} → {new_total}")
            print(f"   ✅ Added changelog entry")

        return True
    else:
        print(f"⚠️  Could not find Active SAPs table pattern in INDEX.md")
        return False


def generate_sap(sap_id, dry_run=False, force=False, catalog_path='sap-catalog.json', skip_index=False, skip_validation=False):
    """Generate all 5 artifacts for a SAP

    Args:
        sap_id: SAP ID (e.g., 'SAP-029')
        dry_run: If True, print what would be generated without writing files
        force: If True, overwrite existing files
        catalog_path: Path to catalog JSON file
        skip_index: If True, skip INDEX.md auto-update
        skip_validation: If True, skip sap-evaluator.py validation

    Returns:
        List of generated file paths
    """
    # Load catalog and get SAP entry
    catalog = load_catalog(catalog_path)
    sap_data = get_sap_entry(catalog, sap_id)

    # Merge generation fields into top-level for template access
    if 'generation' in sap_data:
        sap_data.update(sap_data['generation'])

    # Define artifacts to generate
    artifacts = [
        ('capability-charter.j2', 'capability-charter.md'),
        ('protocol-spec.j2', 'protocol-spec.md'),
        ('awareness-guide.j2', 'awareness-guide.md'),
        ('adoption-blueprint.j2', 'adoption-blueprint.md'),
        ('ledger.j2', 'ledger.md'),
    ]

    # Determine output directory
    output_dir = Path(sap_data['location'])

    if dry_run:
        print(f"🔍 DRY RUN: Would generate artifacts for {sap_id}")
        print(f"📁 Output directory: {output_dir}")
        print()

    # Create output directory
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    # Generate each artifact
    for template_name, output_name in artifacts:
        output_path = output_dir / output_name

        # Check if file exists and force not specified
        if output_path.exists() and not force and not dry_run:
            print(f"⚠️  Skipping {output_path} (already exists, use --force to overwrite)")
            continue

        # Render template
        try:
            content = render_template(template_name, sap_data)
        except Exception as e:
            print(f"❌ Error rendering {template_name}: {e}")
            continue

        if dry_run:
            print(f"✅ Would generate: {output_path}")
            print(f"   Template: {template_name}")
            print(f"   Size: ~{len(content)} characters")
            print()
        else:
            # Write file
            output_path.write_text(content, encoding='utf-8')
            generated_files.append(output_path)
            print(f"✅ Generated {output_path}")

    if not dry_run and generated_files:
        print(f"\n✅ Successfully generated {len(generated_files)} artifacts for {sap_id}")
        print(f"📁 Location: {output_dir}")

        # Update INDEX.md (unless skipped or using test catalog)
        if not skip_index and catalog_path == 'sap-catalog.json':
            update_index(sap_data, dry_run=False)

        # Run validation (unless skipped)
        if not skip_validation:
            run_validation(sap_id, dry_run=False)
    elif dry_run:
        print(f"🔍 DRY RUN COMPLETE: {len(artifacts)} artifacts would be generated")

        # Show INDEX.md update preview
        if not skip_index and catalog_path == 'sap-catalog.json':
            update_index(sap_data, dry_run=True)

        # Show validation preview
        if not skip_validation:
            run_validation(sap_id, dry_run=True)

    return generated_files


def main():
    """Main entry point"""
    import argparse

    # Configure stdout for UTF-8 on Windows
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Generate SAP artifacts from catalog metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate-sap.py SAP-029
  python scripts/generate-sap.py SAP-029 --dry-run
  python scripts/generate-sap.py SAP-029 --force
        """
    )
    parser.add_argument('sap_id', help='SAP ID to generate (e.g., SAP-029)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be generated without writing files')
    parser.add_argument('--force', action='store_true',
                       help='Overwrite existing files')
    parser.add_argument('--catalog', default='sap-catalog.json',
                       help='Path to sap-catalog.json (default: sap-catalog.json)')
    parser.add_argument('--skip-index', action='store_true',
                       help='Skip INDEX.md auto-update')
    parser.add_argument('--skip-validation', action='store_true',
                       help='Skip sap-evaluator.py validation')

    args = parser.parse_args()

    try:
        generate_sap(args.sap_id, dry_run=args.dry_run, force=args.force,
                    catalog_path=args.catalog, skip_index=args.skip_index,
                    skip_validation=args.skip_validation)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print(f"   Make sure you're running from the chora-base root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
