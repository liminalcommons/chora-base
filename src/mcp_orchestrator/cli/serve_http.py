"""
CLI command for starting HTTP server.

Command: mcp-orchestration-serve-http
"""

import argparse
import sys

from mcp_orchestrator.http.server import HTTPTransportServer


def serve_http_cli() -> int:
    """
    CLI entry point for HTTP server.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Start MCP Orchestration HTTP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server on default port (8000)
  mcp-orchestration-serve-http

  # Start server on custom port
  mcp-orchestration-serve-http --port 9000

  # Start server on localhost only
  mcp-orchestration-serve-http --host 127.0.0.1

  # Start server with custom host and port
  mcp-orchestration-serve-http --host 0.0.0.0 --port 8080

Environment variables:
  MCP_ORCHESTRATION_API_KEY    Static API key for X-API-Key authentication
        """,
    )

    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server bind address (default: 0.0.0.0)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Log level (default: info)",
    )

    args = parser.parse_args()

    try:
        # Create and run server
        server = HTTPTransportServer(host=args.host, port=args.port)
        server.run(log_level=args.log_level)

        return 0
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(serve_http_cli())
