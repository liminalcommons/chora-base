"""
CLI command for generating API tokens.

Command: mcp-orchestration-generate-token
"""

import argparse
import sys

from mcp_orchestrator.http.auth import get_auth_service


def generate_token_cli() -> str:
    """
    CLI entry point for token generation.

    Returns:
        Generated token (string)

    Side effects:
        Prints token to stdout
    """
    parser = argparse.ArgumentParser(
        description="Generate a new API token for HTTP authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a new token
  mcp-orchestration-generate-token

  # Save token to environment variable
  export MCP_HTTP_TOKEN=$(mcp-orchestration-generate-token | grep "Generated token:" | awk '{print $3}')

Usage:
  Use the generated token in HTTP requests:

  curl -H "Authorization: Bearer <token>" \\
    http://localhost:8000/v1/clients

Security:
  - Tokens are cryptographically secure (32 bytes, URL-safe base64)
  - Tokens do not expire in v0.2.0
  - Store tokens securely (environment variables, password managers)
  - Rotate tokens monthly for production use
        """,
    )

    parser.parse_args()

    try:
        # Get auth service and generate token
        auth_service = get_auth_service()
        token = auth_service.generate_token()

        # Print token information
        print("Token generated successfully!")
        print()
        print(f"Generated token: {token}")
        print()
        print("Usage in curl:")
        print(f'  curl -H "Authorization: Bearer {token}" \\')
        print("    http://localhost:8000/v1/clients")
        print()
        print("Usage in Python:")
        print("  import requests")
        print(f'  headers = {{"Authorization": "Bearer {token}"}}')
        print(
            '  response = requests.get("http://localhost:8000/v1/clients", headers=headers)'
        )
        print()
        print("Security:")
        print("  - Store this token securely")
        print("  - Do not commit to version control")
        print("  - Use environment variables: export MCP_HTTP_TOKEN='<token>'")
        print()

        return token
    except Exception as e:
        print(f"Error generating token: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    """Main entry point for CLI."""
    try:
        generate_token_cli()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
