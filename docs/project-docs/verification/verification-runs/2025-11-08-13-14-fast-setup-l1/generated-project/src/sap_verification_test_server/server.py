"""SAP Verification Test Server MCP Server.

This server implements the Model Context Protocol (MCP) following
Chora MCP Conventions v1.0 for tool/resource naming.

Tools are namespaced as: sapverify:tool_name
Resources use URI scheme: sapverify://type/id

Reference: https://github.com/liminalcommons/chora-base/blob/main/docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md
"""

import logging
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from fastmcp import FastMCP
from .mcp import (
    NAMESPACE,
    make_tool_name,
    validate_tool_name,
    make_resource_uri,
    validate_resource_uri,
)

# Configure logging
logger = logging.getLogger(__name__)

# === Version Resolution ===

def _get_version() -> str:
    """Get package version from installed metadata.

    Returns version from pyproject.toml (via package metadata) to ensure
    single source of truth. Falls back to development version if package
    is not installed (e.g., during development without editable install).

    Returns:
        Package version string (e.g., "1.5.0") or "0.0.0-dev" if not found.
    """
    try:
        return version("sap_verification_test_server")
    except PackageNotFoundError:
        # Development fallback when package not installed
        return "0.0.0-dev"

# === MCP Server Instance ===

mcp = FastMCP(
    name="SAP Verification Test Server",
    version=_get_version(),
)

# === Example Tools ===

# Tool names are automatically namespaced via make_tool_name()
# Full name will be: sapverify:example_tool

@mcp.tool()
async def example_tool(message: str) -> dict[str, Any]:
    """Example tool demonstrating namespaced naming.

    Tool name: sapverify:example_tool

    Args:
        message: Example message parameter

    Returns:
        Dict with tool response

    Example:
        # Call via MCP client:
        await client.call_tool("sapverify:example_tool", {"message": "Hello"})
    """
    tool_name = make_tool_name("example_tool")

    # Validate naming convention
    validate_tool_name(tool_name, expected_namespace=NAMESPACE)

    logger.info("Tool called: {} with message: {}".format(tool_name, message))

    return {
        "status": "success",
        "message": message,
        "tool": tool_name,
        "namespace": NAMESPACE,
    }


@mcp.tool()
async def hello_world() -> str:
    """Simple hello world tool.

    Tool name: sapverify:hello_world

    Returns:
        Greeting message
    """
    return "Hello from {}!".format(NAMESPACE)


# === Example Resources ===

# Resources use URI scheme: sapverify://type/id

@mcp.resource(uri=make_resource_uri("capabilities", "server"))
async def get_capabilities() -> dict[str, Any]:
    """Server capabilities resource.

    Resource URI: sapverify://capabilities/server

    Returns:
        Server metadata and capabilities

    Example:
        # Access via MCP client:
        capabilities = await client.get_resource("sapverify://capabilities/server")
    """
    uri = make_resource_uri("capabilities", "server")
    validate_resource_uri(uri, expected_namespace=NAMESPACE)

    return {
        "name": "SAP Verification Test Server",
        "namespace": NAMESPACE,
        "version": _get_version(),
        "tools": [
            make_tool_name("example_tool"),
            make_tool_name("hello_world"),
        ],
        "resources": [
            make_resource_uri("capabilities", "server"),
        ],
        "conventions": "Chora MCP Conventions v1.0",
    }


# === Main Entry Point ===

def main() -> None:
    """Run the MCP server.

    This is the entry point registered in pyproject.toml:
        [project.scripts]
        sap-verification-test-server = "sap_verification_test_server.mcp.server:main"
    """
    logger.info("Starting SAP Verification Test Server MCP server...")
    logger.info("Namespace: {}".format(NAMESPACE))
    logger.info("Namespacing enabled: {}".format(True))
    mcp.run()


if __name__ == "__main__":
    main()