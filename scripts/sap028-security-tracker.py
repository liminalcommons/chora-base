#!/usr/bin/env python3
"""
SAP-028 Security Incident Tracker

Tracks security incidents and secret audits for SAP-028 adopters.

Usage:
    # Log security incident
    python scripts/sap028-security-tracker.py incident --project my-package --type token_leak

    # Perform secret audit
    python scripts/sap028-security-tracker.py audit --project my-package --secrets 0

    # Show metrics
    python scripts/sap028-security-tracker.py --metrics
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def load_events(events_path: Path) -> List[dict]:
    """Load security events from JSONL file"""
    if not events_path.exists():
        return []

    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def log_incident_event(
    project: str,
    incident_type: str,
    severity: str,
    resolved: bool,
    events_path: Path
) -> dict:
    """Log security incident event"""
    event = {
        "event_type": "sap028_security_incident",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": project,
        "incident_type": incident_type,  # "token_leak", "unauthorized_publish", etc.
        "severity": severity,  # "low", "medium", "high", "critical"
        "resolved": resolved,
        "tags": ["sap-028", "security", "incident", "roi-tracking"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def log_audit_event(
    project: str,
    secrets_count: int,
    publishing_method: str,
    pep740_enabled: bool,
    events_path: Path
) -> dict:
    """Log secret audit event"""
    event = {
        "event_type": "sap028_secret_audit",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": project,
        "pypi_api_token_count": secrets_count,
        "publishing_method": publishing_method,  # "oidc" or "token"
        "pep740_enabled": pep740_enabled,
        "compliant": secrets_count == 0 and publishing_method == "oidc",
        "tags": ["sap-028", "security", "audit", "roi-tracking"]
    }

    # Append to events log
    with open(events_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def calculate_metrics(events_path: Path) -> dict:
    """Calculate security metrics"""
    events = load_events(events_path)

    incidents = [e for e in events if e.get("event_type") == "sap028_security_incident"]
    audits = [e for e in events if e.get("event_type") == "sap028_secret_audit"]

    unresolved_incidents = [i for i in incidents if not i.get("resolved")]
    compliant_audits = [a for a in audits if a.get("compliant")]

    total_secrets = sum(a.get("pypi_api_token_count", 0) for a in audits)
    oidc_projects = sum(1 for a in audits if a.get("publishing_method") == "oidc")
    pep740_projects = sum(1 for a in audits if a.get("pep740_enabled"))

    return {
        "total_incidents": len(incidents),
        "unresolved_incidents": len(unresolved_incidents),
        "resolved_incidents": len(incidents) - len(unresolved_incidents),
        "total_audits": len(audits),
        "compliant_projects": len(compliant_audits),
        "non_compliant_projects": len(audits) - len(compliant_audits),
        "total_secrets_found": total_secrets,
        "oidc_projects": oidc_projects,
        "token_projects": len(audits) - oidc_projects,
        "pep740_enabled_projects": pep740_projects,
        "target_incidents": 0,
        "meets_target": len(unresolved_incidents) == 0
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track SAP-028 security incidents and audits"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["incident", "audit"],
        help="Log incident or perform audit"
    )
    parser.add_argument(
        "--project",
        help="Project name"
    )
    parser.add_argument(
        "--type",
        choices=["token_leak", "unauthorized_publish", "attestation_failure", "other"],
        help="Incident type (for 'incident' action)"
    )
    parser.add_argument(
        "--severity",
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Incident severity (for 'incident' action)"
    )
    parser.add_argument(
        "--resolved",
        action="store_true",
        help="Incident resolved (for 'incident' action)"
    )
    parser.add_argument(
        "--secrets",
        type=int,
        help="Number of PYPI_API_TOKEN secrets found (for 'audit' action)"
    )
    parser.add_argument(
        "--method",
        choices=["oidc", "token"],
        default="oidc",
        help="Publishing method (for 'audit' action)"
    )
    parser.add_argument(
        "--pep740",
        action="store_true",
        help="PEP 740 attestations enabled (for 'audit' action)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show security metrics"
    )
    parser.add_argument(
        "--events-dir",
        default=".chora/memory/events",
        help="Events directory"
    )

    args = parser.parse_args()

    events_dir = Path(args.events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    events_path = events_dir / "sap028-security.jsonl"

    if args.metrics:
        metrics = calculate_metrics(events_path)
        print(f"SAP-028 Security Metrics")
        print(f"=========================")
        print(f"")
        print(f"Security Incidents:")
        print(f"  Total incidents: {metrics['total_incidents']}")
        print(f"  Unresolved: {metrics['unresolved_incidents']}")
        print(f"  Resolved: {metrics['resolved_incidents']}")
        print(f"  Target: 0 unresolved")
        print(f"  Status: {'✅ Met' if metrics['meets_target'] else '❌ Not met'}")
        print(f"")
        print(f"Secret Audits:")
        print(f"  Total audits: {metrics['total_audits']}")
        print(f"  Compliant projects: {metrics['compliant_projects']}")
        print(f"  Non-compliant: {metrics['non_compliant_projects']}")
        print(f"  Total PYPI_API_TOKEN secrets found: {metrics['total_secrets_found']}")
        print(f"")
        print(f"Adoption Breakdown:")
        print(f"  OIDC publishing: {metrics['oidc_projects']} projects")
        print(f"  Token-based: {metrics['token_projects']} projects")
        print(f"  PEP 740 enabled: {metrics['pep740_enabled_projects']} projects")
        return 0

    if not args.action or not args.project:
        parser.error("action and --project required (or use --metrics)")

    if args.action == "incident":
        if not args.type:
            parser.error("--type required for 'incident' action")

        event = log_incident_event(
            project=args.project,
            incident_type=args.type,
            severity=args.severity,
            resolved=args.resolved,
            events_path=events_path
        )

        status = "✅ Resolved" if args.resolved else "⚠️  Unresolved"
        print(f"🔒 Security incident logged for '{args.project}': {status}")
        print(f"   Type: {args.type}")
        print(f"   Severity: {args.severity}")

    elif args.action == "audit":
        if args.secrets is None:
            parser.error("--secrets required for 'audit' action")

        event = log_audit_event(
            project=args.project,
            secrets_count=args.secrets,
            publishing_method=args.method,
            pep740_enabled=args.pep740,
            events_path=events_path
        )

        compliant = args.secrets == 0 and args.method == "oidc"
        status = "✅ Compliant" if compliant else "⚠️  Non-compliant"
        print(f"🔍 Security audit complete for '{args.project}': {status}")
        print(f"   PYPI_API_TOKEN secrets found: {args.secrets}")
        print(f"   Publishing method: {args.method}")
        print(f"   PEP 740 attestations: {'✅ Enabled' if args.pep740 else '❌ Not enabled'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
