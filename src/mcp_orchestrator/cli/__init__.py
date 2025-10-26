"""CLI commands for mcp-orchestration."""

# Import main from parent cli.py module for backward compatibility
import sys
if "mcp_orchestrator.cli" in sys.modules:
    # Prevent circular import by checking if parent module is already loaded
    from .. import cli as _parent_cli
    main = _parent_cli.main
else:
    # Defer import
    def main(argv=None):
        from .. import cli as _parent_cli
        return _parent_cli.main(argv)

from .serve_http import serve_http_cli
from .token import generate_token_cli

__all__ = ["main", "serve_http_cli", "generate_token_cli"]
