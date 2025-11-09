#!/usr/bin/env python3
"""
A-MEM Metrics Dashboard

Comprehensive ROI metrics dashboard for SAP-010 L3 validation.

Usage:
    python scripts/a-mem-metrics.py                  # Show all metrics
    python scripts/a-mem-metrics.py --json           # JSON output
    python scripts/a-mem-metrics.py --l3-check       # Check if meets L3 criteria
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def load_events(events_dir: Path, event_log: str) -> List[dict]:
    """Load events from a JSONL file"""
    log_path = events_dir / event_log

    if not log_path.exists():
        return []

    events = []
    with open(log_path, "r", encoding='utf-8') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    return events


def calculate_query_metrics(events_dir: Path) -> dict:
    """Calculate knowledge queries per session metric"""
    events = load_events(events_dir, "knowledge-queries.jsonl")

    if not events:
        return {
            "total_queries": 0,
            "avg_queries_per_session": 0.0,
            "target": 3.0,
            "meets_target": False
        }

    # Group by session
    sessions = {}
    for event in events:
        session_id = event.get("session_id", "unknown")
        if session_id not in sessions:
            sessions[session_id] = 0
        sessions[session_id] += 1

    avg_queries = sum(sessions.values()) / len(sessions) if sessions else 0.0

    return {
        "total_queries": len(events),
        "total_sessions": len(sessions),
        "avg_queries_per_session": avg_queries,
        "target": 3.0,
        "meets_target": avg_queries >= 3.0
    }


def calculate_reuse_metrics(knowledge_dir: Path, events_dir: Path) -> dict:
    """Calculate note reuse percentage"""
    if not knowledge_dir.exists():
        return {
            "total_notes": 0,
            "reused_notes": 0,
            "reuse_percentage": 0.0,
            "target": 50.0,
            "meets_target": False
        }

    total_notes = len(list(knowledge_dir.glob("*.md")))

    events = load_events(events_dir, "knowledge-reuse.jsonl")

    reused_note_ids = set(event.get("note_id") for event in events)
    total_time_saved = sum(event.get("time_saved_minutes", 0) for event in events)

    reuse_percentage = (len(reused_note_ids) / total_notes * 100) if total_notes > 0 else 0.0

    return {
        "total_notes": total_notes,
        "reused_notes": len(reused_note_ids),
        "reuse_percentage": reuse_percentage,
        "total_time_saved_minutes": total_time_saved,
        "target": 50.0,
        "meets_target": reuse_percentage >= 50.0
    }


def calculate_mistake_metrics(events_dir: Path) -> dict:
    """Calculate repeated mistake reduction percentage"""
    events = load_events(events_dir, "mistakes.jsonl")

    if not events:
        return {
            "total_mistakes": 0,
            "reduction_percentage": 0.0,
            "target": 30.0,
            "meets_target": False
        }

    # Parse timestamps
    for event in events:
        try:
            event["datetime"] = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        except Exception:
            event["datetime"] = datetime.now()

    events.sort(key=lambda e: e["datetime"])

    if len(events) < 2:
        return {
            "total_mistakes": len(events),
            "reduction_percentage": 0.0,
            "target": 30.0,
            "meets_target": False
        }

    # Split into baseline and recent
    latest = events[-1]["datetime"]
    midpoint = latest - timedelta(days=30)

    baseline_mistakes = [e for e in events if e["datetime"] < midpoint]
    recent_mistakes = [e for e in events if e["datetime"] >= midpoint]

    baseline_repeated = sum(1 for e in baseline_mistakes if e.get("recurrence", 0) > 1)
    recent_repeated = sum(1 for e in recent_mistakes if e.get("recurrence", 0) > 1)

    baseline_rate = (baseline_repeated / len(baseline_mistakes) * 100) if baseline_mistakes else 0
    recent_rate = (recent_repeated / len(recent_mistakes) * 100) if recent_mistakes else 0

    reduction = baseline_rate - recent_rate

    return {
        "total_mistakes": len(events),
        "baseline_repeated": baseline_repeated,
        "recent_repeated": recent_repeated,
        "reduction_percentage": reduction,
        "target": 30.0,
        "meets_target": reduction >= 30.0
    }


def calculate_restoration_metrics(events_dir: Path) -> dict:
    """Calculate context restoration time savings"""
    events = load_events(events_dir, "sessions.jsonl")

    if not events:
        return {
            "total_sessions": 0,
            "time_saved_percentage": 0.0,
            "target": 80.0,
            "meets_target": False
        }

    starts = [e for e in events if e.get("action") == "start"]
    with_memory = [e for e in starts if e.get("context_restored_from_memory")]
    baseline = [e for e in starts if not e.get("context_restored_from_memory")]

    avg_with_memory = (
        sum(e.get("restoration_time_seconds", 0) for e in with_memory) / len(with_memory)
        if with_memory else 0.0
    )

    avg_baseline = (
        sum(e.get("manual_context_baseline_seconds", 0) for e in baseline) / len(baseline)
        if baseline else 180.0
    )

    if not baseline and with_memory:
        avg_baseline = with_memory[0].get("manual_context_baseline_seconds", 180.0)

    time_saved_pct = ((avg_baseline - avg_with_memory) / avg_baseline * 100) if avg_baseline > 0 else 0.0

    return {
        "total_sessions": len(starts),
        "with_memory_sessions": len(with_memory),
        "avg_restoration_with_memory_seconds": avg_with_memory,
        "avg_restoration_baseline_seconds": avg_baseline,
        "time_saved_percentage": time_saved_pct,
        "target": 80.0,
        "meets_target": time_saved_pct >= 80.0
    }


def check_l3_criteria(metrics: dict) -> dict:
    """Check if all L3 criteria are met"""
    criteria = {
        "multi_adopter": metrics.get("multi_adopter", {}).get("meets_target", False),
        "knowledge_queries": metrics.get("knowledge_queries", {}).get("meets_target", False),
        "note_reuse": metrics.get("note_reuse", {}).get("meets_target", False),
        "mistake_reduction": metrics.get("mistake_reduction", {}).get("meets_target", False),
        "context_restoration": metrics.get("context_restoration", {}).get("meets_target", False)
    }

    all_met = all(criteria.values())

    return {
        "criteria": criteria,
        "all_met": all_met,
        "met_count": sum(criteria.values()),
        "total_count": len(criteria)
    }


def main():
    parser = argparse.ArgumentParser(
        description="A-MEM metrics dashboard for ROI validation"
    )
    parser.add_argument(
        "--memory-dir",
        default=".chora/memory",
        help="A-MEM directory (default: .chora/memory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output metrics as JSON"
    )
    parser.add_argument(
        "--l3-check",
        action="store_true",
        help="Check if meets L3 criteria"
    )

    args = parser.parse_args()

    # Resolve paths
    memory_dir = Path(args.memory_dir)
    knowledge_dir = memory_dir / "knowledge"
    events_dir = memory_dir / "events"

    # Gather all metrics
    metrics = {
        "knowledge_queries": calculate_query_metrics(events_dir),
        "note_reuse": calculate_reuse_metrics(knowledge_dir, events_dir),
        "mistake_reduction": calculate_mistake_metrics(events_dir),
        "context_restoration": calculate_restoration_metrics(events_dir)
    }

    # Multi-adopter metric (hardcoded for now)
    metrics["multi_adopter"] = {
        "adopters": ["chora-base", "chora-compose"],
        "count": 2,
        "target": 2,
        "meets_target": True
    }

    # L3 criteria check
    l3_check = check_l3_criteria(metrics)

    # Output
    if args.json:
        output = {
            "metrics": metrics,
            "l3_criteria": l3_check,
            "generated": datetime.utcnow().isoformat() + "Z"
        }
        print(json.dumps(output, indent=2))
        return 0

    # Human-readable output
    print("=" * 80)
    print("A-MEM Adoption Metrics Dashboard (SAP-010)")
    print("=" * 80)
    print()

    print("📊 Multi-Adopter Validation")
    print(f"   Adopters: {', '.join(metrics['multi_adopter']['adopters'])}")
    print(f"   Count: {metrics['multi_adopter']['count']}")
    print(f"   Target: ≥{metrics['multi_adopter']['target']}")
    print(f"   Status: {'✅ Met' if metrics['multi_adopter']['meets_target'] else '❌ Not met'}")
    print()

    print("🔍 Knowledge Queries Per Session")
    print(f"   Total queries: {metrics['knowledge_queries']['total_queries']}")
    print(f"   Total sessions: {metrics['knowledge_queries']['total_sessions']}")
    print(f"   Avg queries/session: {metrics['knowledge_queries']['avg_queries_per_session']:.1f}")
    print(f"   Target: ≥{metrics['knowledge_queries']['target']:.0f}")
    print(f"   Status: {'✅ Met' if metrics['knowledge_queries']['meets_target'] else '❌ Not met'}")
    print()

    print("♻️  Note Reuse Percentage")
    print(f"   Total notes: {metrics['note_reuse']['total_notes']}")
    print(f"   Reused notes: {metrics['note_reuse']['reused_notes']}")
    print(f"   Reuse percentage: {metrics['note_reuse']['reuse_percentage']:.1f}%")
    print(f"   Time saved: {metrics['note_reuse']['total_time_saved_minutes']} minutes")
    print(f"   Target: ≥{metrics['note_reuse']['target']:.0f}%")
    print(f"   Status: {'✅ Met' if metrics['note_reuse']['meets_target'] else '❌ Not met'}")
    print()

    print("🔄 Repeated Mistake Reduction")
    print(f"   Total mistakes: {metrics['mistake_reduction']['total_mistakes']}")
    print(f"   Reduction: {metrics['mistake_reduction']['reduction_percentage']:.1f}%")
    print(f"   Target: ≥{metrics['mistake_reduction']['target']:.0f}%")
    print(f"   Status: {'✅ Met' if metrics['mistake_reduction']['meets_target'] else '❌ Not met'}")
    print()

    print("⚡ Context Restoration Time Saved")
    print(f"   Total sessions: {metrics['context_restoration']['total_sessions']}")
    print(f"   With A-MEM: {metrics['context_restoration']['with_memory_sessions']}")
    print(f"   Avg time (A-MEM): {metrics['context_restoration']['avg_restoration_with_memory_seconds']:.1f}s")
    print(f"   Avg time (baseline): {metrics['context_restoration']['avg_restoration_baseline_seconds']:.1f}s")
    print(f"   Time saved: {metrics['context_restoration']['time_saved_percentage']:.1f}%")
    print(f"   Target: ≥{metrics['context_restoration']['target']:.0f}%")
    print(f"   Status: {'✅ Met' if metrics['context_restoration']['meets_target'] else '❌ Not met'}")
    print()

    if args.l3_check:
        print("=" * 80)
        print("L3 Criteria Check")
        print("=" * 80)
        print()

        for criterion, met in l3_check["criteria"].items():
            status = "✅ Met" if met else "❌ Not met"
            print(f"   {criterion}: {status}")

        print()
        print(f"Overall: {l3_check['met_count']}/{l3_check['total_count']} criteria met")

        if l3_check["all_met"]:
            print("✅ SAP-010 meets all L3 criteria!")
        else:
            print("⏳ SAP-010 does not yet meet all L3 criteria")

    return 0


if __name__ == "__main__":
    sys.exit(main())
