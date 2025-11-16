"""SAP Verification Helper Module - SAP-050 Implementation"""

from pathlib import Path
import re
import sys

def verify_structure(sap_name: str) -> dict:
    """Verify SAP structure (5 artifacts + manifest)"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    required = ['capability-charter.md', 'protocol-spec.md',
                'adoption-blueprint.md', 'ledger.md']
    for artifact in required:
        if not (sap_dir / artifact).exists():
            missing.append(artifact)

    # Check AGENTS.md or awareness-guide.md
    if not (sap_dir / 'AGENTS.md').exists() and not (sap_dir / 'awareness-guide.md').exists():
        missing.append('AGENTS.md (or awareness-guide.md)')

    # Check YAML manifest
    manifest_pattern = sap_name.replace('-', '_')
    manifest_found = any(
        manifest_pattern in str(m)
        for m in Path('capabilities').glob('chora.*.yaml')
    )
    if not manifest_found:
        missing.append('capability manifest (YAML)')

    return {'passed': len(missing) == 0, 'missing': missing}

def verify_completeness(sap_name: str) -> dict:
    """Verify required sections present"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    issues = []

    # Charter: Must have Problem Statement, Solution Design, Success Metrics
    charter = sap_dir / 'capability-charter.md'
    if charter.exists():
        content = charter.read_text(encoding='utf-8')
        for section in ['Problem Statement', 'Solution Design', 'Success Metrics']:
            if section not in content:
                issues.append(f"capability-charter.md missing: {section}")
    else:
        issues.append("capability-charter.md not found")

    # AGENTS.md: Must have Quick Start, Workflow
    agents = sap_dir / 'AGENTS.md'
    if not agents.exists():
        agents = sap_dir / 'awareness-guide.md'

    if agents.exists():
        content = agents.read_text(encoding='utf-8')
        if 'Quick Start' not in content and 'Quick Reference' not in content:
            issues.append("AGENTS.md missing: Quick Start section")
        if 'Workflow' not in content:
            issues.append("AGENTS.md missing: Workflow section")
    else:
        issues.append("AGENTS.md (or awareness-guide.md) not found")

    # Adoption Blueprint: Must have Adoption Checklist
    blueprint = sap_dir / 'adoption-blueprint.md'
    if blueprint.exists():
        content = blueprint.read_text(encoding='utf-8')
        if 'Adoption Checklist' not in content:
            issues.append("adoption-blueprint.md missing: Adoption Checklist")
    else:
        issues.append("adoption-blueprint.md not found")

    # Ledger: Must have Version History
    ledger = sap_dir / 'ledger.md'
    if ledger.exists():
        content = ledger.read_text(encoding='utf-8')
        if 'Version History' not in content:
            issues.append("ledger.md missing: Version History")
    else:
        issues.append("ledger.md not found")

    return {'passed': len(issues) == 0, 'issues': issues}

def verify_links(sap_name: str) -> dict:
    """Verify markdown links using SAP-016 (Link Validation & Reference Management)

    Delegates to scripts/validate-links.py instead of duplicating logic.
    This ensures SAP-050 uses the production-tested SAP-016 infrastructure.
    """
    import subprocess
    import json

    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')

    # Delegate to SAP-016's validate-links.py
    result = subprocess.run(
        ['python', 'scripts/validate-links.py', str(sap_dir), '--json'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {
            'passed': True,
            'broken_links': [],
            'validated_by': 'SAP-016'
        }
    else:
        try:
            # Parse SAP-016's JSON output
            data = json.loads(result.stdout)
            broken_links = []

            # SAP-016 returns: {"results": [{"file": ..., "broken_links": [...]}]}
            for file_result in data.get('results', []):
                file_path = file_result.get('file', '')
                for broken in file_result.get('broken_links', []):
                    broken_links.append({
                        'file': Path(file_path).name,
                        'link': broken.get('link_url', ''),
                        'text': broken.get('link_text', '')
                    })

            return {
                'passed': False,
                'broken_links': broken_links,
                'validated_by': 'SAP-016',
                'total_broken': data.get('broken_count', len(broken_links))
            }
        except (json.JSONDecodeError, KeyError):
            # Fallback: parse output text for broken links
            broken = []
            for line in result.stdout.split('\n'):
                if 'broken' in line.lower() or 'invalid' in line.lower():
                    broken.append({
                        'file': 'unknown',
                        'link': line.strip(),
                        'text': ''
                    })

            return {
                'passed': len(broken) == 0,
                'broken_links': broken,
                'validated_by': 'SAP-016 (fallback parser)'
            }

def verify_all(sap_name: str) -> dict:
    """Run all verifications"""
    structure = verify_structure(sap_name)
    completeness = verify_completeness(sap_name)
    links = verify_links(sap_name)

    all_passed = structure['passed'] and completeness['passed'] and links['passed']

    return {
        'sap_name': sap_name,
        'passed': all_passed,
        'structure': structure,
        'completeness': completeness,
        'links': links
    }

# CLI
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sap_verify.py <sap-name> [<sap-name> ...]")
        print("\nExamples:")
        print("  python sap_verify.py task-tracking")
        print("  python sap_verify.py capability-registry-discovery namespace-resolution")
        sys.exit(1)

    sap_names = sys.argv[1:]

    results = []
    for sap_name in sap_names:
        result = verify_all(sap_name)
        results.append(result)

        print(f"\n{'='*60}")
        print(f"SAP: {sap_name}")
        print(f"{'='*60}")

        # Structure
        if result['structure']['passed']:
            print("[PASS] Structure: all required artifacts present")
        else:
            print(f"[FAIL] Structure")
            print(f"  Missing: {', '.join(result['structure']['missing'])}")

        # Completeness
        if result['completeness']['passed']:
            print("[PASS] Completeness: all required sections present")
        else:
            print(f"[FAIL] Completeness ({len(result['completeness']['issues'])} issues)")
            for issue in result['completeness']['issues']:
                print(f"  - {issue}")

        # Links
        if result['links']['passed']:
            print("[PASS] Links: no broken links")
        else:
            print(f"[FAIL] Links ({len(result['links']['broken_links'])} broken links)")
            for link in result['links']['broken_links']:
                print(f"  - {link['file']}: '{link['text']}' -> {link['link']}")

        # Overall
        print(f"\nOverall: {'[PASS]' if result['passed'] else '[FAIL]'}")

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: Verified {len(results)} SAP(s)")
    print(f"{'='*60}")
    passed_count = sum(1 for r in results if r['passed'])
    failed_count = len(results) - passed_count
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    # Exit code
    sys.exit(0 if failed_count == 0 else 1)
