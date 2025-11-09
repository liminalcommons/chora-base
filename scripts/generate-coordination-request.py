#!/usr/bin/env python3
"""
Generate Coordination Request - CLI tool for inbox artifact generation

Part of SAP-001 Inbox Coordination Protocol implementation.
Week 5: Standalone generator (Path C).

Usage:
    python3 scripts/generate-coordination-request.py \\
        --title "Update documentation" \\
        --description "Update README with new features" \\
        --to-repo "chora-workspace" \\
        --priority P2 \\
        --urgency next_sprint

    # Or with context file:
    python3 scripts/generate-coordination-request.py --context context.json

    # Preview only (no file written):
    python3 scripts/generate-coordination-request.py --context context.json --preview
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from inbox_generator.core.config_loader import ConfigLoader
from inbox_generator.core.assembler import ArtifactAssembler


def load_context_from_args(args) -> Dict[str, Any]:
    """
    Build context from command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Context dictionary
    """
    context = {}

    # Required fields
    if args.title:
        context['title'] = args.title
    if args.description:
        context['description'] = args.description
    if args.to_repo:
        context['to_repo'] = args.to_repo

    # Optional fields
    if args.priority:
        context['priority'] = args.priority
    if args.urgency:
        context['urgency'] = args.urgency
    if args.from_repo:
        context['from_repo'] = args.from_repo

    # Structured fields (as JSON strings or lists)
    if args.deliverables:
        context['deliverables'] = args.deliverables
    if args.acceptance_criteria:
        context['acceptance_criteria'] = args.acceptance_criteria
    if args.background:
        context['background'] = args.background
    if args.rationale:
        context['rationale'] = args.rationale

    return context


def main():
    parser = argparse.ArgumentParser(
        description="Generate coordination request artifacts using config-driven approach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Input mode
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--context',
        type=Path,
        help='Path to context JSON file'
    )
    input_group.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode (prompts for all fields)'
    )

    # Direct arguments (alternative to context file)
    parser.add_argument('--title', help='Request title')
    parser.add_argument('--description', help='Detailed description')
    parser.add_argument('--to-repo', help='Target repository')
    parser.add_argument('--from-repo', default='github.com/liminalcommons/chora-base', help='Source repository')
    parser.add_argument('--priority', choices=['P0', 'P1', 'P2', 'P3'], help='Priority level')
    parser.add_argument('--urgency', choices=['blocks_sprint', 'next_sprint', 'planned', 'exploratory'], help='Urgency level')
    parser.add_argument('--deliverables', nargs='+', help='List of deliverables')
    parser.add_argument('--acceptance-criteria', nargs='+', help='List of acceptance criteria')
    parser.add_argument('--background', help='Background/context information')
    parser.add_argument('--rationale', help='Rationale for the request')

    # Configuration
    parser.add_argument(
        '--artifact-config',
        default='coordination-request-artifact',
        help='Artifact config ID (default: coordination-request-artifact)'
    )
    parser.add_argument(
        '--content-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'inbox' / 'content-blocks',
        help='Directory containing content configs'
    )

    # Output
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (overrides artifact config default)'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview only (do not write file)'
    )

    # AI configuration
    parser.add_argument(
        '--ai-model',
        default='claude-sonnet-4-5-20250929',
        help='AI model for augmented generation (default: claude-sonnet-4-5-20250929)'
    )

    # Processing
    parser.add_argument(
        '--post-process',
        action='store_true',
        help='Run post-processing pipeline after generation'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Load context
    if args.context:
        # Load from JSON file
        with open(args.context, 'r', encoding='utf-8') as f:
            context = json.load(f)
        if args.verbose:
            print(f"✓ Loaded context from: {args.context}")
    elif args.interactive:
        # Interactive mode
        context = interactive_context_builder()
    else:
        # Build from command-line arguments
        context = load_context_from_args(args)

        # Validate required fields
        required = ['title', 'description', 'to_repo']
        missing = [f for f in required if f not in context or not context[f]]
        if missing:
            parser.error(f"Missing required fields: {missing}")

    if args.verbose:
        print(f"Context keys: {list(context.keys())}")

    # Initialize config loader
    config_loader = ConfigLoader(
        content_dir=args.content_dir,
        artifact_dir=args.content_dir  # Same directory for now
    )

    # Initialize assembler
    assembler = ArtifactAssembler(
        config_loader=config_loader,
        ai_model=args.ai_model
    )

    try:
        # Generate artifact
        if args.preview:
            print("\n=== PREVIEW MODE ===\n")
            preview = assembler.preview(args.artifact_config, context)
            print(preview)
            print("\n=== END PREVIEW ===\n")
            artifact_data = json.loads(preview)
        else:
            artifact_data = assembler.assemble(
                args.artifact_config,
                context,
                output_path=args.output
            )

        # Post-process if requested
        if args.post_process and not args.preview:
            output_file = args.output or Path('inbox/draft') / f"{artifact_data.get('title', 'artifact')}.json"
            print(f"\n✓ Running post-processing on: {output_file}")

            import subprocess
            result = subprocess.run(
                ['python3', 'scripts/process-generated-artifact.py', str(output_file), '--verbose'],
                capture_output=True,
                text=True
            )

            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            if result.returncode != 0:
                print(f"✗ Post-processing failed with exit code {result.returncode}")
                sys.exit(result.returncode)

            print("✓ Post-processing complete")

        print("\n✓ Generation successful")

    except Exception as e:
        print(f"\n✗ Generation failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

            traceback.print_exc()
        sys.exit(1)


def interactive_context_builder() -> Dict[str, Any]:
    """
    Build context interactively by prompting user for each field.

    Returns:
        Context dictionary
    """
    print("\n=== Interactive Context Builder ===\n")

    context = {}

    # Required fields
    context['title'] = input("Title: ")
    context['description'] = input("Description: ")
    context['to_repo'] = input("To Repository: ")

    # Optional fields with defaults
    context['from_repo'] = input("From Repository [github.com/liminalcommons/chora-base]: ") or "github.com/liminalcommons/chora-base"
    context['priority'] = input("Priority [P0/P1/P2/P3]: ") or "P2"
    context['urgency'] = input("Urgency [blocks_sprint/next_sprint/planned/exploratory]: ") or "next_sprint"

    # Structured fields
    deliverables_str = input("Deliverables (comma-separated): ")
    if deliverables_str:
        context['deliverables'] = [d.strip() for d in deliverables_str.split(',')]

    acceptance_str = input("Acceptance Criteria (comma-separated): ")
    if acceptance_str:
        context['acceptance_criteria'] = [a.strip() for a in acceptance_str.split(',')]

    context['background'] = input("Background/Context: ")
    context['rationale'] = input("Rationale: ")

    print("\n=== Context Complete ===\n")

    return context


if __name__ == '__main__':
    main()
