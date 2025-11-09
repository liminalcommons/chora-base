#!/usr/bin/env python3
"""
SAP Synergy Discovery Tool

Analyzes SAP relationships and recommends next adoptions based on:
- Declared synergies in sap-catalog.json
- Co-adoption patterns (which SAPs are commonly used together)
- Dependency chains
- Reverse dependencies (impact analysis)

Usage:
    python scripts/discover-synergies.py SAP-004           # Discover synergies for SAP-004
    python scripts/discover-synergies.py --recommend       # Get personalized recommendations
    python scripts/discover-synergies.py --impact SAP-004  # See what depends on SAP-004
    python scripts/discover-synergies.py --visualize       # Show dependency graph (TODO)
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

class SynergyDiscovery:
    def __init__(self, catalog_path: Path):
        with open(catalog_path, 'r', encoding='utf-8') as f:
            self.catalog = json.load(f)

        self.saps = {sap['id']: sap for sap in self.catalog['saps']}
        self.synergies = self.catalog.get('synergies', [])
        self.anti_patterns = self.catalog.get('anti_patterns', [])

    def get_sap(self, sap_id: str) -> Dict[str, Any]:
        """Get SAP by ID."""
        return self.saps.get(sap_id)

    def find_synergies_for(self, sap_id: str) -> List[Dict]:
        """Find all synergies involving a SAP."""
        result = []
        for synergy in self.synergies:
            if sap_id in synergy['saps']:
                result.append(synergy)
        return result

    def find_anti_patterns_for(self, sap_id: str) -> List[Dict]:
        """Find anti-patterns involving a SAP."""
        result = []
        for anti_pattern in self.anti_patterns:
            if sap_id in anti_pattern['saps']:
                result.append(anti_pattern)
        return result

    def get_impact_analysis(self, sap_id: str) -> Dict:
        """Analyze what depends on this SAP."""
        sap = self.get_sap(sap_id)
        if not sap:
            return {}

        return {
            'sap_id': sap_id,
            'name': sap['name'],
            'direct_dependents': sap.get('dependents', []),
            'dependency_count': len(sap.get('dependents', [])),
            'is_foundational': len(sap.get('dependents', [])) > 10,
            'dependencies': sap.get('dependencies', []),
            'synergies': self.find_synergies_for(sap_id),
            'anti_patterns': self.find_anti_patterns_for(sap_id)
        }

    def recommend_next_saps(self, current_saps: List[str]) -> List[Dict]:
        """Recommend next SAPs based on current adoption."""
        recommendations = {}

        # Find synergies for current SAPs
        for sap_id in current_saps:
            for synergy in self.find_synergies_for(sap_id):
                # Get related SAPs
                related = [s for s in synergy['saps'] if s not in current_saps]
                for related_sap in related:
                    if related_sap not in recommendations:
                        recommendations[related_sap] = {
                            'sap_id': related_sap,
                            'name': self.get_sap(related_sap)['name'],
                            'synergy_score': 0,
                            'synergies': [],
                            'reason': []
                        }

                    # Add synergy info
                    recommendations[related_sap]['synergy_score'] += synergy.get('time_multiplier', 1.0)
                    recommendations[related_sap]['synergies'].append(synergy['name'])
                    recommendations[related_sap]['reason'].append(
                        f"{synergy['benefit']} ({synergy['time_multiplier']}x multiplier)"
                    )

        # Find dependencies not yet adopted
        for sap_id in current_saps:
            sap = self.get_sap(sap_id)
            for dep in sap.get('dependents', []):
                if dep not in current_saps and dep not in recommendations:
                    dep_sap = self.get_sap(dep)
                    recommendations[dep] = {
                        'sap_id': dep,
                        'name': dep_sap['name'],
                        'synergy_score': 0.5,
                        'synergies': [],
                        'reason': [f"Depends on {sap_id} (already adopted)"]
                    }

        # Sort by synergy score
        sorted_recs = sorted(
            recommendations.values(),
            key=lambda x: x['synergy_score'],
            reverse=True
        )

        return sorted_recs[:5]  # Top 5 recommendations

    def display_synergies(self, sap_id: str):
        """Display synergies for a SAP."""
        sap = self.get_sap(sap_id)
        if not sap:
            print(f"Error: SAP {sap_id} not found")
            return

        print(f"\n{'='*70}")
        print(f"Synergies for {sap_id} - {sap['name']}")
        print(f"{'='*70}\n")

        # Show direct info
        print(f"Status: {sap['status']}")
        print(f"Dependencies: {', '.join(sap.get('dependencies', [])) or 'None'}")
        print(f"Dependents: {len(sap.get('dependents', []))} SAPs depend on this\n")

        # Show synergies
        synergies = self.find_synergies_for(sap_id)
        if synergies:
            print(f"Strong Synergies ({len(synergies)} found):")
            print("-" * 70)
            for i, synergy in enumerate(synergies, 1):
                other_saps = [s for s in synergy['saps'] if s != sap_id]
                print(f"\n{i}. {synergy['name']}")
                print(f"   Type: {synergy['type']}")
                print(f"   With: {', '.join(other_saps)}")
                print(f"   Benefit: {synergy['benefit']}")
                print(f"   Time Multiplier: {synergy.get('time_multiplier', 'N/A')}x")
                print(f"   Co-adoption Rate: {synergy.get('adoption_rate', 'N/A') * 100:.0f}%")
        else:
            print("No explicit synergies documented")

        # Show anti-patterns
        anti_patterns = self.find_anti_patterns_for(sap_id)
        if anti_patterns:
            print(f"\n\nConflicts & Anti-Patterns ({len(anti_patterns)} found):")
            print("-" * 70)
            for i, anti in enumerate(anti_patterns, 1):
                other_saps = [s for s in anti['saps'] if s != sap_id]
                print(f"\n{i}. Conflict with: {', '.join(other_saps)}")
                print(f"   Type: {anti['type']}")
                print(f"   Reason: {anti['reason']}")
                print(f"   Severity: {anti['severity']}")
                print(f"   Resolution: {anti['resolution']}")

        # Show recommended next steps
        print(f"\n\nRecommended Next SAPs:")
        print("-" * 70)
        recs = self.recommend_next_saps([sap_id])
        if recs:
            for i, rec in enumerate(recs[:3], 1):
                print(f"\n{i}. {rec['sap_id']} - {rec['name']}")
                print(f"   Score: {rec['synergy_score']:.1f}x")
                print(f"   Reason: {'; '.join(rec['reason'])}")
        else:
            print("  No specific recommendations (consider reviewing SAP sets)")

        print(f"\n{'='*70}\n")

    def display_impact(self, sap_id: str):
        """Display impact analysis for a SAP."""
        impact = self.get_impact_analysis(sap_id)
        if not impact:
            print(f"Error: SAP {sap_id} not found")
            return

        print(f"\n{'='*70}")
        print(f"Impact Analysis for {sap_id} - {impact['name']}")
        print(f"{'='*70}\n")

        print(f"Direct Dependents: {impact['dependency_count']}")
        if impact['is_foundational']:
            print("[!] This is a FOUNDATIONAL SAP - many SAPs depend on it\n")

        if impact['direct_dependents']:
            print("SAPs that depend on this:")
            for dep in impact['direct_dependents']:
                dep_sap = self.get_sap(dep)
                print(f"  - {dep}: {dep_sap['name']}")
        else:
            print("No SAPs depend on this (leaf SAP)")

        print(f"\n{'='*70}\n")

def main():
    catalog_path = Path(__file__).parent.parent / "sap-catalog.json"
    discovery = SynergyDiscovery(catalog_path)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/discover-synergies.py SAP-004")
        print("  python scripts/discover-synergies.py --impact SAP-004")
        print("  python scripts/discover-synergies.py --recommend SAP-004 SAP-005")
        sys.exit(1)

    command = sys.argv[1]

    if command == "--impact":
        if len(sys.argv) < 3:
            print("Error: --impact requires SAP-ID")
            sys.exit(1)
        discovery.display_impact(sys.argv[2])

    elif command == "--recommend":
        if len(sys.argv) < 3:
            print("Error: --recommend requires at least one SAP-ID")
            sys.exit(1)
        current_saps = sys.argv[2:]
        print(f"\nRecommendations based on: {', '.join(current_saps)}")
        print("-" * 70)
        recs = discovery.recommend_next_saps(current_saps)
        for i, rec in enumerate(recs, 1):
            print(f"\n{i}. {rec['sap_id']} - {rec['name']}")
            print(f"   Synergy Score: {rec['synergy_score']:.1f}x")
            print(f"   Synergies: {', '.join(rec['synergies']) if rec['synergies'] else 'None'}")
            print(f"   Reason: {'; '.join(rec['reason'])}")

    else:
        # Default: show synergies for SAP
        discovery.display_synergies(command)

if __name__ == "__main__":
    main()
